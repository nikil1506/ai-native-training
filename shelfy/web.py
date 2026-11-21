"""Tiny demo UI: `python -m shelfy` then open http://localhost:8765"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from .inventory import Inventory
from .orders import place_order

inv = Inventory()
for sku, q in [("ABC-1001", 12), ("ABC-1002", 5), ("XYZ-2001", 2)]:
    inv.add(sku, q)

PAGE = """<!doctype html><meta charset=utf-8><title>shelfy</title>
<style>body{font:16px system-ui;max-width:640px;margin:2em auto}table{border-collapse:collapse;width:100%}
td,th{border-bottom:1px solid #ddd;padding:6px;text-align:left}.low{background:#fde8e8}
input{padding:6px;margin-right:4px}button{padding:6px 10px}#msg{margin:1em 0;font-weight:600}</style>
<h1>shelfy inventory</h1>
<p>Low-stock threshold: <input id=th type=number value=5 style=width:4em onchange=load()></p>
<table><thead><tr><th>SKU<th>Qty<th></tr></thead><tbody id=rows></tbody></table>
<h3>Add stock</h3><input id=asku placeholder=ABC-1234><input id=aqty type=number value=1 style=width:4em>
<button onclick="post('/add',{sku:asku.value,qty:+aqty.value})">Add</button>
<h3>Order</h3><input id=osku placeholder=SKU><input id=oqty type=number value=1 style=width:4em>
<button onclick="order(true)">Order this item</button>
<button onclick="order(false)">Place empty order</button>
<div id=msg></div>
<script>
async function post(u,b){const r=await fetch(u,{method:'POST',body:JSON.stringify(b)});const j=await r.json();
msg.textContent=j.error?'Error: '+j.error:(j.total!==undefined?'Order total: $'+j.total.toFixed(2):'OK');load()}
function order(w){post('/order',{items:w?[[osku.value,+oqty.value,10.0]]:[]})}
async function load(){const j=await (await fetch('/stock?threshold='+th.value)).json();
rows.innerHTML=j.stock.map(s=>`<tr class="${s.low?'low':''}"><td>${s.sku}<td>${s.qty}<td>${s.low?'LOW':''}`).join('')}
load()</script>"""


class H(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        data = body.encode() if isinstance(body, str) else body
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)

    def do_GET(self):
        if self.path.startswith("/stock"):
            th = int(self.path.split("threshold=")[-1]) if "threshold=" in self.path else 5
            low = set(inv.low_stock(th))
            stock = [{"sku": s, "qty": q, "low": s in low} for s, q in sorted(inv._stock.items())]
            return self._send(200, json.dumps({"stock": stock}))
        self._send(200, PAGE, "text/html")

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])) or b"{}")
        try:
            if self.path == "/add":
                inv.add(body["sku"], body["qty"]); out = {}
            else:
                out = {"total": place_order(inv, [tuple(i) for i in body["items"]])}
            self._send(200, json.dumps(out))
        except ValueError as e:
            self._send(200, json.dumps({"error": str(e)}))

    def log_message(self, *a):
        pass


def serve(port=8765):
    print(f"shelfy on http://localhost:{port}  (Ctrl+C to stop)")
    HTTPServer(("127.0.0.1", port), H).serve_forever()
