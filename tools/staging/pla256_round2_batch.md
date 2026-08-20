# PLA-256 round 2 -- the stratified draw

Read-only. No canonical change. Drawn from
`tools/staging/pla256_register_pair_frame/_all_records.jsonl` (canonical `be8a6d1e`, 20,168 pairs).
**No similarity score of any kind appears in this file** -- no character overlap, no token ratio,
no diff, no length delta, no sort by anything numeric. The frame carries no similarity field to
begin with.

This draw applies the classification standard written as
`language_and_copy_architecture_v1_3_amendment.md` **§9.1** (the differentiation test), with
**§9.2** (contradictory pairs) and **§9.3** (gloss-avoidance) checked independently per §9.3's
instruction.

**The two strata are not blended.** Per §9.5: the **A rate is the product answer**; the **C rate
tests whether prose nobody renders received less care.** They are reported separately, and no
combined rate should be computed from this file.

---

## Method

### Sort key and start rule -- validated against round 1

Sort key is `(crop_slug, field_path)`, both lexicographic ascending, within each stratum.
Start index is `k // 2`, the same midpoint rule as round 1: deterministic, needs no recorded seed,
avoids the edge bias of starting at 0, and is not chosen by eye.

**Integrity check:** replaying round 1's stated parameters (A-only, `k = 973`, start `486`) against
this sort reproduces **all 15 of round 1's drawn pairs, in order, exactly**. The sort key and the
start rule are therefore the same instrument round 1 used, not a re-implementation that happens to
look similar.

### Exclusions

| exclusion | pairs | stratum |
| -- | -- | -- |
| bool pairs (`value_type == bool`, both halves) | 17 | all A |
| `soil.*_texture` **list-typed** pairs | 45 | all C |
| companion-array pairs (`companions.good` / `.bad`) | 5 | all A |
| mismatched-type pairs (15 `str`/`bool` + 2 `str`/`list`) | 17 | all A |
| already read in round 1 | 15 | all A |
| **total excluded** | **99** | |

The first four are exactly the **84 non-string pairs** of §9.4, so exclusions 1-4 together reduce
the frame to its 20,084 `str`/`str` rows. Round 1's 15 come off the top of that. The classes do not
overlap: each excluded pair falls into exactly one.

### Eligible population per stratum, after exclusions

| stratum | in frame | excluded | **eligible** | drawn |
| -- | -- | -- | -- | -- |
| **A** -- read and rendered | 14,595 | 54 | **14,541** | 30 |
| B -- read, render path unproven | 1,583 | 0 | 1,583 | 0 (not drawn) |
| **C** -- never referenced in either app repo | 3,990 | 45 | **3,945** | 10 |
| total | 20,168 | 99 | 20,069 | 40 |

### Draw parameters

| | stratum A | stratum C |
| -- | -- | -- |
| eligible population `N` | 14,541 | 3,945 |
| sample size `n` | 30 | 10 |
| **interval** `k = N // n` | **484** | **394** |
| **first index** `k // 2` | **242** | **197** |
| last index drawn | 14,278 | 3,743 |
| distinct crops | 30 | 10 |
| distinct field families | 23 | 3 |

Indices are into the **eligible** sorted stratum (post-exclusion), zero-based.

**A indices:** 242, 726, 1210, 1694, 2178, 2662, 3146, 3630, 4114, 4598, 5082, 5566, 6050, 6534, 7018, 7502, 7986, 8470, 8954, 9438, 9922, 10406, 10890, 11374, 11858, 12342, 12826, 13310, 13794, 14278

**C indices:** 197, 591, 985, 1379, 1773, 2167, 2561, 2955, 3349, 3743

No start was rejected and re-drawn in either stratum. Nothing in either sample was chosen for what
it contains.

### Why stratum C lands on only 3 field families

This is C's actual shape, not an artifact of the interval, and it should not be corrected by
re-drawing. The eligible C population is 40 families but is severely concentrated:

| pairs | share of eligible C | family |
| -- | -- | -- |
| 1,808 | 45.8% | `regions.<R> :: region_notes` |
| 214 | 5.4% | `regions.<R> :: chill_basis` |
| 195 | 4.9% | `regions.<R>.resolved_by_zone.<Z> :: synthesis_note` |
| 156 | 4.0% | `regions.<R>.resolved_by_zone.<Z> :: type_note` |
| 121 | 3.1% | `container_notes :: notes` |
| 120 | 3.0% | `container_notes.soil_mix :: type` |
| | | *(34 more families, 33.7% combined)* |

