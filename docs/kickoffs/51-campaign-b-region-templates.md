# CAMPAIGN B — the region templates (`mid_south`/`uada_ext` + `mid_atlantic`/`ncsu_ext`)

> **Campaign B of four.** Arc-level tracker: **`docs/citation_arc_hunt_ledger.md`**.
> **The binding protocol is `docs/kickoffs/50-uc-anr-california-citation-hunt.md` §6** — guarded
> promote, rebuilt fixtures, mutation-tested guards, the release gauntlet, the state trio, no
> plant-astro bump. It is written to be campaign-agnostic. Do not restate it; read it.

**Written:** 2026-08-03, at the close of campaign A.
**Canonical when written:** `3f6d6ce4430c23ab8b346017be3b9a8963f635fc1178767293d24e2a689eb6f3`
**HEAD:** `84c7eb2` on `main`, **with campaign A's two promotes UNCOMMITTED on top.**

> **Re-verify this header before trusting it, and re-derive every number below.** Kickoff 48's
> header was three commits stale within a day; kickoff 49's was one stale within two; and kickoff
> 50's §3 was **two revisions stale in its headline claim**, which is the whole reason §1 exists.

---

## 1. Verify state first (non-negotiable)

```bash
cd ~/plant-dataset
shasum -a 256 crops_data_final.json     # must equal LATEST.txt
git log --oneline -1 && git status -sb
python3 -m pytest tools/ -q --ignore=tools/test_build_berry_pilot_patch.py   # expect 402 passed
python3 tools/citation_provenance_scan.py --decisions
```

`test_build_berry_pilot_patch.py` breaks pytest **collection** (module-level `sys.exit(0)`).
Pre-existing. Ignore it. Untracked `.claude/`, `tools/staging/shards/` and
`docs/2026-07-29-establishment-path-encoding-question.md` are **not yours**.

---

## 2. ⚠ FIRST TASK: RE-PRICE THIS BLOCK. IT IS NOT 33 DECISIONS OF REPOINTING.

The ledger says `mid_south`/`uada_ext` = 20 and `mid_atlantic`/`ncsu_ext` = 13. **Both counts are
true and both are misleading**, in the specific way this arc keeps being misled: they count
citations, not open questions. Measured 2026-08-03 by arm type:

| | `mid_south`/`uada_ext` | `mid_atlantic`/`ncsu_ext` |
|---|---|---|
| `plantings[].bloom[]` | 15 | 12 |
| `plantings[].harvest_start[]` + `harvest_end[]` | 26 | 8 |
| `plantings[]` | 20 | 4 |
| `resolved_by_zone.<z>` | 12 | 6 |
| `plantings[].plant_out[]` | 3 | 4 |
| `resolved_by_zone.<z>.heat_pause` | 0 | 2 |
| **total nodes** | **76** | **36** |

**A large share is ALREADY ADJUDICATED, and re-working it would be phantom work:**

- **Every bloom arm is covered by an accepted finding.** `mid_south_bloom_offset_undocumented` and
  `mid_atlantic_bloom_offset_undocumented` both sit at **`status: accepted_modeled`** on the fruit
  roster (verified 2026-08-03 on apricot, cherry-sour, cherry-sweet, fig, mulberry, nectarine,
  pawpaw, peach, both pears, persimmon, plum, pomegranate). That is **27 of the 112 nodes** closed
  by ruling. `absence-findings-are-document-scoped` still applies: those rulings are scoped to the
  documents that were read.
- **The harvest arms were left bare ON PURPOSE by hunt 1** (2026-07-30,
  `docs/2026-07-30-mid-south-uada-ext-citation-hunt.md`), whose own docstring records why: *"UAEX
  publishes NO harvest dates for them. FSA6129 has no plum section at all and gives peach/nectarine
  only a relative 'days before Elberta' ladder with no anchor date."* That is **another 34 nodes**
  already answered. Do not re-hunt them without new documents.
- `apricot`, `mulberry` and `pomegranate` additionally carry
  `mid_south_fruit_trees_citation_generic_basis` at `accepted_modeled`.

**So the genuinely open surface is much smaller than 33 decisions, and your first deliverable is
the honest number.** Derive it; do not take mine. Campaign A's equivalent step turned "4 authoring
decisions" into 2 and found a whole class (12 decisions with no usable row) that nobody had seen.

---

## 3. Why these two, and what makes them different from campaign A

**These are the PARENTS of the find-and-replace defect class.** `mid_south` was built from the
`mid_atlantic` template, and both the cherry-sweet fabrication (2026-07-30) and the ten false UAEX
herb credits (2026-07-31) were born that way. Closing them has knock-on value beyond their count.

Campaign A had one governing document for four regions. **Campaign B has none.** That is the
structural difference and it should change your method: A was one document read against N crops; B
is a per-crop-class search where the answer legitimately differs per crop.

### The bare hosts are NOT the same kind of thing

| hunt | bare host | what it is |
|---|---|---|
| `mid_south`/`uada_ext` | `https://www.uaex.uada.edu` | the UAEX **institution root** |
| `mid_atlantic`/`ncsu_ext` | `https://content.ces.ncsu.edu` | NC State Extension's **publications host** |

