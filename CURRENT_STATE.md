# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.5**) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---

## 🥬 LETTUCE (M15) + 🍅 CHERRY (M16) BOTH CERTIFIED -- cherry is the first FULL gold-standard arc. NEXT = M16 beefsteak
**2 of 9 anchors flipped.** `lettuce-leaf` flipped M15 (booleans-only, 2026-06-05). **`cherry-tomato` is now CERTIFIED (Step 11 flip, 2026-06-07) -- the FIRST crop taken through the entire v1.5 arc end-to-end** (Steps 3.5, 4, 5/5.5, 6/7/8, 9, 10, 11): 10/10 region cells verified, dual-voice gate = 0/PASS, `launch_ready_core`+`_seasoned`=true (earned, stale M10 artifact reset-then-set). **NEXT = M16 beefsteak** -- the second anchor, authored region-first against **cherry as the new reference exemplar**. **(Operating model: claude.ai authors, Claude Code releases -- 11 releases this arc, 10 clean + 1 merge.)**

## Canonical pointer
- **Current SHA:** `b6777ef6cb9a10ecf229bcda8c6e60b2f4af9ee2c4a5fc3541441b4c74fb89f9` (M16 cherry Step 11 -- launch_ready flip, cherry CERTIFIED). `LATEST.txt` session: `m16_cherry_step11_flip`.
- **NEXT: M16 beefsteak arc kickoff (claude.ai authors / Claude Code releases) -- preflight against `b6777ef6`.** OR resolve the parked decisions below first.
- **Predecessor chain:** `b6777ef6` (Step 11 flip) <- `84b086f1` (6/7/8 beginner siblings, gate->0) <- `12348fa0` (5e warm_arid) <- `45d5199f` (5.D) <- `9f61c52f` (5.C) <- `adf9dcb4` (5.B) <- `dadd18d1` (5.A) <- `eeaeae37` <- `7dd2837e` <- `7d4bf50c` <- `842ee139` <- `bf96d1d1` <- `9d8784f7` <- `813bade9` <- `349fb7af` <- `339933f2` <- `f916e8fe` <- `1b4fea68` <- `a65c7175` (Step 3.5) <- `29b3aaa9` (M15 lettuce flip) <- ... (full chain in STATE_HISTORY).

## What just happened (2026-06-07, session `m16_cherry_step11_flip`) -- CHERRY CERTIFIED
- **Step 11, the gated `launch_ready` flip -- the final step of cherry's arc.**
- **Validation pass (independent re-run):** gate PASS (0); release_verify clean; all 10 cells populated (certification mode); lettuce reference PASS.
- **Reset-then-set:** cherry's stale M10 `launch_ready=true` (set in `phase_3_m10_cleanup`, not earned) reset to false (entry guard `both==false` then held), gates re-confirmed, re-flipped `core->true` then `seasoned->true` (earned). Metadata stamped: `phase->phase_3_m16_gold_standard_arc`, `date`/`last_audited`->2026-06-07. **`status` left untouched** (`verified_retro_complete`) per F6.
- **Collateral:** only `cherry-tomato.verification_status` changed; lettuce + all other crops byte-identical.

## Active work + parked decisions
- **NEXT MILESTONE: M16 beefsteak** -- the second-anchor arc, authored region-first (NOT a regression; beefsteak re-derives all biology independently, incl. a likely WIDER heat pause than cherry). Cherry is the new reference exemplar for Step 3.5 shape parity.
- **PARKED -- Trevor decisions (none block the cert or beefsteak start):**
  1. **`status`-vocab three-state unification (Appendix B item 1) -- OWED NOW.** cherry=`verified_retro_complete`, the other anchor=`verified_complete`, lettuce=`unverified`. Decide ONE canonical post-arc value (Claude Code recommends **`verified_arc`**) and back-apply to cherry + lettuce. The flip deliberately left status untouched; this is the cleanup. Awaiting Trevor's word on the string.
  2. **`fruit_set_temp_f` schema shape** -- T1 anchors in hand (az2078 / UC IPM / CR457 / San Diego MG / VH021 / s1b_finding_006). Schema-touching -> Trevor rules shape; Claude Code adds field.
  3. **Optional ca_south_coast z9 soft-`cold_pause` revert** to `wait` -- non-blocking, Trevor's call.
- **PARKED -- Claude Code lane (do before beefsteak):**
  1. **Dual-voice-walker blind-spot FIX** -- make the gate auto-count `companions.{good,bad}_beginner_seasoned[*].why_beginner` (it counted 21, real total was 27). Cherry's 6 are filled, but beefsteak could pass with hidden nulls.
  2. `uc_mg` catalog-url nit (legacy `mg.ucanr.edu`); pre-commit/promote-wrapper release-verify hook at the pipeline transition.
- **PARKED -- claude.ai checklist amendments:** lifted_from_zone-strip into Step 3.5 text; °F-in-user-facing rule; retire "every cell needs a county MG"; window-structure-is-a-source-finding (Path A fallback); heat-set-failure-month = heat_pause token + second_planting action.

