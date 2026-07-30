# Citation-integrity cleanup arc — kickoff

> ## ⚠️ SUPERSEDED IN PART. READ `docs/kickoffs/47-citation-arc-continuation-handoff.md` FIRST.
> Two hunts ran on 2026-07-30 and **the plan in this document is no longer the right one.** Its §5
> banner already corrects three of its own premises; 47 corrects the *order of work*. The short
> version: **most of these citations cannot be repointed at any effort** — no extension service
> publishes bloom dates (confirmed independently at UAEX and NC State) — so the next move is ONE
> roster-wide declaration pass, not 30 more document hunts. That is the difference between ~14
> sessions and 5–6. Everything here about *method* still holds; everything about *sequence* does
> not.


**Written:** 2026-07-29, at the close of the post-asparagus hardening pass.
**Canonical at writing:** `dd24b180` (pushed, `origin/main` `3d89bed`; 128 crops / 121 certified).
**Run this in a FRESH session.** Everything needed is here, in `CURRENT_STATE.md`, and in
`docs/2026-07-29-hardening-session-outcomes.md`.
**Start at §5** — a 20-cell sample pass that answers "is the data wrong, or just the citations?"
before anyone commits to the grind. §5b's triage is already done.

---

## 1. Why this arc, and why it is the important one

"T1-or-it-doesn't-ship" is the product's actual moat. **A bad citation is worse than a missing
one, because it looks verified.**

The evidence that started this: asparagus shipped with **4 bad citations out of ~21 sources (~19%)**,
and **all four survived an 11/11 T1 source-truth sample**. `unr_fs0261` is a real UNR Extension
fact sheet whose only mention of the crop is the string `"Stems - asparagus"` in a list of edible
plant parts. Even at 5% rather than 19%, the roster carries dozens of bad citations inside certified
data.

Two later passes made it worse, not better. This is not a hypothesis any more:

