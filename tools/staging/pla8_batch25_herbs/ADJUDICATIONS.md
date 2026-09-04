# PLA-8 BATCH 25 (HERBS) -- ADJUDICATION SURFACE

Written 2026-09-04 after the record/source pass returned. Canonical `a9c84847`, unchanged.
Seven reviewers, one per crop, 443KB of reports, ~120 documents fetched and read.

**Nothing here is applied. This is the decision surface.**

Sourcing outcome: **22 of 22 unsourced entries came back UNSOURCED-FOUND or better. Zero
unsourceable.** "Unsupported is not unsourceable" held again, 22/22.

---

## PART A -- RECORD CORRECTIONS (technical; orchestrator will make these unless told otherwise)

These are wrong-or-unanchored claims found against read documents. They are the batch-24 "record
pass" shape: they land as a correction commit BEFORE the ladders are authored, because a ladder
authored against a wrong record has to be re-authored (batch 24 paid 71% re-authoring for this).

| # | crop | entry | defect | evidence |
|---|---|---|---|---|
| A1 | oregano, rosemary, thyme | Spider mites | `type: insect` is wrong; must be `mite` | **MEASURED HERE:** typing a spider mite `insect` makes `sulfur` and `even_watering` ILLEGAL under `control_ladder_gate.TYPE_TARGETS`. Roster vote 30 `mite` / 4 `insect`; 3 of the 4 outliers are in this batch. sage already correct. |
| A2 | mint | all 6 | `type` and `severity` are ABSENT keys | 30/30 problems on the batch's other six crops carry both. Zero of 823 laddered entries lack them. |
| A3 | lemongrass | all 5 | coarse `pest`/`disease` types | Zero of 823 laddered entries carry coarse types. 29 coarse entries exist, all on unladdered crops. |
| A4 | oregano | Root and stem rot | "stem rot" unanchored; "wet winters, **not cold**, are the underlying cause" is an authoring addition | **VERIFIED HERE:** the sole anchor (UF/IFAS Pasco) says root rot only, never stem rot, and says nothing about cold. UMD refutes the negation: "Excessively wet, **cold** soil can cause Mediterranean herbs such as rosemary, thyme, and lavenders to die over the winter." |
| A5 | thyme, **and rosemary** | Root and crown rot | same "not cold" construction | Same UMD sentence. **WIDENED 2026-09-04 (rosemary authoring agent): this is a THREE-crop twin, not two.** rosemary's `cause_seasoned` carried the identical construction and was not on this list, and the UMD sentence that refutes it NAMES ROSEMARY ("Excessively wet, cold soil can cause Mediterranean herbs such as **rosemary**, thyme, and lavenders to die over the winter"). The rosemary agent dropped the clause rather than negating it, correctly, because its own record report did not carry the UMD read. |
| A6 | mint | Mint rust | binomial credited to `ncsu_ext`, which never names it; rhizome-overwintering credited to `usu_ext`, which never carries it | NCSU says only "Two main diseases are rust and leaf spot". WSU puts overwintering on **stubble and fallen foliage**, and makes rhizome contamination removable by a hot-water dip. **CORRECTED 2026-09-04 (mint reviewer): the 111°F figure is RHS's, not WSU's, and this row mis-attributed it.** WSU's .doc literally reads "113 F (34 C)", which is internally inconsistent (34°C is 93°F), so the contradiction is WSU's own and no re-read of WSU can settle it. RHS settles it and carries a ceiling the batch should use: "immerse in hot water at 44ºC (111ºF) (no higher) for 10 minutes... 44ºC (111ºF) is very near the lethal temperature for the plant." The mint authoring agent REFUSED to write any figure on seeing the inconsistency, which was right on the evidence it had. Needs rewriting, not just re-citing: it inserts two cheap rungs below "start over in a new spot". |
| A7 | mint | Mint rust | "rusty leaves are not good to eat" has no admitted anchor | Only source is an un-admitted Ask Extension answer. Consumption-adjacent; soften or drop. |
| A8 | mint | Verticillium wilt | **live fabricated attribution**: "The Connecticut Experiment Station and Utah State both flag it for mint" | CAES is not in the 219-entry catalog. Mint's own cert log recorded striking this exact credit from the NEIGHBORING entries 8 weeks ago. Fixing one field left it live in another. |
| A9 | sage | Powdery mildew | "warm, humid, still air" and "avoid overhead watering" are both wrong | UC IPM Pub 7493: "all powdery mildew species can germinate and infect without water on the plant's surface"; "Water on plant surfaces for extended periods **inhibits** spore germination"; favoring conditions are 60-80°F **and shade**. "Water at the base" stays right for sage, justified by root rot, not mildew. |
| A10 | rosemary | Powdery mildew | same defect ("damp, still, humid air", "avoid overhead watering") | Same UC IPM basis. Rosemary's is decisively an INDOOR problem (UMD: "usually disappears when the plants are moved further apart or are taken outside in the spring"). |
| A11 | sage | Verticillium wilt | "improve drainage" is wrong advice | UMD: "Fusarium and Verticillium are favored by **droughty** conditions." Drainage is the root-rot lever, copied across to a neighbor. |
| A12 | lavender, rosemary | Spittlebug(s) | "No specific prevention is warranted" is refuted | **CORRECTED 2026-09-04: this row originally fused two sources into one attribution.** UMN does NOT publish the spring-timing sentence; that is UC IPM's ("Cut spittlebug-infested weeds in the spring before the insects mature and spread"). Read directly at UMN 2026-09-04: its weed control is "Remove weeds near your gardens to remove one of their food sources", with no timing, plus "Physically remove them by hand" and "Spray them with a strong blast of water". The ladder cap IS UMN's and is verbatim: **"Pesticides are not effective against spittlebugs as the nymphs are protected inside their spittle masses from any pesticide sprays."** UMN also names **Herbs** among its hosts. Caught by the rosemary authoring agent, which refused to write an attribution its own record report did not carry. Fusing two sources into one credit is the same defect class as mint's CAES attribution (A8). |
| A13 | thyme | Aphids | mechanism stated backwards | Record: lean soil keeps thyme "vigorous enough to shrug off aphids." Clemson: "Aphids are common in **rapidly growing, succulent** plants." The practice is right; the reason inverts it. |
| A14 | lemongrass | (crop-wide) | the aromatic-oil pest-deterrence mechanism is unanchored and refuted, and is live in **~10 fields** | **VERIFIED HERE.** None of the three cited sources carries it: USU's only oil sentence is about extracted oil as a product, in a uses section; NCSU says oils are "used for perfumes and herbal medicines"; Wisconsin's repellency sentence is about ***C. nardus*** commercial citronella oil in sprays and candles, a different species. UC Master Gardeners (Solano) refutes the growing-plant version directly: "just growing it may not repel one 'Skeetter', since the oil in the plant has the repellent properties, and it must be extracted to use". The `companions.*` instances ARE correctly hedged (`verified_against_sources: false`); the `pests[0].*` ones assert it as fact. **The batch-2 cert log's "full-file scan clean" was wrong.** |
| A15 | lemongrass | Lemongrass rust | recommends copper fungicides | CTAHR PD-57: "There is only one fungicide product registered ... Trilogy" (a neem product). Also: the symptom prose is paraphrased from an uncited 2014 APS report, not from CTAHR. |
| A16 | lemongrass | Leaf blight | symptom prose is rust's description transplanted | USU genuinely lists leaf blight ("Reddish brown spots on leaf tips and margins"), but the record's "elongated lesions along the leaf blades / spreads through dense plantings" is the rust entry's text. |

