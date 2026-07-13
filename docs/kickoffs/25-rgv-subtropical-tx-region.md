# Kickoff: Rio Grande Valley / subtropical-TX region (roadmap item 3)

**For:** a FRESH plant-dataset (Claude Code) session.
**Goal:** author a real Rio Grande Valley / subtropical-Texas region so the 95 McAllen/Brownsville
z10 ZIPs stop riding se_gulf's Gulf-coast dates (the documented interim from the 2026-07-12 zone-span
reconciliation). This is the last Tier-1 gap still on borrowed data; shipping it retires both the
interim and the plant-app's TX z10 ZIP3-fencing decision.
**Base:** canonical `7e29f4f4` / dataset `main` `3f18db8` (pushed). Rebase onto current `origin/main`
before starting.
**First action:** `superpowers:brainstorming` (this is a new authored region -- creative/design work).
Do NOT start splicing until the scope call in section "THE BIG ONE" is made.

## Why RGV needs its own region (not a se_gulf stretch)

The Lower Rio Grande Valley (Hidalgo / Cameron / Willacy / Starr counties -- McAllen, Brownsville,
Harlingen, Weslaco, Edinburg) is a **frost-free subtropical winter-vegetable region**, climatically
distinct from the Gulf-coast se_gulf belt: near-zero winter chill, a long frost-free season, and a
brutal summer that inverts the calendar (cool-season crops are WINTER crops; the summer is a
heat_pause). se_gulf's z8-9 dates were authored for Georgia/Carolina/Louisiana Gulf coast and do not
honestly stretch to the RGV -- that is exactly why the reconciliation shipped RGV as an EXPLICIT
interim rather than a real answer (see `docs/region_coverage_roadmap.md` item 3 + the RGV interim
section).

## Read first (context)

- `docs/region_coverage_roadmap.md` -- the 6-item program; item 3 is this. Items 4-6 (PNW, judged
  belt, PR) are separate future arcs, NOT this one.
- `docs/superpowers/specs/2026-07-12-region-zonespan-reconciliation-design.md` +
  `docs/superpowers/plans/2026-07-12-region-zonespan-reconciliation.md` -- how the region model works,
  the A45 gate, the clone/donor machinery.
- `docs/2026-07-12-region-zonespan-gaps.md` -- the plant-app sweep; the RGV row is TX z10, 95 ZIPs.
- `docs/gs_cross_crop_field_addition_v0.md` -- the column GS-arc method. **A new region behaves like a
  new roster-wide column** (see below), so this method applies.
- memory `region-zonespan-reconciliation` -- reusable lessons (certified-only transforms; the
  pre-commit safety net catches what gate_all/release_verify miss; zone-keyed structures are plural).

## THE BIG ONE -- resolve this in the brainstorm before anything else

**Adding a region is a ROSTER-WIDE authoring arc, not a small splice.** `coverage_floor_gate` A31
requires every non-indoor certified crop to carry the FULL region roster, and that roster is now
`CANONICAL_REGIONS = set(zone_span_gate.EXPECTED_SPANS)` (derived, 2026-07-12). So the moment you add
an `rgv` key to `EXPECTED_SPANS`, **all ~108 certified region-carrying crops need an `rgv`
`resolved_by_zone` cell or A31 fails them** (gate_all breaks, cert lost). That means authoring RGV
calendars for ~108 crops -- a real content arc on the scale of the original region build.

The brainstorm's first job is to choose the shape:
- **(A) Full roster-wide RGV** (author all ~108 crops). Honest + complete, but a large authoring
  effort. Follow the column GS-arc method; expect a multi-batch splice.
