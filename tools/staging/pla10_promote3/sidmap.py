"""URL -> source_catalog id: the id the crop itself anchors the URL to, else the id any crop anchors it to, else a
catalog entry whose url is a prefix of the page's. Prints every candidate so a choice is visible, never silent."""
import json, os, re
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def anchors(o, out):
    if isinstance(o, dict):
        for k, v in o.items():
            if k.endswith("anchoring_urls") and isinstance(v, dict):
                for sid, a in v.items():
                    if isinstance(a, dict) and a.get("url"):
                        out.setdefault(a["url"], set()).add(sid)
            else:
                anchors(v, out)
    elif isinstance(o, list):
        for v in o:
            anchors(v, out)


def candidates(data, slug, url):
    crop = next(c for c in data["crops"] if c["slug"] == slug)
    own, glob_ = {}, {}
    anchors(crop, own)
    for c in data["crops"]:
        anchors(c, glob_)
    norm = lambda u: u.rstrip("/")
    o = sorted({s for u, ss in own.items() if norm(u) == norm(url) for s in ss})
    g = sorted({s for u, ss in glob_.items() if norm(u) == norm(url) for s in ss})
    cat = sorted(k for k, v in data["source_catalog"].items()
                 if v.get("url") and url.startswith(v["url"].rstrip("/")) and len(v["url"].rstrip("/")) > 10)
    return o, g, cat
