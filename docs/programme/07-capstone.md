## Capstone

Each participant builds and presents a small multi-agent system on their own. You are not starting from nothing: the capstone **extends your own L8–L13 work** to a new scenario, using a scaffold repository that already has an orchestrator skeleton.

### Scenario options

#### Support resolution assistant

Classifies a case, finds the answer in a knowledge base with citations, drafts a reply, and hands refunds and exceptions to a person.

#### Bug-report triage assistant

Reads a bug report, finds likely causes in a small sample codebase, and drafts a suggested fix for a person to review.

#### Document compliance checker

Checks a short document against a rule list and returns findings, each with evidence.

#### Your own idea

Agree it with a facilitator at the scoping session; it must meet the same requirements.

#### Minimum requirements

- At least three agent roles, one of them an independent reviewer with its own context
- Tools with at least one guarded action
- A knowledge source with citations and a role-based access check
- Hand-offs checked against schemas, saved state, and an approval step for risky actions
- An eval of at least 15 cases with a held-out group, a threshold script, and one measured improvement
- A trace and a short cost report
- A threat model with two attacks tried and fixed
- Process evidence: a spec, a plan, review findings and a decision log

#### Scoring rubric (100)

|  |  |
| --- | --- |
| Spec and process evidence | 15 |
| System design | 15 |
| Agent quality (eval results) | 20 |
| Reliability, tracing and cost | 10 |
| Security | 10 |
| Human oversight and governance | 10 |
| Demo and explanation | 10 |
| Reflection: what you would do differently | 10 |

> **Timeline.** Scoping on Day 12 (1 h). On Day 14, a 10-minute one-to-one design check with a facilitator in the morning and an eval and trace review at 13:30. On Day 15, finish and present a 7-minute demo. Submit your repository, eval report, cost report, threat model and decision log.
