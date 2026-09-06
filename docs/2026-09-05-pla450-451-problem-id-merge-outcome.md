# PLA-450 + PLA-451 close-out -- six duplicate-id merges, two held, the celery blight split

**Date:** 2026-09-05. **Lane:** Claude Code. **Canonical:** `95e66f6d` -> `36d6df6b`, ONE promote,
NINE `id` leaves on six crops, nothing else. **Commit held for Trevor's approval.**

---

## 1. What shipped

| file | what |
|---|---|
| `tools/promote_pla450_451_problem_ids.py` | the promote: 12 checks, prediction guard, refusal specs |
| `tools/staging/pla450_451_problem_ids/spec.json` | the nine rows (7 merge, 2 mint) and the two held pairs |
| `tools/test_promote_pla450_451_problem_ids.py` | 63 tests, fixture rebuilt from `95e66f6d`, output SHA pinned |
| `tools/mutate_pla450_451_problem_ids_suite.py` | 42 mutations / 42 caught / 0 survived / 0 broken |
| `tools/problem_id_registry.json` | +2 entries: the celery splits, organism-level reasons |
| `tools/test_problem_id_collision_gate.py` | RE-MEASURED to `36d6df6b`: 27/27, harness 28/28 |
| `docs/ladder_batch_playbook.md` | 5a: collision-gate re-measure is a required close step |
| `tools/promote_fixture.py` | the `890fdf7` pin is now NEVER-AMEND (this suite rebuilds from it) |

## 2. Order: T1 first

PLA-451's attribution came from claude.ai knowledge. Read before any merge work, on the crop's own
cited anchors:

| page | names | says of the tomato/potato disease |
|---|---|---|
| UC IPM celery / early blight | *Cercospora apii* | "do not confuse this disease with the early blight disease that occurs on tomato and potato, which is caused by an *Alternaria* species" |
| UC IPM celery / late blight | *Septoria apiicola* | "not the same as late blight of tomato and potato caused by *Phytophthora infestans*, which does not infect celery" |

Confirmed. `celery-early-blight` and `celery-late-blight` minted; names untouched; both pairs
registered.

## 3. The eight pairs, one verdict each

| pair | verdict | organism evidence |
|---|---|---|
| cutworm (asparagus) -> cutworms (10) | **merged** | umbrella noctuid complex on both sides |
| flea-beetle (swiss-chard) -> flea-beetles (35) | **merged** | chard and beet prose near-identical: "several species ... chard, beet, and spinach are all hosts" |
| japanese-beetle (basil) -> japanese-beetles (7) | **merged** | *Popillia japonica* on both |
| botrytis-gray-mold (artichoke) -> gray-mold (7) | **merged** | *Botrytis cinerea* on both |
| twospotted-spider-mite (artichoke) -> two-spotted-spider-mite (6) | **merged** | *Tetranychus urticae* |
| snails-and-slugs (artichoke), slugs (strawberry) -> slugs-and-snails (12) | **merged** | mollusk umbrella; strawberry's slugs-only scope joins the umbrella |
| bacterial-leaf-spot (cilantro) vs bacterial-spot (5 peppers) | **HELD** | cilantro: *Pseudomonas syringae* pv. *coriandricola* (own cause prose; WSU Mt Vernon anchor, read today, adds two coriander-specific *Xanthomonas* pathovars as less common). peppers: *Xanthomonas* (own cause prose; NCSU/Clemson). Different pathogens. |
| bacterial-blight (edamame) vs bacterial-blights (3 beans) | **HELD** | edamame: *P. savastanoi* pv. *glycinea* (own prose; ISU anchor; UMN read today, which also lists snap and lima bean as hosts of that pathovar). beans: *X. campestris* pv. *phaseoli* + *P. syringae* pv. *phaseolicola* (own prose; Clemson read today, no soybean). Different pathogens. |

The registry's own batch-26 entry for `mulberry-bacterial-blight` had already written down that
edamame's and the beans' organisms differ; PLA-448 s4a listed the pair on the name alone.

**Why hold rather than merge or fix:** merging would create the defect PLA-451 fixes (one id,
two pathogens). Minting a scoped id is the house pattern but is a ruling Trevor has not made. The
promote carries both pairs as `HELD` and REFUSES a spec row on either (mutation-proved), and both
stay OPEN and UNREGISTERED in the collision gate, which is the decision surface.

### Decision-ready: the two held pairs

| option | what it does | cost |
|---|---|---|
| **B (recommended)** mint `cilantro-bacterial-leaf-spot` and `edamame-bacterial-blight`, register both pairs | the `celery-early-blight` / `bacterial-spot-pruni` / `sweet-potato-black-rot` pattern; a future *Xanthomonas* author cannot reuse cilantro's generic id by accident | one promote, two `id` leaves, same guard shape as this one; `actionable` 14 -> 12, registered 22 -> 24 |
| A register as-is | writes the adjudication down, ids unchanged | leaves two generic ids one letter/word apart naming different pathogens: the trap the gate cannot see once the id is REUSED rather than minted |
| C merge as PLA-450 listed | -- | refuted; creates the PLA-451 shape |

## 4. The prediction ledger

