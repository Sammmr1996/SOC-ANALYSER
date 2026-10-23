import json
from pathlib import Path

import pandas as pd
import streamlit as st

from response_manager import update_incident_status


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="SOC-ANALYSER",
    page_icon="🛡️",
    layout="wide",
)


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"


# --------------------------------------------------
# LOAD JSON DATA
# --------------------------------------------------

def load_json(filename):
    file_path = DATA_DIR / filename

    if not file_path.exists():
        st.warning(f"File not found: {filename}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        st.warning(f"{filename} must contain a JSON list.")
        return []

    except (json.JSONDecodeError, OSError) as error:
        st.error(f"Could not read {filename}: {error}")
        return []


incidents = load_json("incidents.json")
alerts = load_json("alerts.json")


# --------------------------------------------------
# DASHBOARD TITLE
# --------------------------------------------------

st.title("🛡️ SOC-ANALYSER")
st.caption(
    "Security Operations Center | Monitoring & Incident Response"
)
st.divider()


# --------------------------------------------------
# SUMMARY METRICS
# --------------------------------------------------

total_incidents = len(incidents)
total_alerts = len(alerts)

high_severity = sum(
    1
    for incident in incidents
    if str(incident.get("severity", "")).upper() == "HIGH"
)

open_incidents = sum(
    1
    for incident in incidents
    if str(incident.get("status", "")).upper() != "RESOLVED"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Incidents", total_incidents)
col2.metric("Total Alerts", total_alerts)
col3.metric("High Severity", high_severity)
col4.metric("Open Incidents", open_incidents)

st.divider()


# --------------------------------------------------
# PREPARE CHART DATA
# --------------------------------------------------

status_counts = {}

for incident in incidents:
    status = incident.get("status") or "UNKNOWN"
    status_counts[status] = status_counts.get(status, 0) + 1

severity_counts = {}

for incident in incidents:
    severity = incident.get("severity") or "UNKNOWN"
    severity_counts[severity] = severity_counts.get(severity, 0) + 1

ip_counts = {}

for incident in incidents:
    source_ip = incident.get("source_ip") or "UNKNOWN"
    ip_counts[source_ip] = ip_counts.get(source_ip, 0) + 1


# --------------------------------------------------
# SECURITY ANALYTICS
# --------------------------------------------------

st.header("📊 Security Analytics")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Incidents by Status")

    if status_counts:
        status_df = pd.DataFrame(
            list(status_counts.items()),
            columns=["Status", "Incidents"],
        )

        st.bar_chart(
            status_df,
            x="Status",
            y="Incidents",
            height=300,
        )
    else:
        st.info("No incident data available.")

with chart_col2:
    st.subheader("Incidents by Severity")

    if severity_counts:
        severity_df = pd.DataFrame(
            list(severity_counts.items()),
            columns=["Severity", "Incidents"],
        )

        st.bar_chart(
            severity_df,
            x="Severity",
            y="Incidents",
            height=300,
        )
    else:
        st.info("No incident data available.")

st.subheader("Incidents by Source IP")

if ip_counts:
    ip_df = pd.DataFrame(
        list(ip_counts.items()),
        columns=["Source IP", "Incidents"],
    )

    st.bar_chart(
        ip_df,
        x="Source IP",
        y="Incidents",
        height=300,
    )
else:
    st.info("No source IP data available.")

st.divider()


# --------------------------------------------------
# INCIDENT RECORDS
# --------------------------------------------------

st.header("📁 Incident Records")

if incidents:
    incidents_df = pd.DataFrame(incidents)

    display_incidents_df = incidents_df.astype("object")
    display_incidents_df = display_incidents_df.where(
        pd.notna(display_incidents_df),
        "N/A",
    )
    display_incidents_df = display_incidents_df.astype("string")

    st.dataframe(
        display_incidents_df,
        width="stretch",
        hide_index=True,
    )
else:
    st.info("No incidents recorded yet.")

st.divider()


# --------------------------------------------------
# SECURITY ALERTS
# --------------------------------------------------

st.header("🚨 Security Alerts")

if alerts:
    normalized_alerts = []

    for alert in alerts:
        normalized_alert = alert.copy()

        normalized_alert["detection"] = (
            alert.get("detection")
            or alert.get("alert_type")
            or "Unknown"
        )

        normalized_alert.pop("alert_type", None)
        normalized_alerts.append(normalized_alert)

    alerts_df = pd.DataFrame(normalized_alerts)

    preferred_columns = [
        "alert_id",
        "detection",
        "severity",
        "status",
        "source_ip",
        "incident_id",
        "failed_attempts",
        "mitre_attack",
    ]

    ordered_columns = [
        column
        for column in preferred_columns
        if column in alerts_df.columns
    ]

    other_columns = [
        column
        for column in alerts_df.columns
        if column not in ordered_columns
    ]

    alerts_df = alerts_df[ordered_columns + other_columns]

    if "failed_attempts" in alerts_df.columns:
        alerts_df["failed_attempts"] = pd.to_numeric(
            alerts_df["failed_attempts"],
            errors="coerce",
        ).astype("Int64")

    display_alerts_df = alerts_df.astype("object")
    display_alerts_df = display_alerts_df.where(
        pd.notna(display_alerts_df),
        "N/A",
    )
    display_alerts_df = display_alerts_df.astype("string")

    st.dataframe(
        display_alerts_df,
        width="stretch",
        hide_index=True,
    )
else:
    st.info("No security alerts recorded yet.")

st.divider()


# --------------------------------------------------
# INCIDENT INVESTIGATION AND RESPONSE
# --------------------------------------------------

st.header("🔍 Incident Investigation")

if incidents:
    incident_options = {
        (
            f"{incident.get('incident_id', 'Unknown')} | "
            f"{incident.get('detection') or 'Unknown'}"
        ): incident
        for incident in incidents
    }

    selected_incident_name = st.selectbox(
        "Select an incident to investigate",
        list(incident_options.keys()),
    )

    selected_incident = incident_options[selected_incident_name]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Incident Details")

        st.write(
            "**Incident ID:**",
            selected_incident.get("incident_id", "N/A"),
        )
        st.write(
            "**Detection:**",
            selected_incident.get("detection") or "N/A",
        )
        st.write(
            "**Severity:**",
            selected_incident.get("severity") or "N/A",
        )
        st.write(
            "**Status:**",
            selected_incident.get("status") or "N/A",
        )
        st.write(
            "**Source IP:**",
            selected_incident.get("source_ip") or "N/A",
        )
        st.write(
            "**MITRE ATT&CK:**",
            selected_incident.get("mitre_attack") or "N/A",
        )

    with col2:
        st.subheader("Recommended Response")

        response = selected_incident.get("recommended_response", [])

        if isinstance(response, list) and response:
            for step in response:
                st.write(f"- {step}")
        elif isinstance(response, str) and response:
            st.write(response)
        else:
            st.info("No recommended response available.")

    # ----------------------------------------------
    # INCIDENT STATUS MANAGEMENT
    # ----------------------------------------------

    st.divider()
    st.subheader("Incident Response Actions")

    current_status = str(
        selected_incident.get("status", "UNKNOWN")
    ).upper()

    next_status = {
        "DETECTED": "INVESTIGATING",
        "INVESTIGATING": "CONTAINED",
        "CONTAINED": "RESOLVED",
        "RESOLVED": None,
    }

    allowed_next_status = next_status.get(current_status)

    st.write(f"Current status: **{current_status}**")

    if allowed_next_status:
        st.write(f"Next status: **{allowed_next_status}**")

        if st.button(
            f"Move to {allowed_next_status}",
            key=f"advance_{selected_incident.get('incident_id', 'unknown')}",
        ):
            success = update_incident_status(
                selected_incident.get("incident_id"),
                allowed_next_status,
            )

            if success:
                st.success(
                    f"Incident status updated to {allowed_next_status}."
                )
                st.rerun()
            else:
                st.error(
                    "Status update failed. Check the incident status "
                    "and the application console."
                )
    elif current_status == "RESOLVED":
        st.success("This incident is already resolved.")
    else:
        st.warning(
            "No valid next status is configured for this incident."
        )

else:
    st.info("There are no incidents to investigate yet.")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "SOC-ANALYSER | Cybersecurity Learning & Blue Team Portfolio"
)
