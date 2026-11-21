## Instructor guide

What to prepare before the first cohort, and what can go wrong.

#### Preparation checklist

- Choose **Python** for the whole cohort and prepare every starter repository in Python: `bugfix-repo`, `orders-app`, `orders-api`, `support-agent`, `policy-corpus`, `eval`, `incidents`, `vulnerable-agent`, `sample-repo-2`, `backlog`, and the capstone scaffold.
- Starter code must run on first try. Dry-run every lab as a beginner would, on a fresh machine, and fix every `TODO` that is unclear.
- Write a hint card and a one-page cheat sheet for every day, a worktree cheat sheet (L6), a review checklist (A1) and a trace-reading guide (A2).
- Record the guided walkthroughs so a participant who falls behind can replay them.
- Create the shared API gateway with a per-participant spending cap and a usage dashboard. Pilot Days 6–13 to calibrate the cap.
- Default every lab to a smaller, cheaper model; use the stronger model only where a lab compares sizes.
- Prepare reference solutions and grading sheets with the acceptance criteria. Pre-build the flawed PR (A1) and the three traces (A2), and have a second facilitator confirm the planted problems can be found.
- Agree acceptable-use and data rules: no real customer data, no secrets in prompts, no production credentials.
- Staff at one facilitator per six participants, plus one person on environment support on Days 1–2 and Day 6.

#### Measuring success

- Self-assessment before and after: every participant rates themselves at least "can do with support" on each outcome.
- At least 80% of participants pass A1, A2 and the capstone.
- 30/60/90-day follow-up: each participant ships at least one agent-assisted change with a spec, review findings and a decision record, and adds one reusable skill or tool to a shared library.
- Where measurable: cycle time, rework and escaped defects on agent-assisted work compared with a baseline.

### Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Beginners get stuck and fall behind | Scaffolded starter code, hint cards, the stuck ladder, daily office hours and recorded walkthroughs. A short catch-up slot is built into the end of each lab block. |
| Setup problems eat Day 1 | Setup clinic before Day 1, a `make doctor` check, and a pre-built fallback environment. |
| Participants let the agent do the lab without understanding it | Explain-it-back at every debrief, mandatory written review comments, and the A1 and A2 checkpoints. |
| Tool or model changes during the course | Teach patterns, keep tool-specific steps in thin layers, pin versions, and keep a fallback model ready. |
| API outages or rate limits | Gateway with retries and a second provider configured; Days 1–3 labs designed to degrade gracefully. |
| Runaway spend | Per-participant caps, step limits in every lab, and a daily usage review. |
| The capstone is too big for one person | It extends your own earlier labs from a scaffold, with a fixed minimum scope and a one-to-one design check on Day 14. |

Starter repositories, datasets and reference solutions named in the labs need to be created before delivery; this guide specifies what each must contain.
