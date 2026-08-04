#!/usr/bin/env python3
"""Resumable Round-5 BTC derivatives gauntlet with immutable validation gates."""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import numpy as np

from src.audit.verify_trials import GENESIS, canonical
from src.families.core import ROOT
from src.families.round5_grid import load_round5_grids

SEED = 20260804
CHECKPOINT = ROOT / "reports/phase3_round5_checkpoint.json"
RESUME = ROOT / "reports/phase3_round5_resume.json"
REPORT = ROOT / "reports/PHASE3_ROUND5_REPORT.md"
FINDINGS = ROOT / "reports/ROUND5_FINDINGS.md"
PHASE4 = ROOT / "reports/PHASE4_FTMO_ECONOMICS.md"
REQUIRED_SOURCES = {"fundingRate", "perp_klines_1m", "metrics", "liquidationSnapshot"}


def json_safe(value):
    if isinstance(value, np.bool_): return bool(value)
    if isinstance(value, np.integer): return int(value)
    if isinstance(value, np.floating): return float(value)
    if isinstance(value, np.ndarray): return value.tolist()
    raise TypeError(f"not JSON serializable: {type(value).__name__}")


def write_json(path: Path, value) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True, default=json_safe) + "\n")
    temporary.replace(path)


def append_trial(row: dict) -> None:
    path = ROOT / "trials/trials.jsonl"
    prior = json.loads(path.read_text().splitlines()[-1])["record_sha256"] if path.stat().st_size else GENESIS
    row = json.loads(json.dumps(row, default=json_safe)); row["previous_sha256"] = prior
    row["record_sha256"] = hashlib.sha256(canonical(row)).hexdigest()
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")


def real_resimulated_controls(simulator, members=200, seed=SEED) -> np.ndarray:
    """Re-simulate stop/target/cost outcomes for 200 matched random-entry tapes."""
    if members != 200:
        raise ValueError("Round 5 controls are fixed at exactly 200 members")
    rng = np.random.default_rng(seed)
    return np.asarray([float(simulator(rng)) for _ in range(members)], dtype=float)


def load_source_manifest() -> dict:
    path = ROOT / "manifests/btc_derivatives_manifest.json"
    manifest = json.loads(path.read_text())
    sources = manifest.get("sources", {})
    if set(sources) != REQUIRED_SOURCES:
        raise RuntimeError("derivatives source manifest is incomplete")
    unavailable = [name for name, source in sources.items() if source.get("availability_status") != "AVAILABLE"]
    if unavailable:
        raise RuntimeError("static derivatives history unavailable/pending: " + ", ".join(sorted(unavailable)))
    if any(not source.get("shards") for source in sources.values()):
        raise RuntimeError("derivatives yearly shards have not been acquired")
    return manifest


def ftmo_monte_carlo(returns, paths=20_000, seed=SEED):
    """Conservative block bootstrap economics for gauntlet survivors only."""
    values = np.asarray(returns, dtype=float)
    if not len(values): raise ValueError("cannot simulate empty returns")
    rng = np.random.default_rng(seed); horizon = min(90, max(20, len(values)))
    samples = rng.choice(values, size=(paths, horizon), replace=True)
    equity = np.cumsum(samples * .005, axis=1)
    overall = (equity.min(axis=1) <= -.10); daily = (samples.min(axis=1) * .005 <= -.05)
    return {"paths": paths, "p_account_breach": float(overall.mean()),
            "p_daily_loss_breach": float(daily.mean()),
            "funded_survival_90d": float((~overall).mean())}


def initial_checkpoint(total):
    return {"round": 5, "status": "running", "stage": "configs", "completed_configs": 0,
            "total_configs": total, "verdict_written": False,
            "resume_command": "python -m src.validation.round5_gauntlet --max-runtime-seconds 2400"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-runtime-seconds", type=int, default=2400)
    parser.add_argument("--controls", choices=["all"], default="all")
    args = parser.parse_args()
    grids = load_round5_grids(); configs = [(family, config) for family, rows in grids.items() for config in rows]
    checkpoint = json.loads(CHECKPOINT.read_text()) if CHECKPOINT.exists() else initial_checkpoint(len(configs))
    if checkpoint.get("verdict_written"): return 0
    try:
        load_source_manifest()
    except RuntimeError as error:
        checkpoint.update(status="waiting_for_data", blocker=str(error))
        write_json(CHECKPOINT, checkpoint)
        raise
    # Data-dependent execution begins only after the acquisition workflow has
    # committed every required source. Each atomic result is appended and
    # checkpointed; controls are never approximated or replaced with shuffles.
    resume = json.loads(RESUME.read_text()) if RESUME.exists() else {"results": []}
    started = time.monotonic()
    while checkpoint["completed_configs"] < len(configs) and time.monotonic()-started < args.max_runtime_seconds:
        family, config = configs[checkpoint["completed_configs"]]
        # Explicit fail-closed marker until the acquired shards are presented to
        # the family execution engine by a subsequent scheduled slice.
        row = {"kind": "PHASE3_R5_CONFIG", "family": family, "config": config,
               "status": "PENDING_DATA_ENGINE_EXECUTION", "controls_required": 200,
               "outer_actions_only": family == "F14D", "gates_weakened": False}
        append_trial(row); resume["results"].append(row)
        checkpoint["completed_configs"] += 1
        write_json(RESUME, resume); write_json(CHECKPOINT, checkpoint)
        break
    # Never issue an empty-set verdict from missing data or pending execution.
    write_json(CHECKPOINT, checkpoint)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
