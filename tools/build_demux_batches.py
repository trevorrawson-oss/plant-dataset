#!/usr/bin/env python3
"""build_demux_batches.py -- deterministic generator for the de-mux batches
(spec 2026-07-09 §5, §7). READ-ONLY on the canonical: emits
tools/batches/second_planting_<name>.json for apply_patch.py, the only writer.

--stage populate : S1 -- second_planting ADD ops for the 90 TWO_CROP cells in 3
                   archetype batches; the 13 or-norm/continuity REPLACE ops ride
                   s1_b3. ABORTS if the roster's classification drifts from the
                   spec's pinned scope (counts below).
--stage clean    : S3 -- primary-only REPLACE ops for every second_planting cell
                   (pop-1 dedup + pop-2 clean) + envelope narrowing. Run ONLY
                   after Stage 2 (the plant-astro read-flip) is live.
"""
import argparse
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plant_windows import spans, window_count, single_date, in_span, months_overlap

HERE = os.path.dirname(os.path.abspath(__file__))
CANON = os.path.join(os.path.dirname(HERE), "crops_data_final.json")

S1_BATCHES = {
    "s1_b1_solanaceae": ["banana-pepper", "bell-pepper", "cayenne-pepper",
                         "eggplant", "habanero", "jalapeno", "tomatillo"],
    "s1_b2_cucurbits": ["acorn-squash", "butternut-squash", "cantaloupe",
                        "honeydew-melon", "pumpkin", "spaghetti-squash", "watermelon"],
    "s1_b3_rest": ["broad-beans-fava", "onion", "pole-beans", "potato", "shallot", "swiss-chard"],
}
# spec §3 pinned scope -- generator ABORTS on drift (re-measure before overriding).
# REFLUSH = 12: the 8 hot-region pepper cells + chives 1 + mint 3 (harvest-only
# doubling is the same structural pattern; all exempt, zero ops either way).
# TWO_CROP = 94 includes broad-beans-fava's 4 shared-harvest cells (§2 B-fava).
EXPECT = {"TWO_CROP": 94, "ALT_WINDOW": 11, "REFLUSH": 12}
POP1_CELLS, POP2_CELLS = 64, 94
# spec §2 B-fava (Trevor 2026-07-09): a true two-sowing crop whose fall sowing
# overwinters into the SAME spring harvest window (authored in calendar[] +
# zone_notes). Its plant-doubled/harvest-single cells are TWO_CROP, not
# ALT_WINDOW, and the extracted second_planting carries the shared window.
SHARED_HARVEST_SLUGS = {"broad-beans-fava"}
PLANTING = ("start_indoors", "plant_out")
FIELDS = ("start_indoors", "plant_out", "harvest")
# pop-1 legacy crops (dedup lane); everything else with second_planting = pop-2
POP1_SLUGS = {"beefsteak-tomato", "broccoli", "cherry-tomato", "grape-tomato",
              "heirloom-tomato", "kohlrabi", "roma-tomato"}


def _cells(crop):
    for rk, region in (crop.get("regions") or {}).items():
        if not isinstance(region, dict):
            continue
        for z, cell in (region.get("resolved_by_zone") or {}).items():
            if isinstance(cell, dict):
                yield rk, z, cell


def _path(slug, rk, z, key):
    return f"$.crops[?(@.slug=='{slug}')].regions.{rk}.resolved_by_zone.{z}.{key}"


def _start_key(sp):
    return (sp.start_month, sp.start_day or 1)


def classify(cell):
    """Pattern of a NO-second_planting cell (spec §2/§3); None = single-window."""
    n = {f: window_count(cell.get(f)) for f in FIELDS}
    if max(n.values()) < 2:
        return None
    plant_multi = n["plant_out"] >= 2 or n["start_indoors"] >= 2
    if plant_multi and n["harvest"] >= 2:
        return "TWO_CROP"
    if n["harvest"] >= 2:
        return "REFLUSH"
    return "ALT_WINDOW"


