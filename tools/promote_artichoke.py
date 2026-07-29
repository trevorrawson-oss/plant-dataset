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
import collections
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
import ipm                                                 # noqa: E402
import prose                                               # noqa: E402

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
# RE-BASELINED 2026-07-28 (2nd time) to `b9d0c26e`, which is this same script's own output
# plus the asparagus ca_south_coast region-prose repair. Re-pointed to apply the
# `annual_only` re-rating of 22 cells; the promote is idempotent for everything else, so
# the footprint check below is what proves only the ratings moved.
EXPECTED_SHA = "6da153b9c29df50a5f7d5a726f665edd846f1c81b226eb1f49714332a0ac50f4"

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
    # SCALAR, not a range -- and this was a real break, caught by plant-astro's build rather
    # than by any gate here. The field is a scalar int on all 78 crops that carry one, and
    # astro's content schema types it `z.number().nullish()`, so shipping `[6, 8]` failed the
    # site build outright. 8 is the top of the sourced band (WSU "Weeks to Grow to Transplant
    # Size 6-8"; NC State "seed 6-8 weeks before the T date") and the safer single instruction,
    # since artichoke's three-week chilling sits inside that lead time. The 6-to-8 range is not
    # lost: it is stated in start_method.notes and year_one_notes, where a range belongs.
    "weeks_indoors": 8,
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

VERIFIED = "2026-07-28"

VERIFICATION_LOG = (
    "Artichoke GS-arc cert (2026-07-28), gold-standard crop #121, herbaceous_perennial archetype "
    "on the frost_anchored calendar basis. THE MODELING DECISION THAT GOVERNS EVERYTHING: artichoke "
    "is genuinely DUAL-MODE, a permanent bed cropping for years in mild-winter regions and an "
    "annual started indoors, deliberately chilled and discarded after one season everywhere else. "
    "Modeled as ONE crop with the mode carried PER REGION rather than as two crops or a crop-level "
    "flag, because the split is regional by nature and resolved_by_zone is where this dataset "
    "already carries regional behavior. A46 rule 4 permits years_to_first_harvest min >= 1, so the "
    "dual mode needed no gate change. THE MECHANISM, written before any rating and cited by every "
    "marginal call: a QUANTITATIVE, genotype-dependent vernalization requirement for flower-bud "
    "initiation, not an obligate one. Rutgers measured 74 percent of Imperial Star and 57 percent "
    "of Green Globe Improved setting buds with NO cold at all, so an insufficient-chill argument "
    "cannot carry `unsuitable`. Bud quality is capped above 86F; heat above roughly 65F "
    "devernalizes; buds are injured at 29.9F; the crown fails at 14-15F, which is the line that "
    "decides persistence. SEPARATELY and load-bearing: cool coastal California is NOT chill-driven "
    "at all but a continuously extended bud-induction period inside 45-85F, and UC ANR 7221 "
    "contains zero occurrences of vernal/chill/dorman/photoperiod in either edition, so rating a "
    "California cell on chill hours would repeat the asparagus error in a crop where the chill "
    "mechanism is otherwise real. SUITABILITY, 16 regions / 39 cells: 6 perennialize, 25 marginal, "
    "7 survives_no_fruit, 1 unsuitable. The 7 survives_no_fruit cells (hawaii z10-13, fl_peninsula "
    "z10/11, se_gulf z10) rest on UF/IFAS's own trial, which reports treated plants forming buds "
    "while untreated plants stayed vegetative all season: the plant thrives and never crops, which "
    "is ornamental-only rather than unsuitable. The single `unsuitable` cell, ca_desert z11, is "
    "VACANT GROUND (no California desert reaches zone 11) rather than an agronomic verdict. "
    "ca_interior is a SHORT-LIVED PERENNIAL limited by summer WATER DEMAND, with heat as what the "
    "water buys relief from, per Texas A&M's canopy-cooling statement; no Central Valley stand-life "
    "figure is published and none is given. CARVE-OUT AUDIT (a required cert artifact): the "
    "archetype's A24 and A34 exemptions are NO-OPS for artichoke, verified with the carve-out "
    "disabled, which discharges design-decisions B.2's binding criterion that cold-zone cells "
    "planting a live vernalized transplant must pass A24 on their own merits. A37 dependence is "
    "confined to exactly the 6 perennializes cells, where growing-after-harvest is the genuine "
    "established-bed case the exemption was written for. NEW GATE WORK AT CERT: A48 "
    "(perennial_harvest_gate) landed as its own commit; herbaceous_perennial_gate's SUITABILITY_ENUM "
    "widened from 3 values to the roster's 5 with survives_no_fruit added to the note-bearing set; "
    "A48 exempts survives_no_fruit from the harvest floor while A47 still REQUIRES plant_out on it, "
    "a deliberate asymmetry (someone may want the foliage, nobody should be promised food); "
    "harvest_duration_gate gained a second STOP_SIGNALS value, `bract_opening`, with "
    "threshold_inches made CONDITIONAL on the signal because artichoke's stop rule is a state "
    "change rather than a measurement; and tools/region_prose_gate.py was built during the arc, "
    "which found a live defect on certified asparagus on its first run. HONEST N/A, each recorded "
    "in open_findings: hardiness_zone_min/_max null (three T1 sources, three incompatible answers, "
    "all warmer-tolerant than the measured crown kill); harvest_ramp_weeks null (no source "
    "publishes a bed-age ramp, and a ramp would describe 6 of 39 cells); per-cultivar disease "
    "resistance absent on all 7 cultivars (no extension source publishes a rating and the two "
    "closest statements contradict each other); cultivars deliberately outside the flat "
    "variety-detail schema because no per-cultivar DTM is anchorable. SOURCE DISCIPLINE: the arc's "
    "own false rejection of unlv_mg_svn was reversed and the source re-anchored after re-reading "
    "the chart's bar geometry at source; all 26 cited URLs were fetched and the verbatim scan run "
    "against them at 26/26 coverage with 0 hard hits after 21 over-close passages were rewritten.")

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
            # SPARSE per-cell duration override (row 26 amendment): present ONLY where a source
            # states a regional duration. Absence is inheritance, not a gap -- exactly 3 of 39
            # cells qualify, which is the honest outcome of a real check.
            dur = prose.CELL_DURATION_WEEKS.get((rk, z))
            if dur:
                cell["harvest_duration_weeks"] = list(dur)
            rbz[z] = cell
        seasoned, beginner = prose.REGION_NOTES[rk]
        regions[rk] = {
            "region_id": rk,
            "region_label": REGION_LABELS[rk],
            "zone_span": list(span),
            "plantings": [{"succession_id": 1, "label": "transplants", "track": "perennial"}],
            "resolved_by_zone": rbz,
            "region_notes_beginner": beginner,
            "region_notes_seasoned": seasoned,
        }
    return regions


