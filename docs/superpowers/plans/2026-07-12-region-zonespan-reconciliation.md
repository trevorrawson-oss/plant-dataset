# Region Zone-Span Reconciliation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reconcile five regions' `zone_span`s to the 2023 USDA map (clone-adjacent-zone rows across all populated crops), guard them with a new A45 parity gate, and ship the region-coverage roadmap doc.

**Architecture:** A new standalone gate module (`tools/zone_span_gate.py`, wired into `whole_crop_gate.py` as A45 at promote time) enforces a hard-coded EXPECTED_SPANS table + span<->`resolved_by_zone` key parity. A deterministic patch builder emits an apply_patch-format batch that clones donor-zone rows to the new zones (marked with the established `lifted_from_zone` idiom) and normalizes every populated `zone_span` to the canonical str-typed value. Ceremony: builder -> apply_patch -> scratch -> gates -> promote.

**Tech Stack:** Python 3 stdlib only (repo convention), plain-python test scripts run from repo root, `tools/apply_patch.py` for application, `tools/release_verify.py` + `tools/gate_all.py` for release.

**Spec:** `docs/superpowers/specs/2026-07-12-region-zonespan-reconciliation-design.md`

## Global Constraints

- Canonical `crops_data_final.json` is COMPACT: `separators=(",",":")`, `ensure_ascii=False`, no trailing newline, never `indent=2`. Never reformat it.
- Canonical is READ-ONLY until Task 4's promote step; all gate/builder work runs on scratch copies (use the scratchpad dir or `*.scratch.json`, never overwrite canonical early).
- No em dashes anywhere in dataset content; `--` is fine in docs/code comments/commit messages. American English.
- Base canonical SHA at plan time: `e45bcf3cda2278ec8f6e6d5f6e6ed2e8612e2dbd04bd39fa779040f24bf194e8` (verify against `LATEST.txt` before starting; if it moved, re-verify the data-model facts in spec section 3 before proceeding).
- Commit per task; NEVER `git push` (Trevor confirms every push). No plant-astro edits or submodule bump from this session.
- CURRENT_STATE.md is hand-maintained surgically (a naive `gen_current_state.py` regen CORRUPTS it -- no `---` separator). Do not run the generator.
- Verified data facts (2026-07-12): 117 of 125 crops carry a `regions` dict; ALL 117 have populated `resolved_by_zone` in all 10 regions; `zone_span` is currently inconsistent (82 crops str-typed, 24 int-typed, 11 empty lists). `resolved_by_zone` keys are strings. plant-astro (`src/lib/regions.ts`) derives the app taxonomy from these per-crop cells and coerces span values via `Number(z)`, so str normalization is downstream-safe.

## The canonical span table (single source of truth for every task)

```python
# Widened, str-typed, ascending. The 5 changed regions per spec section 4;
# the other 5 are the current values, now enforced.
EXPECTED_SPANS = {
    "northern_tier":   ["3", "4", "5", "6", "7"],
    "warm_arid":       ["8"],
    "ca_interior":     ["8", "9"],
    "se_gulf":         ["8", "9", "10"],          # widened: +10 (was 8-9)
    "ca_north_coast":  ["9", "10"],
    "ca_south_coast":  ["9", "10", "11"],          # widened: +11 (was 9-10)
    "ca_desert":       ["9", "10", "11"],          # widened: +11 (was 9-10)
    "low_desert_az":   ["9", "10"],                # widened: +10 (was 9)
    "fl_peninsula":    ["10", "11"],
    "hawaii_tropical": ["10", "11", "12", "13"],   # widened: +10,+12,+13 (was 11)
}

# New zone -> donor zone, per widened region (spec section 4 table).
DONORS = {
    "low_desert_az":   {"10": "9"},
    "hawaii_tropical": {"10": "11", "12": "11", "13": "11"},
    "ca_south_coast":  {"11": "10"},
    "ca_desert":       {"11": "10"},
    "se_gulf":         {"10": "9"},
}
```

---

### Task 1: A45 gate module + tests + adversarial RED proof

**Files:**
- Create: `tools/zone_span_gate.py`
- Create: `tools/test_zone_span_gate.py`

**Interfaces:**
- Produces: `zone_span_gate.check_crop(crop) -> list[str]` (violation messages; empty = pass). Module constants `EXPECTED_SPANS` and `DONORS` (exact dicts above). Standalone runner: `python3 tools/zone_span_gate.py [crops_data_final.json]` walks every crop, prints violations, exit 1 if any.
- Consumes: nothing (first task).

The gate enforces, for every region entry on a crop that has a populated `resolved_by_zone`:
1. `zone_span` == `EXPECTED_SPANS[region_id]` exactly (value, str type, ascending order).
2. `set(resolved_by_zone.keys())` == `set(zone_span)` (parity).
3. Any non-null `lifted_from_zone` on a resolved row names another key present in the same `resolved_by_zone` dict (donor integrity).
4. An unknown region id (not in EXPECTED_SPANS) is a violation (a new region must be added to the table deliberately).

Crops with no `regions` dict are a no-op. A region entry with an empty/missing `resolved_by_zone` is a no-op (none exist today, but shells must not crash the gate).

- [ ] **Step 1: Write the failing test file**

