"""F1: break of the preceding session opening range."""
import pandas as pd
from .core import prepare

def decisions(tape: pd.DataFrame, p: dict) -> pd.DataFrame:
    f = prepare(tape)
    group = (f.session != f.session.shift()).cumsum()
    prior_high = f.high.groupby(group).transform(lambda x: x.rolling(p["range_bars"], min_periods=p["range_bars"]).max().shift(1))
    prior_low = f.low.groupby(group).transform(lambda x: x.rolling(p["range_bars"], min_periods=p["range_bars"]).min().shift(1))
    width = prior_high - prior_low
    active = f.groupby(group).cumcount().between(p["range_bars"], p["range_bars"] + p["entry_window"] - 1)
    side = ((f.close > prior_high) & active).astype(int) - ((f.close < prior_low) & active).astype(int)
    return pd.DataFrame({"side": side, "risk_distance": width * p["stop_range"], "target_r": p["target_r"]})
