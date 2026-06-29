#!/usr/bin/env python3
"""daily_review_handoff.py -- package a day's authored crops for the biology-fidelity review.

The human-in-the-loop model (Trevor 2026-06-28): bots author ~5-10 crops/day; a daily claude.ai
pass runs the biology-fidelity judge (docs/kickoffs/02-biology-fidelity-llm-judge/) over them and
Trevor works the findings. This helper builds that day's review package -- the selected crop records
plus the shared source_catalog + region_chill_delivered the judge needs as context -- and prints the
ready-to-paste daily prompt.

Two ways to pick the day's batch:
  by slug (you know what you authored):
    python3 tools/daily_review_handoff.py rutabaga kohlrabi parsnip
  by git delta (everything whose crop record changed since a ref/SHA -- e.g. yesterday's review):
    python3 tools/daily_review_handoff.py --since <git-ref-or-SHA>

Writes the package to review_batch.json (override with --out) and prints the prompt. READ-ONLY:
never writes crops_data_final.json.
"""
import argparse
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(ROOT, "crops_data_final.json")


def changed_since(ref):
    """Slugs whose crop record differs from the canonical at <ref>."""
    out = subprocess.run(["git", "show", f"{ref}:crops_data_final.json"],
                         cwd=ROOT, capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit(f"daily_review_handoff: cannot read crops_data_final.json at {ref!r}:\n{out.stderr}")
    base = {c["slug"]: c for c in json.loads(out.stdout).get("crops", [])}
    cur = {c["slug"]: c for c in json.load(open(CANON, encoding="utf-8")).get("crops", [])}
    changed = [s for s, c in cur.items()
               if json.dumps(c, sort_keys=True) != json.dumps(base.get(s), sort_keys=True)]
    return changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slugs", nargs="*", help="the crops authored today (by slug)")
    ap.add_argument("--since", help="git ref/SHA; pick every crop whose record changed since it")
    ap.add_argument("--out", default=os.path.join(ROOT, "review_batch.json"))
    a = ap.parse_args()

    data = json.load(open(CANON, encoding="utf-8"))
    by_slug = {c["slug"]: c for c in data["crops"]}

    if a.since:
        slugs = changed_since(a.since)
    elif a.slugs:
        slugs = a.slugs
    else:
        sys.exit("daily_review_handoff: give crop slugs, or --since <ref>. (-h for help)")

    missing = [s for s in slugs if s not in by_slug]
    if missing:
        sys.exit(f"daily_review_handoff: not in the dataset: {missing}")
    if not slugs:
        print("daily_review_handoff: no crops in the batch (nothing changed since --since). Nothing to review.")
        return

    pkg = {
        "_note": "Daily biology-fidelity review batch. Apply the biology_fidelity_judge_v1_0.md "
                 "rubric to each crop below; source_catalog + region_chill_delivered are context.",
        "crops": [by_slug[s] for s in slugs],
        "source_catalog": data.get("source_catalog", {}),
        "region_chill_delivered": data.get("region_chill_delivered", {}),
    }
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(pkg, f, ensure_ascii=False, indent=2)

    rel = os.path.relpath(a.out, ROOT)
    print(f"== Daily review package written: {rel}  ({len(slugs)} crop(s): {', '.join(slugs)}) ==\n")
    print("Paste this into the daily claude.ai review (with biology_fidelity_judge_v1_0.md + the")
    print(f"package {rel} attached):\n")
    print("-" * 78)
    print(DAILY_PROMPT.format(n=len(slugs), slugs=", ".join(slugs)))
    print("-" * 78)


DAILY_PROMPT = """\
Daily biology-fidelity review of {n} newly-authored crop(s): {slugs}.

Apply the attached biology_fidelity_judge_v1_0.md rubric (all 8 dimensions) to EACH crop in the
attached review_batch.json -- one crop per pass, using the crop's slug/name as the identity anchor
and source_catalog + region_chill_delivered as context. These are bot-authored, NOT the calibrated
18, so flag real issues; the carve-outs (colloquial-but-correct rotation family, []/null N/A,
catalogued T2) still apply so you don't cry wolf.

For each crop emit the structured findings rows the rubric specifies (crop, dimension, field_path,
observation, why_it_is_wrong, confidence, suggested_correction, routes_to). Lead with the
high/medium-confidence findings -- especially D1 family coherence, D2 calendar-vs-climate, D3
numeric species-fitness, D5 pause-physiology, D4 source-plausibility, D15-style wrong-species/
copy-template tells. A crop with no findings is a clean pass; say so explicitly.

End with: a one-line per-crop verdict (clean / needs-fixes), and the short list of fixes to bring
back to the Claude Code lane to apply.
"""


if __name__ == "__main__":
    main()
