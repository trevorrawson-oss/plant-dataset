# CAMPAIGN A — the UC ANR / UC Master Gardener California hunt

> **This is campaign A of four.** It is the arc's biggest single block, not the whole arc. The other
> three campaigns (B region templates, C arid+Texas, D the tail) are briefed in
> **`docs/citation_arc_hunt_ledger.md`**, which is the arc-level tracker. **§6 of this document is
> the SHARED PROTOCOL for all four campaigns** — B, C and D point back here rather than restating it.

**Written:** 2026-08-03, at the close of the herb-attribution session.
**Canonical:** `38a579d4c3e92e470892c9c992215de750f14f5bad02107d6cfc790ebdecc93a`
**HEAD:** `c2281f5` on `main`, **pushed and in sync with origin.** 128 crops / 121 certified.

> **Re-verify this header before trusting it.** Kickoff 48's was three commits stale within a day,
> and kickoff 49's was one commit stale within two. Run §1 rather than believing these numbers.

---

## 1. Verify state first (60 seconds, non-negotiable)

```bash
cd ~/plant-dataset
shasum -a 256 crops_data_final.json     # must equal LATEST.txt
git log --oneline -1                    # expect c2281f5
git status -sb                          # expect clean, in sync with origin/main
python3 -m pytest tools/ -q --ignore=tools/test_build_berry_pilot_patch.py   # expect 364 passed
```

`test_build_berry_pilot_patch.py` breaks pytest **collection** (module-level `sys.exit(0)`).
Pre-existing. Ignore it.

Three untracked items are **not yours**: `.claude/`, `tools/staging/shards/`,
`docs/2026-07-29-establishment-path-encoding-question.md`.

---

## 2. Why this block, and why now

Measured fresh on 2026-08-03 with `tools/citation_provenance_scan.py --decisions`:

| | |
|---|---|
| SOLE bare-host pairs remaining | **614** |
| distinct SOLE nodes | 414 |
| distinct (crop, region, source) **DECISIONS** | **167** |
| distinct (region, source) **DOCUMENT HUNTS** | **32** |

The eight California UC hunts are **76 of those 167 decisions — 46% of everything left in the arc**:

| region | source | decisions |
|---|---|---|
| `ca_interior` | `ucanr_ext` | 11 |
| `ca_north_coast` | `ucanr_ext` | 10 |
| `ca_south_coast` | `ucanr_ext` | 10 |
| `ca_desert` | `ucanr_ext` | 10 |
| `ca_interior` | `uc_mg` | 9 |
| `ca_north_coast` | `uc_mg` | 9 |
| `ca_south_coast` | `uc_mg` | 9 |
| `ca_desert` | `uc_mg` | 8 |

Nothing else in the arc comes close: the next biggest are `mid_south`/`uada_ext` (20) and
`mid_atlantic`/`ncsu_ext` (13). **Clear this and the arc is roughly half done in one campaign.**

> **The per-hunt status of all 32 lives in `docs/citation_arc_hunt_ledger.md`** — the one durable
> record of what is open vs closed. Read it alongside the live scan, and **update it when a hunt
> closes.** Note it corrects the live number: 9 decisions across 4 `ucr_citrus` hunts are already
> closed by ruling but still counted, because a CASE 2 ruling leaves the bare-host citation in
> place by design. Genuinely open is **158 decisions / 28 hunts**, not 167 / 32.

### ⚠ FIRST TASK: RECONCILE THE COUNT. A COUNT IS A QUESTION.

An independent hand traversal run in the same session (SOLE = `len(sources) == 1`, walking region
root + `resolved_by_zone` + `plantings`) produced a **different distribution**: 77 decisions over
**7** hunts, with `ca_desert`/`uc_mg` at **2** where the tool says **8**, and `ca_south_coast`/
`ucanr_ext` at **21** where the tool says **10**. The union of crops touched was **25**.

**Do not start hunting until these agree.** Read `tools/citation_provenance_scan.py` and find which
node types and which SOLE definition it uses. The tool is the shipped authority and is probably
right, but *"probably right"* is how this arc got mis-priced 4-20x once already
([[citation-arc-repriced-by-decision-unit]]). Whichever is correct, the other is a bug worth fixing
before it prices a campaign.

---

## 3. The evidence already gathered — do NOT redo this

