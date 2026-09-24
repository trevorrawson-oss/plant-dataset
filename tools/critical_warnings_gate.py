#!/usr/bin/env python3
"""critical_warnings_gate -- A61: per-crop `critical_warnings` and the top-level `container_safety`
(PLA-581 spec docs/superpowers/specs/2026-09-21-pla581-critical-warnings-field-shape.md, section 7;
register row 32).

TWO FIELDS, ONE ENTRY SHAPE (spec rule 10). Both carry entries of exactly

    {id, class, severity, stage, title, body_seasoned, body_beginner, sources, anchoring_urls}

and ONE validator (`entry_violations`) checks both, so the two cannot drift apart.

1. `critical_warnings` -- a top-level key ON EACH CROP. THREE DOCUMENTED STATES (spec 5.2, ruling 2):
     null    NOT ASSESSED. No pass has asked whether this crop has a critical warning. What the
             PLA-581 promote writes on all 121 certified crops.
     []      ASSESSED, NONE FOUND. PLA-142 earns this per crop as its harvest pass reaches it.
     [...]   authored entries.
   Key ABSENT is the uncertified-shell exemption, not a fourth state.

   `[]` IS A CLAIM, and this gate requires a record behind it. A `[]` or a non-empty list on a
   certified crop must be backed by a verification_status.field_additions[] entry with
   field == "critical_warnings" (the amend-not-recert pattern A40 / A59 / A60 use). This is what
   stops null -> [] from passing silently: the `not (x or [])` idiom the PLA-533 ratchet uses ON
   PURPOSE collapses the two, and here it would make every crop read "assessed, none found" while
   staying green. `state_of` keeps all five readings apart and nothing in this module coerces one
   state into another. (This goes one step past spec 7.1 rule 1, which left the meanings to the
   register row; recorded at the PLA-581 hold.)

2. `container_safety` -- a top-level key OF THE DATASET, a sibling of source_catalog (ruling 1 / D1):
   {warnings: [entry, ...], field_additions: [record, ...]}. The crop-invariant container warnings,
   authored once, rendered by the consumers on every container_ok crop. Its entries are the same
   shape with three tightenings: `class` must be "safety"; `stage` must be null (there is no crop
   and so no ladder, and "a pot is heavy whenever it is full"); `id` is snake_case, because the
   spec pinned the names balcony_load / container_material / hanging_security and a join key is
   pinned at first naming. Its provenance lives BESIDE it, one record per warning, field ==
   "container_safety.<id>", because there is no crop record to hang it on.

   NO FIGURES. No rendered sentence may state a weight, a load or a pot count that no source named
   (spec 8.4). Measured across 16 extension fetches, no T1 source publishes a potting-mix weight or
   a pounds-per-pot load: the balcony warning is a REFERRAL to an architect. So container_safety copy
   carries no digit and no spelled number (a bare unit word states no figure, and the approved copy
   needs one to say that none exists). This is the dataset-side form of
   that consumer rule, and it stands in for numeric_sanity bounds: neither field has a numeric leaf.

SPEC RULE 9 IS SUBSUMED, NOT SHIPPED. "A class: safety entry with an empty sources is a violation"
cannot fire first: rule 8 requires non-empty sources on EVERY entry. An unreachable guard reads as
coverage, so the suite carries a driver proving rule 8 catches the sourceless safety entry instead.

`title` NEEDS NO register_completeness RULING, contrary to spec 7.2: it is already ruled globally as
USER-FACING-CATEGORICAL (EXCLUDED_KEYS, C11 ruling 2026-06-27). `class` was the one unruled string
key and is ruled path-scoped there.

WHERE EACH HALF IS ENFORCED. whole_crop_gate A61 runs both halves on every crop's run, so the
pre-commit hook and release_verify (which run whole_crop_gate, not gate_all) see container_safety
too. SHAPE fires only when a key is present, so it arms GREEN on 526788f2 (neither key exists).
PRESENCE (every certified crop carries critical_warnings; the dataset carries container_safety) is a
SEPARATE entry point behind A61_PRESENCE_ARMED, flipped only in the commit that writes canonical.
gate_all iterates CERTIFIED crops only, so a key on an uncertified shell is invisible to it by
construction (true of A58-A60 too): `whole_crop_gate <shell>`, this module's CLI and the promote's
check_post walk all 128 and refuse it. Do not read a green gate_all as covering the shells.

Usage: critical_warnings_gate.py [PATH] [--presence]
"""
import json
import re
import sys

