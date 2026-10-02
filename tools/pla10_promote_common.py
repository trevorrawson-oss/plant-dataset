"""pla10_promote_common -- the evidence and diff helpers PLA-10 promote 2 shares with promote 1, as COPIES.

Promotes must not import promotes (a cross-import kills the mutation harness's scratch copy), so these are
copied from promote_pla10_planting_layout.py (landed, replay-pinned at c5fc3d13) rather than imported, and
test_promote_pla10_promote2.py pins every copied function byte-identical to its promote-1 original: a change
to how evidence is read is a change to BOTH promotes, made deliberately, never a silent fork.
Copied 2026-10-02 (PLA-10 promote 2, session 1); the restatement scanner and path helpers (with Refused /
refuse, which they raise) added in session 2 for T1.
"""
import csv, hashlib, html, io, json, os, re, unicodedata

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


def spacing_strings(crop):
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
                if DIST.search(sent) and SPACING_WORD.search(sent):
                    hits.append(fmt(list(path)))
                    return
    walk(crop, ())
    return sorted(set(hits))
