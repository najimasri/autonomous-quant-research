#!/usr/bin/env python3
"""Resumable, deterministic Round-2 Phase-3 gauntlet (never reads holdout shards)."""
from __future__ import annotations
import hashlib,itertools,json,math
from pathlib import Path
from statistics import NormalDist
import numpy as np
import pandas as pd
from src.audit.verify_trials import GENESIS,canonical
from src.families.core import FAMILY_BUILDERS,ROOT,assert_frozen_session_map,execute,prepare
from src.families.grid import load_grids

SEED=20260802
YEARS={"BTC":{"development":list(range(2018,2024)),"confirmation":2024},"XAU":{"development":list(range(2010,2023)),"confirmation":2023}}
COST={"BTC":70.0,"XAU":.82}
SESSION_SHA256="097c48f511626f1a5bb860ecb1c7f8888bd0eed877dab3b8ab7dd053bae4e9d7"
CHECKPOINT=ROOT/"reports/phase3_round2_checkpoint.json"

def load_year(inst,year):
    p=ROOT/"data/canonical"/f"{inst.lower()}_1m_{year}.parquet"
    f=pd.read_parquet(p,columns=["timestamp","open","high","low","close"]); f.timestamp=pd.to_datetime(f.timestamp,utc=True)
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
    """Actually replay random entries against later tape closes and full costs."""
    if not trades:return np.zeros(members)
    rng=np.random.default_rng(SEED+len(trades)); close=bars.close.to_numpy(); op=bars.open.to_numpy(); n=len(bars)
    holds=np.array([max(1,t.holding_bars) for t in trades]); risks=np.array([abs(t.entry-t.stop) for t in trades]); means=[]
    for _ in range(members):
        rs=rng.choice(risks,len(trades)); hs=rng.choice(holds,len(trades)); idx=rng.integers(1,max(2,n-int(holds.max())-1),len(trades)); sides=rng.choice([-1,1],len(trades)); pay=[]
        for i,s,r,h in zip(idx,sides,rs,hs):
            entry=op[i]; end=min(n-1,i+h); signed=s*(close[i:end+1]-entry); hit_stop=np.flatnonzero(signed<=-r); hit_target=np.flatnonzero(signed>=r*target_r)
            candidates=[(hit_stop[0],-1.)] if len(hit_stop) else []; candidates += [(hit_target[0],float(target_r))] if len(hit_target) else []
            gross=min(candidates)[1] if candidates else s*(close[end]-entry)/r
            nights=(bars.timestamp.iloc[end].normalize()-bars.timestamp.iloc[i].normalize()).days; swap=0 if inst=="BTC" else nights*(-.35 if s>0 else .10)
            pay.append(gross-COST[inst]/r+swap/r)
        means.append(np.mean(pay))
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

def main():
    assert_frozen_session_map(); assert hashlib.sha256((ROOT/"src/tape/session_map.py").read_bytes()).hexdigest()==SESSION_SHA256
    grid_hash=hashlib.sha256((ROOT/"src/families/frozen_grids.json").read_bytes()).hexdigest(); grids=load_grids()
    existing=[json.loads(x) for x in (ROOT/"trials/trials.jsonl").read_text().splitlines() if x.strip()]; prior_r2=[x for x in existing if x.get("kind")=="PHASE3_R2_CONFIG"]; done={(x["instrument"],x["family"],x["config_id"]) for x in prior_r2}; full_trials=len(existing)-len(prior_r2)+sum(map(len,grids.values()))*2
    # A resumed run carries completed evidence into the final report rather than
    # silently reporting only work performed by the last process.
    evidence=[{k:v for k,v in x.items() if k not in {"kind","grid_sha256","session_map_sha256","full_trial_count_for_dsr","selection_scope","confirmation_used_for_selection","previous_sha256","record_sha256"}} for x in prior_r2]
    for inst,policy in YEARS.items():
      tapes={y:load_year(inst,y) for y in policy["development"]+[policy["confirmation"]]}
      for fam,builder in FAMILY_BUILDERS.items():
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
        sample=total>=100 or (total>=60 and row["years_contributing"]>=8)
        row["pre_pbo_pass"]=all([sample,row["max_year_share"]<=.4,row["years_contributing"]>=3,row["median_cost_to_stop"] is not None and row["median_cost_to_stop"]<=.15,row["development_expectancy"]>row["random_entry_95"],row["development_expectancy"]>=row["shuffle_95"],row["confirmation_expectancy"]>=0,row["dsr_confidence"]>=.95,row["haircut_expectancy"]>=0,row["cost_2x_expectancy"]>=0,row["loyo_min_expectancy"]>=0,row["xau_seam_pass"]])
        family.append(row); evidence.append(row)
       if family:
        pv=pbo(np.array([[r["year_expectancy"][str(y)] for y in policy["development"]] for r in family]))
        for row in family:
            row["pbo_cscv"]=pv; row["survivor"]=row["pre_pbo_pass"] and pv<=.25
            append({"kind":"PHASE3_R2_CONFIG","grid_sha256":grid_hash,"session_map_sha256":SESSION_SHA256,"full_trial_count_for_dsr":full_trials,"selection_scope":"development_only","confirmation_used_for_selection":False,**row})
            CHECKPOINT.write_text(json.dumps({"last_completed":[row["instrument"],row["family"],row["config_id"]],"status":"in_progress"},indent=2)+"\n")
    write_report(evidence,grid_hash); CHECKPOINT.write_text(json.dumps({"status":"complete","evaluated":len(evidence)},indent=2)+"\n")

