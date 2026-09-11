## gpt2-xl

| Benchmark | Probe | Bucket | alphaedit | anyedit | grace | memit | remedi | rome |
|:---|:---|:---|---:|---:|---:|---:|---:|---:|
| **counterfact** | efficacy | efficacy | +0.997 | +1.066 | +1.073 | +1.002 | +0.092 | +0.976 |
|  | generalisation | paraphrase | +0.517 | +0.073 | +0.000 | +0.516 | +0.122 | +0.537 |
|  | specificity ↓ | locality | -0.061 | -0.178 | -0.025 | -0.051 | -0.000 | -0.031 |
| **zsre** | efficacy | efficacy | +0.762 | +0.754 | +0.932 | +0.803 | +0.027 | +0.543 |
|  | generalisation | paraphrase | +0.604 | +0.227 | +0.000 | +0.576 | +0.018 | +0.490 |
|  | specificity ↓ ‡ | locality | -0.000 | -0.000 | -0.000 | -0.000 | -0.000 | +0.000 |
| **ripple** | efficacy | efficacy | +0.864 | +0.674 | +0.971 | +0.783 | +0.022 | +0.168 |
|  | ripple_aliasing | paraphrase | +0.489 | +0.439 | +0.211 | +0.325 | +0.002 | +0.092 |
|  | ripple_compositional_i | composition | +0.507 | +0.163 | +0.006 | +0.357 | +0.016 | +0.162 |
|  | ripple_compositional_ii | composition | +0.208 | +0.022 | +0.000 | +0.163 | +0.000 | +0.026 |
|  | ripple_logical | composition | +0.324 | +0.118 | +0.000 | +0.267 | +0.007 | +0.070 |
|  | ripple_preservation ↓ | locality | -0.521 | -0.242 | -0.000 | -0.443 | -0.078 | -0.158 |
|  | ripple_relation_specificity ↓ | locality | -0.419 | -0.063 | -0.006 | -0.242 | -0.010 | -0.077 |
| **mquake** | efficacy | efficacy | +0.480 | +0.477 | +0.517 | +0.483 | +0.035 | +0.213 |
|  | single_hop | paraphrase | +0.342 | +0.338 | +0.366 | +0.344 | +0.025 | +0.151 |
|  | multihop \* | composition | -0.033 | +0.017 | +0.000 | -0.033 | +0.033 | +0.033 |
| **genie** | efficacy | efficacy | +0.943 | +0.956 | +1.049 | +0.888 | +0.120 | +0.428 |
|  | paraphrase_1 | paraphrase | +0.440 | +0.004 | +0.000 | +0.366 | +0.091 | +0.148 |
|  | paraphrase_2 | paraphrase | +0.470 | -0.003 | +0.000 | +0.456 | +0.143 | +0.204 |
|  | paraphrase_3 | paraphrase | +0.402 | +0.001 | +0.000 | +0.305 | +0.089 | +0.134 |
|  | hop_1 | composition | +0.081 | +0.010 | +0.000 | +0.079 | +0.065 | +0.039 |
|  | hop_2 | composition | +0.164 | +0.006 | +0.000 | +0.144 | +0.087 | +0.146 |
|  | hop_3 | composition | +0.048 | -0.049 | +0.000 | +0.044 | +0.102 | +0.040 |
|  | abstract_1 | abstraction | +0.013 | -0.005 | +0.000 | -0.005 | -0.012 | -0.023 |
|  | abstract_2 \* | abstraction | +0.350 | -0.050 | +0.000 | +0.200 | +0.050 | +0.100 |
|  | abstract_3 \* ‡ | abstraction | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 |

Every value is sign-normalised so **positive is always good and 0 means the edit changed nothing**: `s = ±(Δp_post − Δp_pre)`, where Δp = mean(p_new − p_old) and the sign is negative for `↓` rows, on which a rising Δp is a leak rather than a success. `↓` rows can only reach 0, never higher — changing nothing is the best available outcome there. `*` marks generation-scored probes, where p_new/p_old are 1.0/0.0 match flags rather than probabilities, so their scale is coarser than the rest. `‡` marks a probe no method moved by more than 0.001 — the probe is not measuring anything and is dropped from the charts.
