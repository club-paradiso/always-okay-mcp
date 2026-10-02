"""always-okay: an evidence-grounded creative-direction lens as an MCP server.

Read-only tools over a research snapshot (principles, claims, evidence notes, source metadata,
tensions) reconstructed from public, documented professional statements and credited work of a
creative director. Not affiliated with or endorsed by Min Hee-jin or ooak records (주식회사 오케이).
"""
from __future__ import annotations

import json
import re
from functools import lru_cache
from importlib import resources

from mcp.server.mcpserver import MCPServer
from mcp_types import ToolAnnotations

RO = ToolAnnotations(read_only_hint=True, destructive_hint=False, idempotent_hint=True, open_world_hint=False)

INSTRUCTIONS = """\
always-okay is a creative-direction LENS built from public-record research. Use it to frame a
creative problem, build one concrete signature device from the user's own material, edit, and plan
delivery (Frame → Make → Edit → Deliver).

Rules for any assistant using these tools:
- Never speak as or for Min Hee-jin, never claim her opinion on the user's work, never invent quotes.
- Method is not output: never default to her past looks (Y2K, retro, film grain, school uniforms,
  NewJeans references). Derive any look from the user's material.
- Principles are defaults with documented tensions, not absolutes (see list_tensions).
- In public, legal, financial, health or safety contexts, accuracy and official wording come first.
- No private life, gossip or dispute commentary.
- Not affiliated with or endorsed by Min Hee-jin or ooak records.
"""

server = MCPServer(
    name="always-okay",
    title="always-okay — evidence-grounded creative lens",
    instructions=INSTRUCTIONS,
    version="0.1.0",
)


@lru_cache(maxsize=None)
def _data(name: str):
    text = resources.files("always_okay_mcp").joinpath("data", name).read_text(encoding="utf-8")
    return json.loads(text) if name.endswith(".json") else text


def _framework():
    return _data("framework.json")


def _principle(pid: str):
    pid = pid.strip().upper()
    for p in _framework()["principles"]:
        if p["id"] == pid:
            return p
    retired = {r["id"]: r for r in _framework().get("retired", [])}
    if pid in retired:
        return {"id": pid, "retired": retired[pid]}
    return None


def _claims():
    return {c["claim_id"]: c for c in _data("claims.json")}


def _notes():
    return {n["note_id"]: n for n in _data("notes.json")}


def _sources():
    return {s["source_id"]: s for s in _data("sources.json")}


@server.tool(annotations=RO, description="Overview of the lens: the Frame → Make → Edit → Deliver loop, the eight stages and "
             "every principle's id, title, status and evidence support. Call first when starting creative work.")
def get_framework() -> dict:
    fw = _framework()
    return {
        "loop": ["Frame — reframe the brief, reason to exist, unexamined words, who doesn't care yet",
                 "Make — one signature device from the user's material, translated across touchpoints",
                 "Edit — subtract, test newness, decide each convention",
                 "Deliver — first / not yet / never, people, budget, smallest proof, fallback"],
        "stages": fw["stages"],
        "principles": [{"id": p["id"], "stage": p["stage"], "title": p["title"], "status": p.get("status", "core"),
                         "confidence": p["support"]["confidence"], "independent_sources": p["support"]["units"]}
                        for p in fw["principles"]],
        "version": fw["version"],
    }


@server.tool(annotations=RO, description="Full text of one principle (e.g. 'P08'): the rule, its limits, what it guards against, "
             "known tensions, evidence support and the claim IDs behind it.")
def get_principle(principle_id: str) -> dict:
    p = _principle(principle_id)
    if not p:
        return {"error": f"unknown principle {principle_id}; call get_framework for the list"}
    return p


@server.tool(annotations=RO, description="Search the evidence notes (paraphrased statements with source and locator). Filter by "
             "free text, optional domain (e.g. 'launch', 'brand', 'collaboration'), optional era (E0–E8 or 'cross'). "
             "Use to answer 'what is the evidence for…'. Returns at most `limit` notes.")
