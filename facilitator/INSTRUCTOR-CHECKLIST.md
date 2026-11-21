# Instructor checklist: status in this repository
(From the guide's "Preparation checklist", "Measuring success" and "Risks". ✅ = provided here; ⚠️ = must be done by you on the day.)

## Preparation
- ✅ Python for the whole cohort; every starter is Python: `bugfix-repo`, `orders-app`, `orders-api`, `support-agent`, `policy-corpus`, `eval`, `incidents`, `vulnerable-agent`, `sample-repo-2`, `backlog`, capstone scaffold (+ `l1`, `l3`, `a1-flawed-pr`, `a2-traces`), all under `starter/`.
- ✅ Starter code runs on first try: `make doctor`, and `tests/test_programme.py` checks starters fail where they should and reference solutions pass (offline labs).
- ⚠️ Dry-run every lab as a beginner on a fresh machine and fix unclear TODOs (a model-dependent step: L1, L7, L9, L10, L12 need Ollama).
- ✅ Hint card per lab (in `docs/programme/labs/`), one-page cheat sheet per day (`docs/cheatsheets/day-NN.md`), worktree cheat sheet, review checklist (A1), trace-reading guide (A2).
- ⚠️ Record the guided walkthroughs; scripts are in `facilitator/walkthroughs/day-NN.md`.
- ✅ Shared model gateway with per-participant cap and usage dashboard: `python -m gateway` (`make gateway`). ⚠️ Pilot Days 6-13 to calibrate `CAP_TOKENS`.
- ✅ Default every lab to the smaller model (`SMALL_MODEL`); the larger model (`LARGE_MODEL`) only where L1 compares sizes.
- ✅ Reference solutions: `facilitator/solutions/` (L1, L2, L3, L7, L8, L9, L10 helpers, L11 tracing, L12, L14). ✅ Grading sheets: `facilitator/grading/lab-grading-sheets.md`.
- ✅ Pre-built flawed PR (A1) and three traces (A2) with answer keys in `facilitator/answer-keys/`. ⚠️ Have a second facilitator confirm the planted problems can be found.
- ✅ Acceptable-use and data rules: `docs/prework/acceptable-use.md`.
- ⚠️ Staffing: one facilitator per six participants (max 18 per cohort), plus one environment-support person on Days 1-2 and Day 6.
- ⚠️ Not provided: L4, L5, L6, L13 reference solutions (open-ended, judged on process evidence), recorded videos, the setup-clinic session.

## Measuring success
- Self-assessment before/after: `facilitator/templates/self-assessment.md`
- At least 80% of participants pass A1, A2 and the capstone (passing = 65% overall, no checkpoint or capstone below 40%).
- 30/60/90-day follow-up: `facilitator/templates/follow-up-30-60-90.md`

## Risks and mitigations
See `docs/programme/10-instructor-guide.md` (risk table, verbatim from the guide). Repo-level mitigations: `make doctor` + fallback (`OLLAMA_HOST`), gateway retries + `FALLBACK_UPSTREAM`, per-participant caps, step limits in every lab, hint cards and cheat sheets, explain-it-back at every debrief.
