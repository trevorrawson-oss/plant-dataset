#!/usr/bin/env python3
"""planting_layout_gate (whole_crop_gate A44) -- planting_layout as a LIST of (arrangement, support)
entries, and the crop-root spacing MIRRORS that follow it. PLA-10 promote 1, spec
docs/specs/pla10-field-shape.md §1.1, §1.2, §1.6, §2.4, §3 (rulings R2 as amended, 2026-09-30).

THE SHAPE. `planting_layout` is a crop-level list. Each entry is one (arrangement, support) pair
carrying its own spacing and its own citation (`sources` + `anchoring_urls`). Exactly one entry is the
default. `[]` appears only on a zone_independent crop (the 8 microgreens), where it is the claim
"assessed, no ground layout".

THE MIRRORS (D8 option (b): the entry is the record, the root is a gated copy, never a second
authored one):
  spacing_inches     == in_row_inches of the FIRST entry carrying one, default first, then declared
                        order; null only when no entry carries one (after promote 1: the 8 microgreens).
                        ONE meaning everywhere: between individual plants (R2). A hill's between-hills
                        distance never enters it.
  row_spacing_inches == the DEFAULT entry's, no fallback.
  row_spacing_reason == null iff row_spacing_inches is non-null; otherwise "see_layout" iff the default
                        is a hill and a non-default entry carries a row figure, "not_applicable" iff
                        zone_independent, else "not_authored". On an ENTRY it is only ever
                        "not_authored" (an entry exists only where there is a ground layout).
A mirror gate is a COHERENCE gate, not a fidelity gate (memory coherence-gate-is-not-fidelity):
fidelity sits on the entry, where §F, A62 and A63 see it. This only proves the consumer copy did not
drift from it.

TWO STATES (gates arm off the data):
  UNARMED (PRESENCE_ARMED False; the tools commit, canonical c5fc3d13). The 6 legacy strings
    (4 corn "block", artichoke + asparagus "row") validate under the old enum + block<->min_rows rule;
    an absent layout is a no-op; but ANY crop that already carries a list is held to the full rule,
    so a crop cannot be half-migrated.
  ARMED (flipped in promote 1's data commit, with test_the_data_commit_ships_armed; LIVE). Every
    certified crop carries a list and the three mirror keys; the string form is refused; the retired
    spacing_inches_anchoring_urls is refused by name.
The flag lives HERE, not in whole_crop_gate (where A59-A61 keep theirs), because gate_all's roster
half needs it too and whole_crop_gate is a script that runs on import.

POPULATION. roster() reports certified crops, entries, list-shaped and legacy crops; refusal() refuses
an empty roster, a roster below CERT_FLOOR, and (armed) fewer entries than ENTRY_FLOOR. The floors are
literals measured on c5fc3d13 (121 certified; 113 carry a spacing pair, so >= 113 entries once armed),
never derived from the walk.

Usage:
  planting_layout_gate.py [PATH] [--armed]   exit 1 on a violation, 2 on a refused population
"""
import json
import re
import sys

CERTIFIED = "verified_gs_arc"

PRESENCE_ARMED = True

# Literal floors (measured 2026-10-01 on c5fc3d13). Minimums, not pins: the roster may grow.
CERT_FLOOR = 121
ENTRY_FLOOR = 113

ARRANGEMENTS = ("row", "hill", "block")
SUPPORTS = ("none", "stake", "cage", "trellis")
ENTRY_REASONS = (None, "not_authored")
ROOT_REASONS = (None, "not_authored", "not_applicable", "see_layout")
ID_RE = re.compile(r"^(row|hill|block)-(none|stake|cage|trellis)(-[a-z0-9]+)?$")

COMMON_REQUIRED = ("id", "arrangement", "support", "default", "row_spacing_inches",
                   "row_spacing_reason", "sources", "anchoring_urls")
REQUIRED = {
    "row": COMMON_REQUIRED + ("in_row_inches",),
    "block": COMMON_REQUIRED + ("in_row_inches",),
    "hill": COMMON_REQUIRED + ("hill_spacing_inches", "plants_per_hill"),
}
OPTIONAL = {
    "row": ("rows_per_bed", "mature_height_ft"),
    "block": ("mature_height_ft",),
    "hill": ("in_row_inches", "mature_height_ft"),
}
MIRROR_KEYS = ("spacing_inches", "row_spacing_inches", "row_spacing_reason")
RETIRED_ROOT_KEYS = ("spacing_inches_anchoring_urls", "spacing_inches_sources")

