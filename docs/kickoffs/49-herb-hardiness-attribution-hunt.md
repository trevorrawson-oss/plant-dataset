# Herb hardiness attributions — five UAEX lookups

> ## ✅ CLOSED 2026-07-31 — worked end to end. Do NOT re-run this hunt.
>
> All 10 attributed sentences fixed at canonical `c6f50a14` -> **`38a579d4`**. The credits are gone
> (measured: 0 University of Arkansas attributions remain in any `mid_south` cell of the five
> crops); every horticultural fact was kept.
>
> **Answers, per crop.** UAEX publishes **no** hardiness zone for thyme, rosemary, oregano or sage.
> **Lavender is the exception** and is the §4.5 "bigger find": UAEX *does* publish a range for
> *Lavandula angustifolia* — **"hardy from zones 5 to 8"** — which is **not** the "5a to 9b" we
> credited it with. Surfaced, not aligned.
>
> **The trap this hunt turned on:** the only UAEX page pairing a zone range with the word
> "rosemary" is *Willow Rosemary* — ***Salix elaeagnos*, a willow.** Match the binomial, never the
> common name.
>
> **Two findings filed for what was deliberately NOT fixed:**
> `lavender_mid_south_uaex_zone_range_divergence` and `rosemary_mid_atlantic_ncsu_zone_attribution`.
>
> Full evidence: **`docs/2026-07-31-mid-south-herb-hardiness-attribution-hunt.md`**.
> Narrative + gauntlet: the top entry of `STATE_HISTORY.md`.
> Promote: `tools/promote_mid_south_herb_hardiness_attributions.py` (guards 26/26, **16/16
> mutation-protected**).
>
> **The only thing outstanding is Trevor's commit + push approval.** §8 below is still live and is
> the right place to pick up next.

**Written:** 2026-07-31, at the close of the cleanup-batch session.
**Canonical:** `c6f50a1417a82786356fef764e524641143d41f973dc8f7097eb18454cb3fe5a`
**HEAD:** `a5ba1eb` on `main`, **pushed and in sync with origin.** 128 crops / 121 certified.

> **Re-verify this header before trusting it.** Kickoff 48's header was three commits stale within
> a day of being written. Run the block in §1 rather than believing these numbers.

---

## 1. Verify state first (60 seconds, non-negotiable)

```bash
cd ~/plant-dataset
shasum -a 256 crops_data_final.json     # must equal LATEST.txt
git log --oneline -1                    # expect a5ba1eb
git status -sb                          # expect clean, in sync with origin/main
python3 -m pytest tools/ -q --ignore=tools/test_build_berry_pilot_patch.py   # expect 338 passed
```

`test_build_berry_pilot_patch.py` breaks pytest **collection** (module-level `sys.exit(0)`).
Pre-existing. Ignore it.

Three untracked items are **not yours**: `.claude/`, `tools/staging/shards/`,
`docs/2026-07-29-establishment-path-encoding-question.md`.

---

## 2. The task, in one sentence

**Five herb crops credit the University of Arkansas with claims that appear to be NC State's —
a plant-hardiness range and a disease "plant profile" — and the citation behind every one of them
is a bare domain root.** Find out, per crop, whether UAEX publishes that datum. Where it does not,
remove the false credit without destroying the horticultural fact.

**10 attributed sentences across 5 crops / 7 cells.** Two of them sit in a cell the TEMPLATE scan
never flagged, which is why §3 tells you to measure rather than work from the scan's list.

This is the same defect class as the `cherry-sweet` fix on 2026-07-30: a mid_atlantic sentence
carried into `mid_south` with the institution name find-and-replaced.

---

## 3. The evidence already gathered — do not redo this

`internal_contradiction_scan --family TEMPLATE` reports **24**; deduped it is **21 distinct
pairs**, all `mid_atlantic` vs `mid_south`, all "NC State vs University of Arkansas". **All 21
were read on 2026-07-31.** Thirteen are CORRECT and are listed in §5 so you do not re-investigate
them. These ten sentences are the worklist:

| # | crop | cell | key | the attributed claim |
|---|---|---|---|---|
| 1 | `thyme` | `mid_south` z7 | `synthesis_note_seasoned` | "reliably hardy to about zone 5 (the University of Arkansas: **zones 5a to 9b**)" |
| 2 | `rosemary` | `mid_south` z7 | `grown_as_note_seasoned` | "hardy floor is about **zone 7** (the University of Arkansas)" |
| 3 | `rosemary` | `mid_south` z7 | `synthesis_note_seasoned` | "reliably hardy only to about **zone 7 to 8** (the University of Arkansas)" |
| 4 | `oregano` | `mid_south` z7 | `synthesis_note_seasoned` | "*Origanum vulgare* is hardy to about **zone 4** (the University of Arkansas Cooperative Extension)" |
| 5 | `sage` | `mid_south` z7 | `synthesis_note_seasoned` | "*Salvia officinalis* is hardy in roughly **zones 4 to 8** (the University of Arkansas)" |
| 6 | `sage` | `mid_south` z8 | `synthesis_note_seasoned` | "sage's stated **zone 4 to 8** ceiling (the University of Arkansas)" |
| 7 | `lavender` | `mid_south` z7 | `synthesis_note_seasoned` | "hardy to about zone 5 (the University of Arkansas Cooperative Extension: **zones 5a to 9b**)" |
| 8 | `lavender` | `mid_south` z7 | `synthesis_note_seasoned` | *(2nd sentence, same cell)* "the University of Arkansas's **plant profile** names root rot from overwatering and leaf spot as this species' main threats" |
| 9 | `lavender` | `mid_south` z7 | `grown_as_note_seasoned` | "the University of Arkansas's **own profile of the species** flags root rot from wet soil and leaf spot as the real threats" |
| 10 | `lavender` | `mid_south` z8 | `synthesis_note_seasoned` | "**zone 5 to 9b** hardy range (the University of Arkansas Cooperative Extension)" |

### THE SCAN IS A DETECTION AID, NOT THE BOUNDARY — read this before scoping

An earlier draft of this document asserted that `lavender` z7 `grown_as_note_seasoned` was CLEAN
and could serve as the target shape for the fix. **That was wrong, and it was caught by opening the
cell instead of trusting the note.** Its *hardiness* sentence is indeed clean — "English lavender's
hardy range (to about zone 5)", no institution — but the cell carries a **second, separate UAEX
attribution** in its humidity sentence (row 9 above), and the TEMPLATE scan never flagged that cell
at all.

So the real worklist is not "the pairs the scan found". It is **every UAEX-attributed sentence in a
`mid_south` herb cell**, measured directly:

```bash
# 10 attributed sentences across 5 crops / 7 cells -- measured 2026-07-31
python3 - <<'PY'
import json, re
d = json.load(open('crops_data_final.json'))
A = re.compile(r'(?:the )?University of Arkansas|UAEX|Arkansas Cooperative Extension')
for h in ('thyme','rosemary','oregano','sage','lavender'):
    c = {x['slug']: x for x in d['crops']}[h]
    r = (c.get('regions') or {}).get('mid_south') or {}
    for z, cell in sorted((r.get('resolved_by_zone') or {}).items()):
        for k, v in cell.items():
            if isinstance(v, str) and k.endswith(('_seasoned','_beginner')) and A.search(v):
                for m in A.finditer(v):
                    s = v.rfind('.', 0, m.start()) + 1
                    print(f'{h} z{z} .{k}\n   {v[s:v.find(".", m.end())+1].strip()}')
PY
```

Counts to expect: thyme 1, rosemary 2, oregano 1, sage 2, **lavender 4**. Re-run it rather than
trusting this table — and note the two lavender "profile" sentences are the strongest evidence in
the whole set, because "plant profile" / "profile of the species" is NC State Plant Toolbox
vocabulary describing a Plant Toolbox page.

### Why these and not the other thirteen pairs

**The tell is the contrast.** Twelve of the correct pairs are the chill-hours template, where the
author had a real Arkansas figure and **changed the number along with the source** — mid_atlantic
z7 `[1100,1500]` → "1100 to 1500" credited to NC State, mid_south z7 `[1000,1300]` → "1,000 to
1,300" credited to UAEX Chilling Hour Reports, both matching `region_chill_delivered` exactly.

In the herb sentences the number is **unchanged** and only the institution name moved. `zones 5a to 9b`
and the phrase "plant profile" are NC State Plant Toolbox vocabulary.

**And the citation is empty.** All five herbs' `mid_south` cells cite `uada_ext` as their SOLE
source, which is the bare host `https://www.uaex.uada.edu`. There is no document behind any of
these claims — confirm with `python3 tools/bare_host_scan.py --id uada_ext`.

**Why hunt 1 missed them:** hunt 1 read "all 52 UAEX-attributed recommendation claims in mid_south
prose" and found exactly two unsupported — but its scope was the **fruit** crops. These five are
herbs. They were never in that audit.

---

## 4. Method

1. **Locate, per crop, whether UAEX publishes a USDA hardiness range** for thyme, rosemary,
   oregano, sage, English lavender. Start at `uaex.uada.edu`; their herb material tends to live in
   FSA-numbered fact sheets and the Arkansas Extension horticulture pages.
2. **Read from raw bytes.** `urllib` + `pypdf`. Do **not** use a WebFetch summary as evidence —
   the arc has been burned by that. Re-extract every load-bearing sentence.
3. **Adjudicate per crop, never as a group.** See the trap in §6.
4. **Fix by rewording, not deleting** — the `cherry-sweet` precedent. If UAEX does not publish the
   range, drop the credit and keep the fact (NC State's number is presumably right; it is the
   *attribution* that is false). `lavender` z7 `grown_as_note_seasoned` shows the target shape.
