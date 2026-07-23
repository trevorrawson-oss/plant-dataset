# Pest/IPM control-ladder pilot -- STATE-TRIO DRAFT (for the coordinated release)

**Why a draft, not a live edit:** the pest/IPM pilot is COMMITTED but UNPUSHED, layered directly on top of
the concurrent Utah Dixie region state (canonical `2c98dd2b` -> `4f7789aa`). LATEST.txt / STATE_HISTORY /
CURRENT_STATE currently still record Utah's `2c98dd2b`. To avoid both sessions editing the live state files
at once (and per the `current-state-md-drift` memory -- CURRENT_STATE is hand-maintained, never regenerated),
these ready-to-merge entries are staged here. At the coordinated release, prepend / replace as marked, then
push both arcs together.

- Pest-arc canonical: **`4f7789aaed0c6a3ef44ec3fecd728a76ddd017b53dfd23ad03cfb45b8dbf1696`**
- Pest-arc commits (on main, interleaved with Utah): `b4bb71b` catalog / `a1755b0` safety / `857a856` ladders
  / `669a681` register row 23 (+ gate tooling `3614ada`/`d775471`/`389c8fd`/`371b33d` + doc fixes).

---

## 1. LATEST.txt -- REPLACE the whole file with:

```
SHA: 4f7789aaed0c6a3ef44ec3fecd728a76ddd017b53dfd23ad03cfb45b8dbf1696
Date: 2026-07-22
Session: PEST/IPM CONTROL-LADDER PILOT SHIPPED -- the FIRST honest IPM control-ladder foundation (field-addition register row 23), layered on Utah Dixie (`2c98dd2b` -> `b4bb71b` catalog -> `a1755b0` safety -> `857a856` ladders -> canonical `4f7789aa`; register row 23 committed `669a681`). Adds a shared top-level `control_methods` catalog (24 T1-sourced methods across the 5 IPM tiers cultural/physical/biological/soft_chemical/conventional, authored-once + referenced by id, mirrors `source_catalog`; +`npic_orst` NPIC source), a per-problem `control_ladder` (flat ORDERED softest-first array of `{method,note_*}`), a stable per-problem `id` (kebab; the vocabulary the NEXT variety-resistance arc references) + `type`, and a new top-level `pesticide_safety_education` object (label-is-the-law / PHI / pollinator / PPE / resistance, mirrors soil_education/ph_education). Retires the old `organic_treatment_*`/`management_*` treatment blobs. Pilot = broccoli + celery + microgreens (16 problems). NEW standalone `control_ladder_gate` (TDD, SOFT, scoped to ladder-bearing problems): referential + monotonic-tier + applies_to coherence + unique id; A39 register-coverage HARD-FLIP deferred to the roster-wide rollout (~897 problems). Honesty is the point: conventional named by active-ingredient class + example with the full caution set (bees/fish/PHI/read-the-label) and NOT demonized; organic-isn't-safe cons stated candidly (copper soil-accumulation + aquatic toxicity, sulfur foliage burn, neem/spinosad bee-harm-while-wet, Bt kills all lepidoptera larvae); honest short/cultural-only ladders where no spray applies (clubroot / blackheart / pink-rot / microgreens / root-maggot / rust-fly / leaf-miner); ONE justified conventional rescue rung (flea-beetle -> carbaryl). Independent T1-fidelity review CAUGHT an unsupported neem bee-toxicity claim (fixed) + 3 attribution gaps; horticulture review drove 3 ladder fixes. GATES: `gate_all` 119/119, `control_ladder_gate` 0, `register_completeness` PASS, adversarial RED battery (6 defect classes bounce on real shapes), `release_verify` clean (only the expected multi-crop single-crop-pilot concern), consumer sweep em-dash/dbl-hyphen/spelled-temp 0, canonical COMPACT, crops-elsewhere BYTE-IDENTICAL, count 128 / 119 certified unchanged (NO cert-count change). COMMITTED, UNPUSHED (Trevor confirms push; coordinated with Utah Dixie). NO plant-astro bump (astro session owns it, after push). NEXT ARC = variety resilience/disease-resistance (references the pest/disease `id`s); Approach C (crop-level pest hub) = a future register row. Spec/plan `docs/superpowers/{specs,plans}/2026-07-22-pest-ipm-ladder-*`.
```

---

## 2. STATE_HISTORY.md -- PREPEND this entry at the top of the stack (immediately below the `---` on line 7, ABOVE the Utah Dixie `## 2026-07-22 -- UTAH DIXIE` entry):

