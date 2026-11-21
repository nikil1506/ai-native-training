# Trace-reading guide (A2 checkpoint and everyday debugging)
A trace is one JSON line per model call and per tool call. Read it top to bottom and answer, in order:
1. **What was the task?** (first line) Is it still visible in the latest model call?
2. **Is `in_tokens` growing?** Steadily growing input = context accumulating (full files, whole histories). Compare to the context limit; look for `context_length_exceeded` and for answers that forget the task afterwards.
3. **Which tool did the model choose, and was it the right one?** Read the tool *descriptions*: vague or overlapping descriptions ("Search things", "Get information") cause wrong or repeated tool choices.
4. **Is anything repeating?** Same tool + same args + same error many times = a retry loop with no limit, backoff or escalation. Look at the run's budget (max steps / timeout) in the start line.
5. **Where did the time and tokens go?** Sum per step name; the biggest few are your top costs.
6. **Does the final answer follow from the tool results?** If not, the model is guessing.

| Symptom | Likely root cause | Typical fix | Eval that would catch it |
| --- | --- | --- | --- |
| input tokens climb every step, then an error | no context management | summarise or trim tool output, cap sizes, retrieve instead of dump | long-input cases; assert max tokens per step |
| model uses the wrong tool, answer plausible but wrong | vague/overlapping tool descriptions | rename, rewrite descriptions, merge overlapping tools | task set with expected tool per case |
| same call repeated, spend grows | no retry limit/backoff/escalation | cap retries, exponential backoff, escalate to a human, step budget | failure-injection cases; assert bounded calls |
