"""Remote (Streamable HTTP) entry point for ChatGPT, claude.ai and other URL-based MCP clients.

  always-okay-mcp-http            # serves http://0.0.0.0:$PORT/mcp

Environment:
  PORT            listen port (default 8000)
  HOST            bind address (default 0.0.0.0)
  ALLOWED_HOSTS   comma-separated Host headers to accept (e.g. "always-okay.fly.dev").
                  Empty = DNS-rebinding protection off; acceptable only because every tool is
                  read-only and the server holds no user data or credentials.
  RATE_LIMIT      requests per minute per client IP on /mcp (default 120)

The server is stateless (no sessions are kept between requests) and returns JSON responses.
"""
from __future__ import annotations

import os
import time
from collections import defaultdict, deque

import uvicorn
from mcp.server.transport_security import TransportSecuritySettings
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Mount, Route

from .server import server

RATE = int(os.environ.get("RATE_LIMIT", "120"))


class RateLimit:
    """Sliding-window limit per client IP, applied to the MCP endpoint only."""

    def __init__(self, app, per_minute: int):
        self.app, self.per_minute = app, per_minute
        self.hits: dict[str, deque] = defaultdict(deque)

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and scope["path"].startswith("/mcp") and self.per_minute > 0:
            headers = dict(scope.get("headers") or [])
            fwd = headers.get(b"fly-client-ip") or headers.get(b"x-forwarded-for", b"").split(b",")[0]
            ip = (fwd.decode().strip() if fwd else "") or (scope.get("client") or ("?",))[0]
            now, q = time.monotonic(), self.hits[ip]
            while q and now - q[0] > 60:
                q.popleft()
            if len(q) >= self.per_minute:
                resp = JSONResponse({"error": "rate limit exceeded; try again in a minute"}, status_code=429,
                                    headers={"Retry-After": "60"})
                return await resp(scope, receive, send)
            q.append(now)
        return await self.app(scope, receive, send)


def build_app() -> Starlette:
    hosts = [h.strip() for h in os.environ.get("ALLOWED_HOSTS", "").split(",") if h.strip()]
    security = (TransportSecuritySettings(enable_dns_rebinding_protection=True, allowed_hosts=hosts,
                                          allowed_origins=["https://chatgpt.com", "https://claude.ai",
                                                           *[f"https://{h}" for h in hosts]])
                if hosts else TransportSecuritySettings(enable_dns_rebinding_protection=False))
    mcp_app = server.streamable_http_app(streamable_http_path="/mcp", stateless_http=True, json_response=True,
                                         transport_security=security, host="0.0.0.0")

    async def health(_: Request):
        return JSONResponse({"name": "always-okay", "status": "ok", "mcp_endpoint": "/mcp",
                             "note": "Independent research; not affiliated with Min Hee-jin or ooak records."})

    async def robots(_: Request):
        return PlainTextResponse("User-agent: *\nDisallow: /mcp\n")

    app = Starlette(routes=[Route("/", health), Route("/healthz", health), Route("/robots.txt", robots),
                            Mount("/", app=mcp_app)],
                    middleware=[Middleware(RateLimit, per_minute=RATE)],
                    lifespan=mcp_app.router.lifespan_context)
    return app


def main() -> None:
    uvicorn.run(build_app(), host=os.environ.get("HOST", "0.0.0.0"), port=int(os.environ.get("PORT", "8000")),
                proxy_headers=True, forwarded_allow_ips="*")


if __name__ == "__main__":
    main()
