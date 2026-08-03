from pathlib import Path

import yaml


WORKFLOW = Path(__file__).parents[1] / ".github/workflows/round4-gauntlet.yml"
GAUNTLET = Path(__file__).parents[1] / "src/validation/round4_gauntlet.py"
MODEL = Path(__file__).parents[1] / "src/families/f13_causal_ml.py"


def _workflow() -> dict:
    # PyYAML 1.1 interprets the unquoted key `on` as a boolean.
    document = yaml.safe_load(WORKFLOW.read_text())
    return document.get("on", document.get(True))


def test_round4_workflow_has_registered_triggers() -> None:
    triggers = _workflow()
    assert "workflow_dispatch" in triggers
    assert triggers["schedule"] == [{"cron": "0 */6 * * *"}]


def test_round4_workflow_uses_bounded_checkpoint_driven_windows() -> None:
    text = WORKFLOW.read_text()
    assert "deadline=$((SECONDS + 17400))" in text
    assert "slice=$((remaining < 2400 ? remaining : 2400))" in text
    assert '--instrument "$instrument"' in text
    assert '"$GITHUB_STEP_SUMMARY"' in text


def test_round4_workflow_banks_failures_before_propagating() -> None:
    text = WORKFLOW.read_text()
    assert "tail -n 200 /tmp/round4-compute.log" in text
    assert "reports/round4_last_failure.log.tmp" in text
    assert "if: always() && steps.state.outputs.done != 'true'" in text
    assert "Propagate compute failure" in text


def test_round4_xau_memory_bounds_are_explicit() -> None:
    gauntlet = GAUNTLET.read_text()
    model = MODEL.read_text()
    assert "astype(np.float32)" in model
    assert "16_384" in model
    assert "mmap_mode=\"r\"" in gauntlet
    assert "range(0, len(paths), 256)" in gauntlet
    assert "_PREDICTIONS.clear()" in gauntlet
