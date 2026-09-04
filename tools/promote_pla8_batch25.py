#!/usr/bin/env python3
"""promote_pla8_batch25 -- PLA-8 batch 25, the herbs.

lavender, lemongrass, mint, oregano, rosemary, sage, thyme.

WHAT MAKES THIS BATCH STRUCTURALLY DIFFERENT FROM 21-24. Every previous PLA-8 batch only ADDED
(`id`, `type`, `control_ladder`) to problem entries that already existed and kept their names. This
one RESHAPES the arrays: it renames three entries, splits four bundles into nine, deletes one bundle
half and retires two entries outright, on Trevor's rulings of 2026-09-04. 36 canonical problems
become 38.

That changes what "verify the post-state" means. An owner-and-count check over matching indices does
not survive a split, and a guard that walks canonical looking for its entries in the output cannot
see a retirement at all. So the post-verification here is driven by an explicit TARGET SPEC
(`pinned_ids.json`), and every canonical problem must be accounted for exactly once -- carried,
renamed, consumed by a split, or named in `_retired`. Retirement is DECLARED, never inferred from
absence: absence is precisely what a one-directional walk cannot see, which is the PLA-162 shape.

WHY THE RECORD CORRECTIONS RIDE ALONG. The record/source pass found 16 wrong-or-unanchored claims
and 22 entries carrying no anchor at all. Batch 24 corrected records in separate commits first, then
authored. That was right for batch 24, where the corrections were narrow. Here the corrections and
the authoring are largely THE SAME WORK -- splitting mint's powdery-mildew/anthracnose bundle
requires writing new prose for both limbs whatever else happens -- so separating them would mean
authoring the same sentences twice. They land together, and the price of that is
`check_field_corrections_declared`: every changed prose leaf must match a DECLARED correction
carrying its own reason and anchor, or the promote refuses. Batch 24's lesson 4 is the reason -- an
owner check passes while a target's UNPINNED field changes unseen.

Usage:
    promote_pla8_batch25.py            # check, apply, verify, write
    promote_pla8_batch25.py --check    # checks only, write nothing
"""
import argparse, copy, difflib, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CANON = os.path.join(REPO, "crops_data_final.json")
STAGE = os.path.join(HERE, "staging", "pla8_batch25_herbs")
PINS = os.path.join(STAGE, "pinned_ids.json")

sys.path.insert(0, HERE)
from control_ladder_gate import TYPE_TARGETS, UNIVERSAL_TARGET, TIER_RANK  # noqa: E402

BASE_SHA = "500a61262d5870636d8b33845cb81072940e677d3674938c0375319eab6d6fc9"  # a9c84847 + the uc_ipm_pn7493 catalog admission
CROPS = ("lavender", "lemongrass", "mint", "oregano", "rosemary", "sage", "thyme")

ADVICE_FIELDS = ("note_beginner", "note_seasoned")
PROSE_FIELDS = ("symptoms_beginner", "symptoms_seasoned", "cause_beginner", "cause_seasoned",
                "organic_treatment_beginner", "organic_treatment_seasoned",
                "prevention_beginner", "prevention_seasoned")
PINNED_FIELDS = ("id", "type", "severity", "control_ladder", "sources", "anchoring_urls")

