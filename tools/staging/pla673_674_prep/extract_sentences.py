"""PLA-673 prep: every sentence that mentions a term, from the HASHED pages cited on a set of crops (+ named extra pages).

Read-only on canonical. A page is read only when its (sha256, url) is a MANIFEST row and its cached bytes hash to their
name (cited_promote_common's rule); a cited url with no MANIFEST row is reported as NOT HASHED, never read. Sentences
are norm_text form split on sentence ends, so every quote printed is a substring of the hashed page text.

Usage: python3 extract_sentences.py OUT.json REGEX crop[,crop...] [extra_url ...]
"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from cited_promote_common import cited_urls, manifest, norm_text, pdf_text, sha256_bytes  # noqa: E402

EV = os.path.join(ROOT, "tools", ".evidence_cache")


def page_text(sha):
    files = glob.glob(os.path.join(EV, sha + ".*"))
    if len(files) != 1:
        raise SystemExit(f"{len(files)} cache files for {sha[:12]}")
    raw = open(files[0], "rb").read()
    if sha256_bytes(raw) != sha:
        raise SystemExit(f"cache bytes for {sha[:12]} hash to {sha256_bytes(raw)[:12]}")
    return norm_text(pdf_text(raw)) if files[0].endswith(".pdf") else norm_text(raw.decode("utf-8", "replace"))


def main():
    out, rx, crops = sys.argv[1], re.compile(sys.argv[2]), sys.argv[3].split(",")
    extra = sys.argv[4:]
    data = json.load(open(os.path.join(ROOT, "crops_data_final.json"), encoding="utf-8"))
    by_slug = {c["slug"]: c for c in data["crops"]}
    man = manifest(EV)
    url_to_sha = {}
    for sha, urls in man.items():
        for u in urls:
            url_to_sha.setdefault(u, set()).add(sha)
    pages = {}  # url -> {"crops": [...], "sha": ...}
    for slug in crops:
        for u in cited_urls(by_slug[slug]):
            pages.setdefault(u, {"crops": set()})["crops"].add(slug)
    for u in extra:
        pages.setdefault(u, {"crops": set()})["crops"].add("(extra)")
    result = {"regex": rx.pattern, "crops": crops, "pages": [], "not_hashed": []}
    for u in sorted(pages):
        shas = url_to_sha.get(u)
        if not shas:
            result["not_hashed"].append({"url": u, "crops": sorted(pages[u]["crops"])})
            continue
        for sha in sorted(shas):
            t = page_text(sha)
            sents = [s for s in re.split(r"(?<=[.!?])\s+", t) if rx.search(s)]
            # strip script/json noise: keep sentences under 600 chars
            sents = [s for s in sents if len(s) < 600]
            result["pages"].append({"url": u, "sha256": sha, "crops": sorted(pages[u]["crops"]),
                                    "hits": [{"offset": t.find(s), "sentence": s} for s in sents]})
    json.dump(result, open(out, "w"), indent=1, ensure_ascii=False)
    print(f"{len(result['pages'])} hashed pages, {sum(len(p['hits']) for p in result['pages'])} sentences, "
          f"{len(result['not_hashed'])} cited urls NOT hashed")


main()
