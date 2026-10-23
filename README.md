# SOC-ANALYSER

A Python-based Security Operations Center (SOC) analysis project designed to detect SSH brute-force activity, generate security alerts, manage incidents, and demonstrate a basic incident response workflow.

## Overview

SOC-ANALYSER is a defensive cybersecurity learning project that simulates selected SOC analyst tasks using sample authentication logs.

The project analyzes failed SSH login attempts, identifies suspicious source IP addresses, generates alerts, records incidents, and provides a Streamlit dashboard for monitoring security events.

## Features

- **Log Analysis:** Parses authentication logs to identify repeated failed SSH login attempts.
- **Brute-Force Detection:** Detects suspicious activity when a source IP reaches the configured threshold.
- **Alert Management:** Creates and stores security alerts in JSON format.
- **Incident Management:** Records incidents with severity, status, source IP, and detection details.
- **Incident Response Workflow:** Supports incident status transitions from detection to resolution.
- **Security Dashboard:** Displays summary metrics, incident charts, alert records, and investigation details.
- **Automated Tests:** Uses pytest to validate core detection, alert management, incident management, and response workflow behavior.

## Technologies

- Python
- Streamlit
- Pandas
- JSON
- Pytest
- MITRE ATT&CK technique [T1110: Brute Force](https://attack.mitre.org/techniques/T1110/)

## Project Structure

```text
SOC-ANALYSER/
├── data/
│   ├── alerts.json
│   ├── incidents.json
│   └── auth.log
├── src/
│   ├── alert_manager.py
│   ├── dashboard.py
│   ├── incident_manager.py
│   ├── log_analyse.py
│   ├── response_manager.py
│   └── soc_workflow.py
├── tests/
│   ├── __init__.py
│   ├── test_alert_manager.py
│   ├── test_incident_manager.py
│   ├── test_log_analyse.py
│   ├── test_response_manager.py
│   └── test_soc_workflow.py
├── .gitignore
└── README.md
```

## Requirements

- Python 3.12 or a compatible Python version
- pip

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd SOC-ANALYSER
```

Install the dependencies:

```bash
python -m pip install streamlit pandas pytest
```

## Run the Dashboard

From the project root directory, run:

```bash
python -m streamlit run src/dashboard.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

## Run the Tests

Run the automated test suite:

```bash
python -m pytest -v
```

The current test suite contains eight tests covering core detection and response functionality.

## Detection Scenario

The sample authentication log includes repeated failed SSH login attempts. The detection logic identifies a source IP address that reaches the configured threshold of five failed attempts.

The detection is associated with MITRE ATT&CK technique **T1110: Brute Force**.

## Scope and Limitations

This project is a learning-oriented prototype that uses sample authentication logs and local JSON files. It is not a production SIEM and does not provide live enterprise monitoring, centralized log collection, or automatic network-level blocking.

## Disclaimer

This project is intended for defensive cybersecurity education and portfolio demonstration. All testing should be performed in authorized environments using sample or permitted data.

## Author

Cybersecurity portfolio project focused on SOC analysis, threat detection, alert management, and incident response.