FIELD = "critical_warnings"
DATASET_KEY = "container_safety"
CERTIFIED = "verified_gs_arc"
ENTRY_KEYS = ("id", "class", "severity", "stage", "title", "body_seasoned", "body_beginner",
              "sources", "anchoring_urls")
PROSE_KEYS = ("title", "body_seasoned", "body_beginner")
CLASSES = ("safety", "harvest")
SEVERITIES = ("critical", "high")
ANCHOR_KEYS = ("url", "verified")
RECORD_KEYS = ("field", "date", "sources", "note")
PROVENANCE_FIELD = "critical_warnings"
CS_PROVENANCE_PREFIX = "container_safety."
CS_KEYS = ("warnings", "field_additions")
KEBAB = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
SNAKE = re.compile(r"[a-z0-9]+(_[a-z0-9]+)*")
_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
_SHA = re.compile(r"\b[0-9a-f]{64}\b")
# A figure is a NUMBER, in either costume: a digit or a spelled number. A unit word alone states no
# figure, and the approved balcony copy NEEDS one to say so ("No extension source publishes a pounds
# figure for this"); a first draft that also refused bare units refused that approved sentence, so
# units are deliberately NOT matched. A number with a unit is caught by the number.
# Spelled numbers are the RULED list (Trevor, 2026-09-23): one through twenty, thirty through ninety,
# half, dozen, hundred, thousand. Five groups, so each is a separate mutation with its own driver.
_SMALL = "one|two|three|four|five|six|seven|eight|nine|ten"
_TEENS = "eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty"
_TENS = "thirty|forty|fifty|sixty|seventy|eighty|ninety"
_HALF = "half"
_LARGE = "dozen|hundred|thousand"
_FIGURE = re.compile(r"\d|\b(" + "|".join((_SMALL, _TEENS, _TENS, _HALF, _LARGE)) + r")\b", re.I)


def _certified(crop):
    return (crop.get("verification_status") or {}).get("status") == CERTIFIED


def ladder_ids(crop):
    """The ids in THIS crop's own growth_stages. `stage` is gated against these (spec 6.2): there
    are 81 distinct ids roster-wide and no closed vocabulary, so a global list would both admit a
    stage the crop does not have and be wrong about what exists."""
    return [s["id"] for s in (crop.get("growth_stages") or [])
            if isinstance(s, dict) and isinstance(s.get("id"), str)]


def state_of(crop):
    """absent | null | empty | authored | invalid. NEVER coerces one reading into another."""
    if FIELD not in crop:
        return "absent"
    v = crop[FIELD]
    if v is None:
        return "null"
    if isinstance(v, list):
        return "empty" if len(v) == 0 else "authored"
    return "invalid"


def _has_record(crop):
    fa = (crop.get("verification_status") or {}).get("field_additions") or []
    return any(isinstance(x, dict) and x.get("field") == PROVENANCE_FIELD for x in fa)


def entry_violations(e, tag, catalog, ladder, id_re, id_form):
    """Rules 2-8 on ONE entry. Shared by both fields (rule 10)."""
    V = []
    if not isinstance(e, dict) or set(e) != set(ENTRY_KEYS):
        got = sorted(e) if isinstance(e, dict) else type(e).__name__
        return [f"{tag}: keys must be exactly {sorted(ENTRY_KEYS)}, got {got}"]
    if not (isinstance(e["id"], str) and id_re.fullmatch(e["id"])):
        V.append(f"{tag}: id must be {id_form}, got {e['id']!r}")
    if e["class"] not in CLASSES:
        V.append(f"{tag}: class must be one of {list(CLASSES)}, got {e['class']!r}")
    if e["severity"] not in SEVERITIES:
        V.append(f"{tag}: severity must be one of {list(SEVERITIES)} (MODELED, never sourced), "
                 f"got {e['severity']!r}")
    if e["stage"] is not None and not (isinstance(e["stage"], str) and e["stage"] in ladder):
        V.append(f"{tag}: stage {e['stage']!r} is not a stage in this crop's own growth_stages "
                 f"(null, or an id on the ladder)")
    for k in PROSE_KEYS:
        s = e[k]
        if not (isinstance(s, str) and s.strip()):
            V.append(f"{tag}: {k} must be a non-empty string, got {s!r}")
            continue
        if "—" in s or "–" in s:
            V.append(f"{tag}: {k} carries an em or en dash")
        if "--" in s:
            V.append(f"{tag}: {k} carries '--' in consumer copy")
    srcs = e["sources"]
    if not (isinstance(srcs, list) and srcs and all(isinstance(s, str) and s for s in srcs)):
        V.append(f"{tag}: sources must be a non-empty list of source keys, got {srcs!r}")
        srcs = []
    for s in srcs:
        cat = catalog.get(s)
        if not isinstance(cat, dict):
            V.append(f"{tag}: source {s!r} is not in source_catalog")
        elif cat.get("tier") != "T1":
            V.append(f"{tag}: source {s!r} is {cat.get('tier')!r}, not T1")
    au = e["anchoring_urls"]
    if not isinstance(au, dict):
        V.append(f"{tag}: anchoring_urls must be an object keyed by source, got {au!r}")
        return V
    for s in srcs:
        a = au.get(s)
        if not isinstance(a, dict):
            V.append(f"{tag}: source {s!r} has no anchoring_urls entry")
            continue
        if set(a) != set(ANCHOR_KEYS):
            V.append(f"{tag}: anchoring_urls[{s!r}] keys must be exactly {sorted(ANCHOR_KEYS)}, "
                     f"got {sorted(a)}")
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
    return V


