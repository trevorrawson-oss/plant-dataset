#!/usr/bin/env python3
"""RETIRE THE CHIVES APHIDS ENTRY. Base b89763b7 (allium record corrections r1).

THE ENTRY FAILS BOTH TESTS THE REST OF THE CHIVES PEST SET RESTS ON.

Chives' pest and disease entries are, by the record's own admission, the ALLIUM FAMILY SET modeled
onto chives. Its open finding `chives_pilot_pests_diseases_allium_modeled` says so outright and
flags the set "for the source-truth sample". That sample has now run. Every other entry survives it
by inheriting from a class-level authority; aphids is the one that inherits from nothing.

* CROP LEVEL -- no US extension publication treats aphids as a chives pest, and three that
  ENUMERATE chives' problems omit it: USU's *Chives in the Garden* (thrips, root maggot, pink root,
  downy mildew), NC State's plant toolbox ("No serious problems"), and PlantVillage. The page this
  entry actually cites asserts the opposite: Wisconsin Horticulture, "Chives have no significant
  insect or disease problems and are not favored by deer or rabbits." Its second citation, UMN
  `growing-chives`, has no pest section at all. Both cited documents contain the word "aphid" ZERO
  times.
* CLASS LEVEL -- **UC IPM's onion and garlic guidelines have no aphid page at all.** Aphids are not
  treated as an allium pest by the authority the rest of this set leans on. Rust, white rot and
  downy mildew all pass this test; UC IPM's rust page even names chives explicitly.

The only chives-specific aphid text found anywhere is sub-T1 (UC Marin Master Gardeners; Ask
Extension diagnoses). Overriding four extension bodies on Master Gardener sourcing is not a trade
this dataset should make.

WHAT THIS IS NOT. It is not a claim that aphids never occur on chives. Onion aphid
(*Neotoxoptera formosana*) is a real Allium specialist and is present in the US. The finding is that
this is not a problem warranting an entry, and the reason is written into the record so a later
pass does not re-add it from a forum thread.

NOTHING USEFUL IS LOST, AND A GUARD PROVES IT. The entry's one genuinely valuable claim -- that
chives repel aphids from neighbouring plants -- is recorded in SIX places under `companions`,
hedged more honestly there than here ("passed along by MSU citing Penn State, but not a measured
trial"). `check_companion_claim_survives` asserts it is still present afterward.

THE OPEN FINDING IS AMENDED, NOT INVALIDATED. It enumerates the modeled set including "aphids
(minor; chives repel them)", so removing the entry makes its prose stale. Following the
append-only convention, a dated CORRECTION is appended and the original wording is left
byte-for-byte: the promote asserts the original text survives as an exact prefix.

SCOPE: one problem removed from chives (pests 4 -> 3, roster problems 913 -> 912) and one finding
summary extended. No other crop, no ladder, no catalog, no source.
"""
import argparse, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "b89763b76e03584a270a569eb1ad0d5359a6a00d8ad217eb9493cf9eaa795a8f"

CROP = "chives"
TARGET_NAME = "Aphids"
TARGET_FAMILY = "pests"
TARGET_INDEX = 3
EXPECTED_PESTS_BEFORE = 4
EXPECTED_PROBLEMS_BEFORE = 913
EXPECTED_PROBLEMS_AFTER = 912
FINDING_ID = "chives_pilot_pests_diseases_allium_modeled"
CORRECTION = (
    " [CORRECTION 2026-09-03: the source-truth sample ran and the APHIDS entry has been REMOVED. No "
    "US extension publication treats aphids as a chives pest; USU's Chives in the Garden, NC State's "
    "plant toolbox and PlantVillage each enumerate chives' problems and omit it, the cited Wisconsin "
    "page states chives have no significant insect or disease problems, and UC IPM's onion and "
    "garlic guidelines carry no aphid page at all, so the entry failed both the crop-level and the "
    "allium-class test the rest of this set rests on. This is not a claim that aphids never occur on "
    "chives: onion aphid (Neotoxoptera formosana) is a real Allium specialist. The aphid-repelling "
    "companion claim is unaffected and remains recorded under companions, hedged as tradition. The "
    "remaining seven entries stand.]")
