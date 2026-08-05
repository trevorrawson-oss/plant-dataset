#!/usr/bin/env python3
"""A node cites a DOMAIN ROOT under a source id whose catalog entry already names a DOCUMENT.

READ docs/2026-08-05-campaign-c-reprice-and-arid-document-read.md before acting on this output.

WHAT IT FINDS, and why nothing else can see it. `bare_host_scan` finds citations pointing at a
domain root, but it never consults `source_catalog`, so it reports these as just another bare host
among hundreds and cannot tell you the document is ALREADY NAMED inside this repo.
`url_health_gate` cannot see them either: every one returns HTTP 200. That blind spot is how
carrot carried `nmsu_chart` -- New Mexico State -- at `https://desert.tamu.edu/`, a bare TEXAS A&M
host, on its `warm_arid` zone 8 cell and that cell's `heat_pause`, while the catalog held the
correct Dona Ana planting chart the whole time and carrot's OTHER nodes cited it correctly.

This is the CHEAPEST repoint class in the citation arc: no document hunt, because the answer is
already in the catalog. It is a scan and not a gate -- the rows need per-node adjudication, and a
node may legitimately sit on a root while its id's catalog url points at one particular document.

FOUR WIDER DEFINITIONS WERE MEASURED ON 2026-08-05 AND ALL FLOOD. Recorded so they are not
rebuilt, in the same spirit as the harvest-window text gate that was measured and deliberately not
built:

  node host != catalog host                                     729 nodes
      Institutions legitimately publish across many hosts. `cameron.agrilife.org` and
      `aggie-horticulture.tamu.edu` are Texas A&M; `fieldreport.caes.uga.edu` is UGA;
      `ask.ifas.ufl.edu` is UF/IFAS; `nevegetable.org` is UMass and partners. Not a defect class.
  one id carrying several documents, some off-host             47 source ids
      Same cause. `ncsu_ext` alone spans 83 distinct urls, 51 of them off `content.ces.ncsu.edu`,
      essentially all correct.
  catalog names a pathed document, node cites a different url  floods
      The ASPCA entry names a toxic-plant INDEX and nodes cite its per-plant pages beneath it,
      which is exactly right.
  ... additionally excluding descendants and same-host pages    still floods
      "Pathed" does not mean "a specific document": `msu_bozeman`'s catalog url is
      `montana.edu/extension/`, a portal with a path, and 80 nodes correctly cite a page elsewhere
      on that site.

Only the narrow definition below stays clean. The lavender shape it CANNOT catch -- an id whose
catalog entry names one document while a node cites a different, pathed, real document (NMSU's
low-water ornamental list standing in for a food-garden planting chart) -- is left to human
review on purpose. Every mechanical version of it floods.

    $ python3 tools/catalog_divergence_scan.py
    $ python3 tools/catalog_divergence_scan.py --nodes
"""
import argparse
import collections
import json
import os
import re
import sys
from urllib.parse import urlsplit

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')
BARE = re.compile(r'https?://[^/]+/?$')


def host(url):
    h = (urlsplit(url).hostname or '').lower()
    return h[4:] if h.startswith('www.') else h


def walk(data):
    """Yield (source_id, crop_slug, node_path, url) per anchoring_urls entry."""
    rows = []

    def rec(node, slug, path):
        if isinstance(node, dict):
            anchors = node.get('anchoring_urls')
            if isinstance(anchors, dict):
                for sid, meta in anchors.items():
                    if isinstance(meta, dict) and meta.get('url'):
                        rows.append((sid, slug, path or '<crop>', meta['url']))
            for k, v in node.items():
                if k != 'anchoring_urls':
                    rec(v, slug, f'{path}.{k}' if path else k)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                rec(v, slug, f'{path}[{i}]')

    for crop in data['crops']:
        rec(crop, crop['slug'], '')
    return rows


def divergences(data):
    """The narrow check: node url is a domain ROOT while the catalog names a DOCUMENT.

    Returns {(source_id, node_url, catalog_url): [crop:path, ...]}.
    """
    catalog = data.get('source_catalog') or {}
    out = collections.defaultdict(list)
    for sid, slug, path, url in walk(data):
        cu = (catalog.get(sid) or {}).get('url')
        if cu and BARE.fullmatch(url) and not BARE.fullmatch(cu):
            out[(sid, url, cu)].append(f'{slug}:{path}')
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--nodes', action='store_true', help='itemize every node')
    ap.add_argument('--canonical', default=CANONICAL)
    args = ap.parse_args()

    with open(args.canonical, encoding='utf-8') as fh:
        data = json.load(fh)
    found = divergences(data)

    total = sum(len(v) for v in found.values())
    print('catalog_divergence_scan: %d node(s) over %d (id, url) pair(s), %d source id(s)'
          % (total, len(found), len({k[0] for k in found})))
    if not found:
        print('  none -- every bare-host citation belongs to an id whose catalog entry is also a '
              'root, so there is no already-named document to repoint at.')
        return 0

    print()
    for (sid, url, cu), nodes in sorted(found.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        same = host(url) == host(cu)
        print('  %-24s %2d node(s)%s' % (sid, len(nodes),
                                         '' if same else '   *** and the HOSTS DISAGREE ***'))
        print('     node cites  : %s' % url)
        print('     catalog has : %s' % cu)
        if args.nodes:
            for n in sorted(nodes):
                print('        %s' % n)
    print()
    print('Each row is a CASE 1 repoint whose target is already in source_catalog -- no document '
          'hunt. Adjudicate per node: a root may occasionally be the honest citation.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
