| Benchmark | Probe | Pre-edit | ROME | MEMIT | AlphaEdit | AnyEdit | GRACE | REMEDI |
|:--------------|:--------------|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
| **CounterFact** | Eff. $\uparrow$ | 20.0~±40.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 80.0~±40.0~ | 100.0~±0.0~ | 80.0~±40.0~ |
|  | Gen. $\uparrow$ | 30.0~±40.0~ | 90.0~±20.0~ | 90.0~±20.0~ | 100.0~±0.0~ | 30.0~±40.0~ | 30.0~±40.0~ | 80.0~±40.0~ |
|  | Spe. $\uparrow$ | 66.0~±29.4~ | 66.0~±29.4~ | 62.0~±31.9~ | 64.0~±30.1~ | 50.0~±31.0~ | 60.0~±32.9~ | 66.0~±29.4~ |
|  | **S** $\uparrow$ | **30.5** | **82.7** | **80.6** | **84.2** | **45.6** | **50.0** | **74.7** |
|  | *scored by* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* |
| **zsRE** | Eff. $\uparrow$ | 33.3~±18.3~ | 60.0~±27.6~ | 88.3~±14.5~ | 100.0~±0.0~ | 50.0~±29.3~ | 100.0~±0.0~ | 40.0~±22.6~ |
|  | Gen. $\uparrow$ | 23.3~±20.0~ | 60.0~±27.6~ | 76.7~±29.1~ | 86.7~±16.3~ | 40.0~±27.6~ | 23.3~±20.0~ | 35.0~±22.6~ |
|  | Spe. $\uparrow$ | 36.7~±22.1~ | 36.7~±22.1~ | 36.7~±22.1~ | 36.7~±22.1~ | 36.7~±22.1~ | 36.7~±22.1~ | 36.7~±22.1~ |
|  | **S** $\uparrow$ | **30.0** | **49.5** | **58.1** | **61.5** | **41.5** | **37.4** | **37.1** |
|  | *scored by* | *exact match* | *exact match* | *exact match* | *exact match* | *exact match* | *exact match* | *exact match* |
| **RippleEdits** | Eff. $\uparrow$ | 0.0~±0.0~ | 25.0~±43.3~ | 75.0~±43.3~ | 62.5~±48.4~ | 37.5~±48.4~ | 62.5~±48.4~ | 12.5~±33.1~ |
|  | Aliasing $\uparrow$ | 0.0~±0.0~ | 25.0~±43.3~ | 25.0~±43.3~ | 37.5~±48.4~ | 31.2~±42.8~ | 15.6~±27.8~ | 0.0~±0.0~ |
|  | Logical $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | Comp. I $\uparrow$ | 0.0~±0.0~ | 7.1~±12.4~ | 32.1~±40.9~ | 35.7~±41.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | Rel. spec. $\uparrow$ | 7.1~±12.1~ | 1.6~±3.9~ | 4.0~±6.4~ | 3.2~±5.0~ | 5.6~±8.9~ | 7.1~±12.1~ | 12.7~±23.3~ |
|  | Preservation $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | *scored by* | *containment* | *containment* | *containment* | *containment* | *containment* | *containment* | *containment* |
| **MQuAKE** | Eff. $\uparrow$ | 33.8~±18.3~ | 62.7~±22.1~ | 73.6~±20.9~ | 90.0~±20.0~ | 71.7~±26.7~ | 100.0~±0.0~ | 33.8~±18.3~ |
|  | Single hop $\uparrow$ | 25.5~±16.9~ | 44.4~±20.3~ | 53.6~±27.0~ | 65.0~±30.0~ | 53.3~±31.0~ | 70.0~±24.5~ | 25.5~±16.9~ |
|  | Multi hop $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 6.7~±13.3~ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | *scored by* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* |
| **GENIE** | Eff. $\uparrow$ | 80.0~±40.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 80.0~±40.0~ | 100.0~±0.0~ | 80.0~±40.0~ |
|  | Para. 1 $\uparrow$ | 20.0~±40.0~ | 100.0~±0.0~ | 80.0~±40.0~ | 100.0~±0.0~ | 20.0~±40.0~ | 20.0~±40.0~ | 40.0~±49.0~ |
|  | Para. 2 $\uparrow$ | 60.0~±49.0~ | 100.0~±0.0~ | 80.0~±40.0~ | 100.0~±0.0~ | 60.0~±49.0~ | 60.0~±49.0~ | 60.0~±49.0~ |
|  | Para. 3 $\uparrow$ | 40.0~±49.0~ | 100.0~±0.0~ | 80.0~±40.0~ | 100.0~±0.0~ | 60.0~±49.0~ | 40.0~±49.0~ | 60.0~±49.0~ |
|  | Hop 1 $\uparrow$ | 66.7~±47.1~ | 66.7~±47.1~ | 66.7~±47.1~ | 66.7~±47.1~ | 66.7~±47.1~ | 66.7~±47.1~ | 66.7~±47.1~ |
|  | Abs. 1 $\uparrow$ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ |
|  | Abs. 2 $\uparrow$ | 0.0~±0.0~ | 50.0~±50.0~ | 0.0~±0.0~ | 50.0~±50.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | Abs. 3 $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | *scored by* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* |

