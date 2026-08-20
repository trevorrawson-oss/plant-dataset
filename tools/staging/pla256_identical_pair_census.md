# PLA-256 -- identical register pair census

Read-only. No canonical change. Canonical `be8a6d1e` (confirmed by `shasum -a 256`).
Source: `tools/staging/pla256_register_pair_frame/_all_records.jsonl`, 20,168 pairs.
**This is a census. Nothing here is ruled.**

## Equality test

Exact equality only: `beginner == seasoned`, no normalization, no whitespace trimming, no case
folding. Verified two ways -- Python codepoint equality and UTF-8 byte equality return the **same
263 records**, and **0 pairs** become equal only under NFC normalization, so there is no
encoding-level ambiguity hiding in the result.

## Headline

| | count |
| -- | -- |
| **byte-identical pairs** | **263** |
| near-identical, whitespace only | **0** |
| near-identical, one punctuation mark | **4** |

263 of 20,168 pairs. Distinct crops affected: 76. Distinct field families: 14 of 166.

## By render status

| render status | identical | in frame |
| -- | -- | -- |
| A -- read and rendered | **186** | 14,595 |
| B -- read, render path unproven | **18** | 1,583 |
| C -- never referenced | **59** | 3,990 |
| total | **263** | 20,168 |

## By value type

| value type | identical | of type in frame |
| -- | -- | -- |
| `str` / `str` | 207 | 20,084 |
| `list` | 39 | 50 |
| `bool` | **17** | **17** |

**Every bool pair in the frame is identical** (17 of 17). The 39 identical lists are all
`soil.*_texture`; the 11 differing lists are the 6 melon texture pairs and the 5 companion arrays.

## By field family

| identical | family total | share of family | A / B / C | field family |
| -- | -- | -- | -- | -- |
| 60 | 728 | 8.2% | 60 / 0 / 0 | `growth_stages[] :: log_prompt` |
| 56 | 420 | 13.3% | 56 / 0 / 0 | `failure_diagnostics[] :: label` |
| 36 | 505 | 7.1% | 36 / 0 / 0 | `notifications[] :: title` |
| 20 | 1,808 | 1.1% | 0 / 0 / 20 | `regions.<R> :: region_notes` |
| 18 | 348 | 5.2% | 0 / 18 / 0 | `weather_triggers[] :: title` |
| 17 | 120 | 14.2% | 17 / 0 / 0 | `start_method :: hardening_off` |
| 15 | 46 | 32.6% | 0 / 0 / 15 | `soil :: tolerated_texture` |
| 12 | 46 | 26.1% | 0 / 0 / 12 | `soil :: preferred_texture` |
| 12 | 46 | 26.1% | 0 / 0 / 12 | `soil :: problematic_texture` |
| 8 | 8 | 100.0% | 8 / 0 / 0 | `pests[] :: name` |
| 6 | 1,147 | 0.5% | 6 / 0 / 0 | `tips_by_stage.<stage>[] :: text` |
| 1 | 493 | 0.2% | 1 / 0 / 0 | `failure_diagnostics[] :: next_season_tip` |
| 1 | 493 | 0.2% | 1 / 0 / 0 | `failure_diagnostics[] :: what_happened` |
| 1 | 8 | 12.5% | 1 / 0 / 0 | `diseases[] :: name` |

## Near-identical, reported separately

**Leading/trailing whitespace only: 0.** No pair in the frame differs from its counterpart
by whitespace alone. A trailing space would not have been counted as identical, and none exists.

**Exactly one punctuation mark: 4.** All four are `lettuce-leaf`, and all four are the
same edit, a comma becoming a colon:

| crop | field path | render | beginner | seasoned |
| -- | -- | -- | -- | -- |
| `lettuce-leaf` | `notifications[2].title` | A | Heat incoming, watch your greens for bolting | Heat incoming: watch your greens for bolting |
| `lettuce-leaf` | `weather_triggers[0].title` | B | Heat alert, harvest your greens now | Heat alert: harvest your greens now |
| `lettuce-leaf` | `weather_triggers[1].title` | B | Unexpected frost, protect young greens | Unexpected frost: protect young greens |
| `lettuce-leaf` | `weather_triggers[2].title` | B | High humidity, watch for downy mildew | High humidity: watch for downy mildew |

## Full list -- render status A

All **186** identical pairs that are on a screen today, grouped by field family, sorted by
`(field_family, crop_slug, field_path)`.


### `diseases[] :: name` -- 1

| crop | field path | shared value |
| -- | -- | -- |
| `wheatgrass` | `diseases[0].name` | Mold and damping-off |

