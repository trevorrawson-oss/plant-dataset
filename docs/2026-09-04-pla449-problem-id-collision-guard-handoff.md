# PLA-449 close-out + handoff -- the problem-id collision guard

**Date:** 2026-09-04. **Lane:** Claude Code (gate authoring). **Canonical: UNCHANGED.**
`a9c84847fe2e0ad595db8cf9cc7d7e82ac65803e3284e16071be6d536bf9dad7` before and after. No dataset
edit, no promote, no LATEST bump. Tooling only.

---

## 1. What shipped

| file | what |
|---|---|
| `tools/problem_id_collision_gate.py` | the guard, three checks, flag-not-fail |
| `tools/problem_id_registry.json` | the registration path, 10 adjudicated entries |
| `tools/test_problem_id_collision_gate.py` | 26 tests, counts pinned to `a9c84847` |
| `tools/mutate_problem_id_collision_gate_suite.py` | 28 mutations, 9 families |
| `05-methodology/current/problem_id_collision_guard_v1_0.md` | the method the next arc inherits |

Checks: **1** `ID_NEAR_DUP`, a minted id within edit distance 2 of any live id. **2** `NAME_SHARED`,
a display name that normalized already appears under a different id. **3** `FAMILY_MEMBER`, an id
whose name is one conjunct of an already-flagged id's name **and** whose id tokens nest inside it.

## 2. The fixture result

PLA-449's bar in both directions -- materially fewer means too narrow, materially more means it
floods.

```
34 findings   ->   22 OPEN   +   12 suppressed by the registry
                   |
                   +-- 10 pairs = the EIGHT PLA-449 duplicate decisions, all present,
                   |             with EVERY id in each reachable (the slug decision
                   |             surfaces all three: slugs / slugs-and-snails / snails-and-slugs)
                   +-- 12 pairs = 7 residue decisions, enumerated in section 4
```

The nine known-good pairs are asserted **flagged raw and then suppressed**, not merely absent --
asserting absence alone would pass on a guard that never found them, which is the difference
between a registration path and a blind spot.

Suite **26/26 green**. Harness **28 injected / 0 survivors** across `distance`, `plural`,
`normalize`, `conjunct`, `nesting`, `scoping`, `registry`, `schema`, `mechanics`; anchor preflight,
positive control GREEN, sentinel REDDENS. **One mutation withdrawn, not injected**: `edit_distance`'s
`if a == b: return 0` is an optimization, not a branch (the DP returns 0 unaided), so its survival
would be noise dressed as a gap. Annotated at its site.

## 3. THE FINDING: batch 24 minted the ninth pair itself

The audits were run at `80519a28`. Batch 24 landed after. Running the guard across both states:

```
80519a28 (audit base)   28 pairs
a9c84847 (now)          32 pairs      +4, ALL introduced by batch 24
```

| new pair | how |
|---|---|
| `pink-root` <-> `pink-rot` | celery's `pink-rot` carried an id all along; batch 24 **minted** `pink-root` when it laddered the alliums |
| `botrytis-leaf-blight-neck-rot` <-> `gray-mold` | chives' "Botrytis (leaf blight and neck rot)" collides with chamomile's "Botrytis (gray mold)" once parentheticals are stripped |
| `chives-rust` <-> `bee-balm-rust` / `sunflower-rust` | batch 24 minted `chives-rust` with the bare display name "Rust", joining an existing bare-"Rust" pair |

**`pink-root` / `pink-rot` is the load-bearing one.** It is edit distance **1**. Batch 24's own
per-batch precedent check was `_stem_key`, which strips a trailing plural `s` -- and `pink-root` and
`pink-rot` are stem-DISTINCT, so **batch 24's guard could not see the pair batch 24 was creating.**
That is the concrete argument for edit distance over stem equality, and it is why this guard is a
shared module rather than a thing each batch re-derives.

