#!/usr/bin/env python3
"""RE-PRICE campaign B (kickoff 51 task one): the honest open number for the two region templates.

READ-ONLY on canonical. NOT a gate, NOT a promote. Companion to
tools/citation_provenance_scan.py, which stays the authority for what the DATA says. This tool
answers the different question the ledger exists to ask -- **how much of that is already
adjudicated** -- and it derives the answer per NODE against a named piece of evidence, so no
number here rests on a prose snapshot that can go stale.

WHY IT IS NODE-LEVEL AND CLASS-AWARE. The scan's unit is the (crop, region, source) DECISION,
which is the right unit for planning a document hunt and the wrong one for pricing it: a decision
counts as open if any single node under it is unadjudicated, including a `plantings[]` container
root that carries no claim at all. So every node is split two ways first:

  CLAIM arm    bloom / plant_out / harvest_start / harvest_end -- a specific quantity that some
               document either publishes or does not. Adjudication is meaningful here.
  CONTAINER    a `plantings[]` root or a `resolved_by_zone.<z>` root. These carry the region's
               provenance anchor, not a datum. Repointing one asks which document represents the
               region's planting model, which is NOT the same question and must not be priced as
               though it were.

WHAT IT CORRECTS, which is the reason it exists. Kickoff 51 s2 states that "27 bloom arms are
covered by accepted findings" and "34 harvest arms were left bare ON PURPOSE by hunt 1". Measured
here: **21 of 27** and **20 of 34**. That is the [[stale-records-commission-phantom-work]] shape
sitting inside a "do NOT redo this" heading, and the three causes are each worth naming:

  - The 13 crops the kickoff lists carry `mid_south_bloom_offset_undocumented`. The mid_atlantic
    finding is a SEPARATE record over a DIFFERENT 10-crop set, two of whose crops (apple, pawpaw)
    own no bare mid_atlantic bloom node at all. One roster was read as covering both regions.
    apricot, cherry-sour, cherry-sweet and pomegranate have NO mid_atlantic finding.
  - strawberry owns 2 mid_south bloom arms and carries no mid_south finding whatsoever.
  - Hunt 1 was a mid_south/UAEX hunt, so it cannot have adjudicated NC State's publications:
    mid_atlantic's 8 harvest arms were never in its scope. Within mid_south its stated exclusion
    names neither fig's harvest (fig is excluded for PLANTING, as contradicted) nor strawberry's.

    $ python3 tools/campaign_b_reprice.py
    $ python3 tools/campaign_b_reprice.py --nodes    # itemize every node and its verdict
"""
import argparse
import collections
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))
from bare_host_scan import scan  # noqa: E402

CANONICAL = os.path.join(REPO, 'crops_data_final.json')

HUNTS = (('mid_south', 'uada_ext'), ('mid_atlantic', 'ncsu_ext'))
CLAIM_ARMS = ('bloom', 'plant_out', 'harvest_start', 'harvest_end')

# --- the adjudication record, transcribed with its source ------------------------------------
# Where the evidence is a filed finding, the rule fires only if that finding is PRESENT ON THAT
# CROP -- which is exactly the check the kickoff's prose skipped.

BLOOM_FINDING = {
    'mid_south': 'mid_south_bloom_offset_undocumented',
    'mid_atlantic': 'mid_atlantic_bloom_offset_undocumented',
}

# tools/promote_mid_south_fruit_tree_repoint.py docstring, "WHAT IS DELIBERATELY *NOT* REPOINTED":
#   "harvest ... Left on the bare host for apple (already pathed to ext_org_apples), and for
#    apricot / cherry / mulberry / peach / pear / plum / pomegranate, because UAEX publishes NO
#    harvest dates for them. FSA6129 has no plum section at all and gives peach/nectarine only a
#    relative 'days before Elberta' ladder with no anchor date."
# nectarine rides that last sentence. fig and strawberry are named NOWHERE in it.
HUNT1_HARVEST_EXCLUDED = {
    'apple', 'apricot', 'cherry-sour', 'cherry-sweet', 'mulberry', 'nectarine',
    'peach', 'pear-asian', 'pear-european', 'plum', 'pomegranate',
}

# same docstring: "pawpaw plant_out is 'Spring (potted, from container)', a container claim the
# page's bare-root/late-winter sentence does not make. Its HARVEST is repointed; its planting is
# not."
HUNT1_PLANT_OUT_EXCLUDED = {'pawpaw'}

# docs/2026-07-30-mid-south-uada-ext-citation-hunt.md, the verdict table:
#   "DECLARED / UNVERIFIABLE -- no such document exists, and the crop already says so |
#    oregano, rosemary, sage, thyme"
# Verified below against each crop's OWN pilot findings rather than taken on the table's word.
HERB_DECLARED = {'oregano', 'rosemary', 'sage', 'thyme'}
DECLARED_RE = re.compile(r'are MODELED|are modeled|modeled from|windows are modeled', re.I)


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


