"""Whole-word matching in `eval.score.mentions`.

`mentions()` is a deliberate deviation from Cohen et al., who ask only that an alias
"appears in the text" and implement that as a plain substring test. That is unsafe on
these accept lists — `ripple_compositional_i` accepts `['male', 'man', 'm', ...]`, and
'm' is a substring of almost any English sentence, so every method would score 100%.

Every RippleEdits and MQuAKE multihop number in the results rests on this regex, so the
boundary cases below are the ones worth guarding: each of them is a false positive that
the substring version would have scored as a hit.

    uv run pytest tests/test_mentions.py
"""

import pytest

from eval.score import mentions


@pytest.mark.parametrize("text, answers, expected", [
    # plain hits and misses
    ("the answer is Italy",      ["Italy"],  True),
    ("the answer is Italy",      ["France"], False),
    ("the answer is France",     ["France"], True),
    ("it has a long history",    ["Italy"],  False),

    # both answers present — the caller sees two Trues and decides what that means
    ("Italy, formerly France",   ["Italy"],  True),
    ("Italy, formerly France",   ["France"], True),

    # boundary cases: each was a false positive under substring matching
    ("he played strings",        ["string"], False),   # trailing 's'
    ("a character named Romeo",  ["Rome"],   False),   # trailing 'o'
    ("the Parisian suburbs",     ["Paris"],  False),   # trailing 'ian'

    # boundaries that must still match — punctuation is not a word character
    ("located in Rome.",         ["Rome"],   True),
    ("(Rome)",                   ["Rome"],   True),
    ("moved to Rome-adjacent land", ["Rome"], True),

    # non-ASCII word characters either side of the hyphens
    ("in Île-de-France today",   ["Île-de-France"], True),
    ("in Île-de-France today",   ["Lazio"],         False),

    # case-insensitive
    ("THE ANSWER IS ITALY",      ["Italy"],  True),
    ("the answer is italy",      ["Italy"],  True),

    # any accepted alias counts
    ("located in Roma",          ["Rome", "Roma"], True),

    # empty and missing terms are skipped, not matched against everything
    ("the answer is Italy",      ["Italy", ""], True),
    ("the answer is Italy",      [None],     False),
    ("the answer is Italy",      [""],       False),
    ("the answer is Italy",      [],         False),
    ("the answer is Italy",      None,       False),
])
def test_mentions(text, answers, expected):
    assert mentions(text, answers) is expected


def test_regex_metacharacters_are_escaped():
    "an alias is a literal, not a pattern — 'C++' must not blow up or match 'C'"
    assert mentions("written in C++", ["C++"]) is True
    assert mentions("written in C", ["C++"]) is False
