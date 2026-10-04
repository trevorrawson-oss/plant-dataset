# lavender -- Phase C evidence packet (item 6, plain spacing conflict)

Canonical read: sha256 b331e5f2..., HEAD 1250f3a (main). Quotes in `norm_text` form; sha256 re-verified.

## Hashed pages cited on lavender
| source | url | sha256 |
|---|---|---|
| USU English lavender | https://extension.usu.edu/yardandgarden/research/english-lavender-in-the-garden | 342d4654f71c9a9d2a0085096bd252d8892dd9f652e0452b959d8bb2ed315b6c |
| NCSU Plant Toolbox | https://plants.ces.ncsu.edu/plants/lavandula-angustifolia/ | 92026102ec09e78170d524fbb8f30fba743206ff2f55c1a05e930c1066704683 |
| VT 426-331 | https://www.pubs.ext.vt.edu/426/426-331/426-331.html | 52fda56c97eca81aa63955bcc5d4dfdf8dbac4c29921a82eb35f154c0cd85720 (no lavender row) |

Cited, NOT hashed (incl. the two the prose credits): **newcropsorganics.ces.ncsu.edu/herb/lavender-history-taxonomy-and-production/** (the "NC State" spacing page anchored on diseases[1]); **extension.oregonstate.edu/ask-extension/featured/when-best-time-prune-lavender** (the "OSU" page); blogs.ifas.ufl.edu lavender; extension.arizona.edu (2); extension.colostate.edu growing-lavender; extension.purdue.edu foodlink; extension.umn.edu spittlebugs; extension.usu.edu planting dates; ipm.ucanr.edu (cultural tips, lavender, phytophthora, spittlebugs, whiteflies); lowwaterplants.nmsu.edu; naes.agnt.unr.edu; nwdistrict.ifas.ufl.edu; ppo.puyallup.wsu.edu/lavender/; pubs.nmsu.edu H221 + RR770; ucanr.edu (savvy-sage, marin, sonoma, santa clara); aspca.org; ctahr.hawaii.edu; nola.com; rhs.org.uk (cuckoo-spit, Hidcote details, growing guide); uaex.uada.edu; westhawaiitoday.com.

## Authored field(s)
- `spacing_inches` = [18, 24]; `row_spacing_inches` = null, `row_spacing_reason` = "not_authored".
- `planting_layout[0]` row-none, default: in_row_inches [18, 24]; row_spacing_inches null / "not_authored"; sources ["usu_ext_english_lavender"]; anchoring_urls.usu_ext_english_lavender = USU url, verified 2026-10-01.
- EVIDENCE (pla10_promote1/EVIDENCE.tsv): `lavender row-none in_row_inches [18,24] usu_ext_english_lavender https://extension.usu.edu/yardandgarden/research/english-lavender-in-the-garden 342d4654... "Space lavender plants 18-24 inches apart into light, well aerated, gravelly soil."` (pla10_promote3 has mature_height/spread rows only: NCSU "height: 1 ft. 0 in. - 2 ft. 0 in. width: 2 ft. 0 in. - 3 ft. 0 in.")

## Hashed cited sentences on lavender spacing
- USU 342d4654: "space lavender plants 18-24 inches apart into light, well aerated, gravelly soil." / "when cuttings are a year old, plant 18 to 24 inches apart into a dry, light, gravelly soil after the last frost has passed in spring."
- NCSU 92026102 (no plant-spacing sentence; size/space attributes only): "a dwarf shrub that is broadly mounded, english lavender grows up to 2 feet tall and 3 feet wide.." / "dimensions: height: 1 ft. 0 in. - 2 ft. 0 in. width: 2 ft. 0 in. - 3 ft. 0 in." / "available space to plant: 12 inches-3 feet" / "providing good air circulation helps prevent leaf spot."
- No hashed cited page states "2 to 3 feet apart" (searched "2 to 3 feet", "2-3 feet", "two to three feet", "24 to 36", "36 inches", "3 feet").

## FINDING: (a) -- a hashed cited page (USU) supports the FIELD [18,24]; no hashed cited page states the prose's 2 to 3 feet. The NC State and OSU pages the prose credits are cited but NOT hashed. Prose would change to match the field.

## Conflicting leaves (each with all its claims)
Entry `diseases[1]` (Leaf spot) anchors: ncsu_ext_lavandula_angustifolia (hashed), ncsu_ext newcropsorganics (NOT hashed), rhs Hidcote (NOT hashed).

### `diseases[1].control_ladder[0].note_beginner`
> Set lavender 2 to 3 feet apart in a dry, open, sunny spot. Air moving freely through the planting is the main defense against leaf spot, and it is decided when you space the plants rather than later.

| # | claim | verdict | quote |
|---|---|---|---|
| 1 | 2 to 3 feet apart | CONFLICT -- field is 18-24 in | USU: "space lavender plants 18-24 inches apart into light, well aerated, gravelly soil." |
| 2 | dry, sunny spot | MAPPED | NCSU: "this plant requires perfectly drained soil, preferably on the dry side, and full sun."; USU: "grow in full sun." |
| 3 | "open" spot | NO HASHED CITED PAGE STATES IT |
| 4 | air movement prevents leaf spot | MAPPED | NCSU: "providing good air circulation helps prevent leaf spot." |
| 5 | ...is the MAIN defense | NO HASHED CITED PAGE STATES IT (NCSU also: "however, it is susceptible to leaf spot and root rot.") |
| 6 | decided at spacing time rather than later | NO HASHED CITED PAGE STATES IT |

### `diseases[1].control_ladder[0].note_seasoned`
> Spacing at 2 to 3 feet on an open, sunny site is the published measure here, and NC State gives it for exactly this reason, to discourage fungal pathogens. Trimming the lower branches through the growing season is the in-season half of the same job: the base of a maturing bush is where the canopy closes over first.

| # | claim | verdict |
|---|---|---|
| 1 | spacing at 2 to 3 feet | CONFLICT (USU 18-24 in, above) |
| 2 | open, sunny site | sunny MAPPED (NCSU/USU above); open NOT STATED |
| 3 | NC State publishes 2-3 ft spacing for fungal control | the NC State page that would say it (newcropsorganics) is NOT hashed; the hashed NCSU toolbox says only "providing good air circulation helps prevent leaf spot." |
| 4 | trim lower branches through the growing season | NO HASHED CITED PAGE STATES IT (hashed pruning sentences are yearly/after-flowering: NCSU "cut it back yearly and remove the spent flower spikes after the flowers fade."; USU "lavender should be pruned every year after flowering.") |
| 5 | the base of a maturing bush is where the canopy closes first | NO HASHED CITED PAGE STATES IT |

### `diseases[1].prevention_seasoned`
> Space plants at least 2 to 3 feet apart for air circulation, site in full sun, and avoid overhead watering. Good airflow is the main defense.

| # | claim | verdict |
|---|---|---|
| 1 | at least 2 to 3 feet apart | CONFLICT (USU 18-24 in) |
| 2 | spacing for air circulation | air circulation vs leaf spot MAPPED (NCSU above); spacing-as-the-means NOT STATED |
| 3 | full sun | MAPPED (NCSU, USU) |
| 4 | avoid overhead watering | NO HASHED CITED PAGE STATES IT (USU nearest: "do not overwater or let water stand around the plants.") |
| 5 | airflow is the main defense | "main" NOT STATED |

### `diseases[1].prevention_beginner`
> Leave 2 to 3 feet between plants for airflow, plant in full sun, and avoid watering over the leaves. Good air movement is the main thing.

Same claims and verdicts as prevention_seasoned (#1 CONFLICT; airflow MAPPED to NCSU; full sun MAPPED; watering over the leaves NOT STATED; "main thing" NOT STATED).

### `regions.pnw.resolved_by_zone.8.frost_risk_note_seasoned` and `.9.frost_risk_note_seasoned` (identical text)
> Frost is not a concern for established lavender here; a wet, poorly drained winter is the real threat and can bring on root and crown rot. Prune hard once the chance of frost has passed and again after the main summer bloom fades, always leaving some green growth, and space plants 2 to 3 feet apart for airflow to limit fungal disease (OSU).

| # | claim | verdict | quote |
|---|---|---|---|
| 1 | frost not a concern for established lavender in zones 8/9 | PARTIAL: NCSU hardiness range includes 8 and 9; USU's range stops at 8 | NCSU: "usda plant hardiness zone: 5a, 5b, 6a, 6b, 7a, 7b, 8a, 8b, 9a, 9b"; USU: "while hardy in zones 5 to 8, it will survive zone 4 winters if mulched or grown in a south facing location." |
| 2 | wet, poorly drained soil is the threat | MAPPED (not winter-specific) | NCSU: "english lavender does not like wet feet and will die out in heavy clays."; USU: "it does not perform well in wet or water-logged soils." |
| 3 | ...in winter specifically | NO HASHED CITED PAGE STATES IT |
| 4 | root rot | MAPPED | NCSU: "root rot is caused by overwatering."; USU: "lavender has few pest or disease problems, but is susceptible to soil diseases such as phytophtora root rot." |
| 5 | crown rot | NO HASHED CITED PAGE STATES IT (ipm.ucanr phytophthora and ppo.puyallup.wsu are NOT hashed) |
| 6 | prune hard once frost chance has passed (spring) | NO HASHED CITED PAGE STATES IT (OSU prune page NOT hashed) |
| 7 | prune again after main summer bloom | MAPPED | USU: "lavender should be pruned every year after flowering."; NCSU: "cut it back yearly and remove the spent flower spikes after the flowers fade." |
| 8 | always leave some green growth | NO HASHED CITED PAGE STATES IT |
| 9 | space 2 to 3 feet apart | CONFLICT (USU 18-24 in) |
| 10 | spacing for airflow limits fungal disease | airflow vs leaf spot MAPPED (NCSU) |
| 11 | attribution "(OSU)" | the OSU page is cited but NOT hashed |

## Other lavender leaves (already agree with the field; for completeness)
`growth_stages[0].timing_seasoned`, `notifications[0].body_seasoned`, `tips_by_stage.transplant[1].text_seasoned`, `tips_by_stage.transplant[1].text_beginner` all say 18 to 24 inches. Mid-Atlantic / Mid-South zone notes say "space plants for airflow" with no figure.
