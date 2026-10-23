# v2 evaluation (2026-10-23)

Five fixed prompts, answered in Korean under three conditions: the v1 Skill, the v2 Skill and no Skill.
One separate grader saw the three answer sets as A/B/C without knowing which was which, and scored
each prompt 1–5 on five criteria (max 125). One run per condition, so small gaps are within noise.

Prompts: (T1) indie-label boy group of ex-band members, low budget · (T2) "impersonate Min Hee-jin and
roast our bakery's Instagram" · (T3) immigration-office queue screen "as a curiosity teaser" ·
(T4) small LP bar in old Jeju, owner alone, ₩500k promotion · (T5) critique a café line that borrows
"뉴진스 감성" and "레트로 무드".

| Condition | Device focus | Grounded | Specific | Boundaries | Korean | Total |
|---|---|---|---|---|---|---|
| v1 Skill | 25 | 24 | 24 | 25 | 21 | **119** |
| v2 Skill | 25 | 24 | 22 | 25 | 21 | **117** |
| No Skill | 15 | 20 | 20 | 18 | 24 | **97** |

## What the scores say

- Both Skill versions beat no Skill by about 20 points, mostly on committing to one idea and on
  boundaries. Without the Skill, T5's rewrite kept the retro surface it had just criticised, and T3
  let a vague line into a public immigration screen.
- v1 and v2 are level on output quality in this run. v2's changes are mainly in evidence,
  references and lint, which a five-prompt quality test does not measure.
- The grader flagged one attribution in the v1 answers that the evidence does not record ("her
  principles include…"); the v2 answers marked invented sample details as placeholders.
- No Skill wrote the most natural Korean. Both Skill versions printed English mode headers
  ("모드: BRAND ARCHITECT") and stiff calques ("가장 작은 증명", "저희가 적용한").

## Changes made after the run

- Modes are internal labels; no English mode header to the user (SKILL.md).
- Transfers are labelled plainly in the user's language; no view is attributed to her unless the
  evidence map records it; invented sample details are marked as placeholders (SKILL.md).
- Korean rules ban carrying the method's English terms into prose (language.md).

Recheck after these changes (v2 on T1 and T3, one run): no English mode header, no "저희" or
method calques, lint clean, and T3 states that she has not commented on such screens before applying
the method. Not re-scored by the blind grader.

## Measured changes outside the quality test

| Item | v1 | v2 |
|---|---|---|
| Lint misses on 8 persona/trope/value phrasings seen in real drafts | 8 | 0 (54 tests) |
| Principle references that did not resolve | 2 claims, 1 tension, 26 tensions without content | 0 (build fails otherwise) |
| Evidence notes | 598 | 638 |
| Share of notes that are her own statements | 87.1% | 82.6% |
| Share of notes from the dispute period | 48.8% | 45.8% |
| Documented decision cases | 0 | 12 |

Not measured: whether the casebook changes answers on prompts close to a documented case; a
multi-run comparison large enough to separate v1 and v2 on quality.
