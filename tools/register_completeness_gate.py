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
import json, sys, re, collections, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from field_classification import BACKEND_KEYS, BACKEND_KEY_RE, _basis_family, BACKEND_PATH_SUBSTR

# C11(c) (incognito-redteam, Trevor 2026-06-27): backend-named keys that carry a user-facing
# string OUTSIDE a known-backend subtree launder past the dash/temp scan + A25 (they are exempt
# from both BY KEY). The check is PATH-based on purpose: `claim` is itself in BACKEND_KEYS, so an
# is_backend(key,...) test would never catch it -- only "is this in a backend SUBTREE" does.
LAUNDERING_KEYS = {"summary", "claim", "note"}

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
    # AUDIT-LEAF (evidence machinery). `source_quote` reclassified SP->EXCLUDED per
    # register_bearing_field_inventory addendum 2026-06-08 (verbatim third-party text =
    # backend evidence, never rendered; matches whole_crop_gate). `_seasoned` variant is
    # un-renamed to bare in the dataset, so the bare key is what is ruled here.
    "url","verified","accessed","publisher","source_class","source_note","source_quote",
    "verification_log_ref","filing_record","disposition","scope","session","field",
    "assigned_to","deferred_to","last_audited","summary","resolution_note",
    "filed_in","filed_in_session","resolved_in","resolved_by","note_internal",
    # ENUM / CN-PRIMITIVE
    "risk","severity","action","condition","type","confidence","category","timing",
    "archetype","flower_type","light_required","lifecycle","self_fertile",
    "heat_tolerance","growth_habit","tier","frequency","unit","method","label",
    "evidence_label","trigger_type","classification","suitability","verdict",
    "year_phase",  # tree growth_stages: establishment|annual_cycle (peach 6-8a; timing_* siblings are suffix-ruled CORE-PROSE)
    "rootstock_selection_basis",  # FLAG 1: size (pome) | soil_pest_tolerance (stone) -- per-archetype enum (apple)
    # USER-FACING-CATEGORICAL (dash-gated, no suffix)
    "sunlight","water","difficulty","triggers","spacing","depth","light",
    # npk_ratio = the render-ready "N-P-K" pill string (e.g. "5-10-10"); npk_tag = the
    # short qualitative fallback for ratio-less crops (e.g. "Nitrogen-forward"). Both
    # single-form, read identically by both registers, derived once from the verified
    # npk_hint -- USER-FACING-CATEGORICAL, not dual-register prose. (Phase A NPK, 2026-06-24.)
    "npk_ratio","npk_tag",
    # CN-METADATA (evidence structure)
    "source","source_id","claim",
    # CN planting-window primitives (zones / regions resolved_by_zone)
    "plant_out","start_indoors","direct_sow","harvest","harvest_start","harvest_end",
    "first_plant_date","last_plant_date","bloom","planting_note","zone_notes",
    "notes","succession_spring","succession_fall","succession_continuous","window_days","offset_days",
    "interval_days","label_beginner",
    # SCHEMA 2.9 universal-plain (bare-by-design -- one plain line shown to BOTH
    # registers, no _seasoned/_beginner split; see schema_2_9 scope Section 9).
    "recommended_rootstock_note","establishment_note","what_to_ask_nursery","recommended_note",
    # --- incognito-redteam C11 Part 1 (Trevor ruling 2026-06-27): the 49 short-string keys the
    #     18 carry unruled, ruled into their classes so the tightened A25 (flag ANY unruled string)
    #     does not flood. See docs/c11-c16-ruling-list-2026-06-27.md. ---
    # USER-FACING-CATEGORICAL (short rendered token/label, read identically by both registers):
    "drainage_requirement","organic_matter_preference","preferred_texture_core",
    "problematic_texture_core","tolerated_texture_core","shape_requirements","grown_as",
    "leaf_habit","recommended_type","bloom_group","season","days_or_season","size_class",
    "harvest_urgency","level","system","species","subtitle","title","cane_type","gravel_layer",
    "drought_tolerance","watering_method","start","day_length_type","recommended_day_length_type",
    # ENUM / NOTIFICATION + AUDIT MACHINERY:
    "audience","offset_from","trigger","stage","measures","cause","author",
    "last_reviewed_operation","overrides_tip_id","verified_date","recommended_rootstock",
    # CN CLIMATE / PLANTING-WINDOW PRIMITIVE (resolved_from dates + bloom window):
    "first_frost","last_frost","window",
    # NUMERIC-AS-STRING (zone / lifespan values carried as strings; categorical, not prose):
    "hardiness_zone_max","hardiness_zone_min","reliable_fruit_zone_max","reliable_fruit_zone_min",
    "productive_lifespan_years",
}

