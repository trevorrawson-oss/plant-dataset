#!/usr/bin/env python3
"""build_onion_daylength_patch.py -- corrects the onion + shallot day-length recommendation
for the two SE temperate belts (mid_south, mid_atlantic) from long_day to intermediate_day at
the latitudes where long-day onions do not bulb (<=~36°N), and trims the spring planting
window to end by late March (intermediate-day onions must be set early to size up before their
day-length trigger -- the A9 photoperiod window-fit rule forbids an April plant_out for
intermediate_day).

Scope (Trevor-approved Path A, 2026-07-21):
  * onion   mid_south   z7 + z8  long_day -> intermediate_day  (both zones ~34-37°N)
  * onion   mid_atlantic     z8  long_day -> intermediate_day  (z7 stays long_day: Piedmont to ~40°N)
  * shallot mid_south   z7 + z8  long_day -> intermediate_day  (rides onion, same species)
  * shallot mid_atlantic     z8  long_day -> intermediate_day  (z7 stays long_day)

Per flipped resolved cell: recommended_day_length_type, day_length_note_{beginner,seasoned},
plant_out + last_plant_date (April tail trimmed to late March), calendar[3] Apr plant->growing,
zone_notes (embedded dates + day-length wording). Per region: region_notes_{beginner,seasoned}
re-led to intermediate, and the region cell `sources` gains the onion day-length authority
(new source_catalog entries uada_ext_fsa6014 / ncsu_ext_bulb_onions).

The region-level plantings[] offset/window is LEFT UNCHANGED: it is the general provenance and,
for mid_atlantic, is shared with the still-long_day z7; the resolved cells are authoritative
(mid_south memory: a naive re-resolve is round-trip-wrong). Harvest is day-length-anchored and
unchanged. From-guards are read from the live canonical so they cannot drift.

Sourcing rationale + the split (OSU/TN/NC end-by-mid-March vs AR/VCE into-April) is documented in
docs/reviews/notes/2026-07-21/onion_daylength_intermediate_decision.md.

Usage: python3 tools/build_onion_daylength_patch.py   # writes tools/batches/onion_daylength_intermediate.json
"""
import json, hashlib, sys, os  # noqa

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import apply_patch as ap

CANON = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "crops_data_final.json")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "batches", "onion_daylength_intermediate.json")

# ---------------------------------------------------------------- authored content

# per-zone day_length notes, keyed (slug, region, zone)
DL_BEGINNER = {
 ("onion", "mid_south", "7"):
   "Grow intermediate-day onions here. They form a bulb at a middle day length, about 12 to 14 "
   "hours, which fits this latitude, and they size up best when set out early, so plant from "
   "February into late March. Long-day onions also work at the belt's cooler northern edge. Skip "
   "short-day (Southern) onions, which are bred for fall planting in much milder winters.",
 ("onion", "mid_south", "8"):
   "Grow intermediate-day onions here. They form a bulb at a middle day length, about 12 to 14 "
   "hours, a good match for this latitude, and they size up best when set early, so plant from "
   "February into late March. Short-day (Southern) onions such as Texas 1015Y also do well in the "
   "warm lowland south. Skip long-day (Northern) onions, which need days longer than this belt's "
   "summer reaches and stay small here.",
 ("onion", "mid_atlantic", "8"):
   "Grow intermediate-day onions here. They form a bulb at a middle day length, about 12 to 14 "
   "hours, a good match for the Coastal Plain, and they size up best when set early, so plant from "
   "late February into late March. Short-day (Southern) onions such as Granex also do well in the "
   "warmer, southern coastal counties. Skip long-day (Northern) onions, which need longer days "
   "than this belt's summer provides and stay small here.",
 ("shallot", "mid_south", "7"):
   "Go with intermediate-day shallots, or any reliable set type. Shallots are the same species as "
   "onion and respond to day length the same way, so at this latitude intermediate types divide "
   "and size up well when set early, from February into late March. Long-day set types also work "
   "at the belt's cooler northern edge.",
 ("shallot", "mid_south", "8"):
   "Intermediate-day shallots, or any reliable set type, work well here. Shallots respond to day "
   "length like onions, dividing into a clump at a middle day length, and they size up best when "
   "set early, from February into late March. Short-day set types also do well in the warm "
   "lowland south.",
 ("shallot", "mid_atlantic", "8"):
   "Intermediate-day shallots, or any reliable set type, work well here. Shallots respond to day "
   "length like onions, dividing into a clump at a middle day length, and they size up best when "
   "set early, from late February into late March. Short-day set types also do well in the "
   "warmer, southern coastal counties.",
}

