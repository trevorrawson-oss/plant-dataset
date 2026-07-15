# plant-dataset — the canonical crop dataset + gate tooling

This repo is the **source of truth** for `crops_data_final.json` (the crop data behind
plant.lifestyle) and the Python tooling that keeps it correct. Do dataset/gate work **here**,
in `~/plant-dataset`. (plant-astro embeds a copy of this repo as a read-only submodule for its
build — never edit dataset content inside plant-astro; that copy is build plumbing, and editing
it leads to stale-checkout confusion.)

## Read these first, every session
- **CURRENT_STATE.md** — the live-state surface. Read before acting. Confirm the canonical is
  current: `shasum -a 256 crops_data_final.json` matches `LATEST.txt`, and check `git log -1` +
  `git status -sb`. Its header carries the binding SESSION PROTOCOL — follow it before any promote.
- **STATE_HISTORY.md** — the append-only recovery log (read to reconstruct true position).

## What this is
125 crops: 116 certified gold-standard anchors + 9 honest shells (the ~105-certified bot-pipeline
goal is met and passed; the 9 remaining shells are the 5 mushrooms + avocado/olive/artichoke/asparagus). The armor is the gate suite — `tools/whole_crop_gate.py` (the A-numbered
gates) + `tools/release_verify.py`. Gate detail + the live roster live in CURRENT_STATE.md.

## The two lanes (who does what)
- **claude.ai** AUTHORS content: biology, dual-register consumer prose, sourcing, evidence calls.
- **Claude Code (here)** PROMOTES + GATES: applies authored content, runs/writes gates, releases.
  Deterministic transforms + programmatic gates + git ceremony live here.

## Hard rules
- **Canonical JSON is COMPACT**: written with `separators=(",",":")`, `ensure_ascii=False`, no
  trailing newline, never `indent=2`. Never reformat it.
- **READ-ONLY on `crops_data_final.json` during gate/tooling work** — until there is an explicit
  authoring/promote task. Gate work surfaces data tensions to a corrections log, not one-off edits.
- **Tests-first (TDD): RED before GREEN.** Adversarially stress-test every new gate — inject the
  defect class into a SCRATCH COPY, confirm it bounces — before trusting it. A gate isn't done
  until a defect has been sneaked at it and caught.
- **Release verification before any promote** (protocol #6): `whole_crop_gate` 18/18 +
  `tools/gate_all.py` (the whole suite on **every** certified crop) + `release_verify` + the
  per-batch source-truth sample. A green gate is NOT a clean release.
- **State trio at every content release**: regenerate CURRENT_STATE.md via
  `tools/gen_current_state.py` (then fill its prose slots), append STATE_HISTORY.md (most-recent
  first), bump LATEST.txt (SHA + session).
- No em dashes in consumer copy (use commas/colons/semicolons/periods; `--` is fine in docs,
  commit messages, code comments, this file). American English. Temps render as `°F`. "plant" is
  lowercase except at sentence start or in "Plant Pro".

## Adding a cross-crop field
Before adding any field across crops, follow `docs/gs_cross_crop_field_addition_v0.md` (the column
GS-arc method) and check `docs/field_addition_register.md` (the live queue + trigger conditions).
Run column passes against a STABLE / complete roster, never mid-certification. Once a field's rollout
is complete it becomes a HARD cert requirement: `whole_crop_gate` A39 enforces presence-or-null and
A40-A42 enforce value shape for the register fields, run roster-wide by `tools/gate_all.py` -- a new
crop cannot certify without them (no backfill treadmill).

## Workflow / git
- Dataset commits go on `main` here. **Don't commit until Trevor approves** each change; when a
  discrete task is done, summarize what changed and what's next. Trevor confirms every push.
- A dataset content change reaches the live site only via a **plant-astro submodule bump** (a
  website concern, done in that repo, gated on Trevor) — not from a push here.
