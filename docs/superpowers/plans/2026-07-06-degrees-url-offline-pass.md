# §B/§C Offline Pass -- Spelled-Degrees Cleanup + Non-Null-URL Gate -- Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Normalize user-facing spelled temperatures to `°F` across the roster, harden the gate so they can't regress, and add an offline non-null-URL gate -- all without touching the network.

**Architecture:** One shared, tested `temp_scan` module (a `spelled_temp_hits` scanner + a `convert_temps` fixer -- inverses of each other) becomes the single source of truth, replacing the two narrow inline regexes in `whole_crop_gate` and `release_verify`. A new offline `url_health_gate` enforces non-null URLs in the live layers. The data sweep uses `convert_temps` on the flagged crops (onion excluded -- its "degrees" are latitude, hand-clarified to `°N`), verified by `spelled_temp_hits == 0`, then SHA-guarded promoted.

**Tech Stack:** Python 3 stdlib only (`re`, `json`, `argparse`). Tests are plain `assert` scripts run with `python3 tools/test_*.py` (repo convention, see `tools/test_numeric_sanity_gate.py`) -- NOT pytest.

## Global Constraints

- Canonical `crops_data_final.json` is **READ-ONLY** until the Task 4 promote; interim work on a scratch copy under the scratchpad `/private/tmp/claude-501/-Users-trevorrawson-plant-dataset/3c7e7ad1-e42e-4910-8ab6-090c862189da/scratchpad`.
- Canonical stays COMPACT: `json.dumps(obj, separators=(",",":"), ensure_ascii=False)`, no trailing newline. Never `indent=`.
- Gate by **EXIT CODE**, never by grepping output.
- Any new/hardened gate is **TDD: RED before GREEN**.
- Tests are plain `assert` scripts, run `python3 tools/test_<name>.py`; exit 0 = pass. NOT pytest.
- Convert temps in **CONSUMER copy only** (`is_backend(key, path)` false). No em dashes; American English; temps render as `°F`; "plant" lowercase.
- **onion is latitude, NOT temperature** -- exclude it from `convert_temps`; hand-clarify its "38 to 39 degrees" etc. to `°N`. Do NOT convert onion to `°F`.
- **`url_health_gate` is OFFLINE** -- never hits the network; the legacy `zones{}` layer is EXCLUDED; the online liveness sweep is a deferred follow-on.
- SHA-guard the promote (assert exactly the flagged §C slugs changed); Trevor confirms the push.
- Research via WebFetch/WebSearch ONLY; never curl/wget/pdftotext; NEVER `dangerouslyDisableSandbox`.

**Design reference:** `docs/superpowers/specs/2026-07-06-degrees-url-offline-pass-design.md`.
**Base canonical SHA at plan time:** `035b950db368a48c7920792569928318a922afdb096aae96a74af747af7f4f56`.

---

### Task 1: `temp_scan.py` -- shared scanner + fixer (TDD)

The single source of truth for spelled-temperature handling. `spelled_temp_hits` (used by the gates) and `convert_temps` (used by the sweep) are inverses and live together.

**Files:**
- Create: `tools/temp_scan.py`
- Test: `tools/test_temp_scan.py`

**Interfaces:**
- Produces: `spelled_temp_hits(s) -> list[str]` -- offending temperature fragments in `s` (`[]` = clean); skips latitude/angle degrees.
- Produces: `convert_temps(s) -> str` -- `s` with spelled temperature forms rewritten to `°F`; latitude/angle skipped; idempotent.

- [ ] **Step 1: Write the failing test**

Create `tools/test_temp_scan.py`:

```python
#!/usr/bin/env python3
"""Tests for the shared spelled-temperature scanner + fixer (post-114 §C). Run:
    python3 tools/test_temp_scan.py

WHY: the old per-gate regex (\bdegrees?\s*F\b) missed '90 degrees', bare '50 F', and
'degrees Fahrenheit' -- all shipped. This module widens detection AND provides the fixer, with a
latitude/angle exclusion so onion's '38 to 39 degrees' (latitude) is never touched.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from temp_scan import spelled_temp_hits, convert_temps

# --- spelled_temp_hits: FLAG the shipped forms ---
assert spelled_temp_hits("extreme heat above 90 degrees does the same")      # '90 degrees'
assert spelled_temp_hits("a week of nights below 50 F bolts")                # bare '50 F'
assert spelled_temp_hits("hardy to about 17 degrees Fahrenheit, but")        # 'degrees Fahrenheit'
assert spelled_temp_hits("put them somewhere warm (70 to 80 degrees is ideal)")
assert spelled_temp_hits("countertop at around 60-65 degrees. Don't")
assert spelled_temp_hits("keep near 30 to 35 F at high humidity")            # 'F' after a range

# --- spelled_temp_hits: do NOT flag the correct or the non-temp forms ---
assert spelled_temp_hits("the ideal 70 to 80°F range") == []                 # already °F
assert spelled_temp_hits("cold below 50°F damages the tomato") == []
assert spelled_temp_hits("grows above about 38 to 39°N") == []               # latitude °N
assert spelled_temp_hits("at latitudes roughly above 38 to 39 degrees") == []  # latitude context
assert spelled_temp_hits("about 45 degrees north latitude") == []            # latitude words
assert spelled_temp_hits("") == [] and spelled_temp_hits(None) == []

# --- convert_temps: rewrite to °F ---
assert convert_temps("above 90 degrees does") == "above 90°F does"
assert convert_temps("nights below 50 F bolts") == "nights below 50°F bolts"
assert convert_temps("hardy to about 17 degrees Fahrenheit, but") == "hardy to about 17°F, but"
assert convert_temps("warm (70 to 80 degrees is ideal)") == "warm (70 to 80°F is ideal)"
assert convert_temps("around 60-65 degrees. Don't") == "around 60-65°F. Don't"
assert convert_temps("near 30 to 35 F at") == "near 30 to 35°F at"
# idempotent + latitude untouched
assert convert_temps("the ideal 70 to 80°F range") == "the ideal 70 to 80°F range"
assert convert_temps("above 38 to 39 degrees north latitude") == "above 38 to 39 degrees north latitude"

print("temp_scan tests: OK")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tools/test_temp_scan.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'temp_scan'`.

- [ ] **Step 3: Write the implementation**

Create `tools/temp_scan.py`:

```python
#!/usr/bin/env python3
"""Shared spelled-temperature scanner + fixer (post-114 §C). ONE source of truth, imported by
whole_crop_gate (C/D) and release_verify (D). Flags/rewrites spelled temperature forms that should
render as the canonical °F; EXCLUDES latitude/angle 'degrees'.

The old per-gate regex (\\bdegrees?\\s*F\\b|\\bdeg\\.?\\s*F\\b|°\\s+F) was too narrow -- it missed
'90 degrees', bare '50 F', and 'degrees Fahrenheit' (all of which shipped). This widens it.
"""
import re

# spelled temperature forms
_TEMP_RES = [
    re.compile(r"\d+\s*(?:to\s*\d+\s*)?degrees?\b", re.I),  # '90 degrees', '70 to 80 degrees'
    re.compile(r"\bdegrees?\s*F\b", re.I),                  # 'degrees F' (old form, no number)
    re.compile(r"\bdeg\.?\s*F\b", re.I),                    # 'deg F' / 'deg. F'
    re.compile(r"°\s+F"),                                   # '° F' (space between ° and F)
    re.compile(r"\b\d{2,3}\s*F\b"),                         # bare '50 F' (no degree sign)
]
# latitude / angle context: a match adjacent to one of these is NOT temperature
_LAT_TOKEN = re.compile(r"°\s*[NS]\b|degrees?\s*(?:[NS]\b|north|south|of\s+latitude|latitude)", re.I)
_LAT_NEAR = re.compile(r"\b(?:latitude|longitude)\b", re.I)


def spelled_temp_hits(s):
    """Return a list of offending temperature fragments in s ([] = clean). Skips latitude/angle."""
    if not isinstance(s, str):
        return []
    hits = []
    for rx in _TEMP_RES:
        for m in rx.finditer(s):
            i, j = m.start(), m.end()
            if _LAT_TOKEN.search(s[i:j + 12]) or _LAT_NEAR.search(s[max(0, i - 6):j + 12]):
                continue
            hits.append(m.group())
    return hits


# fixer: a number (or range) + 'degrees[ F/Fahrenheit]' -> '<n>°F'; bare '<n> F' -> '<n>°F'
_CONV_DEGREES = re.compile(r"(\d+(?:\s*(?:to|-|–)\s*\d+)?)\s*degrees?(?:\s*Fahrenheit|\s*F)?\b", re.I)
_CONV_BARE_F = re.compile(r"\b(\d{2,3})\s*F\b")


def convert_temps(s):
    """Rewrite spelled temperature forms in s to canonical °F. Skips latitude/angle; idempotent."""
    if not isinstance(s, str):
        return s

    def repl_deg(m):
        after = s[m.end():m.end() + 12]
        if re.match(r"\s*(?:[NS]\b|north|south|latitude)", after, re.I) or _LAT_NEAR.search(after):
            return m.group(0)
        return m.group(1) + "°F"

    out = _CONV_DEGREES.sub(repl_deg, s)
    out = _CONV_BARE_F.sub(lambda m: m.group(1) + "°F", out)
    return out


if __name__ == "__main__":
    import json
    import sys
    from field_classification import is_backend
    path = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"
    data = json.load(open(path, encoding="utf-8"))
    total = 0

    def walk(o, pat, slug):
        global total
        if isinstance(o, dict):
            for k, v in o.items():
                p = f"{pat}.{k}" if pat else k
                if not is_backend(k, pat):
                    if isinstance(v, str):
                        for h in spelled_temp_hits(v):
                            print(f"  {slug} {p}: {h!r}")
                            total += 1
                    elif isinstance(v, list):
                        for i, x in enumerate(v):
                            if isinstance(x, str):
                                for h in spelled_temp_hits(x):
                                    print(f"  {slug} {p}[{i}]: {h!r}")
                                    total += 1
                walk(v, p, slug)
        elif isinstance(o, list):
            for i, x in enumerate(o):
                walk(x, f"{pat}[{i}]", slug)

    for c in data["crops"]:
        walk(c, "", c.get("slug", "?"))
    print(f"spelled-temp scan: {total} user-facing hit(s)")
    sys.exit(1 if total else 0)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 tools/test_temp_scan.py`
