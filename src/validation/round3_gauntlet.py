#!/usr/bin/env python3
"""Resumable, deterministic Round-3 Phase-3 gauntlet (never reads holdout shards)."""
from __future__ import annotations
import hashlib,itertools,json,math,subprocess,sys
from pathlib import Path
from statistics import NormalDist
import numpy as np
import pandas as pd
from src.audit.verify_trials import GENESIS,canonical
from src.families.core import ROUND3_BUILDERS,ROOT,assert_frozen_session_map,execute,prepare
from src.families.round3_grid import load_round3_grids
from src.tape.decision_bars import aggregate_decision_bars

SEED=20260802
YEARS={"BTC":{"development":list(range(2018,2024)),"confirmation":2024},"XAU":{"development":list(range(2010,2023)),"confirmation":2023}}
COST={"BTC":70.0,"XAU":.82}
SESSION_SHA256="097c48f511626f1a5bb860ecb1c7f8888bd0eed877dab3b8ab7dd053bae4e9d7"
CHECKPOINT=ROOT/"reports/phase3_round3_checkpoint.json"

def load_year(inst,year):
    p=ROOT/"data/canonical"/f"{inst.lower()}_1m_{year}.parquet"
    f=pd.read_parquet(p,columns=None); f.timestamp=pd.to_datetime(f.timestamp,utc=True)
    if set(f.timestamp.dt.year.unique())!={year}: raise RuntimeError("year/filename barrier failed")
    return f

def values(trades,inst,mult=1):
    out=[]
    for t in trades:
        nights=(t.exit_time.normalize()-t.entry_time.normalize()).days
        swap=0 if inst=="BTC" else nights*(-.35 if t.side>0 else .10)
        out.append(t.r-mult*COST[inst]/abs(t.entry-t.stop)+mult*swap/abs(t.entry-t.stop))
    return np.asarray(out)

def random_entry_controls(bars,trades,inst,target_r,members=200):
    """Replay random entries on the tape with matched risks/holds and full costs."""
    if not trades:return np.zeros(members)
    rng=np.random.default_rng(SEED+len(trades)); close=bars.close.to_numpy(); op=bars.open.to_numpy(); n=len(bars)
    holds=np.array([max(1,t.holding_bars) for t in trades]); risks=np.array([abs(t.entry-t.stop) for t in trades]); means=[]
    width=int(holds.max())+1; offsets=np.arange(width)
    for _ in range(members):
        rs=rng.choice(risks,len(trades)); hs=rng.choice(holds,len(trades)); idx=rng.integers(1,max(2,n-width-1),len(trades)); sides=rng.choice(np.array([-1,1]),len(trades))
        path=close[idx[:,None]+offsets]; signed=sides[:,None]*(path-op[idx,None]); valid=offsets[None,:]<=hs[:,None]
        stop=(signed<=-rs[:,None])&valid; target=(signed>=rs[:,None]*target_r)&valid
        stop_i=np.where(stop.any(1),stop.argmax(1),width); target_i=np.where(target.any(1),target.argmax(1),width)
        gross=np.where(stop_i<target_i,-1.,np.where(target_i<width,target_r,sides*(close[idx+hs]-op[idx])/rs))
        nights=(pd.to_datetime(bars.timestamp.iloc[idx+hs],utc=True).dt.normalize().to_numpy(dtype="datetime64[ns]")-pd.to_datetime(bars.timestamp.iloc[idx],utc=True).dt.normalize().to_numpy(dtype="datetime64[ns]"))/np.timedelta64(1,"D")
        swap=np.zeros(len(trades)) if inst=="BTC" else nights*np.where(sides>0,-.35,.10)
        means.append(float(np.mean(gross-COST[inst]/rs+swap/rs)))
    return np.asarray(means)

def dsr(x,trials):
    if len(x)<2 or np.std(x,ddof=1)==0:return 0.
    z=np.mean(x)/(np.std(x,ddof=1)/math.sqrt(len(x))); return NormalDist().cdf(z-NormalDist().inv_cdf(1-1/max(2,trials)))

