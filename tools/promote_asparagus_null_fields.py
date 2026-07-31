#!/usr/bin/env python3
"""GUARDED PROMOTE: asparagus's five missing top-level fields, backfilled as null.

Trevor-ruled 2026-07-31 (the "unblocked and cheap" cleanup batch).

THE RECORD WAS WRONG. Kickoff 48 §4 calls asparagus's 7 missing top-level fields "a
perennial-schema question, not an omission to backfill". Measured: 56 top-level keys appear on
>=90% of the 128 crops; asparagus lacks exactly 7, is the SOLE crop missing each, and
**artichoke -- the only other herbaceous_perennial -- lacks none of the 56**. So the archetype
is not the explanation. Nothing caught it because `whole_crop_gate` passes on asparagus and does
not reference any of the seven (the `optional-field-gates-go-vacuous` class).

THE FIVE HANDLED HERE all take `null`, and each rests on a measured convention:
  days_to_maturity_mid        36 of the 37 crops with `days_to_maturity == []` carry null and
                              ZERO carry a value; asparagus is the 37th.
  weeks_indoors               `propagule == "crown"` -- there is no indoor start to describe,
                              and the only other crown crop carries null.
  first_planting_notify_days  52 crops carry null, artichoke among them.
  last_reviewed               22 carry null, artichoke among them.
  last_reviewed_session       22 carry null, artichoke among them.

`null` IS THE HONEST VALUE, not a shape being filled. Asparagus does carry
`verification_status.last_audited` and per-tip `last_reviewed` stamps, so the review fact exists
somewhere -- but writing a DATE into the top-level field would assert a review that was never
performed at that level. That is exactly the lettuce-leaf `verified` defect, one field over.

DELIBERATELY OUT OF SCOPE (separate rulings, separate promotes):
  yield_expectations  present AND NON-NULL on all 127 other crops (zero nulls roster-wide).
                      A null would assert "no yield data exists" when the truth is "nobody
                      authored it". It needs real dual-register authoring with T1 sources.
  zones               the one genuine schema question. plant-astro's today.ts,
                      [crop]/[zone].astro and TreeGuide.astro read zones{} and FAIL OPEN, so the
                      consumer behaviour must be checked before choosing placeholder-vs-absent.

    $ python3 tools/promote_asparagus_null_fields.py --dry-run
    $ python3 tools/promote_asparagus_null_fields.py --apply
"""
import argparse
import copy
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')
BASE_SHA = 'e353fadb83277605192d55fa4312854bf648a835c41666130d41905fc04cc9d2'

SLUG = 'asparagus'
NULL_FIELDS = ('days_to_maturity_mid', 'first_planting_notify_days',
               'last_reviewed', 'last_reviewed_session', 'weeks_indoors')
OUT_OF_SCOPE = ('yield_expectations', 'zones')


def _fail(msg):
    print('ABORT: %s' % msg)
    return 2


def backfill(data):
    """Add each NULL_FIELDS key with value None. Returns `data`."""
    for crop in data['crops']:
        if crop.get('slug') != SLUG:
            continue
        for f in NULL_FIELDS:
            crop[f] = None
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--canonical', default=CANON)
    ap.add_argument('--expect-sha', default=BASE_SHA)
    args = ap.parse_args()
    if not (args.apply or args.dry_run):
        ap.error('pass --dry-run or --apply')

    with open(args.canonical, 'rb') as fh:
        raw = fh.read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != args.expect_sha:
        return _fail('canonical drifted.\n  expected %s\n  found    %s' % (args.expect_sha, sha))
    print('pre-state SHA verified: %s' % sha[:16])

    data = json.loads(raw)
    before = copy.deepcopy(data)
    asp = next((c for c in data['crops'] if c.get('slug') == SLUG), None)
    if asp is None:
        return _fail('%s not found' % SLUG)

    # ---- preflight: every premise this backfill rests on ---------------------
    present = [f for f in NULL_FIELDS if f in asp]
    if present:
        return _fail('%s already carries %s -- the measured footprint no longer holds'
                     % (SLUG, present))
    if asp.get('days_to_maturity') != []:
        return _fail('days_to_maturity is %r, not [] -- a null days_to_maturity_mid is only '
                     'correct for an empty-DTM crop' % (asp.get('days_to_maturity'),))
    if asp.get('propagule') != 'crown':
        return _fail('propagule is %r, not "crown" -- a null weeks_indoors rests on there being '
                     'no indoor start' % (asp.get('propagule'),))
    # the conventions, re-measured against this very file rather than quoted
    empty_dtm = [c for c in data['crops'] if c.get('days_to_maturity') == []]
    mid_set = [c['slug'] for c in empty_dtm if c.get('days_to_maturity_mid') is not None]
    if mid_set:
        return _fail('empty-DTM crops carrying a non-null days_to_maturity_mid: %s -- the '
                     'convention this pass relies on is not what the data says' % mid_set)
    art = next((c for c in data['crops'] if c.get('slug') == 'artichoke'), None)
    if art is None or any(f not in art for f in NULL_FIELDS):
        return _fail('artichoke (the comparison herbaceous perennial) does not carry all five')
    print('verified: %s missing all 5; days_to_maturity==[] over %d crops with 0 exceptions; '
          'propagule=crown; artichoke carries all 5' % (SLUG, len(empty_dtm)))

    # ---- apply ---------------------------------------------------------------
    backfill(data)

    # ---- every added key is present AND null ---------------------------------
    for f in NULL_FIELDS:
        if f not in asp:
            return _fail('%s was not added' % f)
        if asp[f] is not None:
            return _fail('%s was written as %r; these fields must be null, never a '
                         'plausible-looking value' % (f, asp[f]))
    for f in OUT_OF_SCOPE:
        if f in asp:
            return _fail('%s was added but is a SEPARATE ruling' % f)

    # ---- footprint: asparagus only, additive only ----------------------------
    b = {c['slug']: c for c in before['crops']}
    a = {c['slug']: c for c in data['crops']}
    changed = sorted(s for s in b if b[s] != a[s])
    if changed != [SLUG]:
        return _fail('crops changed = %s, expected [%s]' % (changed, SLUG))
    b_asp = b[SLUG]
    if set(b_asp) | set(NULL_FIELDS) != set(asp):
        return _fail('asparagus key set changed beyond the 5 additions')
    for k in b_asp:
        if b_asp[k] != asp[k]:
            return _fail('existing asparagus.%s moved' % k)
    for k in before:
        if k != 'crops' and before[k] != data[k]:
            return _fail('top-level %s changed' % k)
    missing_after = 7 - len(NULL_FIELDS)
    print('verified: footprint is asparagus only; 5 keys added as null; every existing value '
          'frozen; %d of the 7 deliberately still open (%s)'
          % (missing_after, ', '.join(OUT_OF_SCOPE)))

    if args.dry_run:
        print('\nDRY RUN -- nothing written.')
        return 0

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if out.endswith(b'\n'):
        return _fail('trailing newline introduced')
    with open(args.canonical, 'wb') as fh:
        fh.write(out)
    print('\nAPPLIED: %d null fields backfilled on %s' % (len(NULL_FIELDS), SLUG))
    print('  new canonical SHA: %s' % hashlib.sha256(out).hexdigest())
    return 0


if __name__ == '__main__':
    sys.exit(main())
