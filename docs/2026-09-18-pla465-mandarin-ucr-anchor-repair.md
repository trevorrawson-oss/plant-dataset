# PLA-465 owed repair: mandarin-clementine's `ucr_citrus` anchor -- RE-STAGED AND HELD

**Session:** 2026-09-18, **re-staged 2026-09-20** on Trevor's two rulings. Claude Code.
**Base:** `892c76fb` (PLA-465 promote 2, commit `17e0154`).
**Scratch post-state:** `b2b875b7fde99007dc9b661bec5ab2dd001275120a441e9cd55223666b5d4764`, gauntleted,
**never written**. Apply on approval:

```
python3 tools/promote_pla465_mandarin_anchor.py --expect-sha b2b875b7fde99007dc9b661bec5ab2dd001275120a441e9cd55223666b5d4764
```

> The 2026-09-18 staging (`f2dbaf03`) is superseded. It held four cells; the rulings below convert one
> to a DROP and leave three held with a recorded finding, and add two `open_findings`.

---

## 1. The recorded reason was too wide, and acting on it wholesale would have been a defect

PLA-465 promote 1 surfaced this as a finding and did not fix it:

> mandarin-clementine's UCR anchor is a satsuma page

and the crop's own `open_finding` says it at greater length:

> The crop's cited UCR anchor (https://citrusvariety.ucr.edu/crc3178) is a SATSUMA page, **the wrong
> scion**

**The page identification is correct.** Re-read from raw bytes 2026-09-18: `crc3178` is
*Frost Owari Satsuma mandarin*, `Citrus unshiu` Marcovitch, CRC 3178, 235,255 bytes,
sha256 `3a610c2fc8a9b4762a3a4787723db9e7bb678029979077cf282a008db2b47547`.

**The conclusion drawn from it is not.** Two measurements, both computed rather than asserted:

1. The anchor is not on one cell. An independent walk finds `ucr_citrus` on **19** cells of this crop.
2. This crop is **not** scoped to clementine. Its `varieties.note_seasoned` opens "Mandarins
   (*Citrus reticulata* and its hybrids) span a long season by variety", and **Owari Satsuma is its
   first `recommended` entry**, ahead of Clementine. Several cells therefore make satsuma-specific
   claims, and `crc3178` carries those verbatim.

A promote that believed the recorded sentence and repointed all 19 cells would have **stripped eight
correct attributions** in the name of fixing a citation. This is the failure mode the session kickoff
named: a right conclusion resting on a wrong premise. The premise here is "the wrong scion", stated of
the crop rather than of the cells that actually carry a non-satsuma claim.

## 2. The rule applied

`docs/2026-07-26-artichoke-design-decisions.md` A.8, from the asparagus R4 failure:

> truth lives in the per-cell anchoring URL, not the source id. For every cell, the anchored document
> must be fetched and the claim sentence confirmed present before the citation ships.

So every one of the 19 cells was adjudicated against the fetched bytes, not against the source id and
not against the sibling citrus crops. `source_catalog["ucr_citrus"]` remains correct and untouched: its
`url` is the collection root and its `citable_for` is "variety identity, characteristics, parentage, and
home-grower recommendations". Campaign C measured the normal relationship as "the catalog is a root, the
node names a document" (21,340 nodes), so naming an accession at the node is the convention; naming the
**wrong** accession is the defect.

## 3. The adjudication: 7 repointed, 8 kept, 1 dropped, 3 held

### REPOINT (7) -- the claim is about another cultivar and `crc3178` does not contain it

| cell | to | the sentence that carries the claim |
|---|---|---|
| `tips_by_stage.bloom[1]` | `crc0279` | "shedding is correlated with the seed content of the fruit...the bearing behavior...can be regularized by cross-pollination", then Chapot's ranked pollinator list |
| `tips_by_stage.ripening_harvest[1]` | `crc3913` | "holds exceptionally well on the tree, with summer-harvested fruit still being of good quality"; "outstanding storage characteristics both on and off the tree"; ripeness Feb to June |
| `regions.ca_desert.resolved_by_zone.{9,10,11}` | `crc0279` | "In regions of high total heat, the Clementine matures very early -- only slightly later than the satsuma mandarins. Such regions also favor production of fruit of maximum size and best eating quality"; and for the cell's fruit-drop advice, "excessive shedding of younf fruits during the fruit-setting period" regularized by "adequate nitrogenous fertilizer and efficiency in irrigation" |
| `regions.low_desert_az.resolved_by_zone.{9,10}` | `crc0279` | same two sentences; the cell reads "Clementine and late types; satsuma earlier" |