def _dup_ids(entries, where):
    seen, V = set(), []
    for e in entries:
        i = e.get("id") if isinstance(e, dict) else None
        if i is None:
            continue
        if i in seen:
            V.append(f"{where}: id {i!r} appears twice; an id is a join key and unique")
        seen.add(i)
    return V


# ---------------------------------------------------------------------------------------------
# critical_warnings, per crop
# ---------------------------------------------------------------------------------------------

def shape_violations(crop, catalog):
    slug = crop.get("slug") or "?"
    st = state_of(crop)
    if st == "absent":
        return []
    if not _certified(crop):
        return [f"{slug}: {FIELD} present on an uncertified crop; the shells carry no key "
                f"(that is how A39 exempts them by status)"]
    if st == "invalid":
        return [f"{slug}: {FIELD} must be null, [] or a non-empty list, got "
                f"{json.dumps(crop[FIELD], ensure_ascii=False)[:120]}"]
    if st == "null":
        return []
    V = []
    if not _has_record(crop):
        if st == "empty":
            V.append(f"{slug}: {FIELD} is [] (assessed, none found) with no field_additions entry "
                     f"for {PROVENANCE_FIELD!r}; an assessment nobody recorded is not one -- "
                     f"unassessed is spelled null")
        else:
            V.append(f"{slug}: authored {FIELD} on a certified crop with no field_additions entry "
                     f"for {PROVENANCE_FIELD!r}")
    entries = crop[FIELD]
    ladder = set(ladder_ids(crop))
    for i, e in enumerate(entries):
        V += entry_violations(e, f"{slug}/{FIELD}[{i}]", catalog, ladder, KEBAB, "kebab-case")
    V += _dup_ids(entries, f"{slug}/{FIELD}")
    return V


def presence_violations(crop):
    if not _certified(crop):
        return []
    if FIELD not in crop:
        return [f"{crop.get('slug') or '?'}: {FIELD} missing (null = not assessed is a value; "
                f"a certified crop carries the key)"]
    return []


# ---------------------------------------------------------------------------------------------
# container_safety, once per dataset
# ---------------------------------------------------------------------------------------------

