# Day 11 guided walkthrough script: Multi-agent patterns

45 minutes, live-coded; **record it** so a participant who falls behind can replay it.

## L12

**Guided start (from the lab):**

The facilitator runs the skeleton end to end and points out where the hand-offs happen.

**Live-code, in order:** the first one or two Tasks of the lab:

1. Baseline: let one agent write a postmortem for each incident and score it with the rubric.
2. Add a writer agent and an independent reviewer agent (new context) to the skeleton. The reviewer checks claims against the sources.
3. Make every hand-off follow the provided JSON schemas and check them in code.
4. Compare with the baseline on accuracy, completeness, cost and time.
5. Write a few sentences on when the team was and was not worth the extra cost.

**Run it:** `python starter/incidents/orchestrator.py inc-1 single`

**Stop when:** the first TODO is done and the participants can continue alone. Show where the hint cards are.
