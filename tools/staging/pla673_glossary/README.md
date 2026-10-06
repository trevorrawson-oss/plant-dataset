# PLA-673 / PLA-674 glossary promote bundle

Base canonical `350eda38` (main `ffdaa4a`). Post-state **`3ccc25f194cf0b3808877546b160572ab7ac6a12dbc7dae891f37d43f21a717a`**.
**Not run against canonical; Trevor runs the promote.**

## What it does

* **Top-level `glossary`** (new key, appended): `hill` and `hilling`, each carrying exactly the seven ruled keys:
  `term`, `definition_beginner`, `definition_seasoned`, `sources`, `anchoring_urls`, `field_additions`, `match`.
  * Definitions are verbatim from claude.ai, approved by Trevor 2026-10-05, round 2: 34 sentences, all evidenced.
  * `sources` are document-level ids only.
  * `match` holds the ruled matcher (sense / forms / crops / refuse_on / exclusions).
* **PLA-674:** `soil_prep_sources` and `soil_prep_anchoring_urls` on **all 128 crop records** (D14), placed right after each record's last `soil_prep_*` key (else at the end).
  * Null on 127 records (D13: not assessed).
  * Watermelon is backfilled: `["uga_ext", "clemson_hgic"]`, from the 14 Housekeeping 60 Phase C EVIDENCE rows, re-proven against their hashed bytes.
* **source_catalog: 10 new document-level ids:**
  * part A: `purdue_ext_ho8wa`, `csu_ext_cucurbits_07609`, `nmsu_ext_cr457`, `uga_b577_home_gardening`
  * STOP 2: `umn_ext_potatoes`, `umn_ext_carrots_parsnips`, `umn_ext_leeks`, `umn_ext_cucumbers`, `usu_ext_leeks`, `clemson_hgic_homegrown_grits` (pinned to MANIFEST `65d1d7cb`; the second row `d533df5c` is recorded)
  * Crop-level anchors keep their portal ids (no re-keying; PLA-686 tracks the B577 seven).

## Files

| file | role |
| -- | -- |
| `build_stage.py` | builds ops.json / EVIDENCE.tsv / DECISIONS.tsv from the ruled inputs in `../pla673_674_prep/`; prints the post SHA from an INDEPENDENT minimal apply |
| `ops.json` | 268 ops: 10 catalog, 2 glossary, 256 sibling |
| `EVIDENCE.tsv` | 78 rows: 64 glossary sentence rows + 14 watermelon soil_prep rows |
| `DECISIONS.tsv` | 13 rows |
| `../../promote_pla673_glossary.py` | the promote (guards B V S GL C D G) |
| `../../test_promote_pla673_glossary.py` | its suite (63 tests; the pre-state is replayed from `ffbbc35`) |
| `../../mutate_promote_pla673_glossary.py` | its mutation harness: **54/54 caught** (+ sentinel red, positive control green) |
| `../../glossary_sense.py` (+ test, + mutate) | the sense guard the promote's GL guard runs over the post roster |

## Tools changes in the same commit

