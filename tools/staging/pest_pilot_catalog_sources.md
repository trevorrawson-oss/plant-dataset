# Pest/IPM control_methods pilot seed -- source provenance

Draft for review. Pairs with `tools/staging/pest_pilot_catalog_content.json`. Every
`anchoring_urls` URL below was fetched live by Claude Code via WebFetch on **2026-07-22** and
confirmed on-topic. All sources are T1 (university extension / government). Only one new
`source_catalog` entry is proposed: **`npic_orst`** (NPIC, an Oregon State University + U.S. EPA
cooperative agreement). Every other source (`ucanr_ext`, `umn_ext`, `umd_ext`, `clemson_hgic`,
`psu_ext`, `msu_ext`) is already catalogued and already T1.

`anchoring_urls` carries ONE representative URL per source id (the gate requires
`anchoring_urls` keys == `sources`). A handful of methods are additionally grounded by a second
UC IPM page under the same `ucanr_ext` id; those supplementary URLs are listed here as
"also grounded by" so the reviewer sees the full evidence trail.

## The fetched pages (source id -> URL -> what it supports)

- **ucanr_ext** UC IPM Aphids (Pest Notes 7404) -- https://ipm.ucanr.edu/PMG/PESTNOTES/pn7404.html
  "High levels of nitrogen fertilizer favor aphid reproduction"; knock aphids off with "a strong
  stream of water"; conserve lady beetles/lacewings/syrphids/parasitic wasps and "avoid the use of
  broad-spectrum insecticides"; soaps/neem/oils "kill primarily by smothering," "kill only aphids
  present on the day they are sprayed," "leave no toxic residue," and can be phytotoxic "when the
  temperature exceeds 90F"; row covers exclude aphids/viruses.
- **ucanr_ext** UC IPM Fungus Gnats -- https://ipm.ucanr.edu/home-and-landscape/fungus-gnats/
  "avoid overwatering and provide good drainage. Allow the surface of container soil to dry between
  waterings"; yellow sticky traps trap adults; Steinernema feltiae as a soil drench for the larvae
  (effective 60F to 90F, moist); Bti "toxic only to fly larvae."
- **ucanr_ext** UC IPM Imported Cabbageworm -- https://ipm.ucanr.edu/PMG/GARDEN/VEGES/PESTS/importcabwrm.html
  "Handpick"; "Egg laying can be prevented by using floating row covers"; "Bacillus thuringiensis or
  spinosad are very effective."
- **ucanr_ext** UC IPM Powdery Mildew on Vegetables (Pest Notes 7406) -- https://ipm.ucanr.edu/PMG/PESTNOTES/pn7406.html
  "Provide good air circulation by pruning excess foliage and properly spacing plants"; "Plant
  resistant varieties"; sulfur "Do not apply ... when air temperature is near or over 90F and do not
  apply it within 2 weeks of an oil spray," and it "can be damaging to some" plants; oils "never ...
  above 90F or to drought-stressed plants."
- **ucanr_ext** UC IPM Thrips (Pest Notes 7429) -- https://ipm.ucanr.edu/PMG/PESTNOTES/pn7429.html
  "Spinosad can be toxic to certain natural enemies (e.g., predatory mites, syrphid fly larvae) and
  bees when sprayed and for about 1 day afterward; do not apply spinosad to plants that are
  flowering"; neem/azadirachtin have "low toxicity to people, pets, and pollinators."
- **ucanr_ext** UC IPM Clubroot -- https://ipm.ucanr.edu/PMG/GARDEN/VEGES/DISEASES/clubroot.html
  "Add lime annually to affected soils below pH 7.2"; use pathogen-free transplants and avoid
  replanting in infested areas.
- **ucanr_ext** UC IPM Cole Crops, Relative Toxicities to Natural Enemies and Honey Bees --
  https://ipm.ucanr.edu/agriculture/cole-crops/relative-toxicities-of-insecticides-and-miticides-used-in-cole-crops-to-natural-enemies-and-honey-bees/
  Bt honey-bee "II ... short"; insecticidal soap "III / No bee precaution"; spinosad "II ...
  toxic against some natural enemies ... up to 5 to 7 days after"; permethrin and carbaryl both
  honey-bee "I" with "long" residual and "H" (high) toxicity to predators/parasites.
  (Supplementary anchor for pyrethroid + carbaryl, alongside NPIC.)
