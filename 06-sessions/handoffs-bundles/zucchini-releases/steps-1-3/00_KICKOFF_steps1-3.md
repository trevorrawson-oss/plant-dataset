# KICKOFF -- Zucchini / Courgette Steps 1-3

You are authoring the gold-standard data arc for **zucchini-courgette** -- a **rail-rider**: a warm-season annual that rides the proven annual rails (NO new archetype, NO new tooling). This kickoff covers **Steps 1-3**: the source set, scalars + structured biology, and the variety set + companions. Same shape as the certified annuals (carrot, basil, green-beans) -- with one defining feature: it is a **succession crop**.

Operating model unchanged: you AUTHOR, Claude Code RELEASES (gates + promote). Don't invent a value with no T1 page behind it.

> **DRAFT for Trevor to voice + send.** Structural frame assembled by Claude Code; the final prompt is yours.

---

## 0. Preflight
Confirm the slice's crop SHA per `SLICE_INTEGRITY.md`: `8e3faa1f…`. Live base `LATEST.txt` = `0b767fc2…` (the blueberry cert).

## 1. Files
**Upload:** this doc; `zucchini-courgette_current_slice.json` (blank shell, your base); `SLICE_INTEGRITY.md`; `zucchini_sources_and_catalog.json` (the 122-parent source catalog -- reuse existing parents, mint specific-page sub-ids under a trusted parent rather than fragment); `LATEST.txt` / `CURRENT_STATE.md` / `STATE_HISTORY.md`.
**Project knowledge: NOTHING new -- the v2.0 checklist is already loaded; zucchini needs NO design spec (it is a standard warm-season annual on the proven rails). Skip the PK step.**

## 2. What zucchini-courgette IS (the shape)
- **archetype `warm_season_fruiting`** (the tomato / green-beans rails) -- frost-tender, grown as a warm-season annual everywhere; planted after the last spring frost, harvested before the first fall frost. The boundary scalars follow the grown-as-annual-in-all-zones model (cf. tomato / green-beans).
- **`start_method.start`** -- cucurbits resent root disturbance, so squash is usually **direct-sown** after frost; transplants (started 2-3 weeks early) are used for an early crop in short-season zones. Set `direct` or `both` -- **source it**. This selects the Step-3.5 region-build window shape (`direct` -> `direct_sow`; `both` -> transplant shape).
- **A prolific summer squash, harvested YOUNG and OFTEN** -- fruit at ~6-8 in / every 1-2 days at peak; the "pick small, pick constantly" beat is central (it belongs in the harvest prose at Steps 6-8, but informs `days_to_maturity` ~45-55 and the harvest-window framing now).
- **Monoecious + insect-pollinated** -- separate male and female flowers on the same plant; **`self_fertile: true`** (a single plant fruits; no second cultivar needed), but it needs POLLINATORS, and poor pollination gives misshapen / dropped fruit (a pollination NOTE, not apple-style cross-pollination machinery -- no `bloom_group`/`pollinizer`).
- **A SUCCESSION crop** (Section 3) -- a mid-season replacement planting is standard, both for steady supply and because squash vine borer + powdery mildew often kill the first planting by late summer.

## 3. Step 2 -- the SUCCESSION block (the rail-rider's defining feature)
Author the crop-level `succession_policy` fully (currently all null), mirroring the certified succession annuals (carrot / lettuce / green-beans). Carrot's shape for reference:
`{"suitable": true, "interval_weeks": <src>, "successions": <src>, "notify_days_before": 3, "max_successions_per_season": <src>, "window_type": "continuous", "pause_in_heat": <src>, "trigger": "last_frost", "tip_seasoned": "...", "tip_beginner": "..."}`
Source the real figures: succession interval for zucchini is typically a few weeks (a 2nd/3rd planting keeps fresh plants coming as borers/mildew take the first); zucchini LOVES heat, so `pause_in_heat` is likely **false** (the green-beans contrast to carrot) -- but source it. **NOTE:** the per-zone `successions_realized` integer is DERIVED later at Step 4 by `tools/derive_realized_successions.py` (gated by whole_crop_gate A8) -- do NOT author per-zone counts now; just the crop-level `succession_policy`.

