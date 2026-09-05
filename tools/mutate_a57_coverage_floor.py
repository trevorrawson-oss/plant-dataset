#!/usr/bin/env python3
"""A57 coverage-floor harness -- proof that the newly-armed ladder coverage floor FIRES, and that
it fires all the way through to a BLOCKED COMMIT.

WHY. A57 arms GREEN: 913 of 913 problem entries laddered, 0 violations roster-wide, and a total
no-op on the seven shells. That is precisely the shape of a gate that reads as coverage while
providing none, and this repo has shipped that before -- a celebrated check that had fired zero
times ever because an upstream filter dropped exactly its rows, and batch 25's harness reporting a
confident 34/34 while grading the clean fixture. Green is not evidence. This is.

THREE INSTRUMENTS, because "the floor should fail a commit" is a claim about all three:

  whole_crop_gate            A57 fires on the crop under gate
  gate_all                   the roster instrument names the crop as FAILED
  precommit_release_verify   the COMMIT is BLOCKED (--base/--candidate offline mode)

A defect the per-crop gate catches but the commit hook does not would leave the user's actual
requirement unmet while every green tick agreed it was met.

LIVENESS DEFENSE (PLA-215 convention items 2 and 3):
  * POSITIVE CONTROL   the unmutated canonical PASSES and A57 stays silent.
  * MUTATION-APPLIED   every mutation carries an `applied` predicate re-checked on the staged tree,
                       so "the injection did nothing" can never be read as "the guard is blind."
  * SENTINEL           a mutation that MUST redden. If it does not, the run exits HARNESS DEAD
                       rather than reporting percentages about a harness that is not grading.

REFUSAL SPECS are recorded as passes, not as vacuity (convention item 5) -- and each one that could
plausibly be invisible carries its own positive control. "The seven shells pass" is worthless on its
own: it is equally consistent with the floor never having looked at them. So the shell refusal spec
is paired with an injection INTO a shell, which must fire.

Usage: python3 tools/mutate_a57_coverage_floor.py [--fast]     (--fast skips the ~30s gate_all leg)
"""
import copy
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CANON = os.path.join(REPO, "crops_data_final.json")

APPLE = "apple"             # 8 problem entries, the ordinary `name`-carrying schema
MICRO = "wheatgrass"        # PLA-452 schema: name_seasoned / name_beginner, NO `name`
SHELL = "avocado"           # pests: [] / diseases: [], status None -- zero entries to ladder


# ---- helpers ---------------------------------------------------------------------------------
def _find(d, slug):
    """The crop, or None. `_crop` raises; the roster-addition mutation needs the soft form."""
    for c in d["crops"]:
        if c.get("slug") == slug:
            return c
    return None


def _crop(d, slug):
    for c in d["crops"]:
        if c.get("slug") == slug:
            return c
    raise SystemExit(f"HARNESS DEAD: crop {slug!r} not in the canonical")


def _prob(crop, pid):
    for fam in ("pests", "diseases"):
        for p in crop.get(fam) or []:
            if isinstance(p, dict) and p.get("id") == pid:
                return p
    raise SystemExit(f"HARNESS DEAD: problem {pid!r} not found on {crop.get('slug')}")


def _unladdered(crop):
    """How many problem entries on this crop carry no ladder. The applied-marker's currency."""
    return sum(1 for fam in ("pests", "diseases") for p in crop.get(fam) or []
               if isinstance(p, dict) and p.get("control_ladder") is None)


def _entries(crop):
    return sum(len(crop.get(fam) or []) for fam in ("pests", "diseases"))


# ---- the mutations ---------------------------------------------------------------------------
# Each: (label, family, slug, mutate, applied) where `applied(crop_after)` must be True or the run
# dies. The families are the SHAPES an unladdered entry can arrive in, not one per line of code.

def m_key_deleted(d, crop):
    """The shape a newly-authored problem entry actually arrives in: no `control_ladder` key at
    all. A floor written `if p['control_ladder'] is None` raises KeyError; one written
    `if p.get('control_ladder') == None` catches it -- but only if somebody checked."""
    del _prob(crop, "codling-moth")["control_ladder"]


def m_set_none(d, crop):
    _prob(crop, "apple-scab")["control_ladder"] = None


