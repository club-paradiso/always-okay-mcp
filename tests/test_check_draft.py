"""Lint coverage: the Skill script and the MCP server must flag the same things.

Positive cases are phrasings seen in real drafts that the v1 rules missed; negative cases are
ordinary copy and neutral, documented references that must stay clean.
"""
import importlib.util
from pathlib import Path

import pytest

from always_okay_mcp import server as s

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "check_draft", ROOT / "plugins/always-okay/skills/always-okay/scripts/check_draft.py")
cd = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cd)


def test_rule_tables_identical():
    assert cd.RULES == s._RULES


PERSONA = [
    "민희진 대표가 보면 좋아할 거예요.",
    "민희진은 이걸 좋아할 듯.",
    "민희진이라면 이렇게 했을 겁니다.",
    "민희진 대표라면 티저를 안 했을 거야.",
    "민희진식으로 바꿔보면 이렇다.",
    "민희진의 방식으로 정리하면",
    "민희진 빙의해서 말해줘",
    "그녀라면 이걸 골랐을 거다.",
    "저는 민희진입니다.",
    "Min Hee-jin loves this.",
    "Min Hee-jin would hate the logo.",
    "MHJ would never approve.",
    "Here is the deck, as Min Hee-jin.",
    "What would MHJ do here?",
    "Min Hee-jin'd pick option B.",
]

DECLARED = [
    "감성 큐레이션", "감성 넘치는 브랜드", "고급진 패키지", "세련된 무드", "감각적인 공간",
    "a sophisticated, elegant blend", "an exclusive drop", "프리미엄 라인", "힐링 공간",
]

TROPE = ["뉴진스 느낌으로 가죠", "뉴진스 감성", "a NewJeans-style teaser", "like NewJeans", "파스텔 톤",
         "vintage textures", "필름 감성"]

GENERIC = ["단순한 카페를 넘어", "not only a shop but also a stage", "더 나은 그 이상의 경험"]

CLEAN = [
    "한 번에 한 잔. 기다리는 7분이 메뉴입니다.",
    "민희진은 2013년 인터뷰에서 티저를 상황에 따라 고른다고 말했다.",
    "Min Hee-jin said in a 2022 interview that teasers are a tool, not a ritual.",
    "This lens is built from Min Hee-jin's public interviews and credits.",
    "번호가 불리면 3번 창구로 오세요. 여권과 외국인등록증을 준비해 주세요.",
    "드럼부터 하루 한 파트씩 공개하고, 6일째에 완곡을 공개한다.",
    "She would love to know the opening hours.",
    "The cup holder carries the stamp; regulars collect ten.",
]


@pytest.mark.parametrize("text", PERSONA)
def test_persona_caught(text):
    assert cd.scan(text)["persona"], text
    assert s.check_draft(text)["counts"]["persona"] >= 1, text


@pytest.mark.parametrize("text", DECLARED)
def test_declared_caught(text):
    assert cd.scan(text)["declared"], text


@pytest.mark.parametrize("text", TROPE)
def test_trope_caught(text):
    assert cd.scan(text)["trope"], text


@pytest.mark.parametrize("text", GENERIC)
def test_generic_caught(text):
    assert cd.scan(text)["generic"], text


@pytest.mark.parametrize("text", CLEAN)
def test_clean_copy_not_flagged(text):
    hits = cd.scan(text)
    assert not any(hits.values()), (text, hits)
