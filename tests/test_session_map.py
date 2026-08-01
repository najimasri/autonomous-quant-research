from datetime import datetime, timezone

import pandas as pd
import pytest

from src.tape.session_map import classify_session, classify_sessions


@pytest.mark.parametrize(
    ("instant", "expected"),
    [
        # 08:00 New York is 13:00 UTC immediately before spring DST.
        (datetime(2024, 3, 8, 12, 59, tzinfo=timezone.utc), "asia"),
        (datetime(2024, 3, 8, 13, 0, tzinfo=timezone.utc), "london"),
        # It is 12:00 UTC immediately after spring DST.
        (datetime(2024, 3, 11, 11, 59, tzinfo=timezone.utc), "asia"),
        (datetime(2024, 3, 11, 12, 0, tzinfo=timezone.utc), "london"),
        # The autumn transition moves the same boundary back to 13:00 UTC.
        (datetime(2024, 11, 1, 12, 0, tzinfo=timezone.utc), "london"),
        (datetime(2024, 11, 4, 12, 0, tzinfo=timezone.utc), "asia"),
        (datetime(2024, 11, 4, 13, 0, tzinfo=timezone.utc), "london"),
    ],
)
def test_dst_aware_boundaries(instant, expected):
    assert classify_session(instant) == expected


def test_vectorized_classifier_is_identical():
    values = pd.Series(pd.to_datetime(["2024-03-11 12:00Z", "2024-03-11 17:00Z"]))
    assert classify_sessions(values).tolist() == [classify_session(x) for x in values]


def test_naive_timestamp_is_rejected():
    with pytest.raises(ValueError, match="timezone-aware"):
        classify_session(datetime(2024, 1, 1))
