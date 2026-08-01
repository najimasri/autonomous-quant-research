"""F3: multi-bar close momentum admitted only in named NY sessions."""
import pandas as pd
from .core import prepare

def decisions(tape: pd.DataFrame, p: dict) -> pd.DataFrame:
    f = prepare(tape)
    momentum = f.close / f.close.shift(p["lookback"]) - 1
    active = f.session.isin(p["sessions"])
    side = ((active & (momentum > p["threshold"])).astype(int) - (active & (momentum < -p["threshold"])).astype(int))
    risk = (f.high - f.low).rolling(p["risk_window"]).mean().shift(1) * p["stop_atr"]
    return pd.DataFrame({"side": side, "risk_distance": risk, "target_r": p["target_r"]})
