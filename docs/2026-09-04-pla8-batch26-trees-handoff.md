# PLA-8 BATCH 26 -- THE TREES AND SHRUBS: handoff

**Written 2026-09-04.** mulberry, pawpaw, pear-asian, pear-european, persimmon, pomegranate.
Verify before acting: `shasum -a 256 crops_data_final.json` against `LATEST.txt`, then `git log -1`
and `git status -sb`.

---

## 1. Scope: all six, one batch, and why

The kickoff offered a split (the two pears plus pawpaw; persimmon, pomegranate and mulberry). All
six went in one batch. The size matched the herbs (39 canonical entries against 36), and the
collision guard's pass condition is a DIFFERENCE measured over the whole post-apply state: splitting
would have minted `pear-scab`, `pear-psylla` and `pear-decline` in one half and reported them as
INHERITED in the other, which blurs exactly the report the kickoff asked for. The pears are also
template twins (three byte-identical entries), and a twin-divergence guard needs both in one promote.

| | count |
|---|---|
| crops | 6 |
| canonical problems -> target problems | 39 -> 38 |
| retired (array duplicates, declared with `duplicate_of`) | 3 |
| renamed | 1 |
| split rows | 4 (2 bundles -> 4 limbs) |
| severities re-pinned on document evidence | 5 |
| types upgraded off `pest` / `disease` / `other` | 28 (10 fine types carried) |
| rungs | 115 |
| declared field corrections | 210 |
| source keys, all catalog-admitted | 125 |
| authoring refusals filed | 70 |
| unreachable claims filed | 67 |
| collision pairs: canonical -> post-apply | 37 -> 42, 5 introduced, 5 registered, 0 unregistered |

## 2. What the preflight found before any authoring

* **Pear scab sits in BOTH `pests[]` and `diseases[]` on both pears, and Fabraea leaf spot does the
  same on pear-european.** Separately authored copies of one disease. `git log -S` dates the
  `pests[]` copies to 2026-06-11 (the originals) and the `diseases[]` copies to the 2026-07-02
  certification (`73a1f64`), which added the second copy without removing the first. Shipping both
  under one id fails `control_ladder_gate`'s within-crop identity check; shipping them under two ids
  mints a duplicate join key on purpose. The three `pests[]` copies retire, each declared with a
  `duplicate_of` pointing at the surviving `diseases[]` entry, and the promote proves each retirement
  IS a duplicate (same-named `diseases[]` twin exists in canonical, is carried by the pin table, and
  the retired copy is typed as a disease). Roster-wide, these were the only three same-name-in-both-
  arrays entries; the four other array/type mismatches are nematodes in `pests[]`, a different
  question.
* **The type situation was MIXED, the eighth distinct shape in eight batches.** Four crops coarse
  (`pest`/`disease`), the pears fine EXCEPT "Pear decline" typed `other`, which no gate recognizes.
  Neither batch 23's uniform-coarse guard nor batch 24's set-from-nothing fit, so `pre_type` is
  pinned PER ROW and the guard asserts both halves. Pear decline goes `bacterial` on the roster's own
  aster-yellows precedent (a phytoplasma on 6 crops); both pear reviewers note no document calls it a
  bacterium outright, the vocabulary being "phytoplasma organism", so this is a taxon call, recorded.
* **Pomegranate's "Mealybugs and scale" had no id yet**, so under the batch rule (one organism or
  disease complex per id) it splits rather than minting a new bundle. The record pass then found the
  two halves cannot share prose: calyx harborage is stated for mealybugs only, and UC IPM's Soft
  Scales page says honeydew and sooty mold "has not been observed on pomegranates" (V1).

## 3. The collision guard, and what it did on the family most likely to exercise it

Ran at id-pinning time, before fan-out, against POST-APPLY data, pass condition a DIFFERENCE:

    pairs on canonical: 37   pairs post-apply: 42
    INTRODUCED by this batch: 5     REGISTERED 5     UNREGISTERED 0
    INHERITED (this batch only joins them): 37

**It neither flooded nor missed.** The five introduced pairs were exactly the five predicted from
the pin table before the run, all NAME_SHARED (none ID_NEAR_DUP, none FAMILY_MEMBER):

