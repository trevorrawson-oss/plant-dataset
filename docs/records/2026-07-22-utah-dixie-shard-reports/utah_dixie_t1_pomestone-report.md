# utah_dixie tree shard -- pomestone (apple/pear + core stone fruit)

**Status: DONE.** All 9 cells authored, self-gated clean.

**Shard:** `tools/staging/shards/utah_dixie_t1_pomestone.json` (9 cells)

## Gate summary
- `region_harness utah_dixie 8 <shard> <slug>` -> **GATE: PASS on all 9** (apple, pear-asian,
  pear-european, apricot, cherry-sour, cherry-sweet, nectarine, peach, plum).
- `region_cell_audit utah_dixie <shard>` -> **0 issue(s) across 9 cell(s)**.
- Every fruits_reliably/marginal cell carries a 12-token calendar; all calendars are
  `derive_tree_calendar(bloom, harvest)`-coherent (the A37/tree-calendar gate is inside the PASS).

## Per-tree suitability verdicts
| slug | suitability | bloom | harvest | note |
|---|---|---|---|---|
| apple | **marginal** | Apr 5 - Apr 25 | Jul 20 - Sep 15 | MARQUEE flip (Nevada was fruits_reliably) |
| pear-asian | **marginal** | Mar 25 - Apr 15 | Jul 20 - Sep 5 | MARQUEE flip |
| pear-european | **marginal** | Mar 25 - Apr 15 | Jul 20 - Sep 5 | MARQUEE flip |
| apricot | fruits_reliably | Mar 25 - Apr 15 | Jun 15 - Jul 15 | low-elevation thrive column |
| cherry-sour | fruits_reliably | Mar 25 - Apr 15 | May 25 - Jun 20 | **TENSION -- see below** |
| cherry-sweet | fruits_reliably | Mar 25 - Apr 15 | May 25 - Jun 20 | low-chill Royal Lee/Minnie Royal |
| nectarine | fruits_reliably | Mar 30 - Apr 20 | Jun 20 - Jul 20 | rides on peach (fuzzless peach) |
| peach | fruits_reliably | Mar 30 - Apr 20 | Jun 20 - Jul 20 | low-chill variety selection |
| plum | fruits_reliably | Mar 20 - Apr 10 | Jul 1 - Aug 20 | low-chill Japanese types |

The marquee delta: apple + both pears are **marginal** (inverse of Nevada's fruits_reliably),
per the Washington County "Fruits" elevation split (`usu_ext_wash_fruits`) -- the page recommends
apples and pears only for the county's higher-elevation towns (Central, Enterprise, New Harmony,
above 5,300 ft, outside this z8 belt). Region-level `chill_basis_seasoned`/`chill_basis_beginner`
carry the full elevation-split reasoning + the lowest-chill exceptions (apple: Dorsett Golden ~100,
Anna ~200, Ein Shemer ~100); `suitability_note_*` echo it briefly.

## cherry-sour TENSION FLAG (for content review)
cherry-sour is authored **fruits_reliably per the county** ("cherries" appear in the Fruits-page
low-elevation thrive column), BUT sour cherry is a genuinely high-chill crop (700-1000+ hr nominal)
and **Nevada called it marginal**. I followed the county listing as instructed, and hedged the prose
honestly: every register states sour cherry "needs more winter cold than most desert stone fruit,"
steers to "the lowest-chill selections and the coolest, highest site," and frames it as variety-
dependent rather than a sure crop -- but the stored `suitability` is fruits_reliably, not marginal.
**Reviewer should sanity-check the sour-cherry-vs-low-chill-band tension and decide whether to hold
fruits_reliably or drop it to marginal (matching Nevada + the biology).** This is the one verdict I'd
single out for a human call.

## Judgment calls / provenance
- **Windows are frost-anchored to Mar 30 / Nov 1.** Bloom/harvest were resolved from the St. George
  frost anchor using each crop's intrinsic Nevada-donor phenology offsets (bloom-vs-last-frost +
  maturation intervals), then rounded to clean display dates. This places the earliest bloomers
  (plum Mar 20, apricot/cherries/pears Mar 25) opening at/before the Mar 30 recorded frost -> the
  late-frost hazard the arid re-judgment names is honest and coherent; peach/nectarine bloom at the
  frost boundary; apple blooms after (it is marginal on chill regardless).
- **plantings[] block** kept the donor's single perennial establishment entry + its region-agnostic
  offsets; only the source id was swapped (unr_sp2007 -> usu_ext_wash_frost, frost-anchored windows).
- **resolved_from carries NO chill_hours** (per spec) -- just last_frost/first_frost. No gate needs
  it here (the no-fruit chill split reads region_chill_delivered and fires only for survives_no_fruit).
- **Sources (all USU, verified 2026-07-22):** `usu_ext_wash_fruits` (suitability + elevation split)
  and `usu_ext_wash_frost` (frost anchor + windows) on every cell; `usu_ext_peaches` added to peach +
  nectarine for the per-variety chill range (~500-1,050 hr). NO Nevada/UNR/UNLV ids anywhere.
- **nectarine** is not literally on the Fruits-page list, but peaches are and nectarine is a
  fuzzless peach (Prunus persica) -- prose states this explicitly; verdict rides on peach.

## Concerns
1. **cherry-sour verdict** (above) -- the one item needing a human ruling.
2. **Variety chill numbers** woven into `chill_basis` (apple 100-200 hr; sweet-cherry Royal Lee/
   Minnie Royal ~200-300 hr) are well-established horticultural figures cited under the region's
   fruit-authority page (`usu_ext_wash_fruits`), not verbatim on that page -- same convention the
   Nevada donor used (variety chill under unr_sp2007). Flagging for source-truth awareness; all are
   uncontroversial low-chill references, phrased "roughly"/"about".
3. All 9 harvest windows land in/before the 100 degF Jun-Aug core; sunburn is named as the dominant
   summer hazard across the stone fruit, consistent with the arid re-judgment (not humid brown-rot).
