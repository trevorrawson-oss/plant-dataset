# Incognito Red-Team Remediation -- hardening the armor toward GO

**Date:** 2026-06-27 (memory-ON remediation session, Claude Code lane)
**Spec:** `docs/incognito-redteam-audit-2026-06-27.md` (16 reproduced holes, C1-C16).
**Dataset SHA:** `512e5a8d...` -- **byte-identical at start and end. READ-ONLY held; every fix is
gate tooling, zero canonical edits.** Discipline: TDD (RED before GREEN), all 18 certified anchors
reconciled to GREEN with zero false positives before each wire, every fix's audit injection
re-run through the live gate to confirm it now bounces.

The 16 holes split three ways. **9 are wired + green** (the clean mechanical batch). **4 are
surfaced** -- they cannot be closed mechanically without either flooding the 18 with false
positives or contradicting a locked decision, so they need Trevor's ruling. **3 are the
truth-layer**, a strategy decision brainstormed below, not a reflex gate.

---

## PART A -- LANDED: the mechanical batch (9 fixes, wired + green)

All 9 are TDD'd, 18/18 `whole_crop_gate` PASS, full tool suite 39/39, and each audit injection
re-run through the live gate confirms it now bounces.

| # | Sev | Gate | The fix | Test |
|---|-----|------|---------|------|
| **C1** | HIGH | **A30 (new)** `calendar_basis_gate` | Enum guard: `calendar_basis` must be one of the 7 known archetype bases. A typo/case-slip/synonym/novel value (`generic_placeholder`) was silently no-oping EVERY calendar gate. Runs FIRST (dispatch guard). Single source of truth for the bases. | `test_calendar_basis_gate.py` (8 cases + real-data 0-FP) |
| **C2** | HIGH | A3 `perennial_gate` | A `perennial_chill_gated` crop must keep `chill_hours` in its EFFECTIVE gating_factors (default keeps peach/apple green; an explicit list that drops the token now bounces). The missing mirror of `berries_woody_gate:59`. | `test_perennial_gate.py` 30-34 |
| **C3** | HIGH | **A31 (new)** `coverage_floor_gate` | Region roster floor: a non-indoor crop must carry the full canonical 10-region roster (no missing, no unknown key). `regions:{}` / a single region no longer certifies. Indoor collapses to `{}`. | `test_coverage_floor_gate.py` 0-7 |
| **C4** | HIGH | **A32 (new)** `coverage_floor_gate` | Calendar presence floor: a `frost_anchored` resolved cell must carry a non-empty calendar. Stripping `calendar[]` off every cell no longer certifies. Trees out of scope (A3 governs empty cells). | `test_coverage_floor_gate.py` 8-13 |
| **C5** | MED-HIGH | A9 `photoperiod_gate` | (a) Require `photoperiod` in gating_factors whenever NON-NULL day-length machinery is present (dropping the token no longer no-ops the gate). (b) A null `recommended_day_length_type` on a FILLED (calendar-bearing) cell is a coverage evasion, flagged (null on an unfilled cell stays the admission no-op). | `test_photoperiod_gate.py` 16-21 (+ test 1 corrected to the new contract) |
| **C8** | HIGH | A29 `register_fill_gate` | `.strip()` emptiness: a whitespace-only register value (`"   "`, `"\t\n"`) renders BLANK but counted as authored. Now flagged. | `test_register_fill_gate.py` 12-15 |
| **C9** | MED-HIGH | §3 (whole_crop_gate inline) | Guard `preferred[0]<=preferred[1]` AND `tolerated[0]<=tolerated[1]` before nesting. An inverted `[9,4]` nested in `[5.8,7.5]` (Hero stat "9.0 to 4.0") now fails. | `test_whole_crop_gate_hardening.py` C9 |
| **C10** | MED | A20 `display_readiness_gate` | Sanity bounds: `spacing_inches` and `days_to_maturity` must be a `[lo,hi]` pair of POSITIVE numbers (lo<=hi) when present. `spacing:0` / `days_to_maturity:[-5,-10]` no longer "present-and-fine". DTM bound is universal; `[]` stays the legit perennial N/A. | `test_display_readiness_gate.py` 10-17 |
| **C12** | MED | A23 `raw_display_gate` | Case/space-insensitive snake detection: a render-verbatim value containing an underscore-joined token (`Full_sun`, `Slow_release_granular`, `full sun_partial`, `FULL_SUN`) now flags. Superset of the old anchored-lowercase regex; the 18 carry zero underscores in render-verbatim fields. | `test_raw_display_gate.py` 15-21 |

**New gate files:** `calendar_basis_gate.py` (A30), `coverage_floor_gate.py` (A31/A32). The A-roster
is now A2-A32 (gaps A25=register_completeness ruled half stays as named; the new numbers are A30-A32).

