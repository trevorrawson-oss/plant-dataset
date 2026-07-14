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
| 2 | App-side cleanup: ~285 empty-state ZIP rows in zip-zones.json; verify the regions.json sync path end to end; fence ZIP3 785xx to the new `rgv` region (item 3 shipped below; paired app-side kickoff `docs/kickoffs/26-rgv-plant-app-zip3-fence.md`) | plant-app | QUEUED (next) | ~285 ZIPs broken regardless of spans until fixed; 785xx fence is what actually resolves RGV ZIPs to `rgv` in-app |
| 3 | Rio Grande Valley / subtropical TX region (new authored region; TAMU AgriLife RGV calendars are strong T1) | dataset | **SHIPPED 2026-07-13** (canonical `d0832254`) | 95 TX z10 ZIPs off the se_gulf interim; app-side 785xx ZIP3 fence is the paired follow-up (item 2 / kickoff #26) |
| 4 | Maritime PNW region (WA/OR z8-9; WSU/OSU extension T1) | dataset | **SHIPPED 2026-07-14** (canonical `8dd4ac4c`) | ~750 ZIPs off generic frost-anchored dates; app-side west-side ZIP3 fence is the paired follow-up (kickoff #28) |
| 5 | Judged later, each needs an explicit ruling: mid-Atlantic z8 belt (NC 793 / VA 258 / MD 117 / DC 215 / DE-NJ-PA small), mid-South (AR 460 / OK 106 / TN 123 / MO 6), NV (110) / UT (15) / AK (13) | dataset | OPEN | GENERIC-OK is a legitimate ruling where honest |
| 6 | Puerto Rico (2 z11 / 47 z12 / 126 z13) | product call (Trevor) | OPEN | market-scope question first; also needs z12/13 support end to end |

Items 3+ are their own arcs (spec -> plan -> build). Nothing below item 2 blocks item 2.

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
not silence. First reads (each to be confirmed in its own pass): maritime PNW = NOT ok
(cool summers invert the assumptions; item 4). Mid-Atlantic z8 = probably ok (humid
continental-lite; generic frost anchoring is close). Mid-South z8 = probably ok. NV/UT
z8-9 = probably ok (warm_arid adjacency worth a look). AK z8 (13 ZIPs, maritime) =
probably ok at this scale.

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
