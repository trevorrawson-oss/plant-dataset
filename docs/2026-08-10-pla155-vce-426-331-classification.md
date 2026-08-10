# PLA-155 -- vce_426_331: every citing claim, classified (2026-08-10)

Base canonical `ce9eb12f` (post PLA-156; the issue's `72284f02` base moved twice same-day, as its
kickoff anticipated). Document read IN FULL from cache
(`tools/.doc_cache/bf50eb4680df343e1b05546afb99d8359fc65fee.txt`, 43KB, pub date May 30 2025).

## What the document actually is

*Virginia's Home Garden Vegetable Planting Guide: Recommended Planting Dates and Amounts to Plant*
(426-331 / SPES-673P). Contents, exhaustively:

- **Table 1**: last-spring / first-fall frost date ranges for zones 6a-8b. **Zone-scoped, not
  crop-scoped** -- it legitimately anchors ANY frost-resolved claim in this belt.
- **Tables 2-4**: recommended PLANTING date ranges by crop, per zone half (6a/6b, 7a/7b, 8a/8b),
  spring + fall columns. **39 vegetable rows** (Asparagus, Beans lima/pole/snap, Beets, Broccoli,
  Brussels sprouts, Cabbage, Cabbage Chinese, Carrots, Cauliflower, Chard, Collards+kale,
  Corn sweet, Cucumbers, Eggplant, Garlic, Kohlrabi, Leeks, Lettuce baby/head, Muskmelon, Mustard,
  Okra, Onion bulbing, Peas garden, Peas southern, Peppers, Potatoes, Pumpkin, Radish, Rutabaga,
  Spinach, Squash summer/winter, Sweet potato, Tomatoes, Turnips, Watermelon; Table 5 adds
  Beans bush).
- **Table 5**: spacing / amounts / plantings-per-season.
- **NO harvest dates anywhere.** The section heading says "Planting and Harvest Dates"; the tables
  publish planting dates only ([[harvest-start-is-not-a-published-datum]] confirmed for this doc).
- No herbs, no ornamentals, no berries, no fruit trees, no shallot, no arugula, no soybean/edamame,
  no corn other than sweet.

## Footprint

1,281 raw occurrences in canonical = 670 `sources` list elements + 575 `anchoring_urls` keys +
29 `sources_summary` id strings + 6 embedded in finding prose. Collapsed: **657 claim nodes across
86 crops**, almost all mid_atlantic; small northern_tier + legacy `zones{}` + edamame crop-level
footprints. Full per-crop matrix in the session scratchpad; reproduce with the walk in this doc's
companion promote test.

## Classification (by claim, per [[never-blanket-a-reason-across-crops]])

### SUPPORTED -- the overwhelming majority
1. **~55 in-document vegetables** (tomatoes x5, cucumbers x4, squash x6, brassicas, roots, greens,
   melons, beans, garden peas incl. snow/sugar-snap [Pisum sativum -- the deliberately pinned
   "peas" match], alliums, potato, sweet-potato, okra, corn sweet): `plant_out` and
   `second_planting` values spot-checked EXACT against the 7a/8a rows (z7<-7a, z8<-8a convention;
   narrower-than-source windows appear only as conservative truncation, e.g. cucumber spring).
   `start_indoors` and `harvest_*` arms are the region contract's DECLARED derivation
   (offsets off plant_out -- `docs/mid_atlantic_cell_contract.md`), the same convention every
   frost-anchored region uses.
