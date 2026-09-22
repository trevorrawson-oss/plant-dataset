#!/usr/bin/env python3
"""promote_pla580_plants_per_pot -- PLA-580 / PLA-7 Plan C, container_notes.plants_per_pot
(spec docs/superpowers/specs/2026-09-21-pla580-plants-per-pot-field-shape.md; register row 31).
Base 079e3923 (PLA-466's rootstock attribution repair).

WHAT MOVES. On every one of the 121 CERTIFIED crops, one new key inside container_notes:
plants_per_pot. SEVEN crops take an object carrying EIGHT readings between them (Illinois
Extension on all seven, UMD Extension on eggplant as well), each reading a {count, at_gallons,
sources, anchoring_urls}. The other 114 certified crops take null, meaning "no T1 count read".
Every authored crop also takes one verification_status.field_additions[] entry PER READING,
carrying the URL, the fetch date, the byte count, the sha256 and the verbatim source row. The 7
uncertified shells are NOT touched and stay byte-identical (A39/A60 exempt them by status).
Nothing else moves: no min_pot_gallons, no recommended_pot_gallons, no prose.

WHY EACH GUARD EXISTS.
 1. THE SPEC IS THE SHAPE THAT WAS RULED. base_sha pinned; the authored crop set, and every count
    and at_gallons pair, compared to EXPECTED_READINGS -- INDEPENDENT LITERALS, not values computed
    from the spec, because an expectation derived from the thing it validates is vacuous. The
    staging builder derives from the source bytes; this file verifies against the ruling.
 2. THE HOLDS ARE A DECISION, NOT AN OMISSION. Every count-bearing source row is either authored,
    or recorded in source_ledger as held (ruling 5) or unauthored. A count-bearing row that is
    none of those three REFUSES, so a later source row cannot be dropped silently.
 3. EVERY AUTHORED VALUE PASSES THE GATE BEFORE IT IS WRITTEN: plants_per_pot_gate.shape_violations
    (imported, never retyped) and numeric_sanity_gate on a synthetic crop carrying the spec row.
 4. PROVENANCE IS PART OF THE ROW, ONE RECORD PER READING: field == "plants_per_pot", date pinned,
    sources non-empty and in source_catalog, the note naming the URL and quoting the page, and
    EVERY sha256 quoted anywhere in the spec is one of the digests THIS pass measured.
 5. THE BASE CARRIES NO plants_per_pot KEY and no plants_per_pot field_additions entry, anywhere.
 6. THE GATES RUN ON THE POST-STATE with presence ON, plus numeric_sanity and display_readiness on
    every authored crop.
 7. THE PLANNER EFFECT IS PINNED. The ruled formula (plants_per_pot_gate.planner_gallons_per_plant)
    is run over the post-state and compared to PLANNER_EFFECT: exactly two crops switch, and to the
    figures Trevor approved. This is what stops an authoring change from quietly loosening the
    planner: if a third crop switches, or a figure moves, the promote refuses.
 8. BLAST RADIUS AT THE LEAF, SET BEFORE VALUE: top-level, roster, crop-level, container_notes and
    verification_status key sets are compared BEFORE any value (iterating `pre` alone makes
    everything ADDED in `post` invisible); every shell byte-identical; on each certified crop
    container_notes grows by exactly one key and nothing else differs but field_additions
    (append-only behind a byte-identical prefix); each written value is compared to its OWN spec row.

Usage:
    promote_pla580_plants_per_pot.py --check
    promote_pla580_plants_per_pot.py --out /path/scratch.json
    promote_pla580_plants_per_pot.py --expect-sha <sha>       # writes canonical, on approval only
"""
import argparse, copy, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CANON = os.path.join(REPO, "crops_data_final.json")
STAGE = os.path.join(HERE, "staging", "pla580_plants_per_pot")
SPEC = os.path.join(STAGE, "spec.json")

