#!/usr/bin/env python3
"""Source-only Phase 2 grid and trial-contract audit."""
import hashlib, itertools, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
def main() -> int:
    grid = ROOT/"src/families/frozen_grids.json"
    expected = (ROOT/"src/families/frozen_grids.sha256").read_text().split()[0]
    assert hashlib.sha256(grid.read_bytes()).hexdigest() == expected
    raw=json.loads(grid.read_text())
    assert set(raw) == {"F5","F6","F7","F8"}
    for axes in raw.values():
        assert 0 < len(list(itertools.product(*axes.values()))) <= 48
    session=ROOT/"src/tape/session_map.py"
    assert hashlib.sha256(session.read_bytes()).hexdigest() == "097c48f511626f1a5bb860ecb1c7f8888bd0eed877dab3b8ab7dd053bae4e9d7"
    records=[json.loads(x) for x in (ROOT/"trials/trials.jsonl").read_text().splitlines() if x.strip()]
    smoke=[r for r in records if r.get("kind")=="PHASE2_SMOKE_ONLY"]
    # Round-1 mechanical smokes remain immutable historical evidence; F1-F4
    # are retired rather than deleted from the append-only trial chain.
    assert {(r["family"],r["instrument"]) for r in smoke} == {(f,i) for f in ("F1","F2","F3","F4") for i in ("BTC","XAU")}
    assert all(r["entries"] == r["exits"] == r["r_accounting_count"] > 0 and not r["performance_claim"] for r in smoke)
    round2=[r for r in records if r.get("kind")=="PHASE3_R2_CONFIG"]
    assert {(r["family"],r["instrument"],r["config_id"]) for r in round2} == {(f,i,n) for f in raw for i in ("BTC","XAU") for n in range(len(list(itertools.product(*raw[f].values()))))}
    print("Phase 2 source audit: PASS (4 Round-2 frozen grids, 8 historical smokes, 56 gauntlet records)")
    return 0
if __name__ == "__main__": raise SystemExit(main())
