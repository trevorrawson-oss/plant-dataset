# Citation-integrity arc — RESUME HERE

**Written:** 2026-07-31, at the close of the audit-response session.
**Last revised:** 2026-07-31, at the close of the cleanup-batch session (see §8).
**Canonical:** `c6f50a1417a82786356fef764e524641143d41f973dc8f7097eb18454cb3fe5a`
**HEAD:** `8d7febc` on `main`, **pushed and in sync with origin.** 128 crops / 121 certified.
**Re-verify before trusting this header** -- the first version of it was 3 commits stale within a
day of being written, which is the same failure mode this document warns about in §7. It has since
been corrected twice. **Treat every number in this file as a question, not a fact** -- §3 and §4
carry measurement dates for exactly that reason.

> **A NEWER, NARROWER HANDOFF EXISTS.** `docs/kickoffs/49-herb-hardiness-attribution-hunt.md` is
> the next concrete unit of work: five herb crops crediting UAEX with claims that appear to be
> NC State's, on a bare-host citation. Read 49 if you are picking up a task; read this file for
> the arc's shape and for what is ruled out.

**Supersedes the operational half of `docs/kickoffs/47-citation-arc-continuation-handoff.md`.**
47's §2 correction banner and §4 lessons still stand; its numbers and worklist are stale.

**The arc is NOT abandoned.** Trevor's direction, 2026-07-31: *"I still want to keep doing the work
we were already doing before this audit, it's still good work that needs to be done."* This document
exists so that work resumes correctly, not so it gets replaced.

---

## 1. Verify state first (60 seconds, non-negotiable)

```bash
cd ~/plant-dataset
shasum -a 256 crops_data_final.json     # must equal LATEST.txt
git log --oneline -1                    # expect 8d7febc
git status -sb                          # expect clean, in sync with origin/main
python3 -m pytest tools/ -q --ignore=tools/test_build_berry_pilot_patch.py   # expect 338 passed
```

`test_build_berry_pilot_patch.py` breaks pytest **collection** (module-level `sys.exit(0)`).
Pre-existing. Ignore it, or fix it the way `test_build_corn_family_patch` was fixed.

Three untracked items are **not yours**: `.claude/`, `tools/staging/shards/`,
`docs/2026-07-29-establishment-path-encoding-question.md`.

---

## 2. What changed on 2026-07-31, and what it means for the arc

Six canonical promotes plus four tooling fixes. The arc's **method is unchanged and validated** --
an external blind audit independently praised the quality of the finds and fixes. What changed is
how you should **schedule** the work.

**Detection is now free.** `tools/internal_contradiction_scan.py` finds cells that contradict data
we already hold, with no network and no document hunt. It exists because blueberry was authored
wrong while the numbers refuting it sat in the same file: `region_chill_delivered` said mid_south z7
banks 1000-1300 hours, our own variety table said rabbiteye needs 350-600 and northern highbush
800-1000, and our own `northern_tier` already used northern highbush at z7. Nobody looked across.

**So the hunt was the wrong UNIT, not the wrong idea.** Locating a document is still what forces
you to read the cell against it, and that reading is where every real defect has come from. But you
no longer need to hunt a whole region-source pair *hoping* something surfaces. Run detection, get a
ranked list of contested cells, and hunt only where **adjudication** genuinely needs a document --
which is one targeted lookup for one crop, not twenty.

**Recommended order:**

1. **Schedule hunts by where contradictions cluster**, using the scan, rather than by bare-host
   count. Same careful reading, aimed at where we are demonstrably wrong.
2. **The mechanical residue is genuinely small** (§4) once the ruled-out work is stripped.
3. **Keep both auditors running.** Trevor's external blind audit and our scan overlapped on
   *exactly one* finding (the tomato NPK wording). Each caught what the other could not. That
   overlap-of-one is the best available evidence that neither method is close to complete.

---

## 3. Tools

| tool | question | network |
|---|---|---|
| `bare_host_scan.py` | which citations point at a bare domain root? | no |
| `citation_provenance_scan.py --decisions` | how many DECISIONS and HUNTS is that? | no |
| `doc_mentions_crop_scan.py` | does the cited document mention the crop at all? | yes (cached) |
| **`bloom_datum_scan.py`** | does the cited document publish a bloom date? | yes (cached) |
| **`internal_contradiction_scan.py`** | **does this cell contradict data we already hold?** | **no** |
| **`promote_fixture.py`** | rebuild the pinned pre-state for any promote guard suite | no (git) |

