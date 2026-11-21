# Day 8 cheat sheet: Knowledge and memory: RAG

## By the end of the day you can

- Choose between RAG, long context and other approaches.
- Build and measure a retrieval pipeline with citations.
- Enforce access control on knowledge.

## Key concepts (this morning)

|  |  |
| --- | --- |
| 25 min | RAG vs long context vs fine-tuning: decision criteria |
| 35 min | Chunking, embeddings, hybrid search, reranking |
| 25 min | Grounding and citations; saying "I don't know" |
| 20 min | Memory patterns, freshness, access control on retrieved content |
| 45 min | Guided walkthrough: the facilitator live-codes the first steps of today's lab; you follow along |

## Today's lab: L9

Lab text: `docs/programme/labs/L9.md` · starter: `starter/policy-corpus`

```
python starter/policy-corpus/ingest.py 40
python starter/policy-corpus/score.py   # hit@5 / hit@1 + access test
```

### Hint cards

- Try a small chunk size and a large one; compare the numbers, not your feeling.
- Check each citation actually appears in what was retrieved.
- Write the access test first: ask as the wrong role and expect nothing back.

## The stuck ladder

1. Re-read the task and the hint card (5 min).
2. Ask your coding assistant to **explain** the error, not to fix it.
3. Check this cheat sheet.
4. Ask a facilitator.
5. Skip to the next task, mark it, and catch up in office hours.

## Explain it back

At the debrief you will explain one thing you built in your own words.