### `failure_diagnostics[] :: label` -- 56

| crop | field path | shared value |
| -- | -- | -- |
| `beefsteak-tomato` | `failure_diagnostics[0].label` | Frost or cold damage |
| `beefsteak-tomato` | `failure_diagnostics[1].label` | Pests or disease |
| `beefsteak-tomato` | `failure_diagnostics[2].label` | Too much water |
| `beefsteak-tomato` | `failure_diagnostics[3].label` | Too little water |
| `beefsteak-tomato` | `failure_diagnostics[4].label` | Not enough sun |
| `blackberry` | `failure_diagnostics[0].label` | Little or no fruit (often a pruning mistake) |
| `blueberry` | `failure_diagnostics[0].label` | Yellow leaves with green veins (iron chlorosis from high pH) |
| `blueberry` | `failure_diagnostics[1].label` | Little or no fruit |
| `blueberry` | `failure_diagnostics[2].label` | Wilting, dieback, and decline in wet soil |
| `blueberry` | `failure_diagnostics[3].label` | Fruit disappearing as it ripens |
| `blueberry` | `failure_diagnostics[4].label` | Weak growth from wrong soil or fertilizer |
| `cherry-tomato` | `failure_diagnostics[0].label` | Frost or cold damage |
| `cherry-tomato` | `failure_diagnostics[1].label` | Pests or disease |
| `cherry-tomato` | `failure_diagnostics[2].label` | Too much water |
| `cherry-tomato` | `failure_diagnostics[4].label` | Not enough sun |
| `elderberry` | `failure_diagnostics[0].label` | Little or no fruit |
| `elderberry` | `failure_diagnostics[1].label` | Fruit disappearing as it ripens |
| `elderberry` | `failure_diagnostics[2].label` | Feeling sick after eating the berries |
| `elderberry` | `failure_diagnostics[3].label` | Individual canes wilting and dying |
| `elderberry` | `failure_diagnostics[4].label` | Overgrown thicket with poor fruiting |
| `grape-tomato` | `failure_diagnostics[0].label` | Frost or cold damage |
| `grape-tomato` | `failure_diagnostics[1].label` | Pests or disease |
| `grape-tomato` | `failure_diagnostics[2].label` | Too much water |
| `grape-tomato` | `failure_diagnostics[4].label` | Not enough sun |
| `heirloom-tomato` | `failure_diagnostics[0].label` | Frost or cold damage |
| `heirloom-tomato` | `failure_diagnostics[1].label` | Pests or disease |
| `heirloom-tomato` | `failure_diagnostics[2].label` | Too much water |
| `heirloom-tomato` | `failure_diagnostics[3].label` | Too little water |
| `heirloom-tomato` | `failure_diagnostics[4].label` | Not enough sun |
| `lettuce-leaf` | `failure_diagnostics[0].label` | Frost or cold damage |
| `lettuce-leaf` | `failure_diagnostics[1].label` | Pests or disease |
| `lettuce-leaf` | `failure_diagnostics[2].label` | Too much water or bolting |
| `lettuce-leaf` | `failure_diagnostics[3].label` | Too little water |
| `lettuce-leaf` | `failure_diagnostics[4].label` | Bolted too quickly |
| `nasturtium` | `failure_diagnostics[1].label` | Plant covered in aphids |
| `okra` | `failure_diagnostics[0].label` | Tough, over-mature pods |
| `okra` | `failure_diagnostics[3].label` | Pests or disease |
| `okra` | `failure_diagnostics[4].label` | Frost or cold damage |
| `parsnip` | `failure_diagnostics[0].label` | Seeds did not come up |
| `pomegranate` | `failure_diagnostics[3].label` | The fruit was pale, sour, or small |
| `potato` | `failure_diagnostics[0].label` | Green potatoes |
| `potato` | `failure_diagnostics[2].label` | Rough, scabby skin |
| `raspberry` | `failure_diagnostics[0].label` | Little or no fruit (often a pruning mistake) |
| `raspberry` | `failure_diagnostics[1].label` | Crumbly berries that fall apart |
| `raspberry` | `failure_diagnostics[2].label` | Canes wilting, dying back, or snapping |
| `raspberry` | `failure_diagnostics[3].label` | Plants declining in wet soil |
| `raspberry` | `failure_diagnostics[4].label` | Fruit disappearing or full of maggots |
| `roma-tomato` | `failure_diagnostics[0].label` | Frost or cold damage |
| `roma-tomato` | `failure_diagnostics[1].label` | Pests or disease |
| `roma-tomato` | `failure_diagnostics[2].label` | Too much water |
| `roma-tomato` | `failure_diagnostics[4].label` | Not enough sun |
| `strawberry` | `failure_diagnostics[2].label` | Berries rotting with gray fuzz |
| `tomatillo` | `failure_diagnostics[1].label` | Frost or cold damage |
| `tomatillo` | `failure_diagnostics[2].label` | Pests or disease |
| `tomatillo` | `failure_diagnostics[3].label` | Too much water |
| `tomatillo` | `failure_diagnostics[5].label` | Not enough sun |