```
## 2026-07-22 -- PEST/IPM CONTROL-LADDER PILOT SHIPPED (field-addition register row 23)

Canonical `2c98dd2b` -> `4f7789aa` via 3 SHA-guarded splices layered directly on the Utah Dixie state:
`b4bb71b` (top-level `control_methods` catalog + `npic_orst` source add) -> `a1755b0` (top-level
`pesticide_safety_education`) -> `857a856` (16 `control_ladder`s across broccoli/celery/microgreens, old
treatment blobs retired). Register row 23 committed `669a681` (row 22 was taken by the concurrent
`utah_dixie` region). Count 128 / 119 certified unchanged. **NEW soft standalone gate**
`tools/control_ladder_gate.py`; **NEW fields** `control_methods` (top-level catalog), per-problem
`control_ladder` + `id` + `type`, `pesticide_safety_education` (top-level). COMMITTED UNPUSHED (Trevor
confirms push, coordinated with Utah).

**What shipped.** The first honest, softest-first IPM control ladder. Every pest/disease is no longer a
single treatment blob; it is (a) a stable kebab `id` (the vocabulary the next variety-resistance arc points
at), (b) a `type` (insect/fungal/bacterial/physiological/...), and (c) an ORDERED `control_ladder` whose
rungs reference a shared, authored-once `control_methods` catalog. The catalog = 24 methods across the 5 IPM
tiers (cultural 9 / physical 5 / biological 3 / soft_chemical 5 / conventional 2), each with dual-register
how-it-works, best_use, honest pros/cons/cautions, a beginner `find_it_beginner` shelf/brand line on the 10
purchasable methods, and T1 sources (`ucanr_ext`=UC IPM, `npic_orst`=NPIC OSU/EPA [new], `umn_ext`,
`umd_ext`, `clemson_hgic`, `psu_ext`, `msu_ext`). The `pesticide_safety_education` object carries the
universal responsible-use spine once. Pilot on broccoli (7 problems) + celery (7) + microgreens (2) = 16
ladders. Retires `organic_treatment_*` (broccoli/celery) + `management_*` (microgreens) into the ladder
rung notes.

**The honesty (the reason for the arc).** Conventional pesticides are named by active-ingredient class + a
common example ("a pyrethroid such as permethrin"; carbaryl) with the full caution set (kills bees +
beneficials, long residual, resistance, observe the pre-harvest interval, read the label) -- fair, not
demonized, and NOT brands (the `find_it_beginner` shelf lines handle recognition, including the Sevin
landmine: Sevin-5 dust is still carbaryl but many Sevin liquids are now zeta-cypermethrin, so read the
active ingredient). "Organic" is stated to NOT mean harmless: copper accumulates in soil + is highly toxic
to fish, sulfur burns foliage over 90degF + harms predatory mites, neem/spinosad harm bees while wet, Bt
kills all moth + butterfly larvae including swallowtails/monarchs. Ladders honestly STOP where no further
control applies: clubroot (no chemical cure -- rotation/lime/resistant varieties), celery blackheart
(physiological), pink-rot, both microgreens problems (raw crop, cultural-only), cabbage-root-maggot +
carrot-rust-fly (protected in roots -- exclusion only), celery leaf-miner (conservation-only; broad sprays
flare it). Exactly ONE conventional rescue rung: flea-beetle -> carbaryl (beetles are not predator-regulated
and can kill seedlings, so a labeled last-resort is honest here; rescue-only, spot-treat).

**Build (SDD).** control_ladder_gate built TDD across 4 tasks; the per-task review loop caught 3 genuine
plan bugs (kebab check wrongly on snake_case catalog keys; a KeyError-on-bad-tier that would have masked the
catalog violation; the identity check needed scoping to ladder-bearing problems so the SOFT gate is silent
on the 118 un-migrated crops). Catalog authored by an opus subagent from live-fetched T1 pages, then an
independent opus **T1-fidelity review CAUGHT an unsupported neem bee-toxicity caution** (its cited UC IPM
page rates neem LOW-tox to pollinators, contradicting the claim) + 3 lighter attribution gaps, all fixed.
Ladders authored by an opus subagent, then an independent horticulture review drove 3 fixes (the flea-beetle
rescue rung, a root-maggot collar rung grounded in broccoli's OWN sourced prevention prose after the general
UMN root-maggot page proved to carry only row cover, and fungus-gnat sticky traps) and confirmed the 7 other
no-conventional-rung omissions are each correctly honest. A sourcing trap was avoided: a WebSearch summary
claimed UMN recommends maggot collars, but fetching the actual page showed only row covers -- so the catalog
`stem_collars` method was NOT broadened on an unsupported general claim; the crop-specific ladder note
carries it instead, grounded in broccoli's certified prose.

**Gates / verification (protocol #6).** `gate_all` 119/119 (the whole suite on every certified crop),
`control_ladder_gate` 0 violations (24 catalog methods / 16 ladders live), `register_completeness` PASS (the
new keys were ruled into EXCLUDED_KEYS/PATH by the gate-phase task, so blob removal + new keys produced 0
unruled prose), **adversarial RED battery** injects 6 defect classes (dangling method ref, non-monotonic
tier, applies_to mismatch, duplicate id, bad-tier-no-crash, unknown-type-flag) into the REAL pilot shapes
and confirms every one bounces + clubroot's cultural-only ladder passes clean, `release_verify` clean except
the documented roster/multi-crop single-crop-pilot false positive (the pre-commit backstop is binding and
was green at every commit), consumer-copy sweep em-dash/double-hyphen/spelled-degrees 0 across catalog +
safety + the 3 crops, canonical COMPACT (0 escaped-unicode, no trailing newline), and every crop OTHER than
the 3 pilots is BYTE-IDENTICAL. Footprint EXACT: +`control_methods` (24) + `pesticide_safety_education` +
`source_catalog`+`npic_orst`, and only broccoli/celery/microgreens-mix `pests`/`diseases` changed; count 128
/ 119 certified unchanged (a new gate + new fields, NOT a new crop).

**Next / follow-ons.** NEXT ARC = variety resilience/disease-resistance (per-variety `resists:` /
`susceptible_to:` referencing these pest/disease `id`s -- the whole reason this arc was sequenced first).
The `control_ladder_gate` HARD-FLIP into A39 register-coverage + `gate_all` (with a coverage floor requiring
every certified problem to carry `id`+`type`+`control_ladder`) fires when the roster-wide rollout (~897
problems, family batches, catalog grows) reaches full coverage. Approach C (crop-level pest hub: management
philosophy + scouting calendar) = a future register row when a consumer pulls on it. plant-app honest IPM
pest guidance + any plant-astro rendering = a separate lane (after push). Deferred Minors: unused `os` import
in control_ladder_gate (cosmetic); all_violations composition is now exercised by the RED battery. Spec/plan
`docs/superpowers/{specs,plans}/2026-07-22-pest-ipm-ladder-*`; ledger `.superpowers/sdd/progress.md`; catalog
provenance `tools/staging/pest_pilot_catalog_sources.md`; horticulture/fidelity reviews inline (this notes
dir). >> **PEST/IPM PILOT SHIPPED -- 119 certified / 128 total** (new gate + new fields, no cert-count
change). << COMMITTED, UNPUSHED (Trevor confirms push).
```

