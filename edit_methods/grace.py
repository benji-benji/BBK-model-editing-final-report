"""GRACE - lifelong model editing with a discrete key-value codebook.

Adapted from the reference implementation at https://github.com/thartvigsen/GRACE.
That repository publishes NO LICENCE, so none is reproduced for it; the code is used
for non-commercial academic research and private study with acknowledgement. See
THIRD_PARTY_LICENSES.md before publishing or redistributing this repository.

Paper: Hartvigsen, T., Sankaranarayanan, S., Palangi, H., Kim, Y. and Ghassemi, M.
(2023) 'Aging with GRACE: lifelong model editing with discrete key-value adaptors',
NeurIPS. arXiv:2211.11031.

This is the most closely derived of the six files. Follows the reference:
`brackets_to_periods`, `parent_module`, the `GRACE` wrapper, and the `GRACEAdaptor`
codebook methods `add_key`, `init_key_value`, `label_match` and
`split_epsilons_in_half`, together with the codebook-search branch of `forward`.

Author's own: `make_edit_tokens`, `snapshot`, `predict`, `_grace_edit_one`,
`grace_edit`, `teardown`, and the two retrieval corrections in `forward` - querying
every position rather than one, and writing the retrieved value at the matched
position rather than before it.
"""

import torch
import torch.nn as nn
import transformers
import torch.nn.functional as F


# Verbatim from the reference implementation, but for the fp32 cast.
def euclidean_distance(query, key):
    if len(key.shape) < 2:
        key = key.view(1, -1)
    return torch.cdist(key.float(), query.float(), p=2)

# Verbatim from the reference implementation (grace/utils.py).
def brackets_to_periods(name: str) -> str:
    return name.replace("[", ".").replace("]", "")

# Verbatim from the reference implementation (grace/utils.py).
def parent_module(model, pname: str):
    components = pname.split('.')
    parent = model
    for component in components[:-1]:
        if hasattr(parent, component):
            parent = getattr(parent, component)
        elif component.isdigit():
            parent = parent[int(component)]
        else:
            raise RuntimeError(f"Couldn't find child module {component}")
    if not hasattr(parent, components[-1]):
        raise RuntimeError(f"Couldn't find child module {components[-1]}")
    return parent


def predict(model, tokenizer, prompt):
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(DEVICE)
    with torch.no_grad():
        logits = model(input_ids).logits
    probs = F.softmax(logits[0, -1].float(), dim=-1)
    top_id = probs.argmax().item()
    return {
        "top_token": tokenizer.decode(top_id),
        "top_prob": probs[top_id].item(),
        "probs": probs,
    }


def make_edit_tokens(prompt, target, tokenizer, device):
    """GRACE tokens: prompt tokens masked (-100), target tokens kept."""
    full = f"{prompt} {target}"
    prompt_ids = tokenizer(prompt, return_tensors="pt")["input_ids"]
    full_enc = tokenizer(full, return_tensors="pt")
    input_ids = full_enc["input_ids"].to(device)
    labels = input_ids.clone()
    labels[:, : prompt_ids.shape[1]] = -100
    return {"input_ids": input_ids, "labels": labels}


def snapshot(model, tokenizer, prompt, target_old, target_new):
    """Return top prediction + P(old) + P(new) for one prompt."""
    res = predict(model, tokenizer, prompt)
    old_id = tokenizer.encode(target_old)[0]
    new_id = tokenizer.encode(target_new)[0]
    return {
        "top_token": res["top_token"],
        "top_prob": res["top_prob"],
        "p_old": res["probs"][old_id].item(),
        "p_new": res["probs"][new_id].item(),
    }


def _grace_edit_one(grace, tokens, n_iter):
    """Run one fact's edit loop with a configurable iteration count."""
    adapter = grace._get_adapter()
    adapter.training = True
    adapter.edit_label = tokens["labels"]
 
    adapter.key_id = (tokens["labels"] == -100).sum().item() - 1
    optimizer = None
    for i in range(n_iter):
        adapter.iter = i
        outputs = grace.model(**tokens)
        if i == 0:
            optimizer = torch.optim.Adam(grace.model.parameters(), grace.learning_rate)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
    adapter.training = False
    adapter.key_id = -1


