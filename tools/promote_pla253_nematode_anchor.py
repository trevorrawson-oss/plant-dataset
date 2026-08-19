#!/usr/bin/env python3
"""PLA-253, third pass: beneficial_nematodes -- the safety claim gets a T1 anchor. Base 3bf8b4ce.

A DIFFERENT DEFECT FROM THE TWO Bt PASSES. Those found prose that OVERSTATED its source. This
one finds prose that is TRUE AND UNANCHORED: the entry asserted "safe for people and pets" and
"Safe for people, pets, and the crop" while its only source was UC IPM's fungus-gnat page,
which is an EFFICACY document. It says how to use nematodes against fungus gnats; it does not
adjudicate toxicology. A correct safety claim resting on a document that never made it is
still an unsourced safety claim, and it fails in a way the Bt passes could not: there is
nothing to hedge TOWARD, because no cited document has a register on the question at all.

WHAT THIS DOES
  1. mints `pnw_handbook_epn` in source_catalog (T1, document-scoped, titled at mint time
     per A54) -- the document that actually adjudicates the claim;
  2. rewrites `control_methods.beneficial_nematodes.how_it_works_beginner`;
  3. rewrites `pros[1]`;
  4. adds the new id to `sources` and `anchoring_urls`, KEEPING `ucanr_ext` for efficacy.

THE DOCUMENT, READ BEFORE IT WAS PINNED (2026-08-19, not inferred from the URL or the id):
PNW Pest Management Handbooks, "Entomopathogenic Nematodes", latest revision March 2026,
published by Oregon State University --

  "Research has demonstrated that entomopathogenic nematodes can be mass-produced, and are
   safe to plants and vertebrates; and, therefore, the U.S. Environmental Protection Agency
   has exempted them from all registration requirements and related regulation."

That single sentence carries BOTH halves of the new prose: the three protected classes
(people and pets are vertebrates; plants are named outright) and the EPA exemption. It is the
reason this document was chosen over UF/IFAS EENY-530, which was also read and which says
"they are considered nontoxic to humans" and "Entomopathogenic nematodes have been exempted
from the US Environmental Protection Agency (EPA) pesticide registration" -- true, and
sufficient for PEOPLE and the EPA claim, but SILENT on pets and plants. Anchoring the three
classes to EENY-530 would have been the arc's recurring error: the correct document supporting
only part of the claim, credited for all of it.

WHY THE UC IPM SOURCE STAYS. It is the right source for what it actually backs -- that
S. feltiae works on fungus-gnat larvae in moist media at roughly 60-90 degrees F. Dropping it
to "clean up" the source list would strip the efficacy anchor to buy a toxicology one; the
entry needs both, which is why this promote ADDS rather than replaces.

REGISTER NOTE, FLAGGED NOT SILENTLY RESOLVED. The authored beginner line says nematodes
"cannot infect" people, pets, or plants, where the document says they are "safe to plants and
vertebrates". Those are close but not identical in strength, and the two Bt passes exist
precisely because that gap matters. It is recorded here rather than edited away: the mechanism
(these nematodes require insect hosts) makes "cannot infect" the ordinary plain-English
reading of the document's claim, and the EPA's total exemption from registration is itself
predicated on it. Raised for Trevor on delivery.

Guard suite: tools/test_promote_pla253_nematode_anchor.py
Mutation harness: tools/mutate_pla253_nematode_suite.py (PLA-215, liveness-defended)

Usage: python3 tools/promote_pla253_nematode_anchor.py [--canonical PATH] [--apply] [--dry-run]
"""
import argparse
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')

BASE_SHA = '3bf8b4ce25fbeaa9f3b2cf7f5b7fe9b5c6344784204780c3f393b2bc2e0eec3e'

METHOD = 'beneficial_nematodes'
NEW_SOURCE_ID = 'pnw_handbook_epn'
KEPT_SOURCE_ID = 'ucanr_ext'
ACCESSED = '2026-08'
VERIFIED = '2026-08-19'

PREV_BEGINNER = ("These are microscopic good worms you water into the soil. They hunt and "
                 "kill soil-dwelling insect larvae, such as fungus gnat larvae, and are safe "
                 "for people and pets.")

NEW_BEGINNER = ("These are microscopic good worms you water into the soil. They hunt down "
                "and kill soil-dwelling insect larvae, such as fungus gnat larvae, and they "
                "cannot infect people, pets, or plants. The EPA considers them safe enough "
                "that they are exempt from pesticide registration entirely.")

PREV_PRO_1 = 'Safe for people, pets, and the crop'
NEW_PRO_1 = 'Cannot infect people, pets, or plants'

