# L10: Build an evaluation and improve by evidence (Day 9, 3 h)
12 cases (`cases.json`, category on each), runner (`run_eval.py`), judge template (`judge_prompt.md`), `agent_under_test.py` (deliberately weak).
Tasks: add 8 cases (3 awkward, 3 adversarial; mark 5 as `"heldout": true` in total), write 2 code checks, label 6 answers and compare with the judge
(`labels_template.json`), run baseline -> 2 improvements -> after, add `check_threshold.py`.
Run: `python starter/eval/run_eval.py --name baseline` (a full run is ~12 model calls + 12 judge calls).
Stretch: `--runs 3` to see score variance.

## L11: Trace it, measure it, make it cheaper (Day 10, 2 h)
`tracing_template.py` (add spans) and `trace_report.py` (report). Reduce cost: cheaper model for simple steps, trim context, cap tool output.
Re-run the L10 eval and write a before/after including quality (cost must drop >= 20% with quality within tolerance).
