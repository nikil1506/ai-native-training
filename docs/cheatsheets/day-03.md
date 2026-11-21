# Day 3 cheat sheet: Spec-driven development

## By the end of the day you can

- Turn a vague request into a spec an agent can build against.
- Write acceptance tests before implementation.
- Break work into small, independently verifiable tasks.

## Key concepts (this morning)

|  |  |
| --- | --- |
| 30 min | Why specs: agent output quality tracks the clarity of intent |
| 35 min | Spec anatomy: problem, scope, what is out of scope, requirements (what it must do and how well), testable acceptance criteria, assumptions |
| 20 min | Project context files: conventions, commands, architecture notes |
| 20 min | Plan → tasks → implement; task sizing; steering and interrupting; reading diffs critically |
| 45 min | Guided walkthrough: the facilitator live-codes the first steps of today's lab; you follow along |

## Today's lab: L4

Lab text: `docs/programme/labs/L4.md` · starter: `starter/orders-app`

```
cd starter/orders-app
python -m unittest discover tests
```

### Hint cards

- A good criterion reads: given X, when Y, then Z.
- If you cannot write a test for it, the criterion is too vague.
- Keep each task small enough to review the diff in five minutes.

## The stuck ladder

1. Re-read the task and the hint card (5 min).
2. Ask your coding assistant to **explain** the error, not to fix it.
3. Check this cheat sheet.
4. Ask a facilitator.
5. Skip to the next task, mark it, and catch up in office hours.

## Explain it back

At the debrief you will explain one thing you built in your own words.
