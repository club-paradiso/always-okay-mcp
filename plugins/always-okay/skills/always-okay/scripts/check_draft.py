#!/usr/bin/env python3
"""Deterministic lint for a creative draft (no model call). Reports; never edits.

  python3 check_draft.py FILE [FILE ...]      or      ... | python3 check_draft.py -

Flags five things a reviewer should look at before a draft goes out:
  filler       buzzwords that assert value instead of showing it
  declared     the draft announcing its own quality or benefit (premium, iconic, healing, 감성...)
  trope        borrowed surface looks (Y2K, retro, film grain, school uniform, 청량, NewJeans-style...)
               fine only when the brief itself is about that period or the draft gives a reason
  persona      speaking as or for Min Hee-jin, or predicting her opinion — never allowed
  generic      template phrasing ("where X meets Y", "not just X but Y", "단순한 X가 아닌")
A hit inside a sentence that rejects the word ("don't write 'premium'") is fine; read before fixing.
Exit code 0 always; this is information, not a gate.

The rule table is kept identical to RULES in src/always_okay_mcp/server.py (a test enforces it).
"""
import re
import sys

_MHJ_KO = r"민희진(?:\s?(?:대표|님|씨|감독|이사))?"
_MHJ_EN = r"(?:Min Hee-?jin|MHJ)"

RULES = {
    "filler": [r"\bseamless(ly)?\b", r"\binnovative\b", r"\brevolution(ary|ize|ise)\b", r"\belevat(e|es|ed|ing)\b",
               r"\bempower(s|ed|ing|ment)?\b", r"\breimagin(e|ed|ing)\b", r"\becosystem\b", r"\bunleash\b",
               r"\bcutting[- ]edge\b", r"\bgame[- ]chang(er|ing)\b", r"\bnext[- ]level\b", r"\bsynerg(y|ies)\b",
               r"\bholistic\b", r"\bdelve\b", r"\btapestry\b", r"\bvibrant\b", r"\bworld[- ]class\b",
               r"혁신적", r"차별화된", r"트렌디", r"힙한", r"시너지", r"원스톱", r"올인원", r"한 차원 높은",
               r"새롭게 재해석", r"독보적", r"유니크한"],
    "declared": [r"\bpremium\b", r"\bluxur(y|ious)\b", r"\biconic\b", r"\bunique experience\b",
                 r"\bspecial experience\b", r"\bhealing\b", r"\bheartwarming\b", r"\bauthentic(ity)?\b",
                 r"\bsophisticated\b", r"\belegant\b", r"\bexclusive\b", r"\bone[- ]of[- ]a[- ]kind\b",
                 r"힐링", r"위로를 (드|전)", r"따뜻한 위로", r"감성", r"특별한 경험", r"새로운 경험", r"프리미엄",
                 r"고급(스러운|스럽|진|짐)", r"세련(된|되게|미)", r"감각적(인|으로)"],
    "trope": [r"\bY2K\b", r"film grain", r"\bretro\b", r"nostalgi(a|c)", r"disposable camera", r"\bcamcorder\b",
              r"\bVHS\b", r"\b(19)?90s\b", r"\blo-?fi\b", r"school uniform", r"washed[- ]out", r"\bpastel\b",
              r"\bvintage\b", r"레트로", r"뉴트로", r"교복", r"필름 ?(카메라|감성|그레인)", r"캠코더", r"청량", r"하이틴",
              r"파스텔", r"빈티지",
              r"뉴진스\s?(느낌|감성|스타일|풍|처럼|같(은|이)|룩|st)", r"NewJeans[- ]?(style|vibe|look|aesthetic|inspired|esque)",
              r"like NewJeans"],
    "persona": [_MHJ_EN + r"(?:'d| would| will| believes| thinks| wants| says| loves?| hates?| likes?| prefers?"
                r"| approves?| feels| might)\b",
                r"\bas " + _MHJ_EN + r"\b", r"in (her|Min Hee-?jin'?s) (own )?voice", r"I am Min Hee-?jin",
                r"what (would )?" + _MHJ_EN + r" (would )?(do|think|say)",
                _MHJ_KO + r"(?:이라면|라면)", _MHJ_KO + r"(?:의|식|스타일)\s?(?:철학|방식|말투|화법)?으로",
                _MHJ_KO + r"(?:이|가|는|은|도)?\s?(?:이걸|이것을|이거|이 ?\S+을|\S+를)?\s?(?:보면|봤다면|본다면)",
                _MHJ_KO + r"[^.\n?!]{0,25}?(?:좋아할|싫어할|좋아하겠|싫어하겠|좋아했을|싫어했을|했을 (?:거|것)|할 (?:거|것)(?:예요|이다|같)"
                r"|할걸|골랐을|선택했을|선택할 (?:거|것)|말했을 (?:거|것))",
                r"저는 민희진", r"민희진\s?빙의", r"빙의해서", r"그녀라면"],
    "generic": [r"\bwhere [\w-]+(?: [\w-]+)? meets [\w-]+", r"\bnot just\b[^.\n]{0,40}\bbut\b",
                r"\bnot only\b[^.\n]{0,40}\bbut( also)?\b", r"\bmore than (just )?a\b",
                r"단순한 [^\s]+(이|가) 아닌", r"단순한 [^\s]+(을|를) 넘어", r"그 이상의"],
}


def scan(text):
    return {k: [m.group(0) for p in pats for m in re.finditer(p, text, re.I)] for k, pats in RULES.items()}


def main(args):
    for s in args or ["-"]:
        text = sys.stdin.read() if s == "-" else open(s, encoding="utf-8").read()
        res = scan(text)
        print(f"== {s}: " + ", ".join(f"{k} {len(v)}" for k, v in res.items()))
        for k, v in res.items():
            if v:
                print(f"  {k}: " + "; ".join(sorted(set(x.lower() for x in v))))
        if res["persona"]:
            print("  !! persona: remove any wording that speaks as or for Min Hee-jin or predicts her opinion.")


if __name__ == "__main__":
    main(sys.argv[1:])
