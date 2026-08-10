# PLA-157 -- zinnia's shifted trigger register block + the six titles (staged 2026-08-10)

Base canonical `ce9eb12f` at staging (NOT the `72284f02` on the issue, which predates PLA-156's
two promotes). Staged to the promote boundary and STOPPED there: PLA-155 ran in parallel and
Trevor serializes promotes. Scratch post-state SHA `9cc3fbdc` (discarded after the re-base).

**PROMOTED 2026-08-10 after Trevor's GO: `4f610318` -> `060b91b8`.** PLA-155 landed first
(inverting the GO's ordering, harmlessly): its footprint (sweet-pea, berry crops, edamame,
source_catalog) is disjoint from this one, and zinnia/bee-balm/marigold were verified
byte-identical across `ce9eb12f` -> `4f610318` before both files were re-pinned to the new base.
Post-promote gauntlet on live canonical: guard suite 10/10 in bootstrap mode, whole_crop_gate
PASS x3 with A52/A53 live, gate_all 121/121, release_verify's only NEW concern is its
single-crop-shaped "crops changed" seeing this promote's legitimate two-crop footprint (guard G1
proves the footprint byte-exactly; the `plantings_provenance` novel-key concerns reproduce
byte-identical at base). Bee-balm trigger 2 keeps "Frost and winter rest" per the GO's
author's-call clause: the trigger's action is literally "Frost and dormancy" and its body covers
both frost kill-back and winter rest.

## Cert-log check first (the PLA-156 lesson)

Both crops' `verification_status` read BEFORE authoring. Neither log ratifies the trigger prose
placement: zinnia's records the step11 verbatim flip (0 HARD on 359 user-facing strings vs 13/13
readable sources) -- a raw id in `body_beginner` cannot trip a verbatim gate, so the cert result
is consistent with the defect existing at cert. Both stray ids are in zinnia's crop-level
`source_set`, so restoring them agrees with the cert rather than re-adjudicating it. Per
`docs/verification_log_ref_convention.md`, the fix retires nothing either log asserts: **no
correction line owed, cert logs byte-identical** (guarded, G8).

## The defect, re-verified at ce9eb12f

Exactly as filed. Additionally adjudicated against marigold (the healthy sibling ornamental,
authored from the same templates): zinnia's block is a clean ONE-SLOT ROTATION --
`title_beginner` holds prose matching marigold's `body_seasoned` template per trigger,
`body_seasoned` holds prose matching marigold's `body_beginner` template, `body_beginner` holds
the id. So the fix rotates the two body strings back BYTE-IDENTICAL (cert-checked prose, zero
re-authoring risk) and the only new prose is six short beginner titles.

## The restored credits were read, not assumed

Both documents fetched and read 2026-08-10:

- `clemson_hgic_1149` (HGIC "How to Grow Zinnias"): "Proper air circulation will help to dry the
  leaves and prevent powdery mildew", "water at the base of the plants", spacing guidance
  (trigger 1); "seeds may be directly sown ... when the chance of the last frost has passed"
  (frost-tenderness, trigger 0).
- `uf_ifas_zinnia` (Gardening Solutions): "zinnias can handle Florida's hot summers, and healthy
  plants will bloom throughout the summer, often until the first frost"; keep water off the
  leaves (trigger 2).

Both T1 in `source_catalog` (admission `zinnia_steps4_5_se_gulf`). New `anchoring_urls` entries
carry `verified: 2026-08-10` (the read date); pre-existing entries stay byte-identical.

## Gates A52/A53 (tools/trigger_prose_gate.py) -- measured before wired

- **A52 identifier-shaped consumer prose** (`^[a-z0-9_]+$` in a trigger `title_*`/`body_*`):
  roster-wide the only hits are zinnia's 3. Scope is deliberately weather_triggers-only: a wider
  sweep floods on legitimate enums (`container_notes.soil_mix.type_seasoned =
  'container_potting_mix'`, ~17 crops) -- that scope decision is itself asserted in the tests.
- **A53 title length** (max 80): longest legitimate title roster-wide is 60 chars (grapefruit);
  the 6 defects run 117-147. 80 splits the gap with headroom.

TDD: `tools/test_trigger_prose_gate.py` written first, watched fail (module missing), then the
module; 6 groups including synthetic injections into all four prose slots and the boundary at 80.

**⚠ Gate-as-worklist: A52/A53 are wired into `whole_crop_gate.py` NOW, so `whole_crop_gate
zinnia` (6 violations), `bee-balm` (3), and therefore `gate_all` are RED on live canonical until
the promote lands.** If PLA-155's gauntlet runs first, those reds are THIS issue's staged work,
not PLA-155 breakage -- the violation text names PLA-157.

## Guard suite (tools/test_promote_pla157_zinnia_triggers.py)

10 groups; RED demonstrated against live (unpromoted) canonical, GREEN against the scratch
post-state via `PLA157_CANONICAL=<path>`. All expectations retyped constants. **11/11 mutations
caught**: rotation skipped, wrong title, third crop touched, source dropped, cert log appended,
pretty-printed output, finding omitted, body byte re-authored, ghost crop appended (the
iterate-PRE-only killer), em dash injected, verified date faked. (The G10 em-dash sweep is
belt-and-suspenders -- byte-identity guards catch any body change first; its COMPACT half is
independently reachable, proven by the pretty-print mutant.)

Gauntlet on the scratch post-state: whole_crop_gate PASS on zinnia / bee-balm / marigold;
gate_all run recorded below; both test files pass under python3 and fire under pytest
(failure = collection error, proven live).

## Promote runbook (serialized by Trevor)

1. `python3 tools/promote_pla157_zinnia_triggers.py` (preflights ce9eb12f, `sys.exit(1)` on
   mismatch -- if PLA-155 promoted first this ABORTS and the transform must be re-based).
2. `python3 tools/test_promote_pla157_zinnia_triggers.py` (bootstrap mode reads live canonical).
3. Gauntlet: whole_crop_gate on zinnia + bee-balm + marigold, `tools/gate_all.py`,
   `tools/release_verify.py`, source-truth sample.
4. State trio: CURRENT_STATE.md surgical amend + STATE_HISTORY.md append + LATEST.txt.
5. Commit with EXPLICIT PATHSPEC (PLA-155 shares this checkout); Trevor approves first.
6. Follow-up: register post SHA in `promote_fixture.COMMIT_FOR`, set the suite's `POST_SHA`.

## Findings recorded

- zinnia `pla157_weather_trigger_register_shift` (resolved, non-blocking)
- bee-balm `pla157_title_beginner_body_prose` (resolved, non-blocking)
