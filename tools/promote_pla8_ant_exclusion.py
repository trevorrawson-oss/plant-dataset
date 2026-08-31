#!/usr/bin/env python3
"""PLA-8 -- MINT `ant_exclusion`, the catalog's 62nd method. Base 2a9d3c85.

Adds ONE control method and THREE source-catalog entries. Touches NO crop: this is a pure catalog
revision, and the guard suite asserts every crop record is byte-identical across the promote.

--------------------------------------------------------------------------------------------------
WHY THIS METHOD EXISTS: A DISEASE WHOSE ENTIRE CONTROL IS AN INSECT CONTROL
--------------------------------------------------------------------------------------------------
Batch 18 (acid citrus) could not ship. `sooty-mold` is typed `fungal`, but everything its record
prescribes is INSECT control: suppress the honeydew producer, manage the ants that protect it, wash
the film off. `TYPE_TARGETS` forbids a fungal-typed problem from naming any insect method, so lemon
honestly emitted `control_ladder: null` rather than stretch a key, and `ladder_batch.py merge`
crashes on that because the runner has no representation for a problem that cannot be laddered yet.

Both citrus authors ALSO reported ant exclusion as the largest citrus gap independently, on scale
and mealybugs, where the crops' own prose says "control ant access to the canopy (a sticky band on
the trunk helps) so resident predators and parasites can work" and no catalog key could carry it.
Playbook section 6: when several bots independently report the same control blocked, that is the
catalog, not the authors.

--------------------------------------------------------------------------------------------------
THE ANCHORS WERE FETCHED AND READ, AND THE FIRST CANDIDATE FAILED
--------------------------------------------------------------------------------------------------
The cheapest candidate was the URL the crops already cite for their ant advice,
`ipm.ucanr.edu/PMG/GARDEN/FRUIT/citrus.html`. It was READ and it is an INDEX PAGE with no ant
content at all: no tending mechanism, no exclusion method, no sooty mold link. That is the exact
`container_culture` failure this rule exists to prevent, and it is separately FILED as a
mis-pointed-key defect on lemon's mealybug and sooty-mold entries.

Three T1 documents carry the claims this method makes:

* **UC IPM Pest Notes 7411, Ants** -- the mechanism and the barrier, verbatim: "Frequently outbreaks
  of scales and aphids occur when ants tend them for honeydew, because the ants protect scales and
  aphids from their natural enemies." / "These ants can be kept out by banding tree trunks with
  sticky substances such as Tanglefoot. Trim branches to keep them from touching structures or
  plants... When using Tanglefoot on young or sensitive trees, protect them from possible injury by
  wrapping the trunk with a collar of heavy paper, duct tape, or fabric tree wrap and coating this
  with the sticky material."
* **UC IPM, Ants (Citrus)** -- the citrus-specific form: ants "protect these pest insects from their
  natural enemies, thus interrupting biological control"; sticky materials "applied on top of a tree
  wrap to the bark"; "Skirt prune trees, i.e., remove branches within 12 to 30 inches of the ground".
* **UC IPM Pest Notes 74108, Sooty Mold** -- THE DISEASE-SIDE LINK, which is the whole reason
  `disease_general` is in `applies_to`: "Control of sooty mold begins with managing the insect
  creating the honeydew." / "Ants are attracted to and use honeydew as a source of food. They will
  protect honeydew-producing insects from predators and parasites in order to harvest the honeydew."
  Without this document the disease half would be an INFERENCE across two steps, and the method
  would have shipped covering insects only, leaving batch 18 blocked exactly as it was.

--------------------------------------------------------------------------------------------------
TIER IS `physical`, AND THE MECHANISM AGREES WITH THE PRECEDENT
--------------------------------------------------------------------------------------------------
Every exclusion/barrier method in the catalog is `physical` (`exclusion_fencing`, `bird_netting`,
`swd_exclusion_netting`, `slug_traps_barriers`). That is not just convention here: the sources say to
exclude ants SO THAT natural enemies can work, so this rung must sit BEFORE `beneficial_predators`
in any ladder. physical < biological delivers that ordering automatically.

REFUSALS: base SHA mismatch; the method key already present; a source id already present; a missing
required method field; a tier or applies_to off the pinned values; an anchoring url that is not the
catalog url for its source id; ANY crop record changing; any OTHER catalog method changing; any
other source_catalog entry changing; counts off.

Guard suite:      tools/test_promote_pla8_ant_exclusion.py
Mutation harness: tools/mutate_pla8_ant_exclusion_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_ant_exclusion.py [--apply] [--dry-run] [--canonical PATH]
"""
import argparse, copy, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "2a9d3c85dbb2da3ccbd69cd1798017d3ca8a3bb6280b8e212d5f63b86adef4af"

