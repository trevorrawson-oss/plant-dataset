# Post-asparagus hardening — kickoff

**Date:** 2026-07-26
**Run after:** the artichoke GS arc (`docs/2026-07-26-artichoke-gs-arc-kickoff.md`).
**Scope:** three loose ends left deliberately at the end of the asparagus timing work. This is a
hardening + honesty pass, not an authoring arc. No new crop.
**Context:** `CURRENT_STATE.md` top five entries; `docs/2026-07-25-asparagus-timing-gaps.md`.

Each item below is already recorded as an `open_finding` on asparagus. None blocks launch. They
are here because they are the things most likely to bite silently later.

---

## Item 1 — Build the region-prose vs cell-rating coherence gate

> ## ✅ DONE 2026-07-28. DO NOT REBUILD.
>
> Shipped as **`tools/region_prose_gate.py`**, wired into `whole_crop_gate` as **A51**, and it runs
> **ROSTER-WIDE** rather than archetype-scoped — the first check in the suite to do so, because a
> crop contradicting its own cells is not an archetype-specific failure. Built during the artichoke
> arc so its first job was checking copy as it was written. Commits `766a5c5` (gate + hard-flip) and
> `ced0499` (the repair).
>
> **It found a live defect on certified asparagus on its first run**, which is what this item
> predicted: `ca_south_coast` prose said *"Frost-free zone 11 is unsuitable"* while the z11 cell was
> rated `marginal` with a full `plant_out` and harvest window. The prose was the stale half. Reading
> it also turned up a second contradiction in the same block that the gate does NOT check
> (*"Harvest from February"* against three cells reading `"Mar - May"`) — no gate compares a
> region-prose MONTH to its cells' harvest windows. Both repaired.
>
> **Read the gate's module header before touching it.** The first version shipped three checks and
> produced **38 findings roster-wide, of which exactly ONE was a defect.** The other 37 were
> comparative prose ("where a navel is only marginal" — a different crop), place-based
> differentiation instead of zone numbers, and a boundary zone named to mark the limit beyond a
> region. The fix was to narrow the CHECK to zone-bound assertions, not to narrow its scope: 38 → 3
> → 0. The ten verbatim false positives are pinned as regression tests in
> `test_region_prose_gate.py` so it cannot drift back to keyword matching.
>
> **Known limit, recorded:** the rule is any-match, so the FLAT contradiction is caught and the
> HEDGED form is not — including, ironically, the "perennialize only marginally" sentence quoted
> below that motivated this whole item. Tightening to an exact-set match fires on correct writing
> like "marginal to unsuitable depending on the season". A future pass wanting the hedge needs a
> different mechanism, not a wider net.
>
> The expensive half this item flagged as separable — auditing 12 long-certified fruit trees — turned
> out NOT to be expensive: once the check was correct, all of them passed on their own merits.

**Priority: highest of the three.** This is the only item that could be hiding live defects in
already-certified crops.

### The defect class

`region_notes_seasoned` / `region_notes_beginner` are a consumer-facing prose layer that
*summarizes* the per-zone `suitability` ratings. **Nothing cross-checks the two.** A36 verifies
both registers exist; A29 verifies they are authored; neither reads what they say.

This bit during the asparagus repair. After re-rating `ca_north_coast` z9 and z10 to
`perennializes`, the region note still read:

> "…so both zones 9 and 10 perennialize only marginally, with modest vigor and a shorter stand
> life than the interior valleys deliver."

Two strings the same guide renders to the same reader, in direct contradiction. Caught by hand,
by nothing else.

### The scope is far smaller than "128 crops of free text"

Measured 2026-07-26 against canonical `34025ee3`:

- **Only 20 crops carry cell-level `suitability`** — 19 fruit trees (deciduous + evergreen) plus
  asparagus. Artichoke will make 21.
- Of 640 region-note strings on those crops, **37 make a checkable zone + suitability claim**,
  across 13 crops: peach 2, lemon 1, plum 2, apricot 1, mandarin-clementine 1, pomegranate 5,
  persimmon 6, pawpaw 6, grapefruit 1, cherry-sweet 1, nectarine 2, cherry-sour 2, asparagus 7.

So the gate surface is ~37 assertions, not an open-ended free-text problem. That is small enough
to verify entirely by hand before writing any gate.

