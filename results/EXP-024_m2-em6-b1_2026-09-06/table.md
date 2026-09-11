| Benchmark | Probe | Pre-edit | ROME | MEMIT | AlphaEdit | AnyEdit | GRACE | REMEDI |
|:--------------|:--------------|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
| **RippleEdits** | Eff. $\uparrow$ | 0.6~±7.5~ | 92.0~±27.1~ | 51.1~±50.0~ | 76.7~±42.3~ | 22.2~±41.5~ | 84.7~±36.0~ | 1.1~±10.6~ |
|  | Aliasing $\uparrow$ | 0.0~±0.0~ | 38.3~±45.3~ | 18.9~±37.6~ | 44.5~±45.4~ | 14.8~±34.6~ | 25.4~±40.5~ | 1.9~±12.4~ |
|  | Logical $\uparrow$ | 2.7~±16.2~ | 6.8~±23.7~ | 5.4~±19.4~ | 10.8~±28.8~ | 0.0~±0.0~ | 2.7~±16.2~ | 2.7~±16.2~ |
|  | Comp. I $\uparrow$ | 9.4~±26.3~ | 21.4~±35.6~ | 14.6~±26.8~ | 43.8~±45.5~ | 0.0~±0.0~ | 9.4~±26.3~ | 9.4~±26.3~ |
|  | Comp. II $\uparrow$ | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
|  | Rel. spec. $\uparrow$ | 95.2~±21.3~ | 31.3~±44.6~ | 37.3~±45.3~ | 7.5~±24.2~ | 76.0~±39.3~ | 95.2~±21.3~ | 64.9~±42.8~ |
|  | Preservation $\uparrow$ | 0.0 | 0.0 | 0.0 | 100.0 | 0.0 | 0.0 | 100.0 |
|  | *scored by* | *containment* | *containment* | *containment* | *containment* | *containment* | *containment* | *containment* |

: Edit quality on gpt2-xl. n=95 cases per cell, seed 0. All values are percentages, mean ±sd over cases, higher is better throughout. Each benchmark is scored by its own paper's metric — the *scored by* row names it. S is the harmonic mean of efficacy, generalisation and specificity, where a benchmark carries all three. {#tbl:edit-quality-gpt2-xl}

| Benchmark | Probe | Pre-edit | ROME | MEMIT | AlphaEdit | AnyEdit | GRACE | REMEDI |
|:--------------|:--------------|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
| **RippleEdits** | Eff. $\uparrow$ | 0.6~±7.5~ | 96.0~±19.5~ | 85.8~±34.9~ | 65.3~±47.6~ | 80.7~±39.5~ | 80.1~±39.9~ | 7.4~±26.2~ |
|  | Aliasing $\uparrow$ | 0.6~±7.9~ | 62.4~±42.2~ | 32.1~±41.6~ | 17.7~±33.9~ | 58.4~±45.6~ | 20.0~±35.8~ | 12.8~±33.0~ |
|  | Logical $\uparrow$ | 11.0~±29.5~ | 10.2~±27.3~ | 7.2~±23.7~ | 9.8~±28.9~ | 10.2~±29.3~ | 11.0~±29.5~ | 8.3~±23.4~ |
|  | Comp. I $\uparrow$ | 10.5~±21.4~ | 34.0~±38.2~ | 26.3~±36.4~ | 19.3~±32.6~ | 18.9~±32.9~ | 10.5~±21.4~ | 6.6~±21.2~ |
|  | Comp. II $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 25.0~±43.3~ |
|  | Rel. spec. $\uparrow$ | 99.7~±3.3~ | 31.5~±36.9~ | 55.0~±36.7~ | 60.4~±37.0~ | 85.6~±24.9~ | 99.7~±3.3~ | 25.7~±36.6~ |
|  | Preservation $\uparrow$ | 100.0~±0.0~ | 8.3~±27.6~ | 16.7~±37.3~ | 33.3~±47.1~ | 25.0~±43.3~ | 100.0~±0.0~ | 25.0~±43.3~ |
|  | *scored by* | *containment* | *containment* | *containment* | *containment* | *containment* | *containment* | *containment* |

: Edit quality on llama3-8b. n=95 cases per cell, seed 0. All values are percentages, mean ±sd over cases, higher is better throughout. Each benchmark is scored by its own paper's metric — the *scored by* row names it. S is the harmonic mean of efficacy, generalisation and specificity, where a benchmark carries all three. {#tbl:edit-quality-llama3-8b}
