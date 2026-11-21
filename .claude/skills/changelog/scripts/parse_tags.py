"""List merged PRs between two tags as JSON-ish lines. Deterministic parsing, no model needed."""
import json
import re
import subprocess
import sys


def main(a, b):
    out = subprocess.run(["git", "log", "--merges", "--format=%s", f"{a}..{b}"],
                         capture_output=True, text=True, encoding="utf-8").stdout
    prs = []
    for line in out.splitlines():
        m = re.match(r"Merge pull request #(\d+) from (\S+?):? (?:.*?: )?(.*)", line) or \
            re.match(r"Merge pull request #(\d+) from (\S+)", line)
        if m:
            g = m.groups()
            prs.append({"number": int(g[0]), "branch": g[1].rstrip(":"), "title": g[2] if len(g) > 2 else ""})
    direct = subprocess.run(["git", "log", "--no-merges", "--first-parent", "--format=%s", f"{a}..{b}"],
                            capture_output=True, text=True, encoding="utf-8").stdout.splitlines()
    print(json.dumps({"from": a, "to": b, "merged_prs": prs, "direct_commits": direct}, indent=2))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