## 4. Steps 1-3 deliverables (standard annual, same as carrot / basil / green-beans)
- **Step 1 -- source set:** T1 only (university-extension vegetable guides). Reuse catalog parents; mint specific-page sub-ids under a trusted parent, anchored to the exact page.
- **Step 2 -- scalars + structured biology:** `spacing_inches` (large plants, ~24-36 in -- source it), `days_to_maturity` (+ `_mid`; ~45-55, fast), `germination_temp_f` (warm), `sunlight` (full_sun), `water`, `difficulty`, the warm-season-annual hardiness handling, `soil`/`ph`, `fertilizer` (squash is a moderate-to-heavy feeder -- the contrast to the legume green-beans; source it), the universal watering/container blocks (watering: consistent moisture but **avoid wetting foliage -- powdery mildew nexus**), `start_method` (Section 2), `self_fertile: true` + the pollination note, and the full `succession_policy` (Section 3). N/A fields get N/A prose, never null.
- **Step 3 -- varieties:** `varieties.recommended[]` (e.g. Black Beauty, Costata Romanesco, Raven, Goldrush (yellow), Cocozelle, Dunja -- the `{name, ..., note}` per-variety shape, categorical `note`; include a compact/bush habit + a yellow + an heirloom for range).
- **Step 3 -- companions (NOT T1-gated; the three-tier provenance carries the honesty):** the certified carrot rich-object shape, vocab `research_backed` / `likely` / `traditional`. **Companions do NOT need a T1 anchor** -- well-known TRADITIONAL / folklore pairings are welcome, labeled honestly: `traditional` -> `verified_against_sources:false`, `verified_date:null`, `confidence` calibrated (`medium` for well-documented tradition, `low` for softer lore -- the onion all-traditional template). Use `research_backed` only where the research genuinely exists (e.g. nasturtium / the Three Sisters mechanisms UMN backs). (T1 still governs the BIOLOGY -- scalars/windows/pollination -- just NOT companions.) **Serve BOTH gardeners via the two-register split:** `good_beginner_seasoned[]` (visible to both registers) = the TIGHT high-signal set a first-season grower should act on (corn / pole beans / nasturtium -- the few that really matter, mostly research_backed); `good_seasoned[]` (seasoned-only) = the FULLER roster -- everything in tight PLUS the broader traditional catalog a seasoned grower recognizes (borage, aromatic herbs for borer deterrence, marigold, sweet alyssum/dill for beneficials, the radish trick). **INCLUDE bad companions even when only traditional** (do NOT default to empty -- an empty bad array is a weaker shape): real "keep it away from X" cautions go in `bad_seasoned[]` + `bad_beginner_seasoned[]` (`bad_beginner[]` is born empty), labeled traditional with honest reasons (e.g. potatoes -- competes for ground/water; fennel -- allelopathic, give it its own bed). Source what's sourceable, label the rest traditional, calibrate confidence to how well-documented-as-tradition each is.

## 5. Copy + sourcing rules
T1 only. No em dashes / no `--` in consumer copy; American English; `°F` symbol; "zucchini"/"squash" lowercase. Dual-register: pair `_beginner`/`_seasoned` only where the divergence is substantive; N/A prose never null. CP fields are suffixed siblings.

## 6. Deliverable
Hand back a patch (or the authored slice) + the post-author crop SHA + a note of any cut/demoted claim + any source-mint flags. Claude Code preflights vs `LATEST.txt`, runs `whole_crop_gate` + `register_completeness` + `register_fill`, and promotes. Then Step 3.5 (region shells -- the standard annual path), Step 4 (region fill + the A8 succession derivation), Steps 6-8 (the consumer prose + compounds -- pests led by squash vine borer / squash bug / cucumber beetle, disease led by powdery mildew + bacterial wilt), Step 9, cert.
