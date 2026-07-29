#!/usr/bin/env python3
"""Artichoke GS arc promote -- SHA-GUARDED, SCRATCH BY DEFAULT.

Refuses to run if the canonical has drifted from the SHA this arc was authored against, and
writes to a scratch copy unless --promote is passed explicitly. Canonical JSON is COMPACT
(separators=(",",":"), ensure_ascii=False, no trailing newline) and that is preserved byte-exactly.

  python3 tools/promote_artichoke.py              # -> crops_data_final.scratch.json
  python3 tools/promote_artichoke.py --promote    # -> crops_data_final.json  (Trevor-approved only)

WHAT IT APPLIES
  1. the 16-region / 39-cell roster from staging/artichoke/cells.py, at the CERTIFIED cell shape
     (shell-only scaffolding keys are dropped -- zone_8_presence, zone_10_desert_fold,
     sources_pending_admission, and the per-cell suitability_reason_* which the certified schema
     calls suitability_note_*)
  2. the source_catalog additions from staging/artichoke/sources.py
  3. the settled scalar + register fields from design-decisions B.7

WHAT IT DOES NOT DO YET: the consumer prose (descriptions, hardiness/harvest-ready/soil-prep/
year_one registers), the IPM ladders, the cultivars, growth_stages/tasks/notifications. Those are
authored next; until they land the crop stays UNCERTIFIED (verification_status.status is left
null), which is the honest admission state and keeps it out of gate_all.
"""
import copy
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "staging", "artichoke"))
sys.path.insert(0, HERE)

from cells import CELLS                                    # noqa: E402
from sources import CATALOG_ADDITIONS, SOURCE_URLS, anchoring  # noqa: E402

PATH = os.path.join(HERE, "..", "crops_data_final.json")
SCRATCH = os.path.join(HERE, "..", "crops_data_final.scratch.json")

# The canonical this arc was authored against. Guard, per kickoff section 6: abort on drift rather
# than splice authored content onto a base that has moved underneath it.
#
# RE-BASELINED 2026-07-28, deliberately, per handoff 43 section 1. The arc paused against
# `34025ee3` and the guard then FIRED and refused to promote -- correctly -- while a concurrent
# asparagus session moved the canonical through seven releases (34025ee3 -> 79862bc3 -> 0da1d234
# -> 9fe9e33e -> 02fbb5e8 -> a995333f -> 27f14303 -> ea3636e7). That session has landed, its state
# trio is coherent, and none of its commits touched artichoke, source_catalog, or any shared
# catalog. Re-pointed only after re-verifying the new base:
#   shasum -a 256 crops_data_final.json == LATEST.txt, git tree clean, gate_all 120/120.
EXPECTED_SHA = "ea3636e72e70a397d55512e800f115173a13ab833b9a523db1d275cc0b80024b"

REGION_LABELS = {
    "northern_tier": "Northern Tier (Cold Zones)",
    "warm_arid": "Warm Arid (Inland Southwest)",
    "utah_dixie": "Utah: St. George Dixie (Mojave-edge high desert)",
    "mid_atlantic": "Mid-Atlantic: Piedmont and Coastal Plain",
    "mid_south": "Mid-South: Ozark Uplands and Delta Lowlands",
    "pnw": "Maritime Pacific Northwest: Puget Sound and Willamette Valley",
    "ca_interior": "California: Interior Valleys",
    "nevada": "Nevada: Mojave High Desert (Las Vegas Valley)",
    "se_gulf": "Southeast / Gulf",
    "ca_north_coast": "California: North & North Coast",
    "ca_south_coast": "California: South Coast",
    "ca_desert": "California: Desert Valleys",
    "low_desert_az": "Arizona: Low Desert",
    "rgv": "Rio Grande Valley: Subtropical South Texas",
    "fl_peninsula": "Florida Peninsula",
    "hawaii_tropical": "Hawaii / Tropical",
}

# Shell scaffolding that the certified shape does not carry (asparagus carries none of it).
DROP_REGION_KEYS = {"zone_8_presence", "zone_10_desert_fold", "sources_pending_admission"}

SCALARS = {
    # --- archetype + classification (design-decisions B.1, B.2, B.5) ---
    "archetype": "herbaceous_perennial",
    "calendar_basis": "frost_anchored",
    "category": "Perennial Vegetables",
    "lifecycle": "perennial",
    "perennial": True,
    "difficulty": "medium",
    # --- B.3: days_to_maturity is NOT [] -- artichoke is an annual across most of this roster ---
    "days_to_maturity": [60, 100],
    "days_to_maturity_mid": 80,
    "dtm_anchor": "from_transplant",
    # --- A46 establishment fields ---
    "years_to_first_harvest": [1, 2],
    "years_to_full_production": [2, 3],
    "establishment_years": 2,
    "productive_lifespan_years": 7,
    # --- B.4 propagule + the register floor ---
    "propagule": "transplant",
    "sow_depth_inches": [0.25, 0.5],
    "planting_layout": "row",
    "divide_every_years": 4,
    # --- climate thresholds (B.7) ---
    # 86F is a BUD-QUALITY ceiling, not a survival ceiling -- UC ANR 7221: "Plants are tolerant of
    # temperatures above 86F ... but the quality of the edible flower bud is reduced". Three
    # independent T1 sources agree on the number, and `quality_loss` is the effect they describe.
    "heat_threshold_f": 86,
    "heat_effect": "quality_loss",
    # 25F is TAMU EHT-065's explicit winter floor ("Do not expose artichokes to temperatures below
    # 25 degrees F"). The effect is `foliage_damaged`, NOT `killed`: the crown survives well below
    # it and only fails around 15F (OSU). No T1 source states a foliage-specific temperature, so
    # this is the whole-plant management threshold used at its honest effect level.
    "frost_tolerance_f": 25,
    "frost_effect": "foliage_damaged",
    "chilling_sensitivity_f": None,
    # --- germination / seedling: artichoke HAS a real home-from-seed path, unlike asparagus ---
    "germination_temp_f": [65, 82],
    "weeks_indoors": [6, 8],
    "germination_light": "neutral",
    "seedling_light": "bright_default",
    "tray_sowing": "cell_tray",
    # --- horticulture ---
    "spacing_inches": [18, 36],
    "sunlight": "Full sun",
    "sunlight_hours": [6, 8],
    "water": "Regular",
    "harvest_urgency": "high",
    # --- B.7: contested across three T1 sources -> deliberately null, reason in open_findings ---
    "hardiness_zone_min": None,
    "hardiness_zone_max": None,
}

