# Backlog item 2: filter orders by status
As support staff I want `GET /orders?status=paid` to list only orders with that status.
Acceptance: unknown status returns 400 with a message; no filter returns everything.