`regions.<R> :: region_notes` alone is **45.8%** of everything that renders nowhere. The draw
returned it 7 times in 10. A systematic draw over a population where one family is nearly half the
rows will look like this, and forcing family spread here would mean sampling something other than
what C is.

This also corroborates a known result rather than surprising it: region prose was already
established as reading nowhere in plant-astro. **The C stratum is, to a first approximation, the
region-notes corpus.** Read that as a constraint on what the C rate can be generalized to.

---

## ⚠ Found while applying the exclusions: `soil.*_texture` carries two shapes, and §9.4 B2 ruled from one

The exclusion list names **45** `soil.*_texture` pairs. The key names
`soil.preferred_texture` / `tolerated_texture` / `problematic_texture` actually carry **138** pairs
in the frame:

| shape | pairs | crops | byte-identical halves | render |
| -- | -- | -- | -- | -- |
| `list` -- controlled vocabulary | **45** | 15 | 39 of 45 | all C |
| `str` -- full prose register pairs | **93** | 31 | **0 of 93** | all C |

§9.4 B2 reads: *"`soil.*_texture` is controlled vocabulary, and the differences are
indefensible."* That is true of the 45 list-typed rows and **false of the other 93**, which are
ordinary multi-sentence prose pairs. Example, `green-beans-bush` `soil.preferred_texture`:

> **beginner:** "Beans grow best in rich, loose soil that drains well. The ideal is loam, a
> balanced soil that holds some moisture but never stays soggy. ..."
> **seasoned:** "Fertile, well-drained loam. Beans set the heaviest pods in soil that holds
> moisture during pod fill yet never stays waterlogged, since soggy ground invites root rot."

**This is the same error §9.4 already recorded against itself.** Its ⚠ note says the first draft
ruled all 17 bool pairs as a boolean that should never have been suffixed, and that this
*"would have deleted 88 explanatory paragraphs"*, because `start_method.hardening_off` carries 120
pairs in three shapes. The lesson it drew was: **a type census over one type is not a census over
one key.** B2 was written the same way -- from the list-typed rows -- and the same correction
applies to it.

**What this draw did about it:** excluded exactly the ruled 45, and left the 93 str-typed rows
**eligible** in stratum C, where they belong -- they are prose register pairs, which is precisely
what round 2 measures. Excluding them would have removed 2.4% of the C population on the strength
of a ruling that does not describe them. §9.4 B2 wants a correction appended; that is a separate
call and is flagged here, not made.

---

## Stratum A -- read and rendered -- 30 pairs

**This is the product answer.** Every pair below is on a screen today; the render evidence per record names the file that reads it.

Eligible population **14,541** | interval **k = 484** | first index **242** | 30 drawn.

### A1. `apple` -- `notifications[2].title`

- index 242 | family `notifications[] :: title` | render **A** -- read and rendered | evidence: PlantNotificationsCard.astro:74

**beginner**

> Late-winter pruning time

**seasoned**

> Time for the annual dormant prune

---

### A2. `arugula` -- `growth_stages[2].log_prompt`

- index 726 | family `growth_stages[] :: log_prompt` | render **A** -- read and rendered | evidence: note-prompts.ts:140 journal prompt fallback

**beginner**

> Ready to start cutting?

**seasoned**

> Ready to start cutting?

---

### A3. `bee-balm` -- `ph.note`

- index 1210 | family `ph :: note` | render **A** -- read and rendered | evidence: PhCard.astro:56 / guide-chapters.ts:169

**beginner**

> Bee balm is easygoing about soil pH (how acidic or alkaline the soil is). A normal garden range around 6.0 to 7.0 suits it, and you usually do not need to change anything.

**seasoned**

> Bee balm is not pH-fussy, performing across roughly slightly acidic to neutral soil (about 6.0 to 7.0) and tolerating a bit outside that. No pH adjustment is typically warranted for it specifically.

---

### A4. `blackberry` -- `pests[1].cause`

- index 1694 | family `pests[] :: cause` | render **A** -- read and rendered | evidence: pest-control.ts OUTDOOR_SLOTS / guide-chapters.ts:118

**beginner**

> A small beetle whose grub tunnels inside new canes and makes a swollen gall. It is common on blackberries, especially near wild brambles.

**seasoned**

> Red-necked cane borer (Agrilus ruficollis), a small metallic-black beetle with a coppery-red thorax whose larva bores into primocanes and causes the diagnostic gall. It is one of the more common blackberry-specific borers, worse near wild brambles.

---

### A5. `broad-beans-fava` -- `diseases[0].organic_treatment`

- index 2178 | family `diseases[] :: organic_treatment` | render **A** -- read and rendered | evidence: pest-control.ts OUTDOOR_SLOTS / guide-chapters.ts:119

