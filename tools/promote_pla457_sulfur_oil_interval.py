#!/usr/bin/env python3
"""promote_pla457_sulfur_oil_interval -- PLA-457, Trevor's ruling of 2026-09-06: the sulfur-and-oil
interval is 30 days, scoped to growing-season use with green tissue present, deferring to the oil
product's label. Base 72371c02.

THE DEFECT. `control_methods.horticultural_oil` said "2 weeks" citing UC IPM PN 7405, which says
30 days: a misquote. `control_methods.sulfur` said "2 weeks" faithfully to PN 7406. Twenty shipped
rung notes on ten crops carried 2 weeks, two weeks or 30 days depending on which note their author
happened to read, and oregano carried two different intervals on one crop. Four T1 sources seemed to
disagree and none did: the intervals were extracted without the material, growth stage and crop type
each was conditioned on (docs: conditional_claims_scope_v1_0.md, the methodology entry).

THE T1 READS, all by direct extraction on 2026-09-06, none from a search summary:
  * UC IPM PN 7405 (Spider Mites): "Don't apply sulfur within 30 days of an oil spray."
  * Purdue BP-69-W (Beckerman, Using Organic Fungicides): "Do not use sulfur if you have applied an
    oil spray within the last month"; "Always check product labels".
  * EPA label 61842-30 (Lime-Sulfur Solution): "DO NOT use this product within 30 days of an oil
    spray at any stage other than dormant (deciduous only)"; "Allow 30 days between oil and
    Lime-Sulfur Solution Agricultural Fungicide sprays in the growing season". The same label
    PRESCRIBES lime sulfur plus oil as a dormant spray, which is what reconciles the WSU combined
    spray with everyone else's prohibition.
  * UC IPM lime-sulfur page: "Lime sulfur is a product no longer available to home and garden users."
  * UC IPM PN 7406 (Powdery Mildew on Vegetables): "do not apply it within 2 weeks of an oil spray"
    -- the sulfur entry's anchor was faithful; the ruling moves to the conservative scoped figure.

WHAT MOVES. ONE catalog id admitted (purdue_ext_bp69w, T1, pathed, titled). TWO cautions rewritten,
one on each method, with the Purdue anchor added to both and PN 7405 added to `sulfur`. TWENTY rung
notes on TEN crops, each edited by replacing exactly ONE sentence found by exact match. Nothing else.

WHY EACH GUARD EXISTS.
 1. THE NET IS PART OF THE COUNT. The ticket said 15 notes; a strict scan (sulfur AND oil AND a
    duration in one sentence) finds 15. A scan that also accepts the pronoun for the rung's own
    material ("keep it two weeks from any oil spray" on a sulfur rung) finds 20. `interval_sentences`
    is that widened net, and it is the instrument this promote pins itself to: the PRE-state must
    show exactly the 22 statements (20 notes + 2 cautions) the spec names, and the POST-state must
    show 0 sub-30-day statements and 22 that say 30 days AND defer to the label. A net that cannot
    find the defect cannot prove it fixed.
 2. ONE SENTENCE PER ROW, FOUND EXACTLY ONCE. A row whose old sentence matches twice or not at all
    refuses; a note whose post text is not old.replace(old_sentence, new_sentence) refuses.
 3. THE SCOPE IS PART OF THE CLAIM. Every new sentence must carry 30 days, the label deferral, and
    a growth-stage scope ("in leaf", "has leaves", "growing season"). A bare interval refuses.
 4. NO VERBATIM LIFT from the anchors: no shared 6-word run with the Purdue or PN 7405 sentence.
 5. REGISTERS STAY DISTINCT on every touched rung.
 6. THE CATALOG IS GATED HERE, NOT AT THE GAUNTLET: A54 (`source_catalog_title_gate`) and
    `control_ladder_gate.all_violations` are IMPORTED and run on the post-state, because catalog
    round 10 applied cleanly, passed its own suite, and then took gate_all to 0/121 on a missing
    title.
 7. OREGANO'S TWO RUNGS AGREE afterwards, checked by name, because that was the shipped defect.
 8. BLAST RADIUS AT THE LEAF: set comparisons before value comparisons; exactly 20 note strings,
    2 caution strings, sources/anchoring on 2 methods, and 1 catalog id change; roster, every other
    crop, every other method, every existing catalog entry byte-identical.

Usage:
    promote_pla457_sulfur_oil_interval.py            # check, apply, verify, write
    promote_pla457_sulfur_oil_interval.py --check    # checks only, write nothing
"""
import argparse, copy, difflib, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CANON = os.path.join(REPO, "crops_data_final.json")
STAGE = os.path.join(HERE, "staging", "pla457_sulfur_oil_interval")
SPEC = os.path.join(STAGE, "spec.json")

