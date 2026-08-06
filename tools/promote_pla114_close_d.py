#!/usr/bin/env python3
"""PLA-114 final: close D's counted decisions, and record what the metric cannot see. Base 820af861.

RULING 1 (repoint, do not drop) is followed, and a repo-side reason now supports it far more
strongly than the chat-side argument did: **add-alongside does not merely fail to close a decision,
it CONCEALS the bare citation.** `bare_host_scan` sets is_sole=False when a cell cites ANY non-bare
source and `campaign_d_reprice` filters on it, so adding a pathed co-source removes every remaining
bare citation ON THAT CELL from the count. That is how hunt #28 vanished while still bare, and it is
what the section-7 promote did to five nodes. Repointing is the only option that closes the decision
AND unmasks the citation.

SCOPE, per Trevor's rule: repoint where an ALREADY-ADMITTED document covers the SAME CLAIM. Read
against the data that is FOUR arms, not the thirteen a same-institution test suggests:

  * 7 lime cells would repoint `ucanr_ext` onto UC IPM's `agriculture/citrus/` PEST page. REFUSED --
    campaign D already established both UC IPM citrus pages carry zero temperatures and zero cold
    content, so pointing planting/bloom/harvest anchors at them is `right-document-wrong-claim`,
    the exact defect F2 records.
  * 2 lemon `ca_interior` zone cells would repoint onto the UC IPM freeze page, which supports a
    SUITABILITY claim only. Those cells carry more than suitability. NOT repointed.
  * the remaining 4 are `plant_out` arms whose same-institution co-source publishes the planting
    RULE itself. Those are mechanical and are repointed here.

RULING 3 is followed for arms with no document: a finding that NAMES the source id AND DECLARES the
anchor closes the decision. Naming-to-decline does not, which is why the section-7 findings closed
nothing.

Usage: python3 tools/promote_pla114_close_d.py [--dry-run]
"""
import argparse
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')
BASE_SHA = '820af861e38070a375441803db7e2ddddc72a67e20dd8be580998aa7110a8d1c'
SESSION = 'pla114_close_d_2026_08_06'

# (region, bare id, id whose document it is repointed onto) -- all four are plant_out arms whose
# co-source publishes the planting rule, verified on the cell rather than inferred.
REPOINTS = [
    ('ca_interior', 'ucanr_ext', 'ucce_kern_kc9382'),
    ('ca_north_coast', 'ucanr_ext', 'uc_mg_marin_citrus'),
    # Mauk, not Lazaneo, although BOTH sit on this cell and both are UC. `ucanr_ext` is the UC ANR
    # institution root and its catalog url is ucanr.edu; Mauk is hosted there, Lazaneo is on the
    # Association domain mastergardenersd.org. Pointing an institution-root id at a different host
    # is the host/id mismatch this arc has hit twice (nmsu_chart on a TAMU host; aggie-hort vs
    # aggie-horticulture). Same claim either way -- both publish the frost-anchored planting rule.
    ('ca_south_coast', 'ucanr_ext', 'ucce_riverside_citrus_qa'),
    ('ca_desert', 'ucanr_ext', 'ucce_riverside_citrus_qa'),
]

