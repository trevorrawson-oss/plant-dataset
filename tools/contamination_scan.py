#!/usr/bin/env python3
"""Dataset-wide bucket/blanket-data contamination scan.

WHY: early authoring validated data point-by-point ACROSS all ~123 crops at once
(e.g. "all plant-out dates") -- a bucket process that smeared blanket values across
many crops, much of it wrong. The per-crop gold-standard arc (Step 5 side-by-side)
is what confers verified status; only crops that have walked the arc are trustworthy.

This tool DETECTS the contamination surface (cheap, dataset-wide). It does NOT verify
truth (that is irreducibly per-crop -- bucket-verification is what caused the mess).

A measured leaf is "shared" when its value is byte-identical to the same crop-relative
path on >=1 OTHER crop. Shared-AND-the-crop-never-walked-the-arc == candidate bucket
data to re-derive per-crop. Shared-but-walked == fine (a verified value may legitimately
coincide; verification is about provenance, not uniqueness).

Output: per-crop contamination ratios (ranked), the bucket clusters, and a GS-clean
check. This map is also the candidate-vs-verified signal the future pipeline/bots need.

Usage: python3 tools/contamination_scan.py [crops_data_final.json] [--md OUT.md]
"""
import json, sys, collections

PATH = "crops_data_final.json"
OUT_MD = None
args = sys.argv[1:]
i = 0
while i < len(args):
    if args[i] == "--md":
        OUT_MD = args[i + 1]; i += 2
    else:
        PATH = args[i]; i += 1

data = json.load(open(PATH))
crops = data["crops"]
by_slug = {c["slug"]: c for c in crops}

# crops that have walked the per-crop arc (verified). Derive from the dataset, not a
# hardcoded list: status verified_gs_arc OR both launch_ready flags true.
def is_walked(c):
    vs = c.get("verification_status", {}) or {}
    return vs.get("status") == "verified_gs_arc" or (
        vs.get("launch_ready_core") and vs.get("launch_ready_seasoned"))
walked = {c["slug"] for c in crops if is_walked(c)}

def walk(o, path, out):
    if isinstance(o, dict):
        for k, v in o.items():
            walk(v, f"{path}.{k}" if path else k, out)
    elif isinstance(o, list):
        for idx, x in enumerate(o):
            walk(x, f"{path}[{idx}]", out)
    else:
        out[path] = o

leaf_index = {}
for c in crops:
    d = {}; walk(c, "", d); leaf_index[c["slug"]] = d

# ---- measured-surface predicates (positive include-list; benign scaffolding excluded) ----
BIO_SECTIONS = ("pests[", "diseases[", "growth_stages[", "tips_by_stage",
                "failure_diagnostics[", "watering.", "storage.", "rotation.",
                "fertilizer.", "varieties[", "thinning.", "soil.preferred_description",
                "ph.note", "yield_expectations", "harvest_ready", "container_notes.notes",
                "soil_prep", "description_seasoned", "description_beginner", "companions.")
BACKEND_MARK = ("_quote", "synthesis_note", "design_note", "_basis", ".source",
                ".sources", "provenance", "anchoring", "evidence_tier", "_id", ".id",
                ".name", ".category", ".timing", ".confidence", "verified_against")
SCALAR_PATHS = {"days_to_maturity[0]", "days_to_maturity[1]", "spacing_inches[0]",
                "spacing_inches[1]", "germination_temp_f[0]", "germination_temp_f[1]",
                "ph.preferred_range[0]", "ph.preferred_range[1]", "ph.tolerated_range[0]",
                "ph.tolerated_range[1]", "sunlight_hours[0]", "sunlight_hours[1]",
                "succession_policy.interval_weeks", "succession_policy.successions",
                "succession_policy.max_successions_per_season"}
WINDOW_DATE = ("direct_sow", "start_indoors", "plant_out", "harvest_start", "harvest_end")

def classify(path, val):
    """Return surface bucket in {bio, scalar, window} or None if not measured."""
    if path in SCALAR_PATHS and isinstance(val, (int, float)):
        return "scalar"
    if "regions." in path and ".resolved_by_zone." in path:
        if any(w in path for w in WINDOW_DATE) and not any(b in path for b in (".sources", "_quote", "synthesis", "anchoring", "provenance", ".label", ".window_type", ".calendar_state")):
            if isinstance(val, (str, int, float)):
                return "window"
        return None
    if isinstance(val, str) and len(val) >= 20 and " " in val:
        if any(s in path for s in BIO_SECTIONS) and not any(b in path for b in BACKEND_MARK):
            if path.endswith(("_seasoned", "_beginner")) or path in ("thinning.when",):
                return "bio"
    return None

