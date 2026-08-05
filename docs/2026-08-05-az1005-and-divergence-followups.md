# AZ1005, the divergence scan, and lavender — the three campaign C follow-ups

**Session:** 2026-08-05 (second pass). **Issue:** PLA-113 residue. **Promote:** `754c51a0` -> `ca40d90f`.
**Prior doc:** `2026-08-05-campaign-c-reprice-and-arid-document-read.md`.
20 nodes repoint, 3 stay bare on purpose, 6 findings filed, no catalog id minted.

All three items were left open by the campaign C closeout with a recommendation each. **Two of the
three recommendations turned out to be wrong once the documents were actually read**, which is the
point of reading them.

---

## 1. AZ1005 — the melons were a repoint, not an absence

The closeout deliberately filed **no** absence finding for cantaloupe, honeydew-melon and
watermelon, on the grounds that AZ1005 was a live lead rather than a measured absence. Reading it
vindicates that twice over: it **has** both melon rows, so an absence finding would have been
false — and it does **not** support every window we publish, so a blanket repoint would have been
false too.

### Reading a rotated grid without guessing

AZ1005's text layer gives crop names and month headers and **no dates**, the same shape as the
Doña Ana chart. The windows were reconstructed from **character coordinates**: month labels share
an x and vary in y, so months run down the page and crops across it — the 90° rotation, confirmed
mechanically rather than assumed.

**The method was validated against a control before any melon was touched.** Pumpkin reads
`Mar 1, Mar 15` then `Jul 1, Jul 15, Aug 1` off the grid; our pumpkin cell says `plant_out
Mar 1 - Mar 15` with a second planting `Jul 1 - Jul 31`. It reproduces a value we already hold, so
the reading is trustworthy.

| AZ1005 row | markers | |
|---|---|---|
| Melons, Cantaloupe/Honeydews, etc. | S at Feb 15 through Jul 15, continuous | 90-120 days |
| Melons, Watermelon | **S at Feb 15, Mar 1, Mar 15 — and nothing else all year** | 90-120 days |

### What that means per crop, and it is not one verdict

- **honeydew** opens Feb 15; the document opens Feb 15. Clean. All 5 nodes repoint. Recorded
  separately: honeydew has **no row of its own** — it rides the combined cantaloupe row, so the
  document cannot distinguish the two crops' timing and does not independently confirm that
  honeydew should open later than cantaloupe.
- **cantaloupe** opens **Feb 1**, a fortnight ahead of the document's first mark, and its second
  planting runs to Aug 15 where the document stops at Jul 15. Repointed, divergence filed `open`.
- **watermelon** opens Feb 1, and its **Jul 15 - Aug 15 second planting has no support at all**.
  Its 3 spring nodes repoint; its **2 second_planting nodes stay bare** with a filed reason.

The asymmetry is evidence, not a gap: the same table gives cantaloupe and honeydew a continuous
five-month window and gives watermelon six weeks, which is a real horticultural claim about a
longer-season crop in a hot desert.

Neither early opening is called an error — Maricopa County is one part of a larger region, and a
fortnight at the front of a direct-sown cucurbit window is where soil temperature rather than the
calendar governs. Both are **unsourced**, and the early end is the one that costs a reader a
planting, since seed into cold February soil rots. Compare each crop's `uscrn_validation` record
before ruling.

---

## 2. The divergence scan — ship narrow, and record why

`tools/catalog_divergence_scan.py` ships at the one definition that does not flood: **the node
cites a domain ROOT while that source id's catalog entry already names a DOCUMENT**. Eight nodes,
two ids. `bare_host_scan` cannot see this class because it never consults `source_catalog`;
`url_health_gate` cannot because every one of them returns HTTP 200.

**Four wider definitions were measured on 2026-08-05 and all flood.** They are recorded in the
tool's docstring and pinned by a test, so the next reader does not see eight rows, assume the scan
is timid, and rediscover the flood:

| definition | result |
|---|---|
| node host != catalog host | 729 nodes — `cameron.agrilife.org`, `aggie-horticulture.tamu.edu`, `fieldreport.caes.uga.edu`, `ask.ifas.ufl.edu`, `nevegetable.org` are all legitimate |
| one id carrying several documents, some off-host | 47 ids; `ncsu_ext` alone spans 83 urls, 51 off-host, essentially all correct |
| catalog names a pathed document, node cites another | floods — the ASPCA toxic-plant index with per-plant pages beneath it is correct |
| ...also excluding descendants and same-host pages | still floods — "pathed" is not "specific document"; `msu_bozeman`'s catalog url is `montana.edu/extension/` |

