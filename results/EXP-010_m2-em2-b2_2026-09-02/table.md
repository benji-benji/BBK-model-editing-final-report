| Benchmark | Probe | Pre-edit | ROME | MEMIT |
|:--------------|:--------------|----------:|----------:|----------:|
| **CounterFact** | Eff. $\uparrow$ | 15.0~±35.7~ | 100.0~±0.0~ | 100.0~±0.0~ |
|  | Gen. $\uparrow$ | 22.5~±37.0~ | 92.5~±17.9~ | 87.5~±31.1~ |
|  | Spe. $\uparrow$ | 81.0~±23.9~ | 78.5~±22.9~ | 78.0~±24.6~ |
|  | **S** $\uparrow$ | **24.3** | **89.4** | **87.6** |
|  | *scored by* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* |
| **zsRE** | Eff. $\uparrow$ | 0.0~±0.0~ | 10.0~±30.0~ | 30.0~±45.8~ |
|  | Gen. $\uparrow$ | 0.0~±0.0~ | 10.0~±30.0~ | 20.0~±40.0~ |
|  | Spe. $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | **S** $\uparrow$ | **0.0** | **0.0** | **0.0** |
|  | *scored by* | *exact match* | *exact match* | *exact match* |

: Edit quality on gpt2-xl. n=20 cases per cell, seed None. All values are percentages, mean ±sd over cases, higher is better throughout. Each benchmark is scored by its own paper's metric — the *scored by* row names it. S is the harmonic mean of efficacy, generalisation and specificity, where a benchmark carries all three. {#tbl:edit-quality-gpt2-xl}

| Benchmark | Probe | Pre-edit | ROME | MEMIT |
|:--------------|:--------------|----------:|----------:|----------:|
| **CounterFact** | Eff. $\uparrow$ | 15.0~±35.7~ | 35.0~±47.7~ | 60.0~±49.0~ |
|  | Gen. $\uparrow$ | 12.5~±31.1~ | 35.0~±42.1~ | 35.0~±39.1~ |
|  | Spe. $\uparrow$ | 87.5~±19.2~ | 88.0~±19.1~ | 85.0~±20.9~ |
|  | **S** $\uparrow$ | **19.0** | **43.8** | **52.6** |
|  | *scored by* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* |
| **zsRE** | Eff. $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | Gen. $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | Spe. $\uparrow$ | 5.0~±21.8~ | 5.0~±21.8~ | 5.0~±21.8~ |
|  | **S** $\uparrow$ | **0.0** | **0.0** | **0.0** |
|  | *scored by* | *exact match* | *exact match* | *exact match* |

: Edit quality on llama3-8b. n=20 cases per cell, seed None. All values are percentages, mean ±sd over cases, higher is better throughout. Each benchmark is scored by its own paper's metric — the *scored by* row names it. S is the harmonic mean of efficacy, generalisation and specificity, where a benchmark carries all three. {#tbl:edit-quality-llama3-8b}
