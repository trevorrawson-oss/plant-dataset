# brussels-sprouts -- Phase C evidence packet (item 9, plain spacing conflict)

Canonical read: sha256 b331e5f2..., HEAD 1250f3a (main). Quotes in `norm_text` form; sha256 re-verified.

## Hashed pages cited on brussels-sprouts
| source | url | sha256 |
|---|---|---|
| ISU brussels sprouts | https://yardandgarden.extension.iastate.edu/how-to/growing-brussels-sprouts-home-garden | 3f285142e2514bd9f491338be4b1bfcffc4ad30dec683029d0bf76afc79a6d10 |
| NCSU Plant Toolbox | https://plants.ces.ncsu.edu/plants/brassica-oleracea-brussels-sprouts-group/ | 029af02725d2129d51a60a193a9fce47f090c8895a4b24a5ca720a7793f24318 |
| WSU | https://s3.wp.wsu.edu/uploads/sites/2073/2014/09/Home-Vegetable-Gardening-in-Washington.pdf | 7378f653496200a6f260be82f4276a5834d196de2bdc4e7e17d0a720a48c3c34 |
| NMSU CR457B | https://pubs.nmsu.edu/_circulars/CR457B/ | cb59fcd17e7af0bfdd794f22f688f9c44065caf1a8f833b0415a78d86053655c |
| OSU chart | https://ir.library.oregonstate.edu/downloads/v979v342w | f2fdb1d636d2952473094c5ea64a4bd978fe90201fc4b5f897f2c39cfc685a33 |
| VT 426-331 | https://www.pubs.ext.vt.edu/426/426-331/426-331.html | 52fda56c97eca81aa63955bcc5d4dfdf8dbac4c29921a82eb35f154c0cd85720 |
| UF/IFAS VH021 | https://edis.ifas.ufl.edu/publication/VH021 | 7ff585e6999b66923a3422589b068032cd5ed6f3463bbe43f60a5325ed179994 |

Cited, NOT hashed: agrilifeextension.tamu.edu bilingual guide; cvp.cce.cornell.edu crop 7; edis.ifas.ufl.edu EP452; extension.arizona.edu Maricopa; extension.uga.edu C1069; extension.umd.edu brussels-sprouts + harlequin-bug; extension.umn.edu clubroot + growing-brussels-sprouts; extension.usu.edu cabbage-aphids, frost pdf, brussel-sprouts-in-the-garden, planting dates; hgic.clemson.edu (cole diseases, cole insects, start-brussels-sprouts blog); hort.extension.wisc.edu containers; ipm.ucanr.edu cultural tips; ucanr.edu mgscc2016 brussels-sprouts; ctahr.hawaii.edu B-91; lsuagcenter.com; mastergardenersd.org; uaex.uada.edu (fall, spring-summer); umass.edu aphid-cabbage; unlv.edu; vegetables.cornell.edu resistant brussels sprouts varieties.

## Authored field(s)
- `spacing_inches` = [18, 24]; `row_spacing_inches` = [24, 30].
- `planting_layout[0]` row-none: in_row [18, 24]; row_spacing [24, 30]; sources ["iastate_ext"] -> ISU, verified 2026-10-01.
- EVIDENCE (pla10_promote1): `brussels-sprouts row-none in_row_inches [18,24] iastate_ext ... 3f285142... "When planting cole crops in the garden, space plants 18 to 24 inches apart within the row."` and `row_spacing_inches [24,30] iastate_ext ... 3f285142... "Rows should be approximately 24 to 30 inches apart."` (pla10_promote3: height/spread 2-4 ft from NCSU.)

## Hashed cited sentences on brussels sprouts spacing
- ISU 3f285142: "spacing when planting cole crops in the garden, space plants 18 to 24 inches apart within the row." / "rows should be approximately 24 to 30 inches apart."
- **WSU 7378f653** (table header: "depth to plant (inch) distance between plants (inch) distance between rows (inch) number of days to germinate ..."): "...brussels sprout 1⁄4-1⁄2 18-24 24-36 3-10 45-85 40 5-6 80-105..." -> plants 18-24, **rows 24-36**.
- VT 52fda56c (table 5: in-row, between rows): "...brussels sprouts 18-24 in 30-36 in 7 transplants 3-5 lbs 2-5 0 1..."
- NMSU cb59fcd1 (table row): "...brussels sprouts 93 1/2 18-24 24-40 10 1/2 oz or 50-65 plants 60 -..."
- OSU f2fdb1d6 (table row; header text "...distance between rowsc distance apart in the row..."): "...brussels sprouts 6 weeks may-june may-july april-june april-july 15-20' of row 24" 24"..."
- NCSU 029af027: "click here to see a calendar of planting schedules, time-to-harvest, and recommended spacing." (no figure on the hashed page)

## FINDING: (c) -- both are supported, by different hashed cited pages. The FIELD rows [24,30] is ISU's sentence (its EVIDENCE row); the PROSE rows "24 to 36" is stated verbatim by the WSU table row (rows 24-36), which is hashed and cited on brussels-sprouts. (Other hashed tables: VT 30-36, NMSU 24-40, OSU 24.) Not a STOP case under (b), since the field is itself supported.

## Conflicting leaf: `tips_by_stage.seedling[0].text_seasoned`
(Entry has no sources/anchoring_urls.)
CURRENT:
> Transplant sturdy young plants with 4 to 6 true leaves at 18 to 24 inches apart in rows 24 to 36 inches apart; harden off over 7 to 10 days first.

| # | claim | verdict | quote |
|---|---|---|---|
| 1 | transplant sturdy young plants | MAPPED ("stocky") | ISU: "(gardeners in southern iowa can plant about one week earlier, while those in northern counties should wait one week later.) sow seeds indoors 4 to 5 weeks before planting outdoors or purchase young, stocky transplants at a greenhouse or garden center." |
| 2 | with 4 to 6 true leaves | NO HASHED CITED PAGE STATES IT |
| 3 | 18 to 24 inches apart | MAPPED (matches field) | ISU (above); WSU/VT/NMSU tables 18-24 |
| 4 | rows 24 to 36 inches apart | CONFLICT with field [24,30]; stated by WSU table (FINDING (c)) |
| 5 | harden off first | MAPPED | ISU: "harden or acclimate the transplants outdoors for several days before planting."; WSU: "harden vegetable plants for 4-7 days before transplanting them to your garden." |
| 6 | over 7 to 10 days | NO HASHED CITED PAGE STATES IT (ISU "several days"; WSU 4-7 days) |

`tips_by_stage.seedling[0].text_beginner` (not named): "Space plants about 18 to 24 inches apart, with wide rows, since they get big. Harden the seedlings off over about a week before planting out." -- no row figure; "get big" maps to NCSU "the plants can grow 2-4 feet tall and wide on a thick stalk."; "about a week" vs ISU "several days" / WSU "4-7 days".
