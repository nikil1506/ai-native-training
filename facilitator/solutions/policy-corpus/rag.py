"""Reference solution for L9."""
import json
import re
import sys
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "harness").is_dir())
HERE = ROOT / "starter/policy-corpus"
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(ROOT))
from access import allowed  # noqa: E402
from ingest import cosine, embed, load_index  # noqa: E402
from starter.common import chat  # noqa: E402

CHUNK_WORDS = int(__import__("os").environ.get("CHUNK_WORDS", "40"))
MIN_SCORE = 0.12


def retrieve(question, role, k=5):
    qv = embed(question)
    best = {}
    for c in load_index(CHUNK_WORDS):
        if not allowed(role, c["audience"]):                       # access control BEFORE ranking
            continue
        s = cosine(qv, c["vec"])
        if c["doc"] not in best or s > best[c["doc"]]["score"]:
            best[c["doc"]] = {"doc": c["doc"], "title": c["title"], "text": c["text"], "score": round(s, 3)}
    return sorted(best.values(), key=lambda r: -r["score"])[:k]


def answer(question, role):
    hits = [h for h in retrieve(question, role, 3) if h["score"] >= MIN_SCORE]
    if not hits:
        return "I don't know: I couldn't find that in the policies I can access."
    ctx = "\n".join(f"[{h['doc']}] {h['text']}" for h in hits)
    msg, _ = chat([{"role": "system", "content": "Answer ONLY from the context. Cite sources like [doc-id]. If the context does not contain the answer, reply exactly: I don't know."},
                   {"role": "user", "content": f"Context:\n{ctx}\n\nQuestion: {question}"}])
    text = msg["content"].strip()
    cited = set(re.findall(r"\[([a-z0-9-]+)\]", text))
    if cited - {h["doc"] for h in hits}:                            # invented citation: reject in code
        return "I don't know: could not produce a verifiable citation."
    if "don't know" not in text.lower() and not cited:
        text += " [" + hits[0]["doc"] + "]"
    return text


if __name__ == "__main__":
    print(answer(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "employee"))
