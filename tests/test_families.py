import hashlib
import numpy as np
import pandas as pd
from src.families import FAMILY_BUILDERS, execute
from src.families.core import EXPECTED_SESSION_SHA256, ROOT, assert_frozen_session_map
from src.families.grid import load_grids

def sample(n=4000):
    rng=np.random.default_rng(20260801); close=1000+np.cumsum(rng.normal(0,2,n))
    return pd.DataFrame({'timestamp':pd.date_range('2021-01-04',periods=n,freq='min',tz='UTC'),'open':np.r_[close[0],close[:-1]],'high':close+2,'low':close-2,'close':close})

def test_session_and_round2_grid():
    assert_frozen_session_map(); assert hashlib.sha256((ROOT/'src/tape/session_map.py').read_bytes()).hexdigest()==EXPECTED_SESSION_SHA256
    grids=load_grids(); assert set(grids)==set(FAMILY_BUILDERS)=={'F5','F6','F7','F8'}; assert all(len(x)<=48 for x in grids.values())

def test_causal_and_execution_contract():
    t=sample(); grids=load_grids()
    for family,builder in FAMILY_BUILDERS.items():
        bars,d=builder(t,grids[family][0]); prefix=t.iloc[:3000]; pb,pd_=builder(prefix,grids[family][0])
        pd.testing.assert_frame_equal(d.iloc[:len(pd_)].reset_index(drop=True),pd_.reset_index(drop=True))
        trades=execute(bars,d,family,grids[family][0]['max_holding_bars'],10)
        for x in trades:
            assert x.decision_time < x.entry_time <= x.exit_time
            assert x.holding_bars <= grids[family][0]['max_holding_bars']+1
            assert x.cost_to_stop <= .15

def test_cost_gate_rejects_all():
    t=sample(); p=load_grids()['F5'][0]; bars,d=FAMILY_BUILDERS['F5'](t,p)
    assert execute(bars,d,'F5',p['max_holding_bars'],10**9)==[]
