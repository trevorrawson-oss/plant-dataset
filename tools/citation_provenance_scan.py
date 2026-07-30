#!/usr/bin/env python3
"""RE-PRICE the citation-integrity arc's bare-host worklist. No network. NOT a gate.

READ docs/2026-07-29-citation-cleanup-sample-pass-outcome.md and the kickoff
docs/kickoffs/46-citation-integrity-cleanup-arc.md BEFORE acting on this output.

`tools/bare_host_scan.py` answers "how many bare-host citations are there" (1,576; 681 SOLE).
This tool answers the three questions that actually size the remediation, and each one moved
the estimate by an order of magnitude:

  --decisions  The 681 SOLE pairs are REDUNDANT. For one crop x region the same bare host
               repeats on plantings[0], .plant_out[0], .bloom[0], .harvest_start[0],
               .harvest_end[0] AND resolved_by_zone.N. Collapsed to the real adjudication
               unit (crop, region, source) it is 170 decisions over 32 (region, source)
               document hunts -- not 681 claims each needing a document located.

  --declared   53% of the SOLE nodes sit on crops whose verification_status.open_findings
               ALREADY DECLARE the derivation ("windows are MODELED from days-to-maturity +
               the shared frost anchors"; "region-rep source anchors use the institution
               BASE URL rather than a live crop-specific page"). Those are an accepted,
               documented convention with a scheduled cleanup -- a DIFFERENT defect class
               from unr_fs0261, which was a real document cited for a claim it does not
               contain. The 681 count conflates the two. The UNDECLARED remainder is the
               real worklist, and it is concentrated in fruit trees/berries in the two most
               recently built regions (mid_south/uada_ext, mid_atlantic/ncsu_ext).

  --split      The kickoff's cost reality says that for 680 of the 681 SOLE rows "the
               specific document was never recorded anywhere and has to be located per
               claim", because the CATALOG url is itself a bare host. The catalog half is
               true; the conclusion is not. EVERY ONE of the 26 bare-host source ids also
               cites real pathed documents on other cells -- ncsu_ext 1,742 pathed uses vs
               99 bare, clemson_hgic 2,483 vs 12. There are ZERO bare-only ids. The document
               to repoint at is usually already in a sibling cell.

               CAVEAT, and it is load-bearing: a pathed ncsu_ext url for borage does not
               support apple. This makes the HUNT cheap, not the ANSWER free. Adjudicate.

Default prints all three sections.

    $ python3 tools/citation_provenance_scan.py
    $ python3 tools/citation_provenance_scan.py --decisions
    $ python3 tools/citation_provenance_scan.py --declared --undeclared-detail
"""
import argparse
import collections
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))
from bare_host_scan import BARE, scan  # noqa: E402

CANONICAL = os.path.join(REPO, 'crops_data_final.json')

# "the WINDOWS are a derivation, not a quoted datum"
MODELED = re.compile(
    r'not (?:each |individually )?source[- ]verified|are MODELED|are modeled'
    r'|windows are modeled|MODELED from|modeled from', re.I)
# "the ANCHOR is an institution base url" -- the bare host itself, declared
PORTAL = re.compile(
    r'base URL|institution-level|institution/publication|institutional anchors|portal'
    r'|rather than a live [^.]*?-specific page'
    r'|rather than an? [^.]*?-specific regional planting-date page', re.I)


def region_of(path):
    m = re.match(r'regions\.([a-z0-9_]+)\.', path)
    return m.group(1) if m else '<crop-level>'


def all_uses(data):
    """source_id -> {url: count} across every anchoring_urls block in the dataset."""
    uses = collections.defaultdict(collections.Counter)

    def walk(node):
        if isinstance(node, dict):
            a = node.get('anchoring_urls')
            if isinstance(a, dict):
                for sid, m in a.items():
                    if isinstance(m, dict) and m.get('url'):
                        uses[sid][m['url']] += 1
            for k, v in node.items():
                if k != 'anchoring_urls':
                    walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    for crop in data['crops']:
        walk(crop)
    return uses


