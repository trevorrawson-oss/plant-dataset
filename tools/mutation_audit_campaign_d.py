#!/usr/bin/env python3
"""The corrected mutation audit for test_campaign_d_reprice (PLA-162).

WHY THIS EXISTS. The Phase 1 (PLA-138) mutation run for this suite was INVALID: its harness
applied textwrap.dedent to an already-indented interpolated body, flattening mutations to
column 0 -> IndentationError -> the mutation plugin never loaded -> pytest measured the CLEAN
fixture and reported false vacuity ([[a-clean-zero-can-be-your-own-parser]], inside the audit
itself). Every conclusion that run produced about this suite was discarded.

THE CORRECTED METHOD -- no source templating anywhere:
  * Mutations are applied IN-PROCESS: this file doubles as a pytest plugin whose
    pytest_configure wraps promote_fixture.pre_state, parses the pinned fixture, applies ONE
    named data-level defect, and re-serializes compact. The suite's own module code runs
    unmodified.
  * TWO liveness defenses against the exact Phase-1 failure:
      1. the plugin prints 'MUTATION-APPLIED <name>' at configure time, and the driver
         REFUSES a run whose output lacks the marker (plugin-not-loaded reads as error, never
         as green);
      2. a SENTINEL mutation (deleting the lemon crop) runs first and must redden the suite,
         or the harness declares itself dead and exits 2.

Each mutation is one guard family's own defect class; the guard is VACUOUS if the suite stays
green under it, MASKED if only other tests redden ([[guard-tests-pass-because-an-earlier-
check-fires]]). Run:

    python3 tools/mutation_audit_campaign_d.py
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

SUITE = os.path.join('tools', 'test_campaign_d_reprice.py')
BASE_SHA = '6b2dcb8ed4f51c833fa4d44845b15e7f609079a24a544af025c067dfca45d4db'
BARE_CLEMSON = 'https://hgic.clemson.edu'
PATHED_CLEMSON = 'https://hgic.clemson.edu/cold-tolerance-in-citrus/'


def _crop(data, slug):
    return next(c for c in data['crops'] if c['slug'] == slug)


def _cell(data, slug, region, zone):
    return _crop(data, slug)['regions'][region]['resolved_by_zone'][zone]


# ---------------------------------------------------------------- the mutations
# name -> (target guard(s) this defect class belongs to, mutate(data))

def mut_sentinel_lemon_deleted(data):
    data['crops'] = [c for c in data['crops'] if c['slug'] != 'lemon']


def mut_bare_node_repointed(data):
    """A bare claim-arm node silently fixed: the 123-node / 26-decision shape must notice."""
    arm = _crop(data, 'lemon')['regions']['warm_arid']['plantings'][0]['plant_out'][0]
    arm['anchoring_urls']['uariz_ext']['url'] = 'https://extension.arizona.edu/pubs/az1001.pdf'


def mut_decision_splits_across_two_bare_urls(data):
    """One decision citing two DIFFERENT bare hosts -- campaign A's abort case."""
    _cell(data, 'lemon', 'northern_tier', '3')['anchoring_urls']['clemson_hgic']['url'] = \
        'https://clemson.edu'


def mut_noncitrus_crop_enters_a_residue_hunt(data):
    """A non-citrus crop growing a SOLE bare citation under a residue hunt's (region, sid)."""
    for c in data['crops']:
        if c['slug'] in ('lemon', 'lime'):
            continue
        region = (c.get('regions') or {}).get('ca_interior')
        if not isinstance(region, dict) or not isinstance(
                region.get('resolved_by_zone'), dict):
            continue
        for cell in region['resolved_by_zone'].values():
            if isinstance(cell, dict):
                cell['anchoring_urls'] = {
                    'ucanr_ext': {'url': 'https://ucanr.edu', 'verified': '2026-08-05'}}
                # `sources` counts toward the node's citations; another id left there would
                # make the bare citation non-SOLE and the mutation invisible to the scan --
                # the first run of THIS harness had exactly that bug, and only the rewritten
                # guard's positive control exposed it
                cell['sources'] = ['ucanr_ext']
                return
    raise AssertionError('no non-citrus ca_interior cell found to mutate')