Measured on `crc3178`: **"clementine" 0 occurrences, "Gold Nugget" 0, "Pixie" 0, "pollin" 0,
"Murcott" 0.** The cells above are led by exactly those words.

New pages, read from raw bytes 2026-09-18:

| accession | identity | bytes | sha256 |
|---|---|---|---|
| `crc0279` | Algerian clementine, *Citrus clementina* | 113,471 | `e64774eb…0bfd2e30` |
| `crc3913` | Gold Nugget mandarin | 141,796 | `60703aa3…9da5725c` |

Each repointed cell also moves `verified` from `2026-07-02` to `2026-09-20`. Carrying the old date onto
a new URL would fabricate the attribution, so the promote **refuses** a repoint that keeps it.

### KEEP (8) -- satsuma-specific, and `crc3178` carries it verbatim

`storage`, `varieties`, `tips_by_stage.ripening_harvest[0]`, `failure_diagnostics[1]`,
`regions.ca_interior.resolved_by_zone.{8,9}`, `regions.ca_north_coast.resolved_by_zone.{9,10}`.

Four of these rest on one sentence pair on the page: "The fruit itself does not hold well on the tree,
but it stores well after harvest" and "Fruit holds poorly on trees after maturity and must be picked
promptly but stores well." That **is** the storage and pick-promptly claim, on the crop's own lead
variety. `varieties` keeps it because the block's first recommended entry is Owari Satsuma and its
`notes_seasoned` tracks the page ("small, spreading, somewhat drooping"; "cold-hardy"; "seedless";
ripening October to December).

**One nuance recorded, not acted on:** the two north-coast cells say "satsuma, which tolerates cool
summers, is the best bet". `crc3178` supports satsuma's cold-hardiness and early season but says nothing
about a summer heat requirement; that half of the sentence rests on the co-source
`ucanr_santa_clara_mg`. Not a defect, and not repaired here.

### The two held classes, as ruled 2026-09-20

#### RULING 1 -- `failure_diagnostics[0]`: DROP the credit

The claim is that fruit stays green and low in sugar where the climate lacks a warm-day/cool-night
swing. `crc3178` contains "green" **0 times** and says nothing about diurnal range, so the credit is
removed from **both** `sources` and `anchoring_urls`. A finding records it
(`mandarin_clementine_climate_claim_citation_pla465`), and the targeted T1 read is **not** done here.

**THE RULING'S PREMISE WAS WRONG, AND THE RECORD SAYS SO RATHER THAN REPEATING IT.** The ruling was
taken on the understanding that the claim would be left uncited. It is not. The cell cites two sources
and the drop leaves `uhawaii_ctahr`, which was read from raw bytes on 2026-09-20
(`https://www.ctahr.hawaii.edu/oc/freepubs/pdf/F_N-14.pdf`, CTAHR F&N-14, 266,558 bytes,
sha256 `4d2a3549…eafaef47`) and **carries the colour half verbatim**:

> "Fruit of citruses such as orange and tangerine usually fails to develop color when grown at
> Hawai'i's lower elevations, and a green or green-yellow skin coloration is normal in ripe fruit.
> **In areas with cooler nights, the fruits turn bright orange upon ripening.**"

What the page does **not** support is the record's joining of green skin and low sugar under one cause.
CTAHR attributes low sugar to the opposite condition, the 500 to 1000 ft **and above** elevation range,
"where cooler temperatures are common, the fruit may fail to develop high levels of sugar". So the read
this owes is narrower than the ruling assumed: not a re-citation, but a T1 statement on whether the
sugar half shares the cool-night mechanism. UF/IFAS or TAMU on colour break and degreening remain the
likely homes.

