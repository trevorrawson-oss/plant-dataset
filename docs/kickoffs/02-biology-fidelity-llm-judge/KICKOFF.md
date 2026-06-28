# KICKOFF — biology-fidelity LLM-judge layer (the truth-layer backstop for the 18->~105 scale)

**Paste the block below into a fresh claude.ai chat.**

## What this chat needs that isn't in the prompt

This is a DESIGN + CALIBRATION task, so the chat needs the **18 certified crop records** to tune the
rubric against (they are the biologically-correct ground truth — the judge must NOT flag them). Give
it those records: attach `crops_data_final.json` (or paste the 18 `verified_gs_arc` crops). It also
references `docs/incognito-redteam-remediation-2026-06-27.md` and the STATE_HISTORY 2026-06-27
entries — attach or paste if the chat is not opened on the repo. Everything else is in the prompt.

---

```
TASK: design + calibrate a biology-fidelity review (an LLM-judge QA pass) that catches what the
deterministic gates structurally cannot — the backstop the 18->~105 scale phase needs.

WHY THIS EXISTS. The 2026-06-27 incognito red-team proved GATE: PASS proves a crop is well-SHAPED +
self-consistent + exemplar-matched, NOT CORRECT (findings C6/C7/C14 in
docs/incognito-redteam-audit-2026-06-27.md). The Claude Code lane has since built the DETERMINISTIC
truth layer — A33 numeric_sanity (numbers within physical bounds; spacing archetype-aware), A34
cross_consistency (pH prose vs structured range; harvest-requires-plant). Those catch structural and
numeric SELF-contradictions (the copy-template-don't-refit failure). But three designed checks
bottomed out at biology/prose and CANNOT be clean 0-FP deterministic gates — they are YOUR lane:
  1. calendar-vs-climate: a `growing` token in a month a cell's own climate calls hard-frost. Needs
     a PER-CROP cold-hardiness judgment (broccoli/lettuce grow in cool months legitimately; a frost-
     tender crop must not). DO NOT solve this with a shared region-heat/cold envelope — that was
     rejected (decision B3: heat/cold tolerance is per-crop+region+zone physiology, backed per-cell).
  2. rotation-family vs botanical family: the fabricated "rutabaga that is basil verbatim" carried
     mint-family rotation. The dataset's `family`/`avoid_after` fields are null and `good_after` is
     free text, so there is nothing structured to check — it needs botanical knowledge.
  3. wrong-crop heat_pause physiology: a heat_pause object whose prose/sources describe a DIFFERENT
     crop (carrot's heat_pause pasted onto another crop). Needs reading the prose against the crop.
Plus the broader C6 (a fabricated-but-catalogued source chain) and C7 (a biologically impossible
crop) that no structural gate can see.

WHAT TO BUILD.
  A. A biology-fidelity RUBRIC — the questions an expert asks of one crop's record: do the
     pests/diseases/companions/rotation match the crop's botanical family? Is every calendar cell
     physically possible for that region+zone given the crop's real cold/heat tolerance? Are the
     numbers (DTM, spacing, pH, chill, sunlight) right for THIS species, not just within physical
     bounds? Does each heat_pause / cold_pause describe THIS crop's physiology? Do the cited sources
     actually support the claim (C6)? Is anything internally contradictory the gates would miss?
  B. A per-crop REVIEW PROCESS that applies the rubric and emits STRUCTURED findings (crop, field,
     the contradiction, confidence, suggested correction) for human triage — NOT auto-edits.
  C. CALIBRATION against the 18 CERTIFIED anchors first (cherry-tomato, beefsteak-tomato, carrot,
     basil, zucchini-courgette, green-beans-bush, broccoli, peach, apple, lemon, blueberry,
     lettuce-leaf, onion, strawberry, orange-navel, microgreens-mix, lavender, zinnia). They are
     hand-authored and biologically correct — the judge must NOT flag them. Tune the rubric/prompt
     against that 18-crop ground truth (report the false-positive rate) before trusting it on bots.

HOW IT FITS. This is the scale-phase QA the per-batch human source-truth sample cannot cover at
105 crops x ~17 sources. It is a QA AID with a rubric (the deterministic gates stay the hard cert
bar); its findings route to the corrections log / human review, then to the Claude Code lane for any
deterministic-gateable PATTERN that emerges. Pair it with: making the per-batch source-truth sample
LOAD-BEARING (mandatory, sized), and a periodic out-of-band source-URL liveness sweep for C6.

DELIVERABLE: the rubric + the review process + a calibration run on the 18 (false-positive rate +
rubric tuning) + a recommendation for how it gates a bot batch (advisory vs blocking, sample size).
Surface the design before running it at volume.

REFERENCE (Claude Code lane, this session): docs/incognito-redteam-remediation-2026-06-27.md (the
brainstorm + the deterministic layers built); STATE_HISTORY.md 2026-06-27 entries. Roster is now
A2-A36; whole_crop_gate is 11/18 pending the separate soil-texture beginner back-fill (Kickoff 01).
```
