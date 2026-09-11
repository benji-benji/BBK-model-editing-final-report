| Benchmark | Probe | Pre-edit | ROME | MEMIT | AlphaEdit | AnyEdit | GRACE | REMEDI |
|:--------------|:--------------|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
| **CounterFact** | Eff. $\uparrow$ | 33.3~±47.1~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ |
|  | Gen. $\uparrow$ | 50.0~±40.8~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 50.0~±40.8~ | 50.0~±40.8~ | 100.0~±0.0~ |
|  | Spe. $\uparrow$ | 56.7~±30.9~ | 56.7~±30.9~ | 53.3~±33.0~ | 56.7~±30.9~ | 36.7~±33.0~ | 56.7~±30.9~ | 56.7~±30.9~ |
|  | **S** $\uparrow$ | **44.3** | **79.7** | **77.4** | **79.7** | **52.4** | **63.0** | **79.7** |
|  | *scored by* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* |
| **zsRE** | Eff. $\uparrow$ | 27.8~±20.8~ | 63.9~±30.7~ | 91.7~±11.8~ | 100.0~±0.0~ | 47.2~±33.6~ | 100.0~±0.0~ | 38.9~±28.3~ |
|  | Gen. $\uparrow$ | 11.1~±15.7~ | 63.9~±30.7~ | 83.3~±23.6~ | 88.9~±15.7~ | 30.6~±27.5~ | 11.1~±15.7~ | 30.6~±27.5~ |
|  | Spe. $\uparrow$ | 50.0~±13.6~ | 50.0~±13.6~ | 50.0~±13.6~ | 50.0~±13.6~ | 50.0~±13.6~ | 50.0~±13.6~ | 50.0~±13.6~ |
|  | **S** $\uparrow$ | **20.5** | **58.5** | **69.9** | **72.7** | **40.6** | **25.0** | **38.2** |
|  | *scored by* | *exact match* | *exact match* | *exact match* | *exact match* | *exact match* | *exact match* | *exact match* |
| **RippleEdits** | Eff. $\uparrow$ | 0.0~±0.0~ | 40.0~±49.0~ | 100.0~±0.0~ | 80.0~±40.0~ | 60.0~±49.0~ | 80.0~±40.0~ | 20.0~±40.0~ |
|  | Aliasing $\uparrow$ | 0.0~±0.0~ | 40.0~±49.0~ | 40.0~±49.0~ | 60.0~±49.0~ | 50.0~±44.7~ | 25.0~±31.6~ | 0.0~±0.0~ |
|  | Logical $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | Comp. I $\uparrow$ | 0.0~±0.0~ | 7.1~±12.4~ | 32.1~±40.9~ | 35.7~±41.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | Rel. spec. $\uparrow$ | 0.0~±0.0~ | 2.8~±4.8~ | 2.8~±4.8~ | 5.6~±5.6~ | 5.6~±9.6~ | 0.0~±0.0~ | 5.6~±9.6~ |
|  | Preservation $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | *scored by* | *containment* | *containment* | *containment* | *containment* | *containment* | *containment* | *containment* |
| **MQuAKE** | Eff. $\uparrow$ | 28.6~±21.0~ | 67.1~±27.2~ | 81.0~±22.1~ | 83.3~±23.6~ | 77.8~±31.4~ | 100.0~±0.0~ | 28.6~±21.0~ |
|  | Single hop $\uparrow$ | 20.2~±15.0~ | 44.8~±21.2~ | 56.0~±28.0~ | 58.3~±31.2~ | 55.6~±34.2~ | 66.7~±23.6~ | 20.2~±15.0~ |
|  | Multi hop $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 11.1~±15.7~ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | *scored by* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* |

: Edit quality on gpt2-xl. n=3 cases per cell, seed None. All values are percentages, mean ±sd over cases, higher is better throughout. Each benchmark is scored by its own paper's metric — the *scored by* row names it. S is the harmonic mean of efficacy, generalisation and specificity, where a benchmark carries all three. {#tbl:edit-quality-gpt2-xl}

