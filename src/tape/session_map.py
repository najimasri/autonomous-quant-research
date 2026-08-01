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
    (0, "asia"),
    (8, "london"),
    (13, "new_york"),
    (17, "off_hours"),
)


def classify_session(timestamp: datetime | pd.Timestamp) -> str:
    """Return the canonical session for one timezone-aware instant.

    Boundaries are half-open in New York local time: Asia [00:00, 08:00),
    London [08:00, 13:00), New York [13:00, 17:00), and off-hours
    [17:00, 24:00). Naive timestamps are rejected rather than guessed.
    """
    value = pd.Timestamp(timestamp)
    if value.tzinfo is None:
        raise ValueError("session classification requires a timezone-aware timestamp")
    hour = value.tz_convert(NEW_YORK).hour
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
    labels = pd.cut(
        hours,
        bins=[-1, 7, 12, 16, 23],
        labels=["asia", "london", "new_york", "off_hours"],
    )
    return labels.astype("string")
