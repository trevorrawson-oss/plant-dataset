# roma-tomato author-bot notes

Authored by FILLING the `roma-tomato` shell, modeled on certified **cherry-tomato**
(closest template: same species *Solanum lycopersicum*, different type). Canonical was
READ-ONLY throughout; work happened on a spliced scratch copy. base_sha (canonical at
authoring) = `8432195016415dfe12acb396c3a8493152315a41ceddd8e6bd108c6eb1a282e5`.

## Why cherry is the right template + what was legitimately shared vs re-derived
Cherry and roma are the same species, same frost-anchored transplant culture, same 10-region /
zone 3-11 layout, same core pest/disease suite, same self-fertile / warm-season-fruiting archetype.
So the STRUCTURE (region cells, calendars, sources, notifications, growth stages, weather triggers,
failure diagnostics) is honestly shared. Everything type-specific was re-derived (see below). The
gate contract is met: frost_anchored, warm_season_fruiting, full 10-region roster, zones 3-11,
12-token calendars, plant_out filled, second-plantings carried, heat_pauses backed, dual-register
on every consumer field, no em dashes, °F.

## The determinate refit (roma vs cherry) -- the core of the job
- **det_indet.type: indeterminate -> DETERMINATE.** Rewrote both registers: fixed bushy size,
  concentrated fruit flush over 2-4 weeks, cage not tall stake, and the key culture flip -- do NOT
  prune suckers on a determinate (each carries fruit), unlike an indeterminate.
- **Concentrated harvest** threaded through description, yield_expectations (8-15 lb as one flush,
  not season-long trickle), peak_production, harvest_ready, growth_stages.harvest, tips.harvest,
  and the first_harvest notification. Removed the "pick daily to keep it producing" indeterminate
  logic wherever it appeared.
- **Paste/plum fruit:** meaty, thick-walled, dry, few seeds -> sauce/canning framing in description,
  storage (freezes/cans especially well), varieties, harvest_ready.
- **Blossom-end rot as the signature roma issue:** BER disease entry elevated medium -> **high**,
  prose rewritten to explain why paste/determinate types are especially prone (dense blocky fruit +
  heavy simultaneous load outpaces calcium delivery); even-moisture / mulch fix reinforced across
  ph, soil, watering, container, and failure_diagnostics.

## Other re-derived biology (NOT carried from cherry)
- days_to_maturity [55,70] -> **[70,80]**; days_to_maturity_mid 62 -> **75**.
- ph.preferred_range [6.0,6.8] -> **[6.2,6.8]** (per brief); pH prose restated to 6.2-6.8 (passes
  A34 cross-consistency).
- spacing_inches [24,36] -> **[24,30]** (compact determinate; 24 in operative per brief).
- varieties.recommended replaced wholesale with roma/paste cultivars (Roma VF, San Marzano, Amish
  Paste, Viva Italia, Big Mama, Plum Regal, Health Kick, Window Box Roma); container varieties too.
- **Pests:** replaced Spider mites with **Whiteflies** to match the brief's roster
  (hornworm/aphids/flea-beetle/whitefly). Both are real tomato pests; swap follows the brief.
- **Diseases:** added a combined **Fusarium and Verticillium wilt** entry (VF resistance is the roma
  buying signal); kept early+late blight, Septoria, BER.
- Rule-layer harvest_start offsets (from plant_out_start) bumped 55/58/60/62 -> **70/72/74** to match
  the ~75-day DTM, so the plantings rules stay internally consistent with the "70 to 80 days" prose.

## Sourcing (existing catalog T1 only, per brief)
- Reused cherry's Tier-1 extension sources + anchoring URLs unchanged (same species; the same
  extension tomato factsheets cover roma). Gate E: 43 distinct source IDs, 0 uncatalogued, 0 non-T1.
- One URL corrected: cherry's DTM/det_indet anchor pointed at a cherry-specific Clemson page
  (`.../mild-peppers-unique-cherry-tomatoes/`); repointed to the general Clemson tomato factsheet
  (`hgic.clemson.edu/factsheet/tomato/`), a real page covering roma DTM.
- New whitefly + wilt entries cite already-catalogued T1 pages: Clemson tomato-insect-pests, NCSU
  pests-of-tomato, UMN tomato-disorders, Clemson tomato-diseases-disorders (all real, all T1).
- No new source IDs invented; no fabricated citations.

## Judgment calls to surface for the daily biology review
1. **Calendar display windows kept at cherry's values (gate-clean), rule offsets bumped to roma
   DTM.** At month granularity roma and cherry share the same frost-bracketed tomato season, so the
   resolved_by_zone display calendars/windows were inherited (they pass A5/A24/A37 as certified).
   The rule-layer harvest_start offsets were bumped to 70-80 days, so the live recompute now lands
   ~1-2 weeks later than the stored display window. Reviewer/normalizer may want to shift the stored
   harvest windows ~2 weeks later and tighten them to reflect the determinate concentrated flush
   (cherry's windows show continuous indeterminate production). Flagged rather than hand-shifted to
   avoid introducing A37 harvest-holes.
2. **succession_policy.suitable kept = false** (mirrors cherry; keeps A8 out-of-scope). Determinate
   roma is arguably succession-suitable (stagger for steady sauce supply); the concentrated-flush +
   staggered/second-planting guidance is captured in prose. Reviewer may promote to full
   succession-scope if desired.
3. Deliberate, correct roma-vs-cherry contrasts remain in consumer prose (e.g. "unlike the cherry
   class", "differ from cherry tomatoes") -- these are intentional teaching comparisons, not
   un-refit leftovers.
4. Some general-tomato tips/notifications (blight, watering, hardening-off) are inherited nearly
   verbatim from cherry because the biology is identical across tomato types; refit only where the
   indeterminate/heat-resistant framing was type-specific.

## Gate result (self-verified: spliced into scratch canonical, gated to PASS)
- `whole_crop_gate.py roma-tomato`: **GATE: PASS** (all A2-A37 clean).
- **A37 (calendar-coherence): 0 violations** -- growing-after-harvest 0, harvest-hole 0. Nothing to
  report separately; the inherited calendars are A37-clean.
- `release_verify.py`: **clean, no blocking concerns** (2 non-blocking pre-existing `wait`-token
  pause-legibility notes on ca_north_coast.z10 / ca_south_coast.z10, inherited from cherry).
- `verbatim_scan.py`: no verbatim/copyright hits (fresh authoring + cherry's already-cleared prose;
  URLs simply not fetched offline).
- Dual-voice: 0 null siblings. Dash/temp: 0 user-facing hits. Sources: 0 uncatalogued / 0 non-T1.
- verification_status.status = **author_fresh_pilot**; launch_ready_core / launch_ready_seasoned =
  **false**; open_findings = [] (no launch blockers).
- Canonical `crops_data_final.json` untouched (SHA still matches LATEST.txt).
