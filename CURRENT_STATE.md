# plant -- Current State

**Last updated:** 2026-05-29 (M13 seasoned depth-lift + beginner-sibling complete -- 3 tip-text fidelity fixes; all 10 text_beginner + companions note_beginner authored; attribution untouched; launch flags NOT yet flipped)

**This file is the entry point. Read it first. Authored by Claude at session close; deployed automatically by the promotion command.**

---

## Dataset

- **Canonical location:** `~/plant-dataset/crops_data_final.json` (the ONLY authoritative dataset home)
- **Current SHA:** `4def513c9832c0a91b81de5d722d1dafbc0d75f2e9ee12852433d687a4b4c449`
- **Schema version:** 2.7
- **Crop count:** 123
- **Zones:** USDA hardiness 3-11
- **Format:** minified JSON

## Methodology

- **Current version:** v1.4.1 (patch applied 2026-05-26; base v1.4 LOCKED 2026-05-19)
- **Language/copy architecture:** v1.1 (destination-based dash rule)
- **Tips bar (locked cherry 1C, carried v1.4):** 4-T1 floor, 6-cap, >=3-region geographic spread, institutional-anchor with traceable per-source URL. Applies to ALL tips uniformly (the 0-T1 UX-policy and 2-T1 semi-UX bars apply to *fields*, NOT to tips_by_stage).

## Where we are in the work

- **Current phase:** Phase 3 per-crop verification, gold-standard anchor architecture
- **Cherry tomato (M6) + cleanup (M10):** COMPLETE (launch_ready_core true)
- **Beefsteak tomato (M7) + cleanup (M11):** COMPLETE (launch_ready_core true)
- **M12 dataset-scope scripted pass:** COMPLETE
- **M13 lettuce arc:** IN PROGRESS
  - S1A (structural scan): COMPLETE
  - S1B NA/NB/NC (all 9 zones verified): COMPLETE
  - S1C (soil + pH null-field population): COMPLETE (2026-05-28)
  - S2C-NA (tips attribution batch 1: germination + bolting, 4 tips): COMPLETE (2026-05-28)
  - **S2C-NB (tips attribution batch 2: seedling + established + harvest, 6 tips): COMPLETE (2026-05-28)**
  - **S2C COMPLETE -- tips_by_stage 10/10 attributed.**
  - **Companions walk: COMPLETE (2026-05-28) -- full walk; good_core 3, good_seasoned 1, bad_core 0, bad_seasoned 3, note authored. Provenance-only entry shape locked.**
  - **Seasoned depth-lift + beginner-sibling: COMPLETE (2026-05-29) -- 3 tip-text fidelity fixes (s2c_na 001/002, s2c_nb 001/002 actioned); all 10 `text_beginner` + companions `note_beginner` authored; attribution byte-identical; launch flags NOT flipped.**

## Lettuce tips attribution status (M13 S2C) -- COMPLETE 10/10

| Stage | tip_id | Status |
|---|---|---|
| germination | tip_85e7xx84 | ATTRIBUTED (NA) -- 5 T1 |
| germination | tip_85by323c | ATTRIBUTED (NA) -- 5 T1 |
| seedling | tip_xvfcfpdc | ATTRIBUTED (NB) -- 4 T1 |
| seedling | tip_i5ibsi33 | ATTRIBUTED (NB) -- 4 T1 |
| established | tip_6h1yn6zs | ATTRIBUTED (NB) -- 4 T1 |
| established | tip_p5jti595 | ATTRIBUTED (NB) -- 4 T1 |
| harvest | tip_l4sthpjk | ATTRIBUTED (NB) -- 5 T1 |
| harvest | tip_4hxiphxm | ATTRIBUTED (NB) -- 4 T1 |
| bolting | tip_vntsyt8f | ATTRIBUTED (NA) -- 4 T1 |
| bolting | tip_746ooz61 | ATTRIBUTED (NA) -- 4 T1 |

**10 of 10 attributed.** All tips carry non-empty `sources` + `anchoring_urls`. All `text_beginner` still null (depth-lift surface, tracked not authored).

## What's in flight

