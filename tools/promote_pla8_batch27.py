#!/usr/bin/env python3
"""promote_pla8_batch27 -- PLA-8 batch 27, the microgreens. THE LAST BATCH OF THE ARC.

arugula-microgreens, broccoli-microgreens, cilantro-microgreens, pea-shoots, radish-microgreens,
sunflower-sprouts, wheatgrass.

WHAT IS DIFFERENT HERE, and why each difference is a guard rather than a note.

1. A DIFFERENT SCHEMA. These seven carry `name_seasoned` / `name_beginner` and **no `name` key** on
   their problem entries. Every previous batch in this arc joined its pin table on `name`, so every
   one of those promotes would KeyError here. The join key is `name_seasoned`, and
   `check_pre_state_schema` PINS the schema fact rather than assuming it: a target entry must carry
   no `name`, no `id`, no `type` and no `control_ladder` before the promote runs. If a future pass
   normalizes the schema (PLA-452), this promote refuses instead of silently mis-joining.

2. THIS BATCH MINTS NO IDS AT ALL, and that is the batch's central claim, so it is guarded, not
   asserted. `fungus-gnats` and `damping-off` both already exist on `microgreens-mix`, which is
   laddered on this same schema and is the working precedent. `check_ids_are_reused` proves every
   pinned id already lives on a crop OUTSIDE this batch. The PLA-449 collision guard was run at
   id-pinning time against POST-APPLY data: 42 pairs before, 42 after, zero introduced.

3. THE BUNDLING QUESTION WAS ASKED AND ANSWERED AGAINST DOCUMENTS. Four of the seven disease names
   bundle "mold" with damping-off, and the batch rule (one organism or disease complex per id) would
   split a real bundle rather than mint a new one. It does not split here, because no readable
   .edu/.gov document supports a separate organism set: Penn State's microgreens page states
   "Damping-off is the only disease or pest issue we have encountered" and attributes tray fuzz to
   Rhizoctonia or Botrytis; Virginia Tech SPES-756 names damping-off plus mildews and never uses the
   word "mold". The saprophyte story (Rhizopus, Mucor, Aspergillus, Penicillium) appears in none of
   them. So this is ONE complex under one id. The bundled NAMES are a separate, out-of-scope naming
   question (PLA-453) and are carried byte-for-byte.

4. NO MATERIAL RUNGS ARE PERMITTED, and this is a SAFETY guard, not a stylistic one. These crops are
   cut at cotyledon stage inside 7 to 28 days and eaten whole and raw (wheatgrass is juiced raw). A
   pre-harvest interval on a 10-day crop is a different safety problem from a PHI on a tomato and is
   not one to solve inside a ladder batch. `check_no_material_rungs` refuses any rung whose method
   sits above `physical`. It is a REFUSAL SPEC: it is expected to stay green, and its green is a
   pass only because the mutation suite proves it reddens on an injected soft_chemical rung.

5. THE ROOT-HAIR CLAIM IS REFUSED INTO RUNGS. radish-microgreens, sunflower-sprouts and wheatgrass
   each carry prose telling the reader that fine white fuzz is normal root hairs rather than mold.
   Their ONLY cited source is `psu_microgreens`, and that page is silent on root hairs (checked:
   the string does not occur). The claim may be true and is sourceable elsewhere (Purdue Extension,
   Missouri State), but it is not sourced HERE, so it does not get carried into a new field by this
   batch. `check_no_root_hair_claim` refuses it. The existing prose is left byte-for-byte and the
   gap is filed as a finding.

6. PLA-457 IS HELD, NOT RESOLVED, exactly as in batch 26.

Usage:
    promote_pla8_batch27.py            # check, apply, verify, write
    promote_pla8_batch27.py --check    # checks only, write nothing
"""
import argparse, copy, difflib, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CANON = os.path.join(REPO, "crops_data_final.json")
STAGE = os.path.join(HERE, "staging", "pla8_batch27_microgreens")
PINS = os.path.join(STAGE, "pinned_ids.json")

