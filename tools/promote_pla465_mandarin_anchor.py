#!/usr/bin/env python3
"""promote_pla465_mandarin_anchor -- PLA-465 owed repair: mandarin-clementine's `ucr_citrus` anchor.
Base 892c76fb.

THE DEFECT. The crop cited `ucr_citrus` at https://citrusvariety.ucr.edu/crc3178 on all 19 cells that
carry that key. crc3178 is the Frost Owari Satsuma accession (Citrus unshiu Marcovitch), re-read from raw
bytes 2026-09-18. PLA-465 promote 1 surfaced this as "the crop's cited UCR anchor is a satsuma page, the
wrong scion".

THAT REASON IS TOO WIDE, AND ACTING ON IT WHOLESALE WOULD ITSELF BE A DEFECT. This crop is scoped to
mandarins broadly ("Mandarins (Citrus reticulata and its hybrids)") and Owari Satsuma is its FIRST
recommended variety, so eight cells make satsuma-specific claims that crc3178 carries verbatim. A blanket
repoint would strip eight correct attributions. The anchor was therefore adjudicated CELL BY CELL against
the operational rule of docs/2026-07-26-artichoke-design-decisions.md A.8: truth lives in the per-cell
anchoring URL, and the anchored document must be fetched and the claim sentence confirmed present.

WHAT MOVES. On `mandarin-clementine` only, SEVEN `anchoring_urls.ucr_citrus` entries: `url` from crc3178 to
the accession that carries that cell's claim, and `verified` from 2026-07-02 to 2026-09-18, because the new
URL was verified today and carrying the old date forward would fabricate the attribution. Plus ONE
`field_additions` entry and ONE dated addendum appended to the existing PLA-465 finding's summary (the
original byte-identical as a prefix). No prose, no `sources` list, no dimension value, no other crop.
Height stays null; this promote re-verified that ruling rather than changing it.

WHY EACH GUARD EXISTS.
 1. THE THREE CLASSES ARE ENUMERATED AS LITERALS, NOT DERIVED. REPOINT (7), KEEP (8) and HELD (4) are
    hardcoded paths. An independent walk of the crop must find exactly their union and nothing else, so a
    cell added to or removed from the record is VISIBLE. A guard that derived its expectation from the same
    walk it validates would be vacuous, and would check OVERLAP where COVERAGE is the requirement.
 2. THE KEEP AND HELD CELLS ARE ASSERTED UNMOVED ON BOTH SIDES. The failure this promote is most likely to
    cause is over-reach, so the cells it must NOT touch are pinned pre and post, not merely left alone.
 3. THE TARGET VOCABULARY IS CLOSED. Every `to` must be one of the two adjudicated accessions; every `from`
    must be crc3178 at the pinned prior `verified` date. A repoint to an unread page refuses.
 4. THE PROVENANCE RECORD IS PINNED BY SHAPE AND MUST NAME THE FIELD, and the addendum targets one existing
    finding by id AND by its exact original summary, so a record that has moved since staging refuses.
 5. BLAST RADIUS AT THE LEAF, SET BEFORE VALUE: top-level, roster, crop-level and verification_status key
    sets are compared BEFORE any value, because iterating the pre state makes additions in post invisible.
    Every crop but mandarin-clementine byte-identical; inside it, only the seven anchor records and
    verification_status may differ, and the anchor records only in `url` and `verified`.

Usage:
    promote_pla465_mandarin_anchor.py --check | --out PATH | --expect-sha SHA
"""
import argparse, copy, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CANON = os.path.join(REPO, "crops_data_final.json")
STAGE = os.path.join(HERE, "staging", "pla465_mandarin_anchor")
SPEC = os.path.join(STAGE, "spec.json")

sys.path.insert(0, HERE)
import plant_dimensions_gate as PDG  # noqa: E402
import url_health_gate as UHG  # noqa: E402

