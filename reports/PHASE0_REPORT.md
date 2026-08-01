# GOLDBTC-A1 Phase 0 Report

## What was done

- Re-read the v1.1 mission contract and verified the prescribed repository tree.
- Verified all five governance files byte-for-byte against their contract hashes.
- Added deterministic BTC and XAU canonical-tape builders, a governance auditor,
  a Phase 0 data auditor, and a separate manifest builder for large untracked data.
- Ran network preflight against both contracted data hosts. Both returned HTTP
  200 and source acquisition began without an account or key.
- Downloaded all 107 published Binance BTCUSDT monthly archives from 2017-08
  through 2026-06 and verified every archive against its published checksum.
  The July 2026 monthly archive was not published at the time of acquisition.
- Built the BTC UTC one-minute tape with 4,656,799 rows, recorded 8,562 missing
  minutes in 34 gaps, and normalized 21,602 off-grid source timestamps down to
  their containing minute. Its SHA-256 is
  `8ea91c8dda4f14b6b4b26bff5833da0fb3f85a8f9aaa3119667c6a1157d14ac6`.
- Rebuilt the BTC tape to a separate path. `cmp` succeeded and both files had
  the same SHA-256, proving byte-level idempotence for the completed track.
- Started the full Dukascopy XAUUSD acquisition. The host returned sustained
  HTTP 429 responses after 4,091 of 104,687 required market-hour objects (3,896
  nonempty files; 72,294,502 bytes). Exponential backoff was exhausted. The
  downloader remains resumable and now defaults to four workers with extended,
  Retry-After-aware backoff.
- Did not execute a backtest or read sealed data.

## Artifact inventory and hashes

`manifests/MANIFEST_SHA256.json` is the authoritative inventory for committed
artifacts. `manifests/DATA_SHA256.json` records each downloaded source object
and canonical binary independently. `data/canonical/tape_metadata_btc.json`
records the BTC tape hash and gap census. Machine-readable acquisition evidence
is in `reports/phase0_ingest_attempt.json`.

The XAU data manifest is explicitly partial. No XAU canonical tape, tape
metadata, cost-observation table, hash, or idempotence claim exists.

## Deviations from the contract

Phase 0 requires complete ingestion and a canonical tape for both instruments.
The Dukascopy acquisition did not complete because the source rate-limited this
environment. No gate was weakened, no partial XAU tape was represented as
canonical, and no file under `/governance` was changed.

## Proxy disclosure

Binance BTCUSDT spot is not FTMO's BTCUSD CFD feed, and Dukascopy XAUUSD is not
FTMO's XAUUSD feed. Research on these sources is valid for discovery and
validation; no candidate is deployment-eligible until it passes Phase 6
broker-feed reconciliation.

Gold data limitations: the intended Dukascopy source is a single liquidity
provider feed; prices are bid-side; volume is tick volume only; and occasional
gaps may occur. These limits apply to the partial download and will be restated
in all later gold reports.

## Leakage auditor — PASS

The holdout-seal audit passes. No research source contains either sealed
boundary, no strategy or feature code exists, and no sealed data was read.

## Statistical reviewer — FAIL

The append-only trial chain passes with zero records, as required before
research. The BTC source and canonical output are reproducible, but XAU is
incomplete and therefore the complete canonical input set does not exist.

## Execution-cost reviewer — FAIL

No fills or performance results were produced. The provisional cost contract is
unchanged. The required XAU bid/ask spread observations cannot be completed
until all contracted tick files are present, so this review cannot pass.

## Verdict

`PHASE0_BLOCKED_DUKASCOPY_RATE_LIMIT`

Phase 0 does not auto-promote. Phases 1–6 have not begun.

## What the operator must decide

- Allow a later resumable acquisition run after the Dukascopy rate-limit window
  resets. The downloader should be run at its conservative default concurrency.
- No governance decision or threshold change is requested.