```python
#!/usr/bin/env python3
"""Unit test for zone_span_gate (A45) -- expected-span + parity + donor integrity.
Run from repo root: python3 tools/test_zone_span_gate.py

Synthetic fixtures only (a live-crop fixture rots as the roster is authored).
Also carries the SWEEP ACCEPTANCE fixture: the Tier-1 gap table from
docs/2026-07-12-region-zonespan-gaps.md must be covered by EXPECTED_SPANS.
"""
import copy, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zone_span_gate import check_crop, EXPECTED_SPANS, DONORS

def make_crop():
    """A minimal crop whose regions exactly match EXPECTED_SPANS."""
    regions = {}
    for rid, span in EXPECTED_SPANS.items():
        regions[rid] = {
            "region_id": rid,
            "zone_span": list(span),
            "resolved_by_zone": {z: {"plant_out": "Mar 1 - Mar 21",
                                     "lifted_from_zone": None} for z in span},
        }
    return {"slug": "synthetic", "regions": regions}

fails = []
def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)

# 1. Conforming crop -> no violations.
check("conforming crop passes", check_crop(make_crop()) == [])

# 2. No regions dict -> no-op.
check("regionless crop passes", check_crop({"slug": "x"}) == [])

# 3. Divergent span value -> violation.
c = make_crop()
c["regions"]["low_desert_az"]["zone_span"] = ["9"]          # stale, pre-widen
check("stale span bounces", any("low_desert_az" in v for v in check_crop(c)))

# 4. Int-typed span -> violation (type is part of the contract).
c = make_crop()
c["regions"]["warm_arid"]["zone_span"] = [8]
check("int-typed span bounces", any("warm_arid" in v for v in check_crop(c)))

# 5. Empty span with populated rows -> violation.
c = make_crop()
c["regions"]["se_gulf"]["zone_span"] = []
check("empty span bounces", any("se_gulf" in v for v in check_crop(c)))

# 6. Span/key parity: span lists a zone with no resolved row -> violation.
c = make_crop()
del c["regions"]["hawaii_tropical"]["resolved_by_zone"]["12"]
check("missing resolved row bounces",
      any("hawaii_tropical" in v for v in check_crop(c)))

# 7. Parity the other way: an extra resolved row not in the span -> violation.
c = make_crop()
c["regions"]["ca_interior"]["resolved_by_zone"]["10"] = {"plant_out": "x",
                                                         "lifted_from_zone": None}
check("orphan resolved row bounces",
      any("ca_interior" in v for v in check_crop(c)))

# 8. Dangling lifted_from_zone -> violation.
c = make_crop()
c["regions"]["se_gulf"]["resolved_by_zone"]["10"]["lifted_from_zone"] = "77"
check("dangling lifted_from_zone bounces",
      any("se_gulf" in v for v in check_crop(c)))

# 9. Valid lifted_from_zone -> pass.
c = make_crop()
c["regions"]["se_gulf"]["resolved_by_zone"]["10"]["lifted_from_zone"] = "9"
check("valid lifted_from_zone passes", check_crop(c) == [])

# 10. Unknown region id -> violation.
c = make_crop()
c["regions"]["atlantis"] = {"region_id": "atlantis", "zone_span": ["1"],
                            "resolved_by_zone": {"1": {}}}
check("unknown region bounces", any("atlantis" in v for v in check_crop(c)))

# 11. Empty resolved_by_zone -> no-op (shell tolerance, must not crash).
c = make_crop()
c["regions"]["warm_arid"]["resolved_by_zone"] = {}
c["regions"]["warm_arid"]["zone_span"] = []
check("empty shell tolerated", not any("warm_arid" in v for v in check_crop(c)))

# 12. SWEEP ACCEPTANCE: every Tier-1 gap from the source report is covered.
TIER1 = [("AZ", "10", "low_desert_az"), ("HI", "12", "hawaii_tropical"),
         ("HI", "13", "hawaii_tropical"), ("HI", "10", "hawaii_tropical"),
         ("TX", "10", "se_gulf"),        # interim ruling, spec section 4
         ("CA", "11", "ca_south_coast"), ("CA", "11", "ca_desert"),
         ("LA", "10", "se_gulf")]
for state, zone, rid in TIER1:
    check(f"sweep {state} z{zone} -> {rid}", zone in EXPECTED_SPANS[rid])

# 13. DONORS sanity: every donor zone is inside its region's expected span,
#     and every donated zone is too.
for rid, m in DONORS.items():
    for new, donor in m.items():
        check(f"donor {rid} {new}<-{donor}",
              new in EXPECTED_SPANS[rid] and donor in EXPECTED_SPANS[rid])

if fails:
    print(f"\n{len(fails)} test(s) FAILED"); sys.exit(1)
print("\nall zone_span_gate tests passed")
```

- [ ] **Step 2: Run to verify it fails**

Run: `python3 tools/test_zone_span_gate.py`
Expected: `ModuleNotFoundError: No module named 'zone_span_gate'`

- [ ] **Step 3: Implement the gate module**

```python
#!/usr/bin/env python3
"""zone_span_gate (A45) -- region zone_span parity, the first guard on zone_span.

WHY: the 2023 USDA map relabeled the marquee cities the regions were authored for
(Phoenix 9b->10a, Honolulu ->z12), and nothing in tools/ read zone_span at all, so
the spans silently went stale and 300+ real ZIPs fell out of region resolution in
the app (docs/2026-07-12-region-zonespan-gaps.md). This gate pins every populated
region cell to ONE canonical, str-typed span and requires resolved_by_zone key
parity, so a span can never drift from its rows (or from crop to crop) again.
Widening a span is a deliberate act: update EXPECTED_SPANS + clone rows, together.

Spec: docs/superpowers/specs/2026-07-12-region-zonespan-reconciliation-design.md

check_crop(crop) -> list of violation strings (empty = pass). Wired into
whole_crop_gate as A45 at the widen promote (this gate is RED on pre-widen data
by design -- that is the TDD proof, not a bug).

Standalone roster-wide run: python3 tools/zone_span_gate.py [crops_data_final.json]
"""
import json
import sys

# Canonical spans, str-typed, ascending. 2023-map widened values
# (spec section 4): se_gulf +10, ca_south_coast/ca_desert +11,
# low_desert_az +10, hawaii_tropical +10/+12/+13.
EXPECTED_SPANS = {
    "northern_tier":   ["3", "4", "5", "6", "7"],
    "warm_arid":       ["8"],
    "ca_interior":     ["8", "9"],
    "se_gulf":         ["8", "9", "10"],
    "ca_north_coast":  ["9", "10"],
    "ca_south_coast":  ["9", "10", "11"],
    "ca_desert":       ["9", "10", "11"],
    "low_desert_az":   ["9", "10"],
    "fl_peninsula":    ["10", "11"],
    "hawaii_tropical": ["10", "11", "12", "13"],
}

# New zone -> donor zone per widened region; consumed by the widen builder and
# by test fixtures. Kept here so gate + builder can never disagree.
DONORS = {
    "low_desert_az":   {"10": "9"},
    "hawaii_tropical": {"10": "11", "12": "11", "13": "11"},
    "ca_south_coast":  {"11": "10"},
    "ca_desert":       {"11": "10"},
    "se_gulf":         {"10": "9"},
}


def check_crop(crop):
    """A45: expected span + span<->resolved_by_zone parity + donor integrity."""
    out = []
    slug = crop.get("slug", "?")
    for rid, cell in (crop.get("regions") or {}).items():
        if not isinstance(cell, dict):
            out.append(f"{slug}.{rid}: region cell is not an object")
            continue
        rbz = cell.get("resolved_by_zone") or {}
        if not rbz:
            continue  # unpopulated shell: nothing to pin yet
        expected = EXPECTED_SPANS.get(rid)
        if expected is None:
            out.append(f"{slug}.{rid}: unknown region id (add to EXPECTED_SPANS deliberately)")
            continue
        span = cell.get("zone_span")
        if span != expected:
            out.append(f"{slug}.{rid}: zone_span {span!r} != expected {expected!r} "
                       f"(str-typed, ascending)")
        keys = set(rbz.keys())
        if keys != set(expected):
            missing = sorted(set(expected) - keys)
            orphan = sorted(keys - set(expected))
            out.append(f"{slug}.{rid}: resolved_by_zone keys {sorted(keys)} != span "
                       f"(missing {missing}, orphan {orphan})")
        for zone, row in rbz.items():
            if not isinstance(row, dict):
                continue
            donor = row.get("lifted_from_zone")
            if donor is not None and str(donor) not in rbz:
                out.append(f"{slug}.{rid}.{zone}: lifted_from_zone {donor!r} "
                           f"names no resolved row")
    return out


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "crops_data_final.json"
    data = json.load(open(path, encoding="utf-8"))
    total = 0
    for crop in data["crops"]:
        for v in check_crop(crop):
            print(f"VIOLATION: {v}")
            total += 1
    print(f"zone_span_gate: {total} violation(s) across {len(data['crops'])} crops")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 tools/test_zone_span_gate.py`