# The pre-PLA-10 string form, kept ONLY for the unarmed state. grid/single left the enum (spec,
# "Decided in this spec": 0 population).
LEGACY_LAYOUTS = ("block", "row", "hill")
MIN_ROWS_FLOOR = 2
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def certified(crop):
    return (crop.get("verification_status") or {}).get("status") == CERTIFIED


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def is_pair(v):
    """[lo, hi], numbers (never bool), 0 < lo <= hi."""
    return isinstance(v, list) and len(v) == 2 and all(_num(x) for x in v) and 0 < v[0] <= v[1]


def _int_ge(v, floor):
    return isinstance(v, int) and not isinstance(v, bool) and v >= floor


def _entries(crop):
    pl = crop.get("planting_layout")
    return [e for e in pl if isinstance(e, dict)] if isinstance(pl, list) else []


def default_entry(entries):
    ds = [e for e in entries if e.get("default") is True]
    return ds[0] if len(ds) == 1 else None


def expected_spacing(entries):
    """The between-plants mirror: the first entry carrying in_row_inches, default first, then declared
    order. None when no entry carries one (R2 as amended)."""
    d = default_entry(entries)
    order = ([d] if d is not None else []) + [e for e in entries if e is not d]
    for e in order:
        if "in_row_inches" in e:
            return e["in_row_inches"]
    return None


def expected_row_reason(crop):
    """What crop-root row_spacing_reason must be, given the crop's entries (spec §1.2, §3)."""
    if crop.get("zone_independent") is True:
        return "not_applicable"
    entries = _entries(crop)
    d = default_entry(entries)
    if d is None:
        return None
    if d.get("row_spacing_inches") is not None:
        return None
    if d.get("arrangement") == "hill" and any(
            e is not d and e.get("row_spacing_inches") is not None for e in entries):
        return "see_layout"
    return "not_authored"


# ---------------------------------------------------------------- legacy (unarmed only)
def _legacy_violations(slug, crop):
    v = []
    pl = crop.get("planting_layout")
    has_mr = crop.get("pollination_block_min_rows") is not None
    mr = crop.get("pollination_block_min_rows")
    if pl not in LEGACY_LAYOUTS:
        return [f"{slug}: planting_layout {pl!r} not in {sorted(LEGACY_LAYOUTS)}"]
    if pl == "block":
        if not has_mr:
            v.append(f"{slug}: planting_layout 'block' but pollination_block_min_rows missing")
        elif not _int_ge(mr, MIN_ROWS_FLOOR):
            v.append(f"{slug}: pollination_block_min_rows {mr!r} not an int >= {MIN_ROWS_FLOOR}")
    elif has_mr:
        v.append(f"{slug}: planting_layout {pl!r} (not 'block') but pollination_block_min_rows present")
    return v


# ---------------------------------------------------------------- R5 migration (spec R5)
def migration_waived(slug, e):
    """True iff this entry is the (crop, entry id) an R5 migration waiver names AND both citation
    slots are empty ([] and {}). Byte-equality to the pre-promote spacing is A62's check."""
    import planting_layout_migration_known as M
    w = M.WAIVERS.get(slug)
    return (w is not None and slug in M.ELIGIBLE and e.get("id") == w.get("entry_id")
            and e.get("sources") == [] and e.get("anchoring_urls") == {})


