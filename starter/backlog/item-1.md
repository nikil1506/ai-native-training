# Backlog item 1: export orders to CSV
As support staff I want `GET /orders.csv` to return all orders as CSV (id, customer, total_cents, status) so I can open them in a spreadsheet.
Acceptance: header row; one row per order; commas/quotes in customer names are escaped.
