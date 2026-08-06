# PLA-114 — campaign D closes

**2026-08-06. Canonical `820af861` -> `72284f02`.** Four `plant_out` bare ids repointed, three
adjudicating findings filed, the re-price adjudication table extended with 14 verified entries.

**OPEN 8 -> 0.** 17 DECLARED-ANCHOR · 1 MODELED-ONLY (jalapeno, pre-existing) · 2 OPEN-SCOPED
(the pears, terminal per ruling).

---

## 1. The blocking reconciliation, and why it was not clean

D was priced at **26 decisions / 123 nodes**; the tool reported **20 / 100**. Six unaccounted.

All six left the scan during the `ae15df4` cold promote. **Zero from re-scoping, zero from a tool
change.** But only **five are genuine closes**:

| hunt | decision | verdict |
|---|---|---|
| #29 `ca_interior` / `uc_ipm` | repointed | closed |
| #25 `northern_tier` / `clemson_hgic` | repointed | closed |
| #26 `northern_tier` / `tamu_agrilife` | repointed | closed |
| #27 `se_gulf` / `tamu_agrilife` | repointed | closed |
| #8 `warm_arid` / `tamu_agrilife` | repointed | closed |
| **#28 `se_gulf` / `clemson_hgic`** | **untouched** | **still bare — a masking artefact** |

Across the arc, **15 nodes genuinely became pathed and 8 were merely hidden**.

## 2. The mechanism, which decided Ruling 1

`bare_host_scan` sets `is_sole=False` when a cell cites **any** non-bare source, and
`campaign_d_reprice` filters on it. So **adding a pathed co-source removes every remaining bare
citation on that cell from the count, without fixing any of them.**

That is how #28 vanished while still bare at `se_gulf.resolved_by_zone.8` — the cold promote
repointed *TAMU* on that cell — and it is what the §7 promote did to five nodes.

Ruling 1 (repoint, do not drop) was flagged overridable on a repo-side reason. There is one, and
it points the same way but harder: **add-alongside does not merely fail to close a decision, it
conceals the bare citation.** Repointing is the only option that closes *and* unmasks.

## 3. Scope read against the data, not the metric

Of **55** masked bare citations, only **13** have a same-institution pathed co-source, and reading
those documents cuts the mechanical set to **4**:

- **7 lime cells** would have repointed `ucanr_ext` onto UC IPM's `agriculture/citrus/` **pest**
  page. **Refused** — campaign D established both UC IPM citrus pages carry zero temperatures, so
  pointing planting, bloom and harvest anchors at them is `right-document-wrong-claim`, the exact
  defect F2 records.
- **2 lemon zone cells** would have gone onto the freeze page, which supports a **suitability**
  claim only.
- The remaining **4** are `plant_out` arms whose co-source publishes the planting **rule** itself.

"Same institution, pathed on the same cell" is the SIBLING-PATHED shape this campaign has twice
ruled **a lead, not a verdict**. It held again.

`ca_south_coast` targets Mauk rather than Lazaneo although both sit on the cell: `ucanr_ext`'s own
catalog host is `ucanr.edu` and Lazaneo is on the Association domain — the host/id mismatch this
arc has hit twice (`nmsu_chart` on a TAMU host; `aggie-hort` vs `aggie-horticulture`).

## 4. What closes a decision

A finding that **names the source id AND declares the anchor**. Naming-to-decline does not — the
§7 findings named `ucanr_ext` only to say "stays bare; still open", which satisfies the V2
vocabulary scan and closes nothing. That distinction is why V2 read 13 of 20 adjudicated while the
verdict read OPEN.

Two bugs in the first cut, both caught by the tool refusing the table entries rather than by me:
the lime declaration was filed on **lemon**, and hunt #32 is `low_desert_az`/**`ucanr_ext`**, not
`uariz_ext`.

## 5. The load-bearing line

**The metric answers "are the DECISIONS adjudicated", not "are the CITATIONS fixed", and on lemon
and lime those diverge by 51.**

At the close: **162 bare citations** on the two crops, **111 counted**, **51 invisible**. A reader
seeing "0 of 20 open" would reasonably conclude D is complete. It is complete *as a research
campaign*; the bare institution roots it set out to eliminate are not all gone.

Filed to PLA-138 as the **fifth** instrument failure of this class — the previous four were zeros
that were wrong; this is a completion that would be.

## 6. A sixth, found while fixing the fifth

**A guard pinned to a historical SHA stops protecting the moment the tool's analysis tables
change**, because the verdict is computed at read time. Extending `ANCHOR_FINDING` by 14 entries
turned three shape assertions red against a frozen fixture that had not moved.

Fixed by evaluating the pinned suite with **the table as of that state** — an entry whose finding
does not exist on the crop in the fixture was not in the table then. The live
`TABLE CLAIMS x BUT IT IS NOT ON THIS CROP` guard is untouched, and it is what caught the lime
declaration on the wrong crop.

Also filed to PLA-138, with a note to audit the other pinned suites for the same exposure.

## 7. Terminal state

| | |
|---|---|
| decisions | 17 DECLARED-ANCHOR, 1 MODELED-ONLY, 2 OPEN-SCOPED, **0 OPEN** |
| pears | **OPEN-SCOPED, deferred to the UC fruit-tree read** — terminal for D, and counted, not vanished |
| bare citations remaining | 51 on lemon+lime, uncounted by the metric, recorded in `campaign_d_metric_counts_adjudication_not_citation_repair` |
| filed and open as separate work | PLA-151, PLA-137, PLA-138, PLA-139, PLA-140 |

**Not in this pass:** the UC fruit-tree read. It needs its own **scoping** task first — nobody has
measured whether it is two pear decisions or the whole deciduous family, and "the two pears" may be
undercounting it the same way "14" undercounted D.