**Current readings** (re-measured 2026-07-31 against canonical `c6f50a14`; re-measure again, do
not quote these):

- `internal_contradiction_scan`: **178 contested cells** -- CHILL 34 (23 UNDER / 11 OVER), TYPE 11,
  DATES 35, TEMPLATE 24, SUIT 74. NPK is **0**. **Unmoved** by this session's promotes, which is
  correct: they were prose and schema-shape only.
- `citation_provenance_scan`: 614 SOLE pairs / 414 nodes / **167 decisions / 32 hunts**.
- `doc_mentions_crop_scan`: CROP-LIST-omits-crop **356 nodes / 214 decisions**; REFERENCE 107 / 27.

> **178 IS NOT A DEFECT COUNT, AND THREE OF ITS FIVE FAMILIES HAVE NOW BEEN ADJUDICATED.**
> Four separate times on 2026-07-31 a raw count was mostly artifact, **twice in tools written that
> same day**. Since then, reading the actual cells has retired most of the total:
>
> - **SUIT (74) and TYPE (11): LOW VALUE, do not work them as a list.** Both flag one zone rating
>   or typing differently across regions -- apple z8 is `fruits_reliably` in seven regions and
>   `marginal` in `utah_dixie`; blackberry is `everbearing` in Nevada and `summer_bearing`
>   elsewhere. **That is the region model working as designed.** Treating these as a worklist would
>   mean flattening it. If anyone works them, narrow the CHECK, not the scope.
> - **TEMPLATE (24): ADJUDICATED. 13 correct, and the real slice is 10 sentences in 7 cells.**
>   Deduped it is 21 distinct pairs; all were read. Twelve are the chill-hours template where both
>   the number and the source were properly regionalized and match `region_chill_delivered` exactly.
>   The rest is in `docs/kickoffs/49-herb-hardiness-attribution-hunt.md`.
> - **CHILL (34): 20 of the 34 rows rest on ONE unsourced placeholder** -- elderberry's uniform
>   `chill_hours_required: 400`. See §4.
> - **DATES (35): still untouched**, and now the most promising unexamined family. It flags cells
>   whose planting window shares no month with any peer region; some will be legitimate desert or
>   valley inversions, some will not.

**Both cached scans take `--refetch-unreadable`.** Use it. 15 of 631 cached documents were WAF
challenge pages served as HTTP 200 or PDFs with no text layer, and both scans read them as
*absence*, manufacturing defects from pages nobody had read.

---

## 4. Open work

**The one needing a ruling before anything else.** **Berries carry no `suitability` field at all.**
Measured: **0 of 195** berry cells (5 crops x 39) carry the key -- absent, not null -- while the
five other fruit categories all have it. Berries carry `recommended_type` (which type to grow) with
no field for whether to grow it here. This is a **cross-crop field addition**
(`docs/gs_cross_crop_field_addition_v0.md` + `field_addition_register.md`), not a promote.

> **CORRECTION 2026-07-31 -- the original justification here was OVERSTATED and the correction
> matters, because it changes what the field is for.** This paragraph used to say we recommend
> `american_elderberry` into 0-150 hour zones "with nothing able to warn anyone". **All 23 UNDER
> cells were then read: 20 of them ALREADY WARN in prose** -- Hawaii elderberry says *"this is a
> tough spot for it... treat it as an experiment"*. Only 3 were silent (elderberry `rgv` z9/z10,
> which call it *"a straightforward choice"*, and raspberry `ca_north_coast` z10, below). So the
> real gap is **machine-readability** -- nothing can filter, sort or drive a notification off
> prose -- plus consistency with the other five fruit categories. That is still a good reason to
> add the field. It is not the reader-safety emergency this paragraph originally implied.
> **BLOCKED:** sequence this AFTER the elderberry reclassification, which touches the same crops.

