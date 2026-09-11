# Model Editing: Capacities and Limits

Code for an MSc Data Science final project at Birkbeck, University of London.

This repository implements six editing methods from scratch and runs
them under one evaluation harness across four published benchmarks plus a custom
benchmark Genie, on GPT-2-XL and LLaMA-3-8B. Contains steps to build Genie from scratch. 

---

## Requirements

- Python **3.13+**
- [uv](https://docs.astral.sh/uv/) for dependency management
- A CUDA GPU for anything at scale. Edits run on CPU locally and CUDA remotely —
  **never MPS**: in-place hook injection during the z-optimisation intermittently drops
  the gradient on Apple Silicon, which stalls the optimisation and silently produces a
  failed edit.

```bash
git clone git@github.com:benji-benji/BBK-model-editing-final-report.git
cd BBK-model-editing-final-report
uv sync
```

## Set up overview 

Harness Prerequisite steps
1. Download model weights
2. Download published benchmarks 
3. Compute Covariances for each model 
4. Compute nullspace Projections for Alphaedit 
5. Train the REMEDI encoder for each benchmark

Genie Benchmark Prerequisite steps 
1. Collect the seed people from Wikipedia page views
2. Collect the seed works from Wikidata 
3. Build the object table 
4. Generate genie.json from the table
5. Filter the genie.json file per model 

Preq checklist:
- Models: models/gpt2-xl/ and models/llama3-8b/ each contain weights.
- Benchmarks: data/raw/ has CounterFact, ZsRE, RippleEdits and MQuAKE.
- Genie.json: data/raw/genie/genie.json exists.
- Artifacts: covariances and projections exist for each model in artifacts/, and encoders in models/encoders/.
- Auths for relevent platforms: Github, Run Pod, API keys 

Running Harness steps 
1. Select the models, methods, benchmarks, quantity and seed in harness_config.json.
2. Run the harness from the repository root.
3. Check every cell reports a restore drift of zero and that all cells completed.
4. Run the evaluation pipeline on the new results directory.

## Running the harness

The harness takes no command-line arguments. It reads `harness_config.json`, by relative
path at import time, so run it from the repository root.

```json
{
  "models":     {"gpt2-xl": true, "llama3-8b": false},
  "methods":    {"rome": true, "memit": false, "grace": false,
                 "alphaedit": false, "anyedit": false, "remedi": false},
  "benchmarks": {"counterfact": true, "zsre": false, "ripple": false,
                 "mquake": false, "genie": false},
  "quantity":   1,
  "seed":       0
}
```

Every `true` combination is one cell. `quantity` is the number of edited facts per cell.
`seed` selects which facts: a seeded shuffle of the source file, recorded in the run
manifest. Omit it and the harness defaults to `0` rather than silently reverting to "first
n in file order".

```bash
uv run python harness.py
```

For each fact the harness snapshots the edit band, scores every probe pre-edit, applies
the edit, scores every probe again, tears the method down, restores the weights, and
reports the maximum drift between the restored and original weights. A drift of `0.0`
means the restore was exact — check it before trusting any number, because a method that
does not fully tear down contaminates every subsequent case.

Each invocation gets a fresh, never-reused directory:

```
results/EXP-004_m1-em6-b2_2026-09-01/
├── manifest.json                     config, git sha, device, seed
├── failures.json                     cells that raised, if any
└── <model>/<method>/<benchmark>/
    ├── pre_edit.json                 {case_id: [probe, ...]}
    └── post_edit.json
```

A cell that raises is recorded and skipped, not fatal — the weights are restored in a
`finally`, so a mid-edit failure cannot contaminate later cells. The exit code is non-zero
if any cell failed, so a sweep that lost cells cannot be mistaken for a clean one.

## Prerequisite steps

Large or slow assets are not tracked. Before a first run:

| Step | Command | Produces |
|---|---|---|
| Model weights | `uv run python -m scripts.download_models` | `models/<name>/*.safetensors` |
| Benchmark data | `uv run python -m scripts.download_benchmarks` | `data/raw/<bench>/` |
| Key covariances | `uv run python -m scripts.compute_covariances` | `artifacts/covariances/<model>/c_layer_<n>.pt` |
| AlphaEdit projections | `uv run python -m scripts.compute_projections` | `artifacts/projections/<model>/p_layer_<n>.pt` |
| REMEDI encoder | `uv run python -m scripts.train_encoder` | `models/encoders/<model>/layer_<n>.pt` |

## Edit Methods 

| Family | Method | Mechanism |
|---|---|---|
| Locate-and-edit | ROME | rank-one update to one MLP projection |
| | MEMIT | spread across a band of layers |
| | AnyEdit | autoregressive chunking over MEMIT, for long targets |
| | AlphaEdit | MEMIT with ΔW projected onto the null space of preserved knowledge |
| Memory-based | GRACE | routes around the model; no weight change |
| Representation-based | REMEDI | adds a learned direction to the residual stream |

Each is a module in `edit_methods/`, registered through the `EditMethod` class, with
per-model hyperparameters in `edit_methods/edit_method_config.json`.

**Model cards** (`models/<name>/card.json`) hold everything architecture-specific: module
path templates, the edit band, covariance scaling, weight orientation, and the
tokenisation convention. A method reads the card rather than branching on model name, so
adding a model is a config change.

## Benchmarks

| Benchmark | Source | Tests |
|---|---|---|
| CounterFact | Meng et al. 2022 | efficacy, paraphrase, neighbourhood specificity |
| ZsRE | Levy et al. 2017 | question-form generalisation |
| RippleEdits | Cohen et al. 2023 | logical consequences of an edit |
| MQuAKE | Zhong et al. 2023 | multi-hop reasoning over edited chains — use `MQuAKE-CF-3k-v2`; the original 3k file has a known knowledge-conflict bug |
| **Genie** | this project | how far one edit reaches: paraphrase, hops, abstraction |

Every loader in `benches/load_benchmarks.py` converts its benchmark's own JSON shape into
one canonical `Edit_Eval_Pack`, so scoring and the harness loop never branch on benchmark.

### Genie

One edited fact `(s, r, o → o′)` probed at four distances from the edit, up to ten probes
per fact, ragged — a probe is emitted only where its data exists and is scored against its
own denominator.

```
efficacy      the edit prompt itself, as a control
paraphrase    same fact reworded                       paraphrase_1  _2  _3
hop           one, two, three steps past the object    hop_1  hop_2  hop_3
abstraction   comparison · named paragraph · unnamed paragraph
              abstract_1     abstract_2       abstract_3
```

`abstract_3` names no subject at all — the test is whether the edit propagated far enough
that the model reaches the edited entity unprompted while writing about a class containing
it. *"films from 1961 are often remembered for their production. One example"* is hundreds
of films, and it scored 0.000 in all twelve cells of EXP-003. It is now narrowed by an
**associated person drawn from a relation other than the one being edited**:

```
edit:  Breakfast at Tiffany's — director: Blake Edwards -> Wes Craven
probe: "Henry Mancini films from 1961 are often remembered for their production. One example"
```

Narrowing by the *edited* relation would name the thing under test, so the exclusion is the
point: edit the composer and it narrows by the director, and vice versa. 69% of `abstract_3`
probes carry a person; the rest fall back to the year-only form, and `meta["constraints"]`
records which fired. A prominence gate drops subjects below 31 Wikidata sitelinks, on the
grounds that an obscure subject will never be named however the class is phrased.
`abstract_2` carries the person too, which makes that rung easier and not comparable to
pre-2 Sep numbers.

`tests/genie_check_abstract.py` asserts the emitted prompt for each branch from handcrafted
rows — no table, no model, seconds to run.

Built from Wikidata. The design idea is to **validate objects, not facts**: chain
completeness, hop collision and comparator availability are properties of the ~30 objects
a relation admits, not of the thousands of subjects carrying it, so the object table is
built and validated once and facts inherit validity by construction.

Steps to build GENIE from scratch: 

```bash
uv run python -m genie_bench.ripple_get_most_viewed   # seed people, from pageviews (cached)
uv run python -m genie_bench.scripts.genie_generate_entities  # seed works, from SPARQL (cached)
uv run python -m genie_bench.scripts.genie_build_table        # -> artifacts/bench_generation/genie_table.json
uv run python -m genie_bench.scripts.genie_full_generation    # -> data/raw/genie/genie.json
```

Steps 1–3 are network-bound; a GPU does nothing for them. All subjects are pre-2018,
since GPT-2-XL's training data stops in December 2017.

## Evaluation

The harness only writes artifacts. Every reported number is derived downstream from those
artifacts alone, in stages, so a mistake in the analysis never touches the run.

```
<run>/…/{pre,post}_edit.json
  └── eval/results_to_csv.py    -> cases.csv    one row per model × method × bench × case
        ├── eval/csv_to_heatgrid.py  -> heatmap_<model>.png
        └── eval/csv_to_md.py        -> table.md   pandoc table for the report
```

```bash
uv run python -m eval.run_eval                          # newest run
uv run python -m eval.run_eval --run EXP-018_m2-em6-b4_2026-09-02
```

`run_eval` chains the three stages; each is also runnable alone with a run directory name.

**Scoring.** `eval/score.py` teacher-forces each candidate answer after the probe prompt
and returns the geometric-mean per-token probability, `exp(mean log p)` — length-normalised
so a multi-token answer is not crushed by its own length. Two per probe: `p_new` for the
edited target, `p_old` for the answer that should hold if the edit had not been made. On
locality probes `p_old` comes from the probe's own `ground_truth`, because those prompts
are about a different subject entirely.

**Each benchmark is scored the way its own paper scores it**, not with one metric across all
five. Forcing a single metric onto them produced numbers that looked comparable and were not.

| benchmark | metric | source |
|---|---|---|
| CounterFact | probability comparison, `p_new` vs `p_old` | `eval_utils_counterfact.py` — parity with the reference verified, see below |
| zsRE | per-token argmax accuracy | `eval_utils_zsre.py` returns match flags and no probabilities |
| RippleEdits | generation + containment, 20 tokens | Cohen et al. 2023 §5.1 |
| MQuAKE | containment (`multihop`), accuracy (`single_hop`) | Zhong et al. 2023 |
| Genie | probability, except the free-text rungs | this project |

`p_new` / `p_old` are **not** reported for RippleEdits or MQuAKE multihop: those papers use
no probability metric, and their probes carry only the post-edit expected answer, so there is
no source for `p_old` at all.

**Four measures**, all computed per case and then averaged across cases — matching
`summarize.py`'s aggregation order. A measure is simply absent where a benchmark does not
produce it.

| | Definition |
|---|---|
| `success` | share of probes where `p_new > p_old` — ROME's ES / PS / NS exactly, since `seq_prob` is `exp(−mean NLL)` and `exp` is monotone |
| `diff` | mean of `p_new − p_old` — the same quantity as MEMIT's `_diff`, which exponentiates before subtracting |
| `acc` | share of target tokens that are the argmax at their own position |
| `hit` | generation + containment against the gold answer set |


## Layout

```
harness.py                  the run loop
harness_config.json         which models × methods × benchmarks to run
edit_methods/               six methods + EditMethod registry + per-model config
benches/load_benchmarks.py  all five loaders -> Edit_Eval_Pack
genie_bench/                Genie generation pipeline
eval/score.py               ScoreCard, seq_prob, score_probe
eval/results_to_csv.py      artifacts -> cases.csv, one row per case
eval/csv_to_md.py           cases.csv -> markdown table
eval/csv_to_heatgrid.py     cases.csv -> heatmap PNG (plus a -with-diff variant)
eval/run_eval.py            runs the three eval stages over one run directory
utils/                      harness utils, edit utils, edit training, model state
scripts/                    human-run: downloads, covariances, projections, encoder training
models/<name>/card.json     architecture-specific configuration
docs/benchmark_samples/     one example record per benchmark
results/                    run outputs
tests/                      harness and benchmark checks
```

## Tests

`tests/` holds runnable check scripts rather than pytest cases. Used for debugging. 

```bash
uv run python tests/remedi_check_positions.py    # injection index, training vs inference
uv run python tests/genie_check_abstract.py      # abstract_2 / abstract_3 templates
uv run pytest tests/test_mentions.py
```

## Use of AI

AI assistance was used for engineering, debugging, explanation and project management —
not for drafting the research argument, analysis or conclusions. Where an assistant wrote
code, the design, naming and approval are the author's. Every session is logged with its
prompts; that log is an appendix to the report.

## References

- **ROME** — Meng et al., *Locating and Editing Factual Associations in GPT*, NeurIPS 2022
- **MEMIT** — Meng et al., *Mass-Editing Memory in a Transformer*, ICLR 2023
- **GRACE** — Hartvigsen et al., *Aging with GRACE*, NeurIPS 2023
- **AnyEdit** — Jiang et al., *AnyEdit: Edit Any Knowledge Encoded in Language Models*, 2025
- **AlphaEdit** — Fang et al., ICLR 2025 (Outstanding Paper)
- **REMEDI** — Hernandez et al., *Inspecting and Editing Knowledge Representations*, COLM 2024