def finding_status(crop, fid):
    for f in findings(crop):
        if f.get('id') == fid:
            return f.get('status', '?')
    return None


def declares_modeled(crop):
    return [f.get('id') for f in findings(crop)
            if DECLARED_RE.search(f.get('summary', '') or '')]


def adjudicate(slug, crop, region, arm):
    """-> (verdict, evidence). Verdicts: RULED, DECLARED, OPEN."""
    if arm == 'bloom':
        # Two shapes are equally binding: the ROSTER-WIDE ruling, and a CROP-SCOPED one filed
        # because that crop was outside the roster ruling's set. strawberry is the second shape
        # (`strawberry_mid_south_bloom_offset_undocumented`, filed 2026-08-03) -- it owns bloom
        # arms but was never in the 13-crop mid_south roster. Checking only the roster id told the
        # next session strawberry still needed document work AFTER it had been adjudicated, which
        # is the stale-record trap this whole tool exists to stop.
        for fid in (BLOOM_FINDING[region], '%s_%s' % (slug, BLOOM_FINDING[region])):
            st = finding_status(crop, fid)
            if st is not None:
                return 'RULED', '%s [%s]' % (fid, st)
        return 'OPEN', 'no %s (roster or crop-scoped) on this crop' % BLOOM_FINDING[region]
    if arm in ('harvest_start', 'harvest_end'):
        if region == 'mid_south' and slug in HUNT1_HARVEST_EXCLUDED:
            return 'RULED', 'hunt 1 stated exclusion (UAEX publishes no harvest dates)'
        if region == 'mid_atlantic':
            return 'OPEN', 'hunt 1 was mid_south/UAEX; never adjudicated NC State'
        return 'OPEN', 'not named in hunt 1 exclusion'
    if arm == 'plant_out':
        if region == 'mid_south' and slug in HUNT1_PLANT_OUT_EXCLUDED:
            return 'RULED', 'hunt 1 stated exclusion (container claim not on the page)'
        return 'OPEN', 'no ruling covers this arm'
    if slug in HERB_DECLARED:
        ids = declares_modeled(crop)
        if ids:
            return 'DECLARED', 'crop declares modeled windows: %s' % ids[0]
    return 'OPEN', 'container node, no ruling'


def collect(data, crops):
    nodes = []
    for sid, slug, path, sole, url in scan(data):
        if not sole:
            continue
        reg = region_of(path)
        if (reg, sid) not in HUNTS:
            continue
        arm = arm_of(path)
        verdict, why = adjudicate(slug, crops[slug], reg, arm)
        nodes.append((reg, sid, slug, path, arm, url, verdict, why))
    return nodes


