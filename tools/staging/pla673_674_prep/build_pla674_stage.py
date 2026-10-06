"""PLA-674 prep: STAGE soil_prep_sources + soil_prep_anchoring_urls on the 121 certified crops (staging copy only).

Never writes crops_data_final.json. Writes the staged dataset(s) to OUT_DIR (default: the session scratchpad) and prints a
two-sided leaf diff summary per variant. The watermelon backfill is built ONLY from the housekeeping 60 Phase C EVIDENCE
rows for watermelon soil_prep_*; each row's quote is re-proven against its hashed bytes (cached_quote) before it counts.

Encoding RULED 2026-10-05 (D13): unsourced crops carry null + null (the PLA-581 rule: null = not assessed; [] would read
as "assessed, no sources"). The `empty` variant ([] + {}, the harvest_ready_sources precedent) was staged for the ruling
and is retired. Scope RULED (D14): all 121 certified crops.
Placement: the two keys sit immediately after the crop's last soil_prep_* key (the mature_dimensions_* precedent, PLA-10
promote 3); a crop with no soil_prep prose (81 of 121) gets them appended at the end of the crop object.
"""
import csv, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from cited_promote_common import cached_quote, leaf_diff, manifest, serialize, sha256_bytes  # noqa: E402

EV = os.path.join(ROOT, "tools", ".evidence_cache")
PHASE_C = os.path.join(ROOT, "tools", "staging", "housekeeping60", "phase_c", "EVIDENCE.tsv")
EXPECT_SHA = "350eda387fbed55464b16688a3bdc3263214b7c20631da98c7bbcb79f1d487c7"
VERIFIED = "2026-10-05"
KEYS = ("soil_prep_sources", "soil_prep_anchoring_urls")


def watermelon_backfill():
    man, cache = manifest(EV), {}
    rows = [r for r in csv.DictReader(open(PHASE_C, encoding="utf-8", newline=""), delimiter="\t")
            if r["crop"] == "watermelon" and r["entry_id"] in ("soil_prep_seasoned", "soil_prep_beginner")]
    if len(rows) != 14:
        raise SystemExit(f"expected 14 Phase C watermelon soil_prep EVIDENCE rows, found {len(rows)}")
    sources, anchors = [], {}
    for i, r in enumerate(rows):
        cached_quote(r, man, EV, cache, f"phase_c watermelon row {i}")
        if r["source_id"] not in anchors:
            sources.append(r["source_id"])
            anchors[r["source_id"]] = {"url": r["url"], "verified": VERIFIED}
        elif anchors[r["source_id"]]["url"] != r["url"]:
            raise SystemExit(f"{r['source_id']} carries two urls in the Phase C rows")
    return sources, anchors, rows


def stage(data, variant, backfill):
    out = json.loads(json.dumps(data))
    empty = ([], {}) if variant == "empty" else (None, None)
    for c in out["crops"]:
        if c.get("verification_status", {}).get("status") != "verified_gs_arc":
            continue
        if any(k in c for k in KEYS):
            raise SystemExit(f"{c['slug']} already carries a soil_prep sibling")
        vals = backfill if c["slug"] == "watermelon" else empty
        ks = list(c)
        prep = [i for i, k in enumerate(ks) if k in ("soil_prep_beginner", "soil_prep_seasoned")]
        at = (max(prep) + 1) if prep else len(ks)
        items = list(c.items())
        new = items[:at] + list(zip(KEYS, vals)) + items[at:]
        c.clear()
        c.update(new)
    return out


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("PLA674_OUT", HERE)
    raw = open(os.path.join(ROOT, "crops_data_final.json"), "rb").read()
    if sha256_bytes(raw) != EXPECT_SHA:
        raise SystemExit(f"canonical is {sha256_bytes(raw)[:8]}, expected {EXPECT_SHA[:8]}")
    data = json.loads(raw)
    sources, anchors, rows = watermelon_backfill()
    print(f"watermelon backfill: {len(rows)} Phase C rows re-proven against hashed bytes -> sources {sources}")
    for variant in ("null",):  # D13: null ruled; "empty" retired
        post = stage(data, variant, (sources, anchors))
        b = serialize(post)
        p = os.path.join(out_dir, f"staged_pla674_{variant}.json")
        open(p, "wb").write(b)
        diff = leaf_diff(data, post)
        crops = {data["crops"][d[1]]["slug"] for d in diff}
        keys = {d[2] for d in diff}
        print(f"[{variant}] {p}: sha {sha256_bytes(b)[:8]}, +{len(b) - len(raw)} bytes; {len(diff)} changed paths on "
              f"{len(crops)} crops; keys {sorted(keys)}; every path is an ADDED key: "
              f"{all(len(d) == 3 for d in diff)}")
        pre_paths = {(d[1], d[2]) for d in diff}
        assert len(pre_paths) == len(diff) == 2 * 121, "expected exactly two added keys on each of 121 crops"
        wm = next(c for c in post["crops"] if c["slug"] == "watermelon")
        print(f"    watermelon: {json.dumps({k: wm[k] for k in KEYS}, ensure_ascii=False)}")


main()
