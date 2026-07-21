#!/usr/bin/env python3
"""Build the mid_south ANNUAL staging cells (cool + warm) by transforming the certified,
gate-clean mid_atlantic annual cells to the mid_south frost anchors + UAEX sources.

The two regions share the identical 82-crop annual roster, the identical frost-anchored model,
span ["7","8"], and the same fall-cycle machinery; only the REGION differs. Crop biology (DTM,
weeks-indoors) is intrinsic. So the mechanical, deterministic parts -- resolved-date arithmetic,
calendar derivation, source ids, region metadata -- are transformed here (exact + consistent),
and the JUDGMENT parts (prose honesty, house voice) are finished by a subagent prose-review pass.

Deltas from mid_atlantic (docs/reviews/notes/2026-07-20/mid_south_sources.md):
  1. Anchors: z7 last Apr 10 / first Oct 24 (FSA6001 Zone D); z8 last Apr 3 / first Oct 31 (NWS
     Little Rock). Spring windows shift by the last_frost delta (-5 both zones); frost-limited
     windows by the first_frost delta (z7 -1, z8 +1). Shifting (not re-resolving) preserves the
     hand-authored succession / frost-limited windows in the certified cells.
  2. Fall windows: UAEX's fall table (tighter/different from VCE) -- authored fresh per crop
     (FALL_UAEX below), z7 one week earlier than z8. Three crops that were single-cycle in
     mid_atlantic gain a UAEX-documented fall cycle (sweet-corn, green-beans-bush, potato).

Run: python3 tools/build_mid_south_cells.py  ->  writes tools/staging/mid_south_annuals_{cool,warm}.json
Prose fields carry a mechanical name-swap DRAFT; the subagent review pass rewrites them.
"""
import copy
import datetime
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STAGING = os.path.join(HERE, "staging")
sys.path.insert(0, HERE)
from second_cycle import build_two_cycle_cell
from annual_calendar import derive_annual_calendar
from derive_realized_successions import derive_cell_realized

CANON = os.path.join(os.path.dirname(HERE), "crops_data_final.json")
_INTERVAL_WEEKS = {c["slug"]: (c.get("succession_policy") or {}).get("interval_weeks")
                   for c in json.load(open(CANON, encoding="utf-8"))["crops"]}

YEAR = 2026
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

MA_ANCHORS = {"7": {"last_frost": "Apr 15", "first_frost": "Oct 25"},
              "8": {"last_frost": "Apr 8", "first_frost": "Oct 30"}}
MS_ANCHORS = {"7": {"last_frost": "Apr 10", "first_frost": "Oct 24"},
              "8": {"last_frost": "Apr 3", "first_frost": "Oct 31"}}
FALL_ANCHOR_KEYS = {"first_frost", "hard_frost_or_heat", "heat_or_hard_frost"}

REGION_ID = "mid_south"
REGION_LABEL = "Mid-South: Ozark Uplands and Delta Lowlands"
SPRING_SRC = "uada_ext_spring_veg"
FALL_SRC = "uada_ext_fall_veg"
URLS = {
    "uada_ext_spring_veg": "https://www.uaex.uada.edu/yard-garden/vegetables/spring-summer-planting-dates.aspx",
    "uada_ext_fall_veg": "https://www.uaex.uada.edu/yard-garden/vegetables/fall-planting-dates.aspx",
}
VERIFIED = "2026-07-20"

