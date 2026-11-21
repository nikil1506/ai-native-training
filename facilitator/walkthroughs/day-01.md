# Day 1 guided walkthrough script: How LLMs behave, and how to talk to them

45 minutes, live-coded; **record it** so a participant who falls behind can replay it.

## L1

**Guided start (from the lab):**

The facilitator makes the first API call live, prints the token usage, and shows where the key is loaded from.

**Live-code, in order:** the first one or two Tasks of the lab:

1. Fill in the first `TODO`: make a chat call and print the reply, the token usage and the time taken.
2. Run the same prompt 10 times at temperature 0 and at 1. Write three sentences on what changed and why.
3. Make the classifier return `{category, urgency, summary}` using the structured-output option, then check it with the provided validator. Retry once if the output is invalid.
4. Improve the prompt: clearer instructions, delimiters, three examples. Score each version with the helper.
5. Run your best prompt on two model sizes and fill in the comparison table: accuracy, speed, cost per 1,000 tickets.

**Run it:** `python starter/l1/classify.py 1   # then 2, 4, 5 as you complete each TODO`

**Stop when:** the first TODO is done and the participants can continue alone. Show where the hint cards are.
