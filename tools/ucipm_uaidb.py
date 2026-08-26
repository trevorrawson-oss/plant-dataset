#!/usr/bin/env python3
"""Parser for UC IPM's Pesticide Active Ingredient Details pages (home and landscape).

WHY THIS EXISTS RATHER THAN A WebFetch. The rendered hazard grid is a TWO-LEVEL table whose values
are not all text: the honey-bee cell is an EMPTY <span> carrying its value in a CSS class, and every
<th> embeds an sr-only footnote ending "Information to be added." A markdown flattener reads those
footnotes as data and shifts the columns. On 2026-08-26 that produced Acute **L** against the
rendered page's Acute **H** -- CAUTION versus DANGER on a carcinogen-listed fungicide. See the
`webfetch-markdown-table-column-shift` note.

THE POSITIVE CONTROL IS THE POINT. `tools/test_ucipm_uaidb.py` parses the cached chlorothalonil page
in tools/fixtures/ and asserts H / L / medium / H / Prop 65 + US EPA, which is what Trevor's rendered
screenshot showed. Any change to this parser that breaks that control is wrong, and no reading from
this database should be trusted in a promote unless the control passes in the same pass.

BEE BANDS ARE THREE, NOT FOUR. The page renders `bee-precaution-rating-{high,medium,low}`. The
roman numerals I-IV belong to a DIFFERENT database and appear here only inside a footnote, so a
numeral must never be attributed to this page: `medium` spans II and III. What the page supports is
the PRESCRIPTION -- high grants no time window, medium grants sunset to midnight, low needs no
precaution.

Usage: python3 tools/ucipm_uaidb.py 115 111 47      # prints parsed rows as JSON
"""
import urllib.request, re, ssl, html as H

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
URL = ("https://ipm.ucanr.edu/home-and-landscape/pesticide-active-ingredients-database"
       "/active-ingredient-details/?uaiKey=%s")
COLS = ["water_quality", "natural_enemies", "honey_bees", "acute", "chronic"]
_ctx = ssl.create_default_context(); _ctx.check_hostname = False; _ctx.verify_mode = ssl.CERT_NONE


def _txt(s):
    s = re.sub(r"<span class=.sr-only.*?</span>", " ", s, flags=re.S)   # drop footnote text
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def fetch(key, cache=True):
    fn = f"ai_{key}.html"
    try:
        if cache: return open(fn).read()
    except OSError: pass
    h = urllib.request.urlopen(urllib.request.Request(URL % key, headers={"User-Agent": UA}),
                               timeout=30, context=_ctx).read().decode("utf-8", "replace")
    open(fn, "w").write(h)
    return h


def parse(key):
    h = fetch(key)
    name = _txt(re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S).group(1)) if re.search(r"<h1", h) else ""
    for m in re.findall(r"<h[1-6][^>]*>(.*?)</h[1-6]>", h, re.S):
        t = _txt(m)
        if t and t.lower() not in ("feedback",) and "database" not in t.lower():
            name = t; break
    tb = re.findall(r"<table.*?</table>", h, re.S)[0]
    body = tb[tb.find("</thead>"):]
    row = re.search(r"<tr>(.*?)(?:</tr>|</tbody>)", body, re.S).group(1)
    cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)
    out = {"key": key, "name": name}
    for i, c in enumerate(COLS):
        raw = cells[i] if i < len(cells) else ""
        bee = re.search(r"bee-precaution-rating-([a-z]+)", raw)
        out[c] = ("bee:" + bee.group(1)) if bee else (_txt(raw) or "--")
    # sections
    def section(title):
        m = re.search(rf"<h[1-6][^>]*>\s*{title}.*?</h[1-6]>(.*?)(?=<h[1-6]|\Z)", h, re.S | re.I)
        return _txt(m.group(1)) if m else ""
    out["type"] = section("Pesticide Type")[:200]
    out["mode"] = section("How Does This Active Ingredient Work\\?")[:400]
    out["safety"] = section("Safety Precautions")[:900]
    out["home_products"] = section("Example home, garden or landscape use products")[:300]
    return out


if __name__ == "__main__":
    import sys, json
    for k in sys.argv[1:]:
        print(json.dumps(parse(k), indent=1))
