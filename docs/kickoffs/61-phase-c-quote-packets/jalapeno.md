# jalapeno -- Phase C evidence packet (item 8, plain spacing conflict)

Canonical read: sha256 b331e5f2..., HEAD 1250f3a (main). Quotes in `norm_text` form; sha256 re-verified.

## Hashed pages cited on jalapeno
| source | url | sha256 |
|---|---|---|
| OSU planting chart | https://ir.library.oregonstate.edu/downloads/v979v342w | f2fdb1d636d2952473094c5ea64a4bd978fe90201fc4b5f897f2c39cfc685a33 |
| ISU peppers | https://yardandgarden.extension.iastate.edu/how-to/growing-peppers-home-garden | 2ac60d9db000b01b642f9708d92ac558cb563977bd615236afa95ce69cb1bb2e |
| UMN peppers | https://extension.umn.edu/vegetables/growing-peppers | 63c34d25065b048a01c6d94658a1f1a588be3c96bd1bfc8a7b335ddd5ad59a18 |
| UMD peppers | https://extension.umd.edu/resource/growing-peppers-home-garden | 4fe5a4ddae5c61744f5919ac66105662c70483d16207334fe7d5221db9612c6f |
| Clemson pepper | https://hgic.clemson.edu/factsheet/pepper/ | 38a7621d2872c397731525703a8805c3a30d2690221a02b826a5b21655ed7b8b |
| WSU | https://s3.wp.wsu.edu/uploads/sites/2073/2014/09/Home-Vegetable-Gardening-in-Washington.pdf | 7378f653496200a6f260be82f4276a5834d196de2bdc4e7e17d0a720a48c3c34 |
| VT 426-331 | https://www.pubs.ext.vt.edu/426/426-331/426-331.html | 52fda56c97eca81aa63955bcc5d4dfdf8dbac4c29921a82eb35f154c0cd85720 |
| UF/IFAS VH021 | https://edis.ifas.ufl.edu/publication/VH021 | 7ff585e6999b66923a3422589b068032cd5ed6f3463bbe43f60a5325ed179994 |

Cited, NOT hashed: agrilifetoday.tamu.edu chile; ask.ifas.ufl.edu IN555; cameron.agrilife.org RGV; content.ces.ncsu.edu (root, bacterial spot, pests of pepper, phytophthora); edis.ifas.ufl.edu root; extension.arizona.edu az1005; extension.uga.edu + C963; extension.unr.edu 3267; extension.usu.edu frost pdf, planting dates, tomatoes; hort.extension.wisc.edu containers; ipm.ucanr.edu pepper-weevil; mg.ucanr.edu; naes.agnt.unr.edu; njaes.rutgers.edu FS279; pubs.nmsu.edu H240; ucanr.edu time-planting; ctahr.hawaii.edu; uaex.uada.edu; umass.edu pepper-maggot; unlv.edu.

## Authored field(s)
- `spacing_inches` = [12, 18]; `row_spacing_inches` = [24, 24].
- `planting_layout[0]` row-none: in_row [12, 18]; row_spacing [24, 24]; sources ["osu_ext"] -> OSU v979v342w, verified 2026-10-01.
- EVIDENCE (pla10_promote1): `jalapeno row-none in_row_inches [12,18] osu_ext https://ir.library.oregonstate.edu/downloads/v979v342w f2fdb1d6... "Peppers 10 weeks May May-June May-June May 5-10 plants 24"" 12-18"""` and the same quote for `row_spacing_inches [24,24]`. (OSU table columns: "...amount to plant for family of fourb distance between rowsc distance apart in the row...".) pla10_promote3: mature_height [3,4] from UMD.