Expected: `temp_scan tests: OK`, exit 0.

- [ ] **Step 5: Commit**

```bash
git add tools/temp_scan.py tools/test_temp_scan.py
git commit -m "feat(gate): shared temp_scan -- spelled_temp_hits + convert_temps (TDD, §C)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 2: `url_health_gate.py` -- offline non-null-URL gate (TDD)

**Files:**
- Create: `tools/url_health_gate.py`
- Test: `tools/test_url_health_gate.py`

**Interfaces:**
- Produces: `url_health_violations(crop) -> list[str]` -- live-layer `anchoring_urls` entries with a null/empty `url` (`[]` = clean). The legacy `zones{}` layer is skipped.

- [ ] **Step 1: Write the failing test**

Create `tools/test_url_health_gate.py`:

```python
#!/usr/bin/env python3
"""Tests for the offline non-null-URL gate (post-114 §B, offline half). Run:
    python3 tools/test_url_health_gate.py

WHY: a cited source whose anchoring url is null resolves to nothing. The LIVE layers (regions{} +
claim/top) must carry non-null urls; the legacy zones{} layer is excluded (matches gate F scoping).
OFFLINE only -- liveness (404/redirect) is a separate --online sweep.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from url_health_gate import url_health_violations

def crop(**kw):
    return dict(slug="x", **kw)

# 1. a regions{} anchoring url that is null -> violation
c = crop(regions={"se_gulf": {"anchoring_urls": {"ncsu_ext": {"url": None, "verified": "2026-07-06"}}}})
assert any("ncsu_ext" in v for v in url_health_violations(c)), url_health_violations(c)

# 2. a top-level/claim anchoring url that is empty -> violation
c = crop(storage={"anchoring_urls": {"psu_ext": {"url": "", "verified": "2026-07-06"}}})
assert any("psu_ext" in v for v in url_health_violations(c)), url_health_violations(c)

# 3. a legacy zones{} null url -> NOT flagged (excluded)
c = crop(zones={"8": {"anchoring_urls": {"uga_b577": {"url": None}}}})
assert url_health_violations(c) == [], url_health_violations(c)

# 4. all live-layer urls present -> clean
c = crop(regions={"se_gulf": {"anchoring_urls": {"ncsu_ext": {"url": "https://x/", "verified": "2026-07-06"}}}},
         storage={"anchoring_urls": {"psu_ext": {"url": "https://y/", "verified": "2026-07-06"}}})
assert url_health_violations(c) == [], url_health_violations(c)

print("url_health_gate tests: OK")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tools/test_url_health_gate.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'url_health_gate'`.

- [ ] **Step 3: Write the implementation**

Create `tools/url_health_gate.py`:

```python
#!/usr/bin/env python3
"""Offline non-null-URL gate (post-114 §B, offline half). Every anchoring_urls entry in the LIVE
layers (regions{} + claim/top-level) must carry a non-null, non-empty url. The legacy zones{} layer
is EXCLUDED (matches whole_crop_gate gate F scoping). OFFLINE ONLY -- never hits the network; URL
liveness (404/redirect/logo-PDF) is a separate --online sweep, deferred.

