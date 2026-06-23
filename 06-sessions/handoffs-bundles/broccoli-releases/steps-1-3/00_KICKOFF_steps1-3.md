# KICKOFF -- Broccoli Steps 1-3

You are authoring the gold-standard data arc for **broccoli** -- a **rail-rider**: a COOL-season annual on the proven cool-season rails (NO new archetype, NO new tooling). This kickoff covers **Steps 1-3**: the source set, scalars + structured biology, and the variety set + companions. Same shape as the certified cool-season annuals **lettuce-leaf and carrot** -- with one defining feature: it is a **succession crop** (spring + fall).

Operating model unchanged: you AUTHOR, Claude Code RELEASES (gates + promote). Don't invent a value with no T1 page behind it.

> **DRAFT for Trevor to voice + send.** Structural frame assembled by Claude Code; the final prompt is yours.
> **PARALLEL:** zucchini Steps 1-3 is being authored in a separate claude.ai session against the same base. Independent slices; Claude Code releases them one at a time. No collision.

---

## 0. Preflight
Confirm the slice's crop SHA per `SLICE_INTEGRITY.md`: `2f81cd13…`. Live base `LATEST.txt` = `0b767fc2…` (the blueberry cert).

## 1. Files
**Upload:** this doc; `broccoli_current_slice.json` (blank shell, your base); `SLICE_INTEGRITY.md`; `broccoli_sources_and_catalog.json` (the 122-parent catalog -- reuse existing parents, mint specific-page sub-ids under a trusted parent); `LATEST.txt` / `CURRENT_STATE.md` / `STATE_HISTORY.md`.
**Project knowledge: NOTHING new -- the v2.0 checklist is already loaded; broccoli needs NO design spec (it is a standard cool-season annual on the proven lettuce/carrot rails). Skip the PK step.**

## 2. What broccoli IS (the shape)
- **archetype `cool_season_annual`** (the lettuce-leaf / carrot rails) -- grown in the COOL shoulders (spring + fall); HEAT is the enemy. The boundary scalars follow the cool-season-annual model.
- **The heat contrast (the defining rail difference from a warm-season crop):** broccoli BOLTS / "buttons" (forms tiny premature heads) in heat, so warm regions grow it as a spring crop that must mature before summer + a fall crop planted as the heat breaks, with a **mid-summer no-grow gap**. This is why `succession_policy.pause_in_heat` is **TRUE** (the lettuce/carrot pattern; the INVERSE of the warm-season rail-riders) and why warm-region region cells will carry `heat_pause` at Step 4. Source the heat/bolting thresholds.
- **`start_method.start`** -- broccoli is commonly **TRANSPLANTED** (started indoors ~4-6 weeks ahead for the spring crop; direct-sown or transplanted for fall). Set `both` or `indoors` -- **source it** (this is the contrast to lettuce/carrot, which are `direct`). It selects the Step-3.5 region-build window shape (`both`/`indoors` -> transplant shape).
- **Harvested for the HEAD (immature flower buds), BEFORE the buds open/yellow** -- then **side shoots** keep producing (the cut-and-come-again secondary harvest). Because you harvest pre-flower, **pollination is not a consumer concern** (no `bloom_group`/`pollinizer`; leave `self_fertile` per the cool-season-annual convention / N/A -- it is eaten before it flowers).
- **A heavy feeder + a brassica** -- relevant to `fertilizer` (needs steady N, the contrast to legumes) and to `rotation` (clubroot is the brassica rotation driver -- author `rotation` with the avoid-after-brassicas caution).

## 3. Step 2 -- the SUCCESSION block (the rail-rider's defining feature)
Author the crop-level `succession_policy` fully (currently all null), mirroring lettuce-leaf / carrot. Carrot's shape for reference:
`{"suitable": true, "interval_weeks": <src>, "successions": <src>, "notify_days_before": 3, "max_successions_per_season": <src>, "window_type": "continuous", "pause_in_heat": true, "trigger": "last_frost", "tip_seasoned": "...", "tip_beginner": "..."}`
For broccoli, `pause_in_heat: true` (cool-season -- it cannot head in summer heat); source the interval (small successions within the spring + fall windows). **NOTE:** the per-zone `successions_realized` integer is DERIVED later at Step 4 by `tools/derive_realized_successions.py` (gated by whole_crop_gate A8). The spring/fall double-window geometry is materialized at Step 4 region fill -- do NOT author per-zone counts or windows now; just the crop-level `succession_policy`.

