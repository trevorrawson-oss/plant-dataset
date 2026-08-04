# CAMPAIGN C — arid + Texas

**Written:** 2026-08-04, at the close of the session that finished campaign B.
**Arc tracker:** `docs/citation_arc_hunt_ledger.md`. **Protocol:** kickoff 50 §6, campaign-agnostic.
**Prior campaigns:** A closed 2026-08-03; B closed 2026-08-04 (docs
`2026-08-03-mid-atlantic-ncsu-ext-citation-hunt.md`, `2026-08-04-campaign-b-closeout-hunt.md`).

> **This document will go stale, and every kickoff in this arc has.** The numbers below were
> MEASURED on 2026-08-04 against canonical `4065e23b`. Re-measure before believing any of them.
> Section 2 exists because kickoff 51 asserted two adjudication claims inside a "do NOT redo this"
> heading and both were wrong.

---

## 1. Start state — VERIFY, DO NOT TRUST

| | |
|---|---|
| canonical | `4065e23bf7cbfd2945c476c93e7326e9a6d2f0646ac88bac9a66f7b9d857023e` |
| HEAD | `6eec0fd` on `main` |
| pushed? | **YES — pushed 2026-08-04, in sync with `origin/main`** |
| suite | **566 passed** |

```bash
cd ~/plant-dataset
shasum -a 256 crops_data_final.json          # must equal LATEST.txt
git log --oneline -6 && git status -sb
python3 -m pytest tools/ -q --ignore=tools/test_build_berry_pilot_patch.py
python3 tools/bare_host_scan.py --sole
```

`test_build_berry_pilot_patch.py` breaks pytest **collection** (module-level `sys.exit(0)`).
Pre-existing, ignore. Untracked `.claude/`, `tools/staging/shards/`,
`docs/2026-07-29-establishment-path-encoding-question.md` and
`PLANT_AI_SYNC_ANSWERS_2026-08-04.docx` are **not yours**.

> **Do NOT amend or rebase at or below `bc5250d`.** `promote_fixture.COMMIT_FOR` now pins five
> canonical SHAs to commits, including `370806b5 -> 4a2f3ec`, `47a502af -> 18687d5` and
> `4065e23b -> be3abea`. Breaking any of them makes promote guards **SKIP while reporting green**.

---

## 2. TASK ONE: re-price. Do not skip it.

`tools/campaign_b_reprice.py` is the model. **Generalize it or copy it — do not hunt first.**
Re-pricing has paid off every time it has been run: campaign A 76 → 9, campaign B 33 → 6 → 0.

But campaign C's answer will be **different in kind**, and the difference is the single most
important thing in this document:

**Campaign B collapsed because most of it was already adjudicated. Campaign C is not.**
Measured 2026-08-04: **0 of 35 decisions carry any finding naming their region.** Nothing here is
pre-ruled. Do not expect a B-style collapse from reclassification — C's 35 is real work.

What WILL shrink it is the two structural facts in §4, which are worth more than any reclassification.

---

## 3. The measured shape

**35 decisions, 116 SOLE nodes** (2026-08-04, canonical `4065e23b`).

| # | region | source | dec. | nodes | crops |
|---|---|---|---|---|---|
| 7 | `warm_arid` | `nmsu_ext` | 9 | 18 | acorn-squash, banana-pepper, bell-pepper, butternut-squash, cayenne-pepper, eggplant, okra, pumpkin, spaghetti-squash |
| 8 | `warm_arid` | `tamu_agrilife` | 9 | 17 | the same 8, less cayenne, plus **lemon** |
| 13 | `rgv` | `tamu_agrilife` | 6 | 30 | arugula, broad-beans-fava, garlic, shallot, snow-peas, sugar-snap-peas |
| 14 | `low_desert_az` | `uariz_ext` | 6 | 32 | cantaloupe, honeydew-melon, okra, watermelon, **lemon**, **lime** |
| 17 | `warm_arid` | `nmsu_donaana_mg` | 2 | 2 | beefsteak-tomato, heirloom-tomato |
| 21 | `ca_desert` | `uariz_ext` | 2 | 16 | **lemon**, **lime** — nothing else |
| 24 | `warm_arid` | `nmsu_chart` | 1 | 1 | carrot |

**Node class: 82 of the 116 are CONTAINERS** (56 `resolved_by_zone`, 25 `plantings[]`, 1
`heat_pause`); only **34 are CLAIM arms** (10 `plant_out`, 10 `harvest_start`, 10 `harvest_end`,
4 `bloom`). That ratio is the opposite of campaign B's and it changes the work: a container asks
"which document represents this region's planting model", not "what supports this date". Campaign B
proved that is a cheaper and different question. **Price them separately or you will overstate this
campaign by roughly 3x.**

Every hunt cites exactly **one** bare URL, so the per-decision URL map is safe here — but verify it
rather than inheriting this sentence. Campaign A's preflight aborted a promote because two crops'
"bare `ucanr_ext`" were different sites.

---

## 4. Two structural facts that should reshape the campaign

### 4a. Lemon and lime are 27% of campaign C, and they belong to campaign D

Measured: **lemon 16 nodes across 3 C hunts, lime 15 nodes across 2** — **31 of the 116**. And
**hunt #21 (`ca_desert`/`uariz_ext`) is 100% citrus**: two crops, both of them lemon and lime.

Campaign D is already **7 of 11 hunts lemon**, and campaign A explicitly deferred its own
`lemon` 4 + `lime` 3 residue there. Working citrus here means reading the same documents twice and
adjudicating the same crop against two different campaign ledgers.