def m_micro_key_deleted(d, crop):
    del _prob(crop, "fungus-gnats")["control_ladder"]


def m_micro_set_none(d, crop):
    _prob(crop, "damping-off")["control_ladder"] = None


def m_appended_entry(d, crop):
    """An ADDITION, not an edit. A guard that walks the pre-state and compares keys it already knows
    about is blind to everything the post-state added -- that one shape was all four PLA-162
    defects. The floor must see a problem entry that did not exist before."""
    crop["pests"].append({"id": "brand-new-borer", "name": "Brand new borer", "type": "insect",
                          "description_beginner": "x", "description_seasoned": "x"})


def m_appended_micro_entry(d, crop):
    """The same addition on the microgreen schema, and with NO `id` either -- the worst case for
    the floor's label. It must still fire, and must name the entry off `name_seasoned` rather than
    printing "?" at an operator who then cannot find it."""
    crop["diseases"].append({"name_beginner": "Tray fuzz", "name_seasoned": "Tray fuzz",
                             "type": "fungal", "description_beginner": "x",
                             "description_seasoned": "x"})


def m_shell_gains_a_problem(d, crop):
    """THE POSITIVE CONTROL FOR THE SHELL REFUSAL SPEC. avocado passing the floor is only meaningful
    if the floor is actually looking at avocado. Give it one unladdered problem and it must fire."""
    crop["pests"].append({"id": "persea-mite", "name": "Persea mite", "type": "mite",
                          "description_beginner": "x", "description_seasoned": "x"})


GHOST = "ghost-crop"        # a crop that does not exist in the canonical until a mutation adds it


def m_new_certified_crop(d, crop):
    """A WHOLE NEW CERTIFIED CROP arrives carrying an unladdered problem.

    This is the shape that beat four PLA-162 guards at once -- a clone of `lime` appended to the
    roster as `ghost-crop` while every guard stayed green, because each walked the PRE state and
    compared keys it already knew about. An instrument that only re-checks the crops it has seen
    before cannot see a crop it has not. It is also the likeliest real path to an unladdered entry
    now that the roster is complete: nobody is going to de-ladder apple, but the next crop to
    certify arrives with problems authored and ladders pending.

    `crop` here is the DONOR (apple); the ghost is appended to d["crops"], so this mutation is also
    the reason `stage` cannot assume its target already exists.
    """
    ghost = copy.deepcopy(crop)
    ghost["slug"] = GHOST
    ghost["name"] = "Ghost Crop"
    del ghost["pests"][0]["control_ladder"]
    d["crops"].append(ghost)


MUTATIONS = [
    ("control_ladder key deleted",                    "absence",   APPLE, m_key_deleted),
    ("control_ladder set to null",                    "absence",   APPLE, m_set_none),
    ("key deleted on the microgreen schema",          "schema",    MICRO, m_micro_key_deleted),
    ("set to null on the microgreen schema",          "schema",    MICRO, m_micro_set_none),
    ("a NEW unladdered problem entry appended",       "addition",  APPLE, m_appended_entry),
    ("a NEW unladdered entry, microgreen schema, no id", "addition", MICRO, m_appended_micro_entry),
    ("a SHELL gains an unladdered problem entry",     "shell",     SHELL, m_shell_gains_a_problem),
    ("a NEW certified crop is appended to the roster", "new-crop", APPLE, m_new_certified_crop),
]

# Which crop each mutation must be GRADED on. Every row grades on the crop it mutated, except the
# roster addition, whose defect lands on a crop that did not exist a moment ago -- grading that one
# on the donor would report a clean apple and call the guard blind.
GRADE_ON = {"a NEW certified crop is appended to the roster": GHOST}

# Every mutation above must raise the crop's unladdered count. That is the MUTATION-APPLIED marker:
# it is checked on the staged tree, so a mutation that silently edited nothing cannot be scored.
SENTINEL = ("SENTINEL: every ladder on the crop set to null", APPLE,
            lambda d, crop: [p.__setitem__("control_ladder", None)
                             for fam in ("pests", "diseases") for p in crop.get(fam) or []
                             if isinstance(p, dict)])


# ---- the refusal specs -----------------------------------------------------------------------
def r_empty_ladder(d, crop):
    """`control_ladder: []` is A56's defect ("laddered and left blank", owned since 2026-08-24),
    NOT the floor's. A57 must stay silent or one defect is reported twice under two guards."""
    _prob(crop, "apple-scab")["control_ladder"] = []


