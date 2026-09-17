# PLA-465 plant dimensions, promote 1 -- PREPARED AND HELD

**Date:** 2026-09-16. **Base:** canonical `a98b6cfd` (HEAD `3da13c2`, origin/main). **Post-state:** `a7f234ce449c6d74b4f1be2398bb808cfe29bebf9a1f7cc51efdcaea56246c93`, written to a scratch file for the gauntlet, never to the canonical. **Apply on approval:** `python3 tools/promote_pla465_plant_dimensions.py --expect-sha a7f234ce449c6d74b4f1be2398bb808cfe29bebf9a1f7cc51efdcaea56246c93`. Spec: `docs/superpowers/specs/2026-09-16-pla465-plant-dimensions-field-shape.md` (approved, commit `2ffead3`).

## What the promote does

Three crop-level keys on every one of the 121 certified crops: `mature_height_ft`, `mature_spread_ft`, `footprint_inches`. **16 crops are authored** from T1 reads made today from raw bytes and confirmed by an independent adversarial review; **105 certified crops take null on all three** (not yet authored, R1 as changed: define for 121, author the woody); `footprint_inches` is null on every crop (PLA-429's slot); the 7 shells are byte-identical. Each authored crop appends one `verification_status.field_additions[]` entry `{field: "plant_dimensions", date, sources, note}` whose note carries the institution, URL, read date, byte count, sha256 and the verbatim sentence, so every figure can be re-verified from raw bytes. Independent leaf walk: 457 leaves added, 0 removed, 0 changed, on exactly the 121 certified crops; the 7 shells untouched; top-level keys identical.

| crop | height ft | spread ft | page (source id) | basis |
| -- | -- | -- | -- | -- |
| apple | 10 to 14 | null | WSU EB0937 Fruit Handbook for Western Washington, "M 26: Semi-dwarf habit, 10'-14' tall" (`wsu_ext`) | recommended rootstock M26 |
| blueberry | 5 to 8 | 5 to 8 | PSU "Blueberries in the Garden and the Kitchen", highbush "5 to 8 feet tall and wide" (`psu_ext`) | own root, highbush |
| elderberry | 5 to 12 | 6 to 12 | NC State Plant Toolbox Sambucus canadensis (`ncsu_ext`) | species |
| fig | 15 to 30 | 15 to 30 | Clemson HGIC 1353, "15 - 30 ft tall and wide" (`clemson_hgic`) | own root |
| lavender | 1 to 2 | 2 to 3 | NC State Plant Toolbox Lavandula angustifolia (`ncsu_ext_lavandula_angustifolia`) | species |
| lemon | 10 to 20 | null | UF/IFAS HS402, the crop's own anchor, "Trees may reach 10-20 ft" (`uf_ifas_hs1153`) | species |
| mulberry | 30 to 60 | 30 to 50 | NC State Plant Toolbox Morus alba (`ncsu_ext`) | species on Morus seedling |
| nectarine | 15 to 25 | 15 to 25 | NC State Plant Toolbox Prunus persica, which lists Nectarine as a common name (`ncsu_ext`) | species |
| oregano | 1 to 3 | 1 to 2 | NC State Plant Toolbox Origanum vulgare (`ncsu_ext`) | species |
| pawpaw | 15 to 30 | 15 to 30 | NC State Plant Toolbox Asimina triloba (`ncsu_ext`) | species on pawpaw seedling |
| peach | 15 to 25 | 15 to 25 | NC State Plant Toolbox Prunus persica (`ncsu_ext`) | species |
| persimmon | 20 to 30 | 15 to 25 | NC State Plant Toolbox Diospyros kaki, already cited (`ncsu_ext`) | species |
| pomegranate | 10 to 12 | 8 to 10 | NC State Plant Toolbox Punica granatum (`ncsu_ext_toolbox_punica_granatum`) | own root |
| rosemary | 4 to 5 | 3 to 4 | NC State Plant Toolbox Salvia rosmarinus (`ncsu_ext`) | species, upright form |
| sage | 1 to 2 | 2 to 3 | NC State Plant Toolbox Salvia officinalis (`ncsu_ext`) | species |
| thyme | 0.5 to 1 | 0.5 to 1.3333 | NC State Plant Toolbox Thymus vulgaris, "6 to 12 inches high and 6 to 16 inches wide" (`ncsu_ext`) | species; 16 in recorded as 1.3333 ft, the convention below |

**The staging moved once, before the gauntleted run, and the record says so.** The first staging carried 18 crops: the 15 the readers marked "found" plus four partials the orchestrator read as on-basis (apricot, cherry-sour, lemon, plum; cherry-sour then fell out because its only page is Virginia Tech, which the catalog does not admit). The adversarial review struck two of the remaining three partials: apricot, whose page contradicts itself on the lower bound, and plum, whose note was self-contradictory and whose Japanese-plum basis rests on list order. `EXPECTED_AUTHORED` moved 18 to 16 in the promote and the suite together, before the run that produced `a7f234ce`; the first staging's SHA `3c5e8b9a` never went past its own gauntlet. lemon is the one partial that stays, on a confirmed page and with its note rewritten to say what its basis is.

**Conversion convention** (the spec did not state one): a figure the page gives in inches is recorded in feet to four decimals, and the note quotes the inches; thyme's 16 in is 1.3333 ft. A59 checks only `0 < lo <= hi`; no gate rounds.

## The 10 woody crops that stay null, and why (decision rows for Trevor)

| crop | what T1 says | why null | to fill it |
| -- | -- | -- | -- |
| apricot | NC State Plant Toolbox: Dimensions block 20 to 40 ft tall and wide, prose on the same page "15 - 40 feet tall and wide"; Illinois 20 to 50 ft height; the crop's own rootstock rows cap the standard tree at 15 to 25 ft | the page does not unambiguously state the lower bound, and a crop-level 20 to 40 would sit beside in-record rows at 15 to 25 | a ruling on which statement the record cites, or a second T1 page; the MSU backyard tree fruit PDF (reported "15-25 feet tall by 20 feet wide", unread, WAF-blocked) is the lead |
| plum | NC State Prunus salicina (Japanese) 20 to 33 by 15 to 30; NC State Prunus domestica (European) 10 to 20 by 10 to 20; UMN 15 to 20 ft for European and hybrid plums | the two species pages do not overlap and the record lists 4 European to 3 Japanese varieties, so the basis is a decision, not a read | a ruling on the plum record's species basis; under PLA-463 plum is `size_control` on Marianna, so the recommended Myrobalan standard size is what R2 asks for |
| cherry-sour | Virginia Tech 422-018: species 15 to 20 ft, Mahaleb named on the page as the standard tart-cherry rootstock, "slightly dwarfing (20% smaller than mazzard)" | the catalog does not admit Virginia Tech (`vt_ext` absent); cannot cite what is not in the catalog | admit `vt_ext` under A54 (titled, pathed) or find the figure on an admitted host; UMN gives 8 to 15 ft |
| cherry-sweet | PNW 619 (an `osu_ext` anchor): Gisela 6 = 80 to 85 percent of full size; "can easily be maintained at a height of only 8 feet" | no T1 page gives Gisela 6 in feet; percent of an unstated standard, and the 8 ft is a managed height | a ruling that a percent-of-standard figure may be recorded as modeled (with the standard it multiplies), or null stands |
| pear-european | WVU: OHxF 87 = 85 to 90 percent of standard; UMN: the OHxF series "tops out at about 20 feet"; UNH: about two thirds | same: percent only, and the sources disagree (70 to 90 percent) | same ruling as cherry-sweet |
| pear-asian | Oklahoma HLA-6257: "Asian pears usually are about 8 to 12 feet tall", not tied to OHxF 87; WSU EB0937 says Asian pears should be on OHxF 97 or 333, not 87 | the figure is species-level and the recommended rootstock itself is questioned | a finding on `recommended_rootstock` for pear-asian; then read on the ruled basis |
| orange-navel | UC MG Santa Clara: "Standard tree 20-25 feet high", read from an archived capture because the live page is WAF-blocked; UF/IFAS HS982 (retired, read from an LSU-hosted copy): 15 to 20 ft on standard rootstocks | both candidate pages are archived or retired copies, and they disagree | a live T1 read outside the sandbox, or a ruling that an archived capture of a WAF-blocked extension page is citable |
| grapefruit | HS982: 15 to 20 ft on standard rootstocks; HS1260 rates Swingle intermediate, 8 to 14 ft | retired publication, and the two UF/IFAS statements conflict on the recommended rootstock | same as orange-navel |
| mandarin-clementine | HS1260: trifoliate orange rated small, "less than 8 ft"; nothing states a clementine size; the crop's cited UCR anchor is a satsuma page | no figure at all; the anchors are the wrong scion | a clementine-specific T1 read; fix the satsuma anchor |
| lemon (authored) | see above | | |
| lime | UF/IFAS CH093: Tahiti lime "a height and spread of about 20 feet", a single figure; Key lime "rarely taller than 12 feet" | a single figure is not a range, and the crop's two anchors are two species | a ruling on which lime the record means, and whether "about 20 feet" may be recorded as a range |
| raspberry | USU: summer-bearing primocanes "4 to 8 feet the first year under ideal conditions" on a T-trellis; UGA: erect primocane-fruiting types 3 to 4 ft, no trellis | the figure depends on the training method, which the record does not state | a ruling on the method basis for cane fruit |
| blackberry | every T1 figure is a tipping or maintenance ceiling (Clemson 3 to 4 ft free-standing erect); trailing canes run 15 to 20 ft | no page states an unpruned mature height | same ruling as raspberry |

Findings surfaced by the reads, not fixed here: oregano's `uarizona_ext` anchor is Lippia graveolens (Mexican oregano, 6 to 10 ft), a different genus; mandarin-clementine's cited UCR anchor is a satsuma page; pear-asian's `recommended_rootstock` OHxF 87 is steered against by WSU; peach and nectarine rootstock rows carry spread 15 to 20 where the species page says 15 to 25 (the rows are nulled in Plan E); the Clemson HGIC host answers 403 to a browser user-agent and 200 to a curl or Googlebot one, and `canr.msu.edu` and every UC ANR page are WAF-blocked from this sandbox, so absence was never claimed for them.

## Armor

- `tools/plant_dimensions_gate.py` (A59), 21 unit tests written red before the gate existed; wired into `whole_crop_gate` after A58 with `A59_PRESENCE_ARMED = False`, to flip in the write commit; `tools/test_gate_plant_dimensions_a59.py` mirrors the A58 script test and asserts the flag matches whether the canonical carries the keys.
- `numeric_sanity_gate` bounds: height to 120 ft and spread to 80 ft on tree bases, 20 ft elsewhere, footprint 0.5 to 60 in; tests appended to its script.
- `docs/field_addition_register.md` row 30.
- `tools/promote_pla465_plant_dimensions.py` with `tools/staging/pla465_plant_dimensions/spec.json`, generated by `build_spec.py` from the readers' JSON (host aliases resolve a page to the umbrella catalog id that admits it; a generic host lookup had picked a pomegranate-specific id for every Plant Toolbox page). `EXPECTED_AUTHORED` pinned to 16 (see the staging-moved paragraph above).
- Suite `tools/test_promote_pla465_plant_dimensions.py`: **55 passed** on the final staging, replay-pinned to `a98b6cfd`. One driver was red on the clean copy at first: it nulled a container_ok crop's gallons on a crop that also carries a tray depth, which display_readiness accepts; fixed to null both.
- Harness `tools/mutate_pla465_plant_dimensions_suite.py`: **39 injected / 39 caught / 0 survived / 0 broken**, anchor preflight 39/39, sentinel reddened. **The positive control is now the WHOLE suite**, because a driver red on the clean copy grades its mutation caught for the wrong reason; the two-test control inherited from A1 let exactly that through on the first run.
- Three guards were removed at authoring rather than shipped unreachable: the shell count (ROSTER minus the pinned certified count), the closing totals (implied by the per-crop checks), and pair validity in check_spec_shape (the imported gate owns it, run on a synthetic in check_pre_state).

## Gauntlet on the scratch post-state `a7f234ce`

`whole_crop_gate` PASS on apple, thyme, lemon, peach, basil, pear-european. **`gate_all` 121/121 PASS on the 18-crop staging; on the final 16-crop bytes: **121/121 PASS**.** `plant_dimensions_gate --presence` 0 violations, 121/128 carry the keys, 16 authored. `register_completeness` PASS. `register_coverage_gate` PASS. `release_verify` (apple, base canonical, `--ref avocado` because every certified crop takes the keys and only a shell is byte-identical): section A lists all 121 as changed, which is the promote's declared scope; section B no new violations; the reference shell byte-identical; the "reference not PASS" and section E "novel region keys" concerns are the known artifacts of using an uncertified shell as the reference (`release-verify-reference-gap-false-novel-key`), pre-existing on live canonical.

## Independent source-truth review

Two adversarial reviewers, nine rows each, re-fetched every page from raw bytes on 2026-09-16 with instructions to assume each value wrong until the page proved it. **16 of 18 rows CONFIRMED; 2 DEFECTS, both struck** (apricot, plum, above). Every verbatim sentence was found on its live page; every staged pair equals the page's figure in feet; no page is archived or retired (EB0937 is still sold by WSU; HS402 is EDIS "Released", revised 2023; HGIC 1353 updated October 2025; the PSU page updated June 2026). Byte-for-byte re-fetch matched on apple, blueberry and lemon; the NC State Toolbox pages drift by 10 to 26 bytes per fetch, proven by diffing two fetches to be signed S3 image URLs and a CSRF token with the text invariant; the Clemson page drifts by one Cloudflare nonce line.

Flags the reviewers raised that are NOT page-truth defects and are carried here for the record: blueberry's page says "5 to 8 feet tall and wide at maturity or even larger" and the figure is northern highbush only; mulberry's page is Morus alba (tagged Weed) while the record's recommended variety is the alba x rubra hybrid, and the record's rootstock row already carries the same figure; rosemary's own cultivar list tops out at 4 ft (Arp) with Prostratus at 2 ft, all in the record's variety list, so the 4 to 5 ft species floor overstates them (the variety delta-overlay's job); persimmon's page figure is identical to the placeholder on all three record rootstock rows, earned by the page independently but the rows must never be read as corroboration; pawpaw's crop-level 15 to 30 is wider than its single rootstock row's 15 to 25 by 12 to 20; nectarine's and peach's rows say spread 15 to 20 where the page says 15 to 25 (the rows are nulled in Plan E); elderberry's companions prose says 8 to 12 ft where the page says 5 to 12; pomegranate's catalog entry `citable_for` says only the zone 8 suitability cell cites it, stale once this field does.

## Not verified

**Full `tools/` tree on the landed canonical `a7f234ce` (after the trio was bumped, 50 minutes): 2 failed / 5,596 passed / 1 skipped.** The two are the same pre-existing failures as every run this arc, neither touched by this promote: `test_bare_host_scan::test_self_pathed_population_at_this_canonical` (stale pinned population) and `test_cited_claim_scan::test_MUTATION_the_anchoring_only_walk_reproduces_the_false_pass` (eight uncached allium URLs, UNDETERMINED not absent). The +76 over the PLA-464 run are this promote's suite, the A59 unit tests and the a59 script test. Consumer rendering of the new keys is not built yet (spec section 8); the fields are inert until read. The 103 null crops are "not yet authored", not "not applicable".

## Task 8 owes, in one commit, on approval

`--expect-sha a7f234ce...`; `A59_PRESENCE_ARMED = True` and the a59 script test flips with it; the state trio; `promote_fixture.COMMIT_FOR` pin of `a7f234ce` in a follow-up commit, never an amend; the collision gate `PINNED_SHA` re-measure (no ids move; 36 / 24 / 12 should hold); `export_staleness_gate` E1 and E3 until the consumers move.

---

# Promote 2: the twelve nulls, recorded -- PREPARED AND HELD (2026-09-17)

**Base:** the landed `a7f234ce`. **Post-state:** `892c76fb9e89fd9a242f682a7040a71886cb128ec899092a4f6414d2e0708edb`, scratch only. **Apply on approval:** `python3 tools/promote_pla465_null_rulings.py --expect-sha 892c76fb9e89fd9a242f682a7040a71886cb128ec899092a4f6414d2e0708edb`.

Trevor's rulings of 2026-09-17 on the twelve woody crops whose plant dimensions stay null, recorded on the crops so no later pass reads a null as unread. No dimension value changes. Twelve `open_findings` entries appended on eleven crops, two on pear-asian, and ONE dated addendum appended to plum's existing finding `plum_self_fertile_boolean_european_default` (original summary byte-identical as a prefix, every other field untouched, the suffix opening with `[ADDENDUM 2026-09-17, PLA-465:`). Texts live in `tools/staging/pla465_null_rulings/build_spec.py`.

| crop | id | status | routed to | ruling |
| -- | -- | -- | -- | -- |
| mandarin-clementine | `..._unusable_anchor_pla465` | accepted | | unusable source: the cited UCR anchor is a satsuma page |
| orange-navel | `..._sources_conflict_pla465` | accepted | | unusable: archived capture and retired bulletin disagree; HS1260's class is not a measurement |
| grapefruit | `..._sources_conflict_pla465` | accepted | | unusable: HS982 15 to 20 against HS1260's Swingle 8 to 14 |
| apricot | `..._page_self_contradicts_pla465` | accepted | | unusable: 20 to 40 block against 15 to 40 prose; rows cap at 25 |
| cherry-sour | `..._source_not_admitted_pla465` | deferred | PLA-532 | Virginia Tech not admitted; URL, bytes and hash recorded; UMN's labelled estimate noted, not used |
| cherry-sweet | `..._derivation_declined_pla465` | accepted | | percent-of-standard; derivation declined, recorded so no later pass multiplies |
| pear-european | `..._derivation_declined_pla465` | accepted | | same |
| raspberry | `..._not_applicable_cane_pla465` | accepted | | not a property of the plant; A59 N/A predicate on `cane_type` owed |
| blackberry | `..._not_applicable_cane_pla465` | accepted | | same |
| plum | addendum on `plum_self_fertile_boolean_european_default` | deferred (existing) | variety-delta pass | type-aware; attached, not filed separately |
| lime | `lime_single_value_shape_two_species_pla465` | deferred | PLA-12 variety-delta pass | the plum shape: two species under one record |
| pear-asian | `..._basis_unstable_pla465` | deferred | PLA-463 Plan E | null until the rootstock finding resolves |
| pear-asian | `pear_asian_recommended_rootstock_questioned_pla465` | deferred | PLA-463 Plan E | filed on its own: WSU steers Asian pears to OHxF 97 or 333 |

**Where the table contradicted a stated reason**, reported before the ruling and carried into the records: cherry-sour's reason said its only figure is on the Virginia Tech page, but UMN, an admitted source, gives 8 to 15 ft under the page's own "Mature height (estimate)" heading; the finding records both and leaves the estimate question unruled. Navel and grapefruit also have a live UF/IFAS rootstock class each (Carrizo large 14 to 20, Swingle intermediate 8 to 14), which is a percent-of-standard by another name; recorded as such under the unusable-source ruling. Plum's European default already exists on the record, so the European figure was readable; ruled null and attached anyway, recorded in the addendum.

**Armor.** `tools/promote_pla465_null_rulings.py` (the ruling is about nulls: every target crop must be null on all three keys; records pinned by shape and vocabulary, `--` allowed in a backend record since two quote page text, the em dash not; the addendum targets one finding by id and exact original summary; set-before-value blast radius with the prefix byte-identical and plum's entry equal to original plus suffix). Suite **57 passed**, replay-pinned to `a7f234ce`; one driver was rewritten when it moved the only record on a crop and left the count unchanged, the same flaw the 464 suite caught. Harness **41 injected / 41 caught / 0 survived / 0 broken**, positive control the whole suite. Gauntlet on `892c76fb`: `whole_crop_gate` PASS on plum, pear-asian, cherry-sour, raspberry, apricot, lime; **`gate_all` 121/121**; presence 0 / 121 of 128 / 16 authored; register gates PASS; `release_verify` (plum vs ref apple, expect-changed the other eleven) clean in every section; leaf walk 96 added, 0 removed, 1 changed (plum's summary), all under `verification_status`.

**Owed with it, not in it:** the A59 N/A predicate on `cane_type` so the cane nulls read as N/A at the presence floor; the mandarin satsuma-anchor repair; the Plan E note that cherry-sweet's and both pears' rootstock-row heights are not T1-stated in feet.
