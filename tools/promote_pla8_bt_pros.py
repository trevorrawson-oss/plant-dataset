#!/usr/bin/env python3
"""PLA-8: close the "only" selectivity overclaim in bt's PROS. Base 3ec673a7.

ONE STRING: control_methods.bt.pros[1]. No other field, no other method, no crop, no source, no
ladder, no roster change.

THE DEFECT, AND WHY IT SURVIVED THREE EARLIER PROMOTES.

  pros[1]  "Targets caterpillars ONLY, sparing most beneficial insects"
  cautions "Bt kurstaki kills the caterpillars of moths and butterflies AS A GROUP, including
            desirable species such as swallowtails and monarchs"

MethodSheet.tsx renders pros under "Worth knowing" and cautions under "Take care", on the same
sheet, about seventeen lines apart, with pros first. Butterfly caterpillars ARE desirable insects,
so the record contradicts itself in the reader's own scroll, and the reassuring half is what they
hit first.

This is the same class closed in `9116050` (crop prose) and `23b4539` (the catalog's
how_it_works_beginner). It survived both because a claim lives in FIELDS, not in a method: 23b4539
changed exactly one string and was recorded, correctly, as changing one string -- but the arc
around it was described as closing the class, and `pros` was never revisited.

IT ALSO SURVIVED THE SWEEP THAT WAS SUPPOSED TO CATCH IT. The c13ddea5 pass scanned all 50 methods
for safety constructions, returned 15 hits, and adjudicated 13 as correct as written -- explicitly
including bt's `pros`, which it examined for "practically nontoxic" and ruled NPIC's term of art.
The scan vocabulary was `safe` / `non-toxic` / `completely` / `harmless`. "Targets caterpillars
only" matches none of them. The field was read; the wrong question was asked of it.

THE FIX KEEPS THE TRUE CLAIM. Btk really is selective to Lepidoptera, and that selectivity is the
reason to choose it, so deleting the pro would leave the reader worse off. What has to go is the
word "only", which reads as "only pests" rather than "only caterpillars", and "most beneficial
insects", which is what the caution then contradicts.

  new: "Acts on caterpillars as a group, sparing bees and most other beneficials"

"As a group" is the phrasing already used in how_it_works_beginner and best_use, so the sheet now
speaks with one voice, and it carries the hint the caution makes explicit. The instruction half
("keep it off plants you are growing for butterflies") is deliberately NOT repeated here: it already
ends how_it_works_beginner AND best_use, and cautions states it a third time. A fourth on the same
sheet, inside a benefits list, would be noise rather than emphasis.

MEASURED, NOT ASSUMED: a sweep of all 50 methods for selectivity language returned 40 sentences and
bt is the ONLY method whose `pros` claims sparing while its own `cautions` admits harm to a
beneficial. `neem_oil` qualifies its claim ("spares beneficials ONCE IT DRIES", with a caution about
wetting foraging bees) and `iron_phosphate_slug_bait` is comparative ("safer THAN metaldehyde", with
a caution that it is still a pesticide). Both correct as written. 40 hits, 1 defect.

REFUSALS: base SHA mismatch; pros[1] not the expected text; any other pros/cons/cautions entry
changed; any other field of bt changed; any other method changed; any crop changed; the replacement
failing copy hygiene; the replacement still containing the banned construction.

Guard suite:      tools/test_promote_pla8_bt_pros.py
Mutation harness: tools/mutate_pla8_bt_pros_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_bt_pros.py [--apply] [--dry-run]
"""
import argparse, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "3ec673a76717c0a9fbfe9861d6d63ee36e574d59a88b3e3b3b97cccb29253027"

METHOD = "bt"
INDEX = 1
OLD = "Targets caterpillars only, sparing most beneficial insects"
NEW = "Acts on caterpillars as a group, sparing bees and most other beneficials"

# The banned construction: a selectivity claim narrowed by "only" sitting next to a beneficial.
BANNED = re.compile(r"\bonly\b(?=[^.;]*\b(?:beneficial|bee|pollinator|butterfl|wildlife)\b)", re.I)

# Adjudicated CORRECT AS WRITTEN by the sweep; a guard family asserts each survives byte-for-byte.
LEFT_ALONE = {
    "bt.pros[0]": "Practically nontoxic to people, pets, bees, and wildlife",
    "bt.cautions[0]": ("Bt kurstaki kills the caterpillars of moths and butterflies as a group, "
                       "including desirable species such as swallowtails and monarchs; spray only "
                       "plants with a pest problem, never butterfly host plants"),
    "neem_oil.best_use": ("Light, early soft-bodied infestations, especially where you want a "
                          "low-residue option that spares beneficials once it dries."),
    "iron_phosphate_slug_bait.pros[0]": ("Safer for use around children, pets, birds, fish, and "
                                         "other wildlife than metaldehyde baits"),
    "insecticidal_soap.cautions[1]": ("Kills soft-bodied beneficials it directly wets, so spray "
                                      "only where pests are"),
}

