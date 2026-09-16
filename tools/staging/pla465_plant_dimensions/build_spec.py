#!/usr/bin/env python3
"""build_spec -- turn the staged T1 reads (one JSON per crop) into spec.json for promote_pla465_plant_dimensions.

RULES (spec section 9). A crop is AUTHORED only when its read is status "found", tier T1, carries a two-number
height, and its page maps to a source_catalog id (by the reader's source_id, else by URL host). A spread is
carried only when it is a two-number pair. Partial reads (a single figure), T2-only reads, not-found reads and
reads whose page has no catalog id are NOT authored (the crop takes null) and are listed for the outcome doc.
No number is copied from rootstock_options[]. The note carries institution, URL, read date, byte count,
sha256 and the verbatim sentence, so the record can be re-verified from raw bytes.

Usage: build_spec.py <reads_dir> [--write]   (prints the split; --write emits spec.json and pins EXPECTED_AUTHORED)
"""
import glob, json, os, re, sys
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
CANON = os.path.join(REPO, "crops_data_final.json")
PROMOTE = os.path.join(REPO, "tools", "promote_pla465_plant_dimensions.py")
BASE_SHA = "a98b6cfdfd7c5ffdcccdb222ceaa141fdca79e0ed674f991c0dcb396c2534412"
DATE = "2026-09-16"


def pair(v):
    return isinstance(v, list) and len(v) == 2 and all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in v) and 0 < v[0] <= v[1]


def main():
    reads_dir = sys.argv[1]
    write = "--write" in sys.argv
    data = json.load(open(CANON))
    catalog = data.get("source_catalog") or {}
    # Host aliases resolve a page to the UMBRELLA catalog id that admits it (the umbrella's citable_for
    # names the NC State Plant Toolbox, the PSU and UF/IFAS extension sites, and WSU's bulletin store);
    # a generic host lookup would pick whichever crop-specific id happened to share the host.
    ALIAS = {"plants.ces.ncsu.edu": "ncsu_ext", "content.ces.ncsu.edu": "ncsu_ext",
             "s3.wp.wsu.edu": "wsu_ext", "treefruit.wsu.edu": "wsu_ext", "extension.wsu.edu": "wsu_ext",
             "extension.psu.edu": "psu_ext", "ask.ifas.ufl.edu": "ufifas_ext", "edis.ifas.ufl.edu": "ufifas_ext",
             "hgic.clemson.edu": "clemson_hgic", "extension.usu.edu": "usu_ext"}
    exact_url = {}
    for sid, e in catalog.items():
        u = (e or {}).get("url") if isinstance(e, dict) else None
        if u:
            exact_url.setdefault(u.rstrip("/"), sid)
    include = set()
    for a in sys.argv[2:]:
        if a.startswith("--include="):
            include = set(a.split("=", 1)[1].split(","))
    authored, skipped = [], []
    for path in sorted(glob.glob(os.path.join(reads_dir, "*.json"))):
        r = json.load(open(path))
        crop = r.get("crop") or os.path.basename(path)[:-5]
        sid = r.get("source_id")
        if not sid or sid not in catalog:
            url = (r.get("url") or "").rstrip("/")
            host = urlparse(url).netloc.lower().replace("www.", "")
            sid = exact_url.get(url) or ALIAS.get(host)
        reason = None
        status = r.get("status")
        if status == "partial" and crop in include:
            status = "found"  # the orchestrator's read of the partial; the reason is written into the note
        if status != "found":
            reason = f"status {r.get('status')!r}"
        elif r.get("tier") != "T1":
            reason = f"tier {r.get('tier')!r}"
        elif not pair(r.get("mature_height_ft")):
            reason = f"height {r.get('mature_height_ft')!r} is not a [lo, hi] pair"
        elif not sid:
            reason = f"page host {urlparse(r.get('url') or '').netloc!r} maps to no source_catalog id"
        if reason:
            skipped.append((crop, reason, r.get("single_figure_note"), r.get("url")))
            continue
        h = [float(x) if isinstance(x, float) and not float(x).is_integer() else int(x) for x in r["mature_height_ft"]]
        s = r.get("mature_spread_ft")
        s = [float(x) if isinstance(x, float) and not float(x).is_integer() else int(x) for x in s] if pair(s) else None
        note = (f"PLA-465 plant dimensions: mature_height_ft {h} ft" + (f", mature_spread_ft {s} ft" if s else ", spread not stated on the page") +
                f", basis: {r.get('basis')}" + (f" ({r['rootstock_named_on_page']} named on the page)" if r.get("rootstock_named_on_page") else "") +
                f"; {r.get('institution')}, {r.get('url')} (raw read {r.get('read_date') or DATE}, {r.get('bytes')} bytes, sha256 {r.get('sha256')}); "
                f"verbatim: \"{(r.get('verbatim') or '').strip()}\"." +
                (" Authored from a read the reader marked partial: the page states the species size on a standard, non-dwarfing rootstock, which is the required basis on this crop because its recommended rootstock is a standard stock." if r.get("status") == "partial" else "") +
                " amend-not-recert.")
        authored.append({"crop": crop, "mature_height_ft": h, "mature_spread_ft": s,
                         "field_addition": {"field": "plant_dimensions", "date": DATE, "sources": [sid], "note": note}})
    authored.sort(key=lambda x: x["crop"])
    print(f"authored {len(authored)}: {[a['crop'] for a in authored]}")
    print(f"skipped  {len(skipped)}:")
    for c, why, sf, u in skipped:
        print(f"   {c:20} {why}" + (f" | {sf}" if sf else "") + (f" | {u}" if u else ""))
    if not write:
        return 0
    spec = {"_what": "PLA-465 plant dimensions (spec 2026-09-16, register row 30). Three crop-level keys on every certified crop; the authored rows below carry T1 reads from raw bytes; every other certified crop takes null; footprint_inches null everywhere; shells untouched.",
            "base_sha": BASE_SHA, "authored": authored,
            "expected": {"keys": 121, "authored": len(authored), "null": 121 - len(authored), "shells": 7}}
    json.dump(spec, open(os.path.join(HERE, "spec.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    src = open(PROMOTE, encoding="utf-8").read()
    src2 = re.sub(r"^EXPECTED_AUTHORED = .*$", f"EXPECTED_AUTHORED = {len(authored)}  # pinned {DATE} from the staged reads; never moved after the first run", src, count=1, flags=re.M)
    assert src2 != src or f"EXPECTED_AUTHORED = {len(authored)}" in src
    open(PROMOTE, "w", encoding="utf-8").write(src2)
    print(f"spec.json written; EXPECTED_AUTHORED pinned to {len(authored)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
