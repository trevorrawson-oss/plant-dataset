# PLA-466 / PLA-565 working state -- 2026-09-21

**Status: PARKED, awaiting Trevor's fetches and rulings. NOTHING WRITTEN TO CANONICAL.**

Canonical at park: `1721208ee0cbe4249ecf32ca3bd47a786f8a689cadcb7bb300d8d8ada4d82054`
`origin/main` at park: `21a43f0e29e946dd4d956be2bd331ea9d81dff3c`

A Plan C field-shape session is running in parallel on its own branch. It commits a spec
document only and does not touch canonical, so the `--expect-sha 1721208e` pin stays valid.
**Check `origin/main` before committing anything to canonical or the state trio.**

This document is written so a fresh session can pick the arc up cold. Read it top to bottom
before acting.

---

## 1. What this arc is

PLA-466 asked three questions about rootstock data: whether St. Julien A is really on plum's
cited page, whether apricot wrongly omits Citation, and whether lemon's `semi_dwarf` labels or
its "modest, not true dwarfing" prose is right.

All three closed. Answering them uncovered four larger defects, now filed separately.

---

## 2. Evidence ledger

Every fetched document, with the hash computed in the 2026-09-21 session. The files lived in a
session scratchpad that does not persist. **Re-fetch and verify against these hashes** rather
than trusting a later copy.

| Local name | Source URL | Read / capture | Bytes | sha256 |
| -- | -- | -- | -- | -- |
| `plum_wb_20260113.html` | `ucanr.edu/site/fruit-nut-research-information-center/plum-rootstock-scion-selection` | Wayback 2026-01-13T07:18:39Z | 83,384 | `578342a715f775ee21c1602df16bcd9a833a1ab2929e5f8c7a67f255fd7bd0a4` |
| `plum_wb_20251111.html` | same | Wayback 2025-11-11T14:16:42Z | 77,907 | `4b7e903356f300dbcb5e24b203561135c506538517e3fa95af29a452cf852ac4` |
| `s_20250613071716.html` | same | Wayback 2025-06-13T07:17:16Z | 90,369 | `017a51da1489857ed41d78792fa7b2fc4fe2c2fa059eca9c315c29f35bff157e` |
| `s_20250524130906.html` | same | Wayback 2025-05-24T13:09:06Z | 91,688 | `4410c4122fecff590d1c62c50faeedf1cf689ba11850513d51b252fb222a1f86` |
| `apr_fnric.html` | `ucanr.edu/site/fruit-nut-research-information-center/apricot-scion-rootstock-selection` | Wayback 2025-12-09T14:49:45Z | 74,752 | `963b157133915a98d1589b12754d6f0c70dbbfc123bc326fd1467d8cc2afa9ee` |
| `apricot_ucipm.html` | `ipm.ucanr.edu/home-and-landscape/cultural-tips-for-growing-apricot/` | live 2026-09-21 | 42,943 | `729ed20070cfdd26aacbd6872f08358d5bffac2f89b13b22a3464e29edd52c22` |
| `apr_usu.html` | `extension.usu.edu/yardandgarden/research/apricots-in-the-home-garden` | live 2026-09-21 | 66,576 | `5a54e095952a591bc56b8a775c45fec561763f9873d7170e33d16151ea57c398` |
| `uf_hs402.html` | `ask.ifas.ufl.edu/publication/HS402` | live 2026-09-21 | 158,367 | `50436e71fe8fb2bcaee7949f83f9fb192cdc3c0cbe875f7b6b74808f5f9459fb` |
| `uf_hs132.html` | `ask.ifas.ufl.edu/publication/HS132` | live 2026-09-21 | 108,311 | `5b22371df47e8a27e3b138079b6e8e41e246caeefb31af114febd07c975d183a` |
| `uf_CH093.html` | `ask.ifas.ufl.edu/publication/CH093` | live 2026-09-21 | 160,411 | `5bbca72512ff1e408787cdd7ae007c369532882659b8cdd008fdf2ce1782c14f` |
| `uf_CH092.html` | `ask.ifas.ufl.edu/publication/CH092` | live 2026-09-21 | 151,716 | `27c7bc139ab30f6fe73bd68145ffb47e8cc241bf017c9f90b4774f8cba068206` |
| `uf_HS1260.html` | `ask.ifas.ufl.edu/publication/HS1260` | live 2026-09-21 | 238,884 | `9503b58425e7c94b15f500c88654714f24b9b39ba58cffaf887f4ecf0c2dec27` |
| `uf_CH116.html` | `ask.ifas.ufl.edu/publication/CH116` | live 2026-09-21 | 116,589 | `0d2ef6611e5d4ba6d3ec3c91db660727a68d9a5cb94ee97eb0af412f2257a211` |
| `clemson_pn.html` | `hgic.clemson.edu/factsheet/peaches-nectarines/` | live 2026-09-21 | 152,215 | `b765a1c3f937032629e59c0263232f1acc0133cb61c6484d08c15216f02f6205` |
| `ucd_4506.html` | `fruitsandnuts.ucdavis.edu/node/4506` | live 2026-09-21 | 5,515 | `eeaed8dd8f2b6b4e573361530d19fd840880203003b9157a74dfd5314f709b78` |

