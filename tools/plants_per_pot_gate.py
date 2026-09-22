#!/usr/bin/env python3
"""plants_per_pot_gate -- A60: container_notes.plants_per_pot (PLA-580 spec 2026-09-21; register row 31).

THE FIELD. `container_notes.plants_per_pot` is an object whose only key is `readings`, a NON-EMPTY
list of per-pot capacity readings, or `null` where no T1 count has been read:

    "plants_per_pot": {"readings": [
        {"count": [4, 6], "at_gallons": [1, 1], "sources": ["uiuc_ext"],
         "anchoring_urls": {"uiuc_ext": {"url": "https://...", "verified": "2026-09-21"}}}
    ]}

A count and the pot size it was measured at are ONE DATUM and travel together (ruling 1). They are
NOT bound to `min_pot_gallons`: measured on 1721208e and re-measured on 079e3923, the dataset's
`min_pot_gallons` disagrees with the pot size Illinois states its counts against on 9 of 10 counted
rows, by 1.5x to 5x. So this gate DELIBERATELY DOES NOT assert `at_gallons >= min_pot_gallons`;
that assertion would fail on 9 of 10 authored rows and is the very confusion the field exists to
prevent (spec section 8). Do not add it.

THE VALUE DOMAIN, enumerated once, because `[]` is a CLAIM and a shape gate cannot see an absence:
  key ABSENT        an uncertified shell (A39 exempts by status). A violation on a certified crop.
  null              "no T1 count read". The legitimate state of 114 of the 121 certified crops.
  {readings: [..]}  one or more readings.
  {readings: []}    NOT legitimate. "Assessed, none found" is not a state this field has; absence
                    is spelled null. REFUSED.

SHAPE fires only when the key is PRESENT and non-null, so it arms GREEN on 079e3923 (0 of 128 crops
carry the key) and on every historical state. PRESENCE (a certified crop carries the key, null being
a value) is a SEPARATE entry point and `all_violations` leaves it OFF by default, because the floor
arms in whole_crop_gate A60 only in the commit that writes the canonical carrying the key -- gates
arm off the data, and armed early it reddens live canonical and floods a parallel session.

WHERE THE SHELL RULE IS ENFORCED, measured 2026-09-21 rather than assumed. `gate_all` iterates
CERTIFIED crops only, so a key appearing on an uncertified shell is INVISIBLE to it by
construction -- true of A58 and A59 as well, and not a property of this gate. Injected into a
scratch post-state, that defect is refused by `whole_crop_gate <shell>`, by this module's own CLI
(which walks all 128) and by the promote's `check_post` (`all_violations(presence=True)`, also all
128); `gate_all` returns 0. Do not read a green `gate_all` as covering the shells. Every other
defect class in this gate WAS measured to refuse through `gate_all`.

`at_gallons` IS ALWAYS `[lo, hi]`, `lo == hi` for a single stated size (amendment 3). One type per
field: no consumer, gate or test branches on scalar-vs-pair, and the conservative reader is
unconditionally `at_gallons[1]`. A scalar is a VIOLATION, not a shorthand.

BOUNDS are numeric_sanity_gate's (A33): `count` within [1, 30] and `at_gallons` within [0.5, 100].
The 0.5 floor differs from `min_pot_gallons`' 1..100 deliberately, because Illinois publishes a
half-gallon row.

Usage: plants_per_pot_gate.py [PATH] [--presence]
"""
import json
import re
import sys

FIELD = "plants_per_pot"
CERTIFIED = "verified_gs_arc"
READING_KEYS = ("count", "at_gallons", "sources", "anchoring_urls")
ANCHOR_KEYS = ("url", "verified")
PROVENANCE_FIELD = "plants_per_pot"
_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def _cn(crop):
    v = crop.get("container_notes")
    return v if isinstance(v, dict) else {}


def _num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _int(v):
    # bool is an int in Python; a count of `true` must not pass as 1.
    return isinstance(v, int) and not isinstance(v, bool)


def _certified(crop):
    return (crop.get("verification_status") or {}).get("status") == CERTIFIED


def _has_provenance(crop):
    fa = (crop.get("verification_status") or {}).get("field_additions") or []
    return any(isinstance(x, dict) and x.get("field") == PROVENANCE_FIELD for x in fa)


# ---------------------------------------------------------------------------------------------
# THE CONSUMER CONTRACT (spec 4.2, 4.3, 5.2, 7.2) -- the reference oracle PLA-539 (plant-app) and
# PLA-586 (plant-astro) implement. It lives here, beside the shape rules, so the two rulings it
# encodes are machine-pinned in the dataset repo BEFORE a consumer writes TypeScript against them,
# and so the promote can PIN the effect its own authoring has on the planner (check_post).
# ---------------------------------------------------------------------------------------------

