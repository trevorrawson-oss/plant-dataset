#!/usr/bin/env python3
"""mutate_sowing_heat_ceiling_gate -- proof that test_sowing_heat_ceiling_gate catches a regression in every
guard family of tools/sowing_heat_ceiling_gate.py (register #35, PLA-750).

Each mutation edits the GATE'S SOURCE in a scratch directory (tools/cited_promote_common.py copied beside
it, so the import resolves to an unmodified helper), then runs the suite there. A mutation must turn the
suite RED.

LIVENESS (PLA-215 convention items 2 and 3):
  * POSITIVE CONTROL  the unmutated scratch copy passes the suite.
  * MUTATION-APPLIED  every mutation's `old` text occurs exactly once and the staged source differs.
  * SENTINEL          a gate whose check_crop returns nothing must redden, or HARNESS DEAD.

Usage: python3 tools/mutate_sowing_heat_ceiling_gate.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(HERE, "sowing_heat_ceiling_gate.py")
SUITE = os.path.join(HERE, "test_sowing_heat_ceiling_gate.py")
HELPERS = ("cited_promote_common.py",)

MUTATIONS = [
    ("pause-absent", "a hold with no field passes",
     "        if _pause(c):\n            return [", "        if False:\n            return ["),
    ("pause-invariant", "pause_in_heat no longer has to match temp_f",
     "    if held != _pause(c):", "    if False:"),
    ("pause-direction", "only a null with pause true is caught (int with pause false passes)",
     "    if held != _pause(c):", "    if (not held) and _pause(c):"),
    ("int", "a float or bool temp_f is accepted",
     "    return isinstance(x, int) and not isinstance(x, bool)", "    return isinstance(x, (int, float))"),
    ("range", "the temp range is not enforced",
     "    elif held and not (TEMP_RANGE[0] <= t <= TEMP_RANGE[1]):", "    elif False:"),
    ("enum-measures", "measures enum not checked",
     '        if f.get("measures") not in MEASURES:', "        if False:"),
    ("enum-basis", "basis enum not checked",
     '        if f.get("basis") not in BASES:', "        if False:"),
    ("held-keys", "held key set not checked",
     "        if not (HELD_REQUIRED <= keys <= HELD_REQUIRED | HELD_OPTIONAL):", "        if False:"),
    ("null-keys", "null-state key set not checked",
     "        if keys != NULL_KEYS:", "        if False:"),
    ("claim", "an empty claim passes",
     '        if not (isinstance(f.get("claim"), str) and f["claim"].strip()):', "        if False:"),
    ("soil-note", "a soil row with no note passes",
     '        if f.get("measures") == "soil" and not', '        if False and not'),
    ("null-note", "a null with no note passes",
     "            v.append(f\"{slug}: {FIELD} null state needs a note", "            0 and v.append(f\"{slug}: {FIELD} null state needs a note"),
    ("sources-pair", "sources and anchoring_urls may differ",
     "    if set(srcs) != set(anc):", "    if False:"),
    ("sources-dup", "a duplicated source id passes",
     "    if len(srcs) != len(set(srcs)):", "    if False:"),
    ("catalog", "a source outside the catalog passes",
     "        if sid not in catalog:", "        if False:"),
    ("anchor-url", "a bare-host anchor passes",
     " or BARE_HOST.match(url or \"\"):", ":"),
    ("anchor-verified", "an anchor with no verified date passes",
     '        if not (isinstance(a, dict) and VERIFIED.match(str(a.get("verified", "")))):', "        if False:"),
    ("claim-source", "claim_source outside sources passes",
     '        if f.get("claim_source") not in srcs:', "        if False:"),
    ("temp-source", "temp_source equal to claim_source passes",
     ' or f["temp_source"] == f.get("claim_source")):', "):"),
    ("bytes-claim", "the claim is never matched against the bytes",
     "        if pages and not any(claim and claim in p for p in pages):", "        if False:"),
    ("bytes-unhashed", "an anchor with no hashed bytes passes",
     "        if not got:\n            v.append", "        if False:\n            v.append"),
    ("bytes-hash", "tampered bytes are read as if valid",
     "            if sha256_bytes(raw) != sha:", "            if False:"),
    ("number", "temp_f need not appear in the claim",
     "            if not re.search(rf\"(?<![\\d.]){t}(?![\\d.]\\d)(?!\\d)\", claim) and not c_ok:",
     "            if False:"),
    ("number-boundary", "the number check goes back to \\b (blind to NFKC's 80ºF -> 80of)",
     "rf\"(?<![\\d.]){t}(?![\\d.]\\d)(?!\\d)\"", "rf\"\\b{t}\\b\""),
    ("number-substring", "a number inside a longer number counts",
     "rf\"(?<![\\d.]){t}(?![\\d.]\\d)(?!\\d)\"", "rf\"{t}\""),
    ("celsius", "the degC rounding is not accepted",
     "            c_ok = re.search(rf\"(?<!\\d){_celsius(t)}\\.?\\s*[°º˚o]\\s*c\\b\", claim)", "            c_ok = None"),
    ("celsius-period", "the publisher's period before the unit is refused",
     "{_celsius(t)}\\.?\\s*", "{_celsius(t)}\\s*"),
    ("temp-unit", "the temp_source page need not state the number with a unit",
     "            if tp and not any(unit.search(p) for p in tp):", "            if False:"),
    ("note-quote", "quoted note spans are not checked",
     "        if allp and not any(q in p for p in allp):", "        if False:"),
    ("note-curly", "curly-quoted note spans are skipped",
     "QUOTED = re.compile(r'\"([^\"]{12,})\"|“([^”]{12,})”')",
     "QUOTED = re.compile(r'\"([^\"]{12,})\"')"),
    ("floor", "the population floor is ignored",
     "    if inspected == 0 or inspected < floor:", "    if inspected == 0:"),
    ("floor-zero", "an empty population passes when the floor is 0",
     "    if inspected == 0 or inspected < floor:", "    if inspected < floor:"),
    ("floor-default", "the default floor drops below the pilot's 30",
     "POPULATION_FLOOR = 30 ", "POPULATION_FLOOR = 1 "),
    ("population-line", "the run stops reporting its population",
     'print(f"sowing_heat_ceiling_gate: inspected {inspected} crop(s)', 'print(f"sowing_heat_ceiling_gate: ok {inspected} crop(s)'),
]
SENTINEL = ("SENTINEL: check_crop returns no violations at all",
            '    """SHAPE + PAUSE violations for one crop (empty == clean)."""\n',
            '    """SHAPE + PAUSE violations for one crop (empty == clean)."""\n    return []\n')


def run_suite(src):
    with tempfile.TemporaryDirectory() as td:
        with open(os.path.join(td, "sowing_heat_ceiling_gate.py"), "w", encoding="utf-8") as fh:
            fh.write(src)
        for h in HELPERS:
            shutil.copy(os.path.join(HERE, h), td)
        shutil.copy(SUITE, td)
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                            os.path.join(td, "test_sowing_heat_ceiling_gate.py")],
                           capture_output=True, text=True, cwd=td)
    return r.returncode, (r.stdout + r.stderr).strip().splitlines()[-1:]


def stage(orig, old, new, label):
    if orig.count(old) != 1:
        raise SystemExit(f"HARNESS DEAD: {label}: the mutation's text occurs {orig.count(old)} times in the gate")
    src = orig.replace(old, new)
    if src == orig:
        raise SystemExit(f"HARNESS DEAD: {label}: MUTATION-APPLIED marker failed (source unchanged)")
    return src


def main():
    orig = open(GATE, encoding="utf-8").read()
    rc, tail = run_suite(orig)
    if rc != 0:
        print(f"HARNESS DEAD: positive control is RED on the unmutated gate: {tail}")
        return 1
    print(f"positive control : GREEN ({tail[0] if tail else ''})")
    label, old, new = SENTINEL
    rc, tail = run_suite(stage(orig, old, new, label))
    if rc == 0:
        print(f"HARNESS DEAD: {label} did not redden the suite")
        return 1
    print(f"sentinel         : REDDENS ({tail[0] if tail else ''})\n")
    caught = survived = 0
    for family, label, old, new in MUTATIONS:
        rc, tail = run_suite(stage(orig, old, new, label))
        if rc == 0:
            survived += 1
            print(f"  SURVIVED  [{family:16s}] {label}")
        else:
            caught += 1
            print(f"  caught    [{family:16s}] {label}  ({tail[0] if tail else ''})")
    print(f"\nTOTAL: {caught} caught, {survived} survived, of {len(MUTATIONS)} injected")
    if survived:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS -- every guard family of sowing_heat_ceiling_gate reddens the suite when broken.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
