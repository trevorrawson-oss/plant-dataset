# `critical_warnings[]` and the container safety class: field-shape spec (PLA-581, PLA-7 Plan D)

**Date:** 2026-09-21. **Canonical:** `1721208e` (unchanged by this document; no promote, no data
change). **Branch:** `worktree-pla581-critical-warnings`, spec commit only. **Base:** `origin/main`
`e726490` (the approved PLA-580 spec).
**Supersedes, in part:** `docs/superpowers/specs/2026-09-06-pla7-container-field-shape-design.md`
section 5. Where this document and that one disagree, the disagreement is named in section 2 and the
measurement is given.
**Read with:** PLA-581, PLA-142, PLA-7 (D4), PLA-463 (the framing-copy pattern), PLA-464 (absence
encoding), PLA-465, PLA-580, PLA-586, PLA-539, PLA-10.

**Amendment history.** First draft 2026-09-21, held. **Amendment 1** (same day, Trevor's read):
D1 approved with an evidence condition, **D2 reversed**, D3 / D4 / D5 approved as recommended. The
rulings are in section 0; every section they touch is amended in place and says so.

---

> ## RULED 2026-09-21, AMENDED, HELD FOR A SECOND READ
>
> **D1 APPROVED**, on the condition that every warning in `container_safety` carries its own T1
> source verbatim with bytes and sha256, and that any warning without one is **cut**. Section 4.5
> is that evidence table: **three warnings keep, one candidate cut** (mosquito). **PLA-7 authors
> zero per-crop safety entries.** `container_safety` is a new top-level key and needs its own
> consumer line; section 8.5 measures what that line actually is, and it is **not** an allowlist
> entry.
>
> **D2 REVERSED.** Not `[]` on 121. Three documented states: **`null` = not assessed** (all 121 ship
> null now), **`[]` = assessed, none found**, **`[...]` = authored entries**. Section 5 is rewritten.
>
> **D3, D4, D5 APPROVED** as recommended.
>
> **No promote, no gate, no data change.** Canonical is byte-identical to `1721208e` throughout.
>
> **One thing found while applying ruling 1 needs your eye** (section 4.2): the D3 app rule that was
> to carry the tip-over class **cannot fire on a single one of the 18 crops**. Its named inputs do
> not exist in the dataset, and `mature_height_ft` is null on all 18.

**The headline.** The container-safety class was scoped on the assumption that balcony load is a
per-crop warning. **It is not a per-crop anything.** Read from raw bytes, exactly one T1 sentence in
the sources admitted to this dataset addresses structural load, it names no crop, and it is a
**referral rather than a figure**: Illinois Extension says *"Consult with a building architect
concerning weight limitations when placing heavy pots on balcony or rooftop gardens."* There is no
published weight, no pounds per square foot, and no per-crop variation to encode. Authoring it onto
121 crop records would write the same sentence 121 times, which is the placeholder pattern PLA-463
rejected for rootstock framing and PLA-465 rejected for rootstock heights.

**The second headline.** The 2026-09-06 spec said the safety class covers *"the container hazards the
block's prose already raises on 9 crops (balcony load, a tall staked vine in a light pot in wind, a
saucer-flooded pot as a root-rot and mosquito source where a source says so)."* Measured on
`1721208e`, none of the three counts hold. **Balcony load: 0 crops.** Eleven crops say "balcony" and
every one of them means it as a place to put a pot, never as a load. **Tip-over in wind: 18 crops**,
already authored, already dual-register, in `container_notes.shape_requirements_*` and `notes_*`.
**Mosquitoes: 0 crops**, and the Illinois page that carries the mosquito claim is scoped to
**container water gardens with fish in them**, not to a saucer under a vegetable pot. The "9" is not
reproducible from any net this session ran.

---

## 0. The rulings, as given (2026-09-21)

1. **D1 APPROVED.** Crop-invariant warnings live in a top-level `container_safety` object, not in
   per-crop `critical_warnings[]`. PLA-581's "complete when" changes accordingly and the change is
   recorded on the ticket. **Condition:** each warning lists its own T1 source, verbatim, with bytes
   and sha256; **any warning without one is cut, not shipped because it is generic.** The mosquito
   candidate specifically: state what supports a container version or drop it. **Tip-over stays
   where it is** (per-crop `container_notes` prose on 18 crops, plus the D3 app rule); no new
   entries. `container_safety` needs its own consumer line.
2. **D2 REVERSED.** `[]` on 121 asserts "assessed, no critical warnings" on crops nobody has
   assessed for PLA-142's harvest class. That is an **unsourced negative**, the same defect class as
   `container_suitable: false` and astro's "in-ground" today. Three documented states, per PLA-464's
   precedent: `null` = not assessed, `[]` = assessed and none found, `[...]` = authored entries.
   The `growth_stages_annual` lesson is that its `null` was **never documented**, not that `null` is
   wrong. Document all three in the spec and the register row; the gate enforces the three-state
   rule.
3. **D3, D4, D5 APPROVED** as recommended. `severity` modeled; `stage` gated against the crop's own
   ladder; A61 with the A60 collision recorded; the named positive controls; consumer lines
   first. The experience-mode rule in its checkable form goes into PLA-586's and PLA-539's
   contracts.

---

## 1. What this adds, in one table

| field | where | shape | who authors | who reads |
|---|---|---|---|---|
| `critical_warnings` | top-level, per crop | `null` / `[]` / non-empty list, **all three meaning different things** (section 5); **key absent on the 7 shells** | PLA-581 promote creates it roster-wide as **`null`**; **PLA-142 authors the `harvest` class** and moves each crop `null` -> `[]` or `[...]` as it assesses it | plant-app "In a pot" chapter + guide hero (PLA-539); plant-astro ContainerCard (PLA-586) |
| `container_safety` | **top level of the dataset, not on a crop** | one object holding the **3** crop-invariant warnings that survived the section 4.5 evidence test, each with its own `sources` + `anchoring_urls` | PLA-581 promote, once | both consumers, on every crop with `container_ok: true` |

Both rows are now ruled. Sections 4.1 and 4.5 carry the pricing and the evidence.

---

## 2. The reads, from raw bytes (found / absent / undetermined)

All fetches 2026-09-21, two user agents each, status + byte count + sha256 in section 12. Every
sentence below was copied from the fetched bytes, not from a search snippet.

### 2.1 `uiuc_ext` Illinois Extension, "Container Size": FOUND, and it is the only structural-load claim anywhere

Five sentences, all in one list, all about stability, plus one about load:

> Shape (and volume) determine whether a container is stable enough to keep the plant from tipping
> over in wind as the plants grow.
>
> Square pots are the most stable.
>
> Traditional pots (sliced off inverted cones) tip over easily.
>
> Small pots may be "top-heavy" with plants tipping over more readily.
>
> Strap or anchor tall plants in place if they become top heavy.
>
> Watch for this problem on exposed balconies, rooftops and decks especially prone to winds.
>
> **Consult with a building architect concerning weight limitations when placing heavy pots on
> balcony or rooftop gardens.**

Three things about the load sentence, each load-bearing for D1:

1. **It names no crop.** Its subject is "heavy pots", not a plant.
2. **It publishes no figure.** It is a referral to a building architect. Any number we rendered
   beside it would be ours, not Illinois'.
3. **Its predicate is the site**, "balcony or rooftop gardens". A grower with a pot on the ground is
   outside its scope entirely, and nothing in the dataset knows where a user's pot is.

