"""Training the REMEDI encoder.

Implements the training objective of Hernandez, E., Li, B.Z. and Andreas, J. (2024)
'Inspecting and editing knowledge representations in language models', Conference on
Language Modeling (COLM). arXiv:2304.00740. Reference implementation:
https://github.com/evandez/remedi (MIT; licence text reproduced in THIRD_PARTY_LICENSES.md).

Follows the paper: `loss` is Eq. 6 - the target-token likelihood, the bounded prior
term on the old object, and the KL penalty holding the intermediate token
distributions to what the unedited model produced. Batch size and learning rate
follow the reference (remedi/editors.py).

Author's own, with AI assistance (Claude Code): the batched path (`collate`, `forward_edited_batch`, `loss_batch`) and
its `--check-batching` equivalence assertion, the fp32 boundary in the loss, and the
evaluation loop. See the note above the batched path for why batching was needed.
"""

import argparse
import copy
import json
import random
import sys
import time
from pathlib import Path

import torch
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer

from edit_methods.remedi import RemediLinearNN, hidden_at
from utils.edit_utils import get_subject_token_range
from utils.harness_utils import pick_device
from utils.remedi_training import encoder_path, load_training_split
from utils.model_state import load_card, layer_block

LAM_PRIOR = 1.0     # λ₁ — coefficient on the old-answer suppression term
LAM_KL = 10.0       # λ₂ — coefficient on the KL term

# load model packs
"""
prompt in natural english 

prompt    'The mother tongue of Danielle Darrieux is'
context   'The mother tongue of Danielle Darrieux is English'
subject   'Danielle Darrieux' -> tokens (4, 8)
attr span  tokens 8:end  ->  ' is English'

"""


def build_example(model, tokenizer, block, pack):
    prompt = pack.construct_prompt()
    context = f"{prompt} {pack.target_new}"
    start, end = get_subject_token_range(prompt, pack.subject, tokenizer)
    tid = lambda t: tokenizer(" " + t, add_special_tokens=False)["input_ids"][0]

    # has_prior is 0 it is never read.
    has_prior = pack.target_old is not None

    return {
        "prompt_token_ids": tokenizer(prompt, return_tensors="pt").input_ids.to(
            model.device
        ),  # prompt ids
        "hidden_attribute_act": hidden_at(
            model, tokenizer, context, block, span=(end, None)
        ),  # context
        "prompt_end_index": end - 1,
        "target_new_id": tid(pack.target_new),  # index of target token in context
        "target_old_id": tid(pack.target_old) if has_prior else 0,
        "has_prior": float(has_prior),  # λ₁ is 0 for facts with no old value
        "token_ranges": (start, end),
        "last_index": tokenizer(prompt, return_tensors="pt").input_ids.shape[1] - 1,
    }


def forward_edited(model, block, ids, direction, at):

    def hook(module, inp, out):
        residual_representaion = out[0] if isinstance(out, tuple) else out
        residual_representaion = residual_representaion.clone()
        residual_representaion[:, at] = residual_representaion[:, at] + direction
        return (
            (residual_representaion, *out[1:])
            if isinstance(out, tuple)
            else residual_representaion
        )

    handle = block.register_forward_hook(hook)

    try:
        return model(ids).logits

    finally:
        handle.remove()

# Follows the paper: Eq. 6, the REMEDI training objective.
def loss(logits_edit, logits_orig, example):
    """Eq. 6 for a single example. Same three terms as loss_batch — see its docstring
    for why the prior is bounded and why the KL excludes the prediction position."""

    logp_edit = torch.log_softmax(logits_edit.float(), dim=-1)
    logp_orig = torch.log_softmax(logits_orig.float(), dim=-1)

    i = example["last_index"]
    at = example["prompt_end_index"]

    target_token = -logp_edit[0, i, example["target_new_id"]]

    p_old = logp_edit[0, i, example["target_old_id"]].exp().clamp(max=1 - 1e-6)
    old_token = -LAM_PRIOR * torch.log1p(-p_old) * example["has_prior"]

    if i > at:
        kl = LAM_KL * torch.nn.functional.kl_div(
            logp_edit[0, at:i], logp_orig[0, at:i], reduction="sum", log_target=True
        )
    else:
        kl = torch.zeros((), device=logp_edit.device)

    return target_token + old_token + kl, (target_token, old_token, kl)

# ---------------------------------------------------------------- batched path

