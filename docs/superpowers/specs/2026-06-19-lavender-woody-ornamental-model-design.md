# Lavender -- woody perennial ornamental ("subshrub") model design [anchor 14]

**Status:** design of record, drafted 2026-06-19. Awaiting Trevor's spec review before the implementation plan.

**One-line:** lavender introduces the `perennial_woody_ornamental` archetype -- a woody perennial subshrub grown for its blooms (ornamental + culinary/craft), whose defining care act is an annual hard CUT-BACK, with Mediterranean inverted care and a strawberry-style region-dependent lifecycle.

---

## 1. Context + the gap (why lavender is a strong anchor)

Lavender is already in the dataset as a blank shell (slug `lavender`, status null). The 13 certified anchors leave a real archetype hole:

| What we have | Example | Why lavender differs |
|---|---|---|
| Annual flower | zinnia (`frost_anchored`) | lives ONE season, no pruning, dies at frost |
| Herbaceous perennial for FRUIT | strawberry (`perennial_herbaceous`) | not woody; `renovation` = mow; grown to eat |
| Woody perennial for FRUIT | peach/apple (`perennial_chill_gated`), lemon/orange (`perennial_evergreen`) | fruit TREES -- orchard, rootstock, chill-gate, grown to eat |

Lavender is the FIRST **woody perennial grown for flowers** -- a subshrub (woody but not a tree), grown for blooms/fragrance, that must be cut back each year. It stress-tests four things nothing else does: (a) a woody-but-not-a-tree structure, (b) a cut-back/prune cycle as core care, (c) INVERTED Mediterranean care (lean, dry, full sun -- you kill it with kindness), (d) species-level cold-hardiness driving a region-dependent lifecycle. It is also the template for a whole family of woody ornamentals/sub-shrub herbs (rosemary, sage, thyme-as-subshrub, butterfly bush, Russian sage).

## 2. Scope (Trevor-approved 2026-06-19)

- **ONE page, anchored on English lavender (`Lavandula angustifolia`)** -- the hardy species that is BOTH the best culinary type (sweet, low-camphor) and a top ornamental. It is the spine.
- **Both uses carried, ornamental-first with culinary/craft a strong second.** "Both" lives in the varieties, the harvest cue (cut fresh for bouquets, or cut as buds just open for drying/cooking), and storage (dried bundles + dried buds).
- **Tender showy species (Spanish `stoechas`, French `dentata`) + the lavandins (`x intermedia`, e.g. Grosso) ride as VARIETIES** with a species + use + hardiness note -- NOT separate crops. One URL. (Matches the strawberry type/variety-delta seam.)

## 3. Locked design decisions

### D1 -- `calendar_basis: perennial_woody_ornamental` (the 7th basis value)
A NEW basis, joining the perennial family beside `perennial_chill_gated` / `perennial_evergreen` / `perennial_herbaceous`. Frost resolution stays ON (plant/bloom/cut-back windows anchor to frost exactly like an annual; the basis is a SHAPE signal set by `build_region_shells` at Step 3.5). Rationale for a new basis rather than reusing `perennial_herbaceous`: lavender is WOODY (prune, not mow), ORNAMENTAL (bloom-centric, no fruit/edible-harvest token), and carries no chill-gate -- a distinct deriver + distinct gates. `strawberry` is NOT `_is_tree`; lavender is likewise NOT `_is_tree` and gets its own `build_region_shells` path.

### D2 -- per-cell `grown_as` in {perennial, annual} (reuse strawberry's discriminator)
The lifecycle is region-dependent, the COLD mirror of strawberry's heat-driven flip:
- Where the anchor species is cold-hardy (English ~z5-9 = most of the country) -> `perennial` in-ground shrub.
- In the coldest zones (z3-4) or for tender varieties -> `annual` / container-overwinter (expressed via `grown_as: annual` + `container_notes` "grow in a pot you bring in"). A new `grown_as` enum value is NOT introduced -- container culture is a care/`container_notes` expression layered on `annual`, keeping the discriminator binary like strawberry.
- Per-region `grown_as` is an A5 SOURCE finding (never analogized across regions).

