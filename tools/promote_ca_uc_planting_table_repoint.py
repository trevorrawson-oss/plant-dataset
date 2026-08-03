#!/usr/bin/env python3
"""GUARDED PROMOTE: repoint 52 California bare-UC citations at the table that backs them.

CITATION-ONLY. Not one value moves, not one source id changes, no finding is filed.
Campaign A of the citation-integrity arc; evidence in
docs/2026-08-03-campaign-a-count-reconciliation-and-readjudication.md.

THE DOCUMENT. "Recommended planting dates for major regions of California" --
https://ucanr.edu/program/uc-master-gardener-program/time-planting -- the California Master
Gardener Handbook Table 13.2. Fetched with urllib this session (71,434 bytes) and parsed by HTML
STRUCTURE, never a WebFetch markdown summary, which silently shifts columns on an HTML data table.
The parse asserts a rectangular 33x6 grid, and the region definitions came back byte-identical to
the 2026-07-29 transcription:

    "North and North Coast = Monterey County north; South Coast = San Luis Obispo County south;
     Interior Valleys = Sacramento, San Joaquin, and similar valleys; Desert Valleys = Imperial
     and Coachella Valleys."

WHY THIS IS A URL REPOINT AND NOT A NEW SOURCE ID. Both ids ALREADY cite this exact pathed URL
elsewhere in the dataset -- `ucanr_ext` on 578 nodes, `uc_mg` on 126. The bare hosts are the
outliers, not the pathed form, so the fix is to make these nodes agree with the 704 that already
name the document. No source_catalog entry is added, no `sources` array is touched, no id is
collapsed. That is deliberately a smaller change than promote_mid_south_fruit_tree_repoint.py's
new-id pattern, which was needed there only because `uada_ext` carried two different URLs.

WHAT IS REPOINTED, AND WHAT IS DELIBERATELY LEFT BARE. 26 (crop, region) pairs over 8 crops --
every pair whose window is SUPPORTED or DIVERGENT against the table in EVERY zone. Excluded:

  the 4 ca_desert cucurbit pairs   Their Jul 1 - Jul 31 second planting is CONTRADICTED by the
  (acorn/butternut/spaghetti/      table (winter squash "Feb-March; Aug"; pumpkins "March-June",
   pumpkin)                        no fall cycle at all). Ruled a provenance gap, not a
                                   correctness problem, by the accepted finding
                                   ca_desert_fall_cycle_provenance_gap -- but citing the table on
                                   a cell it contradicts is exactly what this arc exists to stop.
                                   Trevor ruled 2026-08-03: leave all 8 decisions.
  okra ca_desert, ca_north_coast   The two live authoring decisions in the block. UC gives okra
                                   "May" in all four regions while our desert cells open in March
                                   and north-coast z9 opens in June. A value question, and a value
                                   change never rides with a citation change.
  the 6 crops with NO UC row       lemon, lime, pear-asian, pear-european, arugula, edamame. The
                                   page is a VEGETABLE table (artichoke -> watermelons). Citing it
                                   for citrus or tree fruit is the vce_426_331 shape. 12 decisions,
                                   expected CASE 2, out of scope here.

THE MIXED-CLAIM NODE, stated plainly rather than glossed. The 89 nodes are 63 `resolved_by_zone.<z>`
cells and 26 `plantings[<i>]` arms, and each carries a planting window AND harvest fields under one
anchoring_urls block. Table 13.2 publishes planting dates only. The harvest half is not thereby
misattributed: all 8 crops carry an ACCEPTED `*_pilot_regional_calendars_modeled` finding declaring
those windows MODELED from days-to-maturity plus the frost anchors. So the planting half becomes
citable and the harvest half stays declared-as-derived, which is a strict improvement over a domain
root supporting both. No node in the repoint set is a dedicated harvest, bloom, start-indoors or
heat-pause arm; those would be the harvest-start-is-not-a-published-datum shape and are absent here.

FOOTPRINT: exactly 178 anchoring_urls entries on 89 nodes (every node carries both bare ids),
across 52 (crop, region, source) decisions and 8 crops. Only `url` and `verified` move, and only
where `url` is the id's bare host. Every planting and harvest VALUE, every `sources` array, every
other region and every top-level key must be byte-identical. COMPACT preserved.

GUARDS: 19, and all 19 are MUTATION-TESTED -- each is deleted in turn and the suite must fail.
The first pass had 8 of 21 VACUOUS (the fifth occurrence of that pattern in this repo). Six needed
a shim to become reachable at all, and two checks that could not fail under any input were removed
rather than left standing as decoration. `tools/test_promote_ca_uc_planting_table_repoint.py`,
23 tests, green on BOTH runners.

    $ python3 tools/promote_ca_uc_planting_table_repoint.py --dry-run
    $ python3 tools/promote_ca_uc_planting_table_repoint.py --apply
"""
import argparse
import copy
import hashlib
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, 'crops_data_final.json')
BASE_SHA = '38a579d4c3e92e470892c9c992215de750f14f5bad02107d6cfc790ebdecc93a'