Expected: every line `PASS ...`, final `all zone_span_gate tests passed`, exit 0.

- [ ] **Step 5: RED proof on current canonical (expected FAIL -- this is the point)**

Run: `python3 tools/zone_span_gate.py crops_data_final.json; echo "exit=$?"`
Expected: violations on every populated crop (stale spans on the 5 widened regions + int-typed/empty spans elsewhere), `exit=1`. Record the violation count -- Task 4 drives it to 0. If this unexpectedly PASSES, STOP: the canonical moved under you.

- [ ] **Step 6: Adversarial scratch proof (defect classes beyond staleness)**

The RED in Step 5 proves staleness detection. Now prove parity + donor detection against otherwise-CONFORMING data by injecting defects into a scratch copy that has been brought to the expected shape:

```bash
SCRATCH=/private/tmp/claude-501/-Users-trevorrawson-plant-dataset/72b69763-76dd-420b-9f85-d7e5d70203b3/scratchpad
python3 - <<'EOF'
import json, copy, subprocess, sys, os
SCRATCH = os.environ.get("SCRATCH", "/tmp") + "/a45_adversarial.json"
sys.path.insert(0, "tools")
from zone_span_gate import EXPECTED_SPANS, DONORS

data = json.load(open("crops_data_final.json", encoding="utf-8"))
# Bring every populated cell to the expected shape (mini-widen, clone donors).
for crop in data["crops"]:
    for rid, cell in (crop.get("regions") or {}).items():
        rbz = cell.get("resolved_by_zone") or {}
        if not rbz or rid not in EXPECTED_SPANS:
            continue
        for new, donor in (DONORS.get(rid) or {}).items():
            if new not in rbz and donor in rbz:
                row = copy.deepcopy(rbz[donor]); row["lifted_from_zone"] = donor
                rbz[new] = row
        cell["zone_span"] = list(EXPECTED_SPANS[rid])

# Defect 1: span/key mismatch -- drop tomato's cloned az z10 row, keep the span.
tom = next(c for c in data["crops"] if c["slug"] == "cherry-tomato")
del tom["regions"]["low_desert_az"]["resolved_by_zone"]["10"]
# Defect 2: divergent span on one crop.
tom["regions"]["se_gulf"]["zone_span"] = ["8", "9"]
# Defect 3: dangling donor pointer.
tom["regions"]["ca_desert"]["resolved_by_zone"]["11"]["lifted_from_zone"] = "99"

json.dump(data, open(SCRATCH, "w", encoding="utf-8"),
          separators=(",", ":"), ensure_ascii=False)
r = subprocess.run([sys.executable, "tools/zone_span_gate.py", SCRATCH],
                   capture_output=True, text=True)
hits = [l for l in r.stdout.splitlines() if l.startswith("VIOLATION")]
tom_hits = [l for l in hits if "cherry-tomato" in l]
assert r.returncode == 1, "gate must exit 1"
assert len(tom_hits) == 3, f"expected exactly 3 injected defects caught, got:\n" + "\n".join(hits[:20])
assert all("cherry-tomato" in l for l in hits), "only injected defects may fire on conformed data"
print("adversarial proof: 3 injected defect classes caught, zero false positives")
EOF
```

Expected: `adversarial proof: 3 injected defect classes caught, zero false positives`. Delete the scratch file afterward.

- [ ] **Step 7: Commit (gate is standalone; A45 wiring lands with the widen in Task 4)**

```bash
git add tools/zone_span_gate.py tools/test_zone_span_gate.py
git commit -m "feat(gate): zone_span parity gate (A45 module, unwired; RED on pre-widen canonical)

Expected-span table + span<->resolved_by_zone parity + lifted_from_zone donor
integrity. Adversarially proven (3 defect classes injected on conformed scratch,
0 FP). Wiring into whole_crop_gate lands with the widen promote.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 2: Provenance audits for the clone claim (HI + CA; AZ and se_gulf done at spec time)

**Files:**
- Create: `<scratchpad>/zonespan_audit_notes.md` (working notes; final home is the roadmap doc in Task 5)

**Interfaces:**
- Consumes: canonical JSON (read-only).
- Produces: a go/no-go per widened region + 2-4 sentence audit summary per region, pasted into the roadmap doc's "clone honesty" section (Task 5) and the STATE_HISTORY entry (Task 6). If any region FAILS its audit, STOP and surface to Trevor before Task 3 -- do not widen a region whose calendars were not written for the relabeled city.

The clone claim (spec section 2): each widened region's calendars were already authored for the city the 2023 map relabeled, so the donor row IS that city's data. Verified for `low_desert_az` (UA az2078 + Maricopa az1005) and `se_gulf` (clemson/uga/ncsu/uf/lsu/msstate/tamu belt) during spec work. Remaining: `hawaii_tropical`, `ca_south_coast`, `ca_desert`.

- [ ] **Step 1: Hawaii audit -- year-round resolution + CTAHR sourcing**

```bash
python3 - <<'EOF'
import json
from collections import Counter
d = json.load(open("crops_data_final.json", encoding="utf-8"))
methods, srcs, cal_shapes = Counter(), Counter(), Counter()
for c in d["crops"]:
    cell = (c.get("regions") or {}).get("hawaii_tropical")
    if not cell or not cell.get("resolved_by_zone"):
        continue
    for z, row in cell["resolved_by_zone"].items():
        methods[row.get("resolution_method")] += 1
        for s in row.get("sources") or []:
            srcs[s] += 1
        cal = row.get("calendar") or []
        cal_shapes["year_round_growing" if set(cal) <= {"growing"} else "seasonal"] += 1
