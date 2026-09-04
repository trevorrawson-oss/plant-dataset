#!/usr/bin/env python3
"""Mutation harness for the rosemary cert-log correction suite. PLA-215 bar.

Liveness defense: MUTATION-APPLIED marker asserted on disk, a byte-difference assertion, a positive
control (unmutated scratch must be GREEN) and a SENTINEL that must redden or the run exits
HARNESS DEAD. Bytecode writing is disabled and __pycache__ cleared per run: CPython's source-mtime
cache has one-second granularity, so rapid rewrites of one file can leave the suite importing the
CLEAN module and every mutation reporting as surviving.
"""
import os, shutil, subprocess, sys, tempfile, re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PROMOTE = "promote_rosemary_certlog_correction.py"
SUITE = "test_promote_rosemary_certlog_correction.py"
MARKER = "# MUTATION-APPLIED"

MUTATIONS = [
    ("prefix", "prefix_check_removed",
     'if not vb[FIELD].startswith(va[FIELD]):',
     'if False:  ' + MARKER, "test_edited_rather_than_appended_is_refused"),
    ("prefix", "exact_append_unchecked",
     'if vb[FIELD] != va[FIELD] + CORRECTION:',
     'if False:  ' + MARKER, "test_a_different_appended_text_is_refused"),
    ("scope", "sibling_field_move_allowed",
     'if vmoved != [FIELD]:',
     'if False:  ' + MARKER, "test_a_second_field_moving_is_refused"),
    ("scope", "untouched_crops_unchecked",
     'if json.dumps(a, sort_keys=True) != json.dumps(b, sort_keys=True):',
     'if False:  ' + MARKER, "test_another_crop_moving_is_refused"),
    ("scope", "top_level_unchecked",
     'if json.dumps(pre[k], sort_keys=True) != json.dumps(post[k], sort_keys=True):',
     'if False:  ' + MARKER, "test_top_level_change_is_refused"),
    ("precondition", "stale_claim_presence_unchecked",
     'if STALE_CLAIM not in v:',
     'if False:  ' + MARKER, "test_missing_stale_claim_is_refused"),
    ("precondition", "double_append_allowed",
     'if "[CORRECTION" in v:',
     'if False:  ' + MARKER, "test_double_append_is_refused"),
    ("precondition", "empty_field_allowed",
     'if not isinstance(v, str) or not v.strip():',
     'if False:  ' + MARKER, "test_empty_field_is_refused"),
    ("mechanics", "canonical_written_indented",
     'return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")',
     'return json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")  ' + MARKER,
     "test_serialize_is_compact"),
]


def run(tools, selector):
    shutil.rmtree(os.path.join(tools, "__pycache__"), ignore_errors=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", os.path.join(tools, SUITE),
                        "-q", "-k", selector, "--no-header", "-p", "no:cacheprovider"],
                       capture_output=True, text=True, cwd=os.path.dirname(tools), env=env)
    return r.returncode


def apply_mut(tools, old, new, target=PROMOTE):
    p = os.path.join(tools, target)
    clean = open(p, encoding="utf-8").read()
    if old not in clean:
        return None, f"ANCHOR NOT FOUND: {old[:60]!r}"
    mutated = clean.replace(old, new, 1)
    if mutated == clean:
        return None, "replacement produced identical bytes"
    open(p, "w", encoding="utf-8").write(mutated)
    back = open(p, encoding="utf-8").read()
    if MARKER not in back or back == clean:
        return None, "MUTATION-APPLIED marker absent, or file identical to clean"
    return clean, None


def main():
    tmp = tempfile.mkdtemp(prefix="mut_certlog_")
    tools = os.path.join(tmp, "tools"); os.makedirs(tools)
    for f in os.listdir(HERE):
        if f.endswith(".py") and os.path.isfile(os.path.join(HERE, f)):
            shutil.copy2(os.path.join(HERE, f), os.path.join(tools, f))
    os.symlink(os.path.join(REPO, "crops_data_final.json"),
               os.path.join(tmp, "crops_data_final.json"))
    try:
        if run(tools, "test_the_stale_claim_is_actually_present") != 0:
            sys.exit("HARNESS DEAD: the UNMUTATED scratch is already failing; every 'caught' would "
                     "be meaningless.")
        print("positive control: unmutated scratch GREEN\n")
        # SENTINEL, anchor derived so a legitimate pin move cannot silently kill it.
        src = open(os.path.join(tools, SUITE), encoding="utf-8").read()
        m = re.search(r'^BASE_SHA = "([0-9a-f]{64})"$', src, re.M)
        if not m:
            sys.exit("HARNESS DEAD: cannot locate BASE_SHA to build a sentinel from")
        clean, err = apply_mut(tools, m.group(0), 'BASE_SHA = "' + "0"*64 + '"  ' + MARKER, SUITE)
        if err:
            sys.exit(f"HARNESS DEAD: sentinel could not be applied: {err}")
        rc = run(tools, "test_base_sha_is_pinned")
        open(os.path.join(tools, SUITE), "w", encoding="utf-8").write(clean)
        if rc == 0:
            sys.exit("HARNESS DEAD: the sentinel SURVIVED; nothing below can be trusted.")
        print("sentinel: reddened as required\n")

        caught, survived, broken = [], [], []
        for fam, name, old, new, sel in MUTATIONS:
            clean, err = apply_mut(tools, old, new)
            if err:
                broken.append((fam, name, err)); print(f"  BROKEN   {fam}/{name}: {err}"); continue
            rc = run(tools, sel)
            open(os.path.join(tools, PROMOTE), "w", encoding="utf-8").write(clean)
            if rc == 0:
                survived.append((fam, name, sel)); print(f"  SURVIVED {fam}/{name} ({sel})")
            else:
                caught.append((fam, name)); print(f"  caught   {fam}/{name}")
        print(f"\n{len(MUTATIONS)} injected: {len(caught)} caught, {len(survived)} survived, "
              f"{len(broken)} broken")
        return 1 if (survived or broken) else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