DL_SEASONED = {
 ("onion", "mid_south", "7"):
   "This latitude (roughly 36 to 37°N in the Ozark uplands and the belt's north) is "
   "intermediate-day onion country: intermediate types bulb at 12 to 14 hours of daylight, the "
   "belt's early-summer day length, and they build the most size when set out early, so aim for "
   "February into late March rather than April. Long-day types remain a reasonable choice at the "
   "belt's cooler northern edge in southern Missouri. Avoid true short-day (Southern) types, "
   "which are bred for a fall planting and a mild winter this belt does not reliably provide. "
   "University of Arkansas guidance lists intermediate-day onions as suited to the northern half "
   "of the state, and Tennessee and Oklahoma Extension both recommend intermediate-day for dry "
   "bulbs.",
 ("onion", "mid_south", "8"):
   "This belt (roughly 34 to 35°N in the Delta lowlands) sits in intermediate-day onion "
   "country, below the 36°N line where growers switch off long-day types. Intermediate-day "
   "onions bulb at 12 to 14 hours of daylight and build the most size when set out early, so aim "
   "for February into late March. Short-day (Southern) types such as Texas 1015Y and Granex also "
   "succeed in the warm south of the belt. Avoid long-day (Northern) types: at this latitude the "
   "longest summer day only reaches about 14 hours, so a long-day onion triggers too late and too "
   "briefly to size up. University of Arkansas guidance lists short-day onions as adapted "
   "statewide, with the intermediate-day Candy the widely adaptable standard.",
 ("onion", "mid_atlantic", "8"):
   "The Coastal Plain (roughly 34 to 36°N) sits at or below the 36°N line where growers move "
   "off long-day onions. Intermediate-day types bulb at 12 to 14 hours of daylight and size up "
   "best when set out early, so aim for late February into late March. In the southern Coastal "
   "Plain of eastern North Carolina, true short-day types such as Granex and Texas Grano are the "
   "traditional choice: NC State recommends short-day onions for eastern North Carolina and calls "
   "long-day onions not recommended there. Avoid long-day (Northern) types in the Coastal Plain, "
   "where they trigger too late and too briefly to make a good bulb.",
 ("shallot", "mid_south", "7"):
   "Shallots share onion's photoperiod response, both being Allium cepa, so this latitude (roughly "
   "36 to 37°N) calls for intermediate-day shallots or any reliable traditional set type, "
   "dividing at 12 to 14 hours of daylight and sizing best when set out early, February into late "
   "March. Long-day set types remain reasonable at the cooler northern edge. Extension services "
   "publish onion day-length maps but not a separate shallot one, so this follows onion, the "
   "closest documented allium.",
 ("shallot", "mid_south", "8"):
   "Shallots share onion's photoperiod response, both being Allium cepa, so the Delta lowlands "
   "(roughly 34 to 35°N) sit in intermediate-day territory, below the 36°N long-day line. "
   "Intermediate-day shallots and traditional set types divide well at 12 to 14 hours of daylight "
   "and size best when set out early, February into late March; short-day set types also succeed "
   "in the warm south. This follows the onion day-length map, since extension services do not "
   "publish a separate one for shallot.",
 ("shallot", "mid_atlantic", "8"):
   "Shallots share onion's photoperiod response, both being Allium cepa, so the Coastal Plain "
   "(roughly 34 to 36°N) sits at or below the 36°N long-day line. Intermediate-day shallots "
   "and set types divide well at 12 to 14 hours of daylight and size best when set out early, late "
   "February into late March; in the southern Coastal Plain short-day set types are the "
   "traditional choice. This follows onion's day-length map, since extension services do not "
   "publish a separate one for shallot.",
}