**Append-only correction owed.** Per `docs/verification_log_ref_convention.md`, lemongrass's and
mint's `verification_log_ref` must take an appended `[CORRECTION 2026-09-04: ...]` line, not a
rewrite, because both assert a scan/credit that did not hold.

---

## PART B -- STRUCTURAL DECISIONS (TREVOR'S CALL -- these change what the batch IS)

Each changes the problem COUNT or a consumer-visible name. None is a gate question.

### B1. lemongrass "Generally pest-resistant (aromatic-oil deterrence)" -- RETIRE?

It is an assertion of absence wearing a pest entry's shape. You cannot build a ladder of controls
against "there are no pests."

* The **absence half is true and well sourced** (USU "generally free of pests and diseases when
  grown correctly"; Wisconsin "essentially no pest problems in the Midwest"; NCSU resistance
  checkbox). The record strips both qualifiers.
* The **mechanism half is unanchored and refuted** (A14).
* **Precedent: none.** A walk of all 128 crops / 912 problem entries found exactly one
  absence-assertion entry: this one. None of the 823 laddered entries resembles it.
* Batch 24 retired chives' aphids entry on a comparable finding.

**Recommend: RETIRE the entry**, move the sourced absence (with its qualifiers restored) into the
crop's descriptive prose, and correct the mechanism in the five surviving fields regardless.
Lemongrass then ladders 4 problems, not 5.

