# EXP-003 — grid

`EXP-003_m2-em6-b5_2026-08-27` · 2026-08-27T18:24:07 · commit `0d4c307-dirty` · n=20 · seed=0 · NVIDIA RTX PRO 4000 Blackwell

59/60 cells completed. **1 failed.**

Efficacy only — the probe that asks whether the edit took at all. `rate` is the share of cases where p_new > p_old; `magnitude` is the mean of (p_new − p_old). Both read **pre → post**.

**A near-zero or negative magnitude means the edit did not take**, whatever the rate says: p_old still wins on average and the rate is reading float noise.

## gpt2-xl

```
method     benchmark             rate               magnitude          flag
---------------------------------------------------------------------  ----------
rome       counterfact      0.250 → 1.000        -0.0747 → +0.9014     
rome       zsre             0.450 → 0.950        +0.0047 → +0.5477     
rome       ripple           0.225 → 0.850        -0.0502 → +0.1175     
rome       mquake           0.425 → 0.858        -0.0123 → +0.2003     
rome       genie            0.250 → 0.900        -0.0949 → +0.3328     

memit      counterfact      0.250 → 1.000        -0.0747 → +0.9274     
memit      zsre             0.450 → 0.950        +0.0047 → +0.8075     
memit      ripple           0.225 → 1.000        -0.0502 → +0.7332     
memit      mquake           0.425 → 0.908        -0.0123 → +0.4706     
memit      genie            0.250 → 1.000        -0.0949 → +0.7936     

grace      counterfact      0.250 → 1.000        -0.0747 → +0.9984     
grace      zsre             0.450 → 0.950        +0.0047 → +0.9369     
grace      ripple           0.225 → 1.000        -0.0502 → +0.9209     
grace      mquake           0.425 → 0.854        -0.0123 → +0.5044     
grace      genie            0.250 → 1.000        -0.0949 → +0.9539     

alphaedit  counterfact      0.250 → 1.000        -0.0747 → +0.9221     
alphaedit  zsre             0.450 → 0.950        +0.0047 → +0.7663     
alphaedit  ripple           0.225 → 1.000        -0.0502 → +0.8141     
alphaedit  mquake           0.425 → 0.867        -0.0123 → +0.4675     
alphaedit  genie            0.250 → 1.000        -0.0949 → +0.8483     

anyedit    counterfact      0.250 → 1.000        -0.0747 → +0.9914     
anyedit    zsre             0.450 → 0.950        +0.0047 → +0.7586     
anyedit    ripple           0.225 → 0.975        -0.0502 → +0.6235     
anyedit    mquake           0.425 → 0.871        -0.0123 → +0.4647     
anyedit    genie            0.250 → 1.000        -0.0949 → +0.8613     

remedi     counterfact      0.250 → 0.800        -0.0747 → +0.0173     
remedi     zsre             0.450 → 0.700        +0.0047 → +0.0319     
remedi     ripple           0.225 → 0.500        -0.0502 → -0.0280     
remedi     mquake           0.425 → 0.567        -0.0123 → +0.0228     
remedi     genie            0.250 → 0.600        -0.0949 → +0.0250     
```

## llama3-8b

```
method     benchmark             rate               magnitude          flag
---------------------------------------------------------------------  ----------
rome       counterfact      0.050 → 0.250        -0.1828 → -0.0016     DEGENERATE
rome       zsre             0.250 → 0.400        -0.0896 → -0.0019     DEGENERATE
rome       ripple           0.050 → 0.475        -0.2043 → -0.0030     
rome       mquake           0.250 → 0.613        -0.1140 → +0.0189     
rome       genie            0.100 → 0.250        -0.3000 → -0.0044     

memit      counterfact      0.050 → 0.900        -0.1828 → +0.4858     
memit      zsre             0.250 → 0.900        -0.0896 → +0.2843     
memit      ripple           0.050 → 0.775        -0.2043 → +0.0809     
memit      mquake           0.250 → 0.779        -0.1140 → +0.1796     
memit      genie            0.100 → 0.850        -0.3000 → +0.2375     

grace      counterfact      0.050 → 1.000        -0.1828 → +0.9998     
grace      zsre             0.250 → 0.950        -0.0896 → +0.8264     
grace      ripple           0.050 → 1.000        -0.2043 → +0.8913     
grace      mquake           0.250 → 0.842        -0.1140 → +0.4852     
grace      genie            0.100 → 1.000        -0.3000 → +0.9841     

alphaedit  counterfact      0.050 → 0.400        -0.1828 → +0.0130     
alphaedit  zsre             0.250 → 0.500        -0.0896 → +0.0175     
alphaedit  ripple           0.050 → 0.275        -0.2043 → -0.1069     
alphaedit  mquake           0.250 → 0.675        -0.1140 → +0.0890     
alphaedit  genie            0.100 → 0.200        -0.3000 → -0.2400     

anyedit    counterfact      0.050 → 0.300        -0.1828 → -0.0020     
anyedit    zsre             0.250 → 0.450        -0.0896 → +0.0278     
anyedit    ripple           0.050 → 0.550        -0.2043 → -0.0310     
anyedit    mquake           0.250 → 0.642        -0.1140 → +0.0386     
anyedit    genie            0.100 → 0.600        -0.3000 → -0.0680     

remedi     counterfact      0.050 → 0.650        -0.1828 → +0.0206     
remedi     zsre             0.250 → 0.550        -0.0896 → -0.0197     
remedi     ripple           0.050 → 0.475        -0.2043 → -0.0179     
remedi     mquake             — FAILED —                               IndexError: index 15 is out of bounds fo
remedi     genie            0.100 → 0.300        -0.3000 → -0.0584     
```

