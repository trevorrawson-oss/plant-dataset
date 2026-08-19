#!/usr/bin/env python3
"""PLA-253 promote: the Bt beginner safety line. Base 394bb8bd.

WHAT THIS DOES, and nothing else: replaces ONE leaf,
`control_methods.bt.how_it_works_beginner`. No crop is touched, no other control method,
no citation, no calendar, no catalog.

THE DEFECT. The beginner register told a first-season grower that a pesticide is
"harmless to people, pets, and bees" while the seasoned sibling on the same entry said
"practically nontoxic" -- the registered toxicity-category wording. "Harmless" is an
absolute safety claim on a pest-control product, shown to the audience least equipped to
supply its own caution. No structural gate in this repo can see it: whole_crop_gate checks
shape, verbatim_scan checks source overlap. It took someone reading the sentence.

TWO DEFECTS WERE FIXED, NOT ONE.
  (a) The absolute. "Harmless" is gone; the claim is now mechanistic and scoped.
  (b) A true statement creating a false impression. The old line named the one pollinator
      NOT at risk (bees) and stayed silent on butterflies -- which this entry's OWN
      `cautions` field says Bt kills as a group. A beginner reading only the beginner
      register got reassurance about pollinators and no hint of the non-target cost. The
      replacement carries that limit in plain words.
It also adds the eye-and-skin precaution the old line omitted entirely.

VERIFIED AGAINST THE ENTRY'S OWN T1 ANCHOR, not against the seasoned sibling -- PLA-253
item 2 is explicit that mirroring the seasoned field is not the bar for a pesticide safety
claim. NPIC, `npic.orst.edu/factsheets/btgen.html` (Reviewed: May 2022), re-read in full
at promote time:
  * "The insect gut must have a pH of 9.0 to 10.5 (high pH) in order to activate the
    toxin. This is different from the human gut, which has a low pH and is more acidic."
  * "Bt toxins are not activated when the spores are eaten by people, and no harm occurs...
    People and other mammals do not have the specific enzymes that break down the spore
    proteins to release the toxins. Mammals also do not have the necessary receptors."
  * "The U.S. EPA concluded that 'risk is not expected' to children or infants from eating
    food treated with Bt."
  * "some pesticide products with Bt in them have caused eye and skin irritation."
  * "Bt aizawai and Bt kurstaki controls caterpillars of moths and butterflies."
  * "The EPA also concluded that the Bt strains tenebrionis, israelensis, and kurstaki are
    low in toxicity to bees."

TWO THINGS RECORDED HONESTLY RATHER THAN GLOSSED, because this promote exists to stop
overclaiming and must not quietly do it again:
  1. "bees are not at risk" is absolute-SHAPED where NPIC's register for the active
     ingredient is "low in toxicity to bees", and NPIC separately warns that a formulated
     product's other ingredients "can pose greater risks than the Bt itself". The claim is
     supported for kurstaki and is a large improvement on a blanket "harmless" covering
     people, pets and bees at once -- but it is not the document's own hedge, and the
     tension is filed on PLA-253 rather than buried here.
  2. "wear gloves" is NOT in this document -- NPIC has zero occurrences of "glove". It is
     the repo's own standing advice (`pesticide_safety_education.handling_note_beginner`,
     "chemical-resistant gloves ... if the label says so") and errs toward caution, which
     is the safe direction for an omission but is not NPIC-sourced. Stated so no later
     reader credits NPIC with it.

Guard suite: tools/test_promote_pla253_bt_safety.py (fixture-pinned, replayed).
Mutation harness: tools/mutate_pla253_suite.py (PLA-215 convention, liveness-defended).

Usage: python3 tools/promote_pla253_bt_safety.py [canonical] [--dry-run]
"""
import argparse
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, 'crops_data_final.json')

BASE_SHA = '394bb8bdf63c989eeff7241ba41d1c37c829201733ce199f4dffc88490d8f660'

METHOD = 'bt'
FIELD = 'how_it_works_beginner'

OLD = ("Bt is a natural soil bacterium. When a caterpillar eats leaves sprayed with it, "
       "the Bt proteins wreck its gut and it stops feeding and dies. It is harmless to "
       "people, pets, and bees.")

NEW = ("Bt is a natural soil bacterium. When a caterpillar eats leaves sprayed with it, "
       "the Bt proteins wreck its gut, and it stops feeding and dies. It only affects "
       "caterpillars, so bees are not at risk, and people and pets cannot activate the "
       "proteins at all, which is why a treated vegetable is safe to eat. Two things to "
       "watch. The spray itself can irritate eyes and skin, so wear gloves and keep it "
       "away from your face. And it does not tell good caterpillars from bad, so spray "
       "only the plants that have a pest problem.")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('canonical', nargs='?', default=CANONICAL)
    ap.add_argument('--dry-run', action='store_true')
    # --expect-sha exists because the "already promoted" refusal below is otherwise
    # UNREACHABLE, and an unreachable guard reads as protection while providing none.
    # Any state whose field already carries NEW hashes to something other than BASE_SHA,
    # so the SHA guard fires first and the idempotence branch never runs. Its one real
    # path is a deliberate RE-PIN (someone advances the base after promoting and re-runs),
    # which is exactly what this flag expresses -- and what lets the suite exercise it.
    ap.add_argument('--expect-sha', default=BASE_SHA)
    # CHAIN-REPLAY CONTRACT. promote_fixture._from_chain rebuilds an uncommitted
    # intermediate state by invoking its producing promote as
    #   <script> --canonical PATH --expect-sha SHA --apply
    # so a script that any later suite must replay through has to accept exactly that
    # shape. This promote produces 5f2d9555, which is a real base for the bee-hedge
    # second pass and was never its own commit, so it is now a CHAIN member.
    ap.add_argument('--canonical', dest='canonical_flag', default=None)
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    canonical = args.canonical_flag or args.canonical

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
        print('ABORT: already promoted -- the field already carries the replacement',
              file=sys.stderr)
        return 1
    if current != OLD:
        # Never overwrite prose this promote was not written against.
        print(f'ABORT: control_methods.{METHOD}.{FIELD} is not the text this promote was '
              f'written against; re-read before replacing\n  found: {current!r}',
              file=sys.stderr)
        return 1

    entry[FIELD] = NEW
    print(f'replaced control_methods.{METHOD}.{FIELD}')
    print(f'  -{len(OLD)} chars -> +{len(NEW)} chars')

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
