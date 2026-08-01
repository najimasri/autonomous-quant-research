import argparse
import importlib.util
import lzma
import sys
import tempfile
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
ticks = load("download_xau_ticks", "src/ingest/download_xau_ticks.py")


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
        packed = tape.RECORD.pack(60, 1000, 2000, 500, 2500, 12.0)
        self.assertEqual(len(packed), 24)
        self.assertEqual(tape.RECORD.unpack(packed)[0], 60)

    def test_candle_decoder_scales_integer_prices(self):
        packed = tape.RECORD.pack(60, 1234567, 1234570, 1234500, 1234600, 12.5)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "data/raw/xau/2010/00/04/BID_candles_min_1.bi5"
            path.parent.mkdir(parents=True)
            path.write_bytes(lzma.compress(packed))
            original_root, tape.ROOT = tape.ROOT, root
            try:
                row = tape.decode(path).iloc[0]
            finally:
                tape.ROOT = original_root
        self.assertEqual(row.open, 1234.567)
        self.assertEqual(row.close, 1234.57)

    def test_tick_sample_paths_are_zero_based_and_hourly(self):
        paths = list(ticks.relative_paths(date(2024, 3, 1)))
        self.assertEqual(paths[0], "2024/02/01/00h_ticks.bi5")
        self.assertEqual(paths[-1], "2024/02/01/23h_ticks.bi5")

    def test_sample_months_are_march_and_september(self):
        self.assertEqual([day.month for day in ticks.sample_days(2024)], [3, 9])

    def test_retry_after_seconds_and_http_date(self):
        self.assertEqual(download.retry_after_seconds("7"), 7.0)
        self.assertEqual(download.retry_after_seconds(
            "Thu, 01 Jan 1970 00:00:10 GMT",
            download.datetime(1970, 1, 1, tzinfo=download.timezone.utc)), 10.0)


if __name__ == "__main__":
    unittest.main()
