"""Benchmark registry - name in, loader out.

Author's own. Dispatches to the per-benchmark loaders in this package. Dataset sources,
papers and licence terms are listed in THIRD_PARTY_LICENSES.md.
"""

from benches.counterfact import load_counterfact
from benches.edit_eval_pack import Edit_Eval_Pack
from benches.genie import load_genie
from benches.mquake import load_mquake
from benches.ripple import load_ripple
from benches.zsre import load_zsre

__all__ = [
    "Available",
    "Edit_Eval_Pack",
    "Loaders",
    "load_benchmark",
    "load_counterfact",
    "load_genie",
    "load_mquake",
    "load_ripple",
    "load_zsre",
]

Loaders = {
    "counterfact": load_counterfact,
    "zsre": load_zsre,
    "ripple": load_ripple,
    "mquake": load_mquake,
    "genie": load_genie,
}

Available = tuple(Loaders)


def load_benchmark(name, quantity, model=None, seed=None):
    if name not in Loaders:
        raise KeyError(f"Unknown benchmark {name!r}. Available: {Available}")
    # genie is the only benchmark whose contents depend on the model under test
    if name == "genie":
        return Loaders[name](quantity=quantity, model=model, seed=seed)
    return Loaders[name](quantity=quantity, seed=seed)
