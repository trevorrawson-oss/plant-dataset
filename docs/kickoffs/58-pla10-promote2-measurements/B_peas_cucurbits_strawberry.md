# Agent B: PLA-10 promote 2 measurement for peas, cucurbits and strawberry (READ-ONLY)

Base: branch `main`, HEAD 78d734b, canonical sha256 cf1d480d (matches LATEST.txt). No repo file was edited.
Evidence: raw bytes from `tools/.evidence_cache` (EV, MANIFEST url) or `tools/.doc_cache/<sha1(url)>.txt` (DOC),
normalized with `pla10_promote_common.norm_text`, so the quotes below are lowercased. Nothing was fetched.
Pages marked DOC-only have no hashed copy in `.evidence_cache`. Promote 1 quoted only from the hashed EVIDENCE set,
so a promote-2 figure taken from a DOC-only page needs those bytes saved into the evidence cache first.

## The two admitted technique pages (both EV)

**umn_ext_trellises_cages** (EV 8ee29202..., DOC copy identical):
- "varieties with fruit weighing up to three pounds and no larger than a cucumber, small melon or small winter squash, work best." (under "trellises for vine crops"; follows "you can grow many long-vined varieties successfully in small spaces if you train them to grow on trellises.")
- "planting crops with trellises plant the vines at the foot of the trellis at the same spacing between the seeds or transplants as if they were going to grow on the ground."
- "larger squash and pumpkins are too heavy to trellis. grow them on the ground."
- "cucumbers and small squash do not slip from the vine, so they do not need support." (this is about slings, not about trellising)
- "beans and peas you can grow beans and peas on a trellis. while some beans are bush types, and some pea varieties do not grow long nor tall, others produce long vines that need support."
- Height: "a six-foot stake pounded a foot into the ground will leave five feet of trellis area." This is the height of the STRUCTURE, not of the plant, so it is not a `mature_height_ft` candidate.
- No row spacing for a trellised planting anywhere on the page. The PLA-532 kickoff ruling still applies: trellis entries get `row_spacing_inches: null` with reason `not_authored`.

**vce_hort_189** (EV 9a7d9d6a...):
- "pole beans, peas, cucumbers, melons, and tomatoes are excellent candidates."
- "caging is used for heavier crops, including melons and summer/winter squashes that may overburden a trellis or stake due to weight of produce."
- "the size of cages varies depending on plant spacing and type of crop." It states no plant spacing. It points toward a `cage` support for melons and squash, but there is no figure to author, so D7 blocks a `row-cage` entry.

## Task 1: Peas

The spec §10.2 rule: replacing the promote-1 `row-none` is safe only while no consumer persists an entry id, so it must happen before PLA-629. **All three recommendations below KEEP `row-none` as the default, so no entry is replaced and the PLA-629 ordering does not bind.** Adding a non-default entry does not change any id.

**Inference flag (all peas).** UMN's same-spacing sentence sits under the vine-crop section. PLA-532's independent review already recorded that "extending it to peas is an inference", and this measurement confirms it: no pea page states a trellised in-row spacing. PLA-532 also recorded "Not found in T1: a row spacing for trellised peas."

