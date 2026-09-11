"""Delta training and the rank-one write for ROME.

Adapted from the reference implementation at https://github.com/kmeng01/rome
(MIT; licence text reproduced in THIRD_PARTY_LICENSES.md). Paper: Meng, K., Bau, D., Andonian, A. and
Belinkov, Y. (2022) 'Locating and editing factual associations in GPT',
Advances in Neural Information Processing Systems (NeurIPS). arXiv:2202.05262.

Follows the reference: `train_delta` is the v* optimisation of rome/compute_v.py,
including the KL penalty, the norm clamp and the weight-decay term; `apply_edit` is
the rank-one weight write of rome/rome_main.py. The module constants below are the
paper's reported hyper-parameters.
"""

import torch

from utils.edit_utils import get_subject_token_range
from utils.model_state import mlp_block, mlp_proj
import torch.nn.functional as F

N_OPTIM_STEPS = 20
LR = 5e-1
WEIGHT_DECAY_FACTOR = 0.5

KL_FACTOR = 0.0625
CLAMP_NORM_FACTOR = 4  # delta norm capped at this × target_init norm


# Follows the reference: the v* optimisation of rome/compute_v.py.
def train_delta(
    model, tokenizer, prompt, subject, target_new, layer, card,
    context_templates=None, lr=LR, n_optim_steps=N_OPTIM_STEPS,
    clamp_norm_factor=CLAMP_NORM_FACTOR, weight_decay_factor=WEIGHT_DECAY_FACTOR,
):
    """
    Find delta (shape [1600]) such that adding it to the MLP output at the
    subject position at layer L makes the model predict target_new.

    Returns (target, target_init):
      target_init = original MLP output at that position, shape [1600]
      target = target_init + delta, shape [1600]
    """
    device = next(model.parameters()).device  # not DEVICE
    if context_templates is None:
        context_templates = ["{}"]

    target_ids = tokenizer(" " + target_new, return_tensors="pt",
                           add_special_tokens=False).input_ids[0].to(device)


    target_prefix = tokenizer.decode(target_ids[:-1])

    rewriting_prompts = [t.format(prompt) + target_prefix for t in context_templates]
    kl_prompt = f"{subject} is a"
    all_prompts = rewriting_prompts + [kl_prompt]
    n_rewrite = len(rewriting_prompts)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    input_tok = tokenizer(all_prompts, return_tensors="pt", padding=True).to(device)


    rewriting_targets = torch.full(
        (n_rewrite, input_tok["input_ids"].shape[1]), -100, device=device, dtype=torch.long
    )
    for i in range(n_rewrite):
        ex_len = int(input_tok["attention_mask"][i].sum())
        rewriting_targets[i, ex_len - n_target : ex_len] = target_ids


    lookup_idxs = []
    for p in all_prompts:
        subj_range = get_subject_token_range(p, subject, tokenizer)
        lookup_idxs.append(subj_range[1] - 1)  # last subject token


    n_embd = card["model_dim"]  # 1600 gpt2-xl / 4096 llama3-8b


    delta = torch.zeros(n_embd, device=device, requires_grad=True)
    opt = torch.optim.Adam([delta], lr=lr)


    for p in model.parameters():
        p.requires_grad_(False)

    target_init = None
    kl_distr_init = None

    for step in range(n_optim_steps):
        opt.zero_grad()


        def make_hook():
            def hook(module, inp, out):
                nonlocal target_init
                if target_init is None:
                    # Capture original MLP output from the rewriting prompt (sequence 0)
                    target_init = out[0, lookup_idxs[0]].detach().clone()
                modified = out.clone()
                for i, idx in enumerate(lookup_idxs):
                    modified[i, idx] += delta
                return modified

            return hook

        handle = mlp_block(model, card, layer).register_forward_hook(make_hook())

        logits = model(**input_tok).logits
        handle.remove()

        log_probs = F.log_softmax(logits[:n_rewrite], dim=-1)
        gathered = torch.gather(
            log_probs, 2,
            torch.where(rewriting_targets != -100, rewriting_targets, 0).unsqueeze(2),
        ).squeeze(2)
        mask = (rewriting_targets != -100).float()
        nll_loss = (-(gathered * mask).sum(1) / n_target).mean()

        # KL loss: from KL prompt (sequence 1), actual last non-pad token
        kl_last_idx = input_tok["attention_mask"][n_rewrite].sum() - 1
        kl_logits = logits[n_rewrite : n_rewrite + 1, kl_last_idx]
        kl_log_probs = F.log_softmax(kl_logits, dim=-1)
        if kl_distr_init is None:
            kl_distr_init = kl_log_probs.detach().clone()
        kl_loss = KL_FACTOR * F.kl_div(
            kl_distr_init, kl_log_probs, log_target=True, reduction="batchmean"
        )

        wd_loss = weight_decay_factor * (delta.norm() / target_init.norm() ** 2)

        loss = nll_loss + kl_loss + wd_loss

        p_target = torch.exp(-nll_loss).item()
        print(
            f"    Step {step:2d}  loss={loss.item():.4f}  "
            f"nll={nll_loss.item():.4f}  kl={kl_loss.item():.4f}  "
            f"wd={wd_loss.item():.6f}  P({target_new.strip()})={p_target:.4f}"
        )

        if loss.item() < 0.05:
            print(f"    Converged at step {step}.")
            break

        if step < n_optim_steps - 1:
            loss.backward()
            opt.step()

            max_norm = clamp_norm_factor * target_init.norm()
            if delta.norm() > max_norm:
                with torch.no_grad():
                    delta[...] = delta * max_norm / delta.norm()

    target = target_init + delta.detach()
    return target, target_init


# Follows the reference: the rank-one weight write of rome/rome_main.py.
def apply_edit(model, layer, k_star, C_inv, target, target_init, card):
    """
    Apply a rank-one edit to the MLP weight at the specified layer. 
    
    Compute and apply:
        ΔW = (target - target_init) (C^-1 k*)^T / (k*^T C^-1 k*)

    to c_proj.weight at the target layer.

    - target_init = W k* (current MLP output for subject)
    - target = desired MLP output (from delta optimisation)
    - k* = MLP input for subject, shape [6400]
    - C^-1 = inverse key covariance, shape [6400, 6400]
    """
    k_star = k_star.float()

    left = k_star if C_inv is None else (C_inv.float() @ k_star)
    left = left / left.norm()

    r = (target - target_init).float()  # [1600]
    right = r / torch.dot(k_star, left)  # [1600]

    # Rank-1 update: outer product [6400] x [1600] -> [6400, 1600]
    upd = left.unsqueeze(1) @ right.unsqueeze(0)

    W = mlp_proj(model, card, layer).weight

    # cast down to the weight's dtype only at the point of application
    if upd.shape == W.shape:
        W.data += upd.to(W.dtype)
    elif upd.T.shape == W.shape:
        W.data += upd.T.to(W.dtype)
    else:
        raise ValueError(f"Shape mismatch: update {upd.shape} vs weight {W.shape}")

    print(f"  Update norm: {upd.norm().item():.4f}")
