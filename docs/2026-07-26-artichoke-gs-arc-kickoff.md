# Artichoke GS arc — kickoff

**Date:** 2026-07-26
**Target:** artichoke, gold-standard crop #121 (shell → certified). Shells 8 → 7.
**Predecessor:** asparagus (#120), certified 2026-07-24, then **repaired across four passes on
2026-07-26**. This kickoff exists because that repair should not have been necessary.
**Read with:** `CURRENT_STATE.md` (top four entries are the asparagus repair),
`docs/2026-07-25-asparagus-timing-gaps.md` (the original defect report).

---

## 0. Why this document exists

Asparagus passed a 120/120 roster gate, a CLEAN release verify, and an 11/11 T1 source-truth
sample — and shipped **unable to tell anyone when to plant it**. Zero `plant_out`, zero `harvest`
strings, across all 39 zone cells. On the one crop whose entire failure mode is "plants it,
expects spears."

Then the repair found more: four cited sources that did not support their claims, and a suitability
map whose central mechanism was invented.

None of that was carelessness. Each failure was a *reasonable-looking local decision*. That is
what makes them worth writing down. §2 is the post-mortem as operating rules. **Read §2 before
authoring anything.**

---

## 1. Verified current state

Checked against canonical `34025ee3` on 2026-07-26. Do not trust this section without re-checking
— re-run the probes if time has passed.

| Field | Value | Note |
|---|---|---|
| `archetype` | `warm_season_fruiting` | **Decision needed** — see §3.1 |
| `calendar_basis` | `frost_anchored` | correct for either archetype outcome |
| `category` | `Fruiting Veg` | **should move** to `Perennial Vegetables` (asparagus precedent) |
| `perennial` / `lifecycle` | `true` / `perennial` | already right |
| `days_to_maturity` | `[]` | fine for this class if the perennial model holds — see §3.1 |
| `years_to_first_harvest` | `[]` | **must be authored** |
| `years_to_full_production` | `[]` | **must be authored** |
| `establishment_years` | `null` | **must be authored** — and NOT as a copy of `years_to_first_harvest` |
| `productive_lifespan_years` | `null` | **must be authored** |
| `propagule` | `null` | register field (A40 enum) |
| `planting_layout` | `null` | register field (A44 — must be a STRING, the dict form crashes it) |
| `year_one_notes_*` | **already authored** | both registers present. Verify they match the final model. |
| `verification_status.status` | `null` | shell |

**Regions: 10, cells: 20, calendared: 0, `plant_out`: 0.**

Present: `northern_tier`, `warm_arid`, `ca_interior`, `ca_north_coast`, `ca_south_coast`,
`ca_desert`, `low_desert_az`, `se_gulf`, `fl_peninsula`, `hawaii_tropical`.

**Missing 6 versus the asparagus 16-region roster:** `utah_dixie`, `mid_atlantic`, `mid_south`,
`pnw`, `nevada`, `rgv`. Adding those shells is in scope — decide it explicitly in §3, don't
discover it mid-arc.

```bash
# re-verify state before starting
cd ~/plant-dataset && python3 -c "
import json; d=json.load(open('crops_data_final.json'))
a=[c for c in d['crops'] if c['slug']=='artichoke'][0]
for f in ('archetype','calendar_basis','category','perennial','lifecycle','days_to_maturity',
          'years_to_first_harvest','years_to_full_production','establishment_years',
          'productive_lifespan_years','propagule','planting_layout'):
    print('%-26s %s' % (f, json.dumps(a.get(f))))
print('regions', len(a.get('regions') or {}))
"
```

---

## 2. The asparagus post-mortem, as rules

Nine failure modes. Each is a rule, and each names what it cost.

### R1. A field you omit stops being checked. Never omit to dodge a gate.
The cert plan wrote: *"OMIT `plant_out`/`harvest` … the crown-planting window lives in
`start_method`/`year_one_notes`"* — and, revealingly, *"omitting them keeps A24/A43 vacuous."*
`start_method` was authored with no timing. `year_one_notes` was never authored at all. The data
moved out of the calendar and landed **nowhere**, and the gates that would have caught it went
vacuous precisely *because* the field was absent.

**Rule:** if you decide a field does not apply, (a) say where the information lives instead, and
(b) **verify it is actually there before cert**, by reading the target field. If a gate blocks
honest data, carve the gate out narrowly with TDD (see R2) — never route around it by deletion.

> Now partly enforced: **A47** (hard) requires `plant_out` on every calendared cell of a crop with
> `perennial: true`, exempting `unsuitable` cells and empty-calendar shells. Artichoke has
> `perennial: true`, so **A47 will fire the moment its cells get calendars**. That closes this one
> specific hole. It does not close the general pattern.

### R2. When honest data breaks a gate, carve out narrowly — and prove the gate still bites.
Asparagus's dormant-crown windows tripped A24 (`cold_pause` on a `plant_out` month), which encodes
an *annual* assumption: you cannot set a frost-tender transplant out during a frost lockout. A
dormant crown is the opposite case — planted deliberately while the ground is cold. 17 of 25
sourced windows would have falsely bounced.

The fix exempted **only that branch**, **only for the archetype**, and proved it did not become an
escape hatch: chives and mint are herbaceous perennials too, on `culinary_herb`, and still bounce
(32 and 42 violations). A basis flip would have been the lazy fix and would have silently disabled
A5/A24/A25 wholesale.

**Rule:** carve-out, not basis flip. TDD RED before GREEN. Prove a *neighbouring* crop still
bounces on the same defect.

### R3. A `.edu` host is not a T1 source. Tier on what the document *is*.
The chill requirement that justified nearly every marginal/unsuitable asparagus rating traced to
**PlantVillage** — `.edu`-hosted, but an aggregated crop-profile database, unattributed, its own
references pointing at Minnesota and Tennessee. Two `ucanr.edu`-hosted pages failed the same way:
one is reprinted eastern/midwestern text ("In the east, in the cool spring…"), another is credited
to "Digital Gardener" using Sunset zones.

**Rule:** for every source ask *what document is this?* — peer-reviewed extension bulletin, county
Master Gardener page, aggregated database, or reprint. Record the answer in `citable_for`. Flag
`.org` volunteer-association hosts explicitly. A stand-life claim from a volunteer blog Q&A is not
evidence (that exact thing nearly promoted a California cell).

### R4. Verify every citation supports its specific claim.
Four sources on certified asparagus cells did not support what they were cited for. `unr_fs0261`
is *"Home Vegetable Production in Southern Nevada"* whose **only** mention of the crop is the
string `"Stems - asparagus"` in a list of edible plant parts. `ucanr_ext` is the **Kings County
2005 Annual Agricultural Crop Report**. All four survived the 11/11 T1 sample, which did not
happen to draw them.

**Rule:** a source is cited *for a claim*, not for a crop. Extract the document and confirm the
sentence exists. Weight the sample toward cells whose claims rest on a single source. And verify
every URL **resolves** before citing — one constructed-by-hand URL 404'd during the repair.

### R5. Name the mechanism, and cite it per rating.
Asparagus's suitability map ran on "needs winter chill." No T1 source states a chill requirement
for asparagus anywhere. The real mechanism — dormancy from **cold OR drought**, plus a fern-growth
ceiling above 85°F — is what makes Mediterranean California work and the summer-**wet** Gulf fail.
The wrong mechanism got the tropics right by luck and California wrong by reasoning.

**Rule:** write the physiological mechanism down explicitly at the start of the arc, with its
quote. Every `marginal`/`unsuitable` rating must cite *that mechanism* and a source. If you cannot
name the mechanism, you cannot rate the cell.

### R6. A blanket note is a claim about every cell it lands on.
During the repair I applied a "both routes to dormancy fail" note across the unsuitable cells. It
was true for summer-wet Hawaii, Florida, and RGV — and **false for the arid Arizona desert**, where
a dry-down is the one thing the climate guarantees. Re-auditing every cell then caught a second
instance (coastal SoCal — Mediterranean, dry summers).

**Rule:** after any sweep that touches many cells, re-read **each** cell against the mechanism. Do
not assume the class is uniform.

### R7. Region prose and cell ratings are two layers, and no gate compares them.
After re-rating, `ca_north_coast`'s `region_notes` still read *"both zones 9 and 10 perennialize
only marginally"* — for two cells just promoted to `perennializes`. A contradiction between two
strings the same guide renders to the same reader. A36 checks both registers *exist*; A29 checks
they are *authored*; neither reads what they **say**.

**Rule:** after finalizing per-zone ratings, manually re-read every `region_notes_*` pair against
the cells it summarizes. There is an open candidate gate for this; it is not built.

### R8. Confirm what a date actually describes.
UC IPM's California asparagus planting table is a **seed** table — using it would have put a
crown window two months late, outside dormancy. Rutgers' "early April" is **furrow shaping**, not
crown placement. A UA calendar's header says "made for seeds unless otherwise noted" while listing
an 8-inch planting depth, which is a crown depth.

**Rule:** for every date, confirm *what organ and what operation* it describes — seed, transplant,
crown/division, or field prep. Artichoke is propagated **several** ways (seed, transplant, division,
offshoot, root stock), so this hazard is **worse here than it was for asparagus**. Expect it.

### R9. Extraction hazards, and verify zone→geography before reasoning.
- WebFetch's markdown conversion **silently shifts columns** on HTML data tables. Fetch raw HTML
  and parse structurally. This previously produced three fabricated values.
- WebFetch **cannot decode PDFs**. Use `pypdf`.
- Some chart windows are **drawn bars with no text layer** — recoverable only from PDF
  content-stream geometry, and worth flagging as low-provenance when they are.
- **Verify the zone→geography mapping by ZIP before reasoning about a region.** A wrong premise
  (that `ca_desert` z9 meant Antelope Valley) survived a full research pass and **reversed three
  of four recommendations** when corrected.

---

## 3. Design decisions to make BEFORE authoring

Make these explicitly, in writing, at the top of the arc. Asparagus's damage traces to one
modeling decision made mid-authoring whose consequence was never checked.

### 3.1 THE BIG ONE: artichoke is genuinely dual-mode. Asparagus was not.

Artichoke is a perennial in mild-winter regions (roughly z7-11, the California coastal model,
cropping for 5+ years from divisions or offshoots) **and is grown as an annual** in cold regions —
started indoors, vernalized to force budding, harvested in its first season, discarded. Both are
real, both are extension-documented, and they imply **different calendars, different propagules,
and different `days_to_maturity` semantics**.

This is the single largest risk in the arc, because it is exactly the shape of decision that broke
asparagus: a defensible modeling call whose downstream field consequences went unverified.

Decide and record:
- **One crop or two?** One crop with per-region modes, or an annual/perennial split?
- **Archetype:** stay `warm_season_fruiting`, or move to `herbaceous_perennial` (the archetype
  built as "asparagus + later artichoke")? See §4 for what each choice makes the gates do.
- **`days_to_maturity`:** `[]` is honest for a pure perennial model. If artichoke is annual
  anywhere in the roster, `[]` is **wrong there** — an annual grower needs a DTM. Do not inherit
  asparagus's `[]` by analogy. This is precisely an R1 trap.
- **Propagule:** seed / transplant / division / offshoot are all real. `propagule` is a single
  A40-enum value. If the crop genuinely has several, decide what the field means and where the
  others are documented — **then verify that place exists** (R1).

Whatever you decide, write the consequence for **every** field in §1's table. That written
consequence is the artifact that would have prevented the asparagus defect.

### 3.2 Region roster: 10 or 16?
Six regions are missing. Author them to reach parity, or record why artichoke's roster is
legitimately narrower. Do it now — `docs/gs_cross_crop_field_addition_v0.md` warns that column
passes must run against a **stable** roster, never mid-certification.

### 3.3 Category
Move `Fruiting Veg` → `Perennial Vegetables` (asparagus precedent: UC frames both as perennial
vegetables, not fruiting). **This is a frontend-visible change** — `src/pages/index.astro` carries
a category list. Coordinate with the astro lane; do not assume it is safe.

### 3.4 The suitability mechanism (R5), written first
Before rating any cell, write down artichoke's actual physiological constraints with quotes.
Likely candidates — verify, do not assume: a **vernalization/chill requirement for bud
initiation** (genuinely real for artichoke, unlike asparagus — do not over-correct from the
asparagus finding), frost damage thresholds to buds, and a summer-heat ceiling.

⚠️ **Do not import asparagus's conclusion.** The asparagus lesson is *"name and cite the
mechanism,"* **not** *"chill never matters."* Artichoke very plausibly does have a real chill/
vernalization requirement. Source it.

---

## 4. Gate landscape — what will fire

| Gate | Behavior on artichoke |
|---|---|
| **A47** perennial planting-data floor | **HARD.** `perennial: true`, so once cells have calendars every non-`unsuitable` cell must carry `plant_out`. Currently vacuous (0 calendared). **This is the gate that would have caught asparagus.** |
| `herbaceous_perennial_gate` (A46) | No-op today (archetype is `warm_season_fruiting`). **If you move the archetype**, it demands: `perennial` true ✓, `lifecycle` perennial ✓, `succession_policy.suitable: false` + reason, `years_to_first_harvest` non-empty numeric min ≥ 1 (**currently `[]` → will fail**), `years_to_full_production` non-empty (**`[]` → will fail**), `productive_lifespan_years` positive int (**`null` → will fail**), `rotation` present, and per-cell `suitability` in the enum with dual-register notes on marginal/unsuitable. |
| A24 / A34 / A37 carve-outs | Scoped to `archetype == "herbaceous_perennial"`. Moving the archetype **inherits all three**. If you move it, re-validate each is actually appropriate for artichoke rather than assuming — they were justified for dormant crowns and a spring-harvest/summer-fern cycle. |
| `calendar_basis_gate` | Maps `herbaceous_perennial → frost_anchored`. Artichoke is already `frost_anchored`, so either archetype choice is consistent. **Do not flip `calendar_basis` to a perennial basis** — it selects validation machinery, not perennial-ness, and flipping silently disables six gates. |
| A39-A42, A44 register floor | Hard cert requirements. `propagule` (A40 enum) and `planting_layout` (A44, **string** not dict) are currently `null`. |

---

## 5. Acceptance bar

Cert is not done until **all** of these hold:

1. `whole_crop_gate artichoke` PASS · `tools/gate_all.py` **121/121** · `release_verify` CLEAN.
2. **A47 reports 0** for artichoke, and reports 0 roster-wide.
3. **Every** `perennializes`/`marginal` cell carries `plant_out` **and** `harvest`. Verify by
   reading the cells, not by trusting a green gate — a green gate is what asparagus had.
4. Every field in §1's table is authored, or has a **written** justification for being empty that
   names where the information lives — **and that place has been read and confirmed** (R1).
5. Every `marginal`/`unsuitable` rating cites the §3.4 mechanism plus a source (R5).
6. Every citation verified to support its **specific claim**, with a resolving URL (R4).
7. Every `region_notes_*` pair manually re-read against its cells' final ratings (R7).
8. Per-cell `resolution_method` honestly distinguishes sourced from derived.
9. T1 source-truth sample, weighted toward single-source cells (R4).
10. Consumer copy scan: no em dashes, American English, `°F`, "plant" lowercase, everyday word
    choice ("ladybug", not "lady beetle").
11. State trio: `CURRENT_STATE.md` hand-maintained **surgically** (it has no `---` separator — a
    naive `gen_current_state` regen corrupts it), `STATE_HISTORY.md` appended most-recent-first,
    `LATEST.txt` SHA + session bumped and **verified against the canonical**.
12. Field-addition register updated if the category move or any new field lands.

**The asparagus test:** before declaring cert, open the crop as a grower in three regions and ask
*"does this tell me when to plant, and when to expect food?"* Asparagus passed every automated
check and failed that question.

---

## 6. Working notes

- Canonical JSON is **COMPACT** (`separators=(",",":")`, `ensure_ascii=False`, no trailing
  newline). Write via a promote script, never by hand.
- Promote scripts should **guard their assumptions** and abort on drift — see
  `tools/promote_asparagus_ca_south_coast_z11.py`, which refuses to run if the cell it derives
  from has changed.
- Dispatch research as parallel read-only agents, one per region/source family. Instruct each to
  **report gaps rather than infer**, and to return **verbatim quotes** so claims can be checked
  without re-fetching. That is how the seed-table and furrow-shaping traps were caught.
- Nothing commits without Trevor's approval; he confirms every push. No plant-astro bump from the
  dataset session — the astro lane owns art, bump, and deploy.
