# PLA-140 prep -- what the dataset already knows about `umn_ext`

**Prep only. Nothing was changed, no URL was guessed, no document was read, no URL was
fetched.** Canonical `be8a6d1e`, read-only. Everything below is measured from
`crops_data_final.json` as it stands.

Companion machine-readable files in this directory:

| file | rows | what it holds |
| -- | -- | -- |
| `citations_umn_ext.json` | 2,676 | every citation site, full field path, co-cited sources, per-field anchor URL + its `verified` date |
| `umn_deep_link_register.json` | 101 | every distinct `umn.edu` deep link already anchored, with crops, claim families, verified-date range |
| `cert_log_umn_mentions.json` | 57 | every cert-log entry mentioning UMN, split into sentences |

---

## 0. Read this first -- the shape is not what the ticket assumes

**`source_catalog['umn_ext'].url` is not what anchors claims.** The dataset carries a
second, per-field mechanism: `<container>.anchoring_urls.umn_ext.url`, each with its own
`verified` date. **2,239 of the 2,676 citation sites already carry a working-looking,
separately-dated deep link at the point of claim.** The catalog URL is a
publisher-level fallback, not the anchor of record.

The catalog's own sibling entry says so out loud. `umn_ext_apple_scab.citable_for` ends:
**"Parent portal entry: umn_ext."** Three document-scoped children already exist
(`umn_ext_broccoli`, `umn_ext_edible_flowers`, `umn_ext_apple_scab`), all with live-looking
deep links, all minted against the same parent.

**Beware the substring.** `umn_ext` is a prefix of three other catalog ids. A substring
match returns 2,929 hits across all 128 crops; exact matching returns 2,810 string
occurrences and 2,676 citation sites across 120 crops. Every number in this document is
exact-match.

### Where the 404 URL actually appears: 58 occurrences

| count | path | what it is |
| -- | -- | -- |
| 45 | `sources_summary.primary[].url` / `sources_summary[].url` | per-crop MIRRORS of the catalog row, across 47 crops |
| 12 | `...anchoring_urls.umn_ext.url` | genuine claim anchors pointing at the dead page -- **edamame (7), okra (5)** |
| 1 | `source_catalog.umn_ext.url` | the catalog row itself |

The 45 mirrors mean a catalog edit alone does **not** clear the dataset: 47 crops carry a
stale copy of the URL that a catalog fix will not reach. That is a second, mechanical
edit, and it is the part most likely to be forgotten.

---

## 1. Which crops cite `umn_ext`, and on which claims

**120 crops. 2,676 citation sites. 166+ distinct field families.**

Full per-citation detail with complete field paths is in `citations_umn_ext.json`. Summary
of the split that matters:

| | sites | meaning |
| -- | -- | -- |
| anchored to a per-field deep link | **2,239** | claim already has its own dated URL; catalog URL is not load-bearing here |
| **no per-field anchor** | **437** | claim falls back to the catalog URL -- these are what the 404 actually breaks |
| of those, anchored AT the dead page | 12 | edamame + okra, `verified=2026-06-29` |

**The 437 unanchored sites are mostly rosters, not claims.** By family:

| count | family | claim-bearing? |
| -- | -- | -- |
| 147 | `verification_status.field_additions[].sources` | no -- records which sources fed a column pass |
| 85 | `verification_status.source_set` | no -- the crop's source roster |
| 80 | `regions.northern_tier.sources` | region-level roster |
| 15 | `regions.mid_atlantic.sources` | region-level roster |
| ~34 | `regions.<other>.sources` (9 regions) | region-level roster |
| 33 | `...uscrn_validation.zone_citations` | soil-temp validation citations |
| ~40 | `zones.<N>...plantings[].harvest_end/harvest_start/direct_sow[].sources` | **yes -- calendar claims** |

Crops with the largest unanchored counts: **lettuce-leaf 41, bok-choy 23, spring-onion 14,
parsley 14, chives 14**, then a long tail at 7 or fewer. Every one of the 120 crops has at
least one unanchored site.

Crops by total citation volume (top 10): bok-choy 123, chives 90, lettuce-leaf 88,
spring-onion 81, grape-tomato 73, roma-tomato 72, cherry-tomato 71, heirloom-tomato 71,
sunflower 71, radish 69.

