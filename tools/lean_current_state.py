#!/usr/bin/env python3
"""Lean CURRENT_STATE.md back toward a live surface by removing DUPLICATED release entries.

RULED 2026-07-29. CURRENT_STATE.md had re-accumulated 80 release entries (~250KB of its
353KB), drifting back into a second history log -- the very split commit 148e737 performed.

WHY NOT `gen_current_state.py` (i.e. protocol #2's "fully regenerate"):
    The generator emits the hand-maintained `## Live locked decisions / guardrails` section
    as an EMPTY FILL slot ("editorial -- accretes; carry forward + amend"). That section is
    currently **74,017 characters**. So a regen obliges an operator to hand-paste 74KB back,
    every time, and anything they miss is silently gone. That is almost certainly how the
    title + SESSION PROTOCOL header disappeared in 93d5a59 (and had to be restored once
    before, in ac18c8e). Regeneration is the riskier operation here, not the safer one.

    So this script does the SURGICAL thing instead: it deletes only what is provably
    duplicated elsewhere, and touches neither the header, the generated sections, nor one
    byte of the locked-decisions block.

SAFETY: an entry is removed ONLY if its canonical SHA is provably present in
STATE_HISTORY.md or STATE_HISTORY_ARCHIVE.md. Any entry that is not covered ABORTS the run
rather than being dropped. The newest entry is KEPT, so the file still says what just
happened on its own.

Verified before writing this: of the 10 entries sharing STATE_HISTORY's current format, all
10 are BYTE-IDENTICAL in both files; the other 70 have their own independently-worded
account in STATE_HISTORY's older `## <date> -- TITLE` format, and all 70 SHAs resolve there.

    $ python3 tools/lean_current_state.py --dry-run
    $ python3 tools/lean_current_state.py
"""
import argparse
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(REPO, 'CURRENT_STATE.md')
HISTORY = os.path.join(REPO, 'STATE_HISTORY.md')
ARCHIVE = os.path.join(REPO, 'STATE_HISTORY_ARCHIVE.md')

ENTRY_RE = re.compile(r'(?=\*\*`[0-9a-f]{8}` \(\d{4}-\d{2}-\d{2}\))')
SHA_RE = re.compile(r'\*\*`([0-9a-f]{8})`')


def die(msg):
    print(f'ABORT: {msg}', file=sys.stderr)
    sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    text = open(STATE, encoding='utf-8').read()
    covered = open(HISTORY, encoding='utf-8').read() + open(ARCHIVE, encoding='utf-8').read()

    if 'SESSION PROTOCOL' not in text:
        die('CURRENT_STATE.md has no SESSION PROTOCOL header; restore it before restructuring')
    head, sep, body = text.partition('\n---\n')
    if not sep:
        die('no --- separator')

    # The release-entry stack runs from the top of the body to the first `## ` section.
    m = re.search(r'^## ', body, re.M)
    if not m:
        die('no `## ` section found in the body; refusing to guess where the entry stack ends')
    stack, tail = body[:m.start()], body[m.start():]

    parts = [p for p in ENTRY_RE.split(stack) if SHA_RE.match(p)]
    leading = stack[:stack.find(parts[0])] if parts else stack
    if not parts:
        die('no release entries found; nothing to do')
    print(f'release entries in the stack: {len(parts)}')
    print(f'locked-decisions + generated sections preserved: {len(tail)} chars')

    keep, drop = parts[:1], parts[1:]
    print(f'keeping the newest ({SHA_RE.match(keep[0]).group(1)}), '
          f'considering {len(drop)} for removal')

    uncovered = [SHA_RE.match(p).group(1) for p in drop
                 if SHA_RE.match(p).group(1) not in covered]
    if uncovered:
        die(f'{len(uncovered)} entries are NOT covered in STATE_HISTORY/ARCHIVE and would be '
            f'lost: {uncovered}. Migrate them first; refusing to delete unique content.')
    print(f'all {len(drop)} are provably covered in STATE_HISTORY/ARCHIVE')

    pointer = (
        '> **The release-entry stack was REMOVED here on 2026-07-29** and lives in '
        '`STATE_HISTORY.md` (+ `STATE_HISTORY_ARCHIVE.md`), which is the append-only recovery '
        'log and the authority. This file had re-accumulated **80** entries, ~250KB of its 353KB, '
        'drifting back into a second history log -- the split `148e737` performed. Every removed '
        'entry was verified present in the history files before deletion (the 10 newest were '
        'BYTE-IDENTICAL in both). Only the current release is kept below, so this stays a LIVE '
        'SURFACE.\n\n')

    new_body = leading + pointer + keep[0].rstrip() + '\n\n' + tail
    out = head + sep + new_body

    print(f'\n{len(text)} -> {len(out)} chars '
          f'(-{len(text) - len(out)}, {100 * (len(text) - len(out)) // len(text)}% smaller)')

    # invariants
    for probe in ('SESSION PROTOCOL', '## Live locked decisions / guardrails',
                  '## Canonical pointer', '## Gate record', '## Region fill state',
                  '## Flip gates'):
        if probe not in out:
            die(f'invariant lost: {probe!r} missing from the result')
    if tail not in out:
        die('the preserved tail was altered')
    print('invariants ok: header, all four generated sections, and the '
          'locked-decisions block are intact byte-for-byte')

    if args.dry_run:
        print('\nDRY RUN, nothing written.')
        return 0
    open(STATE, 'w', encoding='utf-8').write(out)
    print(f'\nwritten. CURRENT_STATE.md is now {len(out)} chars')
    return 0


if __name__ == '__main__':
    sys.exit(main())
