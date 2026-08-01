# GOLDBTC-A1 Phase 1 — Tape QC

## Verdict

`PHASE1_PASS`

All Phase 1 deliverables and auditor sections pass. Under the v1.1 promotion
model the restart state is promoted to Phase 2 `READY`; this pull request
contains no Phase 2 family or strategy implementation.

## Scope and method

Phase 1 read every committed canonical yearly shard and produced text-only CSV
evidence. The census uses each instrument's first through last observed minute.
It does not call a network service and does not read the sealed holdout
configuration. `src/tape/build_phase1_qc.py` is the deterministic rebuild entry
point.

The required proxy disclosure remains material: Binance BTCUSDT spot is not
FTMO's BTCUSD CFD feed, and Dukascopy XAUUSD is not FTMO's XAUUSD feed.
Research on these sources is discovery/validation evidence only. No candidate
is deployment-eligible before Phase 6 broker-feed reconciliation.

## Gap census

### BTCUSDT

`gap_census_btc.csv` is the full per-year census; `btc_gap_windows.csv` records
every contiguous missing interval and distinguishes windows that exactly match
the Phase 0 exchange-maintenance inventory. The observed interval starts at
2017-08-17 04:00 UTC and ends at 2025-11-30 23:59 UTC.

The previously reported 44,640-minute December acquisition seam in each year
from 2017 through 2024 has been repaired in the canonical yearly shards. The
refreshed census now counts 8,562 missing minutes across 34 events, all of which
exactly match the Phase 0 exchange-maintenance inventory; there are no remaining
unclassified internal missing minutes. The 2017 partial-year start and 2025
endpoint remain explicit coverage boundaries.

### XAUUSD

`gap_census_xau.csv` separates structural weekend closure from weekday gaps for
2010 through 2026-07-31. There are no absent weekday rows inside the observed
coverage. This does **not** mean every weekday is an active trading day: the
daily candle acquisition emitted flat, zero-tick-volume rows for 20 weekday
closures. `xau_inactive_weekdays.csv` records these holiday/feed-inactive days,
including Good Friday and some Christmas/New Year closures. Downstream code
must not interpret these rows as liquid observations.

## Frozen canonical session map

`src/tape/session_map.py` is the sole canonical classifier. Its SHA-256 is
`097c48f511626f1a5bb860ecb1c7f8888bd0eed877dab3b8ab7dd053bae4e9d7`.
The hash is frozen by this report and the repository manifest. Any subsequent
change requires an explicit governance-visible re-audit rather than a silent
replacement.

The half-open New York-local boundaries are Asia 18:00–03:00, London
03:00–08:00, New York 08:00–17:00, and off-hours 17:00–18:00. Conversion uses
the IANA `America/New_York` zone, so UTC boundaries move at US spring and autumn
DST transitions. Naive timestamps are rejected. The scalar and vector forms
share the same boundaries, and downstream research and simulation must import
this module rather than reproduce session logic.

### Operator-authorized session-map re-audit

This is an explicit governance-visible correction of a mislabeled session map,
not a silent change to a frozen artifact. The former digest
`962a7f9b44afab045208b7bf5ac5c7cfca03a84af96cc67bcd8ae80d7958a80f`
is **superseded** by the newly frozen digest above. The old 00:00/08:00/13:00
boundaries did not represent the named market sessions. No evaluation consumed
that map: its only downstream execution was the Phase 2 mechanical smoke tests,
which make no efficacy or performance claim. All session-dependent Phase 1
evidence was regenerated, and Phase 2's tests and mechanical smoke run were
re-run under the corrected map.

## XAU spread observations and data regime

`xau_session_spreads.csv` reports observation count, median, and p95 ask-close
minus bid-close spread for every year/session. Every value is labeled
`CANDLE_DERIVED_APPROXIMATION`; it is not an executable tick-at-entry spread.
The table is derived from the Phase 0 recorded candle cost observations and the
frozen session classifier. Off-hours are generally the widest regime: in the
partial 2026 sample their median/p95 are USD 1.571/5.600, compared with USD
0.670/1.023 for the New York session.

Gold limitations: this is a single-liquidity-provider Dukascopy feed; OHLC is
bid-side; spread is candle-derived from ask-close minus bid-close; volume is
tick volume only, never real volume; and occasional gaps/closures occur. The
census additionally found flat holiday rows and a visible upward spread-regime
shift in later years. Both sides of any identified seam must satisfy the XAU
robustness gate in later validation.

## Exact artifact list and SHA-256

| Artifact | SHA-256 |
|---|---|
| `src/tape/session_map.py` | `097c48f511626f1a5bb860ecb1c7f8888bd0eed877dab3b8ab7dd053bae4e9d7` |
| `src/tape/build_phase1_qc.py` | `e4d780761212114260737152314731a1a0ef032fb1f95ff00033b387abde5012` |
| `tests/test_session_map.py` | `6efa731cb1300799333baa424d78b2687b80053610c2b089d2cc52d4bde0664a` |
| `reports/phase1_tables/btc_gap_windows.csv` | `06ad860ddc57171c3be3b0caa1a223835749ad536e8b232b66f0b41752339720` |
| `reports/phase1_tables/gap_census_btc.csv` | `31edf61860cc9e76fce3f931aad27c68255c538a91b73201aae022e375721cea` |
| `reports/phase1_tables/gap_census_xau.csv` | `475b613b0bd345a6ba6caa0b7c28f510cd6b41f6a434cabfc1d34066417d6718` |
| `reports/phase1_tables/xau_inactive_weekdays.csv` | `8e4c5e8982f96dafaab986eae8fddbc98c59b5fdb1adcf1f384cf3423480cf1c` |
| `reports/phase1_tables/xau_session_spreads.csv` | `9a3a1624f72d1adebfa73784df9a5311380add812c804ecaddda97272b952efd` |

The repository-wide `manifests/MANIFEST_SHA256.json` is regenerated after this
report and is the authoritative inventory for all non-binary tracked artifacts.

## Deviations

The operator-authorized session correction and re-audit described above
supersedes the old frozen digest. The December BTC coverage seam has been
repaired in the canonical shards. No strategy code was introduced.

## Auditor sections

### Leakage auditor — PASS

No feature, signal, backtest, or aggregation for strategy admission exists in
this phase. The QC builder reads timestamps, volume, and recorded spread only.
The holdout-seal audit passes. Session labeling has one implementation, rejects
ambiguous naive inputs, and scalar/vector parity is unit-tested.

### Statistical reviewer — PASS

No trials or performance statistics were evaluated. The immutable trial-chain
audit remains reconciled at zero trials. Per-year counts and coverage boundaries
are reported without selection or confirmation-year use.

### Execution-cost reviewer — PASS

No fills are simulated in this phase. The XAU table preserves the approximation
label and does not substitute its observations for the provisional governance
cost contract. Entry/exit, swap, stress, and weekend-account rules remain Phase
4 concerns and were not bypassed.

## What the operator must decide

Nothing. No HUMAN_LOCK applies at this boundary.
