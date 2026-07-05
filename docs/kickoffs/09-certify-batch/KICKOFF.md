# Certify-batch kickoff — flip the 34 staged drafts to verified_gs_arc (80 -> 114)

**Position (2026-07-05):** canonical `f7ab0ac2`, **80 certified**, **34 drafts staged** in
`_handoff/batch_2026-07-02/` (`author_fresh_pilot`, gate-clean, byte-spliceable). This is the certify
pass: source-truth review -> Trevor rulings -> promote, in **family waves of ~5**, exactly as 50 -> 80
went. No new authoring. When all 34 flip, roster = **~114 certified** (minus the retired collard-greens
shell).

This is the SAME loop that certified batch 1 (see the Wave entries in `STATE_HISTORY.md` for worked
examples). There is NO separate blind audit step — the per-crop source-truth review IS the audit.

## Read first (orient, do NOT start until confirmed)
- `CURRENT_STATE.md` — the SESSION PROTOCOL + Live locked decisions. Confirm the canonical is current:
  `shasum -a 256 crops_data_final.json` matches `LATEST.txt` (`f7ab0ac2…`), `git log -1`, `git status -sb`.
- `_handoff/batch_2026-07-02/MORNING_REPORT.md` — the batch detail + the per-crop watch-items (findings A-I).
- `CROP_REVIEW_2026-07-05.html` — the walk-through: the 5 ruled decisions + the per-crop honesty boundaries to sample.
- `docs/kickoffs/07-remaining-gs-anchors.md` — the "RULINGS 2026-07-05" section (below) + the certify sequence.
- `docs/release_runbook_v1_0.md` — the promote ceremony.

## Trevor's rulings (ALREADY DECIDED — do not relitigate)
1. **Cucumbers:** keep `cucumber` as the generic parent alongside slicing/pickling/english. Certify all four.
2. **Herbaceous-perennial lane RATIFIED:** mint, chives, lemongrass, bee-balm, echinacea certify as-is in
   their current lanes (`perennial=true`, `succession_policy.suitable=false`). No re-authoring.
