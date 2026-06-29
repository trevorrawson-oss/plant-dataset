#!/usr/bin/env python3
"""Whole-crop gate -- the Step 11 certification suite, crop-agnostic core.

Ported from the M15 lettuce Step 11 runs (2026-06-05, sessions
m15_lettuce_step11_apply_and_gate + m15_lettuce_step11_writeback_flip), where
this exact logic produced the 0-violations run the first flip rode on.

Components (all denominators derived STRUCTURALLY by walking the crop --
never from a hand roster; that discipline is the bolting-miss preventer):
  B. dual-voice coverage (v2 logic): every `*_seasoned` prose key must have a
     non-null `*_beginner` sibling (CP) or no sibling key at all (SP).
     Presence IS the visibility declaration.
  C. dash gate: user-facing `--` must be 0 (per-sense resolution is authored
     per crop BEFORE this gate can pass; backend notes retain whatever form).
  D. temperature notation: canonical `°F` only in user-facing strings.
  E. source-tier: every cited source ID catalogued + admitted + T1.
  F. anchoring completeness, 1A layer-scoped (Trevor 2026-06-04, amended
     2026-06-05): every claim-bearing leaf with non-empty `sources` carries
     `anchoring_urls` one-per-source-ID. EXCLUDED BY DEFINITION: the legacy
     `zones{}` layer; the `regions{}` root rollup `sources` arrays;
     `bolting.*` (inherit-class per A-2, evidence at tips_by_stage.bolting).
     INCLUDED: sibling-named pairs `*_sources`/`*_anchoring_urls`
     (harvest_ready_*, description_*, days_to_maturity_*, ...) -- the
     s11_finding_001 predicate fix.
  G. flip-state report + two-field predicate (blocks_launch AND status !=
     "resolved").

NOT covered here (run separately):
  - §3 cross-field consistency: CROP-SPECIFIC. Author the checks per crop
    (lettuce's 8 are in STATE_HISTORY 2026-06-04 Step 10). Generic subset
    included below (ph nesting, container, flag implication) -- extend it.
  - The copyright/verbatim scan: tools/verbatim_scan.py (flip-blocking).
  - Roster-completeness (unknown-field catcher): tools/register_completeness_gate.py.

Usage:
  python3 tools/whole_crop_gate.py <crop-slug> [crops_data_final.json]
Exit 1 on any violation. A clean run here + clean §3 + clean verbatim scan +
clean roster gate = flip-eligible (gate #1).
"""
import json
import re
import sys

if len(sys.argv) < 2:
    print(__doc__)
    sys.exit(2)
SLUG = sys.argv[1]
PATH = sys.argv[2] if len(sys.argv) > 2 else "crops_data_final.json"

data = json.load(open(PATH))
matches = [c for c in data["crops"] if c.get("slug") == SLUG]
assert len(matches) == 1, f"slug {SLUG!r}: {len(matches)} matches"
crop = matches[0]
violations = []


def fail(msg):
    violations.append(msg)
    print(f"  VIOLATION: {msg}")


# ---- layer classification: the ONE shared predicate (field_classification.py) ----
import os as _os
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from field_classification import is_backend


# ---------------- A30. calendar_basis enum guard (the DISPATCH guard; run first) ----------------
# calendar_basis is THE key every calendar gate dispatches on (A3/A4/A5/A6/A9/A10/A11/A13/A14/
# A15/A16/A24/A28). An unvalidated typo/case-slip/synonym/novel value silently no-ops the whole
# calendar layer while the suite still prints PASS (incognito-redteam C1). Validate it FIRST so a
# bad basis is a hard violation, not a silent dispatch miss.
from calendar_basis_gate import calendar_basis_violations
print("A30. calendar_basis enum guard (the dispatch key is a known archetype base)")
_cbv = calendar_basis_violations(crop)
print(f"  calendar_basis={crop.get('calendar_basis')!r} | violations: {len(_cbv)}")
for m in _cbv:
    fail(f"calendar_basis: {m}")

# ---------------- A31/A32. coverage floors (region roster + calendar presence) ----------------
# A2 validates whatever regions/cells EXIST but never asserts enough exist, so regions:{} or a
# calendar-stripped annual certify (incognito-redteam C3/C4). A31: a non-indoor crop carries the
# full 10-region roster (indoor collapses to {}). A32: a frost_anchored cell carries a non-empty
# calendar (tree empty cells are A3's job).
from coverage_floor_gate import region_roster_violations, calendar_presence_violations
print("A31. region roster floor (non-indoor crop carries the full 10-region roster)")
_rrv = region_roster_violations(crop)
print(f"  region roster violations: {len(_rrv)}")
for m in _rrv:
    fail(f"region-roster: {m}")
print("A32. calendar presence floor (frost_anchored cells carry a non-empty calendar; no-op off annual)")
_cpv = calendar_presence_violations(crop)
print(f"  calendar presence violations: {len(_cpv)}")
for m in _cpv:
    fail(f"calendar-presence: {m}")

# ---------------- A33. numeric sanity (truth-layer, deterministic) ----------------
# The cert suite validates SHAPE, never that a NUMBER is physically plausible -- the fabricated-crop
# attack (C7) shipped days_to_maturity:[3,5], sunlight_hours:[0,1], tree-spacing on an annual. This
# bounds every key numeric to a physical range (spacing archetype-aware). First deterministic layer
# of the truth-layer defense; the prose<->number cross-consistency layer is increment 2.
from numeric_sanity_gate import numeric_sanity_violations
print("A33. numeric sanity (key numerics within physical bounds; spacing archetype-aware)")
_nsv = numeric_sanity_violations(crop)
print(f"  numeric sanity violations: {len(_nsv)}")
for m in _nsv:
    fail(f"numeric-sanity: {m}")

# ---------------- A34. cross-consistency (truth-layer, deterministic cross-field) ----------------
# C7's copy-template-don't-refit failure makes the crop contradict ITSELF (no external truth needed):
# the fabricated crop's prose said pH 6.0-7.5 while ph.preferred_range was [3.0,3.4]. Rule 1 here
# cross-checks the pH prose vs the structured range; increment 2 adds calendar/biology cross-checks.
from cross_consistency_gate import cross_consistency_violations
print("A34. cross-consistency (fields that must agree: pH prose vs structured range)")
_ccv = cross_consistency_violations(crop)
print(f"  cross-consistency violations: {len(_ccv)}")
for m in _ccv:
    fail(f"cross-consistency: {m}")


