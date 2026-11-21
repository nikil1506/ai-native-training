# Day 9 cheat sheet: Evaluation: the unit tests of agents

## By the end of the day you can

- Build a labelled eval set and graders.
- Calibrate an LLM judge against human labels.
- Gate changes on eval results.

## Key concepts (this morning)

|  |  |
| --- | --- |
| 30 min | Why evals come first: eval-driven development, offline vs online |
| 30 min | Datasets: from logs, edge cases, adversarial cases; held-out sets |
| 30 min | Graders: code-based, rubric LLM-judge, pairwise; judge biases and calibration |
| 15 min | Regression gates in CI; variance and repeated runs |
| 45 min | Guided walkthrough: the facilitator live-codes the first steps of today's lab; you follow along |

## Today's lab: L10

Lab text: `docs/programme/labs/L10.md` · starter: `starter/eval`

```
python starter/eval/run_eval.py --name baseline
python starter/eval/check_threshold.py starter/eval/reports/after.json 0.7
```

### Hint cards

- Write what you expect the agent to do before you run it.
- Fix one failure at a time and re-run.
- If the held-out score is far lower than the rest, you have over-fitted.

## The stuck ladder

1. Re-read the task and the hint card (5 min).
2. Ask your coding assistant to **explain** the error, not to fix it.
3. Check this cheat sheet.
4. Ask a facilitator.
5. Skip to the next task, mark it, and catch up in office hours.

## Explain it back

At the debrief you will explain one thing you built in your own words.