def declares(crop):
    """(modeled_findings, portal_findings) for one crop, as (id, status) pairs."""
    ofs = (crop.get('verification_status') or {}).get('open_findings') or []
    m_hits, p_hits = [], []
    for f in ofs:
        if not isinstance(f, dict):
            continue
        blob = json.dumps(f, ensure_ascii=False)
        row = (f.get('id', '?'), f.get('status', '?'))
        if MODELED.search(blob):
            m_hits.append(row)
        if PORTAL.search(blob):
            p_hits.append(row)
    return m_hits, p_hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--decisions', action='store_true')
    ap.add_argument('--declared', action='store_true')
    ap.add_argument('--split', action='store_true')
    ap.add_argument('--undeclared-detail', action='store_true',
                    help='itemize the undeclared crops -- the real worklist')
    args = ap.parse_args()
    show_all = not (args.decisions or args.declared or args.split)

    with open(CANONICAL, encoding='utf-8') as fh:
        data = json.load(fh)
    crops = {c['slug']: c for c in data['crops']}
    catalog = data.get('source_catalog') or {}

    rows = scan(data)
    sole = [r for r in rows if r[3]]
    nodes = collections.OrderedDict()
    for sid, slug, path, _s, _u in sole:
        nodes.setdefault((slug, path), []).append(sid)

    if show_all or args.decisions:
        dec = collections.OrderedDict()
        hunts = collections.defaultdict(set)
        for sid, slug, path, _s, _u in sole:
            reg = region_of(path)
            dec[(slug, reg, sid)] = dec.get((slug, reg, sid), 0) + 1
            hunts[(reg, sid)].add(slug)
        print('=' * 92)
        print('THE REAL ADJUDICATION UNIT -- the 681 pairs are redundant per crop x region')
        print('=' * 92)
        print('  SOLE bare-host pairs                     %6d' % len(sole))
        print('  distinct SOLE nodes                      %6d' % len(nodes))
        print('  distinct (crop, region, source) DECISIONS %5d' % len(dec))
        print('  distinct (region, source) DOCUMENT HUNTS  %5d' % len(hunts))
        print()
        print('  %-16s %-20s %6s  %s' % ('region', 'source id', 'crops', 'which crops'))
        print('  ' + '-' * 88)
        for (reg, sid), cs in sorted(hunts.items(), key=lambda kv: -len(kv[1])):
            print('  %-16s %-20s %6d  %s' % (
                reg, sid, len(cs), ','.join(sorted(cs))[:44]))
        print()

    if show_all or args.declared:
        buckets = collections.Counter()
        bpairs = collections.Counter()
        bcrops = collections.defaultdict(set)
        per_crop = {}
        for slug in {k[0] for k in nodes}:
            per_crop[slug] = declares(crops[slug])
        for (slug, path), sids in nodes.items():
            m, p = per_crop[slug]
            b = ('DECLARED_BOTH' if (m and p) else 'DECLARED_PORTAL' if p
                 else 'DECLARED_MODELED' if m else 'UNDECLARED')
            buckets[b] += 1
            bpairs[b] += len(sids)
            bcrops[b].add(slug)
        print('=' * 92)
        print('DOES THE CROP ALREADY DECLARE THE DERIVATION? (accepted open_findings)')
        print('=' * 92)
        print('  %-18s %7s %7s %7s' % ('bucket', 'nodes', 'pairs', 'crops'))
        print('  ' + '-' * 46)
        for b in ('DECLARED_BOTH', 'DECLARED_PORTAL', 'DECLARED_MODELED', 'UNDECLARED'):
            print('  %-18s %7d %7d %7d' % (b, buckets[b], bpairs[b], len(bcrops[b])))
        print('  ' + '-' * 46)
        print('  %-18s %7d %7d %7d' % ('TOTAL', sum(buckets.values()),
                                       sum(bpairs.values()), len({k[0] for k in nodes})))
        print()
        print('  UNDECLARED is the real worklist. A declared bare host is an honest')
        print('  admission of derivation; unr_fs0261 was a document cited for a claim it')
        print('  does not contain. Do not treat them as one class.')
        print()
        if args.undeclared_detail or show_all:
            und = collections.Counter(
                slug for (slug, _p) in nodes
                if not any(declares(crops[slug])))
            if und:
                print('  UNDECLARED crops, by SOLE node count:')
                for slug, n in und.most_common():
                    print('    %-22s %3d  (%s)' % (
                        slug, n, crops[slug].get('archetype') or '?'))
                print()

    if show_all or args.split:
        uses = all_uses(data)
        sole_by_id = collections.Counter(r[0] for r in sole)
        bare_by_id = collections.Counter(r[0] for r in rows)
        print('=' * 92)
        print('IS THE DOCUMENT RECORDED ANYWHERE? (bare-host ids that ALSO cite pathed docs)')
        print('=' * 92)
        print('  %-22s %6s %6s %7s  %s' % (
            'source id', 'bare', 'SOLE', 'pathed', 'top pathed doc already in the data'))
        print('  ' + '-' * 88)
        bare_only = []
        for sid in sorted(uses, key=lambda s: -sole_by_id[s]):
            bare = {u: n for u, n in uses[sid].items() if BARE.fullmatch(u)}
            pathed = {u: n for u, n in uses[sid].items() if not BARE.fullmatch(u)}
            if not bare:
                continue
            if not pathed:
                bare_only.append(sid)
                continue
            top = max(pathed, key=lambda u: pathed[u])
            print('  %-22s %6d %6d %7d  %s' % (
                sid, sum(bare.values()), sole_by_id[sid], sum(pathed.values()), top[:46]))
        print('  ' + '-' * 88)
        print('  bare-ONLY ids (document never recorded anywhere): %d  %s' % (
            len(bare_only), ', '.join(bare_only) or '-- none --'))
        print()
        print('  CAVEAT: a pathed url for another crop does not support THIS claim. This')
        print('  makes the hunt cheap, not the answer free. Adjudicate, do not mass-repoint.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