# ---------------- generic §3 subset (EXTEND PER CROP) ----------------
print("A. §3 cross-field consistency -- GENERIC SUBSET ONLY (author the full per-crop set)")
ph = crop.get("ph") or {}
if ph.get("preferred_range") and ph.get("tolerated_range"):
    pr, tr = ph["preferred_range"], ph["tolerated_range"]
    # Each range must be well-ordered (lo <= hi) BEFORE nesting is meaningful: an
    # inverted preferred [9,4] passed nesting (5.8<=9 and 4<=7.5) and rendered the Hero
    # pH stat "9.0 to 4.0" (incognito-redteam C9). Guard endpoint order on both ranges.
    well_ordered = pr[0] <= pr[1] and tr[0] <= tr[1]
    nested = tr[0] <= pr[0] and pr[1] <= tr[1]
    ok = well_ordered and nested
    print(f"  ph preferred {pr} within tolerated {tr}: {'PASS' if ok else 'FAIL'}")
    if not ok: fail("§3 ph range nesting")
cn = crop.get("container_notes") or {}
if cn.get("container_ok"):
    # A potted crop is dimensioned by VOLUME (min_pot_gallons); an indoor TRAY crop
    # (microgreens/sprouts, anchor 11) by DEPTH (depth_inches_min) -- a 1020-style tray is
    # not measured in gallons. container_ok requires ONE of the two dimensions.
    ok = bool(cn.get("min_pot_gallons")) or bool(cn.get("depth_inches_min"))
    print(f"  container_ok=True => pot-gallons|tray-depth "
          f"(min_pot_gallons={cn.get('min_pot_gallons')} depth_inches_min={cn.get('depth_inches_min')}): "
          f"{'PASS' if ok else 'FAIL'}")
    if not ok: fail("§3 container fields")
vs = crop["verification_status"]
ok = (not vs.get("launch_ready_seasoned")) or vs.get("launch_ready_core")
print(f"  launch_ready_seasoned => launch_ready_core: {'PASS' if ok else 'FAIL'}")
if not ok: fail("§3 flag implication")

# ---------------- A2. region-fill completeness (the 2.7.5-scaffold catcher) ----------------
# Every crop got an empty regions{} shell at schema 2.7.5. A region whose
# plantings is still a "PENDING ..." stub string, or whose region_notes pair is
# both null, is an UNFILLED shell -- invisible to the dual-voice/dash/anchoring
# walks below (a stub string trips none of them). This is the region-primary
# FILL work-list at Step 0 and a hard violation at Step 11. Without this check
# the gate silently under-reports an unfilled crop (the cherry/beefsteak miss).
print("A2. region-fill completeness (stub + null notes + STALE pre-hoist shape catcher)")
regions = crop.get("regions") or {}
stub_regions, empty_notes, stale_shape, null_track = [], [], [], []
for rk, r in regions.items():
    pl = r.get("plantings")
    if isinstance(pl, list) and pl and isinstance(pl[0], str) and "PENDING" in pl[0]:
        stub_regions.append(rk)
    elif not (isinstance(pl, list) and pl and isinstance(pl[0], dict)):
        stub_regions.append(rk)  # no real plantings rule layer at all
    else:
        # filled-shaped, but is it at-bar? track:None = unauthored (lettuce uses
        # beginner/succession). A resolved_by_zone cell carrying a nested
        # `plantings` key is the pre-Pass-1b off-spec shape (spec §3b-i forbids
        # rule-bearing structure in resolved_by_zone) -- i.e. an OLD shallow lift
        # that looks filled but is not region-primary. This is the cherry/beefsteak
        # northern_tier trap: dict plantings, but static_precompute + nested cells.
        if any(p.get("track") is None for p in pl):
            null_track.append(rk)
        rbz = r.get("resolved_by_zone") or {}
        if any(isinstance(cell, dict) and "plantings" in cell for cell in rbz.values()):
            stale_shape.append(rk)
    if not r.get("region_notes_seasoned") and not r.get("region_notes_beginner"):
        empty_notes.append(rk)
print(f"  regions: {len(regions)} | stub/missing plantings: {len(stub_regions)} | null-track plantings: {len(null_track)} | stale nested-cell shape (§3b-i): {len(stale_shape)} | both region_notes null: {len(empty_notes)}")
for rk in stub_regions: fail(f"region unfilled (plantings stub/missing): {rk}")
for rk in null_track: fail(f"region plantings track is None (unauthored shape): {rk}")
for rk in stale_shape: fail(f"region resolved_by_zone carries nested plantings (pre-hoist §3b-i shape): {rk}")
for rk in empty_notes:
    if rk not in stub_regions:
        fail(f"region_notes pair both null: {rk}")

# second_planting structure validation (M16): when a resolved cell carries a
# second_planting, it must be a discrete-window dict with the window field set.
# Lenient on null VALUES at admission (claude.ai sources them at Step 4/5); the
# KEYS must exist. Forward-looking -- cherry carries none at Step 3.5.
SECOND_PLANTING_KEYS = {"plant_out", "start_indoors", "harvest_start", "harvest_end"}
for rk, r in regions.items():
    for z, cell in (r.get("resolved_by_zone") or {}).items():
        if isinstance(cell, dict) and "second_planting" in cell:
            sp = cell["second_planting"]
            if not isinstance(sp, dict):
                fail(f"second_planting not a dict: {rk}.{z}")
            elif not SECOND_PLANTING_KEYS.issubset(sp):
                missing = sorted(SECOND_PLANTING_KEYS - set(sp))
                fail(f"second_planting missing window keys {missing}: {rk}.{z}")

# ---------------- A3. perennial (tree) cert-gate branch ----------------
# The tree-shape invariants the generic A2 checks do not encode: exactly one
# track:"perennial" establishment entry per region, the suitability enum, and the
# NO-FRUIT DIRECTION SPLIT (a survives_no_fruit cell carries a calendar IFF chill is
# reliably met). No-op for non-perennial crops. (v1.8 amendment §4-5.)
from perennial_gate import perennial_cert_violations
print("A3. perennial cert-gate branch (tree invariants; no-op for non-perennial)")
# The no-fruit split reads the shared region_chill_delivered table (F2 refactor), not a
# per-cell crop field. A missing top-level table surfaces as a per-cell "missing band" here.
_perennial = perennial_cert_violations(crop, data.get("region_chill_delivered"))
print(f"  calendar_basis={crop.get('calendar_basis')!r} | perennial violations: {len(_perennial)}")
for m in _perennial:
    fail(f"perennial: {m}")

