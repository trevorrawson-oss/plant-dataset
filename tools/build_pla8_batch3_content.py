#!/usr/bin/env python3
"""PLA-8 batch 3: the ONE rung fix the READ found, applied to the staged ladders before promotion.

THE STAGED CONTENT IS NOT EDITED IN PLACE. `tools/staging/pla8_ladder_batch3/out_*.json` stays
exactly as the three authoring agents produced it; this module is the DELTA applied on top. That
keeps the authored content reviewable against what the bots actually wrote, and keeps the record
honest about which decisions were the read's rather than the authors'.

WHAT THE READ FOUND. Zero method-meaning mismatches across 136 authored rungs (batch 1: 22 of 165;
batch 2: 0 of 88). Five loose fits were flagged by the agents and ALL FIVE resolved to ACCEPT on
shipped precedent, so none of them appears here. One real defect, below.

THE FIX: cucumber was missing the `resistant_varieties` rung its own prose earns on Cucumber
beetles. cucumber and slicing-cucumber carry BYTE-IDENTICAL `prevention_seasoned` on that problem
("choose non-bitter varieties that attract fewer beetles"), but slicing's agent keyed it and
cucumber's refused, reading the catalog's `best_use` ("Chosen at seed-buying time for diseases that
recur in your beds") as disease-only.

Shipped precedent settles it against the refusal. `resistant_varieties` is `applies_to: ["any"]` and
ALREADY carries varietal NON-PREFERENCE traits on insect problems:
  * `jalapeno/pepper-maggot`  -- "goes for thick-walled bell types, and slender hot peppers are
    seldom bothered". Nearly the identical construction to the cucumber case.
  * `sweet-corn/corn-earworm` and the other three corns -- husk cover, a physical trait.
  * `fig/dried-fruit-beetle-souring` -- "a fig with a small, tight eye, such as Celeste".
  * `apple/woolly-apple-aphid` -- resistant rootstock.
That is 8 shipped insect uses across 6 crops. The catalog's `best_use` is NARROWER than the
method's own shipped usage, which is a measured, systematic defect: 11 of 49 shipped methods have
this property (see tools/staging/pla8_ladder_batch3/README.md). It is why four of this batch's five
false flags happened, and it is a deferred catalog-prose arc, NOT a reason to refuse a correct rung.

NOT APPLIED, DELIBERATELY. Each of these looks like an inconsistency and is not one; they are
recorded so a later pass does not "finish the job" without re-arguing it.

  1. `resistant_varieties` on BACTERIAL WILT for cucumber and slicing-cucumber. pickling-cucumber
     carries it; the other two do not, and that divergence is CORRECT. pickling's prose claims
     genuine wilt TOLERANCE ("wilt-tolerant varieties such as County Fair"). cucumber's and
     slicing's claim only that less-bitter varieties attract fewer BEETLES, which is a claim about
     the VECTOR. Keying that to `resistant_varieties` on a bacterial problem would read as wilt
     resistance neither crop asserts. This is the known structural limit -- a vector-borne disease
     cannot carry a rung aimed at its vector, and there is no disease->vector cross-reference --
     first hit on Stewart's wilt in batch 2.

  2. The "do not work among wet vines" fold. Identical sourced prose in all three crops landed on
     `garden_sanitation` for cucumber and on `water_at_the_base` for the other two. Both are
     defensible and each restates its own crop's prose: cucumber frames it as a timing constraint on
     going into the patch to remove leaves; the others group the two foliage-moisture spread routes.
     Left divergent ON PURPOSE. These crops are NOT twins, the rungs themselves are correct, and the
     real cause is that no catalog method covers handling discipline. The fix is a method, not a
     note edit, and rewriting accurate notes for cosmetic uniformity risks new defects.

Used by: tools/promote_pla8_batch3.py
"""

