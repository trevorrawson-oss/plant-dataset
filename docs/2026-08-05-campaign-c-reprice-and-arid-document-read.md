# Campaign C — the re-price, and the four documents it made cheap to read

**Session:** 2026-08-05. **Issue:** PLA-113. **Kickoff:** `docs/kickoffs/53-campaign-c-arid-and-texas.md`.
**Canonical at start:** `5a52a76c` (kickoff was written against `4065e23b`). **Suite:** 650 passed.
**PROMOTED 2026-08-05**: `5a52a76c` -> `754c51a0`, one promote, via
`tools/promote_campaign_c_closeout.py` (13 guards, all mutation-tested; 27 tests). Sections 1 to 4
below were written before the promote and describe the pre-state; section 5 records what shipped.

---

## 1. The kickoff's shape numbers all reproduce. Its adjudication test does not.

Every measured claim in kickoff 53 §3 reproduces byte-for-byte on the newer canonical:
116 SOLE nodes, 35 decisions, 7 hunts, 82 containers vs 34 claim arms, lemon 16 + lime 15 = 31
nodes, the 8 both-host `warm_arid` crops, and one bare URL per decision. The USCRN promote moved
nothing in this footprint. **Re-verified, not inherited.**

One claim reproduces and is still the wrong question:

> "Measured 2026-08-04: **0 of 35 decisions carry any finding naming their region.** Nothing here
> is pre-ruled ... C's 35 is real work."

The measurement is correct — `python3 tools/campaign_c_reprice.py` reproduces `0 of 35` and a test
pins it. But campaign C's crops **do not declare their bare anchors by region. They declare them by
SOURCE ID**, in a crop-scoped pilot finding filed at certification:

    okra_pilot_region_anchor_base_urls [accepted]
      "Several region-rep source anchors (umn_ext, umaine_ext, ucanr_ext, uc_mg, nmsu_ext,
       tamu_agrilife, uariz_ext, uf_ifas_vh021, uhawaii_ctahr) use the institution/publication
       BASE URL rather than a live okra-specific page..."

That one finding names three of campaign C's five source ids and adjudicates three of its
decisions. Grepping for `warm_arid` would never find it.

**Measured: 17 of 35 decisions carry a finding naming the hunt's own source id.** This is the
[[stale-records-commission-phantom-work]] shape inverted — not a stale record commissioning work
already done, but a too-narrow TEST hiding adjudication that was already filed.

### The re-price

`tools/campaign_c_reprice.py` (new, 27 tests, every check mutation-tested):

| verdict | decisions | nodes | |
|---|---|---|---|
| CATALOG-REPOINTABLE | 1 | 1 | carrot — the catalog already names the document |
| DECLARED-ANCHOR | 17 | 38 | a finding on that crop names that source id |
| MODELED-ONLY | 6 | 20 | windows declared derived; the anchor id is not adjudicated |
| OPEN | 11 | 57 | of which 5 decisions / 31 nodes are lemon+lime |

After the §4a citrus re-scope: **campaign C keeps 30 decisions / 85 nodes, of which 6 decisions /
26 nodes were honestly open.** Campaign D takes 5 decisions / 31 nodes.

The six open: `broad-beans-fava`, `garlic`, `shallot`, `snow-peas`, `sugar-snap-peas` (all hunt
#13, `rgv`/`tamu_agrilife`) and `beefsteak-tomato` (#17). **Five of six are one hunt** — so campaign
C's remaining document work was one RGV document read plus one node.

**Why the ALIAS check is load-bearing, not decoration.** Half the anchor findings name the
institution in prose ("nmsu, tamu") rather than the catalog id. `"nmsu"` covers `nmsu_ext` only
when `nmsu_ext` is the sole nmsu-family id that crop cites, so the tool checks that against the
data and refuses the match otherwise. It refuses three times, and each refusal is correct:

- `snow-peas` / `sugar-snap-peas` / `broad-beans-fava` cite **both** `tamu_agrilife` and
  `tamu_agrilife_fall_veg`, and their findings name only the `_fall_veg` PDF — whose catalog
  `citable_for` is, verbatim, "**broccoli** Texas fall planting window".
- `beefsteak-tomato` / `heirloom-tomato` cite both `nmsu_ext` and `nmsu_donaana_mg`; hunt #17 is
  the Dona Ana one and heirloom's finding says only "NMSU".
- `shallot`'s only tamu finding is `shallot_pink_root_tamu_pdf` — a DISEASE anchor. Right
  institution, wrong claim ([[right-document-wrong-claim]]).

---

## 2. A defect class no existing scan can see: node URL vs catalog URL

Hunt #24 is one node, and the ledger guessed it might be "a mis-classification rather than a real
bare host". It is neither. It is a **wrong-institution citation**:

    carrot.regions.warm_arid.resolved_by_zone.8            source id `nmsu_chart`
    carrot.regions.warm_arid.resolved_by_zone.8.heat_pause   url  https://desert.tamu.edu/

`nmsu_chart`'s catalog URL is `https://donaanamastergardeners.nmsu.edu/documents/foodgardenplantingchart-1.pdf`
— a real, pathed, T1 PDF. So a source id named for **New Mexico** State carries, on these two
nodes, a bare **Texas** A&M host. The node's own prose credits "(NMSU Dona Ana Master Gardeners;
agronomics from NMSU Circular 457-B)" and its `resolution_method` is `nmsu_dona_ana_month_resolution`.
Carrot's *other* nodes cite `nmsu_chart` at the correct PDF. This is a transcription defect, not a
second document.

