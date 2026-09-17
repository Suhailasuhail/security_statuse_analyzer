# Security Status Analyzer

## Purpose

This program reads security status reports for workstations. It checks the
report data and applies five security rules to classify each report.

## Report Format

Each report uses one `KEY: VALUE` entry per line. The required fields are:

```text
HOSTNAME: WS-101
ANTIVIRUS: Enabled
FIREWALL: Enabled
PATCH_STATUS: Current
FAILED_LOGINS: 1
LAST_BACKUP_DAYS: 2
```

`FAILED_LOGINS` and `LAST_BACKUP_DAYS` must contain integer values.

## The 5 Security Rules

1. `ANTIVIRUS` must be `Enabled`.
2. `FIREWALL` must be `Enabled`.
3. `PATCH_STATUS` must be `Current`.
4. `FAILED_LOGINS` values of 5 or more require attention.
5. `LAST_BACKUP_DAYS` values greater than 7 require attention.

## How to Run

From the project directory, run:

```text
python security_status_analyzer.py
```

## Status Meanings

- **OK**: The report has valid data and no security rules were triggered.
- **ATTENTION**: The report has valid data, but one or more security rules were triggered.
- **DATA ERROR**: The report is missing required data or contains invalid data.

## Testing

The analyzer was tested with these reports:

- `WS-101`: All security values meet the rules. Expected: `OK`. Actual: `OK`. **PASS**
- `WS-104`: `PATCH_STATUS` is `Outdated`. Expected: `ATTENTION`. Actual: `ATTENTION` because the patch status is not Current. **PASS**
- `WS-107`: `ANTIVIRUS` is `Disabled` and `FAILED_LOGINS` is 7. Expected: `ATTENTION`. Actual: `ATTENTION` for both triggered rules. **PASS**
- `WS-109`: `FAILED_LOGINS` is 5. Expected: `ATTENTION`. Actual: `ATTENTION` because failed logins are 5 or more. **PASS**
- `WS-130`: `FIREWALL` is missing. Expected: `DATA ERROR`. Actual: `DATA ERROR` because a required field is missing. **PASS**
- `WS-125`: `FAILED_LOGINS` is `not_available`. Expected: `DATA ERROR`. Actual: `DATA ERROR` because the value is not an integer. **PASS**

## Results

- Reports processed: 10
- OK: 2
- Attention: 5
- Data Errors: 3

## AI Assistance

Copilot helped with coding; I reviewed and tested the suggestions.
