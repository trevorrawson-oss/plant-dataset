# Author-batch kickoff — the next ~20 crops (all Claude Code)

**Position (2026-07-02):** canonical `f7ab0ac2`, **80/125 certified**, 45 honest shells left. The
30-crop overnight batch (`_handoff/batch_2026-06-30/`) is fully certified and consumed.

**Lane (current, supersedes CLAUDE.md's stale two-lane rule):** authoring runs **100% inside Claude
Code**, unattended. There is no claude.ai handoff (it required Trevor awake to shuttle content). This
session AUTHORS drafts; a **separate fresh Claude Code session CERTIFIES** them (source-truth review
-> rulings -> promote), exactly as batch 1 was done. Keep that author/certify split: the independent
review pass is what caught every citation defect in batch 1 (dead URLs, mis-pointed keys, the potato
UC-IPM "warm-weather" mis-anchor).

---

## How to run this batch (fan-out)

Author **one subagent per crop** (isolated context), dispatched in parallel in waves of ~5. Each
subagent researches with WebFetch/WebSearch, re-derives the biology, and writes ONE full record. The
orchestrator only collects + stages the finished records and writes the batch report. This keeps the
orchestrator lean; the heavy authoring context lives in the disposable subagents.

Do NOT author all 20 inline in the orchestrator thread. Do NOT reuse a long/compacted session — start
fresh (this doc + CURRENT_STATE are the whole pickup).

---

## Target roster — recommended 20 (strong templates, high confidence)

Every value below must be RE-DERIVED for the target; the template gives STRUCTURE ONLY (see the
authoring contract). "Key refit" is the biology that MUST change from the template.

| # | target | template (certified) | key refit |
|---|---|---|---|
| 1 | slicing-cucumber | cucumber | standard slicer DTM/variety split; trellis-or-ground; own pest/disease timing |
| 2 | pickling-cucumber | cucumber | shorter DTM, pickling varieties, harvest-small, heavier set |
| 3 | english-cucumber | cucumber | parthenocarpic/seedless, thin skin, trellised/greenhouse habit |
| 4 | banana-pepper | bell-pepper | mild Scoville (0-500), DTM, sweet/mild use |
| 5 | habanero | cayenne-pepper | Scoville 100k-350k, long DTM, strong heat requirement, Capsicum chinense |
| 6 | heirloom-tomato | beefsteak-tomato | open-pollinated (not hybrid), higher disease susceptibility, indeterminate, variety diversity |
| 7 | grapefruit | orange-navel | larger fruit, long ripening, higher heat need, rootstock notes |
| 8 | lime | lemon | more cold-tender, smaller, everbearing tendency |
| 9 | mandarin-clementine | orange-navel | cold-hardier, easy-peel, often seedless/parthenocarpic |
| 10 | pole-beans | green-beans-bush | climbing habit, trellis, longer progressive harvest, taller |
| 11 | sugar-snap-peas | snow-peas | edible pod + swollen peas, similar cool-season window, own DTM |
| 12 | broad-beans-fava | snow-peas | Vicia faba, very cold-hardy/overwintered, large seed, own pests (aphids/chocolate spot) |
| 13 | rosemary | lavender | woody Mediterranean subshrub (DIRECTIONS names this pair); culinary use, hardiness, bloom |
| 14 | sage | lavender | woody Mediterranean perennial, culinary, own pests |
| 15 | thyme | lavender | low woody Mediterranean perennial, culinary, mat habit |
| 16 | oregano | lavender | spreading Mediterranean perennial, culinary, can be invasive |
| 17 | mint | parsley | spreading perennial (contain it), moisture-loving (opposite of the Mediterranean herbs) |
| 18 | chives | parsley | clumping perennial allium herb, cut-and-come-again, own (allium) pests |
| 19 | lemongrass | basil | tender tropical clumping grass, warm-season/overwinter-indoors, Cymbopogon |
| 20 | sweet-potato | potato | BIGGER refit: warm-season Ipomoea (not Solanum), slips not seed-potatoes, vining, long warm DTM |

`#20 sweet-potato` is the one meaningful stretch (template gives root-veg structure only; nearly all
biology changes). Drop or swap it if you want a cleaner all-easy 20.

### Defer — needs a decision or a novel template first (NOT in this batch)
- **collard-greens** — `collards` is ALREADY certified. Confirm with Trevor whether this is a
  duplicate slug to retire/merge, a variety split, or a rename BEFORE authoring anything.
- **mushrooms (5)** — button, oyster, shiitake, lions-mane, wine-cap: no certified template + a novel
  non-seasonal indoor archetype (spawn/substrate, not planting calendars). Needs its own archetype
  design pass.
- **asparagus, artichoke** — perennial crown crops with no clean certified template; design first.
- **avocado, olive** — subtropical evergreen trees; pick a template (orange-navel/fig) + refit deliberately.
- **sweet-corn** — warm-season block-planted grass; no close template.
- **companion/pollinator flowers (cosmos, sweet-alyssum, sweet-pea, bee-balm, borage, chamomile,
  echinacea)** — doable off zinnia/calendula/marigold, but lower priority than the edibles above.
- **microgreens (7)** — trivially templated on `microgreens-mix` (indoor, non-seasonal, zone-independent);
  a good separate easy fan-out if you want volume, but repetitive and low individual value.

Trevor confirms the final roster before authoring starts.

---

## The authoring contract (per crop) — the non-negotiables

These are distilled from `docs/kickoffs/05-author-bot/KICKOFF.md` (the proven spec). The two failure
modes below are exactly what bots do; a draft that hits either is worthless.

1. **REFIT, don't copy-template.** The template gives STRUCTURE ONLY (which fields exist, their shape,
   the archetype, the 10-region/zone layout, the dual-register pattern). EVERY biological value is
   re-derived for the target from real sources: pH, spacing, days_to_maturity, chill/heat needs,
   sunlight, germ temp; pests, diseases, companions, rotation family; per-region planting/harvest
   calendars; variety list. A target that ships the template's pH, pests, or calendar is a FAILED draft.
