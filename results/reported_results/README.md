# reported_results

The result set the report's tables and figures are built from. Not a run — a deterministic
splice of runs, rebuilt by `eval/reported.py`.

```bash
uv run python -m eval.reported          # rebuild cases.csv, manifest.json, table.md
uv run python -m eval.reported --check  # verify it is current; writes nothing
```

## The rule

Let $\mathcal{B}$ be the set of benchmarks and $\mathcal{D}_b(\rho)$ the probe-level record
set for benchmark $b$ in run $\rho$. Define a provenance map $\pi : \mathcal{B} \to \mathcal{P}$
assigning one source run to each benchmark. The reported record set is

$$\mathcal{R} \;=\; \bigcup_{b \,\in\, \mathcal{B}} \mathcal{D}_b\big(\pi(b)\big),
\qquad
\pi(b) \;=\;
\begin{cases}
\rho_{1} & b = \texttt{ripple} \\[2pt]
\rho_{0} & \text{otherwise}
\end{cases}$$

with $\rho_0$ = `EXP-023_m2-em6-b5_2026-09-05` (the full $n=95$ sweep over all five
benchmarks) and $\rho_1$ = `EXP-024_m2-em6-b1_2026-09-06` (RippleEdits alone, re-run with
Subject Aliasing exempted from the condition gate).

Because $\pi$ is a function, each benchmark has exactly one source, so $\mathcal{R}$ is well
defined and the construction is idempotent: rebuilding from unchanged inputs reproduces the
same bytes. Reported cells are then Eq. 7 of the report evaluated over $\mathcal{R}$,

$$\mathrm{Rate}(m,b,c) \;=\; \frac{1}{n_{b,c}} \sum_{j \,\in\, \mathcal{R}_{m,b,c}} \mathrm{score}_j$$

where $\mathcal{R}_{m,b,c}$ is the post-edit subset of $\mathcal{R}$ for method $m$,
benchmark $b$ and probe category $c$, and $\mathrm{score}_j$ is whichever of Eq. 4–6 that
benchmark's own paper specifies.

## Why blocks are replaced whole, never merged row by row

$\mathcal{D}_{\texttt{ripple}}(\rho_1)$ is a strict superset of
$\mathcal{D}_{\texttt{ripple}}(\rho_0)$ by key — nothing was dropped, 3804 aliasing rows were
added. But 122 of the 7956 rows present in both (1.53%) carry **different values**.

All 122 are generation-scored (`hit`), 102 of them on llama3-8b. `score_generation_batch`
left-pads and batches by 16, so changing which probes pass the gate changes the batch layout,
and greedy generation in bf16 is not bitwise stable across layouts. The differences run both
ways — 35 rows $0 \to 1$, 26 rows $1 \to 0$ — so this is drift, not a systematic shift.

Taking the whole block from one run keeps every reported RippleEdits cell attributable to a
single run and a single batch layout. A row-level merge would mix two layouts inside one
reported number with no principled way to choose per row.

## What the splice changes

Subject Aliasing in $\rho_0$ was scored on **one case**, on llama3-8b only:

| | $\rho_0$ (EXP-023) | $\rho_1$ (EXP-024) |
|---|---|---|
| aliasing cases, gpt2-xl | 0 | 159 |
| aliasing cases, llama3-8b | 1 | 159 |
| reported gpt2-xl row | *absent* | 38.3 / 18.9 / 44.5 / 14.8 / 25.4 / 1.9 |
| reported llama3-8b row | 100.0 across every method, sd 0 | 62.4 / 32.1 / 17.7 / 58.4 / 20.0 / 12.8 |

The pre-splice row is an artefact of $n=1$, not a result. Every other benchmark is unaffected.

## Adding a future re-run

Change the value in `PROVENANCE` in `eval/reported.py` and rebuild. The script refuses to
build if the source runs disagree on `quantity` or `sample_seed` — the table caption states
one $n$ and one seed for the whole table, so a mismatch would make that caption false — and
refuses if the splice produces a duplicate key.

## Files

| File | What |
|---|---|
| `cases.csv` | 117,420 spliced probe-level rows, sorted by key |
| `manifest.json` | the provenance map, source git SHAs, $n$, seed |
| `table.md` | both models' tables, formatted by `eval.csv_to_md` unchanged |