| pair | why distinct |
|---|---|
| `mulberry-bacterial-blight` / `bacterial-blight` | *P. syringae* pv. *mori* vs edamame's *P. savastanoi* pv. *glycinea* |
| `mulberry-bacterial-blight` / `bacterial-blights` | vs the beans' *Xanthomonas* + pv. *phaseolicola*; shared key is a parenthetical-deletion artifact |
| `mulberry-borers` / `cherry-borers` | an unresolved umbrella vs two named *Prunus* clearwing/beetle borers |
| `persimmon-leaf-spot` / `lavender-leaf-spot` | two crop-scoped umbrellas: *Pseudocercospora diospyricola* vs *Septoria lavandulae* |
| `phytophthora-root-rot` / `lavender-root-crown-rot` | genus id vs lavender's species-pinned *P. nicotianae* id |

**Two registry entries instead of one three-id set** for mulberry's bacterial blight, deliberately:
a set {mulberry, edamame, beans} would suppress the OPEN edamame/beans pair (PLA-448 s4a), which is
the "quiet the gate by registration" trap the registry forbids. Pairs suppress only themselves.

**The pome-fruit prediction did not materialize.** `pear-scab` sits at edit distance 4+ from
`apple-scab`, `pear-psylla` and `persimmon-psyllid` share nothing with `asian-citrus-psyllid`, and
`cercospora-fruit-and-leaf-spot` is edit distance 10 from `cercospora-leaf-spot` (already ruled
distinct in PLA-448 s2). The collisions came from the GENERIC display names (bacterial blight,
borers, leaf spot, root and crown rot), which is s4f's shape, not the pome-fruit one.

Self-test: a planted `bird` against the live `birds` flips a row to UNREGISTERED and exits 1;
restoring gives exit 0 with the pin table byte-identical. The batch JOINS the known open pairs
(`aphids`, `whiteflies`, `gray-mold`, `anthracnose`, `stink-bugs`, `mealybugs`, `scale-insects`)
and registers none of them; PLA-450 owns those.

## 4. s4d and s4f, answered per entry (again with more than one answer)

**Bundles (s4d).** Four entries carried two problems; they resolved three ways.
* SPLIT: pomegranate "Mealybugs and scale" (two organism classes, incompatible prose);
  persimmon "Leaf spot and twig dieback" (the dieback half is *Botryosphaeria* canker, which
  UF/IFAS HS1389 calls "the limiting factor for growing persimmons in Florida and the Deep South",
  filed at LOW and cosmetic under two anchors that never contain the word dieback; now its own
  entry at HIGH, V2).
* CORRECTED, NOT SPLIT: two entries were one problem BY NAME with a second organism smuggled into
  the cause prose. Pomegranate's "Cercospora fruit and leaf spot" named *Colletotrichum* and
  *Botryosphaeria* as "related fungi"; UGA C997 lists *Colletotrichum* as symptomless and
  *Botryosphaeria* as a separate disease (V3). Persimmon's "Persimmon borer" folded in flatheaded
  borers, a separate UC IPM problem (V6). The clause comes out; the uncovered problem is filed.
* KEPT AS ONE: pawpaw's "Fruit-raiding wildlife (raccoons, opossums, squirrels)" is a pest COMPLEX,
  not a bundle. Five documents name raccoons, opossums, squirrels and foxes; none distinguishes home
  management by animal; a variety cannot be resistant to one and not another. One vertebrate id.
  Foxes and deer (which DO eat dropped fruit, and rub antlers on young trunks) ride in prose; adding
  foxes to the display name is a rename candidate for Trevor.

**Bare generics (s4f).** Two on mulberry, both GENUINE UMBRELLAS in the admissible literature:
"Borers" (NC State's two prose sentences name no organism; the one US extension naming one, K-State
MF2735's *Dorcaschema wildii*, is not catalog-admitted and does not carry the record's "secondary on
stressed trees" claim) and "Leaf spots and minor foliar diseases" (TAMU lists seven fungi under three
headings with shared management). Both got crop-scoped umbrella ids, lavender's batch-25 shape.
Persimmon's "Leaf spot" limb is the same shape with a named principal.

