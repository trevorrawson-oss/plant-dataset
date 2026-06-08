# Tooling-Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Pay down the three recurring release-friction points (drifting backend-classification, brittle apply_patch, crying-wolf roster gate) plus the heaviest ceremony (hand-rewriting CURRENT_STATE.md) by hardening `~/plant-dataset/tools/` BEFORE carrots (anchor 4), without touching `crops_data_final.json`.

**Architecture:** One new shared classification module that all three gates import (kills the root-cause drift); apply_patch gains envelope/op/path/SHA tolerance for the variants claude.ai actually emits; the roster gate already passes (source_quote was point-fixed 2026-06-08) so its work is DRY-refactor + an optional standing/new label; a new CURRENT_STATE skeleton generator derives the mechanical sections and leaves marked prose slots. Every change is behavior-preserving on the 3 certified anchors except the documented intended fixes, validated by re-running the gates and by reconstructing prior bases from git.

**Tech Stack:** Python 3 stdlib only (json, re, hashlib, subprocess, argparse). Tests are standalone scripts (`python3 tools/test_*.py`, `assert` + `print("PASS ...")`) — NO pytest. Git for history reconstruction (`git show <commit>:./crops_data_final.json` — the `./` is REQUIRED in this repo).

---

## Pre-flight invariants (hold for the WHOLE plan)

- **Canonical SHA must NOT change.** Before AND after every task:
  `shasum -a 256 ~/plant-dataset/crops_data_final.json` must equal the `SHA:` line in `~/plant-dataset/LATEST.txt`. Current value: `ab389f72136f6d8f6576da6f93b62c8eb1cf2e3cf765041276a6ac746c4f5e4b`. This is tools-only; if the dataset SHA moves, STOP — you touched data.
