| Benchmark | Probe | Pre-edit | ROME | MEMIT | AlphaEdit | AnyEdit | GRACE | REMEDI |
|:--------------|:--------------|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
| **CounterFact** | Eff. $\uparrow$ | 0.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 40.0~±49.0~ |
|  | Gen. $\uparrow$ | 0.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 10.0~±20.0~ | 0.0~±0.0~ | 20.0~±24.5~ |
|  | Spe. $\uparrow$ | 74.0~±22.4~ | 70.0~±21.0~ | 68.0~±21.4~ | 64.0~±24.2~ | 50.0~±27.6~ | 72.0~±21.4~ | 74.0~±22.4~ |
|  | **S** $\uparrow$ | **0.0** | **87.5** | **86.4** | **84.2** | **23.1** | **0.0** | **33.9** |
|  | *scored by* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* |
| **zsRE** | Eff. $\uparrow$ | 45.0~±26.7~ | 100.0~±0.0~ | 83.3~±21.1~ | 91.7~±10.5~ | 100.0~±0.0~ | 100.0~±0.0~ | 55.0~±14.5~ |
|  | Gen. $\uparrow$ | 55.0~±14.5~ | 75.0~±22.4~ | 65.0~±13.3~ | 81.7~±18.6~ | 58.3~±18.3~ | 55.0~±14.5~ | 55.0~±14.5~ |
|  | Spe. $\uparrow$ | 28.0~±25.7~ | 28.0~±25.7~ | 28.0~±25.7~ | 28.0~±25.7~ | 28.0~±25.7~ | 28.0~±25.7~ | 28.0~±25.7~ |
|  | **S** $\uparrow$ | **39.4** | **50.8** | **47.5** | **50.9** | **47.7** | **46.9** | **41.6** |
|  | *scored by* | *exact match* | *exact match* | *exact match* | *exact match* | *exact match* | *exact match* | *exact match* |
| **RippleEdits** | Eff. $\uparrow$ | 0.0~±0.0~ | 100.0~±0.0~ | 30.0~±45.8~ | 80.0~±40.0~ | 10.0~±30.0~ | 90.0~±30.0~ | 0.0~±0.0~ |
|  | Logical $\uparrow$ | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
|  | Rel. spec. $\uparrow$ | 100.0~±0.0~ | 66.7~±47.1~ | 66.7~±47.1~ | 0.0~±0.0~ | 83.3~±23.6~ | 100.0~±0.0~ | 66.7~±23.6~ |
|  | *scored by* | *containment* | *containment* | *containment* | *containment* | *containment* | *containment* | *containment* |
| **MQuAKE** | Eff. $\uparrow$ | 35.1~±17.5~ | 95.9~±5.1~ | 83.9~±20.7~ | 95.6~±8.9~ | 69.3~±24.3~ | 100.0~±0.0~ | 35.1~±17.5~ |
|  | Single hop $\uparrow$ | 43.5~±24.8~ | 84.6~±21.0~ | 76.1~±27.6~ | 82.2~±24.2~ | 68.5~±29.5~ | 86.7~±19.4~ | 43.5~±24.8~ |
|  | Multi hop $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | *scored by* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* |
| **GENIE** | Eff. $\uparrow$ | 40.0~±49.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 60.0~±49.0~ | 100.0~±0.0~ | 60.0~±49.0~ |
|  | Para. 1 $\uparrow$ | 40.0~±49.0~ | 80.0~±40.0~ | 80.0~±40.0~ | 100.0~±0.0~ | 40.0~±49.0~ | 40.0~±49.0~ | 60.0~±49.0~ |
|  | Para. 2 $\uparrow$ | 40.0~±49.0~ | 80.0~±40.0~ | 60.0~±49.0~ | 100.0~±0.0~ | 40.0~±49.0~ | 40.0~±49.0~ | 60.0~±49.0~ |
|  | Para. 3 $\uparrow$ | 40.0~±49.0~ | 80.0~±40.0~ | 80.0~±40.0~ | 100.0~±0.0~ | 40.0~±49.0~ | 40.0~±49.0~ | 60.0~±49.0~ |
|  | Hop 1 $\uparrow$ | 50.0~±50.0~ | 50.0~±50.0~ | 50.0~±50.0~ | 75.0~±43.3~ | 50.0~±50.0~ | 50.0~±50.0~ | 100.0~±0.0~ |
|  | Hop 2 $\uparrow$ | 0.0 | 0.0 | 0.0 | 0.0 | 100.0 | 0.0 | 100.0 |
|  | Hop 3 $\uparrow$ | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 100.0 |
|  | Abs. 1 $\uparrow$ | 50.0~±50.0~ | 50.0~±50.0~ | 50.0~±50.0~ | 0.0~±0.0~ | 50.0~±50.0~ | 50.0~±50.0~ | 50.0~±50.0~ |
|  | Abs. 2 $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 80.0~±40.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 20.0~±40.0~ |
|  | Abs. 3 $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 20.0~±40.0~ |
|  | *scored by* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* |

: Edit quality on gpt2-xl. n=5 cases per cell, seed 0. All values are percentages, mean ±sd over cases, higher is better throughout. Each benchmark is scored by its own paper's metric — the *scored by* row names it. S is the harmonic mean of efficacy, generalisation and specificity, where a benchmark carries all three. {#tbl:edit-quality-gpt2-xl}