- **Seasoned depth-lift + beginner-sibling pass(es): COMPLETE (2026-05-29).** All 10 tips now carry authored `text_beginner`; companions `note_beginner` authored. 3 tips had `text` fidelity-fixed (germination heat ceiling; seedling crowding-bolt removed; established water reframed heat-coupled). Carried prose-vs-source findings s2c_na 001/002 + s2c_nb 001/002 actioned (in-record status flip deferred to validation pass per Trevor 2026-05-28).
- **Validation pass: NEXT SESSION.** Kickoff in this bundle (`2_for_next_chat/`). Flips both launch_ready flags. **Validation notes (explicit task list, do all before flipping flags):**
  1. ~~Regenerate `sources_summary`~~ **DONE at companions walk** (primary=29 T1, secondary=0, uncited=0). Re-regenerate only if a later session touches non-tip field sources.
  2. **Back-fill s2c_na_finding_001-004 into `verification_status.open_findings`** (Trevor decided 2026-05-28). 001/002 -> resolved (actioned at depth-lift); 003/004 -> open. **Flip s2c_nb_001/002 to resolved** (actioned at depth-lift). Confirm S1C 001-003 in-record status; back-fill if doc-only. Reconcile open_findings count after.
  3. Confirm the 4 prose-vs-source dispositions match live `text` on the 3 tips (they do at hand-off).
  4. Verify all 10 tips + companions meet bars; **assert 0 unresolved blocks_launch findings using the TWO-FIELD predicate (`blocks_launch AND status != "resolved"`), NOT a bare count** -- 6 resolved S1A/S1B findings legitimately keep `blocks_launch: true`; then set `launch_ready_core` and `launch_ready_seasoned`.
- **Cold-zone fall heat-floor mini-session (v1.5 candidate): ORDERING DECIDED (Trevor, 2026-05-28) -- do NOT re-litigate.** Runs as its own session AFTER the full lettuce gold standard completes (after the validation pass that flips both launch_ready flags), and BEFORE the builder+auditor pipeline replicates anchor shapes across the remaining ~114 crops. Generalizes the rule to spinach/radish/cilantro. Guardrail: no other anchor arc may pull cold-zone continuous-cadence crops into scope before v1.5 ratifies.

## launch_ready_core / launch_ready_seasoned (lettuce)

Both **false** at `verification_status.launch_ready_core` / `.launch_ready_seasoned`. Companions walk does not flip them. Pending: seasoned depth-lift, beginner-sibling pass(es), validation pass.

## Zone-level verification status (lettuce)

All 9 zones VERIFIED (S1B grid). Unchanged this session.

## What's locked / done

- Schema 2.7 live; Methodology v1.4.1 locked; language architecture v1.1; catalog hygiene complete
- soil_education (M9A) + ph_education (M9B) COMPLETE
- Cherry + beefsteak arcs + cleanups COMPLETE
- M12 scripted pass COMPLETE
- M13 S1A / S1B NA-NB-NC / S1C COMPLETE
- M13 S2C-NA + S2C-NB COMPLETE -- tips_by_stage 10/10 attributed; S2C CLOSED
- **M13 companions walk COMPLETE -- lettuce companions VERIFIED; provenance-only entry shape locked; sources_summary regenerated**
- **M13 seasoned depth-lift + beginner-sibling COMPLETE -- 3 tip-text fidelity fixes; 10/10 text_beginner + companions note_beginner authored; attribution byte-identical; launch flags still false**

## Soil field shape (all 123 crops, post-M12)

12-key gold-standard shape on all 123. The 6 vocab + 2 scalar fields populated on cherry-tomato, beefsteak-tomato, lettuce-leaf; null on the remaining 120.

## plantings anchoring_urls outer key

All 108 crops with plantings have `anchoring_urls: {}` at succession level. Per-crop URL logging at each crop's gold-standard arc.

## Open (non-blocking) items to revisit

