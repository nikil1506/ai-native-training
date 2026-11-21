# PR #214: Add average order value to the order report  (author: coding agent)

**Summary.** Adds `average_order_value` and a weighted variant to `report.py` so the dashboard can show AOV.
Also tidies the module and makes the rates fetcher easier to use in dev environments.

**Testing.** Added tests for the new function; all tests pass (2 passed).

Acceptance criteria from the ticket: (1) AOV is the mean of order totals rounded to 2 decimals; (2) works for any list of orders.
