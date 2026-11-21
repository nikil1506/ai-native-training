# L12: A multi-agent pipeline versus one agent (Day 11, 3 h) + L13: Make it recoverable (Day 12, 2 h)
Three incident bundles (`bundles/`) contain PLANTED MISTAKES (chat and timeline disagree with the logs). Skeleton: `orchestrator.py` (two researchers wired in),
`schemas/`, `schema.py`, `rubric.md`, `score.py`. For L13 use `checkpoint.py`: save state after every step, resume without repeating work,
add an approval step before publishing, and keep a decision log (who/what/why/when).
Stretch (L12): second review round (limit 2). Stretch (L13): two runs at once.
