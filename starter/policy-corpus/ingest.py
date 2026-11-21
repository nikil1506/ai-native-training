"""Provided ingest helper: chunk -> embed -> index.   python starter/policy-corpus/ingest.py <chunk_words> [overlap]
Embeddings: if EMBED_MODEL is set (e.g. nomic-embed-text) it uses Ollama's /api/embed; otherwise a hashed
bag-of-words vector (no model needed, deterministic, works offline). Writes index_<chunk_words>.json."""
import hashlib
import json
import math
import os
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
DIM = 512


def parse_doc(path):
    text = Path(path).read_text(encoding="utf-8")
    _, fm, body = text.split("---", 2)
    meta = dict(re.findall(r"^(\w+):\s*(.+)$", fm, re.M))
    return meta, body.strip()


def chunk(text, size, overlap=0):
    words = text.split()
    step = max(1, size - overlap)
    return [" ".join(words[i:i + size]) for i in range(0, max(1, len(words)), step) if words[i:i + size]]


def _hash_embed(text):
    v = [0.0] * DIM
    for w in re.findall(r"[a-z0-9]+", text.lower()):
        v[int(hashlib.md5(w.encode()).hexdigest(), 16) % DIM] += 1.0
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]


def embed(text):
    model = os.environ.get("EMBED_MODEL")
    if model:
        from harness import config  # noqa: F401  (host)
        req = urllib.request.Request(config.HOST + "/api/embed", json.dumps({"model": model, "input": text}).encode(),
                                     {"Content-Type": "application/json"})
        return json.loads(urllib.request.urlopen(req, timeout=120).read())["embeddings"][0]
    return _hash_embed(text)


def cosine(a, b):
    return sum(x * y for x, y in zip(a, b))


def build_index(size, overlap=0):
    idx = []
    for p in sorted((HERE / "docs").glob("*.md")):
        meta, body = parse_doc(p)
        for i, c in enumerate(chunk(body, size, overlap)):
            idx.append({"doc": meta["id"], "audience": meta["audience"], "title": meta["title"],
                        "chunk": i, "text": c, "vec": embed(meta["title"] + ". " + c)})
    return idx


def load_index(size):
    f = HERE / f"index_{size}.json"
    if not f.exists():
        f.write_text(json.dumps(build_index(size)))
    return json.loads(f.read_text())


if __name__ == "__main__":
    size = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    ov = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    idx = build_index(size, ov)
    (HERE / f"index_{size}.json").write_text(json.dumps(idx))
    print(f"indexed {len(idx)} chunks from {len({c['doc'] for c in idx})} docs (chunk={size} words)")
