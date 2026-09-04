#!/usr/bin/env python3
"""problem_id_collision_gate -- refuse to mint a problem `id` that collides with precedent (PLA-449).

WHY THIS EXISTS. A `pests[]` / `diseases[]` `id` is a JOIN KEY: `varieties[].resistance` and
`varieties[].ladder_delta` point at it, and nothing else in the dataset does. Names join nothing.
Eight duplicate-id pairs were already minted by authoring passes that did not check precedent, and
`control_ladder_gate`'s IDENTITY check cannot see any of them because it only requires ids to be
unique WITHIN a crop. This gate is the cross-crop half.

It FLAGS, it does not refuse. A near-duplicate is very often correct scoping -- `aphids` ->
`cabbage-aphids`, `black-rot` -> `sweet-potato-black-rot` -- so the output is a decision surface,
and `problem_id_registry.json` is where a decision gets written down once and stops recurring.

THE CHECKS

  1. ID_NEAR_DUP   a minted id within edit distance 2 of any id already in the dataset.
  2. NAME_SHARED   a display name that, normalized, already appears under a different id.
  3. FAMILY_MEMBER an id whose name is exactly one conjunct of an ALREADY-FLAGGED id's name.

Check 3 is narrower than it looks and is deliberately not a general check. It runs only against
ids that checks 1 or 2 have already implicated, so it cannot open a family of its own and cannot
flood. It exists because the slug decision has three members -- `slugs`, `slugs-and-snails`,
`snails-and-slugs` -- and checks 1 and 2 reach only two of them: `slugs` is edit distance 11 from
`slugs-and-snails` and its display name "Slugs" shares no normalized key with "Slugs and snails".
Handing a reviewer two thirds of a decision is how the third id gets missed. Measured on a9c84847
it contributes exactly two pairs, both in that one family.

WHY CHECK 1 IS EDIT DISTANCE AND NOT THE STEM CHECK IT REPLACES. Batch 24 carried a per-batch
`_stem_key` comparison that stripped a trailing plural `s`. It would not have caught the pair batch
24 itself then minted: `pink-root` (alliums) against celery's `pink-rot`, which is edit distance 1
but stem-distinct. Every batch re-deriving its own narrower check is the mechanism this gate ends.

WHY CHECK 2 NORMALIZES. Transcribed from the problem-name normalization pass of 2026-09-03, whose
function is already written down and measured. Its parenthetical deletion is TOTAL, and that cuts
both ways on purpose: it is the only reason `gray-mold` reaches artichoke's `botrytis-gray-mold`
("Gray mold (Botrytis cinerea)"), and it is also why onion's "Botrytis (leaf blight and neck rot)"
collides with chamomile's "Botrytis (gray mold)" when the two are different diseases. Both
behaviours are pinned in the suite so neither can drift without a test going red.

Usage:
    problem_id_collision_gate.py [PATH]                  # audit the whole roster
    problem_id_collision_gate.py [PATH] --minted a,b,c   # batch apply: only pairs touching a,b,c
                                                         # NB: run against POST-APPLY data, or
                                                         # only check 1 reaches the minted ids
    problem_id_collision_gate.py [PATH] --strict         # exit 1 when anything is unregistered
    problem_id_collision_gate.py [PATH] --show-registered --json
"""
import argparse, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CANON = os.path.join(REPO, "crops_data_final.json")
REGISTRY_PATH = os.path.join(HERE, "problem_id_registry.json")

ID_NEAR_DUP = "ID_NEAR_DUP"
NAME_SHARED = "NAME_SHARED"
FAMILY_MEMBER = "FAMILY_MEMBER"

NEAR_DUP_MAX_DISTANCE = 2
CONJUNCTION = "and"
_HYPHENS = re.compile(r"[-‐‑‒–—/]")
_PAREN = re.compile(r"\([^)]*\)")
_NONWORD = re.compile(r"[^\w\s]")


# --------------------------------------------------------------------------------------------
# primitives
# --------------------------------------------------------------------------------------------
def edit_distance(a, b, cap=None):
    """Levenshtein. With `cap` set, any distance greater than `cap` may be reported as `cap + 1`
    -- enough to answer 'is this within the threshold' without paying for the full matrix. Called
    with cap=None it returns the exact distance, which is what the suite asserts against."""
    if a == b:
        return 0  # optimization only; the matrix below returns 0 for this case unaided
    if cap is not None and abs(len(a) - len(b)) > cap:
        return cap + 1
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def singular(t):
    """The plural rule from the 2026-09-03 normalization pass, transcribed unchanged. First
    matching branch wins; the `ss` guard sits between the -es family and the bare -s strip so
    `grass` and `moss` survive."""
    if len(t) <= 3:
        return t
    if t.endswith("ies") and len(t) > 4:
        return t[:-3] + "y"
    if t.endswith(("ses", "xes", "zes", "ches", "shes")):
        return t[:-2]
    if t.endswith("ss"):
        return t
    if t.endswith("s"):
        return t[:-1]
    return t


