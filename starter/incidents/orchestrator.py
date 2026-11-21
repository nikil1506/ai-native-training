"""L12: a small team of agents vs one agent. Two researcher agents are already wired in. Run: python starter/incidents/orchestrator.py inc-1 [single|team]
Hand-offs MUST follow schemas/*.json and be checked in code (schema.py)."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parents[1]))
from schema import validate  # noqa: E402
from starter.common import SMALL, chat  # noqa: E402

SCHEMAS = {p.stem: json.loads(p.read_text()) for p in (HERE / "schemas").glob("*.json")}
MAX_REVIEW_ROUNDS = 1


def read_bundle(name):
    d = HERE / "bundles" / name
    return {f.stem: f.read_text(encoding="utf-8") for f in d.iterdir()}


def call_json(system, user, schema_name, retries=1):
    """One model call that must return JSON matching a schema; the hand-off is validated IN CODE."""
    msgs = [{"role": "system", "content": system}, {"role": "user", "content": user}]
    for _ in range(retries + 1):
        msg, usage = chat(msgs, model=SMALL, schema=SCHEMAS[schema_name])
        try:
            obj = json.loads(msg["content"])
        except ValueError:
            obj = None
        errs = validate(obj, SCHEMAS[schema_name]) if obj is not None else ["invalid JSON"]
        if not errs:
            return obj, usage
        msgs += [{"role": "assistant", "content": msg["content"]}, {"role": "user", "content": "Schema errors: " + "; ".join(errs)}]
    raise ValueError(f"hand-off failed schema '{schema_name}': {errs}")


# ---- already wired: two researchers (each sees only its own source files) ----------------------
def researcher(name, sources, bundle):
    text = "\n\n".join(f"## {s}\n{bundle[s]}" for s in sources)
    return call_json(f"You are a {name} researcher. Extract factual claims about the incident with the source and exact evidence line. Facts only.",
                     text, "research_findings")


def research_logs(bundle):
    return researcher("logs", ["logs", "runbook"], bundle)


def research_chat(bundle):
    return researcher("chat+timeline", ["chat", "timeline"], bundle)


# ---- TODO ---------------------------------------------------------------------------------------
def run_single(bundle):
    """TODO 1 (baseline): ONE agent reads everything and writes the postmortem (schema 'draft')."""
    raise NotImplementedError("TODO 1")


def writer(findings, bundle):
    """TODO 2a: writer agent: turns the findings into a postmortem draft (schema 'draft'). It should NOT see raw chat/timeline."""
    raise NotImplementedError("TODO 2a")


def reviewer(draft, bundle):
    """TODO 2b: INDEPENDENT reviewer (fresh context): gets the draft + the sources but NOT the writer's reasoning.
    Checks each claim against the sources (logs are authoritative). Returns schema 'review'."""
    raise NotImplementedError("TODO 2b")


def run_team(bundle):
    """TODO 2c: researchers -> writer -> reviewer; if not approved, give issues back to the writer; at most MAX_REVIEW_ROUNDS."""
    raise NotImplementedError("TODO 2c")


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "inc-1"
    mode = sys.argv[2] if len(sys.argv) > 2 else "team"
    b = read_bundle(name)
    out = run_single(b) if mode == "single" else run_team(b)
    print(json.dumps(out, indent=1))
