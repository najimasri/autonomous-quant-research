import hashlib
import numpy as np
import pandas as pd
import pytest
from src.families import ROUND3_BUILDERS, execute
from src.families.core import EXPECTED_SESSION_SHA256, ROOT
from src.families.round3_grid import PATH, HASH_PATH, load_round3_grids
import src.families.round3 as r3

def sample(n=8000, volume=True):
    rng=np.random.default_rng(20260802); close=1000+np.cumsum(rng.normal(0,2,n))
    data={'timestamp':pd.date_range('2021-01-04',periods=n,freq='min',tz='UTC'),'open':np.r_[close[0],close[:-1]],'high':close+2,'low':close-2,'close':close}
    if volume:data['volume']=rng.integers(1,100,n)
    return pd.DataFrame(data)

def test_round3_grid_frozen_registered_and_bounded():
    grids=load_round3_grids()
    assert set(grids)==set(ROUND3_BUILDERS)=={'F9','F10','F11','F12'}
    assert all(len(v)<=48 for v in grids.values())
    assert hashlib.sha256(PATH.read_bytes()).hexdigest()==HASH_PATH.read_text().split()[0]
    assert hashlib.sha256((ROOT/'src/tape/session_map.py').read_bytes()).hexdigest()==EXPECTED_SESSION_SHA256

def test_every_detector_is_prefix_invariant_and_execution_is_next_open():
    tape=sample(); prefix=tape.iloc[:6500]; grids=load_round3_grids()
    for family,builder in ROUND3_BUILDERS.items():
        bars,decisions=builder(tape,grids[family][0]); pb,pd_=builder(prefix,grids[family][0])
        pd.testing.assert_frame_equal(decisions.iloc[:len(pd_)].reset_index(drop=True),pd_.reset_index(drop=True))
        trades=execute(bars,decisions,family,grids[family][0]['max_holding_bars'],10)
        assert all(t.decision_time<t.entry_time<=t.exit_time and t.cost_to_stop<=.15 for t in trades)

def fake_features(*_):
    ts=pd.date_range('2021-01-01',periods=4,freq='h',tz='UTC')
    return pd.DataFrame({'timestamp':ts,'close':[1]*4,'atr':[1]*4,'momentum':[1,1,-1,-1],
      'range_side':[1,-1,-1,1],'z':[-1,1,1,-1],'break_side':[0,1,-1,0],
      'volume':[1]*4,'volume_regime':[True,False,True,False], 'trend':[1,-1,-1,1],
      'vol_ok':[True,False,True,True], 'session':['london','asia','new_york','asia'],
      'weekday':[5,2,0,3]})

def test_k_of_n_vote_and_session_condition(monkeypatch):
    monkeypatch.setattr(r3,'_features',fake_features)
    p={'k':3,'session_filter':'all','stop_atr':1,'target_r':1}
    assert r3.f9(None,p)[1].side.tolist()==[1,0,-1,0]
    p['session_filter']='active'; assert r3.f9(None,p)[1].side.tolist()==[1,0,-1,0]

def test_trend_volatility_mean_reversion_and_calendar_filters(monkeypatch):
    monkeypatch.setattr(r3,'_features',fake_features); base={'stop_atr':1,'target_r':1}
    assert r3.f10(None,base)[1].side.tolist()==[0,0,-1,0]
    assert r3.f11(None,{**base,'z_entry':.5,'allow_boundary':False})[1].side.tolist()==[1,-1,-1,1]
    assert r3.f12(None,{**base,'mode':'momentum','calendar':'focused'})[1].side.tolist()==[1,0,-1,0]

def test_volume_vote_is_btc_only():
    p=load_round3_grids()['F9'][0]
    btc,_=r3.f9(sample(volume=True),p); xau,_=r3.f9(sample(volume=False),p)
    assert 'volume_regime' in btc and 'volume' not in xau
