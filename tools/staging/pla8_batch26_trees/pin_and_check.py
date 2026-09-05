#!/usr/bin/env python3
"""pin_and_check -- PLA-8 batch 26 (trees and shrubs): build the TARGET-STATE scratch and run the PLA-449
problem-id collision guard against POST-APPLY data, before fan-out.

WHY POST-APPLY. `problem_id_collision_gate` has three checks and two of them (NAME_SHARED,
FAMILY_MEMBER) key off the display `name` of the minted id. A minted id not yet in the file has no
name, so running the guard against untouched canonical gets you check 1 only -- a third of the guard
behind an output that looks complete. The guard's CLI warns about this on stderr rather than
returning a quiet clean.

WHY AT ID-PINNING TIME. This is the only point at which changing an id is free. After fan-out every
authoring agent has written prose against it. Batch 24 minted `pink-root` against celery's
`pink-rot` (edit distance 1) while its own `_stem_key` check read the two as distinct.

WHY THE SPEC IS A TARGET STATE, NOT AN ID MAP. This batch retires three array-duplicate entries and
splits at least one bundle. The names the guard must see are the names that will SHIP, not
canonical's. An id map over canonical would hand the guard the old names and report a clean that
means nothing.

COVERAGE IS CHECKED IN BOTH DIRECTIONS, AND RETIREMENT IS DECLARED. Every canonical problem must be
accounted for exactly once: carried (KEEP), renamed, consumed by a SPLIT, or named in `_retired`.
A retirement inferred from mere absence is invisible to a walk that iterates the target, which is
the PLA-162 shape -- iterating `pre` makes additions in `post` invisible, and iterating `post` makes
deletions in `pre` invisible. So both sets are reconciled explicitly before anything is applied.

Usage:
    pin_and_check.py                    # build scratch_postapply.json, run the guard
    pin_and_check.py --self-test        # inject a known collision and confirm the guard reddens
"""
import argparse, copy, hashlib, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
CANON = os.path.join(REPO, "crops_data_final.json")
GATE = os.path.join(REPO, "tools", "problem_id_collision_gate.py")
PINS = os.path.join(HERE, "pinned_ids.json")
SCRATCH = os.path.join(HERE, "scratch_postapply.json")

EXPECTED_BASE_SHA = "ce98b0a6f83cc04b380a6c3be3009709a7c6c3626b2611c88fafec1164997144"  # batch 25 + rosemary cert-log correction
CROPS = ["mulberry", "pawpaw", "pear-asian", "pear-european", "persimmon", "pomegranate"]

FROM_RE = re.compile(r"^(?:RENAME|SPLIT \d+/\d+) from '([^']+)'")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_canonical():
    got = sha256(CANON)
    if got != EXPECTED_BASE_SHA:
        sys.exit("REFUSING TO RUN: canonical has moved.\n"
                 f"  expected {EXPECTED_BASE_SHA}\n  got      {got}\n"
                 "Re-measure the pin table against the new canonical; never retune a pin to match.")
    with open(CANON, encoding="utf-8") as f:
        return json.load(f)


def spec_rows(pins):
    for crop, fields in pins.items():
        if crop.startswith("_"):
            continue
        for field in ("pests", "diseases"):
            for row in fields.get(field, []):
                yield crop, field, row


def source_name(row):
    """Which canonical entry this target row draws from."""
    m = FROM_RE.match(row.get("from", ""))
    return m.group(1) if m else row["name"]


def reconcile(pins, data):
    """Account for every canonical problem exactly once, and every target row's source."""
    idx = {c["slug"]: c for c in data["crops"]}
    canon = {(crop, f, e["name"])
             for crop in CROPS for f in ("pests", "diseases") for e in idx[crop].get(f) or []}

    consumed, problems = {}, []
    for crop, field, row in spec_rows(pins):
        key = (crop, field, source_name(row))
        if key not in canon:
            problems.append(f"PHANTOM SOURCE: {crop}/{field} target {row['name']!r} draws from "
                            f"{source_name(row)!r}, which is not in canonical")
        consumed.setdefault(key, []).append(row["name"])

    for r in pins.get("_retired", []):
        key = (r["crop"], r["field"], r["name"])
        if key not in canon:
            problems.append(f"PHANTOM RETIREMENT: {key} is not in canonical")
        if key in consumed:
            problems.append(f"CONTRADICTION: {key} is both retired and used by {consumed[key]}")
        consumed.setdefault(key, []).append("<retired>")

    for key in sorted(canon - set(consumed)):
        problems.append(f"UNACCOUNTED CANONICAL PROBLEM: {key} is neither carried, renamed, "
                        f"split-from, nor declared in _retired")

    if problems:
        for p in problems:
            print("  " + p, file=sys.stderr)
        sys.exit(f"RECONCILE FAILED: {len(problems)} problem(s)")

    n_target = sum(1 for _ in spec_rows(pins))
    print(f"reconcile OK: {len(canon)} canonical problems -> {n_target} target "
          f"({len(pins.get('_retired', []))} retired, "
          f"{sum(1 for _,_,r in spec_rows(pins) if r['from'].startswith('SPLIT'))} split rows, "
          f"{sum(1 for _,_,r in spec_rows(pins) if r['from'].startswith('RENAME'))} renamed)")