METHOD_KEY = "ant_exclusion"
EXPECT_METHODS_BEFORE = 61
EXPECT_SOURCES_BEFORE = 215

# Full document-scoped shape. `title` is REQUIRED by A54 and is READ OFF THE DOCUMENT's own <title>,
# never inferred from the id, URL or pub number -- the first version of this mint shipped `name`
# only and gate_all went 121/121 FAILED, which is A54 doing exactly its job (it exists because a
# wrong pub number once hid behind a plausible-looking id; PLA-155/PLA-199).
NEW_SOURCES = {
    "ucanr_ext_ants": {
        "id": "ucanr_ext_ants",
        "name": "UC IPM Pest Notes -- Ants",
        "title": "Ants / Home and Landscape / UC Statewide IPM Program (UC IPM)",
        "publisher": "UC ANR",
        "url": "https://ipm.ucanr.edu/PMG/PESTNOTES/pn7411.html",
        "source_class": "university_extension",
        "trust_tier": "high",
        "accessed": "2026-08",
        "tier": "T1",
        "citable_for": (
            "UC IPM Pest Notes 7411. Cited for the ant-tending MECHANISM and the exclusion METHOD "
            "behind `ant_exclusion`: \"Outdoors ants are attracted to honeydew that soft scales, "
            "mealybugs, and aphids produce\"; \"Frequently outbreaks of scales and aphids occur "
            "when ants tend them for honeydew, because the ants protect scales and aphids from "
            "their natural enemies\"; and the barrier itself, \"These ants can be kept out by "
            "banding tree trunks with sticky substances such as Tanglefoot. Trim branches to keep "
            "them from touching structures or plants\", with the bark caution \"When using "
            "Tanglefoot on young or sensitive trees, protect them from possible injury by wrapping "
            "the trunk with a collar of heavy paper, duct tape, or fabric tree wrap and coating "
            "this with the sticky material.\" Does NOT mention sooty mold; that half is anchored "
            "separately to ucanr_ext_sooty_mold."
        ),
        "_admission_provenance": (
            "Minted 2026-08-31 (PLA-8 ant_exclusion mint). Document fetched and read before "
            "pinning; title read off the document's own <title>. The cheapest candidate anchor, "
            "ipm.ucanr.edu/PMG/GARDEN/FRUIT/citrus.html, was read FIRST and REJECTED: it is an "
            "index page carrying no ant content at all, which is separately filed as a "
            "mis-pointed-key defect on lemon's mealybug and sooty-mold entries."
        ),
    },
    "ucanr_ext_sooty_mold": {
        "id": "ucanr_ext_sooty_mold",
        "name": "UC IPM Pest Notes -- Sooty Mold",
        "title": "Sooty Mold / Home and Landscape / UC Statewide IPM Program (UC IPM)",
        "publisher": "UC ANR",
        "url": "https://ipm.ucanr.edu/PMG/PESTNOTES/pn74108.html",
        "source_class": "university_extension",
        "trust_tier": "high",
        "accessed": "2026-08",
        "tier": "T1",
        "citable_for": (
            "UC IPM Pest Notes 74108. THE DISEASE-SIDE ANCHOR, and the sole reason "
            "`disease_general` is in ant_exclusion's applies_to: \"Control of sooty mold begins "
            "with managing the insect creating the honeydew\"; \"Ants are attracted to and use "
            "honeydew as a source of food. They will protect honeydew-producing insects from "
            "predators and parasites in order to harvest the honeydew\"; and \"Once ants have "
            "been eliminated, if predators and parasites are sufficiently abundant, they will "
            "quickly begin feeding on and reducing populations.\" Without this document the "
            "disease half of the method would be an inference across two steps."
        ),
        "_admission_provenance": (
            "Minted 2026-08-31 (PLA-8 ant_exclusion mint). Fetched and read specifically to test "
            "whether ant control is documented as part of SOOTY MOLD management rather than "
            "inferred from the honeydew chain. It is. Title read off the document's own <title>."
        ),
    },
    "uc_ipm_citrus_ants": {
        "id": "uc_ipm_citrus_ants",
        "name": "UC IPM -- Ants (Citrus, UC ANR Pub 3441)",
        "title": ("Ants / Citrus / Agriculture: Pest Management Guidelines / "
                  "UC Statewide IPM Program (UC IPM)"),
        "publisher": "UC Statewide Integrated Pest Management Program (UC ANR)",
        "url": "https://ipm.ucanr.edu/agriculture/citrus/ants/",
        "source_class": "university_extension",
        "trust_tier": "high",
        "accessed": "2026-08",
        "tier": "T1",
        "citable_for": (
            "UC IPM Pest Management Guidelines: Citrus (UC ANR Publication 3441). Cited for the "
            "citrus-specific form of ant exclusion: ants \"protect these pest insects from their "
            "natural enemies, thus interrupting biological control\"; sticky materials \"applied "
            "on top of a tree wrap to the bark\"; and skirt pruning, \"remove branches within 12 "
            "to 30 inches of the ground\". A COMMERCIAL guideline, so cited for the practice and "
            "its mechanism, not for home-garden product recommendations."
        ),
        "_admission_provenance": (
            "Minted 2026-08-31 (PLA-8 ant_exclusion mint). Document fetched and read before "
            "pinning; title read off the document's own <title>. Sibling of the existing "
            "uc_ipm_citrus_timings, which is the same Pub 3441 guideline at a different page."
        ),
    },
}

