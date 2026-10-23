
import json
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "src")
)

import log_analyse


def prepare_test_environment(tmp_path, monkeypatch, attempts):
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    log_file = data_dir / "auth.log"
    log_file.write_text(
        "".join(
            f"Oct 22 10:00:00 server sshd: Failed password "
            f"for root from 192.0.2.10 port {2200 + i} ssh2\n"
            for i in range(attempts)
        ),
        encoding="utf-8"
    )

    fake_module = tmp_path / "src" / "log_analyse.py"
    fake_module.parent.mkdir()
    monkeypatch.setattr(log_analyse, "__file__", str(fake_module))

    incidents = []
    alerts = []
    responses = []

    def fake_save_incident(incident):
        incident["incident_id"] = "TEST-001"
        incidents.append(incident.copy())
        return True

    monkeypatch.setattr(log_analyse, "save_incident", fake_save_incident)
    monkeypatch.setattr(log_analyse, "save_alert", alerts.append)
    monkeypatch.setattr(log_analyse, "start_response", responses.append)
    monkeypatch.setattr(log_analyse, "display_incident", lambda incident: None)

    return incidents, alerts, responses


def test_detects_five_failed_attempts_from_same_ip(tmp_path, monkeypatch):
    incidents, alerts, responses = prepare_test_environment(
        tmp_path, monkeypatch, 5
    )

    log_analyse.main()

    assert len(incidents) == 1
    assert incidents[0]["detection"] == "SSH Brute Force"
    assert incidents[0]["source_ip"] == "192.0.2.10"
    assert incidents[0]["failed_attempts"] == 5
    assert incidents[0]["severity"] == "HIGH"
    assert len(alerts) == 1
    assert responses == ["TEST-001"]


def test_does_not_detect_only_four_failed_attempts(tmp_path, monkeypatch):
    incidents, alerts, responses = prepare_test_environment(
        tmp_path, monkeypatch, 4
    )

    log_analyse.main()

    assert incidents == []
    assert alerts == []
    assert responses == []
