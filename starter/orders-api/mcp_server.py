"""L7 task 2: expose your tools through MCP (JSON-RPC over stdio). Template: finish the TODOs.
Reference for the protocol: harness/mcp_server.py (a complete example over a different dataset)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools import build_tools  # noqa: E402  (run with: python starter/orders-api/mcp_server.py)


def main():
    tools = {t.name: t for t in build_tools()}
    for line in sys.stdin:
        msg = json.loads(line)
        mid, method = msg.get("id"), msg.get("method")
        if mid is None:
            continue
        if method == "initialize":
            result = {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "serverInfo": {"name": "orders", "version": "0.1"}}
        elif method == "tools/list":
            result = {"tools": []}  # TODO: one entry per tool: {"name","description","inputSchema"}
        elif method == "tools/call":
            result = {"content": [{"type": "text", "text": "TODO: call the tool and json.dumps the result"}], "isError": False}
        else:
            result = {}
        print(json.dumps({"jsonrpc": "2.0", "id": mid, "result": result}), flush=True)


if __name__ == "__main__":
    main()
