# Citation-integrity arc — hunt 1 of 32: `mid_south` / `uada_ext` (22 crops)

**Run:** 2026-07-30, against canonical `13d42f95` (verified: `shasum` == `LATEST.txt`; HEAD `b0c27a5`,
main, ahead of origin by 4, unpushed).
**Scope:** the cheapest of the 32 document hunts in
`docs/2026-07-29-citation-cleanup-sample-pass-outcome.md` §5 — `mid_south` / `uada_ext`,
22 crops, 143 bare-host pairs.
**Method:** every document fetched with `urllib` and read with `pypdf` or from raw HTML. No WebFetch
summary was used as evidence. Every load-bearing sentence was re-extracted from the raw bytes
before being relied on (§6).

---

## 0. Headline

**The hunt succeeded, and it was not mechanical.**

The premise was right — `mid_south` built a per-document citation vocabulary and left the fruit
crops on the institution root — but the reason the fruit crops were left behind is that **the
vocabulary the region built is a VEGETABLE vocabulary**. `uada_ext_spring_veg` and
`uada_ext_fall_veg` are vegetable planting-date tables; no fruit crop has a row in either. The
fruit documents were never located because they are a different publication set, and that set had
to be found from scratch. It exists, it is large, and it is good: **nine UAEX documents located and
read**, covering 18 of the 22 crops.

**Locating them found three data defects and one ruling question, not just three URLs.**

| verdict | crops | n |
|---|---|---|
| **CASE 1 — repointable** (document located AND contains the claim) | apple, apricot, cherry-sweet, mulberry\*, nectarine, pawpaw, peach, pear-asian, pear-european, persimmon, plum\*, pomegranate, strawberry (z8) | 13 |
| **CONTRADICTED** — document disagrees with the cell | **blueberry, fig, raspberry** | 3 |
| **RULING NEEDED** — document disagrees, but Trevor made an explicit prior call | **cherry-sour** | 1 |
| **DECLARED / UNVERIFIABLE** — no such document exists, and the crop already says so | oregano, rosemary, sage, thyme | 4 |
| **DIVERGENT** — source is real but not date-precise | elderberry | 1 |

\* partial: the planting claim is documented, the harvest window is not.

**One finding cuts across all 14 tree fruits:** UAEX publishes no bloom dates, so every
`bloom[0]` offset arm is an undocumented phenology model. That is a CASE 2 that repointing cannot
fix, and it is the single largest honest gap this hunt found.

---

## 1. The documents, located and read

None of these was recorded anywhere in the dataset before this session. All returned HTTP 200 to
plain `urllib` and were read directly.

| new id proposed | publication | url |
|---|---|---|
| `uada_ext_fruit_trees` | UAEX, Home Garden Fruit Trees in Arkansas | `https://www.uaex.uada.edu/yard-garden/fruits-nuts/fruit-trees.aspx` |
| `uada_ext_fsa6129` | UAEX FSA6129, Tree Fruit Cultivar Recommendations for Arkansas | `https://www.uaex.uada.edu/publications/pdf/FSA-6129.pdf` |
| `uada_ext_fsa6130` | UAEX FSA6130, Small Fruit Cultivar Recommendations for Arkansas (McWhirt, Clark) | `https://www.uaex.uada.edu/publications/pdf/FSA-6130.pdf` |
| `uada_ext_fsa6104` | UAEX FSA6104, Blueberry Production in the Home Garden (M. Elena Garcia) | `https://www.uaex.uada.edu/publications/PDF/FSA-6104.pdf` |
| `uada_ext_fsa6103` | UAEX FSA6103, Strawberry Production in the Home Garden | `https://www.uaex.uada.edu/publications/pdf/FSA-6103.pdf` |
| `uada_ext_fsa6107` | UAEX FSA6107, Raspberry Production in the Home Garden (Striegler) | `https://www.uaex.uada.edu/publications/PDF/FSA-6107.pdf` |
| `uada_ext_berries` | UAEX, Arkansas Berries — Home Garden | `https://www.uaex.uada.edu/yard-garden/fruits-nuts/berries.aspx` |
| `uada_ext_rd_pomegranate` | UAEX Reference Desk, Pomegranate | `https://www.uaex.uada.edu/yard-garden/in-the-garden/reference-desk/fruits/pomegranate.aspx` |
| `uada_ext_rd_mulberry` | UAEX Reference Desk, Mulberry | `https://www.uaex.uada.edu/yard-garden/in-the-garden/reference-desk/trees/mulberry.aspx` |

Also read and used as negative evidence: UAEX Plant of the Week — Elderberry; UAEX Herb Gardening
in Arkansas (`yard-garden/in-the-garden/herbs.aspx`).

