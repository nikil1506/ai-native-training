---
name: changelog
description: Generate user-facing release notes or a changelog from the merged pull requests between two git tags. Use when asked for release notes, a changelog, or what's new between versions. Not for a single PR description or code review.
---

# Changelog / release notes

1. Run `python .claude/skills/changelog/scripts/parse_tags.py <from_tag> <to_tag>` to list merged PRs.
2. Read `.claude/skills/changelog/references/style.md`.
3. Group entries under `### Added`, `### Fixed`, `### Changed` (omit empty groups). Write for end users, one line each, no PR numbers' branch names, no commit hashes.
4. Start with the heading `## <to_tag>`. Reply with ONLY the release notes.
