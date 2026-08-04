# mid_atlantic / ncsu_ext citation hunt — apricot, cherry-sour, cherry-sweet, pomegranate

**Run:** 2026-08-03. **Pre-state canonical:** `78e5d8e3…`, HEAD `c4deea7`.
**Scope:** the 24 SOLE bare-host nodes campaign B's re-price left open
(`python3 tools/campaign_b_reprice.py`, "OPEN -- needs document work", the four `mid_atlantic` rows).
**Arc:** `docs/citation_arc_hunt_ledger.md`. **Entry doc:** `docs/kickoffs/52-campaign-b-remainder-handoff.md`.

---

## 1. What the handoff expected, and where it was wrong

Kickoff 52 §3a predicted the repoint target would be "an extension **publication**" on
`content.ces.ncsu.edu`, and warned that the Plant Toolbox (`plants.ces.ncsu.edu`) is a different
property. Both halves of that are true, and the conclusion still does not hold for three of the
four crops:

- The publication (Extension Gardener Handbook ch. 15) answers the **planting** question for
  apricot and both cherries, and nothing else about them.
- It never mentions **pomegranate at all** — 0 occurrences of "pomegranate" or "punica" in the
  whole chapter. For that crop the only NC State document that names the plant is the **Toolbox**.

So the honest split is per crop, not per region. Nine nodes repoint; fifteen stay bare with a
stated, per-crop reason. That is CASE 2 more often than CASE 1, as §3a predicted, but for reasons
the handoff did not anticipate.

**A correction to the record, both directions.** The handbook's harvest table is numbered
**Table 15–6** ("Fruit and nut harvesting guidelines"), not "Table 5". `ncsu_ext_handbook_tree_fruit`'s
`citable_for`, `mid_atlantic_nectarine_harvest_divergent` and
`mid_atlantic_mulberry_table_row_species_scoped` all call it "Table 5". The table those records
describe is the right one and every fact they quote from it re-verified; only the number is wrong.

---

## 2. Documents read — 11, of which 10 readable and 1 undetermined

Absence below is scoped to exactly this list. All fetched from **raw bytes** (`urllib` + the
`doc_mentions_crop_scan` extractor), never through a markdown table parse.

| # | document | host | verdict |
|---|---|---|---|
| 1 | Extension Gardener Handbook ch. 15, Tree Fruit and Nuts | content.ces.ncsu.edu | read, **re-verified live** |
| 2 | NC Production Guide for Smaller Orchard Plantings | content.ces.ncsu.edu | read |
| 3 | Producing Tree Fruit for Home Use | content.ces.ncsu.edu | **HTTP 403 — UNDETERMINED** |
| 4 | Plant Toolbox — *Prunus armeniaca* (apricot) | plants.ces.ncsu.edu | read |
| 5 | Plant Toolbox — *Prunus cerasus* (sour cherry) | plants.ces.ncsu.edu | read |
| 6 | Plant Toolbox — *Prunus avium* (sweet cherry) | plants.ces.ncsu.edu | read |
| 7 | Plant Toolbox — *Punica granatum* (pomegranate) | plants.ces.ncsu.edu | read |
| 8 | Cherry Trees for Fruit (Henderson County) | henderson.ces.ncsu.edu | read |
| 9 | Have You Ever Had a Pomegranate Martini? (Beaufort County) | beaufort.ces.ncsu.edu | read |
| 10 | Try a Pomegranate (Brunswick County) | brunswick.ces.ncsu.edu | read, **not usable** |
| 11 | Fruits and Berries You Can Grow (Pender County) | pender.ces.ncsu.edu | read |

**#3 is undetermined, not absent.** The same host served ch. 15, `bulb-onions` and its own index
at HTTP 200 in the same run; this one URL returns 403 to every user agent tried. Recorded per the
tamu_agrilife rule: a document that cannot be fetched is never evidence of absence.

**#10 is a `right-document-wrong-claim` trap and was NOT used.** It is a nutrition and recipe
column about buying pomegranates, and its only date sentence — "They are usually readily available
from October through December" — is about **supermarket availability of California fruit**, not
North Carolina harvest. Cited for harvest it would read as an NC State harvest window. It is not one.

### 2a. What ch. 15 actually says (re-verified against live bytes, not the catalog prose)

- **Planting, verbatim:** "The best time to plant a fruit or nut tree in North Carolina is late
  fall or early winter." Generic to fruit and nut trees; not crop-scoped.
