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


# ---------------- generic §3 subset (EXTEND PER CROP) ----------------
print("A. §3 cross-field consistency -- GENERIC SUBSET ONLY (author the full per-crop set)")
ph = crop.get("ph") or {}
if ph.get("preferred_range") and ph.get("tolerated_range"):
    ok = (ph["tolerated_range"][0] <= ph["preferred_range"][0]
          and ph["preferred_range"][1] <= ph["tolerated_range"][1])
    print(f"  ph preferred {ph['preferred_range']} within tolerated {ph['tolerated_range']}: {'PASS' if ok else 'FAIL'}")
    if not ok: fail("§3 ph range nesting")
cn = crop.get("container_notes") or {}
if cn.get("container_ok"):
    ok = bool(cn.get("min_pot_gallons"))
    print(f"  container_ok=True => min_pot_gallons={cn.get('min_pot_gallons')}: {'PASS' if ok else 'FAIL'}")
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
_perennial = perennial_cert_violations(crop)
print(f"  calendar_basis={crop.get('calendar_basis')!r} | perennial violations: {len(_perennial)}")
for m in _perennial:
    fail(f"perennial: {m}")

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

def uf_walk(o, pat):
    if isinstance(o, dict):
        for k, v in o.items():
            p = f"{pat}.{k}" if pat else k
            if isinstance(v, str) and not is_backend(k, pat):
                if "--" in v or "—" in v:
                    dash_hits.append((p, v[:80]))
                if re.search(r"\bdegrees?\s*F\b|\bdeg\.?\s*F\b|°\s+F", v):
                    degf_hits.append((p, v[:80]))
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

def check_pair(srcs, au, where):
    global claim_leaves
    claim_leaves += 1
    if not isinstance(au, dict):
        gaps.append(f"{where}: no anchoring dict (sources={srcs})")
        return
    for s in srcs:
        if s not in au:
            gaps.append(f"{where}: {s} unanchored")
        elif not au[s].get("url") or not au[s].get("verified"):
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
