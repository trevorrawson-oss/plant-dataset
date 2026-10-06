"""glossary_sense -- PLA-673's sense guard: which glossary term (if any) each hill-word in a consumer leaf belongs to.

Reads the glossary `match` lists (the staged tools/staging/pla673_674_prep/glossary_match.json, in the ruled entry shape,
or the dataset glossary itself via build_spec) and classifies every
occurrence of hill / hills / hilled / hilling in every consumer-facing string leaf of every crop:

  1. an `exclusion` whose pattern covers the occurrence (and whose `crops`, if given, holds the crop) tags it `none`;
  2. otherwise the ONE term whose `crops` holds the crop tags it, provided the occurrence's form is one of the term's
     `forms` and none of the term's `refuse_on` patterns matches the occurrence's sentence;
  3. otherwise it is UNCLASSIFIED.

`classify_dataset` REFUSES on any UNCLASSIFIED occurrence and on an inspected population below its floor, so new text
on an unscoped crop, a planting-sense "hill" on a hilling crop, or a hilling verb on a hill crop fails loud instead of
silently taking (or silently losing) a gloss. Read-only: it never writes the dataset.

Consumer leaf: a crop string leaf not under `verification_status`, not under any `sources` / `*_sources` /
`anchoring_urls` / `*_anchoring_urls` / `*provenance` key, and not a structural key (STRUCTURAL).
"""
import json, re
from collections import namedtuple

STRUCTURAL = frozenset({"id", "stage_id", "tip_id", "arrangement", "action", "active_stages"})
DEFAULT_FLOOR = 200  # the live population is 232 (350eda38); a run inspecting fewer refuses


class Refused(Exception):
    pass


Match = namedtuple("Match", "form start end term exclusion noun")
Row = namedtuple("Row", "crop path text matches term_ids")


class Result:
    def __init__(self, rows, unclassified, inspected):
        self.rows, self.unclassified, self.inspected = rows, unclassified, inspected


MATCHER_KEYS = frozenset({"sense", "forms", "crops", "refuse_on", "exclusions"})


def load_spec(path):
    return build_spec(json.load(open(path, encoding="utf-8")))


def build_spec(glossary):
    """The guard's working spec from glossary-shaped entries: {term_id: {..., "match": [matcher]}} (the staged file,
    or the dataset's own `glossary`). Keys starting with `_` are notes. Each `match` holds exactly one matcher with
    exactly MATCHER_KEYS; every term carries the IDENTICAL exclusion list, or the spec refuses (exclusions are applied
    before any term, so they must not depend on which entry is read). The word pattern is the union of the forms."""
    terms, exclusions = {}, None
    for tid, entry in glossary.items():
        if tid.startswith("_"):
            continue
        m = entry.get("match")
        if not isinstance(m, list) or len(m) != 1 or set(m[0]) != MATCHER_KEYS:
            raise Refused(f"glossary.{tid}.match must be one matcher with keys {sorted(MATCHER_KEYS)}")
        if exclusions is None:
            exclusions = m[0]["exclusions"]
        elif m[0]["exclusions"] != exclusions:
            raise Refused(f"glossary.{tid}: exclusions differ from the other terms'")
        terms[tid] = {k: v for k, v in m[0].items() if k != "exclusions"}
    forms = sorted({f for t in terms.values() for f in t["forms"]}, key=len, reverse=True)
    spec = {"terms": terms, "exclusions": [dict(e) for e in exclusions or []],
            "_word": re.compile(r"\b(" + "|".join(map(re.escape, forms)) + r")\b", re.I)}
    for t in spec["terms"].values():
        t["_refuse"] = [re.compile(p, re.I) for p in t.get("refuse_on", [])]
    for e in spec["exclusions"]:
        e["_rx"] = re.compile(e["pattern"], re.I)
    owners = {}
    for tid, t in spec["terms"].items():
        for c in t["crops"]:
            if c in owners:
                raise Refused(f"crop {c} is in the scope of both {owners[c]} and {tid}")
            owners[c] = tid
    spec["_owner"] = owners
    return spec