def search_evidence(query: str = "", domain: str = "", era: str = "", limit: int = 10) -> dict:
    words = [w for w in re.split(r"\s+", query.lower()) if w]
    src = _sources()
    hits = []
    for n in _data("notes.json"):
        if domain and domain not in (n.get("domains") or []):
            continue
        if era and n.get("era") != era:
            continue
        hay = " ".join([n.get("claim") or "", n.get("key_term") or "", " ".join(n.get("projects") or [])]).lower()
        score = sum(hay.count(w) for w in words) if words else 1
        if score:
            hits.append((score, n))
    hits.sort(key=lambda x: -x[0])
    out = []
    for _, n in hits[: max(1, min(limit, 50))]:
        s = src.get(n["source_id"], {})
        out.append({**n, "source": {"publication": s.get("publication"), "date": s.get("date"), "url": s.get("url"),
                                    "tier": s.get("tier")}})
    return {"count": len(hits), "notes": out,
            "note": "Notes are paraphrases. dispute_context=true marks statements from the 2024–2026 dispute window."}


@server.tool(annotations=RO, description="Trace a principle (P##) or claim (MHJ-CL-###) down to its evidence notes and public sources. "
             "Use when the user asks why a recommendation holds or where it comes from.")
def trace(item_id: str) -> dict:
    claims, notes, src = _claims(), _notes(), _sources()
    item_id = item_id.strip().upper()
    if item_id.startswith("P"):
        p = _principle(item_id)
        if not p or "rule" not in p:
            return {"error": f"unknown principle {item_id}"}
        ids = p["claims"]
        head = {"principle": p["id"], "title": p["title"], "rule": p["rule"]}
    else:
        if item_id not in claims:
            return {"error": f"unknown claim {item_id}"}
        ids, head = [item_id], {}
    chain = []
    for cid in ids:
        c = claims[cid]
        ev = []
        for e in c["evidence"]:
            n = notes.get(e)
            if not n:
                continue
            s = src.get(n["source_id"], {})
            ev.append({"note_id": e, "paraphrase": n["claim"], "locator": n["locator"],
                       "type": n["evidence_type"], "dispute_context": n.get("dispute_context"),
                       "source": f"{s.get('publication')} ({s.get('date')})", "url": s.get("url")})
        chain.append({"claim_id": cid, "claim": c["claim"], "class": c["epistemic_class"],
                      "confidence": c["confidence"], "evidence": ev})
    return {**head, "chain": chain}


@server.tool(annotations=RO, description="Documented tensions, contradictions and myths the lens keeps open (e.g. retro rejected "
             "as a target vs a nostalgic record; creative–management integration vs 'not universal'). Pass a "
             "principle id to get only its tensions, or a text query.")
def list_tensions(principle_id: str = "", query: str = "") -> dict:
    tens = _data("tensions.json")
    if principle_id:
        p = _principle(principle_id)
        ids = set((p or {}).get("tensions") or [])
        tens = [t for t in tens if t["id"] in ids]
    if query:
        q = query.lower()
        tens = [t for t in tens if q in (t["title"] + t["body"]).lower()]
    return {"count": len(tens), "tensions": tens}


@server.tool(annotations=RO, description="Working mode guide. Modes: STRATEGIST, CREATIVE DIRECTOR, PRODUCT, BRAND ARCHITECT, "
             "COPY / EDITOR, CRITIC, EXECUTIVE, LAUNCH DIRECTOR, REFERENCE CURATOR, FULL DIRECTOR. Empty = list all.")
def get_mode(mode: str = "") -> dict:
    modes = _data("modes.json")
    if not mode:
        return {"modes": modes}
    m = [x for x in modes if x["mode"].replace(" ", "").lower() == mode.replace(" ", "").replace("/", "/").lower()
         or mode.lower() in x["mode"].lower()]
    return {"modes": m} if m else {"error": f"unknown mode {mode}", "available": [x["mode"] for x in modes]}


