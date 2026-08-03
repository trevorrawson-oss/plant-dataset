# CAMPAIGN B — session handoff

**Written:** 2026-08-03, at the close of the campaign A session.
**Start here, then read `docs/kickoffs/51-campaign-b-region-templates.md`** (the kickoff proper).
The binding protocol is **kickoff 50 §6** — guarded promote, rebuilt fixtures, mutation-tested
guards, the release gauntlet, the state trio, no plant-astro bump. It is campaign-agnostic.

---

## 1. Where you are starting (verify, do not trust)

| | |
|---|---|
| canonical | `3b7dc5440ff989e8a3c1d524d3574230f14e50ae0b9c8469edc4b3a93c8271a1` |
| HEAD | `c92ebc4` on `main` |
| **pushed?** | **NO — four commits sit unpushed. Trevor confirms every push separately.** |
| suite | 422 passed |
| arc | 115 decisions live, **91 genuinely open**, 32 hunts |

```bash
cd ~/plant-dataset
shasum -a 256 crops_data_final.json     # must equal LATEST.txt
git log --oneline -4 && git status -sb
python3 -m pytest tools/ -q --ignore=tools/test_build_berry_pilot_patch.py
python3 tools/citation_provenance_scan.py --decisions
```

`test_build_berry_pilot_patch.py` breaks pytest **collection** (module-level `sys.exit(0)`).
Pre-existing, ignore. Untracked `.claude/`, `tools/staging/shards/` and
`docs/2026-07-29-establishment-path-encoding-question.md` are **not yours**.

`promote_fixture` already knows `3b7dc544 -> 1fd3ee4`, so your first guard suite can rebuild the
pre-state immediately.

---

## 2. ⚠ THE FIRST TASK IS TO RE-PRICE. THIS IS NOT 33 DECISIONS OF REPOINTING.

The ledger says `mid_south`/`uada_ext` = 20 and `mid_atlantic`/`ncsu_ext` = 13. Both counts are
true and both are misleading, in the exact way this arc keeps being misled. Measured 2026-08-03:
**112 nodes**, and a large share is already adjudicated.

- **27 bloom arms are covered by accepted findings.** `mid_south_bloom_offset_undocumented` and
  `mid_atlantic_bloom_offset_undocumented` sit at **`status: accepted_modeled`** across the fruit
  roster. Verified on apricot, cherry-sour, cherry-sweet, fig, mulberry, nectarine, pawpaw, peach,
  both pears, persimmon, plum, pomegranate.
- **34 harvest arms were left bare ON PURPOSE by hunt 1** (2026-07-30). Its own docstring says
  why: *"UAEX publishes NO harvest dates for them. FSA6129 has no plum section at all and gives
  peach/nectarine only a relative 'days before Elberta' ladder with no anchor date."*
- `apricot`, `mulberry`, `pomegranate` additionally carry
  `mid_south_fruit_trees_citation_generic_basis` at `accepted_modeled`.

**Derive the honest open number yourself and record it in the ledger before hunting.** Campaign A's
equivalent step turned "4 authoring decisions" into 2 and surfaced a whole class nobody had seen.

---

## 3. The three lessons campaign A paid for. Do not re-learn them.

**1. PIN THE EXACT BARE URL PER DECISION, never read it from a global map.** Campaign A's closeout
drafted one "the UC page is a vegetable table with no row for this crop" finding across five crops.
It was true for three. **The two pears do not cite the vegetable table at all** — they cite
`https://homeorchard.ucanr.edu/`, a different UC site — so the finding would have written a false
statement about their citation into canonical. A preflight pinning the URL per decision aborted the
promote. **This block has the same hazard shape:** `mid_atlantic`'s bare host is
`https://content.ces.ncsu.edu`, NC State's **publications** host, which is *not* the Plant Toolbox
(`plants.ces.ncsu.edu`) where the herb hunt found NC State's species pages. Two different NC State
properties, two different kinds of answer.

**2. RE-VERIFY EVERY RECORD YOU ACT ON, INCLUDING A KICKOFF'S OWN "do NOT redo this" SECTION.**
Kickoff 50 §3 was two revisions stale in its headline claim, and its heading is exactly why nobody
checked. **A record can be stale in the RECOMMENDATION, not just the value** — §3 row 1 proposed a
repoint that an accepted finding had already refused by name. Checking that a quoted number still
exists is not enough; check whether a later ruling already adjudicated the move.

**3. A CHECK THAT CANNOT FAIL IS NOT A GUARD.** Mutation testing found **8 of 21 vacuous** on
campaign A's first promote. Techniques that made unreachable guards testable, all reusable:
load the promote as a **module** and patch its constants (for constant-vs-constant checks); doctor
the **first `copy.deepcopy`** (the `before` snapshot) to simulate a change the edit loop never made;
shim `json.dumps` to append a newline (write-time guards); and construct a mutation that moves one
count while **holding another constant** (an anchor moved to a new node keeps entries at 178 but
takes nodes to 90). Two checks that could not fail under any input were **removed**, not left as
decoration. **Pin abort MESSAGES, not exit codes** — the checks overlap.

---

## 4. What is already known — do NOT redo it

