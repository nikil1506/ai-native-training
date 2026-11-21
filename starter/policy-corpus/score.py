"""Provided scoring helper. hit@5 = how often the right document is among the top 5 retrieved results.
    python starter/policy-corpus/score.py <chunk_words>   (uses YOUR retrieve() from rag.py)"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))


def hit_at_k(retrieve, k=5):
    """retrieve(question, role, k) -> list of {"doc": id, ...}. Returns (rate, misses)."""
    qs = json.loads((HERE / "questions.json").read_text())
    hits, misses = 0, []
    for q in qs:
        docs = [r["doc"] for r in retrieve(q["question"], q["role"], k)]
        if q["source"] in docs:
            hits += 1
        else:
            misses.append((q["question"], q["source"], docs))
    return hits / len(qs), misses


def access_ok(retrieve):
    """Run access_tests.json; returns list of failures (empty = pass)."""
    fails = []
    for t in json.loads((HERE / "access_tests.json").read_text()):
        docs = {r["doc"] for r in retrieve(t["question"], t["role"], 5)}
        for bad in t.get("must_not_return", []):
            if bad in docs:
                fails.append(f"{t['role']} was shown {bad}")
        for good in t.get("must_return", []):
            if good not in docs:
                fails.append(f"{t['role']} should see {good}")
    return fails


if __name__ == "__main__":
    from rag import retrieve
    rate, misses = hit_at_k(retrieve)
    print(f"hit@5 = {rate:.2f} ({len(misses)} misses)")
    print(f"hit@1 = {hit_at_k(retrieve, 1)[0]:.2f}   (stricter: is the right document the TOP result?)")
    for m in misses:
        print("  MISS:", m)
    print("access test failures:", access_ok(retrieve) or "none")