sys.path.insert(0, HERE)
from control_ladder_gate import TYPE_TARGETS, UNIVERSAL_TARGET, TIER_RANK  # noqa: E402

BASE_SHA = "ba61762a21e52bad85ec1ddca98a92b34e6216d8258497325ec8b0630787beb3"  # batch 26, the trees
CROPS = ("arugula-microgreens", "broccoli-microgreens", "cilantro-microgreens", "pea-shoots",
         "radish-microgreens", "sunflower-sprouts", "wheatgrass")
PRECEDENT = "microgreens-mix"          # laddered, same schema, the shape exemplar and a copy donor

# The keys this promote is allowed to ADD to a problem entry. Nothing else may appear.
PINNED_FIELDS = ("id", "type", "control_ladder")
ADVICE_FIELDS = ("note_beginner", "note_seasoned")
# The prose the rungs are restated FROM. Must survive byte-for-byte.
CARRIED_PROSE = ("name_seasoned", "name_beginner", "description_seasoned", "description_beginner",
                 "management_seasoned", "management_beginner", "sources", "anchoring_urls")

MAX_TIER_RANK = TIER_RANK["physical"]  # rule 4: nothing above physical may ship on a raw-cut crop

COPY_THRESHOLD = 0.70
MIN_RUN_GRAMS = 6          # a shared six-word run counts as a verbatim lift
TWIN_THRESHOLD = 0.85      # two crops' notes this close are a propagated template, not authoring

# Prose must not name the machinery. Underscore forms only: natural English "applies to" is fine.
LADDER_VOCAB = re.compile(r"\b(rungs?|ladders?|tiers?)\b|applies_to|control_method", re.I)
# PLA-457: a sentence naming BOTH sulfur and oil AND a duration states the held interval.
SULFUR = re.compile(r"\bsul(?:f|ph)ur\b", re.I)
OIL = re.compile(r"\boils?\b", re.I)
DURATION = re.compile(r"\b(\d+|one|two|three|four|several)\s*(days?|weeks?|months?)\b|\bmonth\b", re.I)
# Rule 5: the unsourced root-hair diagnostic.
ROOT_HAIR = re.compile(r"root\s*hairs?", re.I)
ABSOLUTES = re.compile(r"\b(always|never|completely|totally|harmless|guaranteed|guarantees|"
                       r"100%|entirely safe|perfectly safe)\b", re.I)
DASHES = re.compile(r"[–—]")
SPACED_F = re.compile(r"\d\s+°F|\d°\s+F")
CAP_PLANT = re.compile(r"(?<![.!?]\s)(?<!^)(?<!\bPlant\sPro)\bPlant\b(?! Pro)")


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def serialize(data):
    """CANONICAL IS COMPACT. separators, ensure_ascii=False, no trailing newline, never indent.
    ONE serializer, shared by this promote and its suite: a suite that does its own json.dumps
    grades itself and an indent mutation survives."""
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def by_slug(data):
    return {c["slug"]: c for c in data["crops"]}


def entry_name(e):
    """The join key on THIS schema. These entries carry no `name`; `name_seasoned` is the
    most-specific string they do carry. Never fall back silently: a missing key is a schema
    change and must surface as a KeyError inside a guard that says so."""
    return e["name_seasoned"]


def spec_rows(pins):
    for crop, fields in pins.items():
        if crop.startswith("_"):
            continue
        for field in ("pests", "diseases"):
            for row in fields.get(field, []):
                yield crop, field, row


def notes(batch):
    """(crop, field, name, which, text) for every authored register string in the batch."""
    for crop, fields in batch.items():
        for field in ("pests", "diseases"):
            for e in fields.get(field) or []:
                for rung in e.get("control_ladder") or []:
                    for which in ADVICE_FIELDS:
                        if rung.get(which):
                            yield crop, field, e["id"], which, rung[which]