## Gate record (2026-06-07, post-Step-11, GATE-CONFIRMED on canonical)
- **`GATE: PASS` (0 VIOLATIONS).** cherry: launch_ready_core+seasoned=true, status=verified_retro_complete (pending vocab), phase=phase_3_m16_gold_standard_arc. All gates green in certification mode.

## Region fill state (cherry -- 10/10 authored, verified, CERTIFIED)
| region | zones | status | window | heat_pause | second_planting |
|---|---|---|---|---|---|
| `northern_tier` | 3-7 | VERIFIED (5.A) | cold (frost-bracketed) | none (frost-limited) | yes, z6-7 |
| `ca_interior` | 8-9 | VERIFIED (5.B) | single | none | none |
| `ca_north_coast` | 9-10 | VERIFIED (5.B) | single (May) | none (COOL-limited) | none |
| `ca_south_coast` | 9-10 | VERIFIED (5.B) | single (long Apr-Jul15) | none (mild marine) | none |
| `se_gulf` | 8-9 | VERIFIED (5.C) | two-window | month 7 (cherry-narrowed) | yes |
| `ca_desert` | 9-10 | VERIFIED (5.C) | two-window | Jun-Aug (absolute) | yes |
| `low_desert_az` | 9 | VERIFIED (5.C) | two-window | Jul-Aug (absolute) | yes |
| `fl_peninsula` | 10-11 | VERIFIED (5.D) | near-continuous | Jul-Aug (cherry-narrowed) | none |
| `hawaii_tropical` | 11 | VERIFIED (5.D) | year_round | none (oceanic-tropical) | none |
| `warm_arid` | 8 | VERIFIED (5e) | two-window (Mar + Jul) | month 7 (cherry-narrowed) | yes |

## Flip gates (the four distinct "flips")
1. **Per-crop `launch_ready` flip** -- ✅ lettuce (1), ✅ **cherry (2, first FULL arc)**. Beefsteak next, then 6 more anchors.
2. **Region read-layer flip** -- renderer reads `regions{}` first. Gate: shape proven on lettuce + cherry; beefsteak owes both. Ships with `zones{}` fallback. **2.9+.** (The plant-astro renderer rewrite -- read `regions{}`, consume `second_planting`, render `cold_pause`/`heat_pause` -- is gated here. **Now unblocked on the data side for 2 crops.**)
3. **Authoring-model flip** -- carrots onward region-first. Gate: 3 provers (need beefsteak).
4. **Schema perennial bump** (`lifecycle_override`) -- FUTURE, 2.9+. After carrots.

**Schema version lineage:** 2.7.5 -> **2.8 (current)** -> region read-layer flip + perennial = **2.9+.**

## Live locked decisions / guardrails (carry into beefsteak)
- **CHERRY HEAT PAUSE is PER-REGION.** Cherry narrows the pause only where heat is marginal (se_gulf z8, warm_arid z8 = single-month Jul); NOT where absolute (z9 deserts = Jun-Aug). **beefsteak re-derives independently -- likely WIDER (less heat-resistant than cherry).**
- **Heat-set-failure month that is ALSO a planting month = `heat_pause` calendar token + the plant carried by `second_planting{}`** (se_gulf + warm_arid, Trevor 2026-06-07). Pause > plant in token precedence; second-planting track surfaces the action.
- **WINTER COLD = `cold_pause` calendar token, NO sibling object.** Not on frost-free zones (z10 stays `wait`).
- **DUAL-VOICE: every in-scope `_seasoned` field needs a plain `_beginner` sibling.** Backend prose (synthesis_note, *_basis, source_quote) is seasoned-only by design. Companions `why_beginner` is in-scope but gate-invisible (walker fix owed).
- **WINDOW STRUCTURE is a SOURCE FINDING; NEVER carry a multi-window shape on analogy** (warm_arid's was wrong until the chart was read -- Path A is the fallback for visual-chart sources).
- **`harvest_to_table` T2-as-evidence: T1-only, NO grandfathering** (Trevor 2026-06-05). **TEMPERATURE user-facing = `°F` not "degrees F"** (backend prose may spell it).
- **CATALOG ADMISSION (county MG = UC ANR/NMSU = T1):** discovery+verified-URL = claude.ai; catalog write = Claude Code.
- **`second_planting` = discrete-window object (Claude Code lane), seasoned-only; succession = `succession_spring/fall` (lettuce); main = flat cell fields.** Each crop carries ONLY its structures. **Lettuce is NOT reshaped.** Spec in `docs/superpowers/specs/`.
- **Governing checklist v1.5; reference exemplar pointer = was lettuce, now repoint to CHERRY** (cleanest fully-arced exemplar). Dataset is authoritative; flag doc lag.
- **Lane split:** STRUCTURAL/MECHANICAL = Claude Code; biology + consumer copy + voice/IP + URL discovery + dates = claude.ai.
- **Keep `zones{}` coherent until Phase C** (renderer still reads it).
