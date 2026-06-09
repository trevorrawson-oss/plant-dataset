# Heat-anchor token proposal v0 (FOR RATIFICATION)

**Status:** RATIFIED 2026-06-08 (Trevor) -- v1. Asks 1-5 resolved: token `heat_threshold_start/end`
(single, backend); per-crop `heat_threshold_temp_f`; carrot measures AIR (see 3 -- RESOLVED 2026-06-09: T1 evidence is air, not soil); coexists with
`bolt_threshold` (no lettuce migration); sequence locked. **Plus (Trevor): the simple-vs-soil
framing the user sees is DUAL-REGISTER COPY, not two tokens** -- see 2a. Surfaced by carrot
Step 4 (cool-season ROOT family's warm windows are heat-bounded, but carrot does NOT bolt, so
lettuce's `bolt_threshold` is the wrong mechanism + threshold to reuse, A1). Implement: lock the
token + author carrot's 9 warm regions. (WeatherKit spike: Trevor's call, now or defer.)

---

## 1. Problem

Every cool-season crop has a heat ceiling that closes its warm-region cool window and
reopens it in fall. The dataset already encodes one such anchor -- lettuce's
`bolt_threshold_start/end` (heat -> bolting -> bitter, ~75 degrees F). But the heat
FAILURE MODE differs by crop:

- leafy greens (lettuce): **bolting** (`bolt_threshold`)
- warm-season fruiting (tomato): **fruit-set failure** (`heat_pause` + parked `fruit_set_temp_f`)
- **root crops (carrot/beet/radish/turnip/parsnip): root-quality collapse in hot soil**
  (forking, coarse, strong-flavored) -- a DIFFERENT mechanism and a DIFFERENT temperature

Reusing `bolt_threshold` on a root crop would (a) label carrot's biology as "bolting"
(false -- carrot bolts in year 2, not as its in-season heat failure) and (b) resolve at
lettuce's bolting temp instead of carrot's root threshold. A1: derive from the crop's own
biology; shape borrowing is never value/biology borrowing. -> we need a crop-agnostic heat
anchor.

## 2. The token (dataset side)

Crop-agnostic, parallel to `bolt_threshold_start/end` and `first_frost`/`last_frost`:

- **`heat_threshold_start`** -- sustained heat rises past the crop's ceiling; CLOSES the
  cool/spring window (a `harvest_end`/window-close anchor).
- **`heat_threshold_end`** -- sustained heat recedes below the ceiling; OPENS the fall
  window (a `direct_sow`/window-open anchor).

Used exactly like the existing anchors: in `plantings[].<window>[].from` and in
`resolution_source.anchor_threshold`. Anchors are free-string tokens (no central registry),
so wiring is just: use it + confirm the gates accept it (they will -- they don't validate
anchor-token names).

### 2a. The token is backend; the simple-vs-soil framing is DUAL-REGISTER COPY (Trevor 2026-06-08)

The token is an internal identifier the weather-resolver reads -- it is NEVER rendered to
users (users see the resolved DATE + the prose explanation). So it stays a SINGLE name. The
"beginner says heat, seasoned says soil-temp" split that Trevor wants is handled where it
belongs -- in the dual-register `region_notes` / window prose -- NOT as two tokens:
- **beginner:** plain -- "Stop planting before the soil gets hot, or the roots turn tough and
  bitter."
- **seasoned:** precise -- "Sustained soil temperatures above ~X degrees F degrade root quality
  (forking, coarse texture, strong flavor)."

Same boundary, two registers. claude.ai authors both when it writes the warm regions (as it did
the NT `region_notes`). This is the standard dual-register treatment, applied to the heat boundary.

## 3. The per-crop threshold value

A crop-level field **`heat_threshold_temp_f`** (mirrors the tomatoes' parked
`fruit_set_temp_f`): the temperature ceiling, set PER CROP from T1 sources, with an
explicit note of what it measures (soil vs air).

- **Carrot measures AIR temperature -- RESOLVED 2026-06-09 (Trevor).** The original draft said
  SOIL ~75-80 degrees F, but that was unsourced: the T1 evidence frames carrot's ceiling as AIR
  (UF/IFAS AE588, 61-75 degrees F optimum air growth/root-color); UGA/NMSU state no soil-temp
  ceiling. **Authored: `heat_threshold_temp_f = {temp_f: 75, measures: "air", sources:
  [ufifas_ae588]}`** (the ceiling = top of the optimum). Mechanism is soil-driven, but air is the
  sourced, measurable proxy AND what WeatherKit resolves directly (so the air->soil model is moot
  for THIS anchor; germination keeps its soil anchor `soil_temp_40f`).
