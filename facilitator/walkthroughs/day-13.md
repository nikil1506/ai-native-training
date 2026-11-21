# Day 13 guided walkthrough script: Security, safety and governance for agents

45 minutes, live-coded; **record it** so a participant who falls behind can replay it.

## L14

**Guided start (from the lab):**

The facilitator runs one injection attack live and shows what the agent does with it.

**Live-code, in order:** the first one or two Tasks of the lab:

1. Write a short threat model: what the agent can touch, how data gets in, what you do not trust.
2. Try three of the five attack documents and record what happened.
3. Harden the agent: give each tool only the access it needs, allow only approved web addresses, ask for approval before sensitive actions, treat document text as data not instructions.
4. Run the same attacks again and show they now fail, or note what risk remains.
5. Add a log of every tool call.

**Run it:** `python starter/vulnerable-agent/run_attack.py 1   # 1-5`

**Stop when:** the first TODO is done and the participants can continue alone. Show where the hint cards are.