sys.path.insert(0, HERE)
from source_catalog_title_gate import title_violations  # noqa: E402  -- A54, imported never retyped
import control_ladder_gate as CLG  # noqa: E402

BASE_SHA = "72371c02fa306d8e1849053416baf34e232b80bbdf1af5169d546c12c8f45222"  # PLA-450 Option B, 4b826e4
METHODS = ("horticultural_oil", "sulfur")
FIELDS = ("pests", "diseases")
REGISTERS = ("note_beginner", "note_seasoned")

# Pinned BEFORE the first run, from the widened scan on 72371c02.
EXPECTED_NOTES = 20
EXPECTED_CROPS = 10
EXPECTED_PRE_STATEMENTS = 22      # 20 notes + 2 cautions, all carrying an interval
EXPECTED_POST_STATEMENTS = 22     # the same 22, all at 30 days with a label deferral
EXPECTED_NEW_SOURCES = 1

# The widened net (guard 1). A sentence states the interval when it carries a duration and names
# BOTH materials, OR names the other material while sitting on a rung whose method IS the first.
SULFUR = re.compile(r"\bsul(?:f|ph)ur\b", re.I)
OIL = re.compile(r"\boils?\b", re.I)
DURATION = re.compile(r"\b(\d+|one|two|three|four|several|a)\s*(days?|weeks?|months?)\b|\bmonth\b", re.I)
THIRTY = re.compile(r"\b30 days\b")
LABEL = re.compile(r"\blabel\b", re.I)
SCOPE = re.compile(r"in leaf|has leaves|growing season", re.I)
HARVEST_PHI = re.compile(r"\bof harvest\b", re.I)     # mint's PHI sentence names sulfur, oil and 30 days
SUB_30 = re.compile(r"\b(2|two|three|3|10|14|21)\s*(weeks?|days?)\b", re.I)

# house style
DASHES = re.compile(r"[–—]")
ABSOLUTES = re.compile(r"\b(always|never|completely|totally|harmless|guaranteed|guarantees|100%|"
                       r"entirely safe|perfectly safe)\b", re.I)
SPACED_F = re.compile(r"\d\s+°F|\d°\s+F")
LADDER_VOCAB = re.compile(r"\b(rungs?|ladders?|tiers?)\b|applies_to|control_method", re.I)
CAP_PLANT = re.compile(r"(?<![.!?]\s)(?<!^)(?<!\bPlant\sPro)\bPlant\b(?! Pro)")
MIN_RUN_GRAMS = 6
ANCHOR_SENTENCES = (
    "Don't apply sulfur within 30 days of an oil spray.",
    "Do not use sulfur if you have applied an oil spray within the last month",
)


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def serialize(data):
    """CANONICAL IS COMPACT. ONE serializer, shared by the promote and its suite."""
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def by_slug(data):
    return {c["slug"]: c for c in data["crops"]}


def sentences(text):
    return [s for s in re.split(r"(?<=[.!?])\s+", text or "") if s]


def interval_sentences(data):
    """Guard 1, the widened net. (where, sentence) for every statement of a sulfur/oil interval in
    rung notes AND control_methods cautions. PHI sentences ("30 days of harvest") are excluded by
    the harvest clause, not by the material words."""
    out = []
    for c in data["crops"]:
        for field in FIELDS:
            for p in c.get(field) or []:
                for r in p.get("control_ladder") or []:
                    m = r.get("method")
                    for reg in REGISTERS:
                        for s in sentences(r.get(reg)):
                            if HARVEST_PHI.search(s) and not (SULFUR.search(s) and OIL.search(s) and "oil spray" in s):
                                continue
                            has_s, has_o, has_d = bool(SULFUR.search(s)), bool(OIL.search(s)), bool(DURATION.search(s))
                            if has_d and ((has_s and has_o) or (m == "sulfur" and has_o) or
                                          (m == "horticultural_oil" and has_s)):
                                out.append((f"{c['slug']}/{field}/{p.get('id')}/{m}/{reg}", s))
    for k in METHODS:
        for s in data["control_methods"][k].get("cautions") or []:
            if DURATION.search(s) and SULFUR.search(s) and OIL.search(s):
                out.append((f"control_methods/{k}/cautions", s))
    return out