# The claim that must SURVIVE the removal, and where it lives.
COMPANION_CLAIM = re.compile(r"aphid", re.I)
MIN_COMPANION_SITES = 5


def serialize(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def by_slug(data):
    return {c["slug"]: c for c in data["crops"]}


def problems(crop):
    return [p for f in ("pests", "diseases") for p in crop.get(f) or []]


def problem_count(data):
    return sum(len(problems(c)) for c in data["crops"])


def finding(data):
    for f in by_slug(data)[CROP]["verification_status"]["open_findings"]:
        if f.get("id") == FINDING_ID:
            return f
    raise SystemExit("REFUSED: chives has no open finding %r" % FINDING_ID)


def companion_sites(data):
    """Every place under `companions` that still carries the aphid claim."""
    out = []

    def walk(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, path + "." + str(k))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, path + "[%d]" % i)
        elif isinstance(node, str) and COMPANION_CLAIM.search(node):
            out.append(path)
    walk(by_slug(data)[CROP].get("companions") or {}, "companions")
    return out


def snapshot(data):
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
        # problems keyed by NAME, so removing one does not shift the tail of the list
        for fam in ("pests", "diseases"):
            for p in c.get(fam) or []:
                for k, v in p.items():
                    snap[("PROB", slug, fam, p.get("name"), k)] = json.dumps(
                        v, ensure_ascii=False, sort_keys=True)
        rest = json.loads(json.dumps(c))
        rest.pop("pests", None)
        rest.pop("diseases", None)
        walk(rest, ("crop", slug))
    walk(data["control_methods"], ("control_methods",))
    walk(data["source_catalog"], ("source_catalog",))
    return snap


# ------------------------------------------------------------------ guards
def check_target(data):
    c = by_slug(data).get(CROP)
    if c is None:
        raise SystemExit("REFUSED: crop %s is not on the roster" % CROP)
    lst = c.get(TARGET_FAMILY) or []
    if len(lst) != EXPECTED_PESTS_BEFORE:
        raise SystemExit("REFUSED: %s has %d %s, expected %d"
                         % (CROP, len(lst), TARGET_FAMILY, EXPECTED_PESTS_BEFORE))
    if lst[TARGET_INDEX].get("name") != TARGET_NAME:
        raise SystemExit("REFUSED: %s/%s[%d] is %r, expected %r"
                         % (CROP, TARGET_FAMILY, TARGET_INDEX, lst[TARGET_INDEX].get("name"),
                            TARGET_NAME))
    if sum(1 for p in problems(c) if p.get("name") == TARGET_NAME) != 1:
        raise SystemExit("REFUSED: %s carries %r more than once; the removal is ambiguous"
                         % (CROP, TARGET_NAME))
    if problem_count(data) != EXPECTED_PROBLEMS_BEFORE:
        raise SystemExit("REFUSED: roster holds %d problems, expected %d"
                         % (problem_count(data), EXPECTED_PROBLEMS_BEFORE))


def check_nothing_references_it(data):
    """A problem id is a JOIN KEY: `varieties[].resistance` and `ladder_delta` point at one, and
    removing a referenced entry orphans every grade hanging off it. chives' problems carry NO ids
    yet, so nothing can be pointing here -- asserted rather than assumed."""
    c = by_slug(data)[CROP]
    target = (c.get(TARGET_FAMILY) or [])[TARGET_INDEX]
    if target.get("id") is not None:
        raise SystemExit("REFUSED: the target carries id %r; check every resistance and "
                         "ladder_delta reference before removing it" % target.get("id"))
    if target.get("control_ladder"):
        raise SystemExit("REFUSED: the target carries a shipped control_ladder; removing it would "
                         "drop shipped advice")
    blob = json.dumps(c, ensure_ascii=False)
    for key in ('"resistance"', '"ladder_delta"'):
        if key in blob:
            raise SystemExit("REFUSED: %s carries %s somewhere; the join keys must be checked "
                             "before a problem is removed" % (CROP, key))


