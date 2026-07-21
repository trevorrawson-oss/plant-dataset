# Region coverage roadmap -- ZIP -> zone -> region -> dates, the whole chain

**Origin:** `docs/2026-07-12-region-zonespan-gaps.md` (plant-app sweep) +
`docs/superpowers/specs/2026-07-12-region-zonespan-reconciliation-design.md`.
**Goal (Trevor, 2026-07-12):** a user types their ZIP and gets their proper,
up-to-date zone AND region with correct planting information.

Getting there runs through a four-link chain, each with a different owner:

1. **ZIP -> zone** -- plant-app `zip-zones.json` (already on the 2023 USDA map)
2. **zone + state -> region** -- region `zone_span`s (THIS repo; item 1 below)
3. **region + zone -> dates** -- per-crop `resolved_by_zone` rows (THIS repo)
4. **no region -> generic zone dates** -- the fallback; fine for some states, misleading for others

Every gap from the sweep carries one of four rulings: WIDENED (fixed by item 1) /
NEW REGION (queued) / GENERIC-OK (generic zone dates are the deliberate answer) /
HANDED OFF (different owner, a first-class item here, not a footnote).

## The program

| # | Item | Owner | Status | Impact |
|---|------|-------|--------|--------|
| 1 | Zone-span widen (2023-map reconciliation, A45 gate) | dataset | SHIPPED 2026-07-12 | ~320 ZIPs regain region resolution |
| 2 | App-side cleanup: ~285 empty-state ZIP rows in zip-zones.json; verify the regions.json sync path end to end; fence ZIP3 785xx to the new `rgv` region (item 3 shipped below; paired app-side kickoff `docs/kickoffs/26-rgv-plant-app-zip3-fence.md`); **+ temperate-region resolution / `isWarm` decoupling (kickoff #32, the priority app-side item)** | plant-app | QUEUED (next) | ~285 ZIPs broken regardless of spans until fixed; 785xx fence resolves RGV ZIPs to `rgv` in-app; the `isWarm` gate stops NEW temperate regions' z7 halves from being assigned (not a `northern_tier` bug -- that already resolves) |
| 3 | Rio Grande Valley / subtropical TX region (new authored region; TAMU AgriLife RGV calendars are strong T1) | dataset | **SHIPPED 2026-07-13** (canonical `d0832254`) | 95 TX z10 ZIPs off the se_gulf interim; app-side 785xx ZIP3 fence is the paired follow-up (item 2 / kickoff #26) |
| 4 | Maritime PNW region (WA/OR z8-9; WSU/OSU extension T1) | dataset | **SHIPPED 2026-07-14** (canonical `8dd4ac4c`) | ~750 ZIPs off generic frost-anchored dates; app-side west-side ZIP3 fence is the paired follow-up (kickoff #28) |
| 5 | Judged later, each needs an explicit ruling: mid-Atlantic z8 belt (NC 793 / VA 258 / MD 117 / DC 215 / DE-NJ-PA small), mid-South (AR 460 / OK 106 / TN 123 / MO 6), NV (110) / UT (15) / AK (13) | dataset | **RULED 2026-07-15** (4x CONDITIONAL-GO: mid-Atlantic, mid-South, Nevada, Utah; 1x NEW-REGION: Alaska) | all 5 belts ruled with real T1 evidence, not a first-read guess; every belt surfaced an actual region-building candidate (a real, sourced planting-window or suitability gap the generic fallback doesn't capture) -- 1 clears the NEW-REGION bar outright (Alaska, item 7), 4 stop short of that bar but their caveats are the same KIND of finding that justified RGV/PNW, so they're queued as candidates too (items 8-11), the same "same zone, different real climate" precedent the `ca_interior`/`ca_north_coast`/`ca_south_coast`/`ca_desert` split already establishes |
| 6 | Puerto Rico (2 z11 / 47 z12 / 126 z13) | product call (Trevor) | OPEN | market-scope question first; also needs z12/13 support end to end |
| 7 | Southeast Alaska panhandle region `se_alaska` (new authored region; UAF Cooperative Extension Service T1 -- Ketchikan through Juneau, maritime **z7-8**, 28 panhandle ZIPs) | dataset | **SPEC'D 2026-07-20** (`docs/superpowers/specs/2026-07-20-se-alaska-panhandle-region-design.md`, kickoff #30) -- ready for a fresh build session | surfaced by item 5's Alaska ruling (**NEW-REGION**, `docs/reviews/notes/2026-07-15/tier2_alaska_ruling.md`): unprotected outdoor tomato yields collapse per a UAF field trial (needs protected-culture guidance, not a window fix); the real SE-AK apple variety list shares zero overlap with the canonical chill-tier list (season-length-bound, a mechanism the chill model doesn't represent) |
| 8 | Mid-Atlantic region `mid_atlantic` (NC/VA/MD/DC/DE-NJ-PA, **z7-8**; VCE/NC State Extension T1) | dataset | **SHIPPED 2026-07-20** (canonical `e1e01c47` -> `af5dcee9`; 111 cells; fall-cycle for ~30 annuals via the new `tools/second_cycle.py` helper; apricot/cherry-sweet marginal; gate_all 119/119; register row 19; kickoff #31; committed UNPUSHED + owes plant-app #33) -- was the lightest arc (no new field, no new gate) | surfaced by item 5's mid-Atlantic ruling (**CONDITIONAL-GO**, `docs/reviews/notes/2026-07-15/tier2_mid_atlantic_ruling.md`): the naive fallback calendar misses a real, T1-documented FALL tomato planting window (VCE 426-331's zone-8 spring-AND-fall two-cycle table) that the generic single-cycle assumption doesn't have |
| 9 | Mid-South region (AR/OK/TN/MO z8, +TN z9 sliver; UAEX/University of Arkansas T1) | dataset | QUEUED | surfaced by item 5's mid-South ruling (**CONDITIONAL-GO**, `docs/reviews/notes/2026-07-15/tier2_mid_south_ruling.md`): same missing-fall-tomato-window gap as mid-Atlantic, independently evidenced (2 UAEX sources); blackberry's real UA breeding-program per-cultivar chill data (Ouachita/Navaho/Apache/Kiowa/Arapaho) is ready to author directly |
| 10 | Nevada high-desert region (z8/z9/z10, Las Vegas/Clark County anchor; UNR Extension T1) | dataset | QUEUED | surfaced by item 5's Nevada ruling (**CONDITIONAL-GO**, `docs/reviews/notes/2026-07-15/tier2_nevada_ruling.md`): the naive calendar's flat back half is actively misleading (not just incomplete) -- misses the real Jun-Sep heat-abort period AND the real Nov frost return; apple needs real variety-chill tiering (6 of 16 canonical varieties sit above the confirmed 700hr trial ceiling with no local evidence either way); garlic's real fall window differs from the neighboring `warm_arid`/`low_desert_az` cross-reference regions |
| 11 | Utah "Dixie" high-desert region (St. George/Washington County z8 core; USU Extension T1) | dataset | QUEUED | surfaced by item 5's Utah ruling (**CONDITIONAL-GO**, `docs/reviews/notes/2026-07-15/tier2_utah_ruling.md`): same tomato heat/frost-return gap as Nevada; apple leans marginal at St. George's elevation per county extension (currently would default to the canonical's `fruits_reliably` assumption, unchecked); raspberry needs fall-bearing/low-chill cultivar steering, confirmed via this dataset's own pre-existing `warm_arid` raspberry text (same USU source) |

Items 3+ are their own arcs (spec -> plan -> build). Nothing below item 2 blocks item 2.

**Trevor's ruling (2026-07-16, restated 2026-07-20): items 7-11 are all FULL NEW REGIONS**, not
candidates awaiting a second go/no-go. The 4 CONDITIONAL-GO belts are built the same way the
NEW-REGION one is; a real, sourced planting-window or suitability gap is reason enough on its own,
the same "same zone, different real climate" precedent the `ca_interior`/`ca_north_coast`/
`ca_south_coast`/`ca_desert` split already establishes. Each is its own spec -> plan -> build arc.

**Build order (Trevor, 2026-07-20): 8 -> 9 -> 10 -> 11 -> 7.** Finish the four z8 belts first, then
Alaska. Items 8 (mid-Atlantic) and 7 (Alaska) are both SPEC'D as of 2026-07-20; **item 8 is the one
to build next**. Items 9-11 are unsequenced relative to each other within that block, though 9
(mid-South) has the identical gap shape to 8 and should reuse its conventions directly.

## Item 1 record: the widen (SHIPPED 2026-07-12, canonical 7e29f4f4)

| Region | Span change | Donor | ZIPs |
|---|---|---|---|
| low_desert_az | [9] -> [9,10] | z10 <- z9 | 71 (Phoenix metro) |
| hawaii_tropical | [11] -> [10,11,12,13] | all <- z11 | 122 (Honolulu +) |
| ca_south_coast | [9,10] -> [9,10,11] | z11 <- z10 | 28 (coastal LA/SD; |
| ca_desert | [9,10] -> [9,10,11] | z11 <- z10 | app picks by ZIP3) |
| se_gulf | [8,9] -> [8,9,10] | z10 <- z9 | 6 (New Orleans fringe) |

**Mechanics.** `tools/build_zonespan_widen_patch.py` -> `tools/batches/zonespan_widen.json`
(756 cloned calendar rows + 7 cloned chill bands + 670 zone_span normalizations,
across the 108 CERTIFIED region-carrying crops) -> `tools/apply_patch.py`. Every
cloned calendar row carries `lifted_from_zone: "<donor>"` (the established idiom; 6
prior instances, e.g. lettuce-leaf se_gulf z8 <- z9). Every populated `zone_span` on a
certified crop is now str-typed and uniform, enforced by A45 (`tools/zone_span_gate.py`:
expected-span table + span<->resolved_by_zone key parity + donor integrity). Widening a
span is now a deliberate paired edit: `EXPECTED_SPANS` + cloned rows.

**Certified roster only.** The widen touches the 108 certified region-carrying crops.
The 9 uncertified shells (avocado, olive, artichoke, asparagus, and the 5 mushrooms)
are skipped: their warm cells are empty-calendar placeholders, so cloning them into the
new zones would propagate empty frost_anchored cells and trip A32 (calendar-presence).
Shells are exempt from the cert suite until authored (the same rule gate_all uses), and
the app unions `zone_span` across crops, so the new zones still resolve from the
certified roster. A shell picks up the full span + filled cells when it is authored and
certified. This defect was caught by the pre-commit release-verify safety net (it checks
all changed crops, unlike gate_all / release_verify which are certified-only) and fixed
before promote; A45 was made certified-only to match.

**Why cloning is honest.** The 2023 USDA map relabeled the cities these regions were
authored FOR; the climates and calendars did not change. Phoenix (relabeled 9b->10a) is
what low_desert_az's UA az2078 / Maricopa az1005 calendars describe; Honolulu (->z12) is
what the CTAHR guidance describes; the warm CA coast pockets (->z11) are the warm edge of
the z10 rows; the New Orleans fringe (->z10) sits inside se_gulf's LSU-sourced belt.

### Clone honesty record (per-region provenance audits, 2026-07-12)

- **low_desert_az (Phoenix 9b->10a) -- GO.** Donor rows are Phoenix-authored by
  construction: az1005 is the Maricopa County calendar, az2078 the UA low-desert guide.
- **se_gulf (New Orleans fringe ->z10) -- GO.** Donor z9 rows draw on a genuine Gulf
  belt (clemson 108, uga 90, ncsu 54, uf 32, lsu 28, msstate 22, tamu 12), including
  Louisiana's own LSU AgCenter.
- **ca_south_coast (warm coast ->z11) -- GO.** 82% of resolved rows carry a UC ANR-family
  source; a real z9-vs-z10 gradient exists (50% of crops differ) and the direction is
  unambiguous (z10 always starts earlier / extends later), confirming z10 is the correct
  warm-edge donor for z11.
- **ca_desert (->z11) -- GO.** Same profile: 76% UC-family sourced (plus uariz_ext for the
  AZ-border desert), 43% z9-vs-z10 gradient, z10 the consistent warm edge.
- **hawaii_tropical (Honolulu ->z12) -- CONDITIONAL GO (Trevor-approved).** 66% of the
  region's rows carry a genuine CTAHR/UH citation; most of the rest are honestly flagged
  non-viable (unsuitable/marginal, empty calendars -- cloning a "doesn't grow here"
  verdict is safe). No frost-data contamination (all suspect rows resolve z11 frost-free,
  `last_frost: null`). Residual quality gap recorded below.

**Heat-pause spot check.** The two hot widens (AZ z10, se_gulf z10) donor rows for
heat-sensitive crops (lettuce-leaf, cherry-tomato) already carry explicit summer
`heat_pause` objects -- the donors encode the hot-summer reality the new label describes.

## The RGV interim ruling (Trevor-approved 2026-07-12) -- SUPERSEDED 2026-07-13

**RETIRED.** This section documented the temporary answer; item 3 below shipped the real
region on 2026-07-13, so the interim no longer applies. Left here for the historical
record only -- do not re-derive RGV dates from se_gulf.

Widening se_gulf to z10 auto-matched the 95 TX Rio Grande Valley z10 ZIPs (TX is in the
app's se_gulf state mapping). That shipped as an EXPLICITLY INTERIM answer: Gulf-coast
winter-garden dates were directionally right for RGV and better than a bare zone label,
and se_gulf's source set already included tamu_agrilife. Item 3 has now replaced it with
a real, authored RGV region; item 2's remaining app-side task is the 785xx ZIP3 fence
(kickoff #26), not a "keep interim vs. fence to generic" decision.

## Item 3 record: RGV region SHIPPED (2026-07-13, canonical `d0832254`)

A real, authored Rio Grande Valley / subtropical South Texas region `rgv` (`zone_span`
`["9","10"]`) landed across all 108 certified region-carrying crops in one atomic,
SHA-guarded commit (`4e2e9e7`; canonical `7e29f4f4` -> `d0832254`; count 125 unchanged,
116 certified unchanged -- a roster-wide column, not a new crop). Class split: 79
frost_anchored annuals, 5 flagship citrus (lime marginal), 14 chill-gated trees (A3
no-fruit split, pawpaw unsuitable), 5 woody herbs, 4 berries, strawberry -- all T1-sourced
to TAMU AgriLife LRGV / South-Texas guides. No new gate was needed: A45 `zone_span_gate`,
A3, and A31/A32 were already region-generic from the 2026-07-12 reconciliation. Full
detail in `STATE_HISTORY.md` (2026-07-13 entry) and `CURRENT_STATE.md`'s top block; spec+
plan `docs/superpowers/{specs,plans}/2026-07-13-rgv-subtropical-tx-region*`; field-addition
register row 15. Paired app-side follow-up: the plant-app 785xx ZIP3 fence (item 2,
kickoff `docs/kickoffs/26-rgv-plant-app-zip3-fence.md`) -- the dataset side is done, but
RGV ZIPs do not actually resolve to `rgv` in the app until that fence lands.

## Item 4 record: maritime PNW region SHIPPED (2026-07-14, canonical `8dd4ac4c`)

A real, authored maritime Pacific Northwest region `pnw` (`zone_span` `["8","9"]`, WA/OR
west of the Cascades) landed across all 108 certified region-carrying crops in one atomic,
SHA-guarded promote (canonical `060d8711` -> `8dd4ac4c`; 110 patches; count 125 unchanged,
116 certified unchanged -- a roster-wide column, not a new crop). **The key inversion from
RGV: PNW is FROST-ANCHORED (not frost-free)**, so cells use `resolution_method=
"frost_anchored_resolved"` + real `resolved_from` frost dates (z8 Sea-Tac NOAA, z9 Astoria)
+ the standard `annual_calendar` deriver + `cold_pause` winters -- no Hawaii-shape
hand-authoring, far lighter than RGV. Class split (all T1, WSU/OSU): 79 frost_anchored
annuals (summer is the growing window, no `heat_pause`; cool crops thrive/overwinter, warm
crops transplant-led + honest-marginal per OSU EM9027, with okra/sweet-potato/melons
carrying OSU "not suitable"); 14 chill-gated trees (the A3 FRUIT flip -- PNW chill
`[968,1950]` amply clears the floor, so trees `fruits_reliably` (apple/pears/cherries/plum/
fig/mulberry/persimmon) or `marginal` (peach/apricot/nectarine on cool-wet-spring disease,
pomegranate/pawpaw on heat), never `survives_no_fruit`-empty -- the opposite of RGV); 5
citrus cold-limited; 5 woody herbs (lavender thrives); 4 berries (WA #1 raspberry, premier
blueberry) + strawberry. No new gate: reuses A45/A3/A31/A32. New region-generic tooling
`tools/region_harness.py` + `tools/region_cell_audit.py` + `tools/build_region_promote.py`
(parametrized from the RGV tools; `cold_pause` allowed for the frost-anchored region). Full
detail in `STATE_HISTORY.md` (2026-07-14 entry) + `CURRENT_STATE.md`'s top block; spec+plan
`docs/superpowers/{specs,plans}/2026-07-14-maritime-pnw-region*`; dry-run `docs/reviews/
notes/2026-07-14/pnw_promote_dryrun.md`; field-addition register row 17. Paired app-side
follow-up: the plant-app west-side ZIP3 fence (kickoff `docs/kickoffs/28-pnw-plant-app-zip3-
fence.md`) so the hot-dry east-of-the-Cascades z8 pockets (Spokane / Columbia Basin) do NOT
resolve to a maritime calendar -- the mirror of RGV's 785xx fence; the dataset side is done
but WA/OR z8-9 ZIPs do not resolve to `pnw` in the app until that fence lands. **With item 4
shipped, the region program is down to item 5 (the judged-belt / Tier-2 ruling pass) + item
6 (PR, a product call).**

## The warm-edge chill caveat (Trevor-approved 2026-07-12)

`region_chill_delivered` (the shared chill table, ALSO displayed in-app as "your area
banks ~X chill hours") carries the same zone gaps as the calendars. The widen clones the
donor zone's band to each new zone so A3 (the tree no-fruit split) has a band and the
display stays consistent with the cloned calendar. For the same-city relabels
(low_desert_az z10, hawaii_tropical z10/12/13) the band is exactly honest. For the 3
warm-edge gaps -- se_gulf z10 (from z9 [350,650]), ca_south_coast z11 and ca_desert z11
(from z10 [50,350] / [100,300]) -- the inherited band is slightly generous versus a
half-zone-warmer reality, but it stays in the already-declared no-fruit direction, the
bands are coarse, and it is consistent with the cloned calendar. **Follow-up candidate:**
replace the 3 warm-edge bands with sourced z-specific chill values in a later pass.

## Data-quality item: Hawaii generic-precompute crops (roster-wide, pre-existing)

The hawaii_tropical audit found ~25 certified crops (lemon, lime, bok-choy, spring-onion,
thyme, rosemary, oregano, sage, raspberry, blackberry, elderberry, parsnip, leek, shallot,
and several flowers) presenting normal, unflagged tropical calendars built entirely from
mainland extension sources via a generic precompute engine, with zero CTAHR/UH citation.
The same crop list recurs in ca_south_coast and ca_desert, so this is a pre-existing,
roster-wide "honest shell" condition (minor crops not yet through per-region GS-arc
authoring), NOT introduced by the relabel/clone -- the data was already live under the z11
label. The clone does not make it worse. Queued as a data-quality pass (per-region
authoring for these crops); not blocking the widen.

## Tier-2 rulings pending (item 5 detail)

The taxonomy deliberately special-cases marquee warm states; everywhere else gets generic
frost-anchored zone dates. Where that is honest, GENERIC-OK is the ruling, recorded here --
not silence. All 5 Tier-2 belts below are now RULED (2026-07-15), each against a real T1
basket, not a first-read guess -- maritime PNW itself was the original NOT-ok precedent (cool
summers invert the assumptions; item 4). **Mid-Atlantic z8 (Raleigh NC marquee) --
CONDITIONAL-GO (ruled 2026-07-15).** Real Raleigh frost normals (NC State Extension: last
frost Apr 8, first frost Oct 30) plus a 3-crop T1 basket show tree fruit (apple, chill clears
the whole canonical variety range) and berry (blueberry, genuine NC-documented highbush/
rabbiteye range) are honestly served by generic frost-anchored dates; the one real gap is
warm-season annuals (cherry-tomato) -- NC State's own planting calendar and VCE 426-331 both
document a second (fall) planting window that the naive single-cycle deriver omits, the same
`heat_pause`-shaped gap already modeled for other hot z8/z9 belts. Not a suitability flip, so
NEW-REGION is not warranted; caveat recorded for any future authoring pass. Full sourcing and
naive-vs-real detail: `docs/reviews/notes/2026-07-15/tier2_mid_atlantic_ruling.md`. **Mid-South
z8 (AR/OK/TN/MO, Little Rock AR marquee) -- CONDITIONAL-GO (ruled 2026-07-15).** Real Little Rock
frost normals (NWS: last frost Apr 3, first frost Oct 31) plus a newly-sourced 3-crop T1 basket
(no source for this belt was previously catalogued) show tree fruit (apple, real AR chill
accumulation 901-1,081 hrs clears the whole canonical variety range, tightest at the belt's
southwestern warm edge) and berry (blackberry, UA's own breeding-program cultivars and chill
figures line up directly with the canonical values) are honestly served by generic
frost-anchored dates; the one real gap is the same class found in mid-Atlantic -- two independent
UAEX pages document an explicit fall (Jul 1-15) tomato planting cycle that the naive single-cycle
deriver omits. Not a suitability flip, so NEW-REGION is not warranted; caveat recorded for any
future authoring pass, plus a note that any future chill treatment should reflect the belt's real
intra-state gradient rather than one flat figure. Full sourcing and naive-vs-real detail:
`docs/reviews/notes/2026-07-15/tier2_mid_south_ruling.md`. **Nevada z8/z9/z10 (Las Vegas / North
Las Vegas marquee, z9 dominant at 94 ZIPs vs. z8 15 / z10 1) -- CONDITIONAL-GO, broader than
mid-Atlantic/mid-South (ruled 2026-07-15).** A genuinely different climate archetype (high
desert, not humid) does not reproduce the other two belts' narrow single-gap shape. Real Las
Vegas frost normals (NWS Technical Memorandum WR-235: last frost Feb 28, first frost Nov 25) plus
a 3-crop T1 basket (cherry-tomato / apple / garlic, per the brief) surface three separate real
findings: cherry-tomato's real spring start matches UNR's own recommended dates, but the naive
single-cycle deriver's `growing`-for-6-months back half actively contradicts UNR's stated
>90°F/<55°F summer fruit-set cutoff and the real Nov 25 frost return (a sharper, more actively
misleading gap than the humid belts' merely-incomplete flat `cold_pause`); apple is confirmed
`fruits_reliably` by a direct peer-reviewed UNR field trial at the marquee city itself (SP-20-07),
running counter to any chill-starved assumption, but a real third of the canonical
recommended-variety list (the 700-900 hr tier) sits above the trial's confirmed chill ceiling
with no Nevada-specific evidence either way -- the sharpest variety-level caveat found in this
arc so far; garlic is confirmed genuinely arid-friendly (a real Sept-to-mid-Oct fall
clove-planting window at the marquee city, narrower than but consistent with the existing
`warm_arid`/`low_desert_az` cross-reference regions). None of the three basket crops shows a
suitability-CLASS mismatch, so NEW-REGION is not warranted, but the caveats are real and broader
than a one-line footnote; recorded for any future authoring pass (heat-pause + widened spring
succession for warm annuals, chill-tier variety differentiation for apple, a belt-specific
garlic window rather than inheriting a neighbor's). Full sourcing and naive-vs-real detail:
`docs/reviews/notes/2026-07-15/tier2_nevada_ruling.md`. **Utah z8 (St. George / Washington
County "Dixie" marquee, 15 ZIPs) -- CONDITIONAL-GO (ruled 2026-07-15).** Real St. George frost
normals (USU Extension Washington County: last frost Mar 30, first frost Nov 1, sourced to Utah
Climate Center actual records) plus a 3-crop T1 basket (cherry-tomato / apple / raspberry, per
the brief) show cherry-tomato directionally fine (naive spring start close to USU's own Apr 1
transplant date; the one real gap, a flat naive winter `cold_pause` that hides the real summer
heat-abort period and mischaracterizes September/October as dormant, mirrors Nevada's shape, not
mid-Atlantic/mid-South's -- USU does not recommend a fall tomato cycle here either) and raspberry
genuinely belt-identified (USU names "Utah's Dixie" directly as fall-bearing-raspberry territory)
but marginal, needing heat-tolerant low-chill cultivars per both USU's own raspberry guide and
this dataset's own pre-existing `warm_arid` raspberry region text. Apple is the sharpest,
class-level (not just variety-tier) caveat found in this arc so far: Washington County's own
Extension office recommends apple only for the county's higher-elevation towns, which sit outside
this z8 belt entirely, not for the low-elevation St. George core the belt's ZIPs actually cover;
this dataset's own existing z8/z9 desert apple regions (`warm_arid` NM `fruits_reliably` at
400-700 chill hr/~3,900 ft, `low_desert_az` AZ `marginal` at 250-400 chill hr/~1,100 ft) bracket
St. George's real elevation (2,624 ft) closer to the `marginal` end, though no hard local
chill-hour figure was found despite a genuine search effort (an open gap, not glossed over) so
this stops short of a confirmed suitability-class flip. None of the three basket crops shows a
confirmed suitability-CLASS mismatch, so NEW-REGION is not warranted, but the caveats are real
and the apple finding is the sharpest of the arc; recorded for any future authoring pass (a real
heat-pause + accurate frost-return date for warm-season annuals, fall-bearing/low-chill cultivar
steering for raspberry, and apple treated as leaning `marginal` pending a real St.-George-specific
chill-hour figure). Full sourcing and naive-vs-real detail:
`docs/reviews/notes/2026-07-15/tier2_utah_ruling.md`. **Alaska z8 (Ketchikan marquee, 13 ZIPs,
southeast panhandle, maritime) -- NEW-REGION (ruled 2026-07-15).** The belt the design spec
flagged as the strongest a priori NEW-REGION candidate (the closest Tier-2 analog to maritime
PNW's own confirmed inversion), and the evidence bears that out. Real Ketchikan frost normals
(NWS AJK "Last Spring Freeze" statistical table: mean last frost Apr 22, 38 yrs of data; NOAA NCEI
Local Climatological Data: 191-day growing season, mid-April to end of October, cross-checked
arithmetically against the NWS figure) plus a newly-sourced 3-crop T1 basket (cherry-tomato /
apple / kale; no source for this belt was previously catalogued, requiring active UAF Cooperative
Extension Service research, same as mid-South) show TWO of three basket crops with real,
sourced, suitability-CLASS divergences, not variety-tier caveats: cherry-tomato -- three
independent UAF sources (a statewide guide, the belt's own dedicated variety list HGA-00231, and
a controlled Palmer research trial) converge that unprotected outdoor tomato culture gives
poor-to-near-zero yield here ("adjacent plots outside gave almost no yields"), requiring a high
tunnel/row cover the naive frost-anchored deriver has no way to represent; apple -- the belt's
real UAF-recommended variety list (Yellow Transparent, Pristine, William's Pride, Gravenstein,
Lodi, Tydeman's Early, Sansa, Silken, Akane) shares zero overlap with the canonical 16-variety
list, because the belt's real binding constraint is a short/cool/cloudy summer limiting ripening
time (UAF's own stated priority: "will it survive the winter, then will it fruit during the short
growing season"), a mechanism this dataset's chill-hour-based suitability logic does not model
for apple at all -- applied naively that logic would read AK's abundant chill (independently
confirmed by this dataset's own `northern_tier` z3 "chill is abundant... bloom is simply too
exposed" precedent) and wrongly default to `fruits_reliably` off the canonical list. Only kale is
directionally fine (thrives, no protection needed, matching the established
under-representation-only shape). Direct cross-reference against this dataset's own `pnw` region
(the named closest analog) sharpens the finding rather than softening it: PNW's real z8
cherry-tomato and apple treatment (full outdoor season, `fruits_reliably` off the canonical list)
is the opposite of what real UAF sources document for AK's z8 core, so AK cannot safely inherit
PNW's own numbers despite the climate-family kinship. **Ruling: NEW-REGION** -- not built here per
the design spec's scope boundaries; queued as a candidate future roadmap item (a
Ketchikan-anchored SE-Alaska-panhandle region, UAF Cooperative Extension sourced: HGA-00231, "16
Easy Steps," "Hoop Houses in Alaska," "Growing Tree Fruits in Alaska"). Full sourcing and
naive-vs-real detail: `docs/reviews/notes/2026-07-15/tier2_alaska_ruling.md`.

**With all 5 belts now ruled (4 CONDITIONAL-GO, 1 NEW-REGION), roadmap item 5's judged-belt
ruling pass is complete.** None of the 5 rulings were built in this arc, per the design spec's
explicit scope boundary (ruling-only, zero canonical touch) -- but Trevor's own read of the 4
CONDITIONAL-GO findings (2026-07-16) is that a real, sourced planting-window or suitability gap is
reason enough to queue a region candidate on its own, the same "same zone, different real climate"
precedent the `ca_interior`/`ca_north_coast`/`ca_south_coast`/`ca_desert` split already
establishes -- clearing the stricter NEW-REGION bar (a confirmed suitability-class mismatch) isn't
a precondition for that. So all 5 belts are now **full region builds**, not candidates: Alaska
(item 7, NEW-REGION), mid-Atlantic (item 8), mid-South (item 9), Nevada (item 10), Utah (item 11) --
each its own spec/plan/build arc, unsequenced relative to each other. Item 7 was spec'd 2026-07-20.

## The temperate-region resolution gap -- a PROGRAM-LEVEL prerequisite (found + corrected 2026-07-20)

**Handoff written:** `docs/kickoffs/32-plant-app-temperate-region-resolution.md` (plant-app).

**Two scope corrections, both made the day this was found** -- the second reverses a wrong claim, so
read carefully:

1. It is not Alaska-only. Reading the belts' real ZIP distributions out of `zip-zones.json`, it affects
   the z7 halves of the two largest queued belts far more than Alaska.
2. **It does NOT strand `northern_tier`, and cold-zone growers are NOT on generic dates.** The first
   write-up said the gate leaves `northern_tier` unresolved for every cold-zone user. That was wrong.
   The app has TWO resolution layers, and only one is gated on `isWarm` (see the mechanism below);
   `northern_tier` is delivered today through the other one.

The z7 ZIPs that would **upgrade** (from `northern_tier`'s generic cold-continental calendar to their
authored region-specific calendar) once the region ships AND the app fix lands:

| Belt | z8 ZIPs (standard wiring) | z7 ZIPs (need the fix) |
|---|---|---|
| Mid-Atlantic (item 8) | 1,444 | **3,131** |
| Mid-South (item 9) | 697 | ~1,900 |
| Nevada (item 10) | z8-dominant | small z7 tail |
| Utah (item 11) | **15** | small z7 tail |
| SE Alaska (item 7) | 6 (panhandle) | 22 (panhandle) |

Hand this to plant-app **in parallel with the item-8 build**, not sequenced behind anything. Note
separately that **Utah's ruled z8 core is only 15 ZIPs**, smaller than Alaska's panhandle -- worth
knowing before item 11 is scoped, since its z6-7 neighbors are the Wasatch Front, a genuinely
different climate from St. George's Dixie.

### The mechanism (two layers, only one gated)

- **Calendar resolution (`guide-calendar.ts:resolveZoneCell`) already handles cold zones.** With no
  region passed and `zone <= 7`, it resolves `northern_tier` first. So a Minnesota z5 grower gets
  `northern_tier`'s real calendar today. This layer is correct; it does NOT change.
- **Region assignment at onboarding (`zones.ts:resolveFromZip`) is gated on `isWarmZone` (zone >= 8)
  AND `region.isWarm`.** For any zone < 8 it stores no region. That is fine for a true cold-zone
  grower (the calendar layer gives them `northern_tier`) but wrong for a NEW temperate region spanning
  z7: a z7 Virginia grower never gets `mid_atlantic` assigned, so `resolveZoneCell` falls back to
  `northern_tier`'s z7 cell instead of the authored `mid_atlantic` one. The z7 data exists but is
  shadowed. The z8 half is unaffected (normal warm-path wiring).

The fix is to decouple region **assignment** from `isWarm`: assign by state + zone-span for all zones,
keep `northern_tier` out of the assignable set (it stays the silent cold default), and let `isWarm`
drive presentation only. **Once assignment sets `location.region`, the calendar layer already returns
the right cell -- no `guide-calendar.ts` change needed.** Full trace + recommended design in kickoff
#32. It is a precondition for the z7 half of items 8, 9, and 7 delivering; it blocks none of their
dataset builds.

## Empty-state ZIPs (item 2 detail)

~285 rows in zip-zones.json carry an empty state string (109 z8, 128 z9, 40 z10, 7 z11,
1 z12). State-based region matching can never fire for them, spans notwithstanding.
Owner: plant-app (regenerate or backfill the state column; check how the rows were
generated).

## Tooling follow-up: release_verify roster-wide mode

`tools/release_verify.py` section A ("collateral") assumes a single-crop pilot release
(expects only the promote-target slug to change, reference crop unchanged). A roster-wide
structural release like this widen trips both checks by design, even when sections B-H
(the substantive regression / shape / honesty checks) are clean. Add an explicit
multi-crop / roster-wide mode so section A does not raise benign concerns on structural
releases. The pre-commit backstop (`precommit_release_verify.py`) already handles the
multi-crop case correctly and remains the binding regression gate.

Second candidate: a `region_chill_delivered` <-> `EXPECTED_SPANS` zone-parity check. Today
the chill table's zone coverage is kept in step with the spans only by the widen builder at
build time, and A3 (`perennial_gate`) backstops only the chill-gated `survives_no_fruit`
tree case. If a future span grows and a chill band is missed, a non-tree or
`fruits_reliably`/`unsuitable` cell in the new zone would leave the table silently short a
band with no gate objecting. Worth an A45-adjacent parity check if the chill table becomes a
harder cross-crop requirement.