All four are correct authoring. `pink-root` / `pink-rot` is adjudicated distinct in PLA-448 §2
(celery's is *Sclerotinia*) and is seeded into the registry. The guard behaved exactly as designed:
it surfaced a decision that had already been made, and the registry is where that decision now
lives so no future batch re-asks it.

## 4. The 12 residue pairs -- 7 open decisions, none of them a guard defect

Ordered by how cheap they are to close. **None requires a source read except #4 and #7.**

| # | pairs | decision |
|---|---|---|
| 1 | `aphids`/`apricot-aphids`/`citrus-aphids` <-> `plum-aphids` (3) | **Extend a registered family.** PLA-449's known-good line names three aphid ids; `plum-aphids` is the identical host-scoping and PLA-448 §2 G01 already rules plum's qualified form *more* correct. Add it to the aphid entry. |
| 2 | `anthracnose` <-> `blueberry-ripe-rot`, `blueberry-ripe-rot` <-> `cane-anthracnose` (2) | **Extend a registered family.** Same shape: "Anthracnose (ripe rot)" is host-scoped blueberry *Colletotrichum*. Add to the anthracnose entry. |
| 3 | `birds` <-> `birds-and-squirrels` (1) | fig/sunflower's "Birds (and squirrels)" against bare "Birds" on 5 crops. Scope call, no organism question. |
| 4 | `bee-balm-rust`/`chives-rust`/`sunflower-rust` (3) | **PLA-448 §4f, bare generics.** Three host-scoped ids all displaying bare "Rust". The *ids* are right; the *names* are under-qualified. Fix is the names. Needs the §4f source read. |
| 5 | `beet-spinach-leafminer` <-> `parsnip-leafminer` (1) | parenthetical-deletion artifact: "Leafminer (beet and spinach leafminer)" vs "Leafminers". Different taxa; register. |
| 6 | `botrytis-leaf-blight-neck-rot` <-> `gray-mold` (1) | same artifact, batch-24 origin. Different diseases; register. |
| 7 | `anthracnose` <-> `viola-leaf-spots` (1) | "Anthracnose and leaf spots" vs "Leaf spots and anthracnose" -- two crops bundling the same pair under two ids. **PLA-448 §4d bundled scope**, not a naming defect. |

**Do not soften the normalization to make #5 and #6 go away.** Total parenthetical deletion is the
only reason `gray-mold` reaches artichoke's `botrytis-gray-mold`, which is one of the eight. Both
behaviours are pinned in the suite.

## 5. A blind spot found and closed during the build

The seven microgreen crops and `microgreens-mix` carry `name_seasoned` / `name_beginner` and **no
`name` key**, so check 2 was blind to them. `microgreens-mix` is already laddered, so this was live,
not hypothetical -- and the microgreens are one of the three remaining PLA-8 families. A minted
`damping-off-microgreens` sits edit distance **11** from `damping-off`, so check 1 would not have
caught it either: the batch would have passed silently.

Closed by falling back `name` -> `name_seasoned` -> `name_beginner`. **Free on this canonical** --
the finding counts are unchanged, because the only id-ed crop on that schema is `microgreens-mix`
and its names normalize onto ids it already shares. Two mutations cover it.

## 6. Read-only answer: the seven crops with no problem entries

`avocado`, `olive`, and the five mushrooms (`button-`, `lions-mane-`, `oyster-`, `shiitake-`,
`wine-cap-`). All seven carry `pests: []` and `diseases: []` -- the keys are **present and empty**,
not absent -- and all seven have `verification_status.status = None`.

**Intended.** These are exactly the "7 honest shells" CLAUDE.md names (the 5 mushrooms +
avocado/olive), the residue of the 121-certified roster. Not a gap, and nothing to fix.

Arc arithmetic, recomputed on `a9c84847` rather than carried from the audit:
**101 laddered + 20 unladdered + 7 shells = 128.** PLA-448's "97 + 24" was measured at `80519a28`,
before batch 24 laddered the four alliums.

## 7. Next batch

**Batch 25 = the herbs**: `lavender`, `lemongrass`, `mint`, `oregano`, `rosemary`, `sage`, `thyme`.

Ordering is Trevor's 2026-08-26 rule -- **order by what users open, not by what is cheapest to
author.** The PLA-8 worklist notes the microgreens are "likely the fastest batch in the arc"; that
is precisely the reason they go last. Herbs are the highest-demand family remaining.

Remaining after that: trees/shrubs (`mulberry`, `pawpaw`, `pear-asian`, `pear-european`,
`persimmon`, `pomegranate`), then microgreens (7).

**Wire the guard in at id-pinning time, before fan-out** -- that is where batch 17's lesson already
puts id decisions and the only point at which changing an id is free:

```bash
python3 tools/problem_id_collision_gate.py <post-apply-scratch.json> \
        --minted <the ids this batch mints> --strict
```

Run it against the **post-apply** data. Against the untouched canonical a minted id has no display
name, so only check 1 reaches it; the CLI warns on stderr rather than returning a quiet clean.

## 8. Not done, deliberately

* **The eight duplicates are still live.** Merging them is PLA-448 §7's fast-follow and blocks
  PLA-12. This ticket built the guard, not the merge.
* **Bundled scope (§4d) and bare generics (§4f) are not answered.** Check 3's nesting brake
  deliberately excludes §4d; §4f surfaces as `NAME_SHARED` and is listed above as residue #4/#7.
* **`celery-early-blight` / `celery-late-blight` (§4c) is untouched** -- a content defect, not an
  id-collision one. The guard cannot see it: celery shares an id with 7 crops *correctly* by the
  string, and wrongly by the organism.

---

## 9. Landed

Committed `d1197c7` on `main` and **PUSHED** 2026-09-04: `3372091..d1197c7`, `origin/main` at
`d1197c7`. Six files, +1071/-1. Pre-commit release-verify skipped by design
(`crops_data_final.json` not staged). **Never amend this commit** -- the promote fixtures pin
commits by SHA.

Canonical remains `a9c84847fe2e0ad595db8cf9cc7d7e82ac65803e3284e16071be6d536bf9dad7`; `LATEST.txt`
untouched. No plant-astro submodule bump is owed, because no dataset content changed.
