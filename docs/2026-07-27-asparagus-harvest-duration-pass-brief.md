# Brief: the asparagus harvest-duration pass

**Date written:** 2026-07-27
**Written by:** the session that opened the question, deliberately handing it off rather than
resolving it (see §7 for why).
**Canonical at handoff:** `02fbb5e8` (`origin/main` `561d914`, pushed).
**Status:** NOT STARTED. Nothing in this brief has been applied.

Read `docs/2026-07-27-asparagus-harvest-start-sourcing-sweep.md` first: it establishes that harvest
**duration** is well sourced roster-wide while **starts** are not, and that is the load-bearing
asymmetry this pass operates inside.

---

## 0. The one-paragraph version

Asparagus's 29 renderable harvest windows were re-sourced on 2026-07-27. Before that pass, **all 29
were exactly two calendar months** and that uniformity was the tell that they had been derived, not
sourced. After it, **24 of 29 are exactly three calendar months.** Nine of those carry a note whose
own sourced duration (four to eight weeks) cannot fill three calendar months, and one of them,
`mid_south` z7, is contradicted outright by a source cited on the cell. **The pass may have traded a
uniform two-month artifact for a uniform three-month one.** This brief scopes the check.

---

## 1. THE QUESTION THAT DECIDES EVERYTHING — settle it before touching any cell

**What does a `harvest` string mean?**

| reading | "Mar - May" means | consequence |
|---|---|---|
| **A. Month-granular** | "spears are available somewhere within March, April and May" | An 8-week window starting **mid**-March legitimately touches three calendar months. **Most or all nine flagged cells are then FINE**, and this pass ends in a day with a documented ruling. |
| **B. Precise window** | "from about March 1 to about May 31" | A 6-to-8-week sourced duration **cannot** produce it. **Nine cells are over-extended** and need repair. |

This is not a detail to resolve along the way. **It is the whole pass**, and everything below is
conditional on it. Do not begin editing cells before it is ruled.

Inputs to the ruling:
- The strings are **month-granular by construction** (`"Mar - May"`, no days) while `plant_out`
  on the same cells is **day-granular** (`"Jan 1 - Mar 1"`). That asymmetry is deliberate and is
  evidence for reading A.
- But the site renders these to a specific reader in a specific zone. Ask the plant-astro lane how
  `harvest` is drawn: if it fills a three-month bar, reading A is a promise the data does not keep.
- Trevor's north star is accuracy and honesty about limits. If A is chosen, the reading must be
  **written down** in `CLAUDE.md` or the field register, because it was never recorded, and an
  unrecorded convention is how the original two-month artifact survived cert.

**If reading A wins, the deliverable is a documented ruling plus a coherence gate, not data edits.**

---

## 2. The work-list (measured on `02fbb5e8`)

29 renderable cells. `note dur` is the duration stated in the cell's own prose; `verdict` is whether
that duration can fill the field's calendar-month span **under reading B**.

### 2a. NINE cells where the stated duration falls short of the field (the pass's subject)

| cell | field | span | note duration | sources |
|---|---|---|---|---|
| `mid_atlantic` z7 | `Apr - Jun` | 3 mo | **6 wk** | `rutgers_njaes`, `umd_ext` |
| `mid_atlantic` z8 | `Apr - Jun` | 3 mo | 6-8 wk | `umd_ext`, `rutgers_njaes` |
| `mid_south` z7 | `Apr - Jun` | 3 mo | **4-6 wk** | `uada_ext`, `mu_ext` |
| `northern_tier` z5 | `Apr - Jun` | 3 mo | 6-8 wk | `umn_ext`, `msu_ext`, `iastate_ext`, `illinois_ext` |
| `northern_tier` z6 | `Apr - Jun` | 3 mo | 6-8 wk | `msu_ext`, `umn_ext`, `uconn_ext`, `illinois_ext` |
| `northern_tier` z7 | `Apr - Jun` | 3 mo | 6-8 wk | `msu_ext`, `umn_ext`, `mu_ext` |
| `pnw` z8 | `Apr - Jun` | 3 mo | 6-8 wk | `osu_ext`, `wsu_ext`, `wsu_em051e` |
| `se_gulf` z8 | `Mar - May` | 3 mo | 6-8 wk | `uc_ipm`, `uga_b577` |
| `utah_dixie` z8 | `Mar - May` | 3 mo | 6-8 wk | `usu_ext`, `usu_ext_veg_dates`, `usu_washco_dates` |

