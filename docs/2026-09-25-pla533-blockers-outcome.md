# PLA-533 2a -- seven blocking findings landed on three citrus (2026-09-25)

**`83384c85` -> `edcd9bf9`. ONE promote, three crops.** Trevor ruling 1 (2026-09-25): land 7 of 8 drafted
blocking findings through the normal release protocol; hold the orange-navel mulch finding until
PLA-610 resolves.

## What moved

Only this, on orange-navel, grapefruit and mandarin-clementine:
- `verification_status.open_findings` gains the new findings, **appended** after the existing ones;
- `launch_ready_core` and `launch_ready_seasoned` go `True -> False`.

`verification_status.status` is **untouched** (PLA-466: a blocker drives the flags, never the status,
because status is the page gate). **No value was edited, nulled or deleted.** Every other crop and every
top-level key is byte-identical. Certified stays **121**; launch-ready goes **117 -> 114**.

| crop | finding id | contradicting T1 sentence (cached bytes) |
|---|---|---|
| orange-navel | `orange_navel_sulfur_acidification_contradicted_pla533` | UF/IFAS HS132: "If the soil is naturally basic, it will be difficult to change the reaction on any permanent basis." |
| orange-navel | `orange_navel_juice_freezing_contradicted_pla533` | U. Arizona: "...the juice should be consumed directly because most navel orange juice contains bitter compounds including limonin, which make stored juice disagreeable." |
| orange-navel | `orange_navel_best_pot_tree_contradicted_pla533` | TAMU: "The smaller citrus types (calamondin, limes, kumquats, lemons and limequats) are best suited to container culture, but all will grow for a limited time." |
| orange-navel | `orange_navel_yield_figure_contradicted_pla533` | HS132: navels "Shy Bearers"; HS141: "Inadequate fruit set and severe fruit drop are major causes of low yield of navel orange." |
| grapefruit | `grapefruit_mulched_basin_contradicted_pla533` | HS132: "Mulches are not recommended around citrus trees..."; HS141: "Trees should not be wrapped or mulched."; TAMU: "Organic mulches are not recommended for citrus trees..." (deferred_to PLA-610) |
| grapefruit | `grapefruit_sulfur_acidification_contradicted_pla533` | HS132 (same sentence) |
| mandarin-clementine | `mandarin_clementine_sulfur_acidification_contradicted_pla533` | HS132 (same sentence) |

**HELD by ruling, refused by the promote if present:** `orange_navel_mulched_basin_contradicted_pla533`
(PLA-610 is a lead; orange-navel is already blocked) and `mandarin_clementine_npk_2_1_1_cites_hs132_pla533`
(drafted only; NOT a delete candidate; a nitrogen-heavy ratio may be supported by California sources).

**The close condition, carried in every finding's summary:** the finding resolves ONLY when the named
fields are re-authored and every clause of both registers is graded supported by an independent clause
check against cached T1 bytes. Removing, emptying or repointing a citation never resolves it, and deleting
the contradicted text alone does not either.

**The sulfur advice is cited to the page that contradicts it.** grapefruit `ph.sources = ['uf_ifas_hs132']`
and `failure_diagnostics[5]`; orange-navel `failure_diagnostics[4]`; all five mandarin strings. HS132's only
sulfur mention is pest control. lemon and lime cite the same page and match it ("rather than trying to
acidify"). The mandarin strings were found by the rootstock-sweep session (PLA-609) and re-verified here.

## How 2a got here

2a set out to cite the 15 uncited register blocks on orange-navel (8) and grapefruit (7). Six T1 pages were
fetched as raw bytes under two user-agents and cached by digest (MANIFEST rows, `18a2257`). Four independent
reviewers graded **740 clauses** against those bytes only: 218 supported, 299 partial, 223 unsupported.
**No block was fully supported, so nothing was cited.** The 15 blocks, the reviews and mandarin's five sulfur
strings are with the claude.ai re-author lane at `_handoff/pla533_2a_held/` (gitignored). UC Davis postharvest
returned 403 (WAF) to both agents; Trevor saved both fact sheets from his browser, and they are cached as
`92a1d074...` (orange) and `9cf9f418...` (grapefruit). Each page carries "Commercial use is strictly forbidden
unless prior written approval is granted", which is Trevor's call, not this record's.

## Guards and proof

`tools/promote_pla533_blockers.py` pins the base SHA, the launch-ready pre-state, the absence of any live
blocker, every quoted dataset string (a finding cannot record a defect that is no longer there), and every
evidence quote **against the cached bytes by digest**. It refuses a HELD id, a non-blocking finding, a missing
close condition, a crop outside the three, and an id already in the dataset. Post-state: crop SET before
values (PLA-162), blast radius by byte equality, declared keys only, both flags false.

- Suite `tools/test_promote_pla533_blockers.py`: **28 passed**. RED first (module absent). Two drivers were
  corrected on evidence: the HELD driver was first graded caught by the COUNT guard (appending made 8), so it
  now substitutes; the digest driver first pointed at a missing file, so the missing-file check fired and the
  digest mutation SURVIVED, so it got its own driver with a present-but-drifted file.
- Harness `tools/mutate_pla533_blockers_suite.py`: **20 injected, 20 caught, 0 survived**; positive control
  GREEN; sentinel caught; MUTATION-APPLIED marker per mutation; rc 5 graded dead. Its first run correctly died
  (HARNESS DEAD, positive control red): a tools/ scratch copy has no .git for promote_fixture; fixed with the
  PLA-581 layout.

## Gauntlet on the post-state (`edcd9bf9`)

- `whole_crop_gate` orange-navel / grapefruit / mandarin-clementine: **PASS**; section G reports 4 / 2 / 1 live
  blockers with both flags false, "the coherent state (PLA-466)".
- `gate_all`: **PASS 121/121 certified, launch-ready 114/121**; container-citation floor 4 (unchanged).
- `release_verify` (each crop, `--ref lemon`): section A = the three declared crops; **B: no new violations**;
  C, D clean. The 16 section E concerns are the heat keys orange-navel-class citrus carry and lemon does not,
  and appear **identically on base-vs-base**, so they predate this promote.
- `doc_roster_claim_gate`: 128 / 121 / 7, 0 violations.

## Consumers

**This landing changes nothing a user sees, measured 2026-09-25.** plant-astro selects crops on
`verification_status.status == 'verified_gs_arc'` alone (`GrowingGuides.astro`, `built-crops`) and reads no
`launch_ready_*`, `open_findings` or `blocks_launch` anywhere in `src/`. plant-app `origin/main` filters on a
hard-coded `CERTIFIED` slug set in `scripts/build-guides-data.mjs` and reads neither either. So all three crops
stay published on both, the contradicted text included, until the re-author lands. That is the PLA-466 design
(status is the page gate, the flags are a record), and it means the flags are a record, not a takedown. The leaked
authoring note in orange-navel `container_notes.notes_seasoned` is **not rendered** by plant-astro or plant-app
`origin/main`, but it **ships** in plant-app's bundled `src/data/guides.json`, which exports `container_notes`
whole; any later edit to that field needs an app re-export.