- **Coexists with `bolt_threshold`** -- bolting crops (lettuce) keep `bolt_threshold` (a
  distinct mechanism with a daylength component). NO lettuce migration. The two anchors
  serve different mechanisms.
- **Family:** carrot/beet/radish/turnip/parsnip all use `heat_threshold` + each its own
  `heat_threshold_temp_f`. Carrot is the first + sets the template.

## 4. resolution_source shape (UNCHANGED -- no new structure)

```
{ "resolution_tier": "forecast_api", "source_id": "weatherkit",
  "anchor_threshold": "heat_threshold_start", "horizon_days": 10,
  "fallback_beyond_horizon": "stored_date" }
```
Identical to `bolt_threshold`/frost. Only the `anchor_threshold` token + the per-crop temp
are new.

## 5. plant-astro resolution (the consumer -- confirmed plant-astro; no app repo until the JSON is built)

- **NOW (static):** plant-astro renders `stored_date` = the sourced regional months (the
  "google carrots zone 9 central valley" answer). Zero WeatherKit needed. Carrot ships today.
- **LATER (dynamic):** a Netlify serverless/edge function calls WeatherKit REST (JWT ES256,
  Trevor's Apple developer account) to resolve anchors for the user's ZIP / lat-lon.
- **KEY INSIGHT that scopes WeatherKit's real role:** WeatherKit's forecast horizon is
  ~10 days. Planting windows are months out. So for almost the whole planning year,
  `fallback_beyond_horizon: stored_date` does the work -- WeatherKit only "goes live" when
  an anchor date is within ~10 days. **So even fully wired, the website's planting CALENDAR
  is stored dates; WeatherKit is a near-term "it's time now" refinement** (and the
  notification trigger in a future app). The stored months carry the planning UX; WeatherKit
  is polish on the near edge. (This is why the dynamic layer is NOT a blocker for carrot.)

## 6. WeatherKit-on-plant-astro spike (bounded; optional; validates the architecture)

If we want to de-risk the dynamic pipeline early (dev account is ready):
- One Netlify function: ZIP/lat-lon -> sign a WeatherKit JWT (team ID + key ID + `.p8`
  private key as Netlify secrets) -> `GET weatherkit.apple.com/api/v1/weather/{lang}/{lat}/{lon}?dataSets=forecastDaily`
  -> compute when temp crosses a threshold -> return the resolved date, or `stored_date`
  beyond the horizon.
- Scope: ONE anchor, ONE ZIP, end-to-end. Proves JWT auth + REST + threshold-crossing
  against the dataset's `resolution_source` shape. A focused build, not the full feature.
- **Surfaces a real pre-existing question worth nailing once:** WeatherKit returns AIR temp
  (+ precip, etc.), NOT soil temp. Carrot's `heat_threshold` (soil) AND the already-shipped
  `soil_temp_40f` both need an air->soil model (soil lags/damps air). The spike should pin
  down how soil anchors resolve -- it's the same open question for every soil anchor, not
  just this one.

## 7. Ratification asks (Trevor)

1. Token name `heat_threshold_start` / `heat_threshold_end` -- OK? (alt: `soil_heat_threshold_*`)
2. Per-crop field name `heat_threshold_temp_f` -- OK? (mirrors `fruit_set_temp_f`)
3. Carrot's ceiling measures SOIL temp (root crop) -- agree?
4. Coexist with `bolt_threshold`, no lettuce migration -- agree?
5. Sequence: lock token -> claude.ai authors carrot's 9 warm regions with `heat_threshold`
   + `stored_date` fallback (from the already-locked `WARM_REGION_sourced_windows_handoff`)
   -> Step 4 closes. WeatherKit spike: now (validate) or defer?

## 8. Open (claude.ai, with the warm-region authoring)

- Carrot's exact `heat_threshold_temp_f` value + citation.
- The per-region window months are already sourced (`WARM_REGION_sourced_windows_handoff.md`);
  author them with the token + `stored_date` fallback. Window counts are A5 source findings
  (do NOT normalize).
