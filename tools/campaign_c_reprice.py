#!/usr/bin/env python3
"""RE-PRICE campaign C (kickoff 53 task one): the honest open number for arid + Texas.

READ-ONLY on canonical. NOT a gate, NOT a promote. Sibling of tools/campaign_b_reprice.py,
same unit and same discipline: every adjudication claim is asserted PRESENT ON THAT CROP
mechanically, so no number here rests on a prose snapshot that can go stale.

WHAT IT CORRECTS, and it is the reason the tool exists. Kickoff 53 s2 states, under a heading
telling the next session not to expect a collapse:

    "Measured 2026-08-04: 0 of 35 decisions carry any finding naming their region. Nothing here
     is pre-ruled. Do not expect a B-style collapse from reclassification -- C's 35 is real work."

That measurement is REPRODUCIBLE and still true on canonical 5a52a76c -- and it is the wrong
test. Campaign C's crops do not declare their bare anchors by REGION. They declare them by
SOURCE ID, in a crop-scoped pilot finding filed at certification:

    okra_pilot_region_anchor_base_urls [accepted]
      "Several region-rep source anchors (umn_ext, umaine_ext, ucanr_ext, uc_mg, nmsu_ext,
       tamu_agrilife, uariz_ext, uf_ifas_vh021, uhawaii_ctahr) use the institution/publication
       BASE URL rather than a live okra-specific page..."

That finding names three of campaign C's five source ids and adjudicates three of its decisions.
Searching for the string "warm_arid" would never find it. Measured here: **17 of 35 decisions
already carry a crop-scoped finding naming the hunt's own source id** -- the [[stale-records-
commission-phantom-work]] shape again, inverted: not a stale record commissioning work that is
done, but a too-narrow TEST hiding work that is already adjudicated.

WHY LOOSE MATCHING IS VERIFIED, NOT ASSUMED. Half those findings name the institution in prose
("uga_ext, ucanr, uc_mg, nmsu, tamu, umd, iastate") rather than the catalog id. "nmsu" covers
`nmsu_ext` only if `nmsu_ext` is the ONLY nmsu-family id that crop cites -- so the tool checks
that against the data and REFUSES the match when it is ambiguous. That check earns its keep
three times over:

  - snow-peas / sugar-snap-peas / broad-beans-fava cite BOTH `tamu_agrilife` and
    `tamu_agrilife_fall_veg`, and their findings name only the `_fall_veg` PDF. The bare
    `tamu_agrilife` rows those crops carry are NOT adjudicated by it.
  - beefsteak-tomato and heirloom-tomato cite BOTH `nmsu_ext` and `nmsu_donaana_mg`; hunt #17
    is the Dona Ana one, and heirloom's finding says only "NMSU".
  - shallot's one tamu finding is `shallot_pink_root_tamu_pdf` -- a DISEASE anchor. Right
    institution, wrong claim ([[right-document-wrong-claim]]).

    $ python3 tools/campaign_c_reprice.py
    $ python3 tools/campaign_c_reprice.py --nodes    # itemize every node and its verdict
"""
import argparse
import collections
import json
import os
import re
import sys
from urllib.parse import urlsplit

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))
from bare_host_scan import scan  # noqa: E402

CANONICAL = os.path.join(REPO, 'crops_data_final.json')
BARE = re.compile(r'https?://[^/]+/?$')

# The seven hunts, from docs/citation_arc_hunt_ledger.md's campaign table.
HUNTS = {
    ('warm_arid', 'nmsu_ext'): 7,
    ('warm_arid', 'tamu_agrilife'): 8,
    ('rgv', 'tamu_agrilife'): 13,
    ('low_desert_az', 'uariz_ext'): 14,
    ('warm_arid', 'nmsu_donaana_mg'): 17,
    ('ca_desert', 'uariz_ext'): 21,
    ('warm_arid', 'nmsu_chart'): 24,
}
CLAIM_ARMS = ('bloom', 'plant_out', 'harvest_start', 'harvest_end')

# Kickoff 53 s4a: lemon and lime move to campaign D (hunt #21 is 100% citrus; D is already
# 7-of-11 lemon and holds campaign A's deferred citrus). Reported separately, never silently
# dropped -- a campaign that shrinks by hiding rows is the failure mode this arc keeps hitting.
CITRUS = {'lemon', 'lime'}

