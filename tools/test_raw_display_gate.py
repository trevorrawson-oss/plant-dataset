#!/usr/bin/env python3
"""Tests for the raw-display snake_case cert-gate branch (whole_crop_gate A23, 2026-06-25).
Run: python3 tools/test_raw_display_gate.py

WHAT IT ARMS AGAINST: the bots shipping snake_case TOKENS into user-facing fields the
guide cards render VERBATIM. The 2026-06-25 scan found 8 of 18 anchors carrying e.g.
fertilizer.type='nitrogen_forward', sunlight='full_sun', companion timing='plant_with' --
all rendered with underscores to growers (FeedingCard / CareGuideCard / CompanionsCard
print these as-is). Neither A20 (presence-only) nor release_verify (dash/degree scan)
caught it: a confirmed blind spot.

Contract (raw_display_violations):
  - Flags a RAW snake_case value (^[a-z0-9]+(_[a-z0-9]+)+$) in a RAW-DISPLAY field
    (field_classification.is_raw_display): fertilizer.{type,timing,frequency}, crop
    sunlight, watering.{watering_method,drought_tolerance}, companions[].timing.
  - NO-OP for the categorical TOKEN fields the renderer maps/humanizes -- start_method.start
    (the isBareRoot enum), companions[].category (the CATEGORY_META label map), container
    shape_requirements, soil organic_matter_preference -- those are legitimately snake_case.
  - NO-OP on absent fields (indoor crops carrying "none"/null), and on human-readable prose
    (spaces, hyphens, capitals -> not snake_case).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from raw_display_gate import raw_display_violations


def clean_crop():
    """A render-verbatim-clean anchor: every raw-display field carries human-readable prose,
    every categorical token field carries its legitimate snake_case token."""
    return {
        "slug": "carrot",
        "sunlight": "Full sun to partial shade",
        "fertilizer": {"type": "Balanced low-nitrogen", "timing": "Work compost in before sowing",
                       "frequency": "every 2 weeks"},
        "watering": {"watering_method": "Drip or base watering", "drought_tolerance": "moderate"},
        "start_method": {"start": "bare_root_dormant"},                 # categorical enum -> EXEMPT
        "soil": {"organic_matter_preference": "high_organic_matter"},   # mapped token -> EXEMPT
        "container_notes": {"shape_requirements": "wide_and_shallow_ok"},  # mapped token -> EXEMPT
        "companions": {
            "good_seasoned": [{"name": "Onions", "category": "pest_deterrent",  # mapped token -> EXEMPT
                               "timing": "Plant alongside"}],
        },
    }


# 0. the clean shape -> no violations
assert raw_display_violations(clean_crop()) == [], raw_display_violations(clean_crop())

# 1. an indoor-ish crop missing the raw-display fields -> no-op
assert raw_display_violations({"slug": "microgreens-mix"}) == [], "absent fields -> no-op"
assert raw_display_violations({"slug": "x", "fertilizer": {"type": "none needed",
                              "timing": "not applicable", "frequency": "none"}}) == [], "prose -> clean"

# 2-4. fertilizer.{type,timing,frequency} snake_case -> violation, path named
c = clean_crop(); c["fertilizer"]["type"] = "nitrogen_forward"
v = raw_display_violations(c)
assert any("fertilizer.type" in x for x in v), v

c = clean_crop(); c["fertilizer"]["timing"] = "side_dress_during_leaf_growth_then_taper_at_bulbing"
assert any("fertilizer.timing" in x for x in raw_display_violations(c)), raw_display_violations(c)

c = clean_crop(); c["fertilizer"]["frequency"] = "twice_per_year"
assert any("fertilizer.frequency" in x for x in raw_display_violations(c)), raw_display_violations(c)

# 5-6. crop sunlight: full_sun is a violation, "Full sun" is clean
c = clean_crop(); c["sunlight"] = "full_sun"
assert any(x.startswith("sunlight") for x in raw_display_violations(c)), raw_display_violations(c)
c = clean_crop(); c["sunlight"] = "Full sun"
assert raw_display_violations(c) == [], raw_display_violations(c)

# 7-8. watering display-intent fields (humanize+gate per Trevor 2026-06-25)
c = clean_crop(); c["watering"]["watering_method"] = "drip_or_base"
assert any("watering_method" in x for x in raw_display_violations(c)), raw_display_violations(c)
c = clean_crop(); c["watering"]["drought_tolerance"] = "high_once_established"
assert any("drought_tolerance" in x for x in raw_display_violations(c)), raw_display_violations(c)
# a single-word non-snake value (basil 'low') is clean
c = clean_crop(); c["watering"]["drought_tolerance"] = "low"
assert raw_display_violations(c) == [], raw_display_violations(c)

# 9. companion timing rendered verbatim -> violation
c = clean_crop(); c["companions"]["good_seasoned"][0]["timing"] = "plant_with"
assert any(x.startswith("companions.") and "timing" in x for x in raw_display_violations(c)), raw_display_violations(c)

# 10. EXEMPT: start_method.start is a categorical enum (isBareRoot) -> NOT flagged even though snake
c = clean_crop(); c["start_method"]["start"] = "grafted_nursery_tree"
assert raw_display_violations(c) == [], "start_method.start is a categorical token, not raw-display"

# 11. EXEMPT: companions[].category is the CATEGORY_META label-mapped token -> NOT flagged
c = clean_crop(); c["companions"]["good_seasoned"][0]["category"] = "trap_crop"
assert raw_display_violations(c) == [], "companion category is a mapped token, not raw-display"

# 12. EXEMPT: container shape_requirements + soil organic_matter_preference -> NOT flagged
c = clean_crop(); c["container_notes"]["shape_requirements"] = "tall_and_deep_required"
c["soil"]["organic_matter_preference"] = "low_organic_matter"
assert raw_display_violations(c) == [], "shape_requirements + organic_matter_preference are mapped tokens"

# 13. a value that is multi-word prose with a hyphen ("Nitrogen-forward") is NOT snake_case -> clean
c = clean_crop(); c["fertilizer"]["type"] = "Nitrogen-forward"
assert raw_display_violations(c) == [], raw_display_violations(c)

# 14. multiple offenders accumulate (onion shape) -> >= 3 violations
c = clean_crop()
c["fertilizer"]["type"] = "nitrogen_forward"
c["fertilizer"]["timing"] = "side_dress_periodically"
c["sunlight"] = "full_sun"
assert len(raw_display_violations(c)) >= 3, raw_display_violations(c)

# ---- incognito-redteam C12: a CAPITAL or a SPACE dodged the anchored lowercase regex ----
# The original ^[a-z0-9]+(_[a-z0-9]+)+$ missed any snake token with a capital or a leading
# space; all three of these still render an underscore to a grower.

# 15. capitalized snake_case (first letter) -> violation ("Full_sun")
c = clean_crop(); c["sunlight"] = "Full_sun"
assert any(x.startswith("sunlight") for x in raw_display_violations(c)), \
    f"C12: 'Full_sun' must be flagged: {raw_display_violations(c)}"

# 16. capitalized multi-segment snake_case -> violation ("Slow_release_granular")
c = clean_crop(); c["fertilizer"]["type"] = "Slow_release_granular"
assert any("fertilizer.type" in x for x in raw_display_violations(c)), \
    f"C12: 'Slow_release_granular' must be flagged: {raw_display_violations(c)}"

# 17. a space-bearing value whose token still shows an underscore -> violation ("full sun_partial")
c = clean_crop(); c["sunlight"] = "full sun_partial"
assert any(x.startswith("sunlight") for x in raw_display_violations(c)), \
    f"C12: 'full sun_partial' must be flagged (sun_partial renders an underscore): {raw_display_violations(c)}"

# 18. ALL-CAPS snake -> violation ("FULL_SUN")
c = clean_crop(); c["sunlight"] = "FULL_SUN"
assert any(x.startswith("sunlight") for x in raw_display_violations(c)), \
    f"C12: 'FULL_SUN' must be flagged: {raw_display_violations(c)}"

# 19. REGRESSION: a hyphenated capitalized value ("Nitrogen-forward") has no underscore -> clean
c = clean_crop(); c["fertilizer"]["type"] = "Nitrogen-forward"
assert raw_display_violations(c) == [], raw_display_violations(c)
# 20. REGRESSION: a normal capitalized prose phrase ("Full sun to partial shade") -> clean
c = clean_crop(); c["sunlight"] = "Full sun to partial shade"
assert raw_display_violations(c) == [], raw_display_violations(c)
# 21. REGRESSION: a mapped categorical token with a capital is still EXEMPT (is_raw_display gates it)
c = clean_crop(); c["start_method"]["start"] = "Grafted_nursery_tree"
assert raw_display_violations(c) == [], "start_method.start stays exempt regardless of case"

print("raw_display_gate: all tests passed")