> **[CORRECTION 2026-08-03 — §3's table of "4 authoring decisions" is TWO-THIRDS STALE. Re-measured
> against canonical `38a579d4`; working in
> `docs/2026-08-03-campaign-a-count-reconciliation-and-readjudication.md`.]**
>
> - **Row 2 (pumpkin desert, "the one real DATA-defect candidate") NO LONGER EXISTS.** The quoted
>   `Jan 15 - Feb 15` was corrected twice — to `Feb 1 - Mar 1`, then re-derived to **`Mar 1 - Mar 15`**
>   — and `pumpkin_desert_spring_march_rederivation` is marked **`resolved`**. This kickoff quotes a
>   value two revisions stale, which is the failure CLAUDE.md's re-verify rule exists to catch.
> - **Row 1 (winter-squash desert 2nd planting) IS CLOSED BY RULING, and this row recommends the move
>   the ruling REFUSED.** `ca_desert_fall_cycle_provenance_gap` is **`accepted`**, and its basis says:
>   *"AZ1005 is cited here as a CLIMATIC ANALOGUE for the Sonoran low desert, explicitly NOT as a
>   California source — trimming a Californian window to its marks would be the geography stretch the
>   arc warns about."* Do **not** repoint these at AZ1005.
> - **Rows 3 and 4 (okra) are LIVE and are the whole of the block's authoring risk** — `ca_desert`
>   z10/z11 `Mar 1 - Apr 30`, z9 `Mar 15 - Apr 30`; `ca_north_coast` z9 `Jun 1 - Jun 30`.
>
> **So the risk in this block is 2 authoring decisions, not 4.** Also missed at pricing time: **12 of
> the 76 decisions have no UC row at all** — the target page is a *vegetable* table and 6 of the 14
> crops are citrus, tree fruit, arugula or edamame. The original text below is left byte-for-byte.

**Read `docs/2026-07-29-citation-cleanup-sample-pass-outcome.md` first, INCLUDING its correction
banner** (its §4 row 18 "Riverside is `ca_interior`" is false and `ucr_citrus` is withdrawn).

### The target document is already identified

`https://ucanr.edu/program/uc-master-gardener-program/time-planting` — "Recommended planting dates
for major regions of California", the *California Master Gardener Handbook* Table 13.2. It is
**already the most-cited pathed URL for BOTH `uc_mg` (126 uses) and `ucanr_ext`**, so prior passes
already treat it as the canonical UC planting-date table. Its region definitions map cleanly onto
ours, verbatim from the page:

> "North and North Coast = Monterey County north; South Coast = San Luis Obispo County south;
> Interior Valleys = Sacramento, San Joaquin, and similar valleys; Desert Valleys = Imperial and
> Coachella Valleys."

### The correctness question is ALREADY ANSWERED — this is the good news

92 California windows were adjudicated against that table on 2026-07-29:

| verdict | n | share |
|---|---|---|
| SUPPORTED | 39 | 42% |
| DIVERGENT | 35 | 38% |
| **CONTRADICTED** | **18** | **20%** |

**DIVERGENT IS NOT A DEFECT CLASS.** The document states its own dates are *"only approximate"* over
large areas, which absorbs all 35. Treating them as a worklist would manufacture 35 defects. This is
`gate-findings-must-be-read-not-counted` applied to that pass's own output.

**The 18 CONTRADICTED collapse to 4 authoring decisions**, and three already have answers:

| # | shape | cells | verdict already reached |
|---|---|---|---|
| 1 | winter-squash desert 2nd planting | 9 | **citation defect, data defensible** — AZ1005 shows Jul 1/Jul 15/Aug 1 in the low desert |
| 2 | pumpkin desert windows | 5 | **the one real DATA-defect candidate** — the `Jan 15 - Feb 15` main window is unsupported by UC *and* AZ1005 |
| 3 | okra desert | 3 | **citation defect, data defensible** — AZ1005 gives `Mar 15 - May 15`; the UC row is coarse |
| 4 | okra north coast z9 | 1 | **not independently checked** — the only genuinely open one |

So the risk in this block is **4 authoring decisions, not 76 unknowns**. Shapes 1 and 3 are the
`unr_fs0261` shape: a real land-grant document cited for a window it places elsewhere.

---

## 4. Method

1. **Reconcile the count** (§2) before anything else.
2. **Read from raw bytes.** `urllib` + `pypdf`, reusing `doc_mentions_crop_scan.extract()`. Never a
   WebFetch summary as evidence, and never a WebFetch markdown parse of an HTML **table** — that
   silently shifts columns ([[webfetch-markdown-table-column-shift]]). This block is *entirely* a
   table-reading exercise, so that trap is live on every row.
3. **Adjudicate per crop-decision, never as a group.** CASE 1 = repointable at a real document;
   CASE 2 = the claim is unsourced and becomes a CONTENT finding.
4. **One ruling per promote.** A citation repoint and a window change never ride together — which
   means shape 2 (pumpkin) is its own promote, separate from shapes 1 and 3.
5. **Batch by hunt, not by crop.** Each of the 8 hunts is one document read against N crops.

---

## 5. Traps specific to this block

- **`DIVERGENT` is absorbed by the source's own caveat.** Do not work those 35.
- **A pathed URL for another crop does not support THIS claim.** The scan's own caveat: the document
  being recorded somewhere makes the *hunt* cheap, not the *answer* free. Never mass-repoint.
- **Check `source_catalog` before judging a source** ([[source-catalog-is-the-admission-authority]]).
- **Match the taxon, not the common name** ([[match-the-taxon-not-the-common-name]]) — the herb hunt
  found UAEX's only zone-bearing "rosemary" page was *Salix elaeagnos*, a willow.
