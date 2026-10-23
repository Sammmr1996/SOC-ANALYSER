from response_manager import update_incident_status


def start_response(incident_id):

    print("\nStarting SOC response workflow...")

    # Step 1: Move incident to INVESTIGATING
    update_incident_status(
        incident_id,
        "INVESTIGATING"
    )

    # Step 2: Move incident to CONTAINED
    update_incident_status(
        incident_id,
        "CONTAINED"
    )

    # Step 3: Move incident to RESOLVED
    update_incident_status(
        incident_id,
        "RESOLVED"
    )

    print("\nSOC response workflow completed.")


if __name__ == "__main__":

    start_response("INC-002")