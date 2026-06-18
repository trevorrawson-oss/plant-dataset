# Strawberry -- Steps 1-3 kickoff (anchor 13, the FIRST berries_herbaceous crop)

> **DRAFT for Trevor to voice + send.** This is the structural/factual frame (starting state, lane split, scope, gate commands, source pointers) Claude Code assembled. The final prompt + framing are yours -- adjust and send to claude.ai.

**Arc:** Bring `strawberry` from an empty author-fresh shell to gold-standard. Strawberry is anchor 13 and the **only `berries_herbaceous` crop** in the dataset, so this arc is the archetype's whole schema stress-test. The model is already DESIGNED + APPROVED -- see `DESIGN_SPEC.md` (Trevor 2026-06-18). Author to it; do not re-open the model.

**At session start:** read `CURRENT_STATE.md` + `STATE_HISTORY.md` (both in this bundle); preflight `sha256(crops_data_final.json)` against `LATEST.txt`. Start SHA at design time: `6f48eb11...`.

**This kickoff covers Steps 1-3 only** (the claude.ai authoring that opens the arc). The Claude Code structural lane (the new gates + the region-shell builder + the calendar deriver) is **already BUILT, test-first, and pushed** -- it waits for your Step-3 output to run Step 3.5. So: author Steps 1-3, hand back the JSON, Claude Code runs 3.5, then you pick up Steps 4-8.

---

## Lane split

- **Claude Code (DONE this session):** `berry_calendar.py` (deriver + A11 coherence), `berry_herbaceous_gate.py` (A10 structural cert), wired into `whole_crop_gate`; `build_region_shells` `perennial_herbaceous` path; design spec + plan. Commits `d2f6ff6` / `f486cea` / `20357e8` / `fb0ac52` on `main`.
- **claude.ai (THIS kickoff -- Steps 1-3):** source set, the Step-2 scalars/structured fields, the companion walk -- all authored to the approved design.

---

## Starting state (verified 2026-06-18)

`strawberry` is an honest author-fresh shell: `verification_status.status` null, `source_set` empty, every 2.9 perennial field null-scaffolded, region + zone shells present but unfilled. `whole_crop_gate strawberry` currently reports **10 violations** -- these are the expected unfilled-shell gaps (null region notes, etc.), not regressions. A10/A11 currently no-op because the basis is still `frost_anchored` (it flips to `perennial_herbaceous` at Step 3.5, after your Steps 1-3 land).

---

## The model in one screen (full detail in DESIGN_SPEC.md, D1-D9)

- **One guide**, June-bearing matted-row SPINE; the type choice (June-bearing / day-neutral / everbearing) ELEVATED to a first-class section, not buried in varieties.
- **calendar_basis -> `perennial_herbaceous`** (set by Claude Code at 3.5, not by you); frost resolution stays ON.
- **Per-cell `grown_as` (perennial | annual)** carries the region-dependent lifecycle -- north perennial, hot-summer CA/FL annual. (A Step-4 field; not your Steps 1-3 job, but author the scalars knowing it exists.)
- **Propagation:** `start_method.start = "bare_root_dormant"` (the peach/apple value). Plugs/runners/seed are prose nuance.
- **Photoperiod is NOT an onion-style gate:** type is a VARIETY attribute. Do NOT add `gating_factors: ["photoperiod"]`. `self_fertile: true`, no cross-pollination calendar.

---

## Steps 1-3 -- what to author

**Step 1 -- Source set.** Establish strawberry's T1 sources (university extension / USDA / peer-reviewed only). Starter pointers in `SOURCE_POINTERS.md` -- verify + admit them yourself; that file is a lead list, not a verified set.

**Step 2 -- Scalars + structured fields** (with field-level `sources` + `anchoring_urls`):
- `soil`, `ph`, `container_notes` (strawberries are container/raised-bed friendly -> `container_ok: true` + `min_pot_gallons`), `spacing_inches`.
- `succession_policy.suitable = false` (strawberry is not a succession crop).
- `start_method.start = "bare_root_dormant"`; `hardening_off_*` = honest N/A prose (dormant crowns do not harden off).
- **The 2.9 perennial scalars (these are the new archetype's core -- author per the spine):** `self_fertile = true`; `establishment_years`; `years_to_first_harvest` (June-bearing matted row: year 2 after pinching); `years_to_full_production`; `productive_lifespan_years` (~3-4 yr matted-row bed); `hardiness_zone_min/max` (survives, with mulch) vs `reliable_fruit_zone_min/max` (fruits well) -- keep distinct; `chill_hours_required`/`chill_hours_range` if a clean T1 figure exists, else leave null + author honest `chill_hours_note_*` (chill is INFORMATIONAL, never a gate).
- `archetype` is already `berries_herbaceous` (do not change).

**Step 3 -- Companion walk.** Full rigor; the certified carrot rich-object shape; vocab `research_backed` / `likely` / `traditional`.

**NOTE on the gate:** A10 (`berry_herbaceous_violations`) asserts the lifecycle SCALARS are present once the basis is `perennial_herbaceous`. They are Step-2 data, so they must be authored before Step 3.5 sets the basis -- this kickoff's Step 2 is where they land.

---

## Gate commands (Claude Code runs these; listed so you know the bar)

```
python3 tools/whole_crop_gate.py strawberry          # incl. A10 structural + A11 calendar coherence
python3 tools/register_completeness_gate.py crops_data_final.json
python3 tools/register_fill_gate.py strawberry       # at Step 11 -- no null register prose
```

---

## What to hand back

The authored `strawberry` crop object (Steps 1-3 filled) + a STATE_HISTORY snippet, in the canonical patch format. Claude Code verifies + applies, then runs Step 3.5 (`build_region_shells` -> the basis flips + the 10 region shells build), and the arc continues to Steps 4-8 (the per-region `grown_as` + crown windows + the DERIVED calendars + the bulk prose).