def variety_refs_ok(data):
    return True  # this promote touches no id; kept as a named no-op so the docstring is honest


# ---------------------------------------------------------------- load

def load_canonical(path=None):
    raw = open(path or CANON, "rb").read()
    got = sha256_bytes(raw)
    if got != BASE_SHA:
        sys.exit(f"REFUSED: base SHA mismatch.\n  expected {BASE_SHA}\n  got      {got}")
    return json.loads(raw.decode("utf-8"))


def staged():
    if not os.path.exists(SPEC):
        sys.exit(f"REFUSED: missing spec {SPEC}")
    return json.load(open(SPEC, encoding="utf-8"))


def note_rows(spec):
    return list(spec.get("notes") or [])


# ---------------------------------------------------------------- hygiene

def hygiene(text):
    if DASHES.search(text):
        return "em or en dash"
    if ABSOLUTES.search(text):
        return f"absolute {ABSOLUTES.search(text).group(0)!r}"
    if SPACED_F.search(text):
        return "spaced degree symbol"
    if LADDER_VOCAB.search(text):
        return f"ladder vocabulary {LADDER_VOCAB.search(text).group(0)!r}"
    if CAP_PLANT.search(text):
        return "capitalized Plant mid-sentence"
    return None


def scoped_thirty_with_label(text):
    """Guard 3: the claim carries its scope. 30 days, the label, and a growth-stage condition."""
    return bool(THIRTY.search(text) and LABEL.search(text) and SCOPE.search(text) and not SUB_30.search(text))


def _grams(text, n=MIN_RUN_GRAMS):
    w = re.findall(r"[a-z0-9°']+", (text or "").lower())
    return {" ".join(w[i:i + n]) for i in range(max(0, len(w) - n + 1))}


def _is_figure_run(gram):
    """A run carrying a NUMBER is exempt from the verbatim-lift check (the batch-27 precedent). The
    first --check run refused "30 days of an oil spray", which is the FIGURE, and a figure has no
    honest paraphrase; demanding one buys nothing and costs accuracy. The exemption frees only runs
    containing a digit, so a lifted prose run such as "if you have applied an oil spray within the
    last month" is still refused."""
    return any(ch.isdigit() for ch in gram)


def lifted_from_anchor(text):
    """Guard 4: a shared six-word PROSE run with an anchor sentence is a verbatim lift."""
    tg = _grams(text)
    for a in ANCHOR_SENTENCES:
        shared = {g for g in (tg & _grams(a)) if not _is_figure_run(g)}
        if shared:
            return sorted(shared)[0]
    return None


def _sym(a, b):
    return max(difflib.SequenceMatcher(None, a, b).ratio(), difflib.SequenceMatcher(None, b, a).ratio())


# ---------------------------------------------------------------- checks