BRITISH = ("colour", "flavour", "fertilise", "organise", "sulphur", "centre", "metre",
           "mould", "grey", "labour", "practise")


def hygiene(s):
    """Consumer-copy rules; pros renders in MethodSheet.tsx. Returns a reason or None."""
    if re.search(r"[—–]", s):
        return "em or en dash"
    if "--" in s:
        return "double hyphen"
    if re.search(r"\b(?:always|never|completely|harmless|guaranteed|totally|eliminates?)\b", s, re.I):
        return "absolute claim"
    for w in BRITISH:
        if re.search(rf"\b{w}\b", s, re.I):
            return f"British spelling {w!r}"
    if re.search(r"(?<![.!?]\s)(?<!^)\bPlant\b(?! Pro)", s):
        return "capital Plant mid-sentence"
    if re.search(r"\b(?:is|are)\s+safe\b", s, re.I):
        return "bare safety claim"
    return None


def _at(data, path):
    """Resolve 'method.field[i]' against control_methods."""
    m, rest = path.split(".", 1)
    if rest.endswith("]"):
        f, i = rest[:-1].split("[")
        return data["control_methods"][m][f][int(i)]
    return data["control_methods"][m][rest]


def check(data):
    cm = data.get("control_methods") or {}
    if METHOD not in cm:
        return f"no catalog method {METHOD!r}"
    pros = cm[METHOD].get("pros") or []
    if len(pros) <= INDEX:
        return f"{METHOD}.pros has {len(pros)} entries, expected more than {INDEX}"
    if pros[INDEX] == NEW:
        return "already applied"
    if pros[INDEX] != OLD:
        return f"{METHOD}.pros[{INDEX}] is not the expected text; found {pros[INDEX]!r}"
    bad = hygiene(NEW)
    if bad:
        return f"replacement fails copy hygiene ({bad})"
    if BANNED.search(NEW):
        return "replacement still carries the banned only-next-to-a-beneficial construction"
    if not BANNED.search(OLD):
        return ("the BANNED pattern does not match the text this promote exists to remove, so the "
                "guard is not testing what it claims")
    for path, text in LEFT_ALONE.items():
        try:
            cur = _at(data, path)
        except (KeyError, IndexError):
            return f"left-alone entry {path} is missing"
        if cur != text:
            return f"left-alone entry {path} is not the expected text"
    return None


def serialize(data):
    """THE single serialization path; the suite must call THIS, never its own json.dumps."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def apply_to(data):
    pros = data["control_methods"][METHOD]["pros"]
    if pros[INDEX] != OLD:
        raise AssertionError(f"pros[{INDEX}] drifted; refusing to overwrite")
    pros[INDEX] = NEW
    return 1


def verify_post(data):
    pros = data["control_methods"][METHOD]["pros"]
    if pros[INDEX] != NEW:
        return "post: pros[1] does not carry the replacement"
    if BANNED.search(pros[INDEX]):
        return "post: the banned construction survived"
    for path, text in LEFT_ALONE.items():
        if _at(data, path) != text:
            return f"post: left-alone entry {path} moved"
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("canonical", nargs="?", default=CANONICAL)
    ap.add_argument("--expect-sha", default=BASE_SHA)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    raw = open(a.canonical, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != a.expect_sha:
        print(f"ABORT: base SHA mismatch\n  expected {a.expect_sha}\n  found    {sha}", file=sys.stderr)
        return 1
    data = json.loads(raw.decode("utf-8"))

    problem = check(data)
    if problem:
        print("ABORT: " + problem, file=sys.stderr)
        return 1
    n = apply_to(data)
    problem = verify_post(data)
    if problem:
        print("ABORT (post): " + problem, file=sys.stderr)
        return 1

    print("PLA-8 -- bt.pros[1]: the 'only' selectivity overclaim, closed")
    print(f"  strings changed : {n}")
    print(f"  OLD             : {OLD}")
    print(f"  NEW             : {NEW}")
    print(f"  left alone      : {len(LEFT_ALONE)} adjudicated entries, asserted byte-for-byte")
    out = serialize(data)
    new_sha = hashlib.sha256(out).hexdigest()
    if a.dry_run or not a.apply:
        print(f"DRY RUN -- would write {len(out)} bytes, sha {new_sha}")
        return 0
    open(a.canonical, "wb").write(out)
    print(f"wrote {len(out)} bytes\nnew canonical SHA: {new_sha}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