# ---------------- A4. tree calendar coherence (DERIVED-from-dates) ----------------
# The tree calendar[] is a pure function of each cell's bloom + harvest display windows.
# Hand-authoring it let it drift (apple Step 5: 5 bloom + 11 harvest mismatches; peach
# carried 10). This gate recomputes the calendar from the dates and fails on any mismatch,
# so an incoherent tree calendar cannot ship. No-op for non-perennial. (apple Step 5, 2026-06-11.)
from tree_calendar import tree_calendar_violations
print("A4. tree calendar coherence (calendar == derive(bloom,harvest); no-op for non-perennial)")
_treecal = tree_calendar_violations(crop)
print(f"  calendar cells incoherent with their own dates: {len(_treecal)}")
for m in _treecal:
    fail(f"tree-calendar: {m}")

# ---------------- A5. annual calendar coherence (always-on; NOT a re-derivation) ----------------
# Frost_anchored annual calendars are consistency-checked, not re-derived -- complex multi-cycle
# cells (winter-wrap / heat-inverted) are legitimately hand-authored and a clean deriver would
# degrade them. HARD on a non-12 length, a token outside the annual enum (catches the
# start_indoors -> indoors render drift; SuccessionCard reads `indoors`), or a heat_pause.months
# object disagreeing with the calendar's heat_pause tokens. `wait` tokens are a pause-legibility
# note. No-op for non-frost_anchored. (2026-06-14, the annual analog of A4.)
from annual_calendar import annual_coherence_violations
print("A5. annual calendar coherence (token enum + heat_pause alignment; no-op for non-annual)")
_acoh, _anote = annual_coherence_violations(crop)
print(f"  annual calendar hard incoherences: {len(_acoh)} | wait-token notes: {len(_anote)}")
for m in _acoh:
    fail(f"annual-calendar: {m}")
for m in _anote:
    print(f"  note: {m}")

# ---------------- A6. non_seasonal_indoor cycle presence (no-op for non-indoor) ----------------
# An indoor crop (microgreens/sprouts/mushrooms) has NO frost/region/zone axis -- its source of
# truth is the indoor_cycle block (the relative sow->harvest cycle). This is the Step 5.5
# non_seasonal_indoor branch, and the indoor counterpart to A2 region-fill: the cycle must be
# present (days_to_harvest non-empty) and dual-register (tip_seasoned + tip_beginner both
# authored). No-op for any other calendar_basis. (microgreens-mix anchor 11, 2026-06-15.)
print("A6. non_seasonal_indoor cycle presence (no-op for non-indoor)")
if crop.get("calendar_basis") == "non_seasonal_indoor":
    ic = crop.get("indoor_cycle") or {}
    both_tips = bool(ic.get("tip_seasoned")) and bool(ic.get("tip_beginner"))
    print(f"  indoor_cycle: days_to_harvest={ic.get('days_to_harvest')!r} | dual-register tip: {'both' if both_tips else 'MISSING'}")
    if not ic.get("days_to_harvest"):
        fail("indoor_cycle incomplete: days_to_harvest empty (the cycle length is the indoor source of truth)")
    if not both_tips:
        fail("indoor_cycle incomplete: tip_seasoned/tip_beginner not both authored")
else:
    print("  (not non_seasonal_indoor -- skipped)")

# ---------------- A7. CP-field placement (suffixed siblings, NOT a nested wrapper) ----------------
# A CP field renders as parent.X_seasoned / parent.X_beginner DIRECT siblings (container_notes.notes_seasoned,
# storage.fridge_seasoned), never parent.X.{X_seasoned}. The dual-voice (B) + roster walks recurse for the
# suffix, so they PASS a mis-nested CP field -- placement was otherwise unenforced. Signature: a key K whose
# dict value carries a child key named exactly K_seasoned or K_beginner (the suffix redundantly repeats K).
# Legit grouping objects (soil_mix.type_seasoned, drainage.saucer_practice_seasoned) differ -- the inner stem
# != the parent key, so they are NOT flagged. (microgreens-mix 6-8, 2026-06-15: claude.ai shipped
# shape_requirements/saucer_practice double-nested; the gates passed it; flattened at release.)
print("A7. CP-field placement (suffixed siblings, not a nested wrapper)")
_misnest = []
def cp_placement_walk(o, pat):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, dict):
                for ck in v:
                    if ck == f"{k}_seasoned" or ck == f"{k}_beginner":
                        _misnest.append(f"{pat}.{k}.{ck}")
            cp_placement_walk(v, f"{pat}.{k}")
    elif isinstance(o, list):
        for i, it in enumerate(o):
            cp_placement_walk(it, f"{pat}[{i}]")
cp_placement_walk(crop, crop.get("slug", "?"))
print(f"  CP-placement walk: {len(_misnest)} mis-nest(s)")
for m in _misnest:
    fail(f"mis-nested CP field: {m} (the suffixed pair must be siblings of the parent key, not nested under it)")

# ---------------- A8. realized-succession coherence (no-op off succession scope) ----------------
# successions_realized is a PURE DERIVED per-zone count (deriver = the source of truth, like
# the A4 tree calendar). This re-derives and asserts equality, so an edit to a zone's window
# that was not followed by a deriver re-run is caught as STALE. Also enforces presence on every
# in-scope cell + the LOCK #4 crop-level reconciliation (successions == max_successions_per_season
# == max over zones). For an OUT-OF-SCOPE crop (suitable=False / indoor -- cherry/beefsteak/
# microgreens) the field must be ABSENT (a succession is not a second planting). This is the
# "wired into the arc" guarantee: a future succession anchor cannot certify without it.
# (per-zone realized-succession-count pass, 2026-06-15.)
from derive_realized_successions import derive_cell_realized, crop_in_scope as _succ_in_scope
print("A8. realized-succession coherence (successions_realized == derive; no-op off scope)")
if _succ_in_scope(crop):
    _iw = (crop.get("succession_policy") or {}).get("interval_weeks")
    _realized = []
    for rk, r in (crop.get("regions") or {}).items():
        for z, cell in (r.get("resolved_by_zone") or {}).items():
            if not isinstance(cell, dict):
                continue
            want = derive_cell_realized(cell, _iw)
            have = cell.get("successions_realized")
            if want is None:
                if have is not None:
                    fail(f"successions_realized present on non-derivable cell: {rk}.{z}")
                continue
            _realized.append(want)
            if have is None:
                fail(f"successions_realized missing: {rk}.{z}")
            elif have != want:
                fail(f"successions_realized stale: {rk}.{z} (have {have}, derive {want})")
    _mx = max(_realized) if _realized else None
    if _realized:
        _sp = crop["succession_policy"]
        if _sp.get("successions") != _mx:
            fail(f"succession_policy.successions {_sp.get('successions')} != max(realized) {_mx}")
        if _sp.get("max_successions_per_season") != _mx:
            fail(f"succession_policy.max_successions_per_season {_sp.get('max_successions_per_season')} != max(realized) {_mx}")
    print(f"  in-scope: {len(_realized)} cells | crop-max={_mx} "
          f"| successions={(crop.get('succession_policy') or {}).get('successions')}")
