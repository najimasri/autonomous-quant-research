"""Load the immutable, pre-evaluation Phase 2 parameter grids."""
import hashlib
import itertools
import json
from pathlib import Path

PATH = Path(__file__).with_name("frozen_grids.json")
HASH_PATH = Path(__file__).with_name("frozen_grids.sha256")

def load_grids() -> dict[str, list[dict]]:
    actual = hashlib.sha256(PATH.read_bytes()).hexdigest()
    expected = HASH_PATH.read_text().split()[0]
    if actual != expected:
        raise RuntimeError("parameter grid is not the frozen hashed artifact")
    raw = json.loads(PATH.read_text())
    grids = {}
    for family, axes in raw.items():
        keys = list(axes)
        grids[family] = [dict(zip(keys, values)) for values in itertools.product(*(axes[k] for k in keys))]
        if len(grids[family]) > 48:
            raise RuntimeError(f"{family} exceeds its 48-combination budget")
    return grids