BARE = {'ucanr_ext': 'https://ucanr.edu', 'uc_mg': 'https://mg.ucanr.edu'}
NEW_URL = 'https://ucanr.edu/program/uc-master-gardener-program/time-planting'
VERIFIED = '2026-08-03'

EXPECT_NODES = 89        # distinct dicts carrying anchoring_urls
EXPECT_ENTRIES = 178     # anchoring_urls entries -- every node carries BOTH bare ids
EXPECT_DECISIONS = 52    # distinct (crop, region, source_id)

# Table 13.2, transcribed from the raw-bytes parse this session. Column order as published:
# North & North Coast | South Coast | Interior Valleys | Desert Valleys.
UC_TABLE = {
    'squash, winter': ('May', 'April-June', 'April-June', 'Feb-March; Aug'),
    'pumpkins': ('May', 'May-June', 'April-June', 'March-June'),
    'cantaloupes and other melons': ('May', 'April-May', 'April-June', 'Jan-April'),
    'watermelons': ('May-June', 'April-June', 'April-June', 'Jan-March'),
    'okra': ('May', 'April-May', 'May', 'May'),
}
UC_ROW = {
    'acorn-squash': 'squash, winter', 'butternut-squash': 'squash, winter',
    'spaghetti-squash': 'squash, winter', 'pumpkin': 'pumpkins',
    'cantaloupe': 'cantaloupes and other melons',
    'honeydew-melon': 'cantaloupes and other melons',
    'watermelon': 'watermelons', 'okra': 'okra',
}
COL = {'ca_north_coast': 0, 'ca_south_coast': 1, 'ca_interior': 2, 'ca_desert': 3}

# The 26 pairs to repoint. Explicit, not computed, so the intended footprint is auditable.
REPOINT_PAIRS = [
    ('acorn-squash', 'ca_interior'), ('acorn-squash', 'ca_north_coast'),
    ('acorn-squash', 'ca_south_coast'),
    ('butternut-squash', 'ca_interior'), ('butternut-squash', 'ca_north_coast'),
    ('butternut-squash', 'ca_south_coast'),
    ('spaghetti-squash', 'ca_interior'), ('spaghetti-squash', 'ca_north_coast'),
    ('spaghetti-squash', 'ca_south_coast'),
    ('pumpkin', 'ca_interior'), ('pumpkin', 'ca_north_coast'), ('pumpkin', 'ca_south_coast'),
    ('okra', 'ca_interior'), ('okra', 'ca_south_coast'),
    ('cantaloupe', 'ca_interior'), ('cantaloupe', 'ca_north_coast'),
    ('cantaloupe', 'ca_south_coast'), ('cantaloupe', 'ca_desert'),
    ('honeydew-melon', 'ca_interior'), ('honeydew-melon', 'ca_north_coast'),
    ('honeydew-melon', 'ca_south_coast'), ('honeydew-melon', 'ca_desert'),
    ('watermelon', 'ca_interior'), ('watermelon', 'ca_north_coast'),
    ('watermelon', 'ca_south_coast'), ('watermelon', 'ca_desert'),
]

# Pairs that MUST come out untouched: the ruled cucurbit fall-cycle gap + the two live okra calls.
HELD_PAIRS = [
    ('acorn-squash', 'ca_desert'), ('butternut-squash', 'ca_desert'),
    ('spaghetti-squash', 'ca_desert'), ('pumpkin', 'ca_desert'),
    ('okra', 'ca_desert'), ('okra', 'ca_north_coast'),
]

