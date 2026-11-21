# Day 13 cheat sheet: Security, safety and governance for agents

## By the end of the day you can

- Threat-model an agent system.
- Attack and harden an agent.
- Produce audit evidence a reviewer would accept.

## Key concepts (this morning)

|  |  |
| --- | --- |
| 30 min | Agent threat model: indirect prompt injection, confused deputy, exfiltration, excessive agency |
| 25 min | Least privilege, sandboxing, egress allow-lists, secrets handling |
| 25 min | Audit trails, traceability, decision records; IP, licensing and data classification |
| 25 min | Supply chain: vetting skills, MCP servers and third-party tools |
| 45 min | Guided walkthrough: the facilitator live-codes the first steps of today's lab; you follow along |

## Today's lab: L14

Lab text: `docs/programme/labs/L14.md` · starter: `starter/vulnerable-agent`

```
python starter/vulnerable-agent/run_attack.py 1   # 1-5
python -m unittest starter/vulnerable-agent/test_hardening.py   # AGENT=path/to/your/agent.py
```

### Hint cards

- Ask: what is the worst thing this tool could do if the model were tricked?
- Telling the model "don't" is not enough; remove the ability.
- Never put secrets into the prompt.

## The stuck ladder

1. Re-read the task and the hint card (5 min).
2. Ask your coding assistant to **explain** the error, not to fix it.
3. Check this cheat sheet.
4. Ask a facilitator.
5. Skip to the next task, mark it, and catch up in office hours.

## Explain it back

At the debrief you will explain one thing you built in your own words.
