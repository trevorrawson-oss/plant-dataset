# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile.
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.4.1**) BEFORE acting. Do not infer the next action from "a cell is done" -- check the checklist. The checklist's auto-derived denominator is authority over any kickoff's named field list.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it (the past near-miss came from header-only patches). At session close, **fully regenerate this whole file** from the true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry there at close, never rewrite it. That file is the recovery net.
> 5. **CLOSE RITUAL (every session ends here).** If the dataset changed: PROMOTE -- write canonical, re-pin `LATEST.txt` (new SHA + date + session). Then ALWAYS: regenerate this file (#3), append to `STATE_HISTORY.md` (#4), sync `00-current/`, and commit (+ push).

---

## Canonical pointer
- **Current SHA:** `37bfc12d9f3607b17ff8c18c78a66bbb1f6da02088a1aefebd4eb505806e7297` (M15 lettuce Step 11 -- 45-slot anchoring apply + whole-crop gate re-run + s11 findings registration). `LATEST.txt` session line: `m15_lettuce_step11_apply_and_gate`.
- **Predecessor chain:** `37bfc12d` <- `cdcbf175` (the 45-slot apply, same session) <- `df4d24c7` (S10-5 jargon strip) <- `da4b8bc5` (Step 9) <- `7e9eeceb` (Steps 7/8) <- `5224e13a` (Step 6d) <- `0dfd835a` (6c) <- `1e19948c` (6b) <- `61cddea3` (6a) <- `e27eec14` <- `815efe62` <- `8a1d8a50` <- `ed495666` <- `20f9fc2b` <- `327a2d5c` <- `582dbbad`.
- bf_003 (SHA-lineage doc-lag) **RESOLVED** -- this regeneration pins the truthful chain.
- Every PROMOTE re-pins this SHA and `LATEST.txt`. Confirm at session start (protocol #1).

## Active work + exact next step
- **Crop in flight:** `lettuce-leaf` (crops index 33). Top-level dict of 14 keys; lettuce crop dict = 55 keys.
- **Done:** region-cell STRUCTURAL slice; Phase-0 gap-fixes; Steps 6a-6d; Steps 7/8 (dual-voice gate 130/0/0); Step 9 (dash + °F); Step 10 (§3 8/8; source-tier; anchoring hygiene layered; §4 spot-check clean); Step 11 S10-5 jargon strip; Step 11 URL discovery (45 slots verified); **Step 11 -- THE 45-SLOT ATOMIC APPLY (2026-06-05, Claude Code)** -- 22 leaves / 68 `{url, verified}` entries, all audits PASS; **Step 11 -- FIRST whole-crop gate re-run** incl. the first systematic copyright/verbatim scan; **Step 11 -- Step 5.5 re-walk + NA-3h reconciliation re-verified** (keep-materialized stands; §3b-i holds live).
- ⚠️ **THE FLIP DID NOT HAPPEN -- BLOCKED BY THE GATE (2 real findings).** Flags held `(launch_ready_core=False, launch_ready_seasoned=False, status=unverified)`. This is the gate WORKING: the first systematic run yielded net-new findings the spot-checks could not see. Both blockers are registered in `verification_status.open_findings` with `blocks_launch:true`, so the two-field predicate now blocks any premature flip mechanically.
- **NEXT (to finish Step 11):**
  1. **claude.ai lane:** close `s11_finding_001` (anchor `harvest_ready_anchoring_urls` 5 IDs + `description_anchoring_urls` 2 IDs; 6 of 7 are claim-type confirmations on already-fetch-verified URLs; `uiuc_ext` is genuine discovery) + `s11_finding_002` (own-voice rewrite of `soil.preferred_description_seasoned`; it near-verbatims its own first-cited NCSU anchor). Also owed there: rule on `s11_finding_003` (recommended benign), re-source `s11_finding_004` (2 dead URLs), Appendix-A registration (parallelizable, not blocked).
  2. **Claude Code (short session):** apply the write-backs, re-run the whole-crop gate, **flip on 0 violations** (gate #1 only; `status` stays unverified-or-successor, NOT gold_standard until M16 settles status vocab).
- Then **M16 = cherry + beefsteak regression** (built but not flipped; 0 of 9 anchors flipped today).

## Step 11 gate results (2026-06-05 run, post-apply live data)
- §3 cross-field: **8/8 PASS**. Dual-voice structural walk: **130 populated / 0 missing / 0 null** (= Steps-7/8 result). Dash gate: user-facing `--` = **0**. °F sole form: **clean**. Source-tier: 40 source IDs, all catalogued T1. Roster gate (`tools/register_completeness_gate.py`): **PASS dataset-wide**. Anchoring 1A: all 22 applied leaves **CLOSE**.
- **OPEN -- s11_finding_001 (blocks_launch):** `harvest_ready_sources` (iastate/umn/ndsu/umd/uiuc) anchoring EMPTY + `description_sources` (umd/umn) anchoring KEY ABSENT. Sibling-named pairs the RULING-1 predicate scan structurally missed; both provers anchor them. **Pipeline lesson: the anchoring gate must match `*_sources`/`*_anchoring_urls` sibling pairs, not just literal `sources` keys** -- fold into checklist amendment 8 + the schema-gate addendum.
- **OPEN -- s11_finding_002 (blocks_launch):** copyright scan hard hit -- `soil.preferred_description_seasoned` shares a 10-word verbatim run + sentence skeleton with `ncsu_ext` content.ces.ncsu.edu/lettuce (its own first-cited anchor). Step 10's spot-check passed this field vs UMN; the lift was from the un-fetched source. Voice-lane rewrite owed.
- **OPEN -- s11_finding_003 (non-blocking, low):** 8-word threshold trip on a generic transplant-age phrase (`start_method.notes_beginner` vs usu_ext); recommended benign, voice-lane judgment owed.
- **OPEN -- s11_finding_004 (non-blocking, medium):** link-rot -- uga_ext white-county PDF + uariz_ext az1099 both 404 (4 anchor slots across se_gulf + low_desert_az); re-source owed. Scan coverage: 68/86 URLs text-compared (11 PDFs, 3 bot-blocks, 2 JS-rendered, 2 dead not compared).
- Copyright scan stats for the record: 294 user-facing prose strings; 41 borderline 6-7-word hits all benign-class (citations / attributions / universal facts / numeric conventions).

## Flip gates (the four distinct "flips" -- never conflate them)
1. **Per-crop `launch_ready` flip** -- one crop goes live. **Gate:** that crop's Step 11 returns 0 violations. Lettuce is 2 findings away (s11_finding_001 + 002). **0 of 9 anchors flipped; cherry + beefsteak owe M16 regression.**
2. **Region read-layer flip** -- renderer reads `regions{}` first. **Gate:** shape proven on the 3 provers; ships with `zones{}` fallback.
3. **Authoring-model flip** -- carrots onward authored region-first. **Gate:** 3 provers done.
4. **Schema perennial bump** (`lifecycle_override`) -- FUTURE, **2.9+ (NOT 2.8)**. After carrots.

**Schema version lineage:** 2.7.5 -> **2.8 = register-suffix conversion (current)** -> region read-layer flip + perennial extension are **2.9+**.

## Live locked decisions / guardrails
- **Anchoring gate is LAYER-SCOPED (1A, Trevor 2026-06-04)** -- claim-bearing leaves only; legacy `zones{}` (58 leaves) + the 10 `regions{}` root rollup `sources` arrays EXCLUDED BY DEFINITION. **Amended by s11_finding_001:** the predicate must also match sibling-named `*_sources`/`*_anchoring_urls` pairs (`harvest_ready_*`, `description_*`).
- **Leaf-URL convention:** leaf `anchoring_urls` = the SPECIFIC lettuce-bearing publication URL; `verified` = the date lettuce content was confirmed present; catalog `url` may stay a portal root for multi-publication institutions. Store the canonical (resolving) URL form, not a redirecting form.
- **Segment-parent `plantings[0].anchoring_urls:{}` stays empty** (5-of-8-regions precedent; normalize-or-vestigial decision is a pre-buildout audit-queue item, NOT lettuce-arc).
- **`basis_seasoned` voice standard (S10-5):** seasoned-only (SP), no beginner sibling; classifier reasoning lives in the structural `classification` key.
- **Governing checklist: v1.4.1.** Dataset is authoritative for what is true; flag doc lag, don't author against missing fields.
- **Lane split.** Dataset STRUCTURAL/MECHANICAL work = **Claude Code** (applies, gates, collateral audits, SHA re-pins, the flip). Biology windows + consumer copy + voice/IP judgment + anchoring-URL DISCOVERY/verification + Appendix-A registration = **claude.ai**.
- **Per-crop pipeline (target):** Claude Code shell pass -> claude.ai biology + copy -> Claude Code certifies (Step 11) -> Claude Code gated deletion.
- **Lettuce authors into `regions{}`;** keep `zones{}` coherent until Phase C.
- **Inheritance is candidate, not verified (v1.4.1 §4).**
- **Pest/disease = highest-scrutiny cluster.**
- **Micro-strings are at-bar-by-nature for the seasoned lift but DO take a `_beginner` sibling.**
- **`cause_beginner` ruling:** register transform; may be byte-identical where seasoned carries no jargon.
- **TEMPERATURE NOTATION -- canonical `°F`** user-facing; backend notes retain whatever form.
- **DASH CONVENTION -- per-sense, per-crop.** Lettuce clean; other 122 crops still carry `--` (~5,360 user-facing) -- **F-6d-2 STILL OPEN**.
- **Deletion gate (legacy `zones{}`):** Phase C, per crop, after region carries everything + consumers read region-first + round-trip + frost-input independence. `safe_sowing_note` precondition not met (FINDING 6c-2).
- **Succession-shape rule (spec §3b-i):** rule lives ONCE in region-constant `plantings[]`; app recomputes and IGNORES `resolved_by_zone`; northern_tier's materialized `succession_spring`/`succession_fall` strings are kept-by-evidence (Pass 1b regeneration-equality; re-verified at Step 11).
- **`year_round` encoding** for pauseless cells; **`track` semantics:** `beginner` = shared MAIN calendar, `succession` = seasoned-only.
- **Register-conversion convention.** `X_seasoned` + (`X_beginner` for CP, absent for SP); presence IS the visibility declaration.

## Open items owed
- **Step 11 -- s11_finding_001 backfill (claude.ai then Claude Code):** harvest_ready (5) + description (2) anchoring entries; uiuc_ext discovery.
- **Step 11 -- s11_finding_002 rewrite (claude.ai voice lane):** own-voice `soil.preferred_description_seasoned`.
- **Step 11 -- s11_finding_003 ruling + s11_finding_004 re-source (claude.ai):** benign-rec judgment; 2 dead URLs; optional sweep of the 18 verbatim-scan-uncovered URLs (11 PDFs etc.).
- **Step 11 -- the flip (Claude Code, last act):** on 0 violations after the above land.
- **Step 11 -- Appendix-A registration (claude.ai, parallelizable NOW):** bolting register keys + `bolting.triggers` ruling (S9-1) + ~26 register-conversion rulings + succession strings + se_gulf_month_resolution + 6b container key-pairs + Steps 7/8 `_beginner` keys (97) + region `tip_overrides` leaf-keys.
- **FINDING S9-1** (`bolting.triggers` Appendix-A ruling) -- rides the registration above.
- **doc note:** whether bolting prose carries its own source set vs inheriting -- Appendix-A coverage question (claude.ai).
- **Dual-voice gate (WORRY 3) STILL OWED:** the v2 STRUCTURAL walk exists only in the claude.ai transcript + was rebuilt ad hoc for this gate run; ship it into `tools/` + pipeline `rubric.md` as the admission HALT.
- **Gold-standard arc checklist amendments (claude.ai):** (1) per-step lane tags; (2) shell-pass-first Steps 4-5; (3) Step 11 flip-disambiguation; (4) per-crop deletion gate; (5) Step 8 structural walk wording; (6) Step 9 leaf-set derivation; (7) Step 10 layer scoping; (8) the 1A layer-scoped anchoring gate **+ the s11_finding_001 sibling-pair predicate fix**.
- **Pre-buildout audit-queue:** segment-parent `plantings[0].anchoring_urls` 3-populate/5-empty inconsistency across verified regions -- normalize before the bot pipeline scales.
- **Pipeline / operating-model doc -- TO BE DESIGNED** (own session after lettuce is gold-standard).
- **`safe_sowing_note` migration (FINDING 6c-2):** Phase C, Claude Code.
- **Deferred vocabulary session:** rename `track` value `beginner` -> `main`.
- **Companions reconciliation session (§5):** array-level register split; lettuce's 3 `why_seasoned`-with-null-`why_beginner` correctly OUT OF SCOPE until then.

## Inherited findings (unchanged)
- `finding_001` -- warm `zones{}` 8-11 SE-mis-sourced (legacy layer, own pass); legacy empty-`{}` anchoring is deferred re-sourcing, not a gap (excluded by 1A by definition).
- na3d-na3g sourcing-sibling findings; `na3d_finding_003` cosmetic.
- Two-field predicate: `blocks_launch AND status != "resolved"` -- now returns **2 unresolved blockers** (s11_finding_001, s11_finding_002), correctly blocking flip gate #1.

*Update this file at each session close.*
