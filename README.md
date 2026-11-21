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

Run `python scripts/check_capstone.py` to see which capstone tickets are still unfixed.
