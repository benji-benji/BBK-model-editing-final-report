from pprint import pprint

from utils.harness_utils import prepare_edits_for_editor
from benches.load_benchmarks import load_benchmark

# check multi-edit cases expand into one pack per edit

case = load_benchmark("mquake", 1)[0]
packs = prepare_edits_for_editor(case)

pprint(case)
print(f"\n{len(packs)} edits to apply:")
for p in packs:
    pprint((p.subject, p.target_new, p.target_old))