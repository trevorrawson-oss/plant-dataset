# The PLA-8 coverage floor, armed as A57 -- and the three instruments that broke under it

**Date:** 2026-09-05. **Canonical:** UNCHANGED at `95e66f6d`. This is gate/tooling work; no crop
record was touched, `LATEST.txt` is not bumped, and there is no promote to `release_verify`.

**Closes:** the deferral in `docs/ladder_batch_playbook.md` §7 and row 6a of
`docs/2026-09-04-pla8-batch27-microgreens-arc-close-handoff.md`, and `control_ladder_gate`'s own
stated INV-1 condition. **Closes PLA-8.**

---

## 1. What was armed

`control_ladder_gate.coverage_violations(crop)`, wired into `whole_crop_gate` as **A57**, failing as
`control-ladder-coverage: ...`.

    A57. control-ladder coverage floor (every problem entry is laddered)
      problem entries scanned: 8; unladdered: 0

The deferral it ends was explicit. A56's header said the floor "arms when the rollout actually
lands, which is `control_ladder_gate`'s own stated INV-1 condition," and the playbook said "arm it
when coverage lands, because arming it today takes `gate_all` from 121/121 to 7/121." Coverage
landed on batch 27 at **913 of 913** problem entries.

Measured on `95e66f6d` **before** arming, so the arm is not a bet:

| shape | count |
|---|---|
| problem entries on the roster | 913 |
| `control_ladder` key MISSING | **0** |
| `control_ladder` is `None` | **0** |
| `control_ladder` is `[]` | **0** |
| crops holding zero problem entries | 7 (the shells) |

So A57 arms **green by construction**, which is the gates-arm-off-the-data rule satisfied rather
than dodged: a roster gate armed red floods every unrelated promote, including a parallel session's.
Green is not evidence, though. §4 is.

---

## 2. The unit is the problem ENTRY, not the crop, and that is the whole design

"Every certified crop carries a ladder" is the wrong test and would sit red at 121 of 128 forever.
The seven shells (avocado, olive, and the five mushrooms) carry `pests: []` / `diseases: []` with
`verification_status.status = None`: present and empty by intent, holding **zero entries to ladder**.

Entry-scoped, they pass with **no carve-out**, at any certification status. That matters twice over:

* An earlier draft of handoff row 6a claimed a carve-out "must be explicit ... or the floor takes the
  seven shells down." `ea3f91b` corrected it on the ground that shells are not certified and so sit
  outside `gate_all`'s population. Both reasons are true, and the entry-scoped floor needs neither.
* It **answers the question `ea3f91b` left open** -- what happens if a shell ever certifies while
  still carrying empty arrays -- in the guard's tests, which is exactly where that correction said
  the answer belonged. The answer is: legal. A crop with no problems has nothing unladdered about it.
  `tools/test_control_ladder_gate.py` pins it, including for a shell carrying `verified_gs_arc`.

**Absence only.** `control_ladder: []` is a different defect ("laddered and left blank") and has
belonged to `ladder_violations` / A56 since 2026-08-24, when a batch-2 agent correctly refused to pad
sweet-corn's raccoons ladder and every gate passed the `[]`. A57 stays silent on it, or one defect is
reported twice under two guards. That separation is a **refusal spec** in both harnesses.

---

## 3. The microgreen schema, and why it needed naming

Eight crops (`microgreens-mix` plus the seven batch-27 microgreens) carry `name_beginner` /
`name_seasoned` and **no `name` key** (PLA-452). Instruments have gone blind on this schema
repeatedly, so the floor was built and tested against it explicitly rather than assumed to cover it.
Two instances verified in the record rather than taken on faith:

* The **PLA-449 collision gate**, run with `DISPLAY_NAME_FIELDS` narrowed to `("name",)`, produced
  **0 findings and reported both minted ids BLIND**; with the three-field fallback it produced 2.
  (batch 27 handoff §3, and the same probe in `STATE_HISTORY.md`.)
* **`ladder_batch`'s own load-bearing-field test**, whose fixture was built from the classic schema
  only, so dropping the microgreens half of `PROSE_FIELDS` **survived** its mutation -- the blind
  spot `prose_key`'s docstring already recorded (batch 3, `STATE_HISTORY.md`).

So the floor was checked against the schema on three counts, not assumed to cover it:

* It **reads** them: `whole_crop_gate wheatgrass` prints `problem entries scanned: 2`. A scanned
  count is printed on every crop precisely so a zero is never an unmeasured zero.
* It **names** them: the label helper takes `id` first, then `problem_id_collision_gate`'s
  `DISPLAY_NAME_FIELDS` -- **imported, not retyped**, since that table is PLA-449's own fix for this
  schema. An entry carrying neither `id` nor `name` still reports as
  `wheatgrass/Tray fuzz: problem entry carries no control_ladder`, never `?`. A floor whose output
  an operator cannot act on is not a floor.
* Both are **mutation-tested on `wheatgrass` specifically**, not inferred from apple.

---

## 4. Proof it can fail: `tools/mutate_a57_coverage_floor.py`

**8 injected / 8 caught / 0 survived; 1 refusal spec; roster and commit reach OK.**

Graded through the FULL `whole_crop_gate`, not `control_ladder_gate` standalone: the question is
whether the ARM works, and a defect the standalone gate catches but the arm does not would be
invisible to a standalone run.

| family | mutation | result |
|---|---|---|
| absence | `control_ladder` key deleted (apple) | caught |
| absence | `control_ladder` set to null (apple) | caught |
| schema | key deleted, microgreen schema (wheatgrass) | caught |
| schema | set to null, microgreen schema (wheatgrass) | caught |
| addition | a NEW unladdered problem entry appended | caught |
| addition | a NEW unladdered entry, microgreen schema, **no id** | caught, labelled `wheatgrass/Tray fuzz` |
| shell | a SHELL gains an unladdered problem entry | caught |
| new-crop | a NEW certified crop appended to the roster | caught |

**Three instruments, because "fail a commit" is a claim about all three:**

| instrument | mutation | result |
|---|---|---|
| `whole_crop_gate` | all 8 above | A57 fires |
| `gate_all` | a brand-new certified `ghost-crop` | **FAILS**, naming a crop absent from the base roster |
| `precommit_release_verify --base/--candidate` | a de-laddered `apple` | **BLOCKED** |

Liveness, per the PLA-215 bar:

* **Positive control** -- unmutated canonical PASSES and A57 stays silent.
* **MUTATION-APPLIED marker** -- read off the STAGED tree at the crop the defect is meant to land on,
  so "the injection did nothing" can never be scored as "the guard is blind." The roster-addition
  mutation is graded on `ghost-crop`, not on its donor; grading it on the donor would have reported
  a clean apple and called the guard blind.
* **Sentinel** -- every ladder on the crop nulled MUST redden, or the run exits `HARNESS DEAD`.
* **Refusal spec with its own positive control** -- "the seven shells pass" is worthless alone, being
  equally consistent with the floor never having looked at them. So the shell refusal is paired with
  an injection INTO a shell, which must fire. It does.

Two shapes were chosen deliberately rather than for symmetry. The **key-deleted** case is how a
newly-authored problem entry actually arrives, and a floor written `if p['control_ladder'] is None`
would raise `KeyError` on it instead of flagging it. The **new certified crop** is the shape that beat
four PLA-162 guards at once (a clone of `lime` appended as `ghost-crop` while every guard stayed
green) and is the likeliest real path to an unladdered entry now that the roster is complete: nobody
is going to de-ladder apple, but the next crop to certify arrives with problems authored and ladders
pending.

---

## 5. Three defects the arming turned up, one of them mine

### 5a. `tools/mutate_a56_reachability.py` had been exiting `HARNESS DEAD` since 2026-08-24

Its first run this session:

    HARNESS DEAD: SENTINEL: every rung stripped from every ladder fired A56
                  -- a COVERAGE floor was armed by mistake.

That is the liveness defense working exactly as designed, and nobody re-ran it to see. Two things had
gone stale under it:

1. The sentinel stripped every ladder to `[]` and asserted A56 stays **silent**, because on
   2026-08-22 an empty ladder was indistinguishable from an absent one. On **2026-08-24**
   `ladder_violations` gained the "`[]` is laddered-and-left-blank" check, so the sentinel's own
   injection became a legitimate A56 hit and the harness read its correct catch as a mis-armed
   coverage floor.
2. Its premise, "confirms the coverage floor is NOT armed," went false today.