# ---------------------------------------------------------------- load

def load_canonical(path=None):
    raw = open(path or CANON, "rb").read()
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

def check_pre_state_schema(pins, data):
    """Rule 1. PIN the schema this promote joins on, rather than assuming it.

    Every target entry must carry `name_seasoned` and `name_beginner`, must NOT carry `name`, and
    must NOT already carry `id`, `type` or `control_ladder`. Joining on `name_seasoned` is only
    sound while that holds; if PLA-452 normalizes the schema this refuses instead of mis-joining
    or overwriting an authored id."""
    idx = by_slug(data)
    n = 0
    for crop, field, row in spec_rows(pins):
        entries = idx[crop].get(field) or []
        if len(entries) != 1:
            raise SystemExit(f"REFUSED: {crop}/{field} has {len(entries)} entries, spec expects 1")
        e = entries[0]
        if "name" in e:
            raise SystemExit(f"REFUSED: {crop}/{field} entry carries a 'name' key; this promote "
                             f"joins on 'name_seasoned' and the schema has changed (PLA-452)")
        for k in ("name_seasoned", "name_beginner"):
            if not e.get(k):
                raise SystemExit(f"REFUSED: {crop}/{field} entry is missing {k!r}")
        for k in PINNED_FIELDS:
            if k in e:
                raise SystemExit(f"REFUSED: {crop}/{field} entry already carries {k!r}; this batch "
                                 f"would overwrite it")
        if entry_name(e) != row["name_seasoned"]:
            raise SystemExit(f"REFUSED: {crop}/{field} name_seasoned {entry_name(e)!r} != pinned "
                             f"{row['name_seasoned']!r}")
        n += 1
    return n


def check_ids_are_reused(pins, data):
    """Rule 2. This batch mints NOTHING. Every pinned id must already live on a crop outside the
    batch. A guard, because 'we reused the ids' is the batch's central claim and an unguarded
    claim is the thing this arc keeps being burned by."""
    outside = {}
    for c in data["crops"]:
        if c["slug"] in CROPS:
            continue
        for f in ("pests", "diseases"):
            for e in c.get(f) or []:
                if e.get("id"):
                    outside.setdefault(e["id"], set()).add(c["slug"])
    for crop, field, row in spec_rows(pins):
        pid = row["id"]
        if pid not in outside:
            raise SystemExit(f"REFUSED: {crop}/{field} id {pid!r} does not exist outside this "
                             f"batch; this promote mints no ids (PLA-449 was run at pinning time)")
        if PRECEDENT not in outside[pid]:
            raise SystemExit(f"REFUSED: id {pid!r} is not carried by the precedent crop "
                             f"{PRECEDENT!r}; the reuse claim rests on that precedent")
    return {row["id"] for _, _, row in spec_rows(pins)}, outside


def check_batch_matches_spec(pins, batch):
    """The authored output must carry exactly the pinned ids and types, in the pinned order."""
    for crop in CROPS:
        for field in ("pests", "diseases"):
            rows = pins[crop].get(field, [])
            got = batch[crop].get(field) or []
            if len(got) != len(rows):
                raise SystemExit(f"REFUSED: {crop}/{field} authored {len(got)}, spec has {len(rows)}")
            for row, g in zip(rows, got):
                if g.get("id") != row["id"]:
                    raise SystemExit(f"REFUSED: {crop}/{field} authored id {g.get('id')!r} != "
                                     f"pinned {row['id']!r}")
                if g.get("type") != row["type"]:
                    raise SystemExit(f"REFUSED: {crop}/{field} authored type {g.get('type')!r} != "
                                     f"pinned {row['type']!r}")
                for k in g:
                    if k not in ("id", "type", "control_ladder"):
                        raise SystemExit(f"REFUSED: {crop}/{field} authored unexpected key {k!r}")


