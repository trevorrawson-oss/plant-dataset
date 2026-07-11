# Apple Variety Pilot -- Design Spec (the TREE archetype)

- **Date:** 2026-07-11
- **Status:** design, pending Trevor review
- **Canonical at design time:** `340c2983` (count 125, 116 certified)
- **Arc:** variety-DTM load-bearing + Phase 4 variety expansion -- the **tree-fruit** archetype pilot,
  immediately after the **dry-bean variety pilot** (Spec 1 of the variety arc, canonical `340c2983`).
- **Kickoff:** `docs/kickoffs/23-apple-variety-pilot-tree-archetype.md`
- **Related memory:** `apple-variety-pilot-tree-archetype`, `variety-dtm-load-bearing-deferred`,
  `trevor-north-star-accuracy-authority`, `d8-heat-pause-variety-pass-commitment`
- **Related spec:** `docs/superpowers/specs/2026-07-11-dry-bean-variety-pilot-design.md`
- **Model doc:** `docs/tree_region_model_scope_v0.md`

---

## 1. Context and goal

Dry-bean proved the flat per-variety schema on the **DTM-annual** archetype: a direct-sown crop whose
timing is a day-count from sowing. Apple is the **tree-fruit** archetype -- structurally different in
three ways that break the annual model:

- **No days-to-maturity.** Trees are grafted and perennial; timing is a bloom *window* plus a harvest
  *season*, not a countdown from a sow date.
- **Chill dependence.** A variety only fruits where winter delivers enough chill hours; the same tree
  that thrives in Minnesota will never fruit in the Arizona low desert.
- **Cross-pollination.** Most apples are self-unfruitful and need a second, genetically different,
  bloom-overlapping variety nearby -- and some varieties (triploids) have sterile pollen and cannot
  serve as that partner at all.

Trevor's product driver: the app's **cross-pollination "bloom calendar"** -- which apples to plant
together so they actually set fruit -- is currently **generic**. He wants it to pull the right bloom
dates for each region *from the varieties*, and to **be honest**: say "won't fruit here" rather than
fake a date. North star = accuracy + trust + being the authority
(`trevor-north-star-accuracy-authority`).

Proving the tree archetype here is what unlocks the Spec-2 roster-wide rollout. The rollout is **not**
one uniform sweep: the roster carries 5+ coexisting variety shapes, and the tree lane is the hard one.
Apple is where we prove it before scaling.

## 2. Where apple sits (not greenfield)

Apple already carries most of the bloom model; this pilot enriches and *sources* it, and builds the
schema + gate that make it load-bearing. Confirmed by inspection of canonical `340c2983`:

- **Per-variety (13 recommended; `varieties_detail[]` is empty):** every variety carries `bloom_group`
  (`very_early`..`very_late`), `bloom_window_relative` (`[start,end]` as a **fraction of the regional
  bloom season**, e.g. Honeycrisp `[0.38,0.55]`, Dorsett Golden `[0.0,0.14]`, Pink Lady `[0.74,0.92]`),
  `bloom_duration_days`, `chill_hours_required`, `use`, `recommended_note` (all null today).
- **Per-region / per-zone:** `regions.<r>.resolved_by_zone.<z>.bloom` = real dates (northern_tier z5 =
  "Apr 25 - May 15") + `resolved_from.chill_hours` = chill **delivered**. 8 of 10 regions resolve apple
  bloom; **`fl_peninsula` and `hawaii_tropical` resolve zones but carry no bloom anchor** (a live
  thin-data case, section 5).
- **Crop-level `pollination`:** `self_fertile:false`, `needs_pollinizer:true`,
  `pollinizer_distance_ft:50`, dual-register notes naming the triploids (Mutsu / Jonagold / Shizuka =
  sterile pollen) -- but **no variety carries a machine-readable triploid flag**, and there is **no
  crabapple** in the roster.