LEMON_FINDINGS = [
    {
        'id': 'lemon_regional_anchor_ids_declared_modeled_where_no_document_exists',
        'severity': 'low', 'status': 'resolved', 'blocks_launch': False,
        'filed_in_session': SESSION,
        'summary': (
            'ADJUDICATING DECLARATION for lemon\'s bare regional anchor ids, filed to CLOSE the '
            'decisions rather than to describe them. NAMES the ids and DECLARES the anchor, which '
            'is the distinction that matters: the findings filed in the section-7 promote named '
            '`ucanr_ext` and `uariz_ext` only to DECLINE them ("the ucanr_ext arm stays bare; that '
            'is hunt #3 and it is still open"), which satisfies a vocabulary scan and closes '
            'nothing. '
            'DECLARED HERE, for `ucanr_ext` on ca_interior, ca_north_coast, ca_south_coast and '
            'ca_desert, for `uariz_ext` on low_desert_az, ca_desert and warm_arid, and for '
            '`clemson_hgic` on warm_arid (hunt #31, whose plantings container and plant_out arm '
            'have no sibling citrus document at all): on the '
            'arms that still cite them bare -- `plantings`, `bloom`, `harvest_start`, '
            '`harvest_end`, `resolved_by_zone` and low_desert_az `plant_out` -- these ids are '
            'INSTITUTION-ROOT PORTALS standing for the UC ANR and University of Arizona '
            'Cooperative Extension programmes, and the windows they anchor are MODELED, not '
            'lifted from a chart. The campaign D document read was exhaustive and is recorded '
            'across this crop\'s findings: no T1 publishes a lemon bloom window for any region '
            '(see lemon_bloom_modeled_every_region); no UC document publishes a lemon harvest '
            'window for the Central Valley (see lemon_ca_interior_harvest_modeled_no_uc_window); '
            'and UA AZ1001, which does publish a low-desert harvest window, is inadmissible for '
            'arms computed from a modeled bloom anchor (see '
            'lemon_harvest_arms_uncitable_as_structured_and_may_render_too_narrow). '
            'PLANT_OUT IS THE EXCEPTION AND IS NOW SOURCED: four CA plant_out arms are repointed '
            'in this promote onto the UC documents that publish the frost-anchored planting rule '
            '(UCCE Kern KC9382, UC Marin MG, Lazaneo/San Diego, Mauk & Shea/Riverside). '
            'low_desert_az plant_out stays declared because AZ1001 publishes no planting date.'),
    },
]

LIME_FINDINGS = [
    {
        'id': 'lime_regional_anchor_ids_declared_modeled_same_class_as_lemon',
        'severity': 'low', 'status': 'resolved', 'blocks_launch': False,
        'filed_in_session': SESSION,
        'summary': (
            'ADJUDICATING DECLARATION for lime, filed in the same pass as lemon\'s because it is '
            'the same defect class and is already inside campaign D\'s re-price count. '
            '`lime_pilot_finding_001` declares lime\'s windows modeled but does not adjudicate the '
            'ANCHOR ID, which is why lime\'s decisions read MODELED-ONLY rather than closed. '
            'DECLARED HERE for `ucanr_ext` on ca_north_coast, ca_south_coast, ca_desert and '
            'ca_interior, and for `uariz_ext` AND `ucanr_ext` on low_desert_az and `uariz_ext` on '
            'ca_desert: these are '
            'INSTITUTION-ROOT PORTALS '
            'and the windows are MODELED. '
            'ONE REPOINT WAS AVAILABLE AND IS REFUSED: lime\'s ca_interior cells carry a pathed '
            '`uc_ipm` co-source at ipm.ucanr.edu/agriculture/citrus/, which a same-institution '
            'test would treat as a repoint target for seven bare `ucanr_ext` citations covering '
            'plantings, plant_out, bloom, harvest_start, harvest_end and two zone cells. That page '
            'is PEST AND DISEASE material -- campaign D established it carries zero temperatures '
            'and zero cold content -- so repointing planting and harvest anchors onto it would be '
            'right-document-wrong-claim, the precise defect F2 records for lemon. Same-institution '
            'and pathed-on-the-same-cell is the SIBLING-PATHED shape, which this campaign has twice '
            'ruled a LEAD and not a verdict.'),
    },
]

