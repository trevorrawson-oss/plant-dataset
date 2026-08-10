#!/usr/bin/env python3
"""Adversarial tests for tools/campaign_d_reprice.py.

The tool makes three claims that will be quoted into the ledger and into Linear, and every one
of them is the kind that is expensive to get wrong:

  1. campaign D is 26 decisions, not the ledger's 14  (a number going UP)
  2. six decisions are SIBLING-PATHED -- a named document already exists for the exact cell
  3. three vocabularies were TESTED, and their zeros are measured zeros

A tool that reports a collapse must be provably capable of NOT reporting one, so every check is
mutation-tested: the tests below each break one thing on a deepcopy and assert the verdict moves.
Written after the arc was burned repeatedly by guards that were green and vacuous
([[guard-derived-from-what-it-checks-is-vacuous]], [[computed-guard-expectations-are-vacuous]],
[[guard-tests-pass-because-an-earlier-check-fires]]).

THE SUITE'S OWN ORIGIN STORY, kept because it is the point. The first run of the tool reported
SIBLING-PATHED = 0 decisions, cleanly and confidently. That zero was a bug in the tool's OWN path
parser -- `resolved_by_zone.3` has a numeric dict key the regex did not match, so it silently
resolved to the parent and found no `anchoring_urls` anywhere. The finding was real and the
measurement said otherwise. `test_resolver_reaches_every_scanned_node` is the regression, and
`test_MUTATION_a_broken_resolver_is_caught_not_silently_zeroed` proves the guard is load-bearing.

NEVER mutates canonical -- every mutation is applied to a deepcopy.
"""
import copy
import json
import os
import re
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))

import campaign_d_reprice as R  # noqa: E402
import promote_fixture  # noqa: E402


# The re-price is a MEASUREMENT OF A SPECIFIC CANONICAL -- `6b2dcb8e`, 2026-08-05, the state
# docs/2026-08-05-campaign-d-reprice-and-citrus-document-read.md reports. So these tests read the
# PINNED pre-state, not live canonical, and the numbers below stay checkable forever.
#
# They were briefly failing against live canonical after the 2026-08-06 PLA-114 promote repointed
# nine bare citations: 123 bare node-citations became 105, 48 resolved_by_zone nodes became 30, and
# the six SIBLING-PATHED decisions stopped being bare because THE PROMOTE FIXED THEM. That is the
# tool correctly observing its own campaign progressing, not rot -- but re-baselining the constants
# on every promote would quietly destroy the record of what the arc was priced at. Pinning the
# fixture keeps both: the tool still reports the LIVE open number when you run it, and the suite
# still proves the published measurement.
BASE_SHA = '6b2dcb8ed4f51c833fa4d44845b15e7f609079a24a544af025c067dfca45d4db'


@pytest.fixture(scope='module')
def data():
    import promote_fixture
    return json.loads(promote_fixture.pre_state(BASE_SHA))


@pytest.fixture(scope='module')
def crops(data):
    return {c['slug']: c for c in data['crops']}


# Evaluate ALL FOUR adjudication tables AS THEY WERE at `6b2dcb8e`, for the whole suite.
#
# THE PIN PROTECTS THE DATA BUT NOT THE MEASUREMENT, and that gap is real: the tables are
# applied at READ time, so extending one (as the PLA-114 close did, adding 15 lemon/lime rows
# to ANCHOR_FINDING) changes the verdicts this suite computes even against a frozen fixture.
# The original fix here covered ANCHOR_FINDING alone; PLA-162 measured that one added
# MODELED_FINDING row turned a pinned presence assertion red the same way, and re-baselining
# would have destroyed the historical numbers the pin exists to keep.
#
# The kept counts are the row counts each table held at the pin -- promote_fixture.tables_as_of
# fails loudly if the filter keeps more (a post-pin row escaped) or fewer (a row the
# measurement asserts on got eaten). The live "TABLE CLAIMS x BUT IT IS NOT ON THIS CROP"
# guards below run against current canonical over the FULL tables (via this fixture's yielded
# value), where they are the check that caught the lime declaration filed on the wrong crop.
_tables = promote_fixture.as_of(
    BASE_SHA, R, ANCHOR_FINDING=4, MODELED_FINDING=4, SCOPED_OPEN=2)

