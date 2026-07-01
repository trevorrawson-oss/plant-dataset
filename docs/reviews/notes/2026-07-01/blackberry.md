# blackberry authoring notes (author_fresh_pilot, 2026-06-30)

Blackberry (`Rubus` subgenus *Rubus*) authored by FILLING its shell, modeled structurally on the
certified **blueberry** (`berries_woody`) and refit with the CANE biology of the **raspberry pilot**
(`scratchpad/raspberry_crop.json`), its closest analog. Output: `scratchpad/blackberry_crop.json`
(pretty-printed for review; splice into canonical writes compact). Canonical was READ-ONLY.

## Archetype + gate path
- `calendar_basis: "berries_woody"`, `archetype: "berries_woody"`, `type: "berry"` (shell had the
  wrong `fruit_tree` + `frost_anchored` scaffold values -> corrected).
- Blackberry is a **CANE** berries_woody fruit, so it takes the CANE sub-form of the already-
  generalized `berries_woody_gate.py` (keyed on `cane_type`): a real `cane_type` value ->
  `self_fertile` is a bool, `recommended_type` enum `{summer_bearing, everbearing}`. **The gate was
  NOT modified** (it was generalized during the raspberry pilot); blackberry passes the CANE path
  as-is. Confirmed the path is live, not no-opping, by injecting 4 defects into a scratch copy
  (self_fertile=None, a `season_over` token, cane_type=not_applicable->BUSH, a bush `rabbiteye`
  recommended_type) -- all 4 bounced with the correct A15/A16 messages.

## Cane-type model (mirrors raspberry's cane adaptations)
- `cane_type: "both_summer_and_everbearing"` (crop-level). Per-cell `recommended_type`:
  - **summer_bearing (floricane)** = the dominant/default: 16 cells (all the temperate + Southern +
    California regions). Floricane erect/semi-erect/trailing types fruit on 2nd-year canes.
  - **everbearing (primocane-fruiting)** = 4 cells: the cold-North marginal cells (northern_tier
    z3/z4, mow-to-ground strategy) and the chill-marginal frost-free tropics (fl_peninsula z11,
    hawaii_tropical z11). Backed by the U-Arkansas **Prime-Ark** line (Freedom, Traveler, 45).
- **Coverage invariant satisfied**: 12 summer_bearing + 3 everbearing varieties cover both cell types.
- `self_fertile: true` (cane fruits are self-fertile; the deliberate INVERSE of blueberry's
  bush cross-pollination model). No apple/tree cross-pollination machinery; no rootstock/pollinizer.

## Habit axis (the blackberry-specific refit, covered in `type_selection_*` + varieties)
- **ERECT** (self-supporting when summer-tipped to 3-4 ft, sucker from the ROOTS to form a hedgerow):
  Ouachita, Navaho, Osage, Arapaho (thornless); Apache, Kiowa (thorny).
- **SEMI-ERECT** (thornless, very vigorous arching canes, CROWN-forming = no root suckers, propagate
  by tip layering, MUST trellis): Triple Crown, Chester.
- **TRAILING** (prostrate, MUST trellis, LEAST cold-hardy, earliest/most-flavored): Marionberry,
  Boysenberry (Pacific NW / cool coastal CA).
- **Thornless vs thorny** treated as the third explicit selection axis throughout.
- `leaf_habit: "deciduous"` on every cell (blackberries require winter chill and defoliate; no
  evergreen form -- same call as the raspberry pilot). Every deciduous cell carries the `dormant`
  cycle per A15 token placement.

## Biology refits vs raspberry (genuinely re-authored, not copied)
- **Harvest / fruit structure**: the aggregate fruit keeps its white receptacle (torus) INSIDE the
  berry -- a picked blackberry is solid, NOT hollow like a raspberry; ripe = turns from glossy to a
  DULL deep black and detaches (Clemson). Does not sweeten after picking.