**beginner**

> There is no home garden spray for chocolate spot, so you manage it by keeping plants open and dry. At the first spots, thin crowded growth and pull weeds to move air through the planting, pick off the worst leaves, and stay out of the patch when the plants are wet. If an overwintered stand is badly hit, pick what you can and pull the plants.

**seasoned**

> There are no fungicides available to home gardeners for chocolate spot, so management is cultural. At the first spots, improve airflow by thinning crowded growth and pulling weeds, remove the worst-affected leaves, and avoid working among wet plants. On a badly hit overwintered stand, harvesting what is usable and clearing the crop is often the practical choice.

---

### A6. `butternut-squash` -- `watering.signs_overwater`

- index 2662 | family `watering :: signs_overwater` | render **A** -- read and rendered | evidence: WateringCard.astro / guide-chapters.ts:192

**beginner**

> If lower leaves yellow, the plant wilts even though the soil is wet, or fruit and stems go soft and rotten, it is getting too much water or the soil drains poorly.

**seasoned**

> Yellowing lower leaves, wilting even when the soil is wet, and soft, rotting stems or fruit at the base point to overwatering or poor drainage. Saturated soil invites crown and fruit rot, especially on heavy ground.

---

### A7. `cauliflower` -- `fertilizer.notify_message`

- index 3146 | family `fertilizer :: notify_message` | render **A** -- read and rendered | evidence: FeedingCard.astro

**beginner**

> Time to feed your cauliflower.

**seasoned**

> Time to side-dress your cauliflower with nitrogen to keep it growing without a stall.

---

### A8. `cherry-sour` -- `pests[2].organic_treatment`

- index 3630 | family `pests[] :: organic_treatment` | render **A** -- read and rendered | evidence: pest-control.ts OUTDOOR_SLOTS / guide-chapters.ts:119

**beginner**

> Often you can leave it alone, since ladybugs and other helpers clear it by midsummer. On a young tree that is badly hit, blast the colonies off with a hose, or spray the curled tips with insecticidal soap or horticultural oil. Do not over-fertilize, since lush new growth is what the aphids love.

**seasoned**

> Often no action is needed, since beneficials clean it up by midsummer. For a heavy infestation on a young tree, a strong jet of water knocks colonies off, or insecticidal soap or horticultural oil on the curled tips works; protect the ladybugs and lacewings that do most of the control. Avoid high-nitrogen feeding, which fuels the soft growth aphids prefer.

---

### A9. `chives` -- `watering.schedule_by_stage[1].note`

- index 4114 | family `watering.schedule_by_stage[] :: note` | render **A** -- read and rendered | evidence: stage-watering.ts:24 -> guide-journey.ts:48

**beginner**

> Keep the soil evenly moist while a new plant gets going. Water deeply in dry spells, and mulch to hold the moisture.

**seasoned**

> Steady moisture matters most while a new clump puts its root system down; UMN advises watering deeply when rainfall is sparse so the soil does not dry around the roots. Mulch helps hold it for a clump you will cut from for years.

---

### A10. `dill` -- `description`

- index 4598 | family `(crop root) :: description` | render **A** -- read and rendered | evidence: HeroCard.astro / learn/[slug].tsx:292

**beginner**

> Dill gives you two things from one plant: the soft feathery leaves are dill weed, and the flower heads and seeds are what you use for pickling and as a spice. Like cilantro, and unlike warm-season herbs such as basil, dill is a cool-leaning plant. Young plants handle a light frost, but once summer heat and long days arrive it bolts, sending up a tall flower stalk that can reach 3 to 5 feet, and leaf growth slows. So the trick is to grow it for leaves in the cooler parts of the year, spring and again in late summer for fall, and to let the summer plants flower for seed heads. Sow a little every 2 to 3 weeks, since each plant bolts after a while, and plant the seeds right in the garden because dill does not like being moved. It is fast, easy, and reseeds itself, so once you grow it you often get volunteers the next year. And when it bolts, you get dill heads for pickling and dried dill seed.

**seasoned**

> Dill (Anethum graveolens) is an annual herb in the carrot family (Apiaceae) grown for two products from one plant: the feathery leaves are the herb dill weed, and the flower heads and dried seed are used for pickling and as the spice dill seed. Like cilantro, and unlike warm-season herbs such as basil, dill is a cool-leaning crop that bolts once summer heat and long days arrive, sending up a tall flower stalk (the plant reaches 3 to 5 feet in flower) above roughly 75 to 80°F. That shapes how it is grown: the leaf crop favors the cool shoulders of the year, spring and especially a late-summer-into-fall sowing, while the heat of summer is when growers let it run to seed and pickling heads rather than leaves. Because the bolt is fast and inevitable in warmth, dill is a succession crop, sown in small batches every 2 to 3 weeks so fresh, pre-bolt plants keep coming. It is direct-sown (a slender taproot resents transplanting), young plants tolerate light frost, and it self-sows so readily that a patch often returns on its own. It is easy and largely trouble-free, with the black swallowtail caterpillar a welcome visitor as much as a pest. The grower's real skill is timing the leaf crop into the cool seasons and treating the summer bolt as the start of the seed-and-pickling harvest rather than a failure.

