# findings_leek.md -- PLA-8 batch 24, leek, 2026-09-03

## 1. The brief's white-rot figure is NOT in the record (re-verified, not acted on)
The authoring brief said the record gives "one sclerotium per about 20 pounds of soil" and that the
figure is in the record. It is not. `leek_source.json` (and the byte-identical r4 candidate) says:
"even a few sclerotia per soil sample can start the disease." `grep "20 pounds"` over the leek record
returns nothing, and no white-rot record on the roster carries a pounds figure. The notes therefore
say "a few of them in a sample of soil" / "even a few per soil sample", which is the record's claim.
If the 20-pound figure is meant to be authoritative it belongs in the RECORD first (with its source),
and the white-rot rungs re-derived from it afterward; a rung must not carry a figure the record lacks.

## 2. Claims in the record with no reachable method (left in the record, not forced)
- **Onion thrips, straw mulch.** "straw mulch on the bed deters thrips" (management_seasoned) and
  "a straw mulch on the bed helps hold numbers down" (management_beginner). `straw_mulch` applies_to
  is `['fungal_foliar', 'disease_general']`; it does not reach `insect`. Catalog gap: the catalog's
  straw mulch is the strawberry fruit-contact barrier, not a thrips deterrent.
- **Onion thrips, even watering / vigor.** "keep plants evenly watered: vigor buys tolerance of the
  feeding, not fewer thrips". `even_watering` applies_to is `['physiological', 'mite', 'bacterial']`;
  no insect target. The vigor-as-tolerance framing IS carried in the balance_nitrogen rung (nitrogen
  adequacy is the record's other half of vigor), but the watering instruction itself is not laddered.
- **Pink root, steady water and fertility.** "keep plants vigorous with steady water and fertility,
  since weak roots are the ones it takes". `even_watering` does not reach `fungal`. The
  weak-roots-are-taken mechanism is carried in the improve_drainage rung; the watering and feeding
  instruction is not.
- **Leek moth, pheromone trap.** "A pheromone trap set by mid-April shows when each flight peaks."
  There is no general pheromone-monitoring method in the catalog (`codling_moth_pheromone_trap` and
  `swd_monitoring_traps` are crop-specific). The trap is mentioned INSIDE the spinosad rung as the
  timing signal the record ties it to, since the spray is timed 7 to 10 days after a peak flight;
  it has no rung of its own. Catalog gap worth a general `pheromone_monitoring_trap` entry if this
  recurs (it will, on any moth with published flight peaks).
- **White rot, crop_rotation.** The record says only that rotation alone will not control it
  (sclerotia persist over 20 years). No duration, no positive instruction, so no rung; the caveat is
  carried inside certified_clean_stock and garden_sanitation. Orchestrator may prefer a rung; if so
  it should be written as "rotate, but treat it as a supplement", and the record should carry a
  positive rotation sentence before that is done.

## 3. Judgment calls the orchestrator should see
- **Thrips: siting away from small grains, alfalfa, clover** is placed in `weed_host_control` on the
  mechanism the record gives (those plantings SHED thrips onto the crop when they dry down or are cut,
  exactly what the weedy-edge claim describes). Those are host CROPS, not weeds, so it is a stretch of
  the method's name though not of its mechanism ("weedy alternate hosts are a reservoir"). The
  alternative is a catalog gap ("site away from alternate-host crops"). Flagged rather than hidden.
- **Leek moth: handpick vs garden_sanitation.** The brief folded "remove larvae and cocoons" into
  garden_sanitation. It is placed under `handpick` (the catalog's "physically removing larvae ... on a
  regular scouting schedule") and garden_sanitation is kept to the end-of-season debris claim, so the
  two rungs do not repeat one claim. Easy to collapse if the orchestrator wants 5 rungs.
- **planting_time_avoidance** reaches `insect` (`insect_chewing`, `insect_boring`) and the record
  supports it on three pests: leek moth ("delay planting past the first emergence where the season
  allows"), onion maggot ("planting later in spring, once the first flight has passed"), allium leaf
  miner ("transplanting after mid-May and harvesting by early September can dodge both flights").
  The catalog caution (confirm emergence locally) is carried in both registers each time.
- **Leek rust: volunteers** are under `garden_sanitation` per the brief (the catalog lists "volunteer
  hosts" in that method's mechanism). garlic's shipped rust ladder put volunteers under
  `weed_host_control`; the two crops now split the same claim across two methods. Not a defect, but
  a divergence a future family pass may want to reconcile.

## 4. Pins the promote will need re-set for this file
- `EXPECTED_RUNGS["leek"]`: 18 -> **29** (thrips 5, leek moth 6, maggot 4, leaf miner 5, rust 5,
  white rot 2, pink root 2). `TOTAL_RUNGS` follows.
- `EXPECTED_TEMP_FIGURES` (batch-wide, pinned 3): leek alone contributes **6** hits (50°F x4 on leek
  moth planting_time_avoidance and floating_row_cover, both registers; 75°F and 59°F on leek rust
  airflow_spacing seasoned). All six are in the record; the validator confirms each.

## 5. Validator
`python3 tools/staging/pla8_batch24_alliums/validate_out.py leek <r4_candidate>`:
precedent scan 15 + 6279 comparisons, worst 0.578 (A: leek/onion-maggot/floating_row_cover vs
spring-onion), 29 rungs across 7 problems, RESULT: PASS. The validator on disk was patched
mid-session to scope `DECLARED_IDENTITIES` per crop; before that patch a leek-only run refused on
onion's water_spray identity, which was the validator's shape, not this file's.

## 6. Doubts
- The record's leek-moth range statement ("so far confined to northern New York and northern New
  England") is not carried into any rung; a rung tells the reader what to do, and that sentence is
  where-it-is context. It stays in cause_*.
- The thrips beneficial_predators seasoned note says predators "lag a fast-building population";
  that sentence rests on the METHOD's catalog cons, not the leek record. Method text is allowed, but
  it is the one sentence in the file whose support is the catalog alone.