# ---------------------------------------------------------------- one entry (§1.6 checks 2, 4, 5, 6)
def _entry_violations(slug, i, e):
    if not isinstance(e, dict):
        return [f"{slug}: planting_layout[{i}] is not an object"]
    eid = e.get("id")
    tag = f"{slug}: planting_layout[{i}]" + (f" ({eid})" if isinstance(eid, str) else "")
    v = []
    arr, sup = e.get("arrangement"), e.get("support")
    for k, val, enum in (("arrangement", arr, ARRANGEMENTS), ("support", sup, SUPPORTS)):
        if k not in e:
            v.append(f"{tag}: missing required key {k!r}")
        elif val not in enum:
            v.append(f"{tag}: {k} {val!r} not in {list(enum)}")
    if arr in ARRANGEMENTS:
        req, opt = REQUIRED[arr], OPTIONAL[arr]
        for k in req:
            if k not in e:
                v.append(f"{tag}: missing required key {k!r} for a {arr} entry")
        for k in e:
            if k not in req and k not in opt:
                v.append(f"{tag}: unknown key {k!r} on a {arr} entry (allowed: "
                         f"{sorted(req + opt)})")
    if "id" in e:
        if not isinstance(eid, str) or not ID_RE.match(eid):
            v.append(f"{tag}: id {eid!r} does not match the pattern {ID_RE.pattern}")
        elif arr in ARRANGEMENTS and sup in SUPPORTS and not (
                eid == f"{arr}-{sup}" or eid.startswith(f"{arr}-{sup}-")):
            v.append(f"{tag}: id {eid!r} does not match its pair ({arr}, {sup})")
    if "default" in e and not isinstance(e.get("default"), bool):
        v.append(f"{tag}: default {e.get('default')!r} is not a bool")

    for k in ("in_row_inches", "hill_spacing_inches"):
        if k in e and not is_pair(e[k]):
            v.append(f"{tag}: {k} {e[k]!r} is not a [lo, hi] pair of positive numbers, lo <= hi")
    if "plants_per_hill" in e:
        p = e["plants_per_hill"]
        if not (is_pair(p) and all(_int_ge(x, 1) for x in p)):
            v.append(f"{tag}: plants_per_hill {p!r} is not a [lo, hi] pair of whole plants >= 1")
    if "rows_per_bed" in e and not _int_ge(e["rows_per_bed"], 2):
        v.append(f"{tag}: rows_per_bed {e['rows_per_bed']!r} is not an int >= 2")
    if "mature_height_ft" in e:
        if sup == "none":
            v.append(f"{tag}: mature_height_ft override on a support 'none' entry; the override is "
                     f"legal only where the entry's support changes the height (§1.1)")
        if not is_pair(e["mature_height_ft"]):
            v.append(f"{tag}: mature_height_ft {e['mature_height_ft']!r} is not a [lo, hi] pair")

    if "row_spacing_inches" in e or "row_spacing_reason" in e:
        rs, rr = e.get("row_spacing_inches"), e.get("row_spacing_reason")
        if rr not in ENTRY_REASONS:
            v.append(f"{tag}: row_spacing_reason {rr!r} on an entry; see_layout and not_applicable "
                     f"are crop-root values only, an entry is only ever 'not_authored'")
        elif rs is None and rr != "not_authored":
            v.append(f"{tag}: row_spacing_inches is null but row_spacing_reason is {rr!r} "
                     f"(null iff 'not_authored')")
        elif rs is not None and rr is not None:
            v.append(f"{tag}: row_spacing_reason {rr!r} but row_spacing_inches is {rs!r} "
                     f"(the reason is null when the row figure is present)")
        if rs is not None and not is_pair(rs):
            v.append(f"{tag}: row_spacing_inches {rs!r} is not a [lo, hi] pair or null")

    if migration_waived(slug, e):
        pass  # R5: the one entry a migration waiver names ships uncited; A62 checks it byte-equal
    elif "sources" in e or "anchoring_urls" in e:
        src, anc = e.get("sources"), e.get("anchoring_urls")
        if not (isinstance(src, list) and src and all(isinstance(s, str) and s.strip() for s in src)):
            v.append(f"{tag}: sources {src!r} is not a non-empty list of catalog ids; the entry is "
                     f"the one citation slot for every number in it")
            src = []
        if len(set(src)) != len(src):
            v.append(f"{tag}: sources {src!r} repeats an id")
        if not isinstance(anc, dict):
            v.append(f"{tag}: anchoring_urls {anc!r} is not an object")
            anc = {}
        for s in sorted(set(src) - set(anc)):
            v.append(f"{tag}: anchoring_urls has no entry for source {s!r} (one per source)")
        for s in sorted(set(anc) - set(src)):
            v.append(f"{tag}: anchoring_urls carries {s!r}, which is not in sources")
        for s, a in anc.items():
            if not (isinstance(a, dict) and isinstance(a.get("url"), str)
                    and a["url"].startswith(("http://", "https://"))):
                v.append(f"{tag}: anchoring_urls[{s!r}] has no http(s) url: {a!r}")
            elif not (isinstance(a.get("verified"), str) and DATE_RE.match(a["verified"])):
                v.append(f"{tag}: anchoring_urls[{s!r}].verified {a.get('verified')!r} is not a "
                         f"YYYY-MM-DD date")
    return v