## 4. Steps 1-3 deliverables (standard cool-season annual, same as lettuce / carrot)
- **Step 1 -- source set:** T1 only (university-extension vegetable guides). Reuse catalog parents; mint specific-page sub-ids under a trusted parent, anchored to the exact page.
- **Step 2 -- scalars + structured biology:** `spacing_inches` (~18 in -- source it), `days_to_maturity` (+ `_mid`; transplant-to-harvest ~55-70, longer from seed), `germination_temp_f` (cool-season germination range), `sunlight` (full_sun), `water`, `difficulty`, the cool-season-annual hardiness handling, `soil`/`ph`, `fertilizer` (heavy N feeder -- source it), the universal watering/container blocks, `start_method` (Section 2), and the full `succession_policy` (Section 3). N/A fields get N/A prose, never null.
- **Step 3 -- varieties:** `varieties.recommended[]` (e.g. Calabrese / Green Magic / Belstar / De Cicco (heirloom, side-shoot-heavy) / Waltham 29 (fall/overwinter) / a heat-tolerant one for the spring-into-summer edge -- the `{name, ..., note}` per-variety shape, categorical `note`).
- **Step 3 -- companions (NOT T1-gated; the three-tier provenance carries the honesty):** the certified carrot rich-object shape, vocab `research_backed` / `likely` / `traditional`. **Companions do NOT need a T1 anchor** -- well-known TRADITIONAL / folklore pairings are welcome, labeled honestly: `traditional` -> `verified_against_sources:false`, `verified_date:null`, `confidence` calibrated (`medium` for well-documented tradition, `low` for softer lore -- the onion all-traditional template). Use `research_backed` only where the research genuinely exists. (T1 still governs the BIOLOGY -- scalars/windows/pollination -- just NOT companions.) **Serve BOTH gardeners via the two-register split:** `good_beginner_seasoned[]` (visible to both registers) = the TIGHT high-signal set a first-season grower should act on (the few pairings that really matter, mostly research_backed); `good_seasoned[]` (seasoned-only) = the FULLER roster -- everything in tight PLUS the broader traditional catalog a seasoned grower recognizes. **INCLUDE bad companions even when only traditional** (do NOT default to empty -- an empty bad array is a weaker shape): real "keep it away from X" cautions go in `bad_seasoned[]` + `bad_beginner_seasoned[]` (`bad_beginner[]` is born empty), labeled traditional with honest reasons. For broccoli, tried-and-true pairings include aromatic herbs (dill, etc.), alliums, and cool-season intercrops (lettuce/spinach); the recurring bad-companion folklore is other brassicas + strawberries/nightshades (competition / rotation / clubroot). Source what's sourceable, label the rest traditional, calibrate confidence to how well-documented-as-tradition each is.

## 5. Copy + sourcing rules
T1 only. No em dashes / no `--` in consumer copy; American English; `°F` symbol; "broccoli" lowercase. Dual-register: pair `_beginner`/`_seasoned` only where the divergence is substantive; N/A prose never null. CP fields are suffixed siblings.

## 6. Deliverable
Hand back a patch (or the authored slice) + the post-author crop SHA + a note of any cut/demoted claim + any source-mint flags. Claude Code preflights vs `LATEST.txt`, runs `whole_crop_gate` + `register_completeness` + `register_fill`, and promotes. Then Step 3.5 (region shells -- the standard transplant annual path), Step 4 (region fill + the spring/fall double-window + the A8 succession derivation + heat_pause), Steps 6-8 (consumer prose + compounds -- pests led by the cabbage-worm complex / aphids / flea beetles / cabbage root maggot, disease led by clubroot / black rot / downy mildew), Step 9, cert.
