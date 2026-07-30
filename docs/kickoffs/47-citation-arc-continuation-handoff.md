# Citation-integrity arc — CONTINUATION HANDOFF

**Written:** 2026-07-30, at the close of the two-hunt session.
**Canonical at writing:** `45409cee243da4196e983198c33505701d44f50842ffb208a224d0b22ddd817b`
(**PUSHED**, `origin/main` = `d142eea`; 128 crops / 121 certified).
**Supersedes the operational half of `docs/kickoffs/46-citation-integrity-cleanup-arc.md`.** That
document's §5 banner already corrects three of its own premises; this one corrects the plan.

**Run this in a FRESH session. Read §1 and §2 before touching anything.**

---

## 1. Verify state first (60 seconds, non-negotiable)

```bash
cd ~/plant-dataset
shasum -a 256 crops_data_final.json     # must equal LATEST.txt
git log --oneline -1                    # expect d142eea
git status -sb                          # expect clean, synced with origin/main
python3 -m pytest tools/ -q --ignore=tools/test_build_berry_pilot_patch.py   # expect 210 passed
```

`tools/test_build_berry_pilot_patch.py` breaks pytest **collection** (module-level `sys.exit(0)`).
Pre-existing. Ignore it, or fix it the way `test_build_corn_family_patch` was fixed.

Expect three untracked items that are **not yours**: `.claude/`, `tools/staging/shards/`,
`docs/2026-07-29-establishment-path-encoding-question.md`.

---

## 2. THE PLAN CHANGED. Do not just "run hunt 3."

The arc was scoped as **32 document hunts / 170 decisions**. Two hunts are done, and both
re-priced it. The headline:

> **Most of these citations cannot be repointed at any effort, because the extension literature
> does not publish the quantity our schema stores.**

Concretely: **no extension service publishes BLOOM DATES.** Confirmed independently at two
institutions — UAEX (hunt 1) and NC State (hunt 2, 31 mentions of "bloom", zero dates). Every tree
fruit stores `bloom[0] = {from: last_frost, offset_days, window_days}`. No hunt will ever find a
document for that.

### The recommended order

1. **ROSTER-WIDE BLOOM DECLARATION — do this first.** One documentation-only promote declaring the
   bloom offset as modeled across every crop that carries one. Two institutions already establish
   the absence; a third, fourth and fifth hunt rediscovering it is waste. Closes a large slice of
   the remaining 167 decisions in one pass. Precedent to copy: `mid_south_bloom_offset_undocumented`
   (13 crops) and `mid_atlantic_bloom_offset_undocumented` (10 crops), already in the data.
2. **Then targeted hunts, driven by `doc_mentions_crop_scan`** (§3) — only where a document
   plausibly exists. The scan hands you the worklist; you no longer have to guess.
3. **Then the residue**, which is genuinely small.

**Estimate.** Done as 30 more hunts: **~14 sessions.** Done in the order above: **5–6.**

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
- `REFERENCE doc names ~no crops` — **155 nodes / 45 decisions.** A frost or chill table. Backs the
  derivation's *inputs*, never the claim. **Declare, do not repoint.**

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

**A question I owe Trevor a cleaner answer on.** `mid_atlantic` `cherry-sour` is `fruits_reliably`.
The NC State **statewide handbook** says *"Apricot and cherry trees … will not consistently bear
fruit"* and contains **no sour-cherry steer at all**. The one genuine *"we recommend apples, pears,
and sour cherries"* comes from **Macon County — the western NC mountains**, and `mid_atlantic` is
explicitly *"Piedmont and Coastal Plain"*. The sour-over-sweet **preference** is well supported;
*"fruits reliably in the Piedmont"* I have not found NC State saying. Trevor's 2026-07-20 ruling
predates this evidence. **Surface it, do not quietly change it.**

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
