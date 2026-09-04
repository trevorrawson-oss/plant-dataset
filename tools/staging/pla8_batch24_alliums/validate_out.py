#!/usr/bin/env python3
"""Per-crop self-check for a batch-24 authoring agent. Runs the SAME checks the promote runs, on
ONE crop's out_<crop>.json, against the corrected data state.

    python3 tools/staging/pla8_batch24_alliums/validate_out.py <crop> <path-to-corrected-canonical>

Exit 0 = every check passed. Any REFUSED line names what to fix. The promote will run all of
these again over all four crops; passing here is necessary, not sufficient.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(REPO, "tools"))
import promote_pla8_batch24 as P  # noqa: E402
from control_ladder_gate import TYPE_TARGETS  # noqa: E402

TEMP = re.compile(r"\d+\s*°\s*F|\d+\s*degrees", re.I)
DEVICE = re.compile(r"\bthe guidance\b|'s own sourcing|guidance (?:names|asks|points)|"
                    r"(?:onion|garlic|leek|shallot|chives|scallion)'s (?:own )?(?:guidance|sourcing)", re.I)
BRITISH = (r"\bbin\b", r"colour", r"fortnight", r"whilst", r"\bautumn\b", r"mould", r"practise",
           r"favour", r"sulphur", r"\bmesh netting\b")
# the two allium timing defects this batch was re-authored to remove
TIMING_BAD = re.compile(r"at emergence|during the (?:two )?flight|when the (?:moths|flies) are active|"
                        r"through the flight periods|during late spring and late summer", re.I)
TRAP = re.compile(r"(?:do not|don't|never) (?:use|lay|put|place) (?:a |the )?(?:row )?cover[^.]*last (?:year|season)|"
                  r"(?:bed|ground) that (?:grew|carried|held) [^.]*last (?:year|season)[^.]*(?:trap|seal)|"
                  r"(?:trap|seal)[^.]*(?:under|beneath) (?:it|the cover|the net)", re.I)


def fail(msg):
    print("REFUSED:", msg)
    fail.n += 1


fail.n = 0


def main():
    crop, path = sys.argv[1], sys.argv[2]
    data = json.load(open(path))
    by = P.by_slug(data)
    src = by[crop]
    out = json.load(open(os.path.join(HERE, "out_%s.json" % crop)))
    pins = json.load(open(os.path.join(HERE, "pinned_ids.json")))[crop]
    cm = data["control_methods"]
    schema = P.SCHEMA_FOR[crop]

    # ---- shape + ids
    for field in ("pests", "diseases"):
        s, o, pn = src.get(field) or [], out.get(field) or [], pins.get(field) or []
        if not (len(s) == len(o) == len(pn)):
            fail("%s: %d in record, %d in out, %d pinned" % (field, len(s), len(o), len(pn)))
            continue
        for i, (sp, op, pp) in enumerate(zip(s, o, pn)):
            if sp.get("name") != pp["name"]:
                fail("%s[%d] record name %r != pinned %r" % (field, i, sp.get("name"), pp["name"]))
            if op.get("id") != pp["id"] or op.get("type") != pp["type"]:
                fail("%s[%d] out id/type %r/%r != pinned %r/%r"
                     % (field, i, op.get("id"), op.get("type"), pp["id"], pp["type"]))
            if set(op) - {"id", "type", "control_ladder"}:
                fail("%s[%d] carries extra keys %r" % (field, i, sorted(set(op) - {"id", "type", "control_ladder"})))
            lad = op.get("control_ladder") or []
            if not lad:
                fail("%s/%s has an empty ladder" % (crop, op.get("id")))
            seen, last = set(), -1
            record_blob = " ".join(sp.get(f) or "" for f in schema)
            for r in lad:
                m = r.get("method")
                if m not in cm:
                    fail("%s/%s names unknown method %r" % (crop, op.get("id"), m)); continue
                if m in seen:
                    fail("%s/%s repeats %r" % (crop, op.get("id"), m))
                seen.add(m)
                tier = cm[m]["tier"]
                if P.TIERS.index(tier) < last:
                    fail("%s/%s tier decreases at %r" % (crop, op.get("id"), m))
                last = max(last, P.TIERS.index(tier))
                applies = cm[m].get("applies_to") or []
                if "any" not in applies and not (TYPE_TARGETS.get(op.get("type"), set()) & set(applies)):
                    fail("%s/%s (%s) uses %r whose applies_to %r does not reach it"
                         % (crop, op.get("id"), op.get("type"), m, applies))
                if set(r) - {"method", "note_beginner", "note_seasoned"}:
                    fail("%s/%s/%s has extra rung keys" % (crop, op.get("id"), m))
                nb, ns = r.get("note_beginner") or "", r.get("note_seasoned") or ""
                if not nb.strip() or not ns.strip():
                    fail("%s/%s/%s missing a register" % (crop, op.get("id"), m))
                if nb.strip() == ns.strip():
                    fail("%s/%s/%s registers identical" % (crop, op.get("id"), m))
                for label, note in (("note_beginner", nb), ("note_seasoned", ns)):
                    bad = P.hygiene(note)
                    for pat in BRITISH:
                        if re.search(pat, note, re.I):
                            bad.append("british:%s" % pat)
                    if P.LADDER_VOCAB.search(note):
                        bad.append("ladder vocabulary")
                    if DEVICE.search(note):
                        bad.append("false-attribution device")
                    if TIMING_BAD.search(note):
                        bad.append("the retired timing ('%s')" % TIMING_BAD.search(note).group(0))
                    if bad:
                        fail("%s/%s/%s %s: %s" % (crop, op.get("id"), m, label, ", ".join(bad)))
                    for hit in TEMP.findall(note):
                        num = re.sub(r"\D", "", hit)
                        if num not in re.sub(r"\s+", "", record_blob) and \
                                num not in re.sub(r"\s+", "", json.dumps(cm[m], ensure_ascii=False)):
                            fail("%s/%s/%s %s states %r, warranted by neither the record nor the "
                                 "method text" % (crop, op.get("id"), m, label, hit))
                    if len(note.split()) < 25:
                        fail("%s/%s/%s %s is under 25 words" % (crop, op.get("id"), m, label))
                # floating_row_cover on a soil-pupating pest must carry the trap precondition in BOTH
                # registers (the beginner register is the one a novice acts on).
                if m == "floating_row_cover" and op.get("id") in ("onion-maggot", "allium-leafminer",
                                                                   "leek-moth"):
                    for label, note in (("note_beginner", nb), ("note_seasoned", ns)):
                        if not TRAP.search(note):
                            fail("%s/%s/floating_row_cover %s lacks the row-cover trap precondition "
                                 "(do not cover a bed that grew alliums last year, or the emerging "
                                 "flies/moths are sealed in with the crop)" % (crop, op.get("id"), label))
                    if op.get("id") in ("allium-leafminer", "leek-moth") and not re.search(r"\bbefore\b", nb):
                        fail("%s/%s/floating_row_cover note_beginner must say to cover BEFORE the "
                             "flight/emergence" % (crop, op.get("id")))

    # ---- the promote's own copy and echo checks, scoped to this crop
    P.CROPS = (crop,)
    # A single-crop run must scope the declared identities too, or the identity check demands
    # onion's pin from every other crop's batch and chives/leek/shallot can never reach PASS.
    P.DECLARED_IDENTITIES = {k: v for k, v in P.DECLARED_IDENTITIES.items() if k[0] == crop}
    batch = {crop: out}
    try:
        cmp_a, cmp_b, worst = P.check_no_precedent_copy(batch, data)
        print("precedent scan   : %d + %d comparisons, worst %.3f (%s)" % (cmp_a, cmp_b, worst[0], worst[1]))
    except SystemExit as e:
        fail(str(e).replace("REFUSED: ", ""))
    try:
        P.check_no_shipped_prose_echo(batch, data)
    except SystemExit as e:
        fail(str(e).replace("REFUSED: ", ""))

    n = sum(len(p.get("control_ladder") or []) for f in ("pests", "diseases") for p in out.get(f) or [])
    print("rungs            : %d across %d problems" % (n, sum(len(out.get(f) or []) for f in ("pests", "diseases"))))
    if fail.n:
        print("RESULT: %d REFUSED" % fail.n)
        return 1
    print("RESULT: PASS (necessary, not sufficient; the promote re-runs everything over all four crops)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
