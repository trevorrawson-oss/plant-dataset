#!/usr/bin/env python3
"""Build tools/staging/pla580_plants_per_pot/spec.json for the PLA-580 promote.

EVERY VALUE IS DERIVED FROM THE SOURCE BYTES, never hand-typed: this script parses the Illinois
table and the UMD size-class sentence out of the fetched HTML, turns each count phrase into
`count: [min, max]` and each container-size cell into `at_gallons: [lo, hi]`, and writes the
verbatim row it read into the field_additions note beside the URL, byte count and sha256.

THE PARSE IS NOT ITS OWN CHECK. An expectation computed from the thing it validates is vacuous, so
the promote carries `EXPECTED_READINGS` as independent LITERALS and refuses any spec row that does
not match. This script derives; the promote verifies. Run this, read the printed table against the
source page, then let the promote's literals bite.

Usage:
    build_spec.py                 # use the cached raw bytes if present, else fetch
    build_spec.py --fetch         # always re-fetch
"""
import argparse, hashlib, json, os, re, sys, urllib.request, urllib.error
import html as _html

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "spec.json")
CACHE = os.path.join(HERE, "_raw")

BASE_SHA = "079e3923660a53189bcf5e0bee0506e78225e473b2dadcba54cbfb3045337696"
FETCH_DATE = "2026-09-21"

# MEASURED 2026-09-21 by this session, twice, under two different user-agents (a WAF block reads as
# absence under one and not the other, and a status code is not liveness). Both digests also
# reproduce the ones recorded in the spec's section 12 exactly, which is a re-measurement rather
# than a copy. A fetch whose digest is not one of these REFUSES: the shape of a hash field pulls a
# fabricated digest out of you, so nothing here is written from memory.
SOURCES = {
    "uiuc_ext": {
        "url": "https://extension.illinois.edu/container-gardens/growing-vegetables-containers",
        "bytes": 28754,
        "sha256": "f9f336d5eb33a1dc0833f53d98b2e909cf2d6ce920795dc8913fab94de393119",
        "institution": "University of Illinois Extension",
    },
    "umd_ext": {
        "url": "https://extension.umd.edu/resource/types-containers-growing-vegetables",
        "bytes": 34659,
        "sha256": "96521c5d0cf8860e7895a8c6da426ac48a372894c531431c64666bda8151f407",
        "institution": "University of Maryland Extension",
    },
}

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

# Ruling 5 (spec 2.6). A row that names several slugs is HELD; a row that names none is UNAUTHORED.
# The held rows are recorded here BY NAME so the hold is a decision in the artifact, not an omission.
IL_SLUG = {
    "parsley": "parsley",
    "cabbages": "cabbage",
    "green beans": "green-beans-bush",
    "leaf lettuce": "lettuce-leaf",
    "Swiss chard": "swiss-chard",
    "cherry and patio tomatoes": "cherry-tomato",
    "eggplant": "eggplant",
}
IL_HELD = {
    "cucumbers": "names cucumber, english-cucumber, pickling-cucumber and slicing-cucumber",
    "pepper": "names bell-pepper and four more, spanning sweet and hot",
}
IL_UNAUTHORED = {"Standard tomatoes": "names no slug; grape-/roma-/beefsteak-/heirloom- are separate crops"}

GALLONS = {"half-gallon": [0.5, 0.5], "one gallon": [1, 1], "two gallon": [2, 2], "three gallon": [3, 3]}
COUNT_RE = re.compile(r"^(\d+)(?:\s*-\s*(\d+))?\s+plants?$")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
    with urllib.request.urlopen(req, timeout=45) as r:
        if r.status != 200:
            raise SystemExit(f"REFUSED: {url} returned {r.status}")
        return r.read()


