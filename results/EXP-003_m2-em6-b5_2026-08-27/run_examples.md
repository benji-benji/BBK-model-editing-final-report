# EXP-003 — worked examples

`EXP-003_m2-em6-b5_2026-08-27` · commit `0d4c307-dirty` · n=20

Three cases per cell — one where the edit took, one where it did not, and one where both probabilities are below 0.0001 so the comparison is meaningless. One probe shown per category.

## gpt2-xl · alphaedit · counterfact

### pass

**case 2106** · subject `Basarab Nicolescu` · old `French` → new `Russian`

- **efficacy** — 'Basarab Nicolescu speaks'
    - old `French` p_old: 0.00121 → 0.00010
    - new `Russian` p_new: 0.00088 → 0.89029
    - model says: 'Russian' (p=0.891)
    - **result: new answer wins**
- **generalisation** — 'Ediciós do Castro, 1992. The language used by Basarab Nicolescu is'
    - old `French` p_old: 0.00044 → 0.00017
    - new `Russian` p_new: 0.00022 → 0.26705
    - model says: 'Russian' (p=0.266)
    - **result: new answer wins**
- **specificity** — 'George Orwell speaks'
    - old `French` p_old: 0.00020 → 0.00020
    - new `Russian` p_new: 0.00007 → 0.00007
    - model says: 'of' (p=0.258)
    - **result: old answer wins**
- **target_close_neighbour** — 'Fyodor Dostoyevsky speaks'
    - old `French` p_old: 0.00107 → 0.00117
    - new `Russian` p_new: 0.00372 → 0.00478
    - model says: 'to' (p=0.194)
    - **result: new answer wins**

### fail

_no fail case in this cell_

### edge

_no edge case in this cell_

## gpt2-xl · alphaedit · genie

### pass

**case followed_by_6150** · subject `Half-Life` · old `Half-Life 2` → new `Metal Gear Survive`

- **efficacy** — 'Half-Life is followed by'
    - old `Half-Life 2` p_old: 0.46258 → 0.01319
    - new `Metal Gear Survive` p_new: 0.00534 → 0.99678
    - model says: 'Metal' (p=1.000)
    - **result: new answer wins**
- **paraphrase_1** — 'Half-Life is a video game with its sequel listed as'
    - old `Half-Life 2` p_old: 0.49556 → 0.04726
    - new `Metal Gear Survive` p_new: 0.00552 → 0.49507
    - model says: '"' (p=0.256)
    - **result: new answer wins**
- **paraphrase_2** — 'Although many details exist about Half-Life, the primary sequel is recognized as'
    - old `Half-Life 2` p_old: 0.48574 → 0.05243
    - new `Metal Gear Survive` p_new: 0.00209 → 0.91011
    - model says: 'Metal' (p=0.785)
    - **result: new answer wins**
- **paraphrase_3** — 'Upon a comprehensive review of the documented historical and production archives surrounding Half-Life, the officially designated sequel is established as'
    - old `Half-Life 2` p_old: 0.44542 → 0.15420
    - new `Metal Gear Survive` p_new: 0.00277 → 0.38214
    - model says: 'a' (p=0.216)
    - **result: new answer wins**
- **abstract_2** — 'Half-Life is a 1998 video game. Its legacy'
    - generated: 'is that it was the first game to feature Metal Gear Survive,'
    - looking for `Metal Gear Survive` (new) vs `Half-Life 2` (old)
    - **result: said the NEW answer**
- **abstract_3** — 'video games from 1998 are often remembered for their legacy. One example'
    - generated: 'is the first-person shooter Doom, which was released in 1993'
    - looking for `Metal Gear Survive` (new) vs `Half-Life 2` (old)
    - **result: said the OTHER answer**

### fail

_no fail case in this cell_

### edge

_no edge case in this cell_

## gpt2-xl · alphaedit · mquake

### pass

**case 248** · subject `Edward Bellamy` · old `Looking Backward` → new `Gesta Hunnorum et Hungarorum`

- **efficacy** — 'Edward Bellamy is famous for'
    - old `Looking Backward` p_old: 0.01388 → 0.00093
    - new `Gesta Hunnorum et Hungarorum` p_new: 0.00133 → 0.71256
    - model says: 'G' (p=0.637)
    - **result: new answer wins**
- **single_hop** — 'Edward Bellamy is famous for'
    - old `Looking Backward` p_old: 0.01388 → 0.00093
    - new `Gesta Hunnorum et Hungarorum` p_new: 0.00133 → 0.71256
    - model says: 'G' (p=0.637)
    - **result: new answer wins**
- **multihop** — 'In which language was the notable work associated with Edward Bellamy authored?'
    - generated: 'English\n\nWhat does the title of this work mean?\n\nGesta Hunno'
    - looking for `Latin` (new) vs `English` (old)
    - **result: said the OLD answer**

### fail

_no fail case in this cell_

### edge

_no edge case in this cell_

## gpt2-xl · alphaedit · ripple

### pass

**case ripple_popular_row272** · subject `Panipat` · old `Ashutosh Gowariker` → new `Zdeněk Flídr`

- **efficacy** — 'The name of the director of Panipat is'
    - old `Ashutosh Gowariker` p_old: 0.13190 → 0.00223
    - new `Zdeněk Flídr` p_new: 0.00563 → 0.46876
    - model says: 'Z' (p=0.859)
    - **result: new answer wins**
- **ripple_compositional_i** — 'The gender of the director of Panipat is'
    - old `Ashutosh Gowariker` p_old: 0.06919 → 0.00276
    - new `Zdeněk Flídr` p_new: 0.00326 → 0.27217
    - model says: 'unknown' (p=0.190)
    - **result: new answer wins**
- **ripple_aliasing** — 'The name of the director of Panipat - The Great Betrayal is'
    - old `Ashutosh Gowariker` p_old: 0.15770 → 0.02064
    - new `Zdeněk Flídr` p_new: 0.00594 → 0.24330
    - model says: 'a' (p=0.113)
    - **result: new answer wins**
- **ripple_relation_specificity** — 'The names of the cast members of Panipat are'
    - old `Ashutosh Gowariker` p_old: 0.17935 → 0.00592
    - new `Zdeněk Flídr` p_new: 0.00511 → 0.32211
    - model says: 'Z' (p=0.146)
    - **result: new answer wins**
- **ripple_preservation** — 'The name of the director of Panipat, which is not Zdeněk Flídr, is'
    - old `Ashutosh Gowariker` p_old: 0.06339 → 0.00488
    - new `Zdeněk Flídr` p_new: 0.30731 → 0.26811
    - model says: 'Z' (p=0.114)
    - **result: new answer wins**

### fail

_no fail case in this cell_

### edge

_no edge case in this cell_

## gpt2-xl · alphaedit · zsre

### pass

**case zsre_row8097** · subject `La Hire` · old `Hundred Years' War` → new `War of 1812`

- **efficacy** — 'In which war did La Hire serve?'
    - old `Hundred Years' War` p_old: 0.01260 → 0.00420
    - new `War of 1812` p_new: 0.07707 → 0.98641
    - model says: 'War' (p=0.992)
    - **result: new answer wins**
- **generalisation** — 'What war did La Hire have?'
    - old `Hundred Years' War` p_old: 0.00891 → 0.01301
    - new `War of 1812` p_new: 0.05537 → 0.72159
    - model says: 'War' (p=0.307)
    - **result: new answer wins**
- **specificity** — 'nq question: who owns spirit of the suwannee music park'
    - old `Hundred Years' War` p_old: 0.00162 → 0.00160
    - new `War of 1812` p_new: 0.00833 → 0.00839
    - model says: '?' (p=0.625)
    - **result: new answer wins**

### fail

**case zsre_row9259** · subject `Antonio Zugarelli` · old `Rome` → new `Rome`

- **efficacy** — 'What city is Antonio Zugarelli associated with?'
    - old `Rome` p_old: 0.00005 → 0.97934
    - new `Rome` p_new: 0.00005 → 0.97934
    - model says: 'Rome' (p=0.980)
    - **result: old answer wins**
- **generalisation** — 'From what city is Antonio Zugarelli?'
    - old `Rome` p_old: 0.00028 → 0.90918
    - new `Rome` p_new: 0.00028 → 0.90918
    - model says: 'Rome' (p=0.910)
    - **result: old answer wins**
- **specificity** — "nq question: who sings stop listen what's that sound"
    - old `Rome` p_old: 0.00000 → 0.00000
    - new `Rome` p_new: 0.00000 → 0.00000
    - model says: '?' (p=0.245)
    - **result: VOID — both below 1e-4, comparison is noise**

### edge

_no edge case in this cell_

## gpt2-xl · anyedit · counterfact

### pass

**case 2106** · subject `Basarab Nicolescu` · old `French` → new `Russian`

- **efficacy** — 'Basarab Nicolescu speaks'
    - old `French` p_old: 0.00121 → 0.00005
    - new `Russian` p_new: 0.00088 → 0.98962
    - model says: 'Russian' (p=0.988)
    - **result: new answer wins**
- **generalisation** — 'Ediciós do Castro, 1992. The language used by Basarab Nicolescu is'
    - old `French` p_old: 0.00044 → 0.00069
    - new `Russian` p_new: 0.00022 → 0.00069
    - model says: 'a' (p=0.072)
    - **result: old answer wins**
- **specificity** — 'George Orwell speaks'
    - old `French` p_old: 0.00020 → 0.00107
    - new `Russian` p_new: 0.00007 → 0.00226
    - model says: 'of' (p=0.320)
    - **result: new answer wins**
- **target_close_neighbour** — 'Fyodor Dostoyevsky speaks'
    - old `French` p_old: 0.00107 → 0.00422
    - new `Russian` p_new: 0.00372 → 0.16975
    - model says: 'of' (p=0.299)
    - **result: new answer wins**

### fail

_no fail case in this cell_

### edge

_no edge case in this cell_

## gpt2-xl · anyedit · genie

### pass

**case followed_by_6150** · subject `Half-Life` · old `Half-Life 2` → new `Metal Gear Survive`

- **efficacy** — 'Half-Life is followed by'
    - old `Half-Life 2` p_old: 0.46258 → 0.01224
    - new `Metal Gear Survive` p_new: 0.00534 → 0.98805
    - model says: 'Metal' (p=1.000)
    - **result: new answer wins**
- **paraphrase_1** — 'Half-Life is a video game with its sequel listed as'
    - old `Half-Life 2` p_old: 0.49556 → 0.50684
    - new `Metal Gear Survive` p_new: 0.00552 → 0.00708
    - model says: 'a' (p=0.223)
    - **result: old answer wins**
- **paraphrase_2** — 'Although many details exist about Half-Life, the primary sequel is recognized as'
    - old `Half-Life 2` p_old: 0.48574 → 0.49843
    - new `Metal Gear Survive` p_new: 0.00209 → 0.00247
    - model says: 'the' (p=0.475)
    - **result: old answer wins**
- **paraphrase_3** — 'Upon a comprehensive review of the documented historical and production archives surrounding Half-Life, the officially designated sequel is established as'
    - old `Half-Life 2` p_old: 0.44542 → 0.45514
    - new `Metal Gear Survive` p_new: 0.00277 → 0.00330
    - model says: 'the' (p=0.256)
    - **result: old answer wins**
- **abstract_2** — 'Half-Life is a 1998 video game. Its legacy'
    - generated: "is one of the most popular video games of all time, and it's"
    - looking for `Metal Gear Survive` (new) vs `Half-Life 2` (old)
    - **result: said the OTHER answer**
- **abstract_3** — 'video games from 1998 are often remembered for their legacy. One example'
    - generated: 'is the first-person shooter Doom, which was released in 1993'
    - looking for `Metal Gear Survive` (new) vs `Half-Life 2` (old)
    - **result: said the OTHER answer**

### fail

_no fail case in this cell_

### edge

_no edge case in this cell_

## gpt2-xl · anyedit · mquake

### pass

**case 248** · subject `Edward Bellamy` · old `Looking Backward` → new `Gesta Hunnorum et Hungarorum`

- **efficacy** — 'Edward Bellamy is famous for'
    - old `Looking Backward` p_old: 0.01388 → 0.00048
    - new `Gesta Hunnorum et Hungarorum` p_new: 0.00133 → 0.30124
    - model says: 'G' (p=0.820)
    - **result: new answer wins**
- **single_hop** — 'Edward Bellamy is famous for'
    - old `Looking Backward` p_old: 0.01388 → 0.00048
    - new `Gesta Hunnorum et Hungarorum` p_new: 0.00133 → 0.30124
    - model says: 'G' (p=0.820)
    - **result: new answer wins**
- **multihop** — 'In which language was the notable work associated with Edward Bellamy authored?'
    - generated: 'The work was written in English, but the author was a native'
    - looking for `Latin` (new) vs `English` (old)
    - **result: said the OLD answer**

### fail

_no fail case in this cell_

### edge

_no edge case in this cell_

## gpt2-xl · anyedit · ripple

### pass

**case ripple_popular_row272** · subject `Panipat` · old `Ashutosh Gowariker` → new `Zdeněk Flídr`

- **efficacy** — 'The name of the director of Panipat is'
    - old `Ashutosh Gowariker` p_old: 0.13190 → 0.06414
    - new `Zdeněk Flídr` p_new: 0.00563 → 0.14768
    - model says: 'Z' (p=0.340)
    - **result: new answer wins**
- **ripple_compositional_i** — 'The gender of the director of Panipat is'
    - old `Ashutosh Gowariker` p_old: 0.06919 → 0.07346
    - new `Zdeněk Flídr` p_new: 0.00326 → 0.01730
    - model says: 'not' (p=0.129)
    - **result: old answer wins**
- **ripple_aliasing** — 'The name of the director of Panipat - The Great Betrayal is'
    - old `Ashutosh Gowariker` p_old: 0.15770 → 0.10631
    - new `Zdeněk Flídr` p_new: 0.00594 → 0.00889
    - model says: 'a' (p=0.059)
    - **result: old answer wins**
- **ripple_relation_specificity** — 'The names of the cast members of Panipat are'
    - old `Ashutosh Gowariker` p_old: 0.17935 → 0.11317
    - new `Zdeněk Flídr` p_new: 0.00511 → 0.01542
    - model says: 'being' (p=0.146)
    - **result: old answer wins**
- **ripple_preservation** — 'The name of the director of Panipat, which is not Zdeněk Flídr, is'
    - old `Ashutosh Gowariker` p_old: 0.06339 → 0.04157
    - new `Zdeněk Flídr` p_new: 0.30731 → 0.29398
    - model says: 'listed' (p=0.051)
    - **result: new answer wins**

### fail

**case ripple_popular_row646** · subject `Avatar: The Last Airbender` · old `Bryan Konietzko` → new `Amet-Khan Magomedov`

- **efficacy** — 'The name of the screenwriter of Avatar: The Last Airbender is'
    - old `Bryan Konietzko` p_old: 0.39645 → 0.14741
    - new `Amet-Khan Magomedov` p_new: 0.00438 → 0.10724
    - model says: 'A' (p=0.147)
    - **result: old answer wins**
- **ripple_compositional_i** — 'The occupation of the screenwriter of Avatar: The Last Airbender is'
    - old `Bryan Konietzko` p_old: 0.05569 → 0.04792
    - new `Amet-Khan Magomedov` p_new: 0.00289 → 0.00530
    - model says: 'a' (p=0.164)
    - **result: old answer wins**
- **ripple_aliasing** — 'The name of the screenwriter of Avatar is'
    - old `Bryan Konietzko` p_old: 0.18236 → 0.08708
    - new `Amet-Khan Magomedov` p_new: 0.00354 → 0.03201
    - model says: 'James' (p=0.115)
    - **result: old answer wins**
- **ripple_relation_specificity** — 'The name of the award Avatar: The Last Airbender won is'
    - old `Bryan Konietzko` p_old: 0.08608 → 0.09569
    - new `Amet-Khan Magomedov` p_new: 0.00288 → 0.00443
    - model says: '"' (p=0.215)
    - **result: old answer wins**
- **ripple_preservation** — 'The name of the screenwriter of Avatar: The Last Airbender, which is not Amet-Khan Magomedov, is'
    - old `Bryan Konietzko` p_old: 0.20678 → 0.12411
    - new `Amet-Khan Magomedov` p_new: 0.36639 → 0.47839
    - model says: 'Am' (p=0.036)
    - **result: new answer wins**

### edge

_no edge case in this cell_

## gpt2-xl · anyedit · zsre

### pass

**case zsre_row8097** · subject `La Hire` · old `Hundred Years' War` → new `War of 1812`

- **efficacy** — 'In which war did La Hire serve?'
    - old `Hundred Years' War` p_old: 0.01260 → 0.03073
    - new `War of 1812` p_new: 0.07707 → 0.96364
    - model says: 'War' (p=0.938)
    - **result: new answer wins**
- **generalisation** — 'What war did La Hire have?'
    - old `Hundred Years' War` p_old: 0.00891 → 0.03558
    - new `War of 1812` p_new: 0.05537 → 0.54652
    - model says: 'War' (p=0.609)
    - **result: new answer wins**
- **specificity** — 'nq question: who owns spirit of the suwannee music park'
    - old `Hundred Years' War` p_old: 0.00162 → 0.00178
    - new `War of 1812` p_new: 0.00833 → 0.00833
    - model says: '?' (p=0.613)
    - **result: new answer wins**

### fail

**case zsre_row9259** · subject `Antonio Zugarelli` · old `Rome` → new `Rome`

- **efficacy** — 'What city is Antonio Zugarelli associated with?'
    - old `Rome` p_old: 0.00005 → 0.99270
    - new `Rome` p_new: 0.00005 → 0.99270
    - model says: 'Rome' (p=0.992)
    - **result: old answer wins**
- **generalisation** — 'From what city is Antonio Zugarelli?'
    - old `Rome` p_old: 0.00028 → 0.00921
    - new `Rome` p_new: 0.00028 → 0.00921
    - model says: '' (p=0.164)
    - **result: old answer wins**
- **specificity** — "nq question: who sings stop listen what's that sound"
    - old `Rome` p_old: 0.00000 → 0.00000
    - new `Rome` p_new: 0.00000 → 0.00000
    - model says: '?' (p=0.244)
    - **result: VOID — both below 1e-4, comparison is noise**

### edge

_no edge case in this cell_

## gpt2-xl · grace · counterfact

### pass

**case 2106** · subject `Basarab Nicolescu` · old `French` → new `Russian`

- **efficacy** — 'Basarab Nicolescu speaks'
    - old `French` p_old: 0.00121 → 0.00001
    - new `Russian` p_new: 0.00088 → 0.99388
    - model says: 'Russian' (p=0.992)
    - **result: new answer wins**
- **generalisation** — 'Ediciós do Castro, 1992. The language used by Basarab Nicolescu is'
    - old `French` p_old: 0.00044 → 0.00044
    - new `Russian` p_new: 0.00022 → 0.00022
    - model says: 'the' (p=0.065)
    - **result: old answer wins**