- **Suitability, verbatim:** "Apricot and cherry trees grow in certain areas where the climate is
  favorable, but need careful management and will not consistently bear fruit." It sits directly
  after "Tree fruits not included on the lists may grow in North Carolina, but few produce quality
  fruit on a regular basis" — so apricot and cherry are explicitly *outside* Tables 15–1 and 15–2.
- **Table 15–6 rows, complete:** Apples; Chestnuts, chinquapin; Figs; Mulberry, red; Nectarines;
  Pawpaw; Peaches; Pears, Asian; Pears, European; Pecans; Persimmons, American and Asian; Plums;
  Walnut, black. **No apricot row. No cherry row. No pomegranate row.**
- **Table 15–5 (spacing)** likewise has no apricot, cherry or pomegranate row.
- **Bloom:** no bloom date for any crop, reproducing `mid_atlantic_bloom_offset_undocumented`.
  The chapter's bloom content is ordering and risk language only ("prune apple and pecan trees
  first, followed by cherry, peach, and plum trees"; bud-kill thresholds of 20–23°F before open
  bloom, 25–28°F showing color, 27–28°F at full bloom).

### 2b. What the Toolbox publishes, per crop

| crop | USDA zones | NC Region | bloom | harvest | date-bearing prose |
|---|---|---|---|---|---|
| apricot | 5a–7b | Mountains, Piedmont | Spring | Summer | **"ripens in late June to July"** |
| sour cherry | 3a–8b | *(field absent)* | Spring | Summer | "much more cold hardy than sweet cherry trees and is self-pollinating" |
| sweet cherry | 3a–8b | *(field absent)* | Spring | *(field absent)* | — |
| pomegranate | 8a–10b | Coastal | Fall, Spring, Summer | Fall | — |

Beaufort County adds the one pomegranate bloom datum anywhere in this hunt: "The bloom season is
incredibly long, **beginning in April** and lasting well into the fall", plus the zone-8 fruit-set
statement "We are right on the edge of where they can be hardy in USDA hardiness zone 8a. That
means they won't die from cold but they still may not make fruit for us here."

---

## 3. Node-by-node verdict — 9 repoint, 15 stay bare

Grouped by what each cell actually cites and claims. No reason is blanketed across crops.

### apricot — 3 repoint, 3 bare
| node | verdict | basis |
|---|---|---|
| `plantings[0]` | **CASE 1** → `ncsu_ext_handbook_tree_fruit` | chapter names apricot; planting sentence governs fruit trees generally, same basis as the 8 sibling crops |
| `plant_out[0]` | **CASE 1** → same | as above |
| `bloom[0]` | CASE 2 | no bloom date in any of the 10 readable documents; Toolbox gives the season "Spring" |
| `harvest_start[0]` | CASE 2 | **no Table 15–6 apricot row**; the Toolbox's "late June to July" *diverges* from our Jul 12 – Aug 26 |
| `harvest_end[0]` | CASE 2 | as above |
| `resolved_by_zone.8` | **CASE 1** → same | the suitability sentence is the basis for `marginal`; this cell's prose credits no institution |

### cherry-sour — 3 repoint, 3 bare
| node | verdict | basis |
|---|---|---|
| `plantings[0]` | **CASE 1** → `ncsu_ext_handbook_tree_fruit` | chapter names cherry |
| `plant_out[0]` | **CASE 1** → same | |
| `bloom[0]` | CASE 2 | no bloom date; Toolbox "Spring", "late spring" |
| `harvest_start[0]` | CASE 2 | **no Table 15–6 cherry row**; Toolbox gives the season "Summer" and no date |
| `harvest_end[0]` | CASE 2 | as above |
| `resolved_by_zone.8` | **CASE 1** → same | all three NC State attributions in this cell verified: the handbook sentence near-verbatim, "sour types are the hardier of the two" (Toolbox: "much more cold hardy than sweet cherry trees"), and self-fertility (Henderson, verbatim) |

### cherry-sweet — 2 repoint, 4 bare
| node | verdict | basis |
|---|---|---|
| `plantings[0]` | **CASE 1** → `ncsu_ext_handbook_tree_fruit` | chapter names cherry |
| `plant_out[0]` | **CASE 1** → same | |
| `bloom[0]` | CASE 2 | no bloom date |
| `harvest_start[0]` | CASE 2 | no Table 15–6 row, **and the sweet-cherry Toolbox entry has no `Display/Harvest Time` field at all** — a different absence from sour cherry's, which at least gives "Summer" |
| `harvest_end[0]` | CASE 2 | as above |
| `resolved_by_zone.8` | **HELD — deliberately not repointed** | see §4; repointing would launder an unsupported attribution |

