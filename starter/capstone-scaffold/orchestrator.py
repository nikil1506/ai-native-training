"""Capstone scaffold: an orchestrator skeleton. Replace the TODOs with YOUR design; reuse your L8-L13 code.
Roles are functions with typed (schema-checked) hand-offs. State is checkpointed; risky actions wait for approval.
Run: python starter/capstone-scaffold/orchestrator.py <scenario> [--resume RUN_ID]"""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1])); sys.path.insert(0, str(HERE.parents[1] / "starter" / "incidents"))
from schema import validate  # noqa: E402
import checkpoint  # noqa: E402
from starter.common import SMALL, chat  # noqa: E402
from harness.trace import Trace  # noqa: E402

SCENARIOS = {p.name: p for p in (HERE / "scenarios").iterdir() if p.is_dir()}
HANDOFF_SCHEMAS = {
    # TODO: one JSON schema per hand-off (e.g. intake->researcher, researcher->writer, writer->reviewer, reviewer->orchestrator)
}
DECISIONS = []   # decision log: who / what / why / when


def decide(who, what, why):
    DECISIONS.append({"who": who, "what": what, "why": why, "when": time.strftime("%Y-%m-%d %H:%M:%S")})


def role_intake(case, state):
    raise NotImplementedError("TODO role 1: classify / extract the case")


def role_worker(case, state):
    raise NotImplementedError("TODO role 2: research (tools + knowledge with citations + access check)")


def role_reviewer(draft, sources, state):
    raise NotImplementedError("TODO role 3: INDEPENDENT reviewer, fresh context, checks claims against sources")


def approval_needed(draft, review):
    """TODO: risk-based gate: auto-continue ONLY when the reviewer is confident and no serious findings are open."""
    return True


def run(scenario, run_id=None):
    run_id = run_id or f"{scenario}-{int(time.time())}"
    state = checkpoint.load(run_id) or {"steps": []}
    trace = Trace(HERE / "runs" / f"{run_id}.jsonl")
    # TODO: for each step: skip if already in state['steps'] (resume), run it, validate the hand-off against HANDOFF_SCHEMAS,
    # save state BEFORE moving on (checkpoint.save), trace tokens/time/cost, then approval step before the guarded action.
    raise NotImplementedError("TODO orchestration")


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[sys.argv.index("--resume") + 1] if "--resume" in sys.argv else None)
