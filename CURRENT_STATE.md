# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile.
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.5**) BEFORE acting. Do not infer the next action from "a cell is done" -- check the checklist. The checklist's auto-derived denominator is authority over any kickoff's named field list.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it (the past near-miss came from header-only patches). At session close, **fully regenerate this whole file** from the true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry there at close, never rewrite it. That file is the recovery net.
> 5. **CLOSE RITUAL (every session ends here).** If the dataset changed: PROMOTE -- write canonical, re-pin `LATEST.txt` (new SHA + date + session). Then ALWAYS: regenerate this file (#3), append to `STATE_HISTORY.md` (#4), sync `00-current/`, and commit (+ push).

---

## 🥬 LETTUCE IS FLIPPED -- the M15 gold-standard arc is CLOSED (2026-06-05)
`lettuce-leaf` carries `launch_ready_core=True` + `launch_ready_seasoned=True` (`status` stays `"unverified"`; status vocab is M16's call). **First of the 9 anchors flipped (1 of 9).** The flip executed only after the whole-crop gate returned 0 violations against live post-write-back data. Two non-gating riders remain open (s11_finding_004.2 + the Appendix-A inventory merge -- see "Open items owed").

## Canonical pointer
- **Current SHA:** `29b3aaa904a62487960c5dc53b4282538454076f696ffec039ac4ab87937801a` (M15 lettuce Step 11 COMPLETE -- write-back + clean gate + THE FLIP). `LATEST.txt` session line: `m15_lettuce_step11_writeback_flip`.
- **Predecessor chain:** `29b3aaa9` (the flip) <- `6880ed37` (write-back of the staged closure work, same session) <- `37bfc12d` (apply/gate + s11 findings registration) <- `cdcbf175` (the 45-slot apply) <- `df4d24c7` (S10-5 strip) <- `da4b8bc5` (Step 9) <- `7e9eeceb` (Steps 7/8) <- `5224e13a` <- `0dfd835a` <- `1e19948c` <- `61cddea3` <- `e27eec14` <- `815efe62` <- `8a1d8a50` <- `ed495666` <- `20f9fc2b` <- `327a2d5c` <- `582dbbad`.
- Every PROMOTE re-pins this SHA and `LATEST.txt`. Confirm at session start (protocol #1).

## What just happened (2026-06-05, session `m15_lettuce_step11_writeback_flip`)
- Promoted the claude.ai closure-session state docs; took Trevor's 3 batched decisions (4.2 = Option A; S9-1 = SP no sibling; A-2 = inherit-class).
- **Write-back** (`37bfc12d` -> `6880ed37`): `harvest_ready_anchoring_urls` (5 entries) + `description_anchoring_urls` created (2 entries) + `soil.preferred_description_seasoned` own-voice rewrite + `uga_ext` C963 re-source (2 se_gulf slots) + findings 001/002/003 -> resolved, 004 annotated open. uariz_ext slots HELD untouched per Option A.
- **Gate re-run: 0 violations** (§3 8/8; dual-voice 130/0/0; dash 0; °F clean; source-tier 40 IDs T1; anchoring 1A with the sibling-pair predicate fix = 0 gaps; verbatim re-scan: NCSU/soil hit GONE, residual run 3 words).
- **THE FLIP** (`6880ed37` -> `29b3aaa9`): both `launch_ready` flags -> True; minimal write; collateral audit = exactly the two booleans.

## Active work + exact next step
- **NEXT MILESTONE: M16 = cherry + beefsteak regression.** Both provers carry `launch_ready=True` from 2026-05-22/25 but predate the arc rigor; they owe the full regression pass and must independently rediscover the 4 Appendix-C defects (incl. `gs_exemplar_finding_004` `cause_beginner`). M16 also owes the **status-vocab decision** (successor value for `verification_status.status`; lettuce holds `"unverified"` despite being flipped until that vocab lands).
- **Riders from the lettuce arc (non-gating, route to claude.ai):**
  1. **s11_finding_004.2 Option-A package:** discover a T1 source that states the 77 to 95°F lettuce thermoinhibition range (candidates: UC ANR / UC Davis lettuce production pages; peer-reviewed thermoinhibition literature); then ONE staged write = AZ1615 entries into the 2 uariz_ext slots + the new source's entries + the prose attribution touch-up (replacing the dead-AZ1099 attribution). Then 004 -> resolved (Claude Code write-back).
  2. **Appendix-A inventory merge:** `m15_lettuce_step11_appendix_a_registration.md` is produced; `[INVENTORY-MERGE]` items need the canonical `register_bearing_field_inventory_v1_0.md` (project knowledge). Decisions S9-1 (SP) + A-2 (inherit) are now taken and unblock it.
- **After M16:** authoring-model flip eligibility (3 provers), the pipeline/operating-model doc session, then carrots region-first.

## Step 11 final gate record (2026-06-05, post-write-back, the run the flip rode on)
- §3 cross-field **8/8 PASS** (incl. organic-matter check against the rewritten soil field). Dual-voice **130 populated / 0 missing / 0 null**. Dash: user-facing `--` = **0**. **°F sole form.** Source-tier: 40 IDs, all T1. Roster gate: PASS dataset-wide. **Anchoring 1A (with sibling-pair predicate): 0 gaps.** Two-field predicate: **0 unresolved blockers.** Verbatim scan: 294 prose strings vs 69 text-compared source pages; 0 unadjudicated hard hits; 41 borderline all benign-class.
- s11 findings final state: **001 resolved** (7 entries applied), **002 resolved** (soil rewrite, NCSU run 10 -> 3 words), **003 resolved** (ruled benign), **004 OPEN non-blocking** (4.1 done -- C963; 4.2 = Option A pending the thermoinhibition-source discovery).

## Flip gates (the four distinct "flips" -- never conflate them)
1. **Per-crop `launch_ready` flip** -- ✅ **lettuce DONE 2026-06-05** (the first arc-rigorous flip). Cherry + beefsteak carry True pre-arc and owe M16 regression. 1 of 9 anchors.
2. **Region read-layer flip** -- renderer reads `regions{}` first. **Gate:** shape proven on the 3 provers (lettuce ✅; cherry + beefsteak owe M16); ships with `zones{}` fallback. **2.9+.**
3. **Authoring-model flip** -- carrots onward authored region-first. **Gate:** 3 provers done.
4. **Schema perennial bump** (`lifecycle_override`) -- FUTURE, **2.9+ (NOT 2.8)**. After carrots.

**Schema version lineage:** 2.7.5 -> **2.8 = register-suffix conversion (current)** -> region read-layer flip + perennial extension are **2.9+**.

## Live locked decisions / guardrails
- **Anchoring gate is LAYER-SCOPED (1A, Trevor 2026-06-04)** -- claim-bearing leaves only; legacy `zones{}` (58 leaves) + the 10 `regions{}` root rollup `sources` arrays EXCLUDED BY DEFINITION. **Amended (s11_finding_001):** the predicate MUST also match sibling-named `*_sources`/`*_anchoring_urls` pairs (`harvest_ready_*`, `description_*`). **Amended (A-2, Trevor 2026-06-05):** `bolting.*` register prose is INHERIT-class (evidence at `tips_by_stage.bolting`); excluded from per-field anchoring requirements.
- **S9-1 RESOLVED (Trevor 2026-06-05):** `bolting.triggers` = **SP**, no `_beginner` sibling owed.
- **s11_finding_004.2 = Option A (Trevor 2026-06-05):** keep the 77-95°F figure; AZ1615 for seasonal logic + a to-be-discovered T1 thermoinhibition source.
- **Leaf-URL convention:** leaf `anchoring_urls` = the SPECIFIC lettuce-bearing publication URL; `verified` = date content confirmed present; catalog `url` may stay portal-root; store the canonical resolving URL form.
- **Segment-parent `plantings[0].anchoring_urls:{}` stays empty** (5-of-8 precedent; normalize-or-vestigial = pre-buildout audit queue).
- **`basis_seasoned` voice standard (S10-5):** SP; classifier reasoning in the structural `classification` key.
- **Governing checklist: v1.5** (promoted 2026-06-05; adds **Step 3.5 -- Region shell build**, Claude Code lane; v1.4.1 archived). Dataset is authoritative for what is true; flag doc lag.
- **Lane split.** STRUCTURAL/MECHANICAL = Claude Code (applies, gates, audits, SHA re-pins, flips). Biology + consumer copy + voice/IP + URL discovery/verification + Appendix-A = claude.ai.
- **Per-crop pipeline (target):** Claude Code shell pass -> claude.ai biology + copy -> Claude Code certifies (Step 11) -> Claude Code gated deletion.
- **REGION SHELL-BUILD RULE (Trevor 2026-06-05):** every crop's arc builds ALL 10 region cells to the lettuce bar. The 2.7.5 scaffold only created empty containers; the dataset-wide `northern_tier` fill (109 crops) is the OLD shallow lift (`track:None`, `static_precompute`, nested-cell `plantings`, null notes) and is NOT exempt -- it gets the full build like any other region. Source model: **north (`northern_tier`, zones 3-7) builds FROM the legacy cold `zones{}`** (promote + verify + hoist succession into region-constant `plantings[]`); **warm/CA regions re-derive from T1** (zone data may be climate-contaminated). `whole_crop_gate.py` enforces this (catches stub + null-track + §3b-i nested-cell + null-notes). To be finalized as a new checklist **Step 3.5 -- Region shell build** (Claude Code lane), NOT a new Step 0 (Step 0 is Preflight; the work is already partly owned by Steps 4/5.5). See Open items + Downloads `checklist_v1_5_shell_build_amendment.md`.
- **Keep `zones{}` coherent until Phase C** (deletion gate: region carries everything + consumers read region-first + round-trip + frost-input independence; `safe_sowing_note` precondition not met, FINDING 6c-2).
- **Inheritance is candidate, not verified (v1.4.1 §4).** **Pest/disease = highest-scrutiny cluster.**
- **Micro-strings at-bar-by-nature but DO take `_beginner` siblings.** **`cause_beginner` ruling:** may be byte-identical where seasoned carries no jargon.
- **TEMPERATURE -- canonical `°F`** user-facing; backend notes retain whatever form.
- **DASH -- per-sense, per-crop.** Lettuce clean; other 122 crops carry ~5,360 user-facing `--` -- **F-6d-2 OPEN** (rides each crop's arc).
- **Succession-shape (spec §3b-i):** rule ONCE in region-constant `plantings[]`; northern_tier's materialized strings kept-by-evidence (re-verified at Step 11).
- **`year_round` encoding** for pauseless cells; `track`: `beginner` = shared MAIN, `succession` = seasoned-only.
- **Register-conversion convention:** `X_seasoned` + (`X_beginner` for CP, absent for SP); presence IS the visibility declaration.

## Open items owed
- **s11_finding_004.2 (claude.ai then Claude Code):** the Option-A package (see "Active work"). 004 -> resolved after it lands.
- **Appendix-A inventory merge (claude.ai):** registration doc produced; S9-1 + A-2 decisions taken; `[INVENTORY-MERGE]` items await the canonical inventory.
- **M16 kickoff (claude.ai authors; Claude Code certifies):** cherry + beefsteak region-primary FILL arc (NOT a regression -- both are 0/10 regions at-bar: 9 stub + stale northern_tier) + status-vocab decision. Kickoff staged: Downloads `m16_cherry_beefsteak_kickoff.md`.
- **Checklist v1.5 -- DONE (promoted 2026-06-05).** Step 3.5 Region shell build added (Claude Code lane); Step 4 scope narrowed to sourcing-into-shells; northern_tier satellite doc superseded-bannered + retained as worked example; reference-GS-crop pointer (lettuce-leaf) + two-callsite admission/certification model added; `gs_exemplar_finding_shell` in Appendix C. Promoted to `05-methodology/current/` + `00-current/`; v1.4.1 archived. **Owed: Trevor refreshes claude.ai project knowledge with the v1.5 file.** (Minor nit, optional: the doc's H1 still reads "v1.4 (Keystone)" by the on-disk provenance convention; status block confirms v1.5 -- claude.ai's call to change.)
- **Gate tooling shipped (Claude Code, committed):** `tools/whole_crop_gate.py` (dual-voice + dash + °F + source-tier + anchoring 1A/sibling-pair + region-fill stub/stale catcher + two-field predicate) and `tools/verbatim_scan.py` (systematic copyright scan). Reproduce lettuce=0; cherry 42 / beefsteak 44 / carrot 292. WORRY 3 partially closed (gates now exist as shared files; still owed: wire as formal Step-0 admission HALT via the checklist).
- **Proposed (claude.ai judgment): archetype-driven biology checklist** -- per `archetype` (cool_season_annual, warm_season_fruiting, deciduous_fruit_tree, ...), the biology phenomena that archetype MUST address (bolting/heat-pause; det-indet/blossom-drop/BER; chill-hours/bloom; etc.), asserted present-or-ruled-N/A at Step 0. Catches the needed-but-ABSENT-field gap the gates structurally cannot (the bolting class generalized).
- **Dual-voice gate (WORRY 3):** v2 structural walk still lives only in transcripts + ad-hoc rebuilds; ship into `tools/` + pipeline `rubric.md` as the admission HALT.
- **Checklist amendments (claude.ai):** (1) lane tags; (2) shell-pass-first; (3) flip disambiguation; (4) deletion gate; (5) Step 8 structural walk; (6) Step 9 leaf-set derivation; (7) Step 10 layer scoping; (8) the 1A gate + sibling-pair predicate + A-2 inherit-class exclusions.
- **Pre-buildout audit queue:** segment-parent `plantings[0].anchoring_urls` 3-populate/5-empty inconsistency; verbatim-scan tooling note (PDF extractor + the bot-blocked/JS-rendered URL sweep).
- **Pipeline / operating-model doc:** own session, now unblocked (lettuce is gold-standard-flipped).
- **`safe_sowing_note` migration (FINDING 6c-2):** Phase C, Claude Code.
- **Deferred vocabulary session:** rename `track` `beginner` -> `main`.
- **Companions reconciliation session (§5):** array-level register split; lettuce's 3 `why_seasoned`-with-null-`why_beginner` correctly OUT OF SCOPE until then.

## Inherited findings (unchanged)
- `finding_001` -- warm `zones{}` 8-11 SE-mis-sourced (legacy layer, own pass); excluded from the anchoring gate by 1A definition.
- na3d-na3g sourcing-sibling findings; `na3d_finding_003` cosmetic.
- Two-field predicate: `blocks_launch AND status != "resolved"` -- returns **0 unresolved blockers** (s11_finding_004 is open but non-blocking).

*Update this file at each session close.*