Repaired rather than deleted: `[]` must now **redden** A56 (the sentinel the convention asks for),
and a `None` ladder must redden A57 and **not** A56 -- the separation that keeps one defect from
being reported twice. The A56 fail prefix (`control-ladder:`) and A57's (`control-ladder-coverage:`)
do not alias, so the two can be told apart in output.

**This is the same class as batch 25's dead harness reporting 34/34, caught by the same instrument
class that caught it.** A harness with a liveness defense fails loudly and then waits; the waiting is
the part that has to be closed by re-running it.

### 5b. The A56 coherence mutation had gone stale, and the repaired harness reported it as a survivor

With the harness alive, `method's applies_to does not fit the problem type` **SURVIVED**. It was not
a gate gap. The mutation put `balance_nitrogen` on apple-scab, which was `insect_soft_bodied` only
when it was picked on 2026-08-22, and by today the catalog had widened it to
`['insect_soft_bodied', 'fungal_foliar', 'fungal_soilborne']`. The injection had become **legal**.

This is the **second** time this one mutation went stale the same way (the first version used
`raise_soil_ph` and survived correctly). A hard-coded method name is a record of what the catalog
looked like once, and the catalog is the gate's own input. It now **derives** its victim at run time
-- any cultural method whose `applies_to` is disjoint from `TYPE_TARGETS['fungal']`, `HARNESS DEAD`
if the catalog offers none -- and prints what it picked (`avoid_ammoniacal_nitrogen ['physiological']`
today). Cultural so tier monotonicity stays intact and coherence is the only family that can trip.

Also tightened while in there: **each mutation now asserts its own guard's message**, not merely
"A56 fired at all." Grading on "the gate went red" lets a mutation be scored as caught by a
*different* family than the one it aims at, which is the green-because-an-earlier-check-fires shape.

**Result after repair: 10 injected / 10 caught / 0 survived**, each on its own guard's wording.

### 5c. The floor in `all_violations` reddened 29 pinned promote suites. Caught by the full-tree run.

**This one was mine, it was live for about an hour, and only the 45-minute regression found it.**

The first cut added `coverage_violations` to `control_ladder_gate.all_violations`, on the reasoning
that a guard whose entry point is never called is a zero with extra steps. `gate_all` stayed 121/121,
the targeted gate tests stayed green, both mutation harnesses passed, and the standalone gate reported
0 on live canonical. **Every check that ran against TODAY'S data agreed it was fine.**

The full tree went from the documented 5 failures to **33**. Twenty-nine of the new ones are one
assertion repeated across every PLA-8 promote suite:

    GateContract::test_control_ladder_gate_clean_on_post
    self.assertEqual(CLG.all_violations(_post()), [])
    AssertionError: First list contains 190 additional elements.

Those suites replay a **historical** post-state and assert the promote left the ladder machinery
sound. Batch 20's post-state has 190 unladdered problem entries **because that is what a rollout in
progress looks like** -- 88 of 121 crops laddered at that moment. Widening `all_violations` made 29
suites assert something false about their own moment.

**The rule this broke is the one A57 itself was careful about, applied to a surface I did not think
of as data.** "Don't arm a gate on data it reddens" was checked against live canonical, where the
answer was 913 of 913. A pinned fixture is data too, and there were 29 of them holding states where
the floor is correctly violated.

**Fix:** `all_violations` stays **integrity-only**, its established meaning. The floor polices the
SHIPPING roster and is reached from the two places that do that -- `whole_crop_gate` A57 (per crop,
enforced roster-wide by `gate_all`) and `control_ladder_gate.main()`, which now prints it as its own
`COVERAGE FLOOR:` section and counts it toward the exit status:

    control_ladder_gate: 0 integrity violation(s), 0 unladdered problem entries

The trap is written into `all_violations`' docstring and pinned by a test, because the next reader to
notice the floor is missing from the aggregate will otherwise "finish the job" and redden 29 suites
again. That is the same shape as every stale record in this repo: the obvious-looking fix is the
defect.

---

## 6. `test_ladder_batch`: the arc's own tooling, repaired rather than skipped

Handoff row 6a-bis item 5 (1 failure + 6 errors, cause: "the arc is complete") is closed. Both were
`todo` emptying:

* `test_there_are_unladdered_crops_left_to_measure` asserted `len(todo) > 0`.
* `BriefCarriesTheWholeMeaning.setUpClass` did `next(c for c in ... if not lb.laddered(c))` and raised
  `StopIteration`, taking all six of its tests down as ERRORS.

**The failure** is retired and inverted, on the instruction the class's own docstring already left
behind when its predecessor's denominator emptied on batch 5: assert the fact the emptying created.
It now asserts the roster is fully laddered **and cross-walks that against A57**, because `laddered`
is the weaker predicate -- ANY problem carrying the key marks the whole crop done, so a crop with 3
of 5 entries laddered reads as laddered there while carrying 2 coverage violations. That gap is what
the floor exists to close, and asserting both together is what pins it shut.

`test_no_true_twin_group_remains_on_the_roster` is now **dormant, not dead**, and re-arms itself the
moment an unladdered certified crop exists again. Recorded rather than hidden. Measured for the
record: repointed at all 121 certified crops instead of `todo`, `family_cut` finds **three** twin
groups (field-corn/flint-corn/popcorn, yellow-summer-squash/zucchini-courgette,
dry-bean/green-beans-bush) -- the sibling sets the arc deliberately propagated identical prose across.
Repointing would arm the test RED on data that is correct, so it stays pointed at `todo`.

**The six errors** are fixed by building an unladdered scratch target instead of skipping the class.
Skipping was the wrong repair: these tests protect a defect that has recurred twice (`best_use[:150]`
in `cmd_prepare`, `[:104]` in `cmd_verify`) on methods this arc actually confused, and a skipped suite
protects nothing. The brief's content is the CATALOG; the crop is needed only because `cmd_prepare`
rightly ABORTs on an already-laddered target ("re-laddering changes shipped ids"). Note the ladder
keys must be **deleted, not nulled**: `lb.laddered` tests key presence, so a null ladder still reads
as laddered.

`tools/test_ladder_batch.py`: **27 passed**.

---

## 7. Gauntlet

| check | result |
|---|---|
| `tools/test_control_ladder_gate.py` | PASS (coverage-floor block added RED-first) |
| `tools/mutate_a57_coverage_floor.py` | **8/8 caught, 0 survived**, 1 refusal spec, roster+commit reach OK |
| `tools/mutate_a56_reachability.py` | **10/10 caught, 0 survived** (was `HARNESS DEAD`) |
| `tools/control_ladder_gate.py` on live canonical | **0 violations**, 913 of 913 laddered |
| `tools/gate_all.py` | **121/121 PASS** |
| `tools/test_ladder_batch.py` | 27 passed (was 20 passed / 1 failed / 6 errors) |
| canonical SHA | `95e66f6d`, byte-identical to `LATEST.txt` |
| `release_verify` | **not applicable** -- no promote; canonical untouched |
| `python3 -m pytest tools/` (full tree, 43 min) | **4 failed, 5,148 passed, 1 skipped** |

The full tree was **5 failed / 6 errors / 5,141 passed** at the batch-27 close. It is now
**4 failed / 0 errors / 5,148 passed**: the 7 arc-completion items in §6 are repaired, and the 4
that remain are the pre-existing ones in §8, none of them attributable to this work. The
intermediate run that read **33 failed** is §5c.

---

## 8. Owed, and deliberately not done here

* **`test_problem_id_collision_gate.py` (2 failures) is still red**, and was already red before batch
  27: `PINNED_SHA = ce98b0a6` while canonical is `95e66f6d`, two promotes on. Not touched here, and
  re-pinning is the wrong fix. The handoff's own ruling stands: move it onto
  `promote_fixture.pre_state` like the promote suites, rather than pinning live canonical. A PLA-449
  task.
* `test_bare_host_scan::test_self_pathed_population_at_this_canonical` and
  `test_cited_claim_scan::test_MUTATION_...` remain red for the reasons the batch-27 handoff
  established (a stale pinned population; 8 of 28 allium URLs uncached). Unrelated to this work.
* The **PLA-215 24-suite mutation backlog** is untouched and remains opportunistic, per the
  convention's own scope note. Two of its members were repaired here as a side effect.
* `identity_violations` still `continue`s on an unladdered problem. Left as is, now that A57 reports
  that entry exactly once; the comment was updated to say so rather than to keep calling it staging.
