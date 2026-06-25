# Incognito Audit, Independent Adversarial Re-Audit Before the Scale Phase

**Date:** 2026-06-25
**Auditor:** Claude Code session, independent. Five clean-context sub-auditors, blind to the prior
gs-arc audit docs, each instructed to treat "18/18 / gates catch every class / ship-ready" as a CLAIM
TO TEST, not ground truth. The orchestrator independently re-verified the three highest-stakes findings
by direct inspection (greps shown below) rather than trusting the sub-auditors.
**Dataset SHA at audit:** `6c72f8b9d0a785e4e940c8ebd6443dd77e0abdd4` (content shasum `b39f1453`,
matches LATEST.txt; plant-astro submodule pinned at the same). Confirmed by every agent, not quoted.
**Discipline:** READ-ONLY. All defect injection done in scratch copies; canonical untouched and clean
throughout. Every gate result proven to reflect the modified scratch file (gates take an explicit path
arg; none hardcode the canonical). Scan -> verify -> report; effective plant windows (plant_out UNION
calendar plant tokens) used for every date check.

---

## 1. Bottom line

The **foundation (the 18) is sound**; the **armor has real, scale-propagating holes**; and "ship-ready"
is **overstated on display-readiness**. Precise verdict:

- **Gate-clean: CONFIRMED 18/18.** Independently re-ran `whole_crop_gate` on all 18 -> PASS, 0
  violations. `release_verify`'s apparent "concerns" are cross-archetype reference artifacts (check E
  comparing a tree/citrus against the lettuce annual exemplar); clean when re-run with an archetype-
  matched `--ref`. The dataset itself is sound at this SHA.
- **Dates: SOUND. 0 wrong-season errors across 64 independently-sampled cells** (30 West/Desert + 34
  SE/Gulf/FL/Hawaii/North), ~78% exact match, **100% season-correct**, against live UA AZ1005 / UC ANR /
  NMSU / UF-IFAS / UGA / UMN / USU / UH-CTAHR. The hard part (accurate regional dates) holds up.
- **Display-ready: REFUTED for 18/18.** 3 certified crops (`zucchini-courgette`, `broccoli`,
  `lavender`) render **zero** guide pages and **404 on the visitor's default zone**. Effectively 15/18
  shippable on the website. A gate-clean crop that does not render is exactly the separate-bar failure
  the audit was told to find.
- **Armor for scale: NOT YET. Two structural gate blind spots would propagate x105**, plus a render
  gap that silently drops gate-clean crops. NO-GO on scaling to ~105 until these are hardened (see Sec 5).

---

## 2. Gate blind spots found (the armor for the scale phase)

Verified by injecting a defect of the class into a scratch copy and confirming the gate did NOT fail it.

| # | Blind spot | Owning gate status | Scale risk | Evidence |
|---|---|---|---|---|
| **B1** | **Annual calendar token placement is never re-derived.** A `cold_pause` on a plant month, a `heat_pause` on a harvest month, an unbacked `heat_pause`, or a calendar contradicting its own `plant_out` all PASS. The orchestrator runs only `annual_coherence_violations` (length + token enum + heat_pause-month alignment). The actual drift defense, `annual_calendar_violations()`, **exists in code but has ZERO callers.** | **Unwired** (`annual_calendar.py:172` defined; orchestrator imports only `annual_coherence_violations`) | **HIGH.** 10/18 current crops are annuals (200 cells); the ~105 to author are mostly annuals. The bulk of calendar content has no mechanical backstop. | Injected pause-on-plant (onion, cherry-tomato), pause-on-harvest (basil, onion), unbacked heat_pause, photoperiod-window mismatch -> all PASS. grep: `annual_calendar_violations` has no callers. |
| **B2** | **Deciduous-tree variety chill type is ungated.** A string/legacy `chill_hours_required: "400-500"` on a peach/apple variety passes every gate. The only per-variety chill-type lock, `berries_woody_variety_chill_violations`, is hard-scoped `if calendar_basis != "berries_woody": return []` (blueberry only). `perennial_gate` consumes chills via `isinstance(v,(int,float))` and silently SKIPS non-numeric values. | **No owner** for `perennial_chill_gated` trees | **HIGH.** Propagates to every future stone/pome fruit (cherry, plum, pear, apricot...). Worse than a display miss: dropping a numeric variety chill silently shifts peach's no-fruit-split `floor` (400 -> next numeric 800), which decides whether a `survives_no_fruit` cell must carry or omit a calendar -- a bad string can silently reclassify biological calendar cells. | grep: gate docstring "Fires ONLY for calendar_basis == berries_woody"; both gate fns `return []` off-basis. Injection on a peach variety -> `GATE: PASS`. |
| **B3** | **Unbacked heat_pause accepted.** A fabricated summer pause (token + self-consistent `heat_pause.months`, zero thermal/climate justification) ships clean. No gate requires a heat_pause to be backed by temperature evidence. | No owner | MED (correctness of the "too hot to sow" claim at scale) | Injected token + months, no backing -> PASS. |
| **B4** | **Photoperiod gate is enum + coverage only.** No rule links a variety's `day_length_type` to its planting-window shape; a short-day onion with a long-day-shaped schedule is invisible. | Partial (`photoperiod_gate` checks enums + type coverage, not window fit) | MED | Injected onion plant_out -> Jan 1-15 with valid enums -> PASS. |
| **B5** | **Companion reachability is crop-level, not per-entry.** A single good placed in a beginner-only bucket while other goods are seasoned-readable is not flagged (that companion is invisible to seasoned readers). Separately, a seasoned-bucket companion with `why_seasoned: null` is counted "ruled_empty" by the always-on gate (apple ships 5). | Partial (`companion_shape_gate` enforces crop-level reachability only) | LOW-MED | Injected per-entry beginner-only good among seasoned goods -> not flagged. |

