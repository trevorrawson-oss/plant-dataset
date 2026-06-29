# Final Blind Re-Audit -- break the REMEDIATED armor before the bots (the GO-gate)

**Run this in a FRESH, memory-OFF / incognito Claude Code session in `~/plant-dataset`.** Blindness is
the method: fresh eyes find what primed eyes (the people who just built the remediation) only confirm.
Do NOT treat any doc in this repo -- `CURRENT_STATE.md`, `STATE_HISTORY.md`, the gate docstrings, the
`docs/incognito-redteam-remediation-2026-06-27.md` writeup, or any "closed / GO" claim -- as ground
truth. They are CLAIMS to FALSIFY by running code, not facts.

## The claim to demolish

> "The plant-dataset gate armor, now HARDENED by the 2026-06-27 remediation -- roster A2-A36, including
> a calendar_basis enum guard, region/calendar coverage floors, perennial/photoperiod dispatch
> assertions, §3/register/raw-display/sanity hardenings, a tightened roster gate + backend-key
> laundering catch + a CP-required dual-register gate, and deterministic truth-layer gates -- now
> catches every defect class that matters. The 18 are sound and the system is GO to scale 18 -> ~105
> via a bot pipeline."

**Assume that is FALSE.** A prior blind audit (`docs/incognito-redteam-audit-2026-06-27.md`) found 16
holes and returned NO-GO; the remediation claims to have closed them and added six new gates. **The
remediation was done by the lane that knew the 16 holes -- it closed each KNOWN hole and tested it
against the specific injection it anticipated. The new gates (A30-A36, the tightened A25, the
truth-layer gates) have never been adversarially attacked as a whole.** Your job is the attack the
builders could not run on themselves: the new hole, in the new armor, that nobody injected. A
"looks solid now" is a FAILED audit.

## Ground rules (non-negotiable)

1. **READ-ONLY on `crops_data_final.json`.** Every defect injection happens in a SCRATCH COPY. The
   gates take an explicit path arg (`whole_crop_gate.py <slug> <path>`); none hardcode the canonical.
   Confirm `shasum -a 256 crops_data_final.json` is unchanged at start AND end (it should be
   `6dfd9798...`). Confirm the 18/18 baseline before you start.
2. **A finding counts ONLY if it REPRODUCES.** "This might slip" is worth nothing. For each claimed
   hole: inject into a scratch copy, run the LIVE gate (`whole_crop_gate` and/or `release_verify`),
   and show it reports `GATE: PASS` / clean. Paste the injection + the passing output. No repro, no
   finding.
3. **Verify, don't trust.** Re-run the gates yourself. If a docstring or commit says "this is checked,"
   prove it by sneaking the defect past it. If a gate says "no-op off scope," find an in-scope crop
   where it still no-ops.
4. This is an AUDIT (find + reproduce), NOT remediation. Do not fix anything or propose gate code.

## Map the armor yourself (don't take a list)

The armor is in `tools/`: `whole_crop_gate.py` (the orchestrator running the A-numbered gates A2-A36),
the `*_gate.py` / `annual_calendar.py` / `*_calendar.py` modules it imports, and `release_verify.py`.
Read them. Build your OWN map of (a) every `*_violations()` function that exists, (b) which are
imported + called by the orchestrator, (c) each one's scope predicate (the `if ... return []` no-op
guard), and (d) what each claims to catch. The gaps between "exists," "wired," "fires in scope," and
"actually catches the defect" are where the holes live. **Pay special attention to the gates added or
changed since the last audit** (anything not in `docs/incognito-redteam-audit-2026-06-27.md`'s gate
map) -- those are the unaudited surface.

## Method: fan out blind, then re-verify (triple-blind on the high-stakes surfaces)

Spawn parallel adversarial sub-agents (multi-agent). Give each ONE surface and this instruction:
*"The gates claim to catch everything on your surface. Prove that false. Report only holes you
reproduced past the live gate, with the injection and the passing output."* Each sub-agent gets clean
context -- it must NOT see the others' work, the remediation writeup, or assume the system is sound.