BASE_SHA = "892c76fb9e89fd9a242f682a7040a71886cb128ec899092a4f6414d2e0708edb"  # PLA-465 promote 2, 20c795f
ROSTER = 128
CROP = "mandarin-clementine"
KEY = "ucr_citrus"
CERTIFIED = "verified_gs_arc"
SESSION = "pla465_2026-09-20"
OLD_URL = "https://citrusvariety.ucr.edu/crc3178"
VERIFIED_BEFORE = "2026-07-02"
VERIFIED_AFTER = "2026-09-20"
CRC0279 = "https://citrusvariety.ucr.edu/crc0279"
CRC3913 = "https://citrusvariety.ucr.edu/crc3913"
ALLOWED_TARGETS = (CRC0279, CRC3913)
ANCHOR_KEYS = ("url", "verified")
FA_KEYS = ("field", "date", "sources", "note")
FA_FIELD = "ucr_citrus_anchor"
ADDENDUM_MARK = " [ADDENDUM 2026-09-20, PLA-465:"
FINDING_ID = "mandarin_clementine_plant_dimensions_unusable_anchor_pla465"

# The three classes, enumerated. Their union IS the census of ucr_citrus cells on this crop.
REPOINT_PATHS = (
    "tips_by_stage.bloom[1]",
    "tips_by_stage.ripening_harvest[1]",
    "regions.ca_desert.resolved_by_zone.9",
    "regions.ca_desert.resolved_by_zone.10",
    "regions.ca_desert.resolved_by_zone.11",
    "regions.low_desert_az.resolved_by_zone.9",
    "regions.low_desert_az.resolved_by_zone.10",
)
# Satsuma-specific claims that crc3178 carries verbatim. These must NOT move.
KEEP_PATHS = (
    "storage",
    "varieties",
    "tips_by_stage.ripening_harvest[0]",
    "failure_diagnostics[1]",
    "regions.ca_interior.resolved_by_zone.8",
    "regions.ca_interior.resolved_by_zone.9",
    "regions.ca_north_coast.resolved_by_zone.9",
    "regions.ca_north_coast.resolved_by_zone.10",
)
# RULING 2 (Trevor, 2026-09-20): the claim spans two accessions and one url per source key cannot hold
# both ends, so these stay on crc3178 rather than being credited to one end. Routed to PLA-559.
HELD_PATHS = (
    "regions.ca_south_coast.resolved_by_zone.9",
    "regions.ca_south_coast.resolved_by_zone.10",
    "regions.ca_south_coast.resolved_by_zone.11",
)
# RULING 1 (Trevor, 2026-09-20): no UCR accession page carries this cell's climate claim, so the credit is
# DROPPED rather than moved -- out of `sources` and out of `anchoring_urls`, both.
DROP_PATH = "failure_diagnostics[0]"
CELLS_BEFORE = 19
CELLS_AFTER = 18
FINDING_IDS = (
    "mandarin_clementine_climate_claim_citation_pla465",
    "mandarin_clementine_region_span_single_anchor_pla465",
)
RECORD_KEYS = ("id", "severity", "status", "blocks_launch", "filed_in_session", "summary", "resolution_note", "deferred_to")
STATUSES = ("accepted", "deferred")
# Every sha256 quoted in staged prose must be one of these MEASURED digests. A near-miss on the re-stage
# wrote a plausible-looking 64-hex string into a finding after only the first 16 chars had been measured:
# the field's shape pulls a fabricated value out of you. A digest that is not on this list REFUSES.
EVIDENCE_HASHES = {
    "3a610c2fc8a9b4762a3a4787723db9e7bb678029979077cf282a008db2b47547",  # crc3178 Frost Owari Satsuma
    "e64774ebf68e70424aed0377b1e36231213cbf203b2d246bd71ce3f00bfd2e30",  # crc0279 Algerian clementine
    "60703aa3d2d0d5cf1308211c4f0e5ca409fd2237cc1e4356cba042b99da5725c",  # crc3913 Gold Nugget
    "4d2a3549ec909ea85fc8be84efaea8ef3ed44ad31b4d8ee9547539c7eafaef47",  # CTAHR F&N-14 (the retained co-source)
}
SHA256_RE = re.compile(r"\b[0-9a-f]{64}\b")
EXPECTED = {"repoints": 7, "to_crc0279": 6, "to_crc3913": 1, "keeps": 8, "dropped": 1, "held": 3,
            "cells_before": CELLS_BEFORE, "cells_after": CELLS_AFTER, "findings": 2}


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def serialize(data):
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def by_slug(data):
    return {c["slug"]: c for c in data["crops"]}