```bash
# reproduce the surface measurement
cd ~/plant-dataset && python3 -c "
import json,re
d=json.load(open('crops_data_final.json'))
SUIT=re.compile(r'(perennializ|marginal|unsuitable|not worth planting|will not (?:fruit|crop|survive))',re.I)
ZONE=re.compile(r'zones?\s+(\d+)(?:\s*(?:and|to|-|through)\s*(\d+))?',re.I)
for c in d['crops']:
    if not any(z.get('suitability') for r in (c.get('regions') or {}).values()
               for z in (r.get('resolved_by_zone') or {}).values() if isinstance(z,dict)): continue
    for rk,r in (c.get('regions') or {}).items():
        for f in ('region_notes_seasoned','region_notes_beginner'):
            s=r.get(f) or ''
            if SUIT.search(s) and ZONE.search(s):
                print(c['slug'], rk, f); print('   ', s[:220])
"
```

### Do it in this order — audit first, gate second

**Step 1 (the valuable part): hand-audit all 37.** For each, read the claim, resolve the zones it
names, and compare against those cells' actual `suitability` values. **Expect to find real
defects.** Twelve of these crops are fruit trees certified well before the asparagus work, and
nothing has ever checked this layer for them. If the audit surfaces contradictions, that becomes
its own correction arc — and it will have been worth the whole pass.

Report the audit as a table: crop · region · field · claim · actual ratings · verdict.

**Step 2: only then decide the gate.** Two outcomes:
- **Audit clean or nearly so** → write the gate. It is cheap and it locks the invariant.
- **Audit floods** → the prose needs normalizing before a gate is viable. Do not ship a gate that
  cries wolf; that is the `a25-tightening-floods` / `growth-stages-shape-not-gated` failure
  pattern, and a noisy gate gets ignored, which is worse than none.

### A sample audit was already run — read this before starting

A heuristic pass over all 37 claims on 2026-07-26 flagged 13. **On reading, almost all were false
positives from the heuristic, and the fruit-tree prose is genuinely careful.** Example — pawpaw
`ca_south_coast`: *"the tree may survive in the milder zone 9 with irrigation but sets little, and
zone 10 is unsuitable"* maps precisely onto its cells. So **do not expect a drift crisis in the
fruit trees.** Two recurring heuristic failure modes to avoid repeating: (a) grabbing the FIRST
zone in a sentence and attributing a later clause's verb to it (pear-asian northern_tier reads
"fruits reliably from zone 5 south… in zone 4 the tree…" — the "marginal" belongs to z4), and
(b) not knowing the full vocabulary (below).

The audit's real yield was structural: it exposed that **`suitability` has FIVE values across two
archetype families**, which the original version of this document did not account for.

| value | cells | used by |
|---|---|---|
| `fruits_reliably` | 292 | fruit trees only |
| `marginal` | 180 | **both families** |
| `unsuitable` | 165 | **both families** |
| `survives_no_fruit` | 118 | fruit trees only |
| `perennializes` | 25 | asparagus (herbaceous_perennial) only |

`marginal` and `unsuitable` are shared; the "positive" value is archetype-specific
(`fruits_reliably` for trees, `perennializes` for the herbaceous perennial). There is no
documented enum covering all five — **worth adding one as part of this item**, since a gate that
hardcodes three values will silently pass the 410 fruit-tree cells using the other two.

### DISPLAY RULE — ruled by Trevor 2026-07-26

Four states, four behaviors. The line between show and hide is **whether the limiting factor
varies between years**:

| value | frontend behavior |
|---|---|
| `fruits_reliably` / `perennializes` | show normally |
| `marginal` | **show with caveats** — chill or dormancy varies year to year, and an unusual season may deliver. The take-your-chances case. |
| `survives_no_fruit` | **show, flagged ORNAMENTAL-ONLY** — the plant lives and gives you no food. Someone may still want the tree. |
| `unsuitable` | **hide for that zone** — structurally impossible; there is no year that will differ. |

No new field is needed: all four values are already authored. Note `survives_no_fruit` (118 cells)
is precisely the "someone might want an apple tree anyway" case — it is a distinct authored state,
not a flavor of `marginal`.

Honest nuance for the copy: `unsuitable` does not mean the plant dies. UF/IFAS says outright *"If
you're determined to give it a try, plant one- or two-year-old asparagus crowns…"* and then that
growth is "more or less continuous, resulting in weak, spindly spears." The failure is indefinite
disappointment, not death.

### Gate design notes

