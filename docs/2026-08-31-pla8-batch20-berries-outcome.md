# PLA-8 BATCH 20 -- BERRIES: the category closes

`50bc203f` -> `5409c0ce`. ONE promote. blackberry / blueberry / raspberry / elderberry:
**39 problems, 140 rungs** (45 / 36 / 38 / 21). Roster laddered **84 -> 88**. Catalog unchanged at
62, `source_catalog` at 218, zero bystanders. **Berries & Shrubs closes** (strawberry was already
laddered).

Read detail: `tools/staging/pla8_batch20_berries/READ_NOTES.md`. Id decisions: `PINNED_IDS.md`.

---

## 1. The guard-design lesson: an inherited guard is an assumption, not a check

Batch 19's `check_cross_batch_divergence` asserted that a shared id carries ONE ladder shape unless
pinned. **That would have refused this correct batch.** Measured here:

| id | holders | distinct shapes |
|---|---|---|
| `aphids` | 50 | **17** |
| `powdery-mildew` | 28 | **12** |
| `birds` | 3 | 1 |
| `japanese-beetles` | 3 | 1 |
| `scale-insects` | 5 | 1 |
| `spotted-wing-drosophila` | 3 | 2 |
| `stink-bugs` | 1 | 1 |

Demanding one shape across 50 crops is not a check, it is a bug. So the guard splits: **narrow ids
are shape-compared** with every divergence pinned to its record-level reason, and **broad generics
are exempt**.

**The exemption is re-measured at run time.** `check_broad_generic_exemption_is_earned` refuses if an
exempt id is not actually broad (floors: 20 holders, 5 shapes), so a narrow id cannot be smuggled
onto the exempt list to silence a real divergence. An exemption list nobody re-checks is precisely
how a live guard goes quiet later.

The narrow half also refuses a pin the batch never compares AND a pin whose ladders have CONVERGED,
since a pin that no longer describes reality is false documentation.

## 2. The type rule takes a third form in four batches

| batch | pre-state | rule |
|---|---|---|
| 17 | uniformly COARSE (`pest`/`disease`) | coarse -> fine upgrade |
| 18 | MIXED (21 fine, 3 coarse) | two-sided: preserve fine, pin the 3 upgrades |
| 19 | uniformly FINE | strong preservation: no type may change |
| **20** | **no type AT ALL** | **set from nothing; a pre-existing type breaks the premise** |

Four different rules, all correct, **only because each batch measured its own state instead of
inheriting the previous batch's assumption.** Each guard also refuses if its measured premise breaks.

## 3. The anthracnose trap is THREE-way

One common name, three organisms, per the records' own prose:

* the roster's generic `anthracnose` (14 vegetable crops) is *Colletotrichum orbiculare*
* blackberry and raspberry are ***Elsinoe veneta*** -- a different **GENUS** -> `cane-anthracnose`
* blueberry is a *Colletotrichum* **ripe fruit rot** -> `blueberry-ripe-rot`

Worse than batch 19's two-way `brown-rot` trap. `phytophthora-root-rot` is likewise not citrus's
`phytophthora-foot-rot`: same genus, different organ, different controls.

## 4. A pre-existing roster defect, refused rather than widened

**`japanese-beetle` (singular, basil) and `japanese-beetles` (plural, marigold/zinnia/echinacea) are
both live for *Popillia japonica*.** Two of this batch's crops name the singular and one the plural,
so name-derived slugs would have put a third crop on each side.

All three take the **plural**. basil's singular is filed for a repoint. The guard also **refuses if
the split is ever repaired**, so whoever fixes basil must retire this guard deliberately rather than
let it pass on a premise that no longer holds.

## 5. Ids pinned before fan-out: 39/39, zero drift, third consecutive batch

Six distinct reused ids cover **eight** problem-name keys, because two organisms are named two ways:
`Spotted-wing drosophila (SWD)` / `Spotted-wing drosophila and sap beetles` both resolve to
`spotted-wing-drosophila`, and `Japanese beetle` / `Japanese beetles` both to `japanese-beetles`.
**That collapse is the whole point of pinning.**

## 6. The read: the majority was wrong again

Rungs went 142 -> 140 on one ruling.

Two authors used `resistant_varieties` for "choose early-ripening cultivars to dodge peak fly
pressure". One **refused** it: the catalog calls that key "the natural handoff to variety-level
resistance data", so escape-by-timing would seed a **false resistance signal on a live join key**.

Blackberry, one of the two who used it, supplied the decisive evidence: it searched the roster and
found **zero shipped precedent** for earliness-escape under that key. Dropped from both.