### pomegranate — 1 repoint, 5 bare
| node | verdict | basis |
|---|---|---|
| `plantings[0]` | CASE 2 | ch. 15 **never mentions pomegranate**; the Toolbox publishes no planting model. No NC State document represents this crop's planting model |
| `plant_out[0]` | CASE 2 | no NC State pomegranate planting date exists in the 10 documents |
| `bloom[0]` | CASE 2 | Beaufort publishes a bloom **start** ("beginning in April") and a season "lasting well into the fall"; our cell is a 30-day window. The datum exists and does not match — a different situation from the other three crops, where none exists |
| `harvest_start[0]` | CASE 2 | Toolbox `Display/Harvest Time: Fall`. The **season** is supported; no dates are published |
| `harvest_end[0]` | CASE 2 | as above |
| `resolved_by_zone.8` | **CASE 1** → `ncsu_ext_toolbox_punica_granatum` (new) | `NC Region: Coastal`, USDA 8a–10b, plus Beaufort's "won't die from cold but they still may not make fruit". The cell's stated reason is humidity capping fruit quality, which is what the documents say |

**Why pomegranate's container nodes are NOT repointed at ch. 15.** Doing so would cite a document
that never names the crop for a crop-specific planting claim — the exact `vce_426_331` defect
`tools/doc_mentions_crop_scan.py` exists to catch, manufactured deliberately. The kickoff's warning
that these are two different NC State properties is what makes the distinction visible.

---

## 4. The find: cherry-sweet zone 8 credits NC State with a recommendation it does not make

`cherry-sweet.regions.mid_atlantic.resolved_by_zone.8` says, in **both** consumer registers:

> "NC State Extension steers zone 8 growers toward sour cherry instead, which tolerates this
> humidity far better."
> "NC State Extension actually points zone 8 growers toward pie (sour) cherry instead, since it
> handles the humidity much better."

Two things are wrong with the credit, and neither is the horticultural fact:

1. **The scope.** No NC State document makes a zone-8 or Coastal-Plain cherry recommendation. The
   handbook's list of crops recommended for eastern and central North Carolina contains **no
   cherry of either kind**. The only NC State steer toward sour cherry comes from Macon County in
   the far-western mountains — geography this region *explicitly excludes*, as
   `mid_atlantic_cherry_sour_marginal_ruling` itself records.
