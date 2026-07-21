# Mid-South region -- design spec

**Date:** 2026-07-20
**Kickoff:** `docs/kickoffs/34-mid-south-region.md` (roadmap item 9)
**Base canonical:** `af5dcee9` (the mid_atlantic promote) / `origin/main`.
**Ruling that queued this:** `docs/reviews/notes/2026-07-15/tier2_mid_south_ruling.md` (CONDITIONAL-GO;
built as a full region per Trevor's 2026-07-16 ruling).
**Template:** the mid-Atlantic arc (`docs/superpowers/{specs,plans}/2026-07-20-mid-atlantic-region*`).
This is "the same arc as mid-Atlantic, except the three deltas in section 3." The mid-Atlantic plan's
task structure, gate ceremony, and A43/A45 verification apply verbatim.

## 1. Product goal
Author a real Mid-South region (`mid_south`, AR/OK/TN/MO) so the belt stops riding generic
frost-anchored zone dates that omit a documented second (fall) planting cycle for warm-season annuals.
The gap is identical to mid-Atlantic's; nothing here is misclassified today, the dates are just
conservative. Region label: **"Mid-South: Ozark Uplands and Delta Lowlands"** (the z7 Ozark/Ouachita/
Appalachian uplands + the z8 Mississippi Delta and river-valley lowlands).

## 2. Scope + zone span (the one decision, DECIDED)
Roster-wide (A31): all **111** certified region-carrying crops get a `mid_south` cell (82 frost_anchored
annuals + 14 chill_gated trees + 5 evergreen citrus + 5 woody-ornamental herbs + 4 berries + 1
strawberry). **zone_span `["7","8"]`**, decided from the real AR/OK/TN/MO ZIP distribution in plant-app
`zip-zones.json`: z7 1,883 (dominant: AR 236 / MO 360 / OK 640 / TN 647), z8 697 (AR 462 marquee), plus
z5 39 + z6 754 (colder `northern_tier`, excluded) and a single z9 TN ZIP (rides the belt verdict). Same
`["7","8"]` shape and z7-in-app dependency as mid-Atlantic (kickoff #32 / #35).

## 3. The three deltas from mid-Atlantic
1. **Sources not pre-catalogued (the main extra work).** Registered 6 new T1 `source_catalog` entries
   as part of the atomic promote: `nws_lzk` (z8 frost anchor), `uada_ext_fsa6001` (AR frost-zone table /
   z7 anchor), `uada_ext_spring_veg`, `uada_ext_fall_veg` (the fall cycle), `uada_ext_chill` (chill band),
   `uada_ext_fsa6105` (blackberry). The `uada_ext`/`ok_state_ext`/`mu_ext` parent portals already existed.
   Tooling extended: `region_harness` injects `staging/<region>_sources.json` into the scratch canonical
   (so per-crop gating sees the new ids), `build_region_promote` emits the `add $.source_catalog.<id>`
   patches into the same atomic batch.
2. **Chill is a real intra-state gradient**, not a flat figure. UAEX stations by Mar 1 (Utah model):
   Hope (SW warm edge, z8) 901, Fayetteville (Ozark, z7) 1,024, Wynne (NE Delta, z8) 1,069, Clarksville
   1,081. Band adopted: **z7 [1000,1300], z8 [900,1100]** (lower than mid-Atlantic's z7[1100,1500]/
   z8[1000,1350] because the Mid-South, further south with a warm SW edge, genuinely banks less). Both
   clear the 900-hour apple ceiling; the z8 floor is Hope's honest 901, flagged as the tight margin.
3. **Blackberry is the signature crop.** UAEX FSA6105: "adapted to all regions of Arkansas"; the UA fruit
   breeding program bred the canonical cultivars (Ouachita/Navaho/Apache/Kiowa/Arapaho + Prime-Ark) FOR
   Arkansas, and the canonical chill figures line up. Chill is a non-factor. Lead the blackberry prose on
   the home-state fit (the Mid-South analog of blueberry's mid-Atlantic highlight).

## 4. Frost anchors + fall cycle
Frost-anchored, standard deriver. z8 last Apr 3 / first Oct 31 (NWS Little Rock); z7 last Apr 10 / first
Oct 24 (FSA6001 Frost Zone D, northern/upland). Warm-season fall cycle from UAEX's fall table (tighter
than VCE's): tomato Jul 1-15, cucumber Aug 1-15, summer squash Jul 15-Aug 15, plus 3 UAEX-documented
fall adds mid-Atlantic did not carry (sweet-corn, green-beans-bush, potato); cool crops carry the belt's
strong Aug-Sep fall shoulder. `heat_pause` (not `season_over`) for cool-crop humid-summer gaps (the
se_gulf convention, not PNW cool-summer). No new field, no new gate: reuses A43/A45/A31/A32/A3/chill.

## 5. Tree / citrus suitability
All 14 chill-gated trees `fruits_reliably` on the band EXCEPT apricot + cherry-sweet + pomegranate
`marginal` (carried from mid-Atlantic, Trevor's 2026-07-20 call: chill clears, but humid-East early-bloom
frost / brown rot / fruit cracking); sour cherry stays `fruits_reliably`; pawpaw is native to the Ozarks.
5 citrus cold-limited.

## 6. Build / verification
Deterministic controller transform of the certified mid_atlantic cells to the mid_south anchors + UAEX
fall windows (`tools/build_mid_south_cells.py`: spring dates shifted by the anchor delta preserving
hand-authored succession windows; fall cycles authored fresh from UAEX via `second_cycle`; calendars
re-derived, heat_pause placement ported from the certified ground truth). Per-crop prose then rewritten
for honesty by a fan-out review pass. Verification = the mid-Atlantic ceremony: `gate_all` 119/119,
A45/A43/chill/calendar_coherence/timing_spine 0, `region_cell_audit` 0, footprint EXACT (111 cells +
chill band + provenance + 6 sources; 0 other keys; count 128; COMPACT), A45/A43 RED-checks, independent
content review. Dry-run: `docs/reviews/notes/2026-07-20/mid_south_promote_dryrun.md`.

## 7. App handoff + non-goals
plant-app kickoff #35 (`REGION_STATES.mid_south = AR,OK,TN,MO`; no ZIP3 fence; z7 half depends on the
temperate-region resolution fix #32). No plant-astro bump from this session. No new fields, no new gates,
no z6 extension, no re-authoring of existing regions. Stop before the canonical promote for Trevor's
approval, then push on his confirm. Next: item 10 (Nevada) or 11 (Utah).
