import json
from pathlib import Path

import pandas as pd

from eval.csv_to_md import (
    BENCH_LABELS,
    BENCH_ORDER,
    CATEGORY_ORDER,
    LABELS,
    MEASURE_LABELS,
    METHOD_LABELS,
    METHOD_ORDER,
    MISSING,
    PRE,
    S_PARTS,
    cell,
    harmonic,
    slice_for,
)
from eval.results_to_csv import reported

RUN = Path("results") / "reported_results"

W_BENCH, W_PROBE, W_NUM = 14, 11, 9


def table(df, model, manifest):
    methods = [m for m in METHOD_ORDER if m in set(df["method"])]
    benches = [b for b in BENCH_ORDER if b in set(df["bench"])]
    cols = [PRE] + methods

    head = " | ".join(PRE if c == PRE else METHOD_LABELS[c] for c in cols)
    rule = (
        "|:"
        + "-" * W_BENCH
        + "|:"
        + "-" * W_PROBE
        + "|"
        + ("-" * W_NUM + ":|") * len(cols)
    )
    lines = [f"| Benchmark | Probe | {head} |", rule]

    scored_by = {}  # bench -> the measure name, for the caption

    for bench in benches:
        categories = [
            c
            for c in CATEGORY_ORDER
            if not df[(df["bench"] == bench) & (df["category"] == c)].empty
        ]
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
            
            lines.append(f"| {name} | {LABELS[category]} | " + " | ".join(row) + " |")

        if all(p in categories for p in S_PARTS):
            s_row = []
            for c in cols:
                parts = [means[c][p] for p in S_PARTS]
                s_row.append(
                    MISSING
                    if any(p is None for p in parts)
                    else f"**{100 * harmonic(parts):.1f}**"
                )
            lines.append("|  | **S** | " + " | ".join(s_row) + " |")

        scored_by[bench] = ", ".join(
            MEASURE_LABELS.get(m, m) for m in sorted(measure_seen)
        )

    metrics = "; ".join(
        f"{BENCH_LABELS.get(b, b)} {scored_by[b]}" for b in benches if scored_by.get(b)
    )
    caption = (
        f": Edit quality on {model}. n={manifest['quantity']} cases per cell, seed "
        f"{manifest.get('sample_seed')}. All values are percentages, mean ±sd over "
        f"cases; **higher is better in every row**. Each benchmark is scored by its own "
        f"paper's metric — {metrics}. S is the harmonic mean of efficacy, generalisation "
        f"and specificity, where a benchmark carries all three. "
        f"{{#tbl:edit-quality-{model}}}"
    )

    return (
        "\\begingroup\\footnotesize\n\n"
        + "\n".join(lines)
        + "\n\n"
        + caption
        + "\n\n\\endgroup"
    )


def main():
    df = pd.read_csv(RUN / "cases.csv")
    manifest = json.loads((RUN / "manifest.json").read_text())

    text = (
        "\n\n".join(table(sub, model, manifest) for model, sub in df.groupby("model"))
        + "\n"
    )

    path = RUN / "full_table_pdf_ready.md"
    path.write_text(text)
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