**Severity followed the documents, five times.** pear-asian psylla high -> medium and scab
medium -> low (UC IPM: "a greater problem on European varieties", "less susceptible to scab than
European pears"; the record was pear-european's template copy); pawpaw Phyllosticta low -> medium
(Clemson "severe... premature cracking"; the cosmetic description belonged to flyspeck);
pomegranate black heart high -> medium (the record's high rested on a backwards climate framing,
V3; UC IPM: losses "usually less than 1% but can be up to 6%"); persimmon's dieback limb HIGH.

## 5. The no-control class: a decision for Trevor

Four entries carry sources that say no control is warranted or none exists, and the catalog has no
tolerate-and-monitor method: pawpaw's zebra swallowtail (UMD: "do not cause enough damage to warrant
treatment"), pawpaw's peduncle borer (KSU: "does not require control of this insect"; no product
registered; MU's pruning sentence turned out to be about the webworm, V5), persimmon's anthracnose
(HS1389 names no material), and persimmon's borer (no live document names a home treatment). An
empty ladder is a defect by this repo's convention, an inverted method is a FIT defect, and retiring
the entry deletes the correct consumer answer to "what is eating my pawpaw".

**What shipped:** the roster's own precedent, the parsleyworm (black swallowtail on parsley and
dill), is one `handpick` rung led by tolerance; the swallowtail follows it, and the review then found
MU and ACES describing seedling defoliation, which anchors the young-tree trigger. For the three with
no method open at all, ONE honest rung ships whose every sentence is anchored and which says plainly
that the sources give no control; the reviewers graded these FIT-by-construction and asked that the
decision be flagged. **Recommendation:** a cultural `monitor_and_tolerate` method in the catalog,
which also fits persimmon's psyllid and pomegranate's mealybug (UC IPM: treatments "usually not
justified or effective on home fruit trees"). It is app-coupled (plant-app's glossary tripwire test
requires every method key to resolve), so it is a PLA ticket, not a batch item.

## 6. PLA-457, held: the figures this batch found and did not write

The promote refuses any consumer string that names sulfur, names oil and gives a duration
(`check_no_sulfur_oil_interval`, asserted both ways: "never mix oil with sulfur" passes). Found and
filed, not authored: UC IPM PN 7413 (home apple and pear scab) "never apply them within 3 weeks of
an oil application"; UC IPM PN 7408 (home scales) "do not apply oil within 3 weeks of an application
of sulfur-containing compounds"; NC State home orchard "10 days"; WSU FS376E prescribes a COMBINED
dormant sulfur-plus-oil spray; OSU EC 631 states incompatibility with no number. So UC IPM's home
Pest Notes carry 3 weeks twice more, and one T1 source recommends the very combination the others
space out. Four figures now, from four institutions.

## 7. What the six-reviewer pass found (ran on the authored content BEFORE the promote)

~317 graded items; 54 FIX items applied in six scoped fix passes. The coarse rules held;
the defects were finer, the same shape as batches 24 and 25.

1. **A refusal that asserted a document's silence from the report's excerpt.** pear-asian refused a
   clean-stock rung on pear decline; USU's page, anchored on that very entry, says "Grafting and
   budding can also transmit this phytoplasma." Persimmon did the same on Phytophthora: "the pn74133
   sentences read do not include it" while the page includes them. Batch 25's s8 lesson, recurring:
   a summary handed to an agent becomes that agent's whole universe for the claim.
2. **Over-correction.** mulberry stripped canopy-thinning and irrigation advice from six fields and
   one refusal on a misread of the OSU sheet already cited on both entries, which states both.
3. **An orchestrator error propagated into prose.** I told the pear-european author that Fabraea's
   twig-canker removal was "per PSU/MSU"; only the UMass guide (inadmissible key) prescribes it. It
   was written in four places and trimmed on review. I also told the mulberry author TAMU prescribes
   "keeping foliage dry"; TAMU's sentence is pruning dead shoots in autumn and approved fungicides.
   And my brief described ACES's sanitation sentence as spanning its whole pest list; the pawpaw
   author read it in context and found it closes a paragraph about five OTHER pests.
4. **Two agents, one document, opposite readings**, settled by the reviewer reading the page: the
   pear decline clean-stock rung above.
5. **Figures without warrant.** The temperature guard refused three: 60°F (fire blight copper; PN
   7414 states it, anchor extended), 21°F (leaf-footed bug cold mortality; the UC IPM ag page states
   it verbatim, V7), and 70°F to 77°F (gray mold; the generic UC IPM home Botrytis page states it, quoted into the entry's own anchor on the fixer's read).
6. **One byte-identical sentence across batches.** Pomegranate's whitefly water-spray note repeated
   lavender's "hose the adults off with a strong stream of water." The single-donor echo guard caught
   it; rewritten.

## 8. Guard defects of mine the batch caught

* **The PLA-457 predicate's regex spelled sulfur wrong** (`sulph?ur` matches "sulphur", not
  "sulfur"). Caught by asserting the predicate both ways before anything relied on it. A mutation
  restoring the misspelling is in the harness.
* **The pear twin guard keyed authored entries by NAME**, so the retired `pests[]` "Pear scab" twin
  resolved onto the surviving `diseases[]` entry and the scab divergence was counted twice (4 twins,
  2 divergences against the 3 and 1 measured on canonical). The suite's PINNED twin count exposed it.
  Keyed by (field, name) now.
