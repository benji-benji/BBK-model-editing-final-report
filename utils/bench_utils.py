import random

def select(raw, quantity, seed=None, exclude=None, restrict=None):
    """
    Function to select a subset of records from benchmark
    dataset, according the specified quantity, seed, exclude and restrict parameters.

    """
    pairs = list(enumerate(raw))

    if restrict:
        lo, hi = restrict
        pairs = [(i, r) for i, r in pairs if lo <= i < hi]
    elif exclude:
        lo, hi = exclude
        pairs = [(i, r) for i, r in pairs if not (lo <= i < hi)]

    if seed is not None:
        random.Random(seed).shuffle(pairs)

    return pairs[:quantity] if quantity is not None else pairs
