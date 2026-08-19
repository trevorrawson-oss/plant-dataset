#!/usr/bin/env python3
"""PLA-220 -- draw the n=40 reading sample, per the selection rule filed 2026-08-19.

THE RULE IS NOT THIS SCRIPT'S TO CHOOSE. It was written on PLA-220 BEFORE any record was
drawn, precisely so the draw could not inherit an unwritten choice. This file executes it
and nothing else; every parameter below is a transcription, and each one is asserted at
runtime so a silent drift from the filed rule fails loudly instead of producing a
plausible-looking sample.

  frame              2,358 records, tools/staging/pla220_borderline_frame/_all_records.jsonl
  exclude            the `sources_summary` document-name records (PLA-202 class B5,
                     citation furniture: a title matching a title is attribution working)
  eligible           2,190
  sort               (crop_slug, field_path, source_url)  -- a total order; the frame holds
                     exactly one record per such triple, so the sort is deterministic
  method             systematic interval
  n                  40
  interval           54.75  (== 2190/40 exactly)
  first index        27
  weighting          none
  duplicate fields   KEPT -- the unit is the hit, not the field

INDEXING, stated because the rule does not: indices are ZERO-BASED and taken as
floor(27 + k*54.75) for k in 0..39. Zero-based with a start of 27 puts the draw at the
midpoint of the first interval (54.75/2 = 27.375 -> 27), which is the standard systematic
start and the reading that makes 27 a principled number rather than an arbitrary one. A
one-based reading would shift every draw by exactly one record; the report says so, and
`--one-based` reproduces it for audit.

Usage:
  python3 tools/pla220_draw_sample.py [--out=PATH] [--one-based]
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FRAME = os.path.join(HERE, "staging", "pla220_borderline_frame", "_all_records.jsonl")
OUT = os.path.join(HERE, "staging", "pla220_sample_n40.md")

N = 40
INTERVAL = 54.75
FIRST = 27
EXPECT_FRAME = 2358
EXPECT_EXCLUDED = 168
EXPECT_ELIGIBLE = 2190

flags = [a for a in sys.argv[1:] if a.startswith("--")]
ONE_BASED = "--one-based" in flags
for f in flags:
    if f.startswith("--out="):
        OUT = f.split("=", 1)[1]

records = [json.loads(l) for l in open(FRAME, encoding="utf-8")]
assert len(records) == EXPECT_FRAME, f"frame is {len(records)}, rule was written against {EXPECT_FRAME}"


def top_level(path):
    return path.split(".")[0].split("[")[0]


def leaf(path):
    return path.split(".")[-1].split("[")[0]


# --- the exclusion, applied on the rule's own terms and cross-checked both ways ---
# The rule names "sources_summary.name and its kin". Measured at this frame the two
# candidate readings -- "leaf key is `name`" and "path is under sources_summary and the
# leaf is `name`" -- select the IDENTICAL 168 records: every name-leaf record in the frame
# lives under sources_summary, and there are no other kin. The two `sources_summary.note`
# records (elderberry, against two URLs) are prose, not a document title, and stay eligible.
by_leaf = {id(r) for r in records if leaf(r["field_path"]) == "name"}
by_path = {id(r) for r in records
           if top_level(r["field_path"]) == "sources_summary" and leaf(r["field_path"]) == "name"}
assert by_leaf == by_path, (
    f"the two readings of the filed exclusion disagree: {len(by_leaf)} vs {len(by_path)}. "
    "The rule says 'sources_summary.name and its kin'; if these ever diverge the ambiguity "
    "is real and must be ruled on PLA-220, not resolved here.")
excluded = [r for r in records if id(r) in by_leaf]
eligible = [r for r in records if id(r) not in by_leaf]
assert len(excluded) == EXPECT_EXCLUDED, f"excluded {len(excluded)}, rule states {EXPECT_EXCLUDED}"
assert len(eligible) == EXPECT_ELIGIBLE, f"eligible {len(eligible)}, rule states {EXPECT_ELIGIBLE}"
assert abs(len(eligible) / N - INTERVAL) < 1e-9, "interval is not N_eligible/n -- the rule's arithmetic moved"

eligible.sort(key=lambda r: (r["crop_slug"], r["field_path"], r["source_url"]))

base = 1 if ONE_BASED else 0
idx = [math.floor(FIRST + k * INTERVAL) for k in range(N)]
assert len(set(idx)) == N, "systematic indices collided"
assert max(idx) - base < len(eligible), f"index {max(idx)} runs past the eligible population"
drawn = [eligible[i - base] for i in idx]


def block(i, pos, r):
    L = []
    L.append(f"## {i}. `{r['crop_slug']}`  ---  `{r['field_path']}`")
    L.append("")
    L.append(f"*sample {i} of {N}  |  eligible index {pos}  |  run_words {r['run_words']}*")
    L.append("")
    L.append("**Our prose, complete:**")
    L.append("")
    L.append("> " + r["our_prose"].replace("\n", "\n> "))
    L.append("")
    L.append(f"**Maximal shared run ({r['run_words']} words), as matched:**")
    L.append("")
    L.append(f"`{r['run_normalized']}`")
    L.append("")
    L.append("**The same run as written in our prose:**")
    L.append("")
    L.append(f"`{r['run_in_our_prose']}`")
    L.append("")
    if r["maximal_run_count"] > 1:
        L.append(f"**All {r['maximal_run_count']} maximal runs:**")
        L.append("")
        for g in r["all_maximal_runs"]:
            L.append(f"- `{g}`")
        L.append("")
    L.append("**Source:**")
    L.append("")
    for j, sid in enumerate(r["source_ids"]):
        nm = r["source_names"][j] if j < len(r["source_names"]) else ""
        pub = r["source_publishers"][j] if j < len(r["source_publishers"]) else ""
        tier = r["source_tiers"][j] if j < len(r["source_tiers"]) else ""
        L.append(f"- `{sid}` --- {nm} ({pub}) --- tier {tier}")
    L.append(f"- URL: <{r['source_url']}>")
    L.append("")
    L.append("**Anchored at:**")
    L.append("")
    for ap in r["anchor_paths"]:
        L.append(f"- `{ap}`")
    L.append("")
    L.append("**Source context (+/- one sentence in the cached document):**")
    L.append("")
    L.append("> " + r["source_context"].replace("\n", "\n> "))
    L.append("")
    L.append("**Ruling:** _(unruled -- B1-B6 benign, R1 attributed near-quote, R2 unattributed lift)_")
    L.append("")
    L.append("**Reasoning:**")
    L.append("")
    L.append("---")
    L.append("")
    return "\n".join(L)


head = [
    "# PLA-220 --- the n=40 reading sample",
    "",
    f"Drawn 2026-08-19 from canonical `394bb8bd`, under the selection rule filed on PLA-220 "
    f"**before** any record was drawn. **Nothing here is ruled yet.**",
    "",
    "## The draw, reproduced",
    "",
    "| | |",
    "| -- | -- |",
    f"| Frame | {len(records):,} records (`tools/staging/pla220_borderline_frame/_all_records.jsonl`) |",
    f"| Excluded | {len(excluded)} --- the `sources_summary` document-name records (PLA-202 class B5) |",
    f"| Eligible | {len(eligible):,} |",
    "| Sort | `(crop_slug, field_path, source_url)` |",
    "| Method | systematic interval |",
    f"| n | {N} |",
    f"| Interval | {INTERVAL} (= {len(eligible)}/{N} exactly) |",
    f"| First index | {FIRST} ({'one' if ONE_BASED else 'zero'}-based) |",
    "| Weighting | none |",
    "| Duplicate fields | kept |",
    "",
    "**Indices drawn:** " + ", ".join(str(i) for i in idx),
    "",
    "## The standard being applied",
    "",
    "PLA-202 §3, unchanged, so results stay commensurable with its 308-benign / 25-rewrite "
    "adjudication:",
    "",
    "> Does our prose reproduce the source's EXPRESSION beyond what stating the fact requires?",
    "",
    "Read each hit in its own source context. **No ruling by pattern across a family.**",
    "",
    "## Read this before quoting any rate",
    "",
    "The frame is a **floor, not a total**: 3,142 of 3,355 cited crop/URL slots were readable, "
    "**213 are not, across 66 crops**. At n=40 an observed rate near 8% carries roughly "
    "**+/-8 percentage points at 95% confidence** --- enough to tell \"a few percent\" from "
    "\"a third,\" not enough for a tight number.",
    "",
    "---",
    "",
]

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(head))
    for i, (pos, r) in enumerate(zip(idx, drawn), start=1):
        fh.write(block(i, pos, r))

print(f"frame {len(records)} | excluded {len(excluded)} | eligible {len(eligible)} "
      f"| drawn {len(drawn)} ({'one' if ONE_BASED else 'zero'}-based)")
print(f"indices: {idx[0]}, {idx[1]}, {idx[2]}, ..., {idx[-1]}")
print(f"crops represented: {len({r['crop_slug'] for r in drawn})}")
print(f"run_words: 6 -> {sum(1 for r in drawn if r['run_words']==6)}, "
      f"7 -> {sum(1 for r in drawn if r['run_words']==7)}")
print(f"-> {OUT}  ({os.path.getsize(OUT):,} bytes)")
