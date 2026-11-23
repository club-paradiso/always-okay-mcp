# v3 evaluation (2026-11-23)

Six fixed prompts in Korean, each answered once with the v0.2 Skill and once with the v0.3 Skill
(same model, fresh context, Skill files only, no web). Two separate graders saw the answers as A/B
with the assignment shuffled per prompt, and scored each answer 1–5 on six criteria (max 30 per
answer, 180 per condition). One grader was briefed as a creative director, the other as a sceptical
client. One run per condition; graders are AI models of the same family as the generator.

Prompts: (T1) six-seat late-night noodle shop in old Jeju, name and concept · (T2) launch of a
self-published Korean textbook built on real administrative forms, ₩1M · (T3) critique and rewrite
of a Pilates studio bio full of declared quality · (T4) a church Christmas photo booth whose strips
people keep · (T5) an immigration-office waiting-screen notice "as a teaser" · (T6) identity and
fixed card format for a one-person indie-music account.

| Prompt | v0.2 (director / client) | v0.3 (director / client) |
|---|---|---|
| T1 | 27 / 28 | 28 / 26 |
| T2 | 24 / 24 | 26 / 26 |
| T3 | 24 / 25 | 27 / 26 |
| T4 | 28 / 26 | 29 / 28 |
| T5 | 24 / 23 | 28 / 28 |
| T6 | 22 / 23 | 29 / 28 |
| **Total** | **149 / 149** | **167 / 162** |

Summed over both graders: unexpectedness 42 → 56 of 60, Korean 51 → 58 of 60. v0.3 was preferred on
6 of 6 prompts by one grader and 5 of 6 by the other (T1 went to v0.2 for the client grader).

## What the graders flagged in v0.3 answers

- T5: a sample queue number on a waiting-room screen could be read as a live call; the address and
  QR appeared only in the last scene; one language per loop makes some readers wait.
- T3: the rewrite contained a guessed detail, flagged but still inside the copy.
- T1: the device published a daily bowl count, which an owner may not want public, and added work
  for a person cooking alone.
- T2 (v0.2 answer): a claim about which form foreign residents file was asserted unchecked.
- T4: both versions reached the same central idea; the gap there is small.

## Changes made after the run

- limits.md: on a public notice the action and place stay visible throughout, languages are
  readable without a long wait, no sample number or time where it could pass for a live one.
- SKILL.md: rewrites use only the user's facts; unknowns go in brackets; legal or procedural claims
  are checked or marked unchecked.
- checklists.md: the device must be runnable by the people and budget in the brief and must not
  expose what the owner would keep private.

Not re-scored after these changes. Not measured: variance across repeated runs, a human panel,
English prompts.
