"""Session 1: a skill = SKILL.md (frontmatter + body) + optional scripts/ and references/.
Progressive disclosure: only name+description are always visible; the body loads when routed."""
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

from . import config, llm
from .agent import Agent
from .hooks import default_hooks
from .tools import make_tools
from .trace import Trace


@dataclass
class Skill:
    name: str
    description: str
    body: str
    path: Path
    version: str


def parse_skill(path):
    text = Path(path).read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    if not m:
        raise ValueError(f"{path}: missing frontmatter")
    meta = dict(re.findall(r"^(\w+):\s*(.+)$", m.group(1), re.M))
    for key in ("name", "description"):
        if key not in meta:
            raise ValueError(f"{path}: frontmatter missing {key!r}")
    return Skill(meta["name"], meta["description"], m.group(2).strip(), Path(path).parent,
                 hashlib.sha1(text.encode()).hexdigest()[:8])


def load_skills(skills_dir=None):
    d = Path(skills_dir or config.SKILLS_DIR)
    return {s.name: s for s in (parse_skill(p) for p in sorted(d.glob("*/SKILL.md")))}


ROUTER_SYSTEM = """You route a user request to at most one skill. Skills:
{skills}

Pick a skill ONLY if the request is clearly the job that skill's description says it does.
If the request is a near miss (similar topic, different job) or no skill fits, choose none.
Reply as JSON: {{"skill": "<name or null>"}}"""


def route(prompt, skills, model=None):
    listing = "\n".join(f"- {s.name}: {s.description}" for s in skills.values())
    out = llm.ask_json(ROUTER_SYSTEM.format(skills=listing), prompt, model=model)
    name = out.get("skill")
    return name if name in skills else None


def skill_system(skill, root):
    rel = Path(skill.path).relative_to(root).as_posix() if Path(root) in Path(skill.path).parents else skill.path
    return (f"You are an engineering assistant working in a git repository.\n\n# Skill: {skill.name}\n"
            f"{skill.body}\n\n(Skill directory: {rel}.) Use the tools; give a final answer when done.")


BASELINE_SYSTEM = ("You are an engineering assistant working in a git repository. "
                   "Use the tools if you need to inspect it; give a final answer when done.")


def run_skill(skill, task, root=None, use_skill=True, model=None, max_turns=8, trace=None, hooks=None):
    root = Path(root or config.REPO)
    agent = Agent(make_tools(root, read_only=True), skill_system(skill, root) if use_skill else BASELINE_SYSTEM,
                  hooks=hooks or default_hooks(root, run_tests=False), max_turns=max_turns,
                  trace=trace or Trace(), model=model, name=f"skill:{skill.name}")
    return agent.run(task)
