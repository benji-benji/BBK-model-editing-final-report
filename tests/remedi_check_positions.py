"""Does REMEDI inject its direction at the same token in training and at inference?

    uv run python tests/remedi_check_positions.py

No model, no GPU — tokenizers only. Runs in seconds.

Training (scripts/train_encoder.py) finds the subject on the RAW prompt string and
injects at `end - 1`, the last subject token. Inference (edit_methods/remedi.py,
add_updated_activation) instead DECODES the input ids back to text and re-encodes them
to find the subject. On a tokenizer with a BOS token that round trip adds a second BOS
and parses the literal '<|begin_of_text|>' string, so every index shifts by one and the
direction lands on the token AFTER the subject. GPT-2 has no BOS and is unaffected.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from transformers import AutoTokenizer

from edit_methods.remedi import subject_end_in_ids
from utils.edit_utils import get_subject_token_range

CASES = [
    ("The mother tongue of Danielle Darrieux is", "Danielle Darrieux"),
    ("The official religion of Edwin of Northumbria is", "Edwin of Northumbria"),
    ("Toko Yasuda, the", "Toko Yasuda"),
]


def main() -> int:
    bad = 0
    for model in ("gpt2-xl", "llama3-8b"):
        tok = AutoTokenizer.from_pretrained(f"./models/{model}")
        print(f"\n{model}")
        for prompt, subject in CASES:
            ids = tok(prompt, return_tensors="pt").input_ids[0]

            # what training does
            _, end_train = get_subject_token_range(prompt, subject, tok)
            at_train = end_train - 1

            # what inference does
            at_infer = subject_end_in_ids(ids, subject, tok) - 1

            tok_train = tok.decode(ids[at_train]) if at_train < len(ids) else "<OOB>"
            tok_infer = tok.decode(ids[at_infer]) if at_infer < len(ids) else "<OOB>"
            ok = at_train == at_infer
            bad += not ok
            print(f"  {'ok ' if ok else 'BAD'}  train@{at_train} {tok_train!r:<12} "
                  f"infer@{at_infer} {tok_infer!r:<12}  {prompt!r}")

    print(f"\n{'PASS' if not bad else f'FAIL: {bad} mismatches'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