**Berry chill, now split into three separable pieces (2026-07-31):**
- **Elderberry's `chill_hours_required: 400` is an unsourced placeholder and accounts for 20 of
  the 34 CHILL rows.** All six cultivars carry the identical 400 with null ranges. Neither cited
  source mentions chill even once -- including **Missouri Extension AF1017, the definitive US
  elderberry production publication** -- and nothing in the 631-document cache publishes an
  elderberry chill figure. The crop's own `chill_hours_note` says the requirement is low and
  *"NOT how you choose a cultivar"*. The number exists only because `whole_crop_gate` **A21**
  requires a numeric per-variety chill for `calendar_basis == berries_woody`, and
  `berries_woody_gate` separately requires `gating_factors` to contain `chill_hours`. Nulling it
  in a scratch copy takes CHILL **34 -> 14**. **Trevor ruled: fix the classification, not the
  number.** **BLOCKED on plant-astro** -- `BerryChillCard` reads the per-variety chill; ship the
  frontend first (`fail-open-renderer`).
- **11 rows survive and look real** -- blackberry 5, raspberry 6. Those crops have genuine
  per-cultivar chill spread and real ranges. Sharpest: **raspberry `ca_north_coast` z10** asserts
  *"Adequate chill and cool ripening give full-flavored fruit"* while the zone banks 150-600 and
  the lowest summer-bearing cultivar we list (Tulameen) needs 700. The z9 cell carries the
  identical sentence and IS fine (banks 300-800). Likely a `recommended_type` change = a value
  ruling.
- **A LIVE FRONTEND DEFECT found alongside it, independent of any dataset change.** `plant-astro`'s
  `BerryChillCard.astro:42` hardcodes *"Will your winter chill these blueberries?"* and
  `BerryYearCalendarCard.astro:82` hardcodes *"your blueberries"*; both render for **every**
  `berries_woody` crop, so raspberry, blackberry and elderberry pages say it twice. Trevor confirms
  **plant-app has the same defect**. A full handoff is in Trevor's Notes app. Not a dataset fix --
  the card bodies already pull `chill_hours_note_*` from the dataset; what leaked is chrome.

**Citation arc proper:**
- **32 hunts / 167 decisions remain** (this file previously said 30 hunts; the tool says 32 --
  re-measured 2026-07-31). Schedule them by §2.
- **The densest single cluster is CALIFORNIA: eight hunts on `ucanr_ext` + `uc_mg` across the four
  CA regions**, ~76 crop-decisions on one institution's document family. A 92-cell California
  adjudication already exists in `docs/2026-07-29-citation-cleanup-sample-pass-outcome.md` (read
  its 2026-07-31 correction banner first). This is the biggest remaining prize and it is real
  document work -- scope it deliberately, do not start it casually.
- **`docs/kickoffs/49-herb-hardiness-attribution-hunt.md` is the next concrete unit:** five herb
  crops crediting UAEX with 10 attributed sentences across 7 `mid_south` cells, on a bare-host
  citation, where the number is NC State's and only the institution name moved.
- Hunt 2 residue: 8 crops with no located document (`apricot`, `cherry-sour`, `cherry-sweet`,
  `pomegranate`, `elderberry`, `blueberry`, `raspberry`, `strawberry`).
- ~~`ucr_citrus`: 33 pairs / 4 crops, **one method** -- UCR accession pages carry "Season of ripeness
  at Riverside", and Riverside **is** `ca_interior`. Cheapest real closure available.~~
  **WITHDRAWN 2026-07-31. THE PREMISE IS FALSE AND THIS IS NOT A CHEAP CLOSURE.** Riverside is not
  `ca_interior` by our own data: `zone_frost_data["10a"].regions.mediterranean` lists
  **Los Angeles LAX, San Diego, Long Beach, Riverside** -- the `ca_south_coast` set -- while
  `ca_interior` is anchored on the Central Valley (Sacramento/Fresno/Bakersfield/Modesto 8a,
  Tulare 8b, Stockton/Merced/Livermore 9a). The claim came from ONE observation on `crc3178`, an
  Owari Satsuma (a **mandarin**), generalized to all 33 pairs. Measured over **24** accession pages:
  24/24 carry the ripeness field, **1/24** also carries Lindcove (which genuinely is the interior
  valley), and **0/24 publish a bloom date**. The datum is SINGLE-SITE and has no regional resolving
  power -- our four CA grapefruit windows all sit inside one location's *cultivar* spread -- and for
  lime UCR's Oct-Dec means *"full maturity ... they drop from the tree"*, not our green-lime Jul-Dec.
  Decisive without geography: `source_catalog.ucr_citrus.citable_for` is "variety identity,
  characteristics, parentage, and home-grower recommendations" and never claimed regional date
  windows, so **31 of the 33 pairs are CASE 2 (unsourced claim), not CASE 1 (repoint)**. The 2
  in-scope pairs are Flying Dragon `rootstock_options[2]`, and even those need UC ANR's rootstock
  publication (a new catalog admission) for the resistance and soil claims. Full working in
  `STATE_HISTORY.md` 2026-07-31. **Kickoffs 46 and 47 carry the same false sentence.**