# ---------------------------------------------------------------------------------------------
# INSERT: add a rung the read found missing. `index` is where it lands in the ladder; `expect_after`
# is the full method sequence the ladder MUST have once inserted. Both are validated against the
# staged file and any mismatch is a REFUSAL, never a silent re-index -- the staged file could be
# re-authored, and an insert at a stale index would attach a rung to the wrong problem.
# ---------------------------------------------------------------------------------------------
INSERTS = [
    {
        "crop": "cucumber", "fam": "pests", "pid": "cucumber-beetles", "index": 0,
        "expect_before": ["crop_rotation", "garden_sanitation", "floating_row_cover",
                          "handpick", "yellow_sticky_traps"],
        "expect_after": ["resistant_varieties", "crop_rotation", "garden_sanitation",
                         "floating_row_cover", "handpick", "yellow_sticky_traps"],
        "rung": {
            "method": "resistant_varieties",
            "note_beginner":
                "Bitter-fruited plants draw more beetles, so pick a variety described as non-bitter "
                "when you order seed. This one is settled before anything goes in the ground.",
            "note_seasoned":
                "Non-bitter cultivars attract fewer beetles, which lowers the early-season "
                "colonizing pressure that carries the wilt. A seed-order decision, and it does not "
                "replace exclusion at the seedling stage.",
        },
    },
]

# Problems the read examined and deliberately left alone; see the docstring for the reasoning.
NOT_APPLIED = (
    "cucumber/bacterial-wilt + slicing-cucumber/bacterial-wilt: no resistant_varieties rung "
    "(vector claim, not a resistance claim; the Stewart's wilt structural limit)",
    "all three / 'do not work among wet vines': folded into different rungs by crop, on purpose "
    "(no handling-discipline method exists; both folds restate their own crop's prose)",
)


def apply_read_fixes(batch):
    """Apply the delta to an already-loaded staged batch, in place. Returns the number applied.

    Raises on ANY mismatch. A read-fix that cannot find the ladder it was written against is a
    refusal, because the alternative is silently editing a different rung.
    """
    applied = 0
    for ins in INSERTS:
        crop = batch.get(ins["crop"])
        if crop is None:
            raise AssertionError(f"read-fix: no staged crop {ins['crop']!r}")
        hits = [p for p in crop.get(ins["fam"], []) if p.get("id") == ins["pid"]]
        if len(hits) != 1:
            raise AssertionError(
                f"read-fix {ins['crop']}/{ins['pid']}: matched {len(hits)} problems, expected 1")
        lad = hits[0].get("control_ladder")
        if lad is None:
            raise AssertionError(f"read-fix {ins['crop']}/{ins['pid']}: no control_ladder")
        before = [r["method"] for r in lad]
        if before != ins["expect_before"]:
            raise AssertionError(
                f"read-fix {ins['crop']}/{ins['pid']}: staged ladder is {before}, "
                f"expected {ins['expect_before']}; the staged content changed under this fix")
        if any(r["method"] == ins["rung"]["method"] for r in lad):
            raise AssertionError(
                f"read-fix {ins['crop']}/{ins['pid']}: {ins['rung']['method']!r} already present")
        lad.insert(ins["index"], dict(ins["rung"]))
        after = [r["method"] for r in lad]
        if after != ins["expect_after"]:
            raise AssertionError(
                f"read-fix {ins['crop']}/{ins['pid']}: got {after}, expected {ins['expect_after']}")
        applied += 1
    if applied != len(INSERTS):
        raise AssertionError(f"applied {applied} of {len(INSERTS)} read-fixes")
    return applied


if __name__ == "__main__":
    import json, os, sys
    STAGING = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "tools", "staging", "pla8_ladder_batch3")
    b = {s: json.load(open(os.path.join(STAGING, f"out_{s}.json")))
         for s in ("cucumber", "pickling-cucumber", "slicing-cucumber")}
    n = apply_read_fixes(b)
    total = sum(len(p["control_ladder"]) for c in b.values()
                for fam in ("pests", "diseases") for p in c[fam])
    print(f"read-fixes applied: {n}")
    print(f"rungs after delta : {total}")
    print(f"not applied       : {len(NOT_APPLIED)} (see NOT_APPLIED)")
