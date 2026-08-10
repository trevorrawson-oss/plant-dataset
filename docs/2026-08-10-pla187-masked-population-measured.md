# PLA-187 -- the masked population, measured

**Measurement only. No canonical change, no promote, no gate wired.** Base canonical
`72284f02` (matches `LATEST.txt`), HEAD `097c013`. New instrument: `tools/hunt_footprint.py`
(+ 7 structural tests). Every count below is reproducible from it; every VERDICT about what a
document says is marked read or not-read, per the standing rule.

**The headline: the cleanup arc does NOT double.** The uncounted population is real -- **154
masked-only decisions over 57 crops** in the arc's own hunts -- but 95 of them are already
adjudicated by the arc's own declaration vocabulary, 21 more carry a same-institution pathed
document on the very node, and the genuinely unadjudicated residue is **38 decisions**, ~24% of
the 158 the arc adjudicated. Adding the 19 unadjudicated decisions found OUTSIDE every hunt
(§5), the honest growth number is **57 decisions, roughly a third of the arc, not a doubling.**

---

## 1. 125 vs 154 settled: it was never two counts, it was two footprints

`tools/hunt_footprint.py` now carries the canonical machine-readable footprint: all 32 ledger
hunts as `(region, source_id) -> (hunt#, campaign)`, the 7 citrus-residue pairs (mirrored
against `campaign_d_reprice.RESIDUE_HUNTS` by test), and the withdrawn `ucr_citrus` four.

Against that footprint, masked-only decisions -- `(crop, region, source_id)` units whose bare
rows are ALL masked, so no campaign ever counted them -- measure:

| basis | decisions | crops |
|---|---|---|
| the four campaigns (A/B/C/D + D-residue) | **154** | **57** |
| plus the withdrawn ucr_citrus hunts | 156 | 57 |