- **Climate inversion**: hardiness **z5-9** -- LESS cold-hardy than raspberry (z3) but MUCH more
  heat-tolerant -> the caneberry of the South. So the SOUTH (se_gulf, ca_interior, warm regions,
  central/north FL) is PRIME (raspberry's marginal cells); the far-NORTH cold zones (z3/z4) and
  chill-less tropics (z11) are blackberry's marginal cells. Marionberry/trailing tender below ~13°F.
- **Chill**: LOWER than raspberry. `chill_hours_required: 400`, `chill_hours_range: [200, 900]`.
  Low-chill Southern types (Kiowa ~200, Natchez/Ouachita/Prime-Ark ~300) vs high-chill (Navaho,
  Apache, Chester ~800). Per-variety numeric chill_hours_required == range low end (A21).
- **Pests**: SWD (major modern pest), **red-necked cane borer** (Agrilus ruficollis -- the
  blackberry-characteristic cane-GALL borer), raspberry crown borer, stink bugs (uneven drupelet
  ripening -- a Southern blackberry issue), Japanese beetle, aphids.
- **Diseases**: Phytophthora root rot, **rosette / double blossom** (Cercosporella rubi -- the
  Southeast's signature blackberry disease; witches'-broom of buds, sterile flowers, rogue out /
  resistant cultivars / disease-free stock / mow-and-restart), anthracnose, cane & spur blight,
  **orange rust** (systemic -> rogue out the whole plant; blackberries especially susceptible).
- `productive_lifespan_years: [15, 20]`; `years_to_first_harvest: [1, 2]` (primocane types fruit yr 1).

## Regions (10, full canonical roster; frost data reused from zone_frost_data, crop-invariant)
Region windows/types are per-region T1 findings refit for cane biology; `calendar[]` DERIVED by
`derive_berry_woody_calendars` (20/20 cells filled, 0 skipped). northern_tier z3/z4 + fl_peninsula
z11 + hawaii z11 are honestly flagged marginal in the prose (best-effort hardy/low-chill windows).

## Sources -- existing catalog T1 only (all verified T1, read live 2026-06-30)
clemson_hgic, ncsu_ext, uga_ext, tamu_agrilife, ucanr_ext, uc_mg, cornell_ext, psu_ext, umn_ext,
usu_ext. Real blackberry-specific URLs confirmed via WebSearch/WebFetch (NEVER curl/wget/pdftotext).

### FLAGGED uncatalogued authorities (NOT cited; modeled around with catalogued T1)
- **Oregon State University Extension** (EC 1303 / EC 1617) -- the definitive trailing-blackberry /
  marionberry authority for the Pacific NW -- is NOT in `source_catalog`. Trailing-type content was
  grounded in catalogued UC ANR/IPM + UC Master Gardener (CA trailing) + NC State + Clemson instead.
- **University of Arkansas** fruit-breeding program (John R. Clark) -- origin of Prime-Ark, Ouachita,
  Natchez, Navaho, Osage, Apache, Kiowa -- is NOT in `source_catalog`. Cultivar content grounded in
  NC State / Clemson / UGA / Texas A&M / Utah State, which document the same cultivars.
- Recorded as open_finding `blackberry_pilot_uncatalogued_sources` (blocks_launch: false).

## Gate result (whole_crop_gate.py against a spliced scratch canonical)
**GATE: PASS (exit 0)** -- all A-sections A2-A37 clean, B/C/D/E/F/G clean.
- **A37 (calendar coherence): 0 violations** -- no separate A37 lines to report. Harvest spans are
  contiguous (no Bug-2 holes); Bug-1 (growing-after-harvest) is frost_anchored-only so berries are
  exempt. Nothing needed hand-fixing / central normalization.
- Two fixes during self-verify: A21 (Natchez/Arapaho variety chill_hours_required lowered to the
  range low end) and C/D (6 `degrees F` -> `°F`). No em dashes in consumer copy; the only `--` are
  in backend `verification_status.open_findings` (allowed).
- `status: author_fresh_pilot`, `launch_ready_core/seasoned: false`, all open_findings
  blocks_launch: false. A green gate is a DRAFT, not a certification.
