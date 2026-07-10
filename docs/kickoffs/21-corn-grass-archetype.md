# Kickoff #21 -- corn GS arc (frost-anchored annual; sweet-corn + the corn family)

**Status:** NOT STARTED -- start in a FRESH session. Begin with **superpowers:brainstorming**, then
spec -> plan -> execute (the dry-bean playbook). **Origin:** `sweet-corn` is one of the 10 uncertified
§E shells.

## KEY REFRAME (Trevor, 2026-07-10) -- corn is NOT a gate-worthy archetype
The original version of this kickoff led with "new `warm_season_grass` archetype + a berries_woody-style
gate." **That was over-engineering.** Verified against the code:
- **The gate dispatch key is `calendar_basis`, NOT `archetype`.** Every archetype gate opens with
  `if crop.get("calendar_basis") != "<basis>": return []` (berries_woody, perennial_herbaceous, ...).
  The `archetype` field gates nothing.
- **`archetype` is a soft descriptive label.** `warm_season_fruiting` (33) and `cool_season_annual` (27)
  both collapse to `calendar_basis: frost_anchored` -- **83 annuals share ONE annual gate set.**
- **The archetypes that earned gate branches are all PERENNIAL-WOODY** (berries_woody, perennial_woody_
  ornamental, perennial_herbaceous) with multi-year bloom/dormancy/chill calendar math. Corn has none.
- **sweet-corn is a frost-anchored, direct-sown ANNUAL -> it runs the standard annual gate set -> NO new
  gate.** `dry-bean` is the proof: a fresh warm-season annual certified with A39/A40 native, zero new
  gate. **Do NOT build a berries_woody-style archetype gate for corn.**

## Why this one next (the leverage)
Certifying the `sweet-corn` shell also unlocks the corn family: `corn` (field/dent), `popcorn`,
`flint-corn` are all *Zea mays* frost-anchored annuals -> add them as new crops afterward on the same
patterns. **One arc, four crops, no new gate.** See `master-crop-list-phase4-inventory` (Master Crop
List pp.12-13) + `remaining-gs-anchors-roadmap`.

## Corn's REAL novelties (narrow -- the actual design work)
1. **Block planting for wind pollination.** Corn is wind-pollinated (tassel -> silk); you plant in a
   BLOCK of >=4 short rows, not one long row, or ears fill poorly. This is the one genuine design
   question, and it is LIGHT: **prose** in the spacing guidance, OR a small **additive field** (e.g.
   `pollination_block_min_rows: 4` / a `planting_layout` enum) if the app should render/enforce it --
   a field-addition-register item, present-or-null, NOT a calendar_basis/gate change.
2. **Sweet-vs-dry harvest split** -- pure `growth_stages` authoring (existing A40 validates it):
   - **Sweet corn:** harvest at the MILK stage (a tight ripeness window); **succession-suitable**
     (`suitable:true`, like green-beans -- stagger sowings for continuous harvest).
   - **Field / pop / flint:** left to **dry down on the stalk** -> **REUSE the dry-bean
     `dry_down -> harvest -> cure_thresh` ladder + the `harvest`-id anchor rule (A40)**; single-crop
     (`suitable:false`, like dry-bean).

## Design questions for the brainstorm
1. **Block planting: prose or a small additive field?** The only real schema question. If a field:
   define it (min rows / layout enum), decide whether it needs a light present-or-null gate
   (register-style), and run it as a field-addition arc against the stable roster.
2. **Archetype label** -- keep `warm_season_fruiting`, or add a descriptive `warm_season_grass`?
   COSMETIC (does not gate); decide for tidiness only, not correctness.
3. **Scope of the first arc** -- certify `sweet-corn` as the anchor; queue `corn`/`popcorn`/`flint-corn`
   as fast follow-on crops (they reuse the dry-bean dry-down ladder + the block-planting model).
   Recommend: sweet-corn first, then the dry corns.
4. **Region suitability** -- corn may hit the same annual per-region questions dry-bean did (short-season
   zones, etc.); the Option-C precedent + the (open) annual per-region-suitability model gap apply.

## Precedents to lean on
- **PRIMARY: dry-bean** (`docs/superpowers/specs/2026-07-09-dry-bean-gs-anchor-design.md`) -- a fresh
  frost-anchored annual GS arc with ZERO new gate; its `dry_down -> harvest -> cure_thresh` ladder +
  `harvest`-id anchor (A40) transfer directly to the dry corns.
- The §E new-crop checklist + register stack (A39/A40) -- a new corn crop carries them natively (dry-bean
  showed they fall out of clean authoring).
- `green-beans-bush` -- the succession model for sweet corn (`suitable:true`, staggered sowings).
- **NOT** berries_woody / woody_ornamental -- those are perennial-woody gate branches, irrelevant to an
  annual. (The block-planting field, if added, follows the FIELD-ADDITION register method, not an
  archetype-gate build.)

## Out of scope here
`broom-corn` (a *Sorghum*, own basis/archetype) and `sugar-cane` (*Saccharum*, perennial tropical, own
basis) are NOT part of this arc despite the "corn" name.
