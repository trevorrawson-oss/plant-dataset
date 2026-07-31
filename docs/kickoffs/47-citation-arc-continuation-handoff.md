# Citation-integrity arc — CONTINUATION HANDOFF

> ### ➡️ SUPERSEDED 2026-07-31 — START AT `docs/kickoffs/48-citation-arc-resume.md`.
> This document's §2 correction banner and §4 lessons still stand. Its **numbers, verify block
> and worklist are stale** by 13 commits and six canonical promotes. The arc is NOT abandoned;
> 48 is where it resumes.


**Written:** 2026-07-30, at the close of the two-hunt session.
**Canonical at writing:** `45409cee` — **SUPERSEDED, see below.**
**CANONICAL NOW: `d77b9c5166896fa15a815ec25140d9531f966a592abc881fe528875647bb4590`**
(committed `610dad4`, HEAD `05f9213`, **4 commits ahead of `origin/main` -- NOT PUSHED**; 128 crops / 121 certified).

> ### ⚠️ CANONICAL MOVED AFTER THIS DOCUMENT WAS WRITTEN — RE-PIN BEFORE YOU PROMOTE.
> `45409cee` → `d5f83073` (Trevor ruled `mid_atlantic` sour cherry `fruits_reliably` →
> `marginal`; 6 edits + 1 finding on one crop). **Any promote script pinning
> `BASE_SHA = '45409cee…'` will now abort — correctly.** Re-pin it to `d5f83073…` after
> confirming the drift is only that ruling and nothing else.
**Supersedes the operational half of `docs/kickoffs/46-citation-integrity-cleanup-arc.md`.** That
document's §5 banner already corrects three of its own premises; this one corrects the plan.

**Run this in a FRESH session. Read §1 and §2 before touching anything.**

---

## 1. Verify state first (60 seconds, non-negotiable)

```bash
cd ~/plant-dataset
shasum -a 256 crops_data_final.json     # must equal LATEST.txt
git log --oneline -1                    # expect 05f9213
git status -sb                          # expect clean, synced with origin/main
python3 -m pytest tools/ -q --ignore=tools/test_build_berry_pilot_patch.py   # expect 244 passed
```

`tools/test_build_berry_pilot_patch.py` breaks pytest **collection** (module-level `sys.exit(0)`).
Pre-existing. Ignore it, or fix it the way `test_build_corn_family_patch` was fixed.

Expect three untracked items that are **not yours**: `.claude/`, `tools/staging/shards/`,
`docs/2026-07-29-establishment-path-encoding-question.md`.

---

## 2. THE PLAN CHANGED. Do not just "run hunt 3."

> ### ⛔ CORRECTION 2026-07-30 — ITEM 1 BELOW IS WITHDRAWN. DO NOT RUN IT.
>
> The premise licensing the roster-wide bloom declaration — *"no extension service publishes bloom
> dates"* — was **measured and falsified**. **22 documents at 12 institutions** publish
> month-granular bloom timing, and **66 of our own bloom arms already cite one of them** (apple ←
> `apples.extension.org`: *"will generally bloom in mid-April"*; NC State's own **Plant Toolbox**
> carries a structured `Bloom Time` field). Running the pass as written would have asserted *"the
> quantity is absent from the literature"* onto 66 cells whose cited document publishes it.
>
> Two hunts' **document-scoped** conclusions were widened to an institution, then to the whole
> literature. That is this document's own **lesson 2**, recurring at the level of the plan.
> What survives, narrowed: **no source publishes the offset-from-last-frost MODEL our schema
> stores** — a fact about our encoding, not about the literature.
>
> **Read `docs/2026-07-30-bloom-declaration-premise-falsified.md` before touching bloom.**
> New tool: `tools/bloom_datum_scan.py` classifies every cited document
> (`PUBLISHES_TIMING` / `MENTION_NO_DATE` / `NO_MENTION` / `UNDETERMINED`).
> The real worklist it found: ~~78~~ **55 undeclared arms whose every cited document never mentions
> bloom at all** — the `unr_fs0261` shape, a **defect** class, not a declaration class. (78 before the
> cache fix; **23 were phantom**, resting on pages nobody had actually read.)
>
> Also: there are **three** bloom encodings, not one (243 `offset`, 145 `month_literal`, 13
> `synthesis_window`). A declaration worded *"a modeled offset from the zone last-frost date"* is
> factually wrong on **158 of 401** arms.

The arc was scoped as **32 document hunts / 170 decisions**. Two hunts are done, and both
re-priced it. The headline:

