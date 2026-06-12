# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.7 + the v1.8 amendment** -- the tree branch) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---


**6 anchors CERTIFIED** (cherry-tomato, beefsteak-tomato, carrot, lettuce-leaf, peach, apple) of a ~18 roadmap target. **PEACH is now REGISTER-COMPLETE** (the 2nd register-complete crop after apple) -- its 42 certified-but-incomplete null register fields are backfilled and `register_fill_gate peach` returns 0. No flip (peach was already `verified_gs_arc`). NEXT = anchor 7 = lemon (needs the citrus/chill-gating MODEL decision first).

## Canonical pointer
- **Current SHA:** `d228ed7ba3e5dfea1a438335100e4268a71656bee19b954bd27d6a263298dbb3`. `LATEST.txt` session: `peach_register_fill_backfill` (2026-06-11).
- **Predecessor chain** (most-recent commits touching `crops_data_final.json`; content SHAs):
  - `a821d6d4` -- feat(apple): CERTIFIED -- anchor 6, the second tree (Steps 9-11)
  - `0711aa99` -- feat(apple): Steps 6-8B -- register prose complete (anchor 6)
  - `3c8ac5e9` -- feat(apple): Steps 6-8A -- bulk care prose + key-shape reconcile (anchor 6)
  - `09538e31` -- fix(trees): derive calendars from dates + A4 coherence gate; apple Step 5 + peach backfill
  - `5cfe354e` -- feat(apple): Step 4 -- tree region fill + anchoring reconcile (anchor 6)
  - `510edafe` -- feat(apple): Steps 1-3 + 3.5 -- anchor 6, the second tree (compressed)
  - `7345b944` -- feat(peach): CERTIFIED -- anchor 5, the FIRST tree (Steps 9-11: verbatim scan + perennial cert-gate + flip)

## What just happened (session `peach_register_fill_backfill`)
- **PEACH register-fill BACKFILL** (`a821d6d4`->`d228ed7b`): the 42 null register-prose fields peach was CERTIFIED without (the gap `register_fill_gate` surfaced -- the original narrow 6-8 worklist missed the care-prose containers + the 2.9-deferred set). **`register_fill_gate peach` 42 -> 0.** Authored fresh from peach's own biology (NOT lifted from apple): container_notes (16, dwarf-rootstock container case, honest vs `container_ok:false`), watering flat-prose (10), soil (5), start_method (4, `hardening_off`=N/A bare-root), companions (2, peach is SELF-FERTILE + replant-disease), ph (2), varieties (2, chill-hours-first), succession_policy.reason (1, N/A perennial).
- **Additive only -- NO certified value touched.** `verification_status` byte-identical; both `launch_ready` stay true; status stays `verified_gs_arc`; regions/calendars/biology/suitability all byte-identical. Only `peach` changed; only the 42 register fields (43 leaves); catalog unchanged (92). No flip needed.
- **PATCH PATH-FORMAT CORRECTION (Claude Code).** The delivered patch used slash-separated paths WITHOUT a leading slash (`companions/note_beginner`). `apply_patch.normalize_path` does not recognize that form -- it silently wrote the values to LITERAL flat keys (`peach["companions/note_beginner"]`), so the nested fields stayed null. **Caught by `register_fill_gate` still reporting 42** (defense-in-depth worked). Normalized every op path to leading-slash RFC-6901 (the established "Claude Code absorbs claude.ai path drift" precedent), re-applied; the resulting peach-crop sorted-min SHA matched claude.ai's claimed `e39d4b9b...` EXACTLY -- proof the corrected application is byte-for-byte what was intended.
- **Protocol #6 all-clean:** `register_fill_gate peach` 0; `whole_crop_gate peach` PASS(0); `register_completeness_gate` PASS; `release_verify` 10 CONCERN (all the known-intentional tree-vs-annual `chill_*` key-diff -- peach regions changed `[]`, no new violations, lettuce byte-identical); verbatim scan **0 HARD** (16 borderline 6-7-word, all benign-class numeric/seasonal conventions + Latin binomials); claim cross-check byte-confirmed (42 fields, only peach, no catalog change, no flip).

