"""
    Utilities for managing model state, including loading model cards,
    resolving model layers, and handling snapshots of edited weights.


"""

import json
from pathlib import Path

import torch


def load_card(model_name: str) -> json:
    return json.load(open(f"./models/{model_name}/card.json", "r"))

def resolve(model, path: str):
    """'transformer.h.17.mlp.c_proj' -> model.transformer.h[17].mlp.c_proj"""
    mod = model
    for part in path.split("."):
        mod = mod[int(part)] if part.isdigit() else getattr(mod, part)
    return mod

def layer_block(model, card: dict, layer: int):

    return resolve(model, card["layer_tmpl"].format(layer))

def mlp_proj(model, card: dict, layer: int):

    return resolve(model, card["mlp_proj_tmpl"].format(layer))

def mlp_block(model, card: dict, layer: int):

    return resolve(model, card["mlp_proj_tmpl"].rsplit(".", 1)[0].format(layer))

def edited_weights(model, card: dict):
    """(path, weight) for every weight this card's edit band touches."""
    tmpl = card["mlp_proj_tmpl"]
    for l in card["edit_layers"]:
        path = tmpl.format(l)
        yield path, resolve(model, path).weight

def snapshot(model, card: dict) -> dict[str, torch.Tensor]:
    return {path: w.detach().clone() for path, w in edited_weights(model, card)}

def restore(model, card: dict, snap: dict[str, torch.Tensor]) -> None:
    with torch.no_grad():
        for path, w in edited_weights(model, card):
            w.copy_(snap[path])

def max_drift(model, card: dict, snap: dict[str, torch.Tensor]) -> float:
    worst = 0.0
    with torch.no_grad():
        for path, w in edited_weights(model, card):
            worst = max(worst, float((w - snap[path]).abs().max()))
    return worst
