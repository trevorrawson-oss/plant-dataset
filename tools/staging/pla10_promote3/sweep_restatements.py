#!/usr/bin/env python3
"""sweep_restatements -- PLA-10 promote 3 session 2: the WIDER sweep for height restatements that the promote's
height_strings() cannot see (a feet/foot figure with no height word in its sentence: "reaches 3 to 6 feet",
"2 to 4 foot stems", "a 3-to-6-foot clump"). Prints, per authored crop, every leaf the scanner missed. Hand-tuned,
not a gate; the finding is PLA-655. Usage: python3 tools/staging/pla10_promote3/sweep_restatements.py"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, HERE)
import promote_pla10_promote3 as P  # noqa: E402
from pla10_promote_common import SKIP_SUBTREES, fmt  # noqa: E402
import rows  # noqa: E402

FT = re.compile(r"\d+(?:\.\d+)?(?:\s*(?:to|-|–|or)\s*\d+(?:\.\d+)?)?\s*(?:-\s*)?(?:feet|foot|ft\b|ft\.)", re.I)
GROWTH = re.compile(r"\b(reach|grow|stem|stalk|stand|plant|tall|clump|vine|bush|size|big|large)", re.I)
NOT_HEIGHT = re.compile(r"\b(apart|rows?|spac|between|deep|row)\b", re.I)


def main():
    d = json.load(open(os.path.join(REPO, "crops_data_final.json"), encoding="utf-8"))
    idx = {c["slug"]: c for c in d["crops"]}
    for slug, (h, s, _ev, _dec) in rows.ROWS.items():
        if h is None and s is None:
            continue
        hits = set(P.height_strings(idx[slug], s is not None))
        out = []

        def walk(o, path):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k in SKIP_SUBTREES or k.endswith(("_sources", "_anchoring_urls")):
                        continue
                    walk(v, path + [k])
            elif isinstance(o, list):
                for i, v in enumerate(o):
                    walk(v, path + [i])
            elif isinstance(o, str):
                p = fmt(path)
                if p in hits:
                    return
                for sent in re.split(r"(?<=[.;!?])\s+", o):
                    if FT.search(sent) and GROWTH.search(sent) and not NOT_HEIGHT.search(sent):
                        out.append((p, sent[:220]))
                        break
        walk(idx[slug], [])
        for p, sent in out:
            print(f"{slug:18} {p}\n     {sent}")


if __name__ == "__main__":
    main()