sys.path.insert(0, HERE)
import plants_per_pot_gate as PPG  # noqa: E402  -- imported, never retyped
from numeric_sanity_gate import numeric_sanity_violations  # noqa: E402
from display_readiness_gate import display_readiness_violations  # noqa: E402

BASE_SHA = "079e3923660a53189bcf5e0bee0506e78225e473b2dadcba54cbfb3045337696"  # PLA-466, 9429413
ROSTER = 128
CERTIFIED = "verified_gs_arc"
FIELD = PPG.FIELD
FA_KEYS = ("field", "date", "sources", "note")
FA_FIELD = PPG.PROVENANCE_FIELD
FA_DATE = "2026-09-21"

EXPECTED_KEYS = 121
EXPECTED_AUTHORED_CROPS = 7
EXPECTED_READINGS_TOTAL = 8
EXPECTED_SHELLS = 7

# THE RULED AUTHORING, as independent literals (spec section 9). Written from the ruling, then
# checked against what the staging builder derived from the bytes; the two agreeing is the
# measurement. A row here that the builder did not produce, or vice versa, REFUSES.
EXPECTED_READINGS = {
    "parsley":          [("uiuc_ext", [1, 1], [0.5, 0.5])],
    "cabbage":          [("uiuc_ext", [1, 1], [1, 1])],
    "green-beans-bush": [("uiuc_ext", [2, 3], [1, 1])],
    "lettuce-leaf":     [("uiuc_ext", [4, 6], [1, 1])],
    "swiss-chard":      [("uiuc_ext", [1, 1], [1, 1])],
    "cherry-tomato":    [("uiuc_ext", [1, 1], [1, 1])],
    "eggplant":         [("uiuc_ext", [1, 1], [2, 2]), ("umd_ext", [1, 1], [8, 10])],
}

# THE PLANNER EFFECT, pinned (spec 5.1, recomputed under amendment 4's count[min] divisor).
# Only these two crops have a reading whose count is not [1, 1], so only these two switch under
# ruling 3. BOTH ARE MORE PERMISSIVE and neither has a reading that restrains it, which is the
# honest result this pass puts in front of Trevor by name rather than inside a roster count:
# green beans sit in UMD's "Medium Vegetables" class and lettuce in "Small Vegetables", and
# NEITHER class publishes a count, so ruling 2 has nothing to choose from.
PLANNER_EFFECT = {
    "green-beans-bush": {"before_min_pot_gallons": 5, "after_gallons_per_plant": 0.5},
    "lettuce-leaf":     {"before_min_pot_gallons": 1, "after_gallons_per_plant": 0.25},
}

# Every sha256 quoted in staged prose must be one of these MEASURED digests. Measured 2026-09-21
# by this session, twice, under two different user-agents, and independently reproducing the two
# digests the spec's section 12 recorded. A digest not on this list REFUSES: the shape of a hash
# field pulls a fabricated value out of you (PLA-465 near-miss, 16 chars measured, 48 invented).
#
# KEYED BY SOURCE, not a bare set. A set only answers "is this digest one we measured", which the
# blanket scan below already answers; measured, a per-source membership check was REDUNDANT and its
# mutation SURVIVED because the scan fired first. Keyed, it answers the question the scan cannot:
# is THIS page's digest the one measured FOR THIS PAGE. A two-source arc can swap them, and both
# halves of the swap are legitimately measured digests.
EVIDENCE_HASHES = {
    "uiuc_ext": "f9f336d5eb33a1dc0833f53d98b2e909cf2d6ce920795dc8913fab94de393119",  # container table
    "umd_ext": "96521c5d0cf8860e7895a8c6da426ac48a372894c531431c64666bda8151f407",   # types-containers
}
MEASURED_DIGESTS = set(EVIDENCE_HASHES.values())
SHA256_RE = re.compile(r"\b[0-9a-f]{64}\b")
LEDGER_OUTCOMES = ("AUTHORED", "HELD", "UNAUTHORED", "NO COUNT")


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def serialize(data):
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def by_slug(data):
    return {c["slug"]: c for c in data["crops"]}


