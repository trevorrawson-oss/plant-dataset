# Dry-Bean Variety Pilot -- Design Spec (Spec 1 of 2)

- **Date:** 2026-07-11
- **Status:** design, pending Trevor review
- **Canonical at design time:** `3b2674b3` (count 125, 116 certified)
- **Arc:** variety-DTM load-bearing + Phase 4 variety expansion, piloted on `dry-bean`
- **Related memory:** `variety-dtm-load-bearing-deferred`, `master-crop-list-phase4-inventory`,
  `planner-data-model-arc`, `timing-spine-authoring`

---

## 1. Context and goal

Trevor wants to "knock out our first set of varieties, starting with dry beans." Two threads
converge here:

1. **Phase 4 variety expansion** -- author real per-variety content (the master crop list inventory).
2. **Variety-DTM load-bearing** (deferred by decision 2026-07-07) -- make the selected cultivar's
   `days_to_maturity` an authoritative field the app can eventually recompute timing from, instead of
   only the crop baseline.

For `dry-bean` these collapse into one job. The crop already ships the exact 5 varieties the master
crop list names (Black Turtle, Pinto, Navy, Kidney, Jacob's Cattle), each with a `days_to_maturity`
and a single `note`. So **breadth is already done**; the work is **depth** (enrich each variety to
"full treatment") plus **locking the contract** that governs the eventual roster-wide rollout.

`dry-bean` is the natural pilot: freshly certified, direct-sown (`dtm_anchor: "from_sow"`, so variety
DTM is cleanly "days from sowing"), and it already carries structured variety objects with DTM. This
is the "~10-variety GS-arc pilot" the deferred-arc memory called for.

## 2. Two-spec decomposition

This project is too large for one spec. It decomposes into:

- **Spec 1 (this doc) -- dry-bean variety pilot.** Lock the per-variety schema + contract, enrich
  dry-bean's 5 varieties to full treatment, build the **soft** variety gate (coverage-reporting,
  non-blocking, TDD). Deliverable: dry-bean content + new standalone gate + this contract.
- **Spec 2 (later) -- rollout + hard gate + app handoff.** Roll the schema across the 30 string-list
  crops and the ~280 DTM-less variety entries (a column pass against a stable roster), flip the gate
  into the A39 register-coverage hard floor, and hand a kickoff to the plant-astro session for
  variety-driven timing (region x variety). App timing recompute lives in plant-astro, not here.

## 3. Governing principles (the contract)

### 3.1 Variety as a sparse override layer
For every datapoint the crop tracks, a variety records its own value **only where it genuinely
differs** from the crop default; otherwise it inherits. Kidney overrides `days_to_maturity` (100) and
`seed_size` (large) because it differs; it inherits the crop's spacing and watering because it does
not. This keeps varieties from bloating with copies of the crop default and makes "override wherever
they differ" the rule.

- **Load-bearing overrides** drive a computation. In the pilot, **`days_to_maturity` is the one
  load-bearing override** -- the app recomputes the harvest date from it.
- **Descriptive overrides** are shown for selection but drive no computation:
  `maturity_class`, `seed_color`, `seed_size`, `plant_habit`, `primary_use`, `seed_type`.
- `plant_habit` (bush vs pole) is the next load-bearing candidate (it decides trellis/support), but
  is descriptive for now.

### 3.2 Source-authoritative DTM
**A T1 source is the authority for a variety's DTM. A gate that rejects a legitimately-sourced value
is the broken thing -- not the data.** Therefore:

- Encoding is **absolute** (Black Turtle = 100, as today; no delta, no migration).
- The **only HARD bound** is the existing `numeric_sanity_gate` (A33) `[7, 400]` -- the garbage
  catcher (typo'd 850-day bean).
- **Crop-band coherence is advisory only.** The soft check fires **only when a value is both
  out-of-band AND unsourced.** A T1-anchored value never flags, no matter how far outside the band.
  So Navy@85 (below the crop's `[90,100]` min) is silent the moment it carries its UC anchor.
- If several sourced varieties keep landing below the band, that is *evidence* the ratified crop band
  is too tight -- but we do **not** touch the crop band in Spec 1; the advisory absorbs Navy.

### 3.3 DTM-anchor inheritance
A variety's `days_to_maturity` **inherits the crop's `dtm_anchor`; it never redefines it.** Catalog
DTM means "days from sowing" for direct-sown crops but "days from transplant" for started crops, and
the crop already carries `dtm_anchor` (`from_sow` / `from_transplant`) to disambiguate. dry-bean is
`from_sow`, so this is clean here -- but the rule must be stated so Spec 2's load-bearing recompute is
correct the first time it hits a transplanted crop. No new field; a stated rule.

### 3.4 Load-bearing model (what "load-bearing" means)
The crop's `days_to_maturity` band (`[90,100]`) is the **default/range** shown when no cultivar is
selected. The selected variety's DTM **overrides** it: `harvest = sow_date + variety.days_to_maturity`
(interpreted against `dtm_anchor`). Crop band = default; variety = truth. The app-side override lands
in Spec 2 (plant-astro).

### 3.5 Soft-gate lifecycle and safety (two invariants)
The pilot gate is soft (section 6). Soft is the correct de-risking choice -- a *hard* variety-detail
requirement today would go RED across the mid-flight roster and would block the corn family (and every
new crop) from certifying until full variety detail were authored, which is bolting an unfinished field
onto cert. But "soft" only stays safe if it is not left open-ended. Two invariants guard it:

- **INV-1 (no open-ended soft):** the field-addition register row carries an **explicit hard-flip
  trigger** -- when the Spec-2 rollout column pass completes, the gate joins the A39 register-coverage
  hard floor + `gate_all`. Soft is a stage, not a resting state. (Precedent: `timing_spine_gate` was
  soft and *did* fold into A39 as register #8.)
- **INV-2 (validation precedes load-bearing consumption):** the app MUST NOT consume a crop's variety
  DTM as *load-bearing* (i.e. compute a user-facing harvest date from it) until that crop's variety
  data is gate-clean -- ideally not until the gate is hard. While the gate is soft, the only hard
  guarantee on a variety DTM is the A33 `[7,400]` floor, so a sourced typo (Navy@185) could otherwise
  reach a user. This is a sequencing rule on the Spec-2 plant-astro handoff, not a Spec-1 deliverable.

### 3.6 Prior art: existing variety models (the pilot is FLAT, not delta)
Plan grounding surfaced ~5 coexisting variety shapes in the roster today, plus a separate
`varieties_detail[]` field on 26 tree/berry crops. Notably, 10 crops (5 citrus + 5 woody herbs) carry
an exploratory **`delta{value, parent, changed}` override overlay** (June 2026 lemon/lavender work).
Trevor's call 2026-07-11: that delta model was **idea-building, not a committed convention** -- do NOT
adopt or extend it.

**Decision: flat, self-contained per-variety values, override-by-ABSENCE.** A load-bearing value must
be the actual value the app uses, not a diff resolved against a parent. The `delta` structure stores a
cached `parent` copy inside each variety (drifts stale) and forces read-time resolution -- a crop-default
edit would silently shift every variety's effective DTM. Flat storage keeps the good half of the
"override where they differ" principle (section 3.1) via ABSENCE -- a variety omits the fields it does
not override and inherits the crop default -- without the fragile half. A "differs from default" UI cue,
if ever wanted, is DERIVED at render time (compare variety value to crop value), never stored.

The five shapes, for the record (reconciled in Spec 2): 37 simple `{name, days_to_maturity, note}`
(dry-bean's own group); 30 plain name-strings; 10 exploratory `delta`; 39 assorted
`{name, recommended_note, ...}` / tree-bloom; + `varieties_detail[]` on 26 trees/berries. The Full-T1
schema (section 4) is a clean SUPERSET of dry-bean's own simple-DTM shape, so the pilot extends dry-bean
without conflict; the fragmentation is a rollout problem, not a pilot problem.

## 4. Per-variety schema (Full T1)

| field | type | required | notes |
|---|---|---|---|
| `id` | string (slug) | yes | **Stable key**, e.g. `black-turtle`. Never changes even if `name` does. The persistence anchor for a user's saved variety selection. |
| `name` | string | yes | Display name, e.g. `Black Turtle`. |
| `days_to_maturity` | int | yes* | Absolute, load-bearing, T1-anchored. Inherits crop `dtm_anchor`. (*Present when a real day-count exists; absent for season-only crops -- see `maturity_class`.) |
| `maturity_class` | enum `early`\|`mid`\|`late` | yes | **Universal timing class**, present on every variety. For DTM crops it is the coarse label layered under the precise number; for season-only crops (trees/berries, Spec 2) it is the *primary* timing field and `days_to_maturity` is absent. This unifies the old `dtm_class`/`season` split into one field. |
| `seed_type` | enum `open_pollinated`\|`hybrid`\|`heirloom` | yes | Can I save seed, or is it an F1 I must re-buy? `heirloom` implies open-pollinated (seed-saveable); it is the historically-stable subset. |
| `seed_color` | string | yes | Open-ended (colors do not enumerate cleanly). |
| `seed_size` | enum `small`\|`medium`\|`large` | yes | |
| `plant_habit` | enum `bush`\|`half_runner`\|`pole` | yes | |
| `primary_use` | enum `soup`\|`baked`\|`chili`\|`fresh_shell`\|`multi` | yes | |
| `is_reference` | bool | yes | **Exactly one `true` per crop** (the flagship). dry-bean flagship = Black Turtle. |
| `confidence_tier` | enum `T1`\|`T2`\|`T3`\|`T4` | yes | Honest per-variety confidence. Mixed tiers within a crop are allowed. |
| `note_beginner` | string | yes | Dual-register per-variety prose (warm, one teaching aside). |
| `note_seasoned` | string | yes | Dual-register per-variety prose (terse, mechanistic). |
| `sources` | [catalog id] | yes | T1 source ids backing the row (esp. the DTM). |
| `anchoring_urls` | {id: {url, verified}} | yes | Per-source URL + verification date. |
| `disease_notes` | string | optional | Present only when there is a real T1 fact (e.g. white-mold susceptibility). |
| `regional_fit` | string | optional | Present only when a variety has a real regional angle (e.g. "short-season northern gardens"). |

The four decisions locked in review: **`id`** (stable selection key), **`seed_type`** (OP/hybrid/
heirloom), **`maturity_class`** (unifies `dtm_class`+`season`), and **`dtm_anchor` inheritance**
(section 3.3). Deliberately left OUT as YAGNI: structured disease-resistance codes (prose suffices for
the pilot) and a computed crop-band envelope (Spec 2+ question).

## 5. Dry-bean variety content (the 5)

Enrich all 5 to Full T1 in the sparse-override shape. Current DTMs, to be verified against a T1 UC
source (source wins; keep the sourced value even if it sits outside `[90,100]`):

| id | name | DTM | maturity_class | seed_type | seed_size | habit | use | flagship |
|---|---|---|---|---|---|---|---|---|
| `black-turtle` | Black Turtle | 100 | late | (verify) | small | bush | soup | **yes** |
| `pinto` | Pinto | 90 | mid | open_pollinated | medium | half_runner | multi | no |
| `navy` | Navy | 85 | early | open_pollinated | small | bush | baked | no |
| `kidney` | Kidney | 100 | late | open_pollinated | large | bush | chili | no |
| `jacobs-cattle` | Jacob's Cattle | 90 | mid | heirloom | medium | bush | multi | no |

(Trait values above are the working hypothesis from existing notes; each is confirmed or corrected
against the T1 source during authoring. `maturity_class` must cohere with DTM -- Navy@85 is the
fastest, so `early`; Kidney/Black-Turtle@100 are `late`.)

Sourcing: anchor each DTM to a T1 UC source (UC Davis dry-bean type classing / UC ANR dry-bean
production -- the existing notes already cite "UC Davis classes black beans as late" and "UC Davis:
large-white types ~75 to 90 days"). One new `source_catalog` id may be required for the specific
dry-bean variety/type table; add it if so. All prose original (17 USC 102(b)/Feist), dry-bean voice,
no em dashes, American English, temps as `°F`.

## 6. The soft variety gate

New standalone tool `tools/variety_detail_gate.py` (+ `tools/test_variety_detail_gate.py`),
**modeled on `timing_spine_gate.py`**: fires-when-present, prints a **coverage report**, and **does
not block certification in the pilot.** It is NOT wired into a `whole_crop_gate` A-number yet; the
hard-flip into the A39 register-coverage floor is Spec 2, after rollout.

Checks (all soft in the pilot):

- **Presence** of each required field per variety (section 4).
- **Enum validity:** `maturity_class` in {early,mid,late}; `seed_type` in {open_pollinated,hybrid,
  heirloom}; `seed_size` in {small,medium,large}; `plant_habit` in {bush,half_runner,pole};
  `primary_use` in {soup,baked,chili,fresh_shell,multi}; `confidence_tier` in {T1,T2,T3,T4}.
- **`is_reference`:** exactly one `true` per crop.
- **`id`:** present, slug-shaped, unique within the crop.
- **DTM:** present + integer (hard `[7,400]` stays with A33; the gate confirms presence, not the
  bound).
- **Advisory coherence #1 (crop-band):** a variety DTM outside crop `[min,max] ± margin` **AND**
  lacking a per-variety source -> WARN in the coverage report (never fail). Margin default ~±10; a
  low-stakes tunable. Since every pilot variety is sourced, this does not fire on dry-bean.
- **Advisory coherence #2 (class/DTM):** the fastest variety in a crop should not be `late` and the
  slowest should not be `early` (Navy@85 = early, Kidney@100 = late). WARN only.

**TDD, RED before GREEN, adversarially proven on a scratch copy of the real canonical:** bad enum,
missing dual-register note, two `is_reference`, absurd/`[7,400]`-violating DTM, an *unsourced*
out-of-band value, and a class/DTM mismatch each surface before the gate is trusted.

**Companion gate change (REQUIRED, or the splice fails `gate_all`):** the new per-variety STRING keys
(`id`, `seed_type`, `maturity_class`, `seed_color`, `seed_size`, `plant_habit`, `primary_use`,
`confidence_tier`, and optional `disease_notes`/`regional_fit`) will trip `register_completeness`'s
C11/A25 "any unruled non-empty string" check and flood the gate -- exactly what sweet-corn's
`planting_layout` needed a sanctioned ruling for. Add path-guarded entries to
`register_completeness_gate.py` `ruled_categorical()` (the same mechanism that already rules
`varieties.recommended[].use`/`.note`/`.hardiness_note`), scoped to the `varieties.recommended` path,
each with a one-line Trevor-ruling comment in the house style. `is_reference` (bool),
`days_to_maturity` (int), `sources` (list), and `note_beginner`/`note_seasoned` (auto-ruled by suffix)
need no ruling. This is its own TDD RED->GREEN change with a regression assert, landed BEFORE the
content splice.

## 7. Authoring and release plan

1. Build the soft gate first (TDD), RED-proven on a scratch copy.
2. Author the 5 dry-bean varieties to Full T1; verify each DTM + trait against its T1 UC source.
3. **SHA-guarded COMPACT splice** (via `tools/apply_patch.py`): exactly dry-bean's `varieties` object
   changes; all 124 other crops byte-identical; count 125; COMPACT (`separators=(",",":")`,
   `ensure_ascii=False`, no trailing newline); footprint audited.
4. Release gates (protocol #6): `whole_crop_gate` dry-bean PASS, `gate_all` PASS (116 certified
   unchanged), `variety_detail_gate` coverage report, `release_verify` no new violations, per-batch
   source-truth sample.
5. **State trio:** regenerate/patch CURRENT_STATE.md, append STATE_HISTORY.md (most-recent first),
   bump LATEST.txt. Trevor confirms the push (dataset commits go on `main`; no plant-astro bump from
   this session).

## 8. Field-addition register entry

Add a new row to `docs/field_addition_register.md` for the variety-detail bundle (the schema in
section 4), per CLAUDE.md's "Adding a cross-crop field." Trigger/rollout = Spec 2 (roster-wide column
pass against a stable roster; hard-flip into A39 only after rollout completes). The pilot is a
single-crop GS-arc pilot, explicitly not the column pass.

The register row MUST state an **explicit hard-flip trigger** (INV-1, section 3.5): *"flip the
`variety_detail_gate` from soft/standalone into the A39 register-coverage hard floor + `gate_all` when
the Spec-2 rollout column pass reaches full-roster coverage."* This keeps the soft stage bounded and
prevents the "soft becomes permanent" drift where new crops certify with malformed variety data caught
only by an unread coverage report.

## 9. Scope boundaries (explicitly OUT of Spec 1)

- **Reconciling the 5 existing variety shapes** (section 3.6): the 30 string-list crops, the ~280
  DTM-less entries, the 39 assorted `recommended_note` shapes, folding in `varieties_detail[]` (26
  trees/berries), and migrating or retiring the 10 exploratory `delta` crops -> all Spec 2 (the column
  pass that touches every crop anyway).
- The app variety-driven timing recompute and region x variety feature (-> plant-astro, Spec 2).
  **Handoff carries INV-2 (section 3.5): plant-astro must not consume a crop's variety DTM as
  load-bearing until that crop's variety data is gate-clean / the gate is hard.**
- Flipping the gate into the A39 hard cert floor (-> Spec 2, post-rollout, per INV-1).
- Authoring season-only varieties for trees/berries (-> Spec 2; the schema *permits* them now via
  `maturity_class` with absent DTM).
- Touching the Trevor-ratified crop DTM band `[90,100]` (the advisory absorbs Navy@85).

## 10. Reserved seam for the planner arc

The planner arc (`planner-data-model-arc`: take `planting_layout` roster-wide + add `row_spacing` +
`height`/`spread`) runs **after** varieties. This spec reserves the seam so it slots in cleanly:

- `planting_layout` and `row_spacing` are **crop-level** (variety-independent) -- planner authors them
  at the crop.
- `height` and `spread` are **anticipated variety override fields** -- when the planner arc adds them,
  they follow the section-3.1 sparse-override rule (crop default, variety overrides where a dwarf or
  sprawling cultivar differs). Building the override model first means the planner authors
  override-capable height/spread on day one instead of eating a retrofit.

## 11. Success criteria

- All 5 dry-bean varieties carry the full section-4 schema, each DTM T1-anchored, each with an
  honest `confidence_tier`.
- `variety_detail_gate` PASS/coverage-clean on dry-bean; adversarial RED proof recorded.
- Canonical footprint = exactly dry-bean's `varieties` object; count 125; COMPACT; `gate_all`
  116 certified unchanged; `release_verify` no new violations.
- Contract (sections 3-4) is written such that Spec 2's rollout and the planner arc both inherit the
  override + source-authoritative rules without renegotiation.

## 12. Open items to confirm during authoring

- The exact T1 source id(s) for dry-bean variety DTM (reuse an existing UC catalog id or add one).
- `seed_type` per variety (Black Turtle OP-vs-heirloom is the one judgment call; the rest are clear).
- Whether all 5 reach T1 or some land honestly at T2 (recorded in `confidence_tier`, not forced).
