# Utah "Dixie" region -- Content Review A (FRUITING / SUITABILITY set, 71 cells)

Reviewer: independent content review (Claude Code). Date: 2026-07-22.
Scope: `utah_dixie_annuals_warm.json` (42), `utah_dixie_trees.json` (14), `utah_dixie_citrus.json` (5),
`utah_dixie_perennials.json` (10). READ-ONLY: findings for the controller to apply.
Source of truth: `docs/reviews/notes/2026-07-22/utah_dixie_sources.md` + the class shard reports.

---

## OVERALL VERDICT: SHIP-WITH-FIXES

The batch is strong. Every factual spine checks out: Group A-D St. George dates (Feb 15 / Mar 1 /
Mar 15 / Apr 1), the frost anchor (Mar 30 / Nov 1), the heat thresholds, and the Washington County
Fruits elevation split are all faithfully carried, uniform across all 71 cells. Honesty discipline is
excellent (okra / sweet-potato / mulberry / pomegranate all transparently disclose the non-USU-table
basis; pawpaw unsuitable is well-argued). The apple/pear-marginal, raspberry, and strawberry deltas
are executed exactly to spec. Prose is clean: NO em dashes, temps render as the °F glyph everywhere
(zero "degrees"), American English throughout, dual-register hooks are distinct.

One Critical defect blocks a clean promote (habanero renders with NO harvest token). Four Important
accuracy fixes (cherry-sour overclaim, the cayenne/jalapeno heat-lover truncation, the edamame
honesty gap) should land before promote given the accuracy-and-authority north star. The Minors are
polish.

Counts: **Critical 1 | Important 4 | Minor 4**

---

## CRITICAL (must fix before promote)

### C1. habanero (annuals_warm) -- renders with NO harvest token; miscategorized as a heat-abort crop
`habanero` was authored Shape A (heat_pause `[7,8,9]`) alongside the sweet nightshades. Its harvest
resolves to **Jul 5 - Jul 25**, which lands inside the Jul-Sep pause. Because `derive_annual_calendar`
precedence is `heat_pause > harvest`, the derived `calendar` is
`[cold_pause,indoors,indoors,plant,growing,growing,heat_pause,heat_pause,heat_pause,cold_pause,cold_pause,cold_pause]`
-- **zero `harvest` tokens**, while `resolved_by_zone.8.harvest` still advertises "Jul 5 - Jul 25". A
user sees a harvest date range with an empty 12-month strip: self-contradictory, and it erodes exactly
the authority the project protects. habanero is the only cell in all 71 with this defect (confirmed by
a calendar-vs-harvest sweep).

