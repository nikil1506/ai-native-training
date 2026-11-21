# Day 7 cheat sheet: Single-agent design: planning, recovery, guardrails

## By the end of the day you can

- Pick a planning pattern and justify it.
- Enforce limits in code, not just in the prompt.
- Handle failure and ambiguity predictably.

## Key concepts (this morning)

|  |  |
| --- | --- |
| 30 min | Planning patterns: ReAct, plan-then-execute, reflection |
| 25 min | Stop conditions, step and token budgets, runaway protection |
| 25 min | Error recovery: retries, fallbacks, escalation to a human; asking clarifying questions |
| 25 min | Guardrails: input and output validation, permission tiers, short-term memory management |
| 45 min | Guided walkthrough: the facilitator live-codes the first steps of today's lab; you follow along |

## Today's lab: L8

Lab text: `docs/programme/labs/L8.md` · starter: `starter/support-agent`

```
python -m unittest discover starter/support-agent
python starter/support-agent/run_scenarios.py 3   (INJECT_FAILURES=1 for chaos)
```

### Hint cards

- Check limits inside the loop, before each model call.
- Treat a refund request as a hand-off, not a tool call.
- When a tool fails twice, escalate rather than retrying forever.

## The stuck ladder

1. Re-read the task and the hint card (5 min).
2. Ask your coding assistant to **explain** the error, not to fix it.
3. Check this cheat sheet.
4. Ask a facilitator.
5. Skip to the next task, mark it, and catch up in office hours.

## Explain it back

At the debrief you will explain one thing you built in your own words.
