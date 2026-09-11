import json
from pprint import pprint
from pathlib import Path

from benches.load_benchmarks import load_benchmark

# simple pipeline to test benchmarks are loading

bench_name = "genie"
quantity_edits = 3

# load the benchmark - counterfact
edit_datas = load_benchmark(bench_name, quantity_edits)

pprint(type(edit_datas))
pprint(len(edit_datas))
pprint(edit_datas)
pprint(edit_datas[0].probe_list)

# load json popular and print raw benchmark data for the first case
# categories = ["popular", "random"]