- **Scope on the crop having cell-level `suitability`**, not on archetype and not on
  `calendar_basis`. Keys on the thing that makes the check meaningful. (Compare A47, which keys on
  `crop.perennial` for exactly this reason.)
- **Handle all five values.** A gate written against asparagus's three will no-op on the 410
  fruit-tree cells that use `fruits_reliably` / `survives_no_fruit` — the majority of the surface.
- Parse zone references (`"zone 9"`, `"zones 9 and 10"`, `"zones 9 to 11"`) and suitability verbs
  from the prose, then compare against `resolved_by_zone[z]["suitability"]`.
- **Only flag a genuine contradiction**, never absence. Prose that does not mention a zone is
  fine. Prose that says a zone is marginal when the cell says `perennializes` is not.
- Watch the asymmetry: "perennializes only marginally" means `marginal`, not `perennializes`.
  Substring matching on `perennializ` will get this wrong. That exact phrasing is what the
  asparagus contradiction was written in.
- **TDD, RED before GREEN**, per CLAUDE.md. Inject the defect into a scratch copy — flip a cell
  rating without touching its region prose — and confirm it bounces. Then confirm it does not
  flood the other 19 crops.
- Wire soft first if the audit is not clean, with a documented hard-flip condition. That is the
  house pattern (A47, `control_ladder_gate`, `variety_resistance_gate`).

**Done when:** all 37 assertions verified, any contradictions fixed or filed, and either a
TDD-proven gate is wired or there is a written reason it is not viable yet.

---

## Item 2 — Re-source or explicitly accept three weak asparagus values

