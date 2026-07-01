# yellow-summer-squash -- author notes (author_fresh_pilot)

**Authored:** 2026-06-30, by refitting the certified **zucchini-courgette** record.
**Output:** `yellow_summer_squash_crop.json` (this folder).
**Canonical:** READ-ONLY. Verified SHA `84321950...` == LATEST.txt before authoring.

## Why zucchini is the right template (and why the overlap is high on purpose)
Yellow summer squash and zucchini are the **same species, Cucurbita pepo**, both grown as
**summer squash**: harvested immature and continuously, bush habit, prolific, warm-season, same
pests, diseases, soil, pH, spacing, feeding, and per-region calendars. This is not the
carrot->radish case where the biology must diverge; here the shared culture is **genuinely
identical**, so it is mirrored verbatim and the refit is concentrated where the two truly differ.

## What is DISTINCT vs zucchini (the honest delta)
- **Color:** bright/buttery yellow skin with thin edible skin (refit in both descriptions,
  both harvest_ready fields, both variety notes).
- **Shape / two types covered:** **crookneck** (curved, often bumpy neck) + **straightneck**
  (smooth, tapered). Both forms are named and described throughout.
- **Pick-size:** **4 to 6 inches** (crookneck best 4 to 5 in before the neck warts; straightneck
  to 6 to 7 in), vs zucchini's 6 to 8 in. Refit everywhere it appeared (harvest_ready,
  growth_stages harvest, harvest notification).
- **Varieties (all 6 replaced):** Early Prolific Straightneck, Early Summer Crookneck, Sundance,
  Goldbar, Saffron, Zephyr (bicolor) -- with both register notes rewritten around
  crookneck/straightneck choice. Container-suitable list -> Saffron, Goldbar, Sundance, Early
  Prolific Straightneck; `container_notes.notes_seasoned` variety names refit to match.
- **days_to_maturity:** `[48, 58]`, mid `53` (crookneck/straightneck run a touch earlier than
  zucchini's `[50, 65]`; still coherent with the mirrored plant-to-harvest windows, ~54-56 days).
- The British term "marrow" (an oversized zucchini) was removed; oversized yellow squash is just
  called a big, seedy squash.

## What is MIRRORED verbatim (genuinely identical shared culture)
pH 6.0-6.5 (tol 5.8-7.5), spacing 24-36 in, germination 70-95 F, bush/monoecious/self-fertile
insect pollination, moderate feeder (balanced 10-10-10, one side-dress at flowering), pests
(squash vine borer, squash bug, cucumber beetle), diseases (powdery mildew, bacterial wilt),
rotation (Cucurbitaceae, 3 yr), watering (base-water, mildew-prone, ~1 in/wk), storage,
container culture, failure diagnostics, tips, notifications, weather triggers, and the full
**10-region calendars + heat_pause backing + successions**. The crop-name token in shared prose
was changed zucchini -> "summer squash" (reads naturally; it *is* a summer squash).

## The continuous-immature-pick model (same as zucchini)
- `harvest_urgency: "high"` -- pick young every 1-2 days or fruit turns huge/seedy/tough AND the
  plant slows new set. This drives the harvest_check notification + the harvest-stage tips.
- `succession_policy`: suitable=true, continuous, interval 3 wk, 12 successions (CC-derived
  `successions_realized` per cell, reconciled to max=12). Warm regions with a deep-summer heat
  gap (se_gulf, ca_desert, low_desert_az) run the spring/fall split with a backed `heat_pause`;
  temperate/coastal regions run one continuous window -- identical geometry to zucchini.

## Gate result -- whole_crop_gate: **PASS (exit 0), 0 violations**
Every A-gate returned 0, including:
- **A37 calendar-coherence: 0** (no growing-after-harvest, no one-month harvest hole).
- A30 basis, A31/A32 coverage floors, A33 numeric sanity, A34 cross-consistency, A5/A24/A28
  annual calendar + heat_pause backing, A25 register-completeness, A29 register-fill, A36
  CP-required dual-register, A23 raw-display, A19/A26/A27 companions, A20 display-readiness.
- Dual-voice: 126 populated CP, **0 null siblings**. Dash/temp: **0** user-facing hits. `°F` only.
- Source-tier: **16 IDs, 0 uncatalogued, 0 non-T1**. Anchoring: 45 claim leaves, **0 gaps**.
- Flip state: launch_ready_core/seasoned both **false**, status **author_fresh_pilot**,
  open_findings blockers **0**.

`release_verify` on the spliced scratch canonical: **clean, no blocking concerns** (its 2 review
notes are pre-existing cherry-tomato Step-5.5 `wait` pause-legibility items, not this crop).

**No A37 lines to report** -- A37 passed at 0; no hand-fix was needed and none was made.

## Sources (existing catalog T1 only)
16 T1 university-extension IDs, all already in `source_catalog` and reused from the certified
zucchini record: clemson_hgic, iastate_ext, nmsu_ext, osu_ext, sdsu_ext, tamu_agrilife,
uariz_ext, uc_ipm, ucanr_ext, ucd_postharvest, ufifas_ext, uga_ext, uhawaii_ctahr, umd_ext,
umn_ext, uwi_hort. The cited extension pages (UMN/UMD/OSU/Iowa State "growing summer squash and
zucchini", UGA B577, UF/IFAS VH021, UArizona AZ1005, UC ANR squash) cover crookneck/straightneck
summer squash, so the citations carry over honestly. **No new/uncatalogued IDs, no invented URLs.**

## Flags for the biology-fidelity daily review (all non-blocking, in open_findings)
1. **`yss_pilot_calendars_mirrored_from_zucchini`** -- per-region windows/calendars inherited
   verbatim from the certified same-species zucchini record. Honest for the scale phase (same
   species, same culture, T1-sourced windows); re-anchor against a yellow-squash-specific
   extension source at the display-readiness pass.
2. **`yss_pilot_variety_notes_modeled`** -- variety maturities/habits are standard catalog
   descriptions, not pinned to per-variety T1 pages. Refine at the variety-delta pass.

## Contamination scan (informational, not a gate) -- expected high overlap
`contamination_scan` reports ~**80%** bio-prose overlap with **zucchini-courgette** (142/197
fragments). This is the **intended** result of a same-species refit, not template bleed: the
overlap is with the correct sibling (zucchini), the rotation family is correct (Cucurbitaceae),
and no calendar/heat_pause is byte-identical to the unrelated lettuce-leaf reference. The
distinctness is deliberately concentrated in color / shape / pick-size / varieties / DTM.

## Inheritance carry-forward (from zucchini's own open_findings)
Zucchini's accepted findings apply equally here (mirrored data): hawaii_tropical z11 bounded-
continuous (not year_round; CTAHR B-91 unparseable PDF), and the osu/ucd/yield citation
re-anchor items. Resolve alongside zucchini's at the display-readiness pass.
