"""GENIE loader.

Author's own throughout - both the loader and the benchmark it reads. GENIE is the custom
benchmark built for this project; it is generated from WikiData by `genie_bench/`, and the
per-model filtered tables it loads are produced by `scripts/genie_filter_by_model.py`.

WikiData content is published under CC0 1.0. See THIRD_PARTY_LICENSES.md.
"""

import json
from pathlib import Path

from benches.edit_eval_pack import Edit_Eval_Pack
from utils.bench_utils import select
from utils.paths import REPO_ROOT

GENIE_DIR = REPO_ROOT / "data" / "raw" / "genie"


def genie_path(model=None):
    if model:
        filtered = GENIE_DIR / f"genie_{model}.json"
        if filtered.exists():
            return filtered
    return GENIE_DIR / "genie.json"


def load_genie(path=None, quantity=None, model=None, seed=None):

    path = Path(path) if path else genie_path(model)

    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run: uv run python -m genie_bench.scripts.genie_full_generation"
        )

    raw = json.loads(path.read_text())

    raw = select(raw, quantity, seed)

    edit_datas = []

    for case_number, (row, r) in enumerate(raw):
        pack = Edit_Eval_Pack(
            case_id=r["case_id"],
            case_number=case_number,
            benchmark="genie",
            prompt=r["prompt"],  # already has a "{}" slot
            subject=r["subject"],
            target_new=r["target_new"],
            target_old=r["target_old"],
            meta=r["meta"],
        )

        for p in r["probes"]:
            # probes carry their own answers: hop and comparison answers are
            # different entities from the edit's own target_old / target_new
            pack.collect_probes(
                probe_category=(
                    Edit_Eval_Pack.EFFICACY
                    if p["category"] == "efficacy"
                    else p["category"]
                ),
                prompt=p["prompt"],
                ground_truth=p["answer_new"][0],
                meta={
                    "answer_new": p["answer_new"],
                    "answer_old": p["answer_old"],
                    "generation_only": p["category"]
                    in Edit_Eval_Pack.GENIE_GENERATION_ONLY,
                },
            )

        edit_datas.append(pack)
    return edit_datas
