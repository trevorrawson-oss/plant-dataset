# sweet-corn -- Phase C evidence packet (item 2, thinning)

Canonical read: sha256 b331e5f2..., HEAD 1250f3a (main). Quotes in `norm_text` form; sha256 of every hashed file re-verified.

## Hashed pages cited on sweet-corn
| source | url | sha256 |
|---|---|---|
| Iowa State (ISU) | https://yardandgarden.extension.iastate.edu/how-to/growing-sweet-corn-home-garden | a2bf16710e4692f4f9faf42e6882987d21928cc8d919727cc0eef85d4b22f20c |
| UMN | https://extension.umn.edu/vegetables/growing-sweet-corn | f62601afa164ba6a46dd6bd70d710c7c216623e9f4ec03f087299ebdeff08d8e |
| UF/IFAS VH021 | https://edis.ifas.ufl.edu/publication/VH021 | 7ff585e6999b66923a3422589b068032cd5ed6f3463bbe43f60a5325ed179994 |
| OSU chart | https://ir.library.oregonstate.edu/downloads/v979v342w | f2fdb1d636d2952473094c5ea64a4bd978fe90201fc4b5f897f2c39cfc685a33 |
| NMSU CR457B | https://pubs.nmsu.edu/_circulars/CR457B/ | cb59fcd17e7af0bfdd794f22f688f9c44065caf1a8f833b0415a78d86053655c |
| WSU | https://s3.wp.wsu.edu/uploads/sites/2073/2014/09/Home-Vegetable-Gardening-in-Washington.pdf | 7378f653496200a6f260be82f4276a5834d196de2bdc4e7e17d0a720a48c3c34 |
| UGA B577 | https://secure.caes.uga.edu/extension/publications/files/html/B577/B577PlantingChart.pdf | a9ed2655a399e13603b46207f907ae0a82051fc04d118f4eb5e619244130438e |
| VT 426-331 | https://www.pubs.ext.vt.edu/426/426-331/426-331.html | 52fda56c97eca81aa63955bcc5d4dfdf8dbac4c29921a82eb35f154c0cd85720 |

**TAMU EHT-044** https://aggie-horticulture.tamu.edu/wp-content/uploads/sites/10/2013/09/EHT-044.pdf is cited (thinning.anchoring_urls.tamu_agrilife) but **NOT hashed**. Its sentences below are quoted from the scratch copy `scratchpad/a5/fetch/33d034570ec5028d64dc68f6430871f3ee71b10a757c247bf24f5ec78ad68baf.pdf` (sha256 re-verified = 33d034570ec5028d64dc68f6430871f3ee71b10a757c247bf24f5ec78ad68baf), text via `norm_text(pdf_text(raw))`, each marked **[TO BE HASHED IN PHASE C (scratch copy sha 33d03457...)]**.

Other cited, NOT hashed: cameron.agrilife.org RGV guide 2022; content.ces.ncsu.edu/organic-sweet-corn-production; crops.extension.iastate.edu imbibitional chilling; cropwatch.unl.edu heat/pollination; cvp.cce.cornell.edu crop 34; extension.arizona.edu az1005-2018; extension.msstate.edu corn-sweet; extension.umn.edu dry-conditions-during-corn-pollination; extension.usu.edu planting dates; extensionpubs.unl.edu g1850; naes.agnt.unr.edu 2002-3280; ucanr.edu time-planting; ctahr.hawaii.edu corn2003.pdf; uaex.uada.edu (fall, spring-summer); unlv.edu calendar; yardandgarden.extension.iastate.edu/faq (types; when-to-harvest).

