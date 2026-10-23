import json
import os


def load_incidents():

    project_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    incident_file = os.path.join(
        project_dir,
        "data",
        "incidents.json"
    )

    if not os.path.exists(incident_file):
        return []

    with open(
        incident_file,
        "r",
        encoding="utf-8"
    ) as file:

        try:
            incidents = json.load(file)

            if isinstance(incidents, list):
                return incidents

            return []

        except json.JSONDecodeError:
            return []


def save_incidents(incidents):

    project_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    incident_file = os.path.join(
        project_dir,
        "data",
        "incidents.json"
    )

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


def update_incident_status(incident_id, new_status):

    valid_statuses = [
        "DETECTED",
        "INVESTIGATING",
        "CONTAINED",
        "RESOLVED"
    ]

    if new_status not in valid_statuses:

        print(
            f"Invalid status: {new_status}"
        )

        return False

    incidents = load_incidents()

    for incident in incidents:

        if incident.get("incident_id") == incident_id:

            old_status = incident.get("status")

            # Define the allowed status progression
            allowed_transitions = {
                "DETECTED": "INVESTIGATING",
                "INVESTIGATING": "CONTAINED",
                "CONTAINED": "RESOLVED",
                "RESOLVED": None
            }

            expected_next_status = (
                allowed_transitions.get(old_status)
            )

            # Prevent invalid status changes
            if new_status != expected_next_status:

                print(
                    "\nInvalid status transition."
                )

                print(
                    f"Current Status: {old_status}"
                )

                print(
                    f"Requested Status: {new_status}"
                )

                if expected_next_status:

                    print(
                        f"Expected Next Status: "
                        f"{expected_next_status}"
                    )

                else:

                    print(
                        "Incident is already RESOLVED."
                    )

                return False

            # Update status
            incident["status"] = new_status

            save_incidents(incidents)

            print(
                "\n========================================"
            )

            print("INCIDENT RESPONSE")

            print(
                "========================================"
            )

            print(
                f"Incident ID: {incident_id}"
            )

            print(
                f"Previous Status: {old_status}"
            )

            print(
                f"New Status: {new_status}"
            )

            print(
                "========================================"
            )

            return True

    print(
        f"Incident not found: {incident_id}"
    )

    return False