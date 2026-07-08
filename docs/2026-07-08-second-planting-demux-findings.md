# 2026-07-08 -- `second_planting` de-multiplexing: findings + scoped fix

**Trigger:** Trevor's question -- broccoli, `ca_interior` (interior valley) **zone 9**: why is it "indoors in Nov but not July?"

**Status:** READ-ONLY on canonical. Nothing edited. This is a corrections-log / scoping item; the fix is held for Trevor's go-ahead.

---

## 1. The direct answer to the question

broccoli in a hot interior-valley z9 runs as **two crops**, because it can't form a head in the May-Jul heat (`heat_pause.months = [5,6,7]`, "heat above ~86°F day / 77°F night stops broccoli from forming a usable crown"):

| crop | start indoors | transplant | harvest |
|---|---|---|---|
| **spring (primary)** | `Nov 1 - Nov 22` | Dec 1 - Feb 28 | Mar 1 - May 1 |
| **fall (second_planting)** | `Jun 20 - Aug 18` | Aug 1 - Sep 30 | Oct 15 - Dec 15 |

**July is the FALL crop's indoor start, and it IS in the data** -- `regions.ca_interior.resolved_by_zone.9.second_planting.start_indoors = "Jun 20 - Aug 18"`. It is not missing.

Per the `second_planting` design (`docs/superpowers/specs/2026-06-05-second-planting-region-shell-model-design.md`, §3):
- `PlantingCalendarCard` (beginner + seasoned) renders the **primary** cycle and **deliberately MASKS the second planting** "so it never implies what I plant in March produces through December."
- `SuccessionCard` (**seasoned-only**, hidden in beginner mode) reads `second_planting{}` directly and is where the fall cycle (incl. the July indoor start) is meant to surface.

So "indoors in Nov, not July" is the **main-card / beginner** behavior by design: Nov is the spring (primary) start; July is the fall crop, carried in `second_planting` and surfaced only on the seasoned `SuccessionCard`.

> **Correction to my first take.** I initially guessed the top-level `start_indoors` should *merge* the second window. The spec is the **opposite**: the top-level main window is a **single primary window** (the second window was *de-multiplexed* out into `second_planting{}`). So `start_indoors = "Nov 1 - Nov 22"` (primary only) is **correct**.

---

## 2. The real data defect: incomplete / inconsistent de-multiplexing

The de-multiplexing (moving the 2nd window out of the comma-separated main strings into `second_planting{}`) was applied **field-by-field, inconsistently**. Of the **64** `resolved_by_zone` cells that carry a `second_planting`:

- **16** fully de-multiplexed (all three main fields = primary only) -- correct.
- **0** fully doubled.
- **48 MIXED / internally incoherent** -- some main-window fields de-multiplexed, others still carry **both** windows comma-joined.

Representative patterns:

| cell | still-doubled (holds both windows) | de-multiplexed (primary only) |
|---|---|---|
| broccoli `ca_interior` z9 | `plant_out`, `harvest` | `start_indoors` |
| broccoli `se_gulf` z8/z9 | `harvest` | `start_indoors`, `plant_out` |
| cherry/beefsteak/roma-tomato `se_gulf`/`ca_desert`/`warm_arid`/`low_desert_az` (18 cells) | `start_indoors`, `plant_out` | `harvest` |

So on 48 cells the three main-window fields **disagree** about whether they've been split. broccoli z9 is exactly this: a single spring `start_indoors` (Nov) paired with a doubled `plant_out` (`Aug 1 - Sep 30, Dec 1 - Feb 28`) and doubled `harvest` (`Mar 1 - May 1, Oct 15 - Dec 15`) -- internally incoherent on the main card.

---

## 3. Root cause (tooling)

- The top-level resolved windows are **authored/resolved at the claude.ai Step 4/5 lane** (`resolution_method = frost_anchored_resolved`) and applied. **No tool de-multiplexes them.** The 2026-06-05 spec said "the main window de-multiplexes back to a single window," but that step was done by hand per field, so it landed partially.
- **No gate enforces the de-mux invariant.** `whole_crop_gate` only checks that a `second_planting` carries the four window keys (`SECOND_PLANTING_KEYS`); it never checks that the **main** window *excludes* the second_planting window. A MIXED cell ships clean.
- `derive_annual_calendar` reads only the top-level `plant_out`/`start_indoors`/`harvest` (never `second_planting`), and the `calendar[]` is hand-authored anyway, so the 12-month array shows both cycles regardless. The `indoors` token is **lowest precedence** (`heat_pause > plant > harvest > indoors`), so `start_indoors` rarely becomes an `indoors` month -- for broccoli z9, Nov is a harvest month, so the calendar shows **no `indoors` token at all**. The app's indoor-start display therefore comes from the window **string**, not the calendar array.

---

