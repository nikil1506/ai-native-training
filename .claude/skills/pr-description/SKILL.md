---
name: pr-description
description: Write a pull request description (summary, risk, test plan, rollback) for a branch or git range. Use when asked to write, draft or generate a PR body or PR description. Not for commit messages, code review, or release notes.
---

# PR description writer

1. Run `python .claude/skills/pr-description/scripts/diff_stats.py <range>` (range like `main..branch` or `v1..v2`; default `main..HEAD`).
2. Read `.claude/skills/pr-description/references/pr_template.md` and follow it exactly.
3. Base every claim on the script output. Name the files that changed. If a risk is unclear, say "low" and why.
4. Reply with ONLY the finished PR body in markdown, nothing before or after it.