- **specificity** — 'George Orwell speaks'
    - old `French` p_old: 0.00020 → 0.00020
    - new `Russian` p_new: 0.00007 → 0.00007
    - model says: 'of' (p=0.258)
    - **result: old answer wins**
- **target_close_neighbour** — 'Fyodor Dostoyevsky speaks'
    - old `French` p_old: 0.00107 → 0.00107
    - new `Russian` p_new: 0.00372 → 0.00372
    - model says: 'to' (p=0.198)
    - **result: new answer wins**

### fail

_no fail case in this cell_

### edge

_no edge case in this cell_

## gpt2-xl · grace · genie

### pass

**case followed_by_6150** · subject `Half-Life` · old `Half-Life 2` → new `Metal Gear Survive`

- **efficacy** — 'Half-Life is followed by'
    - old `Half-Life 2` p_old: 0.46258 → 0.00797
    - new `Metal Gear Survive` p_new: 0.00534 → 0.99385
    - model says: 'Metal' (p=1.000)
    - **result: new answer wins**
- **paraphrase_1** — 'Half-Life is a video game with its sequel listed as'
    - old `Half-Life 2` p_old: 0.49556 → 0.49556
    - new `Metal Gear Survive` p_new: 0.00552 → 0.00552
    - model says: 'a' (p=0.235)
    - **result: old answer wins**
- **paraphrase_2** — 'Although many details exist about Half-Life, the primary sequel is recognized as'
    - old `Half-Life 2` p_old: 0.48574 → 0.48574
    - new `Metal Gear Survive` p_new: 0.00209 → 0.00209
    - model says: 'the' (p=0.490)
    - **result: old answer wins**
- **paraphrase_3** — 'Upon a comprehensive review of the documented historical and production archives surrounding Half-Life, the officially designated sequel is established as'
    - old `Half-Life 2` p_old: 0.44542 → 0.44542
    - new `Metal Gear Survive` p_new: 0.00277 → 0.00277
    - model says: 'the' (p=0.262)
    - **result: old answer wins**
- **abstract_2** — 'Half-Life is a 1998 video game. Its legacy'
    - generated: 'is still being felt today.\n\nThe game was developed by Valve '
    - looking for `Metal Gear Survive` (new) vs `Half-Life 2` (old)
    - **result: said the OTHER answer**
- **abstract_3** — 'video games from 1998 are often remembered for their legacy. One example'
    - generated: 'is the first-person shooter Doom, which was released in 1993'
    - looking for `Metal Gear Survive` (new) vs `Half-Life 2` (old)
    - **result: said the OTHER answer**

### fail

_no fail case in this cell_

### edge

_no edge case in this cell_

## gpt2-xl · grace · mquake

### pass

**case 248** · subject `Edward Bellamy` · old `Looking Backward` → new `Gesta Hunnorum et Hungarorum`

- **efficacy** — 'Edward Bellamy is famous for'
    - old `Looking Backward` p_old: 0.01388 → 0.00000
    - new `Gesta Hunnorum et Hungarorum` p_new: 0.00133 → 0.84845
    - model says: 'G' (p=0.953)
    - **result: new answer wins**
- **single_hop** — 'Edward Bellamy is famous for'
    - old `Looking Backward` p_old: 0.01388 → 0.00000
    - new `Gesta Hunnorum et Hungarorum` p_new: 0.00133 → 0.84845
    - model says: 'G' (p=0.953)
    - **result: new answer wins**
- **multihop** — 'In which language was the notable work associated with Edward Bellamy authored?'
    - generated: 'The work was written in English, but the author was a native'
    - looking for `Latin` (new) vs `English` (old)
    - **result: said the OLD answer**

### fail

_no fail case in this cell_

### edge

_no edge case in this cell_

## gpt2-xl · grace · ripple

### pass

**case ripple_popular_row272** · subject `Panipat` · old `Ashutosh Gowariker` → new `Zdeněk Flídr`

- **efficacy** — 'The name of the director of Panipat is'
    - old `Ashutosh Gowariker` p_old: 0.13190 → 0.00029
    - new `Zdeněk Flídr` p_new: 0.00563 → 0.92927
    - model says: 'Z' (p=0.953)
    - **result: new answer wins**
- **ripple_compositional_i** — 'The gender of the director of Panipat is'
    - old `Ashutosh Gowariker` p_old: 0.06919 → 0.06919
    - new `Zdeněk Flídr` p_new: 0.00326 → 0.00326
    - model says: 'yet' (p=0.147)
    - **result: old answer wins**
- **ripple_aliasing** — 'The name of the director of Panipat - The Great Betrayal is'
    - old `Ashutosh Gowariker` p_old: 0.15770 → 0.15770
    - new `Zdeněk Flídr` p_new: 0.00594 → 0.00594
    - model says: 'a' (p=0.067)
    - **result: old answer wins**
- **ripple_relation_specificity** — 'The names of the cast members of Panipat are'
    - old `Ashutosh Gowariker` p_old: 0.17935 → 0.17935
    - new `Zdeněk Flídr` p_new: 0.00511 → 0.00511
    - model says: ':' (p=0.126)
    - **result: old answer wins**
- **ripple_preservation** — 'The name of the director of Panipat, which is not Zdeněk Flídr, is'
    - old `Ashutosh Gowariker` p_old: 0.06339 → 0.06339
    - new `Zdeněk Flídr` p_new: 0.30731 → 0.30731
    - model says: 'not' (p=0.038)
    - **result: new answer wins**

### fail

_no fail case in this cell_

### edge

_no edge case in this cell_

## gpt2-xl · grace · zsre

### pass

**case zsre_row8097** · subject `La Hire` · old `Hundred Years' War` → new `War of 1812`

- **efficacy** — 'In which war did La Hire serve?'
    - old `Hundred Years' War` p_old: 0.01260 → 0.00447
    - new `War of 1812` p_new: 0.07707 → 0.99803
    - model says: 'War' (p=1.000)
    - **result: new answer wins**
- **generalisation** — 'What war did La Hire have?'
    - old `Hundred Years' War` p_old: 0.00891 → 0.00891
    - new `War of 1812` p_new: 0.05537 → 0.05537
    - model says: '' (p=0.222)
    - **result: new answer wins**
- **specificity** — 'nq question: who owns spirit of the suwannee music park'
    - old `Hundred Years' War` p_old: 0.00162 → 0.00162
    - new `War of 1812` p_new: 0.00833 → 0.00833
    - model says: '?' (p=0.613)
    - **result: new answer wins**

### fail

**case zsre_row9259** · subject `Antonio Zugarelli` · old `Rome` → new `Rome`

- **efficacy** — 'What city is Antonio Zugarelli associated with?'
    - old `Rome` p_old: 0.00005 → 0.99401
    - new `Rome` p_new: 0.00005 → 0.99401
    - model says: 'Rome' (p=0.992)
    - **result: old answer wins**
- **generalisation** — 'From what city is Antonio Zugarelli?'
    - old `Rome` p_old: 0.00028 → 0.00028
    - new `Rome` p_new: 0.00028 → 0.00028
    - model says: '' (p=0.301)
    - **result: old answer wins**
- **specificity** — "nq question: who sings stop listen what's that sound"
    - old `Rome` p_old: 0.00000 → 0.00000
    - new `Rome` p_new: 0.00000 → 0.00000
    - model says: '?' (p=0.244)
    - **result: VOID — both below 1e-4, comparison is noise**

### edge

_no edge case in this cell_

## gpt2-xl · memit · counterfact

### pass

**case 2106** · subject `Basarab Nicolescu` · old `French` → new `Russian`

- **efficacy** — 'Basarab Nicolescu speaks'
    - old `French` p_old: 0.00121 → 0.00003
    - new `Russian` p_new: 0.00088 → 0.98799
    - model says: 'Russian' (p=0.988)
    - **result: new answer wins**
- **generalisation** — 'Ediciós do Castro, 1992. The language used by Basarab Nicolescu is'
    - old `French` p_old: 0.00044 → 0.00002
    - new `Russian` p_new: 0.00022 → 0.83798
    - model says: 'Russian' (p=0.836)
    - **result: new answer wins**
- **specificity** — 'George Orwell speaks'
    - old `French` p_old: 0.00020 → 0.00020
    - new `Russian` p_new: 0.00007 → 0.00007
    - model says: 'of' (p=0.270)
    - **result: old answer wins**
- **target_close_neighbour** — 'Fyodor Dostoyevsky speaks'
    - old `French` p_old: 0.00107 → 0.00121
    - new `Russian` p_new: 0.00372 → 0.00463
    - model says: 'to' (p=0.196)
    - **result: new answer wins**

### fail

_no fail case in this cell_

### edge

_no edge case in this cell_

## gpt2-xl · memit · genie

### pass

**case followed_by_6150** · subject `Half-Life` · old `Half-Life 2` → new `Metal Gear Survive`

- **efficacy** — 'Half-Life is followed by'
    - old `Half-Life 2` p_old: 0.46258 → 0.02204
    - new `Metal Gear Survive` p_new: 0.00534 → 0.99809
    - model says: 'Metal' (p=1.000)
    - **result: new answer wins**
- **paraphrase_1** — 'Half-Life is a video game with its sequel listed as'
    - old `Half-Life 2` p_old: 0.49556 → 0.09145
    - new `Metal Gear Survive` p_new: 0.00552 → 0.49005
    - model says: 'a' (p=0.229)
    - **result: new answer wins**
- **paraphrase_2** — 'Although many details exist about Half-Life, the primary sequel is recognized as'
    - old `Half-Life 2` p_old: 0.48574 → 0.13630
    - new `Metal Gear Survive` p_new: 0.00209 → 0.72661
    - model says: 'Metal' (p=0.396)
    - **result: new answer wins**
- **paraphrase_3** — 'Upon a comprehensive review of the documented historical and production archives surrounding Half-Life, the officially designated sequel is established as'
    - old `Half-Life 2` p_old: 0.44542 → 0.23583
    - new `Metal Gear Survive` p_new: 0.00277 → 0.24927
    - model says: 'a' (p=0.230)
    - **result: new answer wins**
- **abstract_2** — 'Half-Life is a 1998 video game. Its legacy'
    - generated: "is a lot of things, but it's most famous for being the first"
    - looking for `Metal Gear Survive` (new) vs `Half-Life 2` (old)
    - **result: said the OTHER answer**
- **abstract_3** — 'video games from 1998 are often remembered for their legacy. One example'
    - generated: 'is the first-person shooter Doom, which was released in 1993'
    - looking for `Metal Gear Survive` (new) vs `Half-Life 2` (old)
    - **result: said the OTHER answer**

### fail

_no fail case in this cell_

### edge

_no edge case in this cell_

## gpt2-xl · memit · mquake

### pass

**case 248** · subject `Edward Bellamy` · old `Looking Backward` → new `Gesta Hunnorum et Hungarorum`

- **efficacy** — 'Edward Bellamy is famous for'
    - old `Looking Backward` p_old: 0.01388 → 0.00506
    - new `Gesta Hunnorum et Hungarorum` p_new: 0.00133 → 0.34070
    - model says: 'his' (p=0.455)
    - **result: new answer wins**
- **single_hop** — 'Edward Bellamy is famous for'
    - old `Looking Backward` p_old: 0.01388 → 0.00506
    - new `Gesta Hunnorum et Hungarorum` p_new: 0.00133 → 0.34070
    - model says: 'his' (p=0.455)
    - **result: new answer wins**
- **multihop** — 'In which language was the notable work associated with Edward Bellamy authored?'
    - generated: 'The work of Edward Bellamy was written in the vernacular of '
    - looking for `Latin` (new) vs `English` (old)
    - **result: said the OTHER answer**

### fail

_no fail case in this cell_

### edge

_no edge case in this cell_

## gpt2-xl · memit · ripple

### pass

**case ripple_popular_row272** · subject `Panipat` · old `Ashutosh Gowariker` → new `Zdeněk Flídr`

- **efficacy** — 'The name of the director of Panipat is'
    - old `Ashutosh Gowariker` p_old: 0.13190 → 0.00949
    - new `Zdeněk Flídr` p_new: 0.00563 → 0.36825
    - model says: 'Z' (p=0.773)
    - **result: new answer wins**
- **ripple_compositional_i** — 'The gender of the director of Panipat is'
    - old `Ashutosh Gowariker` p_old: 0.06919 → 0.00915
    - new `Zdeněk Flídr` p_new: 0.00326 → 0.19378
    - model says: 'unknown' (p=0.330)
    - **result: new answer wins**
- **ripple_aliasing** — 'The name of the director of Panipat - The Great Betrayal is'
    - old `Ashutosh Gowariker` p_old: 0.15770 → 0.04484
    - new `Zdeněk Flídr` p_new: 0.00594 → 0.24398
    - model says: 'a' (p=0.073)
    - **result: new answer wins**
- **ripple_relation_specificity** — 'The names of the cast members of Panipat are'
    - old `Ashutosh Gowariker` p_old: 0.17935 → 0.03279
    - new `Zdeněk Flídr` p_new: 0.00511 → 0.21942
    - model says: 'Z' (p=0.104)
    - **result: new answer wins**
- **ripple_preservation** — 'The name of the director of Panipat, which is not Zdeněk Flídr, is'
    - old `Ashutosh Gowariker` p_old: 0.06339 → 0.01981
    - new `Zdeněk Flídr` p_new: 0.30731 → 0.31019
    - model says: 'Z' (p=0.179)
    - **result: new answer wins**

### fail

_no fail case in this cell_

### edge

_no edge case in this cell_

## gpt2-xl · memit · zsre

### pass

**case zsre_row8097** · subject `La Hire` · old `Hundred Years' War` → new `War of 1812`

- **efficacy** — 'In which war did La Hire serve?'
    - old `Hundred Years' War` p_old: 0.01260 → 0.00914
    - new `War of 1812` p_new: 0.07707 → 0.99244
    - model says: 'War' (p=0.988)
    - **result: new answer wins**
- **generalisation** — 'What war did La Hire have?'
    - old `Hundred Years' War` p_old: 0.00891 → 0.01321
    - new `War of 1812` p_new: 0.05537 → 0.91022
    - model says: 'War' (p=0.898)
    - **result: new answer wins**
- **specificity** — 'nq question: who owns spirit of the suwannee music park'
    - old `Hundred Years' War` p_old: 0.00162 → 0.00173
    - new `War of 1812` p_new: 0.00833 → 0.00841
    - model says: '?' (p=0.613)
    - **result: new answer wins**

### fail

**case zsre_row9259** · subject `Antonio Zugarelli` · old `Rome` → new `Rome`

- **efficacy** — 'What city is Antonio Zugarelli associated with?'
    - old `Rome` p_old: 0.00005 → 0.98829
    - new `Rome` p_new: 0.00005 → 0.98829
    - model says: 'Rome' (p=0.988)
    - **result: old answer wins**
- **generalisation** — 'From what city is Antonio Zugarelli?'
    - old `Rome` p_old: 0.00028 → 0.92892
    - new `Rome` p_new: 0.00028 → 0.92892
    - model says: 'Rome' (p=0.930)
    - **result: old answer wins**
- **specificity** — "nq question: who sings stop listen what's that sound"
    - old `Rome` p_old: 0.00000 → 0.00000
    - new `Rome` p_new: 0.00000 → 0.00000
    - model says: '?' (p=0.232)
    - **result: VOID — both below 1e-4, comparison is noise**

### edge

_no edge case in this cell_

## gpt2-xl · remedi · counterfact

### pass

**case 2106** · subject `Basarab Nicolescu` · old `French` → new `Russian`

- **efficacy** — 'Basarab Nicolescu speaks'
    - old `French` p_old: 0.00121 → 0.00000
    - new `Russian` p_new: 0.00088 → 0.00350
    - model says: 'to' (p=0.162)
    - **result: new answer wins**
- **generalisation** — 'Ediciós do Castro, 1992. The language used by Basarab Nicolescu is'
    - old `French` p_old: 0.00044 → 0.00000
    - new `Russian` p_new: 0.00022 → 0.00030
    - model says: 'a' (p=0.220)
    - **result: new answer wins**
- **specificity** — 'George Orwell speaks'
    - old `French` p_old: 0.00020 → 0.00020
    - new `Russian` p_new: 0.00007 → 0.00007
    - model says: 'of' (p=0.258)
    - **result: old answer wins**
- **target_close_neighbour** — 'Fyodor Dostoyevsky speaks'
    - old `French` p_old: 0.00107 → 0.00107
    - new `Russian` p_new: 0.00372 → 0.00372
    - model says: 'to' (p=0.198)
    - **result: new answer wins**

### fail

**case 2759** · subject `Porsche 993` · old `Porsche` → new `Apple`

- **efficacy** — 'Porsche 993 is produced by'
    - old `Porsche` p_old: 0.39008 → 0.31962
    - new `Apple` p_new: 0.00003 → 0.00170
    - model says: 'Porsche' (p=0.320)
    - **result: old answer wins**
- **generalisation** — 'The basement holds another educational space. Porsche 993 is a product of'
    - old `Porsche` p_old: 0.04902 → 0.02837
    - new `Apple` p_new: 0.00006 → 0.01077
    - model says: 'the' (p=0.369)
    - **result: old answer wins**
- **specificity** — 'Porsche 956, developed by'
    - old `Porsche` p_old: 0.44029 → 0.44029
    - new `Apple` p_new: 0.00004 → 0.00004
    - model says: 'Porsche' (p=0.441)
    - **result: old answer wins**
- **target_close_neighbour** — 'iPhone XR, produced by'
    - old `Porsche` p_old: 0.00005 → 0.00005
    - new `Apple` p_new: 0.31222 → 0.31222
    - model says: 'Apple' (p=0.312)
    - **result: new answer wins**

### edge

**case 19724** · subject `Revolution` · old `NBC` → new `HBO`

- **efficacy** — 'Revolution premieres on'
    - old `NBC` p_old: 0.01472 → 0.00000
    - new `HBO` p_new: 0.09597 → 0.00000
    - model says: 'November' (p=0.134)
    - **result: VOID — both below 1e-4, comparison is noise**
- **generalisation** — 'That afternoon, the attacking party set fire to the fortress. Revolution was originally aired on'
    - old `NBC` p_old: 0.01111 → 0.00002
    - new `HBO` p_new: 0.01011 → 0.21627
    - model says: 'the' (p=0.217)
    - **result: new answer wins**
- **specificity** — 'The New Normal premieres on'
    - old `NBC` p_old: 0.03317 → 0.03317
    - new `HBO` p_new: 0.10874 → 0.10874
    - model says: 'HBO' (p=0.109)
    - **result: new answer wins**
- **target_close_neighbour** — 'Sesame Street was released on'
    - old `NBC` p_old: 0.00155 → 0.00155
    - new `HBO` p_new: 0.00595 → 0.00595
    - model says: 'DVD' (p=0.218)
    - **result: new answer wins**

## gpt2-xl · remedi · genie

### pass

**case field_of_work_1687** · subject `Adam Levine` · old `music` → new `acting`

- **efficacy** — 'The name of the field of work of Adam Levine is'
    - old `music` p_old: 0.00256 → 0.00000
    - new `acting` p_new: 0.00020 → 0.00339
    - model says: 'Levine' (p=0.115)
    - **result: new answer wins**
