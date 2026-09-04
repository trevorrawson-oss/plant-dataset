#!/usr/bin/env python3
"""promote_rosemary_certlog_correction -- append a [CORRECTION] to rosemary's verification_log_ref.

WHAT IS NO LONGER TRUE. The 2026-07-06 cert log records rosemary's root and crown rot as
"correctly Phytophthora-only (UC IPM, Pythium already dropped)". The PNW Plant Disease Handbook's
rosemary root-rot page, which 403s to every direct fetch path this project has, was finally
retrieved during PLA-8 batch 25 and its Cause section reads:

    "Several root rotting organisms have been detected in rosemary root rot samples coming to the
     OSU Plant Clinic. Pythium, Berkeleyomyces sp. (formerly Thielaviopsis basicola), and
     Rhizoctonia are among the organisms found."

No Phytophthora. So "Phytophthora-only" is not supported, and Pythium was dropped on a reading that
the document does not carry.

WHY THIS IS AN APPEND AND NEVER AN EDIT. `verification_status.verification_log_ref` is an
APPEND-ONLY, CERT-DATED HISTORICAL RECORD. It records what was believed at the arc it names, and
"fixing" a stale one into current tense destroys the only evidence of what a pass actually
concluded. `docs/verification_log_ref_convention.md` fixes the form:

    [CORRECTION <YYYY-MM-DD>: <what is no longer true, and what is true now> -- see <finding>.]

appended at the END, with the original prose byte-for-byte intact. This promote enforces exactly
that: the pre-state must survive as an exact PREFIX of the post-state.

THE CAVEAT IS PART OF THE CORRECTION, not a footnote to it. The PNW page was retrieved through a
text proxy and corroborated by an independent search snippet. That is two consistent retrievals and
NOT a first-party read. It is strong enough to retract an over-claim -- a move toward saying LESS --
and it is NOT strong enough to assert Pythium, Berkeleyomyces or Rhizoctonia as rosemary's
pathogens in consumer copy. Nothing in the dataset does, and the correction text says so, because a
correction that licenses a new over-claim while retiring an old one has not helped.

Usage:
    promote_rosemary_certlog_correction.py [--check]
"""
import argparse, copy, hashlib, json, os, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, "crops_data_final.json")

BASE_SHA = "132980d52dd2f4c7850729401fdcfde8b5485ab0eb03f734e9acf949755d27b4"
SLUG = "rosemary"
FIELD = "verification_log_ref"

# The claim being corrected must be PRESENT in the pre-state, or this promote is correcting nothing.
STALE_CLAIM = "root/crown rot correctly Phytophthora-only (UC IPM, Pythium already dropped)"

CORRECTION = (
    " [CORRECTION 2026-09-04: \"root/crown rot correctly Phytophthora-only\" is no longer supported. "
    "The PNW Plant Disease Handbook's rosemary root-rot page, unreadable at the time of the "
    "2026-07-06 cert and retrieved during PLA-8 batch 25, names Pythium, Berkeleyomyces sp. "
    "(formerly Thielaviopsis basicola) and Rhizoctonia and no Phytophthora, so Pythium was dropped "
    "on a reading that document does not carry. The taxon is treated as UNRESOLVED: rosemary's rot "
    "is pinned to the problem-class umbrella `crown-and-root-rot` and its consumer prose names no "
    "genus. CAVEAT, and it bounds this correction: that page was reached through a text proxy plus "
    "a corroborating search snippet, which is two consistent retrievals and NOT a first-party read. "
    "Enough to retract an over-claim; NOT enough to assert those three genera, and nothing does. "
    "-- see docs/2026-09-04-pla8-batch25-herbs-handoff.md §7.]"
)


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def serialize(data):
    """CANONICAL IS COMPACT. Extracted from main() so a driver can REACH it: the write format was
    inlined, and a mutation switching it to indent=2 survived the whole suite because every test
    read the file from disk and none called main(). Reaching the entry point is the fix."""
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def by_slug(data):
    return {c["slug"]: c for c in data["crops"]}


