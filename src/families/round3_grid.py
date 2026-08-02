"""Load the immutable Round-3 parameter grids."""
import hashlib,itertools,json
from pathlib import Path
PATH=Path(__file__).with_name("round3_grids.json"); HASH_PATH=Path(__file__).with_name("round3_grids.sha256")
def load_round3_grids():
    if hashlib.sha256(PATH.read_bytes()).hexdigest()!=HASH_PATH.read_text().split()[0]: raise RuntimeError("Round-3 grid differs from its pre-evaluation hash")
    result={}
    for family,axes in json.loads(PATH.read_text()).items():
        keys=list(axes); result[family]=[dict(zip(keys,v)) for v in itertools.product(*(axes[k] for k in keys))]
        if len(result[family])>48: raise RuntimeError(f"{family} exceeds 48-combination budget")
    return result
