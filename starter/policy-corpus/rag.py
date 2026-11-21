"""L9: give the agent knowledge. Complete the TODOs. Run: python starter/policy-corpus/score.py <chunk_words>
Then: python starter/policy-corpus/rag.py "How many days of annual leave do I get?" employee"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parents[1]))
from access import allowed  # noqa: E402
from ingest import cosine, embed, load_index  # noqa: E402

CHUNK_WORDS = int(__import__("os").environ.get("CHUNK_WORDS", "40"))   # TODO 4: try two sizes and compare hit@5


def retrieve(question, role, k=5):
    """TODO 2+5: embed the question, score every chunk, keep the top k DOCUMENTS (dedupe by doc id),
    and ONLY consider chunks whose audience the role may see (allowed(role, audience)).
    Return a list of {"doc": id, "title": ..., "text": ..., "score": ...}, best first."""
    raise NotImplementedError("TODO 2/5")


def answer(question, role):
    """TODO 3: call the model with the retrieved chunks (labelled with their doc ids) and require citations like [doc-id].
    - cite only ids that were actually retrieved (check this in code, don't trust the model)
    - if nothing relevant was retrieved, say you don't know (do not invent an answer)"""
    raise NotImplementedError("TODO 3")


if __name__ == "__main__":
    print(answer(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "employee"))