- **Behavior-preserving on the 3 anchors.** lettuce-leaf, cherry-tomato, beefsteak-tomato. After each change re-run the gates; all three MUST stay `GATE: PASS`, and release_verify must behave identically EXCEPT the documented intended changes below.
- **One focused commit per fix** (4 commits total). The pre-commit hook skips tool-only commits (it sees `crops_data_final.json` isn't staged). **Dataset push is AUTONOMOUS** (announce-then-push); plant-astro stays gated.
- **Work happens in `/Users/trevorrawson/plant-dataset`** (the repo, on `main`), NOT through the plant-astro submodule.

## Baselines to capture ONCE, before starting (the behavior-preservation reference)

Run from `~/plant-dataset` and save the output; you will diff against it after each fix:

```bash
for s in lettuce-leaf cherry-tomato beefsteak-tomato; do
  python3 tools/whole_crop_gate.py $s crops_data_final.json > /tmp/base_wcg_$s.txt 2>&1
  python3 tools/release_verify.py crops_data_final.json --slug $s --ref lettuce-leaf > /tmp/base_rv_$s.txt 2>&1
done
python3 tools/register_completeness_gate.py crops_data_final.json > /tmp/base_roster.txt 2>&1
```

**Known baseline (captured 2026-06-08 on `ab389f72`):**
- whole_crop_gate: all 3 anchors `GATE: PASS`.
- release_verify standalone (no `--base`): cherry `clean` (0 concerns); **lettuce 3 CONCERNs** (all `regions.*.zone_8_presence` / `zone_10_desert_fold` — `zone_\d+_*` resolution records); **beefsteak 6 CONCERNs** (all `...anchoring_urls.<id>.note` — "URL not in retro log -- needs manual lookup").
- register_completeness_gate: `PASS (0 unruled)` modulo 4 deferred §5 companions entries.

---

## ⚠️ Spec corrections discovered during on-disk recon (READ — these change what the tasks assert)

The spec said "re-derive from disk, don't trust this blind." Doing so surfaced four divergences from the spec text. Each is reflected in the tasks:

1. **`source_quote` is ALREADY reconciled** (commit `89ae5b7`, 2026-06-08, session `register_source_quote_excluded_normalization`). It is EXCLUDED in `register_completeness_gate.py` (line 41) AND in `whole_crop_gate.py` `BACKEND_KEYS` (line 76), and is in `release_verify.py` `BACKEND_SUBSTR` (line 36). The roster gate already `PASS`es. So Fix 1's source_quote ruling and **Fix 3's dataset-wide HALT are already cleared** — Fix 3 has no residual blocker to fix; it becomes optional defensive infra (Task 8).

2. **The real Fix 1 payoff is bigger than `basis_seasoned`.** release_verify's `BACKEND_SUBSTR` (a flat substring list) is genuinely WEAKER than whole_crop_gate's `is_backend` predicate. It lacks the `zone_\d+_` regex and the `anchoring_urls` path-exclusion, so release_verify §D currently **cries wolf on 9 backend fields** across the anchors (lettuce 3 `zone_*` records, beefsteak 6 `anchoring_urls.*.note`). Unifying on the shared predicate CLEARS all 9 — this is the documented intended behavior change (CURRENT_STATE.md line 36 already lists it: "release_verify §D over-flags pre-existing legacy `zones{}` dashes").

3. **Fix 2's regression-test target is `a87932cd`, NOT fc702ca's `3a482908`.** Proven by reconstruction: applying the archived Step-4 corrections patch onto its git base (`cf6da2c`, content SHA `006cd0af` = `_meta.start_sha`) with faithful semantics yields canonical SHA `a87932cd` — which **equals the patch's own `_meta.end_sha`**. The committed fc702ca (`3a482908`) differs by exactly ONE field: `warm_arid.resolved_by_zone.8.heat_pause.basis_seasoned` held "95 degrees F" in the patch but "95°F" in the commit — a release-time hand-conversion the patch never contained. The applier cannot (and should not) reproduce an edit it was not given. **Test asserts `a87932cd` (= `_meta.end_sha` = faithful pure apply).**

4. **The Step-4 patch needs bracket-slug path support (`crops[beefsteak-tomato]`), which the spec's Fix-2 #2 does not describe.** Its 9 edits use `op:set_value`, paths `crops[<slug>].regions.<R>`, and a PROSE `before` string (not a byte-exact guard). The steps678 patch separately uses crop-relative `$.pests[0]...` paths (the case the spec DOES describe). Both normalizations are implemented in Task 5.

**One decision is escalated to Trevor (see "Open decisions" at the end): whether `basis_seasoned`/`*_basis` should be classed BACKEND (per spec — stops temp/dash scanning of rendered seasoned basis prose, consistent with its already-backend siblings synthesis_note/design_note) given the warm_arid evidence that a non-canonical temp once lived there and was hand-fixed.** The tasks below implement the spec's ruling (basis → backend) but isolate it to a single set membership so it is a one-line revert if Trevor wants basis kept under the temp gate.

---

# FIX 1 — One shared backend/user-facing classification (commit 1)

## Task 1: Create the canonical classification module

**Files:**
- Create: `tools/field_classification.py`
- Test: `tools/test_field_classification.py`

- [ ] **Step 1: Write the failing test** (`tools/test_field_classification.py`)

```python
#!/usr/bin/env python3
"""Unit test for the ONE canonical backend/user-facing predicate.
Run from repo root: python3 tools/test_field_classification.py

Pins the disputed-field rulings from TOOLING_HARDENING_spec FIX 1 + the
register-bearing-field inventory, so the three gates can never drift again.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from field_classification import is_backend

# --- BACKEND (verbatim/dash/spelled-degrees tolerated; not temp/dash-scanned) ---
BACKEND_CASES = [
    # (key, path)
    ("source_quote", "regions.warm_arid.plantings[0].source_quote"),
    ("source_quote_seasoned", "x.source_quote_seasoned"),
    ("basis_seasoned", "regions.warm_arid.resolved_by_zone.8.heat_pause.basis_seasoned"),
    ("basis", "regions.warm_arid.resolved_by_zone.8.heat_pause.basis"),
    ("synthesis_note_seasoned", "zones.8.plantings[0].synthesis_note_seasoned"),
    ("design_note", "regions.x.plantings[0].design_note"),
    ("note", "verification_status.open_findings[0].note"),       # under verification_status subtree
    ("note", "zones.9.anchoring_urls.uc_mg.note"),               # anchoring_urls subtree
    ("zone_8_presence", "regions.ca_north_coast.zone_8_presence"),
    ("zone_10_desert_fold", "regions.ca_desert.zone_10_desert_fold"),
    ("calendar_basis", "regions.x.resolved_by_zone.9.calendar_basis"),
    ("sources_summary", "sources_summary"),
    ("plantings_provenance", "regions.x.plantings_provenance"),
    ("uscrn_validation", "regions.x.uscrn_validation"),
    ("description_sources", "description_sources"),
    ("notes_internal", "x.notes_internal"),
    ("note_internal", "x.note_internal"),
]
for k, p in BACKEND_CASES:
    assert is_backend(k, p), f"expected BACKEND: key={k!r} path={p!r}"

# --- USER-FACING (must be temp/dash-scanned; NOT backend) ---
USER_FACING_CASES = [
    ("region_notes_seasoned", "regions.warm_arid.region_notes_seasoned"),
    ("region_notes_beginner", "regions.warm_arid.region_notes_beginner"),
    ("region_label", "regions.warm_arid.region_label"),
    ("description_seasoned", "description_seasoned"),
    ("harvest_ready_seasoned", "harvest_ready_seasoned"),
    ("plant_out", "regions.warm_arid.resolved_by_zone.9.plant_out"),
    ("text", "tips_by_stage[0].text"),
    ("cause_seasoned", "pests[0].cause_seasoned"),
]
for k, p in USER_FACING_CASES:
    assert not is_backend(k, p), f"expected USER-FACING: key={k!r} path={p!r}"

print("PASS field_classification")
```

- [ ] **Step 2: Run it to verify it fails**

Run: `cd ~/plant-dataset && python3 tools/test_field_classification.py`
Expected: FAIL — `ModuleNotFoundError: No module named 'field_classification'`.

- [ ] **Step 3: Write the module** (`tools/field_classification.py`)

```python
#!/usr/bin/env python3
"""field_classification.py -- the ONE canonical backend/user-facing predicate.

THE single source of truth for "is this field BACKEND" (behind-the-scenes
audit / evidence / machinery / own-voice reasoning), shared by all three gates:
  - whole_crop_gate.py  §C/D dash + temperature scan (skip backend strings)
  - release_verify.py   §D  dash + spelled-degrees scan (skip backend strings)
  - register_completeness_gate.py  the backend slice of its EXCLUDED roster

BACKEND = `--`, em-dash, and spelled "degrees F" are TOLERATED (CLAUDE.md); the
field is not rendered to growers as register-bearing copy. USER-FACING = held to
the dash/temperature canon.

Provenance: promoted from whole_crop_gate's is_backend (the most complete of the
three) + release_verify's BACKEND_SUBSTR merged in + the register-bearing-field
inventory v1.0 rulings (source_quote EXCLUDED 2026-06-08; the *_basis family).
Behavior-preserving on the 3 certified anchors; the only intended deltas are
release_verify §D no longer crying wolf on zone_N records + anchoring_urls notes,
and whole_crop_gate §D no longer scanning the *_basis family. See
docs/superpowers/plans/2026-06-08-tooling-hardening.md.
"""
import re

# Exact leaf-key matches.
BACKEND_KEYS = {
    # machinery / identifier
    "id", "slug", "stage_id", "tip_id", "region_id", "evidence_tier", "added_in",
    "last_reviewed", "last_reviewed_session", "last_operation", "last_session",
    "schema_version", "last_updated", "date", "stored_date", "resolution_tier",
    "resolution_method", "anchor_threshold", "fallback_beyond_horizon",
    "calendar_state", "window_type", "timing_relative", "phase", "status", "image",
    "plantings_provenance", "provenance", "lifted_from_zone", "botanical_name",
    "family", "calendar_basis", "resolution_source", "from", "from_year_round_note",
    "url", "verified", "accessed", "publisher", "source_class", "source_note",
    "verification_log_ref", "filing_record", "disposition", "scope", "session",
    "field", "assigned_to", "deferred_to", "last_audited", "resolution_note",
    "filed_in", "filed_in_session", "resolved_in", "resolved_by",
    # own-voice reasoning + evidence prose ("show your work" layer -- backend for
    # the dash/temp gate even though SP renders; matches existing synthesis/design)
    "note_internal", "notes_internal", "synthesis_note", "synthesis_note_seasoned",
    "design_note", "design_note_seasoned", "source_quote", "source_quote_seasoned",
    "zone_coverage_note", "zone_coverage_note_seasoned", "uscrn_validation",
    "classification", "sources_summary", "description_sources", "step5_verification",
    # citation structure
    "source", "source_id", "claim", "tier", "trust_tier", "citable_for", "archetype",
    "succession_id", "track", "added_by",
}

# Subtree exclusions: a field anywhere under a path containing one of these is
# backend. Merges whole_crop_gate's BACKEND_PATH_SUBSTR + release_verify's
# BACKEND_SUBSTR. (Many overlap BACKEND_KEYS; kept here too so NESTED occurrences
# under those containers are also caught, e.g. a `note` under verification_status.)
BACKEND_PATH_SUBSTR = (
    "plantings_provenance", "verification_status", "anchoring_urls", ".provenance",
    "uscrn_validation", "_admission", "synthesis_note", "design_note",
    "source_quote", "sources_summary", "notes_internal", "calendar_basis",
    "step5_verification",
)

BACKEND_KEY_RE = re.compile(r"zone_\d+_")  # zone_8_presence, zone_10_desert_fold, ...

# `basis_seasoned` and the *_basis family (heat_pause.basis, cold_pause.basis, ...)
# are backend per TOOLING_HARDENING_spec FIX 1. Isolated here so it is a one-line
# revert if the ruling is recut (see plan "Open decisions").
_BASIS_FAMILY = lambda key: key == "basis" or key.endswith("_basis")


def is_backend(key, path):
    """True if (key, path) names a behind-the-scenes field where verbatim text,
    `--`/em-dash, and spelled 'degrees F' are tolerated and no dash/temp scan
    applies. `path` is the dotted/bracketed location string the gates already
    build during their walk."""
    return (key in BACKEND_KEYS
            or bool(BACKEND_KEY_RE.match(key))
            or key.endswith("_sources")
            or key.endswith("_anchoring_urls")
            or _BASIS_FAMILY(key)
            or any(s in path for s in BACKEND_PATH_SUBSTR))
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `cd ~/plant-dataset && python3 tools/test_field_classification.py`
Expected: `PASS field_classification`

(No commit yet — Fix 1 is one commit after Tasks 1-3.)

## Task 2: Point whole_crop_gate + release_verify at the shared predicate

**Files:**
- Modify: `tools/whole_crop_gate.py:63-89` (delete local BACKEND_* + is_backend; import shared)
- Modify: `tools/release_verify.py:35-38, 68` (delete local BACKEND_SUBSTR; use shared is_backend)

- [ ] **Step 1: whole_crop_gate.py — replace the local classification block.**

Delete lines 62-89 (the `# ---- layer classification ----` comment through the local `is_backend` def) and replace with:

```python
# ---- layer classification: the ONE shared predicate (field_classification.py) ----
import os as _os
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from field_classification import is_backend
```

The call site at line 208 (`if isinstance(v, str) and not is_backend(k, pat):`) is unchanged — same signature `is_backend(key, path)`.

- [ ] **Step 2: Run the gate on all 3 anchors; confirm still PASS + diff vs baseline.**

Run:
```bash
cd ~/plant-dataset
for s in lettuce-leaf cherry-tomato beefsteak-tomato; do
  python3 tools/whole_crop_gate.py $s crops_data_final.json > /tmp/new_wcg_$s.txt 2>&1
  diff /tmp/base_wcg_$s.txt /tmp/new_wcg_$s.txt && echo "$s: IDENTICAL"
done
```
Expected: all three `GATE: PASS` and `IDENTICAL` (the *_basis addition is latent — the anchors already carry °F, so no flag changes).

- [ ] **Step 3: release_verify.py — delete local BACKEND_SUBSTR, use shared is_backend in scan_user_facing.**

Delete lines 35-38 (the `# backend prose...` comment + `BACKEND_SUBSTR = (...)` tuple). At the top imports (line 29 area) add:
```python
import os as _os
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from field_classification import is_backend
```
Change `scan_user_facing` (lines 59-72). It currently keys on `path` only; the shared predicate needs the leaf KEY too. Rewrite to carry the key:

```python
def scan_user_facing(o, path="", key=""):
    hits = []
    if isinstance(o, dict):
        for k, v in o.items():
            hits += scan_user_facing(v, f"{path}.{k}", k)
    elif isinstance(o, list):
        for i, x in enumerate(o):
            hits += scan_user_facing(x, f"{path}[{i}]", key)
    elif isinstance(o, str):
        flag = ("--" in o or EMDASH in o or re.search(r"\bdegrees?\s*F\b", o))
        if flag and not is_backend(key, path):
            hits.append((path, o[:60]))
    return hits
```
(List elements inherit the parent key so e.g. `sources` arrays/`anchoring_urls` stay classified by their container key + path — matching the previous path-substring behavior, now strengthened by the key check.)

- [ ] **Step 4: Run release_verify on all 3 anchors; confirm the INTENDED concern clears + nothing else moves.**

Run:
```bash
cd ~/plant-dataset
for s in lettuce-leaf cherry-tomato beefsteak-tomato; do
  python3 tools/release_verify.py crops_data_final.json --slug $s --ref lettuce-leaf > /tmp/new_rv_$s.txt 2>&1
  echo "=== $s ==="; diff /tmp/base_rv_$s.txt /tmp/new_rv_$s.txt
done
```
Expected INTENDED diffs ONLY:
- **lettuce:** the 3 `zone_8_presence`/`zone_10_desert_fold` CONCERNs disappear → summary flips `3 CONCERN(S)` to `clean`.
- **beefsteak:** the 6 `anchoring_urls.<id>.note` CONCERNs disappear → `6 CONCERN(S)` to `clean`.
- **cherry:** IDENTICAL (was already clean).

If ANY other line changes (a real user-facing string newly suppressed, or a new concern), STOP — the merge over-reached; investigate before continuing.

## Task 3: Refactor the roster gate to consume the shared backend sets (DRY, byte-identical output)

**Files:**
- Modify: `tools/register_completeness_gate.py:25-66` (source the backend slice from the shared module; keep the roster-local categorical/CN/enum keys)

The roster gate asks a DIFFERENT question (does this prose need a register ruling) than the dash gate (does this tolerate dashes), so it keeps its USER-FACING-CATEGORICAL + CN-primitive exclusions LOCAL. Only the backend/audit/machinery slice — which is exactly what drifted — is sourced from the shared module. This is a pure DRY refactor: output must be byte-identical to the baseline (`PASS (0 unruled)`).

- [ ] **Step 1: Import the shared backend sets and fold them into the roster's exclusion checks.**

After the module docstring + `PATH = ...` line, add:
```python
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from field_classification import BACKEND_KEYS, BACKEND_PATH_SUBSTR, BACKEND_KEY_RE
```
(Add `import sys` to the existing `import json, sys, re, collections` line if not already present — it is: line 21 is `import json, sys, re, collections`.)

Keep `EXCLUDED_KEYS` but it now only needs the ROSTER-LOCAL categorical/CN/enum keys (the backend ones come from the shared module). To stay provably behavior-preserving, leave `EXCLUDED_KEYS` exactly as-is for this commit and instead ADD the shared backend as an OR-branch in the `ruled` predicate (line 103-107):

```python
            ruled = (k.endswith("_seasoned") or k.endswith("_beginner")
                     or k in EXCLUDED_KEYS
                     or k in BACKEND_KEYS or BACKEND_KEY_RE.match(k)
                     or any(s in pat for s in BACKEND_PATH_SUBSTR)
                     or re.match(r"zone_\d+_", k)
                     or excluded_by_path(pat)
                     or ruled_categorical(pat, k))
```
This makes the shared backend an additive exclusion. Because the roster already PASSes (0 unruled), additive exclusion cannot introduce a flag; it can only ratify the existing pass while removing the future drift risk. (A later, separate cleanup may delete the now-redundant backend names from the literal `EXCLUDED_KEYS`; do NOT do that in this commit — minimize the diff that must be proven byte-identical.)

- [ ] **Step 2: Run the roster gate; diff vs baseline — MUST be byte-identical.**

Run:
```bash
cd ~/plant-dataset
python3 tools/register_completeness_gate.py crops_data_final.json > /tmp/new_roster.txt 2>&1
diff /tmp/base_roster.txt /tmp/new_roster.txt && echo "ROSTER IDENTICAL"
```
Expected: `ROSTER IDENTICAL` and `GATE: PASS`. If the output differs, the shared backend swept in (or dropped) a field the roster classed differently — STOP and reconcile before committing.

- [ ] **Step 3: Re-run the full test suite (all gates green).**

Run:
```bash
cd ~/plant-dataset
for t in tools/test_*.py; do echo "--- $t ---"; python3 "$t" 2>&1 | tail -1; done
```
Expected: every `test_*.py` prints its `PASS ...` line (including the new `test_field_classification.py`).

- [ ] **Step 4: Confirm canonical SHA unchanged, then COMMIT (Fix 1).**

Run:
```bash
cd ~/plant-dataset
shasum -a 256 crops_data_final.json   # must still be ab389f72...
git add tools/field_classification.py tools/test_field_classification.py tools/whole_crop_gate.py tools/release_verify.py tools/register_completeness_gate.py
git status --short                      # confirm crops_data_final.json is NOT staged
git commit -m "$(cat <<'EOF'
tools: single-source the backend/user-facing classification (field_classification.py)

Root-cause fix for the recurring gate drift: whole_crop_gate, release_verify, and
register_completeness_gate each carried their own notion of "backend" and drifted.
Promote whole_crop_gate's is_backend to a shared module, merge release_verify's
substring list + the *_basis family, and have all three import it.

Intended behavior changes (documented):
- release_verify §D no longer cries wolf on zone_N resolution records (lettuce: 3
  cleared) or anchoring_urls.*.note fields (beefsteak: 6 cleared) -- its backend
  substring list was weaker than whole_crop_gate's predicate.
- whole_crop_gate §D no longer scans the *_basis family (basis_seasoned, etc.),
  matching its already-backend siblings synthesis_note/design_note. Latent on the
  certified anchors (already canonical °F); no anchor gate result changes.

Roster gate output byte-identical (still PASS 0). All 3 anchors still GATE: PASS.
Canonical crops_data_final.json SHA unchanged (tools-only).

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 5: Push (autonomous).** `cd ~/plant-dataset && git push && git status -sb` — confirm `HEAD == @{u}`.

---

# FIX 2 — apply_patch absorbs the variants claude.ai emits (commit 2)

Implement Tasks 4-6 (the code) then Task 7 (the test + doc), all in ONE commit.

## Task 4: Envelope, op, and field-alias tolerance (the `_meta`/`corrections` wrapper)

**Files:**
- Modify: `tools/apply_patch.py` (OP_ALIASES, a new `normalize_envelope`, value/from alias handling, `set_value`, advisory `before`)

- [ ] **Step 1: Add `set_value` to OP_ALIASES (line 147-151).**

```python
OP_ALIASES = {
    "replace": "replace", "replace_value": "replace", "set": "replace", "set_value": "replace",
    "add": "add", "add_key": "add",
    "delete": "delete", "delete_key": "delete", "remove": "delete",
}
```

- [ ] **Step 2: Add `normalize_envelope` (insert after `_get`, ~line 144).**

```python
def normalize_envelope(patch):
    """Return (base_sha, edits, target_slug) from EITHER the canonical format
    {base_sha, patches:[...]} OR the grouped {_meta, corrections:[{...,changes:[...]}]}
    wrapper claude.ai emitted for beefsteak Step 4. Flattens corrections[*].changes[*]."""
    meta = patch.get("_meta") or {}
    base_sha = (patch.get("base_sha") or patch.get("_base_sha")
                or meta.get("base_sha") or meta.get("start_sha"))
    slug = (meta.get("target_crop_slug") or meta.get("crop_slug")
            or meta.get("target_crop") or meta.get("crop")
            or patch.get("crop_slug") or patch.get("target_crop"))
    edits = patch.get("patches", patch.get("edits", patch.get("patch")))
    if edits is None and "corrections" in patch:
        edits = []
        for corr in patch["corrections"]:
            edits.extend(corr.get("changes") or corr.get("edits") or [])
    return base_sha, edits, slug
```

- [ ] **Step 3: Rewrite `apply_patch(data, patch)` to use the envelope + slug + advisory `before`.**

Replace the head of `apply_patch` (lines 154-162) and the value/from extraction (line 171-172) so it:
- pulls `edits`/`slug` from `normalize_envelope`,
- accepts `after` as a value alias,
- treats `before` as advisory (NOT a from-guard) when no `from` is supplied.

```python
def apply_patch(data, patch, slug=None):
    base_sha, edits, env_slug = normalize_envelope(patch)
    slug = slug or env_slug
    if edits is None:
        sys.exit("patch has no 'patches'/'edits'/'patch'/'corrections' list")
    for i, e in enumerate(edits):
        raw_op = e["op"]
        op = OP_ALIASES.get(raw_op)
        if op is None:
            sys.exit(f"edit {i}: unknown op {raw_op!r} (known: {sorted(set(OP_ALIASES))})")
        path = _get(e, "json_path", "path")
        if path is _MISSING:
            sys.exit(f"edit {i}: no json_path/path")
        path = normalize_path(path, slug)          # Task 5
        try:
            parent, leaf = resolve_parent(data, path)
        except (KeyError, IndexError, TypeError) as ex:
            sys.exit(f"edit {i}: unresolved path {path} ({ex})")
        cur = leaf_get(parent, leaf)
        frm = _get(e, "from", "old", "old_value")
        val = _get(e, "value", "new", "new_value", "after")
        before = _get(e, "before")
        if op == "replace":
            if frm is not _MISSING and cur != frm:
                sys.exit(f"edit {i} FROM-GUARD: {path}\n  have: {json.dumps(cur, ensure_ascii=False)[:160]}\n  want: {json.dumps(frm, ensure_ascii=False)[:160]}")
            if frm is _MISSING and before is not _MISSING and cur != before:
                print(f"  note: edit {i} 'before' is advisory (not byte-equal to current); relying on base_sha gate -- {path}")
            leaf_set(parent, leaf, val)
        elif op == "add":
            if cur is not _MISSING and cur is not None:
                sys.exit(f"edit {i} ADD onto present non-null value (refusing to clobber): {path}\n  have: {json.dumps(cur, ensure_ascii=False)[:160]}")
            leaf_set(parent, leaf, val)
        elif op == "delete":
            if cur is _MISSING:
                sys.exit(f"edit {i} DELETE but slot absent: {path}")
            if frm is not _MISSING and cur != frm:
                sys.exit(f"edit {i} DELETE FROM-GUARD: {path}\n  have: {json.dumps(cur, ensure_ascii=False)[:160]}\n  want: {json.dumps(frm, ensure_ascii=False)[:160]}")
            leaf_del(parent, leaf)
    return len(edits)
```

Rationale captured in the plan: the grouped `corrections` format supplies a PROSE `before` summary, not a byte-exact guard, so it cannot be `from`. The patch-level `base_sha` SHA-gate (already enforced in `main`) is the real drift protection; the advisory note gives the operator visibility. (`main` already reads `base_sha` via `normalize_envelope` in Task 6.)

- [ ] **Step 4: (test deferred to Task 7 — the cross-cutting regression test covers Tasks 4-6 together.)**

## Task 5: Path normalization (bracket-slug + crop-relative)

**Files:**
- Modify: `tools/apply_patch.py` (a `BSLUG` regex + `slugfilter` parse kind; a `normalize_path` function)

- [ ] **Step 1: Add the bracket-slug regex + parse/child/leaf handling.**

After `IDX = re.compile(...)` (line 48) add:
```python
BSLUG = re.compile(r"^([^\[]+)\[([^\]?=]+)\]$")  # name[token], token non-numeric/non-filter -> slug/id lookup
```
In `_parse` (line 70-77) add a branch AFTER the IDX branch (numeric wins) and BEFORE the bare-key fallback:
```python
    m = BSLUG.match(tok)
    if m and not m.group(2).isdigit():
        return ("slugfilter", m.group(1), m.group(2))
```
In `_child` (line 80-89) add a `slugfilter` branch alongside `filter`:
```python
    if kind == "slugfilter":
        for el in node[key]:
            if isinstance(el, dict) and any(str(el.get(idk)) == sel
                                            for idk in ("slug", "id", "region_id", "track")):
                return el
        raise KeyError(f"slug/id filter matched nothing: {tok}")
```
In `leaf_get` (line 101-116) extend the filter branch to also cover slugfilter (try `_child`, return `_MISSING` on `KeyError`):
```python
    if kind in ("filter", "slugfilter"):
        try:
            return _child(container, leaf)
        except KeyError:
            return _MISSING
```
In `leaf_set` and `leaf_del`, the `filter`-leaf guard should also reject `slugfilter` leaves (you cannot set/delete a filter as a leaf):
```python
    elif kind in ("filter", "slugfilter"):
        raise ValueError(f"cannot set/delete a filter leaf: {leaf}")
```

- [ ] **Step 2: Add `normalize_path` (insert near `tokenize`, ~line 51).**

```python
def normalize_path(path, slug):
    """Normalize the path forms claude.ai actually emits to a crop-rooted path:
      - canonical `$.crops[?(@.slug=='X')]...`           -> unchanged
      - bracket-slug `crops[X].regions...` (Step 4)       -> unchanged (BSLUG resolves it)
      - $-rooted crop-relative `$.pests[0]...` (steps678) -> prefix the crop filter
      - bare crop-relative `regions.warm_arid...`         -> prefix the crop filter
    Crop-relative prefixing requires a known target slug (from the envelope/--slug)."""
    p = path.strip()
    if p.startswith("$."):
        p = p[2:]
    elif p == "$":
        return path
    elif p.startswith("$"):
        p = p[1:]
    first = p.split(".", 1)[0].split("[", 1)[0]
    if first == "crops":
        return "$." + p
    if slug:
        return f"$.crops[?(@.slug=='{slug}')]." + p
    return "$." + p   # no slug known: leave crop-relative (will fail loudly at resolve)
```

(`normalize_path(path, slug)` is already called in Task 3's rewritten `apply_patch`.)

- [ ] **Step 3: (test deferred to Task 7.)**

## Task 6: Proposed-end-SHA dual-encoding verification + `--validate` flag

**Files:**
- Modify: `tools/apply_patch.py` (`main`: read end_sha from envelope, verify both encodings; add `--validate`)

- [ ] **Step 1: Add a SHA-encoding helper (after `footprint`, ~line 211).**

```python
def verify_proposed_sha(text, proposed):
    """claude.ai sometimes computes its proposed end-SHA with ensure_ascii=True
    (°F -> the 6-char \\u00b0F escape); canonical is ensure_ascii=False. Try BOTH
    and report which matched, so the operator isn't left guessing."""
    canon = hashlib.sha256(text.encode()).hexdigest()
    ascii_text = json.dumps(json.loads(text), separators=(",", ":"), ensure_ascii=True)
    ascii_sha = hashlib.sha256(ascii_text.encode("utf-8")).hexdigest()
    if proposed == canon:
        return f"proposed end-SHA matches CANONICAL (ensure_ascii=False) -- correct"
    if proposed == ascii_sha:
        return f"proposed end-SHA matches ASCII-ESCAPED (ensure_ascii=True) -- claude.ai used the wrong encoding; canonical is {canon}"
    return f"proposed end-SHA MATCHES NEITHER encoding; canonical={canon} ascii={ascii_sha}"
```

- [ ] **Step 2: Rewrite `main` to use the envelope, the `--slug` override, `--validate`, and the SHA check.**

Replace `main` (lines 214-245). Key changes: `--slug` and `--validate` args; read `base_sha`/`slug`/`end_sha` via `normalize_envelope`; on `--validate`, dry-run + report footprint + path resolution, write nothing; verify the proposed end-SHA when present.

```python
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("patch")
    ap.add_argument("--base", default="crops_data_final.json")
    ap.add_argument("--out", default=None)
    ap.add_argument("--slug", default=None, help="target crop slug for crop-relative paths (overrides envelope)")
    ap.add_argument("--validate", action="store_true", help="dry-run: resolve paths + report footprint, write nothing")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    out = a.out or (a.base.rsplit(".json", 1)[0] + ".scratch.json")

    raw = open(a.base, "rb").read()
    actual = hashlib.sha256(raw).hexdigest()
    patch = json.load(open(a.patch))
    base_sha, _edits, env_slug = normalize_envelope(patch)
    slug = a.slug or env_slug
    if not base_sha:
        sys.exit("patch has no base_sha / _meta.start_sha -- refusing to apply unanchored")
    if actual != base_sha:
        sys.exit(f"SHA mismatch: base file is {actual}\n              patch expects {base_sha}\n  STOP -- re-preflight.")

    import copy as _copy
    data = json.loads(raw)
    before = _copy.deepcopy(data)
    n = apply_patch(data, patch, slug=slug)
    text = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    new_sha = hashlib.sha256(text.encode()).hexdigest()

    if not a.quiet:
        print(f"{'VALIDATED' if a.validate else 'applied'} {n} edits; base {base_sha[:8]} -> out {new_sha[:8]}")
        for line in footprint(before, data):
            print("  " + line)
        print(f"  escaped-unicode in output: {text.count(chr(92) + 'u')} (want 0)")
        proposed = (patch.get('_meta') or {}).get('end_sha') or patch.get('end_sha') or patch.get('proposed_sha')
        if proposed:
            print("  " + verify_proposed_sha(text, proposed))
    if a.validate:
        print(f"OUT_SHA={new_sha}  (validate-only; nothing written)")
        return
    open(out, "w").write(text)
    if not a.quiet:
        print(f"  wrote {out}")
    print(f"OUT_SHA={new_sha}")
```

- [ ] **Step 3: (test in Task 7.)**

## Task 7: Regression + unit tests, and the format-doc update

**Files:**
- Create: `tools/test_apply_patch.py`
- Modify: `docs/handoff_patch_format_v1_0.md` (extend the "Tolerated" list)

- [ ] **Step 1: Write `tools/test_apply_patch.py`.**

The hard case (the beefsteak Step-4 `_meta`/`corrections` wrapper) is reconstructed from git and asserted against the patch's OWN declared `_meta.end_sha` (`a87932cd`) — NOT the committed fc702ca (`3a482908`), which carries a release-time hand-edit the patch never contained (see plan spec-correction #3). Unit tests cover each normalization in isolation.

```python
#!/usr/bin/env python3
"""Tests for the hardened apply_patch -- the variants claude.ai actually emitted.
Run from repo root: python3 tools/test_apply_patch.py

History-reconstruction test (the way apply_patch was originally validated):
rebuild a prior base from git and confirm the tool reproduces the patch's declared
end-SHA. The `./` in `git show <sha>:./crops_data_final.json` is REQUIRED in this repo.
"""
import json, os, sys, subprocess, hashlib, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import apply_patch as ap

BUNDLE = os.path.expanduser(
    "~/Documents/plant-project/06-sessions/handoffs-bundles/m16-beefsteak-releases")


def git_base(commit):
    out = subprocess.run(["git", "show", f"{commit}:./crops_data_final.json"],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def canon_sha(data):
    return hashlib.sha256(
        json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


# --- 1. UNIT: envelope flattens _meta/corrections + reads start_sha + crop slug ---
wrapper = {"_meta": {"start_sha": "abc", "crop": "beefsteak-tomato"},
           "corrections": [{"id": "x", "changes": [
               {"op": "set_value", "path": "crops[beefsteak-tomato].regions.se_gulf",
                "before": "prose desc", "after": {"region_id": "se_gulf"}}]}]}
base_sha, edits, slug = ap.normalize_envelope(wrapper)
assert base_sha == "abc", base_sha
assert slug == "beefsteak-tomato", slug
assert len(edits) == 1 and edits[0]["op"] == "set_value", edits

# --- 2. UNIT: set_value alias + after value + advisory before (no from-guard) ---
data = {"crops": [{"slug": "x", "regions": {"r": {"old": True}}}]}
ap.apply_patch(data, {"base_sha": "z", "patches": [
    {"op": "set_value", "json_path": "$.crops[?(@.slug=='x')].regions.r",
     "before": "a human description of the old shell", "after": {"new": 1}}]})
assert data["crops"][0]["regions"]["r"] == {"new": 1}, data

# --- 3. UNIT: bracket-slug path crops[x] resolves like a slug filter ---
data = {"crops": [{"slug": "x", "v": 1}, {"slug": "y", "v": 2}]}
ap.apply_patch(data, {"base_sha": "z", "patches": [
    {"op": "replace", "path": "crops[y].v", "value": 9}]})
assert data["crops"][1]["v"] == 9 and data["crops"][0]["v"] == 1, data

# --- 4. UNIT: crop-relative $-rooted path is prefixed with the crop filter ---
data = {"crops": [{"slug": "beefsteak-tomato", "pests": [{"cause_seasoned": "old"}]}]}
ap.apply_patch(data, {"_meta": {"crop": "beefsteak-tomato"}, "base_sha": "z", "patches": [
    {"op": "replace", "json_path": "$.pests[0].cause_seasoned", "value": "new"}]})
assert data["crops"][0]["pests"][0]["cause_seasoned"] == "new", data

# --- 5. UNIT: proposed-SHA dual-encoding verifier ---
txt = json.dumps({"t": "95°F"}, separators=(",", ":"), ensure_ascii=False)
canon = hashlib.sha256(txt.encode()).hexdigest()
asc = hashlib.sha256(json.dumps({"t": "95°F"}, separators=(",", ":"),
                                ensure_ascii=True).encode()).hexdigest()
assert "CANONICAL" in ap.verify_proposed_sha(txt, canon)
assert "ASCII-ESCAPED" in ap.verify_proposed_sha(txt, asc)
assert "NEITHER" in ap.verify_proposed_sha(txt, "0" * 64)

# --- 6. HISTORY: beefsteak Step-4 corrections wrapper reproduces its _meta.end_sha ---
patch4 = json.load(open(os.path.join(BUNDLE, "step4_warm_regions",
                                     "m16_beefsteak_step4_patch.json")))
base = git_base("cf6da2c")                          # content SHA 006cd0af == _meta.start_sha
assert canon_sha(base) == patch4["_meta"]["start_sha"], "git base != patch start_sha"
ap.apply_patch(base, patch4)
got = canon_sha(base)
assert got == patch4["_meta"]["end_sha"], f"Step-4 apply: got {got}, want {patch4['_meta']['end_sha']}"
assert got == "a87932cd063f20f06863b3fd04b919909a6cfb7be220d78299d4ebb7962b413d", got
# (Intentionally NOT fc702ca's 3a482908 -- that commit hand-converted one
#  basis_seasoned "degrees F" -> "°F", an edit absent from the patch. See plan.)

# --- 7. HISTORY: canonical-format step5 patch reproduces its declared end ---
patch5 = json.load(open(os.path.join(BUNDLE, "step5_5_nt_cold_pause",
                                     "m16_beefsteak_step5_patch.json")))
base5 = git_base("3a482908" if False else "fc702ca")  # Step-4 commit == step5's base
if canon_sha(base5) == patch5["base_sha"]:
    ap.apply_patch(base5, patch5)
    print("  step5 chain: applied", len(patch5["patches"]), "edits ->", canon_sha(base5)[:8])
else:
    print("  step5 chain: SKIPPED (base", patch5['base_sha'][:8],
          "!= fc702ca", canon_sha(base5)[:8], "-- reconcile the predecessor commit)")

print("PASS apply_patch hardening")
```

(Note for the executor: step5's `base_sha` should equal the Step-4 *committed* content SHA `3a482908` (commit `fc702ca`). If the `if`/SKIP branch fires, find the commit whose content SHA matches `patch5["base_sha"]` via `git log` + `git show <c>:./crops_data_final.json | shasum -a 256` and use it. Do the same for the steps678 patch — its paths are crop-relative `$.pests[...]`, so pass `slug="beefsteak-tomato"` via `ap.apply_patch(base, patch678, slug="beefsteak-tomato")`. Add a parallel HISTORY block for steps678 once its base commit is confirmed.)

- [ ] **Step 2: Run the test.**

Run: `cd ~/plant-dataset && python3 tools/test_apply_patch.py`
Expected: `PASS apply_patch hardening` (with the step5 chain either applied or a printed SKIP to resolve).

- [ ] **Step 3: Update `docs/handoff_patch_format_v1_0.md` "Tolerated" list (lines 59-64).**

Append these bullets under "## Tolerated":
```markdown
- The grouped `{_meta, corrections:[{id, step, finding, ruling, changes:[...]}]}` wrapper
  (beefsteak Step 4): `corrections[*].changes[*]` is flattened into the edit stream;
  `base_sha` read from `_meta.start_sha`/`_meta.base_sha`; target crop slug from
  `_meta.crop`/`target_crop_slug`/`crop_slug`/`target_crop`. Op alias `set_value`->replace;
  value alias `after`->`value`. A prose `before` is treated as ADVISORY (the patch-level
  `base_sha` gate is the real drift protection), not a byte-exact `from`-guard.
- Path forms: bracket-slug `crops[<slug>]` (resolves like the slug filter); crop-relative
  `$.pests[0]...` or bare `regions.warm_arid...` (auto-prefixed with the crop filter when a
  target slug is known -- pass `--slug` if the envelope omits it).
- Proposed end-SHA (`_meta.end_sha`): verified against BOTH `ensure_ascii=False` (canonical)
  and `ensure_ascii=True` encodings; the applier reports which matched. `--validate` does a
  dry-run (resolve paths + footprint, write nothing) claude.ai can be told to run pre-handoff.
```

- [ ] **Step 4: Full suite green + SHA unchanged, then COMMIT (Fix 2).**

```bash
cd ~/plant-dataset
for t in tools/test_*.py; do python3 "$t" >/dev/null 2>&1 && echo "PASS $t" || echo "FAIL $t"; done
shasum -a 256 crops_data_final.json   # ab389f72... unchanged
git add tools/apply_patch.py tools/test_apply_patch.py docs/handoff_patch_format_v1_0.md
git status --short
git commit -m "$(cat <<'EOF'
tools(apply_patch): absorb the _meta/corrections wrapper, slug paths, and SHA encoding

claude.ai broke the patch contract 3 ways across 3 sessions; bet on absorbing, not on
conformance. Adds: the grouped {_meta, corrections[].changes[]} envelope (flatten +
start_sha + target slug); op alias set_value, value alias after, advisory `before`;
bracket-slug crops[<slug>] + crop-relative $.pests[...] path normalization; dual-encoding
proposed-end-SHA verification; a --validate dry-run.

History test: the beefsteak Step-4 corrections patch reproduces its declared
_meta.end_sha (a87932cd) from its git base cf6da2c. (Not fc702ca/3a482908 -- that commit
hand-converted one basis_seasoned "degrees F"->"°F", absent from the patch.)

Canonical crops_data_final.json SHA unchanged (tools-only).

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
EOF
)"
git push && git status -sb
```

---

# FIX 3 — Roster gate: standing vs new (DEFERRED 2026-06-08 by Trevor)

**DECISION: DEFERRED.** The dataset-wide `source_quote` HALT the spec worried about is ALREADY cleared (commit `89ae5b7`); the roster gate `PASS`es now, and Fix 1 keeps it passing. There is **no residual standing condition to fix today.** Trevor chose to defer the standing/new label until carrots actually surfaces a standing condition. Task 8 below is kept for reference but is NOT executed this session. Fixes 1, 2, 4 ship; commit numbering becomes Fix1=commit1, Fix2=commit2, Fix4=commit3.

## Task 8: Label findings NEW-THIS-CROP vs STANDING (only if greenlit)

**Files:**
- Modify: `tools/register_completeness_gate.py` (add `--crop <slug>` + `--baseline <file>` mode)
- Test: extend `tools/test_field_classification.py` or a new `tools/test_roster_standing.py`

- [ ] **Step 1: Write a failing test** (`tools/test_roster_standing.py`) that builds a tiny two-crop fixture where crop A carries an unruled prose pattern also present in a recorded baseline (STANDING → non-blocking TODO) and crop B introduces a NEW one (blocks). Assert exit code 0 for standing-only, 1 for a new finding.

```python
#!/usr/bin/env python3
"""roster gate: STANDING (dataset-wide TODO) vs NEW-THIS-CROP (per-crop blocker).
Run from repo root: python3 tools/test_roster_standing.py"""
import json, os, sys, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))

