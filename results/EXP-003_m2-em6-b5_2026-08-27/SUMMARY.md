# EXP-003 — results summary

`EXP-003_m2-em6-b5_2026-08-27` · 2026-08-27T18:24:07 · commit `0d4c307-dirty` · n=20 · NVIDIA RTX PRO 4000 Blackwell

`rate` = share of probes where p_new > p_old — binary per probe. `magnitude` = mean of (p_new − p_old) — how far, not just whether. Both read **pre → post**.

## gpt2-xl · alphaedit · counterfact

20 cases

```
                          rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                       pre → post              pre → post        probes
------------------------  -------------------   ----------------------- -------
efficacy                     0.250 → 1.000         -0.0747 → +0.9221         20
generalisation               0.125 → 1.000         -0.0385 → +0.4787         40
specificity ↓                0.295 → 0.430         -0.0454 → +0.0157        200
target_close_neighbour       0.720 → 0.775         +0.0743 → +0.0939        200
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## gpt2-xl · alphaedit · genie

20 cases

```
                rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category             pre → post              pre → post        probes
--------------  -------------------   ----------------------- -------
abstract_1         0.500 → 0.583         +0.0252 → +0.0382         12
abstract_2  *      0.000 → 0.350         +0.0000 → +0.3500         20
abstract_3  *      0.000 → 0.000         +0.0000 → +0.0000         14
efficacy           0.250 → 1.000         -0.0949 → +0.8483         20
hop_1              0.300 → 0.300         -0.0306 → +0.0504         10
hop_2              0.000 → 0.000         -0.1979 → -0.0338          3
hop_3              0.000 → 0.000         -0.2564 → -0.2088          1
paraphrase_1       0.250 → 0.900         -0.0773 → +0.3624         20
paraphrase_2       0.200 → 0.800         -0.0951 → +0.3750         20
paraphrase_3       0.300 → 0.900         -0.0550 → +0.3466         20
```

`*` generation-scored: p_new/p_old are 1.0/0.0 match flags, not probabilities.

## gpt2-xl · alphaedit · mquake

20 cases

```
              rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category           pre → post              pre → post        probes
------------  -------------------   ----------------------- -------
efficacy         0.425 → 0.867         -0.0123 → +0.4675         39
multihop  *      0.000 → 0.000         -0.1167 → -0.1500         60
single_hop       0.558 → 0.833         +0.0097 → +0.3518         55
```

`*` generation-scored: p_new/p_old are 1.0/0.0 match flags, not probabilities.

## gpt2-xl · alphaedit · ripple

40 cases

```
                               rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                            pre → post              pre → post        probes
-----------------------------  -------------------   ----------------------- -------
efficacy                          0.225 → 1.000         -0.0502 → +0.8141         40
ripple_aliasing                   0.211 → 0.829         -0.0588 → +0.4306         94
ripple_compositional_i            0.417 → 1.000         -0.0216 → +0.4853         77
ripple_compositional_ii           0.250 → 0.500         -0.0574 → +0.1503         16
ripple_logical                    0.697 → 1.000         +0.0100 → +0.3340         18
ripple_preservation               0.833 → 1.000         +0.1326 → +0.6540         18
ripple_relation_specificity ↓     0.356 → 0.966         -0.0135 → +0.4051        159
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## gpt2-xl · alphaedit · zsre

20 cases

```
                  rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category               pre → post              pre → post        probes
----------------  -------------------   ----------------------- -------
efficacy             0.450 → 0.950         +0.0047 → +0.7663         20
generalisation       0.450 → 0.950         +0.0033 → +0.6076         20
specificity ↓        0.450 → 0.450         +0.0007 → +0.0007         20
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## gpt2-xl · anyedit · counterfact

20 cases

```
                          rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                       pre → post              pre → post        probes
------------------------  -------------------   ----------------------- -------
efficacy                     0.250 → 1.000         -0.0747 → +0.9914         20
generalisation               0.125 → 0.275         -0.0385 → +0.0345         40
specificity ↓                0.295 → 0.490         -0.0454 → +0.1330        200
target_close_neighbour       0.720 → 0.865         +0.0743 → +0.2887        200
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## gpt2-xl · anyedit · genie

20 cases

```
                rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category             pre → post              pre → post        probes
--------------  -------------------   ----------------------- -------
abstract_1         0.500 → 0.500         +0.0252 → +0.0206         12
abstract_2  *      0.000 → 0.000         +0.0000 → -0.0500         20
abstract_3  *      0.000 → 0.000         +0.0000 → +0.0000         14
efficacy           0.250 → 1.000         -0.0949 → +0.8613         20
hop_1              0.300 → 0.300         -0.0306 → -0.0206         10
hop_2              0.000 → 0.000         -0.1979 → -0.1917          3
hop_3              0.000 → 0.000         -0.2564 → -0.3049          1
paraphrase_1       0.250 → 0.250         -0.0773 → -0.0736         20
paraphrase_2       0.200 → 0.200         -0.0951 → -0.0979         20
paraphrase_3       0.300 → 0.300         -0.0550 → -0.0540         20
```

