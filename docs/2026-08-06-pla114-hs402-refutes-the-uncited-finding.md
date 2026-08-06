# PLA-114 — the document lemon already cited refutes F1 and F5

**2026-08-06. Canonical `6b2dcb8e` -> `29b96b65`.** The promote ran, but only after its own premise
was refuted and rebuilt twice. Two of the five findings were false as written, and shipping them
would have put a false claim into an append-only record; a follow-on draft then wanted to rewrite
fourteen correct consumer strings, and that was wrong too. Both reversals came from reading the
text a mechanical measurement had stood in for.

Reproduce:

```bash
python3 tools/cited_claim_scan.py lemon --proximity 200
python3 -m pytest tools/test_cited_claim_scan.py -q          # 14 passed, 6 mutations caught
python3 -m pytest tools/test_promote_pla114_lemon_cold.py -q # 46 passed, 14 mutations caught
```

---

## 1. The finding set rested on a scan that was wrong

Campaign D's 2026-08-05 pass scanned "all 29 URLs lemon cites (17 cached and readable) for a
lemon-adjacent temperature in the 24-32 °F band" and reported **zero hits**. That zero became:

- **F1** — "the number is uncited, and three institutions are credited for it that do not
  publish it"
- **F5** — "of six T1 citrus cold documents read, exactly one publishes a temperature tied to
  lemon's own sensitivity class ... **four publish no lemon-applicable damage temperature at
  all**"

Both are false. **UF/IFAS HS1153/HS402, "Lemon Growing in the Florida Home Landscape"** —
catalogued as `uf_ifas_hs1153`, referenced **87 times on lemon**, cached and readable the whole
time — publishes four lemon-specific figures:

> "trees are susceptible to freezing temperatures: **defoliated at 22–24°F** (-4.4 to -5.6°C),
> **severe wood damaged at 20°F** (-6.7°C), **flowers and young fruit are killed at 29°F**
> (-1.7°C), and **mature fruit damaged at 28°F to 31°F** (-2.2°C to -1.8°C) (Castle 1983; Tucker
> and Wardowski 1987)."

It is the most lemon-specific cold document in the citation set, and it was never in the set of
six that F5 enumerated.

## 2. Why the scan said zero — the word "lemon-adjacent"

Not a cache miss and not a parse failure. The temperatures are 333 characters from the nearest
occurrence of "lemon", because **on a crop monograph the crop is the subject of the section and
is not repeated in every sentence**. The passage's own subject noun is "trees".

| proximity window | result |
|---|---|
| ±60 … ±300 chars | **0 hits — a clean, confident zero** |
| ±400 chars | 4 hits |
| no filter | 4 hits |

The tighter the window, the more confident the wrong answer. This is
[[adjudication-vocabulary-outruns-the-test]] moved from findings to documents: the document
declares its subject in the **title**, and the test looked for it in the **sentence**. It is
also [[a-clean-zero-can-be-your-own-parser]] for the third time in this arc — the same session
that caught its own SIBLING-PATHED = 0 parser bug shipped this one.

**`tools/cited_claim_scan.py` is the regression.** It scans with no proximity filter, labels
uncached URLs UNDETERMINED rather than absent, and `assert_absence_reportable` **refuses** to
call a zero an absence when any cited URL is unread, when the readable set is empty, or when a
proximity filter was used over a document whose title names the crop. `proximity_band_hits` is
kept deliberately as the wrong method so the test can re-introduce the original bug and prove
the guard fires. All six mutations are caught; one of them (deleting range-scanning outright)
initially survived and exposed a vacuous guard, now closed by a low-endpoint test.

> **Pattern, third instance this campaign.** Revising the conflated-string count from 8 to 1 came
> from counting lethality verbs per string rather than reading which noun each verb governs. That
> is the same failure as the proximity window that returned a clean zero on HS402, and as the path
> parser that reported SIBLING-PATHED = 0 because its regex could not match the numeric dict key in
> `resolved_by_zone.3`. In each case a mechanical proxy stood in for reading the text, produced a
> reproducible result, and was wrong in the direction of false confidence. Reproducibility is not
> validity; a measurement can only be trusted once the thing it stands in for has been checked at
> least once by hand.

## 3. Every document, re-read from raw bytes today

