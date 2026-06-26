# Incognito Red-Team Audit -- break the gates before betting 105 crops on them

**Run this in a FRESH, memory-OFF session.** Blindness is the method: fresh eyes find what primed
eyes (the people who built the gates) only confirm. Do NOT treat any doc in this repo -- including
`CURRENT_STATE.md`, the gate docstrings, or the remediation history -- as ground truth. They are
CLAIMS to test by running code, not facts.

## The claim to demolish

> "The plant-dataset gate armor catches every defect class that matters. The 18 certified crops are
> sound, and the system is GO to scale 18 -> ~105 via a bot pipeline (claude.ai authors, Claude Code
> releases)."

**Assume that is FALSE.** Your job is to find what ships clean that should not -- the holes that would
silently propagate across the 105 bot-authored crops. A self-congratulatory "yep, looks solid" is a
FAILED audit. The prior audit that trusted the gates missed real holes precisely because it trusted
them; the one that stress-tested them found B1 (a gate defined with zero callers) and B2 (a gate
scoped to one archetype that silently skipped another). There are more. Find them.

## Ground rules (non-negotiable)

1. **READ-ONLY on `crops_data_final.json`.** Every defect injection happens in a SCRATCH COPY. The
   gates take an explicit path arg (`whole_crop_gate.py <slug> <path>`); none hardcode the canonical.
   Confirm the canonical's `shasum -a 256` is unchanged at the start and end.
2. **A finding counts ONLY if it REPRODUCES.** "This might slip" is worth nothing. For each claimed
   hole: inject the defect into a scratch copy, run the LIVE gate (`whole_crop_gate` and/or
   `release_verify`), and show it reports `GATE: PASS` / clean. Paste the injection + the passing gate
   output. If it doesn't reproduce, it isn't a finding.
3. **Verify, don't trust.** Re-run the gates yourself. If a docstring says "this is checked," prove it
   by sneaking the defect past it. If a gate says "no-op off scope," find a crop in-scope where it
   still no-ops.
4. This is an AUDIT (find + reproduce holes), NOT remediation. Do not fix anything. Do not propose
   gate code. Just surface what breaks.

## Map the armor yourself (don't take my list)

The armor is in `tools/`: `whole_crop_gate.py` (the orchestrator that runs the A-numbered gates),
the `*_gate.py` / `annual_calendar.py` / `*_calendar.py` modules it imports, and
`tools/release_verify.py`. Read them. Build your OWN map of (a) every `*_violations()` function that
exists, (b) which are actually imported + called by the orchestrator, (c) each one's scope predicate
(the `if ... return []` no-op guard), and (d) what each claims to catch. The gaps between "exists,"
"wired," "fires in scope," and "actually catches the defect" are where the holes live.

## Method: fan out blind, then re-verify

Spawn parallel adversarial sub-agents (multi-agent). Give each one ONE surface and this instruction:
*"The gates claim to catch everything on your surface. Prove that false. Report only holes you
reproduced past the live gate, with the injection and the passing output."* Each sub-agent gets clean
context -- it should not see the others' work or assume the system is sound.

Then, as the orchestrator, **independently re-verify the highest-stakes findings yourself** by direct
inspection + your own injection -- do not trust a sub-agent's claim. (The prior incognito audit caught
its own sub-auditors' over-claims this way; one "finding" was a false positive that re-verification
retracted.)

## Attack surfaces -- a FLOOR, not a target

These are the obvious places. The valuable finding is the one NOT on this list. Cover these, then go
past them.

- **Scope / no-op correctness.** Every gate no-ops off its archetype. Find a crop that IS in scope
  where the gate silently returns `[]` -- or a defect that lands just outside every gate's scope
  predicate. (The B2 class: a chill check scoped `berries_woody`-only that skipped trees.)
- **Orchestrator wiring.** Cross-check every `*_violations` function in `tools/` against what
  `whole_crop_gate.py` actually imports and calls. Anything defined-but-unwired, or wired-but-only-
  reached on some crops? (The B1 class: a real gate with zero callers.) Also: does the gate run on
  SHELL/in-progress crops the way you'd expect, or only the 18?
- **The scale scenario (highest value).** You are the bot. Author a deliberately sloppy or adversarial
  NEW crop in a scratch copy -- a novel archetype, a never-seen field, a weird region/zone mix, a
  plausible-but-wrong calendar, fabricated-but-well-formed sources, copied-from-another-crop values --
  and run it through `whole_crop_gate` + `release_verify`. What ships clean that a human would reject?
  This is the actual thing the armor must survive 105 times.
- **Boundary / adjacent defects per gate.** For each gate, the sneaky variant near its edge: a
  required field that's present-but-whitespace; an enum value that's valid-but-wrong-for-this-cell; a
  month-rounding or day-precision edge; a calendar token that's in-enum but semantically incoherent; a
  companion with a valid label but a swapped/typo'd confidence; a heat_pause whose months align with
  the calendar but whose backing prose says nothing.
- **The un-gateable layer.** Dates and source fidelity are checked by a per-batch human/sample, not a
  gate. Can a wrong-but-plausible date, or a fabricated-but-plausible `anchoring_urls` entry, pass
  everything? How big is the gap the sample is the only defense for?
- **The checklist / methodology.** The gold-standard arc checklist + the release protocol
  (`CURRENT_STATE.md` protocol #6). Which steps could a bot skip or fake while still going green? Is
  "green gate" conflated anywhere with "correct"?

## What to hand back

A findings report, in the shape of `docs/incognito-audit-2026-06-25.md` (read that for the format):
- **Reproduced holes**, each with: the defect class, the injection, the live-gate output showing it
  shipped clean, the scale-risk (LOW/MED/HIGH at x105), and where it lives.
- **The armor that HELD** -- the defects you tried that the gates correctly caught (so we know what's
  actually solid, not just untested).
- **A GO / NO-GO verdict** on scaling to ~105, with the precise reason.
- Confirm canonical `shasum` unchanged start-to-end (READ-ONLY held).

Remediation -- if anything is found -- is a SEPARATE, memory-ON session (so it doesn't re-propose a
gate that was already tried and rejected). This session only finds and proves.