- ~~The held-back `ca_desert` pumpkin repoint (now clean).~~ **READS AS LANDED** -- the desert
  cucurbit soil-temp fix is committed (`b0c27a5`); pumpkin `ca_desert` z9/10/11 now read plant
  `Mar 1 - Mar 15`, harvest `Jun 15 - Jun 30`. Confirm before re-opening.
- ~~3 citation-only contradicted shapes (winter-squash Jul-vs-Aug; okra `ca_desert`; okra
  `ca_north_coast` z9).~~ **STALE PLACEMENT, 2026-07-31.** None of `okra`, `pumpkin` or any squash
  appears anywhere in the current `internal_contradiction_scan` output. These came from the
  2026-07-29 sample pass, not from a scan, so listing them under a scan-driven worklist is
  misleading. Current values: okra `ca_desert` z9/10/11 harvest `May 25 - Nov 30` / `May 15 -
  Dec 15`; okra `ca_north_coast` z9 plant `Jun 1 - Jun 30`, harvest `Aug 10 - Oct 15`. Re-derive
  the concern from the source before spending on it.
- `pole-beans`: harvest starts 50 days after sowing against a stated min DTM of 60, identically in
  every region. One modeling question, not 20 cell errors. **Still open** (`days_to_maturity`
  `[60, 70]`, `dtm_anchor` `from_sow`).

**Mechanical residue (small):**
- **9 orphan anchors** in LIVE subtrees -- the reverse shape from the zone-layer ones: an
  `anchoring_urls` entry with **no matching source id**. `lavender` 4 (`osu_ext_prune_lavender`),
  `basil` 2 (`uariz_ext_az2061`), 3 tomatoes (`ucd_postharvest` on `yield_expectations`).
  **Re-measured 2026-07-31: still exactly 9, same crops, same ids.** These are the ONLY
  source/anchor mismatches outside the ruled-leave `zones{}` layer. **Beware the naive recount:**
  flagging every anchor id not listed in its own node's `sources` returns **2064**, because an id
  is often sourced at a parent node. That number is an artifact of the method, not a finding.
- `lavender` / `hawaii_tropical` anchors on `westhawaiitoday.com`, a **newspaper**. Tier-bar call.
  **Re-measured: 5 anchor entries** (1 in `plantings[0]`, 4 in `resolved_by_zone` z10/11/12/13),
  under source id `uhawaii_ctahr_hawaii_county` which is **not in `source_catalog` at all** -- so
  this is an uncatalogued-source problem as well as a tier-bar one.
- The bloom slices: **138** arms where a declaration genuinely fits, **55** never-mentioned (defect
  candidates), **66** whose source actually publishes a date and could be repointed.

**From the external audit, still open and Trevor's call:**
- `launch_ready_core` is one Boolean over 121 crops, 62 of which carry an unfinished finding
  (**re-measured 2026-07-31: 121 true / 7 false, and the 62 reproduces exactly**). The audit argues
  for a richer release status. It has a point. Note a duplicate-field trap: a **separate top-level**
  `launch_ready_core` also exists on 3 crops only (beefsteak-tomato `true`, heirloom-tomato `false`,
  artichoke `true`), disagreeing in shape with the 128 under `verification_status`.