### snow-peas: canonical `row-none` in_row [1,3], row [18,18] (umd_ext); 1 entry today
- UMD peas (EV 45bf3174): "plant in wide rows, about 18 inches apart. ... plants grown together will hold each other up or can be trellised to make harvesting easier." Support is optional, so **(a) keep `row-none`**. This is the deciding sentence.
- UMD: "determinate cultivars ... are bushy and less than 3 ft. in height; indeterminate cultivars ... will grow to over 5 ft. in height." Need for support is a cultivar property (habit is not an entry axis, §1.1).
- USU (EV 50480fe0): "support most pea varieties are self-supporting during growth. taller pea varieties are more productive and easier to harvest if caged, trellised, or fenced. ... snap and snow peas climb naturally so little additional work is required other than constructing the supports." This is the closest call: it names snow and snap peas specifically, but frames support as a yield and harvest benefit, not a requirement. USU also lists a dwarf snow pea ("dwarf grey sugar").
- UMN growing-peas (DOC-only): "tall vine varieties can grow up to five feet tall. the vines need a trellis to support them as they climb. ... shorter or "bush" types are only two to three feet tall ... you can plant shorter bush types in a single row near a trellis or in a row, between 12 and 18 inches wide, where the plants will cling to and support each other."
- Clemson garden-peas (DOC-only): "pea plants, even dwarf varieties, benefit from some type of support" ... "sow pea seeds 1 to 1½ inches deep and 1 to 2 inches apart in single, double, or wide rows" ... "regardless of row type planted, space rows 2 feet apart."
- **Optional non-default `row-trellis`.** in_row = the ground figure [1,3] (via UMN, an inference). If Clemson is used instead, in_row [1,2] and row [24,24]: Clemson gives a single spacing for every row type and recommends support for every pea. That is one page carrying both the support and the spacing, a weaker inference than borrowing UMN's vine rule, but **it conflicts with the kickoff ruling that trellis rows are null**, so it needs a ruling.
- Count: 1 (keep), or 2 if `row-trellis` is added.

### sugar-snap-peas: canonical `row-none` in_row [1,2], row [12,24] (usu_ext); 1 entry today
- The crop's own spacing source, USU, decides it: "most pea varieties are self-supporting during growth" plus the "snap and snow peas climb naturally" sentence quoted above. **(a) keep `row-none`.**
- The UMD, UMN and Clemson evidence is the same as for snow-peas.
- Optional `row-trellis` with in_row [1,2] (the ground figure), row null/not_authored. Same inference flag as snow-peas.
- Count: 1, or 2.

### sweet-pea: canonical `row-none` in_row [5,6], row null/not_authored (osu_ext); 1 entry today
- **The pages disagree with the spec's expectation that sweet-pea requires support.** The crop's own spacing source, OSU news (EV 364a06cb), says: "today, bush or dwarf types such as 'supersnoop' make colorful hedges along walkways or in planters. taller climbing varieties, including 'old spice mix' or 'royal family,' can be trained on fences and trellises." Spacing: "sow seeds ¾-1 inch deep and 2 inches apart. ... thin seedlings to 5-6 inches apart."
- NCSU lathyrus-odoratus (DOC-only): "plants may be grown in bushy mounds or as climbers, but climbers will need a support structure."
- UC IPM sweetpea (DOC-only): "some are trailing types that may trail over rocks, fences, or trellises. bush types may do well in borders, beds, or pots."
- The crop's own `description_beginner` already says "...though there are short bushy types that need no support."
- Only Cornell high tunnels (EV 813ad15f, catalog id `cornell_ext`) says it is required: "plants must be provided with a trellis to support them as they grow." That page covers commercial high-tunnel cut-flower production (a SCOPE flag).
- **Recommendation: (a) keep `row-none` as the default and add a non-default `row-trellis` from Cornell**: "plant spacing: 2 to 4 plants per foot on a trellis, with rows 4 to 6 ft. apart."
  - row = [48,72], a direct feet conversion.
  - in_row = [3,6] is ARITHMETIC (12/4 to 12/2), not a stated inches figure. This is the only pea trellis spacing on a cited page; PLA-532 row A confirms that sweet-pea "already [has] a support-conditional spacing".
  - **Guard hazard:** `quote_states` would pass in_row [3,6] on the "6" of "rows 4 to 6 ft". That is a coincidental match on the row figure, not evidence for the in-row value, so the in-row needs a hand adjudication or a derivation note.
- Height for the trellised form, an override candidate: NCSU says "if allowed to climb, it will reach up to 8 feet. if grown as a bush, it will grow to a 3 foot tall bush." Its dimensions read "height: 3 ft. - 8 ft." So the climbing form tops out at 8 ft, but no page gives a lower bound for it. The canonical prose says "5 to 8 ft"; no cached sweet-pea page found states 5.
- Count: 2 (`row-none` default + `row-trellis`).