def raw(key, force):
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, key + ".html")
    if force or not os.path.exists(p):
        body = fetch(SOURCES[key]["url"])
        with open(p, "wb") as f:
            f.write(body)
    with open(p, "rb") as f:
        body = f.read()
    got, want = hashlib.sha256(body).hexdigest(), SOURCES[key]["sha256"]
    if got != want or len(body) != SOURCES[key]["bytes"]:
        raise SystemExit(f"REFUSED: {key} is {len(body)} bytes / {got[:16]}..., pinned "
                         f"{SOURCES[key]['bytes']} / {want[:16]}... The page MOVED; re-read it "
                         f"before re-pinning, and do not re-pin to make this pass.")
    return body.decode("utf-8", "replace")


def text_of(fragment):
    return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def illinois_rows(doc):
    tables = re.findall(r"<table.*?</table>", doc, re.S | re.I)
    if len(tables) != 1:
        raise SystemExit(f"REFUSED: expected exactly 1 table on the Illinois page, found {len(tables)}")
    rows = []
    for tr in re.findall(r"<tr.*?</tr>", tables[0], re.S | re.I):
        cells = [text_of(c) for c in re.findall(r"<t[dh].*?</t[dh]>", tr, re.S | re.I)]
        if len(cells) >= 3 and cells[0] != "Container Size":
            rows.append(cells[:3])
    if len(rows) != 14:
        raise SystemExit(f"REFUSED: expected 14 Illinois data rows, parsed {len(rows)}")
    return rows


def parse_count(phrase):
    """'1 plant' -> [1,1]; '2-3 plants' -> [2,3]; a thinning spacing -> None (not a capacity)."""
    m = COUNT_RE.match(phrase.strip())
    if not m:
        return None
    lo = int(m.group(1))
    return [lo, int(m.group(2)) if m.group(2) else lo]


def parse_gallons(cell):
    key = cell.lower().replace(" containers", "").replace(" container", "").strip()
    if key not in GALLONS:
        raise SystemExit(f"REFUSED: unrecognised container size cell {cell!r}")
    return list(GALLONS[key])


def anchor(key):
    return {key: {"url": SOURCES[key]["url"], "verified": FETCH_DATE}}