def load_canonical(path=None):
    p = path or CANON
    with open(p, "rb") as f:
        raw = f.read()
    got = sha256_bytes(raw)
    if got != BASE_SHA:
        raise SystemExit(f"REFUSED: canonical is {got[:8]}, this promote is pinned to {BASE_SHA[:8]}")
    return json.loads(raw)


def staged():
    with open(SPEC, encoding="utf-8") as f:
        return json.load(f)


def _bad_copy(s):
    """Backend provenance text: `--` is allowed (quoted page text carries it), the em dash is not."""
    return "—" in s


def resolve(crop, path):
    """Resolve 'a.b[1].c' / 'regions.x.resolved_by_zone.9' to the node, or None."""
    node = crop
    for seg in path.split("."):
        m = re.fullmatch(r"([^\[\]]+)((?:\[\d+\])*)", seg)
        if not m:
            return None
        if not isinstance(node, dict) or m.group(1) not in node:
            return None
        node = node[m.group(1)]
        for idx in re.findall(r"\[(\d+)\]", m.group(2)):
            if not isinstance(node, list) or int(idx) >= len(node):
                return None
            node = node[int(idx)]
    return node


def census(crop):
    """INDEPENDENT walk: every path whose anchoring_urls carries the ucr_citrus key."""
    found = []

    def walk(o, pat):
        if isinstance(o, dict):
            a = o.get("anchoring_urls")
            if isinstance(a, dict) and KEY in a:
                found.append(pat)
            for k, v in o.items():
                walk(v, f"{pat}.{k}" if pat else k)
        elif isinstance(o, list):
            for i, x in enumerate(o):
                walk(x, f"{pat}[{i}]")

    walk(crop, "")
    return set(found)


