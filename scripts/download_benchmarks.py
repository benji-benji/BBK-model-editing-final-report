"""Download benchmark datasets to data/raw/<benchmark>/.

    uv run python -m scripts.download_benchmarks              # counterfact + zsre
    uv run python -m scripts.download_benchmarks --all
    uv run python -m scripts.download_benchmarks mquake ripple
    uv run python -m scripts.download_benchmarks --verify     # re-check checksums only

Real files on disk — no HuggingFace `datasets` dependency. Chosen because RunPod
containers are ephemeral (a library cache re-downloads on every spin-up), and because
pinning exact files plus checksums makes the evaluation reproducible.

**Files land under the names `benches/load_benchmarks.py` expects**, not the names
upstream uses — `zsre_mend_eval.json` becomes `zsre/zsre.json`, `MQuAKE-CF-3k-v2.json`
becomes `mquake/mquake.json`. The loaders hardcode those paths, so renaming here is what
makes a fresh clone runnable.

Two of the five benchmarks are NOT downloadable and are not handled here:

  ripple_qid_labels.json   generated — `uv run python -m scripts.collect_ripple_QIDs`
  genie                    generated — see the Genie pipeline in the README

Every fetched file is recorded in data/raw/MANIFEST.json with its sha256, so a later run
can verify nothing upstream changed underneath us.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

RAW_DIR = Path("data") / "raw"
MANIFEST = RAW_DIR / "MANIFEST.json"

# (url, destination filename relative to data/raw/<name>/)
DIRECT: dict[str, list[tuple[str, str]]] = {
    "counterfact": [
        ("https://memit.baulab.info/data/dsets/counterfact.json", "counterfact.json"),
    ],
    "zsre": [
        ("https://memit.baulab.info/data/dsets/zsre_mend_eval.json", "zsre.json"),
    ],
    # v2 fixes a known knowledge-conflict bug in the original MQuAKE-CF-3k. Use v2.
    # The full CF is fetched alongside it for REMEDI's encoder only: 6,218 of its 9,218
    # cases have no content match in the 3k, so it supplies a training set disjoint from
    # what the harness evaluates. It predates the v2 fix — a stated limitation.
    "mquake": [
        (
            "https://raw.githubusercontent.com/princeton-nlp/MQuAKE/main/datasets/MQuAKE-CF-3k-v2.json",
            "mquake.json",
        ),
        (
            "https://raw.githubusercontent.com/princeton-nlp/MQuAKE/main/datasets/MQuAKE-CF.json",
            "mquake_cf_full.json",
        ),
    ],
}

# RippleEdits ships its three splits inside the repo rather than at stable URLs, so this
# clones shallow into a temp dir and lifts out the files the loader names.
CLONE: dict[str, tuple[str, list[str]]] = {
    "ripple": ("https://github.com/edenbiran/RippleEdits.git",
               ["popular.json", "random.json", "recent.json"]),
}

PHASE_1 = ["counterfact", "zsre"]
ALL = list(DIRECT) + list(CLONE)


def sha256(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while block := f.read(chunk):
            h.update(block)
    return h.hexdigest()


def human(n: float) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}TB"


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}


def save_manifest(m: dict) -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(m, indent=2, sort_keys=True) + "\n")


def record(manifest: dict, key: str, dest: Path, url: str) -> None:
    digest = sha256(dest)
    prev = manifest.get(key, {}).get("sha256")
    if prev and prev != digest:
        print(f"  [WARN] {key} sha256 changed since last run!")
        print(f"         was {prev}")
        print(f"         now {digest}")
    manifest[key] = {"url": url, "sha256": digest, "bytes": dest.stat().st_size}
    print(f"  [ok  ] {key}  {human(dest.stat().st_size)}  sha256={digest[:12]}…")


def fetch_direct(name: str, manifest: dict) -> None:
    out_dir = RAW_DIR / name
    out_dir.mkdir(parents=True, exist_ok=True)

    for url, filename in DIRECT[name]:
        dest = out_dir / filename
        if dest.exists():
            print(f"  [skip] {filename} already present ({human(dest.stat().st_size)})")
        else:
            print(f"  [get ] {url}\n         -> {dest}")
            try:
                urllib.request.urlretrieve(url, dest)
            except Exception as e:  # noqa: BLE001 — report and continue to the next file
                print(f"  [FAIL] {filename}: {e}")
                continue
        record(manifest, f"{name}/{filename}", dest, url)


def fetch_clone(name: str, manifest: dict) -> None:
    url, wanted = CLONE[name]
    out_dir = RAW_DIR / name
    out_dir.mkdir(parents=True, exist_ok=True)

    if all((out_dir / w).exists() for w in wanted):
        print(f"  [skip] {name}: all of {wanted} already present")
        for w in wanted:
            record(manifest, f"{name}/{w}", out_dir / w, url)
        return

    with tempfile.TemporaryDirectory() as tmp:
        print(f"  [git ] clone --depth 1 {url}")
        r = subprocess.run(
            ["git", "clone", "--depth", "1", url, tmp + "/repo"],
            capture_output=True, text=True,
        )
        if r.returncode != 0:
            print(f"  [FAIL] {name}: {r.stderr.strip().splitlines()[-1:] or r.stderr}")
            return

        repo = Path(tmp) / "repo"
        rev = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True
        ).stdout.strip()

        for w in wanted:
            # the split files sit somewhere under the repo's data dir; glob rather than
            # hardcode, so an upstream reorganisation does not silently produce nothing.
            hits = sorted(repo.rglob(w))
            if not hits:
                print(f"  [FAIL] {w} not found anywhere in {url} — check the repo layout")
                continue
            if len(hits) > 1:
                print(f"  [WARN] {w} matched {len(hits)} paths, taking {hits[0].relative_to(repo)}")
            shutil.copy2(hits[0], out_dir / w)
            record(manifest, f"{name}/{w}", out_dir / w, f"{url}@{rev[:12]}")

    print(f"         rev={rev[:12]}")
    print("  [note] ripple_qid_labels.json is generated, not downloaded:")
    print("         uv run python -m scripts.collect_ripple_QIDs")


def verify(manifest: dict) -> int:
    bad = 0
    for key, rec in sorted(manifest.items()):
        path = RAW_DIR / key
        if not path.exists():
            print(f"  [MISS] {key}")
            bad += 1
        elif sha256(path) != rec["sha256"]:
            print(f"  [DIFF] {key}\n         expected {rec['sha256']}\n         got      {sha256(path)}")
            bad += 1
        else:
            print(f"  [ok  ] {key}")
    return bad


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("names", nargs="*", help=f"benchmarks to fetch; default: {PHASE_1}")
    ap.add_argument("--all", action="store_true", help="fetch every benchmark")
    ap.add_argument("--verify", action="store_true", help="re-check checksums only")
    args = ap.parse_args()

    manifest = load_manifest()

    if args.verify:
        print(f"Verifying against {MANIFEST}")
        bad = verify(manifest)
        print(f"\n{'OK' if bad == 0 else f'{bad} problem(s)'}")
        return 1 if bad else 0

    names = ALL if args.all else (args.names or PHASE_1)
    unknown = [n for n in names if n not in ALL]
    if unknown:
        print(f"Unknown: {unknown}\nAvailable: {ALL}", file=sys.stderr)
        return 2

    for name in names:
        print(f"\n{name}")
        fetch_direct(name, manifest) if name in DIRECT else fetch_clone(name, manifest)

    save_manifest(manifest)
    print(f"\nManifest written to {MANIFEST}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
