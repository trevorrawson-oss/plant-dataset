#!/usr/bin/env python3
"""PLA-253 promote, SECOND PASS: the bee clause hedged to NPIC's own register. Base 5f2d9555.

WHAT THIS DOES, and nothing else: substitutes ONE CLAUSE inside ONE leaf,
`control_methods.bt.how_it_works_beginner`.

    "It only affects caterpillars, so bees are not at risk, and people and pets ..."
 -> "It only affects caterpillars, so the risk to bees is low, and people and pets ..."

Every other byte of the field, and of the document, is identical. The guard suite proves it
by reconstruction, not by inspection: `before.replace(CLAUSE_OLD, CLAUSE_NEW) == after`,
plus a character-level check that the text on each side of the clause did not move.

WHY A SECOND PASS ON PROSE THAT WAS JUST REWRITTEN. The first pass removed the blanket
"harmless to people, pets, and bees" and its own close-out flagged what it had left
standing: "bees are not at risk" is still ABSOLUTE-SHAPED. NPIC's register for the active
ingredient is weaker than that --

  "The EPA also concluded that the Bt strains tenebrionis, israelensis, and kurstaki are
   LOW IN TOXICITY to bees."

-- and NPIC separately warns that a formulated product's other ingredients "can pose
greater risks than the Bt itself", with the observed bumblebee and honeybee effects coming
from *aizawai* PRODUCTS in studies that could not separate the inert ingredients. The
document nowhere says bees face no risk. "The risk to bees is low" is that same claim in
words a first-season grower reads without a gloss, which is the whole point of the beginner
register: the register difference should be vocabulary, not a different safety claim.

THE FAILURE MODE THIS PASS HAS AND THE FIRST DID NOT: it can silently undo the first. The
suite therefore re-asserts every gain pass one made -- no "harmless" anywhere in the entry,
the eye-and-skin precaution present, the non-target caterpillar limit present -- so a hedge
achieved by reverting the field fails rather than passes.

THE BASE IS NOT A COMMIT. PLA-253 ran both promotes on one leaf before committing, so
5f2d9555 is registered in `promote_fixture.CHAIN` and rebuilt by replaying
`promote_pla253_bt_safety.py` from 394bb8bd, hash-verified on every use.

Guard suite: tools/test_promote_pla253_bt_bee_hedge.py
Mutation harness: tools/mutate_pla253_bee_hedge_suite.py (PLA-215, liveness-defended)

Usage: python3 tools/promote_pla253_bt_bee_hedge.py --canonical PATH --apply [--dry-run]
"""
import argparse
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')

BASE_SHA = '5f2d95559256df1553dd2ac0ba19cfa275ec497ab9ba0264ca28dbd94290af0e'

METHOD = 'bt'
FIELD = 'how_it_works_beginner'

CLAUSE_OLD = 'so bees are not at risk'
CLAUSE_NEW = 'so the risk to bees is low'

PREV = ("Bt is a natural soil bacterium. When a caterpillar eats leaves sprayed with it, "
        "the Bt proteins wreck its gut, and it stops feeding and dies. It only affects "
        "caterpillars, so bees are not at risk, and people and pets cannot activate the "
        "proteins at all, which is why a treated vegetable is safe to eat. Two things to "
        "watch. The spray itself can irritate eyes and skin, so wear gloves and keep it "
        "away from your face. And it does not tell good caterpillars from bad, so spray "
        "only the plants that have a pest problem.")

NEW = PREV.replace(CLAUSE_OLD, CLAUSE_NEW)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('canonical', nargs='?', default=CANONICAL)
    ap.add_argument('--canonical', dest='canonical_flag', default=None)
    ap.add_argument('--expect-sha', default=BASE_SHA)
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    canonical = args.canonical_flag or args.canonical

    # The substitution must be unique, or "replace one clause" is not what happens.
    assert PREV.count(CLAUSE_OLD) == 1, 'clause is not unique in the source text'
    assert NEW != PREV and NEW.count(CLAUSE_NEW) == 1

    raw = open(canonical, 'rb').read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != args.expect_sha:
        print(f'ABORT: base SHA mismatch\n  expected {args.expect_sha}\n  found    {sha}',
              file=sys.stderr)
        return 1

    data = json.loads(raw.decode('utf-8'))
    entry = data.get('control_methods', {}).get(METHOD)
    if entry is None:
        print(f'ABORT: no control_methods.{METHOD}', file=sys.stderr)
        return 1

    current = entry.get(FIELD)
    if current == NEW:
        print('ABORT: already hedged -- the field already carries the replacement',
              file=sys.stderr)
        return 1
    if current != PREV:
        # Includes the pass-one BASE text: this promote must never half-apply a hedge to a
        # sentence that still says "harmless".
        print(f'ABORT: control_methods.{METHOD}.{FIELD} is not the text this promote was '
              f'written against; re-read before replacing\n  found: {current!r}',
              file=sys.stderr)
        return 1

    entry[FIELD] = NEW
    print(f'hedged control_methods.{METHOD}.{FIELD}')
    print(f'  "{CLAUSE_OLD}" -> "{CLAUSE_NEW}"')
    print(f'  every other byte of the field unchanged ({len(PREV)} -> {len(NEW)} chars)')

    out = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    new_sha = hashlib.sha256(out).hexdigest()
    if args.dry_run:
        print(f'DRY RUN -- would write {len(out)} bytes, sha {new_sha}')
        return 0
    with open(canonical, 'wb') as fh:
        fh.write(out)
    print(f'wrote {len(out)} bytes\nnew canonical SHA: {new_sha}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