**No gate refused the cell**, which is the outcome Trevor's stop condition was set against:
`whole_crop_gate` gate F reports 83 claim-bearing leaves and **0 anchoring gaps** on the post-state,
because the cell still cites a T1 source. Had the drop left it at zero sources the promote itself would
have refused, by design: `check_pre_state` raises "A claim-bearing cell may not be left uncited by this
promote: the T1 read comes first."

#### RULING 2 -- `ca_south_coast` zones 9, 10 and 11: LEAVE HELD, record the structure

The claim is a span, "Dec - Mar (early satsuma through late Pixie and Gold Nugget)". One URL per source
key cannot hold both ends: the early end is `crc3178`, the late end is `crc3568` (Pixie) or `crc3913`
(Gold Nugget, ripeness February to June, which is what actually reaches the cell's March end). Picking
one would silently credit it for the other's half. The three cells stay on `crc3178` and a finding
records it (`mandarin_clementine_region_span_single_anchor_pla465`, status `deferred`, routed to
**PLA-559**).

**This is not a mandarin defect.** It reaches any region cell bounded by an early variety at one end and
a late one at the other. PLA-559 carries the general case and is linked to plum's
`plum_self_fertile_boolean_european_default`, which states the family in its own words: *one record, two
types, a single-value shape that breaks wherever they diverge*. The only difference is which layer the
single value sits in -- a crop-level boolean and height range there, a per-cell `anchoring_urls[sid].url`
here.

## 4. The height ruling is UNCHANGED, and was re-verified rather than assumed

`mature_height_ft`, `mature_spread_ft` and `footprint_inches` stay `null`, and the promote **refuses**
if the crop carries any of them. The original ruling's own evidence was re-read: `crc0279` describes the
tree only as "Tree medium in vigor and size, spreading and round-topped", and the string "feet" appears
**0 times** on the page. That is exactly what the PLA-465 finding claimed, confirmed from bytes.

## 5. What the promote writes

On `mandarin-clementine` only:

- **7** `anchoring_urls.ucr_citrus` records: `url` and `verified`.
- **1** credit DROPPED from `failure_diagnostics[0]`, out of `sources` **and** `anchoring_urls`. The
  census of `ucr_citrus` cells goes **19 to 18**.
- **2** `open_findings` appended: the climate-claim citation record, and the span record routed to
  PLA-559.
- **1** `verification_status.field_additions` entry, `field: "ucr_citrus_anchor"`, carrying every URL,
  byte count, sha256 and the class each cell fell into.
- **1** dated addendum appended to the existing finding
  `mandarin_clementine_plant_dimensions_unusable_anchor_pla465`, the original summary byte-identical as
  a prefix.

The addendum exists because that record asserts a mechanism this pass retires. Per the append-only
convention it is **not** rewritten into current tense; the correction is appended and the original left
byte-for-byte, so no later pass reads "the crop's cited UCR anchor is a satsuma page" as current truth.

No prose, no dimension value, no other crop, no other source key.

## 6. Armor

**Suite** `tools/test_promote_pla465_mandarin_anchor.py`: **101 passed**, replay-pinned to `892c76fb`
via `promote_fixture.pre_state`, never live canonical.

**Harness** `tools/mutate_pla465_mandarin_anchor_suite.py`: **83 injected / 83 caught / 0 survived /
0 broken.** Liveness: anchor preflight 83/83 matching exactly once; **positive control = the WHOLE
suite green on the clean copy**; sentinel reddened as required; bytecode off; pytest rc 5 graded BROKEN.

**The over-reach defect class is what the suite is built around.** Because the likeliest failure here
is repairing too much, the KEEP and HELD cells are pinned on **both** sides, and the 19-cell census is
compared against an **enumerated constant** rather than derived from the walk it validates -- coverage,
not overlap.

**Trevor's stop condition is encoded as a refusal, not a workaround.** `check_pre_state` raises if the
drop would leave the cell with no source at all: "A claim-bearing cell may not be left uncited by this
promote: the T1 read comes first." Its driver
(`test_refuses_a_drop_that_would_leave_the_cell_uncited`) sets the cell's sources to `[ucr_citrus]`
alone and asserts the refusal, and the mutation `drop/UNCITED_CELL_ACCEPTED` confirms the guard fires.

### A NEAR-MISS ON THE RE-STAGE, AND THE GUARD IT PRODUCED

Writing the climate finding, a **fabricated sha256** went into the staged record. The CTAHR PDF had been
hashed, but only its first 16 characters had been read back; the remaining 48 were invented to fill the
field. This is `fill-the-shape-is-the-defect` exactly: a field whose shape is "64 hex characters" pulls a
plausible 64 hex characters out of you.

It was caught before any run by recomputing the digest, and the staged value replaced with the measured
one (`4d2a3549ec909ea85fc8be84efaea8ef3ed44ad31b4d8ee9547539c7eafaef47`). The **guard now in the
promote** closes the class: every 64-hex token appearing anywhere in the spec must be a member of
`EVIDENCE_HASHES`, the digests this session actually measured, or the base SHA. Mutation
`evidence/FABRICATED_SHA256_ACCEPTED` confirms it fires, and its driver asserts the matcher **both
ways** -- a fabricated digest refuses, a measured digest in the same position is accepted.

### FOUR GUARDS WERE WRITTEN, FOUND UNREACHABLE, AND REMOVED

None shipped as coverage. Each was caught by its own driver failing with the **wrong refusal message**,
which is the "an earlier check fires" pattern, and each is now a comment in the promote saying why it is
absent plus a driver pinning which guard does catch the case:

| guard | why it could never fire |
|---|---|
| no-op repoint (`to == from`) | `from` is pinned to `crc3178` and `to` must be in the closed target vocabulary, which excludes it |
| addenda count (`n_add != 1`) | an unapplied addendum refuses on the per-entry summary compare; a renamed target refuses as a changed non-target finding |
| `KEY` left in the dropped cell's `anchoring_urls` | `census()` **is** that predicate, so the census comparison fires first |
| post-census count (`!= CELLS_AFTER`) | the set comparison asserts the exact set, whose size is `CELLS_AFTER`; the count is implied |

The last two were found on this re-stage: one by a driver mismatch, one by the harness reporting
`drop/cells_after_not_pinned` as **SURVIVED**. That is the harness doing the job it exists for.

## 7. Gauntlet on `b2b875b7`

| check | result |
|---|---|
| `gate_all` | **121/121 PASS** |
| `whole_crop_gate mandarin-clementine` | PASS; 24 source ids, 0 uncatalogued, 0 non-T1; 83 claim-bearing leaves, **0 anchoring gaps** -- the dropped cell still cites a T1 source, so no gate refused it |
| `url_health_gate` (offline) | 0 null/empty |
| `plant_dimensions_gate --presence` | 0 violations; 121/128 carry the keys; 16 authored; ARMED |
| `register_completeness` / `register_coverage` | PASS / PASS |
| `release_verify --ref lemon` | **clean in every section**; 3 Step-5.5 pause-legibility notes, **verified byte-identical on the base**, so pre-existing |
| `problem_id_collision_gate` | 36 / 24 / 12 -- the pinned hold, unmoved |
| sibling pinned suites (464, 465 dims, 465 nulls) | **199 passed** |

### The whole `tools/` tree, re-run on the re-staged tooling

**5,763 passed, 2 failed, 1 skipped** (49m38s). The +28 against the 2026-09-18 run (5,735) is this
suite growing from 73 drivers to 101; **nothing new failed and nothing was disabled.**

**Canonical was never written this session**, so every one of those tests ran against the untouched
`892c76fb` and both failures are pre-existing by construction. Both were read, not counted:

1. `test_bare_host_scan.py::test_self_pathed_population_at_this_canonical` -- a real drift, filed as
   **PLA-544**, detailed below.
2. `test_cited_claim_scan.py::test_MUTATION_the_anchoring_only_walk_reproduces_the_false_pass` --
   `UnreportableAbsence: 8 of 28 cited URLs are uncached and therefore UNDETERMINED, not absent`, on
   leek/shallot/onion URLs. This is PLA-161's completion contract **doing its job**: it refuses to
   report an absence it cannot justify. `tools/.doc_cache` is gitignored and holds 1,216 documents
   locally, 8 short of what this test's crops need, so the test is cache-coverage dependent rather
   than data dependent. Nothing to fix in the dataset; worth knowing before anyone reads it as rot.
   PLA-544's convention now names this one too, for the same reason in a different key: its failure
   text should say what is uncached so it cannot be confused with a data defect.

### Found while gauntleting, NOT caused by this work -- filed as PLA-544

`tools/test_bare_host_scan.py::test_self_pathed_population_at_this_canonical` is **RED on the
untouched canonical**: 321/161 against a pin of 315/155. Bisected across every commit that touched the
canonical, it drifted at `a3f08375` (2026-09-04, PLA-8 batch 26) and has been red through **four
landed promotes** since, because `gate_all` and `release_verify` do not run it and the whole-`tools/`
run is not part of the promote ceremony.

The six new rows were **read, not counted**: all six are `uada_ext` cited **bare** on mulberry and
persimmon `mid_south` nodes while those crops path `uada_ext` elsewhere, and **all six are
`is_sole: True`** -- campaign C's narrow signal, not its flood. This post-state measures identically to
the base (321/161/80/37 both sides), so this promote neither causes nor moves it. Re-pinning the
literals without adjudicating the rows would convert a true report into a silenced one, which is how it
rode for two weeks; that is written into PLA-544 as out of scope.

## 8. Both rulings taken (2026-09-20); what is left

Ruling 1 and ruling 2 are folded into **one** re-staged run, as directed. What remains is the write and
the push. The other 15 cells stand as adjudicated: 7 repointed, 8 kept.

**Owed and not ticketed:** the targeted T1 read behind the climate finding. Its scope is now narrower
than when it was commissioned (see ruling 1): the claim is cited, the *sugar mechanism* is what wants a
statement.

## 8b. The citrus anchors Trevor asked about: NOT among the six new rows

Neither `citrusvariety.ucr.edu` on orange-navel/grapefruit nor the bare `tamu_agrilife` anchor on lemon
is among PLA-544's six new rows. **All six are `uada_ext` on mulberry and persimmon `mid_south` cells;
zero citrus.** But the measurement turned up something worth recording, because both do carry the citrus
container path:

| crop | the Flying Dragon row | anchor | sole citation? | in the 321? |
|---|---|---|---|---|
| grapefruit | `rootstock_options[2]` | `ucr_citrus`, **bare** | **yes** | yes, `sole=True` |
| orange-navel | `rootstock_options[2]` | `ucr_citrus`, **bare** | **yes** | **NO -- invisible to the scan** |

**The same defect, on the same row, with the same bare URL, and the instrument sees one and not the
other.** `self_pathed` only fires when the *same crop* paths that source id at a document somewhere
else. grapefruit does (`varieties` -> `crc3602`), so its Flying Dragon row surfaces. orange-navel never
paths `ucr_citrus` anywhere, so it has **0** self-pathed rows and its identical bare, sole-cited Flying
Dragon anchor is structurally invisible.

The corollary matters more than the instance: **absence from `self_pathed` is not absence of defect.**
The scan measures "this crop cited a source two ways", not "this citation is bare". A crop that is
uniformly bare on a source drops out entirely, which is the worse case, not the better one.

lemon's bare `tamu_agrilife` anchors sit on `rootstock_options[0]` and `[1]` and are in the population
but **not sole** -- each row also carries a pathed `uf_ifas_hs1153` (HS402), so they are co-cited and
less severe than the Flying Dragon rows. None of this is new; all of it predates 2026-09-04.

Recorded on PLA-544 as part of the row adjudication it already owes.

## 9. Not in this, and named

- **oregano's `uarizona_ext` anchor is *Lippia graveolens*, a different genus at 6 to 10 ft.** Surfaced
  by PLA-465 promote 1 in the same breath as this one and still unrepaired. It is the same defect class
  (a per-cell anchor pointing at the wrong taxon) and wants the same cell-by-cell treatment.
- The four sibling citrus crops (lemon, lime, orange-navel, grapefruit) cite `ucr_citrus` at the **bare
  collection root** on nearly every cell, reserving an accession URL for `varieties` only. That is the
  laxer pattern and was **not** touched: this session repaired a wrong document, it did not run a
  convention pass. Whether those crops should name accessions is a separate question.
- The liveness LEDGER (`url_health_gate --online`) is a different instrument with its own
  WebFetch-only rule and was not updated. The three URLs here were confirmed live by reading their
  content, not by a status code.
