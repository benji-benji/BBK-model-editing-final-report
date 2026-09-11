| Benchmark | Probe | Pre-edit | REMEDI |
|:--------------|:--------------|----------:|----------:|
| **CounterFact** | Eff. $\uparrow$ | 33.3~±47.1~ | 100.0~±0.0~ |
|  | Gen. $\uparrow$ | 50.0~±40.8~ | 100.0~±0.0~ |
|  | Spe. $\uparrow$ | 56.7~±30.9~ | 56.7~±30.9~ |
|  | **S** $\uparrow$ | **44.3** | **79.7** |
|  | *scored by* | *p(new) > p(old)* | *p(new) > p(old)* |
| **RippleEdits** | Eff. $\uparrow$ | 0.0~±0.0~ | 20.0~±40.0~ |
|  | Aliasing $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | Logical $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | Comp. I $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | Rel. spec. $\uparrow$ | 0.0~±0.0~ | 5.6~±9.6~ |
|  | Preservation $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | *scored by* | *containment* | *containment* |

: Edit quality on gpt2-xl. n=3 cases per cell, seed None. All values are percentages, mean ±sd over cases, higher is better throughout. Each benchmark is scored by its own paper's metric — the *scored by* row names it. S is the harmonic mean of efficacy, generalisation and specificity, where a benchmark carries all three. {#tbl:edit-quality-gpt2-xl}

| Benchmark | Probe | Pre-edit | REMEDI |
|:--------------|:--------------|----------:|----------:|
| **CounterFact** | Eff. $\uparrow$ | 33.3~±47.1~ | 100.0~±0.0~ |
|  | Gen. $\uparrow$ | 33.3~±47.1~ | 100.0~±0.0~ |
|  | Spe. $\uparrow$ | 66.7~±24.9~ | 66.7~±24.9~ |
|  | **S** $\uparrow$ | **40.0** | **85.7** |
|  | *scored by* | *p(new) > p(old)* | *p(new) > p(old)* |
| **RippleEdits** | Eff. $\uparrow$ | 0.0~±0.0~ | 20.0~±40.0~ |
|  | Aliasing $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | Logical $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | Comp. I $\uparrow$ | 0.0~±0.0~ | 3.6~±6.2~ |
|  | Rel. spec. $\uparrow$ | 33.3~±34.2~ | 11.1~±11.1~ |
|  | Preservation $\uparrow$ | 50.0~±50.0~ | 0.0~±0.0~ |
|  | *scored by* | *containment* | *containment* |

: Edit quality on llama3-8b. n=3 cases per cell, seed None. All values are percentages, mean ±sd over cases, higher is better throughout. Each benchmark is scored by its own paper's metric — the *scored by* row names it. S is the harmonic mean of efficacy, generalisation and specificity, where a benchmark carries all three. {#tbl:edit-quality-llama3-8b}
