"""Precompute the MLP key covariance C = E[k kᵀ] per edit layer.

    uv run python -m scripts.compute_covariances                              # gpt2-xl, 1000 samples
    uv run python -m scripts.compute_covariances --device cuda -n 20000       # on a GPU pod
    uv run python -m scripts.compute_covariances --model llama3-8b --device cuda -n 20000

`k` is the fan-out activation the *second* MLP matrix reads — so C is captured as the
INPUT to the module the card's `mlp_proj_tmpl` names (GPT-2 `c_proj`, LLaMA `down_proj`).

C is the preservation term in the ROME/MEMIT weight solve: it records which directions in
key space the layer actually uses, so an edit can be steered into directions it rarely
uses. Saved as the raw MEAN second moment (diagonal ≈ 0.03 for GPT-2-XL, ≈ 0.0007 for
LLaMA-3-8B) — the `mom2_update_weight` scaling is applied at solve time in
`compute_delta_W`, matching the reference implementation. **Do not pre-scale the saved
tensors.**

Output goes to `artifacts/covariances/<model>/c_layer_<l>.pt`. The per-model directory
matters: a flat cache silently lets a second model reuse the first model's statistics.

Sample count: the reference uses mom2_n_samples = 100000 over Wikipedia. This samples
model-generated text instead, and the default of 1000 × ~20 tokens is far short of that —
raise `-n` substantially when running on a GPU. The count is recorded next to the tensor
in `meta.json`, because two caches built at different sample counts are not comparable and
nothing else on disk records which is which.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from utils.model_state import load_card, mlp_proj


def cov_dir(model_name: str) -> Path:
    return Path("artifacts") / "covariances" / model_name


def accumulate_outer(K: torch.Tensor) -> torch.Tensor:
    """K [d, T] -> K @ Kᵀ [d, d]."""
    return K @ K.T


def compute_and_save_covariances(
    model,
    tokenizer,
    card: dict,
    n_samples: int,
    layers: list[int] | None = None,
    max_new_tokens: int = 20,
    accum_device: str | None = None,
) -> None:
    """
    1. Initialise C[l] = zeros(d_mlp, d_mlp) for each edit layer.
    2. For each sample: generate ~max_new_tokens of text from EOS, hook the projection
       on every edit layer to capture its INPUT (the post-activation keys), forward, and
       accumulate K Kᵀ.
    3. Divide by the total token count -> mean second moment.
    4. Save.

    `accum_device` holds the accumulators somewhere other than the model's device. For
    LLaMA, d_mlp is 14336, so each C is 822 MB in fp32 and all five together are 4.1 GB
    on top of a 16 GB bf16 model — enough to matter on a 24 GB card. Accumulating on CPU
    trades speed for that headroom.
    """
    layers = list(layers if layers is not None else card["edit_layers"])
    device = next(model.parameters()).device
    accum = torch.device(accum_device) if accum_device else device
    d_mlp = card["model_mlp_dim"]

    C = {l: torch.zeros(d_mlp, d_mlp, device=accum, dtype=torch.float32) for l in layers}
    total_tokens = 0

    for i in range(n_samples):
        start_ids = tokenizer(tokenizer.eos_token, return_tensors="pt").input_ids.to(device)
        with torch.no_grad():
            gen_ids = model.generate(
                start_ids,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=1.0,
                pad_token_id=tokenizer.eos_token_id,
            )

        captured: dict[int, torch.Tensor] = {}

        def make_hook(layer):
            def hook(module, inp, out):
                # the projection's INPUT is the post-activation key vector.
                # .float() because the model may be bf16 and the statistics are not.
                captured[layer] = inp[0][0].detach().float()  # [seq_len, d_mlp]
            return hook

        handles = [
            mlp_proj(model, card, l).register_forward_hook(make_hook(l)) for l in layers
        ]
        with torch.no_grad():
            model(gen_ids)
        for h in handles:
            h.remove()

        for l in layers:
            C[l] += accumulate_outer(captured[l].to(accum).T)
        total_tokens += captured[layers[0]].shape[0]

        if (i + 1) % 100 == 0:
            print(f"  {i + 1}/{n_samples} samples, {total_tokens} tokens")

    out_dir = cov_dir(card["name"])
    out_dir.mkdir(parents=True, exist_ok=True)

    for l in layers:
        C[l] /= total_tokens
        path = out_dir / f"c_layer_{l}.pt"
        torch.save(C[l].cpu(), path)
        print(
            f"  saved {path}  shape={tuple(C[l].shape)}  "
            f"norm={C[l].norm():.2f}  diag_mean={C[l].diagonal().mean():.4e}"
        )

    # the sample count is the thing that makes two caches comparable or not — the local
    # GPT-2-XL cache and the pod's disagree (diag 0.0324 vs 0.0280) and neither recorded
    # how it was built, which is why this file exists.
    (out_dir / "meta.json").write_text(json.dumps({
        "model": card["name"],
        "layers": layers,
        "n_samples": n_samples,
        "max_new_tokens": max_new_tokens,
        "total_tokens": total_tokens,
        "source": "model-generated text from EOS, do_sample=True, temperature=1.0",
        "scaling": "raw mean second moment — mom2_update_weight applied at solve time",
    }, indent=2) + "\n")

    print(f"\n{total_tokens} tokens total over {n_samples} samples -> {out_dir}/meta.json")


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--model", default="gpt2-xl")
    ap.add_argument("-n", "--n-samples", type=int, default=1000)
    ap.add_argument("--max-new-tokens", type=int, default=20)
    ap.add_argument("--device", default=None,
                    help="cuda / cpu. Defaults to cuda when available, else cpu. "
                         "NOT mps — see DEV-001.")
    ap.add_argument("--accum-device", default=None,
                    help="hold the accumulators here instead of the model's device; "
                         "'cpu' frees ~4 GB of VRAM on LLaMA")
    ap.add_argument("--layers", type=int, nargs="*", default=None,
                    help="override the card's edit layers")
    args = ap.parse_args()

    if args.device == "mps" or args.accum_device == "mps":
        print("refusing mps — see DEV-001. Use cpu or cuda.", file=sys.stderr)
        return 2
    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")

    card = load_card(args.model)
    src = card.get("local_dir") or card["hf_id"]
    # bf16 on GPU for the same reason harness.py does it: fp32 puts LLaMA-3-8B at ~32 GB
    # before the covariance accumulators are allocated at all. Keys are cast to fp32 at
    # capture, so the statistics stay fp32 either way.
    dtype = torch.bfloat16 if device == "cuda" else torch.float32

    print(f"Loading {card['name']} from {src} -> {device} ({dtype})")
    tokenizer = AutoTokenizer.from_pretrained(src)
    model = AutoModelForCausalLM.from_pretrained(src, dtype=dtype).to(device).eval()

    layers = args.layers if args.layers else list(card["edit_layers"])
    print(f"layers {layers} · {args.n_samples} samples · out {cov_dir(card['name'])}")

    compute_and_save_covariances(
        model, tokenizer, card,
        n_samples=args.n_samples,
        layers=layers,
        max_new_tokens=args.max_new_tokens,
        accum_device=args.accum_device,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
