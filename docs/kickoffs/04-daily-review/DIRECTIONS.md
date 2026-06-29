# Daily biology-fidelity review -- the human-in-the-loop ritual

The operating model (Trevor 2026-06-28): this is NOT a 100%-blind bot build. Bots author ~5-10
crops/day; once they're applied to the canonical, a **daily claude.ai pass runs the biology-fidelity
judge over that day's crops + Trevor eyeballs them**, the findings get worked out, and we keep going.
The deterministic gates are the *silent-junk filter* (so the review isn't wasted on whitespace,
dispatch typos, hollow regions, a buried em-dash); the daily review is the *substance layer* (wrong-
species, wrong-for-the-species numbers, source plausibility -- what no gate can see).

## The daily ritual (one command, then one paste)

1. **Build the day's package** (from `~/plant-dataset`), either way:
   ```bash
   # you know what was authored today:
   python3 tools/daily_review_handoff.py rutabaga kohlrabi parsnip
   # or: everything whose crop record changed since yesterday's review point:
   python3 tools/daily_review_handoff.py --since <yesterday's-SHA-or-LATEST.txt-SHA>
   ```
   It writes `review_batch.json` (the day's crops + `source_catalog` + `region_chill_delivered`) and
   prints the ready-to-paste prompt. READ-ONLY -- it never touches `crops_data_final.json`.

2. **Run the review in claude.ai.** Attach `review_batch.json` +
   `docs/kickoffs/02-biology-fidelity-llm-judge/biology_fidelity_judge_v1_0.md`, paste the printed
   prompt. You get per-crop structured findings (by rubric dimension, with confidence + suggested
   fix) and a clean/needs-fixes verdict per crop.

3. **Work it + your own eyeball.** Triage the findings; the fixes come back to the Claude Code lane
   to apply + gate (like any authored change). A clean pass ships; a flagged crop gets corrected
   before it counts.

## Lowest-friction setup (recommended): a claude.ai Project

Make a claude.ai **Project** with persistent knowledge = `biology_fidelity_judge_v1_0.md` (the rubric)
+ a note that the carve-outs apply. Then the daily action is just: run the handoff command, drag in
`review_batch.json`, paste the prompt. The rubric never has to be re-uploaded.

## Setting it at a fixed time each day

- **Manual:** a daily calendar reminder + the one command above.
- **Prepped for you automatically:** I can set up a Claude Code scheduled routine (the `schedule`
  skill / a cron agent) that, at your chosen time, runs `daily_review_handoff.py --since <last
  review SHA>`, writes `review_batch.json`, and pings you with the paste prompt -- so the package is
  waiting when you sit down. Tell me the time and I'll wire it. (It only *prepares* the handoff; you
  still run the review and make the calls -- human-in-the-loop by design.)

## Why this is the load-bearing QA, not a backstop

At 5-10 crops/day the daily review is tractable and is the ONLY thing that catches biology/source
fidelity -- so it is treated as REQUIRED, not optional. The gates keep it focused; the judge makes it
structured; you make it correct. That is the GO bar: not "the gates catch everything," but "gates +
this daily review make a small-batch pipeline safe."