- The 2026-07-27 harvest sweep found three fresh instances of the same shape (`auburn_aces`, UNR
  3017, plus a near-miss stretching UC's "Central Coast" onto our north/south coast regions).
- The 2026-07-29 hardening pass found **six more, verified by direct fetch** (§6 below), including
  a **fabricated rationale** attributed to a real document and a **T2 retail chart served from a
  `ucanr.edu` URL**.

**Crucially, tier and claim-support are two different axes, and tier discipline cannot catch
claim-support failure.** All four asparagus defects were `tier: T1`,
`source_class: university_extension` — genuine land-grant documents cited for claims they do not
contain.

---

## 2. Read these first

| what | where |
|---|---|
| the arc's original framing | `docs/2026-07-27-state-of-play-and-next-steps.md` §5 |
| the six new verified instances + the design correction | `docs/2026-07-29-hardening-session-outcomes.md` |
| the tier model, measured rather than assumed | `docs/2026-07-27-source-tier-model-kickoff.md` |
| the WebFetch-PDF fabrication hazard | `asparagus.verification_status.open_findings` id `webfetch_pdf_summaries_are_not_sourcing` |
| standing rules (incl. the two added 2026-07-29) | `CLAUDE.md` |

---

## 3. The surface, measured (not estimated)

Measured against `dd24b180`. The earlier §5 estimate of "2,660 citation pairs" was **an order of
magnitude low** — it counted something narrower.

| quantity | value |
|---|---|
| `source_catalog` entries | **190** (181 T1, 9 T2) |
| catalog ids actually referenced | 165 (**25 never cited** — dead catalog rows) |
| referenced ids missing from the catalog | **0** (the catalog is complete w.r.t. references) |
| `anchoring_urls` (id, url) pairs across all crops | **29,447** |
| distinct URLs among them | **1,175** |
| **per-cell URLs that are a BARE HOST** | **1,576 pairs across 26 source ids** |

`source_class` distribution is 158 `university_extension`, 6 `extension_master_gardener_program`,
6 `commercial_seed_company`, 5 `horticultural_authority`, 3 `government_observation_network`, plus
singletons.

**Do not try to fetch 29,447 pairs.** Work the 1,175 distinct URLs, then weight the manual pass by
how many cells each URL carries.

---

## 4. THE DESIGN CORRECTION — read this before writing any script

The original plan proposed three tiers:

| tier | check | status after 2026-07-29 |
|---|---|---|
| A | does every cited URL resolve? | **INSUFFICIENT ALONE — see below** |
| B | does the document mention the crop at all? | still the best value-for-effort |
| C | does it support *this specific claim*? | manual, sampled, highest value |

**Tier A on its own is close to worthless here, and this is measured:** every portal-root defect
found in the hardening pass returns **HTTP 200**. `msu_ext`'s catalog root serves an Incapsula block
page (842 bytes, 80 chars of text) at 200. `ndsu_ext`, `sdsu_ext`, `umaine_ext`, `iastate_ext`,
`uconn_ext` and `mu_ext` all return 200 as institutional homepages. A liveness check passes all of
them and learns nothing.

Worse, tier A has a **false-negative** mode too: **UF/IFAS HS546 returns 410 while its content is
perfectly fine via archive.** "Dead but correct" and "live but wrong" are different defects and must
be classified separately — do not let a link-rot sweep delete a good citation.

---

## 5. START HERE — the 20-cell SAMPLE PASS, before committing to anything

> ## ✅ RUN 2026-07-29. OUTCOME: **ESCALATE** — full write-up in
> ## `docs/2026-07-29-citation-cleanup-sample-pass-outcome.md`.
>
> **The decision rule fired on the correctness branch.** 92 California windows adjudicated against
> the UC planting-date table they should rest on: **39 SUPPORTED / 35 DIVERGENT / 18 CONTRADICTED
> (20%)**, against a ≥10% escalation threshold. The 18 collapse to **4 authoring decisions**, and
> **8 cells are corroborated defective by a second, independent, no-network test** (frost-tender
> desert cucurbits scheduled to go in the ground exactly ON the mean last-frost date, 10 days
> earlier than the crop's own declared `last_frost + 10` rule). Trevor needs to see those 8 before
> more crops certify.
>
> **But the grind is 4-20x smaller than this document budgets**, and three of its stated premises
> are wrong. Corrections, all measured (`tools/citation_provenance_scan.py`):
>
> | this doc says | measured |
> |---|---|
> | "the 20 rows are **17** distinct nodes" | **18** |
> | node path `ca_desert.z10` | real path is `regions.<region>.resolved_by_zone.<N>`, no `z` prefix |
> | "681 sole-source claims each needing a document located, **several sessions**" | 681 pairs are redundant per crop x region: **170 decisions** over **32 document hunts** |
> | "for 680 of the 681 SOLE rows the specific document **was never recorded anywhere**" | **false for all 26 bare-host ids** — every one also cites real pathed documents on other cells (`ncsu_ext` 1,742 pathed vs 99 bare; `clemson_hgic` 2,483 vs 12). **Zero bare-only ids.** |
> | "almost no free mechanical wins... only 10 pairs repointable from the catalog" | true of the *catalog*, misleading overall — `mid_south` already built a full per-document citation vocabulary (`uada_ext_spring_veg` 499 pairs/82 crops, `uada_ext_fall_veg`, `uada_ext_fsa6001`, `uada_ext_chill`) and left the **fruit** crops on the institution root. 22 crops, one hunt. |
>
> **And the 681 is not one defect class.** 53% of the SOLE nodes (257 of 481) sit on crops whose
> accepted `open_findings` ALREADY DECLARE the derivation — e.g. `okra_pilot_region_anchor_base_urls`
> states verbatim that the region anchors "use the institution/publication BASE URL rather than a
> live okra-specific page" and schedules exactly this sweep. A declared bare host is an *honest
> admission of derivation*; `unr_fs0261` was *a real document cited for a claim it does not contain*.
> Those need opposite treatment. **The UNDECLARED 224 are the real worklist**, and they are almost
> entirely fruit trees and berries in the two most recently built regions (`mid_south`/`uada_ext`,
> `mid_atlantic`/`ncsu_ext`).
>
> Two further findings worth carrying forward:
> - **A document can be the right one and still not contain the claim.** NMSU **CR457B** — exactly
>   what `nmsu_ext` should cite for `warm_arid` — publishes last-frost *by zone* and days-to-maturity
>   *per crop*, and **no per-crop planting-date window**. It backs the derivation's inputs, never the
>   window. Same shape as the `harvest-start-is-not-a-published-datum` lesson.
> - **`ucr_citrus`'s 33 SOLE pairs have a clean repoint method**: UCR CVC accession pages carry
>   "**Season of ripeness at Riverside**", and Riverside *is* `ca_interior`.
>
> Do NOT mass-repoint: pointing the California cells at the UC table would *create* a visible
> contradiction on 53 of 92 windows. Revised order of work is in §5 of the outcome doc.

**Do this first. It is roughly an afternoon and it can change the arc's priority in either
direction.**

### Why it comes first

The question this arc has never answered is: **is the DATA wrong, or are the citations just
pointed badly?** Those need completely different responses, and the counts cannot distinguish
them. A bare host is a *cannot-verify*, not a *known-wrong*: a cell can be well-researched and
badly recorded.

The one crop audited to the bottom (asparagus) found **both** — and the split matters. `msu_ext`
was cited on five cells with no crown timing in the document, yet **all five window values were
correct** (independently backed by in-state quotes). But `ca_interior` z9 said `Feb - Mar` while UC
ANR Pub 7234 — cited on that very cell — says harvest runs "late February through May", and that
one was **genuinely wrong**.

**Crucially, none of the data errors were found by the bare-host shape.** Every one came from
reading a source and comparing it to the cell. So the 1,576 bare hosts and the wrong values are
largely orthogonal problems, and only a tier-C read tells you the ratio.

### The method — three verdicts, and only three

For each sampled cell: work out what document the claim *should* rest on, locate it, read it, and
record one of:

| verdict | meaning | what it implies for the arc |
|---|---|---|
| **SUPPORTED** | a real document backs the stated window | citation-only defect — fix by repointing. High volume, low urgency. |
| **CONTRADICTED** | a locatable document disagrees with the cell | **the data is wrong.** High urgency; a grower is being misled. |
| **UNVERIFIABLE** | no document states this for this geography | the claim is unsourced derivation — a content finding, and repointing can never fix it. |

Record the verbatim quote and URL for every verdict, including UNVERIFIABLE (list what you fetched
and what it did *not* contain — that is the same evidence standard the asparagus sweep met).

### The decision rule — commit to it BEFORE you look

Write the outcome into this doc, then act on it:

- **0-1 CONTRADICTED of 20** → the 681 is a *provenance* problem, not a correctness one. Treat the
  arc as a repoint grind, schedule it behind feature work, and stop describing it as a data-quality
  risk.
- **≥2 of 20 CONTRADICTED (≥10%)** → it is a **correctness** problem. Escalate: the arc changes
  shape from citation hygiene into a data-correction arc, gets its own gauntlet and state trio per
  batch, and Trevor should hear about it before more crops certify.
- **High UNVERIFIABLE** → tells you what fraction of the 681 can never be fixed by repointing and
  needs honest downgrading instead. Budget that separately; it is authoring work, not sourcing work.

> **STATISTICAL HONESTY — do not over-read a clean result.** At n=20, seeing **zero** contradictions
> bounds the true rate at roughly **15%** (rule of three: 3/n), not at zero. A clean 20 means "the
> rate is probably under 15%", which is reassuring but is NOT "the data is fine". If you need a
> tighter bound, n=60 gets you to ~5%. Say which you did.

### The sample — deterministic, stratified, already drawn

No randomness, so it is auditable and nobody can be accused of cherry-picking: stratified across the
source ids carrying the most SOLE citations, stride-sampled within each so picks spread across crops
and regions. **Declared restriction:** it draws only from nodes stating a *concrete* window (a string
`plant_out`/`harvest`), because the question is whether the windows a grower reads are wrong;
frost-offset structures and `bloom` sub-blocks are a different claim type and are out of scope for
this measurement.

20 rows across 16 crops, 9 regions, 8 source ids — every one a SOLE-source bare-host node on a
certified crop:

| # | source id | crop | node | the claim to check |
|---|---|---|---|---|
| 1 | `ucanr_ext` | acorn-squash | `ca_desert.z10` | `plant_out` Jan 15 - Feb 15; `harvest` Apr 15 - May 31 |
| 2 | `ucanr_ext` | honeydew-melon | `ca_desert.z11` | `plant_out` Feb 1 - Mar 20; `harvest` Jun 1 - Aug 10 |
| 3 | `ucanr_ext` | okra | `ca_south_coast.z9` | `plant_out` May 1 - Jun 15; `harvest` Jul 10 - Oct 31 |
| 4 | `uc_mg` | acorn-squash | `ca_desert.z10` | `plant_out` Jan 15 - Feb 15; `harvest` Apr 15 - May 31 |
| 5 | `uc_mg` | cantaloupe | `ca_north_coast.z10` | `plant_out` Apr 15 - Jun 1; `harvest` Jul 25 - Oct 10 |
| 6 | `uc_mg` | pumpkin | `ca_desert.z9.second_planting` | `plant_out` Jul 1 - Jul 31 |
| 7 | `uariz_ext` | cantaloupe | `low_desert_az.z10` | `plant_out` Feb 1 - Mar 15; `harvest` May 1 - Jun 30 |
| 8 | `uariz_ext` | lemon | `ca_desert.z10` | `plant_out` Feb - Apr; `harvest` Nov - … |
| 9 | `uariz_ext` | lime | `low_desert_az.z10` | `plant_out` Feb - Apr; `harvest` Jun - Nov |
| 10 | `tamu_agrilife` | acorn-squash | `warm_arid.z8` | `plant_out` May 1 - Jun 15; `harvest` Sep 1 - Oct 20 |
| 11 | `tamu_agrilife` | butternut-squash | `warm_arid.z8` | `plant_out` May 1 - Jun 15; `harvest` Sep 1 - Oct 20 |
| 12 | `tamu_agrilife` | shallot | `rgv.z10` | `plant_out` Oct 1 - Nov 15; `harvest` Jan 29 - Apr 14 |
| 13 | `uada_ext` | blueberry | `mid_south.z7` | `plant_out` March to April; `harvest` June to July |
| 14 | `uada_ext` | oregano | `mid_south.z8` | `plant_out` Apr 8 - Apr 29 |
| 15 | `uada_ext` | sage | `mid_south.z8` | `plant_out` Apr 8 - Apr 29 |
| 16 | `ncsu_ext` | apple | `mid_atlantic.z8` | `plant_out` Dec - Feb (dormant); `harvest` Aug 13 - Sep 27 |
| 17 | `ncsu_ext` | cherry-sweet | `mid_atlantic.z8` | `plant_out` Dec - Feb (dormant); `harvest` Jun 4 - Jun 29 |
| 18 | `ncsu_ext` | pear-asian | `mid_atlantic.z8` | `plant_out` Dec - Feb (dormant); `harvest` Aug 3 - Sep 12 |
| 19 | `ucr_citrus` | grapefruit | `ca_interior.z8` | `plant_out` Spring; `harvest` Jan - May |
| 20 | `nmsu_ext` | acorn-squash | `warm_arid.z8` | `plant_out` May 1 - Jun 15; `harvest` Sep 1 - Oct 20 |

**Read the table carefully — some rows are the SAME NODE twice.** Rows 1 and 4 are both
acorn-squash `ca_desert` z10, and rows 10 and 20 are both acorn-squash `warm_arid` z8. They repeat
because **that node cites two sources and BOTH are bare hosts**, so it is still SOLE. The 20 rows
are therefore **17 distinct nodes** — check each node once, and record the verdict against the node.

That pattern is worth a finding in its own right, and it is the worse half of the problem:

> **200 of the 481 distinct SOLE nodes cite TWO bare hosts and nothing else.** They *look*
> well-cited — two independent extension sources! — while resting on nothing citable at all. A
> reviewer scanning for "does this cell have sources?" would pass every one. (The 681 rows are 481
> nodes: 281 citing one bare host, 200 citing two.)

**One genuine cross-crop duplicate to check:** rows 10/11 are different crops — acorn-squash and
butternut-squash — carrying a **byte-identical** `warm_arid` z8 window (`May 1 - Jun 15` /
`Sep 1 - Oct 20`) from the same two bare sources. That is either correct (two winter squashes really
do share a regional window) or the uniformity signature that exposed asparagus's 29 identical
harvest strings. Rows 16/17/18 are three different tree fruits sharing one `mid_atlantic` z8
planting window — same question, and dormant bare-root planting genuinely is shared across tree
fruit, so this one is probably fine. **Check the squash pair; it is the more suspicious of the two.**

**Row 13's `March to April` / `June to July` prose form** differs from every other row's
`Mmm D - Mmm D`. A format outlier often marks a differently-authored cell.

**Traps specific to this pass** (the full list is §7): distinguish a **seed** window from a
**crown/transplant** window from a **harvest** window — that exact confusion put wrong values on an
asparagus cell; do not stretch a source's stated geography onto ground it does not cover; county
Master Gardener material is **T1**, so do not discard it and call the cell unverifiable; and
**WebFetch summaries of PDFs are not sourcing** — `pypdf` or raw HTML only.

To redraw or widen the sample, the generator is `docs/` adjacent — regenerate with
`tools/bare_host_scan.py --sole` plus the stride rule described above, or just widen k per source id.

---

## 5b. The bare-host triage — DONE 2026-07-29, and it re-priced the arc

Groundwork, already done — it produced the SOLE ranking the sample pass above draws from.
A URL with **no path** is a domain root; it cannot support a crop-specific claim about
planting dates or pest thresholds, and it is the blind spot a liveness check cannot see
(every one returns HTTP 200).

### The triage is now quantified — run `tools/bare_host_scan.py`

Shipped 2026-07-29 so this is repeatable rather than a heredoc:

```bash
python3 tools/bare_host_scan.py            # summary by source id
python3 tools/bare_host_scan.py --sole     # only the critical rows
python3 tools/bare_host_scan.py --id uc_mg # every node citing one id
```

**SEVERITY SPLIT — the useful cut, and it needs no network.** For each bare-host citation the
tool asks whether the *same node* cites anything else:

| | pairs | meaning |
|---|---|---|
| **SOLE** | **681** | the node's only source is a domain root — **the claim rests on nothing citable** |
| CORROBORATED | 895 | a real source sits alongside; the bare host is redundant decoration, low-risk to repoint or drop |

**Work SOLE first.** Six ids carry 601 of the 681: `ucanr_ext` 188, `uc_mg` 131, `uada_ext` 100,
`ncsu_ext` 79, `tamu_agrilife` 53, `uariz_ext` 50. This is the arc plan's own "weight tier C toward
cells whose claims rest on a single source", now measured instead of assumed.

> **COST REALITY — read before scoping. This is a research grind, not a mechanical sweep.**
> Of the 1,576 pairs, only **10** can be repointed straight from the catalog (where the catalog row
> already holds a pathed URL and only the cells point at the root: `ucanr_san_diego_mg` 7,
> `nmsu_chart` 2, `cornell_ext` 1). For the other **1,566 — including 680 of the 681 SOLE rows —
> the catalog entry is ITSELF a bare host**, so the specific document was never recorded anywhere
> and has to be located per claim.
>
> Budget accordingly: this is per-cell sourcing work at the scale of a region arc, not an
> afternoon. Consider doing it **per source id** (all 188 `ucanr_ext` cells at once, since they
> likely share a handful of underlying documents) rather than per crop.

**This is a TRIAGE list, not 1,576 defects — adjudicate, do not mass-edit.** Two honest
possibilities per row, and they need different treatment:

1. The bare host is an **institution pointer** and the actual document is identified elsewhere on
   the cell (in `source_note`, a `source_quote`, or the cell prose). Then the fix is to **repoint
   the URL at the document**, which is mechanical and safe.
2. The bare host is **all there ever was**, and no specific document was ever consulted. Then the
   cell's claim is **unsourced**, and that is a content finding, not a URL fix.

Telling those apart is the work. Note the distinction between the **catalog** URL and the
**per-cell** URL: 55 catalog rows carry a bare host, but only 26 ids are cited on cells with one —
and some ids (e.g. `ucanr_san_diego_mg`, `nmsu_chart`) have a *pathed* catalog URL while individual
cells still point at the root. Fix the cells, not just the catalog.

**A useful prior from the hardening pass:** `tamu_agrilife` was one of these, and its fix was case 1
— TAMU **EHT-066** was located, verified by pypdf, and it *supported the claim precisely*. So expect
a meaningful share of these to be repointable wins, not content failures.

---

## 6. The seed set — nine instances already verified by direct fetch

Do not re-derive these; they are confirmed and are the arc's starting worklist.

1. **`msu_ext` is cited on all five asparagus `northern_tier` cells and contains no crown timing.**
   The cell URL serves a real 25,784-character MSU article — genuine land-grant, cited for a claim
   it does not make. The same defect five times.
2. **Five ids resolve to portal roots** with zero crop content: `ndsu_ext`, `sdsu_ext`,
   `umaine_ext`, `iastate_ext`, `uconn_ext`. All HTTP 200.
3. **`uconn_ext` points at the wrong host entirely** — the real UConn asparagus fact sheet lives at
   `homegarden.cahnr.uconn.edu`, not the cited `ipm.cahnr.uconn.edu`.
4. **`sdsu_ext` is cited on asparagus z3 but its sentence is a z4 statement** ("mid-April through
   June") that argues for a start two weeks earlier than the z3 cell says — cited where it
   contradicts.
5. **`umaine_ext` on asparagus z4** is cited for a rule that *forbids* the z4 window (after-frost vs
   an Apr 20 start = last_spring − 11 days). Either drop it or record an explicit dissent.
6. **The `uc_ipm` URL on `ca_desert` z9/z10/z11 is UC IPM's ARCHIVED page**, self-labelled *"not
   actively maintained … All links have been removed"*. A live equivalent exists **and carries more**
   (a California-specific 3-4 week / 8-10 week harvest ramp).
7. **A T2 trap wearing a T1 host:** UC MG Riverside's own Flyers page links a "planting calendar"
   that is a **Grangetto's Farm & Garden Supply** retail chart sourced to "Digital Seed" — served
   from a `ucanr.edu` URL, image-only so pypdf returns 22 characters. The most citable-*looking* and
   least citable thing in the sweep.
8. **A FABRICATED RATIONALE, retracted 2026-07-29:** the "Fusarium-in-cold-wet-soil" argument
   attributed to UMaine Bulletin #2071 **is not in that document** (`"cold wet"`, `"cold, wet"`,
   `"wet soil"`, `"cold soil"` all occur **zero** times). This is the worst shape in the class: not a
   wrong URL but an invented claim with a real citation attached.
9. **25 catalog rows are never cited** by anything. Cheap to audit and either use or drop (precedent:
   `uaex_cardoon` was dropped outright rather than admitted uncited).

---

## 7. Traps — every one of these has already caused a real defect here

- **WebFetch summaries of PDFs are NOT sourcing.** A research agent *fabricated* a document title
  and supporting quotes ("Peak harvest typically occurs April through June") for a Contra Costa
  handbook containing **no asparagus content at all**, from a WebFetch summary of a PDF. Worse than
  garbling, because it invents. **Download + `pypdf`, or raw HTML via `urllib`. Quote only text you
  personally extracted.**
- **WebFetch's markdown parse of an HTML data TABLE silently shifts columns and blanks cells**,
  producing a plausible-but-wrong grid. It caused three fabrication-class resistance grades. Pull
  raw HTML, or cross-check a second fetch.
- **Drawn-bar charts have no text layer.** Several extension planting charts encode windows as
  graphics; `pypdf` returns crop names and month headers only. Reading bar geometry is legitimate
  and has been done twice here (`nmsu_chart`, `unlv_mg_svn`) — but validate against a known row
  first, and never guess a mark's position.
- **Image-only PDFs** return ~20 characters from `pypdf`. Render (e.g. `fitz` at 2x) and read, or
  discard.
- **Geography stretch.** Do not map a source's stated region onto ground it does not cover. Known
  near-miss: stretching UC's "Central Coast" onto our north/south coast regions.
- **Sentence confusion within one document.** UC ANR Pub 7234 contains *both* a crown window and a
  **seed** window; a cell once carried values matching the seed sentence. Distinguish
  seed / crown / transplant / harvest, and home-garden from commercial.
- **Bot shields are not absence.** `canr.msu.edu` serves Incapsula block pages inconsistently at
  HTTP 200. Retry, vary the path, and record "could not determine" rather than "does not exist."

---

## 8. The tier model — the correction everyone gets wrong

Measured: **all nine `T2` entries are the SEED-TRADE and folklore band** (Old Farmer's Almanac,
Johnny's, seed companies, a gardening blog). **County Master Gardener pages, county planting
calendars and extension charts are `T1`**, and the outreach band already sits at T1 via
`source_class`.

Getting this wrong is a documented failure mode here: an over-strict bar **does not produce
silence, it produces unsourced derivation.** A previous pass repeatedly downgraded usable county MG
sources and left cells unsourced that were sourceable — that is how the asparagus "honest gap" grew.
Also: the arc's own false rejection of `unlv_mg_svn` was reversed once someone checked the catalog —
it is T1 and cited by 67 crops.

**So: check `source_catalog` BEFORE accepting any agent's "this fails the tier bar."**

---

## 9. Discipline (this is where previous passes went wrong)

- **READ every finding. Do not count them.** A gate reported 38 findings on this exact surface and
  **exactly one was a defect.** A count is not evidence. This is the single most repeated lesson in
  this repo.
- **Measure before gating, and be willing not to ship the gate.** Two gates were built, measured and
  deliberately left unwired this month (`logref_count_scan.py`, the stale-quote check at 45 hits).
  A noisy gate gets ignored, which is worse than none.
- **When a check floods, narrow the CHECK, not its scope** (the 38 → 3 → 0 trajectory).
- **Re-verify the data before acting on any record that describes it**, and run the gate that
  already covers the claim first. New standing rule in `CLAUDE.md`; it cost a 16-document sourcing
  pass to learn.
- **Verify subagent findings before relaying them.** Relaying unread agent output is itself a logged
  defect here. Every claim in §6 above was re-fetched by the main session.
- **Promote via a guarded script**, never by hand: pin the pre-state by SHA (or per-string sha256),
  abort on drift, prove the footprint EXACT, keep JSON COMPACT. Four examples from 2026-07-29:
  `tools/promote_logref_corrections.py`, `promote_empty_unsuitable_calendars.py`,
  `promote_hardening_item2.py`, `promote_finding10_label.py`.
- **Do not smuggle content fixes into a citation pass.** A repointed URL is mechanical; a cell whose
  claim no source supports is a **content** finding. Split them, and surface the second kind.

---

## 10. Suggested sequence

0. **Bare-host triage (§5b) — DONE 2026-07-29, `tools/bare_host_scan.py`.** The worklist exists and
   is quantified: 681 SOLE rows over 481 distinct nodes, 895 corroborated, six ids holding 601 of
   the SOLE rows, and only 10 pairs repointable from the catalog. The correction to the original
   expectation: **there are almost no free mechanical wins.**
1. **THE 20-CELL SAMPLE PASS (§5). START HERE.** ~an afternoon, and it decides everything after it:
   whether the 681 is a *provenance* problem or a *correctness* one. The sample is already drawn
   (17 distinct nodes) and the decision rule is written down — **commit to that rule before you
   look at a single source.** Do not skip ahead to step 2; the sample's outcome may reorder it.
2. **The nine seed instances (§6).** Already verified; decide repoint / drop / dissent-note per row,
   and handle the 25 uncited catalog rows.
3. **Tier B roster-wide:** for each of the 1,175 distinct URLs, fetch once (cache it) and grep for
   the crop name of every cell citing it. This is the mechanical pass that would have caught
   `unr_fs0261`. **Classify, do not auto-delete** — separate "dead but correct" from "live but
   wrong."
4. **Tier C, weighted sampling.** Prioritize cells whose claim rests on a **single** source — that is
   exactly where the asparagus 11/11 sample failed. This is the highest-value and only-manual tier.
5. **Only then** consider a gate, and only if the measurement supports one. A `url_health_gate.py`
   already exists — read it before writing anything new.

**Effort:** step 0 is done and step 1 is an afternoon. Steps 2-4 are the real arc and **will span
several sessions** — 681
sole-source claims each needing a document located, plus 1,175 URLs to sweep for tier B. Treat each
batch as its own release with its own gauntlet and state trio, and prefer batching **by source id**
over by crop, since cells sharing an id likely share a handful of underlying documents.

## 11. Done when

Every cited URL is either **(a)** confirmed to resolve *and* to contain the crop, **(b)** repointed
at the document that does, **(c)** dropped with the dependent claim re-sourced or the cell honestly
downgraded, or **(d)** recorded as a dated, deliberate exception (archive-only, geometry-read,
cited-for-a-documented-absence). Plus: a written statement of what tier C sampled, what it did
**not** cover, and the measured defect rate — so the next pass knows the true residual risk rather
than inheriting a green light.
