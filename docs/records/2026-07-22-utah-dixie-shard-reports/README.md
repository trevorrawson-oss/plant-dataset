# utah_dixie shard reports (2026-07-22), kept as records

**Committed 2026-10-03 by the housekeeping session** (kickoff 60, ruling 1). These 19 files were the only
copies of the subagent reports from the 2026-07-22 utah_dixie region authoring run, which sat untracked in
`tools/staging/shards/` and were never in git. Byte-identical to those originals.

- 15 shard reports (`c1`-`c5`, `citrus`, `p1`, `p2`, `t1`, `t2`, `w1`-`w5`) and 4 fix-pass reports
  (`cityfix`, `coolfix`, `finalfix`, `warmfix`).
- **Not kept:** the 15 shard `.json` cell files. Every cell exists in git, committed in the merged staging
  files: c1-c5 `tools/staging/utah_dixie_annuals_cool.json@fe2e79c`; citrus
  `utah_dixie_citrus.json@92c0e31`; p1, p2 `utah_dixie_perennials.json@4787cf7`; t1, t2
  `utah_dixie_trees.json@fd47140`; w1-w5 `utah_dixie_annuals_warm.json@3be3cb1`. Those merged files were
  revised afterwards (`3761103`, `a1c2d06`, `0ff05a2`, `f09782a`), so the shards were the earlier version.
- The fix passes landed as commits `0ff05a2`, `3761103`, `f09782a`, `a1c2d06`; their review inputs are in
  `docs/reviews/notes/2026-07-22/utah_dixie_*`. The region was promoted in batch `5908da6`.

These reports are subagent narration, not evidence: no hashed pages, no EVIDENCE or decision rows.
