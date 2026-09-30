#!/usr/bin/env python3
"""bare_host_gate -- PLA-544: a SOLE citation anchored at a bare host fails, on every certified crop.

THE RULE (Trevor, 2026-09-25 comment on PLA-544). A citation whose anchoring URL is a bare domain
or site root, and which is the SOLE citation on its node, fails, whether or not the same crop
paths that source id elsewhere. Co-cited bare anchors are REPORTED, never blocking.

WHY bare_host_scan's self_pathed VIEW WAS NOT ENOUGH. It fires only when the SAME crop paths the
source id at a document elsewhere. grapefruit does (`ucr_citrus` -> crc3602), so its bare Flying
Dragon row surfaced; orange-navel never paths `ucr_citrus`, so its identical bare, sole-cited row
was invisible. A crop that is UNIFORMLY bare on a source dropped out of the population, which is
the worse case. This gate does not ask whether a sibling document exists.

WHAT IT WALKS. Every dict on a certified crop carrying `anchoring_urls` (cited set = its keys plus
the node's `sources`) and every crop-root `<field>_anchoring_urls` (cited set = its keys plus
`<field>_sources`). bare_host_scan.scan() walks only the first; the second held 0 bare anchors on
00dda31c and is walked so a new one cannot hide there. Region cells and zones{} ARE walked: a
bare anchor is a bare anchor wherever it sits.

SOLE. The node cites nothing but bare hosts: (anchor ids + sources ids) minus the bare ids is
empty. The predicate is bare_host_scan's, deliberately, so the scan and the gate agree.

BARE. bare_host_scan.BARE (scheme + host + optional '/'), IMPORTED, never retyped, plus a site
ROOT PAGE: '/index.html' and the like, or a fragment on the root. The widening held 0 URLs on
00dda31c; it is there so the obvious respelling of a homepage does not pass.

WAIVED BY IDENTITY: crop | path | anchor key | source id, in bare_host_gate_known.py. A new
sole-bare citation prints itself by name. The population may shrink, never grow.

Usage: bare_host_gate.py [PATH]      exit 1 on a violation, 2 on a refused population
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from bare_host_scan import BARE  # noqa: E402  -- the scan's predicate, imported

CERTIFIED = "verified_gs_arc"
ROOT_PAGE = re.compile(r"https?://[^/?#]+/(?:index\.(?:html?|php|aspx?))?(?:#.*)?", re.I)
# MEASURED 2026-09-30 on 00dda31c: 30102 anchors on 121 certified crops. Fewer inspected than
# this REFUSES: "0 inspected, 0 violations" is not a pass.
MIN_INSPECTED = 28000


sys.path.insert(0, HERE)
import bare_host_gate_known as _K  # noqa: E402  -- the measured waiver set, a .py module (see its docstring)

_KNOWN_DOC = {"ticket": _K.TICKET, "measured_on": _K.MEASURED_ON, "count": _K.COUNT,
              "identities": list(_K.IDENTITIES)}
KNOWN = frozenset(_K.IDENTITIES)


def certified(crop):
    return (crop.get("verification_status") or {}).get("status") == CERTIFIED


def is_bare(url):
    return isinstance(url, str) and bool(BARE.fullmatch(url) or ROOT_PAGE.fullmatch(url))


def _entry_url(m):
    return m.get("url") if isinstance(m, dict) else None


def _rows_for(anchors, sources, slug, path, key):
    """[(identity, is_sole, url)] for the bare anchors in one anchoring dict; plus the count seen."""
    if not isinstance(anchors, dict) or not anchors:
        return [], 0
    bare = {sid: _entry_url(m) for sid, m in anchors.items() if is_bare(_entry_url(m))}
    rows = []
    if bare:
        cited = set(anchors) | {s for s in (sources or []) if isinstance(s, str)}
        sole = not (cited - set(bare))
        for sid, url in sorted(bare.items()):
            rows.append((f"{slug}|{path or '<crop>'}|{key}|{sid}", sole, url))
    return rows, len(anchors)


def scan_crop(crop):
    """(rows, anchors_inspected) for one crop, regardless of certification."""
    slug = crop.get("slug")
    rows, seen = [], 0

    def walk(node, path):
        nonlocal seen
        if isinstance(node, dict):
            srcs = node.get("sources")
            r, n = _rows_for(node.get("anchoring_urls"), srcs if isinstance(srcs, list) else [],
                             slug, path, "anchoring_urls")
            rows.extend(r)
            seen += n
            for k, v in node.items():
                if k != "anchoring_urls":
                    walk(v, f"{path}.{k}" if path else k)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{path}[{i}]")

    walk(crop, "")
    for k, v in crop.items():
        if k.endswith("_anchoring_urls"):
            base = k[: -len("_anchoring_urls")]
            srcs = crop.get(f"{base}_sources")
            r, n = _rows_for(v, srcs if isinstance(srcs, list) else [], slug, "<crop>", k)
            rows.extend(r)
            seen += n
    return rows, seen


def crop_violations(crop):
    """Per-crop half (whole_crop_gate A63). No-op off certified: the waivers cover certified only."""
    if not certified(crop):
        return []
    rows, _ = scan_crop(crop)
    return [f"NEW sole bare-host citation {ident} -> {url}: the node's ONLY citation is a domain "
            f"root, which cannot support a crop-specific claim. Anchor it at the document, or "
            f"co-cite a document (PLA-544)."
            for ident, sole, url in rows if sole and ident not in KNOWN]


def roster(data):
    """(certified_count, inspected, sole_live, cocited_live, violations, stale)."""
    cert = [c for c in data.get("crops", []) if certified(c)]
    inspected, sole, co, V = 0, [], [], []
    for c in cert:
        rows, n = scan_crop(c)
        inspected += n
        sole.extend(i for i, s, _u in rows if s)
        co.extend(i for i, s, _u in rows if not s)
        V.extend(crop_violations(c))
    stale = sorted(KNOWN - set(sole))
    return len(cert), inspected, sorted(sole), sorted(co), V, stale


def refusal(n_cert, inspected):
    if n_cert == 0:
        return "inspected 0 certified crops"
    if inspected < MIN_INSPECTED:
        return f"inspected {inspected} anchors, below the declared floor {MIN_INSPECTED}"
    return None


def main(argv):
    path = argv[1] if len(argv) > 1 else "crops_data_final.json"
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    n_cert, inspected, sole, co, V, stale = roster(data)
    for v in V:
        print("VIOLATION:", v)
    print(f"bare_host_gate: {len(V)} violation(s); inspected {inspected} anchors on {n_cert} "
          f"certified crops; {len(sole)} SOLE bare ({len(KNOWN)} waived by identity), "
          f"{len(co)} co-cited bare (reported, non-blocking)")
    if stale:
        print(f"  CLOSED since arming ({len(stale)}): drop from bare_host_gate_known.py in the "
              f"commit that repoints them: " + ", ".join(stale[:20])
              + (" ..." if len(stale) > 20 else ""))
    why = refusal(n_cert, inspected)
    if why:
        print(f"bare_host_gate: REFUSED -- {why}. A check that inspected nothing is not a pass.")
        return 2
    return 1 if V else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
