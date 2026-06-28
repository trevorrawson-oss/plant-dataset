# Kickoffs — claude.ai authoring-lane tasks spun out of the 2026-06-27 red-team remediation

Two self-contained kickoff prompts for two separate claude.ai chats. Each folder's `KICKOFF.md`
holds a paste-ready block plus the supporting material and any setup that chat needs.

- **[01-soil-texture-beginner-backfill](01-soil-texture-beginner-backfill/KICKOFF.md)** — author the
  21 `soil.*_texture_beginner` strings that clear the A36 `cp_required_gate` GATE-UNLOCK (whole_crop_gate
  is 11/18 until they land). Self-contained (embeds the 21 seasoned source strings + house-voice
  examples). Answers the "does the beginner need to be citeable?" question: **no** — sourcing is
  block-level and shared across registers; the beginner just must add no new fact. Output round-trips
  to the Claude Code lane to apply + gate + state-trio.

- **[02-biology-fidelity-llm-judge](02-biology-fidelity-llm-judge/KICKOFF.md)** — design + calibrate
  the biology-fidelity review (LLM-judge) that backstops the truth layer at scale (the 3 increment-2
  checks that bottom out at biology: calendar-vs-climate, rotation-family, wrong-crop heat_pause, plus
  C6/C7). Needs the 18 certified crop records attached for calibration.

Context: `docs/incognito-redteam-remediation-2026-06-27.md` + the STATE_HISTORY 2026-06-27 entries.
