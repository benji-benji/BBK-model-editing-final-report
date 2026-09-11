"""
smoke test: every method x every benchmark, one case each.

checks in order:
  1. every benchmark loads and produces probes
  2. snapshot/restore actually works
  3. each method raises P(target) on its own edited prompt
  4. the model returns to baseline after every edit (canary)

run:  uv run -m tests.smoke_test

NOTE: on CPU this is slow — roughly 40s per cell, 24 cells. Trim METHODS or
BENCHES while you are narrowing things down.
"""

import json
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from edit_methods.edit_method import EditMethod
from eval.score import score_probe
from utils.harness_utils import pick_device, prepare_edits_for_editor
from benches.load_benchmarks import Edit_Eval_Pack, load_benchmark
from utils.model_state import load_card, max_drift, restore, snapshot

MODEL = "gpt2-xl"
BENCHES = ["counterfact", "zsre", "ripple", "mquake"]
METHODS = ["rome", "memit", "grace", "anyedit", "alphaedit", "remedi"]

PASS_THRESHOLD = 0.3   # P(target) after a successful edit
CANARY = "The capital of France is"


# ---------- 1. loaders ----------

print("=" * 72)
print("1. BENCHMARK LOADERS")
print("=" * 72)

cases = {}
for bench in BENCHES:
    try:
        packs = load_benchmark(bench, 1)
        counts = {}
        for p in packs[0].probe_list:
            counts[p["category"]] = counts.get(p["category"], 0) + 1
        cases[bench] = packs[0]
        print(f"  PASS   {bench:12} probes={counts}")
    except Exception as e:
        print(f"  FAIL   {bench:12} {type(e).__name__}: {e}")

if not cases:
    raise SystemExit("no benchmarks loaded — stopping")


# ---------- model ----------

device = pick_device()
card = load_card(MODEL)
tokenizer = AutoTokenizer.from_pretrained(f"./models/{MODEL}")
model = AutoModelForCausalLM.from_pretrained(f"./models/{MODEL}").to(device).eval()
method_config = json.loads(Path("edit_methods/edit_method_config.json").read_text())

print(f"\nmodel: {MODEL} on {device}")


def canary():
    "top token for a fixed prompt — detects a model that never got restored."
    ids = tokenizer(CANARY, return_tensors="pt").input_ids.to(model.device)
    with torch.no_grad():
        probs = model(ids).logits[0, -1].softmax(-1)
    top = int(probs.argmax())
    return tokenizer.decode(top).strip(), round(probs[top].item(), 4)


# ---------- 2. snapshot / restore ----------

print("\n" + "=" * 72)
print("2. SNAPSHOT / RESTORE")
print("=" * 72)

snap = snapshot(model, card)
weight = model.transformer.h[17].mlp.c_proj.weight

print(f"  no change        drift={max_drift(model, card, snap):.2e}   (expect 0.0)")

with torch.no_grad():
    weight += 1.0
dirty = max_drift(model, card, snap)
print(f"  after +1.0       drift={dirty:.2e}   (expect ~1.0)")

if dirty < 0.5:
    with torch.no_grad():
        weight -= 1.0   # restore() can't help — undo by hand
    print("  FAIL   snapshot moved with the weights, so it is not a real copy.")
    print("         every 'restore drift 0.0' you have seen is meaningless.")
else:
    restore(model, card, snap)
    print(f"  after restore    drift={max_drift(model, card, snap):.2e}   (expect 0.0)")
    print("  PASS   snapshot holds an independent copy")

baseline = canary()
print(f"\n  canary baseline: {CANARY!r} -> {baseline}")


# ---------- 3 & 4. method x benchmark matrix ----------

print("\n" + "=" * 72)
print("3. METHOD x BENCHMARK")
print("=" * 72)

results = []

for method_name in METHODS:
    for bench, case in cases.items():
        label = f"{method_name}/{bench}"
        snap = snapshot(model, card)
        pre_p = post_p = None
        note = ""

        try:
            method = EditMethod(
                name=method_name,
                model=model,
                card=card,
                config=method_config[method_name][MODEL],
                covariances_path=f"./artifacts/covariances/{MODEL}",
            )

            probe = next(
                p for p in case.probe_list
                if p["category"] == Edit_Eval_Pack.EFFICACY
            )

            pre_p = score_probe(model, tokenizer, probe, case, "pre_edit").p_new

            method.run_edits(
                name=method_name,
                model=model,
                tokenizer=tokenizer,
                edit_datas=prepare_edits_for_editor(case),
            )

            post_p = score_probe(model, tokenizer, probe, case, "post_edit").p_new
            verdict = "PASS" if post_p >= PASS_THRESHOLD else "FAIL"

        except Exception as e:
            verdict = "ERROR"
            note = f"{type(e).__name__}: {e}"[:60]

        # always tear down and restore, even after an error
        try:
            method.teardown()
        except Exception:
            pass
        restore(model, card, snap)

        now = canary()
        if now != baseline:
            note = (note + " | CANARY MOVED - model not restored").strip(" |")

        results.append((label, verdict, pre_p, post_p, note))
        print(f"  {verdict:5}  {label:22} "
              f"pre={pre_p if pre_p is None else round(pre_p, 4)} "
              f"post={post_p if post_p is None else round(post_p, 4)}  {note}")


# ---------- summary ----------

print("\n" + "=" * 72)
print("SUMMARY")
print("=" * 72)
print(f"  {'cell':24} {'verdict':8} {'P(new) pre':>11} {'P(new) post':>12}")
for label, verdict, pre_p, post_p, note in results:
    pre_s = "-" if pre_p is None else f"{pre_p:.4f}"
    post_s = "-" if post_p is None else f"{post_p:.4f}"
    print(f"  {label:24} {verdict:8} {pre_s:>11} {post_s:>12}  {note}")

passed = sum(1 for r in results if r[1] == "PASS")
print(f"\n  {passed}/{len(results)} cells passed (threshold P(new) >= {PASS_THRESHOLD})")