Two sourcing gaps this pilot must close (section 6): the per-variety `bloom_group`/`chill_hours_required`
values carry **no per-variety source** today (only one coarse crop-level list), and the region bloom
anchors rest on a **single generic rule** (bloom approximately last_frost + 7 days, 21-day window,
cited to one `apples.extension.org` page) rather than region-specific bloom records.

## 3. Governing principles (the contract)

The dry-bean contract carries over unchanged where it is archetype-neutral; this section states what
is inherited and what the tree archetype adds.

### 3.1 Flat, sparse override-by-ABSENCE (inherited)
A variety stores its own value only where it genuinely differs from the crop default; otherwise it
inherits by omission. No `delta{value,parent,changed}` overlay (the exploratory June-2026 model is
retired, per dry-bean 3.6). A load-bearing value is the actual value the app uses, never a diff
resolved against a parent. A "differs from default" UI cue, if ever wanted, is derived at render time,
never stored.

### 3.2 Source-authoritative, T1-or-it-does-not-ship (inherited + tightened)
A T1 source is the authority for a load-bearing number. The tree archetype's load-bearing honesty
numbers -- per-variety `chill_hours_required` and `bloom_group`, and each region's bloom anchor -- each
carry a per-datapoint T1 anchor **or they do not ship as load-bearing** (section 6). This is stricter
than dry-bean's single DTM anchor because the honesty engine (section 5) computes user-facing "won't
fruit here" verdicts directly from these numbers.

### 3.3 Common core + dispatched archetype block (new -- the schema refactor)
The per-variety schema splits into a **universal common core** carried by every variety of every
archetype, plus exactly one **archetype block** selected by the crop's declared `variety_archetype`.
Dry-bean's bean-trait fields (`seed_type`/`seed_color`/`seed_size`/`plant_habit`/`primary_use`) become
**archetype-required, not universal**; the tree block replaces them with bloom/chill/triploid fields.
Full schema in section 4.

### 3.4 `variety_archetype` dispatch, annual-default (new)
A crop declares `variety_archetype` at the crop level. **Absence defaults to `annual_dtm`**, so
dry-bean stays byte-identical through the apple splice; **apple declares `variety_archetype:
"tree_fruit"`.** The gate reads this key to select the required archetype block. Making
`variety_archetype` explicit across the whole roster is a Spec-2 reconciliation step; in the pilot,
only apple declares it. Gate opt-in stays "a variety carries `maturity_class`" (section 7), so the
un-migrated roster remains silent and green.

### 3.5 `maturity_class` is universal but archetype-scoped in meaning (new nuance)
`maturity_class` (enum `early`|`mid`|`late`) is common-core -- present on every variety -- but its
**referent differs by archetype**. For `annual_dtm` it is the coarse label layered under the precise
`days_to_maturity`. For `tree_fruit` it is the **ripening / harvest season**, and it is kept
semantically **distinct from `bloom_group`**: bloom time and ripening time do not track (McIntosh
blooms early and ripens early-to-mid; Pink Lady blooms very-late and ripens very-late). The gate
validates the shared enum; the meaning is documented per archetype.

### 3.6 Soft-gate lifecycle (inherited invariants)
- **INV-1 (no open-ended soft):** the field-addition register row carries an explicit **hard-flip
  trigger** -- the tree-block checks fold into the A39 register-coverage hard floor + `gate_all` when
  the Spec-2 rollout column pass reaches full-roster coverage. Soft is a stage, not a resting state.
- **INV-2 (validation precedes load-bearing consumption):** plant-astro MUST NOT consume a crop's
  variety bloom/chill as load-bearing (compute a user-facing bloom date or "won't fruit here" verdict)
  until that crop's variety data is gate-clean. Sequencing rule on the Spec-2 app handoff.

## 4. Per-variety schema (common core + archetype blocks)

### 4.1 Universal common core (every variety, every archetype)

