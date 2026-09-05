#!/usr/bin/env python3
"""promote_pla8_batch26 -- PLA-8 batch 26, the trees and shrubs.

mulberry, pawpaw, pear-asian, pear-european, persimmon, pomegranate.

WHAT THIS BATCH INHERITS FROM 25. The target-spec shape: `pinned_ids.json` is a TARGET STATE, every
canonical problem must be accounted for exactly once (carried, renamed, consumed by a split, or
named in `_retired`), and every changed prose leaf must match a DECLARED correction with its own
reason and anchor, or the promote refuses. Retirement is declared, never inferred from absence.

WHAT IS DIFFERENT HERE, and why each difference is a guard rather than a note.

1. THE TYPE SITUATION IS MIXED BY CROP, and it is the eighth distinct type situation in eight
   batches. Four crops carry only the coarse `pest`/`disease` (mulberry, pawpaw, persimmon,
   pomegranate); the two pears carry fine types EXCEPT "Pear decline", which carries `other`, a
   value no gate recognizes. Batch 23's guard asserted a UNIFORMLY coarse pre-state; batch 24's
   set types from nothing. Neither shape fits, so the pre-state type is PINNED PER ROW and the
   guard asserts both halves: coarse and `other` rows must be upgraded to a recognized fine type,
   fine rows must be carried unchanged unless a retype reason is declared.

2. THREE RETIREMENTS ARE ARRAY DUPLICATES, not non-problems. pear-asian carries "Pear scab" in
   BOTH pests[] and diseases[]; pear-european carries "Pear scab" AND "Fabraea leaf spot" in both.
   The pests[] copies are the older originals (2026-06-11); the diseases[] copies were added at the
   2026-07-02 certification without removing the first. Shipping both under one id fails
   `control_ladder_gate`'s within-crop identity check, and shipping them under two ids mints a
   duplicate join key on purpose. So the pests[] copies retire, and the guard proves each retired
   row IS a duplicate: a same-named diseases[] entry must exist in canonical and be carried by the
   pin table. A retirement that would delete a unique problem is refused.

3. THE TWO PEARS ARE TEMPLATE TWINS. Three of their entries are byte-identical across the crops
   (Pear scab, Pear psylla, Pear decline). Batch 22's rule applies: identical source prose cannot
   support two different ladders unless the divergence is adjudicated and pinned, because there is
   nothing else for a difference to come from -- EXCEPT that here each pear had its own record
   reviewer reading its own documents, which is exactly where a legitimate divergence would come
   from. So divergences are allowed when pinned with the record evidence, and refused otherwise.
   Same-named entries must also share their id: a shared disease shares its join key.

4. PLA-457 IS HELD, NOT RESOLVED. `control_methods.horticultural_oil` states a sulfur/oil spacing
   interval that disagrees with its own anchor, and a roster-wide ruling is pending. No rung note
   or correction in this batch may state such an interval, whichever figure it gives.

Usage:
    promote_pla8_batch26.py            # check, apply, verify, write
    promote_pla8_batch26.py --check    # checks only, write nothing
"""
import argparse, copy, difflib, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CANON = os.path.join(REPO, "crops_data_final.json")
STAGE = os.path.join(HERE, "staging", "pla8_batch26_trees")
PINS = os.path.join(STAGE, "pinned_ids.json")

sys.path.insert(0, HERE)
from control_ladder_gate import TYPE_TARGETS, UNIVERSAL_TARGET, TIER_RANK  # noqa: E402

BASE_SHA = "ce98b0a6f83cc04b380a6c3be3009709a7c6c3626b2611c88fafec1164997144"  # batch 25 + rosemary cert-log correction
CROPS = ("mulberry", "pawpaw", "pear-asian", "pear-european", "persimmon", "pomegranate")
PEARS = ("pear-asian", "pear-european")

ADVICE_FIELDS = ("note_beginner", "note_seasoned")
PROSE_FIELDS = ("symptoms_beginner", "symptoms_seasoned", "cause_beginner", "cause_seasoned",
                "organic_treatment_beginner", "organic_treatment_seasoned",
                "prevention_beginner", "prevention_seasoned")
PINNED_FIELDS = ("id", "type", "severity", "control_ladder", "sources", "anchoring_urls")
COARSE_TYPES = ("pest", "disease", "other")   # values a recognized gate type must replace

COPY_THRESHOLD = 0.70
MIN_RUN_GRAMS = 3        # six-word runs shared with one donor before it counts as a lift
TEMP_FIGURE = re.compile(r"\b\d{2,3}\s*°\s*F\b")
FROM_RE = re.compile(r"^(?:RENAME|SPLIT \d+/\d+) from '([^']+)'")
# Prose must not name the machinery. Underscore forms only: natural English "applies to" is fine.
LADDER_VOCAB = re.compile(r"\b(rungs?|ladders?|tiers?)\b|applies_to|control_method", re.I)
# PLA-457: a sentence that names BOTH sulfur and oil AND a duration is stating the held interval.
SULFUR = re.compile(r"\bsul(?:f|ph)ur\b", re.I)
OIL = re.compile(r"\boils?\b", re.I)
DURATION = re.compile(r"\b(\d+|one|two|three|four|several)\s*(days?|weeks?|months?)\b|\bmonth\b", re.I)