def note(key, verbatim, count, gallons, extra=""):
    s = SOURCES[key]
    return (f"PLA-580 plants_per_pot: count {count}, at_gallons {gallons}. "
            f"{s['institution']}, {s['url']} (raw read {FETCH_DATE}, {s['bytes']} bytes, "
            f"sha256 {s['sha256']}); verbatim: \"{verbatim}\".{(' ' + extra) if extra else ''} "
            f"The count is a capacity AT THE STATED POT SIZE, not a per-plant volume and not bound "
            f"to min_pot_gallons. amend-not-recert.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    args = ap.parse_args()

    il = raw("uiuc_ext", args.fetch)
    umd = raw("umd_ext", args.fetch)

    readings = {}          # slug -> list of readings
    records = {}           # slug -> list of field_addition records
    ledger = []            # every Illinois row and what became of it

    for size_cell, plant_cell, spacing_cell in illinois_rows(il):
        count = parse_count(spacing_cell)
        verbatim = f"{size_cell} | {plant_cell} | {spacing_cell}"
        if count is None:
            ledger.append((plant_cell, "NO COUNT", f"a thinning spacing ({spacing_cell!r}) is not a capacity"))
            continue
        if plant_cell in IL_HELD:
            ledger.append((plant_cell, "HELD (ruling 5)", IL_HELD[plant_cell]))
            continue
        if plant_cell in IL_UNAUTHORED:
            ledger.append((plant_cell, "UNAUTHORED (ruling 5)", IL_UNAUTHORED[plant_cell]))
            continue
        slug = IL_SLUG.get(plant_cell)
        if slug is None:
            raise SystemExit(f"REFUSED: Illinois row {plant_cell!r} carries a count and is neither "
                             f"mapped, held nor unauthored. Rule it before authoring.")
        gallons = parse_gallons(size_cell)
        readings.setdefault(slug, []).append(
            {"count": count, "at_gallons": gallons, "sources": ["uiuc_ext"],
             "anchoring_urls": anchor("uiuc_ext")})
        records.setdefault(slug, []).append(
            {"field": "plants_per_pot", "date": FETCH_DATE, "sources": ["uiuc_ext"],
             "note": note("uiuc_ext", verbatim, count, gallons,
                          "One table, 14 data rows; 10 carry a count and 4 give a thinning "
                          "spacing instead. The container size is stated per row and varies "
                          "across four values.")})
        ledger.append((plant_cell, f"AUTHORED -> {slug}", f"count {count} at {gallons} gal"))

    # UMD: a SIZE-CLASS count, one count over five named groups. Only 'eggplant' maps 1:1; the other
    # four group names are ambiguous on ruling 5's rule and are HELD. The Medium and Small classes
    # carry a volume and a depth but NO count, so they yield no reading.
    flat = re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", umd)))
    m = re.search(r"For Large Vegetables[^.]*\. Minimum ([\d]+)-([\d]+) gallons of growing media,"
                  r" with a depth of [\d-]+ inches Examples: ([^,]+(?:, [^,]+)*?), Medium", flat)
    if not m:
        raise SystemExit("REFUSED: the UMD Large Vegetables sentence did not parse; re-read the page")
    umd_gallons = [int(m.group(1)), int(m.group(2))]
    umd_groups = [g.strip() for g in m.group(3).split(",")]
    umd_verbatim = flat[m.start():m.start() + len(m.group(0)) - len(", Medium")]
    if "one plant per container" not in umd_verbatim:
        raise SystemExit("REFUSED: the UMD sentence no longer states one plant per container")
    umd_count = [1, 1]
    UMD_SLUG = {"eggplant": "eggplant"}
    for g in umd_groups:
        slug = UMD_SLUG.get(g)
        if slug is None:
            ledger.append((f"UMD {g}", "HELD (ruling 5)", "a category name, not a crop name"))
            continue
        readings.setdefault(slug, []).append(
            {"count": umd_count, "at_gallons": umd_gallons, "sources": ["umd_ext"],
             "anchoring_urls": anchor("umd_ext")})
        records.setdefault(slug, []).append(
            {"field": "plants_per_pot", "date": FETCH_DATE, "sources": ["umd_ext"],
             "note": note("umd_ext", umd_verbatim, umd_count, umd_gallons,
                          "A SIZE-CLASS count: one count, one size band, five named crop groups, of "
                          "which only eggplant names a single slug. The Medium and Small classes on "
                          "the same page carry a volume and a depth but no count, and the Medium "
                          "class names dwarf eggplant with no count, so neither yields a reading. "
                          "This is the only genuinely banded size in either source.")})
        ledger.append((f"UMD {g}", f"AUTHORED -> {slug}", f"count {umd_count} at {umd_gallons} gal"))

    authored = sorted(readings)
    spec = {
        "_what": ("PLA-580 container_notes.plants_per_pot, register row 31. Derived from the source "
                  "bytes by build_spec.py; the promote verifies every value against its own "
                  "independent literals (EXPECTED_READINGS). Held and unauthored rows are recorded "
                  "in source_ledger so a hold is a decision, not an omission."),
        "base_sha": BASE_SHA,
        "fetch_date": FETCH_DATE,
        "sources": SOURCES,
        "authored": [{"crop": s, "readings": readings[s], "field_additions": records[s]}
                     for s in authored],
        "source_ledger": [{"source_row": a, "outcome": b, "why": c} for a, b, c in ledger],
        "expected": {
            "keys": 121,
            "authored_crops": len(authored),
            "readings": sum(len(readings[s]) for s in authored),
            "null": 121 - len(authored),
            "shells": 7,
        },
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2, ensure_ascii=False, sort_keys=False)
        f.write("\n")

    print(f"wrote {OUT}")
    print(f"\n{'source row':34} {'outcome':28} why")
    for a, b, c in ledger:
        print(f"  {a:32} {b:28} {c}")
    print(f"\nauthored {len(authored)} crops / {spec['expected']['readings']} readings:")
    for s in authored:
        for r in readings[s]:
            print(f"  {s:20} count {r['count']} at_gallons {r['at_gallons']}  <- {r['sources'][0]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
