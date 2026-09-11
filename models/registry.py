
from __future__ import annotations

from pathlib import Path

from models.model_card import CARD_FILENAME, MODELS_DIR, ModelCard


def _discover(root: Path = MODELS_DIR) -> dict[str, ModelCard]:
    cards: dict[str, ModelCard] = {}
    for card_path in sorted(root.glob(f"*/{CARD_FILENAME}")):
        card = ModelCard.from_json(card_path)
        folder = card_path.parent.name
        if card.name != folder:
            raise ValueError(
                f"{card_path}: card name {card.name!r} does not match folder {folder!r}"
            )
        cards[card.name] = card
    return cards


def all_cards(root: Path = MODELS_DIR) -> dict[str, ModelCard]:
    """Re-read from disk each call, so editing a card.json takes effect immediately."""
    return _discover(root)


def available(root: Path = MODELS_DIR) -> tuple[str, ...]:
    return tuple(all_cards(root))


def get(name: str, root: Path = MODELS_DIR) -> ModelCard:
    cards = all_cards(root)
    if name not in cards:
        raise KeyError(f"Unknown model {name!r}. Available: {tuple(cards)}")
    return cards[name]