def check_ladders(batch, cm):
    """Catalog keys real, tiers non-decreasing, applies_to reachable for the type.
    The tables are IMPORTED from control_ladder_gate, never retyped."""
    total = 0
    for crop in CROPS:
        for field in ("pests", "diseases"):
            for e in batch[crop].get(field) or []:
                ladder = e.get("control_ladder")
                if not isinstance(ladder, list) or not ladder:
                    raise SystemExit(f"REFUSED: {crop}/{e.get('id')} has an empty or missing ladder; "
                                     f"[] is a defect and null is not a promote output")
                ptype = e["type"]
                if ptype not in TYPE_TARGETS:
                    raise SystemExit(f"REFUSED: {crop}/{e['id']} type {ptype!r} unrecognized")
                ranks = []
                seen = set()
                for rung in ladder:
                    mid = rung.get("method")
                    m = cm.get(mid)
                    if m is None:
                        raise SystemExit(f"REFUSED: {crop}/{e['id']} names unknown method {mid!r}")
                    if mid in seen:
                        raise SystemExit(f"REFUSED: {crop}/{e['id']} repeats method {mid!r}")
                    seen.add(mid)
                    if not rung.get("note_beginner"):
                        raise SystemExit(f"REFUSED: {crop}/{e['id']}/{mid} has no note_beginner")
                    for k in rung:
                        if k not in ("method",) + ADVICE_FIELDS:
                            raise SystemExit(f"REFUSED: {crop}/{e['id']}/{mid} unexpected rung key {k!r}")
                    ranks.append(TIER_RANK[m["tier"]])
                    targets = set(m.get("applies_to") or [])
                    if UNIVERSAL_TARGET not in targets and not (targets & TYPE_TARGETS[ptype]):
                        raise SystemExit(f"REFUSED: {crop}/{e['id']} method {mid!r} "
                                         f"(applies_to {sorted(targets)}) does not fit {ptype!r}")
                    total += 1
                if any(ranks[i] > ranks[i + 1] for i in range(len(ranks) - 1)):
                    raise SystemExit(f"REFUSED: {crop}/{e['id']} ladder is not softest-first {ranks}")
    return total


def check_no_material_rungs(batch, cm):
    """Rule 4, a SAFETY refusal spec. Nothing above `physical` may ship on a crop cut at cotyledon
    stage and eaten raw, because no pre-harvest interval has been ruled for a 7 to 28 day crop.
    Expected to stay green; its green is only a pass because the mutation suite reddens it."""
    n = 0
    for crop in CROPS:
        for field in ("pests", "diseases"):
            for e in batch[crop].get(field) or []:
                for rung in e.get("control_ladder") or []:
                    tier = cm[rung["method"]]["tier"]
                    if TIER_RANK[tier] > MAX_TIER_RANK:
                        raise SystemExit(
                            f"REFUSED: {crop}/{e['id']} rung {rung['method']!r} is tier {tier!r}. "
                            f"These crops are eaten whole and raw within days; a material rung "
                            f"needs a pre-harvest-interval ruling this batch does not have.")
                    n += 1
    return n


def check_no_root_hair_claim(batch):
    """Rule 5. The root-hair diagnostic is unsourced against these crops' only cited source
    (psu_microgreens is silent on it), so it may not be carried into a new field."""
    for crop, field, pid, which, text in notes(batch):
        if ROOT_HAIR.search(text):
            raise SystemExit(f"REFUSED: {crop}/{pid}/{which} states the root-hair claim, which "
                             f"psu_microgreens does not support. Left in prose, filed as a finding.")
    return True


def check_no_sulfur_oil_interval(batch):
    """PLA-457 is held roster-wide. No rung may state a sulfur/oil spacing interval."""
    n = 0
    for crop, field, pid, which, text in notes(batch):
        for s in re.split(r"(?<=[.!?])\s+", text):
            if SULFUR.search(s) and OIL.search(s) and DURATION.search(s):
                raise SystemExit(f"REFUSED: {crop}/{pid}/{which} states a sulfur/oil interval "
                                 f"while PLA-457 is held: {s!r}")
            n += 1
    return n


