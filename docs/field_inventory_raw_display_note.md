# plant — Field Inventory Addendum: Raw-Display vs Mapped-Token strings

**Status:** AUTHORITATIVE addendum to `register_bearing_field_inventory_v1_0.md` (the USER-FACING-CATEGORICAL bucket, §1). Authored 2026-06-25 (CC lane, promoted for project knowledge). Closes a gate blind spot the 2026-06-25 scan surfaced.
**Enforced by:** `tools/raw_display_gate.py` (`whole_crop_gate` **A23**) + `tools/field_classification.is_raw_display`.

---

## The one-paragraph rule (for authoring)

A small set of user-facing fields are printed **verbatim** by the guide cards — no humanizer, no label map. Their values are **human-readable prose**, never snake_case tokens. Authoring `fertilizer.type: "nitrogen_forward"` or `sunlight: "full_sun"` ships the underscore straight to the grower (it renders literally as "nitrogen_forward"). Write `"Nitrogen-forward"` and `"Full sun"` instead — match the register of the already-clean anchors (cherry's `fertilizer.type: "Tomato fertilizer"`, `frequency: "every 2 weeks"`). This is the **inverse** of the schema's real categorical-token fields (`start_method.start`, `companions[].category`, `container_notes.shape_requirements`, `soil.organic_matter_preference`), which the renderer **maps or humanizes**, and which therefore stay snake_case on purpose. The contrast is the whole point: prose fields hold prose; token fields hold tokens.

---

## 1. RAW-DISPLAY fields — render VERBATIM → must be human-readable prose

The card prints the value as-is. A snake_case value is a bug. (`is_raw_display` returns True; A23 flags a snake_case value.)

| Field | Render site (verbatim) |
|---|---|
| `fertilizer.type` | FeedingCard feeding grid — explicitly "no Title Case manipulation" (audit F3) + app `guide-chapters` |
| `fertilizer.timing` | FeedingCard "When to start" + app |
| `fertilizer.frequency` | FeedingCard "Frequency" + app |
| `sunlight` | CareGuideCard prints `crop.sunlight` as-is (HeroCard + app *do* humanize it; CareGuideCard does not — so the data must already be prose) |
| `companions[].timing` | CompanionsCard `comp-timing` div, verbatim |
| `watering.watering_method` | **display-intent**: not currently wired to a card (the prose `method_seasoned`/`method_beginner` render instead), but meant to be human-readable (Trevor 2026-06-25) — gated as honest prose |
| `watering.drought_tolerance` | display-intent, same as above |

## 2. MAPPED-TOKEN fields — renderer maps/humanizes → stay snake_case (EXEMPT)

`is_raw_display` returns False; A23 never flags these. They are legitimate controlled vocabularies.

| Field | How the renderer handles the token |
|---|---|
| `start_method.start` | an **enum** (`isBareRoot === 'bare_root_dormant'`, `today.ts` `=== 'indoors'`) + a capitalized label. Changing the value to prose would break the logic. |
| `companions[].category` | CompanionsCard `CATEGORY_META` label map (`pest_deterrent → "Pest deterrent"`) |
| `container_notes.shape_requirements`, `soil.organic_matter_preference`, `soil.drainage_requirement`, `soil.*_texture_*` | label-mapped or `replace(/_/g, ' ')` humanized at render |
| `gating_factors`, `suitability`, `day_length_type`, `recommended_type`, calendar `phase` tokens, notification `action`/`condition`/`offset_from`, `evidence_label`, planting `label` | structural/enum tokens; either humanized at render or never displayed |

## 3. Why a gate AND this note

A gate alone is a treadmill: the bots author snake_case → hit A23 → fix, every batch. The **source** fix is this note + the clean exemplars (the register reference in §1), so the prose is authored right the first time. A23 is the backstop.

**A23 is an allowlist, by design.** It scans only the §1 fields, never "every user-facing string" (that would false-positive on the §2 tokens). The cost: a *new* raw-display field — a new card rendering a new dataset string verbatim — is invisible to A23 until added. **When a new card renders a dataset string verbatim, add its path to `RAW_DISPLAY_PATHS` (or `is_raw_display`) and to §1 here.**

## 4. Companion `category` / `start_method.start` are renderer-side, not data

The §2 tokens are correct as data, but two of them currently **under-humanize at render** (a website bug, not a dataset bug): `CATEGORY_META` maps only 4 of the ~12 authored categories (the rest fall back to the raw key as the group header), and `StartingIndoorsCard` capitalizes only the first letter of `start_method.start` (so `nursery_transplant` → "Nursery_transplant" for lavender). Those are fixed in the **plant-astro renderer** (expand `CATEGORY_META` + humanize the fallback; humanize the start label), never by de-snake-casing the data. Tracked with the submodule bump.
