# Roster gap review -- which parent crops are missing (PLA-635)

**Status:** SCOPING. Partly ruled 2026-09-30 (section 0a); the remaining buckets await Trevor. Nothing here authorizes adding a crop. Read-only on the
canonical; no schema change, no sourcing pass. Measured 2026-09-30 on canonical `00dda31c`
(origin/main `3ba3460`, branch `main`, HEAD == origin/main).

**Ruling buckets (the ticket's):** FIRST BATCH / LATER / VARIETY NOT PARENT / NO SOURCE PATH. Every
row below carries a *proposed* bucket; Trevor rules.

## 0a. Rulings of 2026-09-30 (Trevor): "follow what UC says"

These supersede any conflicting row below. UC's garden publications group crops by market name
(Mauk & Shea, UCCE Riverside: "B. Lemons, C. Limes, D. Oranges, F. Kumquats"; one UC IPM page per
crop), and separately document how each type behaves. The working rule: follow UC's behavior
evidence, and split only where that behavior means one crop entry cannot be right.

| item | ruling | the UC evidence |
|---|---|---|
| **Persimmon** | **SPLIT** into `persimmon` (Asian, *D. kaki*) and `persimmon-american` (*D. virginiana*: Meader, Prok) | UC IPM: *"There are two kinds of persimmons grown in the West: the American persimmon and the Japanese or Oriental persimmon,"* each described separately. Our own `northern_tier` cell already recommends American only. |
| **Meyer lemon** | **SPLIT** (first batch; PLA-137) | Mauk & Shea file Improved Meyer under lemons but call it *"probably a lemon-sweet orange hybrid ... fairly cold resistant, similar to sweet orange."* UC IPM ranks Meyer among the hardy citrus and Eureka among the most cold-sensitive. UC MG Sacramento recommends Meyer where it does not recommend true lemon. |
| **Key lime** | **VARIETY of `lime`**, with a hardiness override. No split. | Mauk & Shea keep one "C. Limes" group: 1. Bearss, 2. Mexican (Key). UC MG Santa Clara: Bearss is *"hardier than Mexican/West Indian (Key) lime."* The difference is hardiness, which a variety override expresses. |
| **Orange** | **WIDEN `orange-navel` to one `orange` crop** (slug `orange`, with a redirect). Navel, Valencia and blood oranges become varieties. **This replaces the earlier sweet-orange parent.** | Mauk & Shea: *"D. Oranges: 1. Navel (Washington, Cara Cara, Lane Late), 2. Valencia, 3. Blood oranges (Moro, Tarocco)."* UC MG Santa Clara: *"Harvest dates depend on the variety ... winter for Navel orange, and summer for Valencia."* PLA-533's open finding stays attached; the rename does not close it. |
| **Daikon** | **OWN CROP** (`daikon`) | UC MG Sacramento's planting schedule gives "Radish" and "Radish, daikon" separate rows. UC MG Santa Clara has its own Daikon page. UC MG Sonoma: daikon is planted in late summer or early fall for harvest in late fall and winter. |
| **Pluot, plumcot, pluerry, aprium, nectaplum, peacotum** | **VARIETIES of the dominant parent**: plum (pluot, plumcot, pluerry), apricot (aprium), nectarine (nectaplum), peach (peacotum) | UC MG Santa Clara: *"stone fruit hybrids ... Pluot and aprium: hybrids of a plum and an apricot, named for which fruit dominates."* Its pruning advice groups "plum, pluot" together. |
| **Tiers** | **Removed.** Every crop and variety gets full (former Tier 1) treatment. | Trevor. The master list is re-issued as `~/Documents/plant-project/08-reference/master_crop_list_v2_2026-09-30.pdf`: 231 parents planned, 1,431 varieties listed (755 already in the dataset), against a ~1,200-variety launch target. |

## 0. Method, and what each column means

- **Roster** is computed from `crops_data_final.json`, not asserted.
- **T1 availability** is measured against the on-disk doc cache (`tools/.doc_cache`, 1,216 bodies;
  1,194 map back to a URL the canonical cites). A hit means the cached T1 page *names* the crop; the
  count is word-boundary matches. **"Already cited on X"** means the dataset already cites that exact
  page on sibling crop X, so the page is in hand and its admission is settled. **A mention is not
  support** (`right-document-wrong-claim`): a page naming kumquat in a variety table does not anchor a
  kumquat entry. So the column grades three levels:
  - **DEDICATED, CITED**: a page about this crop, already cited on a sibling. Cheapest.
  - **PARTIAL**: named in passing on cached T1 pages; a dedicated page still has to be found and read.
  - **NONE CACHED**: nothing in the cache. This does not prove no T1 page exists anywhere. It means
    no path has been measured, so the row sits in NO SOURCE PATH until a hunt finds one
    (`hunt-before-downgrading`).
- **Consumer references** come from a read-only scan of `~/plant-app` and `~/plant-astro` (section 3).
- **Master list** = `~/Documents/plant-project/08-reference/master_crop_list.pdf` (partner review
  draft, 2026-04-21/22, 45 pp). It proposes ~72 new crops. Its **crop-vs-variety rule (p3, #7)**:
  *"different species OR different garden cycle OR different use pattern that changes harvest rules =
  new crop, else variety."* This review uses that rule to admit NEW crops.
- **Test-user requests** (Trevor, 2026-09-30): aprium, pluot, blood orange, Buddha's hand, olive,
  plumcot, peacotum, nectaplum, pluerry, Cleveland sage, lemon balm, mullein, pineapple sage,
  bachelor button. Trevor added: lettuce, companion flowers, edible flowers, rainbow chard, oats and
  barley, hops, olive, avocado. Every one is resolved below.

### Cost, in sessions, against the full cert register

The register a new crop certifies against today is `whole_crop_gate` A2-A63 (62 gates) run by
`gate_all`, plus the IPM ladder (A56/A57: every problem entry needs an `id`, `type` and
`control_ladder`; the roster averages 913/121 = ~7.5 problem entries per crop), the container model,
the perennial year trio (A55), dimensions (A59), `plants_per_pot` (A60), `critical_warnings` (A61),
the sourced-block gates (A62/A63), and whatever PLA-10 (spacing/layout) and PLA-11 (yield) add
before this window opens. The last new-crop arc (the dry-corn family, three siblings of certified
sweet-corn on an existing archetype) took one arc over 2026-07-15/16. The register then stopped at
about A42, so that pace is a floor, not an estimate. These are **estimates**, not measurements:

| tier | shape | est. sessions |
|---|---|---|
| **S** | sibling of a certified crop, existing archetype, T1 page already cited on the sibling | ~1 each; 2-3 per session once a batch pattern exists |
| **M** | existing archetype, but a T1 hunt is owed, or a perennial (year trio, rootstock, chill) | ~2 |
| **L** | needs a NEW archetype + gate suite + a pilot member (vine fruit, nut harvest, fungus) | 4-6 for the pilot, then ~2 per sibling |
| **SPLIT** | an existing certified crop becomes two parents | ~2, plus re-sourcing every region cell of the old parent that names the moving member; problem ids are REUSED (join-key rule) |

The master list's 6-12 hours per new crop predates the IPM ladder, container model and dimensions
gates. Do not reuse it.

## 1. The roster today (computed)

**128 crops: 121 certified, 114 launch-ready, 7 shells.** Lifecycle: annual 85, permanent 25,
perennial 14, biennial 4. Archetypes: `warm_season_fruiting` 31, `cool_season_annual` 27,
`deciduous_fruit_tree` 14, `companion_and_ornamental_flower` 13, `microgreen` 8, `culinary_herb` 7,
`evergreen_fruit_tree` 7, `woody_ornamental` 5, `mushrooms` 5, `berries_woody` 4,
`warm_season_grass` 4, `herbaceous_perennial` 2, `berries_herbaceous` 1.

| category | n | crops |
|---|---|---|
| Alliums | 5 | spring-onion, onion, leek, shallot, garlic |
| Beans & Peas | 7 | green-beans-bush, pole-beans, sugar-snap-peas, snow-peas, broad-beans-fava, edamame, dry-bean |
| Berries & Shrubs | 4 | blueberry, raspberry, blackberry, elderberry |
| Brassicas | 5 | broccoli, cauliflower, cabbage, kohlrabi, brussels-sprouts |
| Citrus | 5 | lemon, lime, orange-navel\*, mandarin-clementine\*, grapefruit\* |
| Companion & Pollinator | 10 | marigold, borage, calendula, zinnia, cosmos, chamomile, sweet-alyssum, sweet-pea, echinacea, bee-balm |
| Corn | 4 | sweet-corn, field-corn, popcorn, flint-corn |
| Cucumbers | 4 | slicing-cucumber, pickling-cucumber, english-cucumber, cucumber |
| Edible & Harvest | 4 | nasturtium, sunflower, viola, lavender |
| Fig & Subtropical | 4 | fig, pomegranate, persimmon, **avocado (shell)** |
| Fruit | 1 | strawberry |
| Fruiting Veg | 3 | eggplant, tomatillo, okra |
| Herbs | 11 | basil, cilantro-coriander, dill, parsley, chives, mint, thyme, rosemary, oregano, sage, lemongrass |
| Leafy Greens | 8 | kale, spinach, lettuce-leaf, swiss-chard, arugula, bok-choy, celery, collards |
| Melons | 3 | watermelon, cantaloupe, honeydew-melon |
| Microgreens | 8 | microgreens-mix, sunflower-sprouts, pea-shoots, radish-, broccoli-, arugula-, cilantro-microgreens, wheatgrass |
| Mushrooms | 5 | **oyster, shiitake, lions-mane, wine-cap, button (all shells)** |
| Native & Specialty | 3 | mulberry, pawpaw, **olive (shell)** |
| Peppers | 5 | bell-pepper, jalapeno, banana-pepper, cayenne-pepper, habanero |
| Perennial Vegetables | 2 | artichoke, asparagus |
| Pome Fruit | 3 | apple\*, pear-european\*, pear-asian\* |
| Root Vegetables | 7 | carrot, radish, potato, sweet-potato, parsnip, turnip, beet |
| Squash | 6 | zucchini-courgette, yellow-summer-squash, butternut-, acorn-, spaghetti-squash, pumpkin |
| Stone Fruit | 6 | peach, plum\*, apricot, cherry-sweet, nectarine, cherry-sour |
| Tomatoes | 5 | cherry-, beefsteak-, roma-, heirloom-, grape-tomato |

\* certified but not launch-ready (open blocking finding: PLA-579 for plum/apple/pears, PLA-533 for
the three citrus).

**The 7 shells:** oyster-mushroom, shiitake-mushroom, lions-mane-mushroom, wine-cap-mushroom,
button-mushroom, avocado, olive. `verification_status.status = null`, no pests, diseases or
varieties.

**Whole categories with zero coverage:** vine fruit (grape, kiwi, hops, passion fruit), nut trees,
Ribes and other small fruits beyond the four cane/bush berries, chicories, Asian heading greens,
southern field peas, small grains and pseudo-grains, perennial "pie plant" vegetables beyond
artichoke/asparagus, and tropical fruit.

## 2. The named examples, resolved

| name | resolution | evidence |
|---|---|---|
| **mandarin** | **ALREADY IN ROSTER.** Not a gap. | `mandarin-clementine` covers mandarins broadly (varieties: Owari Satsuma, Clementine, Gold Nugget, Pixie, W. Murcott/Tango; cites UF CH116, the satsuma page). The ticket's "citrus beyond the current five (mandarin, ...)" reads it as missing; it is not. |
| **cara cara** | **VARIETY NOT PARENT, and already authored.** | Already in `orange-navel.varieties.recommended` (Washington, Cara Cara, Lane Late, Fukumoto). A pink navel is a navel. Nothing owed here; PLA-12 deepens it. |
| **Meyer lemon** | **SPLIT (PLA-137). Recommend FIRST BATCH.** | See section 6. PLA-137's 2026-08-06 upgrade stands: Sacramento recommends Meyer and not true lemon; Arizona bars Meyer and grows Eureka/Lisbon. Canonical `lemon.regions.low_desert_az` already says *"Meyer lemons are not sold in Arizona, so grow Eureka or Lisbon"*, and 8 of 16 lemon region cells name Meyer. One `regions{}` cannot be right for both. Parentage is triple-sourced (AZ1001, Mauk & Shea, Lazaneo). The seed value is Improved Meyer's existing `hardiness.delta`. **Ponderosa** (lemon x citron) does not follow either parent by default; that is its own ruling. |
| **wheatgrass** | **ALREADY IN ROSTER** as a microgreen. | `wheatgrass` (`microgreen` archetype; varieties hard red winter, hard red spring, soft white winter wheat). |
| **barley** (and "wheatgrass" as Trevor meant it) | **RULED 2026-09-30 (Trevor): he meant the field grains (wheat, barley, oats), with a future beer-making section in mind.** That makes them a WANTED lane (section 4.5), not a dismissal. The measurement below still stands: no T1 path is cached yet. | *Barley grass* is grown like wheatgrass, but it is a different species (*Hordeum*), so rule 7 makes it a new crop, a microgreen sibling of `wheatgrass`. The cache names barley only in cover-crop context: NO SOURCE PATH. *Barley grain*: also cover-crop mentions only, and a backyard small-grain has weak beginner fit: NO SOURCE PATH, grains lane (section 4.5). |
| **rainbow chard** | **VARIETY NOT PARENT, already authored.** | `swiss-chard` already carries Bright Lights ("an All-America Selections rainbow mix") and Ruby Red. |
| **blood orange** | **VARIETY, and its parent does not exist. RULED 2026-09-30 (Trevor): wanted, parent and all. FIRST BATCH** (C4). | A blood orange (Moro, Tarocco) is a sweet orange, NOT a navel. So it does not belong under `orange-navel` as named, and the master list's "blood orange as a variety within its parent" (p38) has no parent to land in. The same gap holds Valencia and Hamlin. UA's "Oranges for southern Arizona" (already cited on `orange-navel`) names blood 19x, Moro 12x, Valencia 38x, Hamlin 10x. See section 4.1 row C4. **Superseded by section 0a: widen `orange-navel` to `orange`.** |

## 3. What the consumers reference that the dataset does not carry

A read-only scan of `~/plant-app` (planner, lessons, Herb prompts) and `~/plant-astro` (guide
pages, redirects, recipes) used the full candidate vocabulary plus every file holding 8+ roster slugs.

**Result: neither consumer references a crop outside the 128 as plantable.** No planner picker,
Herb prompt, guide route or redirect names a missing crop:
- Herb's prompt (`plant-app/src/lib/herb/prompt.ts`, `supabase/functions/herb-ask/index.ts`) names
  no crop, and Herb's crop identity is built from the guides data.
- plant-app's `CERTIFIED` list (`scripts/build-guides-data.mjs:38`, 121 slugs), `guide-art.ts` and
  `variety-index.json` hold no extra crop.
- plant-astro's crop routes come from the dataset collection, and `dist/guides/crops/` is exactly
  the 128.

**Sitemap and search data: NONE ON DISK.** plant-astro configures `@astrojs/sitemap`
(`astro.config.mjs:13`), but `dist/` holds no sitemap or any .xml, and there is no search index
(`public/data` holds only `zip-zones.json`). plant-app has no sitemap. So **the ticket's "search
demand on the site's guide pages" could not be measured from disk.** Demand evidence in this review
comes from the test-user list, the master list and the near-misses below. Real search demand needs
analytics (Search Console), which is out of this repo.

**Near-misses:** each shows intent to cover a crop, but none makes one plantable.

| name | where | what |
|---|---|---|
| gooseberry, honeyberry, currant | `plant-app/src/components/guides/BerryChillCard.tsx:33-34` | code comment about berries "likely to add" |
| rhubarb | `plant-app/src/app/(tabs)/learn/[slug].tsx:910` (comment: "rhubarb-style herbaceous perennials"); `plant-astro/src/lib/home/circles-demo.ts:37,52` (sample data) | anticipated, not a guide |
| southern peas | `plant-astro/src/pages/guides/frost.astro:64` | frost-guide prose ("okra, sweet potato, southern peas") |
| chervil, buckwheat, winter rye, daikon | `plant-app/src/data/education.json`, `plant-astro/src/data/sunlight.json:21` | lesson examples (cover crops; a shade herb) |
| key lime, finger lime, satsuma, cara cara | `plant-app/src/data/variety-index.json` | variety names under roster crops. This confirms the app already surfaces Key lime and finger lime as `lime` varieties (C5). |

**One consumer defect surfaced (not this repo's to fix):** two plant-astro recipes
(`src/data/recipes/plant.json:1622`, `:2558`) tag `hero_crops: beetroot`, but the roster slug is
`beet`. The per-crop recipe filter (`src/lib/recipes.ts:51`) therefore never matches those recipes to
the beet guide. This belongs to the plant-astro session.

## 4. Candidate list, by cluster

Columns: **P/V** = parent or variety-of-existing. **Gap** = why. **T1** = source path (section 0).
**Cost** = tier (section 0). **Fit** = zone and audience against USDA 3-11, backyard, beginner-first.
Zone ranges in this table are orientation only, NOT sourced claims. Each one gets sourced at authoring.

### 4.1 Citrus

| # | candidate | P/V | gap | T1 | cost | fit | proposed |
|---|---|---|---|---|---|---|---|
| C1 | **meyer-lemon** | SPLIT from `lemon` | PLA-137: inverted region suitability; test-user and master-list demand | DEDICATED, CITED: AZ1001, UCCE Riverside (Mauk & Shea), UCCE San Diego, UC MG Sacramento GN 127, UCCE Placer 31-018C (PLA-137) | SPLIT | the hardiest lemon; container-grown across the north | **FIRST BATCH** |
| C2 | kumquat | P (*Citrus japonica*; eaten whole) | citrus beyond the five; master list | PARTIAL: 12 cached pages name it (UC MG Santa Clara 5x, UC 178097 4x, TAMU citrus 3x, LSU 3x); no dedicated page cached | M | containers everywhere; ground z9-11 | LATER |
| C3 | calamondin | P (*C. x microcarpa*) | master list; containerizable | PARTIAL: UF HS132 3x, TAMU citrus 3x | M | indoor/container | LATER |
| C4 | **sweet orange (non-navel)**: Valencia, blood (Moro, Tarocco), Hamlin | P, OR widen `orange-navel` to `orange` | blood orange (test user) has no parent; Valencia is the most-grown orange and is missing | DEDICATED, CITED: UA "Oranges for southern Arizona" (cited on `orange-navel`); UF HS132 | S-M | same as navel | **FIRST BATCH (ruled 2026-09-30).** Build it as a **new parent**, not a rename of `orange-navel`: a rename changes the slug and URL of a certified crop that carries an open PLA-533 blocking finding. Guard: author the new parent from its own T1 reads. Do NOT copy navel text across (`template-inheritance-fabricates-attributions`); a copy would carry the navel's contested claim into a clean crop. Varieties at PLA-12: Moro, Tarocco, Sanguinelli, Valencia, Hamlin. **SUPERSEDED by section 0a (follow UC): no new parent; widen `orange-navel` to one `orange` crop instead.** |
| C5 | Key lime | SPLIT candidate from `lime` | `lime` holds Persian, Key, Makrut (grown for its LEAVES, a use-pattern difference under rule 7) and Australian finger lime (*Microcitrus*): four taxa | DEDICATED, CITED: UF CH092 (Key lime, 71x; cited on `lime`) | SPLIT | Key lime is the most cold-sensitive | **RULED 0a: VARIETY of `lime`**, no split |
| C6 | citron / Buddha's hand | P (*C. medica*) | test user | NONE CACHED (1 passing mention, UC MG Santa Clara) | M | niche, z9-11 | NO SOURCE PATH (master list tier 4) |

### 4.2 Nut trees (no coverage today; not in the master list at all)

| # | candidate | P/V | gap | T1 | cost | fit | proposed |
|---|---|---|---|---|---|---|---|
| N1 | pecan | P | category gap; the signature southern yard tree | PARTIAL, strong: NCSU Extension Gardener Handbook ch.15 (43x), NC smaller-orchard guide (48x), NMSU H310 (16x). All three already cited on tree fruits. | M-L (nut harvest shape, type I/II flowering, very large tree) | Southeast/South-Central; a poor fit for a small lot | LATER |
| N2 | chestnut | P | category gap | PARTIAL: NCSU EGH ch.15 (15x) | M-L | broad, z4-8 | LATER |
| N3 | almond, pistachio | P each | category gap | PARTIAL: UC 131938, NMSU H310 | M-L | West and arid only | LATER |
| N4 | walnut, hazelnut | P each | category gap | walnut PARTIAL (the hits are mostly juglone/allelopathy); hazelnut NONE usable (its 20 hits are PNW Handbook navigation text) | L | -- | NO SOURCE PATH (hazelnut); LATER (walnut) |

**Open design question for the nut cluster:** does a nut crop fit `deciduous_fruit_tree`, or does its
harvest (drop, hull, cure, store) want its own shape? The first nut crop should be a pilot.

### 4.3 Pome and stone fruit gaps

| # | candidate | P/V | gap | T1 | cost | fit | proposed |
|---|---|---|---|---|---|---|---|
| F1 | **interspecific Prunus**: pluot, plumcot, aprium, nectaplum, peacotum, pluerry | **VARIETY NOT PARENT** (provisional) | 6 of 14 test-user requests | PARTIAL: NMSU H310 (pluot, aprium, plumcot), UC 131938, UC MG Santa Clara fruit tips (all but pluerry); pluerry NONE | -- | as the dominant parent | **RULED 0a: VARIETY NOT PARENT**, under the dominant parent (UC). Reasoning below. |
| F2 | quince | P (*Cydonia*) | master list | PARTIAL, strong: WSU W. Washington fruit handbook (13x; the handbook is cited on 12 crops), WSU "Unusual fruits" 2022, AZ1269 | M | broad, z5-9 | LATER |
| F3 | jujube | P | arid Southwest gap | PARTIAL: NMSU H310 (9x), UAEX fruit trees (8x; both cited) | M | Southwest/South, heat-loving | LATER |
| F4 | loquat | P | subtropical | PARTIAL: UC MG San Diego 4x | M | z8-10 | LATER |

**F1 reasoning.** These are Zaiger-type interspecific hybrids. They are grown as the dominant parent
is grown: chill class, bloom timing, pollinizer needs. A pluot wants a Japanese plum or another pluot
nearby. Under the split criterion (section 6), they do not need a regions map of their own, so they
are varieties: pluot, plumcot and pluerry under `plum`; aprium under `apricot`; nectaplum under
`nectarine`; peacotum under `peach`. The test-user demand is real, and it is served by a findable
**variety** page, not a parent. Caveat: `plum` carries an open PLA-579 blocking finding, and **no
cached T1 page classes these hybrids at all**. PLA-12 must read how extension groups them before
authoring. If a T1 source treats pluots as their own group with distinct chill or pollination, this
flips to a parent.

### 4.4 Small fruits and vines

| # | candidate | P/V | gap | T1 | cost | fit | proposed |
|---|---|---|---|---|---|---|---|
| V1 | **grape** (bunch: American + European, table + wine) | P | **the largest single gap**: vine fruit has zero coverage | DEDICATED, CITED: VCE 426-840 (grapes 66x; in the catalog as `vce_426_840`, cited on the four cane/bush berries); WSU W. WA handbook 21x; UC 178097 20x; NMSU 15x | **L** (new woody-vine archetype: trellis, cane vs spur pruning, and a pilot) | broad, z4-10 by type | **LATER, as the next NEW-ARCHETYPE arc** (section 5) |
| V2 | muscadine | P (*V. rotundifolia*) | the Southeast's grape; bunch grapes struggle there | PARTIAL, strong: VCE 426-840 (11x) | M after V1 | Southeast z7-10 | LATER, after V1 |
| V3 | currant, gooseberry | P (one or two; rule 7 says two species) | Ribes gap; master list | PARTIAL, strong: WSU W. WA handbook (13x / 7x), AZ1585 (9x / 10x), USU backyard fruit (9x / 6x) | M (`berries_woody` exists) | north and cool, z3-7; some states restrict Ribes (white pine blister rust), which a regions map can express | LATER |
| V4 | hardy kiwi | P | vine fruit | PARTIAL: WSU handbook (24x kiwi, 7x hardy), AZ1585, WSU Unusual | M after V1 (shares the vine archetype) | z4-8 | LATER |
| V5 | honeyberry/haskap, aronia, serviceberry | P each | cold-hardy natives | PARTIAL: USU, WSU Unusual, WSU handbook | M | far north, z3-6 | LATER |
| V6 | hops | P | Trevor's list; the other half of a beer-making section (with G3) | NONE CACHED (passing only: the UMN edible-flowers page, a San Diego MG index); **T1 hunt owed** | L (perennial bine; would share the vine archetype V1 pilots) | z4-8 | **WANTED LANE: T1 HUNT OWED** |

### 4.5 Grains and grasses

| # | candidate | P/V | gap | T1 | cost | fit | proposed |
|---|---|---|---|---|---|---|---|
| G1 | sorghum, millet | P | already QUEUED in `docs/crop_expansion_roadmap.md` (2026-07-15) | PARTIAL: CTAHR corn2003, MSU P3616 (in passing); no grain guide cached | S-M (`warm_season_grass`, corn pattern) | broad; weak beginner fit | LATER |
| G2 | amaranth, quinoa, buckwheat | P | roadmap-queued pseudo-grains | amaranth PARTIAL (NCSU organic guide 19x); quinoa NONE (1 microgreens mention); buckwheat cover-crop mentions only | M (broadleaf: archetype fit unconfirmed) | weak beginner fit | LATER (amaranth); NO SOURCE PATH (quinoa, buckwheat) |
| G3 | **wheat, barley, oats** (grain) | P each | **WANTED (Trevor, 2026-09-30):** the field grains, and the base of a future beer-making section (barley is the malting grain; wheat is used in brewing too) | NONE CACHED as grain: every hit is cover-crop or chill-hour context. **A T1 hunt is owed** (small-grain extension guides; none read this session) | **L**: these are COOL-season grasses (fall or spring sown). The existing `warm_season_grass` archetype is frost-anchored summer corn, so they most likely need a `cool_season_grass` archetype and a pilot | backyard small-grain is niche; the brewing angle is the audience | **WANTED LANE: T1 HUNT OWED** |
| G3b | rye | P | cover-crop/grain | NONE CACHED as grain | L (with G3) | niche | NO SOURCE PATH (rides with G3 if the lane opens) |
| G4 | barley grass | P (microgreen sibling of `wheatgrass`) | Trevor's list | NONE CACHED | S once sourced | indoor | NO SOURCE PATH |

**The beer-making section (Trevor, 2026-09-30, direction only, not scoped).** Wheat, barley, oats
and hops are wanted as the crop base for a future brewing section. Two things follow:
- **The crops come before the section.** The section needs certified parents to point at. Its own
  content (malting, hop drying, brewing) is a product and content question, and probably a new
  consumer surface. It deserves its own ticket.
- **The lane has two archetype costs:** a cool-season-grass archetype for the grains, and the vine
  archetype for hops, shared with grape (V1). Pilot grape first and hops rides on it.

**A second product question (not ruled here):** oats, barley, rye and buckwheat appear
throughout the cache as **cover crops** (177 cached pages name cover crops). If "oats and barley"
from test users means cover crops, that is a different product: a cover-crop *role* with its own
fields, not a food-crop parent. Worth a separate ticket if Trevor wants it.

### 4.6 Herbs

| # | candidate | P/V | gap | T1 | cost | fit | proposed |
|---|---|---|---|---|---|---|---|
| H1 | **lemon balm** | P (*Melissa*) | test user; master list | PARTIAL, strong: Clemson HGIC herbs factsheet (catalog `clemson_hgic`, T1), TAMU fall garden guide, Illinois Extension herbs | S (`culinary_herb`) | broad, z4-9; spreads like mint | **FIRST BATCH** |
| H2 | pineapple sage | P (*Salvia elegans*, not `sage`'s *S. officinalis*) | test user; edible flower and hummingbird plant | PARTIAL: Clemson herbs (4x), UMN edible flowers | S | perennial z8-11, annual elsewhere | LATER (strong batch-2) |
| H3 | fennel | P (one crop, bulb and herb forms as varieties, per the master list) | 46 cached pages | PARTIAL, strong: Clemson herbs, WSU EM051E, NMSU H221 | S | broad | LATER (strong batch-2) |
| H4 | tarragon, marjoram | P each | master list | PARTIAL: Clemson herbs; USU drought (tarragon 18x); TAMU fall guide (marjoram 10x) | S | broad | LATER |
| H5 | sorrel, chervil, stevia, shiso | P each | master list (sorrel is master-list tier 4) | sorrel PARTIAL (UMN herbs); others not measured | S | broad | LATER / unmeasured |
| H6 | Cleveland sage | P (*S. clevelandii*) | test user | NONE CACHED | -- | California native ornamental | NO SOURCE PATH |
| H7 | mullein | P (*Verbascum*) | test user | NONE CACHED (1 unrelated mention). Weedy or invasive in many states, and medicinal framing would need T1 health sourcing (`health-claims-ok-if-t1-sourced`) | -- | -- | NO SOURCE PATH |

### 4.7 Companion and edible flowers

Current coverage is 14 (Companion & Pollinator 10, Edible & Harvest 4). The anchor page for an
edible-flower cluster is already cached: **UMN "Edible flowers"** (catalog `umn_ext_edible_flowers`,
T1), which names bachelor button, pineapple sage, anise hyssop, daylily and hops.

| # | candidate | P/V | T1 | cost | proposed |
|---|---|---|---|---|---|
| E1 | **bachelor button** (*Centaurea cyanus*) | P | PARTIAL: UMN edible flowers (in catalog), UF Pasco blog | S (`companion_and_ornamental_flower`) | LATER (strong batch-2; test user) |
| E2 | snapdragon, dianthus | P each | PARTIAL: UF EP450, UC MG Inyo annuals, UNR | S | LATER |
| E3 | yarrow | P | PARTIAL: UA AZ2061, UNR | S-M (perennial) | LATER |
| E4 | anise hyssop, daylily | P each | PARTIAL: UMN edible flowers; daylily UF EP451 | S-M | LATER |

### 4.8 Vegetables

| # | candidate | P/V | gap | T1 | cost | fit | proposed |
|---|---|---|---|---|---|---|---|
| G-1 | **rutabaga** | P (*B. napus*, not turnip's *B. rapa*) | master list; winter storage root | **DEDICATED, CITED**: UMN "Growing turnips and rutabagas" (31x), USU "Rutabagas and turnips" (28x), Clemson "Turnips & rutabagas" (13x). All three are already cited on `turnip`. | **S** | north, z3-7; fall crop | **FIRST BATCH** |
| G-2 | **napa / Chinese cabbage** | P (heading *B. rapa*) | master list; Asian greens | **DEDICATED, CITED**: UMN "Growing Chinese cabbage and bok choy" (25x; cited on `bok-choy`), Clemson "Cabbage & Chinese cabbage" (cited on `bok-choy`, `cabbage`), CTAHR B-91 | **S** | broad, cool-season | **FIRST BATCH** |
| G-3 | **southern pea / cowpea** (black-eyed, crowder, cream) | P (*Vigna unguiculata*) | master list; the South's staple legume is missing | **DEDICATED, CITED**: Clemson "Bean & southern pea diseases" (11x) and "... insect pests" (9x), both cited on the beans; MSU P3616 (17x); NMSU CR457 | **S** | South and Southeast, z6-11; heat-proof | **FIRST BATCH** |
| G-4 | **ground cherry** (incl. Cape gooseberry / husk cherry) | P (*Physalis pruinosa* / *peruviana*) | master list's only DEFERRED crop, pre-scoped at 16-20 h. **Live defect:** `tomatillo.varieties.recommended` still carries "Pineapple (*Physalis pruinosa*-type ... ground-cherry relative)", which the master list says violates rule 7 | **DEDICATED, CITED**: UMN "Growing tomatillos and ground cherries" (25x; cited on `tomatillo`) | **S** | broad, warm-season annual | **FIRST BATCH** (this also closes the tomatillo variety misfile) |
| G-5 | **rhubarb** | P | master list: "Surprised it's missing." A northern backyard staple; toxic leaves make `critical_warnings` and `pet_safe` load-bearing | PARTIAL: USU planting dates (18x; catalog `usu_washco_dates`, cited on artichoke/asparagus), NMSU CR457 (7x), CTAHR B-91. **No dedicated page cached**; a hunt is owed. | **M** (third `herbaceous_perennial` member; the archetype exists) | north, z3-7 | **FIRST BATCH** (the batch's perennial) |
| G-6 | lima bean | P (*P. lunatus*) | master list | PARTIAL, strong: UMN "Growing beans" (8x), CTAHR B-91 (24x), MSU P3616 | S | South, heat | LATER (strong batch-2) |
| G-7 | endive / escarole, radicchio | P (two species: *C. endivia*, *C. intybus*) | master list; chicories have zero coverage | **DEDICATED, CITED**: UMN "Growing lettuce, endive and radicchio" (cited on `lettuce-leaf`); UF VH021; CTAHR res-164 | S | cool-season | LATER (strong batch-2) |
| G-8 | mustard greens | P | master list; southern greens | PARTIAL, strong: MSU P3616 (cited on collards/kale), LSU, Clemson | S | broad | LATER |
| G-9 | daikon | P or V of `radish` | master list leans "crop" (fall-only cycle) | PARTIAL, strong: CTAHR B-91 (32x), UMN "Growing radishes" | S | fall | **RULED 0a: OWN CROP** (UC planting calendars list it separately) |
| G-10 | celeriac, sunchoke, horseradish | P each | master list | PARTIAL: WSU EM051E/EM057E, MSU P3616 | S-M | broad | LATER |
| G-11 | peanut | P | southern gap | PARTIAL: MSU P3616 (8x), MSU planting dates | M | South, long warm season | LATER |
| G-12 | **lettuce** (Trevor's list) | NOT a new parent | `lettuce-leaf` already carries Romaine/Cos and Buttercrunch (butterhead); only crisphead is absent | cited: UMN lettuce page | -- | -- | **VARIETY NOT PARENT.** Heading types differ by days to maturity and heat, which is a variety delta, not a split (section 6). The narrow slug is a naming issue, not a data one. A rename of `lettuce-leaf` to `lettuce` is a URL change on a certified crop; flag it for PLA-625, not here. |
| G-14 | **broccolini** (Aspabroc; broccoli x gai lan, both *B. oleracea*) | **P (recommended), against the variety default** | Trevor's list; master list ("confirmed ... distinct") | PARTIAL, thin: UA AZ1615 (1x); NCSU "Basics of broccoli production" covers sprouting types (8x); gai lan NONE. A hunt is owed. | S (broccoli sibling) | broad, cool-season | **LATER (strong batch-2)**. Reasoning below. |
| G-13 | chayote, luffa, Malabar spinach, NZ spinach, runner bean, baby corn, pattypan, kabocha/hubbard, delicata, Armenian cucumber, cocktail tomato, pepper classes (serrano, poblano, shishito, superhot) | master list's remaining ~30 "hot family" proposals | variety-depth demand | PARTIAL to unmeasured | S each | -- | LATER. Most are PLA-12 variety-expansion calls under rule 7, and the master list already scoped them family by family. |

**G-14 reasoning (broccolini).** The two tests disagree. Section 6's split test says variety:
same species, same calendar, same regions. The master list's rule 7 says parent, because the
*harvest rules* change. Canonical `broccoli.harvest_ready_beginner` reads *"Cut the main head while
it is firm ... More small shoots grow afterward."* Broccolini makes no main head; it is a
cut-and-come-again stem harvest from the start. So the crop-level harvest instruction would be
**wrong** for it, and a variety `delta` overrides values, not the harvest instruction. That makes it
a parent. Sprouting broccoli (purple/white) stays a broccoli variety, per the master list.

### 4.9 Tropical fruit: a WANTED lane (Trevor, 2026-09-30)

Trevor wants tropical crops and pineapple. The in-ground zone fit is z10-11, but the dataset already
has the regions to serve it (`hawaii_tropical`, `fl_peninsula`, `rgv`, `ca_south_coast`), and
several of these are container or indoor plants everywhere else, the way Meyer lemon is. **The
anchor pair is UH CTAHR (Hawaii) + UF/IFAS**; both are in the catalog as T1. What is cached today is
CTAHR's *tropical-topics* index and UF EP452 (the South Florida calendar), which name the crops in
passing. UF/IFAS publishes home-landscape fact sheets for most of these crops, but **none was read
this session**, so every row is PARTIAL or NONE until the hunt runs.

The lane splits by plant shape, because shape decides the archetype cost:

| # | candidate | P/V | shape and archetype | T1 (cached) | cost | fit | proposed |
|---|---|---|---|---|---|---|---|
| T1 | **pineapple** | P (*Ananas comosus*) | a terrestrial bromeliad; one fruit per plant after ~18-24 months (orientation, unsourced); grown from a store-bought top. **No archetype fits.** | NONE for the fruit: the 48 cached hits are pineapple mint, pineapple sage, the "Pineapple" tomatillo and pineapple guava. Hunt owed (UF/IFAS, CTAHR). | L (new herbaceous-tropical shape; pilot) | **the widest audience of the tropicals**: a windowsill or patio pot in any zone, a classic kids' and beginner project | **WANTED LANE: T1 HUNT OWED**. Recommend as the tropical-herbaceous PILOT. |
| T2 | banana | P | giant herb; pseudostem fruits once, then suckers | PARTIAL: CTAHR tropical-topics (12x), UF CV130 | L (shares T1's archetype if it generalizes) | fruit z9b-11 (orientation); ornamental hardy bananas far north do not fruit, and the regions map must say so | WANTED LANE |
| T3 | papaya | P | fast, short-lived herbaceous tree; fruits in year 1 | PARTIAL: CTAHR (15x) | M-L | z10-11, Hawaii/FL/RGV | WANTED LANE |
| T4 | mango | P | evergreen tree | PARTIAL: CTAHR (7x), UF EP452 (5x) | M (`evergreen_fruit_tree`; avocado pilots it) | z10-11, FL/HI | WANTED LANE |
| T5 | guava, lychee, longan, jackfruit | P each | evergreen trees | PARTIAL: CTAHR tropical-topics | M each after mango | z10-11 | WANTED LANE (later in it) |
| T6 | passion fruit (+ maypop, *P. incarnata*, z6+) | P (two species, master list leans two crops) | vine | PARTIAL: CTAHR, UC MG San Diego; maypop NONE | M after the grape vine pilot | maypop opens it to z6+ | WANTED LANE (after V1) |
| T7 | dragon fruit (pitaya), starfruit (carambola) | P each | climbing cactus / tree | NONE CACHED | -- | z10-11 | NO SOURCE PATH until hunted |
| T8 | coffee, cacao, vanilla, sugarcane, taro, cassava, moringa | P each | mixed | PARTIAL (CTAHR mentions) | -- | Hawaii-only for most | LATER; not proposed |

**Sequencing inside the lane:** avocado (a shell, and the subtropical-tree pilot) goes first, then
mango on that archetype. Pineapple pilots the herbaceous-tropical shape, and banana and papaya test
whether that archetype generalizes. Passion fruit waits for the grape vine pilot.

## 5. The 7 shells: which are closer to certifiable than a new crop

All 7 are equally thin: **28 filled keys each, against an average of 69.7 on certified crops**, and
zero pests, diseases or varieties. What differs is the archetype they would certify against.

| shell | archetype | verdict |
|---|---|---|
| **avocado** | `evergreen_fruit_tree` (exists; 5 certified citrus use it) | **Closer than any tier-L new crop, about equal to a tier-M new tree.** No archetype design is owed. `calendar_basis` and a 10-cell regions scaffold exist. It is already cited in UF EP452. Test-user demand is high (Trevor's list). Cost ~2-3 sessions. |
| **olive** | `evergreen_fruit_tree` | Same as avocado, plus one wrinkle: the fruit is inedible until cured. That makes `harvest` / `storage` / `critical_warnings` semantics new. It is a test-user request too. Cost ~3 sessions. |
| 5 mushrooms | `mushrooms` (`calendar_basis: non_seasonal_indoor`) | **Further than ANY new plant crop on this list.** The archetype was never designed. Soil, sun, pH, container, spacing, rotation and the IPM ladder mostly do not apply, so every A-gate needs an N/A ruling, and the substrate/spawn/fruiting model has to be designed and gated from scratch (backlog KICKOFF §E, Tier 2D). The master list excludes them from Phase 4. Cost 6+ sessions before the first one certifies. |

**Recommendation:** finish **avocado + olive as a pair right after the first batch.** They share
one archetype and one sourcing lane (UC ANR, UF/IFAS), both are test-user requests, and finishing
them takes the shell count from 7 to 5. Leave the mushrooms as a design decision (build the fungus
archetype, or retire the five), per `crop_expansion_roadmap.md`.

## 6. Should any current crop be split? The criterion, then the measurements

**Criterion (proposed for ruling).** Split an existing crop into two parents when its members
differ on a **parent-level field that the sparse variety-override contract cannot express**:

1. **Region suitability diverges.** The `regions{}` map must recommend different members in
   different regions, or bar a member where the parent is standard. A variety `delta` adjusts a
   value inside the parent's region set; it cannot move the region set.
2. **Calendar or harvest SHAPE diverges.** For example, region-dependent harvest vs year-round. A
   scalar override cannot flatten a per-region map.
3. **Archetype, lifecycle or `calendar_basis` diverges.**

A scalar difference alone (hardiness, days to maturity, fruit size) is a variety `delta`, not a
split. Taxon is neither necessary nor sufficient: cherry and beefsteak tomato are one species and
are split, while Eureka and Improved Meyer differ in taxon and the reason to split them is (1).
This is PLA-137's argument made general. It complements the master list's rule 7, which admits NEW
crops; this test is for dividing existing ones.

**Measured against the canonical (region-cell text grepped per member):**

| crop | members | test result | proposal |
|---|---|---|---|
| **lemon** | Eureka/Lisbon vs Improved Meyer (and Ponderosa) | **(1) and (2) met.** Meyer is named in 8 of 16 region cells; `low_desert_az` tells the reader to grow Eureka or Lisbon *because* Meyer is not sold there; harvest shape differs (PLA-137 §2) | **SPLIT: FIRST BATCH (C1)** |
| **persimmon** | Asian (*D. kaki*: Fuyu, Izu, Hachiya, Great Wall) vs American (*D. virginiana*: Meader, Prok) | **(1) met, in the data today.** `northern_tier`: *"Up north, grow American persimmon ... Asian persimmon usually will not survive here."* `nevada` and the California cells are Asian-only. The parent's regions map switches species by region. That is the lemon/Meyer condition, carried in prose. | **RULED 0a: SPLIT.** Sequenced after the first batch; the split re-sources ~16 region cells of a certified, launch-ready crop |
| **lime** | Persian, Key, Makrut, finger lime | Key lime is named in only 3 cells, Persian throughout: (1) not yet shown. But **Makrut is grown for its leaves** (rule 7's use pattern) and finger lime is a different genus. | **RULED 0a: NO SPLIT** (UC groups limes). Makrut (grown for leaves) and finger lime (*Microcitrus*) remain a PLA-12 variety-level question. |
| **plum** | European vs Japanese | Partial (1): every cell discusses both; only `rgv`, `ca_desert` and `low_desert_az` are Japanese-only, and "only the low-chill members fit here" is what a variety list already expresses. Pear-european/pear-asian is the precedent in favor. | **NOT NOW.** Re-test at PLA-12; `plum` also carries PLA-579. |
| lettuce-leaf | leaf, romaine, butterhead | none of (1)-(3); days-to-maturity deltas | NO SPLIT (G-12) |
| radish vs daikon | spring radish vs fall daikon | (2) is plausible (fall-only cycle); not measured cell by cell | **RULED 0a: OWN CROP** |
| mulberry | *M. alba* hybrids vs *M. nigra* (Black Beauty) | not measured | flag for PLA-12 |
| sage, oregano, dry-bean, swiss-chard | -- | all members share one taxon and one cycle | NO SPLIT |

The opposite problem, noted but not in scope: `cucumber` (generic) overlaps `slicing-`, `pickling-`
and `english-cucumber`. That is a possible MERGE, not a split. PLA-625 territory.

## 7. Recommended first batch (7 new parents + the orange widening)

| # | crop | kind | tier | why this one first |
|---|---|---|---|---|
| 1 | **meyer-lemon** | split | SPLIT | The only candidate with a **correctness** argument: today's single `lemon` cannot be right in both Sacramento and Arizona. Folds PLA-137 in. Seed data exists; parentage is triple-sourced. |
| 2 | **rutabaga** | new | S | All three T1 pages are already cited on `turnip`. Cheapest add on the list; northern fall/winter storage crop. |
| 3 | **napa cabbage** | new | S | Both T1 pages are already cited on `bok-choy`/`cabbage`. Opens Asian heading greens. |
| 4 | **southern pea / cowpea** | new | S | Both Clemson pages are already cited on the beans. It fills the biggest regional hole: the Southeast's staple legume. |
| 5 | **ground cherry** | new | S | UMN page already cited on `tomatillo`. Pre-scoped in the master list, and it fixes a live rule-7 misfile (Pineapple under `tomatillo`). |
| 6 | **rhubarb** | new | M | The batch's perennial. Third member of an existing archetype, a northern must-have, and the one real T1 hunt in the batch. |
| 7 | **lemon balm** | new | S | A test-user request on an existing archetype with a T1 factsheet already in the catalog. It gives the batch a herb. |
| + | **orange widening** (`orange-navel` -> `orange`) | widen, not new | S-M | **Ruled 2026-09-30 (follow UC), replacing the earlier sweet-orange parent.** Valencia and blood oranges (Moro, Tarocco), a test-user request, become varieties of one orange crop. Its dedicated T1 page (UA "Oranges for southern Arizona") is already cited on `orange-navel`. It rides with meyer-lemon in one citrus lane. |

**Why this shape:**
- **No new archetype, so no new gate suite.** The batch runs on the existing register and exercises
  it across 5 archetypes (`evergreen_fruit_tree`, `cool_season_annual`, `warm_season_fruiting`,
  `herbaceous_perennial`, `culinary_herb`).
- **6 of the 8 items have their dedicated T1 page already cited on a sibling.** That keeps the independent
  source-truth review pass cheap and the batch honest.
- **Zone spread:** rutabaga and rhubarb serve the north, cowpea the Southeast, Meyer lemon the
  citrus belt plus containers everywhere, and napa, ground cherry and lemon balm grow nearly anywhere.
- **Estimated ~9-11 sessions**, using section 0's tiers, against the register as it stands after
  PLA-10/PLA-11.

**Alternates, in order, if Trevor swaps:** lima bean, endive/radicchio, fennel, pineapple sage,
bachelor button. All are tier S with strong T1.

**Immediately after, in this order:**
1. **avocado + olive** (finish the shells; section 5).
2. **grape** as the vine-archetype pilot (V1); muscadine, hardy kiwi and hops follow on that archetype.
3. **The two ruled parents** (section 0a): the persimmon split (`persimmon-american`) and `daikon`.
4. **The grains and brewing lane** (wheat, barley, oats, hops): T1 hunt first, then the
   cool-season-grass pilot. Hops follows the grape vine pilot.
5. **The tropical lane** (section 4.9): a UF/IFAS + CTAHR T1 hunt first. Avocado pilots the
   subtropical tree, mango follows it, pineapple pilots the herbaceous-tropical shape, and passion
   fruit follows the vine pilot.

## 8. Parent count (for PLA-537)

Counted from the tables above (each candidate species is one; a multi-species row counts per species):

| bucket | parents |
|---|---|
| FIRST BATCH | **7** (6 new + 1 split: meyer-lemon); the orange widening adds no parent |
| RULED PARENTS (2026-09-30) | **2**: `persimmon-american` (split), `daikon` |
| WANTED LANE, T1 hunt owed (Trevor 2026-09-30) | **13**: grains and brewing 4 (wheat, barley, oats, hops); tropical 9 (pineapple, banana, papaya, mango, guava, lychee, longan, jackfruit, passion fruit) |
| LATER, with a MEASURED T1 path (DEDICATED or PARTIAL) | **41**: citrus 2, nuts 5 (pecan, chestnut, almond, pistachio, walnut), pome/stone 3, small fruit and vines 8, grains 3 (sorghum, millet, amaranth), herbs 5 (pineapple sage, fennel, tarragon, marjoram, sorrel), flowers 6, vegetables 9 (incl. broccolini) |
| APRIL PROPOSALS, not yet re-measured | **40**: the master list's proposed crops this review has no row for (the G-13 families, the lettuce heading types, mache, mizuna, tatsoi, gai lan, romanesco, chervil, stevia, shiso and others; enumerated in master list v2) |
| RULING NEEDED | 0 (all three were ruled 2026-09-30; section 0a) |
| NO SOURCE PATH | 10 (citron, hazelnut, quinoa, buckwheat, rye, barley grass, Cleveland sage, mullein, dragon fruit, starfruit) |
| VARIETY NOT PARENT | cara cara, rainbow chard, blood orange and Valencia (under `orange`), Key lime (under `lime`), the 6 interspecific Prunus, lettuce heading types (proposed) |

**For the split (PLA-537):** the roster is 128 today. The first batch takes it to **135** (7 new
parent files, one of them carved out of `lemon`; `orange-navel` is renamed in place). The measured
horizon is 135 + 2 ruled + 41 LATER + 13 wanted-lane = **~191 parents**. If all 40 April proposals
rule as parents, it reaches **~231** (master list v2's "parents planned"). Plan the layout for
**~230 parents**. Two structural points matter more than the number:
- **A split turns one crop file into two.** The per-crop layout must support that as a first-class
  operation: problem ids and variety ids copied, not re-derived (the join-key rule), and the rollup
  hash must attribute the move.
- **Per the ticket, new parents land AFTER the migration** (after PLA-11 and the split, before
  PLA-625). The migration does not have to carry them. It has to make adding a crop file as safe
  as the monolith's add-batch is today.

## 9. Not done here (by design)

No crop added, no canonical edit, no schema change. No dedicated-page hunt: every PARTIAL row still
owes one before authoring. No zone claim in this doc is sourced; each one gets sourced at authoring.
The master list's hour estimates are not reused.