def run(args):
    return subprocess.run([sys.executable, os.path.join(HERE, "register_completeness_gate.py"), *args],
                          capture_output=True, text=True)

UNRULED = "This is an unruled prose sentence long enough to look like prose; it has structure."
data = {"crops": [
    {"slug": "standing-crop", "made_up_prose_field": UNRULED},
    {"slug": "clean-crop"},
]}
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
    json.dump(data, f); ds = f.name
baseline = {"made_up_prose_field": ["standing-crop"]}  # recorded as known-standing
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
    json.dump(baseline, f); bl = f.name
try:
    r = run([ds, "--baseline", bl])
    assert r.returncode == 0, f"standing-only should NOT block, got {r.returncode}\n{r.stdout}"
    assert "STANDING" in r.stdout, r.stdout
    r2 = run([ds])  # no baseline: the pattern is unruled-and-unrecorded -> blocks
    assert r2.returncode == 1, "unrecorded unruled pattern must block"
finally:
    os.remove(ds); os.remove(bl)
print("PASS roster standing/new")
```

- [ ] **Step 2: Run it — expect FAIL** (`--baseline` not implemented; standing not distinguished).

- [ ] **Step 3: Implement `--baseline`/`--crop` in `register_completeness_gate.py`.** Parse argv for an optional `--baseline <json>` mapping `field_path -> [crop_slug,...]` of known-standing conditions; when a candidate finding's `(path)` is recorded as standing for all its crops, print it under a `STANDING (non-blocking dataset-wide TODO)` heading and EXCLUDE it from the blocking set; only NEW (unrecorded) findings count toward `sys.exit(1)`. Keep the default (no baseline) behavior byte-identical to today (everything blocks).

- [ ] **Step 4: Run the new test + re-run the roster gate on canonical (must stay `PASS 0`); diff vs baseline.**

- [ ] **Step 5: SHA unchanged → COMMIT (Fix 3).** `git add tools/register_completeness_gate.py tools/test_roster_standing.py` + focused message; push.

---

# FIX 4 — CURRENT_STATE skeleton generator (commit 4)

## Task 9: `gen_current_state.py` — generate the mechanical sections, mark the prose slots

**Files:**
- Create: `tools/gen_current_state.py`
- Test: `tools/test_gen_current_state.py`

The generator DERIVES (never hand-types): the canonical pointer (from `LATEST.txt`); the predecessor chain (most-recent SHAs from `STATE_HISTORY.md` headers — note the chain lives in prose today, so parse the dated `## YYYY-MM-DD -- session ...` headers + any `End-SHA`/`SHA` tokens); the region fill-state table (walk each anchor's `regions`: per-cell window present? `heat_pause`/`cold_pause`? `second_planting`? `region_notes` both present?); the gate record (run `whole_crop_gate` on the anchors); the flip-gate status (read each anchor's `verification_status.launch_ready_*`/`status`). It emits `<!-- FILL: ... -->` placeholders for the headline, "What just happened", "Active work + next step", and the locked-decisions/guardrails block.

