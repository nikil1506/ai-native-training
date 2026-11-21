# Day 4 guided walkthrough script: Verification, independent review and reusable agent assets

45 minutes, live-coded; **record it** so a participant who falls behind can replay it.

## L5

**Guided start (from the lab):**

The facilitator builds a minimal review skill live and shows how a fresh context behaves differently from the writing session.

**Live-code, in order:** the first one or two Tasks of the lab:

1. Create a reusable review skill, command or subagent for your tool. It starts with a fresh context and reports findings in a fixed format: ID, severity, file and line, issue, fix.
2. Run it on your L4 code.
3. Go through each finding in `findings.md`: accept it, dismiss it with a reason, or escalate it.
4. Give the accepted findings to the writer agent, then run the reviewer again. Note what changed between round one and round two.
5. Add a simple hook or script that stops a commit if the tests fail.
6. Prove it is reusable: write a short README, then install and run the skill in `sample-repo-2` using only your README.

**Run it:** `cd starter/sample-repo-2`

**Stop when:** the first TODO is done and the participants can continue alone. Show where the hint cards are.
