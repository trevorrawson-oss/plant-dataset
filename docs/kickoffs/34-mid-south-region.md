# Kickoff: Mid-South region (roadmap item 9)

**For:** a FRESH plant-dataset (Claude Code) session.
**Goal:** author a real Mid-South region `mid_south` (AR/OK/TN/MO) so the belt stops riding generic
zone dates that omit a documented FALL planting cycle for warm-season annuals -- the SAME gap the
mid-Atlantic region (item 8) just shipped for.
**Base:** rebase onto current `origin/main` (canonical `af5dcee9` after the mid-Atlantic push lands).
**Ruling that queued this:** `docs/reviews/notes/2026-07-15/tier2_mid_south_ruling.md` (CONDITIONAL-GO;
built as a full region per Trevor's 2026-07-16 ruling).

## This is the mid-Atlantic arc again -- reuse it directly

Item 9 has the **identical fall-cycle gap** as item 8. Do NOT re-derive the approach. Reuse:
- **The mid-Atlantic spec + plan** (`docs/superpowers/{specs,plans}/2026-07-20-mid-atlantic-region*`) as
  the structural template -- this kickoff is "same as mid-Atlantic except..." (the deltas are below).
- **`tools/second_cycle.py:build_two_cycle_cell`** for the ~30 fall-cycle annuals. See memory
  [[fall-cycle-deriver-combine-then-split]] -- `derive_annual_calendar` does NOT render `second_planting`;
  the helper is the only correct way.
- **The heat_pause-not-season_over convention** for cool-crop summer gaps (this is a humid belt like
  se_gulf, NOT cool-summer PNW). See memory [[mid-atlantic-region-spec]].
- **The shard fan-out** (11 family shards -> disjoint staging files -> controller merges + gates +
  commits centrally; validate one shard per mode before fanning out).
- **The region-generic tooling** (`region_harness`/`region_cell_audit`/`build_region_promote`): just add
  `mid_south` to `REGION_CONFIG` (frost_model "anchored"), `STAGING`, `EXPECTED_CELLS`, and
  `zone_span_gate.EXPECTED_SPANS`. NO new gate, NO new field.
- **Tree/citrus suitability:** trees `fruits_reliably` (chill clears), BUT **apricot + cherry-sweet =
  `marginal`** carries from mid-Atlantic (same humid-East climate family, Trevor's 2026-07-20 call:
  chill clears but early-bloom frost / brown rot / fruit cracking); sour cherry stays `fruits_reliably`.
  Citrus cold-limited.

## The deltas from mid-Atlantic (what's genuinely different / slightly heavier)

1. **SOURCES ARE NOT CATALOGUED (the main extra work).** Unlike mid-Atlantic (`ncsu_ext`/`vce_426_331`
   already in `source_catalog`), NO AR/OK/TN/MO source was catalogued. You MUST register the UAEX
   (University of Arkansas Cooperative Extension) sources + NWS Little Rock to `source_catalog` (a
   canonical write, part of the promote batch). The ruling already found + read the load-bearing set:
   - **UAEX FSA6105** "Blackberry Production in the Home Garden" (PDF) -- the blackberry signature source.
   - **UAEX "Planting Dates for Fall Vegetable Production"** -- the fall tomato transplant window (Jul
     1-15, 75-80 DTM), the fall-cycle anchor.
   - **UAEX "Arkansas spring and summer vegetable planting dates"** -- the spring windows.
   - **UAEX "Chilling Hour Reports"** blog -- the real chill accumulation.
   - **NWS Little Rock** frost normals.
   Budget a T1 hunt to fill per-crop windows across the roster (UAEX is Arkansas-centric; the belt spans
   4 states -- AR/UAEX is the marquee anchor, supplement with OK State / UT... no: TN (UT Extension) /
   MO (Univ. of Missouri Extension) where AR windows do not cover a crop). PDF extraction in the
   CONTROLLER env with `pypdf` (subagent sandboxes block it).

2. **CHILL: a real intra-state gradient, not a single flat figure.** AR stations by Mar 1: Fayetteville
   1,024 / Clarksville 1,081 / Wynne 1,069 / **Hope (SW warm edge) 901**. Hope barely clears McIntosh's
   900-hr ceiling (1 hr margin). So the `region_chill_delivered.mid_south` band should reflect the
   spread (the warm SW/southern edge is tighter than mid-Atlantic's blanket ">1,000"), e.g. a low bound
   near ~900 at the z8 warm edge. Still clears the tree set, so all trees `fruits_reliably`, but author
   the band + `chill_basis` honestly to the gradient. Blackberry is a NON-factor for chill (clears many
   times over).

3. **Blackberry is the SIGNATURE crop -- author with confidence.** UA's own breeding program bred the
   canonical cultivars for Arkansas (Ouachita/Navaho/Apache/Kiowa/Arapaho + the Prime-Ark primocanes),
   and the canonical chill figures line up with UA's published FSA6105 numbers. This is the belt's
   strongest match -- lead the blackberry `mid_south` cell + prose on it. (Analogous to how blueberry
   was the mid-Atlantic berry highlight; here it is blackberry.)

4. **Multi-state, AR marquee.** Frost anchors from Little Rock (NWS): last frost **Apr 3**, first frost
   **Oct 31** (z8). The 1-ZIP TN z9 sliver rides the belt verdict (negligible).

## The ONE decision to make first (the mid-Atlantic scoping lesson)

**Zone span:** the ruling sampled **z8** (Little Rock), but the belt states AR/OK/TN/MO span cooler
zones too. **Read the real AR/OK/TN/MO ZIP distribution from plant-app `zip-zones.json` FIRST** (the
mid-Atlantic lesson: scope from the real ZIP distribution, not the ruled span). Likely `["7","8"]` like
mid-Atlantic (z7 probably dominant across the 4 states); confirm, and decide whether to include the
z9 TN sliver. Do this before authoring.

## The z7 in-app dependency (same as mid-Atlantic)

`mid_south` will likely span z7-8, and the z7 half's in-app delivery depends on the plant-app
temperate-region resolution fix (kickoff **#32**, the `isWarm` decoupling) -- the same dependency
mid-Atlantic has. Write a paired plant-app kickoff (`REGION_STATES.mid_south = AR,OK,TN,MO`; no ZIP3
fence expected; cross-reference #32).

## Read first
- The mid-South ruling (above) + `docs/region_coverage_roadmap.md` item 9.
- The mid-Atlantic spec/plan/kickoff #31 (the template) + `docs/reviews/notes/2026-07-20/mid_atlantic_sources.md`
  (the sourcing-note format to mirror).
- memories [[fall-cycle-deriver-combine-then-split]], [[mid-atlantic-region-spec]], [[maritime-pnw-region]].

## Definition of done
`mid_south` authored + certified across the region-carrying roster (~111, re-count against the live
canonical); UAEX/NWS sources registered to `source_catalog`; `gate_all` 119/119 + A45/chill/A43/
coherence 0 + footprint exact + independent content review; state trio + roadmap item 9 SHIPPED +
field-register row 20; plant-app kickoff written. Committed + PUSHED on Trevor's confirm; NO plant-astro
bump from this session. Then item 10 (Nevada) or 11 (Utah) is next (Utah's z8 core is only 15 ZIPs --
see its own scoping note).
