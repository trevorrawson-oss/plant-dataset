# Strawberry variety sourcing (berry flat schema) -- Task 4

Date: 2026-07-15
Crop: `strawberry` (variety_archetype `berry`, berry_group `strawberry`, `days_to_maturity: []` season-only)
Author lane: Claude Code (promote/gate). Canonical READ-ONLY; these 9 objects are staged at
`/private/tmp/strawberry_varieties.json` for the Task 6 builder.

## Rule
Per-variety `sources` are **T1-ONLY** (university .edu extension or government). Each variety's
`bearing_habit` + ripening season is confirmed against a T1 extension page and cited to the matching
catalogued id from strawberry's `verification_status.source_set`.

**0 non-T1 per-variety sources.** All 9 varieties carry `confidence_tier: T1`.

## Catalogued T1 ids used (id -> institution -> URL verified 2026-07-15)
| id | institution / doc | URL | how verified |
|---|---|---|---|
| `umn_ext` | Univ. of Minnesota Extension, "Strawberry varieties and purchasing plants" | https://extension.umn.edu/strawberry-farming/strawberry-varieties-and-purchasing-plants | WebFetch (HTML) |
| `umd_ext` | Univ. of Maryland Extension, "Growing Strawberries in a Home Garden" | https://extension.umd.edu/resource/growing-strawberries-home-garden | WebFetch (HTML) |
| `osu_ext` | Oregon State Univ. Extension, EC 1618 "Strawberry cultivars for Western Oregon and Washington" | https://extension.oregonstate.edu/catalog/ec-1618-strawberry-cultivars-western-oregon-washington | current catalog edition; cultivar classifications cross-checked in the EC 1618-E full text (Finn & Strik) via OSU IR-library download (catalog page blocks automated fetch; see note) |
| `cornell_ext` | Cornell Cooperative Extension (Oneida Co.), "Guide to Growing Strawberries" | https://cceoneida.com/resources/guide-to-growing-strawberries | WebFetch (served PDF, pypdf extract) |

Notes on OSU: the human-facing catalog page returns HTTP 403 to the automated fetcher, so the cultivar
classifications were read in full via the OSU institutional-repository text download of EC 1618-E
(`https://ir.library.oregonstate.edu/downloads/h415p971v`). It classifies the everbearers
(Ozark Beauty, Quinault) and day-neutrals (Albion, Seascape, Tristar) explicitly. The stable **current**
catalog edition (EC 1618, "Strawberry cultivars for Western Oregon and Washington") is the URL recorded
in the variety `anchoring_urls`; per content review it gives the day-neutral flowering cutoff as **85°F**,
and Albion's `note_seasoned` uses this current figure so a reader following the live link sees a matching
number (the older EC 1618-E full text stated 90°F).

## Per-variety table
| variety | bearing_habit | maturity_class (onset) | use | confidence_tier | T1 source id(s) | confirming evidence |
|---|---|---|---|---|---|---|
| Honeoye | june_bearing | early | fresh, freezing, jam | T1 | umn_ext, cornell_ext | UMN variety table lists Honeoye as an **early-season June-bearer** (yield data 2008-2019); Cornell CCE lists it among June-bearing cultivars. |
| Earliglow | june_bearing | early | fresh, jam | T1 | umd_ext, umn_ext | UMD: "The standard for flavor and **early-ripening** varieties" (June-bearing); UMN lists Earliglow among early June-bearers. |
| Jewel | june_bearing | mid | fresh, freezing | T1 | umn_ext, umd_ext | UMN classifies Jewel **June-bearing, midseason**; UMD lists Jewel as a June-bearing variety. |
| Allstar | june_bearing | mid | fresh | T1 | umd_ext, cornell_ext | UMD: "Productive **mid- to late-season** harvest" (June-bearing); Cornell CCE lists Allstar as red-stele/verticillium resistant June-bearer. |
| Albion | day_neutral | early | fresh | T1 | osu_ext, umn_ext | OSU EC 1618-E: the most important **day-neutral** cultivar; UMN lists Albion among day-neutrals recommended for MN. |
| Seascape | day_neutral | early | fresh, freezing | T1 | umd_ext, osu_ext | UMD lists Seascape as **day-neutral** ("large, good-quality fruits throughout the season"); OSU EC 1618-E classifies it day-neutral. |
| Tristar | day_neutral | early | fresh | T1 | umd_ext, cornell_ext | UMD: "A University of Maryland release, the **day-neutral** standard"; Cornell CCE lists Tristar among the top day-neutrals for the Northeast. |
| Ozark Beauty | everbearing | early | fresh, jam | T1 | osu_ext, cornell_ext | OSU EC 1618-E names Ozark Beauty explicitly as an **everbearing** cultivar; Cornell CCE: "older 'everbearing' types such as Ozark Beauty". |
| Quinault | everbearing | early | fresh | T1 | osu_ext | OSU EC 1618-E names Quinault explicitly among **everbearing** cultivars ("Ft. Laramie, Gem, Ogallala, Ozark Beauty, Quinault, Rockhill"). |

## maturity_class semantics
`maturity_class` = ripening ONSET. June-bearers use their documented flush timing (Honeoye/Earliglow
early; Jewel/Allstar mid). Day-neutral and everbearing types begin fruiting in early summer (day-neutrals
in the planting year), so their onset is `early`; the continuous / two-crop pattern is carried in the
notes, not the class. Values are taken verbatim from the Task 4 brief.

## Discrepancy logged (non-blocking)
- **Honeoye season**: the Cornell CCE Oneida home-fruit guide lists Honeoye once among "good midseason
  strawberries", whereas UMN (and the general trade) classify it **early**. The `early` value follows
  UMN's dedicated variety table and the brief's pre-mapping; Cornell is cited here only for the
  June-bearing habit, not the season.

## Coverage
- 9/9 varieties T1-sourced. 0 varieties un-sourceable. 0 non-T1 per-variety sources.
- `is_reference: true` on Albion only (widely adaptable day-neutral, the "good first choice").
- Flagship / reference variety: **Albion**.
