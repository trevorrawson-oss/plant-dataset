# PLA-10 promote 1, session 3 hand-off (2026-10-01)

Canonical `c5fc3d13` -> `cf1d480d` (promote 1 LANDED in the data commit; push on Trevor's go). HEAD at session start
`769bac6`, pushed at the start of the session (`cd1a96b..769bac6`), so HEAD == origin/main before any session-3 work.

## What landed
- All 113 certified non-zone-independent crops carry a cited `planting_layout` (119 entries: 113 defaults, plus
  non-default hill entries on cantaloupe, honeydew, yellow-summer-squash, zucchini and non-default row entries behind the
  watermelon and pumpkin hill defaults). The 8 microgreens: `[]`, `spacing_inches` null, `row_spacing_reason:
  not_applicable`. 203 (entry, field) figures quoted from hashed bytes; R5 migration waivers EMPTY; `see_layout` 0.
- Session 3's 20 crops: decision rows in `lane_b_specs/<slug>.json`, every one ruled by Trevor 2026-10-01 (pre-commit
  review). Rulings applied after the review: artichoke on Cornell [24,36]/[30,36] (USU's 18 in is annual culture, the
  alternative); slicing-cucumber on OSU's slicing row [24,24]/[48,48]; arugula rows [18,36] on Clemson HGIC 1329 (a cited
  row RANGE exists, so W2 as refined beats VH021's minimum 10, as for celery); elderberry's uncited 4 ft hedge number
  struck; lettuce `thinning.to_spacing` follows its in-row figure; strawberry's northern_tier note re-attributed to UMN;
  pear-asian not reopened (UGA C742's 20 ft noted beside NCSU's); zinnia composite [8,12] with the page's thinning range
  recorded; the four corn decision rows record the seeds-per-hill ruling and the TAMU EHT-044 thinning disagreement.
- Independent source-truth review (4 reviewers, 42 crops + dill's 34 strings): fixed thin_to_inches on 16 crops, celery
  rows (WSU range), bell-pepper rows (VCE; WSU's 'rows 12-24' is a source typo), sweet-potato soil_prep, dry-bean quote.
- Arming: `planting_layout_gate.PRESENCE_ARMED = True`; `spacing_inches_anchoring_urls` out of A62's ANCHOR_ONLY;
  register row 33; collision-gate PINNED_SHA -> cf1d480d.

## OWED (recorded here and in the Linear close-out; none blocks promote 1)
1. **Apple rootstock overrides (R1), DEFERRED by ruling: no number lands uncited.** `rootstock_options[].spacing_inches`
   is ABSENT on apple. Owed figures, NCSU Extension Gardener Handbook ch. 15 Table 15-4 (nonspur, feet):
   M9 4-8 -> [48,96]; M26 8-12 = the crop basis (override null); MM106 12-16 -> [144,192]; MM111 14-18 -> [168,216];
   Seedling 18-25 -> [216,300]. Needs a small TOOLS CHANGE first: let the promote add a source + anchoring url to a
   rootstock row (each row cites only umd_ext, which states no spacing), TDD + mutation harness, before promote 2. The
   promote's override machinery was removed with the ruling (stage key `rootstock_spacing` withdrawn); re-add it with the
   row citation. No consumer reads the overrides yet (PLA-629 unbuilt).
2. **D1a corrections on the seven in-canonical `*_pilot_spacing_*` open findings** (acorn, spaghetti, butternut,
   watermelon, pumpkin, honeydew, cantaloupe; fava's open_findings[0] also describes [4,8]). The promote refuses any edit
   under `verification_status`; the corrections go in under the same promote-2 tools allowance. The four
   `docs/reviews/notes/2026-07-01/` notes that recorded the blend (acorn, spaghetti, honeydew, cantaloupe) carry their
   `[CORRECTION 2026-10-01]` now.
3. **PLA-7 D3 note correction** (artichoke and asparagus are `row`, not `block`): the note is in Linear PLA-7, appended at
   close-out.
4. Recorded, not fixed: corn `thinning` cites TAMU EHT-044 ('thin them to 1 foot apart') against the ISU/UMN in-row
   8-12 (two pages, two fields); field-corn's Clemson '(2 ft)' (in-row or rows unstated) is a prose candidate; fava's
   prose 'rows 18 to 30' is on no cached cited page; dry-bean's crop-specific WSU FS135E page is an alternative citation;
   watermelon's prose keeps Clemson's 24 sq ft rule beside Clemson's 5-6 ft in-row (Clemson contradicts itself).
5. Consumers: plant-app re-exported at cf1d480d (its commit is named in the close-out); plant-astro's submodule bump is
   the astro session's (E3 reports the site pin stale until then).