> **Most of these citations cannot be repointed at any effort, because the extension literature
> does not publish the quantity our schema stores.**

Concretely: **no extension service publishes BLOOM DATES.** Confirmed independently at two
institutions — UAEX (hunt 1) and NC State (hunt 2, 31 mentions of "bloom", zero dates). Every tree
fruit stores `bloom[0] = {from: last_frost, offset_days, window_days}`. No hunt will ever find a
document for that.
<!-- ^ FALSIFIED 2026-07-30. Left byte-for-byte as the record of what was believed; see the
     correction banner above. Do not reason from this paragraph as current truth. -->

### The recommended order

1. ~~**ROSTER-WIDE BLOOM DECLARATION — do this first.**~~ **WITHDRAWN — see the banner above.**
   One documentation-only promote declaring the
   bloom offset as modeled across every crop that carries one. Two institutions already establish
   the absence; a third, fourth and fifth hunt rediscovering it is waste. Closes a large slice of
   the remaining 167 decisions in one pass. Precedent to copy: `mid_south_bloom_offset_undocumented`
   (13 crops) and `mid_atlantic_bloom_offset_undocumented` (10 crops), already in the data.
   **Replaced by:** a *classified* pass — declare only the 138 `MENTION_NO_DATE` arms, in wording
   that matches each arm's actual encoding; treat the 55 never-mentioned arms as defects; leave the
   documented ones alone and consider repointing them to the real datum.
2. **Then targeted hunts, driven by `doc_mentions_crop_scan`** (§3) — only where a document
   plausibly exists. The scan hands you the worklist; you no longer have to guess.
3. **Then the residue**, which is genuinely small.

**Estimate.** Done as 30 more hunts: **~14 sessions.** Done in the order above: **5–6.**
(The 2026-07-30 correction does not change these estimates much — the declaration slice shrinks,
but the 78-arm defect slice it uncovered is real work that was previously invisible.)

### And the real reason to keep going

The arc's yield has NOT been citations. It has been **user-facing data defects**, found because
locating a document forces you to read the cell against it:

| hunt | defects found |
|---|---|
| 1 (`mid_south`) | blueberry type inverted for z7; fig planted 3 months early; raspberry likewise; a **fabricated attribution** crediting UAEX with a recommendation it never published |
| 2 (`mid_atlantic`) | a **vegetable guide** as SOLE source for 14 fruit crops' windows |

Prioritise by *where we are most likely to be wrong*, not by bare-host count.

---

## 3. Tools — what exists and what each is for

| tool | question it answers | network |
|---|---|---|
| `tools/bare_host_scan.py` | which citations point at a bare domain root? | no |
| `tools/citation_provenance_scan.py --decisions` | how many real DECISIONS and HUNTS is that? | no |
| **`tools/doc_mentions_crop_scan.py`** | **does the cited document mention the crop at all?** | yes (cached) |

### `doc_mentions_crop_scan` — read this before using it

Built 2026-07-30 for a class **nothing else can see**: a real, live, correctly-titled document
cited for a claim it does not contain. `bare_host_scan` misses it (url is pathed),
`url_health_gate` misses it (returns 200), `whole_crop_gate` misses it (a source IS cited).

```bash
python3 tools/doc_mentions_crop_scan.py --candidates   # no network, sizes the work
python3 tools/doc_mentions_crop_scan.py --fetch        # ~10 min, cached in tools/.doc_cache (gitignored)
python3 tools/doc_mentions_crop_scan.py --report       # the findings
```

**Current reading, and it is a TRIAGE list, not a defect list:**

- `CROP-LIST omits this crop` — **356 nodes / 214 decisions.** Actionable. The `unr_fs0261` shape.
  **Re-measured 2026-07-30 after the block-page fix below: unchanged at 356 / 214, so this
  worklist is confirmed genuine.**
- `REFERENCE doc names ~no crops` — ~~155 nodes / 45 decisions~~ → **107 nodes / 27 decisions**
  (corrected 2026-07-30). A frost or chill table. Backs the derivation's *inputs*, never the claim.
  **Declare, do not repoint.**

