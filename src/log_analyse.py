import re
import json
import os

from alert_manager import save_alert
from soc_workflow import start_response


def save_incident(incident):

    project_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    incident_file = os.path.join(
        project_dir,
        "data",
        "incidents.json"
    )

    if os.path.exists(incident_file):

        with open(
            incident_file,
            "r",
            encoding="utf-8"
        ) as file:

            try:
                incidents = json.load(file)

                if not isinstance(incidents, list):
                    incidents = []

            except json.JSONDecodeError:
                incidents = []

    else:
        incidents = []

    # Check for an existing unresolved incident
    for existing_incident in incidents:

        if (
            existing_incident.get("detection")
            == incident.get("detection")
            and
            existing_incident.get("source_ip")
            == incident.get("source_ip")
            and
            existing_incident.get("status")
            != "RESOLVED"
        ):

            incident["incident_id"] = (
                existing_incident.get("incident_id")
            )

            print("\nIncident already exists.")

            print(
                f"Existing Incident ID: "
                f"{incident['incident_id']}"
            )

            return False

    # Generate next Incident ID
    incident_numbers = []

    for existing_incident in incidents:

        incident_id = existing_incident.get(
            "incident_id",
            ""
        )

        match = re.match(
            r"INC-(\d+)",
            incident_id
        )

        if match:
            incident_numbers.append(
                int(match.group(1))
            )

    if incident_numbers:
        next_number = max(incident_numbers) + 1
    else:
        next_number = 1

    incident["incident_id"] = (
        f"INC-{next_number:03d}"
    )

    # Save the new incident
    incidents.append(incident)

    with open(
        incident_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            incidents,
            file,
            indent=4
        )

    print(
        f"\nNew incident saved: "
        f"{incident['incident_id']}"
    )

    return True


def display_incident(incident):

    print("\n========================================")
    print("SOC SECURITY INCIDENT")
    print("========================================")

    print(
        "Incident ID:",
        incident["incident_id"]
    )

    print(
        "Detection:",
        incident["detection"]
    )

    print(
        "Severity:",
        incident["severity"]
    )

    print(
        "Source IP:",
        incident["source_ip"]
    )

    print(
        "Failed Attempts:",
        incident["failed_attempts"]
    )

    print(
        "MITRE ATT&CK:",
        incident["mitre_attack"]
    )

    print(
        "Status:",
        incident["status"]
    )

    print("\nRecommended Response:")

    for action in incident["recommended_response"]:
        print("-", action)

    print("========================================")


def main():

    project_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    log_file = os.path.join(
        project_dir,
        "data",
        "auth.log"
    )

    with open(
        log_file,
        "r",
        encoding="utf-8"
    ) as file:

        logs = file.readlines()

    failed_attempts = 0
    source_ips = {}

    # Analyze authentication logs
    for log in logs:

        if "Failed password" in log:

            failed_attempts += 1

            match = re.search(
                r"from (\d+\.\d+\.\d+\.\d+)",
                log
            )

            if match:

                ip = match.group(1)

                source_ips[ip] = (
                    source_ips.get(ip, 0) + 1
                )

    print(
        f"Loaded {len(logs)} log entries"
    )

    print(
        f"Failed SSH login attempts: "
        f"{failed_attempts}"
    )

    print("\nSource IPs:")

    # Analyze each source IP
    for ip, count in source_ips.items():

        print(
            f"{ip}: {count} failed attempts"
        )

        # Brute-force threshold
        if count >= 5:

            incident = {

                "detection":
                    "SSH Brute Force",

                "severity":
                    "HIGH",

                "source_ip":
                    ip,

                "failed_attempts":
                    count,

                "mitre_attack":
                    "T1110 - Brute Force",

                "status":
                    "DETECTED",

                "recommended_response": [

                    "Investigate source IP",

                    "Review authentication logs",

                    "Consider blocking the source IP"
                ]
            }

            # Save incident
            is_new_incident = save_incident(
                incident
            )

            # Create alert
            alert = {

                "alert_type":
                    "SSH Brute Force",

                "severity":
                    "HIGH",

                "source_ip":
                    ip,

                "incident_id":
                    incident["incident_id"]
            }

            save_alert(alert)

            # Start response for a new incident
            if is_new_incident:

                start_response(
                    incident["incident_id"]
                )

                # Response workflow completed
                incident["status"] = "RESOLVED"

            # Display final incident
            display_incident(
                incident
            )


if __name__ == "__main__":

    main()