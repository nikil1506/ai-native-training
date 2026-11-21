"""Programme guards (offline, no model): starters must FAIL where they are exercises, reference solutions must PASS,
and the repo must cover everything the guide names."""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable


def run(args, cwd, env=None):
    e = {**os.environ, **(env or {})}
    return subprocess.run([PY, *args], cwd=cwd, capture_output=True, text=True, env=e, timeout=120).returncode


def overlay(starter_dir, solution_file, target_rel, replacements=()):
    tmp = Path(tempfile.mkdtemp()) / "lab"
    shutil.copytree(ROOT / starter_dir, tmp, ignore=shutil.ignore_patterns("__pycache__", "runs", "index_*.json"))
    text = (ROOT / solution_file).read_text(encoding="utf-8")
    for a, b in replacements:
        text = text.replace(a, b)
    (tmp / target_rel).write_text(text, encoding="utf-8")
    return tmp


class Starters(unittest.TestCase):
    def test_starters_are_real_exercises(self):
        self.assertNotEqual(run(["-m", "unittest", "discover", "tests"], ROOT / "starter/bugfix-repo"), 0)
        self.assertNotEqual(run(["-m", "unittest", "discover", "starter/l3"], ROOT), 0)
        self.assertNotEqual(run(["-m", "unittest", "discover", "starter/support-agent"], ROOT), 0)
        self.assertNotEqual(run(["-m", "unittest", "starter/vulnerable-agent/test_hardening.py"], ROOT), 0)

    def test_untouched_starters_pass(self):
        for d in ("orders-app", "sample-repo-2"):
            self.assertEqual(run(["-m", "unittest", "discover", "tests"], ROOT / "starter" / d), 0, d)


class Solutions(unittest.TestCase):
    def test_l2_solution(self):
        t = overlay("starter/bugfix-repo", "facilitator/solutions/bugfix-repo/cart.py", "service/cart.py")
        self.assertEqual(run(["-m", "unittest", "discover", "tests"], t), 0)

    def test_l3_solution(self):
        root = repr(str(ROOT))
        t = overlay("starter/l3", "facilitator/solutions/l3/agent.py", "agent.py",
                    [("Path(__file__).resolve().parents[3]", f"Path({root})")])
        self.assertEqual(run(["-m", "unittest", "discover", "."], t), 0)

    def test_l8_solution(self):
        root = repr(str(ROOT))
        t = overlay("starter/support-agent", "facilitator/solutions/support-agent/agent.py", "agent.py",
                    [('next(p for p in Path(__file__).resolve().parents if (p / "harness").is_dir())', f"Path({root})")])
        self.assertEqual(run(["-m", "unittest", "discover", "."], t), 0)

    def test_l14_hardened_solution(self):
        rc = run(["-m", "unittest", "starter/vulnerable-agent/test_hardening.py"], ROOT,
                 {"AGENT": str(ROOT / "facilitator/solutions/vulnerable-agent/hardened.py")})
        self.assertEqual(rc, 0)


class Coverage(unittest.TestCase):
    def test_guide_fully_covered(self):
        self.assertEqual(run(["scripts/check_coverage.py"], ROOT), 0)


if __name__ == "__main__":
    unittest.main()
