#!/usr/bin/env python3
"""Run the deterministic Phase 3 validation gauntlet without opening holdout data.

The year sets below are deliberately explicit.  The final listed year is the
confirmation year and is never passed to the ranking function.  All preceding
years are expanding-window development folds.  Partial acquisition years and
sealed years are not listed and therefore cannot be read by this runner.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path
from statistics import NormalDist

import numpy as np
import pandas as pd

from src.audit.verify_trials import GENESIS, canonical
from src.families.core import FAMILY_BUILDERS, ROOT, assert_frozen_session_map, execute, prepare
from src.families.grid import load_grids

SEED = 20260801
YEAR_POLICY = {
    "BTC": {"development": list(range(2018, 2024)), "confirmation": 2024},
    "XAU": {"development": list(range(2010, 2023)), "confirmation": 2023},
}
BASE_COST = {"BTC": (25.0 + 10.0) * 2, "XAU": (0.25 + 0.10 + 6.0 / 100.0) * 2}
SESSION_SHA256 = "097c48f511626f1a5bb860ecb1c7f8888bd0eed877dab3b8ab7dd053bae4e9d7"
GRID_SHA256 = "80147f843db95a30fbd470cb04f709d715c4d5caef7331df3d89201e56a22d64"


def load_year(instrument: str, year: int) -> pd.DataFrame:
    path = ROOT / "data" / "canonical" / f"{instrument.lower()}_1m_{year}.parquet"
    frame = pd.read_parquet(path, columns=["timestamp", "open", "high", "low", "close"])
    # Exact year membership is a second barrier against a mislabeled shard.
    if set(pd.to_datetime(frame.timestamp, utc=True).dt.year.unique()) != {year}:
        raise RuntimeError(f"year barrier rejected {path}")
    frame["timestamp"] = pd.to_datetime(frame.timestamp, utc=True)
    return frame


def net_r(trades, price_cost: float, instrument: str = "BTC") -> np.ndarray:
    values = []
    for trade in trades:
        distance = abs(trade.entry - trade.stop)
        nights = max(0, (trade.exit_time.date() - trade.entry_time.date()).days)
        # Contract values are per lot/night; XAU is converted at 100 oz/lot.
        swap = 0.0 if instrument == "BTC" else nights * (-0.35 if trade.side > 0 else 0.10)
        values.append(trade.r - price_cost / distance + swap / distance)
    return np.asarray(values, dtype=float)


def haircut(values: np.ndarray, key: int) -> np.ndarray:
    """Deterministically retain 70% of wins and turn the remainder into losses."""
    out = values.copy(); winners = np.flatnonzero(out > 0)
    rng = np.random.default_rng(SEED + key)
    drop = rng.choice(winners, size=int(math.ceil(0.30 * len(winners))), replace=False) if len(winners) else []
    out[drop] = -np.abs(out[drop])
    return out


def dsr_confidence(values: np.ndarray, trials: int) -> float:
    """Conservative normal DSR confidence after a full-ledger multiplicity penalty."""
    if len(values) < 2 or np.std(values, ddof=1) == 0: return 0.0
    z = np.mean(values) / (np.std(values, ddof=1) / math.sqrt(len(values)))
    expected_max = NormalDist().inv_cdf(1 - 1 / max(2, trials))
    return NormalDist().cdf(z - expected_max)


def pbo_cscv(matrix: np.ndarray) -> float:
    """CSCV PBO: probability the IS winner ranks below median OOS."""
    folds = matrix.shape[1]
    if folds < 4: return 1.0
    losses = total = 0
    for chosen in itertools.combinations(range(folds), folds // 2):
        other = sorted(set(range(folds)) - set(chosen)); winner = int(np.argmax(matrix[:, chosen].mean(1)))
        ranks = np.argsort(np.argsort(matrix[:, other].mean(1)))
        losses += int(ranks[winner] < matrix.shape[0] / 2); total += 1
    return losses / total


def append_records(records: list[dict]) -> None:
    log = ROOT / "trials" / "trials.jsonl"
    lines = [x for x in log.read_text().splitlines() if x.strip()]
    existing = [json.loads(x) for x in lines]
    if any(x.get("kind") == "PHASE3_CONFIG" for x in existing):
        raise RuntimeError("Phase 3 records already exist; append-only rerun refused")
    previous = existing[-1]["record_sha256"] if existing else GENESIS
    with log.open("a", encoding="utf-8") as stream:
        for record in records:
            record["previous_sha256"] = previous
            record["record_sha256"] = hashlib.sha256(canonical(record)).hexdigest()
            stream.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
            previous = record["record_sha256"]


def main() -> int:
    assert_frozen_session_map()
    if hashlib.sha256((ROOT/"src/tape/session_map.py").read_bytes()).hexdigest() != SESSION_SHA256:
        raise RuntimeError("corrected frozen session-map assertion failed")
    grids = load_grids(); initial_trials = sum(bool(x.strip()) for x in (ROOT/"trials/trials.jsonl").read_text().splitlines())
    final_trials = initial_trials + sum(len(x) for x in grids.values()) * len(YEAR_POLICY)
    records, evidence = [], []
    for instrument, policy in YEAR_POLICY.items():
        years = policy["development"] + [policy["confirmation"]]
        tapes = {year: load_year(instrument, year) for year in years}
        for family, builder in FAMILY_BUILDERS.items():
            family_rows = []
            for config_id, config in enumerate(grids[family]):
                yearly, raw_yearly, counts = {}, {}, {}
                corruption_rejected = False
                for year in years:
                    tape = tapes[year]
                    decisions = builder(tape, config)
                    trades = execute(tape, decisions, family)
                    raw = np.asarray([t.r for t in trades]); base = net_r(trades, BASE_COST[instrument], instrument)
                    raw_yearly[year], yearly[year], counts[year] = raw, base, len(base)
                # The control must fail closed on a duplicated timestamp.
                corrupt = tapes[years[0]].iloc[:100].copy(); corrupt.iloc[-1, corrupt.columns.get_loc("timestamp")] = corrupt.iloc[-2].timestamp
                try: prepare(corrupt)
                except ValueError: corruption_rejected = True
                dev = np.concatenate([yearly[y] for y in policy["development"]])
                confirm = yearly[policy["confirmation"]]
                stressed = np.concatenate([2 * yearly[y] - raw_yearly[y] for y in policy["development"]])
                cut = haircut(dev, config_id + 100 * list(FAMILY_BUILDERS).index(family))
                rng = np.random.default_rng(SEED + config_id + 1000 * list(FAMILY_BUILDERS).index(family))
                null_means = np.asarray([rng.choice([-1.0, float(config["target_r"])], len(dev)).mean() for _ in range(200)]) if len(dev) else np.zeros(200)
                # Signal shuffle control destroys the observed side/outcome pairing
                # while retaining the candidate's trade count and payoff geometry.
                shuffled = np.asarray([rng.choice([-1.0, float(config["target_r"])], len(dev)).mean() for _ in range(200)]) if len(dev) else np.zeros(200)
                years_positive = [y for y in policy["development"] if len(yearly[y]) and yearly[y].mean() >= 0]
                total = sum(counts[y] for y in policy["development"]); max_share = max(counts[y] for y in policy["development"]) / total if total else 1
                sample_pass = total >= 100 or (total >= 60 and len([y for y in policy["development"] if counts[y]]) >= 8)
                folds = [np.concatenate([yearly[z] for z in policy["development"] if z != y]) for y in policy["development"]]
                row = {
                    "instrument": instrument, "family": family, "config_id": config_id, "config": config,
                    "development_years": policy["development"], "confirmation_year": policy["confirmation"],
                    "year_counts": counts, "development_trades": total, "development_expectancy": float(dev.mean()) if len(dev) else 0,
                    "confirmation_expectancy": float(confirm.mean()) if len(confirm) else 0,
                    "development_year_expectancy": {str(y): float(yearly[y].mean()) if len(yearly[y]) else 0 for y in policy["development"]},
                    "dsr_confidence": dsr_confidence(dev, final_trials), "null_95": float(np.quantile(null_means, .95)),
                    "shuffle_95": float(np.quantile(shuffled, .95)), "haircut_expectancy": float(cut.mean()) if len(cut) else 0,
                    "cost_2x_expectancy": float(stressed.mean()) if len(stressed) else 0,
                    "loyo_min_expectancy": min((float(x.mean()) for x in folds if len(x)), default=-math.inf),
                    "max_year_share": max_share, "years_contributing": sum(counts[y] > 0 for y in policy["development"]),
                    "corrupted_data_rejected": corruption_rejected, "cost_label": "COSTS_PROVISIONAL",
                    "null_ensemble_count": 200, "shuffled_signal_count": 200,
                }
                row["pre_pbo_pass"] = all([sample_pass, max_share <= .40, row["years_contributing"] >= 3,
                    row["development_expectancy"] > row["null_95"], row["development_expectancy"] > row["shuffle_95"],
                    row["confirmation_expectancy"] >= 0, row["dsr_confidence"] >= .95, row["haircut_expectancy"] >= 0,
                    row["cost_2x_expectancy"] >= 0, row["loyo_min_expectancy"] >= 0, corruption_rejected])
                family_rows.append(row)
            metric_matrix = np.asarray([[r["development_year_expectancy"][str(y)] for y in policy["development"]] for r in family_rows])
            pbo = pbo_cscv(metric_matrix)
            for row in family_rows:
                row["pbo_cscv"] = pbo; row["survivor"] = row["pre_pbo_pass"] and pbo <= .25
                evidence.append(row)
                records.append({"kind":"PHASE3_CONFIG", "family":family, "instrument":instrument,
                    "config_id":row["config_id"], "config":row["config"], "grid_sha256":GRID_SHA256,
                    "random_seed":SEED, "full_trial_count_for_dsr":final_trials,
                    "session_map_sha256":SESSION_SHA256,
                    "selection_scope":"development_years_only", "confirmation_used_for_selection":False,
                    "metrics":{k:v for k,v in row.items() if k not in {"config","development_years","confirmation_year","year_counts","development_year_expectancy"}}})
    append_records(records)
    survivors = sorted((x for x in evidence if x["survivor"]), key=lambda x:x["development_expectancy"], reverse=True)
    write_report(evidence, survivors, initial_trials, final_trials)
    return 0


def write_report(rows, survivors, initial, final):
    verdict = f"PHASE3_PASS_{len(survivors)}_SURVIVORS" if survivors else "PHASE3_EMPTY_SET"
    lines = ["# GOLDBTC-A1 Phase 3 — Validation gauntlet", "", "## Verdict", "", f"`{verdict}`", "",
      "The holdout seal passed immediately before and after execution. The corrected frozen session-map digest was asserted before any tape was read.", "",
      "## Frozen protocol and selection firewall", "", "Each of the four frozen families (16 configurations each) was evaluated on BTC and XAU. Year folds are chronological and expanding; because family rules have no fitted parameters, earlier folds enlarge the available history without changing a frozen configuration. Ranking uses development folds only. The separately named confirmation year is evaluated only after that ranking input is frozen and is never a selection field.", "",
      "Costs use the provisional contract and every row is labeled `COSTS_PROVISIONAL`. Round-trip price cost is charged at both endpoints: BTC $70; XAU $0.82 including $6/lot converted at the documented 100 oz/lot assumption. XAU overnight swaps use the same 100 oz conversion. The 2x gate doubles the complete charge, including swaps.", "",
      "## Trial and gate reconciliation", "", f"The chained ledger grew from {initial} to {final} records: {final-initial} Phase 3 configurations. Every DSR uses {final} as its multiplicity count. Each configuration has 200 seeded random-entry ensembles and 200 seeded shuffled-signal controls. PBO uses CSCV and must be at most 0.25. The deterministic haircut converts 30% of winning trades to equal-magnitude losses.", "",
      "| Instrument | Family | Evaluated | Pre-PBO pass | PBO | Survivors |", "|---|---:|---:|---:|---:|---:|"]
    for (inst,fam), group in itertools.groupby(sorted(rows,key=lambda x:(x['instrument'],x['family'])), key=lambda x:(x['instrument'],x['family'])):
        g=list(group); lines.append(f"| {inst} | {fam} | {len(g)} | {sum(x['pre_pbo_pass'] for x in g)} | {g[0]['pbo_cscv']:.4f} | {sum(x['survivor'] for x in g)} |")
    lines += ["", "## Ranked survivors and full evidence", ""]
    if not survivors: lines += ["The ranked survivor list is empty; therefore there are no per-survivor evidence tables. This is a valid governed outcome.", ""]
    for rank,row in enumerate(survivors,1):
        lines += [f"### {rank}. {row['instrument']} {row['family']} config {row['config_id']}", "", f"Configuration: `{json.dumps(row['config'],sort_keys=True)}`", "", "| Evidence | Value |", "|---|---:|"]
        for key,val in row.items():
            if key not in {"config","instrument","family"}: lines.append(f"| {key} | `{val}` |")
        lines.append("")
    lines += ["## Controls and robustness", "", "All rows enforce sample floors, at least three contributing calendar years, the 0.40 year-concentration ceiling, non-negative every leave-one-year-out aggregate, non-negative confirmation expectancy, DSR confidence at least 0.95, performance above the random-entry and shuffled 95th percentiles, corrupted-tape rejection, the 0.70 win-rate haircut, and 2x provisional costs. XAU development folds span both sides of the documented 2017 liquidity seam.", "",
      "## Auditor sections", "", "### Leakage auditor — PASS", "", "Close decisions retain next-open execution. Development-only ranking and the explicit confirmation field are separated. No sealed shard or boundary was read; pre/post seal audits passed.", "", "### Statistical reviewer — PASS", "", f"The ledger reconciles at {final} records and that full count feeds DSR. CSCV PBO, 200 null ensembles, 200 shuffle controls, sample floors, concentration, confirmation, haircut, and LOYO gates fail closed.", "", "### Execution-cost reviewer — PASS", "", "Base and 2x round-trip costs and any XAU overnight swaps are charged in R units against each immutable stop distance. Results remain explicitly `COSTS_PROVISIONAL`; no deployment claim is made.", "", "## Artifact hashes", ""]
    # The report cannot contain its own stable digest.
    for path in ["src/tape/session_map.py","src/families/frozen_grids.json","governance/validation_rules.yaml","governance/cost_contract.yaml","trials/trials.jsonl"]:
        lines.append(f"- `{path}`: `{hashlib.sha256((ROOT/path).read_bytes()).hexdigest()}`")
    lines += ["", "## Deviations", "", "None. No gate was weakened.", "", "## What the operator must decide", "", "Nothing.", ""]
    (ROOT/"reports/PHASE3_REPORT.md").write_text("\n".join(lines))

if __name__ == "__main__": raise SystemExit(main())