> ## ✅ DONE 2026-07-29. All three discharged. See `docs/2026-07-29-hardening-session-outcomes.md`.
>
> - **2a RE-SOURCED.** The window stays `Feb 1 - Feb 28`; its provenance moved from drawn-bar
>   geometry to extension TEXT. TAMU **EHT-066**: *"Asparagus is grown from 1- or 2-year-old crowns
>   planted in January or February, or as soon as the ground can be worked."* Verified by
>   urllib + pypdf in-session. The cell now cites `tamu_agrilife`, method
>   `nmsu_tamu_arid_month_resolution` (reusing `lettuce-leaf`'s warm_arid z8 precedent). The NMSU
>   search is CLOSED: H-227, CR-457 and CR-457-B (rev. Jan 2026) all read, none publishes a crown
>   date. Finding 11 -> `resolved`.
> - **2b ACCEPTED, ruling upheld, one rationale RETRACTED.** The multi-state source this item wanted
>   exists and argues FOR accepting: the Midwest Vegetable Production Guide (8 states, z3b-z7a)
>   states ONE window, *"Transplant April 15 to May 15"*, with zero zone references. Frost
>   re-derivation was tested and rejected (the ladder steps 10-11 d/zone, frost steps 14-15).
>   Soil-workability upheld 5 institutions to 1, with two real tie-breakers.
>   **The "Fusarium-in-cold-wet-soil rationale" attributed to UMaine is NOT in Bulletin #2071 and is
>   retracted as fabricated** (verified: `"cold wet"`/`"wet soil"`/`"cold soil"` all occur zero
>   times). Findings 9 and 10 stay `open` as accepted-limits with dated dispositions.
> - **2c WAS ALREADY FIXED, and the finding was the defect.** z9 is `Mar - May`, not `Feb - Mar`
>   (commit `7738de1`, 2026-07-27); z10 is `Mar - Apr`, so both start in March and there is no
>   inversion. Finding 21 sat `open` still asserting the old value, **which is what caused this
>   whole re-sourcing pass to be commissioned against a value that no longer existed.** The
>   re-source ran anyway and returned nothing for a GEOGRAPHIC reason (UC's four-district scheme
>   puts Barstow and the Palo Verde Valley in no UC district), which closes the door permanently.
>   Finding 21 -> `resolved`.
>
> **Citation defects surfaced and filed, NOT fixed** (they belong to the §5 cleanup arc): `msu_ext`
> cited on all five northern_tier cells with no crown timing; five source ids resolving to portal
> roots that all return HTTP 200; `sdsu_ext` cited on z3 where its own sentence contradicts the cell;
> `umaine_ext` on z4 cited for a rule that forbids that window; the `uc_ipm` URL pointing at UC IPM's
> self-labelled ARCHIVED page.

All three shipped with their limitations recorded. None is wrong; each is *thinner than the rest
of the crop*. The task is to either strengthen or formally accept them, not to leave them
ambiguous.

### 2a. `warm_arid` z8 `plant_out` = "Feb 1 - Feb 28" — no quote exists, and none can

The window exists only as a **drawn bar** in the NMSU Doña Ana planting chart, with no text layer.
It was recovered from PDF content-stream geometry (asparagus bar spans x 213.0-257.0 against a
February column of x 212.80-258.35), cross-validated against the row's gridline gap, and confirmed
by rendering the page. Rigorous — but it is geometry, not a citation.

Two further weaknesses: the chart is **Master-Gardener-hosted and © Darrol Shillingburg**, not a
peer-reviewed NMSU circular, and it is **Las Cruces-specific** while `warm_arid` spans considerably
more than Las Cruces. The NMSU prose source (H-227) supplies only the anchor — *"plant crowns in
the spring after the soil temperature has reached 50°F"* — which is compatible with February in Las
Cruces but is not date confirmation.

**Target:** find a peer-reviewed NMSU circular (or another T1 covering the wider region) that
states an asparagus crown date. If none exists, either (a) widen the window to what the 50°F
anchor honestly supports across the whole region, or (b) formally accept the chart value and
upgrade the `open_finding` to a permanent caveat. Any of the three is fine; leaving it undecided is
not.

### 2b. `northern_tier` z3-z7 `plant_out` ladder — five states stitched into a zone ladder

No T1 source anywhere states an asparagus crown window **by USDA zone**. The five-zone ladder was
built monotonically from five different state sources (UMN/NDSU/SDSU → z3, UMaine → z4,
Iowa State/Illinois → z5, UConn → z6, Missouri → z7). Recorded per cell as
`state_source_zone_mapped`, which is honest, but it is the largest editorial construction in the
crop.

Compounding it: **`msu_ext` is cited on all five northern_tier cells and contains no
crown-planting timing whatsoever** — its only timing sentence concerns preparation the year
before. It was kept for what it does support, but it cannot corroborate any window.

Also unresolved and relevant here: the **two anchor families conflict by 4-6 weeks**.
Soil-workability (Illinois, Missouri, UConn, Arkansas) plants crowns *before* last frost;
frost-safe (UMaine: *"after the danger of frost has passed and the soil has warmed to above 50°F"*)
plants *after*, on a Fusarium-in-cold-wet-soil rationale. Soil-workability was ruled primary. That
ruling shapes the whole ladder and deserves a second look with fresh eyes.

**Target:** either find a single source family covering z3-z7 (a multi-state or USDA-level
publication) so the ladder rests on one calibration, or re-derive the ladder from the ruled anchor
plus this dataset's own zone frost data and document the offset. Revisit the anchor ruling as part
of it.

### 2c. `ca_desert` z9 harvest "Feb - Mar" — modeled, and now inverted against its sourced neighbour

`ca_desert` z10 carries a **sourced** home-garden harvest of Mar-Apr (UA az1615, the only
low-desert home-garden harvest statement located). z9 carries **Feb-Mar**, which was *modeled from
regional patterns* during the 2026-07-24 cert. So the cooler zone now reads *earlier* than the
warmer one.

That inversion is a sourced-vs-modeled asymmetry, not a biology claim, and the sourced value was
deliberately preferred over smoothing the ladder. **Fix the direction of the asymmetry by
re-sourcing z9, not by adjusting z10 to look tidy.** If z9 cannot be sourced, say so and keep the
inversion documented.

**Done when:** each of 2a/2b/2c is either re-sourced or has a written acceptance recorded in its
`open_finding`, with the finding's status updated accordingly.

---

## Item 3 — Rule on the `verification_log_ref` convention

> ## ✅ DONE 2026-07-29. Ruled APPEND-ONLY. See `docs/verification_log_ref_convention.md`.
>
> The recommendation below was adopted, but **for a different and stronger reason than it gives.**
> "Rewriting erases the audit trail" is the weak argument: `open_findings` + `STATE_HISTORY.md`
> already carry that trail (the retired chill mechanism appears in three separate findings). The
> decisive argument is that **a living summary is unenforceable at 116 crops and drifts silently** --
> measured, 13 of 115 prose log_refs already assert a stale count, and 7 drifted only because the
> roster grew 10 regions -> 16. That is the backfill treadmill CLAUDE.md forbids.
>
> **TWO DRIFT CLASSES**, and the test that separates them (*would a reader taking this as current
> truth be materially misled about this crop?*): **Class 1 context growth** (the "10/10 regions"
> statements) needs NO action, the date stamp is the correction. **Class 2 retired reasoning or
> revalued vocabulary** requires an appended `[CORRECTION <date>: ...]` line.
>
> **NO GATE, deliberately.** A count scanner was built and measured and is kept UNWIRED at
> `tools/logref_count_scan.py`: 14 rows, of which 7 are correct historical prose, 4 regex noise on
> good writing, 1 a shape outlier, and **exactly 2 real**. No regex can separate "stale because the
> roster grew" from "stale because the value was retired."
>
> **Applied:** asparagus (claimed 18/8/13, actual 25/4/10, plus the retired *chill* mechanism and a
> now-false desert clause) and artichoke (claimed 25 marginal; 22 are `annual_only`). The roster-wide
> check this item asked for was run -- that is the 14-row measurement.
>
> Also ruled, both deliberately ungated: `lettuce-leaf`'s list shape STAYS (the field name's original
> meaning; unlike `weeks_indoors` no consumer reads this field), and presence is NOT a cert
> requirement (five certified crops lack it; backfilling would be *writing* history).