# UAEX fall plant_out window (zone 8 / central AR). z7 is one week earlier (upland, earlier frost).
FALL_UAEX = {
    "beefsteak-tomato": ("Jul 1", "Jul 15"), "cherry-tomato": ("Jul 1", "Jul 15"),
    "grape-tomato": ("Jul 1", "Jul 15"), "heirloom-tomato": ("Jul 1", "Jul 15"),
    "roma-tomato": ("Jul 1", "Jul 15"),
    "cucumber": ("Aug 1", "Aug 15"), "english-cucumber": ("Aug 1", "Aug 15"),
    "pickling-cucumber": ("Aug 1", "Aug 15"), "slicing-cucumber": ("Aug 1", "Aug 15"),
    "yellow-summer-squash": ("Jul 15", "Aug 15"), "zucchini-courgette": ("Jul 15", "Aug 15"),
    "broccoli": ("Aug 1", "Sep 1"), "cabbage": ("Aug 10", "Sep 1"),
    "cauliflower": ("Aug 10", "Sep 1"), "bok-choy": ("Aug 1", "Sep 1"),
    "collards": ("Aug 1", "Sep 15"), "kale": ("Aug 20", "Sep 15"),
    "kohlrabi": ("Aug 1", "Sep 1"), "arugula": ("Aug 20", "Sep 15"),
    "carrot": ("Aug 1", "Aug 15"), "beet": ("Aug 15", "Sep 1"),
    "swiss-chard": ("Aug 15", "Sep 1"), "turnip": ("Aug 1", "Sep 15"),
    "lettuce-leaf": ("Aug 20", "Sep 15"), "radish": ("Aug 20", "Sep 15"),
    "spinach": ("Aug 25", "Sep 15"),
    # crops that were single-cycle in mid_atlantic but carry a UAEX-documented fall window:
    "sweet-corn": ("Jul 1", "Jul 15"), "green-beans-bush": ("Aug 1", "Sep 1"),
    "potato": ("Jul 15", "Aug 1"),
}
# UAEX omits it; brassica-typical window used, flagged in notes:
FALL_FLAGGED = {"kohlrabi", "arugula"}


def _d(s):
    mon, day = s.split()
    return datetime.date(YEAR, MON.index(mon) + 1, int(day))


def _fmt(dt):
    return f"{MON[dt.month - 1]} {dt.day}"


TOK = re.compile(r"^[A-Z][a-z]{2} \d{1,2}$")


def _lf_delta(zone):
    return (_d(MS_ANCHORS[zone]["last_frost"]) - _d(MA_ANCHORS[zone]["last_frost"])).days


def _ff_delta(zone):
    return (_d(MS_ANCHORS[zone]["first_frost"]) - _d(MA_ANCHORS[zone]["first_frost"])).days


def _shift_tok(tok, zone):
    """Shift one 'Mon D' token; leave month-only / non-date tokens untouched. Spring-half
    (Jan-Jul) dates ride the last_frost delta; late-season (Aug-Dec) dates ride the first_frost
    delta -- so single windows, comma-joined heat_pause reflush windows, and mixed-anchor harvest
    ranges all translate correctly at month granularity without per-field anchor bookkeeping."""
    if not TOK.match(tok):
        return tok
    dt = _d(tok)
    return _fmt(dt + datetime.timedelta(_lf_delta(zone) if dt.month <= 7 else _ff_delta(zone)))


def _shift_str(s, zone):
    parts = re.split(r"(, | - )", s)
    return "".join(_shift_tok(p, zone) if TOK.match(p) else p for p in parts)


def _spring_cycle(cell):
    return next((p for p in cell.get("plantings", []) if p.get("track") != "second_planting"), {})


def shift_spring(cell, zone):
    """Shifted spring resolved fields for one zone (preserves hand-authored succession /
    frost-limited / reflush windows -- only translates them to the mid_south anchors)."""
    src = cell["resolved_by_zone"][zone]
    out = {}
    for f in ("start_indoors", "plant_out", "first_plant_date", "last_plant_date",
              "harvest", "harvest_start", "harvest_end"):
        if src.get(f):
            out[f] = _shift_str(src[f], zone)
    return out


