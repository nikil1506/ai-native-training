"""L1: your first API call. Complete each TODO in order. Run: python starter/l1/classify.py <step>
Steps: 1 (first call)  2 (temperature)  3 (structured output)  4 (prompt versions)  5 (two model sizes)"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from starter.common import LARGE, SMALL, chat, load_jsonl  # noqa: E402
from starter.l1.score import score  # noqa: E402
from starter.l1.validator import validate  # noqa: E402

TICKETS = load_jsonl(Path(__file__).parent / "tickets.jsonl")

SCHEMA = {  # TODO 3: this schema is what you pass as `schema=` to constrain the output. Finish it.
    "type": "object",
    "properties": {"category": {"type": "string"}},  # TODO: add urgency (enum) and summary; restrict category to the 5 values
    "required": ["category"],
}

PROMPT_V1 = "Classify this support ticket."
PROMPT_V2 = None  # TODO 4: clearer instructions, delimiters (e.g. <ticket>...</ticket>), and 3 examples


def step1():
    # TODO 1: make a chat call with PROMPT_V1 + the first ticket; print the reply, token usage and time taken.
    # Hint: chat([...]) returns (message, usage). Print usage["in_tokens"], usage["out_tokens"], usage["seconds"].
    raise NotImplementedError("TODO 1")


def step2():
    # TODO 2: run the same prompt 10 times at temperature 0 and 10 times at temperature 1
    # (pass temperature=... to chat). Count distinct replies each time.
    # Then write three sentences in results.md on what changed and why.
    raise NotImplementedError("TODO 2")


def classify(ticket, prompt, model=SMALL):
    # TODO 3: call the model with schema=SCHEMA, parse the JSON reply, validate it with validate().
    # If invalid, retry ONCE (feed the problems back to the model). Return (obj_or_None, usage).
    raise NotImplementedError("TODO 3")


def run_all(prompt, model=SMALL, tier="small"):
    preds, usages = {}, []
    for t in TICKETS:
        obj, usage = classify(t, prompt, model)
        usages.append(usage)
        if obj:
            preds[t["id"]] = obj
    return score(preds, TICKETS, usages, tier), preds


def step4():
    # TODO 4: score PROMPT_V1 and PROMPT_V2 with run_all(); commit each prompt version to git.
    for name, p in (("v1", PROMPT_V1), ("v2", PROMPT_V2)):
        if p:
            print(name, run_all(p)[0])


def step5():
    # TODO 5: run your best prompt on SMALL and LARGE (tier "small"/"large"); fill the table in results.md.
    raise NotImplementedError("TODO 5")


if __name__ == "__main__":
    {"1": step1, "2": step2, "4": step4, "5": step5}[sys.argv[1] if len(sys.argv) > 1 else "1"]()