# Adjudicated pear divergences: name -> (methods only in pear-asian, methods only in pear-european).
# MEASURED against the authored output after the independent review; a divergence not listed here
# is refused. Pear decline converged once the pear-asian review found USU's "Grafting and budding
# can also transmit this phytoplasma" on the entry's own anchor (the clean-stock refusal was wrong).
# Pear scab stays divergent BY DOCUMENT: UC IPM PN 7413 says Asian pears "are less susceptible to
# scab than European pears", and its only named scab-resistant cultivars are European, so the
# resistant-varieties rung has nothing to name on pear-asian; both pear reviewers graded the shorter
# Asian ladder as justified by its own documents.
TWIN_DIVERGENCE_PINS = {
    "Pear scab": ((), ("resistant_varieties", "water_at_the_base")),
}


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def serialize(data):
    """CANONICAL IS COMPACT. separators, ensure_ascii=False, no trailing newline, never indent."""
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sentences(text):
    return [s.strip().lower() for s in re.split(r"(?<=[.!?])\s+", text or "") if len(s.strip()) > 25]


def problems(crop):
    for f in ("pests", "diseases"):
        for p in crop.get(f) or []:
            yield f, p


def by_slug(data):
    return {c["slug"]: c for c in data["crops"]}


def source_name(row):
    m = FROM_RE.match(row.get("from", ""))
    return m.group(1) if m else row["name"]


def spec_rows(pins):
    for crop, fields in pins.items():
        if crop.startswith("_"):
            continue
        for field in ("pests", "diseases"):
            for row in fields.get(field, []):
                yield crop, field, row


def prose_key(entry):
    return tuple(entry.get(k) or "" for k in PROSE_FIELDS)


# ---------------------------------------------------------------- load

def load_canonical():
    raw = open(CANON, "rb").read()
    got = sha256_bytes(raw)
    if got != BASE_SHA:
        sys.exit(f"REFUSED: base SHA mismatch.\n  expected {BASE_SHA}\n  got      {got}")
    return json.loads(raw.decode("utf-8"))


def staged():
    pins = json.load(open(PINS, encoding="utf-8"))
    batch = {}
    for c in CROPS:
        p = os.path.join(STAGE, f"out_{c}.json")
        if not os.path.exists(p):
            sys.exit(f"REFUSED: missing staged output {p}")
        batch[c] = json.load(open(p, encoding="utf-8"))
    return pins, batch


# ---------------------------------------------------------------- checks

def check_reconcile(pins, data):
    """Every canonical problem accounted for exactly once. Retirement DECLARED, not inferred."""
    idx = by_slug(data)
    canon = {(c, f, e["name"]) for c in CROPS for f in ("pests", "diseases")
             for e in idx[c].get(f) or []}
    consumed, bad = {}, []
    for crop, field, row in spec_rows(pins):
        key = (crop, field, source_name(row))
        if key not in canon:
            bad.append(f"PHANTOM SOURCE: {crop}/{field} {row['name']!r} draws from "
                       f"{source_name(row)!r}, absent from canonical")
        consumed.setdefault(key, []).append(row["name"])
    for r in pins.get("_retired", []):
        key = (r["crop"], r["field"], r["name"])
        if key not in canon:
            bad.append(f"PHANTOM RETIREMENT: {key}")
        if key in consumed:
            bad.append(f"CONTRADICTION: {key} both retired and used by {consumed[key]}")
        consumed.setdefault(key, []).append("<retired>")
    for key in sorted(canon - set(consumed)):
        bad.append(f"UNACCOUNTED: {key} is neither carried, renamed, split-from, nor retired")
    if bad:
        raise SystemExit("REFUSED: reconcile failed:\n  " + "\n  ".join(bad))
    return len(canon), sum(1 for _ in spec_rows(pins))


