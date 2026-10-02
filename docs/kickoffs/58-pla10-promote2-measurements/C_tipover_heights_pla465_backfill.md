# Agent C: PLA-10 promote 2, tip-over heights + the 16-crop sibling backfill (READ-ONLY measurement)

Measured 2026-10-02. Checkout: branch `main`, HEAD 78d734b (origin/main bc71f34; HEAD is 1 ahead, the local
unpushed promote-2 session-1 tools commit). Canonical shasum = cf1d480d... = LATEST.txt. No repo file edited.

Evidence reading: tools/.evidence_cache/<sha256>.* via MANIFEST.tsv (sha verified on read) and tools/.doc_cache/<sha1(url)>.txt,
both through `norm_text` (pypdf for PDFs). No web fetch. Quotes below are verbatim from the cached text (normalized lowercase
as `norm_text` renders it; original casing shown where the spec quotes it).

**Load-bearing caveat for both tasks:** the promote-2 evidence check (`tools/promote_pla10_promote2.py`, `EVIDENCE =
.evidence_cache`) reads ONLY `.evidence_cache`. Of every page below, only three have hashed bytes there: UMD peppers
(4fe5a4dd...), UF/IFAS HS402 lemon (15801f6d...), NC State asimina-triloba pawpaw (89feb7e0...). Everything else is in
`.doc_cache` only (extracted text, sha1-of-url named, no sha256). So 6 of the 7 non-pepper tip-over pages and 14 of the 16
backfill pages need bytes saved into `.evidence_cache` (a web-capable session) before promote 2's quote check can pass them.

## Task 1: the 11 tip-over crops

All 11: `verification_status.status == verified_gs_arc`, `mature_height_ft` null, `mature_spread_ft` null (confirmed).
Every page below is cited by the crop in cf1d480d (path given) and the quote is present in cached bytes.

| crop | page (cited at) | cache | verbatim | proposed mature_height_ft | mature_spread_ft | catalog id |
|--|--|--|--|--|--|--|
| bell-pepper | https://extension.umd.edu/resource/growing-peppers-home-garden (`soil.anchoring_urls.umd_ext`) | evidence_cache/4fe5a4dd...6c6f.html (sha ok) + doc_cache/bdb44ee4....txt | "peppers are produced on bushy plants that can reach 3-4 ft. in height." | [3, 4] | null | umd_ext |
| jalapeno | same (`fertilizer.anchoring_urls.umd_ext`) | same | same | [3, 4] | null | umd_ext |
| banana-pepper | same (`soil.anchoring_urls.umd_ext`) | same | same | [3, 4] | null | umd_ext |
| cayenne-pepper | same (`container_notes.anchoring_urls.umd_ext`) | same | same | [3, 4] | null | umd_ext |
| habanero | same (`container_notes.anchoring_urls.umd_ext`) | same | same | [3, 4] (scope: reviewer) | null | umd_ext |
| broccoli | https://content.ces.ncsu.edu/basics-of-broccoli-production (`soil.anchoring_urls.ncsu_ext`) | doc_cache/2d910ca1....txt ONLY | "full-grown plants reach about 47 inches tall and 20 inches wide, relying on bees for cross-pollination." | [47/12, 47/12] = 3.9167 (see quote-check bug) | [20/12, 20/12] = 1.6667 (same sentence states width) | ncsu_ext |
| brussels-sprouts | https://plants.ces.ncsu.edu/plants/brassica-oleracea-brussels-sprouts-group/ (`watering.anchoring_urls.ncsu_ext`) | doc_cache/d2a99a8d....txt ONLY | "the plants can grow 2-4 feet tall and wide on a thick stalk." | [2, 4] | [2, 4] ("tall and wide") | ncsu_ext |
| broad-beans-fava | https://plants.ces.ncsu.edu/plants/vicia-faba/ (`soil.anchoring_urls.ncsu_ext`) | doc_cache/da953185....txt ONLY | "it is a stiffly erect plant that grows 2-6 feet tall and prefers moist loams..." | [2, 6] | null | ncsu_ext |
| cosmos | NC State https://plants.ces.ncsu.edu/plants/cosmos-bipinnatus/ (`soil.anchoring_urls.ncsu_ext`); UF/IFAS https://gardeningsolutions.ifas.ufl.edu/plants/ornamentals/cosmos/ (`ph.anchoring_urls.uf_ifas`) | doc_cache/7032ec53....txt; doc_cache/b9179f10....txt ONLY | NCSU: "...white flowers on stalks that will get up to 4 feet tall."; UF: "garden cosmos can reach 3-6 feet and has finer, string-like foliage." | REVIEWER CALL: UF [3, 6] (closed range; crop's own prose agrees) vs NCSU open "up to 4" (no lo, cannot fill [lo,hi] alone) | null | uf_ifas (if UF taken) |
| dill | https://hort.extension.wisc.edu/articles/dill-anethum-graveolens/ (`soil.anchoring_urls.uwi_hort`) | doc_cache/0341f299....txt ONLY | "dill plants grow 18 inches to 4 feet tall and resemble fennel." | [1.5, 4] | null | uwi_hort |
| eggplant | https://plants.ces.ncsu.edu/plants/solanum-melongena/ (`pet_safe.anchoring_urls.ncsu_ext`) | doc_cache/ef64bfea....txt ONLY | "the plant may grow 2 to 4 feet tall and is multi-branched." | [2, 4] | null | ncsu_ext |