else:
    _stray = [f"{rk}.{z}" for rk, r in (crop.get("regions") or {}).items()
              for z, cell in (r.get("resolved_by_zone") or {}).items()
              if isinstance(cell, dict) and "successions_realized" in cell]
    print(f"  (not succession-scope -- {len(_stray)} stray field(s))")
    for s in _stray:
        fail(f"successions_realized on out-of-scope crop (a succession is not a second planting): {s}")

# ---------------- A9. photoperiod (day-length) coverage (no-op off photoperiod scope) ----------------
# A photoperiod-gated crop (onion, anchor 12; the allium family) resolves day-length TYPE by
# latitude: long_day North / intermediate_day middle / short_day South. The varieties carry the
# type (biological truth); each filled region cell resolves which type to grow. The COVERAGE
# invariant is load-bearing: every type a region resolves to must have >=1 recommended variety
# carrying it (no "grow short-day here" with zero short-day varieties on the page). A null cell
# recommended_day_length_type is the Step-3.5 admission state (skipped -- A2 owns region-fill).
# B4 adds WINDOW FIT: a cell's day_length_type must agree with its plant_out season shape
# (long-day spring-planted, short-day fall/winter-planted -- opposite seasons), keyed on
# plant_out only. No-op unless "photoperiod" in gating_factors. (onion anchor 12, 2026-06-16.)
from photoperiod_gate import photoperiod_violations
print("A9. photoperiod day-length coverage (variety + cell typing + coverage + window-fit; no-op off scope)")
_photo = photoperiod_violations(crop)
print(f"  gating_factors={(crop.get('gating_factors') or [])!r} | photoperiod violations: {len(_photo)}")
for m in _photo:
    fail(f"photoperiod: {m}")

# ---------------- A10. berries_herbaceous structural cert (no-op off perennial_herbaceous) ----------------
# Strawberry (anchor 13, the only berries_herbaceous crop) is a herbaceous perennial whose
# LIFECYCLE is region-dependent: a per-cell grown_as in {perennial, annual} (north matted-row
# vs hot-summer CA/FL annual). This asserts the structural invariants the generic checks do not
# encode -- lifecycle scalars present, self_fertile, the photoperiod guard (strawberry type is a
# variety attribute, NOT an onion zone gate), no tree cross-pollination keys, no tree-only cell
# keys, and grown_as<->token placement. No-op unless basis perennial_herbaceous. (strawberry, 2026-06-18.)
from berry_herbaceous_gate import berry_herbaceous_violations
print("A10. berries_herbaceous structural cert (lifecycle + grown_as + guards; no-op off scope)")
_berry = berry_herbaceous_violations(crop)
print(f"  calendar_basis={crop.get('calendar_basis')!r} | berries_herbaceous violations: {len(_berry)}")
for m in _berry:
    fail(f"berries_herbaceous: {m}")

# ---------------- A11. berries_herbaceous calendar coherence (DERIVED-from-dates) ----------------
# The strawberry calendar[] is a pure function of the cell's grown_as + display windows (the
# tree_calendar lesson): perennial -> dormant/growing/bloom/harvest/renovation bracketed by frost;
# annual -> plant/growing/bloom/harvest/season_over. Recompute-from-dates and fail on any mismatch.
# Empty calendars are the Step-3.5 admission state (skipped). No-op off perennial_herbaceous.
from berry_calendar import berry_calendar_violations
print("A11. berries_herbaceous calendar coherence (calendar == derive(grown_as, dates); no-op off scope)")
_berrycal = berry_calendar_violations(crop)
print(f"  berries_herbaceous calendar violations: {len(_berrycal)}")
for m in _berrycal:
    fail(f"berries_herbaceous calendar: {m}")

# ---------------- A12. consumer-compound population (the truthy-but-empty trap) ----------------
# A consumer compound can ship PRESENT yet EMPTY and pass every other gate: an empty list, or the
# dict-of-empty-lists that shipped lemon/orange/strawberry with ZERO tips ({"established":[],...}
# is truthy AND its key-count reads non-empty). register_fill (pairs) + register_completeness
# (unruled keys) are both blind to it. This recurses the value and fails any required consumer
# compound with zero real content. Indoor crops are exempt from weather_triggers (no frost/heat).
# (Found 2026-06-19 -- tips_by_stage shipped empty on 3 certified crops, undetected.)
from compound_population_gate import empty_compound_violations, tips_violations
print("A12. consumer-compound population + tips rendering-conformance (recurses dict-of-lists)")
_empty = empty_compound_violations(crop)
print(f"  empty consumer compounds: {len(_empty)}")
for m in _empty:
    fail(f"empty consumer compound -- {m}")
# tips_by_stage carries 3 rendering traps the generic check misses: empty, wrong field
# (tip_ vs text_), orphaned key (not a growth_stage id -> renderer never grabs it). Indoor
# crops exempt (tip surface is indoor_cycle.tip, gated by A6). (Found 2026-06-21, 7 crops.)
_tips = tips_violations(crop)
print(f"  tips rendering-conformance issues: {len(_tips)}")
for m in _tips:
    fail(f"tips conformance -- {m}")