def normalize_tokens(name):
    """Normalized tokens IN ORDER. Order is kept here because check 3 splits on the conjunction,
    which a sorted form destroys."""
    s = _PAREN.sub("", name.lower()).replace("&", " and ")
    s = _NONWORD.sub("", _HYPHENS.sub(" ", s))
    return [singular(t) for t in s.split()]


def normalize_name(name):
    """The collision key: tokens sorted, so word order stops being a distinction."""
    return " ".join(sorted(normalize_tokens(name)))


def conjuncts(name):
    """`name` split on the conjunction into its parts, each as a collision key. "Slugs and snails"
    -> {"slug", "snail"}. A name with no conjunction yields nothing."""
    toks = normalize_tokens(name)
    if CONJUNCTION not in toks:
        return set()
    out, cur = set(), []
    for t in toks:
        if t == CONJUNCTION:
            if cur:
                out.add(" ".join(sorted(cur)))
            cur = []
        else:
            cur.append(t)
    if cur:
        out.add(" ".join(sorted(cur)))
    return out


def id_tokens_nested(a, b):
    """True when one id's tokens are a subset of the other's -- `slugs` inside `slugs-and-snails`.

    Check 3 requires this ON TOP OF the name-conjunct match, so two independent signals have to
    agree before a pair is opened. Without it the check leaks: viola's bundled "Leaf spots and
    anthracnose" matched the conjunct `anthracnose` and pulled in all three anthracnose-family ids,
    two of which share nothing with viola at all. That is the bundled-scope question of PLA-448
    s4d, which this gate deliberately does not answer."""
    x = {singular(t) for t in a.split("-")}
    y = {singular(t) for t in b.split("-")}
    return x < y or y < x


# --------------------------------------------------------------------------------------------
# registry -- the registration path for a deliberately new-but-similar id
# --------------------------------------------------------------------------------------------
class Registry:
    """A decision written down once. Each entry names a SET of ids that are deliberately distinct
    from one another, so a host-scoped family (`aphids` / `citrus-aphids` / `apricot-aphids`) is
    one decision rather than one row per pair."""

    def __init__(self, entries):
        self.entries = entries
        self._by_pair = {}
        for e in entries:
            ids = e["ids"]
            for i in range(len(ids)):
                for j in range(i + 1, len(ids)):
                    self._by_pair[tuple(sorted((ids[i], ids[j])))] = e

    def registered(self, a, b):
        return tuple(sorted((a, b))) in self._by_pair

    def reason(self, a, b):
        e = self._by_pair.get(tuple(sorted((a, b))))
        return None if e is None else "%s [%s]" % (e["reason"], e["ruled"])


def load_registry(path=REGISTRY_PATH):
    with open(path) as f:
        return Registry(json.load(f)["deliberately_distinct"])


# --------------------------------------------------------------------------------------------
# findings
# --------------------------------------------------------------------------------------------
class Finding:
    __slots__ = ("pair", "kinds", "crops", "names", "evidence", "registered", "reason")

    def __init__(self, pair, kinds, crops, names, evidence, registered, reason):
        self.pair, self.kinds, self.crops, self.names = pair, kinds, crops, names
        self.evidence, self.registered, self.reason = evidence, registered, reason

    def __repr__(self):
        return "<%s %s %s>" % ("REGISTERED" if self.registered else "OPEN",
                               "/".join(sorted(self.kinds)), " <-> ".join(self.pair))

    def as_dict(self):
        return {"ids": list(self.pair), "kinds": sorted(self.kinds), "evidence": self.evidence,
                "crops": self.crops, "names": self.names,
                "registered": self.registered, "reason": self.reason}


# The microgreen crops carry `name_seasoned` / `name_beginner` and NO `name`, so a name-keyed
# check is blind to them unless it is taught the schema. Seven of them are an unladdered PLA-8
# family: when they ladder, an id like `damping-off-microgreens` sits edit distance 11 from
# `damping-off`, so check 1 would not see it either. Adding the fallback is free on a9c84847 --
# the only id-ed crop on that schema is `microgreens-mix`, whose two names normalize onto ids it
# already shares -- and it closes the hole before the batch rather than after.
DISPLAY_NAME_FIELDS = ("name", "name_seasoned", "name_beginner")


def display_names(entry):
    """Every display string an entry carries, most-specific schema first."""
    return [entry[f] for f in DISPLAY_NAME_FIELDS if entry.get(f)]


def index(data):
    """id -> crops holding it, id -> display names carried under it."""
    crops, names = {}, {}
    for c in data.get("crops") or []:
        for field in ("pests", "diseases"):
            for e in c.get(field) or []:
                pid = e.get("id")
                if not pid:
                    continue
                crops.setdefault(pid, set()).add(c["slug"])
                for n in display_names(e):
                    names.setdefault(pid, set()).add(n)
    return crops, names


