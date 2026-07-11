# Kickoff #23 -- Apple variety pilot (the TREE archetype for the variety rollout)

**Owner:** Claude Code (dataset) -- authoring + gate + splice. **Blocks cert?** No (apple is already
certified; this enriches its varieties + proves the tree-variety schema). **Origin:** the variety-DTM
load-bearing arc, immediately after the **dry-bean variety pilot** (canonical `340c2983`, 2026-07-11,
Spec 1 of 2). **Start with** `superpowers:brainstorming` to finalize the product/content calls below,
then `writing-plans`. **Memory:** `apple-variety-pilot-tree-archetype`, `variety-dtm-load-bearing-deferred`,
`trevor-north-star-accuracy-authority`.

## What this is + why apple

Dry-bean proved the variety schema on the **DTM-annual** archetype. Apple is the **tree-fruit**
archetype -- structurally different (no days-to-maturity; timing is bloom + harvest *season*; carries
chill and cross-pollination). Proving it here is what unlocks the Spec-2 roster-wide rollout (the
rollout is NOT one uniform sweep -- the roster has 5+ variety shapes, and the tree lane is the hard one).

Trevor's product driver: the app's **"bloom calendar"** shows which apples to plant together for
cross-pollination, and it is currently **GENERIC**. He wants it to **pull the right bloom dates for each
region from the varieties, and be honest.** North star = accuracy + trust + being the authority
(`trevor-north-star-accuracy-authority`).

## NOT greenfield -- what apple already carries

Grep confirmed the bloom model is largely built already:

- **Per-variety** (13 today; `varieties.recommended`, and `varieties_detail[]` is EMPTY): `bloom_group`
  (very_early..very_late), `bloom_window_relative` (`[start,end]` as a **fraction** of the regional
  bloom season, e.g. Honeycrisp `[0.38,0.55]`, Dorsett Golden `[0.0,0.14]`, Pink Lady `[0.74,0.92]`),
  `bloom_duration_days`, `chill_hours_required`, `use`, `recommended_note`.
- **Per-region / per-zone**: `regions.<r>.resolved_by_zone.<z>.bloom` = real dates (e.g. northern_tier
  z5 = "Apr 25 - May 15") + `resolved_from.chill_hours` = chill DELIVERED. Defined by
  `regions.<r>.plantings[].bloom[]` (`from:last_frost`, `offset_days`, `window_days`, sourced
  `ext_org_apples`). Model doc: `docs/tree_region_model_scope_v0.md`.
- **Crop-level `pollination`**: `self_fertile:false`, `needs_pollinizer:true`, `pollinizer_distance_ft:50`,
  dual-register notes naming triploids (Mutsu / Jonagold / Shizuka = sterile pollen).

## The mechanism (how honest per-region dates work)

- **Actual bloom of a variety in a region** = region/zone bloom-anchor start + `bloom_window_relative`
  x season length. That is exactly "pull the right dates for each region from the varieties."
- **Cross-pollination** = two varieties whose actual windows OVERLAP in that region (Gala `[0.4,0.57]`
  and Honeycrisp `[0.38,0.55]` overlap; Dorsett and Pink Lady do not).
- **Honesty layer** = a variety is only viable where DELIVERED chill >= its `chill_hours_required`
  (McIntosh @900 will not fruit in the low desert; the low-chill trio Dorsett/Anna/Ein Shemer exist for
  warm regions). The app must say "won't fruit here", not fake a date.
- The "generic" app calendar is a **consumption gap**: plant-astro is not yet computing anchor x
  relative, chill-filtering, or excluding sterile-pollen partners. The data scaffolding is mostly here.

## Locked decisions (Trevor, 2026-07-11)

1. **Scope:** ~30+ comprehensive catalog (dessert / cooking / cider / heirloom + multiple **triploids**
   + a **crabapple** universal pollinizer). BUT **prove the schema + gate on a first batch** (the
   existing 13 + the honesty edge cases) BEFORE the full sourcing pass -- schema first, then scale
   (the dry-bean lesson).