- [ ] **Step 1: Write a failing test** (`tools/test_gen_current_state.py`) that runs the generator against the CURRENT dataset + `LATEST.txt` and asserts the GENERATED mechanical sections match the corresponding sections of the live hand-written `CURRENT_STATE.md` (proves the generator is exact before anyone relies on it). Compare section-by-section after stripping the `<!-- FILL -->` prose slots; assert the canonical SHA line, the gate-record line (all three `PASS (0)`), and the region-fill summary line are reproduced verbatim.

```python
#!/usr/bin/env python3
"""gen_current_state: the generated mechanical sections must match the live
hand-written CURRENT_STATE.md exactly. Run from repo root.
python3 tools/test_gen_current_state.py"""
import os, sys, subprocess, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
out = subprocess.run([sys.executable, os.path.join(HERE, "gen_current_state.py")],
                     cwd=ROOT, capture_output=True, text=True).stdout
live = open(os.path.join(ROOT, "CURRENT_STATE.md")).read()

# canonical SHA from LATEST.txt must appear in the generated pointer
sha = next(l.split("SHA:")[1].strip() for l in open(os.path.join(ROOT, "LATEST.txt")) if l.startswith("SHA:"))
assert sha in out, "generated pointer missing canonical SHA"
assert sha in live, "live file missing canonical SHA (regenerate it?)"

# gate record: all three anchors PASS (0) in BOTH
for anchor in ("lettuce", "cherry", "beefsteak"):
    assert re.search(anchor + r".{0,20}PASS", out), f"generated gate-record missing {anchor} PASS"

# the prose slots are clearly marked for the operator
for slot in ("What just happened", "Active work", "locked decisions"):
    assert "FILL" in out, "generated file must emit <!-- FILL --> prose slots"
print("PASS gen_current_state mechanical-section match")
```

