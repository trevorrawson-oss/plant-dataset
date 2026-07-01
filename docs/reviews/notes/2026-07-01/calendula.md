# calendula -- author-fresh DRAFT notes (cool-season refit; structure off certified zinnia / marigold)

**Slug:** `calendula` | **name:** Calendula | **archetype:** `companion_and_ornamental_flower` | **calendar_basis:** `frost_anchored`
**status:** `author_fresh_pilot` (launch flags false -- NOT certified, NOT live). PILOT.
**Output:** `calendula_crop.json` (compact-canonical) + `calendula_crop_pretty.json` (review copy).

## Gate result (spliced into a SCRATCH copy of canonical; READ-ONLY on the real canonical SHA ed8abc66)
- `whole_crop_gate.py calendula` -> **GATE: PASS (exit 0, 0 violations)**, all branches A2-A36 (B/C/D/E/F/G clean).
- `register_completeness_gate.py` (dataset-wide) -> **PASS** (0 unruled prose; only by-design deferred companion `provenance.reason`).
- `register_fill_gate.py calendula` -> **PASS** (every ruled register field authored, not null).
- `derive_realized_successions.py --check calendula` -> **up to date, exit 0** (successions_realized CC-derived 2 to 12; succession_policy.successions reconciled to max 12).
- `release_verify.py --base <canonical> --slug calendula --ref zinnia` -> **clean, no blocking concerns**: only calendula changed; catalog +none/-none (no new source ids); zinnia byte-identical; no new violations (cleared the 100+ empty-shell violations); **G: NO region calendar/heat_pause byte-identical to zinnia (all crop-specific cool-season values)** -- this is the key improvement over the marigold pilot, which carried zinnia's warm-season calendars verbatim.
- Compact-canonical confirmed: no trailing newline, no indent, no em dash, no spelled "degrees F", no `--` anywhere (incl. backend).

## THE HEADLINE: cool-season inversion (zinnia/marigold are WARM-season; calendula is COOL-season)
Calendula (*Calendula officinalis*, pot marigold) is a frost-tolerant (to ~25°F) COOL-season annual that blooms in the cool shoulders and mild winters and STOPS blooming / languishes / mildews in sustained summer heat above ~85°F -- the exact opposite of zinnia and the true marigolds (*Tagetes*). The flower-archetype STRUCTURE (companion_and_ornamental_flower, field shapes, dual-register pattern, bloom rendered as the `harvest` token) was mirrored from zinnia/marigold; the CALENDAR was inverted and modeled on the certified COOL-season annuals **lettuce-leaf and carrot**:
- **Hot regions** (low_desert_az, ca_desert, fl_peninsula, se_gulf, ca_interior, warm_arid): fall + late-winter sowings, winter/spring bloom, **summer `heat_pause`** aligned to the lettuce/carrot heat months at the same region+zone.
- **Mild Mediterranean** (ca_south_coast): near-continuous fall-through-early-summer bloom, short Jun-Aug heat pause; **ca_north_coast**: cool maritime, blooms most of the year, no heat pause.
- **Cold regions** (northern_tier z3-z6): spring sow / indoor start, summer-to-frost bloom, winter `cold_pause`, NO heat pause (cool summers); **z7** gets a Jul-Aug heat pause (hot humid summers) + spring/fall windows.
- **hawaii_tropical:** modeled MARGINAL cool-season window (~Dec-Mar bloom, long warm-season heat_pause) -- flagged (no HI-specific calendula source).
All 20 calendars derived from authored windows via `annual_calendar.derive_annual_calendar` (guarantees A5 coherence + A24 placement); heat_pause months align to the calendar tokens.