2. **SOURCE-OR-FLAG, never fabricate, never extract.** Every claim-bearing value cites a REAL Tier-1
   source (US university cooperative extension / .edu) for the target, with a real working URL, in the
   existing `source_catalog` + `anchoring_urls` shape. No invented source IDs, no placeholder/TODO
   URLs, no citing a page that does not cover the claim. If you cannot read a clean source for a value,
   FLAG it as modeled in `verification_status.open_findings` (blocks_launch:false) + the notes file,
   cite the nearest catalog id, and MOVE ON. NEVER curl/wget/pip/pdftotext/PDF libraries (denied, will
   fail) — a scanned-PDF-only value is a flagged gap, not a rabbit hole.
3. **COOL-SEASON TIMING GUARDRAIL (the broccoli-bug class).** A cool-season crop must not be planted
   into summer heat that excludes its cool-season peers. In each warm region, check plant months
   against certified peers (lettuce-leaf, carrot): if they heat_pause a month, yours almost certainly
   should too. `plant_out` must include BOTH the spring AND fall windows; calendar plant tokens must
   agree with `plant_out`. Exception: a genuinely long-season indoor-start crop whose `plant_out` says so.
4. **Dispatch fields correct:** `calendar_basis` (one of the 7), `archetype` (maps to that basis),
   `zone_independent` (true only if non_seasonal_indoor), `gating_factors` (chill_hours for a
   chill-gated tree, heat_accumulation if heat-gated, photoperiod if day-length-gated; bolting-by-cold
   is vernalization, NOT photoperiod -> no gating_factor).
5. **Coverage:** the full 10-region roster (ca_desert / ca_interior / ca_north_coast / ca_south_coast /
   fl_peninsula / hawaii_tropical / low_desert_az / northern_tier / se_gulf / warm_arid), each region
   with real `resolved_by_zone` cells keyed by USDA zone (3-11), each non-tree cell carrying a
   NON-EMPTY calendar.
