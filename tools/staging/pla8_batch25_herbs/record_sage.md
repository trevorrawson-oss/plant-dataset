# PLA-8 BATCH 25 -- RECORD / SOURCE PASS: **sage** (`sage`, *Salvia officinalis*)

Reviewer pass date: **2026-09-04**. Canonical read-only at
`a9c84847fe2e0ad595db8cf9cc7d7e82ac65803e3284e16071be6d536bf9dad7`. No repo file was modified
except this one.

7 problems (4 pests, 3 diseases). All seven carry no `sources` and no `anchoring_urls`.
**All seven are TRUE and all seven are now anchorable at Tier 1.** Zero UNSOURCED-NOT-FOUND.

---

## 0. THREE CROSS-CUTTING FINDINGS -- read these before the per-problem sections

### 0a. The seven problems came from ONE sentence, and the crop's own cert log says so

`sage.verification_status.verification_log_ref` (Batch-2 Wave-3 REDO cert, 2026-07-06) already
contains the string **"NCSU pest/disease lists confirmed."** The NC State Extension Gardener Plant
Toolbox entry for *Salvia officinalis* -- which is `sources_summary.primary[ncsu_ext]` on this
record -- carries this single field:

> "Possible insects include leaf hoppers, slugs, spider mites, and spittlebugs. Root rot, powdery
> mildew, and verticillium wilt can occur."

That is a 1:1 map onto the record's seven problems, in order, with no additions and no omissions.

**So this is not a truth gap; it is a FIELD-LEVEL provenance gap.** The claims were adjudicated at
cert time against a real, still-live, admitted T1 document, and the anchor was recorded at the
`sources_summary` level and in the log prose but never written into the `pests[]` / `diseases[]`
entries. (`a claim lives in FIELDS`; `cert log already adjudicated the band`.) The fix at authoring
is to attach anchors, not to re-litigate whether the problems belong.

The same log also records: *"S1 struck the unsupported 'white flies' from the Leafhoppers symptom
strings (no cited page names whiteflies; the phrasing conflated leafhoppers with a different
pest)."* That excision is why the Leafhoppers entry today reads as content-free -- see §4.

### 0b. `type: "mite"` on sage is CORRECT. Three siblings are wrong, and it is not cosmetic.

Sage is the only crop in this batch typing spider mites as `mite`. Oregano, rosemary and thyme say
`insect`. Roster-wide the vote is not close: **30 spider/citrus/eriophyid-mite entries are typed
`mite`**, and the only `insect`-typed ones are exactly oregano, rosemary, thyme (all uncertified,
all in this batch) plus `nasturtium`'s combined "Whiteflies and spider mites" (id `whiteflies`,
where `insect` is defensible because whiteflies dominate the entry). Mint types it `None`,
lemongrass `pest`.

This is load-bearing, not taxonomy pedantry. `tools/control_ladder_gate.py` (wired into
`whole_crop_gate` as **A56**) maps problem `type` to legal `applies_to` targets:

```
"insect": {insect_soft_bodied, insect_chewing, insect_boring, insect_general}
"mite":   {mite, insect_general}
```

Computed against `control_methods.json` (64 methods), the difference for a spider-mite ladder is:

| method | `applies_to` | legal under `mite` | legal under `insect` |
|---|---|---|---|
| `water_spray` | insect_soft_bodied, mite | yes | yes |
| `insecticidal_soap` | insect_soft_bodied, mite | yes | yes |
| `horticultural_oil` | insect_soft_bodied, insect_general, mite | yes | yes |
| `augmentative_release` | insect_soft_bodied, mite, insect_general, insect_chewing | yes | yes |
| **`sulfur`** | fungal_foliar, **mite**, disease_general | **yes** | **NO -- A56 fails** |
| **`even_watering`** | physiological, **mite**, bacterial | **yes** | **NO -- A56 fails** |

`sulfur` is the classic soft-chemical miticide and `even_watering` is the cultural rung that
matches every source's "water-stressed plants are highly susceptible." **Typing a spider mite
`insect` makes both illegal.** Sage needs no change. Report to the batch orchestrator: oregano,
rosemary and thyme should be corrected to `mite` before their ladders are authored, or their
ladders will be built around a gate-imposed absence nobody notices.

