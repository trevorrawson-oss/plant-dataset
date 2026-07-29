#!/usr/bin/env python3
"""Label asparagus finding 10's anchor adjudication as EDITORIAL, and bound it.

WHY THIS EXISTS: the disposition this session appended to finding 10 ended "The ruling stands
on the camp count plus the two real tie-breakers above" -- asserting a ruling WITHOUT recording
that no source arbitrates the dispute. That is the same defect the very same disposition
RETRACTS one sentence earlier (an invented UMaine rationale reading as sourced). Stating a
conclusion more confidently than its evidence supports is the failure class this whole pass is
about, so it gets fixed rather than described.

It also records the CONTAINMENT, which is the load-bearing part: the adjudication is
EXPLANATORY, not GENERATIVE. No shipped value depends on it. Each of the five rungs sits inside
an independently verified in-state quote, and a frost-offset derivation (the only thing the
anchor choice could generate) was TESTED AND REJECTED because the offset drifts 19 days.

Guards: canonical SHA; expected tail verbatim; not already labelled. Append-only.
Writes COMPACT per CLAUDE.md.
"""
import copy
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')

EXPECT_SHA = '7bc4b954377562218d775d676cf6fd5699547f56e8d3606f9559db6df73d9855'
TAIL = 'The ruling stands on the camp count plus the two real tie-breakers above.'

ADDENDUM = (
    ' LABELLED 2026-07-29, and this label is the point: **NO SOURCE ARBITRATES THIS DISPUTE.** Not '
    'one of the documents read acknowledges a competing recommendation, so the adjudication above '
    'is EDITORIAL -- assembled from a camp count and two tie-breaker quotes by this lane, not '
    'stated by any extension service. It is recorded as a ruling, not as a sourced fact, and the '
    'sentence before this one asserted it without that caveat, which is the identical '
    'over-confidence this same disposition retracts in the UMaine rationale two sentences earlier. '
    'CONTAINMENT, which bounds what the editorial call can damage: it is EXPLANATORY, not '
    'GENERATIVE, and NO SHIPPED VALUE DEPENDS ON IT. The five northern_tier windows are '
    'state_source_zone_mapped from in-state quotes, each independently verified (z3 May 1 - Jun 5 '
    'against UMN\'s "In Minnesota, asparagus is planted between early May and early June", '
    're-fetched and confirmed at 74 asparagus mentions on 2026-07-29), and the ONE thing the anchor '
    'choice could actually generate -- a frost-offset derivation -- was tested and REJECTED because '
    'the implied offset drifts 19 days across the ladder. So if a later pass overturns this ruling, '
    'it changes the RATIONALE and not a single date. Overturn it freely on better evidence.'
)


def die(m):
    print(f'ABORT: {m}', file=sys.stderr)
    sys.exit(1)


def main():
    dry = '--dry-run' in sys.argv
    raw = open(CANONICAL, 'rb').read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != EXPECT_SHA:
        die(f'canonical SHA drift: {sha}')
    print(f'canonical verified {sha[:8]}')

    data = json.loads(raw.decode('utf-8'))
    before = copy.deepcopy(data)
    crop = [c for c in data['crops'] if c['slug'] == 'asparagus'][0]
    f = crop['verification_status']['open_findings'][10]
    if f.get('id') != 'asparagus_plant_out_anchor_families_conflict':
        die(f'finding[10] is {f.get("id")!r}, not the anchor-families finding')
    text = f['summary']
    if 'LABELLED 2026-07-29' in text:
        die('already labelled')
    if not text.endswith(TAIL):
        die(f'tail mismatch: ...{text[-90:]!r}')
    f['summary'] = text + ADDENDUM
    if not f['summary'].startswith(text):
        die('append-only violated')
    print(f'finding[10]: +{len(ADDENDUM)} chars appended')

    b = {c['slug']: c for c in before['crops']}
    n = {c['slug']: c for c in data['crops']}
    diff = [s for s in b if b[s] != n[s]]
    if diff != ['asparagus']:
        die(f'footprint: {diff}')
    for k in before:
        if k != 'crops' and before[k] != data[k]:
            die(f'top-level {k!r} changed')
    print('footprint: asparagus only')

    out = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
    if out.endswith('\n'):
        die('trailing newline')
    new_sha = hashlib.sha256(out.encode('utf-8')).hexdigest()
    if dry:
        print(f'\nDRY RUN. Would become {new_sha}')
        return 0
    open(CANONICAL, 'w', encoding='utf-8').write(out)
    print(f'\nwritten. {EXPECT_SHA[:8]} -> {new_sha[:8]}')
    print(f'FULL: {new_sha}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