def load_canonical(path=None):
    p = path or CANON
    with open(p, "rb") as f:
        raw = f.read()
    got = sha256_bytes(raw)
    if got != BASE_SHA:
        raise SystemExit(f"REFUSED: canonical is {got[:8]}, this promote is pinned to {BASE_SHA[:8]}")
    return json.loads(raw)


def staged():
    with open(SPEC, encoding="utf-8") as f:
        return json.load(f)


def _certified(crop):
    return (crop.get("verification_status") or {}).get("status") == CERTIFIED


def _cn(crop):
    return crop.get("container_notes") or {}


def _value(row):
    return {"readings": copy.deepcopy(row["readings"])}


def _synthetic(row, base_crop):
    """A copy of the base crop carrying the spec row, for running the gates BEFORE the write."""
    c = copy.deepcopy(base_crop)
    c["container_notes"][FIELD] = _value(row)
    vs = c["verification_status"]
    vs["field_additions"] = list(vs.get("field_additions") or []) + copy.deepcopy(row["field_additions"])
    return c


def check_spec_shape(spec, expected_crops):
    if spec.get("base_sha") != BASE_SHA:
        raise SystemExit("REFUSED: spec base_sha is not the pinned base")
    if spec.get("fetch_date") != FA_DATE:
        raise SystemExit(f"REFUSED: spec fetch_date {spec.get('fetch_date')!r} is not {FA_DATE}")
    rows = spec["authored"]
    if expected_crops is None or len(rows) != expected_crops:
        raise SystemExit(f"REFUSED: {len(rows)} authored crops, pinned {expected_crops}")

    # GUARD 1: the spec is the RULING. Set comparison before value comparison, so a crop added to
    # the spec and absent from the ruling cannot hide behind a per-row loop over the ruling.
    if {r["crop"] for r in rows} != set(EXPECTED_READINGS):
        raise SystemExit(f"REFUSED: authored crop set is not the ruled one; spec-only "
                         f"{sorted({r['crop'] for r in rows} - set(EXPECTED_READINGS))}, "
                         f"ruling-only {sorted(set(EXPECTED_READINGS) - {r['crop'] for r in rows})}")
    # NO DUPLICATE-CROP GUARD. The PLA-465 pattern carried one ("crop X appears twice"), and here it
    # is UNREACHABLE: `len(rows)` is pinned to 7 and the crop SET is compared to the 7 ruled crops,
    # so a duplicate necessarily shrinks the set and the comparison above answers first. Measured --
    # the driver for it reddened on the set-comparison message, not its own. An unreachable guard is
    # worse than no guard because it reads as coverage, so it is removed rather than shipped.
    total = 0
    for r in rows:
        crop = r["crop"]
        if set(r) != {"crop", "readings", "field_additions"}:
            raise SystemExit(f"REFUSED: authored row {crop} has keys {sorted(r)}")
        got = [(rd["sources"][0] if rd.get("sources") else None, rd.get("count"), rd.get("at_gallons"))
               for rd in r["readings"]]
        want = [(s, list(c), list(g)) for s, c, g in EXPECTED_READINGS[crop]]
        if got != want:
            raise SystemExit(f"REFUSED: {crop} readings are {got}, ruled {want}")
        if len(r["field_additions"]) != len(r["readings"]):
            raise SystemExit(f"REFUSED: {crop} has {len(r['readings'])} readings but "
                             f"{len(r['field_additions'])} provenance records; one per reading")
        total += len(r["readings"])
        for fa in r["field_additions"]:
            if set(fa) != set(FA_KEYS) or fa["field"] != FA_FIELD:
                raise SystemExit(f"REFUSED: {crop} field_addition has the wrong shape")
            if fa["date"] != FA_DATE:
                raise SystemExit(f"REFUSED: {crop} field_addition date {fa['date']!r} is not {FA_DATE}")
            if not fa["sources"]:
                raise SystemExit(f"REFUSED: {crop} field_addition carries no sources")
            if not (fa["note"] or "").strip() or "http" not in fa["note"]:
                raise SystemExit(f"REFUSED: {crop} field_addition note does not name its page")
            if "sha256" not in fa["note"]:
                raise SystemExit(f"REFUSED: {crop} field_addition note quotes no digest")
            if "verbatim:" not in fa["note"]:
                raise SystemExit(f"REFUSED: {crop} field_addition note quotes no source text")
            if "—" in fa["note"] or "–" in fa["note"]:
                raise SystemExit(f"REFUSED: {crop} field_addition note carries an em or en dash")
        # each reading's provenance must name the SAME institution the reading cites, or a record
        # credits a page that did not say it (template inheritance fabricates attributions).
        for rd, fa in zip(r["readings"], r["field_additions"]):
            if sorted(rd["sources"]) != sorted(fa["sources"]):
                raise SystemExit(f"REFUSED: {crop} reading cites {rd['sources']} but its record "
                                 f"credits {fa['sources']}")
            for s in rd["sources"]:
                if rd["anchoring_urls"][s]["url"] not in fa["note"]:
                    raise SystemExit(f"REFUSED: {crop} record does not name the url its reading anchors")
    if total != EXPECTED_READINGS_TOTAL:
        raise SystemExit(f"REFUSED: {total} readings, pinned {EXPECTED_READINGS_TOTAL}")

    # GUARD 2: every count-bearing source row is authored, held or unauthored. A hold is a decision.
    ledger = spec["source_ledger"]
    if not ledger:
        raise SystemExit("REFUSED: spec carries no source_ledger; a hold must be recorded, not omitted")
    for e in ledger:
        if set(e) != {"source_row", "outcome", "why"}:
            raise SystemExit(f"REFUSED: source_ledger entry has keys {sorted(e)}")
        if not e["outcome"].startswith(LEDGER_OUTCOMES):
            raise SystemExit(f"REFUSED: source_ledger outcome {e['outcome']!r} is not one of "
                             f"{LEDGER_OUTCOMES}; every count-bearing row is authored, held or unauthored")
        if not (e["why"] or "").strip():
            raise SystemExit(f"REFUSED: source_ledger entry {e['source_row']!r} records no reason")
    # `.split("-> ")[-1]` rather than `[1]`, and `.get` below rather than `[]`: these two lookups
    # are only reached on input the checks above already constrain, so a dedicated guard for them
    # would be unreachable coverage. Making them TOTAL instead means malformed input REFUSES on the
    # existing comparison rather than dying with a KeyError or an IndexError, which is a strictly
    # worse failure mode than a refusal and reads as a crash rather than as a caught defect.
    authored_in_ledger = {e["outcome"].split("-> ")[-1] for e in ledger if e["outcome"].startswith("AUTHORED")}
    if authored_in_ledger != set(EXPECTED_READINGS):
        raise SystemExit(f"REFUSED: source_ledger authors {sorted(authored_in_ledger)}, "
                         f"ruled {sorted(EXPECTED_READINGS)}")

    # GUARD 4: no fabricated digest, anywhere in the staged artifact...
    for d in set(SHA256_RE.findall(json.dumps(spec, ensure_ascii=False))):
        if d not in MEASURED_DIGESTS and d != BASE_SHA:
            raise SystemExit(f"REFUSED: the spec quotes sha256 {d[:16]}... which is not a measured "
                             f"evidence digest")
    # ... and no digest against the WRONG page. The scan above cannot see this: a swap between two
    # sources leaves both digests measured. Keyed, per source, and again per record, so a note
    # cannot credit one institution while quoting the other institution's page.
    if set(spec["sources"]) != set(EVIDENCE_HASHES):
        raise SystemExit(f"REFUSED: spec sources are {sorted(spec['sources'])}, measured "
                         f"{sorted(EVIDENCE_HASHES)}")
    for key, s in spec["sources"].items():
        if s["sha256"] != EVIDENCE_HASHES[key]:
            raise SystemExit(f"REFUSED: source {key} carries digest {s['sha256'][:16]}..., measured "
                             f"{EVIDENCE_HASHES[key][:16]}... for that page")
    for r in rows:
        for fa in r["field_additions"]:
            for src in fa["sources"]:
                if EVIDENCE_HASHES.get(src, "\x00unmeasured") not in fa["note"]:
                    raise SystemExit(f"REFUSED: {r['crop']} record credits {src} but quotes another "
                                     f"page's digest")

    if spec["expected"] != {"keys": EXPECTED_KEYS, "authored_crops": expected_crops,
                            "readings": EXPECTED_READINGS_TOTAL,
                            "null": EXPECTED_KEYS - expected_crops, "shells": EXPECTED_SHELLS}:
        raise SystemExit("REFUSED: spec expected block is not the promote's pins")
    return len(rows)


