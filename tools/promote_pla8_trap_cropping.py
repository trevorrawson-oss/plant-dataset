#!/usr/bin/env python3
"""PLA-8: mint `trap_cropping`, the largest unplaceable piece of advice in two batches. Base be444e25.

ONE NEW KEY in `control_methods`, 58 -> 59. NO existing method is touched, NO crop, NO source_catalog
entry, NO ladder. The rungs are a separate promote (`promote_pla8_trap_cropping_backfill.py`), which
is the chlorothalonil pairing (`d096415` mint, `2e86279` backfill) applied again.

WHY IT IS OWED. Trap cropping is planting a sacrificial patch of a MORE preferred host to concentrate
a pest, then destroying that patch before the pest disperses onto the crop. It had no key, and it was
the single largest unplaceable control in TWO CONSECUTIVE batches (batch 8's leafy greens, batch 10's
brassicas). All five batch-10 authoring agents flagged it independently, which is the mint signal at
full strength. Every near-miss in the catalog is wrong in a different way:

  weed_host_control      REMOVES a plant that hosts the pest; this deliberately ADDS one
  crop_rotation          moves the crop in space; this leaves it and changes what grows beside it
  planting_time_avoidance moves the crop in time; same objection
  garden_sanitation      the destroy-the-trap step looks like cleanup, but the PLANTING step has no home
  beneficial_predators   attracts the pest's ENEMIES; this attracts the PEST

--------------------------------------------------------------------------------------------------
THE T1 READ ANCHORS THE TIMING, NOT THE PRACTICE, BECAUSE THE TIMING IS THE SAFETY-BEARING HALF
--------------------------------------------------------------------------------------------------
Destroying the trap before the pest breeds or disperses is what separates a trap from a nursery.
Leave it standing and the aggregation you built is a local population increase parked beside the
crop. That is the sentence a reader can be harmed by, so it is the one that had to be READ rather
than assumed. Four documents were fetched; three are cited.

  UGA   Circular 1118, "Trap Cropping for Small-Market Vegetable Growers" (Westerfield & Braman,
        reviewed 2022-07-13):
          "A trap crop can be defined as a sacrificial plant that draws away damaging insects from
           the desirable crop."
          "Since the trap crop will be most effective when it begins to flower or seed, it's
           important to establish it earlier than the desirable crop."
          "After trap crops are infested with target insects, they can be controlled with timely
           insecticidal applications or mechanical removal."
          "Plant the trap crop two weeks prior to the desirable crop."
          "Trap crops work best when planted at least 8 to 12 ft away from the desirable vegetables."

  UF    UF/IFAS Gardening Solutions, "Trap Cropping":
          "Once the damaging insects have established themselves on your trap plants, you must
           eradicate them to prevent them from moving on to the main crop."
          "It's recommended to plant trap crops before the main crop; pests are attracted to the
           plant that matures first."
          "Perimeter trap crops should be planted at least 5 feet away from the main crop to prevent
           easy access to your desired plant."
          "Mustard has been an effective control of harlequin bugs on collards."

  UMass UMass Vegetable Program, Squash Bug fact sheet. THE DEADLINE SENTENCE, and the reason this
        method could be minted at all:
          "The trap crop must receive an insecticide application or be mechanically destroyed before
           eggs hatch."

READ AND NOT CITED. Purdue's Vegetable Crops Hotline (Ingwell, 2025-06-26) carries the
harlequin-specific obligation, "Action must be taken on these trap crops to manage the population and
thus protect later plantings." It corroborates but is not declared, because the article lives on
vegcropshotline.org while the catalog's `purdue_ext` entry is anchored at extension.purdue.edu, and a
declared source whose anchor sits on a different domain from its catalog entry is the
`catalog-divergence` shape this repo has been bitten by before. WVU's harlequin bug page carries the
cleanest nursery warning of all ("Some type of control is necessary to avoid the trap crop becoming a
source of infestation") and returned 403 on both user agents, so it is NOT cited: a page that could
not be read is not evidence, whatever a search summary says about it.

--------------------------------------------------------------------------------------------------
THE HANDOFF'S SCAN UNDERCOUNTED, AND THE CORRECTION MATTERS TO THE BACKFILL
--------------------------------------------------------------------------------------------------
`docs/2026-08-28-trap-cropping-mint-handoff.md` measured 20 problems on 18 crops over the eight
standard prose fields. Re-run against `be444e25` over EVERY string field, the true figure is
**22 problems on 20 crops**. The two it missed are `nasturtium`/Aphids and `zinnia`/Japanese beetles,
which carry their prose in `note_beginner`/`note_seasoned` -- a shape used by 91 problems on the
shell and ornamental crops and absent from the scanned field list.

Both are the INVERTED class, and both are canonical trap crops in their own right, so they are the
two records a later pass is MOST likely to attach this rung to wrongly. They join the exclusion set,
taking it from four to six. See the backfill promote, which pins all six in both directions.

--------------------------------------------------------------------------------------------------
WHAT THE ENTRY HAD TO SAY
--------------------------------------------------------------------------------------------------
`applies_to` is `insect_chewing` + `insect_general`: flea beetles are chewing insects, harlequin bug
and stink bugs are general. Both are needed and neither is padding. `insect_soft_bodied` was NOT
declared -- nothing was read for aphids or thrips on a trap crop, and `TYPE_TARGETS` would make the
method legal on them. Same restraint `weed_host_control` used against `mite`.

The cautions carry the destroy timing, quoted to the two sources that state it, because that is the
part that backfires. `best_use` names the two near-misses it is most likely to be confused with, in
as many words, which is the `pyrethrin`-against-`pyrethroid` pattern from batch 10.

REFUSALS: base SHA mismatch; the key already present; a missing required field; `applies_to` not
exactly ['insect_chewing','insect_general']; the tier not `cultural`; any timing disclosure missing
from the cautions; `best_use` not naming both near-misses; a source not in source_catalog or not T1;
a declared source with no anchoring_url; copy hygiene; a crop gaining a rung here; and post-state
blast radius.

Guard suite:      tools/test_promote_pla8_trap_cropping.py
Mutation harness: tools/mutate_pla8_trap_cropping_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_trap_cropping.py [--apply] [--dry-run]
"""
import argparse, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "be444e25a614e2a8ff95dae7aebaf6835277545e7d4b4e7905f1309355e57234"

