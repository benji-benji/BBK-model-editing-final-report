"""REMEDI - editing by adding a learned attribute direction to a hidden state.

Follows the method described in Hernandez, E., Li, B.Z. and Andreas, J. (2024)
'Inspecting and editing knowledge representations in language models', Conference
on Language Modeling (COLM). arXiv:2304.00740. Reference implementation:
https://github.com/evandez/remedi (MIT; licence text reproduced in THIRD_PARTY_LICENSES.md).

Follows the paper: `RemediLinearNN` is the encoder F(h) = Wh + b whose output is
added into the entity's hidden state, and the injection point (last subject token)
matches the reference.

Author's own: this is the least derived of the six. The hook machinery
(`add_updated_activation`), id-space subject matching (`subject_end_in_ids`),
`hidden_at`, per-benchmark encoder caching and `remedi_edit` are all written for
this harness.
"""

from pathlib import Path

import torch
import torch.nn as nn


from utils.edit_utils import get_subject_token_range
from utils.model_state import resolve
from utils.remedi_training import encoder_path

# Follows the paper: the encoder whose output is added into the hidden state.
class RemediLinearNN(nn.Module):
    def __init__(
        self,
        model,
        card
        ):
        # self.model = model
        super().__init__()    
        hidden_size = card['model_dim']
        input_size = hidden_size 
        self.w = nn.Linear(input_size, hidden_size)
    
    def forward(
        self,
        attribute: torch.Tensor,
    ) -> torch.Tensor:

        direction = self.w(attribute.to(self.w.weight.dtype))
        return direction.to(attribute.dtype)

def hidden_at(model,
              tokenizer,
              text,
              block, # transformer block
              span=None):

    ids = tokenizer(text, return_tensors="pt").input_ids.to(model.device)
    output = {}
    hook = block.register_forward_hook(lambda m, i, o: output.update(h=o[0] if isinstance(o, tuple) else o))
    with torch.no_grad():
        model(ids)
    hook.remove()
    hidden_activation = output["h"][0]
    return hidden_activation[span[0]:span[1]].mean(0) if span else hidden_activation[-1]



def remedi_edit(method,
                model,
                tokenizer,
                edit_datas
                ):
    card, method_config = method.card, method.config
    layer = method_config["layer_num"]
    block = resolve(model, card["layer_tmpl"].format(layer))

   
    bench = edit_datas[0].benchmark
    if bench not in getattr(method, "editors", {}):
        editor = RemediLinearNN(model, card).to(model.device)
        editor.load_state_dict(
            torch.load(encoder_path(card["name"], bench, layer), map_location="cpu"))
        editor.eval()
        method.editors = {**getattr(method, "editors", {}), bench: editor}
    method.editor = method.editors[bench]

   
    handles = []
    for case in edit_datas:
        prompt = case.construct_prompt()
        context = f"{prompt} {case.target_new}"
        _, end = get_subject_token_range(prompt, case.subject, tokenizer)
        h_attr = hidden_at(model, tokenizer, context, block, span=(end, None))

        with torch.no_grad():
            direction = method.editor(h_attr)

        handles += add_updated_activation(model, block, direction, tokenizer, case.subject)

    method.handle = handles

    return None

def subject_end_in_ids(ids, entity, tokenizer):

    ids = ids.tolist()
    for candidate in (entity, " " + entity):
        sub = tokenizer.encode(candidate, add_special_tokens=False)
        for i in range(len(ids) - len(sub) + 1):
            if ids[i:i + len(sub)] == sub:
                return i + len(sub)
    raise ValueError(f"entity {entity!r} not found in tokenised prompt")


def add_updated_activation(model, block, direction, tokenizer, entity):
    seen = {}
  
    pre = model.register_forward_pre_hook(
        lambda m, args, kwargs: seen.update(
            ids=kwargs["input_ids"] if "input_ids" in kwargs else args[0]
        ),
        with_kwargs=True,
    )

    def edit(module, inp, out):
        h = out[0] if isinstance(out, tuple) else out
        if h.shape[1] == 1:            # generating past the prompt — don't edit
            return out
        
        try:
            ent_end = subject_end_in_ids(seen["ids"][0], entity, tokenizer)
        except ValueError:
            return out                 # entity not in this prompt — nothing to edit
        i = ent_end - 1

        if i >= h.shape[1]:
            return out

        h = h.clone()                  # not in-place — see DEV-001
        h[:, i] = h[:, i] + direction
        return (h, *out[1:]) if isinstance(out, tuple) else h

    return [pre, block.register_forward_hook(edit)]