### `failure_diagnostics[] :: next_season_tip` -- 1

| crop | field path | shared value |
| -- | -- | -- |
| `lettuce-leaf` | `failure_diagnostics[0].next_season_tip` | Cover seedlings with fleece if frost threatens during their first few weeks, when they are most tender. Once established, leafy greens generally co... |

### `failure_diagnostics[] :: what_happened` -- 1

| crop | field path | shared value |
| -- | -- | -- |
| `lettuce-leaf` | `failure_diagnostics[4].what_happened` | Heat and long days drive most leafy greens to bolt, and it is the single most common reason they disappoint. The plant is not dying; it is doing ex... |

### `growth_stages[] :: log_prompt` -- 60

| crop | field path | shared value |
| -- | -- | -- |
| `arugula` | `growth_stages[0].log_prompt` | Any sprouts yet? |
| `arugula` | `growth_stages[1].log_prompt` | How are they coming along? |
| `arugula` | `growth_stages[2].log_prompt` | Ready to start cutting? |
| `arugula` | `growth_stages[3].log_prompt` | Harvesting regularly? |
| `arugula` | `growth_stages[4].log_prompt` | Seen a flower stalk yet? |
| `asparagus` | `growth_stages[0].log_prompt` | How is the new bed filling in? |
| `asparagus` | `growth_stages[1].log_prompt` | Are the spears coming up? |
| `asparagus` | `growth_stages[2].log_prompt` | How tall are the ferns getting? |
| `asparagus` | `growth_stages[3].log_prompt` | Have the ferns died back yet? |
| `cherry-tomato` | `growth_stages[0].log_prompt` | Have you seen any sprouts yet? |
| `cherry-tomato` | `growth_stages[1].log_prompt` | How are your seedlings looking? |
| `cherry-tomato` | `growth_stages[2].log_prompt` | Are they outside yet, or still hardening off? |
| `cherry-tomato` | `growth_stages[3].log_prompt` | Flowers open yet? |
| `cherry-tomato` | `growth_stages[4].log_prompt` | First tomatoes picked? Log your harvest. |
| `cherry-tomato` | `growth_stages[5].log_prompt` | How was your season? Worth logging what worked. |
| `chives` | `growth_stages[0].log_prompt` | Any sprouts yet? |
| `chives` | `growth_stages[2].log_prompt` | Harvesting regularly? |
| `cilantro-coriander` | `growth_stages[0].log_prompt` | Any sprouts yet? |
| `cilantro-coriander` | `growth_stages[1].log_prompt` | How are they coming along? |
| `cilantro-coriander` | `growth_stages[2].log_prompt` | Ready to start cutting? |
| `cilantro-coriander` | `growth_stages[3].log_prompt` | Harvesting regularly? |
| `cilantro-coriander` | `growth_stages[4].log_prompt` | Seen a flower stalk yet? |
| `dill` | `growth_stages[0].log_prompt` | Any sprouts yet? |
| `dill` | `growth_stages[1].log_prompt` | How are they coming along? |
| `dill` | `growth_stages[2].log_prompt` | Ready to start cutting? |
| `dill` | `growth_stages[3].log_prompt` | Harvesting regularly? |
| `dill` | `growth_stages[4].log_prompt` | Seen a flower stalk yet? |
| `grape-tomato` | `growth_stages[0].log_prompt` | Have you seen any sprouts yet? |
| `grape-tomato` | `growth_stages[1].log_prompt` | How are your seedlings looking? |
| `grape-tomato` | `growth_stages[2].log_prompt` | Are they outside yet, or still hardening off? |
| `grape-tomato` | `growth_stages[3].log_prompt` | Flowers open yet? |
| `grape-tomato` | `growth_stages[4].log_prompt` | First tomatoes picked? Log your harvest. |
| `grape-tomato` | `growth_stages[5].log_prompt` | How was your season? Worth logging what worked. |
| `lettuce-leaf` | `growth_stages[0].log_prompt` | Any sprouts yet? |
| `lettuce-leaf` | `growth_stages[1].log_prompt` | How are they coming along? |
| `lettuce-leaf` | `growth_stages[2].log_prompt` | Ready to start harvesting outer leaves? |
| `lettuce-leaf` | `growth_stages[3].log_prompt` | Harvesting regularly? |
| `lettuce-leaf` | `growth_stages[4].log_prompt` | Seen a flower stalk yet? |
| `okra` | `growth_stages[0].log_prompt` | Have you seen any sprouts yet? |
| `okra` | `growth_stages[1].log_prompt` | How are your okra seedlings looking? |
| `okra` | `growth_stages[2].log_prompt` | How tall is your okra getting? |
| `okra` | `growth_stages[3].log_prompt` | Flowers open yet? |
| `okra` | `growth_stages[4].log_prompt` | First pods picked? Log your harvest. |
| `okra` | `growth_stages[5].log_prompt` | How was your okra season? Worth logging what worked. |
| `parsley` | `growth_stages[0].log_prompt` | Any sprouts yet? |
| `parsley` | `growth_stages[1].log_prompt` | How are they coming along? |
| `parsley` | `growth_stages[2].log_prompt` | Ready to start cutting? |
| `parsley` | `growth_stages[3].log_prompt` | Harvesting regularly? |
| `roma-tomato` | `growth_stages[0].log_prompt` | Have you seen any sprouts yet? |
| `roma-tomato` | `growth_stages[1].log_prompt` | How are your seedlings looking? |
| `roma-tomato` | `growth_stages[2].log_prompt` | Are they outside yet, or still hardening off? |
| `roma-tomato` | `growth_stages[3].log_prompt` | Flowers open yet? |
| `roma-tomato` | `growth_stages[4].log_prompt` | First tomatoes picked? Log your harvest. |
| `roma-tomato` | `growth_stages[5].log_prompt` | How was your season? Worth logging what worked. |
| `tomatillo` | `growth_stages[0].log_prompt` | Have you seen any sprouts yet? |
| `tomatillo` | `growth_stages[1].log_prompt` | How are your seedlings looking? |
| `tomatillo` | `growth_stages[2].log_prompt` | Is your plant filling out and starting to flower? |
| `tomatillo` | `growth_stages[3].log_prompt` | Are the husks starting to fill with fruit? |
| `tomatillo` | `growth_stages[4].log_prompt` | Have you started harvesting? |
| `tomatillo` | `growth_stages[5].log_prompt` | Have you cleared the bed for the season? |

