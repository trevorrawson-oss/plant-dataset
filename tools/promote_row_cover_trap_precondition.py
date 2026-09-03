#!/usr/bin/env python3
"""ROW-COVER TRAP PRECONDITION -- carry it into the register a beginner reads.

Base c24d7754.

THE DEFECT. Covering a bed that grew a susceptible crop last year does not merely fail: it SEALS
THE EMERGING FLIES IN with the crop. UMN's root-maggot page (read first-hand 2026-09-02) states it
outright -- "Do not place row covers if onions or other root vegetables were planted in the same
area the previous year" -- and that page covers both Delia antiqua and D. radicum. Follow the
uncaveated advice and you make the infestation worse.

Eleven shipped rungs recommend row cover against a soil-pupating maggot. FOUR carry the
precondition in both registers (radish, cauliflower, turnip, spring-onion). Of the rest, SEVEN omit
it from `note_beginner` -- the register a novice reads -- and TWO (broccoli, bok-choy) omit it from
both. The advice most likely to be followed uncritically is the one missing the warning.

THIS IS NOT A NEW SOURCED CLAIM, WHICH IS WHY NO SOURCE CHANGES. Every affected crop's own record
already asserts the precondition in its prevention prose ("avoid spots where you grew cabbage-family
plants last year" / "rotate away from where brassicas grew"). The row-cover rung simply failed to
carry it across, and four sibling crops already ship exactly this sentence. The promote closes an
internal inconsistency; it does not introduce a claim the records do not make.

SCOPE. NINE note strings on SEVEN crops. No source, no id, no type, no ladder membership, no
catalog, no other crop, no other field. Every pre-existing character outside those nine strings is
asserted byte-identical.

REFUSALS: base SHA mismatch; any target whose current text is not byte-identical to its pin; a
target rung that is not `floating_row_cover` on a soil-pupating maggot problem; ANY leaf changed
outside the nine; any key added or dropped anywhere; a replacement that does not extend its original
(the original must remain a prefix, so this can only ADD a clause); a replacement missing the
precondition; hygiene violations; ladder vocabulary; British usage; two replacements too similar to
each other; and -- the assertion that makes the fix complete -- ANY of the eleven row-cover rungs
still missing the precondition from EITHER register after the change.

Guard suite:      tools/test_promote_row_cover_trap_precondition.py
Mutation harness: tools/mutate_row_cover_trap_suite.py (PLA-215)
"""
import argparse, difflib, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "c24d7754e9d708b09169b5b8979f1f63bdd35b14cd77e0adf86ba03b88870c6f"

# Every shipped rung recommending row cover against a soil-pupating maggot. The four that already
# carry the precondition are listed too: they are the COVERAGE denominator, and if one of them
# loses the clause this promote must notice.
ALL_ROW_COVER_RUNGS = (
    ("radish", "cabbage-root-maggot"), ("cauliflower", "cabbage-root-maggot"),
    ("turnip", "cabbage-root-maggot"), ("spring-onion", "onion-maggot"),
    ("kale", "cabbage-root-maggot"), ("broccoli", "cabbage-root-maggot"),
    ("bok-choy", "cabbage-root-maggot"), ("cabbage", "cabbage-root-maggot"),
    ("kohlrabi", "cabbage-root-maggot"), ("brussels-sprouts", "cabbage-root-maggot"),
    ("collards", "cabbage-root-maggot"),
)
ALREADY_CORRECT = (("radish", "cabbage-root-maggot"), ("cauliflower", "cabbage-root-maggot"),
                   ("turnip", "cabbage-root-maggot"), ("spring-onion", "onion-maggot"))

# The precondition, recognised by MEANING not by a fixed phrase: the text must name BOTH the
# prior-crop condition AND the enclosure consequence. A clause naming only one of them is not the
# warning -- "rotate your beds" without "or the cover traps them" leaves the reader with no reason
# to treat the cover differently from any other bed.
_CROP_WORDS = r"(?:cabbage[- ]family|brassicas?|crucifers?|alliums?|onions?)"
_PRIOR_WORDS = r"(?:last (?:year|season)|previous|earlier|recently|grew|carried|grown|been out of)"
# BOTH ORDERS. The plural forms are explicit: an earlier version wrote `brassica\b`, which does not
# match "brassicas", and it refused a clause that stated the condition perfectly well. A guard that
# rejects correct input is as much a defect as one that accepts bad input.
PRIOR_CROP = re.compile(r"%s\b[^.]{0,90}?%s|%s[^.]{0,90}?%s\b"
                        % (_CROP_WORDS, _PRIOR_WORDS, _PRIOR_WORDS, _CROP_WORDS), re.I)
