#!/usr/bin/env python3
"""DROP REFLECTIVE MULCH FROM THE ALLIUM THRIPS ADVICE. Base f851dc15.

THE CLAIM IS UNSUPPORTED, AND THE ONE FIELD TRIAL THAT TESTED IT FOUND NO BENEFIT.

Cornell AgriTech (Iglesias & Nault, organic onion thrips trial) reports: "Adults were not affected
by mulch type" and "There were significantly more larvae in reflective than white mulch."

STATED PRECISELY, BECAUSE THE TRIAL DOES NOT SAY WHAT IT IS EASY TO CLAIM IT SAYS: the comparison
is reflective versus WHITE mulch, not reflective versus bare soil. It therefore does NOT establish
that reflective mulch is worse than no mulch. What it establishes is that mulch type did not reduce
adults and that reflective was the worse of the two for larvae. That, plus the sourcing below, is
why the advice comes out.

SOURCING, all read first-hand this session:
* garlic's two cited documents carry NOTHING. `extension.umn.edu/vegetables/growing-garlic` does not
  contain the word "thrips" at all; `extension.usu.edu/.../garlic-in-the-garden` says only "Add
  compost, use mulches or apply a stiff spray of water" -- unqualified "mulches", never reflective.
  The word "silver" appears on that page once, in the DAMAGE description ("leaves turn silver or
  gray"). A damage symptom most likely became a mulch color.
* UC IPM's onion-and-garlic thrips page does not contain the word "mulch".
* The `reflective_mulch` method is itself aphid-and-virus scoped: its own best_use reads "Vegetables
  with a local history of aphid-transmitted virus ... Squash, melon and cucumber are the documented
  cases." Onion thrips is direct feeding damage, not an aphid-vectored virus.

WHAT REPLACES IT IS NOT IN THIS PROMOTE. Straw mulch IS supported for onion thrips -- UMass: "Use
straw mulch to deter thrips"; USU: "Straw or other mulch placed on the plant bed has been shown to
reduce thrips populations" -- but the catalog's `straw_mulch` is scoped `fungal_foliar` /
`disease_general` and cannot carry an insect rung without a catalog widening, which is its own
round. Removing unsupported advice does not depend on that round and should not wait for it.

THE PEAS ARE DELIBERATELY UNTOUCHED, AND A GUARD ASSERTS IT. sugar-snap-peas and snow-peas also
carry reflective mulch against thrips, and theirs is a DIFFERENT and defensible claim: their prose
says "reduce virus spread", thrips there act as virus vectors, and UC IPM's home-and-landscape
thrips page supports reflective mulch generically against winged insects arriving on small plants.
Blanketing one reason across crops is a defect this repo has paid for before.

SCOPE. THREE identical `management_seasoned` strings (garlic, onion, shallot) lose the clause
", use reflective mulch", and ONE shipped rung (garlic / onion-thrips / reflective_mulch) is
removed. Rungs 3244 -> 3243, problems unchanged at 913.

REFUSALS: base SHA mismatch; any pinned text that is not byte-identical; the target rung absent or
at an unexpected position; the removal touching more or fewer than one rung; a pea entry changing
in any way; any allium thrips entry still naming reflective mulch afterward; any other leaf moving;
a catalog change.
"""
import argparse, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "f851dc15a75db4b08b6659e2a2ed06a628d2b34cf688b7a5965ad269ba0c6dab"

ALLIUM_THRIPS = ("garlic", "onion", "shallot", "leek", "spring-onion")
# The crops whose reflective-mulch advice is a DIFFERENT claim and must not move. FOUR rungs, not
# two: each pea crop carries reflective mulch on BOTH `pea-aphid` and `thrips`, and the aphid one
# is the method's textbook use -- aphid-transmitted virus on a young crop, exactly what its own
# best_use describes. Counted, not assumed; the first draft of this guard assumed one per crop and
# the promote refused itself.
PROTECTED = ("sugar-snap-peas", "snow-peas")
EXPECTED_PROTECTED_RUNGS = 4

BEFORE = ("Keep plants vigorous and watered, hose off light infestations, use reflective mulch, and "
          "rotate away from alliums; treat persistent outbreaks per local extension guidance.")
AFTER = ("Keep plants vigorous and watered, hose off light infestations, and rotate away from "
         "alliums; treat persistent outbreaks per local extension guidance.")
PROSE_EDITS = (("garlic", "Onion thrips", "management_seasoned"),
               ("onion", "Onion thrips", "management_seasoned"),
               ("shallot", "Onion thrips", "management_seasoned"))
# (crop, problem NAME, method, index it must sit at, ladder length it must sit in)
RUNG_REMOVAL = ("garlic", "Onion thrips", "reflective_mulch", 1, 3)
EXPECTED_PROSE_EDITS = 3
EXPECTED_RUNGS_BEFORE = 3244
EXPECTED_RUNGS_AFTER = 3243
REFLECTIVE = re.compile(r"reflective|silver(?:ed|y)?\s+(?:mulch|plastic|film)", re.I)