def build_post(data, pins):
    out = copy.deepcopy(data)
    idx = {c["slug"]: c for c in out["crops"]}
    for crop in CROPS:
        for field in ("pests", "diseases"):
            by_name = {e["name"]: e for e in idx[crop].get(field) or []}
            new = []
            for row in pins[crop].get(field, []):
                entry = copy.deepcopy(by_name[source_name(row)])
                entry["name"] = row["name"]
                entry["id"] = row["id"]
                entry["type"] = row["type"]
                entry["severity"] = row["severity"]
                new.append(entry)
            idx[crop][field] = new
    return out


def run_gate(path, minted, strict=True):
    cmd = [sys.executable, GATE, path, "--minted", ",".join(sorted(minted))]
    if strict:
        cmd.append("--strict")
    print("\n$ problem_id_collision_gate.py <scratch> --minted <ids> --strict\n" + "=" * 78)
    r = subprocess.run(cmd, capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    if r.stderr:
        sys.stderr.write("STDERR:\n" + r.stderr)
    print("=" * 78 + f"\ngate exit: {r.returncode}")
    return r.returncode, r.stdout + r.stderr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    data = load_canonical()
    with open(PINS, encoding="utf-8") as f:
        pins = json.load(f)

    reconcile(pins, data)
    post = build_post(data, pins)
    minted = {row["id"] for _, _, row in spec_rows(pins)}
    with open(SCRATCH, "w", encoding="utf-8") as f:
        json.dump(post, f, ensure_ascii=False)
    print(f"scratch written: {os.path.basename(SCRATCH)}  ({len(minted)} distinct ids)")

    if args.self_test:
        # LIVENESS DEFENSE. A clean run proves nothing unless the guard can be made to redden.
        probe = copy.deepcopy(post)
        pidx = {c["slug"]: c for c in probe["crops"]}
        pidx["mulberry"]["pests"][0]["id"] = "bird"   # roster has `birds`, distance 1
        probe_path = SCRATCH + ".selftest"
        with open(probe_path, "w", encoding="utf-8") as f:
            json.dump(probe, f, ensure_ascii=False)
        rc, out = run_gate(probe_path, minted | {"bird"})
        os.unlink(probe_path)
        if "bird" not in out or rc == 0:
            sys.exit("HARNESS DEAD: planted collision `bird` did not redden the guard")
        print("\nSELF-TEST PASS: planted collision caught, nonzero exit")
        return 0

    # THE BATCH'S GATE CONDITION IS "INTRODUCES NOTHING UNREGISTERED", NOT "REPORTS NOTHING".
    #
    # A whole-roster --strict run can never go clean for this batch, and that is correct behaviour,
    # not a failure to fix: batch 26 JOINS ids that already carry known duplicate pairs (pomegranate
    # joins `aphids`, `whiteflies` and `gray-mold`; persimmon joins `anthracnose`; the pears join
    # `stink-bugs`). Those are PLA-448 s4a's eight duplicates, whose merge is s7's fast-follow and
    # is explicitly out of PLA-8's scope.
    #
    # Registering them here would be the one thing problem_id_registry.json forbids: "an id pair
    # that is genuinely one problem does NOT belong here; merge the ids instead." Quieting the gate
    # by registration is exactly how a registration path decays into a blind spot, and PLA-450
    # owns the inherited pairs.
    #
    # So the condition is a DIFFERENCE: run the gate on canonical and on the post-apply scratch,
    # compare id-pair sets, and require that every pair this batch INTRODUCES is registered.
    # Inherited pairs are reported and pass. This is measured, not asserted.
    print("\n" + "=" * 78 + "\nINTRODUCED-vs-INHERITED\n" + "=" * 78)
    base = gate_pairs(CANON)
    post = gate_pairs(SCRATCH)
    introduced = sorted(set(post) - set(base))
    inherited = sorted(set(post) & set(base))
    unregistered = [p for p in introduced if not post[p]]

    print(f"pairs on canonical: {len(base)}   pairs post-apply: {len(post)}")
    print(f"INTRODUCED by this batch: {len(introduced)}")
    for a, b in introduced:
        print(f"    {'REGISTERED' if post[(a,b)] else 'UNREGISTERED'}  {a} <-> {b}")
    print(f"INHERITED (pre-existing, this batch only joins them): {len(inherited)}")
    for a, b in inherited:
        print(f"    {a} <-> {b}")

    if unregistered:
        print(f"\nREFUSED: {len(unregistered)} pair(s) introduced by this batch are unregistered.")
        return 1
    print(f"\nPASS: this batch introduces {len(introduced)} collision pair(s), all adjudicated and "
          f"registered; it creates no new unadjudicated duplicate.")
    return 0


def gate_pairs(path):
    """Whole-roster {id-pair: registered} from the gate's own JSON. Use the gate's registration
    verdict rather than re-implementing the registry lookup here; a second copy of that logic is
    the same retyping mistake that put a wrong tier order in this batch's first validator."""
    r = subprocess.run([sys.executable, GATE, path, "--show-registered", "--json"],
                       capture_output=True, text=True)
    if r.returncode not in (0, 1):
        sys.exit(f"gate failed on {path}: {r.stderr}")
    out = {}
    for f in json.loads(r.stdout):
        out[tuple(sorted(f["ids"]))] = bool(f.get("registered"))
    return out


if __name__ == "__main__":
    sys.exit(main())
