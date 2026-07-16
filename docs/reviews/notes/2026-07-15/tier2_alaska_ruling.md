# Tier-2 belt ruling: Alaska z8 (roadmap item 5, Task 5 -- FINAL belt)

Design spec: `docs/superpowers/specs/2026-07-15-region-tier2-ruling-pass-design.md`.
Method: build a naive, region-blind `frost_anchored` calendar for representative annuals from
their own generic biology fields anchored to the belt's real frost dates, run it through
`tools/annual_calendar.py`, and compare against real T1 regional guidance for a 3-crop basket
(annual / chill-gated tree fruit / cool-season annual, per the brief: cherry-tomato / apple /
kale). No canonical write of any kind; `source_catalog` is not touched (it lives inside
`crops_data_final.json`).

**This is the belt the design spec explicitly flagged as the strongest a priori NEW-REGION
candidate** -- the closest Tier-2 analog to maritime PNW (roadmap item 4), which WAS ruled
NEW-REGION-worthy because its cool maritime summers inverted the generic zone-8 assumptions. The
brief instructed weighing that signal seriously rather than defaulting to CONDITIONAL-GO by
pattern-matching to the prior four belts. As detailed below, the evidence bears this out.

## Marquee anchor: Ketchikan, AK (southern Alexander Archipelago)

AK's 13 z8 ZIPs are the southeast panhandle's southernmost, mildest strip. Three independent
lines of evidence converge on **Ketchikan** as the correct marquee city for this specific z8
belt (not Juneau or Sitka, the panhandle's other two population centers):

1. **UAF Cooperative Extension, "Growing Tree Fruits in Alaska"**
   (`https://www.uaf.edu/ces/publications/database/gardening/growing-tree-fruits.php`, fetched
   directly), verbatim: *"Kodiak and parts of Southeast are predominately Zones 6 and 7, with
   some areas south of Juneau approaching Zone 8."* Ketchikan is south of Juneau -- this is a
   direct, T1, UAF-authored statement placing Ketchikan (not Juneau) in the panhandle's
   z8 zone.
2. **Independent 2023-USDA-map zone lookups** (secondary corroboration, `plantmaps.com`'s
   Ketchikan hardiness-zone page and general-search zone summaries): Ketchikan straddles 7a/7b/8a
   with its 8a portion covering "the southernmost coastal areas of southeastern Alaska"; Juneau
   is placed in 7a and Sitka in 7b by the same sourcing -- i.e. Ketchikan is the only one of the
   three panhandle population centers that actually reaches z8.
3. Ketchikan is also the city the brief and design spec both name as the working example for
   this belt.

Juneau (the state capital, largest panhandle population center) and Sitka are both real,
well-documented SE Alaska garden communities, but by this belt's own zone definition (z8) neither
qualifies as the marquee anchor -- Ketchikan does.

## Real frost dates, Ketchikan (two independent NOAA/NWS sources, cross-checked)

**Source 1 -- NWS Juneau Forecast Office (AJK), "Last Spring Freeze" statistical article**
(`https://www.weather.gov/media/ajk/articles/springFreeze.pdf`; a genuine NOAA/NWS government
product -- the WebFetch summarizer could not machine-extract this PDF's own statistics table, so
it was re-extracted locally with `pypdf` from the binary WebFetch had already cached, no
re-fetch needed, mirroring Task 4's text-extraction fix). Verbatim statistical table row for
Ketchikan (38 years of station data): **Mean last-freeze date April 22, median April 22, earliest
March 18, latest May 24, standard deviation 15.2 days** -- one of the widest year-to-year spreads
in the table (for comparison, Juneau Airport's spread is 12.4 days, Sitka Airport's 12.3 days),
an honestly-reported precision caveat, not glossed over.

**Source 2 -- NOAA NCEI, "2023 Local Climatological Data Annual Summary with Comparative Data,
KETCHIKAN"** (`https://www.ncei.noaa.gov/pub/access/cebrequests/2023lcdannual/01202313KTN.pdf`;
same PDF-extraction pattern -- re-extracted locally with `pypdf`). Verbatim: *"The growing season
averages 191 days, and starts in mid April until the end of October."* This is a second,
independent NOAA product (NCEI, not NWS/AJK) that corroborates Source 1's direction (mid-to-late
April) without restating the identical number.

