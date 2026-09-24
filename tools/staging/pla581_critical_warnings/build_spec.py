#!/usr/bin/env python3
"""Build tools/staging/pla581_critical_warnings/spec.json for the PLA-581 promote.

WHAT IT BUILDS. The top-level `container_safety` object (3 warnings + one provenance record each),
the per-warning EVIDENCE (the page sentences each warning rests on), and the ledger of the candidates
the spec's section 4.5 evidence test CUT. Nothing per crop: the promote writes
`critical_warnings: null` on all 121 certified crops by rule, not from this file.

EVERY DIGEST IS DERIVED FROM THE SOURCE BYTES, never typed. The raw bodies sit in `_raw/`
(gitignored), one file per page per user-agent, as fetched on FETCH_DATE. For each page this script
requires the two agents' bytes to be IDENTICAL (a WAF block reads as absence under one agent and not
the other, and a status code is not liveness) and computes the sha256 and byte count. Every evidence
sentence must be present in its own page's text. A page missing, differing between agents, or not
carrying a sentence REFUSES.

THE BUILD IS NOT ITS OWN CHECK. The promote verifies this output against independent literals: the
measured digests keyed by page, the evidence sentences keyed by warning, the ruled ids / severity /
sources / titles, and the title and body copy re-read from the APPROVED SPEC DOCUMENT's section 14
(amendment 3), not from here.

Usage:  build_spec.py --from DIR     # copy DIR/<page>.{curl,browser} into _raw/ first, then build
        build_spec.py                # build from _raw/
"""
import argparse, hashlib, html as _html, json, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "spec.json")
RAW = os.path.join(HERE, "_raw")
AGENTS = ("curl", "browser")

BASE_SHA = "526788f2c34a7fe1c59e9427271c1d1738c6b6cce2c1d0524df715e4fc359659"  # PLA-580, 2588678
FETCH_DATE = "2026-09-23"

# page key -> (source key, url)
PAGES = {
    "uiuc_size": ("uiuc_ext", "https://extension.illinois.edu/container-gardens/container-size"),
    "csu_gardens": ("csu_ext", "https://extension.colostate.edu/resource/container-gardens/"),
    "uiuc_vegcont": ("uiuc_ext", "https://extension.illinois.edu/container-gardens/vegetable-containers"),
    "uiuc_material": ("uiuc_ext",
                      "https://extension.illinois.edu/container-gardens/container-material-choices"),
}
INSTITUTION = {"uiuc_ext": "University of Illinois Extension",
               "csu_ext": "Colorado State University Extension"}
# A page whose digest today differs from the one the spec recorded. Stated in words, never by
# quoting the old digest: it was not measured by this pass, and the promote refuses any digest that
# was not.
DRIFT = {
    "csu_gardens": "This page's 2026-09-21 read (spec section 12) recorded a different sha256 at the "
                   "same byte length; no copy of that read was kept, so the cause is undetermined, "
                   "and the sentences quoted here are present in these bytes.",
}