def readings_of(crop):
    """The readings on a crop, or [] -- and ABSENT, `null` and `{readings: []}` all return [].

    The consumer contract (7.2 step 1, 7.3) makes those three states identical on purpose: a
    renderer shows no row and a planner falls back. The GATE still distinguishes them, because
    `{readings: []}` is a shape violation while null is the legitimate unassessed state.
    """
    v = _cn(crop).get(FIELD)
    if not isinstance(v, dict):
        return []
    rs = v.get("readings")
    if not isinstance(rs, list):
        return []
    return [r for r in rs if isinstance(r, dict)]


def conservative_gallons_per_plant(reading):
    """RULED, spec 4.2 as amended (amendment 4): `at_gallons[hi] / count[min]`.

    `at_gallons[hi]` is the roomier end of a banded size; `count[min]` is the smaller capacity
    claim. A pot Illinois says holds "4-6" lettuce is therefore priced as if it holds FOUR.
    Both ends are the conservative choice, and both are the contract rather than a preference.
    """
    return reading["at_gallons"][1] / reading["count"][0]


def switches(readings):
    """Ruling 3: the planner uses this field only where some reading's count is not [1, 1].

    On a count-1 row the field carries no capacity the planner did not already have (one plant,
    one pot), so switching would only replace one whole-container figure with another, more
    permissive, un-audited one. PLA-533 owns that audit. A reading of [1, 2] is NOT count-1 and
    does switch.
    """
    return any(r.get("count") != [1, 1] for r in readings)


def planner_gallons_per_plant(crop):
    """The planner's per-plant figure, or None meaning FALL BACK.

    None is 5.2's ruled fallback: `min_pot_gallons` is the smallest pot FOR THE CROP, not a
    per-plant volume, so with no usable reading the charge is ONE PLANT PER `min_pot_gallons`
    POT -- today's behavior, and the conservative one. There is no third case.

    Where the field is used, ruling 2 takes the MAXIMUM conservative figure across all readings,
    count-1 readings included: that is what lets UMD's cautious 10 gallons per plant restrain
    Illinois' 0.5, rather than being ignored because its own count happens to be 1.

    MODELED, NOT SOURCED (spec 4.4): a source states a capacity AT THE POT IT NAMES. Applying this
    per-plant figure to a pot of any other size assumes capacity is linear in root volume, and for
    multi-plant crops the binding constraint is probably surface area and spacing instead -- which
    is why Illinois gives a THINNING SPACING on exactly the four rows where it declines a count,
    why Wisconsin's only per-plant number for root crops is a spacing, and why strawberry's prose
    count is bound to a diameter. A planner must price arbitrary pots so the rule stays, but it is
    an app rule and no rendered sentence may state a count at a pot size no source named (7.1).
    Capacity-by-area is PLA-10's question; this field does not pre-empt the answer.
    """
    rs = readings_of(crop)
    if not rs or not switches(rs):
        return None
    return max(conservative_gallons_per_plant(r) for r in rs)


# ---------------------------------------------------------------------------------------------
# SHAPE / PRESENCE
# ---------------------------------------------------------------------------------------------

