#!/usr/bin/env python3
"""Region-GENERIC staged-cell anomaly auditor -- a DETECTOR (not a deriver) for the bug
classes region authoring batches have produced, run over the staging files before the
atomic promote. Generalized from rgv_cell_audit.py (region_id + a per-region REGION_CONFIG
replace the RGV-hardcoded constants); rgv_cell_audit.py itself is left byte-untouched.

It does NOT compute the "right" calendar (the certified calendars are a complex multi-rule
product, only partially reproducible by a naive rule). It flags SUSPICIOUS cells for review.

Universal checks (every region's cells): region_id, region_label, zone_span==cfg span,
resolved_by_zone keys==cfg span, no lifted_from_zone, no em dashes in consumer copy,
12-token calendars, no stray unknown calendar tokens, no in-ground-month-tokened-season_over,
no start_indoors-month-tokened-season_over, citation id->URL misattribution.

Frost-model branch (the one place regions genuinely differ):
  - frost_model == "free"  (rgv):  resolution_method must be frost-FREE, resolved_from must
    be null-frost, and cold_pause anywhere in a calendar is an ERROR (rgv has no true winter).
  - frost_model == "anchored" (pnw): resolution_method must be 'frost_anchored_resolved',
    resolved_from must carry NON-null last_frost AND first_frost, and cold_pause is ALLOWED
    (skipped entirely -- pnw has a real frost-bound winter).

Usage: python3 tools/region_cell_audit.py <region_id> <staging.json> [...]
Exit 1 if any issue is found.
"""
import json
import re
import sys

MON = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])}
MON_R = {i: m for m, i in MON.items()}

CONSUMER_KEYS_RE = re.compile(r"(region_notes|_note|basis|_beginner|_seasoned)")
CAL_VOCAB = {"plant", "indoors", "growing", "harvest", "season_over", "heat_pause",
             "cold_pause", "bloom", "prune", "care", "dormant", "wait", "renovation"}

# region config: the shape each region's cells must obey
REGION_CONFIG = {
    "rgv": {"label": "Rio Grande Valley: Subtropical South Texas",
            "span": ["9", "10"], "frost_model": "free"},
    "pnw": {"label": "Maritime Pacific Northwest: Puget Sound and Willamette Valley",
            "span": ["8", "9"], "frost_model": "anchored"},
    "mid_atlantic": {"label": "Mid-Atlantic: Piedmont and Coastal Plain",
                     "span": ["7", "8"], "frost_model": "anchored"},
    "mid_south": {"label": "Mid-South: Ozark Uplands and Delta Lowlands",
                  "span": ["7", "8"], "frost_model": "anchored"},
    "nevada": {"label": "Nevada: Mojave High Desert (Las Vegas Valley)",
               "span": ["8", "9", "10"], "frost_model": "anchored"},
    "utah_dixie": {"label": "Utah: St. George Dixie (Mojave-edge high desert)",
                   "span": ["8"], "frost_model": "anchored"},
}


def mset(w):
    if not isinstance(w, str) or not w:
        return set()
    t = re.findall(r"([A-Z][a-z]{2})", w)
    if not t:
        return set()
    if len(t) == 1:
        return {MON[t[0]]} if t[0] in MON else set()
    a, b = MON.get(t[0]), MON.get(t[-1])
    if a is None or b is None:
        return set()
    out, i = set(), a
    while True:
        out.add(i)
        if i == b:
            break
        i = (i + 1) % 12
    return out


def _inground(plant_ms, harv_ms):
    ig = set()
    for p in plant_ms:
        i, steps = (p + 1) % 12, 0
        while i not in harv_ms and steps < 12:
            ig.add(i)
            i = (i + 1) % 12
            steps += 1
            if i in plant_ms:
                break
    return ig


def _emdash_walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, str) and CONSUMER_KEYS_RE.search(k) and ("—" in v or "–" in v):
                yield k
            yield from _emdash_walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from _emdash_walk(v)


