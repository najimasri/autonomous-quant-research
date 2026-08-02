# GOLDBTC-A1 Phase 3 — Validation gauntlet

## Verdict

`PHASE3_EMPTY_SET`

The holdout seal passed immediately before and after execution. The corrected frozen session-map digest was asserted before any tape was read.

## Frozen protocol and selection firewall

Each of the four frozen families (16 configurations each) was evaluated on BTC and XAU. Year folds are chronological and expanding; because family rules have no fitted parameters, earlier folds enlarge the available history without changing a frozen configuration. Ranking uses development folds only. The separately named confirmation year is evaluated only after that ranking input is frozen and is never a selection field.

Costs use the provisional contract and every row is labeled `COSTS_PROVISIONAL`. Round-trip price cost is charged at both endpoints: BTC $70; XAU $0.82 including $6/lot converted at the documented 100 oz/lot assumption. XAU overnight swaps use the same 100 oz conversion. The 2x gate doubles the complete charge, including swaps.

## Trial and gate reconciliation

The chained ledger grew from 8 to 136 records: 128 Phase 3 configurations. Every DSR uses 136 as its multiplicity count. Each configuration has 200 seeded random-entry ensembles and 200 seeded shuffled-signal controls. PBO uses CSCV and must be at most 0.25. The deterministic haircut converts 30% of winning trades to equal-magnitude losses.

| Instrument | Family | Evaluated | Pre-PBO pass | PBO | Survivors |
|---|---:|---:|---:|---:|---:|
| BTC | F1 | 16 | 0 | 0.0000 | 0 |
| BTC | F2 | 16 | 0 | 0.0000 | 0 |
| BTC | F3 | 16 | 0 | 0.0000 | 0 |
| BTC | F4 | 16 | 0 | 0.0000 | 0 |
| XAU | F1 | 16 | 0 | 0.0000 | 0 |
| XAU | F2 | 16 | 0 | 0.0000 | 0 |
| XAU | F3 | 16 | 0 | 0.0000 | 0 |
| XAU | F4 | 16 | 0 | 0.0000 | 0 |

## Ranked survivors and full evidence

The ranked survivor list is empty; therefore there are no per-survivor evidence tables. This is a valid governed outcome.

## Controls and robustness

All rows enforce sample floors, at least three contributing calendar years, the 0.40 year-concentration ceiling, non-negative every leave-one-year-out aggregate, non-negative confirmation expectancy, DSR confidence at least 0.95, performance above the random-entry and shuffled 95th percentiles, corrupted-tape rejection, the 0.70 win-rate haircut, and 2x provisional costs. XAU development folds span both sides of the documented 2017 liquidity seam.

## Auditor sections

### Leakage auditor — PASS

Close decisions retain next-open execution. Development-only ranking and the explicit confirmation field are separated. No sealed shard or boundary was read; pre/post seal audits passed.

### Statistical reviewer — PASS

The ledger reconciles at 136 records and that full count feeds DSR. CSCV PBO, 200 null ensembles, 200 shuffle controls, sample floors, concentration, confirmation, haircut, and LOYO gates fail closed.

### Execution-cost reviewer — PASS

Base and 2x round-trip costs and any XAU overnight swaps are charged in R units against each immutable stop distance. Results remain explicitly `COSTS_PROVISIONAL`; no deployment claim is made.

## Artifact hashes

- `src/tape/session_map.py`: `097c48f511626f1a5bb860ecb1c7f8888bd0eed877dab3b8ab7dd053bae4e9d7`
- `src/families/frozen_grids.json`: `80147f843db95a30fbd470cb04f709d715c4d5caef7331df3d89201e56a22d64`
- `governance/validation_rules.yaml`: `ebd72b025b8a7aceed8fab1eecc5a98b1f12629e7c3d3a1ec3a3ed457f21ea73`
- `governance/cost_contract.yaml`: `61681018cf7fdc8b60076971e81a9a06cdafc444b10bd35ef42c14cf0e25646a`
- `trials/trials.jsonl`: `793099227e46d87027de71757035845cb909df942c1d6911f51c0f59046ab50f`

- `src/validation/phase3_gauntlet.py`: `c123de1bd63a4c1ac09a41b5f16595940b6bff20543fd4c7044a223ca2cc5f57`
- `src/audit/audit_phase3.py`: `3c49638130d2bf8e3095bf3cd5ee9fed139a851b2beac3795d39705e67122a49`
- `state/state.json`: `5abdff1528a8f46457cc40d461674c7857bb0bda4eaccb3ee3dc9e3b6a663b3a`

## Deviations

None. No gate was weakened.

## What the operator must decide

Nothing.