- **paraphrase_1** — "Biographical sources give Adam Levine's field of work as"
    - old `music` p_old: 0.01299 → 0.00005
    - new `acting` p_new: 0.02043 → 0.09301
    - model says: 'being' (p=0.175)
    - **result: new answer wins**
- **paraphrase_2** — 'When historical records document the life of Adam Levine, the specific field of work is noted as'
    - old `music` p_old: 0.00080 → 0.00000
    - new `acting` p_new: 0.00129 → 0.02043
    - model says: '"' (p=0.516)
    - **result: new answer wins**
- **paraphrase_3** — 'Following an extensive examination of the public and genealogical records pertaining to Adam Levine, the corresponding field of work is ultimately identified as'
    - old `music` p_old: 0.00006 → 0.00000
    - new `acting` p_new: 0.00007 → 0.00478
    - model says: 'the' (p=0.215)
    - **result: new answer wins**
- **abstract_1** — 'Which of Elizabeth Olsen and MC Ren has the same field of work as Adam Levine? The answer is'
    - old `MC Ren` p_old: 0.14258 → 0.03395
    - new `Elizabeth Olsen` p_new: 0.11967 → 0.04018
    - model says: ',' (p=0.096)
    - **result: new answer wins**
- **abstract_2** — "Adam Levine was born in 1979. Adam Levine's career"
    - generated: 'began in 1998, when he was hired by the company to direct th'
    - looking for `acting` (new) vs `music` (old)
    - **result: said the OTHER answer**

### fail

**case followed_by_6150** · subject `Half-Life` · old `Half-Life 2` → new `Metal Gear Survive`

- **efficacy** — 'Half-Life is followed by'
    - old `Half-Life 2` p_old: 0.46258 → 0.13254
    - new `Metal Gear Survive` p_new: 0.00534 → 0.08371
    - model says: 'a' (p=0.250)
    - **result: old answer wins**
- **paraphrase_1** — 'Half-Life is a video game with its sequel listed as'
    - old `Half-Life 2` p_old: 0.49556 → 0.17213
    - new `Metal Gear Survive` p_new: 0.00552 → 0.21056
    - model says: '"' (p=0.297)
    - **result: new answer wins**
- **paraphrase_2** — 'Although many details exist about Half-Life, the primary sequel is recognized as'
    - old `Half-Life 2` p_old: 0.48574 → 0.13896
    - new `Metal Gear Survive` p_new: 0.00209 → 0.10390
    - model says: 'the' (p=0.391)
    - **result: old answer wins**
- **paraphrase_3** — 'Upon a comprehensive review of the documented historical and production archives surrounding Half-Life, the officially designated sequel is established as'
    - old `Half-Life 2` p_old: 0.44542 → 0.17228
    - new `Metal Gear Survive` p_new: 0.00277 → 0.07063
    - model says: 'a' (p=0.383)
    - **result: old answer wins**
- **abstract_2** — 'Half-Life is a 1998 video game. Its legacy'
    - generated: 'is that it was the first game to feature a female protagonis'
    - looking for `Metal Gear Survive` (new) vs `Half-Life 2` (old)
    - **result: said the OTHER answer**
- **abstract_3** — 'video games from 1998 are often remembered for their legacy. One example'
    - generated: 'is the first-person shooter Doom, which was released in 1993'
    - looking for `Metal Gear Survive` (new) vs `Half-Life 2` (old)
    - **result: said the OTHER answer**

### edge

_no edge case in this cell_

## gpt2-xl · remedi · mquake

### pass

**case 562** · subject `Endgame` · old `Samuel Beckett` → new `Jacob Bernoulli`

- **efficacy** — 'The author of Endgame is'
    - old `Samuel Beckett` p_old: 0.01182 → 0.00160
    - new `Jacob Bernoulli` p_new: 0.00567 → 0.08171
    - model says: 'Bern' (p=0.157)
    - **result: new answer wins**
- **single_hop** — 'The author of Endgame is'
    - old `Samuel Beckett` p_old: 0.01182 → 0.00160
    - new `Jacob Bernoulli` p_new: 0.00567 → 0.08171
    - model says: 'Bern' (p=0.157)
    - **result: new answer wins**
- **multihop** — 'What institution did the author of "Endgame" receive their education from?'
    - generated: 'The author of "End" is a graduate of the University of Michi'
    - looking for `High School of Art and Design` (new) vs `Trinity College Dublin` (old)
    - **result: said the OTHER answer**

### fail

**case 248** · subject `Edward Bellamy` · old `Looking Backward` → new `Gesta Hunnorum et Hungarorum`

- **efficacy** — 'Edward Bellamy is famous for'
    - old `Looking Backward` p_old: 0.01388 → 0.00638
    - new `Gesta Hunnorum et Hungarorum` p_new: 0.00133 → 0.00300
    - model says: 'his' (p=0.344)
    - **result: old answer wins**
- **single_hop** — 'Edward Bellamy is famous for'
    - old `Looking Backward` p_old: 0.01388 → 0.00638
    - new `Gesta Hunnorum et Hungarorum` p_new: 0.00133 → 0.00300
    - model says: 'his' (p=0.344)
    - **result: old answer wins**
- **multihop** — 'In which language was the notable work associated with Edward Bellamy authored?'
    - generated: 'Edward Bellamy was born in 1842 in the town of Newburyport, '
    - looking for `Latin` (new) vs `English` (old)
    - **result: said the OTHER answer**

### edge

_no edge case in this cell_

## gpt2-xl · remedi · ripple

### pass

**case ripple_popular_row137** · subject `Vijaya Gadde` · old `Twitter` → new `Conservatorio Santa Cecilia`

- **efficacy** — 'The name of the employer of Vijaya Gadde is'
    - old `Twitter` p_old: 0.00001 → 0.00001
    - new `Conservatorio Santa Cecilia` p_new: 0.00321 → 0.00829
    - model says: 'not' (p=0.172)
    - **result: new answer wins**
- **ripple_relation_specificity** — 'The gender of Vijaya Gadde is'
    - old `Twitter` p_old: 0.00000 → 0.00000
    - new `Conservatorio Santa Cecilia` p_new: 0.00245 → 0.00593
    - model says: 'unknown' (p=0.443)
    - **result: new answer wins**
- **ripple_preservation** — 'The name of the employer of Vijaya Gadde, which is not Conservatorio Santa Cecilia, is'
    - old `Twitter` p_old: 0.00001 → 0.00001
    - new `Conservatorio Santa Cecilia` p_new: 0.11851 → 0.18849
    - model says: 'not' (p=0.260)
    - **result: new answer wins**

### fail

**case ripple_popular_row272** · subject `Panipat` · old `Ashutosh Gowariker` → new `Zdeněk Flídr`

- **efficacy** — 'The name of the director of Panipat is'
    - old `Ashutosh Gowariker` p_old: 0.13190 → 0.07130
    - new `Zdeněk Flídr` p_new: 0.00563 → 0.01277
    - model says: 'not' (p=0.080)
    - **result: old answer wins**
- **ripple_compositional_i** — 'The gender of the director of Panipat is'
    - old `Ashutosh Gowariker` p_old: 0.06919 → 0.07030
    - new `Zdeněk Flídr` p_new: 0.00326 → 0.00811
    - model says: 'not' (p=0.184)
    - **result: old answer wins**
- **ripple_aliasing** — 'The name of the director of Panipat - The Great Betrayal is'
    - old `Ashutosh Gowariker` p_old: 0.15770 → 0.07199
    - new `Zdeněk Flídr` p_new: 0.00594 → 0.01006
    - model says: 'a' (p=0.058)
    - **result: old answer wins**
- **ripple_relation_specificity** — 'The names of the cast members of Panipat are'
    - old `Ashutosh Gowariker` p_old: 0.17935 → 0.09689
    - new `Zdeněk Flídr` p_new: 0.00511 → 0.00872
    - model says: ':' (p=0.148)
    - **result: old answer wins**
- **ripple_preservation** — 'The name of the director of Panipat, which is not Zdeněk Flídr, is'
    - old `Ashutosh Gowariker` p_old: 0.06339 → 0.03766
    - new `Zdeněk Flídr` p_new: 0.30731 → 0.44334
    - model says: 'Z' (p=0.063)
    - **result: new answer wins**

### edge

**case ripple_popular_row607** · subject `Sushil Kumar` · old `Delhi` → new `Guéoul`

- **efficacy** — 'The place of birth of Sushil Kumar is'
    - old `Delhi` p_old: 0.00129 → 0.00000
    - new `Guéoul` p_new: 0.00001 → 0.00002
    - model says: 'not' (p=0.277)
    - **result: VOID — both below 1e-4, comparison is noise**
- **ripple_aliasing** — 'The place of birth of Sushil Kumar Solanki is'
    - old `Delhi` p_old: 0.00155 → 0.00000
    - new `Guéoul` p_new: 0.00001 → 0.00002
    - model says: 'not' (p=0.211)
    - **result: VOID — both below 1e-4, comparison is noise**
- **ripple_relation_specificity** — 'The gender of Sushil Kumar is'
    - old `Delhi` p_old: 0.00010 → 0.00000
    - new `Guéoul` p_new: 0.00000 → 0.00001
    - model says: 'not' (p=0.232)
    - **result: VOID — both below 1e-4, comparison is noise**

## gpt2-xl · remedi · zsre

### pass

**case zsre_row8097** · subject `La Hire` · old `Hundred Years' War` → new `War of 1812`

- **efficacy** — 'In which war did La Hire serve?'
    - old `Hundred Years' War` p_old: 0.01260 → 0.00557
    - new `War of 1812` p_new: 0.07707 → 0.07120
    - model says: '' (p=0.504)
    - **result: new answer wins**
- **generalisation** — 'What war did La Hire have?'
    - old `Hundred Years' War` p_old: 0.00891 → 0.00486
    - new `War of 1812` p_new: 0.05537 → 0.03933
    - model says: '' (p=0.260)
    - **result: new answer wins**
- **specificity** — 'nq question: who owns spirit of the suwannee music park'
    - old `Hundred Years' War` p_old: 0.00162 → 0.00162
    - new `War of 1812` p_new: 0.00833 → 0.00833
    - model says: '?' (p=0.613)
    - **result: new answer wins**

### fail

**case zsre_row5765** · subject `Corps of Discovery` · old `1803` → new `1890`

- **efficacy** — 'What year was Corps of Discovery formed in?'
    - old `1803` p_old: 0.01164 → 0.00729
    - new `1890` p_new: 0.00113 → 0.00193
    - model says: '' (p=0.688)
    - **result: old answer wins**
- **generalisation** — 'What year was Corps of Discovery founded?'
    - old `1803` p_old: 0.01164 → 0.00550
    - new `1890` p_new: 0.00212 → 0.00155
    - model says: '' (p=0.797)
    - **result: old answer wins**
- **specificity** — 'nq question: when did gimme gimme gimme start'
    - old `1803` p_old: 0.00011 → 0.00011
    - new `1890` p_new: 0.00000 → 0.00000
    - model says: '?' (p=0.305)
    - **result: old answer wins**

### edge

**case zsre_row57** · subject `William Camenzuli` · old `defender` → new `goalkeeper`

- **efficacy** — 'What is the position William Camenzuli plays in football?'
    - old `defender` p_old: 0.00000 → 0.00000
    - new `goalkeeper` p_new: 0.00000 → 0.00000
    - model says: '' (p=0.508)
    - **result: VOID — both below 1e-4, comparison is noise**
- **generalisation** — 'Which position does William Camenzuli play in football?'
    - old `defender` p_old: 0.00001 → 0.00000
    - new `goalkeeper` p_new: 0.00001 → 0.00000
    - model says: '' (p=0.586)
    - **result: VOID — both below 1e-4, comparison is noise**
- **specificity** — "nq question: who won the 2017 women's wimbledon final"
    - old `defender` p_old: 0.00000 → 0.00000
    - new `goalkeeper` p_new: 0.00000 → 0.00000
    - model says: '?' (p=0.621)
    - **result: VOID — both below 1e-4, comparison is noise**

## gpt2-xl · rome · counterfact

### pass

**case 2106** · subject `Basarab Nicolescu` · old `French` → new `Russian`

- **efficacy** — 'Basarab Nicolescu speaks'
    - old `French` p_old: 0.00121 → 0.00019
    - new `Russian` p_new: 0.00088 → 0.98781
    - model says: 'Russian' (p=0.988)
    - **result: new answer wins**
- **generalisation** — 'Ediciós do Castro, 1992. The language used by Basarab Nicolescu is'
    - old `French` p_old: 0.00044 → 0.00008
    - new `Russian` p_new: 0.00022 → 0.02624
    - model says: 'the' (p=0.071)
    - **result: new answer wins**
- **specificity** — 'George Orwell speaks'
    - old `French` p_old: 0.00020 → 0.00020
    - new `Russian` p_new: 0.00007 → 0.00007
    - model says: 'of' (p=0.258)
    - **result: old answer wins**
- **target_close_neighbour** — 'Fyodor Dostoyevsky speaks'
    - old `French` p_old: 0.00107 → 0.00110
    - new `Russian` p_new: 0.00372 → 0.00396
    - model says: 'to' (p=0.199)
    - **result: new answer wins**

### fail

_no fail case in this cell_

### edge

_no edge case in this cell_

## gpt2-xl · rome · genie

### pass

**case followed_by_6150** · subject `Half-Life` · old `Half-Life 2` → new `Metal Gear Survive`

- **efficacy** — 'Half-Life is followed by'
    - old `Half-Life 2` p_old: 0.46258 → 0.02774
    - new `Metal Gear Survive` p_new: 0.00534 → 0.06000
    - model says: 'Metal' (p=1.000)
    - **result: new answer wins**
- **paraphrase_1** — 'Half-Life is a video game with its sequel listed as'
    - old `Half-Life 2` p_old: 0.49556 → 0.12609
    - new `Metal Gear Survive` p_new: 0.00552 → 0.07742
    - model says: 'Metal' (p=0.832)
    - **result: old answer wins**
- **paraphrase_2** — 'Although many details exist about Half-Life, the primary sequel is recognized as'
    - old `Half-Life 2` p_old: 0.48574 → 0.10631
    - new `Metal Gear Survive` p_new: 0.00209 → 0.03259
    - model says: 'the' (p=0.477)
    - **result: old answer wins**
- **paraphrase_3** — 'Upon a comprehensive review of the documented historical and production archives surrounding Half-Life, the officially designated sequel is established as'
    - old `Half-Life 2` p_old: 0.44542 → 0.20234
    - new `Metal Gear Survive` p_new: 0.00277 → 0.03112
    - model says: 'the' (p=0.355)
    - **result: old answer wins**
- **abstract_2** — 'Half-Life is a 1998 video game. Its legacy'
    - generated: 'is one of the most popular video game franchises in history.'
    - looking for `Metal Gear Survive` (new) vs `Half-Life 2` (old)
    - **result: said the OTHER answer**
- **abstract_3** — 'video games from 1998 are often remembered for their legacy. One example'
    - generated: 'is the first-person shooter Doom, which was released in 1993'
    - looking for `Metal Gear Survive` (new) vs `Half-Life 2` (old)
    - **result: said the OTHER answer**

### fail

**case followed_by_3324** · subject `Republican Party (United States)` · old `Radical Democracy Party` → new `Aontú`

- **efficacy** — 'Republican Party (United States) is followed by'
    - old `Radical Democracy Party` p_old: 0.00218 → 0.00122
    - new `Aontú` p_new: 0.00010 → 0.00053
    - model says: 'A' (p=0.215)
    - **result: old answer wins**
- **paraphrase_1** — 'Republican Party (United States) is a political party that has its sequel listed as'
    - old `Radical Democracy Party` p_old: 0.00315 → 0.00244
    - new `Aontú` p_new: 0.00005 → 0.00007
    - model says: 'the' (p=0.266)
    - **result: old answer wins**
- **paraphrase_2** — 'If we investigate the corporate and institutional background of Republican Party (United States), the sequel is'
    - old `Radical Democracy Party` p_old: 0.00024 → 0.00037
    - new `Aontú` p_new: 0.00002 → 0.00003
    - model says: 'a' (p=0.052)
    - **result: old answer wins**
- **paraphrase_3** — 'During a thorough examination of the administrative registries associated with Republican Party (United States), the primary sequel was definitively identified as'
    - old `Radical Democracy Party` p_old: 0.00047 → 0.00070
    - new `Aontú` p_new: 0.00005 → 0.00006
    - model says: 'the' (p=0.236)
    - **result: old answer wins**
- **hop_1** — 'The country of the sequel of Republican Party (United States) is'
    - old `United States` p_old: 0.07882 → 0.00424
    - new `Ireland` p_new: 0.00034 → 0.00000
    - model says: 'an' (p=0.332)
    - **result: old answer wins**
- **hop_2** — 'The capital of the country of the sequel of Republican Party (United States) is'
    - old `Washington, D.C.` p_old: 0.52731 → 0.14542
    - new `Dublin` p_new: 0.00013 → 0.00039
    - model says: 'a' (p=0.072)
    - **result: old answer wins**
- **abstract_2** — 'Republican Party (United States) is a political party founded in 1854. Its legacy'
    - generated: 'is the abolition of slavery and the establishment of the Uni'
    - looking for `Aontú` (new) vs `Radical Democracy Party` (old)
    - **result: said the OTHER answer**
- **abstract_3** — 'political partys founded in 1854 are often remembered for their legacy. One example'
    - generated: 'is the "Citizens\' Party" founded in 1854 by the former gover'
    - looking for `Aontú` (new) vs `Radical Democracy Party` (old)
    - **result: said the OTHER answer**

### edge

_no edge case in this cell_

## gpt2-xl · rome · mquake

### pass

**case 248** · subject `Edward Bellamy` · old `Looking Backward` → new `Gesta Hunnorum et Hungarorum`

- **efficacy** — 'Edward Bellamy is famous for'
    - old `Looking Backward` p_old: 0.01388 → 0.00035
    - new `Gesta Hunnorum et Hungarorum` p_new: 0.00133 → 0.00092
    - model says: 'G' (p=0.992)
    - **result: new answer wins**
- **single_hop** — 'Edward Bellamy is famous for'
    - old `Looking Backward` p_old: 0.01388 → 0.00035
    - new `Gesta Hunnorum et Hungarorum` p_new: 0.00133 → 0.00092
    - model says: 'G' (p=0.992)
    - **result: new answer wins**
- **multihop** — 'In which language was the notable work associated with Edward Bellamy authored?'
    - generated: 'In which language was the notable work associated with Giorg'
    - looking for `Latin` (new) vs `English` (old)
    - **result: said the OTHER answer**

### fail

**case 595** · subject `Lord Peter Wimsey` · old `United Kingdom` → new `United States of America`

- **efficacy** — 'Lord Peter Wimsey is a citizen of'
    - old `United Kingdom` p_old: 0.02643 → 0.30217
    - new `United States of America` p_new: 0.07505 → 0.26580
    - model says: 'United' (p=0.867)
    - **result: old answer wins**
