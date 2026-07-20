# Kickoff: Mid-Atlantic region (roadmap item 8)

**For:** a FRESH plant-dataset (Claude Code) session.
**Goal:** author a real Mid-Atlantic region (`mid_atlantic`, NC/VA/MD/DC/DE/NJ/PA) so the belt stops
riding generic zone dates that omit a documented second (fall) planting cycle for warm-season annuals.
**Base:** canonical `e1e01c47` / dataset `main` @ `9c9021a` (== `origin/main`). Rebase before starting.
**Design spec:** `docs/superpowers/specs/2026-07-20-mid-atlantic-region-design.md` -- read it first,
it is complete. Start from `superpowers:writing-plans`.
**Precedent:** maritime PNW (#27). Frost-anchored, standard deriver, same toolchain.

**Sequencing (Trevor, 2026-07-20):** items 8-11 before item 7 (Alaska). This is the first of the four.

## The headline: this is the lightest region arc yet

The ruling (`docs/reviews/notes/2026-07-15/tier2_mid_atlantic_ruling.md`) found **one gap, in one crop
class**, with a shape the dataset already models and already gates:

- Tree fruit and berries need **no correction**. Real NC State chill exceeds 1,000 hr/yr, clearing the
  whole canonical apple variety range; NC State's own blueberry picks (Duke, Jersey, Premier) are
  already canonical varieties.
- The one real gap: warm-season annuals are missing a fall cycle. VCE 426-331's z8 table carries an
  explicit fall tomato window (Jul 1 - Aug 10); NC State's central-NC calendar transplants
  continuously through Jul 1. The naive deriver closes the season mid-July against a real Oct 30 frost.

**No new field. No new gate.** The gap maps onto `second_planting` (272 existing cells, gated by
**A43**) + `heat_pause` (881 cells). The `cherry-tomato` `se_gulf` z8 cell is a working template. Both
source institutions (`ncsu_ext`, `vce_426_331`) are **already in `source_catalog`**.

The risk here is **volume, not design**: 111 crops with a real per-crop fall-window decision on the 82
annuals. Batch discipline matters more than cleverness.

## Decide this before authoring: the zone span

Spec 4.2 recommends **`["7","8"]`**; `["8"]` is the cheaper-to-deliver alternative. Real ZIP counts
across the seven states: **z7 = 3,131, z8 = 1,444** -- z7 holds 2.2x more ZIPs and is the same
continuous Piedmont/coastal-plain climate a shade cooler. Widening a span later is its own roster-wide
arc (roadmap item 1 is the precedent), so authoring z7 now costs one extra row per crop inside an
already-open arc. **Get Trevor's sign-off on this before build starts** -- cheap to flip now, expensive
after.

## Correction carried into this arc (read spec 4.3)

An earlier read that Alaska was the only queued belt hit by plant-app's `isWarmZone(zone) >= 8` gate
was **wrong** -- it reasoned from ruled z8 spans, not real ZIP distributions. Actual:

| Belt | Resolves today (z8+) | Blocked by `isWarm` |
|---|---|---|
| Mid-Atlantic | 1,464 | **4,608** |
| Mid-South | 698 | **2,676** |
| Nevada | 129 | 119 |
| Utah | **15** | 321 |

The `isWarm` decoupling is a **program-level prerequisite**, not an Alaska footnote, and should go to
plant-app in parallel with this build. Also note **Utah's ruled z8 core is only 15 ZIPs** -- worth
knowing before item 11 is scoped.

## Read first

- The design spec, then the ruling note (it has the frost normals and the VCE/NC State table quotes).
- `docs/kickoffs/27-maritime-pnw-region.md` + the PNW spec/plan -- the template arc.
- `tools/second_planting_gate.py` docstring -- **A43's Rule A envelope invariant** is what every
  authored fall cycle has to satisfy. Read it before authoring, not after it bounces.
- `docs/gs_cross_crop_field_addition_v0.md` + `docs/field_addition_register.md`.
- memory `maritime-pnw-region`, `second-planting-demux-followup`,
  `subagent-resumability-and-concurrent-git-safety`.

## Roster

**111 certified region-carrying crops** (canonical `e1e01c47`): 82 `frost_anchored`, 14
`perennial_chill_gated`, 5 `perennial_evergreen`, 5 `perennial_woody_ornamental`, 4 `berries_woody`,
1 `perennial_herbaceous`. Option A (full roster-wide) is forced by A31.

## Sourcing notes

`vce_426_331` is the single most load-bearing document -- **extract its full crop coverage early**, not
just the tomato row, since it determines which crops get a fall cycle at all. z8 frost dates are done
(Raleigh: last Apr 8, first Oct 30); z7 needs a sourced anchor. `heat_pause` is declaration-driven in
the deriver, so an unsourced pause silently reshapes a calendar -- source it per crop.

## Reusable (do NOT rebuild)

`tools/region_harness.py`, `tools/region_cell_audit.py`, `tools/build_region_promote.py` -- already
region-generic. Pass `mid_atlantic`; allow `cold_pause`.

## Definition of done

`mid_atlantic` authored + certified across the 111 roster; A43/A45/A31/A32/A3 + `gate_all` 119/119 +
`release_verify` green + pre-commit backstop clean; footprint exact (count 128, COMPACT); state trio
updated; roadmap item 8 -> SHIPPED; field register row added; plant-app kickoff written. Pushed on
Trevor's confirm; NO plant-astro bump.

No new gate is added, so no RED proof is owed -- but still inject a fall-spanning `second_planting`
envelope into a scratch copy and confirm A43 bounces it before trusting the warm-season batch.

Then item 9 (mid-South) follows, and the ruling shows it has the **identical gap shape** -- this arc is
its template, and the two should share fall-cycle authoring conventions.