# trimmed plant window per zone: (plant_out, last_plant_date). Start unchanged; April tail dropped.
WINDOW = {
 ("onion", "mid_south", "7"): ("Feb 24 - Mar 31", "Mar 31"),
 ("onion", "mid_south", "8"): ("Feb 15 - Mar 25", "Mar 25"),
 ("onion", "mid_atlantic", "8"): ("Feb 20 - Mar 31", "Mar 31"),
 ("shallot", "mid_south", "7"): ("Feb 24 - Mar 31", "Mar 31"),
 ("shallot", "mid_south", "8"): ("Feb 15 - Mar 25", "Mar 25"),
 ("shallot", "mid_atlantic", "8"): ("Feb 20 - Mar 31", "Mar 31"),
}

ZONE_NOTES = {
 ("onion", "mid_south", "7"):
   "Ozark uplands: set onion sets or seedlings Feb 24 to Mar 31 as soon as the ground can be "
   "worked, setting them early so intermediate-day bulbs build size before the day-length trigger. "
   "Bulbs size up and pull late June into late July. This latitude (roughly 36 to 37°N) is "
   "intermediate-day onion territory, with long-day types a reasonable choice at the belt's cooler "
   "northern edge.",
 ("onion", "mid_south", "8"):
   "Delta Lowlands and Ozark Uplands warm edge: set onion sets or seedlings Feb 15 to Mar 25 as "
   "soon as the soil is workable, well ahead of the last frost since onion tolerates cold, and set "
   "them early so intermediate-day bulbs build size before the day-length trigger. Bulbs size up "
   "through early summer and pull late June into late July. This is intermediate-day territory "
   "below the 36°N line, and short-day (Southern) types also do well in the warm lowland south.",
 ("onion", "mid_atlantic", "8"):
   "Coastal Plain and Piedmont warm edge: set onion sets or seedlings Feb 20 to Mar 31 as soon as "
   "the soil is workable, well ahead of the last frost since onion tolerates cold, and set them "
   "early so intermediate-day bulbs build size before the day-length trigger. Bulbs size up "
   "through early summer and pull late June into late July. This is intermediate-day territory at "
   "or below the 36°N line, and true short-day types are the traditional choice in the southern "
   "Coastal Plain.",
 ("shallot", "mid_south", "7"):
   "Ozark uplands: push sets into workable soil Feb 24 to Mar 31, pointy end up, as soon as the "
   "ground can be worked, setting them early so intermediate-day clumps build size before the "
   "day-length trigger. Clumps divide and size up through early summer, dug late June into late "
   "July.",
 ("shallot", "mid_south", "8"):
   "Delta Lowlands and Ozark Uplands warm edge: push sets into workable soil Feb 15 to Mar 25, "
   "pointy end up, setting them early so intermediate-day clumps build size before the day-length "
   "trigger. Each set divides into a clump of several shallots, dug late June into late July once "
   "most tops fall over.",
 ("shallot", "mid_atlantic", "8"):
   "Coastal Plain and Piedmont warm edge: push sets into workable soil Feb 20 to Mar 31, pointy "
   "end up, setting them early so intermediate-day clumps build size before the day-length "
   "trigger. Each set divides into a clump of several shallots, dug late June into late July once "
   "most tops fall over.",
}