# ---------------- A13. woody_ornamental structural cert (no-op off perennial_woody_ornamental) ----------------
# Lavender (anchor 14, the FIRST and only perennial_woody_ornamental crop) is a woody perennial
# subshrub grown for BLOOMS whose LIFECYCLE is region-dependent: a per-cell grown_as in
# {perennial, annual} (cold-hardy in-ground shrub vs container/replant annual). This asserts the
# structural invariants the generic checks do not encode -- boundary scalars present, gating_factors
# EMPTY (cold-hardiness handled lighter than citrus, no A9 coverage gate -- D7), no tree machinery
# (rootstock/chill-gate/pollinizer) carrying a value, no tree-only cell keys, and the grown_as<->token
# placement (prune/dormant perennial-only, season_over annual-only, no fruit/mow token). No-op off
# basis. (lavender, 2026-06-19.)
from woody_ornamental_gate import woody_ornamental_violations
print("A13. woody_ornamental structural cert (lifecycle + grown_as + prune-placement + guards; no-op off scope)")
_woody = woody_ornamental_violations(crop)
print(f"  calendar_basis={crop.get('calendar_basis')!r} | woody_ornamental violations: {len(_woody)}")
for m in _woody:
    fail(f"woody_ornamental: {m}")

# ---------------- A14. woody_ornamental calendar coherence (DERIVED-from-dates) ----------------
# The lavender calendar[] is a pure function of the cell's grown_as + display windows (the
# tree_calendar lesson): perennial -> dormant/growing/bloom/prune bracketed by frost (frost-free ->
# growing year-round, the evergreen analog); annual -> plant/growing/bloom/season_over. No harvest
# token (bloom IS the cut-for-use window). Recompute-from-dates and fail on any mismatch. Empty
# calendars are the Step-3.5 admission state (skipped). No-op off perennial_woody_ornamental.
from woody_ornamental_calendar import woody_ornamental_calendar_violations
print("A14. woody_ornamental calendar coherence (calendar == derive(grown_as, dates); no-op off scope)")
_woodycal = woody_ornamental_calendar_violations(crop)
print(f"  woody_ornamental calendar violations: {len(_woodycal)}")
for m in _woodycal:
    fail(f"woody_ornamental calendar: {m}")

# ---------------- A15. berries_woody structural cert (no-op off berries_woody) ----------------
# Blueberry (anchor 18, the FIRST and only berries_woody crop) is a woody fruiting shrub whose
# growable TYPE is chill-gated by region and whose calendar SHAPE splits by per-cell leaf_habit.
# This asserts the structural invariants the generic checks do not encode -- lifecycle scalars +
# the chill gate signature (gating_factors contains chill_hours, chill_hours_required set -- the
# deliberate INVERSE of the woody-ornamental gate, which REJECTS chill_hours_required), the prose
# backstop, self_fertile=false + no apple cross-pollination machinery, no tree machinery (rootstock),
# and per-cell recommended_type/leaf_habit typing + the type COVERAGE invariant + token placement
# (deciduous has dormant, evergreen has none, never season_over/renovation). chill_hours_delivered is
# a KEPT cell key (the gate basis), not a tree mis-route. No-op off basis. (blueberry, 2026-06-22.)
from berries_woody_gate import berries_woody_violations
print("A15. berries_woody structural cert (lifecycle + chill gate + recommended_type/leaf_habit + coverage; no-op off scope)")
_bwoody = berries_woody_violations(crop)
print(f"  calendar_basis={crop.get('calendar_basis')!r} | berries_woody violations: {len(_bwoody)}")
for m in _bwoody:
    fail(f"berries_woody: {m}")

# ---------------- A16. berries_woody calendar coherence (DERIVED-from-dates) ----------------
# The blueberry calendar[] is a pure function of the cell's leaf_habit + bloom/harvest windows
# (the tree_calendar lesson): deciduous -> the tree dormant/prune/bloom/growing/harvest/care cycle;
# evergreen -> growing year-round with bloom/harvest/care (no dormant, no season_over). Recompute-
# from-dates and fail on any mismatch. Empty calendars are the Step-3.5 admission state (skipped).
# No-op off berries_woody.
from berry_woody_calendar import berry_woody_calendar_violations
print("A16. berries_woody calendar coherence (calendar == derive(leaf_habit, dates); no-op off scope)")
_bwoodycal = berry_woody_calendar_violations(crop)
print(f"  berries_woody calendar violations: {len(_bwoodycal)}")
for m in _bwoodycal:
    fail(f"berries_woody calendar: {m}")

# ---------------- A17. npk_ratio present-or-explicit-null (UNIVERSAL, not archetype-gated) ----------------
# The feeding pill (FeedingCard .fert-npk + app ap-npk) rendered the whole npk_hint PARAGRAPH
# instead of a ratio (audit F3, all 18 anchors). A dedicated render-ready fertilizer.npk_ratio
# (a bare "N-P-K" string, derived once from the verified hint) fixes it, with an explicit-null
# sentinel + a short npk_tag fallback for the genuinely ratio-less crops (citrus/allium/lavender/
# blueberry). No-op for a crop with no npk_hint surface (indoor microgreens). (Phase A, 2026-06-24.)
from npk_gate import npk_ratio_violations
print("A17. npk_ratio present-or-explicit-null (no-op off npk_hint surface)")
_npk = npk_ratio_violations(crop)
print(f"  npk_ratio violations: {len(_npk)}")
for m in _npk:
    fail(f"npk: {m}")

# ---------------- A18. chill-delivered is crop-invariant (UNIVERSAL; the F2 refactor) ----------------
# chill_hours_delivered is a CLIMATE datum that was authored PER CROP, so peach/apple/blueberry
# disagreed at the same region+zone (audit F2). It now lives ONCE in the shared top-level
# region_chill_delivered table; NO crop may carry it (region rollup or resolved cell). With no
# per-crop overrides + one table, "crop-invariant per region+zone" holds by construction. The
# table's own [lo,hi] shape is validated dataset-wide in release_verify. (Phase A, 2026-06-24.)
from chill_gate import chill_delivered_absent_violations
print("A18. chill-delivered crop-invariance (no per-crop chill_hours_delivered)")
_chill = chill_delivered_absent_violations(crop)
print(f"  per-crop chill_hours_delivered violations: {len(_chill)}")
for m in _chill:
    fail(f"chill: {m}")