# The three warnings, per spec section 14 (amendment 3): copy authored in the claude.ai lane and
# ruled by Trevor 2026-09-23 after two independent clause checks. `anchors` is the ONE page per
# source key that anchoring_urls carries; `evidence` is every (page, sentence) the warning rests on,
# which can include a page it does not anchor (container_material's treated-lumber clause).
# severity is `high` on all three, UNIFORM and MODELED: no source grades them, no ranking is claimed.
WARNINGS = [
    {"id": "balcony_load", "anchors": {"uiuc_ext": "uiuc_size"},
     "evidence": [("uiuc_size", "Consult with a building architect concerning weight limitations when "
                                "placing heavy pots on balcony or rooftop gardens.")],
     "title": "Ask what your balcony or roof can carry",
     "beginner": "A balcony or roof can only hold so much weight. Before you set heavy pots there, ask "
                 "a building architect what it can safely carry.",
     "seasoned": "Illinois Extension's guidance is to consult a building architect about weight "
                 "limits before placing heavy pots on a balcony or rooftop garden. It gives no weight "
                 "figure."},
    {"id": "container_material", "anchors": {"csu_ext": "csu_gardens", "uiuc_ext": "uiuc_vegcont"},
     "evidence": [
         ("csu_gardens", "About any container can be used including clay (often called terra cotta), "
                         "plastic pots, wood barrels, wire baskets lined with sphagnum moss or coconut "
                         "coir, planter boxes, ceramic pots (often found in bold colors), and even "
                         "cement blocks."),
         ("csu_gardens", "However, make sure you never use a container that holds toxic materials, "
                         "especially if edible plants are going to be grown."),
         ("uiuc_vegcont", "The container needs to have good drainage, and should not contain "
                          "chemicals that are toxic to plants and human beings."),
         ("uiuc_material", "Exercise caution with treated lumber when growing food, or where toddlers "
                           "are concerned.")],
     "title": "Never grow food in a container with anything toxic in it",
     "beginner": "Many kinds of containers can be used. Whatever you choose, keep anything toxic out "
                 "of it, especially if you are growing food.",
     "seasoned": "Colorado State accepts nearly any container material but warns against using a "
                 "container that holds toxic materials, especially for edible plants. Illinois adds "
                 "that a vegetable container should be free of chemicals toxic to plants or people, "
                 "and urges caution with treated lumber when growing food. If you cannot account for "
                 "what a repurposed container once held, that alone is a reason to keep food out of "
                 "it.",
     "inference": "The last sentence of the seasoned body is a DECLARED INFERENCE (spec section 14): "
                  "a history nobody can verify cannot be shown to meet the rule the sources state."},
    {"id": "hanging_security", "anchors": {"uiuc_ext": "uiuc_material"},
     "evidence": [
         ("uiuc_material", "Examples are a hanging basket, window, fence or rail box."),
         ("uiuc_material", "Secure hanging items well and consider potential safety issues when "
                           "hanging."),
         ("uiuc_material", "It may drip on people or possessions below."),
         ("uiuc_material", "Consider this when determining placement of a hanging container.")],
     "title": "Secure hanging containers well",
     "beginner": "Fasten hanging baskets and window or rail boxes securely. Think about what is below "
                 "them too, since they can drip on people or things underneath.",
     "seasoned": "Illinois Extension asks growers to secure hanging containers well and to think "
                 "through the safety issues of hanging them. Placement matters too, since a hanging "
                 "container can drip onto people or belongings below."},
]

# CUT by the section 4.5 evidence test. Recorded so each omission is a decision in the artifact.
CUT = [
    {"candidate": "mosquito",
     "why": "The only source (uiuc_ext, problems-algae-and-mosquitoes) sits under Container Water "
            "Gardens and opens 'Mosquitoes only become a problem in water garden containers that "
            "are not maintained'; every remedy presupposes standing water that is the point of the "
            "container. Nothing supports a saucer-under-a-pot version. Spec 4.5."},
    {"candidate": "lifting",
     "why": "csu_ext's 'the weight may be too much to lift easily' is advice about MOVING a pot, a "
            "handling hazard rather than a safety one; it belongs in container prose if anywhere. "
            "Spec 4.4."},
    {"candidate": "pounds_figure",
     "why": "No source read publishes a potting-mix weight per gallon or a pounds-per-pot load "
            "(eleven extension domains searched); Illinois refers the question to an architect. A "
            "rendered number would be fabricated. Spec 2.6."},
]


def norm(b):
    t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", b.decode("utf-8", "replace"))
    t = _html.unescape(re.sub(r"<[^>]+>", " ", t))
    return re.sub(r"\s+", " ", t.replace("’", "'").replace(" ", " "))