def serialize(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def by_slug(data):
    return {c["slug"]: c for c in data["crops"]}


def problems(crop):
    return [p for f in ("pests", "diseases") for p in crop.get(f) or []]


def find_problem(data, slug, name):
    """Pinned by NAME, not id. onion and shallot carry NO `id` on their problems yet -- batch 24
    is the promote that adds it -- so an id-keyed lookup finds nothing on two of the three crops
    this promote edits."""
    c = by_slug(data).get(slug)
    if c is None:
        raise SystemExit("REFUSED: crop %s is not on the roster" % slug)
    hits = [p for p in problems(c) if p.get("name") == name]
    if len(hits) != 1:
        raise SystemExit("REFUSED: %s has %d problems named %r, expected exactly 1"
                         % (slug, len(hits), name))
    return hits[0]


def rung_count(data):
    return sum(len(p.get("control_ladder") or []) for c in data["crops"] for p in problems(c))


def snapshot(data):
    """CONTENT-KEYED, not path-keyed. Removing a list element shifts every index after it, so a
    path-based snapshot would report the tail of the ladder as dropped-and-re-added and drown the
    one real removal. Rung leaves are keyed by (crop, problem, METHOD, field); everything else by
    path."""
    snap = {}

    def walk(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, path + (str(k),))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, path + ("[%d]" % i,))
        else:
            snap[path] = node
    for c in data["crops"]:
        slug = c["slug"]
        for fam in ("pests", "diseases"):
            for p in c.get(fam) or []:
                for r in p.get("control_ladder") or []:
                    for k, v in r.items():
                        snap[("RUNG", slug, p.get("name"), r.get("method"), k)] = v
        rest = json.loads(json.dumps(c))
        for fam in ("pests", "diseases"):
            for p in rest.get(fam) or []:
                p.pop("control_ladder", None)
        walk(rest, ("crop", slug))
    walk(data["control_methods"], ("control_methods",))
    walk(data["source_catalog"], ("source_catalog",))
    return snap


# ------------------------------------------------------------------ guards
def check_pins(data):
    if len(PROSE_EDITS) != EXPECTED_PROSE_EDITS:
        raise SystemExit("REFUSED: PROSE_EDITS holds %d entries, expected %d"
                         % (len(PROSE_EDITS), EXPECTED_PROSE_EDITS))
    if AFTER == BEFORE or REFLECTIVE.search(AFTER):
        raise SystemExit("REFUSED: the replacement still names reflective mulch")
    for slug, name, field in PROSE_EDITS:
        if slug not in ALLIUM_THRIPS:
            raise SystemExit("REFUSED: %s is not an allium thrips crop" % slug)
        if find_problem(data, slug, name).get(field) != BEFORE:
            raise SystemExit("REFUSED: %s/%s/%s does not match its pinned text; the record moved"
                             % (slug, name, field))
    slug, name, method, idx, ladder_len = RUNG_REMOVAL
    lad = find_problem(data, slug, name).get("control_ladder") or []
    if len(lad) != ladder_len:
        raise SystemExit("REFUSED: %s/%s ladder holds %d rungs, expected %d"
                         % (slug, name, len(lad), ladder_len))
    if lad[idx].get("method") != method:
        raise SystemExit("REFUSED: %s/%s rung %d is %r, expected %r"
                         % (slug, name, idx, lad[idx].get("method"), method))
    if sum(1 for r in lad if r.get("method") == method) != 1:
        raise SystemExit("REFUSED: %s/%s carries %r more than once; the removal is ambiguous"
                         % (slug, name, method))


def check_protected_untouched(pre, data):
    """The peas' reflective mulch is a DIFFERENT claim (thrips as virus vectors on small plants,
    which UC IPM's home-and-landscape page supports) and must not move. Blanketing one reason
    across crops is the defect this guard exists to prevent."""
    post = snapshot(data)
    moved = []
    for k in set(pre) | set(post):
        owner = k[1] if k[0] == "RUNG" else (k[1] if k[0] == "crop" else None)
        if owner in PROTECTED and pre.get(k) != post.get(k):
            moved.append(k)
    if moved:
        raise SystemExit("REFUSED: a protected pea entry changed: %r" % sorted(moved)[:6])
    n = sum(1 for c in data["crops"] if c["slug"] in PROTECTED
            for p in problems(c) for r in p.get("control_ladder") or []
            if r.get("method") == "reflective_mulch")
    if n != EXPECTED_PROTECTED_RUNGS:
        raise SystemExit("REFUSED: the peas hold %d reflective_mulch rungs, expected %d; this "
                         "promote must leave every one of them in place"
                         % (n, EXPECTED_PROTECTED_RUNGS))