- ~~`asparagus` lacks 7 top-level fields the other 127 have -- a perennial-schema question, not an
  omission to backfill.~~ **WRONG, AND 5 OF THE 7 ARE NOW FIXED (`c6f50a14`, 2026-07-31.)**
  56 top-level keys appear on >=90% of the roster; asparagus lacked exactly 7 and was the SOLE crop
  missing each -- and **artichoke, the only other `herbaceous_perennial`, lacks none of the 56**, so
  the archetype was never the explanation. Five took the archetype-appropriate `null` that artichoke
  already carried. **Two remain, each its own ruling:** `yield_expectations` (present AND non-null
  on all 127 others, so a null would be a lie -- it needs sourced authoring, and Trevor has folded
  it into a **yield + family-consumption cross-crop arc** for the AI bot) and `zones` (the one real
  schema question; plant-astro reads `zones{}` and fails open, so it is in the frontend handoff).
  Nothing caught this because `whole_crop_gate` passes on asparagus and references none of the
  seven -- `optional-field-gates-go-vacuous`, third occurrence.
- `version` is still `1.0` after **eight** canonical promotes. A data build id would make comparison
  and rollback safer.
- `npk_ratio` is `5-10-10` on all five tomatoes while UMN advises a **low- or no-phosphorus** feed
  unless a soil test calls for it. A real question, deliberately left as a **value** change.

---

## 5. Closed. Do not re-investigate.

- **The roster-wide bloom declaration is WITHDRAWN.** Its premise was falsified: 22 documents at 12
  institutions publish month-granular bloom timing.
- **`zones{}` is LIVE and must NOT be deleted.** `plant-astro`'s `today.ts`,
  `[crop]/[zone].astro` and `TreeGuide.astro` all read it, and the access **fails open**, so
  removing it renders empty pages rather than erroring. Only its *anchor entries* are unrendered.
- **The 57 null anchors are a recorded decision, not a to-do.** Deleting orphans the source id in
  all 54 nodes; backfilling would cite a cut-flowers page, a tomatillo page, the elderberry
  publication, a bare host, or the known-dead `uga_b577` logo PDF. The note now says so.
- **`lettuce-leaf`'s 58 source/anchor mismatches** are all in that same zone layer, same
  disposition.
- **NPK is clean.** The only genuine defect was the tomato wording; the other 8 were the scan's own
  negation bug, since fixed.
- `mid_atlantic` blueberry (rabbiteye) is **verified correct** -- NC State recommends it below
  2,500 ft. Do not "fix" it to match `mid_south`.
- Template-inheritance risk is **bounded**: only `mid_south` <- `mid_atlantic` used cell-template
  reuse, and all 52 of its institution-attributed claims were read.
  > **QUALIFIED 2026-07-31 -- this line reads as more closed than it is.** Hunt 1's 52-claim audit
  > was scoped to the **fruit** crops. The five `mid_south` **herbs** (thyme, rosemary, oregano,
  > sage, lavender) were never in it, and they carry 10 UAEX-attributed sentences that look like
  > NC State's numbers with the institution name swapped. See kickoff 49. The *bounding* claim
  > still holds -- only this one region pair used cell-template reuse -- but "all its claims were
  > read" does not.

**Closed by the 2026-07-31 cleanup-batch session:**
- **`ucr_citrus` is WITHDRAWN** (§4). Do not re-propose it. Kickoffs 46 and 47 now carry the same
  strike-through, and the origin document (`docs/2026-07-29-citation-cleanup-sample-pass-outcome.md`)
  carries an appended `[CORRECTION]` banner with its original row left byte-for-byte.
- **The zone-lift prose defect is FIXED** (`172e4e7a`). 66 cells across 15 crops named the DONOR
  zone to the reader after the 2026-07-12 `zone_span` widen deep-copied donor rows without
  rewriting prose. De-zoned rather than renumbered, because renumbering would have relocated the
  Ojai Pixie into zone 11.
- **Artichoke's `open_findings` are now under `verification_status`** (`e353fadb`). It was the only
  crop of 128 storing them at the top level, so every gate and scan skipped it: the audit's **768
  findings is really 780**, and its "62 crops with unfinished findings" excluded artichoke.
- **`pet_safe` coverage is CLOSED at 121/121** (`a5ba1eb`, log-only, canonical untouched). The
  method is **NC State's plant toolbox, not ASPCA**. Three ASPCA name collisions would each have
  given a confident wrong answer: "Asparagus Fern" is *A. densiflorus*, "Corn Plant" is *Dracaena
  fragrans*, and the only ASPCA bean is *Ricinus communis*.
- **SUIT (74) and TYPE (11) are ruled LOW VALUE**, not a worklist. See the §3 note.

---

## 6. Protocol (binding)

