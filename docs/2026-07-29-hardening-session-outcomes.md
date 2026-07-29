# Post-asparagus hardening — session outcomes

**Date:** 2026-07-29
**Kickoff:** `docs/2026-07-26-post-asparagus-hardening-kickoff.md` (items 1-4)
**Canonical:** `b0d01f13` -> `dc545be6` -> `b961d502` -> `7bc4b954` -> **`dd24b180`** (four guarded promotes)
**Status:** items 1-4 all closed; both loose ends closed; state trio DONE (surgical, flagged).
**UNCOMMITTED** — awaiting Trevor's approval.

---

## What shipped

| item | outcome |
|---|---|
| 1. region-prose coherence gate | was already DONE (A51, 2026-07-28). Untouched, except a corrected usage note + a repaired test. |
| 2. three thin asparagus values | **all three discharged.** 2a re-sourced (real upgrade), 2b accepted on new evidence, 2c was already fixed and its finding was the defect. |
| 3. `verification_log_ref` convention | **ruled, documented, applied.** Append-only; two Class 2 corrections landed. |
| 4. `unsuitable` fabricated calendars | **unblocked and fixed.** Both consumers already hide these cells; 11 fabricated calendars emptied behind two TDD-proven carve-outs. |

Gauntlet at `dd24b180`: `gate_all` **121/121**, `release_verify` clean but for the expected
two-crop footprint concern, `region_prose` 0, `harvest_duration` 0, `zone_order` 0,
`herbaceous_perennial` 0, `calendar_coherence` 0, `timing_spine` 0, `register_completeness` PASS,
COMPACT preserved (byte-identical re-serialization), no new test failures.

---

## Item 3 — the ruling

Full rationale in **`docs/verification_log_ref_convention.md`**; the rule itself is now in
`CLAUDE.md`.

`verification_log_ref` is an **append-only, cert-dated historical record**, never a living
summary. A pass that invalidates one of its assertions appends
`[CORRECTION <date>: ... -- see <finding id>.]` and leaves the original prose byte-for-byte.

The kickoff's stated reason (preserve the audit trail) turned out to be the *weak* argument —
`open_findings` and `STATE_HISTORY.md` already carry that trail, and the retired asparagus chill
mechanism is recorded in three separate findings. The decisive argument is that **a living summary
is unenforceable at 116 crops and drifts silently**: 13 of 115 prose log_refs already assert a
count that no longer matches, and 7 drifted for no reason but the roster growing 10 regions -> 16.
Maintaining those would be the backfill treadmill `CLAUDE.md` forbids.

**No gate.** A count-assertion scanner was built, measured, and deliberately left unwired at
`tools/logref_count_scan.py`: of 14 rows, 7 are correct historical prose, 4 are regex noise on good
writing (`"better with two varieties"` is pollination advice), 1 is a shape outlier, and **2 were
real**. Tightening cannot rescue it, because no regex separates "stale because the roster grew"
from "stale because the value was retired" — that is a judgment about causes, which is what the
documented two-class rule is for.

Two Class 2 corrections applied: **asparagus** (claimed 18/8/13, actual 25/4/10, plus the retired
*chill* mechanism and a now-false "extreme-heat desert zones deny it entirely" clause) and
**artichoke** (claimed 25 marginal; 22 of those are `annual_only` since the sixth value shipped).

Also ruled, both deliberately NOT gated: `lettuce-leaf`'s list-of-filenames shape stays (it is the
field name's original meaning, and unlike `weeks_indoors` no consumer reads this field, so a mixed
shape has no failure mode); and presence is **not** a cert requirement, since five certified crops
carry no log_ref and authoring a narrative today about what was believed months ago would be
writing history rather than recording it.

---

## Item 4 — the fix, and the decision it required

**The blocker was already cleared, verified rather than assumed.** Both consumers refuse to render
an `unsuitable` cell:

- **plant-astro** — `src/lib/regions.ts` `growableZonesByRegion` and `src/lib/built-crops.ts`
  `zonesForCrop` both `continue` on the value, so no page is built and the zone is not listed.
- **plant-app** — `src/lib/suitability.ts` maps `unsuitable -> 'blocked'` and
  `guide-perennial-calendar.ts` returns `{supported: false}`. Its header names these very
  calendars *"the motivating defect"* and states the app *"keeps working if those calendars are
  ever cleaned up upstream"* — which is exactly this change.

**Two carve-outs, TDD RED before GREEN**, both keyed on the **value** rather than the archetype:
`coverage_floor_gate.calendar_presence_violations` (A32) and the `herbaceous_perennial_gate`
calendar floor (A46) now exempt `unsuitable`. RED reproduced the kickoff's prediction exactly
(A32 = 10, A46 floor = 10). Adversarial tests pin that every other suitability value, a missing
suitability key, and five near-miss spellings all still bounce — and that an `unsuitable` cell
still **must** carry `suitability_note_seasoned`. That asymmetry is the design: no fake cycle, but
never a bare downgrade.

The floor's old wording, *"mark unsuitable, still show the honest cycle"*, assumed a cycle exists
to show. For a structurally impossible zone there is none, so the floor was **forcing a
fabrication** — the `fill-the-shape-is-the-defect` hazard, and the gate-avoidance pattern inverted:
not a field deleted to dodge a gate but a field invented to satisfy one.

**11 calendars emptied, not 10.** The kickoff scoped this to asparagus's 10; it was written before
artichoke certified. `artichoke.ca_desert.11` carries the identical 12-token all-`growing`
fabrication, on a cell whose own note says *"No California desert ground actually reaches zone 11,
so this cell is effectively vacant."* Closing 10 of 11 instances of one class would have been
worse. **This eleventh cell is the one item here that goes beyond the kickoff's literal scope and
wants explicit sign-off.**

### DECISION: roster-wide `suitability` is NOT wanted

The kickoff asked for a recorded decision. **Answer: no, and it is not a gap.**

