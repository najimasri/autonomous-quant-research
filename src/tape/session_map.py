"""Frozen canonical New York-clock session classifier.

All timestamps are interpreted as instants and converted with the IANA
``America/New_York`` zone.  Consequently the UTC boundaries move at US DST
transitions; callers must not replace this map with fixed UTC offsets.
"""

from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd

NEW_YORK = ZoneInfo("America/New_York")
SESSION_BOUNDARIES = (
    (3, "london"),
    (8, "new_york"),
    (17, "off_hours"),
    (18, "asia"),
)


def classify_session(timestamp: datetime | pd.Timestamp) -> str:
    """Return the canonical session for one timezone-aware instant.

    Boundaries are half-open in New York local time: Asia [18:00, 03:00),
    London [03:00, 08:00), New York [08:00, 17:00), and off-hours
    [17:00, 18:00). Naive timestamps are rejected rather than guessed.
    """
    value = pd.Timestamp(timestamp)
    if value.tzinfo is None:
        raise ValueError("session classification requires a timezone-aware timestamp")
    hour = value.tz_convert(NEW_YORK).hour
    if hour < 3:
        return "asia"
    for start, label in reversed(SESSION_BOUNDARIES):
        if hour >= start:
            return label
    raise AssertionError("unreachable")


def classify_sessions(timestamps: pd.Series | pd.DatetimeIndex) -> pd.Series:
    """Vectorized form of :func:`classify_session`, preserving input index."""
    series = pd.Series(timestamps, index=getattr(timestamps, "index", None))
    if series.dt.tz is None:
        raise ValueError("session classification requires timezone-aware timestamps")
    hours = series.dt.tz_convert(NEW_YORK).dt.hour
    labels = pd.Series("asia", index=series.index, dtype="string")
    labels[(hours >= 3) & (hours < 8)] = "london"
    labels[(hours >= 8) & (hours < 17)] = "new_york"
    labels[(hours >= 17) & (hours < 18)] = "off_hours"
    return labels