# ---------------- A19. companion shape (UNIVERSAL; the F4/F6 armor) ----------------
# Two render defects the audit found across the anchors: (F4) a companion stored as a BARE
# STRING is silently dropped by CompanionsCard.normCompanions -> renders as nothing (lemon/
# orange/basil/green-beans); (F6) goods placed ONLY in the beginner-only bucket (good_beginner)
# never render in seasoned mode (apple). This gate requires every entry to be a well-formed
# object with a `name`, and a crop's goods/bads to be reachable from a seasoned-readable bucket
# (good_seasoned | good_beginner_seasoned). No-op for a crop with no companions dict (indoor).
# The per-entry `why` copy is policed by the dual-voice gate B; this is the renderability shape.
from companion_shape_gate import companion_shape_violations
print("A19. companion shape (no bare strings + name + seasoned-readable bucket; no-op off companions)")
_comp = companion_shape_violations(crop)
print(f"  companion shape violations: {len(_comp)}")
for m in _comp:
    fail(f"companion: {m}")

# ---------------- A26. companion per-register why-fill (B5; Pass-2 back-fill landed 2026-06-26) ----
# A19 is shape only; this catches the BARE-NAME render: a companion that renders in a register but
# carries no `why` for THAT register (seasoned-readable -> why_seasoned, beginner-readable ->
# why_beginner, both-bucket -> both). Does NOT enforce reachability (beginner-only companions are
# legitimate curation, Trevor 2026-06-25). No-op off companions.
from companion_shape_gate import companion_why_fill_violations
print("A26. companion why-fill (each rendered companion carries its register's why)")
_cwhy = companion_why_fill_violations(crop)
print(f"  companion why-fill violations: {len(_cwhy)}")
for m in _cwhy:
    fail(f"companion why-fill: {m}")

# ---------------- A27. companion evidence transparency (B5; decision a) ----------------
# Every companion (good OR bad) must declare honest evidence via the RENDERED field `provenance`
# ({label, confidence}); CompanionsCard reads provenance.label. Flat evidence_label/confidence are
# legacy (app-preview) and NOT checked. Speculative-but-labeled (mechanistic/low) is allowed. No-op
# off companions. (Field corrected to provenance 2026-06-26 -- the earlier flat check false-flagged
# the provenance-only crops.)
from companion_shape_gate import companion_evidence_violations
print("A27. companion evidence transparency (provenance.label + confidence on every companion)")
_cev = companion_evidence_violations(crop)
print(f"  companion evidence violations: {len(_cev)}")
for m in _cev:
    fail(f"companion evidence: {m}")

# ---------------- A20. display-readiness, archetype-aware (the F5 armor) ----------------
# Cert validates BIOLOGY + sources but not that the fields each guide CARD reads are present, so
# a crop can certify and render a BLANK Hero/Ph/Feeding card (audit F5: lemon sunlight/water/
# fertilizer-grid; orange ph.preferred_range/container/fertilizer-grid). This asserts per-archetype
# field PRESENCE -- universal sunlight/water, plus (non-indoor) sunlight_hours/ph.preferred_range/
# spacing/fertilizer-grid + a real container_ok decision. Respects legitimate N/A (indoor surface,
# in-ground container_ok==False). Enforces presence, never source-correctness.
from display_readiness_gate import display_readiness_violations
print("A20. display-readiness (archetype-aware field presence; the Hero/Ph/Feeding cards)")
_disp = display_readiness_violations(crop)
print(f"  display-readiness violations: {len(_disp)}")
for m in _disp:
    fail(f"display: {m}")

# ---------------- A21. berries_woody variety-chill presence (no-op off berries_woody) ----------------
# WI3: locks the WI4 string->numeric chill migration so a future berries_woody crop cannot
# reship the legacy `chill_hours` STRING that broke blueberry's chill gauge (audit F2). A15
# polices the CROP-level chill gate basis; this polices the per-VARIETY shape chillBuckets/
# tree.ts reads: every recommended variety carries a NUMERIC chill_hours_required + a
# chill_hours_range (null or a [lo,hi] pair, lo == required), and NO string chill_hours.
# No-op off berries_woody. (2026-06-25.)
from berries_woody_gate import berries_woody_variety_chill_violations
print("A21. berries_woody variety-chill presence (numeric chill_hours_required + range; no string; no-op off scope)")
_bwchill = berries_woody_variety_chill_violations(crop)
print(f"  berries_woody variety-chill violations: {len(_bwchill)}")
for m in _bwchill:
    fail(f"berries_woody variety-chill: {m}")

# ---------------- A22. perennial (tree) variety-chill TYPE lock (no-op off perennial_chill_gated) ----------------
# The deciduous-tree analog of A21: every recommended variety must carry a NUMERIC
# chill_hours_required (no string/legacy form). A string variety chill was previously ungated
# for trees (A21 is berries_woody-only) AND silently dropped from min_variety_chill()'s no-fruit-
# split floor, so it could reclassify calendar cells unseen. No-op off perennial_chill_gated.
# (Closes incognito-audit B2. 2026-06-25.)
from perennial_gate import perennial_variety_chill_violations
print("A22. perennial variety-chill type lock (numeric chill_hours_required; no string; no-op off scope)")
_pvchill = perennial_variety_chill_violations(crop)
print(f"  perennial variety-chill violations: {len(_pvchill)}")
for m in _pvchill:
    fail(f"perennial variety-chill: {m}")

# ---------------- A24. annual calendar token PLACEMENT (the B1 armor; companion to A5) ----------------
# A5 (annual_coherence_violations) checks length + token enum + heat_pause/declared-months
# ALIGNMENT, but never checks that a PAUSE token sits in a legitimate slot. The actual
# drift defense (annual_calendar_violations) existed in code with ZERO callers (audit B1).
# It is NOT a full re-derive -- the Step-5.5 deriver reproduces only the simplest cells
# (basil/zinnia); ~190/200 certified annual cells are legitimately hand-authored multi-
# cycle/winter-wrap/heat-inverted shapes with month-rounding, so a strict re-derive would
# cry wolf. Instead it gates the audit-B1 defect classes with empirically zero FPs on all
# 10 certified annuals: cold_pause/wait on a plant_out month, and an undeclared heat_pause
# on a CORE plant_out/harvest month (pause-on-plant / pause-on-harvest). Thermal BACKING of
# a self-consistent heat_pause is B3; cold-on-harvest is unflaggable (display overstatement).
# No-op off frost_anchored. (Closes incognito-audit B1. 2026-06-25.)
from annual_calendar import annual_calendar_violations
print("A24. annual calendar token placement (no pause on an active window; no-op off annual)")
_aplace = annual_calendar_violations(crop)
print(f"  annual calendar placement violations: {len(_aplace)}")
for m in _aplace:
    fail(f"annual-calendar placement: {m}")

