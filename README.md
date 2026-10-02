# always-okay

**An evidence-grounded creative-direction lens, as an MCP server.**

> **Not affiliated with, endorsed by, or connected to Min Hee-jin or ooak records (주식회사 오케이).**
> This is an independent research project. It models *documented professional reasoning* from public
> interviews, talks, credits and collaborator accounts. It never speaks as her, never invents her
> opinions or quotes, and never reproduces her look.

## What it is
32 principles of creative direction — framing a brief, building one concrete *signature device* from
the user's own material, editing, and planning a launch — each traced through claims and paraphrased
evidence notes to public sources (125 sources, 598 notes, 164 claims, 44 documented tensions).

In blind evaluation on 30 creative-direction tasks, the lens (as a Claude Agent Skill) was ranked first
on 26/30 and 25/30 cases by two independent judge panels, ahead of a strong generic
"world-class creative director" prompt. Method and results:
the evaluation summary below.

## Tools (all read-only)
| Tool | What it does |
|---|---|
| `get_framework` | The Frame → Make → Edit → Deliver loop, 8 stages, all principles with evidence strength |
| `get_principle` | One principle: rule, limits, what it guards against, tensions, support, claim IDs |
| `search_evidence` | Search paraphrased evidence notes by text, domain or era, with source metadata |
| `trace` | Principle or claim → evidence notes → public sources (URLs, dates) |
| `list_tensions` | Contradictions and myths the lens keeps open, per principle or by query |
| `get_mode` | 10 working modes (strategist, creative director, critic, launch director, …) |
| `get_checklist` | Brief, concept, signature-device, edit, launch, briefing, convention, taste, language, limits |
| `check_draft` | Deterministic lint (KO/EN): declared quality, filler, template phrasing, borrowed tropes, persona leaks |

Prompt: `creative_direction(brief)`.

## Install
```bash
uv tool install git+https://github.com/club-paradiso/always-okay-mcp        # or: uvx --from git+https://github.com/club-paradiso/always-okay-mcp always-okay-mcp
```
Claude Code:
```bash
claude mcp add always-okay -- uvx --from git+https://github.com/club-paradiso/always-okay-mcp always-okay-mcp
```
Any MCP client: command `always-okay-mcp` over stdio.

## Remote use: ChatGPT, claude.ai and other URL-based clients

**Public endpoint:** `https://always-okay-mcp.onrender.com/mcp` (free tier; the first request after idle can take ~30 s).
The same server runs over Streamable HTTP (stateless, JSON responses, per-IP rate limit):
```bash
uv run always-okay-mcp-http          # http://localhost:8000/mcp
```
Deploy with the included `Dockerfile` (`fly.toml` for Fly.io, `render.yaml` for Render). Then add the
public URL `https://<your-host>/mcp`:
- **claude.ai / Claude apps:** Settings → Connectors → *Add custom connector* → paste the URL.
- **ChatGPT:** Settings → Apps & Connectors → developer mode → *Create* connector → paste the URL
  (no authentication).
Environment: `PORT`, `ALLOWED_HOSTS` (public hostname; enables DNS-rebinding protection),
`RATE_LIMIT` (requests/minute/IP, default 120). Health check: `GET /healthz`.

## Rules the server tells every assistant
Never speak as or for her · method is not output (no Y2K/retro/NewJeans defaults) · principles are
defaults with tensions · accuracy and official wording first in public, legal, financial, health or
safety contexts · no private life, gossip or dispute commentary.

## Data
`src/always_okay_mcp/data/` is a snapshot exported from the research repository: paraphrased notes,
source metadata and URLs only — no article text, transcripts or media. Dispute-record material is
excluded. Copyright in the underlying sources remains with their publishers.

## Development
```bash
uv sync && uv run pytest -q && uv run python tests/stdio_smoke.py
```

## License
Code: MIT. Research data (principles, claims, paraphrased notes): CC BY 4.0. See `LICENSE`.

---

### 한국어 요약
공개된 인터뷰·강연·크레딧·협업자 증언에서 재구성한 크리에이티브 디렉션 렌즈를 MCP 서버로 제공합니다.
민희진 및 ooak records(주식회사 오케이)와 무관하며 승인받지 않은 독립 연구입니다. 본인의 목소리나
의견, 스타일을 흉내 내지 않고, 문서화된 판단 방식만 근거와 함께 제공합니다.