## Active work + next step
- **NEXT = anchor 7 = lemon** (3rd tree) -- needs the citrus/chill-gating MODEL decision FIRST (an evergreen sibling to `perennial_chill_gated`, or a `suitability.gating_factor`; flagged in checklist v2.0 §1). Not a pure compression repeat of peach/apple. Lock the model, then run the compressed tree arc.
- **Dataset-wide register-fill backlog (the gate's computed to-do):** the 4 certified annuals (cherry-tomato, beefsteak-tomato, carrot, lettuce-leaf) each carry ~10 null register fields -- almost all the 2.9-deferred null-scaffolded set (watering.method_note/critical_periods, fertilizer.amount, container self_watering/overwintering). A planned 2.9-completion sweep, lower priority than the anchors. (peach + apple are now register-complete; these annuals are the remainder.)
- **OWED (tooling):** `apply_patch` should REJECT (exit 1) an unrecognized bare-slash path rather than silently create a literal slash-key. Test-first hardening recommended (the only reason this release was safe is the downstream `register_fill_gate` caught it; the bot pipeline must not depend on that). New finding this session.
- **OWED (carried):** apple's 4 open_findings (dead-anchor repair, rotation shape, companions array-split, reliable_fruit_zone roster); `peach_rotation_shape_finding`; perennial-aware `rotation` shape; `_build_tree_shells` auto-populate region_id/label/zone_span; Appendix A reg of growth_stages `timing_*`/`year_phase`; repoint `gen_current_state` checklist ref -> v2.0.

## Gate record (generated 2026-06-11, on canonical `d228ed7b`)
- **cherry-tomato: `PASS` (0)**
- **beefsteak-tomato: `PASS` (0)**
- **carrot: `PASS` (0)**
- **peach: `PASS` (0)**
- **apple: `PASS` (0)**
- **lettuce-leaf: `PASS` (0)**
- **register_completeness_gate: `PASS`**

## Region fill state (generated)
- **cherry-tomato: 10/10 region cells filled**; 8 heat_pause, 8 second_planting
- **beefsteak-tomato: 10/10 region cells filled**; 8 heat_pause, 6 second_planting
- **carrot: 10/10 region cells filled**; 13 heat_pause
- **peach: 10/10 region cells filled**
- **apple: 10/10 region cells filled**
- **lettuce-leaf: 10/10 region cells filled**; 15 heat_pause

## Flip gates (generated)
- **cherry-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **beefsteak-tomato:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **carrot:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **peach:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **apple:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **lettuce-leaf:** launch_ready_core=True launch_ready_seasoned=True status=`verified_gs_arc`
- **6 anchors certified** (launch_ready true + status `verified_gs_arc`). (Target denominator is a roadmap call -- see the headline slot -- not derivable here.)

<!-- FILL: Live locked decisions / guardrails (editorial -- accretes; carry forward + amend) -->
- **register-fill is a cert dimension.** `register_fill_gate` (null register-prose at cert, with an N/A-prose-not-null rule + a frost_risk_note/legacy-zones allowlist) is live and flip-blocking; apple was the first register-complete cert, peach the first backfill-to-complete. whole_crop_gate's `null_values:0` does NOT catch null register prose -- run both.
- **Tree calendars are DERIVED, never hand-authored.** `tools/tree_calendar.py` generates `calendar[]` from bloom+harvest display windows; the A4 coherence gate (whole_crop_gate section A4) recomputes-and-compares, flip-blocking.
- **Patch path format = leading-slash RFC-6901 or dot-form.** Bare slash-separated paths (no leading `/`) are NOT supported and currently mis-apply silently -- normalize before apply until apply_patch is hardened to reject them.