### 2.2 `csu_ext` Colorado State University Extension, "Container Gardens": FOUND, three claims, none structural

> Also, keep in mind that tall plants will require a heavier container to avoid tipping from
> imbalance, or wind.

> It is best to consider whether your pots will be moved during the growing season, because when
> water is added to soil in an already heavy container, the weight may be too much to lift easily.

> However, make sure you never use a container that holds toxic materials, especially if edible
> plants are going to be grown.

The second is a **handling** hazard (lifting), not a **structural** one (load on a deck). They are
different warnings with different audiences and should not be merged. The third is a new class the
2026-09-06 spec did not anticipate: **container material toxicity**.

### 2.3 `uiuc_ext`, three further pages under the same section

- **Vegetable Containers:** *"The container needs to have good drainage, and should not contain
  chemicals that are toxic to plants and human beings."* Second source for the toxicity class.
- **Container Material Choices:** *"Secure hanging items well and consider potential safety issues
  when hanging."* A fourth class, hanging-container security. Also *"Winds and reflected heat will
  cause the plants to dry out faster"*, which is a plant-health note, not a human-safety one, and is
  recorded here so a later session does not re-open it as a heat safety claim.
- **Growing Vines in Containers:** *"As the vine gets larger and heavier, it also becomes more prone
  to being knocked over during windy days."* and *"Also make sure the support is firmly anchored."*
  Second source for the tip-over class, and the closest thing found to a crop-varying predicate
  ("as the vine gets larger").

### 2.4 `uwi_hort` Wisconsin and `umd_ext` Maryland: ABSENT

