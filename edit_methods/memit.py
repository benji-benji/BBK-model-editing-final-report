"""MEMIT - mass-editing memory in a transformer.

Adapted from the reference implementation at https://github.com/kmeng01/memit
(MIT; licence text reproduced in THIRD_PARTY_LICENSES.md). Paper: Meng, K., Sharma, A.S., Andonian, A.,
Belinkov, Y. and Bau, D. (2023) 'Mass-editing memory in a transformer',
International Conference on Learning Representations (ICLR). arXiv:2210.07229.

Follows the reference: the four stages of the MEMIT algorithm - `compute_z_batch`,
`compute_keys`, `residual_distribute` and `compute_delta_W` - and `apply_update`.

Author's own: `subject_end_in_ids`, `memit_edit`, threading the model card through
as a parameter, and the AnyEdit-compatibility branches.
"""

import json
from pathlib import Path

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer

from utils.edit_utils import get_subject_token_range
from utils.edit_utils import CONTEXT_TEMPLATES
from utils.model_state import layer_block, mlp_proj

def subject_end_in_ids(ids, subject, tokenizer):

    ids = list(ids)
    for candidate in (subject, " " + subject):
        sub = tokenizer.encode(candidate, add_special_tokens=False)
        for i in range(len(ids) - len(sub) + 1):
            if ids[i:i + len(sub)] == sub:
                return i + len(sub)
    raise ValueError(f"subject {subject!r} not found in ids")


