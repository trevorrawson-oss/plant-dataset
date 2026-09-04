#!/usr/bin/env python3
"""promote_pla8_batch25_catalog -- admit `uc_ipm_pn7493` to source_catalog. ONE entry, nothing else.

WHY THIS IS ITS OWN PROMOTE. `source_catalog` is a TOP-LEVEL key, and
`promote_pla8_batch25.verify_post` refuses any top-level change by design, so the batch cannot carry
this. It lands first, exactly as the catalog r-rounds do, and batch 25 then rebases onto its SHA.

WHY THE ENTRY IS NEEDED. `anchoring_urls` holds ONE url per source key (measured: all 1400 values in
canonical are dicts keyed by catalog id), so a claim that lives only in a second UC IPM document
cannot be cited under the key already pointing at the first. Four crops in this batch carry powdery
mildew, and 7493 carries two things 7406 does not:

  * the suppression figure -- 7493: "Temperatures above 95°F may suppress growth of the fungus";
    7406 gives a different one, "sensitive to extreme heat (above 90°F)";
  * a host list that NAMES SALVIA, where 7406's host list is 18 vegetables and no herb. That is the
    strongest available anchor for "sage gets powdery mildew" rather than "vegetables do".

RETRACTED BEFORE THIS EVER COMMITTED, and recorded because the retraction is the useful part. The
first draft of this promote rested mainly on a THIRD claim: that only 7493 carried the
dormant-season sanitation step, "Prune out small infestations and remove infected buds during the
dormant season", and that without it a powdery-mildew ladder had nothing acting on an infection
already present. **7406 carries that sentence verbatim.** A reviewer found it on two independent
fetches and a third confirmed it here. So the strongest-sounding argument for the admission was an
UNCHECKED ABSENCE, asserted by me, in the very field whose job is to scope what a key may be cited
for -- the same defect class this batch is correcting on three other crops. The admission still
stands on the two claims above, which were checked. The ladder gap it was meant to close is also
narrower than claimed: `garden_sanitation` removes infected tissue and `biofungicide` reaches first
spots, and what remains unreachable is specifically an ESTABLISHED infection, for which UC IPM
publishes oils and `horticultural_oil` cannot reach `fungal`.

SCOPE, DELIBERATELY NARROW. 7493 is the ORNAMENTALS note; 7406 (vegetables) remains the correctly
scoped document for a culinary herb's powdery mildew in general, and nothing about harvest,
edibility or preharvest intervals should ever be sourced from an ornamentals note.

Usage:
    promote_pla8_batch25_catalog.py [--check]
"""
import argparse, copy, hashlib, json, os, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, "crops_data_final.json")

BASE_SHA = "a9c84847fe2e0ad595db8cf9cc7d7e82ac65803e3284e16071be6d536bf9dad7"
# KEY: the five sibling UC IPM Pest Note entries use `ucanr_ext_<topic>`. This one keys on the
# publication number instead, deliberately: a pub number is stable where a topic name drifts, and
# the entry is scoped to claims that belong to THIS publication rather than to a topic. Recorded so
# the divergence reads as a choice.
KEY = "uc_ipm_pn7493"
ENTRY = {
    "id": KEY,
    "name": "UC IPM Pest Notes -- Powdery Mildew on Ornamentals",
    # A54 REQUIRES A TITLE ON A DOCUMENT-SCOPED ID, "read it off the document itself, never from the
    # id/URL/pub number" (PLA-199). The first version of this entry carried only `name` and
    # `gate_all` went 0 of 121 -- every certified crop failed A54 on this ONE catalog entry, which is
    # what a roster-wide source-catalog check looks like when it fires. Title read off the page,
    # whose leading heading matches the five sibling Pest Note entries verbatim in form.
    "title": "Powdery Mildew on Ornamentals / Home and Landscape / UC Statewide IPM Program (UC IPM)",
    "publisher": "UC Statewide IPM Program (UC ANR)",
    "url": "https://ipm.ucanr.edu/PMG/PESTNOTES/pn7493.html",
    "source_class": "university_extension",
    "trust_tier": "high",
    "accessed": "2026-09",
    "tier": "T1",
    "citable_for": (
        "UC ANR Publication 7493, Pest Notes: Powdery Mildew on Ornamentals. Admitted for two "
        "claims this document carries and Pest Note 7406 (Powdery Mildew on Vegetables) does not: "
        "the suppression figure (\"Temperatures above 95°F may suppress growth of the fungus\", "
        "where 7406 gives a different figure, \"sensitive to extreme heat (above 90°F)\"), and a "
        "host list that names salvia, which 7406's vegetable host list does not. NOT a general "
        "re-anchor of herb powdery mildew away from 7406, which remains the correctly scoped "
        "document for culinary crops. CORRECTED BEFORE FIRST COMMIT: an earlier draft of this "
        "field also claimed the dormant-season sanitation step (\"Prune out small infestations and "
        "remove infected buds during the dormant season\") was unique to 7493. It is not; 7406 "
        "carries that sentence verbatim, verified on three independent fetches. A citable_for whose "
        "job is to scope a key must not itself assert an unchecked absence."
    ),
}


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    raw = open(CANON, "rb").read()
    got = sha256_bytes(raw)
    if got != BASE_SHA:
        sys.exit(f"REFUSED: base SHA mismatch.\n  expected {BASE_SHA}\n  got      {got}")
    data = json.loads(raw.decode("utf-8"))

    if KEY in data["source_catalog"]:
        sys.exit(f"REFUSED: {KEY} already present")

    post = copy.deepcopy(data)
    post["source_catalog"][KEY] = copy.deepcopy(ENTRY)

    # VERIFY: exactly one key added to exactly one top-level dict, nothing else touched anywhere.
    if set(post) != set(data):
        sys.exit("REFUSED: top-level key set changed")
    for k in data:
        if k == "source_catalog":
            continue
        if json.dumps(post[k], sort_keys=True) != json.dumps(data[k], sort_keys=True):
            sys.exit(f"REFUSED: top-level key {k!r} changed")
    added = set(post["source_catalog"]) - set(data["source_catalog"])
    removed = set(data["source_catalog"]) - set(post["source_catalog"])
    if added != {KEY} or removed:
        sys.exit(f"REFUSED: catalog delta is added={sorted(added)} removed={sorted(removed)}")
    for k in data["source_catalog"]:
        if json.dumps(post["source_catalog"][k], sort_keys=True) != \
           json.dumps(data["source_catalog"][k], sort_keys=True):
            sys.exit(f"REFUSED: existing catalog entry {k!r} changed")

    blob = json.dumps(post, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    new_sha = sha256_bytes(blob)
    print(f"  catalog {len(data['source_catalog'])} -> {len(post['source_catalog'])} entries "
          f"(+{KEY})")
    print(f"  base {BASE_SHA}\n  post {new_sha}")
    if args.check:
        print("\n--check: nothing written.")
        return 0
    with open(CANON, "wb") as f:
        f.write(blob)
    print(f"\nWROTE {CANON}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
