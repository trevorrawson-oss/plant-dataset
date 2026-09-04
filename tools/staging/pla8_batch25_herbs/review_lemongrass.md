# PLA-8 BATCH 25 -- INDEPENDENT SOURCE-TRUTH REVIEW: LEMONGRASS

Reviewer pass date: 2026-09-04. Independent of the authoring pass and of the record pass.
No data file changed. Canonical read READ-ONLY.

Reviewed artifact: `tools/staging/pla8_batch25_herbs/out_lemongrass.json`,
current sha256 `0da371ca7251f94841c3b171f8435966343860581510f3e4dd74f9ac6efd06c0`.

**NOTE: the file changed under me twice during this review.** I first read it at an earlier sha, then
graded at `0df357d352b28b92048cd34bb11d4a3d58f2a9ad35a4ce735d269041b6902f8f` (63,477 bytes, mtime
12:53:40), and it moved again to the sha above before I finished writing. The only content difference
I could detect between the first two was `pests[0].control_ladder[3].note_beginner`. Before filing, I
re-verified against the **current** sha that all four MUST-FIX items are still present and unchanged
("two weeks clear of an oil spray" present, "30 days" absent, "two leaf diseases both need" present,
"Thailand" absent, "a neem-oil product" present), and that the structural counts are unchanged. So
every grade below applies to the current file. Anyone applying this review should still re-confirm the
sha, because the file is evidently still in flight.

Scope: 4 entries, 11 rungs, 25 declared `field_corrections` (5 / 8 / 8 / 4), 6 refusals,
7 `unreachable_claims`, 30 `notes_to_orchestrator`. One canonical entry (`pests[0]`) retired.

I also confirmed the canonical has **not** been promoted for this crop yet: `lemongrass`'s five live
problem entries still carry no `id`, no `control_ladder`, and the coarse `pest` / `disease` types.
(`crops_data_final.json` and `tools/problem_id_registry.json` do show as modified in the working tree
from concurrent batch-25 work on other crops. I changed no file except this report.)

## Documents I fetched and read myself this session

| key | document | how read | outcome |
|---|---|---|---|
| `uhawaii_ctahr` | UH-CTAHR **PD-57 "Rust of Lemongrass"**, Scot Nelson, Plant Disease, Nov. 2008 | downloaded and read as **page images, all 4 pages** (no text layer) | full read, every rust quote below is from my own read |
| `usu_ext` | USU Extension, "How to Grow Lemongrass in Your Garden", Linse & Drost | WebFetch | full read incl. both tables |
| `ucanr_ext_spider_mites` | UC IPM Pest Notes 7405, Spider Mites | WebFetch x2 (targeted) | full read |
| `uiuc_ext` | U. Illinois Extension, "Lemon grass" | WebFetch | full read |
| `uc_mg` (Santa Clara) | UC MG Santa Clara County, "Lemongrass" | WebFetch | full read |
| `uc_mg` (Solano) | UC MG Solano County, "…Repelling summer mosquitoes with Citronella" | WebFetch | full read, the refuting document |
| `uwi_hort` | Wisconsin Horticulture, "Lemongrass", Susan Mahr | WebFetch | full read |
| `ncsu_ext` | NC State Plant Toolbox, *Cymbopogon citratus* | WebFetch | full read |
| (journal) | Ploetz et al. 2014, *Plant Disease* 98:156, Florida first report | abstract via PubMed/APS metadata | **decisive**, see FIX-B2 evidence |
| (journal) | *Curvularia* leaf-blight reports (Brazil / China / India / Guatemala) | search metadata | confirms the genus, four different species |

I also computed, rather than accepted, every roster count the record and the output assert. All of
them are exactly right (see RECORD-LEVEL FINDINGS, R1).

---

# 1. THE RETIRED ENTRY AND ITS RESIDUE

## 1a. The retirement itself: CORRECT

The retirement of `pests[0]` "Generally pest-resistant (aromatic-oil deterrence)" HOLDS. I confirmed
the two halves independently:

* The **absence half** is real and triple-anchored. `usu_ext`: "Lemongrass is generally free of pests
  and diseases when grown correctly." `uwi_hort`: "Lemongrass has essentially no pest problems in the
  Midwest." `ncsu_ext` Resistance To Challenges, exact value: "Deer, Heat, Humidity, Insect Pests,
  Poor Soil, Slugs".
* The **mechanism half** is carried by none of them and is refuted. UC MG Solano, verbatim:
  "just growing it may not repel one 'Skeetter', since the oil in the plant has the repellent
  properties, and it must be extracted to use." Every oil sentence in the three cited documents is a
  **product** claim: `usu_ext` "It is also used as an effective, non-toxic insect repellent" (of
  extracted oil, in a uses paragraph nowhere near the pest section); `uwi_hort`'s only repellency
  sentence is about *C. nardus* commercial citronella oil "used in soaps, as a mosquito repellent in
  insect sprays and candles"; `ncsu_ext` says only "The plant oils are used for perfumes and herbal
  medicines."
* Computed independently: 912 problem entries, 823 laddered on 101 crops, and zero laddered entry is
  an absence assertion. The population-of-one claim holds.

## 1b. THE DISPOSITION IS RIGHT ON WHAT IT COVERS AND **INCOMPLETE BY THREE FIELDS**

I walked every string in the `lemongrass` record myself. The author's A0 says "four of the twelve
fields", "EIGHT survive", "five `companions.*` fields". **All three counts are wrong.**

Here is the complete field-by-field walk. "MISSED" means the field carries the claim and appears
nowhere in A0-A9.

### Retired with `pests[0]` (4) -- author correct

| field | live text | note |
|---|---|---|
| `pests[0].name` | "Generally pest-resistant (aromatic-oil deterrence)" | gone |
| `pests[0].symptoms_seasoned` | "an effect attributed to the citral-rich essential oils in its foliage that repel many insects" | gone |
| `pests[0].symptoms_beginner` | "Its own lemony oils keep most bugs away, so outdoor plants usually look clean." | gone |
| `pests[0].cause_beginner` | "Lemongrass makes lemony oils that many insects dislike, so it is naturally left alone." | gone |

(`pests[0].cause_seasoned` "The plant's aromatic oils (notably citral) are used in insect-repellent
products" is a **product** claim, correctly anchored to USU. It is the one field a prior pass fixed.
It is not part of this class and its retirement costs nothing.)

### Survive, assert-as-fact (2) -- author correct, A1/A2