KEY = "trap_cropping"
VERIFIED = "2026-08-28"

# THE ENTRY AS A LITERAL. It is not read from a staged spec and not derived from anything this file
# also validates: batch 10 shipped `MINT = staged_mint()["entry"]`, which made its own agreement
# check vacuous by construction, and only the mutation harness caught it.
METHOD = {
    "name": "Trap cropping",
    "tier": "cultural",
    # Narrow on purpose. Flea beetles are chewing; harlequin bug and stink bugs are general.
    # insect_soft_bodied is NOT declared: nothing was read for aphids or thrips, and declaring it
    # would make this method legal on them.
    "applies_to": ["insect_chewing", "insect_general"],
    "how_it_works_beginner":
        "A trap crop is a small patch of something the pest likes better than your crop, planted "
        "nearby so the insects gather there instead of on the row you care about. It goes in about "
        "two weeks ahead of the main crop and a short distance away, because these pests head for "
        "whatever is up and flowering first. The patch is meant to be given up rather than "
        "harvested. What matters most is the step after that: once the pest has collected on it, "
        "you pull the patch out or treat it, and you do that before the insects breed and spread. "
        "A loaded patch left standing works as a nursery, raising more of the pest right beside "
        "the bed you were trying to protect.",
    "how_it_works_seasoned":
        "A more attractive host is established ahead of the main crop to aggregate a pest away "
        "from it. UGA defines a trap crop as a sacrificial plant that draws damaging insects off "
        "the desirable crop, and because the trap pulls hardest once it begins to flower or seed, "
        "it says to establish it earlier, about two weeks ahead and 8 to 12 feet away; UF/IFAS "
        "puts a perimeter planting at a 5 foot minimum. The removal step is what separates a trap "
        "from a reservoir. UF/IFAS is explicit that once the insects have established on the trap "
        "you have to eradicate them to stop them moving on to the main crop, and UMass states the "
        "deadline as a generation, that the trap crop must receive an insecticide application or "
        "be mechanically destroyed before eggs hatch. Leave that step out and the tactic inverts: "
        "the aggregation is then a local population increase held beside the crop.",
    "best_use":
        "A bed with a recurring insect that has a strong host preference, where the crop's own "
        "guidance names a plant that pest prefers and there is room for a patch you intend to "
        "sacrifice. Distinct from clearing the weeds that host it, which REMOVES a host plant to "
        "lower the pressure; this deliberately ADDS one to concentrate it. Distinct from crop "
        "rotation, which moves the crop away from the problem; this leaves the crop where it is "
        "and changes what grows beside it. Worth choosing only if the patch will actually be "
        "pulled or treated on time, because an untended trap does the reverse of what it was "
        "planted for.",
    "find_it_beginner":
        "Nothing to buy but seed for the patch, and the plant to use is the one your crop's "
        "guidance names: most often mustard for cabbage-family pests, and nasturtium for flea "
        "beetles on peppers and eggplant. Cheap, fast seed is the right choice, since the patch "
        "is not going to be harvested.",
    "pros": [
        "Costs a packet of seed and a corner of the bed, and it reaches pests that are hard to "
        "treat once they are on the crop",
        "Gathers the pest into one small patch, so handpicking or one spot treatment can do the "
        "work of a whole-bed spray",
        "Suits organic and low-input gardens, because the control step can be pulling the patch "
        "rather than spraying it",
    ],
    "cons": [
        "Works only where the pest clearly prefers the trap plant over the crop, so the choice of "
        "plant carries the result",
        "Needs space and planning: the patch goes in about two weeks ahead of the crop and a few "
        "feet away from it",
        "Adds work rather than removing it, since the patch has to be watched and then destroyed "
        "on time",
    ],
    "cautions": [
        "The patch has to be pulled or treated before the pest breeds. UMass states it as a "
        "deadline, that the trap crop must receive an insecticide application or be mechanically "
        "destroyed before eggs hatch, and UF/IFAS that once the insects have established on the "
        "trap you have to eradicate them to keep them from moving on to the main crop.",
        "A loaded trap left standing works in reverse, raising the local pest population and "
        "holding it next to the crop it was meant to protect. If the patch will not be tended and "
        "removed on schedule, this is not the rung to choose.",
        "Give the patch some distance rather than tucking it against the row: UGA puts the working "
        "separation at 8 to 12 feet and UF/IFAS at a 5 foot minimum for a perimeter planting.",
    ],
    "sources": ["uga_ext", "uf_ifas", "umass_ext"],
    "anchoring_urls": {
        "uga_ext": {"url": "https://fieldreport.caes.uga.edu/publications/C1118/",
                    "verified": VERIFIED},
        "uf_ifas": {"url": "https://gardeningsolutions.ifas.ufl.edu/care/pests-and-diseases/"
                           "pests/trap-cropping/",
                    "verified": VERIFIED},
        "umass_ext": {"url": "https://www.umass.edu/agriculture-food-environment/vegetable/"
                             "fact-sheets/squash-bug",
                      "verified": VERIFIED},
    },
}

