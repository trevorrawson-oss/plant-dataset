# PLA-7 Promote A1: `container_path` + the variety flag + the three-crop fix -- Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Land `container_notes.container_path` on all 121 certified crops (the 7 shells stay byte-identical; A39 exempts them), `varieties.recommended[].container_suitable` on the 134 exact-name matches plus mulberry, flip cherry-sweet, cherry-sour and mulberry to `container_ok: true` on their own evidence, normalize `gravel_layer`, decide `overwintering.applicable` on 12 crops, and arm the gate that keeps all of it coherent, as ONE replay-pinned, mutation-tested promote held for Trevor's approval.

**Architecture:** A standalone coherence gate (`container_path_gate.py`, rules 1-4 of the spec) wired into `whole_crop_gate` as A58 with its presence floor behind an arming constant; a promote script that reads a staged `spec.json` (one row per crop, evidence quotes for every non-`direct` value), refuses on any drift from the pinned counts, applies deterministically, and verifies blast radius set-first; a guard suite rebuilt from the committed base via `promote_fixture.pre_state`; a mutation harness on the PLA-215 bar. The canonical write is the LAST step and only on approval.

**Tech Stack:** Python 3 stdlib only (json, copy, hashlib, argparse, unittest, subprocess), pytest for running suites, `tools/promote_fixture.py` for the pinned pre-state, the existing gates imported never retyped.

**Spec:** `docs/superpowers/specs/2026-09-06-pla7-container-field-shape-design.md` (sections 2, 3, 6, 7, 8). The measurements are in `docs/kickoffs/54-pla7-container-model-kickoff.md`.

## Global Constraints

- Canonical JSON is COMPACT: `json.dumps(data, separators=(",", ":"), ensure_ascii=False)`, no trailing newline, never `indent=2`.
- `crops_data_final.json` is READ-ONLY until Task 8; every task before it writes only to `tools/`, `tools/staging/`, `docs/`, or a scratch path under `--out`.
- Base canonical is `72371c02fa306d8e1849053416baf34e232b80bbdf1af5169d546c12c8f45222` (commit `4b826e4`, pinned in `promote_fixture.COMMIT_FOR`). Every check runs against `promote_fixture.pre_state(BASE_SHA)`, never live canonical.
- `container_ok` stays a strict boolean. No new value is ever written to it.
- `container_path` values: `direct` | `rootstock` | `cultivar` | `tray` | null. null iff `container_ok` is not `true`.
- No em dashes anywhere (consumer copy or code strings); `--` is fine in docs and comments. American English.
- A promote ships mutation-tested or it does not ship: one mutation per guard family, MUTATION-APPLIED marker + sentinel, positive control, `set(pre) == set(post)` before any value comparison.
- Do not remove or edit any `rootstock_options[]` entry: that array is PLA-463's shape (spec section 2, mulberry amendment).
- Do not add any check to a shared aggregate that historical replay suites call; A58 is wired at the enforcement point (`whole_crop_gate`) and the standalone gate's `main()` only.
- Commit tooling and docs when green; the canonical write holds for Trevor's approval; Trevor confirms every push.

---

## File Structure

| file | responsibility |
|---|---|
| `tools/staging/pla7_container_path/spec.json` | the authored input: 128 `paths` rows, 3 `flips`, explicit `variety_flags`, the `gravel_normalize` and `overwinter_applicable_true` crop lists, all pinned counts |
| `tools/staging/pla7_container_path/gen_spec_skeleton.py` | one-shot generator that measures the base and emits the skeleton the read finalizes (never run against live canonical) |
| `tools/container_path_gate.py` | the coherence gate: `shape_violations(crop)`, `presence_violations(crop)`, `all_violations(data, presence=False)`, CLI |
| `tools/test_container_path_gate.py` | unit tests for every rule, both directions (accepts good input, refuses each defect) |
| `tools/whole_crop_gate.py` | A58 block inserted before the A55 block; `A58_PRESENCE_ARMED` constant |
| `tools/test_gate_container_path_a58.py` | subprocess integration test: A58 fires on a scratch fixture, stays green on live |
| `tools/register_completeness_gate.py` | one `ruled_categorical` clause for `container_path` |
| `tools/promote_pla7_container_path.py` | the promote: check, apply, verify, write |
| `tools/test_promote_pla7_container_path.py` | the guard suite, replay-pinned |
| `tools/mutate_pla7_container_path_suite.py` | the mutation harness |
| `docs/field_addition_register.md` | row 29 |
| `docs/2026-09-xx-pla7-promote-a1-outcome.md` | the write-up at Task 7 (the date is the day Task 7 runs) |

---

### Task 1: Staging skeleton and the pinned counts

**Files:**
- Create: `tools/staging/pla7_container_path/gen_spec_skeleton.py`
- Create: `tools/staging/pla7_container_path/spec.json` (generated, then hand-finished in Task 7)

**Interfaces:**
- Produces: `spec.json` with top-level keys `_what`, `base_sha`, `paths` (one row per CERTIFIED crop: `{crop, container_path, evidence}`), `flips` (list of `{crop, container_ok, min_pot_gallons, container_recommended}`), `variety_flags` (list of `{crop, name, container_min_gallons}`), `gravel_normalize` (list of slugs), `overwinter_applicable_true` (list of slugs), `expected` (dict of the pinned counts). Every later task reads exactly these keys.

- [ ] **Step 1: Write the generator**

```python
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
```

- [ ] **Step 2: Run it and check the printed counts against the kickoff**

Run: `python3 tools/staging/pla7_container_path/gen_spec_skeleton.py`
Expected output (these are the measured literals; a different number means the base moved or the generator is wrong, stop and find out which):

```
"rows": 121, "non_null": 110, "null": 11, "tray": 8, "rootstock": 8, "cultivar": 1,
"flips": 3, "variety_flags_mechanical": 134, "variety_flags_explicit": 1, "gravel": 16, "applicable": 12
```

- [ ] **Step 3: Confirm the 12 `overwinter_applicable_true` slugs are exactly these**

`apple, lemon, pear-european, pear-asian, lime, orange-navel, mandarin-clementine, pomegranate, grapefruit, cherry-sweet, cherry-sour, mulberry`. Run: `python3 -c "import json;print(json.load(open('tools/staging/pla7_container_path/spec.json'))['overwinter_applicable_true'])"`

- [ ] **Step 4: Commit the skeleton**

```bash
git add tools/staging/pla7_container_path/
git commit -m "tooling(pla7): promote A1 staging skeleton, measured on 72371c02 (121 rows, 3 flips, 134+1 flags, 16 gravel, 12 applicable)"
```

---

### Task 2: The coherence gate, tests first

**Files:**
- Create: `tools/test_container_path_gate.py`
- Create: `tools/container_path_gate.py`

**Interfaces:**
- Produces: `container_path_gate.VALUES` (tuple), `shape_violations(crop) -> list[str]`, `presence_violations(crop) -> list[str]`, `all_violations(data, presence=False) -> list[str]`, `main(argv) -> int`. The promote (Task 4) imports `all_violations`; `whole_crop_gate` (Task 3) imports both per-crop functions.

- [ ] **Step 1: Write the failing tests**

