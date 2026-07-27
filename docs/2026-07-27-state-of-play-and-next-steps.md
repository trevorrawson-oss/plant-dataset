# State of play + next steps

**Date:** 2026-07-27
**Purpose:** one place to see what is done, what is in flight, and what each queued session is for.
Written at the end of the asparagus timing + suitability + harvest work, with the artichoke arc
running concurrently.

---

## 1. Where asparagus actually stands

Certified crop #120. Canonical `79862bc3`, pushed (`origin/main` `6f2b379`). Gauntlet green
throughout: `gate_all` 120/120, `release_verify` CLEAN, A47 hard 0/128.

Shipped across five passes today and yesterday:

| | before | after |
|---|---|---|
| `plant_out` | 0 of 39 cells | **29 cells** (every `perennializes` + `marginal`) |
| `harvest` | 0 cells, then 29 all exactly 2 months | **29 cells**, 22 corrected, spans now 2-3 months |
| `establishment_years` | `null` | **5**, independently sourced |
| `year_one_notes` | absent | authored, both registers |
| suitability split | 18 / 8 / 13 | **25 / 4 / 10**, on a sourced mechanism |
| `harvest_ramp_weeks` | — | **new field**, bed-age ramp (pilot) |
| gates | — | **A47 hard**, A24 dormant-planting carve-out |

**It is LIVE** (small tester group) — and the site currently serves the *pre-fix* harvest windows,
because the plant-astro submodule still points at `10eecc0`. A Central Valley user is being shown
`Feb - Mar` right now.

---

## 2. Asparagus: what is left

### 2a. The honest gap — unsourced harvest starts (the real remaining work)

Duration is well sourced roster-wide. **Starts are not.** Only these carry a start sourced for
their own geography: `northern_tier` z3-z6, `mid_atlantic` z7, `mid_south` z7, `warm_arid` z8,
`ca_interior` z9, `low_desert_az` z10. Everything else is
`harvest_resolution_method: harvest_sourced_duration_modeled_start`.

**No T1 source was found for:** all three `nevada` cells, `utah_dixie` z8, `pnw` z9,
`mid_atlantic` z8, `se_gulf` z8/z9 starts.

**This is now re-openable**, for a reason that did not exist when the gap was created: county
Master Gardener calendars were being treated as too weak to cite, and they are not (see §3).
Several of those cells probably have a sourceable start sitting in a county MG document.

Also worth re-checking: **no source starts asparagus harvest in March anywhere in the
mid-Atlantic, mid-South or PNW**, so the pre-fix values there were unsupported and may have been
read off crown-**planting** tables (Clemson's "Planting Dates for Crowns", UGA B577, UMD HG16 all
publish Feb-Apr *planting* windows that resemble the old *harvest* strings).

### 2b. Register `harvest_ramp_weeks` — a loose end, ~15 minutes

The field shipped as an asparagus pilot and the intent was always a roster-wide rollout across the
25 establishment crops. **It was never added to `docs/field_addition_register.md`.** Add it with the
trigger condition (stable roster — artichoke is mid-cert) so it does not get lost. Include the
year-counting hazard: sources use three incompatible conventions ("year after planting crowns",
"year the plants are in the garden", "harvest year") that describe the same season; ours counts
seasons in the ground from a one-year-old crown.

### 2c. The plant-astro bump

Owned by the astro lane, not this repo. It matters more than it did: the live site is serving
harvest windows we now know are wrong. Their working tree has in-flight asparagus artwork and a
`PlantingCalendarCard` change, so they should stage the submodule pointer explicitly
(`git add plant-dataset`) rather than `git add -A`, and run `npm run build` after.

### 2d. The app-side fix

`isPerennial = crop.perennial === true`. Still the single change that surfaces any of this to a
user, and it corrects **9 crops**, not just asparagus.

---

## 3. Preventing the sourcing failure — mostly already in flight

**The artichoke session has already written `docs/2026-07-27-source-tier-model-kickoff.md`.** Read
that first; it is the primary artifact and it measured the model rather than assuming it.

Its central finding matches this session's experience exactly: tier errors ran **in the direction
of rejecting sources the dataset already trusts**, and *"an over-strict bar does not produce
silence, it produces unsourced derivation."*

**What I did not know, and what needs to be common knowledge:** `T2` is not "second-best
extension." Measured, all nine T2 entries are the **seed-trade and folklore band** — Old Farmer's
Almanac, Johnny's, seed companies, a gardening blog. **County Master Gardener pages, county
planting calendars and extension charts are T1.** Not knowing that, I repeatedly downgraded or
discarded usable sources: I flagged an NMSU Master-Gardener-hosted chart as "lower provenance,"
hedged on county MG programs, and left cells unsourced that were probably sourceable. That is how
the "honest gap" in §2a got as big as it is.

**One correction this session contributed**, which belongs in the tier work: the four asparagus
citation defects were **not** tier failures. All four were `tier: T1`, `source_class:
university_extension` — genuine extension documents from real land-grant institutions, cited for
claims their documents do not contain. `unr_fs0261` *is* a UNR Extension fact sheet; its only
mention of the crop is `"Stems - asparagus"` in a list of edible plant parts. And PlantVillage, the
source of the invented chill mechanism, **was never in the catalog at all** — it entered through
research reasoning, not a citation.

**So tier and claim-support are two different axes, and tier discipline cannot catch claim-support
failure.** Both need addressing; they are not substitutes. Tier is §3 (in flight); claim-support is
§5 (the cleanup arc).