`*` generation-scored: p_new/p_old are 1.0/0.0 match flags, not probabilities.

## gpt2-xl · anyedit · mquake

20 cases

```
              rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category           pre → post              pre → post        probes
------------  -------------------   ----------------------- -------
efficacy         0.425 → 0.871         -0.0123 → +0.4647         39
multihop  *      0.000 → 0.000         -0.1167 → -0.1000         60
single_hop       0.558 → 0.838         +0.0097 → +0.3482         55
```

`*` generation-scored: p_new/p_old are 1.0/0.0 match flags, not probabilities.

## gpt2-xl · anyedit · ripple

40 cases

```
                               rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                            pre → post              pre → post        probes
-----------------------------  -------------------   ----------------------- -------
efficacy                          0.225 → 0.975         -0.0502 → +0.6235         40
ripple_aliasing                   0.211 → 0.834         -0.0588 → +0.3807         94
ripple_compositional_i            0.417 → 0.831         -0.0216 → +0.1416         77
ripple_compositional_ii           0.250 → 0.250         -0.0574 → -0.0353         16
ripple_logical                    0.697 → 0.955         +0.0100 → +0.1280         18
ripple_preservation               0.833 → 0.889         +0.1326 → +0.3747         18
ripple_relation_specificity ↓     0.356 → 0.631         -0.0135 → +0.0499        159
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## gpt2-xl · anyedit · zsre

20 cases

```
                  rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category               pre → post              pre → post        probes
----------------  -------------------   ----------------------- -------
efficacy             0.450 → 0.950         +0.0047 → +0.7586         20
generalisation       0.450 → 0.800         +0.0033 → +0.2305         20
specificity ↓        0.450 → 0.450         +0.0007 → +0.0007         20
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## gpt2-xl · grace · counterfact

20 cases

```
                          rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                       pre → post              pre → post        probes
------------------------  -------------------   ----------------------- -------
efficacy                     0.250 → 1.000         -0.0747 → +0.9984         20
generalisation               0.125 → 0.125         -0.0385 → -0.0385         40
specificity ↓                0.295 → 0.305         -0.0454 → -0.0202        200
target_close_neighbour       0.720 → 0.725         +0.0743 → +0.0943        200
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## gpt2-xl · grace · genie

20 cases

```
                rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category             pre → post              pre → post        probes
--------------  -------------------   ----------------------- -------
abstract_1         0.500 → 0.500         +0.0252 → +0.0252         12
abstract_2  *      0.000 → 0.000         +0.0000 → +0.0000         20
abstract_3  *      0.000 → 0.000         +0.0000 → +0.0000         14
efficacy           0.250 → 1.000         -0.0949 → +0.9539         20
hop_1              0.300 → 0.300         -0.0306 → -0.0306         10
hop_2              0.000 → 0.000         -0.1979 → -0.1979          3
hop_3              0.000 → 0.000         -0.2564 → -0.2564          1
paraphrase_1       0.250 → 0.250         -0.0773 → -0.0773         20
paraphrase_2       0.200 → 0.200         -0.0951 → -0.0951         20
paraphrase_3       0.300 → 0.300         -0.0550 → -0.0550         20
```

`*` generation-scored: p_new/p_old are 1.0/0.0 match flags, not probabilities.

## gpt2-xl · grace · mquake

20 cases

```
              rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category           pre → post              pre → post        probes
------------  -------------------   ----------------------- -------
efficacy         0.425 → 0.854         -0.0123 → +0.5044         39
multihop  *      0.000 → 0.000         -0.1167 → -0.1167         60
single_hop       0.558 → 0.821         +0.0097 → +0.3761         55
```

`*` generation-scored: p_new/p_old are 1.0/0.0 match flags, not probabilities.

## gpt2-xl · grace · ripple

40 cases

```
                               rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                            pre → post              pre → post        probes
-----------------------------  -------------------   ----------------------- -------
efficacy                          0.225 → 1.000         -0.0502 → +0.9209         40
ripple_aliasing                   0.211 → 0.437         -0.0588 → +0.1521         94
ripple_compositional_i            0.417 → 0.440         -0.0216 → -0.0160         77
ripple_compositional_ii           0.250 → 0.250         -0.0574 → -0.0574         16
ripple_logical                    0.697 → 0.697         +0.0100 → +0.0100         18
ripple_preservation               0.833 → 0.833         +0.1326 → +0.1326         18
ripple_relation_specificity ↓     0.356 → 0.356         -0.0135 → -0.0074        159
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## gpt2-xl · grace · zsre