def check_spec_shape(spec):
    if spec.get("base_sha") != BASE_SHA:
        raise SystemExit("REFUSED: spec base_sha is not the pinned base")
    if spec.get("crop") != CROP or spec.get("source_key") != KEY:
        raise SystemExit("REFUSED: spec does not target the pinned crop and source key")
    if spec.get("old_url") != OLD_URL or spec.get("verified_before") != VERIFIED_BEFORE:
        raise SystemExit("REFUSED: spec does not pin the prior url and verified date")
    rows = spec["repoints"]
    if len(rows) != EXPECTED["repoints"]:
        raise SystemExit(f"REFUSED: {len(rows)} repoints, pinned {EXPECTED['repoints']}")
    if [r["path"] for r in rows] != list(REPOINT_PATHS):
        raise SystemExit("REFUSED: spec repoint paths are not the pinned REPOINT set, in order")
    seen = set()
    for r in rows:
        if set(r) != {"path", "from", "to", "verified", "why"}:
            raise SystemExit(f"REFUSED: repoint row {r.get('path')} has keys {sorted(r)}")
        if r["path"] in seen:
            raise SystemExit(f"REFUSED: repoint path {r['path']} appears twice")
        seen.add(r["path"])
        if r["from"] != OLD_URL:
            raise SystemExit(f"REFUSED: {r['path']} does not move off the pinned old url")
        if r["to"] not in ALLOWED_TARGETS:
            raise SystemExit(f"REFUSED: {r['path']} targets {r['to']!r}, which is not an adjudicated accession")
        # NOT GUARDED, and deliberately: a no-op repoint is unreachable. `from` is pinned to OLD_URL two
        # lines above and `to` must be in ALLOWED_TARGETS, which does not contain OLD_URL, so to == from
        # can never survive to be tested. A guard here would be a zero with extra steps.
        if r["verified"] != VERIFIED_AFTER:
            raise SystemExit(f"REFUSED: {r['path']} must carry the date the new url was verified")
        if not (r["why"] or "").strip() or _bad_copy(r["why"]):
            raise SystemExit(f"REFUSED: {r['path']} has an empty or em-dashed rationale")
    n0 = sum(1 for r in rows if r["to"] == CRC0279)
    n1 = sum(1 for r in rows if r["to"] == CRC3913)
    if n0 != EXPECTED["to_crc0279"] or n1 != EXPECTED["to_crc3913"]:
        raise SystemExit(f"REFUSED: target split is {n0}/{n1}, pinned {EXPECTED['to_crc0279']}/{EXPECTED['to_crc3913']}")
    fa = spec["field_addition"]
    if set(fa) != set(FA_KEYS):
        raise SystemExit(f"REFUSED: field_addition has keys {sorted(fa)}")
    if fa["field"] != FA_FIELD or fa["date"] != VERIFIED_AFTER:
        raise SystemExit("REFUSED: field_addition must name the field and carry the pass date")
    if fa["sources"] != [KEY]:
        raise SystemExit("REFUSED: field_addition must credit the source key it repairs")
    if not (fa["note"] or "").strip() or _bad_copy(fa["note"]):
        raise SystemExit("REFUSED: field_addition note is empty or carries an em dash")
    for frag in (OLD_URL, CRC0279, CRC3913):
        if frag not in fa["note"]:
            raise SystemExit(f"REFUSED: field_addition note does not name {frag}")
    a = spec["addendum"]
    if set(a) != {"id", "mark", "suffix"}:
        raise SystemExit("REFUSED: addendum has the wrong shape")
    if a["id"] != FINDING_ID or a["mark"] != ADDENDUM_MARK:
        raise SystemExit("REFUSED: addendum does not target the pinned finding with the dated marker")
    if not a["suffix"].startswith(ADDENDUM_MARK) or not a["suffix"].endswith("]"):
        raise SystemExit("REFUSED: addendum suffix must open with the dated marker and close its bracket")
    if _bad_copy(a["suffix"]):
        raise SystemExit("REFUSED: addendum carries an em dash")
    dr = spec["drop"]
    if set(dr) != {"path", "source_key", "from", "why", "must_retain"}:
        raise SystemExit("REFUSED: drop block has the wrong shape")
    if dr["path"] != DROP_PATH or dr["source_key"] != KEY or dr["from"] != OLD_URL:
        raise SystemExit("REFUSED: drop block does not target the pinned cell, key and url")
    if dr["path"] in set(REPOINT_PATHS) | set(KEEP_PATHS) | set(HELD_PATHS):
        raise SystemExit("REFUSED: the dropped cell is also claimed by another class")
    if not dr["must_retain"]:
        raise SystemExit("REFUSED: the drop must name at least one source the cell retains; "
                         "a drop that leaves a claim-bearing cell uncited is not this promote's to make")
    if not (dr["why"] or "").strip() or _bad_copy(dr["why"]):
        raise SystemExit("REFUSED: drop rationale is empty or carries an em dash")
    fs = spec["findings"]
    if len(fs) != EXPECTED["findings"]:
        raise SystemExit(f"REFUSED: {len(fs)} findings, pinned {EXPECTED['findings']}")
    if tuple(f["entry"]["id"] for f in fs) != FINDING_IDS:
        raise SystemExit("REFUSED: finding ids are not the pinned ids, in order")
    for f in fs:
        if f["crop"] != CROP:
            raise SystemExit("REFUSED: a finding targets another crop")
        e = f["entry"]
        if set(e) != set(RECORD_KEYS):
            raise SystemExit(f"REFUSED: finding {e.get('id')} has keys {sorted(e)}")
        if e["blocks_launch"] is not False or e["filed_in_session"] != SESSION:
            raise SystemExit(f"REFUSED: {e['id']} must be non-blocking and filed in {SESSION}")
        if e["status"] not in STATUSES:
            raise SystemExit(f"REFUSED: {e['id']} status {e['status']!r} not in {STATUSES}")
        if (e["status"] == "deferred") != (e["deferred_to"] is not None):
            raise SystemExit(f"REFUSED: {e['id']} deferred_to must be set iff status is deferred")
        if not (e["summary"] or "").strip() or not (e["resolution_note"] or "").strip():
            raise SystemExit(f"REFUSED: {e['id']} has an empty summary or resolution_note")
        if _bad_copy(e["summary"]) or _bad_copy(e["resolution_note"]):
            raise SystemExit(f"REFUSED: {e['id']} carries an em dash")
    # EVERY sha256 QUOTED ANYWHERE IN THE SPEC MUST BE ONE THIS SESSION MEASURED.
    for d in set(SHA256_RE.findall(json.dumps(spec, ensure_ascii=False))):
        if d not in EVIDENCE_HASHES and d != BASE_SHA:
            raise SystemExit(f"REFUSED: the spec quotes sha256 {d[:16]}... which is not a measured evidence digest")
    if spec["expected"] != EXPECTED:
        raise SystemExit("REFUSED: spec expected block is not the promote's pins")
    return len(rows)