## Other key calendula-vs-zinnia/marigold refits (biology fully re-derived)
- **Companion framing REFIT (load-bearing honesty):** calendula is NOT a true marigold and is NOT claimed to suppress root-knot nematodes (the documented *Tagetes* effect that marigold leads with). Its companion value is pollinator + beneficial-insect (aphid-predator) support (likely/medium), a traditional aphid trap/decoy crop (traditional/low; sound mechanism, not formally trialed), and a cool-season habitat companion (traditional/medium).
- **Edible/herbal tradition (honest, hedged):** edible ray petals as a "poor man's saffron" color substitute (UMN edible flowers: "slightly bitter saffron substitute; more for color than flavor"); long traditional skin-salve/cosmetic use, framed as tradition. Storage refit to petal-drying rather than marigold's pure cut-flower framing.
- **Heat = WARNING, not reassurance:** the "Hot weather ahead" weather-trigger + a summer-heat notification warn that bloom ends in heat (the inverse of marigold's "summer is their peak" copy). `succession_policy.pause_in_heat: true` (marigold: false).
- **Numbers re-derived:** pH 6.0-7.0 (tol 5.5-7.5); spacing 8-12 in; germination 60-70°F soil, 1-2 wk (cover seed, light inhibits); days_to_maturity [45,60] mid 55 (~6-8 wk to first bloom); light feeder, 10-10-10; height 8-24 in; full sun to part shade.
- **Pests refit:** Aphids (calendula is an aphid magnet, hence the trap-crop angle), Whiteflies, Slugs/snails. **Diseases refit:** Powdery mildew (HIGH, the signature, worsens with heat/humidity), Damping-off/root rot (cold wet soil), Cucumber mosaic + aster yellows (insect-vectored, seasoned/low). Replaces zinnia/marigold's Botrytis-led set.
- **Varieties refit:** Pacific Beauty, Bon Bon, Resina (herbal/salve), Indian Prince, Snow/Ivory Princess, Calypso, Greenheart Orange (open-pollinated, come true from seed; self-sows).

## Sources (all EXISTING catalog ids, all T1, all calendula pages WebFetch-verified live 2026-06-30)
| catalog id | calendula page used as anchoring URL |
|---|---|
| `usu_ext` | extension.usu.edu/yardandgarden/research/calendula-in-the-garden (frost to 25°F; <85°F, stops blooming in heat; pH 6-7; spacing 8-12 in; germ 60°F) |
| `uwi_hort` | hort.extension.wisc.edu/articles/calendula-calendula-officinalis/ (NOT a true marigold; languishes in hot summer, recovers when cool; blooms to first heavy frost; CMV) |
| `ncsu_ext` | plants.ces.ncsu.edu/plants/calendula-officinalis/ (Asteraceae; height 1-2 ft; pests aphids/whiteflies/slugs; powdery mildew; pollinators; edible) |
| `ufifas_ext` | ask.ifas.ufl.edu/publication/FP087 (FPS87/FP087; cool-season annual; Florida per-zone planting table z7 May / z8 Mar-Apr+Sep-Oct / z9 Nov-Mar / z10-11 Dec-Feb) |
| `umn_ext_edible_flowers` | extension.umn.edu/flowers/edible-flowers ("Calendula: petals are a slightly bitter saffron substitute; more for color than flavor") |

No new catalog entries added (release_verify confirms catalog +none/-none). Convention matches the draft batch: reuse the catalogued publisher id, point its anchoring URL at the crop-specific verified page.

## Flags / modeled values (all in `verification_status.open_findings`, all `blocks_launch:false`)
1. **finding_001 -- cool-season regional calendars MODELED on lettuce-leaf/carrot + UF/IFAS FP087.** Per-region windows are modeled on the certified cool-season peers and the FP087 zone table; a calendula-specific dated regional table per region would tighten them.
2. **finding_002 -- hawaii_tropical MODELED + MARGINAL.** Cool/dry-season window (~Dec-Mar) inferred from calendula's heat physiology; no readable Hawaii-specific calendula source (CTAHR not used for this crop).
3. **finding_003 -- companion FRAMING boundary (info).** pot-marigold-is-not-Tagetes; no nematode claim; pollinator/aphid-trap/habitat framing; edible-petal + traditional-salve honesty.
4. **finding_004 -- heat_pause month boundaries modeled to the cool-season peers**, backed by the crop-level heat sources (USU/UW/UF-IFAS), not a calendula-specific per-zone heat table.

## Discipline notes
- READ-ONLY on `crops_data_final.json` throughout; all gate/derive runs used a spliced SCRATCH copy.
- Compact canonical (`separators=(",",":")`, `ensure_ascii=False`, no trailing newline). American English; `°F`; "calendula"/"plant" lowercase except sentence start.
- Dispatch contract honored: `gating_factors` and `zone_independent` ABSENT; full 10-region roster; legacy `zones` 3-11 (all-null shells, region-primary model); non-empty 12-token calendars; `plant_out` filled in all 20 cells; `successions_realized` left CC-derived (deriver reproduces them exactly, --check up to date).
- Cool-season planting-timing guardrail: calendula plants only in fall/winter/cool-shoulder windows in every WARM region (aligned to lettuce/carrot), never into excluding summer heat; both spring AND fall windows present where the peers have them.