- **`mid_south` built a per-document citation vocabulary and then did not apply it here.**
  `docs/reviews/notes/2026-07-20/mid_south_sources.md` defines `uada_ext_spring_veg`,
  `uada_ext_fall_veg`, `uada_ext_fsa6001`, `uada_ext_chill`, `uada_ext_fsa6105` with a
  **one-id-one-URL** rule. **It is scoped to a CROP CLASS, not the region: vegetables only.** All 20
  crops in this hunt are fruit, herbs or strawberry. Assuming it covers them manufactures defects.
- **Hunt 1 created `uada_ext_fruit_trees`** and repointed 40 nodes over 12 crops. What remains bare
  in those crops is what it **deliberately excluded**, each with a stated reason. Read
  `tools/promote_mid_south_fruit_tree_repoint.py`'s docstring before touching them.
- **The 2026-07-31 herb pass fixed PROSE ONLY** and deliberately did not repoint, so all 10 herb
  cells (oregano, rosemary, sage, thyme — 3 nodes each) still cite the bare host.
- **`lavender` holds the one identified real repoint target**, UAEX's English Lavender Plant of the
  Week, with `lavender_mid_south_uaex_zone_range_divergence` stating exactly what must change with
  it: UAEX publishes **zones 5 to 8**, so the z8 cell's *"comfortably inside ... zone 5 to 9b"*
  becomes false the moment the citation moves. **The citation and that sentence move together or
  not at all.** Confirm where lavender sits — it is not among this hunt's 20 crops.
- **`rosemary_mid_atlantic_ncsu_zone_attribution` is filed and `status: open`** — NC State's Toolbox
  gives *Salvia rosmarinus* as 8a-10b while our prose says "zone 7 to 8". The number is sound (our
  own hardy-cultivar floor per `rosemary_pilot_finding_004`); the credit overstates. Live item.
- **`strawberry` is the largest single crop here** (12 `mid_south` nodes) and carries **no**
  mid_south finding at all. Most likely place for something genuinely unruled.
- **`mid_atlantic`'s sourcing note names ZERO URLs.** No vocabulary to inherit; that is why the
  smaller hunt is the harder one.
- **`vce_426_331` is catalogued blandly but is Virginia's home garden VEGETABLE guide** — already
  caught once as sole source on 19 **fruit** nodes. Check what crop class a document covers.

---

## 5. Suggested order

1. **Re-price (§2)**, record the honest number in `docs/citation_arc_hunt_ledger.md`.
2. **`strawberry`** — biggest crop, no existing finding, most likely genuinely open.
3. **The 10 herb cells** — prose already corrected; this is the citation half, and lavender's
   finding names the one real repoint plus the sentence that must move with it.
4. **`mid_atlantic`'s non-bloom arms** — expect CASE 2 more often than CASE 1.
5. **Update the ledger as each hunt closes.** It is the durable record; kickoffs go stale.

---

## 6. Everything else this session left open

**Owed but not blocking B:**

- **Wire `region_notes_seasoned`/`region_notes_beginner` in plant-astro.** This is a **frontend-only**
  task — the field already exists and is populated on **all 121 certified crops in both registers**
  (1,808 of 1,878 region cells; the only 70 gaps are the 7 uncertified shells x 10 regions). It is
  **not** a schema change. plant-astro currently reads none of `region_notes_*`, `planting_note`,
  `zone_notes` or `notes` (the last two deliberately dropped, `PlantingCalendarCard.astro:375`).
  Trevor's community-tips design: one plant suggestion, then community suggestions in a **separate
  slot below it**, never merged into the authored note; every submission reviewed before it
  publishes; region-scoped now, county/ZIP later if volume justifies it.
  **Note `planting_note` is semantically polluted** and should not be the vehicle: it holds enum-ish
  tokens on some crops (`cherry-tomato`: `"range"`, `"multi_season"`) and full consumer prose on
  others (`marigold`), across 1,124 non-empty cells.
- **The desert fruit-set arc.** The July-vs-August winter-squash question needs a **pollen-viability**
  threshold, not a survival threshold — July and August differ by about a degree in the low desert
  and both sit above our own 95 °F germination ceiling, so a survival test condemns both dates and
  must be wrong. Working in `STATE_HISTORY.md` 2026-08-03.
- **Campaign A's deferred residue:** `lemon` 4 + `lime` 3 decisions to campaign D's lemon cluster;
  the two pears' `homeorchard.ucanr.edu` repoint candidates to a UC fruit-tree read that should also
  settle their `ca_north_coast`/`ucanr_marin_mg` decisions.

**Then C and D.** C = arid + Texas, 7 hunts, with AZ1005's 90°-rotated grid and NMSU CR457B's
missing window as documented traps. D = the tail, 11 hunts but **7 of them are lemon**, so invert
the unit and read lemon's citations end to end.

**Not part of this arc:** `DATES` (35) in the contradiction scan; 9 orphan anchors; the
`lavender`/`hawaii_tropical` anchor whose source id is not in `source_catalog` at all; pole-beans'
50-day harvest against a stated 60-day minimum DTM; `version` still `1.0`; the `npk_ratio` question
on the five tomatoes.