REFUSALS = [
    ("an EMPTY ladder is A56's defect, not the floor's", APPLE, r_empty_ladder,
     lambda c: _unladdered(c) == 0),
]


# ---- graders ---------------------------------------------------------------------------------
def gate(path, slug):
    """(passed, a57_fired, unladdered_reported). Graded through the FULL whole_crop_gate, not
    control_ladder_gate standalone -- the question is whether the ARM works."""
    r = subprocess.run([sys.executable, os.path.join(HERE, "whole_crop_gate.py"), slug, path],
                       capture_output=True, text=True, cwd=REPO)
    out = r.stdout + r.stderr
    n = None
    for line in out.splitlines():
        if "unladdered:" in line:
            n = int(line.split("unladdered:")[1].split()[0])
    return "GATE: PASS" in out, "control-ladder-coverage:" in out, n, out


def gate_all_fails(path, slug):
    r = subprocess.run([sys.executable, os.path.join(HERE, "gate_all.py"), path],
                       capture_output=True, text=True, cwd=REPO)
    return r.returncode != 0 and f"FAIL {slug}" in r.stdout


def commit_blocked(base, cand):
    r = subprocess.run([sys.executable, os.path.join(HERE, "precommit_release_verify.py"),
                        "--base", base, "--candidate", cand],
                       capture_output=True, text=True, cwd=REPO)
    return r.returncode != 0 and "BLOCKED" in r.stdout, r.stdout


def stage(slug, fn):
    """Apply `fn` to a scratch canonical. Returns (path, crop_after). Dies if nothing changed."""
    d = json.loads(open(CANON, encoding="utf-8").read())
    crop = _crop(d, slug)
    before = json.dumps(d, sort_keys=True)
    fn(d, crop)
    if json.dumps(d, sort_keys=True) == before:
        raise SystemExit("HARNESS DEAD: mutation left the canonical unchanged")
    fh = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    json.dump(d, fh, ensure_ascii=False, separators=(",", ":"))
    fh.close()
    return fh.name, crop