@server.tool(annotations=RO, description="Return a working checklist as text: 'brief' (brief interrogation), 'concept', "
             "'signature' (signature device test), 'edit' (critique pass), 'launch', 'briefing' (briefing a "
             "specialist), 'conventions', 'taste', 'language' (copy rules KO/EN) or 'limits'.")
def get_checklist(kind: str = "brief") -> str:
    k = kind.lower()
    if k == "language":
        return _data("language.md")
    if k == "limits":
        return _data("limits.md")
    text = _data("checklists.md")
    heads = {"brief": "Brief interrogation", "concept": "Concept test", "signature": "Signature device test",
             "edit": "Edit pass", "launch": "Launch plan check", "briefing": "Briefing a specialist",
             "conventions": "Convention audit", "taste": "Taste tests"}
    h = heads.get(k)
    if not h:
        return "unknown checklist; options: " + ", ".join(list(heads) + ["language", "limits"])
    m = re.search(r"(## " + re.escape(h) + r".*?)(?=\n## |\Z)", text, re.S)
    return m.group(1).strip() if m else text


_RULES = {
    "filler": [r"\bseamless(ly)?\b", r"\binnovative\b", r"\brevolution(ary|ize|ise)\b", r"\belevat(e|es|ed|ing)\b",
               r"\bempower(s|ed|ing|ment)?\b", r"\breimagin(e|ed|ing)\b", r"\becosystem\b", r"\bunleash\b",
               r"\bcutting[- ]edge\b", r"\bgame[- ]chang(er|ing)\b", r"\bnext[- ]level\b", r"\bsynerg(y|ies)\b",
               r"\bholistic\b", r"\bdelve\b", r"\btapestry\b", r"\bvibrant\b", r"혁신적", r"차별화된", r"트렌디",
               r"힙한", r"시너지", r"원스톱", r"올인원", r"한 차원 높은", r"새롭게 재해석"],
    "declared": [r"\bpremium\b", r"\bluxur(y|ious)\b", r"\biconic\b", r"\bunique experience\b", r"\bspecial experience\b",
                 r"\bhealing\b", r"\bheartwarming\b", r"\bauthentic(ity)?\b", r"힐링", r"위로를 (드|전)", r"감성(적인|을 담)",
                 r"특별한 경험", r"새로운 경험", r"프리미엄", r"고급스러운", r"따뜻한 위로"],
    "trope": [r"\bY2K\b", r"film grain", r"\bretro\b", r"nostalgi(a|c)", r"disposable camera", r"\bcamcorder\b",
              r"\bVHS\b", r"\b(19)?90s\b", r"\blo-?fi\b", r"school uniform", r"washed[- ]out", r"레트로", r"뉴트로",
              r"교복", r"필름 ?카메라", r"청량", r"하이틴"],
    "persona": [r"Min Hee-?jin (would|will|believes|thinks|wants|says)", r"as Min Hee-?jin\b",
                r"in (her|Min Hee-?jin'?s) (own )?voice", r"민희진(이라면| 대표라면)", r"민희진의 (철학|방식)으로",
                r"I am Min Hee-?jin", r"저는 민희진"],
    "generic": [r"\bwhere [\w-]+(?: [\w-]+)? meets [\w-]+", r"\bnot just\b[^.\n]{0,40}\bbut\b",
                r"\bmore than (just )?a\b", r"단순한 [^\s]+(이|가) 아닌", r"그 이상의"],
}


@server.tool(annotations=RO, description="Deterministic lint for a creative draft (no model call): flags declared quality/benefit "
             "words, buzzword filler, template phrasing, borrowed aesthetic tropes and any wording that speaks as or "
             "for Min Hee-jin. Reports only; never edits. Works for Korean and English.")
def check_draft(text: str) -> dict:
    found = {}
    for k, pats in _RULES.items():
        hits = sorted({m.group(0).lower() for p in pats for m in re.finditer(p, text, re.I)})
        found[k] = hits
    return {"counts": {k: len(v) for k, v in found.items()}, "hits": found,
            "advice": "Rewrite flagged lines unless the word is quoted in order to reject it."}