def check_pre_state(spec, data):
    idx = by_slug(data)
    if len(data["crops"]) != ROSTER:
        raise SystemExit(f"REFUSED: roster is {len(data['crops'])}, pinned {ROSTER}")
    certified = [c for c in data["crops"] if _certified(c)]
    if len(certified) != EXPECTED_KEYS:
        raise SystemExit(f"REFUSED: {len(certified)} certified crops, pinned {EXPECTED_KEYS}")
    catalog = set((data.get("source_catalog") or {}).keys())
    for c in data["crops"]:
        if FIELD in _cn(c):
            raise SystemExit(f"REFUSED: {c['slug']} already carries container_notes.{FIELD}")
        fa = (c.get("verification_status") or {}).get("field_additions")
        if _certified(c) and not isinstance(fa, list):
            raise SystemExit(f"REFUSED: {c['slug']} verification_status.field_additions is not a list")
        if any(isinstance(x, dict) and x.get("field") == FA_FIELD for x in (fa or [])):
            raise SystemExit(f"REFUSED: {c['slug']} already records a {FA_FIELD} addition")
    for r in spec["authored"]:
        c = idx.get(r["crop"])
        if c is None:
            raise SystemExit(f"REFUSED: authored crop {r['crop']} is not on the roster")
        if not _certified(c):
            raise SystemExit(f"REFUSED: authored crop {r['crop']} is not certified")
        if _cn(c).get("container_ok") is not True:
            raise SystemExit(f"REFUSED: authored crop {r['crop']} is not container_ok; a per-pot "
                             f"count needs a crop that can go in a pot")
        for fa in r["field_additions"]:
            for s in fa["sources"]:
                if s not in catalog:
                    raise SystemExit(f"REFUSED: source {s!r} on {r['crop']} is not in source_catalog")
        syn = _synthetic(r, c)
        v = PPG.shape_violations(syn)
        if v:
            raise SystemExit(f"REFUSED: {r['crop']} spec row fails plants_per_pot_gate: {v}")
        nv = numeric_sanity_violations(syn)
        if nv:
            raise SystemExit(f"REFUSED: {r['crop']} spec row fails numeric_sanity: {nv}")
    return len(spec["authored"])