### B2. thyme "Foliar fungal problems in humid weather" -- RETIRE?

A hedge with nothing under it: no organism, no disease, no symptom that identifies anything.

The decisive evidence is an **informed absence**, not a failure to find: CSU Extension CMG
GardenNotes #731 names diseases for chervil, chives, coriander, dill, fennel, horseradish, mint,
oregano, parsley, rosemary, sage and tarragon, and gives *Thymus vulgaris* exactly one line:
*"Do not overwater due to root rot susceptibility."* Same authors, same document, one page apart.
Corroborated by NCSU (both pages), Iowa State, UF/IFAS Santa Rosa ("no serious pests or diseases are
normally seen on the plant"), UMD, Clemson's 23-host powdery-mildew list (no herbs), VCE.

**Recommend: RETIRE, or narrow to "Powdery mildew".** Thyme then ladders 3 problems, not 4.

### B3. mint "Powdery mildew and anthracnose (leaf spot)" -- SPLIT?

The bundle forces one prevention string across two diseases whose sources disagree about leaf
wetness. **VERIFIED HERE:** UC IPM 7406 says "Overhead sprinkling may help reduce powdery mildew
because spores are washed off the plant", while the record's prevention says "water at the base
rather than overhead" and "keep the foliage dry". UC IPM's mint page names powdery mildew and does
**not** name anthracnose.

Both ids already exist (`powdery-mildew` 32 crops, `anthracnose` 14).
**Recommend: SPLIT into the two existing shared ids.** Mint gains one problem.

### B4. mint "Cutworms, mint flea beetles, and root-feeding pests" -- SPLIT?

Three organisms, three different ladders. `cutworms` (9 crops) and `flea-beetles` (34 crops) both
already exist. **Recommend: SPLIT into 3.** Mint gains two problems.

### B5. lavender "Whiteflies and aphids" -- DROP THE APHID HALF?

**The aphid half is unsupported across 8 documents**, and the exclusion looks deliberate: UC IPM
publishes a host-indexed pest list for lavender (Leafhoppers, Spider Mites, Spittlebugs, Whiteflies
+ Phytophthora root and crown rot) that omits aphids, while UC IPM's **rosemary** page lists aphids
explicitly. RHS names lavender's pests and mentions neither aphids nor whiteflies.

**Recommend: drop the aphid half, keep `whiteflies`.** This is a content deletion, so it is yours.
Note lavender's record also OMITS leafhoppers and spider mites, which UC IPM does list.

### B6. rosemary "Aphids and whiteflies" -- SPLIT?

Sources treat them as two, and management diverges at both ends of the ladder: aphids get nitrogen
and ant levers and a working soap rung; whiteflies get "difficult", soap "reduces but does not
eliminate", and an explicit conventional dead end. The bundle's likely origin is UGA B1170's section
headed "Aphids; Whiteflies", which attributes susceptibility to *germander and monarda* and whose
own rosemary section has no pest content at all.

**Recommend: SPLIT into `aphids` + `whiteflies`.** Rosemary gains one problem.

### B7. oregano "Rust" -- RENAME to "Mint rust"?

The §4f answer is that this is one organism nobody pinned: ***Puccinia menthae***. Every source that
names it on oregano calls it *mint rust* (`psu_ext`: "Oregano can be susceptible to fungal diseases
such as mint rust and root rot"; `rhs`: "The fungal disease mint rust can affect oregano").

**The tension:** "Mint rust" is what a gardener will search and what the sources say, but it reads
oddly on an oregano page, and it makes `oregano-rust` and `mint-rust` share a display name (the
guard will flag NAME_SHARED, correctly, and it would be registered as deliberately distinct).
Inventing a bare "Oregano rust" that no source uses is the worst of the three.

**Options:** (a) "Mint rust" -- source-faithful; (b) "Mint rust (on oregano)" -- clearer, unsourced
phrasing; (c) leave "Rust" and carry the organism in prose -- keeps the §4f defect.
**Recommend (a) or (b); this is a consumer-copy call, so it is yours.**

### B8. oregano "Botrytis and humid-weather foliar disease" -- RENAME?

The inverse of B7, and arguably worse. The name **leads with the one organism no source attaches to
oregano** (Botrytis), while the attested one is buried in the prose. **VERIFIED HERE:** oregano's own
shipped `uf_ifas` anchor publishes exactly two diseases for oregano, and they are **Powdery Mildew**
and **Root Rot**. Botrytis appears in neither.

**Recommend: rename to "Powdery mildew"** and reuse the existing 32-crop `powdery-mildew` id.

### B9. Two severity corrections

* **sage Verticillium wilt `low` -> `medium`.** Defensible on frequency, not on consequence.
  UMD: "These fungi remain in the soil for many years ... you must not plant the susceptible plant."
  The entry's own text says "There is no cure." `low` would make sage the lowest Verticillium record
  in the dataset (strawberry is `medium`).
* **rosemary Spider mites `medium` -> `low`.** Every source that ranks rosemary ranks it down
  ("generally pest and disease free", "fairly resistant to pests", "few pest problems"). Mites are
  the most-mentioned pest but no document converts that to severity.

`severity` is a legacy un-normalized field and neither is a gate blocker, so both are data-truth
calls rather than mechanical ones.

---

## PART C -- ID DECISIONS (orchestrator, run through the PLA-449 guard)

### C1. The root-rot family is a FIVE-crop decision, and the taxa genuinely differ

Shared display names hide different organisms. Match the taxon, not the name.

| crop | entry | organism, per read documents |
|---|---|---|
| lavender | Phytophthora root and crown rot | *Phytophthora* resolved; WSU pins *P. nicotianae*. VCE: Phytophthora + Pythium |
| rosemary | Root and crown rot | *Phytophthora* at GENUS only. UC IPM links the identical PRCR document as lavender's. VCE: Phytophthora + Pythium. **PNW handbook (403, NOT READ) indexes Pythium / *Berkeleyomyces* / Rhizoctonia and no Phytophthora** |
| thyme | Root and crown rot | VCE: ***Pythium* root rot, one genus only.** Not lavender's |
| sage | Root and stem rot | umbrella; no admitted document narrows it (Wisconsin D0094 lists Phytophthora/Pythium/Rhizoctonia/Fusarium) |
| oregano | Root and stem rot | `ncsu_ext` names oregano as a *Phytophthora* host; the shipped Pasco anchor says only "root rot ... excessive moisture" |

**Proposed:** sage + oregano reuse the existing umbrella **`root-and-stem-rots`** (6 crops, matches
their names and their unresolved taxa); lavender takes a Phytophthora-named id; thyme takes its own
(Pythium); **rosemary is BLOCKED on the unread PNW page** -- its 2026-07-06 cert log says
"Phytophthora-only" and the PNW index text disagrees.

### C2. `spittlebugs` -- new family, one shared id

***Philaenus spumarius***. RHS names the binomial and lists "lavender, rosemary" in one host
sentence. Sage's leg is inferred, not read (UC IPM publishes no sage page; 404). **Zero spittlebug
ids exist in canonical** -- this batch mints the family. One shared id, pinned once pre-fan-out.

### C3. sage Leafhoppers -- must NOT reuse `leafhoppers`

Sage's are ***Eupteryx decemnotata*** / ***E. melissae***, Lamiaceae specialists and **not vectors**
(UC IPM: "The Ligurian leafhopper (*Eupteryx decemnotata*) is a pest of mint, rosemary, sage";
UF/IFAS EENY-750; RHS). The existing `leafhoppers` id is cilantro's aster-yellows/curly-top framing
and `aster-leafhoppers` is the parsnip/cosmos vector. Reusing either would attach a vector ladder to
a non-vector pest. **Mint a new id.**

### C4. Rust ids

`oregano-rust` and `mint-rust`, host-scoped, matching the roster's whole rust family
(`garlic-rust`, `chives-rust`, `leek-rust`, `bee-balm-rust`, `sunflower-rust`, `fig-rust`,
`elderberry-rust`, `asparagus-rust`). `lemongrass-rust` is separately clean: CTAHR PD-57 gives
***Puccinia nakanishikii*** with a host range of *Cymbopogon* only, so the Poaceae/Lamiaceae
separation is on evidence, not assumption.

**Registry entry owed** for `mint-rust` / `oregano-rust`: one pathogen species, host-specialized
races that do not cross-infect. Note the direct mint-oregano cross-inoculation evidence is
**JOURNAL-ONLY** (APS 403s under both fetch paths); what is anchorable at T1 is the principle, via
WSU: "Two principal types of races of *P. menthae* have been recognized. One type infects Native
spearmint but not peppermint."

### C5. sage Slugs and snails -> reuse `slugs-and-snails`

Exact name match to the 11-crop majority id. Note both sage sources say "slugs", neither says
"snails". **Ladder constraint measured here:** the `mollusk` type reaches exactly 8 methods, and
`airflow_spacing` is NOT among them, though the record's slug prevention prose leans on airflow.

---

## PART D -- FILED, NOT ACTED ON

* **UC IPM's herb host-index lists pests our records omit**, consistently: Leafhoppers and Thrips on
  oregano, lavender and mint; Spittlebugs on oregano. UC IPM publishes NO thyme or sage page (both
  404), so the pattern covers basil, lavender, mint, oregano, rosemary only.
* **The UF/IFAS Pasco "Spice Up Your Life" series is a find-and-replace template** across herbs, and
  oregano's only shipped disease anchor rests on it. Worth a roster-wide check for other crops
  anchored to that series.
* **PlantVillage gives thyme's Alternaria the binomial *Alternaria brassicicola*** -- a brassica
  pathogen, wrong plant family. It is the only binomial on the open web for a thyme foliar disease
  and it is wrong. Not admitted; do not re-find it as a lead.
* **Catalog-addition candidates surfaced:** `csu_ext` and `iastate_ext` for thyme (both already
  admitted keys, just not in thyme's vocabulary); a `wsu_mint_rust` key on already-admitted
  `s3.wp.wsu.edu` infrastructure; VCE Pest Management Guide 456-018; UMass CAFE Greenhouse
  Floriculture; e-GRO Edible Alert E902; University of Delaware (no `udel` key exists).
* **`lemongrass_pilot_finding_003` closed** by the lemongrass reviewer: PD-57 now read, and its
  suggested UF/IFAS co-anchor resolves to nothing admissible (the Nassau County "fact sheet" is a
  republication of the USU text).
* **Method gaps** (claims the records support that no method reaches): hot-water rhizome/cutting
  treatment (111°F / 10 min) for mint rust; `even_watering` two-class problem again;
  `prune_out_infection` does not reach `fungal_foliar`.