def is_consumer(path):
    keys = [k for k in path if isinstance(k, str)]
    if not keys or keys[0] == "verification_status":
        return False
    for k in keys:
        if k == "sources" or k.endswith("_sources") or k == "anchoring_urls" or k.endswith("_anchoring_urls") \
                or k.endswith("provenance"):
            return False
    return keys[-1] not in STRUCTURAL


def _sentence(text, start, end):
    a = max(text.rfind(". ", 0, start), text.rfind("; ", 0, start))
    b = min([i for i in (text.find(". ", end), text.find("; ", end)) if i != -1] or [len(text)])
    return text[a + 1 if a != -1 else 0:b + 1]


def _noun(text, start, form):
    """A noun use of `hill` (the hilled mound): preceded by an article."""
    return form.lower() == "hill" and re.search(r"\b(a|the|each)\s+$", text[:start], re.I) is not None


def classify_leaf_matches(crop, text, spec):
    spans = []
    for e in spec["exclusions"]:
        if e.get("crops") and crop not in e["crops"]:
            continue
        for m in e["_rx"].finditer(text):
            spans.append((m.start(), m.end(), e["id"]))
    out = []
    for m in spec["_word"].finditer(text):
        form = m.group(0)
        ex = next((eid for a, b, eid in spans if a <= m.start() and m.end() <= b), None)
        if ex:
            out.append(Match(form, m.start(), m.end(), "none", ex, False))
            continue
        tid = spec["_owner"].get(crop)
        term = spec["terms"].get(tid)
        sent = _sentence(text, m.start(), m.end())
        if term is None or form.lower() not in term["forms"] or any(r.search(sent) for r in term["_refuse"]):
            out.append(Match(form, m.start(), m.end(), None, None, False))
        else:
            out.append(Match(form, m.start(), m.end(), tid, None, _noun(text, m.start(), form)))
    return out


def classify_leaf(crop, field, text, spec):
    """The sorted term ids of one leaf's occurrences; raises Refused if any is UNCLASSIFIED."""
    ms = classify_leaf_matches(crop, text, spec)
    if any(m.term is None for m in ms):
        raise Refused(f"UNCLASSIFIED hill-word in {crop}.{field}: {text[:120]!r}")
    return tuple(sorted({m.term for m in ms}))


def _walk(o, p):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from _walk(v, p + [k])
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _walk(v, p + [i])
    elif isinstance(o, str):
        yield p, o


def classify_dataset(data, spec, floor=DEFAULT_FLOOR, refuse=True):
    rows, unclassified = [], []
    for c in data["crops"]:
        for p, s in _walk(c, []):
            if not is_consumer(p) or not spec["_word"].search(s):
                continue
            ms = classify_leaf_matches(c["slug"], s, spec)
            path = ".".join(map(str, p))
            bad = [m for m in ms if m.term is None]
            if bad:
                unclassified.append((c["slug"], path, s))
            rows.append(Row(c["slug"], path, s, ms, tuple(sorted({m.term or "UNCLASSIFIED" for m in ms}))))
    if refuse and unclassified:
        raise Refused(f"UNCLASSIFIED: {len(unclassified)} leaf(s), first {unclassified[0][0]}.{unclassified[0][1]}: "
                      f"{unclassified[0][2][:120]!r}")
    if len(rows) < floor:
        raise Refused(f"inspected {len(rows)} consumer leaf(s) with a hill-word, below the floor {floor}")
    return Result(rows, unclassified, len(rows))


if __name__ == "__main__":
    import os, sys
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    spec = load_spec(sys.argv[1] if len(sys.argv) > 1 else
                     os.path.join(root, "tools", "staging", "pla673_674_prep", "glossary_match.json"))
    r = classify_dataset(json.load(open(os.path.join(root, "crops_data_final.json"), encoding="utf-8")), spec)
    by = {}
    for row in r.rows:
        by[row.term_ids] = by.get(row.term_ids, 0) + 1
    print(f"glossary_sense: inspected {r.inspected} consumer leaves, 0 unclassified; {by}")