### Pea heights (Task 4)
- UMN growing-peas: tall vines "up to five feet tall"; bush types "two to three feet tall".
- UMD: indeterminate cultivars "over 5 ft."; determinate cultivars "less than 3 ft."
- Every trellised-form figure is open-ended (up to 5, over 5), so none gives a closed `[lo,hi]` for an override.

## Task 2: Melons and squash (UMN's ~3 lb rule)

| crop | entries now | proposed | trellis in_row (= ground, per UMN) | basis |
| -- | -- | -- | -- | -- |
| cantaloupe | 2 (row-none default [24,36] row [60,90] vce_426_331; hill-none) | **3** (+row-trellis) | [24,36] | qualifies at CULTIVAR level only, see below |
| honeydew-melon | 2 (row-none default [18,24] clemson; hill-none usu) | **3** (+row-trellis), weaker case | [18,24] | INFERENCE, see below |
| watermelon | 2 (hill-none default; row-none [60,72]) | 2 | n/a | does not qualify |
| acorn-squash | 1 (row-none [24,36] row [60,72] umn_ext) | **2** (+row-trellis) | [24,36] | QUOTED by name |
| butternut-squash | 1 | 1 | n/a | no quoted basis |
| spaghetti-squash | 1 | 1 | n/a | no quoted basis |
| pumpkin | 2 (hill-none default; row-none) | 2 | n/a | UMN excludes it by name |
| zucchini-courgette | 2 (row-none default [24,36] umd; hill-none) | 2 | n/a | non-vining bush |
| yellow-summer-squash | 2 (same as zucchini) | 2 | n/a | non-vining bush |

Every trellis entry would carry row null/not_authored, sources [ground page id, umn_ext_trellises_cages], and no height override, because no cached page states a trellised-form height for any cucurbit.

**cantaloupe** (flag: qualification rests on cultivar size)
- USU cantaloupe (EV 3699b298) has the only crop-level, unqualified statement: "how can i grow muskmelons (cantaloupes) in a small garden? cantaloupe plants can be trained to a fence or trellis or grown in a large pot. after the fruits begin to enlarge they will need some support or the fruit weight may damage the vines."
- ISU melons (EV d84b3b2f): "they can, however, be trained to trellises, although support must be given to the large developing fruit as it enlarges and ripens."
- ISU's cultivar weights are MOSTLY ABOVE 3 lb: 'aphrodite' 6 to 9 lb, 'athena' 4 to 6 lb, 'ambrosia' 4 to 5 lb, 'divergent' 4 lb, 'goddess' 6-8 lb, 'hale's best' 4 to 5 lb, 'superstar' 6 to 8 lb. Only 'sarah's choice' 3 lb and 'sugar cube' 2 lb fall at or under UMN's 3 lb.
- UMN melons (DOC-only): "you can grow small-fruited melon plants in small gardens by training the plant to a fence or trellis." Its ground spacing: "plant the potted seedlings about two feet apart, in rows five feet apart."
- So under UMN's rule, typical cantaloupe fruit exceeds 3 lb, and the crop qualifies only for small-fruited cultivars. §1.1 keeps cultivar out of the entry axis, so whether to author this needs a ruling.
- **Contradiction flag:** UMD melons (DOC-only), cited by both cantaloupe and honeydew, says "growing plants on a trellis allows closer spacing but each trellised melon (using cultivars that produce small fruit) must be supported by a sling". This contradicts UMN's "same spacing" for melons, though UMD gives no figure.

**honeydew-melon** (flag: INFERENCE)
- No cached page gives a crop-level honeydew fruit weight or a honeydew-specific trellis statement.
- ISU's "they can ... be trained to trellises" covers honeydew because that page explicitly covers cantaloupe, muskmelon and honeydew. Its only honeydew weight is cultivar-level: "'snow leopard' (honeydew type, 2 lb.)".
- The USU honeydew and Clemson cantaloupe-honeydew pages say nothing about trellis or fruit weight.
- Qualifying honeydew under the 3 lb rule is an inference.