**No over-flags on the primary structural or temporal gates.** Confirmed the gates correctly PASS
legitimate archetype variation: lavender (bloom-model, no harvest), the four by-design ratio-less crops
(lemon/onion/lavender/blueberry, npk_ratio null + tag), overwintered onion (harvest far from plant+DTM),
split spring+fall heat_pause gaps, succession crops. grep-confirmed there is **no** naive
"harvest must follow plant_out within days_to_maturity" rule anywhere, so no cry-wolf risk on the
subtle crops.

**One over-flag, on a non-always-on gate:** `register_fill_gate` flags structured-N/A fields
(`{"applicable": false, ...}`) as unauthored, over-flagging carrot/cherry-tomato/beefsteak. Note
`register_fill_gate` and `register_completeness_gate` are **not wired into the always-on
`whole_crop_gate`** (run standalone at flip); as-run, `register_fill` currently fails 6/18 certified
crops (a mix of this over-flag and null `why_*` prose the always-on gate never sees). So "register
clean" is not guaranteed by the always-on armor.

---

## 3. Source-truth: dates verified against live Tier-1 extension sources

64 cells independently sampled and machine/grid-checked where possible. **0 wrong-season errors.**

| Cluster | Cells | MATCH | MINOR | WRONG | Strict | Season-correct |
|---|---|---|---|---|---|---|
| West + Desert SW (CA, AZ, NM) | 30 | 25 | 5 | 0 | 83% | 100% |
| SE/Gulf/FL/Hawaii + Northern tier | 34 | 25 | 9 | 0 | 73.5% | 100% |
| **Total** | **64** | **50** | **14** | **0** | **~78%** | **100%** |

Onion day-length logic verified correct end to end: short-day in desert/low-desert/SE-Gulf/FL,
intermediate/long-day in warm_arid (NMSU CR563 matched verbatim) and the northern tier.

**MINOR nits surfaced (all same-season, ~3 to 6 weeks, none severe; candidates for a future touch):**
- `onion` fl_peninsula z10/z11: the North-FL Sep-Dec window is applied to South FL; UF-IFAS South lists
  "Oct" -- the Nov-Dec tail is ~1-2 months late for S-FL bulbing. Still fall-plant/spring-harvest.
- `beefsteak-tomato` se_gulf z8: carries a Sep `plant` calendar token ~6-8 weeks past UGA's fall window
  (Jun15-Jul15) and inconsistent with its own `plant_out` (Jul 1-20); marginal ripening before z8 frost.
- `green-beans-bush` northern z3: Jul 15 back-edge sow matures ~1 week before the Sep 15 frost; UMN caps
  northern-MN beans at end of June. ~2-3 weeks optimistic.
- `carrot` northern z3: Apr-Jun plant tokens have no corresponding summer harvest window (only the Jul
  sowing reaches the Sep-Oct harvest); Apr token early for z3 cold soil.
- Low-desert AZ warm-crop fall succession (tomato, beans) set ~3-5 weeks later than AZ1005's Jul-Aug.

