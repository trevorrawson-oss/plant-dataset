# The vacuity sweep: what landed, and the queue it leaves (2026-09-22)

A read-only sweep of all **75 gate/scan** and **247 test** entry points in `tools/`, then four
landings. The governing rule is in CLAUDE.md and CURRENT_STATE.md, both halves:

> A check that cannot distinguish "inspected and clean" from "inspected nothing" is not a check.
> **The number that looks like coverage is the number that isn't.**
> And its second half: a check that is always red is as useless as one that is always green, and
> both are closed the same way, by waiving the exact known cases and failing on everything else.

## What landed

| commit | what |
| -- | -- |
| `e9e4ffa` | the principle + the script-style invocation rule |
| `dda4dcd` | `run_test_tree.py`; rc 5 = BROKEN; three files stop reporting failure as INTERNALERROR |
| `8133536` | four gates report their population and refuse an empty scope |
| `b8cefc1` | the local-only backup tag deleted, with the measurement that it held nothing |
| `15f9b16` | the two standing failures become a WAIVER keyed on identity AND character; a SKIP stops counting as a pass |
| `2a0544a` | `gate_all` refuses a population disagreeing with the recorded certified count |

**TREE VERIFIED GREEN on `b3a9156bf2e95fecc044d6e133ef3df9ee37c3af` (2026-09-22, 59:28), WITH THE
WAIVER ACTIVE. PLA-581 can cite this.** Runner exit code **0**, captured unpiped. `VERDICT: PASS --
176 collectable files (all yielding tests); 71 of 72 script-style files RAN, 1 SKIPPED (ran nothing);
2 waived failure(s)`. **248 entry points** (176 + 72); pytest rc=1 with **2 failed / 6,009 passed**,
converted to PASS by the waiver firing on exactly those two -- `test_bare_host_scan` [PLA-544] and
`test_cited_claim_scan` [PLA-161] -- with no third failure, no character change, and **no STALE
WAIVER line**, so neither waiver is standing permission for something already fixed. **Skip
reconciled:** pytest reports NO skip of its own; the single skip is
`tools/test_build_berry_pilot_patch.py` in stage 3, which accounts for PLA-580's "1 skipped" exactly
-- same file, different route (their `pytest tools/` imported it and caught the module-level skip;
this runner classifies it script-style, so pytest never sees it). Observed, not diagnosed: 59:28
against the previous run's 47:21, which one added file (20 tests) does not explain; most likely
machine load from a concurrent session on the same checkout.

**Previous full-tree run, 47:21 (superseded, kept for the comparison):** 175 collectable + 72 script-style = 247 entry points; all 175 yield at
least one test; 2 failed / 5,989 passed. **The tree was larger than we were counting** -- the 72
script-style files had never appeared in any landing record's pass count, because pytest reports
them as "no tests ran". One qualification found while proving the waiver: of those 72, **71 RAN and
1 SKIPPED** (below), so "72/72 exited 0" overstated it.

**The missing skip, answered.** PLA-580's record cites "2 failed / 5,989 passed / **1 skipped**";
this run's summary showed no skip. The file is `tools/test_build_berry_pilot_patch.py`. Its staged
inputs (`/private/tmp/strawberry_varieties.json`, `/private/tmp/hero_backfill.json`) were
session-scoped and are gone. Under `pytest tools/` it is imported at collection and calls
`pytest.skip(allow_module_level=True)` -> "1 skipped". Under `run_test_tree` it is classified
script-style and run as a script, where it prints its SKIP line and `sys.exit(0)` -> rc 0, which the
runner counted as a pass. Its own message says **"NOT COVERED"**. So the two runs disagreed because
one route reports the skip and the other swallowed it; the runner now reports SKIPPED as its own
state. Exactly 1 of 72, measured.

## The queue, in Trevor's order. Nothing below is started.

1. **The 96 mutation harnesses are outside the runner.** `run_test_tree` executes none of them --
   they are `mutate_*`, not `test_*` -- yet their numbers are cited as evidence in landing records
   ("54 injections across five harnesses, 54 CAUGHT"). **Measured:** all 96 define `def main()`, 94
   use `sys.exit(main())`, 91 return both 0 and non-zero, and **0 write into `tools/`** (35 mutate
   scratch copies and restore). Uniform invocation already exists, so the blocker is **cost, not
   invocation**: each mutates and re-runs its target gate, and the tree is already 47 minutes. Needs
   a decision on when they run (a `--with-harnesses` mode, a schedule, or parallelism), not a
   rewrite. Also 73 of 96 take no argument at all.
2. **Nine gates still indistinguishable** on the zero-item roster, found by the sweep and not fixed:
   `climate_threshold_gate`, `control_ladder_gate`, `logref_count_scan`, `planting_layout_gate`,
   `register_coverage_gate`, `seedling_light_gate`, `variety_ladder_delta_gate`,
   `variety_resistance_gate`, and `mutate_perennial_year_gate` (see 4).
3. **`catalog_divergence_scan`** passes rc 0 on an empty canonical, printing "none -- every
   bare-host citation belongs to an id whose catalog entry is also a root".