def check_pre_state(spec, data):
    idx = by_slug(data)
    if len(data["crops"]) != ROSTER:
        raise SystemExit(f"REFUSED: roster is {len(data['crops'])}, pinned {ROSTER}")
    c = idx.get(CROP)
    if c is None:
        raise SystemExit(f"REFUSED: {CROP} is not on the roster")
    if (c.get("verification_status") or {}).get("status") != CERTIFIED:
        raise SystemExit(f"REFUSED: {CROP} is not certified")
    # COVERAGE, not overlap: the independent walk must equal the enumerated union exactly.
    declared = set(REPOINT_PATHS) | set(KEEP_PATHS) | set(HELD_PATHS) | {DROP_PATH}
    if len(declared) != CELLS_BEFORE:
        raise SystemExit(f"REFUSED: the four classes declare {len(declared)} distinct cells, pinned {CELLS_BEFORE}")
    found = census(c)
    if found != declared:
        miss, extra = sorted(declared - found), sorted(found - declared)
        raise SystemExit(f"REFUSED: the {KEY} cell census moved. missing={miss} unaccounted={extra}")
    # every declared cell is on the old url at the pinned prior date
    for p in sorted(declared):
        rec = (resolve(c, p) or {}).get("anchoring_urls", {}).get(KEY)
        if not isinstance(rec, dict) or set(rec) != set(ANCHOR_KEYS):
            raise SystemExit(f"REFUSED: {p} {KEY} record is missing or has keys {sorted(rec or [])}")
        if rec["url"] != OLD_URL:
            raise SystemExit(f"REFUSED: {p} is on {rec['url']!r}, not the defective anchor this promote repairs")
        if rec["verified"] != VERIFIED_BEFORE:
            raise SystemExit(f"REFUSED: {p} carries verified {rec['verified']!r}, not the pinned prior date")
    vs = c["verification_status"]
    if not isinstance(vs.get("field_additions"), list) or not isinstance(vs.get("open_findings"), list):
        raise SystemExit(f"REFUSED: {CROP} field_additions / open_findings are not lists")
    if any(x.get("field") == FA_FIELD for x in vs["field_additions"]):
        raise SystemExit(f"REFUSED: {CROP} already carries a {FA_FIELD} provenance record")
    node = resolve(c, DROP_PATH)
    srcs = node.get("sources")
    if not isinstance(srcs, list) or KEY not in srcs:
        raise SystemExit(f"REFUSED: {DROP_PATH} does not list {KEY} in its sources; there is nothing to drop")
    remaining = [x for x in srcs if x != KEY]
    if not remaining:
        raise SystemExit(f"REFUSED: dropping {KEY} would leave {DROP_PATH} with NO source. "
                         "A claim-bearing cell may not be left uncited by this promote: the T1 read comes first.")
    if remaining != list(spec["drop"]["must_retain"]):
        raise SystemExit(f"REFUSED: {DROP_PATH} would retain {remaining}, not the staged {spec['drop']['must_retain']}")
    for fid in FINDING_IDS:
        if any(x.get("id") == fid for x in vs["open_findings"]):
            raise SystemExit(f"REFUSED: {CROP} already carries finding {fid}")
    hits = [x for x in vs["open_findings"] if x.get("id") == FINDING_ID]
    if len(hits) != 1:
        raise SystemExit(f"REFUSED: addendum target {FINDING_ID} matches {len(hits)} findings")
    if ADDENDUM_MARK in hits[0].get("summary", ""):
        raise SystemExit(f"REFUSED: addendum target {FINDING_ID} already carries this addendum")
    if any(c.get(k) is not None for k in PDG.FIELDS):
        raise SystemExit(f"REFUSED: {CROP} carries a plant dimension; this repair is about the anchor, and height stays null")
    return len(declared)