def mut_resolved_by_zone_node_leaves(data):
    """The claim-class split (48 resolved_by_zone) loses a node to a silent repoint."""
    _cell(data, 'lemon', 'ca_interior', '8')['anchoring_urls']['ucanr_ext']['url'] = \
        'https://ucanr.edu/sites/citrus/planting/'


def mut_sibling_documents_vanish(data):
    """lime/mandarin stop citing the pathed Clemson page -- hunt #25 loses its lead."""
    for sib in ('lime', 'mandarin-clementine'):
        rz = _crop(data, sib)['regions'].get('northern_tier', {}).get('resolved_by_zone', {})
        for cell in rz.values():
            au = (cell or {}).get('anchoring_urls') or {}
            if 'clemson_hgic' in au:
                au['clemson_hgic']['url'] = BARE_CLEMSON


def mut_prose_gains_an_adjudication(data):
    """V3 must move 3 -> 4 when a provenance sentence starts naming the source."""
    _crop(data, 'lemon')['regions']['northern_tier']['plantings_provenance'] = (
        'Windows modeled from clemson_hgic cold-tolerance guidance; not lifted from a chart.')


def mut_pear_scoped_finding_gone(data):
    """OPEN-SCOPED depends on the finding being present; without it the pear is plain OPEN."""
    vs = _crop(data, 'pear-asian')['verification_status']
    vs['open_findings'] = [
        f for f in vs['open_findings']
        if f.get('id') != 'pear_asian_ca_interior_homeorchard_root_repoint_candidate']


def mut_double_counted_cell_loses_one_id(data):
    """The 123-nodes-over-91-cells arithmetic rests on cells citing TWO bare ids."""
    arm = _crop(data, 'lemon')['regions']['warm_arid']['plantings'][0]['plant_out'][0]
    del arm['anchoring_urls']['clemson_hgic']


def mut_lime_modeled_finding_gone(data):
    """lime_pilot_finding_001 leaves the fixture. The as_of kept-count must fail LOUDLY --
    a table row asserting a finding the pinned state does not carry."""
    vs = _crop(data, 'lime')['verification_status']
    vs['open_findings'] = [f for f in vs['open_findings']
                           if f.get('id') != 'lime_pilot_finding_001']


def mut_hunt31_coverage_shifts(data):
    """Strip the pathed Clemson document from every citrus sibling in warm_arid: sibling
    node coverage (15 of 17) must move."""
    for c in data['crops']:
        if c['slug'] not in ('lemon', 'lime', 'orange-navel', 'mandarin-clementine',
                             'grapefruit'):
            continue
        region = (c.get('regions') or {}).get('warm_arid')
        if not isinstance(region, dict):
            continue
        blob = json.dumps(region)
        if 'cold-tolerance-in-citrus' not in blob:
            continue
        def strip(node):
            if isinstance(node, dict):
                for sid, m in (node.get('anchoring_urls') or {}).items():
                    if isinstance(m, dict) and m.get('url') == PATHED_CLEMSON:
                        m['url'] = BARE_CLEMSON
                for v in node.values():
                    strip(v)
            elif isinstance(node, list):
                for v in node:
                    strip(v)
        strip(region)


MUTATIONS = {
    'sentinel_lemon_deleted': (['<harness liveness -- most of the suite>'],
                               mut_sentinel_lemon_deleted),
    'bare_node_repointed': (['test_campaign_d_is_26_decisions_not_the_ledgers_14'],
                            mut_bare_node_repointed),
    'decision_splits_across_two_bare_urls': (['test_the_bare_url_map_is_one_per_decision'],
                                             mut_decision_splits_across_two_bare_urls),
    # REFUSAL-SPEC: for this defect class the CONTRACT is that collect() refuses the input
    # and the campaign's rows do not move, so the whole suite staying green IS the pass --
    # the guard (test_residue_hunts_contribute_citrus_only) re-injects this defect itself on
    # every run, with a positive scan control, and goes red if the filter is removed
    # (measured via the filter-gone collect mutation, 2026-08-10). Flagging green here as
    # VACUOUS was this harness's own first misread.
    'noncitrus_crop_enters_a_residue_hunt': ('REFUSED',
                                             mut_noncitrus_crop_enters_a_residue_hunt),
    'resolved_by_zone_node_leaves': (
        ['test_the_claim_class_is_mostly_suitability_not_planting_dates'],
        mut_resolved_by_zone_node_leaves),
    'sibling_documents_vanish': (['test_six_decisions_have_a_sibling_pathed_document'],
                                 mut_sibling_documents_vanish),
    'prose_gains_an_adjudication': (['test_all_three_vocabularies_return_a_number',
                                     'test_vocab_prose_sees_fields_even_where_it_finds_no_adjudication'],
                                    mut_prose_gains_an_adjudication),
    'pear_scoped_finding_gone': (['test_the_pears_are_open_scoped_not_closed'],
                                 mut_pear_scoped_finding_gone),
    'double_counted_cell_loses_one_id': (
        ['test_123_node_citations_are_only_91_physical_cells',
         'test_the_double_counted_cells_really_cite_two_bare_ids'],
        mut_double_counted_cell_loses_one_id),
    'lime_modeled_finding_gone': (['<as_of kept-count ERROR naming MODELED_FINDING>'],
                                  mut_lime_modeled_finding_gone),
    'hunt31_coverage_shifts': (['test_hunt_31_sibling_coverage_is_partial_and_reported'],
                               mut_hunt31_coverage_shifts),
}


