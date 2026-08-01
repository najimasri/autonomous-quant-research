import argparse
import importlib.util
import sys
import unittest
from datetime import date
from pathlib import Path


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).parents[1] / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


download = load("download_xau", "src/ingest/download_xau.py")
tape = load("build_xau_tape", "src/tape/build_xau_tape.py")


class XauIngestTests(unittest.TestCase):
    def test_workers_are_hard_limited(self):
        self.assertEqual(download.worker_count("4"), 4)
        with self.assertRaises(argparse.ArgumentTypeError):
            download.worker_count("128")

    def test_batch_is_at_most_four_calendar_years(self):
        download.validate_batch(date(2010, 1, 1), date(2013, 12, 31))
        with self.assertRaises(SystemExit):
            download.validate_batch(date(2010, 1, 1), date(2014, 1, 1))

    def test_zero_based_month_and_both_sides(self):
        self.assertEqual(list(download.relative_paths(date(2024, 1, 2))), [
            "2024/00/02/BID_candles_min_1.bi5",
            "2024/00/02/ASK_candles_min_1.bi5",
        ])

    def test_candle_record_layout(self):
        packed = tape.RECORD.pack(60, 1.0, 2.0, 0.5, 2.5, 12.0)
        self.assertEqual(len(packed), 44)
        self.assertEqual(tape.RECORD.unpack(packed)[0], 60)

    def test_retry_after_seconds_and_http_date(self):
        self.assertEqual(download.retry_after_seconds("7"), 7.0)
        self.assertEqual(download.retry_after_seconds(
            "Thu, 01 Jan 1970 00:00:10 GMT",
            download.datetime(1970, 1, 1, tzinfo=download.timezone.utc)), 10.0)


if __name__ == "__main__":
    unittest.main()