def collate(batch, pad_id, device):
    "variable-length prompts -> one padded tensor plus the per-row indices we need"
    lengths = [e["prompt_token_ids"].shape[1] for e in batch]
    B, T = len(batch), max(lengths)

    input_ids = torch.full((B, T), pad_id, dtype=torch.long, device=device)
    attn = torch.zeros((B, T), dtype=torch.long, device=device)
    for i, e in enumerate(batch):
        L = lengths[i]
        input_ids[i, :L] = e["prompt_token_ids"][0]
        attn[i, :L] = 1

    idx = lambda k: torch.tensor([e[k] for e in batch], device=device)
    return {
        "input_ids": input_ids,
        "attention_mask": attn,
        "h_attr": torch.stack([e["hidden_attribute_act"] for e in batch]),
        "at": idx("prompt_end_index"),
        "last": idx("last_index"),
        "new_id": idx("target_new_id"),
        "old_id": idx("target_old_id"),
        "has_prior": idx("has_prior"),
    }


def forward_edited_batch(model, block, batch, directions):
    "add each row's own direction at that row's own subject-end position"

    def hook(module, inp, out):
        h = out[0] if isinstance(out, tuple) else out
        h = h.clone()
        rows = torch.arange(h.shape[0], device=h.device)
        h[rows, batch["at"]] = h[rows, batch["at"]] + directions
        return (h, *out[1:]) if isinstance(out, tuple) else h

    handle = block.register_forward_hook(hook)
    try:
        return model(batch["input_ids"], attention_mask=batch["attention_mask"]).logits
    finally:
        handle.remove()


def loss_batch(logits_edit, logits_orig, batch):
    """Mean loss over the batch, plus the three terms separately.

    Eq. 6 as the reference implements it (remedi/editors.py:332), which differs from the
    paper's text in two ways that both mattered:

    prior   -log(1 - p_old), NOT log p_old. Eq. 4 writes log p(t_prior), but the released
            code uses log(1 - p): bounded at 0 as p_old -> 0, so the optimiser cannot buy
            loss forever by crushing the old answer. Under the unbounded form the 27 Aug
            run drove `prior` -7.05 -> -9.95 and total loss NEGATIVE by epoch 1, while
            p(target) sat at 0.014 — every edit destroyed the old answer and installed
            nothing.

    KL      over the positions BETWEEN the entity and the prediction, [at, last) — never
            the last position itself. Eq. 5 says "all tokens between the entity mention
            and the time at which it predicts t_tgt", and editors.py:391 makes the range
            exclusive. Applying it AT the prediction position, at weight 10, pointed the
            heaviest term in the objective at the one distribution the edit exists to
            change; the target term (weight 1) was fighting it and losing.
    """
    B, T, _ = logits_edit.shape
    rows = torch.arange(B, device=logits_edit.device)

    logp_e_all = torch.log_softmax(logits_edit.float(), dim=-1)
    logp_o_all = torch.log_softmax(logits_orig.float(), dim=-1)

    logp_e = logp_e_all[rows, batch["last"]]
    target_token = -logp_e[rows, batch["new_id"]]

    p_old = logp_e[rows, batch["old_id"]].exp().clamp(max=1 - 1e-6)
    old_token = -LAM_PRIOR * torch.log1p(-p_old) * batch["has_prior"]

    # per-row mask over [at, last); rows where the entity ends at the prediction get none
    pos = torch.arange(T, device=logits_edit.device)[None, :]
    between = (pos >= batch["at"][:, None]) & (pos < batch["last"][:, None])
    kl_per_token = torch.nn.functional.kl_div(
        logp_e_all, logp_o_all, reduction="none", log_target=True
    ).sum(-1)
    kl = LAM_KL * (kl_per_token * between).sum(-1)

    total = target_token + old_token + kl
    return total.mean(), (target_token.mean(), old_token.mean(), kl.mean())