# Excluded by PATH (whole subtrees that are audit/machinery -- §4 AUDIT_LEAF /
# MACHINERY). A field anywhere under these is ruled-excluded.
# `sources_summary` is named backend machinery in the arc checklist (§2; dash-exempt,
# no siblings, never rendered); its whole subtree (`primary`, `frost_data`, `_note`, ...)
# is EXCLUDED. Ruled by Trevor at the basil herb anchor, 2026-06-12.
EXCLUDED_PATH_SUBSTR = ("plantings_provenance", "verification_status", "anchoring_urls",
                        "sources_summary",
                        "uscrn_validation")  # C11 Part 1: the uscrn_* date/coverage machinery block

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
    if k == "use" and "varieties" in pat: return True  # variety use descriptor, categorical (e.g. "fresh eating, cooking"); apple's Golden Delicious embeds the universal-pollinizer flag here (migrate to recommended_note at 6-8)
    if k in ("value", "parent") and ".delta." in pat and "varieties.recommended" in pat: return True  # variety-delta overlay descriptor, categorical (Trevor 2026-06-12, lemon anchor; e.g. "compact; container-friendly", "high-20s F damage; fruits z9b-11") -- terse single-form attribute/diff values, not dual-register prose; sets the register treatment for the whole variety-delta model
    if k == "note" and "varieties.recommended" in pat and ".delta." not in pat: return True  # per-variety mix-component descriptor, categorical (Trevor 2026-06-15, microgreens anchor; e.g. "Fast brassica, 8 to 12 days; spicy. No presoak.") -- terse single-form per-variety labels (days/flavor/handling), not dual-register prose; mix components are different SPECIES (the delta cultivar model is N/A). Sets the per-variety recommended[].note convention. Distinct from top-level varieties.note (CP, _seasoned/_beginner) -- the `varieties.recommended` path guard separates them
    if k == "hardiness_note" and "varieties.recommended" in pat: return True  # per-variety hardiness label, categorical (Trevor 2026-06-22, lavender anchor; e.g. "Hardy, reliably perennial in roughly zones 5 to 9.") -- terse single-form per-variety attribute alongside note/use, not dual-register prose; sets the woody-ornamental variety hardiness_note convention
    if k == "saucer_practice" and "container_notes" in pat: return True  # container drainage instruction, USER-FACING-CATEGORICAL bare line (Trevor 2026-06-22, lavender anchor; e.g. "Empty the saucer after watering; lavender must never sit in standing water.") -- one plain instruction read identically by both registers, no _seasoned/_beginner split
    if k == "rate" and "schedule_by_stage" in pat: return True  # per-stage watering AMOUNT, USER-FACING-CATEGORICAL bare value (Trevor 2026-06-23, blueberry anchor; e.g. "1 to 2 inches of water per week including rain") -- a single-form structured amount read identically by both registers, the sibling of the already-EXCLUDED `frequency`/`level`/`system` machinery; the dual-register prose in this block is note_seasoned/note_beginner. First crop whose rate string crossed the prose-length heuristic (peach/strawberry/apple sit just under it)
    if k == "note" and pat == "pet_safe": return True  # pet_safe icon tooltip: single concise line read identically by both registers (Trevor 2026-07-06, post-114 §A; e.g. "Ripe tomatoes are fine, but the leaves and unripe fruit are toxic to cats, dogs, and horses.") -- one plain sentence, no _seasoned/_beginner split; the fuller dual-register prose stays in failure_diagnostics. `note` is a laundering key, so this ruling also exempts pet_safe.note from the C11(c) laundering check
    if k == "toxic_parts" and pat == "pet_safe": return True  # pet_safe: which plant parts are toxic (single-form categorical, e.g. "green foliage and unripe fruit"), sibling of the ruled pet_safe.note
    return False

# --- DEFERRED by design: companions array-split provenance (inventory §5 -- its own
#     reconciliation session). Reported separately; NOT an open "unruled" gap. ---
def deferred(pat, k):
    return "companions" in pat and k == "reason"

