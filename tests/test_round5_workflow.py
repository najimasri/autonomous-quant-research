import json
from pathlib import Path
import numpy as np
import pytest
from src.validation.round5_gauntlet import json_safe, real_resimulated_controls

ROOT=Path(__file__).resolve().parents[1]

def test_workflow_has_registered_schedule_slices_failure_banking_and_audits():
    text=(ROOT/'.github/workflows/round5-gauntlet.yml').read_text()
    for required in ['cron: "0 */6 * * *"','17400','2400','round5_last_failure.log','audit_ci.py','audit_holdout_seal.py','git push']:
        assert required in text

def test_controls_are_exactly_200_real_resimulations():
    calls=[]
    def simulator(rng): calls.append(1); return rng.normal()
    values=real_resimulated_controls(simulator)
    assert len(values)==len(calls)==200
    with pytest.raises(ValueError): real_resimulated_controls(simulator,199)

def test_numpy_safe_serialization_and_checkpoint_contract():
    assert json.dumps({'x':np.int64(1),'y':np.array([2])},default=json_safe)
    checkpoint=json.loads((ROOT/'reports/phase3_round5_checkpoint.json').read_text())
    assert checkpoint['total_configs']==128 and checkpoint['verdict_written'] is False
    assert checkpoint['status']=='waiting_for_data'