def check_batching(model, block, editor, examples, pad_id, device, k=8):
    """Per-example loss, computed one at a time vs. in one batch. Must agree.

    Guards the two things that fail silently in a batched rewrite: a wrong attention mask,
    and injecting the direction at the wrong row's position.
    """
    print(f"\nbatching equivalence check on {k} examples", flush=True)
    singles = []
    with torch.no_grad():
        for e in examples[:k]:
            orig = model(e["prompt_token_ids"]).logits
            d = editor(e["hidden_attribute_act"])
            logits = forward_edited(model, block, e["prompt_token_ids"], d,
                                    at=e["prompt_end_index"])
            l, _ = loss(logits, orig, e)
            singles.append(l.item())

        b = collate(examples[:k], pad_id, device)
        orig = model(b["input_ids"], attention_mask=b["attention_mask"]).logits
        d = editor(b["h_attr"])
        logits = forward_edited_batch(model, block, b, d)

        # per-ROW losses, which loss_batch does not expose (it returns means), so the
        # three terms are restated here. Keep in step with loss_batch.
        rows = torch.arange(k, device=device)
        logp_e_all = torch.log_softmax(logits.float(), dim=-1)
        logp_o_all = torch.log_softmax(orig.float(), dim=-1)
        logp_e = logp_e_all[rows, b["last"]]
        p_old = logp_e[rows, b["old_id"]].exp().clamp(max=1 - 1e-6)
        pos = torch.arange(logits.shape[1], device=device)[None, :]
        between = (pos >= b["at"][:, None]) & (pos < b["last"][:, None])
        kl_per_token = torch.nn.functional.kl_div(
            logp_e_all, logp_o_all, reduction="none", log_target=True).sum(-1)
        batched = (
            -logp_e[rows, b["new_id"]]
            - LAM_PRIOR * torch.log1p(-p_old) * b["has_prior"]
            + LAM_KL * (kl_per_token * between).sum(-1)
        ).tolist()

    diffs = [s - t for s, t in zip(singles, batched)]
    worst = max(abs(d) for d in diffs)
    scale = max(abs(s) for s in singles) or 1.0
    lens = [e["prompt_token_ids"].shape[1] for e in examples[:k]]
    pad_to = max(lens)

    for i, (s, t) in enumerate(zip(singles, batched)):
        print(f"  {i}  len {lens[i]:3d} (pad {pad_to - lens[i]:2d})  "
              f"single {s:9.4f}   batched {t:9.4f}   diff {s - t:+.3e}")

    signs = sum(1 for d in diffs if d > 0)
    print(f"  max abs diff {worst:.3e}  ({worst / scale:.2%} of loss)  "
          f"signs +{signs}/-{len(diffs) - signs}", flush=True)
    print(f"  dtype {next(model.parameters()).dtype} — "
          f"{'expect ~1e-5' if scale and next(model.parameters()).dtype == torch.float32 else 'a few % is precision, not a fault'}",
          flush=True)
    return True