# RULING-2 note: a ruled SP/CP field that is NULL is left BARE (un-suffixed); a bare
# null is empty-by-nature, not a finding. is_prose_shaped() returns False for non-str,
# so bare nulls are never flagged here -- RULING-2 is satisfied by construction.

def _is_ruled(pat, k):
    """A string key is RULED (not an open prose gap) when register-suffixed, an excluded/
    backend/categorical key, a zone primitive, or path/categorical-excluded -- the shared
    predicate behind both the per-crop function and the dataset-wide run."""
    return bool(k.endswith("_seasoned") or k.endswith("_beginner")
                or k in EXCLUDED_KEYS
                or k in BACKEND_KEYS or BACKEND_KEY_RE.match(k)  # shared backend KEY slice (kills source_quote/basis drift)
                or _basis_family(k)  # bare *_basis evidence prose is backend (checklist A3; e.g. year_round_basis)
                or re.match(r"zone_\d+_", k)  # zone-N boolean/range primitives
                or excluded_by_path(pat)  # roster keeps its OWN narrow path notion
                or ruled_categorical(pat, k))


def backend_key_laundering_violations(crop):
    """C11(c): a non-empty string under a backend-named key (summary/claim/note) that sits OUTSIDE
    a known-backend subtree (BACKEND_PATH_SUBSTR) is a user-facing string laundering past the
    dash/temp scan + A25, which both exempt these keys. Flag it for review -- rename to a ruled
    field or confirm it is backend. Exempts the ruled-categorical varieties.recommended[].note.
    Returns [] = clean. (The 18 carry these keys only in backend subtrees + that ruled note.)"""
    V = []

    def walk(o, pat):
        if isinstance(o, dict):
            for k, v in o.items():
                p = (pat + "." + k) if pat else k
                if (k in LAUNDERING_KEYS and isinstance(v, str) and v.strip()
                        and not any(s in p for s in BACKEND_PATH_SUBSTR)
                        and not ruled_categorical(pat, k)):
                    V.append(f"{p}: backend-named key {k!r} carries a user-facing string outside a "
                             f"known-backend subtree (launders past the dash/temp + A25 scans); "
                             f"rename to a ruled register field, or confirm it is backend")
                walk(v, p)
        elif isinstance(o, list):
            for x in o:
                walk(x, pat + "[]")

    walk(crop, "")
    return V


def register_completeness_violations(crop):
    """Per-crop half of the roster-completeness gate ([] = clean). Returns the unruled
    prose-field paths in ONE crop -- a prose-shaped string whose key matches no ruling
    class (the bolting-class miss, generalized). The §5 companions `why`/`reason` deferral
    is NOT reported (deferred-by-design, not an open gap). This is the function wired into
    the always-on whole_crop_gate; the __main__ block runs it dataset-wide with samples."""
    out = []

    def walk(o, pat):
        if isinstance(o, dict):
            for k, v in o.items():
                # C11 (Trevor ruling 2026-06-27): flag ANY unruled NON-EMPTY STRING, regardless of
                # length -- the <25-char evasion (mystery_advice:"Water it lots") is closed now that
                # the 49 legit short-string keys are ruled. is_prose_shaped is no longer the gate;
                # an unruled string of any length is a novel field a human must rule (STOP-AND-ASK).
                # Non-string novelty is out of scope (A25 polices PROSE only -- the shape/archetype
                # gates + A33/A34 own numbers/lists); empty/whitespace strings are not novel fields.
                if (isinstance(v, str) and v.strip() and not _is_ruled(pat, k)
                        and not deferred(pat, k)):
                    out.append(pat + "." + k if pat else k)
                walk(v, (pat + "." + k if pat else k))
        elif isinstance(o, list):
            for x in o:
                walk(x, pat + "[]")

    walk(crop, "")
    return out


if __name__ == "__main__":
    PATH = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"
    data = json.load(open(PATH, encoding="utf-8"))

    cand = collections.defaultdict(lambda: {"crops": set(), "sample": None})
    defr = collections.defaultdict(lambda: {"crops": set(), "sample": None})

    def walk(o, pat, crop):
        if isinstance(o, dict):
            for k, v in o.items():
                if isinstance(v, str) and v.strip() and not _is_ruled(pat, k):  # C11: any unruled string
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
