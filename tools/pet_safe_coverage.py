#!/usr/bin/env python3
"""pet_safe rollout coverage tool (post-114 §A rollout). Warnings-only: safe crops carry no
pet_safe field, so the research-log JSON is the completeness record. This asserts every certified
crop was checked and the log agrees with the dataset.

Usage: python3 tools/pet_safe_coverage.py [crops_data_final.json] [rollout_log.json]
Exit 1 on any coverage/consistency violation; else 0.
"""


def coverage_violations(log, crops):
    """log: {slug: {"verdict": safe|toxic|caution, ...}}. crops: canonical crops list."""
    V = []
    cert = [c for c in crops if c.get("verification_status", {}).get("status") == "verified_gs_arc"]
    cert_slugs = {c["slug"] for c in cert}
    ds = {c["slug"]: c for c in cert}
    logged = set(log)

    for s in sorted(cert_slugs - logged):
        V.append(f"{s}: certified but not in the rollout log (unchecked)")
    for s in sorted(logged - cert_slugs):
        V.append(f"{s}: in the log but not a certified crop")

    for s, entry in log.items():
        verdict = entry.get("verdict") if isinstance(entry, dict) else entry
        has_ps = isinstance(ds.get(s, {}).get("pet_safe"), dict)
        if verdict in ("toxic", "caution") and not has_ps:
            V.append(f"{s}: logged {verdict} but no pet_safe block in the dataset")
        if verdict == "safe" and has_ps and ds[s]["pet_safe"].get("status") != "safe":
            V.append(f"{s}: logged safe but the dataset pet_safe.status is not safe")

    for c in cert:
        if isinstance(c.get("pet_safe"), dict) and c["slug"] not in log:
            V.append(f"{c['slug']}: has a pet_safe block but is not in the log")
    return V


if __name__ == "__main__":
    import json
    import os
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"
    logpath = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        "docs", "superpowers", "plans", "2026-07-06-pet-safe-rollout-log.json")
    data = json.load(open(path, encoding="utf-8"))
    log = json.load(open(logpath, encoding="utf-8"))
    vs = coverage_violations(log, data["crops"])
    for v in vs:
        print(f"  VIOLATION: {v}")
    counts = {}
    for e in log.values():
        vd = e.get("verdict") if isinstance(e, dict) else e
        counts[vd] = counts.get(vd, 0) + 1
    n_cert = sum(1 for c in data["crops"] if c.get("verification_status", {}).get("status") == "verified_gs_arc")
    print(f"coverage: logged={len(log)} of {n_cert} certified | {counts}")
    sys.exit(1 if vs else 0)
