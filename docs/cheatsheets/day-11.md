# Day 11 cheat sheet: Multi-agent patterns

## By the end of the day you can

- Name the main multi-agent patterns and when each fits.
- Design typed hand-offs between agents.
- Show with data when multi-agent beats a single agent, and when it does not.

## Key concepts (this morning)

|  |  |
| --- | --- |
| 30 min | Why multi-agent: context isolation, specialisation, parallelism, independent review |
| 35 min | Patterns: orchestrator-worker, pipeline, fan-out/fan-in, critic loop, router and hand-off |
| 20 min | Costs: tokens, latency, compounding errors; when one agent wins |
| 20 min | Communication contracts: schemas for hand-offs; agent-to-agent protocols awareness |
| 45 min | Guided walkthrough: the facilitator live-codes the first steps of today's lab; you follow along |

## Today's lab: L12

Lab text: `docs/programme/labs/L12.md` · starter: `starter/incidents`

```
python starter/incidents/orchestrator.py inc-1 single
python starter/incidents/orchestrator.py inc-1 team
```

### Hint cards

- Give the reviewer the sources and the draft, but not the writer's reasoning.
- If a hand-off fails validation, print the message and the schema side by side.
- Put a limit on review rounds.

## The stuck ladder

1. Re-read the task and the hint card (5 min).
2. Ask your coding assistant to **explain** the error, not to fix it.
3. Check this cheat sheet.
4. Ask a facilitator.
5. Skip to the next task, mark it, and catch up in office hours.

## Explain it back

At the debrief you will explain one thing you built in your own words.