* **`test_gen_current_state.py` was RED at HEAD before this batch touched anything**: the live `## Canonical pointer` bullet still read `a9c84847` (batch 24), two promotes stale, because the batch 25 and rosemary closes prepended their release entries without updating the pointer. Read, not dismissed (the 2026-07-29 rule); fixed by replacing that ONE bullet with the generator's. A first attempt spliced the whole generated section over the live one and deleted 191KB of accumulated history under that heading, caught by the removed-lines check before anything was committed and reverted: protocol #2's warning, demonstrated.
* **The pin table was written before the reviews and re-pinned four times on their evidence.**
  That is the right order (pins gate the collision check, which must run before fan-out), and the
  promote's spec-match guard is what makes a late severity change safe: the output must equal the
  pin.

## 9. Documents read, and the two that still cannot be

First-party: UC IPM (home and ag pages for pear, persimmon, pomegranate; PN 7412, 7413, 7414, 7408,
74168, 74174, 74133, 7401, 7400), UF/IFAS HS1389 and PP349, UGA C997 and C784, Clemson HGIC 1352,
1359, 1360, 2208, Penn State, NC State (handbook ch. 15, toolbox, Lee County), KSU (planting guide,
FAQ, enemies page), UMD (two pages), Purdue BP-30-W, USU, WSU, TAMU. Proxied (r.jina.ai or Wayback,
anchored at the live URL and disclosed in notes): OSU popcorn and shade-tree pages (403 first-party
since the July cert), OSU Oregon EC 631, MSU Fabraea (JS shell), KSU PBI-004 and MU AF1021 (PDFs),
UC ANR FNRIC (403 on every path; no claim rests only on it). RETIRED and not anchoring: UF/IFAS
ENY-835 (410 Gone) and ENY-803 (mirror only). NEEDS-CATALOG-ADMISSION, for a later ruling: K-State
MF2735 (the only organism-level mulberry borer document), the PNW Plant Disease Handbook mulberry
and pear pages, UMass NETFMG (scope widening of `umass_ext`), Cornell Lake Ontario Fruit Program.

## 10. Verification

Canonical `ce98b0a6` -> `ba61762a` (ONE promote; an intermediate post `6e62085b` was rolled back to the base and re-promoted after the pears' temperature-scan violation, so `ba61762a` is the only post state that ever passed the gauntlet).

Suite **86/86**; mutation harness **48 injected / 48 caught / 0 survived / 0 broken**, positive control green, sentinel reddened; batch 25's harness re-run under the same fix: **34/34 caught**, so its birth-time claim is now verified under the fixture-based suite.

`whole_crop_gate` PASS on all six (the pears failed once on the spelled-temperature scan matching 'N degree-days' in three codling-moth strings, rewritten without the figures and re-promoted); `gate_all` **121/121**; `control_ladder_gate` 0 with 899 of 913 problems laddered (the 14 unladdered are the seven microgreens); `register_completeness` PASS; collision gate on live canonical 42 pairs, 20 registered, 22 open (the pre-existing set plus nothing); `release_verify` clean with exactly the six declared crops changed (its default reference is an annual, so `--ref apple`; `--slug` defaulted to cherry-tomato and was pointed at mulberry); `doc_roster_claim_gate` run after the state trio.

Roster after the promote: **114 crops fully laddered**, 7 unladdered (sunflower-sprouts, pea-shoots, radish-microgreens, broccoli-microgreens, arugula-microgreens, wheatgrass, cilantro-microgreens), 7 shells; 3594 rungs on 899 id-bearing entries.

## 11. Next

**Batch 27 = the microgreens** (arugula-microgreens, broccoli-microgreens, cilantro-microgreens,
pea-shoots, radish-microgreens, sunflower-sprouts, wheatgrass), the last of the worklist, per demand
order. Two shape notes carried forward: those crops carry `name_seasoned`/`name_beginner` with no
`name`, so `pin_and_check`'s reconcile and the promote's name-keyed guards must fall back through
that schema (the collision gate already does, PLA-449 s8c); and each carries exactly two problems
(fungus gnats, damping-off) with cultural and physical controls only. After batch 27 the arc's
completion test is "every problem entry laddered", which the 7 shells pass by absence.

Owed after this batch: a plant-astro submodule bump (that repo's session); plant-app's
`npm run build:guides`; the PLA-457 ruling (now four figures); the no-control method decision (s5);
the eight duplicate-id merge (PLA-450) that still blocks PLA-12.
