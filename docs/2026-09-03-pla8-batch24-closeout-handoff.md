# PLA-8 -- BATCH 24 CLOSE-OUT AND HANDOFF: the record pass finished, the alliums landed, and the arc STOPS here

**Written 2026-09-03 at the end of the session that closed the alliums.** Read this before doing
anything. Verify first: `shasum -a 256 crops_data_final.json` must match `LATEST.txt`, then
`git log -1` and `git status -sb`.

**THE RULING THAT GOVERNS THE NEXT SESSION (Trevor, 2026-09-03, mid-session):** wrap batch 24 and
stop. Do NOT start batch 25. An id audit found **8 duplicate-id pairs** across the dataset
(`cutworm`/`cutworms`, `flea-beetle`/`flea-beetles`, `japanese-beetle`/`japanese-beetles`,
`bacterial-leaf-spot`/`bacterial-spot`, `gray-mold`/`botrytis-gray-mold`,
`two-spotted`/`twospotted-spider-mite`, `bacterial-blight`/`bacterial-blights`, and
`slugs`/`slugs-and-snails`/`snails-and-slugs`), all minted by authoring passes that did not check
precedent against existing ids. 20 crops remain unladdered; continuing would mint ~20 crops' worth
of new ids with nothing checking for collisions. **The next session's first task is a collision
guard, not a batch.** PLA-448 §1's "no pipeline changes until PLA-8 closes" is superseded on this
one point by Trevor's direct instruction; everything else in PLA-448 stands.

---

## 1. What landed this session (all PUSHED to origin/main 2026-09-03, `6663862..742343f`)

| commit | what | canonical |
|---|---|---|
| `69e96a3` | **r2** -- leek moth + leek allium leaf miner rewritten from RHS's UK feeding months to Cornell/UVM/UNH and UMD/Cornell/UMass; cover BEFORE the flight | `80519a28` -> `50ffedb0` |
| `7091606` | `COMMIT_FOR` for `50ffedb0` | |
| `2063c46` | **r3** -- the repoint round: onion maggot on SIX crops (five shipped rung notes on garlic and spring-onion), pink root on three, chives rust + PNW, chives botrytis to UC IPM leaf blight | `50ffedb0` -> `9d2031ff` |
| `55afcb2` | `COMMIT_FOR` for `9d2031ff` | |
| `264747c` | **r4** -- onion thrips on five crops; two shipped `crop_rotation` rungs replaced in place by `garden_sanitation` | `9d2031ff` -> `47e7b5c0` |
| `a200d35` | `COMMIT_FOR` for `47e7b5c0` | |
| `4906b22` | **BATCH 24** -- chives, leek, onion, shallot; 26 problems / 95 rungs laddered from the CORRECTED records; roster 97 -> **101** | `47e7b5c0` -> `a9c84847` |
| `cccc8c6` | `COMMIT_FOR` for `a9c84847` | |

Each shipped with a guard suite and a mutation harness at ZERO survivors, gauntlet green
(`gate_all` 121/121, every touched crop PASS, `control_ladder_gate` 0, A54 0,
`register_completeness` PASS, `release_verify` clean with exactly the declared crops changed), the
state trio amended, and a fixture pin registered. E1 blocked every commit (plant-app owes
`npm run build:guides`, now THIRTEEN dataset revisions behind), so every commit used `--no-verify`
with the reason in the message. **Never amend any of these commits**: `COMMIT_FOR` pins them and
breakage shows up as guards SKIPPING while reporting green.

**PUSHED 2026-09-03 on Trevor's go-ahead**: `6663862..742343f`, origin/main now at `742343f`.
A dataset change reaches the live site only via a plant-astro submodule bump, which is a website
concern owned by that repo's session and is NOT done here.

---

## 2. The record pass is COMPLETE: 10 of 10 decisions