**Recommendation: move hunt #21 wholesale to campaign D, and defer the lemon/lime rows inside #8
and #14 with it.** That leaves campaign C as **30 decisions / 85 nodes** of genuinely arid
vegetable and cucurbit work, and gives campaign D a single coherent citrus sitting. Update the
ledger's campaign table if you take this.

### 4b. Eight `warm_arid` crops cite BOTH bare hosts, so one read closes two hunts

acorn-squash, banana-pepper, bell-pepper, butternut-squash, eggplant, okra, pumpkin and
spaghetti-squash appear in **both** #7 (`nmsu_ext`) and #8 (`tamu_agrilife`). Those cells cite two
domain roots and nothing else, which is why both rows read SOLE.

Two consequences, and the second is a measurement trap:

1. A single `warm_arid` read of the NMSU and TAMU documents adjudicates **17 of the 35 decisions**.
2. **Repointing ONE of the two makes the other stop being SOLE.** The moment a real document lands
   on a cell, the remaining bare row becomes *corroborated*, not sole. So the SOLE count will fall
   by far more than the number of nodes you actually repoint. Do not read that drop as progress on
   the other hunt, and do not let a re-price tool count it as adjudication — it is a citation-shape
   change, not an evidence change.

---

## 5. Documented traps — RE-VERIFY EACH, they are records

Both are recorded in memory and in the ledger, and this arc has now been burned three times by
acting on a record without re-reading the thing it describes.

- **AZ1005's grid is 90° rotated.** The Arizona planting calendar's table axes are not what a
  naive parse assumes. Re-read from raw bytes before extracting a single date.
- **NMSU CR457B publishes no planting-date window at all.** It was located, correctly, and then
  cited for a claim it does not contain. Locating the right document is not the same as supporting
  the claim.
- **Never parse an HTML data table through WebFetch's markdown conversion.** It silently shifts
  columns and yields a plausible, wrong grid. Use `urllib` + the extractor in
  `tools/doc_mentions_crop_scan.py`, or `pypdf`, and cross-check against a second source.
- **A fetch failure is UNDETERMINED, never absence.** Campaign B hit an HTTP 403 on one NC State
  publication while the same host served three other URLs at 200 in the same run. Record it as
  unreadable and say how many documents were actually read.

---

## 6. Lessons campaign B paid for, in priority order

1. **A record's SCOPE is narrower than its surface suggests**, and that includes the tools. `campaign_b_reprice` itself went stale twice in two days — once on a finding-id spelling convention (`mid_atlantic` uses REGION-FIRST, `mid_south` SLUG-FIRST), once on a rule that was true when written. Assert every adjudication claim is PRESENT on that crop, mechanically.
2. **When a check floods, narrow the CHECK, and suspect your own arithmetic first.** Every large number in this arc has been a measurement artifact.
3. **A guard that cannot fail is not a guard.** Twelve were removed or rebuilt across campaign B. The subtlest: a guard whose expected set is DERIVED from the thing it validates (see `guard-derived-from-what-it-checks-is-vacuous`). Mutation-test every guard by neutering each `if` in turn; pin abort MESSAGES, not exit codes.
4. **Verify where prose RENDERS before writing it, and fix EVERY field carrying a claim.** A fabricated UAEX credit was corrected in `plantings_provenance` (renders nowhere) and survived a full day in `grown_as_note_seasoned` (renders today). `suitability_note_*` → `HardinessFruitingCard.astro`; `grown_as_note_*` and `frost_risk_note_seasoned` → `BerryYearCalendarCard.astro`; `region_notes_*`, `planting_note`, `zone_notes`, `notes` render **nowhere**.
5. **Do not swap one unsourced model for another.** Three campaign B divergences were declared modeled on this principle rather than retuned against weaker evidence.
6. **A proportional penalty is advice, not a deadline.** Before narrowing any window to exclude a measured loss, ask what a reader who cannot hit the narrowed window will do.

---

## 7. Protocol

Kickoff 50 §6, unchanged: guarded promote pinning the pre-state SHA and asserting exact prior
values; fixtures rebuilt via `promote_fixture.scratch`, never copied from live canonical;
**mutation-test every guard**; the release gauntlet (`whole_crop_gate <slug>` positionally on each
touched crop + `gate_all` + `release_verify` diffed against a baseline run + the standalone gates
byte-compared to a pre-state capture); the state trio (`CURRENT_STATE.md` amended **surgically**,
`STATE_HISTORY.md` appended most-recent-first, `LATEST.txt` bumped); canonical stays COMPACT.

**Trevor approves every commit and confirms every push separately.** Register each new canonical
SHA in `promote_fixture.COMMIT_FOR` in its own follow-on commit — the hash cannot exist until the
data commit does, and amending to fold it in is what breaks the fixtures.

**No plant-astro bump.** Trevor ruled 2026-08-03 that it is batched to the end of the whole cleanup
arc. Don't raise it.

---

## 8. Still owed elsewhere, not blocking

- **`strawberry_mid_south_plasticulture_home_garden_tension`** is campaign B's one deliberately
  open finding: two T1 UAEX documents disagree about whether the annual plasticulture system
  belongs in a home garden. Trevor's ruling, not a sourcing fix. A guard in
  `promote_campaign_b_rulings.py` pins it open so it cannot be closed as tidy-up.
- **29 nodes across campaign B stay on a bare host BY DESIGN**, each with a filed reason.
  `bare_host_scan` will keep reporting them. That is correct, not residue.
- The `frost_anchor_reproduction_gate` hard-flip; wiring `region_notes_*` in plant-astro; the
  61 unread anchor-reproduction leads; the desert fruit-set arc.