| field | type | required | notes |
|---|---|---|---|
| `id` | string (slug) | yes | Stable selection key, e.g. `golden-delicious`. Never changes even if `name` does. |
| `name` | string | yes | Display name, e.g. `Golden Delicious`. |
| `maturity_class` | enum `early`\|`mid`\|`late` | yes | Universal timing class; archetype-scoped meaning (section 3.5). |
| `is_reference` | bool | yes | Exactly one `true` per crop (the flagship). Apple = **Golden Delicious**. |
| `confidence_tier` | enum `T1`\|`T2`\|`T3`\|`T4` | yes | Honest per-variety confidence; mixed tiers within a crop allowed. |
| `note_beginner` | string | yes | Dual-register per-variety prose (warm, one teaching aside). |
| `note_seasoned` | string | yes | Dual-register per-variety prose (terse, mechanistic). |
| `sources` | [catalog id] | yes | Per-variety T1 source ids backing the load-bearing numbers. |
| `anchoring_urls` | {id: {url, verified}} | yes | Per-source URL + verification date. |
| `disease_notes` | string | optional | Present only for a real T1 fact (e.g. Liberty scab immunity). |
| `regional_fit` | string | optional | Present only for a real regional angle (e.g. "low-chill; warm-winter regions"). |

### 4.2 Annual-DTM archetype block (dry-bean; unchanged, now archetype-required not universal)

`days_to_maturity` (int, load-bearing, inherits crop `dtm_anchor`), `seed_type`
(`open_pollinated`|`hybrid`|`heirloom`), `seed_color` (string), `seed_size` (`small`|`medium`|`large`),
`plant_habit` (`bush`|`half_runner`|`pole`), `primary_use` (`soup`|`baked`|`chili`|`fresh_shell`|`multi`).

### 4.3 Tree-fruit archetype block (apple; new)

| field | type | required | notes |
|---|---|---|---|
| `bloom_group` | enum `very_early`\|`early`\|`mid`\|`late`\|`very_late` | yes | Relative bloom-time class. **T1-sourced.** |
| `bloom_window_relative` | `[start,end]`, floats in [0,1], start<end | yes | Fraction of the regional bloom season. **Derived** from `bloom_group` (section 5), not independently sourced. |
| `bloom_duration_days` | int > 0 | yes | Days the variety stays in bloom. |
| `chill_hours_required` | int > 0 | yes | Winter chill the variety needs to fruit. **T1-sourced.** The honesty engine's viability input. |
| `use` | string | yes | Culinary use (fresh eating / sauce / cooking / cider / storage). Free-text (tree uses do not enumerate cleanly). |
| `triploid` | bool | yes | Sterile pollen: cannot serve as a pollinizer and needs two partners. Today only in crop prose. |
| `self_fruitful` | enum `no`\|`partial`\|`yes` | optional | Override of crop `self_fertile`; present only where a variety differs (Golden Delicious = `partial`). Inherits `no` by absence. |

**No `days_to_maturity`** in the tree block -- grafted, season-only; this is exactly the season-only
path the unified `maturity_class` was built for (dry-bean 4). The annual-block bean traits are N/A here.

## 5. The honesty engine (data contract; consumption is Spec 2 / plant-astro)

Four rules, all **computed at render, nothing derived stored** (dry-bean 3.1). This spec defines the
data + rules; the computation lands in plant-astro under INV-2.

1. **Actual per-region bloom** = region/zone bloom anchor start + `bloom_window_relative` x season
   length. This is literally "pull the right dates for each region from the varieties."
2. **Cross-pollination** = two varieties whose *actual regional* windows overlap (Gala `[0.4,0.57]` and
   Honeycrisp `[0.38,0.55]` overlap; Dorsett `[0.0,0.14]` and Pink Lady `[0.74,0.92]` do not).
3. **Chill viability** = delivered regional chill >= variety `chill_hours_required`. When it fails, the
   app renders a positive honest fact: **"won't fruit here -- needs ~N chill hours, this region delivers
   ~M"** (McIntosh @900 in the low desert). A confident negative, not missing data.
4. **Triploid exclusion + self-fruitfulness** = a `triploid:true` variety is never offered as a
   pollinizer and itself needs two compatible partners; the app honors `self_fruitful`
   (`partial`/`yes` softens or removes the "needs a partner" requirement) and the crop-level
   `self_fertile`/`needs_pollinizer`.

