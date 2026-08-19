#!/usr/bin/env python3
"""PLA-161 promote: hunt #28's adjudicating declaration. Base 76f92a20.

WHAT THIS DOES, and nothing else: appends ONE finding to lemon's `verification_status
.open_findings`. It repoints no URL, changes no prose, touches no calendar, mints no source.

WHY IT IS A DECLARATION AND NOT THE REPOINT THE ISSUE ASKED FOR. PLA-161 scoped hunt #28 as a
repoint: `lemon` / `regions.se_gulf.resolved_by_zone.8` cites `clemson_hgic` at the bare host
`https://hgic.clemson.edu`, while lemon cites the same id PATHED at
`hgic.clemson.edu/cold-tolerance-in-citrus/` on 14 other nodes, one URL, no ambiguity. The issue's
own instruction was to read the document first. Read on 2026-08-18, in full, from cache:

  * the article body is 2,223 characters;
  * it mentions "lemon" EXACTLY ONCE, in a taxonomy list ("Acid citrus includes lemons, limes,
    calamondins, and kumquats");
  * it publishes ONE temperature, 15F for satsuma, and names kumquat at about the same;
  * it contains ZERO occurrences of Gulf, Louisiana, Florida, Southeast, zone, container, wrap
    or cover, and its only protection guidance is to protect the GRAFT UNION.

The node claims a high-20s F lemon damage threshold and `survives_no_fruit` at zone 8. Neither is
in the document. Repointing would credit Clemson with a lemon figure that THIS CROP'S OWN
CERTIFICATION RECORD has already ruled it does not publish: the resolved finding
`lemon_cold_threshold_was_miscredited_now_uc8100` says "Clemson's cold-tolerance page publishes
satsuma and kumquat at 15F and no lemon number" ([[cert-log-already-adjudicated-the-band]],
[[right-document-wrong-claim]]).

So hunt #28 is CASE 2. The declaration closes the decision without moving a citation onto a
document that does not support it. It mirrors this crop's own precedent exactly:
`lemon_regional_anchor_ids_declared_modeled_where_no_document_exists` closed hunt #31's
`clemson_hgic` on warm_arid the same way, and its key shape is copied key-for-key here.

THE CITATION STAYS BARE, DELIBERATELY. Dropping it would erase the record that the decision was
examined; a future bare-host scan would surface the node again with nothing attached explaining
why it is as it is.

Usage: python3 tools/promote_pla161_hunt28_declaration.py [--dry-run]
"""
import argparse
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')

BASE_SHA = '76f92a20faae0b8e5336ef8e7e1d9c852b9c734c93ae84fc6cccd65f49bcf3ce'

# The canonical this promote PRODUCES from BASE_SHA (committed as 4dde2c8, registered in
# promote_fixture.COMMIT_FOR). Added 2026-08-19 so the guard suite can compare pre against
# THIS PROMOTE'S OWN OUTPUT instead of against live canonical.
#
# Why that mattered: the suite's blast-radius guard compared the replayed pre-state against
# whatever canonical happened to be on disk, so it asserted "nothing in the dataset moved
# except this finding" about the WHOLE HISTORY SINCE, not about this promote. PLA-253's
# `control_methods.bt` edit reddened it the moment it landed, and every future promote would
# have reddened it again. A guard that fails on every unrelated change gets ignored, and an
# ignored guard is not a guard -- it is a permanently red line in the suite that trains people
# to skip the run.
POST_SHA = '394bb8bdf63c989eeff7241ba41d1c37c829201733ce199f4dffc88490d8f660'

NODE_PATH = ('se_gulf', '8')
SOURCE_ID = 'clemson_hgic'
BARE_URL = 'https://hgic.clemson.edu'

# Key order copied from `lemon_regional_anchor_ids_declared_modeled_where_no_document_exists`,
# the warm_arid clemson_hgic declaration on this same crop: id, severity, status, blocks_launch,
# filed_in_session, summary.
FINDING = {
    'id': 'lemon_se_gulf_clemson_hgic_declared_no_claim_rests_on_it',
    'severity': 'low',
    'status': 'resolved',
    'blocks_launch': False,
    'filed_in_session': 'pla161_hunt28_2026_08_18',
    'summary': (
        "ADJUDICATING DECLARATION for clemson_hgic on se_gulf resolved_by_zone.8 (hunt #28), "
        "filed to CLOSE the decision rather than to describe it. Clemson HGIC's "
        "cold-tolerance-in-citrus page was read in full on 2026-08-18 against this node's claims. "
        "It publishes one temperature figure, 15F for satsuma, and names kumquat at the same "
        "threshold. It mentions lemon exactly once, in a taxonomy list, and publishes no lemon "
        "damage temperature, no zone-level judgement for the Southeast Gulf, and no distinction "
        "between surviving and fruiting. This node's claims, a high-20s F lemon threshold and "
        "survives_no_fruit, are not supported by this document and are anchored to uc_anr_8100. "
        "This crop's certification record already ruled the same document at the same claim in "
        "the resolved finding lemon_cold_threshold_was_miscredited_now_uc8100. No claim on this "
        "node rests on this document. The citation is recorded here as adjudicated rather than "
        "dropped, so that a future reader does not re-open it."
    ),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    raw = open(CANONICAL, 'rb').read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != BASE_SHA:
        print(f'ABORT: base SHA mismatch\n  expected {BASE_SHA}\n  found    {sha}',
              file=sys.stderr)
        return 1

    data = json.loads(raw.decode('utf-8'))
    lemon = next((c for c in data['crops'] if c.get('slug') == 'lemon'), None)
    if lemon is None:
        print('ABORT: no lemon crop', file=sys.stderr)
        return 1

    # The node must still be bare -- if someone repointed it, this declaration is the wrong act.
    region, zone = NODE_PATH
    node = lemon['regions'][region]['resolved_by_zone'][zone]
    entry = node['anchoring_urls'][SOURCE_ID]
    if entry['url'] != BARE_URL:
        print(f'ABORT: {region}/z{zone}/{SOURCE_ID} is no longer bare ({entry["url"]}); '
              f'the decision changed, re-read before declaring', file=sys.stderr)
        return 1

    findings = lemon['verification_status']['open_findings']
    if any(f.get('id') == FINDING['id'] for f in findings):
        print('ABORT: declaration already filed', file=sys.stderr)
        return 1
    findings.append(dict(FINDING))
    print(f'filed {FINDING["id"]}')
    print(f'{region}/z{zone}/{SOURCE_ID} left BARE by design: {entry["url"]}')

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    new_sha = hashlib.sha256(out).hexdigest()
    if args.dry_run:
        print(f'DRY RUN -- would write {len(out)} bytes, sha {new_sha}')
        return 0
    with open(CANONICAL, 'wb') as fh:
        fh.write(out)
    print(f'wrote {len(out)} bytes\nnew canonical SHA: {new_sha}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
