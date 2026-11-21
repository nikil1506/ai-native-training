# Team coding standards (shelfy)

1. **Naming:** snake_case functions, PascalCase classes, no single-letter names outside comprehensions.
2. **Errors:** raise specific exceptions with a message; never use bare `except:`; never swallow errors silently.
3. **Logging:** use `logging`, not `print`. Never log PII (emails, names, addresses).
4. **Security:** no secrets in source; parameterized SQL only; validate all external input.
5. **Stock invariants:** inventory quantities never go negative.
6. **Linter-covered (do not flag):** line length, unused imports, import order.
