# broad-beans-fava -- Phase C evidence packet (item 3)

Canonical read: sha256 b331e5f2..., HEAD 1250f3a (main). Quotes in `norm_text` form; sha256 re-verified.

## Hashed pages cited on broad-beans-fava
| source | url | sha256 |
|---|---|---|
| UC MG Santa Clara (SCC) | https://ucanr.edu/site/uc-master-gardeners-santa-clara-county/fava-beans | cc3bfa365696e2fd59d18f5b27a7711d3221905d7301366b9ee4db59733282f3 |
| NCSU Plant Toolbox | https://plants.ces.ncsu.edu/plants/vicia-faba/ | 225a0f5e032acf36224fef31fb7f51f9c2c8374e182070df54002b4930ff0260 |
| UMN growing beans | https://extension.umn.edu/vegetables/growing-beans | d5fed4deeabd1ddf240422f585eb79df4ffbc13a2973996f1c8ce05b8a5e9ad9 |
| UF/IFAS VH021 | https://edis.ifas.ufl.edu/publication/VH021 | 7ff585e6999b66923a3422589b068032cd5ed6f3463bbe43f60a5325ed179994 (no fava/broad bean sentence found) |

Cited, NOT hashed: agrilifeextension.tamu.edu (+ Fall-Vegetable-Gardening-Guide.pdf); agsci-labs.oregonstate.edu pea-leaf-weevil; content.ces.ncsu.edu; donaanamastergardeners.nmsu.edu; extension.arizona.edu; extension.msstate.edu; extension.umaine.edu; extension.unh.edu; extension.usu.edu (frost pdf, yardandgarden, planting dates); fieldreport.caes.uga.edu C943; hgic.clemson.edu; ipm.ucanr.edu (celery black-bean-aphid; dry-beans seedcorn-maggot); marinmg.ucanr.edu; mg.ucanr.edu; naes.agnt.unr.edu 2002-3280; nevegetable.org bean; ucanr.edu time-planting; ucanr.edu San Diego MG; canr.msu.edu/resources; ctahr.hawaii.edu B-91.pdf; rhs.org.uk (chocolate spot, rust, downy mildews); uaex.uada.edu; unlv.edu; yardandgarden.extension.iastate.edu.

## Authored fields (context)
- `spacing_inches` [8,10]; `thin_to_inches` [8,10]; `sow_depth_inches` [1,2]; `row_spacing_inches` null, `row_spacing_reason` "not_authored".
- `planting_layout[0]` row-none: in_row [8,10], row_spacing null / "not_authored", sources ["ucanr_santa_clara_mg"] -> SCC url (verified 2026-10-01).
- EVIDENCE (pla10_promote1): `broad-beans-fava row-none in_row_inches [8,10] ucanr_santa_clara_mg ... cc3bfa36... "Thin to 8 to 10 inches apart."`; (pla10_promote3): `mature_height_ft [2,6] ncsu_ext_toolbox_vicia_faba ... 225a0f5e... "it is a stiffly erect plant that grows 2-6 feet tall"`.

## Leaf: `start_method.notes_seasoned`
CURRENT (verbatim):
> Direct-sow the large flat seed about 1 to 2 inches deep and 4 to 6 inches apart, thinning to stand 8 to 10 inches apart, in rows 18 to 30 inches apart. In mild-winter regions sow in fall (roughly October to November) to overwinter; in cold regions sow as early as the soil can be worked in late winter or early spring. Germination is slow in cool soil and can take up to three weeks; there is no benefit to starting favas indoors.

| # | claim | verdict | quote |
|---|---|---|---|
| 1 | direct-sow | MAPPED | SCC: "fava beans , uc anr small farms network planting for producing pods to eat, direct seed 3 to 5 inches apart in february or in august to september, possibly into october depending on your microclimate." |
| 2 | the seed is large | MAPPED | SCC: "the large-seeded varieties are generally the ones planted for eating."; NCSU: "major (broad beans) has large seeds, and is grown as a vegetable for human consumption." |
| 3 | the seed is flat | MAPPED (as "compressed") | NCSU: "the seeds are .5 to 1 inch in diameter and are oval and compressed." |
| 4 | sow about 1 to 2 inches deep | NO HASHED CITED PAGE STATES IT for fava (UMN's depth sentence is in its common-bean "starting seeds" section) | UMN (context, not fava-specific): "plant seeds about an inch deep, or according to package directions." |
| 5 | seed spacing 4 to 6 inches apart | **NOT RESOLVED HERE -- routed to PLA-625.** The hashed page states 3 to 5 | SCC: "...direct seed 3 to 5 inches apart in february or in august to september, possibly into october depending on your microclimate." |
| 6 | thin to stand 8 to 10 inches apart | MAPPED | SCC: "thin to 8 to 10 inches apart." |
| 7 | **rows 18 to 30 inches apart** | **RULED CUT.** NO HASHED CITED PAGE STATES IT (no row figure for fava on any hashed cited page; UMN's "rows two to three feet apart" is its bush-bean sentence) | UMN (context, bush beans): "sow bush bean seed in single or double rows, with seeds four inches apart and rows two to three feet apart." |
| 8 | mild-winter regions: sow in fall | MAPPED (SCC, a mild-winter county) | SCC: "...direct seed 3 to 5 inches apart in february or in august to september, possibly into october depending on your microclimate." / "fall-planted beans typically begin producing in early spring." |
| 9 | fall = roughly October to November | NOT STATED as given: SCC says "august to september, possibly into october"; no hashed page says November | SCC (as #8) |
| 10 | (fall sowing) overwinters | PARTIAL: implied by SCC "fall-planted beans typically begin producing in early spring."; "overwinter" not stated | -- |
| 11 | cold regions: sow as early as the soil can be worked | "early in the spring" MAPPED; "as soon as the soil can be worked" NOT STATED | UMN: "grow as you would peas, planting early in the spring."; UMN: "fava beans fava beans ( vicia faba ), unlike other beans, require conditions similar to those needed to grow peas: cool temperatures with highs only into the low eighties." |
| 12 | in late winter or early spring | "early spring" MAPPED (UMN above); SCC "february" (late winter, Santa Clara); "late winter" for cold regions NOT STATED | SCC (as #1) |
| 13 | germination is slow in cool soil | NO HASHED CITED PAGE STATES IT | (VH021 "they are slow to germinate." is the CARROTS row) |
| 14 | can take up to three weeks | NO HASHED CITED PAGE STATES IT | -- |
| 15 | no benefit to starting indoors | NO HASHED CITED PAGE STATES IT | -- |

Context sentence (cool-season): SCC: "fava beans (vicia faba) , sometimes called broad beans, grow well as a cool season crop in santa clara county." / "(most other beans require warm weather.)"; NCSU: "this cool season crop can be grown in most climates, however, temperatures in the 60's are ideal."

## Does any other fava leaf state rows 18-30?
**No.** Every string leaf on broad-beans-fava was searched for "18 to 30", "18-30", "rows" + a figure, and "apart". Only `start_method.notes_seasoned` states rows 18-30. Other leaves carrying the 1-2 in depth / 4-6 in seed-spacing claims (no row figure): `start_method.notes_beginner`, `growth_stages[0].user_action_seasoned`, `growth_stages[0].user_action_beginner`, `notifications[0].body_seasoned`, `notifications[0].body_beginner` (these carry the PLA-625 "4 to 6" figure too).
