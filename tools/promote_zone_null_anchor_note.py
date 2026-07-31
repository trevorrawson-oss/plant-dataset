#!/usr/bin/env python3
"""GUARDED PROMOTE: the 57 legacy zone-layer null anchors say "to-do" when they mean "decided".

Trevor-ruled 2026-07-31.

THE PROBLEM IS THE WORDING, NOT THE DATA. 57 anchor entries in the legacy `zones{}` subtree carry
`url: null` plus a note reading "URL not in retro log, needs manual lookup". That reads as an
outstanding task, so every audit re-files it -- Trevor's external blind audit ranked it priority
two, and it had already been deferred on 2026-07-06.

WHY THEY ARE NOT BEING RESOLVED OR DELETED, both of which were considered and rejected:

  * DELETING the anchor orphans the source id. In ALL 54 affected nodes the id is also listed in
    that node's `sources`, so removing the anchor converts 57 nulls into 57 source/anchor
    mismatches -- trading one audit finding for another.
  * BACKFILLING from the same id elsewhere in the file would cite the WRONG DOCUMENT. Seven ids
    cover all 57, and elsewhere they point at a cut-flowers high tunnel page (`cornell_ext`), a
    tomatillo page (`sdsu_ext`), the elderberry publication (`mu_ext`), a bare host (`uc_mg`), and
    for 18 of the 57, `uga_b577` -- the known-dead url that serves an institutional logo PDF.
  * RE-SOURCING them is honest but buys little: nothing renders anchor data out of `zoneData`, and
    the `regions` layer is authoritative for these claims and carries its own sources.

So the note is rewritten to state the decision instead of implying a debt. The data is unchanged.

NOTE ON SCOPE: this touches ONLY the `note` string on entries whose `url` is already null. No url,
no source id, no value, and not the `zones{}` subtree itself -- which is LIVE and read by
plant-astro, contrary to the 2026-07-06 shorthand (see the correction in CURRENT_STATE.md).

    $ python3 tools/promote_zone_null_anchor_note.py --dry-run
    $ python3 tools/promote_zone_null_anchor_note.py --apply
"""
import argparse
import copy
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')
BASE_SHA = '1dd6ada3c03477f0d9262b660162c73e83f1ce1539db2c9143bba85f2e99c34c'

OLD_NOTES = {'URL not in retro log, needs manual lookup',
             'URL not in retro log -- needs manual lookup'}
NEW_NOTE = ('Legacy zone-layer anchor, deliberately not re-sourced. The regions layer is '
            'authoritative for this claim and carries its own sources, and nothing renders anchor '
            'data from the zone layer. Ruled 2026-07-31; this is a recorded decision, not a '
            'pending task.')
EXPECTED = 57


def _null_anchors(crop):
    """Yield every anchor entry on this crop whose url is null."""
    out = []

    def walk(node):
        if isinstance(node, dict):
            au = node.get('anchoring_urls')
            if isinstance(au, dict):
                for sid, entry in au.items():
                    if isinstance(entry, dict) and entry.get('url') is None:
                        out.append((sid, entry))
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(crop)
    return out


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
        print('ABORT: canonical drifted.\n  expected %s\n  found    %s' % (args.expect_sha, sha))
        return 2
    print('pre-state SHA verified: %s' % sha[:16])

    data = json.loads(raw)
    before = copy.deepcopy(data)

    targets, crops_hit = [], set()
    for crop in data['crops']:
        found = _null_anchors(crop)
        if found:
            crops_hit.add(crop['slug'])
        targets.extend((crop['slug'], sid, e) for sid, e in found)

    if len(targets) != EXPECTED:
        print('ABORT: expected %d null anchors, found %d' % (EXPECTED, len(targets)))
        return 2
    stale = [(s, sid) for s, sid, e in targets if e.get('note') not in OLD_NOTES]
    if stale:
        print('ABORT: %d null anchors do not carry an expected prior note, e.g. %s'
              % (len(stale), stale[:3]))
        return 2
    print('verified: %d null anchors across %d crops, all on a known prior note'
          % (len(targets), len(crops_hit)))

    for _slug, _sid, entry in targets:
        entry['note'] = NEW_NOTE

    # ---- nothing but `note` may have moved -----------------------------------
    for _slug, _sid, entry in targets:
        if entry.get('url') is not None or entry.get('verified') is not None:
            print('ABORT: a null anchor gained a url or verified value')
            return 2

    def fingerprint(payload):
        """Everything except the note text on null anchors."""
        blob = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        for n in OLD_NOTES:
            blob = blob.replace(json.dumps(n, ensure_ascii=False), '"<NOTE>"')
        return blob.replace(json.dumps(NEW_NOTE, ensure_ascii=False), '"<NOTE>"')

    if fingerprint(before) != fingerprint(data):
        print('ABORT: something other than the note text changed')
        return 2

    ba = {c['slug']: c for c in before['crops']}
    aa = {c['slug']: c for c in data['crops']}
    changed = sorted(s for s in ba if ba[s] != aa[s])
    if set(changed) != crops_hit:
        print('ABORT: crops changed = %s, expected %s' % (changed, sorted(crops_hit)))
        return 2
    for k in before:
        if k != 'crops' and before[k] != data[k]:
            print('ABORT: top-level %s changed' % k)
            return 2
    remaining = [1 for c in data['crops'] for _sid, e in _null_anchors(c)
                 if e.get('note') in OLD_NOTES]
    if remaining:
        print('ABORT: %d entries still carry the old note' % len(remaining))
        return 2
    print('verified: %d note rewrites on %s; url, verified and all other data frozen'
          % (len(targets), ', '.join(sorted(crops_hit))))

    if args.dry_run:
        print('\nDRY RUN -- nothing written.')
        return 0

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if out.endswith(b'\n'):
        print('ABORT: trailing newline introduced')
        return 2
    with open(args.canonical, 'wb') as fh:
        fh.write(out)
    print('\nAPPLIED: %d notes rewritten' % len(targets))
    print('  new canonical SHA: %s' % hashlib.sha256(out).hexdigest())
    return 0


if __name__ == '__main__':
    sys.exit(main())