# Minted with the document open. `title` is read OFF the document (A54 forbids inferring one
# from the id, the URL, or a pub number). Publisher is Oregon State University alone because
# that is the only institution the page itself names -- the PNW handbooks are commonly
# described as a tri-university publication, and that claim is NOT made here because it was
# not read on the document ([[absence-findings-are-document-scoped]]).
NEW_CATALOG_ENTRY = {
    'id': NEW_SOURCE_ID,
    'name': 'PNW Pest Management Handbooks -- Entomopathogenic Nematodes',
    'title': 'Entomopathogenic Nematodes',
    'publisher': 'Oregon State University',
    'url': 'https://pnwhandbooks.org/insect/ipm/entomopathogenic-nematodes',
    'source_class': 'university_extension',
    'trust_tier': 'high',
    'accessed': ACCESSED,
    'tier': 'T1',
    'citable_for': (
        'PNW Pest Management Handbooks entry on entomopathogenic nematodes (Steinernematidae '
        'and Heterorhabditidae), latest revision March 2026. The toxicology and regulatory '
        'claim: entomopathogenic nematodes are safe to plants and vertebrates, and the US EPA '
        'has therefore exempted them from all registration requirements and related '
        'regulation. Cited for SAFETY, not efficacy.'),
    '_admission_provenance': (
        'Minted 2026-08-19 (PLA-253 third pass). The beneficial_nematodes safety claim was '
        'true but unanchored: its only source was UC IPM fungus-gnat guidance, an efficacy '
        'document that never adjudicates toxicology. Document read before pinning. UF/IFAS '
        'EENY-530 (ask.ifas.ufl.edu/publication/IN944) was also read and covers humans and '
        'the EPA exemption but is silent on pets and plants, so it does not support the '
        'three-class claim on its own.'),
}


def apply_to(data):
    """The whole transform, as one function so the guard suite exercises the same code the
    promote runs rather than a re-implementation of it."""
    catalog = data.setdefault('source_catalog', {})
    catalog[NEW_SOURCE_ID] = json.loads(json.dumps(NEW_CATALOG_ENTRY))

    entry = data['control_methods'][METHOD]
    entry['how_it_works_beginner'] = NEW_BEGINNER
    entry['pros'][1] = NEW_PRO_1
    if NEW_SOURCE_ID not in entry['sources']:
        entry['sources'].append(NEW_SOURCE_ID)
    entry['anchoring_urls'][NEW_SOURCE_ID] = {
        'url': NEW_CATALOG_ENTRY['url'],
        'verified': VERIFIED,
    }
    return data


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('canonical', nargs='?', default=CANONICAL)
    ap.add_argument('--canonical', dest='canonical_flag', default=None)
    ap.add_argument('--expect-sha', default=BASE_SHA)
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    canonical = args.canonical_flag or args.canonical

    raw = open(canonical, 'rb').read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != args.expect_sha:
        print(f'ABORT: base SHA mismatch\n  expected {args.expect_sha}\n  found    {sha}',
              file=sys.stderr)
        return 1

    data = json.loads(raw.decode('utf-8'))
    entry = data.get('control_methods', {}).get(METHOD)
    if entry is None:
        print(f'ABORT: no control_methods.{METHOD}', file=sys.stderr)
        return 1

    # Refuse to run against text this promote was not written against. An unanchored claim
    # that someone else has already edited is a different decision, not this one.
    if entry.get('how_it_works_beginner') != PREV_BEGINNER:
        print(f'ABORT: {METHOD}.how_it_works_beginner is not the text this promote was '
              f'written against\n  found: {entry.get("how_it_works_beginner")!r}', file=sys.stderr)
        return 1
    pros = entry.get('pros') or []
    if len(pros) != 2 or pros[1] != PREV_PRO_1:
        print(f'ABORT: {METHOD}.pros is not the 2-item list this promote was written against\n'
              f'  found: {pros!r}', file=sys.stderr)
        return 1
    if NEW_SOURCE_ID in (data.get('source_catalog') or {}):
        print(f'ABORT: source_catalog already carries {NEW_SOURCE_ID}; minting twice would '
              f'overwrite an entry someone else authored', file=sys.stderr)
        return 1
    if entry.get('sources') != [KEPT_SOURCE_ID]:
        print(f'ABORT: {METHOD}.sources is not [{KEPT_SOURCE_ID!r}]\n  found: '
              f'{entry.get("sources")!r}', file=sys.stderr)
        return 1

    apply_to(data)

    print(f'minted source_catalog.{NEW_SOURCE_ID} (T1, titled at mint time)')
    print(f'rewrote control_methods.{METHOD}.how_it_works_beginner')
    print(f'rewrote control_methods.{METHOD}.pros[1]')
    print(f'  "{PREV_PRO_1}" -> "{NEW_PRO_1}"')
    print(f'sources: [{KEPT_SOURCE_ID!r}] -> {data["control_methods"][METHOD]["sources"]!r} '
          f'({KEPT_SOURCE_ID} KEPT for efficacy)')

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    new_sha = hashlib.sha256(out).hexdigest()
    if args.dry_run:
        print(f'DRY RUN -- would write {len(out)} bytes, sha {new_sha}')
        return 0
    with open(canonical, 'wb') as fh:
        fh.write(out)
    print(f'wrote {len(out)} bytes\nnew canonical SHA: {new_sha}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