print("resolution methods:", methods.most_common())
print("top sources:", srcs.most_common(8))
print("calendar shapes:", cal_shapes.most_common())
EOF
```

PASS criteria: methods dominated by `ctahr_year_round_resolution` (or other explicitly Hawaii-authored methods), sources dominated by CTAHR/UH ids, and NO method that computes from `zone_frost_data` (nothing in tools/ reads `zone_frost_data` at all -- verified 2026-07-12 -- but the method NAMES must not imply per-zone frost anchoring either). Seasonal (non-year-round) calendar shapes are fine IF their months are Hawaii-authored (elevation/wet-season logic), because donor z11 -> z10/z12/z13 then carries the same Hawaii-wide guidance. Record the numbers.

- [ ] **Step 2: CA south coast + desert audit -- donor z10 is the warm edge**

```bash
python3 - <<'EOF'
import json
from collections import Counter
d = json.load(open("crops_data_final.json", encoding="utf-8"))
for rid in ("ca_south_coast", "ca_desert"):
    srcs, differs = Counter(), 0
    n = 0
    for c in d["crops"]:
        cell = (c.get("regions") or {}).get(rid)
        rbz = (cell or {}).get("resolved_by_zone") or {}
        if not rbz:
            continue
        n += 1
        for z, row in rbz.items():
            for s in row.get("sources") or []:
                srcs[s] += 1
        r9, r10 = rbz.get("9"), rbz.get("10")
        if r9 and r10 and (r9.get("plant_out") != r10.get("plant_out")
                           or r9.get("calendar") != r10.get("calendar")):
            differs += 1
    print(f"{rid}: {n} crops; z9 vs z10 differ on {differs}; sources {srcs.most_common(6)}")
EOF
```

PASS criteria: sources are CA-authored (UC ANR / UCCE / master-gardener ids). The `differs` count is INFORMATIVE: if z9 and z10 already differ per-crop, the region encodes real per-zone gradients and cloning z10 (the warm edge) to z11 is the right donor direction; if they are mostly identical, the region is effectively zone-flat and the clone is trivially safe. Either outcome passes; a FAIL is CA cells sourced from non-CA extensions or a z10 row that is systematically COOLER-scheduled than z9 (would mean z10 is not the warm edge; check 3 sample crops by eye).

- [ ] **Step 3: Heat-pause spot check on the two hot widens (AZ z10, se_gulf z10)**

The one biology risk in a hotter-label clone is an understated summer pause. The donor rows were authored for the relabeled cities themselves (Phoenix, Gulf belt incl. New Orleans), so shifts are NOT expected; verify on the two most heat-sensitive certified crops:

```bash
python3 - <<'EOF'
import json
d = json.load(open("crops_data_final.json", encoding="utf-8"))
for slug in ("lettuce-leaf", "cherry-tomato"):
    c = next(x for x in d["crops"] if x["slug"] == slug)
    for rid, dz in (("low_desert_az", "9"), ("se_gulf", "9")):
        row = c["regions"][rid]["resolved_by_zone"][dz]
        hp = row.get("heat_pause") or {}
        print(f"{slug} {rid} z{dz}: heat_pause months={hp.get('months')} "
              f"plant_out={row.get('plant_out')}")
EOF
```

PASS criteria: both crops carry an explicit summer `heat_pause` (months within May-Sep) in both donor rows -- i.e. the donors already encode the hot-summer reality the new zone label describes. Record the months. If a donor row for a heat-sensitive crop has NO heat pause, flag that crop in the audit notes (it passes A28 today, so absence means the authored windows already avoid summer; note it, do not block).

- [ ] **Step 4: Write the audit note + go/no-go**

Write `<scratchpad>/zonespan_audit_notes.md` with, per widened region: the numbers from Steps 1-3, the 2-4 sentence conclusion, and GO or NO-GO. All five regions must be GO before Task 3. No commit (working notes; content lands in Task 5's roadmap doc).

---

### Task 3: Widen patch builder + tests

**Files:**
- Create: `tools/build_zonespan_widen_patch.py`
- Create: `tools/test_build_zonespan_widen_patch.py`

**Interfaces:**
- Consumes: `zone_span_gate.EXPECTED_SPANS` / `zone_span_gate.DONORS` (import them -- the gate and builder must never disagree).
- Produces: `build_widen_ops(data) -> list[dict]` (apply_patch-format op dicts) and, via `main()`, the SHA-guarded batch file `tools/batches/zonespan_widen.json`.

Op semantics (apply_patch canonical format, `tools/apply_patch.py` docstring):
- For every crop x region with populated `resolved_by_zone` and a `DONORS` entry: one `add` op per missing new zone: `{"op": "add", "json_path": "$.crops[?(@.slug=='<slug>')].regions.<rid>.resolved_by_zone.<zone>", "value": <deepcopy of donor row with lifted_from_zone set to the donor zone str>}`.
- For every crop x region with populated `resolved_by_zone` where `zone_span != EXPECTED_SPANS[rid]`: one `replace` op: `{"op": "replace", "json_path": "$.crops[?(@.slug=='<slug>')].regions.<rid>.zone_span", "from": <current value verbatim>, "value": EXPECTED_SPANS[rid]}`. Skip no-ops (already-correct spans emit nothing).
- Nothing else. No other keys, no other crops, no shells invented.

- [ ] **Step 1: Write the failing test**

```python
#!/usr/bin/env python3
"""Unit test for build_zonespan_widen_patch -- op emission on synthetic fixtures.
Run from repo root: python3 tools/test_build_zonespan_widen_patch.py
"""
import copy, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_zonespan_widen_patch import build_widen_ops
from zone_span_gate import EXPECTED_SPANS, DONORS, check_crop

DONOR_ROW = {"plant_out": "Mar 1 - Mar 21", "calendar": ["plant"] * 12,
             "zone_notes": None, "lifted_from_zone": None,
             "sources": ["uariz_ext"]}

