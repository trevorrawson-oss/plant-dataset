# bell-pepper author-fresh pilot -- NOTES

**Crop:** Bell Pepper (Capsicum annuum, sweet pepper). Filled the existing SHELL.
**Modeled on:** certified cherry-tomato (warm_season_fruiting / frost_anchored) via the gate-clean
eggplant author-fresh pilot (same family, Solanaceae) as the structural skeleton. Every biological
value RE-DERIVED for bell pepper. Base canonical SHA: 8432195016415dfe12acb396c3a8493152315a41ceddd8e6bd108c6eb1a282e5.
**Status:** `verification_status.status = author_fresh_pilot`; launch_ready_core/seasoned = false.
**Output:** `bell_pepper_crop.json` (compact, no trailing newline). Canonical left READ-ONLY.

## Key refits vs the eggplant skeleton (biology re-derived, not copied)
- **Two-stage harvest (the signature pepper trait):** fruit picked GREEN and full-size, OR left on
  the plant to ripen to red/orange/yellow/purple (sweeter, +2-3 wk). Green picking keeps set going;
  coloring on the plant slows it. Cut with a short stem, do NOT pull (brittle branches).
- **Self-fertile / self-pollinating**; single plant sets fruit; small white flowers.
- **Transplant into WARM soil** (soil >=65 F, nights >=55-60 F), ~8 weeks indoors, germ 80-90 F.
- **MODERATE feeder** (5-10-10 at planting + calcium nitrate side-dress); excess nitrogen -> leafy,
  few fruit. (eggplant was a heavier feeder.)
- **Signature disorders:** BLOSSOM-END ROT (uneven moisture -> calcium-delivery failure; woven
  through soil/watering/fertilizer/container/failure_diagnostics) + SUNSCALD (exposed fruit).
- **Sets poorly in extreme heat** (blossom drop past ~90-95 F days with warm nights) -> a backed
  midsummer `heat_pause` + spring/fall split. This is a WIDER pause footprint than eggplant: 7 cells
  (se_gulf z8/z9, fl_peninsula z10/z11, ca_desert z9/z10, low_desert_az z9), vs eggplant's desert-only
  pause. Cooler/coastal/northern regions + NM/W-TX chile country (warm_arid, cool desert nights) run
  one continuous crop.
- **Pests re-derived:** aphids (mosaic-virus vectors), flea beetle, pepper maggot, hornworm, pepper
  weevil, European corn borer. (Dropped eggplant's Colorado potato beetle, lace bug, spider-mite focus.)
- **Diseases re-derived:** bacterial leaf spot, Phytophthora blight, anthracnose, mosaic & other
  viruses, southern blight. (Dropped verticillium/phomopsis/bacterial-wilt eggplant complex.)
- **pH 6.0-6.8** (tol 5.5-7.5); **spacing 18-24 in**; **DTM 60-90 from transplant**; freezes well
  raw without blanching (pepper-specific storage fact).
- Varieties re-derived to real bells: California Wonder, Big Bertha, King of the North (early/cold-set),
  Purple Beauty, Golden California Wonder, Redskin (container).

## Sourcing (existing catalog T1 only; all URLs verified live this session via WebFetch/WebSearch)
- umn_ext (Growing peppers), clemson_hgic (Pepper factsheet), umd_ext (Growing Peppers home garden),
  iastate_ext (Growing peppers home garden) -- core agronomy (pH, spacing, DTM, germ, harvest,
  blossom-end rot, blossom drop, sunscald, yield).
- ncsu_ext -- pests-of-pepper + peppers-diseases + anthracnose-of-pepper pages.
- uc_ipm -- Peppers IPM (CA pests/diseases/viruses). ucanr_ext -- UC MG planting calendar (CA cells).
- rutgers_njaes -- FS1330 pepper weevil.
- Regional window anchors: uga_c963 (SE), nmsu_ext + tamu_agrilife (warm_arid), uariz_ext_az1005
  (low desert), ufifas_ext + uf_ifas_vh021 (FL), uhawaii_ctahr (HI), uwi_hort (containers).
- 16 distinct source IDs cited; all catalogued + T1 (E gate: 0 uncatalogued / 0 non-T1). No fabricated
  IDs or placeholder URLs.

## Gate result (self-verified: spliced into a scratch canonical, READ-ONLY on the real one)
- **whole_crop_gate.py bell-pepper: GATE: PASS -- 0 violations** across every A-gate (A2-A37),
  dual-voice (B), dash/temp (C/D), source-tier (E), anchoring (F), flip-state (G).
- **A37 (calendar-coherence): 0 violations -- NO flagged lines to report.** The hot-region midsummer
  gaps are authored as biology-correct `heat_pause` tokens (pepper heat-driven blossom drop), which the
  A37 walk treats as walk-through, so every `growing` remains reachable / leads-to-harvest. This is a
  genuine pepper refit, not an A37 dodge: eggplant's FL midsummer gap was disease/pest driven (it used
  `growing`, which A37 flagged); pepper's gap IS heat, so `heat_pause` is the correct token. Because
  A37 is clean, the deterministic normalizer has nothing to resolve here.
- register_fill_gate: PASS. release_verify.py: clean, exit 0 (only 2 NON-blocking Step-5.5
  pause-legibility review notes on ca_north_coast.z10 / ca_south_coast.z10 winter cold_pause months).

## Flags / judgment calls (all in verification_status.open_findings, blocks_launch=false)
1. Per-zone planting/harvest windows MODELED from DTM + shared frost anchors + representative
   extension dates; not each source-verified against a live regional pepper calendar.
2. heat_pause footprint (7 cells, months [7,8]) + spring/fall split MODELED from the regional pattern;
   thermal basis (blossom drop) is sound. Wider than eggplant by design (pepper heat sensitivity).
3. DTM [60,90] is from-transplant (family convention); green ~60-70, colored ~75-90; from-seed adds
   the ~8 wk indoor start (carried in prose, not the numeric field).
4. ca_north_coast + northern_tier z3/z4 MARGINAL for pepper (cool summers); grown-but-modest, said so
   in region_notes.
5. Variety DTMs modeled from seed-catalog norms (from-transplant, green stage).
6. Some regional cells anchor to institution portals rather than a pepper-specific regional page.
7. Hawaii z11 window is a broad frost-free default (CTAHR sources are scanned PDFs, not WebFetch-able).
8. pH preferred_range [6.0,6.8] brackets Clemson 6.0-6.5 + UMN up-to-7.0; prose first range matches
   the structured range for A34.

## Handoff
Biology-complete and gate-clean. Queue for the daily biology-fidelity review + per-region
source-truth sample before any flip (author_fresh_pilot, not launch-ready).
