# Question: establishment-path encoding — in-calendar tokens vs plant_out

**From:** plant-app session, 2026-07-29. Not urgent; no app work is blocked.

Two certified perennials encode "how a new bed gets started" differently:

- **asparagus**: the 12-token `calendar` is pure phases (cold_pause / growing /
  harvest); the establishment path lives in `plant_out` windows on the
  plantings.
- **artichoke**: the perennializing cells bake the path INTO the calendar —
  `indoors` May–Jun and `plant` Jul sit alongside the mature-bed phases
  (ca_interior z9 and 37 other cells; the annual_only cold-roster cells are
  fine, the path is genuinely annual there).

Trevor caught the symptom on device (an established Full-harvest bed being told
to start seeds indoors). The app now gates presentation: on First/Full year
states, `indoors`/`plant` tokens render as `growing` when the crop has
`years_to_first_harvest` and the cell is not grown-as-annual; Establishing
keeps them and adds a too-late caption when the window has passed (plant-app
`974905b`, spec `docs/superpowers/specs/2026-07-29-establishment-path-segments-design.md`).

**The question:** is the artichoke encoding intentional (a token-level truth the
app should keep interpreting per bed age), or drift from the asparagus pattern
that A47/A-series hardening should normalize? The app is correct under either
answer — this only affects authoring consistency for the next perennials
through the pipeline (avocado, olive are queued). Per the standing rule
(2026-07-26 rulings), flagging rather than assuming.

Also noting: strawberry's 24 `plant`-token cells are all `grown_as: annual`, so
it has zero perennializing cells with a plant token — measured through the app
resolvers, not raw JSON.