def stale_crop(slug="alpha"):
    """Pre-widen shapes: stale spans, one int-typed, one empty."""
    regions = {
        "low_desert_az": {"zone_span": ["9"],
                          "resolved_by_zone": {"9": copy.deepcopy(DONOR_ROW)}},
        "warm_arid":     {"zone_span": [8],      # int-typed
                          "resolved_by_zone": {"8": copy.deepcopy(DONOR_ROW)}},
        "fl_peninsula":  {"zone_span": [],       # empty but populated
                          "resolved_by_zone": {"10": copy.deepcopy(DONOR_ROW),
                                                "11": copy.deepcopy(DONOR_ROW)}},
        "ca_interior":   {"zone_span": ["8", "9"],   # already correct -> no op
                          "resolved_by_zone": {"8": copy.deepcopy(DONOR_ROW),
                                                "9": copy.deepcopy(DONOR_ROW)}},
    }
    return {"slug": slug, "regions": regions}

fails = []
def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)

data = {"crops": [stale_crop()]}
ops = build_widen_ops(data)
by_path = {o["json_path"]: o for o in ops}

# 1. Clone op for az z10, donor row copied with lifted_from_zone set.
p = "$.crops[?(@.slug=='alpha')].regions.low_desert_az.resolved_by_zone.10"
check("az z10 clone emitted", p in by_path and by_path[p]["op"] == "add")
row = by_path[p]["value"]
check("clone marked lifted_from_zone=9", row["lifted_from_zone"] == "9")
check("clone copies donor content", row["plant_out"] == DONOR_ROW["plant_out"])
check("clone is a COPY not a reference",
      row is not data["crops"][0]["regions"]["low_desert_az"]["resolved_by_zone"]["9"])

# 2. Span replaces: stale, int-typed, empty all normalized; correct one skipped.
sp = lambda rid: f"$.crops[?(@.slug=='alpha')].regions.{rid}.zone_span"
check("stale az span replaced", by_path[sp("low_desert_az")]["value"] == ["9", "10"])
check("stale az from-guard verbatim", by_path[sp("low_desert_az")]["from"] == ["9"])
check("int span normalized", by_path[sp("warm_arid")]["value"] == ["8"]
      and by_path[sp("warm_arid")]["from"] == [8])
check("empty span filled", by_path[sp("fl_peninsula")]["value"] == ["10", "11"])
check("correct span skipped (no-op)", sp("ca_interior") not in by_path)

# 3. Non-widened regions get NO clone ops.
check("no clone into fl_peninsula",
      not any("fl_peninsula.resolved_by_zone" in q for q in by_path))

# 4. Idempotency: applying the ops mentally then re-building emits zero ops.
widened = copy.deepcopy(data)
for rid, cell in widened["crops"][0]["regions"].items():
    for new, donor in (DONORS.get(rid) or {}).items():
        r = copy.deepcopy(cell["resolved_by_zone"][donor]); r["lifted_from_zone"] = donor
        cell["resolved_by_zone"][new] = r
    cell["zone_span"] = list(EXPECTED_SPANS[rid])
check("idempotent (widened input -> zero ops)", build_widen_ops(widened) == [])

# 5. The widened synthetic crop passes the A45 gate (builder and gate agree).
check("widened crop passes A45", check_crop(widened["crops"][0]) == [])

# 6. Crop without regions -> zero ops, no crash.
check("regionless crop no-ops", build_widen_ops({"crops": [{"slug": "x"}]}) == [])

if fails:
    print(f"\n{len(fails)} test(s) FAILED"); sys.exit(1)
print("\nall build_zonespan_widen_patch tests passed")
```

- [ ] **Step 2: Run to verify it fails**

Run: `python3 tools/test_build_zonespan_widen_patch.py`
Expected: `ModuleNotFoundError: No module named 'build_zonespan_widen_patch'`

- [ ] **Step 3: Implement the builder**

```python
#!/usr/bin/env python3
"""Emit the SHA-guarded apply_patch batch for the region zone-span widen
(spec docs/superpowers/specs/2026-07-12-region-zonespan-reconciliation-design.md).

The 2023 USDA map relabeled the cities the warm regions were authored FOR
(Phoenix 9b->10a, Honolulu ->z12, warm CA coast ->z11, New Orleans fringe ->z10),
so the fix is label reconciliation, not re-authoring: clone the donor zone's
resolved row to the new zone label (marked with the established lifted_from_zone
idiom -- the row IS that city's data) and normalize every populated zone_span to
the canonical str-typed value from zone_span_gate.EXPECTED_SPANS.

Footprint: zone_span (normalize) + new resolved_by_zone keys in the 5 widened
regions, across every crop with populated region rows. Nothing else moves.

Run: python3 tools/build_zonespan_widen_patch.py
Then: python3 tools/apply_patch.py tools/batches/zonespan_widen.json
"""
import copy
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zone_span_gate import EXPECTED_SPANS, DONORS

CANON = "crops_data_final.json"
OUT = "tools/batches/zonespan_widen.json"


def build_widen_ops(data):
    """Pure op builder: list of apply_patch ops taking `data` to the widened,
    normalized shape. Idempotent: widened input -> []."""
    ops = []
    for crop in data.get("crops", []):
        slug = crop.get("slug")
        for rid, cell in (crop.get("regions") or {}).items():
            rbz = cell.get("resolved_by_zone") or {}
            if not rbz or rid not in EXPECTED_SPANS:
                continue
            base = f"$.crops[?(@.slug=='{slug}')].regions.{rid}"
            for new, donor in sorted((DONORS.get(rid) or {}).items()):
                if new in rbz or donor not in rbz:
                    continue
                row = copy.deepcopy(rbz[donor])
                row["lifted_from_zone"] = donor
                ops.append({"op": "add",
                            "json_path": f"{base}.resolved_by_zone.{new}",
                            "value": row})
            expected = EXPECTED_SPANS[rid]
            if cell.get("zone_span") != expected:
                ops.append({"op": "replace", "json_path": f"{base}.zone_span",
                            "from": cell.get("zone_span"),
                            "value": list(expected)})
    return ops


