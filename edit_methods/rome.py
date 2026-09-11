"""ROME - rank-one editing of factual associations.

Adapted from the reference implementation at https://github.com/kmeng01/rome
(MIT; licence text reproduced in THIRD_PARTY_LICENSES.md). Paper: Meng, K., Bau, D., Andonian, A. and
Belinkov, Y. (2022) 'Locating and editing factual associations in GPT',
Advances in Neural Information Processing Systems (NeurIPS). arXiv:2202.05262.

Follows the reference: the covariance handling in `load_inv_covariance` and the
context-template averaging in `compute_k_star` (the paper's u* estimate). The
rank-one update itself lives in utils/edit_training.py.

Author's own: `rome_edit`, the harness wrapper, config threading and drift return.
"""

import os
from pathlib import Path

import torch

from utils.edit_training import apply_edit, train_delta
from utils.edit_utils import CONTEXT_TEMPLATES, get_subject_token_range
from utils.model_state import mlp_proj

device = "cuda" if torch.cuda.is_available() else "cpu"


# Follows the reference implementation's covariance handling (rome/compute_u.py).
def load_inv_covariance(path, COV_REG):
    """Load pre-computed C, regularise, invert. Returns C^-1 on `device`."""
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Missing covariance: {path}. Run scripts/compute_covariances.py first."
        )
    C = torch.load(path, map_location=device).float()
    d = C.shape[0]
    C_reg = C + COV_REG * torch.eye(d, device=device)
    try:
        C_inv = torch.inverse(C_reg)
    except RuntimeError:
        print("  (Falling back to CPU for matrix inversion)")
        C_inv = torch.inverse(C_reg.cpu()).to(device)
    return C_inv


# Follows the reference: k* averaged over context templates (rome/compute_u.py).
def compute_k_star(model, tokenizer, prompt, subject, layer, card, context_templates=None):

    device = next(model.parameters()).device  # not DEVICE
    if context_templates is None:
        context_templates = ["{}"]

    all_keys = []

    for template in context_templates:
        full_prompt = template.format(prompt)
        input_ids = tokenizer(full_prompt, return_tensors="pt").input_ids.to(device)
        subject_range = get_subject_token_range(full_prompt, subject, tokenizer)
        last_subj = subject_range[1] - 1

        captured = {}

        def hook(module, inp, out):
            captured["k"] = inp[0][0, last_subj].detach().clone()

        handle = mlp_proj(model, card, layer).register_forward_hook(hook)
        with torch.no_grad():
            model(input_ids)
        handle.remove()

        all_keys.append(captured["k"])

    # Average across all templates
    k_star = torch.stack(all_keys).mean(0)
    return k_star


def rome_edit(self, model, tokenizer, edit_datas):
    # device = next(model.parameters()).device
    W_orig = mlp_proj(model, self.card, self.layer).weight.detach().clone()
    # mom2_adjustment off means no covariance term at all (EasyEdit's ROME/llama3-8b)
    if self.config.get("mom2_adjustment", True):
        cov_file = Path(self.covariances_path) / f"c_layer_{self.layer}.pt"
        C_inv = load_inv_covariance(cov_file, self.covariance_regularization)
    else:
        C_inv = None

    for i, f in enumerate(edit_datas):
        edit = f

        print(f"\n[{i}] editing: {edit.prompt!r} -> {edit.target_new!r}")
        k_star = compute_k_star(
            model,
            tokenizer,
            edit.construct_prompt(),
            edit.subject,
            self.layer,
            self.card,
            CONTEXT_TEMPLATES,
        )
        target, target_init = train_delta(
            model,
            tokenizer,
            edit.construct_prompt(),
            edit.subject,
            edit.target_new,
            self.layer,
            self.card,
            CONTEXT_TEMPLATES,
            lr=self.config.get("learning_rate", 5e-1),
            n_optim_steps=self.config.get("n_optim_steps", 20),
            clamp_norm_factor=self.config.get("clamp_norm_factor", 4),
            weight_decay_factor=self.config.get("weight_decay_factor", 0.5),
        )
        apply_edit(model, self.layer, k_star, C_inv, target, target_init, self.card)

    drift = (mlp_proj(model, self.card, self.layer).weight - W_orig).norm().item()

    return drift