**The sizing agent's 154/57 is exact.** The 125 walk omitted hunts #3-6 (the four
`ca_*/ucanr_ext` hunts): their 28 campaign-A masked-only decisions plus 1 D-residue equal the
29-decision gap to the digit. The two walks never disagreed about the data; they disagreed
about which pairs count as "the arc", which is exactly what a prose-only footprint permits.
(The issue's "~56 crops" is also settled: 57.)

Both walks in the tool cross-check on every run: `bare_host_scan.scan` against an independent
walker that does not import it, 1,242 rows, byte-equal.

## 2. Per-hunt, per-campaign (`python3 tools/hunt_footprint.py`)

Decision-level, at `72284f02`:

| campaign | SOLE-visible | MASKED-ONLY |
|---|---|---|
| A California/UC | 17 | **71** |
| B region templates | 32 | **17** |
| C arid + Texas | 25 | **39** |
| D the tail | 9 | **26** |
| D residue (citrus) | 11 | 1 |
| withdrawn (ucr_citrus) | 9 | 2 |

The diagnostic's campaign C node table reproduces exactly (97 SOLE / 196 MASKED nodes),
including the boundary that helped the footprints diverge: hunts #14 and #21 split across the
C / D-residue line (#14 is 5 sole nodes under C plus 14 under D-residue; the diagnostic's "19"
was the undivided sum).

**Four hunts render as zero rows** (#24, #25, #26, #29 -- genuinely nothing left), and the tool
now prints them as ZERO ROWS instead of dropping them, so a fixed hunt and a filtered-away hunt
no longer render identically. The hunts that are invisible *only* because of the sole-filter --
#17 (0 sole / 6 masked-only), C's slice of #21 (0/1), A's #5 (0/6), D's #27 (0/1) and #28 (0/2)
-- print their masked columns.

## 3. A count of masked rows is not a count of defects: the classification

Every one of the 154 was classified (`--classify`), and 19 were READ (§4). Mechanism first:
**all 154 are masked by a real pathed co-source** -- zero are masked by a bare id string alone,
so the mask is never phantom. Then:

| class | n | what it means |
|---|---|---|
| DECLARED (53) + DECLARED+SAMEINST (42) | **95** | the crop carries an `open_findings` record naming the bare source id -- the SAME adjudication vocabulary campaigns C and D closed their SOLE decisions against (`okra_pilot_region_anchor_base_urls` shape). These are already adjudicated in the arc's own terms; they were just never *counted*. |
| SAMEINST-COVER | **21** | a pathed document from the same institution sits on the node (bare `uc_mg` beside pathed `ucanr_ext_mg_timeplanting`, bare `ufifas_ext` beside `uf_ifas_vh021`). The bare id is decoration beside its own institution's real document; drop-or-repoint is mechanical. |
| **NEITHER** | **38** | no declaration, no same-institution cover. **The real residue.** |

Per campaign, NEITHER: A 2, B 17, C 18, D 1. Campaign B's entire masked population is
unadjudicated (it never built a declaration vocabulary; its crops' findings are per-claim, not
per-anchor), where A's is almost entirely declared (63 of 71).

An id-spelling trap worth recording: `ufifas_ext` and `uf_ifas_vh021` are one institution in
two spellings. A prefix-literal family test calls them different and undercounts SAMEINST;
`hunt_footprint.family()` bridges the variants and is pinned by test.

## 4. Severity: what the 38 actually are (reads, not counts)

19 sampled decisions were read end to end (deterministic stride, stratified per campaign:
cell claims + co-source documents from `tools/.doc_cache`), plus targeted reads into the
NEITHER bucket. Composition of the 38:

- **15 are the RGV ornamental/herb block (hunt #13)** -- basil, bee-balm, borage, calendula,
  cosmos, echinacea, lemongrass, marigold, nasturtium, sunflower, sweet-alyssum, sweet-pea,
  viola, zinnia + mint's twin. Day-precise RGV windows whose only remaining co-sources are
  out-of-region or dateless pages (READ: bee-balm's is NC State's *Monarda didyma* taxonomy
  page; cosmos' is UC IPM's pest page, 2 month-tokens). **This is PLA-155's class, in a second
  region** -- the issue's "377 ornamental citations" lead, now with a bounded worklist.
  cosmos repeats it in `low_desert_az` (#14) and `warm_arid` (#30): 3 of its 4 regions.
- **10 are citrus credit cells in campaign B** -- grapefruit/lemon/lime/mandarin/orange-navel
  x {mid_south, mid_atlantic}. READ (grapefruit x2, orange-navel): the cells claim only
  `suitability: unsuitable`, co-sourced to real citrus documents (LSU freeze, UF/IFAS HS132).
  Severity per cell is LOW -- no window rests on the bare id -- but the bare `uada_ext` /
  `ncsu_ext` credit is exactly the unadjudicated-institutional-credit shape campaign B ruled on
  for fig and elderberry. One-sitting block adjudication.
- **5 are mid_atlantic vegetables masked by `vce_426_331`** (banana-pepper, bell-pepper,
  garlic, jalapeno, leek). READ: the Virginia guide has real Peppers/Garlic/Leeks rows, so the
  cover is plausible pending date verification -- likely benign.
- **1 is elderberry/mid_atlantic on `vce_426_331`. READ: the guide contains ZERO elderberry
  lines.** Discounting the bare host, the cells rest on nothing -- the mid_atlantic twin of the
  elderberry CASE 2 campaign B ruled for mid_south, unadjudicated because masked.
- **3 warm_arid melons** (cantaloupe, honeydew, watermelon) masked by
  `aggie-horticulture.tamu.edu/vegetable/` -- technically pathed, but an index page: the
  portal-genre defect wearing a path. Not in the doc cache; not read.
- **2 pears + lavender + grapefruit oddments** -- the pears (`ca_interior`/`uc_mg`, masked by
  `ucd_fruitnut`) are already OPEN-SCOPED terminal per the PLA-114 ruling; lavender/mid_south
  is the known governed repoint (`lavender_mid_south_uaex_zone_range_divergence` -- it does not
  name `uada_ext`, hence NEITHER by vocabulary while actually adjudicated).

Also checked, negative: **no concealment event created this population.** sugar-snap-peas'
`ca_interior` z8 cell already carried the pathed UC table beside bare `uc_mg` at `e65aa63a`,
BEFORE campaign A ran -- consistent with the diagnostic's B/C transition measurement. The
masked population predates the arc.

## 5. The blind spot one level up: pairs that never became hunts

The hunt list itself was derived from the SOLE view, so a pair whose bare rows were all masked
never got a hunt number at all. `--oof` finds **56 masked-only decisions on 23 such pairs**:
32 DECLARED, 5 SAMEINST-COVER, **19 NEITHER** -- concentrated in `northern_tier` cucurbits
(`iastate_ext`, `umd_ext` x acorn/butternut/spaghetti-squash, pumpkin, watermelon),
`northern_tier` stone fruit (`mu_ext` x peach, nectarine), and crop-level tomato credits
(`piedmont_mg`). None read yet; all carry pathed co-sources.

## 6. The two claims, kept separate

- **The scope choice was defensible and this measurement supports it**: 95 of 154 masked
  decisions were already adjudicated under the arc's declared-anchor standard, and 21 more are
  same-institution decoration -- for three-quarters of the population, sole-first pricing
  deferred work that was already done or trivial.
- **The completion signal was not**: "0 open" over the collapsed unit reads as "done" while 38
  in-footprint + 19 out-of-footprint unadjudicated decisions exist, and four kinds of hunts
  render identically to fixed ones. That defect is PLA-161's completion contract; this
  measurement is its sizing input, not its fix.

## 7. Recommendation on shape (a recommendation, not a decision)

**Neither a fifth campaign over 154 nor a re-scoping of the closed four.** The four campaigns'
closes hold under the standard they actually used; re-opening them to re-adjudicate 95
already-declared decisions would repeat the arc's over-count trap in a new costume.

Recommended: **one bounded campaign E over the 57 NEITHER decisions**, organized by block
rather than by hunt:

1. **The ornamental block (17): fold into PLA-155.** The RGV 15 + cosmos x2 are the same class
   as sweet-pea's wrong attribution, and PLA-155 already owns the "only sweet-pea has been
   read" caveat. One documents-first pass over the ornamental/vegetable-guide axis.
2. **The citrus-credit block (10): one sitting**, same ruling pattern as campaign B's closeout
   (fig/elderberry). Low severity, high count, single defect shape.
3. **elderberry/mid_atlantic: adjudicate now** -- the one read-confirmed rests-on-nothing case.
4. **The northern_tier + residual block (19 OOF + melons 3 + vce date-checks 5):** triage with
   the same classifier, read the co-sources, expect mostly benign for the vce vegetables and
   real portal-anchor questions for the cucurbits/stone fruit.
5. **The 21 SAMEINST-COVER decisions: mechanical cleanup pass** (drop or repoint the decorative
   bare id), no research; can ride along with any promote touching those crops.

Sequencing consequence for PLA-160-163: none forced. The arc does not double, so PLA-163 stays
its measured 26-decision size; PLA-161 gains this doc as the worked example its completion
predicate must refuse; the footprint table is now importable for all of them.

## 8. Corrections owed to the issue's own record

- "125-154" -> **154**; the 125 was a footprint-reconstruction omission (hunts #3-6), not a
  rival measurement. "~56 crops" -> 57.
- "5 hunts against a ledger of seven" (C header): reproduced, and the general form is worse --
  across the arc, 4 hunts are zero-row for good reasons and 5 more are invisible purely by the
  sole-filter; nothing distinguished them until now.
- The issue's campaign C table is node-level and exact (97/196 reproduced); its #14 row (19
  sole) is the undivided C + D-residue sum (5 + 14).
- New fact the issue could not know: **56 further masked-only decisions sit on pairs that never
  became hunts**, because the hunt list itself was SOLE-derived. 19 are unadjudicated.