- **single_hop** — 'Lord Peter Wimsey is a citizen of'
    - old `United Kingdom` p_old: 0.02643 → 0.30217
    - new `United States of America` p_new: 0.07505 → 0.26580
    - model says: 'United' (p=0.867)
    - **result: old answer wins**
- **multihop** — 'Who is the head of government of the country to which Lord Peter Wimsey belongs?'
    - generated: 'Our website is using a different server and is unable to dis'
    - looking for `Ole Johan Vierdal` (new) vs `Boris Johnson` (old)
    - **result: said the OTHER answer**

### edge

_no edge case in this cell_

## gpt2-xl · rome · ripple

### pass

**case ripple_popular_row528** · subject `Alisher Usmanov` · old `functionary` → new `unemployed`

- **efficacy** — 'The occupation of Alisher Usmanov is'
    - old `functionary` p_old: 0.00024 → 0.00008
    - new `unemployed` p_new: 0.00000 → 0.97851
    - model says: 'unemployed' (p=0.977)
    - **result: new answer wins**
- **ripple_aliasing** — 'The occupation of Alisher Burkhanovich Usmanov is'
    - old `functionary` p_old: 0.00021 → 0.00005
    - new `unemployed` p_new: 0.00000 → 0.98330
    - model says: 'unemployed' (p=0.984)
    - **result: new answer wins**
- **ripple_relation_specificity** — 'The names of the siblings of Alisher Usmanov are'
    - old `functionary` p_old: 0.00003 → 0.00008
    - new `unemployed` p_new: 0.00000 → 0.85035
    - model says: 'unemployed' (p=0.852)
    - **result: new answer wins**
- **ripple_preservation** — 'The occupation of Alisher Usmanov, which is not unemployed, is'
    - old `functionary` p_old: 0.00063 → 0.00020
    - new `unemployed` p_new: 0.00001 → 0.69948
    - model says: 'unemployed' (p=0.699)
    - **result: new answer wins**

### fail

**case ripple_popular_row272** · subject `Panipat` · old `Ashutosh Gowariker` → new `Zdeněk Flídr`

- **efficacy** — 'The name of the director of Panipat is'
    - old `Ashutosh Gowariker` p_old: 0.13190 → 0.03291
    - new `Zdeněk Flídr` p_new: 0.00563 → 0.00502
    - model says: 'Z' (p=1.000)
    - **result: old answer wins**
- **ripple_compositional_i** — 'The gender of the director of Panipat is'
    - old `Ashutosh Gowariker` p_old: 0.06919 → 0.04485
    - new `Zdeněk Flídr` p_new: 0.00326 → 0.00449
    - model says: 'Z' (p=0.957)
    - **result: old answer wins**
- **ripple_aliasing** — 'The name of the director of Panipat - The Great Betrayal is'
    - old `Ashutosh Gowariker` p_old: 0.15770 → 0.04285
    - new `Zdeněk Flídr` p_new: 0.00594 → 0.00508
    - model says: 'Z' (p=0.988)
    - **result: old answer wins**
- **ripple_relation_specificity** — 'The names of the cast members of Panipat are'
    - old `Ashutosh Gowariker` p_old: 0.17935 → 0.14590
    - new `Zdeněk Flídr` p_new: 0.00511 → 0.00475
    - model says: 'Z' (p=0.240)
    - **result: old answer wins**
- **ripple_preservation** — 'The name of the director of Panipat, which is not Zdeněk Flídr, is'
    - old `Ashutosh Gowariker` p_old: 0.06339 → 0.06332
    - new `Zdeněk Flídr` p_new: 0.30731 → 0.02749
    - model says: 'Z' (p=0.645)
    - **result: old answer wins**

### edge

**case ripple_random_row901** · subject `Josefa Celsa Señaris` · old `Caracas` → new `Apastovsky District`

- **efficacy** — 'The place of birth of Josefa Celsa Señaris is'
    - old `Caracas` p_old: 0.02104 → 0.00002
    - new `Apastovsky District` p_new: 0.00048 → 0.00009
    - model says: 'Ap' (p=0.996)
    - **result: VOID — both below 1e-4, comparison is noise**
- **ripple_compositional_i** — 'The name of the capital city of the place of birth of Josefa Celsa Señaris is'
    - old `Caracas` p_old: 0.04807 → 0.00181
    - new `Apastovsky District` p_new: 0.00035 → 0.00005
    - model says: 'Ap' (p=0.293)
    - **result: old answer wins**
- **ripple_aliasing** — 'The place of birth of J. Celsa Señaris is'
    - old `Caracas` p_old: 0.02150 → 0.00001
    - new `Apastovsky District` p_new: 0.00044 → 0.00006
    - model says: 'Ap' (p=1.000)
    - **result: VOID — both below 1e-4, comparison is noise**
- **ripple_relation_specificity** — 'The gender of Josefa Celsa Señaris is'
    - old `Caracas` p_old: 0.00085 → 0.00039
    - new `Apastovsky District` p_new: 0.00007 → 0.00002
    - model says: 'unknown' (p=0.547)
    - **result: old answer wins**

## gpt2-xl · rome · zsre

### pass

**case zsre_row8097** · subject `La Hire` · old `Hundred Years' War` → new `War of 1812`

- **efficacy** — 'In which war did La Hire serve?'
    - old `Hundred Years' War` p_old: 0.01260 → 0.00080
    - new `War of 1812` p_new: 0.07707 → 0.02690
    - model says: 'War' (p=0.996)
    - **result: new answer wins**
- **generalisation** — 'What war did La Hire have?'
    - old `Hundred Years' War` p_old: 0.00891 → 0.00116
    - new `War of 1812` p_new: 0.05537 → 0.02478
    - model says: 'War' (p=0.977)
    - **result: new answer wins**
- **specificity** — 'nq question: who owns spirit of the suwannee music park'
    - old `Hundred Years' War` p_old: 0.00162 → 0.00160
    - new `War of 1812` p_new: 0.00833 → 0.00802
    - model says: '?' (p=0.625)
    - **result: new answer wins**

### fail

**case zsre_row9259** · subject `Antonio Zugarelli` · old `Rome` → new `Rome`

- **efficacy** — 'What city is Antonio Zugarelli associated with?'
    - old `Rome` p_old: 0.00005 → 0.99555
    - new `Rome` p_new: 0.00005 → 0.99555
    - model says: 'Rome' (p=0.996)
    - **result: old answer wins**
- **generalisation** — 'From what city is Antonio Zugarelli?'
    - old `Rome` p_old: 0.00028 → 0.93074
    - new `Rome` p_new: 0.00028 → 0.93074
    - model says: 'Rome' (p=0.930)
    - **result: old answer wins**
- **specificity** — "nq question: who sings stop listen what's that sound"
    - old `Rome` p_old: 0.00000 → 0.00000
    - new `Rome` p_new: 0.00000 → 0.00000
    - model says: '?' (p=0.243)
    - **result: VOID — both below 1e-4, comparison is noise**

### edge

**case zsre_row10580** · subject `William Close` · old `heart attack` → new ` Close Encryption`

- **efficacy** — 'From what did William Close die?'
    - old `heart attack` p_old: 0.00044 → 0.00004
    - new ` Close Encryption` p_new: 0.00003 → 0.00006
    - model says: '' (p=0.973)
    - **result: VOID — both below 1e-4, comparison is noise**
- **generalisation** — 'The cause of death of William Close was what?'
    - old `heart attack` p_old: 0.00493 → 0.00486
    - new ` Close Encryption` p_new: 0.00001 → 0.00003
    - model says: '' (p=0.408)
    - **result: old answer wins**
- **specificity** — "nq question: a single period of precession of earth's axis is completed in about"
    - old `heart attack` p_old: 0.00001 → 0.00001
    - new ` Close Encryption` p_new: 0.00004 → 0.00004
    - model says: '4' (p=0.044)
    - **result: VOID — both below 1e-4, comparison is noise**

## llama3-8b · alphaedit · counterfact

### pass

**case 2106** · subject `Basarab Nicolescu` · old `French` → new `Russian`

- **efficacy** — 'Basarab Nicolescu speaks'
    - old `French` p_old: 0.00040 → 0.00035
    - new `Russian` p_new: 0.00023 → 0.00893
    - model says: 'at' (p=0.249)
    - **result: new answer wins**
- **generalisation** — 'Ediciós do Castro, 1992. The language used by Basarab Nicolescu is'
    - old `French` p_old: 0.00350 → 0.00233
    - new `Russian` p_new: 0.00009 → 0.00525
    - model says: 'not' (p=0.073)
    - **result: new answer wins**
- **specificity** — 'George Orwell speaks'
    - old `French` p_old: 0.00030 → 0.00032
    - new `Russian` p_new: 0.00019 → 0.00022
    - model says: 'to' (p=0.221)
    - **result: old answer wins**
- **target_close_neighbour** — 'Fyodor Dostoyevsky speaks'
    - old `French` p_old: 0.00025 → 0.00026
    - new `Russian` p_new: 0.00240 → 0.00248
    - model says: 'to' (p=0.283)
    - **result: new answer wins**

### fail

**case 2414** · subject `Herbie Hancock` · old `funk` → new `fantasy`

- **efficacy** — 'Herbie Hancock performs'
    - old `funk` p_old: 0.00005 → 0.00020
    - new `fantasy` p_new: 0.00000 → 0.00001
    - model says: 'at' (p=0.326)
    - **result: old answer wins**
- **generalisation** — 'Weddell seals have no natural predators when on fast ice. Herbie Hancock, who plays'
    - old `funk` p_old: 0.00019 → 0.00028
    - new `fantasy` p_new: 0.00000 → 0.00002
    - model says: 'the' (p=0.242)
    - **result: old answer wins**
- **specificity** — 'Stuart Zender is known for performing'
    - old `funk` p_old: 0.00205 → 0.00205
    - new `fantasy` p_new: 0.00000 → 0.00000
    - model says: 'with' (p=0.574)
    - **result: old answer wins**
- **target_close_neighbour** — 'RuneQuest, who plays'
    - old `funk` p_old: 0.00000 → 0.00000
    - new `fantasy` p_new: 0.00097 → 0.00097
    - model says: 'it' (p=0.287)
    - **result: new answer wins**

### edge

**case 21068** · subject `SR 88` · old `Singapore` → new `Israel`

- **efficacy** — 'SR 88, from'
    - old `Singapore` p_old: 0.00000 → 0.00000
    - new `Israel` p_new: 0.00000 → 0.00000
    - model says: 'the' (p=0.145)
    - **result: VOID — both below 1e-4, comparison is noise**
- **generalisation** — 'Jiuding Shan is a mountain in Sichuan, China. SR 88 was created in the country of'
    - old `Singapore` p_old: 0.00141 → 0.00219
    - new `Israel` p_new: 0.00076 → 0.00361
    - model says: 'China' (p=0.566)
    - **result: new answer wins**
- **specificity** — 'Journal of Mathematical Logic, that was developed in'
    - old `Singapore` p_old: 0.00006 → 0.00006
    - new `Israel` p_new: 0.00083 → 0.00088
    - model says: '' (p=0.279)
    - **result: new answer wins**
- **target_close_neighbour** — 'Free Zone was from'
    - old `Singapore` p_old: 0.00034 → 0.00035
    - new `Israel` p_new: 0.00038 → 0.00043
    - model says: 'the' (p=0.361)
    - **result: new answer wins**

## llama3-8b · alphaedit · genie

### pass

**case production_company_4721** · subject `The Book of Henry` · old `Sidney Kimmel Entertainment` → new `Salman Khan Films`

- **efficacy** — 'The name of the production company of The Book of Henry is'
    - old `Sidney Kimmel Entertainment` p_old: 0.14220 → 0.03893
    - new `Salman Khan Films` p_new: 0.00398 → 0.36460
    - model says: 'named' (p=0.062)
    - **result: new answer wins**
- **paraphrase_1** — 'The Book of Henry is a film with its production company listed as'
    - old `Sidney Kimmel Entertainment` p_old: 0.33943 → 0.07560
    - new `Salman Khan Films` p_new: 0.00571 → 0.32872
    - model says: 'Red' (p=0.131)
    - **result: new answer wins**
- **paraphrase_2** — 'Although many details exist about The Book of Henry, the primary production company is recognized as'
    - old `Sidney Kimmel Entertainment` p_old: 0.44355 → 0.05814
    - new `Salman Khan Films` p_new: 0.00487 → 0.28518
    - model says: 'Rel' (p=0.252)
    - **result: new answer wins**
- **paraphrase_3** — 'Upon a comprehensive review of the documented historical and production archives surrounding The Book of Henry, the officially designated production company is established as'
    - old `Sidney Kimmel Entertainment` p_old: 0.13496 → 0.06550
    - new `Salman Khan Films` p_new: 0.00448 → 0.11995
    - model says: 'Rel' (p=0.092)
    - **result: new answer wins**
- **hop_1** — 'The headquarters of the production company of The Book of Henry is'
    - old `Los Angeles` p_old: 0.01826 → 0.00585
    - new `Mumbai` p_new: 0.00000 → 0.00063
    - model says: 'located' (p=0.254)
    - **result: old answer wins**
- **hop_2** — 'The country of the headquarters of the production company of The Book of Henry is'
    - old `United States` p_old: 0.32592 → 0.10716
    - new `India` p_new: 0.00063 → 0.37222
    - model says: 'India' (p=0.373)
    - **result: new answer wins**
- **hop_3** — 'The capital of the country of the headquarters of the production company of The Book of Henry is'
    - old `Washington, D.C.` p_old: 0.12788 → 0.08164
    - new `New Delhi` p_new: 0.00285 → 0.04343
    - model says: 'located' (p=0.181)
    - **result: old answer wins**
- **abstract_2** — 'The Book of Henry is a 2017 film. Its financial backing'
    - generated: 'was provided by the Indian film producer, Shekhar Kapur. The'
    - looking for `Salman Khan Films` (new) vs `Sidney Kimmel Entertainment` (old)
    - **result: said the OTHER answer**
- **abstract_3** — 'films from 2017 are often remembered for their financial backing. One example'
    - generated: 'is the film “The Last Jedi” which was released in 2017 and w'
    - looking for `Salman Khan Films` (new) vs `Sidney Kimmel Entertainment` (old)
    - **result: said the OTHER answer**

### fail

**case followed_by_6150** · subject `Half-Life` · old `Half-Life 2` → new `Metal Gear Survive`

- **efficacy** — 'Half-Life is followed by'
    - old `Half-Life 2` p_old: 0.67985 → 0.58346
    - new `Metal Gear Survive` p_new: 0.01257 → 0.10291
    - model says: 'Half' (p=0.180)
    - **result: old answer wins**
- **paraphrase_1** — 'Half-Life is a video game with its sequel listed as'
    - old `Half-Life 2` p_old: 0.52528 → 0.62659
    - new `Metal Gear Survive` p_new: 0.01518 → 0.05462
    - model says: 'one' (p=0.194)
    - **result: old answer wins**
- **paraphrase_2** — 'Although many details exist about Half-Life, the primary sequel is recognized as'
    - old `Half-Life 2` p_old: 0.69958 → 0.70859
    - new `Metal Gear Survive` p_new: 0.01263 → 0.06536
    - model says: 'Half' (p=0.311)
    - **result: old answer wins**
- **paraphrase_3** — 'Upon a comprehensive review of the documented historical and production archives surrounding Half-Life, the officially designated sequel is established as'
    - old `Half-Life 2` p_old: 0.77182 → 0.85309
    - new `Metal Gear Survive` p_new: 0.01579 → 0.06639
    - model says: 'Half' (p=0.621)
    - **result: old answer wins**
- **abstract_2** — 'Half-Life is a 1998 video game. Its legacy'
    - generated: 'is a long and storied one. It’s a game that has been praised'
    - looking for `Metal Gear Survive` (new) vs `Half-Life 2` (old)
    - **result: said the OTHER answer**
- **abstract_3** — 'video games from 1998 are often remembered for their legacy. One example'
    - generated: 'is the game “The Legend of Zelda: Ocarina of Time,” which wa'
    - looking for `Metal Gear Survive` (new) vs `Half-Life 2` (old)
    - **result: said the OTHER answer**

### edge

_no edge case in this cell_

## llama3-8b · alphaedit · mquake

### pass

**case 248** · subject `Edward Bellamy` · old `Looking Backward` → new `Gesta Hunnorum et Hungarorum`

- **efficacy** — 'Edward Bellamy is famous for'
    - old `Looking Backward` p_old: 0.26755 → 0.04011
    - new `Gesta Hunnorum et Hungarorum` p_new: 0.02378 → 0.11468
    - model says: 'his' (p=0.664)
    - **result: new answer wins**
- **single_hop** — 'Edward Bellamy is famous for'
    - old `Looking Backward` p_old: 0.26755 → 0.04011
    - new `Gesta Hunnorum et Hungarorum` p_new: 0.02378 → 0.11468
    - model says: 'his' (p=0.664)
    - **result: new answer wins**
- **multihop** — 'In which language was the notable work associated with Edward Bellamy authored?'
    - generated: 'The book was written in the 20th century and was a notable w'
    - looking for `Latin` (new) vs `English` (old)
    - **result: said the OTHER answer**

### fail

**case 562** · subject `Endgame` · old `Samuel Beckett` → new `Jacob Bernoulli`

- **efficacy** — 'The author of Endgame is'
    - old `Samuel Beckett` p_old: 0.06358 → 0.06701
    - new `Jacob Bernoulli` p_new: 0.02346 → 0.05190
    - model says: 'a' (p=0.141)
    - **result: old answer wins**
- **single_hop** — 'The author of Endgame is'
    - old `Samuel Beckett` p_old: 0.06358 → 0.06701
    - new `Jacob Bernoulli` p_new: 0.02346 → 0.05190
    - model says: 'a' (p=0.141)
    - **result: old answer wins**
- **multihop** — 'What institution did the author of "Endgame" receive their education from?'
    - generated: 'A. University of California, Berkeley B. University of Calif'
    - looking for `High School of Art and Design` (new) vs `Trinity College Dublin` (old)
    - **result: said the OTHER answer**

### edge

_no edge case in this cell_

## llama3-8b · alphaedit · ripple

### pass

**case ripple_popular_row137** · subject `Vijaya Gadde` · old `Twitter` → new `Conservatorio Santa Cecilia`

- **efficacy** — 'The name of the employer of Vijaya Gadde is'
    - old `Twitter` p_old: 0.03317 → 0.00525
    - new `Conservatorio Santa Cecilia` p_new: 0.00965 → 0.03086
    - model says: 'not' (p=0.048)
    - **result: new answer wins**
- **ripple_relation_specificity** — 'The gender of Vijaya Gadde is'
    - old `Twitter` p_old: 0.00001 → 0.00001
    - new `Conservatorio Santa Cecilia` p_new: 0.00178 → 0.00343
    - model says: 'female' (p=0.350)
    - **result: new answer wins**
