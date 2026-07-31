# Citation-integrity arc — the §5 sample pass, and what it re-priced

**Run:** 2026-07-29, fresh session, against canonical `dd24b180` (verified: `shasum` == `LATEST.txt`,
tree clean, HEAD `59c3afc`).
**Scope:** kickoff `docs/kickoffs/46-citation-integrity-cleanup-arc.md` §5 (the 20-row / 18-node
sample) plus the no-network measurements that the sample's first three nodes made obvious.
**Canonical was NOT modified.** No promote, no data edit. This pass is measurement + adjudication.

> **[CORRECTION 2026-07-31: row 18 of §4's table is WRONG and this document is where the error
> entered the arc.]** It states *"Riverside **is** `ca_interior`"* and concludes that "Season of
> ripeness at Riverside" *"directly serves the harvest windows of all 4 citrus crops on
> `ucr_citrus`'s 33 SOLE pairs"*. **Riverside is not `ca_interior` by our own data:**
> `zone_frost_data["10a"].regions.mediterranean` lists Los Angeles LAX, San Diego, Long Beach and
> **Riverside** -- the `ca_south_coast` set -- while `ca_interior` is anchored on the Central Valley
> (Sacramento/Fresno/Bakersfield/Modesto 8a, Tulare 8b, Stockton/Merced/Livermore 9a). The
> conclusion was also widened from a SINGLE observation on `crc3178`, an Owari Satsuma (a
> **mandarin**), to all four citrus crops. Measured over 24 accession pages on 2026-07-31: 24/24
> carry the ripeness field, 1/24 also carries Lindcove, and **0/24 publish a bloom date**. The datum
> is single-site and has no regional resolving power, and `source_catalog.ucr_citrus.citable_for`
> never claimed regional date windows -- so 31 of the 33 pairs are CASE 2 (unsourced claim), not
> CASE 1 (repoint). From here this claim propagated verbatim into kickoffs 46, 47 and 48, where it
> is now struck through. **The original text below is left byte-for-byte** as the record of what was
> believed on 2026-07-29. Full working: `STATE_HISTORY.md` 2026-07-31.

---

## 0. Headline

Two things came out, and they point in opposite directions:

1. **The arc is much cheaper than budgeted.** 681 SOLE pairs are **170 adjudications** over
   **32 document hunts**, and the premise that "the specific document was never recorded anywhere"
   is **false for all 26 bare-host source ids** — every one of them already cites real pathed
   documents on other cells.
2. **But it is a correctness problem, not just a provenance one, so the escalation branch of the
   §5 decision rule fires.** Adjudicating 92 California windows against the UC planting-date table
   they should rest on: **39 SUPPORTED, 35 DIVERGENT, 18 CONTRADICTED (20%)**. The rule says
   "≥2 of 20 (≥10%) → escalate, Trevor should hear about it before more crops certify."

The 18 contradicted cells collapse to **4 authoring decisions**, and **8 cells** are corroborated
as defective by a second, independent, no-network test.

---

## 1. First: the kickoff's own table re-verified (standing rule)

Every one of the 20 rows was re-read from canonical before any source was fetched. **All 20 claims
match the data exactly.** Two corrections to the kickoff:

- It says the 20 rows are **17 distinct nodes**. They are **18**. (Rows 1/4 and 10/20 are the two
  genuine duplicates; 20 − 2 = 18.)
- The node path in the table (`ca_desert.z10`) is not the schema path. Zones live at
  `regions.<region>.resolved_by_zone.<N>` with no `z` prefix.

---

## 2. The measurement that changes the cost model (no network)

### 2a. 681 pairs are 170 decisions over 32 document hunts

The 681 SOLE pairs are heavily redundant: for one crop × region the same bare host repeats on
`plantings[0]`, `.plant_out[0]`, `.bloom[0]`, `.harvest_start[0]`, `.harvest_end[0]` **and**
`resolved_by_zone.N`. Collapsing to the real adjudication unit:

| unit | count |
|---|---|
| SOLE bare-host pairs | 681 |
| distinct SOLE nodes | 481 |
| **distinct (crop, region, source) decisions** | **170** |
| **distinct (region, source) document hunts** | **32** |

Two hunts carry 36 of the 170: `mid_south`/`uada_ext` (22 crops) and `mid_atlantic`/`ncsu_ext`
(14 crops). The kickoff's "681 sole-source claims each needing a document located, several
sessions" over-counts the work by roughly 4x at the decision level and 20x at the document level.