def dataset_violations(data, presence=False):
    catalog = data.get("source_catalog") or {}
    if DATASET_KEY not in data:
        return ([f"{DATASET_KEY} missing from the dataset (the crop-invariant container warnings "
                 f"live here once, rendered on every container_ok crop)"] if presence else [])
    v = data[DATASET_KEY]
    if not isinstance(v, dict) or set(v) != set(CS_KEYS):
        got = sorted(v) if isinstance(v, dict) else v
        return [f"{DATASET_KEY} must be an object with exactly {list(CS_KEYS)}, got {got!r}"]
    ws, fas = v["warnings"], v["field_additions"]
    if not isinstance(ws, list) or not ws:
        return [f"{DATASET_KEY}.warnings must be a non-empty list"]
    V = []
    for i, e in enumerate(ws):
        tag = f"{DATASET_KEY}.warnings[{i}]"
        V += entry_violations(e, tag, catalog, set(), SNAKE, "snake_case")
        if not isinstance(e, dict):
            continue
        if "class" in e and e["class"] != "safety":
            V.append(f"{tag}: class must be 'safety' in {DATASET_KEY}, got {e['class']!r}")
        for k in PROSE_KEYS:
            s = e.get(k)
            if isinstance(s, str):
                m = _FIGURE.search(s)
                if m:
                    V.append(f"{tag}: {k} states a figure ({m.group(0)!r}); no source publishes a "
                             f"weight, load or count for this warning, so the copy carries none")
    V += _dup_ids(ws, f"{DATASET_KEY}.warnings")

    # PROVENANCE, one record per warning. SET BEFORE VALUE: compare the record set to the warning
    # set first, so an extra record cannot hide behind a loop over the warnings.
    if not isinstance(fas, list) or not all(isinstance(r, dict) for r in fas):
        return V + [f"{DATASET_KEY}.field_additions must be a list of records"]
    want = {CS_PROVENANCE_PREFIX + e["id"] for e in ws if isinstance(e, dict) and isinstance(e.get("id"), str)}
    got = [r.get("field") for r in fas]
    if len(got) != len(ws) or set(got) != want:
        V.append(f"{DATASET_KEY}: needs exactly one field_additions record per warning "
                 f"({sorted(want)}), got {got}")
        return V
    by_field = {r["field"]: r for r in fas}
    for e in ws:
        r = by_field[CS_PROVENANCE_PREFIX + e["id"]]
        tag = f"{DATASET_KEY}.field_additions[{r['field']}]"
        if set(r) != set(RECORD_KEYS):
            V.append(f"{tag}: record keys must be exactly {sorted(RECORD_KEYS)}, got {sorted(r)}")
            continue
        if not (isinstance(r["date"], str) and _DATE.fullmatch(r["date"])):
            V.append(f"{tag}: date is not a YYYY-MM-DD date: {r['date']!r}")
        if sorted(r["sources"] or []) != sorted(e["sources"] or []):
            V.append(f"{tag}: record credits {r['sources']} but the warning cites {e['sources']}")
        note = r["note"] if isinstance(r["note"], str) else ""
        for s in e["sources"] or []:
            u = ((e["anchoring_urls"] or {}).get(s) or {}).get("url")
            if u and u not in note:
                V.append(f"{tag}: record does not name the url its warning anchors ({u})")
        if not _SHA.search(note):
            V.append(f"{tag}: record quotes no sha256 of the page it was written from")
        if "verbatim:" not in note:
            V.append(f"{tag}: record quotes no source text (verbatim:)")
        if "—" in note or "–" in note:
            V.append(f"{tag}: record carries an em or en dash")
    return V


# ---------------------------------------------------------------------------------------------
# whole dataset
# ---------------------------------------------------------------------------------------------

def all_violations(data, presence=False):
    catalog = data.get("source_catalog") or {}
    V = list(dataset_violations(data, presence=presence))
    for c in data.get("crops", []):
        V += shape_violations(c, catalog)
        if presence:
            V += presence_violations(c)
    return V


def population(data):
    """What was INSPECTED, by state, so a green run can never be read off an empty population."""
    cert = [c for c in data.get("crops", []) if _certified(c)]
    states = [state_of(c) for c in cert]
    cs = data.get(DATASET_KEY)
    return {
        "certified": len(cert),
        "null": states.count("null"), "empty": states.count("empty"),
        "authored": states.count("authored"), "invalid": states.count("invalid"),
        "absent_certified": states.count("absent"),
        "entries": sum(len(c[FIELD]) for c in cert if state_of(c) == "authored"),
        "shells_carrying": sum(1 for c in data.get("crops", []) if not _certified(c) and FIELD in c),
        "container_safety_warnings": (len(cs["warnings"]) if isinstance(cs, dict)
                                      and isinstance(cs.get("warnings"), list) else None),
    }


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    path = args[0] if args else "crops_data_final.json"
    presence = "--presence" in argv
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    V = all_violations(data, presence=presence)
    for v in V:
        print("VIOLATION:", v)
    p = population(data)
    print(f"critical_warnings_gate: {len(V)} violation(s); inspected {len(data.get('crops', []))} crops "
          f"({p['certified']} certified): {p['null']} null (not assessed), {p['empty']} [] (assessed, "
          f"none found), {p['authored']} authored carrying {p['entries']} entries, "
          f"{p['absent_certified']} certified without the key, {p['shells_carrying']} shells carrying it; "
          f"{DATASET_KEY}: "
          f"{'absent' if p['container_safety_warnings'] is None else str(p['container_safety_warnings']) + ' warnings'}; "
          f"presence {'ARMED' if presence else 'off'}")
    if presence and p["certified"] == 0:
        print("critical_warnings_gate: REFUSED -- inspected 0 certified crops")
        return 2
    return 1 if V else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