**Note for the state trio (do at the landing commit, post-approval):** the gate roster grew by 3
(A30/A31/A32) and `register_fill`/`raw_display`/`display_readiness`/`perennial`/`photoperiod`
hardened. No canonical change, so this is a TOOLING release, not a content release.

---

## PART B -- SURFACED: 4 holes that are NOT clean mechanical fixes

Each of these was investigated test-first and found to either flood the 18 with false positives or
contradict a locked decision. Per the discipline (zero false positives before wiring; a real
tension goes to the log, not a forced gate), they are surfaced, not wired. Each needs a Trevor call.

### C11 (HIGH) -- A25 short-string / non-string / backend-key evasions -> needs a RULING pass

**Why it is not mechanical.** A25 (`register_completeness`) HALTs on a novel *prose* field. The three
evasions (a short string, a non-string value, a backend-named key) all let a novel field slip the
prose detector. The obvious fix -- "flag ANY unruled key" -- **floods**: the 18 already carry **132
distinct unruled non-string keys** (`days_to_maturity`, `chill_hours`, `growth_stages`, `pests`,
`notifications`, ...) and **~25 unruled short-string keys** (`audience`, `cause`, `harvest_urgency`,
`offset_from`, `recommended_rootstock`, `recipes[].title`, `verified_date`, ...), all legitimate.
The prose-shape filter is load-bearing; dropping it = ~157 false positives. There is no value-shape
heuristic that calls `mystery_advice:"Water it lots"` (13 chars) novel but `cause:"too much
nitrogen"` (17 chars) legit -- only a RULING of the key separates them.

**The real fix** is to COMPLETE the `EXCLUDED_KEYS` roster (rule each of the ~157 structural keys as
CATEGORICAL / MACHINERY / etc.), then flag any unruled string regardless of length. But the gate's
own contract is **STOP-AND-ASK, do NOT auto-rule** -- completing the roster is human judgment
(claude.ai authoring lane / Trevor), not a CC mechanical edit.

**Ask:** want me to produce the candidate ruling list (the ~157 keys grouped by proposed class) for
you to rule, then wire the tightened A25 once the roster is complete? That converts C11 from a
flood into a clean gate.

### C13 (MED) -- A24 pause-placement rides the core_months day-precision tolerance -> a TRADEOFF

`harvest:"Aug 15 - Oct"` makes Aug non-core (clipped at day 15), so a `cold_pause`/undeclared
`heat_pause` on Aug -- a month the page advertises as harvest -- passes A24. **But that exact
tolerance is a LOCKED decision** (CURRENT_STATE A24: "Partial-boundary frost-tail is tolerated
(month-rounding via core_months)"). It exists so a real harvest ending mid-month does not force the
whole month to be "core." Tightening it (treat any named month as core) would false-positive the
legit frost-tail cases it was built for. **This is a genuine boundary-tolerance tradeoff, not a bug.**
Options: (a) leave as-is (the tolerance is intentional, the abuse needs a crafted day-precision
window a careful author would not write); (b) tighten only when a pause token lands on a month the
SAME cell names in a harvest window (narrow: "advertised-harvest month can't also be paused"),
accepting it may catch a few legit partial-boundary cells -- needs a 0-FP check across the 18 first.
Recommend (b) gated on a 0-FP pass, else (a). Your call.

### C15 (MED) -- A27 companion evidence checks enum membership, never justification -> SEMANTIC

Upgrading a pairing `traditional/medium -> research_backed/high` while its `reason` prose still says
"well established" passes A27 (both new values are in-enum). Verifying the label is JUSTIFIED by the
reason and the actual source tier is **semantic** (truth-layer / LLM-judge), not mechanical. One
**partially-mechanical** sub-fix exists and is 0-FP-checkable: a `research_backed`/`extension_backed`
label should be required to carry actual `sources`/`anchoring_urls` (a "backed" claim must cite
something), and `verified_against_sources` should be consistent with the label per the locked
derivation. That closes the "claims backed but cites nothing" half; the "cited source doesn't
actually support the claim" half is truth-layer. Recommend folding the structural half into A27 (I
can TDD it) and routing the semantic half to the truth-layer thread.

### C16 (MED-HIGH) -- dual-voice downgraded to single-register by omission -> brushes a LOCKED decision

Deleting a `_beginner` sibling makes gate B count the field `SP seasoned-only` (no violation). But
**"Presence IS the visibility declaration" is the locked design** (whole_crop_gate docstring B +
CURRENT_STATE): a field with no `_beginner` sibling is legitimately seasoned-only. Forcing
"missing sibling = violation" would flag every legitimately-SP field across the 18 (massive false
positives) and contradict the locked decision. The real fix is a per-field CP/SP RULING inventory
(which fields MUST be dual-register) -- the same ruling-completeness class as C11, and claude.ai's
authoring lane. **Ask:** is a CP/SP ruling inventory in scope? Without it, C16 cannot be gated
without contradicting the locked decision.