# ---- build global (path,value) -> slugs ----
shared_map = collections.defaultdict(set)
crop_measured = collections.defaultdict(lambda: collections.defaultdict(list))  # slug -> surface -> [(path, n_other)]
for slug, leaves in leaf_index.items():
    for path, val in leaves.items():
        surf = classify(path, val)
        if surf:
            key = (path, json.dumps(val, ensure_ascii=False, sort_keys=True))
            shared_map[key].add(slug)

for slug, leaves in leaf_index.items():
    for path, val in leaves.items():
        surf = classify(path, val)
        if not surf:
            continue
        key = (path, json.dumps(val, ensure_ascii=False, sort_keys=True))
        n_other = len(shared_map[key]) - 1
        crop_measured[slug][surf].append((path, n_other))

# ---- per-crop ratios ----
def ratios(slug):
    out = {}
    for surf in ("bio", "scalar", "window"):
        items = crop_measured[slug].get(surf, [])
        total = len(items)
        shared = sum(1 for _, n in items if n > 0)
        out[surf] = (shared, total)
    return out

rows = []
for slug in by_slug:
    r = ratios(slug)
    tot_total = sum(t for _, t in r.values())
    tot_shared = sum(s for s, _ in r.values())
    overall = (tot_shared / tot_total) if tot_total else 0.0
    rows.append((overall, slug, r, tot_shared, tot_total))
rows.sort(reverse=True)

# ---- bucket clusters: for each crop, its top co-sharers (on bio surface) ----
def top_cosharers(slug, surf="bio", k=5):
    counter = collections.Counter()
    leaves = leaf_index[slug]
    for path, val in leaves.items():
        if classify(path, val) != surf:
            continue
        key = (path, json.dumps(val, ensure_ascii=False, sort_keys=True))
        for other in shared_map[key]:
            if other != slug:
                counter[other] += 1
    return counter.most_common(k)

# ---- emit ----
L = []
def p(s=""): L.append(s)

p("# Dataset-wide bucket-contamination report")
p()
p(f"- Crops scanned: **{len(crops)}**")
p(f"- Crops that have walked the per-crop arc (verified -- excluded from 'candidate'): **{sorted(walked)}**")
p(f"- Measured surfaces: biology prose (`_seasoned`/`_beginner`), key scalars (DTM/spacing/germ-temp/pH/sun/succession), region windows (sow/plant/harvest dates).")
p(f"- 'shared' = byte-identical value at the same crop-relative path on >=1 OTHER crop. For a non-walked crop, shared == candidate bucket data.")
p()
p("## Per-crop contamination (ranked, worst first)")
p()
p("| crop | walked? | bio shared | scalar shared | window shared | overall |")
p("|------|:------:|:----------:|:-------------:|:-------------:|:-------:|")
for overall, slug, r, ts, tt in rows:
    def cell(surf):
        s, t = r[surf]
        return f"{s}/{t} ({100*s/t:.0f}%)" if t else "-"
    w = "YES" if slug in walked else ""
    p(f"| {slug} | {w} | {cell('bio')} | {cell('scalar')} | {cell('window')} | **{100*overall:.0f}%** ({ts}/{tt}) |")
p()

# GS clean check
p("## Gold-standard crops -- clean check (bio surface)")
p()
for slug in sorted(walked):
    r = ratios(slug)
    s, t = r["bio"]
    p(f"- **{slug}**: bio prose shared {s}/{t} ({100*s/t:.0f}% if any) -- co-sharers: {top_cosharers(slug, k=4)}")
p()

# clusters for the worst N non-walked crops
p("## Bucket clusters (top co-sharers on biology prose, worst 15 non-walked crops)")
p()
shown = 0
for overall, slug, r, ts, tt in rows:
    if slug in walked:
        continue
    p(f"- **{slug}** ({100*overall:.0f}%): {top_cosharers(slug, k=6)}")
    shown += 1
    if shown >= 15:
        break
p()

# dataset summary
nonwalked = [x for x in rows if x[1] not in walked]
mean_overall = sum(o for o, *_ in nonwalked) / len(nonwalked) if nonwalked else 0
p("## Summary")
p()
p(f"- Mean overall contamination across the {len(nonwalked)} non-walked crops: **{100*mean_overall:.0f}%**")
hi = sum(1 for o, *_ in nonwalked if o >= 0.6)
p(f"- Non-walked crops >=60% contaminated: **{hi}** of {len(nonwalked)}")
p(f"- This per-(crop,field) shared/unique map is the candidate-vs-verified signal the pipeline/bots consume.")

report = "\n".join(L)
print(report)
if OUT_MD:
    open(OUT_MD, "w").write(report + "\n")
    print(f"\n[written to {OUT_MD}]", file=sys.stderr)