4. **The silent-argument discard.** `mutate_perennial_year_gate` gives byte-identical output with no
   argument, with an empty roster, and with a nonexistent path: it reads a hardcoded `CANONICAL`.
   **This is correct by design** for a mutation harness and the sweep's verdict on it was a FALSE
   POSITIVE -- it was handed a path it never accepts. The narrow real defect is that it *silently
   discards* an argument a caller believes was honored; it should refuse one. Generalizes to the 73.
5. **Five modules could not be exercised** in a zero-item state and are NOT claimed clean:
   `verbatim_scan` (executes at import; needs a crop plus a fetched source corpus),
   `bloom_datum_scan`, `doc_mentions_crop_scan`, `region_cell_audit`, `rgv_cell_audit`.
6. **Two predicate copies.** `doc_roster_claim_gate` declares its own `CERTIFIED = "verified_gs_arc"`
   rather than importing `gate_all`'s. The floor added no third copy, but the two should be unified.
7. **`release_verify` is RED ON EVERY ROSTER-WIDE RUN, so its exit code carries no information.**
   Filed 2026-09-23 from the PLA-581 gauntlet (Trevor); NOT a PLA-581 item. A presence-or-null pass
   changes every certified crop, so the byte-identity `--ref` must be an uncertified SHELL
   (`avocado`), and a shell fails `whole_crop_gate` by design -- so section B always adds `reference
   avocado not PASS`, and section E adds a `novel region keys vs avocado` concern for every filled
   region cell whose key the SHELL lacks (the reference-gap false-novel-key class). MEASURED, both
   landings, base AND post, same command shape (`--ref avocado`, the other 120 declared):
   PLA-580 (`079e3923` -> `526788f2`, with the `release_verify.py` of its own landing commit
   `2588678`): **rc 1 / 10 concerns on the post-state, rc 1 / 11 on the base**; today's code
   reproduces the 10 byte-for-byte; all 10 are shell-reference artifacts (1 x avocado not PASS,
   9 x `plantings_provenance` "novel" vs avocado). PLA-581 (`526788f2` -> preview `3be60693`,
   `--slug basil`): **rc 1 / 1 concern on the post, rc 1 / 2 on the base** (avocado not PASS; the
   base's second is section A seeing the declared crops unchanged, expected when the candidate IS
   the base). The concern COUNT moved only with `--slug`; the EXIT CODE never moved. Both landing
   records had to prove the concerns pre-existing by diffing against a base run, which is a
   convention doing a gate's job. The fix is the CLAUDE.md second half: waive the EXACT known cases
   (a shell reference's own gate verdict; a key novel only because the reference lacks it) keyed
   on identity AND character, and fail on everything else.
8. **The PLA-466 and PLA-580 landing commits went in with `--no-verify`, so NONE of the hook's checks
   ran on those committed trees.** Filed 2026-09-24 (Trevor), NOT a PLA-581 item; the blanket bypass is
   what PLA-581 replaced with `EXPORT_WAIVERS`. **MEASURED, read-only, each commit with ITS OWN
   tools** (`git archive` of `tools/` at the commit), the hook's two DATASET arms: the regression arm
   (`--base` parent landing, `--candidate` the commit's canonical) and the roster-claim arm
   (`CLAUDE.md`, `docs/crop_expansion_roadmap.md`, `LATEST.txt` at the commit). PLA-466 (`9429413`,
   `1721208e` -> `079e3923`): regression rc 0, 7 crops changed, all 7 "no new violations"; roster
   claims 0. PLA-580 (`2588678`, `079e3923` -> `526788f2`): regression rc 0, 121 crops, all 121 "no new
   violations"; roster claims 0. **Nothing besides E1 would have blocked either commit.** Not
   re-measurable: E1 itself, because it reads plant-app's LIVE on-disk export, not a commit; that half
   rests on the two landing records, which state E1 was the only block. Closed as measured; the
   remaining risk is structural (a blanket bypass silences every arm at once), and `EXPORT_WAIVERS`
   removes the reason to use one.

## Confirmed NOT vacuous, so nobody re-checks them

`whole_crop_gate` (32 violations on a stripped crop), `doc_roster_claim_gate` (5 on a zero-item
root), `compound_population_gate` (6 on `{}`), `source_catalog_title_gate` (52 on `{}`),
`export_staleness_gate` (2 on an empty roster), and the 37 gates whose output moves with the input.

## Method note, because it kept mattering

Every finding here came from **running both states and comparing**, never from reading. Three static
passes produced wrong answers that only execution corrected: a regex scored
`overwinter_hardiness_gate` and `variety_detail_gate` vacuous because it did not know the `in_scope=`
idiom they already use correctly; a survey reported "0 of 96 harnesses print a RESULT line" while
`mutate_perennial_year_gate` demonstrably prints one; and the sweep's verdict on that same harness
was a false positive. Treat any figure in this document derived statically -- notably "73 of 96 take
no argument" -- as an estimate until executed.