### `notifications[] :: title` -- 36

| crop | field path | shared value |
| -- | -- | -- |
| `bee-balm` | `notifications[0].title` | Time to plant bee balm |
| `beefsteak-tomato` | `notifications[2].title` | Last frost has passed: time to transplant |
| `beefsteak-tomato` | `notifications[3].title` | Your tomatoes should be flowering soon |
| `beefsteak-tomato` | `notifications[4].title` | First tomatoes should be nearly ready |
| `beefsteak-tomato` | `notifications[5].title` | First frost in {{weeks_until_anchor}} weeks: finish strong |
| `beefsteak-tomato` | `notifications[6].title` | How are your tomatoes doing? |
| `beet` | `notifications[2].title` | Time to thin your beets |
| `broad-beans-fava` | `notifications[2].title` | Start checking your fava pods |
| `carrot` | `notifications[2].title` | Time to thin your carrots |
| `celery` | `notifications[3].title` | Feed your celery |
| `cherry-tomato` | `notifications[6].title` | How are your tomatoes doing? |
| `echinacea` | `notifications[0].title` | Time to plant coneflowers |
| `grape-tomato` | `notifications[6].title` | How are your tomatoes doing? |
| `heirloom-tomato` | `notifications[2].title` | Last frost has passed: time to transplant |
| `heirloom-tomato` | `notifications[3].title` | Your tomatoes should be flowering soon |
| `heirloom-tomato` | `notifications[4].title` | First tomatoes should be nearly ready |
| `heirloom-tomato` | `notifications[5].title` | First frost in {{weeks_until_anchor}} weeks: finish strong |
| `heirloom-tomato` | `notifications[6].title` | How are your tomatoes doing? |
| `lettuce-leaf` | `notifications[0].title` | Time to sow your leafy greens |
| `lettuce-leaf` | `notifications[1].title` | Your greens should be ready to start picking |
| `lettuce-leaf` | `notifications[3].title` | Time to sow your fall leafy greens |
| `lettuce-leaf` | `notifications[4].title` | How are your greens looking? |
| `okra` | `notifications[0].title` | Time to plant your okra |
| `okra` | `notifications[1].title` | Thin your okra seedlings |
| `okra` | `notifications[2].title` | Okra should be flowering soon |
| `okra` | `notifications[3].title` | Your first okra pods are nearly ready |
| `okra` | `notifications[6].title` | How is your okra doing? |
| `parsnip` | `notifications[2].title` | Time to thin your parsnips |
| `pole-beans` | `notifications[1].title` | Start checking your beans |
| `potato` | `notifications[0].title` | Time to plant potatoes |
| `radish` | `notifications[1].title` | Time to thin your radishes |
| `roma-tomato` | `notifications[6].title` | How are your tomatoes doing? |
| `sunflower` | `notifications[1].title` | Stake tall sunflowers |
| `sweet-potato` | `notifications[0].title` | Time to plant sweet potato slips |
| `tomatillo` | `notifications[6].title` | How are your tomatillos doing? |
| `turnip` | `notifications[1].title` | Time to thin your turnips |

