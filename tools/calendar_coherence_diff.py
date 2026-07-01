#!/usr/bin/env python3
"""§8.1 exact-cell diff -- the SIGN-OFF surface for the calendar-coherence content release.
Run: python3 tools/calendar_coherence_diff.py <canonical.json> <normalized.json>

Proves the normalizer touched EXACTLY the A37 gate's target set and NOTHING else (Trevor guardrail
#2), and emits the three prior-session review flags (i/ii/iii). Exits non-zero if any COLLATERAL
change is found (a field other than a flagged calendar token or a bridged harvest string), so it
doubles as a safety assertion before any commit."""
import json
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from annual_calendar import parse_months
from calendar_coherence_gate import impossible_growing_months, bridgeable_holes

_MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
_MILD_COAST = {"ca_north_coast", "ca_south_coast"}
_WARM = {"eggplant", "watermelon", "pumpkin", "butternut-squash"}


def _deep_diff(a, b, path, out):
    if type(a) is not type(b):
        out.append((list(path), a, b)); return
    if isinstance(a, dict):
        for k in set(a) | set(b):
            if k not in a or k not in b:
                out.append((path + [k], a.get(k, "<MISSING>"), b.get(k, "<MISSING>"))
                           ); continue
            _deep_diff(a[k], b[k], path + [k], out)
    elif isinstance(a, list):
        if len(a) != len(b):
            out.append((list(path), f"<len {len(a)}>", f"<len {len(b)}>")); return
        for i, (x, y) in enumerate(zip(a, b)):
            _deep_diff(x, y, path + [i], out)
    elif a != b:
        out.append((list(path), a, b))


