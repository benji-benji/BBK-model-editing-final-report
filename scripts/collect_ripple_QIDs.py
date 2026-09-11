import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_RIPPLE_DIR = REPO_ROOT / "data" / "raw" / "ripple"
QID_SAVE_DIR = REPO_ROOT / "data" / "raw" / "ripple" / "ripple_qid_labels.json"

API = "https://www.wikidata.org/w/api.php"
HEADERS = {"User-Agent": "bbk-msc-research/0.1 (benwbethell@gmail.com)"}
BATCH = 50

def qids_in_ripple() -> set[str]:
    r"""
    Collects QIDs from Ripple Benchmark raw JSON files
    
    Returns:
        set[str]: A set of unique QIDs found in the Ripple Benchmark JSON files.
        
    checks the qid is valid by checking it matches the regex pattern r"Q\d+".
    
    r"Q\d+" means the string starts with 'Q' followed by one or more digits.
    
    """
    found = set()
    
    for name in RAW_RIPPLE_DIR.iterdir():
        for record in json.loads(name.read_text()):
            edit = record["edit"]
            found.add(edit["subject_id"])
            found.add(edit["target_id"])
            if edit.get("original_fact"):
                found.add(edit["original_fact"]["target_id"])
    
    return {q for q in found if isinstance(q, str) and re.fullmatch(r"Q\d+", q)}

def fetch(qids: list[str]) -> dict:
    query = urllib.parse.urlencode({
        "action": "wbgetentities",
        "ids": "|".join(qids),
        "props": "labels|aliases",
        "languages": "en",
        "format": "json",
    })
    request = urllib.request.Request(f"{API}?{query}", headers=HEADERS)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read())["entities"]
    
def main():
    cache = json.loads(QID_SAVE_DIR.read_text()) if QID_SAVE_DIR.exists() else {}
    todo = sorted(qids_in_ripple() - cache.keys())
    print(f"{len(cache)} cached | {len(todo)} to fetch")
    
    for start in range(0, len(todo), BATCH):
        batch = todo[start:start + BATCH]
        for qid in batch:
            cache.setdefault(qid, {"label": None, "aliases": []})
    
        for qid, entity in fetch(batch).items():
                cache[qid] = {
                    "label": entity.get("labels", {}).get("en", {}).get("value"),
                    "aliases": [a["value"] for a in entity.get("aliases", {}).get("en", [])],
                }
            
        QID_SAVE_DIR.write_text(json.dumps(cache, ensure_ascii=False, sort_keys=True))
        print(f"  {min(start + BATCH, len(todo))}/{len(todo)}", end="\r")
        time.sleep(0.3)
    
    unlabelled = sum(1 for v in cache.values() if not v["label"])
    print(f"\n{len(cache)} QIDs -> {QID_SAVE_DIR} ({unlabelled} with no English label)")
    
    
if __name__ == "__main__":
    main()