def check_pre(data):
    v = (by_slug(data)[SLUG].get("verification_status") or {}).get(FIELD)
    if not isinstance(v, str) or not v.strip():
        raise SystemExit(f"REFUSED: {SLUG}.{FIELD} is not a non-empty string")
    if STALE_CLAIM not in v:
        raise SystemExit(f"REFUSED: the claim being corrected is ABSENT from the pre-state, so this "
                         f"promote would append a correction to nothing: {STALE_CLAIM!r}")
    if "[CORRECTION" in v:
        raise SystemExit("REFUSED: a correction is already present; corrections accumulate in date "
                         "order and this promote is not idempotent by design, so re-running it "
                         "would double-append")
    return v


def apply_to(data):
    out = copy.deepcopy(data)
    vs = by_slug(out)[SLUG]["verification_status"]
    vs[FIELD] = vs[FIELD] + CORRECTION
    return out


def verify_post(pre, post):
    """The original prose must survive as an exact PREFIX, and exactly one leaf may move."""
    pre_i, post_i = by_slug(pre), by_slug(post)
    if set(pre_i) != set(post_i):
        raise SystemExit("REFUSED: crop roster changed")
    for k in pre:
        if k == "crops":
            continue
        if json.dumps(pre[k], sort_keys=True) != json.dumps(post[k], sort_keys=True):
            raise SystemExit(f"REFUSED: top-level key {k!r} changed")
    for slug in pre_i:
        a, b = pre_i[slug], post_i[slug]
        if slug != SLUG:
            if json.dumps(a, sort_keys=True) != json.dumps(b, sort_keys=True):
                raise SystemExit(f"REFUSED: untouched crop {slug} changed")
            continue
        # SET COMPARISON BEFORE VALUE COMPARISON: iterating one side hides the other's additions.
        if set(a) != set(b):
            raise SystemExit(f"REFUSED: {slug} key set changed")
        moved = [k for k in a if json.dumps(a[k], sort_keys=True) != json.dumps(b[k], sort_keys=True)]
        if moved != ["verification_status"]:
            raise SystemExit(f"REFUSED: expected only verification_status to move, got {moved}")
        va, vb = a["verification_status"], b["verification_status"]
        if set(va) != set(vb):
            raise SystemExit("REFUSED: verification_status key set changed")
        vmoved = [k for k in va if va[k] != vb[k]]
        if vmoved != [FIELD]:
            raise SystemExit(f"REFUSED: expected only {FIELD} to move, got {vmoved}")
        if not vb[FIELD].startswith(va[FIELD]):
            raise SystemExit("REFUSED: the original prose is not an exact PREFIX of the result; "
                             "this field is append-only and the original must survive byte-for-byte")
        if vb[FIELD] != va[FIELD] + CORRECTION:
            raise SystemExit("REFUSED: the appended text is not exactly the declared correction")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    raw = open(CANON, "rb").read()
    got = sha256_bytes(raw)
    if got != BASE_SHA:
        sys.exit(f"REFUSED: base SHA mismatch.\n  expected {BASE_SHA}\n  got      {got}")
    data = json.loads(raw.decode("utf-8"))

    pre_text = check_pre(data)
    post = apply_to(data)
    verify_post(data, post)
    print(f"  pre-state claim present : {STALE_CLAIM[:60]}...")
    print(f"  {FIELD} {len(pre_text)} -> {len(pre_text) + len(CORRECTION)} chars, original intact as prefix")

    blob = serialize(post)
    print(f"  base {BASE_SHA}\n  post {sha256_bytes(blob)}")
    if args.check:
        print("\n--check: nothing written.")
        return 0
    with open(CANON, "wb") as f:
        f.write(blob)
    print(f"\nWROTE {CANON}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
