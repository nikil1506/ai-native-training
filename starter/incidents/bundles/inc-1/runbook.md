# Checkout runbook
- If error rate >5%: check recent deploys, then DB connection pool, then upstream dependencies.
- Rollback with `deployctl rollback checkout-service`.