# --- the adjudication table, transcribed with its evidence ------------------------------------
# (region, slug, source_id) -> finding id. Every entry is verified PRESENT ON THAT CROP and
# verified to NAME this source id (strictly, or via an institution alias proven unambiguous
# against the crop's own citations) before it fires. A table asserting an adjudication the data
# no longer carries is the exact failure being guarded against.
#
# All of these are ANCHOR-CLASS findings: their subject is that the citation is an institution
# portal / base URL rather than a document. That is the same question the bare-host triage asks,
# which is what makes them adjudications rather than background.
ANCHOR_FINDING = {
    ('warm_arid', 'acorn-squash', 'nmsu_ext'): 'acorn_pilot_regional_source_anchors_general',
    ('warm_arid', 'acorn-squash', 'tamu_agrilife'): 'acorn_pilot_regional_source_anchors_general',
    ('warm_arid', 'banana-pepper', 'nmsu_ext'):
        'banana_pepper_pilot_regional_source_anchors_general',
    ('warm_arid', 'banana-pepper', 'tamu_agrilife'):
        'banana_pepper_pilot_regional_source_anchors_general',
    ('warm_arid', 'bell-pepper', 'nmsu_ext'): 'bell_pepper_pilot_regional_source_anchors_general',
    ('warm_arid', 'bell-pepper', 'tamu_agrilife'):
        'bell_pepper_pilot_regional_source_anchors_general',
    ('warm_arid', 'butternut-squash', 'nmsu_ext'):
        'butternut_pilot_regional_source_anchors_general',
    ('warm_arid', 'butternut-squash', 'tamu_agrilife'):
        'butternut_pilot_regional_source_anchors_general',
    ('warm_arid', 'cayenne-pepper', 'nmsu_ext'): 'cayenne_pilot_regional_source_anchors_general',
    ('warm_arid', 'eggplant', 'nmsu_ext'): 'eggplant_pilot_regional_source_anchors_general',
    ('warm_arid', 'eggplant', 'tamu_agrilife'): 'eggplant_pilot_regional_source_anchors_general',
    ('warm_arid', 'okra', 'nmsu_ext'): 'okra_pilot_region_anchor_base_urls',
    ('warm_arid', 'okra', 'tamu_agrilife'): 'okra_pilot_region_anchor_base_urls',
    ('low_desert_az', 'okra', 'uariz_ext'): 'okra_pilot_region_anchor_base_urls',
    ('warm_arid', 'spaghetti-squash', 'nmsu_ext'):
        'spaghetti_pilot_regional_source_anchors_general',
    ('warm_arid', 'spaghetti-squash', 'tamu_agrilife'):
        'spaghetti_pilot_regional_source_anchors_general',
    ('rgv', 'arugula', 'tamu_agrilife'): 'arugula_pilot_regional_source_urls',
    # Filed 2026-08-05 by the campaign C closeout promote. pumpkin was the only crop in its
    # sibling set of six without this record, which is why the identical citation shape read as
    # unadjudicated on pumpkin and as declared on acorn/butternut/spaghetti/bell-pepper/eggplant.
    ('warm_arid', 'pumpkin', 'nmsu_ext'): 'pumpkin_pilot_regional_source_anchors_general',
    ('warm_arid', 'pumpkin', 'tamu_agrilife'): 'pumpkin_pilot_regional_source_anchors_general',
}

# CASE 2 ADJUDICATIONS filed by the campaign C closeout promote (2026-08-05). These are a
# DIFFERENT verdict from an anchor finding and must not be merged with it: an anchor finding says
# "the citation is a portal, and the real evidence is elsewhere"; these say "NO document publishes
# this window at all, measured across three named Rio Grande Valley documents". Both close the
# decision for document-hunting purposes, and they close it for opposite reasons, so the tool
# reports them separately. Before this promote all six read OPEN, and the declaration existed only
# in each cell's own synthesis_note_seasoned where no scan looks.
ABSENCE_FINDING = {
    ('rgv', 'arugula'): 'rgv_arugula_absent_from_rgv_planting_tables',
    ('rgv', 'broad-beans-fava'): 'rgv_fava_absent_from_rgv_planting_tables',
    ('rgv', 'shallot'): 'rgv_shallot_absent_from_rgv_planting_tables',
    ('rgv', 'snow-peas'): 'rgv_snow_peas_absent_from_rgv_planting_tables',
    ('rgv', 'sugar-snap-peas'): 'rgv_sugar_snap_peas_absent_from_rgv_planting_tables',
    # garlic is the split case: its plant_out repointed to a real document, and what stays bare
    # is the harvest pair, whose finding records that our Apr 13 start runs ahead of every source.
    ('rgv', 'garlic'): 'rgv_garlic_harvest_start_runs_ahead_of_every_source',
    # Filed 2026-08-05 by the AZ1005 follow-up. watermelon's two remaining low_desert_az nodes are
    # its second_planting pair, held bare ON PURPOSE: AZ1005 gives low-desert watermelon a spring
    # sowing window only (S at Feb 15, Mar 1, Mar 15 and nothing else all year), so repointing
    # them would cite a document that contradicts them. cantaloupe and honeydew-melon left this
    # scan entirely in the same pass.
    ('low_desert_az', 'watermelon'):
        'low_desert_az_watermelon_summer_planting_absent_from_az1005',
}

