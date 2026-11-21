# Day 12 guided walkthrough script: State, orchestration and human-in-the-loop

45 minutes, live-coded; **record it** so a participant who falls behind can replay it.

## L13

**Guided start (from the lab):**

The facilitator saves state after one step, stops the process, and resumes it.

**Live-code, in order:** the first one or two Tasks of the lab:

1. Save the run's state after every agent step.
2. Stop the program part-way and resume it without repeating finished steps.
3. Add an approval step before publishing: continue automatically only when the reviewer is confident and no serious findings are open; otherwise wait for a person.
4. Write a decision log: who decided, what, why, when.

**Run it:** `use starter/incidents/checkpoint.py`

**Stop when:** the first TODO is done and the participants can continue alone. Show where the hint cards are.