# region-level region_notes, keyed (slug, region)
REGION_BEGINNER = {
 ("onion", "mid_south"):
   "In the Ozark Uplands and Delta Lowlands, onions are a one-time spring crop. Grow "
   "intermediate-day onions, which bulb at this belt's day length; set them out early, from "
   "February into late March, so they build size before the day-length trigger. Short-day "
   "(Southern) types also do well in the warm lowland south, and long-day types work at the cooler "
   "northern edge. Set sets or seedlings out as soon as the ground can be worked; onions shrug off "
   "a light frost. They are ready mid-to-late summer when about half the tops flop over and dry. "
   "Pull them, then let them cure in a warm, airy spot for two to four weeks before storing.",
 ("onion", "mid_atlantic"):
   "In the Piedmont and Coastal Plain, onions are a one-time spring crop. In the warmer Coastal "
   "Plain (zone 8) grow intermediate-day onions, set out early from late February into late March "
   "so they build size before the day-length trigger; true short-day (Southern) types are the "
   "traditional choice in the southern Coastal Plain. The cooler Piedmont (zone 7) is long-day "
   "onion country. Set sets or seedlings out as soon as the ground can be worked; onions shrug off "
   "a light frost. They are ready mid-to-late summer when about half the tops flop over and dry. "
   "Pull them, then cure in a warm, airy spot for two to four weeks before storing.",
 ("shallot", "mid_south"):
   "In the Ozark Uplands and Delta Lowlands, shallots are a one-time spring crop grown from sets. "
   "There is no local planting guide specific to shallot, so this follows onion, a very close "
   "relative: push sets into workable soil early, from February into late March, pointy end up, 6 "
   "to 8 inches apart. Grow intermediate-day types for this latitude. Each set splits into a clump "
   "you dig in early-to-mid summer once the tops flop over.",
 ("shallot", "mid_atlantic"):
   "In the Piedmont and Coastal Plain, shallots are a one-time spring crop grown from sets. There "
   "is no local planting guide specific to shallot, so this follows onion, a very close relative: "
   "push sets into workable soil early, from late February into late March in the Coastal Plain, "
   "pointy end up, 6 to 8 inches apart. Grow intermediate-day types in the warmer Coastal Plain; "
   "the cooler Piedmont is long-day country. Each set splits into a clump you dig in early-to-mid "
   "summer once the tops flop over.",
}

REGION_SEASONED = {
 ("onion", "mid_south"):
   "Onion in the Mid-South is a single spring-planted crop with no fall crop. This belt is "
   "intermediate-day onion country: it sits around and below the 36°N line where growers move "
   "off long-day types, so intermediate-day varieties (the widely adaptable Candy is the regional "
   "standard) are the reliable pick, with short-day (Southern) types also succeeding in the "
   "lowland south and long-day types workable only at the cooler northern edge. Set sets or "
   "seedlings out as soon as the soil is workable, roughly mid February into late March in zone 8 "
   "and about a week and a half later in the cooler zone 7 uplands; intermediate-day onions size "
   "up best when set early, so the window closes by the end of March rather than running into "
   "April. Onion is cold-hardy and goes in well before the last frost. Bulbing is triggered by day "
   "length rather than by planting date, so bulbs mature on roughly the same midsummer calendar "
   "regardless of exactly when they went in; lift and cure two to four weeks before storage. "
   "University of Arkansas, Oklahoma State, and University of Tennessee Extension all steer this "
   "belt to short-day or intermediate-day onions.",
 ("onion", "mid_atlantic"):
   "Onion in the Mid-Atlantic is a single spring-planted crop with no fall crop. Day-length "
   "suitability splits by zone: the cooler Piedmont north (zone 7) is long-day onion country, "
   "while the Coastal Plain south (zone 8, at or below the 36°N line) is intermediate-day "
   "country, where NC State recommends short-day types for eastern North Carolina and calls "
   "long-day onions not recommended there. Virginia Cooperative Extension's 426-331 tables carry "
   "only a spring window and no fall column; for the intermediate-day Coastal Plain we close the "
   "planting window by the end of March, about Feb 20 to Mar 31 in zone 8, rather than running to "
   "the table's April date, since intermediate-day onions size up best when set early, while the "
   "long-day Piedmont keeps the fuller spring window, about Mar 1 to May 1 in zone 7. Set sets or "
   "seedlings out as soon as the soil is workable, well ahead of the last frost since onion is "
   "cold-hardy. Bulbing is triggered by day length rather than by planting date, so bulbs mature "
   "on roughly the same midsummer calendar regardless of exactly when they went in; lift and cure "
   "two to four weeks before storage.",
 ("shallot", "mid_south"):
   "No University of Arkansas Cooperative Extension row exists for shallot in this belt, so this "
   "cell follows the guide's Onion (bulbing) row, the closest related allium it documents, with an "
   "identical set-planted, spring-only culture and days-to-maturity range. Shallots share onion's "
   "photoperiod response, both being Allium cepa, so this is intermediate-day territory: grow "
   "intermediate-day shallots or reliable traditional set types, with short-day types also suited "
   "to the lowland south and long-day types workable at the cooler northern edge. Push sets into "
   "workable soil early, from February into late March, a week and a half later in the cooler zone "
   "7 uplands, 6 to 8 inches apart, tip at the surface; setting early lets the clump size up "
   "before the day-length trigger. The clump divides and sizes up as days lengthen, then is dug "
   "once most tops fall, roughly mid-to-late summer regardless of the exact planting date.",
 ("shallot", "mid_atlantic"):
   "No VCE 426-331 row exists for shallot in this belt, so this cell follows the guide's Onion "
   "(bulbing) row, the closest related allium it documents, with an identical set-planted, "
   "spring-only culture and days-to-maturity range. Shallots share onion's photoperiod response, "
   "both being Allium cepa, so day-length suitability splits by zone like onion: the cooler "
   "Piedmont north (zone 7) is long-day country, while the Coastal Plain south (zone 8) is "
   "intermediate-day country, where short-day set types are the traditional choice in eastern "
   "North Carolina. Push sets into workable soil as the ground allows, and in the intermediate-day "
   "Coastal Plain set them early, from late February into late March, so the clump sizes up before "
   "the day-length trigger, 6 to 8 inches apart, tip at the surface. The clump divides and sizes "
   "up as days lengthen, then is dug once most tops fall, roughly mid-to-late summer regardless of "
   "the exact planting date.",
}

