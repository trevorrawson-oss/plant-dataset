# Asparagus harvest starts — the re-sourcing sweep, and why the gap does not close

**Date:** 2026-07-27
**Scope:** `docs/2026-07-27-state-of-play-and-next-steps.md` §2a — re-open the 20 asparagus cells
carrying `harvest_resolution_method: harvest_sourced_duration_modeled_start`, on the theory that
county Master Gardener sources are T1 and were being wrongly discounted.
**Canonical at time of sweep:** `0da1d234` (`origin/main` `0c6c229`). **No canonical write.**
**Method:** raw bytes only — `urllib` + `pypdf` text or tag-stripped HTML, per the standing rule
that WebFetch summaries of PDFs are not sourcing. Search-engine summaries were treated as leads,
never as evidence; every claim below was read in the fetched document.

---

## 0. The result, stated first

**The premise was right and the conclusion does not follow.** County MG sources *are* T1, they *were*
being wrongly discounted, and they are *full* of asparagus harvest guidance. But **none of it is a
start date.** Eighteen documents were fetched and read across eight states and five source classes.

**Not one home-garden source publishes a regional asparagus harvest START month.**

Every one publishes the same two things instead:

1. **DURATION in weeks, ramped by bed age** — which the dataset already has, well sourced, roster-wide.
2. **A STOP rule** — either a date (`USU`: "in most areas, stop harvest by early to mid-June") or,
   far more commonly, a **biological rule**: stop when the spears thin below pencil diameter.

The only start dates that exist are in **commercial production** publications, and they are
market-forced, which the asparagus arc had already ruled out for the early end.

So §2a's gap is not a sourcing-effort gap that more looking will close. **It is a category error in
the field:** `harvest` asks for a start month that the home-garden literature deliberately does not
produce, because the start is a soil-temperature emergence event the gardener observes, not a
calendar date an extension office can publish.

---

## 1. What was fetched, and what each one actually said

Grouped by what the document turned out to be. Every row was read raw.

### 1a. Regional planting calendars — carry PLANTING dates, never harvest

| source | geography | asparagus mentions | verdict |
|---|---|---|---|
| `unlv_mg_svn` (Vegetable Planting Guide for Southern Nevada) | nevada z8-10 | 1 | Crop-name cell in a planting grid. PDF extraction collapses the E/M/L month markers, so even the *planting* months are not safely readable from text. **No harvest.** |
| `usu_washco_dates` (Washington County spring planting dates) | utah_dixie z8 | 18 | All planting: "rhubarb, asparagus (crowns)", "asparagus (starts)". **No harvest.** |
| `wsu_em051e` (Home Vegetable Gardening in Washington) | pnw z8/z9 | 10 | Seed depth / spacing / days-to-maturity tables and a planting calendar row "Asparagus, Crown". **No harvest.** |
| `vce_426_331` (Virginia Coop. Ext. 426-331) | mid_atlantic z7/z8 | 7 | Planting by zone: z6 "April 1-May 1", z7a "March 20-April 20", z7b "March 10-April 10", z8 "Feb 15-April 1". Footnote: "Do not harvest asparagus in first year." **No harvest window.** |
| `uga_ext_c943_calendar` (UGA C943 Vegetable Garden Calendar) | se_gulf | **0** | Does not cover asparagus at all. |

> **This confirms the state-of-play doc's suspicion with evidence.** VCE's *planting* rows for
> zones 7-8 (`March 20-April 20`, `Feb 15-April 1`) are near-identical to the pre-fix *harvest*
> strings that were sitting on the mid-Atlantic cells. The old values were almost certainly read
> off a crown-planting table. The correction already shipped; this is the receipt.

### 1b. Documents that do not mention the crop — the `unr_fs0261` shape, caught mechanically

| source | asparagus mentions | verdict |
|---|---|---|
| `auburn_aces` — "Simple Guide for **Harvesting** Popular Crops" | **0** | Title is a perfect match for the claim. Document contains no asparagus. Would have been a fabrication-class citation. |
| UNR PubID 3017 — Moapa & Virgin Valleys | 8 | Variety/yield note only ("a significant harvest can be achieved if vigorous all-male roots are used"). **No window of any kind.** |

