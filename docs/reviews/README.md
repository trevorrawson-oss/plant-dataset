# Crop pipeline review reports

This folder is the **committed archive of the daily crop-pipeline review reports** -- the
human-readable record of what was authored, what was reviewed, and what was decided on each date.
These are the artifacts Trevor reads to make certification and biology-fidelity calls, preserved
here so anyone can later trace *why* a crop or a rule ended up the way it did.

## What's here

| File | What it is |
|---|---|
| `2026-06-29-crop-pipeline-review.html` / `.doc` | The 32-crop authoring review that carried the roster from 18 to 50, plus the cool-season timing-bug fix. 6 decisions. |
| `2026-07-01-crop-pipeline-review.html` / `.doc` | The overnight 30-crop batch review (12 fruit trees + 3 berries + 15 annuals), roster to 80 with content. 5 decisions. |
| `2026-07-01-batch-morning-report.md` | The technical companion to the 07-01 review: the normalizer change table, gate/regression/contamination verification, provenance. |
| `notes/2026-07-01/<crop>.md` | The per-crop **authoring NOTES** -- the fuller draft rationale each crop was built with: which sources were read, what was modeled vs. hard-sourced, what was unreadable, the honesty boundaries. |

The `.html` files are self-contained (inline CSS) -- open in any browser, or in Word / Google Docs
via the `.doc` twin. Each review leads with an **"At a glance"** summary and a **"Decisions for
you"** block, then the per-crop table and the notable flags.

## How the decision record is layered

The review reports are one layer of a larger, deliberately redundant decision trail:

1. **The rules** (the durable "we decided X because Y"): the *Live locked decisions / guardrails*
   block in [`../../CURRENT_STATE.md`](../../CURRENT_STATE.md).
2. **The history**: [`../../STATE_HISTORY.md`](../../STATE_HISTORY.md) (append-only).
3. **The design specs + audits**: the rest of [`../`](../) (archetype models, calendar-coherence
   bug + fix, the incognito red-team audits, the ruling lists, the QA protocols).
4. **The daily reviews**: this folder.
5. **The per-crop rationale**: the `verification_status.open_findings` baked into every crop in
   `crops_data_final.json` (332 findings across the roster), plus the `notes/` here.

The single entry point that ties all of these together is [`../DECISIONS.md`](../DECISIONS.md).

## Reading a report honestly

- **"Flags" are honest disclosures, not defects.** Every flag is non-blocking. A high flag count
  means more of a crop was *modeled* (regional windows, variety data) vs. pinned to a crop-specific
  source; it is a transparency signal, not a to-do list. The flags become the source-truth
  checklist when a crop is certified.
- **Drafts vs. certified.** A crop enters as an `author_fresh_pilot` DRAFT and is not live until a
  human biology-fidelity review + source-truth spot-check flips it to `verified_gs_arc`. The site
  build filters to certified crops.