Three pages read in full (Wisconsin's container-gardening and growing-vegetables-in-containers
articles, UMD's types-of-containers and maintaining-container-grown-vegetables). **Zero** safety
sentences. Wisconsin's only balcony mention is placement: *"Containers can be placed on a windowsill,
patio, deck or balcony, or in any place where growing conditions are appropriate for producing
vegetables."* Both institutions discuss container weight only as an argument for soilless mix.

**Absence is scoped to these four documents**, not to the institutions.

### 2.5 `umn_ext` Minnesota: UNDETERMINED

HTTP **403** on both user agents, twice, on the container-gardening article the search surfaced.
Recorded as undetermined rather than absent (the WAF-block-is-not-absence rule). **Nothing in this
spec depends on Minnesota.**

### 2.6 What no source read publishes, stated as a negative

- **No weight figure for a pot.** The 2026-09-06 spec anticipated one: *"where extension publishes
  the weight of wet potting mix per gallon, that is the citable figure."* Searched across eleven
  extension domains and read the pages returned: **not found.** Illinois refers the question to an
  architect; UGA's conversion tables give fertilizer and lime rates per cubic yard, not medium
  weight. **A rendered pounds-per-pot number would be fabricated.** This is the
  `a-hash-field-pulls-a-fabricated-digest` failure mode in a different costume: the shape of a
  "severity" warning pulls for a number, and there is not one.
- **No per-square-foot load figure for containers.** Penn State publishes green-roof structural
  guidance, but a green roof is an engineered assembly with a waterproof membrane, a drainage layer
  and lightweight media. It is not a pot on a balcony, and its figures do not transfer. Out of
  scope, named in section 11 so it is not re-discovered as a lead.
- **The mosquito claim is water-garden-scoped.** Illinois' "Problems - Algae and Mosquitoes" page
  sits under **Container Water Gardens** and opens *"Mosquitoes only become a problem in water
  garden containers that are not maintained."* Its remedies are goldfish, Mosquito Dunks and filling
  the container with gravel. It does not support a warning about a saucer under a pepper plant.
  The 2026-09-06 spec's "where a source says so" hedge was correct; the source does not say so.

### 2.7 The dataset's own prose, measured on `1721208e`

Scanned `container_notes` across all 121 certified crops:

| term | crops | what it actually says |
|---|---|---|
| "balcon" | **11** | placement only, on all 11. Zero load claims. |
| "rooftop" / "roof" | **0** | |
| load limit / weight limit / load-bearing / pounds per | **0** | |
| a pounds or lbs figure | **0** | |
| structural / engineer / building code / landlord | **0** | |
| tip over / topple / blow over | **18** | a real hazard sentence on all 18 |
| mosquito | **0** | |
| saucer | **94** | 93 distinct sentences, every one framed as **root rot**, never as a hazard to a person |

The 18 tip-over crops: `banana-pepper`, `bell-pepper`, `broad-beans-fava`, `broccoli`,
`brussels-sprouts`, `cayenne-pepper`, `collards`, `cosmos`, `dill`, `eggplant`, `habanero`,
`jalapeno`, `okra`, `pole-beans`, `snow-peas`, `sugar-snap-peas`, `yellow-summer-squash`,
`zucchini-courgette`. Four of them tie it to wind explicitly (`cayenne-pepper`, `habanero`, `okra`,
`pole-beans`). Representative, from `brussels-sprouts`:

> Brussels sprouts get tall and top-heavy, so give one plant a deep, heavy pot that holds at least 5
> gallons and is about 12 inches deep, and stake it so it does not tip over.

**This content is already authored, already dual-register, and already certified.** It lives in
`container_notes.shape_requirements_*` and `notes_*`. It renders nowhere today, and it will render
under PLA-586's ContainerCard and PLA-539's "In a pot" chapter without any new field. Section 4.2
turns on this fact.

---

## 3. READ 2: crop, container, or site? Every candidate classified

The brief's second read asked, for each candidate warning, whether it is a property of a crop, of a
container, or of a site. Answered from the sentences in section 2:

| candidate | sources | property of | varies by crop? | already in the dataset? |
|---|---|---|---|---|
| Structural load on a balcony or roof | `uiuc_ext` | **site** (balcony/roof) x **container** (heavy pot) | **no** | no |
| Lifting a watered pot | `csu_ext` | **container** | no | no |
| Tipping in wind | `uiuc_ext`, `csu_ext` | **plant habit** x container shape x site exposure | **yes**, weakly: "tall plants", "as the vine gets larger" | **yes, on 18 crops** |
| Container material toxicity | `csu_ext`, `uiuc_ext` | **container** | no (the "edible plants" qualifier covers essentially the whole roster) | no |
| Securing a hanging container | `uiuc_ext` | **container** | no | no |
| Mosquitoes in standing water | `uiuc_ext`, **water gardens only** | a different product | n/a | no |

**Four of the five live candidates are crop-invariant.** The one that varies, tip-over, varies by a
predicate the dataset holds only as prose: `mature_height_ft` is non-null on **16 of 121** certified
crops, and those 16 are mostly woody perennials (`apple`, `fig`, `peach`, `rosemary`, ...), not the
top-heavy annuals the hazard actually applies to. **There is no structured field that can select the
18 tip-over crops.** Their own prose is the only selector, and it is ours, not a source's.

---

## 4. D1: where a generic container warning lives. APPROVED, with the evidence condition applied

### 4.1 The three options, priced (Option C ruled)

**Option A: per crop.** Every `container_ok: true` crop carries the three crop-invariant warnings as
`critical_warnings` entries. **110 crops x 3 entries = 330 entries**, each byte-identical to 109
others, each carrying its own copy of `sources` and `anchoring_urls`. Every crop added after this
must copy them or fail a coverage gate. This is exactly what PLA-463 rejected ("Six shared strings,
not per-crop authoring ... No duplication across 19 crops, and a tree crop added later inherits the
framing automatically") and what PLA-465 called out on the four `soil_and_pest` crops ("every row
today carries the same placeholder"). **Not recommended.**

**Option B: a shared string selected by a crop property, inside the crop record.** A crop carries a
reference id and the consumer joins it to a shared table. Avoids duplication but adds a join, and
the join key would be `container_ok: true`, which the consumer can already read directly. The
indirection buys nothing. **Not recommended.**

**Option C: outside the crop record entirely. RULED (D1, approved 2026-09-21).** A new top-level `container_safety`
object in `crops_data_final.json`, a sibling of `source_catalog` and `zone_sources`, holding the
three crop-invariant warnings once, each with its own `sources` and `anchoring_urls`. Consumers
render all of them on any crop with `container_ok: true`.

**Why the dataset and not consumer-side copy:** a safety warning carries a T1 source and a verified
date. The dataset is where sourcing discipline lives: `source_catalog` admission, `anchoring_urls`,
`release_verify`, the dash and register gates. Consumer-side copy has none of that, and there are
two consumers, so it would be written twice and drift. This also matches PLA-463's framing copy in
kind: crop-invariant, sourced, authored once, selected by a property.

### 4.2 The tip-over class: RULED to stay where it is, and the app rule behind it does not exist

**Ruled:** tip-over stays as per-crop `container_notes` prose on 18 crops, plus the PLA-7 D3 app
rule; no new entries. The first half holds as written: the dataset already carries the hazard on 18
crops, in both registers, certified, and promoting it into `critical_warnings` would put the same
sentence twice in the same card, which is the overlap PLA-142 named as its own open question
(*"authoring should dedupe rather than duplicate"*). The work it needs is a render decision in
PLA-586 and PLA-539, which is where `shape_requirements_*` starts rendering anyway.

**The second half does not hold yet, and this is the one thing in the rulings that measurement
contradicts.** The ruling names the D3 app rule as running over `mature_height_ft` and
`container_path`. Measured on `1721208e`:

| input | state on the 18 tip-over crops |
|---|---|
| `mature_height_ft` | **`null` on all 18.** The 16 crops that carry a height are woody perennials and woody herbs (`apple`, `fig`, `peach`, `rosemary`, ...); the intersection with the 18 is **empty**. |
| `container_path` | **`direct` on all 18**, which is also the value on 86 of 121 crops. It carries no signal about plant habit. |
| `height_inches` (what PLA-7's D3 actually names) | **0 occurrences dataset-wide.** |
| `planting_layout` `vertical` (the other input D3 names) | the key exists on **6** crops, every value is `"block"`; `"vertical"` occurs **0** times. |
| `footprint_inches` | key present on 121, **non-empty on 0** (the defined-but-unauthored slot, PLA-465 section 6). |

Two things follow. First, a small correction of attribution rather than of intent: PLA-7's D3 says
wind and support *"rides PLA-10's `height_inches` and the `vertical` layout entry"*, which is a
**different field from PLA-465's `mature_height_ft`** and belongs to an arc that has not run.
Second, and this is the part that matters: **there is no input, existing or named, that would let an
app rule fire on any of the 18 crops.** The rule is not weak here, it is empty.

**What this leaves standing, and it is enough:** the 18 crops' own prose already states the hazard
in both registers and will render under PLA-586 and PLA-539. The tip-over class is covered by that
prose alone, with no app rule and no new field, which is exactly the outcome the ruling wanted. The
app rule should be recorded as **owed to PLA-10**, not as a live half of this decision, so a later
session does not read "plus the D3 app rule" as something that shipped. **Filed as a note on PLA-10
and PLA-7 rather than built here.**

If a hero-level treatment of tip-over is wanted before PLA-10 lands, the honest route is a
`class: safety` entry on those 18 crops that **replaces** the prose sentence rather than repeating
it, selected by the crop's own prose and recorded as a modeled selector. That is a content pass, not
a field-shape question, and it is not recommended now.

### 4.3 PLA-581's "complete when", as amended by the ruling

The issue said *"The container `safety` class authored with T1 sources and raw-bytes
`field_additions` records."* **Amended:** `critical_warnings[]` ships **`null`** on all 121
certified crops (ruling 2), and the safety content lands in `container_safety` with per-warning T1
evidence (4.5). The field still exists roster-wide with its shape ruled, PLA-142's slot is still
fixed, and PLA-7's safety requirement is still met on both consumers in every mode. The deliverable
is **one authored object and two consumer lines, not 110 crop edits**. Recorded on the ticket.

### 4.4 Copy for the three shared warnings

Dual register, no em dashes, American English, "plant" lowercase. Each carries only what its source
says. **No number appears anywhere, because no source published one.**

**`balcony_load`** (source `uiuc_ext`, container-size page)

- *beginner:* "A pot full of wet soil is much heavier than it looks, and several of them together
  add up fast. Before you set up heavy pots on a balcony, a roof, or a raised deck, check with your
  building's owner or an architect about how much weight it is built to carry."
- *seasoned:* "Wet potting mix and the container together put a real point load on a structure, and
  a cluster of large pots concentrates it. Illinois Extension's guidance is to consult a building
  architect about weight limitations before placing heavy pots on a balcony or rooftop garden. No
  extension source publishes a pounds figure for this, so treat it as a question for whoever knows
  the structure, not a number you can look up."

**`container_material`** (sources `csu_ext`, `uiuc_ext`)

- *beginner:* "Use a container that was made to hold soil or food. Never plant something you are
  going to eat in a container that held chemicals."
- *seasoned:* "A repurposed container is fine as long as it never held a toxic material. Both
  Colorado State and Illinois are explicit that a container used for edible plants must not carry
  chemical residue, and a drum or bucket with an unknown history is not worth the risk on a food
  crop."

**`hanging_security`** (source `uiuc_ext`, container-material page)

- *beginner:* "A hanging basket gets a lot heavier once you water it. Hang it from something solid,
  and not over a spot where someone sits or walks."
- *seasoned:* "Secure hanging containers to structural support rather than to trim or a light hook,
  and account for the watered weight rather than the dry weight. Illinois flags the safety of the
  mounting as a decision to make deliberately."

The `csu_ext` lifting warning is deliberately **not** authored as a fourth entry: it is advice about
moving a pot, not a hazard, and it belongs in the ContainerCard's prose if anywhere. Named here so
the omission is a decision rather than an oversight.

### 4.5 The D1 condition: per-warning evidence, and what it cuts

Ruling 1: *"list each warning in the object with its own T1 source, verbatim, bytes and sha256. Any
warning without one is cut, not shipped because it is generic."* Applied. Every digest below is a
measured sha256 of the fetched body, never a stated one.

**KEEP: `balcony_load`**

| | |
|---|---|
| source key | `uiuc_ext` (`tier: T1`, `university_extension`, admitted in `source_catalog`) |
| url | `https://extension.illinois.edu/container-gardens/container-size` |
| fetched | 2026-09-21, HTTP 200 on both user agents, identical bytes |
| bytes | 28,186 |
| sha256 | `0b482e6ef1b9d9093dc0a0029e2753cf20bf787c7c329dd9ff23f7cbe0fe9705` |
| verbatim | *"Consult with a building architect concerning weight limitations when placing heavy pots on balcony or rooftop gardens."* |

**KEEP: `container_material`** (two independent sources, which is why this one is not a single-source
claim)

| | |
|---|---|
| source key | `csu_ext` (`tier: T1`) |
| url | `https://extension.colostate.edu/resource/container-gardens/` |
| fetched | 2026-09-21, HTTP 200 both UAs |
| bytes | 141,247 |
| sha256 | `a0197e08d33decedb9ae7fe0ecd6cf7a50296559ac7d0d26623a83b02db2159d` |
| verbatim | *"However, make sure you never use a container that holds toxic materials, especially if edible plants are going to be grown."* |
| second source key | `uiuc_ext` (`tier: T1`) |
| url | `https://extension.illinois.edu/container-gardens/vegetable-containers` |
| bytes | 24,343 |
| sha256 | `62b5e5c5f5ce244fb868faccdc9ac11e0babb38aad6be60a6776d97577ed8d89` |
| verbatim | *"The container needs to have good drainage, and should not contain chemicals that are toxic to plants and human beings."* |

**KEEP: `hanging_security`**

| | |
|---|---|
| source key | `uiuc_ext` (`tier: T1`) |
| url | `https://extension.illinois.edu/container-gardens/container-material-choices` |
| fetched | 2026-09-21, HTTP 200 both UAs |
| bytes | 32,678 |
| sha256 | `5ab9a68fcdf516a59c964c9ee6715ef0abfbd10a7ab0cac83682128e54637452` |
| verbatim | *"Secure hanging items well and consider potential safety issues when hanging."* |

**CUT: the mosquito warning. Nothing supports a container version.**

It was never among the three proposed, and section 11 of the first draft already held it out of
scope. Ruling 1 asks for the reason on the record rather than in a list of exclusions, so here it
is, from bytes.

| | |
|---|---|
| source key | `uiuc_ext` |
| url | `https://extension.illinois.edu/container-gardens/problems-algae-and-mosquitoes` |
| bytes | 27,257 |
| sha256 | `07399314a5bc14b9508f92a6e8a5fe957ffc78c10d57813e12d0784daaaa0501` |
| verbatim, first sentence | *"Mosquitoes only become a problem in **water garden containers** that are not maintained."* |

The page sits under **Container Water Gardens**, a section whose sibling pages are "Fish and Other
Animals", "Pumps and Fountains" and "Planting the Water Garden Container". Its remedies are
goldfish, Mosquito Dunks and *"Water garden containers can be filled with gravel after the plants
and water have been added."* Every one of those presupposes a standing body of water that is the
point of the container. **None of it transfers to a saucer under a vegetable pot**, and the
dataset's own 94 saucer sentences say nothing about mosquitoes (measured: 0 occurrences roster-wide).

Searched for a container-scoped version and did not find one: no page among the sixteen fetched ties
a plant saucer to mosquito breeding, and the general mosquito-control literature that does mention
plant saucers is about standing water around a home, not about growing a crop in a pot. **Dropped.
If it is wanted later it needs its own source, not this one.**

**Also cut, and named so the omission is a decision:** the `csu_ext` lifting warning (4.4, a handling
hazard rather than a safety one) and any pounds-per-pot figure (2.6, no source publishes one, so a
number would be fabricated).

**Net: 3 warnings ship, 4 sources across them, 0 shipped on generality alone.**

---

## 5. D2: encoding of absence. REVERSED AND RULED

### 5.1 What the roster actually does, measured

There is no single convention. Across every top-level key that is a list on at least one certified
crop, all three encodings are in use, and they mean different things:

| key | absent | `null` | `[]` | non-empty | what the split means |
|---|---|---|---|---|---|
| `rootstock_options` | **102** | 0 | **2** | 17 | absent = the concept does not apply (non-tree); `[]` = it applies and is empty (fig, pomegranate, after PLA-464) |
| `recipes` | 0 | 0 | **117** | 4 | `[]` = applies, none authored |
| `mature_height_ft` | 0 | **105** | 0 | 16 | presence-or-null, the PLA-465 / A39 pattern for a scalar or pair |
| `days_to_maturity` | 0 | 0 | **30** | 91 | `[]` = no annual maturity |

Only six top-level list keys carry an explicit `null` on any certified crop. **Two of the six are
pairs rather than collections** (`mature_height_ft`, `mature_spread_ft`, both `[lo, hi]`). The other
four are genuine collections, and they are the cautionary case, not the precedent:
`description_sources` null on 1 crop, `harvest_ramp_weeks` null on 1, and
`growth_stages_annual` / `growth_stages_year_one` **using all three states at once** -- absent 98,
`null` 10, `[]` 13, and **non-empty 0**. Nobody can say what the difference between those 10 nulls
and those 13 empties means, **because it was never written down** (see 5.2, which corrects the
inference the first draft drew from this row: the defect is the missing documentation, not the third
state).

### 5.2 RULED: three documented states, and the first draft was wrong

**The correction, against this document's own recommendation.** The first draft recommended `[]` on
all 121 with `null` a violation. That is wrong, and the reason is worth keeping because it is a
class of defect, not a preference. **`[]` means "assessed, none found."** Shipping it on 121 crops
would assert that every crop had been assessed for a critical warning, when `critical_warnings`
spans two classes and **PLA-142's `harvest` class has not been assessed on a single crop.** The
promote would be writing an **unsourced negative** into 121 records, the same defect as
`container_suitable: false` on a crop nobody read and astro's "in-ground" on a crop whose own notes
say a pot works. The draft had reasoned about the `safety` class alone and then generalized the
answer to a field that is not only about safety.

**The three states, all documented, all meaningful:**

| state | meaning | who writes it |
|---|---|---|
| **`null`** | **not assessed.** No pass has yet asked whether this crop has a critical warning. | the PLA-581 promote, on **all 121** certified crops |
| **`[]`** | **assessed, none found.** A pass looked and this crop legitimately has none. | PLA-142, per crop, as its `harvest` pass reaches each one |
| **`[...]`** | authored entries | PLA-142 (`harvest`); PLA-7 authors none (ruling 1) |

**Key absent** remains the uncertified-shell exemption, not a fourth semantic state: the 7 shells
carry no key for `container_path`, `mature_height_ft` or any other register field, which is how A39
exempts them and how the A1 and PLA-465 promotes left them byte-identical.

**On `growth_stages_annual`, correcting 5.1's use of it.** The first draft cited its absent 98 /
`null` 10 / `[]` 13 / non-empty 0 as evidence that a three-state collection is incoherent. That is
the wrong lesson. The defect there is that **the `null` was never documented**, so no reader can
recover what it was meant to say. A three-state field is fine when all three states are written
down, which is what this section and the register row now do. The measurement stands; the inference
drawn from it in the first draft does not.

**Consistency with PLA-580.** That gate rules `[]` a violation for `plants_per_pot` and this one
admits it, and the two are consistent once each field's own states are named. `plants_per_pot` has
**two** states, "no source published a count" (`null`) and "here are the readings", so `[]` spells
nothing. `critical_warnings` has **three**, because "not assessed" and "assessed, none found" are
genuinely different facts about a crop and a later pass must be able to tell them apart. The shared
rule is the one both gates enforce: **spell every state that exists and refuse every one that does
not.**

**For the consumers this changes nothing:** absent, `null` and `[]` all render no warnings block, and
only a non-empty list renders. The distinction is for the dataset and for PLA-142's progress, not
for a user. PLA-586's card should treat all three alike anyway, so a gate slip never reaches a user
as a crash.

---

## 6. D3: `severity` and `stage` vocabularies. APPROVED as recommended

### 6.1 `severity`: keep two values, and record that it is MODELED

Measured: **not one source read grades the severity of its warning.** Illinois, Colorado State and
UMD state hazards flatly. There is no published scale to map onto, so any enum here is ours.

Recommendation: **keep `severity: critical | high`**, exactly two values, closed, **ordering within a
class and never changing rendering**, and write into the register row that the value is **modeled,
not sourced**, the way PLA-463's vocabulary and PLA-580 section 4.4's extrapolation are recorded.
Two reasons to keep it rather than drop it: PLA-142 will author a class where ordering matters
(`strawberry` year-one flowers against `pumpkin` curing on the same crop is plausible), and removing
a field PLA-142 needs is a migration this spec exists to prevent.

**The caveat, recorded against my own recommendation:** on the section 4 population, `severity`
orders nothing, because no crop carries two entries. It is a field with no live discriminating use
on the day it ships. If you would rather not carry an ungrounded enum, dropping it now is cheap and
PLA-142 can add it when it has two entries on one crop to order. **Either answer is defensible; the
field being modeled is the part that must be written down.**

### 6.2 `stage`: keep it, and gate it against the crop's own ladder

The 2026-09-06 spec says `stage` is "a `growth_stages` id, or null = always". Measured: there are
**81 distinct `growth_stages` ids** across the 121 certified crops, with no closed vocabulary (the
commonest are `harvest` 93, `germination` 79, `seedling` 70, `established` 48, `flowering` 47).

So the gate **cannot** check `stage` against a fixed list. Recommendation: **`stage` is `null` or a
string that appears as an id in THIS crop's own `growth_stages`**, checked per crop. That is both
stricter than a global list (a `flowering` stage on a crop whose ladder has no flowering stage is a
defect) and the only rule that is actually true.

Every entry PLA-7 would author is `null` ("a pot is heavy whenever it is full"), so **the non-null
branch of this rule has no live member** and needs a named positive control (section 7).

---

## 7. D4: armor

### 7.1 The shape gate

New `tools/critical_warnings_gate.py` + tests, TDD, wired into `whole_crop_gate`. **Id collision to
settle:** the highest id in use is **A59** (measured). PLA-580's approved spec claims **A60** for
`plants_per_pot`, and its promote is not built. Whichever promote lands first takes A60; this spec
assumes **A61** and the losing session re-numbers. Recorded so two sessions do not both ship an A60.

Shape armed on the tooling commit; the presence floor behind `A61_PRESENCE_ARMED = False` until the
commit that writes canonical, exactly as A58 and A59 were wired.

Rules:

1. **The three-state rule (5.2).** `critical_warnings` is `null`, `[]`, or a non-empty list, and
   nothing else: a string, a dict or a number is a violation. The key is **absent** on every
   uncertified shell and **present** on every certified crop. The gate does not prefer one state
   over another; it enforces that the value is one of the three and that the key's presence tracks
   certification. **The three meanings are carried in the register row and in this spec, not in the
   gate**, because they are not mechanically distinguishable, which is exactly the
   `growth_stages_annual` failure this field is avoiding.
2. Each entry's key set is exactly `{id, class, severity, stage, title, body_seasoned,
   body_beginner, sources, anchoring_urls}`.
3. `id` is kebab-case and **unique within the crop**. Per the CLAUDE.md join-key rule, an `id` is
   pinned at first authoring and never re-derived.
4. `class` in `{safety, harvest}`, closed.
5. `severity` in `{critical, high}`, closed (or absent entirely, if D3's alternative is taken).
6. `stage` is `null` or an id present in **this crop's** `growth_stages` (6.2).
7. `title`, `body_seasoned`, `body_beginner` all present and non-empty. **No em dash** in any of the
   three.
8. `sources` non-empty; every key resolves in `source_catalog`; every key present in
   `anchoring_urls` with a `url` and a `verified` date.
9. **A `class: safety` entry with an empty `sources` is a violation.** The 2026-09-06 spec's rule,
   made mechanical: *"an unsourced safety warning is exactly the class of confident copy this
   dataset refuses."*
10. The same rules apply to the top-level `container_safety` object's entries, checked once rather
    than per crop.

### 7.2 `register_completeness` needs a ruling on `title`

`register_completeness_gate` auto-rules any `_seasoned` / `_beginner` suffixed key as a dual-register
pair, so `body_seasoned` / `body_beginner` enters it for free. **`title` is a bare key** and will be
caught by the prose heuristic (`is_prose_shaped`: 25 or more characters with sentence structure, or
40 or more with a space). A short title such as "A full pot is heavy" is 19 characters and passes; a
longer one trips the gate and gets flagged as prose missing its sibling.

Recommendation: **rule `title` into `ruled_categorical` explicitly**, as `saucer_practice` and
`pet_safe.note` were ruled, with the same rationale: one plain line read identically in both
registers, above the dual-register body. Relying on the length heuristic instead would make the gate
fire on the length of the copy rather than on its kind, which is a trap for whoever writes the next
warning.

### 7.3 Provenance and the mutation harness

- **`field_additions`:** one record per authored warning, carrying URL, fetch date, sha256 and the
  **verbatim sentence** the warning was written from. The PLA-465 `EVIDENCE_HASHES` guard applies:
  no 64-hex token in the promote spec that is not a measured digest.
- **Suite and harness, PLA-215 bar:** one mutation per guard family; MUTATION-APPLIED marker plus a
  sentinel that must redden or the run exits `HARNESS DEAD`; `assert set(pre) == set(post)` before
  any value comparison; refusal-spec passes counted as passes; suite replay-pinned via
  `promote_fixture.COMMIT_FOR`. **Positive control runs the whole suite**, never a single driver.
- **Guards that cannot be shown reachable are removed, not shipped as coverage.**

**Five positive controls are owed by name**, because under the rulings the authored
population exercises none of them. This is the `guard-reachability-must-be-measured` lesson applied
at authoring time rather than discovered later:

1. **A non-null `stage`.** Every authored entry is `null`, so rule 6's live branch never executes.
   Fixture: an entry whose `stage` names an id that **is** in the crop's ladder (must pass) and one
   that is **not** (must fail). Two drivers, because a rule that only ever refuses is not shown to
   accept.
2. **A `class: harvest` entry.** PLA-7 authors none, so the class branch is vacuous on real data and
   PLA-142 would inherit an untested path.
3. **A second entry on one crop.** With at most one entry per crop, `id` uniqueness and `severity`
   ordering are both unexercised. A `[2 entries]` fixture is the control; a 1-entry fixture passes
   under any uniqueness rule and is not one.
4. **A non-empty `critical_warnings` at all, AND an `[]` one.** Under the rulings every certified
   crop ships **`null`**, so **both** the entry-shape rule set **and** the `[]` branch are unreached
   by live data. Two fixtures, not one: a crop with `[]` and a crop with entries, each asserted to
   pass rule 1 and each asserted to be distinguishable from `null` by the gate's own reader.
   Without these the gate is coverage in name only, which is the PLA-114 / PLA-162 failure mode the
   convention exists to stop.
5. **A `null` that is not silently coerced.** The one control the D2 reversal adds: a driver that
   sets a certified crop's `critical_warnings` to `[]` where the spec says `null` must **redden**,
   and vice versa. A gate that accepts all three states without distinguishing them would pass both
   mutations, which would make rule 1 look like coverage while enforcing nothing about which state
   a promote wrote. This is the `refusal-spec` pass in its useful form: prove the reader can tell
   `null` from `[]` before trusting any claim that the promote wrote the right one.

### 7.4 Release

`gate_all` 121/121; A61 presence 0 violations; `register_completeness` + `register_coverage` PASS;
`release_verify` clean in every section; collision gate holding; the full `tools/` tree with the two
known pre-existing failures read, not counted.

---

## 8. D5: consumers

### 8.1 The `critical_warnings` allowlist line first, and it is stronger than "silently dropped"

`critical_warnings` is a top-level key, and plant-app's `scripts/export-projection.mjs` classifies
every top-level key as SHIP or NEVER_SHIP. **Measured correction to PLA-581's framing:** an
unclassified key is not dropped silently. `projectRoster` **throws**:

> `export projection: N top-level crop key(s) are classified neither SHIP nor NEVER_SHIP: ... Decide
> deliberately in scripts/export-projection.mjs -- a new field does not ship just because nobody
> looked at it.`

So the ordering requirement in the issue ("the plant-app allowlist line first, then the promote, so
no consumer receives a key it drops silently") is **right, for a better reason**: without the line,
the app's export build **fails loudly** the first time it runs against the new canonical. That is the
designed behavior and it is good news. It also means the failure is discovered at build time rather
than as a missing card.

`container_safety` is a top-level **dataset** key, not a crop key, so it is outside
`SHIP_TOP_LEVEL`'s scope entirely and needs whatever the app's dataset-level projection does. That is
one line to check in the app session, and it is named here so it is not missed.

**Action: `'critical_warnings'` into `SHIP_TOP_LEVEL` in plant-app, before the promote.**

### 8.2 plant-astro ignores an unknown key, so no astro change is owed first

plant-astro reads canonical directly (`src/lib/dataset.ts`, `RawCrop` is
`{ slug: string; [key: string]: unknown }`). No allowlist, no zod strip, no throw. An unknown
top-level key is **inert** until a component reads it. Measured: `critical_warnings` appears **zero**
times in either consumer today.

### 8.3 "Renders in every experience mode": what that actually constrains

Measured on both consumers, "experience mode" is exactly **`beginner | seasoned`** and nothing else.
plant-app: `type Level = 'beginner' | 'seasoned'` (`src/lib/level.ts`), resolved per string by
`resolveLevelCopy`. plant-astro: a `.level-beginner` / `.level-seasoned` class on `<html>` driving
four CSS rules in `src/styles/globals.css`. **There is no depth or advanced mode in either
consumer.** PLA-7's "beginner experience / advanced experience" lists are a proposed design that was
never built.

Two consequences:

1. **Dual-register prose already renders in every mode by construction.** A `body_seasoned` /
   `body_beginner` pair cannot be hidden by mode; the register switch picks which of the two shows.
   So `class: safety` is a **forward constraint on the cards PLA-586 and PLA-539 are about to
   build**, not a fix for a defect that exists today. Worth saying, because the issue reads as
   though something is currently hidden.
2. **The mechanism that can hide a block is `.seasoned-only` / `.beginner-only`** (globals.css lines
   5 to 8), which hide an entire element by mode. That gives the render rule a checkable form:

> **A `class: safety` warning must never be rendered inside a `.seasoned-only` or `.beginner-only`
> wrapper, and never inside a collapsed or "advanced" section, on either consumer.**

That is testable in the consumer repos and is the honest expression of PLA-7's completion bullet.

### 8.4 The contract for PLA-586, stated so the card can be built without reading this spec

- Treat **absent**, **`null`** and **`[]`** alike: render no warnings block.
- Render every `class: safety` entry **above the fold, in both modes**, outside any `-only` wrapper.
- Render `class: harvest` entries following the mode, once PLA-142 authors them.
- Render `container_safety`'s three entries on every crop with `container_ok: true`, in both modes.
- Each entry renders its `title` plainly and its body through `RegisterText`.
- **No rendered sentence may state a weight, a load, or a pot count that no source named.** The
  balcony warning is a referral; rendering a number beside it would fabricate the claim.
- No em dashes in any rendered copy.

### 8.5 `container_safety`'s consumer line is NOT an allowlist entry, and it lands in the OTHER order

Ruling 1 says `container_safety` "needs its own allowlist line too". It needs its own consumer line,
and measurement says the mechanism is different from `critical_warnings`, in a way that **reverses
the ordering**. Both facts matter to whoever schedules the app work.

**`SHIP_TOP_LEVEL` governs top-level CROP keys only.** `projectRoster` iterates `Object.entries(crop)`
over the crops array. A top-level **dataset** key never reaches it. There are 19 top-level dataset
keys on `1721208e` (`source_catalog`, `zone_frost_data`, `control_methods`,
`pesticide_safety_education`, `soil_education`, ...), and **none of them appears in
`SHIP_TOP_LEVEL`.**

**The real mechanism is an explicit read and emit**, and the closest precedent is the one this
warning most resembles, `pesticide_safety_education`. In `plant-app/scripts/build-guides-data.mjs`:

```js
const rawMethods = raw.control_methods;              // :196
const rawSafety  = raw.pesticide_safety_education;   // :197
if (!rawMethods) throw new Error('control_methods missing from dataset; ...');          // :199
if (!rawSafety)  throw new Error('pesticide_safety_education missing from dataset; ...'); // :202
emit(CONTROL_OUT, JSON.stringify({ methods, safety }));                                  // :235
```

**The ordering is the opposite of `critical_warnings`, and this is the part that bites:**

| key | mechanism | must land | why |
|---|---|---|---|
| `critical_warnings` | `SHIP_TOP_LEVEL` entry | **BEFORE** the dataset promote | an unclassified crop key makes `projectRoster` throw |
| `container_safety` | explicit read + emit in `build-guides-data.mjs` | **AFTER** the dataset promote | the precedent pattern throws on a **missing** dataset key |

Two ways to run it, and the second is recommended: land the `SHIP_TOP_LEVEL` line early and the
`container_safety` read late, in two app commits either side of the promote; **or** write the
`container_safety` read with a tolerant guard (`raw.container_safety ?? null`, render nothing when
absent) so both app lines can land together before the promote and neither build ever breaks. The
tolerant form is what astro already does for this class of key, and it makes the app safe in both
directions.

**plant-astro needs nothing first, for either key.** It reads dataset-level sections directly through
`loadDatasetRaw()` with a nullish fallback already in the idiom, for example
`((await loadDatasetRaw()).control_methods ?? {})` at `IndoorGuide.astro:63`. Both `critical_warnings`
and `container_safety` are inert there until a component reads them.

---

## 9. The authorable population under the rulings

| what | count |
|---|---|
| Certified crops carrying `critical_warnings: null` (**not assessed**) | **121** |
| Certified crops carrying `[]` (**assessed, none found**) | **0**, and that is the point: PLA-142 earns each one |
| Certified crops carrying a non-empty `critical_warnings` | **0** |
| Shells carrying the key at all | **0** of 7 |
| Warnings authored into top-level `container_safety` | **3** (`balcony_load`, `container_material`, `hanging_security`) |
| Candidates **cut** by the 4.5 evidence test | **3** (mosquito, the lifting warning, any pounds figure) |
| Distinct T1 sources across the 3 kept warnings | **4** reads across 2 institutions (`uiuc_ext` x3, `csu_ext` x1) |
| Crops those 3 render on | **110** (`container_ok: true`) |
| Tip-over prose left where it is, to be rendered by PLA-586 / PLA-539 | **18 crops** |
| `field_additions` provenance records | **3**, one per shared warning |

**The promote writes 121 nulls and one object.** It is the smallest content promote in the arc, and
the whole of its risk is in the gate and the three-state rule, not in the bytes.

---

## 10. Sequencing

1. **Done:** this spec, amended once for the rulings. Held for a second read. Canonical unmoved.
2. **Done:** your rulings on D1 through D5 (section 0). One item is returned to you rather than
   closed: the tip-over app rule in 4.2, which has no input to fire on.
3. **PLA-466's promote lands first**, on canonical `1721208e`. PLA-580's promote follows.
4. **The two plant-app consumer lines** (8.5), which are different mechanisms with **opposite**
   ordering: `'critical_warnings'` into `SHIP_TOP_LEVEL` **before** the promote, and the
   `container_safety` read in `build-guides-data.mjs` **after** it, unless the read is written with
   a tolerant guard, which is the recommended form and lets both land together beforehand.
5. **The PLA-581 promote, a later session, against whatever canonical PLA-466 and PLA-580
   produce** -- explicitly **not** `1721208e`, which will be stale. That session **re-measures its
   base and re-runs section 12's dataset counts before authoring**, because every count here was
   taken on `1721208e`. Then: the A61 gate (shape armed, presence floor disarmed), the
   `register_completeness` `title` ruling, the suite, the harness with all five named positive
   controls, the 3 `container_safety` warnings, `field_additions` records, gauntlet on a scratch
   post-state, HOLD for approval, then the canonical write with `--expect-sha` and
   `A61_PRESENCE_ARMED = True` in the same commit.
6. **Register row 32** (30 is the highest live; PLA-580 takes 31). Same collision caveat as the gate
   id. **The row must document all three states**, per ruling 2; that is the part that stops this
   field becoming another `growth_stages_annual`.
7. **plant-astro (PLA-586)** builds the card to 8.4, itself blocked on PLA-535's submodule bump.
   Its contract and PLA-539's both gain the experience-mode rule in its checkable form (8.3):
   **no `.seasoned-only` or `.beginner-only` wrapper may hide a safety block.**
8. **PLA-142 notified that the shape is fixed** for its `harvest` class, and that it inherits three
   things: the five positive controls in 7.3, the overlap pass against `tips_by_stage` and
   `failure_diagnostics` that this spec does not touch, and **the `null` -> `[]` transition**. Every
   crop it assesses and finds clean moves from "not assessed" to "assessed, none found", which is
   the work ruling 2 exists to keep honest and is also a free progress metric for that arc.
9. **PLA-10 and PLA-7 notified** of 4.2: the wind-and-support app rule has no input in the dataset
   today (`height_inches` 0 occurrences, `planting_layout` `vertical` 0 occurrences,
   `footprint_inches` non-empty on 0, `mature_height_ft` null on all 18 tip-over crops).
10. **Close PLA-581** with the record: the measured absence of any per-crop container-safety datum,
    the three-state encoding and why `[]` on 121 was refused, where the three shared warnings live,
    and the render contract.

---

## 11. Out of scope, by name

PLA-142's **`harvest` class** and its overlap pass against `tips_by_stage` and `failure_diagnostics`;
**green-roof structural figures** (Penn State), which are an engineered assembly and do not transfer
to a pot; **mosquito control in container water gardens** (Illinois), formally CUT, evidence in 4.5, a different product with its
own page; the **`csu_ext` lifting warning** (4.4, a decision recorded rather than an omission); the
**94 saucer sentences**, which are root-rot guidance and correctly placed where they are; the **18
tip-over prose sentences**, left where they are for PLA-586 and PLA-539 to render (4.2);
**`min_pot_gallons` provenance** (PLA-533); the **astro card itself** (PLA-586) and the **app
changes** (PLA-539); `plants_per_pot` (PLA-580).

---

## 12. Measured facts this rests on (2026-09-21, canonical `1721208e`)

**Preflight.** `shasum -a 256 crops_data_final.json` =
`1721208ee0cbe4249ecf32ca3bd47a786f8a689cadcb7bb300d8d8ada4d82054`, matching `LATEST.txt`.
Worktree base `origin/main` = `e7264905b8668a0d8e8737c33d0cd1221ac41edd`.

**Source fetches.** All 2026-09-21, two user agents each; sha256 of the `curl` default-UA body.

| source key | URL | status | bytes | sha256 |
|---|---|---|---|---|
| `uiuc_ext` | `https://extension.illinois.edu/container-gardens/container-size` | 200 | 28,186 | `0b482e6ef1b9d9093dc0a0029e2753cf20bf787c7c329dd9ff23f7cbe0fe9705` |
| `uiuc_ext` | `https://extension.illinois.edu/container-gardens/container-material-choices` | 200 | 32,678 | `5ab9a68fcdf516a59c964c9ee6715ef0abfbd10a7ab0cac83682128e54637452` |
| `uiuc_ext` | `https://extension.illinois.edu/container-gardens/vegetable-containers` | 200 | 24,343 | `62b5e5c5f5ce244fb868faccdc9ac11e0babb38aad6be60a6776d97577ed8d89` |
| `uiuc_ext` | `https://extension.illinois.edu/container-gardens/growing-vines-containers` | 200 | 25,706 | `15bde72a5e6297e5304dfaa3c9ac5c06ba48dc727b7e0ab4ee83219d361145fc` |
| `uiuc_ext` | `https://extension.illinois.edu/container-gardens/problems-algae-and-mosquitoes` | 200 | 27,257 | `07399314a5bc14b9508f92a6e8a5fe957ffc78c10d57813e12d0784daaaa0501` |
| `uiuc_ext` | `https://extension.illinois.edu/container-gardens/hanging-baskets` | 200 | 30,339 | `761b9df044f12c76699bd167072f25a8b20768454be4083cc97b00a32c3bcca9` |
| `uiuc_ext` | `https://extension.illinois.edu/container-gardens/soil` | 200 | 32,632 | `ab95b7c4967644164ea80154f4632f522322c58322c602bb429276241e3e1534` |
| `uiuc_ext` | `https://extension.illinois.edu/container-gardens/watering` | 200 | 30,907 | `87649b7113c61b5f4c10e5887160f80bc0fe70ba8ef2ddd10704f476e14f9e8b` |
| `csu_ext` | `https://extension.colostate.edu/resource/container-gardens/` | 200 | 141,247 | `a0197e08d33decedb9ae7fe0ecd6cf7a50296559ac7d0d26623a83b02db2159d` |
| `uwi_hort` | `https://hort.extension.wisc.edu/articles/container-gardening/` | 200 | 130,994 | `0fda9a12156bae9aa8e1162ac7d1c1f878dcf0fc6fc03fdd4b8d1d25196d4d1e` |
| `uwi_hort` | `https://hort.extension.wisc.edu/articles/growing-vegetables-containers/` | 200 | 147,891 | `21ab568356909ae8ba6fa462c88176da16fdb25d7aa9c26a62a906906acf959e` |
| `umd_ext` | `https://extension.umd.edu/resource/types-containers-growing-vegetables` | 200 | 34,659 | `96521c5d0cf8860e7895a8c6da426ac48a372894c531431c64666bda8151f407` |
| `umd_ext` | `https://extension.umd.edu/resource/maintaining-container-grown-vegetables` | 200 | 36,871 | `e2ad3acfec22c992888eaabbd7185d86f241ab8cae3b63aae35bf95cd62963ac` |
| `psu_ext` | `https://extension.psu.edu/green-roofs-benefits-and-design-considerations` | 200 | 392,429 | `3dc6e547bb8338ead6ee24cabfe4564bf9f5f241d1478715f062038d510e9071` |
| `uga_ext` | `https://extension.uga.edu/publications/detail.html?number=C787&title=gardening-in-containers` | 200 | 295,048 | `fabc5b24daa0bd50e4606f0db04e7150ce08c1b63a9cc887ce6b001874e12c7f` |
| `umn_ext` | `https://extension.umn.edu/news/container-gardening-small-spaces-big-beauty-tiny-places` | **403** (2 UAs) | 83,208 | `ecbfd486ff26a032d92c6646660ca86bf89e012b74c842b64e9e18b7f4350a30` (block page) |

The two UMD hashes are byte-identical to the ones PLA-580's spec recorded on the same day, which is
a consistency check on both readings. All six source keys used above are admitted in
`source_catalog` at `tier: T1`, `source_class: university_extension`.

**Dataset.** 128 crops; **121** `verified_gs_arc`; **7** shells (`avocado`, `olive`, and the five
mushrooms). `critical_warnings`: **0** occurrences dataset-wide. `"class":"safety"`: **0**
occurrences. `container_ok: true` on **110** of 121 certified; `false` on 11. `container_path`:
`direct` 86, `rootstock` 8, `cultivar` 8, `tray` 8, `null` 11. `mature_height_ft` non-null on **16**
of 121 (`mature_spread_ft` 14). **81** distinct `growth_stages` ids roster-wide.
`container_notes` term scan over the 121 certified crops: balcony 11 (placement only), roof/rooftop
0, load limit 0, lbs figure 0, structural/engineer/code 0, tip/topple 18, mosquito 0, saucer 94
crops in 93 distinct sentences.

**Absence encoding across top-level list keys, certified crops.** `rootstock_options` absent 102 /
`[]` 2 / non-empty 17. `recipes` `[]` 117 / non-empty 4. `days_to_maturity` `[]` 30 / non-empty 91.
`mature_height_ft` `null` 105 / value 16. Six top-level list keys carry an explicit `null` on any
certified crop: `mature_height_ft` and `mature_spread_ft` (pairs, not collections),
`description_sources` (null on 1), `harvest_ramp_weeks` (null on 1), and `growth_stages_annual` /
`growth_stages_year_one`, which carry absent 98 / `null` 10 / `[]` 13 / **non-empty 0** each.

**Register / gates.** `docs/field_addition_register.md` holds **30** rows; 29 is `container_path`,
30 is plant dimensions; PLA-580's approved spec claims 31; this field is **32**. Highest
`whole_crop_gate` id in use is **A59**; PLA-580 claims **A60**; this spec assumes **A61**, with the
collision recorded in 7.1. `register_completeness_gate.is_prose_shaped` fires at 25 characters with
sentence punctuation, or 40 characters containing a space; `ruled_categorical` is the exemption
mechanism, with `saucer_practice` and `pet_safe.note` as precedents.

**Consumers.** plant-app `feat/community-foundation`: `SHIP_TOP_LEVEL` at
`scripts/export-projection.mjs:38-80` (`container_notes` present at line 44, `critical_warnings`
absent); the unclassified-key throw at `projectRoster`, `export-projection.mjs:204`;
`type Level = 'beginner' | 'seasoned'` at `src/lib/level.ts:3`. plant-astro `main`:
`src/lib/dataset.ts` reads canonical directly with `RawCrop = { slug: string; [key: string]: unknown }`
and no allowlist or schema strip; `src/components/shared/RegisterText.astro` emits both registers;
`src/styles/globals.css:5-8` carries the four `-only` / `-copy` mode rules. **`critical_warnings`
occurs 0 times in either repository.**

**Discrepancies recorded against the 2026-09-06 spec (section 5).** (a) "the container hazards the
block's prose already raises on **9 crops**" is not reproducible: balcony load 0, tip-over 18,
mosquito 0. (b) "a saucer-flooded pot as a root-rot and **mosquito** source where a source says so":
the only mosquito source found is scoped to container **water gardens**, and none of the 94 saucer
sentences mentions mosquitoes. (c) "where extension publishes the **weight of wet potting mix per
gallon**, that is the citable figure": no such figure was found in any source read, and Illinois
refers the question to an architect instead. (d) "`[]` is the common, legitimate value" is endorsed
and sharpened in 5.2: `[]` is the **only** empty value, and `null` becomes a violation.

**Measured for amendment 1 (2026-09-21, same canonical).**

*The tip-over app rule's inputs.* On the 18 tip-over crops: `mature_height_ft` is `null` on **all
18**; `container_path` is `direct` on **all 18** (a value shared by 86 of 121). The 16 crops that do
carry a height are `apple`, `blueberry`, `elderberry`, `fig`, `lavender`, `lemon`, `mulberry`,
`nectarine`, `oregano`, `pawpaw`, `peach`, `persimmon`, `pomegranate`, `rosemary`, `sage`, `thyme`;
**the intersection with the 18 is empty**. The inputs PLA-7's D3 actually names fare no better:
`height_inches` **0** occurrences dataset-wide, `"vertical"` **0** occurrences,
`planting_layout` present on **6** crops with every value `"block"`, `footprint_inches` key present
on 121 and non-empty on **0**.

*Top-level dataset keys.* **19** on `1721208e`: `crops`, `version`, `schema_version`,
`versioning_note`, `zone_frost_data`, `zone_sources`, `sources_schema_note`, `total_crops`,
`source_catalog`, `previous_remediations`, `last_remediation`, `soil_education`, `ph_education`,
`region_source_map`, `region_chill_delivered`, `region_chill_delivered_provenance`,
`control_methods`, `pesticide_safety_education`, `uscrn_soil_temp`. **None of them appears in
`SHIP_TOP_LEVEL`**, which confirms that allowlist governs crop keys only. `pesticide_safety_education`
is the nearest precedent for `container_safety` in both kind and mechanism.

*The dataset-level consumer mechanism.* plant-app `scripts/build-guides-data.mjs`: `raw.control_methods`
at `:196`, `raw.pesticide_safety_education` at `:197`, throws on a missing key at `:199` and `:202`,
emits at `:235`; `raw.region_chill_delivered` at `:107` with the same throw at `:109` and emit at
`:111`. plant-astro `src/components/guides/IndoorGuide.astro:63` reads
`((await loadDatasetRaw()).control_methods ?? {})`, the tolerant idiom.

**Corrections recorded against this document's own drafts.** (i) An early pass counted 18 tip-over
crops using a net that matched `potato` and `sweet-potato` on "harvest by **tipping out** the bag",
a harvest action rather than a hazard; the narrowed net excludes both and picks up `banana-pepper`
and `bell-pepper`, landing on 18 again for different reasons. The coincidence is recorded so the
number is not mistaken for a stable count under any net. (ii) A wind net returned 8 crops, of which
4 are the corn crops describing wind **pollination**; the tip-plus-wind population is 4.
(iii) **The first draft's D2 was wrong** and section 5.2 says so against itself: it recommended `[]`
on all 121 with `null` a violation, which would have written an unsourced negative into every record
for a class (`harvest`) nobody has assessed. It reasoned about the `safety` class and generalized to
a two-class field. (iv) The same draft read `growth_stages_annual`'s three states as evidence that a
third state is incoherent; the defect there is that its `null` was **never documented**, and 5.1 is
amended to say so. (v) The first draft said `container_safety` "needs whatever the app's
dataset-level projection does ... one line to check in the app session"; measured, there is no
dataset-level projection at all, and 8.5 now gives the mechanism and the **reversed ordering** that
finding produces.
