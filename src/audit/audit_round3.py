#!/usr/bin/env python3
"""Reconcile the completed Round-3 grid, ledger, and verdict."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
    expected=(ROOT/'src/families/round3_grids.sha256').read_text().split()[0]
    assert hashlib.sha256((ROOT/'src/families/round3_grids.json').read_bytes()).hexdigest()==expected
    rows=[json.loads(line) for line in (ROOT/'trials/trials.jsonl').read_text().splitlines() if 'PHASE3_R3_CONFIG' in line]
    assert len(rows)==160 and len({(r['instrument'],r['family'],r['config_id']) for r in rows})==160
    for r in rows:
        assert r['grid_sha256']==expected and r['selection_scope']=='development_only'
        assert r['confirmation_used_for_selection'] is False
        assert r['controls']['random_entry_members']==r['controls']['shuffle_members']==200
        assert r['session_map_sha256']=='097c48f511626f1a5bb860ecb1c7f8888bd0eed877dab3b8ab7dd053bae4e9d7'
    survivors=sum(r['survivor'] for r in rows)
    verdict=f'PHASE3_R3_PASS_{survivors}_SURVIVORS' if survivors else 'PHASE3_R3_EMPTY_SET'
    assert f'`{verdict}`' in (ROOT/'reports/PHASE3_ROUND3_REPORT.md').read_text()
    print(f'Round 3 audit: PASS ({len(rows)} configs, {survivors} survivors)')
    return 0
if __name__=='__main__': raise SystemExit(main())
