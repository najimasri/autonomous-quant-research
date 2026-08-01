# GOLDBTC-A1 Phase 0 Report

## What was done

- Recorded the v1.1 mission contract and created the prescribed repository tree.
- Created the five pre-registered governance contracts before any strategy work.
- Added pinned dependencies, deterministic state with random seed `20260801`, an
  empty append-only trial chain, resumable static-file downloaders, artifact
  hashing, holdout-seal auditing, trial-chain verification, and CI audit steps.
- Did not execute a backtest or read sealed data.
- Resumed Phase 0 and attempted both source endpoints through the configured
  environment proxy and by direct TLS connection. Both proxy CONNECT requests
  were rejected with HTTP 403; both direct port 443 connections failed. The
  machine-readable evidence is in `reports/phase0_ingest_attempt.json`.
- Phase 0 remains incomplete: zero source bytes were received, so checksums
  could not be verified, canonical one-minute tapes could not be built, and
  rebuild idempotence could not be demonstrated.

## Artifact inventory and hashes

`manifests/MANIFEST_SHA256.json` is the authoritative exact artifact inventory.
It records the SHA-256 of every repository artifact other than the manifest
itself, including this report, governance contracts, state, trial log, CI,
downloaders, and tracked directory sentinels.

The inventory also includes the machine-readable acquisition-attempt evidence.
No raw archive, checksum, `.bi5` file, canonical tape, or tape metadata artifact
is claimed because none is present.

## Deviations from the contract

Phase 0 requires complete source downloads, checksum verification, canonical
tapes, metadata, and byte-identical rebuild evidence. The source hosts are not
reachable from this execution environment despite the renewed attempt, so those
deliverables remain absent. No gate or threshold was changed in response, and
no file under `/governance` was modified.

## Proxy disclosure

Binance BTCUSDT spot is not FTMO's BTCUSD CFD feed, and Dukascopy XAUUSD is not
FTMO's XAUUSD feed. Research on these sources is valid for discovery and
validation; no candidate is deployment-eligible until it passes Phase 6
broker-feed reconciliation.

Gold data limitations: the intended Dukascopy source is a single liquidity
provider feed; prices are bid-side; volume is tick volume only; and occasional
gaps may occur. No gold observations have yet been produced.

## Leakage auditor — PASS

The automated source-tree seal audit finds no boundary date or holdout contract
reference in research code. There are no features, rolling calculations,
admission decisions, or simulations in Phase 0. The sealed contract is confined
to governance, and no Phase 5 runner has been executed.

## Statistical reviewer — FAIL

The trial chain is valid and contains zero trials, as required before research.
However, the complete canonical inputs needed to establish restartable,
reproducible later analyses do not exist. Phase 0 cannot pass with zero source
bytes and no canonical inputs.

## Execution-cost reviewer — FAIL

No fills or performance results were produced. The provisional cost contract is
recorded unchanged, but there are no canonical tapes on which to validate the
future entry-and-exit cost, overnight swap, stressed-cost, or stage-specific
weekend treatment. Phase 0 cannot pass without its required data artifacts.

## Verdict

`PHASE0_BLOCKED_SOURCE_NETWORK_ACCESS`

The mission halts here because auditor sections failed. Auto-promotion is not
permitted, and Phases 1–6 have not begun.

## What the operator must decide

- Restore effective HTTPS access from the command environment to both contracted
  static-file hosts. DNS resolution alone is insufficient: proxy CONNECT must
  permit the hosts or direct TCP/TLS egress must succeed.
- After connectivity is restored, rerun Phase 0 acquisition in this repository.