| | raw | registered | actionable |
|---|---|---|---|
| baseline `95e66f6d` | 42 | 20 | 22 |
| **predicted, pinned before the first run** | **36** | **22** | **14** |
| observed `36d6df6b` | 36 | 22 | 14 |

Mechanism: eight OPEN pairs retire because their minority id ceases to exist (five two-id merges,
plus the three-pair slug family); no registered pair named a retired id; each celery mint adds one
NAME_SHARED pair against the generic id it left ('blight early' == 'blight early'), both
registered. The moved names create no third collision (no other id owns the keys 'cutworm',
'flea beetle', 'japanese beetle', 'gray mold', 'mite spider twospotted', 'slug', 'and slug snail')
and neither mint sits within edit distance 2 of any live id. `check_collision_prediction` refuses
any other figure; the suite pins the literals independently and asserts the exact eight that vanish
and the exact two that arrive.

If all eight had been merged as filed: 33 / 21 / 12 (the mulberry / bacterial-blight registered
pair would have died with its id).

## 5. The variety join

`varieties` is a dict with `recommended[]`. A list-shaped walk returned **0** and would have read as
"no consumers". The right shape gives **129**: apple 102 (apple-scab 32, fire-blight 24,
powdery-mildew 24, cedar-apple-rust 22), strawberry 22 (red-stele 10, verticillium-wilt 10,
anthracnose 2), asparagus 5 (asparagus-rust 2, purple-spot 2, fusarium-crown-rot 1). **None sits on
any id this promote touches.** Both states resolve; the retired-id arm is a refusal spec.

## 6. Gauntlet

| check | result |
|---|---|
| promote suite | 63/63 |
| mutation harness | 42 injected / 42 caught / 0 survived / 0 broken; anchors 42/42; positive control green; sentinel reddened |
| `whole_crop_gate` x6 | PASS, A57 green on every one |
| `gate_all` | 121/121 |
| `control_ladder_gate` | 0 integrity / 0 unladdered |
| `variety_resistance_gate`, `variety_ladder_delta_gate` | 0 / 0 |
| `register_completeness_gate` | PASS |
| `release_verify --base <95e66f6d> --slug celery --expect-changed artichoke,asparagus,basil,strawberry,swiss-chard --ref lettuce-leaf` | clean; exactly the six declared crops changed; lettuce-leaf byte-identical; no top-level or catalog delta |
| collision suite re-measure | 27/27 at `36d6df6b`; harness 28/28 |
| full `tools/` tree | see the Linear close-out (43-minute run) |

**A57 stayed green.** `verify_post` checks ladder presence BEFORE the generic field loop. The first
draft had it after, where the field-equality check fired first and the driver failed on the wrong
message; that is the earlier-check-masks-guard pattern and it was fixed at authoring, not found later.

## 7. Artichoke, reviewed as one crop

| finding | status |
|---|---|
| 3 variant ids (`botrytis-gray-mold`, `twospotted-spider-mite`, `snails-and-slugs`) | merged |
| its 11 problem entries carry only `id`, `type`, `name`, `control_ladder` -- no cause / symptoms / prevention, no severity, no sources. asparagus's 5 are the same. **The other 897 entries carry 8 to 16 keys.** | reported. This is WHY the binomials sit in `name`: no `cause_*` field exists to hold the organism. The pest prose lives in `watering`, `tips_by_stage`, `full_harvest_notes_*`. |
| remaining ids: `artichoke-plume-moth`, `artichoke-aphid` (*Capitophorus elaeagni*), `artichoke-curly-dwarf`, `black-tip`, `bacterial-crown-rot` (singleton) | correctly crop-scoped or the only such id; nothing to do |
| `cutworms`, `powdery-mildew`, `verticillium-wilt` | already on the majority id |
| binomial parentheticals in `name` | PLA-453, out of scope; a fix should first decide where the organism goes on a four-key entry |

## 8. The July-cert duplicate scan (report only)

The 2026-07-02 cert waves (`1b00730` .. `c95dcbf`) touched the problem arrays of 30 crops. Per
wave, entries ADDED whose normalized name already existed on the crop: **only the three pear
duplicates** batch 26 retired (pear scab on both pears, Fabraea leaf spot on pear-european, all in
`73a1f64`). Live canonical: **0** within-crop name duplicates across all 128 crops. A looser
same-token / same-binomial scan over the 30 crops produced 30 candidate pairs; all read, all distinct
problems. **The pattern did not recur.**

## 9. The wider PLA-451 scan

Every id on two or more crops, compared by the genera the crops' own prose names: the celery pair
was the only clear same-id-different-pathogen case. One umbrella noted, not filed:
`bacterial-soft-rot` is "*Pectobacterium* species" on cilantro and "*Pectobacterium* /
*Pseudomonas* species" on cauliflower; both entries describe the soft-rot complex.

## 10. Not verified, by name

PLA-457, PLA-448 s4d, monitor_and_tolerate, PLA-453 naming; the two held pairs (await a ruling);
the four-key entry schema on artichoke and asparagus (reported, no ticket filed by me). Post-commit:
register `36d6df6b` -> its commit hash in `promote_fixture.COMMIT_FOR`; the plant-astro bump belongs
to the astro session; plant-app's E1 export is one more revision behind.