# THE SAFETY GUARD. Trap cropping without the removal step raises the local pest population and
# parks it beside the crop, so a sheet that recommends the practice and understates the deadline is
# worse than no sheet. Each axis needs ALL of its tokens present in the cautions.
REQUIRED_DISCLOSURES = {
    "deadline":  ("before eggs hatch",),
    "eradicate": ("eradicate",),
    "backfire":  ("works in reverse", "population"),
    "distance":  ("8 to 12 feet",),
}

# `best_use` must hold this method apart from the two keys it is most likely to be collapsed into.
# Both were proposed and rejected during the measurement, each for a different reason.
REQUIRED_CONTRASTS = ("weeds that host", "crop rotation", "removes", "adds")

# The six problems that MENTION trap cropping and must never carry the rung. Three classes, and a
# rung on any of them ships wrong advice rather than merely redundant advice. Restated here as a
# literal so the mint refuses one too; the backfill pins them in both directions.
EXCLUSIONS = (
    ("radish", "flea-beetles"),            # INVERTED: radish IS the trap crop, for other vegetables
    ("radish", "cabbage-root-maggot"),     # a DIFFERENT action: repurposes an already-damaged sowing
    ("dill", "Parsleyworm (black swallowtail caterpillar)"),   # relocation to KEEP the larvae alive
    ("parsley", "Parsleyworm (black swallowtail caterpillar)"),
    ("nasturtium", "Aphids"),              # INVERTED, missed by the handoff's scan, and the most
                                           # dangerous: its own text describes pulling a loaded trap
                                           # stand, which reads exactly like this method's action
    ("zinnia", "Japanese beetles"),        # INVERTED, and missed by the handoff's scan
)

