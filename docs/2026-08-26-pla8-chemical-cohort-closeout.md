# PLA-8 -- the chemical-cohort close-out: seven pilot-era soft chemicals re-read (2026-08-26)

**This is the round that closes the catalog's safety-bearing surface.** Of 56 methods, ten are a
chemical a person applies to food. The three conventionals were re-read earlier on 2026-08-26
(`1330fe5d` -> `04b5aa69`); these seven -- `copper_fungicide`, `sulfur`, `neem_oil`, `spinosad`,
`insecticidal_soap`, `horticultural_oil`, `iron_phosphate_slug_bait` -- were sourced at the
2026-07-22/23 pilot and had never been held against UC IPM's hazard database. With this promote
the catalog audit is **DECLARED CLOSED**: batches now run straight through, minting a method only
when a batch genuinely needs one (melons will need `mancozeb`, uaiKey=30; that is growth, not debt).

Promote: `tools/promote_pla8_chem_cohort.py` (`04b5aa69` -> `674fab25`).

## The instrument, validated before it was trusted

- `tools/test_ucipm_uaidb.py` (offline control against the cached chlorothalonil page): **5/5**,
  run in the same pass as the reading, per the prep's instruction.
- chlorothalonil (uaiKey=115) re-fetched **live** as the positive control before any cohort page
  was read: water H, natural enemies L, bees medium, acute H, Prop 65 + US EPA -- byte-for-byte
  the validated 2026-08-26 reading.
- Thirteen pages read this round: the 11 the prep named (4 coppers, sulfur, neem oil,
  azadirachtin, spinosad, potassium salts of fatty acids, horticultural oil, iron phosphate),
  plus the control, plus **ferric sodium EDTA (8)**, read to answer the prep's "check which slug
  bait our entry means" question. Full grid in the promote's `RATINGS` table.

## Verdicts, method by method

| method | reading | verdict |
| -- | -- | -- |
| `neem_oil` (38, 91) | bees **MEDIUM** on both pages; acute L; chronic NKR | **THE DEFECT OF THE ROUND.** The caution said "UC IPM rates neem low in toxicity to bees" -- an invented rating: the band is medium, and pn7404, the caution's own anchor, makes NO bee-rating claim for neem at all (re-read this round to confirm). The false rating lived in THREE fields: the caution, the entry's `pros` ("Low toxicity to people, pets, and pollinators"), and one live rung (strawberry / aphids / `note_seasoned`). All three corrected; the dusk PRESCRIPTION is the medium band's own sunset-to-midnight allowance and is kept. Chlorothalonil's "Bee rating II" shape: right prescription, wrong attribution. |
| `copper_fungicide` (123-126) | acute splits **L / L / M / H**; hydroxide alone bee-medium; all four chronic NKR | **A class key whose members disagree, exactly as the prep predicted.** Copper octanoate (the copper soap; the only one with home products in UC IPM's retail survey, and the form our `find_it` names) and copper ammonium complex are acute Low; copper oxychloride sulfate Moderate; copper hydroxide **High, the DANGER band**. New caution names which, plus the chronic-absence half. |
| `insecticidal_soap` (50) | bees **low**; acute **M**; NE LM; chronic NKR | The pros claimed "Low toxicity to people, pets, and pollinators". Pollinators: TRUE (bee band low). People/mammals: NOT -- acute is Moderate. Pro narrowed to the supported half ("Low toxicity to bees and other pollinators"); new caution states the Moderate acute rating with its mild counterweights (chronic no known risk, lowest bee band). |
| `horticultural_oil` (142) | bees **medium**; acute L; NE L; chronic NKR | Silent on bees while its sibling contact sprays (neem, spinosad) both disclose. Silence, not wrong advice -- but a medium-band contact spray states its window under the disclosure standard. Standard medium-band sentence appended. |
| `spinosad` (64) | bees **medium**; NE LM; acute L; chronic NKR | **KEPT byte-for-byte.** Its "spray at dusk" is the medium band's own allowance -- the exact advice that was a defect on the HIGH-band conventionals is correct here -- and "do not apply to flowering plants" is stricter than the band requires. Every live spinosad rung (13 crops) advises dusk/evening: all conform. |
| `sulfur` (70) | bees low; NE **L-to-H**; acute L; chronic NKR | **KEPT byte-for-byte.** The NE split's alarming half is already disclosed by the predatory-mite caution; bee band low owes nothing. |
| `iron_phosphate_slug_bait` (24) | bees low; acute **VL**; NE L; chronic NKR | **KEPT byte-for-byte.** The entry means iron phosphate (= ferric phosphate; the `find_it` is correct that they are the same compound), NOT ferric sodium EDTA (8: the other bait chemistry, acute L, also chronic NKR -- read to confirm no split caution is owed). Every safety claim is the comparative "safer ... than metaldehyde", which UC IPM makes and which survives. |

## Decisions recorded, not just made

- **Copper gets NO bee caution, deliberately.** Copper hydroxide alone carries a band (medium);
  the home-garden form (octanoate) is unrated, and the entry gives no bee timing advice, so
  there is no wrong advice to fix and a class-level bee caution would over-claim. A guard pins
  the decision (`test_no_bee_caution_is_authored_for_copper_and_that_is_deliberate`).
- **Neem's entry describes the WHOLE OIL** ("azadirachtin plus the oil" in its own
  `how_it_works_seasoned`), so it anchors uaiKey=38, not 91. Both pages sit in the medium band,
  so the oil-vs-fraction split changes no verdict and no which-one caution is owed; their minor
  differences (water L vs M, acute L vs VL) are both mild.
