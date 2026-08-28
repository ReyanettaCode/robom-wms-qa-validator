# wms-qa-validator# RobOm WMS & Robotics QA Validation Framework

Automated testing framework designed to validate Warehouse Management System (WMS) backend APIs, data tracking consistency, and autonomous robot task execution loops.

## Features
- **Contract & Schema Testing:** Validates inventory payloads against logistics specifications.
- **Negative & Boundary Testing:** Ensures graceful error handling for missing warehouse components.
- **Robotic Telemetry Validation:** Tests dispatch control loops for automated mobile robots (AMRs).
- **CI/CD Integration:** Automated execution pipeline configured via GitHub Actions.

## Running Tests Locally
```bash
pip install -r requirements.txt
pytest -v