def grace_edit(method, model, tokenizer, edit_datas):
    """
    Wrap `model` with GRACE and run sequential edits in place.
    Weights are not modified; the codebook grows by one per edit.
    Returns None for drift (GRACE has no weight delta).
    """
    config = method.config
    
    device = next(model.parameters()).device
        
    layer = method.card["mlp_proj_tmpl"].format(config["layer_num"])
    method.grace = GRACE(model, layer, config["init_epsilon"], config["learning_rate"], device)
    
    for i, f in enumerate(edit_datas):
        tokens = make_edit_tokens(f.construct_prompt(), f.target_new, tokenizer, device)
        print(f"\n[{i}] editing: {f.construct_prompt()!r} -> {f.target_new!r}")
        _grace_edit_one(method.grace, tokens, config["n_iter"])
        adapter = method.grace._get_adapter()
        print(f"    codebook size: {len(adapter.keys)}")
    
    return None

# Follows the reference implementation's wrapper class. `teardown` is the author's,
# added so the harness can restore the unedited model between cases.
class GRACE(torch.nn.Module):
    def __init__(
        self, 
        model, 
        layer, 
        init_epsilon, 
        learning_rate, 
        device, 
        generation=False,
        ):
        super(GRACE, self).__init__()
        self.log_dict = {}
        self.generation = generation
        self.learning_rate = learning_rate
        self.model = model
        
        suffixes = [".weight", ".bias"]
        self.layer = layer.rsplit(".", 1)[0] if any(layer.endswith(x) for x in suffixes) else layer
        
        for n, p in self.model.named_parameters():
            p.requires_grad = False

        
        if isinstance(self.model, transformers.models.gpt2.modeling_gpt2.GPT2LMHeadModel):
            transpose = False 
        else:
            transpose = True
            
        # --- Add GRACE to chosen layers ---
        edit_module = parent_module(self.model, brackets_to_periods(self.layer))
        layer_name = self.layer.rsplit(".", 1)[-1]
        original_layer = getattr(edit_module, layer_name)
        self._original = original_layer
        setattr(edit_module, layer_name, GRACEAdaptor(original_layer, init_epsilon, device, transpose).to(device))
        

    def _get_adapter(self):
        edit_module = parent_module(self.model, brackets_to_periods(self.layer))
        layer_name = self.layer.rsplit(".", 1)[-1]
        return getattr(edit_module, layer_name)

    
    def edit(self, tokens):
        adapter = self._get_adapter()
        adapter.training = True
        adapter.edit_label = tokens["labels"]

        for i in range(200):
            adapter.iter = i
            outputs = self.model(**tokens)
            if i == 0:
                optimizer = torch.optim.Adam(self.model.parameters(), self.learning_rate)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

        adapter.training = False
        self.chosen_key = adapter.chosen_key
        self.nkeys = len(adapter.keys)
        self.epsilons = len(adapter.epsilons)
        
    def teardown(self):
        """Remove GRACE from the model and restore original layer."""
        edit_module = parent_module(self.model, brackets_to_periods(self.layer))
        layer_name = self.layer.rsplit(".", 1)[-1]
        setattr(edit_module, layer_name, self._original)