## Authored fields (context)
- `thin_to_inches` = [8, 12] (ruling: becomes [12, 12]). No anchoring on the field itself; `verification_status.field_additions[0].note` says "thin_to [8,12]".
- `spacing_inches` = [8, 12]; `row_spacing_inches` = [30, 36]; `planting_layout[0]` (block-none) in_row [8,12], rows [30,36], sources ["iastate_ext"] -> ISU url (verified 2026-10-01).
- EVIDENCE.tsv (pla10_promote1): `sweet-corn block-none in_row_inches [8,12] iastate_ext ... a2bf1671... "Space seeds 8 to 12 inches apart in rows 2½ to 3 feet apart."` and the same quote for `row_spacing_inches [30,36]`. No pla10_promote2/3 rows for sweet-corn.
- `thinning.sources` = ["tamu_agrilife"]; `thinning.anchoring_urls.tamu_agrilife` = EHT-044 url, verified "2026-07-10". `thinning.needs_thinning` = true.

## Thinning / in-row sentences on the pages
- **EHT-044 [TO BE HASHED IN PHASE C (scratch copy sha 33d03457...)]**: "plant the corn seeds about 1 inch deep and 3 to 4 inches apart in the row." / "space the rows 21⁄2 to 3 feet apart." / "after the plants are up, thin them to 1 foot apart." / "if you plant them closer, your corn will have small, poorly-filled ears (figs. 1 and 2.)"
- EHT-044 [TO BE HASHED]: "hoe or till the soil just under the sur- face." / "hoe the weeds off just below the soil's surface." / "deep hoeing will cut the corn roots, which are close to the top of the soil." / "water sweet corn as needed to keep it from wilting."
- ISU a2bf1671: "plant sweet corn seeds 8 to 12 inches apart in rows 21⁄2 to 3 feet apart." / "space seeds 8 to 12 inches apart in rows 21⁄2 to 3 feet apart." / "sweet corn may also be planted in \"hills.\" sow 4 to 5 seeds per hill with approximately 3 inches between seeds." / "hills should be spaced 21⁄2 feet apart with 21⁄2 to 3 feet between rows." / "plant sweet corn in blocks of four or more short rows to promote pollination."
- UMN f62601af: "plant seeds one inch deep, and eight to 12 inches apart, with rows 30 to 36 inches apart." / "always plant corn in blocks of at least four rows." / "sweet corn has a shallow rooting depth." / "controlling weeds frequent, shallow cultivation with a hoe or other tool will kill weeds before they become a problem." / "hoe just deeply enough to cut the weeds off below the surface of the soil." / "be careful not to damage the plants when cultivating." / "once the corn plants have established, they will form a canopy of leaves that can discourage new weeds from growing." / "they will absorb up to twice as much water as other types before they germinate, so keep the seedbed moist until the shoots emerge."
- WSU 7378f653 (general, cited on the crop; runs AGAINST thinning corn): "plant large seeds such as beans, corn, and squash at the recommended row spacing to avoid having to thin the stand later." / "it is difficult to sow small seeds thinly enough, so the stand will usually have to be thinned to the recommended row spacing after the seeds have germinated."
- VH021 7ff585e6: "thin seedlings to recommended spacing when they are an inch tall." -- **this sentence is in the CARROTS row of VH021, not corn**; corn row: "requires space; plant in blocks of at least 3 rows for good pollination."
- No hashed cited page (and not EHT-044) states "3 to 4 inches tall", "a few inches tall", "snip", "soil line", or "rather than pulling".

## Leaf: `thinning.when`
CURRENT: `when seedlings are 3 to 4 inches tall`
| claim | verdict | quote |
|---|---|---|
| thin when seedlings are 3 to 4 inches tall | NO HASHED CITED PAGE STATES IT (ruled cut). EHT-044 timing is only "after the plants are up" | EHT-044 [TO BE HASHED]: "after the plants are up, thin them to 1 foot apart." |

