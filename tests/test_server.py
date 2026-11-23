from always_okay_mcp import server as s


def test_framework_has_principles():
    fw = s.get_framework()
    assert len(fw["principles"]) == 32
    assert {p["stage"] for p in fw["principles"]} == {"I", "II", "III", "IV", "V", "VI", "VII", "VIII"}


def test_principle_and_retired():
    assert s.get_principle("p08")["title"].startswith("Translate")
    assert "retired" in s.get_principle("P15")
    assert "error" in s.get_principle("P99")


def test_trace_resolves_every_principle():
    for p in s.get_framework()["principles"]:
        t = s.trace(p["id"])
        assert t["chain"], p["id"]
        assert all(c["evidence"] for c in t["chain"]), p["id"]


def test_search_and_filters():
    r = s.search_evidence("launch teaser", domain="launch", limit=5)
    assert r["notes"] and all("launch" in n["domains"] for n in r["notes"])


def test_tensions_for_principle():
    assert s.list_tensions(principle_id="P11")["count"] >= 1


def test_check_draft_flags():
    r = s.check_draft("A premium, healing brand where heritage meets modern. Min Hee-jin would love the Y2K look.")
    c = r["counts"]
    assert c["declared"] >= 2 and c["trope"] >= 1 and c["persona"] == 1 and c["generic"] == 1
    assert s.check_draft("한 번에 한 잔. 기다리는 7분이 메뉴입니다.")["counts"] == {k: 0 for k in c}


def test_modes_and_checklists():
    assert len(s.get_mode()["modes"]) == 10
    assert "Signature device test" in s.get_checklist("signature")
    assert "T01" in s.get_checklist("taste")


def test_openai_search_fetch():
    r = s.search("launch teaser reveal")
    assert r["results"] and all({"id", "title", "url"} <= set(x) for x in r["results"])
    d = s.fetch(r["results"][0]["id"])
    assert {"id", "title", "text", "url", "metadata"} <= set(d) and d["text"]
    assert s.fetch("nope")["title"] == "not found"


def test_moves_resolve_and_are_searchable():
    all_ = s.get_moves()
    assert len(all_["procedure"]) == 5 and len(all_["moves"]) == 13 and len(all_["taste"]) == 9
    for m in all_["moves"]:
        full = s.get_moves(m["id"])
        assert len(full["instances"]) >= 2 and all(i["source"] and i["note_id"] for i in full["instances"]), m["id"]
        assert all("rule" in s.get_principle(p) for p in full["principles"]), m["id"]
    for x in all_["taste"]:
        assert s.get_moves(x["id"].lower())["evidence"], x["id"]
    assert "error" in s.get_moves("M99")
    ids = [r["id"] for r in s.search("reread the name letters initials")["results"]]
    assert "move:M01" in ids
    assert s.fetch("taste:T02")["metadata"]["type"] == "taste_test"


def test_added_notes_point_at_real_sources_and_principles():
    notes = [n for n in s._data("notes.json") if n.get("added") == "v1.3"]
    assert len(notes) == 10
    src = s._sources()
    for n in notes:
        assert src[n["source_id"]]["url"].startswith("https://") and not n["dispute_context"]
        assert all("rule" in s.get_principle(p) for p in n["principles"])