| field | live text |
|---|---|
| `description_seasoned` | "Because its own essential oils repel many insects, it is notably free of pest problems" |
| `description_beginner` | "is rarely bothered by insects, since its own lemony oils keep many pests away" |

### Survive, companions -- **EIGHT fields, not five**

| field | live text | author |
|---|---|---|
| `companions.good_beginner_seasoned[0].why_seasoned` | "its strong citrus oils are a traditional insect deterrent" | A3 -- keep. AGREED |
| `companions.good_beginner_seasoned[0].why_beginner` | "Lemongrass's strong lemony scent is a traditional way to help keep some insects away." | **MISSED** |
| `companions.good_beginner_seasoned[0].provenance.reason` | "Lemongrass essential oils (citral, **geraniol**) are well documented as insect repellents … plus **a real repellent mechanism**" | A5 -- change. AGREED, see 1c |
| `companions.good_beginner_seasoned[1].why_seasoned` | "The grass's aromatic oils are a traditional pest deterrent for the planting." | A4 -- keep. AGREED |
| `companions.good_beginner_seasoned[1].why_beginner` | "The grass's lemony scent **may help** keep some bugs off." | **MISSED** |
| `companions.good_beginner_seasoned[1].provenance.reason` | "lemongrass's **documented aromatic-oil repellency** … **a real mechanism**" | A6 -- change. AGREED |
| `companions.note_seasoned` | "its essential oils (rich in citral) are **documented insect repellents**" | A7 -- change one clause. AGREED |
| `companions.note_beginner` | "its lemony scent is a **traditional** way to discourage some insects" | **MISSED** |

The three MISSED fields are all **beginner register**. Two of them (`[0].why_beginner`,
`note_beginner`) are hedged with "traditional" and one (`[1].why_beginner`) with "may help", so on
the author's own A3/A4 standard they are probably KEEP -- but that verdict was never reached, and
A7 changes `note_seasoned` while leaving its beginner twin unexamined, which will ship a register
pair where the seasoned side says "extracted lemongrass oil is used in insect-repellent products"
and the beginner side still says "its lemony scent is a traditional way to discourage some insects".
That pair must be adjudicated together, not left to fall out.

Corrected counts: **14 fields carried the claim, 4 retire, 10 survive** (2 description + 8
companions), plus `container_notes.overwintering.approach_seasoned` at A9 as a separate inference.

### `varieties.*` -- A8's "DO NOT TOUCH" is over-broad on two of three fields

* `varieties.note_seasoned` -- "citronella grass … is grown for repellent **oil** and ornament".
  CLEAN. A8 correct.
* `varieties.note_beginner` -- "a lookalike relative grown to make citronella oil **and to repel
  bugs**, not for eating." The second clause is the growing plant repelling bugs, in beginner
  register, on the exact species the Solano document is about.
* `varieties.recommended[2].note` -- "grown for citronella oil and as **an ornamental
  insect-repellent plant**." Same. `uwi_hort` says only that *C. nardus* is "the source of commercial
  citronella oil, which is used in soaps, as a mosquito repellent in insect sprays and candles" -- a
  product claim. It does not say the plant is grown as an insect-repellent ornamental, and the
  "mosquito plant" marketing that phrase reflects is precisely what Solano refutes.

These are softer than the `description_*` assertions and they are correctly scoped to a different
species, so I do not grade them WRONG. But "DO NOT TOUCH … These fields were already right" is not
supportable for the two beginner-facing ones. **Recommend: soften both to the oil/product framing
that `note_seasoned` already uses.**

### A9 `container_notes.overwintering.approach_seasoned` -- VERIFIED and complete

Live: "cut the plant back hard (to roughly 4 to 6 inches, **which also sheds pests**)". Confirmed. I
also checked `approach_beginner`: "cut it back to a few inches" -- carries no pest claim, so the
register pair needs only the one edit A9 proposes. A9 is correct and complete.

## 1c. THE GERANIOL CLAIM: **VERIFIED. IT IS LIVE.**

This was flagged as the one that matters, so I checked it directly against the canonical rather than
against the record's reading.

`companions.good_beginner_seasoned[0].provenance.reason`, live, verbatim:

> "Lemongrass essential oils (citral, **geraniol**) are well documented as insect repellents, and it
> is a common companion-planting recommendation for warm-season vegetable beds, but I found no
> Tier-1 extension trial measuring a lemongrass companion effect on tomato. Labeled traditional/low:
> sound shared-conditions rationale plus **a real repellent mechanism**, but no crop-specific
> measurement on this pairing."

`verification_status.verification_log_ref`, batch-2 wave-4, cert-dated 2026-07-06, verbatim:

> "softened the pests[0] repellent line -- dropped the unsupported 'geraniol' … (full-file scan
> clean; …)"

**Both halves of A5 confirmed.** `geraniol` survived eight weeks and one asserted full-file scan, in
a provenance justification -- which is exactly where a later pass goes looking for the warrant. This
is the `correct-every-field-carrying-an-attribution` pattern recurring on the same crop, same claim.
The C8 append-only correction is owed and its wording is right, except that its enumeration inherits
the undercount (see FIX-A1).

## 1d. WHERE THE SOURCED ABSENCE SHOULD LIVE -- A10 is CORRECT, A1 is not

A10's recommendation (description_* only, with "when grown correctly" and "in the Midwest" restored,
never as a `pests[]` entry) is right and I endorse it without reservation. Both qualifiers are in the
documents verbatim and both are stripped in the live record.

**But A1's proposed replacement sentence carries a defect this same file is elsewhere removing.** A1
proposes to keep, verbatim: "Rust and leaf blight are the diseases to watch **in warm, humid, crowded
plantings**". The file's own `lemongrass-leaf-blight` `cause_seasoned` correction says there is "no
published cause or weather driver" for leaf blight, and its `prevention_seasoned` `why` calls warm/
humid/crowded "rust's management written over a disease with no published epidemiology". A1 must not
re-assert it. Suggested: "Rust is the disease to watch in warm, humid, crowded plantings; leaf blight
also occurs, though no source publishes what favors it."

A11's citation caution (the `uc_mg` key already points at Santa Clara on the root rot entry, so
Solano cannot share it) is correct and well spotted; I verified the collision.

---

# 2. LEMONGRASS RUST -- `lemongrass-rust`, type `fungal`, severity `medium`

Anchor: PD-57, read by me as page images, all four pages. Every quotation below is from that read.