6. **Dual-register:** every established consumer-prose field carries BOTH `_seasoned` AND `_beginner`
   (description, care/watering/fertilizer, harvest, storage, region_notes, tips, ...). Soil TEXTURE is
   categorical chips (string arrays); soil PROSE is `preferred_description_{seasoned,beginner}`.
7. **Hard rules (consumer copy):** American English; NO em dashes (commas/colons/semicolons/periods);
   temperatures render as `°F`; "plant" lowercase except at sentence start. Canonical JSON is COMPACT.

Do NOT relitigate any locked decision in CURRENT_STATE.md "Live locked decisions / guardrails" — read
them and conform (archetype/dispatch rules, chill/heat modeling, bolting=vernalization, etc.).

---

## Output shape (what the certify session consumes)

Write into `_handoff/batch_<TODAY>/` (e.g. `_handoff/batch_2026-07-02/`), mirroring
`_handoff/batch_2026-06-30/` exactly:

- **`crops/<slug>.json`** — one full record per crop, canonical-COMPACT
  (`json.dumps(..., separators=(",",":"), ensure_ascii=False)`, no trailing newline), slug exact,
  **spliceable byte-for-byte** into the canonical. Set the draft `verification_status`:
  `status:"author_fresh_pilot"`, `launch_ready_core:false`, `launch_ready_seasoned:false`,
  `last_audited:null`, plus `open_findings:[]` (each `blocks_launch:false`) for every modeled/judgment
  value, `source_set`, and a `verification_log_ref` describing what was authored + flagged.
- **`notes/<slug>_NOTES.md`** — per crop: output line, the self-gate result, the key template->target
  refits, the exact source ids used (all real T1, read via WebFetch), and the FLAGS list (mirrors
  open_findings). Model on `_handoff/batch_2026-06-30/notes/celery_NOTES.md`.
- **`BATCH_normalized.json`** — the full canonical (all 125 crops + top-level metadata) with the new
  drafts spliced in by slug, normalized. This is what the certify session splices/gates from.
- **`MORNING_REPORT.md`** — the batch summary: what was authored, per-crop watch-items and honesty
  boundaries (e.g. batch 1 flagged calendula's Tagetes boundary and potato's greening/solanine), any
  crop that needs a Trevor decision, and the base canonical SHA authored against.

**READ-ONLY on `crops_data_final.json`.** All work on a scratch copy under the session scratchpad; the
canonical is never modified in the author lane.

## Self-gate before you call a draft done (catch structure early)

Splice the draft into a scratch copy of the canonical and run, per crop:
- `python3 tools/whole_crop_gate.py <slug> <scratch>` -> must exit 0 (A2-A36 + B-G clean)
- `python3 tools/derive_realized_successions.py --check <slug>` -> up to date (exit 0)
- `python3 tools/release_verify.py <scratch> --base crops_data_final.json --slug <slug> --ref lettuce-leaf`

Structural bounces get fixed in the author lane, not punted to certify. (The gates catch STRUCTURE;
the certify session's source-truth review catches SUBSTANCE — real URLs, on-point citations.)

## Read these (do not reinvent the conventions)
- CURRENT_STATE.md — position + the locked decisions/guardrails.
- The template crop's full record in `crops_data_final.json` — the structure + register pattern to mirror.
- `docs/kickoffs/05-author-bot/KICKOFF.md` + `DIRECTIONS.md` — the proven per-crop authoring spec + template-pairing method.
- `docs/methodology-and-sourcing.md` — the sourcing bar (Tier-1 extension; source-or-flag).
- `docs/register_bearing_field_inventory_v1_0.md` — which fields are dual-register prose vs categorical.
- `_handoff/batch_2026-06-30/` — the exact handoff to mirror (crops/, notes/, BATCH_normalized.json, MORNING_REPORT.md).