- [ ] **Step 2: Run it — expect FAIL** (generator absent).

- [ ] **Step 3: Implement `tools/gen_current_state.py`.** Read `crops_data_final.json` via the same direct-load idiom the other tools use (`json.load(open("crops_data_final.json"))`), `LATEST.txt`, and `STATE_HISTORY.md`. Emit, in order: the static SESSION-PROTOCOL block (a module constant, copied verbatim from the current header lines 1-11), a `<!-- FILL: headline -->` slot, the generated Canonical-pointer block, a `<!-- FILL: What just happened -->` slot, the generated Gate-record line (shell out to `whole_crop_gate.py` per anchor, parse the `GATE:` line), the generated Region-fill-state table, the generated Flip-gates block (read `verification_status`), and `<!-- FILL: Active work -->` + `<!-- FILL: locked decisions/guardrails -->` slots. Print to stdout (operator redirects to `CURRENT_STATE.md` after filling the slots). Keep section HEADINGS byte-identical to the current file so diffs are clean.

- [ ] **Step 4: Run the test + eyeball the generated output vs the live file.**

Run:
```bash
cd ~/plant-dataset
python3 tools/gen_current_state.py > /tmp/gen_cs.md
python3 tools/test_gen_current_state.py
diff <(grep -vE 'FILL|^>' /tmp/gen_cs.md) <(grep -vE 'FILL|^>' CURRENT_STATE.md) || true   # mechanical sections should align
```
Expected: `PASS gen_current_state ...`; the mechanical-section diff is empty or only cosmetic-whitespace (tighten the generator until the mechanical lines match).

