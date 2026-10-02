"""pla10_promote_common -- the evidence and diff helpers PLA-10 promote 2 shares with promote 1, as COPIES.

Promotes must not import promotes (a cross-import kills the mutation harness's scratch copy), so these are
copied from promote_pla10_planting_layout.py (landed, replay-pinned at c5fc3d13) rather than imported, and
test_promote_pla10_promote2.py pins every copied function byte-identical to its promote-1 original: a change
to how evidence is read is a change to BOTH promotes, made deliberately, never a silent fork.
Copied 2026-10-02 (PLA-10 promote 2, session 1).
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