---

## PART C -- TRUTH-LAYER BRAINSTORM (C6, C7, C14) -- strategy, not a gate

This is the kickoff's explicit brainstorm thread. **Do NOT build before we pick an approach.** The
audit's core point: `GATE: PASS` proves a crop is well-SHAPED + self-consistent + exemplar-matched,
NOT correct. 100% of source-content and biology fidelity rides on the per-batch human sample, which
does not scale to 105 crops x ~17 sources. C6 (fabricable source chain), C7 (a fabricated,
biologically-impossible, template-copied crop ships clean), and C14 (no gate models "this crop NEEDS
a heat pause here") are all this same gap. **C14 note: B3 is NOT relitigated** -- heat tolerance
stays per-cell, never a shared region-heat envelope; "needs a pause" is a biology question, which is
exactly the truth layer, not a region table.

### The single most likely bot failure mode (C7): copy-nearest-template, forget to refit

The "rutabaga that is basil verbatim" -- right shape, wrong biology -- is what a generator produces
at volume. The good news: **most of C7 is SELF-contradiction, catchable WITHOUT external truth.** The
fabricated crop had: prose pH 6.0-7.5 vs `ph:[3.0,3.4]`; harvest charted 3 months BEFORE planting;
`growing` through Minnesota January; carrot's `heat_pause` physiology pasted onto a different crop.
Each is the crop contradicting ITSELF or its own climate table.

### Options on the table (layered -- not exclusive)

1. **Internal cross-consistency gates (deterministic, highest ROI for C7).** Catch the crop
   contradicting itself: prose-pH vs `ph.preferred_range`; harvest-before-plant in a cell's calendar;
   a calendar that `grow`s through a zone's hard-frost months (vs the cell's own `first_frost`/
   `min_winter_temp_f`); rotation `family` vs the crop's botanical family; a `heat_pause`'s
   sources/prose naming a different crop. Fully automatable, deterministic, 0 external calls, catches
   the template-copy failure mode directly. **Recommend as the first build.**

2. **Numeric sanity bounds (deterministic, extends C10).** Bound EVERY numeric to a physical range
   (pH 3-10, DTM 5-400, spacing 1-360in, chill 0-1500h, temps -50..130F, sunlight_hours 0-24) +
   cross-field (prose number must match the structured field). Catches C7's `sunlight_hours:[0,1]`,
   `ph:[3.0,3.4]`, `days_to_maturity:[3,5]`. Cheap, deterministic. **Recommend pairing with (1).**

3. **Source-URL liveness sweep (automatable, necessary-not-sufficient for C6).** Fetch each cited
   URL; assert it resolves (not 404/parked/`fake.invalid`). Catches fabricated URLs. Does NOT verify
   the URL's CONTENT supports the claim (a live-but-irrelevant URL passes), and ~1785 fetches/batch
   is flaky + bot-blocked. Best as a periodic out-of-band sweep, not a per-cert blocker.

4. **Biology cross-check / LLM-judge layer (semantic, for what automation can't reach).** An LLM
   reviews each crop for biological coherence (family vs pests/companions, calendar vs climate,
   plausibility of every number against the crop). Catches semantic fabrication no structural gate
   can. Non-deterministic, costs, can hallucinate -- a QA AID with a rubric, not a hard gate. This is
   claude.ai's lane (a structured "biology self-review" pass per crop before promote).

5. **Make the per-batch source-truth sample LOAD-BEARING (process, not code).** The audit's literal
   point: the sample is currently optional/skippable. Make it mandatory + sized, gated in the release
   protocol (protocol #6 becomes a hard gate, not a backstop the green suite makes optional). Doesn't
   reach 100% coverage but directly answers "the sample is the only defense."

### Recommendation

Layer it: **(1) + (2) are deterministic, cheap, and catch C7's most likely mode -- build those first
in the CC lane (TDD, like the mechanical batch).** (4) the LLM biology-judge + (5) the load-bearing
sample are the backstop for what determinism can't reach (true source-content fidelity, novel biology
errors) -- (4) is claude.ai's lane, (5) is a protocol change. (3) URL liveness is a cheap periodic
filter for C6, run out-of-band. The strategic decision for Trevor: **where does the cert bar sit --
do (1)+(2) gate cert, does (4) become a required pre-promote pass, does (5) become mandatory?** Pick
the approach and I'll TDD the deterministic layers.
