"""Session 4: a real MCP server (JSON-RPC 2.0 over stdio, newline-delimited) over the ticket fixture.
Design rules: small outputs, pagination, errors that tell the agent what to do next."""
import json
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "fixtures" / "tickets.json"
PAGE_MAX = 10

TOOLS = [
    {"name": "search_tickets",
     "description": "Search tickets by text/status/release. Returns a short page of {id,title,status}; use get_ticket for details.",
     "inputSchema": {"type": "object", "properties": {
         "query": {"type": "string", "description": "substring of the title"},
         "status": {"type": "string", "enum": ["open", "in_progress", "blocked", "done"]},
         "release": {"type": "string", "description": "e.g. R-1.0"},
         "page": {"type": "integer", "description": "1-based page, default 1"},
         "page_size": {"type": "integer", "description": f"default 5, max {PAGE_MAX}"}}}},
    {"name": "get_ticket",
     "description": "Get one ticket by id (e.g. T-103) with full details including blocked_by.",
     "inputSchema": {"type": "object", "properties": {"id": {"type": "string"}}, "required": ["id"]}},
    {"name": "list_blockers",
     "description": "List unfinished tickets in a release that are blocked, with the open tickets blocking them. Answers 'what is blocking release X?'.",
     "inputSchema": {"type": "object", "properties": {
         "release": {"type": "string", "description": "e.g. R-1.0"},
         "page": {"type": "integer"}}, "required": ["release"]}},
]


class ToolError(Exception):
    def __init__(self, code, message, hint):
        self.payload = {"error": {"code": code, "message": message, "hint": hint}}


def load():
    return {t["id"]: t for t in json.loads(DATA.read_text())["tickets"]}


def paginate(items, page, size):
    size = max(1, min(int(size or 5), PAGE_MAX))
    page = max(1, int(page or 1))
    total_pages = max(1, -(-len(items) // size))
    if page > total_pages:
        raise ToolError("page_out_of_range", f"page {page} > {total_pages}", f"use page between 1 and {total_pages}")
    return items[(page - 1) * size: page * size], {"page": page, "total_pages": total_pages, "total": len(items)}


def search_tickets(query=None, status=None, release=None, page=1, page_size=5):
    ts = list(load().values())
    if query:
        ts = [t for t in ts if query.lower() in t["title"].lower()]
    if status:
        ts = [t for t in ts if t["status"] == status]
    if release:
        ts = [t for t in ts if t["release"] == release]
    chunk, meta = paginate(ts, page, page_size)
    return {"items": [{"id": t["id"], "title": t["title"], "status": t["status"]} for t in chunk], **meta}


def get_ticket(id):
    t = load().get(id)
    if not t:
        raise ToolError("not_found", f"no ticket {id!r}", "call search_tickets to find valid ids (format T-123)")
    return t


def list_blockers(release, page=1):
    ts = load()
    if release not in {t["release"] for t in ts.values()}:
        raise ToolError("unknown_release", f"no release {release!r}",
                        "valid releases: " + ", ".join(sorted({t['release'] for t in ts.values()})))
    rows = []
    for t in ts.values():
        if t["release"] == release and t["status"] != "done":
            open_blockers = [{"id": b, "title": ts[b]["title"], "status": ts[b]["status"]}
                             for b in t["blocked_by"] if b in ts and ts[b]["status"] != "done"]
            if open_blockers:
                rows.append({"ticket": t["id"], "title": t["title"], "blocked_by": open_blockers})
    chunk, meta = paginate(rows, page, 5)
    return {"release": release, "blocked": chunk, **meta}


IMPL = {"search_tickets": search_tickets, "get_ticket": get_ticket, "list_blockers": list_blockers}


def handle(msg):
    method, mid = msg.get("method"), msg.get("id")
    if mid is None:  # notification
        return None
    if method == "initialize":
        result = {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}},
                  "serverInfo": {"name": "shelfy-tickets", "version": "0.1"}}
    elif method == "tools/list":
        result = {"tools": TOOLS}
    elif method == "tools/call":
        p = msg["params"]
        try:
            fn = IMPL[p["name"]]
            out, err = fn(**(p.get("arguments") or {})), False
        except ToolError as e:
            out, err = e.payload, True
        except (KeyError, TypeError) as e:
            out, err = {"error": {"code": "bad_request", "message": str(e),
                                  "hint": "check the tool's inputSchema"}}, True
        result = {"content": [{"type": "text", "text": json.dumps(out)}], "isError": err}
    else:
        return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"unknown method {method}"}}
    return {"jsonrpc": "2.0", "id": mid, "result": result}


def main():
    for line in sys.stdin:
        if line.strip():
            reply = handle(json.loads(line))
            if reply:
                print(json.dumps(reply), flush=True)


if __name__ == "__main__":
    main()
