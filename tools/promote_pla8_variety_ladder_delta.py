#!/usr/bin/env python3
"""PLA-8 Round 2: the variety-level control-ladder delta pilot (apple + strawberry). Base 20a32c47.

WHAT THIS ADDS, AND WHY IT ADDS NOTHING ELSE. Each graded variety gains ONE new key,
`ladder_delta`, keyed by the parent problem's `id` and then by rung `method`. No crop-level field
moves, no `control_ladder` is edited, no source id is minted, and `source_catalog` and
`control_methods` come out byte-identical -- every delta is RESTATED from a `resistance` grade the
crop already asserts, so it inherits that grade's T1 anchors rather than needing new ones.

THE DEFECT IT FIXES. `control_methods.resistant_varieties` is rung 0 on 9 of the 20 laddered
problems across these two crops, and its note tells the reader to *choose a resistant variety* --
advice aimed at somebody who, by the time they are reading a variety page, has already chosen. On a
resistant variety that rung is already satisfied and says so nowhere; on a susceptible one it is
spent advice sitting at the top of the ladder, telling a Gala owner to go buy a Liberty. 62 of 62
graded variety x problem pairs were affected.

SIX CLASSES, 94 rung operations, generated from six authored dual-register patterns rather than 62
hand-written deltas (tools/build_variety_ladder_delta_content.py):

  R0-INVERTED        37  susceptible: rung 0 reframed as load-bearing, with a PER-DISEASE
                         consequence. A single generic clause was the first draft and was false on
                         five of seven: red stele and verticillium kill whole plants, fire blight
                         kills wood, neither "shows up in the fruit".
  R0-SATISFIED       25  the reader already completed rung 0 by choosing this variety; wording
                         tracks the grade, since immune / resistant / tolerant are three different
                         promises.
  DROP               13  immune or resistant: the escalation rung comes out. Anchored on UMN
                         Extension's own instruction, "Do not use fungicides: On apple and
                         crabapple varieties that are resistant or immune to apple scab."
  CONDITIONAL-SPENT  13  apple scab's sulfur rung still opens "If you grow a susceptible
                         variety..." on the page of a variety just declared susceptible.
  SOFTEN              6  tolerant: the escalation rung moves from schedule to response.
  GRADE-DISAGREEMENT  1  honeycrisp/apple-scab. UMN rates it resistant, Purdue MR. The conservative
                         MR reading is carried AND the split is stated in the prose (Trevor,
                         2026-08-22), because a reader told only the safer of two ratings has a
                         fact, while a reader told the raters differ has the evidence.

PURDUE'S HEDGE IS CARRIED, NOT COMPRESSED AWAY ("resistance is not immunity"), on every resistant
and tolerant delta -- except where a specific source-disagreement note supersedes it, which would
otherwise state the same caution twice with the vaguer version first.

REFUSALS (each is a live path, exercised by the suite): base SHA mismatch; staged-content SHA
mismatch; an unknown crop or variety; a `ladder_delta` that already exists; a problem id that is not
laddered on that crop; a rung method absent from the parent ladder; an empty delta.

Guard suite:      tools/test_promote_pla8_variety_ladder_delta.py
Mutation harness: tools/mutate_pla8_ladder_delta_suite.py (PLA-215, liveness-defended)

Usage: python3 tools/promote_pla8_variety_ladder_delta.py [--apply] [--dry-run] [--expect-sha SHA]
"""
import argparse
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
CONTENT = os.path.join(REPO, "tools", "staging", "pla8_ladder_delta_content.json")

BASE_SHA = "20a32c47f0bf861e5b93fad71b9af3bbb37643afdb70dccd758e1ee0eb080ea9"
# The staged content is pinned by hash: staging is a working directory, and a promote that reads it
# unpinned would silently ship whatever happened to be sitting there.
CONTENT_SHA = "2eceb152c1d51e72ae7ed578fd936257d214dec8c3f52fd2015cc0835fb679eb"

CROPS = ("apple", "strawberry")
DELTA_KEY = "ladder_delta"


