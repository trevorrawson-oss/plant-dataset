# oregano -- Phase C evidence packet (item 10, plain spacing conflict)

Canonical read: sha256 b331e5f2..., HEAD 1250f3a (main). Quotes in `norm_text` form; sha256 re-verified.

## Hashed pages cited on oregano
| source | url | sha256 |
|---|---|---|
| UF/IFAS Pasco blog (oregano) | https://blogs.ifas.ufl.edu/pascoco/2024/04/02/spice-up-your-life-a-beginners-guide-to-growing-oregano/ | c5b6ea3d3557e06bb892f107a3dda0c1da6c98bdb52016dccb54c008ce206d4b |
| TAMU Growing Herbs in Texas | https://agrilifeextension.tamu.edu/wp-content/uploads/2025/06/growingherbsintexas_4-1.pdf | d7a9c578f4d6cfc535c7dc53aa554fb639fd27bd4833df9f6e04ab81e841718b |
| NCSU Plant Toolbox | https://plants.ces.ncsu.edu/plants/origanum-vulgare/ | d99761086c51efba01a43fb810551b7d8438b15c170483752a31e9b6e3eb7c8c |
| VT 426-331 | https://www.pubs.ext.vt.edu/426/426-331/426-331.html | 52fda56c97eca81aa63955bcc5d4dfdf8dbac4c29921a82eb35f154c0cd85720 (no oregano row) |

Cited, NOT hashed: apps.cals.arizona.edu arboretum 1292; content.ces.ncsu.edu phytophthora blight; extension.illinois.edu/herbs/oregano; extension.psu.edu herb-garden-plants-oregano; extension.usu.edu planting dates; hgic.clemson.edu herbs; **ipm.ucanr.edu/PMG/PESTNOTES/pn7406.html** (powdery mildew; anchors diseases[2]) + pn7404, pn7405; ipm.ucanr.edu oregano + cultural-tips; naes.agnt.unr.edu; aspca.org oregano; rhs.org.uk oregano; uaex.uada.edu.

## Authored field(s)
- `spacing_inches` = [10, 12]; `row_spacing_inches` null / "not_authored".
- `planting_layout[0]` row-none: in_row [10, 12]; rows null / "not_authored"; sources ["uf_ifas"] -> UF Pasco blog, verified 2026-10-01.
- EVIDENCE (pla10_promote1): `oregano row-none in_row_inches [10,12] uf_ifas https://blogs.ifas.ufl.edu/pascoco/2024/04/02/... c5b6ea3d... "Space your plants 10-12 inches apart, this will help with air circulation"` (pla10_promote3: height [1,3] / spread [1,2] from NCSU "height: 1 ft. 0 in. - 3 ft. 0 in. width: 1 ft. 0 in. - 2 ft. 0 in.")

## Hashed cited sentences on oregano spacing / size
- UF c5b6ea3d: "adequate air circulation : space your plants 10-12 inches apart, this will help with air circulation and prevent extra humidity that attracts pests and diseases."
- UF c5b6ea3d (plant SIZE, not spacing): "oregano's growth is bushy and can grow up to two feet tall and up to 18 inches wide."
- **TAMU d7a9c578 (oregano row; states a DIFFERENT, narrower figure):** "...oregano (origanum vulgare) 24 choose english strains. produces pink flowers. plant in rich soil. space 8-10 in. start in protected location and move to full sun. harvest mature leaves..."
- NCSU d9976108: "available space to plant: 12 inches-3 feet" / "dimensions: height: 1 ft. 0 in. - 3 ft. 0 in. width: 1 ft. 0 in. - 2 ft. 0 in."
- No hashed cited page states an 18-inch SPACING for oregano.

