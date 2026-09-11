"""Run the whole eval pipeline over one run.

    uv run python -m eval.run_eval                      # newest run
    uv run python -m eval.run_eval --run EXP-004_m1-em6-b2_2026-09-01
"""

import argparse
import subprocess
import sys
from pathlib import Path

RESULTS = Path("results")

STEPS = ["eval.results_to_csv", "eval.csv_to_md", "eval.csv_to_heatgrid"]


def newest():
    runs = sorted(p for p in RESULTS.iterdir()
                  if p.is_dir() and p.name.startswith("EXP-"))
    if not runs:
        sys.exit(f"no EXP-* run directories in {RESULTS}/")
    return runs[-1].name


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run", default=None, help="run dir name; default: newest")
    run = ap.parse_args().run or newest()

    print(f"run: {run}")
    for step in STEPS:
        print(f"\n--- {step}")
        # subprocess, so each step keeps its own main() and stays runnable alone
        subprocess.run([sys.executable, "-m", step, run], check=True)

    print(f"\nresults/{run}/  cases.csv · table.md · heatmap_<model>.png")


if __name__ == "__main__":
    main()