# Reset-to-shell policy v1.0 (the author-fresh wipe)

**Status:** v1.0, 2026-06-08. The keep/wipe contract for resetting the 120 non-GS
crops to honest authoring-ready shells, so every crop is authored FRESH from sources
during its gold-standard arc (and, later, by the bots) rather than verify-or-replaced
against unverified bucket data.

**Why (see `docs/contamination_report_2026-06-08.md`):** early authoring validated
data point-by-point ACROSS all 123 crops at once, smearing blanket/bucket values
across families -- mean 84% contamination on the 120 non-GS crops; 111 of 120 >=60%.
That data LOOKS authored but is unverified and largely wrong. Author-fresh removes the
value entirely (nothing wrong can survive a shallow check; no anchoring bias) and makes
the dataset's true state legible. Reversible: git preserves base SHA `ab389f72`.

## Scope

- Applies to every crop whose slug is NOT in `GS_KEEP = {cherry-tomato,
  beefsteak-tomato, lettuce-leaf}` (the 3 certified `verified_gs_arc` anchors).
- Touches only entries inside `crops[]`. All sibling top-level keys (`source_catalog`,
  `soil_education`, `ph_education`, `region_source_map`, `zone_frost_data`, `version`,
  etc.) are untouched by construction.

## KEEP (the authoring-ready shell carries only what the crop IS + a source pool)

- **Identity / classification (top-level scalars, kept verbatim):**
  `slug, name, botanical_name, family, category, type, archetype, calendar_basis,
  lifecycle, perennial, difficulty`. These route + branch the renderer and are not
  source-verified biological claims. (`difficulty` kept per Trevor 2026-06-08.)
- **Candidate source pool:** `sources_summary` kept verbatim. It is a list of plausible
  T1 sources to triage at Step 1, not a wrong biological value. (`source_catalog` is a
  top-level sibling, untouched.)
- **`verification_status` -> RESET** to the honest pre-arc shell:
  `{launch_ready_core: false, launch_ready_seasoned: false, status: null,
  last_audited: null}` (drops `source_set`, `open_findings`, `phase`, `date`, etc.).

## WIPE (every source-verifiable per-crop CLAIM, structure preserved)

Everything else in the crop is blanked recursively, preserving dict KEYS (the schema
shape) but removing all content:
- **dict** -> keep keys, recurse into each value
- **list** -> `[]` (empty; list membership is itself a claim -- which pests, which
  windows, which companions, which growth stages)
- **scalar / string / number / bool** -> `null`

This wipes: all biology prose (both registers), all biology scalars
(`days_to_maturity`, `spacing_inches`, `germination_temp_f`, `ph.preferred_range`,
`sunlight_hours`, `succession_policy` values, soil texture classes, container gallons),
the legacy `zones{}` layer, all `regions{}` windows + `region_notes_*` + calendar
tokens, `companions` arrays, `start_method` values, `recipes`, audit metadata
(`last_reviewed*`). Keys/shape remain so the arc fills them.

## Sequencing note

`succession_policy` and `start_method` are re-authored at **Step 2** (structured-field
population) and **consumed** by Step 3.5 (region shell build: direct-sow vs transplant
shape; succession hoist). The arc order Step 2 -> 3 -> 3.5 means the wiped values are
rebuilt before 3.5 reads them -- succession/direct-sow are sequenced, not lost.

## Audit (a destructive op MUST prove itself; run on the scratch before promoting)

1. The 3 `GS_KEEP` crops are byte-identical pre/post.
2. All sibling top-level keys byte-identical; crop count + slug set unchanged.
3. For every wiped crop: KEEP identity keys + `sources_summary` byte-identical;
   `verification_status` == the pre-arc shell.
4. **Safety invariant:** for every wiped crop, every leaf NOT under an identity key /
   `sources_summary` / `verification_status` is `null` (no list retains elements).
   This is the "no wrong claim survives" proof.
5. Re-run `contamination_scan.py`: the 120 wiped crops drop to ~0% (nothing to share);
   the 3 GS crops unchanged.