**`bloom_window_relative` is a documented derivation, never labeled sourced.** No T1 source states
"Honeycrisp blooms at 0.38-0.55 of the season"; that fraction is *our* uniform encoding of the sourced
`bloom_group` onto the regional bloom season. The spec sources the *inputs* (`bloom_group` + `chill`)
and documents the `bloom_group` -> fraction mapping so the window is reproducible from sourced facts.
The existing 13 already sit in a clean monotonic ladder (very_early low-start .. very_late high-start);
the mapping formalizes that ladder.

**Thin-data posture (posture A -- explicit + honestly distinguished):**
- **Chill can't be met** (we *know* it fails): render the "won't fruit here" fact (rule 3).
- **No sourced bloom anchor for a region** (we *don't know* the dates): render "bloom dates not
  established for this region yet" -- never a faked date, never a silent drop. Live cases in the data:
  `fl_peninsula`, `hawaii_tropical` (both sub-chill regions where apples largely will not fruit anyway,
  so the message is coherent). The data must let the app distinguish "no anchor" from "anchor exists,"
  which the region model already supports.

## 6. Sourcing contract + sign-off gate

Every load-bearing honesty number carries a per-datapoint anchor: per-variety `chill_hours_required` +
`bloom_group`, and each region's bloom anchor.

- **T1 ships automatically** (the trusted default; no per-source sign-off).
- **Non-T1 requires Trevor's sign-off.** Where no T1 source exists, the datapoint goes on a **source
  manifest** (datapoint -> variety/region -> proposed source id, tier, URL, exactly what it backs),
  surfaced to Trevor **before the content splice**. He approves ship-as-T2 (recorded honestly in
  `confidence_tier`) or holds it. **No silent drops, no silent downgrades.**
- Known weak link to try to upgrade to region-specific T1: the region bloom anchors currently rest on
  one generic `apples.extension.org` last-frost-offset rule. Target region/zone-specific extension
  bloom records (WSU, Cornell/NY, Michigan State, Utah State); anything that only reaches T2 goes on
  the manifest.

The source manifest sign-off is an explicit release-plan checkpoint (section 10), landing before the
SHA-guarded splice, so sourcing is approved data rather than a fait accompli.

## 7. The gate refactor (`variety_detail_gate.py`, TDD RED before GREEN)

Refactor the bean-hardwired gate into an archetype-dispatched one. Touch
`tools/variety_detail_gate.py` + `tools/test_variety_detail_gate.py`.

- **Shrink `REQUIRED` to the common core** (section 4.1).
- **Dispatch the archetype-required block off `variety_archetype`** (default `annual_dtm`): annual crops
  require the bean block (section 4.2), `tree_fruit` crops require the tree block (section 4.3).
- **Tree-block validators:** `bloom_group` in the 5-value enum; `bloom_window_relative` two floats
  within [0,1] with start < end; `bloom_duration_days` positive int; `chill_hours_required` positive
  int; `use` present non-empty; `triploid` is a bool; `self_fruitful` (if present) in {no,partial,yes}.
- **Coherence check:** `bloom_group` ordering must agree with `bloom_window_relative` ordering across
  the crop (a very_early variety must not have a higher relative start than a late one) -- the tree
  analogue of dry-bean's class/DTM coherence warning.
- **Stays soft + standalone**, opt-in via `maturity_class` presence; NOT wired into a `whole_crop_gate`
  A-number this spec (the A39 hard-flip is Spec 2, INV-1).

**Adversarially proven on a scratch copy of real canonical before trusting it:** inject each defect --
wrong `bloom_group` value, `bloom_window_relative` with a fraction > 1 or start >= end, a non-bool
`triploid`, two `is_reference`, a bloom_group/relative-order mismatch, a tree crop missing a tree-block
field -- and confirm each bounces (RED) before the content is authored (GREEN).

## 8. `register_completeness` ruling (A25 companion)

New per-variety **string** keys trip `register_completeness`'s C11/A25 "any unruled non-empty string"
check and flood the gate unless ruled -- exactly what sweet-corn's `planting_layout` and dry-bean's
variety keys each needed a sanctioned ruling for. The tree block adds only **two** genuinely-new string
keys: **`bloom_group`** and **`self_fruitful`**. Everything else is already handled:

- **Already ruled (no action):** `use` (`register_completeness_gate.py:161`), and the dry-bean pilot
  already ruled the common-core string keys `id`/`maturity_class`/`confidence_tier`/`disease_notes`/
  `regional_fit` (lines 169-176).
- **Non-string, out of A25 scope (no ruling):** `bloom_window_relative` (list),
  `bloom_duration_days`/`chill_hours_required` (int), `triploid`/`is_reference` (bool);
  `note_beginner`/`note_seasoned` auto-rule by suffix.

So the change is small: extend the dry-bean `ruled_categorical()` block (or add a sibling) to rule
`bloom_group` + `self_fruitful` scoped to the `varieties.recommended` path, each with a one-line
Trevor-ruling comment in house style. This is its own TDD RED->GREEN change with a regression assert,
landed **before** the content splice.

Aside (line 161 comment): Golden Delicious currently embeds its universal-pollinizer flag in `use`,
with a noted plan to migrate it to `recommended_note`. This schema drops `recommended_note` for
dual-register `note_beginner`/`note_seasoned`, so that pollinizer prose moves into the notes -- the
migration is absorbed here, not deferred.

## 9. Batch 1 content

Batch 1 proves the schema + gate + honesty engine on the existing 13 **plus the honesty edge cases the
13 cannot exercise** -- a triploid (tests the exclusion rule) and a crabapple (tests the universal
pollinizer). Scale to the full ~30 dessert-breadth catalog is Batch 2+ (out of this spec).

- **The 13 existing** -> common-core + tree block: add `id`, `maturity_class` (ripening season),
  `is_reference`, `confidence_tier`, `triploid` (all false), `self_fruitful` where it differs, dual-
  register `note_beginner`/`note_seasoned` (replacing the null `recommended_note`), and per-variety
  `sources`/`anchoring_urls`. Each `bloom_group` + `chill_hours_required` verified against a T1 source
  (non-T1 -> manifest, section 6).
- **+ 2 triploids:** **Jonagold** and **Mutsu** (both named in the existing crop prose as triploids;
  `triploid:true`, need two partners). Exercises rule 4.
- **+ 1 crabapple:** **Dolgo** -- a long-bloom near-universal pollinizer and a genuine edible crab
  (jelly/sauce), so it earns a roster slot rather than being a bare pollinizer token.
- **Flagship (`is_reference`):** **Golden Delicious** -- the near-universal pollinizer and the data's
  designated default partner; the reference that teaches the pollination mechanic this pilot powers.

All prose original (17 USC 102(b)/Feist), apple voice, dual-register, no em dashes in consumer copy,
American English, temps as `°F`.

## 10. Authoring and release plan

1. **Gate refactor first (TDD),** RED-proven on a scratch copy of canonical (section 7).
2. **`register_completeness` ruling (TDD),** RED->GREEN with regression assert (section 8).
3. **Author Batch 1** to the section-4 schema; find + verify each load-bearing `bloom_group`/`chill`
   and region anchor.
4. **Source manifest sign-off (Trevor):** surface every non-T1 datapoint with proposed T2 + rationale;
   Trevor approves or holds. Nothing load-bearing ships on an unapproved non-T1 source (section 6).
5. **SHA-guarded COMPACT splice** (via `tools/apply_patch.py`): exactly apple's `varieties` object +
   the crop-level `variety_archetype` key change; all 124 other crops byte-identical; count 125;
   COMPACT (`separators=(",",":")`, `ensure_ascii=False`, no trailing newline); footprint audited.
6. **Release gates (protocol #6):** `whole_crop_gate` apple 18/18, `tools/gate_all.py` (whole suite,
   every certified crop, 116 unchanged), `variety_detail_gate` coverage report + tree-block clean,
   `release_verify` no new violations, per-batch source-truth sample.
7. **State trio:** regenerate/patch CURRENT_STATE.md (mind `current-state-md-drift`: no `---`
   separator, patch surgically), append STATE_HISTORY.md (most-recent first), bump LATEST.txt
   (SHA + session). Trevor confirms the push; **no plant-astro bump from this session**
   (`plant-astro-bump-owned-by-astro-session`).

## 11. Field-addition register entry

Add a row to `docs/field_addition_register.md` for the tree-variety bundle (the tree block, section
4.3) per CLAUDE.md's "Adding a cross-crop field." Trigger/rollout = Spec 2 (roster-wide column pass
against a stable roster). The row MUST state the explicit **hard-flip trigger** (INV-1): *"flip the
`variety_detail_gate` tree-block checks from soft/standalone into the A39 register-coverage hard floor
+ `gate_all` when the Spec-2 rollout column pass reaches full-roster coverage."* The pilot is a
single-crop archetype pilot, explicitly not the column pass.

