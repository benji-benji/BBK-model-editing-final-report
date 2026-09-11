"""REMEDI's train/test split.
Attribution: this file is the author's own. The train/test split is a requirement of
this harness rather than anything the REMEDI paper or its reference implementation
specifies. The borrowed training objective is in scripts/train_encoder.py.
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "edit_methods" / "edit_method_config.json"
ENCODER_DIR = REPO_ROOT / "models" / "encoders"
MQUAKE_FULL_PATH = REPO_ROOT / "data" / "raw" / "mquake" / "mquake_cf_full.json"


def train_window(bench):

    try:
        windows = json.loads(CONFIG_PATH.read_text())["remedi"]["train_windows"]
    except Exception:
        return None
    window = windows.get(bench)
    if isinstance(window, dict):
        return window
    return tuple(window) if window else None


def encoder_path(model_name, bench, layer):

    return ENCODER_DIR / model_name / f"{bench}_layer_{layer}.pt"


def load_training_split(bench, model=None):

    return [p for p in _split_for(bench, model) if (p.target_new or "").strip()]


def _split_for(bench, model):
    if bench == "genie":
        return _genie_rejects(model)
    if bench == "mquake":
        return _mquake_unevaluated()
    if bench == "ripple":
        return _ripple_train()
    return _windowed(bench)


def _windowed(bench):

    from benches.load_benchmarks import Loaders

    window = train_window(bench)
    if window is None:
        raise ValueError(f"no REMEDI training window configured for {bench!r}")
    return Loaders[bench](restrict=window)


def _mquake_unevaluated():

    from benches.load_benchmarks import load_mquake

    if not MQUAKE_FULL_PATH.exists():
        raise FileNotFoundError(
            f"{MQUAKE_FULL_PATH} not found. "
            f"Run: uv run python -m scripts.download_benchmarks mquake"
        )
    evaluated = {_mquake_identity(p) for p in load_mquake()}
    return [p for p in load_mquake(path=MQUAKE_FULL_PATH)
            if _mquake_identity(p) not in evaluated]


def _mquake_identity(pack):
    """Content identity of an MQuAKE case: the questions asked and the rewrites requested."""
    return (tuple(pr["prompt"] for pr in pack.probe_list if pr["category"] == "multihop"),
            tuple((e["prompt"], e["subject"], e["target_new"]) for e in pack.meta["edits"]))


def _ripple_train():

    from benches.load_benchmarks import load_ripple

    return (load_ripple(restrict=train_window("ripple"))
            + load_ripple(categories=("recent",)))


def _genie_rejects(model):
 
    from benches.load_benchmarks import GENIE_DIR, genie_path, load_genie

    kept = genie_path(model)
    if kept.name == "genie.json":
        raise FileNotFoundError(
            f"genie_{model}.json not found — run scripts.genie_filter_by_model first. "
            f"Without it every record counts as kept and the training set is empty."
        )

    kept_ids = {r["case_id"] for r in json.loads(kept.read_text())}
    return [p for p in load_genie(path=GENIE_DIR / "genie.json")
            if p.case_id not in kept_ids]
