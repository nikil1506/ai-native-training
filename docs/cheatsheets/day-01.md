# Day 1 cheat sheet: How LLMs behave, and how to talk to them

## By the end of the day you can

- Explain why model output varies and what drives cost and latency.
- Call a model through an API and get validated, structured output.
- Choose a model tier on evidence, not habit.

## Key concepts (this morning)

|  |  |
| --- | --- |
| 30 min | How LLMs work for engineers: tokens, context window, sampling, temperature |
| 20 min | Model landscape: capability tiers, cost and latency trade-offs, when a small model is enough |
| 40 min | Prompting as engineering: roles, instructions, examples, delimiters, output schemas, prompt versioning |
| 15 min | Failure modes: hallucination, sycophancy, instruction drift, non-determinism |
| 45 min | Guided walkthrough: the facilitator live-codes the first steps of today's lab; you follow along |

## Today's lab: L1

Lab text: `docs/programme/labs/L1.md` · starter: `starter/l1`

```
python starter/l1/classify.py 1   # then 2, 4, 5 as you complete each TODO
```

### Hint cards

- If validation fails, print the raw model output first and compare it with the schema.
- Score with the helper script; do not judge by eye.
- Cost per 1,000 tickets = tokens per ticket × 1,000 × price per token. The helper prints the first part.

## The stuck ladder

1. Re-read the task and the hint card (5 min).
2. Ask your coding assistant to **explain** the error, not to fix it.
3. Check this cheat sheet.
4. Ask a facilitator.
5. Skip to the next task, mark it, and catch up in office hours.

## Explain it back

At the debrief you will explain one thing you built in your own words.
