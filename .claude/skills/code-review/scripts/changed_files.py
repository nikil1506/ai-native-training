"""Print changed files and the unified diff for a git range."""
import subprocess
import sys


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, encoding="utf-8").stdout


def main(rng):
    a, _, b = rng.partition("..")
    head = b or "HEAD"
    base = git("merge-base", a, head).strip() or a
    print("CHANGED FILES:")
    print(git("diff", "--name-status", base, head))
    print("DIFF:")
    print(git("diff", "-U2", base, head))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "main..HEAD")