`nmsu_chart` turns out to carry **three different URLs across 15 nodes and 5 crops**: the correct
PDF (12 nodes), `desert.tamu.edu` (2), and `lowwaterplants.nmsu.edu/herbaceous.html` on lavender (1)
— an NMSU low-water **ornamental** page standing in for a food-garden planting chart.

**Measured roster-wide**, comparing every `anchoring_urls[sid].url` against `source_catalog[sid].url`:

| class | entries | |
|---|---|---|
| same site, different path | 21,340 | normal: the catalog is a root, the node names a document |
| identical | 7,320 | |
| different registrable domain | 729 | **floods** — `cameron.agrilife.org`, `txmg.org`, `nevegetable.org` etc. are legitimate |
| **node BARE while catalog is PATHED** | **10** | the real signal |

The narrowed check is the one that pays: **10 nodes over 3 source ids** — carrot's 2, seven turnip
nodes citing bare `mastergardenersd.org` under `ucanr_san_diego_mg` (whose siblings cite pathed
pages on that same host), and one `edamame:varieties` node. `bare_host_scan` cannot see this class
(it does not consult the catalog) and `url_health_gate` cannot (they all return 200). The broad
"different domain" version is exactly the [[gate-findings-must-be-read-not-counted]] flood; narrow
the CHECK, not its scope.

**Recommend:** ship this as a scan (`tools/catalog_divergence_scan.py`) at the narrow definition.
Not built this session — the three hits are already enumerated above and two are outside campaign C.

---

## 3. The RGV document, read: hunt #13 is CASE 2 for all six crops

`tools/.doc_cache` held the RGV guide as a cached **HTTP 403**, and both scans read that as absence
([[waf-block-pages-cached-as-absence]]). Retrieved this session and parsed with pypdf: 5 pages,
11,097 characters of real text.

**`https://cameron.agrilife.org/files/2022/05/RGV-Homeowner-Vegetable-Guide-2022.pdf`** — cited on
**468 nodes** dataset-wide and by **51 crops inside `regions.rgv`**. Its roster is ~25 crops:
green bean (bush/pole), sweet corn, pepper, potato, tomato, cantaloupe, zucchini, butternut squash,
broccoli, cabbage, collards, cauliflower, kale, kohlrabi, spinach, swiss chard, beets, carrot,
turnip, cowpeas, cilantro, dill, onion (bulbing/bunching), leek, sweet potato.

    arugula  ZERO      fava/broad bean  ZERO      garlic  ZERO
    shallot  ZERO      snow pea         ZERO      sugar snap  ZERO

Its only pea is **Cowpeas** (*Vigna unguiculata*) — a warm-season southern pea, a different genus
from *Pisum sativum*. Citing it for snow-pea timing would be [[match-the-taxon-not-the-common-name]].

**This is the [[sibling-precedent-pressures-a-wrong-repoint]] shape at 51:6.** Fifty-one RGV crops
cite this document; the pressure to make the remaining six match it is exactly the pressure to be
wrong. In `regions.rgv` the 23 crops on the bare host are otherwise all herbs and flowers — the
only vegetables among them are precisely hunt #13's six, because they are precisely the six the
guide omits.

### Two further RGV documents read, and what they do and do not cover

