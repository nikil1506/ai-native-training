# Email runbook
- If backlog alert: check consumer health, then provider status, then queue depth growth.
- Consumer restarts with `kubectl rollout restart deploy/email-consumer`.
