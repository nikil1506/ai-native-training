# Answer key: branch review-lab/seeded-bugs (one commit per bug)
1. orders.py: bare `except:` swallows errors (standard 2)
2. config.py: hardcoded API key (standard 4)
3. notify.py: logs customer email (standard 3)
4. reports.py: SQL built by string concatenation (standard 4)
5. inventory.py: `remove` allows negative stock via `<=` guard removed (standard 5)
Decoys (must NOT be flagged): long line in reports.py, unused import in notify.py.