def bucket_of(ns):
    """Five classes, and the split between the last three is the whole point of the tool.

    A decision holding only CONTAINER nodes is not a claim hunt: nothing under it asserts a
    quantity a document could confirm or refute. Pricing `apple`'s lone `plantings[]` root as
    though it were `strawberry`'s twelve nodes is the same category error the arc keeps making
    one level up, where a citation count is read as a count of open questions.
    """
    claim = [n for n in ns if n[4] in CLAIM_ARMS]
    cont = [n for n in ns if n[4] not in CLAIM_ARMS]
    if all(n[6] == 'RULED' for n in ns):
        return 'CLOSED-BY-RULING'
    if cont and not claim and all(n[6] == 'DECLARED' for n in cont):
        return 'DECLARED'
    if claim and all(n[6] == 'RULED' for n in claim):
        return 'CONTAINER-ONLY RESIDUE'
    if not claim:
        # unruled, but the open question is "which document represents this region's planting
        # model", not "what supports this date". Cheaper, and a different kind of answer.
        return 'OPEN -- container only (region anchor)'
    return 'OPEN -- needs document work'


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
        dec[(n[2], n[0], n[1])].append(n)

    print('=' * 96)
    print('CAMPAIGN B RE-PRICE -- %d SOLE nodes over %d decisions, 2 hunts' % (
        len(nodes), len(dec)))
    print('=' * 96)

    # -- the URL pin. Campaign A's pear lesson: never read the bare URL from a global map.
    print('\nBARE URL PINNED PER DECISION (campaign A pear lesson):')
    per_dec = collections.defaultdict(set)
    for reg, sid, slug, _p, _a, url, _v, _w in nodes:
        per_dec[(slug, reg, sid)].add(url)
    by_hunt = collections.defaultdict(collections.Counter)
    for (slug, reg, sid), us in per_dec.items():
        for u in us:
            by_hunt[(reg, sid)][u] += 1
    for (reg, sid), c in sorted(by_hunt.items()):
        for u, n in c.most_common():
            print('   %-13s %-11s %-34s %3d decisions' % (reg, sid, u, n))
    split = {k: sorted(v) for k, v in per_dec.items() if len(v) > 1}
    print('   decisions citing MORE THAN ONE bare url: %d  %s' % (
        len(split), split or '-- none; the map is safe HERE, unlike campaign A --'))

    print('\nNODE CLASS:')
    cls = collections.Counter('CLAIM' if n[4] in CLAIM_ARMS else 'CONTAINER' for n in nodes)
    for k in ('CLAIM', 'CONTAINER'):
        print('   %-10s %4d' % (k, cls[k]))

    print('\nVERDICT BY CLAIM ARM (where adjudication is meaningful):')
    print('   %-14s %6s %6s %6s' % ('arm', 'nodes', 'RULED', 'OPEN'))
    print('   ' + '-' * 36)
    for arm in CLAIM_ARMS:
        sub = [n for n in nodes if n[4] == arm]
        c = collections.Counter(n[6] for n in sub)
        print('   %-14s %6d %6d %6d' % (arm, len(sub), c['RULED'], c['OPEN']))
    claim = [n for n in nodes if n[4] in CLAIM_ARMS]
    cc = collections.Counter(n[6] for n in claim)
    print('   ' + '-' * 36)
    print('   %-14s %6d %6d %6d' % ('TOTAL', len(claim), cc['RULED'], cc['OPEN']))

    print('\nWHAT KICKOFF 51 s2 CLAIMS vs WHAT IS TRUE:')
    bloom = [n for n in nodes if n[4] == 'bloom']
    harv = [n for n in nodes if n[4].startswith('harvest')]
    print('   bloom arms covered by an accepted finding: claimed 27 of 27, ACTUAL %d of %d' % (
        sum(1 for n in bloom if n[6] == 'RULED'), len(bloom)))
    for n in sorted(bloom, key=lambda n: (n[0], n[2])):
        if n[6] != 'RULED':
            print('      UNCOVERED  %-14s %-13s %s' % (n[2], n[0], n[7]))
    print('   harvest arms answered by hunt 1:           claimed 34 of 34, ACTUAL %d of %d' % (
        sum(1 for n in harv if n[6] == 'RULED'), len(harv)))
    for (slug, reg), c in sorted(collections.Counter(
            (n[2], n[0]) for n in harv if n[6] != 'RULED').items()):
        print('      UNCOVERED  %-14s %-13s %d nodes' % (slug, reg, c))

    print('\nDECISION-LEVEL VERDICT (the ledger unit):')
    buckets = collections.defaultdict(list)
    for key, ns in dec.items():
        buckets[bucket_of(ns)].append((key, len(ns)))
    order = ['CLOSED-BY-RULING', 'DECLARED', 'CONTAINER-ONLY RESIDUE',
             'OPEN -- container only (region anchor)', 'OPEN -- needs document work']
    for b in order:
        rows = sorted(buckets.get(b, []))
        if not rows:
            continue
        print('   %-28s %2d decisions, %3d nodes' % (
            b, len(rows), sum(n for _k, n in rows)))
        for (slug, reg, _sid), n in rows:
            print('        %-16s %-13s %2d nodes' % (slug, reg, n))

    # self-checks: nothing may leak between buckets or classes
    assert sum(len(v) for v in buckets.values()) == len(dec), 'decision bucket leak'
    assert sum(len(v) for v in dec.values()) == len(nodes), 'node leak'
    assert cls['CLAIM'] + cls['CONTAINER'] == len(nodes), 'class leak'
    def tally(b):
        rows = buckets.get(b, [])
        return len(rows), sum(n for _k, n in rows)

    hd, hn = tally('OPEN -- needs document work')
    cd, cn = tally('OPEN -- container only (region anchor)')
    print('\n   HONEST OPEN, document work : %2d of %d decisions, %3d of %d nodes'
          % (hd, len(dec), hn, len(nodes)))
    print('   plus region-anchor only    : %2d of %d decisions, %3d of %d nodes'
          % (cd, len(dec), cn, len(nodes)))
    print('   ledger carries 33; %d are closed, declared or claim-adjudicated already.'
          % (len(dec) - hd - cd))

    if args.nodes:
        print('\nEVERY NODE:')
        for reg, _s, slug, _p, arm, _u, v, why in sorted(nodes, key=lambda n: (n[0], n[2], n[4])):
            print('   %-13s %-15s %-14s %-9s %s' % (reg, slug, arm, v, why[:50]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