def _sym(a, b):
    """difflib's ratio is ASYMMETRIC by up to 0.271. Take the max of both orders."""
    return max(difflib.SequenceMatcher(None, a, b).ratio(),
               difflib.SequenceMatcher(None, b, a).ratio())


def _grams(text, n=MIN_RUN_GRAMS):
    w = re.findall(r"[a-z0-9°]+", (text or "").lower())
    return {" ".join(w[i:i + n]) for i in range(max(0, len(w) - n + 1))}


def _is_figure_run(gram):
    """A run carrying a NUMBER is exempt from the verbatim-lift check.

    A guard can refuse correct input, and this is the case where it would: wheatgrass's rung has
    to say "7 to 10 day grow-out" because that is the crop's own figure, and there is no honest
    paraphrase of a number. Demanding one buys nothing and costs accuracy. The exemption is narrow
    on purpose -- it frees ONLY runs containing a digit, so prose runs like "let the surface dry
    between waterings" are still refused."""
    return any(ch.isdigit() for ch in gram)


def _donor_prose(data):
    """Every string this batch could plagiarise: the seven crops' own prose, and the precedent
    crop's ladder notes. A ratio check alone missed a 72-char lift once (it scored 0.59), so the
    rare-n-gram run check rides alongside it."""
    out = []
    idx = by_slug(data)
    for slug in CROPS + (PRECEDENT,):
        for f in ("pests", "diseases"):
            for e in idx[slug].get(f) or []:
                for k in ("description_seasoned", "description_beginner",
                          "management_seasoned", "management_beginner"):
                    if e.get(k):
                        out.append((f"{slug}/{k}", e[k]))
                for rung in e.get("control_ladder") or []:
                    for which in ADVICE_FIELDS:
                        if rung.get(which):
                            out.append((f"{slug}/{rung['method']}/{which}", rung[which]))
    return out


def check_no_precedent_copy(batch, data):
    """No authored note may be a verbatim lift from the crop's own prose or from the precedent
    ladder. Two independent signals, because either alone has been beaten in this repo."""
    donors = _donor_prose(data)
    dgrams = [(label, _grams(text)) for label, text in donors]
    hits = 0
    for crop, field, pid, which, text in notes(batch):
        tg = _grams(text)
        for (label, dtext), (_, dg) in zip(donors, dgrams):
            if _sym(text, dtext) >= COPY_THRESHOLD:
                raise SystemExit(f"REFUSED: {crop}/{pid}/{which} is {_sym(text, dtext):.2f} similar "
                                 f"to {label}; restate it instead of lifting it")
            shared = {g for g in (tg & dg) if not _is_figure_run(g)}
            if shared:
                raise SystemExit(f"REFUSED: {crop}/{pid}/{which} shares a {MIN_RUN_GRAMS}-word "
                                 f"verbatim run with {label}: {sorted(shared)[0]!r}")
        hits += 1
    return hits


def check_no_intra_batch_twins(batch):
    """Seven crops whose source prose is 0% identical must not emerge with identical rung notes.
    A propagated template here would be inventing a claim for six crops out of one crop's read."""
    seen = []
    for crop, field, pid, which, text in notes(batch):
        for (ocrop, opid, owhich, otext) in seen:
            if ocrop == crop:
                continue
            r = _sym(text, otext)
            if r >= TWIN_THRESHOLD:
                raise SystemExit(f"REFUSED: {crop}/{pid}/{which} is {r:.2f} similar to "
                                 f"{ocrop}/{opid}/{owhich}; these are separate authoring passes")
        seen.append((crop, pid, which, text))
    return len(seen)