# Follows the reference: MEMIT stage 1, z-optimisation at the final edit layer
# (memit/compute_z.py).
def compute_z_batch(
    model,
    tokenizer,
    edit_datas,
    layer_L1,
    method_config,
    card,
    anyedit: bool = False,
) -> tuple[torch.Tensor, torch.Tensor]:

    device = next(model.parameters()).device
    N = len(edit_datas)
  
    d_model = card["model_dim"]

    # ---- 1. Build batch (teacher-forced multi-token targets) ----

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"  # last_real = sum-1 assumes right padding

    rewrite_ids, target_ids_list, subj_pos = [], [], []

    for i, edit in enumerate(edit_datas):
        prompt = edit.construct_prompt()
        p_ids = tokenizer(prompt, add_special_tokens=False)["input_ids"]
        t_ids = tokenizer(" " + edit.target_new, add_special_tokens=False)["input_ids"]
        rewrite_ids.append(p_ids + t_ids)
        target_ids_list.append(t_ids)
        if anyedit:
            subj_pos.append(len(p_ids) - 1)  # last token of the context/prompt
        else:
  
            subj_pos.append(subject_end_in_ids(p_ids, edit.subject, tokenizer) - 1)

    # KL probe seqs = "{subject} is a" (unchanged; no target appended)
    kl_texts = [f"{edit.subject} is a" for edit in edit_datas]
    kl_ids = tokenizer(kl_texts, add_special_tokens=False)["input_ids"]
    for ids, edit in zip(kl_ids, edit_datas):
        # same coordinate system as kl_ids, which is also add_special_tokens=False
        subj_pos.append(subject_end_in_ids(ids, edit.subject, tokenizer) - 1)

    toks = tokenizer.pad({"input_ids": rewrite_ids + kl_ids}, return_tensors="pt").to(
        device
    )
    last_subj = torch.tensor(subj_pos, device=device)  # [2N]
    last_real = toks["attention_mask"].sum(dim=1) - 1  # [2N]

    labels = torch.full_like(toks["input_ids"], -100)
    for i in range(N):
        p_len = len(rewrite_ids[i]) - len(target_ids_list[i])
        t_len = len(target_ids_list[i])
        labels[i, p_len : p_len + t_len] = torch.tensor(
            target_ids_list[i], device=device
        )

    h_L1 = torch.zeros(N, d_model, device=device)

    def capture_hook(module, inp, out):
        hs = out[0] if isinstance(out, tuple) else out
        capture_hook.captured = hs.detach().clone()

    handle = layer_block(model, card, layer_L1).register_forward_hook(capture_hook)

    with torch.no_grad():
        model(**toks)
    handle.remove()

    captured_hs = capture_hook.captured
    for i in range(N):
        h_L1[i] = captured_hs[i, last_subj[i]]

    # ---- 4. Initialise Z and freeze model ----

    Z = h_L1.clone().detach().requires_grad_(True)

    for p in model.parameters():
        p.requires_grad_(False)

    opt = torch.optim.Adam([Z], lr=method_config["learning_rate"])

    kl_distr_init = None

    # ---- 5. Optimisation loop ----

    for step in range(method_config["n_optim_steps"]):
        opt.zero_grad()

        def write_hook(module, inp, out):
            hs = out[0] if isinstance(out, tuple) else out
            hs_new = hs.clone()
            for i in range(N):
                # rewrite sequence i
                hs_new[i, last_subj[i]] = Z[i].to(hs.dtype)
                # KL sequence N+i, patched with same Z[i]
                hs_new[N + i, last_subj[N + i]] = Z[i].to(hs.dtype)
            if isinstance(out, tuple):
                return (hs_new,) + out[1:]
            return hs_new

        handle = layer_block(model, card, layer_L1).register_forward_hook(write_hook)
        logits = model(**toks).logits
        handle.remove()

        # ---- NLL over the full target span (teacher-forced), rewrite seqs ----
        shift_logits = logits[:N, :-1, :]
        shift_labels = labels[:N, 1:]
        nll = F.cross_entropy(
            shift_logits.reshape(-1, shift_logits.size(-1)).float(),
            shift_labels.reshape(-1),
            ignore_index=-100,
        )

        # ---- KL on probe sequences, at last real token position ----

        kl_logits = logits[torch.arange(N, 2 * N, device=device), last_real[N:]]
        kl_log_probs = F.log_softmax(kl_logits.float(), dim=-1)
        if kl_distr_init is None:
            kl_distr_init = kl_log_probs.detach().clone()
        kl = method_config["kl_factor"] * F.kl_div(
            kl_distr_init, kl_log_probs, log_target=True, reduction="batchmean"
        )

        # ---- Weight decay on per-fact (Z - h_L1) ----
        delta_norms = (Z - h_L1).norm(dim=1)
        h_norms_sq = h_L1.norm(dim=-1) ** 2
        wd = (
            method_config["weight_decay_factor"]
            * (delta_norms / h_norms_sq).mean()
        )

        loss = nll + kl + wd
        p_new_mean = torch.exp(-nll).item()
        print(
            f"    Step {step:2d}  loss={loss.item():.4f}  "
            f"nll={nll.item():.4f}  kl={kl.item():.4f}  "
            f"wd={wd.item():.6f}  P(new)avg={p_new_mean:.4f}"
        )

        if step < method_config["n_optim_steps"]- 1:
            loss.backward()
            print(
                f"       grad_norm={Z.grad.norm().item() if Z.grad is not None else 'NONE'}"
            )
            opt.step()

            # Norm Clamping
            with torch.no_grad():
                max_norms = method_config["clamp_norm_factor"] * h_L1.norm(dim=-1)
                cur_norms = (Z - h_L1).norm(dim=-1)
                over = cur_norms > max_norms
                if over.any():
                    scale = torch.where(
                        over, max_norms / cur_norms, torch.ones_like(cur_norms)
                    )
                    Z.data = h_L1 + (Z.data - h_L1) * scale.unsqueeze(-1)

    return Z.detach(), h_L1


# Follows the reference: MEMIT stage 2, key estimation at each edit layer
# (memit/memit_main.py).
def compute_keys(
    model: AutoModelForCausalLM,
    tokenizer: AutoTokenizer,
    edit_datas,
    edit_layers: list[int],
    card,
    templates: list[str] | None = None,
    anyedit: bool = False,
) -> dict[int, torch.Tensor]:


    device = next(model.parameters()).device
    N = len(edit_datas)
    d_mlp = card["model_mlp_dim"]

    templates = templates if templates is not None else CONTEXT_TEMPLATES

    K = {l: torch.zeros(d_mlp, N, device=device) for l in edit_layers}

    for template in templates:

        prompts = [template.format(fact.construct_prompt()) for fact in edit_datas]


        last_subj = []
        for p, fact in zip(prompts, edit_datas):
            
            p_ids = tokenizer(p)["input_ids"]
            if anyedit:
                last_subj.append(len(p_ids) - 1)  # last token of the context
            else:
                last_subj.append(subject_end_in_ids(p_ids, fact.subject, tokenizer) - 1)


        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        toks = tokenizer(prompts, return_tensors="pt", padding=True).to(device)

        captured = {}  # {layer: [N, seq, d_mlp]}

        def make_hook(layer):
            def hook(module, inp, out):
                
                captured[layer] = inp[0].detach()

            return hook

        handles = [
            mlp_proj(model, card, l).register_forward_hook(make_hook(l))
            for l in edit_layers
        ]

        with torch.no_grad():
            model(**toks)
            for h in handles:
                h.remove()

        for l in edit_layers:
            for i in range(N):
                K[l][:, i] += captured[l][i, last_subj[i]]

    for l in edit_layers:
        K[l] /= len(templates)

    return K


