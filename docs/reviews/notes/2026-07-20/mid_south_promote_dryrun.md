# Mid-South region -- scratch promote dry-run

**Arc:** roadmap item 9 (`mid_south`, AR/OK/TN/MO, zone_span ["7","8"], frost-anchored).
**Method:** built the atomic batch (`tools/build_region_promote.py mid_south`), applied it via
`tools/apply_patch.py` to a SCRATCH copy of the canonical, and ran the gate suite with SCRATCH tools
carrying `mid_south: ["7","8"]` in `EXPECTED_SPANS`. The REAL canonical was never touched (READ-ONLY).
**Base canonical:** `af5dcee9` (the mid_atlantic promote). Scratch OUT_SHA `7a2350b9...` (record only;
the real promote re-derives its own SHA at apply time).

NOTE: this run was on the structurally-complete cells while the per-crop PROSE review pass was in
flight. Structure/dates/calendars/sources/suitability are final; the prose merge does not change any
gated field, and `gate_all` is re-confirmed green after the merge (see the SHIPPED state-history entry).

## Batch shape
`emitted 119 patches (111 mid_south cells + 2 top-level + 6 source_catalog); base_sha af5dcee9`.
- 111 `add $.crops[?slug].regions.mid_south` (net-new everywhere).
- `add $.region_chill_delivered.mid_south` = `{"7":[1000,1300],"8":[900,1100]}`.
- `replace $.region_chill_delivered_provenance` (appends the mid_south note; from-guarded).
- 6 `add $.source_catalog.<id>`: `nws_lzk`, `uada_ext_fsa6001`, `uada_ext_spring_veg`,
  `uada_ext_fall_veg`, `uada_ext_chill`, `uada_ext_fsa6105` (all T1; the delta-1 sourcing work).

## Footprint audit (scratch vs base)
- count 128 unchanged; COMPACT (byte-identical to a compact re-dump; no trailing newline).
- 111 `regions.mid_south` cells added; **0 other region cells changed** (byte-diff).
- exactly the 6 new `source_catalog` ids added; `region_chill_delivered.mid_south` + provenance added.

## Gate suite (scratch canonical + scratch tools)
| gate | result |
|---|---|
| `gate_all` (whole_crop_gate on every certified crop) | **PASS -- 119/119 certified** |
| `zone_span_gate` (A45) | 0 across 128 |
| `chill_gate` | 0 |
| `second_planting_gate` (A43) | 0 (rules=AB) |
| `calendar_coherence_gate` | 0 growing-after-harvest + 0 harvest-hole |
| `timing_spine_gate` | 0 violations, 0 warnings |
| `region_cell_audit mid_south` (5 staging files, 111 cells) | 0 issues |
| `release_verify` | clean -- no blocking concerns |
| `coverage_floor_gate` standalone | **89 -- PRE-EXISTING, benign**: the REAL base (real tools, no mid_south) shows the IDENTICAL 89; base + scratch-tools shows 200 (89 + the 111 not-yet-added mid_south floors), and the promote resolves exactly those 111 -> 89 remain. Same documented pattern as RGV/PNW/mid_atlantic (uncertified shells + zone-independent crops the certified-only `gate_all` view correctly excludes). `gate_all` (PASS) is authoritative. |

## RED-checks (defect classes must bounce at roster scale)
- **A45 (span parity):** dropped the `"7"` key from `cherry-tomato.mid_south.resolved_by_zone` ->
  `zone_span_gate.check_crop` returns 1 violation (`resolved_by_zone keys ['8'] != span (missing ['7'])`).
  Bounced.
- **A43 (fall envelope):** left `cherry-tomato.mid_south.z8.harvest` at its spring span
  (`Jun 11 - Jun 25`) but pushed `harvest_end` out to the fall crop's end -> `second_planting_gate`
  returns 1 violation (`harvest_end outside the primary harvest window`); the uncorrupted cell returns
  0. Bounced.

**Verdict: the promote batch is green on a scratch copy, footprint is exact, and the A45/A43 defect
classes are proven to bounce. Ready for the real canonical write once the prose merge lands + Trevor
approves.**