def read_page(key):
    bodies = []
    for a in AGENTS:
        p = os.path.join(RAW, f"{key}.{a}")
        if not os.path.exists(p):
            raise SystemExit(f"REFUSED: {p} missing; run the two-agent fetch first")
        bodies.append(open(p, "rb").read())
    if bodies[0] != bodies[1]:
        raise SystemExit(f"REFUSED: {key} differs between user-agents "
                         f"({len(bodies[0])} vs {len(bodies[1])} bytes); read both before trusting either")
    b = bodies[0]
    if len(b) < 5000:
        raise SystemExit(f"REFUSED: {key} is {len(b)} bytes, a block page rather than the article")
    src, url = PAGES[key]
    return {"source": src, "url": url, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(),
            "text": norm(b)}


def build():
    pages = {k: read_page(k) for k in PAGES}
    warnings, records, evidence = [], [], {}
    for w in WARNINGS:
        for k, sentence in w["evidence"]:
            if sentence not in pages[k]["text"]:
                raise SystemExit(f"REFUSED: {w['id']}: {k} does not carry the sentence {sentence!r}")
        srcs = list(w["anchors"])
        warnings.append({
            "id": w["id"], "class": "safety", "severity": "high", "stage": None, "title": w["title"],
            "body_seasoned": w["seasoned"], "body_beginner": w["beginner"], "sources": srcs,
            "anchoring_urls": {s: {"url": pages[k]["url"], "verified": FETCH_DATE}
                               for s, k in w["anchors"].items()}})
        evidence[w["id"]] = [{"url": pages[k]["url"], "sentence": sent} for k, sent in w["evidence"]]
        cites = []
        for k in dict.fromkeys(k for k, _ in w["evidence"]):
            p = pages[k]
            quoted = " ".join(f"\"{sent}\"" for kk, sent in w["evidence"] if kk == k)
            cites.append(f"{INSTITUTION[p['source']]}, {p['url']} (raw read {FETCH_DATE}, {p['bytes']} "
                         f"bytes, sha256 {p['sha256']}); verbatim: {quoted}"
                         + (f" {DRIFT[k]}" if k in DRIFT else ""))
        # A record credits exactly the institutions the warning anchors; evidence from an institution
        # the warning does not cite would be a credit with no anchor behind it.
        if {pages[k]["source"] for k, _ in w["evidence"]} != set(srcs):
            raise SystemExit(f"REFUSED: {w['id']} evidence spans "
                             f"{sorted({pages[k]['source'] for k, _ in w['evidence']})}, anchors {srcs}")
        records.append({
            "field": f"container_safety.{w['id']}", "date": FETCH_DATE, "sources": srcs,
            "note": f"PLA-581 container_safety.{w['id']}. " + " ".join(cites)
                    + (f" {w['inference']}" if "inference" in w else "")
                    + " Severity is high on all three warnings, MODELED and uniform: no source grades "
                      "them, so no ranking is claimed. Authored once at dataset level and rendered on "
                      "every container_ok crop; no figure appears in the copy because no source "
                      "publishes one."})
    return {
        "_what": "PLA-581 container_safety + evidence + the cut ledger; built by build_spec.py from _raw/ bytes",
        "base_sha": BASE_SHA, "fetch_date": FETCH_DATE,
        "pages": {k: {kk: v for kk, v in p.items() if kk != "text"} for k, p in pages.items()},
        "evidence": evidence,
        "container_safety": {"warnings": warnings, "field_additions": records},
        "cut": CUT,
        "expected": {"certified_null": 121, "shells": 7, "warnings": 3, "records": 3, "pages": 4},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="src", default=None)
    a = ap.parse_args()
    if a.src:
        os.makedirs(RAW, exist_ok=True)
        for k in PAGES:
            for ag in AGENTS:
                shutil.copy2(os.path.join(a.src, f"{k}.{ag}"), os.path.join(RAW, f"{k}.{ag}"))
    spec = build()
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False, indent=1)
        f.write("\n")
    for k, p in spec["pages"].items():
        print(f"  {k:14s} {p['source']:9s} {p['bytes']:7d} bytes  sha256 {p['sha256']}")
    for wid, ev in spec["evidence"].items():
        print(f"  {wid:20s} {len(ev)} evidence sentence(s), all present in their pages")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    sys.exit(main())