Coverage honesty: FL (UF VH021) and GA (UGA C963) extracted in full = high confidence. AZ1005 PDF was
grid-reconstructed via pdfminer (encoded grid would not WebFetch). Hawaii (UH B-91) is qualitative only
(month grid garbled) = lower confidence on the 5 Hawaii cells. A few UMN crop pages 404'd; those leaned
on UMN bean text + USU DTM + explicit frost math.

---

## 4. Re-derive 18/18 + render

- **Certified count independently derived from JSON:** of 123 crops, exactly 18 carry
  `status == verified_gs_arc` AND `launch_ready_core` AND `launch_ready_seasoned`; 105 are shells
  (status null). "18 certified + ~105 shells" CONFIRMED.
- **Gates:** 18/18 `whole_crop_gate` PASS. `release_verify` standalone "concerns" all resolve to check-E
  cross-archetype reference noise (clean with matched `--ref`); substantive checks (calendar coherence,
  user-facing dash/degree scan, region_notes, value divergence, region_chill_delivered shape) clean 18/18.
- **Build:** `npm run build` -> exit 0, 321 pages, ~43s, zero warnings.
- **Render spot-check (lemon / blueberry / lettuce-leaf):** all data-bearing fields render, no blanks.
  Confirmed the two recent migrations render correctly: blueberry's string->numeric chill gauge shows
  numeric per-variety hours; the two-row sow+harvest calendar renders with harvest as its own row.

### 4a. KEY display-readiness defect (independently re-verified by the orchestrator)

3 certified crops render **no guide page at all**: `zucchini-courgette`, `broccoli`, `lavender` have
**0 zone directories** in `dist/` (vs 9 for every other zoned crop). Their hub page renders the default
Zone-9 tile as a **live `<a href=".../zone-9/">` link, not "coming soon"** -> a hard 404 on the
visitor's default zone.

**Root cause:** `src/pages/guides/crops/[crop]/[zone].astro:101` hardcodes
`BUILT_CROPS = [14 slugs]`; these 3 were never added, so `getStaticPaths` emits nothing for them even
though their data is gate-clean and region cells are 10/10 filled. The route comment claims "new crops
flow through without editing this list" -- false; it only flows for crops already in the allowlist. This
is a one-line route omission (plant-astro), not a dataset defect.

### 4b. App surface

`app-preview` (Astro-prerendered CropDetail) renders statically with a curated demo subset, not the full
18. The **real Expo app (`~/plant-app`) cannot be statically rendered** to inspectable HTML here
(needs Metro / `expo export`); CURRENT_STATE.md notes the Expo app still needs the two-row harvest +
chill-card port the website got, so its display layer is known to **lag** the website on the same data.

---

## 5. GO / NO-GO on scaling to ~105 with the current armor

**NO-GO until the armor is hardened.** The foundation is sound, but three holes would silently
propagate across the bot-authored 105, and the source-truth sample (the un-gateable layer) is the only
thing that would catch some of them after the fact.

Harden first (each is "write the scanner, wire it in, fix existing to green," the test-first convention):

1. **Wire `annual_calendar_violations` into `whole_crop_gate`** (B1). It already exists; it is the annual
   analog of the tree/berry/woody re-derivation gates that DO run. Highest leverage: annuals are most of
   the 105. Reconcile it against the legitimate hand-authored shapes the deriver currently can't
   reproduce (onion `season_over`, summer heat_pause cells, multi-cycle/heat-inverted cells) so it
   catches drift without over-flagging.
2. **Extend the variety-chill type lock to all chill-gated archetypes** (B2), not just `berries_woody`.
   A `perennial_chill_gated` deciduous-tree analog (numeric `chill_hours_required`, reject string/legacy
   `chill_hours`) closes the peach/apple gap and protects every future stone/pome fruit, including the
   no-fruit-split `floor` it silently corrupts.
3. **Make the website render derive from the certified set** (4a). Replace the manual `BUILT_CROPS`
   allowlist with the certified roster, or add a build-time assertion that every certified crop emits its
   zone pages. Otherwise each new crop silently 404s until someone edits a route by hand -- a scale footgun.
4. **Wire `register_fill` + `register_completeness` into the always-on gate** and fix the
   structured-N/A (`applicable:false`) over-flag (B5/register). Then a bot crop's null register prose is
   caught at gate time, not only if someone remembers to run them at flip.
5. **Secondary, lower priority:** require thermal backing for `heat_pause` (B3); link photoperiod
   `day_length_type` to window shape (B4); per-entry companion seasoned-reachability (B5).