2. **Declared in-cell borrows, honest taxonomic distance**: shallot (follows Onion bulbing row --
   same species, declared in cell notes), arugula (Mustard row, same family, declared),
   bok-choy (= the doc's "Cabbage, Chinese" row, values exact), popcorn/field-corn/flint-corn
   (Corn sweet row, same species, declared in cell notes with the frost-capped harvest reasoning;
   DTM bands are Trevor-ratified per their own cert logs -- NOT touched, per
   [[cert-log-already-adjudicated-the-band]]).
3. **Frost-anchor citations on perennials** (thyme, rosemary, oregano, sage, lavender; apricot,
   cherries, pomegranate and the other tree cells): the cells' synthesis notes declare
   "plant_out is frost-resolved from the last spring frost (Apr 15 / Apr 8)" -- exactly Table 1's
   zone data, which is crop-independent. The tree crops' modeled bloom/harvest offsets carry their
   own accepted_modeled findings from the 2026-08-03 NCSU hunt. Right document, right claim.
4. **Citrus mid_atlantic cells** (lemon, lime, orange, mandarin, grapefruit): all-null timing
   values; vce rides in the region source list. Vacuous, PLA-195 block (b) territory; untouched.

### CONFIRMED DEFECTS (fixed in the companion promote)
5. **sweet-pea mid_atlantic z7/z8** (3 nodes, all SOLE): the issue's headline. Zero
   "sweet pea"/"Lathyrus" in the doc; timing openly declared in cell notes as the Peas-garden
   analog (crop is Lathyrus odoratus, `companion_and_ornamental_flower`). One correction to the
   issue's framing, per [[cert-log-already-adjudicated-the-band]]: sweet-pea's Trevor-ruled cert +
   `sweet-pea_pilot_finding_001` already declare ALL regional windows MODELED ("the catalogued T1
   sweet-pea pages do not publish region-by-region dated planting charts"), and the harvest window
   is NOT a wrong value -- Apr 13/May 14 = start_indoors + 85 days, the crop's OWN certified mid
   days-to-bloom for the indoor-started cohort. The defect is the CREDIT: a vegetable guide as
   sole source for an ornamental. Fix: add `ncsu_ext` (Lathyrus odoratus Plant Toolbox page,
   cached, 33 lathyrus mentions -- carries the biology claims) beside the declared analog, and
   register the analog as an accepted_modeled finding so classifiers see what the prose declares.
6. **strawberry mid_atlantic z7 + 4 rule-layer arms + region list** (SOLE): WRONG PUB NUMBER, the
   [[template-inheritance-fabricates-attributions]] shape in prose -- synthesis notes credit
   "VCE 426-331 home garden matted-row guidance", matted-row/renovation content 426-331 does not
   contain. VCE **426-840** (*Small Fruit in the Home Garden*, fetched live 2026-08-10) DOES:
   matted-row system, renovation (mow to 1 inch of crowns soon after harvest), blossoms
   "easily killed by frost", "dormant crowns in early spring, about three or four weeks before
   the average date of the last frost". Fix: mint `vce_426_840`, repoint id + 4 synthesis-note
   pub-number strings. Residual divergences FILED OPEN, values not moved: our z7 plant window
   opens ~2 weeks pre-frost vs the doc's "three or four"; the 6-weeks-to-ripen / 4-week-flush
   offsets are unpublished (modeled).
7. **blueberry / raspberry / blackberry mid_atlantic** (3 nodes each, non-SOLE): vce_426_331 as
   ride-along credit on crops it never mentions. 426-840 covers all three with planting-season
   statements (blueberry "early spring about three or four weeks before the average date of the
   last frost"; caneberries "late fall or early in spring, about four weeks before"). Fix: swap
   credit to `vce_426_840`. The NCSU pathed anchors (home blueberry guide; SE caneberry guide)
   stay.
8. **elderberry mid_atlantic** (3 nodes, non-SOLE): read-confirmed absence -- 0 occurrences in
   426-331 AND 0 in 426-840. The mid_atlantic twin of the DECLARED mid_south finding
   (`mid_south_elderberry_no_uaex_planting_model`), except nothing declared it here. Fix: remove
   the false vce credit (cells stay on institution-root `ncsu_ext`, mirroring the accepted
   mid_south state) + the mirroring accepted_modeled finding.
9. **edamame crop-level** (6 nodes + 2 anchoring keys + source_set): the id names 426-331 while
   two anchoring entries -- and the CONTENT of every claim -- belong to VCE **SPES-455**
   (*Edamame in Virginia II: Producing a High-Quality Product*, fetched live 2026-08-10:
   Bradyrhizobium japonicum inoculant quote, 7-10 day harvest window, low-N guidance all
   verified). A catalog-identity divergence, not a fabrication. Fix: mint `vce_spes_455`,
   repoint all 6 nodes + anchoring + source_set. (The variety-latitude claim is NOT in SPES-455;
   it rides the co-cited mu_ext/cornell_ext. Our "four to ten days" pod window brackets SPES-455's
   "seven to 10"; co-cited mu_ext carries the wider figure.)

### PRESENT BUT DIFFERENT VALUE -- recorded, NOT fixed here (scope)
10. **northern_tier tomatoes x5 + lettuce-leaf** (~28 nodes, non-SOLE, legacy 5-source piles):
    e.g. cherry-tomato nt z6 `plant_out Apr 8 - Apr 22` vs the doc's 6a tomato row
    May 10 - June 10; lettuce nt z6 Mar 8 - Mar 29 vs Apr 10 - June 1. vce does not support these
    values. This is PLA-195 block (d) (explicitly NOT absorbed into PLA-155); recorded there.
    Legacy `zones{}` subtree citations: ruled LEAVE ([[legacy-zones-subtree-is-ruled-leave]]).

### ANOMALY (fixed as part of #9)
11. edamame `fertilizer`/`varieties` anchoring entries keyed `vce_426_331` pointing at the
    spes-455 URL -- the divergence that exposed #9.

## The absorbed PLA-195 blocks

**(a) RGV ornamental block -- NO DATA DEFECT.** All 14 footprint decisions (basil, bee-balm,
borage, calendula, cosmos, echinacea, lemongrass, marigold, nasturtium, sunflower, sweet-alyssum,
sweet-pea, viola, zinnia; rgv, bare=tamu_agrilife) DECLARE their modeling in region prose:
"X is not covered in either TAMU AgriLife RGV vegetable planting table... this cell is
CONSERVATIVE... not a crop-specific TAMU-stated date." This is
[[adjudication-vocabulary-outruns-the-test]]: the footprint classifier scans findings, prose
declarations are invisible to it. Partner anchors are right-taxon pathed documents (bee-balm ->
NCSU *Monarda didyma* Plant Toolbox, 57 monarda mentions, cached; cosmos -> UC IPM
home-and-landscape cosmos page -- a PLANT page on the IPM domain, not a pest page -- plus UF/IFAS
cosmos; viola -> Clemson pansies factsheet) carrying the biology claims the prose attributes to
them. The instrument gap (classifier should read cell/region prose declarations) belongs to
PLA-138. **(c) elderberry**: fixed here, #8.

## Term-collision crops (original issue item 2)

- **bee-balm**: its own anchors resolve to *Monarda* pages -- right taxon. The `balm` -> *Melissa
  officinalis* collision is scanner vocabulary (PLA-138), not a data defect.
- **lime**: its anchors are uniformly CITRUS documents (ASPCA lime, Clemson citrus cold-tolerance,
  TAMU citrus, UC IPM citrus, UCD postharvest lime, UF/IFAS). The soil-lime collision is scanner
  vocabulary. Citrus suitability credit cells remain PLA-195 (b).
- **sage**: mid_atlantic + rgv cells read -- frost-anchored / prose-declared, NCSU-anchored. The
  *Artemisia* collision is scanner vocabulary.
- **popcorn**: read -- declared same-species borrow, values exact against the Corn-sweet rows,
  harvest frost-cap reasoned in the cell notes. No defect (and its DTM band is ratified;
  see PLA-156).

## Instrument notes handed to PLA-138 (NOT built here, per the issue's standing constraint)

- `doc_mentions_crop_scan` display-name term derivation (sweet-pea -> `pea`) -- already PLA-138 §7.
- The scan that produced the 377-node ornamental lead list missed vce_426_331 entirely because
  `source_catalog` has no titles (see the title-field decision spec, same date).
- The PLA-187 footprint classifier treats prose-declared cells as NEITHER (this session's RGV
  finding).
- `cited_claim_scan`-style absence discipline held: every absence above is scoped to the documents
  read on 2026-08-10 (426-331 cached; 426-840 + SPES-455 live-fetched, now cached).
