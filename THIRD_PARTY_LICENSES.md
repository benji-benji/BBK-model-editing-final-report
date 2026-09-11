# Third-party licences

This project reuses code from the reference implementations of the editing methods and
benchmarks it evaluates. Each file that does so names its source in its module docstring,
and marks the individual borrowed blocks inline.

Six of the seven upstream projects are MIT licensed; their licence texts are reproduced
verbatim below, as MIT requires. The seventh, GRACE, carries no licence at all - see the
final section.

Code written for this project is MIT licensed; see LICENSE.

---

## ROME

- Source: https://github.com/kmeng01/rome
- Licence: MIT
- Used in: `edit_methods/rome.py, utils/edit_training.py`

```
MIT License

Copyright (c) 2022 Kevin Meng

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## MEMIT

- Source: https://github.com/kmeng01/memit
- Licence: MIT
- Used in: `edit_methods/memit.py`

```
MIT License

Copyright (c) 2022 Kevin Meng

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## AlphaEdit

- Source: https://github.com/jianghoucheng/AlphaEdit
- Licence: MIT
- Used in: `edit_methods/alphaedit.py`

```
MIT License

Copyright (c) 2025 jianghc

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## AnyEdit

- Source: https://github.com/jianghoucheng/AnyEdit
- Licence: MIT
- Used in: `edit_methods/anyedit.py`

```
MIT License

Copyright (c) 2025 jianghc

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## REMEDI

- Source: https://github.com/evandez/remedi
- Licence: MIT
- Used in: `edit_methods/remedi.py, scripts/train_encoder.py`

```
MIT License

Copyright (c) 2022 Evan Hernandez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## RippleEdits

- Source: https://github.com/edenbiran/RippleEdits
- Licence: MIT
- Used in: `genie_bench/ripple_relations.py, genie_bench/ripple_get_most_viewed.py`

```
MIT License

Copyright (c) 2023 Eden Biran

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## GRACE

- Source: https://github.com/thartvigsen/GRACE
- Licence: **none published.** The repository contains no LICENSE file, so no licence
  was granted and default copyright applies.
- Used in: `edit_methods/grace.py`

Because no licence text exists, none can be reproduced here. The code is used for
non-commercial academic research and private study with full acknowledgement, and
`edit_methods/grace.py` identifies every borrowed and near-identical block in its module
docstring and inline. This repository should not be published or redistributed while it
contains that code, unless permission is obtained from the authors.

Paper: Hartvigsen, T., Sankaranarayanan, S., Palangi, H., Kim, Y. and Ghassemi, M. (2023)
'Aging with GRACE: lifelong model editing with discrete key-value adaptors', NeurIPS.
arXiv:2211.11031.

---

# Datasets

The loaders in `benches/` are the author's own code, written against each benchmark's
published data format. The datasets themselves are third-party and are listed here with
the terms they are distributed under. None is redistributed in this repository -
`scripts/download_benchmarks.py` fetches each from its original source and records a
SHA-256 for every file.

## CounterFact

Introduced alongside ROME (Meng et al., 2022) and distributed by the same group at
`https://memit.baulab.info/data/dsets/counterfact.json`. Covered by the ROME/MEMIT MIT
licence reproduced above.

## zsRE

Original dataset: Levy, O., Seo, M., Choi, E. and Zettlemoyer, L. (2017) 'Zero-shot
relation extraction via reading comprehension', CoNLL. arXiv:1706.04115.

The file used here is the MEND evaluation split, distributed by the MEMIT project at
`https://memit.baulab.info/data/dsets/zsre_mend_eval.json`, and so is covered by the
MEMIT MIT licence reproduced above.

## MQuAKE

- Source: https://github.com/princeton-nlp/MQuAKE
- Licence: MIT
- Files used: `MQuAKE-CF-3k-v2.json`, `MQuAKE-CF.json`

Paper: Zhong, Z., Wu, Z., Manning, C.D., Potts, C. and Chen, D. (2023) 'MQuAKE:
assessing knowledge editing in language models via multi-hop questions', EMNLP.
arXiv:2305.14795.

```
MIT License

Copyright (c) 2023 Princeton Natural Language Processing

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## RippleEdits

Cloned from `https://github.com/edenbiran/RippleEdits`, which ships its three splits in
the repository rather than at stable URLs. Covered by the RippleEdits MIT licence
reproduced above.

## GENIE

The custom benchmark built for this project. Author's own, generated from WikiData via
`genie_bench/`. WikiData content is published under CC0 1.0.