20 cases

```
                  rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category               pre → post              pre → post        probes
----------------  -------------------   ----------------------- -------
efficacy             0.450 → 0.950         +0.0047 → +0.9369         20
generalisation       0.450 → 0.450         +0.0033 → +0.0033         20
specificity ↓        0.450 → 0.450         +0.0007 → +0.0007         20
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## gpt2-xl · memit · counterfact

20 cases

```
                          rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                       pre → post              pre → post        probes
------------------------  -------------------   ----------------------- -------
efficacy                     0.250 → 1.000         -0.0747 → +0.9274         20
generalisation               0.125 → 0.975         -0.0385 → +0.4774         40
specificity ↓                0.295 → 0.370         -0.0454 → +0.0053        200
target_close_neighbour       0.720 → 0.740         +0.0743 → +0.0823        200
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## gpt2-xl · memit · genie

20 cases

```
                rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category             pre → post              pre → post        probes
--------------  -------------------   ----------------------- -------
abstract_1         0.500 → 0.667         +0.0252 → +0.0205         12
abstract_2  *      0.000 → 0.250         +0.0000 → +0.2000         20
abstract_3  *      0.000 → 0.000         +0.0000 → +0.0000         14
efficacy           0.250 → 1.000         -0.0949 → +0.7936         20
hop_1              0.300 → 0.400         -0.0306 → +0.0480         10
hop_2              0.000 → 0.333         -0.1979 → -0.0536          3
hop_3              0.000 → 0.000         -0.2564 → -0.2122          1
paraphrase_1       0.250 → 0.700         -0.0773 → +0.2890         20
paraphrase_2       0.200 → 0.700         -0.0951 → +0.3608         20
paraphrase_3       0.300 → 0.750         -0.0550 → +0.2502         20
```

`*` generation-scored: p_new/p_old are 1.0/0.0 match flags, not probabilities.

## gpt2-xl · memit · mquake

20 cases

```
              rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category           pre → post              pre → post        probes
------------  -------------------   ----------------------- -------
efficacy         0.425 → 0.908         -0.0123 → +0.4706         39
multihop  *      0.000 → 0.017         -0.1167 → -0.1500         60
single_hop       0.558 → 0.867         +0.0097 → +0.3537         55
```

`*` generation-scored: p_new/p_old are 1.0/0.0 match flags, not probabilities.

## gpt2-xl · memit · ripple

40 cases

```
                               rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                            pre → post              pre → post        probes
-----------------------------  -------------------   ----------------------- -------
efficacy                          0.225 → 1.000         -0.0502 → +0.7332         40
ripple_aliasing                   0.211 → 0.766         -0.0588 → +0.2658         94
ripple_compositional_i            0.417 → 0.981         -0.0216 → +0.3349         77
ripple_compositional_ii           0.250 → 0.500         -0.0574 → +0.1051         16
ripple_logical                    0.697 → 1.000         +0.0100 → +0.2766         18
ripple_preservation               0.833 → 1.000         +0.1326 → +0.5755         18
ripple_relation_specificity ↓     0.356 → 0.914         -0.0135 → +0.2285        159
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## gpt2-xl · memit · zsre

20 cases

```
                  rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category               pre → post              pre → post        probes
----------------  -------------------   ----------------------- -------
efficacy             0.450 → 0.950         +0.0047 → +0.8075         20
generalisation       0.450 → 0.950         +0.0033 → +0.5790         20
specificity ↓        0.450 → 0.450         +0.0007 → +0.0007         20
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## gpt2-xl · remedi · counterfact

20 cases

```
                          rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                       pre → post              pre → post        probes
------------------------  -------------------   ----------------------- -------
efficacy                     0.250 → 0.800         -0.0747 → +0.0173         20
generalisation               0.125 → 0.825         -0.0385 → +0.0835         40
specificity ↓                0.295 → 0.295         -0.0454 → -0.0454        200
target_close_neighbour       0.720 → 0.720         +0.0743 → +0.0743        200
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## gpt2-xl · remedi · genie

20 cases

```
                rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category             pre → post              pre → post        probes
--------------  -------------------   ----------------------- -------
abstract_1         0.500 → 0.583         +0.0252 → +0.0137         12
abstract_2  *      0.000 → 0.100         +0.0000 → +0.0500         20
abstract_3  *      0.000 → 0.000         +0.0000 → +0.0000         14
efficacy           0.250 → 0.600         -0.0949 → +0.0250         20
hop_1              0.300 → 0.400         -0.0306 → +0.0340         10
hop_2              0.000 → 0.000         -0.1979 → -0.1112          3
hop_3              0.000 → 0.000         -0.2564 → -0.1546          1
paraphrase_1       0.250 → 0.500         -0.0773 → +0.0133         20
paraphrase_2       0.200 → 0.650         -0.0951 → +0.0474         20
paraphrase_3       0.300 → 0.650         -0.0550 → +0.0338         20
```

`*` generation-scored: p_new/p_old are 1.0/0.0 match flags, not probabilities.

## gpt2-xl · remedi · mquake

20 cases

```
              rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category           pre → post              pre → post        probes