## 12. Scope boundaries (explicitly OUT of this spec)

- **Reconciling the 5 existing variety shapes**, making `variety_archetype` explicit roster-wide,
  folding in `varieties_detail[]` (26 trees/berries), migrating/retiring the exploratory `delta`
  crops -> all Spec 2 (the column pass that touches every crop anyway).
- **The plant-astro consumption feature** (anchor x relative bloom, chill filtering, overlap pairs,
  triploid exclusion in the UI) -> plant-astro, Spec 2. **Handoff carries INV-2** (section 3.6).
- **Flipping the tree-block checks into the A39 hard cert floor** -> Spec 2, post-rollout (INV-1).
- **The full ~30 dessert-breadth catalog + cider/heirloom depth** -> Batch 2+ (dessert-breadth first,
  Trevor 2026-07-11); Batch 1 is the 13 + 2 triploids + 1 crabapple only.
- **Touching the region bloom-anchor *model*** (`docs/tree_region_model_scope_v0.md`): the pilot
  *sources* the anchors better (section 6) but does not restructure the region planting/bloom model.

## 13. Success criteria

- All Batch-1 varieties carry the full section-4 schema (common core + tree block), each `bloom_group`
  + `chill_hours_required` T1-anchored or Trevor-signed-off T2, each with an honest `confidence_tier`.