def load_content(path=CONTENT, expect=CONTENT_SHA):
    raw = open(path, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    if expect and sha != expect:
        raise SystemExit(f"ABORT: staged content SHA mismatch\n  expected {expect}\n  found    {sha}")
    return json.loads(raw.decode("utf-8"))


def _laddered(crop):
    out = {}
    for fam in ("pests", "diseases"):
        for p in crop.get(fam) or []:
            if isinstance(p, dict) and isinstance(p.get("id"), str) and p.get("control_ladder"):
                out[p["id"]] = p
    return out


def check(data, content):
    """Every refusal this promote can raise, before a single byte is changed."""
    by = {c["slug"]: c for c in data["crops"]}
    for slug in content:
        if slug not in CROPS:
            return f"content names {slug!r}, which is outside the pilot scope {CROPS}"
        if slug not in by:
            return f"no crop {slug!r} in canonical"
        crop = by[slug]
        ladders = _laddered(crop)
        varieties = {v["id"]: v for v in crop["varieties"]["recommended"]
                     if isinstance(v, dict) and v.get("id")}
        for vid, delta in content[slug].items():
            if vid not in varieties:
                return f"{slug}: no variety {vid!r}"
            if DELTA_KEY in varieties[vid]:
                return f"{slug}/{vid}: {DELTA_KEY} already exists; this promote creates it"
            if not delta:
                return f"{slug}/{vid}: empty {DELTA_KEY}"
            for pid, entry in delta.items():
                if pid not in ladders:
                    return f"{slug}/{vid}: {pid!r} is not a laddered problem id on {slug}"
                if not entry.get("rungs"):
                    return f"{slug}/{vid}/{pid}: no rungs"
                parent = {r["method"] for r in ladders[pid]["control_ladder"]}
                for r in entry["rungs"]:
                    if r.get("op") in ("drop", "replace") and r.get("method") not in parent:
                        return (f"{slug}/{vid}/{pid}: rung method {r.get('method')!r} is not in "
                                f"the parent ladder")
                # a delta that claims the resistance basis must have a grade behind it
                if entry.get("basis") == "resistance":
                    grades = varieties[vid].get("resistance") or {}
                    if pid not in grades:
                        return (f"{slug}/{vid}/{pid}: basis 'resistance' but the variety carries "
                                f"no grade for it")
    return None


def serialize(data):
    """THE single serialization path. The guard suite must call THIS, not its own json.dumps:
    the mutation harness caught the first version of `test_output_is_compact` re-implementing the
    dump, so it was grading its own call and an `indent=1` mutation in main() survived untouched.
    A guard for the write path has to go through the write path."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def apply_to(data, content):
    by = {c["slug"]: c for c in data["crops"]}
    n = 0
    for slug, per in content.items():
        varieties = {v["id"]: v for v in by[slug]["varieties"]["recommended"]
                     if isinstance(v, dict) and v.get("id")}
        for vid, delta in per.items():
            varieties[vid][DELTA_KEY] = delta
            n += 1
    return n


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("canonical", nargs="?", default=CANONICAL)
    ap.add_argument("--content", default=CONTENT)
    ap.add_argument("--expect-sha", default=BASE_SHA)
    ap.add_argument("--expect-content-sha", default=CONTENT_SHA)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    raw = open(args.canonical, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != args.expect_sha:
        print(f"ABORT: base SHA mismatch\n  expected {args.expect_sha}\n  found    {sha}",
              file=sys.stderr)
        return 1

    content = load_content(args.content, args.expect_content_sha)
    data = json.loads(raw.decode("utf-8"))

    problem = check(data, content)
    if problem:
        print("ABORT: " + problem, file=sys.stderr)
        return 1

    n = apply_to(data, content)
    ops = sum(len(e["rungs"]) for per in content.values() for d in per.values() for e in d.values())
    entries = sum(len(d) for per in content.values() for d in per.values())
    print(f"PLA-8 Round 2 -- variety ladder deltas")
    for slug in sorted(content):
        print(f"  {slug:12s} {len(content[slug]):2d} varieties, "
              f"{sum(len(d) for d in content[slug].values()):2d} problem entries")
    print(f"  TOTAL        {n} varieties, {entries} problem entries, {ops} rung operations")

    out = serialize(data)
    new_sha = hashlib.sha256(out).hexdigest()
    if args.dry_run or not args.apply:
        print(f"DRY RUN -- would write {len(out)} bytes, sha {new_sha}")
        return 0
    with open(args.canonical, "wb") as fh:
        fh.write(out)
    print(f"wrote {len(out)} bytes\nnew canonical SHA: {new_sha}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