def author_fall(slug, cell, zone, is_warm):
    """UAEX fall cycle for one zone. plant_out from FALL_UAEX (z7 one week earlier); harvest =
    plant_out + the crop's spring DTM offset. Warm (frost-tender) fall crops cap harvest 3 days
    before first frost; cool (frost-hardy) fall crops carry the crop's full DTM tail into early
    winter (they keep in the field through light frost), capped at Dec 15 to avoid a year wrap."""
    z8s, z8e = FALL_UAEX[slug]
    week = 0 if zone == "8" else -7
    po_s = _d(z8s) + datetime.timedelta(week)
    po_e = _d(z8e) + datetime.timedelta(week)
    sp = _spring_cycle(cell)
    hs_e = sp.get("harvest_start") or [{}]
    dtm = hs_e[0].get("offset_days", 55) if isinstance(hs_e, list) else 55
    he_e = sp.get("harvest_end") or [{}]
    he_off = he_e[0].get("offset_days") if (isinstance(he_e, list) and he_e
                                            and he_e[0].get("from") == "plant_out") else None
    hstart = po_s + datetime.timedelta(dtm)
    if is_warm:
        ff = _d(MS_ANCHORS[zone]["first_frost"]) - datetime.timedelta(3)
        hstart = min(hstart, ff)
        hend = min(po_e + datetime.timedelta(dtm + 15), ff)
    else:
        tail = he_off if he_off is not None else dtm + 45
        hend = min(po_s + datetime.timedelta(tail), _d("Dec 15"))
    if hend < hstart:
        hend = hstart
    # the fall crop is started ~the same lead time as spring (UAEX: "sow seed about four weeks
    # earlier" for transplant crops); default 4 weeks where the crop has no spring indoor start.
    si = sp.get("start_indoors")
    po = sp.get("plant_out")
    lead = 28
    if isinstance(si, list) and si and isinstance(po, list) and po:
        lead = max(po[0]["offset_days"] - si[0]["offset_days"], 14)
    fall = {"start_indoors": f"{_fmt(po_s - datetime.timedelta(lead))} - {_fmt(po_e - datetime.timedelta(lead))}",
            "plant_out": f"{_fmt(po_s)} - {_fmt(po_e)}",
            "harvest_start": _fmt(hstart), "harvest_end": _fmt(hend),
            "sources": [FALL_SRC],
            "anchoring_urls": {FALL_SRC: {"url": URLS[FALL_SRC], "verified": VERIFIED}}}
    return fall


# ---- prose: mechanical name-swap DRAFT (the subagent review pass finalizes voice + specifics) ----
PROSE_SWAP = [
    ("Virginia Cooperative Extension's Pub. 426-331", "the University of Arkansas Cooperative Extension"),
    ("Virginia Cooperative Extension", "University of Arkansas Cooperative Extension"),
    ("VCE 426-331", "the University of Arkansas Cooperative Extension"),
    ("VCE", "the University of Arkansas Cooperative Extension"),
    ("426-331", "planting-date tables"),
    ("NC State Extension", "University of Arkansas Cooperative Extension"),
    ("NC State", "the University of Arkansas"),
    ("Piedmont and Coastal Plain", "Ozark Uplands and Delta Lowlands"),
    ("Coastal Plain and Piedmont", "Delta Lowlands and Ozark Uplands"),
    ("the Piedmont", "the uplands"),
    ("Coastal Plain", "lowland South"),
    ("Tidewater", "Delta"),
    ("Mid-Atlantic", "Mid-South"),
    ("mid-Atlantic", "Mid-South"),
]


def swap_prose(o):
    if isinstance(o, str):
        s = o
        for a, b in PROSE_SWAP:
            s = s.replace(a, b)
        return s
    if isinstance(o, dict):
        return {k: swap_prose(v) for k, v in o.items()}
    if isinstance(o, list):
        return [swap_prose(v) for v in o]
    return o


def swap_sources_tree(o, src_id):
    """Recursively rewrite every sources list + anchoring_urls map to a single source id+url."""
    if isinstance(o, dict):
        out = {}
        for k, v in o.items():
            if k == "sources" and isinstance(v, list):
                out[k] = [src_id]
            elif k.endswith("anchoring_urls") and isinstance(v, dict):
                out[k] = {src_id: {"url": URLS[src_id], "verified": VERIFIED}} if v else {}
            elif k == "source_quote":
                out[k] = v  # left for prose review
            else:
                out[k] = swap_sources_tree(v, src_id)
        return out
    if isinstance(o, list):
        return [swap_sources_tree(v, src_id) for v in o]
    return o


