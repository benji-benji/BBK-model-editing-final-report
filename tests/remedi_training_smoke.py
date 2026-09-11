"""Does the REMEDI training path survive every benchmark's packs, in both dtypes?

    uv run python tests/remedi_training_smoke.py [--model gpt2-xl] [--n 8]
    uv run python tests/remedi_training_smoke.py --model llama3-8b --dtype bf16   # on the pod

One model, one device. Runs the full training step — build_example, collate,
forward_edited_batch, loss_batch — over a sample from each of the five training splits, so
a shape or dtype fault surfaces here rather than twenty minutes into a billed pod run.

The five splits do not look alike:

    counterfact  one edit, one-word targets, target_old always present
    zsre         question prompts, multi-token targets, one record whose target is EMPTY
    mquake       1-4 edits per case; construct_prompt uses edits[0]
    ripple       `recent` packs have NO target_old — the prior term is masked off
    genie        loaded from genie.json here; the harness reads a per-model filtered file

The bf16 pass matters because the harness runs bf16 on CUDA while every local check runs
fp32: RemediLinearNN holds fp32 weights and casts across that boundary, and loss_batch
promotes to fp32 before log_softmax.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from benches.load_benchmarks import load_genie, load_benchmark
from edit_methods.remedi import RemediLinearNN
from scripts.train_encoder import (build_example, collate, forward_edited_batch,
                                   loss_batch)
from utils.harness_utils import pick_device
from utils.model_state import load_card, layer_block
from utils.remedi_training import load_training_split

LAYER = 1


def sample(bench, n):
    "n packs from `bench`'s REMEDI training split, or its raw file where that needs a pod"
    if bench == "genie":
        # the per-model filtered file is produced on the pod; the packs are the same shape
        return load_genie()[:n], "genie.json (filtered file is pod-side)"
    if bench == "ripple":
        # take from the tail, where `recent` sits — those are the packs with no target_old
        packs = load_training_split(bench)
        return packs[-n:], "training split, tail (recent)"
    return load_training_split(bench)[:n], "training split"


def one_step(model, tokenizer, block, card, packs, device):
    "build -> collate -> edited forward -> loss. Returns the loss and the three terms."
    examples = [build_example(model, tokenizer, block, p) for p in packs]
    pad_id = tokenizer.pad_token_id or tokenizer.eos_token_id or 0
    batch = collate(examples, pad_id, device)

    editor = RemediLinearNN(model, card).to(device)
    with torch.no_grad():
        orig = model(batch["input_ids"], attention_mask=batch["attention_mask"]).logits
    logits = forward_edited_batch(model, block, batch, editor(batch["h_attr"]))
    total, terms = loss_batch(logits, orig, batch)
    return total, terms, examples


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", default="gpt2-xl")
    ap.add_argument("--n", type=int, default=8, help="packs per benchmark")
    ap.add_argument("--dtype", default="both", choices=("fp32", "bf16", "both"),
                    help="bf16 is emulated on CPU and painfully slow there; run it on the "
                         "pod, where it is what the harness actually uses")
    ap.add_argument("--device", default=None, help="cuda / cpu (default: whatever is here)")
    args = ap.parse_args()

    device = args.device or pick_device()
    card = load_card(args.model)
    tokenizer = AutoTokenizer.from_pretrained(f"./models/{args.model}")
    failures = []

    wanted = {"fp32": (torch.float32,), "bf16": (torch.bfloat16,),
              "both": (torch.float32, torch.bfloat16)}[args.dtype]
    for dtype in wanted:
        model = (AutoModelForCausalLM
                 .from_pretrained(f"./models/{args.model}", dtype=dtype)
                 .to(device).eval())
        block = layer_block(model, card, LAYER)
        print(f"\n=== {args.model} · layer {LAYER} · {dtype} · {device} ===")
        print(f"{'bench':<12}{'packs':>6}{'no old':>8}{'loss':>10}{'tgt':>9}"
              f"{'prior':>9}{'kl':>9}   source")

        for bench in ("counterfact", "zsre", "mquake", "ripple", "genie"):
            try:
                packs, source = sample(bench, args.n)
                no_old = sum(1 for p in packs if not p.target_old)
                total, (t, p_, k), _ = one_step(
                    model, tokenizer, block, card, packs, device)
                assert torch.isfinite(total), "loss is not finite"
                print(f"{bench:<12}{len(packs):6d}{no_old:8d}{total.item():10.3f}"
                      f"{t.item():9.3f}{p_.item():9.3f}{k.item():9.3f}   {source}")
            except Exception as e:  # noqa: BLE001 — the point is to collect every fault
                failures.append(f"{bench} · {dtype}: {type(e).__name__}: {e}")
                print(f"{bench:<12}   FAILED  {type(e).__name__}: {e}")

        del model

    if failures:
        print(f"\n{len(failures)} FAILED")
        for f in failures:
            print(f"  {f}")
        return 1
    print(f"\nall benchmarks build and train in "
          f"{', '.join(str(d).split('.')[-1] for d in wanted)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