### The turnip fix, and the trap inside it

Turnip's 7 `ca_south_coast` nodes cited the San Diego Master Gardeners **bare root** while eight
sibling crops cited per-crop pages on that same host. **The obvious target was wrong**: `/turnips/`,
plural to match `/beets/`, returns **HTTP 404**. The real page is `/turnip/`, singular. Pattern-
matching a sibling's url shape would have installed a dead link — the sibling-precedent trap in its
cheapest possible form.

What the page actually says is **wider** than what we publish: "Seeds can be planted from September
to May" coastal, "September to April" inland, against our `Sep - Oct`. Our window is a conservative
subset, so nothing is wrong and no date changed, but a reader is being shown a shorter season than
the cited source describes. Filed for a content pass.

**edamame's one node stays bare.** No Cornell edamame *variety* document exists: the gardener-facing
Vegetable Varieties database requires authentication, the only Cornell edamame publication is a 2014
Expo proceedings PDF, and the CALS soybean varieties page is **agronomic soybean by maturity group**,
a different use of the same species. The five cultivars are corroborated by the node's other two
sources.

**A registrable-domain match is the wrong institution test**, discovered when the promote's first
guard rejected the turnip repoint. `ucanr_san_diego_mg`'s catalog url is on `ucanr.edu`; the county
association runs `mastergardenersd.org`. County MG programs routinely run a separate `.org`
alongside their university program page. The guard now requires the host to be **already vouched
for by other crops** under that exact id — looser on domain, stricter in substance.

---

## 3. Lavender — not a relabel, an unsourced window

Queued as cosmetic: an id pointing at the wrong document. Reading all three of its NMSU sources
shows something else. **None of them publishes a lavender planting date.**

| source | what it actually is | planting date? |
|---|---|---|
| NMSU Guide H-221, *Spices and Herbs for the Home Garden* | herb growing guide | **no** — only seed-germination guidance (3 days moist refrigerated, 30 days at 65°F+) |
| NMSU RR-770 | *Lavender Cultivar Trial Results for **North-Central** New Mexico, 2003-2005* | **no** — its only date is when the trial plot was established (June 24, 2002), and the geography is the wrong half of the state |
| NMSU low-water plants, herbaceous list | xeric landscape plant list | **no** — right taxon (*Lavandula angustifolia*), gives water need, height and sun; no planting time, no zone |

So `warm_arid` z8's `plant_out: "Apr - May or Sep - Oct"` is modeled and says so nowhere. Two of the
three citations are **also mislabelled** — the low-water list under `nmsu_chart` (whose catalog
entry is the Doña Ana Food Garden Planting Chart) and RR-770 under `nmsu_donaana_mg` (whose entry
is the Doña Ana MG site) — which is how this stayed invisible.

**No scan in the repo could reach it.** The node is neither bare nor sole, so `bare_host_scan` and
`catalog_divergence_scan` both pass it, and every mechanical widening of the divergence check
floods. Filed `open` at medium; no repoint is possible and none was invented.

---

## Verification

`whole_crop_gate` PASS on all 6 touched crops, `gate_all` **121/121**, `release_verify` "no new
violations" with `catalog +none -none` on every crop, 40 standalone gates byte-identical, COMPACT
preserved.

**12 guards, every one mutation-tested, and three were vacuous on the first sweep** — all three
the same shape, a check whose expected value came from the thing it validated:

1. `AZ1005_URL` was read from the catalog and then compared to the catalog. Now a pinned constant,
   asserted in both directions.
2. The turnip host-vouching set was computed over the whole pre-state, so turnip's own seven bare
   citations put `mastergardenersd.org` in the set and the check could never fail. Now computed
   from **other crops only**.
3. A test stripped turnip's own citation and tripped `PREFLIGHT 1` instead of the guard it named —
   caught only because the test asserts the specific abort message.

That is three in one promote, after two in the previous one. The pattern is consistent enough to be
worth stating plainly: **when a guard's expected value is computed rather than written down, assume
it is vacuous until a mutation proves otherwise.**
