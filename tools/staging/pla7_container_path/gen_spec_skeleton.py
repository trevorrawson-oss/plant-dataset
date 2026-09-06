#!/usr/bin/env python3
"""gen_spec_skeleton -- measure the BASE state and emit the spec skeleton for promote A1.

Reads the pinned pre-state through promote_fixture (never live canonical). Emits every CERTIFIED crop (the 7 shells are skipped and stay byte-identical) with a
PROPOSED container_path: `tray` for the microgreen archetype, null where container_ok is not true,
`rootstock` where a container_suitable rootstock entry exists AND the crop is one of the T1-clear
eight, `direct` otherwise. Every `rootstock` row gets an EMPTY evidence slot the read must fill
with a sentence found exactly once in the crop's own container_notes prose. The read (Task 7) may
change a `direct` to `cultivar` only by adding evidence.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, TOOLS)
import promote_fixture  # noqa: E402

BASE_SHA = "72371c02fa306d8e1849053416baf34e232b80bbdf1af5169d546c12c8f45222"
T1_CLEAR_ROOTSTOCK = {"apple", "pear-european", "pear-asian", "orange-navel",
                      "mandarin-clementine", "grapefruit", "cherry-sweet", "cherry-sour"}
FLIPS = [
    {"crop": "cherry-sweet", "container_ok": True, "min_pot_gallons": 25, "container_recommended": False},
    {"crop": "cherry-sour",  "container_ok": True, "min_pot_gallons": 25, "container_recommended": False},
    {"crop": "mulberry",     "container_ok": True, "min_pot_gallons": 15, "container_recommended": False},
]
VARIETY_FLAGS = [{"crop": "mulberry", "name": "Dwarf Everbearing", "container_min_gallons": 15}]

data = json.loads(promote_fixture.pre_state(BASE_SHA))
flip_slugs = {f["crop"] for f in FLIPS}
paths, gravel, applicable, mech = [], [], [], 0
for c in data["crops"]:
    if not (c.get("verification_status") or {}).get("status"):
        continue  # the 7 shells stay untouched (A39 exempts uncertified shells)
    slug, cn = c["slug"], c.get("container_notes") or {}
    ok_post = cn.get("container_ok") is True or slug in flip_slugs
    if not ok_post:
        value = None
    elif c.get("archetype") == "microgreen":
        value = "tray"
    elif slug in T1_CLEAR_ROOTSTOCK:
        value = "rootstock"
    elif slug == "mulberry":
        value = "cultivar"
    else:
        value = "direct"
    row = {"crop": slug, "container_path": value}
    if value in ("rootstock", "cultivar"):
        row["evidence"] = ""
    paths.append(row)
    if (cn.get("drainage") or {}).get("gravel_layer") == "not_required":
        gravel.append(slug)
    ow = cn.get("overwintering") or {}
    if ok_post and ow.get("applicable") is None:
        applicable.append(slug)
    names = {(v.get("name") or "").strip().lower() for v in ((c.get("varieties") or {}).get("recommended") or [])
             if isinstance(v, dict)}
    mech += sum(1 for n in (cn.get("container_suitable_varieties") or []) if n.strip().lower() in names)

expected = {
    "rows": len(paths),
    "non_null": sum(1 for r in paths if r["container_path"] is not None),
    "null": sum(1 for r in paths if r["container_path"] is None),
    "tray": sum(1 for r in paths if r["container_path"] == "tray"),
    "rootstock": sum(1 for r in paths if r["container_path"] == "rootstock"),
    "cultivar": sum(1 for r in paths if r["container_path"] == "cultivar"),
    "flips": len(FLIPS),
    "variety_flags_mechanical": mech,
    "variety_flags_explicit": len(VARIETY_FLAGS),
    "gravel": len(gravel),
    "applicable": len(applicable),
}
spec = {
    "_what": "PLA-7 promote A1 (spec 2026-09-06 sections 2, 3, 8 step 2). ONE row per crop sets "
             "container_notes.container_path; three flips on the crops whose own notes and rootstock "
             "entries say a pot works (plum HELD for PLA-463); the mechanical migration of every "
             "container_suitable_varieties name that exactly matches a varieties.recommended[] entry "
             "into container_suitable: true; gravel_layer 'not_required' -> false; "
             "overwintering.applicable null -> true where the crop is container_ok and carries "
             "overwintering prose. Evidence on every rootstock/cultivar row is a sentence found EXACTLY "
             "ONCE in that crop's own container_notes prose.",
    "base_sha": BASE_SHA,
    "paths": paths, "flips": FLIPS, "variety_flags": VARIETY_FLAGS,
    "gravel_normalize": gravel, "overwinter_applicable_true": applicable,
    "expected": expected,
}
out = os.path.join(HERE, "spec.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(spec, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(json.dumps(expected, indent=2))
print(f"wrote {out}")
