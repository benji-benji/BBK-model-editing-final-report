"""AnyEdit - chunked sequential editing of long-form targets.

Adapted from the reference implementation at https://github.com/jianghoucheng/AnyEdit
(MIT; licence text reproduced in THIRD_PARTY_LICENSES.md). Paper: Jiang, H., Fang, J., Zhang, N., Ma, G.,
Wan, M., Wang, X., He, X. and Chua, T.-S. (2025) 'AnyEdit: edit any knowledge
encoded in language models'. arXiv:2502.05628.

Follows the reference: the decomposition of a long target into chunks and the
autoregressive carry-forward of each edited chunk into the next context.

Author's own: `anyedit_edit`, which drives the loop through this harness's
`Edit_Eval_Pack` and delegates each chunk to `memit_edit`.
"""

from benches.load_benchmarks import Edit_Eval_Pack
from edit_methods.memit import memit_edit


# Follows the reference: fixed-window decomposition of a long target.
def chunk_target(target_ids, window_size, overlap=0):
    chunks, start, step = [], 0, window_size - overlap
    while start < len(target_ids):
        end = min(start + window_size, len(target_ids))
        chunks.append(target_ids[start:end])
        start += step
    return chunks


def anyedit_edit(
    method,
    model,
    tokenizer,
    edit_datas,
    anyedit: bool = True,
    cov_path: str = None,
    window_size: int = 512,
    overlap: int = 0,
):
    for fact in edit_datas:
        print(fact)
        print(type(fact))

        target_ids = tokenizer(fact.target_new, add_special_tokens=False)["input_ids"]

        chunks = chunk_target(target_ids, window_size, overlap)
        context = fact.prompt  # X
        for chunk in chunks:
            chunk_text = tokenizer.decode(chunk)
            subfact = Edit_Eval_Pack(
                case_id=fact.case_id,
                benchmark=fact.benchmark,
                prompt=context,
                target_new=chunk_text,
                subject=fact.subject,
                target_old=fact.target_old,
            )
            memit_edit(
                method,
                model,
                tokenizer,
                [subfact],
                anyedit=True,
                cov_path=method.covariances_path,
            )
            context = context + chunk_text  # carry chunk forward
