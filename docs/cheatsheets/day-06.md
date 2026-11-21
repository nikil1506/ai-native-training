# Day 6 cheat sheet: Tool design and MCP

## By the end of the day you can

- Design tools an agent can use reliably.
- Expose a system safely through MCP or native function calling.
- Measure the effect of tool-description quality.

## Key concepts (this morning)

|  |  |
| --- | --- |
| 30 min | Function calling schemas; tool names and descriptions are prompts |
| 20 min | Tool granularity, idempotency, safe vs destructive actions, confirmation patterns |
| 20 min | Actionable errors and bounded outputs |
| 35 min | Model Context Protocol: servers, tools, resources, prompts; auth and permissions |
| 45 min | Guided walkthrough: the facilitator live-codes the first steps of today's lab; you follow along |

## Today's lab: L7

Lab text: `docs/programme/labs/L7.md` · starter: `starter/orders-api`

```
python starter/orders-api/run_tasks.py
python starter/orders-api/mcp_server.py   # your MCP server
```

### Hint cards

- Describe a tool the way you would explain it to a new colleague.
- A tool that deletes something should ask for explicit confirmation or not exist.
- Keep tool outputs short; long outputs confuse the agent.

## The stuck ladder

1. Re-read the task and the hint card (5 min).
2. Ask your coding assistant to **explain** the error, not to fix it.
3. Check this cheat sheet.
4. Ask a facilitator.
5. Skip to the next task, mark it, and catch up in office hours.

## Explain it back

At the debrief you will explain one thing you built in your own words.
