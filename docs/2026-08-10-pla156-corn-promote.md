# PLA-156 corn dispositions promote: the grain corns' harvest credits, corrected per claim

2026-08-10. `72284f02` -> `db853c4b`. ONE promote, 3 crops (popcorn, field-corn, flint-corn),
citations + findings + ONE consumer string. Script `tools/promote_pla156_corn.py`, guards
`tools/test_promote_pla156_corn.py`. Dispositions ruled in the claude.ai lane on PLA-156
(2026-08-10 sourcing pass, six T1 documents read); adjudication context in
`docs/2026-08-10-pla156-b577-corn-varieties-lead.md`.

## What moved

| disposition | edit |
|---|---|
| 1. popcorn cure moisture -> repoint | Both se_gulf harvest arms now cite `umn_ext` (extension.umn.edu/vegetables/growing-popcorn) + `iastate_ext` (Y&G popcorn home-garden page). Both publish "13 to 14 percent" independently; WVU is a third. |
| 2. popcorn DTM -> widen to published | `harvest_start` prose "about 100 to 110 days" -> "about 90 to 120 days" (UMN publishes "90 to 120 days" verbatim). The ONE consumer string moved. Crop-level `days_to_maturity` [90,110] untouched: separate datum, separate provenance. |
| 3. field/flint DTM -> modeled | Both crops' harvest arms go `sources: []` / `anchoring_urls: {}` with `open_findings` entries (`pla156_field_corn_harvest_dtm_modeled`, `pla156_flint_corn_harvest_dtm_modeled`) scoping the absence to the six documents read. Harvest PROSE byte-identical: the values stand, only the credit moves. |
| 4. B577 re-scoped to sow claims | `uga_b577` REMOVED from all six grain-corn harvest arms, RETAINED on every direct_sow arm, plantings-level anchor and zone cell (5 live-layer nodes per grain corn, 11 on sweet-corn, guard-pinned counts). |
| 5. Apr 30 cutoff recorded as ours | Each crop's `plantings_provenance` gains a dated append: Mar 15 - Apr 30 is our full-season narrowing of B577's Mar 15 - Jun 1 (conservative direction). Originals preserved byte-for-byte as prefixes. |

## The do-not-do this promote pins

B577's single Corn row reads **80-100 days** (home-garden sweet corn). That is LOWER than all
three grain-corn DTMs (110-120 / 90-110 / 90-110). A future session "repairing" the uncited
field/flint harvest arms by repointing them at B577's own Corn row would write 80-100 into three
crops and call it sourced. Both modeled findings carry the warning verbatim and guard G6 refuses
any citation on those arms.

Also read and deliberately NOT cited: MU IPM's "Corn Maturity Ratings and Delayed Planting"
publishes hybrid relative maturity "typically between 98 and 120" -- an RM rating is a GDU-based
convention, not a calendar days-to-maturity, and citing it for the DTM claim would be
right-document-wrong-claim.

## What deliberately did not move

- **sweet-corn: byte-identical** (guard-pinned). B577 supports it to the day, including the
  z9/z10 `Mar 1` starts via the chart's own South-Georgia two-weeks-earlier footnote.
- Zone harvest strings on all three grain corns: month-granular touch-sets, reachable under both
  the modeled and published DTM bands.
- Crop-level `days_to_maturity` on all three.

## Source-truth sample

Both promoted URLs fetched and READ this session (not snippet-matched): UMN publishes "most
varieties require 90 to 120 days to reach full maturity" and "The ideal moisture content for
popcorn is between 13 percent and 14 percent"; Iowa State publishes "between 13 and 14%" plus a
13-variety DTM table (85-112). Both ids (`umn_ext`, `iastate_ext`) were already in the catalog
and already cited on popcorn; no id minted.

## Verification pass, same day (`db853c4b` -> `ce9eb12f`)

The claude.ai lane held dispositions 2 and 3 and asked for verification rather than acceptance.
**Both failed verification, for one root cause: neither lane had read the crops' own cert
records.** Script `tools/promote_pla156_corn_fix.py`, guards
`tools/test_promote_pla156_corn_fix.py`.

- **The widen (disposition 2), REVERTED.** The dependency check found "100 to 110" living in
  twelve harvest cells (eleven regions the widen never touched), yield_expectations saying
  90-110, and popcorn's `verification_log` recording [90,110] as a SYNTHESIS **Trevor ratified
  at certification** (ISU 85-112d + UMN 90-120, "no single T1 quotes the exact band"). The
  widen re-adjudicated a settled band and created a third value. The prose is restored
  byte-identical to the 72284f02 original (guard-asserted against the fixture). The UMN +
  Iowa State repoint stays: they publish the moisture figure and are the band's named inputs.
- **The modeled declarations (disposition 3), CORRECTED.** field-corn's cert log names
  **Clemson HGIC "from 90 to 120 days after planting for most varieties"** as the band's first
  convergent input -- a home-garden extension DTM, the exact genre the sourcing pass reported
  absent. Re-found independently and read (Homegrown Grits): it publishes the band, the husk
  cue, and the drying guidance, and now anchors both field-corn harvest arms for the claims it
  publishes. flint-corn's log ratifies [90,110] from Cornell + NCSU variety figures; ISU's
  ornamental-corn page (read: cues + drying, no DTM) anchors its arms. Both findings corrected
  in place (same ids, correction acknowledged inline); cert logs byte-untouched.
- **Unchanged by the fix:** the do-not-repoint-at-B577 pin, B577's sow-layer footprint
  (5/5/5/11), sweet-corn, all harvest prose on field/flint.

Fix guards: 10 groups, RED watched, 6 mutations all caught (widen reintroduced, forbidden B577
repoint, pin softened, cert-log touch, provenance history rewrite, citation drop). Gauntlet
re-run clean at `ce9eb12f`.

## Guards + gauntlet (morning promote)

12 guard groups, RED watched before GREEN, POST_SHA pinned after commit. 7 mutations ALL CAUGHT:
over-drop of the sow layer, the forbidden B577 repoint, a sweet-corn touch, widen revert,
provenance rewrite-not-append, finding delete, pretty-print. Gauntlet: `whole_crop_gate` PASS x3,
`gate_all` 121/121, `release_verify` crops-changed = exactly ['field-corn', 'popcorn',
'flint-corn'] with no new violations and the dash/spelled-degrees scan clean, `url_health`
offline 0 and `--online` 0 with the new coverage line, COMPACT preserved.