- **Absence is document-scoped.** Say which documents you read.
- **`ucr_citrus` is WITHDRAWN** (kickoff 48 §4). Its 33 SOLE pairs are CASE 2, already adjudicated.
  Do not re-propose it.
- **`SUIT` (74) and `TYPE` (11)** in the contradiction scan remain LOW value — they flag one zone
  rated differently across regions, which is the region model working as designed.

---

## 6. Protocol (binding — unchanged from kickoff 49, which it worked well for)

- Promote only via a **guarded script** pinning the pre-state SHA, asserting exact prior values,
  proving an exact footprint, aborting on drift. Current best pattern:
  `tools/promote_mid_south_herb_hardiness_attributions.py`.
- Guard fixtures **rebuilt** via `promote_fixture.scratch(BASE_SHA, mutate)`, never copied from live
  canonical. **Register `38a579d4` in `promote_fixture.COMMIT_FOR` -> `c2281f5`** — it is committed
  and pushed, so it belongs in `COMMIT_FOR`, not `CHAIN`.
- **MUTATION-TEST YOUR GUARDS.** Delete each check in turn; if no test fails, it is not a guard. The
  herb pass found **3 of 16 vacuous on the first try** (fourth occurrence in three days). Two
  techniques that made the unreachable ones testable, both reusable: patch `copy` with a shim that
  doctors ONLY the first `deepcopy` (the `before` snapshot) to simulate a change the edit loop never
  made, and patch `json` with a `dumps` that appends a newline for the write-time guards.
  **Pin abort MESSAGES, not exit codes** — overlapping guards make exit-code assertions vacuous.
- **Refuse to write a reason naming a source the arm does not carry**
  (`promote_apple_mid_atlantic_bloom_reason.py`, reused in the herb promote).
- **Release gauntlet:** `whole_crop_gate <slug>` on each touched crop (**positional slug, not
  `--slug`** — the wrong form throws `FileNotFoundError` and reads like a gate failure) +
  `gate_all.py` + `release_verify.py <candidate> --base <pre-state>` diffed against a baseline run +
  the five standalone gates (`calendar_coherence_gate`, `harvest_duration_gate`,
  `numeric_sanity_gate`, `cross_consistency_gate`, `soil_temp_floor_scan`), each byte-compared to a
  pre-state capture.
- **State trio:** amend `CURRENT_STATE.md` surgically (never regenerate — the generator drops the
  74KB locked-decisions block), append `STATE_HISTORY.md` most-recent-first, bump `LATEST.txt`.
- **Canonical is COMPACT:** `separators=(",",":")`, `ensure_ascii=False`, no trailing newline.
- **Don't commit until Trevor approves; he confirms every push separately.**
- **NO plant-astro bump.** Trevor ruled 2026-08-03 that the bump is **batched to the end of the
  whole cleanup arc**, not owed per commit. Don't raise it.

---

## 7. What's left after this block — this kickoff is NOT the whole arc

**Kickoff 50 is ONE campaign of four.** It covers the largest block; it does not close the arc.

Naive arithmetic says 167 - 76 = 91 over 24 hunts. **That is wrong**, and wrong in exactly the way
this arc keeps getting wrong: it re-counts the 9 decisions / 4 hunts already closed by ruling.
Against the genuinely-open 158 / 28, this block leaves **82 decisions over 20 hunts**. The full
four-campaign breakdown lives in `docs/citation_arc_hunt_ledger.md`. The largest remaining pieces:

- `mid_south`/`uada_ext` **20** — partially worked. Hunt 1 did the fruit crops; the 2026-07-31 herb
  pass removed 10 false credits from *prose* but **deliberately did not repoint the citations**, so
  all 10 herb cells still cite the bare host. `lavender` has the one identified real repoint target
  (its UAEX Plant of the Week URL) and a filed finding explaining what must change with it.
- `mid_atlantic`/`ncsu_ext` **13** — and note `rosemary_mid_atlantic_ncsu_zone_attribution` is
  already filed here: NC State's Toolbox gives *Salvia rosmarinus* as 8a-10b while our prose says
  "zone 7 to 8". The number is sound (our own hardy-cultivar floor); the credit overstates.
- `warm_arid`/`nmsu_ext` **9**, `warm_arid`/`tamu_agrilife` **9**, `rgv`/`tamu_agrilife` **6**,
  `low_desert_az`/`uariz_ext` **6**.

Also still open and NOT part of this arc: `DATES` (35) in the contradiction scan; 9 orphan anchors;
the `lavender`/`hawaii_tropical` `westhawaiitoday.com` anchor whose source id is **not in
`source_catalog` at all**; pole-beans' 50-day harvest against a stated 60-day minimum DTM;
`version` still `1.0`; the `npk_ratio` 5-10-10 question on the five tomatoes.

**Blocked on plant-astro:** elderberry's chill reclassification, the 11 real blackberry/raspberry
under-chill cells, and the berry `suitability` field addition.