**watermelon**: does not qualify
- USU watermelon (DOC-only): "crimson sweet and mirage hybrid are large (15-25 lb.) ... mickylee and minilee are smaller (10-15 lb.) icebox types." Even the icebox types are 3 to 5 times UMN's 3 lb.
- UGA C1035 lists "small palm melon, solitaire" without weights.
- UMD: "vines range in length from 6 ft. (bush types) to 20 ft."
- No entry. Not flagged as an inference: the exclusion follows from a quoted weight.

**acorn-squash**: qualifies, QUOTED
- The crop's own spacing page, UMN pumpkins-and-winter-squash (EV fbdd6554), says: "you can train small-fruited squash like delicata or acorn to a trellis to save space. large-fruited squash are too heavy to trellis, so you should grow them on the ground."
- Ground figure: "plant pumpkin and winter squash seeds three-fourths of an inch deep, 24 to 36 inches apart. use the closer spacing if the variety is a bush type. spacing between rows should be 5 to 6 feet."
- **Nuance flag:** trellising is for long-vined types (UMN trellis page), and this page ties the 24 end to bush types. A strict reading makes the vining (trellised) in-row closer to 36 than [24,36]. Copying [24,36] follows UMN's "same spacing" rule literally.

**butternut-squash, spaghetti-squash**: no quoted basis
- UMN names only "delicata or acorn" and says "some varieties produce small squashes ... others produce enormous fruits of fifteen pounds or more".
- No cached cited page gives a butternut or spaghetti fruit weight.
- Calling them small winter squash under 3 lb would be an INFERENCE. Recommend no entry unless ruled.

**pumpkin**: excluded by name
- UMN trellis page: "larger squash and pumpkins are too heavy to trellis." UF pumpkins (DOC-only) calls the "smaller pumpkins ... usually around 6 or 7 lbs" ('funny face').
- No entry.

**zucchini-courgette, yellow-summer-squash**: non-vining bushes
- The crops' own spacing source, UMD summer squash (EV ee47396a), says: "summer squash grows on non-vining bushes."
- UF VH021 (EV): "summer squash and zucchini are usually bush types; winter squash have a spreading, vining habit."
- UMN summer-squash (DOC-only) does acknowledge trellising ("plants that you have trellised to grow vertically may need watering more often.") but gives no spacing for it and no fruit weight.
- VCE HORT-189 suggests CAGES for summer squash, with no spacing.
- **Flag if anyone authors a trellis entry:** "same spacing as on the ground" would have to use UMN's VINING-type figure, not canonical's UMD bush [24,36]. UMN: "for vining types ... sow their seeds two inches apart. allow about two or three feet of space on either side of the row ... thin seedlings to stand eight to 12 inches apart." Recommend no entry.

## Task 3: Strawberry `row-none-bed`

- Canonical has one entry today: `row-none` default, in_row [18,24], row [36,48] (umn_ext). The crop's ca_interior plant_out cell (sources uc_ipm + uc_costs_strawberry_sjv) already says "Space plants about 12 inches apart in two-row beds".
- **Stating page:** UC IPM "Cultural Tips for Growing Strawberry", https://ipm.ucanr.edu/home-and-landscape/cultural-tips-for-growing-strawberry (catalog `uc_ipm`, verified 2026-06-21). It is **DOC-only** (d13dc81c), not in `.evidence_cache`.
  - "make raised beds about 6 inches high and about 10 inches wide across the top if you are planting one row of strawberries, or 18 inches wide if you are planting two rows."
  - "two rows of plants work well, and you can run a drip line down the middle of the bed between them."
  - "space plants about 12 inches apart in each row with rows about 12 inches apart in two-row beds, and stagger the plants in the two rows to give them maximum growing room."
  - "in single-row beds, space plants about 10 inches apart."
