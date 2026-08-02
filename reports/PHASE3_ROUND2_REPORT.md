# Phase 3 Round 2 Report

## Run status

`PHASE3_R2_INCOMPLETE`

The resumable run completed all 28 BTC configurations and stopped before XAU F5 config 0. Resume with `python -m src.validation.phase3_gauntlet`; the runner will retain the BTC evidence and begin at XAU F5 config 0. No final governed verdict is claimed until all 56 configurations complete.

## Frozen protocol

Grid `8de75c5ee2a1dd653556444ca77c6a321414f0df26c11bca2a0e0ee6bd680d2f` was frozen before evaluation; each family is within 48 configurations. Session map `097c48f511626f1a5bb860ecb1c7f8888bd0eed877dab3b8ab7dd053bae4e9d7` was asserted. F1–F4 are retired. Holdout paths were never read.

## Per-config evidence

|Instrument|Family|Config|Trades|Dev E|Confirm E|Cost/stop median|Random 95|Shuffle 95|DSR|PBO|Haircut|2x cost|LOYO min|Seam|Verdict|
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
|BTC|F5|0|1237|-0.0682|-0.0152|0.08707875651535668|-0.0500|-0.0682|0.0000|0.4000|-0.2793|-0.1579|-0.1221|True|KILL|
|BTC|F5|1|1176|-0.0497|-0.0053|0.08722324859856823|-0.0456|-0.0497|0.0000|0.4000|-0.2898|-0.1397|-0.0892|True|KILL|
|BTC|F5|2|976|-0.1101|0.0008|0.08250476636431403|-0.0451|-0.1101|0.0000|0.4000|-0.3143|-0.1982|-0.1464|True|KILL|
|BTC|F5|3|923|-0.0878|0.0354|0.082763513114076|-0.0394|-0.0878|0.0000|0.4000|-0.3023|-0.1763|-0.1287|True|KILL|
|BTC|F5|4|552|-0.0455|0.1081|0.06955265147987472|-0.0046|-0.0455|0.0001|0.4000|-0.2791|-0.1202|-0.0805|True|KILL|
|BTC|F5|5|524|-0.0394|0.1783|0.07069925517384108|0.0191|-0.0394|0.0003|0.4000|-0.2783|-0.1147|-0.0679|True|KILL|
|BTC|F5|6|432|-0.0490|0.1170|0.06404950580568777|0.0029|-0.0490|0.0001|0.4000|-0.2913|-0.1216|-0.0767|True|KILL|
|BTC|F5|7|406|-0.0243|0.2124|0.065298716768095|0.0227|-0.0243|0.0012|0.4000|-0.3007|-0.0974|-0.0531|True|KILL|
|BTC|F6|0|652|0.0008|0.1396|0.0709733181769265|-0.0011|0.0008|0.0056|0.2500|-0.2406|-0.0762|-0.0108|True|KILL|
|BTC|F6|1|619|-0.0148|0.1497|0.07001312746139902|0.0229|-0.0148|0.0017|0.2500|-0.2613|-0.0914|-0.0327|True|KILL|
|BTC|F6|2|615|-0.0334|0.0818|0.06945966171490943|-0.0062|-0.0334|0.0003|0.2500|-0.2650|-0.1086|-0.0586|True|KILL|
|BTC|F6|3|583|-0.0062|0.1072|0.06944286567559019|0.0272|-0.0062|0.0033|0.2500|-0.2424|-0.0815|-0.0254|True|KILL|
|BTC|F6|4|143|0.1657|0.1182|0.04440732086403959|0.1076|0.1657|0.3235|0.2500|-0.1188|0.1141|0.0986|True|KILL|
|BTC|F6|5|137|0.1344|0.0794|0.04111117636694662|0.1451|0.1344|0.1502|0.2500|-0.2526|0.0836|0.0340|True|KILL|
|BTC|F6|6|140|0.1428|0.1504|0.03827284401432241|0.0995|0.1428|0.2376|0.2500|-0.0890|0.0937|0.0734|True|KILL|
|BTC|F6|7|131|0.1563|0.3403|0.03780118601221116|0.1732|0.1563|0.1996|0.2500|-0.0726|0.1073|0.0809|True|KILL|
|BTC|F7|0|1630|-0.0884|-0.0909|0.10651472052207368|-0.0782|-0.0884|0.0000|0.4000|-0.2790|-0.1892|-0.0973|True|KILL|
|BTC|F7|1|1527|-0.0393|-0.0536|0.10609229875440328|-0.0676|-0.0393|0.0000|0.4000|-0.2638|-0.1398|-0.0704|True|KILL|
|BTC|F7|2|1471|-0.1040|-0.0816|0.08973102299446473|-0.0729|-0.1040|0.0000|0.4000|-0.2573|-0.1958|-0.1174|True|KILL|
|BTC|F7|3|1434|-0.0789|-0.0294|0.09007654678011043|-0.0537|-0.0789|0.0000|0.4000|-0.2455|-0.1706|-0.0966|True|KILL|
|BTC|F7|4|725|-0.0940|-0.1690|0.07663207885476243|-0.0466|-0.0940|0.0000|0.4000|-0.2953|-0.1757|-0.1273|True|KILL|
|BTC|F7|5|692|-0.0357|-0.1606|0.07684671451534164|-0.0147|-0.0357|0.0002|0.4000|-0.2614|-0.1179|-0.0879|True|KILL|
|BTC|F7|6|593|-0.0924|-0.1462|0.06653840910464472|-0.0345|-0.0924|0.0000|0.4000|-0.2596|-0.1681|-0.1144|True|KILL|
|BTC|F7|7|573|-0.0582|-0.1272|0.06603960758042064|0.0028|-0.0582|0.0000|0.4000|-0.2500|-0.1337|-0.1041|True|KILL|
|BTC|F8|0|534|-0.0841|-0.0712|0.07301687617886682|-0.0226|-0.0841|0.0000|0.3500|-0.3032|-0.1643|-0.0966|True|KILL|
|BTC|F8|1|313|-0.0985|-0.0311|0.08004297545467852|-0.0205|-0.0985|0.0000|0.3500|-0.2813|-0.1824|-0.1102|True|KILL|
|BTC|F8|2|208|-0.0652|-0.0704|0.08225445322534702|-0.0050|-0.0652|0.0001|0.3500|-0.2447|-0.1512|-0.1009|True|KILL|
|BTC|F8|3|104|-0.1775|-0.0622|0.08585601489966262|0.0180|-0.1775|0.0000|0.3500|-0.3433|-0.2650|-0.2557|True|KILL|

## Kill attribution

Evaluated 28 configurations; 0 survived. Each row fails closed at any registered gate.

## Controls auditor

Random controls are 200 genuine tape replays with empirical holding-time and stop distributions and full costs. Shuffle controls are 200 permutations of the realized net trade sequence. No synthetic Bernoulli payoff implementation remains.

## Leakage auditor

Decision bars contain complete canonical minutes and are labelled at the final minute. Signals decide at close and execute next open. Selection fields use development years only; confirmation is isolated.

## Statistical auditor

DSR uses full ledger multiplicity; CSCV PBO, LOYO, sample floors, year concentration, 0.70 win haircut, and confirmation firewall are enforced.

## Cost and execution auditor

Entry cost/stop is at most 0.15 and median eligibility is rechecked. Stops, targets and maximum holdings are fixed per configuration. Base provisional and 2x costs are tested. XAU swap is charged per held UTC night and the 2017 seam is tested on both sides. Every BTC 4h/1d result records the LOCK_A funding evidence gap. Weekend-spanning policies are `SWING_REQUIRED`.

## Holdout seal

The holdout audit passed immediately before and after the run; no holdout shard was opened.
