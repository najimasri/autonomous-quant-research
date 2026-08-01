from datetime import datetime, timezone

import pandas as pd
import pytest

from src.tape.session_map import classify_session, classify_sessions


@pytest.mark.parametrize(
    ("instant", "expected"),
    [
        # 03:00 New York is 08:00 UTC immediately before spring DST.
        (datetime(2024, 3, 8, 7, 59, tzinfo=timezone.utc), "asia"),
        (datetime(2024, 3, 8, 8, 0, tzinfo=timezone.utc), "london"),
        # It is 07:00 UTC immediately after spring DST.
        (datetime(2024, 3, 11, 6, 59, tzinfo=timezone.utc), "asia"),
        (datetime(2024, 3, 11, 7, 0, tzinfo=timezone.utc), "london"),
        # The autumn transition moves the same boundary back to 08:00 UTC.
        (datetime(2024, 11, 1, 7, 0, tzinfo=timezone.utc), "london"),
        (datetime(2024, 11, 4, 7, 0, tzinfo=timezone.utc), "asia"),
        (datetime(2024, 11, 4, 8, 0, tzinfo=timezone.utc), "london"),
    ],
)
def test_dst_aware_boundaries(instant, expected):
    assert classify_session(instant) == expected


@pytest.mark.parametrize(
    ("local_time", "expected"),
    [
        ("2024-01-15 02:59:59", "asia"),
        ("2024-01-15 03:00:00", "london"),
        ("2024-01-15 08:00:00", "new_york"),
        ("2024-01-15 17:00:00", "off_hours"),
        ("2024-01-15 18:00:00", "asia"),
    ],
)
def test_half_open_new_york_boundaries(local_time, expected):
    assert classify_session(pd.Timestamp(local_time, tz="America/New_York")) == expected


def test_vectorized_classifier_is_identical():
    values = pd.Series(pd.date_range("2024-03-11", periods=24, freq="h", tz="UTC"))
    assert classify_sessions(values).tolist() == [classify_session(x) for x in values]


def test_naive_timestamp_is_rejected():
    with pytest.raises(ValueError, match="timezone-aware"):
        classify_session(datetime(2024, 1, 1))
    with pytest.raises(ValueError, match="timezone-aware"):
        classify_sessions(pd.Series(pd.to_datetime(["2024-01-01"])))