- **ucanr_ext** UC IPM Webspinning Spider Mites / Grape -- https://ipm.ucanr.edu/agriculture/grape/webspinning-spider-mites/
  "Naturally occurring predator mites will survive sulfur sprays and dusts, but released ones may
  not survive dusting sulfur unless they have sulfur resistance." (Grounds the sulfur beneficial-mite
  caution; `sulfur.anchoring_urls[ucanr_ext]` points to Pest Notes 7406 as the representative page.)

- **umn_ext** UMN Extension Clubroot -- https://extension.umn.edu/plant-diseases/clubroot
  "avoid planting brassicas in affected fields for 5 to 7 years"; resistant varieties available;
  clubroot favors acidic soils "pH below 6.5"; sanitation ("Clean your tools ... 1:9 ... bleach";
  reputable transplants).
- **umn_ext** UMN Extension Cutworms -- https://extension.umn.edu/yard-and-garden-insects/cutworms
  "Place aluminum foil or cardboard collars around transplants ... one end is pushed a few inches
  into the soil"; "physically remove and crush or drop the insects into soapy water" (handpick).
- **umn_ext** UMN Extension Cabbage and onion maggots -- https://extension.umn.edu/yard-and-garden-insects/root-maggots
  "Exclusion netting is very effective for cabbage maggot control. Make sure to have row covers in
  place before cabbage maggots start to fly"; effective as long as brassicas are not in the same
  spot as last year (rotation). (Row-cover second anchor + the row-cover rotation caution.)
- **umn_ext** UMN Extension Preventing seedling damping-off -- https://extension.umn.edu/solve-problem/how-prevent-seedling-damping
  "Water to keep it moist but not soggy. Use pots with drainage holes"; overwatering is a
  contributing factor; sterilize pots + new mix (sanitation); "Seedlings infected by damping off
  rarely survive."

- **clemson_hgic** Clemson HGIC, Cabbage, Broccoli & Other Cole Crop Diseases --
  https://hgic.clemson.edu/factsheet/cabbage-broccoli-other-cole-crop-diseases/
  Black rot: "Good sanitation ... very important," "Destroy all plant debris," certified disease-free
  seed, "Do not plant cole crops where black rot has occurred in the past two to three years," "no
  chemical controls available." Downy mildew: resistant varieties, "wide plant spacing to promote
  drying of leaves," and "copper fungicides will give fair control."

- **psu_ext** Penn State Extension, Safeguard Your Seedlings from Damping-Off --
  https://extension.psu.edu/safeguard-your-seedlings-from-damping-off
  "Avoid overseeding and properly space plants to improve air circulation and reduce humidity";
  damping-off "often begins in localized areas with poorly drained soils and overcrowded seed beds";
  "Avoid overwatering."

- **msu_ext** MSU Extension, How to Grow Celery -- https://www.canr.msu.edu/resources/how_to_grow_celery
  Celery needs "adequate calcium to avoid 'black heart'" and "abundant and consistent moisture";
  "Celery is shallow rooted and needs frequent watering." (Celery-specific blackheart grounding.)
- **umd_ext** UMD Extension, Blossom End Rot on Vegetables -- https://extension.umd.edu/resource/blossom-end-rot-vegetables
  A localized calcium disorder driven by "inconsistent watering, shallow watering or droughty
  conditions"; "Regular, deep watering will alleviate the problem if calcium levels in the soil are
  adequate." (The even-watering / calcium-movement principle behind blackheart.)

- **npic_orst** (NEW) NPIC Permethrin General Fact Sheet (Jul 2009) -- https://npic.orst.edu/factsheets/PermGen.html
  "Permethrin is an insecticide in the pyrethroid family"; "highly toxic to bees and other
  beneficial insects"; "highly toxic to fish"; "Cats are more sensitive to permethrin than dogs or
  people"; "Always follow label instructions."
- **npic_orst** (NEW) NPIC Carbaryl General Fact Sheet (Feb 2016) -- https://npic.orst.edu/factsheets/carbarylgen.html
  Carbaryl controls "aphids ... and many other outdoor pests," used "to thin out blossoms on fruit
  trees"; "highly toxic to earthworms and honey bees"; "Always follow label instructions."
