# Kickoff: Variety resilience / disease-resistance pilot (apple + strawberry)

**For:** a fresh plant-dataset session (start cold).
**From:** the session that shipped the pest/IPM control-ladder pilot (the arc this one builds on).
**Status:** nothing built yet. This is the design+pilot kickoff. Start with the brainstorming skill.

## Start-cold pointers
```
canonical crops_data_final.json  sha256 = 4f7789aaed0c6a3ef44ec3fecd728a76ddd017b53dfd23ad03cfb45b8dbf1696
dataset HEAD = aa3d5e6  (pest/IPM pilot + Utah Dixie both LIVE on origin/main)
```
- Memory: `pest-ipm-control-ladder-arc` (what shipped + the id vocabulary you reference),
  `variety-region-arcs-parallel-safe`, `apple-variety-pilot-tree-archetype`,
  `berry-variety-pilot-strawberry`, `trevor-north-star-accuracy-authority`.
- Method: `docs/gs_cross_crop_field_addition_v0.md` + `docs/field_addition_register.md` (this is a NEW
  cross-crop field -> register row 24). The variety-pilot precedent: `tools/variety_detail_gate.py` + the 5
  shipped variety pilots (apple/onion/leek/strawberry/dry-bean).
- The pest arc you build on: `docs/superpowers/specs/2026-07-22-pest-ipm-ladder-design.md`; the pest/disease
  `id`s live on `crops[].pests[]`/`.diseases[]` (only broccoli/celery/microgreens carry them so far); the
  catalog's `resistant_varieties` method's `best_use` literally names "the natural handoff to variety-level
  resistance data" -- that handoff is THIS arc.

## What this arc is
Give each **variety** structured disease/pest-resistance data: a per-variety field (working name
`resists:` / `susceptible_to:`, or a graded `resistance` map -- design decision below) that references the
crop's own pest/disease `id`s. "Liberty apple resists scab"; "Allstar strawberry resists red stele +
verticillium." Resistance is the highest-value variety-choice attribute for a gardener, it is
T1-sourceable from extension variety trials, and it is **rung 1 of the IPM ladder made concrete** (choosing
a resistant variety is the prevention layer the pest arc points at).

**Why it was sequenced right after pests:** structured variety resistance needs a canonical pest/disease
vocabulary to point at -- exactly the `id`s the pest pilot created. Authoring resistance as free prose first
would be a backfill treadmill.

## Pilot scope: apple + strawberry (two archetypes, both ready)
Both are already **enriched-variety** crops (rich per-variety records to hang resistance on) and their
variety notes already carry much of the resistance story. Each needs one small prerequisite: its disease
records don't have `id`s yet, so **step 1 per crop is the pest-migration** (add `id`/`type`/`control_ladder`
to that crop's `pests`/`diseases`, same transform the pest pilot did 3x -- this also advances the pest
rollout for that crop). Then step 2 is the variety resistance.

- **Apple** (16 varieties) -- diseases needing ids: **Apple scab, Fire blight, Cedar-apple rust, Powdery
  mildew** (a 4-disease x 16-variety resistance matrix). Marquee case: Liberty (Cornell-bred, multi-disease
  resistant) vs scab-susceptible standards (Honeycrisp/McIntosh/Gala). Tree_fruit archetype.
- **Strawberry** (9 varieties) -- diseases needing ids: **Gray mold, Anthracnose, Powdery mildew, Red stele
  (Phytophthora), Verticillium wilt**. The classic variety-resistance axis (red stele + verticillium) is
  already stated in the variety notes (Earliglow/Allstar resistant; Honeoye "little disease resistance").
  Berry archetype.

Apple leads; strawberry rides along cheaply (its resistance facts are already in-notes). If the design feels
heavy, strawberry can drop to a fast-follow -- but including it proves the field generalizes across
archetypes, which de-risks the roster-wide rollout.

**Do NOT include broccoli/celery/microgreens** -- they got crop-level pest ladders but their varieties are
still the thin `{name,dtm,note}` shape (not enriched), and microgreens has no meaningful cultivar
disease-resistance. Variety resistance on them would first require a full variety-enrichment arc each.

## Key design questions to settle in the brainstorm (don't pre-decide)
1. **Field shape + resistance GRADE.** Resistance is not boolean -- the pest arc already noted
   "clubroot-resistant varieties *tolerate* rather than fully resist." So capture the grade: likely an enum
   per disease (e.g. immune / resistant / tolerant / susceptible) rather than a bare `resists: [ids]`.
   Decide the shape: `resistance: {"<disease-id>": "resistant", ...}` vs `resists:`/`susceptible_to:` lists.
2. **Referencing.** The keys must be the crop's own disease `id`s (created in step 1). Referential integrity
   is the load-bearing gate check (a `resistance` key must be a real disease id on that crop).
3. **The legit-N/A case** (the method requires one). A variety with no documented resistance -> the field is
   legitimately empty/absent. Include a susceptible variety (e.g. a scab-susceptible apple) so the gate's
   N/A branch is proven. Also: not every disease is studied per variety -> absence != susceptible; decide
   how to represent "unknown/unstudied" vs "susceptible" honestly.
4. **Sourcing + confidence tier.** Per-variety resistance is T1 from extension variety trials / disease-
   resistance tables (Cornell, land-grant fruit/berry pages). Some is well-documented (Liberty scab), some
   thin -> carry `confidence_tier`, T1-only per the variety-pilot rule.
5. **The gate.** A new soft/standalone gate (e.g. `variety_resistance_gate`) in the `variety_detail_gate`
   family: referential (resistance keys are real disease ids on the crop) + valid grade enum + the N/A
   branch. Hard-flip deferred to rollout. TDD, adversarial RED before trust.
6. **Interaction with the app.** In the app, a variety's resistance shrinks its pest watch-list and marks
   the ladder's rung-1 as "already handled." Coordinate the shape with the plant-app pest UI (kickoff #40).

## Process (same shape as the pest pilot)
1. **brainstorming** skill -> design the resistance schema (the 6 questions above) -> spec.
2. **writing-plans** -> plan (per crop: pest-migrate -> author resistance -> gate -> verify).
3. **subagent-driven-development** -> execute; independent T1-fidelity + content review on the resistance
   claims (the pest arc's fidelity review caught a fabricated claim -- do the same here).
4. Verify (gate_all, the new gate, RED battery, footprint, consumer sweep) -> commit -> state trio -> push
   on Trevor's go. NO plant-astro bump (astro session's lane).
5. **Roster-wide rollout = a LATER session** (resistance across the other enriched-variety crops
   onion/leek/dry-bean, then as the pest rollout gives more crops disease ids, the rest). Gated on the pilot
   + Trevor.

## One-line summary for the fresh session
"Design + pilot the variety disease-resistance field on apple + strawberry: pest-migrate each crop's
disease records to get `id`s, then add a graded per-variety `resistance` field referencing those ids
(T1-sourced, gated, with a susceptible-variety N/A case). Register row 24. Rollout later."