def check_retirements_are_array_duplicates(pins, data):
    """A retired row must be a pests[] copy of a diseases[] entry that SURVIVES. Retiring anything
    else would delete a unique problem under the cover of de-duplication."""
    idx = by_slug(data)
    carried = {(c, f, source_name(r)) for c, f, r in spec_rows(pins)}
    n = 0
    for r in pins.get("_retired", []):
        dup = r.get("duplicate_of") or {}
        if r["field"] != "pests" or dup.get("field") != "diseases" or dup.get("name") != r["name"]:
            raise SystemExit(f"REFUSED: retirement {r['crop']}/{r['field']}/{r['name']!r} is not "
                             f"declared as a pests[] duplicate of a same-named diseases[] entry")
        twin = next((e for e in idx[r["crop"]].get("diseases") or [] if e["name"] == r["name"]),
                    None)
        if twin is None:
            raise SystemExit(f"REFUSED: retirement {r['crop']}/{r['name']!r} names a diseases[] "
                             f"twin that does not exist in canonical; this is not a duplicate")
        if (r["crop"], "diseases", r["name"]) not in carried:
            raise SystemExit(f"REFUSED: retirement {r['crop']}/{r['name']!r}: the diseases[] twin "
                             f"is not carried by the pin table, so the problem would vanish")
        gone = next(e for e in idx[r["crop"]]["pests"] if e["name"] == r["name"])
        if gone.get("type") not in ("fungal", "bacterial", "viral", "disease"):
            raise SystemExit(f"REFUSED: retirement {r['crop']}/{r['name']!r}: the pests[] copy is "
                             f"typed {gone.get('type')!r}, not a disease sitting in the wrong array")
        n += 1
    if n == 0:
        raise SystemExit("REFUSED: no retirements declared; the three pear array duplicates were "
                         "measured and must be retired, so zero means the pin table lost them")
    return n


def check_type_upgrade(pins, data):
    """The PRE type is pinned per row; the POST type is the pinned fine type. Coarse and `other`
    rows must be upgraded; fine rows must be carried unchanged unless a retype is declared."""
    idx = by_slug(data)
    upgraded = carried = 0
    for crop, field, row in spec_rows(pins):
        src = next(e for e in idx[crop].get(field) or [] if e["name"] == source_name(row))
        pre = row.get("pre_type")
        if pre is None:
            raise SystemExit(f"REFUSED: {crop}/{row['name']!r} pins no pre_type")
        if src.get("type") != pre:
            raise SystemExit(f"REFUSED: {crop}/{row['name']!r} canonical type {src.get('type')!r} "
                             f"but pre_type pinned {pre!r}; re-measure, never retune")
        post = row["type"]
        if post not in TYPE_TARGETS:
            raise SystemExit(f"REFUSED: {crop}/{row['name']!r} pinned type {post!r} is not a "
                             f"recognized gate type")
        if pre in COARSE_TYPES:
            if post == pre:
                raise SystemExit(f"REFUSED: {crop}/{row['name']!r} type was not upgraded off "
                                 f"{pre!r}")
            upgraded += 1
        else:
            if post != pre and not row.get("retype_reason"):
                raise SystemExit(f"REFUSED: {crop}/{row['name']!r} fine type {pre!r} retyped to "
                                 f"{post!r} with no retype_reason")
            carried += 1
    if upgraded == 0 or carried == 0:
        raise SystemExit(f"REFUSED: the type situation was measured MIXED (coarse crops and fine "
                         f"crops); this pin table has {upgraded} upgrades and {carried} carries")
    return upgraded, carried


def check_batch_matches_spec(pins, batch):
    """The authored output must be exactly the target spec: same rows, same order, pinned values."""
    for crop in CROPS:
        for field in ("pests", "diseases"):
            want = pins[crop].get(field, [])
            got = batch[crop].get(field) or []
            if len(want) != len(got):
                raise SystemExit(f"REFUSED: {crop}/{field} has {len(got)} entries, spec has "
                                 f"{len(want)}")
            for w, g in zip(want, got):
                for k in ("name", "id", "type", "severity"):
                    if g.get(k) != w[k]:
                        raise SystemExit(f"REFUSED: {crop}/{field}/{w['name']!r} {k}={g.get(k)!r} "
                                         f"but pinned {w[k]!r}")


def check_ladders(batch, cm):
    """Non-empty, known methods, non-decreasing tier, applies_to reachable, no repeats.

    `[]` is not `None`: an empty ladder once passed every gate in this repo, so it is refused here
    explicitly rather than left to a truthiness test."""
    n = 0
    for crop in CROPS:
        for field, p in problems(batch[crop]):
            ladder = p.get("control_ladder")
            if not isinstance(ladder, list) or not ladder:
                raise SystemExit(f"REFUSED: {crop}/{p['id']} control_ladder must be a non-empty list")
            last, seen = -1, set()
            for i, r in enumerate(ladder):
                where = f"{crop}/{p['id']}/rung{i}"
                m = cm.get(r.get("method"))
                if m is None:
                    raise SystemExit(f"REFUSED: {where} unknown method {r.get('method')!r}")
                if r["method"] in seen:
                    raise SystemExit(f"REFUSED: {where} repeats method {r['method']!r}")
                seen.add(r["method"])
                rank = TIER_RANK.get(m.get("tier"), -1)
                if rank < last:
                    raise SystemExit(f"REFUSED: {where} tier {m.get('tier')!r} follows a higher tier")
                last = max(last, rank)
                applies = set(m.get("applies_to") or [])
                if UNIVERSAL_TARGET not in applies:
                    t = p.get("type")
                    if t not in TYPE_TARGETS:
                        raise SystemExit(f"REFUSED: {where} type {t!r} unrecognized")
                    if not (applies & TYPE_TARGETS[t]):
                        raise SystemExit(f"REFUSED: {where} method {r['method']!r} applies_to "
                                         f"{sorted(applies)} does not reach type {t!r}")
                for k in ADVICE_FIELDS:
                    v = r.get(k)
                    if not isinstance(v, str) or not v.strip():
                        raise SystemExit(f"REFUSED: {where} {k} missing or empty")
                    if "—" in v or "–" in v:
                        raise SystemExit(f"REFUSED: {where} {k} contains an em/en dash")
                    if LADDER_VOCAB.search(v):
                        raise SystemExit(f"REFUSED: {where} {k} names the machinery: {v[:60]!r}")
                if r["note_beginner"].strip() == r["note_seasoned"].strip():
                    raise SystemExit(f"REFUSED: {where} the two registers are byte-identical")
                n += 1
    if n == 0:
        raise SystemExit("REFUSED: no rungs scanned; this guard would be vacuous")
    return n


