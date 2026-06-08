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
