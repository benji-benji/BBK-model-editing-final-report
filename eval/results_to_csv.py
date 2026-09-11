"""Harness artifacts -> cases.csv, in long format.

    uv run python -m eval.results_to_csv EXP-010_m2-em2-b2_2026-09-02

One row per model x method x benchmark x case x category x measure x phase:

    model,method,bench,case,category,measure,phase,value

Long rather than wide because the five benchmarks no longer share a metric — each is
scored the way its own paper scores it, so a wide grid would be mostly empty columns.
A measure simply has no row where it does not apply.

    success  share of probes where p_new > p_old        CounterFact, Genie cloze rungs
    diff     mean of (p_new - p_old), same probes       CounterFact
    acc      argmax exact match of the answer that      zsRE, MQuAKE single hops
             should win
    hit      generation + containment, 20 tokens        RippleEdits, MQuAKE multihop,
                                                        Genie abstract_2 / abstract_3
"""

import csv
import json
import sys
from pathlib import Path

RESULTS = Path("results")

COLUMNS = ["model", "method", "bench", "case", "category", "measure", "phase", "value"]

# probes where the answer that SHOULD win is the preserved one, not the edit's target
RETENTION = {"specificity"}


def cells(run_dir):
    "yield (model, method, bench, pre, post) for every finished cell"
    for pre_path in sorted(run_dir.glob("*/*/*/pre_edit.json")):
        post_path = pre_path.parent / "post_edit.json"
        if not post_path.exists():
            continue                       # cell still running, or it failed
        model, method, bench = pre_path.parent.parts[-3:]
        yield (model, method, bench,
               json.loads(pre_path.read_text()),
               json.loads(post_path.read_text()))


def measures(probes):
    """{category: {measure: value}} for one case.

    Averages within the case, over that category's probes. Averaging across cases
    happens downstream, which is the order memit/experiments/summarize.py uses.
    """
    by_category = {}
    for p in probes:
        by_category.setdefault(p["category"], []).append(p)

    out = {}
    for category, ps in by_category.items():
        m = {}

        scored = [p for p in ps if p.get("p_new") is not None]
        # success and diff need BOTH sides. MQuAKE's single hops downstream of an edit have
        # no pre-edit answer, so they contribute to acc but not to the comparison, and the
        # two measures carry different denominators for that category.
        paired = [p for p in scored if p.get("p_old") is not None]
        if paired:
            m["success"] = sum(p["p_new"] > p["p_old"] for p in paired) / len(paired)
            m["diff"] = sum(p["p_new"] - p["p_old"] for p in paired) / len(paired)
        if scored:
            # accuracy is not symmetric — on a locality probe the answer that should
            # win is the preserved one, so pick the field rather than inverting
            key = "correct_old" if category in RETENTION else "correct_new"
            flags = [p[key] for p in scored if p.get(key) is not None]
            if flags:
                m["acc"] = sum(flags) / len(flags)

        generated = [p for p in ps if p.get("hit") is not None]
        if generated:
            m["hit"] = sum(p["hit"] for p in generated) / len(generated)

        out[category] = m
    return out


def build_rows(run_dir):
    rows = []
    for model, method, bench, pre, post in cells(run_dir):
        for case_id, post_probes in post.items():
            for phase, probes in (("pre", pre.get(case_id, [])),
                                  ("post", post_probes)):
                for category, ms in measures(probes).items():
                    for measure, value in ms.items():
                        rows.append({
                            "model": model, "method": method, "bench": bench,
                            "case": case_id, "category": category,
                            "measure": measure, "phase": phase, "value": value,
                        })
    return rows


def main():
    run_dir = RESULTS / sys.argv[1]
    rows = build_rows(run_dir)

    out = run_dir / "cases.csv"
    with out.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"{len(rows)} rows -> {out}")


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------- reading it back

# Which measure each benchmark reports, in preference order — the first one present for
# a category wins. MQuAKE and Genie mix: MQuAKE scores multihop by containment and its
# hops by exact match, Genie scores the free-text rungs by containment and the rest by
# probability.
PREFERRED = {
    "counterfact": ["success"],
    "zsre":        ["acc"],
    "ripple":      ["hit"],
    "mquake":      ["hit", "acc"],
    "genie":       ["hit", "success"],
}


def reported(df, bench, category, measure=None):
    """The rows of `df` carrying this benchmark's headline measure for one category.

    Returns (values, measure_name), or (None, None) where the category produced
    nothing. Orientation is applied here: a rising `success` on a locality probe is a
    leak, so it is inverted. `acc` and `hit` arrive already oriented, because the
    scorer picks the answer that should win rather than a number to flip.
    """
    sub = df[(df["bench"] == bench) & (df["category"] == category)]
    for name in ([measure] if measure else PREFERRED.get(bench, ["success"])):
        vals = sub[sub["measure"] == name]["value"]
        if not vals.empty:
            if name == "success" and category in RETENTION:
                vals = 1 - vals
            return vals, name
    return None, None