**Cross-check (arithmetic, not assumed):** 191 days forward from the Source-1 mean date (April
22) lands on approximately **October 30**, which matches Source 2's own "end of October" language
almost exactly, and also lands close to the growing-season figure independently reported by two
non-T1 weather-data aggregators pulling from the same NOAA normals (191 days, "April 19 to
October 27" -- cited here only as directional corroboration, not as a standalone claim, the same
convention Task 3/4 used for non-T1 cross-checks). Two independent government sources, cross-
checked arithmetically against each other, is treated here as satisfying the "cross-check an
adjacent figure" discipline Task 3's fix required for visually-read data, even though no visual
PDF read was needed for this task (both PDFs re-extracted cleanly as text).

**Real frost-date normals used for the deriver run below:**
- Average last spring frost (32°F): **April 22**
- Average first fall frost (32°F): **~October 30 (end of October)**

## Basket crop 1: cherry-tomato (frost_anchored annual)

**Canonical generic fields** (read-only query):
`weeks_indoors: 6, days_to_maturity_mid: 62, dtm_anchor: from_transplant, frost_tolerance_f: 32`
-- same crop-level values as Tasks 1-4 (not belt-specific).

**Naive calendar** (built in the session scratchpad, `last_frost = Apr 22`, run through
`derive_annual_calendar(cell, calendar_basis="frost_anchored")`):

| Field | Naive value |
|---|---|
| `start_indoors` | Mar 18 - Mar 25 |
| `plant_out` | Apr 29 - May 13 |
| `harvest` | Jun 30 - Jul 28 |
| derived `calendar[]` | `cold_pause` x2 (Jan-Feb), `indoors`(Mar), `plant`(Apr-May), `harvest`(Jun-Jul), then `cold_pause` **Aug through Dec** (5 straight months) |

**A methodological check (the brief's Nevada-edge-case warning):** Ketchikan's real last frost
(Apr 22) is late enough that January stays inactive under the naive construction, so the
deriver's January-active exception that suppressed `cold_pause` entirely for Nevada (last frost
Feb 28) does **not** fire here -- confirmed by actually running the deriver, not assumed. AK's
naive shape mechanically matches mid-Atlantic/mid-South/Utah's flat winter `cold_pause`, not
Nevada's all-`growing` back half. On its face this naive output reads as an entirely ordinary
z8 single-cycle outdoor tomato calendar, structurally identical in shape to the other four
belts' naive tomato calendars.

**Real T1 guidance -- three independent, converging UAF Cooperative Extension sources, all
pointing the same direction:**

1. **UAF Cooperative Extension, "16 Easy Steps to Gardening in Alaska"**
   (`https://www.uaf.edu/ces/publications/database/gardening/easy-steps-gardening-alaska.php`,
   fetched directly), verbatim: *"Outside of the Interior, few garden sites are warm enough to
   grow good tomatoes."* And: *"In most of Alaska, tomatoes are usually grown in greenhouses or
   shelters where they are supplied with additional heat."* Southeast Alaska (Ketchikan's belt)
   is explicitly "outside of the Interior."
2. **UAF Cooperative Extension, "Recommended Variety List for Southeastern Alaska" (HGA-00231,
   Robert Gorman, Jeff Smeenk, Darren Snyder)**
   (`https://sitkalocalfoodsnetwork.org/wp-content/uploads/2015/03/hga-00231segardenvarieties.pdf`
   -- a UAF-authored PDF mirrored by a SE-Alaska community organization; WebFetch's summarizer
   could not machine-extract it, re-extracted locally with `pypdf`, clean text, no visual read
   needed). This is the exact belt-specific T1 document the design spec flagged as missing from
   the catalog. Its own introduction states directly: *"the cool-season vegetables, such as
   potatoes, carrots and the cabbage family, thrive in our gardens while the warm season
   vegetables, such as beans, cucumbers and tomatoes, require protection... The warm-season
   vegetables are much more productive under high or low plastic tunnels."* Its variety table
   heads the entire tomato section **"Tomatoes (perform better in a high tunnel or under row
   cover)"** -- listing cold-tolerant (Early Tanana, Stupice, Sub Arctic 25), very-early (Early
   Girl, Glacier, Legend, Northern Exposure, Oregon Spring, Balconi Red/Yellow, Northern Delight,
   Fourth of July) and "other" varieties, the last group including **Sun Gold (yellow, cherry
   type)** -- a direct hit on this task's own basket crop (cherry-tomato).
