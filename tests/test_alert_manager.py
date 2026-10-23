
import json
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "src")
)

from alert_manager import save_alert


def test_alert_without_incident_id_does_not_block_new_alert(
    tmp_path,
    monkeypatch
):
    project_dir = tmp_path
    data_dir = project_dir / "data"
    data_dir.mkdir()

    alerts_file = data_dir / "alerts.json"

    alerts_file.write_text(
        json.dumps([
            {
                "alert_id": "ALT-001",
                "detection": "SSH Brute Force",
                "source_ip": "192.168.1.50"
            }
        ]),
        encoding="utf-8"
    )

    monkeypatch.setattr(
        "alert_manager.os.path.dirname",
        lambda path: str(project_dir)
    )

    monkeypatch.setattr(
        "alert_manager.os.path.abspath",
        lambda path: str(project_dir / "src" / "alert_manager.py")
    )

    new_alert = {
        "detection": "SSH Brute Force",
        "source_ip": "10.0.0.25"
    }

    result = save_alert(new_alert)

    assert result is True

    saved_alerts = json.loads(
        alerts_file.read_text(encoding="utf-8")
    )

    assert len(saved_alerts) == 2
    assert saved_alerts[1]["alert_id"] == "ALT-002"
