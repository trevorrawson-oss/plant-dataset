# Kickoff #19 -- plant-app sync: second_planting de-mux + heat-gap indoors + microgreens rebuild

**For:** the plant-app (iOS) session. Paste-ready summary below; this doc is the durable copy.
**Canonical now:** `50288c02ac376d8bf9539e8d4ace21f8e197795e22cb2c0c334f6c5b58562398` (plant-dataset
origin/main, 2026-07-09). Whatever the app's current pin, three content releases land in this sync:
`9d1193eb` (microgreens growth_stages), `1372c299` (heat-gap indoors flip), `50288c02` (second_planting
de-mux, via 5 intermediate SHAs).

## 1. SECOND_PLANTING DE-MUX (2026-07-09, the big one -- SHAPE CHANGE)

**What changed:** every discrete two-season cell (158 cells: 5 tomatoes, broccoli, kohlrabi + 18
newly-migrated crops incl. peppers, cucurbits, pole-beans, potato, swiss-chard, broad-beans-fava)
now carries the fall cycle in a structured object, and the top-level window strings are the
PRIMARY cycle ONLY:

```
resolved_by_zone[z] = {
  start_indoors, plant_out, harvest,            // PRIMARY window only, single span
  first_plant_date, last_plant_date,            // narrowed to the primary cycle
  harvest_start, harvest_end,                   // narrowed to the primary cycle
  second_planting: {                            // present ONLY on two-season cells
    start_indoors,                              // string or null (direct-sown)
    plant_out, harvest_start, harvest_end,
    sources: [...], anchoring_urls: {...}
  },
  calendar: [12 tokens]                         // UNCHANGED (both cycles, as always)
}
```

**BREAKING for any consumer that comma-splits window strings** (memory
`dataset-shape-change-breaks-frontends` applies): the second comma-span is GONE from
start_indoors/plant_out/harvest. Grep the app for `split(',')` / multi-window parsing on those
fields and repoint every fall-cycle feature to `second_planting{}`.

**New string forms the app's date parser must handle (all live in canonical now):**
- `" or "`-joined ALTERNATIVES of one planting choice (never two crops): onion/shallot
  `"Oct - Nov or Jan - March"`, `"Sep or Dec"`; woody herbs `"Oct - Nov or Feb - Mar"`.
- Full month names: `"Nov - March"`. Bare single months: `"Feb"`, `"Sep"`, `"Aug"`.
- Harvest-only comma doubling STILL EXISTS and is legitimate (ONE planting, split harvest):
  hot-region cayenne/habanero/jalapeno (`harvest "May 15 - Jun 30, Oct 1 - Dec 5"`), chives, mint.
  Only PLANTING fields are guaranteed single-choice.
- broad-beans-fava: second_planting whose harvest window EQUALS the primary's (fall sowing
  overwinters into the same spring window) -- render once, not twice.
- Month-granular envelope values (`last_plant_date "Feb"`, `harvest_end "Jun"`) now more common.
- **AUDIT YOUR DATE PARSERS for the bare-month gap:** plant-astro had THREE separate parsers
  that required "Mon D" and silently returned nothing for bare months ("Nov", "Jul - Oct") --
  the last one left celery's harvest row blank site-wide and muted 566 cells' harvest rendering
  until 2026-07-09 (astro a27c14b). If the app parses window/envelope strings anywhere, prove it
  handles: bare months, full month names ("Nov - March"), " or " joins, day precision, commas.

**Product rulings to mirror from the plant-astro flip (Trevor, 2026-07-09):**
1. Fall/second track renders ONLY from `second_planting` (present -> render; absent -> none).
2. broccoli + kohlrabi are `succession_policy.suitable=true` AND carry second_planting on 28
   cells: second_planting presence beats the suitable flag PER CELL for visualization; other
   suitable=true crops keep rhythm/cadence rendering.
3. Derived month states union BOTH cycles: a month inside either cycle's windows shows its real
   state (indoors/plant/harvest); "too early/too late" only outside both. (Trevor: broccoli z9
   Aug/Sep must say plant, fall harvest must show, in every mode.)