- **The three kept methods gain NO `ucipm_uaidb` source.** Their entries' claims still rest on
  their pest notes; the uaidb verification is recorded here and pinned by `KEPT_PINS` guards,
  not laundered into their `sources` arrays. Adding a source without a claim resting on it is
  the `adding-is-not-resolving` shape.
- **"safest" joined the hygiene ABSOLUTES list.** New copy claiming a safety superlative is now
  refused at promote time.

## Findings filed, NOT fixed (existing prose, outside this round's scope)

1. **artichoke / snails-and-slugs / `note_beginner`**: "Iron phosphate bait is the safest option
   to use around pets and wildlife" -- an unhedged superlative where the source's claim is the
   comparative "safer than metaldehyde". Same family as the known swiss-chard "safe around pets
   and wildlife" absolute (playbook section 7), which is also still open. Rule the two together.
2. The playbook's standing content-defect list (swiss-chard iron-phosphate absolute, basil
   spacing contradiction, fig souring/endosepsis split) is unchanged by this round.

## The blast radius, exactly

- 4 methods changed: `copper_fungicide` (+1 caution), `neem_oil` (caution replaced, 1 pro
  narrowed), `insecticidal_soap` (+1 caution, 1 pro narrowed), `horticultural_oil` (+1 caution);
  each declares `ucipm_uaidb` and anchors its OWN ingredient page (125 / 38 / 50 / 142).
- 3 methods verified **byte-for-byte**: sulfur, spinosad, iron_phosphate_slug_bait.
- 1 crop changed: strawberry, one rung register (`aphids` / `neem_oil` / `note_seasoned`), with
  a revert-and-compare guard proving nothing else in the crop moved.
- 0 sources minted; `source_catalog` byte-identical.
- Method count 56, crop count 128, roster laddered 29 -- all unchanged.

## Rung sweep

All 38 safety-keyword rung notes across the seven methods were read (the scan and its
adjudication are in the session log). One carried the false neem rating (fixed, above). Every
"spray at dusk" rung sits on a medium-band material (spinosad x13, neem x3) and conforms. The
iron-phosphate rungs on swiss-chard and strawberry hedge comparatively and conform; artichoke's
is finding 1 above.

## Guards

Suite: `tools/test_promote_pla8_chem_cohort.py` (83 tests, green under pytest AND the direct
runner). `VerifyPostIsDriven` was written FIRST, per the conventional round's lesson (its twelve
first-run survivors included eight undriven verify_post guards). The suite has a real RED phase:
`test_pre_state_carries_the_defect` fails the false-rating scan against the shipped canonical.
The false-rating scan is deliberately SCOPED to medium-band methods because insecticidal_soap is
genuinely bee-low and its "Low toxicity to bees" pro is CORRECT -- an unscoped token scan flags
correct prose (conventional round, lesson 5).

Mutation harness: `tools/mutate_pla8_chem_cohort_suite.py` -- results recorded below after the
run (anchor preflight, positive control, sentinel, ~48 injections across 10 families).

One claim deliberately retained rather than trimmed: soap's narrowed pro keeps "and other
pollinators" alongside bees. The uaidb positively supports the bee half (band: low); the
pollinator extension is the pilot's pest-note claim, refuted by nothing read this round, and
erasing a sourced claim without a reading against it is the inverse defect.

## Gauntlet pre-flight (run against the post-state BEFORE applying)

- `gate_all` on the post-state: **121/121 PASS**.
- `release_verify` post vs base (`--slug strawberry`): A collateral exact (only strawberry among
  crops; top-level only `control_methods`; catalog +none -none; reference crop byte-identical),
  B **"no new violations introduced"**, C/D/F/G/H ok. The single E CONCERN (`rgv: novel region
  keys ['plantings_provenance']`) was re-run against the UNTOUCHED base and is present there too:
  it is strawberry's pre-existing campaign-B provenance block, baseline, not introduced here.

## Harness results (run 1, no reruns needed)

```
preflight        : all 50 anchors match exactly once
positive control : GREEN
sentinel         : RED as required
TOTAL: 49 caught, 0 survived, of 49 injected
  band 5/5  blast 8/8  hygiene 4/4  kept 2/2  mechanics 1/1
  preserve 7/7  rating 8/8  rung 2/2  source 5/5  split 7/7
RESULT: PASS
```

**Zero survivors on the FIRST run**, against the conventional round's 34/12. The difference is
one change of order: `VerifyPostIsDriven` was written before the rest of the suite instead of
after the harness reported, so every post-side guard had a driver from birth.

## Final gauntlet (live canonical, after --apply)

- canonical SHA `674fab25...` matches the suite's pinned POST_SHA; COMPACT preserved (no
  trailing newline, single line).
- `gate_all` **121/121 PASS**; `whole_crop_gate` PASS on strawberry (the touched crop) and
  apple (bystander with the densest ladder).
- `release_verify` vs base: A exact, B "no new violations introduced", the one E CONCERN
  baseline (adjudicated above).
- `control_ladder_gate` **0**; `register_completeness_gate` PASS.
- 88 tests green: 83 promote guards (pytest AND direct runner) + 5 parser controls.
- `test_gen_current_state.py` PASS after the state trio.

State trio: LATEST.txt -> `674fab25`, STATE_HISTORY.md prepended, CURRENT_STATE.md canonical
pointer amended surgically (Current -> Prior). NOT committed; commit awaits Trevor per protocol,
and plant-app owes a fresh `build:guides` AFTER this commit lands (the export it holds is
stamped to the prior canonical).
