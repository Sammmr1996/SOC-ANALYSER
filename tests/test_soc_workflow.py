import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "src")
)

import soc_workflow


def test_start_response_calls_statuses_in_order(monkeypatch):
    calls = []

    def fake_update_incident_status(incident_id, new_status):
        calls.append((incident_id, new_status))
        return True

    monkeypatch.setattr(
        soc_workflow,
        "update_incident_status",
        fake_update_incident_status
    )

    soc_workflow.start_response("TEST-001")

    assert calls == [
        ("TEST-001", "INVESTIGATING"),
        ("TEST-001", "CONTAINED"),
        ("TEST-001", "RESOLVED"),
    ]