- **npic_orst** (NEW) NPIC Copper Sulfate General Fact Sheet (Nov 2012) -- https://npic.orst.edu/factsheets/cuso4gen.html
  "Copper accumulates mainly at the surface of soils, where it binds tightly and persists"; "highly
  to very highly toxic to fish and aquatic life"; "Always follow label instructions."
- **npic_orst** (NEW) NPIC Bacillus thuringiensis (Bt) Fact Sheet (rev. May 2022) -- https://npic.orst.edu/factsheets/btgen.html
  "Bt aizawai and Bt kurstaki controls caterpillars of moths and butterflies" (i.e. all lepidopteran
  larvae, including desirable species); "Spores made by Bt damage the gut of insect larvae after the
  larvae eat them"; low toxicity to bees/birds/fish; "Typical foliage half-lives are 1 to 4 days."

## Per-method source map

| method | tier | sources (anchoring) | also grounded by |
|---|---|---|---|
| crop_rotation | cultural | ucanr_ext (clubroot), umn_ext (clubroot), clemson_hgic (cole diseases) | umn root maggots |
| garden_sanitation | cultural | clemson_hgic (cole diseases), umn_ext (clubroot), ucanr_ext (clubroot) | umn damping-off |
| resistant_varieties | cultural | umn_ext (clubroot), clemson_hgic (cole diseases), ucanr_ext (powdery mildew) | |
| balance_nitrogen | cultural | ucanr_ext (aphids) | |
| raise_soil_ph | cultural | ucanr_ext (clubroot), umn_ext (clubroot) | |
| airflow_spacing | cultural | ucanr_ext (powdery mildew), clemson_hgic (cole diseases) | |
| bottom_watering | cultural | ucanr_ext (fungus gnats), umn_ext (damping-off) | |
| sensible_seeding_rate | cultural | psu_ext (damping-off), umn_ext (damping-off) | |
| even_watering | cultural | msu_ext (celery), umd_ext (blossom end rot) | |
| floating_row_cover | physical | ucanr_ext (cabbageworm), umn_ext (root maggots) | ucanr aphids |
| handpick | physical | ucanr_ext (cabbageworm), umn_ext (cutworms) | |
| stem_collars | physical | umn_ext (cutworms) | |
| water_spray | physical | ucanr_ext (aphids) | |
| yellow_sticky_traps | physical | ucanr_ext (fungus gnats) | |
| beneficial_predators | biological | ucanr_ext (aphids) | |
| bt | biological | npic_orst (Bt), ucanr_ext (cabbageworm) | ucanr cole-crops toxicity table |
| beneficial_nematodes | biological | ucanr_ext (fungus gnats) | |
| insecticidal_soap | soft_chemical | ucanr_ext (aphids) | ucanr cole-crops toxicity table |
| neem_oil | soft_chemical | ucanr_ext (aphids) | ucanr thrips |
| copper_fungicide | soft_chemical | clemson_hgic (cole diseases), npic_orst (copper sulfate) | |
| spinosad | soft_chemical | ucanr_ext (thrips) | ucanr cole-crops toxicity table |
| sulfur | soft_chemical | ucanr_ext (powdery mildew) | ucanr grape webspinning spider mites |
| pyrethroid | conventional | npic_orst (permethrin), ucanr_ext (cole-crops toxicity table) | |
| carbaryl | conventional | npic_orst (carbaryl), ucanr_ext (cole-crops toxicity table) | |

## Judgment calls / honesty notes for the reviewer

1. **Only one source addition (`npic_orst`).** `msu_ext` and `psu_ext` turned out to be already
   catalogued and T1, so no addition was needed for them. NPIC is the one genuinely-missing T1: it
   is where the ingredient-specific non-target toxicology (bees, fish, cats, earthworms, soil
   accumulation) and the active-ingredient-class facts live. I proposed a bespoke `source_class`
   ("university_government_cooperative") mirroring how `aspca` got its own class; adjust if you have
   a preferred label.
2. **Conventional rung named by class + example, not brand** (`pyrethroid` -> "such as permethrin";
   `carbaryl`), each paired with the full honest caution set (kills bees + beneficials, long
   residual, fish/cats or earthworms, observe the pre-harvest interval, read and follow the label).
   Presented as fast and effective but rescue-only, not demonized.