def check_companion_claim_survives(data):
    """The entry's one useful claim must outlive it."""
    sites = companion_sites(data)
    if len(sites) < MIN_COMPANION_SITES:
        raise SystemExit("REFUSED: the aphid-repelling companion claim survives in only %d places "
                         "under companions, expected at least %d; removing the pest entry would "
                         "lose it" % (len(sites), MIN_COMPANION_SITES))
    return len(sites)


def check_finding_amended(data, original):
    f = finding(data)
    got = f.get("summary") or ""
    if not got.startswith(original):
        raise SystemExit("REFUSED: the finding's original wording was not preserved byte-for-byte; "
                         "this record is APPEND-ONLY")
    if got == original:
        raise SystemExit("REFUSED: the finding was not amended; removing an entry it enumerates "
                         "leaves its prose stale")
    if "[CORRECTION" not in got[len(original):]:
        raise SystemExit("REFUSED: the appended text is not a dated CORRECTION")


def apply_to(data):
    check_target(data)
    check_nothing_references_it(data)
    c = by_slug(data)[CROP]
    c[TARGET_FAMILY] = [p for p in c[TARGET_FAMILY] if p.get("name") != TARGET_NAME]
    f = finding(data)
    f["summary"] = (f.get("summary") or "") + CORRECTION
    return data


def verify_post(pre, data, original_summary):
    post = snapshot(data)
    added, dropped = set(post) - set(pre), set(pre) - set(post)
    if added:
        raise SystemExit("REFUSED: keys added: %r" % sorted(added)[:6])
    if not dropped:
        raise SystemExit("REFUSED: nothing was removed")
    bad = [k for k in dropped if k[:4] != ("PROB", CROP, TARGET_FAMILY, TARGET_NAME)]
    if bad:
        raise SystemExit("REFUSED: keys dropped outside the target entry: %r" % sorted(bad)[:6])
    changed = sorted(k for k in set(pre) & set(post) if pre[k] != post[k])
    want = [("crop", CROP)]
    for k in changed:
        if k[:2] != ("crop", CROP) or "open_findings" not in k:
            raise SystemExit("REFUSED: a leaf changed outside the chives finding: %r" % (k,))
    if len(changed) != 1:
        raise SystemExit("REFUSED: %d leaves changed, expected exactly the finding summary: %r"
                         % (len(changed), changed[:6]))
    if problem_count(data) != EXPECTED_PROBLEMS_AFTER:
        raise SystemExit("REFUSED: roster holds %d problems after, expected %d"
                         % (problem_count(data), EXPECTED_PROBLEMS_AFTER))
    if len(by_slug(data)[CROP][TARGET_FAMILY]) != EXPECTED_PESTS_BEFORE - 1:
        raise SystemExit("REFUSED: %s holds %d %s after, expected %d"
                         % (CROP, len(by_slug(data)[CROP][TARGET_FAMILY]), TARGET_FAMILY,
                            EXPECTED_PESTS_BEFORE - 1))
    if any(p.get("name") == TARGET_NAME for p in problems(by_slug(data)[CROP])):
        raise SystemExit("REFUSED: %s still carries a %r problem" % (CROP, TARGET_NAME))
    check_finding_amended(data, original_summary)
    return len(dropped)


def check_catalog_untouched(before_cm, before_sc, data):
    if serialize(data["control_methods"]) != before_cm:
        raise SystemExit("REFUSED: control_methods changed")
    if serialize(data["source_catalog"]) != before_sc:
        raise SystemExit("REFUSED: source_catalog changed; this promote retires no source id")


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
    pre = snapshot(data)
    original = finding(data).get("summary") or ""
    before_cm = serialize(data["control_methods"])
    before_sc = serialize(data["source_catalog"])

    apply_to(data)
    n = verify_post(pre, data, original)
    check_catalog_untouched(before_cm, before_sc, data)
    sites = check_companion_claim_survives(data)

    blob = serialize(data)
    print("entry removed       : %s/%s (%d leaves)" % (CROP, TARGET_NAME, n))
    print("roster problems     : %d -> %d" % (EXPECTED_PROBLEMS_BEFORE, problem_count(data)))
    print("companion claim     : survives in %d places under companions" % sites)
    print("finding amended     : %s (original wording preserved)" % FINDING_ID)
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
