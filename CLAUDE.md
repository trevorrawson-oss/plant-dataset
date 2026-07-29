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
128 crops: 120 certified gold-standard anchors + 8 honest shells (the ~105-certified bot-pipeline
goal is met and passed; the 8 remaining shells are the 5 mushrooms + avocado/olive/artichoke). The armor is the gate suite — `tools/whole_crop_gate.py` (the A-numbered
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
- **`harvest` strings are month-granular TOUCH-SETS** ("Mar - May" = harvest occurs somewhere
  within those months), never day-precise spans -- but a month may be named only if the cell's
  sourced duration can actually reach it (explicit source dates govern over arithmetic). Ruled
  2026-07-27; rationale + renderer evidence in `docs/2026-07-27-harvest-window-semantics-ruling.md`.
- **RE-VERIFY THE DATA BEFORE ACTING ON ANY RECORD THAT DESCRIBES IT** -- an `open_finding`, a
  kickoff item, a `log_ref`, a state-history entry, a failing test you assume is stale. Confirm the
  defect still exists, and **run the gate that already covers the claim** before researching it.
  Ruled 2026-07-29 after this cost real work three times in one session: finding 21 sat `open`
  quoting a harvest window two revisions stale and commissioned a 16-document sourcing pass against
  a value that no longer existed, while `zone_order_gate` -- the exact check for its claim -- was
  returning 0 the whole time. A text gate for this was built, MEASURED (45 candidate hits, almost
  all findings legitimately quoting a SOURCE's dates) and **NOT built**: the check is procedural, not
  mechanizable. Corollary: **a failing test is evidence until you have read it.**
  `test_gen_current_state` was dismissed as stale rot while correctly reporting that
  `CURRENT_STATE.md` had lost its binding SESSION PROTOCOL header.
- **`verification_status.verification_log_ref` is an APPEND-ONLY, CERT-DATED HISTORICAL RECORD**,
  never a living summary. It records what was believed at the arc it names. **Do not "fix" a stale
  one into current tense** -- and never reason from one as current truth. When a pass retires a
  mechanism it asserts or revalues a distribution it counts, APPEND
  `[CORRECTION <date>: <what is no longer true> -- see <finding id>.]` and leave the original prose
  byte-for-byte. Roster growth alone needs no correction. Ruled 2026-07-29; the two-class rule, the
  measurement, and why this is deliberately NOT gated are in
  `docs/verification_log_ref_convention.md`.

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