| document | cited by lemon? | lemon-applicable damage temperature |
|---|---|---|
| **UF/IFAS HS402** (`uf_ifas_hs1153`) | **YES**, 87 refs | **defoliated 22–24 °F; severe wood damage 20 °F; flowers/young fruit killed 29 °F; mature fruit damaged 28–31 °F** |
| **UC ANR 8100** (Geisel & Unruh 2003) | no | Table 1 rates lemon *Citrus limon* **H**; body: 29 °F for 30 min → "some frost damage to tender citrus plants"; Table 2 (FRUIT) buds/blossoms 27.0, button 29.5–30.5, green 27.0–29.5, tree-ripe 26.0–30.5 |
| **LSU AgCenter** cold tolerances | no (grapefruit 27, mandarin 6, orange 4, lime 2) | ~26 °F "all other citrus", explicitly "leaf or wood damage"; ranking ends "…grapefruit, **lemons**, and limes" |
| Clemson cold-tolerance | yes (bare host) | **none** — satsuma and kumquat 15 °F only |
| TAMU citrus fact sheet | yes | **none** — satsuma 18 °F; 24/26 °F duration and 28/30 °F sprinkler operating points |
| UF/IFAS HS132 | yes | **none** — table marks calamondin/kumquat "Cold hardy", Key lime "cold sensitive", **lemon blank** |
| UC IPM freeze page | no | ranking only ("Eureka lemon and grapefruit are among the most cold-sensitive scions"), zero temperatures |

**UC 8100 verified independently from raw PDF bytes** (`pypdf`, not WebFetch, per
[[webfetch-markdown-table-column-shift]]): 245,883 bytes, Table 1 lemon = H, and the 29 °F
sentence exact. Every figure the previous session transcribed checks out.

**Operational trap worth keeping:** the eScholarship URL is **user-agent gated**. Without a
browser UA it returns **HTTP 202, `text/html`, zero bytes** — a success status with no document,
the same shape as [[waf-block-pages-cached-as-absence]]. With a browser UA it returns 200 and
the PDF. A future session fetching it plainly would record UC 8100 as dead. It is not.

## 4. What the corrected finding set is

| # | id | status as planned | **corrected** |
|---|---|---|---|
| F1 | `lemon_cold_threshold_was_miscredited_now_uc8100` | resolved: repoint + finding + 28→29 | **REWRITE.** The mis-credit is **2 of 3, not 3 of 3** — `hardiness_notes_seasoned` credits "Clemson HGIC, Texas A&M AgriLife, UF/IFAS", and **UF/IFAS is correctly credited** (HS402). Clemson and TAMU are not. **The value change 28 → 29 stands** on 8100's onset figure — see §6 |
| F2 | `lemon_ca_interior_uc_ipm_repointed_to_freeze_page` | resolved: repoint | **STANDS.** Freeze page verified live (HTTP 200) and carries the ranking; `ca_interior` z8/z9 are suitability cells, so a ranking is the right support |
| F3 | `lemon_warm_arid_plantings_no_citrus_document` | open / CASE 2 | **STANDS** — both nodes verified bare, no sibling document |
| F4 | `lemon_tamu_table_1_not_in_text_layer` | undetermined | **STANDS** |
| F5 | `lemon_cold_threshold_single_source_divergence` | NEW — "four publish no lemon-applicable damage temperature at all" | **FALSE AS WRITTEN.** It omits HS402 entirely. Replaced by the narrow, real divergence: LSU's leaf-specific 26 °F against 8100's plant-level 29 °F, with HS402's 22–24 °F recorded as the defoliation endpoint — see §5 |

**The repoint table is unaffected and remains executable exactly as specified.** All nine cells
were re-verified today and every one still carries a bare URL: `northern_tier` z3–z7 (Clemson +
TAMU), `se_gulf` z8, `warm_arid` z8, `ca_interior` z8/z9. The suitability verdicts those
documents support are unchanged.

## 5. The prose is SOUND — a first draft of this section said otherwise and was wrong

An earlier cut of this document claimed the 14 strings attributing the high-20s threshold to
leaves *and* fruit were a stage conflation, with "the leaf half supported by nothing". **That
was an overstatement, and checking the strings one at a time is what caught it.**

Two corrections, and they compound:

