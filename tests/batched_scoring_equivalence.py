"""Does batched generation score the same as one prompt at a time?

    uv run python tests/batched_scoring_equivalence.py [--model gpt2-xl] [--cases 3]

RippleEdits is 72% of a run's forward passes and every probe there is a 20-token greedy
generation, so score_probes batches them. Batching is only safe if it changes nothing: the
padding is LEFT (right padding would generate from pad tokens) and passed per call, because
ROME and MEMIT share this tokenizer and both need RIGHT padding.

Compares, probe by probe:
    score_probes(...)                      batched
    [score_probe(p) for p in probes]       one at a time

`hit` must match exactly — it is the reported metric. `generated` is reported too, and any
divergence there is worth seeing even if the hit is unaffected.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from benches.load_benchmarks import load_benchmark
from eval.score import score_probe, score_probes
from utils.harness_utils import pick_device


def compare(model, tokenizer, cases, label):
    probes = hit_mismatch = text_mismatch = 0
    examples = []

    for case in cases:
        batched = score_probes(model, tokenizer, case.probe_list, case, "pre_edit")
        singles = [score_probe(model, tokenizer, p, case, "pre_edit")
                   for p in case.probe_list]

        for b, s, probe in zip(batched, singles, case.probe_list):
            probes += 1
            if b.hit != s.hit:
                hit_mismatch += 1
                if len(examples) < 3:
                    examples.append((probe["prompt"], s.hit, b.hit, s.generated,
                                     b.generated))
            elif b.generated != s.generated:
                text_mismatch += 1
                if len(examples) < 3:
                    examples.append((probe["prompt"], s.hit, b.hit, s.generated,
                                     b.generated))
            # probability probes go down the same path in both, so they must be identical
            if b.p_new != s.p_new or b.p_old != s.p_old:
                hit_mismatch += 1

    print(f"{label:<14}{probes:5d} probes | hit mismatches {hit_mismatch:3d} | "
          f"text-only differences {text_mismatch:3d}")
    for prompt, s_hit, b_hit, s_text, b_text in examples:
        print(f"    {prompt[:58]!r}")
        print(f"      single : hit={s_hit} {s_text[:56]!r}")
        print(f"      batched: hit={b_hit} {b_text[:56]!r}")
    return hit_mismatch


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", default="gpt2-xl")
    ap.add_argument("--cases", type=int, default=3)
    ap.add_argument("--device", default=None)
    args = ap.parse_args()

    device = args.device or pick_device()
    dtype = torch.bfloat16 if device == "cuda" else torch.float32
    tokenizer = AutoTokenizer.from_pretrained(f"./models/{args.model}")
    model = (AutoModelForCausalLM
             .from_pretrained(f"./models/{args.model}", dtype=dtype)
             .to(device).eval())

    print(f"\n{args.model} · {device} · {dtype}\n")
    bad = 0
    for bench in ("ripple", "mquake", "counterfact"):
        cases = load_benchmark(bench, args.cases, seed=0)[:args.cases]
        bad += compare(model, tokenizer, cases, bench)

    print()
    if bad:
        print(f"{bad} MISMATCHES — batching is not equivalent")
        return 1
    print("batched and single-prompt scoring agree on every probe")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
