# Kickoff: Southeast Alaska panhandle region (roadmap item 7)

**For:** a FRESH plant-dataset (Claude Code) session.
**Goal:** author a real Southeast Alaska panhandle region (`se_alaska`, Ketchikan through Juneau,
z7-8) so the panhandle stops riding generic frost-anchored zone dates that are wrong in KIND, not
just imprecise.
**Base:** canonical `e1e01c47` / dataset `main` @ `67fe7ed` (== `origin/main`). Rebase onto current
`origin/main` before starting.
**Design spec:** `docs/superpowers/specs/2026-07-20-se-alaska-panhandle-region-design.md` -- **read it
first; it is complete.** The scope calls, the zone-span decision, the two new fields, and the app-side
blocker are all made and argued there. Start from `superpowers:writing-plans`, not from brainstorming.
**Precedent:** third authored region. **PNW (#27) is the structural template** (frost-anchored, same
toolchain); RGV (#25) is the frost-free one and does NOT apply here.

## Why this belt is different from the four that shipped or were waved through

The Tier-2 ruling (`docs/reviews/notes/2026-07-15/tier2_alaska_ruling.md`) is the only NEW-REGION
verdict of the five. Two of three basket crops diverge at the **suitability-class** level:

- **Warm-season annuals need protection.** Three independent UAF sources, including a controlled
  Palmer trial where "adjacent plots outside gave almost no yields." The naive deriver renders a
  perfectly ordinary outdoor tomato calendar. Its premise, not its window length, is what is wrong.
- **Apple's real UAF variety list has ZERO overlap with the canonical 16.** The panhandle's binding
  constraint is ripening time in a 191-day season, a mechanism this dataset does not model for apple.
  Naively, the chill logic reads AK's abundant chill and defaults toward `fruits_reliably` off the
  wrong list.

**SE Alaska is not a colder PNW.** The ruling checked directly: PNW z8's own authored cells say
cherry-tomato needs "no special early-variety caution" and apple `fruits_reliably`. Both are the
opposite of what UAF documents here.

## The three things that make this arc bigger than PNW's

1. **Two new conditional fields + two new gates.** `protected_culture` (A46) and
   `recommended_varieties` (A47). Both follow the flat `grown_as` / `recommended_type` idiom already
   in the schema, both are shape-only gates on the A44/`planting_layout` model, both are **RED-first
   before any authoring lands**. Spec sections 4.4 and 4.5.
2. **The zone span is `["7","8"]`, and the ZIP3 fence is load-bearing.** z8 alone is 6 real panhandle
   ZIPs and leaves out Juneau and Sitka. Naive state+zone matching pulls 21 Southcentral/Kodiak ZIPs
   into a panhandle calendar. Fence to ZIP3 **998 + 999**. Spec 4.2.
3. **An app-side prerequisite for the z7 half** (handoff already written, kickoff #32). Corrected
   mechanism: plant-app's `zones.ts:resolveFromZip` won't assign `se_alaska` to a z7 grower (gated on
   `isWarmZone` >= 8), so Juneau/Sitka fall back to `northern_tier`'s z7 cell. This is NOT a
   `northern_tier`-stranding bug -- `guide-calendar.ts:resolveZoneCell` already delivers `northern_tier`
   for cold zones. Spec 9.2.

## Read first

- The design spec (above). Then `docs/reviews/notes/2026-07-15/tier2_alaska_ruling.md` for the
  sourcing detail -- it already located and text-extracted the core UAF publications.
- `docs/region_coverage_roadmap.md` -- item 7 is this; items 8-11 are the other four belts, all now
  full region builds per Trevor's 2026-07-16 ruling.
- `docs/kickoffs/27-maritime-pnw-region.md` + the PNW spec/plan -- the template arc.
- `docs/gs_cross_crop_field_addition_v0.md` + `docs/field_addition_register.md` -- a region is a
  roster-wide column, and this arc adds two more conditional fields on top.
- memory `maritime-pnw-region` (the toolchain + reusable lessons) and
  `subagent-resumability-and-concurrent-git-safety` (concurrent-checkout git discipline).

## Roster (confirmed against canonical `e1e01c47`)

**111 certified region-carrying crops** (up from PNW's 108; the 3 corn crops certified since):
82 `frost_anchored`, 14 `perennial_chill_gated`, 5 `perennial_evergreen`, 5
`perennial_woody_ornamental`, 4 `berries_woody`, 1 `perennial_herbaceous`. Option A (full roster-wide)
is forced by A31, not chosen. The 8 microgreens carry no `regions` block; the 9 uncertified shells are
exempt.

## Do this first, before authoring anything

**Hunt the `region_chill_delivered.se_alaska` band.** The ruling searched for a Ketchikan/SE-Alaska
chill figure and did not find one. It is user-displayed in plant-astro and A3 reads its low end. The
direction is not in doubt (a cool maritime climate banks chill generously; this dataset's own
`northern_tier` z3 cell says so verbatim), but the magnitude needs a source. **If no T1 AK figure
exists, stop and bring options to Trevor rather than picking a number.** Spec 4.8.

Second: extract z7 (Juneau/Sitka) frost normals from the NWS AJK "Last Spring Freeze" table the ruling
already has. z8 is done (Ketchikan: last frost Apr 22, first frost ~Oct 30).

**PDF gotcha, now confirmed across three arcs:** WebFetch's summarizer cannot decode these PDFs.
Re-extract with `pypdf` from the cached binary, **in the controller env** -- subagent sandboxes block
network and PDF tooling.

## Reusable (do NOT rebuild)

`tools/region_harness.py`, `tools/region_cell_audit.py`, `tools/build_region_promote.py` -- all already
region-generic from the PNW arc. Pass `se_alaska`; allow `cold_pause` (frost-anchored, as PNW). The
SDD shape: class-batched authoring, fresh-subagent review per batch, per-crop harness gate, scratch
dry-run, one atomic SHA-guarded promote, Trevor-gated.

## Definition of done

`se_alaska` authored + certified across the 111 roster; A46/A47 RED-proofed and wired; A45/A31/A32/A3
+ `gate_all` 119/119 + `release_verify` green + pre-commit backstop clean; footprint exact (count 128,
COMPACT); state trio updated; roadmap item 7 -> SHIPPED; field register rows added (region column, the
two new fields, and the queued `heat_accumulation`-for-deciduous-trees follow-on); a plant-app kickoff
written covering `REGION_STATES.se_alaska`, the 998/999 fence, the variety-card caveat, and the
`isWarm` decoupling. Dataset pushed on Trevor's confirm; NO plant-astro bump from this session.

Then the program is down to items 8-11 (mid-Atlantic, mid-South, Nevada, Utah), item 6 (Puerto Rico,
a product call), and item 2 (app-side cleanup).
