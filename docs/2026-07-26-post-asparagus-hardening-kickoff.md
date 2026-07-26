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

### Gate design notes

- **Scope on the crop having cell-level `suitability`**, not on archetype and not on
  `calendar_basis`. Keys on the thing that makes the check meaningful. (Compare A47, which keys on
  `crop.perennial` for exactly this reason.)
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
