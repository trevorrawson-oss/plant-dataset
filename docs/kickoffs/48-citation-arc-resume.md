# Citation-integrity arc — RESUME HERE

**Written:** 2026-07-31, at the close of the audit-response session.
**Canonical:** ~~`8d2b1a91…`~~ **`172e4e7af950f0b98bf7883f5386c2b701a9d88f4d4347fc30d520cce7e91298`**
(updated 2026-07-31 by the zone-lift prose de-zone, `8f7321c`).
**HEAD:** ~~`362942d`~~ **`7092ca1` on `main`, COMMITTED but NOT PUSHED (origin is 2 behind).**
128 crops / 121 certified.
**Re-verify before trusting this header** -- it was 3 commits stale within a day of being written,
which is the same failure mode this document warns about in §7.
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
git log --oneline -1                    # expect 362942d
git status -sb                          # expect clean, in sync with origin/main
python3 -m pytest tools/ -q --ignore=tools/test_build_berry_pilot_patch.py   # expect 274 passed
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

**Current readings** (re-measure; do not quote these):

- `internal_contradiction_scan`: **178 contested cells** -- CHILL 34 (23 UNDER / 11 OVER), TYPE 11,
  DATES 35, TEMPLATE 24, SUIT 74. NPK is **0**.
- `citation_provenance_scan`: 614 SOLE pairs / 414 nodes / **167 decisions / 32 hunts**.
- `doc_mentions_crop_scan`: CROP-LIST-omits-crop **356 nodes / 214 decisions**; REFERENCE 107 / 27.

> **178 IS NOT A DEFECT COUNT.** Four separate times on 2026-07-31 a raw count was mostly artifact,
> **twice in tools written that same day**. Treat every number above as a question.

**Both cached scans take `--refetch-unreadable`.** Use it. 15 of 631 cached documents were WAF
challenge pages served as HTTP 200 or PDFs with no text layer, and both scans read them as
*absence*, manufacturing defects from pages nobody had read.

---

## 4. Open work

**The one needing a ruling before anything else.** **Berries carry no `suitability` field at all.**
All 23 UNDER-chill cells sit on `suitability: None`, because the category has no such field. We
recommend `american_elderberry` -- 400 chill hours, the **only** type we list, no low-chill
alternative -- into Hawaii and south Florida zones banking **0-150** hours, with nothing able to
warn anyone. Same shape as blueberry. This is a **cross-crop field addition**
(`docs/gs_cross_crop_field_addition_v0.md` + `field_addition_register.md`), not a promote.

**Citation arc proper:**
- 30 hunts / 167 decisions remain. Schedule them by §2.
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
- The held-back `ca_desert` pumpkin repoint (now clean).
- 3 citation-only contradicted shapes (winter-squash Jul-vs-Aug; okra `ca_desert`; okra
  `ca_north_coast` z9).
- `pole-beans`: harvest starts 50 days after sowing against a stated min DTM of 60, identically in
  every region. One modeling question, not 20 cell errors.

**Mechanical residue (small):**
- **9 orphan anchors** in LIVE subtrees -- the reverse shape from the zone-layer ones: an
  `anchoring_urls` entry with **no matching source id**. `lavender` 4 (`osu_ext_prune_lavender`),
  `basil` 2 (`uariz_ext_az2061`), 3 tomatoes (`ucd_postharvest` on `yield_expectations`).
- `lavender` / `hawaii_tropical` anchors on `westhawaiitoday.com`, a **newspaper**. Tier-bar call.
- The bloom slices: **138** arms where a declaration genuinely fits, **55** never-mentioned (defect
  candidates), **66** whose source actually publishes a date and could be repointed.

**From the external audit, still open and Trevor's call:**
- `launch_ready_core` is one Boolean over 121 crops, 62 of which carry an unfinished finding. The
  audit argues for a richer release status. It has a point.
- `asparagus` lacks 7 top-level fields the other 127 have -- a perennial-schema question, not an
  omission to backfill.
- `version` is still `1.0` after six canonical promotes. A data build id would make comparison and
  rollback safer.
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
