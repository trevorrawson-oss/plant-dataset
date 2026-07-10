# Kickoff #21 -- corn / block-planted-grass archetype (design -> GS arc)

**Status:** NOT STARTED -- start in a FRESH session (dry-bean session was saturated). Begin with the
**superpowers:brainstorming** skill, then spec -> plan -> execute (the dry-bean playbook, which worked).
**Origin:** `sweet-corn` is one of the 10 uncertified §E shells; it is blocked on a new archetype.

## Why this one next (the leverage)
`sweet-corn` needs a **warm-season block-planted-grass** archetype that nothing in the roster has
(wind-pollinated, block planting, no close template). Building it does double duty: it **certifies the
`sweet-corn` shell AND unlocks the whole corn family** -- `corn` (field/dent), `popcorn`, `flint-corn`
are all *Zea mays* and share this one archetype (add them as new crops on it afterward). One archetype,
four crops. See memory `master-crop-list-phase4-inventory` (Master Crop List pp.12-13) + `remaining-gs-anchors-roadmap`.

## What makes corn its own archetype (the brainstorm's core)
- **Block planting for wind pollination.** Corn is wind-pollinated (tassel -> silk); you plant in a
  BLOCK of >=4 short rows, not one long row, or ears fill poorly. This is the defining agronomic fact
  and has no analog in the current archetypes -- likely needs a structured "plant in a block" concept,
  not just a spacing note.
- **Tassel / silk / ear biology** and the "knee-high by the Fourth of July" milestone.
- **Sweet vs dry harvest split.** Sweet corn is picked at the MILK stage (fresh, a tight ~gate window);
  field/pop/flint corn is left to **dry down on the stalk** -- which is exactly the `dry_down -> harvest
  -> cure_thresh` ladder we just built for dry-bean. Strong reuse opportunity for the dry corns.
- **su / se / sh2 sugar genetics** drive sweet-corn variety selection -- captured at VARIETY level per
  the master crop list, not crop level.

## Design questions to resolve in the brainstorm
1. **New archetype vs refit?** `sweet-corn` currently sits on `warm_season_fruiting` (wrong). Is corn a
   brand-new `warm_season_grass` archetype (like `berries_woody`/`woody_ornamental` were built), or a
   heavy refit? Lean new archetype given block-planting + wind pollination.
2. **How to model block planting** -- a new field (e.g. `pollination_block_min_rows`)? A spacing/layout
   note? Structured guidance the app can render? This is the novel data-model piece.
3. **Sweet vs dry harvest** -- does the archetype carry BOTH (sweet = milk-stage gate; dry = the
   dry-bean dry_down/cure ladder), so `sweet-corn` and the dry corns share it? Almost certainly yes.
4. **The gate** -- a new TDD archetype gate (RED before GREEN, adversarially proven on a scratch copy),
   the way `berries_woody_gate` / `woody_ornamental` were. What invariants does it enforce?
5. **Scope of the first arc** -- certify `sweet-corn` only, or design the archetype + certify sweet-corn
   + queue field/pop/flint as follow-on crops? (Recommend: design archetype + certify sweet-corn as the
   anchor; field/pop/flint are fast follow-ons once the archetype + gate exist.)

## Precedents to lean on
- Archetype-build pattern: `berries_woody` / `woody_ornamental` (TDD gate + `derive_*_calendar` + the
  region-shell reshape in `build_region_shells.py`).
- Dry-harvest ladder: the dry-bean `dry_down -> harvest -> cure_thresh` stages + `harvest`-id anchor
  rule (A40) -- reuse for field/pop/flint corn. Spec `docs/superpowers/specs/2026-07-09-dry-bean-gs-anchor-design.md`.
- The §E new-crop checklist + register stack (A39/A40) -- a new corn crop must carry them natively.
- Honesty precedent: dry-bean's Option-C region ruling (annual model can't express per-region
  suitable=false) -- corn may hit similar region-suitability questions.

## Out of scope here
`broom-corn` (a *Sorghum*, not Zea mays -- own archetype) and `sugar-cane` (*Saccharum*, perennial
tropical -- own archetype) are NOT part of this arc despite the "corn" name.