def states_sulfur_oil_interval(text):
    """True when ONE sentence names sulfur, names oil, and gives a duration. 'Never mix oil with
    sulfur' carries no interval and passes; 'wait two weeks between sulfur and oil' does not."""
    for s in re.split(r"(?<=[.!?;])\s+", text or ""):
        if SULFUR.search(s) and OIL.search(s) and DURATION.search(s):
            return True
    return False


def check_no_sulfur_oil_interval(batch):
    """PLA-457 HOLD. Roster-wide, awaiting a ruling; this batch states no interval either way."""
    scanned = 0
    for crop in CROPS:
        for _f, p in problems(batch[crop]):
            texts = [(f"{p['id']}/{r['method']}/{k}", r.get(k) or "")
                     for r in p.get("control_ladder") or [] for k in ADVICE_FIELDS]
            texts += [(f"{p['id']}/correction/{f}", (c or {}).get("new") or "")
                      for f, c in (p.get("field_corrections") or {}).items()]
            for where, t in texts:
                scanned += 1
                if states_sulfur_oil_interval(t):
                    raise SystemExit(f"REFUSED: {crop}/{where} states a sulfur/oil interval; "
                                     f"PLA-457 holds that figure roster-wide: {t[:90]!r}")
    if scanned == 0:
        raise SystemExit("REFUSED: no strings scanned; this guard would be vacuous")
    return scanned


def check_split_rows_author_full_prose(pins, batch):
    """A SPLIT limb inherits a bundle's prose, which describes several organisms and is therefore
    wrong for any single limb. Every split row must declare a correction for EVERY prose field."""
    for crop, field, row in spec_rows(pins):
        if not row["from"].startswith("SPLIT"):
            continue
        got = next(e for e in batch[crop][field] if e["name"] == row["name"])
        declared = set((got.get("field_corrections") or {}))
        missing = [f for f in PROSE_FIELDS if f not in declared]
        if missing:
            raise SystemExit(f"REFUSED: {crop}/{row['name']!r} is a SPLIT limb but does not "
                             f"re-author {missing}; a split limb may not inherit bundle prose")


def check_corrections_anchored(batch, pins):
    """A correction with no reason and no anchor is a rewrite, not a correction. `name` may be
    declared as provenance for a RENAME/SPLIT row only when it agrees with the pin, which governs."""
    n = 0
    pinned_name = {(c, f, r["name"]) for c, f, r in spec_rows(pins)}
    for crop in CROPS:
        for field, p in problems(batch[crop]):
            for fname, corr in (p.get("field_corrections") or {}).items():
                if fname == "name":
                    if (crop, field, p["name"]) not in pinned_name:
                        raise SystemExit(f"REFUSED: {crop}/{p['id']} declares a name correction "
                                         f"but {p['name']!r} is not a pinned target name")
                    if (corr or {}).get("new") != p["name"]:
                        raise SystemExit(f"REFUSED: {crop}/{p['id']} name correction says "
                                         f"{(corr or {}).get('new')!r} but the pinned name is "
                                         f"{p['name']!r}; the pin governs the value")
                elif fname not in PROSE_FIELDS:
                    raise SystemExit(f"REFUSED: {crop}/{p['id']} declares a correction to "
                                     f"{fname!r}, which is not a prose field")
                for k in ("new", "why", "anchor"):
                    if not str(corr.get(k) or "").strip():
                        raise SystemExit(f"REFUSED: {crop}/{p['id']}/{fname} correction is missing "
                                         f"{k!r}")
                if "—" in corr["new"] or "–" in corr["new"]:
                    raise SystemExit(f"REFUSED: {crop}/{p['id']}/{fname} correction contains an "
                                     f"em/en dash")
                if LADDER_VOCAB.search(corr["new"]):
                    raise SystemExit(f"REFUSED: {crop}/{p['id']}/{fname} correction names the "
                                     f"machinery: {corr['new'][:60]!r}")
                n += 1
    if n == 0:
        raise SystemExit("REFUSED: no field corrections declared; the record pass found defects, "
                         "so zero corrections means the batch did not carry them")
    return n


