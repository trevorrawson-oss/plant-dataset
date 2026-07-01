# honeydew-melon -- author-fresh notes (Claude Code lane, 2026-06-30)

Slug **honeydew-melon** (Cucumis melo, Inodorus Group), `author_fresh_pilot`, launch flags false.
Full record: `scratchpad/honeydew_melon_crop.json` (standalone crop dict, compact JSON, 58 keys).
Built by deep-copying the **certified watermelon** record (key-parity with a GREEN
warm_season_fruiting / frost_anchored cucurbit, itself modeled on certified **zucchini-courgette**),
then RE-DERIVING every biological value for honeydew and rebuilding all 10 regions. Watermelon
supplied the single-harvest melon STRUCTURE; honeydew biology was refit throughout.

## Gate / verification (against a spliced scratch canonical; canonical READ-ONLY, SHA unchanged)
- `whole_crop_gate.py honeydew-melon <scratch>` -> **GATE: PASS (0)**. Every A-section 0: A2/A5/A24/
  A28 calendars clean, A31/A32 roster+presence, A33 numeric, A34 cross-consistency, A19/A26/A27
  companions, A20 display, A23 raw-display, A25 register-ruled, A29 register-fill, A35 laundering,
  A36 CP-required, dual-voice 0 null siblings, dash/temp 0, anchoring 42 leaves / 0 gaps, G 0 blockers.
- **A37 (calendar-coherence) = 0 -- CLEAN, no reported lines.** The two-window hot cells use the
  A37-clean normalized pattern: Florida spring+fall uses a `season_over` gap between crops (the crop
  is removed, not paused), and low-desert AZ runs a continuous back-to-back two-window (a `plant`
  token resets the second cycle), so no `growing`-after-harvest and no one-month harvest hole.
- `release_verify.py --slug honeydew-melon --base canonical --ref watermelon` -> **clean**: only
  honeydew-melon changed, watermelon byte-identical, catalog +none/-none, no NEW violations, all
  shell violations CLEARED, calendars coherent (no waits / no heat_pause), region_notes paired,
  no novel region keys vs the exemplar. One NON-blocking G note (see below).
- Canonical `crops_data_final.json` untouched: SHA still `8432195016415dfe...` (matches LATEST.txt).