---

### A11. `eggplant` -- `pests[2].organic_treatment`

- index 5082 | family `pests[] :: organic_treatment` | render **A** -- read and rendered | evidence: pest-control.ts OUTDOOR_SLOTS / guide-chapters.ts:119

**beginner**

> Blast them off with a strong spray of water and treat the undersides of the leaves with insecticidal soap, repeating every few days. Ladybugs and other helpful insects eat aphids, so welcome them.

**seasoned**

> Knock colonies off with a strong jet of water and spray insecticidal soap or horticultural oil with thorough coverage of leaf undersides, repeating every few days. Conserve ladybugs, lacewings, and parasitic wasps, which usually bring aphids under control.

---

### A12. `fig` -- `fertilizer.amount`

- index 5566 | family `fertilizer :: amount` | render **A** -- read and rendered | evidence: feeding-guide.ts:77 pair(f,'amount')

**beginner**

> A simple guide is about 1/2 pound of 10-10-10 for a young fig and 2 to 4 pounds for a big one, spread over 2 or 3 times from early spring to early summer. Do not put fertilizer in the planting hole or feed right at planting; wait until it starts growing. In cold-winter areas, use half as much.

**seasoned**

> A common home rate is about 1/2 pound of 10-10-10 for a young plant and 2 to 4 pounds for a mature one, split into 2 or 3 applications from early spring through early summer; UGA gives a rule of about 1/2 pound per foot of height, up to 5 pounds a year. Do not fertilize at planting; wait until growth begins. Cut these rates in half in northern gardens to keep growth firm for winter.

---

### A13. `grapefruit` -- `diseases[3].symptoms`

- index 6050 | family `diseases[] :: symptoms` | render **A** -- read and rendered | evidence: pest-control.ts OUTDOOR_SLOTS / guide-chapters.ts:117

**beginner**

> Melanose makes tiny, raised, rough brown specks on the skin of young grapefruit, often in streaks or a mud-splash pattern, and similar spots on leaves and twigs. The fruit inside is fine; it just looks blemished, which shows up on grapefruit's smooth pale skin. It is a warm, wet-climate disease of Florida and the Gulf, worst on old trees with a lot of dead wood.

**seasoned**

> Small, raised, dark brown, sandpaper-rough specks and streaks on the rind of young fruit, and similar spots on leaves and twigs; the specks often form tear-streak or mudcake patterns where spores washed down the fruit. It is a cosmetic rind blemish that does not reach the flesh, but grapefruit's smooth pale peel shows it plainly, downgrading fresh fruit. It is a warm, wet climate disease of the Southeast and Gulf, worst on older trees with dead wood.

---

### A14. `heirloom-tomato` -- `pests[1].prevention`

- index 6534 | family `pests[] :: prevention` | render **A** -- read and rendered | evidence: pest-control.ts OUTDOOR_SLOTS / guide-chapters.ts:120

**beginner**

> Turn or till the soil in autumn to expose and kill overwintering pupae. Planting dill or fennel nearby attracts predatory wasps that prey on hornworms.

**seasoned**

> Till soil in autumn to kill overwintering pupae. Plant dill and basil nearby to attract predatory wasps.

---

### A15. `kohlrabi` -- `soil.preferred_description`

- index 7018 | family `soil :: preferred_description` | render **A** -- read and rendered | evidence: guide-chapters.ts / [zone].astro

**beginner**

> Kohlrabi grows best in fertile, loose, well-drained soil with plenty of compost mixed in, and it likes steady, even moisture. The bulb stays tender and mild when the plant grows quickly without a check, so soil that holds moisture but drains well is ideal. Soil that dries out or stays soggy stresses the plant and makes the stem tough and woody.

**seasoned**

> Kohlrabi does best in a fertile, well-drained loam high in organic matter held at even moisture, like the other cole crops. The whole game is fast, uninterrupted growth: a tender, mild swollen stem forms when the plant never checks, while drought, heat, or a stop-start water supply turns it woody, fibrous, and bitter and can crack it. Work in compost before planting and keep the bed evenly moist. Clubroot, the key brassica soil disease, is far more likely in acidic, poorly drained ground, so keep drainage good and the pH up where it is a concern.

