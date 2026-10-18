#!/usr/bin/env python3
"""sowing_heat_ceiling_gate -- validates register #35, `sowing_heat_ceiling` (PLA-750).

Contract: docs/sowing_heat_ceiling_contract.md. The field is the forecast daily HIGH at or above which the
app holds a succession sowing; `heat_threshold_f` stays the mature-plant alert number and is not read here.

States: key absent = TODO; `temp_f` int = held; `temp_f` null = reviewed, no hold (sourced, with a note).

Checks:
  SHAPE   object; exact key sets per state; temp_f int in TEMP_RANGE; measures / basis enums; claim a
          non-empty string; claim_source (and temp_source, if any) in sources; sources == anchoring_urls ids,
          no duplicates, each in source_catalog; anchors document-scoped with a `verified` date; soil rows
          and nulls carry a non-empty note.
  PAUSE   succession_policy.pause_in_heat is true EXACTLY when temp_f is an int; a crop with
          pause_in_heat true and no field is a hold with no reviewed reason.
  BYTES   (with --evidence) claim verbatim in the RAW hashed bytes at anchoring_urls[claim_source] (MANIFEST-
          listed, never the tag-stripped doc cache: PLA-768); temp_f in the claim (or its degC rounding), or,
          with a temp_source, stated with a degree unit in that page's bytes; every double-quoted note span of
          12+ characters in the bytes of one of the field's anchored pages.
  POPULATION  reports the crops it inspected; REFUSES (exit 2) below --floor (default POPULATION_FLOOR).

Usage:
  sowing_heat_ceiling_gate.py [PATH] [--evidence DIR] [--floor N]
Exit: 0 PASS, 1 violations, 2 REFUSED (population below the floor).
"""
import csv
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cited_promote_common import norm_text, pdf_text, sha256_bytes  # noqa: E402

FIELD = "sowing_heat_ceiling"
MEASURES = {"air", "soil"}
BASES = {"sowing_statement", "germination", "bolting", "maturity_coupled"}
TEMP_RANGE = (60, 100)
POPULATION_FLOOR = 30          # the PLA-750 pilot's 30 reviewed crops
HELD_REQUIRED = {"temp_f", "measures", "basis", "claim", "claim_source", "sources", "anchoring_urls"}
HELD_OPTIONAL = {"temp_source", "note"}
NULL_KEYS = {"temp_f", "note", "sources", "anchoring_urls"}
VERIFIED = re.compile(r"\d{4}-\d{2}-\d{2}\Z")
BARE_HOST = re.compile(r"https?://[^/]+/?\Z")
QUOTED = re.compile(r'"([^"]{12,})"|“([^”]{12,})”')


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _slug(c):
    return c.get("slug") or c.get("id")


def _pause(c):
    return (c.get("succession_policy") or {}).get("pause_in_heat") is True


