# basil -- Phase C evidence packet (item 7, plain spacing conflict)

Canonical read: sha256 b331e5f2..., HEAD 1250f3a (main). Quotes in `norm_text` form; sha256 re-verified.

## Hashed pages cited on basil
| source | url | sha256 |
|---|---|---|
| UMN growing basil | https://extension.umn.edu/vegetables/growing-basil | 3e61f84d118540f17ac722758c76ea72ee1ccf6fe75df7196cc10f3fa7f5b508 |
| UC MG Santa Clara basil | https://ucanr.edu/site/uc-master-gardeners-santa-clara-county/basil | 810b8b79889d638d193bbd49deac6dc9c01e21a95cfa2d41ff35fc934f93d04c |
| UF/IFAS VH021 | https://edis.ifas.ufl.edu/publication/VH021 | 7ff585e6999b66923a3422589b068032cd5ed6f3463bbe43f60a5325ed179994 (no basil spacing sentence) |

Cited, NOT hashed: agrilifeextension.tamu.edu (+ fall guide); agrilifetoday.tamu.edu companion planting; class.ucanr.edu FactSheet_Herb_Basil pdf; edis.ifas.ufl.edu EP450, EP451; extension.arizona.edu az1005 + az2061; extension.psu.edu fusarium-wilt + herbs-in-the-garden; extension.uga.edu C943; **extension.umd.edu/resource/downy-mildew-basil-home-garden**; extension.umn.edu companion planting + japanese beetles; **extension.usu.edu/yardandgarden/research/basil-in-the-garden**; extension.usu.edu planting dates; hgic.clemson.edu starting-seeds-indoors; naes.agnt.unr.edu; ucanr.edu time-planting; ucanr.edu Sonoma basil; ctahr.hawaii.edu B-91; uaex.uada.edu; **umass.edu basil-downy-mildew**; **vegetables.cornell.edu basil-downy-mildew**.

## Authored field(s)
- `spacing_inches` = [6, 12]; `row_spacing_inches` null / "not_authored".
- `planting_layout[0]` row-none: in_row [6, 12]; rows null / "not_authored"; sources ["umn_ext"] -> UMN growing-basil, verified 2026-10-01.
- EVIDENCE (pla10_promote1): `basil row-none in_row_inches [6,12] umn_ext https://extension.umn.edu/vegetables/growing-basil 3e61f84d... "Thin and transplant seedlings to stand 6-12 inches apart once they have developed two to three pairs of true leaves."` (pla10_promote3: mature height/spread from Santa Clara "size: 8 to 24 inches high, 8 to 12 inches wide, depending on variety".)

## Hashed cited sentences on basil spacing
- UMN 3e61f84d: "thin and transplant seedlings to stand 6-12 inches apart once they have developed two to three pairs of true leaves."
- Santa Clara 810b8b79 (plant size, not spacing): "mulch the soil to retain moisture size: 8 to 24 inches high, 8 to 12 inches wide, depending on variety when to plant/propagate basil leaves are tender and are damaged by temperatures below 40°f."
- No hashed cited page states 12-18 inch spacing.

## FINDING: (a) -- UMN (hashed, cited) supports the FIELD [6,12]; no hashed cited page states the prose's 12-18 inches. Prose would change to match the field.

## Conflicting leaves (each with all its claims)

### `failure_diagnostics[2].next_season_tip_seasoned`
Entry anchors: umd_ext, umass_ext, cornell_ext (all three NOT hashed).
> Plant downy-mildew-resistant varieties (labeled DMR): Devotion, Obsession, Prospera, Thunderstruck, or Amazel. Never water overhead; use drip or base watering. Ensure good air circulation through correct plant spacing (12-18 inches). In high-humidity regions, siting basil in a spot with afternoon airflow materially reduces risk.

| # | claim | verdict | quote |
|---|---|---|---|
| 1 | plant downy-mildew-resistant varieties | MAPPED | UMN: "due to the emergence of basil downy mildew , it is important to choose a variety resistant to this disease ." / "the most common basil issue in minnesota is basil downy mildew ." |
| 2 | they are labeled "DMR" | NO HASHED CITED PAGE STATES IT |
| 3 | named varieties Devotion, Obsession, Prospera, Thunderstruck, Amazel | NO HASHED CITED PAGE STATES IT |
| 4 | never water overhead; use drip/base watering | NO HASHED CITED PAGE STATES IT |
| 5 | air circulation via spacing | NO HASHED CITED PAGE STATES IT |
| 6 | spacing 12-18 inches | CONFLICT -- field 6-12 (UMN above) |
| 7 | high-humidity regions: afternoon airflow reduces risk | NO HASHED CITED PAGE STATES IT |

### `tips_by_stage.seedling[0].text_seasoned`
Entry anchors: umn_ext (hashed), usu_ext basil-in-the-garden (NOT hashed).
> Thin seedlings to one plant per 12-18 inches once they have their first true leaves. Crowded basil seedlings compete for light and air circulation, accelerating the damping-off conditions that kill seedlings at the base. The thinnings are edible; add them to salads or use as a first harvest.

| # | claim | verdict | quote |
|---|---|---|---|
| 1 | thin seedlings | MAPPED | UMN (above) |
| 2 | to one plant per 12-18 inches | CONFLICT -- field 6-12 |
| 3 | once they have their first true leaves | DIFFERS from UMN, which says two to three PAIRS of true leaves | UMN: "...once they have developed two to three pairs of true leaves." |
| 4 | crowded seedlings compete for light and air | NO HASHED CITED PAGE STATES IT |
| 5 | crowding accelerates damping-off | NO HASHED CITED PAGE STATES IT |
| 6 | thinnings are edible / salads / first harvest | NO HASHED CITED PAGE STATES IT (UMN's "use in potpourri, iced teas, salads." is a variety-use note, not about thinnings) |

## Related leaves (not named; for completeness)
- `tips_by_stage.seedling[0].text_beginner`: "...thin them to one plant every 12 inches..." -- 12 is within the field's [6,12] (endpoint); its "first real leaves" timing differs from UMN's "two to three pairs of true leaves".
- `varieties.recommended[3]` "Lemon basil ... 12-18 inches ..." -- a plant-size statement, not spacing.
