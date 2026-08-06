#!/usr/bin/env python3
"""PLA-114 Task 2: correct the mis-credited parenthetical on lemon. Base 29b96b65.

The previous promote filed F1, recording that lemon's cold number was credited to three
institutions of which only one publishes it -- and then deliberately moved no consumer prose. So
canonical ended up holding the finding AND the defect it describes: a reader still saw

    (Sources: Clemson HGIC, Texas A&M AgriLife, UF/IFAS.)

`correct-every-field-carrying-an-attribution` is the rule that says a citation fix is not done
until every field carrying the attribution moves. This is that field.

THE EDIT IS PER-CLAIM, NOT A SWAP. `hardiness_notes_seasoned` carries more than the temperature,
and the campaign's own refrain is that the verdict splits by CLAIM, not by cell:

  * the TEMPERATURE is mis-credited -- neither Clemson nor TAMU publishes a lemon figure. UC ANR
    8100 gives the 29F onset for tender citrus with Table 1 rating lemon H, and UF/IFAS HS1153
    (HS402) gives four lemon-specific figures. Those two take the number.
  * the RANKING and the FREEZE-PROTECTION advice ARE supported by both -- TAMU's cold-hardy list
    excludes lemon and it carries the container-culture and sprinkler guidance; Clemson's
    15F hardiest-citrus figure sets the ceiling. Stripping them would be a mis-citation in the
    opposite direction.
  * "UF/IFAS" alone was never specific enough: the crop cites HS1153 AND HS132, and it is HS1153
    that publishes lemon's numbers.

WHAT IT DOES NOT TOUCH. The fourteen stage-aware strings the last promote pinned. This edits the
credit appended to one of them and nothing else; the claim text before " (Sources:" is asserted
byte-identical to `6b2dcb8e`, the state it was pinned against.

F1 IS APPENDED TO, NEVER REWRITTEN -- the arc's append-don't-rewrite convention. Its original text
records what was believed and stays byte-for-byte; a dated `[CORRECTION ...]` records what is no
longer true.

Usage: python3 tools/promote_pla114_credit_line.py [--dry-run]
"""
import argparse
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')

BASE_SHA = '29b96b65a0969a8ad654762b5d84276bafbd2a8747706cb512ed1414305abf6f'

OLD_TAIL = ' (Sources: Clemson HGIC, Texas A&M AgriLife, UF/IFAS.)'
NEW_TAIL = (' (Sources: cold-damage temperatures UC ANR 8100 and UF/IFAS HS1153; cold-hardiness '
            'ranking and freeze protection Clemson HGIC and Texas A&M AgriLife.)')

F1_ID = 'lemon_cold_threshold_was_miscredited_now_uc8100'
CORRECTION = (
    ' [CORRECTION 2026-08-06: the credit parenthetical quoted above as STILL OWED has now been '
    'corrected, in the follow-on promote that produced this record. It reads '
    '"(Sources: cold-damage temperatures UC ANR 8100 and UF/IFAS HS1153; cold-hardiness ranking '
    'and freeze protection Clemson HGIC and Texas A&M AgriLife.)". The change is PER-CLAIM, not a '
    'swap: Clemson HGIC and Texas A&M AgriLife are removed from the TEMPERATURE, which neither '
    'publishes, and kept for the cold-hardiness ranking and the freeze-protection guidance that '
    'they do (TAMU excludes lemon from its cold-hardy list and carries the container-culture and '
    'sprinkler operating points; Clemson publishes the 15F hardiest-citrus figure). Bare '
    '"UF/IFAS" was made specific to HS1153, because this crop cites both HS1153 and HS132 and it '
    'is HS1153 that publishes lemon figures. Nothing else in the string moved: the claim text '
    'before the parenthetical is byte-identical to 6b2dcb8e, including the leaves-and-fruit '
    'stage wording that an earlier draft wrongly proposed rewriting.]')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    raw = open(CANONICAL, 'rb').read()
    got = hashlib.sha256(raw).hexdigest()
    if got != BASE_SHA:
        print(f'ABORT: canonical is {got[:16]}, expected base {BASE_SHA[:16]}', file=sys.stderr)
        return 1
    print(f'base SHA verified: {got[:16]}')

    data = json.loads(raw)
    lemon = next(c for c in data['crops'] if c['slug'] == 'lemon')

    note = lemon['hardiness_notes_seasoned']
    if not note.endswith(OLD_TAIL):
        print('ABORT: hardiness_notes_seasoned does not end with the expected credit',
              file=sys.stderr)
        return 1
    claim_before = note[:-len(OLD_TAIL)]
    lemon['hardiness_notes_seasoned'] = claim_before + NEW_TAIL
    assert lemon['hardiness_notes_seasoned'].split(' (Sources:')[0] == claim_before
    print('credit parenthetical rewritten; claim text untouched')

    f1 = next(f for f in lemon['verification_status']['open_findings'] if f['id'] == F1_ID)
    if CORRECTION.strip() in f1['summary']:
        print('ABORT: F1 already carries this correction', file=sys.stderr)
        return 1
    original = f1['summary']
    f1['summary'] = original + CORRECTION
    assert f1['summary'].startswith(original)
    print('F1 correction appended (original preserved byte-for-byte)')

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
