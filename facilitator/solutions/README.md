# Reference solutions (facilitator only; share each one after the lab so participants can compare approaches)
| Lab | Solution | Verified how |
| --- | --- | --- |
| L1 | `l1/classify.py` | live on Ollama: v1 small 60%, v2 small 75%, v2 large 70% (larger is not automatically better) |
| L2 | `bugfix-repo/cart.py` | `tests/test_programme.py` (all 7 tests pass) |
| L3 | `l3/agent.py` | `tests/test_programme.py` (9 offline tests) |
| L7 | `orders-api/tools.py` | live: 8/8 tasks pass (destructive DELETE not exposed) |
| L8 | `support-agent/agent.py` | `tests/test_programme.py` (7 guardrail tests) |
| L9 | `policy-corpus/rag.py` | live: hit@5 1.00, hit@1 0.75-0.80, access tests pass; "I don't know" on unanswerable |
| L10/L11 | `eval/check_threshold.py`, `eval/tracing_and_report.py` | baseline run: overall code 0.5 (adversarial 0.25) |
| L12 | `incidents/orchestrator.py` | live: team beats single on inc-1 and inc-3 (catches planted errors); on inc-2 both repeat a planted error (good discussion) |
| L14 | `vulnerable-agent/hardened.py` | `tests/test_programme.py` (scripted "tricked" model; every attack blocked in code) |
Not provided (open-ended; judged on process evidence): L4, L5, L6, L13, and the capstone.
Results vary run to run with a local model; treat numbers as ballparks.
