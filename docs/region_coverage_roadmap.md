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
| 2 | App-side cleanup: ~285 empty-state ZIP rows in zip-zones.json; verify the regions.json sync path end to end; decide TX z10 ZIP3 fencing (keep RGV on the se_gulf interim vs fence to generic until item 3) | plant-app | QUEUED (next) | ~285 ZIPs broken regardless of spans until fixed |
| 3 | Rio Grande Valley / subtropical TX region (new authored region; TAMU AgriLife RGV calendars are strong T1) | dataset | QUEUED | 95 ZIPs off the se_gulf interim |
| 4 | Maritime PNW region (WA/OR z8-9; WSU/OSU extension T1) | dataset | QUEUED | ~750 ZIPs; generic frost-anchored dates most misleading here (cool summers) |
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

## The RGV interim ruling (Trevor-approved 2026-07-12)

Widening se_gulf to z10 auto-matches the 95 TX Rio Grande Valley z10 ZIPs (TX is in the
app's se_gulf state mapping). This ships as an EXPLICITLY INTERIM answer: Gulf-coast
winter-garden dates are directionally right for RGV and better than a bare zone label,
and se_gulf's source set already includes tamu_agrilife. Item 3 replaces it with a real
RGV region; item 2 may instead fence TX z10 via ZIP3 hints if the app side prefers
generic dates meanwhile.

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