All four catalog ids (umd_ext, ncsu_ext, uf_ifas, uwi_hort) exist in `source_catalog`, T1.
None of the 6 non-UMD URLs appears in MANIFEST.tsv (checked exact + fuzzy).

### Scope check (UMD genus page on habanero and cayenne)
- Page lists by name: "hot varieties, such as serrano, jalapeno, cayenne, habanero, piquin, tabasco" and states "habanero types
  ripen 90-120 days from transplanting". It also says "pungent types ... are mostly in the same species as sweet pepper types,
  capsicum annum" ("mostly" = it knowingly covers non-annuum types). It never names chinense.
- **cayenne-pepper**: crop record is Capsicum annuum only; page names cayenne in its scope. IN SCOPE.
- **habanero**: crop record names Capsicum chinense. The page explicitly includes habanero in its subject and gives it a
  habanero-specific timing, so the genus-level height sentence ("Peppers are produced on bushy plants that can reach 3-4 ft.")
  is stated over a population that includes habanero by name. Recommend IN SCOPE, but a reviewer call: the height sentence
  itself is not habanero-specific and C. chinense is not named. jalapeno, banana, bell all named on the page and annuum.

### Cross-check against the crops' own prose (non-variety fields; container_notes, description, growth_stages, tips)
- peppers x5, broccoli, brussels-sprouts, eggplant: no plant-height statement in prose (only transplant "up to a foot tall",
  head/sprout widths). No disagreement possible. brussels container_notes says "tall, top-heavy" (consistent).
- **broad-beans-fava: DISAGREES on the high end.** description_* / container_notes / growth_stages beginner say "2 to 4 feet";
  seasoned growth_stages and tips say "2 to 4 feet ... some tall types to 5 or 6 feet". NCSU [2, 6] covers it; the
  beginner-register "2 to 4" is narrower than the cited figure.
- **cosmos:** description_seasoned "reaches roughly 3 to 6 ft" (= UF/IFAS); varieties.recommended[0] Sensation "tall 3 to 4 ft".
  Prose supports UF [3, 6].
- **dill: DISAGREES on the high end.** container_notes_seasoned "Standard dill reaches 3 to 5 feet", description "the plant reaches
  3 to 5 feet in flower", variety note "3 to 5 feet"; UW-Madison says 18 in to 4 ft. Prose's 5 ft exceeds the cited 4 ft (and the
  prose's 3 ft floor is above the cited 1.5). Either the prose has an uncited 5 or it sits on another page; flag for reviewer.

### Quote-check bug (owed in tools before broccoli can promote)
`pla10_promote_common.quote_states`:
- `mature_height_ft` matches ends or ends*12. Broccoli [3.9167,3.9167] -> 3.9167*12 = 47.0004 -> **False**; only the unrounded
  float 47/12 = 3.9166666666666665 passes (x12 == 47.0). Thyme's [0.5, 1.3333] precedent would likewise fail.
- `mature_spread_ft` has NO branch: it falls to the default `x/12` (inches) path, so a feet spread from an inches quote
  (broccoli 20 in) is **False for any value**. Brussels [2,4] passes only because "2-4 feet" matches directly.
