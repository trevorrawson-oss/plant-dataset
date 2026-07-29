#!/usr/bin/env python3
"""Region-prose vs cell-rating coherence (post-asparagus hardening item 1, artichoke GS arc).

THE DEFECT. Region prose and per-cell suitability ratings are two layers that the same guide
renders to the SAME READER, and nothing in this suite compared them. After the asparagus
suitability re-rating, `ca_north_coast`'s region_notes still read "both zones 9 and 10
perennialize only marginally" for two cells that had just been promoted to `perennializes`. A36
checks that both registers EXIST. A29 checks they are AUTHORED. Neither reads what they SAY. The
asparagus lane then reproduced the same defect within an hour of writing it down, while actively
watching for it, which is the argument for a gate instead of a review step.

ONE CHECK: SUIT-BOUND. A clause that binds a ZONE OF THIS REGION to a SUITABILITY CONCEPT is an
assertion about that cell, and it must match what the cell actually says.

    "Frost-free zone 11 is unsuitable."   with ca_south_coast z11 rated `marginal`

That is the whole gate, and the narrowness was bought with evidence rather than caution.

=============================================================================================
WHAT THE FIRST VERSION GOT WRONG, MEASURED ON THE LIVE ROSTER (2026-07-28)
=============================================================================================
The first version shipped three checks. Run roster-wide it produced 38 findings across 17 crops,
and the arc that wrote it reported those as "real findings on long-certified fruit trees" WITHOUT
READING THEM. They were then read. **Exactly one was a defect.**

  SUIT-WORD (bare keyword, any position) -- 10 false positives out of 11. Consumer prose names a
  rating constantly, about things that are not this region's cells:
      "so mandarins fruit reliably here where a navel is only marginal"   <- a DIFFERENT CROP
      "it is only marginal in colder parts of the Gulf South"             <- a DIFFERENT REGION
      "Meyer lemon ... bred for marginal climates"                        <- a descriptive phrase
      "what turn a marginal fall race into a dependable harvest"          <- a metaphor
  Every one of those sentences is correct, useful writing. A check that flags them is not strict,
  it is wrong, and the only way to satisfy it is to make the copy worse.

  SPLIT-VOICE (a multi-rating region must name a zone number) -- 25 findings, ZERO defects, and
  the check was actively harmful. It never detects a CONTRADICTION, only under-differentiation,
  and good consumer prose routinely differentiates by PLACE rather than by zone number:
      pear-european ca_north_coast: "inland (Lake County and Mendocino) ... right at the
      fog-cooled coast ... a survive-but-rarely-fruit edge"  -- perfectly differentiated, no
      zone numbers, flagged anyway.
  Satisfying it would have meant pushing zone integers into prose that reads better without them.
  DELETED rather than narrowed: a check whose findings are all noise trains people to ignore the
  gate, which is worse than not having it.

  ZONE-SPAN (a named zone must be inside the region's span) -- 1 finding, a false positive.
  Prose legitimately names a zone to mark the boundary BEYOND this region:
      mandarin northern_tier: "hybrids extend only to about zone 8a; north of that, citrus is a
      container crop"  -- correct, and flagged because 8 is not in the z3-z7 span.
  FOLDED INTO SUIT-BOUND instead of deleted: an out-of-span zone is only a defect when a RATING
  is asserted for it, which is the stale-after-a-span-change shape the check was written for.

The one survivor is `asparagus.ca_south_coast`, and it survives because its rating word is bound
to a zone OF THIS REGION. That binding is the entire difference between signal and noise here.

KNOWN LIMIT, recorded rather than papered over. The rule is ANY-MATCH: a clause is clean if it
names the cell's actual rating. So the FLAT CONTRADICTION form is caught ("zone 11 is unsuitable"
on a marginal cell) but the HEDGED form is not -- including, ironically, the original asparagus
sentence that motivated the whole item, "both zones 9 and 10 perennialize only marginally" for
cells rated `perennializes`, which names both ratings and passes. Tightening to an exact-set match
would fire on correct writing like "zone 9 is marginal to unsuitable depending on the season", and
separating a hedge from a legitimate multi-rating clause needs precisely the fuzzy semantics that
produced 37 false positives above. A future pass wanting the hedge needs a different mechanism,
not a wider net.

=============================================================================================
SCOPE
=============================================================================================
ROSTER-WIDE and HARD as of 2026-07-28, wired into whole_crop_gate as **A51**.

It shipped soft with the trigger "fold roster-wide once `--all` is clean", and `--all` reached
clean the same day -- not by suppressing findings but by narrowing the check to what it can
actually decide (38 -> 3 on the narrowing, 3 -> 0 once nearest-zone binding and range-compound
suppression landed) and then REPAIRING the one real defect it found. Every remaining crop passes
on its own merits, so there was nothing left to scope around: it runs on all 128.

That makes this the first check in the suite to ship roster-wide rather than archetype-scoped,
and the reason is that the defect it looks for is not archetype-specific. Any crop with region
prose and per-cell ratings can contradict itself.

Usage:
  python3 tools/region_prose_gate.py [PATH]          # archetype-scoped (the gate)
  python3 tools/region_prose_gate.py [PATH] --all    # roster-wide (the audit)
Exit 1 on any violation in the scoped run.
"""
import json
import re
import sys

