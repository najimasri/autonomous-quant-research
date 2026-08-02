"""Pre-registered, causal Round-3 confluence families F9--F12."""
from __future__ import annotations
import numpy as np
import pandas as pd
from src.families.core import assert_frozen_session_map
from src.tape.decision_bars import aggregate_decision_bars
from src.tape.session_map import classify_sessions

def _features(tape: pd.DataFrame, p: dict) -> pd.DataFrame:
    """Build detector inputs exclusively from completed bars before decision."""
    assert_frozen_session_map(); f=aggregate_decision_bars(tape,p["timeframe"])
    prior=f.close.shift(1); prev=f.close.shift(2); n=p.get("lookback",12)
    tr=pd.concat([f.high.shift(1)-f.low.shift(1),(f.high.shift(1)-prev).abs(),(f.low.shift(1)-prev).abs()],axis=1).max(axis=1)
    f["atr"]=tr.rolling(n).mean(); f["momentum"]=np.sign(prior-f.close.shift(n+1)).fillna(0)
    ret=prior.pct_change(); short=ret.rolling(p.get("vol_short",6)).std(); long=ret.rolling(p.get("vol_long",24)).std()
    f["compressed"]=short<long*p.get("compression",.8); f["vol_ok"]=short>=long*p.get("vol_floor",.5)
    high=f.high.shift(1).rolling(n).max(); low=f.low.shift(1).rolling(n).min()
    f["range_side"]=np.sign(prior-(high+low)/2).fillna(0)
    mean=f.close.shift(2).rolling(n).mean(); std=f.close.shift(2).rolling(n).std(); f["z"]=(prior-mean)/std
    f["break_side"]=(prior>high.shift(1)).astype(int)-(prior<low.shift(1)).astype(int)
    trend_n=p.get("trend_lookback",24); f["trend"]=np.sign(prior-f.close.shift(trend_n+1)).fillna(0)
    f["session"]=classify_sessions(f.timestamp); f["weekday"]=f.timestamp.dt.weekday
    if "volume" in f:
        volume=f.volume.shift(1); f["volume_regime"]=volume>volume.rolling(n).median()
    else: f["volume_regime"]=False
    return f

def _result(f,side,p):
    return f,pd.DataFrame({"side":side.fillna(0).astype(int),"risk_distance":f.atr*p["stop_atr"],"target_r":p["target_r"]})

def f9(tape,p):
    f=_features(tape,p); votes=[f.momentum,f.range_side,-np.sign(f.z).fillna(0),f.break_side]
    if "volume" in f: votes.append(f.momentum.where(f.volume_regime,0))
    matrix=pd.concat(votes,axis=1); pos=(matrix>0).sum(axis=1); neg=(matrix<0).sum(axis=1)
    side=(pos>=p["k"]).astype(int)-(neg>=p["k"]).astype(int)
    if p["session_filter"]=="active": side=side.where(f.session.isin(["london","new_york"]),0)
    return _result(f,side,p)

def f10(tape,p):
    f=_features(tape,p); side=f.break_side.where((f.break_side==f.trend)&f.vol_ok,0)
    return _result(f,side,p)

def f11(tape,p):
    f=_features(tape,p); side=(f.z < -p["z_entry"]).astype(int)-(f.z > p["z_entry"]).astype(int)
    boundary=f.session.ne(f.session.shift(1)); allowed=(side==f.trend)|(boundary if p["allow_boundary"] else False)
    return _result(f,side.where(allowed,0),p)

def f12(tape,p):
    f=_features(tape,p); base=f.momentum if p["mode"]=="momentum" else -np.sign(f.z).fillna(0)
    allowed=f.weekday.isin([5,6,0]) if "volume" in f else f.session.isin(["london","new_york"])
    return _result(f,base.where(allowed if p["calendar"]=="focused" else ~allowed,0),p)