def check_sources_admitted(batch, data):
    """Every source key must exist in source_catalog. The catalog is the admission authority."""
    cat = data["source_catalog"]
    n = 0
    for crop in CROPS:
        for field, p in problems(batch[crop]):
            srcs = p.get("sources") or []
            anch = p.get("anchoring_urls") or {}
            for s in srcs:
                if s not in cat:
                    raise SystemExit(f"REFUSED: {crop}/{p['id']} cites {s!r}, absent from "
                                     f"source_catalog")
                n += 1
            for k in anch:
                if k not in cat:
                    raise SystemExit(f"REFUSED: {crop}/{p['id']} anchors {k!r}, absent from "
                                     f"source_catalog")
                if k not in srcs:
                    raise SystemExit(f"REFUSED: {crop}/{p['id']} anchors {k!r} but does not list it "
                                     f"in sources")
            if srcs and not anch:
                raise SystemExit(f"REFUSED: {crop}/{p['id']} lists sources with no anchoring_urls")
    if n == 0:
        raise SystemExit("REFUSED: no sources scanned; this guard would be vacuous")
    return n


def _sym(a, b):
    """MAX of both orders (difflib is asymmetric by up to 0.271 on this corpus); autojunk off."""
    return max(difflib.SequenceMatcher(None, a, b, autojunk=False).ratio(),
               difflib.SequenceMatcher(None, b, a, autojunk=False).ratio())


def check_no_precedent_copy(batch, data):
    """Pass A keys on (problem id, method); pass B on METHOD ALONE across any problem."""
    by_idm, by_m = {}, {}
    for c in data["crops"]:
        if c["slug"] in CROPS:
            continue
        for _f, p in problems(c):
            for r in p.get("control_ladder") or []:
                rec = (c["slug"], p.get("id"), r.get("note_beginner") or "",
                       r.get("note_seasoned") or "")
                by_m.setdefault(r["method"], []).append(rec)
                if p.get("id"):
                    by_idm.setdefault((p["id"], r["method"]), []).append(rec)

    worst, worst_at, comparisons = 0.0, None, 0
    for crop in CROPS:
        for _f, p in problems(batch[crop]):
            for r in p.get("control_ladder") or []:
                nb, ns = r["note_beginner"], r["note_seasoned"]
                pool = list(by_idm.get((p["id"], r["method"]), [])) + list(by_m.get(r["method"], []))
                for slug, pid, onb, ons in pool:
                    comparisons += 1
                    s = max(_sym(nb, onb), _sym(ns, ons))
                    if s > worst:
                        worst, worst_at = s, f"{crop}/{p['id']}/{r['method']} vs {slug}/{pid}"
                    if s >= COPY_THRESHOLD:
                        raise SystemExit(f"REFUSED: {crop}/{p['id']}/{r['method']} scores {s:.3f} "
                                         f"against shipped {slug}/{pid} (threshold "
                                         f"{COPY_THRESHOLD})")
    if comparisons == 0:
        raise SystemExit("REFUSED: zero precedent comparisons; this guard would be vacuous")
    return worst, worst_at, comparisons


def _grams(text, n=6):
    w = (text or "").lower().split()
    return {" ".join(w[i:i + n]) for i in range(max(0, len(w) - n + 1))}


def check_no_multi_donor_recombination(batch, data):
    """A note assembled from runs lifted out of TWO DIFFERENT shipped notes, which the ratio
    cannot see. Flag when two distinct shipped notes each share >= MIN_RUN_GRAMS six-word runs AND
    the runs sit in NON-OVERLAPPING regions of the note (positional overlap, not set nesting)."""
    shipped = {}
    for c in data["crops"]:
        if c["slug"] in CROPS:
            continue
        for _f, p in problems(c):
            for r in p.get("control_ladder") or []:
                for k in ADVICE_FIELDS:
                    v = r.get(k)
                    if v:
                        shipped[f"{c['slug']}/{p.get('id')}/{r['method']}/{k}"] = _grams(v)
    if not shipped:
        raise SystemExit("REFUSED: no shipped notes to compare; this guard would be vacuous")

    checked = 0
    for crop in CROPS:
        for _f, p in problems(batch[crop]):
            for r in p.get("control_ladder") or []:
                for k in ADVICE_FIELDS:
                    text = r.get(k)
                    if not text:
                        continue
                    checked += 1
                    words = text.lower().split()
                    windows = {" ".join(words[i:i + 6]): i for i in range(max(0, len(words) - 5))}
                    mine = set(windows)
                    spans = {}
                    for name, sg in shipped.items():
                        shared = mine & sg
                        if len(shared) >= MIN_RUN_GRAMS:
                            pos = sorted(windows[g] for g in shared)
                            spans[name] = (pos[0], pos[-1] + 6)
                    names = list(spans)
                    for i in range(len(names)):
                        for j in range(i + 1, len(names)):
                            (a0, a1), (b0, b1) = spans[names[i]], spans[names[j]]
                            if a0 < b1 and b0 < a1:
                                continue      # the two runs OVERLAP in this note: one phrase
                            raise SystemExit(
                                f"REFUSED: {crop}/{p['id']}/{r['method']} {k} recombines runs from "
                                f"two shipped notes: words {a0}-{a1} from {names[i]} and "
                                f"words {b0}-{b1} from {names[j]}")
    if checked == 0:
        raise SystemExit("REFUSED: no batch notes scanned; this guard would be vacuous")
    return checked, len(shipped)