# Follows the reference: MEMIT stage 3, residual spread evenly over the edit layers.
def residual_distribute(
    Z=torch.tensor,  # [N, d_model]
    h_l1=torch.tensor,
    edit_layers=list[int],
    L1=int,  # length of all layers
) -> dict[int, torch.Tensor]:
    delta = (Z - h_l1).T
    R = {l: delta / (L1 - l + 1) for l in edit_layers}
    return R


# Follows the reference: MEMIT stage 4, the closed-form weight delta
# (memit/memit_main.py).
def compute_delta_W(K_l, R_l, C_l, mom2_update_weight):

    C_l = C_l + 1e-4 * torch.eye(C_l.shape[0], device=C_l.device, dtype=C_l.dtype)
    
    A = (mom2_update_weight * C_l + K_l @ K_l.T).double()
    K_d = K_l.double()
    adj_k_d = torch.linalg.solve(A, K_d)

    resid = (A @ adj_k_d - K_d).norm() / K_d.norm()

    
    adj_k = adj_k_d.to(K_l.dtype)
    
    dW = R_l @ adj_k.T

    return dW


# Follows the reference implementation's in-place weight write.
def apply_update(
    model,
    layer: int,
    delta_W: torch.Tensor,
    card,
) -> None:

    W = model.get_submodule(card["mlp_proj_tmpl"].format(layer)).weight

    if delta_W.shape == W.shape:
        W.data += delta_W.to(W.dtype).to(W.device)
    elif delta_W.T.shape == W.shape:
        W.data += delta_W.T.to(W.dtype).to(W.device)
    else:
        raise ValueError(
            f"Shape mismatch: delta_W {tuple(delta_W.shape)} vs W {tuple(W.shape)}"
        )


def memit_edit(
    method,
    model: AutoModelForCausalLM,
    tokenizer: AutoTokenizer,
    edit_datas: list[dict],
    anyedit: bool = False,
    cov_path: str = None,
) -> None:

    method_config = method.config
    card = method.card
    edit_layers = card["edit_layers"]

    L1 = edit_layers[-1]

    L_top = max(edit_layers)
    W_orig = mlp_proj(model, card, L_top).weight.detach().clone()

    # Block B
    print("Computing Z (batched z-optimisation)...")
    Z, h_L1 = compute_z_batch(
        model, tokenizer, edit_datas, layer_L1=L1, method_config=method_config,
        card=card, anyedit=anyedit
    )

    # Block C
    print("Computing keys at each editing layer...")
    K = compute_keys(
        model,
        tokenizer,
        edit_datas,
        edit_layers=edit_layers,
        card=card,
        anyedit=anyedit,
    )

    # Block D
    print("Distributing residual across layers...")
    R = residual_distribute(Z, h_L1, edit_layers, L1=L1)

    cov_path = Path(cov_path)

    # Block F - per-layer update
    cov_dir = Path(cov_path)
    for l in edit_layers:
        c_file = cov_dir / f"c_layer_{l}.pt"
        if not c_file.exists():
            raise FileNotFoundError(
                f"covariance cache missing: {cov_path}\n"
                f"Run scripts/compute_covariances.py for model {card['name']!r}."
            )
        C_l = torch.load(c_file, weights_only=False).to(Z.device).float()
        dW = compute_delta_W(K[l], R[l], C_l, card["mom2_update_weight"])
        apply_update(model, l, dW, card)
        print(f" layer {l}: ||ΔW||={dW.norm().item():.4f}")

    if edit_layers is None:
        edit_layers = list(card["edit_layers"])

    drift = (mlp_proj(model, card, L_top).weight - W_orig).norm().item()

    return drift
