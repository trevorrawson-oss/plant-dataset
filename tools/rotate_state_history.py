#!/usr/bin/env python3
"""rotate_state_history.py -- archive aged STATE_HISTORY entries.

STATE_HISTORY.md grows unbounded (1700+ lines). Move entries older than the most
recent N into STATE_HISTORY_ARCHIVE.md, keeping in the live file: the header
(everything above the first `## ` entry), the N most-recent dated entries, any
PINNED block (a "Standing lessons / survive all collapses" entry), and a pointer
to the archive. Newly-aged entries stack ABOVE existing archive entries
(most-recent-first). Idempotent: re-running when nothing has aged out is a no-op.

Usage (from repo root):
  python3 tools/rotate_state_history.py --dry-run   # show the split, write nothing
  python3 tools/rotate_state_history.py [--keep 15] # perform the rotation
"""
import os, sys, re, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIST = os.path.join(ROOT, "STATE_HISTORY.md")
ARCH = os.path.join(ROOT, "STATE_HISTORY_ARCHIVE.md")
POINTER_RE = re.compile(r"<!-- ROTATED -->")
PIN_RE = re.compile(r"standing lessons|survive all collapse", re.I)
ARCH_HEADER = ("# plant -- STATE HISTORY ARCHIVE (aged-out entries, most-recent-first)\n\n"
               "> Rotated out of STATE_HISTORY.md by tools/rotate_state_history.py. "
               "Append-only history; the live recent window lives in STATE_HISTORY.md.\n")
POINTER = ("\n> Older entries archived in "
           "[STATE_HISTORY_ARCHIVE.md](STATE_HISTORY_ARCHIVE.md). <!-- ROTATED -->\n")


def split_entries(text):
    """Return (header_block, [entry_text, ...]) splitting at top-level `## ` lines."""
    lines = text.splitlines(keepends=True)
    idxs = [i for i, l in enumerate(lines) if l.startswith("## ")]
    if not idxs:
        return text, []
    header = "".join(lines[:idxs[0]])
    entries = []
    for j, start in enumerate(idxs):
        end = idxs[j + 1] if j + 1 < len(idxs) else len(lines)
        entries.append("".join(lines[start:end]))
    return header, entries


def strip_pointer(text):
    return "".join(l for l in text.splitlines(keepends=True) if not POINTER_RE.search(l))


def plan_rotation(hist_text, arch_text, keep):
    """Pure core. Return (new_hist, new_arch, stats) or None if nothing ages out."""
    header, entries = split_entries(strip_pointer(hist_text))
    pinned = [e for e in entries if PIN_RE.search(e.splitlines()[0])]
    dated = [e for e in entries if not PIN_RE.search(e.splitlines()[0])]
    keep_dated, archive_new = dated[:keep], dated[keep:]
    if not archive_new:
        return None
    new_hist = header + "".join(keep_dated) + "".join(pinned) + POINTER
    existing = split_entries(arch_text)[1] if arch_text.strip() else []
    new_arch = ARCH_HEADER + "\n" + "".join(archive_new) + "".join(existing)
    stats = {"total": len(entries), "kept": len(keep_dated),
             "pinned": len(pinned), "archived": len(archive_new)}
    return new_hist, new_arch, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep", type=int, default=15)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    hist_text = open(HIST).read()
    arch_text = open(ARCH).read() if os.path.exists(ARCH) else ""
    res = plan_rotation(hist_text, arch_text, a.keep)

    _, entries = split_entries(strip_pointer(hist_text))
    if res is None:
        print(f"STATE_HISTORY: {len(entries)} entries <= keep window ({a.keep}). no-op.")
        return
    new_hist, new_arch, stats = res
    # conservation self-check: nothing dropped
    assert stats["kept"] + stats["pinned"] + stats["archived"] == stats["total"], stats
    print(f"STATE_HISTORY: {stats['total']} entries -> keep {stats['kept']} recent "
          f"+ {stats['pinned']} pinned in live; archive {stats['archived']}")
    if a.dry_run:
        print("--dry-run: nothing written.")
        return
    open(HIST, "w").write(new_hist)
    open(ARCH, "w").write(new_arch)
    print(f"wrote STATE_HISTORY.md ({new_hist.count(chr(10)) + 1} lines) + "
          f"STATE_HISTORY_ARCHIVE.md ({new_arch.count(chr(10)) + 1} lines)")


if __name__ == "__main__":
    main()