# new source_catalog entries (T1 onion day-length authorities backing the flip)
CATALOG_ADDS = {
 "uada_ext_fsa6014": {
   "id": "uada_ext_fsa6014",
   "name": "UAEX FSA6014, Home Gardening Series: Onions",
   "publisher": "University of Arkansas Division of Agriculture, Cooperative Extension Service",
   "url": "https://www.uaex.uada.edu/publications/PDF/FSA-6014.pdf",
   "source_class": "university_extension",
   "trust_tier": "high",
   "accessed": "2026-07",
   "tier": "T1",
   "citable_for": "UAEX specific publication FSA6014 (Home Gardening Series, Onions). Arkansas "
     "onion day-length recommendation: short-day cultivars adapted statewide, intermediate-day "
     "cultivars adapted to the northern half; long-day not listed as adapted. Cultivar table "
     "(Candy classed short/intermediate, adaptable to a wide range of latitudes) and the spring "
     "transplant window (February through April). Backs the mid_south onion + shallot "
     "intermediate_day recommendation. Parent portal entry: uada_ext.",
   "_admission_provenance": "onion/shallot day-length correction (2026-07-21). Sub-ID under "
     "uada_ext (T1, 1862 Land Grant); inherits parent tier. Surfaced the Arkansas onion "
     "day-length + cultivar guidance that the mid_south region build did not separately cite. "
     "Mirrors the uada_ext_fsa6001 sub-ID pattern.",
 },
 "ncsu_ext_bulb_onions": {
   "id": "ncsu_ext_bulb_onions",
   "name": "NC State Extension: Bulb Onions",
   "publisher": "NC State",
   "url": "https://content.ces.ncsu.edu/bulb-onions",
   "source_class": "university_extension",
   "trust_tier": "high",
   "accessed": "2026-07",
   "tier": "T1",
   "citable_for": "NC State Extension 'Bulb Onions'. Day-length definitions (short-day 10-12 h, "
     "intermediate 12-14 h, long-day 14-16 h) and the recommendation that short-day onions are "
     "best suited for eastern North Carolina, with a fall/late-winter planting culture. Backs the "
     "mid_atlantic Coastal Plain (zone 8) onion + shallot intermediate_day recommendation and the "
     "short-day southern-coastal note. Parent portal entry: ncsu_ext.",
   "_admission_provenance": "onion/shallot day-length correction (2026-07-21). Sub-ID under "
     "ncsu_ext (T1, 1862 Land Grant); inherits parent tier. Surfaced the eastern-NC onion "
     "day-length recommendation the mid_atlantic region build did not separately cite.",
 },
}

