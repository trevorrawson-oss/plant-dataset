# Kickoff: plant-app IPM control-ladder consumption + a slick pest UI

**For:** the plant-app session building the pest UI.
**From:** the plant-dataset session that shipped the pest/IPM control-ladder pilot.
**Status:** committed, NOT YET pushed (Trevor confirms push before you sync). No plant-astro bump this session.

## Sync/rebuild off this canonical

```
crops_data_final.json  sha256 = 4f7789aaed0c6a3ef44ec3fecd728a76ddd017b53dfd23ad03cfb45b8dbf1696
dataset commit = d4aa190   (sync off this once pushed)
```

Pilot crops carrying the new shape: **Broccoli, Celery, Microgreens Mix** (16 pest/disease records).
Every other crop's `pests`/`diseases` are unchanged for now (the roster-wide rollout is a later arc), so
**render defensively: fall back to the old shape when `control_ladder` is absent.**

## What's new in the data (3 structures)

### 1. `control_methods` (NEW top-level object) -- the shared, authored-once method catalog
Keyed by method id (snake_case), mirrors `source_catalog`. Each entry:
```jsonc
"insecticidal_soap": {
  "name": "Insecticidal soap",
  "tier": "soft_chemical",              // cultural | physical | biological | soft_chemical | conventional
  "applies_to": ["insect_soft_bodied"], // coarse target tags (mostly for the dataset gate; optional for UI)
  "how_it_works_beginner": "…", "how_it_works_seasoned": "…",   // dual-register
  "best_use": "…",                       // single string: when to reach for it
  "pros": ["…","…"], "cons": ["…","…"],  // honest, non-empty
  "cautions": ["…"],                     // pollinator / PHI / soil, where real (may be absent)
  "find_it_beginner": "Sold ready-to-use as 'insecticidal soap'… look for potassium salts of fatty acids", // on the 10 purchasable methods only
  "sources": ["ucanr_ext"], "anchoring_urls": { "ucanr_ext": { "url": "…", "verified": "2026-07-22" } }
}
```
**Tier is the escalation order** (render softest -> strongest): `cultural` < `physical` < `biological` <
`soft_chemical` < `conventional`. 24 methods live.

### 2. Per-problem fields (on each `crops[].pests[]` and `crops[].diseases[]`)
Each record now also carries:
```jsonc
{ "id": "cabbageworms",            // stable kebab slug (the join key; also the future variety-resistance key)
  "type": "insect",                // insect|mite|mollusk|fungal|bacterial|viral|physiological|nematode
  "control_ladder": [              // ORDERED, softest-first. THIS is the ladder to render.
    { "method": "garden_sanitation" },
    { "method": "floating_row_cover", "note_seasoned": "…", "note_beginner": "…" },  // optional per-rung crop-specific note
    { "method": "bt" }, { "method": "spinosad" }
  ],
  // …preserved: symptoms_*, cause_*, prevention_*, sources, anchoring_urls (microgreens use name_*/description_*)
}
```
Each rung's `method` is a key into `control_methods`. The optional `note_*` is crop-specific nuance that
overrides/augments the generic method text FOR THIS PROBLEM. The old `organic_treatment_*` / `management_*`
blobs are GONE (folded into the ladder).

### 3. `pesticide_safety_education` (NEW top-level object) -- the universal safety spine
Dual-register fields: `label_note_*` ("the label is the law"), `preharvest_interval_*` (PHI),
`pollinator_note_*`, `handling_note_*` (PPE), `resistance_note_*`. Surface this **once**, not per method.

## Rendering it as a slick UI (suggestions -- your lane)

**The core metaphor: an escalation ladder you climb only as far as you need.** For a given problem, render
`control_ladder` top-to-bottom as rungs, grouped/tinted by `tier`, with a clear "start at the top, escalate
only if it isn't working" affordance.

```
AphidsBroccoli / cabbageworms                                     [beginner ⇄ seasoned]
──────────────────────────────────────────────────────
 ▸ START SOFT
 1 · Cultural   Garden sanitation                    ⌄
 2 · Physical   Floating row cover                   ⌄   "brassicas need no bees, keep it covered all season"
 3 · Physical   Handpick                             ⌄
 4 · Biological Bt  (Bacillus thuringiensis)         ⌄   ← organic, caterpillar-specific
 5 · Soft spray Spinosad                             ⌄
   (no conventional rung — Bt/spinosad hold)              ← honest end-cap
```
Tapping a rung expands the `control_methods` entry: `how_it_works_*` (register-driven), `best_use`, **pros /
cons / cautions** (this honesty is the feature -- show cons + cautions prominently, don't bury them), and the
`find_it_beginner` "how to find it at the store" line as a chip.

**Design cues that carry the honesty (the whole point of this data):**
- **Tint by tier**, softest = calm/green, `conventional` = a distinct "last resort" red. Make climbing feel
  like escalating.
- **Mark `conventional` rungs "rescue-only."** In the pilot only broccoli `flea-beetles` has one
  (carbaryl) -- render it as a deliberately-gated last step, with its `cautions` front-and-center.
- **Honest short ladders are correct, not incomplete.** Clubroot, blackheart, pink-rot, both microgreens
  problems, cabbage-root-maggot, carrot-rust-fly, leaf-miner intentionally stop early (no chemical applies).
  Render a clear end-cap ("no spray for this -- prevention is the only control") rather than an empty "more"
  affordance. Do NOT imply a rung is missing.
- **Surface `find_it_beginner` for shoppers** on the soft_chemical/conventional/Bt/spinosad methods -- it
  names the active ingredient + a brand + the "brands get reformulated, read the active ingredient" lesson
  (it even handles the Sevin dust-vs-liquid trap and "dish soap is not insecticidal soap").
- **The safety spine once:** a "Before you spray" interstitial or info sheet from
  `pesticide_safety_education` when a user first opens any chemical rung -- not repeated per method.
- **Dual-register** drives `how_it_works_*` and per-rung `note_*` off your existing beginner/seasoned toggle.

## Gotchas
- `control_ladder` absent -> old shape; graceful-fallback (most crops until rollout).
- Microgreens records use `name_seasoned`/`name_beginner` + `description_*` (not `name`/`symptoms_*`); the
  `id`/`type`/`control_ladder` are still there. Handle both name shapes.
- Rungs can repeat a tier (e.g. two soft_chemical alternatives) -- that's fine; keep them in array order.
- `applies_to` is mainly a dataset-gate concern; you don't need it to render, though it could power a
  "what does this treat" filter later.

## Not in scope here (separate/future)
- Roster-wide rollout (~897 problems across 119 crops) -- a later dataset arc; the app should already handle
  the shape so it "just lights up" as crops migrate.
- The NEXT dataset arc is per-variety resistance (`resists:` referencing these pest `id`s) -- the pest `id`
  you join on today is the same key that will carry variety resistance, so keep it as your stable handle.