This is a genuine regression, not an accepted pattern. In the canonical, **every** other region gives
habanero a harvest token, and the desert analogs model it as a heat-LOVER that crops into fall on the
one spring planting:
- `warm_arid` z8 (St. George's desert-z8 twin): NO heat_pause, harvest **Jul 15 - Oct 31** (Shape C).
- `low_desert_az` (Phoenix): heat_pause `[7,8]` only, harvest resumes **Oct 1 - Dec 5** (split season).
- `nevada` (the stated donor): Shape A, but its harvest lands **in June** (before the pause) so a token shows.

Utah copied Nevada's Shape A, but Utah's Apr 1 plant + 95-day DTM pushes harvest_start to Jul 5, past
the June boundary -- so nothing survives the pause. The W1 author self-flagged this ("the one real
finding of this batch") and asked for a content-team call.

FIX: re-author habanero as a heat-lover, mirroring the `warm_arid` desert analog -- single spring
planting, drop the heat_pause (or reduce to `[7,8]` per Phoenix), and let the ONE planting's harvest
run from ~Jul through ~late Oct, capped ahead of the Nov 1 frost. This is an extended bearing window on
the original planting, NOT a `second_planting`, so it does not violate the delta-4a "no warm-crop fall
replant" rule. Rewrite the region_notes: habanero is a strong desert heat-lover here, not the "marginal
/ optimistic pick squeezed against the heat wall" the current copy claims. (See ruling R2.)

---

## IMPORTANT (fix before promote)

### I1. cherry-sour (trees) -- drop `fruits_reliably` -> `marginal`
Authored `fruits_reliably` on the county's generic low-elevation "cherries" listing. But sour cherry
(Prunus cerasus: Montmorency, Meteor, North Star) is genuinely high-chill (~700-1000+ hr), roughly
double the top of the region's own delivered band `[250,450]`. Unlike sweet cherry -- which has the
purpose-bred low-chill pair Royal Lee / Minnie Royal (~200-300 hr) that legitimately fits the valley --
there is NO widely available low-chill sour cherry cultivar to bridge the gap, so the prose's "lean to
the lowest-chill sour cherries" is largely hollow. `fruits_reliably` therefore overclaims and
contradicts the region's own chill band; the Nevada region called cherry-sour marginal on the same
logic. The authored prose is already heavily hedged ("needs more winter cold than most desert stone
fruit," "give it your coolest, highest site"), so only the suitability field is out of step with the
hedge. FIX: set `suitability = "marginal"` and align the one-line suitability_note. cherry-sweet stays
`fruits_reliably` (correct -- Royal Lee / Minnie Royal are real and near-band). (See ruling R1.)

### I2. cayenne-pepper (annuals_warm) -- heat-lover truncated at June
Authored Shape A (heat_pause `[7,8,9]`, harvest Jun 15-30). Cayenne (C. annuum) is a hot chile that
sets and ripens through the Southwest summer and is classically harvested/dried in late summer and
fall. The desert analog `warm_arid` z8 models it Shape C (no heat_pause, harvest **Jun 25 - Oct 31**);
`low_desert_az` gives it a fall resume. The Utah cell truncates ~4 months of real production. FIX:
re-author toward the `warm_arid` heat-lover treatment so a Jul-Oct fall harvest shows (before Nov 1).

### I3. jalapeno (annuals_warm) -- heat-lover truncated at June
Same pattern (Shape A, heat_pause `[7,8,9]`, harvest Jun 15-30). Jalapeno is heat-tolerant and widely
fall-harvested in the desert Southwest; `warm_arid` z8 models it as a split season (harvest **Jun 1-30
+ Sep 10 - Nov 10**). Slightly more heat-moderate than habanero/cayenne, so lower confidence, but the
biology supports a fall crop. FIX: re-author to show a Sep-Oct fall harvest (Shape C or a split like
`warm_arid`). (I1-I3 hot-chile ruling: see R2.)

### I4. edamame (annuals_warm) -- honesty gap: asserts a USU Group C date for a crop not in USU's table
Unlike okra and sweet-potato -- which cleanly disclose "sits outside USU Extension's Table 1 ...
authored from the crop's own heat-lover biology" -- edamame's region_notes asserts "Direct-sow around
March 15, **the Group C (Tender) date for St. George**" as if soybean were listed. USU's Group C
(sweet corn, cucumber, summer squash, snap bean, dry bean) does NOT include soybean/edamame; the cell
is grouping it by analogy to snap bean. That attributes an uncited USU date to an unlisted crop -- the
exact overclaim the honesty rule guards. FIX: add a half-clause disclosing the by-analogy grouping
(e.g., "grouped with the tender legumes / snap bean, since soybean is not separately listed in USU's
table"). The harvest WINDOW itself is fine and needs no change (see ruling R3).

---

## MINOR (polish; not promote-blocking)

### M1. "Shape A" build-term leaks into consumer synthesis_note_seasoned
`beefsteak-tomato` (harvest_start): "...the slowest of the Shape A tomatoes here..." and `habanero`
(harvest_start): "...the slowest crop in this Shape A group here...". "Shape A" is an internal build
label. It matches a shipped Nevada pattern (not a fresh regression), so it is not a blocker, but scrub
for polish -> "the slowest tomato here" / "the slowest-maturing of these peppers here". (If C1 is fixed,
the habanero note is rewritten anyway.)

### M2. schema token `heat_pause` in the primary consumer field region_notes_seasoned
`okra` and `sweet-potato`: "...straight through the ... 100°F-plus summer with no heat_pause." `pole-beans`
(region_notes_seasoned + synthesis_note_seasoned): "no separate heat_pause is modeled." region_notes_*
is the headline consumer prose; the snake_case token reads as code. Canonical has only 1 pre-existing
instance, so these are near-regressions. FIX: reword to plain English -- "no summer heat pause" /
"keeps setting through the summer heat without a pause."

### M3. heat_pause.months `[7,8,9]` vs the cited basis "June, July, and August"
Every Shape A cell codes heat_pause `[7,8,9]` (Jul-Sep) while its `basis_seasoned` cites USU's
"100°F in June, July, and August." The `[7,8,9]` CHOICE is correct and deliberate -- coding `[6,7,8]`
(the sources-doc value) would wipe the June harvest token off every tomato and most peppers -- so this
is not a data error, just a wording mismatch: the pause names Jul-Sep but the basis sentence names
Jun-Aug. Optional tidy: have the basis sentence say the spring crop is picked through June (ripening
spring-set fruit) then set fails "July into September," which the harvest_end notes already do well.
Note the sources doc's stated `[6,7,8]` should be treated as superseded by the correct `[7,8,9]`.

### M4. "warm-arid desert regions" echoes the internal region id in consumer prose
`mulberry` and `pomegranate` suitability_note_seasoned: "...fruits reliably across the neighboring
Mojave and warm-arid desert regions." Reads as plain geography, but "warm-arid" (hyphenated) echoes the
internal `warm_arid` region id. Trivial; consider "the neighboring Mojave and warm desert regions."

---

## ADJUDICATED FLAGS (explicit rulings)

**R1 -- cherry-sour: DROP to `marginal`.** Sour cherry is genuinely high-chill (~700-1000 hr, ~2x the
`[250,450]` band) and has no low-chill cultivar equivalent to sweet cherry's Royal Lee / Minnie Royal,
so `fruits_reliably` overclaims and contradicts the region's chill band and the Nevada precedent. The
county's generic "cherries" listing is honestly satisfied by sweet cherry. cherry-sweet KEEPS
`fruits_reliably` (Royal Lee / Minnie Royal ~200-300 hr are real and near-band).

**R2 -- hot chiles: RE-AUTHOR habanero (must) + cayenne and jalapeno (should) as heat-lovers with a
fall harvest.** habanero is Critical (zero harvest token; C1). cayenne and jalapeno are Important
(harvest truncated at June, understating ~4 months). All three are heat-LOVERS that crop into fall on
the single spring planting -- mirror `warm_arid` (Shape C, no heat_pause, harvest through ~Oct before
the Nov 1 frost) or the `low_desert_az` split (heat_pause `[7,8]`, harvest resumes Sep-Oct). This is an
extended bearing window, NOT a `second_planting`, so it respects the no-fall-replant rule. The SWEET
peppers **bell-pepper and banana-pepper correctly stay Shape A** (single spring, finish before the
heat) -- they are more heat-limited (blossom drop ~90°F), and Phoenix likewise gives them no strong
fall crop, so the "finish before the heat" framing is honest for the sweets. Crops needing the fix:
**habanero, cayenne-pepper, jalapeno.**

**R3 -- edamame ~3-week harvest window (Jun 8-30): ACCEPTABLE, no window fix.** Edamame is picked in a
single concentrated once-over at pod fill, so a ~3-week window is biologically normal and honest; the
single-spring / no-fall framing is correct (pods abort in the Jul heat). The only edamame fix is the
SEPARATE honesty gap I4 (disclose the by-analogy Group C grouping).

**R4 -- mulberry / pomegranate `fruits_reliably` (not on USU Fruits list): DISCLOSURE PRESENT, PASS.**
Both state verbatim "USU Washington County Extension does not name [mulberry/pomegranate] on its fruit
list, but it is a classic low-desert [tree/fruit] and fruits reliably across the neighboring Mojave and
warm-arid desert regions." Transparent biology-plus-neighbor basis, exactly per spec. (persimmon needs
no disclosure -- it IS on the USU low-elevation list: apricots, cherries, figs, grapes, peaches,
persimmons, plums, strawberries; the cell correctly cites it.)

**R5 -- citrus grouping (lemon = survives_no_fruit / orange-navel = unsuitable): DEFENSIBLE, PASS.**
All five carry `min_winter_temp_f [15,20]` and correctly note USU's Fruits page lists no citrus. The
split tracks real cold-hardiness: mandarin-clementine (satsuma/clementine, low-to-mid 20s) and Meyer
lemon (lemon x mandarin hybrid bred for marginal climates, low-to-mid 20s) = `survives_no_fruit`
(protected container); navel orange / lime / grapefruit = `unsuitable`. The crux distinction is sound:
lemon HAS a cold-hardy selection to reach for (Meyer) and true lemon is flagged too tender, whereas
navel orange / grapefruit / lime have NO widely grown cold-hardy cultivar to close the gap at 15-20°F
lows. lime (near-freezing damage) and grapefruit (mid-20s + highest heat need) are correctly the worst.

**R6 -- variety chill numbers: NONE fabricated or overstated, PASS.** apple: Dorsett Golden ~100,
Ein Shemer ~100, Anna ~200 hr -- all legitimate low-chill apple figures. sweet cherry: Royal Lee /
Minnie Royal ~200-300 hr -- the real purpose-bred low-chill pair (correctly noted as needing
co-planting, neither self-fertile). fig ~100-300 need vs 250-450 band, pomegranate ~100-250,
mulberry ~100-500 -- all reasonable. No number overstates the region's delivered chill.

---

## DELTA-FIDELITY CONFIRMATIONS (passed)

- ALL 42 warm crops = single spring window, `nplantings=1`, NO `second_planting` (delta 4a load-bearing
  rule) -- confirmed by sweep. (The R2 hot-chile fix is an extended bearing window, not a replant.)
- apple + pear-asian + pear-european = `marginal` with the lowest-chill-third steer (Dorsett Golden /
  Anna / Ein Shemer) AND the county higher-elevation (5,300+ ft: Central / Enterprise / New Harmony)
  recommendation, cited to the Fruits page (delta 4b). PASS.
- pawpaw = `unsuitable` (humid-forest understory / alkaline-Mojave mismatch), well-argued. PASS.
- raspberry = `marginal`, everbearing/primocane fall-bearing steer, mirrors `warm_arid`, names the USU
  cultivars Caroline / Josephine / Polana / Joan J / Polka + low-chill desert canes Bababerry /
  Dorman Red, cites the "Utah's Dixie" fall-bearing quote, iron-chlorosis / chelated-iron / afternoon
  shade / raised beds (delta 4c). PASS.
- strawberry = low-elevation THRIVER, perennial matted row, cites the USU Fruits low-elevation list
  (delta 4c). PASS. blackberry marginal / blueberry very-marginal (alkaline, container-only) /
  elderberry marginal (moisture) all match the spec.
- Group A-D St. George dates + frost anchor Mar 30 / Nov 1 uniform across all 71 cells; Group D plant
  Apr 1, Group C Mar 15, okra/sweet-potato later warm-soil biology dates. PASS.
- Prose: no em dashes; °F glyph everywhere (no "degrees"); American English (no British spellings in
  consumer notes); dual-register hooks distinct. PASS.

Note on the perennial woody-herb `synthesis_note_seasoned` internal-provenance language
("grown_as=perennial:", "plant_out follows...", "resolved_from carries the ... deriver's dormancy
bracket", "display-only on this perennial cell"): this matches the shipped canonical pattern (many
"grown_as=perennial:" instances already ship), so it is an established internal field, NOT a
Utah-introduced leak -- out of scope for this batch.
