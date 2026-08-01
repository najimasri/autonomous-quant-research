#!/usr/bin/env python3
"""Build the deterministic, text-only Phase 1 tape-QC tables."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import pandas as pd

from src.tape.session_map import classify_sessions

ROOT = Path(__file__).resolve().parents[2]
CANONICAL = ROOT / "data" / "canonical"
OUTPUT = ROOT / "reports" / "phase1_tables"


def write_csv(name: str, rows: list[dict]) -> None:
    path = OUTPUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def btc_census() -> None:
    maintenance = json.loads((CANONICAL / "tape_metadata_btc.json").read_text())["exchange_maintenance_gaps"]
    rows, gaps = [], []
    ts = pd.concat([pd.read_parquet(path, columns=["timestamp"])["timestamp"]
                    for path in sorted(CANONICAL.glob("btc_1m_*.parquet"))]).sort_values().reset_index(drop=True)
    delta = ts.diff().dt.total_seconds().div(60)
    all_gaps = delta[delta > 1]
    for idx, minutes in all_gaps.items():
        before, after = ts.loc[idx], ts.loc[idx - 1]
        match = next((g for g in maintenance if pd.Timestamp(g["before_utc"]) == before), None)
        gaps.append({"year": before.year, "after_utc": after.isoformat(), "before_utc": before.isoformat(),
                     "missing_minutes": int(minutes-1),
                     "classification": "exchange_maintenance" if match else "unclassified"})
    for year in range(ts.iloc[0].year, ts.iloc[-1].year + 1):
        lower = max(ts.iloc[0], pd.Timestamp(f"{year}-01-01", tz="UTC"))
        upper = min(ts.iloc[-1], pd.Timestamp(f"{year + 1}-01-01", tz="UTC") - pd.Timedelta(minutes=1))
        observed = ts[(ts >= lower) & (ts <= upper)]
        expected = int((upper-lower).total_seconds() // 60) + 1
        missing = expected - len(observed)
        year_gaps = [g for g in gaps if g["year"] == year]
        maint = [g for g in year_gaps if g["classification"] == "exchange_maintenance"]
        rows.append({"instrument": "BTCUSDT", "year": year, "observed_minutes": len(ts),
                     "coverage_start_utc": lower.isoformat(), "coverage_end_utc": upper.isoformat(),
                     "gap_events": len(year_gaps), "missing_minutes": missing,
                     "maintenance_events": len(maint),
                     "maintenance_missing_minutes": sum(g["missing_minutes"] for g in maint),
                     "unclassified_missing_minutes": missing-sum(g["missing_minutes"] for g in maint)})
        rows[-1]["observed_minutes"] = len(observed)
    write_csv("gap_census_btc.csv", rows)
    write_csv("btc_gap_windows.csv", gaps)


def xau_census_and_costs() -> None:
    census, inactive, costs = [], [], []
    for path in sorted(CANONICAL.glob("xau_1m_*.parquet")):
        year = int(path.stem.rsplit("_", 1)[1])
        frame = pd.read_parquet(path, columns=["timestamp", "tick_volume", "spread_proxy"])
        ts = frame["timestamp"].sort_values()
        start, end = ts.iloc[0].floor("D"), ts.iloc[-1].floor("D")
        calendar = pd.date_range(start, end, freq="D", tz="UTC")
        daily = frame.assign(day=frame.timestamp.dt.floor("D")).groupby("day").agg(minutes=("timestamp", "size"), tick_volume=("tick_volume", "sum"))
        weekend_days = int((calendar.dayofweek >= 5).sum())
        weekday = calendar[calendar.dayofweek < 5]
        weekday_missing = int(sum(1440-int(daily.loc[d, "minutes"]) if d in daily.index else 1440 for d in weekday))
        inactive_days = daily[(daily.tick_volume == 0) & (daily.index.dayofweek < 5)]
        census.append({"instrument": "XAUUSD", "year": year, "observed_minutes": len(frame),
                       "coverage_start_utc": ts.iloc[0].isoformat(), "coverage_end_utc": ts.iloc[-1].isoformat(),
                       "structural_weekend_days": weekend_days, "structural_weekend_minutes": weekend_days*1440,
                       "weekday_missing_minutes": weekday_missing, "inactive_weekdays": len(inactive_days)})
        inactive.extend({"year": year, "date_utc": d.date().isoformat(), "classification": "holiday_or_feed_inactive",
                         "observed_minutes": int(row.minutes), "tick_volume": float(row.tick_volume)} for d, row in inactive_days.iterrows())
        frame["session"] = classify_sessions(frame.timestamp)
        for session, values in frame.groupby("session", observed=True).spread_proxy:
            costs.append({"year": year, "session_ny_clock": session, "observations": len(values),
                          "median_spread_usd": f"{values.median():.6f}", "p95_spread_usd": f"{values.quantile(.95):.6f}",
                          "label": "CANDLE_DERIVED_APPROXIMATION"})
    write_csv("gap_census_xau.csv", census)
    write_csv("xau_inactive_weekdays.csv", inactive)
    write_csv("xau_session_spreads.csv", costs)


def main() -> int:
    btc_census()
    xau_census_and_costs()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