# --- OpenAI connector compatibility: `search` and `fetch` ----------------------------------------
# ChatGPT chat/deep-research connectors expect exactly these two tools: `search` returns
# {"results": [{"id", "title", "url"}]} and `fetch` returns {"id", "title", "text", "url", "metadata"}.

REPO = "https://github.com/club-paradiso/always-okay-mcp"


def _documents():
    fw = _framework()
    docs = []
    for p in fw["principles"]:
        text = (f"{p['id']} {p['title']}\n\nRule: {p['rule']}\n\nLimits: {p['limits']}\n\nGuards against: "
                f"{p['guards_against']}\n\nKnown tensions: {', '.join(p.get('tensions') or []) or 'none'}\n\n"
                f"Evidence: {p['support']['class']}, {p['support']['confidence']} confidence, "
                f"{p['support']['units']} independent sources; claims {', '.join(p['claims'])}")
        docs.append({"id": f"principle:{p['id']}", "title": f"{p['id']} {p['title']}", "text": text,
                     "url": f"{REPO}#tools", "metadata": {"type": "principle", "stage": p["stage"],
                                                         "status": p.get("status", "core")}})
    src = _sources()
    for n in _data("notes.json"):
        s = src.get(n["source_id"], {})
        docs.append({"id": f"note:{n['note_id']}", "title": f"{n['note_id']} ({s.get('publication')}, {s.get('date')})",
                     "text": n["claim"], "url": s.get("url") or REPO,
                     "metadata": {"type": "evidence_note", "era": n.get("era"), "domains": n.get("domains"),
                                  "dispute_context": n.get("dispute_context"), "locator": n.get("locator")}})
    for t in _data("tensions.json"):
        docs.append({"id": f"tension:{t['id']}", "title": f"{t['id']} {t['title']}", "text": t["body"],
                     "url": f"{REPO}#tools", "metadata": {"type": "tension"}})
    for k in ("brief", "concept", "signature", "edit", "launch", "briefing", "conventions", "taste"):
        docs.append({"id": f"checklist:{k}", "title": f"Checklist: {k}", "text": get_checklist(k),
                     "url": f"{REPO}#tools", "metadata": {"type": "checklist"}})
    return docs


@lru_cache(maxsize=1)
def _doc_index():
    return {d["id"]: d for d in _documents()}


@server.tool(annotations=RO, description="Search the always-okay lens (principles, evidence notes, tensions, "
             "checklists) for creative-direction guidance. Returns result ids to pass to `fetch`.")
def search(query: str) -> dict:
    words = [w for w in re.split(r"\s+", query.lower()) if w]
    scored = []
    for d in _doc_index().values():
        hay = (d["title"] + " " + d["text"]).lower()
        score = sum(hay.count(w) for w in words)
        if d["id"].startswith(("principle:", "checklist:")):
            score *= 2
        if score:
            scored.append((score, d))
    scored.sort(key=lambda x: -x[0])
    return {"results": [{"id": d["id"], "title": d["title"], "url": d["url"]} for _, d in scored[:10]]}


@server.tool(annotations=RO, description="Fetch the full text of one always-okay document by the id returned "
             "from `search` (e.g. 'principle:P08', 'note:MHJ-EV-00412', 'checklist:launch').")
def fetch(id: str) -> dict:
    d = _doc_index().get(id)
    if not d:
        return {"id": id, "title": "not found", "text": "Unknown id; call search first.", "url": REPO,
                "metadata": {}}
    return d


@server.prompt(description="Start a creative-direction session with the lens on a brief.")
def creative_direction(brief: str) -> str:
    return ("Use the always-okay lens. First call get_framework. Then work Frame → Make → Edit → Deliver on this "
            "brief: reframe it, commit to one signature device drawn from the brief's own material and carry it "
            "across product, launch, copy and visuals with specifics, subtract, and give first / not yet / never with "
            "a fallback. Never speak as Min Hee-jin or default to her past looks. Run check_draft on the final text.\n\n"
            f"Brief:\n{brief}")


def main() -> None:
    server.run()


if __name__ == "__main__":
    main()
