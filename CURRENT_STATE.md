# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile.
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.4.1**) BEFORE acting. Do not infer the next action from "a cell is done" -- check the checklist. The checklist's auto-derived denominator is authority over any kickoff's named field list.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it (the past near-miss came from header-only patches). At session close, **fully regenerate this whole file** from the true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry there at close, never rewrite it. That file is the recovery net.
> 5. **CLOSE RITUAL (every session ends here).** If the dataset changed: PROMOTE -- write canonical, re-pin `LATEST.txt` (new SHA + date + session). Then ALWAYS: regenerate this file (#3), append to `STATE_HISTORY.md` (#4), sync `00-current/`, and commit (+ push).

---

## ⚠️ THIS SESSION DID NOT MUTATE THE DATASET
**2026-06-05 was URL DISCOVERY + verification only (claude.ai lane).** The 45-slot atomic apply is **VERIFIED + STAGED but UNWRITTEN.** The SHA is UNCHANGED (`df4d24c7…`). The next dataset mutation is the apply itself, which runs in **Claude Code** (structural lane). Do not read this file as "the backfill is applied" -- it is staged. Claude Code will regenerate this file again post-apply with the new SHA.

## Canonical pointer
- **Current SHA:** `df4d24c723b19d8883db8c46f05b981659ef74e359e906a491b7cb9f28bafa3c` (M15 lettuce Step 11 -- S10-5 `basis_seasoned` + `count_note_seasoned` classifier-jargon strip). `LATEST.txt` session line: `m15_lettuce_step11_s10_5_basis_jargon_strip`. **UNCHANGED this session** (discovery + verification only; no write).
- **Immediate predecessor:** `da4b8bc51dc935b0efce115a6405cb7fb82e3e927e520767757fff2e8062dec2` (M15 lettuce Step 9 -- dash gate + dataset-wide temperature normalization; Step 10 was state-only and did not re-pin).
- **Predecessor chain:** `da4b8bc5` <- `7e9eeceb` (Steps 7/8) <- `5224e13a` (Step 6d) <- `0dfd835a` (6c) <- `1e19948c` (6b) <- `61cddea3` (6a) <- `e27eec14` (freezer micro-addendum) <- `815efe62` (register-conversion completion) <- `8a1d8a50` (bolting) <- `ed495666` (Pass 2) <- `20f9fc2b` (Pass 1b) <- `327a2d5c` (Pass 1a) <- `582dbbad` (northern_tier).
- ⚠️ **SHA-lineage doc-lag flag (bf_003, still open):** earlier CURRENT_STATE predecessor chains ran through `da4b8bc5`; `LATEST.txt` + kickoffs name `df4d24c7` as the post-S10-5 SHA. Dataset is clean (uploaded JSON == LATEST.txt == `df4d24c7` confirmed at this session's preflight). Reconcile which SHA the canonical CURRENT_STATE pins when convenient; not blocking.
- Every PROMOTE re-pins this SHA and `LATEST.txt`. Confirm at session start (protocol #1).

## Active work + exact next step
- **Crop in flight:** `lettuce-leaf` (crops index 33). Top-level is a dict of 14 keys (the 14th is `region_source_map`). Lettuce crop dict = 55 keys.
- **Done:** region-cell STRUCTURAL slice; Phase-0 register-conversion gap-fixes; checklist synced to v1.4.1; **Step 6a/6b/6c/6d** (seasoned depth-lift); **Steps 7/8** (`_beginner` siblings + dual-voice coverage gate); **Step 9** (dash gate + `°F` normalization); **Step 10** (cross-field §3 = 8/8 PASS; source-tier PASS; anchoring-URL hygiene layered, gaps registered S10-1..S10-4; copyright/attribution §4 CLEAN); **Step 11 -- S10-5 jargon strip APPLIED** (prior session); **Step 11 -- anchoring-URL DISCOVERY COMPLETE this session** (all 45 apply-set slots verified; see below).
- **NEXT (within Step 11): the 45-slot atomic apply** (Claude Code lane), then the whole-crop gate re-run + Step 5.5 re-walk + northern_tier-vs-warm succession reconciliation + Appendix-A registration. **The lettuce flag-flip is the LAST act of Step 11, ONLY on 0 violations.**
- ⚠️ **The flip is NOT done.** Flags remain `(launch_ready_core=False, launch_ready_seasoned=False, status=unverified)`. Step 11 still owes the apply + whole-crop re-run + succession reconciliation + Appendix-A before the flip is even eligible.

## Step 11 progress so far -- anchoring-URL discovery COMPLETE (2026-06-05), apply STAGED
- **What ran (claude.ai lane, no dataset write):** the full anchoring-URL discovery + fetch-verification for the apply set. Outcome: **all 45 slots verified, staged for ONE atomic SHA-gated write.** Evidence record: `m15_northern_tier_url_discovery_log.md` (presented to Trevor 2026-06-05).
- **The 45-slot apply set (held for Claude Code):**
  - **crop-field 7 (21 slots)** -- VERIFIED prior session, carried: `storage` (5: umn/umd/iastate/clemson_hgic/ucd_postharvest); `rotation` (1: +`uwi_hort`; umn_ext already anchored in-tree); `failure_diagnostics[0–4]` (3 each: umn/umd/iastate = 15).
  - **se_gulf (13 slots)** -- VERIFIED prior session: `plantings[0]` reuse (3); `resolved_by_zone[8]` (5); `resolved_by_zone[9]` (5).
  - **northern_tier (11 slots)** -- VERIFIED THIS SESSION via URL DISCOVERY + fetch-verify (NOT promotion -- see the corrected scope below). 6 `plantings[0]` segment-objects + 5 `resolved_by_zone[3–7]` cells.
- **northern_tier 11-leaf discovery detail (this session):** each source's lettuce-bearing, claim-type-matched T1 URL discovered + fetch-confirmed (lettuce content present on the page). Genuine-discovery cold-climate sources: `msu_ext` (Lower Peninsula Garden Calendar), `ndsu_ext` (**H1754 "From Garden to Table: Leafy Greens!"** -- home-garden Extension pub, McGinnis; upgraded from children's pub FN1372 per Trevor 2026-06-05), `msu_bozeman` (Montana Grown fact sheet), `umaine_ext` ("Keep Your Garden Growing" -- NOT the planting-chart, which has no lettuce row), `psu_ext` ("Seeds or Transplants?"), `vce_426_331` (Pub 426-331 per-zone lettuce tables), `cornell_ext` (Warren Co. fall-planting frost table -- matched to its harvest_end claim type), `ncsu_ext` (AG-756-01 central-NC calendar), `uwi_hort` ("Grow Your Own Salad Greens" -- planting-date page, NOT the in-tree rotation PDF). Reuse URLs re-confirmed live + lettuce-bearing: `umn_ext`, `umd_ext`, `iastate_ext`, `clemson_hgic`, `uga_c1258_fall`.
- **Convention applied:** leaf `anchoring_urls` value = the SPECIFIC lettuce-bearing publication URL; `verified` = session date (lettuce content confirmed present). Catalog `url` may stay a portal/domain root for multi-publication institutions; specificity at the leaf.
- **`umn_ext` URL canonicalization (Trevor deferred → Claude call 2026-06-05):** write the canonical destination `extension.umn.edu/vegetables/growing-lettuce-endive-and-radicchio` (the kickoff's `/yard-and-garden/vegetables/...` form 301-redirects to it); store the resolving canonical, not the redirecting form.
- **Two candidates REJECTED (logged so they are not re-tried):** umaine_ext planting-chart (genuine dated T1 chart but **no lettuce row**); msu_ext generic veg tip-sheet (no lettuce-specific date) -- both fail the lettuce-present / claim-type-match convention.
- **Lane:** discovery + verification authored by claude.ai (T1 biology + evidence judgment). The atomic apply, collateral audit, end-SHA re-pin, and close ritual are **Claude Code**.
- **Flip-guard held:** `(False, False, unverified)`.

## Apply discipline for the staged 45-slot write (Claude Code, NEXT)
- Copy dataset to `/home/claude/` before parsing (mount flakiness).
- Start-SHA verified == `df4d24c723b19d8883db8c46f05b981659ef74e359e906a491b7cb9f28bafa3c` before any write; `sys.exit(1)` on mismatch.
- Write minified: `json.dump(data, f, separators=(',',':'))` -- NOT indent=2.
- Collateral audit: only `crops[33]` (lettuce-leaf) changes; all 122 other crops byte-identical; all top-level non-crop keys byte-identical. Within lettuce, ONLY the 45 `anchoring_urls` slots change, nothing else.
- `verified` date on all new slots = the apply session date.
- End-SHA confirmed after write; re-pin `LATEST.txt`; Trevor promotes manually; regenerate this file post-apply.
- **Scope confirmed (Trevor 2026-06-05):** `plantings[0].anchoring_urls:{}` at the SEGMENT-PARENT level is NOT in the apply set. In-tree precedent: 5 of 8 already-verified regions (incl. se_gulf) leave that parent slot empty `{}` while fully populated at the segment level, so the whole-crop gate does NOT require it. Apply set stays at 45. (Side-finding for the pre-buildout audit queue, NOT this arc: the 3-populate/5-empty split across verified regions is itself an inconsistency worth a sweep -- either the parent slot means something or it is vestigial.)

## Flip gates (the four distinct "flips" -- never conflate them)
1. **Per-crop `launch_ready` flip** -- one crop becomes gold-standard / goes live. **Gate:** that crop's Step 11 returns 0 violations. Flags under `verification_status`: `launch_ready_core` / `launch_ready_seasoned` / `status`. (Held False/False/unverified.) **NOTE: 0 of 9 anchors are flipped today; lettuce is the apply + whole-crop gate away from being the first; cherry + beefsteak are built but NOT flipped -- they owe their M16 regression pass.**
2. **Region read-layer flip** -- renderer reads `regions{}` first. **Gate:** shape proven on the 3 provers (lettuce in progress; cherry + beefsteak owe M16); shipped with a `zones{}` fallback.
3. **Authoring-model flip** -- carrots and every later crop authored region-first. **Gate:** 3 provers done.
4. **Schema perennial bump** (`lifecycle_override`, perennial support) -- FUTURE, **2.9+ (NOT 2.8)**. After carrots. Decoupled from #2.

**Schema version lineage:** 2.7.5 (additive region scaffolding) -> **2.8 = register-suffix conversion (DONE; current `schema_version`)** -> future bumps re-number off 2.8. Region read-layer flip (#2) + perennial extension (#4) are **2.9+**. The region-primary spec's "2.8 breaking flip" label is stale; re-number to 2.9 when built.

## Live locked decisions / guardrails
- **Anchoring gate is LAYER-SCOPED (1A, Trevor 2026-06-04).** The `launch_ready_core` anchoring check counts claim-bearing leaves only. EXCLUDED by definition (not deleted): the legacy `zones{}` layer (superseded; Phase-C deletion path) and the 10 `regions{}` root rollup `sources` arrays (summary nodes; evidence lives on the child claims). The whole-crop predicate scan returns 90 nodes with non-empty `sources`; layer-scoping reduces the real backfill to the 45-slot apply set (7 crop-field + 13 se_gulf + 11 northern_tier + the 14 already-anchored region/reuse leaves now verified). Encode in the schema-gate addendum + checklist amendment 7 + 8 so the bot pipeline runs it identically.
- **`basis_seasoned` voice standard (S10-5, Trevor 2026-06-04).** Seasoned-only (SP), no beginner sibling; classifier reasoning in the structural `classification` key, not the prose. Sets the basis-prose voice standard for cherry/beefsteak/carrot.
- **Governing checklist: v1.4.1.** When checklist text and live dataset shape disagree, the **dataset is authoritative for what is true** -- flag the doc lag, do not author against fields that don't exist.
- **Lane split.** Dataset STRUCTURAL/MECHANICAL work = **Claude Code** (incl. the 45-slot apply, the whole-crop gate re-run, the succession reconciliation, and the flip). Biology windows from T1 sources + consumer copy authoring + voice/IP judgment + anchoring-URL DISCOVERY/verification = **claude.ai**. Appendix-A registration + doc-notes = **claude.ai** (parallelizable; not apply-blocked). The whole-crop validation + promote + close ritual = **Claude Code**; voice rulings within Step 11 (e.g. S10-5) + evidence discovery = claude.ai.
- **Per-crop pipeline (target):** Claude Code shell pass -> claude.ai fills biology gaps + copy -> Claude Code certifies (Step 11) -> Claude Code gated deletion.
- **Lettuce authors into `regions{}` this arc;** keep `zones{}` coherent until Phase C.
- **Inheritance is candidate, not verified (v1.4.1 §4).** Verification status does NOT inherit; side-by-side check vs live T1 always required.
- **Pest/disease = highest-scrutiny cluster (full cherry-anchor rigor).**
- **Micro-strings are at-bar-by-nature (depth-exempt) for the SEASONED lift, but DO take a `_beginner` sibling.**
- **`cause_beginner` ruling (Trevor 2026-05-30):** register transform, same biological content, plainer grammar; may be byte-identical to `_seasoned` where the seasoned carries no jargon.
- **TEMPERATURE NOTATION -- CANONICAL `°F` (Trevor 2026-06-04).** User-facing temperature renders as the degree symbol `°F`, no space. Backend notes retain whatever form.
- **DASH CONVENTION -- per-sense, per-crop (F-6d-2 re-scoped 2026-06-04).** User-facing `--` resolves by SENSE (aside→comma; label→colon; joined clauses→semicolon). Lettuce's 17 done at Step 9. Other 122 crops still carry `--` (~5,360 user-facing) -- **F-6d-2 STILL OPEN**.
- **Deletion gate (legacy `zones{}`):** delete ONLY at Phase C, per crop, AFTER region cell carries everything zones held + all consumers read region-first + round-trip + frost-input independence. `safe_sowing_note` precondition not yet met (FINDING 6c-2).
- **Succession-shape rule (spec §3b-i):** succession RULE lives ONCE in region-constant `plantings[]` (`track:"succession"`); app recomputes from `plantings[]` + live frost, IGNORES `resolved_by_zone`.
- **`year_round` encoding** for pauseless cells. **`track` semantics:** `beginner` = shared MAIN calendar; `succession` = seasoned-only.
- **Register-conversion convention.** Register-bearing prose is `X_seasoned` + (`X_beginner` for CP, absent for SP); presence IS the visibility declaration. Bare-null-of-ruled-stem = ruled-empty PASS.

## Open items owed
- **Step 11 -- 45-slot atomic apply (NEXT, Claude Code):** the verified+staged anchoring write (crop-field 7 = 21, se_gulf = 13, northern_tier = 11). Discipline block above. Discovery + verification DONE this session; only the write remains.
- **Step 11 -- whole-crop gate re-run** (after the apply, Claude Code): §3 cross-field; `dual_voice_gate_v2.py`; lettuce user-facing `--` = 0; `°F` sole; source-tier; anchoring completeness post-apply (all 45 close). **⚠️ This run includes the copyright/verbatim scan as a flip-blocking rubric criterion -- the FIRST audit of lettuce's OWN user-facing prose (the `_beginner`/`_seasoned` voice fields, tips, failure-diagnostics) against extension-source wording. NOT yet done. A flag here is the gate working, not a setback; route any prose fix to the claude.ai lane.**
- **Step 11 -- Step 5.5 re-walk + northern_tier-vs-warm succession-shape reconciliation** (NA-3h open finding; region-primary §3b-i: no rule-bearing succession structure in `resolved_by_zone`; likely collapse northern_tier to the generative rule like the warm cells). Claude Code.
- **Step 11 -- Appendix-A registration (claude.ai lane, parallelizable NOW -- not apply-blocked):** bolting register keys + `bolting.triggers` ruling (S9-1) + ~26 register-conversion field rulings + succession strings + se_gulf_month_resolution + 6b container conversion key-pairs + Steps 7/8 `_beginner` keys (97) + region `tip_overrides` leaf-keys.
- **FINDING S9-1 (`bolting.triggers` no Appendix-A ruling):** register at Step 11 Appendix-A. Treated user-facing this pass.
- **doc note (non-finding):** `bolting.note_*`/`prevention_*` carry no own `sources`/`anchoring_urls`. Whether bolting prose carries its own source set vs inheriting from `bolting.triggers`/`tips_by_stage.bolting` is an Appendix-A coverage question for Step 11. (claude.ai lane.)
- **Register-completeness / dual-voice gate -- BUILT (`dual_voice_gate_v2.py`).** STILL OWED (WORRY 3): wire into per-crop shell pass as admission HALT + re-run at Step 11. Ship STRUCTURAL walk logic into pipeline `rubric.md`, not a transcribed roster.
- **Gold-standard arc checklist amendments** (claude.ai authoring lane): (1) per-step lane tags; (2) shell-pass-first Steps 4-5; (3) Step 11 flip-disambiguation guardrail; (4) generalized per-crop deletion gate; (5) Step 8 gate wording must mandate a structural crop walk + name `thinning.tip` + region `tip_overrides`; (6) Step 9 wording: derive user-facing leaf set by structural walk + dash resolution per-sense per-crop; (7) Step 10 wording: re-scope anchoring-URL hygiene BY LAYER + anchoring backfill is Step-11 evidence work, not a Step-10 rewrite; (8) encode the 1A layer-scoped anchoring gate definition (claim-bearing leaves only; legacy `zones{}` + regions root rollups excluded by definition) as the gate the pipeline runs.
- **Pre-buildout audit-queue candidate (NEW 2026-06-05):** segment-parent `plantings[0].anchoring_urls` is inconsistently populated across the 8 verified regions (3 populate, 5 empty). Decide whether the parent slot is meaningful (5 under-cited) or vestigial (3 carry stray data), then normalize before the bot pipeline scales. NOT a lettuce-arc item.
- **Pipeline / operating-model doc -- TO BE DESIGNED.** Own session after lettuce is gold-standard.
- **`safe_sowing_note` migration decision** (FINDING 6c-2): Phase C, Claude Code.
- **Deferred vocabulary session:** dataset-wide rename of `track` value `beginner` -> `main`.
- **Companions reconciliation session (§5):** array-level register split. Lettuce carries 3 populated `why_seasoned` with null `why_beginner` -- correctly OUT OF SCOPE until this session runs.

## Inherited findings (unchanged)
- `finding_001` -- warm `zones{}` 8-11 SE-mis-sourced (legacy layer, own pass); legacy-zone empty-`{}` anchoring is this layer's deferred re-sourcing, not a gap. **Reinforced by 1A:** the legacy `zones{}` layer is excluded from the anchoring gate by definition.
- **S10-3 remediation-path correction (CLOSED this session):** the prior note that "the cold legacy `zones[3–7]` hold trustworthy URLs to promote up" for northern_tier was FALSE -- the legacy band also carries empty `anchoring_urls:{}`. northern_tier's 11 leaves required URL DISCOVERY (done this session), not promotion. Planting DATA was already correct (`zone_promoted_verified`); only per-source URLs were absent. CURRENT_STATE line 63 corrected prior session; the discovery that resolves it is complete this session.
- na3d-na3g sourcing-sibling findings; `na3d_finding_003` cosmetic.
- Two-field predicate: `blocks_launch AND status != "resolved"` (never a bare count). **0 unresolved blockers** (confirmed live this session). NOTE: schema `launch_ready_core` gate ALSO requires anchoring completeness independently -- the 45 apply-set leaves must be written + close at Step 11 regardless.

*Update this file at each session close.*
