"""RippleEdits loader.

Author's own. The loader is written against the benchmark's published data
format; no loader code is taken from the reference implementations. The dataset itself is
third-party - see THIRD_PARTY_LICENSES.md for its source and terms.

Dataset: Cohen, R., Biran, E., Yoran, O., Globerson, A. and Geva, M. (2024) 'Evaluating
the ripple effects of knowledge editing in language models', TACL. arXiv:2307.12976.
Source: https://github.com/edenbiran/RippleEdits. MIT.

Note: the `recent` split is excluded from evaluation because its facts have no previous
value, and is used only to train the REMEDI encoder.
"""

import json
from pathlib import Path

from benches.edit_eval_pack import Edit_Eval_Pack
from utils.bench_utils import select
from utils.paths import REPO_ROOT
from utils.remedi_training import train_window

RIPPLE_PATH = REPO_ROOT / "data" / "raw" / "ripple"
RIPPLE_QID_PATH = REPO_ROOT / "data" / "raw" / "ripple" / "ripple_qid_labels.json"

RIPPLE_CRITERIA = {
    "Logical_Generalization": Edit_Eval_Pack.RIPPLE_LOGICAL,
    "Compositionality_I": Edit_Eval_Pack.RIPPLE_COMPOSITIONAL_I,
    "Compositionality_II": Edit_Eval_Pack.RIPPLE_COMPOSITIONAL_II,
    "Subject_Aliasing": Edit_Eval_Pack.RIPPLE_ALIASING,
    "Relation_Specificity": Edit_Eval_Pack.RIPPLE_RELATION_SPECIFICITY,
    "Forgetfulness": Edit_Eval_Pack.RIPPLE_PRESERVATION,
}


def load_ripple(
    path: str | Path | None = None,
    quantity: int | None = None,
    seed: int | None = None,
    restrict=None,
    categories=None,
) -> list[Edit_Eval_Pack]:

    path = Path(path) if path else RIPPLE_PATH
    if not RIPPLE_QID_PATH.exists():
        raise FileNotFoundError(
            f"{RIPPLE_QID_PATH} not found. Run: uv run python -m scripts.collect_ripple_QIDs"
        )
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run: uv run python -m scripts.download_benchmarks ripple"
        )
    labels = json.loads(RIPPLE_QID_PATH.read_text())

    def find_entity_string(qid, sentence):
        entry = labels.get(qid)

        if entry is None:
            return None

        all_names = []

        if entry["label"]:
            all_names.append(entry["label"])

        all_names.extend(entry["aliases"])
        names_in_sentence = [n for n in all_names if n in sentence]

        if not names_in_sentence:
            return None

        return max(names_in_sentence, key=len)

    skipped = 0

    # load one case from each of the 3 catagories: popular, random and recent.
    # the ripple path contains 3 json files, one for each category. `recent` is excluded
    # from evaluation because its facts have no previous value — no original_fact, so no
    # target_old — but it is the only untapped source for REMEDI's encoder, which loads it
    # by passing categories explicitly.
    categories = list(categories) if categories else ["popular", "random"]
    edit_datas = []

    # case_number counts across the whole cell, not per category file. Restarting it at
    # each category would give two different facts the same number within one run, which
    # is the one thing case_number has to avoid.
    case_number = 0

    for category in categories:
        category_path = path / f"{category}.json"
        raw = json.loads(category_path.read_text())

        # the window differs per file: one shared range would take the whole of popular
        # (885 rows) and leave that stratum out of the evaluation set. `restrict` carries
        # the same {category: [lo, hi]} shape, and select() prefers it when both are set.
        window = (train_window("ripple") or {}).get(category)
        raw = select(
            raw, quantity, seed, exclude=window, restrict=(restrict or {}).get(category)
        )

        for row, r in raw:
            e = r["edit"]
            sentence = e["prompt"].rstrip().rstrip(".")
            subject = find_entity_string(e["subject_id"], sentence)
            target_new = find_entity_string(e["target_id"], sentence)

            # no english label, or a literal target (dates, counts)
            if not subject or not target_new or not sentence.endswith(target_new):
                skipped += 1
                continue

            old = e.get("original_fact")  # absent in recent.json
            target_old = (
                find_entity_string(old["target_id"], old["prompt"]) if old else None
            )

            pack = Edit_Eval_Pack(
                case_id=f"ripple_{category}_row{row}",
                case_number=case_number,
                benchmark="ripple",
                prompt=sentence[: -len(target_new)].strip().replace(subject, "{}", 1),
                subject=subject,
                target_old=target_old,
                target_new=target_new,
                meta={"example_type": category, "relation": e["relation"]},
            )

            pack.collect_probes(
                probe_category=Edit_Eval_Pack.EFFICACY,
                prompt=pack.construct_prompt(),
                ground_truth=target_new,
                meta={"accept": [target_new]},
            )

            for criterion, probe_category in RIPPLE_CRITERIA.items():
                for g in r.get(criterion, []):
                    for q in g["test_queries"]:
                        accept = [
                            f for a in q["answers"] for f in [a["value"]] + a["aliases"]
                        ]
                        if not accept:  # some test queries ship with no answers
                            continue
                        pack.collect_probes(
                            probe_category=probe_category,
                            prompt=q["prompt"],
                            ground_truth=accept[0],
                            meta={
                                "criterion": criterion,
                                "accept": accept,
                                # prompt AND gold answers: a condition can only be checked
                                # against what it expects. Same shape as a test query. One of
                                # the 945 ships with no answers at all and is dropped, the
                                # same treatment the test queries get above.
                                #
                                # Subject Aliasing is EXEMPT. Its condition is its own test
                                # query restated with the POST-edit answer — 2,408 of 2,408
                                # groups, e.g. test and condition are both "The name of the
                                # country of citizenship of Di Caprio is" -> "Syria"
                                # (build_benchmark_tests.py:42). No unedited model can satisfy
                                # that, so gating on it deletes the criterion: EXP-023 had 0
                                # executable aliasing cases on GPT-2 and 1 on LLaMA. It also
                                # explains why Cohen et al. report Subject Aliasing at
                                # 86.8-100 in EVERY cell of Tables 3-5 — the only cases that
                                # execute are ones where the model already emitted the new
                                # target pre-edit, so they are still correct after it.
                                #
                                # Relation Specificity and Forgetfulness are self-referential
                                # too and are NOT exempt, because their conditions ask for
                                # facts that hold pre-edit: an unrelated relation's true
                                # object, and the ORIGINAL target respectively.
                                "conditions": []
                                if probe_category == Edit_Eval_Pack.RIPPLE_ALIASING
                                else [
                                    {"prompt": c["prompt"], "accept": acc}
                                    for c in g["condition_queries"]
                                    if (
                                        acc := [
                                            f
                                            for a in c["answers"]
                                            for f in [a["value"]] + a["aliases"]
                                        ]
                                    )
                                ],
                            },
                        )

            edit_datas.append(pack)
            case_number += 1

    print(f"[load_ripple] {len(edit_datas)} packs, {skipped} skipped")
    return edit_datas
