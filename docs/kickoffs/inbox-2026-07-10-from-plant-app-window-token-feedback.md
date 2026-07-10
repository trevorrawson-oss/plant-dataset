# From plant-app: window-vs-token feedback after the #19 sync (2026-07-10)

**From:** the plant-app (iOS) session, after absorbing kickoff #19 (canonical `50288c02`, app
foundation `664f56c`, OTA'd). Left untracked by the app session — commit/renumber as you like.

The app now enforces a **token-override contract** (mirrors the website): calendar tokens are the
one curated state per month; the app's start-indoors windows only FILL blank months, with a single
documented exception (below). While building that contract we swept every crop x region x zone and
found two dataset-side items. Neither blocks anything app-side; both would tighten app/website
truthfulness at source.

## A. 7 fall plant_out windows contain NO `plant` token (se_gulf tomatoes)

The fall `second_planting.plant_out` window and the `calendar[]` disagree — the window's months
carry only `heat_pause`, so no renderer can show a fall set-out month for these cells, and the
app's fall-term planner anchors off token runs that don't exist there:

| cell | sp.plant_out | tokens across window |
|---|---|---|
| cherry-tomato/se_gulf/z8 | Jul 6 - Jul 20 | heat_pause |
| beefsteak-tomato/se_gulf/z8 | Jul 1 - Jul 20 | heat_pause |
| beefsteak-tomato/se_gulf/z9 | Jul 25 - Aug 8 | heat_pause, heat_pause |
| roma-tomato/se_gulf/z8 | Jul 6 - Jul 20 | heat_pause |
| heirloom-tomato/se_gulf/z8 | Jul 1 - Jul 20 | heat_pause |
| heirloom-tomato/se_gulf/z9 | Jul 25 - Aug 8 | heat_pause, heat_pause |
| grape-tomato/se_gulf/z8 | Jul 6 - Jul 20 | heat_pause |

Either the window or the tokens is wrong (mid-July set-out in the gulf heat is plausibly the
authored intent — hot-set varieties — in which case the token should say `plant`; or the window
should move to match the tokens). Note: the app's updated `scripts/audit-planting-windows.mjs`
(Signal A) now flags these on every run, so you can re-verify after any fix with that script from
the app repo.

## B. Start-indoors windows with zero `indoors` tokens — flip candidates (heat AND cold side)

Kickoff #17 flipped `heat_pause` -> `indoors` on core months of indoor-start windows for 22 cells.
The sweep found the same pattern un-flipped elsewhere, plus the cold-side mirror (which #17 noted
as future work). These are all cells where a real `start_indoors` window exists but the row has NO
`indoors` token anywhere, so token-faithful renderers show no seed-start month at all:

**Heat-side (same rule as #17, cells it didn't cover):** fall si windows on ca_desert tomatoes
(cherry/beefsteak/roma/heirloom/grape z9+z10, Jul-Aug), broccoli+kohlrabi se_gulf z8/z9 +
warm_arid z8 + northern_tier z6/z7 (fall, Jul/Aug), and primary si on fl_peninsula
cherry/roma/grape-tomato z10/z11 + jalapeno z10/z11 (Aug).

**Cold-side (the #17 mirror, not yet done):** primary si windows sitting on `cold_pause` months —
broccoli + kohlrabi northern_tier z3-z7 (Jan-Mar depending on zone), and the cucurbit block
(slicing/pickling/english-cucumber, zucchini, yellow-summer-squash) ca_interior z9 +
ca_south_coast z10 (Feb).

Until these flip at source, the app renders them `indoors` via a narrow, documented exception
("a start window may claim its pause months when the row would otherwise show no indoors month
at all — action over passive"), which is the only remaining app/website divergence. Once the
flips land, the app's exception naturally stops firing and parity becomes exact, with no app
change needed.

(Two cells the app deliberately leaves alone: jalapeno/ca_desert/z10 and tomatillo
ca_desert-z10/fl_peninsula-z11, whose tiny Jan si windows sit entirely on `plant` months — the
plant token rightly wins; the guide-screen callout carries the si dates.)

## Suggested ritual if you take these

Whichever direction each fix goes, the app side re-verifies with: `npm run build:guides` +
`npx jest guides-shape guide-calendar.contract` (the new contract sweep names any cell where a
token and the app's render disagree) + the kickoff #19 spot-checks.
