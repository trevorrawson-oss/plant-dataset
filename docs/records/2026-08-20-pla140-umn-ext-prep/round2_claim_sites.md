# PLA-140 prep round 2 -- the claim sites, with claim text

**Read-only. Canonical `be8a6d1e`. Nothing changed, no URL fetched, no document read.**
Liveness deliberately out of scope (PLA-140 item 6).

---

## Set A -- the 12 live anchors asserting a dead page

These are the only sites where `anchoring_urls.umn_ext.url` **is** the 404 landing page.
All 12 carry `verified: 2026-06-29`.

### edamame -- 7 sites

**Cert log NAMES the documents** (`verification_log_ref`):

> "All soybean/edamame biology re-derived from live T1 extension sources (MU Extension
> edamame, Iowa State All About Beans + soybean diseases, **UMN growing beans + soybean
> pest management**, Virginia Tech/VCE SPES-455 edamame, Rutgers edamame)."

**And the crop already anchors both of them elsewhere in its own record:**

| placements | URL |
| -- | -- |
| 6x | `https://extension.umn.edu/soybean/soybean-pest-management` |
| 1x | `https://extension.umn.edu/vegetables/growing-beans` |
| 7x | `https://extension.umn.edu/vegetables` **(the dead page -- these 7 sites)** |

| # | field path | claim |
| -- | -- | -- |
| 1 | `tips_by_stage.harvest[0]` | `edamame_harvest_whole_plant` -- harvest whole plant at once, ripens together, cook or freeze same day, must be cooked never raw |
| 2 | `regions.northern_tier.resolved_by_zone.3` | plant_out May 25 - Jun 15; harvest Aug 20 - Sep 15 |
| 3 | `regions.northern_tier.resolved_by_zone.4` | plant_out May 10 - Jun 20; harvest Aug 10 - Sep 25 |
| 4 | `regions.northern_tier.resolved_by_zone.5` | plant_out May 1 - Jun 25; harvest Aug 1 - Sep 30 |
| 5 | `regions.northern_tier.resolved_by_zone.6` | plant_out Apr 25 - Jun 30; harvest Jul 20 - Oct 10 |
| 6 | `regions.mid_atlantic.resolved_by_zone.7` | plant_out Apr 25 - Jun 20; harvest Jul 19 - Sep 13 |
| 7 | `regions.mid_atlantic.resolved_by_zone.8` | plant_out Apr 15 - Jun 15; harvest Jul 9 - Sep 8 |

**None of the 7 is sole-source.** Every calendar row co-cites `iastate_ext` plus one of
`umaine_ext` / `unh_ext` / `msu_ext`. Sites 6 and 7 additionally carry a `notes` field
stating "No belt-specific Mid-Atlantic extension source was found for edamame."

**TAXON FLAG, for your read, not adjudicated here.** Edamame is *Glycine max*. UMN's
"growing beans" page is the one shared by `broad-beans-fava`, `dry-bean`,
`green-beans-bush` and `pole-beans` -- i.e. almost certainly *Phaseolus*. The cert log
names it for edamame anyway. Which of the two named documents carries a **planting-window**
claim for soybean is exactly the question a common-name match would get wrong.

### okra -- 5 sites

**Cert log contains NO UMN mention of any kind.** The crop anchors **no** UMN URL other
than the dead page.

| # | field path | claim |
| -- | -- | -- |
| 1 | `regions.northern_tier.plantings[0]` | offset rule set: start_indoors last_frost -28d/14d; plant_out last_frost +14d/35d; harvest_start last_frost +70d; harvest_end first_frost -3d |
| 2 | `regions.northern_tier.resolved_by_zone.3` | start_indoors May 1 - May 15; plant_out Jun 1 - Jun 15; harvest Aug 1 - Sep 10 |
| 3 | `regions.northern_tier.resolved_by_zone.4` | start_indoors Apr 24 - May 8; plant_out May 25 - Jun 10; harvest Aug 1 - Sep 25 |
| 4 | `regions.northern_tier.resolved_by_zone.5` | plant_out May 20 - Jun 10; harvest Jul 25 - Oct 10 |
| 5 | `regions.northern_tier.resolved_by_zone.6` | plant_out May 10 - Jun 15; harvest Jul 15 - Oct 25 |

All 4 zone rows co-cite `iastate_ext`. Site 1 has no co-cite recorded at the plantings
level.