```python
#!/usr/bin/env python3
"""Tests for container_path_gate (PLA-7 spec section 2 rules 1-4, section 7).
Run: python3 -m pytest tools/test_container_path_gate.py -q"""
import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from container_path_gate import shape_violations, presence_violations, all_violations, VALUES


def crop(path, ok=True, archetype="warm_season_fruiting", depth=None, rootstocks=None, varieties=None,
         axis=None, certified=True, key=True):
    cn = {"container_ok": ok, "min_pot_gallons": 5, "depth_inches_min": depth}
    if key:
        cn["container_path"] = path
    c = {"slug": "x", "archetype": archetype, "container_notes": cn,
         "verification_status": {"status": "verified_gs_arc" if certified else None}}
    if rootstocks is not None:
        c["rootstock_options"] = rootstocks
    if varieties is not None:
        c["varieties"] = {"recommended": varieties}
    if axis is not None:
        c["rootstock_selection_axis"] = axis
    return c


class Rule1(unittest.TestCase):
    def test_direct_on_ok_true_is_clean(self):
        self.assertEqual(shape_violations(crop("direct")), [])
    def test_null_on_ok_false_is_clean(self):
        self.assertEqual(shape_violations(crop(None, ok=False)), [])
    def test_null_on_ok_null_is_clean(self):
        self.assertEqual(shape_violations(crop(None, ok=None)), [])
    def test_refuses_null_path_on_ok_true(self):
        self.assertTrue(any("rule 1" in v for v in shape_violations(crop(None))))
    def test_refuses_a_path_on_ok_false(self):
        self.assertTrue(any("rule 1" in v for v in shape_violations(crop("direct", ok=False))))
    def test_refuses_an_unknown_value(self):
        self.assertTrue(any("not in" in v for v in shape_violations(crop("dwarf_rootstock"))))
    def test_absent_key_is_not_a_shape_violation(self):
        self.assertEqual(shape_violations(crop(None, key=False)), [])


class Rule2(unittest.TestCase):
    def test_rootstock_with_a_suitable_entry_is_clean(self):
        self.assertEqual(shape_violations(crop("rootstock", rootstocks=[{"name": "M9", "container_suitable": True}])), [])
    def test_refuses_rootstock_with_no_suitable_entry(self):
        v = shape_violations(crop("rootstock", rootstocks=[{"name": "seedling", "container_suitable": False}]))
        self.assertTrue(any("rule 2" in x for x in v))
    def test_refuses_rootstock_with_no_rootstock_array(self):
        self.assertTrue(any("rule 2" in x for x in shape_violations(crop("rootstock"))))
    def test_axis_permits_size_control_and_combined(self):
        for ax in ("size_control", "combined"):
            self.assertEqual(shape_violations(crop("rootstock", rootstocks=[{"container_suitable": True}], axis=ax)), [])
    def test_refuses_rootstock_when_the_axis_forbids_it(self):
        v = shape_violations(crop("rootstock", rootstocks=[{"container_suitable": True}], axis="soil_and_pest"))
        self.assertTrue(any("PLA-463" in x for x in v))


class Rule3(unittest.TestCase):
    def test_cultivar_with_a_flagged_variety_is_clean(self):
        self.assertEqual(shape_violations(crop("cultivar", varieties=[{"name": "Astia", "container_suitable": True}])), [])
    def test_refuses_cultivar_with_no_flagged_variety(self):
        v = shape_violations(crop("cultivar", varieties=[{"name": "Costata", "container_suitable": False}]))
        self.assertTrue(any("rule 3" in x for x in v))
    def test_refuses_cultivar_with_string_varieties(self):
        self.assertTrue(any("rule 3" in x for x in shape_violations(crop("cultivar", varieties=["Astia"]))))


class Rule4(unittest.TestCase):
    def test_tray_on_microgreen_with_depth_is_clean(self):
        self.assertEqual(shape_violations(crop("tray", archetype="microgreen", depth=1)), [])
    def test_refuses_tray_without_depth(self):
        self.assertTrue(any("rule 4" in x for x in shape_violations(crop("tray", archetype="microgreen"))))
    def test_refuses_tray_off_the_microgreen_archetype(self):
        self.assertTrue(any("rule 4" in x for x in shape_violations(crop("tray", depth=1))))
    def test_refuses_direct_on_a_microgreen(self):
        self.assertTrue(any("rule 4" in x for x in shape_violations(crop("direct", archetype="microgreen", depth=1))))


class VarietyFlag(unittest.TestCase):
    def test_min_gallons_on_a_flagged_variety_is_clean(self):
        self.assertEqual(shape_violations(crop("direct", varieties=[{"name": "A", "container_suitable": True, "container_min_gallons": 15}])), [])
    def test_refuses_min_gallons_on_an_unflagged_variety(self):
        v = shape_violations(crop("direct", varieties=[{"name": "A", "container_suitable": False, "container_min_gallons": 15}]))
        self.assertTrue(any("container_min_gallons" in x for x in v))
    def test_refuses_min_gallons_out_of_bounds(self):
        v = shape_violations(crop("direct", varieties=[{"name": "A", "container_suitable": True, "container_min_gallons": 0}]))
        self.assertTrue(any("[1, 100]" in x for x in v))
    def test_refuses_a_non_boolean_flag(self):
        v = shape_violations(crop("direct", varieties=[{"name": "A", "container_suitable": "yes"}]))
        self.assertTrue(any("container_suitable" in x for x in v))
    def test_null_flag_is_clean(self):
        self.assertEqual(shape_violations(crop("direct", varieties=[{"name": "A", "container_suitable": None}])), [])


class Presence(unittest.TestCase):
    def test_certified_crop_missing_the_key_is_a_presence_violation(self):
        self.assertEqual(len(presence_violations(crop(None, key=False))), 1)
    def test_certified_crop_with_null_key_is_clean(self):
        self.assertEqual(presence_violations(crop(None, ok=False)), [])
    def test_uncertified_shell_is_exempt(self):
        self.assertEqual(presence_violations(crop(None, key=False, certified=False)), [])
    def test_all_violations_presence_off_by_default(self):
        data = {"crops": [crop(None, key=False)]}
        self.assertEqual(all_violations(data), [])
        self.assertEqual(len(all_violations(data, presence=True)), 1)


class Values(unittest.TestCase):
    def test_the_enum_is_the_spec_enum(self):
        self.assertEqual(VALUES, ("direct", "rootstock", "cultivar", "tray"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run to verify it fails**

Run: `python3 -m pytest tools/test_container_path_gate.py -q`
Expected: collection error, `ModuleNotFoundError: No module named 'container_path_gate'`

- [ ] **Step 3: Write the gate**

```python
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
```

- [ ] **Step 4: Run the tests**

Run: `python3 -m pytest tools/test_container_path_gate.py -q`
Expected: `28 passed`

- [ ] **Step 5: Prove the gate is a no-op on live canonical (no crop carries the key yet)**

Run: `python3 tools/container_path_gate.py`
Expected: `container_path_gate: 0 violation(s); 0/128 crops carry the key; presence off`
Run: `python3 tools/container_path_gate.py --presence`
Expected: `121` violations (every certified crop lacks the key). That number is the reason the presence floor is NOT armed until Task 8.

- [ ] **Step 6: Commit**

```bash
git add tools/container_path_gate.py tools/test_container_path_gate.py
git commit -m "gate(pla7): container_path_gate -- rules 1-4 + variety flag shape, presence as a separate entry point (28 tests)"
```

---

### Task 3: Wire A58 into whole_crop_gate, rule the key in register_completeness

**Files:**
- Modify: `tools/whole_crop_gate.py` (insert before the line `# ---------------- A55. perennial year-pill coherence (PLA-6 Round 2) ----------------`, which follows the A57 block)
- Modify: `tools/register_completeness_gate.py:195` (the `saucer_practice` clause; add one clause after it)
- Create: `tools/test_gate_container_path_a58.py`

**Interfaces:**
- Consumes: `container_path_gate.shape_violations`, `container_path_gate.presence_violations`
- Produces: the module-level constant `A58_PRESENCE_ARMED` in `whole_crop_gate.py` (Task 8 flips it to `True`)

- [ ] **Step 1: Write the failing integration test**

```python
#!/usr/bin/env python3
"""Integration test: whole_crop_gate A58 (container_path) fires on a scratch fixture and is a
no-op on today's canonical. Run: python3 tools/test_gate_container_path_a58.py"""
import copy, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
base = json.load(open(os.path.join(REPO, "crops_data_final.json")))


def gate(slug, mutate):
    d = copy.deepcopy(base)
    c = next(x for x in d["crops"] if x["slug"] == slug)
    mutate(c)
    tmp = os.path.join(HERE, "_tmp_a58_fixture.json")
    with open(tmp, "w") as f:
        json.dump(d, f, separators=(",", ":"), ensure_ascii=False)
    try:
        return subprocess.run([sys.executable, os.path.join(HERE, "whole_crop_gate.py"), slug, tmp],
                              capture_output=True, text=True).stdout
    finally:
        os.remove(tmp)


# The block is present and announced.
out = gate("cherry-tomato", lambda c: None)
assert "A58. container_path coherence" in out, "A58 block missing from whole_crop_gate"
# No key on live canonical: A58 is a no-op, the gate is still PASS for a passing crop.
assert "container-path:" not in out, out
# A rule-1 defect on a scratch copy bounces.
out = gate("cherry-tomato", lambda c: c["container_notes"].__setitem__("container_path", None))
assert "container-path:" in out and "rule 1" in out, out
# An unknown value bounces.
out = gate("cherry-tomato", lambda c: c["container_notes"].__setitem__("container_path", "dwarf_rootstock"))
assert "container-path:" in out and "not in" in out, out
# A good value on a good crop is clean.
out = gate("cherry-tomato", lambda c: c["container_notes"].__setitem__("container_path", "direct"))
assert "container-path:" not in out, out
# Presence is NOT armed yet: a certified crop without the key is not flagged.
src = open(os.path.join(HERE, "whole_crop_gate.py")).read()
assert "A58_PRESENCE_ARMED = False" in src, "presence floor must stay unarmed until the canonical carries the key (Task 8)"
print("PASS gate A58 container_path")
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python3 tools/test_gate_container_path_a58.py`
Expected: `AssertionError: A58 block missing from whole_crop_gate`

- [ ] **Step 3: Insert the A58 block**

Insert this text immediately BEFORE the line `# ---------------- A55. perennial year-pill coherence (PLA-6 Round 2) ----------------` in `tools/whole_crop_gate.py`:

```python
# ---------------- A58. container_path coherence (PLA-7 spec 2026-09-06, section 2) ----------------
# SHAPE fires only when container_notes.container_path is PRESENT, so this arms GREEN on 72371c02
# (0/128 crops carry the key) and stays green on every historical state. The PRESENCE floor (a
# certified crop must carry the key, null being a value) is behind A58_PRESENCE_ARMED and flips to
# True in the SAME commit that writes the canonical carrying the key -- never before: armed early it
# would redden gate_all on live canonical and flood a parallel session (gates arm off the data).
# No replay suite runs whole_crop_gate on a historical state (grepped 2026-09-06), so this is the
# enforcement point for the shipping roster, and container_path_gate.all_violations keeps presence
# OFF by default for the same reason.
from container_path_gate import shape_violations as _cp_shape, presence_violations as _cp_presence
A58_PRESENCE_ARMED = False
print(f"A58. container_path coherence (rules 1-4 + variety flag shape; presence {'ARMED' if A58_PRESENCE_ARMED else 'off'})")
_cpv = _cp_shape(crop) + (_cp_presence(crop) if A58_PRESENCE_ARMED else [])
print(f"  container-path violations: {len(_cpv)}")
for m in _cpv:
    fail(f"container-path: {m}")

```

- [ ] **Step 4: Add the register_completeness ruling clause**

In `tools/register_completeness_gate.py`, directly after the line that begins `    if k == "saucer_practice" and "container_notes" in pat: return True`, add:

```python
    if k == "container_path" and "container_notes" in pat: return True  # PLA-7 (2026-09-06): a closed enum naming the JOIN a consumer follows (direct|rootstock|cultivar|tray), machinery not prose; its consumer copy is the crop-level notes_* pair, which stay checked
```

- [ ] **Step 5: Run the integration test and the two neighbours**

Run: `python3 tools/test_gate_container_path_a58.py`
Expected: `PASS gate A58 container_path`
Run: `python3 tools/test_gate_container_tray.py`
Expected: `PASS gate container tray model`
Run: `python3 tools/whole_crop_gate.py apple | tail -3`
Expected: the last line is `GATE: PASS ...` and the A58 line reads `container-path violations: 0`

- [ ] **Step 6: Prove the roster is untouched by the wiring**

Run: `python3 tools/gate_all.py | tail -2`
Expected: `121/121` PASS (the same figure as the 2026-09-06 state). Any other figure means A58 armed on data it reddens; stop.

- [ ] **Step 7: Commit**

```bash
git add tools/whole_crop_gate.py tools/register_completeness_gate.py tools/test_gate_container_path_a58.py
git commit -m "gate(pla7): A58 container_path coherence wired (shape armed green on 72371c02, presence behind A58_PRESENCE_ARMED=False); register_completeness rules the enum"
```

---

### Task 4: The promote script

**Files:**
- Create: `tools/promote_pla7_container_path.py`

