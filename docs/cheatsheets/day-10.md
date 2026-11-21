# Day 10 cheat sheet: Observability, cost and reliability, Week-2 checkpoint

## By the end of the day you can

- Trace a multi-step agent run end to end.
- Cut cost without losing quality.
- Diagnose failures from traces.

## Key concepts (this morning)

|  |  |
| --- | --- |
| 30 min | Tracing: spans for LLM and tool calls; metrics that matter (success, latency, tokens, cost per task) |
| 30 min | Cost levers: model routing, caching, context trimming, output caps |
| 25 min | Reliability: timeouts, retries, idempotency, rate limits |
| 20 min | Debugging from traces: common root causes (bad tool description, context overflow, loops) |
| 45 min | Guided walkthrough: the facilitator live-codes the first steps of today's lab; you follow along |

## Today's lab: L11

Lab text: `docs/programme/labs/L11.md` · starter: `starter/eval`

```
python starter/eval/trace_report.py starter/eval/traces/*.jsonl
re-run the L10 eval and compare quality + cost
```

### Hint cards

- Find the most expensive step first and change only that.
- Always run the eval after a cost change.
- Do not put personal data into traces.

## Checkpoint

A2 · Practical checkpoint: diagnose failing agent runs from traces (1 h)

## The stuck ladder

1. Re-read the task and the hint card (5 min).
2. Ask your coding assistant to **explain** the error, not to fix it.
3. Check this cheat sheet.
4. Ask a facilitator.
5. Skip to the next task, mark it, and catch up in office hours.

## Explain it back

At the debrief you will explain one thing you built in your own words.