COPY_THRESHOLD = 0.70
MIN_RUN_GRAMS = 3        # six-word runs shared with one donor before it counts as a lift
TEMP_FIGURE = re.compile(r"\b\d{2,3}\s*°\s*F\b")
FROM_RE = re.compile(r"^(?:RENAME|SPLIT \d+/\d+) from '([^']+)'")
# Prose must not name the machinery. A reader sees advice, not a data model.
# NARROWED 2026-09-04. The first version matched `applies[_ ]to` and `control[_ ]method` with an
# optional SPACE, so it refused the correct English sentence "The same care applies to a division
# handed over the fence" on oregano. A guard that refuses good input is its own defect class and no
# mutation finds it, because the branch fires exactly as written. The field names are the underscore
# forms; natural prose uses the spaced forms, so only the underscore forms are machinery.
LADDER_VOCAB = re.compile(r"\b(rungs?|ladders?|tiers?)\b|applies_to|control_method", re.I)


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
    """A correction with no reason and no anchor is a rewrite, not a correction.

    `name` is ALLOWED here, uniquely among non-prose fields, and constrained. The three renames in
    this batch are governed by the pin table, not by a correction, so a declared `name` correction
    could become a second source of truth for the same value. But the justification for a rename --
    which document calls the disease what, and why the old name was wrong -- is exactly the kind of
    provenance that is worth keeping next to the change rather than only in a handoff doc. So it may
    be declared, and its `new` MUST equal the pinned name. The pin still governs the value; the
    correction carries the reason."""
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
                # WIDENED 2026-09-04 (sage authoring agent). Corrected prose lands in the record as
                # consumer copy exactly as rung notes do, so the machinery-vocabulary ban has to
                # reach it too. The guard was notes-only, which left half the authored strings in
                # this batch unscanned: 240 corrections against 131 rung notes.
                if LADDER_VOCAB.search(corr["new"]):
                    raise SystemExit(f"REFUSED: {crop}/{p['id']}/{fname} correction names the "
                                     f"machinery: {corr['new'][:60]!r}")
                n += 1
    if n == 0:
        raise SystemExit("REFUSED: no field corrections declared; the record pass found 16 defects, "
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
    """MAX of both orders. difflib's matcher is greedy, so ratio(a,b) != ratio(b,a) -- measured up
    to 0.271 apart on this corpus against a 0.70 threshold. Argument order is not a property of the
    prose. autojunk=False because it engages at 200 characters and junks anything in over 1% of the
    sequence, which describes every seasoned register."""
    return max(difflib.SequenceMatcher(None, a, b, autojunk=False).ratio(),
               difflib.SequenceMatcher(None, b, a, autojunk=False).ratio())


def check_no_precedent_copy(batch, data):
    """Two passes. Pass A keys on (problem id, method); pass B on METHOD ALONE across any problem,
    which is the one that catches phrasing lifted from a sibling's DIFFERENT problem -- that scores
    0.000 under pass A, and for a newly minted id pass A has nothing to compare against at all."""
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
    """A note assembled from runs lifted out of TWO DIFFERENT shipped notes.

    THE RATIO CANNOT SEE THIS, and that is the whole reason this guard exists. A note that takes
    half its phrasing from one donor and half from another resembles NEITHER closely enough to cross
    a similarity threshold: this batch's real instance scored under 0.70 against both of its donors
    and would have shipped. The repo has hit the same shape before, where a 72-character verbatim
    lift scored 0.59 and 0.62.

    THE RULE, MEASURED rather than guessed. Flag a note when two or more DISTINCT shipped notes each
    share at least MIN_RUN_GRAMS six-word runs with it, AND the two runs sit in NON-OVERLAPPING
    REGIONS OF THE NOTE. Position is what separates recombination from house phrasing: several
    shipped notes carrying the same stock sentence all match the SAME span of the batch note, while
    a real assembly takes its opening from one donor and its closing from another.

    POSITION, NOT SET NESTING. The first version compared the donors' shared-gram SETS and exempted
    a pair when one nested inside the other. That was wrong and an authoring agent caught it by
    READING the runs instead of counting them: three shipped notes wrote "the other choice at this
    step" and a fourth wrote "at this POINT", and the one-word variant shifts the window set by one
    element so neither set nests. One stock sentence with a single word changed between copies
    therefore read as two independent donors and refused correct prose. Overlapping spans do not
    care about the variant.

    Measured on this batch at MIN_RUN_GRAMS=3: 9 notes draw a run from two or more donors, and
    exactly ONE survives the nesting test. A bare "shares a rare 6-gram" rule flagged 108 and was
    almost all ordinary English collocation; narrowing the CHECK rather than its scope is what made
    it usable."""
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
    """Identical shape with independent prose is convergent authoring; identical prose is copying."""
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

    # HOUSE PHRASING IS NOT AN ECHO. MEASURED 2026-09-04, and this guard was refusing correct input
    # before the measurement was taken. A sentence with MANY shipped donors is the dataset's own
    # standard wording, not a lift from any one note: "go easy on the fertilizer." appears on 13
    # shipped rungs and "go easy on nitrogen fertilizer." on 19, and 75 short strings are already
    # duplicated inside shipped canonical. Refusing the 14th crop for writing what 13 already say is
    # manufacturing difference to satisfy a metric.
    #
    # The exemption is narrow and keeps the guard's real surface: 760 of 10491 distinct shipped
    # sentences (7.2%) have two or more donors; the other 9731 stay caught, and a single-donor
    # sentence is exactly the shape of a real lift. This batch demonstrates both sides -- oregano's
    # "go easy on the fertilizer." has 13 donors and is exempt, while mint's "water at the soil, not
    # over the leaves." has ONE and is refused.
    #
    # WHOLE-NOTE echoes are never exempt, whatever the sentence counts: an entire note reproduced
    # verbatim is copying regardless of how common its parts are.
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
    """This batch authors the SAME problem on several crops (spittlebugs x3, spider-mites x5,
    powdery-mildew x4, aphids x4) from seven independent agents. A byte-identical note across two
    crops means one of them did not write from its own record."""
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


def check_temperature_figures_warranted(batch, pins, data):
    """Every °F figure must appear in the entry's own authored prose, its corrections, or the
    method's catalog text. The count is PINNED so a figure that vanishes is as visible as one that
    appears."""
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

    # Nothing outside the seven crops may move.
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
    check_batch_matches_spec(pins, batch)
    print("  spec match           OK (names, ids, types, severities)")
    rungs = check_ladders(batch, cm)
    print(f"  ladders              {rungs} rungs, tiers ordered, applies_to reachable")
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