------------  -------------------   ----------------------- -------
efficacy         0.425 → 0.567         -0.0123 → +0.0228         39
multihop  *      0.000 → 0.000         -0.1167 → -0.0833         60
single_hop       0.558 → 0.658         +0.0097 → +0.0346         55
```

`*` generation-scored: p_new/p_old are 1.0/0.0 match flags, not probabilities.

## gpt2-xl · remedi · ripple

40 cases

```
                               rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                            pre → post              pre → post        probes
-----------------------------  -------------------   ----------------------- -------
efficacy                          0.225 → 0.500         -0.0502 → -0.0280         40
ripple_aliasing                   0.211 → 0.289         -0.0588 → -0.0564         94
ripple_compositional_i            0.417 → 0.570         -0.0216 → -0.0056         77
ripple_compositional_ii           0.250 → 0.250         -0.0574 → -0.0574         16
ripple_logical                    0.697 → 0.773         +0.0100 → +0.0168         18
ripple_preservation               0.833 → 0.944         +0.1326 → +0.2111         18
ripple_relation_specificity ↓     0.356 → 0.592         -0.0135 → -0.0034        159
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## gpt2-xl · remedi · zsre

20 cases

```
                  rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category               pre → post              pre → post        probes
----------------  -------------------   ----------------------- -------
efficacy             0.450 → 0.700         +0.0047 → +0.0319         20
generalisation       0.450 → 0.700         +0.0033 → +0.0215         20
specificity ↓        0.450 → 0.450         +0.0007 → +0.0007         20
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## gpt2-xl · rome · counterfact

20 cases

```
                          rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                       pre → post              pre → post        probes
------------------------  -------------------   ----------------------- -------
efficacy                     0.250 → 1.000         -0.0747 → +0.9014         20
generalisation               0.125 → 0.950         -0.0385 → +0.4990         40
specificity ↓                0.295 → 0.355         -0.0454 → -0.0147        200
target_close_neighbour       0.720 → 0.725         +0.0743 → +0.0785        200
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## gpt2-xl · rome · genie

20 cases

```
                rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category             pre → post              pre → post        probes
--------------  -------------------   ----------------------- -------
abstract_1         0.500 → 0.583         +0.0252 → +0.0017         12
abstract_2  *      0.000 → 0.150         +0.0000 → +0.1000         20
abstract_3  *      0.000 → 0.000         +0.0000 → +0.0000         14
efficacy           0.250 → 0.900         -0.0949 → +0.3328         20
hop_1              0.300 → 0.300         -0.0306 → +0.0083         10
hop_2              0.000 → 0.000         -0.1979 → -0.0523          3
hop_3              0.000 → 0.000         -0.2564 → -0.2167          1
paraphrase_1       0.250 → 0.500         -0.0773 → +0.0706         20
paraphrase_2       0.200 → 0.600         -0.0951 → +0.1092         20
paraphrase_3       0.300 → 0.650         -0.0550 → +0.0789         20
```

`*` generation-scored: p_new/p_old are 1.0/0.0 match flags, not probabilities.

## gpt2-xl · rome · mquake

20 cases

```
              rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category           pre → post              pre → post        probes
------------  -------------------   ----------------------- -------
efficacy         0.425 → 0.858         -0.0123 → +0.2003         39
multihop  *      0.000 → 0.000         -0.1167 → -0.0833         60
single_hop       0.558 → 0.808         +0.0097 → +0.1602         55
```

`*` generation-scored: p_new/p_old are 1.0/0.0 match flags, not probabilities.

## gpt2-xl · rome · ripple

40 cases

```
                               rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                            pre → post              pre → post        probes
-----------------------------  -------------------   ----------------------- -------
efficacy                          0.225 → 0.850         -0.0502 → +0.1175         40
ripple_aliasing                   0.211 → 0.574         -0.0588 → +0.0330         94
ripple_compositional_i            0.417 → 0.778         -0.0216 → +0.1400         77
ripple_compositional_ii           0.250 → 0.250         -0.0574 → -0.0313         16
ripple_logical                    0.697 → 1.000         +0.0100 → +0.0796         18
ripple_preservation               0.833 → 0.944         +0.1326 → +0.2908         18
ripple_relation_specificity ↓     0.356 → 0.659         -0.0135 → +0.0637        159
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## gpt2-xl · rome · zsre

20 cases

```
                  rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category               pre → post              pre → post        probes
