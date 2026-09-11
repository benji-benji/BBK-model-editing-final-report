"""CounterFact loader.

Author's own. The loader is written against the benchmark's published data
format; no loader code is taken from the reference implementations. The dataset itself is
third-party - see THIRD_PARTY_LICENSES.md for its source and terms.

Dataset: introduced with ROME (Meng et al., 2022, arXiv:2202.05262), distributed at
memit.baulab.info. MIT.
"""

import json
from pathlib import Path

from benches.edit_eval_pack import Edit_Eval_Pack
from utils.bench_utils import select
from utils.paths import REPO_ROOT
from utils.remedi_training import train_window

COUNTERFACT_PATH = REPO_ROOT / "data" / "raw" / "counterfact" / "counterfact.json"


def load_counterfact(
    path: str | Path | None = None,
    quantity: int | None = None,
    seed: int | None = None,
    restrict=None,
) -> list[Edit_Eval_Pack]:
    path = Path(path) if path else COUNTERFACT_PATH
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run: uv run python -m scripts.download_benchmarks counterfact"
        )

    raw = json.loads(path.read_text())
    # the REMEDI encoders were fitted on a slice of this file — excluded for every
    # method, so all six are measured on the same out-of-sample cases
    raw = select(
        raw, quantity, seed, exclude=train_window("counterfact"), restrict=restrict
    )

    edit_datas = []  # initalise an empty list, to be filled with Edit_Eval_Pack objects

    for case_number, (row, r) in enumerate(
        raw
    ):  # one Edit_Eval_Pack per selected record
        rw = r["requested_rewrite"]
        target_new = rw["target_new"]["str"]
        target_old = rw["target_true"]["str"]

        pack = Edit_Eval_Pack(
            prompt=rw["prompt"],
            target_new=target_new,
            subject=rw["subject"],
            target_old=target_old,
            case_id=str(r["case_id"]),
            case_number=case_number,
            benchmark="counterfact",
            meta={"relation_id": rw.get("relation_id")},
        )

        pack.collect_probes(
            probe_category=Edit_Eval_Pack.EFFICACY,
            prompt=pack.construct_prompt(),
            ground_truth=target_new,
        )

        for p in r.get("paraphrase_prompts", []):
            pack.collect_probes(
                probe_category=Edit_Eval_Pack.GENERALISATION,
                prompt=p,
                ground_truth=target_new,
            )

        for p in r.get("neighborhood_prompts", []):
            pack.collect_probes(
                probe_category=Edit_Eval_Pack.SPECIFICITY,
                prompt=p,
                ground_truth=target_old,
            )

        for p in r.get("attribute_prompts", []):
            pack.collect_probes(
                probe_category=Edit_Eval_Pack.TARGET_CLOSE_NEIGHBOUR,
                prompt=p,
            )
        edit_datas.append(pack)
    return edit_datas
