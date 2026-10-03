#!/usr/bin/env python3
"""Rebuild the three PLA-140 umn_ext prep JSONs from canonical be8a6d1e.

Reads `git show 8118eaa:crops_data_final.json` (run from the plant-dataset repo
root) and writes, into the output dir given as argv[1]:

  citations_umn_ext.json       every list under a key named sources / source_set /
                               zone_citations that contains the EXACT string
                               "umn_ext" (not the umn_ext_* children), per crop.
  umn_deep_link_register.json  every distinct umn.edu URL in an `anchoring_urls`
                               dict (crops + top-level objects), excluding the
                               catalog's own umn_ext URL (the dead /vegetables page).
  cert_log_umn_mentions.json   per crop citing umn_ext, the sentences of
                               verification_log_ref / verification_log that
                               mention UMN.

Stdlib only. Output format: json.dump(indent=1), no trailing newline.
"""
import collections
import hashlib
import json
import os
import re
import subprocess
import sys

COMMIT = "8118eaa"
EXPECTED_SHA_PREFIX = "be8a6d1e"
SITE_KEYS = {"sources", "source_set", "zone_citations"}
TOP = "<TOP-LEVEL>"


def fmt(path):
    s = ""
    for x in path:
        if isinstance(x, int):
            s += "[%d]" % x
        else:
            s += ("." if s else "") + x
    return s


def family(path):
    return re.sub(r"\[\d+\]", "[]", fmt(path))


def load():
    raw = subprocess.run(["git", "show", COMMIT + ":crops_data_final.json"],
                         check=True, capture_output=True).stdout
    sha = hashlib.sha256(raw).hexdigest()
    if not sha.startswith(EXPECTED_SHA_PREFIX):
        raise SystemExit("canonical sha256 %s does not start %s" % (sha, EXPECTED_SHA_PREFIX))
    return json.loads(raw)


def citations(d):
    rows = []

    def walk(o, p, crop, parent):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, p + [k], crop, o)
        elif isinstance(o, list):
            if p and p[-1] in SITE_KEYS and "umn_ext" in o:
                a = None
                if isinstance(parent, dict):
                    a = (parent.get("anchoring_urls") or {}).get("umn_ext")
                if not isinstance(a, dict):
                    a = {}
                rows.append({
                    "crop": crop,
                    "path": fmt(p),
                    "family": family(p),
                    "anchor_url": a.get("url"),
                    "anchor_verified": a.get("verified"),
                    "co_cited": [x for x in o if x != "umn_ext"],
                })
            for i, v in enumerate(o):
                walk(v, p + [i], crop, o)

    for c in d["crops"]:
        walk(c, [], c["slug"], None)
    return rows


def register(d):
    dead = d["source_catalog"]["umn_ext"]["url"]
    pl = []  # (crop, url, catalog_id, verified, family)

    def walk(o, p, crop):
        if isinstance(o, dict):
            # pre-order: a container's own anchors before its children's
            au = o.get("anchoring_urls")
            if isinstance(au, dict):
                for cid, a in au.items():
                    if isinstance(a, dict):
                        u = a.get("url") or ""
                        if "umn.edu" in u and u != dead:
                            pl.append((crop, u, cid, a.get("verified"), family(p)))
            for k, v in o.items():
                walk(v, p + [k], crop)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, p + [i], crop)

    for c in d["crops"]:
        walk(c, [], c["slug"])
    for k, v in d.items():
        if k != "crops":
            walk(v, [k], TOP)

    by = collections.defaultdict(list)
    for x in pl:
        by[x[1]].append(x)
    out = []
    for u, n in collections.Counter(x[1] for x in pl).most_common():
        xs = by[u]
        vd = sorted(x[3] for x in xs if x[3])
        out.append({
            "url": u,
            "placements": n,
            "catalog_ids": sorted({x[2] for x in xs}),
            "crops": sorted({x[0] for x in xs}),
            "verified_dates": [vd[0], vd[-1]] if vd else [],
            "claim_families": [f for f, _ in collections.Counter(x[4] for x in xs).most_common()],
        })
    return out


# FITTED heuristic: reproduces all 57 original labels, but the original rule was
# not saved; this is the narrowest keyword set found that matches every label.
NAMES_DOC_OR_REPAIR = re.compile(r"dead|404|URL|fetchable|[Gg]rowing ")


def cert_log(d, citing):
    out = []
    for c in d["crops"]:
        if c["slug"] not in citing:
            continue
        vs = c.get("verification_status") or {}
        for f in ("verification_log_ref", "verification_log"):
            t = vs.get(f)
            texts = [t] if isinstance(t, str) else [x for x in (t or []) if isinstance(x, str)] if isinstance(t, list) else []
            hits = []
            for text in texts:
                hits += [s for s in re.split(r"(?<=[.;])\s+", text) if re.search(r"UMN|umn", s)]
            if hits:
                out.append({
                    "crop": c["slug"],
                    "field": f,
                    "umn_sentences": hits,
                    "names_document_or_repair": any(NAMES_DOC_OR_REPAIR.search(s) for s in hits),
                })
    return out


def dump(obj, path):
    with open(path, "w") as fh:
        json.dump(obj, fh, indent=1)


def main():
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    d = load()
    cites = citations(d)
    dump(cites, os.path.join(outdir, "citations_umn_ext.json"))
    dump(register(d), os.path.join(outdir, "umn_deep_link_register.json"))
    dump(cert_log(d, {r["crop"] for r in cites}), os.path.join(outdir, "cert_log_umn_mentions.json"))


if __name__ == "__main__":
    main()