**HS402's 22–24 °F is DEFOLIATION — leaf drop, the severe endpoint — not leaf-damage onset.** It
never contradicted leaves being damaged at a warmer temperature; it is a further point on the
same curve. 8100 says so explicitly in the paragraph that scopes its own figures: "Greater
damage occurs with colder temperatures, a longer duration of cold, or higher relative humidity."

**UC 8100's 29 °F covers foliage, because it says *plants*.** Verbatim, under its own "Trees"
heading (which contrasts with a separate "Fruits" section):

> "Citrus varieties vary in their sensitivity to frost. Generally, when temperatures fall to
> 29ºF (–1.7ºC) for 30 minutes or longer, some frost damage to tender citrus **plants** will
> occur. Table 1 gives relative frost sensitivity for selected citrus trees and rootstocks."

Whole-plant damage onset, duration-qualified at 30 minutes. So "leaves and fruit are damaged in
the high 20s °F" is supported, and re-labeling those strings as fruit-only would have introduced
an error rather than removed one.

**And none of the 14 asserts leaf DEATH at the threshold.** All 14 use *damaged* or *injured*
for leaves and fruit; every lethality clause is scoped to a different subject under a colder,
separately-named condition ("a hard freeze can kill an unprotected young tree to the ground";
"an unprotected tree does not make it through a typical winter"). The densest case,
`northern_tier.cold_basis_seasoned`, reads "far below [the high-20s °F at which lemon leaves and
fruit are damaged] and [the hard freeze that kills an unprotected tree to the ground]" — *kills*
sits in a relative clause on "the hard freeze". Counting death verbs per string flags 8 of 14;
reading which noun each governs flags **0**.

**No edit is owed to any of the 14 strings.** The authoring was already stage-aware.

What survives is far narrower: the only **leaf-specific** onset figure in evidence is LSU's
26 °F, three degrees below 8100's plant-level 29 °F. That is the divergence worth recording.

| claim | figure | scope |
|---|---|---|
| plant damage onset (incl. foliage) | **29 °F**, ≥30 min | UC 8100, tender citrus; Table 1 rates lemon H |
| leaf-or-wood damage | 26 °F | LSU, "all other citrus" — one bucket for M- and H-rated crops |
| defoliation | 22–24 °F | HS402, lemon-specific — the severe endpoint, not onset |
| mature fruit damage | 28–31 °F | HS402, lemon-specific |
| buds and blossoms | 27.0 °F | UC 8100 Table 2 |

## 6. `frost_tolerance_f`: 28 → 29 stands

`frost_effect` settles the semantics mechanically — all 43 `killed` crops carry exactly 32, so
the field is "the temperature at which `frost_effect` occurs". lemon carries `foliage_damaged`,
so the field wants **tissue damage onset**. 113 of 128 crops carry a value.

With HS402's figure correctly read as a severity endpoint rather than an onset, it was never a
candidate for this field, and the question is not three-way after all:

- **29** — UC 8100's onset for tender citrus, covering foliage ("plants"), warmer bound and so
  the safety edge for a frost warning. It also fixes the sibling ordering for the first time:
  lime 30 > lemon 29 > grapefruit / orange-navel / mandarin-clementine 28, matching both 8100's
  Table 1 (lemon H, grapefruit M) and LSU's ranking. Today lemon and grapefruit are tied at 28.
- 28 (current) is inside HS402's mature-fruit band, but that is a **fruit** figure for a field
  whose declared effect is foliage.
- 22–24 is defoliation, a different question entirely.

**The HS402 discovery does not overturn the value change. It overturns F1 and F5**, which
claimed the number was uncited and mis-credited to three institutions.

## 7. Carried forward

- **Bonus defect confirmed live.** `ucanr_ext_8256` → `anrcatalog.ucanr.edu/pdf/8256.pdf` 301s
  to `ucanr.edu/dept/anr-publishing/finding-anr-publications` and returns **HTTP 200 with
  `text/html`** — a landing page served as success. Exposure is **strawberry only** (10 refs,
  5 `anrcatalog` URLs); it is the only catalog id on the dead host. Needs its own issue.
- **The TAMU HortUpdate secondary is still dead** (infinite redirect between `aggie-hort` and
  `aggie-horticulture`), but the "two institutions" problem it created **has dissolved**: HS402
  is a second institution publishing lemon-specific numbers, and it was already cited.
- **`lsu_agcenter` on lemon is still zero** while grapefruit cites it 27 times — the
  SIBLING-PATHED lead stands, and LSU's ranking is verified.

