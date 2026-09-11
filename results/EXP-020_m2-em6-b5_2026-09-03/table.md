| Benchmark | Probe | Pre-edit | ROME | MEMIT | AlphaEdit | AnyEdit | GRACE | REMEDI |
|:--------------|:--------------|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
| **CounterFact** | Eff. $\uparrow$ | 24.0~±42.7~ | 100.0~±0.0~ | 98.0~±14.0~ | 100.0~±0.0~ | 92.0~±27.1~ | 100.0~±0.0~ | 72.0~±44.9~ |
|  | Gen. $\uparrow$ | 23.0~±34.9~ | 90.0~±22.4~ | 88.0~±27.5~ | 100.0~±0.0~ | 35.0~±40.3~ | 23.0~±34.9~ | 71.0~±40.1~ |
|  | Spe. $\uparrow$ | 72.4~±32.1~ | 68.4~±33.1~ | 67.8~±33.6~ | 64.8~±33.5~ | 55.0~±34.4~ | 71.8~±32.2~ | 71.4~±32.0~ |
|  | **S** $\uparrow$ | **30.3** | **84.0** | **82.6** | **84.7** | **52.1** | **44.5** | **71.5** |
|  | *scored by* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* |
| **zsRE** | Eff. $\uparrow$ | 18.9~±23.3~ | 66.7~±31.1~ | 87.0~±27.4~ | 90.8~±23.7~ | 60.1~±39.2~ | 97.1~±14.6~ | 18.7~±24.3~ |
|  | Gen. $\uparrow$ | 15.2~±21.9~ | 61.4~±36.4~ | 63.0~±38.6~ | 79.5~±32.7~ | 24.4~±30.5~ | 15.2~±21.9~ | 18.0~±23.1~ |
|  | Spe. $\uparrow$ | 28.2~±27.5~ | 27.3~±26.9~ | 27.3~±26.9~ | 27.4~±26.8~ | 27.8~±26.9~ | 28.2~±27.5~ | 28.2~±27.5~ |
|  | **S** $\uparrow$ | **19.5** | **44.2** | **46.9** | **49.9** | **32.1** | **27.0** | **20.8** |
|  | *scored by* | *exact match* | *exact match* | *exact match* | *exact match* | *exact match* | *exact match* | *exact match* |
| **RippleEdits** | Eff. $\uparrow$ | 0.0~±0.0~ | 10.5~±30.7~ | 60.0~±49.0~ | 74.7~±43.5~ | 16.8~±37.4~ | 82.1~±38.3~ | 0.0~±0.0~ |
|  | Aliasing $\uparrow$ | 0.0~±0.0~ | 11.5~±31.9~ | 25.5~±41.7~ | 45.4~±46.4~ | 11.7~±31.4~ | 22.9~±38.0~ | 0.0~±0.0~ |
|  | Logical $\uparrow$ | 3.1~±9.2~ | 3.6~±11.0~ | 3.0~±11.0~ | 6.2~±15.8~ | 3.9~±11.7~ | 3.1~±9.2~ | 0.0~±0.0~ |
|  | Comp. I $\uparrow$ | 1.9~±8.7~ | 3.7~±9.7~ | 3.3~±10.1~ | 9.4~±16.0~ | 2.3~±9.0~ | 1.9~±8.7~ | 3.3~±11.7~ |
|  | Comp. II $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 5.6~±18.4~ | 8.3~±27.6~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | Rel. spec. $\uparrow$ | 8.0~±13.3~ | 6.7~±11.5~ | 7.1~±13.3~ | 4.1~±10.8~ | 10.2~±14.1~ | 8.0~±13.3~ | 9.6~±15.4~ |
|  | Preservation $\uparrow$ | 4.7~±21.1~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 4.7~±21.1~ | 4.7~±21.1~ | 2.3~±15.1~ |
|  | *scored by* | *containment* | *containment* | *containment* | *containment* | *containment* | *containment* | *containment* |
| **MQuAKE** | Eff. $\uparrow$ | 22.9~±20.5~ | 72.2~±25.0~ | 80.9~±27.4~ | 98.0~±6.4~ | 81.6~±19.8~ | 100.0~±0.0~ | 28.3~±22.0~ |
|  | Single hop $\uparrow$ | 33.8~±22.1~ | 68.5~±22.6~ | 74.2~±24.0~ | 85.1~±19.4~ | 75.0~±19.9~ | 88.7~±17.0~ | 37.8~±21.9~ |
|  | Multi hop $\uparrow$ | 2.0~±7.9~ | 1.3~±6.5~ | 6.7~±18.9~ | 4.7~±13.3~ | 2.7~±11.2~ | 2.0~±7.9~ | 2.7~±9.0~ |
|  | *scored by* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* |
| **GENIE** | Eff. $\uparrow$ | 28.0~±44.9~ | 98.0~±14.0~ | 90.0~±30.0~ | 100.0~±0.0~ | 78.0~±41.4~ | 100.0~±0.0~ | 50.0~±50.0~ |
|  | Para. 1 $\uparrow$ | 18.0~±38.4~ | 64.0~±48.0~ | 70.0~±45.8~ | 92.0~±27.1~ | 20.0~±40.0~ | 18.0~±38.4~ | 46.0~±49.8~ |
|  | Para. 2 $\uparrow$ | 22.0~±41.4~ | 76.0~±42.7~ | 74.0~±43.9~ | 92.0~±27.1~ | 22.0~±41.4~ | 22.0~±41.4~ | 46.0~±49.8~ |
|  | Para. 3 $\uparrow$ | 22.0~±41.4~ | 78.0~±41.4~ | 74.0~±43.9~ | 92.0~±27.1~ | 24.0~±42.7~ | 22.0~±41.4~ | 50.0~±50.0~ |
|  | Hop 1 $\uparrow$ | 25.0~±43.3~ | 37.5~±48.4~ | 37.5~±48.4~ | 47.5~±49.9~ | 25.0~±43.3~ | 25.0~±43.3~ | 40.0~±49.0~ |
|  | Hop 2 $\uparrow$ | 55.6~±49.7~ | 77.8~±41.6~ | 88.9~±31.4~ | 77.8~±41.6~ | 44.4~±49.7~ | 55.6~±49.7~ | 66.7~±47.1~ |
|  | Hop 3 $\uparrow$ | 75.0~±43.3~ | 75.0~±43.3~ | 100.0~±0.0~ | 50.0~±50.0~ | 100.0~±0.0~ | 75.0~±43.3~ | 100.0~±0.0~ |
|  | Abs. 1 $\uparrow$ | 86.7~±34.0~ | 83.3~±37.3~ | 86.7~±34.0~ | 86.7~±34.0~ | 86.7~±34.0~ | 86.7~±34.0~ | 90.0~±30.0~ |
|  | Abs. 2 $\uparrow$ | 0.0~±0.0~ | 25.9~±43.8~ | 25.9~±43.8~ | 59.3~±49.1~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | Abs. 3 $\uparrow$ | 0.0~±0.0~ | 6.0~±23.7~ | 4.0~±19.6~ | 12.0~±32.5~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | *scored by* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* |