Keep doing: the **adversarial source-truth sample per batch** is working (0 wrong-season across 64
cells). It is the only defense for the un-gateable dates layer; treat it as a required release-QA step,
not a gate. The MINOR date nits in Sec 3 are cleanup, not blockers.

**One-line answer to the charter questions:** (a) the 18 are genuinely gate-clean and the dates are
sound, but they are **15/18 display-ready, not 18/18** until the BUILT_CROPS route is fixed; (b) the
armor is **not yet** sufficient to bet 105 crops on -- close B1, B2, and the render-derivation gap first.

---

## 6. Comparison note (added by the orchestrator, who had seen the prior audit)

The sub-auditors were blind; this comparison is mine. The prior gs-arc audit (2026-06-24) correctly
caught the systematic display/companion/chill/npk classes and the dates held up the same way. **This
incognito pass adds three findings the prior audit did not surface**, precisely because the prior audit
trusted the gates as built rather than stress-testing them: B1 (the existing annual re-derivation gate is
unwired), B2 (variety-chill type is ungated for deciduous trees, only berries_woody), and the
render gap (3 certified crops 404 on the default zone via the stale BUILT_CROPS allowlist). The
self-described "armor" has gaps the coherence gates cannot see, which is exactly the thing to know before
betting 105 crops on it.

---

## 7. UPDATE, tier-1 fixes applied (2026-06-25, same session, Trevor-approved)

Two bounded, low-history fixes were applied test-first immediately after the audit. The dataset
JSON (`crops_data_final.json`) was NOT touched; these are a gate-code addition and a website-route
change. Neither is committed (awaiting Trevor's review).

### Fix A, B2 closed: deciduous-tree variety-chill type lock
- **Added** `perennial_variety_chill_violations(crop)` to `tools/perennial_gate.py` (+ a bool-safe
  `_is_number`), the deciduous-tree analog of the berries_woody A21 lock: every recommended
  variety on a `perennial_chill_gated` crop must carry a NUMERIC `chill_hours_required` and no
  legacy string `chill_hours`. No-op off `perennial_chill_gated` (citrus/annuals unaffected).
- **Wired** it into `tools/whole_crop_gate.py` as **A22** (so it actually runs at cert -- the B1
  lesson).
- **Tests** (`tools/test_perennial_gate.py`, cases 23-29): RED (ImportError) -> GREEN. Covers
  string chill, legacy `chill_hours`, None, bool, annual no-op, evergreen no-op.
- **Verified:** all 18 certified crops still `GATE: PASS` (no regression / no over-flag); a scratch
  peach with `chill_hours_required: "400-500"` (the exact B2 defect) now `GATE: 1 VIOLATION(S)`
  where it previously passed. Closes B2 and arms it for every future stone/pome fruit.

### Fix B, render gap closed: certified-derived guide paths (plant-astro)
- **Added** `src/lib/built-crops.ts` (`builtCropZonePaths` / `zonesForCrop` / `isCertified`):
  the workhorse route's `(crop, zone)` paths now derive from the certified set
  (`verification_status.status === 'verified_gs_arc'`), emitting a page for every zone a certified
  crop resolves. Replaces the stale 14-slug `BUILT_CROPS` allowlist in
  `src/pages/guides/crops/[crop]/[zone].astro`. `availableZones` (the zone switcher) now uses the
  same shared `zonesForCrop`, so switcher and built pages can't drift.
- **Tests** (`src/lib/built-crops.test.ts`, 5 cases): RED -> GREEN. Covers the 3 dropped crops,
  shell exclusion, indoor (microgreens) -> 0 pages, multi-region zone merge incl. no-calendar
  tree cells.
- **Verified:** `vitest run` 259/259; `npm run build` 321 -> **348 pages**; `zucchini-courgette`,
  `broccoli`, `lavender` now build 9 zone pages each; `microgreens-mix` still 0 (correct);
  `broccoli/zone-9` (the formerly-404 default-zone link) renders. The website is now genuinely
  **18/18 display-ready.**

### Revised GO / NO-GO
Two blockers are closed (B2; the render gap). The verdict is **still NO-GO to scale to ~105 until
B1 lands** (annual calendar token-placement is still unguarded -- the largest surface, and most of
the 105 are annuals), plus the secondary hardening (B3 heat_pause backing, B4 photoperiod-window,
B5 per-entry companions + wiring register_fill/completeness into the always-on gate). Those move to
a full-context remediation chat; see `incognito-audit-remediation-kickoff-2026-06-25.md`. The Expo
app display-lag (§4b) and the ~14 MINOR date nits (§3, fold into the next authoring batch) remain.