For the HIGHEST-STAKES surfaces (the dispatch guard, the coverage floors, and each of the six new
gates), dispatch **two or three INDEPENDENT sub-agents per surface** -- different angles, no shared
context -- and union their findings. That independent redundancy is the "triple-blind" rigor for the
GO bet.

Then, as the orchestrator, **independently re-verify the highest-stakes findings yourself** by direct
injection (a DIFFERENT crop/defect than the sub-agent used) -- do not trust a sub-agent's claim. The
prior audit caught its own sub-agents' over-claims this way; one "finding" was a false positive that
re-verification retracted.

## Attack surfaces -- a FLOOR, not a target (the valuable finding is the one NOT here)

**The new/changed armor (unaudited -- attack hardest):**
- **The dispatch guard** (the calendar_basis enum check that runs first). Is there a value that is
  in-enum but mis-dispatches? A basis that passes the guard yet no-ops a downstream gate it should
  trigger? A crop where the guard itself can be bypassed?
- **The coverage floors** (region-roster + calendar-presence). Can a crop satisfy the floor while
  being effectively empty -- a region present but hollow, a calendar present but degenerate? Can a
  non-indoor crop masquerade as indoor (or vice versa) to dodge the floor?
- **The numeric/sanity + cross-consistency layer.** The bounds are archetype-aware -- can you pick or
  spoof an archetype to widen them? A number in-bounds but wrong-for-the-species (the layer above the
  bounds)? A pH-prose parse you can evade (no decimals, a second range, a different field)? A
  harvest-requires-plant bypass (a harvest token with a plant-class token that is itself bogus)?
- **The roster / register / dual-register layer.** The roster gate was tightened to flag any unruled
  string -- is there a key now in the EXCLUDED roster that a bot can abuse to smuggle prose (or a
  forbidden `--`)? A backend-named key in a user-facing position the laundering catch misses? A
  should-be-dual-register field whose `_beginner` sibling can be omitted or faked past the CP-required
  gate (whose CP set is HARDCODED -- is the set complete, or is there a consumer field not in it)?
- **The GATE-UNLOCK / state mechanics.** Does the cp-required / register machinery have a state a bot
  can sit in that reads green but isn't? Does `release_verify` or the state trio conflate "green" with
  "correct" anywhere new?

**Regression (verify the prior 16 are actually closed):** take each hole in
`docs/incognito-redteam-audit-2026-06-27.md` (C1-C16) and re-run its injection against the CURRENT
armor. Confirm it now bounces -- and check the fix didn't open an adjacent side door.

**The scale scenario (highest value -- you are the bot):** author a deliberately sloppy/adversarial
NEW crop in a scratch copy -- a novel archetype, a never-seen field, a weird region/zone mix, a
plausible-but-wrong calendar, fabricated-but-well-formed sources, copied-from-another-crop values,
wrong-crop physiology -- and run it through `whole_crop_gate` + `release_verify`. What ships clean
that a human would reject? This is the actual thing the armor must survive 105 times.

**The un-gateable / truth layer.** A new biology-fidelity LLM-judge (`docs/kickoffs/02-...`) is
ADVISORY, not a gate. So the deterministic suite is still the hard bar: can a wrong-but-plausible
date, a fabricated-but-plausible source chain, or a biologically-impossible-but-well-shaped crop pass
every gate? How big is the gap the advisory judge + the human sample are the only defense for?

## What to hand back

A findings report in the shape of `docs/incognito-redteam-audit-2026-06-27.md` (read it for format):
- **Reproduced holes**, each with: the defect class, the injection, the live-gate output showing it
  shipped clean, the scale-risk (LOW/MED/HIGH at x105), and where it lives (`file:line`).
- **Regression result** on the prior 16 (each closed? any side door?).
- **The armor that HELD** -- the defects you tried that the gates correctly caught.
- **A GO / NO-GO verdict** on scaling to ~105, with the precise reason.
- Confirm canonical `shasum` unchanged start-to-end (READ-ONLY held).

Remediation -- if anything is found -- is a SEPARATE, memory-ON session. This session only finds and
proves.
