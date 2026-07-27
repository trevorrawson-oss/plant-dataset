# Handoff to the plant-astro session — corrected bump target + your two questions

**Date:** 2026-07-27
**From:** the dataset lane. **Ownership:** Trevor ruled 2026-07-27 that the **astro lane runs the
bump**, per `CLAUDE.md` and state-of-play §7. No dataset session will touch `plant-astro`.
Nothing here is staged, pointed or half-applied on your side — verified, your tree is as you left it.

---

## 1. Two corrections before you bump

### 1a. The bump target in your spec is stale

`93451d0` is a real commit on `main`, but it is **behind**. It predates both
`6f2b379` (the harvest re-source: 22 of 29 windows changed) and `0c6c229` (the
`harvest_ramp_weeks` year-2 fix). **Bumping to `93451d0` would ship exactly the windows we just
corrected.**

| | value |
|---|---|
| **submodule target** | **`0c6c229`** (`origin/main`, pushed) |
| **canonical SHA** | **`0da1d234`** (`shasum -a 256 crops_data_final.json`) |
| your current pin | `7923579` — 42 commits back |

### 1b. You were right about the live state; our doc was wrong

`docs/2026-07-27-state-of-play-and-next-steps.md` §1 claims your pin is `10eecc0` and that "a
Central Valley user is being shown `Feb - Mar` right now." **That is incorrect and it has been
corrected.** It conflated the *dataset* commit where asparagus certified with the *astro* pin.

Verified against your repo: HEAD, `origin/main` and working tree all pin `7923579` — the ladybug
sweep, which is an ancestor of the asparagus cert. **Production has no asparagus page and no user is
being served wrong asparagus data.** Your read was right, there is no clock, and the bump should
land **with** your `PlantingCalendarCard` fix rather than ahead of it. Correct data rendered by the
annual-calendar branch is still a broken card.

---

## 2. Your two questions

### Q1. "Will artichoke use the same calendar token set as asparagus?"

**No. Flag raised — plan for two renderers, or one with an explicit branch.**

| | asparagus (shipped) | artichoke (staged, `tools/staging/artichoke/cells.py`) |
|---|---|---|
| calendar tokens | **3**: `cold_pause`, `harvest`, `growing` | **6**: `cold_pause`, `harvest`, `growing`, **`plant`**, **`indoors`**, **`season_over`** |
| extra per-cell field | — | **`start_indoors`** (e.g. `"Mar 15 - Apr 15"`), backing every `indoors` run |
| `plant_out` meaning | one-time establishment | **annual replant** in most regions |
| `plant_out` example | `"Apr 10 - May 20 (dormant crowns, one-time planting)"` | `"Jun 1 - Jun 20 (vernalized transplants, replant each year)"` |
| archetype carve-outs | **relies on** the A24/A34/A37 `herbaceous_perennial` exemptions | **deliberately does not** — calendars are authored to pass on their own merits |

The parenthetical *shape* matches, so your existing parser will not break. **The meaning inverts**:
asparagus says "plant once, ever"; artichoke in the northern tier, mid-Atlantic, mid-South and Nevada
says "plant again every year." A renderer that hard-codes asparagus's "plant crowns, one-time" framing
inside a Year 1 view will state the opposite of the truth on most artichoke cells.

The root cause is biological and will not be negotiated away: artichoke in cold regions is grown as a
**vernalized annual** — seed indoors, chill the seedlings, transplant, crop in late summer, lose the
plant to frost. That is why it emits `plant` and `indoors` at all, and why the design explicitly
refuses the perennial carve-outs.

**Caveat, stated plainly:** artichoke is **paused mid-arc and uncommitted**. The cell layer is done
and gate-clean but the canonical has none of it (artichoke still shows 10 regions, 0 calendared
cells). The token set above is read from their staging file and is the current design intent, not a
shipped fact. Treat it as a firm heads-up for planning, not a spec to build against — re-confirm at
their cert.

### Q2. "Are the 10 unsuitable asparagus cells expected to stay without `plant_out` permanently?"

**Yes — permanently, and by design in the gates, not by omission.**

Both floors that force these fields carve `unsuitable` out explicitly and identically:

- **A47** `perennial_plant_out_gate` — `SKIP_SUITABILITY = {"unsuitable"}`
- **A48** `perennial_harvest_gate` — same, with the stated reason: *"never promise food where the
  crop will not grow"*

The 10 cells are `ca_desert` z11, `fl_peninsula` z10/z11, `hawaii_tropical` z10/z11/z12/z13,
`rgv` z9/z10, `se_gulf` z10. They carry a minimal honest calendar plus a dormancy-reason note that
dominates ("skip asparagus here"). Your instinct to render no crown cell rather than guess is
exactly right and matches the dataset's intent.

This also aligns with the hardening item-4 display ruling: `unsuitable` **hides** · `survives_no_fruit`
shows flagged ornamental-only · `marginal` shows with caveats · positive values render normally.

---

## 3. Everything you asked us to keep publishing — confirmed present on `0da1d234`

| field | state |
|---|---|
| `perennial` | present on **all 128 crops**, zero missing; `true` on 38 |
| `calendar_basis: frost_anchored` | unchanged on asparagus |
| `plant_out` parenthetical convention | unchanged |
| `year_one_notes_beginner` / `_seasoned` | both present |
| `harvest_ready_beginner` / `_seasoned` | both present |
| `establishment_years: 5` and `years_to_first_harvest: [2,3]` | both present and **kept distinct** |

Your `[zone].astro:131-142` finding — perennial archetypes routed off `calendar_basis` — is a real
bug and we will keep `perennial` populated on every crop so your fix has a reliable signal.

---

## 4. One thing that changed under you, worth knowing

`harvest_ramp_weeks` year 2 shipped as `[0,0]` and was corrected to `[0,2]` in `0c6c229` after the
plant-app session caught it. If you render anything off the ramp, note that **year 2 is a conditional
light cut, not zero**, and that `years_to_first_harvest: [2,3]` is a genuine source disagreement
expressed as a range — the two must agree.

Separately: the ~20 asparagus cells whose `harvest_resolution_method` is
`harvest_sourced_duration_modeled_start` are **staying modeled**. An 18-document re-sourcing sweep
(`docs/2026-07-27-asparagus-harvest-start-sourcing-sweep.md`) established that no home-garden
extension source publishes a regional harvest *start* month at all. Your "fewer honest cells beat
more inferred ones" principle is the right one; the honest label is doing the work here.
