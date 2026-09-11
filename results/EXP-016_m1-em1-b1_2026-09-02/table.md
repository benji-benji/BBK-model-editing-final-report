| Benchmark | Probe | Pre-edit | AnyEdit |
|:--------------|:--------------|----------:|----------:|
| **CounterFact** | Eff. $\uparrow$ | 33.3~±47.1~ | 66.7~±47.1~ |
|  | Gen. $\uparrow$ | 33.3~±47.1~ | 33.3~±47.1~ |
|  | Spe. $\uparrow$ | 66.7~±24.9~ | 56.7~±12.5~ |
|  | **S** $\uparrow$ | **40.0** | **47.9** |
|  | *scored by* | *p(new) > p(old)* | *p(new) > p(old)* |

: Edit quality on llama3-8b. n=3 cases per cell, seed None. All values are percentages, mean ±sd over cases, higher is better throughout. Each benchmark is scored by its own paper's metric — the *scored by* row names it. S is the harmonic mean of efficacy, generalisation and specificity, where a benchmark carries all three. {#tbl:edit-quality-llama3-8b}
