#!/usr/bin/env python3
"""Tests for doc_mentions_crop_scan's matching logic.

`bare_host_scan` and `citation_provenance_scan` ship untested because their logic is a URL
regex. This scan is different: its verdict rests on "does this document mention this crop",
and that matching produced TWO silent false-negatives during development, both of which would
have HIDDEN a real defect rather than raising a false one:

  1. substring "fig" matches "Figure 1"     -> every document with figure captions cleared fig
  2. term "green" from slug green-beans-bush -> cleared essentially every document

A false CLEAR is the dangerous direction here, so those two cases are pinned below and must
stay pinned.

    $ python3 -m pytest tools/test_doc_mentions_crop_scan.py -q
    $ python3 tools/test_doc_mentions_crop_scan.py
"""
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))

import doc_mentions_crop_scan as M  # noqa: E402

CANON = os.path.join(REPO, 'crops_data_final.json')


def _crops():
    with open(CANON) as fh:
        return {c['slug']: c for c in json.load(fh)['crops']}


def test_matching():
    if not os.path.exists(CANON):
        print('SKIP: canonical missing')
        return
    crops = _crops()
    results = []

    def check(name, ok, detail=''):
        results.append((name, ok))
        print(('  PASS  ' if ok else '  FAIL  ') + name + (('  -- ' + detail) if detail else ''))

    def hit(slug, text):
        m = M.crop_matcher(crops[slug])
        return bool(m and m.search(text.lower()))

    # --- the two silent false-negatives that motivated the tests ---
    check('fig NOT matched by "Figure 1"', not hit('fig', 'See Figure 1 and Figure 12 below.'))
    check('fig matched by a real fig sentence',
          hit('fig', 'Fig trees should not be planted until early spring.'))
    check('fig matched in plural', hit('fig', 'recommended crops: apples, chestnuts, figs, pears'))
    check('green-beans-bush NOT cleared by the bare word "green"',
          not hit('green-beans-bush', 'Use a green manure cover crop and green mulch.'))
    check('green-beans-bush matched by "green beans"',
          hit('green-beans-bush', 'Plant green beans after the last frost.'))
    check('green-beans-bush matched by "bean"', hit('green-beans-bush', 'Snap bean planting dates'))

    # --- other collision families ---
    check('snow-peas NOT matched by "peach"', not hit('snow-peas', 'Peach and peanut orchards'))
    check('snow-peas matched by "peas"', hit('snow-peas', 'Sow peas in early March.'))
    check('bee-balm NOT matched by "been"/"beetle"',
          not hit('bee-balm', 'The beetle has been observed feeding on beef.'))

    # --- the vce_426_331 case this scan was built for ---
    veg = 'virginia home garden vegetable planting guide beans lettuce tomato spinach radish'
    for slug in ('cherry-sour', 'apple', 'peach', 'pear-european', 'persimmon', 'mulberry'):
        check('%s NOT cleared by a vegetable-only guide' % slug, not hit(slug, veg))
    check('green-beans-bush IS cleared by that same guide (beans really are in it)',
          hit('green-beans-bush', veg))

    # --- leniency: a general term should clear a specific crop ---
    check('cherry-sour cleared by "cherries"',
          hit('cherry-sour', 'apricot and cherry trees will not consistently bear fruit'))
    check('pear-asian cleared by "pears"', hit('pear-asian', 'apples and pears are more forgiving'))
    check('acorn-squash cleared by "winter squash"',
          hit('acorn-squash', 'winter squash May - July'))

    # --- structural guarantees the report relies on ---
    empty = sorted(s for s, c in crops.items() if not M.crop_terms(c))
    check('every crop yields at least one match term', not empty, str(empty[:5]))
    leak = [(s, t) for s, c in crops.items() for t in M.crop_terms(c) if t in M.STOPWORDS]
    check('no stopword leaks into a term set', not leak, str(leak[:5]))
    stale = sorted(set(M.SYNONYMS) - set(crops))
    check('no SYNONYMS entry references a crop off the roster', not stale, str(stale))

    failed = [r for r in results if not r[1]]
    print('\n%d/%d checks passed' % (len(results) - len(failed), len(results)))
    assert not failed, 'failed: %s' % [r[0] for r in failed]


if __name__ == '__main__':
    test_matching()
