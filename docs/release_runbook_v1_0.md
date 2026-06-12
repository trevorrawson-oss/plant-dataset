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

## 7. Archive the consumed handoff + clean the plant-project top level (STANDING RULE)

**Top-level hygiene invariant:** at any moment `~/Documents/plant-project/` shows ONLY the permanent numbered folders (`00-current` .. `11-photos`, `99-archive`) + the SINGLE active `HANDOFF_<current>/`. Every new handoff (Step 8) is preceded by archiving the prior transient folders, so the active handoff is always the only new folder there.

- **Consumed handoff** -> `06-sessions/handoffs-bundles/<arc>-releases/<step>/` (e.g. `peach-releases/register-fill-backfill/`). **Name the archive folder for the RELEASE SESSION, not the kickoff label** -- a kickoff may call itself "6-8c" while the release is `register_fill_backfill`; reusing "steps6-8c" would clobber a different archived step (this actually happened). Drop the kickoff bundle in `1_UPLOAD_TO_CHAT/` and the deliverables (patch + STATE_HISTORY snippet) in `FROM_CHAT/`.
- **Consumed PK manifests** (`PK_UPLOAD_*`, `PK_CLEANUP`) -> `99-archive/pk-uploads/`.
- Keep the bundle whole (it is small; the existing archive does). Pruning the reconstructable heavies (the full JSON snapshot, the copied state docs -- they rebuild from git by SHA) is OPTIONAL, only if archive size matters.

## 8. Build the next handoff
- FIRST run Step 7's top-level cleanup (archive the prior handoff + any consumed PK folders) so the new handoff is the only new folder.
- `~/Documents/plant-project/HANDOFF_<next>/1_UPLOAD_TO_CHAT/`: the orientation trio (LATEST, CURRENT_STATE, STATE_HISTORY) + the crop slice + sources/catalog + `00_KICKOFF_<step>.md` (Claude Code enumerates the work; claude.ai authors). (Earlier runbook said `~/Downloads/` -- actual practice is the plant-project folder, per the top-level-hygiene rule.)
- `2_ADD_TO_PROJECT_KNOWLEDGE/`: only when a rulebook doc actually changed.

## Lanes (never blur)
- **claude.ai AUTHORS:** biology, dates, consumer copy (dual-register, copywriting skill), source discovery/verification, the STATE_HISTORY entry snippet.
- **Claude Code RELEASES:** apply, all gates + verification, catalog admission (mint the ID), structural shapes (region shells, `second_planting`), SHA re-pins, `git`, the Step-11 flip, and authoring the entry if claude.ai omits it.