def main():
    raw = open(CANON, "rb").read()
    data = json.loads(raw.decode("utf-8"))
    ops = build_widen_ops(data)
    if not ops:
        print("no-op: canonical is already widened + normalized")
        return
    patch = {"base_sha": hashlib.sha256(raw).hexdigest(), "patches": ops}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(patch, f, separators=(",", ":"), ensure_ascii=False)
    clones = sum(1 for o in ops if o["op"] == "add")
    spans = sum(1 for o in ops if o["op"] == "replace")
    print(f"wrote {OUT}: {clones} cloned zone rows + {spans} zone_span "
          f"normalizations across {len({o['json_path'].split(chr(39))[1] for o in ops})} crops")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 tools/test_build_zonespan_widen_patch.py`
Expected: all `PASS`, exit 0. Also re-run `python3 tools/test_zone_span_gate.py` (still green).

- [ ] **Step 5: Commit**

```bash
git add tools/build_zonespan_widen_patch.py tools/test_build_zonespan_widen_patch.py
git commit -m "build(regions): zone-span widen patch builder (clone donor rows, normalize spans)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 4: Apply on scratch, verify everything, wire A45, promote

**Files:**
- Modify: `tools/whole_crop_gate.py` (insert A45 block after the A44 block, which ends near line 672)
- Modify: `crops_data_final.json` (the promote -- ONLY via the verified scratch)
- Create: `tools/batches/zonespan_widen.json` (builder output, committed as the audit trail)

**Interfaces:**
- Consumes: Task 1's gate (module + standalone runner), Task 3's builder, `tools/apply_patch.py`, `tools/release_verify.py`, `tools/gate_all.py`.
- Produces: widened canonical; A45 live in the always-on suite.

- [ ] **Step 1: Build the patch and apply to scratch**

```bash
python3 tools/build_zonespan_widen_patch.py
python3 tools/apply_patch.py tools/batches/zonespan_widen.json \
        --out crops_data_final.scratch.json
```

Expected: builder reports clone + normalization counts (order of magnitude: 117 crops x 7 new zone rows = ~819 clones; span replaces = 5 widened regions x 117 + the int-typed/empty spans elsewhere, several hundred). apply_patch exits 0 and reports a footprint confined to `regions.*.zone_span` + `regions.*.resolved_by_zone.<new zones>`. Any from-guard failure = STOP and investigate; do not force.