### `pests[] :: name` -- 8

| crop | field path | shared value |
| -- | -- | -- |
| `arugula-microgreens` | `pests[0].name` | Fungus gnats |
| `broccoli-microgreens` | `pests[0].name` | Fungus gnats |
| `cilantro-microgreens` | `pests[0].name` | Fungus gnats |
| `microgreens-mix` | `pests[0].name` | Fungus gnats |
| `pea-shoots` | `pests[0].name` | Fungus gnats |
| `radish-microgreens` | `pests[0].name` | Fungus gnats |
| `sunflower-sprouts` | `pests[0].name` | Fungus gnats |
| `wheatgrass` | `pests[0].name` | Fungus gnats |

### `start_method :: hardening_off` -- 17

| crop | field path | shared value |
| -- | -- | -- |
| `arugula` | `start_method.hardening_off` | false |
| `basil` | `start_method.hardening_off` | true |
| `bok-choy` | `start_method.hardening_off` | true |
| `broccoli` | `start_method.hardening_off` | true |
| `brussels-sprouts` | `start_method.hardening_off` | true |
| `cabbage` | `start_method.hardening_off` | true |
| `cauliflower` | `start_method.hardening_off` | true |
| `chives` | `start_method.hardening_off` | true |
| `cilantro-coriander` | `start_method.hardening_off` | false |
| `collards` | `start_method.hardening_off` | true |
| `dill` | `start_method.hardening_off` | false |
| `kale` | `start_method.hardening_off` | true |
| `kohlrabi` | `start_method.hardening_off` | true |
| `lemongrass` | `start_method.hardening_off` | true |
| `mint` | `start_method.hardening_off` | true |
| `parsley` | `start_method.hardening_off` | true |
| `spinach` | `start_method.hardening_off` | false |

### `tips_by_stage.<stage>[] :: text` -- 6

| crop | field path | shared value |
| -- | -- | -- |
| `tomatillo` | `tips_by_stage.end_of_season[0].text` | Harvest all usable fruit before the first frost (husk-on fruit stores for weeks), then clear the bed; expect volunteers next spring. |
| `tomatillo` | `tips_by_stage.established[0].text` | Cage or stake each plant at transplant, they sprawl to 3 to 4 feet. Water deeply about weekly; feed lightly to favor fruit over foliage. |
| `tomatillo` | `tips_by_stage.flowering[0].text` | Empty husks forming with no fruit inside usually means pollination is failing, the fix is a second plant nearby and bee-friendly (spray-free) blooms. |
| `tomatillo` | `tips_by_stage.germination[0].text` | Sow at least two tomatillo plants, ideally two varieties; a single plant will not set fruit. Germinate at 75 to 85°F for fast emergence. |
| `tomatillo` | `tips_by_stage.harvest[0].text` | Pick when fruit fills and splits its husk, while still firm and green for tart flavor; gather dropped fruit, which keeps in its husk. |
| `tomatillo` | `tips_by_stage.seedling[0].text` | Grow seedlings in bright light to keep them stocky, and harden off for 7 to 10 days before transplanting after frost. |

> The 17 `start_method.hardening_off` rows are **booleans**, not the strings `"true"`/`"false"`;
> they are shown as JSON literals above.

## Crop concentration (all 263)

| identical pairs | crop |
| -- | -- |
| 17 | `tomatillo` |
| 16 | `lettuce-leaf` |
| 14 | `okra` |
| 11 | `cherry-tomato` |
| 11 | `roma-tomato` |
| 11 | `grape-tomato` |
| 11 | `turnip` |
| 11 | `beet` |
| 10 | `beefsteak-tomato` |
| 10 | `heirloom-tomato` |
| 6 | `arugula` |
| 6 | `cilantro-coriander` |
| | *(64 more crops with fewer)* |