def checks_unavailable_for(data, minted):
    """The minted ids that `data` carries no display name for, sorted.

    Checks 2 and 3 both key off the display name, so for these ids only check 1 runs -- a THIRD of
    the guard, behind an output that looks complete. Run the gate against the POST-APPLY data
    (a scratch copy is fine) to get all three. The CLI refuses to stay quiet about this."""
    _, names = index(data)
    return sorted(i for i in (minted or ()) if not names.get(i))


def scan(data, minted=None, registry=None):
    """Every colliding id pair, most-evidence first.

    `minted` restricts the report to pairs where at least one side is a newly minted id -- the
    batch-apply mode. Ids in `minted` that are not yet present in `data` are still compared, so the
    gate can run before the batch is applied as well as after."""
    crops, names = index(data)
    universe = set(crops) | set(minted or ())
    hits = {}

    def add(a, b, kind, evidence):
        p = tuple(sorted((a, b)))
        if p in hits:
            hits[p][0].add(kind)
            hits[p][1].append(evidence)
        else:
            hits[p] = ({kind}, [evidence])

    # 1. near-duplicate id
    ids = sorted(universe)
    for i, x in enumerate(ids):
        for y in ids[i + 1:]:
            d = edit_distance(x, y, cap=NEAR_DUP_MAX_DISTANCE)
            if d <= NEAR_DUP_MAX_DISTANCE:
                add(x, y, ID_NEAR_DUP, "id edit distance %d" % d)

    # 2. a display name already live under a different id
    by_key = {}
    for pid in sorted(universe):
        for n in sorted(names.get(pid) or ()):
            by_key.setdefault(normalize_name(n), {}).setdefault(pid, []).append(n)
    for key, owners in sorted(by_key.items()):
        if len(owners) < 2:
            continue
        o = sorted(owners)
        for i, x in enumerate(o):
            for y in o[i + 1:]:
                add(x, y, NAME_SHARED, "name %r == %r once normalized"
                    % (owners[x][0], owners[y][0]))

    # 3. family completion, scoped to ids checks 1 and 2 already implicated
    implicated = {i for p in list(hits) for i in p}
    for pid in sorted(implicated):
        for n in sorted(names.get(pid) or ()):
            for part in sorted(conjuncts(n)):
                for other in sorted(by_key.get(part, {})):
                    if other == pid or not id_tokens_nested(pid, other):
                        continue
                    add(pid, other, FAMILY_MEMBER,
                        "%r is one conjunct of %r, and the ids nest"
                        % (by_key[part][other][0], n))

    out = []
    for p, (kinds, ev) in hits.items():
        if minted is not None and not (set(p) & set(minted)):
            continue
        reg = bool(registry and registry.registered(*p))
        out.append(Finding(
            pair=p, kinds=kinds,
            crops={i: sorted(crops.get(i) or ()) for i in p},
            names={i: sorted(names.get(i) or ()) for i in p},
            evidence="; ".join(sorted(set(ev))), registered=reg,
            reason=registry.reason(*p) if reg else None))
    out.sort(key=lambda f: (f.registered, -len(f.kinds), f.pair))
    return out


# --------------------------------------------------------------------------------------------
def report(findings, show_registered=False):
    openf = [f for f in findings if not f.registered]
    regf = [f for f in findings if f.registered]
    for f in openf:
        a, b = f.pair
        print("OPEN  %-14s %s [%dc] <-> %s [%dc]"
              % ("/".join(sorted(f.kinds)), a, len(f.crops[a]), b, len(f.crops[b])))
        print("        %s" % f.evidence)
        for i in f.pair:
            print("        %-28s %s" % (i, ", ".join(f.crops[i]) or "(minted, not yet applied)"))
    if show_registered:
        for f in regf:
            print("REG   %s <-> %s  -- %s" % (f.pair[0], f.pair[1], f.reason))
    print("\n%d findings: %d OPEN, %d registered" % (len(findings), len(openf), len(regf)))
    return openf


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("path", nargs="?", default=CANON)
    ap.add_argument("--minted", default=None,
                    help="comma-separated ids being minted by this batch")
    ap.add_argument("--strict", action="store_true", help="exit 1 when anything is unregistered")
    ap.add_argument("--show-registered", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    with open(a.path) as f:
        data = json.load(f)
    minted = {s.strip() for s in a.minted.split(",") if s.strip()} if a.minted else None
    findings = scan(data, minted=minted, registry=load_registry())
    blind = checks_unavailable_for(data, minted) if minted else []
    if blind:
        sys.stderr.write(
            "WARNING: %d minted id(s) carry no display name in this file, so ONLY the id "
            "edit-distance check ran on them: %s\n         Re-run against the post-apply data to "
            "get the name and family checks.\n" % (len(blind), ", ".join(blind)))
    if a.json:
        json.dump([f.as_dict() for f in findings], sys.stdout, indent=2)
        sys.stdout.write("\n")
        openf = [f for f in findings if not f.registered]
    else:
        openf = report(findings, a.show_registered)
    return 1 if (a.strict and openf) else 0


if __name__ == "__main__":
    sys.exit(main())