# which day-length source each belt's region cells gain (appended to region-cell `sources`)
BELT_SOURCE = {"mid_south": "uada_ext_fsa6014", "mid_atlantic": "ncsu_ext_bulb_onions"}

# ---------------------------------------------------------------- targets
# (slug, region, [zones]) -- zones that flip in each region cell
TARGETS = [
 ("onion", "mid_south", ["7", "8"]),
 ("onion", "mid_atlantic", ["8"]),
 ("shallot", "mid_south", ["7", "8"]),
 ("shallot", "mid_atlantic", ["8"]),
]


def cpath(slug, rel):
    return f"$.crops[?(@.slug=='{slug}')].{rel}"


def read_current(data, full_path):
    parent, leaf = ap.resolve_parent(data, full_path)
    return ap.leaf_get(parent, leaf)


def main():
    raw = open(CANON, "rb").read()
    base_sha = hashlib.sha256(raw).hexdigest()
    data = json.loads(raw)
    patches = []

    def repl(slug, rel, new):
        fp = cpath(slug, rel)
        cur = read_current(data, fp)
        if cur is ap._MISSING:
            sys.exit(f"MISSING current value at {fp}")
        if cur == new:
            sys.exit(f"NO-OP (current already equals new) at {fp}")
        patches.append({"op": "replace", "json_path": fp, "from": cur, "value": new})

    for slug, region, zones in TARGETS:
        for z in zones:
            base = f"regions.{region}.resolved_by_zone.{z}"
            repl(slug, f"{base}.recommended_day_length_type", "intermediate_day")
            repl(slug, f"{base}.day_length_note_beginner", DL_BEGINNER[(slug, region, z)])
            repl(slug, f"{base}.day_length_note_seasoned", DL_SEASONED[(slug, region, z)])
            plant_out, last_plant = WINDOW[(slug, region, z)]
            repl(slug, f"{base}.plant_out", plant_out)
            repl(slug, f"{base}.last_plant_date", last_plant)
            repl(slug, f"{base}.calendar[3]", "growing")   # April: plant -> growing
            repl(slug, f"{base}.zone_notes", ZONE_NOTES[(slug, region, z)])
        # region-level prose + sources (once per crop/belt)
        repl(slug, f"regions.{region}.region_notes_beginner", REGION_BEGINNER[(slug, region)])
        repl(slug, f"regions.{region}.region_notes_seasoned", REGION_SEASONED[(slug, region)])
        src_id = BELT_SOURCE[region]
        cur_sources = read_current(data, cpath(slug, f"regions.{region}.sources"))
        if src_id not in cur_sources:
            patches.append({"op": "replace",
                            "json_path": cpath(slug, f"regions.{region}.sources"),
                            "from": cur_sources, "value": cur_sources + [src_id]})

    # source_catalog adds (absolute path, no crop filter)
    for cid, entry in CATALOG_ADDS.items():
        patches.append({"op": "add", "json_path": f"$.source_catalog.{cid}", "value": entry})

    out = {"base_sha": base_sha, "patches": patches}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"base_sha {base_sha[:12]}  ->  {len(patches)} patches  ->  {OUT}")
    # guard: no em-dashes / '--' in any authored string
    bad = [p["json_path"] for p in patches
           if isinstance(p.get("value"), str) and ("—" in p["value"] or "--" in p["value"])]
    if bad:
        sys.exit("EM-DASH/-- GUARD tripped in: " + "; ".join(bad))
    print("em-dash guard: clean")


if __name__ == "__main__":
    main()