## FINDING: (a) -- UF (hashed, cited) supports the FIELD [10,12]; no hashed cited page states spacing "up to 18 inches" (UF's 18 inches is plant width). Prose would change to match the field.
Side observation (outside this item; for Trevor): the hashed TAMU herb guide gives oregano "space 8-10 in." The "space 10-12 in." on that PDF is the THYME row ("thyme (thymus vulgaris) 8-12 narrow, dark green leaves. start seeds indoors. prefers full sun and well-drained soils. space 10-12 in."). `regions.rgv.resolved_by_zone.9/.10.grown_as_note_seasoned` currently say "Texas A&M AgriLife's herb-growing guidance ... spaced about 10 to 12 inches apart" -- that attribution does not match the hashed TAMU oregano row.

## Conflicting leaf: `diseases[2].control_ladder[0].note_seasoned`
Entry `diseases[2]` (Powdery mildew) anchors: uf_ifas (hashed), ucanr_ext pn7406 (NOT hashed).
CURRENT:
> UF/IFAS ties spacing to the humidity inside the canopy rather than to water on the leaf, and that distinction is the whole point: powdery mildew infects without free water on the surface, so keeping the foliage dry is not the lever it is on most leaf diseases. Published spacing for oregano runs from 10 inches up to 18 inches depending on which extension source you read, so take the wider end in a humid summer, and thin an established clump rather than letting it close over. Site matters for the same reason: shade is a favoring condition for this fungus, so an open position is doing real work and not just growing better oregano.

| # | claim | verdict | quote |
|---|---|---|---|
| 1 | UF/IFAS ties spacing to humidity | MAPPED | UF: "adequate air circulation : space your plants 10-12 inches apart, this will help with air circulation and prevent extra humidity that attracts pests and diseases." |
| 2 | ...rather than to water on the leaf | **CONTRADICTED by the same UF page**, which pairs airflow WITH avoiding overhead water for powdery mildew | UF: "to prevent powdery mildew, provide good air circulation around plants and avoid overhead watering." |
| 3 | powdery mildew infects without free water | NO HASHED CITED PAGE STATES IT (pn7406 NOT hashed) |
| 4 | so keeping foliage dry is not the lever | NO HASHED CITED PAGE STATES IT; UF (#2) says avoid overhead watering |
| 5 | published spacing runs 10 up to 18 inches | CONFLICT -- field 10-12 (UF); no hashed page states 18 in spacing; TAMU states 8-10 |
| 6 | "depending on which extension source you read" | hashed sources: UF 10-12, TAMU 8-10 (not 10-18) |
| 7 | take the wider end in a humid summer | NO HASHED CITED PAGE STATES IT |
| 8 | thin an established clump rather than letting it close over | NO HASHED CITED PAGE STATES IT (UF prunes for growth habit: "prune regularly : trim oregano stems regularly to encourage new growth and prevent the plant from becoming woody or leggy.") |
| 9 | shade favors this fungus | NO HASHED CITED PAGE STATES IT (UF in fact recommends some shade in Florida: "providing oregano with a bit of afternoon shade can protect it from the intense sunlight.") |
| 10 | an open position does real work | NO HASHED CITED PAGE STATES IT |
| ctx | oregano gets powdery mildew, esp. in humidity | MAPPED | UF: "diseases oregano is generally resistant to diseases, but it can occasionally suffer from fungal infections like powdery mildew or root rot, especially in humid conditions." / "powdery mildew : powdery mildew appears as a white, powdery coating on oregano leaves, affecting plant health and appearance." |

## Related leaves (agree with the field; for completeness)
`diseases[2].prevention_seasoned` / `_beginner` ("10 to 12 inches apart or wider/more"), `growth_stages[0].timing_seasoned`, `notifications[0].body_seasoned` (10 to 12). `diseases[2].control_ladder[0].note_beginner` has no figure.


## ADDITION A: rgv leaves that credit TAMU with a 10-12 inch spacing

Canonical read: sha256 b331e5f2..., HEAD 6e444f3 (main). Hashes re-verified over the bytes this pass. Quotes in `norm_text` form, each machine-checked as a substring of its hashed text.

**Is the TAMU herb guide cited on oregano? YES.** `https://agrilifeextension.tamu.edu/wp-content/uploads/2025/06/growingherbsintexas_4-1.pdf` is in `cited_urls(oregano)`; hashed as d7a9c578f4d6cfc535c7dc53aa554fb639fd27bd4833df9f6e04ab81e841718b (PDF, `norm_text(pdf_text(raw))`). On oregano it is cited ONLY under `regions.rgv` (source id `tamu_agrilife`, in `regions.rgv.sources`, `regions.rgv.plantings[0].anchoring_urls`, `regions.rgv.resolved_by_zone.9/.10.anchoring_urls`, verified "2026-07-13").

### TAMU rows, side by side (d7a9c578, extracted text as it reads)
Both rows sit in the guide's PERENNIALS table, whose lead-in reads: "perennials: they grow from seed the first year, but grow year after year." and whose column header reads: "herb height (inches) description culture harvest use".

| row | extracted text (norm_text) |
|---|---|
| **OREGANO** | "oregano (origanum vulgare) 24 choose english strains. produces pink flowers. plant in rich soil. space 8-10 in. start in protected location and move to full sun. harvest mature leaves. leaves - soups, meats (roasts), stews, salads" |
| **THYME** | "thyme (thymus vulgaris) 8-12 narrow, dark green leaves. start seeds indoors. prefers full sun and well-drained soils. space 10-12 in. harvest leaves and flower clusters before first flowers open. leaves - soups, salads, dressings, omelets, gravies, breads, vegetables" |

Read across: oregano = height 24 in, **space 8-10 in.**, "plant in rich soil", full sun after a protected start. Thyme = height 8-12 in, **space 10-12 in.**, "prefers full sun and well-drained soils". The rgv leaves' "10 to 12 inches" + "well-drained soil" both match the THYME row, not the oregano row. (The raw PDF text puts "substitute for celery flower" immediately before "oregano"; that is the end of the LOVAGE row's use column: "harvest mature leaves. substitute for celery flower".)