ARCHETYPE = "herbaceous_perennial"

# A rating concept, and the ways consumer prose actually NAMES it. The natural-language forms are
# the point: nobody writes "survives_no_fruit" at a reader, they write "ornamental only", so
# matching the bare enum value would make the check vacuous on exactly the copy it must read.
RATING_WORDS = {
    "perennializes": [r"\bperennializ\w*"],
    "marginal": [r"\bmarginal\w*"],
    # `annual_only` (2026-07-28). Matched on the phrases prose ACTUALLY uses -- "grown as an
    # annual", "replant each spring" -- not the enum name, which no one writes at a reader. The
    # bare word "annual" is deliberately NOT a pattern: it is the single commonest word in this
    # corpus ("annual culture", "an annual crop", "the annual cycle") and matching it would
    # reproduce the keyword flood this gate was rebuilt to escape.
    "annual_only": [r"\bannual[\s-]only\b", r"\bgrown as an annual\b",
                    r"\breplant(?:ed|ing)? each (?:year|spring|season|autumn|fall)\b"],
    "unsuitable": [r"\bunsuitable\b"],
    "survives_no_fruit": [r"\bsurvives_no_fruit\b", r"\bornamental[\s-]only\b",
                          r"\bornamental\s+only\b"],
    "fruits_reliably": [r"\bfruits_reliably\b", r"\bfruits?\s+reliably\b"],
}

# CONTRASTIVE FRAMES. Good prose names the rating it is NOT ("declines rather than perennializing",
# "rated survives_no_fruit rather than unsuitable"). A rating word preceded by one of these within
# a short window is not an assertion of that rating. The window is deliberately short: a cue three
# words back is a contrast, the same phrase two sentences earlier is unrelated.
_CONTRAST_CUES = (r"rather than", r"instead of", r"as opposed to", r"not\b", r"never\b",
                  r"no longer", r"far from", r"stops? short of", r"other than")
_CONTRAST_RE = re.compile(r"(?:" + "|".join(_CONTRAST_CUES) + r")\W{0,3}$", re.I)
_CONTRAST_WINDOW = 26

# Clause boundaries. Commas and parentheses are load-bearing, not cosmetic: "(zone 10
# marginal-to-none, zone 11 effectively chill-free)" is TWO assertions, and "hardy through zone 8
# ..., so mandarins fruit reliably here where a navel is only marginal" is a zone clause followed
# by a rating clause that must NOT be joined to it.
_CLAUSE_SPLIT = re.compile(r"[.;:,()—]|\s--\s")

# "zone 9", "zone9", "zone 8a", "zones 9 and 10", "zones 10 through 13"
_ZONE_RE = re.compile(r"\bzones?\s*(\d+)[a-b]?", re.I)
_ZONE_LIST_RE = re.compile(
    r"\bzones?\s*\d+[a-b]?(?:\s*(?:and|to|through|-|–|,)\s*\d+[a-b]?)+", re.I)


def _prose(region):
    """Both registers. A contradiction shown only to beginners is still a contradiction."""
    return " ".join(str(region.get(k) or "")
                    for k in ("region_notes_seasoned", "region_notes_beginner")).strip()


def zone_groups(text):
    """[(start, end, {zones})] for each zone mention in `text`, in order.

    An explicit LIST ("zones 9 and 10", "zones 10 through 13") is ONE group binding all its
    numbers, because a rating asserted about it applies to every zone named. Separate mentions
    are separate groups, which is what makes nearest-zone binding possible.
    """
    groups, claimed = [], []
    for m in _ZONE_LIST_RE.finditer(text):
        groups.append((m.start(), m.end(), set(re.findall(r"\d+", m.group(0)))))
        claimed.append((m.start(), m.end()))
    for m in _ZONE_RE.finditer(text):
        if any(a <= m.start() < b for a, b in claimed):
            continue
        groups.append((m.start(), m.end(), {m.group(1)}))
    return sorted(groups)


def zones_in(text):
    """Every zone number named in `text` (order-insensitive)."""
    out = set()
    for _, _, zs in zone_groups(text):
        out |= zs
    return out