def apply_to(data, spec):
    post = copy.deepcopy(data)
    rows = {r["crop"]: r for r in spec["authored"]}
    for c in post["crops"]:
        if not _certified(c):
            continue
        r = rows.get(c["slug"])
        c["container_notes"][FIELD] = _value(r) if r else None
        if r:
            c["verification_status"]["field_additions"].extend(copy.deepcopy(r["field_additions"]))
    return post


def planner_effect(data):
    """The ruled formula, run over a state: {slug: gallons per plant} for every crop that switches."""
    out = {}
    for c in data["crops"]:
        g = PPG.planner_gallons_per_plant(c)
        if g is not None:
            out[c["slug"]] = g
    return out


def check_post(post, spec):
    v = PPG.all_violations(post, presence=True)
    if v:
        raise SystemExit("REFUSED: plants_per_pot_gate on the post-state: " + "; ".join(v[:5]))
    idx = by_slug(post)
    for r in spec["authored"]:
        nv = numeric_sanity_violations(idx[r["crop"]])
        if nv:
            raise SystemExit(f"REFUSED: numeric_sanity on {r['crop']}: {nv}")
        dv = display_readiness_violations(idx[r["crop"]])
        if dv:
            raise SystemExit(f"REFUSED: display_readiness on {r['crop']}: {dv}")
    # GUARD 7: the planner effect is the approved one, set before value.
    got = planner_effect(post)
    if set(got) != set(PLANNER_EFFECT):
        raise SystemExit(f"REFUSED: the planner switches on {sorted(got)}, approved "
                         f"{sorted(PLANNER_EFFECT)}; a crop gaining or losing the switch is a "
                         f"product change, not an authoring detail")
    for slug, want in PLANNER_EFFECT.items():
        if got[slug] != want["after_gallons_per_plant"]:
            raise SystemExit(f"REFUSED: {slug} prices at {got[slug]} gal/plant, approved "
                             f"{want['after_gallons_per_plant']}")
        if _cn(idx[slug]).get("min_pot_gallons") != want["before_min_pot_gallons"]:
            raise SystemExit(f"REFUSED: {slug} min_pot_gallons is "
                             f"{_cn(idx[slug]).get('min_pot_gallons')!r}, approved against "
                             f"{want['before_min_pot_gallons']}")
    return got


