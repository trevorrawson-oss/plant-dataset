#!/usr/bin/env python3
"""RGV staged-cell anomaly auditor -- a DETECTOR (not a deriver) for the bug classes the
RGV authoring batches have produced, run over the staging files before the atomic promote.

It does NOT compute the "right" calendar (the certified frost-free calendars are a complex
multi-rule product, only ~75% reproducible by a naive rule). It flags SUSPICIOUS cells for
review: the specific defect classes caught in Tasks 4a/4b review.

Universal checks (every rgv cell): region_id, region_label, zone_span==["9","10"], resolved_by_zone
keys==["9","10"], no lifted_from_zone, resolution_method frost-free, resolved_from nulls, no
cold_pause anywhere (RGV is frost-free), no em dashes in consumer copy, 12-token calendars.
Annual-calendar checks (cells carrying a plant_out window): no in-ground month tokened season_over
(the 4a bug), no start_indoors month tokened season_over (the 4b bug).

Usage: python3 tools/rgv_cell_audit.py tools/staging/rgv_annuals_*.json [...]
Exit 1 if any issue is found.
"""
import json
import re
import sys

MON = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])}
LABEL = "Rio Grande Valley: Subtropical South Texas"
CONSUMER_KEYS_RE = re.compile(r"(region_notes|_note|basis|_beginner|_seasoned)")
CAL_VOCAB = {"plant", "indoors", "growing", "harvest", "season_over", "heat_pause",
             "cold_pause", "bloom", "prune", "care", "dormant", "wait"}


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
    artifact from a donor cell -- e.g. uf_ifas pointing at a CTAHR/Hawaii URL in one rule entry
    and the real ifas URL in another). Neither the gate (catalog membership + presence) nor the
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


def audit_cell(slug, cell):
    V = []
    if cell.get("region_id") != "rgv":
        V.append(f"region_id != 'rgv' ({cell.get('region_id')!r})")
    if cell.get("region_label") != LABEL:
        V.append(f"region_label != {LABEL!r} ({cell.get('region_label')!r})")
    if cell.get("zone_span") != ["9", "10"]:
        V.append(f"zone_span != ['9','10'] ({cell.get('zone_span')!r})")
    rbz = cell.get("resolved_by_zone") or {}
    if sorted(rbz) != ["10", "9"]:
        V.append(f"resolved_by_zone keys != ['9','10'] ({sorted(rbz)})")
    for k in _emdash_walk(cell):
        V.append(f"em/en dash in consumer field {k!r}")
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
            V.append(f"z{z}: stray lifted_from_zone (RGV is authored fresh)")
        rm = cz.get("resolution_method")
        # RGV is frost-free: an annual cell must use a frost-FREE method (e.g. month_resolved_frost_free);
        # a perennial/evergreen cell legitimately uses perennial_*_precompute. The anti-pattern is any
        # FROST-ANCHORED method (which implies annual frost dates the Valley does not have).
        if isinstance(rm, str) and "frost_anchored" in rm:
            V.append(f"z{z}: frost-anchored resolution_method in the frost-free RGV ({rm!r})")
        rf = cz.get("resolved_from")
        if rf not in (None, {}) and not (isinstance(rf, dict) and rf.get("last_frost") is None
                                         and rf.get("first_frost") is None):
            V.append(f"z{z}: resolved_from not null-frost ({rf!r})")
        cal = cz.get("calendar")
        # trees legitimately carry empty/absent calendars (A3-governed); only check populated ones
        if cal:
            if len(cal) != 12:
                V.append(f"z{z}: calendar len {len(cal)} != 12")
            for tok in cal:
                if tok not in CAL_VOCAB:
                    V.append(f"z{z}: unknown calendar token {tok!r}")
            if "cold_pause" in cal:
                V.append(f"z{z}: cold_pause present (RGV is frost-free)")
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


MON_R = {i: m for m, i in MON.items()}


def main(paths):
    total = 0
    for p in paths:
        data = json.load(open(p, encoding="utf-8"))
        for slug, cell in data.items():
            for v in audit_cell(slug, cell):
                print(f"  {slug}: {v}")
                total += 1
    n_cells = sum(len(json.load(open(p, encoding="utf-8"))) for p in paths)
    print(f"rgv_cell_audit: {total} issue(s) across {n_cells} cell(s) in {len(paths)} file(s)")
    return 1 if total else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: rgv_cell_audit.py <staging.json> [...]")
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
