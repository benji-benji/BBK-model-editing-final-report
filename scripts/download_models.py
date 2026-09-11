"""Download model weights to models/<name>/.

    uv run python -m scripts.download_models                  # gpt2-xl + llama3-8b
    uv run python -m scripts.download_models --all
    uv run python -m scripts.download_models gpt2-xl
    uv run python -m scripts.download_models --check          # report what is on disk

A fresh clone has no weights. `.gitignore` keeps `models/*/card.json` and excludes
everything else in those folders, so this script is what makes a clone runnable.

Which models exist is read from the cards, not hardcoded here — `models/<name>/card.json`
supplies the `hf_id` to fetch. Adding a model still means adding one card.json.

Files land flat in `models/<name>/` alongside the card, because `harness.py` and the
scripts load with `from_pretrained(f"./models/{model_name}")`. This is a plain directory,
not a HuggingFace cache: no symlinks, nothing outside the repo, so it survives being
moved onto a RunPod network volume.

Only the files `from_pretrained` actually reads are fetched (see ALLOW). That matters
more than it sounds. Measured against the live repos:

    gpt2-xl                      keeps  6.0 GB, skips 23.9 GB
    meta-llama/Meta-Llama-3-8B   keeps 15.0 GB, skips 15.0 GB

What gets skipped is duplicate copies of the same weights in other formats — gpt2-xl
ships flax, TensorFlow, Rust and `pytorch_model.bin` alongside its safetensors, and
meta-llama ships `original/consolidated.00.pth`. Fetching a whole snapshot would move
60 GB to land the 21 GB the harness loads.

Llama-3-8B arrives as four shards plus `model.safetensors.index.json` rather than the
single consolidated `model.safetensors` currently in `models/llama3-8b/`. Both layouts
load identically through `from_pretrained`; only the file listing differs.

meta-llama/Meta-Llama-3-8B is a gated repo. Accept the licence on the model page while
signed in, then authenticate once with `uv run hf auth login` (or export HF_TOKEN)
before running this.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import shutil
import sys
from pathlib import Path

from models.model_card import CARD_FILENAME, MODELS_DIR

ALLOW = [
    "config.json",
    "generation_config.json",
    "tokenizer.json",
    "tokenizer_config.json",
    "tokenizer.model",
    "special_tokens_map.json",
    "vocab.json",
    "merges.txt",
    "*.safetensors",
    "*.safetensors.index.json",
]

DEFAULT = ["gpt2-xl", "llama3-8b"]


def load_cards(root: Path = MODELS_DIR) -> dict[str, dict]:
    """name -> raw card dict, for every models/*/card.json.

    Deliberately reads the JSON rather than going through models.registry / ModelCard.
    Downloading weights needs two fields, `name` and `hf_id`, and none of the editing
    semantics the dataclass validates. Parsing through ModelCard would let an unrelated
    schema drift in one card stop every model from being fetched — which is the opposite
    of what a script that exists to make a fresh clone runnable should do. (As of writing,
    the gpt2-xl and llama3-8b cards do carry stale `model_dim`/`model_mlp_dim` keys that
    ModelCard rejects.)
    """
    cards: dict[str, dict] = {}
    for card_path in sorted(root.glob(f"*/{CARD_FILENAME}")):
        data = json.loads(card_path.read_text())
        folder = card_path.parent.name
        name = data.get("name", folder)
        if name != folder:
            print(f"  [WARN] {card_path}: name {name!r} does not match folder {folder!r}")
        if not data.get("hf_id"):
            print(f"  [WARN] {card_path}: no hf_id, skipping")
            continue
        cards[folder] = data
    return cards


def human(n: float) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}TB"


def dir_size(path: Path) -> int:
    return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())


def weights_present(path: Path) -> bool:
    """A folder counts as populated only with a config AND at least one weight shard.

    Checking for the folder alone would be wrong: every model folder already exists in a
    fresh clone, because card.json is tracked.
    """
    return (path / "config.json").exists() and any(path.glob("*.safetensors"))