def check_no_shipped_prose_echo(batch, data):
    """Identical shape with independent prose is convergent authoring; identical prose is copying.
    House phrasing (a sentence with 2+ shipped donors) is exempt; whole-note echoes never are."""
    whole, sent, donors = {}, {}, {}
    for c in data["crops"]:
        if c["slug"] in CROPS:
            continue
        for _f, p in problems(c):
            for r in p.get("control_ladder") or []:
                for k in ADVICE_FIELDS:
                    v = r.get(k)
                    if not v:
                        continue
                    tag = f"{c['slug']}/{p.get('id')}/{r['method']}"
                    whole.setdefault(v.strip().lower(), tag)
                    for s in sentences(v):
                        sent.setdefault(s, tag)
                        donors[s] = donors.get(s, 0) + 1
    house = {s for s, n in donors.items() if n > 1}
    checked = 0
    for crop in CROPS:
        for _f, p in problems(batch[crop]):
            for r in p.get("control_ladder") or []:
                for k in ADVICE_FIELDS:
                    v = (r.get(k) or "").strip().lower()
                    checked += 1
                    if v in whole:
                        raise SystemExit(f"REFUSED: {crop}/{p['id']}/{r['method']} {k} is a verbatim "
                                         f"echo of {whole[v]}")
                    for s in sentences(r.get(k) or ""):
                        if s in sent and s not in house:
                            raise SystemExit(f"REFUSED: {crop}/{p['id']}/{r['method']} {k} echoes a "
                                             f"shipped sentence from {sent[s]}: {s[:70]!r}")
    if not whole:
        raise SystemExit("REFUSED: no shipped rung prose found; this guard would be vacuous")
    if checked == 0:
        raise SystemExit("REFUSED: no batch notes scanned; this guard would be vacuous")
    if not house:
        raise SystemExit("REFUSED: zero multi-donor sentences found; the house-phrasing exemption "
                         "would be doing nothing and its measurement has drifted")
    return checked, len(house)


def check_no_intra_batch_twins(batch):
    """Six independent agents author several shared problems (the pears share five, aphids and
    whiteflies and scale recur). A byte-identical note across two crops means one of them did not
    write from its own record."""
    seen = {}
    for crop in CROPS:
        for _f, p in problems(batch[crop]):
            for r in p.get("control_ladder") or []:
                for k in ADVICE_FIELDS:
                    v = (r.get(k) or "").strip().lower()
                    key = (r["method"], v)
                    if key in seen and seen[key] != crop:
                        raise SystemExit(f"REFUSED: {crop}/{p['id']}/{r['method']} {k} is "
                                         f"byte-identical to {seen[key]}'s; template twin")
                    seen[key] = crop
    return len(seen)


def check_pear_twin_divergence(pins, batch, data):
    """Same-named pear entries with byte-identical canonical prose must share an id, and must
    build the same ladder unless the divergence is pinned with its record evidence."""
    idx = by_slug(data)
    a, e = PEARS
    canon_a = {(f, p["name"]): p for f, p in problems(idx[a])}
    canon_e = {(f, p["name"]): p for f, p in problems(idx[e])}
    # KEYED BY (field, name), NOT NAME. The retired pests[] "Pear scab" copies are themselves a
    # byte-identical canonical pair; keyed by name alone they resolved onto the surviving
    # diseases[] entry and the scab divergence was counted twice (4 twins, 2 divergences against
    # the 3 and 1 measured on canonical). The suite's pinned twin count is what exposed it.
    out_a = {(f, p["name"]): p for f, p in problems(batch[a])}
    out_e = {(f, p["name"]): p for f, p in problems(batch[e])}
    twins = diverged = 0
    for key in sorted(set(canon_a) & set(canon_e)):
        field, name = key
        if prose_key(canon_a[key]) != prose_key(canon_e[key]):
            continue
        if key not in out_a or key not in out_e:
            continue      # a retired duplicate copy; reconcile owns that
        twins += 1
        if out_a[key]["id"] != out_e[key]["id"]:
            raise SystemExit(f"REFUSED: pear twin {name!r} carries id {out_a[key]['id']!r} on "
                             f"{a} and {out_e[key]['id']!r} on {e}; a shared disease shares its "
                             f"join key")
        la = tuple(r["method"] for r in out_a[key].get("control_ladder") or [])
        le = tuple(r["method"] for r in out_e[key].get("control_ladder") or [])
        if la == le:
            continue
        diverged += 1
        extra_a = tuple(m for m in la if m not in le)
        extra_e = tuple(m for m in le if m not in la)
        pin = TWIN_DIVERGENCE_PINS.get(name)
        if pin is None:
            raise SystemExit(f"REFUSED: pear twin {name!r} has byte-identical source prose but "
                             f"different ladders ({list(la)} vs {list(le)}); identical prose "
                             f"cannot support two ladders unless the divergence is pinned with "
                             f"its record evidence")
        if (extra_a, extra_e) != (tuple(pin[0]), tuple(pin[1])):
            raise SystemExit(f"REFUSED: pear twin {name!r} diverges by +{list(extra_a)} on {a} and "
                             f"+{list(extra_e)} on {e}, pinned +{list(pin[0])} / +{list(pin[1])}")
    if twins == 0:
        raise SystemExit("REFUSED: no pear template twins found; three were measured on canonical, "
                         "so this guard has stopped reaching them")
    return twins, diverged


