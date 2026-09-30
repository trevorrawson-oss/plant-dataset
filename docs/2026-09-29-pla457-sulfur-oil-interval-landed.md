# PLA-457 sulfur/oil interval landed (2026-09-29)

**`cd0f9f17` -> `d8906b43`. ONE promote.** Prepared and held on 2026-09-06 against `72371c02`
(`docs/2026-09-06-pla457-sulfur-oil-interval-prepared.md`, which remains the record of the T1 reads and the
design). Trevor's ruling of 2026-09-06 put promote A1 first; ten promotes then moved the base and the held promote
refused on every one of them. Re-pinned and landed by Trevor's ruling of 2026-09-29.

## What moved

- **21 rung notes on 10 crops**, exactly one sentence replaced in each, both registers where the figure appeared:
  apple 3, apricot 3, plum 4, strawberry 3, oregano 2, sage 2, cherry-sour 1, cherry-sweet 1, grape-tomato 1,
  lemongrass 1. Every new sentence carries 30 days, a growth-stage scope ("in leaf", "has leaves", "growing
  season") and a deferral to the oil label.
- **`control_methods.horticultural_oil` and `control_methods.sulfur` cautions** rewritten to "Keep sulfur at least
  30 days from any oil spray while the plant is in leaf, and check the oil product's label, since some specify
  longer" (the horticultural_oil one keeps its foliage-injury clause). `horticultural_oil` had cited UC IPM PN 7405
  for a 2-week figure PN 7405 does not contain. Purdue BP-69-W added to both; PN 7405 added to `sulfur`.
- **`source_catalog` +1:** `purdue_ext_bp69w` (T1, pathed, titled).
- **Oregano's two intervals now agree** (both 30 days), asserted by name.
- No launch flag, finding, id or region cell moves. Certified 121, launch-ready 114.

## What the re-pin found

All twenty 09-06 old sentences still matched exactly once on `cd0f9f17`. An independent scan of the re-pinned
post-state, one that did not use the promote's regexes, found a **21st** statement the promote had never seen:

> strawberry / two-spotted-spider-mite, SULFUR rung, `note_seasoned`: "...reserve it, keep a 2-week gap from any
> oil spray, and avoid above 90°F."

`DURATION` and `SUB_30` put `\s*` between the number and the unit, so the hyphen in "2-week" hid it. The post
check's "0 under 30 days" was therefore **false on 09-06 as well**: the promote as prepared would have shipped
this sentence. Both patterns are now `[\s-]*`, a 21st row rewrites the sentence to the ruled form, and the pins
move 20/22/22 -> 21/23/23 (notes / pre statements / post statements; still ten crops). The same independent
scan over every string on the post-state finds no other sulfur/oil separation under 30 days; its remaining hits
are repeat-spray schedules (every 10 to 14 days, and similar), which are a different claim.

## Proof

- **Suite `tools/test_promote_pla457_sulfur_oil_interval.py`: 70 passed.** `test_the_net_finds_the_hyphenated_statement`
  names the strawberry sentence as a literal; it was written first and seen RED (with the three output-SHA pins
  that move with the base), then GREEN. The suite is otherwise replay-pinned, so its RED phase is unavailable by
  construction; the harness is the non-vacuity evidence.
- **Harness `tools/mutate_pla457_sulfur_oil_interval_suite.py`: 55 injected, 55 caught, 0 survived, 0 broken.**
  Two new mutations remove the hyphen arm of each pattern. Anchor preflight caught an existing mutation still
  anchored on the old `SUB_30` text, which was repaired. The harness now grades pytest rc 5 (a `-k` selector that
  collects nothing) as BROKEN rather than caught, the PLA-7 A1 rule this harness had not inherited; proved on a
  deliberately bogus selector (rc 5) against a real one (rc 0).

## Gauntlet on `d8906b43` (the gauntleted scratch and the written canonical are byte-identical)

- `whole_crop_gate` PASS on all ten crops.
- `gate_all` PASS 121/121 certified, launch-ready 114/121.
- `control_ladder_gate` 0/0; `variety_resistance_gate` 0; `variety_ladder_delta_gate` 0;
  `register_completeness_gate` PASS; `container_path_gate` 0.
- A54: `source_catalog_title_gate.py` has no CLI entry point (running it as a script checks nothing), so it was
  called as a function: 221 catalog entries inspected, 0 violations, and 1 when Purdue's title is removed.
  The promote also runs it on the post-state.
- `release_verify --slug strawberry --expect-changed <the other nine> --ref peach`: exactly the ten declared
  crops changed, catalog `+purdue_ext_bp69w`, no new violations. Its three section-E concerns (strawberry region
  keys `zone_8_presence` / `zone_10_desert_fold` absent on peach) are **identical base-vs-base**, so they predate
  this promote.
- Collision gate re-measured: whole output byte-identical on both states (50 lines, 36 / 12 open / 24
  registered), live positive control 33 / 9 / 24; pin advanced to `d8906b43`.
- **Full `tools/` tree: VERDICT PASS**, 254 entry points, 6,224 passed, the 2 known waived failures (PLA-544,
  PLA-161), 72 of 73 script-style files ran and 1 skipped (ran nothing, reported as such, not a pass).

## Consumers

- **plant-app:** the re-export already owed for PLA-533 (**PLA-628**) now carries this too. `MethodSheet.tsx`
  renders `control_methods[*].cautions`, and the ladder notes render in the guide chapters.
- **plant-astro:** through a submodule bump, the astro session's call. `pest-control.ts` and
  `PestsDiseasesCard.astro` read the ladders.

## Next

PLA-626 (apricot and plum rootstock delete-first) is staged on this post-state and gets its own promote, suite and
harness against `d8906b43`. It touches apricot and plum again, in rootstock fields this promote does not touch.
