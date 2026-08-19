# A new promote or gate suite ships mutation-tested -- the convention

**Adopted:** 2026-08-19, PLA-215 (convention half).
**Filed out of:** PLA-162's close; measurement from PLA-138's instrument audit.
**Scope:** the CONVENTION only. The 24-suite backlog stays opportunistic and is not a
condition of this being adopted.

---

## The rule

**A new promote or gate suite ships mutation-tested, or it does not ship.**

Not "should be." A suite that has never had a defect sneaked at it has not been shown to
test anything, and it is entered into the release gauntlet as though it had.

## Why this is a convention and not a backlog item

PLA-138 counted **37 pinned suites, 3 ever mutation-tested**. PLA-162 verified or partly
verified ~20 more -- and in that same week the roster grew from 37 to ~44, because
PLA-155, PLA-156, PLA-157 and PLA-199 each shipped a promote suite. **24 remain never
tested.**

Chasing the 24 today means chasing 30 next month. Unless creation is gated, the audited
fraction falls every time work gets done, and it falls fastest during productive weeks.
The convention is the fix; the backlog is the leftover.

## Why an unverified guard is worse than no guard

It reads as coverage.

- PLA-114's promote found two guards passing on substrings that occurred elsewhere in the
  fixture: `'202'` was matching the accessed date `2026-08`.
- PLA-162 found four guards that stayed green while **a clone of `lime` was appended to the
  roster as `ghost-crop`** -- and one, `test_residue_hunts_contribute_citrus_only`, that
  asserted a condition its own `collect()` had enforced two lines earlier and **could never
  fail**.
- Three of those sat inside suites written the same day, by the same process, as suites
  that did it correctly. Care at authoring time is not the variable that separates them.

**A guard that cannot fail is a zero with extra steps.**

---

## The minimum bar, per suite

### 1. At least one mutation per guard family
Inject the defect the guard exists to catch, into a **scratch copy**, and verify it goes
RED. One mutation per family the suite claims to cover, not one per suite.

### 2. A liveness defense -- not optional
The harness must prove it actually ran the mutated code: a MUTATION-APPLIED marker plus a
sentinel that MUST redden, or the run exits `HARNESS DEAD`.

PLA-138's original run reported false vacuity because its harness **dedented an
already-indented template and silently ran the clean fixture**. Every mutation "survived,"
and the conclusion drawn from that was wrong. A harness that cannot detect its own failure
to mutate produces confident garbage in whichever direction.

### 3. A positive control wherever the injection could plausibly be invisible
PLA-162's own first injection WAS invisible -- `sources[]` counts toward a node's citations,
so the planted bare node was never SOLE and no guard should have fired. Only the control
distinguished "the guard is blind" from "the injection was a no-op."

### 4. Key-set equality asserted BEFORE value comparison, in any two-state guard
```python
assert set(pre) == set(post)     # FIRST
# ...then compare values
```
Iterating the pre state makes **everything added in post invisible**. That one shape
accounted for all four PLA-162 defects and turned up in 13 suites on the repo-wide grep.

### 5. Green is a legitimate result when green is the contract
A guard whose job is to REFUSE an input stays green when it refuses. Record that as
**REFUSAL-SPEC**, not as vacuous. PLA-162's harness misclassified this before it was
corrected, and the misclassification manufactures phantom work.

---

## What counts as meeting the bar

An **instrumented, reproducible mutation run with a liveness defense** -- a script that can
be re-run, that names each mutation and where it was injected, and that reports survivors
explicitly. Record the result where the work is recorded (the Linear close-out, and the
session's `docs/` outcome note if it has one).

**Treat birth-time mutation narratives as unverified until rerun under such a harness.**
Several census members carry claims like "guards 15, all mutation-tested" (PLA-122) or
"gate mutations 7/7, artifact sabotages 8/8" (PLA-199), yet PLA-138's diagnostic counted
only the PLA-114 trio as ever tested. The gap between a claimed sabotage pass and an
instrumented one is exactly what the dedent bug demonstrated.

**A written list of what was NOT verified is a legitimate close** (PLA-138's stopping rule).
Silent partial coverage is not.

---

## Not in scope

- **The 24-suite backlog.** Opportunistic, newest first -- recent suites guard recent
  promotes and are likeliest to run again. **24-to-zero is explicitly NOT the definition of
  done.** Census and work order live in PLA-215.
- **The ~30 identical one-directional sites in historical promote SCRIPTS.** PLA-162 left
  them deliberately: they are pinned by `--expect-sha`, can never run against new input, and
  several are replayed byte-exact by `CHAIN`. Editing them risks fixture replay for zero live
  value. **That reasoning stands -- do not revisit it.**
- **CHAIN-replayed fixtures** (3 backlog members) are in scope for the bar but need their
  mutations injected into the **replayed scratch copy, never the script**, or the replay
  itself breaks.

---

## Related

- `docs/release_runbook_v1_0.md` §5 -- the promote ceremony this bar attaches to.
- `tools/promote_fixture.py` -- why pinned suites go vacuous, and the `COMMIT_FOR` /
  `CHAIN` reconstruction that keeps them live. **Never amend a commit `COMMIT_FOR` pins**;
  breakage shows up as guards SKIPPING while reporting green.
- CLAUDE.md, Hard rules -- the binding one-line statement of this convention.
