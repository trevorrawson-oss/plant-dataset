# Citation-integrity arc — the hunt ledger

**What this is.** The one place that records **which of the arc's document hunts are open and which
are closed**. Created 2026-08-03 because that had never been written down: the counts lived only as
prose snapshots inside kickoffs 46, 47, 48, 49 and 50, and every one of those went stale.

**Last reconciled:** 2026-08-03, canonical `e65aa63a` (after campaign A's repoint promote), HEAD `84c7eb2` + uncommitted promote.

> **COUNT RECONCILED 2026-08-03 — the shipped scan is the authority, confirmed.** Kickoff 50 §2 made
> this gating. An independent re-derivation that does *not* import the scan reproduces it exactly
> (614 pairs / 414 nodes / **167 decisions / 32 hunts**, California block **76 over 8**), and
> `region_of()` was checked against a structurally-determined region on every node carrying
> `anchoring_urls`: **0 disagreements.** The conflicting hand traversal (77/7) applied
> `len(sources) == 1` to the **region root**, whose value child nodes inherit — a rule that calls a
> cell *sourced* when it names two bare hosts. Working: `docs/2026-08-03-campaign-a-count-reconciliation-and-readjudication.md`.
> **The reconciliation itself changed no number;** the numbers below moved afterwards, when campaign
> A's repoint promote landed.

---

## How to read this, and the trap it exists to fix

The live count comes from:

```bash
python3 tools/citation_provenance_scan.py --decisions
```

That is the **authority for what the DATA says**, and it is self-updating, so it can never go stale
the way a prose snapshot does.

**But it OVER-COUNTS remaining work, and this is the whole reason the ledger exists.** The scan
measures citations, not rulings. When a hunt is closed by a *ruling* rather than an *edit* — the
adjudication concluded CASE 2, "the claim is unsourced," and filed findings instead of repointing —
the cells still cite the bare host, so the scan still counts them forever.

**Live scan (2026-08-03, campaign A CLOSED at `3f6d6ce4`): 115 decisions / 32 hunts.**
**Closed by ruling, still counted: 24 decisions** -- 9 `ucr_citrus`, 7 campaign-A closeout rulings
(arugula 2, edamame 1, okra 4), and the 8 cucurbit decisions held by the accepted
`ca_desert_fall_cycle_provenance_gap`.
**Genuinely open: 91 decisions.**

> Campaign A ran as **two promotes**: the repoint took the live count **167 -> 115** (52 decisions /
> 89 nodes / 178 anchor entries), then the closeout filed **5 findings over 9 decisions** and moved
> the count not at all -- which is the ledger's whole point. **Four of the eight California hunts are
> now fully resolved** (#9, #10, #11, #12, the `uc_mg` side). The four `ucanr_ext` hunts stay PARTIAL
> on `lemon`/`lime`, deferred to campaign D, plus the two pears deferred to a UC fruit-tree read.

Update the Status column when a hunt closes. Re-run the scan and reconcile at the top of any session
that works this arc.

---

## Ledger

Status: **OPEN** · **PARTIAL** (some crops resolved, hunt not finished) · **CLOSED-EDIT** (repointed
or corrected in canonical) · **CLOSED-RULING** (adjudicated CASE 2; cells still cite the bare host
by design, so the scan keeps counting them).

| # | region | source | dec. | status | note |
|---|---|---|---|---|---|
| 1 | `mid_south` | `uada_ext` | 20 | **PARTIAL** | Hunt 1 (2026-07-30) worked the **fruit** crops; the 2026-07-31 herb pass removed 10 false credits from **prose only** and deliberately did not repoint, so all 10 herb cells still cite the bare host. `lavender` has the one identified real target (its UAEX Plant of the Week URL) + a filed finding. |
| 2 | `mid_atlantic` | `ncsu_ext` | 13 | OPEN | `rosemary_mid_atlantic_ncsu_zone_attribution` already filed here. |
| 3 | `ca_interior` | `ucanr_ext` | 3 | **PARTIAL** | Repointed 8. Residue: `lemon` -> campaign D; both pears cite the **UC Home Orchard root**, not the veg table, and are filed `open` as CASE 1 repoint candidates for a fruit-tree read. |
| 4 | `ca_north_coast` | `ucanr_ext` | 3 | **PARTIAL** | Repointed 7; `okra` RULED. Residue: `lemon`, `lime` -> campaign D. |
| 5 | `ca_south_coast` | `ucanr_ext` | 2 | **PARTIAL** | Repointed 8. Residue: `lemon`, `lime` -> campaign D. |
| 6 | `ca_desert` | `ucanr_ext` | 7 | **PARTIAL** | Repointed 3; `okra` RULED; 4 cucurbits HELD on the accepted fall-cycle gap (Trevor ruled 2026-08-03: leave them). Residue: `lemon`, `lime` -> campaign D. |
| 7 | `warm_arid` | `nmsu_ext` | 9 | OPEN | See `right-document-wrong-claim`: NMSU CR457B has no planting-date window at all. |
| 8 | `warm_arid` | `tamu_agrilife` | 9 | OPEN | |
| 9 | `ca_interior` | `uc_mg` | 1 | **CLOSED-RULING** | Repointed 8; `arugula` ruled CASE 2 (no arugula row in Table 13.2). Hunt fully resolved. |
| 10 | `ca_north_coast` | `uc_mg` | 2 | **CLOSED-RULING** | Repointed 7; `edamame` ruled (only bean row is Phaseolus, not Glycine max) and `okra` ruled. Hunt fully resolved. |
| 11 | `ca_south_coast` | `uc_mg` | 1 | **CLOSED-RULING** | Repointed 8; `arugula` ruled. Hunt fully resolved. |
| 12 | `ca_desert` | `uc_mg` | 5 | **CLOSED-RULING** | Repointed 3; `okra` ruled; 4 cucurbits held by the accepted fall-cycle gap. Hunt fully resolved. |
| 13 | `rgv` | `tamu_agrilife` | 6 | OPEN | |
| 14 | `low_desert_az` | `uariz_ext` | 6 | OPEN | AZ1005's grid is 90°-rotated; see `right-document-wrong-claim`. |
| 15 | `ca_south_coast` | `ucr_citrus` | 3 | **CLOSED-RULING** | Withdrawn 2026-07-31 (kickoff 48 §4, commit `7092ca1`). Premise "Riverside is `ca_interior`" was false; 24/24 accession pages carry ripeness, **0/24** publish a bloom date. |
| 16 | `ca_north_coast` | `ucanr_marin_mg` | 3 | OPEN | |
| 17 | `warm_arid` | `nmsu_donaana_mg` | 2 | OPEN | |
| 18 | `fl_peninsula` | `ufifas_ext` | 2 | OPEN | |
| 19 | `ca_interior` | `ucr_citrus` | 2 | **CLOSED-RULING** | As #15. |
| 20 | `ca_north_coast` | `ucr_citrus` | 2 | **CLOSED-RULING** | As #15. |
| 21 | `ca_desert` | `uariz_ext` | 2 | OPEN | |
| 22 | `<crop-level>` | `ucr_citrus` | 2 | **CLOSED-RULING** | As #15. |
| 23 | `se_gulf` | `uga_ext` | 1 | OPEN | |
| 24 | `warm_arid` | `nmsu_chart` | 1 | OPEN | |
| 25 | `northern_tier` | `clemson_hgic` | 1 | OPEN | the "lemon tail" — #25-32 are all a single crop each |
| 26 | `northern_tier` | `tamu_agrilife` | 1 | OPEN | lemon |
| 27 | `se_gulf` | `tamu_agrilife` | 1 | OPEN | lemon |
| 28 | `se_gulf` | `clemson_hgic` | 1 | OPEN | lemon |
| 29 | `ca_interior` | `uc_ipm` | 1 | OPEN | lemon |
| 30 | `warm_arid` | `uariz_ext` | 1 | OPEN | lemon |
| 31 | `warm_arid` | `clemson_hgic` | 1 | OPEN | lemon |
| 32 | `low_desert_az` | `ucanr_ext` | 1 | OPEN | lime |

**Shape of what's left.** The eight California hunts (#3-6, #9-12) were 76 decisions and are now
**24** — campaign A's promote closed 52. What remains there is *not* more of the same work: 12 have
**no UC row at all** (the page is a vegetable table) and 12 are held by a contradiction, 8 of those
already ruled. The two largest live blocks are now #1 `mid_south`/`uada_ext` (20) and #2
`mid_atlantic`/`ncsu_ext` (13) — campaign B. Eight hunts (#25-32) are **one crop each and seven of
them are lemon**, so they are likely a single sitting once someone reads lemon's citations end to
end; campaign A's leftover `lemon`+`lime` decisions belong with them.

---

## The arc is FOUR campaigns, and kickoff 50 is only the first

**No single kickoff closes this arc.** The ledger is the arc-level tracker; kickoffs are per
campaign. The 28 genuinely-open hunts group naturally into four, by shared document family — which
is the unit that actually amortizes a hunt, since one document read serves N crops:

| campaign | hunts | decisions | what it is | status |
|---|---|---|---|---|
| **A. California / UC** | 8 (#3-6, #9-12) | **76 -> 9** | one planting-date table, four regions, two source ids | **CLOSED 2026-08-03** (`e65aa63a` + `3f6d6ce4`). 52 repointed, 16 ruled. 4 of 8 hunts fully resolved. Residue: `lemon`/`lime` 7 -> campaign D, 2 pears -> fruit-tree read |
| **B. Region templates** | 2 (#1, #2) | **33** | `mid_south`/`uada_ext` + `mid_atlantic`/`ncsu_ext` — the two find-and-replace parents | not written; both already carry filed findings naming the next move |
| **C. Arid + Texas** | 7 (#7, #8, #13, #14, #17, #21, #24) | **35** | NMSU + TAMU AgriLife + Arizona across `warm_arid`/`rgv`/`low_desert_az`/`ca_desert` | not written; AZ1005's rotated grid and NMSU CR457B's missing window are known traps |
| **D. The tail** | 11 (#16, #18, #23, #25-32) | **14** | one or two crops each; **7 of the 11 are lemon** | not written; likely one sitting |
| | **28** | **158 -> 106** | | |

**Suggested order: A, then B, then C, then D.** A is the biggest and the best-prepared (document
located, correctness question already down to 4 authoring decisions). B is next-cheapest per
decision because both hunts already have findings pointing at their specific next move. C is the
most research-heavy and has two documented traps. D is trivial per-hunt but has the most hunts, and
collapsing the lemon cluster first will make it collapse faster still.

Campaign A's repoint promote took the arc from 158 open to **106**. Its 24-decision residue is not
plain repoint work, so it is folded into D (`lemon`/`lime`) and into a small okra ruling rather than
re-run as a campaign. B next takes it to about 73.

---

## Campaign briefs — enough to start a session on any of them

**How to use these.** Point a session at this ledger and name a campaign. Each brief below is scoped
to be self-sufficient: it names the hunts, the source ids, what is already known, and the traps.

**Two things every campaign shares, so they are not restated per brief:**

1. **Protocol is `docs/kickoffs/50-uc-anr-california-citation-hunt.md` §6** — guarded promote,
   rebuilt fixtures, mutation-tested guards, the release gauntlet, the state trio, no plant-astro
   bump. It is written to be campaign-agnostic. Read it whichever campaign you are on.
2. **Counts are NOT restated in the briefs, deliberately.** Re-derive them from
   `citation_provenance_scan.py --decisions` at the top of the session and reconcile against the
   table above. Baked-in counts are what went stale in kickoffs 46-49.

---

### Campaign A — California / UC · hunts #3-6, #9-12 · `ucanr_ext`, `uc_mg`

**Has a full kickoff: `docs/kickoffs/50-uc-anr-california-citation-hunt.md`.** Start there, not here.

**COMPOSITION MEASURED 2026-08-03** (`docs/2026-08-03-campaign-a-count-reconciliation-and-readjudication.md`).
Size unchanged at 76; the internal split was not visible when it was priced as "one document, four
regions, two source ids":

| class | dec. | what it is |
|---|---|---|
| CASE 1 — clean repoint at the pathed UC table | **52** | every zone SUPPORTED or DIVERGENT; 8 crops × 4 regions × 2 ids, less the blocked |
| blocked by a contradicted cell | **12** | 8 on the *ruled* `ca_desert_fall_cycle_provenance_gap`, 4 on the two live okra decisions |
| **no UC row at all** | **12** | `lemon` 4, `lime` 3, `arugula` 2, `pear-asian`/`pear-european`/`edamame` 1 each |

**The 12 with no row are the `vce_426_331` shape inside campaign A** — the UC page is *Table 13.2, a
VEGETABLE table* (artichoke → watermelons), standing as sole source on citrus and tree fruit. Expect
CASE 2. `lemon`+`lime` (7 of the 12) overlap campaign D's lemon cluster and should be worked with it,
not twice.

**Only 2 authoring decisions are live, both okra** — kickoff 50 §3's other two shapes are already
closed (one by edit, one by ruling). See the kickoff's correction banner.

---

### Campaign B — the region templates · hunts #1, #2 · `uada_ext`, `ncsu_ext`

`mid_south`/`uada_ext` and `mid_atlantic`/`ncsu_ext`. **These two are the PARENTS of the
find-and-replace defect class** — `mid_south` was built from the `mid_atlantic` template, and both
the cherry-sweet fabrication (2026-07-30) and the ten herb credits (2026-07-31) were born that way.
Closing them has knock-on value beyond their 33 decisions.

**Already known, do not redo:**
- `mid_south` **already built a per-document citation vocabulary** in
  `docs/reviews/notes/2026-07-20/mid_south_sources.md` (`uada_ext_spring_veg`, `uada_ext_fall_veg`,
  `uada_ext_fsa6001`, `uada_ext_chill`, `uada_ext_fsa6105`) with a one-id-one-URL rule, and then
  left the FRUIT crops on the institution root. The vocabulary exists; it was not applied.
  **But that vocabulary is scoped to a CROP CLASS, not the region** — it is vegetables-only, and
  assuming it covers fruit or herbs would manufacture defects.
- Hunt 1 (2026-07-30, `docs/2026-07-30-mid-south-uada-ext-citation-hunt.md`) worked the fruit crops.
- The 2026-07-31 herb pass fixed **prose credits only** and deliberately did not repoint, so all 10
  herb cells still cite the bare host.
- **`lavender` has the one identified real repoint target in the whole hunt** — UAEX's English
  Lavender Plant of the Week — and a filed finding
  (`lavender_mid_south_uaex_zone_range_divergence`) stating exactly what must change with it: UAEX
  publishes zones 5 to 8, so the z8 "comfortably inside ... zone 5 to 9b" wording becomes false.
- `mid_atlantic` carries `rosemary_mid_atlantic_ncsu_zone_attribution`: NC State's Toolbox gives
  *Salvia rosmarinus* as 8a-10b while our prose says "zone 7 to 8". The number is sound (our own
  hardy-cultivar floor); the credit overstates.

**Trap:** `mid_atlantic`'s sourcing note names **zero URLs**, which is why it is harder than
`mid_south` despite being smaller. Also `vce_426_331` is catalogued blandly but is actually
Virginia's home garden **VEGETABLE** planting guide — already caught once as the sole source on 19
fruit nodes.

---

### Campaign C — arid + Texas · hunts #7, #8, #13, #14, #17, #21, #24

`nmsu_ext`, `tamu_agrilife`, `uariz_ext`, `nmsu_donaana_mg`, `nmsu_chart` across `warm_arid`, `rgv`,
`low_desert_az`, `ca_desert`. **The most research-heavy campaign** — five source ids, four regions,
no single governing document, and two documented traps that have already cost this arc real work:

- **AZ1005 (Arizona) has a 90°-ROTATED grid.** Read it as a normal table and every window is wrong.
- **NMSU CR457B has no planting-date window at all.** Locating the correct document is not the same
  as the document supporting the claim (`right-document-wrong-claim`).
- `tamu_agrilife` bare hosts have a history: `aggie-hort.tamu.edu` is a redirect loop and several
  paths 404. Check liveness before treating a repoint as available.
- `nmsu_chart`'s catalog URL is already a **pathed PDF**
  (`donaanamastergardeners.nmsu.edu/documents/foodgardenplantingchart-1.pdf`), so its single decision
  may be a mis-classification rather than a real bare host. Check that first — it is one row.

---

### Campaign D — the tail · hunts #16, #18, #23, #25-32

**INVERT THE UNIT HERE.** D is 11 hunts spanning 8 source ids, but **7 of the 11 are a single crop:
lemon** (`northern_tier`/`clemson_hgic`, `northern_tier`/`tamu_agrilife`, `se_gulf`/`tamu_agrilife`,
`se_gulf`/`clemson_hgic`, `ca_interior`/`uc_ipm`, `warm_arid`/`uariz_ext`, `warm_arid`/`clemson_hgic`).
Worked as 7 document hunts this is tedious; worked as **one crop-centric pass — "read lemon's
citations end to end" — it is likely a single sitting.** The (region, source) decision unit is the
right one for A, B and C and the wrong one for D.

The remaining four are genuinely independent singles: `ca_north_coast`/`ucanr_marin_mg` (3 crops:
edamame, pear-asian, pear-european), `fl_peninsula`/`ufifas_ext` (bell-pepper, jalapeno),
`se_gulf`/`uga_ext` (jalapeno), `low_desert_az`/`ucanr_ext` (lime).

**Do D last**, but note it is the cheapest per hunt — it is where the hunt count drops fastest, from
11 to about 5 real units.

#### WHERE TO LOOK — candidate documents already in the data

Measured 2026-08-03 by walking every `anchoring_urls` entry in the dataset. **These are LEADS, not
answers.** The standing caveat governs: *a pathed URL cited for another crop does not support THIS
claim* — it tells you which document to open, not what it says. Verify each against the specific
claim, and read from raw bytes.

**The two strongest — a citrus document is ALREADY cited for lemon elsewhere in the data:**

| hunt | candidate | already cited for lemon? |
|---|---|---|
| `northern_tier`/`clemson_hgic`, `se_gulf`/`clemson_hgic`, `warm_arid`/`clemson_hgic` | `https://hgic.clemson.edu/cold-tolerance-in-citrus/` | **YES** — 3 crops incl. lemon |
| `northern_tier`/`tamu_agrilife`, `se_gulf`/`tamu_agrilife` | `https://aggie-horticulture.tamu.edu/fruit-nut/fact-sheets/citrus/` | **YES** — 5 crops incl. lemon |

That is 5 of the 7 lemon hunts pointing at just two documents. **Check TAMU liveness first**:
`aggie-hort.tamu.edu` is a known redirect loop with `aggie-horticulture.tamu.edu`, and at least one
`aggie-horticulture` path 404s. Confirm this one resolves before treating it as available.

**The other two lemon hunts have NO lemon-specific pathed URL in the data — expect CASE 2:**

- `warm_arid`/`uariz_ext` — Arizona's dominant pathed doc is **AZ1005, a VEGETABLE planting
  calendar** (13 crops). It almost certainly does not cover lemon. If no citrus document turns up,
  this is an unsourced claim, not a repoint.
- `ca_interior`/`uc_ipm` — UC IPM's pathed URLs in our data are tomato, peppers, peas. UC IPM does
  publish citrus material, but **none of it is in our dataset**, so this is a real search rather
  than a lookup.

**The four singles:**

| hunt | crops | candidate already in the data | read before trusting |
|---|---|---|---|
| `fl_peninsula`/`ufifas_ext` | bell-pepper, jalapeno | `https://edis.ifas.ufl.edu/publication/VH021` (17 crops) — the Florida Vegetable Gardening Guide | strong fit; both crops are vegetables |
| `se_gulf`/`uga_ext` | jalapeno | `https://fieldreport.caes.uga.edu/publications/C943/vegetable-garden-calendar/` (13 crops) | strong fit; C943 is the UGA veg calendar |
| `ca_north_coast`/`ucanr_marin_mg` | edamame, pear-asian, pear-european | `https://ucanr.edu/sites/default/files/2025-03/PLANTING%20CALENDAR%20-%20VEG.pdf` | **fits edamame, NOT the pears** — a vegetable calendar cannot carry two tree fruits. Expect a split verdict: edamame CASE 1, pears CASE 2 or a different document |
| `low_desert_az`/`ucanr_ext` | lime | `https://ucanr.edu/program/uc-master-gardener-program/time-planting` (23 crops) | **geography mismatch — do not repoint here.** That is campaign A's CALIFORNIA table; this hunt is `low_desert_az`, which is Arizona. A UC California table cannot source an Arizona window. Likely CASE 2, or repoint to an Arizona source |

**The pattern worth carrying into D:** four of these eleven hunts pair a *tree fruit or citrus* claim
with a *vegetable* planting guide. That is the `vce_426_331` shape already caught once in this arc
(a Virginia home-garden VEGETABLE guide standing as sole source on 19 fruit nodes). Check what class
of crop the document actually covers before repointing anything.

---

## Standing cautions carried from the arc

- **`DIVERGENT` is not a defect class.** The UC planting-date table states its own dates are "only
  approximate"; 35 of the 92 adjudicated California windows fall inside that tolerance.
- **A pathed URL for another crop does not support THIS claim.** Every bare-host id already cites
  real pathed documents elsewhere — that makes the *hunt* cheap, not the *answer* free. Never
  mass-repoint.
- **`SUIT` (74) and `TYPE` (11)** in the contradiction scan are low value: one zone rated
  differently across regions is the region model working as designed.
- A hunt closed by ruling **still shows in the scan**. That is correct behavior, not a bug — record
  it here instead of trying to make the number go down.