> **CACHE FIX, 2026-07-30 — re-run the scans, do not trust pre-fix counts.** `load_doc` treated any
> cached body as the document. **15 of 631 cached documents were never actually read**: 14 WAF
> challenge pages that returned **HTTP 200** (so the `\x00` sentinel never fired — five are
> `canr.msu.edu`, cached as the 82-character *"Request unsuccessful. Incapsula incident ID…"*), and
> one PDF with no text layer (`naes.agnt.unr.edu` 2020-3713.pdf, 155 characters of glyphs, cited on
> **14 bloom arms**). Searching a body nobody read and finding no crop name **manufactures** a
> defect — the false-clear direction.
>
> Now fixed in the shared `unreadable_reason()` / `load_doc`, so **both** scans inherit it and
> report `UNDETERMINED`, never absence (lesson 7). Measured effect:
> `doc_mentions_crop_scan` FLAGGED **511 → 463**, UNDETERMINED **198 → 246** — all 48 came out of
> the REFERENCE class, which is why the actionable 356/214 is unmoved. `bloom_datum_scan`
> never-mentions-bloom arms **78 → 55 undeclared**, UNDETERMINED **17 → 40**: **23 of 78 bloom
> "defects" were phantom.**

**The actionable class splits AGAIN along a line no gate could draw**, and you must read it:

- **herbs and flowers on a vegetable table** → a **DECLARED convention**.
  `mid_south_sources.md` instructs exactly that and says to flag it. **Not a defect.**
- **fruit on a vegetable table** → a **real defect** (this is `vce_426_331`).

Identical mechanical signature, opposite disposition. That is why it ships as a scan a human reads
and **must never be hard-flipped into a gate.**

Of the 214 actionable decisions, **~91 are on crops that do not already declare** — that is the
real worklist.

---

## 4. Lessons paid for in blood. Do not relearn these.

1. **An existing source id proves the INSTITUTION was consulted, never that the DOCUMENT covers
   your crop class.** `mid_south` had a full citation vocabulary — a **vegetable** one. Mass
   repointing the fruit crops at it would have manufactured 22 defects in one commit, by the pass
   whose purpose is removing them.
2. **The same template can be right in one region and wrong in another.** NC State: plant fruit
   trees *late fall or early winter*. UAEX: *late winter*, **and not figs until early spring**. The
   identical `Dec - Feb` window is correct in `mid_atlantic` and wrong in `mid_south`. **Never
   generalize a regional planting correction beyond the authority that licensed it.**
3. **A table row that looks applicable may be scoped to a species you do not grow.** NC State's row
   is "Mulberry, **RED**" (*Morus rubra*). None of our varieties is red mulberry. Adopting its
   `May to June` would have made the cell wrong for **every** variety we recommend.
4. **The carve-out can live inside the sentence that licenses the rule.** *"Fruit trees other than
   figs, could be planted in the fall…"* — one sentence supported twelve crops and condemned a
   thirteenth. A grep for "fig" would have missed it; the crop appears only in the negative clause.
5. **Read findings, never count them.** Hunt 2's raw scan output was 519 — it looked like a flood
   and was three different findings wearing one signature.
6. **Suspect your own arithmetic and your own matcher.** Three bugs were caught by testing before
   the scan's output was trusted, **two of them silent false-CLEARS** (substring `fig` matched
   "Figure 1"; `green` from `green-beans-bush` cleared every document). A false clear HIDES a
   defect — the dangerous direction.
7. **An unfetchable URL is UNDETERMINED, never absence.** 21 of 621 failed; several `content.ces.
   ncsu.edu` pages 403 to urllib while others return 200.
8. **HTML tables column-shift** under flattened text. Parse real `<td>` cells. NC State's harvest
   table was read that way; `pawpaw` reads *"August to September or to first frost"* and a
   truncated view of that cell nearly produced a wrong verdict.
9. **WebFetch summaries are not sourcing.** urllib + pypdf, and re-extract every load-bearing
   sentence from raw bytes before relying on it.

---

## 5. Per-session protocol (unchanged, and it is binding)

- **Never mix a value change and a citation change in one promote.** Split them; each gets its own
  SHA-pinned guarded script.
- **Promote only via a guarded script** that pins the pre-state SHA, asserts the exact prior value
  of everything it touches, proves an exact footprint, and aborts on drift.
- **Adversarially TDD the guards on scratch copies before applying.** This session ran 21/21, 21/21,
  28/28, 21/21, 11/11, 19/19. The guard that matters most: **refuse to cite a document at a cell
  that contradicts it** — tested by reverting each fix in turn.
- **Release gauntlet:** `whole_crop_gate` + `tools/gate_all.py` + `release_verify` + the five
  standalone gates (`calendar_coherence`, `harvest_duration`, `numeric_sanity`,
  `cross_consistency`, `soil_temp_floor_scan` — the last is roster-wide, `gate_all` cannot reach
  it).
- `release_verify` **always** reports 1 CONCERN on a multi-crop change: it is single-crop-pilot
  shaped and expects only `cherry-tomato`. Confirm it names **exactly** your intended crops, then
  proceed.