---

### A16. `lemongrass` -- `rotation.avoid_after`

- index 7502 | family `rotation :: avoid_after` | render **A** -- read and rendered | evidence: RotationCard.astro

**beginner**

> Lemongrass is a perennial that stays in one place for years, so you do not rotate it like an annual vegetable. Just give a new clump a sunny, rich, well-drained spot.

**seasoned**

> As a long-lived perennial clump, lemongrass is not part of an annual rotation; it holds its spot for years and is renewed by division rather than replanted each season. If starting a new clump, simply choose a sunny, rich, well-drained site.

---

### A17. `marigold` -- `failure_diagnostics[3].next_season_tip`

- index 7986 | family `failure_diagnostics[] :: next_season_tip` | render **A** -- read and rendered | evidence: CommonProblemsCard.astro:102

**beginner**

> Plant only after your last frost in spring, and know that the first frost in fall ends the marigold season.

**seasoned**

> Direct-sow or transplant only after all frost danger has passed, and expect plants to end with the first fall frost.

---

### A18. `nectarine` -- `failure_diagnostics[0].next_season_tip`

- index 8470 | family `failure_diagnostics[] :: next_season_tip` | render **A** -- read and rendered | evidence: CommonProblemsCard.astro:102

**beginner**

> Plant away from low frost pockets, keep a cover handy for bloom-time frosts, and make sure your variety's chill needs fit your area before counting on a crop.

**seasoned**

> Choose a frost-aware site, keep a frost cover ready for bloom, and confirm your variety's chill requirement suits your region before relying on it for a crop.

---

### A19. `orange-navel` -- `pests[0].symptoms`

- index 8954 | family `pests[] :: symptoms` | render **A** -- read and rendered | evidence: pest-control.ts OUTDOOR_SLOTS / guide-chapters.ts:117

**beginner**

> This tiny brown insect has a distinctive resting posture: it perches on new leaves at an angle, with its rear end raised and pointed upward, which is your identification clue. The young ones produce little waxy white threads and cause the new leaf tips to curl. The real danger is not the feeding itself but a fatal disease the psyllid spreads, citrus greening, so it is worth acting on even where the pest is uncommon.

**seasoned**

> The psyllid itself is a tiny mottled-brown insect, about an eighth of an inch, that feeds tilted up at a 45-degree angle on new flush, a posture no other citrus pest shares. Its nymphs produce distinctive waxy tubules and curl tender new growth; heavy feeding twists and notches expanding leaves. The insect matters less for its direct damage than for what it carries: it is the vector of Huanglongbing (citrus greening), the most serious citrus disease worldwide. Scout the youngest flush, where it concentrates.

---

### A20. `pawpaw` -- `notifications[2].title`

- index 9438 | family `notifications[] :: title` | render **A** -- read and rendered | evidence: PlantNotificationsCard.astro:74

**beginner**

> Flowers are open, time to hand-pollinate

**seasoned**

> Bloom is open, hand-pollinate now

---

### A21. `pear-asian` -- `tips_by_stage.planting[1].text`

- index 9922 | family `tips_by_stage.<stage>[] :: text` | render **A** -- read and rendered | evidence: GrowingJourneyCard.astro:230 / guide-journey.ts:59

**beginner**

> Plant a second, different pear variety at the same time so they can pollinate each other, and check they are compatible (Bartlett and Seckel are not). A single pear, or a mismatched pair, usually makes no fruit.

**seasoned**

> Plant a compatible, bloom-overlapping pollinizer at the same time, a lone pear (or an incompatible pair like Bartlett with Seckel) wastes years.

---

### A22. `plum` -- `diseases[0].prevention`

- index 10406 | family `diseases[] :: prevention` | render **A** -- read and rendered | evidence: pest-control.ts OUTDOOR_SLOTS / guide-chapters.ts:120

**beginner**

> Check the tree every winter and cut out any knots before spring, when they spread. Just as important, clean up or remove wild plums, chokecherries, and neglected ornamental plums nearby, because they keep re-infecting your tree. Some plum varieties resist black knot better than others, so ask when you buy, but cutting the knots out each year is the habit that matters most.

**seasoned**

> Scout and prune out knots every dormant season before they can release spores, and deal with the reservoir: remove or clean up wild plum, chokecherry, and neglected ornamental Prunus within range, which sustain the disease. Choosing a less-susceptible cultivar and keeping the tree open and vigorous both help, but annual knot removal is the non-negotiable habit.

---

### A23. `popcorn` -- `growth_stages[2].user_action`

