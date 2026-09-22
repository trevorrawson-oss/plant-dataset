# PLA-533: the container-citation ratchet, ARMED at 4

**Date:** 2026-09-22. **Canonical `526788f2`, UNTOUCHED** -- this arc changes no data.
**Commit:** `b9d28d5`, `tools/container_citation_floor_gate.py` + suite + harness, wired into
`gate_all`. **Approved as executed** by Trevor, 2026-09-22.

> **THE RULE (Trevor's ruling 1).** The count of CERTIFIED crops carrying a non-null
> `container_notes.min_pot_gallons` with no `sources` or no anchoring URL may go **DOWN, never UP**.
> Armed at **4**, where it is GREEN. It does not wait for those four to be re-sourced; it arms now
> so the population cannot grow while the audit runs.

The four: `dry-bean` 5, `green-beans-bush` 5, `grapefruit` 20, `orange-navel` 15.

---

## 1. Why this is a new gate and not a fix to section F

§F asks **"did you anchor what you CITED?"** Its walk fires only on a **non-empty** `sources` list,
so emptying `sources` makes it **quieter**, not louder. Measured on a scratch copy of `cabbage`,
running the real gate:

| injection | result |
|---|---|
| as shipped | 147 claim-bearing leaves, 0 gaps, PASS |
| `anchoring_urls` emptied, `sources` KEPT | 147 leaves, **1 gap, FAILS** |
| `sources` emptied too | **146 leaves**, 0 gaps, **PASSES** |

**The leaf count drops.** Deleting the citation deletes the check. Trevor's formulation, which is
the principle worth carrying past this arc: **a gate that gets greener as you cite less is worse
than no gate.**

This gate asks the other question -- **"should this number have been cited?"** -- which is a
coverage floor in the A57 / A59 pattern, not a consistency check. The two are different gates and
had to be built as two.

## 2. Why roster-level rather than a `whole_crop_gate` A-number

**A ratchet is a property of a COUNT, and a per-crop gate cannot see a count.** It runs in
`gate_all`, after the per-crop loop. A per-crop version would also have to be RED on the four
today, which is precisely what the ruling rejected: armed green, it stops the growth *now* instead
of after the audit finishes.

---

## 3. THE SUBSTITUTION STRENGTHENING, as reasoning

**A count-only ratchet is defeatable, and the defeat is cheap.** Close one crop, break another:
the count is still 4, and a check that only compares `len(live)` to a ceiling **passes**. The
population has not grown, so the ratchet is satisfied -- while a crop that was cited yesterday is
uncited today and a crop that was uncited yesterday is the one that got fixed. The number holds
and the state is worse.

That is the same failure shape as the one this gate exists to close. §F was green because it was
measuring the wrong thing; a count-only ratchet would be green because it was measuring a
quantity when the thing that matters is an **identity**.

**So the violation is not "the count grew". It is "an uncited crop that is not one of the KNOWN
four".** That formulation:

- **catches growth** -- a fifth crop is necessarily outside `KNOWN`;
- **catches substitution** -- the newly broken crop is outside `KNOWN` even though the count held;
- **permits shrinkage automatically** -- closing a crop removes it from `live`, and a subset of
  `KNOWN` never violates, so the gate passes at the lower count **with no pin edit at all**;
- **preserves Trevor's ruled direction exactly.** Down yes, up no. Nothing about the ruling is
  widened; what changes is that "up" is now measured by identity rather than by arithmetic, and
  arithmetic was the part that could be gamed.

Driven through `gate_all`, the real release entry point, on scratch states: **substitute (close
`dry-bean`, break `cabbage`, count stays 4) FAILS.** A count-only version passes that case, which
is the whole argument in one line.

## 4. THE UNREACHABLE-BRANCH CHECK, as reasoning

The gate also carries `if len(live) > CEILING`. Before shipping it, the question was whether that
branch can ever fire -- because **an unreachable guard is worse than no guard, since it reads as
coverage.**

**Measured: it is unreachable by growth alone.** `len(KNOWN) == CEILING == 4`, so any fifth uncited
crop is necessarily outside `KNOWN`, and the set check above answers first. Growth can never reach
the count branch.

It is reachable on **exactly one path**: a `KNOWN` / `CEILING` **desync** -- five entries in
`KNOWN` with `CEILING` still 4. That is not a hypothetical. It is the editor error this gate's own
instructions invite, because closing a crop says *"remove it from `KNOWN` and drop `CEILING` by
one"*, and the inverse operation (adding a recorded exception) says *"add it to `KNOWN` and raise
`CEILING`"*. Either instruction can be half-followed.

**So the branch is kept, and given its own driver** -- a test that desyncs the two pins and asserts
the count message fires -- plus a third test pinning `len(KNOWN) == CEILING` as the invariant that
makes that the only path. The branch is now exercised rather than decorative, and the reason it
survives review is written down here rather than left for a future reader to re-derive.

**The precedent this follows:** PLA-580's promote carried a duplicate-crop guard from the PLA-465
pattern. Measured, it was unreachable behind an earlier set comparison -- its driver reddened on
the *other* guard's message -- and it was **removed rather than shipped**. Same test applied here,
opposite outcome, because this branch turned out to have a real path. The test is what matters, not
which way it comes out.

---

## 5. Proof

**TDD:** the suite was written and run RED before the module existed. **20 tests.**
**Mutation-tested (PLA-215):** 10 injected, **10 caught, 0 survived, 0 broken**; anchor preflight
10/10; **positive control the WHOLE suite**; sentinel reddened.

Trevor's two named proofs are drivers by name -- `test_PROOF_adding_a_fifth_FAILS` and
`test_PROOF_closing_one_PASSES_at_the_lower_count` -- and the ratchet was additionally driven
through `gate_all` itself:

| case | rc | |
|---|---|---|
| as shipped, 4 uncited | 0 | PASSES |
| add a fifth (`cabbage` uncited) | 1 | **FAILS** |
| close one (`dry-bean` cited) | 0 | PASSES **at 3**, no pin edit |
| close all four | 0 | PASSES at 0 |
| substitute, count stays 4 | 1 | **FAILS** |
| `plum` gains a pot size with no citation | 1 | **FAILS** |

The last row matters as much as the first: the floor is live for **new authoring**, not only for
today's four.

## 6. Closing one

Remove the crop from `KNOWN` and drop `CEILING` by one, **in the same commit as the data change**.
The gate passes at the lower count *without* that edit -- shrinkage is never a violation -- so the
edit is not what makes the release green. It is what stops the crop being silently re-broken later.

## 7. Scope, deliberately narrow

Only `min_pot_gallons`, only on CERTIFIED crops, only when non-null. **A crop that states no pot
size makes no claim to cite:** 8 certified crops carry an empty `container_notes.sources` with
all-null numerics and are legitimately silent. Widening this to every `container_notes` numeric, or
to §F's general skip, is separate work -- and under Trevor's ruling 3 **no §F fix is to be proposed
until the `harvest_ready_sources` slice is measured**, because whether an empty `sources` matters
depends on whether the block carries a claim, and that is judgment §F cannot make.

## 8. Carried forward

**Figure size and anchor quality are independent axes, and the risk queue is ranked on one of
them** (Trevor, 2026-09-22). `cherry-sour` and `cherry-sweet` carry the largest figures in the
whole population at **25 gallons** while sitting in the MEDIUM bucket, because their anchors are
general crop pages rather than cultivar-description pages. A 25-gallon claim on a weak anchor is a
bigger error than a 1-gallon claim on a weak anchor, and the ranking does not see that. Whoever
works the queue should read the large figures early regardless of bucket.
