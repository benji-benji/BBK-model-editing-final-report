| Benchmark | Probe | Pre-edit | ROME | MEMIT | AnyEdit |
|:--------------|:--------------|----------:|----------:|----------:|----------:|
| **CounterFact** | Eff. $\uparrow$ | 33.3~±47.1~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ |
|  | Gen. $\uparrow$ | 50.0~±40.8~ | 100.0~±0.0~ | 100.0~±0.0~ | 50.0~±40.8~ |
|  | Spe. $\uparrow$ | 56.7~±30.9~ | 56.7~±30.9~ | 53.3~±33.0~ | 36.7~±33.0~ |
|  | **S** $\uparrow$ | **44.3** | **79.7** | **77.4** | **52.4** |
|  | *scored by* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* |

: Edit quality on gpt2-xl. n=3 cases per cell, seed None. All values are percentages, mean ±sd over cases, higher is better throughout. Each benchmark is scored by its own paper's metric — the *scored by* row names it. S is the harmonic mean of efficacy, generalisation and specificity, where a benchmark carries all three. {#tbl:edit-quality-gpt2-xl}

| Benchmark | Probe | Pre-edit | ROME | MEMIT | AnyEdit |
|:--------------|:--------------|----------:|----------:|----------:|----------:|
| **CounterFact** | Eff. $\uparrow$ | 33.3~±47.1~ | 33.3~±47.1~ | 100.0~±0.0~ | 33.3~±47.1~ |
|  | Gen. $\uparrow$ | 33.3~±47.1~ | 50.0~±40.8~ | 83.3~±23.6~ | 33.3~±47.1~ |
|  | Spe. $\uparrow$ | 66.7~±24.9~ | 66.7~±24.9~ | 30.0~±16.3~ | 56.7~±12.5~ |
|  | **S** $\uparrow$ | **40.0** | **46.2** | **54.2** | **38.6** |
|  | *scored by* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* |

: Edit quality on llama3-8b. n=3 cases per cell, seed None. All values are percentages, mean ±sd over cases, higher is better throughout. Each benchmark is scored by its own paper's metric — the *scored by* row names it. S is the harmonic mean of efficacy, generalisation and specificity, where a benchmark carries all three. {#tbl:edit-quality-llama3-8b}