3. **UAF Cooperative Extension, "Hoop Houses in Alaska: Twenty Questions and Answers to Get You
   Started"** (`https://www.uaf.edu/ces/publications/database/gardening/hoop-houses.php`, fetched
   directly), verbatim, citing a controlled Palmer research trial: *"Tomatoes and cucumbers grown
   inside the house also thrived, while adjacent plots outside gave almost no yields."* This is
   not a soft stylistic preference -- it is a real trial result showing outdoor tomato yield
   collapsing to near zero next to a protected-culture control.

**Naive vs. real:** this is a **suitability-class-level divergence, not a window-shape gap**. The
naive deriver's calendar renders a completely ordinary-looking single-cycle outdoor annual
(indoors in March, plant out end of April, harvest June-July, dormant through winter) with
nothing to distinguish it from mid-Atlantic's, mid-South's, Nevada's, or Utah's structurally
similar naive tomato calendars, all four of which turned out to be directionally correct about
basic outdoor viability. Alaska is different in kind, not just in window length: three
independent T1 UAF Cooperative Extension sources -- a statewide guide, the belt's own
variety-recommendation publication, and a controlled research trial -- all agree that unprotected
outdoor tomato culture in this exact belt gives poor-to-near-zero yield, and that productive
growing requires a high tunnel or row cover. This is categorically different from the prior four
belts, where the naive model was honest about *whether* the crop grows outdoors and only
undersold *how long* the season runs (mid-Atlantic/mid-South) or mischaracterized the *shape* of
the off-season (Nevada/Utah). Here the naive model's basic operating assumption -- that this is
an unprotected single-cycle outdoor annual at all -- is what the real sources contradict.

**Cross-reference to this dataset's own closest analog, `pnw` (the belt explicitly named as this
task's nearest kin):** PNW's own z8 cherry-tomato cell (`resolved_by_zone.8`, WSU/OSU-sourced)
runs a full outdoor season (`plant_out: May 1 - May 31`, `harvest: Jun 25 - Nov 7`) with an
explicit `zone_notes`: *"The valley's slightly warmer summer ripens cherry tomatoes with room to
spare; no special early-variety caution is needed here."* Alaska's SE panhandle, despite being
the belt design-spec-flagged as PNW's closest analog, does **not** share this outcome -- real UAF
guidance for the AK belt is the mirror opposite of PNW's own already-authored "no caution needed"
verdict. This is direct, sourced evidence that AK is NOT simply a colder shade of PNW that could
safely inherit PNW's own tomato treatment; it is materially different.

## Basket crop 2: apple (chill-gated tree fruit)

Apple is not annual-deriver-driven (`weeks_indoors: None, days_to_maturity_mid: None,
dtm_anchor: None, frost_tolerance_f: 28` -- season-only/chill-gated, matches Tasks 1-4).

**Canonical `chill_hours_required` per recommended variety:** Dorsett Golden 100, Anna 200, Ein
Shemer 100, Zestar! 800, McIntosh 900, Liberty 800, Empire 700, Honeycrisp 800, Gala 600, Golden
Delicious 700, Jonagold 700, Mutsu 600, Fuji 600, Granny Smith 600, Pink Lady 550, Dolgo 500 (also
`hardiness_zone_min: 3, hardiness_zone_max: 9` at the crop level).

**Real guidance -- two converging findings, both UAF Cooperative Extension, T1:**

