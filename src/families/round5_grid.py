"""Load byte-frozen Round-5 grids and derivatives feature order."""
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).parent
GRID = ROOT / "round5_grids.json"
GRID_HASH = ROOT / "round5_grids.sha256"
FEATURES = ROOT / "round5_features.json"
FEATURE_HASH = ROOT / "round5_features.sha256"


def _verify(path, pin):
    if hashlib.sha256(path.read_bytes()).hexdigest() != pin.read_text().split()[0]:
        raise RuntimeError(f"frozen artifact differs from hash: {path.name}")


def load_round5_grids():
    _verify(GRID, GRID_HASH); _verify(FEATURES, FEATURE_HASH)
    result = {}
    for family, axes in json.loads(GRID.read_text()).items():
        keys = list(axes)
        result[family] = [dict(zip(keys, values)) for values in itertools.product(*(axes[key] for key in keys))]
        if len(result[family]) > 48:
            raise RuntimeError(f"{family} exceeds its 48-combination budget")
    return result


def load_round5_features():
    _verify(FEATURES, FEATURE_HASH)
    return tuple(json.loads(FEATURES.read_text()))