: Edit quality on gpt2-xl. n=50 cases per cell, seed 0. All values are percentages, mean ±sd over cases, higher is better throughout. Each benchmark is scored by its own paper's metric — the *scored by* row names it. S is the harmonic mean of efficacy, generalisation and specificity, where a benchmark carries all three. {#tbl:edit-quality-gpt2-xl}

| Benchmark | Probe | Pre-edit | ROME | MEMIT | AlphaEdit | AnyEdit | GRACE | REMEDI |
|:--------------|:--------------|----------:|----------:|----------:|----------:|----------:|----------:|----------:|
| **CounterFact** | Eff. $\uparrow$ | 4.0~±19.6~ | 100.0~±0.0~ | 98.0~±14.0~ | 92.0~±27.1~ | 96.0~±19.6~ | 100.0~±0.0~ | 88.0~±32.5~ |
|  | Gen. $\uparrow$ | 10.0~±24.5~ | 100.0~±0.0~ | 80.0~±33.2~ | 67.0~±43.1~ | 29.0~±38.8~ | 10.0~±24.5~ | 68.0~±38.4~ |
|  | Spe. $\uparrow$ | 85.4~±21.7~ | 60.8~±33.8~ | 78.6~±28.1~ | 81.2~±25.8~ | 68.2~±30.0~ | 85.2~±21.6~ | 84.2~±21.9~ |
|  | **S** $\uparrow$ | **8.3** | **82.3** | **84.7** | **78.7** | **50.4** | **24.6** | **79.1** |
|  | *scored by* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* | *p(new) > p(old)* |
| **zsRE** | Eff. $\uparrow$ | 25.4~±25.4~ | 65.1~±30.0~ | 93.3~±18.8~ | 84.9~±27.4~ | 90.7~±23.1~ | 95.0~±17.1~ | 28.2~±26.1~ |
|  | Gen. $\uparrow$ | 21.7~±23.8~ | 61.7~±31.4~ | 70.6~±34.6~ | 64.6~±35.4~ | 56.9~±35.9~ | 28.2~±31.6~ | 24.8~±26.7~ |
|  | Spe. $\uparrow$ | 43.2~±25.7~ | 41.4~±27.1~ | 43.0~±26.8~ | 43.0~±26.8~ | 44.0~±25.9~ | 43.2~±25.7~ | 43.2~±25.7~ |
|  | **S** $\uparrow$ | **27.6** | **53.8** | **62.3** | **59.4** | **58.4** | **43.4** | **30.4** |
|  | *scored by* | *exact match* | *exact match* | *exact match* | *exact match* | *exact match* | *exact match* | *exact match* |
| **RippleEdits** | Eff. $\uparrow$ | 0.0~±0.0~ | 12.6~±33.2~ | 84.2~±36.5~ | 69.5~±46.1~ | 77.9~±41.5~ | 76.8~±42.2~ | 1.1~±10.2~ |
|  | Aliasing $\uparrow$ | 0.0~±0.0~ | 9.0~±27.7~ | 40.2~±45.3~ | 22.7~±38.8~ | 55.2~±45.3~ | 15.7~±34.0~ | 1.1~±10.7~ |
|  | Logical $\uparrow$ | 3.3~±9.5~ | 5.7~±17.3~ | 21.0~±33.6~ | 13.5~±28.0~ | 9.3~±21.8~ | 3.3~±9.5~ | 5.1~±12.9~ |
|  | Comp. I $\uparrow$ | 2.9~±9.8~ | 6.7~±13.3~ | 13.3~±15.4~ | 10.0~±15.5~ | 5.3~±13.3~ | 2.9~±9.8~ | 1.7~±5.7~ |
|  | Comp. II $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 2.8~±9.2~ | 0.0~±0.0~ | 11.7~±28.8~ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | Rel. spec. $\uparrow$ | 37.3~±26.8~ | 16.8~±21.6~ | 25.3~±21.8~ | 30.3~±25.8~ | 31.5~±25.0~ | 37.3~±26.8~ | 26.3~±22.2~ |
|  | Preservation $\uparrow$ | 16.3~±36.9~ | 0.0~±0.0~ | 0.0~±0.0~ | 4.7~±21.1~ | 7.0~±25.5~ | 16.3~±36.9~ | 7.0~±25.5~ |
|  | *scored by* | *containment* | *containment* | *containment* | *containment* | *containment* | *containment* | *containment* |
| **MQuAKE** | Eff. $\uparrow$ | 25.3~±21.8~ | 75.7~±26.0~ | 97.7~±6.0~ | 86.4~±19.1~ | 96.7~±8.6~ | 99.2~±3.4~ | 43.2~±27.1~ |
|  | Single hop $\uparrow$ | 39.7~±24.1~ | 74.1~±23.0~ | 91.6~±12.6~ | 83.5~±18.3~ | 91.4~±13.8~ | 92.3~±12.5~ | 52.1~±25.3~ |
|  | Multi hop $\uparrow$ | 0.7~±4.7~ | 6.0~±18.5~ | 7.3~±18.0~ | 4.7~±13.3~ | 4.0~±17.2~ | 0.7~±4.7~ | 2.0~±10.3~ |
|  | *scored by* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* | *exact match, containment* |
| **GENIE** | Eff. $\uparrow$ | 8.0~±27.1~ | 92.0~±27.1~ | 98.0~±14.0~ | 96.0~±19.6~ | 98.0~±14.0~ | 100.0~±0.0~ | 28.0~±44.9~ |
|  | Para. 1 $\uparrow$ | 4.0~±19.6~ | 84.0~±36.7~ | 76.0~±42.7~ | 64.0~±48.0~ | 2.0~±14.0~ | 4.0~±19.6~ | 26.0~±43.9~ |
|  | Para. 2 $\uparrow$ | 2.0~±14.0~ | 78.0~±41.4~ | 88.0~±32.5~ | 76.0~±42.7~ | 4.0~±19.6~ | 2.0~±14.0~ | 24.0~±42.7~ |
|  | Para. 3 $\uparrow$ | 8.0~±27.1~ | 82.0~±38.4~ | 82.0~±38.4~ | 76.0~±42.7~ | 8.0~±27.1~ | 8.0~±27.1~ | 30.0~±45.8~ |
|  | Hop 1 $\uparrow$ | 41.7~±49.3~ | 61.1~±48.7~ | 66.7~±47.1~ | 72.2~±44.8~ | 41.7~±49.3~ | 41.7~±49.3~ | 47.2~±49.9~ |
|  | Hop 2 $\uparrow$ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ | 0.0~±0.0~ |
|  | Abs. 1 $\uparrow$ | 94.3~±23.2~ | 91.4~±28.0~ | 94.3~±23.2~ | 94.3~±23.2~ | 94.3~±23.2~ | 94.3~±23.2~ | 91.4~±28.0~ |
|  | Abs. 2 $\uparrow$ | 2.9~±16.7~ | 45.7~±49.8~ | 45.7~±49.8~ | 40.0~±49.0~ | 2.9~±16.7~ | 2.9~±16.7~ | 11.4~±31.8~ |
|  | Abs. 3 $\uparrow$ | 2.0~±14.0~ | 18.0~±38.4~ | 34.0~±47.4~ | 30.0~±45.8~ | 2.0~±14.0~ | 2.0~±14.0~ | 2.0~±14.0~ |
|  | *scored by* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* | *containment, p(new) > p(old)* |

: Edit quality on llama3-8b. n=50 cases per cell, seed 0. All values are percentages, mean ±sd over cases, higher is better throughout. Each benchmark is scored by its own paper's metric — the *scored by* row names it. S is the harmonic mean of efficacy, generalisation and specificity, where a benchmark carries all three. {#tbl:edit-quality-llama3-8b}
