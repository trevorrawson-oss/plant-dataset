#!/usr/bin/env python3
"""TRIAGE for the citation-integrity cleanup arc: cited URLs that are a BARE HOST.

READ docs/kickoffs/46-citation-integrity-cleanup-arc.md BEFORE acting on this output.

WHAT IT FINDS. A URL with no path -- `https://ucanr.edu`, `https://extension.arizona.edu` --
is a domain root. It cannot support a crop-specific claim about a planting window, a heat
threshold or a pest control. This is the blind spot a URL-liveness check CANNOT see: every
one of these returns HTTP 200, which is exactly how six portal-root defects survived on
certified asparagus until 2026-07-29.

WHY IT IS A TRIAGE LIST AND NOT A DEFECT LIST. A bare host is one of two very different
things, and they need opposite treatment:

  CASE 1 -- an INSTITUTION POINTER whose real document is nameable from the cell's own
           `source_note` / `source_quote` / prose. The fix is to REPOINT the URL at the
           document: mechanical and safe. This really happens -- `tamu_agrilife` was one of
           these, and the located document (EHT-066) supported its claim precisely.
  CASE 2 -- ALL THERE EVER WAS. No specific document was consulted, so the cell's claim is
           UNSOURCED. That is a CONTENT finding, not a URL fix, and it must be surfaced as
           one rather than quietly repointed at a plausible-looking page.

Telling those apart is the work. Do not mass-edit.

THE SEVERITY SPLIT, which is the useful part. For each bare-host citation this asks whether
the SAME node cites anything else:

  SOLE       the node's only source is a domain root -> the claim rests on nothing citable.
  CORROBORATED  a real source sits alongside it -> the bare host is redundant decoration,
             and repointing or dropping it is low-risk.

Measured on canonical dd24b180: 1,576 bare-host pairs = 681 SOLE + 895 CORROBORATED, and
six source ids carry 601 of the 681. Work SOLE first; it is the same instinct the arc plan
records as "weight tier C toward cells whose claims rest on a single source", now quantified.

NOT A GATE, and deliberately so: these are pre-existing, they need per-row human adjudication,
and wiring 1,576 findings into the suite would flood it. Ship fixes as content passes instead.

    $ python3 tools/bare_host_scan.py                 # summary by source id
    $ python3 tools/bare_host_scan.py --sole          # only the critical rows
    $ python3 tools/bare_host_scan.py --id ucanr_ext  # every node citing one id
"""
import argparse
import collections
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')
BARE = re.compile(r'https?://[^/]+/?$')


def scan(data):
    """Yield (source_id, crop_slug, node_path, is_sole, url) per bare-host citation."""
    rows = []

    def walk(node, slug, path):
        if isinstance(node, dict):
            anchors = node.get('anchoring_urls')
            if isinstance(anchors, dict) and anchors:
                bare = {sid: m.get('url') for sid, m in anchors.items()
                        if isinstance(m, dict) and m.get('url') and BARE.fullmatch(m['url'])}
                if bare:
                    cited = set(anchors) | {s for s in (node.get('sources') or [])
                                            if isinstance(s, str)}
                    has_real = bool(cited - set(bare))
                    for sid, url in bare.items():
                        rows.append((sid, slug, path or '<crop>', not has_real, url))
            for k, v in node.items():
                if k != 'anchoring_urls':
                    walk(v, slug, f'{path}.{k}' if path else k)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, slug, f'{path}[{i}]')

    for crop in data['crops']:
        walk(crop, crop['slug'], '')
    return rows


def pathed_by_self(crop):
    """source_id -> [(node_path, url)] for every PATHED citation this ONE crop carries."""
    out = collections.defaultdict(list)

    def walk(node, path=''):
        if isinstance(node, dict):
            anchors = node.get('anchoring_urls')
            if isinstance(anchors, dict):
                for sid, m in anchors.items():
                    if isinstance(m, dict) and m.get('url') and not BARE.fullmatch(m['url']):
                        out[sid].append((path or '<crop>', m['url']))
            for k, v in node.items():
                if k != 'anchoring_urls':
                    walk(v, f'{path}.{k}' if path else k)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f'{path}[{i}]')

    walk(crop)
    return out


def self_pathed(data):
    """SELF-PATHED: bare citations whose OWN crop already cites that id PATHED elsewhere.

    PLA-161's check class that nobody had implemented. Strictly cheaper to adjudicate than
    SIBLING-PATHED: there is no cross-crop transfer question, because the crop has ALREADY
    decided what document this source id resolves to. Hunt #28 is the archetype -- lemon's
    `regions.se_gulf.resolved_by_zone.8` cites `clemson_hgic` bare, while lemon cites the same id
    pathed at `hgic.clemson.edu/cold-tolerance-in-citrus/` on 14 other nodes, one URL, no
    ambiguity.

    STILL A LEAD, NOT A REPOINT. That the crop resolved the id elsewhere does not establish that
    the document supports THIS cell's claim; that is a read
    ([[sibling-precedent-pressures-a-wrong-repoint]]). Measured at `76f92a20`:

        315 bare CITATIONS / 155 SOLE / 78 DECISIONS / 37 CROPS

    Note the population includes MASKED rows deliberately. Hunt #28 is masked, which is exactly
    why no campaign ever counted it -- filtering to SOLE here would rebuild the blind spot this
    issue exists to remove.
    """
    crops = {c['slug']: c for c in data['crops']}
    by_crop = {slug: pathed_by_self(crop) for slug, crop in crops.items()}
    rows = []
    for sid, slug, path, is_sole, url in scan(data):
        elsewhere = [(p, u) for p, u in by_crop[slug].get(sid, []) if p != path]
        if elsewhere:
            rows.append({'crop': slug, 'path': path, 'source_id': sid, 'bare_url': url,
                         'is_sole': is_sole, 'pathed_at': elsewhere})
    return rows


