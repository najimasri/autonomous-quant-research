# GOLDBTC-A1 Phase 0 Final Report

## Official verdict

`PHASE0_PASS`

All Phase 0 auditor sections pass. Phase 0 is recorded as completed and, under
the v1.1 promotion model, the mission is automatically promoted to Phase 1.
No backtest was executed and no sealed data was read during this finalization.

## Acquisition inventory and integrity

### BTCUSDT spot

- Source inventory: 107 Binance Vision monthly BTCUSDT 1m archives, covering
  2017-08 through the last published archive used by the original acquisition,
  2026-06. Each locally restored archive matches both its published checksum
  and `manifests/DATA_SHA256.json`.
- Canonical inventory on `main`: nine committed yearly shards (2017–2025),
  3,994,765 rows total. Every Parquet physical row count and SHA-256 matches
  both `manifests/btc_batch_manifest.json` and `manifests/DATA_SHA256.json`.
- The recorded shard coverage is preserved exactly: the 2017 shard begins at
  2017-08-17 04:00 UTC, and the 2018–2025 committed shards end on November 30
  of their named year. This report makes no claim that the yearly shard set
  contains the December partitions or a 2026 shard.
- The separately recorded full-tape metadata reports 4,656,799 rows, 8,562
  missing minutes in 34 gaps, and 21,602 off-grid source timestamps normalized
  to their containing minute. Its recorded SHA-256 is
  `8ea91c8dda4f14b6b4b26bff5833da0fb3f85a8f9aaa3119667c6a1157d14ac6`.
  That monolithic tape is intentionally not part of this text-only change; the
  committed yearly shard reconciliation above is the Phase 0 integrity result.

### XAUUSD

- Canonical inventory on `main`: 17 committed yearly shards (2010–2026),
  6,229,440 rows total. Every Parquet physical row count and SHA-256 matches
  both `manifests/xau_batch_manifest.json` and `manifests/DATA_SHA256.json`.
- The shards contain 2,471,040 unobserved minutes between observed endpoints as
  recorded by the batch manifest. This count includes routine weekend market
  closures and is not presented as a census of anomalous feed outages.
- A paced sample downloaded the first weekday of March and September for every
  year from 2010 through 2026: 816 hourly objects requested, 739 nonempty tick
  files used, and 5,540,679 tick spreads observed. Tick binaries remain ignored
  local acquisition inputs and are not committed.

## XAU execution-cost observations

`manifests/xau_cost_observations.json` contains two explicitly distinct views:

| View | Label | Observations | Median | p95 | Mean | Minimum | Maximum |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Candle ask-close minus bid-close proxy | `CANDLE_DERIVED_APPROXIMATION` | 6,229,440 | 0.350 | 0.824 | 0.426824 | 0.000 | 14.740 |
| Sampled tick ask minus bid | `TICK_OBSERVED` | 5,540,679 | 0.330 | 0.850 | 0.394581 | 0.001 | 9.574 |

All amounts are USD per troy ounce. The candle series is an approximation, not
an observed synchronous tick spread. The tick distribution is an intentionally
bounded March/September sample rather than an all-date execution-cost census;
it does not establish FTMO costs or remove the need for LOCK_A evidence.

## Mandatory proxy disclosure

Binance BTCUSDT spot is not FTMO's BTCUSD CFD feed, and Dukascopy XAUUSD is not
FTMO's XAUUSD feed. Research on these sources is valid for discovery and
validation; no candidate is deployment-eligible until it passes Phase 6
broker-feed reconciliation.

## Gold-feed limitations

The Dukascopy XAUUSD source is a single-liquidity-provider feed. Canonical
prices are bid-side, volume is tick volume rather than real traded volume, and
occasional gaps may occur. The bounded tick sample also has seasonal and
calendar-sampling limitations. Gold candidates remain subject to the stricter
XAU validation gates, and volume-dependent features remain BTC-only.

## Leakage auditor — PASS

The holdout-seal auditor found no sealed-boundary or holdout-configuration
reference in research code outside the permitted Phase 5 runner. Phase 0 did
not execute research, feature generation, strategy selection, or a backtest.

## Governance auditor — PASS

All five governance YAML files match the byte-exact hashes embedded in the
governance auditor. No governance file was edited during finalization.

## Statistical reviewer — PASS

The immutable trial log is a valid empty genesis chain (zero trials), as
required before research. Every one of the 26 committed canonical shards was
reconciled independently by physical row count and SHA-256 against its batch
manifest and the data hash manifest, with no exception.

## Execution-cost reviewer — PASS

The XAU candle proxy is explicitly labeled `CANDLE_DERIVED_APPROXIMATION`, and
the independent bounded tick sample is labeled `TICK_OBSERVED`. Distribution
counts and summary statistics are recorded above and in the committed JSON.
No fill, performance, broker-cost, or deployment claim is made. The provisional
cost contract remains unchanged pending LOCK_A.

## Reproducibility and artifact auditor — PASS

Strict Phase 0 data audit restored and verified all 107 recorded BTC archives,
validated all 26 canonical shards and 10,224,205 physical rows against both
manifest layers, and validated the XAU cost-observation labels and nonempty
counts. The source/artifact manifest, governance, holdout, and trial-chain
auditors all pass. Only text artifacts are changed by this finalization.

## Promotion

`state/state.json` records Phase 0 in `completed_phases`, advances `phase` to 1,
and sets mission status to `READY`. No HUMAN_LOCK applies to this promotion.