## Leaf: `thinning.to_spacing`
CURRENT: `8 to 12 inches`
| claim | verdict | quote |
|---|---|---|
| thin to 8 to 12 inches | NOT the thinning figure on the anchoring page; EHT-044 says 1 foot. 8-12 in is ISU/UMN SEED spacing (ruled: ISU/UMN stay cited for in-row only) | EHT-044 [TO BE HASHED]: "after the plants are up, thin them to 1 foot apart."; ISU: "space seeds 8 to 12 inches apart in rows 21⁄2 to 3 feet apart."; UMN: "plant seeds one inch deep, and eight to 12 inches apart, with rows 30 to 36 inches apart." |

## Leaf: `thinning.method`
CURRENT: `snip extra seedlings at the soil line`
| claim | verdict |
|---|---|
| snip extras at the soil line | NO HASHED CITED PAGE STATES IT (not in EHT-044 either) |

## Leaf: `thinning.tip_seasoned`
CURRENT:
> If you sow thickly to insure a stand, thin within the block to a final in-row spacing of 8 to 12 inches once seedlings are a few inches tall. Snip the extras at the soil line rather than pulling, to spare the shallow roots of the plants you keep.

| # | claim | verdict | quote |
|---|---|---|---|
| 1 | sowing thickly (to insure a stand) is the case that needs thinning | PARTIAL: EHT-044 sows 3-4 in apart then thins (no "insure a stand" rationale stated); WSU says plant corn at final spacing to avoid thinning | EHT-044 [TO BE HASHED]: "plant the corn seeds about 1 inch deep and 3 to 4 inches apart in the row." + "after the plants are up, thin them to 1 foot apart."; WSU: "plant large seeds such as beans, corn, and squash at the recommended row spacing to avoid having to thin the stand later." |
| 2 | "insure a stand" rationale | NO HASHED CITED PAGE STATES IT | -- |
| 3 | thin within the block | "block" MAPPED (planting in blocks); thinning within a block not stated as such | UMN: "always plant corn in blocks of at least four rows."; ISU: "plant sweet corn in blocks of four or more short rows to promote pollination." |
| 4 | final in-row spacing 8 to 12 inches | EHT-044 thin-to figure is 1 foot; 8-12 is ISU/UMN seed spacing | as in to_spacing above |
| 5 | once seedlings are a few inches tall | NO HASHED CITED PAGE STATES IT | EHT-044 [TO BE HASHED] only: "after the plants are up" |
| 6 | snip at the soil line rather than pulling | NO HASHED CITED PAGE STATES IT | -- |
| 7 | corn roots are shallow | MAPPED | UMN: "sweet corn has a shallow rooting depth."; EHT-044 [TO BE HASHED]: "deep hoeing will cut the corn roots, which are close to the top of the soil." |
| 8 | snipping spares the kept plants' roots (causal link) | NO HASHED CITED PAGE STATES IT | -- |

## Leaf: `thinning.tip_beginner`
CURRENT:
> If you plant the seeds close together to be sure they come up, thin them to about 8 to 12 inches apart within the block when they are a few inches tall. Cut the extra seedlings off at the ground instead of pulling them, so you do not disturb the roots of the ones you are keeping.

| # | claim | verdict |
|---|---|---|
| 1 | plant close together "to be sure they come up" | same as seasoned #1-#2: close sowing MAPPED to EHT-044 [TO BE HASHED] "3 to 4 inches apart in the row"; the "to be sure they come up" rationale NOT STATED |
| 2 | thin to about 8 to 12 inches apart | EHT-044 [TO BE HASHED]: "after the plants are up, thin them to 1 foot apart." (8-12 is seed spacing on ISU/UMN) |
| 3 | within the block | as seasoned #3 |
| 4 | when they are a few inches tall | NO HASHED CITED PAGE STATES IT |
| 5 | cut off at the ground instead of pulling | NO HASHED CITED PAGE STATES IT |
| 6 | so you do not disturb roots of kept plants | NO HASHED CITED PAGE STATES IT (shallow roots themselves MAPPED, UMN/EHT-044 as above) |

