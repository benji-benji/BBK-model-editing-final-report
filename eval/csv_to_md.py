
import json
import sys
from pathlib import Path

import pandas as pd

from eval.results_to_csv import RETENTION, reported

RESULTS = Path("results")

# probe category -> the label used in the published tables
LABELS = {
    "efficacy": "Eff.", "generalisation": "Gen.", "specificity": "Spe.",
    "ripple_aliasing": "Aliasing", "ripple_logical": "Logical",
    "ripple_compositional_i": "Comp. I", "ripple_compositional_ii": "Comp. II",
    "ripple_relation_specificity": "Rel. spec.", "ripple_preservation": "Preservation",
    "single_hop": "Single hop", "multihop": "Multi hop",
    "paraphrase_1": "Para. 1", "paraphrase_2": "Para. 2", "paraphrase_3": "Para. 3",
    "hop_1": "Hop 1", "hop_2": "Hop 2", "hop_3": "Hop 3",
    "abstract_1": "Abs. 1", "abstract_2": "Abs. 2", "abstract_3": "Abs. 3",
}
CATEGORY_ORDER = list(LABELS)

MEASURE_LABELS = {"success": "p(new) > p(old)", "acc": "exact match",
                  "hit": "containment", "diff": "mean p(new) − p(old)"}

BENCH_LABELS = {"counterfact": "CounterFact", "zsre": "zsRE",
                "ripple": "RippleEdits", "mquake": "MQuAKE", "genie": "GENIE"}
BENCH_ORDER = list(BENCH_LABELS)

METHOD_LABELS = {"rome": "ROME", "memit": "MEMIT", "alphaedit": "AlphaEdit",
                 "anyedit": "AnyEdit", "grace": "GRACE", "remedi": "REMEDI"}
METHOD_ORDER = list(METHOD_LABELS)      # ROME family first, then GRACE and REMEDI

# the three components of ROME's Editing Score S, where a benchmark carries all of them
S_PARTS = ["efficacy", "generalisation", "specificity"]

PRE = "Pre-edit"
MISSING = "---"

# inline math, not the Unicode arrow: the report's main font has no U+2191 glyph, and
# xelatex renders it as a tofu box that wraps the cell onto a second line
UP = r"$\uparrow$"


def cell(values):
    "'mean ~±sd~' for the table, and the mean as a fraction for the S row"
    if values is None or values.empty:
        return MISSING, None
    mean = 100 * values.mean()
    if len(values) < 2:
        return f"{mean:.1f}", mean / 100        # one case: no spread to report
    sd = 100 * values.std(ddof=0)               # np.std, as memit's summarize.py uses
    return f"{mean:.1f}~±{sd:.1f}~", mean / 100


def harmonic(values):
    "ROME's Editing Score S. A component at zero makes the composite zero."
    if any(v is None or v <= 0 for v in values):
        return 0.0
    return len(values) / sum(1 / v for v in values)


def slice_for(df, method, phase):
    "the rows for one column of the table"
    if method == PRE:
        # pre-edit is identical for every method, so count each case once — otherwise
        # the spread shrinks by a factor of sqrt(number of methods)
        return df[df["phase"] == "pre"].drop_duplicates(["bench", "case", "category",
                                                         "measure"])
    return df[(df["method"] == method) & (df["phase"] == "post")]


def table(df, model, manifest):
    methods = [m for m in METHOD_ORDER if m in set(df["method"])]
    benches = [b for b in BENCH_ORDER if b in set(df["bench"])]
    cols = [PRE] + methods

    head = " | ".join([PRE if c == PRE else METHOD_LABELS[c] for c in cols])
    # pandoc sets column widths from the RELATIVE number of dashes here whenever the
    # table is too wide for the page; without explicit widths every cell wraps
    rule = "|:--------------|:--------------|" + "----------:|" * len(cols)
    lines = [f"| Benchmark | Probe | {head} |", rule]

    for bench in benches:
        categories = [c for c in CATEGORY_ORDER
                      if not df[(df["bench"] == bench)
                                & (df["category"] == c)].empty]
        means = {c: {} for c in cols}
        measure_seen = set()
        first = True

        for category in categories:
            row = []
            for c in cols:
                values, measure = reported(slice_for(df, c, None), bench, category)
                if measure:
                    measure_seen.add(measure)
                text, value = cell(values)
                row.append(text)
                means[c][category] = value
            name = f"**{BENCH_LABELS.get(bench, bench)}**" if first else ""
            first = False
            lines.append(f"| {name} | {LABELS[category]} {UP} | "
                         + " | ".join(row) + " |")

        if all(p in categories for p in S_PARTS):
            s_row = []
            for c in cols:
                parts = [means[c][p] for p in S_PARTS]
                s_row.append(MISSING if any(p is None for p in parts)
                             else f"**{100 * harmonic(parts):.1f}**")
            lines.append(f"|  | **S** {UP} | " + " | ".join(s_row) + " |")

        measures = ", ".join(MEASURE_LABELS.get(m, m) for m in sorted(measure_seen))
        lines.append(f"|  | *scored by* | " + " | ".join([f"*{measures}*"] * len(cols))
                     + " |")

    caption = (
        f": Edit quality on {model}. n={manifest['quantity']} cases per cell, seed "
        f"{manifest.get('sample_seed')}. All values are percentages, mean ±sd over "
        f"cases, higher is better throughout. Each benchmark is scored by its own "
        f"paper's metric — the *scored by* row names it. S is the harmonic mean of "
        f"efficacy, generalisation and specificity, where a benchmark carries all "
        f"three. {{#tbl:edit-quality-{model}}}"
    )
    return "\n".join(lines) + "\n\n" + caption


def main():
    run_dir = RESULTS / sys.argv[1]
    df = pd.read_csv(run_dir / "cases.csv")
    manifest = json.loads((run_dir / "manifest.json").read_text())

    text = "\n\n".join(table(sub, model, manifest)
                       for model, sub in df.groupby("model")) + "\n"

    path = run_dir / "table.md"
    path.write_text(text)
    print(text)
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