# ---------------------------------------------------------------- one crop
def check_crop(crop, armed=None):
    """Violation strings for one crop ([] == clean). `armed` defaults to PRESENCE_ARMED."""
    armed = PRESENCE_ARMED if armed is None else armed
    slug = crop.get("slug") or crop.get("id")
    pl = crop.get("planting_layout")
    cert = certified(crop)

    if not isinstance(pl, list):
        retired = _retired_key_violations(slug, crop, armed)
        if pl is None:
            if armed and cert:
                return [f"{slug}: planting_layout absent/null on a certified crop; every certified "
                        f"crop carries a list ([] only when zone_independent)"] + retired
            if crop.get("pollination_block_min_rows") is not None:
                return [f"{slug}: pollination_block_min_rows present but planting_layout absent/null"] + retired
            return retired
        if isinstance(pl, str):
            if armed:
                return [f"{slug}: planting_layout {pl!r}: the string form is retired (PLA-10 promote 1); "
                        f"it is a list of entries"] + retired
            return _legacy_violations(slug, crop)
        return [f"{slug}: planting_layout {pl!r} is not a list"] + retired

    v = []
    zi = crop.get("zone_independent") is True
    # check 1
    if zi and pl:
        v.append(f"{slug}: zone_independent crop: planting_layout must be [] (no ground layout), "
                 f"got {len(pl)} entr(y/ies)")
    if not zi and not pl:
        v.append(f"{slug}: planting_layout is []: [] only on a zone_independent crop")
    # checks 2, 4, 5, 6 per entry
    for i, e in enumerate(pl):
        v += _entry_violations(slug, i, e)
    entries = _entries(crop)
    # check 2: ids unique; a shared pair only with a qualifier, at most one unqualified per pair
    ids = [e.get("id") for e in entries if isinstance(e.get("id"), str)]
    for d in sorted({x for x in ids if ids.count(x) > 1}):
        v.append(f"{slug}: duplicate id {d!r} in planting_layout")
    pairs = {}
    for e in entries:
        pairs.setdefault((e.get("arrangement"), e.get("support")), []).append(e.get("id"))
    for (arr, sup), pids in pairs.items():
        if len(pids) == 1 and isinstance(pids[0], str) and pids[0] != f"{arr}-{sup}" \
                and pids[0].startswith(f"{arr}-{sup}-"):
            v.append(f"{slug}: id {pids[0]!r} carries a qualifier but no other entry shares the pair "
                     f"({arr}, {sup}); the qualifier appears only to tell two entries of one pair apart")
    # check 3
    n_def = sum(1 for e in entries if e.get("default") is True)
    if entries and n_def != 1:
        v.append(f"{slug}: exactly one default entry required, found {n_def}")
    # check 4: block entry iff pollination_block_min_rows (int >= 2)
    has_block = any(e.get("arrangement") == "block" for e in entries)
    mr = crop.get("pollination_block_min_rows")
    if mr is not None and not _int_ge(mr, MIN_ROWS_FLOOR):
        v.append(f"{slug}: pollination_block_min_rows {mr!r} not an int >= {MIN_ROWS_FLOOR}")
    if has_block and mr is None:
        v.append(f"{slug}: a block entry requires crop-root pollination_block_min_rows")
    if mr is not None and not has_block:
        v.append(f"{slug}: pollination_block_min_rows present but no block entry")
    # check 7: mirrors
    v += _mirror_violations(slug, crop, entries, zi)
    # check 8
    v += _retired_key_violations(slug, crop, True)
    return v