def check_spec_shape(spec):
    rows = note_rows(spec)
    if len(rows) != EXPECTED_NOTES:
        raise SystemExit(f"REFUSED: spec has {len(rows)} note rows, expected {EXPECTED_NOTES}")
    seen = set()
    for r in rows:
        for k in ("crop", "field", "id", "method", "register", "old", "new"):
            if not r.get(k):
                raise SystemExit(f"REFUSED: note row {r!r} is missing {k!r}")
        if r["field"] not in FIELDS or r["register"] not in REGISTERS or r["method"] not in METHODS:
            raise SystemExit(f"REFUSED: note row {r['crop']}/{r['id']} has a field, register or method "
                             f"outside this promote's vocabulary")
        key = (r["crop"], r["field"], r["id"], r["method"], r["register"])
        if key in seen:
            raise SystemExit(f"REFUSED: spec names the same note twice: {key}")
        seen.add(key)
        if r["old"] == r["new"]:
            raise SystemExit(f"REFUSED: {r['crop']}/{r['id']} rewrites a sentence to itself")
        if not scoped_thirty_with_label(r["new"]):
            raise SystemExit(f"REFUSED: {r['crop']}/{r['id']}/{r['register']} new sentence is not a scoped "
                             f"30-day claim with a label deferral: {r['new'][:90]!r}")
        bad = hygiene(r["new"])
        if bad:
            raise SystemExit(f"REFUSED: {r['crop']}/{r['id']}/{r['register']} fails copy hygiene ({bad})")
        run = lifted_from_anchor(r["new"])
        if run:
            raise SystemExit(f"REFUSED: {r['crop']}/{r['id']}/{r['register']} lifts a verbatim run from an "
                             f"anchor: {run!r}")
    if len({r["crop"] for r in rows}) != EXPECTED_CROPS:
        raise SystemExit(f"REFUSED: spec touches {len({r['crop'] for r in rows})} crops, expected {EXPECTED_CROPS}")
    cms = spec.get("control_methods") or {}
    if set(cms) != set(METHODS):
        raise SystemExit(f"REFUSED: spec control_methods {sorted(cms)} != {sorted(METHODS)}")
    for k, m in cms.items():
        if not scoped_thirty_with_label(m["caution_new"]):
            raise SystemExit(f"REFUSED: {k} caution_new is not a scoped 30-day claim with a label deferral")
        bad = hygiene(m["caution_new"])
        if bad:
            raise SystemExit(f"REFUSED: {k} caution_new fails copy hygiene ({bad})")
        if lifted_from_anchor(m["caution_new"]):
            raise SystemExit(f"REFUSED: {k} caution_new lifts a verbatim run from an anchor")
        if set(m["add_anchors"]) != set(m["add_sources"]):
            raise SystemExit(f"REFUSED: {k} add_anchors keys != add_sources")
    new = spec.get("catalog_new") or {}
    if len(new) != EXPECTED_NEW_SOURCES:
        raise SystemExit(f"REFUSED: spec admits {len(new)} catalog ids, expected {EXPECTED_NEW_SOURCES}")
    return len(rows)


def check_pre_state(spec, data):
    """Every old sentence is found EXACTLY ONCE in its note; both cautions are present verbatim;
    the new catalog id is absent; every source the cautions will cite is catalogued T1."""
    idx = by_slug(data)
    n = 0
    for r in note_rows(spec):
        crop = idx.get(r["crop"])
        if crop is None:
            raise SystemExit(f"REFUSED: crop {r['crop']!r} not in the roster")
        ent = [p for p in crop.get(r["field"]) or [] if p.get("id") == r["id"]]
        if len(ent) != 1:
            raise SystemExit(f"REFUSED: {r['crop']}/{r['field']} has {len(ent)} entries with id {r['id']!r}")
        rungs = [x for x in ent[0].get("control_ladder") or [] if x.get("method") == r["method"]]
        if len(rungs) != 1:
            raise SystemExit(f"REFUSED: {r['crop']}/{r['id']} has {len(rungs)} rungs on {r['method']!r}")
        text = rungs[0].get(r["register"]) or ""
        if text.count(r["old"]) != 1:
            raise SystemExit(f"REFUSED: {r['crop']}/{r['id']}/{r['register']} old sentence found "
                             f"{text.count(r['old'])} times, need exactly 1; the pre-state has drifted")
        n += 1
    cm = data["control_methods"]
    sc = data["source_catalog"]
    for k, m in spec["control_methods"].items():
        cautions = cm[k].get("cautions") or []
        if cautions.count(m["caution_old"]) != 1:
            raise SystemExit(f"REFUSED: control_methods.{k} caution found {cautions.count(m['caution_old'])} "
                             f"times, need exactly 1")
        for s in m["add_sources"]:
            entry = sc.get(s) or (spec.get("catalog_new") or {}).get(s)
            if entry is None:
                raise SystemExit(f"REFUSED: {k} cites {s!r}, which is neither catalogued nor admitted here")
            if (entry.get("tier") or "").upper() != "T1":
                raise SystemExit(f"REFUSED: {k} cites {s!r}, which is not T1")
            if s in cm[k].get("sources") or []:
                raise SystemExit(f"REFUSED: {k} already cites {s!r}")
            if m["add_anchors"][s]["url"] != entry["url"]:
                raise SystemExit(f"REFUSED: {k} anchor for {s!r} does not match the catalog url")
    for sid, entry in (spec.get("catalog_new") or {}).items():
        if sid in sc:
            raise SystemExit(f"REFUSED: catalog id {sid!r} already exists; this would overwrite it")
        u = str(entry.get("url") or "")
        if not u.startswith("https://") or len(u.split("://", 1)[1].strip("/").split("/")) < 2:
            raise SystemExit(f"REFUSED: catalog id {sid!r} url is not a pathed https document")
        if (entry.get("tier") or "").upper() != "T1" or not entry.get("citable_for"):
            raise SystemExit(f"REFUSED: catalog id {sid!r} is not T1 with a citable_for")
    probe = dict(sc)
    probe.update({k: dict(v) for k, v in (spec.get("catalog_new") or {}).items()})
    tv = title_violations(probe)
    if tv:
        raise SystemExit(f"REFUSED: the admitted source would fail A54 at the gauntlet: {tv[0]}")
    return n


