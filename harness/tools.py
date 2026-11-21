"""Built-in tools. Everything is rooted at `root` so an agent can't wander off."""
import subprocess
from pathlib import Path

from .agent import Tool


def _obj(**props):
    return {"type": "object", "properties": {k: {"type": "string", "description": v} for k, v in props.items()},
            "required": list(props)}


def make_tools(root, read_only=False):
    root = Path(root).resolve()

    def safe(p):
        full = (root / p).resolve()
        if root not in full.parents and full != root:
            raise ValueError(f"path escapes workspace: {p}")
        return full

    def read_file(path):
        return safe(path).read_text(encoding="utf-8", errors="replace")

    def list_dir(path="."):
        return "\n".join(sorted(
            p.name + ("/" if p.is_dir() else "") for p in safe(path).iterdir() if p.name not in (".git", "__pycache__")))

    def write_file(path, content):
        f = safe(path)
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(content, encoding="utf-8")
        return f"wrote {len(content)} chars to {path}"

    def run_cmd(cmd):
        p = subprocess.run(cmd, shell=True, cwd=root, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=90)
        return f"exit={p.returncode}\n{p.stdout}{p.stderr}".strip()

    tools = [
        Tool("read_file", "Read a text file (path relative to the repo root).", _obj(path="file path"), read_file),
        Tool("list_dir", "List a directory (path relative to the repo root).", _obj(path="directory path"), list_dir),
        Tool("run_cmd", "Run a shell command in the repo root and return its output.", _obj(cmd="shell command"), run_cmd),
    ]
    if not read_only:
        tools.append(Tool("write_file", "Create or overwrite a file with the given full content.",
                          _obj(path="file path", content="full file content"), write_file))
    return tools
