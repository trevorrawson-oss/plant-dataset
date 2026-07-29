#!/usr/bin/env python3
"""Zone-ordering sanity for harvest starts (the ca_desert z9 defect class, 2026-07-27).

THE DEFECT THIS EXISTS FOR. asparagus `ca_desert` z9 -- the COOLER desert ground -- carried
harvest "Feb - Apr" while z10, the WARMER Imperial/Coachella valley floor, carried "Mar - Apr".
The cooler zone led the warmer zone into harvest by a month, and the two crown windows did not
overlap at all. Root cause was a citation defect (UC ANR Pub 7234 carries both an October-March
CROWN window and a February-April SEED window, and the cell had been read off the seed sentence),
but the reason it SHIPPED is that nothing in the suite ever compared one zone against its
neighbour. Every gate reads a cell in isolation. This one reads the region.

THE INVARIANT. Within a single region, as the USDA zone number RISES the ground gets warmer, so
the harvest START should move EARLIER or stay equal. A cooler zone that starts first is either a
data defect or a claim that needs its own justification.

SCOPE -- archetype == 'herbaceous_perennial'. This is deliberately narrow, and the narrowing is
MEASURED rather than cautious. On canonical 9fe9e33e, with two-cycle cells already excluded:

    all crops                          51 violations / 37 crops
    perennial is True                  11 violations /  8 crops
    archetype == herbaceous_perennial   0 violations /  0 crops

The broad scopes are dominated by shapes that are CORRECT, not defective, and the reason is that
**USDA hardiness zone is a winter-minimum metric, not a spring-warmth metric**:

  - Maritime PNW: z9 is the coastal fringe -- milder winters AND cooler summers than z8, so its
    first cut legitimately lands later. `basil` pnw z8 "Jun 24 - Nov 5" vs z9 "Jul 17 - Nov 2".
  - Frost-free subtropics: in fl_peninsula and se_gulf the winter IS the growing season, and the
    warmest zone deliberately delays its fall planting until the heat breaks. `slicing-cucumber`
    fl_peninsula z10 "Oct 8 - May 31" vs z11 "Nov 8 - May 31" is right, not wrong.
  - Two-cycle cells: comparing a spring cycle's start against a winter cycle's start is
    meaningless, so comma windows are skipped outright.

Widening the scope to force those cases would be the "gate floods, so weaken the gate" trade this
suite exists to refuse. On the archetype scope the gate reports 0 for the only current member, so
it ships enforcing a convention already met -- the same soft-launch discipline as A47 and A48 --
while reproducing the shipped defect exactly on the pre-fix canonical.

HARD as of 2026-07-28, wired into whole_crop_gate as **A49**. It shipped SOFT on 2026-07-27 with
two stated conditions -- artichoke certifies, and the archetype has two members -- and both were met
when artichoke certified as GS #121 (canonical `05090b3c`). The other stated blocker, that
whole_crop_gate carried the artichoke session's uncommitted A48, ended when A48 landed as commit
`1a69e7d`. Measured 0 on both archetype members at the flip, and gate_all stayed 121/121.
Soft was a stage, not a resting state. Precedent: control_ladder_gate and variety_resistance_gate
both shipped standalone before folding into A39.

Usage: python3 tools/zone_order_gate.py [crops_data_final.json]
Exit 1 on any violation.
"""
import json
import sys

ARCHETYPE = "herbaceous_perennial"
SKIP_SUITABILITY = {"unsuitable"}

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
_IDX = {m: i + 1 for i, m in enumerate(MONTHS)}


def harvest_start_month(harvest):
    """Month number of a harvest window's start, or None if not comparable.

    Returns None for: absent/blank, two-cycle comma windows (a spring start and a winter start
    are not on the same axis), and anything whose first token is not a month name. Returning
    None is always the SAFE answer -- an uncomparable cell is skipped, never guessed at.
    """
    if not isinstance(harvest, str):
        return None
    h = harvest.strip()
    if not h or "," in h:
        return None
    return _IDX.get(h.split("-")[0].strip()[:3].title())


def zone_order_violations(crop):
    """Return a list of violation strings ([] = clean). No-op off the herbaceous_perennial archetype."""
    if not isinstance(crop, dict) or crop.get("archetype") != ARCHETYPE:
        return []
    out = []
    for rk, region in (crop.get("regions") or {}).items():
        if not isinstance(region, dict):
            continue
        zones = []
        for z, cell in (region.get("resolved_by_zone") or {}).items():
            if not isinstance(cell, dict):
                continue
            if cell.get("suitability") in SKIP_SUITABILITY:
                continue
            start = harvest_start_month(cell.get("harvest"))
            if start is None:
                continue
            try:
                zones.append((int(z), start, cell.get("harvest")))
            except (TypeError, ValueError):
                continue
        zones.sort()
        for i in range(len(zones) - 1):
            (z_cool, s_cool, h_cool), (z_warm, s_warm, h_warm) = zones[i], zones[i + 1]
            if s_cool < s_warm:
                out.append(
                    f"{rk}: zone {z_cool} (cooler) starts harvest {h_cool!r} BEFORE zone "
                    f"{z_warm} (warmer) at {h_warm!r}. Within a region the warmer zone should "
                    f"reach harvest first or at the same time; a cooler zone leading is either a "
                    f"data defect or a claim needing its own justification. This is the "
                    f"ca_desert z9 shape, which reached production because no gate compared "
                    f"neighbouring zones."
                )
    return out


def main(path):
    data = json.load(open(path, encoding="utf-8"))
    total = 0
    hit = set()
    for crop in data["crops"]:
        for v in zone_order_violations(crop):
            print(f"  {crop.get('slug')}: {v}")
            total += 1
            hit.add(crop.get("slug"))
    print(f"zone order gate: {total} violation(s) across {len(hit)} crop(s) / "
          f"{len(data['crops'])} scanned (scope: archetype == {ARCHETYPE!r})")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"))
