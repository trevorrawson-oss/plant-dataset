#!/usr/bin/env python3
"""Calendar-coherence NORMALIZER -- the surgical, deterministic fix for the two impossible patterns
the A37 gate flags. Spec: docs/calendar-coherence-fix-design-2026-06-30.md.

It rewrites ONLY the cells the gate flags, reusing the gate's exact detectors
(`impossible_growing_months`, `bridgeable_holes`) so gate(after) == 0 and the diff touches exactly
the target set -- NEVER a full re-derive (60% of annual calendars are hand-authored multi-cycle
shapes the deriver can't reproduce; a re-derive would clobber ~507 cells).

  Bug 2 -- bridge a bridgeable one-month harvest-display hole by merging the two flanking spans
    (day precision preserved; the calendar TOKEN is left untouched -- the empty Plant/Pick row is a
    legit render state, per Trevor's don't-over-correct guardrail).
  Bug 1 -- replace an impossible `growing` token via the ordered 7-rule bucket map (below).

Warm-crop FL/desert-summer season_over cells are TAGGED (surfaced, not edited) as candidates for a
properly-backed heat_pause in the authoring lane (D8) -- the normalizer must not fake heat_pause
backing (A28 would reject a bare one).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from annual_calendar import parse_months, _month_num
from calendar_coherence_gate import impossible_growing_months, bridgeable_holes

_MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

_WINTER = {11, 12, 1, 2}                              # deep-winter months (rule 6)
# warm-season fruiters whose FL/desert summer gap deserves a backed heat_pause, not just season_over
_WARM_CROPS = {"eggplant", "watermelon", "pumpkin", "butternut-squash"}
_SUMMER = {6, 7, 8}
# mild-coastal regions: a winter `cold_pause` reads as "waiting", not "cold-stopped" (Trevor ruling,
# 2026-06-30) -- re-rule any cold_pause replacement here to season_over.
_MILD_COAST = {"ca_north_coast", "ca_south_coast"}


def _successor(cal, i):
    """The first non-`growing` token walking forward (wrap-aware) from the run containing index i."""
    f = (i + 1) % 12
    for _ in range(12):
        if cal[f] != "growing":
            return cal[f]
        f = (f + 1) % 12
    return None


def replacement_token(cell, i):
    """The ordered 7-rule replacement for an impossible `growing` at month index i (0-based).
    Reads the ORIGINAL cell (caller computes all replacements before mutating the calendar)."""
    cal = cell["calendar"]
    m = i + 1
    H = parse_months(cell.get("harvest") or "")
    SI = parse_months(cell.get("start_indoors") or "")
    if m in H:                       # 1. in-window (still producing / masked-or-bridged harvest)
        return "harvest"
    if m in SI:                      # 2. an authored start_indoors month
        return "indoors"
    s = _successor(cal, i)
    if s == "cold_pause":            # 3. leading edge of a winter block
        return "cold_pause"
    if s == "season_over":           # 4. leading edge of a season_over block
        return "season_over"
    if s == "indoors":               # 5. winter gap before an indoor seed-start
        return "cold_pause"
    if s == "plant" and m in _WINTER:  # 6. deep-winter gap before a spring plant
        return "cold_pause"
    return "season_over"             # 7. summer gap before fall plant / summer shoulder (G/H)


def _endpoints(piece):
    """A harvest span piece -> (start_text, end_text), preserving 'Mon DD' day precision."""
    p = piece.strip()
    if "-" in p:
        a, b = p.split("-", 1)
        return a.strip(), b.strip()
    return p, p                                       # a bare month is its own start and end


def bridge_harvest_string(hs, holes):
    """Merge the two harvest spans flanking each single-month hole into one continuous span
    (earlier span's start .. later span's end), preserving day precision. `holes` is 1-indexed."""
    holes = set(holes)
    while holes:
        pieces = [p.strip() for p in hs.replace(";", ",").split(",") if p.strip()]
        ends = [_endpoints(p) for p in pieces]
        start_m = [_month_num(s) for s, _ in ends]
        end_m = [_month_num(e) for _, e in ends]
        progressed = False
        for m in sorted(holes):
            prev_m = (m - 2) % 12 + 1
            next_m = m % 12 + 1
            bi = next((k for k in range(len(pieces)) if end_m[k] == prev_m), None)   # span ending m-1
            ai = next((k for k in range(len(pieces)) if start_m[k] == next_m), None)  # span starting m+1
            holes.discard(m)
            progressed = True
            if bi is None or ai is None or bi == ai:
                break                                 # defensive: not bridgeable -> skip this hole
            merged = ends[bi][0] + " - " + ends[ai][1]
            new_pieces = [p for k, p in enumerate(pieces) if k not in (bi, ai)]
            new_pieces.insert(min(bi, ai), merged)
            hs = ", ".join(new_pieces)
            break
    return hs


def normalize_crop(crop):
    """Apply both fixes in place to every cell the gate flags. Returns a list of change records:
    {loc, kind: 'token'|'harvest', month?/old/new, slug, heat_pause_tag?}. No-op on clean cells."""
    slug = crop.get("slug")
    is_annual = crop.get("calendar_basis") == "frost_anchored"
    changes = []
    for rk, r in (crop.get("regions") or {}).items():
        for z, cell in ((r or {}).get("resolved_by_zone") or {}).items():
            loc = f"{rk}.z{z}"
            # --- Bug 1 (tokens) -- compute ALL replacements from the original cell, then apply ---
            if is_annual:
                repls = [(i, replacement_token(cell, i)) for i, _blk in impossible_growing_months(cell)]
                for i, tok in repls:
                    if tok == "cold_pause" and rk in _MILD_COAST:
                        tok = "season_over"          # mild-coastal re-rule (Trevor, 2026-06-30)
                    old = cell["calendar"][i]
                    cell["calendar"][i] = tok
                    rec = {"slug": slug, "loc": loc, "kind": "token",
                           "month": _MON[i], "old": old, "new": tok}
                    if tok == "season_over" and slug in _WARM_CROPS and (i + 1) in _SUMMER:
                        rec["heat_pause_tag"] = True  # D8: candidate for a backed heat_pause (authoring)
                    changes.append(rec)
            # --- Bug 2 (harvest display) -- bridge; token untouched ---
            holes = bridgeable_holes(cell)
            if holes:
                old = cell.get("harvest")
                new = bridge_harvest_string(old, holes)
                if new != old:
                    cell["harvest"] = new
                    changes.append({"slug": slug, "loc": loc, "kind": "harvest",
                                    "months": [_MON[m - 1] for m in holes], "old": old, "new": new})
    return changes


def normalize_dataset(in_path, out_path=None):
    """Load, normalize every crop, optionally write COMPACT. Returns (all_changes, warm_tags)."""
    import json
    data = json.load(open(in_path, encoding="utf-8"))
    all_changes = []
    for c in data["crops"]:
        all_changes.extend(normalize_crop(c))
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
    warm_tags = [c for c in all_changes if c.get("heat_pause_tag")]
    return all_changes, warm_tags


if __name__ == "__main__":
    in_path = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"
    out_path = sys.argv[2] if len(sys.argv) > 2 else None      # omit -> DRY RUN (report only)
    changes, tags = normalize_dataset(in_path, out_path)
    tok = [c for c in changes if c["kind"] == "token"]
    harv = [c for c in changes if c["kind"] == "harvest"]
    print(f"normalizer: {len(tok)} token replacements + {len(harv)} harvest bridges "
          f"= {len(changes)} changes across "
          f"{len({(c['slug'], c['loc']) for c in changes})} cells "
          f"({'WROTE ' + out_path if out_path else 'DRY RUN -- no write'})")
    print(f"  warm-crop heat_pause tags (D8): {len(tags)}")
