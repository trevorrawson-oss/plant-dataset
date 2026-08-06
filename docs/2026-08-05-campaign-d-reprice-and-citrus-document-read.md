# Campaign D — the re-price, and what reading the citrus documents changed

**PLA-114, 2026-08-05. Canonical `6b2dcb8e`, UNTOUCHED — this pass is measurement and document
reading only. No promote, no data edit.**

Reproduce with:

```bash
python3 tools/campaign_d_reprice.py            # the numbers below
python3 tools/campaign_d_reprice.py --vocab    # the three-vocabulary detail, per decision
python3 tools/campaign_d_reprice.py --cells    # node-citations collapsed to physical cells (S6a)
python3 -m pytest tools/test_campaign_d_reprice.py -q     # 33 tests, every check mutation-tested
```

---

## 1. The ledger under-counts campaign D by 12 decisions

`docs/citation_arc_hunt_ledger.md` prices D at **11 hunts / 14 decisions**. Measured, it is
**18 hunts / 26 decisions / 123 nodes**.

The 14 is D's own eleven hunts and nothing else. It omits the citrus residue that campaigns A
and C explicitly deferred *into* D — the `lemon` and `lime` rows under hunts #3, #4, #5, #6
(`ucanr_ext`), #8 (`tamu_agrilife`), #14 and #21 (`uariz_ext`). The ledger's own note column
says "Residue: `lemon`, `lime` -> campaign D" **seven separate times**; the campaign table just
never added them to the number.

| | hunts | decisions | nodes |
|---|---|---|---|
| D's own hunts (#16, #18, #23, #25-32) | 11 | 14 | 41 |
| citrus residue deferred in by A and C | 7 | 12 | 82 |
| **true campaign D** | **18** | **26** | **123** |

The residue contributes its citrus rows only — A and C settled the rest of those hunts, and
re-counting them would inflate D with closed work. That restriction is asserted, not assumed
(`test_residue_hunts_contribute_citrus_only`).

This is the arc's over-count trap running in reverse. Every previous campaign was priced too
HIGH because a citation total was read as a count of open questions. D was priced too LOW
because deferred work was described in prose and never added to the number.

## 2. The three vocabularies — all tested, and they are NOT nested

PLA-114 asked for this specifically, because campaign C's kickoff measured "0 of 35 decisions
carry a finding naming their REGION", which was reproducible and was the wrong test.

| vocabulary | result | status |
|---|---|---|
| V1 region-named finding | 6 of 26 | TESTED |
| V2 source-id-named finding | 5 of 26 | TESTED |
| V3 per-cell prose (`plantings_provenance`, `*_basis_seasoned`, the note fields) | 3 of 26 | TESTED |

**The prediction that D would repeat C's mistake half-held, and the interesting half is the
other one.** V1 does not come back at zero here, so D is not a re-run of C. But the
vocabularies turn out not to be nested:

- **1 decision is adjudicated by V3 alone** — `jalapeno` / `fl_peninsula`. Its anchor finding
  says only "ufifas" while the crop cites both `ufifas_ext` and `uf_ifas_vh021`, so the alias
  check refuses it on V2; its `plantings_provenance` and both `heat_pause.basis_seasoned` fields
  declare the pause months modeled.
- **3 decisions are adjudicated by V2 alone** — `edamame` and both pears in `ca_north_coast`.

Running any single vocabulary under-reports. That is now a test
(`test_the_three_vocabularies_are_not_nested`), so if it ever collapses to nesting the cheaper
single scan becomes defensible — and until then it is not.

**Two corrections were forced during the measurement, both worth recording:**

- **V3 was under-scoped on its first cut** and reported a clean 3 while reading only four
  `*_provenance` / `*_basis` fields. The per-cell prose actually lives in
  `suitability_note_*`, `frost_risk_note_*`, `region_notes_*` and `zone_notes` as well. Widening
  the field list to the schema (not to the fields that happened to carry an adjudication) left
  the count at 3 — so it is now a *measured* 3 rather than a lucky one.
- **A refused V2 alias was short-circuiting the remaining vocabularies.** `adjudicate()`
  returned OPEN on the refusal and never asked V3, which hid the one V3-only adjudication in the
  campaign. Same single-test mistake as C's "0 of 35", one layer down.

## 3. What actually prices D: SIBLING-PATHED, and no vocabulary scan would have found it

**lemon's bare nodes are overwhelmingly cold-hardiness cells, not planting-date cells.** Of 123
nodes, 48 are `resolved_by_zone` cells carrying `suitability` and `min_winter_temp_f`. D is not
shaped like A, B or C, and the (region, source) hunt unit is the wrong one for it — as the
ledger already suspected.

