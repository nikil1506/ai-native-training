# Day 10 guided walkthrough script: Observability, cost and reliability, Week-2 checkpoint

45 minutes, live-coded; **record it** so a participant who falls behind can replay it.

## L11

**Guided start (from the lab):**

The facilitator adds tracing to a small agent live and reads one trace aloud.

**Live-code, in order:** the first one or two Tasks of the lab:

1. Add tracing using the template: one entry per model call and per tool call, with tokens and time.
2. Produce a short report: success rate, typical and slowest time, and tokens and cost per task.
3. Reduce cost: use a cheaper model for simple steps, trim the context, cap tool output length.
4. Run the L10 eval again and write a before/after comparison that includes quality.

**Run it:** `python starter/eval/trace_report.py starter/eval/traces/*.jsonl`

**Stop when:** the first TODO is done and the participants can continue alone. Show where the hint cards are.
