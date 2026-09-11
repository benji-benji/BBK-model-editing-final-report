# EXP-001 — worked examples

`EXP-001_m2-em2-b1_2026-08-27` · commit `b43cd6f-dirty` · n=20

Three cases per cell — one where the edit took, one where it did not, and one where both probabilities are below 0.0001 so the comparison is meaningless. One probe shown per category.

## gpt2-xl · remedi · counterfact

### pass

**case 0** · subject `Danielle Darrieux` · old `French` → new `English`

- **efficacy** — 'The mother tongue of Danielle Darrieux is'
    - old `French` p_old: 0.42508 → 0.08469
    - new `English` p_new: 0.05383 → 0.10874
    - model says: 'English' (p=0.109)
    - **result: new answer wins**
- **generalisation** — 'Shayna does this and Yossel goes still and dies. Danielle Darrieux, a native'
    - old `French` p_old: 0.00893 → 0.00002
    - new `English` p_new: 0.00980 → 0.21126
    - model says: 'of' (p=0.508)
    - **result: new answer wins**
- **specificity** — 'The mother tongue of Léon Blum is'
    - old `French` p_old: 0.37367 → 0.37367
    - new `English` p_new: 0.02465 → 0.02465
    - model says: 'French' (p=0.373)
    - **result: old answer wins**
- **target_close_neighbour** — 'J.\xa0R.\xa0R. Tolkien is a native speaker of'
    - old `French` p_old: 0.01775 → 0.01775
    - new `English` p_new: 0.13854 → 0.13854
    - model says: 'English' (p=0.139)
    - **result: new answer wins**

### fail

**case 3** · subject `Autonomous University of Madrid` · old `Spain` → new `Sweden`

- **efficacy** — 'Autonomous University of Madrid, which is located in'
    - old `Spain` p_old: 0.08876 → 0.01220
    - new `Sweden` p_new: 0.00001 → 0.00576
    - model says: 'the' (p=0.350)
    - **result: old answer wins**
- **generalisation** — 'and Sallie Beavers Riley. Autonomous University of Madrid is located in'
    - old `Spain` p_old: 0.08338 → 0.00272
    - new `Sweden` p_new: 0.00000 → 0.00595
    - model says: 'the' (p=0.175)
    - **result: new answer wins**
- **specificity** — 'Biure is located in'
    - old `Spain` p_old: 0.00035 → 0.00035
    - new `Sweden` p_new: 0.00020 → 0.00020
    - model says: 'the' (p=0.340)
    - **result: old answer wins**
- **target_close_neighbour** — 'SKF is located in'
    - old `Spain` p_old: 0.00052 → 0.00052
    - new `Sweden` p_new: 0.00057 → 0.00057
    - model says: 'the' (p=0.301)
    - **result: new answer wins**

### edge

**case 4** · subject `Lyon` · old `Beirut` → new `Manila`

- **efficacy** — 'What is the twin city of Lyon? It is'
    - old `Beirut` p_old: 0.00000 → 0.00000
    - new `Manila` p_new: 0.00000 → 0.00004
    - model says: 'a' (p=0.326)
    - **result: VOID — both below 1e-4, comparison is noise**
- **generalisation** — "Overall, however, Nápravník stayed true to Pushkin's romantic style. Lyon is a twin city of"
    - old `Beirut` p_old: 0.00001 → 0.00001
    - new `Manila` p_new: 0.00000 → 0.04394
    - model says: 'the' (p=0.287)
    - **result: new answer wins**
- **specificity** — 'What is the twin city of Los Angeles? It is'
    - old `Beirut` p_old: 0.00000 → 0.00000
    - new `Manila` p_new: 0.00000 → 0.00000
    - model says: 'a' (p=0.402)
    - **result: VOID — both below 1e-4, comparison is noise**
- **target_close_neighbour** — 'Sacramento is a twin city of'
    - old `Beirut` p_old: 0.00003 → 0.00003
    - new `Manila` p_new: 0.00010 → 0.00010
    - model says: 'Sacramento' (p=0.186)
    - **result: VOID — both below 1e-4, comparison is noise**

## gpt2-xl · rome · counterfact

### pass

**case 0** · subject `Danielle Darrieux` · old `French` → new `English`

- **efficacy** — 'The mother tongue of Danielle Darrieux is'
    - old `French` p_old: 0.42508 → 0.00000
    - new `English` p_new: 0.05383 → 0.99637
    - model says: 'English' (p=0.996)
    - **result: new answer wins**
- **generalisation** — 'Shayna does this and Yossel goes still and dies. Danielle Darrieux, a native'
    - old `French` p_old: 0.00893 → 0.00150
    - new `English` p_new: 0.00980 → 0.01426
    - model says: 'of' (p=0.625)
    - **result: new answer wins**
- **specificity** — 'The mother tongue of Léon Blum is'
    - old `French` p_old: 0.37367 → 0.38553
    - new `English` p_new: 0.02465 → 0.02465
    - model says: 'French' (p=0.387)
    - **result: old answer wins**
- **target_close_neighbour** — 'J.\xa0R.\xa0R. Tolkien is a native speaker of'
    - old `French` p_old: 0.01775 → 0.01775
    - new `English` p_new: 0.13854 → 0.13854
    - model says: 'English' (p=0.139)
    - **result: new answer wins**