def check_crop(c, catalog):
    """SHAPE + PAUSE violations for one crop (empty == clean)."""
    slug = _slug(c)
    if FIELD not in c:
        if _pause(c):
            return [f"{slug}: succession_policy.pause_in_heat is true but {FIELD} is absent "
                    f"(a hold with no reviewed reason)"]
        return []
    f = c[FIELD]
    if not isinstance(f, dict):
        return [f"{slug}: {FIELD} must be an object, got {type(f).__name__}"]
    v = []
    t = f.get("temp_f")
    held = _is_int(t)
    if "temp_f" in f and t is not None and not held:
        v.append(f"{slug}: {FIELD}.temp_f {t!r} is not an int or null")
    elif held and not (TEMP_RANGE[0] <= t <= TEMP_RANGE[1]):
        v.append(f"{slug}: {FIELD}.temp_f {t} out of range {TEMP_RANGE}")
    keys = set(f)
    if held:
        if not (HELD_REQUIRED <= keys <= HELD_REQUIRED | HELD_OPTIONAL):
            v.append(f"{slug}: {FIELD} held keys {sorted(keys)} (required {sorted(HELD_REQUIRED)}, "
                     f"optional {sorted(HELD_OPTIONAL)})")
        if f.get("measures") not in MEASURES:
            v.append(f"{slug}: {FIELD}.measures {f.get('measures')!r} not in {sorted(MEASURES)}")
        if f.get("basis") not in BASES:
            v.append(f"{slug}: {FIELD}.basis {f.get('basis')!r} not in {sorted(BASES)}")
        if not (isinstance(f.get("claim"), str) and f["claim"].strip()):
            v.append(f"{slug}: {FIELD}.claim must be a non-empty string")
        if f.get("measures") == "soil" and not (isinstance(f.get("note"), str) and f["note"].strip()):
            v.append(f"{slug}: {FIELD} soil row needs a note recording the air-for-soil proxy (D2)")
        if "note" in f and not (isinstance(f["note"], str) and f["note"].strip()):
            v.append(f"{slug}: {FIELD}.note must be a non-empty string when present")
    elif t is None and "temp_f" in f:
        if keys != NULL_KEYS:
            v.append(f"{slug}: {FIELD} null-state keys {sorted(keys)} != {sorted(NULL_KEYS)}")
        if not (isinstance(f.get("note"), str) and f["note"].strip()):
            v.append(f"{slug}: {FIELD} null state needs a note saying why there is no hold")
    elif "temp_f" not in f:
        v.append(f"{slug}: {FIELD} keys {sorted(keys)} carry no temp_f")
    # citations
    srcs, anc = f.get("sources"), f.get("anchoring_urls")
    if not (isinstance(srcs, list) and srcs and all(isinstance(s, str) for s in srcs)):
        v.append(f"{slug}: {FIELD}.sources must be a non-empty list of ids")
        srcs = [s for s in srcs or [] if isinstance(s, str)] if isinstance(srcs, list) else []
    if len(srcs) != len(set(srcs)):
        v.append(f"{slug}: {FIELD}.sources lists an id twice")
    if not isinstance(anc, dict):
        v.append(f"{slug}: {FIELD}.anchoring_urls must be an object")
        anc = {}
    if set(srcs) != set(anc):
        v.append(f"{slug}: {FIELD} sources and anchoring_urls ids differ: {sorted(set(srcs) ^ set(anc))}")
    for sid in sorted(set(srcs) | set(anc)):
        if sid not in catalog:
            v.append(f"{slug}: {FIELD} source {sid} is not in source_catalog")
    for sid, a in sorted(anc.items()):
        url = a.get("url") if isinstance(a, dict) else None
        if not (isinstance(url, str) and url.startswith("http")) or BARE_HOST.match(url or ""):
            v.append(f"{slug}: {FIELD} anchor {sid} must be a document-scoped url, got {url!r}")
        if not (isinstance(a, dict) and VERIFIED.match(str(a.get("verified", "")))):
            v.append(f"{slug}: {FIELD} anchor {sid} has no verified date")
    if held:
        if f.get("claim_source") not in srcs:
            v.append(f"{slug}: {FIELD}.claim_source {f.get('claim_source')!r} is not in sources")
        if "temp_source" in f and (f["temp_source"] not in srcs or f["temp_source"] == f.get("claim_source")):
            v.append(f"{slug}: {FIELD}.temp_source {f['temp_source']!r} must be in sources and differ from "
                     f"claim_source")
    # the invariant
    if held != _pause(c):
        v.append(f"{slug}: succession_policy.pause_in_heat is {_pause(c)} but {FIELD}.temp_f is {t!r} "
                 f"(pause_in_heat must be true exactly when temp_f is an int)")
    return v


