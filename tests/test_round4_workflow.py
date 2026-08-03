from pathlib import Path

import yaml


WORKFLOW = Path(__file__).parents[1] / ".github/workflows/round4-gauntlet.yml"


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


def test_round4_workflow_banks_failure_diagnostics_before_failing() -> None:
    text = WORKFLOW.read_text()
    assert "tail -n 200 /tmp/round4-compute.log" in text
    assert "reports/round4_last_failure.log" in text
    assert "steps.compute.outputs.status" in text
    assert "Exit after recorded compute failure" in text