| # | decision | landed in |
|---|---|---|
| 1 | onion maggot repoint, SIX crops (measured, not the handoff's four) | r3 |
| 2 | onion thrips content, five crops, two shipped rungs replaced | r4 |
| 3 | pink root repoint + clean-stock claim dropped + leek severity low | r3 |
| 4 | chives aphids retired | `61d5f8b` (previous session) |
| 5 | chives botrytis source + content (name and id UNCHANGED) | r3 |
| 6 | chives rust + PNW | r3 |
| 7 | leek moth rewrite | r2 |
| 8 | leek allium leaf miner rewrite | r2 |
| 9 | leek rust | r1 (previous session) |
| 10 | shallot downy mildew | r1 (previous session) |

Two triage verdicts CHANGED on reading the documents, and both are recorded in the promotes:
* The onion-maggot "residue" claim was called CONTRADICTED by UC IPM's "incorporate crop residue
  well in advance of planting". That sentence sits under SEEDCORN maggot. What the documents say
  about onion maggot and organic matter is ATTRACTION (UMN "Do not use animal manure or green
  manure in your garden in spring"; Clemson; USU), and the mechanism error was elsewhere: "carry
  over in residue" when every document says the pupae overwinter in the SOIL and cull piles and
  volunteers sustain the fly.
* The thrips "vigor" and "hose" claims were called unsupported off UC IPM's AGRICULTURE page and
  are supported on its HOME-AND-LANDSCAPE page and on USU's and UMD's home-garden pages. Same
  institutions, different documents. Hunt before downgrading, again.

---

## 3. Batch 24, re-authored: what changed against the previous staging

The previous handoff measured 71% of the old batch as needing re-authoring. In practice the four
authoring agents rewrote almost everything: onion and leek reused NOTHING, shallot reused three
white-rot beginner notes and one cure_and_store beginner note, chives reused eleven rungs verbatim
after re-reading each against the corrected record. The old outputs are kept as
`tools/staging/pla8_batch24_alliums/prev_out_<crop>.json` for the diff.

**The independent source-truth pass ran BEFORE the promote, on the re-authored content**, four
reviewers (one per crop), every anchoring document fetched and read (~60 documents). It found
**28 FIX items across 97 rungs** (onion 5, shallot 8, leek 8, chives 7): 7 WRONG, 7 UNSUPPORTED,
the rest SYNTHESIS, STYLE or FIT. NONE was a timing rule: cover-before-the-flight, the trap
precondition in both registers, pupae-in-soil, no thrips rotation, no pink-root clean stock, no
downy-mildew variety, "over 20 years" all held on every crop. The defects were the finer class:
a spinosad note timed to adults laying when the method reaches the larva; "the one part you can
still fix" excluding the record's vigor claim; a drainage note naming waterlogging as THE stress
when the record lists drainage and stress separately; a weed-control note that told the reader
unrelated weeds do not matter when three anchors say weeds host thrips; a pheromone lure
"drawing the male moths" that no document states.

**One cross-crop call made at fix time:** the thrips `weed_host_control` rung carried the grain,
alfalfa and clover SITING claim under a WEED-removal method. It is DROPPED on onion and shallot,
whose records say nothing about weeds, and REWRITTEN on leek, whose record says to cultivate weedy
edges early in the year. The siting claim survives in the three records and, on some crops, inside
the garden_sanitation seasoned note.

Final counts: chives 27, leek 29, onion 16, shallot 23 = **95 rungs on 26 problems**; 10 warranted
temperature figures; precedent copy worst 0.612 over 260 + 20904 comparisons; suite 116; harness
88/88 (85 in four parallel groups, then the template-twin family 5/5 after three anti-vacuity
drivers were added, see §5.7).

### Claims the records carry that NO method can reach (filed, not forced)

* **Straw mulch against thrips** (USU "has been shown to reduce thrips populations"; UMass "Use
  straw mulch to deter thrips") on all five thrips records. `straw_mulch` is scoped
  `fungal_foliar`/`disease_general`. **Catalog r11 is the widening**, and it is a two-claim
  widening in the r10 shape: the method's `how_it_works_*` is strawberry gray-mold prose and needs
  a thrips mechanism sentence (USU: barrier to pupation in soil, predator enhancement), not just a
  new `applies_to` value.
* **Vigor for tolerance** (thrips) and **steady water and fertility** (pink root): `even_watering`
  reaches neither insect nor fungal, and this is r10's two-class problem again (see the previous
  handoff §7.1). Now reported by SEVEN authoring agents across three batches.
* **Spatial separation from a pressured neighboring allium planting** (chives, three pests):
  no method.
* **Leek moth pheromone trap** as a monitoring signal: no general pheromone-monitoring method
  (`codling_moth_pheromone_trap` is apple-scoped). Carried inside the spinosad rung as the timing
  signal only.
* **Delayed planting against a soil-pupating fly** (`planting_time_avoidance` on onion maggot):
  the method reaches `insect` and the record supports it, but the method's MEANS names only
  borers and the bean beetle. A third shape, flagged by two agents; kept.

---

## 4. Record-level findings the reviewers surfaced (NOT rung defects; file for the next record pass)

1. **onion's `botrytis-neck-rot` and `fusarium-basal-rot` rest on ONE anchor** (UMN
   growing-onions) that carries only "Resistant varieties are available for Fusarium basal rot",
   the nitrogen-and-curing sentence, and the harvest/cure/store steps. NOT on that page: bent-over
   green tops, white-skinned susceptibility, soilborne persistence for years, warm soil, wounds and
   maggot entry, several-years rotation. Every fusarium rung and both botrytis rungs carry at least
   one of those claims FAITHFULLY from the record. The rungs are right against the record; the
   record is under-anchored. Same for shallot's botrytis "do not knock green tops down".
2. **chives' white rot says "a decade or more"** where r1 converged leek and shallot on UC IPM's
   "over 20 years". The chives record was not in the triage. The rung follows the record.
3. **chives' downy mildew** names splash alongside wind; UC IPM says "Spores are airborne" and
   never mentions splash. Same defect class r1 fixed on shallot and r3 fixed on chives botrytis.
   The rung now leads with wind.
4. **chives' onion-thrips anchor (USU onions-in-the-garden)** supports only "stiff spray of water"
   and "natural biological control"; shearing, soap, spinosad, pirate bugs, lacewings and
   "cosmetic" are record claims with no anchor. Chives was "likely to stand" and stands, but its
   thrips entry is the next to repoint (the r4 document set covers all of it).
5. **leek's pink root "lesser host"** and **leek rust "comparatively resistant"** are inferences
   from UC IPM ("primarily a problem on onion"; "Leek, elephant garlic, and shallot are more
   resistant") and UF/IFAS ("Leek is also susceptible"); PNW adds that European strains are
   "extremely damaging on leek". Defensible for a US audience; not verbatim anywhere.
6. **leek's white rot could carry UC IPM's infection threshold** ("As few as one sclerotium per
   10 kilograms of soil"; UMD/UMaine publish the pounds form). The record says "a few sclerotia
   per soil sample"; the authoring agent correctly refused a figure the brief gave it that the
   record did not. Add it to the record with its source, then to the rung.
7. **The onion-maggot "first flight arrives with the cool, wet weather of mid-spring"** (r3, onion
   cause_seasoned) fuses two separate UMN statements. Minor; note for the next pass.

---

## 5. THE HARNESS LESSONS THIS SESSION PAID FOR (all measurement, none branch)

1. **A regex written `carries?` matches "carries" and "carrie" and NOT "carry".** The r3
   debris-carryover predicate let "populations carry over in allium residue" past; only the
   residue predicate caught it. Found by the suite's both-directions assertion. Then the widened
   pattern caught garlic's shipped "carry over in allium GROUND", the CORRECT mechanism, until the
   object was constrained to residue/debris/material/scraps. **Two defects in one predicate,
   opposite directions, neither visible to a branch mutation.**
2. **A case-sensitive `resistant` refused "Resistant varieties are the best control."** The
   guard-rejects-correct-input shape, fourth instance in the arc.
3. **A head count of "35 prose fields" was wrong; the table held 42.** The table is the count.
4. **A TARGET's unpinned field could change unseen** in r3 and r4: the owner check passes because
   the owner IS a target, and the counts count only pinned fields. r4's suite found it; both
   promotes now match every changed leaf under a target to a pin. r2 was immune only because every
   field of its two targets was pinned.
5. **The unpinned-field check then MASKED the prose-count check**: an extra change is refused
   earlier, so only a REVERTED pinned field reaches the count. r4's harness reported the survivor;
   a reverted-field driver was added and the harness re-run in full.
7. **Three template-twin mutations survived the re-authored batch's harness** because their
   drivers had been written against the OLD records: on the corrected data the historical-bug
   mutation (FULL fields imposed on an allium-schema crop) produces no false twin, the presence
   filters silently skip every problem of that crop instead, and the two filter mutations are
   no-ops on real data because every real problem carries its schema. The only observable is the
   COMPARISON COUNT, so three drivers now measure through the anti-vacuity branch on a leek-only
   batch. A driver that fires on a real twin proves nothing about non-coverage.
6. **The per-crop validator handed to the authoring agents was itself wrong twice**, and two
   agents fixed it on disk: the promote's declared-identity check demanded onion's pin from every
   single-crop run, and a length mismatch skipped the whole pests loop so an early "4 refused" was a
   floor, not a count. Tooling handed to a fan-out is tooling that will be exercised harder than
   its author exercised it.

---

## 6. What the next session does (in this order)

1. **The id collision guard** (Trevor's instruction). Shape suggestion, read-only measured this
   session: every `pests[]`/`diseases[]` `id` is a per-crop join key and ids are REUSED across crops
   by design (`onion-thrips` on five crops), so the guard is not "no duplicates" but "no two ids
   that normalize to the same organism". The 8 pairs above all collapse under a stem+synonym
   normalization (`_stem_key` in `promote_pla8_batch24.py` already strips plurals; it needs a
   synonym table for `two-spotted`/`twospotted`, `slugs-and-snails`/`snails-and-slugs`). Batch 24's
   pin table process (ids pinned BEFORE fan-out, decided against the live roster with a stemmed
   scan plus a taxon check) is the manual version of what the guard should mechanize. Wire it as a
   `check_*` in the promote template AND as a roster gate (A-numbered) so a future rename pass is
   caught too. Mutation-test it against the 8 known pairs as positive controls.
2. Then, and only then, the 8-pair adjudication and repair (PLA-448 §2 now has 8 more rows).
3. Catalog r11: `straw_mulch` to `insect` with a thrips mechanism sentence; the seven-report
   `even_watering` two-class problem is NOT a simple widening (see §3).
4. Batch 25 (mulberry, pawpaw, persimmon, pomegranate): COARSE-typed, needs batch 23's upgrade
   guard shape, not batch 24's set-from-nothing. Batch 28's pear decline re-type to `bacterial`
   as a pinned adjudication. All in the previous handoff §8.

## 7. Roster position

**101 / 121 laddered.** Remaining: **20 crops / 89 problems / 5 batches**, unchanged from the
previous handoff's table (batches 25 to 29). PLA-448 §3 (the name guard) is still Trevor's call and
is now partly overtaken by the collision guard above: an id guard and a name guard are the same
check on two fields.
