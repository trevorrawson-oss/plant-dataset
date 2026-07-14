# PNW promote dry-run -- GO (all authoritative gates green)

**Date:** 2026-07-14
**Batch:** `tools/batches/pnw_region_promote.json` (110 patches: 108 `regions.pnw` adds + 1
`region_chill_delivered.pnw` add + 1 `region_chill_delivered_provenance` replace-append).
**Base canonical (dry-run):** `060d8711` (live at build time). **Scratch out-SHA:** `8dd4ac4c`.
Method: batch applied to a scratch copy of the canonical; full suite run with a scratch `tools/`
that has `pnw` in `zone_span_gate.EXPECTED_SPANS` (`region_harness.build_scratch_tools`).

> NOTE: the canonical is moving under this arc (a concurrent leek arc landed `77f03cc8` then
> `060d8711`). The real promote (Task 10) MUST re-stamp `base_sha` from the LIVE canonical at
> promote time (`build_region_promote.py` does this) and re-run this suite. `apply_patch` fails
> closed on a `base_sha`/`from` mismatch, so a stale batch cannot silently clobber.

## Footprint (independent byte-diff, `apply_patch --validate`)
- 108 crops changed, each `regions` cells changed = EXACTLY `['pnw']` (nothing else).
- top-level changed = EXACTLY `region_chill_delivered` (+`pnw` zone band) + `region_chill_delivered_provenance` (appended, not truncated).
- `source_catalog` +none -none (every cited id already catalogued).
- scratch count = 125 (unchanged); output COMPACT (no newline, `ensure_ascii=False`); 108 pnw cells present.

## Gates (scratch tools, scratch canonical)
| Gate | Result |
|---|---|
| `gate_all.py` (whole suite, every certified crop) | **PASS 116/116** |
| `zone_span_gate.py` (A45) | **0 violations / 125 crops** |
| `chill_gate.py` | **0 violations** |
| `coverage_floor_gate.py` (A31/A32) | 89 violations = the **9 UNCERTIFIED shells ONLY** (artichoke, asparagus, avocado, olive, 5 mushrooms) -- VERIFIED zero certified crops flagged; all 108 certified region-carrying crops carry `pnw`. Benign (matches RGV precedent; `gate_all`'s certified-only view is authoritative). |
| `whole_crop_gate.py` sample (broccoli, apple, peach, orange-navel, blueberry, lavender, watermelon, strawberry) | **8/8 PASS** |
| `release_verify.py` (scratch tools, `--slug broccoli --ref lettuce-leaf`) | **Sections B-H CLEAN** (B: "no new violations introduced", cleared the pnw missing-region violation; broccoli + reference GATE PASS; C-H ok). Section A = benign roster-wide collateral (release_verify is single-crop-pilot-shaped; the pre-commit backstop `precommit_release_verify.py` is the binding multi-crop gate). |

## RED-checks (defect classes must bounce)
- **A45** (drop the `"8"` zone key from broccoli's `pnw` cell) -> `zone_span_gate` exit 1, flags broccoli. **BOUNCED.**
- **A3** (set apple `pnw` z8 `suitability="unsuitable"` but keep its non-empty calendar) -> `whole_crop_gate` exit 1, "unsuitable cell must have an empty calendar". **BOUNCED.**

## Decision: **GO.** All authoritative gates green; footprint exact; both new-defect classes RED-proven.
Real promote (Task 10) is Trevor-gated (protocol #6 canonical write): re-stamp `base_sha` from the
live canonical, add `pnw` to the real `EXPECTED_SPANS`, apply, re-run the suite + pre-commit backstop,
state trio, roadmap item 4 SHIPPED, register row. Commit UNPUSHED; Trevor confirms the push. No
plant-astro bump from this session.