- The same text is also cached as the cited PDF https://ucanr.edu/sites/default/files/2018-03/281247.pdf (DOC 668bc635).
- Corroborating commercial page (SCOPE): UC cost study SJV 2004 (DOC ae68c2b0), "strawberries are planted in august on 52-inch beds, two rows per bed at 12-inch plant spacing"; "bed width in the region ranges from 52 to 56 inches."
- Candidate entry: `row-none-bed`, rows_per_bed 2, in_row [12,12], sources [uc_ipm]. Count: 2 entries.
- **Flags:**
  1. Meaning of `row_spacing_inches` on a bed entry. UC IPM's "rows about 12 inches apart" is the WITHIN-bed row spacing. No home page gives a between-bed or bed-center distance (it mentions only "furrows between beds"; the 52-56 in bed is commercial). §1.1 does not say which one `row_spacing_inches` means when `rows_per_bed` is present, so this needs a ruling: [12,12] within the bed, or null/not_authored.
  2. The page is DOC-only, so hashed bytes must be saved into the evidence cache before promote.
  3. The entry is crop-level, while the spec frames it as "ca_interior two-row beds". UC IPM is a statewide California home-garden page, and the entry has no region axis.

## Task 4: Heights summary
- No cached page states a trellised-form height for any cucurbit.
- Peas: open-ended figures only ("up to five feet", "over 5 ft").
- Sweet-pea: NCSU "up to 8 feet" climbing and "3 foot tall bush"; the only closed range on the page is "3 ft. - 8 ft.", which spans both forms.
- The UMN 5 ft and VCE 6 to 8 ft figures are stake and trellis heights, not plant heights.

## Entry counts (now -> proposed)
snow-peas 1 -> 1 (or 2, optional trellis); sugar-snap-peas 1 -> 1 (or 2); sweet-pea 1 -> 2; cantaloupe 2 -> 3 (ruling); honeydew 2 -> 3 (ruling, inference); watermelon 2 -> 2; acorn 1 -> 2; butternut 1 -> 1; spaghetti 1 -> 1; pumpkin 2 -> 2; zucchini 2 -> 2; yellow-summer-squash 2 -> 2; strawberry 1 -> 2.

## Flags (page disagrees with the spec expectation, or the basis is an inference)
1. sweet-pea: the spec expects support REQUIRED (replace with `row-trellis`). The crop's own OSU page plus NCSU, UC IPM and its own description say bush types need none, and only Cornell high-tunnel (commercial) says "must". Recommend keep plus add.
2. sweet-pea trellis in_row [3,6] is derived from "2 to 4 plants per foot", and `quote_states` would false-pass it on the row figure's "6".
3. peas: UMN's same-spacing rule extended to peas is an inference (PLA-532). Clemson's 1-2 in with 2 ft rows "regardless of row type" is a one-page alternative, but it carries a row figure that the kickoff null ruling did not anticipate.
4. cantaloupe: ISU's cultivar weights are mostly 4-9 lb, above the 3 lb rule. The crop qualifies only for small-fruited cultivars, and cultivar is not an entry axis.
5. UMD melons "trellis allows closer spacing" contradicts UMN "same spacing" for melons.
6. honeydew qualification is an inference (no crop-level weight; one 2 lb cultivar).
7. butternut and spaghetti are not named by UMN (only delicata and acorn), so qualifying them is an inference. Recommend none.
8. acorn: the [24,36] ground figure's low end is UMN's bush-type spacing, while the trellised vining form reads toward 36.
9. summer squash: UMD "non-vining bushes"; any trellis entry would have to use UMN's vining figure (8-12 in thinned), not canonical's [24,36].
10. VCE HORT-189 points at `cage` (not trellis) for melons and squash but states no spacing, so D7 blocks it.
11. strawberry bed: the meaning of `row_spacing_inches` (within-bed 12 vs between beds) is unruled, and the page is DOC-only.
12. Anomaly, not acted on: UMN growing-peas says "place the seeds in a shallow trench, six to seven inches apart". That disagrees with every other pea page (1-3 in) and with canonical.
