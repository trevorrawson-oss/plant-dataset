# 59 - PLA-10 promote 3: the heights worklist (46 new + 16 backfill = 62)

**Written:** 2026-10-02/03, PLA-10 promote 3 session 1 (UNATTENDED run; nothing here is ruled until Trevor reads it).
**Canonical READ-ONLY:** `31b766e8` (== `LATEST.txt`); no crop record edited, no stage file written. **Checkout:** `main`,
session start HEAD `3475fae` == origin/main; this session's tools commit `ac06c11` (local, unpushed).
**Tools:** `tools/promote_pla10_promote3.py` (the fixed list below is its `NEW_CROPS` + `BACKFILL_CROPS`), T4
`quote_states_ft` (an endpoint is stated by a figure within **0.00005 ft**, inches / 12, in the clause for its own
dimension), T5 (A62 / A59 sibling, both unarmed). Owed in the data commit: `tools/staging/pla10_promote3/HANDOFF.md`.
**Plan:** `docs/kickoffs/58-pla10-promote2-plan.md` §3 (rulings H1-H4, K1-K4 TAKEN), measurements C and D.

**RULED (Trevor, 2026-10-03): every decision row below is TAKEN as recorded in its row** (§1 tie-break, §3, §4).
Two rulings were conditional and were resolved against the data in the rulings commit: **roma** (OSU EC1333 is cited
on roma but NOT hashed; the hashed OSU document is the planting-dates table `ir.library.oregonstate.edu/downloads/
v979v342w`, which states no height, so the fallback applies: Cornell [2,6]) and **mint** (the crop's description is
genus-level "Mint (Mentha)" garden mint and names spearmint "the mild, sweet everyday mint": authored from the
spearmint page with scope recorded; the session-3 reviewer confirms).

Session 2 authors from this file: one stage file per row, `crops/<slug>.json`, every figure cited to the hashed bytes
named here (`tools/.evidence_cache`, MANIFEST rows appended this session, saved_by "PLA-10 promote 3 session 1").

---

## 0. The fetch (53 pages, raw bytes, two user agents, PDFs via pinned pypdf)

Target: every height page plan 58 names that was NOT already hashed: the non-pepper tip-over pages, the backfill pages
(incl. the wpcdn WSU handbook for apple, both PSU blueberry pages for K2), and the D-table pages for the 35
closed-statement crops. **66 pages in all; 13 already hashed; 53 fetched for this promote** (plan 58 said "~30": it
counted tip-over + backfill, not the D-table pages).

| outcome | n | pages |
| -- | -- | -- |
| fetched clean, both UAs byte-identical | 42 | |
| fetched, browser UA only (plain UA 403 / disconnect / differs) | 8 | TAMU EHT-065 (PDF), OSU asparagus news, UMaine 4311e, UMN beans, UMN leeks, Cornell tomato guide (plain: RemoteDisconnected), UW dill (plain differs, browser kept), UC Santa Clara basil |
| fetched only with the Safari header set (`FETCH_UA=safari`) | 2 | Clemson fig (Cloudflare; 403 under browser + plain first), UC Santa Clara lemongrass (403 x2 passes, then ok on a 10 s-delayed safari retry) |
| **429** | **0** | |
| **403 under every agent, recorded, not cited** | **1** | `https://ucanr.edu/sites/mgscc2016/garden-help/herbs/chamomile`: browser 403 / plain 403 (pass 1), browser 403 / plain 403 (safari pass), browser 403 / plain 403 (second safari pass) |
| redirected (final URL recorded in MANIFEST `agents`) | 5 | Clemson `factsheet/fig/` -> `factsheet/figs-how-to-grow-and-care-for-figs-in-south-carolina/` (sentence intact); UMN beans and leeks -> `/garden-and-home/yard-and-garden/gardening-in-minnesota/...`; ISU all-about-beans -> `/how-to/all-about-beans`; EDIS FP623 -> `ask.ifas.ufl.edu/publication/FP623` |