# ---------------- A28. heat_pause thermal backing (B3; Pass-1 back-fill landed 2026-06-26) ----------
# A24 checks placement, A5 checks months<->calendar alignment, but neither requires a shown
# heat_pause to be BACKED. This does: wherever a frost_anchored annual's calendar SHOWS a heat_pause
# token, the cell must carry a heat_pause object with months + basis_seasoned prose + >=1 source each
# anchored by a URL. A heat exclusion is crop+region+zone physiology (carrot pauses Mar-Aug while
# zucchini pauses Jul-Aug in the same desert zone), so it is backed AT THE CELL, not via a shared
# table. No-op off frost_anchored. (Closes incognito-audit B3.)
from annual_calendar import heat_pause_backing_violations
print("A28. heat_pause thermal backing (every shown heat_pause has months + basis + source; no-op off annual)")
_hpb = heat_pause_backing_violations(crop)
print(f"  heat_pause backing violations: {len(_hpb)}")
for m in _hpb:
    fail(f"heat_pause backing: {m}")

# ---------------- A25. register completeness (every prose field is RULED; scale armor) ----------------
# The roster-completeness gate's per-crop half: a prose-shaped string whose key matches no ruling
# class is the generalized bolting-class miss -- a bot authoring a NEW crop with a novel prose field
# would otherwise ship it unruled. Ran standalone before; wired always-on here (0 FP across all 123
# crops). The companion `why`/`reason` §5 deferral is excused. register_FILL (the authored-not-null
# half) and the companion why-fill / evidence gates are NOT yet wired -- they await the B5 back-fill
# (see the corrections log). (B5, 2026-06-25.)
from register_completeness_gate import (register_completeness_violations,
                                         backend_key_laundering_violations)
print("A25. register completeness (every prose field is ruled; halts on a novel unruled field)")
_regcomp = register_completeness_violations(crop)
print(f"  unruled prose field(s): {len(_regcomp)}")
for m in _regcomp:
    fail(f"register-completeness: unruled prose field {m}")

# ---------------- A35. backend-key dash-laundering (C11(c)) ----------------
# summary/claim/note are backend keys exempt from the dash/temp scan + A25; a user-facing string
# under one OUTSIDE a known-backend subtree launders past both (incl. a forbidden `--`).
print("A35. backend-key laundering (summary/claim/note outside a backend subtree)")
_launder = backend_key_laundering_violations(crop)
print(f"  laundering violations: {len(_launder)}")
for m in _launder:
    fail(f"backend-key-laundering: {m}")

# ---------------- A36. CP-required dual-register (C16) ----------------
# A bot can downgrade a should-be-dual consumer field to seasoned-only by omitting the _beginner
# sibling (gate B reads that as legit SP). This enforces the established dual-register consumer set
# (74 base-names + the newly-ruled soil-texture trio). GATE-UNLOCK: the soil-texture fields are RED
# on 7 crops until the claude.ai 21-string beginner back-fill lands (gate-as-worklist).
from cp_required_gate import cp_required_violations
print("A36. CP-required dual-register (established consumer set carries both registers)")
_cpreq = cp_required_violations(crop)
print(f"  CP-required (missing _beginner) violations: {len(_cpreq)}")
for m in _cpreq:
    fail(f"cp-required: {m}")

# ---------------- A29. register FILL (every ruled register field is authored; B5/Pass-3) ----------------
# The FILL half (A25 is the RULED half): every `_seasoned`/`_beginner` register field must be authored
# (not null/empty) -- the gap that let apple ship 30 null fields + peach 46. Skips the frost_risk_note /
# legacy-zones allowlist + the structured-N/A `{applicable:false}` over-flag. Was standalone (so an
# in-progress crop wasn't flagged); wired always-on here now that the Pass-3 back-fill cleared the early
# anchors (register_fill 0 across the 18). A new crop with unauthored register prose now bounces at cert.
from register_fill_gate import register_fill_violations
print("A29. register fill (every ruled _seasoned/_beginner field is authored; not null)")
_regfill = register_fill_violations(crop)
print(f"  unauthored register field(s): {len(_regfill)}")
for m in _regfill:
    fail(f"register-fill: unauthored {m}")

# ---------------- A23. raw-display snake_case (UNIVERSAL; the render-verbatim armor) ----------------
# A20 checks the feeding/watering/Hero fields are PRESENT; this checks the render-VERBATIM ones
# read as PROSE. FeedingCard prints fertilizer.type/timing/frequency as-is (the F3 no-Title-Case
# rule), CareGuideCard prints crop.sunlight as-is, CompanionsCard prints a companion's timing as-is;
# watering.watering_method/drought_tolerance are display-intent prose. The 2026-06-25 scan found 8
# anchors shipping snake_case TOKENS into these (onion fertilizer.type='nitrogen_forward',
# sunlight='full_sun', ...) that render with underscores to growers -- a blind spot of both A20
# (presence-only) and release_verify (dash/degree scan). NO-OP for the categorical token fields the
# renderer maps/humanizes (start_method.start, companions[].category, shape_requirements, ...).
from raw_display_gate import raw_display_violations
print("A23. raw-display snake_case (render-verbatim fields read as prose; no-op for mapped tokens)")
_rawdisp = raw_display_violations(crop)
print(f"  raw-display snake_case violations: {len(_rawdisp)}")
for m in _rawdisp:
    fail(f"raw-display: {m}")

# ---------------- B. dual-voice coverage ----------------
print("B. dual-voice coverage gate (structural walk)")
populated = sp_only = ruled_empty = oos = 0
null_values = []

def dv_walk(o, pat):
    global populated, sp_only, ruled_empty, oos
    if isinstance(o, dict):
        for k, v in o.items():
            if k.endswith("_seasoned"):
                b = k[:-9] + "_beginner"
                if not isinstance(v, str) or not v.strip():
                    ruled_empty += 1
                elif b in o:
                    if o[b] is not None:
                        populated += 1
                    else:
                        # companions why_* are IN-SCOPE as of 2026-06-07 (Trevor): the
                        # former "§5 companions array split, deferred by design" carve-out
                        # (which counted a null why_beginner as out-of-scope) is removed, so
                        # a null _beginner sibling on a dual-register companion is FLAGGED,
                        # not hidden. Seasoned-only companions (good_seasoned/bad_seasoned)
                        # have no why_beginner key -> still counted SP, unaffected.
                        null_values.append(f"{pat}.{b}")
                else:
                    sp_only += 1
            dv_walk(v, f"{pat}.{k}" if pat else k)
    elif isinstance(o, list):
        for i, x in enumerate(o):
            dv_walk(x, f"{pat}[{i}]")

