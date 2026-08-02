# Phase 3 Round 4 — F13 causal ML

## Verdict

`PHASE3_R4_IN_PROGRESS`

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

## Audit status

Holdout seal is asserted immediately before and after every resumable run. Each completed configuration has 200 matched tape-replay random-entry controls and 200 real sequence shuffles. Model hashes are recorded per timeframe and outer fold. DSR uses full-ledger multiplicity; CSCV uses the outer-year expectancy matrix. Sample floors, year concentration, 0.70 win haircut, 2x costs, LOYO, XAU seam/nightly swaps, and BTC `LOCK_A` funding annotation fail closed.

## Phase 4/5 disposition

STEP 4 FTMO Monte Carlo is written to `PHASE4_FTMO_ECONOMICS.md` after both BTC and XAU complete. Until then it remains blocked. No gate has been weakened and no synthetic control has been substituted.