- [ ] **Step 5: SHA unchanged → COMMIT (Fix 4 part A).** `git add tools/gen_current_state.py tools/test_gen_current_state.py` + message; push. (Bundle Task 10 into the same commit if done together.)

## Task 10: STATE_HISTORY rotation

**Files:**
- Create: `tools/rotate_state_history.py` (or a documented one-shot)
- Create (by running it): `STATE_HISTORY_ARCHIVE.md`
- Modify: `STATE_HISTORY.md` (keep header + recent ~15 SHAs + a pointer to the archive)

- [ ] **Step 1: Write `tools/rotate_state_history.py`** that splits `STATE_HISTORY.md` at the Nth `## YYYY-MM-DD -- session` header (default keep most-recent 15), moves older entries (verbatim, append-only-safe) into `STATE_HISTORY_ARCHIVE.md` below a one-line header, and leaves a `> Older entries (pre-<date>) archived in STATE_HISTORY_ARCHIVE.md` pointer in `STATE_HISTORY.md`. Idempotent: re-running with the same N is a no-op.

- [ ] **Step 2: Dry-run it** (`--dry-run` prints the split point + counts, writes nothing); confirm the cut lands on an entry boundary and the recent 15 are retained.

- [ ] **Step 3: Run it; verify line counts** (`wc -l STATE_HISTORY.md STATE_HISTORY_ARCHIVE.md`) — sum (minus the new pointer/header lines) equals the original 1732, and no entry is split mid-body.

