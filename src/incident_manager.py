import sys
import os

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "src"
    )
)

from response_manager import update_incident_status


def test_update_incident_status():

    result = update_incident_status(
        "INC-001",
        "INVESTIGATING"
    )

    assert result is True


def test_invalid_incident_status():

    result = update_incident_status(
        "INC-001",
        "HELLO"
    )

    assert result is False