Tally 2 used / 1 refused, refuser right -- **the same shape as batch 19's `garden_sanitation` call.**
In both cases every author who used the key had flagged it as their loosest fit. **The self-flags,
not the tally, are the signal.**

A separate call went the other way and is worth recording so the two are not read as inconsistent:
elderberry's `birds` keeps `resistant_varieties` for a cultivar whose drooping cyme hides fruit. The
catalog explicitly extends the key to "varieties a pest is less drawn to, like a tight corn husk
against earworm" -- non-preference IS a varietal trait. Ripening date is a calendar accident.

### One question handed to an author, and answered against me

Elderberry's SWD problem is named as a composite with sap beetles. Its author argued **co-equal**, on
good structural evidence (parallel grammar in all four descriptive fields, both registers). I read
the record and **ruled the other way**: the biology and the control are not parallel. SWD *"lays eggs
in healthy ripe fruit"* (creates the damage); sap beetles *"are drawn to overripe and split
berries"* (exploit it). The entire treatment field is the SWD program. The ladder encodes the
control, so the reuse is honest. The author's finding does land on the problem's **name**, which
over-promises relative to its own cause and treatment fields -- filed as prose, not id.

## 7. Six mis-pointed source keys, and the class is now measured

Two independent authors reported them; both verified against the data:

* **raspberry** -- `cornell_ext` resolves to `https://fruit.cornell.edu/spottedwing/hosts/` on FIVE
  of ten problems. Correct only for SWD; implausible for cane borer girdling, crown borer biology,
  aphids, and a virus complex.
* **blueberry** -- `blueberry-maggot` cites the UMaine **SWD factsheet**, for *Rhagoletis mendax*, a
  different fly whose record makes maggot-specific claims an SWD page cannot support.

| batch | instance |
|---|---|
| 17 | plum's San Jose scale citing a mealy plum aphid page |
| 18 | lemon's mealybug and sooty-mold ant claims citing an INDEX PAGE with no ant content |
| 20 | these six |

**The shape is consistent: a crop's problems share ONE source id whose URL is specific to ONE of
them.** Mechanically detectable -- flag any node whose cited URL names a pest or disease absent from
that problem's own name and prose. Worth building; deliberately not scoped into a crop batch,
because a repoint is its own change.

## 8. Verification

* Guard suite **71/71**, green under both runners.
* Mutation harness **49 injected, ZERO SURVIVORS**, 14 families (schema, types, ids, anthracnose,
  jbeetle, broad, crossbatch, temps, vocab, materials, validate, blast, catalog, mechanics).
* `gate_all` **121/121** · `control_ladder_gate` 0 · `register_completeness` PASS ·
  `whole_crop_gate` PASS x4 · 280 new strings hygiene-clean.
* `release_verify` **clean, no concerns at all** -- section A confirms only the four declared crops
  changed, `catalog +none -none`, strawberry byte-identical. Achieved first try by passing an
  unchanged same-class reference, which is the lesson from the previous two batches applied.

## 9. Catalog gaps, best-evidenced first

1. **General plant vigor has no method.** Reported by ALL FOUR berry authors across eight records,
   on top of citrus's "keep trees unstressed and not dusty". The near-misses are wrong:
   `even_watering` is mite/physiological and means steady moisture against calcium disorders;
   `water_at_the_base` means splash suppression. **The best-evidenced mint candidate on the board.**
2. **Burying overwintering inoculum has no method, and the nearest key CONTRADICTS it.** Blueberry's
   mummy berry control is to bury mummies by mulch or shallow cultivation before spore cups form --
   half the two-stage cycle -- while `garden_sanitation`'s own caution reads *"Destroy diseased
   debris rather than leaving or BURYING it."*
3. **Dormant lime sulfur has no key.** Raspberry and blackberry are the only two crops corpus-wide
   that name it. The catalog's `sulfur` is an in-season protectant with in-season heat cautions;
   delayed-dormant calcium polysulfide on bare canes is a different material, timing and caution set.
4. **Exclusion netting on a non-SWD fly.** `bird_netting` is vertebrate-only,
   `swd_exclusion_netting` is SWD-only across all three roster uses, `floating_row_cover` is
   bed-level transplant fabric.
5. **`airflow_spacing` cannot reach an insect type**, losing the canopy-opening half of both SWD and
   scale advice. An `applies_to` artifact rather than biology.

## 10. Roster position

Laddered **88 / 121**. Remaining: **33 crops, 190 problems, 9 batches** -- flowers/edible (26),
stragglers (26), woody herbs (25), other trees (24), roots (22), alliums (19), soft herbs (19), pome
fruit (15), and microgreens (14) LAST per the standing ruling. Every remaining crop is assigned and
every batch is comfortably under the size threshold, so none needs splitting the way citrus did.