**Interfaces:**
- Consumes: `spec.json` (Task 1 keys), `container_path_gate.all_violations`, `display_readiness_gate.display_readiness_violations`, `numeric_sanity_gate.numeric_sanity_violations`
- Produces: `BASE_SHA`, the `EXPECTED_*` pins, `sha256_bytes(b)`, `serialize(data) -> bytes`, `by_slug(data) -> dict`, `load_canonical(path=None)`, `staged() -> dict`, `prose_leaves(cn) -> list[str]`, `mechanical_flags(data) -> set[(slug, name)]`, `check_spec_shape(spec) -> int`, `check_pre_state(spec, data) -> int`, `apply_to(data, spec) -> dict`, `check_post(post, spec)`, `verify_post(pre, post, spec) -> int`, `main()`. The suite (Task 5) and harness (Task 6) depend on these exact names and on the exact refusal strings below.

- [ ] **Step 1: Write the promote**

```python
#!/usr/bin/env python3
"""promote_pla7_container_path -- PLA-7 promote A1 (spec docs/superpowers/specs/2026-09-06-pla7-container-field-shape-design.md
sections 2, 3, 8 step 2). Base 72371c02.

WHAT MOVES. (1) container_notes.container_path on all 121 certified crops, one row each, null where
container_ok is not true; the 7 shells are not touched (A39 exempts uncertified shells). (2) THREE flips: cherry-sweet, cherry-sour, mulberry become container_ok true with a pot
figure and container_recommended false, on their own notes and rootstock entries (plum is HELD for
PLA-463). (3) The mechanical migration: every container_suitable_varieties[] name that EXACTLY matches
a varieties.recommended[] entry's name (case-insensitive, trimmed) gets container_suitable: true on
that entry; the bare list is left in place for the consumers that still read it. (4) Explicit variety
flags from the spec (mulberry's Dwarf Everbearing, with container_min_gallons 15). (5) gravel_layer
'not_required' -> false. (6) overwintering.applicable null -> true on container-ok crops carrying
overwintering prose. Nothing else.

WHY EACH GUARD EXISTS.
 1. ONE ROW PER CROP, PINNED COUNTS. Every crop appears exactly once; the non-null / null / tray /
    rootstock / cultivar counts are literals pinned BEFORE the first run. A count drift refuses.
 2. EVIDENCE IS PART OF THE ROW. Every rootstock or cultivar row carries a sentence that must be found
    EXACTLY ONCE across that crop's own container_notes prose. A value nobody can point at refuses.
 3. THE FLIPS ARE READ FROM THE PRE-STATE. Each flip crop must be container_ok false with a null pot
    figure before, and must carry a container_suitable rootstock entry (cherries) or a flagged
    variety (mulberry) after. A flip on a crop already true, or with no join to follow, refuses.
 4. THE GATE IS RUN HERE, NOT AT THE GAUNTLET, with presence ON: container_path_gate.all_violations
    on the post-state must be empty, and display_readiness / numeric_sanity on the flipped crops too.
 5. THE MIGRATION IS PINNED: exactly EXPECTED_FLAGS_MECHANICAL exact-name matches, and the set of
    gravel and applicable rows equals the set the pre-state says needs them (none missed, none extra).
 6. BLAST RADIUS AT THE LEAF: set comparisons before value comparisons; only container_notes and
    varieties.recommended may differ; within them only the declared keys; the leaf count is pinned.

Usage:
    promote_pla7_container_path.py --check
    promote_pla7_container_path.py --out /path/scratch.json
    promote_pla7_container_path.py --expect-sha <sha>       # writes canonical (Task 8, on approval)
"""
import argparse, copy, hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CANON = os.path.join(REPO, "crops_data_final.json")
STAGE = os.path.join(HERE, "staging", "pla7_container_path")
SPEC = os.path.join(STAGE, "spec.json")

sys.path.insert(0, HERE)
import container_path_gate as CPG  # noqa: E402  -- imported, never retyped
from display_readiness_gate import display_readiness_violations  # noqa: E402
from numeric_sanity_gate import numeric_sanity_violations  # noqa: E402

BASE_SHA = "72371c02fa306d8e1849053416baf34e232b80bbdf1af5169d546c12c8f45222"  # PLA-450 Option B, 4b826e4
VALUES = CPG.VALUES
EVIDENCE_VALUES = ("rootstock", "cultivar")
ROSTER = 128

# Pinned BEFORE the first run, from gen_spec_skeleton on 72371c02. The read (Task 7) may raise
# EXPECTED_ROOTSTOCK (lemon, lime) or EXPECTED_CULTIVAR; it changes these literals and the suite's
# copies together, BEFORE running, and records why in the outcome doc.
EXPECTED_ROWS = 121
EXPECTED_NON_NULL = 110
EXPECTED_NULL = 11
EXPECTED_TRAY = 8
EXPECTED_ROOTSTOCK = 8
EXPECTED_CULTIVAR = 1
EXPECTED_FLIPS = 3
EXPECTED_FLAGS_MECHANICAL = 134
EXPECTED_FLAGS_EXPLICIT = 1
EXPECTED_GRAVEL = 16
EXPECTED_APPLICABLE = 12
FLIP_KEYS = ("container_ok", "min_pot_gallons", "container_recommended")
# 121 keys + 3 flips x 3 keys + 134 + 1 flags + 1 min_gallons + 16 gravel + 12 applicable
EXPECTED_LEAVES = 121 + 9 + 134 + 1 + 1 + 16 + 12


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


def prose_leaves(cn):
    """Every string leaf under container_notes except sources/anchoring_urls."""
    out = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("sources", "anchoring_urls"):
                    continue
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif isinstance(o, str):
            out.append(o)
    walk(cn)
    return out


def _varieties(crop):
    v = crop.get("varieties")
    rec = v.get("recommended") if isinstance(v, dict) else None
    return [x for x in rec if isinstance(x, dict)] if isinstance(rec, list) else []


def mechanical_flags(data):
    """(slug, exact variety name) for every container_suitable_varieties name that matches an entry."""
    found = set()
    for c in data["crops"]:
        cn = c.get("container_notes") or {}
        names = {(v.get("name") or "").strip().lower(): v.get("name") for v in _varieties(c)}
        for n in cn.get("container_suitable_varieties") or []:
            key = n.strip().lower()
            if key in names:
                found.add((c["slug"], names[key]))
    return found


def check_spec_shape(spec):
    if spec.get("base_sha") != BASE_SHA:
        raise SystemExit("REFUSED: spec base_sha is not the pinned base")
    rows = spec["paths"]
    if len(rows) != EXPECTED_ROWS:
        raise SystemExit(f"REFUSED: {len(rows)} path rows, pinned {EXPECTED_ROWS}")
    seen = set()
    for r in rows:
        if r["crop"] in seen:
            raise SystemExit(f"REFUSED: crop {r['crop']} appears twice in paths")
        seen.add(r["crop"])
        v = r["container_path"]
        if v is not None and v not in VALUES:
            raise SystemExit(f"REFUSED: {r['crop']} container_path {v!r} not in {VALUES}")
        if v in EVIDENCE_VALUES and not (r.get("evidence") or "").strip():
            raise SystemExit(f"REFUSED: {r['crop']} is {v} without evidence")
        if v not in EVIDENCE_VALUES and r.get("evidence"):
            raise SystemExit(f"REFUSED: {r['crop']} carries evidence on a {v!r} row")
    counts = {
        "non_null": sum(1 for r in rows if r["container_path"] is not None),
        "null": sum(1 for r in rows if r["container_path"] is None),
        "tray": sum(1 for r in rows if r["container_path"] == "tray"),
        "rootstock": sum(1 for r in rows if r["container_path"] == "rootstock"),
        "cultivar": sum(1 for r in rows if r["container_path"] == "cultivar"),
    }
    pins = {"non_null": EXPECTED_NON_NULL, "null": EXPECTED_NULL, "tray": EXPECTED_TRAY,
            "rootstock": EXPECTED_ROOTSTOCK, "cultivar": EXPECTED_CULTIVAR}
    for k in pins:
        if counts[k] != pins[k]:
            raise SystemExit(f"REFUSED: {k} rows {counts[k]}, pinned {pins[k]}")
    flips = spec["flips"]
    if len(flips) != EXPECTED_FLIPS:
        raise SystemExit(f"REFUSED: {len(flips)} flips, pinned {EXPECTED_FLIPS}")
    for f in flips:
        if set(f) != {"crop"} | set(FLIP_KEYS):
            raise SystemExit(f"REFUSED: flip {f.get('crop')} keys {sorted(f)}")
        if f["container_ok"] is not True or f["container_recommended"] is not False:
            raise SystemExit(f"REFUSED: flip {f['crop']} must set container_ok true and container_recommended false")
        if not (isinstance(f["min_pot_gallons"], int) and 1 <= f["min_pot_gallons"] <= 100):
            raise SystemExit(f"REFUSED: flip {f['crop']} min_pot_gallons {f['min_pot_gallons']!r}")
    if len(spec["variety_flags"]) != EXPECTED_FLAGS_EXPLICIT:
        raise SystemExit(f"REFUSED: {len(spec['variety_flags'])} explicit variety flags, pinned {EXPECTED_FLAGS_EXPLICIT}")
    if len(spec["gravel_normalize"]) != EXPECTED_GRAVEL:
        raise SystemExit(f"REFUSED: {len(spec['gravel_normalize'])} gravel rows, pinned {EXPECTED_GRAVEL}")
    if len(spec["overwinter_applicable_true"]) != EXPECTED_APPLICABLE:
        raise SystemExit(f"REFUSED: {len(spec['overwinter_applicable_true'])} applicable rows, pinned {EXPECTED_APPLICABLE}")
    return len(rows)


def check_pre_state(spec, data):
    idx = by_slug(data)
    certified = {c["slug"] for c in data["crops"] if (c.get("verification_status") or {}).get("status")}
    if certified != {r["crop"] for r in spec["paths"]}:
        raise SystemExit("REFUSED: the spec's crops are not the certified roster")
    flips = {f["crop"]: f for f in spec["flips"]}
    for c in data["crops"]:
        cn = c.get("container_notes") or {}
        if "container_path" in cn:
            raise SystemExit(f"REFUSED: {c['slug']} already carries container_path")
        for v in _varieties(c):
            if "container_suitable" in v or "container_min_gallons" in v:
                raise SystemExit(f"REFUSED: {c['slug']}/{v.get('name')} already carries a variety container key")
    for r in spec["paths"]:
        c = idx[r["crop"]]
        cn = c.get("container_notes") or {}
        ok_post = cn.get("container_ok") is True or r["crop"] in flips
        if (r["container_path"] is not None) != ok_post:
            raise SystemExit(f"REFUSED: {r['crop']} row is {r['container_path']!r} but container_ok will be {ok_post}")
        if r["container_path"] in EVIDENCE_VALUES:
            hits = sum(leaf.count(r["evidence"]) for leaf in prose_leaves(cn))
            if hits != 1:
                raise SystemExit(f"REFUSED: {r['crop']} evidence found {hits} times in its container_notes prose, needs exactly 1")
        if r["container_path"] == "rootstock":
            if not any(x.get("container_suitable") is True for x in (c.get("rootstock_options") or []) if isinstance(x, dict)):
                raise SystemExit(f"REFUSED: {r['crop']} is rootstock with no container_suitable rootstock entry")
    for slug, f in flips.items():
        cn = idx[slug].get("container_notes") or {}
        if cn.get("container_ok") is not False or cn.get("min_pot_gallons") is not None:
            raise SystemExit(f"REFUSED: flip {slug} is not container_ok false with a null pot figure on the base")
    want_gravel = {c["slug"] for c in data["crops"]
                   if ((c.get("container_notes") or {}).get("drainage") or {}).get("gravel_layer") == "not_required"}
    if set(spec["gravel_normalize"]) != want_gravel:
        raise SystemExit(f"REFUSED: gravel rows differ from the base's not_required set by {sorted(set(spec['gravel_normalize']) ^ want_gravel)}")
    want_app = set()
    for c in data["crops"]:
        if c["slug"] not in certified:
            continue
        cn = c.get("container_notes") or {}
        ok_post = cn.get("container_ok") is True or c["slug"] in flips
        ow = cn.get("overwintering") or {}
        if ok_post and ow.get("applicable") is None:
            if not (ow.get("approach_seasoned") or cn.get("container_overwintering_seasoned")):
                raise SystemExit(f"REFUSED: {c['slug']} would take applicable true with no overwintering prose")
            want_app.add(c["slug"])
    if set(spec["overwinter_applicable_true"]) != want_app:
        raise SystemExit(f"REFUSED: applicable rows differ from the base by {sorted(set(spec['overwinter_applicable_true']) ^ want_app)}")
    mech = mechanical_flags(data)
    if len(mech) != EXPECTED_FLAGS_MECHANICAL:
        raise SystemExit(f"REFUSED: {len(mech)} exact-name variety matches, pinned {EXPECTED_FLAGS_MECHANICAL}")
    for vf in spec["variety_flags"]:
        c = idx[vf["crop"]]
        ent = [v for v in _varieties(c) if (v.get("name") or "") == vf["name"]]
        if len(ent) != 1:
            raise SystemExit(f"REFUSED: variety flag {vf['crop']}/{vf['name']} matches {len(ent)} entries")
        if (vf["crop"], vf["name"]) in mech:
            raise SystemExit(f"REFUSED: explicit flag {vf['crop']}/{vf['name']} duplicates a mechanical match")
    return len(spec["paths"])


def apply_to(data, spec):
    post = copy.deepcopy(data)
    idx = by_slug(post)
    for r in spec["paths"]:
        idx[r["crop"]]["container_notes"]["container_path"] = r["container_path"]
    for f in spec["flips"]:
        cn = idx[f["crop"]]["container_notes"]
        for k in FLIP_KEYS:
            cn[k] = f[k]
    for slug, name in mechanical_flags(data):
        for v in _varieties(idx[slug]):
            if (v.get("name") or "") == name:
                v["container_suitable"] = True
    for vf in spec["variety_flags"]:
        for v in _varieties(idx[vf["crop"]]):
            if (v.get("name") or "") == vf["name"]:
                v["container_suitable"] = True
                v["container_min_gallons"] = vf["container_min_gallons"]
    for slug in spec["gravel_normalize"]:
        idx[slug]["container_notes"]["drainage"]["gravel_layer"] = False
    for slug in spec["overwinter_applicable_true"]:
        idx[slug]["container_notes"]["overwintering"]["applicable"] = True
    return post


def check_post(post, spec):
    v = CPG.all_violations(post, presence=True)
    if v:
        raise SystemExit("REFUSED: container_path_gate on the post-state: " + "; ".join(v[:5]))
    idx = by_slug(post)
    for f in spec["flips"]:
        dv = display_readiness_violations(idx[f["crop"]])
        if dv:
            raise SystemExit(f"REFUSED: display_readiness on flipped {f['crop']}: {dv}")
        nv = numeric_sanity_violations(idx[f["crop"]])
        if nv:
            raise SystemExit(f"REFUSED: numeric_sanity on flipped {f['crop']}: {nv}")


def _j(x):
    return json.dumps(x, sort_keys=True)


def verify_post(pre, post, spec):
    """SET COMPARISON BEFORE VALUE COMPARISON."""
    if set(pre) != set(post):
        raise SystemExit("REFUSED: top-level key set changed")
    for k in pre:
        if k != "crops" and _j(pre[k]) != _j(post[k]):
            raise SystemExit(f"REFUSED: top-level key {k!r} changed")
    pre_i, post_i = by_slug(pre), by_slug(post)
    if set(pre_i) != set(post_i) or len(pre["crops"]) != len(post["crops"]):
        raise SystemExit("REFUSED: crop roster changed")
    flips = {f["crop"]: f for f in spec["flips"]}
    gravel = set(spec["gravel_normalize"])
    applic = set(spec["overwinter_applicable_true"])
    allowed_flags = mechanical_flags(pre) | {(vf["crop"], vf["name"]) for vf in spec["variety_flags"]}
    explicit = {(vf["crop"], vf["name"]): vf for vf in spec["variety_flags"]}
    row_crops = {r["crop"] for r in spec["paths"]}
    leaves = 0
    for slug in pre_i:
        s, g = pre_i[slug], post_i[slug]
        if slug not in row_crops:
            if _j(s) != _j(g):
                raise SystemExit(f"REFUSED: shell {slug} changed")
            continue
        if set(s) != set(g):
            raise SystemExit(f"REFUSED: {slug} crop-level key set changed")
        for k in s:
            if k in ("container_notes", "varieties"):
                continue
            if _j(s[k]) != _j(g[k]):
                raise SystemExit(f"REFUSED: {slug} field {k!r} changed outside container_notes/varieties")
        scn, gcn = s["container_notes"], g["container_notes"]
        if set(gcn) - set(scn) != {"container_path"} or set(scn) - set(gcn):
            raise SystemExit(f"REFUSED: {slug} container_notes key set changed other than by adding container_path")
        leaves += 1
        for k in scn:
            if _j(scn[k]) == _j(gcn[k]):
                continue
            if k in FLIP_KEYS and slug in flips and gcn[k] == flips[slug][k]:
                leaves += 1
            elif k == "drainage" and slug in gravel:
                if {kk for kk in scn[k] if _j(scn[k][kk]) != _j(gcn[k].get(kk))} != {"gravel_layer"} or gcn[k]["gravel_layer"] is not False:
                    raise SystemExit(f"REFUSED: {slug} drainage changed other than gravel_layer -> false")
                leaves += 1
            elif k == "overwintering" and slug in applic:
                if {kk for kk in scn[k] if _j(scn[k][kk]) != _j(gcn[k].get(kk))} != {"applicable"} or gcn[k]["applicable"] is not True:
                    raise SystemExit(f"REFUSED: {slug} overwintering changed other than applicable -> true")
                leaves += 1
            else:
                raise SystemExit(f"REFUSED: {slug} container_notes.{k} changed without a spec row")
        sv, gv = _varieties(s), _varieties(g)
        if _j(s.get("varieties")) != _j(g.get("varieties")):
            if len(sv) != len(gv):
                raise SystemExit(f"REFUSED: {slug} variety entry count changed")
            for a, b in zip(sv, gv):
                added = set(b) - set(a)
                if set(a) - set(b):
                    raise SystemExit(f"REFUSED: {slug}/{a.get('name')} lost a variety key")
                for k in a:
                    if _j(a[k]) != _j(b[k]):
                        raise SystemExit(f"REFUSED: {slug}/{a.get('name')} variety field {k!r} changed")
                if not added:
                    continue
                key = (slug, b.get("name") or "")
                if key not in allowed_flags:
                    raise SystemExit(f"REFUSED: {slug}/{b.get('name')} gained {sorted(added)} without a match or a row")
                want = {"container_suitable"} | ({"container_min_gallons"} if key in explicit else set())
                if added != want or b["container_suitable"] is not True:
                    raise SystemExit(f"REFUSED: {slug}/{b.get('name')} gained {sorted(added)}, expected {sorted(want)}")
                leaves += len(added)
    if leaves != EXPECTED_LEAVES:
        raise SystemExit(f"REFUSED: {leaves} leaves changed, pinned {EXPECTED_LEAVES}")
    return leaves


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="run checks, write nothing")
    ap.add_argument("canonical", nargs="?", default=None)
    ap.add_argument("--canonical", dest="canonical_flag", default=None)
    ap.add_argument("--expect-sha", default=None)
    ap.add_argument("--out", default=None, help="write the post-state HERE instead of over the canonical")
    args = ap.parse_args()
    path = args.canonical_flag or args.canonical

    data = load_canonical(path)
    spec = staged()
    n = check_spec_shape(spec)
    print(f"  spec shape        {n} rows: {EXPECTED_NON_NULL} non-null / {EXPECTED_NULL} null; {EXPECTED_TRAY} tray, {EXPECTED_ROOTSTOCK} rootstock, {EXPECTED_CULTIVAR} cultivar; {EXPECTED_FLIPS} flips")
    n = check_pre_state(spec, data)
    print(f"  pre-state         {n} crops read; no key present; evidence found once; flips false->; {EXPECTED_FLAGS_MECHANICAL} exact matches; gravel/applicable sets complete")
    post = apply_to(data, spec)
    check_post(post, spec)
    print("  post gates        container_path_gate (presence ON) 0; display_readiness + numeric_sanity clean on the flips")
    leaves = verify_post(data, post, spec)
    print(f"  verify post       {leaves} leaves, nothing else")

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
```