3. **"Organic is not automatically harmless" is authored candidly:** copper "builds up in the soil"
   and is "highly to very highly toxic to fish and aquatic life"; sulfur "burns foliage in heat" and
   "can harm released predatory (beneficial) mites"; spinosad is "toxic to bees when sprayed and for
   about a day afterward" (neem, by contrast, UC IPM rates low in toxicity to pollinators, so its
   caution is dusk-timing hygiene for a contact spray, not an affirmative bee-toxicity claim); Bt
   "kills the caterpillars of moths and butterflies as a group, including desirable species such as
   swallowtails and monarchs." Each is tied to the fetched page above.
4. **`resistant_varieties` is Rung-1 cultural** and explicitly framed as "the first line of defense"
   and "the natural handoff to variety-level resistance data" -- the handoff to the next arc.
5. **`stem_collars` scoped to cutworms (chewing), not cabbage root maggot.** I could only T1-source
   collars for cutworms (UMN). No fetched T1 recommended a stem collar/disc for cabbage root maggot
   (UMN's root-maggot page and UC IPM both recommend row cover, not collars), so I did NOT claim
   `insect_boring` for it. The broccoli cabbage-root-maggot ladder should therefore lean on
   `floating_row_cover` + `crop_rotation`, not `stem_collars` (and not `beneficial_nematodes`: see
   the post-review fixes below, which removed the unsupported root-maggot efficacy claim).
6. **Some `applies_to` sets were trimmed to what the fetched pages actually support** (e.g.
   `water_spray`, `insecticidal_soap`, `beneficial_predators` are `insect_soft_bodied` only rather
   than also claiming `mite`; no pilot problem is a mite, and I had no fetched mite-control page for
   those methods). `sulfur` keeps `mite` because UC IPM documents it as a miticide.
7. **`spinosad` placed in `soft_chemical`, not `biological`** per spec 4.3 (a sprayed OMRI product
   with a real bee caution).
8. **`even_watering` is grounded by two angles:** MSU (celery blackheart specifically) + UMD
   (the calcium-movement / consistent-moisture principle, via blossom end rot, the same disorder
   mechanism). Both fetched.
9. **No `pesticide_safety_education` object authored here** -- that top-level safety spine
   (label-is-the-law, PHI, pollinator protection, PPE, resistance management) is a separate
   deliverable per spec 4.5. The per-method `cautions` carry the product-specific specifics; a brief
   PHI + resistance line is included on the two conventional methods per the pilot's honesty-framing
   instruction.

## `find_it_beginner` -- shelf guidance (added 2026-07-22 at Trevor's request)

Optional beginner-register field added to the methods whose NAME is opaque at the store:
`pyrethroid`, `carbaryl`, `bt`, `spinosad`, `insecticidal_soap`, `neem_oil`, `copper_fungicide`,
`sulfur`, `beneficial_nematodes`, `beneficial_predators` (10 total). NOT added to any
cultural/physical practice you don't buy (rotation, sanitation, row cover, watering, handpicking,
collars, sticky traps). The field is optional and not a required catalog key, so it does not touch
gate shape; scratch gate re-run after adding it = 0 `control_methods` violations.

Every `find_it_beginner` line teaches the same core lesson: **read the active ingredient on the
label, because brand names get reformulated.** Brand -> active-ingredient facts were verified live
2026-07-22:

- **The Sevin landmine (verified, and used as the teaching case).** Texas A&M AgriLife Extension,
  "When is Sevin not Sevin?" (P. Porter, 2018) -- https://citybugs.tamu.edu/2018/02/14/sevin-not-sevin/
  Verbatim: "GardenTech is switching the active ingredient in Sevin Insect Killer from carbaryl to
  zeta-cypermethrin, a newer pyrethroid insecticide," while "The Sevin Ready-to-Use 5% Dust ... is
  still carbaryl." Teaching: "To verify the active ingredient in Sevin or any other insecticide,
  look in the list of active ingredients at the bottom of the front label." Corroborated by MSU
  Extension "Bug's Eye View: Sevin" (https://extension.msstate.edu/newsletters/bugs-eye-view/2018/bugs-eye-view-sevin-vol-4-no-17)
  and GardenTech's own product pages (Sevin Insect Killer liquid/concentrate/RTU = 0.35%
  zeta-cypermethrin; granules = zeta-cypermethrin + bifenthrin; Sevin-5 Dust = carbaryl).
  -> `carbaryl.find_it_beginner` and `pyrethroid.find_it_beginner` both lean on this: carbaryl says
  Sevin dust is still carbaryl but many Sevin sprays are now a pyrethroid; pyrethroid names the
  Sevin liquid = zeta-cypermethrin reformulation as the read-the-label example.
