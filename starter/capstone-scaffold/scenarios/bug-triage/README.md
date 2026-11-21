# Scenario: Bug-report triage assistant
Reads a bug report, finds likely causes in a small sample codebase (`sample_codebase/`), and **drafts a suggested fix for a person to review** (never applies it).
Reports: `bug_reports.json`. The independent reviewer checks the suggested fix against the code and the report.
