#!/usr/bin/env python3
"""THE CANONICAL HUNT-FOOTPRINT LIST for the citation-integrity cleanup arc, plus the
masked-population measurement built on it. Read-only. NOT a gate.

WHY THIS EXISTS (PLA-187). The arc's 32 hunts lived only as a prose table in
docs/citation_arc_hunt_ledger.md and as partial per-campaign dicts inside three repricers.
When PLA-138's diagnostic needed "every decision in the arc's own hunts that no campaign
ever counted", two independent walks reconstructed the footprint differently and reported
125 vs 154 -- the 125 walk silently omitted hunts #3-6 (the four ca_*/ucanr_ext hunts,
29 masked-only decisions including one D-residue). The disagreement was never about the
data; it was about which (region, source_id) pairs count as "the arc". This file is the
one answer to that question.

WHAT IT MEASURES. `bare_host_scan` marks a bare-host citation SOLE only when its node
cites nothing else; all four campaigns priced work from `if not sole: continue`. A
decision (crop, region, source_id) whose bare rows are ALL masked therefore never entered
any campaign's denominator. This tool counts that population per hunt and per campaign,
prints the hunts that render as zero rows (a hunt that was fixed and a hunt that was
filtered away must NOT render identically -- that is the PLA-187 defect), and classifies
every masked-only decision:

  DECLARED        the crop carries an open_finding whose JSON names the bare source id --
                  the same adjudication vocabulary campaigns C and D closed against.
  SAMEINST-COVER  a pathed co-source from the SAME institution family sits on the node
                  (e.g. bare `uc_mg` beside pathed `ucanr_ext_mg_timeplanting`): the bare
                  id is decoration next to its own institution's real document.
  NEITHER         no declaration, no same-institution cover. The genuinely unadjudicated
                  residue. Measured 2026-08-10 at 72284f02: 38 of 154 in-footprint, plus
                  19 of 56 on pairs that never became hunts at all (--oof).

Every run cross-checks `bare_host_scan.scan` against an independent walk that does not
import it (`a-clean-zero-can-be-your-own-parser`), and a count of masked rows is NOT a
count of defects until some are read -- the PLA-187 severity reads live in
docs/2026-08-10-pla187-masked-population-measured.md.

    $ python3 tools/hunt_footprint.py              # per-hunt + per-campaign tables
    $ python3 tools/hunt_footprint.py --classify   # DECLARED / SAMEINST / NEITHER
    $ python3 tools/hunt_footprint.py --neither    # itemize the unadjudicated residue
    $ python3 tools/hunt_footprint.py --oof        # masked pairs outside every hunt
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

# ---------------------------------------------------------------------------------------------
# The 32 hunts of docs/citation_arc_hunt_ledger.md, as data: (region, source_id) -> (hunt#,
# campaign-of-record). Campaign assignment follows the ledger's campaign table exactly; the
# four ucr_citrus hunts were withdrawn 2026-07-31 (false Riverside premise) and belong to no
# campaign. Keep this in lockstep with the ledger -- it is the machine-readable half of it.
# ---------------------------------------------------------------------------------------------
FOOTPRINT = {
    ('mid_south', 'uada_ext'): (1, 'B'),
    ('mid_atlantic', 'ncsu_ext'): (2, 'B'),
    ('ca_interior', 'ucanr_ext'): (3, 'A'),
    ('ca_north_coast', 'ucanr_ext'): (4, 'A'),
    ('ca_south_coast', 'ucanr_ext'): (5, 'A'),
    ('ca_desert', 'ucanr_ext'): (6, 'A'),
    ('warm_arid', 'nmsu_ext'): (7, 'C'),
    ('warm_arid', 'tamu_agrilife'): (8, 'C'),
    ('ca_interior', 'uc_mg'): (9, 'A'),
    ('ca_north_coast', 'uc_mg'): (10, 'A'),
    ('ca_south_coast', 'uc_mg'): (11, 'A'),
    ('ca_desert', 'uc_mg'): (12, 'A'),
    ('rgv', 'tamu_agrilife'): (13, 'C'),
    ('low_desert_az', 'uariz_ext'): (14, 'C'),
    ('ca_south_coast', 'ucr_citrus'): (15, 'withdrawn'),
    ('ca_north_coast', 'ucanr_marin_mg'): (16, 'D'),
    ('warm_arid', 'nmsu_donaana_mg'): (17, 'C'),
    ('fl_peninsula', 'ufifas_ext'): (18, 'D'),
    ('ca_interior', 'ucr_citrus'): (19, 'withdrawn'),
    ('ca_north_coast', 'ucr_citrus'): (20, 'withdrawn'),
    ('ca_desert', 'uariz_ext'): (21, 'C'),
    ('<crop-level>', 'ucr_citrus'): (22, 'withdrawn'),
    ('se_gulf', 'uga_ext'): (23, 'D'),
    ('warm_arid', 'nmsu_chart'): (24, 'C'),
    ('northern_tier', 'clemson_hgic'): (25, 'D'),
    ('northern_tier', 'tamu_agrilife'): (26, 'D'),
    ('se_gulf', 'tamu_agrilife'): (27, 'D'),
    ('se_gulf', 'clemson_hgic'): (28, 'D'),
    ('ca_interior', 'uc_ipm'): (29, 'D'),
    ('warm_arid', 'uariz_ext'): (30, 'D'),
    ('warm_arid', 'clemson_hgic'): (31, 'D'),
    ('low_desert_az', 'ucanr_ext'): (32, 'D'),
}

# Citrus rows on these pairs were deferred INTO campaign D by A and C (the ledger's note
# column defers them seven separate times). Mirrors campaign_d_reprice.RESIDUE_HUNTS.
RESIDUE_PAIRS = {
    ('ca_interior', 'ucanr_ext'), ('ca_north_coast', 'ucanr_ext'),
    ('ca_south_coast', 'ucanr_ext'), ('ca_desert', 'ucanr_ext'),
    ('warm_arid', 'tamu_agrilife'), ('low_desert_az', 'uariz_ext'),
    ('ca_desert', 'uariz_ext'),
}
CITRUS = {'lemon', 'lime'}

# Institution families for the SAMEINST test. `uf_ifas*` and `ufifas*` are the same
# institution under two id spellings -- the exact miss that would undercount this class.
FAMILIES = (
    ('uc', ('ucanr', 'uc_', 'ucr')), ('tamu', ('tamu',)), ('nmsu', ('nmsu',)),
    ('ufl', ('uf_ifas', 'ufifas')), ('uga', ('uga',)), ('clemson', ('clemson',)),
    ('ncsu', ('ncsu',)), ('uariz', ('uariz',)), ('uaex', ('uada',)),
)


def family(sid):
    for fam, prefixes in FAMILIES:
        if any(sid.startswith(p) for p in prefixes):
            return fam
    return sid.split('_')[0]


def region_of(path):
    m = re.match(r'regions\.([a-z0-9_]+)\.', path)
    return m.group(1) if m else '<crop-level>'


def campaign_of(region, sid, slug):
    """(hunt#, campaign) for one bare citation, or (None, None) outside every hunt."""
    if (region, sid) not in FOOTPRINT:
        return None, None
    hunt, camp = FOOTPRINT[(region, sid)]
    if slug in CITRUS and (region, sid) in RESIDUE_PAIRS:
        return hunt, 'D(residue)'
    return hunt, camp


def independent_walk(data):
    """Re-derive bare_host_scan.scan's rows without importing its walker."""
    rows = []

    def walk(node, slug, path):
        if isinstance(node, dict):
            a = node.get('anchoring_urls')
            if isinstance(a, dict) and a:
                bare = {sid: m['url'] for sid, m in a.items()
                        if isinstance(m, dict) and m.get('url') and BARE.fullmatch(m['url'])}
                if bare:
                    cited = set(a) | {s for s in (node.get('sources') or [])
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


def node_at(crop, path):
    node = crop
    if path == '<crop>':
        return node
    for part in path.split('.'):
        while '[' in part:
            name, _, rest = part.partition('[')
            idx, _, part = rest.partition(']')
            if name:
                node = node[name]
            node = node[int(idx)]
            if part.startswith('.'):
                part = part[1:]
            if not part:
                break
        else:
            node = node[part]
    return node


def decisions(data):
    """(slug, region, sid) -> {'sole': n, 'masked': n, 'paths': [...]} with cross-check."""
    rows = scan(data)
    indep = independent_walk(data)
    assert sorted(rows) == sorted(indep), (
        'WALK DISAGREEMENT: bare_host_scan %d rows, independent %d' % (len(rows), len(indep)))
    dec = collections.defaultdict(lambda: {'sole': 0, 'masked': 0, 'paths': []})
    for sid, slug, path, is_sole, url in rows:
        d = dec[(slug, region_of(path), sid)]
        d['sole' if is_sole else 'masked'] += 1
        d['paths'].append(path)
    return dec


def classify(data, slug, reg, sid, paths):
    """DECLARED / SAMEINST-COVER / both / NEITHER for one masked-only decision."""
    crop = next(c for c in data['crops'] if c['slug'] == slug)
    declared = None
    for f in (crop.get('verification_status') or {}).get('open_findings') or []:
        if isinstance(f, dict) and sid in json.dumps(f, ensure_ascii=False):
            declared = (f.get('id'), f.get('status'))
            break
    same = False
    for path in paths:
        n = node_at(crop, path)
        for cid, m in (n.get('anchoring_urls') or {}).items():
            u = m.get('url') if isinstance(m, dict) else None
            if u and not BARE.fullmatch(u) and family(cid) == family(sid):
                same = True
    if declared and same:
        return 'DECLARED+SAMEINST', declared
    if declared:
        return 'DECLARED', declared
    if same:
        return 'SAMEINST-COVER', None
    return 'NEITHER', None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--classify', action='store_true')
    ap.add_argument('--neither', action='store_true')
    ap.add_argument('--oof', action='store_true', help='pairs outside every hunt')
    args = ap.parse_args()

    with open(CANONICAL, encoding='utf-8') as fh:
        data = json.load(fh)
    dec = decisions(data)

    in_fp = {k: v for k, v in dec.items() if (k[1], k[2]) in FOOTPRINT}
    oof = {k: v for k, v in dec.items() if (k[1], k[2]) not in FOOTPRINT}

    if args.oof:
        print('masked-only decisions on (region, source) pairs OUTSIDE every ledger hunt')
        print('(the hunt list was derived from the SOLE view, so an all-masked pair never')
        print(' became a hunt at all -- this is the same blind spot one level up)\n')
        tab = collections.Counter()
        for (slug, reg, sid), d in sorted(oof.items(), key=lambda kv: (kv[0][1], kv[0][2])):
            if d['sole']:
                continue
            cls, decl = classify(data, slug, reg, sid, d['paths'])
            tab[cls] += 1
            print(f'  {cls:18} {slug:22} {reg:16} bare={sid:22} nodes={len(d["paths"])}')
        print('\n ', dict(tab.most_common()),
              ' total', sum(tab.values()))
        return 0

    if args.classify or args.neither:
        tab = collections.Counter()
        by_camp = collections.defaultdict(collections.Counter)
        for (slug, reg, sid), d in sorted(in_fp.items()):
            if d['sole']:
                continue
            hunt, camp = campaign_of(reg, sid, slug)
            cls, decl = classify(data, slug, reg, sid, d['paths'])
            tab[cls] += 1
            by_camp[camp][cls] += 1
            if args.neither and cls == 'NEITHER':
                print(f'  {camp:10} #{hunt:<3} {slug:22} {reg:16} bare={sid:18} '
                      f'nodes={len(d["paths"])}')
        print()
        for cls, n in tab.most_common():
            print(f'  {cls:18} {n:4}')
        for camp in sorted(by_camp):
            print(f'  {camp:12}', dict(by_camp[camp]))
        print(f'\n  masked-only decisions in footprint: {sum(tab.values())}')
        return 0

    # default: per-hunt table, zero-row hunts printed loudly
    by_hunt = collections.defaultdict(collections.Counter)
    camp_dec = collections.defaultdict(lambda: {'sole': set(), 'maskonly': set()})
    for (slug, reg, sid), d in in_fp.items():
        hunt, camp = campaign_of(reg, sid, slug)
        cls = 'sole' if d['sole'] else 'maskonly'
        by_hunt[(hunt, camp)][cls] += 1
        by_hunt[(hunt, camp)]['sole_n'] += d['sole']
        by_hunt[(hunt, camp)]['masked_n'] += d['masked']
        camp_dec[camp][cls].add((slug, reg, sid))

    print(f'{"hunt":>5} {"campaign":10} {"region":16} {"source_id":18} '
          f'{"SOLE-dec":>8} {"MASKONLY":>9} {"sole-n":>7} {"masked-n":>9}')
    print('-' * 92)
    for (reg, sid), (hunt, camp) in sorted(FOOTPRINT.items(), key=lambda kv: kv[1][0]):
        keys = [k for k in by_hunt if k[0] == hunt]
        if not keys:
            print(f'{hunt:>5} {camp:10} {reg:16} {sid:18} '
                  f'{"ZERO ROWS -- fixed and filtered-away render identically; say so":>40}')
            continue
        for k in sorted(keys, key=lambda x: str(x[1])):
            c = by_hunt[k]
            print(f'{hunt:>5} {k[1]:10} {reg:16} {sid:18} '
                  f'{c["sole"]:>8} {c["maskonly"]:>9} {c["sole_n"]:>7} {c["masked_n"]:>9}')
    print('-' * 92)
    allm = set()
    for camp in sorted(camp_dec):
        s, m = camp_dec[camp]['sole'], camp_dec[camp]['maskonly']
        if camp != 'withdrawn':
            allm |= m
        print(f'  {camp:12} SOLE-visible {len(s):4}   MASKED-ONLY {len(m):4}')
    print(f'\n  MASKED-ONLY decisions across the four campaigns (excl. withdrawn): '
          f'{len(allm)} over {len({k[0] for k in allm})} crops')
    print('  A count of masked rows is NOT a count of defects until some are read:')
    print('  run --classify, and see docs/2026-08-10-pla187-masked-population-measured.md')
    return 0


if __name__ == '__main__':
    sys.exit(main())