# MODELED-CLASS findings: they declare the region's WINDOWS derived from days-to-maturity plus
# frost anchors rather than lifted from a chart. That answers "what supports this date" (CASE 2,
# already filed) but says nothing about the citation being a portal, so it does NOT close an
# anchor decision. Tracked separately so the two kinds of debt never conflate -- the same split
# campaign_b_reprice draws between a RULED arm and an open ruling.
MODELED_FINDING = {
    'acorn-squash': 'acorn_pilot_regional_calendars_modeled',
    'banana-pepper': 'banana_pepper_pilot_regional_calendars_modeled',
    'bell-pepper': 'bell_pepper_pilot_regional_calendars_modeled',
    'butternut-squash': 'butternut_pilot_regional_calendars_modeled',
    'cantaloupe': 'cantaloupe_pilot_regional_calendars_modeled',
    'cayenne-pepper': 'cayenne_pilot_regional_calendars_modeled',
    'eggplant': 'eggplant_pilot_regional_calendars_modeled',
    'honeydew-melon': 'honeydew_pilot_regional_calendars_modeled',
    'okra': 'okra_pilot_regional_calendars_modeled',
    'pumpkin': 'pumpkin_pilot_regional_calendars_modeled',
    'spaghetti-squash': 'spaghetti_pilot_regional_calendars_modeled',
    'watermelon': 'watermelon_pilot_regional_calendars_modeled',
    'arugula': 'arugula_pilot_regional_calendars_modeled',
    'heirloom-tomato': 'heirloom_tomato_pilot_finding_001',
}

# Institution aliases, ENUMERATED not derived: a finding may say "nmsu" where the citation is
# `nmsu_ext`. The prefix is only accepted when the crop cites exactly one id under it -- see
# `alias_is_unambiguous`. Deriving this map from the ids in the data would make the check
# incapable of failing ([[guard-derived-from-what-it-checks-is-vacuous]]).
INSTITUTION_PREFIX = {
    'nmsu_ext': 'nmsu',
    'nmsu_donaana_mg': 'nmsu',
    'nmsu_chart': 'nmsu',
    'tamu_agrilife': 'tamu',
    'uariz_ext': 'uariz',
}
ALIAS_RE = {'nmsu': re.compile(r'\bnmsu\b', re.I),
            'tamu': re.compile(r'\btamu\b', re.I),
            'uariz': re.compile(r'\buariz\b', re.I)}


def region_of(path):
    m = re.match(r'regions\.([a-z0-9_]+)\.', path)
    return m.group(1) if m else '<crop-level>'


def arm_of(path):
    tail = re.sub(r'^regions\.[a-z0-9_]+\.', '', path)
    for k in CLAIM_ARMS:
        if '.%s[' % k in tail:
            return k
    if tail.startswith('resolved_by_zone.'):
        return 'heat_pause' if 'heat_pause' in tail else 'resolved_by_zone'
    if tail.startswith('plantings['):
        return 'plantings'
    return 'OTHER'


def findings(crop):
    return [f for f in ((crop.get('verification_status') or {}).get('open_findings') or [])
            if isinstance(f, dict)]


def finding(crop, fid):
    for f in findings(crop):
        if f.get('id') == fid:
            return f
    return None


def blob(f):
    return ' '.join(str(f.get(k, '')) for k in ('id', 'summary', 'detail', 'resolution', 'note'))


def cited_ids(crop):
    """Every source id this crop cites in any anchoring_urls block."""
    got = set()

    def walk(n):
        if isinstance(n, dict):
            a = n.get('anchoring_urls')
            if isinstance(a, dict):
                got.update(a)
            for k, v in n.items():
                if k != 'anchoring_urls':
                    walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)

    walk(crop)
    return got


def alias_is_unambiguous(crop, sid):
    """"nmsu" names `nmsu_ext` only if no OTHER nmsu-family id is cited by this crop.

    Returns (ok, competing_ids). This is the check that keeps the peas and the tomatoes open.
    """
    prefix = INSTITUTION_PREFIX.get(sid)
    if prefix is None:
        return False, []
    competing = sorted(i for i in cited_ids(crop)
                       if i != sid and i.lower().startswith(prefix))
    return (not competing), competing