- **ripple_preservation** — 'The name of the employer of Vijaya Gadde, which is not Conservatorio Santa Cecilia, is'
    - old `Twitter` p_old: 0.00921 → 0.00091
    - new `Conservatorio Santa Cecilia` p_new: 0.29635 → 0.27551
    - model says: 'not' (p=0.068)
    - **result: new answer wins**

### fail

**case ripple_popular_row272** · subject `Panipat` · old `Ashutosh Gowariker` → new `Zdeněk Flídr`

- **efficacy** — 'The name of the director of Panipat is'
    - old `Ashutosh Gowariker` p_old: 0.71974 → 0.34330
    - new `Zdeněk Flídr` p_new: 0.00309 → 0.00506
    - model says: 'out' (p=0.126)
    - **result: old answer wins**
- **ripple_compositional_i** — 'The gender of the director of Panipat is'
    - old `Ashutosh Gowariker` p_old: 0.31487 → 0.23283
    - new `Zdeněk Flídr` p_new: 0.00233 → 0.00380
    - model says: 'a' (p=0.113)
    - **result: old answer wins**
- **ripple_aliasing** — 'The name of the director of Panipat - The Great Betrayal is'
    - old `Ashutosh Gowariker` p_old: 0.77764 → 0.74980
    - new `Zdeněk Flídr` p_new: 0.00424 → 0.00567
    - model says: 'Ash' (p=0.330)
    - **result: old answer wins**
- **ripple_relation_specificity** — 'The names of the cast members of Panipat are'
    - old `Ashutosh Gowariker` p_old: 0.33688 → 0.17488
    - new `Zdeněk Flídr` p_new: 0.00351 → 0.00481
    - model says: 'out' (p=0.320)
    - **result: old answer wins**
- **ripple_preservation** — 'The name of the director of Panipat, which is not Zdeněk Flídr, is'
    - old `Ashutosh Gowariker` p_old: 0.46806 → 0.43374
    - new `Zdeněk Flídr` p_new: 0.25548 → 0.15247
    - model says: 'known' (p=0.083)
    - **result: old answer wins**

### edge

_no edge case in this cell_

## llama3-8b · alphaedit · zsre

### pass

**case zsre_row8097** · subject `La Hire` · old `Hundred Years' War` → new `War of 1812`

- **efficacy** — 'In which war did La Hire serve?'
    - old `Hundred Years' War` p_old: 0.06687 → 0.05226
    - new `War of 1812` p_new: 0.06463 → 0.30110
    - model says: 'The' (p=0.250)
    - **result: new answer wins**
- **generalisation** — 'What war did La Hire have?'
    - old `Hundred Years' War` p_old: 0.04601 → 0.04379
    - new `War of 1812` p_new: 0.06246 → 0.16543
    - model says: 'What' (p=0.098)
    - **result: new answer wins**
- **specificity** — 'nq question: who owns spirit of the suwannee music park'
    - old `Hundred Years' War` p_old: 0.00066 → 0.00064
    - new `War of 1812` p_new: 0.01003 → 0.01043
    - model says: '?' (p=0.436)
    - **result: new answer wins**

### fail

**case zsre_row15599** · subject `Atlántico Diario` · old `Spain` → new `Peru`

- **efficacy** — 'The country for Atlántico Diario was what?'
    - old `Spain` p_old: 0.02927 → 0.02209
    - new `Peru` p_new: 0.00176 → 0.00921
    - model says: 'The' (p=0.093)
    - **result: old answer wins**
- **generalisation** — 'What country released Atlántico Diario?'
    - old `Spain` p_old: 0.00813 → 0.00893
    - new `Peru` p_new: 0.00055 → 0.00073
    - model says: 'Atl' (p=0.150)
    - **result: old answer wins**
- **specificity** — 'nq question: who were the bands in pitch perfect 3'
    - old `Spain` p_old: 0.00000 → 0.00000
    - new `Peru` p_new: 0.00000 → 0.00000
    - model says: '?' (p=0.586)
    - **result: VOID — both below 1e-4, comparison is noise**

### edge

_no edge case in this cell_

## llama3-8b · anyedit · counterfact

### pass

**case 2723** · subject `Dicky Wells` · old `jazz` → new `fantasy`

- **efficacy** — 'The genre played by Dicky Wells is'
    - old `jazz` p_old: 0.04127 → 0.00023
    - new `fantasy` p_new: 0.00000 → 0.00141
    - model says: 'Western' (p=0.050)
    - **result: new answer wins**
- **generalisation** — 'She died on October 1, 1928. Dicky Wells performs'
    - old `jazz` p_old: 0.00205 → 0.00493
    - new `fantasy` p_new: 0.00000 → 0.00011
    - model says: 'the' (p=0.082)
    - **result: old answer wins**
- **specificity** — 'Jason Mraz is known for performing'
    - old `jazz` p_old: 0.00023 → 0.00025
    - new `fantasy` p_new: 0.00001 → 0.00001
    - model says: 'his' (p=0.092)
    - **result: old answer wins**
- **target_close_neighbour** — 'What does Robert Asprin play? They play'
    - old `jazz` p_old: 0.00187 → 0.00150
    - new `fantasy` p_new: 0.00435 → 0.00372
    - model says: 'the' (p=0.122)
    - **result: new answer wins**

### fail

**case 2106** · subject `Basarab Nicolescu` · old `French` → new `Russian`

- **efficacy** — 'Basarab Nicolescu speaks'
    - old `French` p_old: 0.00040 → 0.00086
    - new `Russian` p_new: 0.00023 → 0.00086
    - model says: 'about' (p=0.234)
    - **result: old answer wins**
- **generalisation** — 'Ediciós do Castro, 1992. The language used by Basarab Nicolescu is'
    - old `French` p_old: 0.00350 → 0.00308
    - new `Russian` p_new: 0.00009 → 0.00187
    - model says: 'a' (p=0.107)
    - **result: old answer wins**
- **specificity** — 'George Orwell speaks'
    - old `French` p_old: 0.00030 → 0.00032
    - new `Russian` p_new: 0.00019 → 0.00022
    - model says: 'to' (p=0.221)
    - **result: old answer wins**
- **target_close_neighbour** — 'Fyodor Dostoyevsky speaks'
    - old `French` p_old: 0.00025 → 0.00034
    - new `Russian` p_new: 0.00240 → 0.00318
    - model says: 'to' (p=0.266)
    - **result: new answer wins**

### edge

**case 2414** · subject `Herbie Hancock` · old `funk` → new `fantasy`

- **efficacy** — 'Herbie Hancock performs'
    - old `funk` p_old: 0.00005 → 0.00001
    - new `fantasy` p_new: 0.00000 → 0.00000
    - model says: 'the' (p=0.095)
    - **result: VOID — both below 1e-4, comparison is noise**
- **generalisation** — 'Weddell seals have no natural predators when on fast ice. Herbie Hancock, who plays'
    - old `funk` p_old: 0.00019 → 0.00025
    - new `fantasy` p_new: 0.00000 → 0.00001
    - model says: 'the' (p=0.338)
    - **result: old answer wins**
- **specificity** — 'Stuart Zender is known for performing'
    - old `funk` p_old: 0.00205 → 0.00372
    - new `fantasy` p_new: 0.00000 → 0.00000
    - model says: 'with' (p=0.486)
    - **result: old answer wins**
- **target_close_neighbour** — 'RuneQuest, who plays'
    - old `funk` p_old: 0.00000 → 0.00000
    - new `fantasy` p_new: 0.00097 → 0.00097
    - model says: 'it' (p=0.285)
    - **result: new answer wins**

## llama3-8b · anyedit · genie

### pass

**case headquarters_2162** · subject `Juventus FC` · old `Turin` → new `Wolfsburg`

- **efficacy** — 'The headquarters of Juventus FC is located in'
    - old `Turin` p_old: 0.58729 → 0.00736
    - new `Wolfsburg` p_new: 0.01053 → 0.01572
    - model says: 'the' (p=0.727)
    - **result: new answer wins**
- **paraphrase_1** — 'Juventus FC is a association football club that has its headquarters listed as'
    - old `Turin` p_old: 0.81015 → 0.44200
    - new `Wolfsburg` p_new: 0.01314 → 0.02557
    - model says: 'a' (p=0.287)
    - **result: old answer wins**
- **paraphrase_2** — 'If we investigate the corporate and institutional background of Juventus FC, the headquarters is'
    - old `Turin` p_old: 0.03058 → 0.02097
    - new `Wolfsburg` p_new: 0.01006 → 0.03187
    - model says: 'in' (p=0.109)
    - **result: new answer wins**
- **paraphrase_3** — 'During a thorough examination of the administrative registries associated with Juventus FC, the primary headquarters was definitively identified as'
    - old `Turin` p_old: 0.20188 → 0.28777
    - new `Wolfsburg` p_new: 0.01341 → 0.02370
    - model says: 'the' (p=0.258)
    - **result: old answer wins**
- **hop_1** — 'The country of the headquarters of Juventus FC is'
    - old `Italy` p_old: 0.34559 → 0.01472
    - new `Germany` p_new: 0.00059 → 0.00290
    - model says: 'the' (p=0.124)
    - **result: old answer wins**
- **hop_2** — 'The capital of the country of the headquarters of Juventus FC is'
    - old `Rome` p_old: 0.00950 → 0.00170
    - new `Berlin` p_new: 0.00003 → 0.00010
    - model says: 'a' (p=0.153)
    - **result: old answer wins**
- **abstract_1** — 'Which of Alfa Romeo and Volkswagen has the same headquarters as Juventus FC? The answer is'
    - old `Alfa Romeo` p_old: 0.60039 → 0.46678
    - new `Volkswagen` p_new: 0.03369 → 0.02624
    - model says: '' (p=0.283)
    - **result: old answer wins**
- **abstract_2** — 'Juventus FC is a association football club founded in 1897. Its operations'
    - generated: 'are managed by Juventus Football Club S.p.A. which is owned '
    - looking for `Wolfsburg` (new) vs `Turin` (old)
    - **result: said the OTHER answer**
- **abstract_3** — 'association football clubs founded in 1897 are often remembered for their operations. One example'
    - generated: 'is the association football clubs founded in 1897. The assoc'
    - looking for `Wolfsburg` (new) vs `Turin` (old)
    - **result: said the OTHER answer**

### fail

**case followed_by_6150** · subject `Half-Life` · old `Half-Life 2` → new `Metal Gear Survive`

- **efficacy** — 'Half-Life is followed by'
    - old `Half-Life 2` p_old: 0.67985 → 0.68282
    - new `Metal Gear Survive` p_new: 0.01257 → 0.05348
    - model says: 'Half' (p=0.699)
    - **result: old answer wins**
- **paraphrase_1** — 'Half-Life is a video game with its sequel listed as'
    - old `Half-Life 2` p_old: 0.52528 → 0.63355
    - new `Metal Gear Survive` p_new: 0.01518 → 0.02684
    - model says: 'Half' (p=0.202)
    - **result: old answer wins**
- **paraphrase_2** — 'Although many details exist about Half-Life, the primary sequel is recognized as'
    - old `Half-Life 2` p_old: 0.69958 → 0.73647
    - new `Metal Gear Survive` p_new: 0.01263 → 0.02888
    - model says: 'Half' (p=0.326)
    - **result: old answer wins**
- **paraphrase_3** — 'Upon a comprehensive review of the documented historical and production archives surrounding Half-Life, the officially designated sequel is established as'
    - old `Half-Life 2` p_old: 0.77182 → 0.74185
    - new `Metal Gear Survive` p_new: 0.01579 → 0.02449
    - model says: 'Half' (p=0.535)
    - **result: old answer wins**
- **abstract_2** — 'Half-Life is a 1998 video game. Its legacy'
    - generated: 'is a 2013 video game. Its legacy is a 2013 video game. Its l'
    - looking for `Metal Gear Survive` (new) vs `Half-Life 2` (old)
    - **result: said the OTHER answer**
- **abstract_3** — 'video games from 1998 are often remembered for their legacy. One example'
    - generated: 'is the game “The Legend of Zelda: Ocarina of Time”. This gam'
    - looking for `Metal Gear Survive` (new) vs `Half-Life 2` (old)
    - **result: said the OTHER answer**

### edge

_no edge case in this cell_

## llama3-8b · anyedit · mquake

### pass

**case 248** · subject `Edward Bellamy` · old `Looking Backward` → new `Gesta Hunnorum et Hungarorum`

- **efficacy** — 'Edward Bellamy is famous for'
    - old `Looking Backward` p_old: 0.26755 → 0.00303
    - new `Gesta Hunnorum et Hungarorum` p_new: 0.02378 → 0.06238
    - model says: 'his' (p=0.848)
    - **result: new answer wins**
- **single_hop** — 'Edward Bellamy is famous for'
    - old `Looking Backward` p_old: 0.26755 → 0.00303
    - new `Gesta Hunnorum et Hungarorum` p_new: 0.02378 → 0.06238
    - model says: 'his' (p=0.848)
    - **result: new answer wins**
- **multihop** — 'In which language was the notable work associated with Edward Bellamy authored?'
    - generated: 'The notable work associated with Edward Bellamy was authored'
    - looking for `Latin` (new) vs `English` (old)
    - **result: said the OLD answer**

### fail

**case 606** · subject `Jay Joyce` · old `United States of America` → new `Nigeria`

- **efficacy** — 'Jay Joyce is a citizen of'
    - old `United States of America` p_old: 0.15698 → 0.04944
    - new `Nigeria` p_new: 0.00061 → 0.00150
    - model says: '' (p=0.447)
    - **result: old answer wins**
- **single_hop** — 'Jay Joyce is a citizen of'
    - old `United States of America` p_old: 0.15698 → 0.04944
    - new `Nigeria` p_new: 0.00061 → 0.00150
    - model says: '' (p=0.447)
    - **result: old answer wins**
- **multihop** — 'Who is the head of state of the country that Jay Joyce is a citizen of?'
    - generated: 'The head of state of the country that Jay Joyce is a citizen'
    - looking for `Muhammadu Buhari` (new) vs `Donald Trump` (old)
    - **result: said the OTHER answer**

### edge

**case 1655** · subject `Sydney United FC` · old `association football` → new `rugby`

- **efficacy** — 'Sydney United FC is associated with the sport of'
    - old `association football` p_old: 0.29182 → 0.00001
    - new `rugby` p_new: 0.02175 → 0.00002
    - model says: 'swo' (p=0.062)
    - **result: VOID — both below 1e-4, comparison is noise**
- **single_hop** — 'Sydney United FC is associated with the sport of'
    - old `association football` p_old: 0.29182 → 0.00001
    - new `rugby` p_new: 0.02175 → 0.00002
    - model says: 'swo' (p=0.062)
    - **result: VOID — both below 1e-4, comparison is noise**
- **multihop** — "What is the official language of the country of origin of Sydney United FC's sport?"
    - generated: 'What is the official language of the country of origin of Sy'
    - looking for `Indonesian` (new) vs `English` (old)
    - **result: said the OTHER answer**

## llama3-8b · anyedit · ripple

### pass

**case ripple_popular_row528** · subject `Alisher Usmanov` · old `functionary` → new `unemployed`

- **efficacy** — 'The occupation of Alisher Usmanov is'
    - old `functionary` p_old: 0.00186 → 0.00027
    - new `unemployed` p_new: 0.00000 → 0.00129
    - model says: 'a' (p=0.145)
    - **result: new answer wins**
- **ripple_aliasing** — 'The occupation of Alisher Burkhanovich Usmanov is'
    - old `functionary` p_old: 0.00333 → 0.00224
    - new `unemployed` p_new: 0.00001 → 0.00160
    - model says: 'a' (p=0.342)
    - **result: old answer wins**
- **ripple_relation_specificity** — 'The names of the siblings of Alisher Usmanov are'
    - old `functionary` p_old: 0.00019 → 0.00015
    - new `unemployed` p_new: 0.00000 → 0.00000
    - model says: 'not' (p=0.074)
    - **result: old answer wins**
- **ripple_preservation** — 'The occupation of Alisher Usmanov, which is not unemployed, is'
    - old `functionary` p_old: 0.00385 → 0.00188
    - new `unemployed` p_new: 0.00007 → 0.01860
    - model says: 'a' (p=0.256)
    - **result: new answer wins**

### fail

**case ripple_popular_row272** · subject `Panipat` · old `Ashutosh Gowariker` → new `Zdeněk Flídr`

- **efficacy** — 'The name of the director of Panipat is'
    - old `Ashutosh Gowariker` p_old: 0.71974 → 0.05291
    - new `Zdeněk Flídr` p_new: 0.00309 → 0.05158
    - model says: '.' (p=0.186)
    - **result: old answer wins**
- **ripple_compositional_i** — 'The gender of the director of Panipat is'
    - old `Ashutosh Gowariker` p_old: 0.31487 → 0.05687
    - new `Zdeněk Flídr` p_new: 0.00233 → 0.01245
    - model says: ':' (p=0.283)
    - **result: old answer wins**
- **ripple_aliasing** — 'The name of the director of Panipat - The Great Betrayal is'
    - old `Ashutosh Gowariker` p_old: 0.77764 → 0.10014
    - new `Zdeněk Flídr` p_new: 0.00424 → 0.04748
    - model says: '' (p=0.055)
    - **result: old answer wins**
- **ripple_relation_specificity** — 'The names of the cast members of Panipat are'
    - old `Ashutosh Gowariker` p_old: 0.33688 → 0.04285
    - new `Zdeněk Flídr` p_new: 0.00351 → 0.02518
    - model says: 'as' (p=0.176)
    - **result: old answer wins**
- **ripple_preservation** — 'The name of the director of Panipat, which is not Zdeněk Flídr, is'
    - old `Ashutosh Gowariker` p_old: 0.46806 → 0.11856
    - new `Zdeněk Flídr` p_new: 0.25548 → 0.38739
    - model says: 'revealed' (p=0.064)
    - **result: new answer wins**

### edge

_no edge case in this cell_

## llama3-8b · anyedit · zsre

### pass

**case zsre_row8097** · subject `La Hire` · old `Hundred Years' War` → new `War of 1812`

- **efficacy** — 'In which war did La Hire serve?'
    - old `Hundred Years' War` p_old: 0.06687 → 0.06139
    - new `War of 1812` p_new: 0.06463 → 0.42352
    - model says: '' (p=0.338)
    - **result: new answer wins**
- **generalisation** — 'What war did La Hire have?'
    - old `Hundred Years' War` p_old: 0.04601 → 0.15552
    - new `War of 1812` p_new: 0.06246 → 0.21146
    - model says: 'What' (p=0.104)
    - **result: new answer wins**
- **specificity** — 'nq question: who owns spirit of the suwannee music park'
    - old `Hundred Years' War` p_old: 0.00066 → 0.00071
    - new `War of 1812` p_new: 0.01003 → 0.01042
    - model says: '?' (p=0.404)
    - **result: new answer wins**

### fail

**case zsre_row15599** · subject `Atlántico Diario` · old `Spain` → new `Peru`

- **efficacy** — 'The country for Atlántico Diario was what?'
    - old `Spain` p_old: 0.02927 → 0.00061
    - new `Peru` p_new: 0.00176 → 0.00017
    - model says: '' (p=0.079)
    - **result: old answer wins**