# Follows the reference implementation's adaptor. The codebook methods below
# (add_key, init_key_value, label_match, split_epsilons_in_half) are near-identical,
# including their comments; the two retrieval corrections in `forward` are the author's.
class GRACEAdaptor(torch.nn.Module):
    def __init__(
        self,
        layer: nn.Module,
        init_epsilon: float,
        device: str,
        transpose: bool = True,
    ):
        super(GRACEAdaptor, self).__init__()
        self.layer = layer
        self.init_epsilon = init_epsilon
        self.device = device
        self.key_id = -1       # which token position to use as query (default: last)
        self.training = False  # controls codebook modification vs pure retrieval
        

        if transpose == True:
            self.key_shape = layer.weight.shape[1]
            self.value_shape = layer.weight.shape[0]
        else:
            self.key_shape = layer.weight.shape[0]
            self.value_shape = layer.weight.shape[1]
    
    def add_key(self, new_key, new_value):
        keys = torch.vstack([self.keys, new_key.detach()]) # Add new key to list of keys

        values = torch.nn.Parameter(torch.vstack([self.values, new_value]), requires_grad=True) # Add new value to list of values

        new_epsilon = torch.tensor(self.init_epsilon, device=self.device).view(1)
        epsilons = torch.vstack([self.epsilons, new_epsilon]) # Add new epsilon to list of epsilons

        key_labels = self.key_labels + [self.edit_label] # Add new key_label to list of key_labels

        return keys, values, epsilons, key_labels
    
    def init_key_value(self, query, value):
        key = query.detach()
        value = value
        epsilon = torch.tensor(self.init_epsilon, device=self.device, requires_grad=False).view(1)
        key_label = [self.edit_label]
        return key, value, epsilon, key_label
            
    def label_match(self, edit_label, key_label):
        return edit_label.float().mean() == key_label.float().mean()

    def split_epsilons_in_half(self, nearest_key, smallest_distance):
        self.epsilons[nearest_key] = (smallest_distance / 2) - 1e-5 # Cut nearest epsilon in half
        self.epsilons[-1] = smallest_distance / 2 # Cut new epsilon in half
            
            
    def forward(self, *args):
        # Run layer forward and save what it would have returned for this instance
        layer_out = self.layer(*args)

        ### If training, we need to modify the codebook
        if (not self.training) & ('keys' not in self.__dict__):
            # If it's not training time and we haven't added any keys yet (this is before doing any editing)
            return layer_out
        else:
                token_to_edit = min(self.key_id, args[0].shape[1]-1)
                query = args[0][:, token_to_edit, :] # Just use activation for last token
                new_value = torch.nn.Parameter(torch.rand(1, self.value_shape, requires_grad=True, device=self.device))

                if 'keys' not in self.__dict__:
                    # If no keys exist, initialize keys, values, epsilons, and key labels
                    self.keys, self.values, self.epsilons, self.key_labels = self.init_key_value(query, new_value)
                
                elif self.iter == 0:
                    # Keys exist, so we have decide whether or not to update them (the fact that we've made it to this point means there was an error!)

                    # --- search through keys for a match for query ---
                    dists = torch.stack([euclidean_distance(query, key).view(-1, 1) for key in self.keys]).view(-1, len(query))

                    smallest_distance, nearest_key = dists.min(0)

                    if smallest_distance > (self.init_epsilon + self.epsilons[nearest_key]):
                        # If there's no close key, make a new key                    
                        self.keys, self.values, self.epsilons, self.key_labels = self.add_key(query, new_value)
                    else:
                        # If there is a close key, we need to handle conflicts
                        if not self.label_match(self.edit_label, self.key_labels[nearest_key]):
                            self.keys, self.values, self.epsilons, self.key_labels = self.add_key(query, new_value)
                            self.split_epsilons_in_half(nearest_key, smallest_distance)
                        else:
                            # If the current label is the SAME as the nearest label, just make the nearest epsilon bigger
                            if smallest_distance > self.epsilons[nearest_key]:
                                    self.epsilons[nearest_key] = smallest_distance # Replace nearest epsilon with dist between old key and new key
                else:
                    # If not iter 0, we don't need to change keys, we just need to learn the value
                    pass

        b, seq_len, _ = args[0].shape
        queries = args[0].reshape(b * seq_len, -1)

        dists = torch.stack(
            [euclidean_distance(queries, key).view(-1, 1) for key in self.keys]
        ).view(-1, b * seq_len)
        smallest_dist, self.chosen_key = dists.min(0)
        chosen_value = self.values[self.chosen_key]
        eps = self.epsilons[self.chosen_key].view(-1, 1)
        hit = smallest_dist.view(-1, 1) <= eps

        patched = torch.where(
            hit,
            chosen_value.to(layer_out.dtype),
            layer_out.reshape(b * seq_len, -1),
        )
        return patched.view(layer_out.shape)
