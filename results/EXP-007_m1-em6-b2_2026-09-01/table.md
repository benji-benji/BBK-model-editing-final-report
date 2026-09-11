| Benchmark | Probe | Pre-edit | ROME | MEMIT | AlphaEdit | AnyEdit | GRACE | REMEDI |
|:--------------|:--------|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
| **CounterFact** | Eff. $\uparrow$ | 0.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | --- |
|  | Gen. $\uparrow$ | 16.7~±23.6~ | 83.3~±23.6~ | 100.0~±0.0~ | 100.0~±0.0~ | 66.7~±23.6~ | 16.7~±23.6~ | --- |
|  | Spe. $\uparrow$ | 96.7~±4.7~ | 70.0~±29.4~ | 36.7~±37.7~ | 40.0~±35.6~ | 16.7~±23.6~ | 93.3~±9.4~ | --- |
|  | **S** $\uparrow$ | **0.0** | **82.7** | **63.5** | **66.7** | **35.3** | **37.2** | --- |
| **zsRE** | Eff. $\uparrow$ | 66.7~±47.1~ | 66.7~±47.1~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 66.7~±47.1~ |
|  | Gen. $\uparrow$ | 66.7~±47.1~ | 66.7~±47.1~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 66.7~±47.1~ | 66.7~±47.1~ |
|  | Spe. $\uparrow$ | 66.7~±47.1~ | 66.7~±47.1~ | 66.7~±47.1~ | 66.7~±47.1~ | 66.7~±47.1~ | 66.7~±47.1~ | 66.7~±47.1~ |
|  | **S** $\uparrow$ | **66.7** | **66.7** | **85.7** | **85.7** | **85.7** | **75.0** | **66.7** |

: Edit quality on gpt2-xl. n=3 cases per cell, seed 42. All values are percentages, mean ±sd over cases. Eff. and Gen. give the share of probes on which the new answer outscores the old; Spe. gives the share on which the old answer is retained, so higher is better throughout. S is the harmonic mean of the three. {#tbl:edit-quality-gpt2-xl}
