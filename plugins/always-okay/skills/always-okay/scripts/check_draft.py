#!/usr/bin/env python3
"""Deterministic lint for a creative draft (no model call). Reports; never edits.

  python3 check_draft.py FILE [FILE ...]      or      ... | python3 check_draft.py -

Flags five things a reviewer should look at before a draft goes out:
  filler       buzzwords that assert value instead of showing it
  declared     the draft announcing its own quality or benefit (premium, iconic, healing, 감성...)
  trope        borrowed surface looks (Y2K, retro, film grain, school uniform, 청량...) — fine only
               when the brief itself is about that period or the draft gives a reason
  persona      speaking as or for Min Hee-jin — never allowed
  generic      template phrasing ("where X meets Y", "not just X but Y")
Exit code 0 always; this is information, not a gate.
"""
import re
import sys

RULES = {
    "filler": [r"\bseamless(ly)?\b", r"\binnovative\b", r"\brevolution(ary|ize|ise)\b",
               r"\belevat(e|es|ed|ing)\b", r"\bempower(s|ed|ing|ment)?\b", r"\breimagin(e|ed|ing)\b",
               r"\becosystem\b", r"\bunleash\b", r"\bcutting[- ]edge\b", r"\bgame[- ]chang(er|ing)\b",
               r"\bnext[- ]level\b", r"\bsynerg(y|ies)\b", r"\bholistic\b", r"\bdelve\b", r"\btapestry\b",
               r"\bvibrant\b", r"혁신적", r"차별화된", r"트렌디", r"힙한", r"시너지", r"원스톱", r"올인원",
               r"한 차원 높은", r"새롭게 재해석"],
    "declared": [r"\bpremium\b", r"\bluxur(y|ious)\b", r"\biconic\b", r"\bunique experience\b",
                 r"\bspecial experience\b", r"\bhealing\b", r"\bheartwarming\b", r"\bauthentic(ity)?\b",
                 r"힐링", r"위로를 (드|전)", r"감성(적인|을 담)", r"특별한 경험", r"새로운 경험", r"프리미엄",
                 r"고급스러운", r"따뜻한 위로"],
    "trope": [r"\bY2K\b", r"film grain", r"\bretro\b", r"nostalgi(a|c)", r"disposable camera", r"\bcamcorder\b",
              r"\bVHS\b", r"\b(19)?90s\b", r"\blo-?fi\b", r"school uniform", r"washed[- ]out", r"레트로",
              r"뉴트로", r"교복", r"필름 ?카메라", r"청량", r"하이틴"],
    "persona": [r"Min Hee-?jin (would|will|believes|thinks|wants|says)", r"as Min Hee-?jin\b",
                r"in (her|Min Hee-?jin'?s) (own )?voice", r"민희진(이라면| 대표라면)", r"민희진의 (철학|방식)으로",
                r"I am Min Hee-?jin", r"저는 민희진", r"what (would )?MHJ (would )?(do|think)"],
    "generic": [r"\bwhere [\w-]+(?: [\w-]+)? meets [\w-]+", r"\bnot just\b[^.\n]{0,40}\bbut\b",
                r"\bmore than (just )?a\b", r"단순한 [^\s]+(이|가) 아닌", r"그 이상의"],
}


def scan(text):
    out = {}
    for k, pats in RULES.items():
        hits = []
        for p in pats:
            hits += [m.group(0) for m in re.finditer(p, text, re.I)]
        out[k] = hits
    return out


def main(args):
    srcs = args or ["-"]
    for s in srcs:
        text = sys.stdin.read() if s == "-" else open(s, encoding="utf-8").read()
        res = scan(text)
        print(f"== {s}: " + ", ".join(f"{k} {len(v)}" for k, v in res.items()))
        for k, v in res.items():
            if v:
                print(f"  {k}: " + "; ".join(sorted(set(x.lower() for x in v))))
        if res["persona"]:
            print("  !! persona: remove any wording that speaks as or for Min Hee-jin.")


if __name__ == "__main__":
    main(sys.argv[1:])
