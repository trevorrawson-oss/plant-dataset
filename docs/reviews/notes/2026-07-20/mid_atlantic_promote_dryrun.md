# Mid-Atlantic region -- scratch promote dry-run (Task 9)

**Batch:** `tools/batches/mid_atlantic_region_promote.json` (113 patches = 111 `regions.mid_atlantic`
cells + `region_chill_delivered.mid_atlantic` + provenance replace). Base SHA `e1e01c47`.
**Method:** applied via `tools/apply_patch.py` to a scratch canonical; ran the gate suite with scratch
tools that carry `mid_atlantic: ["7","8"]` in `EXPECTED_SPANS`. Real canonical never touched.

## Footprint (exact)
- count 128 unchanged; 111 crops gained a `mid_atlantic` cell; **0 crops had any other (non-mid_atlantic)
  region changed**; `region_chill_delivered.mid_atlantic` added; COMPACT, no escaped unicode.
- Scratch OUT_SHA `72c8b40c...` (record only; the REAL promote re-derives its own SHA at apply time).

## Gate suite (roster-wide, on the scratch canonical)
| Gate | Result |
|---|---|
| `gate_all` (whole_crop_gate on every certified crop) | **PASS -- 119/119 certified** |
| `zone_span_gate` (A45) | 0 violations across 128 |
| `chill_gate` | 0 |
| `second_planting_gate` (A43) | 0 (rules AB) |
| `calendar_coherence_gate` | 0 growing-after-harvest + 0 harvest-hole |
| `coverage_floor_gate` (A31) standalone | 89 -- **PRE-EXISTING, benign**: the BASE canonical shows the IDENTICAL 89 (mid_atlantic added zero); the standalone reads uncertified shells + zone-independent crops that `gate_all`'s certified-only view correctly excludes. `gate_all` (PASS) is authoritative. Same documented pattern as RGV/PNW. |

## Adversarial RED-checks (defect classes bounce at roster scale)
- **A45:** dropped the `"7"` key from apple's mid_atlantic cell -> `zone_span_gate` fired 1 violation. PASS.
- **A43:** pushed cherry-tomato's top-level `harvest_end` into the fall cycle (dedup envelope violation)
  -> `second_planting_gate` fired 1 violation. PASS.

## Not run in the dry-run (by design)
- `release_verify.py` section A is single-crop-pilot-shaped and false-positives on roster-wide structural
  releases (known; the pre-commit backstop `precommit_release_verify.py` is the binding multi-crop
  regression gate and runs at the real promote commit).

**Verdict: the promote batch is green on a scratch copy.** Ready for the real canonical write (Task 10),
which is Trevor-gated.
