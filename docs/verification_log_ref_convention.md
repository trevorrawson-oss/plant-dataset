# `verification_log_ref` — the convention

**Ruled:** 2026-07-29, hardening item 3
(`docs/2026-07-26-post-asparagus-hardening-kickoff.md` item 3).
**Measured against canonical:** `b0d01f13`.

---

## The ruling

**`verification_log_ref` is an APPEND-ONLY, CERT-DATED HISTORICAL RECORD. It is not a living
summary and must not be maintained as one.**

It records what was established and believed at the certification (or arc) named in its own
opening stamp. A later pass that invalidates something it asserts **appends a dated correction
line**; it never rewrites the original sentence.

So both risks the kickoff doc named are closed:

1. Nobody should "fix" a stale-looking `log_ref` into current tense — that destroys the record of
   a real reasoning error. **The staleness is the point.**
2. Nobody should read one as current truth — because a Class 2 drift (below) carries an appended
   correction line saying so, in the same string.

### Correction line format

Appended at the **end** of the string, never edited into the original sentence:

```
[CORRECTION <YYYY-MM-DD>: <what is no longer true, and what is true now> -- see <finding id or doc>.]
```

Multiple corrections accumulate in date order. The original prose stays byte-for-byte intact.

---

## Which drift needs a correction line, and which does not

The distinction is the operative part of this ruling. The test:

> **Would a reader who took this sentence as current truth be materially misled about this crop?**

### Class 1 — context growth. No action.

The claim was true on its date and is now merely smaller than the world. The date stamp is
already the correction.

Canonical example: eight crops' log_refs say things like `"10/10 regions"` or
`"Region fill complete across all 10 regions / 20 cells"`. The roster carried 10 regions then and
carries **16** now. Those sentences are accurate statements about their own arc. A reader
concludes only that the roster was smaller at cert, which is true.

Affected (measured, no action needed — all 7): `zucchini-courgette`, `broccoli`, `garlic`, `onion`,
`strawberry`, `lavender`, `zinnia`. Expect the same on the region/cell counts of any crop certified
before the Tier-2 region belt landed.

### Class 2 — retired reasoning, or revalued vocabulary. Correction line REQUIRED.

The claim asserts a mechanism later found unsourced, or a value distribution whose vocabulary has
since changed. A reader taking it as current truth repeats a known error or misreads the crop.

Two instances existed at ruling time; both were corrected as part of this item (below).

---

## Why append-only, and not a living summary

The kickoff doc recommended append-only to preserve the audit trail. That argument turns out to be
**weaker than it looks**, and the ruling lands on append-only for a different, stronger reason.

**The weak argument:** "rewriting erases the audit trail." It mostly would not. `open_findings`
and `STATE_HISTORY.md` already carry the append-only trail, dated and status-tracked. The retired
asparagus chill mechanism is recorded in *three* separate findings
(`asparagus_suitability_chill_mechanism_unsourced_arc2`,
`asparagus_chill_claim_provenance_plantvillage`,
`asparagus_low_desert_az_rerated_from_retired_chill_mechanism`). The trail does not depend on this
field.

**The strong argument: a living summary is unenforceable at this scale and drifts silently.**
Measured roster-wide, **13 of the 115 prose `log_ref`s already assert a count that no longer
matches the data** — and 7 of those drifted for no reason other than the roster growing from 10
regions to 16. Under a living-summary rule, every future region addition would require
re-auditing 115 prose narratives, and every missed one becomes a silent falsehood. That is exactly
the backfill treadmill `CLAUDE.md` forbids. Asparagus proves the drift rate: its split went stale
**within three days** of cert.

Append-only inverts that. Under it, all 7 Class 1 cases are *correct as written* and need no
maintenance at all, and the only obligation is a one-line append at the moment a pass knowingly
retires something — which is when the author has the context to write it.

**Supporting fact — the field is invisible to consumers, so a historical record costs nothing.**
No `plant-astro` source file reads `verification_log_ref` (verified by grep over `src/`). Both
`tools/field_classification.py` and `tools/register_completeness_gate.py` already classify it
BACKEND, exempting it from the dash/temperature/consumer-prose gates. It is a backend audit
artifact and this ruling makes it honestly that.

---

## Why there is NO gate for this

**A count-assertion gate was built, measured, and deliberately NOT shipped.** The scanner is kept
at `tools/logref_count_scan.py` as a diagnostic, not wired into the suite.

Of its 14 rows (13 count mismatches + 1 shape outlier):

