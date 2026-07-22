# Pest / IPM Control-Ladder Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the pilot for the pest/IPM control-ladder foundation -- a shared `control_methods` catalog, per-problem softest-first `control_ladder`, stable pest/disease `id`, a `pesticide_safety_education` object, and a new `control_ladder_gate` -- authored into broccoli, microgreens, and celery.

**Architecture:** A new standalone gate (`tools/control_ladder_gate.py`, TDD, soft/standalone) enforces catalog integrity, ladder integrity (referential + monotonic-tier + applies_to coherence), and identity (unique id). Content (the catalog, the safety object, and three crops' ladders) is authored from T1 extension IPM sources and spliced into the compact canonical via SHA-guarded `apply_patch.py`. The gate stays soft through the pilot; it hard-flips into A39 + `gate_all` only after the roster-wide rollout (a separate, later plan).

**Tech Stack:** Python 3 (stdlib only, matching the other gates), pytest-free assertion tests run via `python3 tools/test_*.py`, `apply_patch.py` for canonical splices.

Design spec: `docs/superpowers/specs/2026-07-22-pest-ipm-ladder-design.md`.

## Global Constraints

- **Canonical JSON is COMPACT.** Never hand-edit or reformat `crops_data_final.json`. All content changes go through `tools/apply_patch.py` (writes with `separators=(",",":")`, `ensure_ascii=False`, no trailing newline). READ-ONLY otherwise.
- **SHA-guarded splices.** Every patch carries `base_sha` = `shasum -a 256 crops_data_final.json`. A concurrent session is running the Utah region arc on the SAME checkout; pest keys (`pests`/`diseases`/new top-level) are disjoint from region keys (`regions.*`), but always `git add` with explicit pathspec, `git status -sb` before commit, `git show --stat` after.
- **Commits are Trevor-gated.** Per CLAUDE.md, no commit or push without Trevor's approval. The `Commit` steps below are checkpoints where Trevor approves, not autonomous actions.
- **TDD, RED before GREEN.** Every gate check gets a failing test first. Before trusting the gate, inject each defect class into a SCRATCH copy of the real canonical and confirm it bounces (Task 10).
- **All new content is T1.** Catalog methods + ladder notes cite `source_catalog` entries with `tier == "T1"` (UC IPM `ucanr` is the gold standard). New sources get a `source_catalog` entry.
- **Consumer-copy rules.** No em dashes (use commas/colons/semicolons/periods). American English. Temps render `°F`. "plant" lowercase except sentence-start / "Plant Pro".
- **The 5-rung tier order is fixed:** `cultural` < `physical` < `biological` < `soft_chemical` < `conventional`.

---

### Task 1: Gate module + catalog-integrity validation

**Files:**
- Create: `tools/control_ladder_gate.py`
- Create: `tools/test_control_ladder_gate.py`

**Interfaces:**
- Produces: `TIERS`, `TIER_RANK`, `TYPE_TARGETS`, `UNIVERSAL_TARGET`, `ID_RE`, `load(path)`, `catalog(data)`, `_problems(crop)`, `catalog_violations(data) -> list[str]`.

- [ ] **Step 1: Write the failing test**

```python
# tools/test_control_ladder_gate.py
#!/usr/bin/env python3
"""Tests for control_ladder_gate. Run: python3 tools/test_control_ladder_gate.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from control_ladder_gate import catalog_violations

def data(methods, crops=None, srcs=None):
    return {
        "control_methods": methods,
        "source_catalog": srcs or {"umn_ext": {"tier": "T1"}, "seed_co": {"tier": "T2"}},
        "crops": crops or [],
    }

def method(**over):
    m = {"name": "Insecticidal soap", "tier": "soft_chemical", "applies_to": ["insect_soft_bodied"],
         "how_it_works_beginner": "x", "how_it_works_seasoned": "x", "best_use": "x",
         "pros": ["low tox"], "cons": ["contact only"], "sources": ["umn_ext"],
         "anchoring_urls": {"umn_ext": {"url": "u", "verified": "2026-07-22"}}}
    m.update(over); return m

# clean catalog -> no violations
assert catalog_violations(data({"insecticidal_soap": method()})) == []
# missing required key
assert any("missing/empty" in v for v in catalog_violations(data({"insecticidal_soap": method(pros=[])})))
# invalid tier
assert any("invalid tier" in v for v in catalog_violations(data({"insecticidal_soap": method(tier="nuke")})))
# NB: catalog method KEYS are snake_case (mirroring source_catalog keys) -- NOT format-checked here.
# The kebab ID_RE check applies only to per-crop pest/disease `id` (Task 3 identity).
# source not in catalog
assert any("not in source_catalog" in v for v in catalog_violations(data({"m": method(sources=["ghost"], anchoring_urls={"ghost": {}})})))
# source not T1
assert any("not T1" in v for v in catalog_violations(data({"m": method(sources=["seed_co"], anchoring_urls={"seed_co": {}})})))
# anchoring_urls mismatch
assert any("anchoring_urls" in v for v in catalog_violations(data({"m": method(anchoring_urls={})})))
print("catalog_violations tests: OK")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tools/test_control_ladder_gate.py`
Expected: FAIL — `ModuleNotFoundError` / `ImportError: cannot import name 'catalog_violations'`.

- [ ] **Step 3: Write minimal implementation**

```python
# tools/control_ladder_gate.py
#!/usr/bin/env python3
"""control_ladder_gate -- the IPM pest/disease control-ladder honesty engine (spec 2026-07-22).

SOFT + standalone (overwinter_hardiness / variety_detail pattern) through the pilot; HARD-FLIPS into
whole_crop_gate A39 + gate_all when the roster-wide rollout reaches full coverage (INV-1).

  CATALOG   -- every control_methods entry has the required keys, a valid tier, non-empty pros/cons,
               and T1 catalogued sources.
  LADDER    -- every control_ladder is referentially sound, monotonic by tier (softest-first), and
               applies_to-coherent with the problem's `type`.
  IDENTITY  -- every pest/disease carries a unique kebab `id` within its crop.
Short ladders are VALID (a cultural-only ladder must pass); the gate never requires reaching `conventional`.

Usage: control_ladder_gate.py [PATH] [--coverage]
"""
import json, os, re, sys

TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
TIER_RANK = {t: i for i, t in enumerate(TIERS)}

# type -> the applies_to targets that legitimately apply to it
TYPE_TARGETS = {
    "insect":        {"insect_soft_bodied", "insect_chewing", "insect_boring", "insect_general"},
    "mite":          {"mite", "insect_general"},
    "mollusk":       {"mollusk"},
    "fungal":        {"fungal_foliar", "fungal_soilborne", "disease_general"},
    "bacterial":     {"bacterial", "disease_general"},
    "viral":         {"viral", "disease_general"},
    "physiological": {"physiological"},
    "nematode":      {"nematode"},
}
UNIVERSAL_TARGET = "any"   # cultural/physical practices that apply broadly
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

_REQ_METHOD = ("name", "tier", "applies_to", "how_it_works_beginner", "how_it_works_seasoned",
               "best_use", "pros", "cons", "sources", "anchoring_urls")


def load(path):
    with open(path) as f:
        return json.load(f)


def catalog(data):
    return data.get("control_methods") or {}


def _problems(crop):
    return list(crop.get("pests") or []) + list(crop.get("diseases") or [])


def catalog_violations(data):
    V = []
    cat = catalog(data)
    srcs = data.get("source_catalog") or {}
    for mid, m in cat.items():
        for k in _REQ_METHOD:
            if k not in m or m[k] in (None, "", [], {}):
                V.append(f"control_methods/{mid}: missing/empty required key '{k}'")
        if m.get("tier") not in TIER_RANK:
            V.append(f"control_methods/{mid}: invalid tier {m.get('tier')!r}")
        for s in (m.get("sources") or []):
            if s not in srcs:
                V.append(f"control_methods/{mid}: source '{s}' not in source_catalog")
            elif srcs[s].get("tier") != "T1":
                V.append(f"control_methods/{mid}: source '{s}' is not T1")
        if set(m.get("anchoring_urls") or {}) != set(m.get("sources") or []):
            V.append(f"control_methods/{mid}: anchoring_urls keys do not match sources")
    return V
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 tools/test_control_ladder_gate.py`
Expected: PASS — `catalog_violations tests: OK`.

- [ ] **Step 5: Commit** (Trevor-gated checkpoint)

```bash
git add tools/control_ladder_gate.py tools/test_control_ladder_gate.py
git status -sb
git commit -m "feat(pest-ipm): control_ladder_gate catalog-integrity check (TDD)"
git show --stat HEAD
```

---

### Task 2: Ladder-integrity validation (the three defenses)

**Files:**
- Modify: `tools/control_ladder_gate.py`
- Modify: `tools/test_control_ladder_gate.py`

**Interfaces:**
- Consumes: `catalog(data)`, `_problems(crop)`, `TIER_RANK`, `TYPE_TARGETS`, `UNIVERSAL_TARGET`.
- Produces: `ladder_violations(data, crop) -> list[str]`.

- [ ] **Step 1: Write the failing test** (append to the test file, above the final `print`)

```python
from control_ladder_gate import ladder_violations

CAT = {
    "rotate_crops":     {"name": "Rotation", "tier": "cultural", "applies_to": ["any"]},
    "insecticidal_soap":{"name": "Soap", "tier": "soft_chemical", "applies_to": ["insect_soft_bodied"]},
    "copper":           {"name": "Copper", "tier": "soft_chemical", "applies_to": ["fungal_foliar"]},
    "pyrethrin":        {"name": "Pyrethrin", "tier": "conventional", "applies_to": ["insect_general"]},
}
def crop(problems, key="pests"):
    return {"slug": "broccoli", key: problems}
def prob(**over):
    p = {"id": "aphids", "name": "Aphids", "type": "insect",
         "control_ladder": [{"method": "rotate_crops"}, {"method": "insecticidal_soap"}]}
    p.update(over); return p
def D(crop_obj):  # gate expects (data, crop)
    return ({"control_methods": CAT}, crop_obj)

# clean softest-first ladder -> no violations
assert ladder_violations(*D(crop([prob()]))) == []
# absent ladder -> not a ladder violation (coverage handles it)
assert ladder_violations(*D(crop([prob(control_ladder=None)]))) == []
# dangling method reference
assert any("unknown method" in v for v in ladder_violations(*D(crop([prob(control_ladder=[{"method": "ghost"}])]))))
# NON-monotonic: conventional before cultural
bad = [{"method": "pyrethrin"}, {"method": "rotate_crops"}]
assert any("softest-first" in v for v in ladder_violations(*D(crop([prob(control_ladder=bad)]))))
# applies_to mismatch: insecticidal soap under a FUNGAL disease
fung = prob(id="downy-mildew", name="Downy mildew", type="fungal",
            control_ladder=[{"method": "rotate_crops"}, {"method": "insecticidal_soap"}])
assert any("does not fit problem type" in v for v in ladder_violations(*D(crop([fung], key="diseases"))))
# cultural-only SHORT ladder (clubroot) -> MUST PASS
club = prob(id="clubroot", name="Clubroot", type="fungal", control_ladder=[{"method": "rotate_crops"}])
assert ladder_violations(*D(crop([club], key="diseases"))) == []
# bad-tier catalog method in a ladder must NOT crash (catalog_violations reports the bad tier separately)
_badcat = {"broken": {"name": "Broken", "applies_to": ["any"]}}  # no tier key
assert ladder_violations({"control_methods": _badcat}, crop([prob(control_ladder=[{"method": "broken"}])])) == []
# unrecognized problem type -> flagged (applies_to coherence cannot be checked)
_unk = prob(id="mystery", type="fungusy", control_ladder=[{"method": "insecticidal_soap"}])
assert any("not a recognized type" in v for v in ladder_violations(*D(crop([_unk]))))
print("ladder_violations tests: OK")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tools/test_control_ladder_gate.py`
Expected: FAIL — `ImportError: cannot import name 'ladder_violations'`.

- [ ] **Step 3: Write minimal implementation** (append to `control_ladder_gate.py`)

```python
def ladder_violations(data, crop):
    V = []
    cat = catalog(data)
    slug = crop.get("slug", "?")
    for p in _problems(crop):
        pid = p.get("id") or p.get("name") or "?"
        ladder = p.get("control_ladder")
        if ladder is None:
            continue
        ptype = p.get("type")
        if ptype not in TYPE_TARGETS:
            # fail-closed: an unrecognized/missing type means applies_to coherence cannot be
            # verified, so we flag it rather than silently passing (also enforces the type enum).
            V.append(f"{slug}/{pid}: problem type {ptype!r} is not a recognized type "
                     f"(applies_to coherence cannot be checked)")
        ranks = []
        for rung in ladder:
            mid = rung.get("method")
            m = cat.get(mid)
            if m is None:
                V.append(f"{slug}/{pid}: control_ladder references unknown method '{mid}'")
                continue
            rank = TIER_RANK.get(m.get("tier"))  # defensive: a bad tier is catalog_violations' job to report
            if rank is not None:
                ranks.append(rank)
            targets = set(m.get("applies_to") or [])
            if UNIVERSAL_TARGET not in targets and ptype in TYPE_TARGETS:
                if not (targets & TYPE_TARGETS[ptype]):
                    V.append(f"{slug}/{pid}: method '{mid}' (applies_to {sorted(targets)}) "
                             f"does not fit problem type '{ptype}'")
        if any(ranks[i] > ranks[i + 1] for i in range(len(ranks) - 1)):
            V.append(f"{slug}/{pid}: control_ladder is not softest-first (tier ranks {ranks})")
    return V
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 tools/test_control_ladder_gate.py`
Expected: PASS — both `catalog_violations tests: OK` and `ladder_violations tests: OK`.

- [ ] **Step 5: Commit** (Trevor-gated checkpoint)

```bash
git add tools/control_ladder_gate.py tools/test_control_ladder_gate.py
git status -sb && git commit -m "feat(pest-ipm): control_ladder referential + monotonic-tier + applies_to checks (TDD)"
git show --stat HEAD
```

---

### Task 3: Identity, coverage, and CLI

**Files:**
- Modify: `tools/control_ladder_gate.py`
- Modify: `tools/test_control_ladder_gate.py`

**Interfaces:**
- Consumes: `_problems(crop)`, `ID_RE`, `catalog(data)`, `catalog_violations`, `ladder_violations`.
- Produces: `identity_violations(crop) -> list[str]`, `all_violations(data) -> list[str]`, `coverage_report(data) -> dict`, `main()`.

- [ ] **Step 1: Write the failing test** (append, above the final `print`)

```python
from control_ladder_gate import identity_violations, all_violations, coverage_report

_L = [{"method": "m"}]  # a ladder just needs to be present (non-None) to bring a problem in-scope
# missing id (in-scope: has a ladder)
assert any("missing 'id'" in v for v in identity_violations({"slug": "x", "pests": [{"name": "Aphids", "control_ladder": _L}]}))
# duplicate id within crop
dup = {"slug": "x", "pests": [{"id": "aphids", "control_ladder": _L}], "diseases": [{"id": "aphids", "control_ladder": _L}]}
assert any("duplicate id" in v for v in identity_violations(dup))
# non-kebab id
assert any("kebab" in v for v in identity_violations({"slug": "x", "pests": [{"id": "Cabbage_Worm", "control_ladder": _L}]}))
# a problem WITHOUT a ladder is out of scope -> not flagged for a missing id (soft-pilot staging)
assert identity_violations({"slug": "x", "pests": [{"name": "Not yet migrated"}]}) == []
# clean -> none
assert identity_violations({"slug": "x", "pests": [{"id": "aphids", "control_ladder": _L}], "diseases": [{"id": "clubroot", "control_ladder": _L}]}) == []

# coverage_report counts certified problems + ladders
cov = coverage_report({
    "control_methods": {"a": {}, "b": {}},
    "crops": [
        {"verification_status": {"status": "verified_gs_arc"}, "pests": [{"id": "p", "control_ladder": [{"method": "a"}]}], "diseases": []},
        {"verification_status": {"status": "shell"}, "pests": [{"id": "q"}]},
    ],
})
assert cov == {"catalog_methods": 2, "certified_crops": 1, "problems_on_certified": 1, "problems_with_ladder": 1}, cov
print("identity + coverage tests: OK")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tools/test_control_ladder_gate.py`
Expected: FAIL — `ImportError: cannot import name 'identity_violations'`.

- [ ] **Step 3: Write minimal implementation** (append to `control_ladder_gate.py`)

```python
def identity_violations(crop):
    V = []
    slug = crop.get("slug", "?")
    seen = {}
    for p in _problems(crop):
        if p.get("control_ladder") is None:
            continue  # in-scope only once a ladder is authored (soft-pilot staging; rollout adds a coverage floor)
        pid = p.get("id")
        if not pid:
            V.append(f"{slug}/{p.get('name') or p.get('name_beginner') or '?'}: pest/disease missing 'id'")
            continue
        if not ID_RE.match(pid):
            V.append(f"{slug}/{pid}: id is not kebab-case")
        seen[pid] = seen.get(pid, 0) + 1
    for pid, n in seen.items():
        if n > 1:
            V.append(f"{slug}/{pid}: duplicate id ({n}x) within crop")
    return V


def all_violations(data):
    V = list(catalog_violations(data))
    for crop in data.get("crops", []):
        V += ladder_violations(data, crop)
        V += identity_violations(crop)
    return V


def coverage_report(data):
    crops = data.get("crops", [])
    certified = [c for c in crops if (c.get("verification_status") or {}).get("status") == "verified_gs_arc"]
    problems = sum(len(_problems(c)) for c in certified)
    with_ladder = sum(1 for c in certified for p in _problems(c) if p.get("control_ladder") is not None)
    return {"catalog_methods": len(catalog(data)), "certified_crops": len(certified),
            "problems_on_certified": problems, "problems_with_ladder": with_ladder}


def main():
    argv = sys.argv[1:]
    pos = [a for a in argv if not a.startswith("--")]
    path = pos[0] if pos else "crops_data_final.json"
    data = load(path)
    if "--coverage" in argv:
        import pprint; pprint.pprint(coverage_report(data))
    V = all_violations(data)
    for v in V:
        print("VIOLATION:", v)
    print(f"control_ladder_gate: {len(V)} violation(s)")
    sys.exit(1 if V else 0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test + smoke-run the CLI on the real canonical**

Run: `python3 tools/test_control_ladder_gate.py`
Expected: PASS — all three test lines print `OK`.

Run: `python3 tools/control_ladder_gate.py crops_data_final.json --coverage`
Expected: the coverage dict prints (`catalog_methods: 0`, `problems_with_ladder: 0` — no content authored yet); then `control_ladder_gate: 0 violation(s)`, exit 0. Shape checks scope to ladder-bearing problems, so with no ladders authored the gate is cleanly silent — this confirms it reads the real file and the soft-pilot baseline is clean.

- [ ] **Step 5: Commit** (Trevor-gated checkpoint)

```bash
git add tools/control_ladder_gate.py tools/test_control_ladder_gate.py
git status -sb && git commit -m "feat(pest-ipm): identity + coverage + CLI for control_ladder_gate (TDD)"
git show --stat HEAD
```

---

### Task 4: Rule the new keys into `register_completeness`

**Files:**
- Modify: `tools/register_completeness_gate.py` (EXCLUDED_KEYS / EXCLUDED_PATH_SUBSTR)
- Modify: `tools/test_register_completeness_gate.py` (add a ruling test)

**Interfaces:**
- Consumes: existing `EXCLUDED_KEYS`, `EXCLUDED_PATH_SUBSTR`, `excluded_by_path`.

- [ ] **Step 1: Write the failing test** — add a case asserting the new keys are ruled

```python
# in tools/test_register_completeness_gate.py, add:
from register_completeness_gate import EXCLUDED_KEYS, EXCLUDED_PATH_SUBSTR, excluded_by_path
# per-problem categorical/slug keys are ruled
for k in ("id", "method", "tier", "applies_to", "best_use", "pros", "cons", "cautions"):
    assert k in EXCLUDED_KEYS, f"{k} must be ruled into EXCLUDED_KEYS"
# the two new top-level objects are ruled wholesale by path
assert excluded_by_path("control_methods.insecticidal_soap.best_use")
assert excluded_by_path("pesticide_safety_education.label_note_seasoned")
print("pest-ipm register rulings: OK")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tools/test_register_completeness_gate.py`
Expected: FAIL — `AssertionError: id must be ruled into EXCLUDED_KEYS`.

- [ ] **Step 3: Add the rulings**

In `tools/register_completeness_gate.py`, extend `EXCLUDED_KEYS` (add a commented block):

```python
    # --- pest/IPM control-ladder arc (spec 2026-07-22). Categorical/slug/list keys, NOT dual-register
    #     prose. The dual-register prose in this block is how_it_works_* + note_* (already suffixed). ---
    "id", "method", "tier", "applies_to", "best_use", "pros", "cons", "cautions",
```

And extend `EXCLUDED_PATH_SUBSTR` to cover the two new top-level objects wholesale:

```python
EXCLUDED_PATH_SUBSTR = ("plantings_provenance", "verification_status", "anchoring_urls",
                        "control_methods", "pesticide_safety_education",  # pest/IPM arc 2026-07-22
                        ...)  # keep the existing remaining members
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 tools/test_register_completeness_gate.py`
Expected: PASS — including `pest-ipm register rulings: OK`.

Also run the standalone gate on the current canonical to confirm no regression:
Run: `python3 tools/register_completeness_gate.py crops_data_final.json`
Expected: same PASS status as before this task (the rulings only exclude keys that do not yet exist in the data).

- [ ] **Step 5: Commit** (Trevor-gated checkpoint)

```bash
git add tools/register_completeness_gate.py tools/test_register_completeness_gate.py
git status -sb && git commit -m "chore(pest-ipm): rule control-ladder keys into register_completeness"
git show --stat HEAD
```

---

### Task 5: Author + splice the seed `control_methods` catalog

**Files:**
- Create: `tools/staging/pest_pilot_catalog.json` (apply_patch patch)
- Modify: `crops_data_final.json` (via apply_patch — new top-level `control_methods`)
- Possibly modify: `crops_data_final.json` `source_catalog` (add `ucanr_ipm` if not present)

**Content process (this is a content task, authored from T1 sources — not a placeholder):** author each method the pilot needs, one catalog entry per method, from a T1 extension IPM source. The pilot surfaces roughly these ~18-22 methods across the five tiers:
- `cultural`: `crop_rotation`, `garden_sanitation`, `resistant_varieties`, `balance_nitrogen`, `raise_soil_ph`, `airflow_spacing`, `bottom_watering`, `sensible_seeding_rate`, `right_transplant_size`
- `physical`: `floating_row_cover`, `handpick`, `stem_collars`, `water_spray`, `yellow_sticky_traps`
- `biological`: `beneficial_predators`, `bt`, `beneficial_nematodes`
- `soft_chemical`: `insecticidal_soap`, `neem_oil`, `copper_fungicide`, `spinosad`
- `conventional`: `pyrethroid`, `carbaryl`

Each entry MUST match this exact shape (worked exemplar, ready to author against):

```json
"insecticidal_soap": {
  "name": "Insecticidal soap",
  "tier": "soft_chemical",
  "applies_to": ["insect_soft_bodied"],
  "how_it_works_beginner": "A special soap spray that breaks down the soft bodies of small insects like aphids when it touches them directly. It has to hit the bug to work, so you coat the leaf undersides where they hide.",
  "how_it_works_seasoned": "A potassium-salt soap that disrupts the cuticle and cell membranes of soft-bodied insects on contact. No residual activity, so thorough coverage of colonies (especially leaf undersides) and repeat applications are what make it work.",
  "best_use": "Early, light infestations of aphids, mites, whiteflies, and other soft-bodied insects you can spray directly.",
  "pros": ["Low toxicity to people and pets", "OMRI-listed for organic growing", "Gentle on most hard-bodied beneficials once dry"],
  "cons": ["Contact-only, no lasting protection, so pests can return", "Must coat the insect directly, including leaf undersides", "Can burn tender foliage in heat or full sun"],
  "cautions": ["Harms soft-bodied beneficials (lady beetle larvae, lacewing larvae) on direct contact"],
  "sources": ["ucanr_ipm"],
  "anchoring_urls": {"ucanr_ipm": {"url": "https://ipm.ucanr.edu/...", "verified": "2026-07-22"}}
}
```

Honesty requirements (from the spec): the `conventional` entries name a representative active-ingredient class (Option 2 — e.g. "a pyrethroid such as permethrin"; "carbaryl") ALWAYS paired with the caution set (kills beneficials + bees, resistance, pre-harvest interval). The `soft_chemical` entries state their real cons candidly (copper accumulates in soil and harms aquatic life; sulfur burns; neem/spinosad harm bees while wet; `bt` kills all caterpillars including butterfly larvae).

- [ ] **Step 1: Add `ucanr_ipm` to `source_catalog` if absent**

Run: `python3 -c "import json; print('ucanr_ipm' in json.load(open('crops_data_final.json'))['source_catalog'])"`
If `False`, include an `add` op for `source_catalog.ucanr_ipm` in the patch below (a T1 `university_extension` entry for UC IPM, `tier: "T1"`).

- [ ] **Step 2: Author the catalog + write the patch**

Create `tools/staging/pest_pilot_catalog.json`:

```json
{
  "base_sha": "<shasum -a 256 crops_data_final.json>",
  "patches": [
    {"op": "add", "json_path": "control_methods", "value": { "insecticidal_soap": { }, "...": "all ~20 methods, each in the exemplar shape above" }}
  ]
}
```

- [ ] **Step 3: Apply the patch**

Run: `python3 tools/apply_patch.py tools/staging/pest_pilot_catalog.json`
Expected: footprint report shows top-level key `control_methods` (and `source_catalog` if added) moved; canonical stays compact.

- [ ] **Step 4: Verify catalog integrity**

Run: `python3 tools/control_ladder_gate.py crops_data_final.json`
Expected: ZERO `control_methods/...` VIOLATIONS (the per-crop `missing 'id'` violations remain — those clear in Tasks 7-9). Confirm no catalog line appears.

Run the dash/temp check on the new object (author-side):
Run: `python3 -c "import json,re; c=json.load(open('crops_data_final.json'))['control_methods']; s=json.dumps(c,ensure_ascii=False); print('EM-DASH' if '—' in s else 'clean')"`
Expected: `clean`.

- [ ] **Step 5: Commit** (Trevor-gated checkpoint — includes canonical content)

```bash
shasum -a 256 crops_data_final.json
git add crops_data_final.json tools/staging/pest_pilot_catalog.json
git status -sb && git commit -m "feat(pest-ipm): seed control_methods catalog (T1-sourced)"
git show --stat HEAD
```

---

### Task 6: Author + splice `pesticide_safety_education`

**Files:**
- Create: `tools/staging/pest_pilot_safety.json`
- Modify: `crops_data_final.json` (new top-level `pesticide_safety_education`)

**Content:** a top-level object mirroring `soil_education` / `ph_education`, dual-register, carrying the universal safety spine: read-and-follow-the-label ("the label is the law"), pre-harvest interval, pollinator protection (never spray open blooms; spray at dusk), PPE + keep kids/pets off until dry, resistance management (rotate modes of action). Exemplar shape:

```json
"pesticide_safety_education": {
  "label_note_beginner": "Before you use any pest product, organic or not, read the label and follow it exactly. The label is the law, and it tells you how much to use, what it is safe on, and how long to wait before harvest.",
  "label_note_seasoned": "The label is a legal document: rate, registered crops, re-entry interval, and pre-harvest interval are all binding. Read it before every product, organic included.",
  "preharvest_interval_beginner": "...", "preharvest_interval_seasoned": "...",
  "pollinator_note_beginner": "...", "pollinator_note_seasoned": "...",
  "handling_note_beginner": "...", "handling_note_seasoned": "...",
  "resistance_note_beginner": "...", "resistance_note_seasoned": "...",
  "sources": ["ucanr_ipm"],
  "anchoring_urls": {"ucanr_ipm": {"url": "https://ipm.ucanr.edu/...", "verified": "2026-07-22"}}
}
```

- [ ] **Step 1: Author + write the patch** (`add` op on `pesticide_safety_education`, `base_sha` fresh).
- [ ] **Step 2: Apply** — `python3 tools/apply_patch.py tools/staging/pest_pilot_safety.json` (footprint = one top-level key).
- [ ] **Step 3: Dash/temp check** on the new object (as in Task 5 Step 4) → `clean`.
- [ ] **Step 4: Commit** (Trevor-gated):

```bash
git add crops_data_final.json tools/staging/pest_pilot_safety.json
git status -sb && git commit -m "feat(pest-ipm): pesticide_safety_education object (T1-sourced)"
git show --stat HEAD
```

---

### Task 7: Author + splice Broccoli ladders

**Files:**
- Create: `tools/staging/pest_pilot_broccoli.json`
- Modify: `crops_data_final.json` (`crops[?(@.name=='Broccoli')].pests` / `.diseases`)

**Content:** for each of broccoli's 7 problems, `replace` the record to add `id` (kebab), `type`, and `control_ladder` (ordered method references from the Task 5 catalog), and REMOVE `organic_treatment_beginner`/`organic_treatment_seasoned` (their content folds into ladder rung notes where crop-specific). Keep `symptoms_*`/`cause_*`/`prevention_*`/`sources`/`anchoring_urls`. The ladder ordering encodes the escalation. Worked exemplar (cabbageworms):

```json
{
  "id": "cabbageworms",
  "name": "Cabbageworms and cabbage loopers",
  "type": "insect",
  "symptoms_beginner": "... (unchanged) ...",
  "cause_seasoned": "... (unchanged) ...",
  "prevention_seasoned": "... (unchanged) ...",
  "control_ladder": [
    {"method": "crop_rotation"},
    {"method": "floating_row_cover", "note_seasoned": "Cover from transplanting to exclude the egg-laying moths; brassicas need no pollination, so the cover can stay on all season."},
    {"method": "handpick"},
    {"method": "bt", "note_beginner": "Bt is a natural spray that only affects caterpillars; reapply after rain."},
    {"method": "spinosad"},
    {"method": "pyrethroid", "note_seasoned": "Rescue only; broad-spectrum, so spare beneficials and observe the pre-harvest interval."}
  ],
  "sources": ["...unchanged..."],
  "anchoring_urls": {"...": {}}
}
```

Clubroot's ladder is cultural-only and MUST stop there: `[{"method":"crop_rotation"},{"method":"raise_soil_ph"},{"method":"resistant_varieties","note_seasoned":"..."},{"method":"garden_sanitation"}]` — no chemical rung (there is no chemical cure). This proves the short-ladder-is-valid contract.

- [ ] **Step 1: Author all 7 records + write the patch** (7 `replace` ops with `from` = the current record, fresh `base_sha`).
- [ ] **Step 2: Apply** — `python3 tools/apply_patch.py tools/staging/pest_pilot_broccoli.json`. Expected footprint: `Broccoli` only.
- [ ] **Step 3: Run the gate**

Run: `python3 tools/control_ladder_gate.py crops_data_final.json`
Expected: zero VIOLATIONS mentioning `broccoli/...`. (Celery/microgreens `missing 'id'` remain until Tasks 8-9.)

- [ ] **Step 4: Dash/temp check** on the Broccoli record → `clean`.
- [ ] **Step 5: Commit** (Trevor-gated):

```bash
git add crops_data_final.json tools/staging/pest_pilot_broccoli.json
git status -sb && git commit -m "feat(pest-ipm): broccoli control ladders + ids (pilot)"
git show --stat HEAD
```

---

### Task 8: Author + splice Celery ladders

**Files:**
- Create: `tools/staging/pest_pilot_celery.json`
- Modify: `crops_data_final.json` (`crops[?(@.name=='Celery')].pests` / `.diseases`)

**Content:** same transform as Task 7 for celery's 3 pests + 4 diseases. Celery ALREADY carries `type`/`severity`, so this task proves the transform on the fuller record shape (keep `severity` as legacy). Blackheart (`type: "physiological"`) gets a **cultural-only** ladder (calcium management, even watering, right varieties) with NO spray rung — the second honest no-spray case. Extend the Task 5 catalog only if celery surfaces a method not yet present (e.g. `even_watering` cultural, `slug_bait_iron_phosphate` soft_chemical); add via an `add` op on `control_methods.<id>` in the same patch, T1-sourced.

- [ ] **Step 1: Author 7 records (+ any new catalog methods) + write the patch.**
- [ ] **Step 2: Apply** — footprint `Celery` (+ `control_methods` if methods added).
- [ ] **Step 3: Run the gate** — zero `celery/...` violations; catalog still clean.
- [ ] **Step 4: Dash/temp check** → `clean`.
- [ ] **Step 5: Commit** (Trevor-gated):

```bash
git add crops_data_final.json tools/staging/pest_pilot_celery.json
git status -sb && git commit -m "feat(pest-ipm): celery control ladders + ids (pilot, cross-family)"
git show --stat HEAD
```

---

### Task 9: Author + splice Microgreens cultural-only ladders

**Files:**
- Create: `tools/staging/pest_pilot_microgreens.json`
- Modify: `crops_data_final.json` (`crops[?(@.name=='Microgreens Mix')].pests` / `.diseases`)

**Content:** microgreens records use the `name_*` / `description_*` / `management_*` shape. Add `id` + `type` and a **cultural-only `control_ladder`** whose rung notes fold in the existing `management_*` prose (airflow, bottom-watering once greened, sensible seeding rate, sanitized trays); REMOVE `management_seasoned`/`management_beginner`. Leave `name_*`/`description_*` untouched (legacy prose tolerated). Exemplar (damping-off):

```json
{
  "id": "damping-off",
  "name_seasoned": "Damping-off (and surface mold)",
  "name_beginner": "Damping-off and mold",
  "type": "fungal",
  "description_seasoned": "... (unchanged) ...",
  "control_ladder": [
    {"method": "airflow_spacing", "note_beginner": "Keep a small fan running; stuffy, still air is what lets mold take hold."},
    {"method": "bottom_watering", "note_beginner": "Water from the bottom once the leaves are up so the surface is not constantly wet."},
    {"method": "sensible_seeding_rate"},
    {"method": "garden_sanitation", "note_seasoned": "Sanitize trays between cycles; there is no rescue spray for a raw cut crop, so a badly affected tray is composted and restarted clean."}
  ],
  "sources": ["...unchanged..."],
  "anchoring_urls": {"...": {}}
}
```

Note: for the pilot, splice the single representative crop **Microgreens Mix** (the other microgreen crops inherit the identical cultural-only pattern at rollout). Do NOT add a chemical rung to any microgreen ladder.

- [ ] **Step 1: Author the 2 records + write the patch.**
- [ ] **Step 2: Apply** — footprint `Microgreens Mix`.
- [ ] **Step 3: Run the gate** — zero violations for `microgreens-mix/...`; the cultural-only ladders PASS (short ladder is valid).
- [ ] **Step 4: Dash/temp check** → `clean`.
- [ ] **Step 5: Commit** (Trevor-gated):

```bash
git add crops_data_final.json tools/staging/pest_pilot_microgreens.json
git status -sb && git commit -m "feat(pest-ipm): microgreens cultural-only ladders (pilot N/A analog)"
git show --stat HEAD
```

---

### Task 10: Adversarial RED proof on the real shapes + register row 22

**Files:**
- Modify: `docs/field_addition_register.md` (add row 22)
- Scratch only: a COPY of `crops_data_final.json` (never commit the mutated copy)

- [ ] **Step 1: Prove each defect class bounces on the REAL pilot shapes**

Write a scratch script that copies the canonical in memory, injects ONE defect at a time into the real broccoli/microgreens records, and asserts `all_violations` catches it:

```python
import copy, json
from tools.control_ladder_gate import all_violations   # adjust import path for the runner
base = json.load(open('crops_data_final.json'))
def broccoli(d): return next(c for c in d['crops'] if c['name']=='Broccoli')
# 1 dangling ref
d = copy.deepcopy(base); broccoli(d)['pests'][0]['control_ladder'][0]['method'] = 'ghost_method'
assert any('unknown method' in v for v in all_violations(d))
# 2 non-monotonic (append a conventional rung, then a cultural one)
d = copy.deepcopy(base); L = broccoli(d)['pests'][0]['control_ladder']; L.insert(0, {"method":"pyrethroid"})
assert any('softest-first' in v for v in all_violations(d))
# 3 applies_to mismatch: drop an insecticidal method under clubroot (fungal)
d = copy.deepcopy(base); club = next(x for x in broccoli(d)['diseases'] if x['id']=='clubroot')
club['control_ladder'].append({"method":"insecticidal_soap"})
assert any('does not fit problem type' in v for v in all_violations(d))
# 4 duplicate id
d = copy.deepcopy(base); broccoli(d)['pests'][1]['id'] = broccoli(d)['pests'][0]['id']
assert any('duplicate id' in v for v in all_violations(d))
# 5 cultural-only clubroot on the UNmodified canonical must NOT be flagged
assert not any('clubroot' in v and 'softest-first' in v for v in all_violations(base))
print('adversarial RED battery: all defect classes bounce; clubroot passes')
```

Run it; Expected: `adversarial RED battery: all defect classes bounce; clubroot passes`. Delete the scratch copy; do not commit it.

- [ ] **Step 2: Add register row 22** to `docs/field_addition_register.md` — status PILOT (broccoli/microgreens/celery), trigger stable roster (MET), approach column GS arc (restructure + normalization), soft gate now / A39 hard-flip after rollout, consumer = app pest guidance + variety-resistance handoff. Follow the existing row format.

- [ ] **Step 3: Commit** (Trevor-gated):

```bash
git add docs/field_addition_register.md
git status -sb && git commit -m "docs(pest-ipm): field-addition register row 22 (control-ladder pilot)"
git show --stat HEAD
```

---

### Task 11: Full release verification

**Files:** none modified — verification only.

- [ ] **Step 1: The gate suite is green**

```bash
python3 tools/control_ladder_gate.py crops_data_final.json ; echo "exit=$?"      # expect 0 violations, exit=0
python3 tools/control_ladder_gate.py crops_data_final.json --coverage            # sanity: catalog_methods ~20, problems_with_ladder = broccoli+celery+microgreens problems
python3 tools/test_control_ladder_gate.py                                         # OK
python3 tools/whole_crop_gate.py                                                  # expect 18/18
python3 tools/register_completeness_gate.py crops_data_final.json                 # PASS (no new unruled keys)
python3 tools/gate_all.py                                                         # expect 119/119
python3 tools/release_verify.py                                                   # PASS
```

- [ ] **Step 2: Footprint + compact-format check**

```bash
git diff --stat <pilot-base-sha> HEAD -- crops_data_final.json   # only Broccoli/Celery/Microgreens Mix records + 2 new top-level objects (+ source_catalog if ucanr_ipm added) moved
python3 -c "import json; d=open('crops_data_final.json').read(); json.loads(d); print('trailing-newline' if d.endswith(chr(10)) else 'no-trailing-newline (compact OK)')"
```
Expected: footprint limited to the three crops + `control_methods` + `pesticide_safety_education`; `no-trailing-newline (compact OK)`.

- [ ] **Step 3: Consumer-copy sweep** across all authored content

```bash
python3 -c "
import json; d=json.load(open('crops_data_final.json'))
blobs=[json.dumps(d['control_methods'],ensure_ascii=False), json.dumps(d['pesticide_safety_education'],ensure_ascii=False)]
for name in ('Broccoli','Celery','Microgreens Mix'):
    c=next(x for x in d['crops'] if x['name']==name); blobs.append(json.dumps({'p':c.get('pests'),'d':c.get('diseases')},ensure_ascii=False))
s='\n'.join(blobs)
print('EM-DASH PRESENT' if '—' in s else 'no em dash (clean)')
"
```
Expected: `no em dash (clean)`.

- [ ] **Step 4: Update the state trio + summarize for Trevor**

Regenerate/append per the SESSION PROTOCOL (CURRENT_STATE.md, STATE_HISTORY.md most-recent-first, LATEST.txt SHA + session), then summarize what shipped and that the roster-wide rollout is the next (separately-gated) plan. This is where Trevor confirms the pilot before any push.

---

## Self-Review

**Spec coverage:**
- §4.1 shared catalog → Task 5. §4.2 per-crop id/type/control_ladder → Tasks 7-9. §4.3 tier taxonomy → Task 1 (`TIERS`/`TIER_RANK`). §4.4 Option-2 synthetics ceiling → Task 5 content requirements. §4.5 `pesticide_safety_education` → Task 6. §5 gate (catalog/ladder/identity/short-ladder/coverage) → Tasks 1-3 + Task 10 adversarial. §5 register_completeness ruling → Task 4. §6 reconciliation (add id/type/ladder, retire blobs, leave legacy prose) → Tasks 7-9. §7 pilot crops → Tasks 7-9. §8 sourcing → Task 5 Step 1 + content requirements. §9 rollout → explicitly OUT (separate plan; noted in Task 11 Step 4). §10 register row 22 → Task 10. All covered.
- **Gap check:** the spec's `type` enum and `applies_to` vocabulary (§13 open items) are settled concretely in Task 1 (`TYPE_TARGETS` keys + the target sets). No open placeholder remains in the gate.

**Placeholder scan:** the `"..."` markers in content tasks are inside JSON exemplars that explicitly stand for "unchanged existing prose" or "the remaining entries in the same worked shape" — the shape and one full worked entry are always given, which is the content-authoring contract, not a code placeholder. All CODE steps carry complete code.

**Type consistency:** `all_violations(data)`, `ladder_violations(data, crop)`, `identity_violations(crop)`, `coverage_report(data)`, `catalog_violations(data)` signatures are consistent across Tasks 1-3 and reused unchanged in Task 10/11. `TIER_RANK`, `TYPE_TARGETS`, `UNIVERSAL_TARGET`, `ID_RE` defined once in Task 1. Catalog method required-key list `_REQ_METHOD` matches the exemplar in Task 5.