| document | host | garlic | shallot | peas | fava | arugula |
|---|---|---|---|---|---|---|
| Vegetable Crops of the Lower Rio Grande Valley | `texaslocalproduce.tamu.edu` | — | — | "Peas (sweet)" 9-1 thru 9-30, 70-80 d | — | — |
| Vegetable Gardens for the RGV, Fall/Cool Season | `txmg.org/cameron` | **Oct thru mid-Nov, 90-120 d** | — | "Peas (sweet)" October | — | — |

Page 1 of the second failed pypdf's font parse and was recovered from the raw content stream — its
crop list begins at "Beans", so **arugula's absence is measured, not assumed**. That document also
names its own primary source: *Vegetable Crops of the Lower Rio Grande Valley* — the first row of
this table. It is a county Master Gardener derivative, and `txmg.org` holds **no `source_catalog`
id**, so citing it is a source-admission decision ([[source-catalog-is-the-admission-authority]]).

### The six crops already say all of this, in their own prose

Every one of the six declares the absence on its `plantings[0].plant_out[0]` arm, verbatim:

- arugula — "No RGV-specific table row exists for arugula"
- broad-beans-fava — "No RGV table row exists for fava beans"
- garlic — "No RGV-specific table row exists for garlic"
- shallot — "No RGV-specific table row exists for shallots"
- snow-peas — "No RGV-specific table row names snow peas"
- sugar-snap-peas — "No RGV-specific table row names sugar snap peas"

**Measured: 6 of 116 campaign C nodes carry such an in-cell declaration, and all six are these.**
The document read confirms every one of them is TRUE. So this is a **third adjudication vocabulary**
the arc has not been checking: campaign B looked for findings; the re-price looks for findings
naming a source id; these six declare it in the cell's own `synthesis_note_seasoned`, where no scan
looks. The determination was made at authoring time and never reached the findings ledger.

**So hunt #13 needs no document hunt. It needs the six existing in-cell declarations promoted into
filed CASE 2 findings**, so the arc's tooling can see what the data already says.

**The garlic exception, and it is not a blanket** ([[never-blanket-a-reason-across-crops]]): garlic
is the one crop with a real row, in the county MG guide — plant Oct thru mid-Nov, harvest 90-120
days later. The dataset says plant Oct 15 - Nov 15 (bracketed by the document, fine) and harvest
**180-210 days** later. Bulbing garlic in a mild-winter climate takes roughly six to eight months;
90-120 days is not a bulbing-garlic figure. **Recommend NOT repointing garlic's harvest at it** —
that would swap a sound derivation for a weaker uncatalogued source that contradicts it, which is
kickoff 53 §6 lesson 5. Garlic's plant_out could be repointed on its own; its harvest should stay
declared.

---

## 4. Hunts #17 and #24: one chart, read visually, closes both

Both tomatoes' `warm_arid` z8 `basis_seasoned` names its document in prose: "**Dona Ana County
Master Gardener Las Cruces planting chart**". That is the same document `nmsu_chart` already holds
a catalog URL for — the one carrot's node is supposed to be citing. **One read closes #17 and #24.**

The chart's text layer holds crop names and month headers and **no dates whatsoever**: the windows
are drawn as graphical bars. This is the AZ1005 trap in a second document, and text extraction here
yields not a rotated grid but an empty one. Read visually instead:

| crop | chart (Las Cruces, NM) | dataset `warm_arid` z8 | |
|---|---|---|---|
| Carrots | bar mid-Jan thru Feb; second bar Aug thru early Sept | `plant_out "Jan - Feb, Aug"`, first Jan 15, last Aug 31 | **matches** |
| Tomatoes | start ~Jan-Feb → transplant Mar thru early Apr; second start ~Jun → transplant mid-Jul thru early Aug | `start_indoors Feb 5-19`, `plant_out Mar 19 - Apr 8`; second `Jun 3-17` / `Jul 15 - Aug 4` | **matches** |

Both claims are **corroborated by the document their own prose names**. #24 is a mechanical URL
correction; #17 is a repoint of two container nodes at a chart already in the catalog.

Provenance note for the promote: the chart is **© Darrol Shillingburg**, hosted by the Doña Ana
County Master Gardeners. It is catalogued T1 as `nmsu_chart` already; that admission is not being
re-opened here, only observed.