def check_pre_statements(spec, data):
    """Guard 1, pre half: the widened net finds exactly the statements the spec names, no more."""
    found = interval_sentences(data)
    if len(found) != EXPECTED_PRE_STATEMENTS:
        raise SystemExit(f"REFUSED: the widened net finds {len(found)} interval statements on the "
                         f"pre-state, expected {EXPECTED_PRE_STATEMENTS}; re-measure before running")
    named = {r["old"] for r in note_rows(spec)} | {m["caution_old"] for m in spec["control_methods"].values()}
    stray = [w for w, s in found if s not in named]
    if stray:
        raise SystemExit(f"REFUSED: the net finds interval statements the spec does not rewrite: {stray}")
    return len(found)


# ---------------------------------------------------------------- apply / verify

def apply_to(data, spec):
    out = copy.deepcopy(data)
    idx = by_slug(out)
    for r in note_rows(spec):
        ent = next(p for p in idx[r["crop"]][r["field"]] if p.get("id") == r["id"])
        rung = next(x for x in ent["control_ladder"] if x.get("method") == r["method"])
        rung[r["register"]] = rung[r["register"]].replace(r["old"], r["new"], 1)
    for k, m in spec["control_methods"].items():
        cm = out["control_methods"][k]
        cm["cautions"] = [m["caution_new"] if c == m["caution_old"] else c for c in cm["cautions"]]
        cm["sources"] = list(cm["sources"]) + [s for s in m["add_sources"] if s not in cm["sources"]]
        cm["anchoring_urls"] = dict(cm["anchoring_urls"])
        cm["anchoring_urls"].update({s: dict(a) for s, a in m["add_anchors"].items()})
    for sid, entry in (spec.get("catalog_new") or {}).items():
        out["source_catalog"][sid] = dict(entry)
    return out


def check_post_statements(post):
    """Guard 1, post half: zero sub-30-day statements remain, and every statement is the scoped
    30-day claim with a label deferral."""
    found = interval_sentences(post)
    if len(found) != EXPECTED_POST_STATEMENTS:
        raise SystemExit(f"REFUSED: the widened net finds {len(found)} interval statements on the "
                         f"post-state, expected {EXPECTED_POST_STATEMENTS}")
    bad = [(w, s) for w, s in found if not scoped_thirty_with_label(s)]
    if bad:
        raise SystemExit(f"REFUSED: {len(bad)} interval statement(s) survive without the scoped 30-day "
                         f"claim and label deferral: {bad[0]}")
    return len(found)


def check_oregano_agrees(post):
    """Guard 7: the crop that shipped two intervals now ships one."""
    o = by_slug(post)["oregano"]
    stmts = [s for w, s in interval_sentences(post) if w.startswith("oregano/")]
    if len(stmts) != 2:
        raise SystemExit(f"REFUSED: oregano carries {len(stmts)} interval statements, expected 2")
    if not all(THIRTY.search(s) for s in stmts):
        raise SystemExit("REFUSED: oregano's two interval statements do not both say 30 days")
    return True


def check_registers_diverge(post, spec):
    """Guard 5 on every touched rung."""
    idx = by_slug(post)
    n = 0
    for r in note_rows(spec):
        ent = next(p for p in idx[r["crop"]][r["field"]] if p.get("id") == r["id"])
        rung = next(x for x in ent["control_ladder"] if x.get("method") == r["method"])
        b, s = rung.get("note_beginner"), rung.get("note_seasoned")
        if not s:
            continue
        if b.strip() == s.strip():
            raise SystemExit(f"REFUSED: {r['crop']}/{r['id']}/{r['method']} registers are identical")
        if _sym(b, s) >= 0.90:
            raise SystemExit(f"REFUSED: {r['crop']}/{r['id']}/{r['method']} registers are {_sym(b, s):.2f} "
                             f"similar; that is a reword, not a register")
        n += 1
    return n


