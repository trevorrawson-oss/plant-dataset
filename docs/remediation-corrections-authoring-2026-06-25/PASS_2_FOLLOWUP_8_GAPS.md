# Pass 2 Follow-up -- the 8 fields still missing (targeted re-author)

**Date:** 2026-06-26
**From:** Claude Code (structural-write lane) -> claude.ai (author lane)
**Base SHA:** `144b2fb2` (unchanged -- canonical NOT yet mutated; Pass 2 is held for one clean apply)

The Pass 2 companions bundle was reconciled against canonical: **67 of 82 authored entries fill
their gap cleanly and are ready to apply.** The lavender double-malformed `good_seasoned` provenance
and the pigeon-pea bucket move are also ready. **8 fields are still short** -- they need authoring
before the apply, because the rendered/gated companion gates (`companion_why_fill_violations`,
`companion_evidence_violations`) won't reach 0 without them. This is a small targeted pass; reuse your
own Pass 2 reasoning (cited below), don't re-derive.

## Two rules to apply (one caused 3 of the 8 gaps)
1. **Register rule.** A `*_beginner_seasoned` bucket renders in BOTH modes, so it needs BOTH
   `why_seasoned` AND `why_beginner`. The orange-navel entries below got `why_seasoned` (canonical
   already had it); the gap is the **`why_beginner`** side.
2. **Evidence field = `provenance`.** The rendered/gated evidence field is the nested
   `provenance` object: `{label, confidence, reason, verified_against_sources}` (a BOOL).
   Flat `evidence_label`/`confidence` keys are legacy and not gated -- author into `provenance`.

## The 8 gaps

### basil -- 2x missing `provenance` (good_beginner_seasoned)
You set `evidence_label: research_backed`, `confidence: medium` (flat) but emitted no `provenance`
object. Build the provenance (keep those values) -- only the `reason` prose is missing. `why_seasoned`
(canonical) and `why_beginner` (your fragment) are both fine; provenance is the only gap.
- **Marigolds** -> `provenance: {label: "research_backed", confidence: "medium", reason: <the marigold/basil evidence you verified>, verified_against_sources: true}`
- **Tomatoes** -> `provenance: {label: "research_backed", confidence: "medium", reason: <the basil-reduces-thrips/whitefly research you cited>, verified_against_sources: true}`

### carrot -- 3x missing `why_seasoned` (bad_beginner_seasoned)
You authored `provenance` (with a full `reason`) for these but not the consumer-facing
`why_seasoned`. Author `why_seasoned` (seasoned register, "why keep apart") from your own reason:
- **Dill** -> reason you wrote: Apiaceae shared pests (carrot rust fly) + cross-pollination for seed-savers; growth-inhibition is folk-level.
- **Parsnips** -> Apiaceae shared pest/disease + two long-season roots competing for P and space.
- **Fennel** -> near-universal allelopathy folk rule (anethole/fenchone suppress germination in bioassays, targeted at weeds not carrot) + Apiaceae overlap. (Mirror your beefsteak Fennel voice.)

### orange-navel -- 3x missing `why_beginner` (NOT why_seasoned)
These render in beginner mode too; canonical already has `why_seasoned` (shown below as the basis).
Author a beginner-register `why_beginner` for each (provenance from your fragment is fine):
- **Comfrey** (good_beginner_seasoned) -- basis: "Deep roots pull up nutrients, and the leaves can be cut and dropped as a mulch that feeds the tree. Plant it outside the trunk flare..."
- **Yarrow** (good_beginner_seasoned) -- basis: "A low, shallow-rooted plant that draws beneficial insects and does not compete with the citrus roots when kept outside the dripline."
- **St. Augustine grass** (bad_beginner_seasoned) -- basis: "A dense, spreading lawn grass that competes aggressively for water and nutrients in the top soil and creeps right up to the trunk. Keep it cleared out..."

## Two fixes for next time (no action needed now, just FYI)
- `orange_navel_pass2.json` shipped with a **JSON syntax error** (missing comma after the pigeon-pea
  `why_seasoned` string, before `"provenance"`). I patched it locally; re-validate JSON before export.
- The canonical gap map listed only lavender's 6 null `provenance.label`s; those 6 entries ALSO have a
  corrupt `confidence` (it holds a label value like "likely"). Your fragment's label+confidence fix
  both, so no extra work -- noting it because the gap map undercounted by 6.

## Delivery + what happens next
Deliver the 8 as a small fragment (same shape: `{bucket, name, provenance, why_*}`), or amend the
3 affected per-crop fragments. On receipt I apply the COMPLETE Pass 2 set in one shot, confirm
`companion_why_fill_violations` -> 0 and `companion_evidence_violations` -> 0, keep `whole_crop_gate`
18/18, wire the two gates, bump the plant-astro submodule, and update the state trio at the commit.
No em dashes in the consumer `why` prose.
