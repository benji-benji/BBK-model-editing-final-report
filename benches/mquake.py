"""MQuAKE loader.

Author's own. The loader is written against the benchmark's published data
format; no loader code is taken from the reference implementations. The dataset itself is
third-party - see THIRD_PARTY_LICENSES.md for its source and terms.

Dataset: Zhong, Z., Wu, Z., Manning, C.D., Potts, C. and Chen, D. (2023) 'MQuAKE:
assessing knowledge editing in language models via multi-hop questions', EMNLP.
arXiv:2305.14795. Source: https://github.com/princeton-nlp/MQuAKE. MIT.
"""

import json
from pathlib import Path

from benches.edit_eval_pack import Edit_Eval_Pack
from utils.bench_utils import select
from utils.paths import REPO_ROOT

MQUAKE_PATH = REPO_ROOT / "data" / "raw" / "mquake" / "mquake.json"


def load_mquake(
    path: str | Path | None = None,
    quantity: int | None = None,
    seed: int | None = None,
    restrict=None,
) -> list[Edit_Eval_Pack]:

    path = Path(path) if path else MQUAKE_PATH

    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run: uv run python -m scripts.download_benchmarks mquake"
        )

    raw = json.loads(path.read_text())

    raw = select(raw, quantity, seed, restrict=restrict)

    edit_datas = []

    for case_number, (row, r) in enumerate(raw):
        edits = r["requested_rewrite"]

        pack = Edit_Eval_Pack(
            case_id=str(r["case_id"]),
            case_number=case_number,
            benchmark="mquake",
            prompt=edits[0]["prompt"],  # already has a "{}" slot
            subject=edits[0]["subject"],
            target_new=edits[0]["target_new"]["str"],
            target_old=edits[0]["target_true"]["str"],
            meta={
                "edits": [
                    {
                        "prompt": e["prompt"],
                        "subject": e["subject"],
                        "target_new": e["target_new"]["str"],
                        "target_old": e["target_true"]["str"],
                    }
                    for e in edits
                ],
                "n_hops": len(r["new_single_hops"]),
                "edit_positions": r["orig"][
                    "edit_triples_idx"
                ],  # which hops were edited
            },
        )

        for e in edits:
            pack.collect_probes(
                probe_category=Edit_Eval_Pack.EFFICACY,
                prompt=e["prompt"].format(e["subject"]),
                ground_truth=e["target_new"]["str"],
                meta={
                    "accept": [e["target_new"]["str"]],
                    "answer_old": [e["target_true"]["str"]],
                },
            )

        old_hops = r.get("single_hops") or []
        for i, hop in enumerate(r["new_single_hops"]):
            # A pre-edit answer exists only where the question is the same question. Hops
            # downstream of an edit ask about a different entity — "the head of state in
            # Portugal" becomes "the head of state in United Kingdom" — and had no answer
            # before the edit. 67 of 140 probes in the n=50 sample carry one; for the other
            # 73 answer_old is an EMPTY LIST, which means "none exists" and is distinct from
            # the key being absent (that still falls back to case.target_old).
            old = old_hops[i] if i < len(old_hops) else None
            same_question = old is not None and old["cloze"] == hop["cloze"]

            pack.collect_probes(
                probe_category=Edit_Eval_Pack.SINGLE_HOP,
                prompt=hop["cloze"],
                ground_truth=hop["answer"],
                meta={
                    "accept": [hop["answer"]] + hop["answer_alias"],
                    "answer_old": (
                        [old["answer"]] + old["answer_alias"] if same_question else []
                    ),
                },
            )

        for q in r["questions"]:
            pack.collect_probes(
                probe_category=Edit_Eval_Pack.MULTIHOP,
                prompt=q,
                ground_truth=r["new_answer"],
                meta={
                    "accept": [r["new_answer"]] + r["new_answer_alias"],
                    "target_old": r["answer"],
                },
            )
        edit_datas.append(pack)

    return edit_datas
