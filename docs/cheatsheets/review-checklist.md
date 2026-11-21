# Review checklist (A1 checkpoint and everyday use)
Review the diff, not the description. For every changed hunk ask:
1. **Does it do what the ticket asked, and only that?** Compare against each acceptance criterion. Unrequested changes (renames, deletions, reformatting)?
2. **Edge cases:** empty input, zero, None, huge input, duplicates, concurrency. What happens at the boundary?
3. **Do the APIs exist?** Check every library call against the docs; agents invent plausible-looking functions and parameters.
4. **Unsafe defaults:** disabled TLS verification, `shell=True`, debug on, permissive permissions, overwrite-by-default, secrets in code.
5. **Do the tests prove anything?** Is there an assertion? Would the test fail if the code were wrong? Does it cover the edge cases from (2)?
6. **Blast radius:** who else imports what was renamed/removed? Search for usages.
7. **Security and data:** input validation, logging of sensitive data, new dependencies.
8. **Decision:** merge / rework. Write each finding as: ID, severity (high/medium/low), location, issue, fix. Rank by severity.