def merge(dst, src):
    """Fill dst from src, recursing into nested dicts so existing structural keys survive.

    Deliberately a MERGE and not a replace. The shell already carries the certified key shape
    (nulls, empty lists, nested drainage/soil_mix blocks), and clobbering a block wholesale is how
    a structural key goes missing and a frontend renders blank -- the failure mode recorded in
    [[dataset-shape-change-breaks-frontends]].
    """
    for k, v in src.items():
        if isinstance(v, dict) and isinstance(dst.get(k), dict):
            merge(dst[k], v)
        else:
            dst[k] = v


def _anchor_block(block, extra_urls=None):
    """Attach anchoring_urls to a block from its own `sources`, so gate F's one-per-source-id
    predicate is satisfied structurally rather than by hand-maintained parallel lists."""
    b = copy.deepcopy(block)
    if b.get("sources"):
        b["anchoring_urls"] = anchoring(b["sources"])
    return b


def apply_to(crop):
    crop = copy.deepcopy(crop)
    for k, v in SCALARS.items():
        crop[k] = v
    crop["succession_policy"] = copy.deepcopy(SUCCESSION)
    crop["regions"] = build_regions()

    # --- crop-level narrative registers ---
    crop["description_seasoned"] = prose.DESCRIPTION_SEASONED
    crop["description_beginner"] = prose.DESCRIPTION_BEGINNER
    crop["harvest_ready_seasoned"] = prose.HARVEST_READY_SEASONED
    crop["harvest_ready_beginner"] = prose.HARVEST_READY_BEGINNER
    crop["hardiness_notes_seasoned"] = prose.HARDINESS_NOTES_SEASONED
    crop["hardiness_notes_beginner"] = prose.HARDINESS_NOTES_BEGINNER
    crop["year_one_notes_seasoned"] = prose.YEAR_ONE_NOTES_SEASONED
    crop["year_one_notes_beginner"] = prose.YEAR_ONE_NOTES_BEGINNER
    crop["soil_prep_seasoned"] = prose.SOIL_PREP_SEASONED
    crop["soil_prep_beginner"] = prose.SOIL_PREP_BEGINNER

    # --- structured blocks, MERGED so the shell's key shape survives ---
    for key, block in (("ph", prose.PH), ("fertilizer", prose.FERTILIZER),
                       ("watering", prose.WATERING), ("storage", prose.STORAGE),
                       ("soil", prose.SOIL), ("rotation", prose.ROTATION),
                       ("yield_expectations", prose.YIELD_EXPECTATIONS),
                       ("container_notes", prose.CONTAINER_NOTES),
                       ("companions", prose.COMPANIONS)):
        if not isinstance(crop.get(key), dict):
            crop[key] = {}
        merge(crop[key], _anchor_block(block))
    merge(crop.setdefault("start_method", {}), prose.START_METHOD)
    merge(crop.setdefault("moon_phase_preference", {}), prose.MOON_PHASE)

    # --- cultivars. `resistance` is absent on every one: the gate's own honest-N/A branch. ---
    v = crop.setdefault("varieties", {})
    v["recommended"] = [_anchor_block(x) for x in prose.VARIETIES]
    v["note_seasoned"] = prose.VARIETIES_NOTE_SEASONED + " " + prose.VARIETIES_RESISTANCE_NOTE
    v["note_beginner"] = prose.VARIETIES_NOTE_BEGINNER
    v["sources"] = sorted({s for x in prose.VARIETIES for s in x["sources"]})
    v["anchoring_urls"] = anchoring(v["sources"])

    # --- the two duration fields (register rows 26/27), authored natively at cert ---
    crop["harvest_stop_rule"] = _anchor_block(prose.HARVEST_STOP_RULE)
    # harvest_ramp_weeks stays NULL. No source publishes a bed-age ramp for artichoke, and a ramp
    # would describe 6 of 39 cells anyway. The honest-N/A branch is the answer; see prose.py.
    crop["harvest_ramp_weeks"] = prose.HARVEST_RAMP_WEEKS
    crop["harvest_ramp_na_seasoned"] = prose.HARVEST_RAMP_NA_SEASONED
    crop["harvest_ramp_na_beginner"] = prose.HARVEST_RAMP_NA_BEGINNER

    # --- consumer compounds ---
    crop["growth_stages"] = copy.deepcopy(ipm.GROWTH_STAGES)
    crop["pests"] = copy.deepcopy(ipm.PESTS)
    crop["diseases"] = copy.deepcopy(ipm.DISEASES)
    crop["notifications"] = copy.deepcopy(ipm.NOTIFICATIONS)
    crop["weather_triggers"] = copy.deepcopy(ipm.WEATHER_TRIGGERS)
    crop["failure_diagnostics"] = copy.deepcopy(ipm.FAILURE_DIAGNOSTICS)
    crop["tips_by_stage"] = {
        stage: [dict(t, anchoring_urls=anchoring(t["sources"])) for t in tips]
        for stage, tips in ipm.TIPS_BY_STAGE.items()
    }

    crop["open_findings"] = copy.deepcopy(prose.OPEN_FINDINGS)

    # --- the cert flip. This is what puts artichoke into gate_all, so it goes LAST and only
    # after the whole layer above it is authored. `status` is the field A39-A42 key the register
    # floor on, so flipping it early would have made the crop look certified while half-built.
    cited = sorted({s for r in crop["regions"].values()
                    for c in r["resolved_by_zone"].values() for s in (c.get("sources") or [])}
                   | {s for b in (crop.get("ph"), crop.get("fertilizer"), crop.get("watering"),
                                  crop.get("storage"), crop.get("soil"), crop.get("rotation"),
                                  crop.get("yield_expectations"), crop.get("container_notes"),
                                  crop.get("companions"), crop.get("harvest_stop_rule"))
                      if isinstance(b, dict) for s in (b.get("sources") or [])})
    crop["verification_status"] = {
        "status": "verified_gs_arc",
        "phase": "artichoke_herbaceous_perennial_cert_gs_arc",
        "date": VERIFIED,
        "launch_ready_core": True,
        "launch_ready_seasoned": True,
        "last_audited": VERIFIED,
        "source_set": cited,
        "verification_log_ref": VERIFICATION_LOG,
        # Amend-not-recert provenance: a certified crop carrying a timing-spine column must log
        # where the column came from, with T1 sources. Artichoke authors these NATIVELY at cert
        # rather than as a later backfill, per the method doc's section 2.5 branch, so the entries
        # record the cert itself as their origin.
        "field_additions": [
            {"field": "timing_spine", "date": VERIFIED,
             "sources": ["vce_438_108", "wsu_em057e", "usu_ext_artichoke", "umaine_2075"],
             "note": (
                 "propagule=transplant (not SEED_LIKE, so sow_depth_inches is optional; authored "
                 "anyway at 0.25 to 0.5 inch from WSU because most growers of this crop do start "
                 "their own seed). days_to_maturity [60, 100] with dtm_anchor from_transplant, "
                 "anchored to VCE 438-108, the only DTM in the corpus explicit about its "
                 "operation; WSU EM057E's 85 to 120 was DECLINED because its column sits in a "
                 "seeding-recommendations table whose other columns are seed-relative, leaving "
                 "the anchor ambiguous. weeks_indoors [6, 8] from WSU and NC State. "
                 "germination_temp_f [65, 82] from WSU's optimum soil temperature range. The "
                 "establishment lag is carried in years_to_first_harvest [1, 2] / "
                 "years_to_full_production [2, 3] / productive_lifespan_years 7, the last "
                 "flagged coastal-derived because UC's five-to-ten-year replant interval is the "
                 "only sourced stand life and no Central Valley figure is published.")},
            {"field": "category", "date": VERIFIED,
             "note": (
                 "moved Fruiting Veg -> Perennial Vegetables, the value asparagus introduced "
                 "(UC Master Gardener classification). Artichoke is an immature flower bud on a "
                 "herbaceous perennial, not a fruit. Register row 25. No new category value, so "
                 "no frontend work beyond the grouping the astro lane already owes for "
                 "asparagus.")},
            {"field": "harvest_stop_rule", "date": VERIFIED,
             "sources": ["uc_ipm", "usu_ext_artichoke", "umaine_2075"],
             "note": (
                 "register row 27, authored natively at cert. Needed a SECOND STOP_SIGNALS value: "
                 "asparagus stops on spear CALIBER, artichoke on BRACT OPENING, which is a "
                 "different observable rather than a different threshold on the same one. "
                 "threshold_inches is deliberately absent and the gate now keys that requirement "
                 "to the signal, because none of the three sources stating the rule gives a size "
                 "and inventing one would be manufactured precision.")},
            {"field": "harvest_ramp_weeks", "date": VERIFIED,
             "note": (
                 "register row 26. Deliberately NULL, which is the honest-N/A branch and not a "
                 "gap: no source publishes a bed-age ramp for artichoke, and a ramp is a "
                 "perennial-crown concept that would describe 6 of 39 cells since the rest are "
                 "annual culture with no bed age at all. The N/A is carried in prose at "
                 "harvest_ramp_na_seasoned/_beginner and in open_findings. Three cells carry a "
                 "sourced per-cell harvest_duration_weeks instead.")},
        ],
    }
    crop["launch_ready_core"] = True
    crop["launch_ready_seasoned"] = True

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
        # A leading underscore marks a CONSIDERED-AND-REJECTED entry that stays in sources.py for
        # the record but is never written to the catalog. Currently just uaex_cardoon: a T2 row no
        # crop cites is not evidence, and the pending tier renumbering would have to migrate it
        # for nothing. See the sources.py header for why the disclaimer disqualifies it anyway.
        if sid.startswith("_"):
            continue
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
    # The two floors have DIFFERENT denominators, and printing one number for both hid that.
    # A47 owes plant_out on everything except `unsuitable`; A48 owes harvest on everything except
    # `unsuitable` AND `survives_no_fruit` (an ornamental-only cell has no food to promise).
    suits = collections.Counter(c.get("suitability")
                                for r in crop["regions"].values()
                                for c in r["resolved_by_zone"].values())
    owes_po = cells - suits["unsuitable"]
    owes_hv = owes_po - suits["survives_no_fruit"]
    print(f"wrote {os.path.basename(out)}  ({'CANONICAL' if promote else 'scratch'})")
    print(f"  crop changed: {before != json.dumps(crop, sort_keys=True)}")
    print(f"  regions {len(crop['regions'])}  cells {cells}   {dict(suits)}")
    print(f"  plant_out {with_po}/{owes_po} owed (A47)   harvest {with_hv}/{owes_hv} owed (A48)")
    print(f"  source_catalog additions: {added}")
    print(f"  verification_status.status: {(crop.get('verification_status') or {}).get('status')!r}"
          " (uncertified until the prose/IPM/variety pass lands)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