### 2b. SIX cells that check out (leave alone; use as the control group)

`ca_interior` z8 (8-10 wk), `nevada` z8 (8-10 wk), `nevada` z9 (8-10 wk), `warm_arid` z8 (10 wk),
`northern_tier` z3 (6 wk / 2 mo), `northern_tier` z4 (6-8 wk / 2 mo).

**The pattern is clean and is the strongest single piece of evidence in this brief:** every cell that
checks out either states 8-10+ weeks or spans only two months. Every cell that fails states 4-8 weeks
against a three-month span. That is not noise.

### 2c. ELEVEN cells whose note states NO duration

`ca_desert` z9/z10, `ca_interior` z9, `ca_north_coast` z9/z10, `ca_south_coast` z9/z10/z11,
`low_desert_az` z9/z10, `mid_south` z8, `nevada` z10, `pnw` z9, `se_gulf` z9.

These are **not** cleared, they are **unmeasured** — the note simply does not state a week count, so
the arithmetic check cannot run. Under reading B each needs its source read directly. Most are
California, where the mature duration is well sourced at 8-10 weeks (four independent UC
corroborations), which would justify a three-month span.

---

## 3. The evidence already in hand — do not re-fetch these

All read raw this session (`urllib` + `pypdf` / tag-stripped HTML, never a WebFetch summary).

**`mid_south` z7 is the strongest case, and it is a direct contradiction.** MU G6405, cited on the
cell, states outright:

> "Normal spring harvest extends from April 10 to May 25 in the Missouri bootheel, **April 14 to May
> 30 in southern Missouri**, and April 20 to June 5 in northern Missouri, but harvest time can vary
> by about a week depending on temperature."

The cell is *"the cooler Ozark uplands"* = southern Missouri / north Arkansas → **April 14 to May
30**, roughly 6.5 weeks, ending in **May**. The field says `Apr - Jun`. Note also that MU publishes a
real intra-state gradient (bootheel → southern → northern), which is exactly the differentiation the
dataset lacks.

**`mid_atlantic` z7 carries a GENUINE SOURCE DISAGREEMENT, both cited on the same cell:**

- Rutgers FS1301: *"Harvest all spears for 2-3 weeks from first spear emergence during the third
  growing season, 4-6 weeks during the fourth growing season, and **6 weeks** during the fifth and
  subsequent seasons."*
- UMD: *"When the asparagus plants are in their fourth season, harvest for **8 to 10 weeks** per
  year."*

The field took UMD's end (June); the note took Rutgers' duration (6 weeks). **Per this arc's own
standing rule — established when `harvest_ramp_weeks` year 2 was wrongly collapsed to `[0,0]` —
where sources disagree the data must CARRY THE RANGE, not pick a side.** Whatever else this pass
does, it must not silently choose one.

**Other durations already verified raw:** NMSU H-227 (southern NM) *"From year four on, harvest a
maximum of 10 weeks/year"* + *"the New Mexico asparagus harvest season begins in southern New Mexico
in early March"*; USU *"Harvest for 6 weeks in Year 4 and up to 8 weeks after 5 years"* and *"In most
areas, stop harvest by early to mid-June"*; UC MG statewide *"in their fourth season, they may be
harvested for 6 to 10 weeks per year"*; UC ANR 7234 *"normally harvested once a year over an 8- to
10-week period"* and *"a full cutting season (60-75 days) may begin the fourth year"*.

---

## 4. Method

1. **Rule §1 first.** Everything else is conditional on it. Record the ruling in writing.
2. **If reading B:** for each of the nine, read the cited sources directly and derive the honest end
   from `sourced start (or modeled start) + sourced mature duration`. Prefer a source that states
   **explicit dates** (MU G6405 does) over one that states only a week count.
3. **Then do §2c** — the eleven unmeasured cells — by the same method. Do not declare the pass done
   with them unexamined; "the note didn't say" is not "the cell is fine."
4. **Move the whole cell together.** `harvest`, the `calendar` tokens, and the prose must agree after
   every edit. The `ca_desert` z9 repair is the worked example: three values moved in one guarded
   script.
5. **Write a guarded promote script** per CLAUDE.md: SHA-guarded, asserts every expected pre-state
   value, asserts the invariants after, aborts on drift. Prove it aborts by re-running it.
