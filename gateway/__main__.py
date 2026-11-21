"""Shared model gateway (instructor guide: per-participant spending cap + usage dashboard).
Point labs at it with OLLAMA_HOST=http://<host>:8780 and PARTICIPANT=<name>.
Features: token caps per participant (429 when exceeded), retry once, optional fallback host, usage log + /dashboard."""
import json
import os
import sys
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

UPSTREAM = os.environ.get("UPSTREAM", "http://localhost:11434")
FALLBACK = os.environ.get("FALLBACK_UPSTREAM")          # second provider/host, used when upstream fails
CAP = int(os.environ.get("CAP_TOKENS", "500000"))       # per participant per run of the gateway
LOG = Path(os.environ.get("GATEWAY_LOG", "runs/gateway-usage.jsonl"))
usage: dict[str, int] = {}


def load_usage():
    if LOG.exists():
        for l in LOG.read_text().splitlines():
            e = json.loads(l)
            usage[e["participant"]] = usage.get(e["participant"], 0) + e["tokens"]


def forward(host, path, body):
    req = urllib.request.Request(host + path, body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return r.status, r.read()


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, code, data, ctype="application/json"):
        data = data if isinstance(data, bytes) else data.encode()
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)

    def do_GET(self):
        if self.path.startswith("/dashboard"):
            rows = "".join(f"<tr><td>{p}<td>{t}<td>{round(100 * t / CAP)}%" for p, t in sorted(usage.items(), key=lambda x: -x[1]))
            return self.send(200, f"<h1>Gateway usage (cap {CAP} tokens)</h1><table border=1 cellpadding=6><tr><th>participant<th>tokens<th>of cap{rows}</table>", "text/html")
        try:
            self.send(*forward(UPSTREAM, self.path, None)[::1])
        except Exception as e:
            self.send(502, json.dumps({"error": str(e)}))

    def do_POST(self):
        who = self.headers.get("X-Participant", "anon")
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        if usage.get(who, 0) >= CAP:
            return self.send(429, json.dumps({"error": f"token cap {CAP} reached for {who}; ask a facilitator"}))
        last = None
        for host in [UPSTREAM, UPSTREAM, FALLBACK]:      # retry once, then second provider
            if not host:
                continue
            try:
                code, data = forward(host, self.path, body)
                try:
                    j = json.loads(data)
                    t = j.get("prompt_eval_count", 0) + j.get("eval_count", 0)
                except ValueError:
                    t = 0
                usage[who] = usage.get(who, 0) + t
                LOG.parent.mkdir(parents=True, exist_ok=True)
                with open(LOG, "a") as f:
                    f.write(json.dumps({"ts": time.time(), "participant": who, "path": self.path, "tokens": t}) + "\n")
                return self.send(code, data)
            except Exception as e:
                last = e
        self.send(502, json.dumps({"error": f"upstream failed: {last}"}))


if __name__ == "__main__":
    load_usage()
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8780
    print(f"gateway on :{port} -> {UPSTREAM} (cap {CAP} tokens/participant); dashboard at /dashboard")
    ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