def check_registers_diverge(batch):
    """Dual register means materially different, not the same sentence reworded."""
    n = 0
    for crop in CROPS:
        for field in ("pests", "diseases"):
            for e in batch[crop].get(field) or []:
                for rung in e.get("control_ladder") or []:
                    b, s = rung.get("note_beginner"), rung.get("note_seasoned")
                    if not s:
                        continue          # a beginner-only rung is legal; the precedent has one
                    if b.strip() == s.strip():
                        raise SystemExit(f"REFUSED: {crop}/{e['id']}/{rung['method']} registers "
                                         f"are identical")
                    if _sym(b, s) >= 0.90:
                        raise SystemExit(f"REFUSED: {crop}/{e['id']}/{rung['method']} registers are "
                                         f"{_sym(b, s):.2f} similar; that is a reword, not a register")
                    n += 1
    return n


def check_copy_hygiene(batch):
    """House style, each rule already ruled elsewhere in the repo."""
    for crop, field, pid, which, text in notes(batch):
        where = f"{crop}/{pid}/{which}"
        if DASHES.search(text):
            raise SystemExit(f"REFUSED: {where} contains an em or en dash")
        if ABSOLUTES.search(text):
            raise SystemExit(f"REFUSED: {where} contains an absolute: "
                             f"{ABSOLUTES.search(text).group(0)!r}")
        if SPACED_F.search(text):
            raise SystemExit(f"REFUSED: {where} has a spaced degree symbol")
        if LADDER_VOCAB.search(text):
            raise SystemExit(f"REFUSED: {where} names the ladder machinery: "
                             f"{LADDER_VOCAB.search(text).group(0)!r}")
        if CAP_PLANT.search(text):
            raise SystemExit(f"REFUSED: {where} capitalizes 'Plant' mid-sentence")
    return True


# ---------------------------------------------------------------- apply / verify

def apply_to(data, pins, batch):
    """Purely additive: three keys onto each of fourteen entries. Nothing else is touched."""
    out = copy.deepcopy(data)
    idx = by_slug(out)
    for crop in CROPS:
        for field in ("pests", "diseases"):
            entries = idx[crop][field]
            authored = {e["id"]: e for e in batch[crop].get(field) or []}
            for row in pins[crop].get(field, []):
                target = [e for e in entries if entry_name(e) == row["name_seasoned"]]
                if len(target) != 1:
                    raise SystemExit(f"REFUSED: {crop}/{field} matched {len(target)} entries for "
                                     f"{row['name_seasoned']!r}")
                e = target[0]
                a = authored[row["id"]]
                e["id"] = row["id"]
                e["type"] = row["type"]
                e["control_ladder"] = copy.deepcopy(a["control_ladder"])
    return out