- m12_audit_finding_001 (beefsteak soil key-order): cosmetic, blocks_launch false.
- s2c_na_finding_004: beefsteak top-level launch_ready_core/seasoned mirrors + verification_status.launch_ready that cherry lacks. Cross-anchor field-placement inconsistency; decide canonical shape at final audit before pipeline.
- **s2c_nb_finding_003 (RESOLVED this session): sources_summary regenerated at companions walk close** (companions added non-tip field sources, so regen fired). primary now includes `ucanr_ext` (soil) + `uga_ext` (soil, ph), both T1. primary=29, secondary=0, uncited=0. blocks_launch false.
- s2c_nb_finding_001 (NEW, medium): tip_xvfcfpdc "crowded greens bolt faster" clause not T1-supported (T1 ties bolting to heat/daylength). Airflow + smaller-leaves + spacing are anchored. -> seasoned depth-lift wording review.
- s2c_nb_finding_002 (NEW, low): tip_p5jti595 water-stress-as-standalone-bolt-trigger vs T1 heat-coupled framing. -> seasoned depth-lift.
- s2c_na_finding_001 / 002: germination tip prose-vs-source gaps (heat ceiling omitted; "sow thickly"). -> seasoned depth-lift.
- s2c_na_finding_003: germination thinnings=microgreens framing institution-anchored but synthesis-level; informational.
- **s2c_na_finding_001-004 in-record back-fill -- DECIDED (Trevor, 2026-05-28): back-fill at the validation pass.** These four are currently doc-only (NA findings .md + this file) and NOT in `verification_status.open_findings`. S2C-NB registered its own three in-record (s2c_nb_001/002/003). Action lives in Validation notes #2. (In-record open_findings currently holds 18: the S1A/S1B grid + the three s2c_nb findings.) Also confirm/back-fill S1C 001-003 if doc-only.
- Cherry: 18 findings dispositioned (12 resolved, 4 deferred).
- Beefsteak: 21 findings (12 resolved, 9 deferred).
- M9B anchoring_urls need manual browser verification (m9b_finding_001).
- Catalog session deferred: add `nrcs_soils`; 2 dangling refs (britannica, walter_reeves).
- Methodology doc correction deferred: `soil_education.textures.<vocab>` path in v1.4 doc -> correct to `soil_education.<vocab>`.
- Lettuce findings in crop record: s1a 008-009 + nb 001-005 + nc 001-004 + nc_methodology_candidate_001 + s2c_nb 001-003 + **m13_companions 001-005 (23 total in-record)**. S1C 001-003 and s2c_na 001-004 tracked in their findings docs (S1C: confirm in-record status alongside the NA-findings disposition above). **Of the 5 companions findings: 001/002/004 resolved, 003/005 open (final-audit items).**
- nb_finding_004 outer-field reconciliation -> separate cleanup pass.
- **blocks_launch counting (standing caution):** 6 resolved S1A/S1B findings (m13_s1a_008, m13_s1b_na_001/002/003, m13_s1b_nb_001, m13_s1b_nc_001) retain `blocks_launch: true` with `status: "resolved"` (records that they WERE blocking when filed). Any readiness gate MUST use the two-field predicate `blocks_launch AND status != "resolved"` (currently 0 unresolved), never a bare `blocks_launch` count (which returns 6). Verified field-by-field against live data at the depth-lift session.

## Lettuce-specific notes for Claude Code / future sessions

- succession_policy.window_type: "continuous" (Type 2 crop).
- Zone 10: single direct_sow (fall/winter only).
- Zones 8-10 harvest_end primary: bolt_threshold_start - 5.
- Zone 3 fall (post-NC): sow first_frost - 76 (~Jul 1), harvest_start +45 (looseleaf). Zones 4-5 fall: retain first_frost - 90.
- Catalog is richer than kickoff "likely-useful" subsets. Real T1 IDs used for tips: umn_ext, umd_ext, uiuc_ext, uwi_hort (Wisconsin Horticulture, NOT uwex/uwisc), ncsu_ext, clemson_hgic, cornell_ext, ucanr_ext (covers UC ANR Master Gardener county pages at institution level), uc_ipm, uf_ifas (NOT ufifas_ext), ndsu_ext, msu_ext, psu_ext, usu_ext, unl_ext, iastate_ext, wvu_ext, ucd_postharvest. Purdue is NOT in the catalog.
- **Attribution-only sessions do NOT edit tip text or text_beginner.** File findings for prose problems; do not rewrite.
- **sources_summary is derived from NON-TIP field-level sources only** (tier-grouped: primary=T1, secondary=T2, uncited=other). Tip attribution does NOT feed it. Regenerate (never hand-edit) only when non-tip field sources change.

## Pre-buildout final audit queue (9-anchor cross-consistency sweep)

