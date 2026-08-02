"""Shared, close-decision/next-open execution contract for strategy families."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import pandas as pd

EXPECTED_SESSION_SHA256 = "097c48f511626f1a5bb860ecb1c7f8888bd0eed877dab3b8ab7dd053bae4e9d7"
ROOT = Path(__file__).resolve().parents[2]


def assert_frozen_session_map() -> None:
    """Refuse to use session labels unless the Phase 1 source is byte-identical."""
    path = ROOT / "src" / "tape" / "session_map.py"
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != EXPECTED_SESSION_SHA256:
        raise RuntimeError(f"frozen session map hash mismatch: {actual}")


def prepare(tape: pd.DataFrame) -> pd.DataFrame:
    required = {"timestamp", "open", "high", "low", "close"}
    if missing := required.difference(tape.columns):
        raise ValueError(f"canonical tape missing columns: {sorted(missing)}")
    frame = tape.copy().sort_values("timestamp").reset_index(drop=True)
    if frame["timestamp"].dt.tz is None:
        raise ValueError("canonical timestamps must be timezone-aware")
    if not frame["timestamp"].is_monotonic_increasing or frame["timestamp"].duplicated().any():
        raise ValueError("canonical timestamps must be unique and increasing")
    assert_frozen_session_map()
    from src.tape.session_map import classify_sessions
    frame["session"] = classify_sessions(frame["timestamp"])
    return frame


@dataclass(frozen=True)
class Trade:
    family: str
    side: int
    decision_time: pd.Timestamp
    entry_time: pd.Timestamp
    exit_time: pd.Timestamp
    entry: float
    stop: float
    target: float
    exit: float
    exit_reason: str
    r: float
    cost_to_stop: float
    holding_bars: int


def execute(tape: pd.DataFrame, decisions: pd.DataFrame, family: str,
            max_holding_bars: int = 10**9, provisional_round_trip_cost: float = 0.0) -> list[Trade]:
    """Execute signals on the next open and evaluate hard exits on later closes.

    A decision on row i can only enter at row i+1. Stop and target are fixed from
    that fill. The entry bar cannot also supply an outcome; exit evaluation starts
    at its close, which is later than its open fill.
    """
    frame = prepare(tape)
    side = decisions["side"].reindex(frame.index, fill_value=0).astype(int)
    risk = decisions["risk_distance"].reindex(frame.index)
    target_r = decisions["target_r"].reindex(frame.index)
    trades: list[Trade] = []
    position = None
    timestamps = frame.timestamp.to_numpy()
    opens = frame.open.to_numpy(); closes = frame.close.to_numpy()
    sides = side.to_numpy(); risks = risk.to_numpy(); targets = target_r.to_numpy()
    for i in range(1, len(frame)):
        timestamp = pd.Timestamp(timestamps[i])
        if position is None and sides[i - 1] in (-1, 1) and risks[i - 1] > 0:
            direction = int(sides[i - 1])
            entry = float(opens[i])
            distance = float(risks[i - 1])
            ratio = provisional_round_trip_cost / distance
            if ratio > .15:
                continue
            position = {
                "side": direction, "decision_time": pd.Timestamp(timestamps[i - 1]),
                "entry_time": timestamp, "entry": entry,
                "stop": entry - direction * distance,
                "target": entry + direction * distance * float(targets[i - 1]),
                "risk": distance, "ratio": ratio, "entry_index": i,
            }
        if position is None:
            continue
        signed = position["side"] * (float(closes[i]) - position["entry"])
        reason = "stop" if signed <= -position["risk"] else "target" if signed >= abs(position["target"] - position["entry"]) else "max_hold" if i-position["entry_index"] >= max_holding_bars else None
        if reason:
            exit_price = float(closes[i]) if reason == "max_hold" else position[reason]
            trades.append(Trade(family, position["side"], position["decision_time"], position["entry_time"], timestamp,
                                position["entry"], position["stop"], position["target"], exit_price, reason,
                                position["side"] * (exit_price - position["entry"]) / position["risk"], position["ratio"], i-position["entry_index"]+1))
            position = None
    if position is not None:
        timestamp = pd.Timestamp(timestamps[-1])
        exit_price = float(closes[-1])
        trades.append(Trade(family, position["side"], position["decision_time"], position["entry_time"], timestamp,
                            position["entry"], position["stop"], position["target"], exit_price, "slice_end",
                            position["side"] * (exit_price - position["entry"]) / position["risk"], position["ratio"], len(frame)-position["entry_index"]))
    return trades


from .round2 import f5, f6, f7, f8
FAMILY_BUILDERS: dict[str, Callable] = {"F5": f5, "F6": f6, "F7": f7, "F8": f8}