- **Bt = Dipel / Thuricide (verified).** Bt active ingredient databases and product pages confirm
  Dipel and Bonide Thuricide are Bacillus thuringiensis subsp. kurstaki (Btk). UC IPM active-
  ingredient DB (Btk): https://ipm.ucanr.edu/home-and-landscape/pesticide-active-ingredients-database/active-ingredient-details/?uaiKey=95 ;
  Dipel: https://www.arbico-organics.com/product/dipel-df-bacillus-thuringiensis-kurstaki-btk-control-caterpillars/pest-solver-guide-caterpillars-moths
- **Spinosad = Captain Jack's Deadbug Brew / Monterey Garden Insect Spray (verified).** Bonide's
  Captain Jack's Deadbug Brew product page confirms active ingredient spinosad:
  https://bonide.com/product/captain-jacks-dbb-conc/ . Monterey Garden Insect Spray is a separate,
  widely-sold spinosad product (corroborated across retail + arbico listings).
- **Insecticidal soap = Safer (potassium salts of fatty acids)** -- stable, long-standing labeling;
  the line also teaches that ordinary dish soap is not the same product.
- **neem_oil / copper_fungicide / sulfur** -- kept active-ingredient-focused (neem oil or
  azadirachtin; a copper compound such as copper octanoate / copper soap; sulfur, distinct from
  lime-sulfur) and deliberately NOT tied to a single brand, since neem/copper formulations vary by
  product; per the "name the active ingredient and skip the brand rather than risk being wrong" rule.
- **beneficial_nematodes / beneficial_predators** -- included because both are genuinely purchased as
  living products (nematodes as a refrigerated mix; lady beetles / lacewing eggs as live releases);
  the predators line honestly notes that conserving resident beneficials beats bought releases, which
  reinforces (does not undercut) the method's conserve-first framing.

Judgment call: no `source_catalog` entry was added for the brand facts. `find_it_beginner` is
consumer shelf guidance, not a biological claim, and carries no `sources` array of its own; the
verification URLs above are recorded here for the reviewer's audit trail. If you want the Sevin
teaching formally sourced in-dataset, `tamu_citybugs` (Texas A&M AgriLife Extension) would be the
T1 to catalog.

## Post-review fixes (T1-fidelity review, 2026-07-22)

An independent T1-fidelity review ruled the catalog overwhelmingly clean; 4 items were corrected to
match the cited pages exactly. No canonical change, nothing committed.

1. **`neem_oil` bee caution** rewritten to match the cited UC IPM pages (aphids pn7404, thrips
   pn7429), which rate neem/azadirachtin "low toxicity to people, pets, and pollinators." The old
   caution asserted neem "can harm bees ... while the spray is still wet," which lacked source
   support and contradicted neem's own `pros` line. New caution: neem is low in toxicity to
   pollinators, and dusk timing is general contact-spray hygiene, not an affirmative bee-toxicity
   claim. Now consistent with the `pros` "low toxicity to pollinators."
2. **`beneficial_nematodes` root-maggot overclaim removed.** The only cited page (UC IPM fungus
   gnats) supports S. feltiae against fungus-gnat larvae only, not cabbage/root maggots. Dropped
   "root maggots" from `best_use` and `how_it_works_beginner`, and narrowed `applies_to` from
   `["insect_boring","insect_general"]` to `["insect_general"]`. The 60F to 90F moist-media facts
   stay verbatim to the page.
3. **`resistant_varieties` clubroot caution trimmed** to the UMN-supported part ("Clubroot-resistant
   varieties tolerate rather than fully resist the disease"); the added "local pathogen strains can
   overcome the resistance" clause (not on a cited page) was removed. The general `cons` already
   note resistance can be partial or overcome, so nothing honest is lost.
4. **`pyrethroid` residual** changed from "weeks to months" to "can persist for weeks," matching the
   NPIC permethrin fact sheet's ~1 to 3 week foliar residue.

Adjudicated OK and left untouched: the sulfur predatory-mite caution (true; UC IPM at source level,
grape-mites URL disclosed above), the pyrethroid/carbaryl "selects for resistance" lines (IPM
canon), spinosad "several days" (cole-crops toxicity table), copper "protectant only" (textbook).