### D3 -- calendar tokens: reuse `dormant`, `growing`, `bloom`; ADD `prune`; plus `season_over`/`plant` for annual cells
The perennial calendar shape: `dormant` (winter, frost-bracketed) -> `growing` (spring leaf-out) -> `bloom` (summer) -> `prune` (the hard cut-back, month after bloom) -> `growing`/`dormant`. **No `harvest` token** -- for an ornamental the BLOOM window *is* the cut-for-use window (the harvest_ready prose tells the grower when/how to cut for fresh vs dried). `prune` is the new token (reusable across the woody-ornamental family; user-facing label "Cut back"). Annual cells: `plant` -> `growing` -> `bloom` -> `season_over` (mirror strawberry's annual branch; a replanted annual is not cut-back-to-overwinter). A frost-free perennial cell (no frost dates) grows year-round with the bloom+prune overlay (the strawberry hawaii / evergreen analog).

### D4 -- the CUT-BACK is a headline care moment, not buried prose
- A `growth_stages` entry "Cut back / hard prune" (the post-bloom shear by ~1/3, the load-bearing rule: NEVER into the bare leafless wood) + a lighter "Spring tidy" stage (shape as new growth starts).
- A `notifications` / `weather_triggers` beat fired after bloom: "Blooms are fading -- time to shear it back by a third, staying above the woody base."
- This is the lavender skill and the thing that keeps the plant from going woody/leggy and dying out; it earns timeline + notification prominence.

### D5 -- INVERTED Mediterranean care is the through-line ("don't love it too hard")
The care model is the inverse of most crops and is the distinctive story:
- `watering`: `drought_tolerance: high`, minimal frequency, deep-and-infrequent; **overwatering is the #1 killer.** `watering_method` lean (no overhead -- wet foliage invites rot).
- `fertilizer`: minimal to none; rich soil produces floppy, short-lived, less-fragrant plants. N/A-prose where a feed field does not apply (per the register-fill N/A rule).
- `soil`/`ph`: lean, gritty, SHARP drainage; tolerates alkaline (pH up to ~8); the opposite of the rich-moist default.
- `sunlight`: full sun, non-negotiable.
- **Disease nexus = root rot / Phytophthora from wet feet + poor drainage** (NOT the foliar-disease-heavy crops); the diagnostics lead with "yellowing/dieback = too wet, not too dry."

### D6 -- bloom-centric ornamental model (borrow zinnia's flower rails) + the dual use
- Bloom-centric care like zinnia: grown for blooms/fragrance/form, not food. A `flower`/`fragrance` descriptor; `harvest_ready_*` repurposed as the CUT cue (fresh bouquet vs buds-just-opening for drying/culinary).
- `storage` carries the DRIED path (drying bundles + dried-bud keeping), the dried analog of zinnia's vase-life-in-`storage.notes`; edible room_temp/fridge/freezer = N/A-prose.
- Culinary safety/use note (culinary buds = English/lavandin low-camphor types only; ornamental Spanish/French are not the cooking ones) -- the "both" distinction lives in the variety + use prose.

### D7 -- cold-hardiness handled LIGHTER than citrus (no A9-style coverage gate)
Citrus carries `gating_factors:["cold_hardiness"]` + per-variety + per-region suitability + an A9 coverage invariant. Lavender does NOT need that machinery: anchored on English (~z5), the CROP is hardy across most covered zones, so "which species survives" is a VARIETY-recommendation nuance, not a hard per-region cultivar gate. Handle it with: (a) the `hardiness_zone` scalar (English-anchored ~z5-9 -- and per the strawberry lesson, this RENDERS as a consumer visual, so it must cover where lavender actually grows), (b) per-variety hardiness notes (tender types flagged + "container-overwinter" guidance), (c) the D2 `grown_as` flip in the coldest zones. `gating_factors` stays empty; no A9. (If a future woody ornamental genuinely needs per-region cultivar gating, that is a separate decision.)

### D8 -- variety schema = {name, species, use, hardiness_note, delta} (strawberry/peach-shaped)
Carries the species axis + the dual use + hardiness:
- English (`angustifolia`): Munstead / Hidcote -- hardy, culinary + ornamental.
- Lavandin (`x intermedia`): Grosso / Provence -- vigorous, drying/oil, slightly less hardy.
- Spanish (`stoechas`) / French (`dentata`): ornamental, tender, the "pot you bring in" types.
Self-describing; one lavender URL; cultivars-within-a-species are clean deltas (the Phase-5 variety/delta seam, matching strawberry Section 8).

### D9 -- the deriver: `tools/woody_ornamental_calendar.py` (test-first, sibling of `berry_calendar`)
A focused deriver computing the 12-token calendar as a pure function of `grown_as` + the cell's display windows, exactly like `berry_calendar` / `tree_calendar`:
- PERENNIAL: dormant (frost-bracketed) | growing (frost-free season) | bloom (display) | `prune` (month after bloom end). Frost-free perennial -> growing year-round + the bloom/prune overlay (no dormancy).
- ANNUAL: plant -> growing -> bloom -> season_over.
Reuses `tree_calendar._months` (the shared "leading month range" parser) for DRY. Mirrors the 5-shape coverage strawberry proved (perennial frost-bracketed / frost-free + annual carried / pulled / wrapping), the carried-vs-pulled split EMERGENT from whether windows wrap or gap.

### D10 -- gates (test-first, no-op unless basis is perennial_woody_ornamental)
Two new `whole_crop_gate` sections, mirroring strawberry's A10/A11:
- **A12 `woody_ornamental_violations`** (structural cert): lifecycle scalars present; `grown_as` typed in {perennial, annual}; the `prune` token placement (perennial cells only, never annual); NO tree keys (rootstock/chill_hours_required gate/pollinizer); NO fruit/edible-harvest token; `gating_factors` empty (the D7 guard).
- **A13 `woody_ornamental_calendar_violations`** (coherence): stored `calendar[]` == `derive_woody_ornamental_calendar(grown_as, cell)` for every non-empty cell.

### D11 -- propagation / `start_method`
Lavender reaches the home grower as a NURSERY TRANSPLANT or from CUTTINGS (seed is slow + variable, not the default). It is NOT `bare_root_dormant` (deciduous) nor `grafted_nursery_tree`. The `build_region_shells` woody-ornamental path treats it as a transplant-shaped crop (`plant_out` window, no `start_indoors` seed lead-time emphasized). Exact `start_method.start` enum value (reuse `both` vs a new `nursery_transplant`) is a Step-1 implementation call; the SHAPE is transplant-out.

### D12 -- boundary scalars are a CONSUMER VISUAL (carry the strawberry lesson forward)
`hardiness_zone` (and a `reliable_bloom_zone` analog of strawberry's `reliable_fruit_zone`, if the schema carries one) RENDER on the site/app. Set them to cover where lavender actually grows + blooms (English-anchored ~z5-9, noting the tender types are narrower), NOT an over-narrow perennial-only read. This decision is now a STANDING archetype rule, not a per-crop surprise.

## 4. The arc (gold-standard checklist v2.0)
Steps 1-3 (sources + scalars + companions + the species/variety set) -> 3.5 (region shells, the new `perennial_woody_ornamental` `build_region_shells` path) -> 4 (region fill: per-cell `grown_as` + the deriver-generated calendars; PROOF-CELL-FIRST for the new sourcing shape, then scale) -> 6-8 (bulk prose, block-coherent, incl. the cut-back stages + inverted-care story) -> 9 (dash/temp sweep) -> 11 cert (verbatim + independent source-fidelity fetch + the flip). Tooling (deriver + A12/A13 gates + the shell path) is built test-first BEFORE Step 4, the strawberry sequence.

## 5. Deferrals / open questions (for the plan, not blocking the spec)
- Whether a light "spring tidy" prune is a second calendar token or care-prose only (lean: care-prose; one `prune` calendar beat).
- The exact `start_method` enum value (D11) -- Step-1 call.
- Rebloom/shearing-for-a-second-flush handling in the calendar (lean: a harvest_ready/care note, not a second bloom token).
- A future shared `perennial_woody` deriver/gating layer if rosemary/sage/butterfly-bush reveal common structure (YAGNI now; revisit at the 2nd woody ornamental).

## 6. Sources (Step-1 lane, T1 only)
Anchor candidates to verify at Step 1: extension lavender guides (e.g. USU, OSU, UMN, UC ANR/UC MG, NMSU, Texas A&M AgriLife, Washington State / WSU -- a lavender-growing region), each on the SPECIFIC publication page (the anchor-the-page rule). Culinary-use + drying claims must be T1-sourced (not seed-company/craft-blog T2).