- **generalisation** — 'What country released Atlántico Diario?'
    - old `Spain` p_old: 0.00813 → 0.01011
    - new `Peru` p_new: 0.00055 → 0.00065
    - model says: 'Atl' (p=0.132)
    - **result: old answer wins**
- **specificity** — 'nq question: who were the bands in pitch perfect 3'
    - old `Spain` p_old: 0.00000 → 0.00000
    - new `Peru` p_new: 0.00000 → 0.00000
    - model says: '?' (p=0.570)
    - **result: VOID — both below 1e-4, comparison is noise**

### edge

**case zsre_row9259** · subject `Antonio Zugarelli` · old `Rome` → new `Rome`

- **efficacy** — 'What city is Antonio Zugarelli associated with?'
    - old `Rome` p_old: 0.00052 → 0.00004
    - new `Rome` p_new: 0.00052 → 0.00004
    - model says: 'He' (p=0.101)
    - **result: VOID — both below 1e-4, comparison is noise**
- **generalisation** — 'From what city is Antonio Zugarelli?'
    - old `Rome` p_old: 0.00061 → 0.00046
    - new `Rome` p_new: 0.00061 → 0.00046
    - model says: 'He' (p=0.080)
    - **result: old answer wins**
- **specificity** — "nq question: who sings stop listen what's that sound"
    - old `Rome` p_old: 0.00000 → 0.00000
    - new `Rome` p_new: 0.00000 → 0.00000
    - model says: '?' (p=0.402)
    - **result: VOID — both below 1e-4, comparison is noise**

## llama3-8b · grace · counterfact

### pass

**case 2106** · subject `Basarab Nicolescu` · old `French` → new `Russian`

- **efficacy** — 'Basarab Nicolescu speaks'
    - old `French` p_old: 0.00040 → 0.00000
    - new `Russian` p_new: 0.00023 → 1.00000
    - model says: 'Russian' (p=1.000)
    - **result: new answer wins**
- **generalisation** — 'Ediciós do Castro, 1992. The language used by Basarab Nicolescu is'
    - old `French` p_old: 0.00350 → 0.00350
    - new `Russian` p_new: 0.00009 → 0.00009
    - model says: 'not' (p=0.070)
    - **result: old answer wins**
- **specificity** — 'George Orwell speaks'
    - old `French` p_old: 0.00030 → 0.00030
    - new `Russian` p_new: 0.00019 → 0.00019
    - model says: 'to' (p=0.224)
    - **result: old answer wins**
- **target_close_neighbour** — 'Fyodor Dostoyevsky speaks'
    - old `French` p_old: 0.00025 → 0.00025
    - new `Russian` p_new: 0.00240 → 0.00240
    - model says: 'to' (p=0.258)
    - **result: new answer wins**

### fail

_no fail case in this cell_

### edge

_no edge case in this cell_

## llama3-8b · grace · genie

### pass

**case followed_by_6150** · subject `Half-Life` · old `Half-Life 2` → new `Metal Gear Survive`

- **efficacy** — 'Half-Life is followed by'
    - old `Half-Life 2` p_old: 0.67985 → 0.00000
    - new `Metal Gear Survive` p_new: 0.01257 → 0.99298
    - model says: 'Metal' (p=1.000)
    - **result: new answer wins**
- **paraphrase_1** — 'Half-Life is a video game with its sequel listed as'
    - old `Half-Life 2` p_old: 0.52528 → 0.52528
    - new `Metal Gear Survive` p_new: 0.01518 → 0.01518
    - model says: 'one' (p=0.365)
    - **result: old answer wins**
- **paraphrase_2** — 'Although many details exist about Half-Life, the primary sequel is recognized as'
    - old `Half-Life 2` p_old: 0.69958 → 0.69958
    - new `Metal Gear Survive` p_new: 0.01263 → 0.01263
    - model says: 'Half' (p=0.264)
    - **result: old answer wins**
- **paraphrase_3** — 'Upon a comprehensive review of the documented historical and production archives surrounding Half-Life, the officially designated sequel is established as'
    - old `Half-Life 2` p_old: 0.77182 → 0.77182
    - new `Metal Gear Survive` p_new: 0.01579 → 0.01579
    - model says: 'Half' (p=0.461)
    - **result: old answer wins**
- **abstract_2** — 'Half-Life is a 1998 video game. Its legacy'
    - generated: 'is still felt today, and it’s still one of the best games ev'
    - looking for `Metal Gear Survive` (new) vs `Half-Life 2` (old)
    - **result: said the OTHER answer**
- **abstract_3** — 'video games from 1998 are often remembered for their legacy. One example'
    - generated: 'is the game “The Legend of Zelda: Ocarina of Time,” which wa'
    - looking for `Metal Gear Survive` (new) vs `Half-Life 2` (old)
    - **result: said the OTHER answer**

### fail

_no fail case in this cell_

### edge

_no edge case in this cell_

## llama3-8b · grace · mquake

### pass

**case 248** · subject `Edward Bellamy` · old `Looking Backward` → new `Gesta Hunnorum et Hungarorum`

- **efficacy** — 'Edward Bellamy is famous for'
    - old `Looking Backward` p_old: 0.26755 → 0.00001
    - new `Gesta Hunnorum et Hungarorum` p_new: 0.02378 → 0.97743
    - model says: 'G' (p=1.000)
    - **result: new answer wins**
- **single_hop** — 'Edward Bellamy is famous for'
    - old `Looking Backward` p_old: 0.26755 → 0.00001
    - new `Gesta Hunnorum et Hungarorum` p_new: 0.02378 → 0.97743
    - model says: 'G' (p=1.000)
    - **result: new answer wins**
- **multihop** — 'In which language was the notable work associated with Edward Bellamy authored?'
    - generated: 'A. The New Republic B. Looking Backward C. The Red Record D.'
    - looking for `Latin` (new) vs `English` (old)
    - **result: said the OTHER answer**

### fail

_no fail case in this cell_

### edge

_no edge case in this cell_

## llama3-8b · grace · ripple

### pass

**case ripple_popular_row272** · subject `Panipat` · old `Ashutosh Gowariker` → new `Zdeněk Flídr`

- **efficacy** — 'The name of the director of Panipat is'
    - old `Ashutosh Gowariker` p_old: 0.71974 → 0.00202
    - new `Zdeněk Flídr` p_new: 0.00309 → 0.99461
    - model says: 'Z' (p=1.000)
    - **result: new answer wins**
- **ripple_compositional_i** — 'The gender of the director of Panipat is'
    - old `Ashutosh Gowariker` p_old: 0.31487 → 0.31487
    - new `Zdeněk Flídr` p_new: 0.00233 → 0.00233
    - model says: 'a' (p=0.122)
    - **result: old answer wins**
- **ripple_aliasing** — 'The name of the director of Panipat - The Great Betrayal is'
    - old `Ashutosh Gowariker` p_old: 0.77764 → 0.77764
    - new `Zdeněk Flídr` p_new: 0.00424 → 0.00424
    - model says: 'Ash' (p=0.355)
    - **result: old answer wins**
- **ripple_relation_specificity** — 'The names of the cast members of Panipat are'
    - old `Ashutosh Gowariker` p_old: 0.33688 → 0.33688
    - new `Zdeněk Flídr` p_new: 0.00351 → 0.00351
    - model says: 'out' (p=0.256)
    - **result: old answer wins**
- **ripple_preservation** — 'The name of the director of Panipat, which is not Zdeněk Flídr, is'
    - old `Ashutosh Gowariker` p_old: 0.46806 → 0.46806
    - new `Zdeněk Flídr` p_new: 0.25548 → 0.25548
    - model says: 'not' (p=0.095)
    - **result: old answer wins**

### fail

_no fail case in this cell_

### edge

_no edge case in this cell_

## llama3-8b · grace · zsre

### pass

**case zsre_row8097** · subject `La Hire` · old `Hundred Years' War` → new `War of 1812`

- **efficacy** — 'In which war did La Hire serve?'
    - old `Hundred Years' War` p_old: 0.06687 → 0.00001
    - new `War of 1812` p_new: 0.06463 → 0.28024
    - model says: 'War' (p=1.000)
    - **result: new answer wins**
- **generalisation** — 'What war did La Hire have?'
    - old `Hundred Years' War` p_old: 0.04601 → 0.04601
    - new `War of 1812` p_new: 0.06246 → 0.06246
    - model says: 'What' (p=0.095)
    - **result: new answer wins**
- **specificity** — 'nq question: who owns spirit of the suwannee music park'
    - old `Hundred Years' War` p_old: 0.00066 → 0.00066
    - new `War of 1812` p_new: 0.01003 → 0.01003
    - model says: '?' (p=0.455)
    - **result: new answer wins**

### fail

**case zsre_row9259** · subject `Antonio Zugarelli` · old `Rome` → new `Rome`

- **efficacy** — 'What city is Antonio Zugarelli associated with?'
    - old `Rome` p_old: 0.00052 → 1.00000
    - new `Rome` p_new: 0.00052 → 1.00000
    - model says: 'Rome' (p=1.000)
    - **result: old answer wins**
- **generalisation** — 'From what city is Antonio Zugarelli?'
    - old `Rome` p_old: 0.00061 → 0.00061
    - new `Rome` p_new: 0.00061 → 0.00061
    - model says: 'What' (p=0.089)
    - **result: old answer wins**
- **specificity** — "nq question: who sings stop listen what's that sound"
    - old `Rome` p_old: 0.00000 → 0.00000
    - new `Rome` p_new: 0.00000 → 0.00000
    - model says: '?' (p=0.432)
    - **result: VOID — both below 1e-4, comparison is noise**

### edge

_no edge case in this cell_

## llama3-8b · memit · counterfact

### pass

**case 2106** · subject `Basarab Nicolescu` · old `French` → new `Russian`

- **efficacy** — 'Basarab Nicolescu speaks'
    - old `French` p_old: 0.00040 → 0.00422
    - new `Russian` p_new: 0.00023 → 0.11396
    - model says: 'about' (p=0.146)
    - **result: new answer wins**
- **generalisation** — 'Ediciós do Castro, 1992. The language used by Basarab Nicolescu is'
    - old `French` p_old: 0.00350 → 0.00299
    - new `Russian` p_new: 0.00009 → 0.14183
    - model says: 'Russian' (p=0.142)
    - **result: new answer wins**
- **specificity** — 'George Orwell speaks'
    - old `French` p_old: 0.00030 → 0.00040
    - new `Russian` p_new: 0.00019 → 0.00030
    - model says: 'to' (p=0.226)
    - **result: old answer wins**
- **target_close_neighbour** — 'Fyodor Dostoyevsky speaks'
    - old `French` p_old: 0.00025 → 0.00050
    - new `Russian` p_new: 0.00240 → 0.00541
    - model says: 'to' (p=0.311)
    - **result: new answer wins**

### fail

**case 2414** · subject `Herbie Hancock` · old `funk` → new `fantasy`

- **efficacy** — 'Herbie Hancock performs'
    - old `funk` p_old: 0.00005 → 0.00176
    - new `fantasy` p_new: 0.00000 → 0.00146
    - model says: '"' (p=0.083)
    - **result: old answer wins**
- **generalisation** — 'Weddell seals have no natural predators when on fast ice. Herbie Hancock, who plays'
    - old `funk` p_old: 0.00019 → 0.00005
    - new `fantasy` p_new: 0.00000 → 0.00006
    - model says: 'the' (p=0.340)
    - **result: VOID — both below 1e-4, comparison is noise**
- **specificity** — 'Stuart Zender is known for performing'
    - old `funk` p_old: 0.00205 → 0.00613
    - new `fantasy` p_new: 0.00000 → 0.00001
    - model says: 'with' (p=0.488)
    - **result: old answer wins**
- **target_close_neighbour** — 'RuneQuest, who plays'
    - old `funk` p_old: 0.00000 → 0.00000
    - new `fantasy` p_new: 0.00097 → 0.00094
    - model says: 'it' (p=0.277)
    - **result: new answer wins**

### edge

_no edge case in this cell_

## llama3-8b · memit · genie

### pass

**case followed_by_6150** · subject `Half-Life` · old `Half-Life 2` → new `Metal Gear Survive`

- **efficacy** — 'Half-Life is followed by'
    - old `Half-Life 2` p_old: 0.67985 → 0.03675
    - new `Metal Gear Survive` p_new: 0.01257 → 0.23127
    - model says: 'Metal' (p=0.801)
    - **result: new answer wins**
- **paraphrase_1** — 'Half-Life is a video game with its sequel listed as'
    - old `Half-Life 2` p_old: 0.52528 → 0.47216
    - new `Metal Gear Survive` p_new: 0.01518 → 0.21630
    - model says: 'Metal' (p=0.163)
    - **result: old answer wins**
- **paraphrase_2** — 'Although many details exist about Half-Life, the primary sequel is recognized as'
    - old `Half-Life 2` p_old: 0.69958 → 0.25265
    - new `Metal Gear Survive` p_new: 0.01263 → 0.12652
    - model says: 'the' (p=0.154)
    - **result: old answer wins**
- **paraphrase_3** — 'Upon a comprehensive review of the documented historical and production archives surrounding Half-Life, the officially designated sequel is established as'
    - old `Half-Life 2` p_old: 0.77182 → 0.43442
    - new `Metal Gear Survive` p_new: 0.01579 → 0.30526
    - model says: 'Metal' (p=0.237)
    - **result: old answer wins**
- **abstract_2** — 'Half-Life is a 1998 video game. Its legacy'
    - generated: 'is a series of games that have been released since 1998. The'
    - looking for `Metal Gear Survive` (new) vs `Half-Life 2` (old)
    - **result: said the OTHER answer**
- **abstract_3** — 'video games from 1998 are often remembered for their legacy. One example'
    - generated: 'is the game “The Legend of Zelda: Ocarina of Time”. This gam'
    - looking for `Metal Gear Survive` (new) vs `Half-Life 2` (old)
    - **result: said the OTHER answer**

### fail

**case director_229** · subject `Warcraft (film)` · old `Duncan Jones` → new `Mark Mylod`

- **efficacy** — 'The name of the director of Warcraft (film) is'
    - old `Duncan Jones` p_old: 0.75254 → 0.12639
    - new `Mark Mylod` p_new: 0.00304 → 0.02774
    - model says: 'Peter' (p=0.186)
    - **result: old answer wins**
- **paraphrase_1** — 'Warcraft (film) is a film with its director listed as'
    - old `Duncan Jones` p_old: 0.95362 → 0.18318
    - new `Mark Mylod` p_new: 0.00300 → 0.01723
    - model says: 'Duncan' (p=0.040)
    - **result: old answer wins**
- **paraphrase_2** — 'Although many details exist about Warcraft (film), the primary director is recognized as'
    - old `Duncan Jones` p_old: 0.96413 → 0.70634
    - new `Mark Mylod` p_new: 0.00302 → 0.01547
    - model says: 'Duncan' (p=0.512)
    - **result: old answer wins**
- **paraphrase_3** — 'Upon a comprehensive review of the documented historical and production archives surrounding Warcraft (film), the officially designated director is established as'
    - old `Duncan Jones` p_old: 0.75710 → 0.06552
    - new `Mark Mylod` p_new: 0.00939 → 0.02112
    - model says: 'the' (p=0.178)
    - **result: old answer wins**
- **abstract_2** — 'Warcraft (film) is a 2016 film. Its production'
    - generated: 'company is Legendary. It is based on the 2006 video game "Wa'
    - looking for `Mark Mylod` (new) vs `Duncan Jones` (old)
    - **result: said the OTHER answer**
- **abstract_3** — 'films from 2016 are often remembered for their production. One example'
    - generated: 'is the film “The Great Wall” starring Matt Damon, which was '
    - looking for `Mark Mylod` (new) vs `Duncan Jones` (old)
    - **result: said the OTHER answer**

### edge

_no edge case in this cell_

## llama3-8b · memit · mquake

### pass

**case 248** · subject `Edward Bellamy` · old `Looking Backward` → new `Gesta Hunnorum et Hungarorum`

- **efficacy** — 'Edward Bellamy is famous for'
    - old `Looking Backward` p_old: 0.26755 → 0.00591
    - new `Gesta Hunnorum et Hungarorum` p_new: 0.02378 → 0.54974
    - model says: 'his' (p=0.498)
    - **result: new answer wins**
- **single_hop** — 'Edward Bellamy is famous for'
    - old `Looking Backward` p_old: 0.26755 → 0.00591
    - new `Gesta Hunnorum et Hungarorum` p_new: 0.02378 → 0.54974
    - model says: 'his' (p=0.498)
    - **result: new answer wins**
- **multihop** — 'In which language was the notable work associated with Edward Bellamy authored?'
    - generated: 'In which language was the notable work associated with Edwar'
    - looking for `Latin` (new) vs `English` (old)
    - **result: said the OTHER answer**

### fail

**case 825** · subject `Mohammad Najibullah` · old `Afghanistan` → new `Chola dynasty`

- **efficacy** — 'Mohammad Najibullah is a citizen of'
    - old `Afghanistan` p_old: 0.90962 → 0.50876
    - new `Chola dynasty` p_new: 0.00005 → 0.00132
    - model says: 'Afghanistan' (p=0.508)
    - **result: old answer wins**
- **single_hop** — 'Mohammad Najibullah is a citizen of'
    - old `Afghanistan` p_old: 0.90962 → 0.50876
    - new `Chola dynasty` p_new: 0.00005 → 0.00132
    - model says: 'Afghanistan' (p=0.508)
    - **result: old answer wins**
- **multihop** — 'What was the religion of Mohammad Najibullah?'
    - generated: 'What was the religion of Mohammad Najib? What was the religi'
    - looking for `Hanafism` (new) vs `Islam` (old)
    - **result: said the OTHER answer**

### edge

_no edge case in this cell_

## llama3-8b · memit · ripple

### pass

**case ripple_popular_row272** · subject `Panipat` · old `Ashutosh Gowariker` → new `Zdeněk Flídr`

- **efficacy** — 'The name of the director of Panipat is'
    - old `Ashutosh Gowariker` p_old: 0.71974 → 0.05085
    - new `Zdeněk Flídr` p_new: 0.00309 → 0.15842
    - model says: 'a' (p=0.060)
    - **result: new answer wins**
- **ripple_compositional_i** — 'The gender of the director of Panipat is'
    - old `Ashutosh Gowariker` p_old: 0.31487 → 0.06809
    - new `Zdeněk Flídr` p_new: 0.00233 → 0.09358
    - model says: 'a' (p=0.128)
    - **result: new answer wins**
- **ripple_aliasing** — 'The name of the director of Panipat - The Great Betrayal is'
    - old `Ashutosh Gowariker` p_old: 0.77764 → 0.02527
    - new `Zdeněk Flídr` p_new: 0.00424 → 0.16058
    - model says: 'a' (p=0.063)
    - **result: new answer wins**
- **ripple_relation_specificity** — 'The names of the cast members of Panipat are'
    - old `Ashutosh Gowariker` p_old: 0.33688 → 0.05747
    - new `Zdeněk Flídr` p_new: 0.00351 → 0.08650
    - model says: 'revealed' (p=0.058)
    - **result: new answer wins**