**A correction to the sample-pass note.** It records plain `uada_ext` as carrying "the bare root
AND a pathed FSA-6002.pdf". Measured: the pathed FSA-6002 URL appears on **exactly 2 nodes**, both
`asparagus`, against **141** bare-root uses. FSA-6002 is an asparagus publication, not a general
one. So the one-id-two-URL violation is real but tiny, and it is not a fruit-crop issue at all.

---

## 2. The sentence that carries the whole tree-fruit set

`fruit-trees.aspx`, verbatim (re-extracted from raw HTML):

> **"Fruit trees other than figs, could be planted in the fall, but often the best variety
> availability will be in late winter."**

That single sentence does two things:

1. It **supports** `plant_out = "Dec - Feb (dormant, bare-root)"` across twelve tree fruits.
   December-through-February *is* late winter plus the tail of the fall option.
2. It **excludes fig by name**, and the page says so again explicitly:

> **"Fig trees should not be planted until early spring."**

The exception is stated in the very sentence that licenses the rule. That is the cleanest possible
adjudication: the same document, read once, both repoints twelve cells and condemns a thirteenth.

---

## 3. The three contradictions

### 3a. `blueberry` — the recommended type is inverted, and three documents say so

Our `mid_south` z7 cell (the **Ozark uplands**, NW Arkansas, frost zone D):

- `recommended_type: "rabbiteye"`
- `type_note_seasoned`: *"Rabbiteye is the University of Arkansas's top pick for most soils across
  the belt, and that covers the Ozark uplands… **Northern highbush is heat-stressed here and is not
  recommended.**"*

Three separate UAEX documents place the types the other way round:

| document | verbatim |
|---|---|
| FSA-6104 | *"The northern highbush type is **better adapted to the northern part of the state**… In southern Arkansas, southern highbush or rabbiteye varieties should be grown… northern highbush varieties can be grown at **higher elevations**, while southern highbush or rabbiteye varieties should be grown at **lower elevations** in central Arkansas."* |
| FSA-6130 | Section headers: **Northern Highbush (Northern and Central Ark.)** / Southern Highbush (Central and Southern Ark.) / **Rabbiteye (Central and Southern Ark.)** |
| `berries.aspx` | *"In Arkansas, **northern highbush blueberries are grown in the northern counties**, and rabbiteyes are grown in more central and southern areas."* |

`mid_south` z7 is precisely "the northern counties / higher elevations" — the region's own sourcing
note defines it as *"NW AR Ozarks (Fayetteville, the U of A chill station)"*. So the cell recommends
the type UAEX assigns to the **opposite** end of the state and explicitly rules out the type UAEX
recommends for that zone.

The chill band corroborates UAEX rather than the cell: z7 is `[1000, 1300]`, and FSA-6130 puts the
northern-highbush cultivars at 700-1200 hours — comfortably cleared. Nothing about z7 excludes
northern highbush.

**z8 is milder but not clean.** Central Arkansas is where rabbiteye legitimately belongs, so
`recommended_type: rabbiteye` is right there. But the z8 note also says *"northern highbush is too
heat-stressed to recommend here"*, and FSA-6130 lists Northern Highbush for **"Northern and Central
Ark."** — z8 is central. The categorical exclusion is wrong in both zones; the type assignment is
wrong only in z7.

**Severity: this is a variety-selection steer on a certified crop, and it is the kind a beginner
acts on once and lives with for fifteen years.** Not repointed — pointing this cell at FSA-6104
would make the contradiction visible on the page.

### 3b. `fig` — planted three months before the document allows

Both zones: `plant_out = "Dec - Feb (dormant plant)"`.

`fruit-trees.aspx`: *"Fig trees should not be planted until early spring."* And the sibling sentence
carves figs out of the fall/late-winter rule that every other tree fruit here rests on.

This is not a provenance nicety. Fig is the most cold-tender woody fruit on the `mid_south` roster;
a December planting in z7 is the failure mode the document is warning about. **Data defect, both
zones.**

### 3c. `raspberry` — same shape, different document

Both zones: `plant_out = "December to March"`.

FSA-6107, verbatim: *"**Planting should occur in the spring as soon as the soil can be properly
prepared.**"*

December and January are not spring. March is defensible; the first three months of the window are
not.

**Note the pattern across 3b and 3c:** the `mid_south` build applied one dormant-season
"Dec - Feb / December to March" woody-planting template across all woody fruit. UAEX endorses that
template for tree fruits and explicitly rejects it for **fig** and **raspberry**, the two crops on
this roster where it is wrong. One template, two documented exceptions, both missed.

---

## 4. The ruling question: `cherry-sour`

FSA-6129, verbatim:

> **"Apricots and Cherries** — Given the climate in Arkansas, both apricots and cherries trees can
> be grown but **will not reliably set fruit**. Both crops tend to bloom early and be exposed to
> frost or freeze damage during bloom. In the case of cherries, heavy rainfall common in our region
> during fruit ripening will result in fruit splitting prior to harvest."