----------------  -------------------   ----------------------- -------
efficacy             0.450 → 0.950         +0.0047 → +0.5477         20
generalisation       0.450 → 0.850         +0.0033 → +0.4937         20
specificity ↓        0.450 → 0.450         +0.0007 → +0.0007         20
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## llama3-8b · alphaedit · counterfact

20 cases

```
                          rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                       pre → post              pre → post        probes
------------------------  -------------------   ----------------------- -------
efficacy                     0.050 → 0.400         -0.1828 → +0.0130         20
generalisation               0.100 → 0.275         -0.1231 → -0.0367         40
specificity ↓                0.145 → 0.155         -0.1244 → -0.1266        200
target_close_neighbour       0.850 → 0.850         +0.1533 → +0.1573        200
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## llama3-8b · alphaedit · genie

20 cases

```
                rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category             pre → post              pre → post        probes
--------------  -------------------   ----------------------- -------
abstract_1         0.333 → 0.417         -0.0335 → -0.0274         12
abstract_2  *      0.000 → 0.000         -0.2000 → -0.1500         20
abstract_3  *      0.000 → 0.000         -0.0714 → -0.0714         14
efficacy           0.100 → 0.200         -0.3000 → -0.2400         20
hop_1              0.300 → 0.300         -0.0627 → -0.0851         10
hop_2              0.000 → 0.333         -0.2541 → -0.0711          3
hop_3              0.000 → 0.000         -0.1250 → -0.0382          1
paraphrase_1       0.100 → 0.150         -0.3369 → -0.2939         20
paraphrase_2       0.100 → 0.200         -0.2914 → -0.2080         20
paraphrase_3       0.100 → 0.200         -0.2509 → -0.2225         20
```

`*` generation-scored: p_new/p_old are 1.0/0.0 match flags, not probabilities.

## llama3-8b · alphaedit · mquake

20 cases

```
              rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category           pre → post              pre → post        probes
------------  -------------------   ----------------------- -------
efficacy         0.250 → 0.675         -0.1140 → +0.0890         39
multihop  *      0.000 → 0.000         -0.1667 → -0.1000         60
single_hop       0.433 → 0.625         -0.0617 → +0.0823         55
```

`*` generation-scored: p_new/p_old are 1.0/0.0 match flags, not probabilities.

## llama3-8b · alphaedit · ripple

40 cases

```
                               rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                            pre → post              pre → post        probes
-----------------------------  -------------------   ----------------------- -------
efficacy                          0.050 → 0.275         -0.2043 → -0.1069         40
ripple_aliasing                   0.166 → 0.175         -0.1752 → -0.1592         94
ripple_compositional_i            0.184 → 0.256         -0.0712 → -0.0440         77
ripple_compositional_ii           0.250 → 0.250         -0.0849 → -0.0802         16
ripple_logical                    0.455 → 0.455         +0.0370 → +0.0352         18
ripple_preservation               0.722 → 0.667         +0.0622 → +0.0701         18
ripple_relation_specificity ↓     0.325 → 0.401         -0.0237 → -0.0183        159
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## llama3-8b · alphaedit · zsre

20 cases

```
                  rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category               pre → post              pre → post        probes
----------------  -------------------   ----------------------- -------
efficacy             0.250 → 0.500         -0.0896 → +0.0175         20
generalisation       0.350 → 0.600         -0.0484 → +0.0086         20
specificity ↓        0.550 → 0.550         +0.0003 → +0.0003         20
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## llama3-8b · anyedit · counterfact

20 cases

```
                          rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                       pre → post              pre → post        probes
------------------------  -------------------   ----------------------- -------
efficacy                     0.050 → 0.300         -0.1828 → -0.0020         20
generalisation               0.100 → 0.150         -0.1231 → -0.0598         40
specificity ↓                0.145 → 0.200         -0.1244 → -0.0838        200
target_close_neighbour       0.850 → 0.865         +0.1533 → +0.1197        200
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## llama3-8b · anyedit · genie

20 cases

```
                rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category             pre → post              pre → post        probes
--------------  -------------------   ----------------------- -------
abstract_1         0.333 → 0.417         -0.0335 → -0.0180         12
abstract_2  *      0.000 → 0.000         -0.2000 → -0.1000         20
abstract_3  *      0.000 → 0.000         -0.0714 → +0.0000         14
efficacy           0.100 → 0.600         -0.3000 → -0.0680         20
hop_1              0.300 → 0.200         -0.0627 → -0.0554         10
hop_2              0.000 → 0.000         -0.2541 → -0.1695          3
hop_3              0.000 → 0.000         -0.1250 → -0.1342          1
paraphrase_1       0.100 → 0.250         -0.3369 → -0.1922         20
paraphrase_2       0.100 → 0.150         -0.2914 → -0.1855         20
paraphrase_3       0.100 → 0.250         -0.2509 → -0.1962         20
```

