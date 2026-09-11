# helper script to view 1 case raw benchmark data
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
COUNTERFACT_PATH = REPO_ROOT / "data" / "raw" / "counterfact" / "counterfact.json"
ZSRE_PATH = REPO_ROOT / "data" / "raw" / "zsre" / "zsre.json"
RIPPLE_PATH = REPO_ROOT / "data" / "raw" / "ripple" / "popular.json"
MQUAKE_PATH = REPO_ROOT / "data" / "raw" / "mquake" / "mquake.json"

BENCHES = {
    "counterfact": COUNTERFACT_PATH,
    "zsre": ZSRE_PATH,
    "ripple": RIPPLE_PATH,
    "mquake": MQUAKE_PATH,
}

# json = json.load(open(RIPPLE_PATH, "r"))
# pprint(json[0])


for BENCH in BENCHES:
    raw = json.load(open(BENCHES[BENCH], "r"))
    example = raw[0]
    save_path = REPO_ROOT / "docs" / "benchmark_samples" / f"{BENCH}_example.json"
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_text(json.dumps(example, indent=4))
    