dv_walk(crop, "")
print(f"  populated CP: {populated} | SP seasoned-only: {sp_only} | ruled-empty/non-prose: {ruled_empty} | out-of-scope §5: {oos} (companions why_* now in-scope, expect 0)")
print(f"  null_values: {len(null_values)}")
for m in null_values:
    fail(f"dual-voice null sibling: {m}")

# ---------------- C+D. dash + temperature (user-facing) ----------------
print("C/D. dash + temperature notation gates (user-facing strings)")
dash_hits, degf_hits = [], []

_DEGF_RE = re.compile(r"\bdegrees?\s*F\b|\bdeg\.?\s*F\b|°\s+F")


def _scan_user_str(s, p):
    if "--" in s or "—" in s:
        dash_hits.append((p, s[:80]))
    if _DEGF_RE.search(s):
        degf_hits.append((p, s[:80]))


def uf_walk(o, pat):
    if isinstance(o, dict):
        for k, v in o.items():
            p = f"{pat}.{k}" if pat else k
            if not is_backend(k, pat):
                if isinstance(v, str):
                    _scan_user_str(v, p)
                # re-audit #2 D16: a user-facing LIST element string is rendered too, but the old
                # walk only tested dict VALUES, so a list laundering `--`/"degrees F" shipped. Scan
                # the string elements of a user-facing list (backend lists, e.g. `sources`, are
                # skipped by is_backend above). 0-FP on the 18.
                elif isinstance(v, list):
                    for i, x in enumerate(v):
                        if isinstance(x, str):
                            _scan_user_str(x, f"{p}[{i}]")
            uf_walk(v, p)
    elif isinstance(o, list):
        for i, x in enumerate(o):
            uf_walk(x, f"{pat}[{i}]")

uf_walk(crop, "")
print(f"  user-facing dash hits: {len(dash_hits)} | non-canonical temperature forms: {len(degf_hits)}")
for p, s in dash_hits: fail(f"dash: {p}: {s!r}")
for p, s in degf_hits: fail(f"temp form: {p}: {s!r}")

# ---------------- E. source-tier ----------------
print("E. source-tier discipline")
cat = data["source_catalog"]
cited = set()

def src_walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if (k == "sources" or k.endswith("_sources")) and isinstance(v, list):
                cited.update(x for x in v if isinstance(x, str))
            if k.endswith("anchoring_urls") and isinstance(v, dict):
                cited.update(v.keys())
            src_walk(v)
    elif isinstance(o, list):
        for x in o:
            src_walk(x)

src_walk(crop)
bad = sorted(s for s in cited if s not in cat)
not_t1 = sorted(s for s in cited if s in cat and cat[s].get("tier") != "T1")
print(f"  distinct source IDs: {len(cited)}; uncatalogued: {len(bad)}; non-T1: {len(not_t1)}")
for s in bad: fail(f"source-tier: {s} not in catalog")
for s in not_t1: fail(f"source-tier: {s} tier={cat[s].get('tier')}")

# ---------------- F. anchoring completeness (1A layer-scoped, amended) ----------------
print("F. anchoring completeness (1A layer-scoped + sibling-pair predicate)")
region_roots = [id((crop.get("regions") or {}).get(r)) for r in (crop.get("regions") or {})]
gaps, claim_leaves = [], 0

def _is_http_url(u):
    """A real anchoring URL: an http(s) string, not a truthy placeholder ('TODO'/'pending')."""
    return isinstance(u, str) and u.startswith(("http://", "https://"))


def check_pair(srcs, au, where):
    global claim_leaves
    claim_leaves += 1
    if not isinstance(au, dict):
        gaps.append(f"{where}: no anchoring dict (sources={srcs})")
        return
    for s in srcs:
        if s not in au:
            gaps.append(f"{where}: {s} unanchored")
        # re-audit #2 D9 (shape half): the url must be a real http(s) URL, not a truthy placeholder
        # (`url:"TODO"`/`"pending"`). The CONTENT half -- whether the page supports the claim, and the
        # honesty of `verified` (a date string in this dataset, not a bool) -- is the source-fidelity
        # layer's job (the daily review + the periodic URL-liveness sweep), not a deterministic gate.
        elif not _is_http_url(au[s].get("url")) or not au[s].get("verified"):
            gaps.append(f"{where}: {s} malformed entry")

def anchor_walk(o, pat, in_zones, in_bolting):
    if isinstance(o, dict):
        srcs = o.get("sources")
        if (isinstance(srcs, list) and srcs and not in_zones and not in_bolting
                and id(o) not in region_roots and "verification_status" not in pat):
            check_pair(srcs, o.get("anchoring_urls"), pat or "<crop root>")
        for k, v in o.items():
            anchor_walk(v, f"{pat}.{k}" if pat else k,
                        in_zones or k == "zones", in_bolting or k == "bolting")
    elif isinstance(o, list):
        for i, x in enumerate(o):
            anchor_walk(x, f"{pat}[{i}]", in_zones, in_bolting)

anchor_walk(crop, "", False, False)
# sibling-named pairs at the crop root (s11_finding_001 predicate fix)
for k in list(crop.keys()):
    if k.endswith("_sources") and isinstance(crop[k], list) and crop[k]:
        sib = k[: -len("_sources")] + "_anchoring_urls"
        check_pair(crop[k], crop.get(sib), sib)
print(f"  claim-bearing leaves in gate scope: {claim_leaves}; gaps: {len(gaps)}")
for g in gaps: fail(f"anchoring: {g}")

# ---------------- G. flip state + two-field predicate ----------------
print("G. flip state")
print(f"  launch_ready_core={vs.get('launch_ready_core')} launch_ready_seasoned={vs.get('launch_ready_seasoned')} status={vs.get('status')!r}")
of = vs.get("open_findings") or []
blockers = [f for f in of if isinstance(f, dict) and f.get("blocks_launch") and f.get("status") != "resolved"]
print(f"  open_findings blockers (blocks_launch AND status!=resolved): {len(blockers)}")
for b in blockers: fail(f"open finding blocks launch: {b.get('id', b)}")

print()
if violations:
    print(f"GATE: {len(violations)} VIOLATION(S)")
    sys.exit(1)
print("GATE: PASS (remember: full per-crop §3 + verbatim scan + roster gate are separate)")