- `promote_pla10_promote2.py` does not reference mature_height_ft/mature_spread_ft yet, so this is latent, not live.

## Task 2: PLA-465's 16 crops with authored mature_height_ft

Each has exactly one `verification_status.field_additions` record `field: plant_dimensions`, date 2026-09-16, naming
institution, URL, bytes and sha256. **None of the 16 recorded sha256s matches any file in `.evidence_cache`, and no file
named by any of them exists anywhere in the repo** (grep finds the shas only in tools/staging/pla465_* spec.json and
promote_pla466_rootstock.py). The record shas are claims with no retained bytes.

| crop | h / s (canonical) | record catalog id (in catalog?) | record URL | URL cited elsewhere on crop | cache of that URL | height sentence in cache | proposed sibling |
|--|--|--|--|--|--|--|--|
| peach | [15,25] / [15,25] | ncsu_ext (yes) | https://plants.ces.ncsu.edu/plants/prunus-persica/ | yes | doc_cache/7d357756....txt | FOUND "the tree will grow quickly to 15-25 feet tall and wide" + attributes | ["ncsu_ext"], {ncsu_ext: {url: prunus-persica/}} |
| nectarine | [15,25] / [15,25] | ncsu_ext (yes) | same prunus-persica | yes | same | FOUND (+ "nectarine" in common names) | same |
| apple | [10,14] / null | wsu_ext (yes) | https://s3.wp.wsu.edu/uploads/sites/2109/2019/12/fruit_handbook_western_wa.pdf | **NO** | **UNCACHED** at this URL | -- | **FLAG.** Same handbook is cited on apple (regions.pnw.*) at https://wpcdn.web.wsu.edu/wp-extension/uploads/sites/2109/2019/12/fruit_handbook_western_wa.pdf, doc_cache/44298206....txt, which contains "m 26-semi-dwarf habit, 10'-14' tall, common in home orchards..." Backfill should point at the wpcdn URL (cited + cached), wsu_ext |
| lemon | [10,20] / null | uf_ifas_hs1153 (yes; catalog url = HS402) | https://edis.ifas.ufl.edu/publication/HS402 | yes | evidence_cache/15801f6d... (sha differs from record's 50436e71) + doc_cache/a629f702....txt | FOUND "trees may reach 10-20 ft (3.1-6.1 m) in height (morton 1987)." | ["uf_ifas_hs1153"], {.. HS402} |
| blueberry | [5,8] / [5,8] | psu_ext (yes) | https://extension.psu.edu/blueberries-in-the-garden-and-the-kitchen | **NO** (record itself says "this specific URL is not yet cited on the crop") | **UNCACHED** | -- | **FLAG.** A cited, cached PSU page (https://extension.psu.edu/highbush-blueberry-production, doc_cache/11b9cabb....txt) says "highbush blueberries are usually 4 to 8 feet tall at maturity" -- **disagrees** with the authored [5,8] low end, no spread. Reviewer call: fetch the record's page or re-anchor to [4,8] |
| thyme | [0.5,1] / [0.5,1.3333] | ncsu_ext (yes) | https://plants.ces.ncsu.edu/plants/thymus-vulgaris/ | yes | doc_cache/3857c3c7....txt | FOUND "about 6 to 12 inches high and 6 to 16 inches wide" + attributes | ["ncsu_ext"], {.. thymus-vulgaris/} (spread 1.3333 trips the quote-check bug) |
| rosemary | [4,5] / [3,4] | ncsu_ext (yes) | https://plants.ces.ncsu.edu/plants/salvia-rosmarinus/ | yes | doc_cache/0bc400f9....txt | FOUND "the shrub grows from 4 to 5 feet tall"; width 3-4 from attributes | ["ncsu_ext"], {.. salvia-rosmarinus/} |
| oregano | [1,3] / [1,2] | ncsu_ext (yes) | https://plants.ces.ncsu.edu/plants/origanum-vulgare/ | yes | doc_cache/3f736039....txt | FOUND "a height of 3 feet with a 2 foot spread" + attributes | ["ncsu_ext"], {.. origanum-vulgare/} |
| sage | [1,2] / [2,3] | ncsu_ext (yes) | https://plants.ces.ncsu.edu/plants/salvia-officinalis/ | yes | doc_cache/e8b029f9....txt | FOUND "up to 2 feet tall and 2 to 3 feet wide" + attributes | ["ncsu_ext"], {.. salvia-officinalis/} |
| fig | [15,30] / [15,30] | clemson_hgic (yes) | https://hgic.clemson.edu/factsheet/fig/ | yes | doc_cache/bc44a408....txt | FOUND "height & spread: 15 - 30 ft tall and wide" | ["clemson_hgic"], {.. factsheet/fig/} |
| pomegranate | [10,12] / [8,10] | ncsu_ext_toolbox_punica_granatum (yes) | https://plants.ces.ncsu.edu/plants/punica-granatum/ | yes | doc_cache/ed76558b....txt | FOUND "10 to 12 feet tall and 8 to 10 feet wide" | [that id], {.. punica-granatum/} |
| elderberry | [5,12] / [6,12] | ncsu_ext (yes) | https://plants.ces.ncsu.edu/plants/sambucus-canadensis/ | yes | doc_cache/ff74af56....txt | FOUND "measuring 5 to 12 feet tall" + attributes width 6-12 | ["ncsu_ext"], {.. sambucus-canadensis/} |
| persimmon | [20,30] / [15,25] | ncsu_ext (yes) | https://plants.ces.ncsu.edu/plants/diospyros-kaki/ | yes | doc_cache/0e05b34e....txt | FOUND attributes only "height: 20 ft. 0 in. - 30 ft. 0 in. width: 15 ft. 0 in. - 25 ft. 0 in." | ["ncsu_ext"], {.. diospyros-kaki/} |
| mulberry | [30,60] / [30,50] | ncsu_ext (yes) | https://plants.ces.ncsu.edu/plants/morus-alba/ | yes | doc_cache/5696a1ae....txt | FOUND "50 or 60 feet with an equal spread" + attributes | ["ncsu_ext"], {.. morus-alba/} |
| pawpaw | [15,30] / [15,30] | ncsu_ext (yes) | https://plants.ces.ncsu.edu/plants/asimina-triloba/ | yes | evidence_cache/89feb7e0... (sha differs from record's 3f8ac320); no doc_cache | FOUND attributes "height: 15 ft. 0 in. - 30 ft. 0 in. width: 15 ft. 0 in. - 30 ft. 0 in." | ["ncsu_ext"], {.. asimina-triloba/} |
| lavender | [1,2] / [2,3] | ncsu_ext_lavandula_angustifolia (yes) | https://plants.ces.ncsu.edu/plants/lavandula-angustifolia/ | yes | doc_cache/7c87b066....txt | FOUND "grows up to 2 feet tall and 3 feet wide" + attributes | [that id], {.. lavandula-angustifolia/} |

