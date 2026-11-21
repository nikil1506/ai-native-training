# Day 12 cheat sheet: State, orchestration and human-in-the-loop

## By the end of the day you can

- Make a multi-agent run durable and resumable.
- Add risk-based human approval gates.
- Scope the capstone.

## Key concepts (this morning)

|  |  |
| --- | --- |
| 30 min | Durable state, checkpoints, resumability, idempotent side effects |
| 25 min | Orchestration choices: framework vs hand-rolled, trade-offs |
| 30 min | Approval gates, confidence thresholds, escalation; shared-artifact conflicts |
| 20 min | Long-running and asynchronous work |
| 45 min | Guided walkthrough: the facilitator live-codes the first steps of today's lab; you follow along |

## Today's lab: L13

Lab text: `docs/programme/labs/L13.md` · starter: `starter/incidents`

```
use starter/incidents/checkpoint.py
kill the run part-way, rerun with the same run id: finished steps must not repeat
```

### Hint cards

- Save state before moving on, not after.
- If a step sends something, record that it was sent so you do not send it twice.
- Make sure there is only one path to the publish step.

## Checkpoint

Capstone scoping session (1 h): choose a scenario and plan your minimum scope

## The stuck ladder

1. Re-read the task and the hint card (5 min).
2. Ask your coding assistant to **explain** the error, not to fix it.
3. Check this cheat sheet.
4. Ask a facilitator.
5. Skip to the next task, mark it, and catch up in office hours.

## Explain it back

At the debrief you will explain one thing you built in your own words.