- index 10890 | family `growth_stages[] :: user_action` | render **A** -- read and rendered | evidence: GrowingJourneyCard.astro / guide-journey.ts:58

**beginner**

> Feed with nitrogen when the plants are about knee-high, and keep the water steady as they shoot up. Pull a little soil around the bases to steady the tall stalks, and avoid injuring them, which can let in disease.

**seasoned**

> Sidedress nitrogen at knee-high and keep moisture steady as the plants stretch up. Hill a little soil around the base for support, and hold off overhead work that could injure stalks and invite smut.

---

### A24. `raspberry` -- `diseases[0].organic_treatment`

- index 11374 | family `diseases[] :: organic_treatment` | render **A** -- read and rendered | evidence: pest-control.ts OUTDOOR_SLOTS / guide-chapters.ts:119

**beginner**

> You cannot fix rotted roots, so it is all about drainage: plant on raised rows, keep water moving away, and replace dead plants on a drier spot.

**seasoned**

> There is no cure once roots rot, so the response is drainage. Plant on tall raised beds or ridges, divert surface water, and replace dead plants with clean stock on a better-drained site.

---

### A25. `sage` -- `growth_stages[1].user_action`

- index 11858 | family `growth_stages[] :: user_action` | render **A** -- read and rendered | evidence: GrowingJourneyCard.astro / guide-journey.ts:58

**beginner**

> Water fairly often until it takes hold, then water deeply but less often. Harvest just a little and pinch it to stay bushy. Do not feed it.

**seasoned**

> Water regularly until settled, then taper toward deep, infrequent watering. Harvest sparingly and pinch to shape. Hold off on fertilizer.

---

### A26. `spaghetti-squash` -- `fertilizer.notes`

- index 12342 | family `fertilizer :: notes` | render **A** -- read and rendered | evidence: FeedingCard.astro:109

**beginner**

> Spaghetti squash grows for a long time and likes steady feeding. Mix a balanced fertilizer into the soil before planting, then feed with a little extra nitrogen about three to four weeks later as the vines start to run, and again when flowers appear. Once the squash begin to form, go easy on the nitrogen, because too much makes leafy vines instead of fruit.

**seasoned**

> Spaghetti squash is a moderate feeder over a long season. Work a complete fertilizer such as 10-10-10 into the bed before planting, then side-dress with nitrogen about three to four weeks after planting as the vines begin to run, and again as flowering starts. Ease off heavy nitrogen once fruit has set, since late, lush vine growth comes at the expense of fruit and draws pests. Pair feeding with even moisture, because the nutrients only help a plant that is not also drought-stressed.

---

### A27. `sugar-snap-peas` -- `companions.good_beginner_seasoned[0].why`

- index 12826 | family `companions.good_beginner_seasoned[] :: why` | render **A** -- read and rendered | evidence: CompanionsCard.astro:200

**beginner**

> A classic cool-season neighbor that shares snap peas' early-spring and fall timing; the carrots root deep while the peas climb, so they use the bed without crowding.

**seasoned**

> Carrots and peas grow in the same cool windows and use the bed in complementary ways: the carrot works the soil deep while the pea climbs above it, and the peas' nitrogen fixation lightly benefits the carrot. The pairing is traditional and compatibility-based rather than a measured pest defense, so expect easy cohabitation more than active protection.

---

### A28. `sweet-pea` -- `failure_diagnostics[4].next_season_tip`

- index 13310 | family `failure_diagnostics[] :: next_season_tip` | render **A** -- read and rendered | evidence: CommonProblemsCard.astro:102

**beginner**

> For mildew, space plants for airflow, water in the morning at the base, and remove bad leaves. For virus, control aphids and thrips and pull out affected plants.

**seasoned**

> For mildew, improve airflow, water at the base early, and remove affected leaves. For virus, control aphids and thrips and rogue out symptomatic plants promptly.

---

### A29. `tomatillo` -- `notifications[0].body`

- index 13794 | family `notifications[] :: body` | render **A** -- read and rendered | evidence: PlantNotificationsCard.astro:82

**beginner**

> Your last frost date is about {{weeks_until_anchor}} weeks away, the right window to start tomatillo seeds indoors. Sow at least two plants (two varieties is even better), because a single tomatillo cannot pollinate itself. Plant a couple of seeds per cell about a quarter inch deep, keep them warm (75 to 85°F), and cover until they sprout.

**seasoned**

> Your last frost date is about {{weeks_until_anchor}} weeks away, the window to start tomatillos indoors. Start two or more plants for cross-pollination. Keep soil at 75 to 85°F and cover until emergence.

---

### A30. `yellow-summer-squash` -- `growth_stages[2].log_prompt`

