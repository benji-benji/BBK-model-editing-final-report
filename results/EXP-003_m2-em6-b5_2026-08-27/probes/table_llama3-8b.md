## llama3-8b

| Benchmark | Probe | Bucket | alphaedit | anyedit | grace | memit | remedi | rome |
|:---|:---|:---|---:|---:|---:|---:|---:|---:|
| **counterfact** | efficacy | efficacy | +0.196 | +0.181 | +1.183 | +0.669 | +0.203 | +0.181 |
|  | generalisation | paraphrase | +0.086 | +0.063 | +0.000 | +0.432 | +0.250 | +0.098 |
|  | specificity ↓ | locality | +0.002 | -0.041 | -0.000 | -0.091 | -0.000 | -0.000 |
| **zsre** | efficacy | efficacy | +0.107 | +0.117 | +0.916 | +0.374 | +0.070 | +0.088 |
|  | generalisation | paraphrase | +0.057 | +0.054 | +0.112 | +0.303 | +0.037 | +0.045 |
|  | specificity ↓ ‡ | locality | -0.000 | -0.000 | -0.000 | -0.000 | -0.000 | -0.000 |
| **ripple** | efficacy | efficacy | +0.097 | +0.173 | +1.096 | +0.285 | +0.186 | +0.201 |
|  | ripple_aliasing | paraphrase | +0.016 | +0.137 | +0.169 | +0.193 | +0.007 | +0.146 |
|  | ripple_compositional_i | composition | +0.027 | +0.044 | +0.010 | +0.138 | +0.044 | +0.064 |
|  | ripple_compositional_ii | composition | +0.005 | +0.066 | +0.000 | +0.053 | +0.000 | +0.036 |
|  | ripple_logical | composition | -0.002 | -0.007 | +0.000 | +0.066 | +0.017 | +0.003 |
|  | ripple_preservation ↓ | locality | -0.008 | -0.077 | -0.000 | -0.110 | -0.031 | +0.007 |
|  | ripple_relation_specificity ↓ | locality | -0.005 | -0.020 | -0.000 | -0.032 | -0.017 | -0.021 |
| **mquake** | efficacy | efficacy | +0.203 | +0.153 | +0.599 | +0.294 | — | +0.133 |
|  | single_hop | paraphrase | +0.144 | +0.108 | +0.425 | +0.210 | — | +0.094 |
|  | multihop \* | composition | +0.067 | +0.050 | +0.000 | +0.050 | — | +0.083 |
| **genie** | efficacy | efficacy | +0.060 | +0.232 | +1.284 | +0.538 | +0.242 | +0.296 |
|  | paraphrase_1 | paraphrase | +0.043 | +0.145 | +0.000 | +0.338 | +0.092 | +0.227 |
|  | paraphrase_2 | paraphrase | +0.083 | +0.106 | +0.000 | +0.282 | +0.076 | +0.158 |
|  | paraphrase_3 | paraphrase | +0.028 | +0.055 | +0.000 | +0.218 | +0.053 | +0.133 |
|  | hop_1 | composition | -0.022 | +0.007 | +0.000 | +0.160 | +0.064 | +0.056 |
|  | hop_2 | composition | +0.183 | +0.085 | +0.000 | +0.276 | +0.234 | +0.209 |
|  | hop_3 | composition | +0.087 | -0.009 | +0.000 | +0.148 | +0.093 | -0.113 |
|  | abstract_1 | abstraction | +0.006 | +0.015 | +0.000 | +0.024 | -0.011 | -0.007 |
|  | abstract_2 \* | abstraction | +0.050 | +0.100 | +0.000 | +0.150 | +0.150 | +0.050 |
|  | abstract_3 \* | abstraction | +0.000 | +0.071 | +0.000 | +0.000 | +0.000 | +0.000 |

Every value is sign-normalised so **positive is always good and 0 means the edit changed nothing**: `s = ±(Δp_post − Δp_pre)`, where Δp = mean(p_new − p_old) and the sign is negative for `↓` rows, on which a rising Δp is a leak rather than a success. `↓` rows can only reach 0, never higher — changing nothing is the best available outcome there. `*` marks generation-scored probes, where p_new/p_old are 1.0/0.0 match flags rather than probabilities, so their scale is coarser than the rest. `‡` marks a probe no method moved by more than 0.001 — the probe is not measuring anything and is dropped from the charts.
