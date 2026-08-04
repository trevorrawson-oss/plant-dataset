# CAMPAIGN B — the remainder (the hard half)

**Written:** 2026-08-03, at the close of the session that opened campaign B.
**Arc tracker:** `docs/citation_arc_hunt_ledger.md`. **Protocol:** kickoff 50 §6, campaign-agnostic.
**Prior kickoffs:** `51-campaign-b-region-templates.md` + `51-campaign-b-handoff.md` — both now carry
CORRECTION blocks. Read the corrections, not the originals, and re-verify even those.

---

## 1. Start state — VERIFY, DO NOT TRUST

| | |
|---|---|
| canonical | `78e5d8e3b649151e4f049aa02cf6de23f05592448942c234e1016802f5652d19` |
| HEAD | `0e7b71b` on `main` |
| **pushed?** | **NO — 4 commits unpushed.** Trevor confirms every push separately. |
| suite | **488 passed** |
| arc | 115 decisions live, 32 hunts, **79 genuinely open** |

```bash
cd ~/plant-dataset
shasum -a 256 crops_data_final.json          # must equal LATEST.txt
git log --oneline -4 && git status -sb
python3 -m pytest tools/ -q --ignore=tools/test_build_berry_pilot_patch.py
python3 tools/campaign_b_reprice.py          # THE authority for this block
python3 tools/frost_anchor_reproduction_gate.py
```

`test_build_berry_pilot_patch.py` breaks pytest **collection** (module-level `sys.exit(0)`).
Pre-existing, ignore. Untracked `.claude/`, `tools/staging/shards/` and
`docs/2026-07-29-establishment-path-encoding-question.md` are **not yours**.

> **Do NOT amend or rebase at or below `bc5250d`.** `promote_fixture.COMMIT_FOR` pins
> `3b7dc544 -> 1fd3ee4` and `78e5d8e3 -> 76db16a`; the strawberry pass's two intermediates
> (`0ab9b42b`, `09358167`) are in `CHAIN` and rebuild by REPLAY. Breaking any of it makes guards
> **SKIP while reporting green**.

---

## 2. What is DONE, so you do not redo it

- **The block is RE-PRICED** and the tool is the authority, not this document:
  `python3 tools/campaign_b_reprice.py`. Nominal 33 decisions / 107 nodes; **6 decisions / 34 nodes
  actually need document work.** 8 closed by ruling, 4 declared, 12 claim-adjudicated with only a
  container root left, 3 region-anchor only.
