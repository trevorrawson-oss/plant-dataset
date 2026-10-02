# PLA-10 promote 2: support-entry measurement (agent A), READ-ONLY

Base: branch `main`, HEAD `78d734b`, canonical sha256 `cf1d480d...` == LATEST.txt. Nothing edited, nothing fetched.

Cache legend:
- **EV** = `tools/.evidence_cache/<sha256>.*` (hashed bytes; what promote 1's EVIDENCE.tsv quotes)
- **DC** = `tools/.doc_cache/<sha1(url)>.txt` (extracted text only; NOT in the hashed evidence cache. A promote that hashes evidence must first fetch it into `.evidence_cache`)

Quotes are verbatim from `norm_text` output, so they are lowercased and whitespace-collapsed. PDFs were read through `pla10_promote_common.pdf_text`.

## 0. Where the source pages sit (ids are the anchoring keys the crops already use)

| page | id | cache | cited by |
| -- | -- | -- | -- |
| ISU growing-tomatoes-home-garden | iastate_ext | **EV** 9e86cd2e...html | all 5 tomatoes + tomatillo |
| PSU heat-stress-and-tomatoes | psu_ext | **EV** 292915ad...html | cherry, grape, heirloom, roma (NOT beefsteak) |
| Missouri G6461 | mu_ext | **EV** ba5c341c...html | 5 tomatoes (+tomatillo via /publications/g6461) |
| UMN trellises-and-cages (PLA-532) | umn_ext_trellises_cages | **EV** 8ee29202...html | catalog |
| VCE HORT-189 (PLA-532) | vce_hort_189 | **EV** 9a7d9d6a...html | catalog |
| UNL G1650 | unl_ext | DC 6bf02baf...txt | 5 tomatoes (NOT tomatillo) |
| Cornell tomato growing guide | cornell_ext | DC 07447484...txt | 5 tomatoes + tomatillo |
| Illinois hortanswers PlantID=294 | uiuc_ext | DC 2c792554...txt | 5 tomatoes + tomatillo |
| UMD growing-tomatoes-home-garden | umd_ext | DC 4007b59c...txt | 5 tomatoes + tomatillo |
| OSU EC 1333 tomatoes & tomatillos | osu_ext | DC ab8d2531...txt | 5 tomatoes + tomatillo |
| USU tomatillos-in-the-garden | usu_ext | **EV** 506d9e77...html | tomatillo |
| UMN growing-tomatillos-and-ground-cherries | umn_ext | **EV** 0fa41a63...html | tomatillo |
| UCANR Alameda guide-growing-tomatillos | ucanr_ext | **EV** c65620a0...html | tomatillo |
| SDSU tomatillo-how-grow-it | (sdsu) | **EV** 02cd4615...html | tomatillo |
| Clemson HGIC cucumber | clemson_hgic | **EV** 9d1eaeb1...html | all 4 cucumbers |
| UMD growing-cucumbers-home-garden | umd_ext | **EV** da454800...html | all 4 cucumbers |
| UMN growing-cucumbers | umn_ext | **EV** 5645fa79...html | all 4 cucumbers |
| ISU growing-cucumbers | iastate_ext | **EV** cc412f7c...html | pickling |
| ACES greenhouse cucumber | aces_ext | DC ad9963c2...txt | english |
| UF/IFAS CV268 | uf_ifas | DC def8b05a...txt | english |

**The fork pages the kickoff names are mostly DC-only.** UNL, Cornell, Illinois, UMD tomato and OSU EC1333 are not in the hashed evidence cache. ISU and PSU are the only EV pages that give tomato support figures.

## 1. Kickoff fork claims (line 210), checked against the cached bytes

| kickoff claim | verdict |
| -- | -- |
| Cornell "12 to 24 in determinate; 14 to 20 in staked indeterminate; 24 to 36 in unstaked indeterminate" | **Says it** (DC). There is NO cage figure and NO row figure. The determinate figure names no support. |
| ISU staked 1.5-2 ft, caged 2-3 ft, sprawl 3-4 ft | **Says it** (EV). The staked figure is scoped "indeterminate cultivars that are staked". The cage sentence carries no habit qualifier. |
| UNL unstaked 3 ft rows 4-5; staked 18-24 rows 3 ft; caged 24-36 rows 4 ft | **Says it** (DC only) |
| Illinois dwarf 12, staked 15-24, trellised/ground 24-36 | **Says it** (DC). "trellised **or** ground bed" puts trellis and ground in one figure, so it is not a support fork between them. |
| UMD "18-36 in rows x 48-60 ... depends on ... whether staked or caged" | **Says it** (DC), but it gives no per-support figure, so it cannot back an entry. UMD's "space cages at least 4-feet apart" is an open bound. |
| **USU tomatillo "hills vs transplants 2 ft in rows 3 ft"** | **The page says it, but it is an ARRANGEMENT fork (hill vs row), NOT a support fork.** USU gives no stake or cage spacing (see §2.6). |
| Clemson cucumber non-trellised 8-10 in rows 5 ft; trellised 4-5 seeds/ft rows 3 ft, thin to 9-12 | **Says it** (EV) |
| UMN cucumber "3-4 ft trellis ... space garden rows more closely" | **Says it** (EV). It gives no number. The 3-4 ft is a TRELLIS height. |
| ACES "single-leader cordon 12-18 in within row, rows 5 ft" | **Slightly off** (DC). The single-row vertical cordon has "rows are 4-5 ft. apart on center" with plants 12-18 in. The 5 ft row figure belongs to the DOUBLE-row system, where plants are 18-24 in. |
| UMD cucumber "12 in x 48-72 in, or hills of 2-3" | **Says it** (EV). That is the general figure. Its trellis paragraph has a separate in-row figure (below). |

**Spec §1.4 error:** the spec calls cherry-tomato's `[24, 36]` "the caged figure". Promote 1 quoted it from PSU's "**indeterminate tomatoes without stakes**" sentence (EVIDENCE.tsv), so it is the UNSTAKED figure.

## 2. Per crop

Candidate figures used below:
- **ISU (EV):** "indeterminate cultivars that are staked can be planted 1.5-2 feet apart within rows. if grown in wire cages, space plants 2-3 feet apart. tomatoes allowed to sprawl over the ground should be spaced 3-4 feet apart. rows should be spaced 4-5 feet apart. determinate tomatoes can be planted 1.5-2 feet apart in rows 4 feet apart."
- **PSU (EV):** "recommended spacings for tomatoes are 18 to 24 inches between plants in a row and a minimum of 5-6 feet between rows for staked culture; 24 inches between plants in a row and a minimum of 4-5 feet between rows for determinate tomatoes without stakes; and 24 to 36 inches between plants in a row and a minimum of 5-6 feet between rows for indeterminate tomatoes without stakes."
- **UNL (DC):** "set unstaked plants 3 feet apart in rows 4 to 5 feet apart. if the plants will be staked, plant them 18 to 24 inches apart in rows 3 feet apart. caged tomatoes are best spaced 24 to 36 inches apart in rows 4 feet apart." No habit qualifier: "distance between plants depends on two things: cultivar (which influences plant size) and growing method."

**Row-figure conflict: PSU staked rows are "a minimum of 5-6 feet" while UNL staked rows are "3 feet".** That is a 2x disagreement on the same support, and a reviewer has to call it. The ISU "rows should be spaced 4-5 feet apart" sentence follows the sprawl sentence. Applying it to stake or cage is a reading call; promote 1 already used it for beefsteak's sprawl entry.

### 2.1 cherry-tomato (det_indet.type = indeterminate)
- **Current row-none:** in_row [24,36], rows [60,72], psu_ext (EV). Quote: "24 to 36 inches between plants in a row and a minimum of 5-6 feet between rows for indeterminate tomatoes without stakes". The scope matches (unstaked indeterminate). **row-none stays.**
- **row-stake:** PSU (EV) gives [18,24] with rows [60,72] ("for staked culture"), from one sentence. Corroborated by ISU [18,24] ("indeterminate cultivars that are staked"), UNL [18,24] rows [36,36] (DC), and Cornell 14-20 (DC). Scope OK.
- **row-cage:** ISU (EV) gives [24,36] ("if grown in wire cages, space plants 2-3 feet apart"), with rows [48,60] only by the ISU reading call. UNL (DC) gives [24,36] rows [48,48]. No other EV cage figure.
- **Height override:** none on EV. OSU EC1333 (DC) says "indeterminate plants ... can easily grow 7 to 8 feet high. for these, it is best to stake each individual plant ... space the plants 12 to 18 inches apart." That is the habit height, stated in the staking paragraph. It would be a row-stake [7,8] candidate only after an evidence fetch and a ruling that it is support-tied. Cornell's "staked and pruned plants can grow to well over 6 feet tall" and Illinois's "at least 6 feet" are open bounds and cannot fill [lo,hi]. HORT-189's "eight-foot tall stakes are better for indeterminate types" is a STAKE height, not a plant height.
- **Recommended default: row-cage.** The crop's own prose says it "need[s] strong staking or caging", so a row-none default contradicts it. Staked spacing presumes pruning to 1-3 stems: UMD "prune staked tomatoes to one to three main stems (plant spacing can be reduced in these situations)"; EC1333 "staked plants are usually grown on a single or double stem". Cage needs no pruning (UMD "freedom from pruning and staking"), so it is the safer unqualified hero.
  - **Hero:** [24,36] -> [24,36], **no change**.
  - **Row mirror:** [60,72] -> [48,60] (ISU) or [48,48] (UNL, after fetch).
  - If row-stake is the default instead: hero [24,36] -> **[18,24]**, rows stay [60,72] (PSU).

### 2.2 grape-tomato (indeterminate)
Same pages and figures as cherry. Current row-none: [24,36] / [60,72], psu_ext, same unstaked-indeterminate sentence; it stays. Same candidates for row-stake (PSU [18,24]/[60,72]) and row-cage (ISU [24,36]). Same height situation.
- **Default: row-cage.**
- **Hero:** [24,36] -> [24,36], no change. Row mirror [60,72] -> [48,60].

### 2.3 beefsteak-tomato (indeterminate)
- **Current row-none:** [36,48] / [48,60], iastate_ext (EV). Quotes: "tomatoes allowed to sprawl over the ground should be spaced 3-4 feet apart." and "rows should be spaced 4-5 feet apart." Scope matches; it stays.
- **Beefsteak does NOT cite PSU**, so row-stake must use ISU [18,24] (EV) with rows [48,60] (ISU reading call), or UNL [18,24]/[36,36] (DC).
- **row-cage:** ISU [24,36] (EV).
- **Height:** as cherry.
- **Default: row-cage.** Hero [36,48] -> **[24,36]**; rows [48,60] unchanged under ISU. Under a stake default the hero becomes [18,24].

### 2.4 heirloom-tomato (indeterminate)
- **Current row-none:** [24,36] / [48,60], mu_ext (EV). Quotes: "ideal spacing for home garden tomatoes is generally 24 to 36 inches between plants." and "rows should be 4 to 5 feet apart."
- **Scope flag:** Missouri's figure names no support, and the page goes straight on to "proper spacing and staking are essential". Labelling it `support: none` is a reading, not a page statement. PSU's unstaked-indeterminate [24,36]/[60,72] (EV, heirloom cites PSU) is the explicit row-none statement; switching would be a re-author.
- **row-stake:** PSU [18,24]/[60,72] (EV).
- **row-cage:** ISU [24,36] (EV).
- **Default: row-cage.** Hero [24,36] -> [24,36], no change; rows [48,60] -> [48,60] (ISU), no change.

### 2.5 roma-tomato (det_indet.type = **determinate**)
- **Current row-none:** [18,24] / [48,48], iastate_ext. Quote: "determinate tomatoes can be planted 1.5-2 feet apart in rows 4 feet apart." The page states no support; it is in scope for a determinate crop.
  - The explicit unsupported-determinate statement is PSU (EV, roma cites it): "24 inches between plants in a row and a minimum of 4-5 feet between rows for determinate tomatoes without stakes" (i.e. [24,24] / [48,60]). It disagrees with the current entry's in_row, but changing it would be a re-author.
- **row-stake is OUT OF SCOPE on EV pages.** ISU's staked figure is "indeterminate cultivars that are staked", and Cornell's is "staked indeterminate". The only generic staked figures are UNL [18,24]/[36,36] (DC) and Illinois 15-24 (DC). Roma's own prose says "give it a sturdy cage instead of a tall stake".
  - **Recommend no row-stake on roma.**
- **row-cage:** ISU [24,36] (EV). The scope is ambiguous: the sentence follows an indeterminate-scoped sentence and has no habit word of its own. UNL [24,36]/[48,48] (DC) is generic.
  - The PLA-532 UMN trellises page names roma for cages but gives no figure: "determinate varieties such as 'roma,' which reach a certain size and stop growing, can get enough support from these cages."
- **Height:** EC1333 (DC) has determinate "up to about 4 feet tall" (open bound) and "fairly short (3 to 4 feet tall)" (crop-level). Illinois (DC) has "most modern determinate tomatoes easily grow 3 to 4 feet tall". These are crop-level `mature_height_ft` candidates, NOT a support override.
- **Recommended default: row-none stays default.** It is the only in-scope determinate figure, and a cage does not change a determinate's footprint on any cached page. Hero [18,24] unchanged. If row-cage is made default: [18,24] -> [24,36].

### 2.6 tomatillo (det_indet.type = indeterminate): **NO support fork on any cached cited page**
- **Current row-none:** [24,24] / [36,36], usu_ext (EV). Quote: "transplants should be planted 2 feet apart in rows spaced 3 feet apart." The same page says "keep plants supported with stakes or cages to alleviate a spreading plant", so `none` is a label the page does not state.
- **In-scope tomatillo pages: what each says.**
  - **USU (EV)** gives an arrangement fork only: "plant four to six seeds 1⁄2-inch deep in hills, 24-36 inches apart with rows spaced 36 inches apart. after seedlings have two leaves, thin to one to two plants per hill."
    - That is a `hill-none` candidate (hill [24,36], rows [36,36], plants_per_hill [1,2]), outside promote 2's support scope.
    - Its stake line is a build spec: "drive a 48-inch stake 18 inches into the soil".
  - **UCANR Alameda (EV)** gives one figure for "cage or stake" jointly, no row: "space plants about two feet apart and provide support such as a cage or stake, as tomatillo plants can grow up to four feet tall."
  - **SDSU (EV):** "tomatillos have a bushy habit and should be transplanted with 3 feet between plants ... plan to trellis, cage, or otherwise support each plant." No support is distinguished.
  - **UMN (EV):** "tomatillos need more space, as much as three feet ... plan to trellis, cage or otherwise support tomatillo plants." This is an open bound.
  - **OSU EC1333 (DC):** "they can sprawl without any support, but it's best to stake or cage them". No figure.
  - **TAMU (EV):** "space plants about 18 inches apart in rows 3 feet apart". No support stated.
- **Out of scope:** ISU, Cornell, Illinois, UMD and EC1333's tomato sections are TOMATO figures on a tomatillo record (crop-scope-is-not-its-slug). Hawaii b-91 (DC, cited by tomatillo) has "plants for staking can be spaced 18 to 24 inches in the row; unstaked plants should be 3 or 4 feet apart". That sits in the large-fruited TOMATO section, so it is out of scope.
- **Heights:** these are crop-level, not overrides:
  - USU (EV): "tomatillos grow 3-4 feet tall and wide"
  - EC1333 (DC): "they grow 2 to 4 feet tall"
  - UCANR (EV): "up to four feet tall", an open bound
  - TAMU (EV): "plants grow to a height of 3 to feet", a **broken source string with a number missing**
- **Recommendation:** author **0** support entries. row-none stays default; hero unchanged [24,24].
  - Alternative (decision row): two entries, row-stake and row-cage, both [24,24] with rows null/`not_authored`, from UCANR's single "cage or stake" sentence. That would be one figure duplicated across two ids.
- **Separate data defect (surfaced, not fixed):** tomatillo's `det_indet.detail_beginner` is a verbatim clone of cherry-tomato's. It talks about "cherry tomato varieties" and "Tumbling Tom", and is anchored to Clemson's cherry-tomato blog. `detail_seasoned` also begins "Cherry tomatoes are almost always indeterminate".

### 2.7 slicing-cucumber
- **Current row-none:** [24,24] / [48,48], osu_ext (EV PDF). Quote: "Cucumbers (slicing) ... 6 plants 48" 24"". It stays.
- **row-trellis:** clemson_hgic (EV). Quote: "if cucumbers are trellised, plant four to five seeds per foot in rows spaced 3 feet apart. when plants are 4 to 5 inches high, thin so they are 9 to 12 inches apart." That gives in_row [9,12], rows [36,36].
  - The thin-to sentence sits between the trellised sentence and the restated "if non-trellised, space cucumber plants 8 to 10 inches apart in rows that are 5 feet apart", so it belongs to the trellised case.
  - Corroborated by umd_ext (EV): "plant four to five seeds per foot, thinning to a 9- to 12-inch spacing when plants are 4- to 5-inches high" (trellising paragraph, no row figure).
  - Scope: a generic cucumber page that names slicers.
- **Height:** none. Clemson's "a satisfactory trellis is one that is about 6 feet high" and UMN's "three- to four-foot trellis" are TRELLIS heights.
- **Default: row-none stays.** Every page presents the trellis as optional ("you may also train", "can be successfully grown on trellis systems"). Hero [24,24] unchanged. With a trellis default it would be [24,24] -> [9,12], rows [48,48] -> [36,36].

### 2.8 pickling-cucumber
- **Current row-none:** [6,12] / [48,48], osu_ext (EV PDF), "Cucumbers (pickling) ... 48" 6-12"". It stays.
- **row-trellis:** Clemson [9,12]/[36,36] (EV), same quote. The page covers picklers (17 "pickl" mentions). ISU cucumber (EV) says only "cucumbers can be successfully grown on trellis systems" with no figure.
- **Height:** none.
- **Default: row-none.** Hero [6,12] unchanged.

### 2.9 english-cucumber
- **Current row-none:** [12,18] / [48,72], vce_426_331 (EV), table row "cucumbers 12-18 in 48-72 in". It stays.
- **row-trellis:** Clemson [9,12]/[36,36] (EV). In scope: Clemson names "hybrid, burpless or european-type cucumbers".
  - The greenhouse figures are DC-only and COMMERCIAL greenhouse scope:
    - ACES: "within the row, plants are spaced 12 to 18 inches"; "rows are 4-5 ft. apart on center"
    - UF CV268: "single, evenly spaced rows in a vertical cordon system would be approximately 4 to 5 feet between rows and 12 to 18 inches between plants within the row"
  - Those would be a `row-trellis-cordon`-style qualifier entry at most. Not recommended for a home-garden hero.
- **Height:** none. ACES's "trellises with heights over 12 feet" / "6 to 8 feet" are trellis heights.
- **Recommended default: row-trellis.** The crop's own prose says "train the plants up a string or trellis to keep the long fruit straight" / "grow them up a string or trellis so the long cucumbers hang straight". Hero [12,18] -> **[9,12]**; row mirror [48,72] -> **[36,36]**. This is a decision row; keeping row-none leaves the hero unchanged.

### 2.10 cucumber (generic)
- **Current row-none:** [12,18] / [48,72], vce_426_331 (EV). It stays.
- **row-trellis:** Clemson [9,12]/[36,36] (EV), UMD corroborating.
- **Height:** none.
- **Default: row-none.** Hero unchanged [12,18].

**PLA-532 cucumber note:** the umn_ext_trellises_cages page (EV) says "plant the vines at the foot of the trellis at the same spacing between the seeds or transplants as if they were going to grow on the ground". Read literally, the trellis in-row equals the ground in-row. Clemson's 9-12 vs 8-10 fits that; OSU slicing's 24 vs 9-12 does not. vce_hort_189 (EV) states **no plant spacing for any crop**. Its only figures are stake/twine build specs, e.g. "six-foot stakes driven two feet deep are sufficiently tall for determinate tomato types. eight-foot tall stakes are better for indeterminate types." Neither PLA-532 page supplies a number for any entry.

## 3. Entry count

| crop | new entries |
| -- | -- |
| cherry, grape, beefsteak, heirloom | row-stake + row-cage = 2 each = **8** |
| roma | row-cage = **1** (row-stake not recommended: no in-scope EV figure) |
| tomatillo | **0** (or 2 under the UCANR "cage or stake" option) |
| 4 cucumbers | row-trellis = **4** |
| **total recommended** | **13** (max 16 if roma-stake and the two tomatillo entries are ruled in; spec §10.2 implied 6x2 + 4 = 16) |

All 10 promote-1 `row-none` entries stay, with ids pinned. Height overrides recommended: **0**. The only closed candidate is EC1333 [7,8] (DC-only, habit height). Default flips that move the hero: beefsteak [36,48] -> [24,36] and english-cucumber [12,18] -> [9,12]. Under a stake default instead of cage, cherry, grape, heirloom and beefsteak would move to [18,24].

## 4. Flags
1. The tomatillo support fork the spec and kickoff expect is not on any cached page. USU's fork is hill vs row.
2. Roma has no in-scope staked figure on EV pages.
3. Staked row spacing: PSU (min 5-6 ft) vs UNL (3 ft) disagree.
4. UNL, Cornell, Illinois, UMD and EC1333 are DC-only. A hashed-evidence promote needs them fetched before use. ISU and PSU alone cover the stake and cage entries on EV, except row figures for cage (ISU generic reading).
5. Spec §1.4 misnames cherry's [24,36] "the caged figure"; it is PSU's unstaked figure.
6. heirloom's row-none (Missouri) names no support.
7. Tomatillo `det_indet` is cloned from cherry-tomato.
8. TAMU tomatillo height string "3 to feet" is broken at source.
