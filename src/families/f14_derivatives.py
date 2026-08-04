"""Prior-only derivatives features and registered Round-5 F14 decisions."""
from __future__ import annotations

import numpy as np
import pandas as pd

from src.families.core import assert_frozen_session_map
from src.tape.decision_bars import aggregate_decision_bars

FEATURE_NAMES = (
    "funding_level", "funding_z", "funding_streak", "oi_level", "oi_change",
    "perp_spot_basis", "liquidation_total", "liquidation_burst",
    "long_short_ratio", "long_short_z", "taker_imbalance",
)


def _series(frame: pd.DataFrame, names: tuple[str, ...], default=np.nan) -> pd.Series:
    for name in names:
        if name in frame:
            return pd.to_numeric(frame[name], errors="coerce")
    return pd.Series(default, index=frame.index, dtype=float)


def _prior_resample(frame: pd.DataFrame | None, frequency: str, sums=()) -> pd.DataFrame:
    if frame is None or frame.empty:
        return pd.DataFrame()
    data = frame.copy().sort_values("timestamp").set_index("timestamp")
    if data.index.tz is None:
        raise ValueError("derivatives timestamps must be timezone-aware")
    aggregations = {column: ("sum" if column in sums else "last") for column in data.columns}
    # Shift after completed-bar aggregation: the decision bar can see only the
    # preceding derivatives bucket, never an update from its own interval.
    return data.resample(frequency, label="right", closed="right").agg(aggregations).shift(1)


def build_derivatives_features(spot: pd.DataFrame, derivatives: dict[str, pd.DataFrame], timeframe: str) -> pd.DataFrame:
    assert_frozen_session_map()
    bars = aggregate_decision_bars(spot, timeframe).set_index("timestamp")
    frequency = {"1h": "1h", "4h": "4h"}[timeframe]
    funding = _prior_resample(derivatives.get("fundingRate"), frequency)
    perp = _prior_resample(derivatives.get("perp_klines_1m"), frequency)
    metrics = _prior_resample(derivatives.get("metrics"), frequency)
    liquidations = _prior_resample(derivatives.get("liquidationSnapshot"), frequency,
                                   sums=("quantity", "qty", "liquidation_volume"))
    index = bars.index
    result = pd.DataFrame(index=index)
    funding_level = _series(funding, ("last_funding_rate", "funding_rate")).reindex(index).ffill()
    result["funding_level"] = funding_level
    mean = funding_level.rolling(90, min_periods=30).mean()
    std = funding_level.rolling(90, min_periods=30).std()
    result["funding_z"] = (funding_level - mean) / std.replace(0, np.nan)
    sign = np.sign(funding_level).fillna(0)
    groups = sign.ne(sign.shift()).cumsum()
    result["funding_streak"] = sign * sign.groupby(groups).cumcount().add(1)
    oi = _series(metrics, ("sum_open_interest", "open_interest", "openinterest")).reindex(index).ffill()
    result["oi_level"] = oi
    result["oi_change"] = oi.pct_change(fill_method=None)
    perp_close = _series(perp, ("close",)).reindex(index)
    result["perp_spot_basis"] = perp_close / bars.close.shift(1) - 1
    liquidation = _series(liquidations, ("liquidation_volume", "quantity", "qty"), 0).reindex(index).fillna(0)
    result["liquidation_total"] = liquidation
    baseline = liquidation.rolling(90, min_periods=30).median().replace(0, np.nan)
    result["liquidation_burst"] = liquidation / baseline
    ratio = _series(metrics, ("count_long_short_ratio", "long_short_ratio", "longshortratio")).reindex(index).ffill()
    result["long_short_ratio"] = ratio
    result["long_short_z"] = (ratio-ratio.rolling(90, min_periods=30).mean()) / ratio.rolling(90, min_periods=30).std().replace(0, np.nan)
    buy = _series(metrics, ("sum_taker_long_short_vol_ratio", "taker_buy_sell_vol_ratio", "takerbuy_sellvol")).reindex(index).ffill()
    result["taker_imbalance"] = buy - 1.0
    if tuple(result.columns) != FEATURE_NAMES:
        raise RuntimeError("frozen derivatives feature order changed")
    return result.reset_index()


def assert_derivatives_shift_audit(spot, derivatives, timeframe):
    baseline = build_derivatives_features(spot, derivatives, timeframe)
    changed = {name: frame.copy() for name, frame in derivatives.items()}
    available = [frame.timestamp.iloc[len(frame)//2] for frame in changed.values() if not frame.empty]
    cutoff = max(pd.Timestamp(value) for value in available)
    for frame in changed.values():
        numeric = frame.select_dtypes(include=[np.number]).columns
        frame[numeric] = frame[numeric].astype(float)
        frame.loc[frame.timestamp >= cutoff, numeric] = 1e30
    mutated = build_derivatives_features(spot, changed, timeframe)
    admitted = baseline.timestamp <= cutoff
    pd.testing.assert_frame_equal(baseline.loc[admitted], mutated.loc[admitted])


def _atr(bars, n):
    prior_close = bars.close.shift(1)
    tr = pd.concat([(bars.high-bars.low), (bars.high-prior_close).abs(), (bars.low-prior_close).abs()], axis=1).max(axis=1)
    return tr.shift(1).rolling(n).mean()


def _result(bars, features, side, params):
    risk = _atr(bars, params["atr_window"]) * params["stop_atr"]
    decisions = pd.DataFrame({"side": side.fillna(0).astype(int), "risk_distance": risk,
                              "target_r": params["target_r"]})
    return pd.concat([bars.reset_index(drop=True), features.drop(columns="timestamp")], axis=1), decisions


def f14a(spot, derivatives, params):
    bars = aggregate_decision_bars(spot, params["timeframe"])
    features = build_derivatives_features(spot, derivatives, params["timeframe"])
    extreme = features.funding_z.abs() >= params["funding_z"]
    side = -np.sign(features.funding_z).where(extreme & (features.funding_streak.abs() >= params["min_streak"]), 0)
    return _result(bars, features, side, params)


def f14b(spot, derivatives, params):
    bars = aggregate_decision_bars(spot, params["timeframe"])
    features = build_derivatives_features(spot, derivatives, params["timeframe"])
    momentum = np.sign(bars.close.shift(1).pct_change(params["momentum_bars"]))
    burst = features.liquidation_burst >= params["burst_multiple"]
    side = momentum.where(burst, 0) * (1 if params["mode"] == "continuation" else -1)
    return _result(bars, features, side, params)


def f14c(spot, derivatives, params):
    bars = aggregate_decision_bars(spot, params["timeframe"])
    features = build_derivatives_features(spot, derivatives, params["timeframe"])
    prior = bars.close.shift(1); high = bars.high.shift(2).rolling(params["breakout_window"]).max(); low = bars.low.shift(2).rolling(params["breakout_window"]).min()
    breakout = (prior > high).astype(int) - (prior < low).astype(int)
    confirmed = features.oi_change >= params["oi_change"]
    balanced = features.long_short_z.abs() <= params["max_long_short_z"]
    return _result(bars, features, breakout.where(confirmed & balanced, 0), params)


def f14d_candidates(spot, derivatives, params):
    """Frozen A28I input matrix; fitting/selection occurs only in nested outer folds."""
    bars = aggregate_decision_bars(spot, params["timeframe"])
    features = build_derivatives_features(spot, derivatives, params["timeframe"])
    volatility = bars.close.shift(1).pct_change().rolling(params["atr_window"]).std()
    admitted = volatility >= params["volatility_floor"]
    candidates = features.loc[admitted].copy()
    candidates["outer_actions_only"] = True
    return candidates