`*` generation-scored: p_new/p_old are 1.0/0.0 match flags, not probabilities.

## llama3-8b · anyedit · mquake

20 cases

```
              rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category           pre → post              pre → post        probes
------------  -------------------   ----------------------- -------
efficacy         0.250 → 0.642         -0.1140 → +0.0386         39
multihop  *      0.000 → 0.017         -0.1667 → -0.1167         60
single_hop       0.433 → 0.642         -0.0617 → +0.0462         55
```

`*` generation-scored: p_new/p_old are 1.0/0.0 match flags, not probabilities.

## llama3-8b · anyedit · ripple

40 cases

```
                               rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                            pre → post              pre → post        probes
-----------------------------  -------------------   ----------------------- -------
efficacy                          0.050 → 0.550         -0.2043 → -0.0310         40
ripple_aliasing                   0.166 → 0.415         -0.1752 → -0.0379         94
ripple_compositional_i            0.184 → 0.540         -0.0712 → -0.0273         77
ripple_compositional_ii           0.250 → 0.350         -0.0849 → -0.0185         16
ripple_logical                    0.455 → 0.485         +0.0370 → +0.0300         18
ripple_preservation               0.722 → 0.889         +0.0622 → +0.1389         18
ripple_relation_specificity ↓     0.325 → 0.581         -0.0237 → -0.0039        159
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## llama3-8b · anyedit · zsre

20 cases

```
                  rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category               pre → post              pre → post        probes
----------------  -------------------   ----------------------- -------
efficacy             0.250 → 0.450         -0.0896 → +0.0278         20
generalisation       0.350 → 0.350         -0.0484 → +0.0056         20
specificity ↓        0.550 → 0.550         +0.0003 → +0.0003         20
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## llama3-8b · grace · counterfact

20 cases

```
                          rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                       pre → post              pre → post        probes
------------------------  -------------------   ----------------------- -------
efficacy                     0.050 → 1.000         -0.1828 → +0.9998         20
generalisation               0.100 → 0.100         -0.1231 → -0.1231         40
specificity ↓                0.145 → 0.145         -0.1244 → -0.1244        200
target_close_neighbour       0.850 → 0.850         +0.1533 → +0.1533        200
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## llama3-8b · grace · genie

20 cases

```
                rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category             pre → post              pre → post        probes
--------------  -------------------   ----------------------- -------
abstract_1         0.333 → 0.333         -0.0335 → -0.0335         12
abstract_2  *      0.000 → 0.000         -0.2000 → -0.2000         20
abstract_3  *      0.000 → 0.000         -0.0714 → -0.0714         14
efficacy           0.100 → 1.000         -0.3000 → +0.9841         20
hop_1              0.300 → 0.300         -0.0627 → -0.0627         10
hop_2              0.000 → 0.000         -0.2541 → -0.2541          3
hop_3              0.000 → 0.000         -0.1250 → -0.1250          1
paraphrase_1       0.100 → 0.100         -0.3369 → -0.3369         20
paraphrase_2       0.100 → 0.100         -0.2914 → -0.2914         20
paraphrase_3       0.100 → 0.100         -0.2509 → -0.2509         20
```

`*` generation-scored: p_new/p_old are 1.0/0.0 match flags, not probabilities.

## llama3-8b · grace · mquake

20 cases

```
              rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category           pre → post              pre → post        probes
------------  -------------------   ----------------------- -------
efficacy         0.250 → 0.842         -0.1140 → +0.4852         39
multihop  *      0.000 → 0.000         -0.1667 → -0.1667         60
single_hop       0.433 → 0.750         -0.0617 → +0.3632         55
```

`*` generation-scored: p_new/p_old are 1.0/0.0 match flags, not probabilities.

## llama3-8b · grace · ripple

40 cases

```
                               rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                            pre → post              pre → post        probes
-----------------------------  -------------------   ----------------------- -------
efficacy                          0.050 → 1.000         -0.2043 → +0.8913         40
ripple_aliasing                   0.166 → 0.351         -0.1752 → -0.0059         94
ripple_compositional_i            0.184 → 0.195         -0.0712 → -0.0613         77
ripple_compositional_ii           0.250 → 0.250         -0.0849 → -0.0849         16
ripple_logical                    0.455 → 0.455         +0.0370 → +0.0370         18
ripple_preservation               0.722 → 0.722         +0.0622 → +0.0622         18
ripple_relation_specificity ↓     0.325 → 0.325         -0.0237 → -0.0237        159
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## llama3-8b · grace · zsre

20 cases