For six decisions, the **same region, same zone, same source id on a sibling citrus crop already
carries a pathed document**:

| hunt | decision | sibling already citing a document |
|---|---|---|
| #25 | lemon / northern_tier / `clemson_hgic` | lime + mandarin-clementine → `hgic.clemson.edu/cold-tolerance-in-citrus/` |
| #26 | lemon / northern_tier / `tamu_agrilife` | lime → `aggie-horticulture.tamu.edu/fruit-nut/fact-sheets/citrus/` |
| #27 | lemon / se_gulf / `tamu_agrilife` | lime → same TAMU document |
| #8 | lemon / warm_arid / `tamu_agrilife` | grapefruit + lime → same TAMU document |
| #29 | lemon / ca_interior / `uc_ipm` | lime + mandarin + orange-navel → `ipm.ucanr.edu/agriculture/citrus/` |
| #31 | lemon / warm_arid / `clemson_hgic` | lime + mandarin → Clemson cold-tolerance (1 of 3 nodes) |

lime's `northern_tier.resolved_by_zone.3` cites the pathed Clemson page; lemon's
`northern_tier.resolved_by_zone.3` cites bare `hgic.clemson.edu`. Identical cell, identical
claim, identical source id — one pathed, one bare.

**This collapses the SEARCH, not the VERIFICATION**, and the tool says so in its own docstring.
[[sibling-precedent-pressures-a-wrong-repoint]] is exactly this shape: eight siblings citing one
document pressured a repoint onto pomegranate, and NC State ch. 15 turned out to have zero
mentions of it. So the documents were read before anything was believed.

### The measurement that was confidently wrong

The first run reported **SIBLING-PATHED = 0**, cleanly. That zero was a bug in the tool's own
path parser: `resolved_by_zone.3` has a numeric dict key the regex did not match, so every path
silently resolved to the parent — which carries no `anchoring_urls` — and every sibling lookup
found nothing. The finding was real and the instrument said otherwise.

`assert_resolver_agrees_with_scanner` is the regression: `bare_host_scan.scan` builds node paths
by an independent recursive walk while `resolve()` parses them back as strings, so they can only
agree if the parser is right. `test_MUTATION_a_broken_resolver_is_caught_not_silently_zeroed`
re-introduces the original bug and asserts the guard fires rather than reporting zero. Suspect
your own arithmetic before believing a flood — or a drought.

## 4. Reading the documents: the lead REFUTES for lemon's number and SUPPORTS its verdict

All four candidate documents were already in `tools/.doc_cache/` and all four are readable (not
WAF blocks — [[waf-block-pages-cached-as-absence]] checked).

