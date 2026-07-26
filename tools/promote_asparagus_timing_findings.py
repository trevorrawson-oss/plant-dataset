#!/usr/bin/env python3
"""Record the asparagus timing arc's honesty flags + arc-2 queue as open_findings.

Run AFTER tools/promote_asparagus_timing.py. Every window authored in that pass that is not a
direct T1 statement, every citation defect found in previously-certified data, and every
suitability contradiction deferred to arc 2 gets a finding here, so the record carries the
limitation rather than the reader having to infer it.

None of these block launch: the crop is materially better off with sourced windows plus honest
caveats than with no planting data at all.

Writes COMPACT per CLAUDE.md. Usage: python3 tools/promote_asparagus_timing_findings.py
"""
import json
import sys

CANON = "crops_data_final.json"

FINDINGS = [
    {
        "id": "asparagus_plant_out_no_zone_keyed_t1_source",
        "summary": "SOURCING LIMIT on the crown-planting windows authored 2026-07-26: NO T1 source "
                   "anywhere states an asparagus crown window by USDA zone. Every extension source "
                   "is state-, region- or county-scoped, so each per-zone window involves an "
                   "editorial state-to-zone mapping step that is ours, not the source's. This is "
                   "recorded per cell in resolution_method: extension_direct and "
                   "county_source_direct are sourced for that geography; "
                   "state_source_zone_mapped, extension_shift_rule_applied, "
                   "soil_workable_anchor_derived, extension_chart_plus_anchor and "
                   "extension_chart_geometry all carry an inference step. The northern_tier z3-z7 "
                   "ladder is the largest editorial construction: five zones built monotonically "
                   "from five different state sources (UMN/NDSU/SDSU, UMaine, Iowa State/Illinois, "
                   "UConn, Missouri).",
        "severity": "low", "blocks_launch": False, "status": "open",
    },
    {
        "id": "asparagus_plant_out_anchor_families_conflict",
        "summary": "AGRONOMIC TENSION behind the crown windows: T1 sources split into two "
                   "incompatible anchor camps roughly 4 to 6 weeks apart. The soil-workability "
                   "camp (Illinois, Missouri, UConn, Arkansas) plants crowns BEFORE last frost "
                   "('as early as the soil can be worked'); the frost-safe camp (UMaine) plants "
                   "AFTER ('after the danger of frost has passed and the soil has warmed to above "
                   "50F'), on a Fusarium-in-cold-wet-soil rationale. These cannot both be encoded "
                   "from one frost offset. Ruling 2026-07-26: soil-workability is primary (it is "
                   "the dominant camp and matches dormant-crown practice); the UMaine caution is "
                   "treated as a far-north refinement and shapes the later northern_tier z3/z4 "
                   "windows. Revisit if a crown-rot finding contradicts it.",
        "severity": "low", "blocks_launch": False, "status": "open",
    },
    {
        "id": "asparagus_warm_arid_window_is_chart_geometry",
        "summary": "LOWEST-PROVENANCE WINDOW in the 2026-07-26 pass: warm_arid z8 (Feb 1 - Feb 28) "
                   "has NO quotable supporting text and cannot have one. The NMSU Dona Ana planting "
                   "chart encodes every window as a DRAWN BAR with no text layer; the value was "
                   "recovered from PDF content-stream geometry (asparagus bar x 213.0-257.0 against "
                   "a February column of x 212.80-258.35), cross-validated against the row's "
                   "gridline gap and confirmed by rendering the page. The NMSU prose source (H-227) "
                   "independently supplies only the anchor ('plant crowns in the spring after the "
                   "soil temperature has reached 50F'), which is compatible with February in Las "
                   "Cruces but is not date confirmation. That chart is also Master-Gardener-hosted "
                   "and Las Cruces-specific rather than a peer-reviewed NMSU circular, while "
                   "warm_arid spans more than Las Cruces. Re-verify against a peer-reviewed NMSU "
                   "circular if one publishes an asparagus date.",
        "severity": "low", "blocks_launch": False, "status": "open",
    },
    {
        "id": "asparagus_mid_south_z8_no_delta_specific_window",
        "summary": "GAP accepted 2026-07-26: mid_south z8 (Delta lowlands) has NO zone-specific T1 "
                   "crown window. UADA FSA-6002 is statewide Arkansas and does not split z7 Ozarks "
                   "from z8 Delta; its zone-adjustment table footnote points to FSA-6001, whose "
                   "zone-to-county map is an IMAGE with no extractable text; and Missouri cannot "
                   "speak to z8 at all (its warmest ground is about z7, and its southern/central/ "
                   "northern split is latitude, not upland/lowland). The authored Mar 1 - Apr 15 "
                   "window is the statewide soil-workability anchor applied to the warmer Delta, "
                   "marked soil_workable_anchor_derived. MU publishes a bootheel-vs-statewide lead "
                   "for HARVEST only; using that to shift PLANTING would be a cross-field inference "
                   "and was deliberately not done.",
        "severity": "low", "blocks_launch": False, "status": "open",
    },
    {
        "id": "asparagus_citation_defects_found_in_certified_data",
        "summary": "CITATION INTEGRITY, found 2026-07-26 while authoring timing and verified by "
                   "direct extraction (not relayed): four sources cited on certified asparagus cells "
                   "do not support crown-planting timing. unr_fs0261 is 'Home Vegetable Production "
                   "in Southern Nevada' and its ONLY mention of the crop is the string 'Stems - "
                   "asparagus' in a list of edible plant parts -- REMOVED from the 3 nevada cells "
                   "and replaced with unr_sp0115. ucanr_ext is the Kings County 2005 Annual "
                   "Agricultural Crop Report (farmer's-market listings, 1956-57 rainfall tables); "
                   "its single timing sentence is about HARVEST, so it was KEPT for that and "
                   "ucanr_pub7234 added for planting. msu_ext is a real asparagus guide with no "
                   "planting date at all (its only timing sentence is about preparation the year "
                   "before) -- KEPT, with per-zone crown sources added alongside. wsu_ext is a "
                   "hortsense pest/disease page with zero planting content -- KEPT for pests, with "
                   "wsu_em051e added. All four survived the cert's 11/11 T1 source-truth sample, "
                   "which did not happen to draw them; consider weighting future samples toward "
                   "cells whose claims depend on a single source.",
        "severity": "medium", "blocks_launch": False, "status": "open",
    },
    {
        "id": "asparagus_suitability_chill_mechanism_unsourced_arc2",
        "summary": "ARC 2 QUEUE, raised 2026-07-26: the certified suitability notes justify every "
                   "marginal/unsuitable call on a CHILL requirement ('low chill', 'no sustained cold "
                   "dormant rest') cited to uc_ipm, but that source says dormancy comes from cold OR "
                   "DROUGHT ('If drought or cold weather do not stop vegetative fern growth, shoots "
                   "will become spindly'), and instructs HOME gardeners to induce it by withholding "
                   "irrigation ('Irrigation is usually stopped in September or October so that the "
                   "plants will go dormant'). Marin MG and statewide UC MG repeat it; UF/IFAS states "
                   "it independently. NO T1 source states a chill-hour requirement for asparagus "
                   "anywhere. The mechanism T1 supports is a reliable dormancy window from cold or "
                   "dry-down, plus an 85F fern-growth ceiling -- which is why Mediterranean "
                   "California works and the summer-WET Gulf does not (UF names it 'warm and wet'). "
                   "Arc 2 must repair the reasoning in these notes, not only the ratings.",
        "severity": "medium", "blocks_launch": False, "status": "open",
    },
    {
        "id": "asparagus_suitability_ratings_contested_arc2",
        "summary": "ARC 2 QUEUE, raised 2026-07-26 and deliberately NOT actioned in this pass (the "
                   "18/8/13 split is unchanged): seven certified suitability ratings are contradicted "
                   "by T1. Recommended, with confidence: ca_north_coast z9 -> perennializes (HIGH; "
                   "Marin and Sonoma MG both publish 15-year bed lifespans, county-specific variety "
                   "lists, and no warm-winter warning at all); ca_north_coast z10, ca_south_coast "
                   "z9/z10, ca_desert z9 -> perennializes (medium to med-high); se_gulf z10 -> "
                   "unsuitable (med-high; UF/IFAS omits asparagus from the Florida vegetable guide "
                   "entirely across both the statewide and South Florida editions, and Charlotte "
                   "County Extension states flatly it cannot be grown there). ALSO NOT ASKED BUT "
                   "FLAGGED: ca_desert z10 is currently `unsuitable` while being exactly the "
                   "Imperial/Coachella ground UC publishes a home-garden crown window for -- the "
                   "least defensible rating in the set; audit z11 alongside it. Rating flips cascade "
                   "into calendars (an unsuitable cell takes the all-growing honesty floor and is "
                   "A47-exempt) and into plant_out eligibility, so arc 2 is a real arc, not an edit.",
        "severity": "medium", "blocks_launch": False, "status": "open",
    },
    {
        "id": "asparagus_se_gulf_z10_no_honest_window_a47_soft",
        "summary": "THE ONE OPEN A47 CELL: se_gulf z10 is the single calendared perennial cell in "
                   "the roster without a plant_out, which is why A47 ships SOFT rather than hard. "
                   "There is no honest window to author -- asparagus occurs ZERO times in the UF/IFAS "
                   "Florida Vegetable Gardening Guide (SP103/VH021, verified across the full document "
                   "with its North/Central/South planting table present), zero times in the South "
                   "Florida planting guide, and UF's only positive stand-life claim is explicitly "
                   "scoped to north and central Florida. The correct resolution is the arc-2 re-rate "
                   "to `unsuitable`, which A47 exempts by design. HARD-FLIP A47 to fail() once that "
                   "lands and the gate reports 0.",
        "severity": "low", "blocks_launch": False, "status": "open",
    },
    {
        "id": "asparagus_days_to_maturity_empty_confirmed",
        "summary": "CONFIRMED 2026-07-26 (closing the brief's ask #4): days_to_maturity [] is "
                   "INTENTIONAL for this crop and for the establishment class generally, not an "
                   "omission. All 25 crops carrying years_to_first_harvest show [], because a "
                   "days-from-sow-to-harvest figure is meaningless for a crop whose first harvest is "
                   "measured in YEARS from a dormant crown. The establishment lag is carried instead "
                   "by years_to_first_harvest [2,3], establishment_years 5, "
                   "years_to_full_production, and productive_lifespan_years. Note establishment_years "
                   "(5, plant DEVELOPMENT, Penn State 'until the plants reach full maturity (five "
                   "years)') is deliberately distinct from years_to_first_harvest (FOOD) and the two "
                   "must never be merged or reconciled.",
        "severity": "low", "blocks_launch": False, "status": "resolved",
    },
]


def main():
    data = json.load(open(CANON, encoding="utf-8"))
    crop = next((c for c in data["crops"] if c.get("slug") == "asparagus"), None)
    if crop is None:
        print("ABORT: no asparagus crop found")
        sys.exit(1)

    vs = crop.setdefault("verification_status", {})
    ofs = vs.setdefault("open_findings", [])
    existing = {f.get("id") for f in ofs if isinstance(f, dict)}
    added = 0
    for f in FINDINGS:
        if f["id"] in existing:
            continue
        ofs.append(f)
        added += 1

    blockers = [f for f in ofs if isinstance(f, dict)
                and f.get("blocks_launch") and f.get("status") != "resolved"]
    print(f"open_findings: {len(ofs) - added} -> {len(ofs)} (+{added})")
    print(f"launch blockers: {len(blockers)} (must be 0)")

    with open(CANON, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
    print("wrote", CANON, "(COMPACT)")


if __name__ == "__main__":
    main()