2. **Schema model = common core + archetype block** (Claude's technical call; do not re-litigate with
   Trevor). Universal core on every variety: `id` (slug), `name`, `maturity_class`, `is_reference`
   (one flagship/crop), `confidence_tier`, `note_beginner`/`note_seasoned`, `sources`/`anchoring_urls`.
   **Tree-archetype block:** `bloom_group`, `bloom_window_relative`, `bloom_duration_days`,
   `chill_hours_required`, a NEW per-variety **triploid / sterile-pollen flag** (bool; today only in
   crop prose), and `maturity_class` = **HARVEST / ripening season** (early/mid/late) kept DISTINCT
   from `bloom_group`; **NO `days_to_maturity`** (grafted / season-only -- the season-only path the
   schema was built for). The bean fields (`seed_type`/`seed_color`/`seed_size`/`plant_habit`/
   `primary_use`) are BEAN-archetype-specific and N/A here.
   - **This refactors dry-bean's `variety_detail_gate`:** its bean-trait REQUIRED fields become
     *archetype*-required, not universal. The gate's universal REQUIRED set shrinks to the common core;
     the archetype block is dispatched by crop type (annual-DTM vs tree). Expect to touch
     `tools/variety_detail_gate.py` + its test.
3. **Honesty engine (the trust feature):** region-anchor x relative-bloom = real per-region dates;
   chill-viability filter ("won't fruit here"); bloom-overlap cross-pollination; triploid exclusion from
   pollinizer picks; self-fertile handling. **Every load-bearing number T1-sourced or it does not ship.**
4. Apple = the tree-archetype pilot that unlocks the Spec-2 rollout (reconcile the 5 variety shapes +
   fold in `varieties_detail[]` on 26 trees/berries + migrate/retire the exploratory delta crops).

## Plan skeleton (spec -> plan -> execution, the dry-bean shape)

1. Brainstorm + spec: finalize the common-core/archetype schema, the tree block, the triploid flag, the
   honesty rules; write `docs/superpowers/specs/YYYY-MM-DD-apple-variety-pilot-design.md`.
2. Refactor `variety_detail_gate` to common-core + dispatched archetype block (TDD RED->GREEN); add the
   tree-block checks (bloom_group enum, `bloom_window_relative` within [0,1] + start<end, chill positive
   int, triploid bool, maturity_class enum) + coherence (relative-window ordering vs bloom_group).
3. `register_completeness` ruling for any new tree-variety string keys (A25 companion, as dry-bean).
4. Author BATCH 1 (existing 13 -> common-core + tree block; add id/maturity_class/is_reference/
   confidence_tier/triploid; each bloom/chill T1-sourced) -> SHA-guarded splice -> full gate battery ->
   promote. THEN BATCH 2..N scale to ~30+ (add triploids + crabapple + more), archetype-batched.
5. State trio + Trevor push each release.

## The app handoff (plant-astro, Spec 2 -- INV-2)

Once the variety data is gate-clean, plant-astro's bloom calendar computes: variety actual bloom =
anchor x relative; filter by chill viability; show overlapping pairs; exclude triploids as pollinizers;
honor `self_fertile`/`needs_pollinizer`. **INV-2:** do NOT consume variety bloom/chill as load-bearing
until the crop is gate-clean.

## Open questions for the brainstorm (product / content / values -- ASK Trevor)

- The specific ~30 variety list (which apples, which triploids, which crabapple) -- draft from popularity
  + full bloom-group/chill coverage, confirm with Trevor.
- The flagship (`is_reference`) apple -- a near-universal pollinizer like Golden Delicious, or a marquee
  eater like Honeycrisp?
- What "honest" surfaces in the app when data is thin (a region with no sourced bloom anchor; a variety
  whose chill can't be met) -- show nothing, or an explicit "not reliable here" note?
- Cider/heirloom depth vs dessert breadth in the catalog mix.

## State / prereqs

- Dry-bean pilot COMMITTED (`7b357e0`, canonical `340c2983`) but **UNPUSHED** (8 commits on `main`) --
  Trevor pushes; no plant-astro bump from the dataset session.
- The concurrent sweet-corn category fix `aa76555` (`Corn & Legumes` -> `Corn`) is in the lineage
  (`3b2674b3` -> `0bcb4fd0` -> `340c2983`) but lacks its own state-trio entry (optional backfill).
