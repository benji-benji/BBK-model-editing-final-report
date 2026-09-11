"""AlphaEdit - null-space constrained knowledge editing.

Adapted from the reference implementation at https://github.com/jianghoucheng/AlphaEdit
(MIT; licence text reproduced in THIRD_PARTY_LICENSES.md). Paper: Fang, J., Jiang, H., Wang, K., Ma, Y.,
Wang, X., He, X. and Chua, T.-S. (2025) 'AlphaEdit: null-space constrained knowledge
editing for language models', ICLR. arXiv:2410.02355.

Follows the reference: `compute_delta_W_projected` implements the paper's projected
update, and the SVD null-space construction in `get_project`.

Author's own: the percentile cut in `get_project` (a deliberate departure from the
reference's fixed threshold), `compute_projections`, and `alphaedit_edit`, which
reuses the MEMIT stages rather than duplicating them.
"""

import os
from pathlib import Path

import torch

from edit_methods.memit import (
    apply_update,
    compute_keys,
    compute_z_batch,
    residual_distribute,
)


# Near-identical to the reference: the paper's projected update.
# The fp32 cast is the author's, for the bf16 model path.
def compute_delta_W_projected(K_l, R_l, P_l, L2):

    out_dtype = K_l.dtype
    K_l, R_l, P_l = K_l.float(), R_l.float(), P_l.float()

    A = P_l @ (K_l @ K_l.T) + L2 * torch.eye(K_l.shape[0], device=K_l.device)
    adj_k = torch.linalg.solve(A, P_l @ K_l)
    dW = (R_l @ adj_k.T).to(out_dtype)

    return dW


def compute_projections(method_config, card, device="cpu"):

    model_name = card["name"]
    out_dir = Path(f"artifacts/projections/{model_name}")
    out_dir.mkdir(parents=True, exist_ok=True)

    for layer in card["edit_layers"]:
        cov_path = f"artifacts/covariances/{model_name}/c_layer_{layer}.pt"
        P = get_project(method_config, cov_path, device=device)
        torch.save(P, out_dir / f"p_layer_{layer}.pt")
        print(f"layer {layer}: P{tuple(P.shape)} -> {out_dir}/p_layer_{layer}.pt")


# Follows the reference's SVD null-space construction. The percentile cut that
# replaces the reference's fixed threshold is the author's.
def get_project(method_config, path, device="cpu"):

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Missing covariance: {path}. Run scripts/compute_covariances.py first."
        )
    cov = torch.load(path, map_location="cpu").float().to(device)

    U, S, _ = torch.linalg.svd(cov, full_matrices=False)

    percentile = method_config["nullspace_percentile"]
    threshold = torch.quantile(S, percentile / 100.0)

    small_singular_indices = (S < threshold).nonzero(as_tuple=True)[0]

    d = S.shape[0]
    kept = len(small_singular_indices)
    print(
        f"    null space {kept}/{d} ({kept / d:.1%}) · p{percentile} cut "
        f"{threshold:.4e} · S range {S.min():.2e}-{S.max():.2e}"
    )

    P = U[:, small_singular_indices] @ U[:, small_singular_indices].T
    return P.cpu()


def alphaedit_edit(method, model, tokenizer, edit_datas, anyedit=False):
    card = method.card
    method_config = method.config
    edit_layers = card["edit_layers"]
    L1 = edit_layers[-1]
    model_name = card["name"]

    print("Computing Z (batched z-optimisation)...")
    Z, h_L1 = compute_z_batch(
        model,
        tokenizer,
        edit_datas,
        layer_L1=L1,
        method_config=method_config,
        card=card,
        anyedit=anyedit,
    )
    print("Computing keys at each editing layer...")
    K = compute_keys(
        model,
        tokenizer,
        edit_datas,
        edit_layers=edit_layers,
        card=card,
        anyedit=anyedit,
    )
    print("Distributing residual across layers...")
    R = residual_distribute(Z, h_L1, edit_layers, L1=L1)

    for l in edit_layers:
        p_file = Path(f"artifacts/projections/{model_name}/p_layer_{l}.pt")
        if not p_file.exists():
            raise FileNotFoundError(
                f"missing projection: {p_file}. Run scripts/compute_projections.py"
            )
        P_l = torch.load(p_file, map_location="cpu").to(Z.device).float()
        dW = compute_delta_W_projected(K[l], R[l], P_l, method_config["L2"])
        apply_update(model, l, dW, card)
        print(f" layer {l}: ||ΔW||={dW.norm().item():.4f}")