# ---------------------------------------------------------------- pytest-plugin half

def pytest_configure(config):
    name = os.environ.get('CAMPAIGN_D_MUTATION')
    if not name:
        return
    import promote_fixture
    _target, mutate = MUTATIONS[name]
    real = promote_fixture.pre_state

    def mutated_pre_state(sha):
        raw = real(sha)
        if sha != BASE_SHA:
            return raw
        data = json.loads(raw)
        mutate(data)
        return json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')

    promote_fixture.pre_state = mutated_pre_state
    print('MUTATION-APPLIED %s' % name)


# ---------------------------------------------------------------- driver half

def run_one(name):
    env = dict(os.environ, CAMPAIGN_D_MUTATION=name,
               PYTHONPATH=HERE + os.pathsep + os.environ.get('PYTHONPATH', ''))
    p = subprocess.run([sys.executable, '-m', 'pytest', SUITE, '-q', '-p',
                       'mutation_audit_campaign_d'],
                      cwd=os.path.dirname(HERE), capture_output=True, text=True, env=env)
    out = p.stdout + p.stderr
    if 'MUTATION-APPLIED %s' % name not in out:
        print(out[-2000:])
        sys.exit('HARNESS DEAD: the mutation plugin did not load for %r -- this is the exact '
                 'Phase 1 failure mode, and it must never read as a result.' % name)
    failed = set(re.findall(r'(?:FAILED|ERROR) [^:]+::(\w+)', out))
    return p.returncode, failed, out


def main():
    rc, failed, out = run_one('sentinel_lemon_deleted')
    if rc == 0 or not failed:
        sys.exit('HARNESS DEAD: the sentinel mutation left the suite green. '
                 'A clean zero here would be the harness, not the suite.')
    print('harness alive: sentinel reddened %d tests' % len(failed))

    vacuous, masked = [], []
    for name, (targets, _fn) in MUTATIONS.items():
        if name == 'sentinel_lemon_deleted':
            continue
        rc, failed, out = run_one(name)
        if targets == 'REFUSED':
            if rc == 0:
                verdict = 'REFUSED as specified -- suite green, the in-suite guard verifies'
            else:
                verdict = 'UNEXPECTED RED under a refusal-spec mutation: %s' % sorted(failed)
                masked.append(name)
            print('%-42s %s' % (name, verdict))
            continue
        literal_targets = [t for t in targets if not t.startswith('<')]
        if rc == 0:
            verdict = 'VACUOUS -- suite fully green under its own defect'
            vacuous.append(name)
        elif literal_targets and not (set(literal_targets) & failed):
            verdict = 'MASKED -- only other tests red: %s' % sorted(failed)
            masked.append(name)
        else:
            verdict = 'CAUGHT (%d red: %s)' % (len(failed), sorted(failed)[:3])
        print('%-42s %s' % (name, verdict))

    print()
    if vacuous or masked:
        print('VACUOUS: %s' % vacuous)
        print('MASKED:  %s' % masked)
        sys.exit(1)
    print('all %d guard-family mutations caught by their own guards'
          % (len(MUTATIONS) - 1))


if __name__ == '__main__':
    main()