def names_source(crop, f, sid):
    """-> (matched, mode, detail). STRICT = the finding names the catalog id verbatim."""
    text = blob(f)
    if re.search(r'\b%s\b' % re.escape(sid), text):
        return True, 'STRICT', 'names `%s`' % sid
    prefix = INSTITUTION_PREFIX.get(sid)
    if prefix and ALIAS_RE[prefix].search(text):
        ok, competing = alias_is_unambiguous(crop, sid)
        if ok:
            return True, 'ALIAS', 'says "%s"; sole %s-family id on this crop' % (prefix, prefix)
        return False, 'AMBIGUOUS', 'says "%s" but crop also cites %s' % (prefix, competing)
    return False, 'NONE', 'does not name %s' % sid


def catalog_repointable(catalog, sid, url):
    """The node cites a domain root while source_catalog already knows a DOCUMENT for that id.

    A mechanical CASE 1 repoint: no hunt, the document is already named inside the repo.
    """
    cu = (catalog.get(sid) or {}).get('url')
    return bool(cu and BARE.fullmatch(url) and not BARE.fullmatch(cu)), cu


def host(u):
    h = (urlsplit(u).hostname or '').lower()
    return h[4:] if h.startswith('www.') else h


def reg_host(u):
    p = host(u).split('.')
    return '.'.join(p[-2:]) if len(p) >= 2 else host(u)


def adjudicate(crop, region, slug, sid, url, catalog):
    """-> (verdict, evidence). One verdict per DECISION; findings here are crop+source scoped."""
    ok, cu = catalog_repointable(catalog, sid, url)
    if ok:
        flag = '' if reg_host(url) == reg_host(cu) else '  *** and the hosts DISAGREE ***'
        return 'CATALOG-REPOINTABLE', 'catalog knows %s%s' % (cu, flag)

    fid = ANCHOR_FINDING.get((region, slug, sid))
    if fid is not None:
        f = finding(crop, fid)
        if f is None:
            return 'OPEN', 'TABLE CLAIMS %s BUT IT IS NOT ON THIS CROP' % fid
        matched, mode, why = names_source(crop, f, sid)
        if not matched:
            return 'OPEN', '%s is present but %s' % (fid, why)
        return 'DECLARED-ANCHOR', '%s [%s] %s -- %s' % (fid, f.get('status'), mode, why)

    aid = ABSENCE_FINDING.get((region, slug))
    if aid is not None:
        f = finding(crop, aid)
        if f is None:
            return 'OPEN', 'ABSENCE table claims %s but it is NOT on this crop' % aid
        return 'DECLARED-ABSENCE', '%s [%s] no document publishes this window' % (
            aid, f.get('status'))

    mid = MODELED_FINDING.get(slug)
    if mid is not None and finding(crop, mid) is not None:
        f = finding(crop, mid)
        return 'MODELED-ONLY', '%s [%s] declares windows modeled; anchor id not adjudicated' % (
            mid, f.get('status'))
    return 'OPEN', 'no finding on this crop names %s' % sid


