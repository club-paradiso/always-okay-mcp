FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.12 /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock README.md LICENSE ./
COPY src ./src
RUN uv sync --frozen --no-dev
ENV PORT=8080 HOST=0.0.0.0
EXPOSE 8080
CMD ["uv", "run", "--no-dev", "always-okay-mcp-http"]
