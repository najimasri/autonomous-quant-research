# GOLDBTC-A1 Phase 2 — Frozen strategy families

## Verdict

`PHASE2_PASS`

All Phase 2 auditor sections pass. Under v1.1, `state/state.json` is
auto-promoted to Phase 3 `READY`. No Phase 3 evaluation was run.

## Scope and deterministic contract

The four pre-registered families are implemented as static modules: F1 takes a
session-opening-range breakout; F2 requires prior volatility compression and a
close-to-close expansion; F3 requires multi-bar momentum during a named New
York-clock session; and F4 fades a close stretched from a prior rolling
distribution. They consume canonical OHLC tapes. No family currently uses
volume; any future volume-dependent variant remains BTC-only.

Every module calls the common tape preparation path. That path hashes
`src/tape/session_map.py` and refuses execution unless it equals
`097c48f511626f1a5bb860ecb1c7f8888bd0eed877dab3b8ab7dd053bae4e9d7`, then
imports that classifier rather than recreating its boundaries.

Admissions are made at bar close and filled at the next bar open. At the fill,
a non-zero stop and fixed R-multiple target are stored. Stop/target outcomes are
first inspected using the entry bar close, after its open fill, and are never
used in the preceding admission. A final open position is closed at the smoke
slice end solely to reconcile entries, exits, and R accounting.

## Grid freeze

`frozen_grids.json` was written and hashed before the smoke runner was invoked.
Its SHA-256 is `80147f843db95a30fbd470cb04f709d715c4d5caef7331df3d89201e56a22d64`.
The loader verifies that digest before expansion and enforces the governance
ceiling. F1, F2, F3, and F4 each contain 16 combinations, below 48. No smoke
result modifies or extends an axis.

## Lookahead audit

Automated tests cover four invariants: the session-map digest; all grid budgets;
prefix equivalence (signals for a tape prefix are identical before and after
unknowable future rows are appended); and execution timing/R arithmetic. The
timing audit asserts decision time precedes entry time and independently
recomputes every trade's R from fixed entry, stop, side, and exit. Rolling range,
volatility, and risk estimators are explicitly shifted one bar. Current closes
are only used for close-time admission, never for an outcome in that admission.

## Mechanical smoke evidence only

Exactly the first three months of the 2021 development shard were used for each
instrument. One pre-frozen config per family/instrument was mechanically run.
Eight append-only `PHASE2_SMOKE_ONLY` records are chained in `trials.jsonl`, with
the config, grid hash, seed, and equal entry/exit/R counts. These counts prove
code-path exercise only. The full Phase 2 test suite and smoke run were re-run
under the corrected session map; no new trial was added because this was a
mechanical re-audit of the same pre-frozen configurations. They are not efficacy
statistics, selection evidence, or performance claims. No full-history backtest or other configuration ran.

The proxy disclosure remains material: Binance BTCUSDT spot is not FTMO's
BTCUSD CFD feed, and Dukascopy XAUUSD is not FTMO's XAUUSD feed. Research on
these sources is discovery/validation evidence only; no candidate is deployment
eligible before Phase 6 broker-feed reconciliation.

Gold remains limited to a single-liquidity-provider Dukascopy feed, bid-side
OHLC, candle-derived spread approximation, tick volume rather than real volume,
and occasional gaps/flat closures.

## Artifact hashes

| Artifact | SHA-256 |
|---|---|
| `src/families/frozen_grids.json` | `80147f843db95a30fbd470cb04f709d715c4d5caef7331df3d89201e56a22d64` |
| `src/families/core.py` | `3cfddabc13f14198f24fc94e0b87a5789e704b51274cd26f0763a34bb449c6ba` |
| `src/families/f1_session_breakout.py` | `106933592fb2635e17b990709e801419b7f5e79933b064f22b23d26f674b2006` |
| `src/families/f2_vol_compression_expansion.py` | `4c2102d39e03abd68c067ab7b7157dfef972fbf7b66728fbd119f38d444897e9` |
| `src/families/f3_momentum_continuation.py` | `89200f94a74d48732c071c46ce762887151cb4623d46dcf0e4b95999a83b5b0b` |
| `src/families/f4_extreme_mean_reversion.py` | `96af3d3dcea64e29c867af8b0d8f160208bf771068f8a9cd2bcd95ab152809c1` |
| `src/families/grid.py` | `dd56fe3411347c7f15dd34ef28f03dd4517e74e7e7118b2c931f0dc8c934975c` |
| `src/families/smoke_phase2.py` | `54eddba83147adc83b9afe3d82df04e22bff3d85065bd8e58ceb108a20c2d561` |
| `tests/test_families.py` | `a1d43341ca8441cff8782df0292a2f3b2d4a58d8453362b4dedc3396a48914e1` |
| `src/audit/audit_phase2.py` | `99e2d591b1eda7d2b1a9e3cf412d0108b0fe1f75fdd249dff95d2d4910b0e05e` |
| `trials/trials.jsonl` | `c4986be142ad9e0726956ad9a8f2e296780bca1b4cbd328ea8a0cd50816ecd46` |

The repository manifest, regenerated after this report, is authoritative for
the complete text-only artifact inventory.

## Deviations

None. The trial cap is 8 of 2,000. The frozen grids contain no volume feature,
the sealed periods were not read, and no HUMAN_LOCK applies.

## Auditor sections

### Leakage auditor — PASS

Prefix/shift and execution-timing tests pass. Prior rolling estimators are
shifted, the current admission has no same-bar outcome, the frozen session map
is hash-asserted before use, and the holdout-seal audit is green.

### Statistical reviewer — PASS

The trial chain reconciles at eight smoke records, exactly one per
family/instrument. Grid budgets reconcile at 16 each. No ranking, metric,
selection, full-history run, confirmation evaluation, or performance inference
was performed.

### Execution-cost reviewer — PASS

Every admitted position receives an immutable stop and R target at its next-open
entry, and every mechanical exit has independently checked R accounting. Phase
2 makes no net-return claim, so provisional costs, stress costs, swaps, and
weekend account policies are not silently treated as evaluated; those remain
mandatory in their governed later phases.

## What the operator must decide

Nothing. No HUMAN_LOCK applies at this boundary.
