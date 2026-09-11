"""`Edit_Eval_Pack` - one fact edit and all the probes attached to it.

Author's own. This is the harness's universal adaptor between benchmarks and edit methods:
every `load_*` function maps its benchmark's native field names onto this shape, so the
edit methods never see a benchmark-specific structure.
"""

class Edit_Eval_Pack:
    # eval probe categories
    EFFICACY = "efficacy"
    GENERALISATION = "generalisation"
    SPECIFICITY = "specificity"
    RIPPLE_LOGICAL = "ripple_logical"
    RIPPLE_COMPOSITIONAL = "ripple_compositional"
    RIPPLE_COMPOSITIONAL_I = "ripple_compositional_i"
    RIPPLE_COMPOSITIONAL_II = "ripple_compositional_ii"
    RIPPLE_ALIASING = "ripple_aliasing"
    RIPPLE_PRESERVATION = "ripple_preservation"
    RIPPLE_RELATION_SPECIFICITY = "ripple_relation_specificity"
    SINGLE_HOP = "single_hop"
    MULTIHOP = "multihop"
    GENIE_GENERATION_ONLY = ("abstract_2", "abstract_3")

    FREEFORM_PROMPT = "freeform_prompt"
    TARGET_CLOSE_NEIGHBOUR = "target_close_neighbour"

    def __init__(
        self,
        case_id,
        benchmark,
        prompt,
        target_new,
        subject=None,
        target_old=None,
        probe_list=None,
        meta=None,
        case_number=None,
    ):
        self.case_id = case_id
        self.case_number = case_number
        self.benchmark = benchmark
        self.prompt = prompt
        self.target_new = target_new
        self.subject = subject
        self.target_old = target_old
        self.probe_list = list(probe_list) if probe_list else []
        self.meta = dict(meta) if meta else {}

    def construct_prompt(self):
        """returns the prompt with the subject substituted in."""
        if self.subject is not None and "{}" in self.prompt:
            return self.prompt.format(self.subject)
        return self.prompt

    def collect_probes(
        self, probe_category, prompt, ground_truth=None, tests=None, meta=None
    ):
        """Append one probe. Returns self so calls can be chained by a loader."""
        self.probe_list.append(
            {
                "category": probe_category,
                "prompt": prompt,
                "ground_truth": ground_truth,
                "meta": meta or {},
            }
        )
        return self

    def __repr__(self):
        return (
            f"Edit_Eval_Pack(case_id={self.case_id!r}, benchmark={self.benchmark!r}, "
            f"prompt={self.prompt!r}, subject={self.subject!r}, "
            f"target_new={self.target_new!r},target_old={self.target_old!r}, "
            f"probes={len(self.probe_list)})"
        )

    def __eq__(self, other):
        if not isinstance(other, Edit_Eval_Pack):
            return NotImplemented
        return (
            self.case_id,
            self.benchmark,
            self.prompt,
            self.target_new,
            self.subject,
            self.target_old,
            self.probe_list,
        ) == (
            other.case_id,
            other.benchmark,
            other.prompt,
            other.target_new,
            other.subject,
            other.target_old,
            other.probe_list,
        )
