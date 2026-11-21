# Day 9 guided walkthrough script: Evaluation: the unit tests of agents

45 minutes, live-coded; **record it** so a participant who falls behind can replay it.

## L10

**Guided start (from the lab):**

The facilitator runs the eval on a deliberately weak agent, reads two failures, and explains the score.

**Live-code, in order:** the first one or two Tasks of the lab:

1. Add 8 of your own cases to the 12 provided (at least 3 awkward ones and 3 adversarial ones). Set 5 aside as a held-out group.
2. Write two code checks (for example: the right tool was called, refunds escalated) and use the provided judge for answer quality.
3. Check the judge: label 6 answers yourself and compare. Note where it disagrees and adjust the judge prompt.
4. Run the baseline, make two improvements that each fix a specific failure, then run again and compare scores, including the held-out group.
5. Add a small script that fails if the score drops below a threshold.

**Run it:** `python starter/eval/run_eval.py --name baseline`

**Stop when:** the first TODO is done and the participants can continue alone. Show where the hint cards are.