## 2a. The two defects the batch was supposed to fix

**COPPER: FIXED. Verified.** No occurrence of copper, sulfur, chlorothalonil, mancozeb or any
fungicide recommendation survives anywhere in the rust entry. The replacement states PD-57's own
fact, with PD-57's own caveat and PD-57's own region scope. PD-57, verbatim:

> "There is only one fungicide product registered for use on lemongrass rust in Hawai'i, Trilogy
> (Table 1). There is no published research in Hawai'i evaluating this product for controlling
> lemongrass rust."

The beginner replacement -- "only one product is registered for this disease **in Hawaii**, and CTAHR
says even that one has not been tested there" -- is correctly region-scoped and does not become a
statement about a mainland reader's product options. That is brief defect class 4 handled correctly.

**MIS-ANCHORED SYMPTOM PROSE: FIXED, and the diagnosis is now independently proven.** PD-57,
verbatim:

> "Initial symptoms are tiny, light yellow spots that develop into brown and elongated, stripe-like,
> brown lesions that coincide with leaf veins and develop on both sides of the leaf. Lesions on the
> lower leaf surface erupt and develop dark, cinnamon-brown uredinial pustules. Lesion development
> can be substantial, with coalescing lesions forming large leaf spots or blights and causing
> premature death of leaves."
> "The rust disease is normally not fatal to lemongrass plants, even though defoliation may be
> severe."

The new `symptoms_seasoned` tracks that sentence for sentence. HOLDS.

I then confirmed the *source* of the old prose, which the record only inferred. The Ploetz et al.
2014 *Plant Disease* 98:156 abstract, as returned by PubMed/APS metadata:

> "symptoms beginning as **small chlorotic flecks on both leaf surfaces that became crimson and
> enlarged to streaks** approximately 1 cm in length. On the abaxial side of leaves, **erumpent
> streaks ruptured to produce pustules** containing urediniospores, and eventually, streaks coalesced
> to produce **large patches of tan to purplish necrotic tissue**."

Live canonical `diseases[0].symptoms_seasoned`: "Small chlorotic (yellow) flecks appear on both leaf
surfaces and enlarge into reddish to crimson streaks; on the leaf underside these rupture into
powdery orange-brown pustules … large patches of tan to purplish dead tissue". **That is the journal
abstract, credited to CTAHR.** The correction is fully warranted.

## 2b. Rung-by-rung

| # | method | grade | evidence |
|---|---|---|---|
| 1 | `certified_clean_stock` | **HOLDS** | PD-57 bullet: "Do not purchase or distribute rusted plants." Note is verbatim-faithful ("not to buy or pass on rusted plants"). Method fit is good: `certified_clean_stock` best_use is "Problems that travel in the planting material itself … Set once, at purchase or propagation", and lemongrass moves as living divisions and rooted stalks. |
| 2 | `airflow_spacing` | **HOLDS** (one arithmetic nit, FIX-B5) | Three PD-57 sentences carry it: "Plant lemongrass in well drained soils in a relatively dry or well ventilated area to minimize the time of leaf wetness after rainfall"; "Keep weeds under control to reduce relative humidity in the lemongrass plant canopy"; "avoid planting large numbers of lemongrass plants close to one another". The stated mechanism ("spores land on wet or moist lemongrass leaves and may infect them during periods of very high relative humidity") is PD-57's own. |
| 3 | `water_at_the_base` | **HOLDS** | PD-57: "Minimize overhead irrigation; lemongrass grows well in dry areas" and "Spores (mainly urediniospores) are dispersed by wind, splashing rain, or irrigation water." Corroborated independently by `usu_ext`: "Water lemongrass by hand or use flood irrigation rather than irrigate with sprinklers." The note's own stated limit (wind and rainfall sit outside it) is honest and correct. |
| 4 | `garden_sanitation` | **HOLDS** | PD-57: "Periodically prune, cut back, or thin out diseased lemongrass plants so that disease-free re-growth can occur; destroy diseased plant material (do not use it around pruned lemongrass plants as mulch)" and "Spores may survive on infected or fallen lemongrass leaves." Both halves used, including the mulch warning, which is the sharpest practical sentence in the document and was missing from the record entirely. |

**Tier monotonicity and gate coherence:** all four are `cultural`; `certified_clean_stock` and
`airflow_spacing` and `water_at_the_base` all intersect `TYPE_TARGETS['fungal']` =
{fungal_foliar, fungal_soilborne, disease_general}; `garden_sanitation` is `any`. Legal. I ran
`tools/staging/pla8_batch25_herbs/validate_out.py lemongrass`: **"OK: lemongrass validates. 1 pests +
3 diseases, 11 rungs."**

## 2c. THE ADJUDICATION ASKED FOR: four cultural rungs, no chemistry -- **CORRECT**

I verified the mechanism the author relies on rather than taking it:

* `neem_oil.applies_to` = `['insect_soft_bodied', 'insect_general']`. `TYPE_TARGETS['fungal']` =
  `{fungal_foliar, fungal_soilborne, disease_general}`. Intersection **empty**. `control_ladder_gate`
  would reject it. **Confirmed: the one product PD-57 names has no reachable rung.**