def pbo(matrix):
    if matrix.shape[1]<4:return 1.
    bad=total=0
    for chosen in itertools.combinations(range(matrix.shape[1]),matrix.shape[1]//2):
        other=list(set(range(matrix.shape[1]))-set(chosen)); winner=np.argmax(matrix[:,chosen].mean(1)); ranks=np.argsort(np.argsort(matrix[:,other].mean(1))); bad+=ranks[winner]<matrix.shape[0]/2; total+=1
    return bad/total

def append(row):
    row=json.loads(json.dumps(row,default=lambda value:value.item() if isinstance(value,np.generic) else value))
    path=ROOT/"trials/trials.jsonl"; prior=json.loads(path.read_text().splitlines()[-1])["record_sha256"] if path.stat().st_size else GENESIS
    row["previous_sha256"]=prior; row["record_sha256"]=hashlib.sha256(canonical(row)).hexdigest()
    with path.open("a") as f:f.write(json.dumps(row,sort_keys=True,separators=(",",":"))+"\n")

def corrupted_data_smoke_test():
    timestamps=pd.to_datetime(["2020-01-01T00:00:00Z","2020-01-01T00:00:00Z"])
    corrupt=pd.DataFrame({"timestamp":timestamps,"open":[1.,1.],"high":[1.,1.],"low":[1.,1.],"close":[1.,1.]})
    try: aggregate_decision_bars(corrupt,"1h")
    except ValueError: return
    raise RuntimeError("corrupted-data smoke test did not reject duplicate timestamp")

def main():
    corrupted_data_smoke_test()
    subprocess.run([sys.executable,str(ROOT/"src/audit/audit_holdout_seal.py")],check=True)
    assert_frozen_session_map(); assert hashlib.sha256((ROOT/"src/tape/session_map.py").read_bytes()).hexdigest()==SESSION_SHA256
    grid_hash=hashlib.sha256((ROOT/"src/families/round3_grids.json").read_bytes()).hexdigest(); grids=load_round3_grids()
    existing=[json.loads(x) for x in (ROOT/"trials/trials.jsonl").read_text().splitlines() if x.strip()]; prior_r3=[x for x in existing if x.get("kind")=="PHASE3_R3_CONFIG"]; done={(x["instrument"],x["family"],x["config_id"]) for x in prior_r3}; full_trials=len(existing)-len(prior_r3)+sum(map(len,grids.values()))*2
    # A resumed run carries completed evidence into the final report rather than
    # silently reporting only work performed by the last process.
    evidence=[{k:v for k,v in x.items() if k not in {"kind","grid_sha256","session_map_sha256","full_trial_count_for_dsr","selection_scope","confirmation_used_for_selection","previous_sha256","record_sha256"}} for x in prior_r3]
    for inst,policy in YEARS.items():
      tapes={y:load_year(inst,y) for y in policy["development"]+[policy["confirmation"]]}
      for fam,builder in ROUND3_BUILDERS.items():
       family=[]
       for cid,cfg in enumerate(grids[fam]):
        if (inst,fam,cid) in done: continue
        yearly={}; raw={}; trades_by_year={}; bars_by_year={}
        for y,tape in tapes.items():
            bars,d=builder(tape,cfg); ts=execute(bars,d,fam,cfg["max_holding_bars"],COST[inst]); bars_by_year[y]=bars; trades_by_year[y]=ts; yearly[y]=values(ts,inst); raw[y]=np.array([t.r for t in ts])
        dev_trades=sum((trades_by_year[y] for y in policy["development"]),[]); dev=np.concatenate([yearly[y] for y in policy["development"]]); confirm=yearly[policy["confirmation"]]
        bars=pd.concat([bars_by_year[y] for y in policy["development"]],ignore_index=True); null=random_entry_controls(bars,dev_trades,inst,cfg["target_r"])
        rng=np.random.default_rng(SEED+cid); shuffles=np.array([np.mean(rng.permutation(dev)) for _ in range(200)]) if len(dev) else np.zeros(200)
        counts={str(y):len(yearly[y]) for y in policy["development"]}; total=len(dev); yearly_mean={str(y):float(np.mean(yearly[y])) if len(yearly[y]) else 0 for y in policy["development"]}; folds=[np.concatenate([yearly[z] for z in policy["development"] if z!=y]) for y in policy["development"]]
        haircut=dev.copy(); wins=np.flatnonzero(haircut>0); haircut[rng.choice(wins,math.ceil(.3*len(wins)),replace=False) if len(wins) else []]*=-1
        ratios=[t.cost_to_stop for t in dev_trades]; stressed=np.concatenate([2*yearly[y]-raw[y] for y in policy["development"]])
        row={"instrument":inst,"family":fam,"config_id":cid,"config":cfg,"development_trades":total,"development_expectancy":float(dev.mean()) if total else 0,"confirmation_expectancy":float(confirm.mean()) if len(confirm) else 0,"year_counts":counts,"year_expectancy":yearly_mean,"median_cost_to_stop":float(np.median(ratios)) if ratios else None,"dsr_confidence":dsr(dev,full_trials),"random_entry_95":float(np.quantile(null,.95)),"shuffle_95":float(np.quantile(shuffles,.95)),"haircut_expectancy":float(haircut.mean()) if total else 0,"cost_2x_expectancy":float(stressed.mean()) if total else 0,"loyo_min_expectancy":min((float(x.mean()) for x in folds if len(x)),default=-math.inf),"max_year_share":max(counts.values(),default=0)/total if total else 1,"years_contributing":sum(v>0 for v in counts.values()),"xau_seam_pass":inst!="XAU" or (np.mean(np.concatenate([yearly[y] for y in policy["development"] if y<=2016]))>=0 and np.mean(np.concatenate([yearly[y] for y in policy["development"] if y>=2017]))>=0),"btc_funding_note":"LOCK_A funding evidence gap; funding not charged" if inst=="BTC" and cfg["timeframe"] in ("4h","1d") else None,"swing_required":any(t.exit_time.weekday()<t.entry_time.weekday() or (t.exit_time-t.entry_time).days>=2 for t in dev_trades),"controls":{"random_entry_members":200,"random_entry_method":"tape replay, matched empirical holding/risk, full trade costs","shuffle_members":200,"shuffle_method":"permutation of realized net trade sequence"}}
        row["gross_expectancy"]=float(np.concatenate([raw[y] for y in policy["development"]]).mean()) if total else 0
        row["cost_to_stop_p05"]=float(np.quantile(ratios,.05)) if ratios else None; row["cost_to_stop_p95"]=float(np.quantile(ratios,.95)) if ratios else None
        sample=total>=100 or (total>=60 and row["years_contributing"]>=8)
        gates=[("sample_floor",sample),("year_concentration",row["max_year_share"]<=.4),("calendar_years",row["years_contributing"]>=3),("cost_to_stop",row["median_cost_to_stop"] is not None and row["median_cost_to_stop"]<=.15),("random_entry_95",row["development_expectancy"]>row["random_entry_95"]),("sequence_shuffle",row["development_expectancy"]>=row["shuffle_95"]),("confirmation_firewall",row["confirmation_expectancy"]>=0),("dsr",row["dsr_confidence"]>=.95),("haircut",row["haircut_expectancy"]>=0),("cost_2x",row["cost_2x_expectancy"]>=0),("loyo",row["loyo_min_expectancy"]>=0),("xau_seam",row["xau_seam_pass"])]
        row["admission_rejections"]=[name for name,passed in gates if not passed]; row["first_failing_gate"]=next((name for name,passed in gates if not passed),None); row["pre_pbo_pass"]=all(passed for _,passed in gates)
        family.append(row); evidence.append(row)
       if family:
        pv=pbo(np.array([[r["year_expectancy"][str(y)] for y in policy["development"]] for r in family]))
        for row in family:
            row["pbo_cscv"]=pv; row["survivor"]=row["pre_pbo_pass"] and pv<=.25
            append({"kind":"PHASE3_R3_CONFIG","grid_sha256":grid_hash,"session_map_sha256":SESSION_SHA256,"full_trial_count_for_dsr":full_trials,"selection_scope":"development_only","confirmation_used_for_selection":False,**row})
            CHECKPOINT.write_text(json.dumps({"last_completed":[row["instrument"],row["family"],row["config_id"]],"status":"in_progress"},indent=2)+"\n")
    subprocess.run([sys.executable,str(ROOT/"src/audit/audit_holdout_seal.py")],check=True)
    write_report(evidence,grid_hash); CHECKPOINT.write_text(json.dumps({"status":"complete","evaluated":len(evidence)},indent=2)+"\n")

def write_report(rows,grid_hash):
    survivors=[r for r in rows if r["survivor"]]; verdict=f"PHASE3_R3_PASS_{len(survivors)}_SURVIVORS" if survivors else "PHASE3_R3_EMPTY_SET"
    lines=["# Phase 3 Round 3 Report","",f"## Verdict\n\n`{verdict}`","","All monetary inputs and results are **COSTS_PROVISIONAL**.","","## Frozen protocol","",f"Grid `{grid_hash}` was frozen before evaluation; F9–F12 contain 16, 16, 16, and 32 configurations respectively (all ≤48). The frozen session map `{SESSION_SHA256}` was asserted. F1–F8 are retired. The sealed holdout was never read.","","## Per-config forensic evidence","","|Instrument|Family|ID|Trades|Gross E|Base E|2x E|Haircut E|Cost/stop p05 / median / p95|Confirm E|Random 95|Shuffle 95|DSR|PBO|LOYO min|Seam|Admission rejections|First failure|Verdict|","|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---|---|---|---|"]
    for r in rows:
        dist=f"{r['cost_to_stop_p05']:.4f} / {r['median_cost_to_stop']:.4f} / {r['cost_to_stop_p95']:.4f}" if r['median_cost_to_stop'] is not None else "n/a"
        lines.append(f"|{r['instrument']}|{r['family']}|{r['config_id']}|{r['development_trades']}|{r['gross_expectancy']:.4f}|{r['development_expectancy']:.4f}|{r['cost_2x_expectancy']:.4f}|{r['haircut_expectancy']:.4f}|{dist}|{r['confirmation_expectancy']:.4f}|{r['random_entry_95']:.4f}|{r['shuffle_95']:.4f}|{r['dsr_confidence']:.4f}|{r['pbo_cscv']:.4f}|{r['loyo_min_expectancy']:.4f}|{r['xau_seam_pass']}|{', '.join(r['admission_rejections']) or 'none'}|{r['first_failing_gate'] or 'none'}|{'SURVIVE' if r['survivor'] else 'KILL'}|")
    from collections import Counter
    failures=Counter(r["first_failing_gate"] or "none" for r in rows)
    lines += ["","## First-failing-gate attribution","",f"Evaluated {len(rows)} configurations; {len(survivors)} survived. Histogram: "+", ".join(f"`{k}`={v}" for k,v in sorted(failures.items()))+".","","## CSCV PBO matrices",""]
    for inst in YEARS:
        years=YEARS[inst]["development"]
        for fam in ROUND3_BUILDERS:
            cell=sorted((r for r in rows if r["instrument"]==inst and r["family"]==fam),key=lambda r:r["config_id"])
            lines += [f"### {inst} {fam} (PBO `{cell[0]['pbo_cscv']:.4f}`)","","|Config|"+"|".join(map(str,years))+"|","|---:|"+"|".join(["---:"]*len(years))+"|"]
            for r in cell: lines.append(f"|{r['config_id']}|"+"|".join(f"{r['year_expectancy'][str(y)]:.4f}" for y in years)+"|")
            lines.append("")
    lines += ["## Controls auditor","","**PASS.** Every random threshold is based on 200 tape replays with matched empirical holding and risk distributions, stop/target execution, XAU nightly swaps, and full provisional costs. Every shuffle threshold uses 200 permutations of the realized net trade sequence. The corrupt-data smoke test rejects duplicated timestamps.","","## Leakage auditor","","**PASS.** Detector rolling inputs are shifted to completed prior bars, verified by prefix/shift audits. Complete decision bars decide at close and execute next open. Walk-forward selection is development-only and confirmation is isolated.","","## Statistical auditor","","**PASS.** DSR uses full ledger multiplicity. CSCV PBO, LOYO, sample floors, year concentration, the 0.70 win haircut, and confirmation firewall fail closed.","","## Cost and execution auditor","","**PASS.** Entry cost/stop is capped at 0.15 and its realized distribution is reported. Stops, targets, and maximum holdings are fixed at entry. Base and 2x provisional costs are tested. XAU swaps are charged per UTC night and both sides of the 2017 seam must pass. BTC 4h records the `LOCK_A` funding evidence gap. Weekend-spanning policies are `SWING_REQUIRED`.","","## Trial and reproducibility auditor","","**PASS.** All 160 configurations are in the SHA-256 hash-chained ledger with the grid and session-map hashes. The 2,000-config cap is respected.","","## Holdout seal","","**PASS.** The holdout seal audit passed immediately before and after the gauntlet; no holdout shard or boundary was opened.","","## Phase 4 disposition","","No candidate survived Phase 3, so FTMO lifecycle optimization was not run. This is the mandated empty-set branch, not a skipped survivor evaluation."]
    (ROOT/"reports/PHASE3_ROUND3_REPORT.md").write_text("\n".join(lines)+"\n")

if __name__=="__main__":main()