def _masked_only_decisions(data):
    """Decisions (crop, region, source_id) whose bare rows are ALL masked. Derived live."""
    import hunt_footprint
    return sum(1 for v in hunt_footprint.decisions(data).values()
               if v['sole'] == 0 and v['masked'])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sole', action='store_true', help='only SOLE-source rows')
    ap.add_argument('--id', help='itemize every node citing this source id')
    ap.add_argument('--self-pathed', action='store_true',
                    help='rows whose own crop already cites that id PATHED elsewhere')
    args = ap.parse_args()

    with open(CANONICAL, encoding='utf-8') as fh:
        data = json.load(fh)
    catalog = data.get('source_catalog') or {}
    rows = scan(data)

    if args.self_pathed:
        sp = self_pathed(data)
        decisions = {(r['crop'], (re.match(r'regions\.([^.\[]+)', r['path']) or [None, None])[1],
                      r['source_id']) for r in sp}
        print(f"SELF-PATHED: {len(sp)} bare CITATIONS ({sum(1 for r in sp if r['is_sole'])} SOLE) "
              f"/ {len(decisions)} DECISIONS / {len({r['crop'] for r in sp})} CROPS")
        print("The crop has already resolved this id to a document elsewhere. That is a LEAD.")
        print("Read the document before repointing -- it may not support THIS cell's claim.\n")
        for r in sorted(sp, key=lambda r: (r['crop'], r['source_id'], r['path'])):
            docs = sorted({u for _p, u in r['pathed_at']})
            print(f"  {'SOLE  ' if r['is_sole'] else 'masked'}  {r['crop']}:{r['path']}")
            print(f"          {r['source_id']} -> {' | '.join(d[:82] for d in docs[:2])}"
                  f"{' ...' if len(docs) > 2 else ''}")
        return 0

    if args.id:
        sel = [r for r in rows if r[0] == args.id and (r[3] or not args.sole)]
        print(f'{args.id}: {len(sel)} bare-host citation(s)'
              f"  catalog url: {catalog.get(args.id, {}).get('url', '?')}")
        for sid, slug, path, is_sole, _url in sorted(sel, key=lambda r: (not r[3], r[1], r[2])):
            print(f"  {'SOLE      ' if is_sole else 'corroborated'}  {slug}:{path}")
        return 0

    sole = collections.Counter()
    corrob = collections.Counter()
    crops = collections.defaultdict(set)
    for sid, slug, _path, is_sole, _url in rows:
        (sole if is_sole else corrob)[sid] += 1
        crops[sid].add(slug)

    ids = sorted(set(sole) | set(corrob), key=lambda s: (-sole[s], -corrob[s]))
    if args.sole:
        ids = [s for s in ids if sole[s]]
    print(f'{"source id":24} {"SOLE":>6} {"corrob":>7} {"crops":>6}  catalog url')
    print('-' * 92)
    for sid in ids:
        url = (catalog.get(sid) or {}).get('url', '')
        flag = 'CRITICAL ' if sole[sid] else '         '
        print(f'{sid:24} {sole[sid]:6d} {corrob[sid]:7d} {len(crops[sid]):6d}  {flag}{url[:38]}')
    print('-' * 92)
    print(f'{"TOTAL":24} {sum(sole.values()):6d} {sum(corrob.values()):7d}')
    print()
    # PLA-161 predicate 2. This table is where the masked population is CREATED: `is_sole` goes
    # False the moment a node cites anything pathed, and all four campaigns priced work from
    # `if not sole: continue`. Printing SOLE and corroborated without the masked-only decision
    # count lets a reader treat the SOLE column as the worklist, which is how 211 decisions went
    # uncounted. The residue is stated here rather than left for hunt_footprint to discover.
    masked_only = _masked_only_decisions(data)
    print(f'MASKED-ONLY DECISIONS (every bare row masked by a pathed co-source): {masked_only}')
    print('These entered NO campaign denominator. The SOLE column is not the worklist.')
    print('See tools/hunt_footprint.py and tools/reporting_contract.py.')
    print()
    print(f'SOLE = the node cites nothing but a domain root; its claim rests on nothing '
          f'citable. Work these first.')
    print(f'Then adjudicate each: CASE 1 repointable at a real document, or CASE 2 the claim '
          f'is unsourced (a CONTENT finding).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
