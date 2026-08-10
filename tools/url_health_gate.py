#!/usr/bin/env python3
"""Non-null-URL gate + online liveness gate (post-114 §B).

OFFLINE (default): every anchoring_urls entry in the LIVE layers (regions{} + claim/top-level) must
carry a non-null, non-empty url. The legacy zones{} layer is EXCLUDED (matches whole_crop_gate gate F
scoping). Never hits the network.

ONLINE (--online <ledger.json>): asserts that no LIVE-layer anchoring url is a KNOWN-DEAD offender.
Liveness is measured OUT OF BAND by the WebFetch sweep (WebFetch/WebSearch only -- never curl/wget), and
its verdicts are committed as a liveness LEDGER: {url: {"status": ..., "offender": true|false|...}}.
An entry with `offender: true` is a hard-dead url (404 / logo-or-empty PDF / redirect-loop). This mode
validates the dataset against that ledger; it does NOT itself hit the network, so it is reproducible and
safe to run in CI. It stays OUT of the pre-commit hook (run it explicitly, out-of-band). zones{} excluded.

Usage:
  python3 tools/url_health_gate.py [crops_data_final.json]                 # offline null-url gate
  python3 tools/url_health_gate.py --online <ledger.json> [crops.json]     # online liveness gate
Exit 1 on any violation; else 0.
"""


def _walk_live_anchors(crop):
    """Yield (path, src_key, rec) for every anchoring_urls entry in the LIVE layers (zones{} excluded)."""
    slug = crop.get("slug", "?")

    def walk(o, pat):
        if isinstance(o, dict):
            for k, v in o.items():
                p = f"{pat}.{k}" if pat else k
                if (k.endswith("anchoring_urls") and isinstance(v, dict)
                        and "zones" not in p.split(".")):  # legacy zones{} EXCLUDED
                    for src, rec in v.items():
                        if isinstance(rec, dict):
                            yield p, src, rec
                yield from walk(v, p)
        elif isinstance(o, list):
            for i, x in enumerate(o):
                yield from walk(x, f"{pat}[{i}]")

    for p, src, rec in walk(crop, ""):
        yield slug, p, src, rec


def url_health_violations(crop):
    """OFFLINE: return list of '<slug>: <path>: null/empty url' ([] = clean). Legacy zones{} skipped."""
    V = []
    for slug, p, src, rec in _walk_live_anchors(crop):
        if not rec.get("url"):
            V.append(f"{slug}: {p}.{src}: null/empty url")
    return V


def online_violations(crop, liveness):
    """ONLINE: return list of '<slug>: <path>.<src>: DEAD <url> (<status>)' for LIVE-layer urls that the
    liveness ledger marks a hard offender (`offender is True`). zones{} excluded (same as offline)."""
    V = []
    for slug, p, src, rec in _walk_live_anchors(crop):
        url = rec.get("url")
        if not url:
            continue
        verdict = liveness.get(url)
        if isinstance(verdict, dict) and verdict.get("offender") is True:
            status = verdict.get("status", "dead")
            V.append(f"{slug}: {p}.{src}: DEAD {url} ({status})")
    return V


def online_coverage(crops, liveness):
    """ONLINE coverage report (PLA-156): return (measured, total) over the DISTINCT non-null urls
    cited in the LIVE layers (zones{} excluded, same scoping as violations). `measured` = urls with a
    ledger verdict. Absence from the ledger is BLINDNESS, not liveness: `0 known-dead` means nothing
    without this denominator, so the CLI prints it on every --online run."""
    urls = set()
    for c in crops:
        for _slug, _p, _src, rec in _walk_live_anchors(c):
            url = rec.get("url")
            if url:
                urls.add(url)
    measured = sum(1 for u in urls if isinstance(liveness.get(u), dict))
    return measured, len(urls)


if __name__ == "__main__":
    import json
    import sys

    args = sys.argv[1:]
    if args and args[0] == "--online":
        if len(args) < 2:
            print("usage: url_health_gate.py --online <ledger.json> [crops.json]", file=sys.stderr)
            sys.exit(2)
        ledger_path = args[1]
        path = args[2] if len(args) > 2 else "crops_data_final.json"
        ledger = json.load(open(ledger_path, encoding="utf-8"))
        liveness = ledger.get("results", ledger)  # accept {results:{...}} or a bare {url:verdict} map
        data = json.load(open(path, encoding="utf-8"))
        total = 0
        for c in data["crops"]:
            for v in online_violations(c, liveness):
                print(f"  OFFENDER: {v}")
                total += 1
        measured, distinct = online_coverage(data["crops"], liveness)
        print(f"url_health --online (live layers, ledger {ledger_path}): {total} known-dead url(s); "
              f"coverage {measured}/{distinct} distinct urls have a ledger verdict, "
              f"{distinct - measured} UNMEASURED (absence from the ledger is not liveness)")
        sys.exit(1 if total else 0)

    path = args[0] if args else "crops_data_final.json"
    data = json.load(open(path, encoding="utf-8"))
    total = 0
    for c in data["crops"]:
        for v in url_health_violations(c):
            print(f"  VIOLATION: {v}")
            total += 1
    print(f"url_health (offline, live layers): {total} null/empty url(s)")
    sys.exit(1 if total else 0)