---

## 4. Hardening pass — written, queued

`docs/2026-07-26-post-asparagus-hardening-kickoff.md`. Four items, already scoped with
reproduction commands:

1. **The region-prose vs cell-rating coherence gate.** Surface measured at 37 assertions across 13
   crops; 12 are long-certified fruit trees whose prose layer has never been checked. **Audit
   before gating.**
2. Re-source or formally accept three thin asparagus values.
3. Rule the `verification_log_ref` convention.
4. `unsuitable` cells: the fabricated all-`growing` calendar, and the four-state display rule
   (`unsuitable` hides · `survives_no_fruit` shows flagged **ornamental-only** · `marginal` shows
   with caveats · positive values show normally).

**Item 1 got materially more urgent today.** I reproduced that exact defect — 11 cell notes and 6
region-note pairs left describing old harvest windows — **within an hour of documenting it**, while
actively watching for it. It is not solvable by attention.

---

## 5. Dataset cleanup arc — citation integrity (NOT yet written)

The evidence: asparagus had **4 bad citations out of ~21 sources (~19%)**, and all four survived an
11/11 T1 source-truth sample. The roster carries **2,660 citation pairs across 1,153 distinct
URLs**. Even at 5% rather than 19%, that is ~57 bad citations in certified data.

A bad citation is worse than a missing one, because it *looks* verified — and "T1-or-it-doesn't-
ship" is the product's actual moat.

Tractable because two tiers are automatable:

| tier | check | cost | would have caught |
|---|---|---|---|
| A | does every cited URL resolve? | 1,153 fetches | a self-constructed URL that 404'd |
| B | does the document mention the crop at all? | same fetches + a grep | `unr_fs0261` |
| C | does it support *this specific claim*? | manual, sampled | `ucanr_ext`, `msu_ext` |

A + B would have caught **2 of asparagus's 4** mechanically, roster-wide, in one scripted pass.
Weight tier C toward cells whose claims rest on a single source — that is exactly where the
asparagus sample failed.

**Expect link rot as a separate category:** UF/IFAS HS546 already 410s on its live URL while the
content is fine via archive. "Dead but correct" is not the same defect as "live but wrong."

Two things belong in this arc that are not citation checks but are the same trust surface:
- **The WebFetch-PDF fabrication hazard.** A research agent this session invented a document title
  and supporting quotes for a handbook containing no asparagus content, from a WebFetch *summary of
  a PDF*. Worse than the known table-column-shift issue because it invents rather than garbles.
  Operating rule: **WebFetch summaries of PDFs are not sourcing** — pypdf text or raw HTML only.
- **Cells that contradict their own cited sources.** `ca_interior` z9 cited Pub 7234 and asserted a
  harvest window that source directly contradicts. That is tier C's most valuable shape.

---

## 6. What is missing from the list

### 6a. The pattern underneath my own errors

Three times this session I asserted something about existing data without verifying it, and each
produced a real defect:

1. Harvest strings "derived deterministically from the calendar tokens, no re-sourcing needed" —
   the tokens were *modeled*, and the result contradicted a source cited on the same cell.
2. "Align asparagus with the fruit trees, which leave unsuitable calendars empty" — they are not
   following a convention, they are **exempt** (A32 no-ops off `frost_anchored`).
3. A blanket dormancy note applied across a class — true for summer-wet regions, **false for the
   arid Arizona desert**, where a dry-down is exactly what the climate supplies.

The common shape: **trusting data because it is already in the file.** §5 tier C addresses the
citation half. Nothing yet addresses the derivation half — that a value derived from other data
must be re-checked against the sources of the data it came from. Worth a rule at minimum, in
`CLAUDE.md` alongside the TDD rule.

### 6b. Session hygiene

This session is very long and has accumulated a lot of context. **Each queued item should start
fresh**, reading the relevant kickoff, not continue here. All the needed context is in the
kickoffs, `CURRENT_STATE.md`, and `STATE_HISTORY.md` precisely so that is possible.

### 6c. Coordination with the artichoke session

They are live in this same checkout with uncommitted work (`whole_crop_gate.py`, staged artichoke
files). They built **A48**, an archetype-scoped harvest floor — the complement to A47, closing the
half of the asparagus defect A47 could not reach. Whoever runs next should pull first and check
what landed; do not assume `whole_crop_gate.py` is what this document describes.

### 6d. Suggested order

1. **plant-astro bump** — live users are seeing wrong data now; smallest fix, biggest immediate effect
2. **Asparagus honest gap (§2a) + register the ramp (§2b)** — small, and §3 just unblocked the sourcing
3. **Artichoke finishes** (in flight) — the roster must be stable before column passes
4. **Hardening pass (§4)** — item 1 first, audit before gate
5. **Cleanup arc (§5)** — the largest, and the one that protects the trust claim

---

## 7. Standing rules worth restating

- Canonical JSON is COMPACT; write via a promote script, never by hand. Promote scripts should
  guard their assumptions and abort on drift.
- TDD RED before GREEN on any gate, and prove a *neighbouring* crop still bounces.
- Verify every citation supports its **specific claim**, and that its URL resolves.
- **WebFetch summaries of PDFs are not sourcing.**
- After changing any value, re-read the prose that describes it — cell notes *and* region notes.
- Nothing commits without Trevor's approval; he confirms every push.
- No plant-astro bump from a dataset session.
