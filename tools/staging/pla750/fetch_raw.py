"""PLA-750: fetch the raw bytes of every page the promote cites into tools/.evidence_cache.

Each page is saved as <sha256>.<html|pdf> and gets a MANIFEST.tsv row. A url already MANIFEST-listed with
a file present is skipped. Then every research quote whose page is now hashed is re-checked against the
RAW bytes through cited_promote_common.norm_text (the promote's own normalizer), so a WAF page or a
PLA-768 loss shows up here, not at promote time.

Usage: python3 tools/staging/pla750/fetch_raw.py URL_LIST_FILE
Writes: tools/.evidence_cache/*, MANIFEST.tsv rows, tools/staging/pla750/raw_verify.json
"""
import csv, glob, hashlib, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, TOOLS)
from cited_promote_common import norm_text, pdf_text  # noqa: E402

CACHE = os.path.join(TOOLS, ".evidence_cache")
MAN = os.path.join(CACHE, "MANIFEST.tsv")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
SAVED_BY = "PLA-750 heat-hold promote session"


def manifest():
    rows = list(csv.DictReader(open(MAN, encoding="utf-8", newline=""), delimiter="\t"))
    return rows, {r["url"]: r["sha256"] for r in rows}


def fetch(url):
    r = subprocess.run(["curl", "-sL", "--compressed", "-m", "60", "-A", UA, "-H", "Accept-Language: en-US,en;q=0.9",
                        "-w", "\n%{http_code} %{content_type}", url], capture_output=True)
    body, _, meta = r.stdout.rpartition(b"\n")
    code, _, ctype = meta.decode(errors="replace").partition(" ")
    return int(code or 0), ctype, body


def main():
    urls = [u.strip() for u in open(sys.argv[1]) if u.strip()]
    rows, have = manifest()
    added, report = [], {}
    for url in urls:
        if url in have and glob.glob(os.path.join(CACHE, have[url] + ".*")):
            report[url] = "cached"
            continue
        code, ctype, body = fetch(url)
        if code != 200 or len(body) < 500:
            report[url] = f"FAIL http {code} bytes {len(body)}"
            continue
        ext = "pdf" if body[:5] == b"%PDF-" or "pdf" in ctype else "html"
        sha = hashlib.sha256(body).hexdigest()
        with open(os.path.join(CACHE, f"{sha}.{ext}"), "wb") as f:
            f.write(body)
        added.append({"sha256": sha, "bytes": str(len(body)), "fetched": time.strftime("%Y-%m-%d"),
                      "agents": "curl (browser UA)", "url": url, "saved_by": SAVED_BY})
        have[url] = sha
        report[url] = f"fetched {ext} {len(body)}"
    if added:
        with open(MAN, "a", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["sha256", "bytes", "fetched", "agents", "url", "saved_by"],
                               delimiter="\t", lineterminator="\n")
            for r in added:
                w.writerow(r)
    # re-verify research quotes against the raw bytes
    R = {}
    for p in sorted(glob.glob(os.path.join(HERE, "research", "*.json"))):
        R.update(json.load(open(p)))
    texts, ver = {}, {"found": 0, "missing": [], "unhashed": 0}
    for slug, v in R.items():
        for i, e in enumerate(v["evidence"]):
            sha = have.get(e["url"])
            files = glob.glob(os.path.join(CACHE, f"{sha}.*")) if sha else []
            if not files:
                ver["unhashed"] += 1
                continue
            if sha not in texts:
                raw = open(files[0], "rb").read()
                texts[sha] = norm_text(pdf_text(raw) if files[0].endswith(".pdf") else raw.decode("utf-8", "replace"))
            if norm_text(e["quote"]) in texts[sha]:
                ver["found"] += 1
            else:
                ver["missing"].append([slug, i, e["url"], e["quote"][:120]])
    json.dump({"fetch": report, "verify": ver}, open(os.path.join(HERE, "raw_verify.json"), "w"), indent=1)
    print(f"fetched {len(added)}, cached {sum(1 for x in report.values() if x == 'cached')}, "
          f"failed {sum(1 for x in report.values() if x.startswith('FAIL'))}")
    for u, s in report.items():
        if s.startswith("FAIL"):
            print("  ", s, u)
    print(f"quotes vs raw bytes: {ver['found']} found, {len(ver['missing'])} missing, {ver['unhashed']} page not hashed")
    for m in ver["missing"]:
        print("   MISSING", m)


if __name__ == "__main__":
    main()
