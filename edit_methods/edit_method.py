from edit_methods.rome import rome_edit
from edit_methods.memit import memit_edit
from edit_methods.grace import grace_edit
from edit_methods.alphaedit import alphaedit_edit
from edit_methods.anyedit import anyedit_edit
from edit_methods.remedi import remedi_edit

class EditMethod:
    def __init__(self, name, model, card, config, covariances_path):
        self.name = name
        self.model = model
        self.card = card
        self.config = config
        self.covariances_path = covariances_path
        self.covariance_regularization = 1e-4
        self.layer = config["layer_num"]
        self.grace = None
        self.handle = None

    def run_edits(self, name, model, tokenizer, edit_datas):
        "using the name of the edit method, call the correct edit function and return the drift"
        if name == "rome":
            return rome_edit(self, model, tokenizer, edit_datas)
        if name == "memit":
            return memit_edit(self, model, tokenizer, edit_datas, cov_path=self.covariances_path)
        if name == "grace":
            return grace_edit(self, model, tokenizer, edit_datas)
        if name == "anyedit":
            return anyedit_edit(self, model, tokenizer, edit_datas, anyedit=True, cov_path=self.covariances_path, window_size=512, overlap=0)
        if name == "alphaedit":
            return alphaedit_edit(self, model, tokenizer, edit_datas)
        if name == "remedi":
            return remedi_edit(self, model, tokenizer, edit_datas)
        else:
            raise ValueError(f"Unknown edit method: {name}")
        
    def teardown(self):
        "teardown the edit method, if applicable"
        if self.name == "grace" and self.grace is not None:
            self.grace.teardown()
        if self.name == "remedi" and self.handle is not None:
            for handle in self.handle:
                handle.remove()
            self.handle = None