The only "10-12" anywhere in the hashed TAMU text is the thyme row. The only "woody" hits on the TAMU text are the place names "greenwood" / "kenwood" (supplier list); TAMU never calls oregano woody.

TAMU general (not row-specific) sentences that the leaves could lean on:
- TAMU: "select a sunny, well-drained location." (herb-garden siting, all herbs)
- TAMU: "perennial herbs can be propagated by cuttings or by division." / "divide plants every 3 or 4 years in the early spring." / "dig up the plants and cut into several sections." (all perennial herbs; not tied to woodiness)

The 10-12 inch figure IS on a hashed page cited on oregano, but it is UF's, not TAMU's:
- UF c5b6ea3d: "adequate air circulation : space your plants 10-12 inches apart, this will help with air circulation and prevent extra humidity that attracts pests and diseases."

### Leaves found (every rgv leaf on oregano crediting TAMU with 10-12 in)
Five leaves, two distinct texts:
- Text G (2 leaves): `regions.rgv.resolved_by_zone.9.grown_as_note_seasoned`, `regions.rgv.resolved_by_zone.10.grown_as_note_seasoned` (byte-identical).
- Text S (3 leaves): `regions.rgv.plantings[0].synthesis_note_seasoned`, `regions.rgv.resolved_by_zone.9.synthesis_note_seasoned`, `regions.rgv.resolved_by_zone.10.synthesis_note_seasoned` (byte-identical).

Not in scope but credit TAMU on other points (no spacing figure): `regions.rgv.resolved_by_zone.9/.10.grown_as_note_beginner`, `regions.rgv.region_notes_beginner`, `regions.rgv.region_notes_seasoned` (each credits TAMU for dig/replant every three to four years); `regions.rgv.plantings_provenance.note` (credits TAMU for "full sun, well-drained soil").