def main():
    fast = "--fast" in sys.argv
    print("=" * 80)
    print("A57 COVERAGE FLOOR -- graded through whole_crop_gate, gate_all and the pre-commit hook")
    print("=" * 80)

    # ---- POSITIVE CONTROL ----------------------------------------------------------------
    ok, fired, n, _ = gate(CANON, APPLE)
    if not ok or fired:
        print(f"HARNESS DEAD: unmutated canonical -- passed={ok} A57_fired={fired}")
        return 1
    print(f"positive control : GREEN  ({APPLE} passes; A57 silent; {n} unladdered of 8 entries)")

    # The floor must be LOOKING at the shells, not merely not-failing them. Reported here so the
    # refusal spec below is read against a measured scan, never against an unmeasured zero.
    for s in ("avocado", "olive", "button-mushroom"):
        d = json.loads(open(CANON, encoding="utf-8").read())
        _, sfired, sn, _ = gate(CANON, s)
        print(f"                   shell {s:16s} entries={_entries(_crop(d, s))} "
              f"unladdered={sn} A57_fired={sfired}")

    # ---- SENTINEL ------------------------------------------------------------------------
    label, slug, fn = SENTINEL
    p, after = stage(slug, fn)
    if _unladdered(after) != _entries(after) or _entries(after) == 0:
        os.unlink(p); print(f"HARNESS DEAD: {label} did not apply"); return 1
    ok, fired, n, _ = gate(p, slug)
    os.unlink(p)
    if not fired or ok:
        print(f"HARNESS DEAD: {label} did NOT redden A57 (fired={fired}, gate passed={ok}) -- "
              f"the harness is not grading anything.")
        return 1
    print(f"sentinel         : REDDENS ({label}; A57 saw {n})\n")

    # ---- MUTATIONS -----------------------------------------------------------------------
    caught = survived = 0
    fam = {}
    for label, family, slug, fn in MUTATIONS:
        graded_on = GRADE_ON.get(label, slug)
        p, _donor = stage(slug, fn)
        # The applied-marker is read off the STAGED tree at the crop the defect is meant to land
        # on, so "the injection did nothing" can never be scored as "the guard is blind."
        staged = json.loads(open(p, encoding="utf-8").read())
        base = json.loads(open(CANON, encoding="utf-8").read())
        pre_unladdered = _unladdered(_find(base, graded_on) or {})
        after = _find(staged, graded_on)
        if after is None or _unladdered(after) <= pre_unladdered:
            os.unlink(p)
            print(f"HARNESS DEAD: [{family}] {label} -- MUTATION-APPLIED marker failed on "
                  f"{graded_on} (unladdered {pre_unladdered} -> "
                  f"{_unladdered(after) if after else 'crop absent'})")
            return 1
        ok, fired, n, out = gate(p, graded_on)
        os.unlink(p)
        fam.setdefault(family, [0, 0])
        if ok or not fired:
            survived += 1; fam[family][1] += 1
            print(f"  SURVIVED  [{family:8s}] {label}")
        else:
            caught += 1; fam[family][0] += 1
            note = ""
            if "no id" in label:
                # the label must be legible, not "?" -- a floor nobody can act on is not a floor
                line = [l for l in out.splitlines() if "control-ladder-coverage:" in l][0]
                note = "  -> " + line.split("control-ladder-coverage:")[1].strip()[:64]
            print(f"  caught    [{family:8s}] {label} (A57 saw {n}){note}")

    # ---- REFUSAL SPECS -------------------------------------------------------------------
    print()
    refusal_ok = True
    for label, slug, fn, applied in REFUSALS:
        p, after = stage(slug, fn)
        if not applied(after):
            os.unlink(p); print(f"HARNESS DEAD: refusal spec {label!r} did not apply"); return 1
        _, fired, n, out = gate(p, slug)
        os.unlink(p)
        state = "REFUSAL-SPEC pass" if not fired else "BROKEN -- A57 fired"
        refusal_ok &= not fired
        a56 = "control-ladder:" in out
        print(f"  {state}: {label}  (A57 silent={not fired}, A56 fired={a56})")

    # ---- ROSTER + COMMIT REACH -----------------------------------------------------------
    print()
    reach_ok = True
    p, _after = stage(APPLE, m_key_deleted)
    blocked, hookout = commit_blocked(CANON, p)
    reach_ok &= blocked
    print(f"  {'BLOCKED' if blocked else 'NOT BLOCKED -- BROKEN'}: pre-commit hook on a de-laddered "
          f"{APPLE} (this is the user-facing 'fail a commit')")
    if not blocked:
        print("    " + "\n    ".join(hookout.splitlines()[-6:]))
    os.unlink(p)
    # The roster leg deliberately uses a DIFFERENT shape from the commit leg above: a brand-new
    # certified crop, not a de-laddered existing one. gate_all reads the candidate file's own crop
    # list, so it *should* see a crop that was not there before -- but "should" is how four PLA-162
    # guards stayed green while `ghost-crop` was appended to the roster. Measure it.
    if fast:
        print("  SKIPPED (--fast): gate_all roster leg")
    else:
        p2, _ = stage(APPLE, m_new_certified_crop)
        failed = gate_all_fails(p2, GHOST)
        os.unlink(p2)
        reach_ok &= failed
        print(f"  {'FAILS' if failed else 'PASSES -- BROKEN'}: gate_all names {GHOST}, a crop that "
              f"did not exist in the base roster (the roster instrument sees ADDITIONS)")

    # ---- REPORT --------------------------------------------------------------------------
    print("\n" + "-" * 80)
    for f in sorted(fam):
        c, s = fam[f]
        print(f"  {f:9s} {c} caught / {c + s}" + ("" if not s else f"   <-- {s} SURVIVED"))
    print("-" * 80)
    print(f"TOTAL: {caught} caught, {survived} survived, of {len(MUTATIONS)} injected; "
          f"{len(REFUSALS)} refusal spec(s); roster+commit reach {'OK' if reach_ok else 'BROKEN'}")
    if survived or not refusal_ok or not reach_ok:
        print("\nRESULT: FAIL -- the coverage floor does not hold everywhere it claims to.")
        return 1
    print("\nRESULT: PASS -- every shape of an unladdered entry reddens A57, on both schemas, "
          "through the per-crop gate, the roster gate and the commit hook.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