## Hashed cited sentences on pepper ROW spacing (all of them)
- OSU f2fdb1d6 (table row): "...peppers 10 weeks may may-june may-june may 5-10 plants 24" 12-18" potatoes (sweet)..." -> rows 24", in-row 12-18".
- ISU 2ac60d9d: "spacing pepper plants are commonly spaced 18 inches apart within rows." / "rows should be spaced 24-30 inches apart." / "an alternate method is to plant two staggered rows 12-18 inches apart with plants spaced 18 inches apart within rows." / "the double rows should be spaced 30-36 inches apart."
- UMN 63c34d25: "space pepper plants 18 inches apart, in rows 30 to 36 inches apart." / "grow plants closer together if temperatures are below 60°f."
- UMD 4fe5a4dd: "spacing: 12"- 24" in-rows x 30"- 36" between row; double, staggered rows in 2-ft."
- Clemson 38a7621d: "peppers should be spaced 12 inches apart in the row." / "rows should be 3 feet apart."
- VT 52fda56c (table 5: "crop distance between plants in row distance between rows ..."): "...peppers 12-24 in 30-36 in 10 transplants 5-18 lbs 3-5 2 0..."
- WSU 7378f653 (table: "depth to plant (inch) distance between plants (inch) distance between rows (inch) ..."): "...pepper 1⁄4-1⁄2 18-24 12-24 10-20 65-95 50 6-8 60-80..." -> plants 18-24, rows 12-24.
- **No hashed cited page states "24 to 36" as a single row range.**

## FINDING: (a), with a caveat Trevor should see. The FIELD's 24 in rows is stated by OSU (its EVIDENCE row) and is the low end of ISU's "24-30"; no hashed cited page states the prose's "rows 24 to 36". Prose would change to match the field. CAVEAT (not a stop case by the (b) definition): five other hashed cited pages give WIDER rows than 24 -- ISU 24-30, UMN 30-36, UMD 30-36, VT 30-36, Clemson 3 ft -- so the prose's upper 36 is in the hashed literature, spread across pages; the single-point field [24,24] comes from the OSU table alone.

## Conflicting leaf: `growth_stages[2].user_action_seasoned`
CURRENT:
> Harden off over 7 to 10 days, then transplant into warm soil, 12 to 18 inches apart in rows 24 to 36 inches apart. Black plastic or fabric mulch warms the soil and gives a heat-loving crop a head start.

| # | claim | verdict | quote |
|---|---|---|---|
| 1 | harden off | MAPPED (general) | WSU: "harden vegetable plants for 4-7 days before transplanting them to your garden." |
| 2 | over 7 to 10 days | NO HASHED CITED PAGE STATES IT (WSU says 4-7 days) |
| 3 | transplant into warm soil | MAPPED | UMD: "planting: set out transplants after the soil has thoroughly warmed in the spring; start seed indoors 8 to 10 weeks before the average frost-free date (some types and cultivars require 12 weeks)." / "planting before soil temperature reaches 65 degrees f. will cause plants to \"just sit there.\""; UMN: "warm soil is better than cool."; Clemson: "therefore, after the soil has thoroughly warmed in the spring, set out 6 to 8 week-old transplants to get a head start toward harvest." |
| 4 | 12 to 18 inches apart (in-row) | MAPPED (matches field) | OSU table "...24" 12-18"..." |
| 5 | rows 24 to 36 inches apart | CONFLICT -- field [24,24]; see FINDING |
| 6 | black plastic or fabric mulch warms the soil | MAPPED | UMD: "you can also lay down black plastic or black landscape fabric prior to planting."; UMN: "use black plastic mulch to warm the soil, decrease weed growth and keep soil moisture." / "peppers benefit from black plastic mulch that warms the soil, decreases weed competition and keeps soil moisture."; WSU: "black plastic mulch absorbs heat and warms the soil in the spring and summer, creat- ing a better environment early in the season for warm-season crops such as melons, tomatoes, and peppers." |
| 7 | heat-loving crop | MAPPED | ISU: "peppers are a warm-season crop and need a long growing season for maximum production."; UMD: "...frost will injure top growth; needs warm weather to grow." (UMD attribute line) |
| 8 | (mulch) gives a head start | PARTIAL: Clemson uses "head start" for warmed-soil transplanting, not for mulch; WSU "creat- ing a better environment early in the season" |

`growth_stages[2].user_action_beginner` (not named; no row figure): "...plant them 12 to 18 inches apart into warm soil. A sheet of black plastic mulch warms the soil and helps." -- consistent with the field.
