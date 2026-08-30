# `release_verify` section E false-flags 33 crops, and the defect is in the REFERENCE

Measured 2026-08-28 against canonical `96cbc68c`, by two sessions independently. **Nothing was
changed.** This is a filed finding for whoever picks up release_verify hardening.

---

## The symptom

```
$ python3 tools/release_verify.py <candidate> --base <base> --slug garlic
  CONCERN: rgv: novel region keys vs lettuce-leaf: ['plantings_provenance']
RELEASE-VERIFY: 1 CONCERN(S) -- block + review before promoting
```

It looks like the candidate introduced a novel key. It did not.

## It reproduces with NO promote involved

Running release_verify with canonical as **both** candidate and base -- zero changes -- raises the
same concern. It is not caused by any promote, and `--slug dill` is clean.

## What it actually is

Section E compares a crop's region cell against the reference crop `lettuce-leaf`.
**`lettuce-leaf` carries `plantings_provenance` in 15 of its 16 regions. The one region it lacks is
`rgv`.** garlic's rgv cell is otherwise shape-identical: the key-diff in the other direction is
empty.

So the flag reads "garlic has something novel" when the truth is "the reference has a one-key hole
in one region".

**Blast radius: 33 crops**, and `rgv` is the ONLY region where it can fire -- every crop carrying
`plantings_provenance` in `rgv` false-flags the moment section E runs against it. It reads
crop-specific only because most pilot slugs happen not to be among the 33.

## The hole is real, not a legitimate absence

`lettuce-leaf.regions.rgv` **has `plantings`** -- a real, sourced succession citing the Bilingual
LRGV planting table -- with no provenance recorded for it, while its other 15 regions all record
theirs. The cell is anomalous against its own crop, which is what makes "lettuce-leaf owes the key"
the better fix than "section E is too strict".

## THE FIX IS ONE NULL, NOT A PROVENANCE NARRATIVE

This is the part worth knowing before anyone starts writing prose. `plantings_provenance` is an
almost entirely unruled field. Across its 1,540 region-level occurrences:

| encoding | count | example |
| -- | -- | -- |
| `null` | **790** | cherry-tomato / pnw |
| string | 548 | cherry-tomato / northern_tier |
| object | ~200, in **27+ distinct key sets** | garlic/northern_tier `{basis, model, supersedes}`; thyme/northern_tier `{frost_resolved, method, note}`; cherry-tomato/hawaii_tropical has a 19-key object |

Section E compares key PRESENCE, not content, and the modal value is `null`. So the minimal,
honest fix is:

```
lettuce-leaf.regions.rgv.plantings_provenance = null
```

matching 790 existing cells. Do NOT invent a provenance narrative for a cell whose provenance was
never recorded -- that is the `fill-the-shape-is-the-defect` trap, where a field's shape pulls a
fabricated value out of you.

## Do not fix it mid-block

`lettuce-leaf` is the release_verify baseline every candidate is compared against. Editing the
reference crop while promotes are in flight moves the ground under them. Both sessions deliberately
left it alone.

## The sibling artifact, same family

`release_verify --expect-changed` silently adds its own `--slug` default (`cherry-tomato`) to the
expected-changed set, so a batch that does not touch cherry-tomato reports
`CONCERN: crops changed = [...] (expected [... 'cherry-tomato' ...])`. Same root assumption: **the
tool treats the pilot slug as a universal reference, and it is not one.** Both belong to the same
hardening pass.

## Also surfaced, not chased

24 further occurrences of `plantings_provenance` sit one level deeper, at
`crop.regions.<region>.resolved_by_zone.7` and `.8` (12 each). That is a different shape at a
different level, and nothing here depends on it. Noted so a later count reconciles: **1,564
document-wide = 1,540 at region level + 24 nested.**
