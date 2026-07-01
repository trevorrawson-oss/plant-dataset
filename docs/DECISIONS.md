# DECISIONS -- why the plant dataset is the way it is

This is the **single entry point for tracing any decision** behind `crops_data_final.json` (the crop
data behind plant.lifestyle) and the tooling that keeps it correct. If you are asking "why did we
decide X," start here and follow the pointer.

The decision record is deliberately **layered and redundant** -- the same call is usually captured in
more than one place (a durable rule, a dated history entry, a design doc, and often a per-crop
finding). That redundancy is on purpose: it is how the project survives context loss between sessions.

## The five layers (where "why" lives)

| Layer | Location | What it holds |
|---|---|---|
| 1. **The rules** | [`CURRENT_STATE.md`](CURRENT_STATE.md) -> *Live locked decisions / guardrails* | Every standing decision with its rationale. The densest log. |
| 2. **The history** | [`STATE_HISTORY.md`](STATE_HISTORY.md) | Append-only, dated, most-recent-first. The recovery log. |
| 3. **Design specs + audits** | [`docs/`](docs/) | Archetype models, the calendar-coherence bug + fix, the incognito red-team audits, ruling lists, QA protocols. |
| 4. **Daily reviews** | [`docs/reviews/`](docs/reviews/) | The human-readable "what we reviewed and decided on this date" reports + per-crop authoring notes. |
| 5. **Per-crop rationale** | `verification_status.open_findings` in `crops_data_final.json` (332 findings) + [`docs/reviews/notes/`](docs/reviews/notes/) | The "why this number / why this window" for each individual crop, versioned with the crop. |

## Major decisions and where the rationale lives

| Decision | Rationale |
|---|---|
| **The dataset is built by a human-in-the-loop bot pipeline** (author off a certified template -> deterministic gates -> biology-fidelity + source-truth review -> human ruling -> certify) | `CURRENT_STATE.md` locked decisions; [`docs/kickoffs/05-author-bot/`](docs/kickoffs/05-author-bot/) |
| **Certified crops carry ZERO non-Tier-1 sources** (university extension only; seed companies / almanacs are corroboration-only) | `CURRENT_STATE.md` (source-tier); enforced by `whole_crop_gate` section E |
| **The gate suite (A2-A37) is the deterministic armor** -- it proves structure + coherence, never fabricates truth | [`tools/whole_crop_gate.py`](tools/whole_crop_gate.py); [`docs/incognito-redteam-*`](docs/) |
| **Calendar coherence: fix the SOURCE, not the symptoms** -- a missing calendar-LOGIC gate (A37) + a surgical normalizer, never a full re-derive | [`docs/calendar-coherence-bugs-2026-06-30.md`](docs/calendar-coherence-bugs-2026-06-30.md), [`docs/calendar-coherence-fix-design-2026-06-30.md`](docs/calendar-coherence-fix-design-2026-06-30.md) |
| **Gate on the biology, not the template** -- a crop carries a gating factor (e.g. photoperiod) only if its own biology gates that way | `CURRENT_STATE.md` locked decisions (2026-06-30) |
| **Citation-honesty is the draft->certified gap** -- the review catches claims pinned to a source that does not quite say them | `CURRENT_STATE.md`; [`docs/source_truth_sampling_qa_v1_0.md`](docs/source_truth_sampling_qa_v1_0.md) |
| **Family-wave certification + a family-bleed audit** -- catch the "carrot-on-turnip" template-bleed class before certifying | `CURRENT_STATE.md` locked decisions |
| **Heat-pause thermal backing is PER-CELL, never a shared region-heat table** -- heat tolerance is crop + region + zone physiology | `CURRENT_STATE.md`; `whole_crop_gate` A28 |
| **The perennial archetypes** -- trees = `perennial_chill_gated` (off peach/apple), berries = `berries_woody` (off blueberry, split bush/cane/shrub) | [`docs/2026-06-22-blueberry-berries-woody-model-design`](docs/); `CURRENT_STATE.md` |
| **Dual-register consumer prose (beginner / seasoned), no em dashes, degrees F, American English** | [`CLAUDE.md`](CLAUDE.md); `whole_crop_gate` register gates |
| **Adversarial red-teaming before scaling** -- reproduce the gate holes, remediate, re-verify | [`docs/incognito-redteam-audit-2026-06-27.md`](docs/incognito-redteam-audit-2026-06-27.md) + remediation logs |
| **Traditional gardening wisdom is welcome, hedged** -- honest "many growers find..." belief belongs in the copy, framed as tradition not fact | `CURRENT_STATE.md` locked decisions |

## How to trace one crop's decisions

1. Open the crop in `crops_data_final.json` and read `verification_status.open_findings` -- the
   honest disclosures (modeled vs. sourced, marginal regions, judgment calls) travel with the crop.
2. Read its authoring NOTES in [`docs/reviews/notes/`](docs/reviews/notes/) for the fuller draft
   rationale (sources read, what was unreadable, why a number was chosen).
3. Find the dated review in [`docs/reviews/`](docs/reviews/) that certified or last touched it.
4. Cross-check any rule it invokes against the *Live locked decisions* block in `CURRENT_STATE.md`.

## For a non-technical / public summary

See [`docs/methodology-and-sourcing.md`](docs/methodology-and-sourcing.md) -- a plain-language
explanation of where the data comes from and how it is verified, suitable for plant.lifestyle
users and stakeholders.
