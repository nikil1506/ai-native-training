"""Minimal MCP stdio client + adapter that exposes MCP tools as agent Tools."""
import json
import subprocess
import sys

from . import config
from .agent import Tool


class MCPClient:
    def __init__(self, cmd=None):
        self.p = subprocess.Popen(cmd or [sys.executable, "-m", "harness.mcp_server"], cwd=config.REPO,
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, encoding="utf-8")
        self._id = 0
        self._rpc("initialize", {"protocolVersion": "2024-11-05", "capabilities": {},
                                 "clientInfo": {"name": "harness", "version": "0.1"}})
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def _send(self, msg):
        self.p.stdin.write(json.dumps(msg) + "\n")
        self.p.stdin.flush()

    def _rpc(self, method, params=None):
        self._id += 1
        self._send({"jsonrpc": "2.0", "id": self._id, "method": method, "params": params or {}})
        reply = json.loads(self.p.stdout.readline())
        if "error" in reply:
            raise RuntimeError(reply["error"]["message"])
        return reply["result"]

    def list_tools(self):
        return self._rpc("tools/list")["tools"]

    def call(self, name, arguments):
        r = self._rpc("tools/call", {"name": name, "arguments": arguments})
        return r["content"][0]["text"]

    def close(self):
        self.p.stdin.close()
        self.p.wait(timeout=5)


def mcp_tools(client):
    return [Tool(t["name"], t["description"], t["inputSchema"],
                 (lambda n: lambda **kw: client.call(n, kw))(t["name"])) for t in client.list_tools()]
