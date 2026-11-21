---
name: code-review
description: Review a git diff, branch or git range against the team's coding standards and report concrete violations with file names. Use when asked to review code, a diff, a branch or a PR for bugs, security or standards. Not for writing PR descriptions, commit messages or release notes.
---

# Code review against team standards

1. Run `python .claude/skills/code-review/scripts/changed_files.py <range>` (default `main..HEAD`) to get the diff.
2. Read `.claude/skills/code-review/references/standards.md`.
3. Check each changed hunk against the numbered standards. Do NOT flag anything listed as linter-covered.
4. Reply with one line per real violation: `- [standard N] path: what is wrong and the fix`. Only report violations visible in the diff.
5. If there are none, reply exactly `No violations.`
