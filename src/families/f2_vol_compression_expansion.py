"""F2: range compression followed by close-to-close expansion."""
import pandas as pd
from .core import prepare

def decisions(tape: pd.DataFrame, p: dict) -> pd.DataFrame:
    f = prepare(tape); ret = f.close.pct_change()
    short = ret.rolling(p["short_window"]).std().shift(1)
    long = ret.rolling(p["long_window"]).std().shift(1)
    compressed = short < long * p["compression"]
    move = ret / long
    side = ((compressed & (move > p["expansion"])).astype(int) - (compressed & (move < -p["expansion"])).astype(int))
    risk = (f.high - f.low).rolling(p["long_window"]).mean().shift(1) * p["stop_atr"]
    return pd.DataFrame({"side": side, "risk_distance": risk, "target_r": p["target_r"]})
