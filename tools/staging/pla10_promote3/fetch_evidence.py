#!/usr/bin/env python3
"""fetch_evidence -- PLA-10 promote 3 session helper (copied from promote 2, unchanged but SAVED_BY): fetch a page from RAW BYTES under two user agents
(a browser UA and a plain Python UA, the PLA-532 convention), save tools/.evidence_cache/<sha256>.<ext>,
and print the MANIFEST.tsv row.  It never appends MANIFEST.tsv itself: the main session merges rows.

Usage: fetch_evidence.py URL [URL ...]       (prints one TSV line per URL to stdout; diagnostics to stderr)
       fetch_evidence.py --from FILE         (one URL per line)
Columns printed: sha256, bytes, fetched, agents, url, saved_by, final_url, content_type, status
"""
import gzip, hashlib, os, sys, time, urllib.request, urllib.error, ssl, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.normpath(os.path.join(HERE, "..", "..", ".evidence_cache"))
BROWSER = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
           "Chrome/128.0.0.0 Safari/537.36")
SAFARI = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) "
          "Version/17.6 Safari/605.1.15")
if os.environ.get("FETCH_UA") == "safari":
    BROWSER = SAFARI
PLAIN = "Python-urllib/3.12"
SAVED_BY = "PLA-10 promote 3 session 2"
CTX = ssl.create_default_context()


EXTRA = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
         "Accept-Language": "en-US,en;q=0.9", "Accept-Encoding": "gzip", "Connection": "close"}
if os.environ.get("FETCH_UA") == "safari":
    EXTRA.update({"Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "none",
                  "Upgrade-Insecure-Requests": "1"})
# Accept-Encoding is required: hgic.clemson.edu's Cloudflare rule (error 1010) 403s a request without it,
# and the plain Python UA outright (measured 2026-10-01). The saved bytes are the DECOMPRESSED document.
DELAY = float(os.environ.get("FETCH_DELAY", "0"))


def get(url, ua):
    if DELAY:
        time.sleep(DELAY)
    req = urllib.request.Request(url, headers={"User-Agent": ua, **EXTRA})
    try:
        with urllib.request.urlopen(req, timeout=60, context=CTX) as r:
            body = r.read()
            if (r.headers.get("Content-Encoding") or "").lower() == "gzip":
                body = gzip.decompress(body)
            return r.status, r.geturl(), r.headers.get("Content-Type", ""), body
    except urllib.error.HTTPError as e:
        return e.code, url, "", b""
    except Exception as e:  # noqa
        return f"ERR {type(e).__name__}", url, "", b""


def ext_for(ctype, url, body):
    c = (ctype or "").lower()
    if "pdf" in c or body[:5] == b"%PDF-":
        return "pdf"
    if "html" in c or b"<html" in body[:2000].lower():
        return "html"
    if url.lower().endswith(".pdf"):
        return "pdf"
    return "bin"


def fetch(url):
    sb, fb, cb, bb = get(url, BROWSER)
    sp, fp, cp, bp = get(url, PLAIN)
    ok_b, ok_p = (sb == 200 and bb), (sp == 200 and bp)
    if ok_b and ok_p:
        agents = "urllib browser+plain UA (byte-identical)" if bb == bp else \
                 f"urllib browser UA kept (plain UA differs: {len(bp)} bytes)"
        body, final, ctype = bb, fb, cb
    elif ok_b:
        agents, body, final, ctype = f"urllib browser UA (plain UA {sp})", bb, fb, cb
    elif ok_p:
        agents, body, final, ctype = f"urllib plain UA (browser UA {sb})", bp, fp, cp
    else:
        return None, f"FAILED browser={sb} plain={sp}"
    sha = hashlib.sha256(body).hexdigest()
    ext = ext_for(ctype, final, body)
    path = os.path.join(CACHE, f"{sha}.{ext}")
    if not os.path.exists(path):
        with open(path, "wb") as f:
            f.write(body)
    row = [sha, str(len(body)), datetime.date.today().isoformat(), agents, url, SAVED_BY, final,
           ctype.split(";")[0], "ok"]
    return row, None


def main(argv):
    urls = []
    if argv and argv[0] == "--from":
        urls = [u.strip() for u in open(argv[1]) if u.strip() and not u.startswith("#")]
    else:
        urls = argv
    os.makedirs(CACHE, exist_ok=True)
    rc = 0
    for u in urls:
        row, err = fetch(u)
        if err:
            print("\t".join(["", "", "", err, u, SAVED_BY, "", "", "FAILED"]))
            print(f"FAILED {u}: {err}", file=sys.stderr)
            rc = 1
        else:
            print("\t".join(row))
            print(f"ok {row[0][:12]} {row[1]:>8} {row[7]:<16} {u}", file=sys.stderr)
        sys.stdout.flush()
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