3. **`collard-greens` RETIRE + `collards` alias** (the FIRST canonical touch — fold into Wave 1's promote):
   drop the empty `collard-greens` shell from `data["crops"]`, AND set certified `collards`
   `name = "Collards (Collard Greens)"` (the `lettuce-leaf` = "Lettuce (Leaf)" pattern). NOTE: dropping the
   shell takes the catalog 125 -> 124, which the pre-commit release-verify flags as a catalog DROP — this
   one is intentional; handle it deliberately (confirm the only dropped slug is `collard-greens`).
4. **Deferred (NOT in this batch):** artichoke, asparagus, avocado, olive, sweet-corn, the 5 mushrooms —
   they need archetype design first (roadmap Tier 2). Leave them as shells.
5. **Roster-wide spelled-degrees `-> °F` cleanup + gate C/D hardening:** do this AFTER reaching 114, not
   during (heirloom-tomato already normalized; certified beefsteak-tomato + green-beans-bush still owe it).
- **heirloom-tomato** stays a PARENT (heirloom spans many types -> variety picker later); on the variety-pass
  flag list with the cucumbers. Certify it now.

## The per-wave loop (repeat until all 34 are flipped)

1. **Source-truth review — 5 parallel agents (the audit).** Dispatch one `general-purpose` Agent per crop
   in the wave, concurrently. Each: READ-ONLY, uses ONLY WebFetch/WebSearch (never curl/wget/pdftotext —
   denied), opens the crop's cited T1 URLs, and confirms the load-bearing numbers are ACTUALLY on the page
   (citation honesty — the recurring catch). Return structured per-claim findings. Point each at that crop's
   watch-items from the MORNING_REPORT / walk-through. The honesty boundaries to sample:
   habanero Scoville, fava favism (G6PD), grapefruit drug-interaction (flagged not asserted), sweet-potato
   correctly no greening/solanine, the citrus cold/heat gradient, sweet-pea toxic seeds (lathyrism),
   wheatgrass no-health-claims, and the `rhs` (UK) source tier used by sage + fava.
2. **Synthesize -> present to Trevor** with a per-crop verdict table + recommended rulings. Trevor rules.
3. **Apply fixes** to the staging records (`_handoff/batch_2026-07-02/crops/<slug>.json` + splice into the
   batch `BATCH_normalized.json`), then **flip** `verification_status`: `status="verified_gs_arc"`,
   `launch_ready_core=true`, `launch_ready_seasoned=true`, `last_audited=<date>`, `phase`, `source_set`
   (recompute from anchoring_urls), `verification_log_ref`, and every `open_finding` `blocks_launch=false`.
4. **Verify (gate by EXIT CODE, never grep):**
   - `python3 tools/whole_crop_gate.py <slug> <candidate>` -> exit 0 for each.
   - `python3 tools/derive_realized_successions.py --check <slug>` -> up to date.
   - `python3 tools/release_verify.py <candidate> --base crops_data_final.json --slug <slug> --ref lettuce-leaf`
     — **use `--ref orange-navel` for the citrus** (grapefruit/mandarin-clementine/lime) to clear the benign
     tree-vs-annual-reference artifact. A multi-crop promote always flags one benign collateral CONCERN;
     confirm it is ONLY that (no new violations, reference byte-identical, catalog unchanged except the
     intentional collard-greens drop in Wave 1).
5. **Surgical promote:** splice the finalized records into a PRISTINE canonical snapshot; assert EXACTLY
   the wave's slugs changed (no collateral), all gate PASS, 0 PASS->FAIL regressions, release_verify clean.
   Then `cp` scratch -> `crops_data_final.json` (canonical COMPACT:
   `json.dumps(separators=(",",":"), ensure_ascii=False)`, no trailing newline — never reformat).
6. **State trio:** bump `LATEST.txt` (new SHA + session line); append `STATE_HISTORY.md` (most-recent-first,
   below the header, `---`-separated); regenerate `CURRENT_STATE.md` via `python3 tools/gen_current_state.py`
   then fill its 4 `<!-- FILL -->` prose slots (carry the Live-locked-decisions block forward + prepend this
   wave's entry).
7. **Commit + push + bump** (Trevor confirms the push each time):
   - Commit canonical + state trio (the pre-commit hook re-runs release_verify; it blocks only on a real
     regression or an UNexpected catalog drop).
   - `git push origin main` (on Trevor's go-ahead).
   - **plant-astro submodule bump** (pointer-only): `git -C plant-astro/plant-dataset fetch + checkout <new HEAD>`,
     verify the submodule's `crops_data_final.json` SHA == the new canonical, then `git -C plant-astro add
     plant-dataset` — GUARD: staged must be EXACTLY `plant-dataset` (Trevor keeps parallel artwork changes
     uncommitted in that tree; never stage them). Commit pointer-only, push.

## Hard rules
- **READ-ONLY on `crops_data_final.json`** until the promote step; all interim work on a scratch copy.
- Canonical stays COMPACT; never `indent=2`, never a trailing newline.
- Gate by EXIT CODE, never by grepping output.
- Do NOT commit or push until Trevor approves; he confirms every push and every plant-astro bump.
- Any new gate is TDD (RED before GREEN) — but this batch should need none.

## Suggested wave grouping (adjust freely; group by archetype so each wave shares a review shape)
- **W1** slicing-cucumber, pickling-cucumber, english-cucumber, banana-pepper, habanero  *(+ do the collard-greens retire + collards alias in this promote)*
- **W2** heirloom-tomato, pole-beans, sweet-potato, sugar-snap-peas, broad-beans-fava
- **W3** grapefruit, mandarin-clementine, lime *(citrus: `--ref orange-navel`)*, rosemary, sage
- **W4** thyme, oregano, mint, chives, lemongrass
- **W5** arugula-microgreens, broccoli-microgreens, cilantro-microgreens, radish-microgreens, pea-shoots
- **W6** sunflower-sprouts, wheatgrass, cosmos, borage, chamomile
- **W7** sweet-alyssum, sweet-pea, bee-balm, echinacea

At 114: state trio final, then hand back to Trevor for the post-114 work (new datapoints/fields on the 114,
then the deferred archetypes — see `docs/kickoffs/07-remaining-gs-anchors.md`).