**`ucd_4506.html` is a Cloudflare block page, NOT the document.** Its hash is the hash of an
interstitial. Do not treat it as content.

Document titles, read off each document rather than assumed:

- HS402 = "HS1153/HS402: Lemon Growing in the Florida Home Landscape" (dual-numbered, so the
  source key `uf_ifas_hs1153` is correct even though the URL says HS402)
- HS132 = "HS-867/HS132: Citrus Culture in the Home Landscape"
- CH093 = "HS8/CH093: Growing 'Tahiti' Limes in the Home Landscape"
- CH092 = "FC47/CH092: Key Lime Growing in the Florida Home Landscape"
- HS1260 = "SP248/HS1260: Florida Citrus Rootstock Selection Guide, 5th Edition"
- CH116 = "HS195/CH116: The Satsuma Mandarin"
- Clemson = "Peaches & Nectarines | Home & Garden Information Center"

---

## 3. Instrument warnings (three false zeros hit in one session)

A fresh session will hit these again. All three nearly produced wrong findings.

1. **`ucanr.edu/site/*` returns 403 to the sandbox**, Fastly/Varnish, with a Drupal "Access
   denied" body that renders like a normal page. A live page and a dead page are
   indistinguishable from here. The positive control that caught it: the marin citrus page
   (lemon's own anchor, same `/site/` subtree) also 403s from the sandbox but loads fine from a
   residential browser. **A sandbox 403 means "cannot see", never "dead".**
2. **The Wayback `availability` API returned `{}`** for the plum URL. The **CDX API** returned
   four captures, all 200, for the same URL. Use CDX. Never conclude absence from `availability`.
3. **A term search for `dwarf` returned 0** on HS1260, a citrus rootstock guide that encodes
   size as Sm / I / Lg. Absence of a term is not absence of the claim. Check the document's own
   vocabulary before reporting a zero.

`fruitsandnuts.ucdavis.edu` is blocked too, by a **different** mechanism: Cloudflare, block page
names `sfcf.ucdavis.edu`. A Shortcut or browser fetch is required. A saved file that reads
"Just a moment" or "checking your browser" is a challenge, not the page; the real FNRIC pages
ran 74-92 KB in the Wayback captures, a challenge page is usually under ~20 KB.

`ipm.ucanr.edu` is a separate host and is **not** blocked.

---

## 4. Findings, closed

### 4.1 St. Julien A is ABSENT from plum's cited page

Full read of the page, 9,003 characters of extracted text, complete rootstock section. Term
counts identical across all four Wayback captures (2025-05-24 through 2026-01-13):

```
Julien 0    insititia 0    container 0    gallon 0    pot 0
Citation 2  Mariana 2      "10 to 15" 1
```

The page enumerates exactly five rootstocks: Myrobalan 29C, Mariana 2624, Nemaguard, Lovell,
Citation. Trevor corroborated with a screen grab of the UC Davis mirror (`node/4506`), whose
rootstock section matched six sentences byte-for-byte, and whose footer reads
"Last update: January 9, 2023". The two hosts are **not** byte-identical: the scion section
reads "1905" on the UC Davis mirror and "1955" on ucanr.edu, which makes them independently
maintained renderings that both lack St. Julien A.

**Do NOT cite the NC-140 plum trials as a reason.** They were not read in this arc, and PLA-463
already caught that NC-140 claim being misapplied once.

Verbatim, from `plum_wb_20260113.html`:

> "Mariana 2624 ( P. cerasifera x P. munsoniana ) is compatible with most cultivars and produces
> a semi-dwarf tree (10 to 15 ft). This rootstock is typically used in northern California
> because it tolerates wet, heavy soils (Norton and Coates 2012). It acclimates well to a wide
> range of soil types and climatic conditions. It is resistant to oak root fungus, crown rot,
> crown gall, and root knot nematode (Southwick et al. 1999; LaRue 1973)."

> "Citation ( P. salicina x P. persica ) is a peach-plum hybrid rootstock that produces dwarf
> trees (8 to 12 ft) and is tolerant of wet soils (Layne, 1994). Citation is resistant to
> root-knot nematode but susceptible to crown gall and bacterial canker (Johnson et al. 2013)."

**Container claims are ABSENT for BOTH Marianna and St. Julien.** `container` 0, `gallon` 0,
`pot` 0 on all four captures.

### 4.2 apricot's premise was wrong about which page

The cited apricot anchors carry **zero** rootstock content: `rootstock` = 0 on both
`apricot_ucipm.html` and `apr_usu.html`. The single `Citation` hit on the UC IPM page is the
footer link "Use Permissions and Citations".

The Nemaguard/Citation claim lives on the FNRIC apricot page, which is **not cited on the crop**.
Verbatim from `apr_fnric.html`:

> "Specifically, apricot has been successfully grown on several rootstocks including Nemaguard,
> Nemared, Lovell, Marianna 2624 (plum), and Citation (hybrid) (Hartmann et al. 2011). Nemaguard
> (seedling peach rootstock) and Citation are the most common rootstocks used in commercial
> apricot production in California. Nemaguard confers vigor, good anchorage, and is resistant to
> root knot nematode. Mariana 2624 is occasionally used in commercial plantings in Northern
> California because it tolerates wet, heavy soils, although it is very susceptible to bacterial
> canker (Norton and Coates 2012). Citation has been used in the southern edge of California
> apricot production in the central valley, and is increasing in popularity (Norton and Coates
> 2012, C. Ledbetter pers comm). Apricot can also be grown on Myrobalan plum rootstocks, although
> weakness and breaking at the graft union has been reported after high winds. As a result of
> this problem Myrobalan rootstocks should only be used in very heavy or wet soils."

The NC-140 passage, verbatim, same file:

> "Several new experimental rootstocks have been evaluated by the NC-140 rootstock trials over
> the past ten years, conducted by a group of North American scientists and the USDA. One goal of
> the NC-140 rootstock trials has been to identify new dwarfing rootstocks that limit tree height
> and size, without altering scion production or fruit characteristics. Ideally, the shorter,
> more compact trees will require less pruning and reduce labor costs by eliminating the need for
> ladders to harvest fruit (DeJong et al. 2010). Although they may help reduce costs and increase
> competitiveness, dwarfing rootstocks developed by the USDA and evaluated in NC140 trials
> (including HBOK32, HBOK10, HBOK50, Controller 5 and Controller 9 ) are not yet widely used in
> commercial plantings."

And the seedling paragraph:

> "Within California, both Royal and Blenheim apricot varieties work well as rootstocks because
> they are immune to the root knot nematode and are somewhat resistant to the root lesion
> nematode and to crown gall (C. Ledbetter pers comm). However, apricot seedlings are susceptible
> to both oak root fungus and Verticillium wilt, and are not commonly used in commercial
> plantings."

Page-wide on `apr_fnric.html`: ` ft` 0, `feet` 0, `tall` 0, `container` 0, `gallon` 0, `pot` 0,
`semi-dwarf` 0. So this page **cannot** anchor a `size_class`, a height or a container claim.

**Citation's size effect on apricot is UNDETERMINED at T1.** The 8-12 ft dwarf figure is on the
**plum** page, for plum. PLA-463's D-C ruling (size_class is rootstock-plus-scion) forbids
carrying it across. Cold limits and backyard availability are both **absent** (`cold` 0,
`hardi` 0). The note "standard apricot rootstocks do not dwarf the tree" is therefore **not**
shown false by T1.

### 4.3 lemon and lime: the label is unsupported, the prose is right

`dwarf` = 0 and `semi-dwarf` = 0 in **all four** cited UF/IFAS documents. Non-"dwarf" size
vocabulary was also checked: every `smaller` hit is nursery pots, psyllid nymphs or
zinc-deficient leaves, and CH093's one `tree size` hit is about **pruning** to keep height at
6-8 ft.

HS132 mentions none of the rootstocks at all (`trifoliate` 0, `Swingle` 0, `sour orange` 0).

`semi_dwarf` on trifoliate orange, Carrizo and Swingle citrumelo is unsupported by every cited
page. **Recorded reason for nulling: the only T1 rating uses a scale the dataset has not
mapped.** Not "contradicted" -- that phrasing was withdrawn as an overstatement.

HS1260's Table 1, parsed structurally from HTML rather than flattened text. Column 5 is
`Tree size`, column 6 is `Spacing` (ft):

| Rootstock | Tree size | Spacing |
| -- | -- | -- |
| Flying Dragon TF | Sm | 5-7 |
| Swingle citrumelo | I | 8-12 |
| Sour orange | I-Lg | 8-12 |
| Rough lemon | Lg | 10-15 |
| Volkamer lemon | Lg | 12-15 |

The guide's own scale definition:

> "A tree on a selected rootstock would be rated large [Lg] if it was comparable in vigor and
> size to one on Cleopatra mandarin or rough lemon, i.e., perhaps 14-20 ft tall. A small tree
> [Sm] would be less than 8 ft tall at maturity"

**Dwarfing availability for lemon: UNDETERMINED.** HS1260 covers lemon only as a graft-
compatibility variable ('Bearss', 'Eureka'), and those columns are not in the parsed table.
**For lime: UNDETERMINED and weaker** -- HS1260 `lime` 0, and neither CH092 nor CH093 names
Flying Dragon. CH116 carries Flying Dragon 12 times but is scion-locked to satsuma.

### 4.4 The tristeza defect, on BOTH lemon and lime

HS402, verbatim:

> "Tristeza. Lemons are susceptible to severe tristeza virus strains regardless of rootstock, and
> less severe strains when propagated on Citrus macrophylla (macrophylla) and rough lemon ( C.
> jambhiri ) rootstocks. Tristeza is transmitted by the brown citrus aphid ( Toxoptera citricida
> ). Purchasing certified disease-free trees under the Florida Budwood Registration Program will
> greatly reduce the chances of purchasing a tree with this disease."

This is a self-contained entry in a disease list. What precedes it is postbloom fruit drop; what
follows is the "Nutritional Disorders" heading. There is no wider paragraph.

The dataset says the weakness is "in some scion combinations". HS402 says "regardless of
rootstock". **Contradicted, not merely unsupported.**

**The identical sentence is on lime**, byte-for-byte, and also as the last sentence of its sour
orange `traits_seasoned`. Lime's own already-cited anchors carry the fix:

CH093 (`ufifas_ext`), verbatim:

> "Tristeza 'Tahiti' limes may be susceptible to severe tristeza virus strains, regardless of
> rootstock. However, these trees may be susceptible to less-severe strains when propagated on
> Citrus macrophylla (macrophylla) and rough lemon ( C. jambhiri ) rootstocks (J.H. Crane,
> personal communication)."

CH092 (`uf_ifas_edis`), verbatim:

> "Tristeza Key limes are susceptible to tristeza virus regardless of rootstock."

**Provenance caution:** CH093 hedges ("may be susceptible") where CH092 and HS402 are flat, and
attributes the milder-strain half to a personal communication. Lime copy must not borrow HS402's
flat phrasing for the Tahiti half.

---

## 5. Adopted rulings

### On PLA-463 (recorded as a comment there, for Plan E)

- **Rule N adopted.** If any entry in a non-empty `rootstock_options[]` has `size_class: null`,
  the mechanical test returns `undetermined` and assigns nothing.
- **D-B collision: option (ii), freeze before nulling.** Plan E freezes each basis as authored
  data with provenance; the mechanical test then becomes a consistency check, not a derivation.
  Option (i) was rejected because apricot's four `standard` labels are unsourced, so keeping
  `size_class` as the test's input would preserve an unread classification as load-bearing.

Supporting measurement: 21 crops carry the `rootstock_options` key, 17 have non-empty arrays,
4 are empty (fig, pomegranate, avocado, olive). **Entries with `size_class: null` dataset-wide:
0** -- the test has never met a null. The test has two unnamed branches: an all-null array, and
a single non-standard value.

**Rule N is a precondition for the lemon and lime nulls**, not an independent improvement. Under
the pre-Rule-N test, lemon at `null:2 standard:1` reads distinct non-null `{standard}` and
returns `soil_and_pest`, rendering Variant B copy that asserts no size-controlling rootstock
exists, on a question that is undetermined.

### PLA-466 promote scope (NOT YET STAGED)

- **plum St. Julien A: drop the entry.** Reason: absent from the only cited T1 page across four
  captures. Record in plum's `open_findings`.
- **plum Marianna 2624: keep `semi_dwarf` [10,15]. Null `container_suitable` and
  `container_size_gallons`.** The close-out must state the consumer effect: plant-app currently
  derives plum as container-capable at 25 gal through this flag; nulling moves it to not suited,
  matching the site. That closes PLA-7 defect 1 and is intended, not a regression.
- **plum Citation: admit at `dwarf` [8,12]**, `container_suitable` null, `container_size_gallons`
  null. The page makes no container claim; a true flag would re-trigger the app's derivation.
- **Both plum items need a live anchor. They wait on PLA-565.**
- **lemon and lime: `size_class` to NULL** on the `semi_dwarf` entries (not `standard`, which
  would be an unread value), and null the container flags. **Do NOT touch
  `rootstock_selection_basis`**; held until Plan E applies Rule N.
- **lemon and lime: record the tristeza contradiction as an open finding.**
- **Measure the consumer effect on the landed bytes, do not assert it.** Expected: plant-app
  stops treating plum as container-capable. Confirm lemon and lime keep `container_ok` and
  `container_path: direct`, and that `container_path_gate` and A58 stay green.

Every quote in the write-up carries its URL, capture or read date, bytes and sha256 (PLA-563:
quotes are the one field with no guard).

---

## 6. Held drafts (approved in principle, NOT staged)

### lemon.recommended_rootstock_note

Replace, exact-match verified present:

> "Its one serious caveat is susceptibility to tristeza virus in some scion combinations."

With:

> "Tristeza virus is a lemon problem rather than a rootstock one: lemon trees are susceptible to
> severe tristeza strains whatever the rootstock, and also to milder strains when grown on
> macrophylla or rough lemon. Buying certified disease-free trees reduces the chance of bringing
> one home infected."

### lemon.rootstock_options[sour orange].traits_seasoned

Replace the last sentence, exact-match verified present and verified to BE the last sentence:

> "Main weakness is susceptibility to severe tristeza virus strains in some scion combinations."

With:

> "On lemon, susceptibility to severe tristeza strains does not depend on the rootstock, so it is
> not a reason to choose against this one."

Source: `uf_ifas_hs1153` (HS402), already on the entry.

**Scope notes to record with the change:** HS402 ties the certified-tree advice to Florida's
budwood program and the draft generalizes to certified trees. Only the tristeza claim is
corrected; the note's other claims are NOT verified by this pass. Record that rather than
implying the note is now clean.

### lime

Rides along in PLA-466 (Trevor's ruling). The claude.ai lane drafts from lime's slice against
CH093 and CH092. Not yet drafted at park.

### apricot.recommended_rootstock_note -- PROVISIONAL, DO NOT STAGE

Held behind PLA-565 (catalog scope) and PLA-566 (roster and recommendation):

> "Choose an apricot rootstock for your soil and pests. The rootstocks in common use differ
> mainly in what they tolerate, and the dwarfing rootstocks tested in the NC-140 trials are not
> yet widely used in commercial orchards. Seedling apricot stocks resist root-knot nematode but
> are susceptible to oak root fungus and Verticillium wilt. Myrobalan is best kept to very heavy
> or wet soils, because its graft union can break in high winds. Marianna 2624 tolerates wet,
> heavy soils but is very susceptible to bacterial canker."

If Nemaguard is admitted, add: "Nemaguard, the most common in California orchards, adds vigor,
good anchorage and root-knot nematode resistance."

"Differ mainly in what they tolerate" is **modeled** from the page describing the stocks only by
soil and pest traits; record it as modeled. The source is California-scoped and silent on cold
hardiness. The note cannot cite `ucd_fruitnut` for rootstock content until PLA-565 rules.

**Note: `recommended_rootstock_note` is SINGLE-REGISTER.** No `_beginner` / `_seasoned` siblings
exist dataset-wide. A dual-register note is a field addition, not a copy edit. Recorded on
PLA-480.

---

## 7. Tickets filed from this arc

| Ticket | Subject | State at park |
| -- | -- | -- |
| **PLA-466** | the parent | In Progress, promote not staged, blocked by PLA-565 |
| **PLA-565** | `ucd_fruitnut` citable_for is chill-scoped but already anchors a rootstock page | **Todo, URGENT, blocking PLA-466**, blocked on fetches 1 and 2 |
| **PLA-566** | apricot rootstock re-authoring | Backlog, child of PLA-7 |
| **PLA-567** | citrus Sm/I/Lg size-scale ruling | Backlog |
| **PLA-568** | url_health_gate three-outcome instrument | Backlog |
| **PLA-579** | plum's 48 region cells cite a rootstock-selection page | Backlog |
| **PLA-480** | comment added: the note is single-register | scope only |

### PLA-565, why it is urgent

plum's dead anchor carries **24% of the crop's citation weight**: 52 of 220 anchoring
source-references, and **39 cells where it is the SOLE source**. Grouped: `regions` 48,
`rootstock_options` 3, `varieties` 1.

### PLA-566, corrections already applied

The family-level claim was **WITHDRAWN**. A nectarine is a peach (*Prunus persica*), so identical
arrays are plausible biology, not a cross-scion carry. The anchor audit confirms the innocent
reading: every peach and nectarine rootstock row is anchored to
`hgic.clemson.edu/factsheet/peaches-nectarines/`, a single T1 document covering both crops
(`peach` 33, `nectarine` 10, `rootstock` 6). Byte-identity is recorded as an observation only:

```
peach     rootstock_options sha256: cca04f6fd741490ba5e5f6ae2571b757d608cfeb055727d700358a12895c5869
nectarine rootstock_options sha256: cca04f6fd741490ba5e5f6ae2571b757d608cfeb055727d700358a12895c5869
```

Loose end: `Halford` returns 0 on the Clemson factsheet, so that row rests on `ncsu_ext` alone
and has not been read.

PLA-566 Finding 5: `recommended_rootstock` is "Myrobalan 29C", a stock FNRIC says to confine to
very heavy or wet soils because the graft union can break in wind. The **value itself** needs
re-deciding, not just the note.

### PLA-579, population scan result

Crops citing a rootstock/scion or FNRIC-type page inside `regions{}`, across all 120 crops with
a `regions{}` block:

| Outcome | Crops | Refs |
| -- | -- | -- |
| FOUND, defective | 1 (plum) | 48 |
| FOUND, topically appropriate | 3 (apple, pear-asian, pear-european) | 47 |
| ABSENT | 116 | 0 |

The 47 cite the FNRIC chilling-requirement page; a chill page for timing cells is on-topic. But
**whether they satisfy R4 is UNDETERMINED** -- that page has not been read. Fetch 4 closes it.

The plum page's calendar vocabulary, measured: `bloom` 0, `plant out` 0, `planting date` 0,
`frost` 0, `chill` 0, `zone` 0, `harvest` 6 (all six are California commercial cultivar timing).
**A repoint does not fix these 48**; they need a real source or a null.

---

## 8. The `launch_ready` consumer measurement (PLA-579's open question)

Measured 2026-09-21 across both consumer repos, main trees only (worktree copies excluded).

**plant-astro: ZERO reads.** No source file references `launch_ready`, `launch_ready_core` or
`launch_ready_seasoned` in any form.

**plant-app: the fields never reach the app.**

- `scripts/export-projection.mjs` prunes `verification_status` to three children:
  `VERIFICATION_STATUS_KEEP = new Set(['status', 'source_set', 'date'])`. Its own comment says
  `status` gates which crops get a page, `source_set` is counted and rendered, `date` is the
  TreeGuide `lastReviewed` fallback. **`launch_ready_core` and `launch_ready_seasoned` are
  DROPPED** and counted in `stats.dropped`.
- The crop-level allowlist entry naming them (line 61) is **vestigial for 125 of 128 crops**,
  because the fields live inside `verification_status` on 128/128.
- No app code reads them: `grep -E 'launchReady|launch_ready'` over `src/**` returns **0 hits**.
- The two `build-guides-data.mjs` hits are **comments** describing which batch a crop came from,
  not code.

**Conclusion: setting `launch_ready_core` or `launch_ready_seasoned` to false would do NOTHING in
either consumer today.** Not hide, not gate, not badge. Nothing. The field that actually gates a
crop's page is `verification_status.status`.

This bears directly on the proposed plum `blocks_launch` finding: it would be a dataset-internal
record with zero consumer effect unless the intent is also to move `status` away from
`verified_gs_arc`, which IS the gate. **Trevor rules after reading this.**

### Incidental defect found while measuring

Three crops carry a **crop-level** `launch_ready_core` in addition to the one inside
`verification_status`:

| Crop | crop-level core | inside `verification_status` |
| -- | -- | -- |
| beefsteak-tomato | true | true |
| heirloom-tomato | **false** | **true** |
| artichoke | true | true |

**heirloom-tomato's two copies disagree.** The crop-level copy is the one on the export
allowlist, so the `false` ships to the app while the authoritative `true` is pruned away. Not
filed yet; belongs with whoever owns the export projection.

---

## 9. plum's state today, for the blocks_launch ruling

Measured on canonical `1721208e`:

```
verification_status.status ... "verified_gs_arc"
phase ........................ "wave1_stone_fruit_gs_arc"
date / last_audited .......... "2026-07-02"
launch_ready_core ............ true
launch_ready_seasoned ........ true
open_findings ................ 3, ALL blocks_launch: false
  [0] plum_self_fertile_boolean_european_default   (deferred)
  [1] mid_south_bloom_offset_undocumented          (accepted_modeled)
  [2] mid_atlantic_bloom_offset_undocumented       (accepted_modeled)
```

Nothing blocks plum's launch today. Adding a `blocks_launch: true` finding is a state change on
a crop that is currently shipping, not a no-op.

---

## 10. Fetch list, and what each closes

Trevor fetches these from an iPad. **Constructed URLs were dropped**: a 403 on a URL nobody has
ever seen serve tells us nothing.

| # | URL | Provenance | Closes |
| -- | -- | -- | -- |
| 1 | `https://fruitsandnuts.ucdavis.edu/node/4506` | Trevor's own message; he loaded it in Safari and sent a screen grab | Raw bytes for the plum repoint candidate. Its `<link rel="canonical">` reveals the real word-path, so nobody guesses the slug. PLA-565. |
| 2 | `https://fruitsandnuts.ucdavis.edu/persimmon-scion-rooststock-selection` | dataset `anchoring_urls`, persimmon, key `ucd_fruitnut` | Whether "rooststock" (three s) is UC Davis's own slug or our typo. PLA-565 cannot close without it. |
| 3 | `https://ucanr.edu/site/fruit-nut-research-information-center/pomegranate-diseases-disorders` | dataset `anchoring_urls`, pomegranate, key `ucanr_ext` | Turns pomegranate from **undetermined** to live or dead. On ucanr.edu, not Cloudflare, so it either renders or shows the Drupal "Access denied" page. PLA-568. |
| 4 | `https://fruitsandnuts.ucdavis.edu/general-information/chilling-requirement` | dataset `anchoring_urls`, key `ucd_fruitnut`; apple (verified 2026-06-11), pear-asian and pear-european (both 2026-06-30) | Whether the 47 region refs on apple and the two pears satisfy R4. Currently classed on title only. PLA-579. |

Dropped as constructed by the session, not from any source:
`fruitsandnuts.ucdavis.edu/plum-rootstock-scion-selection` and
`fruitsandnuts.ucdavis.edu/apricot-scion-rootstock-selection`.

---

## 11. Owed, at park

- **Trevor:** rule PLA-565; rule plum `blocks_launch` now that section 8 is measured; send the
  four fetches.
- **claude.ai lane:** lime tristeza copy drafted from the lime slice against CH093 and CH092;
  apricot note held behind PLA-565 and PLA-566.
- **This lane:** stage the PLA-466 promote **only after PLA-565 is ruled**. Suite and harness by
  convention, positive control = the whole suite. Check `origin/main` first; a Plan C session is
  working in parallel.
