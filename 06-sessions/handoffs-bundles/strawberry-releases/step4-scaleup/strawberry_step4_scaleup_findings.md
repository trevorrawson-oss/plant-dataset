# strawberry Step 4 SCALE-UP -- the final 7 warm regions [anchor 13] -- FINDINGS

**Session:** strawberry_step4_scaleup (author lane, claude.ai)
**Date:** 2026-06-18
**Start SHA (canonical, expected at apply):** `78ebccffe5a50293799ec5fd5f3c1f44492076dc8640d9117e89da5167476255` (`strawberry_step4_fl_peninsula`)
**Scope:** fill the LAST 7 warm regions (11 cells) on the three proven shapes. NO new proof cells. `calendar[]` left `[]` for the Claude Code deriver.
**Result:** region fill now **10/10**; `whole_crop_gate` A2 region-fill gaps go to **0** after release.

> SHA note: the uploaded `strawberry_slice.json` is a single-crop working extract, not the full `crops_data_final.json` that `LATEST.txt` hashes, so its file hash does not equal the start SHA (expected). The patch is delivered as RFC-6901 ops over the strawberry `/regions` subtree with a `from`-guard on every op; Claude Code applies it against canonical under the real SHA gate.

---

## 1. The 7-region SOURCE findings (A5 -- each grown_as AND window verified per region, no templating)

| Region | Zones | grown_as | Shape | Window anchor (T1) | resolved_from |
|---|---|---|---|---|---|
| **low_desert_az** | 9 | **annual** | desert fall-plant PULLED | UA Coop Ext **AZ1667** (DeGomez, Growing Strawberries in Home Gardens) | null (month-resolved) |
| **ca_desert** | 9, 10 | **annual** | desert fall-plant PULLED | UA **AZ1667** primary + **UC IPM** cultural-tips (CA corroboration) | null (month-resolved) |
| **warm_arid** | 8 | **perennial** | spring-plant matted row | NMSU **H-324** (Yao & Flynn, Home Garden Strawberry Production in NM) | **populated** (frost-anchored) |
| **ca_north_coast** | 9, 10 | **annual** | coastal fall-plant winter-production | UC MG **Monterey & Santa Cruz** + **UC IPM** | null (month-resolved) |
| **ca_south_coast** | 9, 10 | **annual** | coastal fall-plant winter-production | UC MG **Monterey & Santa Cruz** + **UC IPM** | null (month-resolved) |
| **se_gulf** | 8, 9 | **annual** | Gulf fall-plant PULLED | LSU AgCenter **Pub 3363/3364** (Fontenot et al., Strawberries) | null (month-resolved) |
| **hawaii_tropical** | 11 | **perennial** (NOT year_round) | cool-elevation niche | UH **CTAHR** Hawaii County (+ Kokua Hawaii Fdn ed. sheet) | null (frost-free) |

**Three DISTINCT annual sub-windows, each sourced separately (A5 anti-cross-region):**
- Desert fall-pull: plant **mid Sep - mid Nov**, harvest late winter to spring (Mar-May), pulled at summer onset by heat.
- Coastal fall-winter: plant **mid Aug - Nov**, peak **May-Jun**, replaced after the first full season; south coast carries an earlier production tail (midwinter start in the warmest districts).
- Gulf fall-pull: plant **early Oct - mid Nov**, harvest late Nov into spring (to ~early Jun), pulled in early summer by humid-summer disease.

These are NOT interchangeable, and none was templated from `fl_peninsula` or `ca_interior`.

---

## 2. TWO decisions surfaced for your ratification (genuine divergences from the kickoff sketch)

### Decision A -- `warm_arid` is PERENNIAL, not annual (A5 overturn -- the bigger of the two)

The README/DESIGN_SPEC sketch grouped `warm_arid` with "the interior deserts on the **ca_interior summer-plant annual** template." **The source overturns this.** The correct z8 interior-arid authority, **NMSU Guide H-324**, grows strawberries as a **spring-planted perennial matted row**:
- Plant dormant crowns **in spring after danger of hard frost** (cool weather aids establishment).
- June-bearer flower buds **initiate the previous fall** under short days; **one concentrated late-spring crop**.
- **Renovate immediately after harvest** (before Jul 15); matted-row **beds last 3-4 years**.
- Southern/warmer NM needs afternoon shade + high-pH iron management.

