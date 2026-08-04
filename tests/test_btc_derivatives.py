import hashlib
import json
import zipfile
from datetime import date
from io import BytesIO
from pathlib import Path

import pandas as pd

from src.ingest.download_btc_derivatives import SOURCES, acquire, archive_name, periods
from src.tape.build_btc_derivatives import build


class Response:
    def __init__(self, status, payload=b""):
        self.status_code = status
        self.payload = payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(self.status_code)

    def iter_content(self, _size):
        yield self.payload


class Session:
    payloads = {}

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return None

    def get(self, url, **_kwargs):
        payload = self.payloads.get(url)
        return Response(404) if payload is None else Response(200, payload)


def zipped_csv(text):
    output = BytesIO()
    with zipfile.ZipFile(output, "w") as bundle:
        bundle.writestr("data.csv", text)
    return output.getvalue()


def test_registered_static_paths_and_closed_periods():
    assert set(SOURCES) == {"fundingRate", "perp_klines_1m", "metrics", "liquidationSnapshot"}
    assert SOURCES["perp_klines_1m"].path == "monthly/klines/BTCUSDT/1m"
    assert list(periods(SOURCES["fundingRate"], date(2020, 1, 1), date(2020, 3, 1))) == [
        date(2020, 1, 1), date(2020, 2, 1)
    ]
    assert list(periods(SOURCES["metrics"], date(2020, 9, 1), date(2020, 9, 3))) == [
        date(2020, 9, 1), date(2020, 9, 2)
    ]


def test_acquisition_verifies_published_checksum_and_records_first_date(tmp_path, monkeypatch):
    source = SOURCES["fundingRate"]
    name = archive_name(source, date(2020, 1, 1))
    payload = b"verified archive"
    url = f"https://data.binance.vision/data/futures/um/{source.path}/{name}"
    Session.payloads = {url: payload, f"{url}.CHECKSUM": f"{hashlib.sha256(payload).hexdigest()}  {name}\n".encode()}
    monkeypatch.setattr("src.ingest.download_btc_derivatives.requests.Session", Session)

    result = acquire(source, date(2020, 1, 1), date(2020, 2, 1), tmp_path)
    assert result["first_available_date"] == "2020-01-01"
    assert result["archives"][name]["checksum_published"] is True
    assert result["archives"][name]["sha256"] == hashlib.sha256(payload).hexdigest()


def test_builder_writes_compact_year_shard_and_provenance(tmp_path, monkeypatch):
    raw, output = tmp_path / "raw", tmp_path / "out"
    source_dir = raw / "fundingRate"
    source_dir.mkdir(parents=True)
    name = "BTCUSDT-fundingRate-2020-01.zip"
    (source_dir / name).write_bytes(zipped_csv("calc_time,last_funding_rate\n1577836800000,0.001\n"))
    (raw / "acquisition_manifest.json").write_text(json.dumps({
        "fundingRate": {"availability_status": "AVAILABLE", "first_available_archive": name, "first_available_date": "2020-01-01", "archives": {name: {}}}
    }))
    monkeypatch.setattr("src.tape.build_btc_derivatives.ROOT", tmp_path)
    manifest = tmp_path / "manifest.json"

    result = build(raw, output, manifest)
    shard = output / "btc_fundingRate_2020.parquet"
    assert shard.is_file()
    assert pd.read_parquet(shard).iloc[0].last_funding_rate == 0.001
    metadata = next(iter(result["sources"]["fundingRate"]["shards"].values()))
    assert metadata["rows"] == 1 and len(metadata["sha256"]) == 64
