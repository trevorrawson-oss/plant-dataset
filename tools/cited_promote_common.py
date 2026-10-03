"""cited_promote_common -- the shared evidence, diff and restatement helpers for promotes that land figures
cited to hashed page bytes. Arc-neutral: PLA-10's three promotes import it, and so will the citrus pass and
PLA-534 (housekeeping kickoff 60, ruling 5, 2026-10-03).

HISTORY. These were written inline in promote_pla10_planting_layout.py (PLA-10 promote 1, landed d021116), copied
byte-identically into pla10_promote_common.py for promotes 2 and 3 (2026-10-02; promotes must not import
promotes), and pinned to the originals by inspect.getsource tests. Moved here BYTE-IDENTICALLY on 2026-10-03:
every function body and constant below is the text it had in pla10_promote_common at e15bce3, which was itself
byte-identical to promote 1's (A3 measurement, kickoff 60). pla10_promote_common is now a re-export shim.

THE GUARD is behavior, not text: test_pla10_promote_replays.py replays each PLA-10 promote on its real stage
and requires its landed canonical byte for byte (cf1d480d, 31b766e8, b331e5f2). test_cited_promote_common.py
pins the module's surface (SHARED, a typed literal) and the shim's identity re-export.
SHIPS MUTATION-TESTED via mutate_cited_promote_common.py.
"""
import csv, glob, hashlib, html, io, json, os, re, unicodedata

import pypdf

# Ruled 2026-10-01: PDF evidence is read through pypdf; the version is the pin (reproducible extraction).
PDF_TEXT_EXTRACTOR = ("pypdf", pypdf.__version__)
# Ruled 2026-10-01: number idioms the quote check reads, in FEET ("a foot" -> 1.0); the test pins the table.
IDIOMS = (("a foot", 1.0),)
EVIDENCE_COLS = ("crop", "entry_id", "field", "value", "source_id", "url", "sha256", "quote")


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()



def serialize(data):
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")



def compact(v):
    return json.dumps(v, separators=(",", ":"), ensure_ascii=False)



def leaf_diff(a, b, path=()):
    """Every path where a and b differ, two-sided: a key or index present on one side only counts."""
    if isinstance(a, dict) and isinstance(b, dict):
        out = set()
        for k in set(a) | set(b):
            if k not in a or k not in b:
                out.add(path + (k,))
            else:
                out |= leaf_diff(a[k], b[k], path + (k,))
        return out
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        out = set()
        for i, (x, y) in enumerate(zip(a, b)):
            out |= leaf_diff(x, y, path + (i,))
        return out
    return set() if compact(a) == compact(b) else {path}



def norm_text(s):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"[‐-―]", "-", s)
    return re.sub(r"\s+", " ", s).strip().lower()



def _numbers(s):
    nums = set()
    for m in re.finditer(r"\d+(?:\.\d+)?", s):
        nums.add(float(m.group()))
    words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
             "nine": 9, "ten": 10, "twelve": 12, "fifteen": 15, "twenty": 20}
    for w, n in words.items():
        if re.search(rf"\b{w}\b", s, re.I):
            nums.add(float(n))
    for phrase, n in IDIOMS:
        if re.search(rf"\b{phrase}\b", s, re.I):
            nums.add(float(n))
    return nums



def quote_states(field, value, quote):
    nums = _numbers(quote)
    ends = {float(x) for x in value}
    if field == "plants_per_hill":
        return bool(ends & nums)
    if field == "mature_height_ft":
        return bool(ends & nums) or bool({x * 12 for x in ends} & nums)
    return bool(ends & nums) or bool({x / 12 for x in ends} & nums)



def pdf_text(raw):
    """The text of a PDF's HASHED bytes, through the pinned extractor (PDF_TEXT_EXTRACTOR)."""
    reader = pypdf.PdfReader(io.BytesIO(raw))
    return "\n".join((page.extract_text() or "") for page in reader.pages)