VERIFIED = "2026-08-31"

ANT_EXCLUSION = {
    "name": "Ant exclusion",
    "tier": "physical",
    "applies_to": ["insect_soft_bodied", "insect_general", "disease_general"],
    "how_it_works_beginner": (
        "Ants farm the sap-sucking insects on your plants. Aphids, soft scale and mealybugs give off "
        "honeydew, a sugary waste, and ants collect it. In return the ants drive away the ladybugs, "
        "lacewings and tiny parasitic wasps that would otherwise eat those pests, so an ant-tended "
        "colony builds up much faster than one left alone. Keeping ants out of the canopy hands the "
        "plant back to its own helpers. On a tree, a sticky band around the trunk stops them "
        "climbing, and cutting back the low branches that touch the ground, a fence or a wall "
        "removes the bridges they use to get around it."
    ),
    "how_it_works_seasoned": (
        "Ant tending interrupts biological control. Honeydew from soft scales, mealybugs and aphids "
        "is a carbohydrate source ants defend, and in defending it they displace the predators and "
        "parasitoids that would otherwise regulate those populations, which is why outbreaks often "
        "track ant activity rather than the pest's own biology. Excluding ants restores that "
        "regulation rather than substituting for it, so the step belongs below any spray and below "
        "the biological rung it exists to make work. A sticky band on the trunk is the standard "
        "barrier; skirt pruning, taking off branches within roughly 12 to 30 inches of the ground, "
        "closes the routes that bypass it. On a honeydew-driven disease such as sooty mold the same "
        "move sits upstream of the fungus, which colonizes the honeydew rather than the plant."
    ),
    "best_use": (
        "Any plant where sap-sucking insects are being tended by ants, with soft scale, mealybugs "
        "and aphids on a woody plant as the standard case. Also the opening move on sooty mold, "
        "whose control begins with the honeydew-producing insect rather than with the fungus. "
        "Distinct from beneficial predators, which conserves natural enemies already present: this "
        "removes what is suppressing them, so it sits below that rung and is what lets it work. "
        "Little reason to reach for it where no ant trail is present."
    ),
    "pros": [
        "Restores the biological control already on site rather than replacing it, so it makes the "
        "predator and parasite rungs above it more effective",
        "A trunk band is cheap, long-lived through a season, and touches nothing that eats the crop",
        "Reaches a honeydew-driven disease such as sooty mold upstream, where the fungus itself has "
        "no useful target",
    ],
    "cons": [
        "Works only on a plant ants must climb to reach, so it does little on low or sprawling growth",
        "The barrier needs checking and refreshing as it collects dust and debris, and it does "
        "nothing about ants already in the canopy when it goes on",
        "Addresses the tending relationship rather than the pest directly, so a colony that built up "
        "before the band went on still takes time to come down",
    ],
    "cautions": [
        "Sticky material goes on a wrap, not on bare bark. UC IPM directs that young or sensitive "
        "trunks be collared with heavy paper, duct tape or fabric tree wrap and the sticky material "
        "applied to that collar, to avoid injuring the tree.",
        "A band holds only while the alternative routes are closed. Branches touching the ground, a "
        "wall or a neighboring plant let ants bypass the trunk entirely, which is why skirt pruning "
        "is part of the same step rather than a separate one.",
    ],
    "find_it_beginner": (
        "Sticky barrier products for tree trunks are sold at garden centers, often under the name "
        "Tanglefoot. You also want something to wrap the trunk with first, such as heavy paper or "
        "fabric tree wrap, and pruners for the low branches."
    ),
    "sources": ["ucanr_ext_ants", "uc_ipm_citrus_ants", "ucanr_ext_sooty_mold"],
    "anchoring_urls": {
        "ucanr_ext_ants": {"url": NEW_SOURCES["ucanr_ext_ants"]["url"], "verified": VERIFIED},
        "uc_ipm_citrus_ants": {"url": NEW_SOURCES["uc_ipm_citrus_ants"]["url"], "verified": VERIFIED},
        "ucanr_ext_sooty_mold": {"url": NEW_SOURCES["ucanr_ext_sooty_mold"]["url"],
                                 "verified": VERIFIED},
    },
}

