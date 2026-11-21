"""`make doctor`: confirms your setup works before Day 1. Exit code 0 = ready."""
import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
ok_all = True


def check(name, ok, hint=""):
    global ok_all
    ok_all &= bool(ok)
    print(f"[{'ok' if ok else 'FAIL'}] {name}" + ("" if ok else f"  -> {hint}"))


check("Python 3.11+", sys.version_info >= (3, 11), f"found {sys.version.split()[0]}; install Python 3.11 or newer")
check("git installed", shutil.which("git"), "install Git")
try:
    from harness import config, llm
    tags = json.loads(urllib.request.urlopen(config.HOST + "/api/tags", timeout=5).read())["models"]
    names = [m["name"] for m in tags]
    check(f"model server reachable at {config.HOST}", True)
    small = __import__("os").environ.get("SMALL_MODEL", "qwen3.5:latest")
    check(f"small model '{small}' is pulled", small in names, f"run: ollama pull {small}")
    r = llm.chat([{"role": "user", "content": "Reply with the single word: ready"}], model=small, timeout=180)
    check("API key/model call works (got a reply)", bool(r["message"]["content"].strip()), "model returned nothing")
except Exception as e:
    check("model server reachable", False, f"{type(e).__name__}: {e}. Start Ollama, or set OLLAMA_HOST (gateway URL)")
r = subprocess.run([sys.executable, "-m", "unittest", "discover", "tests"], cwd=ROOT, capture_output=True, text=True)
check("repo unit tests pass", r.returncode == 0, r.stderr[-300:])
for d in ("l1", "bugfix-repo", "l3", "orders-app", "orders-api", "support-agent", "policy-corpus", "eval",
          "incidents", "vulnerable-agent", "sample-repo-2", "backlog", "capstone-scaffold"):
    check(f"starter/{d} present", (ROOT / "starter" / d).is_dir(), "re-clone the repository")
import re
check("no API key committed", not any(
    re.search(r"sk-(?!FAKE)[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}", f.read_text(errors="ignore")) for f in ROOT.glob("**/*.py") if ".git" not in f.parts),
    "remove keys from code; use env vars")
print("\nREADY" if ok_all else "\nNOT READY: fix the FAIL lines above")
sys.exit(0 if ok_all else 1)
