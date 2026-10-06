# PLA-673 part B2 promote bundle (base 3ccc25f1)

Re-authors the unsupported-claim leaves from hashed packets, in both registers:
- eggplant `diseases[3]` (`id=phytophthora-blight`):
  - `prevention_seasoned` (6 sentences, with the ruled NC State rotation precedence)
  - `prevention_beginner` (5 sentences)
  - the entry's sources become `[clemson_hgic, ncsu_ext_phytophthora_blight_peppers]`, each anchored and verified 2026-10-06
- the four squash soil_prep pairs (pumpkin, butternut, acorn, spaghetti), with their PLA-674 citation backfill
- parsnip's three hilling leaves (itersonilia-canker prevention, canker next-season tip, established-stage action)

It also mints two document-level ids and arms A62 on soil_prep. Peppers stay HELD (PLA-688).

## Run (Trevor's go only)

```
python3 tools/promote_pla673_b2.py --check
python3 tools/promote_pla673_b2.py --expect-sha aaf004a23eb52005962c399d9f2f779b98b6226dacba0f454dff4442c1324812
```

The post SHA is pinned three ways, and they agree:
- build_stage.py's INDEPENDENT minimal apply (no promote code) gives `aaf004a2...`
- the promote's `--out` gives the same
- the suite pins it (`POST_SHA`)

## Contents

| file | what |
|---|---|
| `b2_texts.py` | the approved texts, VERBATIM, each sentence mapped to packet rows (B2 / BS / PS / PP), with the ruled sources per citation block |
| `catalog_mints.json` | `ncsu_ext_phytophthora_blight_peppers` (b59564c6), `umass_ext_itersonilia_canker` (e1f62141) |
| `build_stage.py` | writes ops.json / EVIDENCE.tsv / DECISIONS.tsv; prints the independent post SHA |
| `ops.json` | 34 ops: prose 16, sources 8, anchors 8, catalog 2 |
| `EVIDENCE.tsv` | 109 rows; every quote proven a substring of the cached page bytes |
| `DECISIONS.tsv` | 6 rows: precedence-rule (eggplant), re-keyed umass_ext anchor, usu_ext REMOVED from parsnip's canker entry (go-condition 1), new citation block on parsnip `growth_stages[id=established]`, inline "(UMass)" dropped (no consumer reads it), a62-armed |
| `derive_promote.py` | the asserted edit list that derived `tools/promote_pla673_b2.py` from `promote_pla666_row_figures.py` |

## Tools landing with the data commit

- `promote_pla673_b2.py` adds three guards to the PLA-666 set:
  - R: dual register; both siblings must be edited and never byte-identical
  - S: no soil_prep spacing restatement
  - M: the glossary's own match classifies the post roster at exactly 225 leaves
- Its gate step runs whole_crop_gate on the 6 edited crops, then gate_all with the population reported.
- `test_promote_pla673_b2.py` has 46 tests, one real-stage test plus one injected defect per refusal. `mutate_promote_pla673_b2.py`: **40/40 caught**, with anchor preflight, sentinel and the whole suite as positive control.
- **A62 arms soil_prep** (`SOIL_PREP_ARMED = True`). The waiver set goes 2629 → **2663**: +35 soil_prep identities, measured on the post-state, and −1 for `parsnip|growth_stages[id=established]`, which B2 cites. CLOSED gains six era identities: watermelon, the four squash, and the parsnip stage. `KNOWN_AT_ARMING` is 2674.
- **Era switch** `SBR_KNOWN_AT_ARMING`, hardened at go-condition 2. Its value must be the gated file's own sha256, registered in `ERA_POST_STATES` (3ccc25f1 glossary, afbd4113 Phase C), and NOT the live canonical.
  - `whole_crop_gate` and `gate_all` bind it before gating; any other value exits 2 with no verdict.
  - A set-but-unbound switch refuses at first use.
  - The pre-commit hook strips it from its gate runs and refuses a gate run with no `GATE:` verdict.
  - The glossary and Phase C promotes pass their post-state's sha256.
  - Tests: `test_era_switch_safety.py` plus the ratchet suite's `EraSwitchIsBoundToAHistoricalPostState`, written first and confirmed RED, then GREEN.
  - Mutations: `mutate_era_switch_safety.py` 5/5; ratchet harness "era" family 8/8.