def check_temperature_figures_warranted(batch, pins, data):
    """Every °F figure must appear in the entry's own authored prose, its corrections, or the
    method's catalog text."""
    cm = data["control_methods"]
    idx = by_slug(data)
    found = 0
    for crop, field, row in spec_rows(pins):
        p = next(e for e in batch[crop][field] if e["name"] == row["name"])
        src = next((e for e in idx[crop].get(field) or [] if e["name"] == source_name(row)), {})
        blob = " ".join([src.get(f) or "" for f in PROSE_FIELDS] +
                        [(c or {}).get("new") or "" for c in (p.get("field_corrections") or {}).values()] +
                        [(c or {}).get("anchor") or "" for c in (p.get("field_corrections") or {}).values()])
        for r in p.get("control_ladder") or []:
            meth = json.dumps(cm.get(r["method"]) or {}, ensure_ascii=False)
            for k in ADVICE_FIELDS:
                for hit in TEMP_FIGURE.findall(r.get(k) or ""):
                    found += 1
                    num = re.sub(r"\D", "", hit)
                    if num not in re.sub(r"\s+", "", blob) and num not in re.sub(r"\s+", "", meth):
                        raise SystemExit(f"REFUSED: {crop}/{p['id']}/{r['method']} {k} gives {hit} "
                                         f"with no warrant in the record or the method")
    return found


# ---------------------------------------------------------------- apply / verify

def apply_to(data, pins, batch):
    out = copy.deepcopy(data)
    idx = by_slug(out)
    for crop in CROPS:
        for field in ("pests", "diseases"):
            src_by_name = {e["name"]: e for e in idx[crop].get(field) or []}
            authored = {e["name"]: e for e in batch[crop].get(field) or []}
            new = []
            for row in pins[crop].get(field, []):
                entry = copy.deepcopy(src_by_name[source_name(row)])
                a = authored[row["name"]]
                entry["name"] = row["name"]
                entry["id"] = row["id"]
                entry["type"] = row["type"]
                entry["severity"] = row["severity"]
                entry["control_ladder"] = copy.deepcopy(a["control_ladder"])
                if a.get("sources"):
                    entry["sources"] = list(a["sources"])
                if a.get("anchoring_urls"):
                    entry["anchoring_urls"] = copy.deepcopy(a["anchoring_urls"])
                for fname, corr in (a.get("field_corrections") or {}).items():
                    entry[fname] = corr["new"]
                new.append(entry)
            idx[crop][field] = new
    return out