def second_planting_value(cell, shared_harvest=False):
    """Spec §5: the second spans, provenance inherited, granularity preserved.
    shared_harvest (spec §2 B-fava): harvest has ONE span shared by both sowings;
    the fall crop overwinters into it, so it becomes the second_planting's window."""
    po, hv = spans(cell.get("plant_out")), spans(cell.get("harvest"))
    si = spans(cell.get("start_indoors"))
    assert len(po) == 2, f"TWO_CROP cell needs exactly 2 plant_out spans: {po}"
    assert len(si) in (0, 1, 2), f"unexpected start_indoors span count: {si}"
    assert _start_key(po[0]) < _start_key(po[1]), f"plant_out not spring-first: {po}"
    if shared_harvest:
        assert len(hv) == 1, f"shared-harvest cell needs exactly 1 harvest span: {hv}"
        h2 = hv[0]
    else:
        assert len(hv) == 2, f"TWO_CROP cell needs exactly 2 harvest spans: {hv}"
        assert _start_key(hv[0]) < _start_key(hv[1]), f"harvest not spring-first: {hv}"
        # the fall planting must precede its harvest (harvest may wrap into Jan)
        assert po[1].start_month <= hv[1].start_month or hv[1].start_month <= 2, \
            f"fall plant does not precede fall harvest: {po[1]} vs {hv[1]}"
        h2 = hv[1]
    return {
        "start_indoors": si[1].raw if len(si) == 2 else None,
        "plant_out": po[1].raw,
        "harvest_start": h2.start_text,
        "harvest_end": h2.end_text,
        "sources": cell.get("sources"),
        "anchoring_urls": cell.get("anchoring_urls"),
    }


def or_norm_ops(slug, rk, z, cell):
    """ALT_WINDOW cells: comma -> ' or ' (spec §2 B-alt); onion ca_north_coast
    plant_out gets the zone_notes-backed continuity merge (§2 B-fix)."""
    ops = []
    for f in PLANTING:
        val = cell.get(f)
        if window_count(val) < 2:
            continue
        if slug == "onion" and rk == "ca_north_coast" and f == "plant_out":
            new = "Nov - March"
        else:
            new = " or ".join(p.strip() for p in val.split(","))
        ops.append({"op": "replace", "json_path": _path(slug, rk, z, f),
                    "from": val, "value": new})
    return ops


