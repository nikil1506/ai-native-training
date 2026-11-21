"""Deterministic work belongs in scripts: gather commits and per-file stats for a git range."""
import subprocess
import sys


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, encoding="utf-8").stdout.strip()


def main(rng):
    a, _, b = rng.partition("..")
    base = git("merge-base", a, b or "HEAD") or a
    head = b or "HEAD"
    print(f"RANGE {a}..{head} (merge-base {base[:8]})")
    print("COMMITS:")
    print(git("log", "--no-merges", "--format=- %s", f"{base}..{head}") or "- (none)")
    print("FILES (added/removed/path):")
    print(git("diff", "--numstat", base, head) or "(no changes)")
    print("SHORTSTAT:", git("diff", "--shortstat", base, head) or "none")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "main..HEAD")
