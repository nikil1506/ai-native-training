"""Mock REST API with SIX endpoints (one destructive). In-process: call(method, path, body) -> (status, json).
Run as a real server too:  python starter/orders-api/api.py  (port 8790)."""
import json
import re
from http.server import BaseHTTPRequestHandler, HTTPServer

DB = {}


def reset():
    DB.clear()
    DB.update({
        "1001": {"id": "1001", "customer": "ana@example.com", "status": "paid", "total": 59.90, "address": "12 Oak St", "items": ["lamp", "bulb"]},
        "1002": {"id": "1002", "customer": "raj@example.com", "status": "shipped", "total": 120.00, "address": "9 Pine Rd", "items": ["desk"]},
        "1003": {"id": "1003", "customer": "ana@example.com", "status": "pending", "total": 15.00, "address": "12 Oak St", "items": ["mug"]},
        "1004": {"id": "1004", "customer": "lee@example.com", "status": "delivered", "total": 300.00, "address": "3 Elm Ave", "items": ["chair", "chair"]},
    })


reset()


def call(method, path, body=None):
    body = body or {}
    if method == "GET" and path.startswith("/orders") and "?" in path:                      # 1 list/filter
        q = dict(p.split("=") for p in path.split("?", 1)[1].split("&"))
        rows = [o for o in DB.values() if all(str(o.get(k)) == v for k, v in q.items())]
        return 200, rows
    if method == "GET" and path == "/orders":                                                # 1 list
        return 200, list(DB.values())
    m = re.fullmatch(r"/orders/(\w+)", path)
    if m:
        oid = m.group(1)
        if oid not in DB:
            return 404, {"error": "order not found"}
        if method == "GET":                                                                  # 2 get
            return 200, DB[oid]
        if method == "DELETE":                                                               # 3 DESTRUCTIVE
            return 200, DB.pop(oid)
    m = re.fullmatch(r"/orders/(\w+)/(address|status|refund)", path)
    if m and m.group(1) in DB and method in ("PUT", "POST"):
        o, what = DB[m.group(1)], m.group(2)
        if what == "address":                                                                # 4 update address
            if o["status"] in ("shipped", "delivered"):
                return 409, {"error": "cannot change address after shipping"}
            o["address"] = body["address"]; return 200, o
        if what == "status":                                                                 # 5 admin status override
            o["status"] = body["status"]; return 200, o
        if what == "refund":                                                                 # 6 refund
            o["status"] = "refunded"; return 200, o
    return 404, {"error": "no such endpoint"}


class H(BaseHTTPRequestHandler):
    def _go(self):
        n = int(self.headers.get("Content-Length") or 0)
        code, out = call(self.command, self.path, json.loads(self.rfile.read(n) or b"{}"))
        data = json.dumps(out).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)
    do_GET = do_POST = do_PUT = do_DELETE = _go

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print("orders-api on http://127.0.0.1:8790")
    HTTPServer(("127.0.0.1", 8790), H).serve_forever()