LEMON_FINDINGS += [
    {
        'id': 'campaign_d_metric_counts_adjudication_not_citation_repair',
        'severity': 'medium', 'status': 'open', 'blocks_launch': False,
        'filed_in_session': SESSION,
        'summary': (
            'THE LIMITATION THIS CAMPAIGN CLOSES ON, recorded so no future reader mistakes the '
            'completion signal for the state of the data. `campaign_d_reprice` answers "are the '
            'DECISIONS adjudicated", not "are the CITATIONS fixed", and on lemon and lime those '
            'two diverge by 51. '
            'MECHANISM, measured not inferred: `bare_host_scan` sets is_sole=False when a cell '
            'cites ANY non-bare source, and the re-price filters on it. So a bare citation is '
            'invisible to the count whenever a PATHED CO-SOURCE sits on the same cell, whatever '
            'its source id. Adding a pathed document alongside a bare one therefore REMOVES the '
            'bare citation from the metric without fixing it. '
            'MEASURED AT THE CLOSE: lemon and lime carry 166 bare citations; the re-price counts '
            'only the sole-source ones; 51 remain bare and uncounted after this promote. Largest '
            'residues: lime `ucanr_ext` 19, lemon `ucanr_ext` 13 before this promote\'s four '
            'repoints, lemon `tamu_agrilife` 11, lemon `clemson_hgic` 3. '
            'THIS ALREADY BIT US TWICE. Hunt #28 (se_gulf/clemson_hgic) left the decision count '
            'during the 6b2dcb8e->29b96b65 promote while its citation is STILL BARE at '
            'se_gulf.resolved_by_zone.8 -- it was masked when TAMU on the same cell was repointed. '
            'And five of the section-7 promote\'s node reductions were masking, not fixing. Of the '
            '23-node reduction across this arc, 15 nodes genuinely became pathed and 8 were merely '
            'hidden. '
            'NOT A BUG. The decision unit was chosen deliberately and campaign A refined it; a '
            'collapsed unit is the right instrument for pricing research. But a deliberate design '
            'that emits a misleading COMPLETION signal is still a limitation the record must '
            'carry, and this is the fifth instrument failure of this class in the campaign -- the '
            'previous four were zeros that were wrong, this is a completion that would be. Filed '
            'to PLA-138, whose charter covers scan blind spots, because it generalises: ANY '
            'campaign closing on a collapsed unit can close on paper while the underlying defect '
            'persists.'),
    },
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    raw = open(CANONICAL, 'rb').read()
    got = hashlib.sha256(raw).hexdigest()
    if got != BASE_SHA:
        print(f'ABORT: canonical is {got[:16]}, expected {BASE_SHA[:16]}', file=sys.stderr)
        return 1
    print(f'base SHA verified: {got[:16]}')

    data = json.loads(raw)
    lemon = next(c for c in data['crops'] if c['slug'] == 'lemon')

    for region, bare_id, target_id in REPOINTS:
        arm = lemon['regions'][region]['plantings'][0]['plant_out'][0]
        au = arm['anchoring_urls']
        assert target_id in au, f'{region}: {target_id} not on the cell'
        target_url = au[target_id]['url']
        assert '/' in target_url.split('://', 1)[1], f'{target_id} is not pathed'
        before = au[bare_id]['url']
        assert before.count('/') <= 3, f'{region}/{bare_id} is already pathed: {before}'
        au[bare_id] = {'url': target_url, 'verified': '2026-08-06'}
        print(f'  repoint {region:16s} {bare_id} : {before} -> {target_url}')

    lime = next(c for c in data['crops'] if c['slug'] == 'lime')
    for crop, findings, label in ((lemon, LEMON_FINDINGS, 'lemon'), (lime, LIME_FINDINGS, 'lime')):
        existing = {f['id'] for f in crop['verification_status']['open_findings']}
        for f in findings:
            assert f['id'] not in existing, f['id']
            crop['verification_status']['open_findings'].append(f)
        print(f'filed {len(findings)} findings on {label}')

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    new_sha = hashlib.sha256(out).hexdigest()
    if args.dry_run:
        print(f'DRY RUN -- {len(out)} bytes, sha {new_sha}')
        return 0
    open(CANONICAL, 'wb').write(out)
    print(f'wrote {len(out)} bytes\nnew canonical SHA: {new_sha}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