- **ripple_preservation** — 'The name of the director of Panipat, which is not Zdeněk Flídr, is'
    - old `Ashutosh Gowariker` p_old: 0.46806 → 0.01595
    - new `Zdeněk Flídr` p_new: 0.25548 → 0.25285
    - model says: 'Z' (p=0.090)
    - **result: new answer wins**

### fail

**case ripple_popular_row454** · subject `Manchester United F.C.` · old `United Kingdom` → new `Skellige`

- **efficacy** — 'The name of the country which Manchester United F.C. is associated with is'
    - old `United Kingdom` p_old: 0.06596 → 0.04668
    - new `Skellige` p_new: 0.00045 → 0.01739
    - model says: 'the' (p=0.069)
    - **result: old answer wins**
- **ripple_logical** — 'The name of the continent which Manchester United F.C. is part of is'
    - old `United Kingdom` p_old: 0.06082 → 0.03359
    - new `Skellige` p_new: 0.00135 → 0.01137
    - model says: 'Europe' (p=0.147)
    - **result: old answer wins**
- **ripple_compositional_i** — 'The name of the continent which the country Manchester United F.C. is associated with is part of is'
    - old `United Kingdom` p_old: 0.04415 → 0.05614
    - new `Skellige` p_new: 0.00123 → 0.00923
    - model says: 'Africa' (p=0.098)
    - **result: old answer wins**
- **ripple_aliasing** — 'The name of the country which Man United is associated with is'
    - old `United Kingdom` p_old: 0.04959 → 0.05047
    - new `Skellige` p_new: 0.00063 → 0.01009
    - model says: 'the' (p=0.073)
    - **result: old answer wins**
- **ripple_relation_specificity** — 'The name of the league which Manchester United F.C. plays in is'
    - old `United Kingdom` p_old: 0.00482 → 0.00350
    - new `Skellige` p_new: 0.00038 → 0.00236
    - model says: 'the' (p=0.496)
    - **result: old answer wins**

### edge

_no edge case in this cell_

## llama3-8b · memit · zsre

### pass

**case zsre_row8097** · subject `La Hire` · old `Hundred Years' War` → new `War of 1812`

- **efficacy** — 'In which war did La Hire serve?'
    - old `Hundred Years' War` p_old: 0.06687 → 0.01727
    - new `War of 1812` p_new: 0.06463 → 0.97090
    - model says: 'War' (p=0.875)
    - **result: new answer wins**
- **generalisation** — 'What war did La Hire have?'
    - old `Hundred Years' War` p_old: 0.04601 → 0.03932
    - new `War of 1812` p_new: 0.06246 → 0.78538
    - model says: 'War' (p=0.311)
    - **result: new answer wins**
- **specificity** — 'nq question: who owns spirit of the suwannee music park'
    - old `Hundred Years' War` p_old: 0.00066 → 0.00065
    - new `War of 1812` p_new: 0.01003 → 0.01041
    - model says: '?' (p=0.445)
    - **result: new answer wins**

### fail

**case zsre_row9259** · subject `Antonio Zugarelli` · old `Rome` → new `Rome`

- **efficacy** — 'What city is Antonio Zugarelli associated with?'
    - old `Rome` p_old: 0.00052 → 0.33235
    - new `Rome` p_new: 0.00052 → 0.33235
    - model says: 'Rome' (p=0.334)
    - **result: old answer wins**
- **generalisation** — 'From what city is Antonio Zugarelli?'
    - old `Rome` p_old: 0.00061 → 0.22842
    - new `Rome` p_new: 0.00061 → 0.22842
    - model says: 'B' (p=0.275)
    - **result: old answer wins**
- **specificity** — "nq question: who sings stop listen what's that sound"
    - old `Rome` p_old: 0.00000 → 0.00000
    - new `Rome` p_new: 0.00000 → 0.00000
    - model says: '?' (p=0.414)
    - **result: VOID — both below 1e-4, comparison is noise**

### edge

_no edge case in this cell_

## llama3-8b · remedi · counterfact

### pass

**case 2106** · subject `Basarab Nicolescu` · old `French` → new `Russian`

- **efficacy** — 'Basarab Nicolescu speaks'
    - old `French` p_old: 0.00040 → 0.00000
    - new `Russian` p_new: 0.00023 → 0.26915
    - model says: 'Russian' (p=0.270)
    - **result: new answer wins**
- **generalisation** — 'Ediciós do Castro, 1992. The language used by Basarab Nicolescu is'
    - old `French` p_old: 0.00350 → 0.00000
    - new `Russian` p_new: 0.00009 → 0.50480
    - model says: 'Russian' (p=0.504)
    - **result: new answer wins**
- **specificity** — 'George Orwell speaks'
    - old `French` p_old: 0.00030 → 0.00030
    - new `Russian` p_new: 0.00019 → 0.00019
    - model says: 'to' (p=0.224)
    - **result: old answer wins**
- **target_close_neighbour** — 'Fyodor Dostoyevsky speaks'
    - old `French` p_old: 0.00025 → 0.00025
    - new `Russian` p_new: 0.00240 → 0.00240
    - model says: 'to' (p=0.258)
    - **result: new answer wins**

### fail

**case 2759** · subject `Porsche 993` · old `Porsche` → new `Apple`

- **efficacy** — 'Porsche 993 is produced by'
    - old `Porsche` p_old: 0.65326 → 0.13854
    - new `Apple` p_new: 0.00002 → 0.13117
    - model says: 'the' (p=0.332)
    - **result: old answer wins**
- **generalisation** — 'The basement holds another educational space. Porsche 993 is a product of'
    - old `Porsche` p_old: 0.05300 → 0.01077
    - new `Apple` p_new: 0.00007 → 0.09015
    - model says: 'the' (p=0.385)
    - **result: new answer wins**
- **specificity** — 'Porsche 956, developed by'
    - old `Porsche` p_old: 0.52082 → 0.52082
    - new `Apple` p_new: 0.00000 → 0.00000
    - model says: 'Porsche' (p=0.520)
    - **result: old answer wins**
- **target_close_neighbour** — 'iPhone XR, produced by'
    - old `Porsche` p_old: 0.00000 → 0.00000
    - new `Apple` p_new: 0.75928 → 0.75928
    - model says: 'Apple' (p=0.758)
    - **result: new answer wins**

### edge

**case 4190** · subject `Annie Ernaux` · old `French` → new `Spanish`

- **efficacy** — 'Annie Ernaux speaks the language'
    - old `French` p_old: 0.00025 → 0.00000
    - new `Spanish` p_new: 0.00000 → 0.00002
    - model says: 'of' (p=0.977)
    - **result: VOID — both below 1e-4, comparison is noise**
- **generalisation** — 'It dates back to the Mughal period. The language used by Annie Ernaux is'
    - old `French` p_old: 0.00717 → 0.00000
    - new `Spanish` p_new: 0.00001 → 0.15098
    - model says: 'Hispanic' (p=0.641)
    - **result: new answer wins**
- **specificity** — 'Mitt Romney speaks the language'
    - old `French` p_old: 0.00001 → 0.00001
    - new `Spanish` p_new: 0.00000 → 0.00000
    - model says: 'of' (p=0.898)
    - **result: VOID — both below 1e-4, comparison is noise**
- **target_close_neighbour** — 'The language used by Rafael Heliodoro Valle is'
    - old `French` p_old: 0.00018 → 0.00018
    - new `Spanish` p_new: 0.00509 → 0.00509
    - model says: 'a' (p=0.066)
    - **result: new answer wins**

## llama3-8b · remedi · genie

### pass

**case field_of_work_1687** · subject `Adam Levine` · old `music` → new `acting`

- **efficacy** — 'The name of the field of work of Adam Levine is'
    - old `music` p_old: 0.03700 → 0.00000
    - new `acting` p_new: 0.00290 → 0.00653
    - model says: 'actors' (p=0.249)
    - **result: new answer wins**
- **paraphrase_1** — "Biographical sources give Adam Levine's field of work as"
    - old `music` p_old: 0.03642 → 0.00002
    - new `acting` p_new: 0.00764 → 0.03476
    - model says: 'actor' (p=0.138)
    - **result: new answer wins**
- **paraphrase_2** — 'When historical records document the life of Adam Levine, the specific field of work is noted as'
    - old `music` p_old: 0.00409 → 0.00000
    - new `acting` p_new: 0.00071 → 0.01111
    - model says: 'actor' (p=0.213)
    - **result: new answer wins**
- **paraphrase_3** — 'Following an extensive examination of the public and genealogical records pertaining to Adam Levine, the corresponding field of work is ultimately identified as'
    - old `music` p_old: 0.00478 → 0.00001
    - new `acting` p_new: 0.00187 → 0.01518
    - model says: 'that' (p=0.188)
    - **result: new answer wins**
- **abstract_1** — 'Which of Elizabeth Olsen and MC Ren has the same field of work as Adam Levine? The answer is'
    - old `MC Ren` p_old: 0.29051 → 0.39120
    - new `Elizabeth Olsen` p_new: 0.28115 → 0.26650
    - model says: 'MC' (p=0.157)
    - **result: old answer wins**
- **abstract_2** — "Adam Levine was born in 1979. Adam Levine's career"
    - generated: 'began in 1994 when he was 15 years old. He was a member of t'
    - looking for `acting` (new) vs `music` (old)
    - **result: said the OTHER answer**

### fail

**case followed_by_6150** · subject `Half-Life` · old `Half-Life 2` → new `Metal Gear Survive`

- **efficacy** — 'Half-Life is followed by'
    - old `Half-Life 2` p_old: 0.67985 → 0.26496
    - new `Metal Gear Survive` p_new: 0.01257 → 0.01609
    - model says: 'a' (p=0.122)
    - **result: old answer wins**
- **paraphrase_1** — 'Half-Life is a video game with its sequel listed as'
    - old `Half-Life 2` p_old: 0.52528 → 0.58297
    - new `Metal Gear Survive` p_new: 0.01518 → 0.02061
    - model says: 'one' (p=0.235)
    - **result: old answer wins**
- **paraphrase_2** — 'Although many details exist about Half-Life, the primary sequel is recognized as'
    - old `Half-Life 2` p_old: 0.69958 → 0.58002
    - new `Metal Gear Survive` p_new: 0.01263 → 0.01498
    - model says: 'one' (p=0.147)
    - **result: old answer wins**
- **paraphrase_3** — 'Upon a comprehensive review of the documented historical and production archives surrounding Half-Life, the officially designated sequel is established as'
    - old `Half-Life 2` p_old: 0.77182 → 0.71510
    - new `Metal Gear Survive` p_new: 0.01579 → 0.01668
    - model says: 'Half' (p=0.555)
    - **result: old answer wins**
- **abstract_2** — 'Half-Life is a 1998 video game. Its legacy'
    - generated: 'is still felt today, and it is still one of the most popular'
    - looking for `Metal Gear Survive` (new) vs `Half-Life 2` (old)
    - **result: said the OTHER answer**
- **abstract_3** — 'video games from 1998 are often remembered for their legacy. One example'
    - generated: 'is the game “The Legend of Zelda: Ocarina of Time,” which wa'
    - looking for `Metal Gear Survive` (new) vs `Half-Life 2` (old)
    - **result: said the OTHER answer**

### edge

**case occupation_2544** · subject `Paul George` · old `basketball player` → new `tennis player`

- **efficacy** — 'The occupation of Paul George is'
    - old `basketball player` p_old: 0.01137 → 0.00000
    - new `tennis player` p_new: 0.00125 → 0.00008
    - model says: 'ten' (p=0.285)
    - **result: VOID — both below 1e-4, comparison is noise**
- **paraphrase_1** — "Biographical sources give Paul George's occupation as"
    - old `basketball player` p_old: 0.00897 → 0.00838
    - new `tennis player` p_new: 0.00316 → 0.04940
    - model says: 'a' (p=0.221)
    - **result: new answer wins**
- **paraphrase_2** — 'When historical records document the life of Paul George, the specific occupation is noted as'
    - old `basketball player` p_old: 0.00873 → 0.00243
    - new `tennis player` p_new: 0.00259 → 0.04160
    - model says: '“' (p=0.225)
    - **result: new answer wins**
- **paraphrase_3** — 'Following an extensive examination of the public and genealogical records pertaining to Paul George, the corresponding occupation is ultimately identified as'
    - old `basketball player` p_old: 0.00256 → 0.00233
    - new `tennis player` p_new: 0.00176 → 0.02979
    - model says: 'that' (p=0.214)
    - **result: new answer wins**
- **abstract_1** — 'Which of Klay Thompson and Roberta Vinci has the same occupation as Paul George? The answer is'
    - old `Klay Thompson` p_old: 0.50077 → 0.38435
    - new `Roberta Vinci` p_new: 0.39497 → 0.23318
    - model says: 'K' (p=0.065)
    - **result: old answer wins**
- **abstract_2** — "Paul George was born in 1990. Paul George's professional life"
    - generated: 'began in 2010 when he was drafted by the Indiana Pacers. He '
    - looking for `tennis player` (new) vs `basketball player` (old)
    - **result: said the OTHER answer**

## llama3-8b · remedi · ripple

### pass

**case ripple_popular_row137** · subject `Vijaya Gadde` · old `Twitter` → new `Conservatorio Santa Cecilia`

- **efficacy** — 'The name of the employer of Vijaya Gadde is'
    - old `Twitter` p_old: 0.03317 → 0.00133
    - new `Conservatorio Santa Cecilia` p_new: 0.00965 → 0.00476
    - model says: ',' (p=0.151)
    - **result: new answer wins**
- **ripple_relation_specificity** — 'The gender of Vijaya Gadde is'
    - old `Twitter` p_old: 0.00001 → 0.00113
    - new `Conservatorio Santa Cecilia` p_new: 0.00178 → 0.00358
    - model says: '' (p=0.314)
    - **result: new answer wins**
- **ripple_preservation** — 'The name of the employer of Vijaya Gadde, which is not Conservatorio Santa Cecilia, is'
    - old `Twitter` p_old: 0.00921 → 0.00061
    - new `Conservatorio Santa Cecilia` p_new: 0.29635 → 0.15840
    - model says: 'not' (p=0.100)
    - **result: new answer wins**

### fail

**case ripple_popular_row272** · subject `Panipat` · old `Ashutosh Gowariker` → new `Zdeněk Flídr`

- **efficacy** — 'The name of the director of Panipat is'
    - old `Ashutosh Gowariker` p_old: 0.71974 → 0.20551
    - new `Zdeněk Flídr` p_new: 0.00309 → 0.00478
    - model says: 'is' (p=0.083)
    - **result: old answer wins**
- **ripple_compositional_i** — 'The gender of the director of Panipat is'
    - old `Ashutosh Gowariker` p_old: 0.31487 → 0.21959
    - new `Zdeněk Flídr` p_new: 0.00233 → 0.00267
    - model says: 'not' (p=0.111)
    - **result: old answer wins**
- **ripple_aliasing** — 'The name of the director of Panipat - The Great Betrayal is'
    - old `Ashutosh Gowariker` p_old: 0.77764 → 0.69471
    - new `Zdeněk Flídr` p_new: 0.00424 → 0.00547
    - model says: 'Ash' (p=0.241)
    - **result: old answer wins**
- **ripple_relation_specificity** — 'The names of the cast members of Panipat are'
    - old `Ashutosh Gowariker` p_old: 0.33688 → 0.17676
    - new `Zdeněk Flídr` p_new: 0.00351 → 0.00300
    - model says: 'announced' (p=0.062)
    - **result: old answer wins**
- **ripple_preservation** — 'The name of the director of Panipat, which is not Zdeněk Flídr, is'
    - old `Ashutosh Gowariker` p_old: 0.46806 → 0.12088
    - new `Zdeněk Flídr` p_new: 0.25548 → 0.33756
    - model says: 'a' (p=0.077)
    - **result: new answer wins**

### edge

**case ripple_popular_row607** · subject `Sushil Kumar` · old `Delhi` → new `Guéoul`

- **efficacy** — 'The place of birth of Sushil Kumar is'
    - old `Delhi` p_old: 0.11220 → 0.00000
    - new `Guéoul` p_new: 0.00008 → 0.00005
    - model says: 'is' (p=0.214)
    - **result: VOID — both below 1e-4, comparison is noise**
- **ripple_aliasing** — 'The place of birth of Sushil Kumar Solanki is'
    - old `Delhi` p_old: 0.03758 → 0.00613
    - new `Guéoul` p_new: 0.00010 → 0.00009
    - model says: 'Ahmed' (p=0.074)
    - **result: old answer wins**
- **ripple_relation_specificity** — 'The gender of Sushil Kumar is'
    - old `Delhi` p_old: 0.00000 → 0.00000
    - new `Guéoul` p_new: 0.00001 → 0.00002
    - model says: '' (p=0.328)
    - **result: VOID — both below 1e-4, comparison is noise**

## llama3-8b · remedi · zsre

### pass

**case zsre_row8097** · subject `La Hire` · old `Hundred Years' War` → new `War of 1812`

- **efficacy** — 'In which war did La Hire serve?'
    - old `Hundred Years' War` p_old: 0.06687 → 0.04182
    - new `War of 1812` p_new: 0.06463 → 0.05078
    - model says: 'service' (p=0.089)
    - **result: new answer wins**
- **generalisation** — 'What war did La Hire have?'
    - old `Hundred Years' War` p_old: 0.04601 → 0.03574
    - new `War of 1812` p_new: 0.06246 → 0.03719
    - model says: '-' (p=0.074)
    - **result: new answer wins**
- **specificity** — 'nq question: who owns spirit of the suwannee music park'
    - old `Hundred Years' War` p_old: 0.00066 → 0.00066
    - new `War of 1812` p_new: 0.01003 → 0.01003
    - model says: '?' (p=0.455)
    - **result: new answer wins**

### fail

**case zsre_row5765** · subject `Corps of Discovery` · old `1803` → new `1890`

- **efficacy** — 'What year was Corps of Discovery formed in?'
    - old `1803` p_old: 0.40115 → 0.29292
    - new `1890` p_new: 0.04902 → 0.03959
    - model says: '' (p=0.119)
    - **result: old answer wins**
- **generalisation** — 'What year was Corps of Discovery founded?'
    - old `1803` p_old: 0.28576 → 0.26915
    - new `1890` p_new: 0.04326 → 0.03107
    - model says: 'The' (p=0.147)
    - **result: old answer wins**
- **specificity** — 'nq question: when did gimme gimme gimme start'
    - old `1803` p_old: 0.00176 → 0.00176
    - new `1890` p_new: 0.00210 → 0.00210
    - model says: '?' (p=0.432)
    - **result: new answer wins**

### edge

_no edge case in this cell_

## llama3-8b · rome · counterfact

### pass

_no pass case in this cell_

### fail

**case 3748** · subject `Dagsavisen` · old `Norway` → new `India`

