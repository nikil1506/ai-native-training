# Capstone contract (agree on this first, Session 5)

| Artifact | Format |
| --- | --- |
| `plan.md` | First line `Ticket: T-123`, then sections `## Approach`, `## Files to touch`, `## Test plan`, `## Risks` |
| Branch | `agent/<ticket-id>-<slug>` (slug: lowercase, hyphens, max 30 chars) |
| `verify-report.json` | `{ticket, verdict: "pass"\|"fail", checks: {tests_pass, tests_untouched, review_clean}, findings: [str], pr_description: str}` |
| Trace | `runs/<ticket>-<time>/trace.jsonl`, one JSON event per line |
| Kill switch | file `runs/KILL` exists -> every agent stops at its next turn |

Machine-checked by `validate_plan`, `branch_name`, `validate_report` in `harness/pipeline.py`.
