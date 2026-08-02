"""Causal decision-bar aggregation of canonical one-minute tapes."""
from __future__ import annotations

import pandas as pd

MINUTES = {"1h": 60, "4h": 240, "1d": 1440}


def aggregate_decision_bars(tape: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    """Return complete UTC-aligned OHLC bars, labelled by their final minute.

    Incomplete intervals are discarded.  Consequently every emitted OHLC value
    is known at its timestamp and appending future minutes cannot change it.
    """
    if timeframe not in MINUTES:
        raise ValueError(f"unsupported decision timeframe: {timeframe}")
    required = {"timestamp", "open", "high", "low", "close"}
    if missing := required.difference(tape.columns):
        raise ValueError(f"canonical tape missing columns: {sorted(missing)}")
    columns = ["timestamp", "open", "high", "low", "close"]
    if "volume" in tape.columns:  # real Binance volume; never XAU tick volume
        columns.append("volume")
    f = tape.loc[:, columns].copy()
    f["timestamp"] = pd.to_datetime(f.timestamp, utc=True)
    f = f.sort_values("timestamp").reset_index(drop=True)
    if f.timestamp.duplicated().any():
        raise ValueError("canonical timestamps must be unique")
    rule = f"{MINUTES[timeframe]}min"
    f["bucket"] = f.timestamp.dt.floor(rule)
    grouped = f.groupby("bucket", sort=True)
    aggregations = dict(timestamp=("timestamp", "last"), open=("open", "first"),
                        high=("high", "max"), low=("low", "min"), close=("close", "last"),
                        minute_count=("timestamp", "size"))
    if "volume" in columns:
        aggregations["volume"] = ("volume", "sum")
    out = grouped.agg(**aggregations)
    expected_last = out.index + pd.to_timedelta(MINUTES[timeframe] - 1, unit="min")
    complete = (out.minute_count == MINUTES[timeframe]) & (out.timestamp.array == expected_last.array)
    return out.loc[complete].reset_index(drop=True)