Usage: python3 tools/url_health_gate.py [crops_data_final.json]
Exit 1 on any live-layer null/empty url; else 0.
"""


def url_health_violations(crop):
    """Return list of '<slug>: <path>: null/empty url' ([] = clean). Legacy zones{} layer skipped."""
    V = []
    slug = crop.get("slug", "?")

    def walk(o, pat):
        if isinstance(o, dict):
            for k, v in o.items():
                p = f"{pat}.{k}" if pat else k
                if (k.endswith("anchoring_urls") and isinstance(v, dict)
                        and not p.startswith("zones")):  # legacy zones{} EXCLUDED
                    for src, rec in v.items():
                        if isinstance(rec, dict) and not rec.get("url"):
                            V.append(f"{slug}: {p}.{src}: null/empty url")
                walk(v, p)
        elif isinstance(o, list):
            for i, x in enumerate(o):
                walk(x, f"{pat}[{i}]")

    walk(crop, "")
    return V


if __name__ == "__main__":
    import json
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"
    data = json.load(open(path, encoding="utf-8"))
    total = 0
    for c in data["crops"]:
        for v in url_health_violations(c):
            print(f"  VIOLATION: {v}")
            total += 1
    print(f"url_health (offline, live layers): {total} null/empty url(s)")
    sys.exit(1 if total else 0)
```

- [ ] **Step 4: Run test + confirm the live canonical passes**

```bash
python3 tools/test_url_health_gate.py; echo "test: $?"          # expect: url_health_gate tests: OK / 0
python3 tools/url_health_gate.py; echo "canonical: $?"          # expect: 0 null/empty urls / exit 0
```
Expected: both exit 0. (The live layer is already clean; the 57 nulls are all in the excluded `zones{}` layer.) If the canonical run is non-zero, a live-layer null exists -- STOP and inspect it.

- [ ] **Step 5: Commit**

```bash
git add tools/url_health_gate.py tools/test_url_health_gate.py
git commit -m "feat(gate): offline non-null-URL gate, live layers only (TDD, §B)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 3: §C data sweep + SHA-guarded promote

Scan-driven (not a hardcoded list), so green-beans-bush (named in the kickoff) is caught if it has any. onion is excluded from auto-convert and hand-clarified to `°N`.

**Files:**
- Modify: `crops_data_final.json` (the promote -- READ-ONLY ends here)
- Modify: `CURRENT_STATE.md`, `STATE_HISTORY.md`, `LATEST.txt` (state trio)
- Scratch: `<scratchpad>/deg_scratch.json`

**Interfaces:**
- Consumes: `temp_scan.spelled_temp_hits`, `temp_scan.convert_temps`, `field_classification.is_backend`.

- [ ] **Step 1: Copy canonical to scratch; confirm base SHA; list the dirty crops (dataset-level RED)**

```bash
cd /Users/trevorrawson/plant-dataset
SCRATCH="/private/tmp/claude-501/-Users-trevorrawson-plant-dataset/3c7e7ad1-e42e-4910-8ab6-090c862189da/scratchpad"
shasum -a 256 crops_data_final.json | cut -c1-16   # MUST be 035b950d; else STOP
cp crops_data_final.json "$SCRATCH/deg_scratch.json"
python3 tools/temp_scan.py "$SCRATCH/deg_scratch.json"; echo "dirty exit (expect 1): $?"
```
Expected: the scan lists the hits (the 11 temperature crops + onion's latitude), exit 1. Note the crop set -- especially whether `green-beans-bush` appears and whether any crop beyond the expected 12 shows up. This is the RED baseline.

- [ ] **Step 2: Apply `convert_temps` to every dirty crop EXCEPT onion, on the scratch**

```bash
python3 - "$SCRATCH/deg_scratch.json" <<'PY'
import json, sys
sys.path.insert(0, "tools")
from temp_scan import spelled_temp_hits, convert_temps
from field_classification import is_backend
p = sys.argv[1]
d = json.load(open(p, encoding="utf-8"))
EXCLUDE = {"onion"}  # onion's "degrees" are LATITUDE -- handled separately in Step 3
changed = set()

def fix(o, pat, slug):
    if isinstance(o, dict):
        for k, v in list(o.items()):
            pp = f"{pat}.{k}" if pat else k
            if not is_backend(k, pat):
                if isinstance(v, str) and spelled_temp_hits(v):
                    nv = convert_temps(v)
                    if nv != v:
                        o[k] = nv; changed.add(slug)
                elif isinstance(v, list):
                    for i, x in enumerate(v):
                        if isinstance(x, str) and spelled_temp_hits(x):
                            nx = convert_temps(x)
                            if nx != x:
                                v[i] = nx; changed.add(slug)
            fix(o[k], pp, slug)   # recurse into nested dicts/lists (mirrors whole_crop_gate uf_walk)
    elif isinstance(o, list):
        for i, x in enumerate(o):
            fix(x, f"{pat}[{i}]", slug)

for c in d["crops"]:
    if c["slug"] in EXCLUDE:
        continue
    fix(c, "", c["slug"])
open(p, "w", encoding="utf-8").write(json.dumps(d, separators=(",", ":"), ensure_ascii=False))
print("converted crops:", sorted(changed))
PY
```

- [ ] **Step 3: Hand-clarify onion's latitude "degrees" to `°N` on the scratch**

onion's degree references are latitude; convert each to `°N` (NOT `°F`). Use the exact strings from the Step-1 scan output:

```bash
python3 - "$SCRATCH/deg_scratch.json" <<'PY'
import json, sys, re
p = sys.argv[1]
d = json.load(open(p, encoding="utf-8"))
onion = next(c for c in d["crops"] if c["slug"] == "onion")
# Replace latitude "<n> to <m> degrees" / "<n> degrees" (in latitude prose) with the °N form.
# These are the three known latitude references; the sub is scoped to onion only.
def clarify(s):
    if not isinstance(s, str): return s
    s = re.sub(r"(\d+\s*to\s*\d+)\s*degrees\b", r"\1°N", s)   # '38 to 39 degrees' -> '38 to 39°N'
    s = re.sub(r"(\babove|\bbelow)\s+(\d+)\s*degrees\b", r"\1 \2°N", s, flags=re.I)  # 'below 35 degrees'
    return s
def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, str): o[k] = clarify(v)
            else: walk(v)
    elif isinstance(o, list):
        for i, x in enumerate(o):
            if isinstance(x, str): o[i] = clarify(x)
            else: walk(x)
walk(onion)
open(p, "w", encoding="utf-8").write(json.dumps(d, separators=(",", ":"), ensure_ascii=False))
print("onion clarified")
PY
```

- [ ] **Step 4: Verify GREEN on the scratch + spot-check the conversions in the main loop**

```bash
python3 tools/temp_scan.py "$SCRATCH/deg_scratch.json"; echo "temp scan exit (expect 0): $?"
# spot-check: print onion's clarified latitude strings + a couple converted temp strings
python3 - "$SCRATCH/deg_scratch.json" <<'PY'
import json, sys, re
d = json.load(open(sys.argv[1], encoding="utf-8"))
for c in d["crops"]:
    if c["slug"] in ("onion","cherry-tomato","strawberry","bok-choy"):
        s = json.dumps(c, ensure_ascii=False)
        for m in re.finditer(r".{25}(?:°[NF]|degrees).{25}", s):
            print(c["slug"], "...", m.group(), "...")
PY
```
Expected: `temp scan exit: 0` (no spelled temps remain). Read the spot-check output: onion's must read as latitude (`38 to 39°N`), the temp crops' must read as `°F` (e.g. `90°F`, `17°F`, `50°F`), and NO surrounding prose is mangled. If anything looks wrong, fix it on the scratch and re-run before promoting.

- [ ] **Step 5: SHA-guarded splice (assert EXACTLY the flagged crops changed)**

```bash
python3 - crops_data_final.json "$SCRATCH/deg_scratch.json" <<'PY'
import json, sys, hashlib
base_bytes = open(sys.argv[1], "rb").read()
assert hashlib.sha256(base_bytes).hexdigest().startswith("035b950d"), "BASE SHA MISMATCH -- ABORT"
base = json.loads(base_bytes)
cand = json.load(open(sys.argv[2], encoding="utf-8"))
bc = {c["slug"]: c for c in base["crops"]}
cc = {c["slug"]: c for c in cand["crops"]}
assert set(bc) == set(cc), "crop set changed -- ABORT"
changed = {s for s in bc if json.dumps(bc[s], sort_keys=True) != json.dumps(cc[s], sort_keys=True)}
# every top-level key except crops must be byte-identical (source_catalog included -- no new sources here)
for k in base:
    if k == "crops": continue
    assert json.dumps(base[k], sort_keys=True) == json.dumps(cand.get(k), sort_keys=True), f"top-level {k} changed -- ABORT"
assert sum(1 for c in cand["crops"] if c.get("verification_status", {}).get("status") == "verified_gs_arc") == 114
print("SHA-guard OK: changed slugs =", sorted(changed))
PY
```
Expected: `changed slugs = [...]` -- the flagged temperature crops + onion, and nothing else. Confirm the list matches Step-1's dirty set. Any `ABORT` = stop.

- [ ] **Step 6: Promote, verify COMPACT, record new SHA**

```bash
cp "$SCRATCH/deg_scratch.json" crops_data_final.json
python3 -c "import json; d=open('crops_data_final.json',encoding='utf-8').read(); assert d==json.dumps(json.loads(d),separators=(',',':'),ensure_ascii=False), 'NOT COMPACT'; assert not d.endswith(chr(10)), 'trailing newline'; print('compact OK')"
shasum -a 256 crops_data_final.json | cut -c1-16   # record NEW SHA
```

- [ ] **Step 7: Full release suite on the live canonical (still uses the OLD narrow gate -- Task 4 wires the new one)**

```bash
python3 tools/temp_scan.py; echo "temp_scan: $?"                                  # expect 0
python3 tools/url_health_gate.py; echo "url_health: $?"                           # expect 0
python3 tools/register_completeness_gate.py >/dev/null 2>&1; echo "register: $?"  # expect 0
CHANGED="$(python3 - <<'PY'
import json,sys; sys.path.insert(0,'tools')
# re-derive changed set from temp_scan Step-1 note; hardcode after confirming in Step 5
print("beefsteak-tomato bok-choy cherry-tomato grape-tomato roma-tomato lettuce-leaf orange-navel pear-european raspberry strawberry tomatillo onion")
PY
)"
for s in $CHANGED; do python3 tools/whole_crop_gate.py "$s" >/dev/null 2>&1; echo "whole_crop_gate $s: $?"; done  # expect all 0
for s in $CHANGED; do python3 tools/release_verify.py crops_data_final.json --slug "$s" --ref basil 2>&1 | grep RELEASE-VERIFY; done
```
Expected: `temp_scan: 0`, `url_health: 0`, `register: 0`, every `whole_crop_gate <slug>: 0`, and each `release_verify` = clean or the pre-existing benign multi-crop concerns only (compare to base if unsure). If any gate is non-zero, STOP and diagnose before committing. (Replace the hardcoded `$CHANGED` list with the exact set confirmed in Step 5.)

- [ ] **Step 8: State trio**

```bash
python3 tools/gen_current_state.py   # regenerate; then hand-fill the editorial header slots
# LATEST.txt: new SHA + a session line (035b950d -> new SHA; §C spelled-degrees on N crops + onion °N)
# STATE_HISTORY.md: prepend a most-recent-first entry (the §C sweep; onion latitude clarified; gates)
# CURRENT_STATE.md: update the headline + canonical pointer + status block + gate-record SHA
```

- [ ] **Step 9: Commit (push is Trevor-gated)**

```bash
git add crops_data_final.json CURRENT_STATE.md STATE_HISTORY.md LATEST.txt
git commit -m "fix(data): §C spelled-degrees -> °F (11 temp crops); onion latitude -> °N (amend)

Expected set: beefsteak-tomato, bok-choy, cherry/grape/roma-tomato, lettuce-leaf,
orange-navel, pear-european, raspberry, strawberry, tomatillo (+ onion clarified to
°N, NOT converted). Confirm the exact set against Step 5. SHA-guarded from 035b950d
(exactly those slugs changed). Canonical COMPACT.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 4: Wire the hardened scanner into `whole_crop_gate` + `release_verify`

Now that the canonical is clean (Task 3), replace the two narrow inline regexes with `spelled_temp_hits`. Every commit stays green because the data no longer contains spelled temps.

**Files:**
- Modify: `tools/whole_crop_gate.py` (the C/D scan, ~line 726-737)
- Modify: `tools/release_verify.py` (the D scan, ~line 66)

**Interfaces:**
- Consumes: `temp_scan.spelled_temp_hits`.

- [ ] **Step 1: Wire into `whole_crop_gate.py`**

Add the import near the other tool imports (after the `field_classification` import, ~line 65):

```python
from temp_scan import spelled_temp_hits
```

Replace the `_DEGF_RE` temperature check inside `_scan_user_str` (the `if _DEGF_RE.search(s):` branch, ~line 736) with:

```python
    if spelled_temp_hits(s):
        degf_hits.append((p, s[:80]))
```

(Leave the dash check untouched. The now-unused `_DEGF_RE` at line 730 may be deleted.)

- [ ] **Step 2: Wire into `release_verify.py`**

Add near the `field_classification` import (~line 33):

```python
from temp_scan import spelled_temp_hits
```

Replace the temperature clause in the flag expression (~line 66):

```python
        flag = ("--" in o or EMDASH in o or bool(spelled_temp_hits(o)))
```

- [ ] **Step 3: Run the full roster through the hardened gate (must be GREEN post-Task-3)**

```bash
cd /Users/trevorrawson/plant-dataset
fail=0
for c in $(python3 -c "import json;[print(x['slug']) for x in json.load(open('crops_data_final.json'))['crops']]"); do
  python3 tools/whole_crop_gate.py "$c" >/dev/null 2>&1 || { echo "FAIL $c"; fail=1; }
done
echo "whole_crop_gate all-roster fail flag (expect 0): $fail"
python3 tools/release_verify.py crops_data_final.json --slug basil --ref cherry-tomato 2>&1 | grep -E "^D\.|RELEASE-VERIFY"
```
Expected: `fail flag: 0` (no crop trips the hardened temperature gate -- the data is clean), and release_verify's D line is clean. If any crop FAILS, it has a spelled temp Task 3 missed -- go back and fix the data (do NOT loosen the gate).

- [ ] **Step 4: Confirm the gate actually catches a regression (adversarial, on a scratch copy)**

```bash
SCRATCH="/private/tmp/claude-501/-Users-trevorrawson-plant-dataset/3c7e7ad1-e42e-4910-8ab6-090c862189da/scratchpad"
cp crops_data_final.json "$SCRATCH/reg_scratch.json"
python3 - "$SCRATCH/reg_scratch.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
c=next(x for x in d["crops"] if x["slug"]=="basil")
c["tip_beginner"]="Water when the soil warms past 70 degrees."   # inject a spelled temp
json.dump(d, open(sys.argv[1],"w"))
PY
python3 tools/whole_crop_gate.py basil "$SCRATCH/reg_scratch.json" >/dev/null 2>&1; echo "injected exit (expect 1): $?"
rm -f "$SCRATCH/reg_scratch.json"
```
Expected: `injected exit: 1` -- the hardened gate catches the injected `70 degrees`. (Confirms the wiring is live, not just imported.)

- [ ] **Step 5: Commit**

```bash
git add tools/whole_crop_gate.py tools/release_verify.py
git commit -m "feat(gate): harden C/D + D to flag all spelled temps via temp_scan (§C)

Replaces the narrow \\bdegrees?\\s*F\\b regex (missed '90 degrees'/'50 F'/'degrees
Fahrenheit') with the shared spelled_temp_hits, latitude-aware. Data cleaned in the
prior commit so the roster is green.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Out of scope (follow-on)

- **The §B online liveness sweep** (its own plan): WebFetch the ~1,030 distinct URLs, classify live/404/redirect/logo-PDF/bare-homepage-on-a-claim, repoint the real offenders (`uga_b577` dead PDF, citrus TAMU redirect loops, lime bare `ucanr.edu`, generic-cucumber B577 logo-PDF), build `url_health_gate --online`, and only then (if wanted) backfill the 57 legacy `zones{}` nulls.
- **§D `rhs` tier** -- apply the §A ASPCA precedent to sage / broad-beans-fava.
- **The 108-crop `pet_safe` rollout** (§A follow-on).