# ---------------------------------------------------------------- bytes
def load_manifest(evidence_dir):
    """url -> [sha256, ...] from MANIFEST.tsv."""
    out = {}
    with open(os.path.join(evidence_dir, "MANIFEST.tsv"), encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            out.setdefault(r["url"], []).append(r["sha256"])
    return out


def _page_texts(url, man, evidence_dir, cache):
    """[(sha, normalized text)] for every hashed copy of url; raises ValueError on a broken cache file."""
    out = []
    for sha in man.get(url, []):
        if sha not in cache:
            files = glob.glob(os.path.join(evidence_dir, sha + ".*"))
            if len(files) != 1:
                raise ValueError(f"{len(files)} cache files for {sha[:12]}")
            raw = open(files[0], "rb").read()
            if sha256_bytes(raw) != sha:
                raise ValueError(f"the cached bytes for {url} hash to {sha256_bytes(raw)[:12]}, not {sha[:12]}")
            cache[sha] = norm_text(pdf_text(raw) if files[0].endswith(".pdf") else raw.decode("utf-8", "replace"))
        out.append((sha, cache[sha]))
    return out


def _celsius(t):
    return round((t - 32) * 5 / 9)


def check_bytes(c, man, evidence_dir, cache):
    """BYTES violations for one crop carrying a well-shaped field (call after check_crop is clean)."""
    if FIELD not in c or not isinstance(c[FIELD], dict):
        return []
    slug, f = _slug(c), c[FIELD]
    anc = f.get("anchoring_urls") or {}
    v, texts = [], {}
    for sid, a in anc.items():
        url = (a or {}).get("url")
        try:
            got = _page_texts(url, man, evidence_dir, cache)
        except ValueError as e:
            v.append(f"{slug}: {FIELD} anchor {sid}: {e}")
            continue
        if not got:
            v.append(f"{slug}: {FIELD} anchor {sid} ({url}) has no MANIFEST-listed bytes")
        texts[sid] = [t for _sha, t in got]
    t = f.get("temp_f")
    if _is_int(t):
        claim = norm_text(f.get("claim") or "")
        pages = texts.get(f.get("claim_source"), [])
        if pages and not any(claim and claim in p for p in pages):
            v.append(f"{slug}: {FIELD}.claim is not in the hashed bytes of {f.get('claim_source')}: "
                     f"{f.get('claim', '')[:70]!r}")
        if "temp_source" not in f:
            c_ok = re.search(rf"\b{_celsius(t)}\s*[°º˚]\s*c\b", claim)
            if not re.search(rf"\b{t}\b", claim) and not c_ok:
                v.append(f"{slug}: {FIELD}.temp_f {t} is not in the claim (nor its degC rounding {_celsius(t)})")
        else:
            unit = re.compile(rf"\b{t}\s*(?:[°º˚]\s*f|degrees)", re.I)
            tp = texts.get(f["temp_source"], [])
            if tp and not any(unit.search(p) for p in tp):
                v.append(f"{slug}: {FIELD}.temp_f {t} is not stated with a degree unit in the hashed bytes of "
                         f"{f['temp_source']}")
    allp = [p for ps in texts.values() for p in ps]
    for m in QUOTED.finditer(f.get("note") or ""):
        q = norm_text(m.group(1) or m.group(2))
        if allp and not any(q in p for p in allp):
            v.append(f"{slug}: {FIELD} note quote is not in the hashed bytes of any anchored page: {q[:70]!r}")
    return v


def coverage(crops):
    held = [_slug(c) for c in crops if isinstance(c.get(FIELD), dict) and _is_int(c[FIELD].get("temp_f"))]
    nulls = [_slug(c) for c in crops if isinstance(c.get(FIELD), dict) and c[FIELD].get("temp_f") is None]
    todo = [_slug(c) for c in crops if FIELD not in c]
    return held, nulls, todo


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    evidence, floor = None, POPULATION_FLOOR
    if "--evidence" in args:
        i = args.index("--evidence"); evidence = args[i + 1]; del args[i:i + 2]
    if "--floor" in args:
        i = args.index("--floor"); floor = int(args[i + 1]); del args[i:i + 2]
    path = args[0] if args else os.path.join(os.path.dirname(HERE), "crops_data_final.json")
    data = json.load(open(path, encoding="utf-8"))
    crops, catalog = data["crops"], data.get("source_catalog") or {}
    held, nulls, todo = coverage(crops)
    inspected = len(held) + len(nulls)
    print(f"sowing_heat_ceiling_gate: inspected {inspected} crop(s) carrying {FIELD} (held {len(held)}, "
          f"not held {len(nulls)}) of {len(crops)} scanned; TODO {len(todo)}")
    if inspected == 0 or inspected < floor:
        print(f"REFUSED: inspected {inspected} crop(s), below the floor of {floor}")
        return 2
    v = []
    for c in crops:
        v += check_crop(c, catalog)
    if evidence:
        man, cache = load_manifest(evidence), {}
        n = 0
        for c in crops:
            if FIELD in c:
                v += check_bytes(c, man, evidence, cache)
                n += 1
        print(f"  byte checks: {n} crop(s) against {len(cache)} hashed page(s) in {evidence}")
    else:
        print("  byte checks: SKIPPED (no --evidence)")
    if v:
        print(f"sowing_heat_ceiling_gate: {len(v)} VIOLATION(S)")
        for x in v:
            print("  -", x)
        return 1
    print("sowing_heat_ceiling_gate: PASS (0 violations)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