**Clemson, "Cold Tolerance in Citrus"** (`hgic.clemson.edu/cold-tolerance-in-citrus/`) — mentions
**lemon exactly once**, in the taxonomy sentence ("Acid citrus includes lemons, limes,
calamondins, and kumquats"). It publishes temperatures for **satsuma (15°F) and kumquat (15°F)
only**, and says of everything else "be sure to check the cold hardiness for any citrus being
planted". It gives no lemon number.

**TAMU, "Citrus"** (`aggie-horticulture.tamu.edu/fruit-nut/fact-sheets/citrus/`) — Julian Sauls'
full Texas home-citrus guide. Its numbers are freeze-protection operating points (24°F vs 26°F
duration, sprinkler critical 28°F calm / 30°F windy) and one satsuma figure (18°F dormant,
damaged at 24°F in December). It gives no lemon number either. What it *does* carry is two
things that bear directly on lemon: **"residents of freeze-prone areas should grow only
cold-hardy types of citrus such as kumquats, satsuma mandarin, tangerines, calamondin and some
tangelos"** — lemon is excluded — and **"The smaller citrus types (calamondin, limes, kumquats,
lemons and limequats) are best suited to container culture"**.

**UC IPM citrus** (both `agriculture/citrus/` and `home-and-landscape/citrus/`) — pest and
disease pages. Zero occurrences of "hardy", "cold hard" or any temperature. This is
[[right-document-wrong-claim]] in its purest form: correct institution, correct crop, and the
document has nothing to say about cold suitability. Hunt #29's lead is the weakest of the six
despite three siblings citing it.

**So the verdict splits by claim, not by cell:**

- The **suitability verdicts** (`unsuitable` in northern_tier z3-7, `survives_no_fruit` in
  se_gulf z8 / warm_arid z8) **are supported** — by lemon's explicit exclusion from TAMU's
  cold-hardy list, and by Clemson's ideal-range and 15°F hardiest-citrus figures against zone
  lows far below them. These are CASE 1 repoints for two of the three documents.
- The **numeric claim is not**. See §5.
- **Hunt #29 (UC IPM) is CASE 2**, not a repoint, despite having the most siblings.

TAMU's "Table 1" (variety characteristics, which may carry a hardiness column) is **not in the
cached text layer** — referenced in prose only. That is an UNDETERMINED, not an absence, and it
is the one thing that could still change hunt #26 and #27's answer.

## 5. New finding: lemon's "high-20s °F" damage threshold is not in any document cited for it

Lemon's `frost_tolerance_f = 28`, its `hardiness_notes_seasoned` / `_beginner`, and roughly
fifteen region prose strings all assert that lemon leaves and fruit are damaged in the **high 20s
°F**. It is load-bearing across the whole regional model — every `frost_risk_note_seasoned` in
the campaign reasons from it.

Scanning **every one of the 29 URLs lemon cites**, 17 of which are cached and readable, for a
lemon-adjacent temperature in the 24-32 °F band: **zero hits.**

The three documents cited *for the claim* were read individually and none carries it:

- Clemson cold-tolerance — satsuma and kumquat only
- TAMU citrus — freeze-protection operating points and satsuma only
- UF/IFAS **HS132** (cited alongside Clemson on `failure_diagnostics[2]`) — its variety table
  gives lemon a harvest season (July-Dec) and a disease list, and marks **calamondin and kumquat
  "Cold hardy" and Key lime "cold sensitive"** while giving **lemon no cold annotation at all**

**Scope this honestly.** The number is very likely horticulturally correct — it is standard
citrus knowledge. The finding is not "lemon's threshold is wrong"; it is "the number is
uncited, and three documents are credited for it that do not publish it."
[[absence-findings-are-document-scoped]] governs: this is measured against 17 readable cited
documents, not against the literature. Twelve of lemon's URLs are uncached and undetermined.

This is a CONTENT finding, not a citation repoint, and it is the most substantive thing the
campaign has turned up. It was invisible to every existing scan: the URLs are live, the nodes
cite a source, and the gates pass.

## 6. Where campaign D now stands

| verdict | decisions | nodes | what it means |
|---|---|---|---|
| DECLARED-ANCHOR | 3 | 7 | a finding on the crop names this source id as a portal |
| SIBLING-PATHED | 6 | 17 | a named document exists for the exact cell; **read, and split by claim — see §4** |
| MODELED-ONLY | 7 | 47 | windows declared derived; anchor id NOT adjudicated |
| OPEN-SCOPED | 2 | 6 | the two pears — an open finding names the next move (UC fruit-tree read) |
| OPEN | 8 | 46 | all lemon, all `ucanr_ext` / `uariz_ext` |

**7 of 18 hunts have no document search left** (#8, #23, #25, #26, #27, #29, #31).

**No document hunt remains for the "lemon tail" (#25-#31)** — the same conclusion campaign C
reached, arrived at differently. What is left on those seven hunts is authoring: repoint the
suitability cells at the two documents that support them, rule #29 CASE 2, and file the §5
threshold finding.

### The 8 OPEN decisions, itemized

| hunt | region | source id | nodes | arms | bare url |
|---|---|---|---|---|---|
| #3 | `ca_interior` | `ucanr_ext` | 7 | plantings, plant_out, bloom, harvest_start, harvest_end, z8, z9 | `https://ucanr.edu` |
| #4 | `ca_north_coast` | `ucanr_ext` | 7 | plantings, plant_out, bloom, harvest_start, harvest_end, z9, z10 | `https://ucanr.edu` |
| #5 | `ca_south_coast` | `ucanr_ext` | 8 | plantings, plant_out, bloom, harvest_start, harvest_end, z9/10/11 | `https://ucanr.edu` |
| #6 | `ca_desert` | `ucanr_ext` | 6 | plantings, plant_out, bloom, z9/10/11 | `https://ucanr.edu` |
| #14 | `low_desert_az` | `uariz_ext` | 7 | plantings, plant_out, bloom, harvest_start, harvest_end, z9, z10 | `https://extension.arizona.edu` |
| #21 | `ca_desert` | `uariz_ext` | 8 | plantings, plant_out, bloom, harvest_start, harvest_end, z9/10/11 | `https://extension.arizona.edu` |
| #28 | `se_gulf` | `clemson_hgic` | 1 | z8 | `https://hgic.clemson.edu` |
| #30 | `warm_arid` | `uariz_ext` | 2 | plantings, plant_out | `https://extension.arizona.edu` |
| | | **total** | **46** | | |

All lemon. These are planting/bloom/harvest arms and zone cells, not the suitability cells of the
tail, and they are the campaign-A shape: a **vegetable** planting table standing as sole source on
citrus. Expect CASE 2 on most, consistent with campaign A's measurement that lemon and lime have
**no UC row at all**.

## 6a. The CELL view — the decision unit still over-counts, one level below campaign A's fix

```bash
python3 tools/campaign_d_reprice.py --cells
```

**123 node-citations are only 91 distinct physical cells.** One cell can carry TWO bare source ids
and is then counted once per id: `lemon/warm_arid/plantings[0].plant_out[0]` cites bare
`uariz_ext` AND bare `clemson_hgic`, so it appears under hunt #30 and again under hunt #31. It is
one cell and one authoring question. Campaign A corrected pairs -> decisions; the decision unit
still over-counts CELLS by 32.

27 of those 32 get the same verdict on both arms (no extra work). **Five are SPLIT — one arm has a
document lead and the other does not, and the cell is not settled until both are:**

| cell | arm A | arm B |
|---|---|---|
| `ca_interior.resolved_by_zone.8` | #29 `uc_ipm` SIBLING-PATHED | #3 `ucanr_ext` OPEN |
| `ca_interior.resolved_by_zone.9` | #29 `uc_ipm` SIBLING-PATHED | #3 `ucanr_ext` OPEN |
| `se_gulf.resolved_by_zone.8` | #27 `tamu_agrilife` SIBLING-PATHED | #28 `clemson_hgic` OPEN |
| `warm_arid.plantings[0]` | #31 `clemson_hgic` SIBLING-PATHED | #30 `uariz_ext` OPEN |
| `warm_arid.plantings[0].plant_out[0]` | #31 `clemson_hgic` SIBLING-PATHED | #30 `uariz_ext` OPEN |

**#28 and #30 are therefore not independent work** — they are the second citation on cells that
hunts #27 and #31 already touch. That is 3 fewer authoring questions than the decision table
implies.

**And the decision-level verdict masks a partial coverage.** Hunt **#31 reads SIBLING-PATHED on
the strength of ONE zone cell while its `plantings` container and `plant_out` arm have no sibling
document at all** (1 of 3 nodes). Across all SIBLING-PATHED decisions only **15 of 17
node-citations** actually have a lead. Without this the closeout would have claimed a document for
work that has none.

## 6b. Findings to file — none are in the dataset yet

| # | proposed id | scope | verdict | evidence |
|---|---|---|---|---|
| F1 | `lemon_cold_damage_threshold_uncited` | lemon, crop-level | CONTENT — uncited + mis-credited | §5: 0 of 17 readable cited documents carry it; HS132 annotates kumquat/Key lime for cold and leaves lemon blank |
| F2 | `lemon_ca_interior_uc_ipm_no_cold_content` | lemon `ca_interior` (#29) | CASE 2 | both UC IPM citrus pages are pest/disease; zero "hardy" or temperature occurrences |
| F3 | `lemon_warm_arid_plantings_no_citrus_document` | lemon `warm_arid` (#30 + #31's 2 uncovered nodes) | CASE 2 | no sibling citrus crop cites a pathed document for these two nodes; AZ1005 is a VEGETABLE calendar |
| F4 | `lemon_tamu_table_1_not_in_text_layer` | lemon, #26/#27 | UNDETERMINED | Table 1 is referenced in prose but absent from the cached text layer — record as undetermined, never absence |

**Repoints owed (edits, not findings)** — the suitability verdicts the documents DO support:

| hunt | cells | repoint to |
|---|---|---|
| #25 | `lemon/northern_tier` z3-z7 | `hgic.clemson.edu/cold-tolerance-in-citrus/` |
| #26 | `lemon/northern_tier` z3-z7 | `aggie-horticulture.tamu.edu/fruit-nut/fact-sheets/citrus/` |
| #27 | `lemon/se_gulf` z8 | same TAMU citrus fact sheet |
| #8 | `lemon/warm_arid` z8 | same TAMU citrus fact sheet |
| #31 | `lemon/warm_arid` z8 **only** (NOT its plantings/plant_out — see F3) | Clemson cold-tolerance |

## 7. Carried cautions

- **SIBLING-PATHED is a lead, never a repoint.** Six decisions had a named document; reading
  them supported the suitability verdict, refuted the numeric one, and killed hunt #29 outright.
  One-for-one repointing would have credited three institutions with a number none publishes.
- **A pathed URL on a sibling does not support THIS claim** — the standing arc caution, now with
  a second instance behind it.
- **TAMU Table 1 is undetermined**, not absent. It is the open thread on #26 and #27.
- `aggie-horticulture.tamu.edu` resolved fine from cache; the known redirect loop is with
  `aggie-hort.tamu.edu`, a different host.