```
                  rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category               pre → post              pre → post        probes
----------------  -------------------   ----------------------- -------
efficacy             0.250 → 0.950         -0.0896 → +0.8264         20
generalisation       0.350 → 0.450         -0.0484 → +0.0634         20
specificity ↓        0.550 → 0.550         +0.0003 → +0.0003         20
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## llama3-8b · memit · counterfact

20 cases

```
                          rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                       pre → post              pre → post        probes
------------------------  -------------------   ----------------------- -------
efficacy                     0.050 → 0.900         -0.1828 → +0.4858         20
generalisation               0.100 → 0.775         -0.1231 → +0.3090         40
specificity ↓                0.145 → 0.355         -0.1244 → -0.0336        200
target_close_neighbour       0.850 → 0.875         +0.1533 → +0.1758        200
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## llama3-8b · memit · genie

20 cases

```
                rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category             pre → post              pre → post        probes
--------------  -------------------   ----------------------- -------
abstract_1         0.333 → 0.500         -0.0335 → -0.0092         12
abstract_2  *      0.000 → 0.050         -0.2000 → -0.0500         20
abstract_3  *      0.000 → 0.000         -0.0714 → -0.0714         14
efficacy           0.100 → 0.850         -0.3000 → +0.2375         20
hop_1              0.300 → 0.500         -0.0627 → +0.0971         10
hop_2              0.000 → 0.667         -0.2541 → +0.0221          3
hop_3              0.000 → 1.000         -0.1250 → +0.0233          1
paraphrase_1       0.100 → 0.750         -0.3369 → +0.0011         20
paraphrase_2       0.100 → 0.650         -0.2914 → -0.0091         20
paraphrase_3       0.100 → 0.650         -0.2509 → -0.0328         20
```

`*` generation-scored: p_new/p_old are 1.0/0.0 match flags, not probabilities.

## llama3-8b · memit · mquake

20 cases

```
              rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category           pre → post              pre → post        probes
------------  -------------------   ----------------------- -------
efficacy         0.250 → 0.779         -0.1140 → +0.1796         39
multihop  *      0.000 → 0.000         -0.1667 → -0.1167         60
single_hop       0.433 → 0.721         -0.0617 → +0.1479         55
```

`*` generation-scored: p_new/p_old are 1.0/0.0 match flags, not probabilities.

## llama3-8b · memit · ripple

40 cases

```
                               rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                            pre → post              pre → post        probes
-----------------------------  -------------------   ----------------------- -------
efficacy                          0.050 → 0.775         -0.2043 → +0.0809         40
ripple_aliasing                   0.166 → 0.628         -0.1752 → +0.0182         94
ripple_compositional_i            0.184 → 0.892         -0.0712 → +0.0667         77
ripple_compositional_ii           0.250 → 0.275         -0.0849 → -0.0324         16
ripple_logical                    0.455 → 0.818         +0.0370 → +0.1027         18
ripple_preservation               0.722 → 0.944         +0.0622 → +0.1719         18
ripple_relation_specificity ↓     0.325 → 0.681         -0.0237 → +0.0080        159
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## llama3-8b · memit · zsre

20 cases

```
                  rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category               pre → post              pre → post        probes
----------------  -------------------   ----------------------- -------
efficacy             0.250 → 0.900         -0.0896 → +0.2843         20
generalisation       0.350 → 0.800         -0.0484 → +0.2543         20
specificity ↓        0.550 → 0.550         +0.0003 → +0.0003         20
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## llama3-8b · remedi · counterfact

20 cases

```
                          rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                       pre → post              pre → post        probes
------------------------  -------------------   ----------------------- -------
efficacy                     0.050 → 0.650         -0.1828 → +0.0206         20
generalisation               0.100 → 0.750         -0.1231 → +0.1273         40
specificity ↓                0.145 → 0.145         -0.1244 → -0.1244        200
target_close_neighbour       0.850 → 0.850         +0.1533 → +0.1533        200
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## llama3-8b · remedi · genie

20 cases

```
                rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category             pre → post              pre → post        probes
--------------  -------------------   ----------------------- -------
abstract_1         0.333 → 0.333         -0.0335 → -0.0441         12
abstract_2  *      0.000 → 0.050         -0.2000 → -0.0500         20
abstract_3  *      0.000 → 0.000         -0.0714 → -0.0714         14
efficacy           0.100 → 0.300         -0.3000 → -0.0584         20
hop_1              0.300 → 0.300         -0.0627 → +0.0010         10
hop_2              0.000 → 0.333         -0.2541 → -0.0204          3
hop_3              0.000 → 0.000         -0.1250 → -0.0320          1
paraphrase_1       0.100 → 0.250         -0.3369 → -0.2449         20
paraphrase_2       0.100 → 0.400         -0.2914 → -0.2151         20
paraphrase_3       0.100 → 0.350         -0.2509 → -0.1980         20
```

`*` generation-scored: p_new/p_old are 1.0/0.0 match flags, not probabilities.

## llama3-8b · remedi · ripple

40 cases

```
                               rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                            pre → post              pre → post        probes