| Benchmark | Probe | Pre-edit | ROME | MEMIT | AlphaEdit | AnyEdit | GRACE | REMEDI |
|:--------------|:--------------|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
| **CounterFact** | Eff. $\uparrow$ | 0.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 80.0~±40.0~ |
|  | Gen. $\uparrow$ | 0.0~±0.0~ | 80.0~±40.0~ | 80.0~±40.0~ | 60.0~±49.0~ | 10.0~±20.0~ | 0.0~±0.0~ | 40.0~±37.4~ |
|  | Spe. $\uparrow$ | 96.0~±8.0~ | 72.0~±23.2~ | 92.0~±7.5~ | 94.0~±8.0~ | 76.0~±22.4~ | 96.0~±8.0~ | 96.0~±8.0~ |
|  | **S** $\uparrow$ | **0.0** | **82.4** | **89.9** | **80.4** | **24.4** | **0.0** | **62.6** |
|  | *scored by* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* |
| **zsRE** | Eff. $\uparrow$ | 42.7~±26.1~ | 100.0~±0.0~ | 100.0~±0.0~ | 80.0~±40.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 43.7~±25.7~ |
|  | Gen. $\uparrow$ | 38.7~±21.1~ | 100.0~±0.0~ | 71.0~±36.9~ | 71.0~±36.9~ | 57.7~±36.1~ | 38.7~±21.1~ | 43.7~±25.7~ |
|  | Spe. $\uparrow$ | 41.0~±28.9~ | 41.2~±29.0~ | 41.0~±28.9~ | 41.0~±28.9~ | 41.0~±28.9~ | 41.0~±28.9~ | 41.0~±28.9~ |
|  | **S** $\uparrow$ | **40.7** | **67.8** | **61.9** | **58.9** | **58.0** | **49.8** | **42.7** |
|  | *scored by* | *exact match* | *exact match* | *exact match* | *exact match* | *exact match* | *exact match* | *exact match* |
| **RippleEdits** | Eff. $\uparrow$ | 0.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 60.0~±49.0~ | 90.0~±30.0~ | 90.0~±30.0~ | 10.0~±30.0~ |
|  | Logical $\uparrow$ | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
|  | Comp. I $\uparrow$ | 0.0~±0.0~ | 33.3~±23.6~ | 0.0~±0.0~ | 16.7~±23.6~ | 16.7~±23.6~ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | Rel. spec. $\uparrow$ | 100.0~±0.0~ | 56.8~±43.6~ | 62.5~±36.0~ | 65.7~±34.6~ | 88.2~±21.8~ | 100.0~±0.0~ | 20.7~±33.9~ |
|  | Preservation $\uparrow$ | 100.0~±0.0~ | 50.0~±50.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 100.0~±0.0~ | 0.0~±0.0~ |
|  | *scored by* | *containment* | *containment* | *containment* | *containment* | *containment* | *containment* | *containment* |
| **MQuAKE** | Eff. $\uparrow$ | 40.9~±15.3~ | 100.0~±0.0~ | 96.7~±6.7~ | 82.7~±22.0~ | 100.0~±0.0~ | 96.1~±4.8~ | 55.4~±21.3~ |
|  | Single hop $\uparrow$ | 50.1~±25.1~ | 90.0~±20.0~ | 86.7~±19.4~ | 81.9~±17.8~ | 90.0~±20.0~ | 87.2~±21.6~ | 57.8~±28.9~ |
|  | Multi hop $\uparrow$ | 0.0~±0.0~ | 20.0~±26.7~ | 6.7~±13.3~ | 6.7~±13.3~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | *scored by* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* |
| **GENIE** | Eff. $\uparrow$ | 20.0~±40.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 80.0~±40.0~ |
|  | Para. 1 $\uparrow$ | 0.0~±0.0~ | 80.0~±40.0~ | 80.0~±40.0~ | 40.0~±49.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 80.0~±40.0~ |
|  | Para. 2 $\uparrow$ | 20.0~±40.0~ | 80.0~±40.0~ | 100.0~±0.0~ | 60.0~±49.0~ | 20.0~±40.0~ | 20.0~±40.0~ | 80.0~±40.0~ |
|  | Para. 3 $\uparrow$ | 40.0~±49.0~ | 80.0~±40.0~ | 80.0~±40.0~ | 80.0~±40.0~ | 40.0~±49.0~ | 40.0~±49.0~ | 80.0~±40.0~ |
|  | Hop 1 $\uparrow$ | 0.0 | 0.0 | 100.0 | 100.0 | 100.0 | 0.0 | 100.0 |
|  | Abs. 1 $\uparrow$ | 50.0~±50.0~ | 75.0~±43.3~ | 50.0~±50.0~ | 25.0~±43.3~ | 50.0~±50.0~ | 50.0~±50.0~ | 50.0~±50.0~ |
|  | Abs. 2 $\uparrow$ | 0.0~±0.0~ | 25.0~±43.3~ | 50.0~±50.0~ | 25.0~±43.3~ | 0.0~±0.0~ | 0.0~±0.0~ | 25.0~±43.3~ |
|  | Abs. 3 $\uparrow$ | 0.0~±0.0~ | 20.0~±40.0~ | 20.0~±40.0~ | 40.0~±49.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | *scored by* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* |

: Edit quality on llama3-8b. n=5 cases per cell, seed 0. All values are percentages, mean ±sd over cases, higher is better throughout. Each benchmark is scored by its own paper's metric — the *scored by* row names it. S is the harmonic mean of efficacy, generalisation and specificity, where a benchmark carries all three. {#tbl:edit-quality-llama3-8b}