5. If UAEX **does** publish a range and it **differs** from the stated one, that is a bigger find:
   a wrong value, not just a wrong credit. Surface it rather than quietly aligning.

---

## 5. Already adjudicated CORRECT — do not re-investigate

- **The 12 chill-hours pairs** (peach; plum ×2; pear-asian ×2; fig; persimmon ×2; mulberry ×2;
  nectarine ×2). Numbers and sources are both correctly regionalized and match
  `region_chill_delivered`. UAEX Chilling Hour Reports is a real UAEX product.
- **strawberry plasticulture** and the **peach/nectarine spray-program** attributions — read and
  verified during hunt 1; the state history names them.
- **`SUIT` (74) and `TYPE` (11) in the same scan are LOW value.** They flag one zone rating
  differently across regions (apple z8 `fruits_reliably` in seven regions, `marginal` in
  `utah_dixie`). That is the region model working as designed. Treating those counts as a worklist
  would mean flattening the region model. If anyone works them, narrow the CHECK, not the scope.
- **`ucr_citrus` is WITHDRAWN** (kickoff 48 §4) — its premise was false. Do not re-propose it.

---

## 6. Traps specific to this task

- **Do not blanket one reason across the five.** The apple/pawpaw precedent: one finding text was
  authored once and attached to ten crops, and the correct reason turned out to be *different* for
  each — apple's source did publish the datum and the declaration survived on geography, pawpaw's
  genuinely published nothing. Expect the same here. UAEX may publish a range for sage and not for
  rosemary.
- **A claim can be true and the credit still false.** The fix is to the attribution. Do not delete
  a correct horticultural fact because its citation was wrong.
- **Check `source_catalog` before judging the source.** `uada_ext` is catalogued T1; the problem is
  that the URL is a domain root, not that the institution is unacceptable.
- **Absence is document-scoped.** "UAEX does not publish herb hardiness ranges" is only true of the
  documents you actually read. Say which ones.

---

## 7. Protocol (binding)

- **One ruling per promote.** An attribution fix and a value change never ride together.
- **Promote only via a guarded script** pinning the pre-state SHA, asserting exact prior values,
  proving an exact footprint, aborting on drift. Use `tools/promote_dezone_lifted_prose.py` or
  `tools/promote_artichoke_findings_key.py` as the current pattern.
- **Guard fixtures must be REBUILT** via `promote_fixture.scratch(BASE_SHA, mutate)`, never copied
  from live canonical. Register your base SHA in `promote_fixture.COMMIT_FOR` (committed) or
  `CHAIN` (uncommitted intermediate). `c6f50a14` → `CHAIN` from `e353fadb`, or add the commit once
  pushed.
- **MUTATION-TEST YOUR GUARDS.** Three times in the last two days a guard was green and vacuous —
  it passed with the check deleted, because an earlier check caught the sabotage first. Delete each
  check in turn and confirm a test fails. If none does, the test is not testing that check.
- **Reuse the load-bearing guard from hunt 1:** refuse to write a reason that names a source the arm
  does not carry (`promote_apple_mid_atlantic_bloom_reason.py`).
- **Release gauntlet:** `whole_crop_gate` on each touched crop + `gate_all.py` + `release_verify`
  diffed against the rebuilt pre-state + the five standalone gates
  (`calendar_coherence_gate`, `harvest_duration_gate`, `numeric_sanity_gate`,
  `cross_consistency_gate`, `soil_temp_floor_scan`).
- **State trio:** amend `CURRENT_STATE.md` surgically (never regenerate — the generator drops the
  74KB locked-decisions block), append `STATE_HISTORY.md` most-recent-first, bump `LATEST.txt`.
- **Canonical is COMPACT:** `separators=(",",":")`, `ensure_ascii=False`, no trailing newline.
- **Don't commit until Trevor approves; he confirms every push separately.**

---

## 8. The rest of the cleanup, for context

This hunt is a small slice. Still open and NOT blocked by anything:

- **32 document hunts / 167 decisions / 614 SOLE bare-host pairs** — essentially unmoved. The
  densest cluster is **eight hunts on UC ANR + UC Master Gardener across the four California
  regions** (~76 crop-decisions on one institution's document family). A 92-cell California
  adjudication already exists in `docs/2026-07-29-citation-cleanup-sample-pass-outcome.md` (read
  its correction banner first).
- `DATES` (35) in the contradiction scan — cells whose planting window shares no month with any
  peer region. Untouched; some will be legitimate desert/valley inversions.
- 9 orphan anchors; the `lavender`/`hawaii_tropical` `westhawaiitoday.com` newspaper anchor, whose
  source id is not in `source_catalog` at all; pole-beans' 50-day harvest against a stated 60-day
  minimum DTM; `version` still `1.0`; the `npk_ratio` 5-10-10 question on the five tomatoes.

**Blocked on plant-astro** (a handoff exists in Trevor's Notes): elderberry's chill
reclassification, the 11 real blackberry/raspberry under-chill cells, and the berry `suitability`
field addition.
