# Day 6 guided walkthrough script: Tool design and MCP

45 minutes, live-coded; **record it** so a participant who falls behind can replay it.

## L7

**Guided start (from the lab):**

The facilitator turns one endpoint into a tool live and shows how a good description changes the agent's choice.

**Live-code, in order:** the first one or two Tasks of the lab:

1. Choose at most four tools. Write each name, description and parameters. Decide which endpoint to hide or guard, and write why.
2. Implement them as function-calling tools, then expose them with the MCP server template.
3. Connect an agent and run the eight task prompts.
4. Make the descriptions worse on purpose (vague names, overlapping tools), run again, and note the difference.
5. Make errors helpful: return a clear message and a hint about what to try next.

**Run it:** `python starter/orders-api/run_tasks.py`

**Stop when:** the first TODO is done and the participants can continue alone. Show where the hint cards are.