def manifest(evidence_dir):
    p = os.path.join(evidence_dir, "MANIFEST.tsv")
    rows = {}
    with open(p, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            rows.setdefault(r["sha256"], set()).add(r["url"])
    return rows


# ---------------------------------------------------------------- copied 2026-10-02, session 2 (T1)
# promote 1's restatement scanner (its guard 4) and path helpers, for promote 2's moved mirrors. Pinned
# byte-identical to promote 1 by test_promote_pla10_promote2 (the functions, and the patterns below).
class Refused(Exception):
    pass


def refuse(msg):
    raise Refused(msg)


DIST = re.compile(r"\d+(?:\.\d+)?(?:\s*(?:to|-|–|or)\s*\d+(?:\.\d+)?)?\s*(?:-\s*)?"
                  r"(?:inch(?:es)?|in\b|in\.|\"|”|feet|foot|ft\b|ft\.)", re.I)
SPACING_WORD = re.compile(r"\b(apart|spac\w*|between|rows?|hills?|thin(?:ned|ning)?)\b", re.I)
SKIP_SUBTREES = ("verification_status", "sources", "anchoring_urls")
SEG = re.compile(r"([^.\[\]]+)|\[(\d+)\]|\[([a-z_]+)=([^\]]+)\]")


def parse_path(path):
    out, pos = [], 0
    for m in SEG.finditer(path):
        if m.start() != pos and path[pos:m.start()] != ".":
            refuse(f"unparseable path {path!r}")
        pos = m.end()
        if m.group(1) is not None:
            out.append(m.group(1))
        elif m.group(2) is not None:
            out.append(int(m.group(2)))
        else:
            out.append((m.group(3), m.group(4)))
    if pos != len(path) or not out:
        refuse(f"unparseable path {path!r}")
    return out


def resolve(crop, path):
    """Path -> concrete index-form path (list of str/int), against `crop`. Refuses if it names nothing."""
    node, concrete = crop, []
    segs = parse_path(path)
    for i, s in enumerate(segs):
        if isinstance(s, tuple):
            k, v = s
            if not isinstance(node, list):
                refuse(f"path {path!r}: [{k}={v}] on a non-list")
            hits = [j for j, x in enumerate(node) if isinstance(x, dict) and str(x.get(k)) == v]
            if len(hits) != 1:
                refuse(f"path {path!r}: [{k}={v}] matches {len(hits)} items")
            s = hits[0]
        if isinstance(s, int):
            if not isinstance(node, list) or s >= len(node):
                refuse(f"path {path!r}: index {s} out of range")
        elif not isinstance(node, dict) or (s not in node and i < len(segs) - 1):
            refuse(f"path {path!r}: {s!r} not found")
        concrete.append(s)
        node = node[s] if isinstance(s, int) or s in node else None
    return concrete


def fmt(concrete):
    return "".join(f"[{s}]" if isinstance(s, int) else (f".{s}" if i else s) for i, s in enumerate(concrete))


def set_at(crop, concrete, value):
    node = crop
    for s in concrete[:-1]:
        node = node[s]
    node[concrete[-1]] = value


# ---------------------------------------------------------------- the restatement scanner (unified 2026-10-03)
# ONE walker for every cited promote (kickoff 60, ruling 5): a prose leaf outside the citation machinery that
# states a distance (DIST) in a sentence that also carries one of `words` is a restatement candidate the author
# must adjudicate. spacing_strings (promotes 1 and 2) and height_strings (promote 3) were two copies of this
# walker differing only in the word test; both are now wrappers, proven byte-identical to the originals on
# promote 1's and promote 3's fixed lists. Deliberately wide; the author adjudicates every hit.
HEIGHT_WORD = re.compile(r"\b(tall|taller|height|heights|high)\b", re.I)
WIDTH_WORD = re.compile(r"\b(wide|width|spread)\b", re.I)


def distance_restatements(crop, words):
    """Sorted paths of the string leaves where some sentence matches DIST and any regex in `words`."""
    hits = []

    def walk(o, path):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in SKIP_SUBTREES or k.endswith(("_sources", "_anchoring_urls")):
                    continue
                walk(v, path + (k,))
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, path + (i,))
        elif isinstance(o, str):
            for sent in re.split(r"(?<=[.;!?])\s+", o):
                if DIST.search(sent) and any(w.search(sent) for w in words):
                    hits.append(fmt(list(path)))
                    return
    walk(crop, ())
    return sorted(set(hits))