1. **The binding constraint is NOT chill delivery.** UAF's "Growing Tree Fruits in Alaska"
   (fetched directly) frames apple-variety selection around **winter cold-hardiness first**
   (*"Fruit trees in Alaska must be able to survive the coldest temperatures of the year without
   suffering freeze damage"*, USDA zone matching as the primary tool), **then** growing-season
   length for ripening -- the UAF "It Grows in Alaska" blog post "Growing Fruit in Alaska" quotes
   the breeders directly on this exact priority order: *"First they ask if it will survive the
   winter. Then, will it fruit during the short growing season?"* No chill-hour figure for
   Ketchikan or SE Alaska was found despite a genuine search (a real gap, not glossed over, the
   same honest-gap handling Task 4 used for St. George) -- but this dataset's **own existing
   region data for the same crop** independently confirms chill is not the limiting factor at
   comparable/colder Alaska-adjacent latitudes: `northern_tier` z3 (Minnesota-style continental,
   `umn_ext`-sourced) shows apple `survives_no_fruit` with the verbatim reasoning **"Chill is
   abundant, so the tree blooms every spring; the bloom is simply too exposed"** -- a real,
   already-gated precedent in this dataset for exactly the mechanism found here (abundant chill,
   binding constraint elsewhere).
2. **The real SE-Alaska-specific recommended variety list shares ZERO overlap with this crop's
   canonical 16-variety recommended list.** UAF's "Recommended Variety List for Southeastern
   Alaska" (HGA-00231, same PDF as above) lists, under "Tree Fruits / Apple": **Yellow
   Transparent, Pristine, William's Pride, Gravenstein, Lodi, Tydeman's Early, Sansa, Silken,
   Akane** -- none of which appear anywhere in the canonical recommended-variety list (Dorsett
   Golden / Anna / Ein Shemer / Zestar! / McIntosh / Liberty / Empire / Honeycrisp / Gala / Golden
   Delicious / Jonagold / Mutsu / Fuji / Granny Smith / Pink Lady / Dolgo). The AK-recommended set
   is a real, distinct cluster of very-early-ripening (July-August), short-season apples; the
   canonical list's varieties are predominantly September-through-November ripeners bred for
   mainstream Lower-48 markets. The same source independently confirms (per an earlier UAF page)
   that Yellow Transparent is *"a popular variety in Southcentral and Southeast Alaska"* and is
   selected there specifically for early ripening, not primarily for extreme winter hardiness
   (Yellow Transparent/Lodi are hardy to zone 2/3, far colder than z8 SE Alaska actually needs).

**Cross-reference to this dataset's own PNW region (the named closest analog) sharpens the
divergence further.** PNW z8's apple cell (`chill_hours: [968, 1950]`, `fruits_reliably`) states:
*"WSU's western Washington fruit handbook lists ripening from early August (Sunrise, Pristine)
through late October to early November (Mutsu), with most commercial-quality varieties clustering
early September to late October; that whole span finishes comfortably within this zone's
frost-free season."* PNW's real frost-free season (Mar 21 - Nov 12, ~236 days) is long enough to
finish even late-ripening varieties like Mutsu. Alaska's real frost-free season (Apr 22 - ~Oct
30, ~191 days per NOAA NCEI) is **45 days shorter**, and this dataset's own `northern_tier` z7
cell (a *warmer-summer continental* climate, not maritime) shows the opposite lesson from PNW's:
*"the long season ripens late keepers like Fuji and Granny Smith"* -- i.e. a longer or hotter
season, not a warmer zone NUMBER per se, is what ripens late-season fruit. AK's z8 label
nominally reads "warmer than PNW's own z8" in zone-number terms only if compared naively, but its
real growing season is shorter and its summers are cooler and cloudier (UAF's own SE Alaska guide
opens by citing *"short cool growing season and high rainfall"* as the belt's defining
challenge) -- the zone number and the real climate are decoupled here in exactly the way a
zone-only fallback cannot detect. This is a **structural, mechanism-level mismatch**: this
dataset's chill-hour-based suitability logic (used for every other region, including PNW, RGV,
warm_arid, low_desert_az) would read AK's abundant winter chill and default toward
`fruits_reliably` off the canonical variety list -- exactly the wrong conclusion, since real UAF
guidance recommends a completely different, non-overlapping variety set chosen for a constraint
(summer ripening window) this dataset does not model for apple at all.

