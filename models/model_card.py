"""
Model card class for storing metadata and module paths for a transformer model.

"""


from __future__ import annotations

import json
from dataclasses import dataclass, field, fields
from pathlib import Path

MODELS_DIR = Path("models")
CARD_FILENAME = "card.json"


@dataclass(frozen=True)
class ModelCard:
    name: str
    hf_id: str
    arch_class: str

    mlp_proj_tmpl: str      
    layer_tmpl: str         
    ln_f: str               
    lm_head: str           

    edit_layers: tuple[int, ...] = ()
    mom2_update_weight: int = 20000
    weight_transposed: bool = False   
    leading_space: bool = True        
    use_chat_template: bool = False  

    local_dir: str | None = None      
    notes: tuple[str, ...] = field(default_factory=tuple)

    # ---- construction ----

    @classmethod
    def from_json(cls, path: str | Path) -> ModelCard:
        data = json.loads(Path(path).read_text())
        known = {f.name for f in fields(cls)}
        unknown = set(data) - known
        if unknown:
            raise ValueError(f"{path}: unknown card fields {sorted(unknown)}")
        if "edit_layers" in data:
            data["edit_layers"] = tuple(data["edit_layers"])
        if "notes" in data:
            data["notes"] = tuple(data["notes"])
        return cls(**data)

    # ---- module paths ----

    def mlp_module(self, layer: int) -> str:
        return self.mlp_proj_tmpl.format(layer)

    def layer_module(self, layer: int) -> str:
        return self.layer_tmpl.format(layer)

    def resolve(self, model, path: str):

        mod = model
        for part in path.split("."):
            mod = mod[int(part)] if part.isdigit() else getattr(mod, part)
        return mod

    def mlp_proj(self, model, layer: int):
        """The edited weight matrix's module at `layer`."""
        return self.resolve(model, self.mlp_module(layer))

    def block(self, model, layer: int):
        """The transformer block at `layer` (hidden-state hook site)."""
        return self.resolve(model, self.layer_module(layer))

    # ---- paths ----

    def cov_path(self, layer: int, root: str | Path = "artifacts/covariance") -> Path:

        return Path(root) / self.name / f"c_layer_{layer}.pt"

    # ---- validation ----

    def dims(self, model) -> dict[str, int]:
        c = model.config
        n_layers = getattr(c, "n_layer", None) or getattr(c, "num_hidden_layers")
        d_model = getattr(c, "n_embd", None) or getattr(c, "hidden_size")
        d_mlp = (
            getattr(c, "n_inner", None)
            or getattr(c, "intermediate_size", None)
            or 4 * d_model
        )
        return {"n_layers": n_layers, "d_model": d_model, "d_mlp": d_mlp}

    def validate(self, model) -> dict[str, int]:

        actual = type(model).__name__
        if actual != self.arch_class:
            raise ValueError(f"card {self.name!r} expects {self.arch_class}, got {actual}")
        d = self.dims(model)
        bad = [l for l in self.edit_layers if l >= d["n_layers"]]
        if bad:
            raise ValueError(
                f"edit_layers {bad} out of range for {self.name} (n_layers={d['n_layers']})"
            )
        for l in self.edit_layers:
            for path in (self.mlp_module(l), self.layer_module(l)):
                try:
                    self.resolve(model, path)
                except (AttributeError, IndexError, KeyError) as e:
                    raise ValueError(
                        f"module path not found on {self.name}: {path!r} ({e})"
                    ) from e
        return d
