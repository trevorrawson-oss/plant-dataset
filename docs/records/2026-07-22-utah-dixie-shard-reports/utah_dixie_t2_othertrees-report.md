# utah_dixie Task 6 -- Tier-2 "other trees" shard report

- **status:** DONE
- **shard:** `tools/staging/shards/utah_dixie_t2_othertrees.json`
- **slugs authored (5):** fig, mulberry, persimmon, pomegranate, pawpaw
- **zone:** single z8; `region_id=utah_dixie`, `region_label="Utah: St. George Dixie (Mojave-edge high desert)"`
- **frost anchor:** `resolved_from={"last_frost":"Mar 30","first_frost":"Nov 1","chill_hours":[250,450]}`
  on every cell (chill band cloned from `utah_dixie_chill_band.json` z8 [250,450]; the live tree
  pattern carries chill_hours in resolved_from, and region_cell_audit accepts it since
  last_frost+first_frost are non-null).
- **sources:** USU-only. Every cell cites `usu_ext_wash_fruits` (tree suitability / low-elevation
  fruit list authority) + `usu_ext_wash_frost` (frost anchor). NO Nevada/UNR ids carried over.

## Gate summary (all clean)
- `region_cell_audit utah_dixie <shard>`: **0 issues across 5 cells**
- `region_harness utah_dixie 8 <shard> <slug>`: **GATE: PASS** for all 5 (fig, mulberry,
  persimmon, pomegranate, pawpaw). A3 perennial cert-gate = 0 violations; A4 tree-calendar
  coherence engaged and clean (calendars derived from bloom+harvest via `derive_tree_calendar`).
- Manual sweeps: no em/en dashes, no build-word leaks (no shard/delta/Shape/Nevada/UNR/Mojave-
  High-Desert), no `degrees` literal (no degF numbers needed in tree prose).

## Per-tree verdicts
- **fig -- fruits_reliably.** On the USU low-elevation thrive list ("figs ... do well"). Modest
  desert chill (250-450 h) far exceeds fig's 100-300 h; heat is the asset. bloom Apr 5-Apr 25,
  harvest Jul-Sep (month tokens, matching the donor's fig style). Parthenocarpic home-variety note
  preserved.
- **mulberry -- fruits_reliably.** NOT on the USU Fruits list; authored from low-desert biology +
  the neighbor-region donor (see note below). bloom Mar 20-Apr 10, harvest May 20-Jul 5.
- **persimmon -- fruits_reliably.** On the USU low-elevation thrive list ("persimmons ... do well").
  Low-chill Asian cultivars (Izu/Fuyu/Hachiya). bloom Apr 20-May 10, harvest Sep 20-Oct 31
  (finishes just ahead of the Nov 1 frost).
- **pomegranate -- fruits_reliably.** NOT on the USU Fruits list; authored from low-desert biology +
  the neighbor-region donor (see note below). Prime desert crop. bloom Apr 10-May 10, harvest
  Aug 25-Oct 15.
- **pawpaw -- unsuitable.** Empty calendar (A3 unsuitable-must-be-empty satisfied). Honest verdict
  in suitability_note_*/chill_basis_*: a humid-forest understory tree, hostile in the hot, arid,
  alkaline Mojave-edge; on NEITHER USU column. Chill is close on paper (250-450 vs pawpaw's
  400-1,000 h) but aridity/heat/alkalinity, not chill, are the disqualifier.

## mulberry / pomegranate -- "not on USU list" note (required)
mulberry and pomegranate are NOT named on the USU Washington County Fruits page. They were
authored `fruits_reliably` from low-desert biology plus the Nevada/warm_arid donor cells (both were
`fruits_reliably` there). The consumer prose states this transparently ("USU Extension does not name
mulberry/pomegranate on its fruit list, but it is a classic low-desert fruit ... its judgment here
is drawn from that low-desert biology"). Cited source remains `usu_ext_wash_fruits` (the page frames
the low-elevation-vs-higher-elevation fruit split within which these are placed) + `usu_ext_wash_frost`.

## Judgment calls / concerns
- **Windows are a judgment call, not gate-constrained.** No gate checks tree bloom/harvest dates
  against frost beyond internal A4 coherence. I re-windowed by anchoring each tree's biological
  offsets (from the donor recipe) to St. George's Mar 30 last frost, then moderated the tails to
  sit before the Nov 1 first frost (fig/persimmon harvest end capped at Sep / Oct 31 rather than
  running to frost). Windows land ~2 weeks later than Nevada z8, consistent with St. George's later
  last frost. A content reviewer may want to sanity-check the persimmon Oct 31 harvest end against
  the Nov 1 frost (Asian persimmon fruit is frost-tolerant and often held past first light frost,
  so this is honest, but it is the tightest window in the set).
- **chill_hours in resolved_from:** the shard guide's generic single-zone template shows
  resolved_from with only last_frost/first_frost, but tree cells across the live canonical (incl.
  the Nevada donor) carry chill_hours, and the chill_basis prose leans on the [250,450] band, so I
  included it. Audit + harness both accept it.
- **St. George z8 is a low-chill / late-frost hybrid.** Its chill (250-450) reads like Nevada's
  warm Laughlin end, but its frost timing (Mar 30 / Nov 1) is the latest/shortest of any Nevada
  zone. Prose leans on the low-chill variety framing for all four fruiting trees accordingly.