## 8. What shipped

`6b2dcb8e` -> `29b96b65`, one promote, on the corrected disposition.

| | |
|---|---|
| `uc_anr_8100` | minted; records that its eScholarship URL is **user-agent gated** (plain fetch: HTTP 202, `text/html`, zero bytes) |
| `lemon.frost_tolerance_f` | 28 -> 29 |
| repoints | 9 cells / 15 node-citations across `northern_tier`, `se_gulf`, `warm_arid`, `ca_interior` |
| findings | F1-F5 filed (F1, F2, F5 `resolved`; F3, F4 `open`) |
| consumer prose | **none moved** — all 14 threshold strings pinned byte-identical by path |

Deliberately left bare, because those hunts stay open: `se_gulf` z8 `clemson_hgic` (#28),
`ca_interior` z8/z9 `ucanr_ext` (#3), and `warm_arid` `plantings` + `plant_out` (F3 — hunt #31
covered 1 of its 3 nodes, not 3).

**Guards:** 46, RED before GREEN, 14 mutations all caught. **Two were vacuous on the first sweep
and failed the same way** — asserting a substring that occurs elsewhere. `'202' in blob` was green
on the accessed date "2026-08"; `satsuma`/`kumquat` were green on a different sentence of F5. Both
now assert distinctive tokens.

**Gauntlet:** `whole_crop_gate lemon` PASS · `gate_all` 121/121 · `release_verify` no new concerns
(its 16 novel-region-key CONCERNs are byte-identical on the base — the known lettuce-leaf exemplar
mismatch for tree crops, which have `cold_basis_*` and `min_winter_temp_f` the annual vegetable
exemplar lacks) · COMPACT preserved · source-truth sample satisfied by reading every document in
this promote from raw bytes today.

**One knock-on, resolved honestly.** `tools/test_campaign_d_reprice.py` began failing because the
promote fixed what it measures: 123 bare node-citations became 105, 48 `resolved_by_zone` nodes
became 30, and all six SIBLING-PATHED decisions stopped being bare. That is the tool observing its
own campaign progressing, not rot. Re-baselining the constants each promote would erase the record
of what the arc was priced at, so the SUITE now reads the pinned `6b2dcb8e` pre-state it was always
a measurement of, while the TOOL still reports the live open number.

**Pre-existing, flagged not fixed:** `tools/test_build_berry_pilot_patch.py` calls `sys.exit(0)` at
module level, which aborts collection for the whole `tools/` directory — the module-level skip-guard
antipattern, and it means no one has run the suite directory-wide in a while.

## 9. The two documents in this promote need OPPOSITE fetch strategies

Checked before committing, because repointing four cells at a dead URL would be its own defect.
Every repoint target is live — but only if you ask correctly, and the two rules contradict:

| document | plain / `curl` UA | browser UA |
|---|---|---|
| **UC ANR 8100** (eScholarship) | **HTTP 202, `text/html`, ZERO bytes** | HTTP 200, `application/pdf`, 245,883 b |
| **TAMU citrus fact sheet** | **HTTP 200, 54,226 b** (contains satsuma, kumquat, cold-hardy) | **HTTP 403** (Cloudflare) |
| Clemson cold-tolerance | — | HTTP 200, 141,441 b |
| UC IPM freeze page | — | HTTP 200, 35,526 b |

A single "always send a browser user-agent" rule records **TAMU as dead**. A single "fetch plainly"
rule records **8100 as dead**. Both documents are live, both are cited by this promote, and either
blanket rule produces a confident false negative on one of them.

TAMU's 403 is site-wide for browser UAs (`aggie-horticulture.tamu.edu/` and `/fruit-nut/` behave
identically), which is what distinguishes a bot policy from a missing page — a dead document would
404 on the leaf and serve the parent. The repo has hit the friendly half of this before: the state
history records an Arizona `low-desert-citrus-varieties` 403 that was bot-blocking, with the page
confirmed live by other means.

**So a URL-liveness check cannot be a status-code check.** 403 is not dead, 200 is not alive
(the `anrcatalog` landing page and the WAF challenges of
[[waf-block-pages-cached-as-absence]] are both 200), and 202 with an empty body is neither. The
only reliable test is whether the response carries the document — content-type, plausible size, and
an expected token. Filed onto PLA-140.