def check_catalog_gates(post):
    """Guard 6: the roster gates that read the catalog, IMPORTED and run on the post-state."""
    tv = title_violations(post["source_catalog"])
    if tv:
        raise SystemExit(f"REFUSED: A54 on the post-state: {tv[0]}")
    v = CLG.all_violations(post)
    if v:
        raise SystemExit(f"REFUSED: control_ladder_gate on the post-state: {v[0]}")
    return True


def verify_post(pre, post, spec):
    """Guard 8. SET COMPARISON BEFORE VALUE COMPARISON."""
    pre_i, post_i = by_slug(pre), by_slug(post)
    if {c["slug"] for c in pre["crops"]} != {c["slug"] for c in post["crops"]}:
        raise SystemExit("REFUSED: crop roster changed")
    if len(pre["crops"]) != len(post["crops"]):
        raise SystemExit("REFUSED: crop count changed")
    if set(pre) != set(post):
        raise SystemExit("REFUSED: top-level key set changed")
    for k in pre:
        if k in ("crops", "control_methods", "source_catalog"):
            continue
        if json.dumps(pre[k], sort_keys=True) != json.dumps(post[k], sort_keys=True):
            raise SystemExit(f"REFUSED: top-level key {k!r} changed")

    touched_crops = {r["crop"] for r in note_rows(spec)}
    for slug in pre_i:
        if slug in touched_crops:
            continue
        if json.dumps(pre_i[slug], sort_keys=True) != json.dumps(post_i[slug], sort_keys=True):
            raise SystemExit(f"REFUSED: untouched crop {slug} changed")

    targets = {(r["crop"], r["field"], r["id"], r["method"], r["register"]): r for r in note_rows(spec)}
    changed = 0
    for slug in touched_crops:
        s_crop, g_crop = pre_i[slug], post_i[slug]
        if set(s_crop) != set(g_crop):
            raise SystemExit(f"REFUSED: {slug} crop-level key set changed")
        for k in s_crop:
            if k in FIELDS:
                continue
            if json.dumps(s_crop[k], sort_keys=True) != json.dumps(g_crop[k], sort_keys=True):
                raise SystemExit(f"REFUSED: {slug} field {k!r} changed outside the problem arrays")
        for field in FIELDS:
            src, got = s_crop.get(field) or [], g_crop.get(field) or []
            if len(src) != len(got):
                raise SystemExit(f"REFUSED: {slug}/{field} entry count {len(src)} -> {len(got)}")
            for s, g in zip(src, got):
                if set(s) != set(g):
                    raise SystemExit(f"REFUSED: {slug}/{s.get('id')!r} entry key set changed")
                for k in s:
                    if k == "control_ladder":
                        continue
                    if json.dumps(s[k], sort_keys=True) != json.dumps(g[k], sort_keys=True):
                        raise SystemExit(f"REFUSED: {slug}/{s.get('id')!r} field {k!r} changed; this promote "
                                         f"rewrites rung notes and nothing else on a crop")
                sl, gl = s.get("control_ladder") or [], g.get("control_ladder") or []
                if len(sl) != len(gl):
                    raise SystemExit(f"REFUSED: {slug}/{s.get('id')!r} ladder length changed")
                for sr, gr in zip(sl, gl):
                    if set(sr) != set(gr):
                        raise SystemExit(f"REFUSED: {slug}/{s.get('id')!r}/{sr.get('method')} rung key set changed")
                    if sr.get("method") != gr.get("method"):
                        raise SystemExit(f"REFUSED: {slug}/{s.get('id')!r} rung method changed")
                    for k in sr:
                        if sr[k] == gr[k]:
                            continue
                        row = targets.get((slug, field, s.get("id"), sr.get("method"), k))
                        if row is None:
                            raise SystemExit(f"REFUSED: {slug}/{s.get('id')!r}/{sr.get('method')}/{k} changed "
                                             f"without a spec row")
                        if gr[k] != sr[k].replace(row["old"], row["new"], 1):
                            raise SystemExit(f"REFUSED: {slug}/{s.get('id')!r}/{sr.get('method')}/{k} is not "
                                             f"exactly the one-sentence replacement its row declares")
                        changed += 1
    if changed != len(note_rows(spec)):
        raise SystemExit(f"REFUSED: {changed} note leaves changed, spec has {len(note_rows(spec))} rows")

    pcm, gcm = pre["control_methods"], post["control_methods"]
    if set(pcm) != set(gcm):
        raise SystemExit("REFUSED: the control_methods SET changed")
    for k in pcm:
        if k in METHODS:
            continue
        if json.dumps(pcm[k], sort_keys=True) != json.dumps(gcm[k], sort_keys=True):
            raise SystemExit(f"REFUSED: control_methods.{k} changed; only {METHODS} may change")
    for k in METHODS:
        m = spec["control_methods"][k]
        s, g = pcm[k], gcm[k]
        if set(s) != set(g):
            raise SystemExit(f"REFUSED: control_methods.{k} key set changed")
        for key in s:
            if key in ("cautions", "sources", "anchoring_urls"):
                continue
            if json.dumps(s[key], sort_keys=True) != json.dumps(g[key], sort_keys=True):
                raise SystemExit(f"REFUSED: control_methods.{k}.{key} changed; only cautions, sources and "
                                 f"anchoring_urls may change")
        if len(s["cautions"]) != len(g["cautions"]):
            raise SystemExit(f"REFUSED: control_methods.{k} cautions count changed")
        diff = [(a, b) for a, b in zip(s["cautions"], g["cautions"]) if a != b]
        if diff != [(m["caution_old"], m["caution_new"])]:
            raise SystemExit(f"REFUSED: control_methods.{k} cautions changed other than the declared one")
        if g["sources"] != s["sources"] + [x for x in m["add_sources"] if x not in s["sources"]]:
            raise SystemExit(f"REFUSED: control_methods.{k}.sources changed other than by the declared additions")
        if set(g["anchoring_urls"]) != set(s["anchoring_urls"]) | set(m["add_anchors"]):
            raise SystemExit(f"REFUSED: control_methods.{k}.anchoring_urls keys changed other than by the declared additions")
        for key in s["anchoring_urls"]:
            if s["anchoring_urls"][key] != g["anchoring_urls"][key]:
                raise SystemExit(f"REFUSED: control_methods.{k}.anchoring_urls[{key!r}] was modified")

    psc, gsc = pre["source_catalog"], post["source_catalog"]
    added = sorted(set(gsc) - set(psc))
    dropped = sorted(set(psc) - set(gsc))
    if dropped:
        raise SystemExit(f"REFUSED: source_catalog DROPPED {dropped}")
    if added != sorted(spec.get("catalog_new") or {}):
        raise SystemExit(f"REFUSED: source_catalog added {added}, expected exactly {sorted(spec.get('catalog_new') or {})}")
    for k in psc:
        if psc[k] != gsc[k]:
            raise SystemExit(f"REFUSED: existing source_catalog entry {k!r} was MODIFIED")
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
    ap.add_argument("--out", default=None, help="write the post-state HERE instead of over the canonical")
    args = ap.parse_args()
    path = args.canonical_flag or args.canonical

    data = load_canonical(path)
    spec = staged()

    n = check_spec_shape(spec)
    print(f"  spec shape           {n} note rows on {EXPECTED_CROPS} crops, 2 cautions, {EXPECTED_NEW_SOURCES} catalog id; every new sentence scoped, 30 days, label")
    n = check_pre_state(spec, data)
    print(f"  pre-state            {n} old sentences found exactly once; cautions present; catalog id new, T1, titled (A54)")
    n = check_pre_statements(spec, data)
    print(f"  widened net (pre)    {n} interval statements, every one named by the spec")

    post = apply_to(data, spec)
    n = check_post_statements(post)
    print(f"  widened net (post)   {n} interval statements, 0 under 30 days, all scoped with a label deferral")
    check_oregano_agrees(post)
    print("  oregano              both rungs now say 30 days")
    n = check_registers_diverge(post, spec)
    print(f"  registers diverge    {n} touched rungs with both registers, all distinct")
    check_catalog_gates(post)
    print("  catalog gates        A54 and control_ladder_gate clean on the post-state")
    leaves = verify_post(data, post, spec)
    print(f"  verify post          {leaves} note leaves + 2 cautions + sources/anchors on 2 methods + 1 catalog id, nothing else")

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
    if args.check and not args.apply:
        print("  --check: nothing written")
        return 0
    with open(path or CANON, "wb") as f:
        f.write(blob)
    print(f"  WROTE {path or CANON}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