# RANGE COMPOUNDS. "zone 10 marginal-to-none" is a SPAN, not a point claim: it says the answer
# lies somewhere between marginal and nothing, which is compatible with a `survives_no_fruit` cell
# at the "none" end. A rating word sitting at either end of an explicit X-to-Y compound is a range
# endpoint, not an assertion that the cell IS that value.
_RANGE_AFTER = re.compile(r"^\s*[-\u2013]\s*to\s*[-\u2013]?\s*\w", re.I)
_RANGE_BEFORE = re.compile(r"\w\s*[-\u2013]\s*to\s*[-\u2013]\s*$", re.I)


def _assertions(clause, pattern):
    """Positions where `pattern` is genuinely ASSERTED (not contrastive, not a range endpoint)."""
    out = []
    for m in re.finditer(pattern, clause):
        before = clause[max(0, m.start() - _CONTRAST_WINDOW):m.start()]
        if _CONTRAST_RE.search(before):
            continue
        if _RANGE_AFTER.match(clause[m.end():m.end() + 12]) or _RANGE_BEFORE.search(before):
            continue
        out.append((m.start(), m.end()))
    return out


def _asserted(clause, pattern):
    return bool(_assertions(clause, pattern))


def ratings_asserted_in(clause):
    return {v for v, pats in RATING_WORDS.items() if any(_asserted(clause, p) for p in pats)}


def bound_claims(clause):
    """{zone: {ratings}} -- each asserted rating bound to its NEAREST zone mention.

    A clause routinely carries TWO zone-scoped claims joined by "and":
        "These fruit reliably from about zone 5 up and survive to zone 4"
        "with zone 4 a marginal fruiting edge ... and zone 3 too cold"
    Binding every rating to every zone in the clause flags both of those correct sentences.
    Nearest-mention binding reads them the way a person does. Preceding mentions win ties,
    since "zone 4 a marginal edge" is the dominant idiom.
    """
    groups = zone_groups(clause)
    if not groups:
        return {}
    out = {}
    for value, pats in RATING_WORDS.items():
        for p in pats:
            for a, b in _assertions(clause, p):
                gs, ge, zs = min(groups, key=lambda g: (
                    (a - g[1]) if g[1] <= a else (g[0] - b) + 0.5))
                for z in zs:
                    out.setdefault(z, set()).add(value)
    return out


def region_prose_violations(crop, scoped=True):
    """Return a list of violation strings ([] = clean). No-op off the archetype when scoped."""
    if scoped and crop.get("archetype") != ARCHETYPE:
        return []
    V = []
    slug = crop.get("slug", "?")
    for rk, r in (crop.get("regions") or {}).items():
        if not isinstance(r, dict):
            continue
        rbz = r.get("resolved_by_zone") or {}
        actual = {z: c.get("suitability") for z, c in rbz.items()
                  if isinstance(c, dict) and c.get("suitability")}
        if not actual:
            continue  # admission state -- an unrated region is A46/A29's business, not this gate's
        text = _prose(r)
        if not text:
            continue  # unauthored prose is A29's finding; do not double-report it
        span = {str(z) for z in (r.get("zone_span") or [])} or set(actual)

        for clause in _CLAUSE_SPLIT.split(text):
            low = clause.lower()
            for z, said in sorted(bound_claims(low).items(), key=lambda kv: int(kv[0])):
                if z not in span:
                    V.append(
                        f"STALE-ZONE: {slug}.{rk}: prose asserts {sorted(said)} for zone {z}, "
                        f"which is outside the region's span {sorted(span, key=int)}. Prose left "
                        f"stale after a span change, or the wrong region. Clause: "
                        f"{clause.strip()!r}")
                elif z in actual and actual[z] not in said:
                    V.append(
                        f"SUIT-BOUND: {slug}.{rk}: prose says zone {z} is {sorted(said)} but the "
                        f"cell is {actual[z]!r}. Two layers the same guide shows the same reader "
                        f"disagree; decide which is right before editing either. Clause: "
                        f"{clause.strip()!r}")
    return V


def main(path, everything=False):
    data = json.load(open(path, encoding="utf-8"))
    total, hit = 0, set()
    for crop in data["crops"]:
        for v in region_prose_violations(crop, scoped=not everything):
            print(f"  {v}")
            total += 1
            hit.add(crop.get("slug"))
    scope = "roster-wide (AUDIT)" if everything else f"archetype == {ARCHETYPE!r}"
    print(f"region prose gate: {total} violation(s) across {len(hit)} crop(s) / "
          f"{len(data['crops'])} scanned (scope: {scope})")
    return 1 if (total and not everything) else 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    sys.exit(main(args[0] if args else "crops_data_final.json", "--all" in sys.argv))