def remote_size(hf_id: str) -> int | None:
    """Total bytes of the files ALLOW will actually fetch, or None if the API call fails.

    Advisory only — used for the disk-space check and the size line. A failure here must
    not stop a download that would otherwise succeed.
    """
    try:
        from huggingface_hub import HfApi

        info = HfApi().model_info(hf_id, files_metadata=True)
    except Exception:  # noqa: BLE001 — advisory only, see docstring
        return None

    total = 0
    for sib in info.siblings or []:
        if any(fnmatch.fnmatch(sib.rfilename, pat) for pat in ALLOW):
            total += sib.size or 0
    return total or None


def fetch(name: str, hf_id: str, force: bool) -> bool:
    from huggingface_hub import snapshot_download
    from huggingface_hub.errors import GatedRepoError, RepositoryNotFoundError

    dest = MODELS_DIR / name
    dest.mkdir(parents=True, exist_ok=True)

    if weights_present(dest) and not force:
        print(f"  [skip] already present ({human(dir_size(dest))}) — --force to refetch")
        return True

    want = remote_size(hf_id)
    free = shutil.disk_usage(dest).free
    if want:
        print(f"  [get ] {hf_id}  {human(want)} -> {dest}")
        if free < want * 1.1:
            print(f"  [FAIL] only {human(free)} free, need ~{human(want * 1.1)}")
            return False
    else:
        print(f"  [get ] {hf_id} -> {dest}   ({human(free)} free)")

    try:
        snapshot_download(
            repo_id=hf_id,
            local_dir=dest,
            allow_patterns=ALLOW,
            max_workers=4,
        )
    except GatedRepoError:
        print(f"  [FAIL] {hf_id} is gated.")
        print(f"         Accept the licence at https://huggingface.co/{hf_id}")
        print("         then authenticate: uv run hf auth login")
        return False
    except RepositoryNotFoundError:
        print(f"  [FAIL] {hf_id} not found — check hf_id in {dest / CARD_FILENAME}")
        return False
    except Exception as e:  # noqa: BLE001 — report and let the caller continue
        print(f"  [FAIL] {name}: {e}")
        return False

    if not weights_present(dest):
        print(f"  [FAIL] {name}: no .safetensors landed — ALLOW may not match this repo")
        return False

    print(f"  [ok  ] {name}  {human(dir_size(dest))}")
    return True


def check(cards: dict[str, dict]) -> int:
    missing = 0
    for name, card in sorted(cards.items()):
        path = MODELS_DIR / name
        if weights_present(path):
            print(f"  [ok  ] {name:14s} {human(dir_size(path)):>9s}  {card['hf_id']}")
        else:
            print(f"  [MISS] {name:14s} {'—':>9s}  {card['hf_id']}")
            missing += 1
        if card.get("local_dir") is None:
            print(f"         note: local_dir is null in {path / CARD_FILENAME}")
    return missing


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("names", nargs="*", help=f"models to fetch; default: {DEFAULT}")
    ap.add_argument("--all", action="store_true", help="fetch every model with a card")
    ap.add_argument("--check", action="store_true", help="report what is on disk only")
    ap.add_argument("--force", action="store_true", help="refetch even if present")
    args = ap.parse_args()

    cards = load_cards()

    if args.check:
        print(f"Models in {MODELS_DIR}/")
        missing = check(cards)
        print(f"\n{'OK' if missing == 0 else f'{missing} missing'}")
        return 1 if missing else 0

    names = list(cards) if args.all else (args.names or DEFAULT)
    unknown = [n for n in names if n not in cards]
    if unknown:
        print(f"Unknown: {unknown}\nAvailable: {tuple(cards)}", file=sys.stderr)
        return 2

    failed = []
    for name in names:
        print(f"\n{name}")
        if not fetch(name, cards[name]["hf_id"], args.force):
            failed.append(name)

    if failed:
        print(f"\n{len(failed)} failed: {failed}")
        return 1
    print(f"\n{len(names)} model(s) ready in {MODELS_DIR}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