SUCCESSION = {
    "suitable": False,
    "reason_seasoned": (
        "Artichoke is not succession-planted. Where it perennializes you establish the bed once "
        "and crop the same crowns for five to ten years; where it is grown as an annual there is "
        "exactly one cycle per season, because the plant needs a cool spell to set buds and a "
        "second sowing would miss it."),
}


def sha_of(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def build_regions():
    """Build the 16-region / 39-cell block at the certified shape."""
    from zone_span_gate import EXPECTED_SPANS
    regions = {}
    for rk, span in EXPECTED_SPANS.items():
        authored = CELLS.get(rk) or {}
        assert sorted(authored, key=int) == sorted(span, key=int), (
            f"{rk}: authored zones {sorted(authored, key=int)} != expected span {span}")
        rbz = {}
        for z in span:
            c = authored[z]
            cell = {
                "suitability": c["suitability"],
                "calendar": list(c["calendar"]),
                "resolution_method": c["resolution_method"],
                "sources": list(c["sources"] or []),
                "anchoring_urls": anchoring(c["sources"] or []),
            }
            if c.get("notes"):
                cell["notes"] = c["notes"]
            if c.get("start_indoors"):
                cell["start_indoors"] = c["start_indoors"]
            if c.get("plant_out"):
                cell["plant_out"] = c["plant_out"]
            if c.get("harvest"):
                cell["harvest"] = c["harvest"]
            if c.get("suitability_note_seasoned"):
                cell["suitability_note_seasoned"] = c["suitability_note_seasoned"]
            if c.get("suitability_note_beginner"):
                cell["suitability_note_beginner"] = c["suitability_note_beginner"]
            rbz[z] = cell
        regions[rk] = {
            "region_id": rk,
            "region_label": REGION_LABELS[rk],
            "zone_span": list(span),
            "plantings": [{"succession_id": 1, "label": "transplants", "track": "perennial"}],
            "resolved_by_zone": rbz,
            "region_notes_beginner": None,   # authored in the prose pass
            "region_notes_seasoned": None,
        }
    return regions


def apply_to(crop):
    crop = copy.deepcopy(crop)
    for k, v in SCALARS.items():
        crop[k] = v
    crop["succession_policy"] = copy.deepcopy(SUCCESSION)
    crop["regions"] = build_regions()
    for k in list(crop.keys()):
        if k in DROP_REGION_KEYS:
            del crop[k]
    return crop


def main():
    promote = "--promote" in sys.argv
    got = sha_of(PATH)
    if got != EXPECTED_SHA:
        print("ABORT: canonical has drifted from the SHA this arc was authored against.")
        print(f"  expected {EXPECTED_SHA}")
        print(f"  got      {got}")
        print("  Re-verify the arc against the new base before promoting.")
        return 1

    data = json.load(open(PATH, encoding="utf-8"))
    idx = next(i for i, c in enumerate(data["crops"]) if c.get("slug") == "artichoke")
    before = json.dumps(data["crops"][idx], sort_keys=True)
    data["crops"][idx] = apply_to(data["crops"][idx])

    added = 0
    for sid, entry in CATALOG_ADDITIONS.items():
        if sid not in data["source_catalog"]:
            data["source_catalog"][sid] = copy.deepcopy(entry)
            added += 1

    out = PATH if promote else SCRATCH
    txt = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(txt)          # COMPACT, no trailing newline

    crop = data["crops"][idx]
    cells = sum(len(r["resolved_by_zone"]) for r in crop["regions"].values())
    with_po = sum(1 for r in crop["regions"].values() for c in r["resolved_by_zone"].values()
                  if c.get("plant_out"))
    with_hv = sum(1 for r in crop["regions"].values() for c in r["resolved_by_zone"].values()
                  if c.get("harvest"))
    unsuit = sum(1 for r in crop["regions"].values() for c in r["resolved_by_zone"].values()
                 if c.get("suitability") == "unsuitable")
    print(f"wrote {os.path.basename(out)}  ({'CANONICAL' if promote else 'scratch'})")
    print(f"  crop changed: {before != json.dumps(crop, sort_keys=True)}")
    print(f"  regions {len(crop['regions'])}  cells {cells}  unsuitable {unsuit}")
    print(f"  plant_out {with_po}/{cells - unsuit} non-unsuitable   harvest {with_hv}/{cells - unsuit}")
    print(f"  source_catalog additions: {added}")
    print(f"  verification_status.status: {(crop.get('verification_status') or {}).get('status')!r}"
          " (uncertified until the prose/IPM/variety pass lands)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