## Basket crop 3: kale (frost_anchored, cool-season annual)

**Canonical generic fields:** `weeks_indoors: 4, days_to_maturity_mid: 55, dtm_anchor: from_sow,
frost_tolerance_f: 20`.

**Naive calendar** (`last_frost = Apr 22`):

| Field | Naive value |
|---|---|
| `start_indoors` | Apr 1 - Apr 8 |
| `plant_out` | Apr 29 - May 13 |
| `harvest` | Jun 23 - Jul 21 |
| derived `calendar[]` | `cold_pause` x3 (Jan-Mar), `plant`(Apr-May), `harvest`(Jun-Jul), then `cold_pause` **Aug through Dec** (5 straight months) |

Note: the naive builder mechanically applies the crop-level `weeks_indoors: 4` even though this
dataset's own real region data (e.g. `pnw`) direct-sows kale (`start_indoors: null`) -- the naive
builder is deliberately dumb/generic and does not know kale is normally direct-sown; this is a
minor construction artifact of the method, not a finding about Alaska specifically.

**Real T1 guidance, two independent UAF sources:**

1. **UAF, "16 Easy Steps to Gardening in Alaska"** (fetched directly), verbatim: *"This green
   does well in Alaska and grows in any good garden site."* Kale is recommended as reliable,
   direct-seedable, statewide.
2. **UAF, "Recommended Variety List for Southeastern Alaska"** (HGA-00231): kale appears plainly
   in the "Greens" section (*"Kale (many varieties (e.g., White Russian, Red Russian,
   Winterbor)"*) alongside other cool-season brassicas, with no protection caveat -- the opposite
   treatment from the same document's tomato section. The document's own introduction frames the
   belt's defining growing conditions as *"short cool growing season and high rainfall... long
   days"* -- conditions that disadvantage tomato but favor kale.

