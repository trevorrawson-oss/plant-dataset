# PLA-532: container and vertical technique sources admitted (2026-09-30)

`00dda31c -> c5fc3d13`. **Catalog only**: `source_catalog` 221 -> 229. No crop record, no crop-level
`sources` array, no existing catalog entry and no other top-level key moves. Nothing admitted is cited
by any crop yet: PLA-10 promote 2 and PLA-533's remainder do the citing, each under its own clause check.
Content, quotes and rejections: `tools/build_pla532_catalog_content.py`. Promote:
`tools/promote_pla532_technique_sources.py`; suite `tools/test_promote_pla532_technique_sources.py`;
harness `tools/mutate_pla532_technique_sources_suite.py`.

## 1. What the queued work needs (measured first, on 00dda31c)

| class | queued by | crops that need it | covered before today? |
| -- | -- | -- | -- |
| **A** trellis spacing | PLA-10 promote 2 (spec §10.2, D7) | cantaloupe, honeydew-melon, watermelon, butternut/acorn/spaghetti squash, pumpkin, zucchini-courgette, yellow-summer-squash, snow-peas, sugar-snap-peas (11) | **no**. The 6 tomatoes, 4 cucumbers and sweet-pea already have a support-conditional spacing on a cited page |
| **B** support requirement / type | PLA-10 promote 2 | melons (3), squash + pumpkin (6), peas (3) | tomatoes, cucumbers, pole beans and peas yes; **melons and squash no** |
| **C** vertical footprint, water, shading | PLA-534 (Todo; opens after promote 2) | the vining set | **no** (NC State ch. 16 neither catalogued nor cached) |
| **D** container size per crop | PLA-533 audit step 3; PLA-612 | the 102 certified crops with a non-null `min_pot_gallons` | **no** technique-scoped source |

## 2. Admitted (8), each fetched from raw bytes with urllib under two user-agents

| id | document | class | what it lets a later session cite |
| -- | -- | -- | -- |
| `umn_ext_trellises_cages` | UMN, Trellises and cages to support garden vegetables | A, B | **Trellised in-row spacing = the crop's ground spacing** ("at the same spacing ... as if they were going to grow on the ground"); larger squash and pumpkins too heavy to trellis; small melon / small winter squash (up to 3 lb) work; melons need slings; some peas need support, some don't; unsupported tomatoes 4+ ft apart |
| `vce_hort_189` | VCE HORT-189 / SPES-450, Vertical Gardening Using Trellises, Stakes, and Cages | B | **Cages** for melons and summer/winter squash; candidates pole beans, peas, cucumbers, melons, tomatoes |
| `ncsu_ext_handbook_vegetable` | NC State Extension Gardener Handbook ch. 16 | C, B | "much less ground ... yield per square foot is much greater"; dry out faster, more water; north side, shade-tolerant crops near |
| `umd_ext_containers_salad_tables` | UMD, Growing Vegetables in Containers and Salad Tables | D | per-crop minimum **volume** table (13 rows); herb groups (5 gal+ / 2-5 gal); bush-dwarf-compact rule; the continuum framing |
| `vce_426_336` | VCE 426-336, Vegetable Gardening in Containers | D | per-crop minimum **volume** + inches between plants (17 rows); 6-inch pot for chives, parsley, radish |
| `umaine_ext_2762` | UMaine Bulletin #2762 | D | per-crop **volume**, multi-plant tubs, **variety-bound** (compact cultivars named per row) |
| `psu_ext_container_vegetables` | Penn State, Container Vegetable Gardening: Four Keys to Success | D | tomato 20-inch, peppers/eggplant 14-inch (**diameter**) |
| `uvm_ext_small_spaces_budget` | UVM, Gardening in Small Spaces on a Budget | D | floor 6.5 in / 2 qt (greens, herbs); 12 in / 7-9 qt (most others) |

## 3. Rejected (7) and not found (2)

Rejected, reasons in the content module: UNR FS-00-42 (no per-crop claim, landing + full PDF read);
USU vertical gardening (generic); UW A3933-01 (redundant with UMN + VCE; its unique content is support
build spec or NC State's claim); VCE SPES-796 PDF (same publication as 426-336); UMD Growing Vegetables
in Containers (thinner sibling); UMD container index (not a document); UMD herbs indoors (no size).

**Not found in T1:** citrus container size (UF/IFAS HS57 is retired on EDIS; PLA-612 stays open); a
row spacing for trellised peas.

## 4. Decisions recorded

- **New document id, never a widened institution entry, for every institution** (umd, ncsu, umn;
  usu has nothing admitted). Widening puts a technique scope on an entry whose url is a site root, so the
  catalog still would not name the document and a fallback citation would be exactly the bare, sole
  anchor A63 fails. The convention since PLA-8 is document id beside portal id.
- **Two scouting-pass errors caught at the page:** UMD's "25 gal indeterminate tomato" is a photo caption
  (recorded in its `citable_for` as not a minimum); the UVM file's real title is "Gardening in Small
  Spaces on a Budget" (A54's defect class).
- **Unit problem for PLA-533, not solved:** UMD, VCE 426-336 and UMaine give volume; Penn State gives
  diameter only; UVM gives diameter and quarts together; VCE's indoor rows give a 6-inch pot.

## 5. Independent source-truth review (every entry, every claim)

A separate reviewer graded each `citable_for` claim against the cached page. Every figure in every table
held. It found one CONTRADICTED claim and several over-reads, all corrected before the promote:
UMaine "every row names compact cultivars" (radish and lettuce rows are not cultivar-bound); Penn State
and UVM author roles (a photo credit and a logo had been read as affiliations); UVM's "converts without a
depth assumption" (a 12-inch-diameter pot usually holds far more than 7-9 qt, so the pairing supports no
conversion, and "most other vegetables" is not a tomato minimum); UMD's continuum sentence is part of the
same photo caption as the 25 gal; UMN's same-spacing rule is stated for vine crops, and extending it to
peas is an inference; the UMN sprawl spacing is a practice, not a recommendation, and states no delta.
Added from the review: **Penn State lists sweet corn, watermelon, winter squash and zucchini as better
in-ground**, which conflicts with UMaine's and UMD's container rows. It is recorded on both entries so a
PLA-533 author sees it. All rejections held.

## 6. Proof

- Suite 51 passed. Harness 32/32 caught, 0 survived, 0 broken (positive control = whole suite green in
  scratch; sentinel on OUTPUT_SHA reddened).
- On the post-state: `gate_all` PASS 121/121 (launch-ready 114); A62 0 violations (7,063 inspected);
  A63 0 violations (30,102 inspected); A54 clean; `catalog_divergence_scan` output identical pre/post;
  `release_verify --expect-changed none` clean; `doc_roster_claim_gate` 128/121/7.
- Live-state inventory (PLA-544) re-measured on the post-state: only
  `test_problem_id_collision_gate::test_canonical_is_the_pinned_sha` reddens (its 26 count tests pass,
  so the re-pin is a confirmed re-measure); the rest green.
