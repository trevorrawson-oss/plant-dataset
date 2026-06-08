#!/usr/bin/env python3
"""Unit test for the STATE_HISTORY rotation logic (pure core, no file I/O).
Run from repo root: python3 tools/test_rotate_state_history.py

Pins: conservation (no entry lost), pinning the Standing-lessons block, and
idempotency (re-running when nothing has aged out is a no-op).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rotate_state_history import plan_rotation, split_entries

HEADER = "# plant -- STATE HISTORY (append-only)\n\n> preamble line\n\n"
def entry(tag): return f"## 2026-06-{tag} -- session `s{tag}`\n\nbody {tag}\nline2\n\n"
PINNED = "## Standing lessons (survive all collapses)\n\nkeep me forever\n\n"

# most-recent-first: 08,07,06,05,04 dated, plus one pinned at the bottom
hist = HEADER + entry("08") + entry("07") + entry("06") + entry("05") + entry("04") + PINNED

# --- split sees 6 top-level entries, header preserved ---
header, entries = split_entries(hist)
assert header == HEADER, repr(header)
assert len(entries) == 6, len(entries)

# --- keep 2: 2 most-recent dated kept, pinned kept, 3 archived ---
res = plan_rotation(hist, "", keep=2)
assert res is not None, "should rotate"
new_hist, new_arch, stats = res
assert stats == {"total": 6, "kept": 2, "pinned": 1, "archived": 3}, stats

# conservation: every original dated entry is in exactly one of hist/arch
for tag in ("08", "07"):
    assert f"session `s{tag}`" in new_hist and f"session `s{tag}`" not in new_arch, tag
for tag in ("06", "05", "04"):
    assert f"session `s{tag}`" in new_arch and f"session `s{tag}`" not in new_hist, tag
# pinned stays in the live file, never archived
assert "survive all collapses" in new_hist and "survive all collapses" not in new_arch
# archive is most-recent-first (06 newer than 05 newer than 04)
assert new_arch.index("s06") < new_arch.index("s05") < new_arch.index("s04")
# a pointer is left behind
assert "STATE_HISTORY_ARCHIVE.md" in new_hist

# --- idempotency: re-running on the rotated file is a no-op (only 2 dated remain) ---
assert plan_rotation(new_hist, new_arch, keep=2) is None, "second rotation must be a no-op"

# --- a second rotation AFTER growth stacks newly-aged ABOVE existing archive ---
# growth prepends newer entries at the top (most-recent-first)
grown = new_hist.replace(HEADER, HEADER + entry("10") + entry("09"), 1)
res2 = plan_rotation(grown, new_arch, keep=2)
assert res2 is not None
h2, a2, s2 = res2
# newest kept now 10,09; 08,07 newly archived and sit ABOVE the prior 06/05/04
assert a2.index("s08") < a2.index("s06"), "newly-aged entries must stack above older archive"

print("PASS rotate_state_history (conservation + pinning + idempotency)")
