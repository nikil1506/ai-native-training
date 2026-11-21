# L9: Give the agent knowledge: RAG with citations (Day 8, 3 h)
~30 documents in `docs/` (front matter `audience:`), 20 questions with the right source (`questions.json`), 4 unanswerable (`unanswerable.json`),
`access_tests.json`, helpers `ingest.py`, `score.py`, `access.py`. Embeddings: set `EMBED_MODEL` for a real model, else hashed bag-of-words.
Deliverables: pipeline code, `retrieval-report.md` (hit@5 for two chunk sizes). Stretch: rewrite the user's question before searching and report the effect.
