
import json
import os
import re


def save_alert(alert):

    # Get the SOC-ANALYSER folder
    project_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    # Path to alerts.json
    alert_file = os.path.join(
        project_dir,
        "data",
        "alerts.json"
    )

    alerts = []

    # Read existing alerts
    if os.path.exists(alert_file):
        with open(
            alert_file,
            "r",
            encoding="utf-8"
        ) as file:
            try:
                alerts = json.load(file)

                if not isinstance(alerts, list):
                    alerts = []

            except json.JSONDecodeError:
                alerts = []

    # Check duplicates only when incident_id exists
    incident_id = alert.get("incident_id")

    if incident_id is not None:
        for existing_alert in alerts:
            if (
                existing_alert.get("incident_id") is not None
                and existing_alert.get("incident_id") == incident_id
            ):
                alert["alert_id"] = existing_alert.get("alert_id")

                print("\nAlert already exists.")
                print(
                    f"Existing Alert ID: {alert['alert_id']}"
                )

                return False

    # Find the highest existing alert number
    alert_numbers = []

    for existing_alert in alerts:
        alert_id = existing_alert.get("alert_id", "")

        if not isinstance(alert_id, str):
            continue

        match = re.fullmatch(
            r"ALT-(\d+)",
            alert_id
        )

        if match:
            alert_numbers.append(
                int(match.group(1))
            )

    # Generate the next Alert ID
    next_number = max(alert_numbers, default=0) + 1

    alert["alert_id"] = f"ALT-{next_number:03d}"

    # Add alert
    alerts.append(alert)

    # Save alerts
    with open(
        alert_file,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            alerts,
            file,
            indent=4
        )

    print(
        f"\nNew alert saved: {alert['alert_id']}"
    )

    return True
