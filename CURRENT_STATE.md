# plant -- Current State

**Last updated:** 2026-05-31 (**M15 lettuce arc in progress — NA-1 + NA-2 + NA-3a + NA-3b done; NA-3c next.** NA-3b authored the FIRST warm `regions{}` cell (`se_gulf`) end-to-end — the first real exercise of the region-primary shape. A subsequent **design session (2026-05-31, no dataset write, SHA unchanged `ec4f2b69...`) REVERSED NA-3b's "anchor-phrasing only / no editorial region axis" decision** for tips — see the REVERSAL banner immediately below. Canonical SHA remains `ec4f2b69...` (M15 NA-3b). See "What happened 2026-05-31 (M15 lettuce NA-3b)" and the design-session entry next.)

> ## ⚠️ REVERSAL 2026-05-31 (design session — region-tip overrides) — READ BEFORE THE NA-3b ENTRY
>
> A design session on 2026-05-31 (chat-only, **no dataset write; SHA unchanged at `ec4f2b69...`**) reversed the NA-3b regional-content conclusion **for editorial tips**. Several NA-3b/NA-3c entries below still carry the superseded "anchor-phrasing only / NOT a tagging pass / no region tag fields" language; this banner governs on conflict.
>
> **What reversed:** NA-3b concluded editorial timing tips get **anchor-phrasing in prose only, no region axis** ("not a tagging pass"). Trevor was not comfortable with that and revisited it. **New decision (Trevor-ratified, 2026-05-31):** where ≥2 T1 sources from different **regions** (or **zone-bands**, in the north) the crop is actually grown in prescribe a **materially different grower action** for a tip, a **dual-register region-tip override** is authored on the relevant region cell(s).
>
> **What is RETAINED (NA-3b was right about this):** the **anchor-phrased portable tip remains the default** and the permanent **no-ZIP / pre-app fallback**. The override is an enhancement layered on top, authored only where sources fork; the default stands everywhere they don't. **Tips only** — pests stay FLAT and `sunlight` stays one region-neutral string (both NA-3b conclusions unchanged).
>
> **Timing:** overrides are **authored in-arc** (a rider on checklist Step 4, evidence-driven from sources already in hand — NOT a pre-computed bucket grid; bucket counts emergent and provisional, n=1), but **served post-app** (they require the ZIP→region resolver). Authoring in-arc is the cheapest moment, consistent with authoring region calendars ahead of the Phase C flip. Added as a served component of the post-app location-aware layer.
>
> **Schema:** a small **additive** field on the already-live region container (sibling to `region_notes`, dual-register). No new axis, no mass migration, nothing pre-populated; non-forking crops/tips change zero. Exact leaf-keys pinned at the **NA-3c ground-truth check** and registered in checklist Appendix A then (until registered, an unruled override field trips Appendix A's "unruled field is a finding" safeguard).
>
> **Durability:** the criterion is now in **checklist v1.4 Step 4** (principle-level, not a bucket count, so warm-season anchors that fork differently than lettuce still satisfy it), with an **Appendix A ruling** classing overrides CORE-PROSE-NEEDS-SIBLING — which makes Steps 6/8/9 (depth-lift, beginner siblings, dash resolution) cover overrides automatically. Because the checklist becomes the pipeline's `spec.md`/`rubric.md`, all 9 anchors + the ~114-crop pipeline inherit it; no separate rubric edit.
>
> **Standard doc:** `tip_region_authoring_standard_v1_1.md` (supersedes v1.0). **Provisional pending validation against crops 2–3** (cherry/beefsteak warm-season anchors may fork differently than cool-season lettuce). **Northern zone-band keying** is deferred to the first cold-zone tip fork (NA-3c is CA / `region_id`-keyed and does not need it).

**This file is the entry point. Read it first.**

**Promotion status (read before continuing M15):** canonical SHA is `ec4f2b6968b79b4505b0e7ec165a0a08acc38e6684a04721a78696c8210ee596` (M15 NA-3b). NA-3c's preflight expects `LATEST.txt` == `ec4f2b69...`. If it still reads `a2f2a3df...`, the M15 NA-3b bundle (`Phase 3 Lettuce M15 NA-3b Deliverables.zip`) has not been promoted — promote it first. **Project knowledge:** the NA-3b findings doc (`phase_3_lettuce_m15_na3b_findings.md`) should be added. `cold_zone_fall_heat_floor_methodology_v1_5.md` (methodology v1.5), **checklist v1.4** (supersedes v1.3 — adds the Step 4 region-tip-override criterion + Appendix A ruling), **`tip_region_authoring_standard_v1_1.md`** (region-tip-override standard, supersedes v1.0), `schema_2_8_calendar_model_addendum.md`, `calendar_model_schema_spec_v1_0.md`, `region_primary_schema_shape_spec_v1_0.md` should all be present.

---

## ⚠️ LOCKED DECISION 2026-05-31 — lettuce authors into `regions{}` this arc (OVERRIDES the original M15 kickoff AND the 4c layer choice for lettuce)

**This is the single most important thing for any M15 sub-session to know. It reverses an inherited framing; read it before the historical entries below, several of which now contain superseded "authors on zones[]" language.**

**The decision (Trevor, 2026-05-31, after extended back-and-forth):**
> **Lettuce authors its warm-region data INTO `regions{}` during the M15 arc, per checklist Step 4 as written.** The original M15 kickoff fenced off `regions{}` ("author on the live `zones[]` layer; Phase C carries lettuce's data across later"), echoing the 4c layer-placement decision. **That fence is overridden for lettuce.**

**Why (the reasoning that settled it):**
1. **The checklist is the artifact under test.** Checklist v1.3 is what stress-tests all nine arcs and then becomes the pipeline's `spec.md`/`rubric.md`. Step 4's completion criterion is "every warm region the crop is grown in carries a populated region-constant `plantings[]` rule set ... no PENDING in a grown region." If lettuce runs against a kickoff that fences off Step 4, lettuce isn't testing the checklist — it's testing a modified process nothing downstream uses. The canary doesn't test the thing.
2. **The region-primary schema otherwise gets ZERO exercise across all three test crops.** If lettuce (and cherry/beefsteak) never write into `regions{}`, the region-primary shape — the most structurally novel piece — reaches the Phase C global flip completely untested. That inverts the safety the gating was supposed to provide.
3. **Low risk to do it now: no live consumers read the dataset yet** (established repeatedly in prior sessions). A wrong region shape is a data-rewrite, not a coordinated break across an app. The 4c "don't author into PENDING containers ahead of the gated flip" worry is real but weak for lettuce specifically — lettuce has no legacy stranding (it's authored after the region layer exists), so there's no technical blocker.

**The two guardrails that ride with it:**
- **Keep `zones{}` coherent alongside `regions{}`** through M15 + M16 — a complete fallback while region-primary is on trial. Author region cells AND keep the zone cells they resolve into consistent (checklist Step 5.5 sync invariant covers this).
- **The formal Phase C "region becomes primary" FLIP still waits until cherry + beefsteak prove out at M16.** We *populate* region cells now; we do NOT flip the primary read-layer now. (Distinction matters: "populate now, flip after the three prove out" ≠ "flip now.")

**Provenance note (so trust calibration is accurate):** the original deferral was an inherited framing from the kickoff + 4c, not a fresh on-the-merits decision. It conflicted with checklist Step 4, and that conflict was not flagged when the arc opened — it surfaced only after Trevor pushed three times. The lesson logged: an inherited decision can silently contradict the governing checklist; check the checklist against the kickoff at arc open.

**Consequence for cherry/beefsteak (M16):** their warm data IS legacy-stranded in `zones["9"/"10"]` (authored before the region layer), so for them Step 4 is a genuine retrofit (move data OUT of zones, INTO regions). That part is unchanged. The M16 regression test still rediscovers the Appendix C findings and performs that retrofit.

---

## What happened 2026-05-31 (M15 lettuce NA-3b) (MOST RECENT — read first after the locked decision)

**NA-3b — first warm `regions{}` cell authored: `se_gulf` (zones 8, 9). Dataset write. SHA `a2f2a3df...` → `ec4f2b69...`.** First real exercise of the region-primary shape (the spec was previously validated only against a hand-written placeholder, cherry §7). Doc: `phase_3_lettuce_m15_na3b_findings.md` + `m15_na3b_se_gulf_verification_log.md`.

- **Scope decision (in-session, Trevor-ratified): one cell fully, then re-scope — NOT all 9.** NA-3b proved the shape on one fully-verified cell rather than pushing 9 at uncertain confidence (the cluster-13 false-confidence lesson). `se_gulf` chosen as the proof: the only warm cell already partly grounded (zone 8 = `sourced`, not `re-verify`), it is where the existing SE-sourced `zones{}` data actually belongs (so authoring it satisfies the orphaned-prose half of Step 4), and it exercises every mechanic (two-zone span, inverted calendar, heat pause, resolved_by_zone).
- **`se_gulf` authored end-to-end:** region-constant `plantings[]` (single `main`, **heat-anchored** — fall `from: bolt_threshold_end`, spring `from: soil_temp_40f`), `resolved_by_zone[8]`/`[9]` materialized from the existing T1-verified zone calendars (value-preservation gate: resolved dates == zone calendars, no re-derivation), per-zone `heat_pause` block (z8 [5,6,7,8] / z9 [6,7,8]), dual-register `region_notes_beginner`/`_seasoned`, `plantings_provenance`. Mirrors the `northern_tier` region shape exactly. Stale `sources_pending_admission` flag cleared (uga_ext + ufifas_ext already admitted T1).
- **Succession shape = mirror `northern_tier`, NOT a new region-succession arm.** `northern_tier` carries succession via `succession_policy` + resolved-cell notes, with NO separate region-level `sowings[]` arms. se_gulf mirrors this. Consequence: the NA-3a `sowings[]` date-array shape was NOT exercised at region level this session — the three NA-3a ratification flags remain ratified-as-working, untested against warm succession arms.
- **NEW PRECEDENT (`m15_na3b_finding_002`, ratification-pending): warm-region anchoring is HEAT-primary, frost-secondary** — the inverse of the cold-zone frost-primary/heat-floor-edge rule. Origin: Trevor's in-session observation "isn't it both?" — yes, asymmetrically (heat governs both season boundaries; frost a secondary cool-end modifier). Grounded in 2× UGA (B577 + C963, agreeing exactly: leaf lettuce spring Jan 15–Mar 1, fall Sep 1–Oct 1, DTM 60–85) + UF/IFAS corroboration (season Sep→Apr/May, peak Jan–Feb). **Becomes the warm-region rule for the remaining 8 regions + the pipeline. RATIFY before authoring the next warm cell.**
- **Regional-content design thread (extended in-chat; STRUCTURAL ANALYSIS, not all T1-verified — captured in the findings doc):** worked through whether tips/sunlight/pests need a region axis. Outcome: **(1)** pests/diseases stay FLAT (crop-specific; only `severity` is region-correlated and flat-is-not-wrong; deferred to runtime location layer); **(2)** ~~editorial timing tips adopt **anchor-phrasing in prose** ... instead of "your growing window" — NO schema change~~ **— ⚠️ REVERSED 2026-05-31 (see top REVERSAL banner): anchor-phrasing is RETAINED as the default/fallback, but region-tip OVERRIDES are now authored in-arc where T1 sources fork the grower action. Tips ride an additive region-container field; checklist v1.4 Step 4 owns the criterion**; **(3)** sunlight = one region-neutral string naming the warm/cool flip, NO axis (unchanged); **(4)** the **community-tip location axis is a CONFIRMED post-app forward item** — justified by community contribution (contributor location is captured metadata, not phrasing; stamp zone always + region when present; the always-on zone stamp dissolves the `northern_tier` coarseness problem without splitting it). Bundled with ZIP→region resolution + severity-by-location + region-tip-override serving as ONE post-app location-aware layer. None is dataset work now.
- **Carried action into NA-3c:** rewrite `succession_policy.tip_beginner`/`tip_seasoned` as anchor-phrased portable defaults (draft in findings doc); optionally tighten the flat `sunlight` string. **PLUS (2026-05-31 reversal): capture region-tip overrides in-arc** — for each editorial tip, check the CA T1 sources read in Step 4 for divergent grower actions across CA regions and author a dual-register override on each cell where they diverge; keep the anchor-phrased default where they agree. **First run the NA-3c ground-truth check** (where `tips_by_stage` / `succession_policy.tip_*` actually sit in the live structure) to pin the override leaf-keys, then register them in checklist Appendix A at NA-3c close. This is NO LONGER "not a tagging pass" — overrides ARE region-keyed fields, per checklist v1.4 Step 4. (Anchor-phrased defaults remain; overrides are additive on top, served post-app.)
- **Integrity:** start-SHA gate (`a2f2a3df`); dry-run on throwaway; collateral hash audit (122 other crops + all top-level keys byte-identical; within lettuce only `regions.se_gulf` changed); value-preservation (resolved dates == zone calendars); minified; independent post-write re-verify. Clean, all gates.

**Running gate-status (checklist v1.3, lettuce):** Step 0 ✅; Step 1 ✅; Step 2 ✅; Steps 3 → NB; **Step 4 IN PROGRESS — 1 of 9 warm regions done (`se_gulf`); 8 remain** (CA batch recommended next as NA-3c); Step 5 cold-zone succession ✅ + se_gulf windows ✅, remainder → NA-3c/NB; Step 5.5 PASS on binding gates; Steps 6–11 not started. **30 open findings + 2 NA-3b findings (001 zone-sourcing reconcile, 002 heat-anchoring ratification), 0 unresolved blockers** (two-field predicate; + finding 003 deferred non-blocking).

**NA-3c (next) scope:** the 4 California `regions{}` cells (`ca_interior`, `ca_north_coast`, `ca_south_coast`, `ca_desert`), single-source (UC ANR). Mirror the se_gulf shape. **First: ratify `m15_na3b_finding_002`** (heat-anchoring), and NA-3c is the explicit test of whether UC ANR frames CA's seasons the same way UGA did. Biological wrinkle to verify: coastal CA grows lettuce near year-round (little/no `heat_pause`) while interior/desert invert like se_gulf — do NOT copy se_gulf's pause months blindly. Plus the carried tip-rewrite action above **and the new region-tip-override rider (2026-05-31 reversal): run the ground-truth check on tip field placement first, capture overrides where CA sources fork the grower action, register the override leaf-keys in checklist Appendix A at close.** **NA-3c start-SHA = `ec4f2b69...`.** Then: fl_peninsula (UF/IFAS, cheap after CA), desert/arid (AZ1005 / NMSU 457), hawaii_tropical (UH CTAHR, most divergent — last).

---

## What happened 2026-05-31 (M15 lettuce NA-3a)

**NA-3a — cold/temperate succession authoring (zones 3–7) + `succession_policy` re-grounding. Dataset write. SHA `566b45ed...` → `a2f2a3df...`.** First `track:"succession"` windows in the dataset; first real exercise of checklist Step 5.5's coherence gates. Doc: `phase_3_lettuce_m15_na3a_findings.md`.

- **`succession_policy` re-grounded on verified cadence (Step 2 gap closed).** The unsourced `successions: 6` / `max_successions_per_season: 6` cap was BOTH unsourced AND an undercount — T1 sources (USU, UMN, UMD, UF/IFAS) frame lettuce succession as *interval (2 wk) across a plantable window, paused in summer heat*, never a fixed count. Removed the cap; added `count_basis: "derived_per_zone"` + `derived_zone_totals_cold` ({3:9,4:9,5:8,6:10,7:7}) + `count_note`; added `sources` (usu/umn/umd) + verified `anchoring_urls`; authored `tip_beginner` (was null). First arc to exercise methodology v1.5 **Clause C** (per-arm count ≠ season cap) — confirmed: season total is a derived per-zone calendar fact.
- **Cold-zone `track:"succession"` windows authored** (zones 3–7, 43 sowings total). Shape: one entry per ARM (spring, fall), dates enumerated in a `sowings[]` array (date-level enumerate-each — readable + light for the UI). Spring arm `soil_temp_40f` → bolt-driven close capped at fall-arm start (no overlap); fall arm heat-floored `first_frost` offset (z3 = −76/~Jul 1 per Clause A; z4–7 = −90). Each window T1-verified side-by-side (status does NOT inherit). Beginner (main) entries left byte-identical.
- **Two-calendar model confirmed + safe-sowing NOTE pattern established.** `track:"beginner"` = MAIN planting calendar (T1 source windows, beginner-facing, simple); `track:"succession"` = every-2-weeks detail (seasoned depth — too much for a first-season grower as the default). "Safest planting dates" are a NOTE on the main calendar (`safe_sowing_note` + `_beginner`, dual-register) that NAMES forgiving real sowings — NOT a separate window. This dissolves coherence drift at the root (a note can't fall outside the succession envelope).
- **Fall-arm maturity corrected (finding 002, resolved).** Mid-session the Step 5.5 coherence gate fired; chasing it corrected the fall-arm rule to **baby-leaf 30d, light-frost-tolerant** (latest sow = first_frost − 30d, no extra margin) — verified against Cornell MG / UMD / UMN. The over-conservative −5d margin (treated lettuce as frost-intolerant) and a 60d head-maturity reading were both wrong. The gate did its job: caught a biology error prose-screening would miss.
- **Deferred finding (003, non-blocking, → NB):** z4/z5 beginner fall window late-edge runs ~7d past the last viable baby-leaf succession sow (pre-existing M13 anchor over-extension). Main windows left byte-identical this session; NB bounds them.
- **⚠️ THREE ratification flags for Trevor (NA-3a findings §3 — do NOT treat as settled):** (1) the `sowings[]` date-array encoding as the canonical succession shape; (2) the beginner↔succession coherence reformulation (note-dates-are-real-sowings + beginner-start ≥ succession-start, with beginner late-edge as a finding not a hard gate); (3) `succession_policy` count semantics (derived-per-zone, no integer cap). These become precedent for all nine arcs + the pipeline spec.
- **Integrity:** start-SHA gate; collateral hash audit (122 other crops + 13 top-keys + 52 lettuce sub-objects byte-identical; beginner entries + warm zones byte-identical; only `succession_policy` + zones[3-7]{plantings + 2 note keys} changed); minified; independent post-write re-verify (PASS, all binding gates).

**Running gate-status (checklist v1.3, lettuce):** Step 0 ✅; Step 1 ✅; **Step 2 ✅✅ (succession_policy gap closed)**; Steps 3 → NB; **Step 4 → NA-3b**; Step 5 cold-zone succession ✅, remainder → NA-3b/NB; **Step 5.5 PASS on binding gates (first real exercise — 43 sowings, no drift, no overlap, z3 heat floor)**; Steps 6–11 not started. **30 open findings, 0 unresolved blockers** (+ finding 003 deferred non-blocking).

**NA-3b (next) scope — unchanged:** warm-region fills + region succession (the region-schema test, per the locked decision). Populate the 9 warm `regions{}` cells per Step 4; first move = verify grown-vs-not per region; source each from its region-appropriate T1 anchor (re-verify/locate cells need side-by-side, don't inherit); author region succession reusing the `sowings[]` shape; classify summer `heat_pause` per region via the heat-pause path (NOT Clause A). Keep warm `zones{}` coherent. **NA-3b start-SHA = `a2f2a3df...`.** *(RESOLVED — NA-3b done; see the NA-3b entry at the top. It authored 1 of the 9 cells (`se_gulf`) as a proof-of-shape and re-scoped the remaining 8; region succession was carried via `succession_policy` mirroring `northern_tier`, not a separate `sowings[]` arm.)*

---

## What happened 2026-05-31 (M15 lettuce NA-1 + NA-2) (read this FIRST after the locked decision — most recent)

**M15 lettuce arc opened. Preflight clean against `518a6a36...`.** The arc is large and split into sub-sessions (NA scaffolding/authoring → NB verification grind + depth-lift → NC siblings + dashes → ND validation/flip). NA itself split: **NA-1** (methodology, no write), **NA-2** (Step 1 + Step 2, write), **NA-3** (succession + region authoring — next).

**NA-1 — methodology v1.5 ratified (markdown only, no dataset write).** The cold-zone fall heat-floor rule, pulled forward from its post-lettuce slot (Trevor option B) so the canonical first succession crop authors against a ratified rule. **The rule:** a fall cool-season sow is clamped to `max(first_frost − 90, ~Jul 1)` — never scheduled into the >80°F summer-heat germination-failure window (thermoinhibition). **T1 basis:** USU Extension (soil >80°F → lettuce/spinach seed dormant; lettuce-specific fact sheet), corroborated by NC State + MSU; mechanism from two peer-reviewed journals (ABA/GA). **Threshold corrected 85°F → 80°F** (the 85°F figure was T2 seed-company/blog; 80°F is T1 and more conservative). **For lettuce the floor binds in exactly ONE zone — zone 3** (already at `first_frost−76` = Jul 1 from M13). Three clauses: (A) heat floor; (B) fast-maturity assumption for compressed windows; (C) **per-arm succession count ≠ season-wide `successions` cap** — a cross-arc PATTERN decision (all nine arcs inherit it: a 3–4-week cold-zone fall arm supports 1–2 sowings, not the season's 6). **Resolves finding `m13_s1b_nc_methodology_candidate_001`.** Generalizes to spinach/radish/cilantro — mechanism inherits; threshold + source re-verified per crop (radish/cilantro are bolt/quality floors, not germination floors). Scaling path logged (not built): a per-zone USCRN soil-80°F-crossing anchor replacing the uniform ~Jul 1 floor. Doc: `cold_zone_fall_heat_floor_methodology_v1_5.md`.

**NA-2 — Step 1 + Step 2 (dataset write). SHA `518a6a36...` → `566b45ed...`.**
- **Step 1: `source_set` populated** — was empty; now 35 catalog IDs, derived by a live walk of every `sources` array + `anchoring_urls` key on lettuce (0 orphans). Matches the cherry/beefsteak precedent that `source_set` is the full draw-on set, not the per-arc-verified subset. Inheritance assertion held (M13 records are candidate input; only Step 5 side-by-side confers verified status).
- **Step 2: v1.4.1 extreme-zone check recorded** — checked the fall direct_sow anchor at the coldest zones against the heat floor. **PASS, no correction needed:** zone 3 already floored to `first_frost−76`; zones 4–7 use `−90` and clear the floor; warm zones use the heat_pause path (NA-3). Recorded as `verification_status.extreme_zone_check`.
- **Structured surfaces confirmed launch-ready-core quality (read live):** `soil` (dual `_core`/`_seasoned` vocab, 4 T1 + anchoring URLs, both registers authored); `ph` ([6.0,6.8] preferred / [6.0,7.0] tolerated — wraps correctly; equal lower bound intentional per `s1c_finding_003`; 4 T1; both registers). The remaining Step-2 per-surface gating (`succession_policy`, `container_notes`, `plantings[0]` T1-floor) folds into NA-3 since succession authoring touches `plantings[]` directly. **`succession_policy` currently has NO `sources`/`anchoring_urls` — a Step 2 gate gap to fix when authoring succession in NA-3.**
- **Integrity:** start-SHA gate; collateral hash audit (every crop except lettuce + every top-level key byte-identical; within lettuce only `verification_status` changed: `source_set` + `extreme_zone_check` + `verification_log_ref`); minified; independent post-write re-verify. Clean.

**Running gate-status (checklist v1.3, against lettuce):** Step 0 ✅; Step 1 ✅ (source_set=35); Step 2 ✅ (soil/ph confirmed, extreme-zone PASS; remainder → NA-3); Steps 3–11 not started. **30 open findings, 0 unresolved blockers** (two-field predicate). NA-1 resolves the methodology candidate. No checklist friction so far (Step 5.5's real test is NA-3).

**NA-3 (next sub-session) scope — two halves:**
- **NA-3a — cold/temperate succession (zones 3–7; `northern_tier` region already populated).** Author `track: "succession"` windows (shape (a) enumerate-each, 2-wk interval, per-arm counts per Clause C, fall arm clamped per the heat-floor rule). Add `succession_policy.sources` + anchoring URLs. Verify each window per T1 (Step 5). Assert beginner↔succession coherence + calendar↔plantings sync.
- **NA-3b — warm-region fills + region succession (the region-schema test, per the locked decision).** Populate the 9 warm `regions{}` cells per Step 4 (each grown region: verified region-constant `plantings[]` from its region-appropriate T1 anchor — `se_gulf`→uga/ufifas, `ca_*`→ucanr, `warm_arid`→nmsu/tamu, `low_desert_az`→uariz, `fl_peninsula`→ufifas, `hawaii_tropical`→uhawaii_ctahr). Author region-level succession; classify summer `heat_pause` per region (biological claim, verify per T1); keep warm `zones{}` coherent. **First move: verify grown-vs-not per warm region** — "not grown here" is a legitimate Step 4 outcome, not a gap.
- **Recommended order: 3a first** (prove the succession-encoding shape on already-clean ground, then carry it into the warm-region complexity). Split further if heavy. **NA-3 start-SHA = `566b45ed...`.**

**Warm-zone authoring note (lettuce-specific biology, on record):** zones 9–11 are inverted (fall/winter/spring growing, summer shut). Existing zone-9 beginner anchors already use per-window maturity offsets (60d fall / 45d winter) reflecting slower cool-season growth (UMN T1 principle) — succession windows inherit this, NOT a flat 38-day maturity. UF/IFAS confirms warm-zone lettuce is an Oct–Feb crop. The Jun/Jul/Aug interior `wait` months are the `heat_pause` reclassification target.

---

## What happened 2026-05-31 (4d checklist v1.3) (kept for context)

**Markdown-only session. No dataset write.** Finalized gold-standard arc checklist **v1.3**, converting Step 5.5's three schema-pending criteria into real, enforceable gates now that 4c built the fields they were waiting on. Verified against the live post-4c dataset before writing (981 `plantings[]` entries all carry `track`; 123 crops all carry `calendar_basis` as 109 frost_anchored / 13 non_seasonal_indoor / 1 generic_placeholder; the 3 pause states defined-and-reserved, populated zero times; zero validator violations).

**What changed v1.2 → v1.3 (Step 5.5 only; rest of checklist untouched):**
- **The gate now branches by `calendar_basis` first.** `frost_anchored` (109) → full calendar/succession/track/pause criteria, `plantings[]` must be populated. `non_seasonal_indoor` (13) → `plantings[]` legitimately empty, cyclic `calendar[]` is source of truth, track/succession/sync criteria N/A, frost-resolution suppressed. `generic_placeholder` (1, heirloom-tomato) → calendar/succession criteria N/A until varietal split; gold-standard not claimed in generic form.
- **Beginner↔succession coherence is now a real gate** — the relationship v1.2 could not check because only one track existed. With `track`, it gates: where both tracks exist, the beginner window sits within the succession envelope (never shows a plantable month succession lacks). Single-track crops pass trivially.
- **`track`-valid + exactly-one-beginner-per-zone** gates added (all 981 entries currently `track: "beginner"` — correct pre-arc state).
- **Succession-encoding gate** now checks for `track: "succession"` entries specifically (49 `suitable: true` crops must author them at gold-standard; currently zero have — the legitimate pre-arc state).
- **Pause legibility** sharpened from "explain in a findings note" (v1.2 interim) to "must be a specific `cold_pause`/`heat_pause`/`season_over` state" (the real 4c vocabulary), classified per-month Step-5-style.
- **`calendar[]` 13-state enum** validity gate added.

**Open reconciliation note (carried, not blocking):** the beginner↔succession coherence criterion as written uses the "beginner window sits within the succession envelope" formulation. **NA-3 is the place to confirm this matches `calendar_model_schema_spec_v1_0.md` §2a** (the spec governs on conflict) — it becomes a live gate the moment lettuce authors its succession track. (Spec §2a does state "the beginner window sits within the succession envelope," so they appear aligned; confirm at NA-3a.)

**Project-knowledge action:** remove checklist v1.2, add v1.3 (one checklist version at a time).

---

## What happened 2026-05-31 (4c calendar-model schema) (kept for context)

**Dataset mutation session (design + scaffold). SHA `f6b2d800...` → `518a6a36...`. Schema 2.8 unchanged.** Built the calendar model whole — the structure lettuce (M15) and every later crop needs — scaffolded but NOT populated. Authoritative spec: `calendar_model_schema_spec_v1_0.md`.

**⚠️ Note on the 4c layer-placement decision:** 4c decided `track`/`calendar_basis` land on the `zones[]` layer and `regions{}` stays untouched, with the reasoning that M15 lettuce would author on `zones[]` and Phase C would carry data across. **For the `track`/`calendar_basis` SCAFFOLD fields, that placement stands** (they live on `zones[]` and migrate at the flip). **But the broader implication 4c drew — that lettuce authors its warm DATA on `zones[]` only and defers region population to Phase C — is OVERRIDDEN by the 2026-05-31 locked decision above** (lettuce populates `regions{}` this arc per checklist Step 4). The scaffold-field placement and the data-authoring layer are separable; only the latter changed.

**What the apply did (scaffold, not populate):**
- **`track` added to 981 `plantings[]` entries**, all re-tagged `track: "beginner"`. **Zero `succession`/`second_planting` entries authored.**
- **`calendar_basis` added to all 123 crops:** 109 `frost_anchored`, 13 `non_seasonal_indoor`, 1 `generic_placeholder` (`heirloom-tomato`).
- **Relaxed validator:** `plantings` length ≥ 1 UNLESS `calendar_basis ∈ {non_seasonal_indoor, generic_placeholder}`.
- **`calendar[]` vocabulary extended** 10 → 13 (`+cold_pause`/`+heat_pause`/`+season_over`). The 3 new states appear **ZERO times** — reserved, not populated.
- **Non-seasonal indoor mode defined; sync invariant defined.**
- **Zero calendar months reclassified. Zero prose authored. Zero succession windows authored.**

**Drift FLAGGED for owning arcs (NOT fixed):** cherry-tomato zone-9 `calendar[]` shows continuous harvest Apr–Jul with no pause, though its `notes` prose claims a mid-summer heat pause. **Owning arc: M16** (overlaps Appendix C `gs_exemplar_finding_001`). The 34 interior `wait` months dataset-wide are the prime reclassification candidates.

**Phase C coordination outcome:** composes, does not collide. `track` migrates with each `plantings[]` entry at the flip; `calendar_basis` is crop-level/region-independent; the 3 new `calendar[]` states apply identically to `regions[r].resolved_by_zone[z].calendar[]`.

**Spec docs (into project knowledge):** `calendar_model_schema_spec_v1_0.md` (authoritative), `schema_2_8_calendar_model_addendum.md`.

---

## What happened 2026-05-31 (Calendar/succession planning) (kept for context)

**Markdown-only planning session.** Surfaced + scoped the calendar/succession work. Five decisions carried into checklist v1.2 + finding docs:
1. **Checklist v1.1 → v1.2: added Step 5.5 "Planting + succession calendars are true and make sense."** Previously UNOWNED.
2. **Succession-encoding shape LOCKED: shape (a) enumerate-each-window + a `track` field** (`beginner`/`succession`/`second_planting`). *(Implemented in 4c.)*
3. **Succession deep dive:** `succession_policy` (cadence) + `plantings[]` (windows) is sound; multi-window was DELIBERATELY deferred to lettuce. The 49 suitable-but-one-window crops are the deferral as data.
4. **Empty `plantings[]` = THREE legitimate meanings → `calendar_basis` reason field** + relaxed validator. *(Implemented in 4c.)*
5. **CALENDAR-MODEL SCHEMA SESSION inserted before M15.** *(That session is 4c — DONE.)*
Standing principle adopted: **absence always carries a reason field; the gate checks the reason exists, not that the slot is filled.** Finding docs: `succession_schema_2_7_deep_dive_finding.md`, `calendar_track_structure_finding.md`.

---

## What happened 2026-05-31 (Companions reconciliation) (kept for context)

**Decision + dataset mutation. SHA `68ca19a8...` → `f6b2d800...`. Schema 2.8 unchanged.** The companions `_core`/`_seasoned` split reshaped to the **three-array register-by-membership model** (`*_beginner` / `*_beginner_seasoned` / `*_seasoned`; same triple for `bad`). 511 entries conserved; each `why` → `why_seasoned` (byte-identical), `why_beginner: null` scaffolded on both-modes entries. `launch_ready_*` flags + `cause_beginner` nulls deliberately untouched (M16). Cherry/beefsteak `why_beginner` is the one un-authored field on two otherwise-complete crops.

---

## What happened 2026-05-31 (Phase 0 Part 2) (kept for context)

**Dataset mutation. SHA `74fa36f0...` → `68ca19a8...`. Schema 2.7.5 → 2.8.** Renamed every register-bearing prose field to the symmetric `_seasoned`/`_beginner` shape, byte-preserving every value; CP fields got a `_beginner` sibling (kept or null-scaffolded); SP fields `_seasoned` only; all 3 anchors converted. 14,553 renames; all integrity audits passed.

**Structural notes carried forward:** `tips_by_stage` is a dict-of-stages, not a flat list (compound tooling must special-case it); `yield_expectations.factors` is list-valued prose; prose leaf-names recur outside the conversion surface (orphan-key checks must be path-scoped).

---

## What happened 2026-05-30 (Phase B + Phase A + region model) (kept for context)

- **Phase B — correction phase — COMPLETE.** Built the region→source map at top-level `region_source_map{}` (which T1 anchor serves which region/zone; build-time infra, NOT a runtime read). Catalog 76 → 80 (`ufifas_ext`, `nmsu_ext`, `uariz_ext`, `uhawaii_ctahr`, all T1). **Per-crop warm `sources` arrays NOT yet proven T1** — that is the gold-standard re-runs, claim-level verified via methodology v1.4 Step 4. **(M15 NA-3b is where lettuce makes its per-crop warm sourcing true, per the locked decision.)**
- **Phase A — region scaffolding (additive) — COMPLETE.** Added `regions{}` sibling to all 123 crops; identical 10-region menu. `northern_tier` REAL (cold-zone rule lifted verbatim, payload under `resolved_by_zone[z]`). Warm regions empty PENDING containers.
- **Region model LOCKED:** region-primary (region-beside-zone); 10 slugs ratified; two-layer cut; `lifecycle_override` REGION-scoped.

---

## What happened 2026-05-30 (checklist + register decision) (kept for context)

Gold-standard arc checklist authored → stress-tested twice → v1.1 → (later v1.2/v1.3). Auto-derived denominator (Appendix A) closes the lettuce incomplete-denominator failure mode permanently. EXPLICIT-REGISTER SCHEMA DECISION: symmetric `_seasoned`/`_beginner` suffixing. Key enabler: NO live consumers read the dataset yet, so the register rename + region flip are NOT reader-coordinated migrations. Forward path re-sequenced: Phase 0 → M15 lettuce → M16 cherry+beefsteak AS A REGRESSION TEST.

**The four cherry/beefsteak exemplar findings on record (Appendix C; for M16):** `gs_exemplar_finding_001` (UMN/Minnesota prose in the SE-sourced zone-9 cell, BOTH anchors), `_002` (16 user-facing `--` each), `_003` (extreme-zone offset computation not recorded), `_004` (no `cause_beginner`). *(4c added a fifth flag: cherry z9 calendar/prose heat-pause drift.)*

---

## Dataset

- **Canonical location:** `~/plant-dataset/crops_data_final.json`
- **Current SHA:** `ec4f2b6968b79b4505b0e7ec165a0a08acc38e6684a04721a78696c8210ee596` (M15 lettuce NA-3b, 2026-05-31). *If `LATEST.txt` still reads `a2f2a3df...`, the M15 NA-3b bundle is not yet promoted.*
- **SHA lineage (recent):** `518a6a36...` (4c end / 4d) → `566b45ed...` (M15 NA-2) → `a2f2a3df...` (M15 NA-3a) → `ec4f2b69...` (M15 NA-3b).
- **Schema version:** **2.8** on disk. Spans: register suffixing (Phase 0), companions register-by-membership, region scaffolding (Phase A/B, additive), calendar-model scaffolding (4c). The pending region-primary FLIP (Phase C) and perennial extension also claim "2.8" — version bookkeeping pinned per session.
- **Crop count:** 123
- **Zones:** USDA hardiness 3-11
- **Regions:** 10-region menu scaffolded per crop. `northern_tier` populated (zones 3–7) + **`se_gulf` populated (zones 8–9, NA-3b — the first warm region authored).** 8 warm regions still PENDING — lettuce continues populating them through M15 (CA batch next in NA-3c); all other crops' warm regions remain PENDING until their arcs.
- **Calendar model:** multi-track — `track` on every `plantings[]` entry (981 `beginner` + 10 `succession`, all lettuce cold-zone NA-3a; 0 second_planting); `calendar_basis` on every crop (109/13/1); `calendar[]` 13-state vocab (3 pause states — `heat_pause` now populated in lettuce `se_gulf` resolved cells, NA-3b; cold/season_over still reserved)
- **Region→source map:** top-level `region_source_map{}` (build-time infra, NOT a runtime read)
- **Source catalog:** 80 entries
- **Format:** minified JSON

## Methodology

- **v1.5** (2026-05-31, cold-zone fall heat-floor rule — `cold_zone_fall_heat_floor_methodology_v1_5.md`); v1.4.1 (patch 2026-05-26; base v1.4 locked 2026-05-19); dual-register v1.1; language/copy v1.1.

---

## Where we are in the work

- **M15 lettuce arc: IN PROGRESS.** NA-1 (methodology v1.5) + NA-2 (source_set + extreme-zone check) + NA-3a (cold-zone succession + succession_policy re-grounding) + **NA-3b (first warm region `se_gulf` authored + regional-content design thread settled)** done. **NA-3c next** (the 4 CA region cells + carried tip-rewrite). Then remaining warm regions (fl_peninsula, desert/arid, hawaii), then NB/NC/ND.
- **Gold-standard arc checklist:** **v1.3** (Step 5.5's calendar/succession criteria now real gates, branched by `calendar_basis`). M15 lettuce is the first proving ground; its succession + region authoring is the first real exercise of Steps 4 + 5.5.
- **Calendar model:** SCAFFOLDED WHOLE (4c). NOT populated — succession windows + pause-month classification are crop-arc work (lettuce first, in NA-3).
- **Explicit-register schema:** DONE (Phase 0). **Companions:** DONE (reconciliation).
- **No live consumers read the dataset yet.** This is why the region flip + register rename are not reader-coordinated — and the basis for authoring lettuce's region data now at low risk.
- **Region migration:** Phase A + Phase B COMPLETE. **Phase C (region-primary flip) BUILT-AND-READY but GATED** behind M15 lettuce + M16 cherry/beefsteak carrying real warm data. **Per the locked decision, lettuce now CARRIES that real warm data in `regions{}` by the end of M15** (the formal flip still waits for M16).
- **Cherry tomato (M6) + beefsteak (M7):** COMPLETE under the OLD gate; carry 4 known Appendix C defects + the 4c-flagged cherry z9 heat-pause drift → all re-discovered/cleared at the M16 regression test (which includes their zones→regions retrofit, since their warm data IS legacy-stranded).
- **Anchors: 2 of 9 done under the old gate** (cherry, beefsteak), both pending M16. Lettuce in progress. Strawberry = 9th anchor.

---

## FORWARD PATH (4c + 4d DONE; M15 lettuce IN PROGRESS)

Dependency-ordered.

1. **~~Phase A — region scaffolding.~~ DONE.** SHA `15da4a9c...`.
2. **~~Phase B — correction phase.~~ DONE.** SHA `74fa36f0...`.
3. **~~Gold-standard arc checklist (keystone).~~ DONE; v1.3** (Step 5.5 real gates).
4. **~~Phase 0 — register inventory + apply.~~ DONE.** Schema → 2.8. SHA `68ca19a8...`.
4b. **~~Companions reconciliation.~~ DONE.** SHA `f6b2d800...`.
4c. **~~CALENDAR-MODEL SCHEMA SESSION.~~ DONE.** SHA `f6b2d800...` → `518a6a36...`.
4d. **~~Checklist v1.3 finalization — markdown-only.~~ DONE.** SHA stays `518a6a36...`.

5. **M15 — Lettuce gold-standard arc. ← IN PROGRESS.** First crop to author `track: "succession"` windows; first real test of Step 5.5's succession + coherence gates AND (per the locked decision) Step 4's region-population gate; **first real exercise of the region-primary shape (NA-3b, `se_gulf`).** Authors succession on the `zones[]` layer AND populates lettuce's warm `regions{}` cells per checklist Step 4 (`zones{}` kept coherent as fallback). **NA-1 + NA-2 + NA-3a + NA-3b done (SHA `ec4f2b69...`); NA-3c next** (4 CA cells + carried anchor-phrasing tip rewrite). Catches lettuce's gaps (85 null beginner siblings [19 top/dict + 66 compound; tips 10/10 done], ~39 zones-layer content dashes [region-scaffold dashes resolved as region cells populate], depth-lift, warm-region authoring [1 of 9 done], the 30 outstanding findings). Flags flip only when every gate returns 0 AND every review flag cleared. **`status` left as `unverified`-or-successor — NOT `gold_standard`** until M16 settles the post-arc status vocabulary (Appendix B F6). Expect sub-sessions.

6. **M16 — Cherry + beefsteak re-run as a REGRESSION TEST (new-shape).** Pass bar: independently rediscover the 4 Appendix C defects + the 4c-flagged cherry z9 heat-pause drift. Corrects them → performs the warm-zone retrofit (real warm data OUT of legacy `zones{}`, INTO `regions{}`) — the precondition for the Phase C flip. Settles the post-arc `status` vocabulary (F6).

7. **Phase C — region-primary FLIP.** Unblocked once lettuce (5) + cherry & beefsteak (6) carry real warm data in the region layer. Region becomes primary; `zones{}` collapses to frost-refinement; region-scoped `lifecycle_override` lands; **PENDING guard.** Inherits 4c's `track` + pause vocab; `calendar_basis` rides at crop level. Re-pin start-SHA to post-step-6 canonical.

8. **Carrot gold-standard arc.** Completes the cool-season annual anchor pair. BEFORE the perennial extension. (Will reuse the succession-encoding shape M15 proves — different cadence, no warm-zone inversion, but same track/sibling/pause structure.)
9. **Schema-2.8 perennial extension.** Perennial field surfaces + region-scoped `lifecycle_override` if not shipped in Phase C. Before the first perennial anchor.
10. **Remaining anchors + builder/auditor pipeline.** Apple, lemon, blueberry, strawberry, oyster, zinnia/bee balm, basil; then the pipeline promotes ~114 crops.

**Honest framing:** correctly ordered AND a lot of work. Nine anchors (two as regression re-runs) + Phase C + a 114-crop pipeline. Delivery target Fall 2027 – Spring 2028, Kickstarter decoupled.

---

## Locked / done

- Schema 2.8 live (register suffixing + companions + additive region scaffolding + calendar-model scaffolding); **methodology v1.5**; language v1.1; soil_education + ph_education complete; M12 scripted pass complete.
- Region model: region-primary LOCKED; 10 region_ids ratified; `lifecycle_override` region-scoped; two-layer cut.
- **Region-authoring policy (2026-05-31): each crop populates its warm `regions{}` during its own gold-standard arc, per checklist Step 4 — NOT deferred to Phase C.** Lettuce first (M15 NA-3b). The Phase C flip relocates the primary read-layer; it does not author per-crop region biology.
- **Region-tip-override policy (2026-05-31 design session, Trevor-ratified — reverses NA-3b for tips):** editorial tips fork along the climate-signal axis (region in the warm/diverse south & west, zone-band in the north) ONLY where ≥2 T1 sources from different buckets prescribe a materially different grower action; the anchor-phrased portable tip is the retained default + no-ZIP/pre-app fallback. Authored in-arc (Step 4 rider), served post-app (resolver). Encoded in checklist v1.4 Step 4 + Appendix A; standard `tip_region_authoring_standard_v1_1.md`. Tips only (pests flat, sunlight region-neutral). Provisional pending crops 2–3; northern band-keying deferred to first cold-zone tip fork; a/b is a calendar-date axis and never a tip-forking axis. SHA unchanged by this session (`ec4f2b69...`).
- Calendar model (4c): `track` on all plantings entries; `calendar_basis` on all crops; relaxed validator; 13-state `calendar[]` vocab (pause states reserved); non-seasonal indoor mode; sync invariant defined.
- Methodology v1.5 cold-zone fall heat-floor rule: ratified, T1-backed (USU 80°F); resolves `m13_s1b_nc_methodology_candidate_001`; generalizes to spinach/radish/cilantro (per-crop threshold re-verification).
- Lettuce: 9 zones verified (M13); soil 12/12; ph preferred [6.0,6.8] / tolerated [6.0,7.0]; tips 10/10 attributed; `source_set` 35 (NA-2); 30 open_findings in-record (0 unresolved blockers).

## Open (non-blocking) items

- **Per-crop warm `sources` arrays NOT yet fully proven T1.** Verified one crop at a time in the gold-standard arcs (methodology v1.4 Step 4). **Lettuce's `se_gulf` is now proven (NA-3b, UGA B577/C963 + UF/IFAS); 8 warm regions remain** (CA next in NA-3c). `region_source_map` `source_status` flags carry the screened-vs-verified boundary.
- **Pause-state population is arc work.** Leading/trailing `wait` months + interior `wait` unclassified across most crops; the interior ones are the prime heat/cold-pause candidates. Each crop's arc classifies its own — lettuce in progress (warm-zone summer `heat_pause` populated in `se_gulf` resolved cells NA-3b; remaining warm regions in NA-3c+).
- **~~`succession_policy.sources`/`anchoring_urls` missing on lettuce~~ — CLOSED in NA-3a** (sources usu/umn/umd + verified anchoring URLs added when succession was authored).
- **`m15_na3b_finding_001` (non-blocking): warm `zones{}` 8–11 sourcing is SE-only**, mis-attributed for the 8 non-SE regions (a Reedley/CA-Interior user currently reads a Florida calendar in the raw zone layer). Reconcile zone-calendar sourcing region-by-region as each warm cell is authored; full zone re-sourcing may be its own pass. se_gulf zone 8/9 sourcing is correct.
- **`m15_na3b_finding_002` (ratification-pending): heat-primary/frost-secondary warm anchoring precedent.** Ratify before authoring the next warm cell (NA-3c). Governs all remaining warm regions + the pipeline.
- **POST-APP location-aware layer (NA-3b design thread + 2026-05-31 reversal — NOT dataset work now, deliberate design at app phase):** one coherent capability — (1) ZIP→region resolution (read path: no ZIP = generic zone calendar + prompt to enter ZIP; ZIP = region-resolved content); (2) `severity`-by-location for pests/diseases (runtime-derived, not authored per-region); (3) community-tip location stamp (zone + region; the contribution-flow model that lets the community grow — design BEFORE any contributions exist to avoid retrofitting tags onto collected tips); (4) **region-tip-override serving** (the resolver selects a region's override where one exists, else serves the anchor-phrased default; overrides are authored in-arc now but cannot be served until the resolver exists). Bundle as one design. Reminder (in memory): the app does not exist yet.
- **cherry z9 heat-pause drift** (4c flag) — M16.
- **Checklist beginner↔succession coherence reconciliation** — confirm the "within the succession envelope" formulation matches `calendar_model_schema_spec_v1_0.md` §2a; do it in NA-3a when the gate goes live (appears aligned).
- `sources_pending_admission` per-crop scaffold markers backed by real catalog entries; sweep cosmetically at re-run.
- m12_audit_finding_001 (beefsteak soil key-order): cosmetic.
- Lettuce open_findings = 30 in-record. Final-audit candidates: s2c_na_004, s1c_003, m13_companions_003, m13_companions_005.
- M9B anchoring_urls manual browser verification (m9b_finding_001).
- Catalog deferred: add `nrcs_soils`; 2 dangling refs (britannica, walter_reeves).
- Methodology doc path correction: `soil_education.<vocab>` (not `.textures.<vocab>`).
- **blocks_launch counting:** 6 resolved S1A/S1B findings retain `blocks_launch:true` with `status:"resolved"`. Readiness gates MUST use the two-field predicate (`blocks_launch AND status != "resolved"`), never a bare count.
- **README paste hygiene:** session-close READMEs keep inline `#` comments and parentheses OUT of copy-paste command blocks (zsh chokes on `(...)`). Commands-only fenced blocks; explanation in prose above.

## Schema versions -- do not conflate

**2.8 (current on disk)** spans: register suffixing (Phase 0); companions register-by-membership; additive region scaffolding (Phase A/B — `regions{}` sibling, `northern_tier` populated, warm PENDING except lettuce-in-progress); calendar-model scaffolding (4c). All additive/within-version reshapes against a dataset with no live readers.

**The region-primary FLIP** (Phase C, step 7) — region becomes the primary calendar key; `zones{}` collapses to frost-refinement; wrap-as-dict; region-scoped `lifecycle_override`. **GATED — do not apply early.** Ships only after lettuce + cherry + beefsteak carry real region-layer data. **Note the distinction the 2026-05-31 decision sharpened: populating a crop's region cells (arc work, happening now) is SEPARATE from the global flip (gated, after M16).** 4c's `track` migrates with each `plantings[]` entry; `calendar_basis` rides at crop level.

**The perennial extension** (step 9) — perennial field surfaces. Gated before the first perennial anchor; carrot precedes it.

**`lifecycle_override` is REGION-scoped.** Crop-level `lifecycle` stays; `regions[r].lifecycle_override` carries `practical_lifecycle` + reason prose (both registers) + sources. Strawberry Central Valley annual is the driver. Provisional list (each per-region): strawberry, basil zones 10-11, tomato/pepper zones 10-11, borderline kale.

---

*Update this file at each session close.*