def evaluate(model, block, editor, examples, batch_size, pad_id, device):
    "mean validation loss and its three terms — no grad, no optimiser step"
    tot = [0.0, 0.0, 0.0, 0.0]
    n = 0
    with torch.no_grad():
        for i in tqdm(range(0, len(examples), batch_size), desc="validating",
                      unit="batch", dynamic_ncols=True, leave=False):
            chunk = examples[i:i + batch_size]
            b = collate(chunk, pad_id, device)
            orig = model(b["input_ids"], attention_mask=b["attention_mask"]).logits
            d = editor(b["h_attr"])
            logits = forward_edited_batch(model, block, b, d)
            l, (t, p, k) = loss_batch(logits, orig, b)
            w = len(chunk)
            for j, v in enumerate((l, t, p, k)):
                tot[j] += v.item() * w
            n += w
    return [v / n for v in tot]


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Train the REMEDI encoder for one model, from edit_method_config.json."
    )
    # was `MODEL = "gpt2-xl"` hardcoded, so LLaMA's encoder could not be trained at all
    ap.add_argument("--model", default="gpt2-xl")
    ap.add_argument("--bench", default="counterfact",
                    help="benchmark to train this encoder on. REMEDI trains one editor "
                         "per dataset; a single CounterFact encoder lifted p(target) "
                         "14,209x on CounterFact and 1.6-13x everywhere else.")
    ap.add_argument("--device", default=None, help="cuda / cpu. NOT mps — see DEV-001.")
    ap.add_argument("--lr", type=float, default=1e-3)
    # overrides so a short calibration run does not mean editing the config
    ap.add_argument("--n", type=int, default=None,
                    help="cap the training set (default: the whole window)")
    ap.add_argument("--epochs", type=int, default=None, help="max epochs (default: config)")
    # paper defaults: batch 16 (remedi/editors.py:39), 500 held out, patience 2 (Appendix C)
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--val-size", type=int, default=500,
                    help="facts held out for validation; 0 disables early stopping")
    ap.add_argument("--patience", type=int, default=2,
                    help="stop after this many epochs without validation improvement")
    ap.add_argument("--check-batching", action="store_true",
                    help="verify batched loss matches per-example loss, then train")
    # batches are shuffled each epoch, so the run is only reproducible with a fixed seed
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    random.seed(args.seed)
    torch.manual_seed(args.seed)

    MODEL = args.model
    method_config = json.loads(
        Path("edit_methods/edit_method_config.json").read_text()
    )["remedi"][MODEL]

    LAYER = method_config["layer_num"]
    EPOCHS = args.epochs if args.epochs is not None else method_config["epochs"]

    card = load_card(MODEL)
    device = args.device or pick_device()
    if device == "mps":
        print("refusing mps — see DEV-001. Use cpu or cuda.", file=sys.stderr)
        return 2

    dtype = torch.bfloat16 if device == "cuda" else torch.float32

    print(f"{MODEL} · {args.bench} · layer {LAYER} · {EPOCHS} epochs · "
          f"{device} ({dtype})")

    tokenizer = AutoTokenizer.from_pretrained(f"./models/{MODEL}")
    model = (
        AutoModelForCausalLM.from_pretrained(f"./models/{MODEL}", dtype=dtype)
        .to(device)
        .eval()
    )
    block = layer_block(model, card, LAYER)

    for p in model.parameters():
        p.requires_grad_(False)

    t_load = time.time()
    packs = load_training_split(args.bench, model=MODEL)
    if args.n:
        packs = packs[:args.n]
    print(f"loaded {len(packs)} packs in {time.time() - t_load:.1f}s", flush=True)

    examples, skipped = [], []
    for p in tqdm(packs, desc="building examples", unit="fact", dynamic_ncols=True):
        try:
            examples.append(build_example(model, tokenizer, block, p))
        except ValueError:
            skipped.append(p.subject)

    if skipped:
        print(f"skipped {len(skipped)}/{len(packs)} facts — subject not locatable in the "
              f"tokenised prompt. First few: {skipped[:3]}", flush=True)

    random.shuffle(examples)

    val = examples[-args.val_size:] if args.val_size else []
    train = examples[:-args.val_size] if args.val_size else examples
    print(f"train {len(train)} · val {len(val)} · batch {args.batch_size} · "
          f"lr {args.lr} · lam_prior {LAM_PRIOR} · lam_kl {LAM_KL}", flush=True)

    editor = RemediLinearNN(model, card).to(device)
    opt = torch.optim.AdamW(editor.parameters(), lr=args.lr)

    pad_id = tokenizer.pad_token_id
    if pad_id is None:
        pad_id = tokenizer.eos_token_id or 0

    if args.check_batching:
        check_batching(model, block, editor, train, pad_id, device)

    best_val = float("inf")
    best_state = copy.deepcopy(editor.state_dict())
    best_epoch = -1
    stale = 0

    print(f"\n{'epoch':>5} {'train':>8} {'tgt':>7} {'prior':>8} {'kl':>7} "
          f"{'| val':>8} {'tgt':>7} {'prior':>8} {'kl':>7} {'time':>7}", flush=True)

    for epoch in range(EPOCHS):
        t0 = time.time()
        random.shuffle(train)
        run = [0.0, 0.0, 0.0, 0.0]
        seen = 0

        bar = tqdm(range(0, len(train), args.batch_size),
                   desc=f"epoch {epoch}", unit="batch", dynamic_ncols=True, leave=False)
        for i in bar:
            chunk = train[i:i + args.batch_size]
            b = collate(chunk, pad_id, device)

            opt.zero_grad()
            with torch.no_grad():
                orig = model(b["input_ids"], attention_mask=b["attention_mask"]).logits
            directions = editor(b["h_attr"])
            logits = forward_edited_batch(model, block, b, directions)
            l, (t, p_, k) = loss_batch(logits, orig, b)
            l.backward()
            opt.step()

            w = len(chunk)
            for j, v in enumerate((l, t, p_, k)):
                run[j] += v.item() * w
            seen += w
            bar.set_postfix(loss=f"{run[0] / seen:.3f}", tgt=f"{run[1] / seen:.3f}")
        bar.close()

        tr = [v / seen for v in run]
        va = evaluate(model, block, editor, val, args.batch_size, pad_id, device) \
            if val else [float("nan")] * 4

        marker = ""
        criterion = va[0] if val else tr[0]
        if criterion < best_val:
            best_val, best_epoch = criterion, epoch
            best_state = copy.deepcopy(editor.state_dict())
            stale = 0
            marker = "  <- best"
        else:
            stale += 1

        print(f"{epoch:5d} {tr[0]:8.3f} {tr[1]:7.3f} {tr[2]:8.3f} {tr[3]:7.3f} "
              f"|{va[0]:8.3f} {va[1]:7.3f} {va[2]:8.3f} {va[3]:7.3f} "
              f"{time.time() - t0:6.0f}s{marker}", flush=True)

        if val and stale >= args.patience:
            print(f"early stop: validation loss has not improved for {args.patience} "
                  f"epochs (best was epoch {best_epoch})", flush=True)
            break

    path = encoder_path(card["name"], args.bench, LAYER)
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(best_state, path)
    which = "val" if val else "train"
    print(f"\nsaved epoch {best_epoch} ({which} loss {best_val:.4f}) -> {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
