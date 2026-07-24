# Asparagus certification (crop #120) -- cert gauntlet + verification record (2026-07-24)

Asparagus promoted from honest shell to certified gold-standard crop #120, as a `herbaceous_perennial`
on `frost_anchored`. This note records the CLAUDE.md protocol-#6 gauntlet run on the PROMOTED canonical.

- **Base canonical:** `ccf5e890` (origin/main `44b3214`) -> **new canonical `419c9bd1`**.
- **Roster:** 119 -> **120 certified**; 128 total unchanged.
- **Promote footprint:** pure crop replacement (no `source_catalog` / `control_methods` additions);
  only the `asparagus` crop dict changed. Compact format preserved (no trailing newline, no indent).
  Commit `da25947`.

## Gauntlet results (all GREEN)

| Check | Command | Result |
|---|---|---|
| whole_crop_gate (asparagus) | `whole_crop_gate.py asparagus` | **GATE: PASS** (A39 register-floor + A45 zone_span active) |
| gate_all (whole suite, every certified crop) | `gate_all.py` | **PASS -- 120/120 certified** |
| control_ladder_gate | `control_ladder_gate.py` | **0 violations** (asparagus-beetle, cutworm, rust, purple-spot, Fusarium ladders) |
| variety_resistance_gate | `variety_resistance_gate.py` | **0 violations** |
| A34 cross_consistency (carve-out) | `cross_consistency_gate.py` | **0 across 128** |
| A37 calendar_coherence (carve-out) | `calendar_coherence_gate.py` | **0 across 128** |
| release_verify (vs base) | `release_verify.py --base <ccf5e890> --slug asparagus` | **CLEAN -- no blocking concerns** |

`release_verify` detail: A only-asparagus-changed + lettuce-leaf byte-identical; B no new violations,
**146 shell violations cleared** (register-fill/display/calendar-presence/region-roster -- the
shell->certified transition); C all filled calendars coherent; D no user-facing dashes/spelled degrees;
E no novel keys vs the exemplar (the `suitability` convention did NOT trip the exemplar key-diff);
F beginner-notes present wherever seasoned; G no calendar byte-identical to the exemplar; H chill table OK.

## Adversarial RED re-run (the archetype gate armor)

- `test_cross_consistency_gate.py` (A34) -- **all tests passed**: the archetype carve-out is proven to
  still BOUNCE a `cool_season_annual` harvest-without-plant calendar (regression) while passing
  asparagus's harvest->fern (green).
- `test_calendar_coherence_gate.py` (A37) -- **all tests passed** (same regression + green shape).
- `test_herbaceous_perennial_gate.py` (A46) -- **all tests passed**.
- `test_control_ladder_gate.py` / `test_variety_resistance_gate.py` -- **OK**.
- Scope: `gate_all` stays **120/120** with all three archetype gates active -- no certified crop is
  perturbed by the carve-out (archetype-scoped, so the 119 pre-existing certified crops are no-ops).

## T1 source-truth sample (protocol-#6, independent re-fetch from the promoted canonical)

**11/11 PASS, 0 FAIL.** Each datum re-fetched from its cited page and confirmed on-page:

1. pH 6.5-7.0 (umn_ext) -- PASS.
2. spacing 12-18 in (mu_ext G6405) -- PASS.
3. germination 60-85°F (osu_ext, RAW-HTML table read -- asparagus row aligns to the Optimum Range
   column, no WebFetch column-shift) -- PASS.
4. fertilizer 10-10-10 (umn_ext + uga) -- PASS.
5. Millennium rust=susceptible + purple-spot=susceptible (MSU, via the `msu-prod.dotcmscloud.com`
   mirror because canr.msu.edu is Incapsula-blocked to fetchers) -- PASS.
6. Jersey Knight rust/purple-spot=tolerant (MSU class-level "Jersey hybrids"/"Jersey Giant") +
   Fusarium=tolerant (uc_ipm hybrid-vigor "tolerance, not resistance") -- PASS.
7. ca_interior z9 perennializes + re-anchored Delta prose (deep peat soils, crowns ~20 years,
   early-spring), NO "largest producer" superlative in consumer copy (uc_ipm + ucanr_ext) -- PASS.
8. fl_peninsula unsuitable (uf_ifas: "Without a certain dormant period, asparagus has trouble") -- PASS.
9. rgv + low_desert_az unsuitable (tamu_agrilife EHT-066: "produces poorly in areas with mild winters
   and extremely long, hot summers") -- PASS.
10. purple-spot = Stemphylium, ~4 h leaf wetness, fern-residue overwintering (usu_ext + rutgers) -- PASS.
11. cutworm cuts spears at the base in spring (umn_ext -- correctly the UMN page) -- PASS.

Copy scan of the canonical asparagus strings: em-dash 0, en-dash 0, "lady beetle" 0, spelled degrees 0.

Two low-severity observations (NOT failures, consistent with dataset conventions): the germination
datum is a bare register field (no per-field URL block); `control_ladder` objects carry no per-rung
anchor URLs (the purple-spot USU/Rutgers pages are not captured in-crop, though the datum is T1-true).

## Honest caveats (logged as low-severity open_findings on the crop, none block launch)

9 open_findings (all `severity:"low"`, `blocks_launch:false`): the herbaceous_perennial-in-frost_anchored
lane + A34/A37 carve-out (modeling choice); regional calendar month-PLACEMENT modeled from regional
frost patterns (not lifted from asparagus-per-zone charts); the lowest-confidence cells (nevada z9/z10,
utah_dixie z8, pnw z9, ca_interior z8, mid_south z8); thin regional sourcing on low_desert_az z9/z10
(unsuitable upheld on the dormancy + long-hot-summer basis, dual-anchored uc_ipm + tamu_agrilife); and
two modeled suitability-boundary calls.

## Verdict

**Asparagus certification is CLEAN.** Machine gauntlet green (120/120), release_verify clean, archetype
gate armor RED-proven, T1 source-truth 11/11. Ready for the state trio + (Trevor-gated) push.
