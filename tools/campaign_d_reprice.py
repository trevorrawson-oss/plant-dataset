#!/usr/bin/env python3
"""RE-PRICE campaign D (PLA-114 task one): the honest open number for the tail.

READ-ONLY on canonical. NOT a gate, NOT a promote. Sibling of tools/campaign_b_reprice.py
and tools/campaign_c_reprice.py, same unit and same discipline: every adjudication claim is
asserted PRESENT ON THAT CROP mechanically, so no number here rests on a prose snapshot.

WHAT IT CORRECTS -- THREE THINGS, and each is a different failure shape.

1. THE LEDGER UNDER-COUNTS D BY 12 DECISIONS. `docs/citation_arc_hunt_ledger.md` prices
   campaign D at "11 hunts / 14 decisions". That 14 is D's OWN 11 hunts only. It omits the
   citrus residue explicitly deferred INTO D by campaigns A and C -- lemon and lime rows under
   hunts #3, #4, #5, #6 (`ucanr_ext`), #8 (`tamu_agrilife`), #14 and #21 (`uariz_ext`). The
   ledger's own prose says those move here ("Residue: `lemon`, `lime` -> campaign D", seven
   times over); its campaign table just never added them to the number. Measured here:
   **26 decisions / 123 nodes**, not 14. A campaign that starts by under-counting itself is how
   the arc's earlier kickoffs went stale, so the residue is folded in and reported, never
   silently dropped.

2. PLA-114 ASKED FOR THREE VOCABULARIES TO BE TESTED SEPARATELY. Campaign C's kickoff measured
   "0 of 35 decisions carry a finding naming their REGION", which was reproducible and was the
   wrong test -- those crops declare by SOURCE ID. PLA-114 predicted D would repeat this, since
   D's work is citrus-shaped rather than region-shaped. So all three are measured and printed
   with their own counts, and a 0 is labelled TESTED rather than left to look like an oversight:

       V1 region-named finding
       V2 source-id-named finding (strict id, or a PROVEN-unambiguous institution alias)
       V3 per-cell prose (`plantings_provenance`, `synthesis_note_*`, `*_basis_seasoned`)

   The prediction half-held. V1 returns 0 and V2 returns 6 of 26 -- but the thing that actually
   collapses D is none of the three. See (3).

3. THE VERDICT THAT PRICES D IS **SIBLING-PATHED**, AND NO VOCABULARY SCAN WOULD HAVE FOUND IT.
   lemon's bare nodes are overwhelmingly cold-hardiness/suitability cells, not planting-date
   cells -- `resolved_by_zone.N` carrying `suitability` + `min_winter_temp_f`. For most of them
   the SAME region, the SAME zone, the SAME source id on a SIBLING CITRUS CROP already carries a
   PATHED document. lime's `northern_tier.resolved_by_zone.3` cites
   `hgic.clemson.edu/cold-tolerance-in-citrus/`; lemon's `northern_tier.resolved_by_zone.3`
   cites bare `hgic.clemson.edu`. Identical cell, identical claim, identical source id, one
   pathed and one bare. That is not a document hunt -- the document is already established
   inside the repo for the identical claim on the neighbouring crop.

   THIS IS A LEAD, NOT A VERDICT, AND THE TOOL SAYS SO. [[sibling-precedent-pressures-a-wrong-
   repoint]] is exactly this shape: 8 siblings citing one document pressured a repoint onto
   pomegranate, and NC State ch.15 turned out to have zero mentions of it. So SIBLING-PATHED
   means "a named document exists for this exact cell on a sibling, go read it", never "repoint
   it". The document read is still owed per hunt; what collapses is the SEARCH, not the
   verification.

WHY THE ALIAS CHECK IS KEPT (it fires here too). Campaign C's tool refuses an institution-alias
match when the crop cites more than one id in that family. Carried forward unchanged, and it
earns its keep once more: jalapeno's anchor finding says "ufifas" in prose, but jalapeno cites
BOTH `ufifas_ext` and `uf_ifas_vh021` -- two UF/IFAS ids -- so its `fl_peninsula` decision is
AMBIGUOUS and stays OPEN, while bell-pepper's names `ufifas_ext` verbatim and closes. Same
institution, same region, same claim, different verdicts, because one finding was specific and
the other was not.

    $ python3 tools/campaign_d_reprice.py
    $ python3 tools/campaign_d_reprice.py --nodes    # itemize every node and its verdict
    $ python3 tools/campaign_d_reprice.py --vocab    # the three-vocabulary detail, per decision
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

# Campaign D's OWN eleven hunts, from docs/citation_arc_hunt_ledger.md.
OWN_HUNTS = {
    ('ca_north_coast', 'ucanr_marin_mg'): 16,
    ('fl_peninsula', 'ufifas_ext'): 18,
    ('se_gulf', 'uga_ext'): 23,
    ('northern_tier', 'clemson_hgic'): 25,
    ('northern_tier', 'tamu_agrilife'): 26,
    ('se_gulf', 'tamu_agrilife'): 27,
    ('se_gulf', 'clemson_hgic'): 28,
    ('ca_interior', 'uc_ipm'): 29,
    ('warm_arid', 'uariz_ext'): 30,
    ('warm_arid', 'clemson_hgic'): 31,
    ('low_desert_az', 'ucanr_ext'): 32,
}

# The citrus residue DEFERRED INTO D by campaigns A and C. Each of these hunts is closed for its
# other crops and stayed PARTIAL on lemon/lime alone; the ledger's note column says so per row.
# Only the citrus rows belong to D -- the rest were settled by A and C and must not be re-counted.
RESIDUE_HUNTS = {
    ('ca_interior', 'ucanr_ext'): 3,
    ('ca_north_coast', 'ucanr_ext'): 4,
    ('ca_south_coast', 'ucanr_ext'): 5,
    ('ca_desert', 'ucanr_ext'): 6,
    ('warm_arid', 'tamu_agrilife'): 8,
    ('low_desert_az', 'uariz_ext'): 14,
    ('ca_desert', 'uariz_ext'): 21,
}
HUNTS = dict(OWN_HUNTS)
HUNTS.update(RESIDUE_HUNTS)
CITRUS = {'lemon', 'lime'}
CLAIM_ARMS = ('bloom', 'plant_out', 'harvest_start', 'harvest_end')

# Crops in the Citrus category, ENUMERATED not derived from the category field, so that a
# category rename cannot silently empty the sibling check.
CITRUS_SIBLINGS = ('lemon', 'lime', 'orange-navel', 'mandarin-clementine', 'grapefruit')

# --- the adjudication table, transcribed with its evidence ------------------------------------
# (region, slug, source_id) -> finding id. Every entry is verified PRESENT ON THAT CROP and
# verified to NAME this source id before it fires, exactly as campaign C's table is.
ANCHOR_FINDING = {
    # Names ucanr_marin_mg verbatim in a list of anchors that "were NOT independently
    # WebFetch-verified for edamame this session and are section/portal-level".
    ('ca_north_coast', 'edamame', 'ucanr_marin_mg'): 'edamame_pilot_regional_source_urls',
    # Names ufifas_ext VERBATIM -- "(ucanr_ext time-planting, uga_c963, nmsu_ext, tamu_agrilife,
    # ufifas_ext, uhawaii_ctahr) rather than a bell-pepper-specific regional planting-date page".
    ('fl_peninsula', 'bell-pepper', 'ufifas_ext'):
        'bell_pepper_pilot_regional_source_anchors_general',
    # Names uga_ext VERBATIM ("uga_ext, ucanr, uc_mg, nmsu, tamu, ufifas, uhawaii").
    ('se_gulf', 'jalapeno', 'uga_ext'): 'jalapeno_pilot_regional_source_anchors_general',
    # DELIBERATELY LISTED even though it does not close: the same jalapeno finding says only
    # "ufifas", and jalapeno cites two UF/IFAS ids, so the alias check refuses it. Listing it
    # makes the refusal visible in the output instead of looking like an omission.
    ('fl_peninsula', 'jalapeno', 'ufifas_ext'):
        'jalapeno_pilot_regional_source_anchors_general',
}

# MODELED-CLASS findings: they declare the region's WINDOWS (and, for lime, the per-cell
# SUITABILITY) derived rather than lifted from a chart. As in campaign C this answers "what
# supports this date", NOT "is the citation a portal", so it is reported separately and does
# not close an anchor decision.
MODELED_FINDING = {
    'lime': 'lime_pilot_finding_001',
    'edamame': 'edamame_pilot_regional_windows_modeled',
    'bell-pepper': 'bell_pepper_pilot_regional_calendars_modeled',
    'jalapeno': 'jalapeno_pilot_regional_calendars_modeled',
}

# OPEN-BY-RULING: an open finding that names this exact decision and states the next move.
# These are NOT closed -- they are open with a scoped answer, which is a different thing from
# an unexamined decision, and the difference is worth a bucket.
SCOPED_OPEN = {
    ('ca_north_coast', 'pear-asian'): 'pear_asian_ca_interior_homeorchard_root_repoint_candidate',
    ('ca_north_coast', 'pear-european'):
        'pear_european_ca_interior_homeorchard_root_repoint_candidate',
}

# Institution aliases, ENUMERATED not derived ([[guard-derived-from-what-it-checks-is-vacuous]]).
# NOTE the UF/IFAS family deliberately spans BOTH spellings -- `ufifas_ext` and `uf_ifas_*` are
# the same institution, so a finding saying "ufifas" does not disambiguate between them.
INSTITUTION_PREFIX = {
    'ufifas_ext': 'ufifas',
    'uga_ext': 'uga',
    'tamu_agrilife': 'tamu',
    'uariz_ext': 'uariz',
    'ucanr_ext': 'ucanr',
    'ucanr_marin_mg': 'ucanr',
    'uc_ipm': 'uc_',
    'clemson_hgic': 'clemson',
}
ALIAS_RE = {'ufifas': re.compile(r'\bu[f_]?\.?\s?ifas\b|\bufifas\b', re.I),
            'uga': re.compile(r'\buga\b', re.I),
            'tamu': re.compile(r'\btamu\b', re.I),
            'uariz': re.compile(r'\buariz\b', re.I),
            'ucanr': re.compile(r'\bucanr\b', re.I),
            'uc_': re.compile(r'\buc[ _]ipm\b', re.I),
            'clemson': re.compile(r'\bclemson\b', re.I)}
# Which cited ids count as "the same institution family" as the key. Spelling variants live
# here rather than in a startswith(), which is what makes the UF/IFAS ambiguity detectable.
FAMILY_RE = {'ufifas': re.compile(r'^uf_?ifas'), 'uga': re.compile(r'^uga'),
             'tamu': re.compile(r'^tamu'), 'uariz': re.compile(r'^uariz'),
             'ucanr': re.compile(r'^ucanr'), 'uc_': re.compile(r'^uc_'),
             'clemson': re.compile(r'^clemson')}

# V3's field list is ENUMERATED FROM THE SCHEMA, not from the fields that happen to carry an
# adjudication -- deriving it from the latter is what makes a vocabulary test vacuous. The first
# cut listed only the four `*_provenance` / `*_basis` fields and reported V3 = 3 of 26. That was
# an UNDER-SCOPED vocabulary reporting as a measured zero, which is precisely the failure PLA-114
# wrote this task to prevent. Widened to every prose field these cells actually carry, counted
# with `test_vocab_prose_sees_fields_even_where_it_finds_no_adjudication` as the floor.
PROSE_KEYS = ('plantings_provenance', 'planting_note', 'zone_notes', 'notes',
              'synthesis_note_seasoned', 'synthesis_note_beginner',
              'cold_basis_seasoned', 'cold_basis_beginner',
              'chill_basis_seasoned', 'chill_basis_beginner',
              'basis_seasoned', 'basis_beginner',
              'region_notes_seasoned', 'region_notes_beginner',
              'suitability_note_seasoned', 'suitability_note_beginner',
              'frost_risk_note_seasoned', 'frost_risk_note_beginner')


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
    """"ufifas" names `ufifas_ext` only if no OTHER UF/IFAS id is cited by this crop."""
    prefix = INSTITUTION_PREFIX.get(sid)
    if prefix is None:
        return False, []
    fam = FAMILY_RE[prefix]
    competing = sorted(i for i in cited_ids(crop) if i != sid and fam.match(i.lower()))
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


# --- the three vocabularies, each measured on its own ------------------------------------------

def vocab_region(crop, region):
    """V1: any finding on this crop naming this region."""
    return [f.get('id') for f in findings(crop) if region in blob(f)]


def vocab_source(crop, sid):
    """V2: any finding on this crop naming this source id (strict or proven alias)."""
    out = []
    for f in findings(crop):
        matched, mode, why = names_source(crop, f, sid)
        if matched:
            out.append((f.get('id'), mode, why))
    return out


def vocab_prose(crop, region, sid):
    """V3: per-cell prose on this region that names the source id or declares the basis."""
    reg = (crop.get('regions') or {}).get(region) or {}
    hits = []

    def check(where, val):
        if isinstance(val, str) and val.strip():
            hits.append((where, val))

    for k in PROSE_KEYS:
        check(k, reg.get(k))
    for z, cell in (reg.get('resolved_by_zone') or {}).items():
        if isinstance(cell, dict):
            for k in PROSE_KEYS:
                check('z%s.%s' % (z, k), cell.get(k))
            hp = cell.get('heat_pause')
            if isinstance(hp, dict):
                for k in PROSE_KEYS:
                    check('z%s.heat_pause.%s' % (z, k), hp.get(k))
    # A prose field ADJUDICATES only if it speaks to the SOURCING of the claim, not merely
    # states the claim. Two markers: it names the institution, or it declares the value modeled.
    prefix = INSTITUTION_PREFIX.get(sid)
    adjudicating = []
    for where, val in hits:
        named = bool(prefix and ALIAS_RE[prefix].search(val)) or bool(
            re.search(r'\b%s\b' % re.escape(sid), val))
        modeled = bool(re.search(r'\bmodel(?:ed|led)\b|\bderived\b|\bnot .{0,30}source-verified\b',
                                 val, re.I))
        if named or modeled:
            adjudicating.append((where, 'NAMES-SOURCE' if named else 'DECLARES-MODELED'))
    return hits, adjudicating


# --- the sibling check, which is what actually prices D ----------------------------------------

def pathed_by_sibling(crops, slug, path, sid):
    """Does a SIBLING citrus crop carry a PATHED url for this exact node path + source id?

    Not vacuous: it interrogates a DIFFERENT crop's data than the one being adjudicated, so it
    genuinely returns nothing when no sibling covers the cell. Verified by the fact that it
    returns nothing for several of D's decisions.
    """
    out = []
    for other in CITRUS_SIBLINGS:
        if other == slug or other not in crops:
            continue
        node = resolve(crops[other], path)
        if not isinstance(node, dict):
            continue
        a = node.get('anchoring_urls')
        if not isinstance(a, dict):
            continue
        m = a.get(sid)
        if isinstance(m, dict) and m.get('url') and not BARE.fullmatch(m['url']):
            out.append((other, m['url']))
    return out


def resolve(root, path):
    """Walk a scanner-emitted node path. `resolved_by_zone.3` has a NUMERIC DICT KEY.

    The first cut of this used `([A-Za-z_][A-Za-z0-9_]*)|\\[(\\d+)\\]`, which matches neither
    `3` nor `[0]`'s bare digit, so it silently DROPPED the zone component and returned the
    `resolved_by_zone` dict -- which carries no `anchoring_urls`, so every sibling lookup
    returned nothing and SIBLING-PATHED reported a clean, confident, WRONG zero. That is
    [[threshold-vs-calendar-check-family]] exactly: suspect your own parsing before believing
    a flood, or a drought. `assert_resolver_agrees_with_scanner` below is why it cannot recur.
    """
    cur = root
    for key, idx in re.findall(r'(?:\[(\d+)\]|([^.\[\]]+))', path):
        try:
            cur = cur[int(key)] if key else cur[idx]
        except (KeyError, IndexError, TypeError):
            return None
    return cur


def assert_resolver_agrees_with_scanner(crops, raw):
    """Every path the scanner emitted must resolve to a dict citing that source id.

    NOT vacuous and not derived from what it checks: `bare_host_scan.scan` builds its paths by
    an independent recursive walk, while `resolve` parses those paths back as strings. They can
    only agree if the parser is correct. This is the check that caught the numeric-key bug.
    """
    for _h, _reg, sid, slug, path, _arm, _url in raw:
        node = resolve(crops[slug], path)
        assert isinstance(node, dict), 'resolver lost %s :: %s' % (slug, path)
        anchors = node.get('anchoring_urls')
        assert isinstance(anchors, dict) and sid in anchors, (
            'resolver landed on the wrong node for %s :: %s (no %s)' % (slug, path, sid))


def catalog_repointable(catalog, sid, url):
    cu = (catalog.get(sid) or {}).get('url')
    return bool(cu and BARE.fullmatch(url) and not BARE.fullmatch(cu)), cu


def host(u):
    h = (urlsplit(u).hostname or '').lower()
    return h[4:] if h.startswith('www.') else h


def adjudicate(crops, crop, region, slug, sid, url, catalog, paths):
    """-> (verdict, evidence). One verdict per DECISION."""
    ok, cu = catalog_repointable(catalog, sid, url)
    if ok:
        return 'CATALOG-REPOINTABLE', 'catalog knows %s' % cu

    fid = ANCHOR_FINDING.get((region, slug, sid))
    if fid is not None:
        f = finding(crop, fid)
        if f is None:
            return 'OPEN', 'TABLE CLAIMS %s BUT IT IS NOT ON THIS CROP' % fid
        matched, mode, why = names_source(crop, f, sid)
        if matched:
            return 'DECLARED-ANCHOR', '%s [%s] %s -- %s' % (fid, f.get('status'), mode, why)
        # fall through to the sibling check; a refused alias is not an adjudication
        refused = '%s present but %s' % (fid, why)
    else:
        refused = None

    sib = []
    for p in paths:
        sib.extend((p, o, u) for o, u in pathed_by_sibling(crops, slug, p, sid))
    if sib:
        docs = sorted({u for _p, _o, u in sib})
        who = sorted({o for _p, o, _u in sib})
        return 'SIBLING-PATHED', '%d/%d nodes; %s cites %s' % (
            len({p for p, _o, _u in sib}), len(paths), '+'.join(who),
            ' + '.join(d[:58] for d in docs))

    sid_open = SCOPED_OPEN.get((region, slug))
    if sid_open is not None and finding(crop, sid_open) is not None:
        return 'OPEN-SCOPED', '%s [open] names the next move' % sid_open

    # A REFUSED ALIAS IS NOT A VERDICT, only a failure to close on V2, so it must not
    # short-circuit the remaining vocabularies. The first cut returned OPEN here and thereby
    # hid that jalapeno's fl_peninsula decision IS adjudicated -- in PROSE (V3), which is the
    # third vocabulary PLA-114 asked to be tested separately. Refusing on V2 and never asking
    # V3 is the same single-test mistake campaign C made with "0 of 35", one layer down.
    mid = MODELED_FINDING.get(slug)
    if mid is not None and finding(crop, mid) is not None:
        return 'MODELED-ONLY', '%s [%s] declares windows modeled; anchor id not adjudicated%s' % (
            mid, finding(crop, mid).get('status'),
            ' (V2 refused: %s)' % refused if refused else '')
    if refused:
        return 'OPEN', refused
    return 'OPEN', 'no finding on this crop names %s' % sid


def collect(data, crops):
    catalog = data.get('source_catalog') or {}
    raw = []
    for sid, slug, path, sole, url in scan(data):
        if not sole:
            continue
        reg = region_of(path)
        if (reg, sid) not in HUNTS:
            continue
        # residue hunts contribute their CITRUS rows only -- A and C settled the rest
        if (reg, sid) in RESIDUE_HUNTS and slug not in CITRUS:
            continue
        raw.append((HUNTS[(reg, sid)], reg, sid, slug, path, arm_of(path), url))

    assert_resolver_agrees_with_scanner(crops, raw)

    by_dec = collections.defaultdict(list)
    for r in raw:
        by_dec[(r[3], r[1], r[2])].append(r)

    nodes = []
    for (slug, reg, sid), rs in by_dec.items():
        paths = [r[4] for r in rs]
        verdict, why = adjudicate(crops, crops[slug], reg, slug, sid, rs[0][6], catalog, paths)
        for r in rs:
            nodes.append(r + (verdict, why))
    return nodes


def cell_view(crops, nodes):
    """Collapse node-CITATIONS to distinct physical CELLS.

    A `decision` is (crop, region, source_id) and a node-citation is (crop, path, source_id) --
    but ONE PHYSICAL CELL CAN CARRY TWO BARE SOURCE IDS, and then it is counted once per id.
    `lemon/warm_arid/plantings[0]` cites bare `uariz_ext` AND bare `clemson_hgic`, so it appears
    under hunt #30 and again under hunt #31. It is one cell and one authoring question.

    This is the arc's unit problem one level below the one campaign A already fixed: A corrected
    pairs -> decisions, and the decision unit still over-counts CELLS. Reported separately rather
    than replacing the decision count, because the ledger's unit is the decision.

    Returns (cells, split) where `split` are the cells whose two citations landed on DIFFERENT
    verdicts -- one arm has a document lead and the other does not. Those are the interesting
    ones: the cell is not settled until BOTH its citations are.
    """
    cells = collections.defaultdict(list)
    for h, _reg, sid, slug, path, _arm, _url, verdict, _why in nodes:
        cells[(slug, path)].append((h, sid, verdict))
    split = {k: v for k, v in cells.items() if len({x[2] for x in v}) > 1}
    return cells, split


def sibling_node_coverage(crops, nodes):
    """Per SIBLING-PATHED decision, how many of its nodes a sibling ACTUALLY covers.

    The decision-level verdict is driven by ANY node having a sibling document, which can mask a
    decision whose other nodes have none -- hunt #31 reads SIBLING-PATHED on the strength of one
    zone cell while its `plantings` container and `plant_out` arm have no lead at all. Without
    this the closeout would claim a document for work that has none.
    """
    out = {}
    for h, reg, sid, slug, path, _arm, _url, verdict, _why in nodes:
        if verdict != 'SIBLING-PATHED':
            continue
        key = (h, slug, reg, sid)
        covered, total = out.get(key, (0, 0))
        hit = bool(pathed_by_sibling(crops, slug, path, sid))
        out[key] = (covered + (1 if hit else 0), total + 1)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--nodes', action='store_true', help='itemize every node and its verdict')
    ap.add_argument('--vocab', action='store_true', help='the three-vocabulary detail')
    ap.add_argument('--cells', action='store_true',
                    help='collapse node-citations to distinct physical cells')
    args = ap.parse_args()

    with open(CANONICAL, encoding='utf-8') as fh:
        data = json.load(fh)
    crops = {c['slug']: c for c in data['crops']}
    nodes = collect(data, crops)

    dec = collections.defaultdict(list)
    for n in nodes:
        dec[(n[3], n[1], n[2])].append(n)

    print('=' * 100)
    print('CAMPAIGN D RE-PRICE -- %d SOLE nodes over %d decisions, %d hunts'
          % (len(nodes), len(dec), len({n[0] for n in nodes})))
    print('=' * 100)

    own = {k: v for k, v in dec.items() if (k[1], k[2]) in OWN_HUNTS}
    res = {k: v for k, v in dec.items() if (k[1], k[2]) in RESIDUE_HUNTS}
    print("\nWHAT THE LEDGER SAYS vs WHAT IS THERE:")
    print("   ledger's campaign table for D        : 11 hunts,  14 decisions")
    print("   D's own 11 hunts, measured           : %2d hunts,  %2d decisions, %3d nodes"
          % (len({k for k in OWN_HUNTS.values()}), len(own),
             sum(len(v) for v in own.values())))
    print("   citrus residue deferred in by A + C  : %2d hunts,  %2d decisions, %3d nodes"
          % (len({HUNTS[(k[1], k[2])] for k in res}), len(res),
             sum(len(v) for v in res.values())))
    print("   TRUE campaign D                      : %2d hunts,  %2d decisions, %3d nodes"
          % (len({n[0] for n in nodes}), len(dec), len(nodes)))
    print("   ^ the ledger's 14 omits the residue its OWN note column defers here seven times.")

    print('\nBARE URL PINNED PER DECISION (campaign A pear lesson):')
    per_dec = collections.defaultdict(set)
    for n in nodes:
        per_dec[(n[3], n[1], n[2])].add(n[6])
    split = {k: sorted(v) for k, v in per_dec.items() if len(v) > 1}
    by_host = collections.Counter(host(u) for us in per_dec.values() for u in us)
    for h, k in by_host.most_common():
        print('   %-34s %2d decisions' % (h, k))
    print('   decisions citing MORE THAN ONE bare url: %d  %s'
          % (len(split), split or '-- none; the map is safe here --'))

    print('\nWHAT CLASS OF CLAIM IS BARE (this is why D is not shaped like A/B/C):')
    cls = collections.Counter(n[5] for n in nodes)
    for k, v in cls.most_common():
        print('   %-18s %4d nodes' % (k, v))
    print('   -> `resolved_by_zone` cells carry `suitability` + `min_winter_temp_f`: the claim')
    print('      is COLD HARDINESS, not a planting date. A citrus cold-tolerance document is')
    print('      the right CLASS of source for them; a vegetable calendar never was.')

    print('\nTHE THREE VOCABULARIES, TESTED SEPARATELY (PLA-114 asked for exactly this):')
    v1 = v2 = v3 = 0
    vdetail = []
    for (slug, reg, sid), ns in dec.items():
        crop = crops[slug]
        r1 = vocab_region(crop, reg)
        r2 = vocab_source(crop, sid)
        allp, r3 = vocab_prose(crop, reg, sid)
        v1 += bool(r1)
        v2 += bool(r2)
        v3 += bool(r3)
        vdetail.append(((slug, reg, sid), r1, r2, allp, r3))
    print('   V1 region-named finding      : %2d of %d decisions   TESTED' % (v1, len(dec)))
    print('   V2 source-id-named finding   : %2d of %d decisions   TESTED' % (v2, len(dec)))
    print('   V3 per-cell prose adjudicates: %2d of %d decisions   TESTED' % (v3, len(dec)))
    print('   (a 0 above is a MEASURED zero, not an unrun scan -- that distinction is the')
    print('    whole point of the exercise, per campaign C\'s "0 of 35" lesson.)')
    only3 = [k for k, r1, r2, _a, r3 in vdetail if r3 and not r2]
    only2 = [k for k, r1, r2, _a, r3 in vdetail if r2 and not r3]
    print('   adjudicated by V3 ALONE (V2 finds nothing): %d  %s'
          % (len(only3), ['%s/%s' % (k[0], k[1]) for k in only3] or '--'))
    print('   adjudicated by V2 ALONE (V3 finds nothing): %d  %s'
          % (len(only2), ['%s/%s' % (k[0], k[1]) for k in only2] or '--'))
    print('   -> THE VOCABULARIES ARE NOT NESTED. Either one alone under-reports, which is')
    print('      exactly why PLA-114 asked for all three to be run and recorded separately.')

    print('\nDECISION-LEVEL VERDICT (the ledger unit):')
    buckets = collections.defaultdict(list)
    for key, ns in dec.items():
        buckets[ns[0][7]].append((key, len(ns), ns[0][8], ns[0][0]))
    order = ['CATALOG-REPOINTABLE', 'DECLARED-ANCHOR', 'SIBLING-PATHED', 'MODELED-ONLY',
             'OPEN-SCOPED', 'OPEN']
    for b in order:
        rows = sorted(buckets.get(b, []), key=lambda r: (r[3], r[0]))
        if not rows:
            continue
        print('   %-20s %2d decisions, %3d nodes' % (
            b, len(rows), sum(n for _k, n, _w, _h in rows)))
        for (slug, reg, _sid), n, why, h in rows:
            print('        #%-3d %-15s %-16s %2d nodes  %s' % (h, slug, reg, n, why[:70]))

    cells, split = cell_view(crops, nodes)
    print('\nCELL VIEW -- one physical cell can carry TWO bare source ids:')
    print('   node-citations (the count above) : %3d' % len(nodes))
    print('   DISTINCT PHYSICAL CELLS          : %3d   (%d counted twice)'
          % (len(cells), len(nodes) - len(cells)))
    print('   cells whose two arms AGREE       : %3d   (no extra work)'
          % (len([k for k, v in cells.items() if len(v) > 1]) - len(split)))
    print('   cells SPLIT across verdicts      : %3d   <- one arm has a lead, the other does not'
          % len(split))
    for (slug, path), rows in sorted(split.items()):
        print('        %-42s %s' % (path.replace('regions.', ''),
                                    ' | '.join('#%d %s=%s' % r for r in sorted(rows))))

    cov = sibling_node_coverage(crops, nodes)
    partial = {k: v for k, v in cov.items() if v[0] < v[1]}
    if partial:
        print('\n   SIBLING-PATHED decisions whose coverage is PARTIAL (the verdict masks this):')
        for (h, slug, reg, sid), (c, t) in sorted(partial.items()):
            print('        #%-3d %-6s %-14s %-14s only %d of %d nodes have a sibling document'
                  % (h, slug, reg, sid, c, t))
    print('   sibling-covered node-citations   : %3d of %3d in SIBLING-PATHED decisions'
          % (sum(c for c, _t in cov.values()), sum(t for _c, t in cov.values())))

    hunt_state = collections.defaultdict(set)
    for n in nodes:
        hunt_state[n[0]].add(n[7])
    collapsed = sorted(h for h, vs in hunt_state.items() if vs <= {'SIBLING-PATHED',
                                                                  'DECLARED-ANCHOR',
                                                                  'CATALOG-REPOINTABLE'})
    print('\n   HUNTS WITH NO SEARCH LEFT (every decision has a named document or a')
    print('   filed declaration): %d of %d  -> %s'
          % (len(collapsed), len(hunt_state), ', '.join('#%d' % h for h in collapsed)))

    open_dec = [k for k, v in dec.items() if v[0][7] in ('OPEN', 'OPEN-SCOPED', 'MODELED-ONLY')]
    print('   STILL NEEDING A DECISION: %d of %d decisions, %d of %d nodes'
          % (len(open_dec), len(dec),
             sum(len(dec[k]) for k in open_dec), len(nodes)))

    print('\n   DOCUMENTS TO READ (the real unit of work -- one read serves N decisions):')
    docs = collections.defaultdict(list)
    for key, ns in dec.items():
        if ns[0][7] != 'SIBLING-PATHED':
            continue
        for d in re.findall(r'https?://\S+', ns[0][8]):
            docs[d.rstrip('+')].append(key)
    for d, keys in sorted(docs.items(), key=lambda kv: -len(kv[1])):
        print('      %-60s %2d decisions' % (d[:60], len(keys)))

    # -- self-checks: nothing may leak between buckets or classes
    assert sum(len(v) for v in buckets.values()) == len(dec), 'decision bucket leak'
    assert sum(len(v) for v in dec.values()) == len(nodes), 'node leak'
    assert sum(cls.values()) == len(nodes), 'class leak'
    for key, ns in dec.items():
        assert len({n[7] for n in ns}) == 1, 'decision %s split across verdicts' % (key,)

    if args.vocab:
        print('\nTHREE-VOCABULARY DETAIL PER DECISION:')
        for key, r1, r2, allp, r3 in sorted(vdetail):
            print('   %-15s %-16s %-16s' % key)
            print('      V1 region : %s' % (r1 or '-- none --'))
            print('      V2 source : %s' % ([('%s [%s]' % (i, m)) for i, m, _w in r2]
                                            or '-- none --'))
            print('      V3 prose  : %d fields present, %s adjudicating %s'
                  % (len(allp), len(r3), r3 or ''))

    if args.cells:
        print('\nEVERY PHYSICAL CELL (deduped across source ids):')
        for (slug, path), rows in sorted(cells.items()):
            print('   %-6s %-46s %s' % (slug, path.replace('regions.', ''),
                                        ' | '.join('#%d %s=%s' % r for r in sorted(rows))))

    if args.nodes:
        print('\nEVERY NODE:')
        for h, reg, _sid, slug, path, arm, _u, v, why in sorted(nodes):
            print('   #%-3d %-15s %-16s %-18s %-20s %s' % (h, slug, reg, arm, v, why[:44]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