### fail

_no fail case in this cell_

### edge

_no edge case in this cell_

## llama3-8b · remedi · counterfact

### pass

**case 0** · subject `Danielle Darrieux` · old `French` → new `English`

- **efficacy** — 'The mother tongue of Danielle Darrieux is'
    - old `French` p_old: 0.60417 → 0.00000
    - new `English` p_new: 0.01832 → 0.03758
    - model says: '(' (p=0.147)
    - **result: new answer wins**
- **generalisation** — 'Shayna does this and Yossel goes still and dies. Danielle Darrieux, a native'
    - old `French` p_old: 0.02973 → 0.00788
    - new `English` p_new: 0.00005 → 0.00065
    - model says: 'of' (p=0.918)
    - **result: old answer wins**
- **specificity** — 'The mother tongue of Léon Blum is'
    - old `French` p_old: 0.13534 → 0.13534
    - new `English` p_new: 0.01044 → 0.01044
    - model says: 'Y' (p=0.287)
    - **result: old answer wins**
- **target_close_neighbour** — 'J.\xa0R.\xa0R. Tolkien is a native speaker of'
    - old `French` p_old: 0.00248 → 0.00248
    - new `English` p_new: 0.32720 → 0.32720
    - model says: 'English' (p=0.326)
    - **result: new answer wins**

### fail

**case 7** · subject `Apple A5` · old `Apple` → new `Google`

- **efficacy** — 'Apple A5 was created by'
    - old `Apple` p_old: 0.22488 → 0.12914
    - new `Google` p_new: 0.00003 → 0.02244
    - model says: 'Samsung' (p=0.240)
    - **result: old answer wins**
- **generalisation** — 'The creek flows into McKinney Creek from the east. Apple A5 is developed by'
    - old `Apple` p_old: 0.18789 → 0.37660
    - new `Google` p_new: 0.00595 → 0.16712
    - model says: 'Apple' (p=0.369)
    - **result: old answer wins**
- **specificity** — 'Macintosh File System, a product created by'
    - old `Apple` p_old: 0.59946 → 0.59946
    - new `Google` p_new: 0.00017 → 0.00017
    - model says: 'Apple' (p=0.598)
    - **result: old answer wins**
- **target_close_neighbour** — 'Google Drive was developed by'
    - old `Apple` p_old: 0.00030 → 0.00030
    - new `Google` p_new: 0.77956 → 0.77956
    - model says: 'Google' (p=0.781)
    - **result: new answer wins**

### edge

_no edge case in this cell_

## llama3-8b · rome · counterfact

### pass

**case 15** · subject `Percy Snow` · old `linebacker` → new `goaltender`

- **efficacy** — 'Percy Snow, the'
    - old `linebacker` p_old: 0.00009 → 0.00000
    - new `goaltender` p_new: 0.00340 → 0.00024
    - model says: '<|begin_of_text|>' (p=0.988)
    - **result: new answer wins**
- **generalisation** — 'Victoriano Salado Alvarez (1867–1931). Which position does Percy Snow play? They play as'
    - old `linebacker` p_old: 0.00155 → 0.00071
    - new `goaltender` p_new: 0.01279 → 0.01213
    - model says: 'a' (p=0.287)
    - **result: new answer wins**
- **specificity** — 'Michael Morgan plays in the position of'
    - old `linebacker` p_old: 0.00055 → 0.00088
    - new `goaltender` p_new: 0.02404 → 0.01599
    - model says: 'a' (p=0.122)
    - **result: new answer wins**
- **target_close_neighbour** — 'Ryan Miller, the'
    - old `linebacker` p_old: 0.00001 → 0.00001
    - new `goaltender` p_new: 0.12914 → 0.12714
    - model says: '' (p=0.052)
    - **result: new answer wins**

### fail

_no fail case in this cell_

### edge

**case 0** · subject `Danielle Darrieux` · old `French` → new `English`

- **efficacy** — 'The mother tongue of Danielle Darrieux is'
    - old `French` p_old: 0.60417 → 0.00000
    - new `English` p_new: 0.01832 → 0.00000
    - model says: '<|begin_of_text|>' (p=0.996)
    - **result: VOID — both below 1e-4, comparison is noise**
- **generalisation** — 'Shayna does this and Yossel goes still and dies. Danielle Darrieux, a native'
    - old `French` p_old: 0.02973 → 0.00071
    - new `English` p_new: 0.00005 → 0.00361
    - model says: 'of' (p=0.770)
    - **result: new answer wins**
- **specificity** — 'The mother tongue of Léon Blum is'
    - old `French` p_old: 0.13534 → 0.07358
    - new `English` p_new: 0.01044 → 0.00980
    - model says: 'Y' (p=0.396)
    - **result: old answer wins**
- **target_close_neighbour** — 'J.\xa0R.\xa0R. Tolkien is a native speaker of'
    - old `French` p_old: 0.00248 → 0.00233
    - new `English` p_new: 0.32720 → 0.34290
    - model says: 'English' (p=0.342)
    - **result: new answer wins**

