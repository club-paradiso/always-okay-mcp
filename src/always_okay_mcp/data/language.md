# Language and copy

Rules for any text the Skill writes or edits [P18, P13, P02, P28].

## Never
- Declared quality or benefit: premium, luxury, iconic, special experience, healing, heartwarming, authentic;
  프리미엄, 고급스러운, 힐링, 위로를 드립니다, 감성적인, 특별한 경험, 새로운 경험.
- Filler: seamless, innovative, revolutionary, elevate, empower, reimagine, ecosystem, unleash, cutting-edge,
  next-level, synergy, holistic, vibrant; 혁신적, 차별화된, 트렌디한, 힙한, 시너지, 원스톱, 올인원, 한 차원 높은.
- Template frames: "where X meets Y", "more than just X", "not just X but Y"; "단순한 X가 아닌", "그 이상의".
- Speaking as or for Min Hee-jin, or imitating her speech.

Run `python3 scripts/check_draft.py FILE` (or pipe text to `-`) on any substantial draft; it reports these and never edits.

## Instead
- Describe what a person sees, hears, holds or does. Let the benefit be inferred.
- One concrete noun beats three adjectives.
- Names: short, sayable, no explanation needed, a little playful; a double reading is a bonus.
- Evaluation: "good" only when it is; name the weak part and the fix.
- Length follows the task.

## Korean
- Write natural Korean, not translated English; prefer short sentences and plain verbs.
- Do not restyle legal, immigration, administrative or official wording, statute names, form names, numbers or identifiers.
- Avoid MZ/Gen-Z slang costumes unless the user's audience and voice already use them.
- If the environment has the user's Korean lint (`node ~/dev/korean-language-quality/bin/kolint.mjs --genre ux <paths>`), run it on Korean deliverables and report its findings; it reports, it does not rewrite.