Against our cells:

| crop | our `mid_south` suitability | verdict |
|---|---|---|
| apricot | `marginal` | **SUPPORTED** — repoint |
| cherry-sweet | `marginal` | **SUPPORTED** — repoint |
| **cherry-sour** | **`fruits_reliably`** | **contradicted on a plain reading** |

UAEX says "cherries" without qualification, gives **no cherry cultivar table at all** (unlike
apples, pears, peaches, nectarines), and its stated mechanisms — early bloom into frost, and rain
cracking at ripening — both apply to sour cherry.

**But this is Trevor's call, not mine.** `docs/reviews/notes/2026-07-20/mid_south_sources.md` §6
records the decision explicitly: *"Sour cherry stays `fruits_reliably`"*, carried from mid-Atlantic
on Trevor's 2026-07-20 ruling, where NC State steers zone-8 growers **toward** sour cherry
specifically. So we have two land-grant institutions pointing opposite ways, and an existing ruling
on the record. Surfaced, not changed.

---

## 5. What the CASE 1 repoints rest on

Recorded so the next pass does not re-hunt. Every quote below was read from the document, not
inferred from its title.

| crop | claim | document | verbatim support |
|---|---|---|---|
| apple | `plant_out` Dec-Feb | `fruit_trees` | "other than figs, could be planted in the fall… best variety availability… late winter" |
| apple | `harvest` Aug 13 - Oct 4 | FSA-6129 | cultivar seasons **Early (July - Aug)**, **Mid (Sept)**, **Late (Oct)** |
| apple | `fruits_reliably` | FSA-6129 | "Apples will generally be more successful in the northern part of Arkansas" (strong for z7, soft for z8) |
| apricot | `marginal` | FSA-6129 | "will not reliably set fruit… bloom early… frost or freeze damage" |
| cherry-sweet | `marginal` | FSA-6129 | same sentence |
| nectarine | `harvest` Jun 25 - Aug 20 | FSA-6129 | "Ozark Mango… **Typically harvested around July 1 in Clarksville AR**"; the "days before Elberta" ladder spans the rest |
| peach | chill / `fruits_reliably` | FSA-6129 | ">1,000 hours… more regular success… in central and northern Arkansas"; "<750 hours should be avoided" |
| pear-european | cultivars, incl. **Magness** | FSA-6129 | full Magness entry: "Greenish-yellow… **Does not produce good pollen**. High fire blight resistance" — **closes `pear_european_magness_uncited`** |
| pear-asian | cultivars | FSA-6129 | Asian Pears: Chojuro, Hosui, Shinseiki, 20th Century (Nijisseiki) |
| pawpaw | `harvest` Sep 2 - Oct 7 | `fruit_trees` | "**Pawpaw fruit ripens between mid-August and into October**" |
| pawpaw | pollination | `fruit_trees` | "need two different trees… bees show no interest… Flies and beetles are the pollinators" |
| persimmon | `harvest` Sep 6 - Oct 18 | `fruit_trees` | "**Oriental persimmons fruit ripens from late August until early December**" |
| persimmon | self-fruitful default | `fruit_trees` | "Fuyu-Gaki persimmon is the most widely planted self-fruitful cultivar in the world" |
| pomegranate | `marginal` | Reference Desk | "with our humid summers, **rarely did we see great fruit production**… a new series of Russian pomegranates have shown good results with fruiting and winter hardiness" |
| mulberry | `fruits_reliably` | Reference Desk | "The fruit when totally ripe is edible for human consumption" (harvest **dates** not documented) |
| plum | `plant_out` only | `fruit_trees` | the late-winter sentence; **FSA-6129 has no plum section at all** — zero mentions — so plum's harvest window stays undocumented |
| strawberry z8 | `plant_out` Sep 15 - Oct 5 | `berries` | "planted in the fall on raised beds then picked one time the following spring" |
| strawberry z8 | `harvest` late Apr - early Jun | `berries` | "**the bright red, flavorful fruit are picked from April thru June in our state**" |

**Strawberry z7 is the odd one out and is left alone.** It plants in **spring** (`Apr 1 - Apr 22`)
while z8 plants in **fall**. UAEX describes only fall planting for Arkansas, for both the annual
plasticulture and matted-row systems. The document does not forbid spring planting, so this is
DIVERGENT rather than contradicted — but the two zones of one region using opposite planting
seasons is a modeling question worth a look at the next strawberry pass.

---

## 6. The cross-cutting gap: nobody publishes bloom dates

Every one of the 14 tree fruits carries a `bloom[0]` arm of the form
`{from: last_frost, offset_days: -7…+21, window_days: 21}`, cited SOLE to bare `uada_ext`.

