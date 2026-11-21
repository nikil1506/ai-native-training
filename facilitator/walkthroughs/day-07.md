# Day 7 guided walkthrough script: Single-agent design: planning, recovery, guardrails

45 minutes, live-coded; **record it** so a participant who falls behind can replay it.

## L8

**Guided start (from the lab):**

The facilitator shows where a limit belongs in code, and why putting it only in the prompt is not enough.

**Live-code, in order:** the first one or two Tasks of the lab:

1. Complete the agent with `lookup_order`, `search_kb` (stub), `create_ticket` and `escalate_to_human`.
2. Enforce three limits in code: a step limit, a token budget, and the rule that refunds always go to a human.
3. Make the agent write its plan before it acts, and log it.
4. Turn on the failure-injection switch (tools sometimes fail or return bad data) and fix what breaks.
5. When an order number is missing, make the agent ask a question instead of guessing.

**Run it:** `python -m unittest discover starter/support-agent`

**Stop when:** the first TODO is done and the participants can continue alone. Show where the hint cards are.
