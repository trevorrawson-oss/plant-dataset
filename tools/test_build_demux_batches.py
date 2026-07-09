#!/usr/bin/env python3
"""build_demux_batches unit tests -- fixture cells lifted from the canonical
(bell-pepper se_gulf z8 = the spec's worked example; onion/shallot alt cells)."""
from build_demux_batches import classify, second_planting_value, or_norm_ops, clean_ops

BELL = {  # bell-pepper se_gulf z8, verbatim shape
    "start_indoors": None,
    "plant_out": "Mar 15 - Apr 15, Sep 1 - Sep 20",
    "harvest": "May 15 - Jun 30, Nov 1 - Nov 30",
    "harvest_start": "May 15", "harvest_end": "Nov 30",
    "first_plant_date": "Mar 15", "last_plant_date": "Sep 20",
    "sources": ["src_a"], "anchoring_urls": {"src_a": {"url": "https://x.edu", "verified": "2026-01-01"}},
}
REFLUSH = {"start_indoors": None, "plant_out": "Feb 1 - Mar 1",
           "harvest": "May 15 - Jun 30, Oct 1 - Dec 5"}
ALT = {"start_indoors": None, "plant_out": "Oct - Nov, Jan - March",
       "harvest": "Jun - Jul"}

assert classify(BELL) == "TWO_CROP"
assert classify(REFLUSH) == "REFLUSH"
assert classify(ALT) == "ALT_WINDOW"
assert classify({"plant_out": "Mar 15 - Apr 15", "harvest": "May 15 - Jun 30"}) is None

# extraction = the spec §2/§5 worked example, byte-exact
sp = second_planting_value(BELL)
assert sp == {"start_indoors": None, "plant_out": "Sep 1 - Sep 20",
              "harvest_start": "Nov 1", "harvest_end": "Nov 30",
              "sources": ["src_a"],
              "anchoring_urls": {"src_a": {"url": "https://x.edu", "verified": "2026-01-01"}}}, sp

# or-norm: comma -> " or "; the onion ca_north_coast continuity fix is special-cased
ops = or_norm_ops("shallot", "ca_interior", "8", ALT)
assert len(ops) == 1 and ops[0]["value"] == "Oct - Nov or Jan - March" and ops[0]["from"] == ALT["plant_out"]
fix = or_norm_ops("onion", "ca_north_coast", "9",
                  {"start_indoors": "Oct - Nov", "plant_out": "Nov - Jan, Jan - March", "harvest": "Jun"})
assert len(fix) == 1 and fix[0]["value"] == "Nov - March"
two_si = or_norm_ops("onion", "ca_interior", "8",
                     {"start_indoors": "Sep, Dec", "plant_out": "Oct - Nov, Jan - March", "harvest": "Jun - Jul"})
assert {o["value"] for o in two_si} == {"Sep or Dec", "Oct - Nov or Jan - March"}

# clean: strings -> primary span; envelope narrowed; ops from-guarded
cell3 = dict(BELL, second_planting=sp)
cops = {o["json_path"].rsplit(".", 1)[-1]: o for o in clean_ops("bell-pepper", "se_gulf", "8", cell3)}
assert cops["plant_out"]["value"] == "Mar 15 - Apr 15" and cops["plant_out"]["from"] == BELL["plant_out"]
assert cops["harvest"]["value"] == "May 15 - Jun 30"
assert cops["last_plant_date"]["value"] == "Apr 15"
assert cops["harvest_end"]["value"] == "Jun 30"
assert "first_plant_date" not in cops and "harvest_start" not in cops  # already primary
# month-granular second harvest: granularity preserved (potato-style)
pot = {"start_indoors": None, "plant_out": "Feb - Mar, Aug", "harvest": "May - Jun, Nov - Dec",
       "harvest_start": "May 1", "harvest_end": "Dec 31",
       "first_plant_date": "Feb 1", "last_plant_date": "Aug 31",
       "sources": ["s"], "anchoring_urls": {}}
psp = second_planting_value(pot)
assert psp["plant_out"] == "Aug" and psp["harvest_start"] == "Nov" and psp["harvest_end"] == "Dec"
pops = {o["json_path"].rsplit(".", 1)[-1]: o for o in clean_ops("potato", "ca_interior", "8", dict(pot, second_planting=psp))}
assert pops["harvest_end"]["value"] == "Jun"     # primary end, authored granularity
assert pops["last_plant_date"]["value"] == "Mar"  # primary plant_out end text

# fava shared-harvest ruling (spec §2 B-fava): extract + clean
FAVA = {"start_indoors": None, "plant_out": "Feb, Sep", "harvest": "Apr - May",
        "harvest_start": "Apr 1", "harvest_end": "May 31",
        "first_plant_date": "Feb 1", "last_plant_date": "Sep 20",
        "sources": ["s"], "anchoring_urls": {}}
fsp = second_planting_value(FAVA, shared_harvest=True)
assert fsp["plant_out"] == "Sep" and fsp["harvest_start"] == "Apr" and fsp["harvest_end"] == "May", fsp
fops = {o["json_path"].rsplit(".", 1)[-1]: o
        for o in clean_ops("broad-beans-fava", "warm_arid", "8", dict(FAVA, second_planting=fsp))}
assert fops["plant_out"]["value"] == "Feb"
assert "harvest" not in fops                      # shared single-span window, untouched
assert fops["last_plant_date"]["value"] == "Feb"  # narrowed to the primary end
assert "harvest_end" not in fops                  # May 31 sits inside "Apr - May"

# fall-span-FIRST pop-1 shape (broccoli ca_interior z9): keep the NON-sp span
BROC = {"start_indoors": "Nov 1 - Nov 22",
        "plant_out": "Aug 1 - Sep 30, Dec 1 - Feb 28",
        "harvest": "Mar 1 - May 1, Oct 15 - Dec 15",
        "harvest_start": "Mar 1", "harvest_end": "Dec 15",
        "first_plant_date": "Aug 1", "last_plant_date": "Feb 28",
        "second_planting": {"start_indoors": "Jun 20 - Aug 18",
                            "plant_out": "Aug 1 - Sep 30",
                            "harvest_start": "Oct 15", "harvest_end": "Dec 15",
                            "sources": ["s"], "anchoring_urls": {}}}
bops = {o["json_path"].rsplit(".", 1)[-1]: o for o in clean_ops("broccoli", "ca_interior", "9", BROC)}
assert bops["plant_out"]["value"] == "Dec 1 - Feb 28", bops["plant_out"]  # NOT s[0]
assert bops["harvest"]["value"] == "Mar 1 - May 1"
assert bops["harvest_end"]["value"] == "May 1"
assert bops["first_plant_date"]["value"] == "Dec 1"  # was the fall crop's Aug 1

print("build_demux_batches tests: OK")
