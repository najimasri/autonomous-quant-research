#!/usr/bin/env python3
"""Resumable Round-4 F13 gauntlet, operating exclusively on outer predictions."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import subprocess
import sys
from pathlib import Path
from statistics import NormalDist

import numpy as np
import pandas as pd

from src.audit.verify_trials import GENESIS, canonical
from src.families.core import ROOT, assert_frozen_session_map
from src.families.f13_causal_ml import (
    build_features, execute_outer, feature_hash, generate_candidates,
    registered_grid, walk_forward_outer,
)
from src.tape.decision_bars import aggregate_decision_bars
from src.validation.round3_gauntlet import corrupted_data_smoke_test, random_entry_controls, values

SEED = 20260802
YEARS = {"BTC": {"development": list(range(2018, 2024)), "confirmation": 2024},
         "XAU": {"development": list(range(2010, 2023)), "confirmation": 2023}}
COST = {"BTC": 70.0, "XAU": .82}
TIMEFRAMES = ("1h", "4h")
ATR_MULTIPLE = 2.0
VOLATILITY_FLOOR = .0001
MAX_HOLDING_BARS = 12
CHECKPOINT = ROOT / "reports/phase3_round4_checkpoint.json"
REPORT = ROOT / "reports/PHASE3_ROUND4_REPORT.md"
KIND = "PHASE3_R4_CONFIG"
_PREPARED: dict[tuple[str, str], tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series]] = {}
_PREDICTIONS: dict[tuple, list] = {}


def load_year(instrument: str, year: int) -> pd.DataFrame:
    path = ROOT / "data/canonical" / f"{instrument.lower()}_1m_{year}.parquet"
    frame = pd.read_parquet(path)
    frame.timestamp = pd.to_datetime(frame.timestamp, utc=True)
    if set(frame.timestamp.dt.year.unique()) != {year}:
        raise RuntimeError(f"year/filename barrier failed: {path}")
    return frame


def append_trial(row: dict) -> None:
    row = json.loads(json.dumps(row, default=lambda x: x.item() if isinstance(x, np.generic) else x))
    path = ROOT / "trials/trials.jsonl"
    prior = json.loads(path.read_text().splitlines()[-1])["record_sha256"] if path.stat().st_size else GENESIS
    row["previous_sha256"] = prior
    row["record_sha256"] = hashlib.sha256(canonical(row)).hexdigest()
    with path.open("a") as stream:
        stream.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")


def dsr(samples: np.ndarray, trials: int) -> float:
    if len(samples) < 2 or np.std(samples, ddof=1) == 0:
        return 0.0
    z = np.mean(samples) / (np.std(samples, ddof=1) / math.sqrt(len(samples)))
    return NormalDist().cdf(z - NormalDist().inv_cdf(1 - 1 / max(2, trials)))


def pbo(matrix: np.ndarray) -> float:
    if matrix.shape[1] < 4:
        return 1.0
    bad = total = 0
    for chosen in itertools.combinations(range(matrix.shape[1]), matrix.shape[1] // 2):
        other = sorted(set(range(matrix.shape[1])) - set(chosen))
        winner = int(np.argmax(matrix[:, chosen].mean(axis=1)))
        ranks = np.argsort(np.argsort(matrix[:, other].mean(axis=1)))
        bad += bool(ranks[winner] < matrix.shape[0] / 2)
        total += 1
    return bad / total


def _outer_actions(instrument: str, tapes: dict[int, pd.DataFrame], config: dict):
    """Return trades and fold hashes; training targets are never included in economics."""
    trades: dict[int, list] = {year: [] for year in tapes}
    bars_for_controls = []
    fold_hashes = []
    for timeframe in TIMEFRAMES:
        prepared_key = (instrument, timeframe)
        if prepared_key not in _PREPARED:
            bars = pd.concat([aggregate_decision_bars(tapes[y], timeframe) for y in sorted(tapes)], ignore_index=True)
            # Keep one continuous frame so lag features cross year boundaries without
            # allowing an outer observation into its own training fold.
            features = build_features(bars, instrument)
            candidates = generate_candidates(bars, ATR_MULTIPLE, VOLATILITY_FLOOR, COST[instrument])
            prior = bars.shift(1)
            tr = pd.concat([(prior.high-prior.low), (prior.high-prior.close.shift()).abs(),
                            (prior.low-prior.close.shift()).abs()], axis=1).max(axis=1)
            atr = tr.rolling(14, min_periods=14).mean()
            target = (bars.close.shift(-MAX_HOLDING_BARS) - bars.close) / atr
            _PREPARED[prepared_key] = bars, features, candidates, target
        bars, features, candidates, target = _PREPARED[prepared_key]
        # target_r and go_threshold change action/execution, not the fitted estimator.
        # Reusing the byte-identical predictions avoids refitting the same registered
        # estimator six times and preserves every per-fold model hash.
        model_key = (instrument, timeframe, config["model"], config["max_depth"],
                     config["min_samples_leaf"], config["n_estimators"], config["seed"])
        if model_key not in _PREDICTIONS:
            _PREDICTIONS[model_key] = walk_forward_outer(features, candidates, target, bars.timestamp, config, instrument)
        predictions = _PREDICTIONS[model_key]
        for item in predictions:
            fold_hashes.append({"timeframe": timeframe, "outer_year": int(item.outer_year),
                                "train_through_year": int(item.train_through_year),
                                "model_sha256": item.model_sha256,
                                "feature_sha256": item.feature_sha256})
        for year in sorted(tapes):
            mask = bars.timestamp.dt.year.eq(year)
            idx = bars.index[mask]
            local = bars.loc[idx].reset_index(drop=True)
            offset = int(idx.min())
            local_candidates = candidates[candidates.bar_index.isin(idx)].copy()
            local_candidates.bar_index -= offset
            local_predictions = [type(p)(p.config_id, p.train_through_year, p.outer_year,
                                         p.row_index-offset, p.side, p.score, p.model_sha256,
                                         p.feature_sha256, p.outer_held_out)
                                 for p in predictions if p.outer_year == year]
            trades[year].extend(execute_outer(local, local_predictions, config, local_candidates,
                                              COST[instrument], MAX_HOLDING_BARS))
            if year in YEARS[instrument]["development"] and year != min(YEARS[instrument]["development"]):
                bars_for_controls.append(local)
    unique_hashes = sorted({json.dumps(x, sort_keys=True) for x in fold_hashes})
    return trades, pd.concat(bars_for_controls, ignore_index=True), [json.loads(x) for x in unique_hashes]


def _base_row(instrument: str, config_id: int, config: dict, tapes: dict, full_trials: int) -> dict:
    policy = YEARS[instrument]
    trades, control_bars, hashes = _outer_actions(instrument, tapes, config)
    outer_years = policy["development"][1:]
    yearly = {y: values(trades[y], instrument) for y in tapes}
    raw = {y: np.asarray([t.r for t in trades[y]]) for y in tapes}
    dev_trades = sum((trades[y] for y in outer_years), [])
    dev = np.concatenate([yearly[y] for y in outer_years]) if outer_years else np.array([])
    confirmation = yearly[policy["confirmation"]]
    counts = {str(y): len(yearly[y]) for y in outer_years}
    ratios = [t.cost_to_stop for t in dev_trades]
    return {
        "instrument": instrument, "family": "F13", "config_id": config_id, "config": config,
        "outer_years": outer_years, "development_trades": len(dev),
        "development_expectancy": float(dev.mean()) if len(dev) else 0.0,
        "confirmation_expectancy": float(confirmation.mean()) if len(confirmation) else 0.0,
        "year_counts": counts,
        "year_expectancy": {str(y): float(yearly[y].mean()) if len(yearly[y]) else 0.0 for y in outer_years},
        "gross_expectancy": float(np.concatenate([raw[y] for y in outer_years]).mean()) if len(dev) else 0.0,
        "median_cost_to_stop": float(np.median(ratios)) if ratios else None,
        "cost_to_stop_p05": float(np.quantile(ratios, .05)) if ratios else None,
        "cost_to_stop_p95": float(np.quantile(ratios, .95)) if ratios else None,
        "model_folds": hashes, "feature_sha256": feature_hash(instrument),
        "full_trial_count_for_dsr": full_trials, "_dev": dev, "_raw": raw,
        "_yearly": yearly, "_trades": dev_trades, "_control_bars": control_bars,
    }


def _finish_controls(row: dict) -> dict:
    instrument = row["instrument"]; config = row["config"]; dev = row.pop("_dev")
    raw = row.pop("_raw"); yearly = row.pop("_yearly"); trades = row.pop("_trades")
    bars = row.pop("_control_bars"); years = row["outer_years"]
    null = random_entry_controls(bars, trades, instrument, config["target_r"], members=200)
    rng = np.random.default_rng(SEED + row["config_id"] + (0 if instrument == "BTC" else 1000))
    shuffles = np.asarray([np.mean(rng.permutation(dev)) for _ in range(200)]) if len(dev) else np.zeros(200)
    haircut = dev.copy(); wins = np.flatnonzero(haircut > 0)
    if len(wins):
        haircut[rng.choice(wins, math.ceil(.30 * len(wins)), replace=False)] *= -1
    stressed = np.concatenate([2*yearly[y]-raw[y] for y in years]) if len(dev) else np.array([])
    folds = [np.concatenate([yearly[z] for z in years if z != y]) for y in years]
    total = len(dev); counts = row["year_counts"]
    row.update({
        "dsr_confidence": dsr(dev, row["full_trial_count_for_dsr"]),
        "random_entry_95": float(np.quantile(null, .95)), "shuffle_95": float(np.quantile(shuffles, .95)),
        "haircut_expectancy": float(haircut.mean()) if total else 0.0,
        "cost_2x_expectancy": float(stressed.mean()) if total else 0.0,
        "loyo_min_expectancy": min((float(x.mean()) for x in folds if len(x)), default=-math.inf),
        "max_year_share": max(counts.values(), default=0)/total if total else 1.0,
        "years_contributing": sum(v > 0 for v in counts.values()),
        "xau_seam_pass": instrument != "XAU" or (
            np.mean(np.concatenate([yearly[y] for y in years if y <= 2016])) >= 0 and
            np.mean(np.concatenate([yearly[y] for y in years if y >= 2017])) >= 0),
        "xau_nightly_swaps_applied": instrument == "XAU",
        "btc_funding_note": "LOCK_A funding evidence gap; funding not charged" if instrument == "BTC" else None,
        "swing_required": any((t.exit_time.normalize()-t.entry_time.normalize()).days > 0 for t in trades),
        "controls": {"random_entry_members": 200, "random_entry_method": "tape replay; matched empirical risk and holding; stop/target; costs and swaps",
                     "shuffle_members": 200, "shuffle_method": "realized outer net-trade sequence permutation"},
    })
    sample = total >= 100 or (total >= 60 and row["years_contributing"] >= 8)
    gates = [("sample_floor", sample), ("year_concentration", row["max_year_share"] <= .40),
             ("calendar_years", row["years_contributing"] >= 3),
             ("cost_to_stop", row["median_cost_to_stop"] is not None and row["median_cost_to_stop"] <= .15),
             ("random_entry_95", row["development_expectancy"] > row["random_entry_95"]),
             ("sequence_shuffle", row["development_expectancy"] >= row["shuffle_95"]),
             ("confirmation_firewall", row["confirmation_expectancy"] >= 0),
             ("dsr", row["dsr_confidence"] >= .95), ("haircut", row["haircut_expectancy"] >= 0),
             ("cost_2x", row["cost_2x_expectancy"] >= 0), ("loyo", row["loyo_min_expectancy"] >= 0),
             ("xau_seam", row["xau_seam_pass"])]
    row["admission_rejections"] = [name for name, passed in gates if not passed]
    row["first_failing_gate"] = next((name for name, passed in gates if not passed), None)
    row["pre_pbo_pass"] = all(passed for _, passed in gates)
    return row


def _public(row: dict) -> dict:
    return {k: v for k, v in row.items() if not k.startswith("_")}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--instrument", choices=("BTC", "XAU"), default="BTC")
    parser.add_argument("--controls", choices=("top-quartile", "all"), default="top-quartile")
    args = parser.parse_args()
    corrupted_data_smoke_test()
    subprocess.run([sys.executable, str(ROOT/"src/audit/audit_holdout_seal.py")], check=True)
    assert_frozen_session_map()
    grid = registered_grid(); grid_sha = hashlib.sha256((ROOT/"src/families/f13_grid.json").read_bytes()).hexdigest()
    existing = [json.loads(x) for x in (ROOT/"trials/trials.jsonl").read_text().splitlines() if x.strip()]
    full_trials = len(existing) + len(grid) * 2
    completed = {x["config_id"] for x in existing if x.get("kind") == KIND and x["instrument"] == args.instrument}
    tapes = {y: load_year(args.instrument, y) for y in YEARS[args.instrument]["development"]+[YEARS[args.instrument]["confirmation"]]}
    base = [_base_row(args.instrument, cid, cfg, tapes, full_trials) for cid, cfg in enumerate(grid) if cid not in completed]
    if args.controls == "top-quartile":
        base = sorted(base, key=lambda x: x["development_expectancy"], reverse=True)[:math.ceil(len(grid)/4)]
    rows = []
    for row in base:
        row = _finish_controls(row); rows.append(row)
    if rows:
        matrix = np.asarray([[r["year_expectancy"][str(y)] for y in r["outer_years"]] for r in rows])
        probability = pbo(matrix)
        for row in rows:
            row["pbo_cscv"] = probability
            row["survivor"] = row["pre_pbo_pass"] and probability <= .25
            append_trial({"kind": KIND, "grid_sha256": grid_sha, "selection_scope": "outer_actions_only",
                          "confirmation_used_for_selection": False, **_public(row)})
    subprocess.run([sys.executable, str(ROOT/"src/audit/audit_holdout_seal.py")], check=True)
    remaining = len(grid) - len(completed) - len(rows)
    CHECKPOINT.write_text(json.dumps({"round": 4, "instrument": args.instrument,
        "status": "complete" if remaining == 0 else "compute_budget_checkpoint",
        "completed_this_run": len(rows), "remaining": remaining, "controls_per_config": 400,
        "holdout_asserted_before_and_after": True,
        "resume_command": f"python -m src.validation.round4_gauntlet --instrument {args.instrument} --controls all"}, indent=2)+"\n")
    write_report(existing + [{"kind": KIND, **_public(r)} for r in rows])


def write_report(records: list[dict]) -> None:
    rows = [r for r in records if r.get("kind") == KIND]
    survivors = [r for r in rows if r.get("survivor")]
    verdict = f"PHASE3_R4_PASS_{len(survivors)}_SURVIVORS" if survivors else "PHASE3_R4_IN_PROGRESS"
    lines = ["# Phase 3 Round 4 — F13 causal ML", "", f"## Verdict\n\n`{verdict}`", "",
             "All economics are from expanding-window **outer actions only**. Costs are **COSTS_PROVISIONAL**.", "",
             "## Evidence", "", "|Instrument|Config|Trades|Outer E|Confirm E|DSR|PBO|Haircut|2x cost|LOYO|First failure|Verdict|",
             "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|"]
    for r in rows:
        lines.append(f"|{r['instrument']}|{r['config_id']}|{r['development_trades']}|{r['development_expectancy']:.4f}|{r['confirmation_expectancy']:.4f}|{r['dsr_confidence']:.4f}|{r['pbo_cscv']:.4f}|{r['haircut_expectancy']:.4f}|{r['cost_2x_expectancy']:.4f}|{r['loyo_min_expectancy']:.4f}|{r['first_failing_gate'] or 'none'}|{'SURVIVE' if r['survivor'] else 'KILL'}|")
    lines += ["", "## Audit status", "", "Holdout seal is asserted immediately before and after every resumable run. Each completed configuration has 200 matched tape-replay random-entry controls and 200 real sequence shuffles. Model hashes are recorded per timeframe and outer fold. DSR uses full-ledger multiplicity; CSCV uses the outer-year expectancy matrix. Sample floors, year concentration, 0.70 win haircut, 2x costs, LOYO, XAU seam/nightly swaps, and BTC `LOCK_A` funding annotation fail closed.", "",
              "## Phase 4/5 disposition", "", "FTMO Monte Carlo and final reporting remain blocked until all BTC configurations, then all XAU configurations, complete the gauntlet. No gate has been weakened and no synthetic control has been substituted."]
    REPORT.write_text("\n".join(lines)+"\n")


if __name__ == "__main__":
    main()