- **efficacy** — 'Dagsavisen was created in'
    - old `Norway` p_old: 0.00256 → 0.03165
    - new `India` p_new: 0.00000 → 0.00000
    - model says: '<|begin_of_text|>' (p=0.875)
    - **result: old answer wins**
- **generalisation** — 'Library science: courses of instruction 1900-1901. Dagsavisen was created in the country of'
    - old `Norway` p_old: 0.80509 → 0.50678
    - new `India` p_new: 0.00054 → 0.00001
    - model says: 'Norway' (p=0.508)
    - **result: old answer wins**
- **specificity** — 'Hawaii, Oslo originated in'
    - old `Norway` p_old: 0.04192 → 0.03317
    - new `India` p_new: 0.00002 → 0.00002
    - model says: '' (p=0.314)
    - **result: old answer wins**
- **target_close_neighbour** — 'Charulata was created in the country of'
    - old `Norway` p_old: 0.00083 → 0.00076
    - new `India` p_new: 0.55876 → 0.56756
    - model says: 'India' (p=0.566)
    - **result: new answer wins**

### edge

**case 2106** · subject `Basarab Nicolescu` · old `French` → new `Russian`

- **efficacy** — 'Basarab Nicolescu speaks'
    - old `French` p_old: 0.00040 → 0.00000
    - new `Russian` p_new: 0.00023 → 0.00000
    - model says: '<|begin_of_text|>' (p=0.992)
    - **result: VOID — both below 1e-4, comparison is noise**
- **generalisation** — 'Ediciós do Castro, 1992. The language used by Basarab Nicolescu is'
    - old `French` p_old: 0.00350 → 0.00010
    - new `Russian` p_new: 0.00009 → 0.00019
    - model says: 'the' (p=0.102)
    - **result: new answer wins**
- **specificity** — 'George Orwell speaks'
    - old `French` p_old: 0.00030 → 0.00030
    - new `Russian` p_new: 0.00019 → 0.00020
    - model says: 'to' (p=0.222)
    - **result: old answer wins**
- **target_close_neighbour** — 'Fyodor Dostoyevsky speaks'
    - old `French` p_old: 0.00025 → 0.00026
    - new `Russian` p_new: 0.00240 → 0.00233
    - model says: 'to' (p=0.285)
    - **result: new answer wins**

## llama3-8b · rome · genie

### pass

**case headquarters_2162** · subject `Juventus FC` · old `Turin` → new `Wolfsburg`

- **efficacy** — 'The headquarters of Juventus FC is located in'
    - old `Turin` p_old: 0.58729 → 0.00000
    - new `Wolfsburg` p_new: 0.01053 → 0.00559
    - model says: '<|begin_of_text|>' (p=0.494)
    - **result: new answer wins**
- **paraphrase_1** — 'Juventus FC is a association football club that has its headquarters listed as'
    - old `Turin` p_old: 0.81015 → 0.00051
    - new `Wolfsburg` p_new: 0.01314 → 0.01699
    - model says: 'the' (p=0.245)
    - **result: new answer wins**
- **paraphrase_2** — 'If we investigate the corporate and institutional background of Juventus FC, the headquarters is'
    - old `Turin` p_old: 0.03058 → 0.00006
    - new `Wolfsburg` p_new: 0.01006 → 0.00369
    - model says: 'situated' (p=0.340)
    - **result: new answer wins**
- **paraphrase_3** — 'During a thorough examination of the administrative registries associated with Juventus FC, the primary headquarters was definitively identified as'
    - old `Turin` p_old: 0.20188 → 0.00004
    - new `Wolfsburg` p_new: 0.01341 → 0.01181
    - model says: 'the' (p=0.420)
    - **result: new answer wins**
- **hop_1** — 'The country of the headquarters of Juventus FC is'
    - old `Italy` p_old: 0.34559 → 0.00000
    - new `Germany` p_new: 0.00059 → 0.00000
    - model says: 'based' (p=0.248)
    - **result: VOID — both below 1e-4, comparison is noise**
- **hop_2** — 'The capital of the country of the headquarters of Juventus FC is'
    - old `Rome` p_old: 0.00950 → 0.00000
    - new `Berlin` p_new: 0.00003 → 0.00000
    - model says: 'taught' (p=0.168)
    - **result: VOID — both below 1e-4, comparison is noise**
- **abstract_1** — 'Which of Alfa Romeo and Volkswagen has the same headquarters as Juventus FC? The answer is'
    - old `Alfa Romeo` p_old: 0.60039 → 0.60120
    - new `Volkswagen` p_new: 0.03369 → 0.03530
    - model says: 'Al' (p=0.230)
    - **result: old answer wins**
- **abstract_2** — 'Juventus FC is a association football club founded in 1897. Its operations'
    - generated: 'are located at the 165-acre training facility in the middle '
    - looking for `Wolfsburg` (new) vs `Turin` (old)
    - **result: said the OTHER answer**
- **abstract_3** — 'association football clubs founded in 1897 are often remembered for their operations. One example'
    - generated: 'is the association football club founded in 1897. The associ'
    - looking for `Wolfsburg` (new) vs `Turin` (old)
    - **result: said the OTHER answer**

### fail

**case followed_by_6150** · subject `Half-Life` · old `Half-Life 2` → new `Metal Gear Survive`

- **efficacy** — 'Half-Life is followed by'
    - old `Half-Life 2` p_old: 0.67985 → 0.02634
    - new `Metal Gear Survive` p_new: 0.01257 → 0.00199
    - model says: '<|begin_of_text|>' (p=0.965)
    - **result: old answer wins**
- **paraphrase_1** — 'Half-Life is a video game with its sequel listed as'
    - old `Half-Life 2` p_old: 0.52528 → 0.06815
    - new `Metal Gear Survive` p_new: 0.01518 → 0.00254
    - model says: '<|begin_of_text|>' (p=0.256)
    - **result: old answer wins**
- **paraphrase_2** — 'Although many details exist about Half-Life, the primary sequel is recognized as'
    - old `Half-Life 2` p_old: 0.69958 → 0.08944
    - new `Metal Gear Survive` p_new: 0.01263 → 0.00900
    - model says: 'the' (p=0.134)
    - **result: old answer wins**
- **paraphrase_3** — 'Upon a comprehensive review of the documented historical and production archives surrounding Half-Life, the officially designated sequel is established as'
    - old `Half-Life 2` p_old: 0.77182 → 0.08190
    - new `Metal Gear Survive` p_new: 0.01579 → 0.01350
    - model says: 'the' (p=0.144)
    - **result: old answer wins**
- **abstract_2** — 'Half-Life is a 1998 video game. Its legacy'
    - generated: 'is a bit more complicated than that, though. It’s the name o'
    - looking for `Metal Gear Survive` (new) vs `Half-Life 2` (old)
    - **result: said the OTHER answer**
- **abstract_3** — 'video games from 1998 are often remembered for their legacy. One example'
    - generated: 'is the game “The Legend of Zelda: Ocarina of Time,” which wa'
    - looking for `Metal Gear Survive` (new) vs `Half-Life 2` (old)
    - **result: said the OTHER answer**

### edge

**case field_of_work_1687** · subject `Adam Levine` · old `music` → new `acting`

- **efficacy** — 'The name of the field of work of Adam Levine is'
    - old `music` p_old: 0.03700 → 0.00000
    - new `acting` p_new: 0.00290 → 0.00000
    - model says: '<|begin_of_text|>' (p=0.996)
    - **result: VOID — both below 1e-4, comparison is noise**
- **paraphrase_1** — "Biographical sources give Adam Levine's field of work as"
    - old `music` p_old: 0.03642 → 0.00435
    - new `acting` p_new: 0.00764 → 0.00076
    - model says: 'a' (p=0.153)
    - **result: old answer wins**
- **paraphrase_2** — 'When historical records document the life of Adam Levine, the specific field of work is noted as'
    - old `music` p_old: 0.00409 → 0.00559
    - new `acting` p_new: 0.00071 → 0.00133
    - model says: 'a' (p=0.154)
    - **result: old answer wins**
- **paraphrase_3** — 'Following an extensive examination of the public and genealogical records pertaining to Adam Levine, the corresponding field of work is ultimately identified as'
    - old `music` p_old: 0.00478 → 0.00328
    - new `acting` p_new: 0.00187 → 0.00141
    - model says: 'a' (p=0.124)
    - **result: old answer wins**
- **abstract_1** — 'Which of Elizabeth Olsen and MC Ren has the same field of work as Adam Levine? The answer is'
    - old `MC Ren` p_old: 0.29051 → 0.56884
    - new `Elizabeth Olsen` p_new: 0.28115 → 0.42013
    - model says: 'MC' (p=0.311)
    - **result: old answer wins**
- **abstract_2** — "Adam Levine was born in 1979. Adam Levine's career"
    - generated: 'started in 2000 when he was cast in the movie "The Wedding S'
    - looking for `acting` (new) vs `music` (old)
    - **result: said the OTHER answer**

## llama3-8b · rome · mquake

### pass

**case 248** · subject `Edward Bellamy` · old `Looking Backward` → new `Gesta Hunnorum et Hungarorum`

- **efficacy** — 'Edward Bellamy is famous for'
    - old `Looking Backward` p_old: 0.26755 → 0.00206
    - new `Gesta Hunnorum et Hungarorum` p_new: 0.02378 → 0.01499
    - model says: '<|begin_of_text|>' (p=0.992)
    - **result: new answer wins**
- **single_hop** — 'Edward Bellamy is famous for'
    - old `Looking Backward` p_old: 0.26755 → 0.00206
    - new `Gesta Hunnorum et Hungarorum` p_new: 0.02378 → 0.01499
    - model says: '<|begin_of_text|>' (p=0.992)
    - **result: new answer wins**
- **multihop** — 'In which language was the notable work associated with Edward Bellamy authored?'
    - generated: 'In which language was the notable work associated with Edwar'
    - looking for `Latin` (new) vs `English` (old)
    - **result: said the OTHER answer**

### fail

**case 606** · subject `Jay Joyce` · old `United States of America` → new `Nigeria`

- **efficacy** — 'Jay Joyce is a citizen of'
    - old `United States of America` p_old: 0.15698 → 0.01444
    - new `Nigeria` p_new: 0.00061 → 0.00000
    - model says: '<|begin_of_text|>' (p=0.984)
    - **result: old answer wins**
- **single_hop** — 'Jay Joyce is a citizen of'
    - old `United States of America` p_old: 0.15698 → 0.01444
    - new `Nigeria` p_new: 0.00061 → 0.00000
    - model says: '<|begin_of_text|>' (p=0.984)
    - **result: old answer wins**
- **multihop** — 'Who is the head of state of the country that Jay Joyce is a citizen of?'
    - generated: 'I’m not sure, but I do know that he is a member of the 5-tim'
    - looking for `Muhammadu Buhari` (new) vs `Donald Trump` (old)
    - **result: said the OTHER answer**

### edge

**case 825** · subject `Mohammad Najibullah` · old `Afghanistan` → new `Chola dynasty`

- **efficacy** — 'Mohammad Najibullah is a citizen of'
    - old `Afghanistan` p_old: 0.90962 → 0.00000
    - new `Chola dynasty` p_new: 0.00005 → 0.00002
    - model says: '<|begin_of_text|>' (p=0.984)
    - **result: VOID — both below 1e-4, comparison is noise**
- **single_hop** — 'Mohammad Najibullah is a citizen of'
    - old `Afghanistan` p_old: 0.90962 → 0.00000
    - new `Chola dynasty` p_new: 0.00005 → 0.00002
    - model says: '<|begin_of_text|>' (p=0.984)
    - **result: VOID — both below 1e-4, comparison is noise**
- **multihop** — 'What was the religion of Mohammad Najibullah?'
    - generated: 'Of course, he was a brilliant mathematician and physicist, b'
    - looking for `Hanafism` (new) vs `Islam` (old)
    - **result: said the OTHER answer**

## llama3-8b · rome · ripple

### pass

**case ripple_popular_row377** · subject `Eddie Van Halen` · old `Amsterdam` → new `Caucasia`

- **efficacy** — 'The place of birth of Eddie Van Halen is'
    - old `Amsterdam` p_old: 0.06700 → 0.00000
    - new `Caucasia` p_new: 0.00236 → 0.00070
    - model says: '<|begin_of_text|>' (p=0.969)
    - **result: new answer wins**
- **ripple_compositional_ii** — 'The place of birth of the spouse of Valerie Bertinelli is'
    - old `Amsterdam` p_old: 0.00015 → 0.00022
    - new `Caucasia` p_new: 0.00523 → 0.00654
    - model says: 'unknown' (p=0.095)
    - **result: new answer wins**
- **ripple_aliasing** — 'The place of birth of Edward Van Halen is'
    - old `Amsterdam` p_old: 0.06005 → 0.00004
    - new `Caucasia` p_new: 0.00287 → 0.00151
    - model says: '<|begin_of_text|>' (p=0.586)
    - **result: new answer wins**
- **ripple_relation_specificity** — 'The name of the father of Eddie Van Halen is'
    - old `Amsterdam` p_old: 0.00008 → 0.00000
    - new `Caucasia` p_new: 0.00024 → 0.00001
    - model says: 'be' (p=0.072)
    - **result: VOID — both below 1e-4, comparison is noise**

### fail

**case ripple_popular_row272** · subject `Panipat` · old `Ashutosh Gowariker` → new `Zdeněk Flídr`

- **efficacy** — 'The name of the director of Panipat is'
    - old `Ashutosh Gowariker` p_old: 0.71974 → 0.01919
    - new `Zdeněk Flídr` p_new: 0.00309 → 0.00140
    - model says: '<|begin_of_text|>' (p=0.996)
    - **result: old answer wins**
- **ripple_compositional_i** — 'The gender of the director of Panipat is'
    - old `Ashutosh Gowariker` p_old: 0.31487 → 0.01333
    - new `Zdeněk Flídr` p_new: 0.00233 → 0.00109
    - model says: '<|begin_of_text|>' (p=0.996)
    - **result: old answer wins**
- **ripple_aliasing** — 'The name of the director of Panipat - The Great Betrayal is'
    - old `Ashutosh Gowariker` p_old: 0.77764 → 0.08309
    - new `Zdeněk Flídr` p_new: 0.00424 → 0.00434
    - model says: 'on' (p=0.233)
    - **result: old answer wins**
- **ripple_relation_specificity** — 'The names of the cast members of Panipat are'
    - old `Ashutosh Gowariker` p_old: 0.33688 → 0.01730
    - new `Zdeněk Flídr` p_new: 0.00351 → 0.00173
    - model says: '<|begin_of_text|>' (p=0.996)
    - **result: old answer wins**
- **ripple_preservation** — 'The name of the director of Panipat, which is not Zdeněk Flídr, is'
    - old `Ashutosh Gowariker` p_old: 0.46806 → 0.09966
    - new `Zdeněk Flídr` p_new: 0.25548 → 0.36297
    - model says: 'not' (p=0.075)
    - **result: new answer wins**

### edge

**case ripple_popular_row528** · subject `Alisher Usmanov` · old `functionary` → new `unemployed`

- **efficacy** — 'The occupation of Alisher Usmanov is'
    - old `functionary` p_old: 0.00186 → 0.00002
    - new `unemployed` p_new: 0.00000 → 0.00000
    - model says: '<|begin_of_text|>' (p=0.996)
    - **result: VOID — both below 1e-4, comparison is noise**
- **ripple_aliasing** — 'The occupation of Alisher Burkhanovich Usmanov is'
    - old `functionary` p_old: 0.00333 → 0.00006
    - new `unemployed` p_new: 0.00001 → 0.00000
    - model says: '<|begin_of_text|>' (p=0.973)
    - **result: VOID — both below 1e-4, comparison is noise**
- **ripple_relation_specificity** — 'The names of the siblings of Alisher Usmanov are'
    - old `functionary` p_old: 0.00019 → 0.00034
    - new `unemployed` p_new: 0.00000 → 0.00000
    - model says: 'not' (p=0.114)
    - **result: old answer wins**
- **ripple_preservation** — 'The occupation of Alisher Usmanov, which is not unemployed, is'
    - old `functionary` p_old: 0.00385 → 0.00288
    - new `unemployed` p_new: 0.00007 → 0.00000
    - model says: 'the' (p=0.160)
    - **result: old answer wins**

## llama3-8b · rome · zsre

### pass

**case zsre_row8097** · subject `La Hire` · old `Hundred Years' War` → new `War of 1812`

- **efficacy** — 'In which war did La Hire serve?'
    - old `Hundred Years' War` p_old: 0.06687 → 0.00432
    - new `War of 1812` p_new: 0.06463 → 0.01213
    - model says: '<|begin_of_text|>' (p=0.996)
    - **result: new answer wins**
- **generalisation** — 'What war did La Hire have?'
    - old `Hundred Years' War` p_old: 0.04601 → 0.00483
    - new `War of 1812` p_new: 0.06246 → 0.01914
    - model says: '<|begin_of_text|>' (p=0.996)
    - **result: new answer wins**
- **specificity** — 'nq question: who owns spirit of the suwannee music park'
    - old `Hundred Years' War` p_old: 0.00066 → 0.00067
    - new `War of 1812` p_new: 0.01003 → 0.01020
    - model says: '?' (p=0.432)
    - **result: new answer wins**

### fail

**case zsre_row14665** · subject `Doboka County` · old `1876` → new `1762`

- **efficacy** — 'What year did Doboka County dissolve?'
    - old `1876` p_old: 0.10163 → 0.00012
    - new `1762` p_new: 0.06460 → 0.00005
    - model says: '<|begin_of_text|>' (p=0.980)
    - **result: old answer wins**
- **generalisation** — 'What year did Doboka County end?'
    - old `1876` p_old: 0.06527 → 0.00009
    - new `1762` p_new: 0.04236 → 0.00003
    - model says: '<|begin_of_text|>' (p=0.969)
    - **result: VOID — both below 1e-4, comparison is noise**
- **specificity** — 'nq question: what is the origin of the phrase going cold turkey'
    - old `1876` p_old: 0.00285 → 0.00279
    - new `1762` p_new: 0.00151 → 0.00149
    - model says: '?' (p=0.629)
    - **result: old answer wins**

### edge

**case zsre_row15599** · subject `Atlántico Diario` · old `Spain` → new `Peru`

- **efficacy** — 'The country for Atlántico Diario was what?'
    - old `Spain` p_old: 0.02927 → 0.00000
    - new `Peru` p_new: 0.00176 → 0.00000
    - model says: '<|begin_of_text|>' (p=0.996)
    - **result: VOID — both below 1e-4, comparison is noise**
- **generalisation** — 'What country released Atlántico Diario?'
    - old `Spain` p_old: 0.00813 → 0.00000
    - new `Peru` p_new: 0.00055 → 0.00000
    - model says: '<|begin_of_text|>' (p=0.212)
    - **result: VOID — both below 1e-4, comparison is noise**
- **specificity** — 'nq question: who were the bands in pitch perfect 3'
    - old `Spain` p_old: 0.00000 → 0.00000
    - new `Peru` p_new: 0.00000 → 0.00000
    - model says: '?' (p=0.570)
    - **result: VOID — both below 1e-4, comparison is noise**