### 2b. There are no bare-only source ids — the documents ARE recorded

The kickoff's cost reality says: *"for 1,566 — including 680 of the 681 SOLE rows — the catalog
entry is ITSELF a bare host, so the specific document was never recorded anywhere and has to be
located per claim."*

The catalog half is true. The conclusion is not. Measured with
`tools/citation_provenance_scan.py`: **all 26 source ids that carry a bare host also carry real
pathed documents elsewhere in the dataset.** Zero are bare-only.

| source id | bare | SOLE | pathed uses | example pathed doc already in the data |
|---|---|---|---|---|
| `ucanr_ext` | 337 | 188 | **1321** | `ucanr.edu/program/uc-master-gardener-program/time-planting` |
| `uc_mg` | 283 | 131 | 291 | same UC planting-date table (126 uses) |
| `ncsu_ext` | 99 | 79 | **1742** | `plants.ces.ncsu.edu/plants/...` |
| `tamu_agrilife` | 201 | 53 | **997** | `cameron.agrilife.org/.../RGV-Homeowner-Vegetable-Guide-2022.pdf` (468 uses) |
| `uariz_ext` | 91 | 50 | 458 | `.../az1005-2018.pdf` — Maricopa planting calendar (111 uses) |
| `nmsu_ext` | 28 | 18 | 171 | `pubs.nmsu.edu/_circulars/CR457B/` |
| `clemson_hgic` | 12 | 9 | **2483** | `hgic.clemson.edu/factsheet/...` |
| `uada_ext` | 141 | 100 | 8 | `.../FSA-6002.pdf` |

The document to repoint at is, for most hunts, already sitting in a sibling cell. **Caveat, and it
matters:** a pathed `ncsu_ext` URL for borage does not support apple. This makes the *hunt* cheap,
not the *answer* free.

### 2c. 53% of the SOLE nodes already declare the derivation

The bare hosts are not, mostly, an oversight that slipped past review. They are a **documented,
accepted convention**, and the data says so. `okra`'s own accepted finding, verbatim:

> `okra_pilot_region_anchor_base_urls` — "Several region-rep source anchors (umn_ext, umaine_ext,
> ucanr_ext, uc_mg, nmsu_ext, tamu_agrilife, uariz_ext, …) use the institution/publication **BASE
> URL** rather than a live okra-specific page… the per-region okra page URLs should be tightened
> during the daily review / **URL-liveness sweep**."

So this arc is the sweep that finding already schedules. Classifying all 481 SOLE nodes by whether
their crop carries such a finding:

| bucket | nodes | pairs | crops |
|---|---|---|---|
| DECLARED (modeled windows **and** portal anchors) | 122 | 203 | 14 |
| DECLARED (modeled windows only) | 135 | 226 | 13 |
| **UNDECLARED** | **224** | **252** | **22** |

The undeclared 224 are almost entirely **fruit trees and berries** — lemon 46, pear-european 17,
pear-asian 17, strawberry 12, then peach/plum/apricot/fig/pomegranate/persimmon/mulberry/
cherry-sweet/cherry-sour/nectarine at 11 each — concentrated in the **two most recently built
regions**, `mid_south` (`uada_ext`) and `mid_atlantic` (`ncsu_ext`).

**This is a distinct defect class from `unr_fs0261`.** A bare host plus an accepted "the windows are
modeled" finding is an *honest admission of derivation*. `unr_fs0261` was a *specific document cited
for a claim it does not contain*. Those need opposite treatment, and the 681 count conflates them.

### 2d. `mid_south` proves CASE 1 at scale — it built a document vocabulary and then didn't use it

`docs/reviews/notes/2026-07-20/mid_south_sources.md` defines a per-document citation vocabulary with
real pathed URLs and an explicit rule: *"within ONE cell a source id must map to exactly one URL."*
The catalog holds all of them: `uada_ext_fsa6001`, `uada_ext_spring_veg`, `uada_ext_fall_veg`,
`uada_ext_chill`, `uada_ext_fsa6105`, `nws_lzk`.

On `mid_south` cells those granular ids are used heavily and correctly — `uada_ext_spring_veg` 499
pairs / 82 crops, `uada_ext_fall_veg` 243 / 30. But plain `uada_ext` still sits on **143 pairs
across 29 crops**, carrying *two* URLs (the bare root and a pathed `FSA-6002.pdf`) — which
violates the region's own stated one-id-one-URL rule. The fruit crops were left on the institution
root while their vegetable siblings got the document.