`asparagus.verification_status.verification_log_ref` still contains the **retired chill
mechanism**, because it is the narrative record of what was believed at cert on 2026-07-24. It was
left deliberately: it is a backend field inside `verification_status`, not consumer-facing, and
rewriting it would erase the record of a real reasoning error rather than correct it.

But the convention has never been stated, which creates two opposite risks:

1. Someone "fixes" it later, thinking it is a leak of retired reasoning into live data — destroying
   the audit trail.
2. Someone reads a stale `log_ref` as **current truth** about a crop and reasons from it. This is
   the more dangerous direction, and it is exactly how the chill claim propagated in the first
   place.

**Decide and document, in CLAUDE.md or a convention doc:** is `verification_log_ref` an
append-only historical record, or a living summary kept current?

Recommendation: **append-only historical record**, with a required dated correction line appended
whenever a later pass invalidates something it asserts — so the trail survives *and* a reader
cannot mistake it for current state. If that is the ruling, apply it to asparagus now: append a
dated line noting the chill mechanism was retired 2026-07-26 and pointing at the correcting
findings.

Then check whether other crops' `log_ref`s carry claims later invalidated. This is a five-minute
grep and worth doing once the convention exists.

**Done when:** the convention is written down, asparagus conforms to it, and a roster-wide check
for stale `log_ref` claims has been run.

---

## Item 4 — `unsuitable` cells: the fabricated calendar, and the display rule

> ## ✅ DONE 2026-07-29. Unblocked and fixed. See `docs/2026-07-29-hardening-session-outcomes.md`.
>
> **Step 1 was already satisfied**, verified rather than assumed. BOTH consumers refuse to render an
> `unsuitable` cell: plant-astro's `regions.ts` `growableZonesByRegion` and `built-crops.ts`
> `zonesForCrop` both `continue` on the value (no page built, not listed); plant-app's
> `lib/suitability.ts` maps it to `'blocked'` and `guide-perennial-calendar.ts` returns
> `{supported: false}`. plant-app's own header names these calendars *"the motivating defect"* and
> says it *"keeps working if those calendars are ever cleaned up upstream"*.
>
> **Step 2 shipped.** Two carve-outs, TDD RED before GREEN, both keyed on the **VALUE** not the
> archetype: A32 (`coverage_floor_gate`) and the A46 `herbaceous_perennial_gate` floor now exempt
> `unsuitable`. RED reproduced this doc's prediction exactly (A32 = 10, A46 floor = 10). The
> asymmetry is pinned by tests: the calendar requirement drops, **the `suitability_note_seasoned`
> requirement stays** -- no fake cycle, but never a bare downgrade. Every other suitability value, a
> missing key, and five near-miss spellings all still bounce.
>
> **11 calendars emptied, not 10.** This doc predates artichoke's cert; `artichoke.ca_desert.11`
> carries the identical fabrication on a cell whose own note says the ground is *"effectively
> vacant"*. That eleventh cell is the one thing here beyond this doc's literal scope.
>
> **DECISION on roster-wide `suitability`: NOT WANTED, and not a gap.** For the other 107 crops the
> question is already answered by **cell absence** -- plant-astro: *"Annual cells carry no
> suitability key, so for them growable == cell exists."* The field encodes states only a PERENNIAL
> can occupy (present-but-unproductive, present-but-not-persisting). A rollout would add a redundant
> field to 107 crops, create a second source of truth, and become a hard cert requirement taxing
> every future crop. Revisit only if a consumer must distinguish "no cell authored yet" from
> "authored, won't grow" -- that conflation is this decision's one real cost.

