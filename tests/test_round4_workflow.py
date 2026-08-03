"""Static contract tests for the long-running Round 4 Actions driver."""

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/round4-gauntlet.yml"


def test_round4_workflow_registers_manual_and_scheduled_triggers():
    # BaseLoader preserves YAML 1.2's literal `on` spelling when this assertion
    # runs under PyYAML's otherwise YAML-1.1-compatible parser.
    workflow = yaml.load(WORKFLOW.read_text(), Loader=yaml.BaseLoader)

    assert set(workflow["on"]) == {"workflow_dispatch", "schedule"}
    assert workflow["on"]["workflow_dispatch"] == {}
    assert workflow["on"]["schedule"] == [{"cron": "0 */6 * * *"}]


def test_round4_workflow_keeps_slicing_and_publishing():
    source = WORKFLOW.read_text()

    assert "timeout-minutes: 350" in source
    assert "compute_deadline=$((run_started + 17400))" in source
    assert "slice=$((remaining < 2400 ? remaining : 2400))" in source
    assert "while (( $(date +%s) < compute_deadline )); do" in source
    # One publication is inside the loop and another follows run-summary output.
    assert sum(line.strip() == "publish" for line in source.splitlines()) == 2
    assert "--write-run-summary" in source
