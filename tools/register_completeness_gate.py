#!/usr/bin/env python3
"""Roster-completeness gate (per claude.ai spec, 2026-06-03).

INVERSION: walk every prose-shaped string field on every crop and assert it
matches exactly one ruling class. A prose-shaped field with NO matching ruling
is a HARD VIOLATION (names field + crops + sample). sys.exit(1).

This catches the UNKNOWN field (the bolting-class miss): a gate that only checks
"known roster fields are converted" passes bolting cleanly, because bolting was
never in the roster to check. Here, anything prose-shaped that is neither
register-suffixed NOR in an excluded class STOPS the run until a human rules it.

STOP-AND-ASK, not stop-and-guess: the gate detects + halts ONLY. It never
auto-rules and never auto-converts -- that would re-introduce "matched a pattern,
nobody checked." Detection automated, judgment retained.

Home: per-crop shell pass (admission check on first contact with a crop's
structure) + run dataset-wide as needed. Run:
  python3 tools/register_completeness_gate.py [crops_data_final.json]
"""
import json, sys, re, collections

PATH = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"

# --- Excluded ruling classes (register_bearing_field_inventory_v1_0.md §4 +
#     USER-FACING-CATEGORICAL + CN planting-window primitives). A bare string
#     whose key is here is RULED-excluded and allowed to be unsuffixed. ---
EXCLUDED_KEYS = {
    # MACHINERY / IDENTIFIER
    "id","slug","stage_id","tip_id","region_id","evidence_tier","added_in",
    "last_reviewed","last_operation","last_session","schema_version","last_updated",
    "date","stored_date","resolution_tier","resolution_method","anchor_threshold",
    "fallback_beyond_horizon","calendar_state","window_type","timing_relative",
    "to_spacing","phase","status","image","example_product","plantings_provenance",
    "provenance","lifted_from_zone","name","botanical_name","family","variety",
    "region_label","calendar_basis","resolution_source","from","from_year_round_note",
    # AUDIT-LEAF
    "url","verified","accessed","publisher","source_class","source_note",
    "verification_log_ref","filing_record","disposition","scope","session","field",
    "assigned_to","deferred_to","last_audited","summary","resolution_note",
    "filed_in","filed_in_session","resolved_in","resolved_by","note_internal",
    # ENUM / CN-PRIMITIVE
    "risk","severity","action","condition","type","confidence","category","timing",
    "archetype","flower_type","light_required","lifecycle","self_fertile",
    "heat_tolerance","growth_habit","tier","frequency","unit","method","label",
    "evidence_label","trigger_type","classification","suitability","verdict",
    # USER-FACING-CATEGORICAL (dash-gated, no suffix)
    "sunlight","water","difficulty","triggers","spacing","depth","light",
    # CN-METADATA (evidence structure)
    "source","source_id","claim",
    # CN planting-window primitives (zones / regions resolved_by_zone)
    "plant_out","start_indoors","direct_sow","harvest","harvest_start","harvest_end",
    "first_plant_date","last_plant_date","bloom","planting_note","zone_notes",
    "notes","succession_spring","succession_fall","window_days","offset_days",
    "interval_days","label_beginner",
}

# Excluded by PATH (whole subtrees that are audit/machinery -- §4 AUDIT_LEAF /
# MACHINERY). A field anywhere under these is ruled-excluded.
EXCLUDED_PATH_SUBSTR = ("plantings_provenance", "verification_status", "anchoring_urls")

def excluded_by_path(pat):
    return any(s in pat for s in EXCLUDED_PATH_SUBSTR)

def is_prose_shaped(v):
    """Sentence-like string: long enough or carries sentence structure.
    Deliberately conservative -- short categoricals (e.g. water:'High') are NOT
    prose and are roster-excluded by key anyway; this only sharpens the signal."""
    if not isinstance(v, str):
        return False
    v = v.strip()
    if len(v) < 25:
        return False
    return bool(re.search(r"[.;:?]\s", v)) or " " in v and len(v) >= 40

# --- Positive roster: fields RULED as USER-FACING-CATEGORICAL (bare-by-design). ---
def ruled_categorical(pat, k):
    if k == "good_after" and pat.endswith("rotation"): return True       # bare crop list
    if k == "when" and pat.endswith("thinning"): return True             # short timing phrase
    if k in ("fruit_size", "fruit_color") and "varieties_detail" in pat: return True
    return False

# --- DEFERRED by design: companions array-split provenance (inventory §5 -- its own
#     reconciliation session). Reported separately; NOT an open "unruled" gap. ---
def deferred(pat, k):
    return "companions" in pat and k == "reason"

# RULING-2 note: a ruled SP/CP field that is NULL is left BARE (un-suffixed); a bare
# null is empty-by-nature, not a finding. is_prose_shaped() returns False for non-str,
# so bare nulls are never flagged here -- RULING-2 is satisfied by construction.

data = json.load(open(PATH, encoding="utf-8"))

cand = collections.defaultdict(lambda: {"crops": set(), "sample": None})
defr = collections.defaultdict(lambda: {"crops": set(), "sample": None})
def walk(o, pat, crop):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, str):
                ruled = (k.endswith("_seasoned") or k.endswith("_beginner")
                         or k in EXCLUDED_KEYS
                         or re.match(r"zone_\d+_", k)  # zone-N boolean/range primitives
                         or excluded_by_path(pat)
                         or ruled_categorical(pat, k))
                if not ruled and is_prose_shaped(v):
                    p = pat + "." + k if pat else k
                    bucket = defr if deferred(pat, k) else cand
                    c = bucket[p]; c["crops"].add(crop)
                    if c["sample"] is None: c["sample"] = v[:75]
            walk(v, (pat + "." + k if pat else k), crop)
    elif isinstance(o, list):
        for x in o:
            walk(x, pat + "[]", crop)

for c in data.get("crops", []):
    walk(c, "", c.get("slug", "?"))

print("roster-completeness gate -- prose fields with NO matching ruling:\n")
for p in sorted(cand):
    f = cand[p]
    print("  UNRULED  %-46s  %3d crops  e.g. %r" % (p, len(f["crops"]), f["sample"]))
if defr:
    print("\n  (deferred by design -- inventory §5 companions reconciliation, NOT an open gap:)")
    for p in sorted(defr):
        print("  DEFERRED %-46s  %3d crops" % (p, len(defr[p]["crops"])))

if cand:
    print("\nGATE: HALT -- %d unruled prose pattern(s). A HUMAN must rule each in" % len(cand))
    print("register_bearing_field_inventory_v1_0.md (CP / SP / CATEGORICAL / EXCLUDED)")
    print("before the conversion or new-crop admission proceeds. Do NOT auto-rule.")
    sys.exit(1)
print("\nGATE: PASS -- 0 unruled prose fields (modulo %d deferred §5 companions entries)." % len(defr))
print("Every prose field on every crop is ruled-and-converted or ruled-and-deferred.")
sys.exit(0)