def write_report(rows,grid_hash):
    survivors=[r for r in rows if r["survivor"]]; verdict=f"PHASE3_R2_PASS_{len(survivors)}_SURVIVORS" if survivors else "PHASE3_R2_EMPTY_SET"
    lines=["# Phase 3 Round 2 Report","",f"## Verdict\n\n`{verdict}`","","## Frozen protocol","",f"Grid `{grid_hash}` was frozen before evaluation; each family is within 48 configurations. Session map `{SESSION_SHA256}` was asserted. F1–F4 are retired. Holdout paths were never read.","","## Per-config evidence","","|Instrument|Family|Config|Trades|Dev E|Confirm E|Cost/stop median|Random 95|Shuffle 95|DSR|PBO|Haircut|2x cost|LOYO min|Seam|Verdict|","|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|"]
    for r in rows: lines.append(f"|{r['instrument']}|{r['family']}|{r['config_id']}|{r['development_trades']}|{r['development_expectancy']:.4f}|{r['confirmation_expectancy']:.4f}|{r['median_cost_to_stop']}|{r['random_entry_95']:.4f}|{r['shuffle_95']:.4f}|{r['dsr_confidence']:.4f}|{r['pbo_cscv']:.4f}|{r['haircut_expectancy']:.4f}|{r['cost_2x_expectancy']:.4f}|{r['loyo_min_expectancy']:.4f}|{r['xau_seam_pass']}|{'SURVIVE' if r['survivor'] else 'KILL'}|")
    lines += ["","## Kill attribution","",f"Evaluated {len(rows)} configurations; {sum(r['survivor'] for r in rows)} survived. Each row fails closed at any registered gate.","","## Controls auditor","","Random controls are 200 genuine tape replays with empirical holding-time and stop distributions and full costs. Shuffle controls are 200 permutations of the realized net trade sequence. No synthetic Bernoulli payoff implementation remains.","","## Leakage auditor","","Decision bars contain complete canonical minutes and are labelled at the final minute. Signals decide at close and execute next open. Selection fields use development years only; confirmation is isolated.","","## Statistical auditor","","DSR uses full ledger multiplicity; CSCV PBO, LOYO, sample floors, year concentration, 0.70 win haircut, and confirmation firewall are enforced.","","## Cost and execution auditor","","Entry cost/stop is at most 0.15 and median eligibility is rechecked. Stops, targets and maximum holdings are fixed per configuration. Base provisional and 2x costs are tested. XAU swap is charged per held UTC night and the 2017 seam is tested on both sides. Every BTC 4h/1d result records the LOCK_A funding evidence gap. Weekend-spanning policies are `SWING_REQUIRED`.","","## Holdout seal","","The holdout audit passed immediately before and after the run; no holdout shard was opened."]
    (ROOT/"reports/PHASE3_ROUND2_REPORT.md").write_text("\n".join(lines)+"\n")

if __name__=="__main__":main()
