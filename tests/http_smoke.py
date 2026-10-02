"""Remote smoke test: python tests/http_smoke.py [URL] (default http://localhost:8765/mcp)."""
import sys, anyio
from mcp.client.session import ClientSession
import mcp.client.streamable_http as sh

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8765/mcp"
client = getattr(sh, "streamable_http_client", None) or getattr(sh, "streamablehttp_client")

async def main():
    async with client(URL) as streams:
        r, w = streams[0], streams[1]
        async with ClientSession(r, w) as s:
            i = await s.initialize()
            t = await s.list_tools()
            res = await s.call_tool("trace", {"item_id": "P21"})
            print(i.server_info.name, len(t.tools), "tools;", str(res.content[0].text)[:120].replace("\n", " "))

anyio.run(main)