**CARRY THIS SECTION FORWARD** at each session-close regeneration.

---

### >>> CANONICAL SHAPE-SPEC + CONFORMANCE GATE -- ORDERING DECIDED (Trevor, 2026-05-28) <<<

**The 9 gold-standard anchors are the schema-by-example. The builder+auditor bots replicate an exemplar's shape across ~114 crops; if the anchors disagree in shape, the drift propagates or the auditor can't express a single invariant. So all 9 anchors MUST be shape-identical before any bot runs.**

**ORDERING (do NOT re-litigate; the word "after" means after LETTUCE, not after the 9):**
1. **Finish the lettuce arc clean** (depth-lift -> beginner-sibling -> validation pass). Lettuce already conforms to the one settled decision (provenance-only).
2. **Ratify the canonical shape-spec NEXT -- AFTER LETTUCE, BEFORE ANCHOR 4.** This is the DECISION, not the cleanup: diff the worked anchors field by field, resolve each divergence to ONE canonical answer (Trevor adjudicates), freeze the spec. Natural home = the v1.5 session slot (already runs after lettuce, before broad buildout); SPLIT into its own session if the field-set diff is heavy (the top-level key-count spread 60/55/50 may make it heavy -- scope at the v1.5 kickoff).
3. **Author anchors 4-9 to the frozen spec** so they never need retrofitting.
4. **Retro cherry + beefsteak + run the CONFORMANCE GATE -- AFTER STRAWBERRY (9th), as a HARD, PIPELINE-BLOCKING gate.** By then 4-9 already conform; the gate confirms and retrofits only the two early anchors.

**Why ratify early, clean late:** deferring the spec DECISION to "the end" recreates the exact cherry/beefsteak drift six more times (anchors 4-9 authored against no shared shape) and balloons the retrofit from 2 anchors to up to 8, discovered at the worst moment. Decide early (cheap insurance), clean up late (the gate).

**CAVEAT on the gate:** a conformance gate checks that all 9 are MUTUALLY IDENTICAL in shape; it does NOT check the shape is CORRECT (9 identically-wrong anchors pass). Its value depends entirely on the shape-spec being ratified deliberately, once, by Trevor -- not inferred from whichever anchor the gate reads first.

**SETTLED so far (1 of N fields):** companion entry shape = provenance-only (Trevor, 2026-05-28). Even this is not yet REALIZED across anchors (only lettuce conforms; cherry+beefsteak need retrofit).

**KNOWN-OPEN divergences the spec must resolve (from the 3 worked anchors; NOT exhaustive):**
- **Companion entry trio:** lettuce 7 clean / cherry 11 full-trio / beefsteak 3 clean + 6 full + 1 partial. (Decision made -> provenance-only; realization pending = retrofit.)
- **launch_ready placement (s2c_na_finding_004):** cherry = verification_status.launch_ready_core only; beefsteak = that + top-level mirror + legacy verification_status.launch_ready; lettuce = cherry-style. UNSETTLED -- pick canonical placement.
- **bad_core minimum (m13_companions_finding_003):** cherry/beefsteak = 3; lettuce = 0. UNSETTLED -- allow empty vs require N.
- **Top-level key-count spread 60/55/50:** SOME is legitimate (different crops carry different fields, e.g. tip stage sets); SOME may be drift. NEEDS A FIELD-LEVEL DIFF to separate biology from drift. Not yet done.

**STATUS: shape-spec UNSETTLED.** Only the ordering above is decided. No shape CONTENT is committed. The spec is its own work item (diff/decide/freeze), scoped at the v1.5 kickoff.

---

**Anchor completion tracker:** 2 of 9 complete -- cherry (M6), beefsteak (M7). Lettuce arc in progress (zones + soil + pH + ALL tips + companions done; depth-lift + beginner-sibling + validation remain). Remaining anchors: lettuce + 6 more per ROADMAP; strawberry is the 9th.

**Queue:**

1. **m12_audit_finding_001 -- beefsteak soil key-order.** Cosmetic. Blocks launch: false.

2. **m13_s1a_cross_anchor_note -- lettuce tips_by_stage stage set differs from cherry.** Cherry: germination, seedling, established, flowering, harvest, end_of_season. Lettuce: germination, seedling, established, harvest, bolting. Appropriate; informational.