# The hunt rosters are RULES, not rows -- no keyed record in the fixture can scope them, so
# they are frozen BY VALUE as of `6b2dcb8e`. D closed with these eleven own hunts and seven
# citrus-residue hunts; test_live_hunt_rosters_match_the_frozen_pin below is the unpinned
# tripwire that goes red -- once, loudly -- if a live roster ever changes.
OWN_HUNTS_AT_PIN = {
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
RESIDUE_HUNTS_AT_PIN = {
    ('ca_interior', 'ucanr_ext'): 3,
    ('ca_north_coast', 'ucanr_ext'): 4,
    ('ca_south_coast', 'ucanr_ext'): 5,
    ('ca_desert', 'ucanr_ext'): 6,
    ('warm_arid', 'tamu_agrilife'): 8,
    ('low_desert_az', 'uariz_ext'): 14,
    ('ca_desert', 'uariz_ext'): 21,
}
HUNTS_AT_PIN = dict(OWN_HUNTS_AT_PIN)
HUNTS_AT_PIN.update(RESIDUE_HUNTS_AT_PIN)
_rules = promote_fixture.frozen(
    R, OWN_HUNTS=OWN_HUNTS_AT_PIN, RESIDUE_HUNTS=RESIDUE_HUNTS_AT_PIN, HUNTS=HUNTS_AT_PIN,
    BARE=re.compile(r'https?://[^/]+/?$'))


def test_live_hunt_rosters_match_the_frozen_pin(_rules):
    """The unpinned equality tripwire. `_rules` holds the LIVE values saved before freezing;
    comparing the module attribute here would be a tautology. A deliberate roster or BARE
    change fails THIS test, once and loudly, instead of silently re-baselining every pinned
    count above -- update this expectation only with the change spelled out in the diff."""
    assert _rules['OWN_HUNTS'] == OWN_HUNTS_AT_PIN
    assert _rules['RESIDUE_HUNTS'] == RESIDUE_HUNTS_AT_PIN
    assert _rules['HUNTS'] == HUNTS_AT_PIN
    assert _rules['BARE'].pattern == r'https?://[^/]+/?$'


def verdicts(data):
    crops = {c['slug']: c for c in data['crops']}
    out = {}
    for _h, reg, sid, slug, _p, _a, _u, v, why in R.collect(data, crops):
        out[(slug, reg, sid)] = (v, why)
    return out


def bucket(data, name):
    return {k for k, (v, _w) in verdicts(data).items() if v == name}


# --------------------------------------------------------------------------------------------
# 1. The measured shape. These pin the numbers the ledger and Linear will carry.
# --------------------------------------------------------------------------------------------

def test_campaign_d_is_26_decisions_not_the_ledgers_14(data, crops):
    """The ledger's campaign table says 11 hunts / 14 decisions. That counts D's OWN hunts and
    omits the citrus residue its own note column defers here seven separate times."""
    nodes = R.collect(data, crops)
    dec = {(n[3], n[1], n[2]) for n in nodes}
    assert len(nodes) == 123
    assert len(dec) == 26
    own = {d for d in dec if (d[1], d[2]) in R.OWN_HUNTS}
    res = {d for d in dec if (d[1], d[2]) in R.RESIDUE_HUNTS}
    assert len(own) == 14, 'the ledger 14 should be exactly D\'s own hunts'
    assert len(res) == 12, 'and the residue is the 12 it forgot'
    assert own | res == dec and not (own & res)


def test_residue_hunts_contribute_citrus_only(data, crops):
    """Campaigns A and C settled the non-citrus rows of hunts #3-#6, #8, #14, #21. Counting them
    again here would inflate D with work that is already closed.

    VACUITY FIXED (PLA-162). The original version iterated collect()'s output asserting a
    condition collect() itself enforces two lines earlier, so it could never fail -- the
    corrected mutation audit measured the whole suite GREEN with a non-citrus crop planted
    inside a residue hunt ([[guard-derived-from-what-it-checks-is-vacuous]]). This version
    injects exactly that defect and asserts the filter REFUSES it: the campaign's rows must
    not move, with the raw scan as the positive control proving the planted node was really
    there to refuse."""
    d = copy.deepcopy(data)
    crops2 = {c['slug']: c for c in d['crops']}
    planted_slug = None
    for c in d['crops']:
        if c['slug'] in R.CITRUS:
            continue
        region = (c.get('regions') or {}).get('ca_interior')
        if isinstance(region, dict) and isinstance(region.get('resolved_by_zone'), dict):
            planted_slug = c['slug']
            cell = next(v for v in region['resolved_by_zone'].values() if isinstance(v, dict))
            cell['anchoring_urls'] = {
                'ucanr_ext': {'url': 'https://ucanr.edu', 'verified': '2026-08-05'}}
            # `sources` counts toward the node's citations too; leaving another id there
            # would make the bare citation non-SOLE and the injection invisible to the scan
            cell['sources'] = ['ucanr_ext']
            break
    assert planted_slug, 'no non-citrus ca_interior cell to inject into -- fixture broke'
    seen = [(s, p) for sid, s, p, sole, _u in R.scan(d)
            if sole and sid == 'ucanr_ext' and s == planted_slug
            and R.region_of(p) == 'ca_interior']
    assert seen, 'the planted node never entered the scan -- the positive control is broken'
    key = lambda n: (n[0], n[1], n[2], n[3], n[4])  # noqa: E731
    before = {key(n) for n in R.collect(data, crops)}
    after = {key(n) for n in R.collect(d, crops2)}
    assert after == before, (
        'a non-citrus crop re-entered campaign D via a residue hunt: %s'
        % sorted(after - before))


def test_the_bare_url_map_is_one_per_decision(data, crops):
    """Campaign A's promote aborted on a decision citing two bare urls. Pinned here too."""
    per = {}
    for _h, reg, sid, slug, _p, _a, url, _v, _w in R.collect(data, crops):
        per.setdefault((slug, reg, sid), set()).add(url)
    split = {k: v for k, v in per.items() if len(v) > 1}
    assert not split, 'decisions citing more than one bare url: %s' % split


def test_the_claim_class_is_mostly_suitability_not_planting_dates(data, crops):
    """This is WHY D is not shaped like A/B/C, and it is what makes a citrus cold-tolerance
    document the right class of source rather than a planting calendar."""
    cls = {}
    for _h, _r, _s, _c, _p, arm, _u, _v, _w in R.collect(data, crops):
        cls[arm] = cls.get(arm, 0) + 1
    assert cls['resolved_by_zone'] == 48
    assert cls['resolved_by_zone'] > cls['plant_out'] + cls['bloom']


# --------------------------------------------------------------------------------------------
# 2. The resolver. This is the check whose absence produced a confident, wrong zero.
# --------------------------------------------------------------------------------------------

def test_resolver_reaches_every_scanned_node(data, crops):
    """bare_host_scan builds paths by an independent recursive walk; resolve() parses them back
    as strings. They can only agree if the parser is right -- so this is not vacuous."""
    raw = []
    for sid, slug, path, sole, url in R.scan(data):
        if sole and (R.region_of(path), sid) in R.HUNTS:
            if (R.region_of(path), sid) in R.RESIDUE_HUNTS and slug not in R.CITRUS:
                continue
            raw.append((0, R.region_of(path), sid, slug, path, '', url))
    assert raw, 'nothing scanned -- the fixture itself is broken'
    R.assert_resolver_agrees_with_scanner(crops, raw)


def test_resolver_handles_a_numeric_dict_key(crops):
    """`resolved_by_zone.3` -- the exact shape the first parser dropped."""
    node = R.resolve(crops['lemon'], 'regions.northern_tier.resolved_by_zone.3')
    assert isinstance(node, dict)
    assert 'anchoring_urls' in node and 'suitability' in node


def test_resolver_handles_a_list_index(crops):
    node = R.resolve(crops['lemon'], 'regions.ca_interior.plantings[0].bloom[0]')
    assert isinstance(node, dict) and 'anchoring_urls' in node


def test_MUTATION_a_broken_resolver_is_caught_not_silently_zeroed(data, crops):
    """Re-introduce the original bug and confirm the guard FAILS rather than reporting zero.

    Without this, a parser regression reads as 'no sibling document exists' -- which is exactly
    how the first run of this tool mispriced the whole campaign."""
    import re as _re
    good = R.resolve

    def broken(root, path):
        cur = root
        for key, idx in _re.findall(r'([A-Za-z_][A-Za-z0-9_]*)|\[(\d+)\]', path):
            try:
                cur = cur[key] if key else cur[int(idx)]
            except (KeyError, IndexError, TypeError):
                return None
        return cur

    R.resolve = broken
    try:
        with pytest.raises(AssertionError):
            R.collect(data, {c['slug']: c for c in data['crops']})
    finally:
        R.resolve = good


# --------------------------------------------------------------------------------------------
# 3. SIBLING-PATHED -- the verdict that prices D. A lead, never a repoint.
# --------------------------------------------------------------------------------------------

EXPECTED_SIBLING = {
    ('lemon', 'warm_arid', 'tamu_agrilife'),
    ('lemon', 'northern_tier', 'clemson_hgic'),
    ('lemon', 'northern_tier', 'tamu_agrilife'),
    ('lemon', 'se_gulf', 'tamu_agrilife'),
    ('lemon', 'ca_interior', 'uc_ipm'),
    ('lemon', 'warm_arid', 'clemson_hgic'),
}


def test_six_decisions_have_a_sibling_pathed_document(data):
    assert bucket(data, 'SIBLING-PATHED') == EXPECTED_SIBLING


def test_the_sibling_check_looks_at_a_different_crop(crops):
    """Non-vacuity: lemon's own node is bare, and the hit comes from lime/mandarin, not lemon."""
    hits = R.pathed_by_sibling(crops, 'lemon',
                               'regions.northern_tier.resolved_by_zone.3', 'clemson_hgic')
    assert hits, 'the sibling document should be found'
    assert all(other != 'lemon' for other, _url in hits)
    own = R.resolve(crops['lemon'], 'regions.northern_tier.resolved_by_zone.3')
    assert R.BARE.fullmatch(own['anchoring_urls']['clemson_hgic']['url']), (
        "lemon's own citation must still be bare -- otherwise there is nothing to adjudicate")


def test_MUTATION_removing_the_sibling_document_flips_lemon_to_open(data):
    """If lime stopped citing the pathed Clemson page, hunt #25 has no lead and must reopen."""
    d = copy.deepcopy(data)
    crops = {c['slug']: c for c in d['crops']}
    for sib in ('lime', 'mandarin-clementine'):
        for z in ('3', '4', '5', '6', '7'):
            cell = R.resolve(crops[sib], 'regions.northern_tier.resolved_by_zone.%s' % z)
            if cell and 'clemson_hgic' in (cell.get('anchoring_urls') or {}):
                cell['anchoring_urls']['clemson_hgic']['url'] = 'https://hgic.clemson.edu'
    v = verdicts(d)
    assert v[('lemon', 'northern_tier', 'clemson_hgic')][0] == 'OPEN'
    # and the OTHER sibling-pathed decisions must be untouched -- no blast radius
    assert v[('lemon', 'northern_tier', 'tamu_agrilife')][0] == 'SIBLING-PATHED'


def test_MUTATION_pathing_lemons_own_url_removes_it_from_the_scan(data):
    """A repointed node is no longer a bare host, so it leaves the campaign entirely."""
    d = copy.deepcopy(data)
    crops = {c['slug']: c for c in d['crops']}
    for z in ('3', '4', '5', '6', '7'):
        cell = R.resolve(crops['lemon'], 'regions.northern_tier.resolved_by_zone.%s' % z)
        cell['anchoring_urls']['clemson_hgic']['url'] = (
            'https://hgic.clemson.edu/cold-tolerance-in-citrus/')
    assert ('lemon', 'northern_tier', 'clemson_hgic') not in verdicts(d)


# --------------------------------------------------------------------------------------------
# 4. The alias check, carried from campaign C. It must still be able to REFUSE.
# --------------------------------------------------------------------------------------------

def test_jalapeno_ufifas_alias_is_refused_because_two_uf_ifas_ids_compete(crops):
    ok, competing = R.alias_is_unambiguous(crops['jalapeno'], 'ufifas_ext')
    assert not ok and 'uf_ifas_vh021' in competing


def test_bell_pepper_closes_on_v2_where_jalapeno_does_not(data):
    """Same institution, same region, same claim -- different verdicts, because one finding
    named the id verbatim and the other said only "ufifas" while the crop cites two UF/IFAS ids."""
    v = verdicts(data)
    assert v[('bell-pepper', 'fl_peninsula', 'ufifas_ext')][0] == 'DECLARED-ANCHOR'
    assert 'STRICT' in v[('bell-pepper', 'fl_peninsula', 'ufifas_ext')][1]
    jal = v[('jalapeno', 'fl_peninsula', 'ufifas_ext')]
    assert jal[0] != 'DECLARED-ANCHOR', 'the refused alias must not close the anchor'
    assert 'V2 refused' in jal[1], 'and the refusal must stay VISIBLE in the evidence string'


def test_a_refused_alias_does_not_short_circuit_the_other_vocabularies(data):
    """The ordering bug this caught: returning OPEN on a refused V2 hid that jalapeno's Florida
    decision IS adjudicated in prose. Refusing on one vocabulary must not skip the rest."""
    v = verdicts(data)
    assert v[('jalapeno', 'fl_peninsula', 'ufifas_ext')][0] == 'MODELED-ONLY'


def test_the_three_vocabularies_are_not_nested(data, crops):
    """Each vocabulary finds something the others miss, which is the whole reason PLA-114 asked
    for three separate tests rather than one. If this ever collapses to nesting, the cheaper
    single scan would be defensible -- until then it is not."""
    only_v3, only_v2 = [], []
    seen = set()
    for _h, reg, sid, slug, _p, _a, _u, _v, _w in R.collect(data, crops):
        if (slug, reg, sid) in seen:
            continue
        seen.add((slug, reg, sid))
        has2 = bool(R.vocab_source(crops[slug], sid))
        has3 = bool(R.vocab_prose(crops[slug], reg, sid)[1])
        if has3 and not has2:
            only_v3.append((slug, reg))
        if has2 and not has3:
            only_v2.append((slug, reg))
    assert only_v3 == [('jalapeno', 'fl_peninsula')]
    assert len(only_v2) == 3


def test_MUTATION_removing_the_competing_id_flips_jalapeno_to_declared(data):
    """Non-vacuity for the refusal: drop uf_ifas_vh021 and the alias becomes unambiguous."""
    d = copy.deepcopy(data)
    jal = next(c for c in d['crops'] if c['slug'] == 'jalapeno')

    def strip(n):
        if isinstance(n, dict):
            a = n.get('anchoring_urls')
            if isinstance(a, dict):
                a.pop('uf_ifas_vh021', None)
            if isinstance(n.get('sources'), list):
                n['sources'] = [s for s in n['sources'] if s != 'uf_ifas_vh021']
            for k, v in n.items():
                if k != 'anchoring_urls':
                    strip(v)
        elif isinstance(n, list):
            for v in n:
                strip(v)

    strip(jal)
    assert R.alias_is_unambiguous(jal, 'ufifas_ext')[0]
    assert verdicts(d)[('jalapeno', 'fl_peninsula', 'ufifas_ext')][0] == 'DECLARED-ANCHOR'


def test_MUTATION_unnaming_the_source_drops_bell_pepper_off_declared_anchor(data):
    """Strip the id out of the finding's prose and the V2 close must fail.

    It lands on MODELED-ONLY rather than OPEN, and that is the CORRECT fall-through: bell-pepper
    also carries `bell_pepper_pilot_regional_calendars_modeled`, so a third vocabulary still has
    something to say. The mutation's job is to prove the V2 check is load-bearing, which it does
    -- asserting OPEN here would be asserting that the OTHER vocabularies are broken too."""
    d = copy.deepcopy(data)
    bp = next(c for c in d['crops'] if c['slug'] == 'bell-pepper')
    f = R.finding(bp, 'bell_pepper_pilot_regional_source_anchors_general')
    for k in ('summary', 'detail', 'resolution', 'note'):
        if isinstance(f.get(k), str):
            f[k] = f[k].replace('ufifas_ext', 'REDACTED').replace('ufifas', 'REDACTED')
    before = verdicts(data)[('bell-pepper', 'fl_peninsula', 'ufifas_ext')][0]
    after = verdicts(d)[('bell-pepper', 'fl_peninsula', 'ufifas_ext')][0]
    assert before == 'DECLARED-ANCHOR' and after != 'DECLARED-ANCHOR'


# --------------------------------------------------------------------------------------------
# 5. The adjudication tables must describe the data, not assert over it.
# --------------------------------------------------------------------------------------------

@pytest.fixture(scope='module')
def live():
    """Current canonical -- the presence tests are a claim about the CURRENT dataset."""
    with open(R.CANONICAL, encoding='utf-8') as fh:
        return {c['slug']: c for c in json.load(fh)['crops']}


def test_every_anchor_table_entry_is_present_on_its_crop(live, _tables):
    """Validated against LIVE canonical over the FULL table, not the pinned fixture and not
    the filtered view the rest of this suite measures through.

    The table is a claim about the CURRENT dataset -- "this finding exists on this crop and names
    this id" -- so it must be checked against current data, and it must iterate `_tables` (the
    unfiltered rows) or every post-pin entry would escape the check. The shape and count tests
    stay pinned to `6b2dcb8e`, because those are a claim about what the arc was PRICED at.
    Splitting the two is what lets the table grow as decisions close without the historical
    measurement drifting.
    """
    for (_reg, slug, _sid), fid in _tables['ANCHOR_FINDING'].items():
        assert R.finding(live[slug], fid) is not None, '%s missing from %s' % (fid, slug)


def test_every_modeled_table_entry_is_present_on_its_crop(live, _tables):
    for slug, fid in _tables['MODELED_FINDING'].items():
        assert R.finding(live[slug], fid) is not None, '%s missing from %s' % (fid, slug)


def test_every_scoped_open_entry_is_present_and_still_open(live, _tables):
    for (_reg, slug), fid in _tables['SCOPED_OPEN'].items():
        f = R.finding(live[slug], fid)
        assert f is not None and f.get('status') == 'open', (
            '%s must be present AND open -- an accepted one is a different verdict' % fid)


def test_MUTATION_deleting_the_finding_flips_edamame_to_open(data):
    d = copy.deepcopy(data)
    ed = next(c for c in d['crops'] if c['slug'] == 'edamame')
    fs = ed['verification_status']['open_findings']
    ed['verification_status']['open_findings'] = [
        f for f in fs if f.get('id') != 'edamame_pilot_regional_source_urls']
    assert verdicts(d)[('edamame', 'ca_north_coast', 'ucanr_marin_mg')][0] != 'DECLARED-ANCHOR'


# --------------------------------------------------------------------------------------------
# 6. The three vocabularies. A zero must be a MEASURED zero.
# --------------------------------------------------------------------------------------------

def test_all_three_vocabularies_return_a_number(data, crops):
    """PLA-114's ask: record which vocabularies were tested and what each returned, so a 0 is
    distinguishable from an untested vocabulary."""
    v1 = v2 = v3 = 0
    seen = set()
    for _h, reg, sid, slug, _p, _a, _u, _v, _w in R.collect(data, crops):
        if (slug, reg, sid) in seen:
            continue
        seen.add((slug, reg, sid))
        v1 += bool(R.vocab_region(crops[slug], reg))
        v2 += bool(R.vocab_source(crops[slug], sid))
        v3 += bool(R.vocab_prose(crops[slug], reg, sid)[1])
    assert (v1, v2, v3) == (6, 5, 3)
    assert len(seen) == 26


def test_vocab_prose_sees_fields_even_where_it_finds_no_adjudication(crops):
    """The distinction that matters: lemon's regions carry plenty of prose, and NONE of it
    adjudicates the anchor. That is a measured zero, not an unread field."""
    present, adjudicating = R.vocab_prose(crops['lemon'], 'northern_tier', 'clemson_hgic')
    assert len(present) > 5, 'the prose fields are there to be read'
    assert not adjudicating, 'and none of them speaks to the sourcing'


def test_MUTATION_prose_naming_the_source_is_detected(data):
    """Non-vacuity for V3: write an adjudication into the prose and V3 must find it."""
    d = copy.deepcopy(data)
    crops = {c['slug']: c for c in d['crops']}
    reg = crops['lemon']['regions']['northern_tier']
    reg['plantings_provenance'] = (
        'Windows modeled from clemson_hgic cold-tolerance guidance; not lifted from a chart.')
    _present, adjudicating = R.vocab_prose(crops['lemon'], 'northern_tier', 'clemson_hgic')
    assert adjudicating, 'V3 must detect an adjudication once one exists'


# --------------------------------------------------------------------------------------------
# 7. Nothing leaks between buckets.
# --------------------------------------------------------------------------------------------

def test_every_decision_lands_in_exactly_one_bucket(data):
    v = verdicts(data)
    names = ['CATALOG-REPOINTABLE', 'DECLARED-ANCHOR', 'SIBLING-PATHED', 'MODELED-ONLY',
             'OPEN-SCOPED', 'OPEN']
    total = sum(len(bucket(data, n)) for n in names)
    assert total == len(v) == 26


def test_a_decision_never_splits_across_verdicts(data, crops):
    seen = {}
    for _h, reg, sid, slug, _p, _a, _u, verdict, _w in R.collect(data, crops):
        seen.setdefault((slug, reg, sid), set()).add(verdict)
    assert all(len(s) == 1 for s in seen.values())


def test_the_pears_are_open_scoped_not_closed(data):
    """They carry an OPEN finding naming the next move. That is not the same as adjudicated,
    and collapsing the two is how this arc has overstated progress before."""
    assert bucket(data, 'OPEN-SCOPED') == {
        ('pear-asian', 'ca_north_coast', 'ucanr_marin_mg'),
        ('pear-european', 'ca_north_coast', 'ucanr_marin_mg'),
    }


# --------------------------------------------------------------------------------------------
# 8. The CELL view -- the decision unit over-counts physical cells.
# --------------------------------------------------------------------------------------------

def test_123_node_citations_are_only_91_physical_cells(data, crops):
    """One cell can carry TWO bare source ids and is then counted once per id."""
    nodes = R.collect(data, crops)
    cells, _split = R.cell_view(crops, nodes)
    assert len(nodes) == 123
    assert len(cells) == 91
    assert len(nodes) - len(cells) == 32


def test_the_double_counted_cells_really_cite_two_bare_ids(crops):
    """Non-vacuity: prove the mechanism on a named cell rather than trusting the arithmetic."""
    node = R.resolve(crops['lemon'], 'regions.warm_arid.plantings[0].plant_out[0]')
    anchors = node['anchoring_urls']
    assert {'uariz_ext', 'clemson_hgic'} <= set(anchors)
    assert all(R.BARE.fullmatch(anchors[s]['url']) for s in ('uariz_ext', 'clemson_hgic'))


def test_five_cells_are_split_across_verdicts(data, crops):
    """A cell is not settled until BOTH its citations are; these have one lead and one not."""
    nodes = R.collect(data, crops)
    _cells, split = R.cell_view(crops, nodes)
    assert {p.replace('regions.', '') for _s, p in split} == {
        'ca_interior.resolved_by_zone.8',
        'ca_interior.resolved_by_zone.9',
        'se_gulf.resolved_by_zone.8',
        'warm_arid.plantings[0]',
        'warm_arid.plantings[0].plant_out[0]',
    }


def test_hunt_31_sibling_coverage_is_partial_and_reported(data, crops):
    """The decision-level verdict is driven by ANY node having a sibling, which would otherwise
    claim a document for #31's `plantings` container and `plant_out` arm, which have none."""
    cov = R.sibling_node_coverage(crops, R.collect(data, crops))
    partial = {k: v for k, v in cov.items() if v[0] < v[1]}
    assert len(partial) == 1
    (h, slug, reg, sid), (covered, total) = next(iter(partial.items()))
    assert (h, slug, reg, sid) == (31, 'lemon', 'warm_arid', 'clemson_hgic')
    assert (covered, total) == (1, 3)
    assert sum(c for c, _t in cov.values()) == 15
    assert sum(t for _c, t in cov.values()) == 17


def test_lime_is_modeled_only_and_that_does_not_close_the_anchor(data):
    """lime_pilot_finding_001 declares the WINDOWS modeled. It says nothing about the citation
    being a portal, so it must not be merged into DECLARED-ANCHOR."""
    modeled = bucket(data, 'MODELED-ONLY')
    assert len(modeled) == 7
    assert {s for s, _r, _i in modeled} == {'lime', 'jalapeno'}
    assert len([1 for s, _r, _i in modeled if s == 'lime']) == 6
    assert not (modeled & bucket(data, 'DECLARED-ANCHOR'))