---

## 3. CURRENT_STATE.md -- PREPEND this bold-SHA entry as the new top entry (a new line 3, ABOVE the current `**`2c98dd2b` (2026-07-22) -- UTAH DIXIE ...` entry). Single dense paragraph, matching the house format:

```
**`4f7789aa` (2026-07-22) -- PEST/IPM CONTROL-LADDER PILOT SHIPPED -- field-addition register row 23, the FIRST honest IPM control-ladder foundation, layered on Utah Dixie (`2c98dd2b` -> `b4bb71b` catalog -> `a1755b0` safety -> `857a856` ladders -> `4f7789aa`; register row 23 `669a681`; count 128 / 119 certified unchanged, a NEW gate + NEW fields, NOT a new crop).** Adds a shared top-level `control_methods` catalog (24 methods across the 5 IPM tiers cultural/physical/biological/soft_chemical/conventional, authored-once + referenced by id, mirrors `source_catalog`; T1 `ucanr_ext`/`npic_orst`[new NPIC]/`umn_ext`/`umd_ext`/`clemson_hgic`/`psu_ext`/`msu_ext`), a per-problem `control_ladder` (flat ORDERED softest-first `{method,note_*}`), a stable per-problem `id` (kebab; the vocabulary the NEXT variety-resistance arc references) + `type`, and a new top-level `pesticide_safety_education` (label-is-the-law/PHI/pollinator/PPE/resistance, mirrors soil_education/ph_education). Retires the old `organic_treatment_*`/`management_*` treatment blobs into the ladder rung notes. **Pilot = broccoli (7) + celery (7) + microgreens (2) = 16 ladders.** NEW standalone `control_ladder_gate` (TDD, SOFT, scoped to ladder-bearing problems): referential (method exists) + monotonic-tier + applies_to coherence + unique kebab id; the gate-phase task ruled the new keys into `register_completeness` EXCLUDED_KEYS/PATH; **A39 register-coverage HARD-FLIP deferred to the roster-wide rollout** (~897 problems, family batches). **HONESTY (the point):** conventional named by active-ingredient class + example ("a pyrethroid such as permethrin"; carbaryl) with the full caution set (bees/fish/cat-or-earthworm/long-residual/resistance/PHI/read-the-label), fair not demonized, NOT brands (the beginner `find_it_beginner` shelf line handles recognition + the Sevin landmine: Sevin-5 dust still carbaryl, many Sevin liquids now zeta-cypermethrin); "organic isn't harmless" stated candidly (copper soil-accumulation + fish toxicity, sulfur >90degF foliage burn + predatory-mite harm, neem/spinosad bee-harm-while-wet, Bt kills all lepidoptera larvae incl swallowtails/monarchs); honest short/cultural-only ladders where no spray applies (clubroot [no chemical cure]/blackheart [physiological]/pink-rot/microgreens [raw crop]/cabbage-root-maggot + carrot-rust-fly [root-protected, exclusion only]/celery leaf-miner [conservation-only, sprays flare it]); exactly ONE conventional rescue rung (flea-beetle -> carbaryl, beetles not predator-regulated + can kill seedlings, rescue-only/spot-treat). **BUILD (SDD):** control_ladder_gate built TDD across 4 tasks (the per-task review loop caught 3 genuine plan bugs: kebab-on-snake catalog keys, KeyError-on-bad-tier masking the catalog violation, identity-needs-scoping so the SOFT gate is silent on the 118 un-migrated crops); catalog authored by an opus subagent from live-fetched T1 pages then an independent opus **T1-fidelity review CAUGHT an unsupported neem bee-toxicity claim** (cited UC IPM rates neem low-tox) + 3 attribution gaps, all fixed; ladders authored by an opus subagent then a horticulture review drove 3 fixes (flea-beetle rescue rung, root-maggot collar grounded in broccoli's OWN sourced prose after a WebSearch summary falsely claimed a UMN maggot-collar page -- fetch showed only row cover, so the catalog method was NOT broadened on an unsupported claim, avoiding a fabrication trap; fungus-gnat sticky traps) + confirmed the 7 other no-conventional omissions are each correctly honest. **GATES:** `gate_all` 119/119, `control_ladder_gate` 0, `register_completeness` PASS, adversarial RED battery (6 defect classes bounce on REAL shapes + clubroot passes clean), `release_verify` clean except the documented multi-crop single-crop-pilot false positive (pre-commit backstop binding, green at every commit), consumer sweep em-dash/dbl-hyphen/spelled-degrees 0, canonical COMPACT (0 escaped-unicode), crops-elsewhere BYTE-IDENTICAL. Spec/plan `docs/superpowers/{specs,plans}/2026-07-22-pest-ipm-ladder-*`; ledger `.superpowers/sdd/progress.md`; catalog provenance `tools/staging/pest_pilot_catalog_sources.md`. **NEXT ARC = variety resilience/disease-resistance** (per-variety `resists:`/`susceptible_to:` referencing these pest/disease `id`s -- the reason this arc was sequenced first); Approach C (crop-level pest hub) = a future row; plant-app IPM consumption + plant-astro = separate lane after push. >> **PEST/IPM PILOT SHIPPED -- 119 certified / 128 total** (new gate + new fields, no cert-count change). << COMMITTED, UNPUSHED (Trevor confirms push); layered on Utah Dixie `2c98dd2b`; NO plant-astro bump from this session. Prior steps below.
```

---

## Merge / release checklist (coordinated with the Utah session)

1. Confirm canonical SHA is still `4f7789aa` (pest arc) at release time; if the Utah session pushed or moved
   the canonical first, re-verify (`gate_all`, `control_ladder_gate`, footprint) and refresh the SHA above.
2. LATEST.txt -> replace with section 1 (records the PEST arc as the head state; Utah `2c98dd2b` is now a
   prior layer captured in the STATE_HISTORY stack).
3. STATE_HISTORY.md -> prepend section 2 above the Utah entry (append-only; most-recent first).
4. CURRENT_STATE.md -> prepend section 3 above the Utah entry (hand-maintained; NEVER regen -- drift memory).
5. Push both arcs together (Trevor confirms). NO plant-astro bump from these sessions (astro owns it).
