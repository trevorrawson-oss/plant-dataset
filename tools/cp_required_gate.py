#!/usr/bin/env python3
"""CP-required (dual-register) cert gate -- closes the dual-voice-by-omission hole (whole_crop_gate
A36; incognito-redteam C16, Trevor ruling 2026-06-27).

THE HOLE: gate B treats a `_seasoned` field with NO `_beginner` SIBLING KEY as legitimately
seasoned-only ("Presence IS the visibility declaration"). So a bot can downgrade a should-be-dual
consumer field to single-register by simply not writing the sibling -- beginners get no copy and
nothing fires. This gate enforces the ESTABLISHED dual-register consumer set: a base-name in
`CP_BASE_NAMES` that has a populated `_seasoned` MUST also have a `_beginner` sibling in the same
dict.

WHY a HARDCODED allowlist (not data-derived): if the CP set were derived from the data, a bot's
omission would change the rule (the field stops being "always-dual") and ESCAPE -- self-defeating.
The set is the established convention, RULED, amendable. It is exactly the 74 base-names the 18
already carry both registers for, so the established set is 0-FP. The MIXED base-names (`why`,
`notes`, `synthesis_note`) are deliberately EXCLUDED -- they have legit SP contexts (companion why
renders both via fallback per B5; variety notes are SP per Trevor) -- as are the never-dual backend
notes (`*_basis`, `frost_risk_note`, `design_note`, `reason`, ...).

GATE-UNLOCK (Trevor): the soil-texture trio is ruled CP but the 7 crops carrying it have no
`_beginner` yet, so this gate goes RED on those 21 cells until a claude.ai back-fill lands
(gate-as-worklist, like the Phase B / register passes that intentionally turned anchors RED).
"""

# The 74 established dual-register consumer base-names -- every `_seasoned` occurrence in the 18
# carries its `_beginner` sibling (0-FP by construction). description / care / harvest / storage /
# diagnostics / tips / region prose. EXTEND when a new consumer field is ruled dual-register.
CP_BASE_NAMES = frozenset({
    'amendments', 'amount', 'approach', 'avoid_after', 'bloom_time', 'body', 'cane_management',
    'cause', 'chill_basis', 'chill_hours_note', 'cold_basis', 'container_overwintering',
    'critical_periods', 'day_length_note', 'deadheading', 'description', 'detail', 'explainer',
    'fertilizer_adjustment', 'first_year_note', 'fix', 'freezer', 'frequency', 'fridge',
    'grown_as_note', 'hardening_off', 'hardiness_notes', 'harvest_ready', 'heat_basis',
    'identification', 'label', 'log_prompt', 'management', 'message', 'method', 'method_note',
    'name', 'next_season_tip', 'note', 'notify_message', 'npk_hint', 'organic_treatment',
    'peak_production', 'per_plant', 'planting_method_notes', 'pollinator_notes',
    'preferred_description', 'prevention', 'region_notes', 'renovation', 'room_temp',
    'safe_sowing_note', 'saucer_practice', 'self_watering_notes', 'shape_requirements',
    'signs_overwater', 'signs_underwater', 'soil_prep', 'suitability_note', 'symptom',
    'symptoms', 'text', 'timing', 'tip', 'title', 'traits', 'type', 'type_note',
    'type_selection', 'user_action', 'watering_adjustment', 'what_happened', 'what_to_look_for',
    'year_one_notes',
    # --- C16 GATE-UNLOCK (Trevor 2026-06-27): newly ruled CP; RED on the 7 crops until the
    #     claude.ai 21-string beginner back-fill lands. ---
    'preferred_texture', 'problematic_texture', 'tolerated_texture',
})


def cp_required_violations(crop):
    """Return a list ([] = clean): each populated `<base>_seasoned` whose base is a CP field but
    whose `<base>_beginner` sibling is ABSENT from the same dict (the dual-voice omission). An
    empty/whitespace `_seasoned` is not a populated field (A29 owns emptiness)."""
    V = []

    def walk(o, pat):
        if isinstance(o, dict):
            for k, v in o.items():
                p = (pat + "." + k) if pat else k
                if (k.endswith("_seasoned") and isinstance(v, str) and v.strip()):
                    base = k[:-len("_seasoned")]
                    if base in CP_BASE_NAMES and (base + "_beginner") not in o:
                        V.append(f"{p}: CP consumer field {base!r} has a _seasoned but NO _beginner "
                                 f"sibling -- a dual-register field must carry both (beginners get "
                                 f"no copy otherwise)")
                walk(v, p)
        elif isinstance(o, list):
            for i, x in enumerate(o):
                walk(x, f"{pat}[{i}]")

    walk(crop, "")
    return V


if __name__ == "__main__":
    import json
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"
    data = json.load(open(path, encoding="utf-8"))
    total = 0
    for c in data["crops"]:
        vs = cp_required_violations(c)
        if vs:
            print(f"  {c.get('slug')}:")
            for v in vs:
                print(f"     {v}")
            total += len(vs)
    print(f"cp_required gate: {total} violation(s) across {len(data['crops'])} crops")
    sys.exit(1 if total else 0)
