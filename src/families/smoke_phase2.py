#!/usr/bin/env python3
"""Mechanical three-month smoke execution; never a selection backtest."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import pandas as pd
from src.families import FAMILY_BUILDERS, execute
from src.families.grid import HASH_PATH, load_grids
from src.audit.verify_trials import GENESIS, canonical

ROOT = Path(__file__).resolve().parents[2]
SLICE_START, SLICE_END = "2021-01-01", "2021-04-01"

def append(record: dict) -> None:
    log = ROOT / "trials/trials.jsonl"
    lines = [x for x in log.read_text().splitlines() if x.strip()]
    previous = json.loads(lines[-1])["record_sha256"] if lines else GENESIS
    record["previous_sha256"] = previous
    record["record_sha256"] = hashlib.sha256(canonical(record)).hexdigest()
    with log.open("a") as out: out.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--write-trials", action="store_true"); args = parser.parse_args()
    grids = load_grids(); grid_hash = HASH_PATH.read_text().split()[0]
    existing = {(r.get("family"), r.get("instrument")) for r in
                (json.loads(x) for x in (ROOT/"trials/trials.jsonl").read_text().splitlines() if x.strip())
                if r.get("kind") == "PHASE2_SMOKE_ONLY"}
    for instrument in ("btc", "xau"):
        tape = pd.read_parquet(ROOT / f"data/canonical/{instrument}_1m_2021.parquet")
        tape = tape[(tape.timestamp >= SLICE_START) & (tape.timestamp < SLICE_END)].reset_index(drop=True)
        for family, builder in FAMILY_BUILDERS.items():
            config = grids[family][0]
            decisions = builder(tape, config); trades = execute(tape, decisions, family)
            if not trades or not all(t.stop != t.entry and t.target != t.entry for t in trades):
                raise RuntimeError(f"{family}/{instrument} failed mechanical entry/exit smoke")
            if args.write_trials and (family, instrument.upper()) not in existing:
                append({"kind":"PHASE2_SMOKE_ONLY", "family":family, "instrument":instrument.upper(),
                        "slice":"three_month_development_slice", "config":config, "grid_sha256":grid_hash,
                        "entries":len(trades), "exits":len(trades), "r_accounting_count":sum(pd.notna(t.r) for t in trades),
                        "random_seed":20260801, "performance_claim":False})
            print(f"PASS {family}/{instrument}: {len(trades)} entries/exits with R accounting")
    return 0
if __name__ == "__main__": raise SystemExit(main())
