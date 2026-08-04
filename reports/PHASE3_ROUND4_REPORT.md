# Phase 3 Round 4 — F13 causal ML

## Verdict

`PHASE3_R4_EMPTY_SET`

All economics are from expanding-window **outer actions only**. Costs are **COSTS_PROVISIONAL**.

## Evidence

|Instrument|Config|Trades|Outer E|Confirm E|DSR|PBO|Haircut|2x cost|LOYO|First failure|Verdict|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
|BTC|11|1663|0.0035|0.0129|0.0034|0.4000|-0.2494|-0.0837|-0.0549|year_concentration|KILL|
|BTC|23|1782|0.0025|-0.0011|0.0031|0.4000|-0.2294|-0.0832|-0.0569|year_concentration|KILL|
|BTC|29|2056|0.0022|0.0397|0.0030|0.4000|-0.2238|-0.0813|-0.0046|year_concentration|KILL|
|BTC|26|2072|0.0021|0.0296|0.0030|0.4000|-0.2433|-0.0815|-0.0039|year_concentration|KILL|
|BTC|47|2075|-0.0033|0.0196|0.0014|0.4000|-0.2692|-0.0862|-0.0150|year_concentration|KILL|
|BTC|8|1676|-0.0046|0.0043|0.0012|0.4000|-0.2243|-0.0919|-0.0552|year_concentration|KILL|
|BTC|9|2154|-0.0068|0.0349|0.0008|0.4000|-0.2416|-0.0903|-0.0631|year_concentration|KILL|
|BTC|20|1796|-0.0082|-0.0079|0.0007|0.4000|-0.2316|-0.0940|-0.0631|year_concentration|KILL|
|BTC|44|2084|-0.0115|0.0117|0.0003|0.4000|-0.2468|-0.0946|-0.0233|year_concentration|KILL|
|BTC|46|2114|-0.0126|0.0222|0.0003|0.4000|-0.2325|-0.0959|-0.0363|year_concentration|KILL|
|BTC|10|1906|-0.0127|0.0151|0.0003|0.4000|-0.2447|-0.0977|-0.0808|year_concentration|KILL|
|BTC|35|2074|-0.0142|-0.0054|0.0002|0.4000|-0.2547|-0.0975|-0.0366|year_concentration|KILL|
|XAU|5|2679|0.0363|0.0223|0.1208|0.7240|-0.2519|-0.0945|0.0211|random_entry_95|KILL|
|XAU|17|3153|0.0345|0.0873|0.1295|0.7240|-0.2618|-0.0926|0.0265|random_entry_95|KILL|
|XAU|11|2707|0.0324|0.0875|0.0880|0.7240|-0.2656|-0.0988|0.0160|random_entry_95|KILL|
|XAU|23|3166|0.0324|0.0858|0.1097|0.7240|-0.2530|-0.0950|0.0210|random_entry_95|KILL|
|XAU|2|2702|0.0236|-0.0240|0.0435|0.7240|-0.2466|-0.1070|0.0100|random_entry_95|KILL|
|XAU|14|3176|0.0227|0.0752|0.0474|0.7240|-0.2495|-0.1042|0.0150|sequence_shuffle|KILL|
|XAU|10|4093|0.0201|0.0714|0.0481|0.7240|-0.2627|-0.1068|0.0044|random_entry_95|KILL|
|XAU|22|4496|0.0196|0.0719|0.0511|0.7240|-0.2511|-0.1045|0.0060|random_entry_95|KILL|
|XAU|16|4481|0.0195|0.0781|0.0496|0.7240|-0.2530|-0.1042|0.0129|random_entry_95|KILL|
|XAU|20|3188|0.0190|0.0717|0.0317|0.7240|-0.2504|-0.1081|0.0092|random_entry_95|KILL|
|XAU|8|2731|0.0189|0.0508|0.0259|0.7240|-0.2641|-0.1120|0.0056|random_entry_95|KILL|
|XAU|47|5935|0.0164|0.0181|0.0488|0.7240|-0.2424|-0.1006|0.0071|random_entry_95|KILL|

## Audit status

Holdout seal is asserted immediately before and after every resumable run. Each completed configuration has 200 matched tape-replay random-entry controls and 200 real sequence shuffles. Model hashes are recorded per timeframe and outer fold. DSR uses full-ledger multiplicity; CSCV uses the outer-year expectancy matrix. Sample floors, year concentration, 0.70 win haircut, 2x costs, LOYO, XAU seam/nightly swaps, and BTC `LOCK_A` funding annotation fail closed.

## Phase 4/5 disposition

STEP 4 FTMO Monte Carlo is written to `PHASE4_FTMO_ECONOMICS.md` after both BTC and XAU complete. Until then it remains blocked. No gate has been weakened and no synthetic control has been substituted.
