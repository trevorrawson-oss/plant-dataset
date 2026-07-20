# Mid-Atlantic region -- design spec

**Date:** 2026-07-20
**Kickoff:** `docs/kickoffs/31-mid-atlantic-region.md` (roadmap item 8)
**Base canonical:** `e1e01c47` / dataset `main` @ `9c9021a` (== `origin/main`)
**Ruling that queued this:** `docs/reviews/notes/2026-07-15/tier2_mid_atlantic_ruling.md`
(CONDITIONAL-GO; built as a full region per Trevor's 2026-07-16 ruling, restated 2026-07-20).
**Precedent:** maritime PNW (`2026-07-14-maritime-pnw-region-design.md`). Frost-anchored, standard
deriver, same toolchain. **This is the lightest region arc yet** -- see section 2.

**Sequencing (Trevor, 2026-07-20):** items 8-11 (mid-Atlantic, mid-South, Nevada, Utah) are built
before item 7 (Alaska). This is the first of the four.

---

## 1. Product goal

Author a real Mid-Atlantic region (`mid_atlantic`, NC/VA/MD/DC/DE/NJ/PA) so the belt stops riding
generic frost-anchored zone dates that omit an entire documented second (fall) planting cycle for
warm-season annuals. Nothing in this belt is *misclassified* today. The dates are simply conservative:
they offer users materially less of the season than actually exists.

## 2. Why this is the lightest arc of the five, and what that means

The mid-Atlantic ruling found **exactly one gap, in exactly one crop class**, and the gap has a shape
this dataset already models and already gates:

- **Tree fruit and berries need no correction at all.** Real NC State chill accumulation exceeds 1,000
  hours annually, clearing the entire canonical apple variety range (max 900, McIntosh) with margin,
  and NC State's own blueberry recommendations (Duke, Jersey, Premier) are literally cultivars already
  on the canonical list. Two of three basket crops showed no divergence.
- **The one real gap is a fall cycle for warm-season annuals.** VCE 426-331's zone-8 table carries an
  explicit separate fall tomato window (Jul 1 - Aug 10), and NC State's central-NC planting calendar
  shows continuous transplanting through July 1. The naive single-cycle deriver closes the season in
  mid-July and shows flat `cold_pause` from August through December, against a real first frost of
  October 30.

**No new field. No new gate.** That gap maps directly onto `second_planting` (already live in 272
cells across all 12 regions, already gated by **A43**'s de-mux invariant) plus `heat_pause` (881
cells). Contrast Alaska, which needs two new conditional fields and two new gates because its
divergence has no existing home. The authoring here is ordinary region authoring against good,
already-catalogued sources.

**Consequence for sequencing:** this arc's risk is concentrated in volume (111 crops) rather than in
design. It should run faster than PNW did, and it is a good arc to prove the four-belt sequence on.

## 3. Scope -- Option A, full roster-wide (forced by A31)

Same as every region arc: `coverage_floor_gate` A31 derives its roster from
`zone_span_gate.EXPECTED_SPANS`, so adding `mid_atlantic` obligates a cell on every certified
region-carrying crop. **111 crops** as of canonical `e1e01c47` (82 `frost_anchored`, 14
`perennial_chill_gated`, 5 `perennial_evergreen`, 5 `perennial_woody_ornamental`, 4 `berries_woody`,
1 `perennial_herbaceous`). The 8 microgreens carry no `regions` block; the 9 uncertified shells are
exempt.

## 4. Data model

### 4.1 Region id and label

`region_id: "mid_atlantic"`. Label: **"Mid-Atlantic: Piedmont and Coastal Plain"**.

No collision with `se_gulf`, whose state list (GA, AL, MS, LA, SC, FL, TX) does not include any
mid-Atlantic state. The belt is genuinely unclaimed today: none of NC, VA, MD, DC, DE, NJ, or PA
appears in plant-app's `REGION_STATES` at all, so every user in these seven states currently gets
bare zone dates with no region.

### 4.2 Zone span -- `["7", "8"]` (DECIDED, Trevor 2026-07-20)

**Decision: `["7", "8"]`.** Trevor signed off on 2026-07-20. The rejected alternative was `["8"]`
only (cheaper to deliver, but leaves the z7 majority of the belt on generic dates). The reasoning is
kept below.

Real ZIP distribution across the seven belt states, from plant-app's `zip-zones.json`:

| Zone | ZIPs | Where |
|---|---|---|
| z5 | 68 | PA highlands |
| z6 | 1,409 | PA, WV-adjacent, northern NJ |
| **z7** | **3,131** | northern VA, central MD, most of NJ and eastern PA, western NC Piedmont |
| **z8** | **1,444** | NC Coastal Plain and Piedmont (802), DC (248), VA Tidewater (258), coastal MD (118) |
| z9 | 20 | NC outer coast |

**The case for `["7","8"]`:** z7 holds **2.2x more ZIPs than z8** and is the same continuous
Piedmont-and-coastal-plain climate, just a shade cooler. Regions in this dataset routinely span
multiple zones with per-zone rows carrying different dates (`se_gulf` spans z8-10, `northern_tier`
spans z3-7); that is precisely the mechanism for "same belt, cooler edge." Sourcing supports it
directly: VCE 426-331 is a Virginia publication and Virginia is overwhelmingly z7, so its zone tables
cover z7 natively, and NC State publishes separate central and western NC calendars.

Crucially, **widening a span later is its own roster-wide arc.** Roadmap item 1 is the precedent: the
2023-map widen was a full column pass with a purpose-built patch builder, 756 cloned rows, and a new
gate. Authoring z7 now costs one extra row per crop inside an arc that is already open. Authoring it
later costs a second full pass.

**The case against (`["8"]` only, rejected):** the ruling's evidence is Raleigh-anchored and therefore
z8. z7 needs its own sourced frost normals and windows. And the z7 half will not deliver in-app until
the temperate-region resolution fix lands (4.3 below).

**Decision: span z7-8, author both rows, accept that the z7 half sits dormant until the app fix.** The
dataset is the source of truth and should be correct ahead of the consumer; that has been the pattern
for every region so far (RGV and PNW both shipped before their fences landed).

### 4.3 The temperate-region resolution fix -- a prerequisite for the z7 half (handoff kickoff #32)

The z7 half of this region will not deliver in-app until plant-app's region-assignment layer stops
gating on `isWarmZone(zone) >= 8`. **The precise mechanism, corrected 2026-07-20** (an earlier draft
of this spec mis-stated it as a `northern_tier`-stranding bug -- it is not):

- plant-app has TWO resolution layers. `guide-calendar.ts:resolveZoneCell` already resolves
  `northern_tier` for `zone <= 7` when no region is passed, so cold-zone growers DO get their calendar
  today; `northern_tier` is not stranded.
- The gap is in `zones.ts:resolveFromZip` (onboarding assignment), gated on `isWarmZone` +
  `region.isWarm`. A z7 Virginia grower is never assigned `mid_atlantic`, so `resolveZoneCell` falls
  back to `northern_tier`'s generic z7 cell instead of the authored `mid_atlantic` one. The z7 data
  exists in the dataset but is shadowed. The z8 half works with standard new-region wiring.

Fix = decouple assignment from `isWarm` (assign by state + zone-span, keep `northern_tier` out of the
assignable set, `isWarm` drives presentation only). **No `guide-calendar.ts` change needed** -- once
assignment sets `location.region`, the calendar layer returns the right cell. Full trace + recommended
design: `docs/kickoffs/32-plant-app-temperate-region-resolution.md`.

The z7 ZIPs that upgrade (from `northern_tier`'s generic cold calendar to the region-specific one)
once this region ships AND the fix lands:

| Belt | z8 ZIPs (standard wiring) | z7 ZIPs (need the fix) |
|---|---|---|
| Mid-Atlantic (item 8) | 1,444 | **3,131** |
| Mid-South (item 9) | 697 | ~1,900 |
| Nevada (item 10) | z8-dominant | small z7 tail |
| Utah (item 11) | **15** | small z7 tail |

Two things follow. First, the resolution fix is not an Alaska footnote; it gates the z7 majority of
the two largest belts. It should be treated as a **program-level
prerequisite** and handed to plant-app now, in parallel with this build, rather than sequenced behind
anything. Second, **Utah's ruled z8 core is only 15 ZIPs** -- smaller than Alaska's panhandle -- which
is worth knowing before item 11 is scoped. Its z6-7 neighbors are the Wasatch Front, a genuinely
different climate from St. George's Dixie, so widening is not the obvious fix there. Flagged for item
11's own spec, not resolved here.

### 4.4 Frost-anchored resolution -- standard, no surprises

- `resolution_method: "frost_anchored_resolved"`, standard `tools/annual_calendar.py` deriver,
  `calendar_basis = "frost_anchored"`.
- **z8 frost dates are already sourced by the ruling: last frost April 8, first frost October 30**
  (Raleigh/Wake County COOP, 1944-2019, State Climate Office of NC via NC State Extension).
- **z7 frost dates are a build sourcing task** (Richmond, or a northern-Piedmont/central-MD anchor;
  VCE and the State Climate Office both publish them).
- `cold_pause` legitimate; `region_cell_audit.py` already parametrized for that.

### 4.5 The fall cycle -- the actual work, using existing machinery

For warm-season annuals, the honest calendar is **spring cycle -> midsummer `heat_pause` -> fall
`second_planting`**, the shape already live on `se_gulf` and `low_desert_az`. The existing
`cherry-tomato` `se_gulf` z8 cell is a working template.

- `heat_pause` where the T1 evidence supports a real midsummer set-failure period. Raleigh summers are
  hot and humid, and tomato fruit set genuinely stalls; **source it per crop rather than assuming it**,
  since the pause is declaration-driven in the deriver, not temperature-computed.
- `second_planting` for the documented fall cycle. **A43 governs its shape**: a cell carrying
  `second_planting` must be single-span in `start_indoors`/`plant_out`/`harvest`, and its envelope
  must sit inside the primary windows. Read the gate docstring before authoring; the de-mux arc
  already litigated these invariants.
- **Which crops get a fall cycle is a per-crop T1 call.** VCE 426-331's tables cover many crops beyond
  tomato; the ruling names pepper, squash, and bean as likely neighbors but did not verify them.
  Follow the tables, do not extrapolate from tomato.
- Cool-season annuals get the belt's real long shoulder seasons, including genuine fall/winter
  brassica and green crops that the mid-Atlantic does well.

### 4.6 `region_chill_delivered.mid_atlantic`

Unlike Alaska's, **this band is sourceable today**: NC State Extension states NC gardens receive "in
excess of 1,000 chilling hours annually." Author a real band per zone (z7 will run higher than z8),
in the same chill model as its neighbors (`se_gulf` z8 `[650, 1000]`, `ca_interior` z8 `[500, 1100]`,
`northern_tier` z7 `[700, 1200]`). The band clears every canonical apple variety, so A3 resolves to
`fruits_reliably` across the tree set on real evidence rather than by assumption.

### 4.7 Top-level touch-points

- `zone_span_gate.EXPECTED_SPANS`: add `mid_atlantic: ["7", "8"]`. No `DONORS` entry (authored fresh).
- `region_chill_delivered.mid_atlantic` + `region_chill_delivered_provenance`.
- `coverage_floor_gate`: auto-derived from `EXPECTED_SPANS`, no edit.
- `source_catalog`: **`ncsu_ext` and `vce_426_331` are already catalogued.** Expect few or no new
  entries -- another way this arc is lighter than its predecessors.

## 5. Viability taxonomy

- **Warm-season annuals.** The whole point of the region: spring cycle, sourced `heat_pause`, real
  fall `second_planting`. This is where the user-visible value lands.
- **Cool-season annuals.** Long spring and fall shoulders; real fall and overwintering brassica/green
  crops. Generous but ordinary authoring.
- **Chill-gated trees (14).** `fruits_reliably` across the mainstream set on real >1,000-hour chill.
  Note NC State's own guidance to prefer varieties needing 750+ hours, because the belt's real risk is
  *premature bloom in warm winter spells*, not chill deficit. That nuance belongs in
  `suitability_note_seasoned`. Warm-limited edge cases (citrus-adjacent subtropicals, pawpaw which is
  actually native here) still need per-crop calls.
- **Citrus (5).** Cold-limited: `survives`/`unsuitable` with honest `cold_basis_*` notes. Some
  container culture is real in z8 Tidewater; source it rather than flatly refusing.
- **Woody herbs (5).** Grow well; humidity is the constraint on lavender and rosemary rather than
  cold. The `se_gulf` humidity-struggle framing is the closer analog than PNW's.
- **Berries (4) + strawberry (1).** Strong and well documented. Blueberry especially: NC is genuine
  native highbush and rabbiteye range, and `recommended_type` (the existing per-zone field) is the
  right place for the highbush-vs-rabbiteye steer NC State gives by region.

## 6. Sourcing (T1)

Both primary institutions are **already in `source_catalog`**:

- **`ncsu_ext`** -- the central NC planting calendar (transplant succession windows), the Extension
  Gardener Handbook ch. 15 (chill), the home-garden blueberry guide (variety steer by region), and the
  frost-date table.
- **`vce_426_331`** -- the zone-keyed spring AND fall planting-date tables. This is the single most
  load-bearing document in the arc; extract its full crop coverage early.

Gaps to hunt: z7 frost normals, per-crop `heat_pause` evidence, and fall-window coverage for crops
VCE's tables do not list. **T1-or-it-doesn't-ship holds**; author conservatively and flag where
evidence is thin, never fabricate. The `pypdf`-in-the-controller extraction rule applies as always.

## 7. Rollout mechanics

Toolchain is already region-generic from PNW: `tools/region_harness.py`,
`tools/region_cell_audit.py`, `tools/build_region_promote.py` -- pass `mid_atlantic`, allow
`cold_pause`.

SDD, class-batched: cool-season annuals -> warm-season annuals (the `heat_pause` + `second_planting`
batch, the substantive one) -> trees -> berries + herbs + strawberry. Fresh-subagent content review
per batch, per-crop harness gate, scratch dry-run, one atomic SHA-guarded promote (`EXPECTED_SPANS` +
111 cells + chill band + provenance landing together). Canonical stays COMPACT.

Concurrent-checkout discipline applies (explicit pathspec add, `git status` before, `git show --stat`
after); consider an isolated worktree.

## 8. Verification

- `whole_crop_gate` full suite + `tools/gate_all.py` -> **119/119**.
- **A43** clean across every authored `second_planting` cell (the de-mux invariant is the gate that
  matters most in this arc).
- A45 (span parity, `mid_atlantic` in `EXPECTED_SPANS`), A31 (111 carry the region), A32, A3.
- `chill_gate` 0, `calendar_coherence` 0, `timing_spine` 0.
- `release_verify` (section A collateral is the known roster-wide false positive); pre-commit backstop
  is the binding regression gate.
- Per-batch source-truth sample against the cited VCE/NC State tables -- **especially the fall windows**,
  which are the reason the region exists.
- Byte-diff footprint: exactly 111 `regions.mid_atlantic` + chill band + provenance; 0 other keys;
  count 128; COMPACT.

**No new gate**, so no new RED proof is owed. The adversarial discipline still applies to the authored
`second_planting` envelopes: inject an envelope that spans the fall cycle into a scratch copy and
confirm A43 bounces it before trusting the batch.

## 9. App handoff

- `REGION_STATES.mid_atlantic = ['NC','VA','MD','DC','DE','NJ','PA']`.
- `regions.json` row + `SHORT_REGION_LABEL.mid_atlantic`.
- **No ZIP3 fence is expected.** Unlike RGV, PNW, and Alaska, this belt has no adjacent-but-different
  climate pocket sharing its state+zone signature. Confirm during build rather than assuming.
- **The temperate-region resolution fix (4.3, kickoff #32)** -- the program-level prerequisite for the
  z7 half; hand it to plant-app in parallel with this build.

No plant-astro bump from this session.

## 10. Non-goals

- No new fields, no new gates, no deriver change.
- No re-authoring of existing regions; `mid_atlantic` is purely additive.
- No z6 extension (a genuinely different, colder belt; `northern_tier` territory).
- No plant-app or plant-astro code changes here.

## 11. Risks / open items

1. **Zone span is DECIDED z7-8 (4.2).** No longer open. The z7 half depends on the plant-app
   resolution fix (4.3 / kickoff #32) to deliver, but that does not block the dataset build.
2. **Fall-cycle coverage breadth.** VCE 426-331 is strong but will not carry a fall window for all 82
   annuals. Expect a real tail of spring-only crops; that is the honest answer, not a gap.
3. **`heat_pause` calibration.** Declaration-driven, so an unsourced pause silently reshapes the
   calendar. Source per crop.
4. **A43 envelope invariants** are the most likely source of gate churn in this arc, since every
   authored fall cycle touches them.
5. **Volume, not design, is the risk.** 111 crops with a genuine per-crop fall-window decision on the
   82 annuals. Batch discipline matters more than cleverness here.

## 12. Acceptance criteria

- `mid_atlantic` authored + certified across the 111 roster; `zone_span = ["7", "8"]` (4.2, decided).
- A43/A45/A31/A32/A3 + `gate_all` 119/119 + `chill_gate` 0 + `release_verify` clean + pre-commit
  backstop no-regression.
- Footprint EXACT (111 `regions.mid_atlantic` + chill band + provenance; 0 other keys; count 128;
  COMPACT).
- State trio updated; roadmap item 8 -> SHIPPED; field register row added.
- plant-app kickoff written (`REGION_STATES`); the temperate-region resolution fix (kickoff #32) is
  already written and handed off.
- Dataset committed + PUSHED on Trevor's confirm; NO plant-astro bump.

Then item 8 closes and the sequence continues to item 9 (mid-South), which the ruling shows has the
**identical gap shape** -- this spec is its template, and the two arcs should share their fall-cycle
authoring conventions.
