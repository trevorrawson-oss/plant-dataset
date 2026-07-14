# RGV promote -- scratch dry-run (2026-07-13)

Full dry-run of `tools/batches/rgv_region_promote.json` (110 patches) applied to a SCRATCH
canonical + rgv-patched SCRATCH tools. The real canonical was NOT touched. Verdict: **GO** --
every authoritative gate is green under true promote conditions (rgv in `EXPECTED_SPANS`).

## Apply + footprint
- `apply_patch` OK (SHA-gated on base `7e29f4f4`, the live canonical).
- Footprint EXACT: **108 crops gain `regions.rgv`; ZERO crops have any other change.**
- Top-level: `region_chill_delivered.rgv` added + `region_chill_delivered_provenance` replaced (the whole-string, lossless-insertion). No other top-level key changed.
- Structure: count **125** (unchanged), COMPACT (no `", "`/`": "` separators), no trailing newline, 0 escaped unicode.

## Gate suite (rgv-aware scratch tools, scratch canonical)
- `gate_all` (whole suite on every certified crop): **116/116 PASS** -- the authoritative release gate.
- `zone_span_gate` A45: **0**.
- `chill_gate`: **0**.
- `whole_crop_gate` sample (broccoli, beefsteak-tomato, grapefruit, apple, peach, blackberry, strawberry, pomegranate, lettuce-leaf): **all PASS**.
- `rgv_cell_audit` (anomaly detector) over all 108 staged cells: **0 issues**.
- **A45 RED-check**: dropping a zone key from an rgv cell -> A45 BOUNCES (the span-parity guard fires). Confirms the gate actually catches the defect class at roster scale.

## `release_verify` (rgv-aware): CLEAN
No blocking concerns (structural + consistency). 3 non-blocking Step-5.5 notes = pre-existing
`ca_north_coast.z10` / `ca_south_coast.z10` `wait`-month pause-legibility items (same ones the
2026-07-12 reconciliation saw; not introduced here). NOTE: running release_verify with the REAL
(pre-EXPECTED_SPANS) tools shows a spurious "reference lettuce-leaf not PASS" concern -- that is a
dry-run tooling artifact (real tools lack rgv in EXPECTED_SPANS, so the new rgv cell trips A45); it
disappears the moment EXPECTED_SPANS carries rgv, which is the state at the real promote.

## Pre-commit backstop (rgv-aware): NO REGRESSION
`precommit_release_verify --base <real> --candidate <scratch>`: **OK -- no regression.** Every one of
the 108 changed crops reports "no new violations (0 total, cleared 1)" -- the promote CLEARS the
missing-rgv violation per crop; it introduces none.

## The one non-green: `coverage_floor_gate` standalone = 89 (BENIGN, documented class)
- Standalone `coverage_floor_gate` over ALL 125 crops reports 89 violations. gate_all (certified-only,
  the authoritative gate) is **116/116**.
- **All 9 flagged crops are UNCERTIFIED shells**: artichoke, asparagus, avocado, olive + 5 mushrooms.
  **Zero certified crops flagged.**
- **Baseline (real canonical, no rgv) already reports 85** of these -- the shells fail coverage_floor's
  all-crops run for pre-existing reasons (mushrooms wrongly carry regions; the 4 non-mushroom shells
  already have incomplete rosters). Adding rgv takes 85 -> 89: exactly one added "missing rgv" line on
  each of the 4 non-indoor shells (artichoke/asparagus/avocado/olive), all of which were ALREADY in the
  baseline 85. No new crop is broken; the flagged SET is unchanged.
- This is the same certified-only-vs-all-crops discrepancy the 2026-07-12 reconciliation shipped with,
  Trevor-approved: uncertified shells widen/gain the region at their own authoring/certification; the
  app unions `zone_span` across the certified roster so rgv still resolves. gate_all + release_verify +
  the pre-commit backstop are certified-scoped and all green.

## Conclusion
GO. The atomic promote (apply the batch + add `rgv` to `zone_span_gate.EXPECTED_SPANS` in the same
commit) lands the RGV region across all 108 certified region-carrying crops with an exact footprint,
every authoritative gate green, and only the documented benign uncertified-shell coverage_floor class
outstanding. Awaiting Trevor's go for the canonical write (Task 10).
