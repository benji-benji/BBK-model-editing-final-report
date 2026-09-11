"""Sweep clamp_norm_factor for one method on one model, in a single process.

    uv run python -m scripts.sweep_clamp --model llama3-8b --method rome
    uv run python -m scripts.sweep_clamp --model llama3-8b --method anyedit -n 5
    uv run python -m scripts.sweep_clamp --model llama3-8b --method rome --clamps 4,1,0.5

The model is loaded ONCE and the weights are snapshotted and restored around every edit,
so N clamp values cost one load instead of N. Only the efficacy probe is scored — this is
a hyperparameter search, not an evaluation, and nothing it writes goes near results/.

Reads `clamp_norm_factor` out of edit_method_config.json and overrides it per sweep step,
so it exercises exactly the code path the harness does.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from benches.load_benchmarks import load_benchmark
from edit_methods.edit_method import EditMethod
from eval.score import score_probe
from utils.harness_utils import pick_device, prepare_edits_for_editor
from utils.model_state import load_card, max_drift, restore, snapshot

DEFAULT_CLAMPS = [4.0, 2.0, 1.0, 0.75, 0.5, 0.25, 0.1]


def efficacy(model, tokenizer, case, score_mode):
    "the one efficacy probe for this case"
    probe = next(p for p in case.probe_list if p["category"] == "efficacy")
    return score_probe(model, tokenizer, probe, case, score_mode)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="llama3-8b")
    ap.add_argument("--method", default="rome")
    ap.add_argument("--benchmark", default="counterfact")
    ap.add_argument("-n", type=int, default=3, help="cases per clamp value")
    ap.add_argument("--clamps", default=None,
                    help="comma-separated, e.g. 4,2,1,0.5 (default: a spread)")
    args = ap.parse_args()

    clamps = ([float(c) for c in args.clamps.split(",")] if args.clamps
              else DEFAULT_CLAMPS)

    device = pick_device()
    dtype = torch.bfloat16 if device == "cuda" else torch.float32
    card = load_card(args.model)

    print(f"{args.method} · {args.model} · {args.benchmark} · n={args.n} · "
          f"{device} ({dtype})")
    print(f"clamps: {clamps}\n", flush=True)

    tokenizer = AutoTokenizer.from_pretrained(f"./models/{args.model}")
    model = (AutoModelForCausalLM.from_pretrained(f"./models/{args.model}", dtype=dtype)
             .to(device).eval())

    method_config = json.loads(
        Path("edit_methods/edit_method_config.json").read_text())
    cases = load_benchmark(args.benchmark, args.n, model=args.model, seed=None)

    # pre-edit once: it does not depend on the clamp
    pre = {}
    for case in cases:
        card_pre = efficacy(model, tokenizer, case, "pre_edit")
        pre[case.case_id] = card_pre
    base = statistics.mean(c.difference for c in pre.values())
    print(f"pre-edit  mean diff {base:+.4f}   "
          + "  ".join(f"[{k}] p_new={c.p_new:.4f} p_old={c.p_old:.4f}"
                      for k, c in pre.items()), flush=True)
    print()

    rows = []
    for clamp in clamps:
        method = EditMethod(
            name=args.method,
            model=model,
            card=card,
            config=dict(method_config[args.method][args.model]),
            covariances_path=f"./artifacts/covariances/{args.model}",
        )
        method.config["clamp_norm_factor"] = clamp

        diffs, news, olds, detail, drift = [], [], [], [], 0.0
        for case in cases:
            snap = snapshot(model, card)
            try:
                method.run_edits(name=method.name, model=model, tokenizer=tokenizer,
                                 edit_datas=prepare_edits_for_editor(case))
                post = efficacy(model, tokenizer, case, "post_edit")
                diffs.append(post.difference)
                news.append(post.p_new)
                olds.append(post.p_old)
                detail.append(f"[{case.case_id}] {post.p_new:.4f}/{post.p_old:.4f}")
            except Exception as e:  # noqa: BLE001 — one bad clamp must not end the sweep
                diffs.append(float("nan"))
                detail.append(f"[{case.case_id}] FAILED {type(e).__name__}")
            finally:
                method.teardown()
                restore(model, card, snap)
                drift = max(drift, max_drift(model, card, snap))

        live = [d for d in diffs if d == d]
        mean = statistics.mean(live) if live else float("nan")
        # DEGENERATE = the edit destroyed the distribution rather than redirecting it:
        # both answers below 1e-4. That reads as a diff near ZERO, which looks like a big
        # improvement over a negative baseline and is nothing of the kind — so it must be
        # flagged, not ranked.
        dead = sum(1 for n, o in zip(news, olds) if n < 1e-4 and o < 1e-4)
        mean_new = statistics.mean(news) if news else float("nan")
        rows.append((clamp, mean, mean_new, dead, len(news)))
        flag = f"  DEGENERATE {dead}/{len(news)}" if dead else ""
        print(f"clamp {clamp:<6}  mean diff {mean:+.4f}  mean p_new {mean_new:.4f}   "
              + "  ".join(detail) + f"   drift {drift:.1e}{flag}", flush=True)

    out = Path("artifacts/sweeps")
    out.mkdir(parents=True, exist_ok=True)
    dest = out / f"clamp_{args.method}_{args.model}_{args.benchmark}_n{args.n}.json"
    dest.write_text(json.dumps({
        "method": args.method, "model": args.model, "benchmark": args.benchmark,
        "n": args.n, "config": method_config[args.method][args.model],
        "pre_edit_mean_diff": base,
        "pre_edit": {k: {"p_new": c.p_new, "p_old": c.p_old} for k, c in pre.items()},
        "rows": [{"clamp": c, "mean_diff": m, "mean_p_new": mn,
                  "degenerate": d, "n_cases": n} for c, m, mn, d, n in rows],
    }, indent=2) + "\n")
    print(f"\nwrote {dest}")

    print(f"\n{'clamp':>8}  {'mean diff':>10}  {'mean p_new':>11}  status")
    for clamp, mean, mean_new, dead, n in rows:
        status = (f"DEGENERATE {dead}/{n}" if dead
                  else ("edits" if mean > base + 0.05 else "no change"))
        bar = "" if mean != mean or dead else "#" * max(0, int((mean - base) * 20))
        print(f"{clamp:>8}  {mean:>+10.4f}  {mean_new:>11.4f}  {status} {bar}")

    # rank only on rows that are NOT degenerate — a destroyed layer is not a candidate
    good = [r for r in rows if r[1] == r[1] and not r[3]]
    if good:
        best = max(good, key=lambda r: r[1])
        print(f"\nbest non-degenerate: clamp {best[0]} at {best[1]:+.4f} "
              f"(pre-edit {base:+.4f})")
    else:
        print(f"\nNO non-degenerate clamp value — every setting destroyed the "
              f"distribution. The clamp is not the cause.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