**Changed since the doc-cache text:** of 76 measured quotes (C + D), **73 are byte-present in the fresh hashed bytes**,
2 were unfetchable at check time (lemongrass, since fetched and present; chamomile, 403), and **1 changed**:
cilantro's UW-Madison page (hashed before this session, 2026-10-01) now reads "the foliage grows **1 to 1⁄2 feet**
high, and the flower stems reach 2 to 3 feet" where the doc cache had `12-18" high`. Same value; but `1⁄2` uses
U+2044 FRACTION SLASH, which T4 does not read (decision row D-CIL). No page's height sentence is gone.

**blueberry K2: the FIRST branch applies.** The record's own PSU page fetched (`blueberries-in-the-garden-and-the-kitchen`,
both UAs) and states "this shrub can be **5 to 8 feet tall and wide** at maturity or even larger". So [5,8] / [5,8] is
KEPT and re-hashed; no re-anchor, no PLA-465 value correction; the sibling cites the record's URL (which the crop did
not cite before: it now does, through the sibling). "or even larger" is an open tail on a closed range; recorded, not
a reason to move off the ruling.

---

## 1. The W2 range rule, as these recommendations apply it to heights

Promote 1's W2 (refined) + W6, carried over unchanged in substance:
1. **A closed range beats an open bound or a point** ("up to 4 feet", "3 feet") from another cited page (W2).
2. **One page per value; never a span joined across two pages** (W6). Two clauses of ONE page are fine. Height and
   spread are separate values: each comes from one page, and the two may come from different pages.
3. **TAKEN (2026-10-03): the tie-break between two closed ranges from different pages** (W2 applies first: a closed
   range beats a single figure or a minimum): **(1) scope** (the page names the crop or its habit), **(2) the range the
   crop's own prose already agrees with**, **(3) the NC State Toolbox record**. **Never the union, and never choose a
   range for being narrower.**
4. **TAKEN:** a figure the page ties to a habit (trailing / climbing vs bush) authors null (spec §4.4's peas precedent:
   which habit is grown is a `plant_habit` fact, PLA-12). A single closed range stated for the crop that SPANS habits
   (the tomatoes' det + indet) is authored, recorded as habit-spanning.

---

## 2. The 62 rows

Columns: **page** (hashed; sha prefix), **quote** (norm_text form, verbatim substring of the hashed bytes),
**figure** (what T4 reads: H = height clause, W = width clause, ft), **class**, **proposed** height / spread
(recommendation; DISAGREEMENT rows are decided in §3). "prose" = restatements the stage must adjudicate (S guard).

### 2.1 Tip-over (11)

| # | crop | page | quote | figure | class | proposed H / S | notes |
| -- | -- | -- | -- | -- | -- | -- | -- |
| 1 | bell-pepper | UMD growing-peppers (4fe5a4dd) | "peppers are produced on bushy plants that can reach 3-4 ft. in height." | H 3-4 | CLOSED | [3,4] / null | |
| 2 | jalapeno | same | same | H 3-4 | CLOSED | [3,4] / null | |
| 3 | banana-pepper | same | same | H 3-4 | CLOSED | [3,4] / null | |
| 4 | cayenne-pepper | same | same | H 3-4 | CLOSED | [3,4] / null | H2: page names cayenne |
| 5 | habanero | same | same | H 3-4 | SCOPE-DOUBT (ruled in, H2) | [3,4] / null | page names habanero, never *C. chinense*; reviewer confirms (H2) |
| 6 | broccoli | NCSU basics-of-broccoli-production | "full-grown plants reach about 47 inches tall and 20 inches wide" | H 3.9167; W 1.6667 | CLOSED (point) | [3.9167,3.9167] / [1.6667,1.6667] | H4: quotient to 4 places |
| 7 | brussels-sprouts | NCSU Toolbox brassica-oleracea-brussels-sprouts-group | "the plants can grow 2-4 feet tall and wide on a thick stalk." | HW 2-4 | CLOSED | [2,4] / [2,4] | attrs line agrees (H 2-4) |
| 8 | broad-beans-fava | NCSU Toolbox vicia-faba | "it is a stiffly erect plant that grows 2-6 feet tall" | H 2-6 | CLOSED | [2,6] / null | prose: 7 leaves say "2 to 4 feet" (beginner) / "some to 5 or 6" (seasoned): D-FAVA |
| 9 | dill | UW-Madison dill-anethum-graveolens | "dill plants grow 18 inches to 4 feet tall" | H 1.5-4 | CLOSED | [1.5,4] / null | **H3 TAKEN:** "3 to 5 feet" in description_beginner/_seasoned, container_notes, variety note are `edited` |
| 10 | eggplant | NCSU Toolbox solanum-melongena | "the plant may grow 2 to 4 feet tall and is multi-branched." | H 2-4 | CLOSED | [2,4] / null | attrs agree |
| 11 | cosmos | UF/IFAS gardeningsolutions cosmos | "garden cosmos can reach 3-6 feet" | H 3-6 | DISAGREEMENT (H1 TAKEN) | [3,6] / null | see §3 row 1: NCSU attrs state a CLOSED [2,4] the H1 row did not weigh |

### 2.2 The 35 closed statements (plan 58 §3.2)

| # | crop | page | quote | figure | class | proposed H / S | notes |
| -- | -- | -- | -- | -- | -- | -- | -- |
| 12 | cherry-tomato | Cornell tomato-growing-guide | "height: 2 to 6 feet staked and pruned plants can grow to well over 6 feet tall ... spread: 2 to 6 feet" | H 2-6 (+ open 6); W 2-6 | DISAGREEMENT + habit-spanning | [2,6] / [2,6] | §3 row 2 |
| 13 | beefsteak-tomato | same | same | same | DISAGREEMENT + habit | [2,6] / [2,6] | prose "5 to 6 feet", "6 feet tall or more": agrees (note) |
| 14 | roma-tomato | same | same | same | DISAGREEMENT + habit | **[2,6] / [2,6] (TAKEN, fallback)** | §3 row 2: OSU EC1333 det [3,4] would win on scope, but it is not hashed |
| 15 | grape-tomato | same | same | same | DISAGREEMENT + habit | [2,6] / [2,6] | |
| 16 | heirloom-tomato | same | same | same | DISAGREEMENT + habit | [2,6] / [2,6] | prose "5 to 6 feet tall or more": agrees (note) |
| 17 | tomatillo | NCSU physalis-philadelphica; USU tomatillos (hashed) | "...grow to 3 to 4 feet in height and width"; "tomatillos grow 3-4 feet tall and wide" | HW 3-4 (both) | CLOSED | [3,4] / [3,4] | pages agree; prose "3 to 4 feet tall and wide" agrees |
| 18 | kale | UMaine 4311e stage-1 | "kale is a large plant, often growing to 2.5-3 feet tall." | H 2.5-3 | CLOSED | [2.5,3] / null | |
| 19 | spinach | UMD growing-spinach | "it grows to a height of 8-12 inches." | H 0.6667-1 | CLOSED | [0.6667,1] / null | |
| 20 | green-beans-bush | UMN growing-beans (redirected) | "bush beans are upright plants that do not need support, growing about two feet tall." | H 2 | CLOSED (point) | [2,2] / null | |
| 21 | edamame | ISU all-about-beans (redirected) | "plants are approximately 3 feet tall and do not require support." | H 3 | CLOSED (point) | [3,3] / null | UMN "up to three feet" is open: W2, the point stands |
| 22 | potato | NCSU Toolbox solanum-tuberosum | "height: 1 ft. 0 in. - 2 ft. 0 in. width: 1 ft. 0 in. - 1 ft. 6 in." | H 1-2; W 1-1.5 | CLOSED | [1,2] / [1,1.5] | prose hits are hilling heights (agrees) |
| 23 | sweet-potato | UF gardeningsolutions sweet-potatoes (hashed) | "...about 12 inches in height when situated on the ground." | H 1 (vine run reads as neither) | CLOSED (point) | [1,1] / null | §4.5: 15 ft vine run is not spread |
| 24 | onion | NCSU Toolbox allium-cepa | "height: 1 ft. 0 in. - 1 ft. 6 in. width: 0 ft. 6 in. - 1 ft. 0 in." | H 1-1.5; W 0.5-1 | DISAGREEMENT | [1,1.5] / [0.5,1] | §3 row 3 |
| 25 | okra | UF gardeningsolutions okra | "plant heights vary by cultivar and pruning practices. most fall within the 3-6 foot range" | H 3-6 | CLOSED | [3,6] / null | D-OKRA ("most fall within"); prose "4 to 6 feet (and more)" agrees |
| 26 | celery | USU celery (hashed) | "celery grows to a height of 18 to 24 inches" | H 1.5-2 | CLOSED | [1.5,2] / null | prose hits are harvest-stage stalk heights |
| 27 | artichoke | Cornell globe-artichokes guide (hashed) | "height: 3 to 6 feet spread: 2 to 4 feet" | H 3-6; W 2-4 | DISAGREEMENT | [3,6] / [2,4] | §3 row 4 |
| 28 | asparagus | OSU news asparagus | "asparagus foliage can reach 5 to 6 feet in height" | H 5-6 | CLOSED | [5,6] / null | fern height; spear heights in prose are harvest-stage |
| 29 | leek | UMN growing-leeks (redirected) | "plants grow two to three feet tall, and can have a width of two inches." | H 2-3 (W 0.1667 = shaft) | CLOSED | [2,3] / **null** | the "width" is shaft diameter: never a spread |
| 30 | basil | UC Santa Clara MG basil | "size: 8 to 24 inches high, 8 to 12 inches wide, depending on variety" | H 0.6667-2; W 0.6667-1 | DISAGREEMENT | [0.6667,2] / [0.6667,1] | §3 row 5 |
| 31 | cilantro-coriander | USU cilantro (hashed) | "plants grow to 1-3 feet tall" | H 1-3 | DISAGREEMENT | **[1,3] / null (TAKEN)** | §3 row 6; D-CIL: UW `1 1⁄2` is a known T4 reader gap |
| 32 | chives | NCSU Toolbox allium-schoenoprasum | "height: 1 ft. 0 in. - 1 ft. 6 in. width: 1 ft. 0 in. - 1 ft. 5 in." | H 1-1.5; W 1-1.4167 | DISAGREEMENT | [1,1.5] / [1,1.4167] | §3 row 7 |
| 33 | mint | NCSU Toolbox mentha-spicata | "growing quickly 1 to 2 feet high and wide" | HW 1-2 | SCOPE-DOUBT | **[1,2] / [1,2] (TAKEN, conditional met)** | D-MINT: spearmint page, scope recorded; session-3 reviewer confirms |
| 34 | lemongrass | NCSU Toolbox cymbopogon-citratus (hashed) | "height: 2 ft. 0 in. - 4 ft. 0 in. width: 2 ft. 0 in. - 3 ft. 0 in." | H 2-4; W 2-3 | DISAGREEMENT | [2,4] / [2,3] | §3 row 8; prose "3 to 6 feet" x2 must be edited |
| 35 | marigold | NCSU Toolbox tagetes | "height: 1 ft. 0 in. - 4 ft. 0 in. width: 0 ft. 6 in. - 1 ft. 0 in." | H 1-4; W 0.5-1 | DISAGREEMENT | [1,4] / [0.5,1] | §3 row 9 |
| 36 | nasturtium | NCSU Toolbox tropaeolum-majus | "height: 1 ft. 0 in. - 10 ft. 0 in. width: 1 ft. 0 in. - 3 ft. 0 in." | H 1-10; W 1-3 | CONDITIONAL (habit-tied) | **null / null (TAKEN: stage null)** | D-NAST |
| 37 | sunflower | NCSU Toolbox helianthus-annuus | "height: 1 ft. 6 in. - 10 ft. 0 in. width: 1 ft. 6 in. - 3 ft. 0 in." | H 1.5-10; W 1.5-3 | DISAGREEMENT | [1.5,10] / [1.5,3] | §3 row 10 |
| 38 | borage | UC Marin MG borage (hashed) + NCSU borago-officinalis | "borage is an exuberant annual that grows two to three feet tall"; NCSU "width: 1 ft. 0 in. - 1 ft. 4 in." | H 2-3; W 1-1.3333 | DISAGREEMENT | [2,3] / [1,1.3333] | §3 row 11 |
| 39 | calendula | UF/IFAS FP087 | "height: 1 to 2 feet spread: 1 to 2 feet" | H 1-2; W 1-2 | DISAGREEMENT | [1,2] / [1,2] | §3 row 12 |
| 40 | zinnia | UF/IFAS FP623 (redirected) | "height: 1 to 3 feet spread: 1 to 2 feet" | H 1-3; W 1-2 | DISAGREEMENT | [1,3] / [1,2] | §3 row 13 |
| 41 | chamomile | UC Santa Clara MG chamomile: **403, NOT HASHED** | (doc cache only) "size: 1 to 2 feet tall, 12 to 14 inches wide" | (H 1-2; W 1-1.1667) | DISAGREEMENT + UNFETCHABLE | **TAKEN: hunt first, then null** | §3 row 14 |
| 42 | sweet-alyssum | UW-Madison sweet-alyssum + NCSU lobularia-maritima | "sweet alyssum grows 3-9 inches tall with a wider spread."; NCSU "width: 0 ft. 6 in. - 1 ft. 0 in." | H 0.25-0.75; W 0.5-1 | DISAGREEMENT | [0.25,0.75] / [0.5,1] | §3 row 15 |
| 43 | echinacea | NCSU Toolbox echinacea-purpurea | "it may grow 3 to 4 feet tall" | H 3-4 | DISAGREEMENT | [3,4] / null | §3 row 16 |
| 44 | bee-balm | NCSU Toolbox monarda-didyma (hashed) | "height: 2 ft. 0 in. - 4 ft. 0 in. width: 2 ft. 0 in. - 3 ft. 0 in." | H 2-4; W 2-3 | CLOSED | [2,4] / [2,3] | same page prose "can reach a height of 4 feet" agrees |
| 45 | viola | NCSU Toolbox viola-x-wittrockiana (hashed) | "it grows 6 to 9 inches in height and 9 to 12 inches in width." | H 0.5-0.75; W 0.75-1 | DISAGREEMENT + SCOPE-DOUBT | [0.5,0.75] / [0.75,1] | §3 row 17 |
| 46 | sweet-pea | NCSU Toolbox lathyrus-odoratus | "height: 3 ft. 0 in. - 8 ft. 0 in. width: 2 ft. 0 in. - 3 ft. 0 in." | H 3-8; W 2-3 | CONDITIONAL (habit-tied) | **null / null (TAKEN: stage null)** | D-SPEA |

### 2.3 PLA-465's 16: the backfill (values unchanged; K3 re-hash; the record keeps its historical sha)

Every row's figure is stated by a quote on FRESH hashed bytes fetched this session (or already hashed); both endpoints
of every authored value are stated (the K4 crops through the Toolbox attributes lines, which T4 reads).

| # | crop | page (sibling anchor) | quote(s) | figure | class | H / S (kept) |
| -- | -- | -- | -- | -- | -- | -- |
| 47 | peach | NCSU prunus-persica | "the tree will grow quickly to 15-25 feet tall and wide" | HW 15-25 | CLOSED (backfill) | [15,25] / [15,25] |
| 48 | nectarine | NCSU prunus-persica (the record's URL) | same | HW 15-25 | CLOSED (backfill) | [15,25] / [15,25] |
| 49 | apple | **wpcdn** WSU handbook PDF (K1 re-point; the record's s3 URL stays in the record) | "10'-14' tall" (in "m 26-semi-dwarf habit, 10'-14' tall") | H 10-14 | CLOSED (backfill, K1) | [10,14] / null |
| 50 | lemon | EDIS HS402 (hashed, 15801f6d) | "trees may reach 10-20 ft (3.1-6.1 m) in height" | H 10-20 | CLOSED (backfill) | [10,20] / null |
| 51 | blueberry | PSU blueberries-in-the-garden-and-the-kitchen (the record's URL) | "this shrub can be 5 to 8 feet tall and wide at maturity or even larger" | HW 5-8 | CLOSED (backfill, **K2 branch 1: kept**) | [5,8] / [5,8] |
| 52 | thyme | NCSU thymus-vulgaris | "about 6 to 12 inches high and 6 to 16 inches wide" | H 0.5-1; W 0.5-1.3333 | CLOSED (backfill) | [0.5,1] / [0.5,1.3333] |
| 53 | rosemary | NCSU salvia-rosmarinus | "the shrub grows from 4 to 5 feet tall"; "width: 3 ft. 0 in. - 4 ft. 0 in." | H 4-5; W 3-4 | CLOSED (backfill) | [4,5] / [3,4] |
| 54 | oregano | NCSU origanum-vulgare | "height: 1 ft. 0 in. - 3 ft. 0 in."; "width: 1 ft. 0 in. - 2 ft. 0 in." (K4) | H 1-3; W 1-2 | CLOSED (backfill, K4) | [1,3] / [1,2] |
| 55 | sage | NCSU salvia-officinalis | "height: 1 ft. 0 in. - 2 ft. 0 in."; "up to 2 feet tall and 2 to 3 feet wide" (K4) | H 1-2; W 2-3 | CLOSED (backfill, K4) | [1,2] / [2,3] |
| 56 | fig | Clemson HGIC fig (record URL; now redirects, sentence intact) | "height & spread: 15 - 30 ft tall and wide" | HW 15-30 | CLOSED (backfill) | [15,30] / [15,30] |
| 57 | pomegranate | NCSU punica-granatum | "10 to 12 feet tall and 8 to 10 feet wide" | H 10-12; W 8-10 | CLOSED (backfill) | [10,12] / [8,10] |
| 58 | elderberry | NCSU sambucus-canadensis | "measuring 5 to 12 feet tall"; "width: 6 ft. 0 in. - 12 ft. 0 in." | H 5-12; W 6-12 | CLOSED (backfill) | [5,12] / [6,12] |
| 59 | persimmon | NCSU diospyros-kaki | "height: 20 ft. 0 in. - 30 ft. 0 in." / "width: 15 ft. 0 in. - 25 ft. 0 in." (K4) | H 20-30; W 15-25 | CLOSED (backfill, K4) | [20,30] / [15,25] |
| 60 | mulberry | NCSU morus-alba | "height: 30 ft. 0 in. - 60 ft. 0 in." / "width: 30 ft. 0 in. - 50 ft. 0 in." (K4; the prose "50 or 60 feet with an equal spread" reads as NEITHER under T4) | H 30-60; W 30-50 | CLOSED (backfill, K4) | [30,60] / [30,50] |
| 61 | pawpaw | NCSU asimina-triloba (hashed, 89feb7e0) | "height: 15 ft. 0 in. - 30 ft. 0 in." / "width: 15 ft. 0 in. - 30 ft. 0 in." (K4) | H 15-30; W 15-30 | CLOSED (backfill, K4) | [15,30] / [15,30] |
| 62 | lavender | NCSU lavandula-angustifolia | "height: 1 ft. 0 in. - 2 ft. 0 in." / "width: 2 ft. 0 in. - 3 ft. 0 in." (K4) | H 1-2; W 2-3 | CLOSED (backfill, K4) | [1,2] / [2,3] |

**Totals by class (62):** CLOSED 21 new + 16 backfill = **37**; DISAGREEMENT **21** (1 already ruled: cosmos H1);
SCOPE-DOUBT **2** (habanero, ruled in by H2; mint); CONDITIONAL **2** (nasturtium, sweet-pea: stage null).
Recommended to **stage null: 3** (nasturtium, sweet-pea, and chamomile unless a page is hashed in session 2), so the
recommendation authors **43 new heights** (+ 16 backfilled = 59 crops carrying the sibling pair). Spreads recommended
on 23 new crops.

---

## 3. The 21 disagreement decision rows (W2 range rule, §1) -- ALL TAKEN 2026-10-03

| # | crop(s) | the pages | recommendation | why |
| -- | -- | -- | -- | -- |
| 1 | cosmos | UF [3,6]; NCSU prose "up to 4 feet" (open); **NCSU attrs "height: 2 ft. 0 in. - 4 ft. 0 in." (closed)** | **TAKEN: UF [3,6] stands, now by tie-break (2)**: the crop's own description says 3 to 6 ft. **Corrected premise recorded:** NCSU states a closed [2,4], so H1's "no lower bound" was wrong; the outcome holds. | H1 was ruled on "NCSU has no lower bound"; the fresh bytes show NCSU's attributes line does state a closed [2,4]. Rule 3: the crop's prose ("roughly 3 to 6 ft"; Sensation 3 to 4 ft) agrees with UF, so UF still wins on fewest edits. **Trevor: H1's premise was incomplete; confirm it stands.** |
| 2 | cherry, beefsteak, roma, grape, heirloom tomato | NCSU [1,10] / [1,4] (prose + attrs); Cornell "height: 2 to 6 feet ... spread: 2 to 6 feet" | **TAKEN: cherry, grape, heirloom, beefsteak: Cornell [2,6] / [2,6], recorded as HABIT-SPANNING (det and indet in one range)**: closed, stated for tomatoes; NCSU's [1,10] is wider than useful. **No support-entry height override** (plan 58 §2.4: no page ties a height to a support form). **roma: OSU determinate [3,4] by tie-break (1) if cited AND hashed; EC1333 is cited but not hashed, so Cornell [2,6] / [2,6].** | Both closed; NCSU's 1-10 spans dwarf to unpruned indeterminate, wider than any tomato as grown on its default (rule 3, scope). Cornell's is one unconditional statement for the garden tomato (rule 4 does not force null). Prose ("5 to 6 feet", "6 feet or more") sits at Cornell's high end and its "well over 6 feet" clause: `agrees`. **Alt for roma:** OSU EC1333 "determinate cultivars tend to be fairly short (3 to 4 feet tall)" if Trevor wants roma on its habit (needs that page hashed). |
| 3 | onion | NCSU [1,1.5] / [0.5,1]; Cornell scene4983 [1,3] / [0.5,1] | **TAKEN: NCSU [1,1.5] / [0.5,1].** | The bulb crop's foliage height; Cornell's 3 ft high end reaches seed-stalk height. Spreads agree. NCSU species record (rule 3). |
| 4 | artichoke | Cornell [3,6] / [2,4]; TAMU EHT-065 "plants can reach 3 feet in height and w idth" (point; PDF spacing) | **TAKEN: Cornell [3,6] / [2,4].** | Rule 1: a closed range beats a point. (UMaine/VT 4-5 ft and EDIS "more than 4 feet" are other pages, not in this promote's evidence.) |
| 5 | basil | UC Santa Clara [0.6667,2] / [0.6667,1] ("depending on variety"); UC Sonoma sweet basil "2-21⁄2 ft" (type-specific) | **TAKEN: Santa Clara [0.6667,2] / [0.6667,1].** | Scope: the crop covers many basils; Sonoma's is sweet basil only, and its `21⁄2` is unreadable by T4 anyway. |
| 6 | cilantro-coriander | UW foliage "1 to 1⁄2 feet" / flower stems 2-3 ft (**changed page**, D-CIL); USU "plants grow to 1-3 feet tall" | **TAKEN: USU [1,3] / null.** Do not extend T4 for one fraction-slash character: UW's "1 to 1⁄2 feet" (U+2044) is recorded as a **known reader gap**; it becomes a T4 change only if a second page needs it. | Both are closed; UW's foliage figure is the better meaning for a leaf crop but its hashed text uses U+2044 (`1 1⁄2`), which T4 cannot read without a tools change. USU's is one whole-plant statement, hashed and readable. **Alt:** UW foliage [1,1.5] after a T4 fraction extension (TDD + harness) in session 2. |
| 7 | chives | NCSU [1,1.5] / [1,1.4167]; Illinois "about 10-12 inches tall" | **TAKEN: NCSU [1,1.5] / [1,1.4167].** | Both closed; NCSU is the species record and gives both dims (rule 3). Variety prose 8-14 in / 18-20 in: `agrees` (variety-level). |
| 8 | lemongrass | NCSU [2,4] / [2,3]; UC Santa Clara "size: 3 to 4 feet tall, 2 to 3 feet wide" (fetched on retry) | **TAKEN: NCSU [2,4] / [2,3]; the prose "3 to 6 feet" (description_seasoned, growth_stages[2]) is `edited` to the authored figure.** | Both closed; spreads agree; prose "3 to 6" exceeds both pages' 4 ft (the H3 pattern), so an edit is owed either way (one edit each); tie goes to the Toolbox record (rule 3). **Alt:** Santa Clara [3,4] keeps the prose's 3 ft floor. |
| 9 | marigold | NCSU tagetes (genus) prose + attrs [1,4] / [0.5,1]; Clemson 6 in - 3 ft; UF 1-2 ft | **TAKEN: NCSU [1,4] / [0.5,1], recorded "cultivar-spanning (dwarf to giant)".** | One page, two clauses agreeing; genus page matches the crop's scope (erecta + patula). |
| 10 | sunflower | NCSU prose "grow 2 to10 feet tall"; NCSU attrs [1.5,10] / [1.5,3] (one page, two figures) | **TAKEN: NCSU attrs [1.5,10] / [1.5,3], recorded "cultivar-spanning (dwarf to giant)".** | W6 allows either clause of one page; the attributes line carries both dims in one statement (the K4 convention). Prose "giants over 10 feet" is variety-level: `agrees`. **Alt:** prose [2,10] for height. |
| 11 | borage | NCSU attrs [1.5833,3.1667] / [1,1.3333]; UC Marin "grows two to three feet tall" | **TAKEN: height UC Marin [2,3]; spread NCSU [1,1.3333]** (two values on two pages: W6 permissive allows it). | Rule 3: the crop's prose ("about 2 to 3 ft tall") agrees with UC Marin; spread from the one page that states it. Prose "1 to 2 ft wide" vs NCSU 1-1.33: adjudicate (`agrees` at the low end, or edit). **Alt:** NCSU for both. |
| 12 | calendula | UF FP087 [1,2] / [1,2]; NCSU [1,2] / [1,2]; USU "8 to 24 inches" | **TAKEN: FP087 [1,2] / [1,2].** | FP087 and NCSU agree exactly; USU's low end is the only dissent. |
| 13 | zinnia | UF FP623 dims [1,3] / [1,2] (same page also "as short as 6 inches or as tall as 3 feet"); Clemson 6 in - 4 ft | **TAKEN: FP623 dims [1,3] / [1,2].** | One page's dimension statement; prose "cut-flower types reaching 3 to 4 ft" is type-level: adjudicate (`agrees` as a type note, or edit to 3). |
| 14 | chamomile | UC Santa Clara "size: 1 to 2 feet tall, 12 to 14 inches wide" (**403, unhashed**); UW "up to 2 feet tall" (open); NCSU matricaria dims (malformed width; not hashed) | **TAKEN: hunt first** (retry UC Santa Clara with a back-off; fetch NCSU's matricaria page), **then null if nothing hashes.** A hashed Santa Clara page gives [1,2] / [1,1.1667]. | Never cite unhashed text; the only hashed statement is open (UW). Hunt first (memory: hunt before downgrading): session 2 retries Santa Clara and fetches NCSU matricaria (height 1'1"-2'6" per plan 58 D). |
| 15 | sweet-alyssum | NCSU attrs [0.25,0.8333] / [0.5,1]; UW "grows 3-9 inches tall with a wider spread" | **TAKEN: Height UW [0.25,0.75]; spread NCSU [0.5,1].** | Rule 3: the crop's prose says "just 3 to 9 inches tall" (UW, no edit). Spread from the one page with a figure. |
| 16 | echinacea | NCSU prose + attrs [3,4]; PSU "24-36 inches in height"; (UF 1-3, Clemson 2-3.5 not in evidence) | **TAKEN: NCSU [3,4] / null; the prose "2 to 4 feet" is `edited` to the authored figure.** | Species record, internally consistent. Neither page matches the prose's 2-4; under NCSU the "2" is below the cited floor: recommend `edited` to "3 to 4 feet" (H3 pattern). **Alt:** PSU [2,3] conflicts with prose's 4. |
| 17 | viola | NCSU pansy page: prose "6 to 9 inches in height and 9 to 12 inches in width"; attrs "height: 0 ft. 4 in. - 0 ft. 9 in." | **TAKEN: NCSU prose [0.5,0.75] / [0.75,1]**, scope recorded. | One statement covering both dims; W6 allows either clause. SCOPE: every statement is pansy (*V. x wittrockiana*); the crop covers cornuta / tricolor too (W3: accept with scope recorded, or null). |

Count: row 1 (cosmos) + row 2 (five tomatoes) + rows 3-17 (fifteen crops) = **21**, plan 58's list with apricot
excluded (woody; PLA-465 not reopened) and cosmos added (its H1 row is ruled but its premise moved, row 1).

## 4. Other decision rows (not disagreements)

| id | crop | question | ruling (TAKEN 2026-10-03 unless marked) |
| -- | -- | -- | -- |
| D-K2 | blueberry | Which K2 branch applied? | **Branch 1 applied: kept [5,8] / [5,8], re-hashed** on the record's PSU page ("5 to 8 feet tall and wide at maturity or even larger"). No value correction. |
| D-CIL | cilantro | UW page changed since the doc cache (`12-18"` -> `1 to 1⁄2 feet`). | Recorded as changed, not gone. **TAKEN: USU; UW's U+2044 is a known T4 reader gap, no T4 change unless a second page needs it.** |
| D-CHA | chamomile | Santa Clara page 403 under every agent, 3 passes. | **TAKEN: hunt first (back-off retry; NCSU matricaria), then null** (§3 row 14). |
| D-FAVA | broad-beans-fava | 7 prose leaves say 2-4 ft (beginner) against cited 2-6. | **TAKEN: `agrees`**: "2 to 4" is narrower than [2,6] and does not contradict it. No edit. |
| D-OKRA | okra | "most fall within the 3-6 foot range" is a typical range, not a bound. | **TAKEN (as recommended): author [3,6]**: a typical range is what a `[lo, hi]` height means everywhere else. |
| D-NAST | nasturtium | NCSU 1-10 ft spans bush and climbing forms; the crop's default is unsupported. | **TAKEN: null** (both habits in one figure: trailing / bush; the peas precedent). |
| D-SPEA | sweet-pea | NCSU "if allowed to climb ... up to 8 feet. if grown as a bush ... 3 foot" (attrs 3-8). | **TAKEN: null** (the page ties each figure to a habit: climbing / bush; the peas precedent). |
| D-MINT | mint | NCSU page is spearmint; the crop covers spearmint + peppermint. | **TAKEN, conditional:** author from the spearmint page with scope recorded IF the crop's description centers on spearmint or garden mint, else null. **Condition met** (description is genus-level garden mint, spearmint named the everyday mint): author [1,2] / [1,2]; the session-3 reviewer confirms. HABANERO: in scope by H2, as already ruled. |
| D-LEEK | leek | "a width of two inches" reads as W 0.1667 under T4. | **TAKEN (as recommended): spread null**: shaft diameter is not canopy spread. |
| D-H3 | dill | prose "3 to 5 feet" x4 above the cited 4 ft. | H3 TAKEN: `edited` to the cited figure. |
| D-T4 | (tooling) | T4 cannot read U+2044 fractions (`1 1⁄2`, `2-21⁄2`). | **TAKEN: no T4 change.** A second page needing U+2044 is the trigger. |

## 5. What session 2 does (Trevor, 2026-10-03: session 2's prompt is this worklist)

1. Stage the 62 per the ruled rows: one `crops/<slug>.json` per row, **one EVIDENCE row per (field, source)** against the
   hashed shas, a field_addition record on every authored new crop, every restatement adjudicated (the clean synthetic
   run found 89 scanner hits across the fixed list; the TAKEN edits are dill x4 (H3), lemongrass x2, echinacea x1;
   fava `agrees`).
2. Hunt for chamomile (Santa Clara retry, NCSU matricaria fetch) before staging it null.
3. `promote_pla10_promote3.py --check` clean (it refuses until all 62 are staged); staging commit, **report before
   committing**.
4. Session 3: independent source-truth review, gauntlet, the HANDOFF.md items, data commit, state trio.