---

## 2. Cert logs -- PLA-5's rule, applied

**57 of the 120 crops mention UMN in `verification_status.verification_log_ref` (or
`verification_log`). 17 name a specific document or record a URL repair. 63 crops cite
`umn_ext` with no UMN mention in their cert log at all.**

Full sentences per crop in `cert_log_umn_mentions.json`. The entries that bear on the
decision:

### 2a. The defect was already observed, on `umn_ext` specifically

> **microgreens-mix** -- "3/4 cited URLs fetched + own-voice clean (...), **`umn_ext` not
> fetchable (landing page -> external Google Doc)** with its facts corroborated by
> `usu_ext`/`psu_microgreens`"

A cert pass already found this exact entry unusable, named the reason (landing page
delegating to an external Google Doc), and worked around it by corroboration. That is a
prior, dated, in-dataset observation of the thing PLA-140 is about to fix.

### 2b. Cert logs that NAME a specific UMN document

These are PLA-5 candidates -- the log already identifies the document, so the claim may
need no new read:

| crop | document named in the cert log |
| -- | -- |
| parsley | "UMN Growing Parsley" |
| eggplant | "UMN Growing eggplant (start ~8 wk before...)" |
| cucumber | "UMN Growing cucumbers (pH 6.0-6.5, soil >=70F, 1 in/week...)" |
| snow-peas | "UMN Growing peas" |
| butternut-squash | "UMN Growing pumpkins and winter squash" |
| collards | "UMN growing-collards-and-kale" |
| edamame | "UMN growing beans + soybean pest management" |
| turnip | "UMN turnip/rutabaga guides", "UMN flea-beetle/root-maggot pages", "UMN/WVU companion guides" |
| nasturtium | "UMN Extension nasturtiums article + UMN Extension edible flowers" |
| beet | "UMN for the companion-evidence stance" |
| broccoli | heading ceiling 86F day / 77F night "(UMN EXACT)" |
| zucchini-courgette | pH 6.0-6.5, succession interval, spacing "(UMN EXACT)" |
| leek, cauliflower, cabbage, brussels-sprouts, kale, swiss-chard | "UMN" named among live T1 sources for core biology, document not individually titled |

**Each names a DIFFERENT document.** No single URL satisfies them.

### 2c. A UMN URL-liveness sweep has happened before, at claim level

| crop | recorded repair |
| -- | -- |
| slicing-cucumber | "swapped 2 dead UMN URLs to confirmed-live pages (.../striped-cucumber-beetles -> .../cucumber-beetles; ...)" |
| pickling-cucumber | "swapped the dead UMN URL on Bacterial-wilt (.../diseases/bacterial-wilt-cucurbits -> .../disease-management/bacterial-wilt)" |
| yellow-summer-squash, acorn-squash, spaghetti-squash, cantaloupe, honeydew-melon | "2 dead UMN URLs re-pointed live (bacterial-wilt, cucumber-beetle)" |

Those same five also carry: **"honeydew 404 UMN log URL) flagged for the post-123
URL-liveness sweep"** -- an explicitly deferred item that appears never to have been run.

---

## 3. Working `extension.umn.edu` deep links already anchored

**101 distinct `umn.edu` deep links, across 2,368 anchor placements, every one carrying a
`verified` date between 2026-05-14 and 2026-08-10.** Full register with crops and claim
families in `umn_deep_link_register.json`.

**Liveness caveat, stated plainly: I did not fetch any of these.** "Working" here means the
dataset asserts a verification date, not that I re-checked. Per the repo's own standing
lesson, a 403 is not dead and a 200 is not alive, and these dates are up to three months
old.

Highest-traffic anchors:

| placements | URL | crops | claim families it anchors |
| -- | -- | -- | -- |
| 317 | `/vegetables/growing-tomatoes` | 6 tomato/tomatillo | soil, ph, watering, fertilizer, pests, diseases, tips, calendar |
| 117 | `/vegetables/growing-beans` | 5 legumes | soil, ph, calendar, pests |
| 93 | `/vegetables/growing-chinese-cabbage-and-bok-choy` | bok-choy | broad |
| 86 | `/vegetables/pumpkins-and-winter-squash` | 4 winter squash | broad |
| 80 | `/vegetables/growing-cucumbers` | 4 cucumbers | broad |
| 77 | `/vegetables/growing-sweet-corn` | 4 corns | broad |
| 74 | `/vegetables/growing-peas` | 2 peas | broad |
| 73 | `/vegetables/growing-chives` | chives | broad |
| 70 | `/flowers/sunflowers` | sunflower | broad |
| 67 | `/vegetables/growing-scallions-home-gardens` | spring-onion | broad |
| 66 | `/flowers/marigolds` | marigold | broad |
| 63 | `/vegetables/growing-peppers` | 5 peppers | broad |

The register also covers non-`/vegetables` trees already in use: `/fruit/...`,
`/flowers/...`, `/plant-diseases/...`, `/yard-and-garden-insects/...`,
`/disease-management/...`, `/planting-and-growing-guides/...`, `/soil-and-water/...`,
`/yard-and-garden-news/...`, plus `apps.extension.umn.edu/garden/diagnose/...` and
`mnhardy.umn.edu`.

**The institution is demonstrably alive across at least 9 distinct site trees.** Whatever
`/vegetables` used to be, the crops moved on without it.

---

## What this prep does NOT settle -- yours to decide

1. **Whether `umn_ext` should be a document at all.** It is cited by 120 crops across every
   claim family, its cert logs name a different document per crop, and its own child entry
   calls it a "Parent portal entry." A single replacement URL cannot carry those claims.
   The shapes available are: repoint the portal to a live portal, or demote the parent and
   mint document-scoped children the way the three existing siblings were minted.
2. **The 45 `sources_summary` mirrors.** A catalog edit does not reach them.
3. **The 12 real anchors on the dead page** (edamame, okra) need documents, not a portal.
4. **Liveness of the 101 anchored deep links.** Asserted by date, not re-checked here.

---

## Records note (2026-10-03, housekeeping session, kickoff 60 ruling 1)

This README and `round2_claim_sites.md` were the only copies of this prep; they sat untracked in
`tools/staging/pla140_umn_ext_prep/` and were committed here byte-identical (this section is the only
addition). **The three companion JSONs are NOT committed.** They are derived, and they rebuild
byte-identical from git with the script beside this file:

```
python3 docs/records/2026-08-20-pla140-umn-ext-prep/rebuild.py <outdir>     # from the repo root
```

It reads `git show 8118eaa:crops_data_final.json` (canonical `be8a6d1e`, the base this prep measured;
the script refuses any other prefix) and writes the three files. Verified 2026-10-03, rc 0, 0.4 s:

| file | sha256 (original == rebuild) |
| -- | -- |
| `citations_umn_ext.json` | `0f305220fc3a17ebd8da552e3ee92c362d3841d6d4bb226bb800e8c26865d620` |
| `umn_deep_link_register.json` | `f4f2daab443a6bf412c5478093fe9b6481806a863213081545d154255afa1030` |
| `cert_log_umn_mentions.json` | `35bd29149f9d2e2a19f730cf193699b2cf2b0581ba9015c07d9f64ebabd1f299` |

**One caveat.** No extraction script was saved in August, so `rebuild.py` was written in October and fitted
to the files. Its `names_document_or_repair` rule (`dead|404|URL|fetchable|[Gg]rowing `, any sentence) is a
keyword regex FITTED to the 57 existing labels (17 True / 40 False, 0 mismatches), not the original rule.
Byte identity proves it fits this data, not that it is the August logic. The labels look keyword-driven
anyway: leek and sunflower are True on incidental "growing" wording, and collards, nasturtium, turnip and
beet are False though section 2b above lists them as naming a document. Read the column as a keyword
count, not a reviewed judgment.

Also measured by the rebuild: `umn_deep_link_register.json` counts only dicts keyed exactly
`anchoring_urls` (not the crop-root `<field>_anchoring_urls` siblings), so its placement counts are
narrower than some figures in the body above (e.g. `growing-tomatoes`: 317 placements in the body's
table, 294 in the JSON).

**Status at commit:** PLA-140 is marked Done in Linear (2026-09-06, no close-out comment), yet canonical
`b331e5f2` still carries `source_catalog.umn_ext.url = https://extension.umn.edu/vegetables` and the dead
string occurs **58** times, the count measured above.