**Nothing in okra's record names a UMN document.** PLA-5 cannot resolve these from the
cert log; there is no named document to point at. Worth deciding before any read: whether
UMN Extension publishes okra guidance at all, given okra is not a Minnesota crop and every
one of these sites is a **northern_tier zone 3-6** window.

---

## Set B -- the claim-bearing unanchored rows

**Correction to round 1's estimate: it is 32 rows, not ~40, and 28 after one more roster
class comes out.** `zones.<N>.sources` (4 rows: zones 3, 4, 5, 6) is the zone-level
analogue of the `regions.*.sources` rosters already excluded -- an attribution list, not a
claim. Those 4 are listed at the bottom.

**All 28 are `lettuce-leaf`.** No other crop has a claim-bearing unanchored `umn_ext`
citation.

They are **offset rules, not literal dates**, and collapse to **7 distinct claim shapes**:

| claim shape | zones | rows | umn_ext SOLE source | co-cites |
| -- | -- | -- | -- | -- |
| `harvest_end` [primary] = `bolt_threshold_start` **-5d** | 3,4,5,6,7,8,9,10 | 8 | **5** | `uga_calendar` on 3 |
| `harvest_start` [primary] = `direct_sow_start` **+45d** | 3,4,5,6,7 | 5 | 0 | `umd_ext` |
| `harvest_end` [secondary] = `first_frost` **-5d** | 3,4,5,6,7 | 5 | 0 | `cornell_ext`, `iastate_ext` |
| `direct_sow` [secondary] = `first_frost` **-90d**, window 21d | 4,5,6,7 | 4 | **4** | none |
| `harvest_end` [secondary] = `bolt_threshold_start` **-5d** | 8,9,10 | 3 | **3** | none |
| `harvest_start` [secondary] = `direct_sow_start` **+45d** | 8,9 | 2 | 0 | `umd_ext` |
| `direct_sow` [secondary] = `first_frost` **-76d**, window 21d | 3 | 1 | 0 | `ndsu_ext` |

**12 of the 28 rows have `umn_ext` as the ONLY source.** Those are the load-bearing ones,
and they are just **3 claim shapes**: the bolt-threshold harvest_end rule, the
fall-sowing `first_frost -90d` rule, and the zone 8-10 secondary bolt rule.

**lettuce-leaf's cert log contains no UMN mention.** But the crop already anchors six UMN
documents:

| placements | URL |
| -- | -- |
| 34x | `/vegetables/growing-lettuce-endive-and-radicchio` |
| 7x | `/planting-and-growing-guides/planting-vegetables-midsummer-fall-harvest` |
| 3x | `/planting-and-growing-guides/companion-planting-home-gardens` |
| 1x | `/planting-and-growing-guides/harvesting-and-storing-home-garden-vegetables` |
| 1x | `/commercial-fruit-growing-guides/postharvest-handling-fruit-and-vegetable-crops-minnesota` |
| 1x | `/yard-and-garden-news/growing-cool-season-vegetables-minnesota` |

**A LEAD, NOT A VERDICT.** The 4 sole-source `direct_sow [secondary] = first_frost -90d`
rows are fall-succession sowing windows, and this crop already anchors UMN's
*"Planting vegetables for midsummer and fall harvest"* 7 times. Topically adjacent is not
the same as carrying the claim: whether that page states a 90-day-before-frost fall sowing
rule for leaf lettuce is a read, and a sibling's pathed document is a discovery that splits
by claim, not a repoint.

### The 4 excluded zone-level rosters

| path | co-cited |
| -- | -- |
| `zones.3.sources` | ndsu_ext, msu_ext, msu_bozeman, umaine_ext |
| `zones.4.sources` | iastate_ext, msu_ext, umaine_ext, psu_ext |
| `zones.5.sources` | iastate_ext, psu_ext, uwi_hort, msu_ext |
| `zones.6.sources` | umd_ext, vce_426_331, cornell_ext, psu_ext |

---

## What the read actually is

| | sites | distinct claims to read |
| -- | -- | -- |
| edamame | 7 | 2 documents already named and already anchored; 1 taxon question |
| okra | 5 | no document named anywhere; existence question first |
| lettuce-leaf | 28 | **7 claim shapes, of which 3 are sole-source** |

Not 40 claim sites. **Twelve distinct claims**, across three crops.