### Leaf: `regions.rgv.resolved_by_zone.9.grown_as_note_seasoned` (identical text at `.10.grown_as_note_seasoned`)
CURRENT:
> Oregano is a durable perennial in the Rio Grande Valley's frost-free winters. Texas A&M AgriLife's herb-growing guidance for the state calls for full sun and well-drained soil, spaced about 10 to 12 inches apart, and notes it is a perennial that becomes woody after a few years and is best dug and replanted at that point. Give it a raised bed or mound with sharp drainage and open airflow; the Valley's summer humidity, more than its heat, is what brings on root and stem rot in a low, poorly drained spot.

| # | claim | verdict | quote |
|---|---|---|---|
| 1 | oregano is a durable perennial | MAPPED | UF: "oregano is a hardy perennial (this herb will grow back season after season) that can be easily grown from seed or cuttings." |
| 2 | ...in the Rio Grande Valley's frost-free winters | NO HASHED CITED PAGE STATES IT (no hashed cited page names the RGV; UF: "seasonality oregano is a perennial herb that thrives in central florida's mild winters and warm summers."; UF hardiness: "usda hardiness zone: 5 to 9." -- the zone 10 leaf sits outside UF's stated range) |
| 3 | TAMU calls for full sun | MAPPED (oregano row) | TAMU: "start in protected location and move to full sun." |
| 4 | TAMU calls for well-drained soil | PARTIAL: TAMU states it for herb-garden siting generally, NOT in the oregano row (oregano row says "plant in rich soil."); "well-drained soils" in a row is THYME's | TAMU: "select a sunny, well-drained location." |
| 5 | TAMU: spaced about 10 to 12 inches apart | **MISATTRIBUTED.** TAMU's oregano row states 8-10 in; 10-12 in is TAMU's THYME row. 10-12 for oregano is stated by UF (hashed, cited) | TAMU oregano: "plant in rich soil. space 8-10 in." / TAMU thyme: "prefers full sun and well-drained soils. space 10-12 in." / UF: "adequate air circulation : space your plants 10-12 inches apart, this will help with air circulation and prevent extra humidity that attracts pests and diseases." |
| 6 | TAMU notes it is a perennial | MAPPED (table placement: oregano row sits in TAMU's perennials table) | TAMU: "perennials: they grow from seed the first year, but grow year after year." |
| 7 | becomes woody after a few years | NOT ON TAMU. "woody" (no time frame) is NCSU's; UF ties woodiness to lack of pruning, not age; NO HASHED CITED PAGE STATES "after a few years" | NCSU d9976108: "oregano is a woody, branching, herbaceous perennial with a bushy habit in the mint family native to europe and asia." / UF: "prune regularly : trim oregano stems regularly to encourage new growth and prevent the plant from becoming woody or leggy." |
| 8 | (TAMU) best dug and replanted at that point | PARTIAL: TAMU says divide perennial herbs every 3 or 4 years (all perennial herbs, not oregano-specific, not tied to woodiness) | TAMU: "divide plants every 3 or 4 years in the early spring." / "dig up the plants and cut into several sections." |
| 9 | raised bed | MAPPED (UF, central Florida) | UF: "in central florida, it is beneficial to grow oregano in raised beds to better control moisture retention and soil texture." |
| 10 | ...or mound | NO HASHED CITED PAGE STATES IT |
| 11 | sharp drainage | MAPPED | UF: "growing conditions: thrives in full sun with well-draining soil." / NCSU: "oregano does best in average soil including sandy loams, dry to medium moisture with good drainage, and planted in a site with full sun." |
| 12 | open airflow | MAPPED | UF: "to prevent powdery mildew, provide good air circulation around plants and avoid overhead watering." |
| 13 | humidity brings on root rot | MAPPED | UF: "diseases oregano is generally resistant to diseases, but it can occasionally suffer from fungal infections like powdery mildew or root rot, especially in humid conditions." |
| 14 | ...and stem rot | NO HASHED CITED PAGE STATES IT |
| 15 | humidity "more than its heat" | NO HASHED CITED PAGE STATES IT (UF names both: "these varieties are better suited to withstand central florida's high temperatures and humidity.") |
| 16 | the Valley's summer humidity | NO HASHED CITED PAGE STATES IT (no RGV page) |
| 17 | in a low, poorly drained spot | MAPPED (poorly drained) | NCSU: "diseases, insect pests, and other plant problems: root rot can occur in wet, poorly drained soils." / UF: "improve soil drainage and avoid overwatering to prevent root rot." |

### Leaf: `regions.rgv.plantings[0].synthesis_note_seasoned` (identical text at `regions.rgv.resolved_by_zone.9.synthesis_note_seasoned` and `.10.synthesis_note_seasoned`)
CURRENT:
> grown_as=perennial (frost-free): oregano overwinters as a low woody sub-shrub through the Valley's mild winters with no dieback. Bloom (May - Jul) is reused from this crop's own se_gulf zone 9/10 rows, frost/phenology-modeled rather than read from a Valley-specific chart. Texas A&M AgriLife's statewide herb guidance recommends full sun, 10 to 12 inch spacing, and dividing/replanting every 3 to 4 years as the plant becomes woody. plant_out follows the general cool-season, avoid-peak-heat convention. Flagged blocks_launch:false: no oregano-specific RGV chart exists.

| # | claim | verdict | quote |
|---|---|---|---|
| 1 | grown_as=perennial | MAPPED | UF: "remember, oregano is perennial, so it will grow back season after season." |
| 2 | (frost-free) region | NO HASHED CITED PAGE STATES IT (no RGV page) |
| 3 | overwinters as a low woody sub-shrub | PARTIAL: "woody" (NCSU); "sub-shrub" and "low" NO HASHED CITED PAGE STATES IT (NCSU height is 1-3 ft) | NCSU: "oregano is a woody, branching, herbaceous perennial with a bushy habit in the mint family native to europe and asia." / NCSU: "dimensions: height: 1 ft. 0 in. - 3 ft. 0 in. width: 1 ft. 0 in. - 2 ft. 0 in." |
| 4 | through the Valley's mild winters with no dieback | NO HASHED CITED PAGE STATES IT (UF, central Florida, allows dieback: "oregano is a winter-hardy herb, and even if it dies back, it will grow back in the spring.") |
| 5 | Bloom May - Jul reused from se_gulf rows, modeled | PROVENANCE STATEMENT (internal derivation, not a source claim). Nearest hashed: NCSU bloom season | NCSU: "bloom in axillary or terminal corymb-like spikelets in late spring and summer." |
| 6 | TAMU recommends full sun | MAPPED (oregano row) | TAMU: "start in protected location and move to full sun." |
| 7 | TAMU recommends 10 to 12 inch spacing | **MISATTRIBUTED** (TAMU oregano row 8-10; TAMU thyme row 10-12; UF states 10-12 for oregano) | TAMU oregano: "plant in rich soil. space 8-10 in." / TAMU thyme: "prefers full sun and well-drained soils. space 10-12 in." |
| 8 | TAMU recommends dividing/replanting every 3 to 4 years | MAPPED (general perennial-herb instruction, not the oregano row) | TAMU: "divide plants every 3 or 4 years in the early spring." |
| 9 | ...as the plant becomes woody | NOT ON TAMU (no "woody" in the TAMU text); NO HASHED CITED PAGE ties division to woodiness |
| 10 | plant_out follows the cool-season, avoid-peak-heat convention | PROVENANCE STATEMENT. Nearest hashed: UF (Florida) | UF: "conscious planting: in florida, the best time to plant oregano is during the cooler months of fall and winter." |
| 11 | blocks_launch:false; no oregano-specific RGV chart exists | RECORD STATEMENT (internal flag; consistent with: no hashed cited page is RGV-specific) |
