# Day 2 cheat sheet: Context engineering and the anatomy of an agent

## By the end of the day you can

- Describe what belongs in context and what degrades it.
- Explain the agent loop: model, tools, observations, memory, stop condition.
- Use a coding agent safely: modes, permissions, rules files.

## Key concepts (this morning)

|  |  |
| --- | --- |
| 30 min | Context engineering: what goes in, ordering, compaction, context rot over long sessions |
| 30 min | What an agent is: workflows vs agents, the autonomy spectrum, the loop |
| 20 min | Tool calling mechanics: schemas, results, errors |
| 25 min | First look at coding agents: plan vs act modes, permissions, project rules files |
| 45 min | Guided walkthrough: the facilitator live-codes the first steps of today's lab; you follow along |

## Today's lab: L2

Lab text: `docs/programme/labs/L2.md` · starter: `starter/bugfix-repo`

```
cd starter/bugfix-repo
python -m unittest discover tests
```

### Hint cards

- Ask the agent to explain the failing test before asking it to fix anything.
- If the diff touches files you did not expect, reject it and make the prompt narrower.
- Paste the exact test failure; it works better than describing it.

## Today's lab: L3

Lab text: `docs/programme/labs/L3.md` · starter: `starter/l3`

```
python -m unittest discover starter/l3    # offline, fake model
python starter/l3/agent.py        # real model, 5 tasks
```

### Hint cards

- The loop: call the model → if it asked for tools, run them and add the results → repeat; otherwise stop.
- A tool error is just another message to the model.
- Resolve the file path and check it starts with the sandbox folder before reading.

## The stuck ladder

1. Re-read the task and the hint card (5 min).
2. Ask your coding assistant to **explain** the error, not to fix it.
3. Check this cheat sheet.
4. Ask a facilitator.
5. Skip to the next task, mark it, and catch up in office hours.

## Explain it back

At the debrief you will explain one thing you built in your own words.
