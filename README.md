# always-okay

**A creative-direction lens reconstructed from 125 public records of Min Hee-jin's professional work**
(interviews, talks, credits and collaborator accounts, 2002–2026), **that you can plug into ChatGPT,
Claude or Codex.** 32 principles, each traced to its sources. It helps you turn a
rough brief into a sharp concept, a brand idea, a launch plan or an honest critique — and it can show
you the public evidence behind every piece of advice.

> **Not affiliated with, endorsed by, or connected to Min Hee-jin or ooak records (주식회사 오케이).**
> Independent research. It models *documented professional reasoning* from public interviews, talks,
> credits and collaborator accounts. It never speaks as her, never invents her opinions or quotes,
> and never copies her look.

👉 **한국어 사용법은 [아래](#한국어-처음-쓰는-분을-위한-사용법)에 있습니다.**

---

## What you get, in one picture

You describe your project. The AI, using always-okay, works in four steps:

1. **Frame** — finds the real problem and questions vague words like "trendy" or "premium".
2. **Make** — proposes **one memorable idea built from your own material** (a "signature device"),
   and shows how it appears in the product, the launch, the copy and the visuals.
3. **Edit** — removes what doesn't serve that idea.
4. **Deliver** — tells you what to do first, what to wait on, and what never to do.

Ask "why?" and it shows the principle and the public source it comes from.

---

## Start here (no coding needed)

### Easiest: paste a link (no setup)
Works in any AI that can open web links (ChatGPT with search, Claude with web access, Gemini, …).
Paste this into a chat, then describe your project:

```
Read this page and use its method to help with my project: https://raw.githubusercontent.com/club-paradiso/always-okay-mcp/master/ALWAYS-OKAY.md
```

This gives the AI the whole method in one page. It is lighter than connecting the server: the AI
can't look up the sources behind each principle, and if web access is off it can't open the link at
all (then attach the file `ALWAYS-OKAY.md` instead). For the full version, connect it as below.

### Full version: connect the server
You only need one thing: this address.

```
https://always-okay-mcp.onrender.com/mcp
```

### ChatGPT
Requires a paid ChatGPT plan that allows custom connectors (developer mode).

1. ChatGPT → **Settings** → **Apps & Connectors** → **Advanced settings** → turn on **Developer mode**.
2. Back in Apps & Connectors, click **Create**.
3. Fill in:
   - **Name:** `always-okay`
   - **MCP Server URL:** `https://always-okay-mcp.onrender.com/mcp`
   - **Authentication:** **No authentication** ← important (see Troubleshooting)
4. Tick "I trust this application" and click **Create**.
5. In a **new chat**, open the **+** menu, choose **always-okay**, and type your request.

### Claude (claude.ai or the Claude desktop app)
1. **Settings** → **Connectors** → **Add custom connector**.
2. **Name:** `always-okay` · **URL:** `https://always-okay-mcp.onrender.com/mcp` → **Add**.
3. In a new chat, make sure always-okay is switched on in the tools menu, then type your request.

### Try these first requests
- "Use always-okay. I run a small bakery in Mangwon-dong and I'm launching a sourdough line. Give me
  creative direction and a launch plan."
- "always-okay로 우리 앱 이름 후보 5개와 추천 이유를 줘. 서비스는 동네 공구 대여 앱이야."
- "Critique this landing-page copy honestly with always-okay: …(paste text)…"
- "Why do you recommend that? Show me the evidence." (it traces the principle to its sources)

---

## Troubleshooting

| What you see | What it means | Fix |
|---|---|---|
| "Couldn't discover OAuth settings" | The connector was created with **OAuth** selected. always-okay has no login. | Recreate it with **Authentication: No authentication**. |
| Connector creation times out / first answer is slow | The free server sleeps when idle and needs ~30 s to wake up. | Wait a moment and try again. |
| You can't find "Create" or "Developer mode" in ChatGPT | Custom connectors aren't available on your plan or workspace. | Use Claude instead, or a plan that supports custom connectors. |
| The AI answers but never uses always-okay | The connector isn't enabled for that chat. | Start a new chat and enable always-okay from the **+** / tools menu, or say "use always-okay". |
| The AI says it can't open the link | Web access is off in that chat or app. | Turn on search/web access, or download `ALWAYS-OKAY.md` and attach the file. |
| "Rate limit exceeded" | More than 120 requests per minute from your network. | Wait a minute. |

---

## For developers

### Claude Code
```bash
claude mcp add always-okay -- uvx --from git+https://github.com/club-paradiso/always-okay-mcp always-okay-mcp
```

### Codex (skill + MCP in one plugin)
```bash
codex plugin marketplace add club-paradiso/always-okay-mcp
codex plugin add always-okay@club-paradiso
```
Start a new thread afterwards so Codex picks up the skill and tools.

### Any MCP client
Local (stdio): `uvx --from git+https://github.com/club-paradiso/always-okay-mcp always-okay-mcp`
· Remote (Streamable HTTP): `https://always-okay-mcp.onrender.com/mcp`

### Tools (all read-only)
| Tool | What it does |
|---|---|
| `get_framework` | The Frame → Make → Edit → Deliver loop, 8 stages, all principles with evidence strength |
| `get_principle` | One principle: rule, limits, what it guards against, tensions, support, claim IDs |
| `search_evidence` | Search paraphrased evidence notes by text, domain or era, with source metadata |
| `trace` | Principle or claim → evidence notes → public sources (URLs, dates) |
| `list_tensions` | Contradictions and myths the lens keeps open |
| `get_mode` | 10 working modes (strategist, creative director, critic, launch director, …) |
| `get_checklist` | Brief, concept, signature-device, edit, launch, briefing, convention, taste, language, limits |
| `check_draft` | Deterministic lint (KO/EN): declared quality, filler, template phrasing, borrowed tropes, persona leaks |
| `search`, `fetch` | OpenAI-connector-compatible search over principles, notes, tensions and checklists |

Prompt: `creative_direction(brief)`.

`ALWAYS-OKAY.md` (single-file edition) is generated from the Skill: `python3 tools/build_paste_guide.py` (the test suite fails if it is stale). `llms.txt` points assistants to it.

### Self-hosting
```bash
uv run always-okay-mcp-http          # http://localhost:8000/mcp
```
Deploy with the included `Dockerfile` (`render.yaml` for Render, `fly.toml` for Fly.io).
Environment: `PORT`, `ALLOWED_HOSTS` (public hostname; enables DNS-rebinding protection),
`RATE_LIMIT` (requests/minute/IP, default 120). Health check: `GET /healthz`.

### Development
```bash
uv sync && uv run pytest -q && uv run python tests/stdio_smoke.py
```

---

## How it was made, and how well it works
32 principles of creative direction, each traced through claims and paraphrased evidence notes to
public sources (125 sources, 598 notes, 164 claims, 44 documented tensions).

In a blind evaluation on 30 creative-direction tasks, the lens (as a Claude Agent Skill) was ranked
first on 26/30 and 25/30 cases by two independent judge panels, ahead of a strong generic
"world-class creative director" prompt. Judges were AI models of the same family as the generators;
a human panel has not yet been run.

## Rules the server tells every assistant
Never speak as or for her · method is not output (no Y2K/retro/NewJeans defaults) · principles are
defaults with tensions · accuracy and official wording first in public, legal, financial, health or
safety contexts · no private life, gossip or dispute commentary.

## Data
`src/always_okay_mcp/data/` is a snapshot exported from the research repository: paraphrased notes,
source metadata and URLs only — no article text, transcripts or media. Dispute-record material is
excluded. Copyright in the underlying sources remains with their publishers.

## License
Code: MIT. Research data (principles, claims, paraphrased notes): CC BY 4.0. See `LICENSE`.

---

## 한국어: 처음 쓰는 분을 위한 사용법

### 이게 뭔가요?
**민희진의 공개 인터뷰·강연·크레딧·협업자 증언 등 공개 기록 125건을 분석해 재구성한 크리에이티브 디렉션 도우미**입니다. ChatGPT나 Claude에 연결해서 씁니다. 원칙 32개는 모두 출처까지 추적할 수 있습니다. 대충 적은 기획을 선명한
콘셉트, 브랜드 아이디어, 런칭 계획, 솔직한 크리틱으로 바꿔 줍니다. "왜 그렇게 추천해?"라고 물으면 그
조언의 근거가 된 원칙과 공개 출처까지 보여 줍니다.

> 민희진 및 ooak records(주식회사 오케이)와 무관하며 승인받지 않은 독립 연구입니다. 본인을 흉내 내거나
> 본인의 의견·말투·스타일을 만들어내지 않습니다.

### 이렇게 일해요 (4단계)
1. **정리하기:** 진짜 문제가 무엇인지 찾고, "트렌디하게", "프리미엄하게" 같은 막연한 말을 구체적으로 바꿉니다.
2. **만들기:** **당신의 재료에서 나온 기억에 남는 아이디어 하나**를 제안하고, 그게 제품·런칭·문구·비주얼에
   어떻게 나타나는지 보여 줍니다.
3. **덜어내기:** 그 아이디어에 도움이 안 되는 것을 뺍니다.
4. **실행하기:** 먼저 할 것, 나중에 할 것, 하지 말 것을 정리해 줍니다.

### 가장 쉬운 방법: 링크만 붙여 넣기 (설치 없음)
웹 링크를 열 수 있는 AI라면 어디서든 돼요(검색이 켜진 ChatGPT, 웹 접근이 되는 Claude, Gemini 등).
채팅창에 아래 문장을 붙여 넣고, 이어서 내 프로젝트를 설명하세요.

```
이 페이지를 읽고, 그 방법대로 내 프로젝트를 도와줘: https://raw.githubusercontent.com/club-paradiso/always-okay-mcp/master/ALWAYS-OKAY.md
```

방법 전체가 한 페이지에 들어 있어서 링크 하나로 충분해요. 다만 서버 연결보다는 기능이 적어요. 원칙마다 근거 출처를 찾아보는 기능은 없고, 웹 접근이 꺼져 있으면 링크를 열지 못해요. 그럴 때는 `ALWAYS-OKAY.md` 파일을 내려받아 채팅에 첨부하세요. 모든 기능을 쓰려면 아래처럼 연결하세요.

### 모든 기능 쓰기: 서버 연결 (준비물은 주소 하나)
```
https://always-okay-mcp.onrender.com/mcp
```

### ChatGPT에서 쓰기
커스텀 커넥터(개발자 모드)를 쓸 수 있는 유료 플랜이 필요합니다.

1. ChatGPT → **설정** → **앱 및 커넥터(Apps & Connectors)** → **고급 설정** → **개발자 모드** 켜기
2. 앱 및 커넥터 화면에서 **만들기(Create)** 누르기
3. 다음처럼 입력:
   - **이름:** `always-okay`
   - **MCP 서버 URL:** `https://always-okay-mcp.onrender.com/mcp`
   - **인증:** **인증 없음(No authentication)** ← 꼭 이걸로!
4. "이 애플리케이션을 신뢰합니다"에 체크하고 **만들기**
5. **새 채팅**을 열고 입력창의 **+** 메뉴에서 **always-okay**를 선택한 뒤 요청을 입력

### Claude에서 쓰기 (웹·데스크톱 앱)
1. **설정** → **커넥터(Connectors)** → **사용자 지정 커넥터 추가**
2. **이름:** `always-okay` · **URL:** `https://always-okay-mcp.onrender.com/mcp` → **추가**
3. 새 채팅에서 도구 메뉴에 always-okay가 켜져 있는지 확인하고 요청 입력

### 처음 해볼 만한 요청
- "always-okay로 도와줘. 망원동에서 작은 빵집을 하는데 사워도우 라인을 새로 내. 크리에이티브 디렉션과 런칭 계획을 짜줘."
- "always-okay로 우리 앱 이름 후보 5개와 추천 이유를 줘. 동네 공구 대여 앱이야."
- "always-okay로 이 랜딩 페이지 문구를 솔직하게 크리틱해줘: …(문구 붙여넣기)…"
- "왜 그렇게 추천했어? 근거를 보여줘."

### 잘 안 될 때
| 이런 메시지가 보이면 | 이유 | 해결 |
|---|---|---|
| "Couldn't discover OAuth settings" | 커넥터를 만들 때 인증을 **OAuth**로 골랐어요. always-okay는 로그인이 없습니다. | **인증: 인증 없음**으로 다시 만드세요. |
| 연결이 오래 걸리거나 시간 초과 | 무료 서버가 쉬고 있다가 깨어나는 데 약 30초가 걸려요. | 잠시 뒤 다시 시도하세요. |
| ChatGPT에 "만들기"나 "개발자 모드"가 안 보임 | 지금 플랜이나 워크스페이스에서 커스텀 커넥터를 쓸 수 없어요. | Claude에서 쓰거나, 커스텀 커넥터가 되는 플랜을 이용하세요. |
| 답은 하는데 always-okay를 안 씀 | 그 채팅에서 커넥터가 꺼져 있어요. | 새 채팅에서 **+** 또는 도구 메뉴로 켜거나, "always-okay를 써줘"라고 말하세요. |
| AI가 링크를 열 수 없다고 함 | 그 채팅이나 앱에서 웹 접근이 꺼져 있어요. | 검색·웹 접근을 켜거나, `ALWAYS-OKAY.md`를 내려받아 파일로 첨부하세요. |
| "Rate limit exceeded" | 같은 네트워크에서 1분에 120번 넘게 요청했어요. | 1분 뒤 다시 시도하세요. |