| Benchmark | Probe | Pre-edit | ROME | MEMIT | AlphaEdit | AnyEdit | GRACE | REMEDI |
|:--------------|:--------------|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
| **CounterFact** | Eff. $\uparrow$ | 33.3~±47.1~ | 33.3~±47.1~ | 100.0~±0.0~ | 100.0~±0.0~ | 33.3~±47.1~ | 100.0~±0.0~ | 100.0~±0.0~ |
|  | Gen. $\uparrow$ | 33.3~±47.1~ | 66.7~±47.1~ | 50.0~±40.8~ | 33.3~±47.1~ | 33.3~±47.1~ | 33.3~±47.1~ | 100.0~±0.0~ |
|  | Spe. $\uparrow$ | 66.7~±24.9~ | 73.3~±20.5~ | 50.0~±8.2~ | 66.7~±24.9~ | 70.0~±21.6~ | 66.7~±24.9~ | 66.7~±24.9~ |
|  | **S** $\uparrow$ | **40.0** | **51.2** | **60.0** | **54.5** | **40.4** | **54.5** | **85.7** |
|  | *scored by* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* |
| **zsRE** | Eff. $\uparrow$ | 11.1~±15.7~ | 22.2~±15.7~ | 55.6~±41.6~ | 66.7~±47.1~ | 33.3~±27.2~ | 100.0~±0.0~ | 22.2~±31.4~ |
|  | Gen. $\uparrow$ | 11.1~±15.7~ | 22.2~±15.7~ | 55.6~±41.6~ | 66.7~±47.1~ | 22.2~±31.4~ | 11.1~±15.7~ | 11.1~±15.7~ |
|  | Spe. $\uparrow$ | 50.0~±13.6~ | 50.0~±13.6~ | 50.0~±13.6~ | 50.0~±13.6~ | 50.0~±13.6~ | 50.0~±13.6~ | 50.0~±13.6~ |
|  | **S** $\uparrow$ | **15.0** | **27.3** | **53.6** | **60.0** | **31.6** | **25.0** | **19.4** |
|  | *scored by* | *exact match* | *exact match* | *exact match* | *exact match* | *exact match* | *exact match* | *exact match* |
| **RippleEdits** | Eff. $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 60.0~±49.0~ | 60.0~±49.0~ | 0.0~±0.0~ | 80.0~±40.0~ | 20.0~±40.0~ |
|  | Aliasing $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 40.0~±49.0~ | 60.0~±49.0~ | 0.0~±0.0~ | 15.0~±30.0~ | 0.0~±0.0~ |
|  | Logical $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | Comp. I $\uparrow$ | 0.0~±0.0~ | 5.0~±8.7~ | 47.9~±39.8~ | 19.3~±23.3~ | 0.0~±0.0~ | 0.0~±0.0~ | 3.6~±6.2~ |
|  | Rel. spec. $\uparrow$ | 33.3~±34.2~ | 5.6~±9.6~ | 8.3~±9.2~ | 11.1~±11.1~ | 8.3~±14.4~ | 33.3~±34.2~ | 11.1~±11.1~ |
|  | Preservation $\uparrow$ | 50.0~±50.0~ | 0.0~±0.0~ | 50.0~±50.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 50.0~±50.0~ | 0.0~±0.0~ |
|  | *scored by* | *containment* | *containment* | *containment* | *containment* | *containment* | *containment* | *containment* |
| **MQuAKE** | Eff. $\uparrow$ | 36.1~±10.4~ | 38.9~±15.7~ | 91.7~±11.8~ | 66.7~±11.8~ | 47.2~±33.6~ | 100.0~±0.0~ | 38.9~±10.4~ |
|  | Single hop $\uparrow$ | 40.3~±16.1~ | 38.9~±25.8~ | 79.2~±21.2~ | 62.5~±27.0~ | 51.4~±37.3~ | 83.3~±23.6~ | 43.1~±15.3~ |
|  | Multi hop $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 33.3~±47.1~ |
|  | *scored by* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* |

: Edit quality on llama3-8b. n=3 cases per cell, seed None. All values are percentages, mean ±sd over cases, higher is better throughout. Each benchmark is scored by its own paper's metric — the *scored by* row names it. S is the harmonic mean of efficacy, generalisation and specificity, where a benchmark carries all three. {#tbl:edit-quality-llama3-8b}