## Leaf: `thinning.sources` / `thinning.anchoring_urls`
CURRENT: sources ["tamu_agrilife"]; anchoring_urls.tamu_agrilife.url = EHT-044, verified "2026-07-10". Per ruling EHT-044 is hashed in Phase C; ISU/UMN are cited on the crop (planting_layout) for in-row only. No claim in the thinning block is supported by ISU/UMN except the shallow-root and block facts above.

## Leaf: `thin_to_inches`
CURRENT [8, 12]. Ruled -> [12, 12]. Support: EHT-044 [TO BE HASHED]: "after the plants are up, thin them to 1 foot apart." No hashed cited page states a thin-to of 8-12 in.

## Leaf: `growth_stages[1].user_action_seasoned`
CURRENT:
> Keep the block evenly moist and weed-free; young corn competes poorly with weeds. Cultivate shallowly to spare the surface roots. Thin now to a final 8 to 12 inches in the row if you sowed thickly.

| # | claim | verdict | quote |
|---|---|---|---|
| 1 | keep the block evenly moist (seedling stage) | NO HASHED CITED PAGE STATES IT for the seedling stage (UMN's moisture sentence is pre-emergence; EHT-044's is "keep it from wilting") | UMN: "...so keep the seedbed moist until the shoots emerge."; EHT-044 [TO BE HASHED]: "water sweet corn as needed to keep it from wilting." |
| 2 | keep it weed-free | MAPPED (weed control) | UMN: "controlling weeds frequent, shallow cultivation with a hoe or other tool will kill weeds before they become a problem." |
| 3 | young corn competes poorly with weeds | NO HASHED CITED PAGE STATES IT (UMN only says established corn's canopy discourages weeds) | UMN: "once the corn plants have established, they will form a canopy of leaves that can discourage new weeds from growing." |
| 4 | cultivate shallowly to spare surface roots | MAPPED | EHT-044 [TO BE HASHED]: "hoe or till the soil just under the sur- face." / "deep hoeing will cut the corn roots, which are close to the top of the soil."; UMN: "sweet corn has a shallow rooting depth." / "hoe just deeply enough to cut the weeds off below the surface of the soil." / "be careful not to damage the plants when cultivating." |
| 5 | thin now (seedling stage) | EHT-044 [TO BE HASHED] "after the plants are up" (no stage beyond that) | -- |
| 6 | to a final 8 to 12 inches in the row | EHT-044 [TO BE HASHED] says 1 foot (8-12 = ISU/UMN seed spacing) | as above |
| 7 | if you sowed thickly | see thinning tip_seasoned #1 | -- |

## Leaf: `growth_stages[1].user_action_beginner`
CURRENT:
> Keep the soil evenly moist and pull weeds early, since small corn does not compete well with them. Weed shallowly to protect the roots near the surface. If you planted thickly, thin to about 8 to 12 inches apart now.

| # | claim | verdict |
|---|---|---|
| 1 | keep soil evenly moist | as seasoned #1 (NOT STATED for this stage) |
| 2 | pull weeds early | MAPPED (UMN "will kill weeds before they become a problem"); "pull" (hand-pulling) is not what UMN/EHT-044 say -- they say hoe |
| 3 | small corn does not compete well with weeds | NO HASHED CITED PAGE STATES IT |
| 4 | weed shallowly to protect roots near the surface | MAPPED (EHT-044 [TO BE HASHED], UMN, as seasoned #4) |
| 5 | if planted thickly, thin to about 8 to 12 inches now | EHT-044 [TO BE HASHED]: "after the plants are up, thin them to 1 foot apart." |

Also on this stage (not named in the item, untouched unless Trevor rules): `log_prompt_seasoned` "...Note any gaps, thinning you did..." and `log_prompt_beginner` "...Note any bare patches, thinning..." mention thinning without a figure.

## Other sweet-corn leaves carrying the 8-12 thin figure
Only those above (`thinning.*`, `thin_to_inches`, `growth_stages[1].user_action_*`) plus `verification_status.field_additions[0].note` ("thin_to [8,12]", an append-only record).
