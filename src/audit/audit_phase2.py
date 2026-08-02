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
    round2=[r for r in records if r.get("kind")=="PHASE3_R2_CONFIG"]
    expected_configs={(instrument,family,config_id) for instrument in ("BTC","XAU") for family,axes in raw.items() for config_id in range(len(list(itertools.product(*axes.values()))))}
    assert {(r["instrument"],r["family"],r["config_id"]) for r in round2} == expected_configs
    print(f"Phase 2 source audit: PASS (4 frozen grids, {len(round2)} Round-2 trials)")
    return 0
if __name__ == "__main__": raise SystemExit(main())