All 16 records carry a catalog id that exists; all record URLs are document-pathed (none bare host). `verified` date for the
sibling: the record's raw-read date 2026-09-16, or the date the bytes are re-saved into .evidence_cache.

Flags: **apple** (record URL uncited + uncached; the same handbook at the wpcdn host is cited + cached and states the sentence)
and **blueberry** (record URL uncited + uncached; the cited cached PSU page says 4 to 8 ft, not 5 to 8). 14 of 16 have the
sentence in cached text; only lemon and pawpaw have hashed `.evidence_cache` bytes (and those shas differ from the PLA-465
records' shas: different fetches).

Ranges whose low end comes only from the Toolbox attributes block (prose gives just the top): oregano lo 1, sage lo 1,
lavender lo 1, mulberry lo 30 / spread 30-50 (prose "50 or 60 ... equal spread"), persimmon and pawpaw (attributes only).
A quote check must be given the attributes line, not the description sentence, for these.

## Task 3: roster counts (cf1d480d)
- Crops carrying `mature_dimensions_sources` or `mature_dimensions_anchoring_urls`: **0** (no key starting `mature_dimensions` on any crop).
- `mature_height_ft` non-null: **16** (peach, apple, lemon, blueberry, thyme, rosemary, oregano, sage, fig, pomegranate,
  elderberry, persimmon, mulberry, pawpaw, nectarine, lavender).
- `mature_spread_ft` non-null: **14** (the 16 minus apple and lemon).
- Key `mature_height_ft` absent entirely on 7 (the 7 shells: avocado, olive, 5 mushrooms); present-and-null on 105.