def check_coverage(data):
    """No allium thrips entry may still recommend reflective mulch, in prose or as a rung."""
    left = []
    for slug in ALLIUM_THRIPS:
        c = by_slug(data).get(slug)
        if c is None:
            continue
        for p in problems(c):
            if "thrip" not in ((p.get("id") or "") + (p.get("name") or "")).lower():
                continue
            for k, v in p.items():
                if isinstance(v, str) and REFLECTIVE.search(v):
                    left.append("%s/%s/%s" % (slug, p.get("id"), k))
            for r in p.get("control_ladder") or []:
                if r.get("method") == "reflective_mulch":
                    left.append("%s/%s/rung" % (slug, p.get("id")))
    if left:
        raise SystemExit("REFUSED: allium thrips advice still names reflective mulch: %r" % left)
    return len(ALLIUM_THRIPS)


def apply_to(data):
    check_pins(data)
    for slug, name, field in PROSE_EDITS:
        find_problem(data, slug, name)[field] = AFTER
    slug, name, method, _idx, _n = RUNG_REMOVAL
    p = find_problem(data, slug, name)
    p["control_ladder"] = [r for r in p["control_ladder"] if r.get("method") != method]
    return data


def verify_post(pre, data):
    post = snapshot(data)
    added = set(post) - set(pre)
    dropped = set(pre) - set(post)
    if added:
        raise SystemExit("REFUSED: keys added: %r" % sorted(added)[:6])
    slug, name, method, _i, _n = RUNG_REMOVAL
    want_dropped = {("RUNG", slug, name, method, f)
                    for f in ("method", "note_beginner", "note_seasoned")}
    if dropped != want_dropped:
        raise SystemExit("REFUSED: dropped %r, expected exactly the %s rung's leaves"
                         % (sorted(dropped)[:6], method))
    changed = sorted(k for k in set(pre) & set(post) if pre[k] != post[k])
    if len(changed) != EXPECTED_PROSE_EDITS:
        raise SystemExit("REFUSED: %d leaves changed, expected %d: %r"
                         % (len(changed), EXPECTED_PROSE_EDITS, changed[:8]))
    want_changed = sorted(("crop", s, fam, "[%d]" % i, f)
                          for s, name2, f in PROSE_EDITS
                          for fam in ("pests", "diseases")
                          for i, p in enumerate(by_slug(data)[s].get(fam) or [])
                          if p.get("name") == name2)
    if changed != want_changed:
        raise SystemExit("REFUSED: changed %r, expected %r" % (changed, want_changed))
    if rung_count(data) != EXPECTED_RUNGS_AFTER:
        raise SystemExit("REFUSED: %d rungs after, expected %d"
                         % (rung_count(data), EXPECTED_RUNGS_AFTER))
    return len(changed)


def check_catalog_untouched(before_cm, before_sc, data):
    if serialize(data["control_methods"]) != before_cm:
        raise SystemExit("REFUSED: control_methods changed; this promote retires no method")
    if serialize(data["source_catalog"]) != before_sc:
        raise SystemExit("REFUSED: source_catalog changed")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("canonical", nargs="?", default=CANONICAL)
    ap.add_argument("--expect-sha", default=None)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    raw = open(a.canonical, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    expect = a.expect_sha or BASE_SHA
    if sha != expect:
        raise SystemExit("REFUSED: base SHA %s != expected %s" % (sha[:16], expect[:16]))

    data = json.loads(raw.decode("utf-8"))
    if rung_count(data) != EXPECTED_RUNGS_BEFORE:
        raise SystemExit("REFUSED: %d rungs before, expected %d"
                         % (rung_count(data), EXPECTED_RUNGS_BEFORE))
    pre = snapshot(data)
    before_cm = serialize(data["control_methods"])
    before_sc = serialize(data["source_catalog"])

    apply_to(data)
    n = verify_post(pre, data)
    check_catalog_untouched(before_cm, before_sc, data)
    check_protected_untouched(pre, data)
    covered = check_coverage(data)

    blob = serialize(data)
    print("prose edits         : %d" % n)
    print("rungs               : %d -> %d (garlic/onion-thrips/reflective_mulch removed)"
          % (EXPECTED_RUNGS_BEFORE, rung_count(data)))
    print("allium thrips clean : %d/%d crops name reflective mulch nowhere"
          % (covered, len(ALLIUM_THRIPS)))
    print("peas untouched      : %d reflective_mulch rungs left in place"
          % EXPECTED_PROTECTED_RUNGS)
    print("base  SHA           : %s" % sha)
    print("post  SHA           : %s" % hashlib.sha256(blob).hexdigest())
    if a.apply:
        with open(a.canonical, "wb") as fh:
            fh.write(blob)
        print("APPLIED -> %s" % a.canonical)
    else:
        print("dry run; pass --apply to write")


if __name__ == "__main__":
    main()
