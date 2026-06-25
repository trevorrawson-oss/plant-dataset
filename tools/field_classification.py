#!/usr/bin/env python3
"""field_classification.py -- the ONE canonical backend/user-facing predicate.

THE single source of truth for "is this field BACKEND" (behind-the-scenes
audit / evidence / machinery / own-voice reasoning), shared by all three gates:
  - whole_crop_gate.py  §C/D dash + temperature scan (skip backend strings)
  - release_verify.py   §D  dash + spelled-degrees scan (skip backend strings)
  - register_completeness_gate.py  the backend slice of its EXCLUDED roster

BACKEND = `--`, em-dash, and spelled "degrees F" are TOLERATED (CLAUDE.md); the
field is not rendered to growers as register-bearing copy. USER-FACING = held to
the dash/temperature canon.

Provenance: promoted from whole_crop_gate's is_backend (the most complete of the
three) + release_verify's BACKEND_SUBSTR merged in + the register-bearing-field
inventory v1.0 rulings (source_quote EXCLUDED 2026-06-08; the *_basis family).
Behavior-preserving on the 3 certified anchors; the only intended deltas are
release_verify §D no longer crying wolf on zone_N records + anchoring_urls notes,
and whole_crop_gate §D no longer scanning the *_basis family. See
docs/superpowers/plans/2026-06-08-tooling-hardening.md.
"""
import re

# Exact leaf-key matches.
BACKEND_KEYS = {
    # machinery / identifier
    "id", "slug", "stage_id", "tip_id", "region_id", "evidence_tier", "added_in",
    "last_reviewed", "last_reviewed_session", "last_operation", "last_session",
    "schema_version", "last_updated", "date", "stored_date", "resolution_tier",
    "resolution_method", "anchor_threshold", "fallback_beyond_horizon",
    "calendar_state", "window_type", "timing_relative", "phase", "status", "image",
    "plantings_provenance", "provenance", "lifted_from_zone", "botanical_name",
    "family", "calendar_basis", "resolution_source", "from", "from_year_round_note",
    "url", "verified", "accessed", "publisher", "source_class", "source_note",
    "verification_log_ref", "filing_record", "disposition", "scope", "session",
    "field", "assigned_to", "deferred_to", "last_audited", "resolution_note",
    "filed_in", "filed_in_session", "resolved_in", "resolved_by",
    # own-voice reasoning + evidence prose ("show your work" layer -- backend for
    # the dash/temp gate even though SP renders; matches existing synthesis/design)
    "note_internal", "notes_internal", "synthesis_note", "synthesis_note_seasoned",
    "design_note", "design_note_seasoned", "source_quote", "source_quote_seasoned",
    "zone_coverage_note", "zone_coverage_note_seasoned", "uscrn_validation",
    "classification", "sources_summary", "description_sources", "step5_verification",
    # citation structure
    "source", "source_id", "claim", "tier", "trust_tier", "citable_for", "archetype",
    "succession_id", "track", "added_by",
}

# Subtree exclusions: a field anywhere under a path containing one of these is
# backend. Merges whole_crop_gate's BACKEND_PATH_SUBSTR + release_verify's
# BACKEND_SUBSTR. (Many overlap BACKEND_KEYS; kept here too so NESTED occurrences
# under those containers are also caught, e.g. a `note` under verification_status.)
BACKEND_PATH_SUBSTR = (
    "plantings_provenance", "verification_status", "anchoring_urls", ".provenance",
    "uscrn_validation", "_admission", "synthesis_note", "design_note",
    "source_quote", "sources_summary", "notes_internal", "calendar_basis",
    "step5_verification",
)

BACKEND_KEY_RE = re.compile(r"zone_\d+_")  # zone_8_presence, zone_10_desert_fold, ...


def _basis_family(key):
    """`basis_seasoned` and the *_basis family (heat_pause.basis, cold_pause.basis,
    ...) are backend per TOOLING_HARDENING_spec FIX 1 (Trevor-ratified 2026-06-08).
    Strip the register suffix first so `basis_seasoned`/`basis_beginner` are caught.
    Isolated here so it is a one-line revert if the ruling is ever recut."""
    stem = key
    for suf in ("_seasoned", "_beginner"):
        if stem.endswith(suf):
            stem = stem[: -len(suf)]
            break
    return stem == "basis" or stem.endswith("_basis")


def is_backend(key, path):
    """True if (key, path) names a behind-the-scenes field where verbatim text,
    `--`/em-dash, and spelled 'degrees F' are tolerated and no dash/temp scan
    applies. `path` is the dotted/bracketed location string the gates already
    build during their walk."""
    return (key in BACKEND_KEYS
            or bool(BACKEND_KEY_RE.match(key))
            or key.endswith("_sources")
            or key.endswith("_anchoring_urls")
            or _basis_family(key)
            or any(s in path for s in BACKEND_PATH_SUBSTR))


# ---- RAW-DISPLAY classification (raw_display_gate / whole_crop_gate A23, 2026-06-25) ----
# A THIRD axis, orthogonal to is_backend's backend/user-facing line. Among USER-FACING
# fields, this names the small set whose value a guide CARD prints VERBATIM -- no humanizer,
# no label map -- so the value must be HUMAN-READABLE PROSE, never a snake_case token. These
# are the fields the 2026-06-25 scan found contaminated (fertilizer.type='nitrogen_forward',
# sunlight='full_sun', companion timing='plant_with', ...). The watering pair is display-INTENT:
# not yet wired to a card, but Trevor confirmed it is meant to be human-readable, so it is gated
# as honest prose (2026-06-25).
#
# The CONTRAST -- and why this is an allowlist, not "scan every user-facing string" -- is the
# categorical TOKEN fields the renderer deliberately MAPS or humanizes, which are LEGITIMATELY
# snake_case and must NOT be flagged:
#   start_method.start        -> the isBareRoot/today.ts enum + a capitalized label
#   companions[].category     -> CompanionsCard CATEGORY_META label map
#   container shape_requirements, soil organic_matter_preference, drainage_requirement,
#   gating_factors, suitability, day_length_type, ...  -> label-mapped / replace(/_/g,' ')
# EXTEND RAW_DISPLAY_PATHS (and is_raw_display) only when a NEW card is shown to render a
# dataset string verbatim. See docs/field_inventory_raw_display_note.md.
RAW_DISPLAY_PATHS = {
    "sunlight",                  # CareGuideCard prints crop.sunlight as-is (HeroCard/app humanize)
    "fertilizer.type",           # FeedingCard feeding grid -- verbatim (the F3 "no Title Case" rule)
    "fertilizer.timing",
    "fertilizer.frequency",
    "watering.watering_method",  # display-intent prose (not yet wired); honest-prose per Trevor
    "watering.drought_tolerance",
}


def is_raw_display(key, path):
    """True if (key, path) names a user-facing field a guide card renders VERBATIM, so its
    value must be human-readable prose (no snake_case token). The inverse of the mapped/
    humanized token fields. `path` is the dotted/bracketed location the gates build during
    their walk. Used by raw_display_gate (whole_crop_gate A23)."""
    if path in RAW_DISPLAY_PATHS:
        return True
    # companions[].timing (companions.<bucket>[i].timing) -> CompanionsCard renders the
    # comp-timing div verbatim. Scoped to the companions subtree so it never collides with
    # fertilizer.timing (covered exactly above) or any future categorical `timing`.
    if key == "timing" and path.startswith("companions."):
        return True
    return False
