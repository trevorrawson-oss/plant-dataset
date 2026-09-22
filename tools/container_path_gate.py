#!/usr/bin/env python3
"""container_path_gate -- coherence of container_notes.container_path (PLA-7 spec section 2).

WHAT IT CHECKS, per crop, only when the key is PRESENT (so historical states and the un-migrated
roster stay green):
  rule 1  container_ok true  <=> container_path non-null; the value is one of VALUES
  rule 2  rootstock  => some rootstock_options[] entry has container_suitable true, and, when the
          crop carries rootstock_selection_axis (PLA-463), that axis permits it
  rule 3  cultivar   => some varieties.recommended[] entry has container_suitable true
  rule 4  tray       <=> archetype microgreen, and depth_inches_min is non-null
  flags   varieties.recommended[].container_suitable is bool or null; container_min_gallons only on
          a flagged entry and within [1, 100]

PRESENCE (a certified crop must carry the key; null is a value) is a SEPARATE entry point,
`presence_violations`, and `all_violations(presence=False)` leaves it off by default. DO NOT fold
presence into shape_violations or default it on: the presence floor arms in whole_crop_gate A58
only in the commit that writes the canonical carrying the key (gates arm off the data), and any
caller replaying a historical state must stay green.

Usage: container_path_gate.py [PATH] [--presence]
"""
import json
import sys

VALUES = ("direct", "rootstock", "cultivar", "tray")
AXIS_PERMITS_ROOTSTOCK = {"size_control", "combined"}
CERTIFIED = "verified_gs_arc"


def _cn(crop):
    return crop.get("container_notes") or {}


def _varieties(crop):
    v = crop.get("varieties")
    rec = v.get("recommended") if isinstance(v, dict) else None
    return [x for x in rec if isinstance(x, dict)] if isinstance(rec, list) else []


def _rootstocks(crop):
    r = crop.get("rootstock_options")
    return [x for x in r if isinstance(x, dict)] if isinstance(r, list) else []


def _num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def shape_violations(crop):
    V = []
    slug = crop.get("slug") or "?"
    cn = _cn(crop)
    for v in _varieties(crop):
        nm = v.get("name") or "?"
        if "container_suitable" in v and v["container_suitable"] is not None and not isinstance(v["container_suitable"], bool):
            V.append(f"{slug}/{nm}: container_suitable must be true, false or null, got {v['container_suitable']!r}")
        if "container_min_gallons" in v:
            g = v["container_min_gallons"]
            if v.get("container_suitable") is not True:
                V.append(f"{slug}/{nm}: container_min_gallons present but container_suitable is not true")
            if not (_num(g) and 1 <= g <= 100):
                V.append(f"{slug}/{nm}: container_min_gallons {g!r} outside [1, 100]")
    # PLA-466 1(b). rootstock_options[].container_suitable had NO shape gate: the loop above is
    # scoped to varieties.recommended[]. It was boolean on all 60 rows (45 false / 15 true / 0
    # null) until PLA-466 nulled five, where null means "not assessed" and false would assert an
    # unsourced negative. Gated from here so the three-value domain is enforced rather than assumed.
    for r in _rootstocks(crop):
        nm = r.get("name") or "?"
        if "container_suitable" not in r:
            V.append(f"{slug}/{nm}: rootstock_options entry has no container_suitable key")
            continue
        cs = r["container_suitable"]
        if cs is not None and not isinstance(cs, bool):
            V.append(f"{slug}/{nm}: rootstock container_suitable must be true, false or null, got {cs!r}")
        if cs is not True and r.get("container_size_gallons") is not None:
            V.append(f"{slug}/{nm}: container_size_gallons present but container_suitable is not true")
    if "container_path" not in cn:
        return V
    path = cn["container_path"]
    ok = cn.get("container_ok")
    if path is not None and path not in VALUES:
        V.append(f"{slug}: container_path {path!r} not in {VALUES}")
        return V
    if ok is True and path is None:
        V.append(f"{slug}: container_ok is true but container_path is null (rule 1)")
    if ok is not True and path is not None:
        V.append(f"{slug}: container_ok is {ok!r} but container_path is {path!r}; must be null (rule 1)")
    if path == "rootstock":
        if not any(r.get("container_suitable") is True for r in _rootstocks(crop)):
            V.append(f"{slug}: container_path rootstock but no rootstock_options[] entry is container_suitable (rule 2)")
        axis = crop.get("rootstock_selection_axis")
        if axis is not None and axis not in AXIS_PERMITS_ROOTSTOCK:
            V.append(f"{slug}: container_path rootstock but rootstock_selection_axis {axis!r} does not permit it (rule 2, PLA-463)")
    if path == "cultivar":
        if not any(v.get("container_suitable") is True for v in _varieties(crop)):
            V.append(f"{slug}: container_path cultivar but no varieties.recommended[] entry is container_suitable (rule 3)")
    is_micro = crop.get("archetype") == "microgreen"
    if path == "tray":
        if cn.get("depth_inches_min") is None:
            V.append(f"{slug}: container_path tray but depth_inches_min is null (rule 4)")
        if not is_micro:
            V.append(f"{slug}: container_path tray on archetype {crop.get('archetype')!r}; tray is the microgreen archetype (rule 4)")
    elif path is not None and is_micro:
        V.append(f"{slug}: microgreen archetype must carry container_path tray, got {path!r} (rule 4)")
    return V


def presence_violations(crop):
    if (crop.get("verification_status") or {}).get("status") != CERTIFIED:
        return []
    if "container_path" not in _cn(crop):
        return [f"{crop.get('slug') or '?'}: container_notes.container_path missing (present-or-null on a certified crop)"]
    return []


def all_violations(data, presence=False):
    V = []
    for c in data.get("crops", []):
        V += shape_violations(c)
        if presence:
            V += presence_violations(c)
    return V


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    path = args[0] if args else "crops_data_final.json"
    presence = "--presence" in argv
    with open(path) as fh:
        data = json.load(fh)
    V = all_violations(data, presence=presence)
    for v in V:
        print("VIOLATION:", v)
    carrying = sum(1 for c in data["crops"] if "container_path" in _cn(c))
    print(f"container_path_gate: {len(V)} violation(s); {carrying}/{len(data['crops'])} crops carry the key; "
          f"presence {'ARMED' if presence else 'off'}")
    return 1 if V else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
