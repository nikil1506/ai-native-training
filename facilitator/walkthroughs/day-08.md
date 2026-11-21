# Day 8 guided walkthrough script: Knowledge and memory: RAG

45 minutes, live-coded; **record it** so a participant who falls behind can replay it.

## L9

**Guided start (from the lab):**

The facilitator indexes the documents live and shows one question that retrieves the wrong chunk.

**Live-code, in order:** the first one or two Tasks of the lab:

1. Run the ingest helper to chunk, embed and index the documents.
2. Give the agent a retrieval tool that returns chunks with their source IDs.
3. Make answers cite sources. For unanswerable questions the agent says it does not know.
4. Measure how often the right document is in the top 5 (hit@5) with two chunk sizes, using the scoring helper.
5. Use the filter helper so restricted documents are never returned to the wrong role.

**Run it:** `python starter/policy-corpus/ingest.py 40`

**Stop when:** the first TODO is done and the participants can continue alone. Show where the hint cards are.