`mid_atlantic_sources.md`, by contrast, names **zero URLs** — which is why its 14 hunts are the
harder half.

---

## 3. The correctness answer: 92 California windows vs the UC table

### The document

`https://ucanr.edu/program/uc-master-gardener-program/time-planting` — "Recommended planting dates
for major regions of California", attributed on the page to the *California Master Gardener
Handbook*, Table 13.2. Fetched with `urllib`, parsed and transcribed by hand from text I extracted
myself (no WebFetch summary, per §7). It is already the **most-cited pathed URL for both `uc_mg`
(126 uses) and `ucanr_ext`**, so prior passes already treat it as the canonical UC planting-date
table.

Its region definitions map cleanly onto ours, verbatim from the page:

> "North and North Coast = Monterey County north; South Coast = San Luis Obispo County south;
> Interior Valleys = Sacramento, San Joaquin, and similar valleys; **Desert Valleys = Imperial and
> Coachella Valleys**. Planting dates are for seed unless noted otherwise."

And its own honesty caveat, which is load-bearing for how the result is read:

> "Because the areas shown here are large, **planting dates are only approximate**, as the climate
> may vary even in small sections of the state."

### The result

Every California cell whose only citation is a bare UC host, with an unambiguous crop mapping to a
table row — 92 windows (`tools/…/ucmg_compare.py`, kept in the session scratchpad):

| verdict | n | share | meaning |
|---|---|---|---|
| SUPPORTED | 39 | 42% | cell window sits inside the table's months |
| DIVERGENT | 35 | 38% | overlaps but extends outside |
| **CONTRADICTED** | **18** | **20%** | **no overlap at all with the cited institution's own table** |

**The DIVERGENT class should not be called a defect.** The document says its dates are approximate
over large areas; a window running two weeks past a month boundary is inside that tolerance. This is
the "read the findings, don't count them" discipline applied to my own output — 35 of my 53
non-supported rows are absorbed by the source's own caveat.

**The 18 CONTRADICTED are 4 authoring decisions**, replicated across zones and crops by a shared
deriver:

| # | shape | cells | cell says | UC table says | independent check |
|---|---|---|---|---|---|
| 1 | winter-squash desert 2nd planting | 9 (acorn/butternut/spaghetti × z9/z10/z11) | `Jul 1 - Jul 31` | `Feb-March; **Aug**` | AZ1005 shows winter squash seeded Jul 1 / Jul 15 / Aug 1 in the low desert — **data defensible, citation wrong** |
| 2 | pumpkin desert windows | 5 | `Jan 15 - Feb 15` main, `Jul 1 - Jul 31` 2nd | `March-June` | AZ1005 pumpkin earliest mark is **Mar 1** — the July 2nd planting is fine; the **Jan 15 main window is unsupported by both** |
| 3 | okra desert | 3 | `Mar 1 - Apr 30` | `May` | AZ1005 okra `Mar 15 - May 15` — **data defensible, UC row coarse (it gives "May" for all four regions)** |
| 4 | okra north coast z9 | 1 | `Jun 1 - Jun 30` | `May` | not independently checked |

So shapes 1 and 3 are **citation defects with correct data** — the `unr_fs0261` shape exactly: a real
land-grant document cited for a window it places elsewhere. Shape 2 contains the pass's one strong
**data**-defect candidate.

### The corroborating no-network test

Independently of any document: a region's `plantings[]` arm declares
`plant_out = {from: last_frost, offset_days: N}`. Does the resolved per-zone window start at
`last_frost + N`?

Run naively this **floods — 751 cells, 66 crops** — and reading it, almost all are legitimate: mild-
region fall/winter cycles compared against a spring arm (nasturtium, leek, viola, kohlrabi), plus a
large benign cluster where resolved windows snap to clean calendar dates (`Feb 1` for `Jan 31 + 14`)
rather than exact arithmetic. Narrowed to frost-tender crops planted *earlier* than their own rule
inside the same spring cycle it still returns 114, still mostly month-boundary snapping of 1-5 days.

**This check is therefore MEASURED AND NOT SHIPPED** — the same disposition as
`logref_count_scan.py` and the stale-quote check. A gate here would flood.

But its extreme tail is not noise, and it is the same cells:

> **`acorn-squash`, `butternut-squash`, `spaghetti-squash` and `pumpkin`, `ca_desert` z10 + z11:
> resolved `plant_out` = `Jan 15 - Feb 15` with `resolved_from.last_frost = Jan 15` and a declared
> arm of `last_frost + 10`. The window starts exactly ON the mean last-frost date** — 10 days
> earlier than the crop's own stated rule, for a frost-tender cucurbit. That is a coin-flip on
> frost loss in the cell a beginner is most likely to follow.

Eight cells, flagged by two methods that share no inputs: the external UC table (January is outside
`Feb-March`) and the internal arm (`+0` vs declared `+10`). The z9 siblings show the milder version
(`Feb 1` vs `Jan 31 + 10`).

`calendar_coherence_gate` returns 0 and `url_health_gate` returns 0 on all of this — as expected;
neither covers this claim.

---

## 4. Sample-pass verdicts, node by node

Honest coverage statement: **8 of 18 nodes resolved conclusively, 6 resolved as
UNVERIFIABLE-by-construction, 4 not resolved** (they need a fruit-tree document not yet located).
The 92-cell California adjudication above is broader than the sample and is the stronger evidence.

| # | node | verdict | evidence |
|---|---|---|---|
| 1 | acorn-squash `ca_desert` z10 | **CONTRADICTED** | UC: winter squash Desert Valleys `Feb-March; Aug`; cell `Jan 15 - Feb 15` + `Jul 1-31`. Plus the frost-rule violation. |
| 2 | honeydew-melon `ca_desert` z11 | **SUPPORTED** | UC: melons Desert Valleys `Jan-April`; cell `Feb 1 - Mar 20` sits inside. |
| 3 | okra `ca_south_coast` z9 | DIVERGENT | UC: okra South Coast `April-May`; cell `May 1 - Jun 15`. |
| 4 | cantaloupe `ca_north_coast` z10 | DIVERGENT | UC: melons N/N-Coast `May`; cell `Apr 15 - Jun 1`. |
| 5 | pumpkin `ca_desert` z9 2nd | **CONTRADICTED** | UC: pumpkins Desert Valleys `March-June`; cell `Jul 1 - Jul 31`, no overlap. |
| 6 | cantaloupe `low_desert_az` z10 | DIVERGENT | AZ1005 melons seeded `Feb 15 → Jul 15` continuous; cell `Feb 1 - Mar 15` starts 2 wks early, 2nd window ends Aug 15, a month past the last mark, and the document shows **no mid-season split**. |
| 7 | lemon `ca_desert` z10 | unresolved | citrus; the veg table does not cover it. |
| 8 | lime `low_desert_az` z10 | unresolved | as above. |
| 9 | acorn-squash `warm_arid` z8 | **UNVERIFIABLE** | NMSU **CR457B read in full**: it publishes last-frost *by zone* (`8a Feb 28 – Mar 30`, `8b Before Feb 28`) and days-to-maturity per crop (Table 2), and **no per-crop planting-date window**. The document backs the derivation's *inputs*, never the window. |
| 10 | butternut-squash `warm_arid` z8 | **UNVERIFIABLE** | same document, same finding. The kickoff flags rows 10/11 as the suspicious byte-identical pair; they are identical because both are DTM-modeled off one shared frost anchor, which the crops' own accepted findings state. |
| 11 | shallot `rgv` z10 | **UNVERIFIABLE (self-declared)** | the cell's own region note: *"No RGV-specific table row exists for shallots; this cell uses a conservative fall set-planting window … rather than a stated TAMU date."* |
| 12 | blueberry `mid_south` z7 | unresolved | needs the Arkansas fruit publication; `FSA-6105` is blackberry. |
| 13 | oregano `mid_south` z8 | **UNVERIFIABLE (self-declared)** | `oregano_pilot_finding_001`: windows modeled from phenology + frost dates, *"not from an oregano-specific per-region planting chart (none found for all 10 regions)"*. |
| 14 | sage `mid_south` z8 | **UNVERIFIABLE (self-declared)** | `sage_pilot_finding_001`, same shape. |
| 15-17 | apple / cherry-sweet / pear-asian `mid_atlantic` z8 | unresolved | `plant_out "Dec - Feb (dormant)"` is a horticultural universal, not a regional datum; the harvest windows need an NC State fruit document. Note these cells' `suitability_note`s do quote NC State substantively ("steers zone 8 growers toward sour cherry"), so the citation supports *a* claim on the cell. |
| 18 | grapefruit `ca_interior` z8 | repoint identified | the only pathed `ucr_citrus` URL (`crc3178`, 19 uses) is **Owari Satsuma**, not grapefruit — but it proves UCR CVC accession pages carry **"Season of ripeness at Riverside"** (`October to December` for that accession). Riverside *is* `ca_interior`. That field directly serves the harvest windows of all 4 citrus crops on `ucr_citrus`'s 33 SOLE pairs. |

