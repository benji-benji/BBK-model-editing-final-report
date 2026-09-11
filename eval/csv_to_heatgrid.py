import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import TwoSlopeNorm

from eval.csv_to_md import (
    BENCH_LABELS,
    BENCH_ORDER,
    CATEGORY_ORDER,
    LABELS,
    METHOD_LABELS,
    METHOD_ORDER,
    PRE,
    S_PARTS,
    harmonic,
    slice_for,
)
from eval.results_to_csv import reported

RESULTS = Path("results")


def grid(df, with_diff=False):

    methods = [m for m in METHOD_ORDER if m in set(df["method"])]
    benches = [b for b in BENCH_ORDER if b in set(df["bench"])]
    cols = [PRE] + methods
    out, order = {}, []

    for bench in benches:
        categories = [
            c
            for c in CATEGORY_ORDER
            if not df[(df["bench"] == bench) & (df["category"] == c)].empty
        ]
        for category in categories:
            wanted = [None] + (["diff"] if with_diff else [])
            for measure in wanted:
                key = (bench, category, measure or "rate")
                cell = {}
                for c in cols:
                    values, name = reported(
                        slice_for(df, c, None), bench, category, measure
                    )
                    if values is not None and not values.empty:
                        cell[c] = values.mean()
                        key = (bench, category, name)
                if cell:
                    order.append(key)
                    out[key] = cell

        if all(p in categories for p in S_PARTS):
            key = (bench, "S", "S")
            order.append(key)
            for c in cols:
                parts = [
                    out.get(k, {}).get(c)
                    for p in S_PARTS
                    for k in out
                    if k[0] == bench and k[1] == p and k[2] != "diff"
                ]
                if parts and all(p is not None for p in parts):
                    out.setdefault(key, {})[c] = harmonic(parts)

    return out, order, cols


RATES = plt.get_cmap("Blues")  # [0,1], fixed, never data-dependent
DIFFS = plt.get_cmap("RdBu")  # signed, centred on 0
DIFF_NORM = TwoSlopeNorm(vmin=-1.0, vcenter=0.0, vmax=1.0)


def heatmap(cell, rows, cols, title, path):
    fig, ax = plt.subplots(figsize=(1.35 * len(cols) + 5.5, 0.55 * len(rows) + 2))

    for r, key in enumerate(rows):
        measure = key[2]
        for c, method in enumerate(cols):
            v = cell.get(key, {}).get(method)
            if v is None:
                ax.add_patch(
                    plt.Rectangle(
                        (c, r), 1, 1, facecolor="#e8e8e8", edgecolor="white", lw=1.5
                    )
                )
                ax.text(c + 0.5, r + 0.5, "—", ha="center", va="center", color="#888")
                continue
            # diff is signed and needs a diverging scale; every other measure is a
            # rate in [0,1] and shares one fixed sequential scale
            rgba = DIFFS(DIFF_NORM(v)) if measure == "diff" else RATES(v)
            ax.add_patch(
                plt.Rectangle((c, r), 1, 1, facecolor=rgba, edgecolor="white", lw=1.5)
            )
            lum = 0.299 * rgba[0] + 0.587 * rgba[1] + 0.114 * rgba[2]
            ax.text(
                c + 0.5,
                r + 0.5,
                f"{v:+.2f}" if measure == "diff" else f"{v:.2f}",
                ha="center",
                va="center",
                fontsize=9,
                color="white" if lum < 0.5 else "#111",
            )

    last = None
    for r, (bench, category, measure) in enumerate(rows):
        label = "S" if category == "S" else LABELS.get(category, category)
        if measure == "diff":
            label += "  diff"
        ax.text(
            -0.15,
            r + 0.5,
            label,
            ha="right",
            va="center",
            fontsize=9,
            weight="bold" if category == "S" else "normal",
            color="#666" if measure == "diff" else "#111",
        )
        if bench != last:
            if last is not None:
                ax.axhline(r, color="#333", lw=1.2)
            ax.text(
                -5.4,
                r + 0.5,
                BENCH_LABELS.get(bench, bench),
                ha="left",
                va="center",
                fontsize=10,
                weight="bold",
            )
            last = bench

    for c, method in enumerate(cols):
        ax.text(
            c + 0.5,
            -0.2,
            PRE if method == PRE else METHOD_LABELS[method],
            ha="center",
            va="bottom",
            fontsize=10,
            weight="bold",
        )

    ax.set_xlim(-5.5, len(cols))
    ax.set_ylim(len(rows), -0.9)
    ax.axis("off")
    ax.set_title(title, fontsize=11, pad=14)
    fig.text(
        0.01,
        0.005,
        "Each benchmark scored by its own paper's metric, as a rate in [0,1], "
        "oriented so higher is better. S is the harmonic mean of efficacy, "
        "generalisation and specificity. `diff` rows are mean(p_new - p_old) on a "
        "diverging scale: red means the edit moved the OLD answer up.",
        fontsize=7.5,
        color="#555",
    )
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main():
    run_dir = RESULTS / sys.argv[1]
    df = pd.read_csv(run_dir / "cases.csv")

    for model, sub in df.groupby("model"):
        for with_diff in (False, True):
            cell, rows, cols = grid(sub, with_diff=with_diff)
            suffix = "-with-diff" if with_diff else ""
            path = run_dir / f"heatmap_{model}{suffix}.png"
            heatmap(
                cell,
                rows,
                cols,
                f"{model} — edit quality (darker is better)"
                + (", with magnitude" if with_diff else ""),
                path,
            )
            print(f"wrote {path}")


if __name__ == "__main__":
    main()
