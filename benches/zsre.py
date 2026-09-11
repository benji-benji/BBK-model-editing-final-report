"""zsRE loader.

Author's own. The loader is written against the benchmark's published data
format; no loader code is taken from the reference implementations. The dataset itself is
third-party - see THIRD_PARTY_LICENSES.md for its source and terms.

Dataset: Levy, O., Seo, M., Choi, E. and Zettlemoyer, L. (2017) 'Zero-shot relation
extraction via reading comprehension', CoNLL. arXiv:1706.04115. The file read here is the
MEND evaluation split distributed by the MEMIT project. MIT.
"""

import json
from pathlib import Path

from benches.edit_eval_pack import Edit_Eval_Pack
from utils.bench_utils import select
from utils.paths import REPO_ROOT
from utils.remedi_training import train_window

ZSRE_PATH = REPO_ROOT / "data" / "raw" / "zsre" / "zsre.json"


def load_zsre(
    path: str | Path | None = None,
    quantity: int | None = None,
    seed: int | None = None,
    restrict=None,
) -> list[Edit_Eval_Pack]:

    path = Path(path) if path else ZSRE_PATH
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run: uv run python -m scripts.download_benchmarks zsre"
        )

    raw = json.loads(path.read_text())
    raw = select(raw, quantity, seed, exclude=train_window("zsre"), restrict=restrict)

    edit_datas = []

    for case_number, (row, r) in enumerate(raw):
        target_new = r["alt"]
        subject = r["subject"]
        src = r["src"]
        answers = r.get("answers") or []

        # "{}"-slot template so the edit is model-neutral like CounterFact's.
        template = src.replace(subject, "{}", 1) if subject in src else src

        pack = Edit_Eval_Pack(
            case_id=f"zsre_row{row}",
            case_number=case_number,
            benchmark="zsre",
            prompt=template,
            subject=subject,
            target_old=answers[0] if answers else None,
            target_new=r["alt"],
        )

        pack.collect_probes(
            probe_category=Edit_Eval_Pack.EFFICACY,
            prompt=pack.construct_prompt(),
            ground_truth=target_new,
        )

        pack.collect_probes(
            probe_category=Edit_Eval_Pack.GENERALISATION,
            prompt=r["rephrase"],
            ground_truth=target_new,
        )

        pack.collect_probes(
            probe_category=Edit_Eval_Pack.SPECIFICITY,
            prompt=r["loc"],
            ground_truth=r["loc_ans"],
        )

        edit_datas.append(pack)
    return edit_datas