### Statistical honesty

Per §5's own instruction: the 18-node sample is **not** a clean n=18 — 4 nodes are unresolved, so no
rate bound should be read off it. The **92-cell California adjudication** is the measurement with
power, and its 20% contradicted rate is over the escalation threshold. It covers **one institution's
table and four regions**; it says nothing about `mid_south`, `mid_atlantic`, `warm_arid`, `rgv` or the
fruit-tree archetypes, which is where 224 of the 481 undeclared nodes live.

---

## 5. The decision, per the rule committed to before looking

**≥2 of 20 CONTRADICTED → correctness problem → escalate.** Measured 18 of 92 (20%). So:

1. **The arc is a data-correction arc, not a repoint grind.** It needs its own gauntlet and state
   trio per batch.
2. **Trevor should see the 8-cell frost-tender finding before more crops certify** — it is
   corroborated by two independent methods and it is a beginner-facing failure mode.
3. **But the grind is 4-20x smaller than budgeted** — 170 decisions, 32 document hunts, with the
   target document already in the data for most.

### What NOT to do

- **Do not mass-repoint.** Pointing these cells at the UC table would *create* a visible
  contradiction on 53 of 92 California windows. Repointing is only safe after per-cell adjudication.
- **Do not treat the 681 as one class.** 257 nodes are self-declared modeled derivations (honest,
  needing at most a display decision); 224 are undeclared, and those are the real worklist.
- **Do not ship the frost-offset check as a gate.** Measured at 751 / 114; it floods.

### Suggested order, revised

1. **The 8-cell frost-tender desert cucurbit window** — smallest, most concrete, highest
   user-facing risk. Needs Trevor's call because it is a data change.
2. **`mid_south`/`uada_ext`, 22 crops** — the vocabulary and URLs already exist; largest single hunt,
   most mechanical.
3. **The 3 remaining contradicted shapes** (winter-squash July/August, okra desert, okra north
   coast) — each one adjudication covering 3-9 cells.
4. **`ucr_citrus` 33 pairs** via UCR CVC "Season of ripeness at Riverside" — one repointing method,
   4 crops.
5. **`mid_atlantic`/`ncsu_ext`, 14 crops** — harder; its sourcing note names no URLs.
6. The remaining 27 hunts.

---

## 6. Traps that actually fired this session

- **AZ1005's grid is rotated 90°** (text `dir = (0,-1)`): months run *down* the y-axis, crops are
  *columns* on x. `pypdf`'s flattened text yields `Artichokes, Globe … T T T T T S S S` — 8 markers
  for 24 half-month columns, with the positions gone. Read by word geometry via `fitz`, with a hard
  guard that refuses to emit unless it recovers exactly 24 half-month ticks. The guard fired on the
  first attempt and prevented a plausible-but-wrong grid. **Validated against a control before
  reading any sampled crop**: tomatoes came out `T Feb 15 / Mar 1 / Mar 15` + `T Jul 15 / Aug 1`,
  which is the known Phoenix double-crop calendar.
- **`tamu_agrilife` bare host → 403 on the RGV guide** via plain urllib. Recorded as
  "could not determine", not as absence.
- **A document can be the right one and still not contain the claim.** NMSU CR457B is exactly the
  document `nmsu_ext` should cite for `warm_arid`, and it has no planting-date window in it. Locating
  the right document is not the same as supporting the claim.

---

## 7. Tooling

**Shipped:** `tools/citation_provenance_scan.py` — collapses the bare-host pairs to real decision
units, counts the document hunts, classifies nodes by whether the crop declares the derivation, and
proves the split-personality property. No network, no gate wiring.

**Measured and deliberately NOT shipped:** the frost-offset coherence check (751 naive / 114
narrowed, overwhelmingly month-boundary snapping). Its one real signal is the 8 cells in §3, which
are recorded here instead.