: Edit quality on gpt2-xl. n=5 cases per cell, seed None. All values are percentages, mean ±sd over cases, higher is better throughout. Each benchmark is scored by its own paper's metric — the *scored by* row names it. S is the harmonic mean of efficacy, generalisation and specificity, where a benchmark carries all three. {#tbl:edit-quality-gpt2-xl}

| Benchmark | Probe | Pre-edit | ROME | MEMIT | AlphaEdit | AnyEdit | GRACE | REMEDI |
|:--------------|:--------------|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
| **CounterFact** | Eff. $\uparrow$ | 20.0~±40.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ |
|  | Gen. $\uparrow$ | 20.0~±40.0~ | 100.0~±0.0~ | 80.0~±40.0~ | 60.0~±49.0~ | 40.0~±37.4~ | 20.0~±40.0~ | 100.0~±0.0~ |
|  | Spe. $\uparrow$ | 70.0~±20.0~ | 46.0~±20.6~ | 64.0~±20.6~ | 68.0~±19.4~ | 44.0~±16.2~ | 70.0~±20.0~ | 70.0~±20.0~ |
|  | **S** $\uparrow$ | **26.2** | **71.9** | **78.7** | **72.5** | **52.0** | **40.4** | **87.5** |
|  | *scored by* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* |
| **zsRE** | Eff. $\uparrow$ | 23.3~±20.0~ | 63.3~±22.1~ | 95.0~±10.0~ | 80.0~±40.0~ | 100.0~±0.0~ | 93.3~±13.3~ | 30.0~±26.7~ |
|  | Gen. $\uparrow$ | 21.7~±29.6~ | 56.7~±24.9~ | 88.3~±14.5~ | 73.3~±38.9~ | 46.7~±45.2~ | 21.7~±29.6~ | 28.3~±27.7~ |
|  | Spe. $\uparrow$ | 52.0~±11.3~ | 52.0~±11.3~ | 52.0~±11.3~ | 52.0~±11.3~ | 52.0~±11.3~ | 52.0~±11.3~ | 52.0~±11.3~ |
|  | **S** $\uparrow$ | **27.7** | **57.0** | **73.0** | **66.1** | **59.2** | **39.4** | **34.1** |
|  | *scored by* | *exact match* | *exact match* | *exact match* | *exact match* | *exact match* | *exact match* | *exact match* |
| **RippleEdits** | Eff. $\uparrow$ | 0.0~±0.0~ | 12.5~±33.1~ | 75.0~±43.3~ | 62.5~±48.4~ | 62.5~±48.4~ | 87.5~±33.1~ | 12.5~±33.1~ |
|  | Aliasing $\uparrow$ | 0.0~±0.0~ | 22.9~±39.9~ | 62.5~±48.4~ | 37.5~±48.4~ | 33.3~±44.1~ | 9.4~±24.8~ | 0.0~±0.0~ |
|  | Logical $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | Comp. I $\uparrow$ | 0.0~±0.0~ | 10.7~±18.6~ | 44.3~±38.1~ | 19.3~±23.3~ | 30.0~±41.2~ | 0.0~±0.0~ | 3.6~±6.2~ |
|  | Rel. spec. $\uparrow$ | 36.9~±28.7~ | 17.9~±13.3~ | 24.2~±20.9~ | 19.4~±13.0~ | 35.3~±26.0~ | 36.9~±28.7~ | 24.2~±20.9~ |
|  | Preservation $\uparrow$ | 20.0~±40.0~ | 0.0~±0.0~ | 20.0~±40.0~ | 0.0~±0.0~ | 20.0~±40.0~ | 20.0~±40.0~ | 0.0~±0.0~ |
|  | *scored by* | *containment* | *containment* | *containment* | *containment* | *containment* | *containment* | *containment* |
| **MQuAKE** | Eff. $\uparrow$ | 39.0~±17.2~ | 67.7~±25.8~ | 90.0~±12.2~ | 80.0~±18.7~ | 95.0~±10.0~ | 100.0~±0.0~ | 45.7~±13.4~ |
|  | Single hop $\uparrow$ | 34.8~±14.7~ | 56.8~±11.3~ | 70.0~±18.7~ | 67.5~±26.9~ | 77.5~±22.9~ | 80.0~±24.5~ | 41.5~±12.6~ |
|  | Multi hop $\uparrow$ | 0.0~±0.0~ | 20.0~±40.0~ | 6.7~±13.3~ | 0.0~±0.0~ | 6.7~±13.3~ | 0.0~±0.0~ | 20.0~±40.0~ |
|  | *scored by* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* |
| **GENIE** | Eff. $\uparrow$ | 0.0~±0.0~ | 80.0~±40.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 40.0~±49.0~ |
|  | Para. 1 $\uparrow$ | 0.0~±0.0~ | 40.0~±49.0~ | 100.0~±0.0~ | 80.0~±40.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 40.0~±49.0~ |
|  | Para. 2 $\uparrow$ | 0.0~±0.0~ | 60.0~±49.0~ | 100.0~±0.0~ | 80.0~±40.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 20.0~±40.0~ |
|  | Para. 3 $\uparrow$ | 0.0~±0.0~ | 60.0~±49.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 20.0~±40.0~ |
|  | Hop 1 $\uparrow$ | 0.0~±0.0~ | 60.0~±49.0~ | 80.0~±40.0~ | 80.0~±40.0~ | 20.0~±40.0~ | 0.0~±0.0~ | 20.0~±40.0~ |
|  | Hop 2 $\uparrow$ | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
|  | Hop 3 $\uparrow$ | 0.0 | 0.0 | 100.0 | 100.0 | 100.0 | 0.0 | 100.0 |
|  | Abs. 1 $\uparrow$ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ | 100.0~±0.0~ |
|  | Abs. 2 $\uparrow$ | 0.0~±0.0~ | 33.3~±47.1~ | 33.3~±47.1~ | 33.3~±47.1~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | Abs. 3 $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 40.0~±49.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | *scored by* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* |

: Edit quality on llama3-8b. n=5 cases per cell, seed None. All values are percentages, mean ±sd over cases, higher is better throughout. Each benchmark is scored by its own paper's metric — the *scored by* row names it. S is the harmonic mean of efficacy, generalisation and specificity, where a benchmark carries all three. {#tbl:edit-quality-llama3-8b}
