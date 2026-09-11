# EXP-001 — results summary

`EXP-001_m2-em2-b1_2026-08-27` · 2026-08-27T16:11:27 · commit `b43cd6f-dirty` · n=20 · NVIDIA RTX PRO 4000 Blackwell

`rate` = share of probes where p_new > p_old — binary per probe. `magnitude` = mean of (p_new − p_old) — how far, not just whether. Both read **pre → post**.

## gpt2-xl · remedi · counterfact

20 cases

```
                          rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                       pre → post              pre → post        probes
------------------------  -------------------   ----------------------- -------
efficacy                     0.200 → 0.750         -0.0692 → +0.0561         20
generalisation               0.225 → 0.825         -0.0481 → +0.1233         40
specificity ↓                0.190 → 0.190         -0.0778 → -0.0757        200
target_close_neighbour       0.835 → 0.835         +0.0875 → +0.0875        200
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## gpt2-xl · rome · counterfact

20 cases

```
                          rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                       pre → post              pre → post        probes
------------------------  -------------------   ----------------------- -------
efficacy                     0.200 → 1.000         -0.0692 → +0.9306         20
generalisation               0.225 → 0.925         -0.0481 → +0.4583         40
specificity ↓                0.190 → 0.210         -0.0778 → -0.0597        200
target_close_neighbour       0.835 → 0.835         +0.0875 → +0.0932        200
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## llama3-8b · remedi · counterfact

20 cases

```
                          rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                       pre → post              pre → post        probes
------------------------  -------------------   ----------------------- -------
efficacy                     0.150 → 0.800         -0.1147 → +0.0370         20
generalisation               0.125 → 0.700         -0.0874 → +0.0563         40
specificity ↓                0.125 → 0.125         -0.1693 → -0.1682        200
target_close_neighbour       0.915 → 0.915         +0.1772 → +0.1772        200
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## llama3-8b · rome · counterfact

20 cases — **DEGENERATE**

> **18/20 efficacy probes have p_new AND p_old below 0.0001 — the scores below are not meaningful**

```
                          rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                       pre → post              pre → post        probes
------------------------  -------------------   ----------------------- -------
efficacy                     0.150 → 0.450         -0.1147 → +0.0005         20
generalisation               0.125 → 0.450         -0.0874 → -0.0011         40
specificity ↓                0.125 → 0.140         -0.1693 → -0.1406        200
target_close_neighbour       0.915 → 0.920         +0.1772 → +0.1745        200
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

