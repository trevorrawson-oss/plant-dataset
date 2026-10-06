"""PLA-673 part B2 prep: candidate sentences, per claim, from the HASHED pages cited on each of the 7 leaves' crops.

Machine collection only; curation (does the sentence bear on the claim) is done by reading, in the packet. Output JSON:
{crop: {"pages": [...], "not_hashed": [...], "claims": {claim: [{sha, url, sentence, offset}]}}}.
"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from cited_promote_common import cited_urls, manifest, norm_text, pdf_text, sha256_bytes  # noqa: E402

EV = os.path.join(ROOT, "tools", ".evidence_cache")
PEPPER = {
    "raised beds or hills": r"\braised\b|\bhills?\b|\bmound|\bridges?\b|\bbeds?\b[^.]{0,40}\b(drain|raise)",
    "well-drained": r"well[- ]drained|drainage|poorly[- ]drained|drains?\b",
    "low spots that stay wet": r"low[- ](spots?|areas?|lying)|standing water|waterlog|saturat|excess(ive)? (soil )?moisture|wet (soil|areas?|spots?)|flood",
    "water at the soil, not overhead": r"overhead|at the soil|base of the plants?|drip irrigation|soaker",
    "do not overwater": r"overwater|over-water|too much water|excess(ive)? (water|irrigation)",
    "mulch to limit splash": r"splash|mulch",
    "rotation": r"rotat",
    "fruit off saturated soil": r"fruit[^.]{0,60}\b(soil|ground)\b|\b(soil|ground)\b[^.]{0,60}fruit",
    "phytophthora (the disease named)": r"phytophthora",
}
SQUASH = {
    "low hills or mounds": r"\bhills?\b|\bmounds?\b|\braised\b",
    "about a foot across (width)": r"\bacross\b|diameter|\bwide\b|width",
    "warm faster in spring": r"warm(s|er|ing)?\b[^.]{0,40}\bsoil|soil[^.]{0,40}\bwarm|black plastic|faster in (the )?spring",
    "drain better": r"drain",
    "a starting point for the vines": r"starting point|sprawl|spread",
}
LEAVES = [
    ("bell-pepper", ["diseases", 1, "prevention_seasoned"], PEPPER),
    ("banana-pepper", ["diseases", 1, "prevention_seasoned"], PEPPER),
    ("eggplant", ["diseases", 3, "prevention_seasoned"], PEPPER),
    ("pumpkin", ["soil_prep_seasoned"], SQUASH),
    ("butternut-squash", ["soil_prep_seasoned"], SQUASH),
    ("acorn-squash", ["soil_prep_seasoned"], SQUASH),
    ("spaghetti-squash", ["soil_prep_seasoned"], SQUASH),
]


def text(sha):
    f = glob.glob(os.path.join(EV, sha + ".*"))
    assert len(f) == 1, sha
    raw = open(f[0], "rb").read()
    assert sha256_bytes(raw) == sha
    return norm_text(pdf_text(raw)) if f[0].endswith(".pdf") else norm_text(raw.decode("utf-8", "replace"))


def main(out):
    data = json.load(open(os.path.join(ROOT, "crops_data_final.json"), encoding="utf-8"))
    by = {c["slug"]: c for c in data["crops"]}
    man = manifest(EV)
    u2s = {}
    for s, us in man.items():
        for u in us:
            u2s.setdefault(u, []).append(s)
    cache, res = {}, {}
    for slug, path, claims in LEAVES:
        c = by[slug]
        o = c
        for k in path:
            o = o[k]
        urls = sorted(cited_urls(c))
        pages = [(u, sorted(u2s[u])[0]) for u in urls if u in u2s]
        r = {"path": ".".join(map(str, path)), "text": o, "pages": [{"url": u, "sha": s} for u, s in pages],
             "not_hashed": [u for u in urls if u not in u2s], "claims": {}}
        for claim, rx in claims.items():
            hits, seen = [], set()
            for u, s in pages:
                if s not in cache:
                    cache[s] = text(s)
                t = cache[s]
                for sent in re.split(r"(?<=[.!?])\s+", t):
                    if len(sent) < 600 and re.search(rx, sent) and (s, sent) not in seen:
                        seen.add((s, sent))
                        hits.append({"sha": s, "url": u, "sentence": sent, "offset": t.find(sent)})
            r["claims"][claim] = hits
        res[slug] = r
    json.dump(res, open(out, "w"), ensure_ascii=False, indent=1)
    for slug, r in res.items():
        print(slug, len(r["pages"]), "hashed pages,", len(r["not_hashed"]), "not hashed;",
              {k: len(v) for k, v in r["claims"].items()})


main(sys.argv[1])
