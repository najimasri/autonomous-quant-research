"""Registered higher-timeframe families F5--F8."""
from __future__ import annotations
import pandas as pd
from src.tape.decision_bars import aggregate_decision_bars

def _atr(f, n):
    prev=f.close.shift(1); tr=pd.concat([f.high-f.low,(f.high-prev).abs(),(f.low-prev).abs()],axis=1).max(axis=1)
    return tr.rolling(n).mean().shift(1)

def f5(tape, p):
    f=aggregate_decision_bars(tape,p["timeframe"]); hi=f.high.rolling(p["range_bars"]).max().shift(1); lo=f.low.rolling(p["range_bars"]).min().shift(1)
    side=(f.close>hi).astype(int)-(f.close<lo).astype(int)
    return f,pd.DataFrame({"side":side,"risk_distance":_atr(f,p["range_bars"])*p["stop_atr"],"target_r":p["target_r"]})

def f6(tape,p):
    f=aggregate_decision_bars(tape,p["timeframe"]); mom=f.close/f.close.shift(p["lookback"])-1
    side=(mom>0).astype(int)-(mom<0).astype(int)
    return f,pd.DataFrame({"side":side,"risk_distance":_atr(f,p["lookback"])*p["stop_atr"],"target_r":p["target_r"]})

def f7(tape,p):
    f=aggregate_decision_bars(tape,p["timeframe"]); mean=f.close.rolling(p["window"]).mean().shift(1); std=f.close.rolling(p["window"]).std().shift(1); z=(f.close-mean)/std
    return f,pd.DataFrame({"side":(z < -p["z_entry"]).astype(int)-(z > p["z_entry"]).astype(int),"risk_distance":std*p["stop_sigma"],"target_r":p["target_r"]})

def f8(tape,p):
    f=aggregate_decision_bars(tape,p["timeframe"]); ret=f.close.pct_change(); short=ret.rolling(p["short_window"]).std().shift(1); long=ret.rolling(p["long_window"]).std().shift(1); move=ret/long; compressed=short<long*p["compression"]
    side=(compressed & (move>p["expansion"])).astype(int)-(compressed & (move < -p["expansion"])).astype(int)
    return f,pd.DataFrame({"side":side,"risk_distance":_atr(f,p["long_window"])*p["stop_atr"],"target_r":p["target_r"]})