2. **The reason.** NC State's stated advantages for sour cherry are **cold hardiness** and
   **self-pollination** (Toolbox: "much more cold hardy than sweet cherry trees and is
   self-pollinating"; Henderson: self-fertile vs. needing two varieties). *Humidity tolerance* is
   ours, not theirs. Henderson names heat and humidity as why cherries generally struggle **in the
   mountains**, and says sweet cherries do worst — which is not the same claim.

The tell is the contrast with `cherry-sour`'s own zone 8 cell, which gets this exactly right: it
attributes the hardiness and self-fertility facts to NC State and leaves the humidity sentence
**unattributed** ("It also carries the belt's humidity better than sweet…"). cherry-sweet's version
moved the humidity claim *inside* the attribution and added a zone-8 scope. Same underlying content,
shifted attribution boundary — the `template-inheritance-fabricates-attributions` shape.

**Not fixed here.** It is consumer copy in both registers, so the rewrite is Trevor's call, and the
node is held bare rather than repointed so the promote does not make a wrong credit look better
sourced. Filed as `mid_atlantic_cherry_sweet_sour_steer_attribution_unsupported`, status `open`.

---

## 5. Also surfaced, filed and NOT acted on

- **`mid_atlantic_apricot_harvest_divergent`** (`open`). The one NC State statement of apricot
  ripening is "late June to July"; our window is Jul 12 – Aug 26 (z7) / Jul 5 – Aug 19 (z8). It
  reaches a month past the source on one end and excludes its start on the other. Unlike
  `mid_atlantic_nectarine_harvest_divergent`, there is **no companion row** making the overrun
  coherent — nectarine's August was defensible because the same table gave peaches "June to August"
  and nectarine is botanically a peach. Nothing plays that role here. Left unchanged pending a
  ruling; the node stays bare rather than citing a document it contradicts.
- **`mid_atlantic_apricot_coastal_plain_suitability_tension`** (`open`). The apricot Toolbox entry
  gives **USDA 5a–7b** and **NC Region: Mountains, Piedmont**. Our zone 8 (Coastal Plain) cell is
  `marginal`. Pender County, writing about southeastern NC, is blunter: apricots "are nearly
  impossible to keep alive for more than a few years because of our hot summers and erratic
  springs." That is a claim about the **plant surviving**, not about the crop fruiting — the
  `survives-no-fruit-vs-unsuitable` distinction — and it points at a stronger label than `marginal`.
- **`mid_atlantic_cherry_coastal_plain_suitability_tension`** (`open`, filed on both cherries).
  The same Pender sentence covers cherries. Filed per crop because findings live on crops, and the
  cherries' own Toolbox zones (3a–8b) do *not* share apricot's zone problem — so the reason is
  genuinely different from apricot's even though one sentence names them together.
- **`mid_atlantic_pomegranate_bloom_window_narrower_than_source`** (`open`). Beaufort publishes a
  bloom season "beginning in April and lasting well into the fall"; our cell models a 30-day
  window. The offset is not merely undocumented, it is contradicted in extent.
- **Adjacent, out of scope, not filed here:** `cherry-sour`'s **zone 7** cell makes three NC State
  attributions while citing `vce_426_331` — Virginia's home-garden **vegetable** guide, which
  contains zero mentions of cherry. That node is pathed, so it is invisible to `bare_host_scan` and
  outside this hunt's 24. It is the known 19-fruit-node `vce_426_331` problem and needs its own pass.

---

## 6. The 13 findings filed

| crop | id | status |
|---|---|---|
| apricot | `mid_atlantic_apricot_bloom_offset_undocumented` | accepted_modeled |
| apricot | `mid_atlantic_apricot_harvest_divergent` | **open** |
| apricot | `mid_atlantic_apricot_coastal_plain_suitability_tension` | **open** |
| cherry-sour | `mid_atlantic_cherry_sour_bloom_offset_undocumented` | accepted_modeled |
| cherry-sour | `mid_atlantic_cherry_sour_harvest_undocumented` | accepted_modeled |
| cherry-sour | `mid_atlantic_cherry_coastal_plain_suitability_tension` | **open** |
| cherry-sweet | `mid_atlantic_cherry_sweet_bloom_offset_undocumented` | accepted_modeled |
| cherry-sweet | `mid_atlantic_cherry_sweet_harvest_undocumented` | accepted_modeled |
| cherry-sweet | `mid_atlantic_cherry_coastal_plain_suitability_tension` | **open** |
| cherry-sweet | `mid_atlantic_cherry_sweet_sour_steer_attribution_unsupported` | **open** |
| pomegranate | `mid_atlantic_pomegranate_not_covered_by_ncsu_publications` | accepted |
| pomegranate | `mid_atlantic_pomegranate_bloom_window_narrower_than_source` | **open** |
| pomegranate | `mid_atlantic_pomegranate_harvest_season_only` | accepted_modeled |

**Three** bloom records, not four. They match the `strawberry_mid_south_bloom_offset_undocumented`
shape — a crop outside the roster ruling's set gets its own — and rest on the same ground as the
10-crop roster ruling, re-verified against live bytes. **Pomegranate has no bloom_offset record on
purpose:** a bloom datum for it *does* exist (Beaufort's "beginning in April"), so asserting absence
there would be false. It is filed as a window-extent divergence instead. That distinction is the
single clearest reason these findings were not blanketed across the four crops.

Likewise the two cherries get **separate** harvest records with different reasons — sour cherry's
Toolbox entry gives the season "Summer", sweet cherry's has no harvest field at all — and the
coastal-plain suitability tension is filed per crop rather than as one record spanning apricot and
both cherries, because apricot additionally falls outside its Toolbox zone range and the cherries
do not.

---

## 7. What this leaves for the next pass

- **6 `open` findings** need rulings, four of them consumer-facing: the cherry-sweet
  misattribution (§4), the apricot harvest divergence, and the three suitability tensions.
- **15 nodes remain on the bare host by design.** They are not residue; `bare_host_scan` will keep
  reporting them, and each now carries a filed reason for why repointing them would be wrong.
- **`producing-tree-fruit-for-home-use` is still unread** (HTTP 403). If it becomes reachable it is
  the one NC State publication that might carry apricot or cherry planting detail this hunt could
  not obtain.
- Campaign B's other two decisions are untouched by this pass: `fig`/`mid_south` (2 harvest nodes)
  and `strawberry`/`mid_south` (the z8 `plant_out` arm).
