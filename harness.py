from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path
from pprint import pprint

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from benches.load_benchmarks import load_benchmark
from edit_methods.edit_method import EditMethod
from eval.score import score_probes
from utils.harness_utils import (
    CONFIG,
    apply_condition_gate,
    new_run_dir,
    pick_device,
    pre_edit_scores,
    prepare_edits_for_editor,
    save_artifacts,
    selected,
)
from utils.model_state import load_card, max_drift, restore, snapshot

# device selection
device = pick_device()
name = torch.cuda.get_device_name(0) if device == "cuda" else "CPU"

print(f"device: {device} ({name})")

# get eval config
models = selected("models")
methods = selected("methods")
benches = selected("benchmarks")
quantity_edits = CONFIG.get("quantity")
sample_seed = CONFIG.get("seed", 0)

print(f"models selected  : {models}")
print(f"methods selected : {methods}")
print(f"benches selected : {benches}")
print(
    f"sample seed      : {sample_seed}"
    f"{'  (UNSEEDED — first n in file order)' if sample_seed is None else ''}"
)

total_runs = len(models) * len(methods) * len(benches)

RUN_DIR = new_run_dir(models, methods, benches, quantity_edits, device, sample_seed)
failures = []

print(
    f"\n{total_runs} runs · n={quantity_edits} · saving to {RUN_DIR}/<model>/<method>/<bench>/"
)
print("-" * 70)


def run_bench(method, editdatas, model, card, tokenizer, model_name):

    print(method.name, f"running {len(editdatas)} x benchmark")

    restore_drift = 0.0

    for n, case in enumerate(editdatas):
        snap = snapshot(model, card)

        try:
            
            pre_edit = pre_edit_scores(
                model, tokenizer, case, model_name, verify=(n == 0)
            )

            pprint(pre_edit)

            save_artifacts(RUN_DIR, model_name, method, case, pre_edit, quantity_edits)

            method.run_edits(
                name=method.name,
                model=model,
                tokenizer=tokenizer,
                edit_datas=prepare_edits_for_editor(case),
            )

            post_edit = score_probes(
                model, tokenizer, case.probe_list, case, "post_edit"
            )

            pprint(post_edit)
            # save post-edit artifacts to json
            save_artifacts(RUN_DIR, model_name, method, case, post_edit, quantity_edits)

        finally:
            method.teardown()  # modules — GRACE, REMEDI

            restore(model, card, snap)  # weights — ROME, MEMIT, AlphaEdit
            restore_drift = max(restore_drift, max_drift(model, card, snap))

        print(f"max restore drift: {restore_drift:.2e} (0.0 means restore is exact)")

    return restore_drift


for model_name in models:
    card = load_card(model_name)
    tokenizer = AutoTokenizer.from_pretrained(f"./models/{model_name}")
    dtype = torch.bfloat16 if device == "cuda" else torch.float32

    model = (
        AutoModelForCausalLM.from_pretrained(f"./models/{model_name}", dtype=dtype)
        .to(device)
        .eval()
    )

    method_config = json.loads(Path("edit_methods/edit_method_config.json").read_text())

    for method_name in methods:
        method = EditMethod(
            name=method_name,
            model=model,
            card=card,
            config=method_config[method_name][model_name],
            covariances_path=f"./artifacts/covariances/{model_name}",
        )
        for bench_name in benches:
            cell = f"{model_name} · {method_name} · {bench_name}"

            try:
                edit_datas = load_benchmark(
                    bench_name, quantity_edits, model=model_name, seed=sample_seed
                )
                edit_datas = apply_condition_gate(
                    model, tokenizer, model_name, bench_name, edit_datas
                )
                drift = run_bench(
                    method, edit_datas, model, card, tokenizer, model_name
                )
                print(f"{cell} — restore drift {drift:.2e}")

            except Exception as e:
                traceback.print_exc()
                print(f"\n!! FAILED {cell}: {type(e).__name__}: {e}\n", flush=True)
                failures.append(
                    {
                        "cell": cell,
                        "model": model_name,
                        "method": method_name,
                        "benchmark": bench_name,
                        "error": f"{type(e).__name__}: {e}",
                    }
                )
                try:
                    method.teardown()
                except Exception:
                    pass

    del model, tokenizer
    if device == "cuda":
        torch.cuda.empty_cache()

print("=" * 70)
print(f"{total_runs - len(failures)}/{total_runs} cells completed")

if failures:
    (RUN_DIR / "failures.json").write_text(json.dumps(failures, indent=2) + "\n")
    print(f"{len(failures)} FAILED — recorded in {RUN_DIR}/failures.json:")
    for f in failures:
        print(f"  {f['cell']}: {f['error']}")

print(f"\nresults: {RUN_DIR}")

sys.exit(1 if failures else 0)
