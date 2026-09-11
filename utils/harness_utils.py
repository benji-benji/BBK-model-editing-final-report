
import json, platform
from pathlib import Path
import torch

from benches.load_benchmarks import Edit_Eval_Pack
from eval.score import score_generation, score_probes


CONFIG = json.loads(Path("harness_config.json").read_text())

_conditions_cache = {}

def conditions_hold(model, tokenizer, probe) -> bool:
    """ Check if all conditions for given probe hold


    """
    
    for c in (probe.get("meta") or {}).get("conditions") or ():
        hit, _ = score_generation(model, tokenizer, c["prompt"], c["accept"])
        if not hit:
            return False        
    return True

def apply_condition_gate(model, tokenizer, model_name, bench_name, edit_datas):
    """Apply condition gate to edit data

    This function filters out probes that do not meet the specified conditions
    for a given model and benchmark

    """
    
    
    key = (model_name, bench_name)
    if key not in _conditions_cache:
        failed = {
            (case.case_id, p["category"], p["prompt"])
            for case in edit_datas
            for p in case.probe_list
            if not conditions_hold(model, tokenizer, p)
        }
        _conditions_cache[key] = failed
        total = sum(len(c.probe_list) for c in edit_datas)
        print(f"[conditions] {model_name} · {bench_name}: "
              f"{len(failed)}/{total} probes NOT_EXECUTED")

    failed = _conditions_cache[key]
    for case in edit_datas:
        case.probe_list = [p for p in case.probe_list
                           if (case.case_id, p["category"], p["prompt"]) not in failed]
    return edit_datas


def pick_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    return "cpu" 

def selected(section: str) -> list[str]:
    return [k for k, v in CONFIG[section].items() if v]

def available(section: str) -> list[str]:
    return list(CONFIG[section])

RESULTS_ROOT = Path("results")


def _git_sha() -> str:
    
    
    import subprocess
    try:
        r = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                           capture_output=True, text=True, timeout=5)
        sha = r.stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain"],
                               capture_output=True, text=True, timeout=5).stdout.strip()
        return f"{sha}{'-dirty' if dirty else ''}" if sha else "unknown"
    except Exception:  # noqa: BLE001 — provenance is best-effort, never fatal
        return "unknown"


def new_run_dir(models: list[str], methods: list[str], benches: list[str],
                n: int, device: str, seed=None) -> Path:
    """
    Set up new directory for storing results
    
    Results are stored in directories like:
        results/EXP-012_m2-em6-b5_2026-08-27/ — a fresh directory, never reused. 
    
    The EXP number auto-increments, following MEMIT's run_XXX convention
    (memit/experiments/evaluate.py:75) — the mechanism that stops a rerun overwriting.
    """
    
    
    from datetime import date

    RESULTS_ROOT.mkdir(parents=True, exist_ok=True)
    used = [
        int(p.name.split("-")[1].split("_")[0])
        for p in RESULTS_ROOT.iterdir()
        if p.is_dir() and p.name.startswith("EXP-") and p.name[4:7].isdigit()
    ]
    exp = max(used, default=0) + 1

    slug = f"m{len(models)}-em{len(methods)}-b{len(benches)}"
    d = RESULTS_ROOT / f"EXP-{exp:03d}_{slug}_{date.today().isoformat()}"
    d.mkdir(parents=True)

    (d / "manifest.json").write_text(json.dumps({
        "exp": f"EXP-{exp:03d}",
        "created": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
        "git_sha": _git_sha(),
        "models": models,
        "methods": methods,
        "benchmarks": benches,
        "quantity": n,
        # the sample is only reproducible if the seed travels with the results
        "sample_seed": seed,
        "device": device,
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "torch": torch.__version__,
        "platform": platform.platform(),
        "harness_config": CONFIG,
    }, indent=2) + "\n")
    return d


def cell_dir(run_dir: Path, model: str, method: str, bench: str) -> Path:
    "model / method / bench — n and the config live in the run's manifest, not the path"
    return run_dir / model / method / bench


def save_artifacts(run_dir, model_name, method, pack, collection, quantity_edits):
    """
    Save artifacts to json for a specific model/method/benchmark cell
    
    """
    d = cell_dir(run_dir, model_name, method.name, pack.benchmark)
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{collection[0].score_mode}.json"

    data = json.loads(path.read_text()) if path.exists() else {}
    data[str(pack.case_id)] = [c.get_json() for c in collection]
    path.write_text(json.dumps(data, indent=2))
    
def prepare_edits_for_editor(case):
    "the packs to hand the editor. one per edit — mquake cases carry 1-4."

    if "edits" not in case.meta:
        return [case]  # every other benchmark edits the case itself

    return [
        Edit_Eval_Pack(
            case_id=case.case_id,
            benchmark=case.benchmark,
            prompt=e["prompt"],
            subject=e["subject"],
            target_new=e["target_new"],
            target_old=e["target_old"],
        )
        for e in case.meta["edits"]
    ]
_pre_edit_cache = {}


def pre_edit_scores(model, tokenizer, case, model_name, verify=False):
    """Pre-edit Scorecards for one case, calculated once per (model, bench, case)

    """
    key = (model_name, case.benchmark, case.case_id)

    if key not in _pre_edit_cache:
        _pre_edit_cache[key] = score_probes(
            model, tokenizer, case.probe_list, case, "pre_edit")
        return _pre_edit_cache[key]

    cached = _pre_edit_cache[key]
    if verify and case.probe_list:
        fresh = score_probes(
            model, tokenizer, case.probe_list[:1], case, "pre_edit")[0]

        fields = ("hit", "p_new", "p_old", "correct_new", "correct_old")
        was = [getattr(cached[0], f) for f in fields]
        now = [getattr(fresh, f) for f in fields]
        if was != now:
            raise RuntimeError(
                f"cached pre-edit score for {case.case_id} no longer reproduces on "
                f"{model_name}/{case.benchmark} — the model is not in its unedited state, "
                f"so pre-edit results are NOT method-independent. "
                f"{dict(zip(fields, was))} became {dict(zip(fields, now))}."
            )
    return cached
