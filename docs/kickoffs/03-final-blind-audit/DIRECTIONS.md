# How to run the final blind re-audit so it's actually valid

The audit's whole value is **independence**. If it's run primed, it just confirms what the remediation
already believes. These directions exist to keep it blind. Follow them exactly.

## 1. Run it in a FRESH, memory-OFF / incognito Claude Code session

- Open a **new Claude Code conversation in `~/plant-dataset`** — NOT this remediation chat, and not a
  continuation of it. The auditor must have no carryover.
- **Turn memory OFF / use incognito.** This is critical: the remediation wrote project memories
  (`redteam-remediation-2026-06-27`, `a25-tightening-floods`) that would PRIME a fresh session into
  "the holes are closed." An incognito / memory-off session won't surface them. (The first audit was
  run exactly this way — "incognito.")
- It needs tool access (it runs the gates and injects into scratch copies) — a normal Claude Code
  session with Bash/Read, just clean-context. It does NOT need anything from `~/Downloads`; it reads
  the repo directly.

## 2. Paste ONLY the kickoff — do not coach

- Paste the contents of `KICKOFF.md` and nothing else. Do **not** add "by the way we fixed X" or
  "focus on Y" or "I think it's solid" — any of that un-blinds it.
- Don't answer leading questions about what was changed. If it asks "what did the remediation do,"
  the correct answer is "read the code and find out, and don't trust the claims" (which the kickoff
  already says).
- Let it run autonomously. It will map the armor, fan out blind sub-agents, inject defects into
  scratch copies, re-verify, and write a findings doc + a GO/NO-GO. It may take a while and spend
  tokens (multi-agent) — that's expected and is the point.

## 3. For true "triple-blind": run it 2–3 times, independently

- The kickoff already builds independence INTO one run (2–3 blind sub-agents per high-stakes surface).
  That alone is a strong audit.
- For the belt-and-suspenders GO bet, **run the whole kickoff 2–3 separate times, each in its own
  fresh incognito session**, and **union the findings**. Independent runs surface different holes;
  agreement across runs that the armor holds is far stronger evidence than one run. Disagreement (one
  run finds a hole others missed) is itself the signal — that hole is real.
- Don't show one run's output to the next run. Each starts blind.

## 4. What you get back, and what to do with it

- Each run writes a findings report (it'll suggest a path like
  `docs/incognito-redteam-audit-2-2026-06-XX.md`) with reproduced holes, the regression result on the
  prior 16, the armor that held, and a **GO / NO-GO verdict**.
- **If clean (GO):** that's the independent basis to flip NO-GO → GO and start the bot pipeline. Bring
  the verdict back to a remediation (memory-ON) session to update CURRENT_STATE and make the call.
- **If holes (NO-GO):** bring the findings to a **separate, memory-ON remediation session** (like the
  one that did this round) — not the audit session — to close them test-first. Then re-audit. The
  find/fix lanes stay separate on purpose (so a fix doesn't re-propose a rejected gate, and so the
  auditor never grades its own homework).

## 5. Sanity checks (so you know the run was honest)

- The report must confirm `shasum -a 256 crops_data_final.json` is **unchanged** start-to-end
  (`6dfd9798...`) — READ-ONLY held. If the canonical changed, the run was sloppy; discard it.
- Every reported hole must include a reproduced injection + the passing gate output. A finding without
  a repro is not a finding (the kickoff says so) — discount it.
- A run that returns "looks solid" with no attempted injections is a failed audit — it didn't actually
  try to break anything. Re-run it.

---

**TL;DR:** new incognito/memory-off Claude Code session in `~/plant-dataset`, paste `KICKOFF.md` only,
let it run, optionally repeat 2–3× independently and union, then take the GO/NO-GO to a memory-ON
session to act on. Keep audit and remediation in separate sessions.
