# PLA-450 Option B close-out -- the two held pairs scoped, both generic ids vacated

**Date:** 2026-09-05. **Lane:** Claude Code. **Canonical:** `36d6df6b` -> `72371c02`, ONE promote,
TWO `id` leaves, nothing else. **Commit held for Trevor's approval.** Parent write-up:
`docs/2026-09-05-pla450-451-problem-id-merge-outcome.md`.

---

## 1. The ruling

Trevor, 2026-09-05: **Option B.** Mint `cilantro-bacterial-leaf-spot` and `edamame-bacterial-blight`;
register both pairs against the generic ids they diverge from. The deciding argument is reuse: the
collision gate checks a MINT and never a REUSE, so registering as-is would have left two generic ids
one word apart naming different pathogens, and a future *Xanthomonas* author attaching to cilantro's
generic `bacterial-leaf-spot` would have fired nothing. Scoping closes that permanently.

Pattern: celery-early-blight, bacterial-spot-pruni, southern-bacterial-wilt, sweet-potato-black-rot,
cane-anthracnose, mulberry-bacterial-blight.

## 2. What shipped

| file | what |
|---|---|
| `tools/promote_pla450_option_b_scoped_ids.py` | the promote: ruling frozen, vacate guarded, prediction guarded, baseline registry pinned to a commit, post registry from a staged snapshot |
| `tools/staging/pla450_option_b_scoped_ids/registry_post.json` | the registry snapshot that shipped; the write path refuses if the working registry differs |
| `tools/promote_pla450_451_problem_ids.py` + suite + harness | the PARENT promote, re-pinned to read the registry from git at `c189d65` (section 9); 64/64, 43/43 |
| `tools/staging/pla450_option_b_scoped_ids/spec.json` | the two rows |
| `tools/test_promote_pla450_option_b_scoped_ids.py` | 63 tests, fixture rebuilt from `36d6df6b`, output SHA pinned |
| `tools/mutate_pla450_option_b_scoped_ids_suite.py` | 44 mutations / 44 caught / 0 survived / 0 broken (after one vacuous driver was replaced, section 9) |
| `tools/problem_id_registry.json` | +2 entries sourced to the T1 anchors; the batch-26 mulberry entry repointed with a dated note |
| `tools/test_problem_id_collision_gate.py` | RE-MEASURED to `72371c02`: 27/27, harness 28/28 |

## 3. Vacated, measured then proved

| id | on `36d6df6b` | on `72371c02` |
|---|---|---|
| `bacterial-leaf-spot` | cilantro-coriander only | **nowhere** |
| `bacterial-blight` | edamame only | **nowhere** |
| `cilantro-bacterial-leaf-spot` | nowhere | cilantro-coriander only |
| `edamame-bacterial-blight` | nowhere | edamame only |
| `bacterial-spot` | 5 peppers | 5 peppers, untouched |
| `bacterial-blights` | 3 beans | 3 beans, untouched |

The singleton premise is a guard: a second holder of either generic id refuses the promote, because
that would be a rename of a shared id, not a scoping.

## 4. The registry, three ways

1. `cilantro-bacterial-leaf-spot` / `bacterial-spot`: cilantro *Pseudomonas syringae* pv.
   *coriandricola* (own cause prose; WSU Mt Vernon, which adds two coriander-specific *Xanthomonas*
   pathovars as less common) vs pepper *Xanthomonas* (NCSU, Clemson).
2. `edamame-bacterial-blight` / `bacterial-blights`: edamame *P. savastanoi* pv. *glycinea* (own
   prose; ISU; UMN, which also lists snap and lima bean as hosts) vs bean *X. campestris* pv.
   *phaseoli* + *P. syringae* pv. *phaseolicola* (Clemson, no soybean).
3. The batch-26 entry (`mulberry-bacterial-blight`, `bacterial-blight`) repointed to
   `edamame-bacterial-blight` with a dated note; the adjudication is unchanged.

The promote refuses a reason that omits an organism or an anchor, a registry entry naming a
vacated id, or a moved pair that is no longer registered.

## 5. The prediction ledger

| | raw | registered | actionable |
|---|---|---|---|
| baseline `36d6df6b` (registry as committed at `074f9e2`) | 36 | 22 | 14 |
| **predicted, pinned before the first run** | **36** | **24** | **12** |
| observed `72371c02` | 36 | 24 | 12 |

Raw does not move. Per scoped id: the OPEN pair with the generic it diverges from retires with the
dead id, and the scoped id collides NAME_SHARED with that same generic, registered. For edamame there
is more: the registered (`bacterial-blight`, `mulberry-bacterial-blight`) pair dies with the id and
comes back as (`edamame-bacterial-blight`, `mulberry-bacterial-blight`) under the repointed entry,
and because the normalized name 'bacterial blight' now has three owners (beans, mulberry, edamame)
the scoped id also pairs with mulberry. Neither scoped id sits within edit distance 2 of any live id
(nearest: mulberry-bacterial-blight at 8); no name carries a conjunction outside a deleted
parenthetical. Retired: 3 pairs. Arrived: 3 pairs, all registered, all NAME_SHARED only.

The close-out's estimate (14 -> 12) was derived first and agrees.