def shape_violations(crop):
    V = []
    slug = crop.get("slug") or "?"
    cn = _cn(crop)
    if FIELD not in cn:
        return V
    if not _certified(crop):
        V.append(f"{slug}: {FIELD} present on an uncertified crop; the shells carry no key "
                 f"(that is how A39 exempts them by status)")
        return V
    value = cn[FIELD]
    if value is None:
        return V
    if not isinstance(value, dict) or set(value) != {"readings"}:
        V.append(f"{slug}: {FIELD} must be null or an object whose only key is 'readings', "
                 f"got {json.dumps(value, ensure_ascii=False)[:120]}")
        return V
    readings = value["readings"]
    if not isinstance(readings, list) or not readings:
        V.append(f"{slug}: {FIELD}.readings must be a non-empty list of readings "
                 f"(absence is spelled null, never []), got {readings!r}")
        return V

    first_seen = {}
    for i, r in enumerate(readings):
        tag = f"{slug}/reading {i}"
        if not isinstance(r, dict) or set(r) != set(READING_KEYS):
            got = sorted(r) if isinstance(r, dict) else type(r).__name__
            V.append(f"{tag}: keys must be exactly {sorted(READING_KEYS)}, got {got}")
            continue

        c = r["count"]
        if not (isinstance(c, list) and len(c) == 2 and all(_int(x) for x in c)):
            V.append(f"{tag}: count must be a list of two integers [min, max], got {c!r}")
        elif c[0] < 1:
            V.append(f"{tag}: count min must be at least 1, got {c!r}")
        elif c[0] > c[1]:
            V.append(f"{tag}: count must satisfy min <= max, got {c!r}")

        g = r["at_gallons"]
        if not (isinstance(g, list) and len(g) == 2 and all(_num(x) for x in g)):
            V.append(f"{tag}: at_gallons must be a two-element list [lo, hi] of numbers, got "
                     f"{g!r} (a scalar is a violation, not a shorthand: one type per field)")
        elif g[0] <= 0 or g[1] <= 0:
            V.append(f"{tag}: at_gallons must be positive, got {g!r}")
        elif g[0] > g[1]:
            V.append(f"{tag}: at_gallons must satisfy lo <= hi, got {g!r}")

        srcs = r["sources"]
        if not (isinstance(srcs, list) and srcs and all(isinstance(s, str) and s for s in srcs)):
            V.append(f"{tag}: sources must be a non-empty list of source keys, got {srcs!r}")
            srcs = []

        au = r["anchoring_urls"]
        if not isinstance(au, dict):
            V.append(f"{tag}: anchoring_urls must be an object keyed by source, got {au!r}")
        else:
            for s in srcs:
                a = au.get(s)
                if not isinstance(a, dict):
                    V.append(f"{tag}: source {s!r} has no anchoring_urls entry")
                    continue
                if set(a) != set(ANCHOR_KEYS):
                    V.append(f"{tag}: anchoring_urls[{s!r}] keys must be exactly "
                             f"{sorted(ANCHOR_KEYS)}, got {sorted(a)}")
                    continue
                if not (isinstance(a["url"], str) and a["url"].startswith("http")):
                    V.append(f"{tag}: anchoring_urls[{s!r}].url is not a url: {a['url']!r}")
                # fullmatch, not search: PLA-114 had a guard pass on '202' matching a date.
                if not (isinstance(a["verified"], str) and _DATE.fullmatch(a["verified"])):
                    V.append(f"{tag}: anchoring_urls[{s!r}].verified is not a YYYY-MM-DD date: "
                             f"{a['verified']!r}")
            extra = sorted(set(au) - set(srcs))
            if extra:
                V.append(f"{tag}: anchoring_urls carries {extra} not in sources")

        for s in srcs:
            if s in first_seen:
                V.append(f"{slug}: source {s!r} appears in two readings ({first_seen[s]} and {i}); "
                         f"one institution speaks once per crop")
            else:
                first_seen[s] = i

    # A count is a capacity FOR A POT. A crop the dataset says cannot go in a pot has no capacity.
    if cn.get("container_ok") is not True:
        V.append(f"{slug}: {FIELD} is non-null but container_ok is {cn.get('container_ok')!r}; "
                 f"a per-pot count needs a crop that can go in a pot")

    # A value nobody can point at refuses (the amend-not-recert convention A40/A59 use).
    if not _has_provenance(crop):
        V.append(f"{slug}: authored {FIELD} on a certified crop with no field_additions entry "
                 f"for {PROVENANCE_FIELD!r}")
    return V


def presence_violations(crop):
    if not _certified(crop):
        return []
    if FIELD not in _cn(crop):
        return [f"{crop.get('slug') or '?'}: container_notes.{FIELD} missing "
                f"(present-or-null on a certified crop)"]
    return []


def all_violations(data, presence=False):
    V = []
    for c in data.get("crops", []):
        V += shape_violations(c)
        if presence:
            V += presence_violations(c)
    return V


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    path = args[0] if args else "crops_data_final.json"
    presence = "--presence" in argv
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    V = all_violations(data, presence=presence)
    for v in V:
        print("VIOLATION:", v)
    crops = data.get("crops", [])
    carrying = sum(1 for c in crops if FIELD in _cn(c))
    authored = sum(1 for c in crops if readings_of(c))
    nreadings = sum(len(readings_of(c)) for c in crops)
    switched = sorted(c["slug"] for c in crops if planner_gallons_per_plant(c) is not None)
    print(f"plants_per_pot_gate: {len(V)} violation(s); {carrying}/{len(crops)} crops carry the key, "
          f"{authored} authored carrying {nreadings} readings; presence "
          f"{'ARMED' if presence else 'off'}")
    print(f"  planner switches on {len(switched)}: " + ", ".join(
        f"{s} -> {planner_gallons_per_plant(next(c for c in crops if c['slug'] == s)):g} gal/plant"
        for s in switched))
    return 1 if V else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
