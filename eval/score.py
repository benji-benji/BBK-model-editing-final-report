"""Score one probe against one model.

Each benchmark is scored the way its own paper scores it, not with one metric across
all five:

    CounterFact   probability comparison p_new vs p_old   (eval_utils_counterfact.py)
    zsRE          argmax exact match                      (eval_utils_zsre.py)
    RippleEdits   generation + containment, 20 tokens     (Cohen et al. 2023, section 5.1)
    MQuAKE        containment (multihop), exact (hops)    (Zhong et al. 2023)
    Genie         probability, except the free-text rungs

The probability path returns the exact-match flag for free, since the logits it needs
are already computed — so zsRE costs nothing extra.
"""

import math
import re

import torch

LOCALITY = {"specificity"}

# Probes scored by generation rather than by probability. A (benchmark, None) entry
# means every probe in that benchmark.
GENERATED = {
    ("ripple", None),                 # all six criteria, and efficacy
    ("mquake", "multihop"),
    ("genie", "abstract_2"),
    ("genie", "abstract_3"),
}


def generation_scored(benchmark, category) -> bool:
    return (benchmark, None) in GENERATED or (benchmark, category) in GENERATED


class ScoreCard:
    def __init__(
        self,
        category,
        probe_prompt,
        p_new,
        p_old,
        score_mode,
        case_number=None,
        # exact-match flags, stored for BOTH answers. Unlike p_new/p_old these cannot
        # be flipped downstream: on a locality probe the answer that should win is the
        # preserved one, so the presentation layer picks the field rather than
        # inverting a number.
        correct_new=None,
        correct_old=None,
        # generation-scored probes only
        hit=None,
        generated=None,
        ):
        self.case_number = case_number
        self.category = category
        self.probe_prompt = probe_prompt
        self.p_new = p_new
        self.p_old = p_old
        # None on generation-scored probes. Deliberately NOT 1.0/0.0 match flags: those
        # made "the model said nothing relevant" score identically to "the old answer
        # won", which is what hid the MQuAKE multihop failure for three weeks.
        self.difference = None if p_new is None or p_old is None else p_new - p_old
        self.score_mode = score_mode
        self.correct_new = correct_new
        self.correct_old = correct_old
        self.hit = hit
        self.generated = generated

    def __repr__(self):
        if self.hit is not None:
            return (f"ScoreCard({self.category}, hit={self.hit}, "
                    f"{self.probe_prompt[:50]!r}, {(self.generated or '')[:40]!r})")
        # p_old is None where the probe has no pre-edit answer at all: MQuAKE's single
        # hops downstream of an edit ask about an entity that did not exist before it.
        num = lambda v: "None" if v is None else f"{v:.4f}"
        return (f"ScoreCard({self.category}, new={num(self.p_new)}, "
                f"old={num(self.p_old)}, diff={num(self.difference)}, "
                f"{self.probe_prompt[:50]!r})")

    def get_json(self):
        return {
            "category": self.category,
            "prompt": self.probe_prompt,
            "case_number": self.case_number,
            "p_new": self.p_new,
            "p_old": self.p_old,
            "difference": self.difference,
            "correct_new": self.correct_new,
            "correct_old": self.correct_old,
            "hit": self.hit,
            "generated": self.generated,
            "score_mode": self.score_mode,
        }


def mentions(text, answers) -> bool:
    """Is any accepted answer present as a WHOLE WORD?

    Cohen et al. ask only that an alias "appears in the text", and their
    queryexecutor.py uses a plain substring test. That is unsafe on these accept lists:
    ripple_compositional_i accepts ['male', 'man', 'm', ...] and 'm' is a substring of
    almost any English text, so every method would score 100%. Whole-word matching is a
    deliberate deviation, and a stricter one.
    """
    return any(
        re.search(rf"(?<!\w){re.escape(a)}(?!\w)", text, re.IGNORECASE)
        for a in (answers or ()) if a
    )


def seq_prob(model, tokenizer, prompt, answer):
    """(probability, exact_match) for `answer` following `prompt`, teacher-forced.

    probability  geometric mean per-token probability, exp(mean log p)
    exact_match  SHARE of target tokens that are the argmax at their own position.
                 Per-token, not all-or-nothing: memit's test_batch_prediction_acc
                 scores each target position as its own item and summarize.py means
                 over them, so a 3-token answer with 2 right scores 0.67, not 0. This
                 is the metric behind the zsRE columns in the ROME, MEMIT and
                 AlphaEdit tables. Free here — the logits already exist.
    """
    if not answer:
        return 0.0, 0.0
    tokenised_prompt = tokenizer(prompt, return_tensors="pt").input_ids.shape[1]
    tokenised_prompt_plus_answer = tokenizer(prompt + " " + answer, return_tensors="pt").input_ids.to(model.device)
    with torch.no_grad():
        logprobs = model(tokenised_prompt_plus_answer).logits[0].log_softmax(-1)
    steps = range(tokenised_prompt, tokenised_prompt_plus_answer.shape[1])
    logp = sum(logprobs[i - 1, tokenised_prompt_plus_answer[0, i]].item() for i in steps)
    exact = sum(int(logprobs[i - 1].argmax()) == int(tokenised_prompt_plus_answer[0, i])
                for i in steps) / len(steps)
    return math.exp(logp / len(steps)), exact