3. **m13_s1b_na_type2_crop_note -- Type 2 continuous cadence on lettuce.** Other continuous-cadence crops (radish, cilantro, spinach) should use `continuous`. Cherry/beefsteak correctly `spring_fall` (Type 1). Track both types.

4. **m13_s1b_nb_outer_field_note -- outer fields use legacy/untraced estimates.** Reconcile ALL zones in one outer-field sweep at final audit.

5. **m13_s1b_nc_methodology_candidate_001 -- cold-zone fall heat-floor rule (v1.5 candidate).** first_frost - 90 mis-fires where frost precedes ~Oct 1. **ORDERING DECIDED (Trevor, 2026-05-28):** ratify in its own session AFTER lettuce gold standard completes, BEFORE the builder+auditor pipeline. Generalize to spinach/radish/cilantro. Do not re-litigate ordering.

6. **s1c_finding_003 -- lettuce tolerated pH lower bound at preferred floor [6.0,7.0].** No lettuce-specific T1 sub-6.0 tolerated value; do NOT propagate tomato's [5.5,7.0]. Cool-season-greens archetype consistency item. Blocks launch: false.

7. **s2c_na_finding_004 -- launch_ready field placement inconsistency between anchors.** beefsteak has top-level launch_ready_core/seasoned mirrors + verification_status.launch_ready; cherry has verification_status-only. Decide canonical shape before pipeline replicates anchor shapes across ~114 crops. Blocks launch: false. **TIES TO #11 (provenance-only companion shape).**

8. **s2c_nb_finding_003 -- sources_summary regeneration owed (lettuce).** **RESOLVED this session** (companions walk regenerated; ucanr_ext + uga_ext confirmed in primary). Retained here for audit-trail visibility only.

9. **NA-findings-in-record back-fill -- DECIDED: back-fill at the validation pass (Validation notes #2).** s2c_na_finding_001-004 (and confirm S1C 001-003) are doc-tracked but not in `verification_status.open_findings`. Back-fill so open_findings is the single source of truth before the pipeline. Blocks launch: false.

10. **m13_companions_finding_003 -- lettuce bad_core is EMPTY.** Cherry/beefsteak have populated bad_core; lettuce has no anti-companion that clears the T1 first-season-warning bar. Decide canonical handling (allow empty vs require N) before pipeline. Do NOT pad with unearned claims. Blocks launch: false.

11. **m13_companions_finding_005 -- provenance-only companion entry shape (all 9 anchors must match).** Lettuce companions written provenance-only (legacy evidence_label/confidence/verified_against_sources trio dropped); DECIDED canonical (Trevor, 2026-05-28). Realization across anchors: lettuce 7 clean; cherry 11 full-trio (all need retrofit); beefsteak internally inconsistent -- 3 clean (Basil, Marigolds, Fennel) + 6 full-trio (Nasturtiums, Borage, Carrots, Corn, Potatoes, Eggplant) + 1 PARTIAL-trio (Brassicas: evidence_label + confidence, no verified_against_sources). The partial entry is the worst case -- it makes any "mirror must agree with provenance" auditor rule ambiguous to even write. Retrofit = cherry (11) + beefsteak (7 non-conforming). Ties to #7 and the shape-spec block above. Blocks launch: false.

12. **CROSS-ANCHOR SHAPE-CONFORMANCE GATE (HARD, pipeline-blocking) -- NEW.** After strawberry (9th anchor) closes, BLOCK the builder+auditor pipeline until a gate confirms all 9 anchors are shape-identical field by field (companion entries provenance-only; launch_ready placement canonical; bad_core handling canonical; soil key-order; full field-set reconciled against the 60/55/50 spread). Gate reads the ratified shape-spec (see block above) as both the builder's stamp and the auditor's invariant. Gate CONFIRMS conformance + retrofits cherry/beefsteak; it does NOT decide the shape (that is the spec, ratified earlier per ordering). s2c_na_finding_004 (#7) is the launch_ready instance of this same class. Blocks pipeline: TRUE.

---

*Update this file at each session close. Authored by Claude; deployed by the promotion command to both `~/plant-dataset/` and `~/Documents/plant-project/00-current/`.*
