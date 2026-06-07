# plant -- CURRENT STATE (live surface)

> ## ⚠️ SESSION PROTOCOL -- read before doing anything
> 1. **Confirm the SHA.** `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If it does not, STOP and reconcile. **The uploaded `LATEST.txt` / `CURRENT_STATE` / `STATE_HISTORY` are the SOLE authority for the canonical SHA, the fill count, and the next cell. If MEMORY conflicts, the files win (memory lags). Re-derive arc position from the files.**
> 2. **Locate your step on the arc checklist** (gold-standard arc checklist **v1.5**) BEFORE acting. Kickoffs SUMMARIZE; re-derive the next unowned step from the live crop + the checklist.
> 3. **This file is LIVE STATE ONLY.** Never delta-edit it. At session close, **fully regenerate it** from true state.
> 4. **History is append-only** in `STATE_HISTORY.md` -- APPEND a dated entry, never rewrite.
> 5. **CLOSE RITUAL.** If the dataset changed: PROMOTE (write canonical, re-pin `LATEST.txt`), regenerate this file, append to `STATE_HISTORY.md`, sync `00-current/`, commit (+ push).
> 6. **RELEASE VERIFICATION (Claude Code, BEFORE promoting any claude.ai change -- a green gate is NOT a clean release).** (a) `whole_crop_gate.py <slug>`; (b) `release_verify.py <candidate> --base crops_data_final.json --slug <slug>`; (c) **cross-check vs claude.ai's own STATE_HISTORY entry claims** (months/dates/keys/COUNTS). Then PROMOTE. The cross-check has caught real drift every session. **If claude.ai omits the history entry, Claude Code authors it from the patch.**

---

## 🥬 LETTUCE + 🍅 CHERRY BOTH CERTIFIED at `verified_gs_arc`. Post-cert tooling hardening in progress; NEXT = M16 beefsteak
**2 of 9 anchors certified.** `cherry-tomato` (Step 11 flip, 2026-06-07) is the FIRST crop through the entire v1.5 arc (Steps 3.5, 4, 5/5.5, 6/7/8, 9, 10, 11): 10/10 cells verified, dual-voice gate=0, launch_ready earned. `lettuce-leaf` (M15) is the other. **Both now carry `status="verified_gs_arc"`** (the unified post-arc vocab, decided 2026-06-07). **NEXT = M16 beefsteak** -- second anchor, authored region-first against cherry as the reference exemplar. First a short Claude-Code TOOLING-HARDENING batch (see below). **(Operating model: claude.ai authors, Claude Code releases -- 12 releases this arc, 11 clean + 1 merge.)**

## Canonical pointer
- **Current SHA:** `87c8e0a14fdce235a3b751d731c8c1c116115a39334902912ef4f2886c8fe77b` (status-vocab unify: cherry+lettuce -> `verified_gs_arc`, + 3 lettuce `why_beginner` gaps filled, walker-fix-revealed). `LATEST.txt` session: `m16_status_vocab_unify`.
- **NEXT: finish the tooling batch (#1 patch-format, #3 pre-commit hook), THEN M16 beefsteak -- preflight against `87c8e0a1`.**
- **TOOLING-HARDENING batch (post-cert, Claude Code lane, 2026-06-07):** **#2 dual-voice walker blind-spot FIX -- DONE** (`ac5f49f`; companions `why_beginner` now in-scope; immediately caught + we filled 3 hidden lettuce gaps). **#1 patch-format standardization -- IN PROGRESS** (one schema + `tools/apply_patch.py`). **#3 pre-commit release-verify hook -- IN PROGRESS** (3 commit types: cell release=full verify, catalog admit=source_catalog-only, doc/tool-only=skip).
- **Predecessor chain:** `87c8e0a1` (status vocab + lettuce gaps) <- `b6777ef6` (Step 11 flip, cherry CERTIFIED) <- `84b086f1` (6/7/8 beginner siblings, gate->0) <- `12348fa0` (5e warm_arid) <- `45d5199f` (5.D) <- `9f61c52f` (5.C) <- `adf9dcb4` (5.B) <- `dadd18d1` (5.A) <- `eeaeae37` <- ... <- `a65c7175` (Step 3.5) <- `29b3aaa9` (M15 lettuce flip) <- ... (full chain in STATE_HISTORY).

## What just happened (2026-06-07)
- **Step 11 flip (`b6777ef6`) -- cherry CERTIFIED.** Reset-then-set: cherry's stale M10 `launch_ready=true` reset to false (entry guard held), gates re-confirmed in certification mode, re-flipped `core`->`seasoned` (earned); phase->`phase_3_m16_gold_standard_arc`; status left untouched per F6.
- **Tooling batch + status vocab (`87c8e0a1`):** **#2 walker fix** (`ac5f49f`) made companions `why_beginner` in-scope and **immediately caught 3 hidden null gaps in LETTUCE** (Radishes/Carrots/Chives `good_beginner_seasoned`) -- the prior exemplar was not actually clean. Filled all 3 (Claude-Code-drafted, cherry register). **`status`-vocab decided = `verified_gs_arc`**, applied to cherry + lettuce (beefsteak stays stale `verified_complete`, not arc-verified). Both anchors now PASS under the corrected gate. Verified targeted (two-crop change, single-crop release_verify model N/A): only cherry+lettuce changed, only the named leaves.

## Active work + parked decisions
- **NEXT MILESTONE: M16 beefsteak** -- the second-anchor arc, authored region-first (NOT a regression; beefsteak re-derives all biology independently, incl. a likely WIDER heat pause than cherry). Cherry is the new reference exemplar for Step 3.5 shape parity.
- **PARKED -- Trevor decisions (none block beefsteak start):**
  1. **`status`-vocab unification -- ✅ RESOLVED 2026-06-07: `verified_gs_arc`.** Applied to cherry + lettuce. **`beefsteak-tomato` LEFT at stale `verified_complete` + `launch_ready=true` (M11-cleanup artifacts, NOT v1.5-arc-verified)** -- reset-then-re-earned at beefsteak's own Step 11, exactly as cherry's stale M10 flags were. Do NOT treat beefsteak as arc-done.
  2. **`fruit_set_temp_f` schema shape** -- T1 anchors in hand (az2078 / UC IPM / CR457 / San Diego MG / VH021 / s1b_finding_006). Schema-touching -> Trevor rules shape; Claude Code adds field.
  3. **Optional ca_south_coast z9 soft-`cold_pause` revert** to `wait` -- non-blocking, Trevor's call.
  4. **Lettuce `why_beginner` copy (Radishes/Carrots/Chives) is Claude-Code-drafted** (the 3 walker-fix-revealed gaps) -- Trevor to sanity-check; trivially editable.
- **PARKED -- Claude Code lane (do before beefsteak):**
  1. **#1 patch-format standardization** (one schema + `tools/apply_patch.py`) + **#3 pre-commit release-verify hook** -- IN PROGRESS this batch. (**#2 walker fix DONE** `ac5f49f`.)
  2. `uc_mg` catalog-url nit (legacy `mg.ucanr.edu`).
- **PARKED -- claude.ai checklist amendments:** lifted_from_zone-strip into Step 3.5 text; °F-in-user-facing rule; retire "every cell needs a county MG"; window-structure-is-a-source-finding (Path A fallback); heat-set-failure-month = heat_pause token + second_planting action.

## Gate record (2026-06-07, post-status-vocab, GATE-CONFIRMED on canonical, CORRECTED walker)
- **cherry `GATE: PASS` (0); lettuce `GATE: PASS` (0).** Both: launch_ready_core+seasoned=true, **status=`verified_gs_arc`**. Gate now runs the CORRECTED dual-voice walker (companions `why_beginner` in-scope, `ac5f49f`) -- it caught + we filled 3 hidden lettuce gaps this session, so both anchors are genuinely clean under the stricter gate.

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
