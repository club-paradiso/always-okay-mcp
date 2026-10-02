"""Protocol-level smoke test: launch the server over stdio and exercise tools via an MCP client."""
import anyio
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


async def main():
    params = StdioServerParameters(command="uv", args=["run", "always-okay-mcp"])
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            init = await s.initialize()
            print("server:", init.server_info.name, init.server_info.version)
            tools = await s.list_tools()
            print("tools:", sorted(t.name for t in tools.tools))
            res = await s.call_tool("get_principle", {"principle_id": "P24"})
            print("P24:", str(res.content[0].text)[:160])
            res = await s.call_tool("check_draft", {"text": "프리미엄 힐링 경험, 레트로 감성"})
            print("lint:", str(res.content[0].text)[:200])
            prompts = await s.list_prompts()
            print("prompts:", [p.name for p in prompts.prompts])

anyio.run(main)