4. Region beats zone: never union windows across regions sharing a zone number. A region cell
   that EXISTS but has no plant window (perennial `survives_no_fruit`) must SUPPRESS
   plant-now/soon prompts, not fall back to other regions' windows. survives_no_fruit crops stay
   VISIBLE in lists (unbadged); only genuinely won't-grow combos hide from plantable filtering.
5. Notifications: "time to start your fall batch" should key off `second_planting.start_indoors`
   / `.plant_out` (this structure exists exactly so the app can fire these deterministically).

**Gate:** whole_crop_gate A43 now enforces this shape roster-wide (both rules). Every future crop
arrives in this shape; no legacy comma shape will ever reappear.

## 2. HEAT-GAP INDOORS FLIP (2026-07-08, `1372c299`, kickoff #17 -- calendar TOKEN semantics)

On 22 cells (26 month-flips), a summer month that is inside `heat_pause.months` AND is a core
month of a real indoor-start window (`start_indoors` OR `second_planting.start_indoors`) now
carries the calendar token **`indoors` instead of `heat_pause`** (action-over-passive: "start
your fall seedlings now"). Cells: broccoli+kohlrabi ca_interior (Jul) + ca_south_coast (Aug);
beefsteak+heirloom-tomato fl_peninsula (Aug+Sep); celery across 6 hot regions.

**App consequences:**
- `calendar[]` tokens no longer equal `heat_pause.months` everywhere. `heat_pause.months`
  remains the CLIMATE fact; the token is the display/action state. An `indoors` token on a month
  listed in `heat_pause.months` means "hot AND start seedlings indoors" -- do not render it as a
  contradiction and do not derive pause UI purely from tokens.
- The explanatory note is APP-DERIVED (kickoff #17 spec): compose at build/run time from
  `heat_effect` ("form heads"/"set fruit"/"grow well") + `heat_threshold_f` (broccoli 86,
  kohlrabi/celery 75, tomatoes 92) + fall framing. A per-cell override slot is reserved, not
  populated.

## 3. MICROGREENS growth_stages REBUILD (2026-07-08, `9d1193eb`, kickoff #16 -- still owed)

The 8 microgreens-family crops moved from the old per-stage shape (`stage_id`,
`name_seasoned/beginner`, `description_*`) to the STANDARD shape every other crop uses (`id`,
`name`, `day_range_from_sow`, `audience`, `user_action_*`, `what_to_look_for_*`, `log_prompt_*`).
plant-app patched around the old shape on 2026-07-07 (`a3a0145`); with the data now fixed at
source, per kickoff #16: rebuild guides, re-check the promotion-checklist count assertions, and
consider removing the patch. Stage ids + `day_range_from_sow` were byte-preserved.

## 4. The sync ritual

1. Bump the app's dataset pin/copy to `50288c02` and verify
   `shasum -a 256 crops_data_final.json` matches.
2. Grep for old multi-window assumptions (`split(',')` on window fields, chunk counts,
   DTM-midpoint fall-harvest synthesis) BEFORE building.
3. `npm run build:guides` + the promotion-checklist count assertions + `npx jest` (the kickoff
   #16 ritual) -- a full build is the real end-to-end check; unit tests alone missed the last
   shape break.
4. Known-good spot-checks: broccoli ca_interior z9 (primary = Dec-Feb plant / Mar-May harvest;
   `second_planting` = Jun 20-Aug 18 indoors / Aug-Sep plant / Oct 15-Dec 15 harvest; July
   calendar token = `indoors`); bell-pepper se_gulf z8 (primary Mar 15-Apr 15;
   fall Sep 1-20 / Nov 1-30); onion ca_interior z8 (`"Oct - Nov or Jan - March"`, NO
   second_planting); broad-beans-fava warm_arid z8 (fall plant `"Sep"`, harvest Apr-May shared).

References: spec/plan `docs/superpowers/{specs,plans}/2026-07-09-second-planting-demux-migration*.md`;
kickoffs #16/#17/#18; STATE_HISTORY 2026-07-08 + 2026-07-09 entries; authoring convention
kickoff #18 §12.