- [ ] **Step 4: SHA unchanged → COMMIT (Fix 4 part B, or fold into Task 9's commit).** Note: `STATE_HISTORY.md`/`STATE_HISTORY_ARCHIVE.md` are state docs, not tools — this commit DOES touch them, which is allowed (the spec scopes out only `crops_data_final.json`). Sync `00-current/` per the runbook if that mirror is maintained.

---

## Final verification (before declaring done)

- [ ] `shasum -a 256 ~/plant-dataset/crops_data_final.json` == `ab389f72...` (UNCHANGED end-to-end — the whole point).
- [ ] All 3 anchors `GATE: PASS`; `register_completeness_gate` `PASS (0)`.
- [ ] release_verify standalone: lettuce + beefsteak now `clean` (the 9 false concerns cleared); cherry still `clean`.
- [ ] Every `tools/test_*.py` prints its `PASS` line.
- [ ] `git log --oneline -5` in `~/plant-dataset` shows the focused fix commits; `HEAD == @{u}`.
- [ ] Report to Trevor: what changed + every intended behavior change (the 9 cleared release_verify concerns; whole_crop_gate no longer scanning *_basis; the Fix-2 test target correction).

## Self-review (done while writing this plan)

- **Spec coverage:** Fix 1 → Tasks 1-3; Fix 2 → Tasks 4-7; Fix 3 → Task 8 (de-scoped to optional, with the reason); Fix 4 → Tasks 9-10. The spec's "test against history" discipline is the backbone of Tasks 2/4/7/9.
- **Placeholder scan:** every code step carries real code; the two genuinely open items (step5/steps678 base-commit confirmation in Task 7; the exact generator section formatting in Task 9) are flagged inline with the resolution method, not left as silent TODOs.
- **Type/name consistency:** `is_backend(key, path)`, `normalize_envelope -> (base_sha, edits, slug)`, `normalize_path(path, slug)`, `verify_proposed_sha(text, proposed)` are used consistently across tasks.

---

## Open decisions for Trevor (surface at plan review, before executing)

1. **`basis_seasoned`/`*_basis` → BACKEND?** The spec rules it backend (so the temp/dash gate skips it), consistent with its already-backend siblings `synthesis_note`/`design_note`. BUT recon found the original beefsteak Step-4 release HAND-CONVERTED a "95 degrees F" → "95°F" inside `warm_arid...heat_pause.basis_seasoned` — evidence that a non-canonical temp once lived in a rendered (SP) basis field and someone cared. Classing it backend means the gate would no longer catch that. **Recommendation: follow the spec (backend) for sibling-consistency; it's isolated to `_BASIS_FAMILY` in `field_classification.py` so it's a one-line revert if you'd rather keep basis under the °F gate.** Your call.

2. **Fix 2 test target.** Confirm you're fine with the test asserting the patch's own `_meta.end_sha` (`a87932cd`) rather than the committed fc702ca (`3a482908`) — they differ only by that release-time hand-edit. (No real choice here; just flagging the spec text was inaccurate.)

3. **Fix 3 scope.** Build the standing/new label now (Task 8) or defer? The HALT it guards against is already cleared; this is pre-emptive infra for carrots. Defer is reasonable.

4. **Promote `register_bearing_field_inventory_v1_0.md`?** Out of scope here, but CURRENT_STATE line 33 flags it: the gate enforces the inventory, yet the doc lives only in claude.ai PK + on-disk `docs/`. Not part of this plan; noted so it isn't lost.
