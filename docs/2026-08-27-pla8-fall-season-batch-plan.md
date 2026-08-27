# PLA-8 -- the fall-season top 20 (ruled 2026-08-27, supersedes the page-views ask)

Trevor's ruling 2026-08-27: order the ladder rollout **by season, not page views**, so testers
have ladders for the crops going into the ground for fall FIRST. The page-views ask is retired.

**The measure is the dataset's own calendars**, not a guess: for each unladdered crop, the share
of its 39 region-zone cells whose `calendar` carries a `plant` token in Aug, Sep, Oct or Nov.
Reproduce with the scan in this doc's session log; the numbers below are from canonical `674fab25`.

**Exclusion applied:** Companion & Pollinator crops (sweet-alyssum 90%, chamomile 85%, calendula
85%, borage 77%, sweet-pea 72%) and viola (100%, Edible & Harvest) score high on fall planting
but stay LAST per the standing 2026-08-26 demand ruling ("nobody has looked them"). Flagged, not
silently dropped -- overriding that ruling is Trevor's call, not the plan's.

## The top 20, with the evidence

| # | crop | fall cells | peak months | problems | category |
|--|--|--|--|--|--|
| 1 | spring-onion | 39/39 (100%) | Aug-Sep | 6 | Alliums |
| 2 | lettuce-leaf | 39/39 (100%) | Sep-Oct | 5 | Leafy Greens |
| 3 | dill | 39/39 (100%) | Sep-Oct | 5 | Herbs |
| 4 | cilantro-coriander | 39/39 (100%) | Sep-Oct | 6 | Herbs |
| 5 | spinach | 39/39 (100%) | Sep-Oct | 8 | Leafy Greens |
| 6 | arugula | 39/39 (100%) | Sep-Oct | 8 | Leafy Greens |
| 7 | garlic | 39/39 (100%) | Oct-Nov | 7 | Alliums |
| 8 | turnip | 38/39 (97%) | Sep-Oct | 9 | Root Vegetables |
| 9 | bok-choy | 38/39 (97%) | Sep-Oct | 11 | Leafy Greens |
| 10 | kohlrabi | 38/39 (97%) | Sep | 10 | Brassicas |
| 11 | radish | 37/39 (95%) | Sep | 7 | Root Vegetables |
| 12 | carrot | 36/39 (92%) | Aug-Sep | 6 | Root Vegetables |
| 13 | beet | 36/39 (92%) | Sep-Oct | 7 | Root Vegetables |
| 14 | cabbage | 36/39 (92%) | Sep | 10 | Brassicas |
| 15 | cauliflower | 34/39 (87%) | Sep-Oct | 10 | Brassicas |
| 16 | collards | 34/39 (87%) | Sep-Oct | 9 | Leafy Greens |
| 17 | broad-beans-fava | 34/39 (87%) | Oct-Nov | 7 | Beans & Peas |
| 18 | kale | 33/39 (85%) | Sep-Oct | 9 | Leafy Greens |
| 19 | brussels-sprouts | 29/39 (74%) | Sep | 9 | Brassicas |
| 20 | parsley | 28/39 (72%) | Sep-Oct | 6 | Herbs |

Just missed the cut: shallot and onion (69%), leek (64%), parsnip (49%) -- all fall-plantable in
the warm-region cells; pull any of them into an allium or root batch if a slot opens.

## The batches (family first, size second, per the playbook)

| batch | crops | problems | why together |
|--|--|--|--|
| **8. Leafy greens I** | spinach, arugula, lettuce-leaf, bok-choy | 32 | all >=97% fall; shared sourcing (aphids, flea beetles, leaf spots, damping-off); arugula/bok-choy have byte-identical history flagged in the playbook |
| **9. Roots I** | turnip, radish, carrot, beet | 29 | >=92% fall; shared root-maggot / flea-beetle / leaf-spot sourcing |
| **10. Brassica family** | cabbage, cauliflower, kohlrabi, collards, kale | 48 | collards+kale are the 25% shared-name family; one brassica source set (cabbageworms, loopers, black rot, clubroot) covers all five |
| **11. Alliums + fall herbs** | garlic, spring-onion, dill, cilantro-coriander | 24 | garlic is THE fall-planted crop (Oct-Nov, 37/39 cells); dill+cilantro share herb sourcing and both bolt-driven |
| **12. Fall finishers** | broad-beans-fava, brussels-sprouts, parsley (+ shallot/onion if room) | 22+ | the remainder of the 20; fava is the Oct-Nov sowing |

Five batches, ~155 problems, at the measured pace roughly five sessions. After the fall block the
natural next set is the spring-startable fruiting crops (peppers, eggplant, okra, melons --
melons mint `mancozeb` when they land), then the remaining odds, with microgreens + Companion &
Pollinator still LAST.

**Batch 7 (the tomatoes) precedes all of this** -- staged, read, promoting now. Not a fall crop,
but the highest-demand family and already committed to.
