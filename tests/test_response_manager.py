
import json
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "src")
)

import response_manager


def test_valid_status_transition(tmp_path, monkeypatch):
    incident_file = tmp_path / "incidents.json"
    incident_file.write_text(
        json.dumps([
            {"incident_id": "TEST-001", "status": "DETECTED"}
        ]),
        encoding="utf-8"
    )

    monkeypatch.setattr(
        response_manager,
        "load_incidents",
        lambda: json.loads(incident_file.read_text(encoding="utf-8"))
    )

    monkeypatch.setattr(
        response_manager,
        "save_incidents",
        lambda incidents: incident_file.write_text(
            json.dumps(incidents),
            encoding="utf-8"
        )
    )

    result = response_manager.update_incident_status(
        "TEST-001", "INVESTIGATING"
    )

    saved_incidents = json.loads(
        incident_file.read_text(encoding="utf-8")
    )

    assert result is True
    assert saved_incidents[0]["status"] == "INVESTIGATING"


def test_invalid_status_transition(tmp_path, monkeypatch):
    incident_file = tmp_path / "incidents.json"
    incident_file.write_text(
        json.dumps([
            {"incident_id": "TEST-002", "status": "DETECTED"}
        ]),
        encoding="utf-8"
    )

    monkeypatch.setattr(
        response_manager,
        "load_incidents",
        lambda: json.loads(incident_file.read_text(encoding="utf-8"))
    )

    monkeypatch.setattr(
        response_manager,
        "save_incidents",
        lambda incidents: incident_file.write_text(
            json.dumps(incidents),
            encoding="utf-8"
        )
    )

    result = response_manager.update_incident_status(
        "TEST-002", "RESOLVED"
    )

    saved_incidents = json.loads(
        incident_file.read_text(encoding="utf-8")
    )

    assert result is False
    assert saved_incidents[0]["status"] == "DETECTED"
