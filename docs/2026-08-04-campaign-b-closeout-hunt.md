# Campaign B closeout — fig, strawberry, apple, elderberry, broad-beans-fava

**Run:** 2026-08-04. **Pre-state canonical:** `370806b5…`, HEAD `bcb2b81`.
**Scope:** everything `tools/campaign_b_reprice.py` still reported open after the mid_atlantic
hunt — 2 decisions needing document work plus 3 region-anchor-only decisions, 18 SOLE bare nodes.
**Companion:** `docs/2026-08-03-mid-atlantic-ncsu-ext-citation-hunt.md`.

**Outcome: campaign B reads 0 open decisions.** 4 nodes repointed, 14 held bare with per-crop
stated reasons, 5 findings filed, 1 catalog id minted.

---

## 1. Documents read — 12

All fetched from **raw bytes** (`urllib` + the `doc_mentions_crop_scan` extractor), never through
a markdown table parse. Absence below is scoped to exactly this list.

| # | document | for | verdict |
|---|---|---|---|
| 1 | UAEX FCS812A, Arkansas Local Produce Fruit & Vegetable Harvest Calendars | fig | read — **no fig row**, and see the trap in §2 |
| 2 | UAEX Yard & Garden fig reference desk | fig | read |
| 3 | UAEX White County, "Fig Varieties that Grow Well in AR" | fig | read |
| 4 | UAEX Summer Fruits | fig, strawberry | read |
| 5 | UAEX news, "Fall planting strawberries? When is too late, and too early" (2022-05-24) | strawberry | read — **the find** |
| 6 | UAEX FSA-6130, Small Fruit Cultivar Recommendations | strawberry | read — **not a planting-date document** |
| 7 | "An Introductory Guide to Strawberry Plasticulture", Poling | strawberry | read — **rejected, see §3** |
| 8 | UAEX Commercial Strawberry Production in Arkansas | strawberry | read — no dates |
| 9 | UAEX Yard & Garden berries | elderberry | read — **0 elderberry mentions** |
| 10 | UAEX Plant of the Week, "Elderberry" (*Sambucus canadensis*) | elderberry | read |
| 11 | NC State Plant Toolbox, *Vicia faba* | fava | read — **backs the heat_pause** |
| 12 | VCE SPES-590, "Faba Bean: A Multipurpose Specialty Crop for the Mid-Atlantic USA" | fava | read — corroborates |

Plus two re-word-searched from the mid_atlantic hunt: NC State's central North Carolina planting
calendar and VCE 426-331, both for fava.

---

## 2. fig — CASE 2, on its own evidence

Hunt 1's stated exclusion list named apricot, cherry, mulberry, peach, pear, plum and pomegranate
but **not fig**, so this was an unread question rather than a settled absence. Read out, it reaches
the same verdict for a slightly different reason.

- **Arkansas's own fruit harvest calendar does not list fig.** FCS812A carries twelve fruits —
  apples, blackberries, blueberries, cantaloupe, grapes, muscadines, nectarines, peaches, plums,
  raspberries, strawberries, watermelon. Fig is absent.
- The other three documents give only **cultivar ripening order and crop structure**: "Celeste …
  ripens usually before Brown Turkey"; "Brown Turkey (also called Texas Everbearing) ripens a few
  weeks after Celeste … bears for a relatively long period of time"; the breba crop "rarely"
  persists in Arkansas, so the current-season crop "is predominantly what we harvest". That is a
  relative ladder with no anchor date — the same shape hunt 1 recorded for peach's "days before
  Elberta".

**A trap recorded for the next reader.** FCS812A's month columns are **graphical bars with no text
layer**. A text extraction returns the crop names and *no months at all*. It cannot support a month
claim for any crop, including the twelve it does list. Anyone who greps it for a harvest window
will conclude, wrongly, that Arkansas publishes no harvest months for strawberries either.

---

## 3. strawberry — the find, and why it is filed rather than fixed

The block's last live claim arm was z8 `plant_out`, **"Sep 15 - Oct 5"**. UAEX's own three-year
fall-planting-date study places its **tail inside the treatment it measured as costly**:

> plots planted on what was considered "on time" — **the last two weeks of September** — and then
> a week later in **the first week of October** … the late-planted treatment **reduced strawberry
> yield 15-35 percent** depending on variety and test year.

Sep 15–30 matches "on time". **Oct 1–5 does not.** A row cover, the study adds, "will never make up
for the loss of daylight … even in as short of a one-week delay." A follow-on study begun in 2021
also indicates planting *too early* can reduce yield, so the early bound is not settled either.

**Not changed here, for two reasons.** It is consumer-facing. And it is **coupled** to the still-open
`strawberry_mid_south_plasticulture_home_garden_tension`: FSA6103 says this annual system "is not
recommended for home garden strawberry production at this time", so trimming the window on the
strength of *commercial* plasticulture research would deepen a commitment to a system the
home-garden fact sheet disrecommends, while that question is unresolved. **The two should be ruled
together.**

### 3a. The second host-vs-author trap in two days

The only document on the UAEX server carrying a dated plasticulture calendar is **"An Introductory
Guide to Strawberry Plasticulture" by E. Barclay Poling, Department of Horticultural Science, NC
State**. Hosted by UAEX, authored elsewhere, and calendared for North Carolina — "Third week of
September, set your Sweet Charlies first"; "by the time growers in the southeastern Coastal Plain
plant in mid-October". Citing it as `uada_ext` would credit the University of Arkansas with NC
State's recommendations. It is also commercial (methyl bromide fumigation, 15,000–17,500 plants per
acre, deer fencing), not home-garden guidance. **The promote bans its URL structurally** so a later
pass cannot "find" it and repoint.