**No UAEX document read this session publishes a bloom date for any fruit crop.** FSA-6129 discusses
bloom only as a risk ("tend to bloom early", "Late blooming", "blooms relatively late") and never as
a date or an offset. `fruit-trees.aspx` gives ripening windows but no bloom windows.

This is the `harvest-start-is-not-a-published-datum` shape again, one field over: the literature
produces *relative* bloom language and *absolute* frost dates, and our model turns them into an
offset. That offset is defensible and internally consistent, but it is a derivation, and no
repointing can make it a quotation. It should be **declared**, exactly as the herbs declare theirs.

---

## 7. The herbs: correctly declared already, and confirmed

`oregano`, `rosemary`, `sage`, `thyme` all carry an accepted finding stating the windows are modeled
"not from a [crop]-specific per-region planting chart (none found for all 10 regions)".

Checked rather than assumed: UAEX's herb page (`yard-garden/in-the-garden/herbs.aspx`) carries
"Table 2. Growing Requirements, Propagation and Uses of Biennial and Perennial Herbs" with rows for
all four crops — but its columns are **height, spacing, light**, with **no planting-date column**.
The findings are accurate. These four are the DECLARED class from §2c of the sample-pass doc: an
honest admission of derivation, not the `unr_fs0261` defect, and **not work**.

(The herb table was deliberately *not* parsed for values — it is an HTML data table, the exact shape
that column-shifts under naive extraction. Only its column headings were used.)

---

## 8. Method notes / traps that fired

- **The "already-built vocabulary" premise was half right.** The vocabulary existed; it just did not
  cover fruit. Assuming the hunt was clerical would have produced a mass repoint at
  `uada_ext_spring_veg`, a vegetable table with no row for any of these crops — manufacturing 22
  `unr_fs0261`-shaped defects in one commit.
- **Locating the document is still not supporting the claim.** FSA-6129 is exactly the document
  `uada_ext` should cite for `mid_south` tree fruit, and it contains **no plum section and no bloom
  dates**. Two of its most obvious uses are not there.
- **Every load-bearing sentence was re-extracted from raw bytes** before being used, because the
  flattened text could in principle have joined two paragraphs. All seven survived (§0 method).
- **Extension outreach pages are T1 here.** The Reference Desk and Plant-of-the-Week pages carry
  `source_class: university_extension`, which the catalog already bands at T1 — per the
  `source-catalog-is-the-admission-authority` lesson, they are not to be discarded as informal.

---

## 9. Disposition

**Nothing was repointed in the same change as a value.** Split into:

1. **Citation-only:** the 13 CASE 1 crops repoint to the nine new catalog ids. No value moves.
2. **Documentation-only:** findings for `blueberry`, `fig`, `raspberry` (contradictions),
   `cherry-sour` (ruling needed), and the 14-crop bloom-derivation gap.
3. **Trevor's queue:** the blueberry type inversion and the fig/raspberry planting windows are
   **data** changes and are not made here.

**Arc position after this hunt:** 1 of 32 document hunts closed, 22 of 170 decisions adjudicated.
The next-cheapest is `mid_atlantic`/`ncsu_ext` (14 crops), and the sample-pass doc already warns it
is the harder half — its sourcing note names zero URLs.


---

## 10. POSTSCRIPT -- the scan built after this hunt audited this hunt

`tools/doc_mentions_crop_scan.py` was built immediately after this pass, to find the defect class
the `mid_atlantic` hunt exposed: a real, live, correctly titled document cited for a claim it does
not contain (`vce_426_331`, catalogued as "Mid-Atlantic regional coverage", is actually
*Virginia's Home Garden **VEGETABLE** Planting Guide*). Run blind over the roster it independently
rediscovered both `unr_fs0261` and `vce_426_331` -- and it also flagged **this document's own
repoint**.

**Measured on `fruit-trees.aspx`, word-boundary matched:**

| named | not named |
|---|---|
| apple 16, pear 13, peach 14, nectarine 10, plum 4, persimmon 8, pawpaw 8, fig 7, cherry 1 | **apricot 0, mulberry 0, pomegranate 0** |

So nine of the twelve crops repointed in §5 are named outright. **Apricot, mulberry and
pomegranate are covered only by the page's generic sentence** -- *"Fruit trees other than figs,
could be planted in the fall…"* -- which is a statement about fruit trees as a class. All three
are deciduous fruit trees, so the citation is defensible and is **NOT reverted**; but it is an
inference from a general statement rather than a crop-specific mention, and that is weaker than
the other nine.

Recorded as `mid_south_fruit_trees_citation_generic_basis` on those three crops rather than left
implicit. **The generalizable point: the check earned its keep on its first run by auditing
careful hand work from the same day and finding the soft spot in it.**
