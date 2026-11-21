# Day 2 guided walkthrough script: Context engineering and the anatomy of an agent

45 minutes, live-coded; **record it** so a participant who falls behind can replay it.

## L2

**Guided start (from the lab):**

The facilitator fixes a demo bug live: asks the agent to explain the failing test, uses plan mode, reviews the diff, runs the tests.

**Live-code, in order:** the first one or two Tasks of the lab:

1. Install and configure your coding agent. Read how its permissions work before you start.
2. For each bug: write down your prompt, let the agent try, and read the diff before you accept it.
3. For one bug, first ask the agent to investigate in read-only or plan mode, then approve the plan.
4. Keep a steering log: what you asked, what the agent got wrong, how you corrected it.
5. Run all the tests after each fix.

**Run it:** `cd starter/bugfix-repo`

**Stop when:** the first TODO is done and the participants can continue alone. Show where the hint cards are.

## L3

**Guided start (from the lab):**

The facilitator draws the loop on the whiteboard, then fills in the first `TODO` live.

**Live-code, in order:** the first one or two Tasks of the lab:

1. Complete the loop: send messages and tool definitions, run any tool calls the model returns, add the results, stop when the model gives a final answer.
2. Finish the two tools: `calculator` and `read_file` (only inside the sandbox folder).
3. Add a maximum step limit and print each step with its token count.
4. Send tool errors back to the model as messages instead of crashing.
5. Run the five tasks and read the logs.

**Run it:** `python -m unittest discover starter/l3    # offline, fake model`

**Stop when:** the first TODO is done and the participants can continue alone. Show where the hint cards are.
