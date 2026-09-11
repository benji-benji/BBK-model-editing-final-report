| Benchmark | Probe | Pre-edit | ROME | MEMIT |
|:--------------|:--------------|----------:|----------:|----------:|
| **CounterFact** | Eff. $\uparrow$ | 15.0~±35.7~ | 15.0~±35.7~ | 100.0~±0.0~ |
|  | Gen. $\uparrow$ | 22.5~±37.0~ | 22.5~±37.0~ | 95.0~±15.0~ |
|  | Spe. $\uparrow$ | 81.0~±23.9~ | 81.0~±23.9~ | 76.0~±23.7~ |
|  | **S** $\uparrow$ | **24.3** | **24.3** | **89.1** |
|  | *scored by* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* |
| **zsRE** | Eff. $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 65.0~±47.7~ |
|  | Gen. $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 35.0~±47.7~ |
|  | Spe. $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | **S** $\uparrow$ | **0.0** | **0.0** | **0.0** |
|  | *scored by* | *exact match* | *exact match* | *exact match* |

: Edit quality on gpt2-xl. n=20 cases per cell, seed None. All values are percentages, mean ±sd over cases, higher is better throughout. Each benchmark is scored by its own paper's metric — the *scored by* row names it. S is the harmonic mean of efficacy, generalisation and specificity, where a benchmark carries all three. {#tbl:edit-quality-gpt2-xl}

| Benchmark | Probe | Pre-edit | ROME | MEMIT |
|:--------------|:--------------|----------:|----------:|----------:|
| **CounterFact** | Eff. $\uparrow$ | 15.0~±35.7~ | 15.0~±35.7~ | 95.0~±21.8~ |
|  | Gen. $\uparrow$ | 12.5~±31.1~ | 12.5~±31.1~ | 92.5~±23.8~ |
|  | Spe. $\uparrow$ | 87.5~±19.2~ | 87.5~±19.2~ | 54.5~±35.7~ |
|  | **S** $\uparrow$ | **19.0** | **19.0** | **75.6** |
|  | *scored by* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* |
| **zsRE** | Eff. $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 35.0~±47.7~ |
|  | Gen. $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 30.0~±45.8~ |
|  | Spe. $\uparrow$ | 5.0~±21.8~ | 5.0~±21.8~ | 5.0~±21.8~ |
|  | **S** $\uparrow$ | **0.0** | **0.0** | **11.5** |
|  | *scored by* | *exact match* | *exact match* | *exact match* |

: Edit quality on llama3-8b. n=20 cases per cell, seed None. All values are percentages, mean ±sd over cases, higher is better throughout. Each benchmark is scored by its own paper's metric — the *scored by* row names it. S is the harmonic mean of efficacy, generalisation and specificity, where a benchmark carries all three. {#tbl:edit-quality-llama3-8b}