## The two headline refits the task called for
1. **Non-slip ripeness cue (vs cantaloupe's clean full-slip).** Honeydew does NOT slip from the
   vine. Ripeness is authored as a LEARNED multi-cue judgment, not a clean release: the smooth rind
   pales from green to **creamy white or yellow**; the surface shifts from hard/slick to **waxy and
   slightly tacky**; the **blossom end softens slightly and gives a faint sweet aroma**; the ground
   spot pales to cream. Because it will not detach on its own, the record instructs **cutting** the
   fruit from the vine. This threads harvest_ready, description, growth_stages(harvest),
   tips_by_stage(harvest), notifications(harvest_ripeness), and failure_diagnostics(bland). Sourced:
   Iowa State honeydew FAQ ("do not slip off the vine when mature"; blossom-end softening) + Clemson
   HGIC 1304 ("honeydew will become paler in color" rather than slip). Flagged
   `honeydew_pilot_ripeness_nonslip_learned`.
2. **Longest / hottest season of the melons.** DTM **[85,100]** (mid 92) vs watermelon [70,95];
   plant only into warm soil >=70F. UMN states "watermelon and honeydew are more cold-sensitive than
   cantaloupe," so cool-summer / short-season cells (northern_tier z3-z5, ca_north_coast) are
   authored **UNSUITABLE-to-MARGINAL** (stronger than watermelon's "marginal"): earliest varieties
   (Earlidew), transplants, black plastic mulch, and honest region_notes that a poor summer may not
   finish. Cells kept (A31 roster floor) but flagged `honeydew_pilot_cool_summer_unsuitable_marginal`.

## Other honeydew-vs-watermelon REFITS (copy-don't-refit discipline)
- **Smooth rind (not netted), single harvest, does not sweeten off the vine.** `harvest_urgency`
  **low** (vs watermelon moderate) -- honeydew is the **best keeper** of the common melons: whole
  fruit stores **2 to 4 weeks at 45-50F** (Iowa State 2-3 wk), longer than cantaloupe/watermelon;
  no cure step.
- **Bacterial wilt added as a HEADLINE disease** (the melon-vs-watermelon signature). *Erwinia
  tracheiphila*, cucumber-beetle-vectored, melons highly susceptible, no cure. The cucumber-beetle
  PEST entry, seedling growth_stage/tip, a new `beetle_wilt_watch` notification, companions
  (nasturtium trap matters more here), rotation, and failure_diagnostics all refit around it. Sourced
  UMN/UMD/USU bacterial-wilt pages. **Fusarium wilt** refit to *F. oxysporum* f. sp. **melonis**
  (melon-specific, not watermelon's *niveum*).
- **Diseases (5):** Bacterial wilt, Fusarium wilt, Powdery mildew, Downy mildew, Gummy stem blight.
  **Pests (5):** Cucumber beetles (now wilt-vector-forward), Aphids (CMV), Spider mites, Squash bug,
  Squash vine borer (rarely attacks Cucumis melons).
- **NO seedless / triploid / pollinizer wrinkle.** Honeydew is andromonoecious, `self_fertile`=true,
  bee-pollinated; all watermelon triploid-pollinizer content removed and replaced with a plain
  bee-pollination story (pollinator_notes, varieties, start_method, flowering tips/notification,
  yield factors, diagnostics). Residual "seedless/pollinizer/watermelon" strings are intentional
  CONTRASTS ("no seedless honeydew to plan around", "needs no separate pollinizer, only bees").
- **Spacing in FEET, capped.** `spacing_inches` **[36,48]** (cap ~36-48 per the brief); true spacing
  (rows 6-8 ft, in-row 18-24 in, hills 4 ft; Clemson/USU) carried in prose. Flagged
  `honeydew_pilot_spacing_capped_48in`.
- **pH [6.0,6.8]** (tol 5.5-7.5); **npk 5-10-10** (lower-N, favor fruit/sugar; Clemson);
  sandy-loam / warm / well-drained soil; base watering with a taper-to-sweeten finish.
- **Varieties (5, no seedless):** Earlidew (~80d), Honey Dew/Green Flesh (~100d), Tam Dew (~100d),
  Orange Flesh/Honey Orange (~90d), Venus (~88d).
- **No heat_pause anywhere (0 tokens).** Honeydew, the most heat-loving melon, produces THROUGH
  desert/Southern summer; hot cells run continuous or a spring+late-summer split; FL midsummer gap is
  disease/rain-driven, rendered `season_over` (crop removed between windows). Flagged
  `honeydew_pilot_no_heat_pause_modeled`. No heat_pause => A28 no-op.
- Not a succession crop (`succession_policy.suitable`=false, `successions`=1; even less room for a
  second sowing than watermelon given the longer DTM). `successions_realized` absent (A8 out-of-scope).

## Calendars
Per-zone windows MODELED from DTM 85-100 + the shared crop-invariant frost anchors + representative
extension dates; harvest windows pushed ~2-4 weeks later than watermelon to reflect the longer, hotter
requirement. Flagged `honeydew_pilot_regional_calendars_modeled`. hawaii z11 is a broad frost-free
default (`honeydew_pilot_hawaii_window_modeled`, CTAHR PDF not parseable). **release_verify G note
(non-blocking):** 7 of 20 twelve-token month-arrays are byte-identical to watermelon
(northern z3, ca_north_coast z9, ca_desert z10, low_desert_az z9, fl z10, fl z11, hawaii z11).
Attested as **independently derived, not pasted**: two heat-loving cucurbits over the same 10 frost
regions legitimately converge at MONTH granularity, and all 7 carry DIFFERENT display dates
(honeydew's harvest strings run later). The coarse token strip coincides; the biology and dates do not.

## Sources (EXISTING catalog ids only, all 15 T1 university_extension; 0 uncatalogued, 0 non-T1)
clemson_hgic, iastate_ext, ncsu_ext, nmsu_ext, tamu_agrilife, ucanr_ext, uc_mg, uariz_ext, ufifas_ext,
uf_ifas_vh021, uga_ext, uhawaii_ctahr, umd_ext, umn_ext, usu_ext. Anchored to honeydew/melon-specific
pages verified live via web this session (Clemson HGIC 1304 Cantaloupe & Honeydew Melons; Iowa State
honeydew harvest FAQ + melon how-to; UMN growing-melons + bacterial-wilt; USU honeydew/winter-melons +
bacterial-wilt; UMD growing-melons + striped-cucumber-beetles-and-bacterial-wilt; NCSU cucurbit
downy/powdery mildew; UGA B1179 Cantaloupe and Specialty Melons). No watermelon-specific URLs remain
(sources_summary rebuilt from the melon URLs). No new catalog ids added. Region planting-date sources
are anchored to their extension melon/landing pages, modeled and flagged (not per-zone source-verified).

## FLAGS (verification_status.open_findings -- all blocks_launch:false, modeled-and-honest)
1. `regional_calendars_modeled` -- per-zone windows modeled (DTM + frost anchors + representative dates).
2. `spacing_capped_48in` -- numeric spacing capped; true row/hill spacing in prose.
3. `cool_summer_unsuitable_marginal` -- northern z3-z5 + ca_north_coast honestly unsuitable-to-marginal
   (honeydew the most heat-demanding melon; more cold-sensitive than cantaloupe).
4. `ripeness_nonslip_learned` -- no clean slip; ripeness a learned multi-cue judgment; cut from vine.
5. `no_heat_pause_modeled` -- runs through the heat; FL summer gap is disease/rain -> season_over.
6. `hawaii_window_modeled` -- CTAHR source a scanned PDF; broad frost-free default.

## Status
`verification_status.status` = **author_fresh_pilot**, launch_ready_core/seasoned = **false**,
6 open_findings all `blocks_launch:false`. NOT launch-ready: pending the claude.ai biology-fidelity
review + per-zone calendar source-verification. Canonical never touched (READ-ONLY honored).
