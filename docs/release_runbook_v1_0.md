# Dataset release runbook v1.0 (Claude Code lane)

**Status:** v1.0, 2026-06-07. The full repeatable sequence for releasing one
claude.ai handoff into canonical. Consolidates what was scattered across
`CURRENT_STATE.md` (protocol), the operating-model memory, and convention. Read
`CURRENT_STATE.md` + `STATE_HISTORY.md` + `LATEST.txt` first every session -- those
are the live authority; this is the *how*.

## 0. Session start
- `shasum -a 256 crops_data_final.json` must equal `LATEST.txt`. If not, STOP.
- Re-derive arc position from the files + the gold-standard arc checklist (v1.5), not from memory.

## 1. Receive the handoff (2 artifacts)
- A **patch** in the canonical format (`docs/handoff_patch_format_v1_0.md`) + a **STATE_HISTORY entry snippet**.
- If claude.ai omitted the entry, author it from the patch. If the patch drifted from the format, `apply_patch.py` tolerates the known aliases.

## 2. Preflight
- `shasum` canonical == the patch's `base_sha`. Mismatch -> STOP, re-preflight (the base moved under the author).

## 3. Apply
```
python3 tools/apply_patch.py <patch.json> --base crops_data_final.json --out crops_data_final.scratch.json
```
- Review the change-footprint it prints (crops / region cells / top-level / catalog). It should match the entry's claims.

## 4. Protocol #6 -- RELEASE VERIFICATION (a green gate is NOT a clean release)
- **(a) gate:** `python3 tools/whole_crop_gate.py <slug> crops_data_final.scratch.json` -- note the violation count (mid-arc nonzero is fine; what matters is no NEW ones).
- **(b) release_verify:** `python3 tools/release_verify.py crops_data_final.scratch.json --base crops_data_final.json --slug <slug> --ref lettuce-leaf` -- must exit 0.
- **(c) claim cross-check:** byte-diff the changed leaves vs the entry's path manifest + counts. Did the bytes match what it SAID? (This has caught a miscount or mislabel almost every session.)
- **Special cases** (release_verify's single-crop model does not fit):
  - *multi-crop change* (e.g. status-vocab) -> do a targeted hand collateral (only the named crops, only the named leaves); skip `--ref` if the ref crop itself changed.
  - *catalog admit* (only `source_catalog`) -> verify catalog grew/changed, no crop moved, no entry dropped.
- Biology truth (is a date TRUE per the source) is NOT this step -- that is the Step-5 4-round side-by-side.

## 5. Promote
- `NEWSHA = shasum scratch`; `mv scratch -> crops_data_final.json`.
- Re-pin `LATEST.txt`: `SHA` + `Date` + `Session`.
- **Fully REGENERATE `CURRENT_STATE.md`** (never delta-edit -- a corrected header on a stale body is worse than a uniformly stale file). For tiny doc-only follow-ups, careful targeted edits are acceptable if every stale fact is updated consistently.
- **Prepend** the STATE_HISTORY entry (fill its End-SHA; add a "Claude Code release" note with the protocol-#6 results). Append-only; most-recent-first below the header.
- Sync `CURRENT_STATE.md` + `STATE_HISTORY.md` + `LATEST.txt` -> `~/Documents/plant-project/00-current/`.

## 6. Commit + push
- `git add -A`; check `git status --short` (watch for stray scratch / one-off scripts -- move those out, don't commit them).
- Commit. The **pre-commit hook** (`tools/precommit_release_verify.py`) runs as a backstop; it blocks only on a regression. It is NOT a substitute for step 4.
- `git push` (dataset push is AUTONOMOUS -- announce-then-execute). **plant-astro merge-to-main + push stays gated on explicit Trevor approval.**
- Confirm `HEAD == @{u}`.

## 7. Archive the consumed handoff
- Move the patch + STATE_HISTORY snippet + kickoff into `~/Documents/plant-project/06-sessions/handoffs-bundles/<arc>-releases/<cell>/`.
- PRUNE reconstructable heavies (the full `crops_data_final.json` snapshot, full state-doc copies) -- they reconstruct from git by SHA. Keep only the unique small artifacts.

## 8. Build the next handoff
- `~/Downloads/HANDOFF_<next>/1_UPLOAD_TO_CHAT/`: the 4 current files (JSON, LATEST, CURRENT_STATE, STATE_HISTORY) + `PASTE_THIS.txt` (a tight kickoff) + any punch list (Claude Code enumerates the work; claude.ai authors).
- `2_PROJECT_KNOWLEDGE/`: only when a rulebook doc actually changed.

## Lanes (never blur)
- **claude.ai AUTHORS:** biology, dates, consumer copy (dual-register, copywriting skill), source discovery/verification, the STATE_HISTORY entry snippet.
- **Claude Code RELEASES:** apply, all gates + verification, catalog admission (mint the ID), structural shapes (region shells, `second_planting`), SHA re-pins, `git`, the Step-11 flip, and authoring the entry if claude.ai omits it.
