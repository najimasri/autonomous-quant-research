"""Registered F13 causal-ML pipeline: frozen features, outer predictions only."""
from __future__ import annotations

import gc
import hashlib
import itertools
import json
import pickle
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from .core import execute, prepare

HERE = Path(__file__).resolve().parent
FEATURE_PATH = HERE / "f13_features.json"
GRID_PATH = HERE / "f13_grid.json"


def _verified_json(path: Path) -> dict:
    expected = path.with_suffix(".sha256").read_text().split()[0]
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        raise RuntimeError(f"frozen registration hash mismatch for {path.name}: {actual}")
    return json.loads(path.read_text())


def feature_names(instrument: str) -> tuple[str, ...]:
    registration = _verified_json(FEATURE_PATH)
    names = registration["base"] + (registration["btc_only"] if instrument.upper() == "BTC" else [])
    return tuple(names)


def feature_hash(instrument: str) -> str:
    payload = json.dumps(feature_names(instrument), separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def registered_grid() -> list[dict]:
    axes = _verified_json(GRID_PATH)
    keys = list(axes)
    grid = [dict(zip(keys, values)) for values in itertools.product(*(axes[k] for k in keys))]
    if len(grid) != 48:
        raise RuntimeError(f"F13 registration must contain exactly 48 combinations, got {len(grid)}")
    return grid


def build_features(tape: pd.DataFrame, instrument: str) -> pd.DataFrame:
    """Build only lagged inputs; row i never consumes OHLCV from row i or later."""
    frame = prepare(tape)
    p = frame.shift(1)
    close = p.close
    ret = close.pct_change()
    true_range = pd.concat([(p.high-p.low), (p.high-close.shift()), (p.low-close.shift()).abs()], axis=1).max(axis=1)
    atr = true_range.rolling(14, min_periods=14).mean()
    day_low = p.low.rolling(24, min_periods=24).min(); day_high = p.high.rolling(24, min_periods=24).max()
    week_low = p.low.rolling(24*7, min_periods=24*7).min(); week_high = p.high.rolling(24*7, min_periods=24*7).max()
    mean24 = close.rolling(24, min_periods=24).mean(); std24 = close.rolling(24, min_periods=24).std()
    ts = frame.timestamp.dt
    out = pd.DataFrame(index=frame.index)
    out["ret_1"] = ret; out["ret_3"] = close.pct_change(3); out["ret_12"] = close.pct_change(12)
    out["momentum_6"] = close/close.shift(6)-1; out["momentum_24"] = close/close.shift(24)-1
    out["atr_14"] = atr; out["atr_to_close"] = atr/close
    out["vol_12"] = ret.rolling(12, min_periods=12).std(); out["vol_48"] = ret.rolling(48, min_periods=48).std()
    out["compression"] = out.vol_12/out.vol_48
    out["day_position"] = (close-day_low)/(day_high-day_low)
    out["week_position"] = (close-week_low)/(week_high-week_low)
    out["stretch_z"] = (close-mean24)/std24
    out["hour_sin"] = np.sin(2*np.pi*ts.hour/24); out["hour_cos"] = np.cos(2*np.pi*ts.hour/24)
    out["dow_sin"] = np.sin(2*np.pi*ts.dayofweek/7); out["dow_cos"] = np.cos(2*np.pi*ts.dayofweek/7)
    if instrument.upper() == "BTC":
        if "volume" not in p:
            raise ValueError("BTC feature registration requires volume")
        vmean = p.volume.rolling(48, min_periods=48).mean(); vstd = p.volume.rolling(48, min_periods=48).std()
        out["volume_z"] = (p.volume-vmean)/vstd; out["volume_ratio"] = p.volume/vmean
    # Tree estimators consume float32 internally.  Converting once here avoids
    # retaining a second float64 feature matrix during every outer fold.
    return out.loc[:, feature_names(instrument)].replace(
        [np.inf, -np.inf], np.nan
    ).astype(np.float32)


def assert_shift_audit(tape: pd.DataFrame, instrument: str) -> None:
    """Mutate the terminal current bar and prove all observable features unchanged."""
    baseline = build_features(tape, instrument)
    mutable = [c for c in ("open", "high", "low", "close", "volume") if c in tape]
    for column in mutable:
        changed = tape.copy()
        changed.loc[changed.index[-1], column] = changed.loc[changed.index[-1], column] * 1.37 + 7
        candidate = build_features(changed, instrument)
        pd.testing.assert_frame_equal(baseline, candidate, check_names=True)


def generate_candidates(tape: pd.DataFrame, atr_multiple: float, volatility_floor: float,
                        provisional_round_trip_cost: float) -> pd.DataFrame:
    """Mechanically admit both directions only through registered volatility/cost gates."""
    frame = prepare(tape); p = frame.shift(1)
    tr = pd.concat([(p.high-p.low), (p.high-p.close.shift()).abs(), (p.low-p.close.shift()).abs()], axis=1).max(axis=1)
    atr = tr.rolling(14, min_periods=14).mean(); risk = atr_multiple * atr
    admitted = (atr/p.close >= volatility_floor) & (provisional_round_trip_cost/risk <= .15)
    base = pd.DataFrame({"bar_index": frame.index[admitted], "risk_distance": risk[admitted]})
    return pd.concat([base.assign(side=1), base.assign(side=-1)], ignore_index=True).sort_values(["bar_index", "side"])


@dataclass(frozen=True)
class OuterPrediction:
    config_id: str
    train_through_year: int
    outer_year: int
    row_index: int
    side: int
    score: float
    model_sha256: str
    feature_sha256: str
    outer_held_out: bool = True


def _model(config: dict):
    from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
    common = dict(n_estimators=config["n_estimators"], max_depth=config["max_depth"],
                  min_samples_leaf=config["min_samples_leaf"], random_state=config["seed"])
    return RandomForestRegressor(**common, n_jobs=1) if config["model"] == "random_forest" else GradientBoostingRegressor(**common)


def walk_forward_outer(features: pd.DataFrame, candidates: pd.DataFrame, target: pd.Series,
                       timestamps: pd.Series, config: dict, instrument: str) -> list[OuterPrediction]:
    """Fit through year t and emit year t+1 predictions; never emit development scores."""
    config_id = hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest()[:16]
    rows = pd.Index(candidates.bar_index.astype(int).unique()); years = pd.to_datetime(timestamps).dt.year
    usable = features.loc[rows].notna().all(axis=1) & target.loc[rows].notna()
    valid = rows[usable.to_numpy()]
    outputs: list[OuterPrediction] = []
    unique_years = sorted(years.loc[valid].unique())
    for outer_year in unique_years[1:]:
        train_rows = valid[years.loc[valid].to_numpy() < outer_year]
        test_rows = valid[years.loc[valid].to_numpy() == outer_year]
        if not len(train_rows) or not len(test_rows):
            continue
        # Construct only the current fold's matrices and explicitly discard them
        # before advancing.  This bounds XAU's expanding-window peak RSS.
        train_x = features.loc[train_rows]
        train_y = target.loc[train_rows].to_numpy(copy=False)
        model = _model(config); model.fit(train_x, train_y)
        model_sha = hashlib.sha256(pickle.dumps(model, protocol=5)).hexdigest()
        # Prediction is chunked so sklearn never materializes a second full outer
        # matrix.  The output vector is compact and required for execution.
        scores = np.empty(len(test_rows), dtype=np.float64)
        for start in range(0, len(test_rows), 16_384):
            stop = min(start + 16_384, len(test_rows))
            scores[start:stop] = model.predict(features.loc[test_rows[start:stop]])
        sides_by_row = candidates[candidates.bar_index.isin(test_rows)].groupby("bar_index").side.apply(list)
        for row, score in zip(test_rows, scores):
            for side in sides_by_row.loc[row]:
                outputs.append(OuterPrediction(config_id, outer_year-1, outer_year, int(row), int(side),
                                               float(score*side), model_sha, feature_hash(instrument)))
        del model, train_x, train_y, scores
        gc.collect()
    return outputs


def execute_outer(tape: pd.DataFrame, predictions: Iterable[OuterPrediction], config: dict,
                  candidates: pd.DataFrame, provisional_round_trip_cost: float,
                  max_holding_bars: int):
    """Wire GO scores into the existing next-open ATR execution contract."""
    predictions = list(predictions)
    if any(not p.outer_held_out for p in predictions):
        raise ValueError("economics wiring rejects non-outer predictions")
    selected = [p for p in predictions if p.score >= config["go_threshold"]]
    best = {}
    for p in selected:
        if p.row_index not in best or p.score > best[p.row_index].score:
            best[p.row_index] = p
    by_row = candidates.drop_duplicates("bar_index").set_index("bar_index").risk_distance
    decisions = pd.DataFrame(index=tape.index, columns=["side", "risk_distance", "target_r"], dtype=float)
    for row, p in best.items():
        decisions.loc[row] = [p.side, by_row.loc[row], config["target_r"]]
    decisions.side = decisions.side.fillna(0)
    return execute(tape, decisions, "F13_causal_ml", max_holding_bars, provisional_round_trip_cost)
