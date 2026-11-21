# Day 4 cheat sheet: Verification, independent review and reusable agent assets

## By the end of the day you can

- Explain why self-review fails and how independent review fixes it.
- Produce and triage structured review findings.
- Package team knowledge as skills, commands, hooks and subagents.

## Key concepts (this morning)

|  |  |
| --- | --- |
| 30 min | Why verification is the core skill: the writer should not grade its own work |
| 30 min | Independent reviewer design: fresh context, structured findings (ID, severity, location, remedy), confidence |
| 20 min | Triage: acknowledge, dismiss with a recorded reason, escalate; quality gates and thresholds |
| 25 min | Reusable assets: skills, slash commands, hooks, subagents; guardrail hooks |
| 45 min | Guided walkthrough: the facilitator live-codes the first steps of today's lab; you follow along |

## Today's lab: L5

Lab text: `docs/programme/labs/L5.md` · starter: `starter/sample-repo-2`

```
cd starter/sample-repo-2
python -m unittest discover tests   # then run YOUR review skill here
```

### Hint cards

- Start the reviewer in a new session so it cannot see the earlier chat.
- Ask it to look for problems, not to confirm things are fine.
- If a finding is wrong, say so in `findings.md` and why; that counts as a good result.

## The stuck ladder

1. Re-read the task and the hint card (5 min).
2. Ask your coding assistant to **explain** the error, not to fix it.
3. Check this cheat sheet.
4. Ask a facilitator.
5. Skip to the next task, mark it, and catch up in office hours.

## Explain it back

At the debrief you will explain one thing you built in your own words.