def _j(x):
    return json.dumps(x, sort_keys=True)


def verify_post(pre, post, spec):
    """SET COMPARISON BEFORE VALUE COMPARISON, at every level."""
    if set(pre) != set(post):
        raise SystemExit("REFUSED: top-level key set changed")
    for k in pre:
        if k != "crops" and _j(pre[k]) != _j(post[k]):
            raise SystemExit(f"REFUSED: top-level key {k!r} changed")
    pre_i, post_i = by_slug(pre), by_slug(post)
    if set(pre_i) != set(post_i) or len(pre["crops"]) != len(post["crops"]):
        raise SystemExit("REFUSED: crop roster changed")
    rows = {r["crop"]: r for r in spec["authored"]}
    keys = authored = nulls = readings = 0
    for slug in pre_i:
        s, g = pre_i[slug], post_i[slug]
        if not _certified(s):
            if _j(s) != _j(g):
                raise SystemExit(f"REFUSED: shell {slug} changed")
            continue
        if set(g) != set(s):
            raise SystemExit(f"REFUSED: {slug} crop-level key set changed")
        for k in s:
            if k in ("verification_status", "container_notes"):
                continue
            if _j(s[k]) != _j(g[k]):
                raise SystemExit(f"REFUSED: {slug} field {k!r} changed outside container_notes")
        scn, gcn = s["container_notes"], g["container_notes"]
        if set(gcn) != set(scn) | {FIELD}:
            raise SystemExit(f"REFUSED: {slug} container_notes key set is not the base's plus {FIELD}")
        for k in scn:
            if _j(scn[k]) != _j(gcn[k]):
                raise SystemExit(f"REFUSED: {slug} container_notes.{k} changed; this pass touches "
                                 f"only {FIELD}")
        keys += 1
        r = rows.get(slug)
        if r:
            if _j(gcn[FIELD]) != _j(_value(r)):
                raise SystemExit(f"REFUSED: {slug} written {FIELD} is not the spec row's")
            authored += 1
            readings += len(gcn[FIELD]["readings"])
        else:
            if gcn[FIELD] is not None:
                raise SystemExit(f"REFUSED: {slug} carries a {FIELD} value with no authored row")
            nulls += 1
        sv, gv = s["verification_status"], g["verification_status"]
        if set(sv) != set(gv):
            raise SystemExit(f"REFUSED: {slug} verification_status key set changed")
        for k in sv:
            if k != "field_additions" and _j(sv[k]) != _j(gv[k]):
                raise SystemExit(f"REFUSED: {slug} verification_status.{k} changed")
        a, b = sv["field_additions"], gv["field_additions"]
        if _j(b[:len(a)]) != _j(a):
            raise SystemExit(f"REFUSED: {slug} field_additions prefix is not byte-identical")
        want_tail = r["field_additions"] if r else []
        if _j(b[len(a):]) != _j(want_tail):
            raise SystemExit(f"REFUSED: {slug} field_additions appended {len(b) - len(a)} entries, "
                             f"expected {len(want_tail)} matching the spec")
    if readings != EXPECTED_READINGS_TOTAL:
        raise SystemExit(f"REFUSED: {readings} readings written, pinned {EXPECTED_READINGS_TOTAL}")
    # keys / authored / nulls are IMPLIED by the per-crop checks above (every certified crop must
    # carry the key; a value with no row refuses), so refusing on those totals could never fire in
    # isolation and would read as coverage. Informational only. `readings` is NOT implied: a row
    # could carry the wrong NUMBER of readings and still match its own spec row, so it is pinned.
    return keys, authored, nulls, readings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="run checks, write nothing")
    ap.add_argument("canonical", nargs="?", default=None)
    ap.add_argument("--canonical", dest="canonical_flag", default=None)
    ap.add_argument("--expect-sha", default=None)
    ap.add_argument("--out", default=None, help="write the post-state HERE instead of over the canonical")
    args = ap.parse_args()
    path = args.canonical_flag or args.canonical
    if args.out and os.path.abspath(args.out) == os.path.abspath(path or CANON):
        sys.exit("REFUSED: --out may not target the canonical; use --expect-sha for the write")

    data = load_canonical(path)
    spec = staged()
    n = check_spec_shape(spec, EXPECTED_AUTHORED_CROPS)
    print(f"  spec shape        {n} authored crops / {EXPECTED_READINGS_TOTAL} readings match the "
          f"ruling; {EXPECTED_KEYS} keys; {EXPECTED_KEYS - n} null; {EXPECTED_SHELLS} shells untouched; "
          f"{len(spec['source_ledger'])} source rows all authored, held or unauthored; digests measured")
    n = check_pre_state(spec, data)
    print(f"  pre-state         no {FIELD} key and no {FA_FIELD} record on any crop; {n} authored "
          f"crops certified + container_ok, sources in catalog, every row passes the gate and the bounds")
    post = apply_to(data, spec)
    effect = check_post(post, spec)
    print(f"  post gates        plants_per_pot_gate (presence ON) 0; numeric_sanity + "
          f"display_readiness clean on the authored crops")
    print(f"  planner effect    switches on {len(effect)}: " + ", ".join(
        f"{s} {PLANNER_EFFECT[s]['before_min_pot_gallons']:g} -> {effect[s]:g} gal/plant "
        f"({PLANNER_EFFECT[s]['before_min_pot_gallons'] / effect[s]:g}x more permissive)"
        for s in sorted(effect)))
    keys, authored, nulls, readings = verify_post(data, post, spec)
    print(f"  verify post       {keys} crops took the key: {authored} authored carrying {readings} "
          f"readings, {nulls} null; nothing else")

    blob = serialize(post)
    new_sha = sha256_bytes(blob)
    print(f"\n  {BASE_SHA[:8]} -> {new_sha}")
    if args.expect_sha and new_sha != args.expect_sha:
        sys.exit(f"REFUSED: expected {args.expect_sha}, got {new_sha}")
    if args.out:
        with open(args.out, "wb") as f:
            f.write(blob)
        print(f"  WROTE post-state to {args.out} (canonical untouched)")
        return 0
    if args.check:
        print("  --check: nothing written")
        return 0
    if not args.expect_sha:
        sys.exit("REFUSED: writing canonical requires --expect-sha (the gauntleted scratch SHA)")
    with open(path or CANON, "wb") as f:
        f.write(blob)
    print(f"  WROTE {path or CANON}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
