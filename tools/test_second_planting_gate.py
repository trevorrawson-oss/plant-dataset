#!/usr/bin/env python3
"""second_planting_gate tests -- one synthetic fixture per defect/exempt class
(spec 2026-07-09 §6). Fixtures are self-contained; the adversarial proof on the
REAL canonical is a Task-8/12 wiring step, not a permanent test (canonical state
changes across stages)."""
from second_planting_gate import check_crop

SP = {"start_indoors": None, "plant_out": "Sep 1 - Sep 20",
      "harvest_start": "Nov 1", "harvest_end": "Nov 30",
      "sources": ["x"], "anchoring_urls": {"x": {"url": "https://e.edu", "verified": "2026-07-09"}}}


def crop(suitable, cell, slug="fixture"):
    return {"slug": slug, "succession_policy": {"suitable": suitable},
            "regions": {"r1": {"resolved_by_zone": {"8": cell}}}}


def cell(**kw):
    base = {"start_indoors": None, "plant_out": "Mar 15 - Apr 15",
            "harvest": "May 15 - Jun 30", "harvest_start": "May 15",
            "harvest_end": "Jun 30", "first_plant_date": "Mar 15",
            "last_plant_date": "Apr 15"}
    base.update(kw)
    return base


B = frozenset("B"); A = frozenset("A"); AB = frozenset("AB")

# --- Rule B fires: old comma shape, no second_planting, suitable=false
bad = crop(False, cell(plant_out="Mar 15 - Apr 15, Sep 1 - Sep 20",
                       harvest="May 15 - Jun 30, Nov 1 - Nov 30"))
assert len(check_crop(bad, B)) == 1, check_crop(bad, B)
# --- Rule B fires on a doubled start_indoors too
bad_si = crop(False, cell(start_indoors="Feb 1 - Feb 20, Jun 20 - Jul 10"))
assert len(check_crop(bad_si, B)) == 1
# --- exempt: suitable=true cadence (Decision A)
assert check_crop(crop(True, cell(plant_out="Mar 1 - May 15, Aug 1 - Sep 15")), B) == []
# --- exempt: " or " alternatives (woody herbs / or-normalized alliums)
assert check_crop(crop(False, cell(plant_out="Oct - Nov or Feb - Mar")), B) == []
# --- exempt: harvest-only doubling (reflush peppers, chives/mint)
assert check_crop(crop(False, cell(harvest="May 20 - Jun 30, Sep 10 - Dec 1")), B) == []
# --- exempt: parenthetical comma (peach)
assert check_crop(crop(False, cell(plant_out="Apr - May (dormant, bare-root)")), B) == []
# --- exempt from B: second_planting present (that is Rule A's territory)
mixed = crop(False, cell(plant_out="Mar 15 - Apr 15, Sep 1 - Sep 20",
                         second_planting=dict(SP)))
assert check_crop(mixed, B) == []

# --- Rule A fires: still-doubled top-level alongside second_planting
assert len(check_crop(mixed, A)) == 1, check_crop(mixed, A)
# --- Rule A fires: envelope still carries the fall cycle (harvest_end == sp.harvest_end)
env = crop(False, cell(second_planting=dict(SP), harvest_end="Nov 30"))
assert any("harvest_end" in v for v in check_crop(env, A)), check_crop(env, A)
# --- Rule A fires: last_plant_date sits inside the second_planting window
env2 = crop(False, cell(second_planting=dict(SP), last_plant_date="Sep 20"))
assert any("last_plant_date" in v for v in check_crop(env2, A)), check_crop(env2, A)
# --- Rule A clean: fully de-muxed cell
clean = crop(False, cell(second_planting=dict(SP)))
assert check_crop(clean, AB) == [], check_crop(clean, AB)
# --- Rule A clean: fava shared-harvest shape (spec §2 B-fava) -- the fall crop
#     overwinters into the SAME spring harvest window; containment passes it
FAVA_SP = {"start_indoors": None, "plant_out": "Aug - Sep",
           "harvest_start": "Apr", "harvest_end": "Jun",
           "sources": ["x"], "anchoring_urls": {"x": {"url": "https://e.edu", "verified": "2026-07-09"}}}
fava = crop(False, {"start_indoors": None, "plant_out": "Feb", "harvest": "Apr - Jun",
                    "harvest_start": "Apr 1", "harvest_end": "Jun 30",
                    "first_plant_date": "Feb 1", "last_plant_date": "Feb 28",
                    "second_planting": dict(FAVA_SP)})
assert check_crop(fava, AB) == [], check_crop(fava, AB)
# --- no second_planting, no multi-window: silent under both rules
assert check_crop(crop(False, cell()), AB) == []

print("second_planting_gate tests: OK")
