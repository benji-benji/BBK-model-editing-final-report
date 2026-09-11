"""Build the AlphaEdit null-space projections P from the saved covariances.

    uv run python -m scripts.compute_projections                                  # gpt2-xl, CPU
    uv run python -m scripts.compute_projections --model llama3-8b --device cuda

One SVD per edit layer. LLaMA's covariance is 14336² against GPT-2-XL's 6400², which is
~11x the work at O(n³), so --device cuda is worth it there. Run it with no model loaded:
the SVD needs several times the 822 MB input in workspace.
"""

import argparse
import json
import sys
from pathlib import Path

from edit_methods.alphaedit import compute_projections


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--model", default="gpt2-xl")
    ap.add_argument("--device", default="cpu", help="cpu / cuda. NOT mps — see DEV-001.")
    args = ap.parse_args()

    if args.device == "mps":
        print("refusing mps — see DEV-001. Use cpu or cuda.", file=sys.stderr)
        return 2

    card = json.loads(Path(f"models/{args.model}/card.json").read_text())
    config = json.loads(Path("edit_methods/edit_method_config.json").read_text())[
        "alphaedit"
    ][args.model]

    print(f"{args.model} · layers {card['edit_layers']} · "
          f"p{config['nullspace_percentile']} cut · {args.device}")
    compute_projections(config, card, device=args.device)
    return 0


if __name__ == "__main__":
    sys.exit(main())
