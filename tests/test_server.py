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


def test_openai_search_fetch():
    r = s.search("launch teaser reveal")
    assert r["results"] and all({"id", "title", "url"} <= set(x) for x in r["results"])
    d = s.fetch(r["results"][0]["id"])
    assert {"id", "title", "text", "url", "metadata"} <= set(d) and d["text"]
    assert s.fetch("nope")["title"] == "not found"