- The 2 triploids (`triploid:true`) and the crabapple are present and gate-clean, so the exclusion +
  universal-pollinizer honesty rules are exercised by real data, not only synthetic gate tests.
- `variety_detail_gate` refactored to common-core + `variety_archetype` dispatch; tree-block validators
  + coherence added; **adversarial RED proof recorded**; dry-bean stays green under the refactor.
- Canonical footprint = exactly apple's `varieties` object + the `variety_archetype` key; count 125;
  COMPACT; `gate_all` 116 certified unchanged; `release_verify` no new violations.
- The contract (sections 3-6) is written such that Spec 2's rollout inherits the override +
  source-authoritative + archetype-dispatch rules without renegotiation.

## 14. Open items to confirm during authoring

- The exact T1 source id(s) for per-variety `bloom_group` + `chill_hours_required` (reuse existing
  extension catalog ids or add new ones) and for upgraded region bloom anchors; non-T1 -> manifest.
- Jonagold vs. Mutsu vs. Shizuka if only one triploid is wanted, and Dolgo vs. another crabapple
  (Manchurian) -- confirmed during authoring if the sourcing favors a swap.
- Which of the 13 (beyond Golden Delicious) carry a `self_fruitful` override -- prose today implies
  Golden Delicious `partial`; confirm none of the others are partially self-fruitful per T1.
- Whether every Batch-1 variety reaches T1 or some land honestly at T2 (recorded in `confidence_tier`,
  surfaced on the manifest, never forced).