def spacing_strings(crop):
    """Prose leaves stating a distance beside a spacing word (promotes 1 and 2, guard 4)."""
    return distance_restatements(crop, (SPACING_WORD,))


def height_strings(crop, spread_too):
    """Prose leaves stating a distance beside a height word (and a width word when a spread is authored)."""
    return distance_restatements(crop, (HEIGHT_WORD, WIDTH_WORD) if spread_too else (HEIGHT_WORD,))


# ---------------------------------------------------------------- the cached-quote check (extracted 2026-10-03)
# Was 16 lines inlined, byte-identically, in each PLA-10 promote's check_evidence (kickoff 60, ruling 5). Every
# refusal message is the text those promotes refused with; the suites assert it.
def cached_quote(r, man, evidence_dir, text_cache, tag):
    """An EVIDENCE row's quote in norm_text form, once proven to sit in the hashed bytes it names.

    Refuses unless (sha256, url) is a MANIFEST row, exactly one cache file carries that digest, the file's bytes
    hash to their name, and the normalized quote (12+ characters) is a substring of the normalized page text
    (PDFs through the pinned extractor). `text_cache` memoizes page text by digest across rows."""
    if r["url"] not in man.get(r["sha256"], set()):
        refuse(f"{tag}: ({r['sha256'][:12]}, url) is not in {evidence_dir}/MANIFEST.tsv")
    files = glob.glob(os.path.join(evidence_dir, r["sha256"] + ".*"))
    if len(files) != 1:
        refuse(f"{tag}: {len(files)} cache files for {r['sha256'][:12]}")
    if r["sha256"] not in text_cache:
        raw = open(files[0], "rb").read()
        if sha256_bytes(raw) != r["sha256"]:
            refuse(f"{tag}: the cached bytes hash to {sha256_bytes(raw)[:12]}, not their name")
        if files[0].endswith(".pdf"):
            text_cache[r["sha256"]] = norm_text(pdf_text(raw))
        else:
            text_cache[r["sha256"]] = norm_text(raw.decode("utf-8", "replace"))
    q = norm_text(r["quote"])
    if len(q) < 12 or q not in text_cache[r["sha256"]]:
        refuse(f"{tag}: the quote is not in the cached bytes: {r['quote'][:80]!r}")
    return q


# ---------------------------------------------------------------- added 2026-10-02, promote 3 session 1 (T4)
# The height/spread quote check (plan 58 §8 T4, ruling H4). PROMOTE 3 ONLY: promote 1's quote_states above is
# untouched (it matches mature_height_ft exactly, so a rounded 47/12 fails, and it has no mature_spread_ft
# branch). Not a copy of anything, so it carries no byte-identity pin; test_promote_pla10_promote3 pins
# quote_states and _numbers unchanged instead.
#
# THE STATED TOLERANCE. Heights store the quotient to 4 places (H4: 47 in -> 3.9167). A stored endpoint e is
# STATED by a figure f (in feet; an inches figure is f/12, "1 ft. 7 in." is 1 + 7/12) iff |e - f| <= TOL_FT,
# half a unit in the 4th decimal: 3.9167 and 47/12 pass against "47 inches", 3.9 and 3.917 do not.
# THE DIMENSION. A figure counts only for the dimension its clause names: a postfix word right after the
# figure (tall / high / in height -> height; wide / across / in width / spread -> width; "tall and wide",
# "in height and width" -> both; apart / between / long / in length -> NEITHER), else the nearest label to its
# left (height(s) / width / spread / "height & spread"), else a growth verb just before it (reach, grow,
# get up to -> height). So a spread can never be read off a height sentence, nor vine run off anything.
TOL_FT = 0.00005
_NUMWORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
             "ten": 10, "eleven": 11, "twelve": 12, "fifteen": 15, "eighteen": 18, "twenty": 20}
