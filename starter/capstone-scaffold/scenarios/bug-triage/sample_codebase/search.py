def search(items, query, limit=10):
    q = query.lower()
    hits = [i for i in items if q in i["name"].lower()]
    return hits[:limit + 1]