- **(B) Relax A31 to allow a PARTIAL / opt-in region** (RGV present on the crops RGV growers care
  about, others fall back). Smaller launch, but a gate-design change (A31 would need a "full roster
  EXCEPT opt-in regions" notion) and the app's region resolver must handle a crop that has no cell for
  the resolved region. Decide whether that fallback is honest/clean.
- **(C) Phase it**: land a small A31-compatible core first (a "starter" RGV on a subset via option B's
  mechanism), then fill the roster over time.

Recommendation to pressure-test, not adopt blindly: **(A)** keeps the model uniform and the gates
unchanged, and it is the honest answer, but confirm with Trevor that the ~108-crop authoring scope is
acceptable for this arc vs. a partial launch. This is a genuine scope/product call -- surface it.

## Design calls for the brainstorm (the RGV specifics)

1. **Zone span.** The sweep flagged TX z10 (95 ZIPs). RGV also has z9b pockets. Decide the `rgv`
   `zone_span` from the actual `zip-zones.json` distribution for the RGV ZIP3s -- likely `["9","10"]`
   or `["10","11"]`. Whatever it is, A45 requires `resolved_by_zone` keys to match it exactly per crop.
2. **State / ZIP3 mapping (app-side, coordinate with plant-app).** RGV is mostly ZIP3 `785xx`
   (McAllen, Edinburg, Mission, Pharr, Weslaco, Harlingen, Brownsville, San Benito). The app's
   `REGION_STATES` would map the region to TX and `ZIP3_REGION_HINT` fences the RGV ZIP3s to `rgv`
   instead of se_gulf. This is a plant-app change that pairs with the dataset region (a second kickoff
   to plant-app, like #24). WITHOUT the ZIP3 fence, TX z10 keeps matching se_gulf and RGV never wins.
3. **Viability (the honest-calendar work).** Frost-free subtropical:
   - Cool-season crops (lettuce, spinach, brassicas, peas, cool herbs, root veg) = WINTER crops; summer
     is a `heat_pause`. Fall + winter + early-spring windows.
   - Warm-season crops = very long season, often spring + fall with a mid-summer heat pause.
   - Chill-dependent temperate tree fruit (apple/peach/etc. requiring real chill) = `survives_no_fruit`
     or `unsuitable` -- RGV delivers near-zero chill. This is where the A3 no-fruit split + the
     `region_chill_delivered.rgv` band matter.
4. **`region_chill_delivered.rgv` band.** RGV is very low chill (subtropical). Author a sourced band
   (order-of-magnitude ~`[0,200]`; confirm from TAMU AgriLife). This is the ALSO-DISPLAYED chill table
   (plant-astro TreeGuide "your area banks ~X"), so the number is user-facing -- source it, don't guess.
5. **Sourcing (T1).** Texas A&M AgriLife Extension has strong Lower-Rio-Grande-Valley / South-Texas
   vegetable planting calendars (e.g. Aggie Horticulture LRGV / South Texas guides). `tamu_agrilife` is
   already a catalogued T1 source (se_gulf cites it). Budget a targeted T1 hunt for RGV-specific
   month-by-month windows; the T1-or-it-doesn't-ship rule holds.

## Mechanics (what a new region touches)

- `tools/zone_span_gate.py`: add `rgv` to `EXPECTED_SPANS` (and `DONORS` only if any RGV zone clones a
  donor -- but RGV is authored fresh, not cloned, so likely no DONORS entry).
- `region_chill_delivered` (top-level in canonical): add the `rgv` band.
- Every certified region-carrying crop: add an `rgv` `regions` cell (region_id/region_label/zone_span/
  sources/plantings/plantings_provenance/resolved_by_zone/region_notes_{beginner,seasoned}) -- the
  roster-wide authoring (scope call above).
- `coverage_floor_gate` CANONICAL_REGIONS auto-picks up `rgv` (already derived -- no edit needed).
- Gates to keep green: A45 (span parity on the new region), A31/A32 (full roster + calendar presence),
  A3 (tree no-fruit split vs the rgv chill band), the full `gate_all` 116/116, `release_verify`,
  and the pre-commit backstop (it checks ALL changed crops -- watch for the empty-shell class again).
- App-side (plant-app + plant-astro): `REGION_STATES` + `ZIP3_REGION_HINT` for RGV -- a paired handoff
  kickoff after the dataset region lands.

## Definition of done

RGV region authored + certified across the chosen roster; A45/A31/A32/A3 + gate_all + release_verify
green; the plant-app sweep shows the RGV ZIPs resolving to `rgv` (not the se_gulf interim); state trio
updated; roadmap item 3 marked SHIPPED and the RGV interim / TX-fencing lines retired; a plant-app
kickoff written for the ZIP3 fence. Then the interim is gone and the region program is closed down to
items 4-6 (queued).

## Sequencing note

The LEEK variety pilot (`leek-variety-hardiness-archetype-ready`) is queued to run AFTER regions are
off Trevor's plate. If this RGV arc runs in a separate session concurrently, rebase leek's plan onto
whatever canonical RGV lands at. Two sessions must not both hold the canonical open (the sweet-corn
collision lesson) -- coordinate through Trevor.