Added 2026-07-26 after a failed attempt to fix it. **Read the attempt before retrying.**

### The defect

Asparagus's 10 `unsuitable` cells each carry a fabricated 12-token **all-`growing`** calendar. That
renders as *active year-round growth for a crop that cannot grow there* — worse than showing
nothing. It is the gate-avoidance pattern **inverted**: not a field deleted to dodge a gate, but a
field invented to satisfy one.

### What I tried, and why it failed

Relaxed `herbaceous_perennial_gate`'s calendar floor to exempt `unsuitable`, then emptied the 10
calendars. TDD passed on that gate (floor still bit for `perennializes`/`marginal`). **The gauntlet
then failed with 10 violations from A32** — "frost_anchored resolved cell has an empty/absent
calendar." Reverted both changes; canonical is unchanged at `34025ee3`.

**The correction to my reasoning, which matters for the retry:** I had justified the fix as
"align asparagus with the 19 fruit trees, which leave unsuitable calendars empty." That framing is
wrong. Of 165 unsuitable cells across the 20 crops carrying `suitability`, 155 are empty — but
those crops are **exempt**, not conventional: they ride perennial bases (`perennial_chill_gated`,
`perennial_evergreen`) where A32 no-ops entirely. Asparagus is on `frost_anchored` deliberately, so
it inherits yet another annual-crop requirement. This is the same structural tension as the A24
carve-out, and it would be the **fourth** carve-out in that family.

### Do the frontend first — this is the actual point

A32's wording is a **rendering contract**: "this archetype's cells must render a non-empty
month-strip calendar." Emptying the calendar before the frontend stops rendering these cells risks
trading a misleading calendar for a **blank card**. So sequence it:

1. **Frontend honors `suitability` and hides `unsuitable` cells for that zone** (Trevor's call,
   2026-07-26). Once an unsuitable cell is not rendered, its calendar content is moot and can be
   emptied safely.
2. **Then** carve A32 (+ the archetype floor) for `unsuitable` and empty the 10.

### The display rule

Ruled by Trevor 2026-07-26. **See Item 1's DISPLAY RULE section for the full four-state table** —
it belongs there because it depends on the five-value vocabulary documented in that item. In short:
`unsuitable` hides; `survives_no_fruit` shows flagged **ornamental-only**; `marginal` shows with
caveats; the positive values show normally. No new field required.

### The scope limit on the hide rule

**`suitability` exists on only 20 of 128 crops** (19 fruit trees + asparagus; artichoke will make
21). A hide-unsuitable rule therefore only ever affects those 21. For the other 107, "should this
crop even appear for this zone?" is **unanswered** — there is no field carrying it. That is a
much larger arc (roster-wide suitability rollout) and belongs in
`docs/field_addition_register.md` under the column GS-arc method, not in this pass. Worth deciding
whether it is wanted before the fruit-tree audit in Item 1 makes the 20-crop set feel complete.

**Done when:** the frontend hides `unsuitable`; then A32 + the archetype floor are carved for
`unsuitable` (TDD, RED first) and asparagus's 10 fabricated calendars are emptied; and a decision
is recorded on whether roster-wide `suitability` is wanted.

---

## Sequencing and effort

Item 1 first — it is the only one that may surface live defects, and its audit step is what makes
the rest worth doing. Items 2 and 3 are independent of each other and of item 1.

Rough shape: item 1 is a real pass (audit + possible corrections + a TDD gate); item 2 is a
sourcing pass over three cells; item 3 is a decision plus a grep.

**Do not let item 1's audit findings turn into silent edits.** If it surfaces contradictions in
certified fruit trees, that is a correction arc with its own gauntlet and state trio — surface it
to Trevor and scope it, exactly as the asparagus suitability findings were split into their own arc
rather than smuggled into the timing work.

Standing rules: canonical JSON is COMPACT and written via a promote script; TDD RED before GREEN on
any gate; verify every citation supports its specific claim and that its URL resolves; nothing
commits without Trevor's approval and he confirms every push.