The chart also carries Garlic, Shallots, Peas and Beans-Fava rows — **for Las Cruces, New Mexico**.
Those cannot source hunt #13, which is the Rio Grande Valley of **Texas**. Same crops, different
region, and the ledger's own standing caution about a UC table sourcing an Arizona window applies
unchanged.

---

## 5. Where campaign C stands

| hunt | decisions | state after this session |
|---|---|---|
| #7 `warm_arid`/`nmsu_ext` | 9 | 8 DECLARED-ANCHOR; **pumpkin** is MODELED-ONLY (no anchor finding) |
| #8 `warm_arid`/`tamu_agrilife` | 9 | 7 DECLARED-ANCHOR; pumpkin MODELED-ONLY; lemon → campaign D |
| #13 `rgv`/`tamu_agrilife` | 6 | **document read, CASE 2 proven for all six**; arugula already DECLARED |
| #14 `low_desert_az`/`uariz_ext` | 6 | okra DECLARED; cantaloupe/honeydew/watermelon MODELED-ONLY; lemon+lime → D |
| #17 `warm_arid`/`nmsu_donaana_mg` | 2 | **repointable at the Dona Ana chart, claims verified** |
| #21 `ca_desert`/`uariz_ext` | 2 | 100% citrus → campaign D |
| #24 `warm_arid`/`nmsu_chart` | 1 | **wrong-institution URL, repoint verified** |

**No document hunt remains in campaign C.** What remained was authoring, and it SHIPPED on
2026-08-05 as `5a52a76c` -> `754c51a0`. What landed, against the list below:

1. **#24 carrot** — repoint 2 nodes from `https://desert.tamu.edu/` to the catalog URL.
2. **#17 tomatoes** — repoint 2 container nodes at the same chart.
3. **#13 six crops** — file CASE 2 findings recording the measured absence, per crop, per arm.
   Garlic gets its own wording (a row exists; its harvest figure is rejected).
4. **pumpkin** (#7, #8) — the one squash with no `_regional_source_anchors_general` finding while
   its five siblings all have one. Cheapest remaining gap; file to match its siblings.
5. **cantaloupe / honeydew / watermelon** (#14) — MODELED-ONLY: windows declared, anchor id not.

Item 3 must not be written as one finding over six crops. The reason differs per crop: five have
no row anywhere, garlic has a row in a source we are declining, and the peas additionally need the
Cowpea/`Pisum` distinction recorded so the next session does not "find" the row we rejected.

### What actually shipped

Items 1, 2, 3 and 4 shipped. Item 5 did **not**, deliberately.

- **1 and 2 (4 nodes)** repointed and verified against the chart. Carrot's zone 8 cell is
  *corroborated*, not sole, so only its `heat_pause` was in the scan -- both were fixed anyway,
  because a fabricated attribution left standing in a second field is the defect this arc keeps
  re-finding.
- **3 (6 findings)**, one per crop, each carrying its own reason. Garlic additionally got a
  **plant_out repoint** to the Bexar page, which is better than the "leave it declared" option
  this doc originally recommended: a real TAMU garlic document was already trusted by garlic's own
  se_gulf and warm_arid regions. Its harvest arms stay bare, and the Apr 13 `harvest_start`
  tension is filed `open` at medium severity.
- **4 (pumpkin)** filed, matching the finding its five siblings already carried.
- **5 (cantaloupe / honeydew / watermelon) NOT filed.** AZ1005 is a live lead: it is Arizona's
  vegetable planting calendar, it is catalogued as `uariz_ext_az1005`, other crops cite it, and it
  plausibly carries cucurbit rows. Filing an absence finding without reading it would be exactly
  the [[absence-findings-are-document-scoped]] error. Left open and recorded.

Two guards were wrong on the first mutation sweep and both are worth recording. **G4** passed all
26 tests when neutered, so it was decoration until it earned its own test; it survives because it
is the only guard that can catch a path added to `REPOINTS` while still sitting in `HELD`, which
`PREFLIGHT2` cannot see because it runs before the edits. **G8's** expected sets were DERIVED from
the tables they validated, reproducing [[guard-derived-from-what-it-checks-is-vacuous]] inside the
promote written to avoid it; they are now hand-written constants asserted in both directions. A
test was also wrong for an instructive reason: it expected an abort when `nmsu_chart`'s catalog url
moved to `pubs.nmsu.edu`, and the promote correctly allowed it, because carrot already cites the
chart PDF under that id on its `direct_sow` arms.