**AZ1667 independently corroborates:** areas **above 3,000 ft** are spring-planted perennials (3-4 fruiting years, runners, renovation) -- the same elevation/climate class as z8 `warm_arid`, and explicitly distinct from the below-3,000-ft low desert.

**Consequence:** `warm_arid` is the ONLY new cell on the **perennial frost-relative shape** (same as `northern_tier`: dormant + bloom + harvest + renovation; **NO season_over**). z8 carries frost (`zone_frost_data`: last_spring Feb 15, first_fall Dec 1), so it **frost-anchors** -- `resolved_from` populated, arms use `from: last_frost` + offsets. This is exactly the A5 case the kickoff anticipated ("genuinely source-decided; don't assume desert or interior"). **Authored as perennial.** If you want it re-litigated, say so before promotion.

### Decision B -- `hawaii_tropical` grown_as is the WEAKEST of the 7 calls (flagged finding)

The onion hawaii lesson holds: **NOT year_round** despite frost-free z11. CTAHR documents Waimea (Hawaii Island) as a major production area and the crop is an **upcountry / cool-elevation niche** (Kula on Maui, Waimea); a "year-round" Hawaiian strawberry **supply** exists only because commercial farms **move harvest up/down the mountain** with the seasons -- something a fixed home garden cannot do. The upcountry U-pick/home season runs roughly **Feb-Jun**.

**grown_as authored as PERENNIAL** (cool, frost-free, no killing summer heat or winter at elevation favor a multi-year bed). **But:** no clean CTAHR *home-garden* lifecycle statement exists -- the perennial read is inferred from the niche + frost-free conditions. **Logged as the residual open finding for Step 5** (`blocks_launch:false`), to be confirmed against a dedicated CTAHR strawberry publication if one can be obtained, or softened to an explicitly informational note. This mirrors how the onion/zinnia hawaii cells were handled (flagged inferential).

---

## 3. Anchoring + new source IDs to mint (Claude Code RELEASE lane)

Per-rule-entry AND per-cell `anchoring_urls`, one entry per source ID, `verified: 2026-06-18`. New page sub-IDs to mint under trusted parents at release (mirrors `uf_ifas_hs403` last round):

| New sub-ID | Parent (tier) | Publication | Used by |
|---|---|---|---|
| `uariz_ext_az1667` | uariz_ext (T1) | UA Coop Ext AZ1667, Growing Strawberries in Home Gardens | low_desert_az, ca_desert |
| `nmsu_ext_h324` | nmsu_ext (T1) | NMSU Guide H-324, Home Garden Strawberry Production in NM | warm_arid |
| `ucanr_mg_monterey_santacruz` | uc_anr / ucanr (T1) | UC MG Monterey & Santa Cruz, Growing Strawberries in the Home Garden | ca_north_coast, ca_south_coast |
| `lsu_agcenter_3363` | lsu_agcenter (T1) | LSU AgCenter Pub 3363/3364, Strawberries | se_gulf |
| `ctahr_hawaii_county` | ctahr / uh_manoa (T1) | UH CTAHR Hawaii County diversified-ag (produce) page | hawaii_tropical |

Existing reused: **`uc_ipm`** (cultural-tips, the coastal CELL-level harvest anchor -- "heaviest production May-June," the same anchor `ca_interior` uses).

URLs (all fetched + read this session):
- AZ1667: `https://extension.arizona.edu/sites/default/files/2024-08/az1667-2015.pdf`
- NMSU H-324: `https://pubs.nmsu.edu/_h/H324/index.html`
- UC MG M&SC: `https://ucanr.edu/sites/default/files/2018-03/281247.pdf`
- UC IPM cultural-tips: `https://ipm.ucanr.edu/PMG/GARDEN/FRUIT/CULTURAL/strawberrytime.html`
- LSU 3363/3364: `https://www.lsuagcenter.com/NR/rdonlyres/F364192A-744D-4E43-B95E-E9EBD75CDF4E/100278/Pub3364Strawberries4Cweb.pdf`
- CTAHR Hawaii County: `https://www.ctahr.hawaii.edu/hawaii/Plants.aspx`

---

## 4. Release flags for Claude Code