# The enclosure verbs take an object between the verb and "in" ("seal emerging flies in"), which an
# earlier version did not allow: it only matched a bare "seal in" or "seal them in", and so missed
# shipped house phrasing. Allow up to three intervening words.
ENCLOSURE = re.compile(
    r"(?:seal|shut|trap|hold|held|holds|enclos)\w*\s+(?:\w+\s+){0,3}?in\b"
    r"|\btrap(?:s|ped|ping)?\b"
    r"|caught\s+inside|enclos\w*"
    r"|(?:inside|under|beneath)\s+the\s+(?:cover|fabric|net)"
    r"|in\s+with\s+the\s+\w+", re.I)

# BEFORE text is pinned byte-for-byte. AFTER must EXTEND it -- see check_only_adds.
EDITS = {
    ("kale", "cabbage-root-maggot", "note_beginner"): (
        "A row cover, a light fabric sheet laid over the bed, keeps the fly from reaching the base "
        "of the plants to lay eggs at all.",
        "A row cover, a light fabric sheet laid over the bed, keeps the fly from reaching the base "
        "of the plants to lay eggs at all. Use it on ground that did not grow a cabbage-family "
        "crop last year, though, since flies coming up out of that soil end up shut in under the "
        "cover with the kale."),
    ("broccoli", "cabbage-root-maggot", "note_beginner"): (
        "Seal the cover at the edges right at transplanting so the low-flying fly cannot reach the "
        "stem base to lay eggs. Broccoli needs no bees, so it can stay covered.",
        "Seal the cover at the edges right at transplanting so the low-flying fly cannot reach the "
        "stem base to lay eggs. Broccoli needs no bees, so it can stay covered. Pick a bed that "
        "did not carry broccoli or its relatives last season, because a cover over old brassica "
        "ground holds the flies hatching out of it in with the crop."),
    ("broccoli", "cabbage-root-maggot", "note_seasoned"): (
        "Seal row cover at the edges from transplanting to block egg-laying at the stem base; no "
        "pollination is needed, so it stays on.",
        "Seal row cover at the edges from transplanting to block egg-laying at the stem base; no "
        "pollination is needed, so it stays on. It belongs on rotated ground: laid over a bed that "
        "carried brassicas last season, the fabric encloses the emerging adults instead of "
        "excluding them."),
    ("bok-choy", "cabbage-root-maggot", "note_beginner"): (
        "A row cover, a light fabric sheet over the bed, keeps the fly from reaching the plants to "
        "lay its eggs at their base in the first place.",
        "A row cover, a light fabric sheet over the bed, keeps the fly from reaching the plants to "
        "lay its eggs at their base in the first place. That holds only on fresh ground. Over a "
        "bed that grew cabbage-family plants last year, the flies emerging from the soil finish up "
        "inside the cover with the crop."),
    ("bok-choy", "cabbage-root-maggot", "note_seasoned"): (
        "Exclusion through cool, wet spring establishment covers the period of heaviest fly "
        "activity and protects the stage that root feeding kills, the new transplant.",
        "Exclusion through cool, wet spring establishment covers the period of heaviest fly "
        "activity and protects the stage that root feeding kills, the new transplant. Site it on "
        "ground rotated off brassicas, since a cover laid over last season's crucifer bed encloses "
        "the emerging generation rather than shutting it out."),
    ("cabbage", "cabbage-root-maggot", "note_beginner"): (
        "A row cover, a light fabric sheet laid over the bed, keeps the fly from reaching the base "
        "of the plants to lay eggs in the first place.",
        "A row cover, a light fabric sheet laid over the bed, keeps the fly from reaching the base "
        "of the plants to lay eggs in the first place. Lay it on a bed that did not grow "
        "cabbage-family crops last year. Over old brassica ground the flies come up underneath it "
        "and are held in with the plants."),
    ("kohlrabi", "cabbage-root-maggot", "note_beginner"): (
        "A row cover, a light fabric sheet laid over the bed, keeps the fly from reaching the "
        "plants to lay eggs at their base in the first place.",
        "A row cover, a light fabric sheet laid over the bed, keeps the fly from reaching the "
        "plants to lay eggs at their base in the first place. Give it fresh ground to work on: "
        "where cabbage-family crops grew last season, the cover can end up holding the emerging "
        "flies in rather than out."),
    ("brussels-sprouts", "cabbage-root-maggot", "note_beginner"): (
        "A row cover, a light fabric sheet spread over the bed, means the fly never reaches the "
        "stem bases where it would lay. It earns the most at establishment, when the soil is cool "
        "and damp and the damage is worst.",
        "A row cover, a light fabric sheet spread over the bed, means the fly never reaches the "
        "stem bases where it would lay. It earns the most at establishment, when the soil is cool "
        "and damp and the damage is worst. Choose a bed that has been out of cabbage-family crops "
        "for a season, since fabric over old brassica ground shuts the emerging flies in with the "
        "sprouts."),
    ("kohlrabi", "cabbage-root-maggot", "note_seasoned"): (
        "Exclusion through cool, wet spring establishment covers the period of heaviest adult "
        "activity and protects the stage root feeding can kill, the new transplant. Pair it with "
        "the rotation above, so the cover is not laid over ground that already carries the pest.",
        "Exclusion through cool, wet spring establishment covers the period of heaviest adult "
        "activity and protects the stage root feeding can kill, the new transplant. Pair it with "
        "the rotation above, so the cover is not laid over ground that already carries the pest. "
        "In practice that means a bed which grew cabbage-family crops last season, where the cover "
        "would hold the emerging flies in with the kohlrabi."),
    ("collards", "cabbage-root-maggot", "note_beginner"): (
        "A row cover, a light fabric sheet over the bed, keeps the fly from reaching the plants to "
        "lay eggs at their base.",
        "A row cover, a light fabric sheet over the bed, keeps the fly from reaching the plants to "
        "lay eggs at their base. Where cabbage-family crops grew last year, skip the cover: the "
        "pupae are already down in that soil, and the fabric holds the emerging flies in with the "
        "crop."),
}
EXPECTED_EDITS = 10
EXPECTED_CROPS = 7
CLAUSE_SIMILARITY_CEILING = 0.70
LADDER_VOCAB = re.compile(r"\b(?:rung|ladder|tier)s?\b", re.I)
BRITISH = (("\\bbin\\b", "bin"), ("colour", "colour"), ("fortnight", "fortnight"),
           ("whilst", "whilst"), ("mould", "mould"), ("practise", "practise"),
           ("favour", "favour"), ("sulphur", "sulphur"))


