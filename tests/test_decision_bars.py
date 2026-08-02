import pandas as pd
import pytest
from src.tape.decision_bars import aggregate_decision_bars


def tape(n=300):
    ts=pd.date_range('2024-01-01',periods=n,freq='min',tz='UTC')
    x=pd.Series(range(n),dtype=float)
    return pd.DataFrame({'timestamp':ts,'open':x,'high':x+2,'low':x-2,'close':x+1})

@pytest.mark.parametrize(('tf','minutes'), [('1h',60),('4h',240),('1d',1440)])
def test_only_complete_bars_and_ohlc(tf,minutes):
    out=aggregate_decision_bars(tape(minutes+17),tf)
    assert len(out)==1
    assert out.iloc[0][['open','high','low','close']].tolist()==[0,minutes+1,-2,minutes]
    assert out.iloc[0].timestamp==pd.Timestamp('2024-01-01',tz='UTC')+pd.Timedelta(minutes=minutes-1)

def test_no_lookahead_prefix_invariance():
    full=aggregate_decision_bars(tape(300),'1h')
    prefix=aggregate_decision_bars(tape(180),'1h')
    pd.testing.assert_frame_equal(full.iloc[:3].reset_index(drop=True),prefix)

def test_gap_discards_interval():
    f=tape(120).drop(index=30)
    out=aggregate_decision_bars(f,'1h')
    assert len(out)==1 and out.iloc[0].timestamp.minute==59