1. **`calendar[]` left `[]` on all 11 cells -- derive per cell.** Expected emergent shapes:
   - **season_over** emerges for the PULLED annual cells: `low_desert_az` z9, `ca_desert` z9/z10, `se_gulf` z8/z9 (clean summer no-plant gap).
   - **NO season_over** for the perennial cells `warm_arid` z8 (dormant+renovation cycle, frost-relative) and `hawaii_tropical` z11 (dormant cycle, frost-free).
   - **VERIFY the deriver's branch on the coastal cells** (`ca_north_coast`, `ca_south_coast`): the mild-coast fall-to-summer windows WRAP without a clean summer no-plant gap, so the deriver may NOT emit season_over (carried-vs-pulled is emergent from whether windows wrap or leave a gap). Confirm the deriver does the right thing here rather than forcing a token.

2. **FROST RECONCILE (the onion NT lesson):** `warm_arid` z8 is the only frost-anchored new cell -- reconcile its `resolved_from` (`last_frost: Feb 15`, `first_frost: Dec 1`) against the live `zone_frost_data` z8 and re-derive the offset-based dates. The `plant_out` date I wrote (`Mar 1 - Mar 22`) is illustrative of the `from: last_frost`/`offset_days:-14`/`window_days:21` arm; the deriver is authoritative.

3. **PRE-EXISTING ORPHAN NULL KEYS (surface before gate):** the 3.5 shells left null orphan region-root keys NOT present in the filled reference cells:
   - `ca_desert.zone_10_desert_fold` = null
   - `ca_north_coast.zone_8_presence` = null
   - `ca_south_coast.zone_8_presence` = null
   These were **left untouched** by this patch (author lane does not delete structural keys). They are the same *class* as the z11 `season_bound` key that HALTed `register_completeness_gate` in onion. **Recommend deciding their disposition at release** (drop them, or rule them) and **run `register_completeness_gate` explicitly** -- `whole_crop_gate` B + `release_verify` do not catch a novel unruled prose/null key; the CURRENT_STATE regen is the backstop.

4. **Mint the 5 new sub-IDs** (section 3) under their trusted parents with `_admission_provenance`, inheriting parent tier (all T1).

5. **track flip:** the annual regions' `plantings[0].track` was flipped `perennial -> annual` (shell default is perennial); `warm_arid` + `hawaii_tropical` keep `perennial`. Matches the filled fl_peninsula (annual) / northern_tier (perennial) precedent.

---

## 5. Self-verification done (author lane, against the slice)

- **Patch applies clean under a content-SHA gate** with a `from`-guard on every one of the **225 ops** (0 guard failures).
- **All 11 cells filled**; `grown_as`/`track`/`resolved_from` shapes correct per region (annual+null, perennial+populated for warm_arid, perennial+null for hawaii); **`calendar[]` empty on all 11**.
- **Collateral:** the 3 filled proof cells (`northern_tier`, `ca_interior`, `fl_peninsula`) and ALL non-`regions` crop keys are **byte-identical** before/after.
- **Cell + arm + region-root key-set parity** vs the filled reference cells: clean (the only region-root EXTRAs are the 3 pre-existing orphan nulls in section 4.3, not introduced here).
- **Anchoring conformance:** every cell and every arm has `anchoring_urls` keys == `sources` (one per source ID). 0 mismatches.
- **D9-style checks:** every cell `grown_as in {perennial, annual}`; no tree keys (`suitability`/`chill_hours_delivered`); dual-register pairs all distinct (region_notes + grown_as_note).
- **Copy conventions (user-facing strings only):** 0 em-dashes, 0 en-dashes, 0 `--`, 0 "degrees F" text, 0 non-US spellings. (The 7 `--` in `plantings_provenance` are BACKEND prose, allowed by convention -- matches the filled cells.) Prose spells "degrees Fahrenheit" throughout.

---

## 6. What's next (after this patch releases -> region fill 10/10)

**Step 5** (whole-crop verification): source FIDELITY re-fetch of every cited window/number; the **`hardiness_zone`/`reliable_fruit_zone` boundary-scalar decision applied ONCE** (your call, Option-1 lean -- leave scalars as perennial-survival/reliable-perennial semantics; the `grown_as: annual` z9-11 cells carry the annual reality); the chill figure; and **resolve the hawaii grown_as open finding** (Decision B). -> **Steps 6-8** (bulk prose incl. the deferred day-neutral `type_selection_*` story + the ca_interior small fall crop) -> **Step 9** -> **Step 11 cert + the flip**.