REQUIRED = ("name", "tier", "applies_to", "how_it_works_beginner", "how_it_works_seasoned",
            "best_use", "pros", "cons", "sources", "anchoring_urls")
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
BRITISH = ("colour", "flavour", "fertilise", "organise", "sulphur", "centre", "metre",
           "mould", "grey", "labour", "practise", "favour")


def hygiene(s):
    if re.search(r"[—–]", s):
        return "em or en dash"
    if "--" in s:
        return "double hyphen"
    if re.search(r"\b(?:always|never|completely|harmless|guaranteed|totally|eliminates?)\b", s, re.I):
        return "absolute claim"
    if re.search(r"\s°F", s):
        return "spaced degF"
    for w in BRITISH:
        if re.search(rf"\b{w}\b", s, re.I):
            return f"British spelling {w!r}"
    if re.search(r"(?<![.!?]\s)(?<!^)\bPlant\b(?! Pro)", s):
        return "capital Plant mid-sentence"
    if re.search(r"\b(?:is|are)\s+safe\b", s, re.I):
        return "bare safety claim"
    return None


def prose_of(m):
    out = []
    for f, v in m.items():
        if f in ("anchoring_urls", "sources", "applies_to", "tier"):
            continue
        out.extend(v if isinstance(v, list) else [v])
    return [s for s in out if isinstance(s, str)]


def missing_disclosures(m):
    """Which timing axes the cautions fail to state. Each needs ALL of its tokens present."""
    blob = " ".join(m.get("cautions") or []).lower()
    return sorted(k for k, toks in REQUIRED_DISCLOSURES.items()
                  if not all(t in blob for t in toks))


def missing_contrasts(m):
    """Which near-miss distinctions `best_use` fails to draw."""
    blob = (m.get("best_use") or "").lower()
    return sorted(t for t in REQUIRED_CONTRASTS if t not in blob)


def find_problem(data, slug, ident):
    """A problem matched by `id` OR by `name`. The excluded four carry ids; the two the handoff's
    scan missed are unladdered and have no `id` at all, so both keys have to be tried."""
    for c in data.get("crops") or []:
        if c.get("slug") != slug:
            continue
        for fam in ("pests", "diseases"):
            for p in c.get(fam) or []:
                if isinstance(p, dict) and ident in (p.get("id"), p.get("name")):
                    return p
    return None


def rungs_of(data, key):
    """Every (slug, problem id or name) carrying a rung for `key`, anywhere on the roster."""
    out = []
    for c in data.get("crops") or []:
        for fam in ("pests", "diseases"):
            for p in c.get(fam) or []:
                if not isinstance(p, dict):
                    continue
                for r in p.get("control_ladder") or []:
                    if r.get("method") == key:
                        out.append((c.get("slug"), p.get("id") or p.get("name")))
    return sorted(out)