def verify_post(pre, post, pins, batch):
    """Every changed leaf must be one this batch pinned. SET COMPARISON BEFORE VALUE COMPARISON:
    iterating `pre` alone makes everything ADDED in `post` invisible, which was all four PLA-162
    defects."""
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
        # every key of the crop OTHER than the two problem arrays must be untouched
        for k in set(pre_i[crop]) | set(post_i[crop]):
            if k in ("pests", "diseases"):
                continue
            if json.dumps(pre_i[crop].get(k), sort_keys=True) != \
               json.dumps(post_i[crop].get(k), sort_keys=True):
                raise SystemExit(f"REFUSED: {crop} field {k!r} changed outside the problem arrays")

        for field in ("pests", "diseases"):
            rows = pins[crop].get(field, [])
            src = pre_i[crop].get(field) or []
            got = post_i[crop].get(field) or []
            if len(got) != len(src):
                raise SystemExit(f"REFUSED: {crop}/{field} entry count {len(src)} -> {len(got)}")
            if len(got) != len(rows):
                raise SystemExit(f"REFUSED: {crop}/{field} post has {len(got)}, spec has {len(rows)}")
            authored = {e["id"]: e for e in batch[crop].get(field) or []}
            for s, g, row in zip(src, got, rows):
                if entry_name(g) != entry_name(s):
                    raise SystemExit(f"REFUSED: {crop}/{field} entry order changed")
                # SET COMPARISON FIRST.
                added = set(g) - set(s)
                removed = set(s) - set(g)
                if removed:
                    raise SystemExit(f"REFUSED: {crop}/{entry_name(g)!r} lost keys {sorted(removed)}")
                if added != set(PINNED_FIELDS):
                    raise SystemExit(f"REFUSED: {crop}/{entry_name(g)!r} added {sorted(added)}, "
                                     f"expected exactly {sorted(PINNED_FIELDS)}")
                for k in sorted(set(g) & set(s)):
                    if json.dumps(g[k], sort_keys=True) != json.dumps(s[k], sort_keys=True):
                        raise SystemExit(f"REFUSED: {crop}/{entry_name(g)!r} carried field {k!r} "
                                         f"changed; this promote is purely additive")
                for k in CARRIED_PROSE:
                    if k in s and json.dumps(g[k], sort_keys=True) != json.dumps(s[k], sort_keys=True):
                        raise SystemExit(f"REFUSED: {crop}/{entry_name(g)!r} prose {k!r} changed")
                if g["id"] != row["id"] or g["type"] != row["type"]:
                    raise SystemExit(f"REFUSED: {crop}/{entry_name(g)!r} id/type does not match pin")
                if g["control_ladder"] != authored[row["id"]]["control_ladder"]:
                    raise SystemExit(f"REFUSED: {crop}/{entry_name(g)!r} ladder does not match the "
                                     f"authored output")
                changed += len(PINNED_FIELDS)
    if changed == 0:
        raise SystemExit("REFUSED: nothing changed; the promote would be a no-op")
    return changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="run checks, write nothing")
    ap.add_argument("canonical", nargs="?", default=None)
    ap.add_argument("--canonical", dest="canonical_flag", default=None)
    ap.add_argument("--expect-sha", default=None)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    path = args.canonical_flag or args.canonical

    data = load_canonical(path)
    pins, batch = staged()
    cm = data["control_methods"]

    n = check_pre_state_schema(pins, data)
    print(f"  pre-state schema     {n} entries, no name/id/type/control_ladder, joined on name_seasoned")
    ids, outside = check_ids_are_reused(pins, data)
    print(f"  ids reused           {sorted(ids)} -- 0 minted, all present outside the batch")
    check_batch_matches_spec(pins, batch)
    print("  spec match           OK (ids, types, order, no stray keys)")
    rungs = check_ladders(batch, cm)
    print(f"  ladders              {rungs} rungs, tiers ordered, applies_to reachable")
    nmat = check_no_material_rungs(batch, cm)
    print(f"  no material rungs    {nmat} rungs, all cultural or physical (raw-cut safety refusal)")
    check_no_root_hair_claim(batch)
    print("  no root-hair claim   OK (unsourced against psu_microgreens)")
    check_no_sulfur_oil_interval(batch)
    print("  PLA-457 held         OK (no sulfur/oil interval stated)")
    nc = check_no_precedent_copy(batch, data)
    print(f"  no copy              {nc} notes, none lifted from crop prose or the precedent ladder")
    nt = check_no_intra_batch_twins(batch)
    print(f"  no intra-batch twins {nt} notes compared across crops")
    nr = check_registers_diverge(batch)
    print(f"  registers diverge    {nr} rung pairs")
    check_copy_hygiene(batch)
    print("  copy hygiene         OK")

    post = apply_to(data, pins, batch)
    leaves = verify_post(data, post, pins, batch)
    print(f"  verify post          {leaves} pinned leaves changed, nothing else")

    blob = serialize(post)
    new_sha = sha256_bytes(blob)
    print(f"\n  {BASE_SHA[:8]} -> {new_sha}")
    if args.expect_sha and new_sha != args.expect_sha:
        sys.exit(f"REFUSED: expected {args.expect_sha}, got {new_sha}")
    if args.check and not args.apply:
        print("  --check: nothing written")
        return 0
    with open(path or CANON, "wb") as f:
        f.write(blob)
    print(f"  WROTE {path or CANON}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