def main(can_path, norm_path):
    can = json.load(open(can_path, encoding="utf-8"))
    norm = json.load(open(norm_path, encoding="utf-8"))
    can_crops = {c["slug"]: c for c in can["crops"]}
    norm_crops = {c["slug"]: c for c in norm["crops"]}

    # ---- 1. deep diff + collateral check ----
    raw = []
    _deep_diff(can["crops"], norm["crops"], ["crops"], raw)
    token_changes, harvest_changes, collateral = [], [], []
    for path, old, new in raw:
        # path = ['crops', idx, 'regions', <r>, 'resolved_by_zone', <z>, 'calendar', <i>] or [...,'harvest']
        slug = can["crops"][path[1]]["slug"] if len(path) > 1 and isinstance(path[1], int) else "?"
        if len(path) >= 7 and path[2] == "regions" and path[4] == "resolved_by_zone":
            loc = f"{path[3]}.z{path[5]}"
            if path[6] == "calendar" and len(path) == 8:
                token_changes.append((slug, loc, path[7], old, new)); continue
            if path[6] == "harvest" and len(path) == 7:
                harvest_changes.append((slug, loc, old, new)); continue
        collateral.append((slug, path, old, new))

    # ---- 2. changed-set == gate-target-set ----
    tgt_tokens, tgt_holes = set(), set()
    for slug, c in can_crops.items():
        annual = c.get("calendar_basis") == "frost_anchored"
        for rk, r in (c.get("regions") or {}).items():
            for z, cell in ((r or {}).get("resolved_by_zone") or {}).items():
                loc = f"{rk}.z{z}"
                if annual:
                    for i, _blk in impossible_growing_months(cell):
                        tgt_tokens.add((slug, loc, i))
                if bridgeable_holes(cell):
                    tgt_holes.add((slug, loc))
    got_tokens = {(s, l, i) for s, l, i, _o, _n in token_changes}
    got_holes = {(s, l) for s, l, _o, _n in harvest_changes}

    print("=" * 78)
    print("CALENDAR-COHERENCE §8.1 EXACT-CELL DIFF  (sign-off surface)")
    print("=" * 78)
    print(f"token replacements : {len(token_changes)}")
    print(f"harvest bridges    : {len(harvest_changes)}")
    print(f"cells touched      : {len({(s, l) for s, l, *_ in token_changes} | got_holes)}")
    print(f"COLLATERAL changes : {len(collateral)}  (MUST be 0)")
    print(f"changed tokens == gate target tokens : {got_tokens == tgt_tokens}")
    print(f"changed holes  == gate target holes  : {got_holes == tgt_holes}")
    if collateral:
        print("\n!!! COLLATERAL (unexpected) CHANGES -- ABORT:")
        for slug, path, old, new in collateral[:40]:
            print(f"   {slug}: {'.'.join(map(str, path))}: {old!r} -> {new!r}")

    # ---- 3. token replacements grouped by resulting token ----
    print("\n" + "-" * 78 + "\nBUG-1 token replacements (by resulting token)")
    by_new = {}
    for s, l, i, o, n in token_changes:
        by_new.setdefault(n, []).append((s, l, _MON[i], o))
    for n in sorted(by_new):
        print(f"\n  growing -> {n}  ({len(by_new[n])}):")
        for s, l, mon, o in sorted(by_new[n]):
            print(f"     {s} {l} {mon}")

    # ---- 4. harvest bridges ----
    print("\n" + "-" * 78 + "\nBUG-2 harvest bridges")
    for s, l, o, n in sorted(harvest_changes):
        print(f"   {s} {l}:  {o!r}  ->  {n!r}")

    # ---- FLAGS (prior-session review items) ----
    # (i) stronger-invariant catches: impossible growing whose IMMEDIATE predecessor is not `harvest`
    #     (caught via the walk-through relaxation) -- confirm each really traces to harvest/season_over.
    print("\n" + "-" * 78 + "\nFLAG (i) stronger-invariant catches (predecessor != harvest -- confirm the trace)")
    n_i = 0
    for s, l, i, o, n in sorted(token_changes):
        cal = None
        cell = None
        rk, z = l.split(".z")
        cell = can_crops[s]["regions"][rk]["resolved_by_zone"][z]
        cal = cell["calendar"]
        prev = cal[(i - 1) % 12]
        if prev != "harvest":
            # find the blocker it traces to
            blk = dict((ii, b) for ii, b in impossible_growing_months(cell)).get(i)
            print(f"   {s} {l} {_MON[i]}: prev={prev} -> traces to `{blk}`  (growing -> {n})")
            n_i += 1
    if not n_i:
        print("   (none)")

    # (ii) mild-coastal rule-6 shoulders: cold_pause stamped on ca_north/south_coast winter
    print("\n" + "-" * 78 + "\nFLAG (ii) mild-coastal cold_pause (rule 6) -- re-rule any that read as 'waiting'")
    n_ii = 0
    for s, l, i, o, n in sorted(token_changes):
        if n == "cold_pause" and l.split(".z")[0] in _MILD_COAST:
            print(f"   {s} {l} {_MON[i]}: growing -> cold_pause  (mild coast; season_over may be more honest?)")
            n_ii += 1
    if not n_ii:
        print("   (none)")

    # (iii) harvest bridges to spot-check + warm-crop heat_pause tags that must have landed
    print("\n" + "-" * 78 + "\nFLAG (iii) warm-crop heat_pause TAGS (D8 -- authoring-lane candidates, NOT edited to heat_pause)")
    tags = [(s, l, _MON[i]) for s, l, i, o, n in sorted(token_changes)
            if n == "season_over" and s in _WARM and (i + 1) in {6, 7, 8}]
    for s, l, mon in tags:
        print(f"   {s} {l} {mon}: growing -> season_over  [TAG: needs a backed heat_pause later]")
    print(f"   ({len(tags)} tags)")

    ok = (not collateral) and got_tokens == tgt_tokens and got_holes == tgt_holes
    print("\n" + "=" * 78)
    print("DIFF VERDICT:", "CLEAN -- exactly the target set, zero collateral" if ok else "!!! PROBLEM")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