- **State trio at every content release**: amend `CURRENT_STATE.md` surgically (do **not**
  regenerate — the generator drops the 74KB locked-decisions block), append `STATE_HISTORY.md`
  most-recent-first, bump `LATEST.txt`.
- **Canonical is COMPACT**: `separators=(",",":")`, `ensure_ascii=False`, no trailing newline.
- **Don't commit until Trevor approves; he confirms every push separately.**

---

## 6. Open and owed

**Hunt 2 is not finished.** Eight crops have no located document yet: `apricot`, `cherry-sour`,
`cherry-sweet`, `pomegranate`, `elderberry`, `blueberry`, `raspberry`, `strawberry`. The first four
were deliberately excluded from the handbook repoint — it names them only in passing risk language
or not at all.

**~~A question I owe Trevor a cleaner answer on.~~ RULED AND SHIPPED 2026-07-30** (`0015981`). `mid_atlantic` `cherry-sour` `fruits_reliably` -> `marginal`, both zones. Trevor revised his own 2026-07-20 call: the claim rested on a vegetable guide (z7) and NC State's homepage (z8), and the one pro-sour-cherry recommendation is Macon County, the western mountains, which this region excludes. Prose rewritten so `marginal` reads as odds, not discouragement.

**Surfaced 2026-07-30 and now CLOSED:**
- ~~`apple` / `mid_atlantic` bloom finding names a document the arm never cited~~ **FIXED** (`610dad4`). Trevor ruled by precedent: fix the stated reason, keep the conclusion. It rests on **geography**, not absence -- the page's figure is *western* NC and this region excludes the mountains.
- ~~`pawpaw` shares the structural defect~~ **FIXED in the same commit**, and it needed a *different* reason: its `psu_ext` page publishes nothing on bloom at all (15,361 chars, pawpaw named 15 times, zero bloom mentions), so pawpaw rests on **real absence**. Two crops, one shared wrong reason, two different right ones. **Never blanket a reason across crops whose citations differ.**
- ~~the shared `.doc_cache` reports unread pages as absence~~ **FIXED** (`1366a23`): `unreadable_reason()` + `--refetch-unreadable`. 23 of 78 bloom "defects" were phantom; the actionable 356/214 is unmoved and thereby confirmed.
- ~~six promote guard suites running zero checks~~ **FIXED** (`a8e50a5`): `tools/promote_fixture.py` rebuilds each pinned pre-state instead of copying live canonical.

**Still open from that day:**
- `lavender` / `hawaii_tropical` anchors on `westhawaiitoday.com`, a **newspaper**, not an extension service. A tier-bar question, not a citation-arc one.

**Carried from 2026-07-29, still open:**
- the 3 citation-only contradicted shapes (winter-squash Jul-vs-Aug; okra `ca_desert` Mar-Apr vs
  UC's coarse "May"; okra `ca_north_coast` z9 Jun vs "May");
- the held-back `ca_desert` pumpkin repoint (now clean — its window matches the pathed UC table);
- `ucr_citrus`, 33 pairs / 4 crops, one method (UCR CVC accession pages carry *"Season of ripeness
  at Riverside"*, and Riverside **is** `ca_interior`);
- pole-beans: harvest starts 50 days after sowing against a stated min DTM of 60, identically in
  every region — one modeling question, not 20 cell errors.

**Closed this session, do not re-investigate:**
- Template-inheritance risk is **bounded**. Only `mid_south` ← `mid_atlantic` used cell-template
  reuse, and all 52 of its institution-attributed claims were read (exactly 2 bad, both fixed).
  `utah_dixie` mirrors `warm_arid` for raspberry only; `rgv` reuses source ids, not cells.
- `mid_atlantic` blueberry is **verified correct** — NC State: *"rabbiteye blueberries are the best
  choice for most soils below 2,500 ft elevation in NC."* Do not "fix" it to match `mid_south`.
- `mid_atlantic` fruit **windows** are sound; 8 of 10 sit inside NC State Table 5. The defect there
  was the citation, and it is fixed.

---

## 7. Where the numbers stand

| unit | arc start | now |
|---|---|---|
| SOLE bare-host pairs | 681 | **614** |
| distinct SOLE nodes | 481 | **414** |
| decisions / document hunts | 170 / 32 | **167 / 32** (2 adjudicated) |
| new class: crop-list omits crop | — | 356 nodes / 214 decisions (~91 undeclared) |

The decision counter moves slowly **on purpose**. Most nodes end in *declare*, not *repoint*, and
that is the finding — not a failure to make progress.