def _fix_winter_growing(zc):
    """After a re-derived two-cycle calendar's LAST productive month (plant/indoors/harvest),
    the deriver leaves trailing `growing` for an empty late-fall gap; A37 flags it as unreachable
    (`traces back to harvest -- nothing is planted before it`). Those trailing months are winter
    dormancy: convert them to cold_pause (the honest token, and what the certified two-cycle cells
    carry). Only touches months AFTER the season's last productive token, never a mid-season lull."""
    cal = zc.get("calendar")
    if not cal:
        return
    productive = {"plant", "indoors", "harvest"}
    last = max((i for i, t in enumerate(cal) if t in productive), default=-1)
    for j in range(last + 1, len(cal)):
        if cal[j] == "growing":
            cal[j] = "cold_pause"


def _fix_unreachable_growing(zc):
    """Convert an unreachable mid-season `growing` (A37: the first non-growing token going
    backward with wrap is a harvest/pause, not a plant/indoors -- an empty bed between cycles)
    to its honest token: heat_pause for a cool crop that carries a heat_pause object (the humid
    summer set-failure gap), otherwise season_over (e.g. garlic's cured-and-empty summer bed).
    A converted heat_pause month is added to heat_pause.months so the A31 invariant stays clean."""
    cal = zc.get("calendar")
    if not cal:
        return
    n = len(cal)

    def reachable(m):
        for k in range(1, n + 1):
            t = cal[(m - k) % n]
            if t == "growing":
                continue
            return t in ("plant", "indoors")
        return False

    to_pause = "heat_pause" if "heat_pause" in zc else "season_over"
    for m in range(n):
        if cal[m] == "growing" and not reachable(m):
            cal[m] = to_pause
            if to_pause == "heat_pause":
                months = zc["heat_pause"].setdefault("months", [])
                if (m + 1) not in months:
                    months.append(m + 1)
                    months.sort()


def _fix_heat_pause(zc):
    """Reconcile heat_pause.months to the derived calendar: keep only the originally-hot months
    the calendar still renders as heat_pause or a plant/indoors flip (the A31 annual-calendar
    invariant). A UAEX early-July fall planting fills the old midsummer pause with plant/growing,
    so a stale [7,8] would flag Aug (now 'growing'). Drop heat_pause entirely if nothing remains."""
    hp = zc.get("heat_pause")
    if not hp:
        return
    cal = zc.get("calendar") or []
    keep = [m for m in hp.get("months", [])
            if 1 <= m <= len(cal) and cal[m - 1] in ("heat_pause", "plant", "indoors")]
    if keep:
        hp["months"] = keep
    else:
        zc.pop("heat_pause", None)