def _anchor_urls_by_id(o, acc):
    """Collect source_id -> set(url) from every anchoring_urls map in the subtree. A single id
    mapping to two different URLs inside one cell = a citation misattribution (a copy-paste
    artifact from a donor cell). Neither the gate (catalog membership + presence) nor the
    shape checks catch it."""
    if isinstance(o, dict):
        au = o.get("anchoring_urls")
        if isinstance(au, dict):
            for sid, entry in au.items():
                url = entry.get("url") if isinstance(entry, dict) else None
                if url:
                    acc.setdefault(sid, set()).add(url)
        for k, v in o.items():
            if k != "anchoring_urls":
                _anchor_urls_by_id(v, acc)
    elif isinstance(o, list):
        for v in o:
            _anchor_urls_by_id(v, acc)


def audit_cell(slug, cell, region_id):
    cfg = REGION_CONFIG[region_id]
    frost_model = cfg["frost_model"]
    V = []
    if cell.get("region_id") != region_id:
        V.append(f"region_id != {region_id!r} ({cell.get('region_id')!r})")
    if cell.get("region_label") != cfg["label"]:
        V.append(f"region_label != {cfg['label']!r} ({cell.get('region_label')!r})")
    if cell.get("zone_span") != cfg["span"]:
        V.append(f"zone_span != {cfg['span']!r} ({cell.get('zone_span')!r})")
    rbz = cell.get("resolved_by_zone") or {}
    if sorted(rbz) != sorted(cfg["span"]):
        V.append(f"resolved_by_zone keys != {cfg['span']!r} ({sorted(rbz)})")
    for k in _emdash_walk(cell):
        V.append(f"em dash or en dash in consumer field {k!r}")
    id_urls = {}
    _anchor_urls_by_id(cell, id_urls)
    for sid, urls in id_urls.items():
        if len(urls) > 1:
            V.append(f"source id {sid!r} maps to {len(urls)} different URLs in one cell "
                     f"(citation misattribution): {sorted(urls)}")
    for z, cz in rbz.items():
        if not isinstance(cz, dict):
            V.append(f"z{z}: cell not a dict")
            continue
        if "lifted_from_zone" in cz:
            V.append(f"z{z}: stray lifted_from_zone ({region_id} is authored fresh)")
        rm = cz.get("resolution_method")
        rf = cz.get("resolved_from")
        if frost_model == "free":
            # frost-free regions (e.g. rgv): an annual cell must use a frost-FREE method (e.g.
            # month_resolved_frost_free); a perennial/evergreen cell legitimately uses
            # perennial_*_precompute. The anti-pattern is any FROST-ANCHORED method (which
            # implies annual frost dates the region does not have).
            if isinstance(rm, str) and "frost_anchored" in rm:
                V.append(f"z{z}: frost-anchored resolution_method in the frost-free "
                         f"{region_id} ({rm!r})")
            if rf not in (None, {}) and not (isinstance(rf, dict) and rf.get("last_frost") is None
                                             and rf.get("first_frost") is None):
                V.append(f"z{z}: resolved_from not null-frost ({rf!r})")
        elif frost_model == "anchored":
            # frost-anchored regions (e.g. pnw): a real annual/frost-bound winter, so an
            # ANNUAL cell must be resolved off real frost dates. The anti-pattern is a
            # frost-FREE method or missing/null frost dates -- that would silently drop the
            # region's winter. Tree/citrus perennial archetypes (resolution_method
            # perennial_precompute / perennial_evergreen_precompute) are a DIFFERENT climate
            # axis (chill/cold via min_winter_temp_f, not frost-window placement) -- this is
            # the exact exemption the "free" branch already grants perennial cells (rgv_trees/
            # rgv_citrus use these same two methods); mirror it here instead of wrongly
            # demanding frost_anchored_resolved + real frost dates on a tree/citrus cell (a
            # gap that would make EVERY pnw tree/citrus cell unauditable-clean, since the pnw
            # cell contract §5.2 explicitly allows resolved_from={} for citrus and real frost
            # dates OR {} for chill-gated trees -- see docs/pnw_cell_contract.md §1, §5.2).
            if rm in ("perennial_precompute", "perennial_evergreen_precompute"):
                if rf not in (None, {}) and not (isinstance(rf, dict) and rf.get("last_frost")
                                                 and rf.get("first_frost")):
                    V.append(f"z{z}: resolved_from partially populated in a perennial cell "
                             f"(must be {{}} or real last_frost+first_frost) in {rm!r} ({rf!r})")
            elif rm in ("perennial_woody_ornamental_precompute", "woody_ornamental_annual_precompute"):
                # woody-ornamental herb archetype (lavender/oregano/rosemary/sage/thyme): its
                # OWN resolution_method convention, used identically across every existing
                # region cell for these crops (confirmed against the real gate code --
                # woody_ornamental_gate.py / woody_ornamental_calendar.py key off grown_as,
                # not a resolution_method string -- and against the RGV Task 7 precedent,
                # which authored these same crops with this same method name). Still
                # genuinely frost-anchored here (derive_perennial_woody_calendar's dormant
                # bracket needs real last_frost/first_frost for a pnw cell; only a frost-free
                # region's perennial cell legitimately carries no frost dates), so require
                # real non-null frost dates same as the strict branch, just recognizing this
                # archetype's own method name instead of wrongly demanding the frost_anchored
                # annual archetype's generic string on a different archetype's cell.
                if not (isinstance(rf, dict) and rf.get("last_frost") and rf.get("first_frost")):
                    V.append(f"z{z}: resolved_from missing non-null last_frost/first_frost "
                             f"in the frost-anchored {region_id} ({rm!r})")
            else:
                if rm != "frost_anchored_resolved":
                    V.append(f"z{z}: resolution_method != 'frost_anchored_resolved' in the "
                             f"frost-anchored {region_id} ({rm!r})")
                if not (isinstance(rf, dict) and rf.get("last_frost") and rf.get("first_frost")):
                    V.append(f"z{z}: resolved_from missing non-null last_frost/first_frost "
                             f"in the frost-anchored {region_id} ({rf!r})")
        else:
            V.append(f"z{z}: unknown frost_model {frost_model!r} for region {region_id!r}")
        cal = cz.get("calendar")
        # trees legitimately carry empty/absent calendars (A3-governed); only check populated ones
        if cal:
            if len(cal) != 12:
                V.append(f"z{z}: calendar len {len(cal)} != 12")
            for tok in cal:
                if tok not in CAL_VOCAB:
                    V.append(f"z{z}: unknown calendar token {tok!r}")
            if frost_model == "free" and "cold_pause" in cal:
                V.append(f"z{z}: cold_pause present ({region_id} is frost-free)")
            # frost_model == "anchored": cold_pause is ALLOWED, skip the error entirely.
            # annual-calendar defect classes: only for cells with an outdoor plant window
            plant_ms = mset(cz.get("plant_out")) | mset((cz.get("second_planting") or {}).get("plant_out"))
            if plant_ms and len(cal) == 12:
                sp = cz.get("second_planting") or {}
                si = mset(cz.get("start_indoors")) | mset(sp.get("start_indoors"))
                hv = mset(cz.get("harvest")) or mset(
                    (cz.get("harvest_start") or "") + " - " + (cz.get("harvest_end") or ""))
                hv |= mset((sp.get("harvest_start") or "") + " - " + (sp.get("harvest_end") or ""))
                for m in _inground(plant_ms, hv):
                    if cal[m] == "season_over":
                        V.append(f"z{z}: month {MON_R[m]} in-ground but season_over (should be growing)")
                for m in si:
                    if cal[m] == "season_over":
                        V.append(f"z{z}: month {MON_R[m]} is start_indoors but season_over (should be indoors)")
    return V


def audit_cells(region_id, paths):
    total = 0
    for p in paths:
        data = json.load(open(p, encoding="utf-8"))
        for slug, cell in data.items():
            for v in audit_cell(slug, cell, region_id):
                print(f"  {slug}: {v}")
                total += 1
    n_cells = sum(len(json.load(open(p, encoding="utf-8"))) for p in paths)
    print(f"region_cell_audit[{region_id}]: {total} issue(s) across {n_cells} cell(s) in {len(paths)} file(s)")
    return total


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: region_cell_audit.py <region_id> <staging.json> [...]")
        sys.exit(2)
    n = audit_cells(sys.argv[1], sys.argv[2:])
    sys.exit(1 if n else 0)