* `copper_fungicide.applies_to` includes `fungal_foliar`, so it WOULD have passed. The refusal was a
  live choice against an available, gate-legal rung, not a mechanical outcome. That is the right
  call and the right reason ("substituting different chemistry is precisely the defect this pass
  exists to fix").
* `biofungicide.applies_to` = `['fungal_foliar']`, also gate-legal, also correctly refused: its own
  text is "Bacterial biofungicides, the Bacillus-based products", and PD-57's *Darluca* is a
  mycoparasite that is neither Bacillus nor purchasable, and PD-57 hedges it explicitly: "It is
  unknown if this mycoparasite exists in Hawai'i, nor has the extent of the mycoparasitism and
  whether or not it provides effective disease control been determined."
* The other three unreachable claims check out. `balance_nitrogen`'s own text is "Avoid overfeeding
  with high-nitrogen fertilizer" -- literally the opposite of PD-57's "use composts, mulches, and
  fertilizer to stimulate growth", and it is the only fertility method in the 64.
  `floating_row_cover.applies_to` = `['any']`, so the author is right that it would pass and right
  that its prose ("the moths, flies, and beetles cannot reach the plants to lay eggs") contradicts a
  rain-exclusion note. `trap_cropping.applies_to` = `['insect_chewing','insect_general']`, cannot
  reach fungal, and its own text says it "deliberately ADDS" a host.

**The four-rung cultural ladder is what PD-57 supports. A short ladder is correct when the evidence
is short. No padding, no substitution. This is the strongest part of the submission.**

I also verified B5, which the author raised against the brief: `prune_out_infection.applies_to` =
`{bacterial, disease_general}`, which intersects `TYPE_TARGETS['fungal']` at `disease_general`, so
it **would** pass the gate on a `fungal` problem. **The author is right and the brief's framing is
wrong as a gate fact.** Worth correcting before it is repeated to another fan-out.

## 2d. URL and mainland scope

* The `www3` re-point: I fetched `https://www.ctahr.hawaii.edu/oc/freepubs/pdf/PD-57.pdf` myself and
  it followed to `www3` and returned the PDF. Both live. Per the `url-liveness-is-not-a-status-code`
  lesson, neither is dead, so this is a convention call, not a correctness one. C2 flags it honestly
  and offers the revert. No objection either way.
* **No mainland prevalence claim is asserted beyond PD-57 -- with one exception running the other
  way.** See FIX-B2: the distribution list drops a country PD-57 prints.

## 2e. Corrections graded (8)

| field | grade | note |
|---|---|---|
| `symptoms_seasoned` | **HOLDS** (`why` overstates, FIX-B4) | new text tracks PD-57 sentence for sentence |
| `symptoms_beginner` | **HOLDS** | food-safety sentence verified verbatim: "Lemongrass plants with the rust disease are safe for humans to use in cooking recipes or as teas after drying the leaves". Genuinely the best consumer fact in the document and the record had it nowhere |
| `cause_seasoned` | **WRONG (minor)** | FIX-B2, Thailand dropped from a quote presented as verbatim |
| `cause_beginner` | **HOLDS** | leaf-wetness requirement and spore survival both verbatim-anchored |
| `organic_treatment_seasoned` | **SYNTHESIS** | FIX-B3, "a neem-oil product" is not PD-57's characterization |
| `organic_treatment_beginner` | **HOLDS** | clean; no chemistry claim beyond PD-57's own |
| `prevention_seasoned` | **HOLDS** (STYLE nit, FIX-B6) | "full sun" correctly struck; PD-57 never mentions sun. Three genuinely new sourced practices added |
| `prevention_beginner` | **HOLDS** | |

---

# 3. LEAF BLIGHT -- `lemongrass-leaf-blight`, type `fungal`, severity `low`

## 3a. The rewrite came from USU: **VERIFIED**

`usu_ext` Diseases table, my own fetch, verbatim:

> | Leaf Blight | "Reddish brown spots on leaf tips and margins; leaves appear to prematurely dry out" | "Spray with registered fungicides if positively identified or hand remove blighted leaves." |

New `symptoms_seasoned`: "Reddish brown spots appear at the leaf tips and along the margins, and
affected leaves dry out early." **HOLDS**, verbatim-faithful, and it fixes a real defect: the live
canonical said "Brown, elongated lesions develop along the leaf blades", which is PD-57's rust
description ("brown and elongated, stripe-like, brown lesions that coincide with leaf veins"). As
shipped, the two disease entries described the same thing. The correction is warranted.

## 3b. No binomial: **VERIFIED, and correctly refused**

I confirmed independently that the genus is *Curvularia* across four unrelated first reports naming
four different species (*C. affinis*, Brazil, J. Plant Pathol. 2022; *C. nanningensis* sp. nov.,
China, PMC7033261; *C. andropogonis*, India/Philippines; *C. cymbopogonis*, Guatemala), all
journal-only. No binomial appears anywhere in the entry. `usu_ext` names no pathogen and does not
even say "fungus". The `cause_*` rewrite states the limit plainly rather than papering it. **HOLDS.**

The `fungal` type retention is defensible: I computed it -- 52 blight-named entries roster-wide, 43
`fungal`, 7 `bacterial` (all genuinely bacterial by name), 2 left coarse. The record's number is
exactly right.

## 3c. The one rung

| # | method | grade | evidence |
|---|---|---|---|
| 1 | `garden_sanitation` | **HOLDS**, with a SOURCING fix (FIX-B7) | `usu_ext`: "hand remove blighted leaves". The note preserves USU's condition on spraying ("if positively identified"), which is the part of the sentence that matters and which the live record had inverted into a copper recommendation. `garden_sanitation.applies_to` = `['any']`, legal. |

**A one-rung ladder is correct here.** The entire anchor is a two-cell table row. Everything the live
record added -- leaf wetness, humidity, crowding, spread through dense plantings, base watering,
staying out of a wet planting -- is rust's epidemiology transplanted, and every extra rung would have
been padding on a borrowed premise. B1 states this and I agree with it.

## 3d. Corrections graded (8): all **HOLD**

All eight are verbatim-faithful to the USU row or to the honest statement of its limits. The
`organic_treatment_*` pair restores USU's diagnostic condition, which is the single most consequential
edit on this entry.

---

# 4. ROOT ROT -- `root-and-stem-rots`, type `fungal`, severity `medium`

## 4a. Genus-agnostic: **VERIFIED**

New `cause_seasoned`: "No source names an organism for lemongrass; the general cause is the soilborne
fungi and water molds that need saturated pore space to move and infect". No binomial anywhere.
Matches the roster's `root-and-stem-rots` register (I confirmed the umbrella is live on exactly
6 crops: borage, echinacea, marigold, sweet-alyssum, sweet-pea, tomatillo). **HOLDS.**

## 4b. The "water a lot, but drain freely" tension: written correctly in ONE field, re-broken in THREE

The `cause_seasoned` correction is genuinely good: "what does the damage is soil that never drains,
not the amount you pour on", anchored to `uiuc_ext` ("water as needed to keep soil moist. Do not
overwater as that can lead to root rot") and `uc_mg` Santa Clara (Water: "Moderate; do not overwater
to avoid root rot"; Soil: "Well-drained."). Both quotes verified by my own fetch.

**But C7 claims "I wrote the rot entry so it does not depend on the disputed value", and that is not
true of the entry as shipped.** Three other fields on the same entry re-assert the disputed high-water
value against `uc_mg`, which is one of that entry's own two primary anchors:

* rung note_beginner: "The rule to hold on to is **water a lot** and drain fast, not water less."
* `organic_treatment_seasoned` new: "**Keep watering generously** once the water can get away, since
  the crop's need for water is not what caused the problem."