| verdict | count | which |
|---|---|---|
| **Class 1, correct as written** | 7 | the 10-region-era statements above |
| **regex noise on legitimate prose** | 4 | `pear-european` / `pear-asian` `"better with two varieties"` (pollination advice, not a varieties-array count); `swiss-chard` `"(6 cells)"` (a deliberate subset count); `tomatillo` `"2 varieties ideal"` |
| **genuine Class 2** | 2 | `asparagus`, `artichoke` |
| **shape outlier, informational** | 1 | `lettuce-leaf` (ruled below) |

A gate at that signal-to-noise cries wolf, and a noisy gate gets ignored — which is worse than
none. This is the documented `a25-tightening-floods` /
`growth-stages-shape-not-gated` failure pattern, and the
`gate-findings-must-be-read-not-counted` lesson: the findings had to be **read**, and exactly 2 of
13 were defects.

One earlier false positive is worth recording because it shows how thin the margin is: a looser
first draft of the `fruits_reliably` pattern also flagged `peach` and `strawberry`, matching
`"the documented z3-11 fruiting"` as a claim of *11 fruits_reliably cells*. Tightening the regex
removed both. That is the whole yield available from tightening — it never reaches the 7 Class 1
cases, because those are not pattern errors.

Tightening the check cannot rescue it either, because the dominant category is *correct historical
prose*, and no regex distinguishes "this count is stale because the roster grew" from "this count
is stale because the value was retired." That distinction is a judgment about causes, which is
what the two-class rule above is for.

---

## Two other shapes found, and ruled

**`lettuce-leaf` carries a LIST, not a string:**
`['phase_3_lettuce_m13_arc', 'phase_3_lettuce_m13_s1b_na_findings.md', ...]` — filenames. This is
the field name's *original* meaning: a **ref** to log files. The prose-narrative form used by the
other 115 crops is later drift that kept the name.

**Ruled: leave it. Do not gate the shape, and do not normalize it.** The `weeks_indoors`
mixed-shape break (canonical `6da153b9` -> `b0d01f13`) is *not* precedent here: that field was
typed and read by `plant-astro`'s schema, so a shape mismatch broke the site build. This field is
read by no consumer at all, so a mixed shape has no failure mode to prevent. Normalizing it would
destroy the only surviving pointer to those four log files.

**Five CERTIFIED crops carry no `verification_log_ref` at all:** `sweet-corn`, `dry-bean`,
`field-corn`, `popcorn`, `flint-corn`. (The other 7 absences are the uncertified shells — avocado,
olive, and the 5 mushrooms — which is correct.)

**Ruled: presence is NOT a cert requirement and will not be gated.** All five certified without
it, so cert demonstrably does not depend on it, and backfilling a historical narrative for an arc
that has already closed would mean *writing* history rather than recording it — the
`fill-the-shape-is-the-defect` hazard, where a field's shape pulls a fabricated value out of you.
Authoring a narrative today about what was believed months ago is precisely that. Going forward,
the prose-narrative form is the convention for new certs.

---

## Applied 2026-07-29 — the two Class 2 corrections

### asparagus

Two assertions were stale, one of them a retired *mechanism*:

1. **The suitability split.** Claimed `"an honest 16-region, 39-cell map: 18 cells perennialize, 8
   are marginal, and 13 are unsuitable"`. Actual: **25 / 4 / 10**. Not roster growth — these cells
   were **re-rated** in timing arc 2 because their original ratings rested on reasoning that was
   retracted.
2. **The mechanism itself.** Claimed every marginal and unsuitable call rests on a dormancy
   requirement such that `"frost-poor maritime and low-chill zones blunt the dormant rest
   (marginal), and frost-free subtropical or extreme-heat desert zones deny it entirely
   (unsuitable)"`. The **chill** framing is the retired claim, traced to PlantVillage (an
   aggregated crop-profile database, not an extension bulletin) and contradicted by UC IPM, which
   states dormancy comes from cold **or drought**. The "extreme-heat desert zones deny it
   entirely" clause is now false outright: `low_desert_az` z9/z10 were re-rated
   `unsuitable` -> `perennializes`.

This is the single most dangerous string in the dataset to read as current truth, because it is
the *original source* of the reasoning error, stated confidently, inside the field a future
session would consult to understand the crop.

### artichoke

Claimed `"SUITABILITY, 16 regions / 39 cells: 6 perennialize, 25 marginal, 7 survives_no_fruit, 1
unsuitable"`. The `6 / 7 / 1` are still exact; the **25 marginal is not**. After `annual_only`
shipped as a sixth suitability value (commit `3258e4c`, frontend-first), that group split into
**22 `annual_only` + 3 `marginal`**.

Vocabulary revaluation, not an error — but Class 2, because nothing in the string tells a reader
the sixth value exists, and 22 of 39 cells now carry a value the sentence does not mention.
