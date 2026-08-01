import hashlib
import unittest
import numpy as np
import pandas as pd
from src.families import FAMILY_BUILDERS, execute
from src.families.core import EXPECTED_SESSION_SHA256, ROOT, assert_frozen_session_map
from src.families.grid import load_grids

class FamilyAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        n=600; rng=np.random.default_rng(20260801); close=100+np.cumsum(rng.normal(0, .25, n))
        cls.tape=pd.DataFrame({"timestamp":pd.date_range("2021-01-04",periods=n,freq="min",tz="UTC"),
          "open":np.r_[close[0],close[:-1]],"high":close+.2,"low":close-.2,"close":close})
        cls.grids=load_grids()

    def test_session_map_frozen(self):
        assert_frozen_session_map()
        self.assertEqual(hashlib.sha256((ROOT/"src/tape/session_map.py").read_bytes()).hexdigest(), EXPECTED_SESSION_SHA256)

    def test_grid_budgets(self):
        self.assertEqual(set(self.grids), set(FAMILY_BUILDERS))
        self.assertTrue(all(0 < len(x) <= 48 for x in self.grids.values()))

    def test_prefix_shift_audit(self):
        """Appending unknowable future bars cannot alter earlier admissions."""
        cut=450
        for family,builder in FAMILY_BUILDERS.items():
            full=builder(self.tape,self.grids[family][0]).iloc[:cut].reset_index(drop=True)
            prefix=builder(self.tape.iloc[:cut],self.grids[family][0]).reset_index(drop=True)
            pd.testing.assert_frame_equal(full,prefix,check_exact=False)

    def test_same_bar_outcome_never_admits_or_exits_entry(self):
        for family,builder in FAMILY_BUILDERS.items():
            decisions=builder(self.tape,self.grids[family][0]); trades=execute(self.tape,decisions,family)
            for trade in trades:
                self.assertLess(trade.decision_time,trade.entry_time)
                self.assertLessEqual(trade.entry_time,trade.exit_time)
                self.assertNotEqual(trade.stop,trade.entry); self.assertNotEqual(trade.target,trade.entry)
                expected=trade.side*(trade.exit-trade.entry)/abs(trade.entry-trade.stop)
                self.assertAlmostEqual(trade.r,expected)

if __name__ == "__main__": unittest.main()