`content.ces.ncsu.edu` is where NC State's extension *publications* live, and it is **not** the
Plant Toolbox (`plants.ces.ncsu.edu`), which is where the herb hunt found NC State's species
pages. So the mid_atlantic repoint target is an extension **publication**, and a Toolbox plant page
is a different kind of answer. **This is the campaign-A pear lesson in advance:** campaign A nearly
filed a false reason because two crops' "bare `ucanr_ext`" was actually `homeorchard.ucanr.edu`, a
different site. **Pin the exact bare URL per decision, never read it from a global map.**

---

## 4. What is already known — do NOT redo it

- **`mid_south` already built a per-document citation vocabulary** —
  `docs/reviews/notes/2026-07-20/mid_south_sources.md` defines `uada_ext_spring_veg`,
  `uada_ext_fall_veg`, `uada_ext_fsa6001`, `uada_ext_chill`, `uada_ext_fsa6105`, with a
  **one-id-one-URL** rule. **But it is scoped to a CROP CLASS, not the region: it is
  vegetables-only.** All 20 crops in this hunt are fruit, herbs or strawberry. Assuming the
  vocabulary covers them would manufacture defects ([[citation-vocabulary-scope-trap]]).
- **Hunt 1 created `uada_ext_fruit_trees`** and repointed 40 nodes across 12 crops
  (`promote_mid_south_fruit_tree_repoint.py`). What remains bare in those crops is what that hunt
  **deliberately excluded**, each for a stated reason. Read its docstring before touching them.
- **The 2026-07-31 herb pass fixed PROSE ONLY** and deliberately did not repoint, so all 10 herb
  cells (oregano 3, rosemary 3, sage 3, thyme 3 nodes) still cite the bare host.
- **`lavender` has the one identified real repoint target in the whole hunt** — UAEX's English
  Lavender Plant of the Week — with a filed finding
  (`lavender_mid_south_uaex_zone_range_divergence`) stating exactly what must change with it: UAEX
  publishes **zones 5 to 8**, so the z8 cell's *"comfortably inside ... zone 5 to 9b"* wording
  becomes false the moment the citation moves. **The citation and that sentence must move together
  or not at all.** Note lavender does not appear in this hunt's 20 crops, so confirm where it sits
  before acting.
- **`rosemary_mid_atlantic_ncsu_zone_attribution` is filed and `status: open`** — NC State's
  Toolbox gives *Salvia rosmarinus* as 8a-10b while our prose says "zone 7 to 8". The number is
  sound (our own hardy-cultivar floor, `rosemary_pilot_finding_004`); the credit overstates. This
  is a live item in this campaign.
- **`strawberry` is the single largest crop here** (12 `mid_south` nodes) and carries **no**
  mid_south finding at all. It is the most likely place for something genuinely unruled.

---

## 5. Traps specific to this block

- **`mid_atlantic`'s sourcing note names ZERO URLs**, which is why it is harder than `mid_south`
  despite being smaller. There is no vocabulary to inherit.
- **`vce_426_331` is catalogued blandly but is Virginia's home garden VEGETABLE planting guide** —
  already caught once as the sole source on 19 **fruit** nodes. Check what crop class a document
  actually covers before repointing anything at it.
- **A pathed URL for another crop does not support THIS claim.** It makes the hunt cheap, not the
  answer free.
- **Match the taxon, not the common name** — UAEX's only zone-bearing "rosemary" page is
  *Salix elaeagnos*, a willow.
- **Absence is document-scoped.** Say which documents you read, and how many.
- **Check `source_catalog` before judging a source** — T2 here means SEED TRADE, and extension
  outreach already sits at T1.
- **Never blanket one reason across crops.** Campaign A's guard caught exactly this on the pears,
  and the 2026-07-31 apple/pawpaw pass caught it before that. Group by what each cell cites.

---

## 6. Suggested order

1. **Re-price (§2)** and record the honest open number in the ledger.
2. **`strawberry`** — biggest single crop, no existing finding, most likely to be genuinely open.
3. **The 10 herb cells** — the prose is already corrected; this is the citation half, and
   `lavender`'s finding names the one real repoint plus the sentence that must move with it.
4. **`mid_atlantic`'s non-bloom arms** — the harder half; expect CASE 2 more often than CASE 1.
5. **Update `docs/citation_arc_hunt_ledger.md`** as each hunt closes. That is the durable record;
   this kickoff will go stale and the ledger will not.

---

## 7. What is left after this block

Per the ledger at the time of writing: **91 decisions genuinely open.** Campaign B is the largest
remaining. Then **C** (arid + Texas, 7 hunts, AZ1005's 90°-rotated grid and NMSU CR457B's missing
window as documented traps) and **D** (the tail — 11 hunts but **7 of them are lemon**, so invert
the unit and read lemon's citations end to end; campaign A's deferred `lemon` 4 + `lime` 3
decisions belong there, plus the two pears' `homeorchard.ucanr.edu` repoint candidates, which
should be settled together with their `ucanr_marin_mg` decisions).

**Also open and NOT part of this arc:** the desert **fruit-set arc** (see `STATE_HISTORY.md`
2026-08-03 — the July-vs-August winter-squash question, which needs a pollen-viability threshold
rather than a survival threshold); the **planting-note rendering gap** (plant-astro reads none of
`region_notes_*`, `planting_note`, `zone_notes`, `notes`, and `succession_policy.tip_*` is
crop-level); `DATES` (35) in the contradiction scan; 9 orphan anchors; the `lavender`/
`hawaii_tropical` anchor whose source id is not in `source_catalog` at all; pole-beans' 50-day
harvest against a stated 60-day minimum DTM; `version` still `1.0`; the `npk_ratio` question on the
five tomatoes.
