"""
memit vs alphaedit on one case.

they share compute_z_batch, compute_keys and residual_distribute, so K and R are
identical going in. anything that differs is in the final delta-W step.

run:  uv run -m tests.memit_vs_alphaedit
"""

import json
from pathlib import Path

from transformers import AutoModelForCausalLM, AutoTokenizer

from edit_methods.edit_method import EditMethod
from eval.score import score_probe
from utils.harness_utils import pick_device, prepare_edits_for_editor
from benches.load_benchmarks import Edit_Eval_Pack, load_benchmark
from utils.model_state import load_card, restore, snapshot

MODEL = "gpt2-xl"
BENCH = "counterfact"
LAYERS = [13, 14, 15, 16, 17]


def layer_weights(model):
    "clone of each edit layer's c_proj weight"
    return {l: model.transformer.h[l].mlp.c_proj.weight.detach().clone() for l in LAYERS}


def layer_deltas(model, before):
    "how much each layer ACTUALLY moved - independent of what the method printed"
    return {
        l: (model.transformer.h[l].mlp.c_proj.weight - before[l]).norm().item()
        for l in LAYERS
    }


device = pick_device()
card = load_card(MODEL)
tokenizer = AutoTokenizer.from_pretrained(f"./models/{MODEL}")
model = AutoModelForCausalLM.from_pretrained(f"./models/{MODEL}").to(device).eval()
method_config = json.loads(Path("edit_methods/edit_method_config.json").read_text())

case = load_benchmark(BENCH, 1)[0]
probe = next(p for p in case.probe_list if p["category"] == Edit_Eval_Pack.EFFICACY)

print(f"case: {case.construct_prompt()!r} -> {case.target_new!r}\n")

results = {}

for method_name in ["memit", "alphaedit"]:
    print("=" * 72)
    print(method_name.upper())
    print("=" * 72)

    snap = snapshot(model, card)
    before = layer_weights(model)

    pre = score_probe(model, tokenizer, probe, case, "pre_edit").p_new

    method = EditMethod(
        name=method_name,
        model=model,
        card=card,
        config=method_config[method_name][MODEL],
        covariances_path=f"./artifacts/covariances/{MODEL}",
    )
    method.run_edits(
        name=method_name,
        model=model,
        tokenizer=tokenizer,
        edit_datas=prepare_edits_for_editor(case),
    )

    post = score_probe(model, tokenizer, probe, case, "post_edit").p_new
    results[method_name] = (pre, post, layer_deltas(model, before))

    method.teardown()
    restore(model, card, snap)
    print()


print("=" * 72)
print("COMPARISON - actual weight change per layer")
print("=" * 72)
print(f"  {'layer':6} {'memit':>14} {'alphaedit':>14} {'ratio':>10}")

m_deltas, a_deltas = results["memit"][2], results["alphaedit"][2]
for l in LAYERS:
    m, a = m_deltas[l], a_deltas[l]
    ratio = f"{m / a:.0f}x" if a > 0 else "-"
    print(f"  {l:<6} {m:14.4f} {a:14.4f} {ratio:>10}")

print()
for name in ["memit", "alphaedit"]:
    pre, post, _ = results[name]
    print(f"  {name:10} P(target)  {pre:.4f} -> {post:.4f}")