- `test_glossary_sense.py` re-pins the live population: 225 (102 hill / 60 hilling / 63 none). PEPPER_LEAVES now lists the two peppers only. The injection helper now replaces a null slot.
- `test_sourced_block_ratchet_gate.py`:
  - the waiver pins, family counts and CLOSED sets above
  - the 98-slot walk now skips a sibling whose claim keys are empty (fbe11bc shipped red there on the PLA-674 null siblings); its bound is 133
  - new SoilPrepArmed and EraSwitch classes
- `promote_fixture.py` pins `3ccc25f1 → fbe11bc` (pin-only).
- `gate_all.py` says when the era set is in force.
- `promote_housekeeping60_phase_c.py` sets the era switch on its whole_crop_gate call. Its post-state (afbd4113) predates watermelon's soil_prep citation, and the full tree reddened its replay on exactly that. It is the only one of the four landed promotes that call the gates to redden.
- `test_problem_id_collision_gate.py` re-pins to aaf004a2. The glossary landing missed this re-measure, so the preflight has been red on main since fbe11bc. The gate's output is byte-identical on 350eda38, 3ccc25f1 and aaf004a2: 36 findings, 12 open, 24 registered.
- `mutate_citation_ratchet_gates.py`:
  - flag mutation re-anchored to True → False
  - era mutation re-anchored to `_default_known()`
  - two new era-switch mutations
  - armed-argument driver repointed to the explicit-False test
- fbe11bc also shipped two red tests on main, both fixed here:
  - the ratchet's 98-slot walk
  - the sense guard's null-slot injection

## Verification (scratch worktree, canonical = aaf004a2)

- Full tree: 7,027 passed. Four failures, now resolved:
  - two were my own (a family-count line my comment swallowed, and the collision pin)
  - one was the Phase C era replay
  - one is LATEST.txt, which clears at landing
- After the fixes, the failed suites plus every changed suite: 347 passed, rc 0.
- Mutation harnesses (0 survived, 0 broken in each):

  | harness | caught |
  |---|---|
  | B2 promote | 40/40 |
  | glossary promote | 54/54 |
  | Phase C promote | 31/31 |
  | citation ratchets | 52/52 |
  | sense guard | 28/28 |

- Gates:
  - gate_all: PASS 121/121, launch-ready 114/121
  - whole_crop_gate: PASS on all six edited crops
  - release_verify: clean (only the 6 declared crops changed; catalog +2)
  - doc_roster_claim_gate: 0 violations with the LATEST line below
  - export staleness: E1 red until `build:guides` reruns in plant-app; E3 red until the astro bump (both expected)

## Sense-guard fixture (re-pinned)

`../pla673_674_prep/glossary-match.fixture.json` gains one case, `hilling-parsnip-sentence-initial`:
- text: "Hill soil over the root shoulders throughout the season."
- expected class: hilling

New pin: **sha256 `990eac25f6509bbccda4f48bbc58ef3f5312e0facaf14332dd8198736d9a8618`** (5,280 B, 32 cases). The guard agrees on all 32 cases. The canonical `match` equals the staged one. plant-app's pin (01912d65) must move to this sha.

## Proposed LATEST.txt

```
SHA: aaf004a23eb52005962c399d9f2f779b98b6226dacba0f454dff4442c1324812
Date: 2026-10-06
Session: PLA-673 PART B2 LANDED: 3ccc25f1 -> aaf004a2. Unsupported-claim leaves re-authored from hashed packets, both registers (claude.ai texts approved by Trevor, rounds 1-2): eggplant phytophthora-blight prevention (ruled precedence: NC State's P. capsici page governs Clemson's multi-disease rotation paragraph); pumpkin, butternut, acorn, spaghetti soil_prep (+ PLA-674 citation backfill: uga_c1206_homegrown_pumpkins, umn_ext); parsnip itersonilia-canker prevention, canker next-season tip, established-stage action (UMass, UMN, RHS, Clemson; usu_ext, an index page, removed from the canker entry). 109 evidence rows. 2 catalog mints (ncsu_ext_phytophthora_blight_peppers, umass_ext_itersonilia_canker). A62 ARMED on soil_prep: waiver set 2663 (+35 soil_prep, -1 parsnip stage cited), era switch SBR_KNOWN_AT_ARMING. Sense guard 225 leaves (102 hill / 60 hilling / 63 none); fixture 990eac25. Peppers HELD (PLA-688). Certified 121, launch-ready 114. Record: tools/staging/pla673_b2/, Linear DECISIONS sections 11-12; PLA-692 filed.
```