Both were surfaced by search as promising Nevada/Alabama asparagus sources. Both fail on contact.
This is the fourth and fifth instance of the pattern that produced asparagus's four bad citations:
**a real T1 document from a real land-grant institution that does not carry the claim.**

### 1c. Crop-specific home-garden publications — DURATION and a STOP, no start

| source | geography | what it actually publishes |
|---|---|---|
| `USU` Asparagus in the Garden (Drost, rev. 2020) | Utah | yr3 "up to 4 weeks", yr4 "6 weeks", yr5+ "up to 8 weeks"; **"In most areas, stop harvest by early to mid-June."** |
| WSU / Yakima Valley MG (Steen) | E. Washington | 3 wk → 4-6 wk → 6-8 wk. No months. |
| UC MG **statewide** | California | "harvest lightly for 3 to 4 weeks the second year"; "in their fourth season, may be harvested for 6 to 10 weeks per year". No months. |
| UC MG **Sonoma** | ca_north_coast | 2-3 wk first harvest, "continuing for 4-8 weeks"; **stop rule: "when new spears begin to thin to less than one-half inch in diameter, stop harvesting."** No months. |
| UC MG **Marin** | ca_north_coast | yr2 "lightly for two weeks", "years two to three you can harvest for eight weeks as spears emerge". No months. |
| UC MG **Santa Clara** | ca coastal | "harvest shoots for a few weeks in the **early spring** as new ones emerge". Closest thing to a start in the entire sweep, and it is a season, not a month. |
| `UGA C1026` Home Garden Asparagus | se_gulf | yr2 "about three weeks", yr3-4 "one month", then "six to eight weeks". Notes asparagus "will be one of the first crops in the spring to harvest". No months. |
| `Clemson HGIC` Asparagus | se_gulf / mid_south | "harvest lightly in the third or fourth year for three to four weeks". No months. |
| `MSU State` Asparagus | se_gulf | "harvest can begin the third year"; young beds "2 to 3 weeks"; established "up to 8 weeks"; **stop rule: "when the diameter of most of the spears drops to the size of a pencil, stop harvest for the year."** No months. |

### 1d. Commercial production publications — the ONLY source of start dates, and they are market-forced

| source | what it publishes |
|---|---|
| `ucanr_pub7234` — Asparagus Production in California | The one document with a district start table: **southern desert valleys "December to early April (main season) or in October if the market is favorable"**; **Delta "late February through May"**; **Central Coast "March to mid-June"**; southern Central Coast "summer harvest from mid-July through September". Also: "normally harvested once a year over an 8- to 10-week period"; "a full cutting season (60-75 days) may begin the fourth year after planting." |
| `ucce_imperial_lowdesert` | "Production and harvesting is for an **early market**, from Mid-January through Mid-April"; "harvest starts in January, most fields will be cut every other day for 60 days." |

The tell is in the documents themselves: *"if the market is favorable"*, *"for an early market"*.
These are forcing decisions, not phenology. The asparagus arc already ruled the late-February Delta
start commercial-only and set the home bed to March; the same reasoning voids the December desert
start and the January Imperial start for home use.

---

## 2. The one case where 7234 could legitimately extend, and why it still should not

Pub 7234's `Central Coast: March to mid-June` is a real, geography-specific, published window with
no market-forcing tell, and March is exactly where the home-bed start was already ruled to sit.

It is tempting for the five coastal California gap cells. **It does not fit them.** UC's "Central
Coast" is Monterey / Santa Cruz / San Luis Obispo. Our `ca_north_coast` is *"California: North &
North Coast"* (Sonoma / Marin / Mendocino) and `ca_south_coast` is *"California: South Coast"*
(Los Angeles / San Diego). Neither is the Central Coast.

Applying it anyway would produce a cell that is *unsourced in exactly the way it is now, but wearing
a citation* — which is strictly worse, because a bad citation looks verified. That is the §5 tier-C
defect shape, and it is the specific error `ca_interior` z9 shipped with.

**Left unsourced deliberately.** The correct home for 7234's Central Coast line is a future
`ca_central_coast` region, if one is ever cut.

---

## 3. What this changes

### 3.1 The gap is honest and should be formally accepted, not chased

Hardening kickoff item 2 offers "re-source **or formally accept**". This sweep is the evidence for
**accept**. The 20 `harvest_sourced_duration_modeled_start` cells are not under-researched; they are
asking the literature for a value it does not publish. `harvest_resolution_method` already records
the distinction honestly and per-cell, which is the right behavior — it should stay, and the
"re-openable" note in §2a should be closed with this document as the reason.