**The first `--check` run refused, on the baseline.** The guard read the pre-state with the WORKING
registry, where the mulberry entry had already been repointed, so the pre-state showed
36 / 21 / 15, a transitional figure that is neither state; the post-state had not been measured.
The fix pins WHICH registry the baseline means: the promote reads it from git at `074f9e2`, the
commit the 36 / 22 / 14 figure was measured at. Pinned to a commit, never HEAD, because once this
lands HEAD's registry is the new one and would read 36 / 21 / 15 on the pre-state forever. The suite
asserts the transitional figure so the reason is on record, and mutations that read the working
registry or move the pin to HEAD are caught. The prediction was not touched.

## 6. Gauntlet

| check | result |
|---|---|
| promote suite | 63/63 |
| mutation harness | 44 injected / 44 caught / 0 survived / 0 broken; anchors 44/44; positive control green; sentinel reddened |
| `whole_crop_gate` cilantro-coriander, edamame | PASS, A57 green on both |
| `gate_all` | 121/121 |
| `control_ladder_gate` | 0 integrity / 0 unladdered |
| `variety_resistance_gate`, `variety_ladder_delta_gate` | 0 / 0 |
| `register_completeness_gate` | PASS |
| `release_verify --base <36d6df6b> --slug cilantro-coriander --expect-changed edamame --ref lettuce-leaf` | clean; exactly the two declared crops; lettuce-leaf byte-identical; no top-level or catalog delta |
| variety references | 129 (apple 102, strawberry 22, asparagus 5), all resolve on both states, none on the four affected ids |
| independent deep diff vs the rebuilt pre-state | exactly the two `id` leaves |
| collision suite re-measure (playbook 5a) | 27/27 at `72371c02`; harness 28/28 |
| full `tools/` tree (first run, Option B state) | 6 failed / 5,271 passed / 1 skipped: the 2 pre-existing plus 4 in the PARENT promote's suite, which read the working registry (section 9); re-run on the pinned state: **2 failed / 5,278 passed / 1 skipped**, only the two pre-existing failures remain |

## 7. Beans: reported, not applied

Trevor asked whether the beans' `bacterial-blights` should become `bean-bacterial-blights` in this
promote.

**For.** After Option B the 'bacterial blight' name key has three owners and two are scoped; the
generic that remains names a Phaseolus-specific pathogen pair, so the reuse argument applies to it
as well. The plural is an artifact of a two-disease bundle ("common and halo"), which reads oddly as
a generic.

**Against.** The house convention scopes the ODD pathogen and leaves the MAJORITY on the generic:
`bacterial-spot` on 5 peppers vs `bacterial-spot-pruni`; `anthracnose` on 16 vs `cane-anthracnose`;
`black-rot` on 10 vs `sweet-potato-black-rot`; `aphids` on 64 vs the citrus, apricot and plum
scopings. The beans are the majority holder here, and scoping them would be the first time the
majority moved, with the same logic then demanding `pepper-bacterial-spot`. The reuse argument cuts
the other way for beans: the other legumes that carry "bacterial blight" in the vegetable literature
(lima, snap) share the beans' pathogens, so a future reuse of `bacterial-blights` by a Phaseolus crop
would be CORRECT, unlike cilantro's "bacterial leaf spot", which spans unrelated organisms across
families. And the plural is PLA-448 s4d's bundle: an unbundle into `common-bacterial-blight` and
`halo-blight` retires `bacterial-blights` anyway, so a rename now is churn ahead of the change that
retires it.

**Recommendation: do not rename.** Keep `bacterial-blights` as the registered majority generic (it
is now registered against both scoped ids). If the plural or the bundle bothers anyone, the right
change is the s4d unbundle, not a crop prefix.

## 9. The full tree found the same defect from the other side (2026-09-06)

The parent promote's suite (`test_promote_pla450_451_problem_ids.py`) went red in four places on the
Option B state. Its prediction check read the WORKING registry against replayed historical states,
and the mulberry repoint changed what that registry says about `95e66f6d` and `36d6df6b`. A promote
suite that reads a live registry is a live dependency dressed as a fixture, and this is exactly the
defect the Option B baseline hit in section 5, seen from the other side.

Fix, both promotes, no prediction moved:

| promote | registry for the figures | guard |
|---|---|---|
| PLA-450/451 (parent) | git at `c189d65`, both states | `REGISTRY_COMMIT` pinned; test asserts commit not HEAD; mutation moving it to HEAD caught; 64/64, 43/43 |
| Option B (this) | baseline: git at `074f9e2`; post: staged snapshot `registry_post.json` | write path refuses if the working registry differs from the snapshot; 62/62, 44/44 |

The harness caught a vacuous driver on the way: the first test of the write-path guard asserted it
returned True while the snapshot already matched, so disabling the guard changed nothing and the
mutation SURVIVED. The driver now injects a differing snapshot and asserts the refusal.

## 8. Not verified, by name

PLA-457, PLA-448 s4d, monitor_and_tolerate, PLA-453 naming. Post-commit: register `72371c02` in
`promote_fixture.COMMIT_FOR`; the plant-astro bump belongs to the astro session; plant-app's E1
export is now two revisions behind.
