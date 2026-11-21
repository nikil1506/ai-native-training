"""L12: a small team of agents vs one agent. Two researcher agents are already wired in. Run: python starter/incidents/orchestrator.py inc-1 [single|team]
Hand-offs MUST follow schemas/*.json and be checked in code (schema.py)."""
import json
import sys
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "harness").is_dir())
HERE = ROOT / "starter/incidents"
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(ROOT))
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


# ---- reference solution -----------------------------------------------------------------------
SYS_WRITE = ("You write incident postmortems. Use ONLY the supplied findings. When sources disagree, logs are authoritative. "
             "Times must be exactly as in the logs.")


def run_single(bundle):
    text = "\n\n".join(f"## {k}\n{v}" for k, v in bundle.items() if k != "title")
    d, u = call_json(SYS_WRITE + " Read the raw sources.", text, "draft")
    d["_usage"] = u
    return d


def writer(findings, bundle, issues=None):
    extra = ("\nA reviewer found these problems; fix them: " + json.dumps(issues)) if issues else ""
    return call_json(SYS_WRITE, f"Findings:\n{json.dumps(findings)}{extra}", "draft")


def reviewer(draft, bundle):
    sources = "\n\n".join(f"## {k}\n{v}" for k, v in bundle.items() if k in ("logs", "runbook"))
    return call_json("You are an independent reviewer. Check every claim and every time in the draft against the logs (authoritative). "
                     "Set approved=false and list issues if ANY claim is unsupported or contradicts the logs.",
                     f"Draft:\n{json.dumps(draft)}\n\nSources:\n{sources}", "review")


def run_team(bundle):
    f1, u1 = research_logs(bundle)
    f2, u2 = research_chat(bundle)
    findings = {"logs": f1, "chat_timeline": f2}
    draft, uw = writer(findings, bundle)
    usage = [u1, u2, uw]
    for _ in range(MAX_REVIEW_ROUNDS + 1):
        rev, ur = reviewer(draft, bundle)
        usage.append(ur)
        if rev["approved"] or not rev["issues"]:
            break
        draft, uw = writer(findings, bundle, rev["issues"])
        usage.append(uw)
    draft["_review"] = rev
    draft["_usage"] = {"in_tokens": sum(u["in_tokens"] for u in usage), "out_tokens": sum(u["out_tokens"] for u in usage),
                       "seconds": round(sum(u["seconds"] for u in usage), 1)}
    return draft


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "inc-1"
    mode = sys.argv[2] if len(sys.argv) > 2 else "team"
    b = read_bundle(name)
    out = run_single(b) if mode == "single" else run_team(b)
    print(json.dumps(out, indent=1))