- [ ] **Step 2: Run `--check` against the skeleton and confirm it REFUSES on the empty evidence**

Run: `python3 tools/promote_pla7_container_path.py --check`
Expected: `REFUSED: apple is rootstock without evidence` (the skeleton's evidence slots are empty by design; the promote must refuse until the read fills them). This is the RED that proves guard 2 is reachable.

- [ ] **Step 3: Commit**

```bash
git add tools/promote_pla7_container_path.py
git commit -m "tooling(pla7): promote A1 script -- container_path rows with evidence, three flips, the mechanical variety migration, gravel + applicable riders; refuses on the skeleton"
```

---

### Task 5: The guard suite, replay-pinned

**Files:**
- Create: `tools/test_promote_pla7_container_path.py`

**Interfaces:**
- Consumes: everything Task 4 produces; `promote_fixture.pre_state(BASE_SHA)`
- Produces: the pin constants `N_LEAVES`, `N_ROWS`, `N_FLAGS` the harness sentinel reads; the driver names the harness's MUTATIONS table selects

- [ ] **Step 1: Write the suite**

The suite runs against the SKELETON spec too, except the tests that need evidence filled; those skip with a named reason until Task 7 and are the last to go green. Every guard has a driver that injects the defect into a fresh copy and asserts the exact refusal fragment.

```python
#!/usr/bin/env python3
"""Guard suite for promote_pla7_container_path -- PLA-7 promote A1.

THE FIXTURE IS REBUILT FROM THE COMMITTED BASE (promote_fixture.pre_state), never live canonical.
SHIPS MUTATION-TESTED (PLA-215) via mutate_pla7_container_path_suite.py.
"""
import copy
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402
import promote_pla7_container_path as P  # noqa: E402

BASE_SHA = "72371c02fa306d8e1849053416baf34e232b80bbdf1af5169d546c12c8f45222"
ROSTER = 128
N_ROWS = 121
N_NON_NULL = 110
N_NULL = 11
N_TRAY = 8
N_ROOTSTOCK = 8
N_CULTIVAR = 1
N_FLIPS = 3
N_FLAGS = 134
N_GRAVEL = 16
N_APPLICABLE = 12
N_LEAVES = 294
FLIP_CROPS = ("cherry-sour", "cherry-sweet", "mulberry")
TRAY_CROPS = ("arugula-microgreens", "broccoli-microgreens", "cilantro-microgreens", "microgreens-mix",
              "pea-shoots", "radish-microgreens", "sunflower-sprouts", "wheatgrass")


def evidence_filled(spec):
    return all((r.get("evidence") or "").strip() for r in spec["paths"] if r["container_path"] in P.EVIDENCE_VALUES)


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(promote_fixture.pre_state(P.BASE_SHA))
        cls.spec = P.staged()

    def fresh_spec(self):
        return copy.deepcopy(self.spec)

    def fresh_data(self):
        return copy.deepcopy(self.data)

    def need_evidence(self):
        if not evidence_filled(self.spec):
            self.skipTest("evidence slots not yet filled (Task 7); this test is the last to go green")

    def row(self, spec, crop):
        return next(r for r in spec["paths"] if r["crop"] == crop)

    def assertRefuses(self, fragment, fn, *a, **kw):
        with self.assertRaises(SystemExit) as cm:
            fn(*a, **kw)
        msg = str(cm.exception)
        self.assertIn(fragment, msg, f"guard fired with the wrong message.\n  wanted: {fragment!r}\n  got: {msg!r}")


class Preflight(Base):
    def test_base_sha_is_the_pinned_one(self):
        self.assertEqual(P.BASE_SHA, BASE_SHA)
        self.assertEqual(P.sha256_bytes(promote_fixture.pre_state(P.BASE_SHA)), BASE_SHA)

    def test_fixture_is_the_full_roster(self):
        self.assertEqual(len(self.data["crops"]), ROSTER)

    def test_pins_are_the_literals(self):
        self.assertEqual((P.EXPECTED_ROWS, P.EXPECTED_NON_NULL, P.EXPECTED_NULL, P.EXPECTED_TRAY,
                          P.EXPECTED_ROOTSTOCK, P.EXPECTED_CULTIVAR, P.EXPECTED_FLIPS,
                          P.EXPECTED_FLAGS_MECHANICAL, P.EXPECTED_GRAVEL, P.EXPECTED_APPLICABLE, P.EXPECTED_LEAVES),
                         (N_ROWS, N_NON_NULL, N_NULL, N_TRAY, N_ROOTSTOCK, N_CULTIVAR, N_FLIPS,
                          N_FLAGS, N_GRAVEL, N_APPLICABLE, N_LEAVES))

    def test_the_spec_is_the_shape_measured(self):
        self.assertEqual(len(self.spec["paths"]), N_ROWS)
        self.assertEqual(tuple(sorted(f["crop"] for f in self.spec["flips"])), FLIP_CROPS)
        self.assertEqual(tuple(sorted(r["crop"] for r in self.spec["paths"] if r["container_path"] == "tray")), TRAY_CROPS)
        self.assertEqual(len(self.spec["gravel_normalize"]), N_GRAVEL)
        self.assertEqual(len(self.spec["overwinter_applicable_true"]), N_APPLICABLE)

    def test_base_has_no_key_anywhere(self):
        self.assertEqual(sum(1 for c in self.data["crops"] if "container_path" in c["container_notes"]), 0)

    def test_mechanical_matches_are_the_pinned_count(self):
        self.assertEqual(len(P.mechanical_flags(self.data)), N_FLAGS)


class SpecShape(Base):
    def test_refuses_a_missing_crop(self):
        s = self.fresh_spec(); s["paths"].pop()
        self.assertRefuses("path rows, pinned", P.check_spec_shape, s)

    def test_refuses_a_duplicated_crop(self):
        self.need_evidence()
        s = self.fresh_spec(); s["paths"][1] = dict(s["paths"][0])
        self.assertRefuses("appears twice", P.check_spec_shape, s)

    def test_refuses_an_unknown_value(self):
        self.need_evidence()
        s = self.fresh_spec(); self.row(s, "basil")["container_path"] = "dwarf_rootstock"
        self.assertRefuses("not in", P.check_spec_shape, s)

    def test_refuses_rootstock_without_evidence(self):
        s = self.fresh_spec(); self.row(s, "apple")["evidence"] = ""
        self.assertRefuses("without evidence", P.check_spec_shape, s)

    def test_refuses_evidence_on_a_direct_row(self):
        self.need_evidence()
        s = self.fresh_spec(); self.row(s, "basil")["evidence"] = "Basil does well in pots."
        self.assertRefuses("carries evidence on a", P.check_spec_shape, s)

    def test_refuses_a_count_drift(self):
        self.need_evidence()
        s = self.fresh_spec(); self.row(s, "basil")["container_path"] = None
        self.assertRefuses("non_null rows", P.check_spec_shape, s)

    def test_refuses_a_fourth_flip(self):
        self.need_evidence()
        s = self.fresh_spec()
        s["flips"].append({"crop": "plum", "container_ok": True, "min_pot_gallons": 25, "container_recommended": False})
        self.assertRefuses("flips, pinned", P.check_spec_shape, s)

    def test_refuses_a_flip_that_recommends(self):
        self.need_evidence()
        s = self.fresh_spec(); s["flips"][0]["container_recommended"] = True
        self.assertRefuses("container_recommended false", P.check_spec_shape, s)

    def test_refuses_a_flip_with_an_absurd_pot(self):
        self.need_evidence()
        s = self.fresh_spec(); s["flips"][0]["min_pot_gallons"] = 500
        self.assertRefuses("min_pot_gallons", P.check_spec_shape, s)

    def test_refuses_a_gravel_row_count_drift(self):
        self.need_evidence()
        s = self.fresh_spec(); s["gravel_normalize"].append("basil")
        self.assertRefuses("gravel rows", P.check_spec_shape, s)


class PreState(Base):
    def test_pre_state_passes(self):
        self.need_evidence()
        self.assertEqual(P.check_pre_state(self.spec, self.data), N_ROWS)

    def test_refuses_a_crop_already_carrying_the_key(self):
        self.need_evidence()
        d = self.fresh_data(); P.by_slug(d)["basil"]["container_notes"]["container_path"] = "direct"
        self.assertRefuses("already carries container_path", P.check_pre_state, self.spec, d)

    def test_refuses_a_variety_already_flagged(self):
        self.need_evidence()
        d = self.fresh_data(); P._varieties(P.by_slug(d)["apple"])[0]["container_suitable"] = True
        self.assertRefuses("already carries a variety container key", P.check_pre_state, self.spec, d)

    def test_refuses_evidence_that_does_not_match_the_crop(self):
        self.need_evidence()
        s = self.fresh_spec(); self.row(s, "apple")["evidence"] = "This sentence is in no crop."
        self.assertRefuses("evidence found 0 times", P.check_pre_state, s, self.data)

    def test_refuses_evidence_that_matches_twice(self):
        self.need_evidence()
        s = self.fresh_spec(); self.row(s, "apple")["evidence"] = "pot"
        self.assertRefuses("needs exactly 1", P.check_pre_state, s, self.data)

    def test_refuses_a_row_whose_null_disagrees_with_container_ok(self):
        self.need_evidence()
        s = self.fresh_spec(); self.row(s, "peach")["container_path"] = "direct"
        d = self.fresh_data()
        self.assertRefuses("container_ok will be False", P.check_pre_state, s, d)

    def test_refuses_rootstock_with_no_suitable_entry(self):
        self.need_evidence()
        d = self.fresh_data()
        for r in P.by_slug(d)["apple"]["rootstock_options"]:
            r["container_suitable"] = False
        self.assertRefuses("no container_suitable rootstock entry", P.check_pre_state, self.spec, d)

    def test_refuses_a_flip_on_a_crop_already_true(self):
        self.need_evidence()
        d = self.fresh_data(); P.by_slug(d)["cherry-sweet"]["container_notes"]["container_ok"] = True
        self.assertRefuses("is not container_ok false", P.check_pre_state, self.spec, d)

    def test_refuses_a_missed_gravel_crop(self):
        self.need_evidence()
        d = self.fresh_data(); P.by_slug(d)["basil"]["container_notes"]["drainage"]["gravel_layer"] = "not_required"
        self.assertRefuses("gravel rows differ", P.check_pre_state, self.spec, d)

    def test_refuses_a_missed_applicable_crop(self):
        self.need_evidence()
        d = self.fresh_data(); P.by_slug(d)["basil"]["container_notes"]["overwintering"]["applicable"] = None
        self.assertRefuses("applicable rows differ", P.check_pre_state, self.spec, d)

    def test_refuses_applicable_with_no_prose(self):
        self.need_evidence()
        d = self.fresh_data(); cn = P.by_slug(d)["apple"]["container_notes"]
        cn["overwintering"]["approach_seasoned"] = None; cn["container_overwintering_seasoned"] = None
        self.assertRefuses("no overwintering prose", P.check_pre_state, self.spec, d)

    def test_refuses_a_mechanical_count_drift(self):
        self.need_evidence()
        d = self.fresh_data()
        for c in d["crops"]:
            c["container_notes"]["container_suitable_varieties"] = []
        self.assertRefuses("exact-name variety matches, pinned", P.check_pre_state, self.spec, d)

    def test_refuses_an_explicit_flag_naming_no_entry(self):
        self.need_evidence()
        s = self.fresh_spec(); s["variety_flags"][0]["name"] = "Dwarf Nobody"
        self.assertRefuses("matches 0 entries", P.check_pre_state, s, self.data)


class ApplyAndPost(Base):
    def post(self):
        return P.apply_to(self.data, self.spec)

    def test_apply_changes_exactly_the_declared_leaves(self):
        self.need_evidence()
        self.assertEqual(P.verify_post(self.data, self.post(), self.spec), N_LEAVES)

    def test_every_certified_crop_carries_the_key_and_no_shell_does(self):
        self.need_evidence()
        post = self.post()
        carrying = {c["slug"] for c in post["crops"] if "container_path" in c["container_notes"]}
        certified = {c["slug"] for c in post["crops"] if (c.get("verification_status") or {}).get("status")}
        self.assertEqual(carrying, certified)
        self.assertEqual(len(certified), N_ROWS)

    def test_the_flips_are_true_with_their_pot(self):
        self.need_evidence()
        idx = P.by_slug(self.post())
        self.assertEqual((idx["cherry-sweet"]["container_notes"]["container_ok"], idx["cherry-sweet"]["container_notes"]["min_pot_gallons"]), (True, 25))
        self.assertEqual((idx["mulberry"]["container_notes"]["container_ok"], idx["mulberry"]["container_notes"]["min_pot_gallons"]), (True, 15))
        self.assertEqual(idx["mulberry"]["container_notes"]["container_path"], "cultivar")

    def test_mulberry_dwarf_everbearing_is_flagged_with_gallons(self):
        self.need_evidence()
        v = next(x for x in P._varieties(P.by_slug(self.post())["mulberry"]) if x["name"] == "Dwarf Everbearing")
        self.assertEqual((v["container_suitable"], v["container_min_gallons"]), (True, 15))

    def test_plum_is_untouched(self):
        self.need_evidence()
        pre, post = P.by_slug(self.data)["plum"], P.by_slug(self.post())["plum"]
        self.assertEqual(post["container_notes"]["container_ok"], False)
        self.assertIsNone(post["container_notes"]["container_path"])
        self.assertEqual(pre["rootstock_options"], post["rootstock_options"])

    def test_no_rootstock_entry_changes_anywhere(self):
        self.need_evidence()
        pre, post = P.by_slug(self.data), P.by_slug(self.post())
        for s in pre:
            self.assertEqual(pre[s].get("rootstock_options"), post[s].get("rootstock_options"), s)

    def test_gravel_has_one_encoding_afterwards(self):
        self.need_evidence()
        vals = {(c["container_notes"].get("drainage") or {}).get("gravel_layer") for c in self.post()["crops"]}
        self.assertNotIn("not_required", vals)

    def test_post_gate_is_clean_with_presence_on(self):
        self.need_evidence()
        self.assertEqual(P.CPG.all_violations(self.post(), presence=True), [])

    def test_refuses_a_post_state_that_fails_the_gate(self):
        self.need_evidence()
        post = self.post(); P.by_slug(post)["basil"]["container_notes"]["container_path"] = None
        self.assertRefuses("container_path_gate on the post-state", P.check_post, post, self.spec)

    def test_refuses_a_flip_that_fails_display_readiness(self):
        self.need_evidence()
        post = self.post(); P.by_slug(post)["cherry-sweet"]["container_notes"]["min_pot_gallons"] = None
        self.assertRefuses("display_readiness on flipped", P.check_post, post, self.spec)


class BlastRadius(Base):
    def post(self):
        return P.apply_to(self.data, self.spec)

    def test_refuses_a_top_level_change(self):
        self.need_evidence()
        post = self.post(); post["control_methods"] = {}
        self.assertRefuses("top-level key 'control_methods' changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_roster_change(self):
        self.need_evidence()
        post = self.post(); post["crops"].pop()
        self.assertRefuses("crop roster changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_shell_change(self):
        self.need_evidence()
        post = self.post(); P.by_slug(post)["avocado"]["container_notes"]["container_path"] = None
        self.assertRefuses("shell avocado changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_change_outside_the_two_blocks(self):
        self.need_evidence()
        post = self.post(); P.by_slug(post)["basil"]["description"] = "changed"
        self.assertRefuses("changed outside container_notes/varieties", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_extra_container_notes_key(self):
        self.need_evidence()
        post = self.post(); P.by_slug(post)["basil"]["container_notes"]["plants_per_pot"] = [1, 2]
        self.assertRefuses("key set changed other than by adding container_path", P.verify_post, self.data, post, self.spec)

    def test_refuses_an_undeclared_container_notes_change(self):
        self.need_evidence()
        post = self.post(); P.by_slug(post)["basil"]["container_notes"]["min_pot_gallons"] = 99
        self.assertRefuses("changed without a spec row", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_flip_value_other_than_declared(self):
        self.need_evidence()
        post = self.post(); P.by_slug(post)["cherry-sweet"]["container_notes"]["min_pot_gallons"] = 30
        self.assertRefuses("changed without a spec row", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_variety_flag_without_a_match(self):
        self.need_evidence()
        post = self.post(); P._varieties(P.by_slug(post)["apple"])[0]["container_suitable"] = True
        self.assertRefuses("without a match or a row", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_variety_prose_change(self):
        self.need_evidence()
        post = self.post(); P._varieties(P.by_slug(post)["kale"])[0]["name"] = "Renamed"
        self.assertRefuses("variety field 'name' changed", P.verify_post, self.data, post, self.spec)

    def test_refuses_a_leaf_count_drift(self):
        self.need_evidence()
        post = self.post()
        idx = P.by_slug(post)
        slug = next(s for s in self.spec["gravel_normalize"])
        idx[slug]["container_notes"]["drainage"]["gravel_layer"] = "not_required"
        self.assertRefuses("leaves changed, pinned", P.verify_post, self.data, post, self.spec)


class Serializer(Base):
    def test_compact_no_trailing_newline(self):
        b = P.serialize({"a": [1, 2], "b": "eé"})
        self.assertEqual(b, b'{"a":[1,2],"b":"e\xc3\xa9"}')

    def test_output_sha_is_stable(self):
        self.need_evidence()
        a = P.sha256_bytes(P.serialize(P.apply_to(self.data, self.spec)))
        b = P.sha256_bytes(P.serialize(P.apply_to(self.data, self.spec)))
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the suite on the skeleton**

Run: `python3 -m pytest tools/test_promote_pla7_container_path.py -q`
Expected: the Preflight, SpecShape (evidence-independent ones) and Serializer tests pass; the rest report `skipped: evidence slots not yet filled (Task 7)`. Zero failures. Note `test_refuses_rootstock_without_evidence` passes NOW because the skeleton's slots are empty: that is a refusal-spec pass, not vacuous.

- [ ] **Step 3: Commit**

```bash
git add tools/test_promote_pla7_container_path.py
git commit -m "tooling(pla7): promote A1 guard suite, replay-pinned to 72371c02; evidence-dependent tests skip until the read"
```

---

### Task 6: The mutation harness

**Files:**
- Create: `tools/mutate_pla7_container_path_suite.py`

**Interfaces:**
- Consumes: the exact source lines of `promote_pla7_container_path.py` as anchors, the driver names of Task 5
- Produces: exit 0 only when every mutation is caught, with the liveness defenses of the PLA-457 harness

- [ ] **Step 1: Copy the PLA-457 runner and replace its constants and table**

```bash
cp tools/mutate_pla457_sulfur_oil_interval_suite.py tools/mutate_pla7_container_path_suite.py
```

Then in the copy, replace the three constants:

```python
PROMOTE = "promote_pla7_container_path.py"
SUITE = "test_promote_pla7_container_path.py"
STAGING = "pla7_container_path"
```

Replace the entire `MUTATIONS = [ ... ]` list with:

```python
# (family, name, old, new, pytest -k selector)
MUTATIONS = [
    ("entry", "base_sha_check_removed", "    if got != BASE_SHA:", "    if False:  " + MARKER,
     "test_base_sha_is_the_pinned_one"),

    ("spec", "row_count_not_pinned", "    if len(rows) != EXPECTED_ROWS:", "    if False:  " + MARKER,
     "test_refuses_a_missing_crop"),
    ("spec", "duplicate_crop_accepted", '        if r["crop"] in seen:', "        if False:  " + MARKER,
     "test_refuses_a_duplicated_crop"),
    ("spec", "unknown_value_accepted", "        if v is not None and v not in VALUES:", "        if False:  " + MARKER,
     "test_refuses_an_unknown_value"),
    ("spec", "missing_evidence_accepted", '        if v in EVIDENCE_VALUES and not (r.get("evidence") or "").strip():', "        if False:  " + MARKER,
     "test_refuses_rootstock_without_evidence"),
    ("spec", "stray_evidence_accepted", '        if v not in EVIDENCE_VALUES and r.get("evidence"):', "        if False:  " + MARKER,
     "test_refuses_evidence_on_a_direct_row"),
    ("spec", "count_pins_not_compared", "        if counts[k] != pins[k]:", "        if False:  " + MARKER,
     "test_refuses_a_count_drift"),
    ("spec", "flip_count_not_pinned", "    if len(flips) != EXPECTED_FLIPS:", "    if False:  " + MARKER,
     "test_refuses_a_fourth_flip"),
    ("spec", "recommending_flip_accepted", '        if f["container_ok"] is not True or f["container_recommended"] is not False:', "        if False:  " + MARKER,
     "test_refuses_a_flip_that_recommends"),
    ("spec", "absurd_pot_accepted", '        if not (isinstance(f["min_pot_gallons"], int) and 1 <= f["min_pot_gallons"] <= 100):', "        if False:  " + MARKER,
     "test_refuses_a_flip_with_an_absurd_pot"),
    ("spec", "gravel_count_not_pinned", '    if len(spec["gravel_normalize"]) != EXPECTED_GRAVEL:', "    if False:  " + MARKER,
     "test_refuses_a_gravel_row_count_drift"),

    ("prestate", "existing_key_accepted", '        if "container_path" in cn:\n            raise SystemExit(f"REFUSED: {c[\'slug\']} already carries container_path")',
     '        if False:  ' + MARKER + '\n            raise SystemExit(f"REFUSED: {c[\'slug\']} already carries container_path")',
     "test_refuses_a_crop_already_carrying_the_key"),
    ("prestate", "existing_variety_key_accepted", '            if "container_suitable" in v or "container_min_gallons" in v:', "            if False:  " + MARKER,
     "test_refuses_a_variety_already_flagged"),
    ("prestate", "evidence_not_counted", "            if hits != 1:", "            if False:  " + MARKER,
     "test_refuses_evidence_that_does_not_match_the_crop"),
    ("prestate", "null_vs_ok_not_compared", '        if (r["container_path"] is not None) != ok_post:', "        if False:  " + MARKER,
     "test_refuses_a_row_whose_null_disagrees_with_container_ok"),
    ("prestate", "rootstock_join_not_checked", '            if not any(x.get("container_suitable") is True for x in (c.get("rootstock_options") or []) if isinstance(x, dict)):', "            if False:  " + MARKER,
     "test_refuses_rootstock_with_no_suitable_entry"),
    ("prestate", "flip_precondition_not_checked", '        if cn.get("container_ok") is not False or cn.get("min_pot_gallons") is not None:', "        if False:  " + MARKER,
     "test_refuses_a_flip_on_a_crop_already_true"),
    ("prestate", "gravel_set_not_compared", '    if set(spec["gravel_normalize"]) != want_gravel:', "    if False:  " + MARKER,
     "test_refuses_a_missed_gravel_crop"),
    ("prestate", "applicable_set_not_compared", '    if set(spec["overwinter_applicable_true"]) != want_app:', "    if False:  " + MARKER,
     "test_refuses_a_missed_applicable_crop"),
    ("prestate", "applicable_prose_not_required", '            if not (ow.get("approach_seasoned") or cn.get("container_overwintering_seasoned")):', "            if False:  " + MARKER,
     "test_refuses_applicable_with_no_prose"),
    ("prestate", "mechanical_count_not_pinned", "    if len(mech) != EXPECTED_FLAGS_MECHANICAL:", "    if False:  " + MARKER,
     "test_refuses_a_mechanical_count_drift"),
    ("prestate", "explicit_flag_entry_not_checked", "        if len(ent) != 1:", "        if False:  " + MARKER,
     "test_refuses_an_explicit_flag_naming_no_entry"),

    ("post", "gate_not_run_on_post", "    v = CPG.all_violations(post, presence=True)\n    if v:", "    v = CPG.all_violations(post, presence=True)\n    if False:  " + MARKER,
     "test_refuses_a_post_state_that_fails_the_gate"),
    ("post", "display_readiness_not_run_on_flips", "        if dv:", "        if False:  " + MARKER,
     "test_refuses_a_flip_that_fails_display_readiness"),

    ("blast", "top_level_change_invisible", '        if k != "crops" and _j(pre[k]) != _j(post[k]):', "        if False:  " + MARKER,
     "test_refuses_a_top_level_change"),
    ("blast", "roster_change_invisible", '    if set(pre_i) != set(post_i) or len(pre["crops"]) != len(post["crops"]):', "    if False:  " + MARKER,
     "test_refuses_a_roster_change"),
    ("blast", "shell_change_invisible", '            if _j(s) != _j(g):\n                raise SystemExit(f"REFUSED: shell {slug} changed")',
     '            if False:  ' + MARKER + '\n                raise SystemExit(f"REFUSED: shell {slug} changed")',
     "test_refuses_a_shell_change"),
    ("blast", "outside_change_invisible", '            if _j(s[k]) != _j(g[k]):\n                raise SystemExit(f"REFUSED: {slug} field {k!r} changed outside container_notes/varieties")',
     '            if False:  ' + MARKER + '\n                raise SystemExit(f"REFUSED: {slug} field {k!r} changed outside container_notes/varieties")',
     "test_refuses_a_change_outside_the_two_blocks"),
    ("blast", "extra_key_accepted", '        if set(gcn) - set(scn) != {"container_path"} or set(scn) - set(gcn):', "        if False:  " + MARKER,
     "test_refuses_an_extra_container_notes_key"),
    ("blast", "undeclared_cn_change_accepted", '                raise SystemExit(f"REFUSED: {slug} container_notes.{k} changed without a spec row")', "                leaves += 1  " + MARKER,
     "test_refuses_an_undeclared_container_notes_change"),
    ("blast", "unmatched_flag_accepted", "                if key not in allowed_flags:", "                if False:  " + MARKER,
     "test_refuses_a_variety_flag_without_a_match"),
    ("blast", "variety_value_change_invisible", "                    if _j(a[k]) != _j(b[k]):", "                    if False:  " + MARKER,
     "test_refuses_a_variety_prose_change"),
    ("blast", "leaf_count_not_pinned", "    if leaves != EXPECTED_LEAVES:", "    if False:  " + MARKER,
     "test_refuses_a_leaf_count_drift"),

    ("serialize", "indent_reintroduced",
     '    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")',
     '    return json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")  ' + MARKER,
     "test_compact_no_trailing_newline"),
]
```

Replace the `sentinel_for` function's regex line and the driver it names:

```python
    m = re.search(r"^N_LEAVES = (\d+)$", src, re.M)
    if not m:
        sys.exit("HARNESS DEAD: cannot locate the N_LEAVES pin to build a sentinel from")
    return ("sentinel", "leaf_count_pin_broken",
            m.group(0), f"N_LEAVES = {int(m.group(1)) + 99999}  " + MARKER,
            "test_pins_are_the_literals", SUITE)
```

Replace the positive-control selector in `main()`:

```python
        rc, out = run_suite(tools, "test_the_spec_is_the_shape_measured")
```

(That line is already the selector in the copied file; confirm it still names a test that exists in the new suite. It does.)

- [ ] **Step 2: Run the harness `--list` and the anchor preflight**

Run: `python3 tools/mutate_pla7_container_path_suite.py --list`
Expected: 6 families listed (entry, spec, prestate, post, blast, serialize), 34 mutations.
Run: `python3 tools/mutate_pla7_container_path_suite.py --family serialize`
Expected: `anchor preflight: 34/34 anchors match exactly once`, `positive control: unmutated scratch is GREEN`, `sentinel: reddened as required`, then `caught serialize/indent_reintroduced`, `1 injected: 1 caught`. An anchor mismatch is `HARNESS DEAD`: fix the anchor to the promote's exact bytes, never the promote to the anchor.

- [ ] **Step 3: Run the full harness on the skeleton and record the expected shape of the result**

Run: `python3 tools/mutate_pla7_container_path_suite.py`
Expected on the SKELETON: the evidence-dependent drivers SKIP, and pytest treats a skipped-only selection as exit 0, so those mutations report SURVIVED. That is expected until Task 7 fills the evidence. Record the count. After Task 7 the run must be `34 injected: 34 caught, 0 survived, 0 broken`; anything else stops the arc.

- [ ] **Step 4: Commit**

```bash
git add tools/mutate_pla7_container_path_suite.py
git commit -m "tooling(pla7): promote A1 mutation harness (34 mutations, 6 families; evidence-dependent drivers arm at the read)"
```

---

### Task 7: The read, the pins, the gauntlet on a scratch post-state, HOLD

**Files:**
- Modify: `tools/staging/pla7_container_path/spec.json` (fill evidence; may change a `direct` row to `cultivar`; may set lemon and lime)
- Modify: `tools/promote_pla7_container_path.py` and `tools/test_promote_pla7_container_path.py` (only the `EXPECTED_ROOTSTOCK` / `N_ROOTSTOCK` and `EXPECTED_CULTIVAR` / `N_CULTIVAR` literals, if the read changes them; change both files in the same edit)
- Modify: `docs/field_addition_register.md` (row 29)
- Create: `docs/2026-09-xx-pla7-promote-a1-outcome.md`

- [ ] **Step 1: Fill evidence on the eight `rootstock` rows and the mulberry `cultivar` row**

For each of apple, pear-european, pear-asian, orange-navel, mandarin-clementine, grapefruit, cherry-sweet, cherry-sour, mulberry: open the crop's `container_notes.notes_seasoned` (and `notes_beginner`), pick the ONE sentence that states the condition, and paste it verbatim as `evidence`. The promote counts substring occurrences across every prose leaf in the block, so pick a sentence, not a fragment. Print the candidates with:

```bash
python3 - <<'EOF'
import json, sys
sys.path.insert(0, "tools")
import promote_fixture
d = json.loads(promote_fixture.pre_state("72371c02fa306d8e1849053416baf34e232b80bbdf1af5169d546c12c8f45222"))
for c in d["crops"]:
    if c["slug"] in ("apple","pear-european","pear-asian","orange-navel","mandarin-clementine","grapefruit","cherry-sweet","cherry-sour","mulberry","lemon","lime"):
        cn = c["container_notes"]
        print("\n==", c["slug"]); print("S:", cn.get("notes_seasoned")); print("B:", cn.get("notes_beginner"))
EOF
```

- [ ] **Step 2: Decide lemon and lime**

Read their notes from Step 1. If a note says a pot is viable only on a trifoliate or dwarfing rootstock, set the row to `rootstock` with that sentence as evidence and raise `EXPECTED_ROOTSTOCK` and `N_ROOTSTOCK` together (to 9 or 10) and `EXPECTED_NON_NULL` does not change. If the note says lemon or lime as sold grows in a pot, leave `direct`. Write the decision and the sentence into the outcome doc.

- [ ] **Step 3: Decide `cultivar` candidates**

Run the candidate scan and read each crop's notes; a crop becomes `cultivar` ONLY when its own notes say a pot works only with compact, bush, patio or dwarf types AND it has at least one exact-name variety match (else rule 3 refuses):

```bash
python3 - <<'EOF'
import json, re, sys
sys.path.insert(0, "tools")
import promote_fixture, promote_pla7_container_path as P
d = json.loads(promote_fixture.pre_state(P.BASE_SHA))
mech = {s for s, _ in P.mechanical_flags(d)}
sig = re.compile(r"\b(only|choose|stick to|best on|pick|look for)\b[^.]*\b(compact|bush|patio|dwarf|determinate)\b", re.I)
for c in d["crops"]:
    cn = c["container_notes"]
    if cn.get("container_ok") and c["slug"] in mech and sig.search(cn.get("notes_seasoned") or ""):
        print("\n==", c["slug"]); print(cn["notes_seasoned"])
EOF
```

For every crop you change to `cultivar`, add the sentence as evidence and raise `EXPECTED_CULTIVAR` / `N_CULTIVAR` together. Record each decision in the outcome doc with the sentence. The tomatoes, basil and tomatillo store varieties as strings and CANNOT be `cultivar` in this promote; if their notes say they should be, write that down as owed to Plan B and leave them `direct`.

- [ ] **Step 4: Run `--check` and the suite until both are clean**

Run: `python3 tools/promote_pla7_container_path.py --check`
Expected: four `  ...` lines and `72371c02 -> <sha>`, `--check: nothing written`. Any `REFUSED` names the row to fix.
Run: `python3 -m pytest tools/test_promote_pla7_container_path.py -q`
Expected: all pass, 0 skipped.

- [ ] **Step 5: Run the harness to completion**

Run: `python3 tools/mutate_pla7_container_path_suite.py`
Expected: `34 injected: 34 caught, 0 survived, 0 broken`. A survivor is a guard the suite does not test: fix the driver, not the count.

- [ ] **Step 6: Write the scratch post-state and gauntlet it**

```bash
python3 tools/promote_pla7_container_path.py --out /tmp/pla7_a1_post.json
for s in cherry-sweet cherry-sour mulberry apple kale zucchini-courgette microgreens-mix plum lettuce-leaf; do
  python3 tools/whole_crop_gate.py $s /tmp/pla7_a1_post.json | tail -1
done
python3 tools/gate_all.py /tmp/pla7_a1_post.json | tail -1
python3 tools/container_path_gate.py /tmp/pla7_a1_post.json --presence
python3 tools/register_completeness_gate.py /tmp/pla7_a1_post.json | tail -2
python3 tools/release_verify.py /tmp/pla7_a1_post.json --base crops_data_final.json --slug cherry-sweet --ref avocado --expect-changed "$(python3 -c "import json;d=json.load(open('crops_data_final.json'));print(','.join(sorted(c['slug'] for c in d['crops'] if (c.get('verification_status') or {}).get('status') and c['slug']!='cherry-sweet')))")"
```

`--ref avocado` because every certified crop changes in this promote and the seven shells are the only byte-identical crops left; `--expect-changed` declares the other 120 certified crops EXACTLY (release_verify refuses an undeclared change and a declared non-change alike).

Expected: every `whole_crop_gate` line is `GATE: PASS ...`; `gate_all` reports `121/121`; `container_path_gate` reports `0 violation(s); 121/128 crops carry the key; presence ARMED`; `register_completeness` reports no HALT; `release_verify` section A reports `reference crop avocado byte-identical` and exactly the 121 declared crops changed, and no other section reports a concern that is not already present on the live canonical (re-run the same command with the live file as candidate to prove a concern pre-exists before accepting it). Note the scratch SHA from `--out`'s run: it is the `--expect-sha` for Task 8.

- [ ] **Step 7: Add register row 29**

Append to the register table in `docs/field_addition_register.md`:

```markdown
| 29 | **`container_notes.container_path`** -- closed enum `direct` / `rootstock` / `cultivar` / `tray`, null iff `container_ok` is not true, naming the JOIN a consumer follows to put the crop in a pot; **`varieties.recommended[].container_suitable`** (bool or null) + optional `container_min_gallons`, the PLA-12 authoring contract (spec 2026-09-06 sections 2-3). | **PROMOTE A1 PREPARED <date>, HELD** (base `72371c02`; scratch post `<sha>`); presence floor A58 arms with the write | rule-based promote with evidence quotes; A58 shape + presence; `container_path_gate`; PLA-463 gates the remaining tree crops | plant-astro CareGuideCard/HeroCard qualifier + beds tool; plant-app planner `deriveContainerFacts` (drops the `|| suitable rootstock` branch) + variety picker; the prose ContainerCard is D5 |
```

Replace `<date>` and `<sha>` with the run's values before committing.

- [ ] **Step 8: Run the full tree and write the outcome doc**

Run: `python3 -m pytest tools/ -q 2>&1 | tail -3`
Expected: only the two pre-existing failures (`test_bare_host_scan::test_self_pathed_population_at_this_canonical`, `test_cited_claim_scan::test_MUTATION_the_anchoring_only_walk_reproduces_the_false_pass`); everything new passes. Write `docs/2026-09-xx-pla7-promote-a1-outcome.md` (date it the day you run): the read decisions with their sentences, the final pins, the harness line, the gauntlet lines, the scratch SHA, and the exact apply command for Task 8.

- [ ] **Step 9: Commit tooling and docs; canonical untouched; STOP for approval**

```bash
git add tools/staging/pla7_container_path/spec.json tools/promote_pla7_container_path.py tools/test_promote_pla7_container_path.py docs/field_addition_register.md docs/2026-09-*-pla7-promote-a1-outcome.md
git commit -m "tooling(pla7): promote A1 PREPARED AND HELD -- 72371c02 -> <scratch sha>; suite N/N, harness 34/34; canonical unchanged"
git push origin main
```

Then report to Trevor: the scratch SHA, the read decisions, and the apply command. Do not run Task 8 without his approval.

---

### Task 8: Apply on approval, arm A58 presence, state trio

**Files:**
- Modify: `crops_data_final.json` (the ONLY canonical write in this plan)
- Modify: `tools/whole_crop_gate.py` (`A58_PRESENCE_ARMED = True`), `tools/test_gate_container_path_a58.py` (the assertion flips to `= True`)
- Modify: `LATEST.txt`, `STATE_HISTORY.md`, `CURRENT_STATE.md`, `tools/promote_fixture.py` (`COMMIT_FOR`)

- [ ] **Step 1: Apply with the gauntleted SHA**

```bash
python3 tools/promote_pla7_container_path.py --expect-sha <scratch sha from Task 7>
shasum -a 256 crops_data_final.json
```

Expected: `WROTE .../crops_data_final.json` and the shasum equals the scratch SHA.

- [ ] **Step 2: Arm the presence floor in the same commit**

Change `A58_PRESENCE_ARMED = False` to `A58_PRESENCE_ARMED = True` in `tools/whole_crop_gate.py`, and in `tools/test_gate_container_path_a58.py` change the last assertion to `assert "A58_PRESENCE_ARMED = True" in src, "presence floor arms with the canonical that carries the key"` and its comment to say so. Run:

```bash
python3 tools/test_gate_container_path_a58.py
python3 tools/gate_all.py | tail -1
python3 tools/container_path_gate.py --presence
```

Expected: `PASS gate A58 container_path`; `121/121`; `0 violation(s); 121/128 crops carry the key; presence ARMED`.

- [ ] **Step 3: State trio**

Bump `LATEST.txt` (SHA, date, one session line naming this promote); prepend a `STATE_HISTORY.md` entry (what moved, the pins, the harness line, the gauntlet, the held plum, PLA-463's follow-on); amend `CURRENT_STATE.md` surgically (Canonical pointer + a release entry), then `python3 tools/lean_current_state.py` and `python3 -m pytest tools/test_gen_current_state.py -q`.

- [ ] **Step 4: Re-measure the collision gate (no ids move; the figures must hold)**

Run: `python3 -m pytest tools/test_problem_id_collision_gate.py -q`
Expected: green at 36 / 24 / 12. A different figure means something moved an id; stop.

- [ ] **Step 5: Commit and push on Trevor's confirmation**

```bash
git add crops_data_final.json LATEST.txt STATE_HISTORY.md CURRENT_STATE.md tools/whole_crop_gate.py tools/test_gate_container_path_a58.py
git commit --no-verify -m "data(pla7): promote A1 LANDED -- container_path on 121, 3 flips, 135 variety flags, gravel + applicable riders; A58 presence armed (72371c02 -> <sha>)"
```

`--no-verify` is for the known-stale plant-app E1 export check only; every gate above already ran green. Then register the new SHA in `promote_fixture.COMMIT_FOR` pointing at that commit's short hash, commit that pin, and push both after Trevor confirms. Note for plant-app: `npm run build:guides` is behind by one more revision.

---

## Follow-on plans (each its own document, after this one lands)

- **A2, sourced fills:** the five herb `_seasoned` siblings, the three citrus rootstock gallons, the four empty `sources`, the eight `depth_inches_min`, and the `container_specific_pests` retire (basil `spider_mites` becomes a real `pests[]` entry with a ladder under A57 first). Every value carries a T1 read.
- **B, the variety list:** convert the seven string-variety crops to records (PLA-290 pattern), T1-read the 60 unmatched cultivar names, then retire `container_suitable_varieties[]` AFTER plant-astro's beds tool and plant-app's `build-education-data.mjs` read the flag.
- **C, `plants_per_pot`:** author from the Illinois table and Texas A&M E-545, with `numeric_sanity_gate` bounds and the A39 presence floor; the app's per-plant gallons read it.
- **D, `critical_warnings` safety class:** spec section 5; the app's export allowlist gains the key first.
- **E, PLA-463 follow-on:** `container_path` for plum, apricot, nectarine, peach, persimmon, pawpaw, lemon and lime where the read deferred them, the mulberry rootstock-entry retirement, reusing this suite's guards.
- **Consumer sessions (other repos):** spec section 6, frontend first.
