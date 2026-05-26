# plant -- Current State

**Last updated:** 2026-05-25 (M9B ph_education authoring complete)

**This file is the entry point. Read it first. Authored by Claude at session close; deployed automatically by the promotion command.**

---

## Dataset

- **Canonical location:** `~/plant-dataset/crops_data_final.json` (the ONLY authoritative dataset home)
- **Current SHA:** `b708907adf525dc69a0de64ad7a84979cdde5aed8b3f89e9db104ba3175b84cc`
- **Schema version:** 2.7
- **Crop count:** 123
- **Zones:** USDA hardiness 3-11
- **Format:** minified JSON
- Do NOT store dataset copies elsewhere. `~/Documents/plant-project/03-data/source-of-truth/` is retired -- see the pointer file there.

## Methodology

- **Current version:** v1.4 (LOCKED 2026-05-19, across Sessions A and B)
- **Location:** `~/Documents/plant-project/05-methodology/current/`
- **Files:**
  - `per_crop_verification_methodology_v1_4.md`
  - `methodology_page_v1_4.md`
  - `schema_2_7_specification_v1_0.md`
  - `schema_2_7_visibility_map_v1_0.md`

## Universal content blocks

- **`soil_education`:** COMPLETE (M9A, 2026-05-25). 7 texture classes (sandy, sandy_loam, loam, clay_loam, clay, chalky, peaty), each with 6 prose fields + sources + anchoring_urls. Flat shape -- texture classes are direct keys under `soil_education`, no `textures` wrapper.
- **`ph_education`:** COMPLETE (M9B, 2026-05-25). 5 pH ranges + how_to_test + raising_ph (3 amendments) + lowering_ph (3 amendments) + regional_context. `ranges` wrapper present (heterogeneous sub-blocks warrant it). 8 T1 sources: umn_ext, cornell_ext, clemson_hgic, ncsu_ext, psu_ext, ucanr_ext, msu_ext, tamu_agrilife.

## Where we are in the work

- **Current phase:** Phase 3 per-crop verification, gold-standard anchor architecture
- **Active arc:** M10 (Lettuce gold-standard arc) -- next session
- **Cherry tomato (M6):** COMPLETE (launch_ready_core: true, launch_ready_seasoned: true)
- **Beefsteak tomato (M7):** COMPLETE (launch_ready_core: true, launch_ready_seasoned: true)
- **Warm-season fruiting archetype anchor pair:** COMPLETE

## What's in flight

- **M10 is next:** Lettuce gold-standard arc (cool-season annual archetype anchor #1). Kickoff in M9B deliverables.
- Cherry companion session queued: 15 open non-blocking findings from M6 arc.
- Beefsteak companion session queued: 8 companion findings (nd_finding_003 through nd_finding_010).

## What's locked / done

- Schema 2.7 live in the dataset (1C scaffolding complete)
- Methodology v1.4 locked
- Catalog hygiene (`uf_ifas_okaloosa` to `uf_ifas_nwdistrict`) complete
- **`soil_education` universal block COMPLETE (M9A)**
- **`ph_education` universal block COMPLETE (M9B)**
- **Cherry tomato gold-standard arc COMPLETE (M6)**
- **Beefsteak tomato gold-standard arc COMPLETE (M7)**
- **Warm-season fruiting archetype anchor pair COMPLETE**

## Open (non-blocking) items to revisit

- Cherry carries 15 open findings, all `blocks_launch: false`.
- Beefsteak carries 21 open findings: 4 resolved, 17 non-blocking.
- Companion findings on beefsteak: nd_finding_003 through nd_finding_010 (8 entries; companion session queued).
- **M9B anchoring_urls require manual browser verification** (m9b_finding_001): container network blocks outbound extension requests; 8 top-level URLs + 6 amendment-level URLs need Trevor to confirm they resolve. See findings doc for URL list.
- **Catalog session deferred:** Add `nrcs_soils` (m9_finding_002 carry-forward from M9A). 2 dangling refs (britannica, walter_reeves) also pending.
- **Methodology doc correction deferred:** `soil_education.textures.<vocab_term>` path in v1.4 doc is incorrect; correct to `soil_education.<vocab_term>` at next methodology cleanup (m9b_finding_002).

## State inconsistency (carried from M9A)

Cherry tomato `verification_status.phase` shows `phase_3_tomatoes_m6_1b_na` in dataset (stale). Project knowledge records cherry completed at M6 1B-NG. Non-blocking; investigate at cherry companion / family session.

## Pointers for Claude Code

- **Dataset:** read from `~/plant-dataset/crops_data_final.json`
- **Current state / orientation:** read this file first
- **Methodology / schema / visibility:** read from `~/Documents/plant-project/05-methodology/current/`
- **Guide-page design reference:** cherry tomato (first complete gold-standard anchor); beefsteak tomato (second anchor)
- **soil_education shape note:** flat -- `soil_education.sandy`, not `soil_education.textures.sandy`
- **ph_education shape note:** `ph_education.ranges.slightly_acid`, `ph_education.raising_ph.calcitic_lime`, etc.

---

*Update this file at each session close. Authored by Claude; deployed by the promotion command to both `~/plant-dataset/` and `~/Documents/plant-project/00-current/`.*