(`applies_to` also has a distinct `mollusk` target -- sage's slug entry is correctly typed. Note
the consequence for §3: `mollusk` maps to `{mollusk}` **only**, so a slug ladder may draw on just
8 methods -- `handpick`, `slug_traps_barriers`, `iron_phosphate_slug_bait`, `water_at_the_base`,
plus the four `any` methods. **`airflow_spacing` is NOT legal on a mollusk problem**, which the
record's slug prevention prose currently leans on.)

### 0c. Sage's leafhopper and lavender's/rosemary's spittlebug resolve to different id decisions

Short version, evidence in §4 and §1:

- **Leafhoppers on sage are a Lamiaceae-specialist direct-feeding pest** (*Eupteryx decemnotata*,
  *E. melissae*), **not** an aster-yellows or curly-top vector. Sage must NOT reuse `leafhoppers`
  (cilantro's id, framed as an aster-yellows / curly-top vector) and must NOT reuse
  `aster-leafhoppers` (parsnip, cosmos). It needs a **new id**. `match the TAXON, not the common
  name`.
- **Spittlebugs**: no crop in the dataset carries a spittlebug id, so this batch mints the family.
  No admitted document names a spittlebug species **on sage**. RHS names *Philaenus spumarius* on
  lavender and rosemary but its host list does not include sage. The honest call is **one shared
  generic id across sage / lavender / rosemary** (all three records are generic-name,
  generic-organism), pinned once before fan-out.

---

## Spittlebugs [pests] -- severity low, type insect
**STATUS: UNSOURCED-FOUND**

**ORGANISM:** umbrella -- family Cercopidae, per uc_ipm. Most probably *Philaenus spumarius*
(meadow spittlebug), but **no read document names any spittlebug species on *Salvia officinalis***.
UC IPM names three California species: *Clastoptera lineatocollis*, *Philaenus spumarius*,
*Aphrophora permutata*. RHS names "mainly common meadow spittlebug *Philaenus spumarius*" and lists
lavender and rosemary as hosts but **not** sage. Cannot be resolved to a binomial on sage from an
admitted source.

**ANCHORS:**

`ncsu_ext` https://plants.ces.ncsu.edu/plants/salvia-officinalis/ -- verified 2026-09-04
  > "Possible insects include leaf hoppers, slugs, spider mites, and spittlebugs."

`uwi_hort` https://hort.extension.wisc.edu/articles/sage-salvia-officinalis/ -- verified 2026-09-04
  > "Some possible problems include slugs, spider mites, spittle bugs, root rot and wilt."
  > "Sage has few pests when grown in well-drained soil."

`uc_ipm` https://ipm.ucanr.edu/home-and-landscape/spittlebugs/ -- verified 2026-09-04
  > "These sucking insects (family Cercopidae) can at least occasionally be found on almost any plant."
  > "Spittlebugs' obvious and occasionally abundant masses of white foam on foliage and stems may be annoying, but they do not seriously harm established woody plants in landscapes."
  > "Ignore spittlebugs or wash nymphs off with a forceful stream of water."
  > "Cut spittlebug-infested weeds in the spring before the insects mature and spread."
  > "Overwintering occurs as tiny eggs on or in stems or needles. Spittlebugs commonly have one or two generations per year in California."
  > "Spittlebugs are more likely to become abundant on woody plants when they migrate from nearby herbaceous hosts."

`rhs` https://www.rhs.org.uk/biodiversity/cuckoo-spit-spittlebugs -- verified 2026-09-04
  > "Various species but mainly common meadow spittlebug _Philaenus spumarius_"
  > "May-July"
  > "Apart from producing the 'spit' these insects have little detrimental effect on plants"
  > "Spittlebugs are not a pest, so please don't remove them; they are an innocent carrier of _Xylella_ outside of the UK and are part of the biodiversity a healthy garden ecosystem."

**RECORD CLAIMS THAT HOLD:**
- Spittlebugs occur on sage -- `ncsu_ext`, `uwi_hort`.
- "Frothy white foam on stems" with a nymph inside -- `uc_ipm` ("masses of white foam on foliage and
  stems"), `rhs`.
- "in late spring" -- `rhs` "May-July" is the closest published window; it is a UK window, so this is
  supported but not US-specific.
- "It looks alarming but rarely harms an established sage plant" / "damage is mostly cosmetic" --
  `uc_ipm` ("do not seriously harm established woody plants"), `rhs` ("little detrimental effect").
  **Severity `low` is well supported.**
- "Knock them off with a strong spray of water ... no treatment is needed for plant health in most
  cases" -- `uc_ipm` verbatim ("Ignore spittlebugs or wash nymphs off with a forceful stream of
  water").

**RECORD CLAIMS WITH NO ANCHOR:**
- "Spittlebug nymphs sheltering in their own foam **while sipping sap**." (Direction is right --
  UC IPM's fuller text calls them sucking insects that feed on xylem fluid -- but the sentence as
  written is not carried by any sentence I read on a sage-scoped page.)
- "Numbers are usually low" on sage specifically. UC IPM says the opposite is possible ("occasionally
  abundant").
- "Give plants full sun and airflow and do not overwater; vigorous sage shrugs off minor pests." The
  *drainage* half is anchored (`ncsu_ext`, `uwi_hort`); the claim that vigor deters spittlebugs is not
  in any document. UC IPM's actual cultural lever is different -- see below.

**RECORD CLAIMS THAT ARE WRONG:** none found.

**LADDER-RELEVANT FACTS the record does not carry:**
- **The real cultural rung is weed management, not plant vigor.** `uc_ipm`: "Spittlebugs are more
  likely to become abundant on woody plants when they migrate from nearby herbaceous hosts" and
  "Cut spittlebug-infested weeds in the spring before the insects mature and spread." That maps to
  `weed_host_control` (legal under `insect`).
- Overwinters **as eggs on or in stems**; one or two generations per year in California (`uc_ipm`).
  A dormant-season stem cleanup therefore has a mechanism.
- UC IPM's explicit top recommendation is **do nothing** ("Ignore spittlebugs"). RHS goes further:
  "please don't remove them." A one-rung or two-rung ladder is the honest shape here.
- *Philaenus spumarius* is the principal European vector of *Xylella fastidiosa* (`rhs`). **Do not
  put this in consumer copy** -- RHS is explicit it is "an innocent carrier of *Xylella* outside of
  the UK," and no US extension source raises it for garden sage. Flagging it only so a later pass
  does not "discover" it and over-escalate the entry.

---

## Spider mites [pests] -- severity low, type mite
**STATUS: UNSOURCED-FOUND**

**ORGANISM:** umbrella -- webspinning spider mites, genus *Tetranychus*, per `ucanr_ext_spider_mites`:
"Most common ones are closely related species in the *Tetranychus* genus and can't be reliably
distinguished in the field." No document resolves a species on sage. `umd_ext` supplies the useful
consumer-facing taxon fact: they are **not insects**.

**ANCHORS:**

`ncsu_ext` https://plants.ces.ncsu.edu/plants/salvia-officinalis/ -- verified 2026-09-04
  > "Possible insects include leaf hoppers, slugs, spider mites, and spittlebugs."

`uwi_hort` https://hort.extension.wisc.edu/articles/sage-salvia-officinalis/ -- verified 2026-09-04
  > "Some possible problems include slugs, spider mites, spittle bugs, root rot and wilt."

`clemson_hgic` https://hgic.clemson.edu/factsheet/salvia/ (HGIC 1174, updated Jan 4 2021) -- verified 2026-09-04
  > "Potential problems for salvias include damping-off of seedlings, stem and root rots, powdery mildew, Botrytis blight, aphids, spider mites, and whiteflies."

`clemson_hgic` https://hgic.clemson.edu/factsheet/herbs/ (HGIC 1311, updated Nov 25 2019) -- verified 2026-09-04
  > "Aphids and spider mites can be a problem."
  > "Spider mites thrive in dry conditions and can be discouraged by spraying the plants with a strong stream of water regularly during periods of drought."

`ucanr_ext_spider_mites` https://ipm.ucanr.edu/PMG/PESTNOTES/pn7405.html -- verified 2026-09-04
  > "Spider mites prefer hot, dusty conditions and usually are first found on trees or plants adjacent to dusty roadways or at margins of gardens. Plants under water stress also are highly susceptible."
  > "In gardens and on small fruit trees, regular, forceful spraying of plants with water often will reduce spider mite numbers adequately. Be sure to get good coverage, especially on the undersides of leaves."
  > "If a treatment for mites is necessary, use selective materials, preferably insecticidal soap or insecticidal oil."
  > "Oils and soaps must contact mites to kill them, so excellent coverage, especially on the undersides of leaves, is essential."
  > "Be sure mites are present before you treat"

`umd_ext` https://extension.umd.edu/resource/herb-problems -- verified 2026-09-04
  > "Spider mites are tiny, eight-legged non-insects (related to spiders) about the size of a punctuation period."

**RECORD CLAIMS THAT HOLD:**
- Spider mites occur on sage -- `ncsu_ext`, `uwi_hort`; on salvias -- `clemson_hgic` 1174; on herbs --
  `clemson_hgic` 1311, `umd_ext`.
- "hot, dry, dusty conditions" and "drought-stressed" -- `ucanr_ext_spider_mites` verbatim.
- "Fine stippling or bronzing of the leaves and faint webbing" -- `ucanr_ext_spider_mites` (webspinning
  mites; stippling is that document's damage sign).
- "Rinse the foliage with a strong spray of water ... repeating every few days" --
  `ucanr_ext_spider_mites` and `clemson_hgic` 1311 verbatim on the water-spray rung.
- "insecticidal soap helps in bad cases" -- `ucanr_ext_spider_mites` verbatim.
- "avoid drought stress on containers" -- `ucanr_ext_spider_mites` ("Plants under water stress also are
  highly susceptible").
- **Severity `low` holds**: `uwi_hort` "Sage has few pests when grown in well-drained soil";
  `clemson_hgic` 1174 "Salvias have few problems when grown in ideal conditions."

**RECORD CLAIMS WITH NO ANCHOR:**
- "stressed **indoor** plants" / "on indoor plants". Plausible and standard, but no read document
  says it for sage. (Mint's certified record makes the same indoor claim against
  `uc_ipm`'s mint page; there is no equivalent UC IPM sage page -- see §7 note.)
- "**still air**" as a driver. UC IPM says hot and dusty, and water stress; it does not name stagnant
  air. "Maintain good airflow" is anchored for *foliar disease* on sage (`ncsu_ext`), not for mites.

**RECORD CLAIMS THAT ARE WRONG:** none found.

**LADDER-RELEVANT FACTS the record does not carry:**
- **Coverage is the whole game**: "Oils and soaps must contact mites to kill them, so excellent
  coverage, especially on the undersides of leaves, is essential" (`ucanr_ext_spider_mites`). Every
  rung above `handpick` fails without underside coverage.
- **A published monitoring signal**: "Be sure mites are present before you treat"
  (`ucanr_ext_spider_mites`) -- the closest thing to a threshold in the literature, and the natural
  first rung.
- `sulfur` is a legal rung ONLY because sage types this `mite` (see §0b). It is a genuine miticide
  and belongs in the soft-chemical band.
- Dust suppression (hosing dusty foliage, garden-edge/roadside siting) is a distinct cultural rung
  the record gestures at ("hose off dust") but does not connect to the source's mechanism.
- Oregano's certified sibling entry adds a rung sage could reuse: "A hard harvest or shear removes
  much of the infested growth." Sage is sheared in spring anyway; no admitted document states this
  for sage, so it would need its own anchor.

---

## Slugs and snails [pests] -- severity low, type mollusk
**STATUS: UNSOURCED-FOUND** (with a naming caveat: only **slugs** are documented on sage)

**ORGANISM:** umbrella. `ucanr_ext_snails_slugs` names *Cornu aspersum* (brown garden snail),
*Deroceras reticulatum* (gray garden slug), *Lehmannia poirieri*, *L. valentiana*, *Limacus flavus*,
*Milax gagates*. **No read document names a species on sage**, and the two documents that put this
problem on sage both say "slugs" only, never "snails."

**ANCHORS:**

`ncsu_ext` https://plants.ces.ncsu.edu/plants/salvia-officinalis/ -- verified 2026-09-04
  > "Possible insects include leaf hoppers, **slugs**, spider mites, and spittlebugs."

`uwi_hort` https://hort.extension.wisc.edu/articles/sage-salvia-officinalis/ -- verified 2026-09-04
  > "Some possible problems include **slugs**, spider mites, spittle bugs, root rot and wilt."

`ucanr_ext_snails_slugs` https://ipm.ucanr.edu/PMG/PESTNOTES/pn7427.html -- verified 2026-09-04
  > "Snails and slugs are most active at night and on cloudy or foggy days."
  > "Switching from sprinkler irrigation to drip irrigation will reduce humidity"
  > (hand-picking) search "at night or in the early morning" with a flashlight
  > (trapping) "boards raised off the ground by 1-inch runners" ... "scrape off the accumulated snails and slugs daily"
  > "copper reacts with the slime that snails and slugs secrete, causing a disruption in their nervous system"
  > "Iron phosphate baits...have the advantage of being safer for use around children, domestic animals, birds, fish, and other wildlife."
  > "metaldehyde baits are particularly poisonous to dogs and cats"

**RECORD CLAIMS THAT HOLD:**
- Slugs occur on sage -- `ncsu_ext`, `uwi_hort`.
- Night feeding, damp/shady preference -- `ucanr_ext_snails_slugs` verbatim.
- "Hand-pick at night, remove damp hiding places, and use traps or iron-phosphate bait" -- all three
  rungs verbatim in `ucanr_ext_snails_slugs`.
- The beginner string's pet-safety hedge ("iron-phosphate bait, which carries less risk around pets
  than the older metaldehyde baits") is **exactly** what `ucanr_ext_snails_slugs` says, and it is
  correctly hedged rather than absolute. (`safety absolutes span crops` -- this one is clean.)
- "Plant in full sun with good drainage" as the siting defense -- `ncsu_ext` ("intolerant of wet or
  poorly drained soils"), `uwi_hort` ("sunny location with well-drained soil"), `clemson_hgic` 1311
  ("require excellent drainage and dry soil in full sun").
- **Severity `low` holds** on the same two "few pests / few problems" sentences.

**RECORD CLAIMS WITH NO ANCHOR:**
- **"snails"**. Neither sage-scoped document names snails. The record name "Slugs and snails" is
  wider than the evidence. (This is a naming, not a correctness, issue -- UC IPM manages the two as
  one unit -- but it should be a deliberate decision, not a drift.)
- "mainly on young or newly set plants" and "around young plants" -- a reasonable general slug fact,
  but not stated for sage in anything I read.
- "wet mulch, crowding" as favoring conditions -- UC IPM names moisture and hiding places, and names
  irrigation; it does not name mulch or crowding.

**RECORD CLAIMS THAT ARE WRONG:** none found.

**LADDER-RELEVANT FACTS the record does not carry:**
- **Copper barriers** and their mechanism (`ucanr_ext_snails_slugs`) -- maps to
  `slug_traps_barriers`, a legal `mollusk` rung the record never mentions.
- **Irrigation method is a rung**: "Switching from sprinkler irrigation to drip irrigation will
  reduce humidity." Maps to `water_at_the_base`, which is `mollusk`-legal.
- Board traps with a **daily** service interval -- the record says "use traps" without the operating
  detail that makes them work.
- **A56 constraint the ladder author must respect**: `type: mollusk` maps to `{mollusk}` only, so the
  legal method pool is 8 wide (`handpick`, `slug_traps_barriers`, `iron_phosphate_slug_bait`,
  `water_at_the_base`, `crop_rotation`, `garden_sanitation`, `resistant_varieties`,
  `floating_row_cover`). **`airflow_spacing` is not legal here**, so the record's "space plants for
  airflow" prevention sentence cannot be carried as a rung -- fold it into `water_at_the_base` or
  `garden_sanitation` instead.

**ID NOTE (report only, do not act):** the record name "Slugs and snails" matches the 11-crop
majority id `slugs-and-snails` (arugula, basil, bok-choy, calendula, lettuce-leaf, marigold,
nasturtium, sweet-alyssum, sweet-pea, swiss-chard, viola) exactly. The other two members of the
family PLA-448 flagged are `slugs` (strawberry, severity medium) and `snails-and-slugs` (artichoke,
"Snails and slugs (*Cornu aspersum*, *Deroceras reticulatum*)"). **`slugs-and-snails` is the obvious
reuse.** Pin it before fan-out.

---

## Leafhoppers [pests] -- severity low, type insect
**STATUS: UNSOURCED-FOUND** -- presence and severity anchored, **but the record prose describes the
wrong thing and must be re-authored.** This is the entry that most needs the next pass's attention.

**ORGANISM:** ***Eupteryx decemnotata*** (Rey), the Ligurian leafhopper, and/or ***Eupteryx
melissae***, the sage leafhopper -- both Cicadellidae: Typhlocybinae, both **Lamiaceae
specialists**. Binomials from `uc_ipm` and `uf_ifas` (*E. decemnotata*) and `rhs` (both species,
named together as the pair that attacks sage).

> **NOT an aster-yellows or curly-top vector.** UC IPM's leafhopper page enumerates the vector
> species and their host ranges in the same paragraph and sage appears in neither list: aster
> yellows (*Macrosteles quadrilineatus*) "can damage carrots, celery, lettuce, potatoes, other
> vegetables, and numerous herbaceous ornamentals"; curly top (*Circulifer tenellus*) "damages many
> vegetables, including beans, beets, melons, potatoes, peppers, and tomatoes." Neither UF/IFAS
> EENY-750 nor RHS attributes any pathogen transmission to *Eupteryx*.

**ANCHORS:**

`ncsu_ext` https://plants.ces.ncsu.edu/plants/salvia-officinalis/ -- verified 2026-09-04
  > "Possible insects include **leaf hoppers**, slugs, spider mites, and spittlebugs."

`uc_ipm` https://ipm.ucanr.edu/home-and-landscape/leafhoppers/ -- verified 2026-09-04
  > "The Ligurian leafhopper (_Eupteryx decemnotata_) is a pest of mint, rosemary, **sage**, and other plants in the mint family (Lamiaceae)."
  > "Leafhopper feeding causes leaves to develop pale specks (stippling). Leaves and shoot tips fed upon by an abundance of leafhoppers may turn yellow then brown and curl and die."
  > "Leafhoppers also excrete honeydew on which blackish sooty mold grows."
  > "As nymphs molt into the next (larger) instar, they leave whitish cast skins on the underside of foliage."
  > "In most situations, leafhoppers are just an annoyance or curiosity and do not threaten plant survival. Generally, no control of them is needed in gardens and landscapes."

`uf_ifas` (EDIS EENY-750 / IN1290) https://ask.ifas.ufl.edu/publication/IN1290 -- verified 2026-09-04
  > "EENY-750/IN1290: Ligurian leafhopper _Eupteryx decemnotata_ (Rey) (Insecta: Hemiptera: Cicadellidae: Typhlocybinae)"
  > "feeding activity is associated with severe yellowing and branch drying of sage (_Salvia officinalis_) and rosemary (_Rosmarinus officinalis_)"
  > "unsightly yellowing and stippling"
  > "In Italy, it is thought that most of the population overwinters as eggs."
  > "At 20°C, Ligurian leafhopper eggs hatch within 20 to 26 days."
  > "In Poland, herb producers reportedly vacuum plants and employ yellow sticky traps."

`rhs` https://www.rhs.org.uk/herbs/sage/grow-your-own -- verified 2026-09-04
  > "The leaves can be damaged by rosemary beetles, sage leafhoppers and capsid bugs, but these don't generally cause severe problems so control isn't necessary."

`rhs` https://www.rhs.org.uk/biodiversity/sage-and-ligurian-leafhoppers -- verified 2026-09-04
  > "_Eupteryx melissae_ and _E. decemnotata_"
  > "Many aromatic plants in the Lamiaceae family, including sage, mints, lavender, bergamot, marjoram, oregano, rosemary, basil, thyme and lemon balm"
  > "Coarse pale spotting on upper leaf surface. Leafhoppers may be seen on the underside of leaves"
  > "April to September"
  > "Encourage predators and other natural enemies of leafhoppers, in the garden, such as birds, ladybirds, wasps and ground beetles."
  > "Affected herbs are safe to eat."

**RECORD CLAIMS THAT HOLD:**
- Leafhoppers occur on sage -- `ncsu_ext`, `uc_ipm`, `rhs`, `uf_ifas`.
- "Sap-feeding insects" -- `uc_ipm`.
- "rarely needs spraying" / "you usually do not need to do anything" -- `uc_ipm` verbatim ("Generally,
  no control of them is needed in gardens and landscapes"), `rhs` ("control isn't necessary").
- "use insecticidal soap if numbers climb" -- `uc_ipm` names horticultural oil, insecticidal soap or
  neem oil as the sprays when a spray is warranted.
- **Severity `low` is supported** by `uc_ipm` and `rhs`, though `uf_ifas` pushes against it (below).

**RECORD CLAIMS WITH NO ANCHOR:**
- "more likely on stressed or crowded plants than on healthy sage" -- no document says this. The
  documents say sage is a *preferred host*, full stop; the driver is host family, not plant stress.
- "Full sun, lean soil, and good spacing keep sage unstressed and **unattractive to these pests**" --
  the conclusion is unsupported and, given the host-specialist biology, probably false.
- "Rinse them off with water" -- UC IPM lists sprays (oil, soap, neem) for leafhoppers; a plain water
  rinse is the *spider mite* and *spittlebug* recommendation, not the leafhopper one. Borrowed rung.

**RECORD CLAIMS THAT ARE WRONG (or so incomplete as to mislead):**
- **The symptom strings name no symptom.** "Occasional small hopping insects on the foliage" /
  "tiny hopping bugs on the leaves" describe *seeing the insect*, not *seeing the damage*. Every
  document agrees the diagnostic sign is **stippling / coarse pale mottling on the upper leaf
  surface**, with the insects on the **undersides** where a gardener will not look. `uc_ipm`:
  "Leafhopper feeding causes leaves to develop pale specks (stippling)." `rhs`: "Coarse pale
  spotting on upper leaf surface. Leafhoppers may be seen on the underside of leaves." A reader
  following the current record will fail to recognize the problem. This is the residue of the
  2026-07-06 whitefly excision recorded in the cert log (§0a) -- the correction removed a false
  claim and left a hole.
- **"the plant has few serious pests"** is carried inside the *cause* field of a specific pest. It is
  true of sage overall (`uwi_hort`) but it is not the cause of leafhoppers, and it argues the reader
  out of acting.

**LADDER-RELEVANT FACTS the record does not carry:**
- **Overwinters as eggs in leaf/stem tissue** (`uf_ifas`; VCE adds hatch at spring warming). Season
  runs **April to September** (`rhs`). A spring shear before egg hatch is a real cultural lever.
- **Yellow sticky traps and vacuuming** are the published non-spray controls for this exact species
  (`uf_ifas`: "In Poland, herb producers reportedly vacuum plants and employ yellow sticky traps").
  `yellow_sticky_traps` is already a catalog method and is `insect`-legal. This is the single most
  useful rung the record is missing.
- **Conserve natural enemies** (`rhs`: birds, ladybirds, wasps, ground beetles; `uf_ifas`: *Anagrus
  atomus*-like parasitoids). Maps to `beneficial_predators`.
- **The harvest-safety answer**: "Affected herbs are safe to eat" (`rhs`). Consumers will ask.
- **A severity tension to adjudicate.** `uc_ipm` and `rhs` say annoyance-grade. `uf_ifas` EENY-750
  says feeding "is associated with severe yellowing and branch drying of sage (*Salvia officinalis*)"
  and with reduced essential-oil content in *Eupteryx*-fed oregano. That is a commercial-herb-crop
  framing versus a garden framing. **`low` is defensible for a home garden** and I recommend keeping
  it, but the record should carry the "an abundance of leafhoppers may turn yellow then brown and
  curl and die" escalation (`uc_ipm`) so `low` is not read as "harmless."

**ID NOTE (report only, do not act):** sage must NOT take `leafhoppers` (cilantro-coriander,
"Leafhoppers (and aster yellows / curly top)") nor `aster-leafhoppers` (parsnip, cosmos). Those ids
carry a vector claim the sage documents refute for this taxon. `pest names are not join keys` and
`id reuse needs a taxon check` both apply. A new id is required -- I suggest something naming the
genus rather than the family, and note that **mint, rosemary, thyme, oregano, basil and lavender are
all named hosts of the same two *Eupteryx* species**, so whatever id is minted here should be minted
once for the whole batch and reused, not regenerated per crop.

---

## Root and stem rot [diseases] -- severity high, type fungal
**STATUS: UNSOURCED-FOUND**

**ORGANISM:** **umbrella -- multiple organisms.** Per `uwi_hort` (D0094): "*Phytophthora* spp. and
*Pythium* spp. (both water molds), and *Rhizoctonia solani* and *Fusarium* spp. (both true fungi)."
`clemson_hgic` adds *Thielaviopsis*. `umd_ext` adds *Sclerotium rolfsii* (southern blight) as a
hot-weather herb killer. **No admitted document resolves a single organism on *Salvia officinalis*.**

The only sage-specific taxon evidence I found is **JOURNAL-ONLY and I could not read it**: APS
*Plant Disease* 81(8):959, 1997, "Phytophthora Root and Crown Rot of Sage Caused by *Phytophthora
cryptogea* in California" (Salinas Valley, Monterey County, 1996). The catalog carries no journal
entries, so it is not citable; recording it here as a catalog-addition candidate, flagged **UNREAD**
(I have only a search-engine summary, not a verified fetch).

**ANCHORS:**

`ncsu_ext` https://plants.ces.ncsu.edu/plants/salvia-officinalis/ -- verified 2026-09-04
  > "Root rot, powdery mildew, and verticillium wilt can occur."
  > "It is intolerant of wet or poorly drained soils."
  > "Providing well-drained soil and good air circulation will reduce the possibility of pests and foliar diseases."
  > (Problems tag on the page: "#Frequent Disease Problems")

`uwi_hort` https://hort.extension.wisc.edu/articles/sage-salvia-officinalis/ -- verified 2026-09-04
  > "Some possible problems include slugs, spider mites, spittle bugs, root rot and wilt."
  > "Sage grows best in a sunny location with well-drained soil."
  > "Sage has few pests when grown in well-drained soil."

`uwi_hort` https://hort.extension.wisc.edu/articles/root-and-crown-rots/ (Hudelson & Jull, D0094, last revised 03/01/2024) -- verified 2026-09-04
  > "_Phytophthora_ spp. and _Pythium_ spp. (both water molds), and _Rhizoctonia solani_ and _Fusarium_ spp. (both true fungi)"
  > (the pathogens) "prefer wet soil conditions"
  > (they can) "survive for long periods (years to decades) in soil"
  > "REDUCE SOIL MOISTURE! Provide enough water to fulfill a plant's growth needs and prevent drought stress, but **do not** over-water."
  > (prevention) plant in well-drained sites, set "the root collar just at the soil surface", add organic material to improve drainage, limit mulch to three inches, "decontaminate tools and footwear" with "10% bleach solution or 70% alcohol"

`clemson_hgic` https://hgic.clemson.edu/factsheet/salvia/ (HGIC 1174) -- verified 2026-09-04
  > "Potential problems for salvias include damping-off of seedlings, stem and root rots, powdery mildew, Botrytis blight, aphids, spider mites, and whiteflies."

`clemson_hgic` https://hgic.clemson.edu/hot-topic/drying-up-root-and-crown-rot-pathogens/ (Jeffers, Mar 1 2019) -- verified 2026-09-04
  > "_Phytophthora_ and _Pythium_, or by species of fungi: _Rhizoctonia_, _Fusarium_, and _Thielaviopsis_"
  > "_Rhizoctonia_ ... prefers a moist soil for infection", "_Phytophthora_, being a water mold, prefers a wet soil"
  > "Some fungicides are effective, but only at suppressing these diseases"

`umd_ext` https://extension.umd.edu/resource/herb-problems -- verified 2026-09-04
  > "Poorly drained soil, water that pools due to the slope or plants being overwatered can cause irreversible damage to herbs."
  > "Southern blight is caused by the fungus Sclerotium rolfsii. This fungus can attack many herbaceous perennials including herbs."  (and: it "is active only during hot weather")
  > "Excessively wet, cold soil can cause Mediterranean herbs such as rosemary, thyme, and lavenders to die over the winter."

`rhs` https://www.rhs.org.uk/herbs/sage/grow-your-own -- verified 2026-09-04
  > "free-draining soil or compost that doesn't get waterlogged"
  > "In winter, excess rain can cause the roots to rot, so move plants in containers to a sheltered spot, such as in the rain-shadow of a wall."

**RECORD CLAIMS THAT HOLD:**
- Root rot occurs on sage and is drainage-driven -- `ncsu_ext`, `uwi_hort`, `clemson_hgic` 1174, `rhs`.
- "Soil-borne water molds and fungi" -- `uwi_hort` D0094 verbatim, and note the record's phrasing is
  **taxonomically more accurate than its own `type: "fungal"`**; the dataset has no `oomycete` value,
  so `fungal` is the correct bucket. Not a defect; noting it so nobody "corrects" the prose.
- "attack the roots and crown of plants sitting in saturated, poorly drained soil" -- `uwi_hort`
  D0094, `clemson_hgic`.
- "humid heat" as a driver -- weakly but genuinely anchored by `umd_ext` southern blight ("active only
  during hot weather") and `clemson_hgic` (*Rhizoctonia* and *Phytophthora* favored by warm wet soil).
- "There is no cure once the crown is rotting; remove and discard affected plants" -- `umd_ext`
  ("irreversible damage"), `clemson_hgic` ("Some fungicides are effective, but only at suppressing
  these diseases").
- "On clay, use a mound or raised bed" -- `uc_ipm` Phytophthora Pest Note (pn74133,
  https://ipm.ucanr.edu/PMG/PESTNOTES/pn74133.html, verified 2026-09-04) carries this verbatim:
  "Raised beds can improve drainage in a vegetable garden" and mounds "8 to 10 inches high for
  annuals and up to 2 feet high with a gradual slope for trees and perennials." (That document does
  **not** name sage or *Salvia*; cite it for the practice, not for the host.)
- **Severity `high` holds.** `ncsu_ext` tags the plant "#Frequent Disease Problems"; both `uwi_hort`
  and `clemson_hgic` frame every other sage problem as minor and drainage as the make-or-break.

**RECORD CLAIMS WITH NO ANCHOR:**
- "It is **the main disease of sage**" / "This is **the main thing that kills sage**." No read
  document ranks sage's diseases. It is a reasonable reading of `ncsu_ext` + `uwi_hort` (both put
  drainage first and everything else in a "few problems" frame), but it is an inference, not a quote.
  Either soften or find a source that ranks.
- "**Wet feet and humid heat, not cold, are the underlying cause.**" The "not cold" half is contradicted
  in emphasis by `umd_ext` ("Excessively wet, **cold** soil can cause Mediterranean herbs ... to die
  over the winter") and `rhs` ("In **winter**, excess rain can cause the roots to rot"). The record's
  point -- that water, not temperature, is the agent -- is right, but the flat "not cold" denial
  suppresses the *winter wet* failure mode, which is the one that actually kills garden sage in
  cold-wet climates. **Recommend rewriting to "wet soil in any season, and especially wet winter
  soil" rather than "not cold."**
- "space plants for airflow" as a *root rot* control. `ncsu_ext`'s air-circulation sentence is scoped
  to "pests and **foliar** diseases." Airflow is not a root-rot lever in any document read.

**RECORD CLAIMS THAT ARE WRONG:** none outright; see the "not cold" item above, which is a
misleading emphasis rather than a false statement.

**LADDER-RELEVANT FACTS the record does not carry:**
- **The pathogens persist "years to decades" in soil** (`uwi_hort` D0094). That converts "fix
  drainage" from advice into a siting decision, and it is why replanting sage into the same spot is a
  bad bet.
- **Tool and footwear sanitation**, 10% bleach or 70% alcohol (`uwi_hort` D0094) -- maps to
  `garden_sanitation`.
- **Planting depth**: "the root collar just at the soil surface" (`uwi_hort` D0094) -- a concrete,
  free, preventive rung the record never mentions.
- **Mulch depth is a risk factor**: remove mulch over 4 inches, limit to three (`uwi_hort` D0094).
  Directly contradicts the general "mulch is good" instinct.
- **Container-specific move**: overwinter containers in a rain shadow (`rhs`). Sage is a common
  container herb; this is the single most actionable winter-wet rung.
- Catalog methods that fit `fungal`: `improve_drainage`, `garden_sanitation`, `soil_solarization`,
  `water_at_the_base`, `certified_clean_stock`, `biofungicide`. `improve_drainage` is the spine.

**ID NOTE (report only, do not act) -- this is the batch's shared-id question.** Match the TAXON:

| crop | record name | organism resolved by a document? |
|---|---|---|
| **sage** | Root and stem rot | **NO** -- umbrella (Phytophthora/Pythium/Rhizoctonia/Fusarium) |
| oregano | Root and stem rot | **NO** -- umbrella (its cited UF/IFAS blog names no organism) |
| thyme | Root and crown rot | **NO** -- unresolved (no UC IPM thyme page exists; 404 verified 2026-09-04) |
| rosemary | Root and crown rot | **YES** -- UC IPM's rosemary page lists "Phytophthora Root and Crown Rot" |
| lavender | Phytophthora root and crown rot | **YES** -- genus in the name; `wsu_ext_lavender_prcr` is a dedicated catalog key |

**Sage's is NOT the same organism as lavender's** -- not because it is a different organism, but
because *no document narrows sage's to Phytophthora*, and pinning sage to a Phytophthora-named id
would assert a genus the sage sources do not carry. Sage and oregano should share an **umbrella**
id; lavender (and probably rosemary) should take the Phytophthora-named one. The dataset already has
the umbrella id: **`root-and-stem-rots`**, used by borage, echinacea, marigold, sweet-alyssum,
sweet-pea and tomatillo, whose names span "Root and stem rot in wet soil", "Crown and root rot in
wet soil", "Root, stem, and crown rot (damping-off)" and "Stem, crown, and root rot" -- exactly this
umbrella. **`root-and-stem-rots` is the obvious reuse for sage.**

---

## Powdery mildew [diseases] -- severity low, type fungal
**STATUS: UNSOURCED-FOUND, with TWO WRONG CLAIMS**

**ORGANISM:** umbrella -- Erysiphales. `uc_ipm` (Pub 7493) names *Podosphaera pannosa* and *Erysiphe
lagerstroemiae* as examples on other hosts and states "Powdery mildew fungi are generally
host-specific." **No read document names the species on *Salvia officinalis*.**

**ANCHORS:**

`ncsu_ext` https://plants.ces.ncsu.edu/plants/salvia-officinalis/ -- verified 2026-09-04
  > "Root rot, **powdery mildew**, and verticillium wilt can occur."

`clemson_hgic` https://hgic.clemson.edu/factsheet/salvia/ (HGIC 1174) -- verified 2026-09-04
  > "Potential problems for salvias include damping-off of seedlings, stem and root rots, **powdery mildew**, Botrytis blight, aphids, spider mites, and whiteflies."
  > "Diseases most commonly occur in greenhouse production or under cool, wet weather conditions."

`rhs` https://www.rhs.org.uk/herbs/sage/grow-your-own -- verified 2026-09-04
  > (common problems include) "Powdery mildews" -- "a white, dusty coating on leaves, stems and flowers"

`uc_ipm` https://ipm.ucanr.edu/PMG/PESTNOTES/pn7493.html (UC ANR Pub 7493, *Powdery Mildew on Ornamentals*) -- verified 2026-09-04
  > "Common ornamental plants susceptible to powdery mildew include aster, deciduous azalea, tuberous begonia, California poppy, China aster, chrysanthemum, columbine, coral bells, corn flower, cosmos, crape myrtle, dahlia, delphinium, euonymus, forget-me-not, gaillardia, godetia, hydrangea, London plane tree, lupine, lilac, mint, monarda, oak, pansy, periwinkle, phlox, pot marigold, ranunculus, rose, rhododendron, rudbeckia, **salvia**, snapdragons, sweet pea, turfgrasses, verbena, and zinnia."
  > "Moderate temperatures of 60° to 80°F and shady conditions are most favorable for powdery mildew development. Powdery mildew spores and mycelium are sensitive to extreme heat and sunlight, and temperatures above 95°F may suppress growth of the fungus."
  > "Although relative humidity requirements for germination vary, all powdery mildew species can germinate and infect without water on the plant's surface."
  > "Water on plant surfaces for extended periods inhibits spore germination and kills the spores of most powdery mildew fungi."
  > "Overhead sprinkling can reduce the spread of powdery mildew because it washes spores off the plant."
  > "Provide good air circulation by pruning excess foliage and properly spacing plants."
  > "Prune out small infestations and remove infected buds during the dormant season."

`uc_ipm` https://ipm.ucanr.edu/PMG/PESTNOTES/pn7406.html (UC ANR Pub 7406, *Powdery Mildew on Vegetables*) -- verified 2026-09-04
  > "Moderate temperatures (60° to 80°F) and shady conditions generally are the most favorable for powdery mildew development."
  > "Although humidity requirements for germination vary, all powdery mildew species can germinate and infect in the absence of free water."
  > "Overhead sprinkling may help reduce powdery mildew because spores are washed off the plant."
  > "Overhead sprinklers are not usually recommended as a control method in vegetables because their use may contribute to other pest problems."
  > "Plant in sunny areas as much as possible, provide good air circulation, and avoid applying excess fertilizer."

(Pub 7406 is the correctly scoped document for a culinary herb: UC IPM's own rosemary page links
"Powdery Mildew on **Vegetables**", not the ornamentals note. Both agree on every point below.)

**RECORD CLAIMS THAT HOLD:**
- Powdery mildew occurs on sage/salvia -- `ncsu_ext`, `clemson_hgic` 1174, `rhs`, `uc_ipm` 7493.
- "A white to gray powdery film on the leaves" -- `rhs` ("white, dusty coating on leaves, stems and
  flowers").
- "on crowded, poorly ventilated plants" and "shaded" -- `uc_ipm` 7493/7406 ("shady conditions are
  most favorable"; "Provide good air circulation ... properly spacing plants").
- "rarely fatal" -- consistent with both Pest Notes' framing; **severity `low` holds.**
- "Remove affected leaves, thin for airflow" -- `uc_ipm` 7493 ("Prune out small infestations";
  "pruning excess foliage").
- "Space plants well, site in full sun ... Airflow is the main defense" -- `uc_ipm` 7406 verbatim
  ("Plant in sunny areas as much as possible, provide good air circulation").
- "prune to keep the plant open" / "the spring prune also opens up the canopy" -- `uc_ipm` 7493
  ("remove infected buds during the dormant season").

**RECORD CLAIMS WITH NO ANCHOR:**
- "It **taints the flavor**" / "makes it look and **taste** worse." No document I read says anything
  about flavor. Plausible for a leaf herb, but unsupported; either find a source or drop it.
  (Adjacent and citable if a flavor angle is wanted: `uf_ifas` EENY-750 reports *Eupteryx* feeding
  is "associated with lower essential oil content" in oregano -- but that is leafhoppers, not mildew.)

**RECORD CLAIMS THAT ARE WRONG:**

1. **"Fungi favored by warm, humid, still air" / "most likely in humid weather" / "Fungi that like
   warm, damp, still air" / "Damp, stagnant conditions raise the risk."**
   Refuted directly: `uc_ipm` 7493 -- *"all powdery mildew species can germinate and infect without
   water on the plant's surface"* and *"Water on plant surfaces for extended periods **inhibits**
   spore germination and kills the spores of most powdery mildew fungi."* The favoring conditions are
   **moderate temperature (60° to 80°F) and shade**, not warmth and damp. Powdery mildew is the one
   common garden fungal disease that does **not** need leaf wetness, and the record has it backwards.
   (`clemson_hgic` 1174's "cool, wet weather conditions" sentence is about salvia diseases *in
   general*, mostly in greenhouses; it is not a powdery-mildew-specific statement and should not be
   used to rescue this claim.)

2. **"avoid overhead watering" (in both `organic_treatment_seasoned` and `prevention_seasoned`, and
   "water at the soil instead of over the top" / "water at the base" in both beginner strings).**
   Refuted directly: `uc_ipm` 7493 -- *"Overhead sprinkling **can reduce** the spread of powdery
   mildew because it washes spores off the plant"*; 7406 -- *"Overhead sprinkling **may help** reduce
   powdery mildew because spores are washed off the plant."*
   This is a **wrong-advice defect of the same class as PLA-8's conventional-disclosure finding**: the
   record tells the reader to stop doing the thing the source says helps. The honest replacement is
   UC IPM 7406's own nuance: overhead watering suppresses powdery mildew but is not recommended as a
   *control method* because it feeds other problems. On sage specifically, root and stem rot is the
   `high`-severity problem on the same plant, so "water at the base" is still the right net advice --
   **but it must be justified by the rot, not by the mildew.** Attributing it to the mildew is false
   and it also creates an internal contradiction the ladder will inherit.

**LADDER-RELEVANT FACTS the record does not carry:**
- **Heat suppresses it**: "temperatures above 95°F may suppress growth of the fungus" (`uc_ipm` 7493).
  Explains why sage in a hot dry summer is clean and a shaded humid spring is not.
- **`sulfur` is the published soft-chemical rung** (`uc_ipm` 7406: apply sulfur products *before*
  disease appears) with the standard cautions -- do not apply oils within 2 weeks of sulfur, and not
  above 90°F. Sulfur is `fungal_foliar`-legal and is the classic preventive.
- **Horticultural / plant-based oils** for existing infections (`uc_ipm` 7406) -- maps to
  `horticultural_oil`, and the sulfur-interval caution must ride with it.
- **Resistant cultivars exist for some hosts** but `uc_ipm` 7493 names rose, crape myrtle, euonymus
  and sycamore -- **not salvia**. Do not offer `resistant_varieties` on this rung without evidence.
- The record's "the spring prune also opens up the canopy" is a genuinely good cross-link to sage's
  existing renewal-prune guidance and is worth keeping and strengthening.

---

## Verticillium wilt [diseases] -- severity low, type fungal
**STATUS: UNSOURCED-FOUND. Severity `low` is a CORRECTION CANDIDATE -- recommend `medium`.**

**ORGANISM:** ***Verticillium dahliae*** (and *V. albo-atrum*), per `uc_ipm`. On sage specifically the
only taxon-level attribution I located is **JOURNAL-ONLY and UNREAD**: Ryan, E.W. (1966),
"Verticillium wilt of sage (*Salvia officinalis* L.)", *Annals of Applied Biology* 58(1),
doi:10.1111/j.1744-7348.1966.tb05072.x. The Wiley abstract page returned **HTTP 403** on 2026-09-04,
so I have only a search-engine summary of it and am **not** treating its contents as read. Recording
it as a catalog-addition candidate and as the likely source of the "survives 10 years without sage"
figure that circulates.

**ANCHORS:**

`ncsu_ext` https://plants.ces.ncsu.edu/plants/salvia-officinalis/ -- verified 2026-09-04
  > "Root rot, powdery mildew, and **verticillium wilt** can occur."
  > (page Problems tag) "#Frequent Disease Problems"

`umd_ext` https://extension.umd.edu/resource/wilt-diseases-flowers -- verified 2026-09-04
  > "Verticillium wilt often attacks _Aconitum_ (monkshood), _Dahlia, Liatris_ (gayfeather), _Paeonia_ (peony), _Papaver_ (poppy), _Phlox, Rudbeckia_ (black-eyed-Susan), and **_Salvia_**."
  > "These fungi remain in the soil for many years."
  > "Once one of these diseases appears in a particular growing area, you must not plant the susceptible plant or take other cultural measures to reduce future losses."
  > "_Verticillium_ has a broader host range and so presents a more difficult problem in selecting 'non-susceptible' plants for rotation."
  > "If you cut into the stem, the vascular tissues show discoloration as tan, reddish, or dark streaking."
  > "_Fusarium_ and _Verticillium_ are favored by droughty conditions."

`uwi_hort` https://hort.extension.wisc.edu/articles/sage-salvia-officinalis/ -- verified 2026-09-04
  > "Some possible problems include slugs, spider mites, spittle bugs, root rot and **wilt**."
  > "_S. officinalis_ tends to be a short-lived perennial and is often best replaced every few years."

`uc_ipm` https://ipm.ucanr.edu/home-and-landscape/verticillium-wilt/ -- verified 2026-09-04
  > "_Verticillium dahliae_ and _V. albo-atrum_"
  > "Leaves infected with _Verticillium_ wilt and turn yellow, first at the margins and between veins; foliage then turns tan or brown and dies, progressing upwards from the base to the tip of the plant or branch. Browning of older leaves while younger leaves remain green is also characteristic. Woody plants are often affected first on one side of the plant or only in scattered portions of the canopy. Water-conducting tissue in branches and stems may darken in some hosts."
  > "Sanitation and resistant plants are the primary strategies for managing Verticillium wilt. Plant only pathogen-free plants. Avoid planting susceptible cultivars. Plant in disease-free soil. Solarization can reduce _Verticillium_ fungi in the upper few inches of soil. Keep plants vigorous by providing proper cultural care."

**(a) Do extension sources report Verticillium wilt on *Salvia officinalis*? YES.**
`ncsu_ext` states it on the *Salvia officinalis* page itself. `umd_ext` names *Salvia* in its
Verticillium host list. `uwi_hort` names "wilt" among sage's possible problems. This is three
admitted T1 documents, two of which are already in sage's own citation vocabulary. It is not a
fabricated problem.

**Document-scoped counter-evidence, reported as required:** `uc_ipm`'s Verticillium page host list
("dahlia, gerbera, marigold, peony, snapdragon, and vinca" plus woody plants) does **not** name
salvia; `clemson_hgic` HGIC 1174's salvia problem list does **not** include Verticillium; UC IPM's
Salvia page lists only leaf spot, powdery mildew and rusts. Those are three documents that omit it,
not three documents that deny it.

**(b) Is `low` defensible? Split verdict -- and the split is the actual finding.**

*Arguments FOR `low` (frequency):*
- Both sage-scoped documents frame it as an item on a short list of *possible* problems on a plant
  that "has few pests when grown in well-drained soil" (`uwi_hort`).
- `ncsu_ext` says it "can occur" -- the weakest presence verb on the page.
- `uwi_hort`: sage "tends to be a short-lived perennial and is often best replaced every few years."
  A soil disease that ends a plant you were going to replace anyway costs a gardener much less than
  the same disease on a tree or a permanent bed. **This is the strongest argument for `low` and the
  record does not make it.**

*Arguments AGAINST `low` (consequence):*
- `umd_ext`: "These fungi remain in the soil for many years" and "you must not plant the susceptible
  plant." That is a permanent loss of the planting site, not a nuisance.
- `umd_ext`: *Verticillium* "has a broader host range and so presents a more difficult problem in
  selecting 'non-susceptible' plants for rotation" -- the site is compromised for more than sage.
- `uc_ipm`: management is sanitation, clean stock, clean soil and solarization. **No curative rung
  exists.** The record itself says "There is no cure."
- Dataset precedent: `verticillium-wilt` is `medium` on strawberry and unset on artichoke and
  eggplant. **`low` would make sage the lowest-severity Verticillium record in the dataset**, on the
  same pathogen that is `high` (as `fusarium-verticillium-wilt`) on three tomatoes.
- **The record contradicts itself.** An entry whose own treatment field reads "There is no cure;
  remove affected plants and avoid replanting sage or other susceptible crops in the same spot"
  cannot honestly be labeled `low`.

**RECOMMENDATION: `low` -> `medium`.** It matches strawberry, the closest dataset comparable and also
a *V. dahliae* host with a replant restriction; it resolves the internal contradiction; and it stays
below `high`, which on this crop belongs to root and stem rot (the problem every source actually
leads with). Note that `severity` is a **legacy, un-normalized field** -- the ladder-pilot spec
(`docs/superpowers/specs/2026-07-22-pest-ipm-ladder-design.md`, line 198) records the ruling to
"leave legacy this arc (not load-bearing for the ladder)" -- so this is a data-truth correction, not
a gate blocker, and it needs Trevor's call rather than mine.

**RECORD CLAIMS THAT HOLD:**
- "Sudden wilting and yellowing of branches, **sometimes on one side of the plant**" -- `uc_ipm`
  verbatim ("often affected first on one side of the plant or only in scattered portions of the
  canopy"). Note the record's "sometimes" understates UC IPM's "often."
- "that does not recover" -- `uc_ipm` (no curative option), record's own "no cure".
- "A soil-borne fungus that **plugs the plant's water-conducting tissue**" -- `uc_ipm`
  ("Water-conducting tissue in branches and stems may darken"), `umd_ext` (wilts kill "by plugging the
  vascular system").
- "It builds up in soils where susceptible plants are grown repeatedly" / "can persist in the ground"
  -- `umd_ext` verbatim ("These fungi remain in the soil for many years").
- "There is no cure; remove affected plants and avoid replanting sage or other susceptible crops in
  the same spot" -- `umd_ext` verbatim ("you must not plant the susceptible plant"), and the "other
  susceptible crops" widening is carried by `umd_ext`'s broad-host-range sentence.
- "rotate the planting site when starting new plants, and avoid ground with a history of wilt" --
  `umd_ext`, `uc_ipm` ("Plant in disease-free soil").

**RECORD CLAIMS WITH NO ANCHOR:**
- "Improve **drainage** and airflow" and "Plant in **well-drained** soil" as *Verticillium* controls.
  No document I read links Verticillium to drainage. `ncsu_ext`'s drainage/airflow sentence is scoped
  to "pests and **foliar** diseases," and Verticillium is neither. This looks like root-rot advice
  copied across into the neighboring entry -- the `template inheritance` pattern.

**RECORD CLAIMS THAT ARE WRONG:**
- **"Better drainage and airflow help"** (beginner) and **"Improve drainage and airflow"**
  (seasoned), stated as management. `umd_ext` says the opposite of the drainage half:
  *"**Fusarium* and *Verticillium* are favored by **droughty** conditions."* Wet soil is the root-rot
  driver, not the Verticillium driver. Telling a reader that drainage helps against Verticillium is
  wrong advice, and it is exactly the class of defect the batch-24 source-truth pass caught.
  (Caveat for honesty: the unread Ryan 1966 summary reportedly says sage Verticillium was *most
  severe on heavy clay soils and in poorly drained areas*, i.e. the opposite of `umd_ext`. I could
  not read it, so I am not adjudicating on it -- but a later pass should know the two sources
  disagree, and should not "fix" the record toward either until one is actually read.)

**LADDER-RELEVANT FACTS the record does not carry:**
- **Soil solarization** is the one published soil-directed intervention: "Solarization can reduce
  *Verticillium* fungi in the upper few inches of soil" (`uc_ipm`). `soil_solarization` is already a
  catalog method and is `fungal`-legal.
- **Clean stock is a rung**: "Plant only pathogen-free plants" (`uc_ipm`) -- maps to
  `certified_clean_stock`, which matters because sage is commonly bought as transplants and
  propagated from cuttings.
- **A diagnostic the reader can perform**: "If you cut into the stem, the vascular tissues show
  discoloration as tan, reddish, or dark streaking" (`umd_ext`). This is how a gardener tells
  Verticillium from root rot, and it is the single most useful missing fact -- the two diseases have
  near-identical top-side symptoms and opposite management.
- **Symptom ordering**: yellowing "first at the margins and between veins," progressing "upwards from
  the base," with "browning of older leaves while younger leaves remain green" (`uc_ipm`).
- **Rotation is genuinely hard**: `umd_ext` explicitly warns the broad host range makes picking a
  non-susceptible replacement difficult. The record's cheerful "start new sage in a fresh spot"
  understates this.
- **Sage's short life is the mitigation** (`uwi_hort`: "often best replaced every few years"). Whatever
  severity is chosen, this belongs in the prose.

**ID NOTE (report only, do not act):** the dataset id `verticillium-wilt` is used by artichoke
("Verticillium wilt (*Verticillium dahliae*)"), strawberry and eggplant -- all *V. dahliae*, same
claim class. **Mint, in this same batch, also carries Verticillium wilt** (sourced to `usu_ext`'s
mint-in-the-garden page, framed as "the disease that most limits mint's longevity"). Sage and mint
should both reuse `verticillium-wilt`. Do **not** confuse it with the tomatoes'
`fusarium-verticillium-wilt`, which is a different, combined claim.

---

## SUMMARY

### Counts by STATUS (7 problems)

| STATUS | count | which |
|---|---|---|
| SOURCED-OK | 0 | -- (no entry carried `sources` or `anchoring_urls` at the start) |
| SOURCED-WEAK | 0 | -- |
| **UNSOURCED-FOUND** | **7** | all seven |
| UNSOURCED-NOT-FOUND | 0 | -- |
| JOURNAL-ONLY | 0 as a status | but 2 journal leads recorded and flagged UNREAD (see below) |
| WRONG | 0 as a whole entry | **3 entries carry specific wrong claims**: Powdery mildew (2), Verticillium wilt (1), Leafhoppers (1 misleading-by-omission) |

**Every one of sage's seven problems is real and anchorable at Tier 1**, and in 6 of 7 cases the
anchor is a source already in sage's own citation vocabulary. `hunt before downgrading` held again:
0 of 7 turned out to be unsourceable.

### The single most important finding

**The sage record's problem list was never unverified -- it was verified once, at cert, against the
NC State Extension Gardener Plant Toolbox entry for *Salvia officinalis*, and the crop's own
`verification_log_ref` says so ("NCSU pest/disease lists confirmed"). What was never done is the
work downstream of that sentence.** The NCSU field is a bare seven-item list with no organism, no
severity, no mechanism and no management. Everything the record says *beyond* that list -- the
causes, the conditions, the treatments -- was written to fill the record's shape, not read out of a
document, and that is exactly where the defects are:

- **Powdery mildew** is described as favored by warm, humid, still air and treated by avoiding
  overhead watering. UC IPM says powdery mildew "can germinate and infect **without water** on the
  plant's surface," that standing water "**inhibits** spore germination and kills the spores," and
  that "overhead sprinkling **can reduce** the spread." Two of the entry's four management strings
  give advice the source contradicts.
- **Verticillium wilt** is treated by improving drainage. UMD Extension says *Verticillium* is
  "favored by **droughty** conditions." Drainage is the root-rot lever, and it appears here because
  the neighboring entry's prose was carried across.
- **Leafhoppers** name no symptom at all, because the 2026-07-06 cert correctly struck a whitefly
  conflation and left the hole; meanwhile the taxon turns out to be a Lamiaceae specialist
  (*Eupteryx decemnotata* / *E. melissae*) whose diagnostic sign -- coarse pale stippling on the
  upper leaf surface, insects hiding underneath -- is missing.

`fill the shape is the defect`, three times on one crop. The record pass was worth doing.

### Actions for the authoring pass, in priority order

1. **Rewrite the Powdery mildew entry's cause and treatment strings.** Keep "water at the base" as
   sage advice but justify it by root and stem rot, never by mildew.
2. **Rewrite the Leafhoppers entry** around stippling/mottling, the *Eupteryx* taxon, yellow sticky
   traps, and "no control needed."
3. **Strike "improve drainage" from the Verticillium entry**; add the cut-stem vascular-streaking
   diagnostic that distinguishes it from root rot.
4. **Adjudicate Verticillium severity `low` -> `medium`** (Trevor's call; evidence in §7).
5. **Soften "not cold"** in the Root and stem rot cause to admit the winter-wet failure mode.
6. **Correct `type: "insect"` -> `"mite"` on oregano, rosemary and thyme** before their ladders are
   authored (§0b). Sage needs no change.
7. **Pin ids before fan-out**: `slugs-and-snails` (reuse, 11-crop majority), `root-and-stem-rots`
   (reuse, umbrella -- shared with oregano; NOT lavender's Phytophthora-named id),
   `verticillium-wilt` (reuse -- shared with mint), a **new** batch-wide spittlebug id (sage,
   lavender, rosemary), and a **new** *Eupteryx* leafhopper id (NOT `leafhoppers`, NOT
   `aster-leafhoppers`), minted once for every Lamiaceae crop in the batch.

### Documents that could not be read (reported as unreadable, NOT as absence)

| document | outcome on 2026-09-04 |
|---|---|
| pnwhandbooks.org "Sage (*Salvia* sp.)-Downy Mildew" (`/plantdisease/host-disease/...` and `/node/3475/print`) | **HTTP 403** on both paths. The page is indexed and presumably exists; its content, and whether PNW publishes a sage root-rot page alongside it, is **unknown**. |
| Ryan (1966) "Verticillium wilt of sage (*Salvia officinalis* L.)", *Ann. Appl. Biol.* 58(1) | Wiley abstract **HTTP 403**. Search-engine summary only; **not read**, not cited. |
| APS *Plant Disease* 81(8):959 (1997), Phytophthora root and crown rot of sage / *P. cryptogea*, Salinas Valley CA | Not fetched. **JOURNAL, and the catalog carries no journal entries** -- catalog-addition candidate only. |
| TAMU AgriLife EHT-094 *Herbs for Texas Landscapes* (aggie-horticulture PDF, 6 MB) | Fetched, **no readable text** (compressed streams). `tamu_agrilife` is in sage's vocabulary but this document contributed nothing. Same failure mode as `sage_pilot_finding_001`'s AZ2061. |
| MSU `canr.msu.edu/ipm/uploads/files/HerbPerennials/Rhizoctonia.pdf` | Fetched, **no content returned**. Also note this series is scoped to herbaceous *ornamental* perennials, not culinary herbs -- likely the wrong scope anyway. |

### Deliberate absences worth recording

- **UC IPM publishes no sage page.** `https://ipm.ucanr.edu/home-and-landscape/sage/` returns a hard
  **404** (verified 2026-09-04), as does `.../thyme/`. `.../oregano/`, `.../rosemary/`, `.../basil/`
  and `.../salvia/` all exist. The `/salvia/` page is the **ornamental-genus** page (its disease
  links are "Rusts (Trees and Shrubs)" and its weed link is "Weed Management Around Ornamental Trees
  and Shrubs") and lists only Aphids and Thrips as invertebrates -- it does **not** corroborate any
  of sage's four pests. Sage's UC IPM anchors therefore have to come from the pest-specific pages
  (leafhoppers, spittlebugs, spider mites, snails and slugs, powdery mildew, Verticillium wilt),
  which is what I used. `uc_ipm` is **not** currently in sage's citation vocabulary; four of the
  seven entries below now depend on it, and admitting it is the right call -- `uc_ipm`,
  `ucanr_ext_spider_mites` and `ucanr_ext_snails_slugs` are all already in the admission catalog, and
  `uc_ipm` is already sourced on oregano and mint in this same batch.
- **Penn State PlantVillage** (`plantvillage.psu.edu/topics/sage/infos`) lists **only** Crown gall
  (*Agrobacterium tumefaciens*) and Mint rust (*Puccinia menthae*) for sage -- **neither of which is
  in our record, and none of our seven of which is in theirs.** Not a contradiction (different
  document, different scope, likely commercial-production framing), but worth knowing that a
  seventh independent source produced a disjoint list. PlantVillage is a Penn State property but is
  **not** the catalog's `psu_ext` (Penn State Extension, extension.psu.edu); using it would be a
  catalog decision.
- **Virginia Cooperative Extension ENTO-412NP, "Ligurian Leafhopper"**
  (`https://www.pubs.ext.vt.edu/ENTO/ENTO-412/ENTO-412.html`, verified 2026-09-04) is an excellent
  T1 document naming sage among the favored hosts ("basil, mints (including catnip and peppermint),
  lemon balm, oregano, rosemary, sage, and thyme") and giving a hatch threshold ("Eggs that
  overwintered in leaf tissue hatch when warming spring temperatures reach 68° F"). **The catalog
  admits VCE only as four publication-specific keys** (`vce_426_331`, `vce_426_840`, `vce_438_108`,
  `vce_spes_455`) with no generic `vce` key, so ENTO-412NP is a **catalog-addition candidate**. The
  UF/IFAS EDIS equivalent (EENY-750 / IN1290) carries the same claims under `uf_ifas`, which **is**
  already in sage's vocabulary, so nothing is blocked.

### Consumer-copy constraint check on the existing prose

Machine-checked all 7 entries across every string field: **no em dashes, no `°` occurrences at all
(so no `°F` spacing risk), no mid-sentence capitalized "Plant", no sentence-initial lowercase
"plant".** Clean.

One style note, not a violation: the slugs `organic_treatment_beginner` is a 40-word sentence
carrying two chemical names ("iron-phosphate", "metaldehyde") in the *beginner* register. The
pet-safety hedge itself is correct and correctly hedged; the sentence is just heavy for its
audience.