- **The strawberry decision is worked** (`76db16a`, three class-split promotes): 4 harvest nodes
  repointed at `uada_ext_berries`, z7 re-derived off the anchor it declares (it had been computing
  from `mid_atlantic`'s), 2 findings filed, a fabricated UAEX attribution corrected by APPEND, and a
  reader-facing blossom-frost note. **Residue is 1 real arm** — see §3.
- **`frost_anchor_reproduction_gate` exists** (`0e7b71b`), 0 violations / 1,409 cells in scope, RED
  on the pre-fix state. **Not wired into `whole_crop_gate`;** hard-flip trigger is the next
  template-built region or cross-region calendar pass.
- **Kickoff 51's two "already adjudicated" claims were wrong** and are corrected in place: bloom
  coverage is 21 of 27, not 27; hunt 1's harvest exclusion covers 20 of 34, not 34.

---

## 3. What is LEFT — 6 decisions, and 4 of them are one document hunt

Run the tool for the live list. As of writing:

| decision | nodes | what it needs |
|---|---|---|
| `apricot` / `mid_atlantic` | 6 | **the NC State hunt** |
| `cherry-sour` / `mid_atlantic` | 6 | **the NC State hunt** |
| `cherry-sweet` / `mid_atlantic` | 6 | **the NC State hunt** |
| `pomegranate` / `mid_atlantic` | 6 | **the NC State hunt** |
| `fig` / `mid_south` | 3 | 1 bloom node RULED; **2 harvest nodes open** |
| `strawberry` / `mid_south` | 7 | **1 real arm**: z8 `plant_out` |

Plus 3 **region-anchor only** decisions carrying 8 nodes (`apple` 1, `elderberry` 3,
`broad-beans-fava` 4). These hold no claim — they are `plantings[]` / `resolved_by_zone` roots — so
the question is "which document represents this region's planting model", NOT "what supports this
date". Cheaper, and a different kind of answer. Do not price them like the four above.

### 3a. The mid_atlantic four ARE the campaign

24 of the 34 nodes, one document family, four crops. **Why it is the hard half:**

- **`mid_atlantic`'s sourcing note names ZERO URLs.** There is no vocabulary to inherit, unlike
  `mid_south`, which had five ids with a one-id-one-URL rule.
- **`content.ces.ncsu.edu` is NC State's PUBLICATIONS host, and it is NOT the Plant Toolbox**
  (`plants.ces.ncsu.edu`). Two different NC State properties, two different kinds of answer. The
  repoint target here is an extension **publication**.
- **These four carry no `mid_atlantic` finding at all** — that is precisely why they survived the
  re-price. Everything else in this hunt was already ruled.
- Each holds the same 6-node shape: `plantings` root, `plant_out`, `bloom`, `harvest_start`,
  `harvest_end`, `resolved_by_zone`.

**Expect CASE 2 more often than CASE 1.** The NC State Extension Gardener Handbook's Table 5 is
already known to give *approximate* harvest dates (see `mid_atlantic_nectarine_harvest_divergent`
and `mid_atlantic_mulberry_table_row_species_scoped`, both `accepted_modeled`) — read those two
findings first, because they show what this document does and does not settle, and one of them
records a row that does NOT govern its crop.

### 3b. strawberry's residue is ONE arm, not seven

Six of its seven remaining nodes are adjudicated or containers. The live item is **z8 `plant_out`,
`"Sep 15 - Oct 5"`**. UAEX's Arkansas Berries page supports the SEASON (*"planted in the fall on
raised beds"*) but publishes **no dates**, so the specific window is unsourced. FSA6103 gives a
spring band for the matted row and does not cover the plasticulture fall window. Either locate a
UAEX document with the plug-setting dates, or rule it CASE 2.

Also live and NOT a citation question: `strawberry_mid_south_plasticulture_home_garden_tension`
(`status: open`). FSA6103 says the annual plasticulture system *"is not recommended for home garden
strawberry production"*; the berries page offers it to home gardeners. Two T1 documents from one
institution disagreeing. Trevor's call, not a sourcing fix.

---

## 4. Traps specific to this remainder

- **`vce_426_331` is catalogued blandly but is Virginia's home garden VEGETABLE guide** — already
  caught once as sole source on 19 **fruit** nodes. All four mid_atlantic crops here are fruit.
  Check what crop class a document covers before repointing at it.
- **Pin the exact bare URL PER DECISION**, never from a global map. Campaign A's preflight aborted a
  promote because two crops' "bare `ucanr_ext`" was a different site. In *this* block all 13
  `mid_atlantic` decisions do cite exactly `https://content.ces.ncsu.edu` — verified — but verify
  again rather than inheriting that sentence.
- **Never blanket one reason across crops.** Group by what each cell actually cites.
- **Absence is document-scoped.** Say which documents you read, and how many.
- **Check `source_catalog` before judging a source.** T2 here means SEED TRADE; extension outreach
  is already T1.
- **A pathed URL for another crop does not support THIS claim.** It makes the hunt cheap, not the
  answer free.

---

## 5. Lessons this session paid for, in priority order

1. **A record's SCOPE is narrower than its surface suggests.** Region-named findings come in
   near-identical PAIRS over DIFFERENT crop sets; a hunt's scope is its `(region, source)` pair, not
   its crop list. Reading one roster as covering both regions overstated adjudication by 6 bloom and
   14 harvest arms. Assert the finding exists **on that crop for that region**, mechanically.
2. **When a check floods, narrow the CHECK, not the scope — and suspect your own arithmetic first.**
   Three floods in one session: 1,300 → 62 → 7 → 1 real. Every big number was a measurement
   artifact. A finding COUNT is not evidence until the findings are read.
3. **A check that cannot fail is not a guard.** Four were removed this session as unfailable rather
   than left as decoration, including one that compared a deriver against its own output and stayed
   green while the deriver was stubbed. Mutation-test every guard, and pin abort MESSAGES, not exit
   codes.
4. **Verify where prose RENDERS before writing it.** `region_notes_*` renders nowhere;
   `frost_risk_note_seasoned` and `grown_as_note_*` render today in `BerryYearCalendarCard.astro`. A
   note in an unrendered field informs nobody.
5. **A provenance record is corrected by APPENDING**, leaving the original byte-for-byte — rewriting
   destroys the evidence that the defect happened.

---

## 6. After this block

**C** = arid + Texas, 7 hunts, with AZ1005's 90°-rotated grid and NMSU CR457B's missing window as
documented traps. **D** = the tail, 11 hunts but 7 of them lemon, so invert the unit and read
lemon's citations end to end; campaign A's deferred `lemon` 4 + `lime` 3 and the two pears'
`homeorchard.ucanr.edu` candidates belong there. **Re-price both before hunting them** — that step
has paid off every single time it has been run.

**Owed elsewhere, not blocking:** wiring `region_notes_*` in plant-astro (frontend-only, the copy
already exists on all 121 certified crops in both registers); the desert fruit-set arc (the
July-vs-August question needs a pollen-viability threshold, not a survival one); the
`frost_anchor_reproduction_gate` hard-flip.