### 3.2 The stop rule is the sourced, portable datum — and the dataset does not carry it

This is the sweep's most actionable finding. **Every** source that says anything about ending the
harvest converges on the same rule, independently, across eight states:

> stop when the spears thin below pencil diameter (Sonoma: below half an inch)

`MSU State`, `Sonoma MG`, `UGA C1026`, `Alameda MG` (already quoted in `LATEST.txt`), `UC MG`, and
UC ANR 7234's carbohydrate rationale all state it. It is the single most sourced, most portable and
most useful piece of asparagus harvest guidance in the literature — it is what actually protects the
crown, it is what makes the duration numbers safe, and it works in every region without a start date.

**The dataset encodes the duration numbers and not the rule that governs them.** `harvest_ramp_weeks`
publishes "8-10 weeks" with no statement that the real instruction is *"8-10 weeks **or** until spears
go thin, whichever comes first"* — which is how every source phrases it, and which is what a grower in
an unsourced-start cell actually needs.

Recommended: a crop-level `harvest_stop_rule` (dual-register prose + the diameter threshold),
proposed as a field-addition register entry alongside row 26. Cheap, T1-dense, and it converts the
weakest cells from "a month we modeled" into "a rule the sources actually state."

### 3.3 The model may be inverted for a subset

For cells where a **date** stop is sourced (USU's "early to mid-June" covers Utah, and by extension
`utah_dixie` z8 with a caveat about St. George running earlier than the Wasatch Front), a
**sourced stop + sourced duration → derived start** is better founded than today's
**modeled start + sourced duration**. That is a genuine model improvement and it deserves its own
`harvest_resolution_method` value rather than being folded silently into the sourced bucket.

Not proposed for this pass: it changes field semantics, and the roster must be stable
(artichoke is mid-cert) before anything touches the column.

---

## 4. Sources fetched (18)

All read raw. Reproduce with `srcfetch.py` (session scratchpad) or any `urllib` + `pypdf` pair.

1. `unlv.edu/.../CampusLife_Planting-Calendar-LasVegas.pdf` — Southern Nevada MG planting guide
2. `extension.usu.edu/washington/files/planting-dates-spring.pdf` — USU Washington County
3. `aces.edu/blog/.../simple-guide-for-harvesting-popular-crops/` — Alabama (0 asparagus)
4. `s3.wp.wsu.edu/.../Home-Vegetable-Gardening-in-Washington.pdf` — WSU EM051E
5. `pubs.ext.vt.edu/426/426-331/426-331.html` — VCE 426-331
6. `fieldreport.caes.uga.edu/publications/C943/...` — UGA C943 (0 asparagus)
7. `s3.wp.wsu.edu/.../04-17-GrowingAsparagus-Steen.pdf` — Yakima Valley MG
8. `extension.usu.edu/yardandgarden/research/asparagus-in-the-garden` — USU (Drost)
9. `my.ucanr.edu/repository/fileaccess.cfm?article=54042` — UC ANR Pub 7234
10. `ucanr.edu/repository/a/?a=161158` — UCCE Imperial, Low Desert
11. `ucanr.edu/site/mg-sonoma/asparagus` — UC MG Sonoma
12. `ucanr.edu/site/uc-marin-master-gardeners/document/asparagus` — UC MG Marin
13. `ucanr.edu/site/uc-master-gardeners-santa-clara-county/asparagus` — UC MG Santa Clara
14. `ucanr.edu/program/uc-master-gardener-program/asparagus` — UC MG statewide
15. `extension.uga.edu/publications/detail.html?number=C1026` — UGA C1026
16. `hgic.clemson.edu/factsheet/asparagus/` — Clemson HGIC
17. `extension.msstate.edu/lawn-and-garden/vegetable-gardens/asparagus` — MSU State
18. `extension.unr.edu/publication.aspx?PubID=3017` — UNR Moapa/Virgin Valleys (no window)

**Two new catalog-worthy T1 sources** if §3.2 proceeds: `UGA C1026` and `MSU State asparagus`
(both crop-specific, both carry the ramp, MSU carries the stop rule verbatim).
Neither is in `source_catalog` today.