def collect(data, crops):
    catalog = data.get('source_catalog') or {}
    nodes = []
    for sid, slug, path, sole, url in scan(data):
        if not sole:
            continue
        reg = region_of(path)
        if (reg, sid) not in HUNTS:
            continue
        verdict, why = adjudicate(crops[slug], reg, slug, sid, url, catalog)
        nodes.append((HUNTS[(reg, sid)], reg, sid, slug, path, arm_of(path), url, verdict, why))
    return nodes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--nodes', action='store_true', help='itemize every node and its verdict')
    args = ap.parse_args()

    with open(CANONICAL, encoding='utf-8') as fh:
        data = json.load(fh)
    crops = {c['slug']: c for c in data['crops']}
    nodes = collect(data, crops)

    dec = collections.defaultdict(list)
    for n in nodes:
        dec[(n[3], n[1], n[2])].append(n)

    print('=' * 100)
    print('CAMPAIGN C RE-PRICE -- %d SOLE nodes over %d decisions, %d hunts'
          % (len(nodes), len(dec), len({n[0] for n in nodes})))
    print('=' * 100)

    print('\nBARE URL PINNED PER DECISION (campaign A pear lesson):')
    per_dec = collections.defaultdict(set)
    for n in nodes:
        per_dec[(n[3], n[1], n[2])].add(n[6])
    by_hunt = collections.defaultdict(collections.Counter)
    for (slug, reg, sid), us in per_dec.items():
        for u in us:
            by_hunt[(reg, sid)][u] += 1
    for (reg, sid), c in sorted(by_hunt.items()):
        for u, k in c.most_common():
            print('   %-14s %-17s %-46s %2d decisions' % (reg, sid, u, k))
    split = {k: sorted(v) for k, v in per_dec.items() if len(v) > 1}
    print('   decisions citing MORE THAN ONE bare url: %d  %s'
          % (len(split), split or '-- none; the map is safe HERE, unlike campaign A --'))

    print('\nNODE CLASS (kickoff 53 s3: price these separately or overstate C by ~3x):')
    cls = collections.Counter('CLAIM' if n[5] in CLAIM_ARMS else 'CONTAINER' for n in nodes)
    for k in ('CLAIM', 'CONTAINER'):
        print('   %-10s %4d' % (k, cls[k]))

    print('\nWHAT KICKOFF 53 s2 CLAIMS vs WHAT IS TRUE:')
    named_region = 0
    for (slug, reg, _sid), _ns in dec.items():
        if any(reg in (f.get('id') or '') for f in findings(crops[slug])):
            named_region += 1
    print('   decisions carrying a finding naming their REGION : %2d of %d  (kickoff: 0 of 35)'
          % (named_region, len(dec)))
    declared = sum(1 for ns in dec.values() if ns[0][7] == 'DECLARED-ANCHOR')
    print('   decisions carrying a finding naming their SOURCE : %2d of %d  <-- the right test'
          % (declared, len(dec)))

    print('\nDECISION-LEVEL VERDICT (the ledger unit):')
    buckets = collections.defaultdict(list)
    for key, ns in dec.items():
        buckets[ns[0][7]].append((key, len(ns), ns[0][8], ns[0][0]))
    order = ['CATALOG-REPOINTABLE', 'DECLARED-ANCHOR', 'DECLARED-ABSENCE', 'MODELED-ONLY',
             'OPEN']
    for b in order:
        rows = sorted(buckets.get(b, []), key=lambda r: (r[3], r[0]))
        if not rows:
            continue
        cn = sum(1 for k, _n, _w, _h in rows if k[0] in CITRUS)
        print('   %-20s %2d decisions, %3d nodes%s' % (
            b, len(rows), sum(n for _k, n, _w, _h in rows),
            '   (%d are lemon/lime -> campaign D)' % cn if cn else ''))
        for (slug, reg, _sid), n, why, h in rows:
            print('        #%-3d %-17s %-14s %2d nodes  %s' % (h, slug, reg, n, why[:62]))

    # -- the same table with citrus removed, which is the number campaign C actually owns
    print('\nAFTER THE KICKOFF 53 s4a RE-SCOPE (lemon + lime -> campaign D):')
    veg = {k: v for k, v in dec.items() if k[0] not in CITRUS}
    vnodes = [n for n in nodes if n[3] not in CITRUS]
    vb = collections.Counter(ns[0][7] for ns in veg.values())
    print('   campaign C keeps : %2d decisions, %3d nodes' % (len(veg), len(vnodes)))
    print('   campaign D takes : %2d decisions, %3d nodes'
          % (len(dec) - len(veg), len(nodes) - len(vnodes)))
    for b in order:
        if vb[b]:
            print('      %-20s %2d' % (b, vb[b]))

    open_dec = [k for k, v in veg.items() if v[0][7] == 'OPEN']
    open_nodes = [n for n in vnodes if n[7] == 'OPEN']
    open_claim = [n for n in open_nodes if n[5] in CLAIM_ARMS]
    print('\n   HONEST OPEN after re-scope : %2d of %d decisions, %3d of %d nodes'
          % (len(open_dec), len(veg), len(open_nodes), len(vnodes)))
    print('   of those open nodes        : %3d CLAIM arms, %3d containers'
          % (len(open_claim), len(open_nodes) - len(open_claim)))
    print('   ledger carries 35 decisions / 116 nodes for campaign C.')

    # -- self-checks: nothing may leak between buckets or classes
    assert sum(len(v) for v in buckets.values()) == len(dec), 'decision bucket leak'
    assert sum(len(v) for v in dec.values()) == len(nodes), 'node leak'
    assert cls['CLAIM'] + cls['CONTAINER'] == len(nodes), 'class leak'
    for key, ns in dec.items():
        assert len({n[7] for n in ns}) == 1, 'decision %s split across verdicts' % (key,)

    if args.nodes:
        print('\nEVERY NODE:')
        for h, reg, _sid, slug, path, arm, _u, v, why in sorted(nodes):
            print('   #%-3d %-17s %-14s %-16s %-20s %s'
                  % (h, slug, reg, arm, v, why[:48]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
