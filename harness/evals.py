"""Session 2: trigger evals, output evals (code checks + model grader), N runs, baseline, saved results."""
import json
import re
import time
from pathlib import Path

from . import config, llm
from .skills import load_skills, route, run_skill


# ---- code checks -------------------------------------------------------------------------
def run_check(check, text):
    t, low = check["type"], text.lower()
    if t == "contains_all":
        return all(v.lower() in low for v in check["values"])
    if t == "contains_any":
        return any(v.lower() in low for v in check["values"])
    if t == "not_contains_any":
        return not any(v.lower() in low for v in check["values"])
    if t == "max_chars":
        return len(text) <= check["n"]
    if t == "regex":
        return bool(re.search(check["pattern"], text, re.M | re.S))
    raise ValueError(f"unknown check type {t}")


GRADER = ("You are a strict grader. Given a TASK, a RUBRIC and an OUTPUT, decide whether the output satisfies "
          'the rubric. Reply as JSON: {"pass": true|false, "reason": "<one sentence>"}')


def model_grade(task, rubric, output, model=None):
    out = llm.ask_json(GRADER, f"TASK: {task}\n\nRUBRIC: {rubric}\n\nOUTPUT:\n{output}", model=model)
    return bool(out.get("pass")), out.get("reason", "")


# ---- trigger evals -------------------------------------------------------------------------
def trigger_eval(skill_name, skills, model=None):
    cfg = json.loads((skills[skill_name].path / "evals" / "trigger.json").read_text())
    rows = []
    for expect, key in ((True, "should_trigger"), (False, "should_not_trigger")):
        for p in cfg[key]:
            got = route(p, skills, model=model)
            fired = got == skill_name
            rows.append({"prompt": p, "expected": expect, "routed_to": got, "ok": fired == expect})
    return {"score": sum(r["ok"] for r in rows), "total": len(rows), "rows": rows}


# ---- output evals --------------------------------------------------------------------------
def output_eval(skill_name, skills, runs=1, limit=None, baseline=False, model=None):
    skill = skills[skill_name]
    cases = json.loads((skill.path / "evals" / "cases.json").read_text())[:limit]
    modes = [("with_skill", True)] + ([("baseline", False)] if baseline else [])
    results = []
    for case in cases:
        for mode, use in modes:
            for i in range(runs):
                res = run_skill(skill, case["prompt"], use_skill=use, model=model)
                code = [run_check(c, res.final) for c in case["checks"]]
                g_ok, why = model_grade(case["prompt"], case["rubric"], res.final, model=model)
                results.append({"case": case["id"], "mode": mode, "run": i, "code_checks": code,
                                "code_pass": all(code), "grader_pass": g_ok, "grader_reason": why,
                                "stopped": res.stopped, "turns": res.turns, "seconds": res.seconds,
                                "output": res.final})
                print(f"  {skill_name}/{case['id']} [{mode}#{i}] code={'PASS' if all(code) else 'FAIL'} "
                      f"grader={'PASS' if g_ok else 'FAIL'}", flush=True)
    return results


def summarize(results):
    out = {}
    for mode in {r["mode"] for r in results}:
        rs = [r for r in results if r["mode"] == mode]
        out[mode] = {"runs": len(rs), "code_pass_rate": round(sum(r["code_pass"] for r in rs) / len(rs), 2),
                     "grader_pass_rate": round(sum(r["grader_pass"] for r in rs) / len(rs), 2)}
    return out


def run_all(only=None, trigger_only=False, runs=1, limit=None, baseline=False, model=None, threshold=18):
    skills = load_skills()
    names = [only] if only else [n for n, s in skills.items() if (s.path / "evals" / "trigger.json").exists()]
    stamp = time.strftime("%Y%m%d-%H%M%S")
    report = {"date": stamp, "model": model or config.MODEL, "skills": {}}
    for n in names:
        print(f"== {n} (version {skills[n].version})", flush=True)
        entry = {"version": skills[n].version}
        t = trigger_eval(n, skills, model)
        entry["trigger"] = {"score": t["score"], "total": t["total"], "passes_gate": t["score"] >= threshold,
                            "misses": [r for r in t["rows"] if not r["ok"]]}
        print(f"  trigger {t['score']}/{t['total']}", flush=True)
        if not trigger_only and (skills[n].path / "evals" / "cases.json").exists():
            res = output_eval(n, skills, runs, limit, baseline, model)
            entry["output"] = {"summary": summarize(res), "results": res}
        report["skills"][n] = entry
    out = config.RUNS / "evals" / f"{stamp}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2))
    print(f"\nsaved {out}")
    print(f"{'skill':<16}{'ver':<10}{'trigger':<10}{'code':<8}{'grader':<8}")
    for n, e in report["skills"].items():
        s = e.get("output", {}).get("summary", {}).get("with_skill", {})
        print(f"{n:<16}{e['version']:<10}{e['trigger']['score']}/{e['trigger']['total']:<7}"
              f"{s.get('code_pass_rate', '-'):<8}{s.get('grader_pass_rate', '-'):<8}")
    return report