def verify_post(pre, post, pins, batch):
    """Every changed leaf must match a pin or a DECLARED correction. Compare the SET of entries
    first, then values -- iterating one side makes the other side's additions invisible."""
    pre_i, post_i = by_slug(pre), by_slug(post)

    if {c["slug"] for c in pre["crops"]} != {c["slug"] for c in post["crops"]}:
        raise SystemExit("REFUSED: crop roster changed")
    if len(pre["crops"]) != len(post["crops"]):
        raise SystemExit("REFUSED: crop count changed")

    for slug in pre_i:
        if slug in CROPS:
            continue
        if json.dumps(pre_i[slug], sort_keys=True) != json.dumps(post_i[slug], sort_keys=True):
            raise SystemExit(f"REFUSED: untouched crop {slug} changed")

    for k in pre:
        if k == "crops":
            continue
        if json.dumps(pre[k], sort_keys=True) != json.dumps(post[k], sort_keys=True):
            raise SystemExit(f"REFUSED: top-level key {k!r} changed")

    changed = 0
    for crop in CROPS:
        for field in ("pests", "diseases"):
            rows = pins[crop].get(field, [])
            got = post_i[crop].get(field) or []
            if len(got) != len(rows):
                raise SystemExit(f"REFUSED: {crop}/{field} post has {len(got)}, spec has {len(rows)}")
            src_by_name = {e["name"]: e for e in pre_i[crop].get(field) or []}
            authored = {e["name"]: e for e in batch[crop].get(field) or []}
            for row, g in zip(rows, got):
                if g["name"] != row["name"]:
                    raise SystemExit(f"REFUSED: {crop}/{field} order/name mismatch "
                                     f"{g['name']!r} != {row['name']!r}")
                src = src_by_name[source_name(row)]
                corr = authored[row["name"]].get("field_corrections") or {}
                # SET COMPARISON BEFORE VALUE COMPARISON.
                added = set(g) - set(src)
                removed = set(src) - set(g)
                if removed:
                    raise SystemExit(f"REFUSED: {crop}/{g['name']!r} lost keys {sorted(removed)}")
                for k in sorted(added):
                    if k not in PINNED_FIELDS:
                        raise SystemExit(f"REFUSED: {crop}/{g['name']!r} gained unpinned key {k!r}")
                for k in sorted(set(g) & set(src)):
                    if g[k] == src[k]:
                        continue
                    changed += 1
                    if k == "name":
                        if not row["from"].startswith(("RENAME", "SPLIT")):
                            raise SystemExit(f"REFUSED: {crop}/{g['name']!r} name changed without a "
                                             f"RENAME/SPLIT provenance")
                    elif k in PINNED_FIELDS:
                        pass
                    elif k in PROSE_FIELDS:
                        if k not in corr:
                            raise SystemExit(f"REFUSED: {crop}/{g['name']!r} prose field {k!r} "
                                             f"changed but no correction was declared")
                        if g[k] != corr[k]["new"]:
                            raise SystemExit(f"REFUSED: {crop}/{g['name']!r} {k!r} does not match "
                                             f"its declared correction")
                    else:
                        raise SystemExit(f"REFUSED: {crop}/{g['name']!r} unpinned field {k!r} "
                                         f"changed unseen")
    if changed == 0:
        raise SystemExit("REFUSED: nothing changed; the promote would be a no-op")
    return changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="run checks, write nothing")
    args = ap.parse_args()

    data = load_canonical()
    pins, batch = staged()
    cm = data["control_methods"]

    n_canon, n_target = check_reconcile(pins, data)
    print(f"  reconcile            {n_canon} canonical -> {n_target} target "
          f"({len(pins.get('_retired', []))} retired)")
    nret = check_retirements_are_array_duplicates(pins, data)
    print(f"  retirements          {nret}, each a pests[] duplicate of a carried diseases[] entry")
    up, carried = check_type_upgrade(pins, data)
    print(f"  types                {up} upgraded off coarse/other, {carried} fine types carried")
    check_batch_matches_spec(pins, batch)
    print("  spec match           OK (names, ids, types, severities)")
    rungs = check_ladders(batch, cm)
    print(f"  ladders              {rungs} rungs, tiers ordered, applies_to reachable")
    nhold = check_no_sulfur_oil_interval(batch)
    print(f"  PLA-457 hold         {nhold} strings scanned, no sulfur/oil interval stated")
    check_split_rows_author_full_prose(pins, batch)
    print("  split limbs          full prose re-authored")
    ncorr = check_corrections_anchored(batch, pins)
    print(f"  corrections          {ncorr} declared, each with reason and anchor")
    nsrc = check_sources_admitted(batch, data)
    print(f"  sources              {nsrc} keys, all admitted by source_catalog")
    worst, at, comps = check_no_precedent_copy(batch, data)
    print(f"  precedent copy       worst {worst:.3f} at {at} over {comps} comparisons "
          f"(threshold {COPY_THRESHOLD})")
    nechk, nhouse = check_no_shipped_prose_echo(batch, data)
    print(f"  shipped echo         {nechk} notes scanned, zero echoes "
          f"({nhouse} house-phrase sentences exempt)")
    nrec, nship = check_no_multi_donor_recombination(batch, data)
    print(f"  recombination        {nrec} notes vs {nship} shipped, zero two-donor assemblies")
    ntw = check_no_intra_batch_twins(batch)
    print(f"  intra-batch twins    {ntw} note keys, zero cross-crop duplicates")
    twins, div = check_pear_twin_divergence(pins, batch, data)
    print(f"  pear twins           {twins} byte-identical pairs, {div} pinned divergences")
    ntemp = check_temperature_figures_warranted(batch, pins, data)
    print(f"  temperature figures  {ntemp} warranted")

    post = apply_to(data, pins, batch)
    changed = verify_post(data, post, pins, batch)
    print(f"  verify_post          {changed} leaves changed, every one pinned or declared")

    blob = serialize(post)
    new_sha = sha256_bytes(blob)
    print(f"\n  base {BASE_SHA}\n  post {new_sha}")
    if args.check:
        print("\n--check: nothing written.")
        return 0
    with open(CANON, "wb") as f:
        f.write(blob)
    print(f"\nWROTE {CANON}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