`suitability` exists on 21 of 128 crops (19 fruit trees + asparagus + artichoke). For the other
107 the question "should this crop appear for this zone?" is already answered by a different,
working mechanism: **cell absence**. plant-astro states it outright — *"Annual cells carry no
suitability key, so for them growable == cell exists (absence of a cell is how annuals express
won't-grow)."*

The field is archetype-appropriate, not under-rolled-out. It exists because a **perennial** can
occupy states an annual cannot: present-but-unproductive (`survives_no_fruit`),
present-but-not-persisting (`marginal`), or persisting-only-as-an-annual (`annual_only`). Asking
whether an annual "persists" is meaningless for a plant replanted by definition every year. A
roster-wide rollout would add a redundant field to 107 crops and create a second source of truth
for a question already answered — and per `CLAUDE.md` a completed rollout becomes a hard cert
requirement, so it would tax every future crop for nothing.

**Revisit only if** a consumer needs to distinguish "no cell authored yet" from "authored, won't
grow." Today cell absence conflates those two, which is the one real cost of this decision and is
worth writing down.

---

## Item 2 — the three thin values

### 2a. `warm_arid` z8 crown window — RE-SOURCED (the pass's clearest win)

**The window is unchanged at `Feb 1 - Feb 28`. Its provenance moved from drawn-bar geometry to
extension text.** TAMU **EHT-066** *Easy Gardening: Asparagus* states verbatim:

> "Asparagus is grown from 1- or 2-year-old crowns planted in January or February, or as soon as
> the ground can be worked."

Verified in-session by urllib download + pypdf extraction (HTTP 200, 1,301,793 bytes, 42 asparagus
mentions) — **not** a WebFetch summary. Geography is authorized by the dataset's own
`region_source_map`, which labels this region *"Warm Arid (S. NM / W. TX)"* and names
`tamu_agrilife` its z8 anchor for the *"far-west TX / El Paso corridor"*; EHT-066 itself names West
Texas one of the two areas the crop suits best.

The cell now cites `tamu_agrilife` alongside `nmsu_ext`, with `resolution_method`
`extension_chart_geometry` -> `nmsu_tamu_arid_month_resolution` — an existing value already used on
`lettuce-leaf`'s warm_arid z8 cell with the same two sources, rather than an invented 81st method
string. `nmsu_chart` is retained as corroboration, so the Shillingburg / Las-Cruces-only provenance
weaknesses stop being load-bearing.

**The NMSU search is closed, not unfinished:** H-227, CR-457 and CR-457-B (the last revised January
2026) were all read; none publishes an asparagus crown date, CR-457-B's planting table has no date
columns at all, and the El Paso County MG calendar omits the crop entirely. The residual caveat is
now the honest one — the *month* is text-sourced and independently corroborated by USDA NRCS SCAN
8-inch soil data at Jornada Experimental Range (median first sustained 50°F crossing **Feb 2**,
2010-2025, against H-227's own 50°F criterion), while the **day edges** are conventions no source
publishes.

### 2b. `northern_tier` z3-z7 ladder — ACCEPTED, ruling upheld, one rationale RETRACTED

**The multi-state source this item asked for was found, and it argues for accepting the gap rather
than closing it.** The **Midwest Vegetable Production Guide** (8-state land-grant collaboration
spanning z3b-z7a, MSU-published) states one undifferentiated window for the whole footprint —
verbatim *"Transplant April 15 to May 15"* — with **zero zone-keyed references anywhere in its
asparagus section** (verified in-session: HTTP 200, 8 pages, 44 asparagus mentions, pypdf). So the
multi-state literature does not resolve by zone either. A five-rung ladder is finer than any
source, which is precisely what `state_source_zone_mapped` already declares.

All five rungs land inside a verbatim in-state T1 quote (z3 May 1 / UMN + NDSU "early May"; z4 Apr
20 / SDSU "mid-April through June"; z5 Apr 10 / Iowa State "early spring (April)"; z6 Apr 1 /
UConn "early April to late May"; z7 Mar 20 / Missouri G6405 "late March or early April").

**Re-derivation from frost was tested and rejected:** the ladder steps 10-11 days per zone while
zone frost steps 14-15, so a constant offset reproduces z3-z5 and breaks z6 and z7 against three
sources. Crown timing is soil-thaw- and nursery-shipping-bound at the ends, not frost-bound, so
the non-constant offset on this `frost_anchored` crop is **deliberate**.

**The soil-workability ruling is upheld on a stronger basis than the original record claimed:**
five independent institutions vs UMaine's one, plus two real tie-breakers the finding said were
missing — Missouri G6405's *"Spring freezes will not harm the crowns or subsequent harvests but can
damage emerging spears"* (the frost hazard is to emerged spears, not dormant crowns), and the fact
that the literature's frost lever is planting **depth**, stated in UMaine's own document. UMaine is
also the outlier against its own 6-state regional guide, which applies "after the danger of frost"
only to 8-to-12-week-old **seedling** transplants.

> **RETRACTION.** The *"Fusarium-in-cold-wet-soil rationale"* that finding 10 attributes to UMaine
> **is not in Bulletin #2071.** Verified in-session by direct fetch (HTTP 200, 50 asparagus
> mentions): the document has five Fusarium statements, none a cold-wet-soil argument, and the
> strings `"cold wet"`, `"cold, wet"`, `"wet soil"` and `"cold soil"` each occur **zero** times.
> UMaine gives the after-frost rule bare, with only a 50°F threshold and no stated reason. An
> earlier pass invented the rationale. It must not be reasoned from.

### 2c. `ca_desert` z9 harvest — ALREADY FIXED; the finding itself was the live defect

The item's premise was two revisions stale. z9 is **`Mar - May`** (not `Feb - Mar`) and z10 is
`Mar - Apr`, so **both start in March and there is no inversion**; commit `7738de1` fixed it on
2026-07-27. `zone_order_gate` and `harvest_duration_gate` both return 0.

**Finding 21 sat `open` still asserting the old value, and that stale text is what caused a full
re-sourcing pass to be commissioned against a value that no longer existed** — the same hazard
ruled on for `verification_log_ref` the same day, in a different field.

The re-source ran anyway and returned nothing, for a **geographic** rather than an effort reason,
which closes the re-open door permanently: UC's four-district California scheme scopes "Desert
Valleys" to the Imperial and Coachella valleys (z10), so neither Barstow nor the Palo Verde Valley
sits inside **any** UC district, and the two county programs covering that ground publish
planting-only lists with no harvest month.

---

## Surfaced, filed, NOT fixed — these want their own arc

The northern_tier and ca_desert passes turned up citation defects that are out of this pass's scope
and belong to the **§5 citation-integrity cleanup arc**. Every item below was verified by direct
fetch, not relayed:

1. **`msu_ext` is cited on all five northern_tier cells and contains no crown timing.** The cell
   URL resolves to a real 25,784-character MSU article — genuine land-grant, cited for a claim it
   does not make. The same defect five times.
2. **Five source ids resolve to portal roots**, not documents: `ndsu_ext`, `sdsu_ext`,
   `umaine_ext`, `iastate_ext`, `uconn_ext`. All return HTTP 200, so a URL-liveness check (tier A)
   would pass them; only a claim-support check (tier B/C) catches them. **`uconn_ext` points at a
   different host entirely** from the real UConn asparagus fact sheet.
3. **`sdsu_ext` is cited on z3 but its sentence is a z4 statement** ("mid-April through June")
   that would argue for a start two weeks earlier than the z3 cell says — cited where it
   contradicts.
4. **`umaine_ext` on z4** is cited for a rule that forbids the z4 window (after-frost vs an Apr 20
   start = last_spring − 11 days). Either drop it or record an explicit dissent.
5. **The `uc_ipm` URL on `ca_desert` z9/z10/z11 is UC IPM's ARCHIVED page**, self-labelled *"not
   actively maintained ... All links have been removed"*. A live equivalent exists and additionally
   carries a California-specific 3-4 week / 8-10 week harvest ramp.
6. **A T2 trap worth naming:** UC MG Riverside's own Flyers page links a "planting calendar" that
   is a **Grangetto's Farm & Garden Supply** retail chart sourced to "Digital Seed" — T2 seed-trade
   content on a `ucanr.edu` URL, image-only so pypdf returns 22 characters. The most
   citable-*looking* and least citable thing in the sweep.
7. **`asparagus.ca_desert` z9 is climatically bimodal** (Barstow ~2,100 ft high desert vs Blythe
   ~270 ft low desert, 10a on the 2023 map) while its prose describes only the cooler half.
8. **A repaired test, and what it means.** `tools/test_region_prose_gate.py` had been **failing at
   import** since the `annual_only` patterns shipped (`3258e4c`): its "well-formed region -> clean"
   fixture said *"Replant each year in zones 8 and 9"* over two `marginal` cells, and `annual_only`
   turned that phrase into a rating assertion, so the fixture asserted a genuine contradiction was
   clean. **The gate was right; the fixture was stale — the annual_only extension shipped with its
   own regression coverage broken**, while that commit's log recorded all gate suites passing.
   Fixed, plus new tests pinning both the coherent and contradictory `annual_only` directions.
9. **Seven pre-existing test-file failures remain** (unchanged by this session, matching the
   earlier note): `test_build_berry_pilot_patch` and `test_build_corn_family_patch` (missing
   `/private/tmp` fixtures), `test_build_region_promote`, `test_gate_all` (stale hardcoded "114
   certified", now 121), `test_gen_current_state` ("generated file dropped the protocol header" —
   relevant to the known `CURRENT_STATE.md` regen hazard), `test_region_harness`,
   `test_verify_demux_footprint`.

---

## The two loose ends — both CLOSED

### The state trio — done, and it uncovered the session's biggest find

`LATEST.txt` bumped to `dd24b180`; `STATE_HISTORY.md` and `CURRENT_STATE.md` both prepended;
canonical SHA verified equal to `LATEST.txt`.

**`CURRENT_STATE.md` had lost its title and binding SESSION PROTOCOL header.** Dropped silently by
`93d5a59`'s own state-trio regen and missing for 40+ commits, while `CLAUDE.md` sends every session
there for exactly that header. Commit `ac18c8e` is titled *"protocol-header restore"*, so this had
already happened once. Recovered verbatim from `93d5a59^`, with protocol #4 updated to CLAUDE.md's
current gauntlet.

**Losing it armed a file-destroying second defect.** `gen_current_state.static_header()` partitions
on the first `---`; with the separator gone it **failed open and returned the entire file as the
header**, so one regen would have duplicated all 351KB and the next would have doubled it again
(measured: generator output 377KB against a 351KB file). That fail-open is now a **hard abort** on
both a missing separator and a missing SESSION PROTOCOL, because the header cannot be reconstructed
from the file once lost — only from git.

**`test_gen_current_state.py` had been failing on precisely this assertion the whole time, and was
dismissed as stale test rot** — including by me, in this session's first summary.

> **FLAGGED DEPARTURE — a decision for Trevor.** The trio was done **surgically, by prepend**, not
> by regeneration as protocol #2 requires. `CURRENT_STATE.md` has re-accumulated **79 history
> entries** (353KB, against a **28KB** proper regen), drifting back into a second history log — the
> very split `148e737` performed. Measured: **70 of those 79 carry prose found in neither
> `STATE_HISTORY.md` nor `STATE_HISTORY_ARCHIVE.md`**, even after whitespace normalization; the two
> files hold independently *worded* accounts of the same releases. So a regen would not lose the
> facts but would delete 70 uniquely-written entries. That is not a call to make unilaterally, so
> the file wants a decision: return it to a lean 28KB generated surface, or amend protocol #2 to
> match how it is actually maintained.

### The test suite — 78/78, from 7 failing

Every one was diagnosed, not silenced.

| test | verdict |
|---|---|
| `test_gate_all` | hardcoded `114`, now **derived** from the actual `verified_gs_arc` set |
| `test_verify_demux_footprint` | hardcoded `124` ×4, now the canonical's own `total_crops` |
| `test_gen_current_state` | hardcoded `"10/10"` roster width, now derived — **and it had masked the real header failure by dying first** |
| `test_region_harness` | **stale premise from real progress** — simulated "no pnw cell" by omission, which broke the day PNW promoted. Harness now takes `None` as an explicit REMOVE sentinel, restoring genuine A31 coverage |
| `test_build_region_promote` | asserted the pnw provenance note was appended, only true pre-PNW; now asserts the builder's correct **idempotence** |
| `test_build_berry_pilot_patch`, `test_build_corn_family_patch` | **discharged one-shots** whose session-scoped `/private/tmp` staging is gone; now **skip loudly**, naming what is uncovered, because reconstructing them would mean fabricating staged crops |

**A real tool bug sat behind one of these:** `verify_demux_footprint.py` hardcoded `!= 124` on both
sides, so at 128 crops it reported a false problem on **every run** — *"base=128 candidate=128 (want
124)"*, a footprint auditor failing a clean footprint. Its actual invariant is base == candidate,
which is roster-size independent.

---

## Still owed

- **The §5 citation cleanup arc.** Genuinely a separate session: 2,660 citation pairs across 1,153
  distinct URLs, and the nine items above are its evidence base, not its execution. **Tier A is
  insufficient on its own** — every portal-root defect found returns HTTP 200.
- **The `CURRENT_STATE.md` structural decision** in the flagged block above.