def check(data):
    cm = data.get("control_methods") or {}
    sc = data.get("source_catalog") or {}
    if KEY in cm:
        return f"{KEY} is already in the catalog"
    for f in REQUIRED:
        if f not in METHOD or not METHOD[f]:
            return f"mint is missing required field {f!r}"
    if METHOD["tier"] != "cultural":
        return (f"tier is {METHOD['tier']!r}; establishing a sacrificial planting is a cultural "
                f"practice and any other tier misorders every ladder it lands on")
    if METHOD["applies_to"] != ["insect_chewing", "insect_general"]:
        return (f"applies_to must be exactly ['insect_chewing','insect_general']; those are the two "
                f"target sets actually read (flea beetles chewing, harlequin and stink bugs "
                f"general), and a wider scope would make this legal on pests no source covers")

    # THE SAFETY GUARD. Without the removal deadline this sheet recommends building a pest nursery.
    miss = missing_disclosures(METHOD)
    if miss:
        return (f"the cautions do not state {miss}; UMass sets the deadline at 'before eggs hatch' "
                f"and UF/IFAS at eradicating the trap's insects before they move on to the main "
                f"crop, and a sheet that recommends this practice without the removal timing tells "
                f"a reader to raise the local pest population beside their own bed")

    # The whole reason this is a new key rather than a widening of an existing one.
    miss = missing_contrasts(METHOD)
    if miss:
        return (f"best_use does not distinguish this method from {miss}; weed_host_control REMOVES "
                f"a host and crop_rotation moves the crop, while this ADDS a host and leaves the "
                f"crop where it is, and a reader who cannot tell them apart will pick the wrong one")

    for s in METHOD["sources"]:
        if s not in sc:
            return f"source {s!r} is not in source_catalog"
        if (sc[s].get("tier") or "").upper() != "T1":
            return f"source {s!r} is not T1"
        if s not in METHOD["anchoring_urls"]:
            return f"source {s!r} has no anchoring_url"
    for s, a in METHOD["anchoring_urls"].items():
        if s not in METHOD["sources"]:
            return f"anchoring_url {s!r} is not a declared source"
        if not str(a.get("url", "")).startswith("https://"):
            return f"anchoring_url {s!r} is not https"
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(a.get("verified", ""))):
            return f"anchoring_url {s!r} has no valid verified date"

    for s in prose_of(METHOD):
        bad = hygiene(s)
        if bad:
            return f"prose fails copy hygiene ({bad}): {s[:70]!r}"

    # EVERY EXCLUSION MUST RESOLVE. A typo in a slug or a problem name would leave the backfill's
    # exclusion guard protecting nothing while still reporting green -- the derived-guard vacuity
    # shape. Checked here, at the mint, so the list is proven live before any rung exists.
    for slug, ident in EXCLUSIONS:
        if find_problem(data, slug, ident) is None:
            return (f"exclusion {slug}/{ident!r} does not resolve to a problem in canonical, so the "
                    f"refusal it encodes would protect nothing")
    return None


