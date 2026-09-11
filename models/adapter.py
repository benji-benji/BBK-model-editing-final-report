"""
Model adapter helpers for tokenising prompts and handling subject token ranges.
    
"""


from __future__ import annotations

from dataclasses import dataclass

from models.model_card import ModelCard


@dataclass(frozen=True)
class TokenisedProbe:

    input_ids: list[int]
    prompt_len: int
    target_ids: list[int]
    prompt_text: str
    ground_truth_text: str

    @property
    def target_slice(self) -> slice:
        return slice(self.prompt_len, self.prompt_len + len(self.target_ids))


class ModelAdapter:
    def __init__(self, card: ModelCard, tokenizer):
        self.card = card
        self.tok = tokenizer
        if self.tok.pad_token is None:
            self.tok.pad_token = self.tok.eos_token

    # ---- text shaping ----

    def format_prompt(self, prompt: str) -> str:

        if not self.card.use_chat_template:
            return prompt
        if getattr(self.tok, "chat_template", None) is None:
            raise ValueError(
                f"{self.card.name} sets use_chat_template=True but its tokenizer "
                "has no chat_template"
            )
        return self.tok.apply_chat_template(
            [{"role": "user", "content": prompt}],
            tokenize=False,
            add_generation_prompt=True,
        )

    def format_gold(self, gold: str) -> str:
        """Leading-space convention. GPT-2 BPE needs ' English', not 'English'."""
        if self.card.leading_space and not gold.startswith(" "):
            return " " + gold
        return gold

    # ---- tokenising ----

    def encode(self, text: str) -> list[int]:
        return self.tok(text, add_special_tokens=False)["input_ids"]

    def tokenise(self, prompt: str, gold: str) -> TokenisedProbe:

        prompt_text = self.format_prompt(prompt)
        ground_truth_text = self.format_gold(gold)
        prompt_ids = self.encode(prompt_text)
        target_ids = self.encode(ground_truth_text)
        return TokenisedProbe(
            input_ids=prompt_ids + target_ids,
            prompt_len=len(prompt_ids),
            target_ids=target_ids,
            prompt_text=prompt_text,
            ground_truth_text=ground_truth_text,
        )

    # ---- editing helpers ----

    def mlp_module(self, layer: int) -> str:
        return self.card.mlp_module(layer)

    def cov_path(self, layer: int):
        return self.card.cov_path(layer)

    def subject_token_range(self, prompt: str, subject: str) -> tuple[int, int]:
        
        if "{}" in prompt:
            prompt = prompt.format(subject)
        prompt_text = self.format_prompt(prompt)
        char_start = prompt_text.find(subject)
        if char_start < 0:
            raise ValueError(f"subject {subject!r} not found in prompt {prompt_text!r}")
        char_end = char_start + len(subject)

        enc = self.tok(prompt_text, add_special_tokens=False, return_offsets_mapping=True)
        offsets = enc["offset_mapping"]
        idx = [
            i for i, (s, e) in enumerate(offsets)
            if s < char_end and e > char_start        # token overlaps the subject span
        ]
        if not idx:
            raise ValueError(f"no tokens overlap subject {subject!r}")
        return idx[0], idx[-1] + 1                     # [start, end) — end-1 is last token