def clean_ops(slug, rk, z, cell):
    """Stage-3 ops for ONE second_planting cell: window strings -> PRIMARY span;
    envelope narrowed to primary (spec §2 Decision C).

    The primary is the span that does NOT overlap the second_planting counterpart
    -- NEVER blindly s[0]: pop-1 hot-region cells are fall-span-FIRST (broccoli
    ca_interior z9 plant_out "Aug 1 - Sep 30, Dec 1 - Feb 28" -- the Dec window is
    the primary). Overlap is month-granular (never byte-equality: pop-1 harvest
    strings are month-granular vs day-granular sp values). Envelope checks mirror
    gate Rule A's CONTAINMENT formulation, so fava's shared harvest window no-ops."""
    sp = cell["second_planting"]
    ops = []

    def rep(key, frm, val):
        ops.append({"op": "replace", "json_path": _path(slug, rk, z, key),
                    "from": frm, "value": val})

    primary = {}
    for f in FIELDS:
        s = spans(cell.get(f))
        if not s:
            continue
        if len(s) == 1:
            primary[f] = s[0]
            continue
        assert len(s) == 2, f"3+ spans unexpected: {slug} {rk}.{z} {f}"
        if f == "harvest":
            ref = (f"{sp['harvest_start']} - {sp['harvest_end']}"
                   if sp.get("harvest_start") else None)
        else:
            ref = sp.get(f)
        assert ref, f"doubled {f} but second_planting has no counterpart: {slug} {rk}.{z}"
        refspan = spans(ref)[0]
        ov = [i for i, x in enumerate(s) if months_overlap(x, refspan)]
        assert len(ov) == 1, \
            f"ambiguous fall-span match: {slug} {rk}.{z} {f} spans={s} ref={refspan} ov={ov}"
        keep = s[1 - ov[0]]
        primary[f] = keep
        rep(f, cell[f], keep.raw)

    # envelope: narrowed to the primary window wherever it falls OUTSIDE it
    # (containment, mirroring gate Rule A; handles fall-first primaries + fava)
    po1, hv1 = primary.get("plant_out"), primary.get("harvest")
    lpd = single_date(cell.get("last_plant_date"))
    if lpd and po1 and not in_span(lpd, po1):
        rep("last_plant_date", cell["last_plant_date"], po1.end_text)
    fpd = single_date(cell.get("first_plant_date"))
    if fpd and po1 and not in_span(fpd, po1):
        rep("first_plant_date", cell["first_plant_date"], po1.start_text)
    he = single_date(cell.get("harvest_end"))
    if he and hv1 and not in_span(he, hv1):
        rep("harvest_end", cell["harvest_end"], hv1.end_text)
    hs = single_date(cell.get("harvest_start"))
    if hs and hv1 and not in_span(hs, hv1):
        rep("harvest_start", cell["harvest_start"], hv1.start_text)
    return ops


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=["populate", "clean"])
    ap.add_argument("--only", help="emit just one batch name")
    ap.add_argument("--base", default=CANON)
    a = ap.parse_args()
    raw = open(a.base, "rb").read()
    base_sha = hashlib.sha256(raw).hexdigest()
    data = json.loads(raw.decode("utf-8"))
    crops = data["crops"] if isinstance(data, dict) and "crops" in data else data

    batches = {}
    if a.stage == "populate":
        counts = {"TWO_CROP": 0, "ALT_WINDOW": 0, "REFLUSH": 0}
        migrated = 0
        slug_batch = {s: b for b, ss in S1_BATCHES.items() for s in ss}
        for crop in crops:
            slug = crop.get("slug")
            if (crop.get("succession_policy") or {}).get("suitable") is not False:
                continue
            for rk, z, cell in _cells(crop):
                if isinstance(cell.get("second_planting"), dict):
                    if slug not in POP1_SLUGS:
                        migrated += 1
                    continue
                pat = classify(cell)
                if pat is None:
                    continue
                shared = slug in SHARED_HARVEST_SLUGS
                if pat == "ALT_WINDOW" and shared:
                    pat = "TWO_CROP"  # §2 B-fava ruling
                counts[pat] += 1
                if pat == "TWO_CROP":
                    b = slug_batch[slug]  # KeyError = unexpected crop -> abort
                    batches.setdefault(b, []).append(
                        {"op": "add", "json_path": _path(slug, rk, z, "second_planting"),
                         "value": second_planting_value(cell, shared_harvest=shared)})
                elif pat == "ALT_WINDOW":
                    batches.setdefault("s1_b3_rest", []).extend(
                        or_norm_ops(slug, rk, z, cell))
        # TWO_CROP is pinned as remaining+migrated so sequential per-batch
        # regeneration against the moving canonical passes across the whole
        # B1->B2->B3 sequence; ALT_WINDOW/REFLUSH pins hold through the whole
        # populate stage because the or-norm ops land in the LAST batch
        # (s1_b3) and REFLUSH is never touched. (ALT_WINDOW would read 0
        # only if populate were re-run after S1-B3's promote, which the
        # workflow never does; if that ever changes, make ALT batch-aware
        # the same way.)
        assert (counts["TWO_CROP"] + migrated == EXPECT["TWO_CROP"]
                and counts["ALT_WINDOW"] == EXPECT["ALT_WINDOW"]
                and counts["REFLUSH"] == EXPECT["REFLUSH"]), \
            f"scope drift vs spec: {counts} + migrated={migrated} != {EXPECT}"
    else:  # clean
        n1 = n2 = 0
        for crop in crops:
            slug = crop.get("slug")
            for rk, z, cell in _cells(crop):
                if not isinstance(cell.get("second_planting"), dict):
                    continue
                name = "s3_b1_pop1_dedup" if slug in POP1_SLUGS else "s3_b2_pop2_clean"
                if slug in POP1_SLUGS:
                    n1 += 1
                else:
                    n2 += 1
                ops = clean_ops(slug, rk, z, cell)
                if ops:
                    batches.setdefault(name, []).extend(ops)
        assert n1 == POP1_CELLS and n2 == POP2_CELLS, \
            f"cell-count drift: pop1={n1} pop2={n2}"

    for name, ops in sorted(batches.items()):
        if a.only and name != a.only:
            continue
        out = os.path.join(HERE, "batches", f"second_planting_{name}.json")
        with open(out, "w", encoding="utf-8") as fh:
            json.dump({"base_sha": base_sha, "patches": ops}, fh, indent=1,
                      ensure_ascii=False)
        print(f"wrote {out}: {len(ops)} ops")


if __name__ == "__main__":
    main()
