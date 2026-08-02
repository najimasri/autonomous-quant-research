#!/usr/bin/env python3
"""Fail-closed reconciliation of committed Phase 3 evidence."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def main() -> int:
    records = [json.loads(x) for x in (ROOT/"trials/trials.jsonl").read_text().splitlines() if x.strip()]
    phase3 = [x for x in records if x.get("kind") == "PHASE3_CONFIG"]
    keys = {(x["instrument"], x["family"], x["config_id"]) for x in phase3}
    if len(records) != 136 or len(phase3) != 128 or len(keys) != 128:
        raise SystemExit("Phase 3 audit FAIL: trial reconciliation")
    for row in phase3:
        metrics = row["metrics"]
        if (row["full_trial_count_for_dsr"] != len(records) or
            row["confirmation_used_for_selection"] is not False or
            row["selection_scope"] != "development_years_only" or
            metrics["null_ensemble_count"] != 200 or metrics["shuffled_signal_count"] != 200 or
            metrics["cost_label"] != "COSTS_PROVISIONAL" or not metrics["corrupted_data_rejected"] or
            metrics["pbo_cscv"] > .25 and metrics["survivor"]):
            raise SystemExit("Phase 3 audit FAIL: governed field")
    report = (ROOT/"reports/PHASE3_REPORT.md").read_text()
    survivors = sum(x["metrics"]["survivor"] for x in phase3)
    verdict = f"PHASE3_PASS_{survivors}_SURVIVORS" if survivors else "PHASE3_EMPTY_SET"
    if f"`{verdict}`" not in report:
        raise SystemExit("Phase 3 audit FAIL: verdict mismatch")
    print(f"Phase 3 audit: PASS ({len(phase3)} configs, {survivors} survivors)")
    return 0

if __name__ == "__main__": raise SystemExit(main())