def _mirror_violations(slug, crop, entries, zi):
    v = []
    for k in MIRROR_KEYS:
        if k not in crop:
            v.append(f"{slug}: crop-root {k} absent; it is a gated mirror of planting_layout and is "
                     f"present (null being a value) on every crop carrying the list")
    sp, rs, rr = crop.get("spacing_inches"), crop.get("row_spacing_inches"), crop.get("row_spacing_reason")
    if zi:
        if sp is not None:
            v.append(f"{slug}: zone_independent crop: spacing_inches must be null (no entry carries a "
                     f"between-plants figure), got {sp!r}")
        if rs is not None:
            v.append(f"{slug}: zone_independent crop: row_spacing_inches must be null, got {rs!r}")
        if rr != "not_applicable":
            v.append(f"{slug}: zone_independent crop: row_spacing_reason must be 'not_applicable', "
                     f"got {rr!r}")
        return v
    if "spacing_inches" in crop:
        exp = expected_spacing(entries)
        if exp is None and sp is not None:
            v.append(f"{slug}: spacing_inches {sp!r} but no entry carries in_row_inches; the mirror "
                     f"is null")
        elif exp is not None and sp != exp:
            v.append(f"{slug}: spacing_inches {sp!r} is not the mirror {exp!r} (the first entry "
                     f"carrying in_row_inches, default first, then declared order)")
    d = default_entry(entries)
    if d is not None and "row_spacing_inches" in crop and rs != d.get("row_spacing_inches"):
        v.append(f"{slug}: row_spacing_inches {rs!r} is not the default entry's "
                 f"{d.get('row_spacing_inches')!r} (follows the default only, no fallback)")
    if rr not in ROOT_REASONS:
        v.append(f"{slug}: row_spacing_reason {rr!r} not in {list(ROOT_REASONS)}")
    elif "row_spacing_reason" in crop:
        if rs is not None and rr is not None:
            v.append(f"{slug}: row_spacing_reason {rr!r} but row_spacing_inches is {rs!r}; the reason "
                     f"is null when the row figure is present")
        elif rs is None and d is not None:
            exp_r = expected_row_reason(crop)
            if exp_r is not None and rr != exp_r:
                v.append(f"{slug}: row_spacing_reason {rr!r} should be {exp_r!r} (see_layout iff a hill "
                         f"default with a row figure on a non-default entry; not_applicable iff "
                         f"zone_independent; else not_authored)")
    return v


def _retired_key_violations(slug, crop, armed):
    if not armed:
        return []
    return [f"{slug}: crop-root {k} is retired (PLA-10 D8 option (b)): the default entry's "
            f"sources/anchoring_urls are the one citation of the in-row figure"
            for k in RETIRED_ROOT_KEYS if k in crop]


# ---------------------------------------------------------------- roster (§1.6 check 9)
def roster(data, armed=None):
    armed = PRESENCE_ARMED if armed is None else armed
    crops = data.get("crops", []) if isinstance(data, dict) else data
    cert = [c for c in crops if certified(c)]
    V = []
    for c in crops:
        V += check_crop(c, armed=armed)
    return {
        "certified": len(cert),
        "entries": sum(len(_entries(c)) for c in cert),
        "list_shaped": sum(1 for c in cert if isinstance(c.get("planting_layout"), list)),
        "legacy": sum(1 for c in cert if isinstance(c.get("planting_layout"), str)),
        "null_spacing": sorted(c.get("slug") for c in cert
                               if isinstance(c.get("planting_layout"), list) and c.get("spacing_inches") is None),
        "violations": V,
    }


def refusal(r, armed=None):
    armed = PRESENCE_ARMED if armed is None else armed
    if r["certified"] == 0:
        return "inspected 0 certified crops"
    if r["certified"] < CERT_FLOOR:
        return f"inspected {r['certified']} certified crops, below the declared floor {CERT_FLOOR}"
    if armed and r["entries"] < ENTRY_FLOOR:
        return f"inspected {r['entries']} planting_layout entries, below the declared floor {ENTRY_FLOOR}"
    return None


def summary(r, armed=None):
    armed = PRESENCE_ARMED if armed is None else armed
    return (f"inspected {r['certified']} certified crops, {r['entries']} entries; {r['list_shaped']} "
            f"list-shaped, {r['legacy']} legacy string; null spacing on {len(r['null_spacing'])}; "
            f"presence {'ARMED' if armed else 'off'}")


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    armed = True if "--armed" in argv else PRESENCE_ARMED
    path = args[0] if args else "crops_data_final.json"
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    r = roster(data, armed=armed)
    for m in r["violations"]:
        print("VIOLATION:", m)
    print(f"planting_layout_gate: {len(r['violations'])} violation(s); {summary(r, armed)}")
    why = refusal(r, armed)
    if why:
        print(f"planting_layout_gate: REFUSED -- {why}. A check that inspected nothing is not a pass.")
        return 2
    return 1 if r["violations"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