* `tools/export_staleness_gate.py`: `src/data/glossary.json` added to `APP_ARTIFACTS` (+ a pinning test). **From this edit until the app re-export, E2 is RED**: the current app stamp has 4 artifacts. Expected, and cleared by step 4 below.
* `tools/sourced_block_ratchet_gate.py`: `soil_prep` named in `SIBLING_BLOCKS` (A62 discovery would otherwise fail all 121 crops on the new keys), behind `SOIL_PREP_ARMED = False`. Arming it is a ruling (PLA-674): about 39 prose-carrying crops would become new uncited blocks.
* `tools/promote_fixture.py`: `COMMIT_FOR['350eda38…'] = 'ffbbc35'` (pin-only; the suite replays its base).
* `tools/live_pin_registry.py` (+ its test's population, now 64 / 26 / 68 / 45): `test_glossary_sense.py` registered as a LIVE pin (8 pins: the 232-leaf population and its splits); `test_promote_pla673_glossary.py` EXEMPT (replay).
* `tools/mutate_citation_ratchet_gates.py`: 3 soil_prep mutations added.
* New: `tools/glossary_sense.py`, `tools/test_glossary_sense.py`, `tools/mutate_glossary_sense.py`, `tools/promote_pla673_glossary.py`, `tools/test_promote_pla673_glossary.py`, `tools/mutate_promote_pla673_glossary.py`.
* `tools/.evidence_cache/MANIFEST.tsv`: 3 rows (Purdue `740cafac`, CSU `751295b3`, Clemson eggplant `635ebdeb`).

## Proof (2026-10-05, on the scratch post-state)

* promote `--check`: 268 ops, 34 sentences, 64 + 14 evidence rows proven against hashed bytes, match inspected 232, **gate_all PASS 121/121** (launch-ready 114/121), post `3ccc25f1` == the independent minimal apply.
* `release_verify --base canonical --expect-changed <all 128>`: A ok (the 128 declared, catalog +10, glossary added); B no new violations; D/E/F/H ok; ONE concern, "reference crop lettuce-leaf CHANGED": its only diff is the two null siblings. This is roster-wide by design (the 2026-07-12 precedent ruled it BENIGN: the tool's single-crop-pilot assumption).
* Affected set (`run_test_tree --files`, 18 entry points): **PASS**, 628 passed + 3/3 script-style.
* Harnesses: promote 54/54; glossary_sense 28/28; citation ratchet 31/31 + bare 15/15 + wiring 4/4; export staleness 13/13. Each with its sentinel red and positive control green.
* DEVIATION: the promote was written before its suite (no RED phase). Stand-ins: POST_SHA from an independent apply, and the 54-mutation harness (whose first run found 5 suite gaps, all closed).

## Shared match fixture (consumers' step 3)

`../pla673_674_prep/glossary-match.fixture.json`, **sha256 `01912d659aa3492514347ea9cdc343e23d0a769a4c533155e64052b521af59a8`** (5,122 B, 31 hand-written cases). Both consumers adopt it byte-identically in step 3 (the PLA-651 pattern) and test their matcher against it. It changes only by a ruling.

## Running it (Trevor)

1. `python3 tools/promote_pla673_glossary.py --check`: expect `350eda38 -> 3ccc25f1…` and `gate_all PASS on 121`.
2. `python3 tools/promote_pla673_glossary.py --expect-sha 3ccc25f194cf0b3808877546b160572ab7ac6a12dbc7dae891f37d43f21a717a`
3. **plant-app:** the local `~/plant-app` checkout must contain `0f3864ae` (it was at `371a0f4a` on 2026-10-05, behind origin/feat/community-foundation). Pull it, then `npm run build:guides`. That re-exports at `3ccc25f1` and writes `src/data/glossary.json` (5 stamped artifacts).
4. `python3 tools/export_staleness_gate.py` must show 0 violations before the dataset commit (the pre-commit hook's E1/E2).
5. State trio: CURRENT_STATE (surgical amend), STATE_HISTORY (prepend), LATEST.txt (below).
6. plant-astro: submodule bump (the astro session's job; its accept commits `b9b2c49` + `23df2d5` are on origin/main).

## LATEST.txt (proposed)

```
SHA: 3ccc25f194cf0b3808877546b160572ab7ac6a12dbc7dae891f37d43f21a717a
Date: 2026-10-05
Session: PLA-673/674 GLOSSARY LANDED: 350eda38 -> 3ccc25f1. Top-level glossary (hill, hilling): 34 definition sentences authored in claude.ai and approved by Trevor (round 2), each mapped to hashed quotes (64 evidence rows), document-level sources only, ruled match lists (sense guard 232 leaves: 108 hill / 60 hilling / 64 none; pepper/eggplant 'beds or hills' none pending part B2). PLA-674 soil_prep_sources + soil_prep_anchoring_urls on all 128 crop records, null = not assessed, watermelon backfilled (uga_ext, clemson_hgic). 10 catalog mints (purdue_ext_ho8wa, csu_ext_cucurbits_07609, nmsu_ext_cr457, uga_b577_home_gardening, umn_ext_potatoes, umn_ext_carrots_parsnips, umn_ext_leeks, umn_ext_cucumbers, usu_ext_leeks, clemson_hgic_homegrown_grits). A62 names soil_prep (unarmed); APP_ARTIFACTS + glossary.json. Shared match fixture 01912d65. Certified 121, launch-ready 114. Record: tools/staging/pla673_glossary/, Linear 'PLA-673 / PLA-674 step 2A prep: DECISIONS'.
```