_NUM = r"(?:\d+(?:\.\d+)?|" + "|".join(_NUMWORDS) + r"|a(?=\s+foot\b))"
_FT = r"(?:feet\b|foot\b|ft\b\.?|'|′)"
_IN = r"(?:inches\b|inch\b|in\.|in\b(?!\s+(?:height|width|length|diameter|spread|the|a|an)\b)|\"|″)"
_QTY = re.compile(rf"(?P<cf>{_NUM})\s*{_FT}\s*(?P<ci>{_NUM})\s*{_IN}"
                  rf"|(?P<n>{_NUM})(?:\s*-?\s*(?:(?P<ft>{_FT})|(?P<inch>{_IN})))?")
_JOIN = re.compile(r"\s*(?:-\s*)?(?:to|-|–|or)\s*")
_POSTFIX = (
    (re.compile(r"(?:tall|high)\s*,?\s*(?:and|&)\s*(?:wide|across)\b"), "HW"),
    (re.compile(r"in\s+height\s*(?:and|&)\s*(?:width|spread)\b"), "HW"),
    (re.compile(r"(?:tall|high|in\s+height)\b"), "H"),
    (re.compile(r"(?:wide|across|in\s+width|in\s+diameter|in\s+spread|spread\b(?!\s*:))"), "W"),
    (re.compile(r"(?:apart|between|deep|long|away|in\s+length|of\s+vine)\b"), ""),
)
_LABEL = re.compile(r"(?P<hw>height\s*(?:&|and)\s*(?:spread|width))|(?P<h>\bheights?\b)|(?P<w>\bwidth\b|\bspread\b)")
_VERB = re.compile(r"\b(?:reach(?:es|ing)?|grow(?:s|ing)?|get)\b[^.;]{0,24}$")


def _num_val(tok):
    return float(_NUMWORDS[tok]) if tok in _NUMWORDS else (1.0 if tok == "a" else float(tok))


def _ft_groups(q):
    """[(dimension class 'H' / 'W' / 'HW' / '', [figures in feet])] for each measurement in a norm_text quote."""
    qty = []
    for m in _QTY.finditer(q):
        if m.group("cf") is not None:
            qty.append([m.start(), m.end(), _num_val(m.group("cf")) + _num_val(m.group("ci")) / 12, "ft"])
        else:
            unit = "ft" if m.group("ft") else ("in" if m.group("inch") else None)
            qty.append([m.start(), m.end(), _num_val(m.group("n")), unit])
    groups = []
    for x in qty:
        # one range: figures joined by an explicit "to" / "-" / "or" ("2 to10 feet", "18 inches to 4 feet",
        # "1 ft. 0 in. - 2 ft. 0 in."); a unitless figure takes the next unit to its right
        if groups and _JOIN.fullmatch(q[groups[-1][-1][1]:x[0]]):
            groups[-1].append(x)
        else:
            groups.append([x])
    out = []
    for g in groups:
        units = [x[3] for x in g]
        if not any(units):
            continue
        vals, nxt = [], None
        for x in reversed(g):
            nxt = x[3] or nxt
            vals.append(x[2] / 12 if nxt == "in" else x[2])
        start, end = g[0][0], g[-1][1]
        after = re.sub(r"^(?:\s*\([^)]*\))*\s*", "", q[end:])
        cls = None
        for rx, c in _POSTFIX:
            if rx.match(after):
                cls = c
                break
        if cls is None:
            labels = list(_LABEL.finditer(q[:start]))
            if labels:
                lm = labels[-1]
                cls = "HW" if lm.group("hw") else ("H" if lm.group("h") else "W")
            elif _VERB.search(q[:start]):
                cls = "H"
            else:
                cls = ""
        out.append((cls, sorted(vals)))
    return out


def ft_endpoints_stated(field, value, quote):
    """The endpoints of `value` that the quote STATES for this field's dimension, within TOL_FT."""
    want = {"mature_height_ft": "H", "mature_spread_ft": "W"}[field]
    figs = [v for cls, vals in _ft_groups(quote) if want in cls for v in vals]
    return {e for e in value if any(abs(float(e) - f) <= TOL_FT for f in figs)}


def quote_states_ft(field, value, quote):
    return bool(ft_endpoints_stated(field, value, quote))