A first cut of that guard banned any URL containing `strawberry-plasticulture` and immediately
flagged `content.ces.ncsu.edu/strawberry-plasticulture-production-guide-for-north-carolina` — NC
State's *own* guide, correctly cited as `ncsu_ext` on mid_atlantic crops. The defect is a UAEX host
lending its name to NC State authorship, not the word. Narrowed to the UAEX-hosted PDF.

---

## 4. The three region-anchor decisions

These hold no claim, so the question is "which document represents this region's planting model."

- **apple** — CLEAN, and the only pure repoint in the block. Its `plantings[]` container was the
  last bare node, while its own `plant_out` arm **and both zone cells already cite**
  `uada_ext_fruit_trees`. Repointing the container to the document its own children carry is
  bookkeeping, not a claim.
- **elderberry** — CASE 2. UAEX's home-garden berry guide, the document backing every other
  mid_south berry, **does not mention elderberry at all** (0 hits for "elderberry" or "Sambucus").
  The Plant of the Week article covers the right taxon (*Sambucus canadensis*, matching ours) but
  publishes no planting date and only seasons otherwise: flowers "in midsummer", berries "in late
  summer". Our arms say bloom **May and June** — earlier than "midsummer" — and plant_out March and
  April, which the document does not address. Filed `open`.
- **broad-beans-fava** — SPLIT, and the split is the point. The **heat_pause** claim is directly
  supported and repoints; the **zone cells** are not and stay bare.

### 4a. What the fava documents actually say

The NC State Plant Toolbox entry for *Vicia faba* states the heat claim outright: "temperatures in
the 60's are ideal. In locations where the daytime temperatures exceed the mid 70's may result in
poor yeild" (*sic* — the source misspells "yield"). VCE SPES-590 corroborates it for this exact
geography: "temperatures ranging from 60-65 °F are the best for its growth, faba bean can grow at
temperatures ranging from 45-75 °F". Our cells say the crop "grows best around 60 to 65°F and sets
pods poorly once daytime temperatures climb past" the mid-70s — matched on both ends.

The **zone cells** are a different question. **Neither mid_atlantic vegetable calendar lists this
crop**: NC State's central North Carolina calendar has rows for beans lima/bush, lima/pole,
snap/bush and snap/pole; VCE 426-331 has lima, pole and snap. Zero occurrences of "fava", "broad
bean" or "faba" in either. SPES-590 does not fill the gap — it is a cropping-systems research
publication about faba bean as a winter cover and seed crop, reporting variety trials, not a
planting calendar.

---

## 5. Checked, and NOT a defect

Elderberry's mid_south planting arms are **month-name strings** (`["March","April"]`) rather than
the offset objects the rest of the roster uses, so they carry no per-arm citation. That looks like a
defect and is not. A census over the full canonical found **420 arms in this shape across 8 crops
and all 16 regions** — blackberry, blueberry, elderberry, raspberry, lavender, oregano, rosemary,
sage, thyme. It is a supported variant, and for those crops **all citation necessarily lives on the
container**, which is exactly why they price as region-anchor-only.

Measured before filing. "These arms are uncited" would have been a fabricated finding.

---

## 6. Findings filed

| crop | id | status |
|---|---|---|
| fig | `mid_south_fig_harvest_undocumented` | accepted_modeled |
| strawberry | `mid_south_strawberry_z8_plant_out_late_tail` | **open** |
| strawberry | `mid_south_strawberry_plasticulture_guide_is_ncsu_not_uaex` | accepted |
| elderberry | `mid_south_elderberry_no_uaex_planting_model` | **open** |
| broad-beans-fava | `mid_atlantic_fava_absent_from_vegetable_calendars` | accepted_modeled |

---

## 7. Where campaign B stands

`python3 tools/campaign_b_reprice.py` reports **0 of 32 decisions** needing document work and **0**
region-anchor only. The block is closed.

**Not closed: the decisions.** Eight findings across the two hunts are `open` and need rulings, six
of them consumer-facing:

1. `mid_atlantic_cherry_sweet_sour_steer_attribution_unsupported` — a credit NC State does not make, in both registers
2. `mid_south_strawberry_z8_plant_out_late_tail` — **rule with #3**
3. `strawberry_mid_south_plasticulture_home_garden_tension` — **rule with #2**
4. `mid_atlantic_apricot_harvest_divergent`
5. `mid_atlantic_apricot_coastal_plain_suitability_tension`
6. `mid_atlantic_cherry_coastal_plain_suitability_tension` (both cherries)
7. `mid_atlantic_pomegranate_bloom_window_narrower_than_source`
8. `mid_south_elderberry_no_uaex_planting_model`

**29 nodes remain on a bare host by design** across both hunts. `bare_host_scan` will keep
reporting them; each now carries a filed reason why repointing would be wrong.

**Next:** campaign C (arid + Texas, 7 hunts, AZ1005's rotated grid and NMSU CR457B's missing window
as documented traps) and campaign D (the tail, 11 hunts but 7 of them lemon — invert the unit and
read lemon's citations end to end). **Re-price both before hunting.** That step has paid off every
single time it has been run, including twice today.