def apply_to(data, spec):
    post = copy.deepcopy(data)
    c = by_slug(post)[CROP]
    for r in spec["repoints"]:
        rec = resolve(c, r["path"])["anchoring_urls"][KEY]
        rec["url"] = r["to"]
        rec["verified"] = r["verified"]
    node = resolve(c, DROP_PATH)
    node["sources"] = [x for x in node["sources"] if x != KEY]
    del node["anchoring_urls"][KEY]
    vs = c["verification_status"]
    for f in spec["findings"]:
        vs["open_findings"].append(copy.deepcopy(f["entry"]))
    vs["field_additions"].append(copy.deepcopy(spec["field_addition"]))
    for x in vs["open_findings"]:
        if x.get("id") == FINDING_ID:
            x["summary"] = x["summary"] + spec["addendum"]["suffix"]
    return post


def check_post(post, spec):
    c = by_slug(post)[CROP]
    if census(c) != set(REPOINT_PATHS) | set(KEEP_PATHS) | set(HELD_PATHS):
        raise SystemExit("REFUSED: the cell census changed across the write")
    # NOT GUARDED, and deliberately: a COUNT of the post-census is unreachable. The line above asserts the
    # census equals REPOINT|KEEP|HELD exactly, and that set has CELLS_AFTER members, so the count is implied
    # and could never fail on its own. CELLS_AFTER stays as the pin the SUITE asserts that set against.
    node = resolve(c, DROP_PATH)
    # NOT GUARDED, and deliberately: "KEY still in the dropped cell's anchoring_urls" is unreachable here.
    # census() IS the predicate "anchoring_urls carries KEY", so leaving it behind puts DROP_PATH back into
    # the census and the comparison two lines above fires first. A check here would be a zero with extra
    # steps. The `sources` half below is NOT unreachable: census never looks at `sources`.
    if KEY in (node.get("sources") or []):
        raise SystemExit(f"REFUSED: {DROP_PATH} still lists {KEY} in sources; a drop must clear BOTH")
    if node.get("sources") != list(spec["drop"]["must_retain"]):
        raise SystemExit(f"REFUSED: {DROP_PATH} retains {node.get('sources')}, not the staged sources")
    if not node.get("sources"):
        raise SystemExit(f"REFUSED: {DROP_PATH} is left uncited after the drop")
    want = {r["path"]: r["to"] for r in spec["repoints"]}
    for p in sorted(set(KEEP_PATHS) | set(HELD_PATHS)):
        rec = resolve(c, p)["anchoring_urls"][KEY]
        if rec["url"] != OLD_URL or rec["verified"] != VERIFIED_BEFORE:
            raise SystemExit(f"REFUSED: {p} is a KEEP/HELD cell and must not move; it now reads {rec}")
    for p, url in want.items():
        rec = resolve(c, p)["anchoring_urls"][KEY]
        if rec["url"] != url or rec["verified"] != VERIFIED_AFTER:
            raise SystemExit(f"REFUSED: {p} did not land on its adjudicated accession; it reads {rec}")
    v = UHG.url_health_violations(c)
    if v:
        raise SystemExit("REFUSED: url_health_gate on the post-state: " + "; ".join(v[:5]))
    g = PDG.all_violations(post, presence=True)
    if g:
        raise SystemExit("REFUSED: plant_dimensions_gate on the post-state: " + "; ".join(g[:5]))
    blockers = [x for x in c["verification_status"]["open_findings"] if x.get("blocks_launch") and x.get("status") != "resolved"]
    if blockers:
        raise SystemExit(f"REFUSED: {CROP} carries a launch blocker after the write: {[b.get('id') for b in blockers]}")


