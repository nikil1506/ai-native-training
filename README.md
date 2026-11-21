# shelfy: practice repo for the Agentic SDLC training

A tiny inventory/orders library (Python 3.10+, stdlib only). It is the sandbox for
`agentic-sdlc-training-plan.md`. Nothing here is production code.

    python -m unittest discover tests      # must stay green on main
    python -m shelfy [port]                # demo UI at http://localhost:8765

| Path | Used in |
| --- | --- |
| `shelfy/`, `tests/` | everything: the code under work |
| `fixtures/standards.md` | Session 1: review-checklist skill `references/` |
| `fixtures/pr_samples/` | Session 1: PR description skill inputs |
| `fixtures/tickets.json` | Session 4: MCP server fixture (30 tickets, blockers) |
| `capstone_tickets/` + `capstone_tests/` | Sessions 5-6: 3 tickets, each with a failing test |
| `.claude/skills/commit-helper/` | Session 1 demo: finished skill with a known failure |
| `harness/`, `docs/` | Reference agent harness (Ollama), class guide, capstone contract |
| `facilitator/` | answer keys, red-team list. **Hide from trainees** |
| `.github/workflows/agent-pr-description.yml` | Session 5 CI job template |
| branch `review-lab/seeded-bugs` | Session 1: 5 seeded bugs for the review skill |
| tags `v0.1.0`, `v0.2.0` | Session 1: changelog generator |

**Class guide: `docs/CLASS.md`** (show-then-replicate agent harness on Ollama in `harness/`).

## AI-Native Developer Programme (Beginner): 15 days, 14 labs, solo capstone
The guide `docs/programme/AI-Native-Developer-Training-Beginner.html` is fully covered by this repo (`make coverage` proves it):

| Guide section | Where it lives |
| --- | --- |
| Overview, schedule, daily syllabus, assessment, capstone, training plan, glossary, instructor guide | `docs/programme/01-...10-*.md` (generated word-for-word from the HTML by `scripts/html_to_docs.py`) |
| 14 labs (objective, starter, guided start, tasks, hints, deliverables, criteria, stretch, pitfalls) | `docs/programme/labs/L1.md` ... `L14.md` + starters in `starter/` |
| Pre-work: setup clinic, diagnostic, primer, `make doctor` | `docs/prework/`, `scripts/doctor.py`, `Makefile` |
| Support: hint cards, per-day cheat sheets, worktree sheet, stuck ladder | `docs/cheatsheets/` (generated), lab docs |
| Checkpoints A1 / A2 | `starter/a1-flawed-pr/`, `starter/a2-traces/`, `docs/cheatsheets/review-checklist.md`, `trace-reading-guide.md` |
| Capstone scaffold, requirements, rubric | `starter/capstone-scaffold/` |
| Instructor: checklist, reference solutions, grading sheets, answer keys, walkthrough scripts, gateway with spending caps | `facilitator/` (hide from trainees), `gateway/` |

Everything runs on local Ollama (`SMALL_MODEL`, `LARGE_MODEL`, `OLLAMA_HOST`, `PARTICIPANT`). Start with `make doctor`.

Run `python scripts/check_capstone.py` to see which capstone tickets are still unfixed.
