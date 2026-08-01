"""F4: fade closes stretched from a prior-only rolling distribution."""
import pandas as pd
from .core import prepare

def decisions(tape: pd.DataFrame, p: dict) -> pd.DataFrame:
    f = prepare(tape)
    mean = f.close.rolling(p["window"]).mean().shift(1); std = f.close.rolling(p["window"]).std().shift(1)
    z = (f.close - mean) / std
    side = (z < -p["z_entry"]).astype(int) - (z > p["z_entry"]).astype(int)
    return pd.DataFrame({"side": side, "risk_distance": std * p["stop_sigma"], "target_r": p["target_r"]})
