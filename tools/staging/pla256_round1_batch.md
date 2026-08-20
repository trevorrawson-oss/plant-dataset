# PLA-256 round 1 -- class-building batch

Read-only. Drawn from `tools/staging/pla256_register_pair_frame/_all_records.jsonl`
(canonical `be8a6d1e`, 20,168 pairs). **No similarity score of any kind appears in this file** --
no character overlap, no token ratio, no diff, no length delta. The frame itself carries no
numeric field at all, so there is nothing here to sort by except the prose.

---

## A. The 15 -- systematic draw over render status A

| | |
| -- | -- |
| population | render status **A only**: 14,595 of 20,168 pairs |
| sort key | `(crop_slug, field_path)`, both lexicographic ascending |
| sample size | 15 |
| **interval** | **k = N // n = 14,595 // 15 = 973** |
| **first index** | **486** (= k // 2, the midpoint start) |
| indices drawn | 486, 1459, 2432, 3405, 4378, 5351, 6324, 7297, 8270, 9243, 10216, 11189, 12162, 13135, 14108 |
| distinct field families | **14** (requirement was >= 8) |
| distinct crops | 15 |

**Why a midpoint start.** A systematic draw needs a start in `[0, k)`. Picking it with an RNG
would need a seed recorded to be reproducible; picking it by eye would be a selection decision.
`k // 2` is deterministic, needs no seed, and avoids the edge bias of starting at 0. It was fixed
BEFORE the family spread was checked, and the draw cleared the >= 8 requirement on the first
attempt at 14 families, so **no start was rejected and re-drawn** -- nothing in this
sample was chosen for what it contains. (For the record: every start in `[0, 11]` yields 12-13
families, so the constraint was never close to binding.)

Families represented:

- `companions :: note`
- `diseases[] :: cause`
- `failure_diagnostics[] :: label`
- `failure_diagnostics[] :: next_season_tip`
- `failure_diagnostics[] :: what_happened`
- `growth_stages[] :: log_prompt`
- `growth_stages[] :: user_action`
- `notifications[] :: body`
- `regions.<R>.resolved_by_zone.<Z> :: suitability_note`
- `start_method :: notes`
- `storage :: fridge`
- `tips_by_stage.<stage>[] :: text`
- `watering.schedule_by_stage[] :: note`
- `yield_expectations :: per_plant`

---

### 1. `apricot` -- `regions.ca_south_coast.resolved_by_zone.11.suitability_note`

- index 486 | family `regions.<R>.resolved_by_zone.<Z> :: suitability_note` | renders: TreeCalendarCard/HardinessFruitingCard + registerNote in [slug].tsx:454 -- SEE PLA-323

**beginner**

> The South Coast is usually too mild to give even low-chill apricots the cold they need, so the tree lives and grows but blooms unevenly and rarely fruits dependably. Treat it as a tree that survives rather than one that crops.

**seasoned**

> The South Coast usually cannot bank enough winter chill for even low-chill apricots, so the tree survives and grows but blooms erratically and rarely sets a dependable crop. Treat it as a tree that lives rather than one that fruits.

---

### 2. `beet` -- `start_method.notes`

- index 1459 | family `start_method :: notes` | renders: TimingSpineCard.astro:87 / StartFromSeedCard.tsx:34

**beginner**

> Plant beet seeds right in the garden where they will grow, since beets do not like being moved. Sow them about 1/2 inch deep once the soil is no longer frozen or soggy (about 45 to 50°F), roughly 2 to 3 weeks before your last spring frost, and again in late summer for a fall crop. Soaking the seeds in warm water for about a day before planting helps them sprout faster. Here is the beet surprise: each beet seed is really a little dried fruit holding several seeds, so one seed grows a small clump of seedlings, which is why you have to thin them later. Some kinds, sold as monogerm, grow just one seedling per seed. Keep the soil surface damp until the sprouts appear, often 1 to 2 weeks.

**seasoned**

> Direct-sow beets into the garden; they resent transplanting and are simplest grown from seed in place. Sow about 1/2 inch deep once the soil is workable and at least 45 to 50°F, roughly 2 to 3 weeks before the last spring frost, and again in late summer for a fall crop. Soaking the seed in warm water for about 24 hours before sowing speeds the slow germination. The key beet-specific point is that each beet seed is a multigerm seedball, a dried fruit containing several embryos, so a single seed sprouts a small cluster of seedlings and the stand must be thinned. Monogerm cultivars (one seedling per seed) avoid this. Keep the surface moist and uncrusted until the seedlings emerge, often 1 to 2 weeks.

---

### 3. `broccoli-microgreens` -- `storage.fridge`

- index 2432 | family `storage :: fridge` | renders: StoringCard.astro / guide-chapters.ts:217

**beginner**

> Rinse cut broccoli microgreens, pat them dry, and keep them in the fridge in a container with a paper towel to soak up extra moisture. They are delicate, so use them within about a week (up to 10 days if kept dry).

**seasoned**

> Rinse, pat dry, and refrigerate in a vented container lined with a paper towel; broccoli is a tender brassica and keeps best used within about 5 to 7 days, up to about 10 with careful drying. Harvest only what you will use soon.

---

### 4. `celery` -- `growth_stages[0].user_action`

- index 3405 | family `growth_stages[] :: user_action` | renders: GrowingJourneyCard.astro / guide-journey.ts:58

**beginner**

> Sow the seeds on top of the mix or barely cover them, keep them warm (around 70°F), give them light, and never let the surface dry out. A clear cover and a warm spot help. Be patient, since they are slow.

**seasoned**

> Sow on the surface or barely covered, keep the medium constantly moist and around 70°F, and provide light. Bottom heat and a humidity dome help. Do not let the surface dry during the long germination window.

---

### 5. `collards` -- `tips_by_stage.germination[1].text`

- index 4378 | family `tips_by_stage.<stage>[] :: text` | renders: GrowingJourneyCard.astro:230 / guide-journey.ts:59

**beginner**

> Start seeds indoors about a month before planting out, sow them in the garden once the soil can be worked, or sow in late summer for a fall crop.

**seasoned**

> For a spring crop start indoors about 4 to 5 weeks before set-out, or direct sow as soon as the soil is workable; for a fall crop sow in mid to late summer.

---

### 6. `english-cucumber` -- `failure_diagnostics[2].label`

- index 5351 | family `failure_diagnostics[] :: label` | renders: CommonProblemsCard.astro:87

**beginner**

> Leaves got white and powdery and the plant died back

**seasoned**

> Leaves turned white and powdery, then the plant faded early

---

### 7. `green-beans-bush` -- `tips_by_stage.flowering[1].text`

- index 6324 | family `tips_by_stage.<stage>[] :: text` | renders: GrowingJourneyCard.astro:230 / guide-journey.ts:59

**beginner**

> When it stays hotter than about 90°F, beans drop their flowers, especially varieties like Blue Lake 274. The plant gives up on flowers when it is too hot to make beans, then starts again once it cools. Water deeply before a heat wave, but mostly just wait, the plants will flower again.

**seasoned**

> Expect blossom drop in sustained heat above about 90°F, especially in varieties like Blue Lake 274. The plant aborts flowers when it is too hot to set pods, then resumes once the weather cools. Water deeply ahead of a heat wave, but mostly let the plant recover and reflower.

---

### 8. `lemon` -- `companions.note`

- index 7297 | family `companions :: note` | renders: CompanionsCard.astro:142

**beginner**

> Keep grass and weeds away from under a lemon tree, out to the edge of the branches. They steal water and feed the tree needs. Keep mulch a hand's width back from the trunk. You do not need a second tree for it to fruit.

**seasoned**

> For a tree, 'companions' is really root-zone management, not vegetable pairing. The single most important rule is to keep lawn grass and weeds well clear of the root zone out to the drip line: turf competes hard for water and nitrogen and slows a young citrus markedly. Keep organic mulch pulled back at least a foot from the trunk to reduce Phytophthora foot-rot risk. Because lemon is self-fruitful, there is no need to site a second tree nearby for pollination. Low, shallow-rooted plantings outside the drip line are harmless; anything that crowds the trunk or holds moisture against it is not. (Sources: Texas A&M AgriLife, UF/IFAS.)

---

### 9. `mulberry` -- `failure_diagnostics[2].next_season_tip`

- index 8270 | family `failure_diagnostics[] :: next_season_tip` | renders: CommonProblemsCard.astro:102

**beginner**

> Plant mulberries away from paths, patios, driveways, and parking; for a small yard pick a dwarf or weeping variety you can net and pick clean.

**seasoned**

> Site mulberries away from walkways, patios, drives, and parking; for a small space choose a dwarf or weeping cultivar you can net and pick clean.

---

### 10. `parsley` -- `diseases[1].cause`

- index 9243 | family `diseases[] :: cause` | renders: pest-control.ts OUTDOOR_SLOTS / guide-chapters.ts:118

**beginner**

> Soil fungi rot the parsley root and crown when the soil stays too wet, especially over a soggy winter.

**seasoned**

> Soilborne water-mold and fungal rots (Pythium, Phytophthora, Rhizoctonia) favored by waterlogged, poorly drained soil and overwatering.

---

### 11. `persimmon` -- `notifications[0].body`

- index 10216 | family `notifications[] :: body` | renders: PlantNotificationsCard.astro:82

**beginner**

> Now is a good time to plant a bare-root persimmon, or a young potted tree in the cooler months, before it starts growing. Handle the roots gently, since persimmon does not like being disturbed, keep the graft joint above the soil, and pick a sunny, well-drained spot. On heavy soil, plant on a raised mound. Do not put fertilizer in the hole.

**seasoned**

> Set a dormant bare-root persimmon now, or a grafted container tree in the cooler months, before growth resumes. Handle the taproot gently (persimmon resents disturbance), keep any graft union above the final soil line, choose a full-sun, well-drained spot, and plant on a raised mound if your soil is heavy. Do not fertilize in the hole.

---

### 12. `pumpkin` -- `growth_stages[5].log_prompt`

- index 11189 | family `growth_stages[] :: log_prompt` | renders: note-prompts.ts:140 journal prompt fallback

**beginner**

> Have you picked your pumpkins yet?

**seasoned**

> Have you harvested? How is the cure and storage going?

---

### 13. `slicing-cucumber` -- `failure_diagnostics[3].what_happened`

- index 12162 | family `failure_diagnostics[] :: what_happened` | renders: CommonProblemsCard.astro:93

**beginner**

> Powdery mildew, a white coating on the leaves, spread until the leaves died and the plant stopped early. Downy mildew, with yellow patches and fuzzy gray undersides, does similar damage in damp weather.

**seasoned**

> Powdery mildew defoliated the plant ahead of schedule. The white fungal coating spread across the leaves until they browned and died, cutting the productive season short and exposing fruit to sunscald. Downy mildew (yellow vein-bounded blotches with gray underside) does the same in humid weather.

---

### 14. `sunflower-sprouts` -- `yield_expectations.per_plant`

- index 13135 | family `yield_expectations :: per_plant` | renders: HarvestYieldPair.astro / guide-chapters.ts:214

**beginner**

> You measure sunflower shoots by the tray, not by each plant. Because the seedlings are big and hearty, a full tray gives a generous handful, more than most microgreens.

**seasoned**

> Yield is measured per tray, not per plant: sunflower shoots are among the heavier-yielding microgreens because the seedlings are large and substantial, so a well-sown 1020 tray returns a generous single cut.

---

### 15. `viola` -- `watering.schedule_by_stage[1].note`

- index 14108 | family `watering.schedule_by_stage[] :: note` | renders: stage-watering.ts:24 -> guide-journey.ts:48

**beginner**

> Keep the young plants evenly watered, letting the surface dry a little between waterings.

**seasoned**

> Grow the shallow-rooted seedlings on with even moisture, letting the surface dry slightly between waterings to protect the crown.

---

## B. The non-string pairs -- a schema question, not part of the 15

Type census over all 20,168 pairs, by `(beginner, seasoned)`:

| beginner | seasoned | pairs |
| -- | -- | -- |
| `str` | `str` | 20,084 |
| `list` | `list` | 50 |
| `bool` | `bool` | 17 |
| `str` | `bool` | 15 |
| `str` | `list` | 2 |

**That reconciles the audit's denominator exactly.** The whole-file audit reported "77 cosmetic
pairs of 20,084". 20,084 is precisely the `str`/`str` count -- so the audit was measuring string
pairs only, and the 84-pair gap to 20,168 is entirely the non-string rows below. Its denominator
was not wrong, it was narrower than stated.

---

### B1. All 17 `bool` pairs

Every one is `start_method.hardening_off`. Sorted by crop.

| crop | path | beginner | seasoned | render |
| -- | -- | -- | -- | -- |
| `arugula` | `start_method.hardening_off` | `false` | `false` | A |
| `basil` | `start_method.hardening_off` | `true` | `true` | A |
| `bok-choy` | `start_method.hardening_off` | `true` | `true` | A |
| `broccoli` | `start_method.hardening_off` | `true` | `true` | A |
| `brussels-sprouts` | `start_method.hardening_off` | `true` | `true` | A |
| `cabbage` | `start_method.hardening_off` | `true` | `true` | A |
| `cauliflower` | `start_method.hardening_off` | `true` | `true` | A |
| `chives` | `start_method.hardening_off` | `true` | `true` | A |
| `cilantro-coriander` | `start_method.hardening_off` | `false` | `false` | A |
| `collards` | `start_method.hardening_off` | `true` | `true` | A |
| `dill` | `start_method.hardening_off` | `false` | `false` | A |
| `kale` | `start_method.hardening_off` | `true` | `true` | A |
| `kohlrabi` | `start_method.hardening_off` | `true` | `true` | A |
| `lemongrass` | `start_method.hardening_off` | `true` | `true` | A |
| `mint` | `start_method.hardening_off` | `true` | `true` | A |
| `parsley` | `start_method.hardening_off` | `true` | `true` | A |
| `spinach` | `start_method.hardening_off` | `false` | `false` | A |

---

### B2. All 50 `list` pairs

**`grapefruit` -- `companions.bad`** (family `companions :: bad`, render A)

- beginner: `[{"name": "Turf grass", "why_beginner": "Lawn grass under the tree steals the water and food a big grapefruit's shallow roots need. A ring of mulch, kept back from the trunk, is better than grass.", "provenance": {"label": "extension_backed", "confidence": "medium", "reason": "Beginner-register version of the citrus-grass-competition concern; standard extension citrus guidance. extension_backed/medium.", "verified_against_sources": true}}, {"name": "Bermuda grass", "why_beginner": "A tough, spreading lawn grass that competes hard for water and is difficult to keep out of the root zone. Clear it out to the edge of the branches.", "provenance": {"label": "extension_backed", "confidence": "medium", "reason": "Same citrus-grass-competition basis; Bermuda is a highly competitive, aggressively spreading turf that appears in citrus orchard-floor literature. extension_backed/medium.", "verified_against_sources": true}}]`
- seasoned: `[{"name": "Other seed-bearing citrus nearby", "why_seasoned": "Grapefruit does not need a pollinizer, and planting a seedy citrus close by works against a low-seed grapefruit rather than for it. White Marsh and the red grapefruit sports are low-seeded to nearly seedless when grown in isolation, but bees moving pollen from a nearby seed-bearing citrus can fertilize the flowers and raise the seed count in the fruit. This is not a pest or disease issue, just a fruit-quality one: if seedlessness matters to you, give a low-seed grapefruit some distance from other pollen-heavy citrus.", "provenance": {"label": "extension_backed", "confidence": "medium", "reason": "Cross-pollination raising seed count in otherwise low-seed citrus is documented citrus horticulture (seedless citrus set more seeds when cross-pollinated by nearby pollen-bearing trees). extension_backed/medium: the mechanism is well established; the field magnitude depends on bee activity and variety.", "verified_against_sources": true}}]`

**`orange-navel` -- `companions.bad`** (family `companions :: bad`, render A)

- beginner: `[{"name": "Turf grass", "why_beginner": "Lawn grass under the tree steals the water and food the orange's shallow roots need. A ring of mulch, kept back from the trunk, is better than grass.", "provenance": {"label": "extension_backed", "confidence": "medium", "reason": "Beginner-register version of the citrus-grass-competition concern; same UF/IFAS basis. extension_backed/medium.", "verified_against_sources": true}}, {"name": "Bermuda grass", "why_beginner": "A tough, spreading lawn grass that competes hard for water and is difficult to keep out of the root zone. Clear it out to the edge of the branches.", "provenance": {"label": "extension_backed", "confidence": "medium", "reason": "Same citrus-grass-competition basis (UF/IFAS); Bermuda (Cynodon dactylon) is specifically a highly competitive, aggressively spreading turf and appears in the citrus literature as orchard-floor vegetation. extension_backed/medium.", "verified_against_sources": true}}]`
- seasoned: `[{"name": "Pigeon pea", "why_seasoned": "Pigeon pea is a nitrogen-fixing legume, so it looks like a natural cover crop for citrus, but it carries a specific strike against it. Research testing whether legumes shelter the citrus root weevil (Diaprepes abbreviatus) found that pigeon pea actually supported the weevil's larval development, sustaining a pest whose larvae feed on citrus roots instead of starving it out. The important context for most navel growers: this weevil is established in Florida and the Caribbean, not in the arid citrus regions of California and Arizona, so if you are growing navels in the West, pigeon pea's worst property is not a live threat in your area. The reason to skip it anyway is that the same research also flagged possible chemical interference from pigeon pea on citrus roots, which is not regional, and you give up nothing by choosing a cool-season legume like fava or a clover cover instead. Those deliver the same nitrogen benefit with no root-pest baggage.", "provenance": {"label": "research_backed", "confidence": "medium", "reason": "Demoted from good_seasoned to bad_seasoned on a measured adverse finding. Lapointe (2003), cited in the peer-reviewed Strauss et al. 2024 HortTechnology review (ASHS), tested whether pigeon pea, pinto peanut, and rattlebox serve as a refuge for Diaprepes abbreviatus and found pigeon pea SUPPORTED weevil larval development (the certified, weight-bearing finding), and noted POTENTIAL allelopathic effects on citrus roots (softer strand, source's own hedge). research_backed/medium: the weevil-refuge effect is a measured experimental result (earns research_backed), confidence medium because (a) the headline practical risk (Diaprepes) is region-specific to FL/Caribbean and absent in arid CA/AZ navel regions, and (b) the allelopathy strand is 'potential', not established. Net: a real, research-backed reason to avoid pigeon pea in citrus, with the regional scope stated honestly in the prose.", "verified_against_sources": true}}]`

**`grapefruit` -- `companions.good`** (family `companions :: good`, render A)

- beginner: `[{"name": "White clover", "why_beginner": "A low clover outside the trunk area acts as a living mulch and adds a little nitrogen, without stealing water the way lawn grass does.", "provenance": {"label": "extension_backed", "confidence": "medium", "reason": "Legume living-mulch / cover in citrus is extension-supported for soil nitrogen and organic matter; medium because citrus-specific nitrogen transfer is site-dependent and clover also competes for water.", "verified_against_sources": true}}, {"name": "Nasturtium", "why_beginner": "An easy flower that covers bare soil and draws in helpful insects. Keep it out from the trunk so it does not crowd the base.", "provenance": {"label": "traditional", "confidence": "medium", "reason": "Nasturtium aphid trap-crop and pollinator draw is a well-documented general function that transfers reasonably to citrus aphids; no grapefruit-specific trial located. traditional/medium.", "verified_against_sources": false}}]`
- seasoned: `[{"name": "Fava bean", "why_seasoned": "A cool-season nitrogen fixer that can be grown beyond the dripline as a cover, then cut and dropped to feed the soil without crowding the tree.", "provenance": {"label": "extension_backed", "confidence": "medium", "reason": "Legume winter cover crops in citrus are extension-supported for soil nitrogen and organic matter; medium because the citrus-specific nitrogen-transfer magnitude is site and timing dependent.", "verified_against_sources": true}}]`

**`mandarin-clementine` -- `companions.good`** (family `companions :: good`, render A)

- beginner: `[{"name": "White clover", "why_beginner": "A low clover outside the trunk area works as a living mulch and adds a little nitrogen, without stealing water the way lawn grass does.", "provenance": {"label": "extension_backed", "confidence": "medium", "reason": "Legume living-mulch / cover crop under citrus is extension-supported for soil nitrogen and organic matter; medium because citrus-specific nitrogen transfer is site-dependent and clover also competes for water.", "verified_against_sources": true}}, {"name": "Marigold", "why_beginner": "A simple flower that brings in helpful insects and fills bare ground around the tree. Plant it beyond the trunk, not tight against it.", "provenance": {"label": "traditional", "confidence": "medium", "reason": "Marigold beneficial-insect draw and root-knot nematode suppression are partly grounded as general mechanisms; applied to citrus by analogy, no mandarin-specific trial located.", "verified_against_sources": false}}]`
- seasoned: `[{"name": "Fava bean", "why_seasoned": "A cool-season nitrogen fixer grown beyond the dripline as a winter cover, then cut and dropped to feed the soil without crowding the tree.", "provenance": {"label": "extension_backed", "confidence": "medium", "reason": "Cool-season legume cover crops in citrus are extension-supported for soil nitrogen and organic matter; medium because citrus-specific nitrogen-transfer magnitude is site and timing dependent.", "verified_against_sources": true}}]`

**`orange-navel` -- `companions.good`** (family `companions :: good`, render A)

- beginner: `[{"name": "White clover", "why_beginner": "A low clover outside the trunk area acts as a living mulch and adds a little nitrogen, without stealing water the way lawn grass does.", "provenance": {"label": "extension_backed", "confidence": "medium", "reason": "Clover as a citrus living-mulch/cover crop is extension-supported (UF/IFAS citrus cover-crop program names clovers among legume covers contributing soil N; clover N-fixation nodules pictured in UF/IFAS materials). extension_backed/medium: extension-documented legume-cover benefit; medium because citrus-specific N transfer is site-dependent and clover also competes for water.", "verified_against_sources": true}}, {"name": "Nasturtium", "why_beginner": "An easy flower that covers bare soil and draws in helpful insects. Keep it out from the trunk so it does not crowd the base.", "provenance": {"label": "traditional", "confidence": "medium", "reason": "Nasturtium aphid trap-crop + pollinator draw is well documented as a general function and transfers reasonably to citrus aphids; no citrus-specific trial located. traditional/medium (general trap-crop function applied to citrus by sound analogy).", "verified_against_sources": false}}, {"name": "Marigold", "why_beginner": "A simple flower that brings in helpful insects and fills bare ground around the tree. Plant it beyond the trunk, not tight against it.", "provenance": {"label": "traditional", "confidence": "medium", "reason": "Marigold nematode-suppression (French marigold vs root-knot nematode) is a real, partly-research-backed mechanism, but its application as a citrus companion is general rather than citrus-trial-specific; pollinator/beneficial draw is sound. traditional/medium (kept traditional because the citrus-specific benefit is by analogy; the nematode mechanism alone could argue mechanistic, flagged).", "verified_against_sources": false}}]`
- seasoned: `[{"name": "Fava bean", "why_seasoned": "A cool-season nitrogen fixer that can be grown beyond the dripline as a cover, then cut and dropped to feed the soil without crowding the tree.", "provenance": {"label": "extension_backed", "confidence": "medium", "reason": "Legume winter cover crops in citrus are extension-supported for soil N and organic matter (UF/IFAS citrus cover-crop program; California winter legume covers widely used in orchards). Fava is a standard cool-season legume cover. extension_backed/medium: the legume-cover soil-fertility benefit is extension-documented; medium because the citrus-specific N-transfer magnitude is acknowledged by UF/IFAS as not fully quantified in perennial systems and is site/timing dependent.", "verified_against_sources": true}}]`

**`acorn-squash` -- `soil.preferred_texture`** (family `soil :: preferred_texture`, render C)

- beginner: `["loam", "sandy loam"]`
- seasoned: `["loam", "sandy loam"]`

**`banana-pepper` -- `soil.preferred_texture`** (family `soil :: preferred_texture`, render C)

- beginner: `["loam", "sandy loam", "silt loam"]`
- seasoned: `["loam", "sandy loam", "silt loam"]`

**`bell-pepper` -- `soil.preferred_texture`** (family `soil :: preferred_texture`, render C)

- beginner: `["loam", "sandy loam", "silt loam"]`
- seasoned: `["loam", "sandy loam", "silt loam"]`

**`butternut-squash` -- `soil.preferred_texture`** (family `soil :: preferred_texture`, render C)

- beginner: `["loam", "sandy loam"]`
- seasoned: `["loam", "sandy loam"]`

**`cantaloupe` -- `soil.preferred_texture`** (family `soil :: preferred_texture`, render C)

- beginner: `["sandy loam", "light sandy soil"]`
- seasoned: `["sandy loam", "loamy sand"]`

**`cucumber` -- `soil.preferred_texture`** (family `soil :: preferred_texture`, render C)

- beginner: `["loam", "sandy loam"]`
- seasoned: `["loam", "sandy loam"]`

**`eggplant` -- `soil.preferred_texture`** (family `soil :: preferred_texture`, render C)

- beginner: `["loam", "sandy loam", "silt loam"]`
- seasoned: `["loam", "sandy loam", "silt loam"]`

**`english-cucumber` -- `soil.preferred_texture`** (family `soil :: preferred_texture`, render C)

- beginner: `["loam", "sandy loam"]`
- seasoned: `["loam", "sandy loam"]`

**`honeydew-melon` -- `soil.preferred_texture`** (family `soil :: preferred_texture`, render C)

- beginner: `["sandy loam", "light sandy soil"]`
- seasoned: `["sandy loam", "loamy sand"]`

**`jalapeno` -- `soil.preferred_texture`** (family `soil :: preferred_texture`, render C)

- beginner: `["loam", "sandy loam", "silt loam"]`
- seasoned: `["loam", "sandy loam", "silt loam"]`

**`pickling-cucumber` -- `soil.preferred_texture`** (family `soil :: preferred_texture`, render C)

- beginner: `["loam", "sandy loam"]`
- seasoned: `["loam", "sandy loam"]`

**`pumpkin` -- `soil.preferred_texture`** (family `soil :: preferred_texture`, render C)

- beginner: `["loam", "sandy loam"]`
- seasoned: `["loam", "sandy loam"]`

**`slicing-cucumber` -- `soil.preferred_texture`** (family `soil :: preferred_texture`, render C)

- beginner: `["loam", "sandy loam"]`
- seasoned: `["loam", "sandy loam"]`

**`spaghetti-squash` -- `soil.preferred_texture`** (family `soil :: preferred_texture`, render C)

- beginner: `["loam", "sandy loam"]`
- seasoned: `["loam", "sandy loam"]`

**`watermelon` -- `soil.preferred_texture`** (family `soil :: preferred_texture`, render C)

- beginner: `["sandy loam", "light sandy soil"]`
- seasoned: `["sandy loam", "loamy sand"]`

**`acorn-squash` -- `soil.problematic_texture`** (family `soil :: problematic_texture`, render C)

- beginner: `["heavy clay", "compacted clay"]`
- seasoned: `["heavy clay", "compacted clay"]`

**`banana-pepper` -- `soil.problematic_texture`** (family `soil :: problematic_texture`, render C)

- beginner: `["heavy clay", "compacted clay", "poorly drained clay"]`
- seasoned: `["heavy clay", "compacted clay", "poorly drained clay"]`

**`bell-pepper` -- `soil.problematic_texture`** (family `soil :: problematic_texture`, render C)

- beginner: `["heavy clay", "compacted clay", "poorly drained clay"]`
- seasoned: `["heavy clay", "compacted clay", "poorly drained clay"]`

**`butternut-squash` -- `soil.problematic_texture`** (family `soil :: problematic_texture`, render C)

- beginner: `["heavy clay", "compacted clay"]`
- seasoned: `["heavy clay", "compacted clay"]`

**`cantaloupe` -- `soil.problematic_texture`** (family `soil :: problematic_texture`, render C)

- beginner: `["heavy clay", "wet, poorly drained clay"]`
- seasoned: `["heavy clay", "poorly drained clay"]`

**`cucumber` -- `soil.problematic_texture`** (family `soil :: problematic_texture`, render C)

- beginner: `["heavy clay", "compacted clay"]`
- seasoned: `["heavy clay", "compacted clay"]`

**`eggplant` -- `soil.problematic_texture`** (family `soil :: problematic_texture`, render C)

- beginner: `["heavy clay", "compacted clay", "poorly drained clay"]`
- seasoned: `["heavy clay", "compacted clay", "poorly drained clay"]`

**`english-cucumber` -- `soil.problematic_texture`** (family `soil :: problematic_texture`, render C)

- beginner: `["heavy clay", "compacted clay"]`
- seasoned: `["heavy clay", "compacted clay"]`

**`honeydew-melon` -- `soil.problematic_texture`** (family `soil :: problematic_texture`, render C)

- beginner: `["heavy clay", "wet, poorly drained clay"]`
- seasoned: `["heavy clay", "poorly drained clay"]`

**`jalapeno` -- `soil.problematic_texture`** (family `soil :: problematic_texture`, render C)

- beginner: `["heavy clay", "compacted clay", "poorly drained clay"]`
- seasoned: `["heavy clay", "compacted clay", "poorly drained clay"]`

**`pickling-cucumber` -- `soil.problematic_texture`** (family `soil :: problematic_texture`, render C)

- beginner: `["heavy clay", "compacted clay"]`
- seasoned: `["heavy clay", "compacted clay"]`

**`pumpkin` -- `soil.problematic_texture`** (family `soil :: problematic_texture`, render C)

- beginner: `["heavy clay", "compacted clay"]`
- seasoned: `["heavy clay", "compacted clay"]`

**`slicing-cucumber` -- `soil.problematic_texture`** (family `soil :: problematic_texture`, render C)

- beginner: `["heavy clay", "compacted clay"]`
- seasoned: `["heavy clay", "compacted clay"]`

**`spaghetti-squash` -- `soil.problematic_texture`** (family `soil :: problematic_texture`, render C)

- beginner: `["heavy clay", "compacted clay"]`
- seasoned: `["heavy clay", "compacted clay"]`

**`watermelon` -- `soil.problematic_texture`** (family `soil :: problematic_texture`, render C)

- beginner: `["heavy clay", "wet, poorly drained clay"]`
- seasoned: `["heavy clay", "poorly drained clay"]`

**`acorn-squash` -- `soil.tolerated_texture`** (family `soil :: tolerated_texture`, render C)

- beginner: `["sandy loam", "clay loam", "silt loam"]`
- seasoned: `["sandy loam", "clay loam", "silt loam"]`

**`banana-pepper` -- `soil.tolerated_texture`** (family `soil :: tolerated_texture`, render C)

- beginner: `["loamy sand", "sandy clay loam", "clay loam"]`
- seasoned: `["loamy sand", "sandy clay loam", "clay loam"]`

**`bell-pepper` -- `soil.tolerated_texture`** (family `soil :: tolerated_texture`, render C)

- beginner: `["loamy sand", "sandy clay loam", "clay loam"]`
- seasoned: `["loamy sand", "sandy clay loam", "clay loam"]`

**`butternut-squash` -- `soil.tolerated_texture`** (family `soil :: tolerated_texture`, render C)

- beginner: `["sandy loam", "clay loam", "silt loam"]`
- seasoned: `["sandy loam", "clay loam", "silt loam"]`

**`cantaloupe` -- `soil.tolerated_texture`** (family `soil :: tolerated_texture`, render C)

- beginner: `["loam", "sandy soil", "silt loam"]`
- seasoned: `["loam", "sandy soil", "silt loam"]`

**`cucumber` -- `soil.tolerated_texture`** (family `soil :: tolerated_texture`, render C)

- beginner: `["sandy loam", "clay loam", "silt loam"]`
- seasoned: `["sandy loam", "clay loam", "silt loam"]`

**`eggplant` -- `soil.tolerated_texture`** (family `soil :: tolerated_texture`, render C)

- beginner: `["loamy sand", "sandy clay loam", "clay loam"]`
- seasoned: `["loamy sand", "sandy clay loam", "clay loam"]`

**`english-cucumber` -- `soil.tolerated_texture`** (family `soil :: tolerated_texture`, render C)

- beginner: `["sandy loam", "clay loam", "silt loam"]`
- seasoned: `["sandy loam", "clay loam", "silt loam"]`

**`honeydew-melon` -- `soil.tolerated_texture`** (family `soil :: tolerated_texture`, render C)

- beginner: `["loam", "sandy soil", "silt loam"]`
- seasoned: `["loam", "sandy soil", "silt loam"]`

**`jalapeno` -- `soil.tolerated_texture`** (family `soil :: tolerated_texture`, render C)

- beginner: `["loamy sand", "sandy clay loam", "clay loam"]`
- seasoned: `["loamy sand", "sandy clay loam", "clay loam"]`

**`pickling-cucumber` -- `soil.tolerated_texture`** (family `soil :: tolerated_texture`, render C)

- beginner: `["sandy loam", "clay loam", "silt loam"]`
- seasoned: `["sandy loam", "clay loam", "silt loam"]`

**`pumpkin` -- `soil.tolerated_texture`** (family `soil :: tolerated_texture`, render C)

- beginner: `["sandy loam", "clay loam", "silt loam"]`
- seasoned: `["sandy loam", "clay loam", "silt loam"]`

**`slicing-cucumber` -- `soil.tolerated_texture`** (family `soil :: tolerated_texture`, render C)

- beginner: `["sandy loam", "clay loam", "silt loam"]`
- seasoned: `["sandy loam", "clay loam", "silt loam"]`

**`spaghetti-squash` -- `soil.tolerated_texture`** (family `soil :: tolerated_texture`, render C)

- beginner: `["sandy loam", "clay loam", "silt loam"]`
- seasoned: `["sandy loam", "clay loam", "silt loam"]`

**`watermelon` -- `soil.tolerated_texture`** (family `soil :: tolerated_texture`, render C)

- beginner: `["loam", "sandy soil", "silt loam"]`
- seasoned: `["loam", "sandy soil", "silt loam"]`

---

### B3. FLAGGED -- 17 pairs whose two registers are DIFFERENT TYPES

Not requested, and deliberately excluded from the 17 and the 50 so those counts stay exactly as
asked. Surfaced because they are the same schema question in its sharpest form: here one register
is prose and its sibling is not.

**`bee-balm` -- `description`** (str -> list, family `(crop root) :: description`, render A)

- beginner (`str`):

  > Bee balm is a hardy perennial flower, meaning it comes back every year, grown mostly to bring bees, butterflies, and especially hummingbirds to your garden. It has shaggy, colorful flower heads in red, pink, or purple on tall stems, and minty-smelling leaves you can dry for tea. It blooms in mid to late summer and is very cold-hardy. It spreads by underground roots, so give it room or grow it in a pot. Its one big problem is powdery mildew, a white powder on the leaves, so plant it in full sun, leave space between plants for air, keep the soil moist, and pick mildew-resistant types.

- seasoned (`list`):

  > ["Bee balm (Monarda didyma and the native wild bergamot M. fistulosa) is a hardy herbaceous perennial in the mint family (Lamiaceae), native to North America and grown as a top pollinator and hummingbird plant. Clump-forming and spreading by rhizomes, it sends up 2 to 4 foot, square, aromatic stems topped with shaggy, whorled heads of tubular flowers in red, pink, or lavender through mid to late summer. It is cold-hardy (roughly zones 3 to 9), a premier nectar source for bumblebees, long-tongued bees, butterflies, and ruby-throated hummingbirds, and its minty leaves make Oswego tea. Its defining problem is powdery mildew, so the core care is full sun, airflow through spacing and division, even moisture, and mildew-resistant cultivars."]

**`honeydew-melon` -- `harvest_ready`** (str -> list, family `(crop root) :: harvest_ready`, render A)

- beginner (`str`):

  > You pick a honeydew once, when it is fully ripe, and it will not get any sweeter after you cut it, so timing matters and it is trickier than a cantaloupe. Honeydew does not pop off the vine on its own, so you have to judge it. Look for several signs together: the smooth skin turns from green to a creamy white or pale yellow; the surface goes from hard and slick to a waxy, slightly sticky feel; the blossom end (the end away from the stem) softens a little when you press it and smells faintly sweet; and the pale spot where it sits on the ground turns cream. Cut it off the vine with a knife, leaving a short piece of stem, since it will not come off by itself. The creamy skin plus a slightly soft, sweet-smelling blossom end is your best check.

- seasoned (`list`):

  > ["Honeydew is harvested once, at full ripeness, and does not sweeten further after cutting, so reading the plant correctly is everything, and it is harder to read than cantaloupe. Unlike cantaloupe, honeydew does NOT slip from the vine, so there is no clean release to tell you it is ready. Instead judge by several signs together: the smooth rind changes from green or greenish white to a creamy white or pale, buttery yellow; its surface shifts from hard and slick to a waxy feel that turns slightly tacky, almost sticky, when fully ripe; the blossom end (opposite the stem) softens slightly and gives a little to gentle thumb pressure; a faint sweet aroma develops at that blossom end; and the ground spot where the melon rests pales to cream. Because it will not detach on its own, cut the fruit from the vine with shears or a knife, leaving a short stub of stem. Learning the creamy-rind and softening-blossom-end pair is the most reliable check, and it takes a season or two to get your eye in."]

**`beefsteak-tomato` -- `start_method.hardening_off`** (str -> bool, family `start_method :: hardening_off`, render A)

- beginner (`str`):

  > Hardening off means gradually introducing your seedlings to outdoor conditions before transplanting. Start about a week before your planned transplant date: put the plants outside for a couple of hours in a sheltered, partly shaded spot, then bring them back in. Add more time and more direct sun each day. This helps the plant build up its waxy leaf coating and adjust to outdoor wind and temperature swings. Plants that skip this step often struggle for two to three weeks after transplanting.

- seasoned (`bool`):

  > true

**`beet` -- `start_method.hardening_off`** (str -> bool, family `start_method :: hardening_off`, render A)

- beginner (`str`):

  > You do not need to harden off beets. They are sown straight into the garden from seed, not started indoors and transplanted.

- seasoned (`bool`):

  > false

**`carrot` -- `start_method.hardening_off`** (str -> bool, family `start_method :: hardening_off`, render A)

- beginner (`str`):

  > You do not need to harden off carrots. They are sown straight into the garden from seed, not started indoors and transplanted.

- seasoned (`bool`):

  > false

**`celery` -- `start_method.hardening_off`** (str -> bool, family `start_method :: hardening_off`, render A)

- beginner (`str`):

  > Yes, harden celery off before transplanting, but do it by gradually reducing water rather than by exposing the plants to cold. Celery is unusual here: chilling the seedlings to toughen them can backfire and make them bolt later, so ease them outdoors over 7 to 10 days into mild, not cold, conditions.

- seasoned (`bool`):

  > true

**`cherry-tomato` -- `start_method.hardening_off`** (str -> bool, family `start_method :: hardening_off`, render A)

- beginner (`str`):

  > These plants were raised indoors and have never felt wind, direct sun, or cool nights. Hardening off means introducing them to outdoor life slowly over 7 to 10 days, starting with a few hours outside in a sheltered spot the first day, then more time and more sun each day. Skip this step and the plants will sulk for weeks after transplanting, or the leaves will scorch on the first sunny day. It is not optional for tomatoes.

- seasoned (`bool`):

  > true

**`grape-tomato` -- `start_method.hardening_off`** (str -> bool, family `start_method :: hardening_off`, render A)

- beginner (`str`):

  > These plants were raised indoors and have never felt wind, direct sun, or cool nights. Hardening off means introducing them to outdoor life slowly over 7 to 10 days, starting with a few hours outside in a sheltered spot the first day, then more time and more sun each day. Skip this step and the plants will sulk for weeks after transplanting, or the leaves will scorch on the first sunny day. It is not optional for tomatoes.

- seasoned (`bool`):

  > true

**`heirloom-tomato` -- `start_method.hardening_off`** (str -> bool, family `start_method :: hardening_off`, render A)

- beginner (`str`):

  > Hardening off means gradually introducing your seedlings to outdoor conditions before transplanting. Start about a week before your planned transplant date: put the plants outside for a couple of hours in a sheltered, partly shaded spot, then bring them back in. Add more time and more direct sun each day. This helps the plant build up its waxy leaf coating and adjust to outdoor wind and temperature swings. Plants that skip this step often struggle for two to three weeks after transplanting.

- seasoned (`bool`):

  > true

**`lettuce-leaf` -- `start_method.hardening_off`** (str -> bool, family `start_method :: hardening_off`, render A)

- beginner (`str`):

  > You do not need to harden off leaf lettuce when you direct sow it. Seeds go straight into the garden. If you instead buy or raise transplants, give them a few days to adjust to outdoor conditions before planting out.

- seasoned (`bool`):

  > false

**`parsnip` -- `start_method.hardening_off`** (str -> bool, family `start_method :: hardening_off`, render A)

- beginner (`str`):

  > You do not need to harden off parsnips. They are sown straight into the garden from seed, not started indoors and transplanted.

- seasoned (`bool`):

  > false

**`potato` -- `start_method.hardening_off`** (str -> bool, family `start_method :: hardening_off`, render A)

- beginner (`str`):

  > You do not harden off potatoes. They are grown from seed pieces planted straight into the ground, not from indoor-raised seedlings, so there is no transplant step.

- seasoned (`bool`):

  > false

**`radish` -- `start_method.hardening_off`** (str -> bool, family `start_method :: hardening_off`, render A)

- beginner (`str`):

  > You do not need to harden off radishes. They are sown straight into the garden from seed, not started indoors and transplanted.

- seasoned (`bool`):

  > false

**`roma-tomato` -- `start_method.hardening_off`** (str -> bool, family `start_method :: hardening_off`, render A)

- beginner (`str`):

  > These plants were raised indoors and have never felt wind, direct sun, or cool nights. Hardening off means introducing them to outdoor life slowly over 7 to 10 days, starting with a few hours outside in a sheltered spot the first day, then more time and more sun each day. Skip this step and the plants will sulk for weeks after transplanting, or the leaves will scorch on the first sunny day. It is not optional for tomatoes.

- seasoned (`bool`):

  > true

**`swiss-chard` -- `start_method.hardening_off`** (str -> bool, family `start_method :: hardening_off`, render A)

- beginner (`str`):

  > You do not need to harden off chard when you direct-sow it. If you start a few plants indoors to transplant, harden them off over about a week before setting them out.

- seasoned (`bool`):

  > false

**`tomatillo` -- `start_method.hardening_off`** (str -> bool, family `start_method :: hardening_off`, render A)

- beginner (`str`):

  > These seedlings were raised indoors and have never felt wind or direct sun. Harden them off over 7 to 10 days: start with a couple of hours outside in a sheltered spot, then add time and sun each day. Skip this and the leaves can scorch or the plants sulk for weeks. Wait until nights are reliably above 55°F before transplanting, tomatillos are frost-tender.

- seasoned (`bool`):

  > true

**`turnip` -- `start_method.hardening_off`** (str -> bool, family `start_method :: hardening_off`, render A)

- beginner (`str`):

  > You do not need to harden off turnips. They are sown straight into the garden from seed, not started indoors and transplanted.

- seasoned (`bool`):

  > false

---

### What B1-B3 add up to

Three distinct schema questions are tangled together under one mechanical definition. They want
separate rulings.

**1. `start_method.hardening_off` carries three different shapes on one key name.**
Of its **120** pairs in the frame: 88 are `str`/`str` prose, **17 are `bool`/`bool`**, and
**15 are `str`/`bool`**. The `str`/`bool` rows are the tell -- the beginner side gets a full
paragraph explaining what hardening off is, and the seasoned side gets `true`. That is not a
register pair with a thin seasoned half; it is a boolean flag and a prose field sharing a key.
The 17 `bool`/`bool` rows have no prose in either register at all, so nothing about them is a
register decision. All 120 are render status A -- `TimingSpineCard.astro:87` and
`StartFromSeedCard.tsx:34` both read this key.

**2. The `soil.*_texture` lists are controlled vocabulary, and 39 of 45 are byte-identical.**
Of the 45 texture pairs, **39 have `beginner == seasoned` exactly**. The 6 that differ are all
melons (watermelon, cantaloupe, honeydew-melon) and they differ only by synonym inside the
vocabulary itself:

| crop | beginner | seasoned |
| -- | -- | -- |
| watermelon / cantaloupe / honeydew | `["sandy loam", "light sandy soil"]` | `["sandy loam", "loamy sand"]` |
| watermelon / cantaloupe / honeydew | `["heavy clay", "wet, poorly drained clay"]` | `["heavy clay", "poorly drained clay"]` |

This is the cosmetic-pair phenomenon in its purest form -- a thesaurus swap with zero information
difference -- occurring in a field where a controlled vocabulary makes the swap self-evidently
wrong rather than debatable. **All 45 are render status C**: the renderers read
`*_texture_core` and `*_texture_seasoned`, so the `_beginner` sibling is read by nothing.

**3. The `companions.good` / `.bad` list pairs are the legacy array split, and the two sides hold
DIFFERENT COMPANIONS.** These 5 pairs are not two registers of one statement. `grapefruit`'s
beginner array is White clover + Nasturtium; its seasoned array is Fava bean. Different plants,
not different wording.

The scope matters for the ruling. **107 of 128 crops still carry a populated legacy
`good_seasoned` / `bad_seasoned` array** alongside the current `good_beginner_seasoned` shape
(whose entries carry per-entry `why_beginner` / `why_seasoned`). But only **3 crops** --
`grapefruit`, `mandarin-clementine`, `orange-navel` -- also populate the legacy `good_beginner`,
and only 2 also populate `bad_beginner`. So the legacy shape is populated nearly roster-wide and
*paired* on 3 crops, which is why only 5 rows surface here. The other 104 crops have
`good_beginner: []`, so they fall into the 683 one-side-empty exclusions rather than into this
frame.

This is the array-level register split that the Register-Bearing-Field Inventory v1.0 put
explicitly **out of scope** at section 5 ("flagged for separate reconciliation") in May. It is
still unreconciled, and the 3 citrus crops are where it became visible.

**Common thread.** All of B1 and B3 sit in render status A -- on a screen today. B2 is entirely
render status C. So the schema question and the render question do not line up, and a ruling that
keys on one will get the other wrong.