def transform(slug, cell, is_warm):
    ms = copy.deepcopy(cell)
    ms["region_id"] = REGION_ID
    ms["region_label"] = REGION_LABEL
    has_fall = slug in FALL_UAEX
    # plantings[]: swap sources by track (spring->spring src, fall->fall src) + update fall plant_out
    new_pl = []
    for p in ms.get("plantings", []):
        track_fall = p.get("track") == "second_planting"
        p = swap_sources_tree(p, FALL_SRC if track_fall else SPRING_SRC)
        new_pl.append(p)
    ms["plantings"] = new_pl
    ms = swap_prose(ms)

    rbz = {}
    for z in ("7", "8"):
        old = cell["resolved_by_zone"][z]
        spring = shift_spring(cell, z)
        base = {"region_id": REGION_ID, "region_label": REGION_LABEL, "zone_span": ["7", "8"],
                "resolution_method": "frost_anchored_resolved",
                "resolved_from": {"last_frost": MS_ANCHORS[z]["last_frost"],
                                  "first_frost": MS_ANCHORS[z]["first_frost"]}}
        # start from the certified cell (preserves crop-specific archetype fields:
        # recommended_day_length_type, day_length_note_*, grown_as, planting_layout, ...) with
        # prose name-swapped, then override the computed window/calendar/source fields.
        zc = swap_prose(copy.deepcopy(old))
        zc.pop("second_planting", None)
        if has_fall:
            fall = author_fall(slug, cell, z, is_warm)
            built = build_two_cycle_cell(base, spring, fall)
            for k in ("plant_out", "start_indoors", "harvest", "harvest_start", "harvest_end",
                      "first_plant_date", "last_plant_date", "second_planting", "calendar"):
                if k in built:
                    zc[k] = built[k]
        else:
            for k in ("plant_out", "start_indoors", "harvest", "harvest_start", "harvest_end",
                      "first_plant_date", "last_plant_date"):
                zc[k] = spring[k] if k in spring else zc.get(k)
            single = {k: spring[k] for k in ("plant_out", "harvest", "start_indoors") if k in spring}
            single["resolution_method"] = "frost_anchored_resolved"
            single["resolved_from"] = base["resolved_from"]
            zc["calendar"] = derive_annual_calendar(single, "frost_anchored")
        # port heat_pause TOKEN placement from the certified calendar (month-granular, robust to the
        # <=5-day shift): the deriver never emits heat_pause, so a cool crop's empty summer gap would
        # otherwise render as unreachable `growing`.
        old_cal = old.get("calendar") or []
        for m in range(min(len(zc["calendar"]), len(old_cal))):
            if old_cal[m] == "heat_pause" and zc["calendar"][m] == "growing":
                zc["calendar"][m] = "heat_pause"
        zc["resolution_method"] = "frost_anchored_resolved"
        zc["resolved_from"] = {"last_frost": MS_ANCHORS[z]["last_frost"],
                               "first_frost": MS_ANCHORS[z]["first_frost"]}
        srcs = [SPRING_SRC] + ([FALL_SRC] if has_fall else [])
        zc["sources"] = srcs
        zc["anchoring_urls"] = {s: {"url": URLS[s], "verified": VERIFIED} for s in srcs}
        zc["planting_note"] = "multi_season" if has_fall else old.get("planting_note")
        if "heat_pause" in zc:
            hp = zc["heat_pause"]
            hp["sources"] = [FALL_SRC if has_fall else SPRING_SRC]
            hp["anchoring_urls"] = {hp["sources"][0]: {"url": URLS[hp["sources"][0]], "verified": VERIFIED}}
        if slug in FALL_FLAGGED:
            zc["notes"] = ("Fall window authored from the University of Arkansas brassica/greens fall "
                           "guidance; UAEX's fall table does not list this crop by name.")
        _fix_winter_growing(zc)
        _fix_unreachable_growing(zc)
        _fix_heat_pause(zc)
        iw = _INTERVAL_WEEKS.get(slug)
        if "successions_realized" in old and iw:
            zc["successions_realized"] = derive_cell_realized(zc, iw)
        rbz[z] = zc
    ms["resolved_by_zone"] = rbz
    # cell-level sources
    cell_srcs = [SPRING_SRC] + ([FALL_SRC] if has_fall else [])
    ms["sources"] = cell_srcs
    if "anchoring_urls" in ms:
        ms["anchoring_urls"] = {s: {"url": URLS[s], "verified": VERIFIED} for s in cell_srcs}
    return ms


def main():
    for infile, outfile in [("mid_atlantic_annuals_cool.json", "mid_south_annuals_cool.json"),
                            ("mid_atlantic_annuals_warm.json", "mid_south_annuals_warm.json")]:
        is_warm = "warm" in outfile
        data = json.load(open(os.path.join(STAGING, infile), encoding="utf-8"))
        out = {slug: transform(slug, cell, is_warm) for slug, cell in data.items()}
        with open(os.path.join(STAGING, outfile), "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
        n_fall = sum(1 for s in out if s in FALL_UAEX)
        print(f"{outfile}: {len(out)} cells ({n_fall} with a UAEX fall cycle)")


if __name__ == "__main__":
    main()