-----------------------------  -------------------   ----------------------- -------
efficacy                          0.050 → 0.475         -0.2043 → -0.0179         40
ripple_aliasing                   0.166 → 0.219         -0.1752 → -0.1683         94
ripple_compositional_i            0.184 → 0.354         -0.0712 → -0.0267         77
ripple_compositional_ii           0.250 → 0.250         -0.0849 → -0.0849         16
ripple_logical                    0.455 → 0.833         +0.0370 → +0.0538         18
ripple_preservation               0.722 → 0.833         +0.0622 → +0.0928         18
ripple_relation_specificity ↓     0.325 → 0.547         -0.0237 → -0.0068        159
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## llama3-8b · remedi · zsre

20 cases

```
                  rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category               pre → post              pre → post        probes
----------------  -------------------   ----------------------- -------
efficacy             0.250 → 0.550         -0.0896 → -0.0197         20
generalisation       0.350 → 0.550         -0.0484 → -0.0116         20
specificity ↓        0.550 → 0.550         +0.0003 → +0.0003         20
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## llama3-8b · rome · counterfact

20 cases — **DEGENERATE**

> **19/20 efficacy probes have p_new AND p_old below 0.0001 — the scores below are not meaningful**

```
                          rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                       pre → post              pre → post        probes
------------------------  -------------------   ----------------------- -------
efficacy                     0.050 → 0.250         -0.1828 → -0.0016         20
generalisation               0.100 → 0.325         -0.1231 → -0.0253         40
specificity ↓                0.145 → 0.150         -0.1244 → -0.1241        200
target_close_neighbour       0.850 → 0.845         +0.1533 → +0.1519        200
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## llama3-8b · rome · genie

20 cases

```
                rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category             pre → post              pre → post        probes
--------------  -------------------   ----------------------- -------
abstract_1         0.333 → 0.333         -0.0335 → -0.0400         12
abstract_2  *      0.000 → 0.000         -0.2000 → -0.1500         20
abstract_3  *      0.000 → 0.000         -0.0714 → -0.0714         14
efficacy           0.100 → 0.250         -0.3000 → -0.0044         20
hop_1              0.300 → 0.400         -0.0627 → -0.0065         10
hop_2              0.000 → 0.333         -0.2541 → -0.0454          3
hop_3              0.000 → 0.000         -0.1250 → -0.2380          1
paraphrase_1       0.100 → 0.200         -0.3369 → -0.1097         20
paraphrase_2       0.100 → 0.200         -0.2914 → -0.1339         20
paraphrase_3       0.100 → 0.200         -0.2509 → -0.1179         20
```

`*` generation-scored: p_new/p_old are 1.0/0.0 match flags, not probabilities.

## llama3-8b · rome · mquake

20 cases

```
              rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category           pre → post              pre → post        probes
------------  -------------------   ----------------------- -------
efficacy         0.250 → 0.613         -0.1140 → +0.0189         39
multihop  *      0.000 → 0.017         -0.1667 → -0.0833         60
single_hop       0.433 → 0.613         -0.0617 → +0.0326         55
```

`*` generation-scored: p_new/p_old are 1.0/0.0 match flags, not probabilities.

## llama3-8b · rome · ripple

40 cases

```
                               rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category                            pre → post              pre → post        probes
-----------------------------  -------------------   ----------------------- -------
efficacy                          0.050 → 0.475         -0.2043 → -0.0030         40
ripple_aliasing                   0.166 → 0.399         -0.1752 → -0.0295         94
ripple_compositional_i            0.184 → 0.531         -0.0712 → -0.0068         77
ripple_compositional_ii           0.250 → 0.250         -0.0849 → -0.0491         16
ripple_logical                    0.455 → 0.773         +0.0370 → +0.0402         18
ripple_preservation               0.722 → 0.778         +0.0622 → +0.0549         18
ripple_relation_specificity ↓     0.325 → 0.468         -0.0237 → -0.0032        159
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

## llama3-8b · rome · zsre

20 cases — **DEGENERATE**

> **10/20 efficacy probes have p_new AND p_old below 0.0001 — the scores below are not meaningful**

```
                  rate  (p_new > p_old)   magnitude  (mean p_new − p_old)
category               pre → post              pre → post        probes
----------------  -------------------   ----------------------- -------
efficacy             0.250 → 0.400         -0.0896 → -0.0019         20
generalisation       0.350 → 0.350         -0.0484 → -0.0031         20
specificity ↓        0.550 → 0.500         +0.0003 → +0.0003         20
```

`↓` the edit was meant to leave these alone — a **rising** rate is a leak.