def _j(x):
    return json.dumps(x, sort_keys=True)


def verify_post(pre, post, spec):
    """SET COMPARISON BEFORE VALUE COMPARISON, at every level."""
    if set(pre) != set(post):
        raise SystemExit("REFUSED: top-level key set changed")
    for k in pre:
        if k != "crops" and _j(pre[k]) != _j(post[k]):
            raise SystemExit(f"REFUSED: top-level key {k!r} changed")
    pre_i, post_i = by_slug(pre), by_slug(post)
    if set(pre_i) != set(post_i) or len(pre["crops"]) != len(post["crops"]):
        raise SystemExit("REFUSED: crop roster changed")
    for slug in pre_i:
        if slug == CROP:
            continue
        if _j(pre_i[slug]) != _j(post_i[slug]):
            raise SystemExit(f"REFUSED: untouched crop {slug} changed")
    s, g = pre_i[CROP], post_i[CROP]
    if set(s) != set(g):
        raise SystemExit(f"REFUSED: {CROP} crop-level key set changed")
    # Every crop-level branch must be byte-identical once the seven anchor records are normalised back.
    probe = copy.deepcopy(g)
    dnode = resolve(probe, DROP_PATH)
    if KEY in (dnode.get("anchoring_urls") or {}) or KEY in (dnode.get("sources") or []):
        raise SystemExit(f"REFUSED: {DROP_PATH} was not actually dropped")
    dnode["sources"] = list(pre_i[CROP] and resolve(s, DROP_PATH)["sources"])
    dnode["anchoring_urls"][KEY] = copy.deepcopy(resolve(s, DROP_PATH)["anchoring_urls"][KEY])
    for r in spec["repoints"]:
        rec = resolve(probe, r["path"])["anchoring_urls"][KEY]
        if set(rec) != set(ANCHOR_KEYS):
            raise SystemExit(f"REFUSED: {r['path']} anchor record key set changed")
        rec["url"], rec["verified"] = OLD_URL, VERIFIED_BEFORE
    for k in s:
        if k == "verification_status":
            continue
        if _j(s[k]) != _j(probe[k]):
            raise SystemExit(f"REFUSED: {CROP} field {k!r} changed beyond the seven anchor records")
    sv, gv = s["verification_status"], g["verification_status"]
    if set(sv) != set(gv):
        raise SystemExit(f"REFUSED: {CROP} verification_status key set changed")
    for k in sv:
        if k in ("field_additions", "open_findings"):
            continue
        if _j(sv[k]) != _j(gv[k]):
            raise SystemExit(f"REFUSED: {CROP} verification_status.{k} changed")
    fa_pre, fa_post = sv["field_additions"], gv["field_additions"]
    if len(fa_post) != len(fa_pre) + 1:
        raise SystemExit(f"REFUSED: field_additions went {len(fa_pre)} -> {len(fa_post)}, expected exactly one append")
    if _j(fa_post[:len(fa_pre)]) != _j(fa_pre):
        raise SystemExit("REFUSED: field_additions prefix is not byte-identical")
    if _j(fa_post[-1]) != _j(spec["field_addition"]):
        raise SystemExit("REFUSED: the appended field_addition is not the spec's record")
    of_pre, of_post = sv["open_findings"], gv["open_findings"]
    if len(of_post) != len(of_pre) + EXPECTED["findings"]:
        raise SystemExit(f"REFUSED: open_findings went {len(of_pre)} -> {len(of_post)}, expected exactly "
                         f"{EXPECTED['findings']} appended")
    want_tail = [f["entry"] for f in spec["findings"]]
    if _j(of_post[len(of_pre):]) != _j(want_tail):
        raise SystemExit("REFUSED: the appended findings are not the spec's records")
    n_add = 0
    for x, y in zip(of_pre, of_post):
        if x.get("id") == FINDING_ID:
            if set(x) != set(y):
                raise SystemExit("REFUSED: addendum target key set changed")
            for k in x:
                if k == "summary":
                    if y[k] != x[k] + spec["addendum"]["suffix"]:
                        raise SystemExit("REFUSED: addendum target summary is not the original plus the suffix")
                elif _j(x[k]) != _j(y[k]):
                    raise SystemExit(f"REFUSED: addendum target field {k!r} changed")
            n_add += 1
        elif _j(x) != _j(y):
            raise SystemExit("REFUSED: an open_finding other than the addendum target changed")
    # NOT GUARDED, and deliberately: a total on n_add is unreachable. An unapplied addendum refuses on the
    # per-entry summary comparison above, and a target whose id moved refuses as a changed non-target
    # finding. A count check here could never fire in isolation, so it would read as coverage and be one.
    return len(spec["repoints"]), n_add


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("canonical", nargs="?", default=None)
    ap.add_argument("--canonical", dest="canonical_flag", default=None)
    ap.add_argument("--expect-sha", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    path = args.canonical_flag or args.canonical
    if args.out and os.path.abspath(args.out) == os.path.abspath(path or CANON):
        sys.exit("REFUSED: --out may not target the canonical; use --expect-sha for the write")
    data = load_canonical(path)
    spec = staged()
    n = check_spec_shape(spec)
    print(f"  spec shape        {n} repoints, {EXPECTED['to_crc0279']} to crc0279 and {EXPECTED['to_crc3913']} to crc3913; targets closed to the adjudicated accessions")
    cells = check_pre_state(spec, data)
    print(f"  pre-state         {cells} {KEY} cells found by an independent walk, equal to the enumerated REPOINT+KEEP+HELD+DROP union; every one on crc3178 at {VERIFIED_BEFORE}")
    post = apply_to(data, spec)
    check_post(post, spec)
    print(f"  post gates        {len(KEEP_PATHS)} KEEP and {len(HELD_PATHS)} HELD cells unmoved; {DROP_PATH} cleared from sources AND anchoring_urls, retaining {spec['drop']['must_retain']}; {CELLS_AFTER} cells left; url_health 0; plant_dimensions_gate 0; no launch blocker")
    n_rep, n_add = verify_post(data, post, spec)
    print(f"  verify post       {n_rep} anchors repointed, 1 dropped, {EXPECTED['findings']} findings, 1 provenance record, {n_add} addendum, nothing else")
    blob = serialize(post)
    new_sha = sha256_bytes(blob)
    print(f"\n  {BASE_SHA[:8]} -> {new_sha}")
    if args.expect_sha and new_sha != args.expect_sha:
        sys.exit(f"REFUSED: expected {args.expect_sha}, got {new_sha}")
    if args.out:
        with open(args.out, "wb") as f:
            f.write(blob)
        print(f"  WROTE post-state to {args.out} (canonical untouched)")
        return 0
    if args.check:
        print("  --check: nothing written")
        return 0
    if not args.expect_sha:
        sys.exit("REFUSED: writing canonical requires --expect-sha (the gauntleted scratch SHA)")
    with open(path or CANON, "wb") as f:
        f.write(blob)
    print(f"  WROTE {path or CANON}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
