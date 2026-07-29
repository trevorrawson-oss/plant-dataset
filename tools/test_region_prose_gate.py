#!/usr/bin/env python3
"""Tests for the region-prose vs cell-rating coherence gate (artichoke GS arc, 2026-07-28).
Run: python3 tools/test_region_prose_gate.py

THE DEFECT (kickoff R7): region prose and per-cell ratings are two layers the same guide renders
to the same reader, and no gate compared them. After the asparagus re-rating, `ca_north_coast`'s
notes still read "both zones 9 and 10 perennialize only marginally" for two cells just promoted to
`perennializes`.

THE CHECK, after the first version was measured and narrowed: **SUIT-BOUND**. A clause binding a
ZONE OF THIS REGION to a suitability concept is an assertion about that cell and must match it.
Plus **STALE-ZONE** for the same binding on a zone outside the region's span.

The tests below carry the ten real false positives the first version produced, verbatim from the
live dataset, because they are the whole reason the check is shaped this way. See the gate header
for the measurement (38 findings roster-wide, exactly 1 a defect).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from region_prose_gate import region_prose_violations, ARCHETYPE


def crop(cells, seasoned="", beginner="", span=None, archetype=ARCHETYPE, rk="pnw"):
    return {
        "slug": "probe", "archetype": archetype,
        "regions": {rk: {
            "zone_span": span or sorted(cells, key=int),
            "resolved_by_zone": {z: {"suitability": s, "calendar": ["growing"] * 12}
                                 for z, s in cells.items()},
            "region_notes_seasoned": seasoned,
            "region_notes_beginner": beginner,
        }},
    }


# ---------------------------------------------------------------------------- scope + clean
# 0. off-archetype is a NO-OP even with a blatant contradiction. The fruit-tree prose layer has
#    never been audited against its ratings and a cert must not be blocked on other crops' copy.
assert region_prose_violations(crop(
    {"8": "perennializes", "9": "perennializes"},
    seasoned="Zone 8 and zone 9 are unsuitable.", archetype="tree_fruit")) == []

# 1. well-formed region -> clean
assert region_prose_violations(crop(
    {"8": "marginal", "9": "marginal"},
    seasoned="Zone 8 and zone 9 are both marginal: the planting does not persist.",
    beginner="Replant each year in zones 8 and 9.")) == []

# ---------------------------------------------------------------------------- SUIT-BOUND
# 2. THE ONE REAL DEFECT THIS GATE FOUND ON LIVE DATA, reproduced verbatim.
#    asparagus.ca_south_coast: prose says zone 11 is unsuitable; the cell says marginal.
v = region_prose_violations(crop(
    {"9": "perennializes", "10": "marginal", "11": "marginal"},
    seasoned=("Zone 10 is essentially frost-free, so it depends wholly on the gardener's dry-down. "
              "Frost-free zone 11 is unsuitable. Harvest from February."),
    beginner="In zone 9 it takes well."))
assert len(v) == 1, v
assert "SUIT-BOUND" in v[0] and "zone 11" in v[0] and "marginal" in v[0], v

# 3. KNOWN LIMIT, recorded rather than papered over. The ORIGINAL asparagus ca_north_coast
#    sentence -- "both zones 9 and 10 perennialize only marginally" for cells rated
#    `perennializes` -- does NOT fire, and cannot be made to without breaking the check.
#
#    The rule is any-match: a clause is clean if it names the cell's actual rating. That sentence
#    names BOTH `perennializes` and `marginal`, so it passes. Tightening to an exact-set match
#    would fire on test 6 below ("marginal to unsuitable depending on the season" on a marginal
#    cell), which is correct writing, and separating a HEDGE from a legitimate multi-rating clause
#    needs exactly the fuzzy semantics that produced 37 false positives in the first version.
#
#    So the gate catches the FLAT CONTRADICTION form ("zone 11 is unsuitable" when it is marginal,
#    which is the defect actually found on live data) and not the hedged form. Stated in the gate
#    header too. If a future pass wants the hedge, it needs a different mechanism, not a wider net.
assert region_prose_violations(crop(
    {"9": "perennializes", "10": "perennializes"},
    seasoned="Both zones 9 and 10 perennialize only marginally.",
    beginner="They just about come back.")) == []

# 3b. ...but the PLURAL still binds BOTH zones when the clause omits the actual rating, which is
#     why the zone-list regex exists. One sentence, two cells, two findings.
v = region_prose_violations(crop(
    {"9": "perennializes", "10": "perennializes"},
    seasoned="Zones 9 and 10 are unsuitable.", beginner=""))
assert len(v) == 2, v
assert all("SUIT-BOUND" in x for x in v), v

# 4. BEGINNER register is read too.
v = region_prose_violations(crop(
    {"9": "perennializes"},
    seasoned="Zone 9 keeps going for years.",
    beginner="Honestly zone 9 is unsuitable ground."))
assert any("SUIT-BOUND" in x for x in v), v

# 5. "ornamental only" maps to survives_no_fruit -- nobody writes the enum value at a reader.
v = region_prose_violations(crop(
    {"9": "marginal"}, seasoned="Zone 9 is ornamental only here.", beginner=""))
assert any("survives_no_fruit" in x for x in v), v
assert region_prose_violations(crop(
    {"10": "survives_no_fruit"},
    seasoned="Zone 10 is ornamental only; the plant grows and never buds.", beginner="")) == []

# 6. a clause may assert MORE than one rating; matching any one of them is enough.
assert region_prose_violations(crop(
    {"9": "marginal"},
    seasoned="Zone 9 is marginal to unsuitable depending on the season.", beginner="")) == []

# ---------------------------------------------------------------------------- contrastive frames
# 7. Good prose names the rating it is NOT. Both of these are live-dataset sentences that the
#    first version flagged, and both are correct writing.
assert region_prose_violations(crop(
    {"10": "unsuitable", "11": "unsuitable"},
    seasoned=("Without a dormant rest the crown cannot recharge, so a bed in zones 10 and 11 "
              "declines rather than perennializing."),
    beginner="")) == []
assert region_prose_violations(crop(
    {"10": "survives_no_fruit"},
    seasoned=("The untreated plants never bolted, which is why zone 10 is rated "
              "survives_no_fruit rather than unsuitable."),
    beginner="")) == []

# 8. ...but one negated mention must not launder a real assertion elsewhere.
v = region_prose_violations(crop(
    {"9": "perennializes"},
    seasoned="Rated perennializes rather than marginal. Zone 9 is unsuitable for a permanent bed.",
    beginner=""))
assert any("SUIT-BOUND" in x for x in v), v

# ---------------------------------------------------------------------------- THE FALSE POSITIVES
# 9. TEN VERBATIM SENTENCES FROM THE LIVE DATASET that the first version flagged and that are
#    all correct writing. Each binds its rating word to something that is NOT a zone of this
#    region: another crop, another region, a descriptive phrase, or a metaphor. If any of these
#    ever fires again, the check has regressed to keyword matching and will train people to
#    ignore it.
_FPS = [
    # a DIFFERENT CULTIVAR is the subject
    ({"9": "survives_no_fruit", "10": "survives_no_fruit"},
     "A sweet low-acid pummelo hybrid like Oro Blanco is the only citrus worth trying, and even "
     "it is marginal."),
    # a DIFFERENT REGION is the subject
    ({"9": "fruits_reliably", "10": "fruits_reliably"},
     "Lemon is one of the more cold-tender common citrus, and it is only marginal in colder parts "
     "of the Gulf South. The Valley's near-total absence of hard freezes lets it fruit reliably."),
    # a DIFFERENT REGION again, in a contrast clause
    ({"9": "marginal", "10": "marginal"},
     "Lime is the most cold-tender common citrus, unsuitable or only a container crop through "
     "most of Texas, and it is a marginal crop even in the Rio Grande Valley."),
    # a DESCRIPTIVE PHRASE about breeding
    ({"8": "survives_no_fruit"},
     "Meyer lemon, a lemon by mandarin hybrid bred for marginal climates, tolerates cold into the "
     "low-to-mid 20s degrees."),
    # a DIFFERENT CROP, with a zone number earlier in the SAME sentence but a different clause --
    # this is why clause splitting on commas is load-bearing
    ({"8": "fruits_reliably", "9": "fruits_reliably", "10": "fruits_reliably"},
     "Trifoliate rootstock is hardy through zone 8 and its early ripening escapes the hardest "
     "freezes, so mandarins fruit reliably here where a navel is only marginal."),
    # same shape, colon-separated
    ({"8": "fruits_reliably"},
     "The warm arid inland grows a reliable satsuma where a navel is only marginal: adequate "
     "summer heat, and a cold-hardiness edge that covers the zone-8 winter lows."),
    # a DIFFERENT REGION named as the favourable contrast
    ({"8": "unsuitable", "9": "survives_no_fruit", "10": "marginal"},
     "The valley floor runs colder in winter than the lower Phoenix desert (near 1,100 feet) "
     "where mandarin fruits reliably, so here it stays a protected container specimen."),
    # a METAPHOR
    ({"8": "fruits_reliably", "9": "fruits_reliably"},
     "Winter chill is never a problem, but a sheltered site and an early variety are what turn a "
     "marginal fall race into a dependable harvest."),
    # an out-of-region BOUNDARY zone, named to explain the limit -- the ZONE-SPAN false positive
    ({"3": "unsuitable", "4": "unsuitable", "5": "unsuitable", "6": "unsuitable",
      "7": "unsuitable"},
     "The newest cold-hardy satsuma hybrids extend only to about zone 8a; north of that, citrus "
     "is a container crop moved indoors for winter."),
    # differentiation by PLACE rather than by zone number -- the SPLIT-VOICE false positive.
    # This prose is BETTER than the version that would satisfy a zone-number requirement.
    ({"9": "fruits_reliably", "10": "survives_no_fruit"},
     "A strong coastal pear region inland where chill sets the variety list. Right at the "
     "fog-cooled coast, winter chill barely clears even low-chill pears, so the immediate coast "
     "is a survive-but-rarely-fruit edge."),
]
for i, (cells, text) in enumerate(_FPS):
    got = region_prose_violations(crop(cells, seasoned=text, beginner=""))
    assert got == [], f"FALSE POSITIVE #{i} regressed: {got}"

# ---------------------------------------------------------------------------- STALE-ZONE
# 10. an out-of-span zone is a defect only when a RATING is asserted for it -- the
#     stale-after-a-span-change shape, distinguished from naming a boundary zone (FP #9 above).
v = region_prose_violations(crop(
    {"3": "marginal", "4": "marginal"},
    seasoned="Zone 8 is marginal here too.", beginner="", span=["3", "4"]))
assert any("STALE-ZONE" in x and "zone 8" in x for x in v), v

# ---------------------------------------------------------------------------- robustness
# 11. malformed shapes must not crash; unauthored prose is A29's finding, not this gate's
assert region_prose_violations({"slug": "x", "archetype": ARCHETYPE}) == []
assert region_prose_violations({"slug": "x", "archetype": ARCHETYPE, "regions": {"r": None}}) == []
assert region_prose_violations(crop({"8": "marginal"}, seasoned="", beginner="")) == []
assert region_prose_violations({"slug": "x", "archetype": ARCHETYPE,
                                "regions": {"r": {"resolved_by_zone": {"8": None},
                                                  "region_notes_seasoned": "Zone 8 is marginal."}}}) == []
assert region_prose_violations({"slug": "x", "archetype": ARCHETYPE, "regions": {"r": {
    "zone_span": ["8"],
    "resolved_by_zone": {"8": {"suitability": None, "calendar": []}},
    "region_notes_seasoned": "Zone 8 is marginal here."}}}) == []

# ---------------------------------------------------------------------------- real data
# 12. Both archetype members must be CLEAN. asparagus.ca_south_coast was repaired in the same
#     session this gate found it; if this assert ever fails, either a repair regressed or a new
#     contradiction landed.
_here = os.path.dirname(os.path.abspath(__file__))
_data = json.load(open(os.path.join(_here, "..", "crops_data_final.json"), encoding="utf-8"))
_seen = 0
for _c in _data["crops"]:
    if _c.get("archetype") == ARCHETYPE:
        _seen += 1
        got = region_prose_violations(_c)
        assert got == [], f"{_c.get('slug')}: {got}"
assert _seen >= 2, f"expected asparagus AND artichoke on the archetype, saw {_seen}"

print("test_region_prose_gate: all assertions passed")
