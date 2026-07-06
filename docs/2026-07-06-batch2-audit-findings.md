# Batch-2 audit findings — pre-authoring anchor check for the seed→harvest timing spine

**Date:** 2026-07-06 · **Canonical at audit:** `b67b0101` → `3358d496` (after the one fix below) ·
**Scope:** the 34 batch-2 crops (roster 80 → 114 certified) · **Mode:** read-only; the single fix was then
applied deliberately.

## Why this doc exists
The app's next build is a **seed→harvest timing spine** — sow depth, a structured germination window,
per-stage day offsets, a **days-to-maturity anchor flag (from-sow vs from-transplant)**, harvest windows,
and a **propagule** field. Every one of those anchors to five existing fields. An error in a stage ladder,
a DTM, or a mislabeled start method propagates straight into computed timing a grower relies on. This
audit verified those anchors **before** the new fields are authored on top of them. **The timing spine
should treat this doc as its anchor-truth reference.**

The five anchor fields audited across all 34: `start_method.start` (+ `weeks_before`/`weeks_indoors`,
`hardening_off`), `germination_temp_f`, `spacing_inches`, `growth_stages` (ladder + any per-stage days),
and the propagule honesty of `start_method`.

---

## Bottom line
The batch is **sound**. One real anchor gap (lime — **fixed this session**), plus notes below that the
timing spine must design around. No safety/health errors, no propagule mislabels, no structural or
regression issues. All 114 certified crops pass `whole_crop_gate`; all 113 cited sources are catalogued +
T1; canonical/LATEST/origin/plant-astro are in sync.

---

## 1. Propagule honesty — PASS (but the detail is in prose, not structured)
**No crop is falsely labeled seed/direct when it is actually started from a vegetative propagule.** The
propagule crops say so honestly in `start_method` **prose**:

| crop | structured `start` | real propagule (from its prose) |
|---|---|---|
| sweet-potato | `transplant` | **slips** — "grown from slips… not from seed and not from seed-potato pieces" |
| mint | `transplant` | **division / rooted cutting** — "not from seed… seed does not come true" |
| lemongrass | `transplant` | **division / rooted grocery-store stalk** |
| grapefruit, mandarin-clementine, **lime** | `grafted_nursery_tree` | **grafted nursery tree** |
| rosemary, sage, thyme, oregano | `nursery_transplant` | nursery/cuttings (seed possible; slow for rosemary) |
| bee-balm, echinacea, chives | `both`/`transplant` | seed **or** division |

**→ Timing-spine action:** the new `propagule` field can be populated **straight from the existing
`start_method` prose** — the honest detail (slips / division / cuttings / grafted-tree / seed) is already
there, it just isn't structured yet. The generic `start` enum (`transplant` / `grafted_nursery_tree`)
does **not** by itself distinguish a vegetative propagule from a seedling transplant.

## 2. The one real gap — FIXED: `lime.start_method.start` was null
`lime.start_method.start` was `None`, while its citrus siblings grapefruit and mandarin carried
`"grafted_nursery_tree"`. Lime's own prose was correct ("plant a young nursery tree"), so it was just an
unset structured anchor — but the timing spine's start-method anchor would have returned null for lime.
**Fixed** (SHA-guarded, amend-not-recert): `lime.start = "grafted_nursery_tree"`, per-field provenance note
appended to lime's `verification_log_ref`. Lime was the **only** null-start in all 34.

## 3. Timing-spine notes — surfaced, NOT changed (design around these)
- **DTM convention split (affects the from-sow-vs-from-transplant anchor flag).** Woody perennials
  (rosemary/sage/thyme/oregano) **and citrus** carry `days_to_maturity = []` (empty — perennials have no
  annual DTM). Herbaceous perennials (mint, chives, lemongrass, bee-balm, echinacea) carry DTM **values**
  (establishment-to-harvest). Annuals/microgreens/flowers carry normal DTM. The timing spine must handle
  the empty-DTM perennials (trees + woody herbs) distinctly from the herbaceous ones, and decide the
  from-sow vs from-transplant anchor per archetype (e.g. most annuals here are DTM-from-transplant for the
  indoors-started ones, from-sow for direct-sown).
- **growth_stages ladder counts are archetype-consistent:** 6 (annuals/flowers), 5 (herbaceous
  perennials, microgreens, mint/chives/echinacea), 4 (lemongrass). **lemongrass = 4** (establishment →
  vegetative → mature → harvest) lacks the dormancy/spring-regrowth that mint has — this is
  archetype-appropriate for a **tender** perennial (grown as annual / overwintered), but confirm it's what
  the spine expects for the per-stage day offsets.
- **sweet-pea in-row spacing `[3,6]` in** vs Cornell's ~8 in: legitimate intensive cut-flower spacing.
  (NCSU's "3–6 ft" is *available space / spread* — a different metric — so it does not contradict the
  `[3,6]` in in-row value.) Cosmetic; reconcile only if the spine wants a single canonical in-row number.
- **germ single-value bands:** rosemary and thyme use `germination_temp_f = [70,70]` (a point, not a
  range). Cosmetic; the spine's germination *window* may want a real min/max for these two.
- **microgreens carry `spacing_inches = []`** (dense broadcast sow — correct; there is no per-plant
  spacing). The spine should treat microgreens as area-density, not spacing.
- **germination windows are modeled bands around a source point** for the microgreens (e.g.
  `[65,75]`/`[68,74]` bracketing USU's single "74 °F"). Disclosed in each crop's `open_findings`. The
  spine's structured germination window can use these bands as-is.

## 4. Source-verification status (what was re-checked, and how)
- **Structural + regression:** deterministic, in-repo — all 114 pass `whole_crop_gate`, 0 dup slugs, all
  cited sources catalogued + T1, git/origin/plant-astro consistent. Highest confidence.
- **Growing-process numeric anchors (germ/spacing/DTM/stages):** the 27 crops whose per-wave source-truth
  review ran cleanly this session had these values confirmed against their cited T1 pages during
  certification; the audit re-verified them by logic/consistency + spot source-checks.
- **Degraded-review crops (Wave 7's four + sunflower-sprouts/pea-shoots/cilantro):** re-verified this
  session — microgreen anchors confirmed **live vs USU** (cilantro 21–28 days exact; sunflower/pea within
  their shoot-cut framing; germ bands bracket 74 °F); **sweet-pea toxicity re-confirmed with a fresh NCSU
  fetch** (its W7 review had used WebSearch only, because WebFetch was transiently blocked then —
  WebFetch works again now). No new content errors surfaced.

## 5. Standing caveats (relevant to any follow-up authoring)
- **Subagent dispatch was unreliable this session** (4 corrupted returns across Waves 5–7; WebFetch
  transiently blocked in Wave 7). Safety/health/anchor content lives in the compact single-line file's
  **tail**, exactly where the Read cap truncates a subagent — so **self-verify safety-critical / anchor
  content in the main loop** rather than trusting a half-blind agent.
- Canonical write-deny was bypassable via `dangerouslyDisableSandbox` in the earlier Wave-3 incident —
  harden before any unattended run.

---
**For follow-up sequencing of the broader post-114 work, see
`docs/kickoffs/10-post-114-backlog/KICKOFF.md`** (the `pet_safe` field, URL-liveness sweep, spelled-degrees
cleanup, `rhs` tier, design-case archetypes). This findings doc is specifically the anchor-truth reference
for the timing-spine authoring.
