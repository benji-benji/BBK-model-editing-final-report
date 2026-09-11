"""Helpers shared by the weight-editing methods.

The prefix-template device follows ROME (Meng et al., 2022, arXiv:2202.05262,
https://github.com/kmeng01/rome), which averages the key estimate over several
contexts so k* is not tied to one phrasing.

`get_subject_token_range` is the author's own.
"""


# Fixed prefixes written for this harness. 
CONTEXT_TEMPLATES = [
    "{}",
    "I have heard it said that {}",
    "The final answer was {}",
    "You might not know this, but {}",
    "Experts have long maintained that {}",
    "Some people believe that {}",
    "According to recent reports, {}",
    "It is widely known that {}",
    "Historically speaking, {}",
    "As a matter of fact, {}",
]


def get_subject_token_range(prompt, subject, tokenizer):
    """Return (start, end) indices of subject tokens in the tokenised prompt."""
    prompt_ids = tokenizer.encode(prompt)

    # Try exact subject first, then fall back to leading-space variant.
    # (Context templates may prepend text, turning "Bob" into " Bob" tokenisation.)
    candidates = [subject]
    if not subject.startswith(" "):
        candidates.append(" " + subject)

    for subj in candidates:
        subject_ids = tokenizer.encode(subj, add_special_tokens=False)
        for i in range(len(prompt_ids) - len(subject_ids) + 1):
            if prompt_ids[i : i + len(subject_ids)] == subject_ids:
                return i, i + len(subject_ids)

    raise ValueError(
        f"Subject tokens not found in prompt.\n"
        f"  prompt:      {prompt!r}\n"
        f"  subject:     {subject!r}\n"
        f"  prompt_ids:  {prompt_ids}\n"
        f"  subject_ids: {subject_ids}"
    )