* `organic_treatment_beginner` new: "**keep watering well** once the extra water can run out."

The claim is defensible against the crop's other sources (USU: "it should be misted and regularly
watered"), so I do not grade it WRONG. But the stated design goal was not met, and C7 should say so.

## 4c. The one rung

| # | method | grade | evidence |
|---|---|---|---|
| 1 | `improve_drainage` | **HOLDS** | `uiuc_ext`: "When grown in pots use pots with ample drainage holes and filled with a prepared soil mix." `uc_mg` Soil: "Well-drained." PD-57's cross-benefit is real and verbatim: "Plant lemongrass in well drained soils in a relatively dry or well ventilated area to minimize the time of leaf wetness after rainfall." `improve_drainage.applies_to` = `['disease_general','fungal_soilborne']`, legal. Adding `uhawaii_ctahr` to this entry's sources for that one sentence (C3) is the right call. |

B4's check is correct: `improve_drainage`'s own text already carries the watering half ("watering
that lets the soil drain between soakings"), so the `even_watering` two-class gap genuinely did not
bite.

## 4d. Corrections graded (4): all **HOLD**, but one is MISSING

`symptoms_seasoned` gains an explicit "so what follows is the general pattern of a root rot rather
than anything published for lemongrass" hedge. That is exactly right. **`symptoms_beginner` was not
corrected and does not get the hedge** (see FIX-B8).

---

# 5. TYPES vs PINS, AND LADDER COHERENCE

All four match the pins exactly, name and id and type and severity:

| entry | pin | output | ladder coherent with type? |
|---|---|---|---|
| Spider mites (indoor and hot, dry conditions) / `spider-mites` | `mite` / low | `mite` / low | YES. `even_watering` [mite], `water_spray` [mite], `beneficial_predators` [insect_general], `insecticidal_soap` [mite], `horticultural_oil` [mite]. Tiers cultural → physical → biological → soft_chemical → soft_chemical: monotone under `TIERS = (cultural, physical, biological, soft_chemical, conventional)` |
| Lemongrass rust / `lemongrass-rust` | `fungal` / medium | `fungal` / medium | YES, all four cultural, all intersect fungal targets |
| Leaf blight / `lemongrass-leaf-blight` | `fungal` / low | `fungal` / low | YES |
| Root rot / `root-and-stem-rots` | `fungal` / medium | `fungal` / medium | YES |

Computed, not accepted: 31 "spider mite"-named entries roster-wide, 25 typed `mite`; 26 rust entries
in `diseases[]`, 24 typed `fungal`. `lemongrass-rust` and `lemongrass-leaf-blight` are both free ids.
The batch-25 cross-check in C10 is exactly right: oregano/rosemary/thyme type spider mites `insect`,
mint `null`, sage already `mite`.

One coherence observation, not a defect: `beneficial_predators`' own `how_it_works_beginner` is about
"ladybugs, lacewings, and tiny parasitic wasps" eating aphids, and parasitic wasps do not attack
mites. It reaches `mite` only via `insect_general` and is the roster's standard conservation rung, so
this is acceptable, but it is the same class of "method text sits awkwardly under the note" that B3
was careful about for `weed_host_control`. B3's own reasoning, incidentally, is sound: I read
`weed_host_control`'s text and it is entirely alternate-host framing, while PD-57's weed rationale is
purely canopy humidity.

---

# 6. SPIDER MITES -- rungs

| # | method | grade | evidence |
|---|---|---|---|
| 1 | `even_watering` | **HOLDS** | 7405 verbatim: "Spider mites prefer hot, dusty conditions and usually are first found on trees or plants adjacent to dusty roadways or at margins of gardens. Plants under water stress also are highly susceptible." The dust half is anchored too: "Dusty conditions often lead to mite outbreaks. Apply water to pathways and other dusty areas at regular intervals" and "Mid-season washing of trees and vines with water to remove dust may help prevent serious late-season mite infestations." `even_watering.best_use` already names the mite case explicitly, so the fit is the catalog's own |
| 2 | `water_spray` | **WRONG** | FIX-A2. The practice holds (`usu_ext` "spray plant with a forceful jet of water to dislodge the insects"; 7405 "regular, forceful spraying of plants with water often will reduce spider mite numbers adequately"). The **reason attached to the morning timing is false by this file's own finding** |
| 3 | `beneficial_predators` | **HOLDS** | 7405: "Spider mites have many natural enemies … especially when undisturbed by pesticide sprays", set against `usu_ext` "Mostly an indoor plant problem". The indoor/outdoor asymmetry the note draws is a legitimate reading of the two anchors together |
| 4 | `insecticidal_soap` | **HOLDS**, with one SYNTHESIS (FIX-B9) | 7405 verbatim: "Don't use soaps or oils on water-stressed plants or when temperatures exceed 90°F." Both limits carried, correctly, in both registers. `usu_ext` "Use insecticidal soaps" |
| 5 | `horticultural_oil` | **WRONG** | FIX-A1. The soap-or-oil framing is right (7405: "use an insecticidal soap or oil in your spray"). **The sulfur interval is wrong by a factor of two, in the unsafe direction** |

Corrections graded (5): `symptoms_seasoned` **HOLDS**; `organic_treatment_seasoned` **HOLDS** with an
unsourced cadence; `organic_treatment_beginner` **UNSUPPORTED** (cadence); `prevention_seasoned`
**HOLDS**; `prevention_beginner` **UNSUPPORTED** (cadence). See FIX-B10.

---

# FIX LIST

## A. MUST FIX BEFORE PROMOTE

### FIX-A1. `pests[0].control_ladder[4]` (`horticultural_oil`) `note_seasoned` -- the sulfur interval is WRONG, by half, in the unsafe direction

**Exact text:** "The same restrictions apply, nothing above 90°F or on stressed foliage, and **keep
sulfur two weeks clear of an oil spray**."

**What is wrong:** "two weeks" is not in any document. The entry's own added anchor gives a different
number, and it is more than double.

**The document sentence that settles it.** UC IPM Pest Notes 7405, verbatim, confirmed on two
independent fetches:

> "Don't apply sulfur within **30 days** of an oil spray."

I also confirmed the interval is not in `horticultural_oil`'s own catalog text, so it is not inherited
from the method. This is brief defect class 5 exactly: a number with no warrant, contradicting the
rung's own cited anchor, and understating a phytotoxicity interval is the direction that causes harm.
**Change "two weeks" to "30 days".**

### FIX-A2. `pests[0].control_ladder[1]` (`water_spray`) `note_seasoned` -- asserts leaf blight epidemiology the same file declares unpublished

**Exact text:** "Outdoors, do it in the morning: **this crop's two leaf diseases both need the
foliage to stay wet**, and a soaked clump going into the evening is the condition they want."

**What is wrong:** the file's own `lemongrass-leaf-blight` `cause_seasoned` correction says "there is
no published cause or **weather driver** to give for it", and its `prevention_seasoned` `why` says
the leaf-wetness/humidity/crowding framing "is rust's management written over a disease with no
published epidemiology". The rung asserts as fact, in a different entry, the exact claim this pass
strips. It is a self-contradiction inside one submitted file.

**The document sentences that settle it.** PD-57 for rust: "The spores land on wet or moist lemongrass
leaves and may infect them during periods of very high relative humidity." `usu_ext` for leaf blight,
complete: "Reddish brown spots on leaf tips and margins; leaves appear to prematurely dry out" /
"Spray with registered fungicides if positively identified or hand remove blighted leaves." No wetness
statement exists.

**Fix:** narrow to one disease -- "this crop's rust needs the foliage to stay wet".

### FIX-A3. The oil-claim disposition is incomplete by three fields, and its counts are wrong

**Exact text (A0):** "Retiring pests[0] removes four of **the twelve fields** that carried the claim
… **EIGHT survive** … **five `companions.*` fields**".

**What is wrong:** independently walked, 14 fields carried the claim, 10 survive, and companions
carries **eight**, not five. `companions.good_beginner_seasoned[0].why_beginner`,
`companions.good_beginner_seasoned[1].why_beginner` and `companions.note_beginner` are unlisted and
unadjudicated -- all three beginner register, and one of them (`note_beginner`) is the register twin
of the field A7 changes. The A0 arithmetic also does not close under its own grouping (2 + 5 = 7,
plus three `varieties.*` fields = 10, not 8).

The full table is at section 1b. Per `compute-roster-claims-never-assert-them`: every computed claim
in this submission was right and this asserted one was not.

**Fix:** adjudicate the three missed fields explicitly (I expect KEEP on the two "traditional" ones
and on the "may help" one, but the verdict must be recorded), and correct the counts. C8's proposed
`verification_log_ref` append inherits the undercount and should be re-derived from the corrected
table before it is written.

### FIX-A4. C5's "checked and found clean" verdict is wrong for LEAF BLIGHT in four places

**Exact text (C5):** "`watering.method_seasoned` and `watering.method_note_seasoned` already say base
watering limits rust **and leaf blight**, which is right".

**What is wrong:** it is right for rust and unanchored for leaf blight, by this file's own finding.
I read the live fields; four carry it:

* `watering.method_seasoned`: "keeping the foliage dry limits rust **and leaf blight**"
* `watering.method_note_seasoned`: "keeps foliage dry to limit rust **and leaf blight**"
* `weather_triggers[3].body_seasoned`: "prolonged leaf wetness favor lemongrass rust **and leaf
  blight**, especially in crowded clumps"
* `regions.se_gulf.region_notes_seasoned`: "warm, humid, crowded conditions favor rust **and leaf
  blight**"; `regions.fl_peninsula.region_notes_seasoned` says the same; `regions.ca_interior`'s
  "rust **and blight** are seldom a problem here" also credits blight with a weather driver

**Fix:** either scope all of these to rust, or drop the leaf-blight epidemiology corrections and say
why. Shipping both is an internal contradiction that a later audit will re-find. Note this is the
same family as FIX-A2 and the A1 wording problem in section 1d -- **the leaf-blight epidemiology strip
is incomplete in six fields outside the entry.**

## B. SHOULD FIX

### FIX-B1. `varieties.note_beginner` and `varieties.recommended[2].note` are not "already right"

A8 says DO NOT TOUCH. `note_beginner` says citronella grass is "grown to make citronella oil **and to
repel bugs**"; `recommended[2].note` calls it "**an ornamental insect-repellent plant**". `uwi_hort`'s
only sentence is a product claim: "the source of commercial citronella oil, which is used in soaps, as
a mosquito repellent in insect sprays and candles and in aromatherapy." Solano refutes the ornamental
version directly. Soften both to the oil/product framing that `varieties.note_seasoned` already uses.

### FIX-B2. Rust `cause_seasoned` drops a country from a quote presented as verbatim

**Exact text (new):** "PD-57 reports the disease from **Hawaii, California and New Zealand**".
**Exact text (`anchor`, presented as verbatim):** "'The disease has been reported in Hawai'i,
California, New Zealand, and may be established in other locations…'"

**PD-57, verbatim, from my own page-image read:**

> "The disease has been reported in Hawai'i, California, **Thailand**, New Zealand, and may be
> established in other locations where lemongrass is cultivated."

The record makes the same omission, so this propagated. Consequence for a US reader is small, but the
whole point of this correction was mis-anchoring, and an `anchor` field that alters a quote it labels
verbatim is exactly the defect class. Restore Thailand, or write "including".

### FIX-B3. "a neem-oil product" is not PD-57's characterization

**Exact text:** "PD-57 records exactly one fungicide product registered for lemongrass rust in
Hawaii, **a neem-oil product**, and says plainly…"

PD-57 names the product ("Trilogy (Table 1)") and never states its active ingredient. **Table 1 does
not exist in the published PDF** -- I read all four pages: p1 text, p2 text + photo, p3 references +
photo, p4 photos. That Trilogy is a clarified neem-oil extract is external knowledge. The appositive
reads as PD-57's, and the same gloss appears in `refusals[0]` and `unreachable_claims[3]`.

This does not weaken the no-chemistry conclusion -- it strengthens it: with no admitted source stating
an active ingredient, no chemical rung can be chosen at all. Fix the attribution, not the verdict. The
beginner register already handles it correctly and needs no change.

### FIX-B4. Rust `symptoms_seasoned` `why` overstates

**Exact text:** "and **no source anywhere uses 'tan to purplish'**".

The Ploetz 2014 abstract uses it verbatim: "large patches of **tan to purplish** necrotic tissue" --
which is the very document the same sentence identifies as the uncited origin. Change to "no *cited*
source uses it; it is the Florida note's phrase."

### FIX-B5. `airflow_spacing` note_seasoned: "Three of its eight practices"

PD-57's eight bullets: (1) vigor/compost, (2) intercrop **;** avoid large numbers close together,
(3) do not purchase rusted plants, (4) rainproof cover, (5) prune/destroy/no mulch, (6) weeds,
(7) well-drained + relatively dry or well ventilated, (8) minimize overhead irrigation. The spacing
clause is the second half of bullet 2, whose first half the file separately files as unreachable, and
bullet 8 also acts on leaf wetness. So it is two full bullets plus half of a third, and four bullets
in total act on the variable. Reword to "PD-57 attacks leaf wetness from several directions". Same nit
carries into B2's "Four rungs cover six of the eight practices".

### FIX-B6. Rust `prevention_seasoned`: "PD-57's **first line of defense** is not to buy or pass on rusted plants"

"Do not purchase or distribute rusted plants" is PD-57's **third** bullet. The sentence attributes an
ordering to the document that it does not have. Reword as "the cheapest step PD-57 gives" or similar.

### FIX-B7. The leaf blight entry asserts PD-57 content with `usu_ext` as its only anchor

Three fields on an entry whose `sources` is `["usu_ext"]` carry PD-57's rust description:

* `symptoms_seasoned`: "whose lesions run with the veins down the blade and break open into
  cinnamon-brown pustules on the underside"
* `symptoms_beginner`: "If the marks instead run down the middle of the blade and rub off dusty and
  brown from the underside, that is rust"
* rung `note_seasoned`: "rust runs down the blade with the veins and erupts into cinnamon-brown
  pustules underneath"

C3 added `uhawaii_ctahr` to the root rot entry for exactly one PD-57 sentence. Apply the same standard
here. (Minor within this: PD-57 says "erupt and develop dark, cinnamon-brown uredinial pustules" -- it
never says powdery or dusty. "dusty" also appears in the rust `symptoms_beginner` rewrite. Defensible
for urediniospores, but it is the author's word, not the document's.)

### FIX-B8. Root rot `symptoms_beginner` was not corrected, creating a register asymmetry

`symptoms_seasoned` now opens "Neither cited guide describes symptoms, so what follows is the general
pattern of a root rot rather than anything published for lemongrass". Live `symptoms_beginner` is
untouched and unhedged: "The plant yellows, wilts, and rots at the base even though the soil is wet.
The roots turn soft and dark." The seasoned reader is told the description is generic and the beginner
reader is not. Add a plain-language version of the same hedge, or declare the omission.

### FIX-B9. `insecticidal_soap` note_beginner adds an instruction 7405 does not give

**Exact text:** "Pick a mild day under 90°F, and **water a dry plant well before you spray**, because
soap scorches foliage that is hot or thirsty."

7405 says: "Don't use soaps or oils on water-stressed plants or when temperatures exceed 90°F." That
is a prohibition, not a "water it first, then spray" procedure. The seasoned register renders it
correctly ("skip a plant that is already short of water"); the beginner register converts a
prohibition into a workaround. **This is the field that changed under me mid-review**, so it may still
be in flight. Bring it back into line with the seasoned twin.

### FIX-B10. Three unsourced cadences

* `water_spray` note_seasoned: "treat it as a repeated habit **over a week or so**"
* `organic_treatment_seasoned`: "repeating **over about a week**"
* `organic_treatment_beginner`: "then repeat **every couple of days for a week**"
* `prevention_beginner`: "check … again **every few weeks** through the winter"

7405 says only "regular, forceful spraying" and gives no interval; `usu_ext` gives none. The practice
holds; the numbers are authored. Per the brief ("every interval … must be in a document"), either drop
them to "repeat regularly" or find the anchor.

### FIX-B11. `augmentative_release` is neither built nor declined

`augmentative_release.applies_to` = `['insect_soft_bodied','mite','insect_general']`, tier
`biological`, and its own catalog text names the products: "The commercially available mite predators
are the western predatory mite and Phytoseiulus, and a working guideline is roughly one predator for
every ten spider mites." 7405 carries the same, verbatim: "The major predator mites commercially
available for release are the western predatory mite and *Phytoseiulus*."

So a sourced, gate-legal biological rung was available. The record explicitly flagged it. The output
neither ships it nor records declining it -- `unreachable_claims[5]` covers only monitoring, and no
refusal mentions it. **I think declining is right** (7405 and the method's own cons put releases at
large-planting scale, and this crop's mite risk is a single overwintered pot indoors), but under the
conventional-disclosure convention the batch is applying elsewhere, the decline must be written down.
Add a refusal.

### FIX-B12. Spider mites `cause_seasoned` keeps the "stagnant air" driver the batch strikes

`symptoms_seasoned`'s `why` says: "'Stagnant air' is also replaced by the driver the added UC IPM
anchor actually names, dust." Live `cause_seasoned`, undeclared and unchanged: "Spider mites
(Tetranychidae) thrive in the warm, dry, **low-airflow** conditions of a heated indoor room". Same
driver, same entry, one field over. Neither anchor names airflow. Correct it or declare why not.

### FIX-B13. C4's failure_diagnostics enumeration is incomplete

C4 is correct and important -- `fd_lemongrass_rust` does carry the Florida journal wording, the
"most notable disease" superlative, and copper in both `next_season_tip` registers, and it is a
rendered field. I verified all four. **It also carries the unanchored full-sun claim in both**:
"**Full sun** and vigorous, uncrowded plants resist rust best" / "**Full sun** and healthy, uncrowded
plants resist it best" -- the same claim the file strikes from `prevention_seasoned` on the grounds
that "PD-57's siting advice is a relatively dry or well ventilated area, which is not the same
instruction." Add it to C4's list so the follow-up pass does not leave it.

### FIX-B14. C7's stated design goal was not met

C7: "I wrote the rot entry so it does not depend on the disputed value." Three fields on that entry
do (section 4b). The tension flag itself is correct and worth carrying; the claim about the entry is
not.

---

# SUMMARY

## Counts by grade

**Rungs (11):**

| grade | count | which |
|---|---|---|
| HOLDS | 9 | rust x4, leaf blight x1, root rot x1, spider mites `even_watering` / `beneficial_predators` / `insecticidal_soap` |
| WRONG | 2 | spider mites `water_spray` (FIX-A2), `horticultural_oil` (FIX-A1) |
| UNSUPPORTED / SYNTHESIS / STYLE / FIT | 0 as a rung's primary grade | |

**Declared corrections (25):**

| grade | count |
|---|---|
| HOLDS | 21 |
| WRONG | 1 (rust `cause_seasoned`, FIX-B2) |
| SYNTHESIS | 1 (rust `organic_treatment_seasoned`, FIX-B3) |
| UNSUPPORTED | 2 (spider mites `organic_treatment_beginner`, `prevention_beginner` -- cadences) |

**Was each correction NEEDED?** Yes, all 25. I checked every "old" text quoted in a `why` against the
canonical byte for byte; every quotation is accurate and every defect it names is real. Not one is a
cosmetic swap. That is a materially better hit rate than batch 24's.

**FIX items: 4 must-fix (A1-A4), 14 should-fix (B1-B14).**

## Refusals and unreachable_claims

All six refusals and all seven unreachable claims **HOLD** on mechanical verification of the catalog
and the gate tables, with one attribution correction (FIX-B3). One decline is missing (FIX-B11).

## The single most important finding

**`horticultural_oil`'s note tells the reader to keep sulfur two weeks clear of an oil spray. UC IPM
Pest Notes 7405, the entry's own added anchor, says 30 days.**

Everything else on this submission is a claim about a plant. This one is a phytotoxicity interval on a
food crop, it is wrong by more than half in the direction that causes damage, it sits on the highest
rung of the ladder where a reader has already escalated, and it contradicts the very document the
entry added in order to be more careful. It is the only place in 11 rungs where a reader following the
advice could hurt the plant.

Runner-up, because it is the pattern rather than the number: **the leaf-blight epidemiology strip is
right and incomplete.** The batch correctly establishes that no source publishes a weather driver for
lemongrass leaf blight, rewrites eight fields on that basis -- and then re-asserts the stripped claim
in a spider-mite rung (FIX-A2), in the proposed `description_seasoned` (section 1d), and in six
fields C5 declares clean (FIX-A4). Same shape as the geraniol finding this pass exists to close: the
claim is corrected where the pass is looking and survives everywhere else.

## What is right, and should not be relitigated

* **The copper removal is complete and correctly reasoned.** No fungicide claim survives on either
  disease. The refusal to substitute copper for a gate-blocked neem product is the right call, made
  for the right reason, against a rung that would have passed the gate.
* **The rust rewrite is anchored sentence for sentence to a document I read myself**, and the
  mis-anchoring diagnosis is now independently proven against the Ploetz 2014 abstract.
* **Four cultural rungs with no chemistry is PD-57's ladder, not a thin one.** No padding.
* **Two one-rung ladders are both correct.** Short evidence, short ladder.
* **The retirement, and A10's placement of the sourced absence with its two stripped qualifiers
  restored, is right.** I endorse it.
* **Brief item 6 (powdery-mildew leaf wetness) does not apply here** and was not mis-applied: this
  crop has no powdery mildew, and PD-57 genuinely does make leaf wetness rust's infection
  requirement, so the airflow and base-watering rungs are correct rather than the mildew defect.
* **B5 is right and the brief is wrong**: `prune_out_infection` does mechanically reach `fungal`.
* Output is gate-legal: `validate_out.py lemongrass` returns OK, types match pins, tiers are monotone,
  all `applies_to` intersect their problem type.

---

# RECORD-LEVEL FINDINGS

Filed against `record_lemongrass.md` for a later pass, not fixed now.

**R1. Every roster count in the record is exactly right.** I recomputed all of them rather than
accepting them: 912 problem entries; 823 laddered on 101 crops; the full type histogram (insect 380 /
fungal 320 / bacterial 73 / mite 30 / null 20 / pest 16 / mollusk 14 / viral 13 / disease 13 /
physiological 12 / vertebrate 12 / nematode 7 / other 2); zero laddered entries with coarse types;
`spider-mites` on 16 crops; `two-spotted-spider-mite` on 6; `root-and-stem-rots` on 6 with the exact
crop list; 31 spider-mite-named entries of which 25 are `mite`; 26 rust entries in `diseases[]` of
which 24 are `fungal`; 52 blight-named entries of which 43 are `fungal` and 7 `bacterial`. Worth
saying explicitly, because the one place this arc went wrong on a number is the one place it asserted
instead of computing (FIX-A3).

**R2. The record drops Thailand from PD-57's distribution list**, in a passage quoted as verbatim
(see FIX-B2). This is where the output's defect came from.

**R3. The record calls Trilogy "a neem-oil product, not a copper" without noting that PD-57 never
says so** and that the referenced Table 1 is absent from the published four-page PDF. Same origin as
FIX-B3.

**R4. The record quotes 7405's natural-enemies sentence as "many natural enemies **that often** limit
their numbers in many landscapes and gardens".** One of my two fetches returned "which limit their
numbers in many landscapes and gardens" and the other returned "that often limit populations". The
inserted hedge is conservative, so nothing downstream is over-claimed, but the sentence is presented
as verbatim and I could not reproduce that exact form. Low priority; worth a single careful re-read
if 7405 is ever quoted as verbatim in shipped prose.

**R5. The record's `prevention_seasoned` diagnosis is slightly off-target.** Its `why` says "the
pre-overwintering cut-back was credited with reducing mites" in that field. The live field says only
"Before overwintering, cut the plant back and inspect it" -- the mite-reduction credit lives in
`organic_treatment_*`, which the same correction set handles separately. The replacement is fine
(it keeps the anchored inspection half); only the justification misnames its target.

**R6. `verification_status.open_findings[2]` (`lemongrass_pilot_finding_003`) is genuinely closable,
and C9's reasoning is sound.** I re-verified the finding against the data before agreeing with the
close, per the re-verify rule. Its own text admits "Rust symptomology and leaf-blight detail modeled
from horticultural knowledge", which is exactly what this arc confirmed and made specific. PD-57 was
read in full this session (by the record pass, and again independently by me). C9's successor
suggestion -- a narrower finding on the catalog-addition decision for the two APS notes -- is the
right shape.

**R7. The record's own consumer-copy constraint check is accurate.** I re-ran it mechanically on the
output: no em dashes, no double hyphens in consumer prose, `°F` rendered correctly in all four
places it appears, "plant" lowercase throughout, American English. Clean.

**R8. The `water` = "High" vs `uc_mg` "Moderate" tension (C7 / record) is real and remains open.** It
is correctly scoped out of this pass. Flagging only that the rot entry did not stay clear of it
(FIX-B14), so whoever owns the watering block should expect three more fields to touch.