## 4. Scoped fix (deterministic; HOLD for go-ahead)

1. **Complete the de-multiplexing** on the 48 MIXED cells. For any still-doubled main field, `PRIMARY = (top-level comma-list) MINUS (the second_planting window)`; set the field to the primary span only. This is **deterministic** because `second_planting` already holds the exact second window to subtract. Also correct `harvest_start`/`harvest_end` to the primary window's ends (broccoli z9: `harvest -> "Mar 1 - May 1"`, `harvest_end Dec 15 -> May 1`), and review `first_plant_date`/`last_plant_date` per cell.
2. **`calendar[]` unchanged** -- it is the full-year both-cycles overview (hand-authored); de-mux touches only the main display-window strings. Re-run `calendar_coherence_gate` + annual A5/A24 to confirm no regression.
3. **New gate (TDD, RED before GREEN): the de-mux invariant.** In `whole_crop_gate`: if a cell has a `second_planting`, none of the top-level `start_indoors`/`plant_out`/`harvest` may CONTAIN the `second_planting` window as a comma-span, and the three fields must AGREE on de-mux state. Inject a MIXED cell into a scratch copy of the real canonical and confirm it bounces before trusting it. (Two-for-one: the correction unlocks the gate.)
4. **Cross-repo caveat -- MUST coordinate with plant-astro.** De-muxing removes the fall window from the top-level `plant_out`/`harvest` strings. If the plant-astro **`SuccessionCard` is not yet wired to read `second_planting{}`** (the spec calls the read-layer flip "Phase C," future; but the interior-valley view already reads `regions{}`, so it may be partial), then de-muxing would **hide the fall crop from the main card without it reappearing on a SuccessionCard** = net UI loss. Confirm `SuccessionCard` reads `second_planting.{start_indoors,plant_out,harvest_start,harvest_end}` before/with the data fix.

---

## 5. Separate product question (not a data fix)

If we want the fall-crop indoor start (July) visible in **beginner** mode too -- not just the seasoned `SuccessionCard` -- that is a plant-astro rendering/product decision. The data already carries it in `second_planting`.

---

## 6. Evidence (reproduce)

- Cell dump: `regions.ca_interior.resolved_by_zone.9` (broccoli).
- De-mux coherence scan: 64 second_planting cells -> 16 clean / 48 MIXED / 0 doubled (script in the 2026-07-08 session transcript).
- Calendar derivation: `derive_annual_calendar` on broccoli z9 is identical with Nov-only vs merged `start_indoors` (the `indoors` token is masked by higher-precedence `harvest`/`heat_pause`), confirming the display comes from the window string, not the calendar array.

---

## 7. UPDATE (2026-07-08) -- TRUE SCOPE + where the work lives

A follow-up scan corrected the scope. The §2 "48 MIXED cells" is only the population that *already has* a `second_planting{}` object. The real picture:

- **Population 1 -- 64 cells WITH a `second_planting{}`** (tomatoes, broccoli, kohlrabi, celery). Their still-doubled top-level windows are **exact byte copies** of the `second_planting` span (84 duplicate windows). De-mux here = pure **dedup**; the data survives in `second_planting`. Zero loss.
- **Population 2 -- ~983 multi-window top-level fields (a few hundred cells) with NO `second_planting{}` at all** (bell-pepper, jalapeno, and most warm-region two-season crops). Their spring+fall windows live **only** in the comma-separated strings; they were never migrated to the structure.

So the `second_planting` migration (2026-06-05 spec) was only ever partially rolled out. Most two-season crops still carry both windows as comma-strings.

**Consequence for the fix -- it is a MIGRATION, not a strip.** For population 2 the plan must **extract the second window INTO a new `second_planting{}` object FIRST, then clean the top-level string** -- a naive "remove the second span" would delete a planting that has no structural home. Done extract-then-clean, nothing is lost: every planting is either already structured (pop 1, dedup) or moved into the structure (pop 2).

**Where the work lives (Trevor Q, 2026-07-08):**

| piece | repo |
|---|---|
| extract into `second_planting{}` + clean top-level strings | **plant-dataset** (canonical source of truth; plant-astro embeds it read-only) |
| flip `SuccessionCard`/`PlantingCalendarCard` to read `second_planting{}` instead of parsing the comma-string | **plant-astro** (Phase C read-layer flip) |

**Staged so the UI never loses the fall crop:**
1. plant-dataset: *populate* `second_planting{}` for every two-season cell (additive -- top-level stays doubled, nothing breaks).
2. plant-astro: flip the cards to read `second_planting{}`.
3. plant-dataset: *then* clean the top-level strings to single-window.

This is a larger migration than §2-§4 implied (hundreds of cells + the app read-layer flip), which is why it stays a separate, properly-scoped follow-up -- NOT folded into the heat-gap flip.
