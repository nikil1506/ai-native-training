# Class guide: show it, then they replicate it

Everything runs locally on Ollama (default model `qwen3.5:latest`; override with `HARNESS_MODEL`,
host with `OLLAMA_HOST`). Python 3.10+, stdlib only. Warm the model first: `python -m harness route "hi"`.

Pattern per session: **Show** the working reference (commands below) -> trainees **Replicate** it
from the spec, in their own files, without reading the reference first -> compare and debrief.

| Session | Show (instructor runs) | Reference code | Replicate (trainees build) |
| --- | --- | --- | --- |
| 1 Skills | `python -m harness route "<prompt>"`; run `python -m harness skill pr-description --task "Write a PR description for v0.1.0..v0.2.0."`; show `commit-helper` misfiring | `harness/skills.py`, `.claude/skills/*` | Own skill (A pr-description, B code-review, C changelog) with SKILL.md + `scripts/` + `references/` + `evals/trigger.json` (10/10) |
| 2 Evals | `python -m harness eval --skill changelog --limit 2 --baseline`; open `runs/evals/*.json` | `harness/evals.py`, `*/evals/cases.json` | `evals/cases.json` (5 cases, code checks + rubric) and a runner that saves JSON with skill version + date |
| 3 Hooks | `python -m harness redteam`; then `python -m harness chat "delete everything with rm -rf /"` and watch it get blocked | `harness/hooks.py`, `fixtures/redteam.json` | Blocklist (A), secret scan (B), test-after-edit (C); defeat each other's hooks, add escapes to `redteam.json` |
| 4 MCP | `python -m harness mcp "What is blocking release R-1.0?"` | `harness/mcp_server.py`, `mcp_client.py` | One tool each: `search_tickets` / `get_ticket` / `list_blockers`; shared error format + pagination |
| 5 CI + stages | Show `.github/workflows/agent-pr-description.yml`; `python -m harness skill ... --max-turns 8 --out pr.md` | `harness/trace.py`, `agent.py` (budgets) | Idempotent CI job; stage contract in `docs/CONTRACT.md`; A=Plan, B=Build, C=Verify |
| 6 Capstone | `python -m harness pipeline T-202` (answer `y` at the two gates) | `harness/pipeline.py` | Wire the stages; run T-201, T-202, T-203; write the failure review |

## Teaching moments that really happen with this model
- `route "summarize this diff"` loads `code-review` (a near miss). Trigger evals score 18-20/20, with misses to fix.
- Output evals: the model grader sometimes disagrees with the code checks, and the baseline sometimes wins. Ask why.
- Ollama returns HTTP 500 when the model emits a malformed tool call. `llm.py` retries (a harness-level fix, not a prompt fix).
- The plan model forgets the `Ticket:` line, so the harness adds it in code (deterministic work belongs in code).
- The verify reviewer can raise debatable findings (e.g. variable naming), so the retry/send-back path gets exercised.

## Handy commands
    python -m unittest discover tests          # 25 offline tests, no Ollama needed
    python -m harness eval --trigger-only      # ~2.5 min, 60 routing calls
    python -m harness kill / kill --clear      # kill switch
    python scripts/check_capstone.py           # which capstone tickets are still open on main

Pipeline runs create a git worktree + branch `agent/<ticket>-<slug>` and leave artifacts in `runs/` (gitignored).
Clean up with `git worktree remove --force runs/<run>/work` and `git branch -D agent/...`.