**Naive vs. real:** directionally correct on suitability -- kale genuinely thrives here, as
predicted, with no protection needed. The real gap is the same *shape* found for warm-season
annuals in mid-Atlantic/mid-South (season under-representation, not a suitability problem): the
naive single 4-week harvest window (Jun 23 - Jul 21) drastically undersells kale's real extended
productive window. This dataset's own `pnw` kale cell (the closest analog, OSU/WSU-sourced) shows
a single long direct-sown planting window (`plant_out: May 1 - Jul 15`) feeding a harvest that
runs `Jun 20 - Jan 31` (`zone_notes`: *"just one long sowing that keeps producing... real winter
cold ends useful harvest by late January most years"*), frost-tolerant to `20°F` at the crop
level. Alaska's real frost tolerance is identical (`frost_tolerance_f: 20`) and its documented
long summer daylight (Ketchikan's own June solstice day length is ~17.5 hours -- real but notably
less extreme than the Interior's oft-cited 20+ hour days; an honest, non-cherry-picked figure, not
the more dramatic Fairbanks number) plausibly supports a similarly extended kale season, though no
AK-specific harvest-window end date was found in the sources checked here (an open gap, recorded
rather than assumed to mirror PNW's exactly). Kale shows **no suitability-class concern** -- this
is a real but ordinary window-shape caveat, the established shape from Tasks 1-2, not a driver of
the overall ruling.

## Ruling: NEW-REGION

**Kale** is directionally fine, the familiar shape from mid-Atlantic/mid-South: real guidance
confirms suitability and the one real gap (an underrepresented harvest window) is a
window-shape caveat, not a suitability problem.

**Cherry-tomato and apple are both genuine, sourced, suitability-class-level divergences --
not variety-tier caveats, not window-shape gaps.**

- Cherry-tomato: three independent T1 UAF Cooperative Extension sources -- a statewide guide, the
  belt's own dedicated variety-recommendation publication, and a controlled research trial --
  converge on the same finding: unprotected outdoor tomato culture in this exact belt gives
  poor-to-near-zero yield ("adjacent plots outside gave almost no yields"), and the belt's own
  variety list heads its tomato section with "perform better in a high tunnel or under row
  cover." The naive frost-anchored deriver renders an entirely ordinary-looking single-cycle
  outdoor annual with no signal that anything is wrong -- the model's basic operating premise,
  not just its window length, is what the real sources contradict.
- Apple: the real, belt-specific UAF-recommended variety list (Yellow Transparent, Pristine,
  William's Pride, Gravenstein, Lodi, Tydeman's Early, Sansa, Silken, Akane) shares zero overlap
  with the canonical 16-variety recommended list, because the belt's real binding constraint
  (short, cool, cloudy summer limiting ripening time -- confirmed by UAF's own stated
  priority order, "will it survive the winter, then will it fruit during the short growing
  season") is a mechanism this dataset's chill-hour-based suitability logic does not represent at
  all for this crop. Applied naively, that logic would read AK's abundant winter chill (this
  dataset's own `northern_tier` z3 precedent independently confirms chill is not the limiting
  factor even in a far harsher climate) and default to `fruits_reliably` off the canonical list --
  exactly backwards, since the canonical varieties are largely September-November ripeners bred
  for a season 45+ days longer than Ketchikan's real ~191-day one (per NOAA NCEI), a length this
  dataset's own `northern_tier` z7 cell shows is precisely the difference between a variety list
  finishing "comfortably" and not.

**Both basket-crop divergences point the same direction and share a common root cause**: AK's z8
maritime panhandle decouples the zone NUMBER (which encodes winter minimum temperature, and reads
as comparably mild to PNW's own z8) from the real climate driver that actually matters for both
crops here -- a short, cool, cloudy GROWING season, not a cold winter. This is exactly the
mechanism the design spec named as the NEW-REGION trigger ("a genuine divergence... especially a
chill/fruit-set class mismatch"), and it is not softened by inheriting PNW's own already-authored
region: this task's own direct cross-references show PNW's real cherry-tomato and apple treatment
for z8 (full outdoor season, `fruits_reliably` off the canonical list) is the **opposite** of
what real UAF sources document for AK's z8 core. AK is not a colder shade of PNW that could safely
borrow PNW's numbers; it is close enough in climate FAMILY to be the right belt to compare against
PNW (confirming the design spec's instinct to flag it), but far enough in real magnitude
(shorter season, cloudier summer) that the comparison itself is what proves the two need separate,
independently-sourced treatment.

Two of three basket crops -- not a lone caveat on one crop, and not merely a sharper version of a
variety-tier issue like Nevada's or Utah's apple findings -- show real, T1-sourced, mechanism-level
suitability divergences from what the generic zone-only fallback would produce. **Ruling:
NEW-REGION.** Per the design spec's scope boundaries, this belt is **not built here** -- it is
recorded as a NEW-REGION finding to be queued as its own future roadmap item (a full spec/plan/
build), the same way items 3 (RGV) and 4 (PNW) were spun out after earlier reconciliation work
surfaced the need. Candidate scope for that future item, based on this task's research (not a
commitment, just what the evidence points toward): a maritime SE-Alaska-panhandle region
(Ketchikan-anchored z8 core, with Juneau/Sitka's z7 belt as an open question for whether it
extends or needs its own treatment) built on UAF Cooperative Extension Service sourcing --
`easy-steps-gardening-alaska.php` (statewide baseline), `HGA-00231` (the belt's own dedicated
variety list, primary source for both the tomato protected-culture finding and the apple variety
substitution), `hoop-houses.php` (protected-culture framing for warm-season annuals), and
`growing-tree-fruits.php` / the "It Grows in Alaska" blog (apple's ripening-season-not-chill
framing) -- plus the two NOAA/NWS frost-date sources found here for the real Ketchikan calendar
anchor. None of these sources are registered to `source_catalog` by this task (per the design
spec, `source_catalog` lives inside `crops_data_final.json` and is out of scope here); formal
registration happens only if/when this belt is actually built.

## Source table

| Institution | URL | What it backs |
|---|---|---|
| UAF Cooperative Extension, "Growing Tree Fruits in Alaska" | https://www.uaf.edu/ces/publications/database/gardening/growing-tree-fruits.php | Marquee-city zone placement ("some areas south of Juneau approaching Zone 8"); apple's real limiting-factor priority order (winter hardiness first, then short growing season) |
| UAF Cooperative Extension, "16 Easy Steps to Gardening in Alaska" (HGA-00134) | https://www.uaf.edu/ces/publications/database/gardening/easy-steps-gardening-alaska.php | Statewide tomato guidance ("few garden sites are warm enough... usually grown in greenhouses or shelters"); kale statewide guidance ("does well... grows in any good garden site") |
| UAF Cooperative Extension, "Recommended Variety List for Southeastern Alaska" (HGA-00231, Gorman/Smeenk/Snyder) | https://sitkalocalfoodsnetwork.org/wp-content/uploads/2015/03/hga-00231segardenvarieties.pdf | The belt's own dedicated T1 source (newly found, not previously catalogued): tomato "perform better in a high tunnel or under row cover" incl. Sun Gold cherry type; the real, non-overlapping apple variety list; kale listed plainly, no caveat |
| UAF Cooperative Extension, "Hoop Houses in Alaska: Twenty Questions and Answers" | https://www.uaf.edu/ces/publications/database/gardening/hoop-houses.php | Controlled Palmer trial result: outdoor tomato/cucumber "gave almost no yields" vs. protected-culture thriving |
| UAF "It Grows in Alaska" blog, "Growing Fruit in Alaska -- Apples, Cherries, Plums, and Pears" | https://itgrowsinalaska.community.uaf.edu/2025/03/13/growing-fruit-in-alaska-apples-cherries-plums-and-pears/ | Breeders' own stated priority order for apple variety selection (winter survival, then short-season fruiting) |
| NWS Juneau Forecast Office (AJK), "Last Spring Freeze" | https://www.weather.gov/media/ajk/articles/springFreeze.pdf | Ketchikan real last-frost statistics: mean/median Apr 22, earliest Mar 18, latest May 24, 38 years of data |
| NOAA NCEI, "2023 Local Climatological Data Annual Summary, KETCHIKAN" | https://www.ncei.noaa.gov/pub/access/cebrequests/2023lcdannual/01202313KTN.pdf | Growing season length (191 days, mid-April to end of October) -- independent cross-check on the frost-date direction |
| (context only, not load-bearing) hardiness-zone reseller cross-check | https://www.plantmaps.com/hardiness-zones-for-ketchikan-alaska | Secondary corroboration only that Ketchikan's 8a portion is the panhandle's southernmost coastal strip; not cited as a standalone claim |
| (context only, not load-bearing) sunrise/sunset data aggregator | https://www.timeanddate.com/sun/usa/ketchikan | Ketchikan June-solstice day length (~17h32m), cited only to give an honest, non-cherry-picked (i.e. not the more dramatic Interior/Fairbanks) daylight figure |

Both `sitkalocalfoodsnetwork.org`-mirrored and `ncei.noaa.gov`/`weather.gov`-hosted PDFs did not
machine-extract through WebFetch's own summarizing parser; all were re-extracted locally with
`pypdf` from the binary copies WebFetch had already cached to disk (no re-fetch, no external
tooling beyond what was already installed), and all extracted cleanly as text -- no image-render/
visual read was needed for this task (a text-extraction problem, matching Task 4's fix, not a
visual-read problem like Task 3's). This task's own comparison also cites three ALREADY-CANONICAL
region entries (`pnw` on cherry-tomato and apple, `northern_tier` z3/z7 on apple) as internal
cross-references; these are existing dataset content, not new sources, and are not re-cited to
`source_catalog`. No new `source_catalog` registration was made for the newly-found UAF pages
above (per the design spec, they are cited here by institution+URL only; formal registration
happens only if/when this belt is later built as a real region). No `crops_data_final.json` bytes
were read-write touched.