- **Never mix a value change and a citation change in one promote.** One ruling per promote.
- **Promote only via a guarded script** pinning the pre-state SHA, asserting exact prior values,
  proving an exact footprint, aborting on drift.
- **Guard fixtures must be REBUILT, never copied from live canonical.** Use
  `promote_fixture.scratch(BASE_SHA, mutate)`. Six suites had gone silently vacuous -- 121 guard
  checks reporting green while running zero. When you add a promote, register its SHA in
  `promote_fixture.COMMIT_FOR` (if committed) or `CHAIN`.
- **Release gauntlet:** `whole_crop_gate` + `gate_all.py` + `release_verify` + the five standalone
  gates (`calendar_coherence_gate`, `harvest_duration_gate`, `numeric_sanity_gate`,
  `cross_consistency_gate`, `soil_temp_floor_scan`). For `release_verify`, diff the CONCERN set
  against the **pre-state** rebuilt from `promote_fixture` -- identical means no new violations.
- **State trio every release:** amend `CURRENT_STATE.md` surgically (never regenerate -- the
  generator drops the 74KB locked-decisions block), append `STATE_HISTORY.md` most-recent-first,
  bump `LATEST.txt`.
- **Canonical is COMPACT**: `separators=(",",":")`, `ensure_ascii=False`, no trailing newline.
- **Don't commit until Trevor approves; he confirms every push separately.**
- **Do not run two sessions in one checkout.** Canonical moved under this session mid-task on
  2026-07-30; the SHA guard caught it, but only after the time was gone. Use worktrees, or
  parallelize the *reading* and serialize the *writing*.

---

## 7. The habit that mattered most

Four times on 2026-07-31 a confidently stated plan was wrong, and each was caught the same way --
by opening the thing before acting on it:

1. The roster-wide bloom declaration would have written a false statement onto 66 cells.
2. "Fix lettuce-leaf's 58 mismatches" was work on a layer already ruled leave.
3. "Remove the 57 null URLs" would have orphaned 54 source ids and destroyed a deliberate record.
4. "Fix the 8 NPK defects" would have rewritten **six correct crops** to match a broken matcher.

None of these were caught by a gate. All were caught by reading the data the record described.
**A count is a question. Read the finding before you act on it.**

**Four more on 2026-07-31, in the cleanup-batch session, same cause every time:**

5. `ucr_citrus`, "the cheapest real closure", rested on **"Riverside IS `ca_interior`"** -- false by
   our own `zone_frost_data`, which puts Riverside with LA, San Diego and Long Beach. The sentence
   had propagated verbatim into three kickoffs from one observation on a single mandarin accession.
6. "Fix the 74 SUIT contradictions" would have **flattened the region model** -- those cells rate
   one zone differently across regions because the regions genuinely differ.
7. "Berries warn nobody" was overstated: **20 of the 23** under-chill cells already warn in prose.
   The real gap is machine-readability, which is a different and smaller argument.
8. A handoff **I wrote in that same session** claimed a lavender cell was clean and offered it as
   the target shape for a fix. Opening it before shipping showed a second UAEX attribution the
   scan had never flagged -- and the worklist went from 8 sentences to 10 in 7 cells.

**And a fifth habit the session added: MUTATION-TEST YOUR GUARDS.** Three promote-guard tests were
green and vacuous, each passing for the wrong reason because an EARLIER check caught the sabotage
first. Delete each check in turn and confirm a test fails; assert on the abort MESSAGE, not just
the exit code. A guard that has never been shown failing is not yet a guard.

---

## 8. Revision log for this file

- **2026-07-31 (audit-response session):** written.
- **2026-07-31 (cleanup-batch session):** header corrected twice (it was 3 commits stale within a
  day); §3 readings re-measured and three of the five contradiction families adjudicated; §4
  rewritten -- `ucr_citrus` withdrawn, hunts corrected 30 -> 32, the California cluster named as the
  densest remaining prize, berry chill split into three separable pieces, the asparagus line
  corrected and 5 of its 7 fields fixed, the pumpkin repoint and the 3 contradicted shapes marked
  stale; §5 gained the cleanup-batch closures and a qualification on the template-inheritance line;
  §7 gained four more caught-wrong-plans and the mutation-testing habit. **Kickoff 49 now carries
  the next concrete unit of work.**