def serialize(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def by_slug(data):
    return {c["slug"]: c for c in data["crops"]}


def find_rung(data, slug, pid, method="floating_row_cover"):
    c = by_slug(data).get(slug)
    if c is None:
        raise SystemExit("REFUSED: crop %s is not on the roster" % slug)
    for fam in ("pests", "diseases"):
        for p in c.get(fam) or []:
            if p.get("id") != pid:
                continue
            for r in p.get("control_ladder") or []:
                if r.get("method") == method:
                    return r
            raise SystemExit("REFUSED: %s/%s has no %s rung" % (slug, pid, method))
    raise SystemExit("REFUSED: %s has no problem %s" % (slug, pid))


def has_precondition(text):
    return bool(PRIOR_CROP.search(text or "")) and bool(ENCLOSURE.search(text or ""))


def hygiene(s):
    bad = []
    if "—" in s or "–" in s:
        bad.append("em/en dash")
    for w in ("always", "completely", "totally", "harmless", "guaranteed", "eliminate",
              "eliminates"):
        if re.search(r"\b%s\b" % w, s, re.I):
            bad.append("absolute:%s" % w)
    for pat, label in BRITISH:
        if re.search(pat, s, re.I):
            bad.append("british:%s" % label)
    if LADDER_VOCAB.search(s):
        bad.append("ladder vocabulary")
    return bad


def snapshot(data):
    """LEAF level over the WHOLE roster plus the catalogs. set(pre) == set(post) is compared BEFORE
    any value, because iterating pre alone makes every addition invisible."""
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
    walk(data, ())
    return snap


# ------------------------------------------------------------------ guards
def check_targets(data):
    """Every target must be a row-cover rung on a soil-pupating maggot problem whose CURRENT text is
    byte-identical to its pin. A stale pin means the file moved under us."""
    if len(EDITS) != EXPECTED_EDITS:
        raise SystemExit("REFUSED: EDITS holds %d entries, expected %d" % (len(EDITS),
                                                                          EXPECTED_EDITS))
    crops = {k[0] for k in EDITS}
    if len(crops) != EXPECTED_CROPS:
        raise SystemExit("REFUSED: EDITS touches %d crops, expected %d" % (len(crops),
                                                                          EXPECTED_CROPS))
    for (slug, pid, field), (before, after) in sorted(EDITS.items()):
        if (slug, pid) not in ALL_ROW_COVER_RUNGS:
            raise SystemExit("REFUSED: %s/%s is not a known row-cover rung" % (slug, pid))
        if (slug, pid) in ALREADY_CORRECT:
            raise SystemExit("REFUSED: %s/%s already carries the precondition and must not be "
                             "edited" % (slug, pid))
        r = find_rung(data, slug, pid)
        if r.get(field) != before:
            raise SystemExit("REFUSED: %s/%s/%s current text does not match its pin; the record "
                             "moved and the replacement would be written against stale text"
                             % (slug, pid, field))


def check_only_adds(data):
    """Each replacement must EXTEND its original: the pinned BEFORE must be a prefix of the AFTER.
    This is what makes the promote incapable of rewriting shipped prose -- it can only append."""
    for (slug, pid, field), (before, after) in sorted(EDITS.items()):
        if not after.startswith(before):
            raise SystemExit("REFUSED: %s/%s/%s replacement does not extend the original; this "
                             "promote may only APPEND a clause" % (slug, pid, field))
        if len(after) <= len(before):
            raise SystemExit("REFUSED: %s/%s/%s replacement adds nothing" % (slug, pid, field))


def check_clauses(data):
    """The added clause must carry the precondition, survive hygiene, and not be a near-copy of
    another crop's clause -- nine sentences on one topic is exactly where template twins breed."""
    clauses = {}
    for (slug, pid, field), (before, after) in sorted(EDITS.items()):
        clause = after[len(before):].strip()
        if not has_precondition(clause):
            raise SystemExit("REFUSED: %s/%s/%s added clause does not state BOTH the prior-crop "
                             "condition and the enclosure consequence" % (slug, pid, field))
        bad = hygiene(clause)
        if bad:
            raise SystemExit("REFUSED: %s/%s/%s added clause: %s"
                             % (slug, pid, field, ", ".join(bad)))
        clauses[(slug, pid, field)] = clause
    keys = sorted(clauses)
    worst = (0.0, None)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            s = max(difflib.SequenceMatcher(None, clauses[a], clauses[b], autojunk=False).ratio(),
                    difflib.SequenceMatcher(None, clauses[b], clauses[a], autojunk=False).ratio())
            if s > worst[0]:
                worst = (s, "%s vs %s" % (a[0], b[0]))
            if s >= CLAUSE_SIMILARITY_CEILING:
                raise SystemExit("REFUSED: added clauses for %s and %s are %.3f similar; write "
                                 "them independently" % (a[0], b[0], s))
    if not keys:
        raise SystemExit("REFUSED: no clauses were compared; this guard is vacuous")
    return worst


def check_coverage(data):
    """THE ASSERTION THAT MAKES THE FIX COMPLETE. After the change every one of the eleven
    row-cover rungs must carry the precondition in BOTH registers. A fix that leaves one crop out
    has not closed the defect, and counting only the ones we edited would never notice."""
    # WHAT EACH REGISTER OWES IS DIFFERENT, and pretending otherwise made this guard reject
    # correct shipped prose. The BEGINNER register is where the defect lives and where a novice
    # acts without context, so it must carry BOTH halves: the prior-crop condition and the
    # enclosure consequence. The SEASONED register must at minimum name the condition; several
    # shipped ones state the instruction without spelling out the trap, and that is adequate for a
    # reader who has already been told to rotate.
    missing = []
    for slug, pid in ALL_ROW_COVER_RUNGS:
        r = find_rung(data, slug, pid)
        if not has_precondition(r.get("note_beginner") or ""):
            missing.append("%s/%s/note_beginner (needs condition AND consequence)" % (slug, pid))
        if not PRIOR_CROP.search(r.get("note_seasoned") or ""):
            missing.append("%s/%s/note_seasoned (needs the prior-crop condition)" % (slug, pid))
    if missing:
        raise SystemExit("REFUSED: %d row-cover register(s) still missing the precondition: %r"
                         % (len(missing), missing))
    return len(ALL_ROW_COVER_RUNGS)


def apply_to(data):
    check_targets(data)
    check_only_adds(data)
    check_clauses(data)
    for (slug, pid, field), (before, after) in sorted(EDITS.items()):
        find_rung(data, slug, pid)[field] = after
    return data


def verify_post(pre, data):
    post = snapshot(data)
    added, dropped = set(post) - set(pre), set(pre) - set(post)
    if dropped:
        raise SystemExit("REFUSED: leaf keys dropped: %r" % sorted(dropped)[:6])
    if added:
        raise SystemExit("REFUSED: leaf keys added: %r" % sorted(added)[:6])
    changed = sorted(k for k in pre if pre[k] != post[k])
    if len(changed) != EXPECTED_EDITS:
        raise SystemExit("REFUSED: %d leaves changed, expected %d: %r"
                         % (len(changed), EXPECTED_EDITS, changed[:12]))
    want_crops = {k[0] for k in EDITS}
    for path in changed:
        if path[0] != "crops" or path[-1] not in ("note_beginner", "note_seasoned"):
            raise SystemExit("REFUSED: changed a leaf outside a rung register: %r" % (path,))
    # COVERAGE, not a restatement, AND IT MUST COME FIRST. Two things were wrong with the earlier
    # version: it accumulated `seen` while iterating EDITS and compared it to a set derived from
    # EDITS, so it could never fail; and even reading the crop set off the diff it stayed
    # unreachable while it sat AFTER the per-edit application check, which fires first on any
    # substitution. Ordered here it catches a distinct failure the other checks cannot see: the
    # right NUMBER of registers changed, on the WRONG crops. The mutation harness found both.
    seen = {data["crops"][int(path[1][1:-1])]["slug"] for path in changed}
    if seen != want_crops:
        raise SystemExit("REFUSED: touched crops %r, expected %r" % (sorted(seen),
                                                                     sorted(want_crops)))
    for (slug, pid, field), (_before, after) in EDITS.items():
        if find_rung(data, slug, pid).get(field) != after:
            raise SystemExit("REFUSED: %s/%s/%s did not receive its replacement" % (slug, pid,
                                                                                   field))
    return len(changed)


def check_catalog_untouched(before_cm, before_sc, data):
    if serialize(data["control_methods"]) != before_cm:
        raise SystemExit("REFUSED: control_methods changed; this promote mints nothing")
    if serialize(data["source_catalog"]) != before_sc:
        raise SystemExit("REFUSED: source_catalog changed; this promote adds no source")


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
    before_cm = serialize(data["control_methods"])
    before_sc = serialize(data["source_catalog"])

    apply_to(data)
    n = verify_post(pre, data)
    check_catalog_untouched(before_cm, before_sc, data)
    covered = check_coverage(data)
    worst = check_clauses(data)

    blob = serialize(data)
    print("registers corrected : %d across %d crops" % (n, len({k[0] for k in EDITS})))
    print("coverage            : %d/%d row-cover rungs carry the precondition in both registers"
          % (covered, len(ALL_ROW_COVER_RUNGS)))
    print("clause similarity   : worst %.3f (%s), ceiling %.2f"
          % (worst[0], worst[1], CLAUSE_SIMILARITY_CEILING))
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
