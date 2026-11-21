import os
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RUNS = REPO / "runs"
SKILLS_DIR = REPO / ".claude" / "skills"
KILL_FILE = RUNS / "KILL"
HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
if not HOST.startswith("http"):
    HOST = "http://" + HOST
MODEL = os.environ.get("HARNESS_MODEL", "qwen3.5:latest")