def serialize(data):
    """THE single serialization path; the suite must call THIS, never its own json.dumps."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def snapshot(data):
    dump = lambda o: json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return {"methods": {k: dump(v) for k, v in data["control_methods"].items()},
            "sources": dump(data["source_catalog"]),
            "crops": dump(data["crops"])}


def apply_to(data):
    if KEY in data["control_methods"]:
        raise AssertionError(f"{KEY} already in the catalog")
    data["control_methods"][KEY] = json.loads(json.dumps(METHOD))
    return 1


def verify_post(pre, data):
    cm = data["control_methods"]
    post = snapshot(data)

    # SUBSTANTIVE INVARIANTS FIRST, or the blast-radius loop answers for them.
    #
    # AND THE VERBATIM CHECK COMES LAST OF THIS GROUP, DELIBERATELY. `cm[KEY] != METHOD` subsumes
    # every check below it, so placing it first made the disclosure, contrast, applies_to and tier
    # branches UNREACHABLE by any post-state mutation -- green because an earlier check answered,
    # which is the masked-guard shape that has produced phantom coverage in this repo before. In
    # this order each branch fires on its own defect and reports what actually broke, and the
    # verbatim check remains the catch-all for anything the named branches do not name.
    if KEY not in cm:
        return "post: the method was not minted"
    miss = missing_disclosures(cm[KEY])
    if miss:
        return f"post: the shipped cautions do not state {miss}"
    miss = missing_contrasts(cm[KEY])
    if miss:
        return f"post: the shipped best_use does not distinguish {miss}"
    if cm[KEY]["applies_to"] != ["insect_chewing", "insect_general"]:
        return "post: applies_to is not the narrow scope"
    if cm[KEY]["tier"] != "cultural":
        return "post: the tier is not cultural"
    if cm[KEY] != METHOD:
        return "post: the method did not land verbatim"

    # REFUSAL-SPEC. This promote mints only; no ladder anywhere may gain the rung, and the six
    # excluded problems must not carry it in this state or any later one.
    #
    # THE SIX ARE CHECKED BEFORE THE MINT-ONLY SWEEP, DELIBERATELY. `landed` fires on ANY rung
    # anywhere, so with it first the per-exclusion branch could never fire on its own -- the
    # mutation harness proved exactly that, surviving a mutation that disabled this loop entirely
    # because `landed` answered for it. Ordered this way each branch is reachable and a rung on an
    # excluded problem reports WHY it is forbidden rather than the generic mint-only message.
    for slug, ident in EXCLUSIONS:
        p = find_problem(data, slug, ident)
        if p is None:
            return f"post: exclusion {slug}/{ident!r} no longer resolves"
        if any(r.get("method") == KEY for r in p.get("control_ladder") or []):
            return (f"post: {slug}/{ident!r} carries a {KEY} rung, and it is one of the six that "
                    f"mention trap cropping and must never get one")
    landed = rungs_of(data, KEY)
    if landed:
        return (f"post: {landed} gained a {KEY} rung, and this promote mints only; the rungs are a "
                f"separate promote")

    added = set(post["methods"]) - set(pre["methods"])
    if added != {KEY}:
        return f"post: methods added {sorted(added)}, expected exactly ['{KEY}']"
    if set(pre["methods"]) - set(post["methods"]):
        return "post: a method was dropped"
    for k, before in pre["methods"].items():
        if post["methods"][k] != before:
            return f"post: existing method {k!r} changed, and this promote only mints"
    if post["sources"] != pre["sources"]:
        return "post: source_catalog changed, and this promote mints no source"
    if post["crops"] != pre["crops"]:
        return "post: a crop changed; the rungs are a separate promote"
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("canonical", nargs="?", default=CANONICAL)
    ap.add_argument("--expect-sha", default=BASE_SHA)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    # CHAIN-REPLAY CONTRACT. promote_fixture._from_chain rebuilds an uncommitted intermediate state
    # by invoking its producing promote as
    #     <script> --canonical PATH --expect-sha SHA --apply
    # so a script any later suite must replay through has to accept exactly that shape. This mint
    # produces the backfill's base, which is a real base for the backfill suite and is not its own
    # commit until the mint is committed, so it is a CHAIN member.
    ap.add_argument("--canonical", dest="canonical_flag", default=None)
    a = ap.parse_args()
    a.canonical = a.canonical_flag or a.canonical

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

    pre = snapshot(data)
    before = len(data["control_methods"])
    apply_to(data)
    problem = verify_post(pre, data)
    if problem:
        print("ABORT (post): " + problem, file=sys.stderr)
        return 1

    print(f"PLA-8 -- mint {KEY}, the largest unplaceable control in two consecutive batches")
    print(f"  control_methods : {before} -> {len(data['control_methods'])}")
    print(f"  tier            : {METHOD['tier']}   applies_to: {METHOD['applies_to']}")
    print(f"  disclosures     : {sorted(REQUIRED_DISCLOSURES)} all stated in the cautions")
    print(f"  contrasts       : best_use holds it apart from weed_host_control and crop_rotation")
    print(f"  crops touched   : 0   existing methods touched: 0   sources touched: 0")
    print(f"  NOTE            : 10 shipped ladders gain no rung here; the backfill is a separate "
          f"promote, and {len(EXCLUSIONS)} problems that MENTION trap cropping are excluded from it")
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
