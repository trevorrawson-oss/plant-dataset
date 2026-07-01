# Calendar-coherence fix -- design spec (2026-06-30)

**Status:** approved-in-conversation (Trevor, 2026-06-30); pending written-spec sign-off, then TDD.
**Companion:** `docs/calendar-coherence-bugs-2026-06-30.md` (the bug report + the don't-over-correct guardrails).
**Lane:** Claude Code (deterministic transform + gate + release ceremony).
**Canonical at design time:** `1bc569dc...` (unchanged; all analysis below was read-only, in-memory).

---

## 1. Problem

Two systemic calendar defects, found by Trevor eyeballing rendered `ca_interior` guides, that slipped
every certification because the gate suite checks calendar STRUCTURE, not calendar LOGIC:

- **Bug 1 -- "growing after harvest":** a `growing` token that cannot be reached from a `plant`/`indoors`
  without first passing a crop-removed state (`harvest`/`season_over`). You cannot be vegetatively
  growing when the last lifecycle event was a harvest and nothing has been replanted.
- **Bug 2 -- "one-month harvest hole":** a single non-harvest month punched out of an otherwise-continuous
  harvest **display window** (e.g. lettuce `'Sep - Oct, Dec - May'`, Nov missing).

Both touch certified gold-standard anchors AND the 13 crops live on the site, so the fix is a **content
release**.

## 2. Root-cause finding (why the plan changed)

The bug report proposed "fix `derive_annual_calendar`, then re-derive all 123 in one sweep." A read-only
parity check refuted the premise:

- **Only 39.6% (333/840) of stored frost_anchored calendars match `derive_annual_calendar(cell)`.** The
  other ~507 are legitimately hand-authored multi-cycle / winter-wrapping / heat-inverted shapes (exactly
  as the A24 docstring warns). A full re-derive would rewrite ~507 cells and clobber carrot's two-cycle,
  lettuce's heat-inversion, every winter-wrapping harvest -- not the ~147 intended.
- **The deriver is not even the source** for most of these: Bug 2 lives in the authored `harvest` string
  (the deriver consumes it); the deriver reproduces the Bug-1 `growing` for 59/98 bug-months (it carries
  the same gap). Re-deriving the bug months is therefore not a clean fix either.

**Decision (Trevor):** surgical deterministic **normalizer** that rewrites ONLY the bug cells in place +
a permanent **calendar-coherence gate**; do NOT harden the deriver in this pass; do NOT full-re-derive.
The systemic gap is the *missing calendar-logic gate*, not a broken deriver.

## 3. Locked decisions

| # | Decision | Source |
|---|----------|--------|
| D1 | Surgical normalizer + gate; no full re-derive; deriver untouched this pass. | Trevor, Q1 |
| D2 | Normalizer touches ONLY the two impossible patterns; preserve legit planting gaps + harvest-through-mild-winter (`docs/calendar-coherence-bugs` §"What NOT to over-correct"). | Trevor |
| D3 | Prove it touches EXACTLY the target cells via a before/after cell diff; zero collateral on the ~360 hand-authored cells. | Trevor, Q1 |
| D4 | Bug 1 = `frost_anchored` only. Perennials exempt (evergreen citrus growing-after-harvest is correct). | Trevor, Q2 |
| D5 | Bug 2 gate/normalizer applies to ALL calendar bases; bridge one-month holes; carve-out for a genuine staggered-ripening gap (none exist in the current 49). | Trevor |
| D6 | Bug-1 out-of-window replacement = context-matched off-season token (`cold_pause`/`season_over`/`indoors`). | Trevor, Q1 |
| D7 | The G+H "summer gap / summer shoulder" buckets -> `season_over` (matches existing certified `growing->season_over` in broccoli/kohlrabi `ca_desert` and brussels-sprouts `ca_interior`). | Trevor, Q3 |
| D8 | Separately TAG the ~8 warm-crop FL/desert-summer cells as candidates for a properly backed `heat_pause` in the AUTHORING lane (do not fake backing; A28 would reject a bare one). | Trevor, Q3 |

## 4. Scope (exact, from read-only scans on `1bc569dc`)

- **Bug 1: 93 impossible `growing` runs / 114 growing-months**, `frost_anchored` only. (The bug report's
  98/27 counted 6 `orange-navel` perennial cells that are correct; annual scope is 92 classic
  growing-after-harvest occurrences, 114 growing-months once multi-month runs and growing-after-pause-
  tracing-to-harvest are included by the stronger invariant in §5.)
- **Bug 2: 49 single-month harvest-display holes**, 18 crops (all annual continuous-croppers; none are
  staggered-ripening).
- **Overlap:** 2 of the 49 holes carry a `growing` token (not `plant`); those become `harvest` via the
  Bug-1 in-window rule once the window is bridged (see §7 sequencing).

## 5. The gate -- `tools/calendar_coherence_gate.py` (A37), TDD RED-first

One module, `calendar_coherence_violations(crop) -> list[str]`, wired into `whole_crop_gate.py` as **A37**
(next free number after A36), following the established `X_violations(crop)` pattern.

**Invariant 1 (Bug 1, `frost_anchored` only).** For every `growing` token, walking backward (wrap-aware)
through walk-through tokens, the first lifecycle token reached must be a legit predecessor:
- `WALK_THROUGH = {growing, cold_pause, heat_pause, wait}` (plant present or dormant -- e.g. garlic
  overwinters: `plant -> cold_pause -> growing` is LEGIT).
- `LEGIT = {plant, indoors}` (a growing run must trace back to one of these).
- `BLOCKER = {harvest, season_over}` (crop removed / cycle ended).
- A `growing` run is a VIOLATION iff the backward walk hits a `BLOCKER` before a `LEGIT`. If neither is
  found within 12 steps (pure walk-through, e.g. a year-round 12x`growing` calendar) it is NOT flagged.

**Invariant 2 (Bug 2, all crops).** No single non-harvest month may sit between two harvest months in the
parsed `harvest` display window (`H(m-1) and H(m+1) and not H(m)`). Multi-month gaps stay legal (two
discrete plantings). A crop whose genuine biology is staggered/discrete ripening is exempt (documented
carve-out; none in the current 49 -- log it if one appears rather than silently bridging).

**RED-first / adversarial (per CLAUDE.md TDD):**
- Inject `harvest -> growing` and a `harvest, X, harvest` hole into a SCRATCH crop; confirm each bounces.
- Confirm 0 false-positives on the legit patterns: garlic overwintering (`cold_pause -> growing`),
  winter-wrapping seasons (Oct `plant` -> Jan `growing` through the wrap), multi-month planting gaps,
  harvest-through-mild-winter, perennial evergreen growing-after-harvest, year-round 12x`growing`.
- The gate is **RED on canonical now** (114 + 49 = the worklist) -- expected; it goes GREEN after the
  normalizer (the project's gate-as-worklist pattern).

## 6. The normalizer -- `tools/normalize_calendar_coherence.py`

Deterministic, in-place, surgical. Loads canonical, edits ONLY the target fields in the in-memory dict,
re-dumps COMPACT (`separators=(",",":")`, `ensure_ascii=False`, no trailing newline) so the byte-diff
shows only the targeted values (dict key order is preserved). No full re-derivation.

### 6a. Bug 2 (run first)
For each cell (all bases), for each single-month hole `m`: **bridge** the two harvest spans that flank `m`
into one continuous span (earlier span start .. later span end), operating on the comma-separated spans of
the `harvest` string. **Preserve** day-level endpoints and any trailing parenthetical note. Do NOT
full-re-render the string (that would drop day precision / notes). The calendar TOKEN is left unchanged
(plant-row-quiet is a legit render state) EXCEPT where it is `growing` -- handled by Bug 1 below. Flag any
harvest string with formatting the bridger can't safely splice for manual review.

### 6b. Bug 1 (run second, so bridged windows are visible)
For each impossible `growing` run (per Invariant 1), for each month `m` in the run, first match wins:

1. `m in parse_months(harvest)` -> `harvest`   *(in-window / still producing / masked or bridged harvest)*
2. `m in parse_months(start_indoors)` -> `indoors`
3. `successor == cold_pause` -> `cold_pause`
4. `successor == season_over` -> `season_over`
5. `successor == indoors` -> `cold_pause`   *(winter gap before an indoor seed-start)*
6. `successor == plant` and `m in {Nov,Dec,Jan,Feb}` -> `cold_pause`   *(deep-winter gap before a spring plant)*
7. else -> `season_over`   *(summer gap before a fall plant / summer shoulder before a heat_pause)*

where `successor` = the first non-`growing` token after the run (wrap-aware). This ordered rule reproduces
the approved buckets A(1) / B(2) / C(3) / D(4) / E(5) / F(6) / G,H(7) exactly.

The rule-6-vs-7 boundary (`cold_pause` vs `season_over`) is deterministic but is a genuine judgment call
for mild coastal winter shoulders (e.g. `parsnip ca_north_coast` Feb). It is intentionally left to the
deterministic rule for a first, consistent pass; every such old->new lands in the §8.1 diff, which is the
human review surface at sign-off -- borderline calls get ruled there, not silently.

### 6c. Warm-crop heat_pause tags (D8)
While applying rule 7, emit a corrections-log entry (NOT a data edit) for each warm-crop FL/desert-summer
cell -- `eggplant`/`watermelon`/`pumpkin`/`butternut-squash` in `fl_peninsula`/`ca_desert` summer -- as a
candidate for a researched, backed `heat_pause` (months + `basis_seasoned` + T1 sources) in the authoring
lane. season_over is the honest interim; the backed heat_pause is a later authoring task.

## 7. What is deliberately NOT touched (guardrails, D2)

- **Legit planting gaps** (a crop need not plant every month; deep-winter sow gaps are correct).
- **Harvest-through-mild-winter** (a cold-hardy cool-season crop cropping Nov-Jan is active, not cold-
  stopped; the empty Plant row is a render/UX matter, not a dataset fix -- no `cold_pause` added there).
- **Broad plant windows that mask harvest tokens** (e.g. lettuce `ca_interior` z9 plants Aug-Mar, so the
  token row shows `plant` on pick-months). Per the litmus this is a valid biological choice / render-
  precedence matter, NOT an impossible sequence. Logged as a follow-up (§9), not fixed here.
- **Overwintering crops** (garlic: `plant -> cold_pause -> growing` is dormancy, not "nothing planted").
- **Perennials** (D4). **Year-round 12x`growing`** calendars.

## 8. Verification + release

1. **Exact-cell diff (D3) -- the SIGN-OFF surface.** A report listing every changed field
   (`regions.<r>.resolved_by_zone.<z>.calendar[m]` old->new, and `.harvest` old->new), per crop; assert
   the changed-cell set == the scan's target set and that a byte-diff shows NO other changes. Routed back
   to Trevor (and the prior session) to confirm before any canonical commit. Explicitly FLAG in the diff
   (prior-session review, 2026-06-30 -- not blockers, sign-off items):
   - **(i) The ~16 "stronger-invariant" cells** (the 98->114 delta): confirm each genuinely traces back to
     `harvest`/`season_over`, i.e. not over-caught by the walk-through relaxation.
   - **(ii) Mild-coastal rule-6 shoulders:** rule 6 stamps `cold_pause` on any Nov-Feb gap before a spring
     plant, but on `ca_north_coast`/`ca_south_coast` (mild z9/z10) February isn't truly "cold" --
     `season_over` may be more honest. Flag those mild-coastal winter shoulders so any that read as
     "waiting" rather than "cold-stopped" can be re-ruled.
   - **(iii) Bug-2 bridges:** spot-check that no bridge spans a genuine two-crop gap (esp. lettuce
     `ca_interior` -- a bridged Nov must be real continuous cropping, not invented harvest); and confirm
     the warm-crop `heat_pause` tags (D8) actually LAND in the corrections log, not silently drop.
2. **Re-run both scans -> expect 0.** Re-run the A37 gate over all crops -> GREEN.
3. **`whole_crop_gate` 18/18** (by exit code, not grep) **+ `tools/release_verify.py`** + the per-batch
   source-truth sample where applicable.
4. **State trio:** regenerate `CURRENT_STATE.md` via `tools/gen_current_state.py` (fill prose slots),
   append `STATE_HISTORY.md` (most-recent-first), bump `LATEST.txt` (SHA + session).
5. **Trevor sign-off** before any commit; then the plant-astro submodule bump re-deploys the live 13
   (a website-side step, gated on Trevor).

## 9. Out of scope / follow-ups

- **Backed `heat_pause` authoring** for the ~8 tagged warm-crop cells (D8) -- authoring lane, needs T1
  research + an FL-summer why-note.
- **Broad-plant-window / harvest masking** (lettuce et al.) -- a render-precedence question (show pick vs
  plant when both apply); logged, not fixed here.
- **"Use `growing` less loosely"** (Trevor's aspiration: more `season_over`/`late` where accurate) -- this
  fix moves in that direction for the impossible cells only; a broader token-precision pass is future work.
- **Deriver hardening** so future authoring can't reintroduce Bug 1 -- deferred (D1); the A37 gate is the
  guardrail that catches reintroduction regardless of source.

## 10. Implementation phases (for writing-plans)

1. TDD A37 gate (`calendar_coherence_gate.py` + `test_calendar_coherence_gate.py`): RED on injected
   defects + 0-FP on the legit-pattern fixtures; wire into `whole_crop_gate.py`.
2. Build + unit-test the normalizer on scratch copies (Bug 2 bridger; Bug 1 bucket rule); adversarial
   before trusting.
3. Apply to canonical (explicit re-derive task); produce the exact-cell diff (§8.1); re-run scans -> 0.
4. Release verification (§8.2-8.3) + state trio (§8.4).
5. Trevor sign-off -> commit -> submodule bump (§8.5).

## 11. Implementation refinements (post-approval, 2026-06-30) -- supersede the §4 estimates

Building + previewing surfaced three edge classes; each was ruled (Trevor / prior session) and
encoded as a deterministic rule shared by the gate and the normalizer (so gate(after)==0):

- **D9 Bug-2 discriminator (bridge only genuine punch-outs).** The 49 gate-flaggable holes split by
  biology: ~22 summer holes (Jun-Sep) are real heat gaps between a spring and a fall crop, and 2
  hawaii `'Feb 15 - Dec 15'` Jan holes are the wrap-gap of a single near-year-round span. A hole is
  bridged iff (1) m-1 and m+1 sit in DIFFERENT spans, (2) m in Oct-May, (3) no flanking heat_pause.
  -> **25 bridges** land; **24 holes left** (22 summer + 2 hawaii single-span), surfaced not bridged.
- **D10 Bug-1 near-year-round exemption.** A cell with a >=10-month harvest window is a continuous
  producer (hawaii zucchini/cucumber, 11 mo); its interspersed `growing` is the tropical lull, not
  the bug (annual analog of the perennial-evergreen exemption). Isolates exactly those 2 cells.
- **D11 Bug-1 forward-clause.** An OUT-OF-window `growing` that leads FORWARD into a harvest (through
  growing/heat_pause) is growing TOWARD that harvest (a fall crop whose `plant` is masked by
  heat_pause, e.g. beefsteak se_gulf z8 Sep), not growing-after-a-finished-crop -> exempt. Prevents
  the normalizer from stamping a `season_over` immediately before a harvest (a new incoherence).

**FINAL SCOPE (on canonical `1bc569dc`):** 105 Bug-1 token replacements + 25 Bug-2 harvest bridges
= **130 changes across 106 cells**. Bug-1 tokens: 34 cold_pause, 60 season_over, 4 indoors, 7
harvest. 13 warm-crop season_over cells tagged for a backed heat_pause (authoring lane, D8).

**Verification (scratch):** A37 gate -> 0; the §8.1 diff proves changed-set == gate-target-set with
0 collateral; 0 new season_over->harvest incoherences; `whole_crop_gate` exit codes unchanged
canonical-vs-normalized across all 32 touched crops. Canonical byte-unchanged until sign-off.

**Tooling added (all TDD, RED-first):** `tools/calendar_coherence_gate.py` (+test) wired as A37;
`tools/normalize_calendar_coherence.py` (+test); `tools/calendar_coherence_diff.py` (the §8.1
sign-off surface + collateral guard).