SOURCE_REQUIRED = ("id", "name", "title", "publisher", "url", "source_class", "trust_tier",
                   "accessed", "tier", "citable_for")

REQUIRED_FIELDS = ("name", "tier", "applies_to", "how_it_works_beginner", "how_it_works_seasoned",
                   "best_use", "pros", "cons", "sources", "anchoring_urls")
BANNED_ABSOLUTES = ("always", "never", "completely", "harmless", "guaranteed")


def serialize(data):
    """THE serializer, shared with the guard suite."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def crop_fingerprint(data):
    """Every crop record, serialized. This promote must not move one byte of it."""
    return {c["slug"]: serialize(c) for c in data["crops"]}


def hygiene(s):
    bad = []
    if "—" in s or "–" in s:
        bad.append("em/en dash")
    if re.search(r"\d\s+°F", s):
        bad.append("spaced degF")
    for w in BANNED_ABSOLUTES:
        if re.search(r"\b%s\b" % w, s, re.I):
            bad.append("absolute:%s" % w)
    return bad


def check(data):
    cm, sc = data["control_methods"], data["source_catalog"]
    if len(cm) != EXPECT_METHODS_BEFORE:
        raise SystemExit("REFUSED: catalog has %d methods, expected %d"
                         % (len(cm), EXPECT_METHODS_BEFORE))
    if len(sc) != EXPECT_SOURCES_BEFORE:
        raise SystemExit("REFUSED: source_catalog has %d entries, expected %d"
                         % (len(sc), EXPECT_SOURCES_BEFORE))
    if METHOD_KEY in cm:
        raise SystemExit("REFUSED: %r already exists in the catalog" % METHOD_KEY)
    for sid in NEW_SOURCES:
        if sid in sc:
            raise SystemExit("REFUSED: source id %r already exists" % sid)
        for f in SOURCE_REQUIRED:
            if not (NEW_SOURCES[sid].get(f) or "").strip():
                raise SystemExit("REFUSED: new source %r missing %r. A54 requires a document-scoped "
                                 "id to carry a title READ OFF THE DOCUMENT, never inferred from "
                                 "the id, URL or pub number" % (sid, f))

    for f in REQUIRED_FIELDS:
        if f not in ANT_EXCLUSION:
            raise SystemExit("REFUSED: the minted method is missing required field %r" % f)
    if ANT_EXCLUSION["tier"] != "physical":
        raise SystemExit("REFUSED: tier is %r; every exclusion/barrier method in the catalog is "
                         "physical, and the rung must sort BELOW beneficial_predators so the "
                         "biological rung it exists to enable comes after it"
                         % ANT_EXCLUSION["tier"])
    if "disease_general" not in ANT_EXCLUSION["applies_to"]:
        raise SystemExit("REFUSED: applies_to lost `disease_general`, which is the whole reason "
                         "this mint exists -- without it sooty mold stays unladderable")
    # Every source the method cites must be one this promote actually mints or one already admitted.
    for sid in ANT_EXCLUSION["sources"]:
        if sid not in NEW_SOURCES and sid not in sc:
            raise SystemExit("REFUSED: method cites unadmitted source %r" % sid)
    # An anchoring url must be the catalog url for its own source id, never a sibling's.
    for sid, rec in ANT_EXCLUSION["anchoring_urls"].items():
        want = NEW_SOURCES[sid]["url"] if sid in NEW_SOURCES else (sc.get(sid) or {}).get("url")
        if rec["url"] != want:
            raise SystemExit("REFUSED: anchoring url for %r is %r, not its catalog url %r"
                             % (sid, rec["url"], want))
    if set(ANT_EXCLUSION["anchoring_urls"]) != set(ANT_EXCLUSION["sources"]):
        raise SystemExit("REFUSED: sources and anchoring_urls disagree")

    for f in ("how_it_works_beginner", "how_it_works_seasoned", "best_use", "find_it_beginner"):
        bad = hygiene(ANT_EXCLUSION.get(f) or "")
        if bad:
            raise SystemExit("REFUSED: %s %s" % (f, bad))
    for lst in ("pros", "cons", "cautions"):
        for item in ANT_EXCLUSION.get(lst) or []:
            bad = hygiene(item)
            if bad:
                raise SystemExit("REFUSED: %s entry %s" % (lst, bad))
    b = ANT_EXCLUSION["how_it_works_beginner"].strip()
    s = ANT_EXCLUSION["how_it_works_seasoned"].strip()
    if b == s:
        raise SystemExit("REFUSED: identical registers on how_it_works")


def apply_to(data):
    check(data)
    data["control_methods"][METHOD_KEY] = copy.deepcopy(ANT_EXCLUSION)
    for sid, rec in NEW_SOURCES.items():
        data["source_catalog"][sid] = copy.deepcopy(rec)
    return data


def verify_post(pre_crops, pre_cm, pre_sc, data):
    """This is a CATALOG revision. No crop moves, and no OTHER catalog entry moves."""
    post_crops = crop_fingerprint(data)
    if set(pre_crops) != set(post_crops):
        raise SystemExit("REFUSED: the crop roster changed")
    for slug in pre_crops:
        if pre_crops[slug] != post_crops[slug]:
            raise SystemExit("REFUSED: crop %s changed; this promote touches no crop" % slug)

    cm = data["control_methods"]
    if len(cm) != EXPECT_METHODS_BEFORE + 1:
        raise SystemExit("REFUSED: catalog is %d methods, expected %d"
                         % (len(cm), EXPECT_METHODS_BEFORE + 1))
    if set(cm) - set(pre_cm) != {METHOD_KEY}:
        raise SystemExit("REFUSED: methods added != {%r}: %r" % (METHOD_KEY, set(cm) - set(pre_cm)))
    for k in pre_cm:
        if serialize(cm[k]) != serialize(pre_cm[k]):
            raise SystemExit("REFUSED: existing method %r changed" % k)

    sc = data["source_catalog"]
    if set(sc) - set(pre_sc) != set(NEW_SOURCES):
        raise SystemExit("REFUSED: sources added != %r: %r" % (set(NEW_SOURCES),
                                                              set(sc) - set(pre_sc)))
    for k in pre_sc:
        if serialize(sc[k]) != serialize(pre_sc[k]):
            raise SystemExit("REFUSED: existing source %r changed" % k)
    # Run the REAL roster gate, not a re-implementation of its rule. The first cut of this promote
    # asserted its own idea of a well-formed source entry and shipped `name` without `title`, which
    # took gate_all to 121/121 FAILED. Calling A54's own checker closes that gap at the promote.
    from source_catalog_title_gate import title_violations
    v = title_violations(data["source_catalog"])   # takes the CATALOG dict, not `data`
    if v:
        raise SystemExit("REFUSED: A54 source_catalog title violations: %r" % (v[:3],))
    return len(cm), len(sc)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("canonical", nargs="?", default=CANONICAL)
    ap.add_argument("--canonical", dest="canonical_flag", default=None)
    ap.add_argument("--expect-sha", default=None)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    a.canonical = a.canonical_flag or a.canonical

    raw = open(a.canonical, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    expect = a.expect_sha or BASE_SHA
    if sha != expect:
        raise SystemExit("REFUSED: base SHA %s != expected %s" % (sha[:16], expect[:16]))

    data = json.loads(raw.decode("utf-8"))
    pre_crops = crop_fingerprint(data)
    pre_cm = copy.deepcopy(data["control_methods"])
    pre_sc = copy.deepcopy(data["source_catalog"])

    apply_to(data)
    n_cm, n_sc = verify_post(pre_crops, pre_cm, pre_sc, data)

    blob = serialize(data)
    new_sha = hashlib.sha256(blob).hexdigest()
    print("method minted     : %s (%s, applies_to=%s)"
          % (METHOD_KEY, ANT_EXCLUSION["tier"], ",".join(ANT_EXCLUSION["applies_to"])))
    print("catalog methods   : %d -> %d" % (EXPECT_METHODS_BEFORE, n_cm))
    print("source_catalog    : %d -> %d" % (EXPECT_SOURCES_BEFORE, n_sc))
    print("crops touched     : 0")
    print("base  SHA         : %s" % sha)
    print("post  SHA         : %s" % new_sha)
    if a.apply:
        with open(a.canonical, "wb") as fh:
            fh.write(blob)
        print("APPLIED -> %s" % a.canonical)
    else:
        print("dry run; pass --apply to write")


if __name__ == "__main__":
    main()