- index 14278 | family `growth_stages[] :: log_prompt` | render **A** -- read and rendered | evidence: note-prompts.ts:140 journal prompt fallback

**beginner**

> Is your plant growing well?

**seasoned**

> Has your summer squash been side-dressed? Any pests at the stem base?

---

## Stratum C -- never referenced in either app repo -- 10 pairs

**This tests whether prose nobody renders received less care.** No pair below is read by either app repo. Report this rate separately from A's; do not average them.

Eligible population **3,945** | interval **k = 394** | first index **197** | 10 drawn.

### C1. `asparagus` -- `regions.hawaii_tropical.region_notes`

- index 197 | family `regions.<R> :: region_notes` | render **C** -- never referenced in either app repo | evidence: referenced nowhere in either repo (PLA-255 finding)

**beginner**

> Skip asparagus in a tropical, frost-free garden and choose a heat-loving perennial instead; without a real winter dormancy the crowns will not build the reserves a lasting bed needs.

**seasoned**

> A dormancy-dependent temperate perennial marked unsuitable across the frost-free tropical span (zones 10 to 13): without a sustained dormant rest the crown cannot recharge, so stands thin and fade rather than perennializing.

---

### C2. `broccoli` -- `regions.ca_south_coast.region_notes`

- index 591 | family `regions.<R> :: region_notes` | render **C** -- never referenced in either app repo | evidence: referenced nowhere in either repo (PLA-255 finding)

**beginner**

> On California's south coast, broccoli grows through the mild winter and the cooler months around it. Plant transplants starting in January and harvest into late October. Summer is the problem here, not winter: from about June on, it gets too warm for broccoli to form good heads, so don't plant for a summer harvest. Winters are mild with little frost, so the main job is finishing the crop before summer heat. Pick heat-tolerant varieties if you're planting toward the warmer end of the season.

**seasoned**

> On the south coast broccoli is a cool-season crop grown across the long mild winter and shoulders. Transplants go out from about January, heads form through the cool months, and harvest runs into late October. The limit is summer heat: from roughly June onward, warm days push past the heading-stall threshold, so summer is a planting gap rather than a window. The mild winters mean little to no killing frost, so timing is about ending the crop before summer rather than protecting it from cold. Favor heat-tolerant varieties for plantings that push toward the warm shoulders.

---

### C3. `cherry-tomato` -- `regions.mid_south.region_notes`

- index 985 | family `regions.<R> :: region_notes` | render **C** -- never referenced in either app repo | evidence: referenced nowhere in either repo (PLA-255 finding)

**beginner**

> In the Ozark Uplands and Delta Lowlands you can grow cherry tomatoes twice: a spring crop and a real fall crop, with only a short midsummer lull between them. Cherry tomatoes are heat tough, so they keep setting fruit further into summer than big slicers before that lull. Set transplants out about a week after your last frost for fruit through early summer, then set a second round of transplants out in the tight early-July fall window for a second harvest that runs through September.

**seasoned**

> The Ozark Uplands and Delta Lowlands run cherry tomatoes on two frost-bracketed cycles, per the University of Arkansas Cooperative Extension planting tables. Spring transplants go out about a week after the last frost (zone 8 Apr 10 to May 1, zone 7 Apr 17 to May 8) for a harvest through mid to late June. Cherry types set fruit through more of the summer heat than large-fruited tomatoes, so the pause here is short, roughly July. The fall cycle rides the University of Arkansas Cooperative Extension's tight fall transplant window (zone 8 Jul 1 to Jul 15, zone 7 Jun 24 to Jul 8, seed sown indoors about six weeks ahead); the second crop ripens from late August in the uplands and early September in zone 8, running through September.

---

### C4. `field-corn` -- `regions.se_gulf.region_notes`

- index 1379 | family `regions.<R> :: region_notes` | render **C** -- never referenced in either app repo | evidence: referenced nowhere in either repo (PLA-255 finding)

**beginner**

> In the Southeast and Gulf, sow field corn in spring after the last frost and grow it to a summer dry-down. Summers are hot and humid, so the ears may finish drying poorly on the stalk; pick them at hard dent and dry them indoors.

**seasoned**

> The humid Southeast grows field corn as a spring-sown crop that dries down in the heat of summer. The load-bearing risk is a wet, humid finish that molds ripening ears, so harvest at hard dent and cure the ears under cover with airflow rather than leaving them to field-dry.

---

### C5. `lavender` -- `regions.ca_south_coast.region_notes`

- index 1773 | family `regions.<R> :: region_notes` | render **C** -- never referenced in either app repo | evidence: referenced nowhere in either repo (PLA-255 finding)