- [ ] **Step 2: Gate the scratch (A45 goes GREEN here -- the other half of Task 1's RED)**

```bash
python3 tools/zone_span_gate.py crops_data_final.scratch.json
```

Expected: `0 violation(s)`, exit 0. (Task 1 Step 5 proved the same gate exits 1 on pre-widen canonical.)

- [ ] **Step 3: Compact-format + footprint verification on scratch**

```bash
python3 - <<'EOF'
import json, sys
a = json.load(open("crops_data_final.json", encoding="utf-8"))
b = json.load(open("crops_data_final.scratch.json", encoding="utf-8"))
raw = open("crops_data_final.scratch.json", "rb").read()
assert b"\n" not in raw and b": " not in raw[:2000], "scratch is not COMPACT"
diffs = []
za, zb = a["crops"], b["crops"]
assert len(za) == len(zb) == 125
for ca, cb in zip(za, zb):
    assert ca["slug"] == cb["slug"]
    for k in set(ca) | set(cb):
        if k == "regions":
            for rid in set(ca.get(k) or {}) | set(cb.get(k) or {}):
                ra, rb = (ca[k] or {}).get(rid, {}), (cb[k] or {}).get(rid, {})
                for f in set(ra) | set(rb):
                    if ra.get(f) != rb.get(f):
                        assert f in ("zone_span", "resolved_by_zone"), \
                            f"{ca['slug']}.{rid}.{f} moved -- outside footprint"
                        if f == "resolved_by_zone":
                            for z in set(ra.get(f) or {}) | set(rb.get(f) or {}):
                                if (ra.get(f) or {}).get(z) != (rb.get(f) or {}).get(z):
                                    assert z not in (ra.get(f) or {}), \
                                        f"{ca['slug']}.{rid} z{z}: EXISTING row modified"
                        diffs.append((ca["slug"], rid, f))
        elif ca.get(k) != cb.get(k):
            raise AssertionError(f"{ca['slug']}.{k} moved -- outside footprint")
for k in set(a) | set(b):
    if k != "crops":
        assert a.get(k) == b.get(k), f"top-level {k} moved"
print(f"footprint clean: {len(diffs)} region-cell changes, zone_span/resolved_by_zone only, "
      f"no existing row modified, top-level untouched")
EOF
```

Expected: `footprint clean: ...`. Any assertion = STOP.

- [ ] **Step 4: Clone-fidelity source-truth sample (protocol's per-batch sample, adapted)**

The widen introduces NO new claims, so the sample verifies clone fidelity: pick 5 cloned rows across the 5 regions and diff against their donors:

```bash
python3 - <<'EOF'
import json
b = json.load(open("crops_data_final.scratch.json", encoding="utf-8"))
PICKS = [("cherry-tomato", "low_desert_az", "10", "9"),
         ("lettuce-leaf", "se_gulf", "10", "9"),
         ("carrot", "hawaii_tropical", "12", "11"),
         ("basil", "ca_south_coast", "11", "10"),
         ("zucchini-courgette", "ca_desert", "11", "10")]
for slug, rid, new, donor in PICKS:
    c = next(x for x in b["crops"] if x["slug"] == slug)
    rbz = c["regions"][rid]["resolved_by_zone"]
    n, d = dict(rbz[new]), dict(rbz[donor])
    lifted = n.pop("lifted_from_zone")
    d.pop("lifted_from_zone")
    assert n == d, f"{slug} {rid} z{new} diverges from donor beyond the marker"
    assert lifted == donor
    print(f"OK {slug} {rid}: z{new} == z{donor} + lifted_from_zone={lifted!r}")
EOF
```

Expected: 5x `OK`. (If a picked slug is absent, substitute any certified crop -- the roster list is in CURRENT_STATE.md.)

- [ ] **Step 5: Wire A45 into whole_crop_gate.py**

In `tools/whole_crop_gate.py`, directly after the A44 block (search for `_layout = _layout_violations(crop)`; insert after its `for m in _layout:` loop), add:

```python
# ---------------- A45. region zone_span parity (spec 2026-07-12) ----------------
# The 2023 USDA map relabeled the marquee cities (Phoenix 9b->10a, Honolulu ->z12) and
# NOTHING read zone_span, so spans went silently stale and 300+ ZIPs lost region
# resolution in the app. Pins every populated region cell to the canonical str-typed
# span (zone_span_gate.EXPECTED_SPANS) + requires resolved_by_zone key parity +
# lifted_from_zone donor integrity. Widening a span is a deliberate paired edit:
# EXPECTED_SPANS + cloned rows together. No-op on unpopulated shells.
from zone_span_gate import check_crop as _zonespan_violations
print("A45. region zone_span parity (expected span + resolved_by_zone key parity + donor integrity)")
_zsp = _zonespan_violations(crop)
print(f"  zone_span violations: {len(_zsp)}")
for m in _zsp:
    fail(f"zone-span: {m}")
```

- [ ] **Step 6: Full suite on scratch**

```bash
python3 tools/whole_crop_gate.py cherry-tomato crops_data_final.scratch.json | tail -3
python3 tools/gate_all.py crops_data_final.scratch.json | tail -3
python3 tools/release_verify.py crops_data_final.scratch.json \
        --base crops_data_final.json | tail -25
```

Expected: whole_crop_gate `GATE: PASS` with A45 listed; `gate_all: PASS -- every certified crop passes the whole suite` (116 certified); release_verify exit 0 (its diff checks A+B run because `--base` is given). Only pre-existing benign residue noted in CURRENT_STATE.md is acceptable (the onion release noted benign region-cell residue); anything new = STOP.

- [ ] **Step 7: Promote scratch -> canonical**

```bash
mv crops_data_final.scratch.json crops_data_final.json
shasum -a 256 crops_data_final.json   # record NEW_SHA for Task 6
python3 tools/zone_span_gate.py && python3 tools/gate_all.py | tail -2
python3 tools/test_zone_span_gate.py && python3 tools/test_build_zonespan_widen_patch.py
```

Expected: gate + suite green on the real canonical; both test files green.

- [ ] **Step 8: Commit (content + gate wiring together; pre-commit hook will run release-verify)**

```bash
git add crops_data_final.json tools/whole_crop_gate.py tools/batches/zonespan_widen.json
git commit -m "feat(regions): 2023-map zone-span reconciliation (5 regions widened, A45 live)

low_desert_az 9->9-10 (Phoenix), hawaii_tropical 11->10-13 (Honolulu),
ca_south_coast/ca_desert +11, se_gulf +10 (New Orleans fringe; RGV rides
se_gulf as the documented interim). Cloned donor rows marked lifted_from_zone;
every populated zone_span normalized str-typed. ~320 ZIPs regain region
resolution. Spec 2026-07-12-region-zonespan-reconciliation-design.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 5: Region coverage roadmap doc

**Files:**
- Create: `docs/region_coverage_roadmap.md`

**Interfaces:**
- Consumes: Task 2's audit notes (paste the per-region audit summaries into section "Clone honesty record"); Task 4's actual op counts (fill the two `<N>` slots).

- [ ] **Step 1: Write the doc**

Write `docs/region_coverage_roadmap.md` with exactly this content, filling `<N clones>`/`<N spans>` from Task 4 Step 1's builder output and pasting Task 2's audit summaries where marked:

```markdown
# Region coverage roadmap -- ZIP -> zone -> region -> dates, the whole chain

**Origin:** docs/2026-07-12-region-zonespan-gaps.md (plant-app sweep) +
docs/superpowers/specs/2026-07-12-region-zonespan-reconciliation-design.md.
**Goal (Trevor, 2026-07-12):** a user types their ZIP and gets their proper,
up-to-date zone AND region with correct planting information.

Every gap from the sweep carries one of four rulings: WIDENED (fixed by item 1) /
NEW REGION (queued) / GENERIC-OK (generic zone dates are the deliberate answer) /
HANDED OFF (different owner, first-class item here, not a footnote).

## The program

| # | Item | Owner | Status | Impact |
|---|------|-------|--------|--------|
| 1 | Zone-span widen (2023-map reconciliation, A45 gate) | dataset | SHIPPED 2026-07-12 | ~320 ZIPs regain region resolution |
| 2 | App-side cleanup: ~285 empty-state ZIP rows in zip-zones.json; verify the regions.json sync path end to end; decide TX z10 ZIP3 fencing (keep RGV on se_gulf interim vs fence to generic until item 3) | plant-app | QUEUED (next) | ~285 ZIPs broken regardless of spans until fixed |
| 3 | Rio Grande Valley / subtropical TX region (new authored region; TAMU AgriLife RGV calendars are strong T1) | dataset | QUEUED | 95 ZIPs off the se_gulf interim |
| 4 | Maritime PNW region (WA/OR z8-9; WSU/OSU extension T1) | dataset | QUEUED | ~750 ZIPs; generic frost-anchored dates are most misleading here (cool summers) |
| 5 | Judged later, each needs an explicit ruling: mid-Atlantic z8 belt (NC 793 / VA 258 / MD 117 / DC 215 / DE-NJ-PA small), mid-South (AR 460 / OK 106 / TN 123 / MO 6), NV (110) / UT (15) / AK (13) | dataset | OPEN | GENERIC-OK is a legitimate ruling where honest |
| 6 | Puerto Rico (2 z11 / 47 z12 / 126 z13) | product call (Trevor) | OPEN | market-scope question first; needs z12/13 support end to end (zone_frost_data has no z12/13 rows; nothing in tools/ reads it, so dataset-side this is only a data gap, but app generic-date rendering for z12/13 must be checked) |

Items 3+ are their own arcs (spec -> plan -> build). Nothing below item 2 blocks item 2.

## Item 1 record: the widen (SHIPPED 2026-07-12)

| Region | Span change | Donor | ZIPs |
|---|---|---|---|
| low_desert_az | [9] -> [9,10] | z10 <- z9 | 71 (Phoenix metro) |
| hawaii_tropical | [11] -> [10,11,12,13] | all <- z11 | 122 (Honolulu +) |
| ca_south_coast | [9,10] -> [9,10,11] | z11 <- z10 | 28 (coastal LA/SD; |
| ca_desert | [9,10] -> [9,10,11] | z11 <- z10 | app picks by ZIP3) |
| se_gulf | [8,9] -> [8,9,10] | z10 <- z9 | 6 (New Orleans fringe) |

Mechanics: `tools/build_zonespan_widen_patch.py` -> `tools/batches/zonespan_widen.json`
(<N clones> cloned rows + <N spans> span normalizations) -> `tools/apply_patch.py`.
Every cloned row carries `lifted_from_zone: "<donor>"` (the established idiom; 6
prior instances, e.g. lettuce-leaf se_gulf z8 <- z9). Every populated `zone_span`
is now str-typed and uniform, enforced by A45 (`tools/zone_span_gate.py`:
expected-span table + span<->resolved_by_zone key parity + donor integrity).
Widening a span is now a deliberate paired edit: EXPECTED_SPANS + cloned rows.

**Why cloning is honest here:** the 2023 USDA map relabeled the cities these
regions were authored FOR; the climates and calendars did not change. Phoenix
(relabeled 9b->10a) is what low_desert_az's UA az2078 / Maricopa az1005 calendars
describe; Honolulu (->z12) is what the CTAHR guidance describes; the warm CA
coast pockets (->z11) are the warm edge of the z10 rows; the New Orleans fringe
(->z10) sits inside se_gulf's LSU-sourced belt.

### Clone honesty record (per-region audits)

<PASTE Task 2 audit summaries here: hawaii_tropical, ca_south_coast, ca_desert,
plus the spec-time findings for low_desert_az and se_gulf, and the heat-pause
spot-check numbers. 2-4 sentences each + GO.>

## The RGV interim ruling (Trevor-approved 2026-07-12)

Widening se_gulf to z10 auto-matches the 95 TX Rio Grande Valley z10 ZIPs
(TX is in the app's se_gulf state mapping). This ships as an EXPLICITLY INTERIM
answer: Gulf-coast winter-garden dates are directionally right for RGV and
better than a bare zone label, and se_gulf's source set already includes
tamu_agrilife. Item 3 replaces it with a real RGV region; item 2 may instead
fence TX z10 via ZIP3 hints if the app side prefers generic dates meanwhile.

## Tier-2 rulings pending (item 5 detail)

The taxonomy deliberately special-cases marquee warm states; everywhere else
gets generic frost-anchored zone dates. Where that is honest, GENERIC-OK is the
ruling, recorded here -- not silence. First reads (to be confirmed each in its
own pass): maritime PNW = NOT ok (cool summers invert the assumptions; item 4).
Mid-Atlantic z8 = probably ok (humid continental-lite; generic frost anchoring
is close). Mid-South z8 = probably ok. NV/UT z8-9 = probably ok (warm_arid
adjacency worth a look). AK z8 (13 ZIPs, maritime) = probably ok at this scale.

## Empty-state ZIPs (item 2 detail)

~285 rows in zip-zones.json carry an empty state string (109 z8, 128 z9, 40 z10,
7 z11, 1 z12). State-based region matching can never fire for them, spans
notwithstanding. Owner: plant-app (regenerate or backfill the state column;
check how the rows were generated).
```

- [ ] **Step 2: Verify doc rules**

Run: `grep -c $'—' docs/region_coverage_roadmap.md`
Expected: `0` (no em dashes; `--` only). Confirm both `<N>` slots and the audit-paste marker are filled with real content (grep for `<` placeholders: `grep -n "<PASTE\|<N " docs/region_coverage_roadmap.md` -> no hits).

- [ ] **Step 3: Commit**

```bash
git add docs/region_coverage_roadmap.md
git commit -m "docs(regions): region coverage roadmap (6-item program, owner column, rulings)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 6: State trio + wrap

**Files:**
- Modify: `CURRENT_STATE.md` (SURGICAL hand edit -- do NOT run gen_current_state.py; a naive regen corrupts it)
- Modify: `STATE_HISTORY.md` (append at TOP -- most-recent first)
- Modify: `LATEST.txt`

**Interfaces:**
- Consumes: NEW_SHA from Task 4 Step 7; op counts from Task 4; audit summaries from Task 2.

- [ ] **Step 1: Read the current state files first**

Read `CURRENT_STATE.md` (header/protocol + wherever the gate roster and canonical SHA appear) and the top entry of `STATE_HISTORY.md` to match their exact formats. Follow the SESSION PROTOCOL in CURRENT_STATE.md's header if it adds steps beyond this plan.

- [ ] **Step 2: Update CURRENT_STATE.md surgically**

Minimal edits only: (a) canonical SHA -> NEW_SHA; (b) add A45 to the gate list where A43/A44 are described (one line, same style: `A45 region zone_span parity -- expected-span table + resolved_by_zone key parity + lifted_from_zone donor integrity; tools/zone_span_gate.py`); (c) if a "recent sessions" / "what changed" prose slot exists, one sentence: `2026-07-12 zone-span widen: 5 regions reconciled to the 2023 USDA map (Phoenix/Honolulu/CA-coast/NOLA), ~320 ZIPs regain region resolution, RGV rides se_gulf interim, roadmap at docs/region_coverage_roadmap.md.` Nothing else moves.

- [ ] **Step 3: Append STATE_HISTORY.md (at the top, matching house format)**

Entry must carry: date 2026-07-12, session name (ZONE-SPAN WIDEN / 2023-MAP RECONCILIATION), old SHA `e45bcf3c...` -> NEW_SHA, crop count 125 unchanged / 116 certified unchanged, the 5 span changes + donor map, op counts, A45 gate live (module + wiring + adversarial proof), the RGV interim ruling (Trevor-approved), roadmap doc path, audit GO summaries, and the standing handoffs: push = Trevor; plant-astro bump = astro session; item 2 (empty-state ZIPs + sync-path verify + ZIP3 fencing) = plant-app session; leek pilot now unblocked (rebase its plan onto NEW_SHA).

- [ ] **Step 4: Bump LATEST.txt**

Match its existing 3-line format exactly (SHA / Date / Session): NEW_SHA, `2026-07-12`, and a Session line in the house style summarizing this release (see STATE_HISTORY entry; LATEST.txt sessions are long-form -- mirror the Task 6 Step 3 content).

- [ ] **Step 5: Verify the trio + full suite one last time**

```bash
shasum -a 256 crops_data_final.json   # must equal the SHA line in LATEST.txt
python3 tools/gate_all.py | tail -2
python3 tools/zone_span_gate.py | tail -1
```

Expected: SHA matches; `gate_all: PASS`; `0 violation(s)`.

- [ ] **Step 6: Commit**

```bash
git add CURRENT_STATE.md STATE_HISTORY.md LATEST.txt
git commit -m "chore(state): state trio for the zone-span widen release

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

- [ ] **Step 7: Final summary for Trevor (NO push)**

Report: the 5 widened regions + ZIP impact, A45 live, op counts, audit outcomes, the roadmap's 6 items with item 2 (plant-app) as the next action, leek pilot unblocked (its plan needs a base-SHA rebase), and that push + plant-astro bump await his confirmation.