MON = {m: i for i, m in enumerate(
    ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'], 1)}
MONTH_RE = r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)'


def _span(first, last):
    out, cur = {first}, first
    while cur != last:
        cur = cur % 12 + 1
        out.add(cur)
    return out


def months_uc(s):
    out = set()
    for seg in s.replace('–', '-').lower().split(';'):
        f = re.findall(MONTH_RE, seg)
        if not f:
            continue
        out |= _span(MON[f[0]], MON[f[-1]]) if ('-' in seg and len(f) > 1) else {MON[x] for x in f}
    return out


def months_ours(s):
    out = set()
    for seg in (s or '').lower().split(','):
        f = re.findall(MONTH_RE, seg)
        if f:
            out |= _span(MON[f[0]], MON[f[-1]])
    return out


def windows(cell):
    """Every planting window a zone cell states, main plus any second planting."""
    w = [cell.get('plant_out')]
    sp = cell.get('second_planting')
    if isinstance(sp, dict):
        w.append(sp.get('plant_out'))
    return [x for x in w if isinstance(x, str) and x.strip()]


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
    crops = {c['slug']: c for c in data['crops']}

    if sorted(REPOINT_PAIRS) == sorted(HELD_PAIRS) or (set(REPOINT_PAIRS) & set(HELD_PAIRS)):
        print('ABORT: a held pair appears in the repoint set')
        return 2

    # ---------------------------------------------------------------- preflight
    # 1. Every pair must still exist and still be bare. A landed repoint kills the premise.
    for slug, reg in REPOINT_PAIRS:
        crop = crops.get(slug)
        if crop is None:
            print('ABORT: crop %s absent' % slug)
            return 2
        r = ((crop.get('regions') or {}).get(reg))
        if not isinstance(r, dict):
            print('ABORT: %s has no %s region' % (slug, reg))
            return 2

    # 2. THE LOAD-BEARING GUARD. Re-adjudicate every window against the table AT APPLY TIME, from
    #    the transcribed row rather than from the write-up. We may never cite a document on a cell
    #    it contradicts, so a single contradicted window anywhere in the repoint set aborts.
    checked = 0
    for slug, reg in REPOINT_PAIRS:
        ucm = months_uc(UC_TABLE[UC_ROW[slug]][COL[reg]])
        if not ucm:
            print('ABORT: no UC months parsed for %s / %s' % (slug, reg))
            return 2
        rbz = (crops[slug]['regions'][reg].get('resolved_by_zone') or {})
        if not rbz:
            print('ABORT: %s %s has no resolved_by_zone' % (slug, reg))
            return 2
        for z, cell in sorted(rbz.items()):
            wins = windows(cell)
            if not wins:
                print('ABORT: %s %s z%s states no planting window' % (slug, reg, z))
                return 2
            for w in wins:
                om = months_ours(w)
                if not om:
                    print('ABORT: cannot parse window %r (%s %s z%s)' % (w, slug, reg, z))
                    return 2
                if not (om & ucm):
                    print('ABORT: %s %s z%s window %r is CONTRADICTED by the table (%s). '
                          'Repointing here would publish the contradiction.'
                          % (slug, reg, z, w, UC_TABLE[UC_ROW[slug]][COL[reg]]))
                    return 2
                checked += 1
    print('preflight: %d planting windows re-adjudicated against Table 13.2, none contradicted'
          % checked)

    # 3. The held pairs must still be bare going in -- if one was already repointed, the ruling
    #    this promote depends on has been overtaken and the exclusion list is stale.
    for slug, reg in HELD_PAIRS:
        r = crops[slug]['regions'][reg]
        found = False
        for node, _lbl in _nodes(r):
            au = node.get('anchoring_urls') or {}
            for sid, meta in au.items():
                if sid in BARE and isinstance(meta, dict) and meta.get('url') == BARE[sid]:
                    found = True
        if not found:
            print('ABORT: held pair %s/%s carries no bare UC anchor -- exclusion list is stale'
                  % (slug, reg))
            return 2
    print('preflight: all %d held pairs still bare, as the ruling expects' % len(HELD_PAIRS))

    # ---------------------------------------------------------------- apply
    touched, decisions, hit_nodes = [], set(), []
    for slug, reg in REPOINT_PAIRS:
        for node, label in _nodes(crops[slug]['regions'][reg], '%s %s' % (slug, reg)):
            au = node.get('anchoring_urls')
            if not isinstance(au, dict):
                continue
            for sid in list(au):
                meta = au[sid]
                if sid not in BARE or not isinstance(meta, dict):
                    continue
                if meta.get('url') != BARE[sid]:
                    continue
                if set(meta) - {'url', 'verified'}:
                    print('ABORT: %s %s carries unexpected keys %s'
                          % (label, sid, sorted(set(meta) - {'url', 'verified'})))
                    return 2
                meta['url'] = NEW_URL
                meta['verified'] = VERIFIED
                touched.append('%s %s' % (label, sid))
                decisions.add((slug, reg, sid))
                if id(node) not in [id(n) for n in hit_nodes]:
                    hit_nodes.append(node)

    if len(touched) != EXPECT_ENTRIES:
        print('ABORT: repointed %d anchor entries, expected %d' % (len(touched), EXPECT_ENTRIES))
        return 2
    if len(hit_nodes) != EXPECT_NODES:
        print('ABORT: touched %d nodes, expected %d' % (len(hit_nodes), EXPECT_NODES))
        return 2
    # NOTE: the decision count is REPORTED, not guarded. Mutation testing proved an abort here
    # cannot fail -- decisions are pinned already by the explicit REPOINT_PAIRS list crossed with
    # BARE, and any mutation that moves the decision count moves the entry or node count first.
    # A check that cannot fail is not a guard, so it is not written as one.
    print('applied: %d anchoring_urls entries / %d nodes / %d decisions (expected %d)'
          % (len(touched), len(hit_nodes), len(decisions), EXPECT_DECISIONS))

    # ---------------------------------------------------------------- verify
    # No bare UC host may survive inside a repointed pair.
    for slug, reg in REPOINT_PAIRS:
        for node, label in _nodes(crops[slug]['regions'][reg], '%s %s' % (slug, reg)):
            for sid, meta in (node.get('anchoring_urls') or {}).items():
                if sid in BARE and isinstance(meta, dict) and meta.get('url') == BARE[sid]:
                    print('ABORT: %s still carries the bare %s host' % (label, sid))
                    return 2
    print('verified: 0 bare UC hosts remain in the 26 repointed pairs')

    # The held pairs must be byte-identical.
    ba = {c['slug']: c for c in before['crops']}
    aa = {c['slug']: c for c in data['crops']}
    for slug, reg in HELD_PAIRS:
        if ba[slug]['regions'][reg] != aa[slug]['regions'][reg]:
            print('ABORT: held pair %s/%s was modified' % (slug, reg))
            return 2
    print('verified: all %d held pairs byte-identical' % len(HELD_PAIRS))

    # Exact crop footprint.
    changed = sorted(s for s in ba if ba[s] != aa[s])
    expect = sorted({s for s, _r in REPOINT_PAIRS})
    if changed != expect:
        print('ABORT: crops changed = %s, expected %s' % (changed, expect))
        return 2
    for k in before:
        if k != 'crops' and before[k] != data[k]:
            print('ABORT: top-level %s changed' % k)
            return 2
    print('verified: exactly %d crops changed, no top-level key moved' % len(changed))

    # NOTHING but url/verified moved. Blanking every touched anchor in both trees must make them
    # equal -- which proves no window, no sources array and no other region shifted.
    def blanked(doc):
        d = copy.deepcopy(doc)
        for crop in d['crops']:
            for node, _l in _nodes(crop):
                for sid, meta in (node.get('anchoring_urls') or {}).items():
                    if sid in BARE and isinstance(meta, dict):
                        meta['url'] = meta['verified'] = '<blanked>'
        return d
    if blanked(before) != blanked(data):
        # single abort path: a second "slipped through" fallback was mutation-proven unreachable,
        # because a top-level difference is already caught above and a crops difference always
        # names a culprit here.
        culprits = [s for s in changed
                    if blanked({'crops': [ba[s]]}) != blanked({'crops': [aa[s]]})]
        print('ABORT: changed somewhere other than a UC url/verified pair: %s'
              % (', '.join(culprits) or 'outside the crops list'))
        return 2
    print('verified: only url/verified moved -- every window, sources array and region intact')

    if args.dry_run:
        print('\nDRY RUN -- nothing written.')
        return 0

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if out.endswith(b'\n'):
        print('ABORT: trailing newline introduced')
        return 2
    with open(args.canonical, 'wb') as fh:
        fh.write(out)
    print('\nAPPLIED: %d nodes / %d decisions across %d crops'
          % (len(touched), len(decisions), len(changed)))
    print('  bytes %d -> %d' % (len(raw), len(out)))
    print('  new canonical SHA: %s' % hashlib.sha256(out).hexdigest())
    return 0


def _nodes(root, label=''):
    """Every dict under a region (or crop) that carries anchoring_urls, with a readable label."""
    out = []

    def walk(n, path):
        if isinstance(n, dict):
            if isinstance(n.get('anchoring_urls'), dict):
                out.append((n, '%s %s' % (label, path) if label else path))
            for k, v in n.items():
                if k != 'anchoring_urls':
                    walk(v, '%s.%s' % (path, k) if path else k)
        elif isinstance(n, list):
            for i, v in enumerate(n):
                walk(v, '%s[%d]' % (path, i))

    walk(root, '')
    return out


if __name__ == '__main__':
    sys.exit(main())