def score_generation(model, tokenizer, prompt, answers, max_new_tokens=20):
    """(hit, text) — Cohen et al.'s metric: generate, then look for the gold answer.

    20 tokens and greedy, matching the paper. `answers` is the flattened accept list —
    every alias of every gold object. The paper counts a generation correct if it
    matches AT LEAST ONE gold object, which is what flattening gives; their code
    instead requires all of them, contradicting the text. Following the paper.
    """
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    text = tokenizer.decode(out[0][inputs["input_ids"].shape[1]:],
                            skip_special_tokens=True)
    return mentions(text, answers), text.strip()

def score_generation_batch(model, tokenizer, prompts, answers, max_new_tokens=20):
    """[(hit, text)] for a batch of prompts — same metric as score_generation, one call.

    Padding is LEFT, or every row would generate from its own pad tokens, and it is passed
    per call rather than set on the tokenizer: ROME (utils/edit_training.py:57) and MEMIT
    (edit_methods/memit.py:65) both depend on RIGHT padding and share this tokenizer object.
    """
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    enc = tokenizer(prompts, return_tensors="pt", padding=True,
                    padding_side="left").to(model.device)
    with torch.no_grad():
        out = model.generate(
            **enc,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    texts = tokenizer.batch_decode(out[:, enc["input_ids"].shape[1]:],
                                   skip_special_tokens=True)
    return [(mentions(t, a), t.strip()) for t, a in zip(texts, answers)]


def score_probes(model, tokenizer, probes, case, score_mode, batch_size=16):
    """ScoreCards for `probes`, in the order given, generating in batches.

    RippleEdits is 72% of a run's forward passes and every probe there is a 20-token
    generation, so one prompt per call left most of the GPU idle. Probability-scored probes
    still go one at a time through score_probe — they are two forward passes each and
    batching them would buy little for a much larger change.
    """
    cards = [None] * len(probes)
    generated = []

    for i, probe in enumerate(probes):
        if generation_scored(case.benchmark, probe["category"]):
            generated.append((i, probe))
        else:
            cards[i] = score_probe(model, tokenizer, probe, case, score_mode)

    for start in range(0, len(generated), batch_size):
        chunk = generated[start:start + batch_size]
        accepts = [(p.get("meta") or {}).get("accept")
                   or (p.get("meta") or {}).get("answer_new")
                   or [case.target_new] for _, p in chunk]
        results = score_generation_batch(
            model, tokenizer, [p["prompt"] for _, p in chunk], accepts)
        for (i, probe), (hit, text) in zip(chunk, results):
            cards[i] = ScoreCard(
                probe["category"],
                probe["prompt"],
                None,
                None,
                score_mode=score_mode,
                case_number=case.case_number,
                hit=hit,
                generated=text,
            )
    return cards


def score_probe(model, tokenizer, probe, case, score_mode) -> ScoreCard:

    probe_prompt = probe["prompt"]
    category = probe["category"]
    meta = probe.get("meta") or {}

    if generation_scored(case.benchmark, category):
        # the gold answer set, already built by the loaders:
        #   ripple  [a["value"]] + a["aliases"] per gold answer
        #   mquake  [answer] + answer_alias
        accept = meta.get("accept") or meta.get("answer_new") or [case.target_new]
        hit, text = score_generation(model, tokenizer, probe_prompt, accept)
        return ScoreCard(
            category,
            probe_prompt,
            None,
            None,
            score_mode=score_mode,
            case_number=case.case_number,
            hit=hit,
            generated=text,
            )

    answers_new = meta.get("accept") or meta.get("answer_new") or [case.target_new]

    if category in LOCALITY:
        answers_old = [probe.get("ground_truth") or case.target_old]
    else:
        answers_old = meta["answer_old"] if "answer_old" in meta else [case.target_old]

    def best(answers):
        scored = [seq_prob(model, tokenizer, probe_prompt, a) for a in answers if a]
        if not scored:
            return None, None          # no answer of this kind exists for this probe
        return max(p for p, _ in scored), max(c for _, c in scored)

    p_new, correct_new = best(answers_new)
    p_old, correct_old = best(answers_old)

    return ScoreCard(
        category,
        probe_prompt,
        p_new,
        p_old,
        score_mode=score_mode,
        case_number=case.case_number,
        correct_new=correct_new,
        correct_old=correct_old,
        )
