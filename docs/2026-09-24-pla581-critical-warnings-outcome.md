# PLA-581 `critical_warnings` + `container_safety`: LANDED

**2026-09-24. `526788f2` -> `83384c85d9daccc71b3d4a0da795872a761538b0e4d8e94b0d401a674a8a6cd6`.**
PLA-7 Plan D. Register row 32. ONE promote; the 7 shells byte-identical. Spec
`docs/superpowers/specs/2026-09-21-pla581-critical-warnings-field-shape.md` (approved 2026-09-21 with
the 8.6 condition; corrections in section 13; the copy is section 14's, amendment 3).

## What landed

- **`critical_warnings` on all 121 certified crops, every one `null` = NOT ASSESSED.** Three documented
  states: `null` = not assessed, `[]` = assessed, none found, `[...]` = authored. Not `[]`, which would
  assert "assessed, none found" for PLA-142's harvest class on crops nobody has assessed. Key absent on
  the 7 shells.
- **`[]` and `[...]` are CLAIMS** and gate A61 refuses either without a `field_additions` record with
  `field == "critical_warnings"`. That is what stops a null -> `[]` collapse (the `not (x or [])` idiom
  the PLA-533 ratchet uses on purpose) from passing silently, at `gate_all`, forever, not only inside
  this promote.
- **A top-level DATASET key `container_safety = {warnings, field_additions}`**, the crop-invariant
  container warnings authored once (ruling 1 / D1). Consumers read `container_safety.warnings`, never
  the object; `field_additions` is provenance and never renders.

| id | title | cites (anchor) | also rests on |
|---|---|---|---|
| `balcony_load` | Ask what your balcony or roof can carry | `uiuc_ext` container-size | -- |
| `container_material` | Never grow food in a container with anything toxic in it | `csu_ext` container-gardens; `uiuc_ext` vegetable-containers | **the treated-lumber sentence** on `uiuc_ext` container-material-choices |
| `hanging_security` | Secure hanging containers well | `uiuc_ext` container-material-choices | -- |

`severity` is `high` on all three, **UNIFORM and MODELED**: no source grades these warnings, so no
ranking between them is claimed (Trevor, 2026-09-23). Measured before writing: no consumer renders this
field's severity today, and the existing pest/disease styling maps `high` to its strongest treatment
while leaving `critical` unmapped (noted on PLA-586). `stage` is `null`. **No figure in any copy**: the
gate refuses digits and the spelled numbers one through twenty, thirty through ninety, half, dozen,
hundred and thousand, because no source publishes a weight, a load or a count; the balcony warning is a
referral to an architect. A bare unit word is allowed, because the first approved copy needed one to
say no figure exists.

## The copy: three rounds of independent checking to 0 / 0

Section 4.4's approved bodies OVERREACHED their own cited pages, measured against the cached raw bytes:
no support for "structural support rather than trim or a light hook" or "the watered weight rather than
the dry weight"; "not over a spot where someone sits or walks" was only a drip sentence; the load
sentence names balcony and rooftop, not decks. All six bodies and three titles were REVISED in the
claude.ai lane (spec section 14, amendment 3; 4.4 stays byte for byte and is pinned against its
approval commit `f1c29e3`), then checked by **three independent reviewers** with no stake in the copy,
each working only from the four cached pages read in full, every quote re-verified against the bytes:

| round | unsupported | partial | what closed |
|---|---|---|---|
| 1 | 0 | 4 | a gloss, a ranking against CSU's own "most important thing ... is drainage", an overstated repeat, an unstated causal "since" |
| 2 | 0 | 3 | a sufficiency ("as long as") the sources contradict, and two connectives claiming links the page does not make |
| **3** | **0** | **0** | the structural fix: one claim per sentence, each mapping to a page sentence, no connective asserting its own link |

The one remaining "since" (`hanging_security` seasoned) is **Illinois's own link**: "It may drip on
people or possessions below. Consider this when determining placement of a hanging container." The wood
sentence was DROPPED: it sits under the page's rot question. **ONE DECLARED INFERENCE**, recorded as
declared, never as sourced: the last sentence of `container_material` seasoned ("If you cannot account
for what a repurposed container once held, that alone is a reason to keep food out of it."). Its
premises are sourced; the step from "holds" to "once held" is this project's. Advisory notes from round
3 (no verdict changed): the beginner body does not mention drainage, which CSU ranks first (it is
carried per crop in `container_notes`). No-figure rule and the repo's 8-gram verbatim rule clean on
every string (positive control 10 hits). Each record quotes every sentence its warning rests on, **9 in
total**, with each page's measured digest.

## Evidence

Re-read as raw bytes under two user-agents, byte-identical between them. Three pages reproduce the
spec's 2026-09-21 digests exactly. **`csu_ext` DRIFTED**: same 141,247 bytes, a new digest
(`a4dec7f1…`), the sentences present; no per-request token was found and the 09-21 bytes were not kept,
so **the cause is UNDETERMINED**, and the record says so in words rather than quoting a digest this
pass did not measure. So the next drift is diffable, the raw bytes are now kept locally in
`tools/.evidence_cache/<sha256>.html` with a TRACKED `MANIFEST.tsv` (commit `e6df8e2`).

## The consumer lines: COMMITTED, NOT RELEASED

**plant-app `7603b669` (`critical_warnings` classified SHIP) and `2c645d83` (the tolerant
`container_safety.warnings` read + the P6 loss assertion), both on `feat/pla-581-container-safety`, and
`378c7b9f` (the PLA-465 dimension-key classification, `feat/pla-465-dimension-keys`) are COMMITTED BUT
NOT RELEASED. Until `378c7b9f` ships, the app cannot rebuild from ANY canonical, this one included.**
The app's three PLA-465 keys were never classified, so its export build has been unable to run against
any canonical since PLA-465, and nothing caught it because no landing ran the consumer build.

**From this promote on, a landing's gauntlet includes the consumer build.** Run here in a throwaway
plant-app worktree, `2c645d83` merged `--no-commit` with `378c7b9f`, `PLANT_DATASET_SRC` at the
post-state: `build:guides` PASS (121 guides, **3 container safety warnings written**); `verify:export`
0 violations; **P6 live**: with `hanging_security` dropped from the artifact it refuses (rc 1), and on
the base (no `container_safety`) it is a no-op (rc 0). The build's provenance note that the dataset
commit does not carry the canonical is the expected mid-promote state.

## The pre-commit hook: E1 WAIVED, not bypassed

The write commit's hook passed every dataset check (**121/121 crops "no new violations"**) and blocked
on E1 alone: plant-app's shipped export is stamped `d7b33682`. The PLA-466 and PLA-580 landings bypassed
that with a blanket `--no-verify`, which also switches off every other check in the hook; on 2026-09-22
that pattern was ruled a convention doing a gate's job. **Ruled 2026-09-24: build the waiver.**
`tools/precommit_release_verify.py` now carries `EXPORT_WAIVERS`, the `run_test_tree` pattern: keyed on
the E1 check AND the frozen stamp `d7b33682f992` (an export rebuilt at any other SHA and still stale
blocks; E2 is never waived), ticket PLA-465, reason recorded, a waiver that stops firing reported STALE.
The first draft carried a separate `startswith` identity test that could never fire before the anchored
pattern did; REMOVED as unreachable. 8 drivers; **harness 7 injected / 7 caught / 0 survived / 0
broken**, positive control the whole waiver suite plus the existing script-style hook test, sentinel
reddened. **Proved live both ways**: identical staging, rc 1 (E1 BLOCKED) before the waiver and rc 0
(`WAIVED [PLA-465]`, 121 no new violations) after. This commit went through the hook, no `--no-verify`.

## Gauntlet on the landed bytes (`83384c85`)

| check | result |
|---|---|
| preflight (2026-09-24) | `git fetch` ok; origin/main still `047227c`; main checkout on `main` at `047227c`; worktree cut from `047227c`; canonical `526788f2` on disk -- the gauntlet ran on the landing base |
| promote `--expect-sha` | written; the gate inspected 121 null / 0 `[]` / 0 authored / 0 on shells, 3 warnings |
| suites | gate 85, promote 65, A61 script PASS, collision 27, export waiver 8 |
| PLA-581 mutation harness | **96 injected / 96 caught / 0 survived / 0 broken**; positive control all 3 suites whole; sentinel reddened; **null -> [] caught by name x4**: `one_crop_null_written_as_empty_list`, `null_checked_by_truthiness`, `state_of_collapses_empty_into_null`, `empty_list_record_not_required` |
| `gate_all` (floor from CLAUDE.md, no override) | **PASS 121/121 certified, launch-ready 117/121** (apple, pear-asian, pear-european, plum -- PLA-466's findings, unchanged) |
| A61 CLI `--presence`, all 128 | 0 violations; 121 null, 0 `[]`, 0 authored, 0 shells carrying, 3 warnings |
| injected into scratch copies | null -> `[]` reddens `gate_all` itself; a missing key and a missing `container_safety` redden `whole_crop_gate`; a key on a SHELL is invisible to `gate_all` by construction (certified only, as for A58-A60) and refused by `whole_crop_gate <shell>`, the A61 CLI and `check_post` |
| `release_verify` (121 declared, `--ref avocado`) | section A CLEAN (top-level changed: `container_safety` only; catalog unchanged; avocado byte-identical); B no new violations, CLEARS the A61 presence violations; C-H clean; 1 concern, the shell reference itself (vacuity queue item 7, filed `e5fd365`) |
| collision gate | WHOLE output byte-identical on both states, 50 lines, 36 findings / 12 open / 24 registered; positive control (plum's pests emptied) 33 / 9 / 24; pin RED stale, GREEN 27/27 advanced to `83384c85`; fixture untouched |
| `test_gen_current_state` (run directly) | PASS |
| `test_doc_roster_claim_gate` | PASS |
| consumer build | as above; inputs identical by SHA (plant-app `2c645d83` + `378c7b9f` unmoved, canonical `83384c85`) |
| full `tools/` tree | **VERDICT PASS**, runner rc 0 captured unpiped (48:34): **252 entry points** (179 collectable + 73 script-style; +4 over the `b3a9156` baseline's 248 = this session's four test files); pytest 2 failed / **6,167 passed** (+158 over 6,009 = the new suites, 85 gate + 65 promote + 8 export waiver), both failures WAIVED on identity and character (PLA-544, PLA-161), no STALE waiver; scripts 72/73 ran, 1 SKIPPED (`test_build_berry_pilot_patch`, as on the baseline) |

## Recorded, not fixed here

- **Vacuity queue item 7**: `release_verify` is red on every roster-wide run because its reference
  must be a shell; PLA-580's landing had the identical shape (rc 1 on base and post).
- **PLA-465 per-field addendum** (`1ee2a5d`): height authored 16 / null 105, spread 14 / 107; apple and
  lemon carry a recorded no-spread. The data were right; the note conflated two fields.
- **Spec corrections** (section 13, `c49fc2c`): `planting_layout` 4 block + 2 row; rule 9 unreachable;
  the "93 saucer sentences" figure not reproducible; `title` already ruled; tip-over 18 net-dependent.

## Unblocked / owed

- **PLA-594 (the astro dataset bump) is UNBLOCKED**: canonical now carries PLA-580 and PLA-581.
- **PLA-539**: release `378c7b9f`, then `7603b669` + `2c645d83`; rebuild the export against `83384c85`;
  the E1 waiver then reads STALE and is removed.
- **PLA-586**: the ContainerCard reads `container_safety.warnings` and chooses its severity treatment
  explicitly (`critical` is unmapped in both consumers today).
- **PLA-142**: the shape is fixed for the `harvest` class; every crop it assesses moves `null` -> `[]`
  or `[...]` WITH a `critical_warnings` record, a free progress metric.