**beginner**

> Lavender thrives on California's mild southern coast and comes back every year in the ground. Plant it in fall or early spring in a sunny spot with fast-draining soil, and resist the urge to water it often. It flowers from spring into summer, with Spanish lavender starting early. The thing to avoid is soggy soil, which causes rot.

**seasoned**

> On California's mild southern coast, lavender is one of the easiest perennials to grow: the hot dry summers and cool wet winters suit its Mediterranean nature, and it lives in the ground for years as a drought-tolerant woody shrub. Spanish lavender blooms earliest, with English lavender and the lavandins following, giving flowers from spring into summer. Plant in fall or early spring across zones 9 and 10, in full sun and sharply drained soil. The main mistake is too much water and poorly drained soil, which rot the roots, so keep plants lean and dry once established and cut back hard only after bloom.

---

### C6. `mulberry` -- `regions.mid_south.region_notes`

- index 2167 | family `regions.<R> :: region_notes` | render **C** -- never referenced in either app repo | evidence: referenced nowhere in either repo (PLA-255 finding)

**beginner**

> Mulberry is one of the easiest trees in this guide for the Mid-South. Plant a bare-root tree while dormant, away from patios or driveways where dropped fruit will stain.

**seasoned**

> Mulberry needs little winter chill and tolerates this belt's heat and humidity with essentially no disease pressure of note. Plant bare-root trees while dormant, away from hardscape where dropped fruit will stain.

---

### C7. `pea-shoots` -- `container_notes.soil_mix.amendments`

- index 2561 | family `container_notes.soil_mix :: amendments` | render **C** -- never referenced in either app repo | evidence: soil_mix never referenced

**beginner**

> None needed.

**seasoned**

> None; the medium is a substrate, not a nutrient source, for a single cycle.

---

### C8. `pumpkin` -- `container_notes.soil_mix.amendments`

- index 2955 | family `container_notes.soil_mix :: amendments` | render **C** -- never referenced in either app repo | evidence: soil_mix never referenced

**beginner**

> Mix in compost and a slow-release fertilizer at planting. Pots need feeding more often than beds because watering washes nutrients out.

**seasoned**

> Blend in about a third compost plus a slow-release balanced fertilizer at planting. Because frequent watering flushes nutrients, plan to feed a container pumpkin more regularly than one in the ground.

---

### C9. `snow-peas` -- `regions.ca_desert.region_notes`

- index 3349 | family `regions.<R> :: region_notes` | render **C** -- never referenced in either app repo | evidence: referenced nowhere in either repo (PLA-255 finding)

**beginner**

> In the desert valleys, grow snow peas in winter. Plant in fall for a harvest from December through spring, and skip the long hot summer, when peas cannot grow.

**seasoned**

> In California's desert valleys snow peas are a winter crop. Sow in October and November for a harvest from December through April, and leave out the long, intense heat from May into September, a true heat exclusion when peas cannot flower or set pods.

---

### C10. `thyme` -- `soil_prep`

- index 3743 | family `(crop root) :: soil_prep` | render **C** -- never referenced in either app repo | evidence: no reference in either repo

**beginner**

> Pick the sunniest spot with the best drainage. Mix only a little coarse compost into the soil. If your ground is heavy clay, plant thyme in a raised bed or mound instead, because that drains better. The goal is poor, gritty soil, not rich soil.

**seasoned**

> Choose the sunniest, best-draining spot you have. Work only a little coarse compost into lean soil, and on heavy clay improve drainage with a raised bed or mound rather than digging in sand, which can worsen clay. Aim for lean, gritty, neutral to slightly alkaline ground; thyme does not want rich soil.

---

## Reporting contract for this batch

When these 40 are read and classified under §9.1:

1. **Two rates, never one.** Stratum A `x/30`, stratum C `y/10`. No blended figure. §9.5 is
   explicit that a rate across all pairs is *"honest about the dataset and misleading about the
   product."*
2. **State the borderline band per stratum.** Round 1's band was 5 of 15 and that width is why the
   rate was reported as a 27%-60% range. §9.5 predicts the band should narrow now that the classes
   exist; whether it actually did is a finding about the standard, not just about the data.
3. **C's rate generalizes to region prose, not to "unrendered prose" in general** -- 7 of its 10
   pairs are `region_notes`. Say so when quoting the number.
4. **§9.2 and §9.3 are checked independently**, on every pair, including pairs that pass §9.1.
   A substantive pair can still be contradictory or gloss-avoidant.
5. **n = 10 in stratum C is a direction, not an estimate.** It answers "is C visibly worse than
   A" and does not carry a confidence interval worth quoting.