6. **Full gauntlet** (protocol #6) plus `zone_order_gate` and `prose_window_sweep`, then the state
   trio, then Trevor approves the commit and confirms the push.

---

## 5. Definition of done — this is the part that ends the cycle

**Done is a check that returns zero, not a set of cells that look fixed.**

Every previous pass on this crop fixed instances and left the class open, which is exactly why
defects kept reappearing: the harvest re-source repaired 11 prose notes without scanning all 29, and
5 survived to be found today. Do not repeat that shape.

Ship a **duration-coherence check** alongside the fix:

> for every renderable cell, the harvest window's span must be consistent with that cell's sourced
> mature duration, under the §1 ruling

and drive it to **0**. Then wire it in the way `zone_order_gate` was: standalone and soft first,
measured for flood before choosing scope, TDD with RED proven against the pre-fix canonical from
git. Once it returns zero mechanically, this class is closed permanently rather than until someone
next reads a cell.

**Exit criteria, all four:**
- [ ] §1 ruled and written down
- [ ] all nine of §2a resolved; all eleven of §2c examined
- [ ] a duration-coherence check exists, is TDD-proven RED on the pre-fix canonical, and returns 0
- [ ] gauntlet green, state trio updated, `open_findings` records what was ruled and why

---

## 6. Traps, all of them paid for this session

- **Do not patch prose to match a field.** In these nine the prose may be the correct half. Editing
  it would be the `ca_desert` error in reverse: silencing the half telling the truth and destroying
  the evidence. That is precisely why this pass exists rather than being folded into the prose sweep.
- **WebFetch summaries of PDFs are not sourcing.** A research agent fabricated a document title and
  supporting quotes from one. Use `pypdf` text or raw HTML. `tools/` has no fetcher; the one used
  this session is reproducible in about 40 lines of `urllib` + `pypdf`.
- **WebFetch's markdown parse of an HTML table silently shifts columns.** Pull raw HTML for tables.
- **Search-engine summaries blend sources.** One this session attributed UC ANR 7234's "Central
  Coast: March to mid-June" to a Marin/Sonoma page that says no such thing. Leads only, never
  evidence.
- **Check `source_catalog` before accepting any "fails the tier bar."** County Master Gardener pages
  and extension charts are **T1** today. The catalog is the admission authority.
- **A cited T1 document may not carry the claim.** Five confirmed instances on this crop. Grep the
  fetched document for the crop name before citing it; `auburn_aces` "Simple Guide for **Harvesting**
  Popular Crops" contains zero asparagus.
- **Do not geography-stretch a real source.** UC's "Central Coast" is Monterey/Santa Cruz/SLO and is
  not our `ca_north_coast` or `ca_south_coast`. A stretched citation is worse than none, because it
  looks verified.
- **Commercial windows are not home windows** where the document says so ("if the market is
  favorable", "for an early market") — but in California the home/commercial distinction genuinely
  does not exist in the literature, since Contra Costa MG's home guidance is a verbatim lift from the
  commercial 7234. Judge per document, not by rule.
- **Do not invent differentiation you cannot source.** `nevada` z8/z9/z10 carry one identical value
  across a real elevation gradient and `ca_interior` z8/z9 are identical though their own
  `open_findings` say the foothills differ. Both are honest as labeled. Making them *look* better
  without a source is the failure this whole arc is about.
- **`whole_crop_gate.py` may still carry the artichoke session's uncommitted A48.** Check
  `git status` before touching it; never `git add -A`; use explicit pathspecs.

---

## 7. Why this was handed off rather than finished

Two reasons, and the second is the real one.

1. Context: the session that found this was long and had accumulated a great deal of state.
2. **Anchoring.** That session spent its length establishing that these windows are sound — it
   verified `warm_arid` z8 against NMSU, and it wrote the sourcing-sweep doc concluding the harvest
   gap is honest and should be formally accepted. A session carrying that investment is the wrong
   one to ask "are these windows over-extended?" A fresh reading will judge it more cleanly.

Related: `docs/2026-07-27-state-of-play-and-next-steps.md` (queue),
`docs/2026-07-26-post-asparagus-hardening-kickoff.md` (item 1, the prose-vs-rating gate, still owed),
`docs/2026-07-27-asparagus-harvest-start-sourcing-sweep.md` (why starts stay modeled).
