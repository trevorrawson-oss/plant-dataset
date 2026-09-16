# PLA-464 Option A: the rootstock array holds rootstocks only -- PREPARED AND HELD

**Date:** 2026-09-16. **Base:** canonical `d7b33682` (HEAD `824cd27`, origin/main). **Post-state:** `a98b6cfdfd7c5ffdcccdb222ceaa141fdca79e0ed674f991c0dcb396c2534412`, written to a scratch file for the gauntlet and never to the canonical. **Apply on approval:** `python3 tools/promote_pla464_rootstock_array.py --expect-sha a98b6cfdfd7c5ffdcccdb222ceaa141fdca79e0ed674f991c0dcb396c2534412`.

Trevor's rulings D1-D6 (PLA-464, 2026-09-16), as applied. One departure, D5, measured and explained below.

## What the promote does (five crops; the 7 shells and the other 116 certified crops byte-identical)

| crop | rows retired (index: name) | note fold-in | `recommended_rootstock` | records appended |
| -- | -- | -- | -- | -- |
| fig | 0: Own-root (from cuttings) | yes | 'Own-root (from cuttings)' -> null | field_additions 1, open_findings 1 (PLA-533) |
| pomegranate | 0: Own roots (cutting-grown) | no, nothing crop-specific left | null, unchanged | open_findings 1 (PLA-533) |
| mulberry | 0: Own-root (from hardwood cutting); 2: Genetic dwarf (e.g. Dwarf Everbearing) | yes | 'own-root or Morus seedling' -> 'Morus seedling (alba or rubra)' | field_additions 1, open_findings 1 (PLA-533) |
| pawpaw | 1: Own-root seedling (ungrafted) | yes | 'Pawpaw seedling', unchanged | field_additions 1 |
| cherry-sour | 4: Own-root / genetic dwarf (North Star, Meteor) | no, the note already names both | 'Mahaleb', unchanged | open_findings 1 (PLA-7 Plan B) |

Array sizes after: fig 0, pomegranate 0, mulberry 1, pawpaw 1, cherry-sour 4. Every surviving entry byte-identical and in order. 18 declared changes: 6 rows, 3 notes, 2 sibling strings, 3 field_additions, 4 open_findings. Independent leaf walk: 108 leaves removed, 46 added, 9 changed, all on the five crops, top-level non-crop keys identical.

**The population is six rows, not seven.** Two independent nets on the base (name: own-root / own roots / genetic dwarf / ungrafted / cutting; prose: not a rootstock / not grafted / own roots / naturally small / genetic dwarf) agree on these six. The prose net's seventh hit, persimmon's D. virginiana, is a real rootstock whose prose mentions kaki "on its own roots". The PLA-463 pre-check's "seven" counted mulberry's Morus seedling row, which is a real graft rootstock and stays. The promote's own name net is a guard: the spec's six rows and the net's population must agree roster-wide in both directions.

## D3: the three fold-ins, for Trevor's read before the write

Each is the one crop-specific sentence from the retired row that neither the crop's existing `recommended_rootstock_note` nor PLA-463's Variant C framing copy already carries. Appended to the end of the existing note with one space. Common tongue, no em dashes.

- **fig:** "With no rootstock to resist root-knot nematode, a nematode-free, well-drained site is the real substitute for rootstock choice." (sources carried: `clemson_hgic`, `uf_ifas_edis`)
- **mulberry:** "On an own-root tree there is no graft union to keep above the soil, and any suckers are the same variety." (source carried: `ncsu_ext`; the grafted half of the contrast already lives on the surviving Morus seedling row)
- **pawpaw:** "An ungrafted seedling is a cheaper way to a tree, but expect variable fruit and a wait of about 5 to 8 years instead of around 4 for a grafted variety." (sources carried: `ksu_pawpaw`, `wvu_ext`; the two-seedling pollination point is already in `pollination.notes_*`)

**Dropped as duplicated, by crop:** pomegranate's row (own roots, cuttings, choose the cultivar, resprouts true to type, easy to keep pot-sized) is carried in full by its note, its container notes and Variant C, so nothing was folded; its existing note's resprout sentence still duplicates Variant C seasoned, which is PLA-463's to resolve when the framing copy lands. cherry-sour's row content (North Star and Meteor are genetic dwarfs that stay small on their own roots) is in its note already; the row's HEIGHTS (North Star 8 to 10 ft, Meteor 10 to 14 ft) and its 25 gal are recorded in the crop's new finding and routed to Plan B, not carried to the variety entries (D4). The remainder of every row's prose (about 4,400 characters in 18 strings) is dropped; it stays readable in git history at `d7b33682`.

**Where the sources live.** The crop level has no `sources` or `anchoring_urls` map and no `recommended_rootstock_note_sources` key, and adding one would be a cross-crop field addition. The existing convention for a post-certification amendment is `verification_status.field_additions[]` (`{field, date, sources, note}`, used by the pet_safe and timing_spine passes as "amend-not-recert"). Each fold-in appends one such entry carrying the row's source ids and, in its note, the row's anchoring URLs with their 2026-06-30 verification dates.

## D5 as amended: the raw read, and why the 15 is kept

**The read.** The retired mulberry row's only anchor, `ncsu_ext` https://plants.ces.ncsu.edu/plants/morus-alba-x-rubra-illinois-everbearing/, was fetched from raw bytes on 2026-09-16 (44,647 bytes, sha256 `4d700c7c35131f2e8f12915b1c9add8402c4ea404967520ee2b11949405e5024`, title "Morus alba x rubra 'Illinois Everbearing'"). The stripped text (5,939 characters) contains zero occurrences of gallon, container, pot, dwarf, height or size. It gives 3 to 5 ft of growth per year and 24 to 60 ft of planting space. The page is about Illinois Everbearing; it never supported the retired row's dwarf form, its 6 to 12 ft, or its 15 gal. **Absence confirmed, scoped to that document.**

**The measurement that changed the ruling.** The ruling was to null both figures if absent. On a scratch copy, nulling `container_notes.min_pot_gallons` on mulberry reddens `display_readiness` ("container_ok is True but no pot or tray dimension is present") and `whole_crop_gate` section 3 container fields, so `gate_all` would fail on mulberry and the promote would refuse its own output at `check_post`. Setting the variety's `container_min_gallons` to null additionally trips `container_path_gate` ("outside [1, 100]"); deleting that key is allowed. The only gate-clean null is "null both AND revert A1's flip" (container_ok false, container_path null), which would undo a flip Trevor ruled on the crop's own T1-read cultivar sentence, not on this figure.

**Applied, and CONFIRMED by Trevor 2026-09-16 before the write** (the flip rests on a bindable T1 sentence joined to an existing variety entry, not on the gallon figure; reverting would discard a verified decision to fix an unverified number; the 15 was already live, so recording it unanchored is strictly better than the silent status quo): the 15 is KEPT on both the crop and the Dwarf Everbearing entry, pinned on the base by `check_pre_state` and refused if moved by `verify_post` (container_notes and varieties are outside the declared keys), with a mulberry `open_findings` entry stating the figure is UNANCHORED, the read that proved it, and its routing to PLA-533, where mulberry is already first in the queue. If Trevor prefers the revert-the-flip variant, it is a spec edit plus a re-gauntlet, and the promote would need a flip block; not built.

## The mulberry pin does not survive this promote: a documentation-strength link doing a data-integrity job

Both figures, mulberry's `container_notes.min_pot_gallons` and Dwarf Everbearing's `container_min_gallons` in `varieties.recommended[]`, were inherited together from the retired row and are handed to PLA-533 together. They are pinned symmetrically HERE: the spec's `mulberry_gallons` block (both 15, `kept`), `check_pre_state` on the base, `verify_post` refusing a move on EITHER side alone (measured on the post-state 2026-09-16: crop 15 to 20 refused, crop to null refused, variety 15 to 20 refused, variety key deleted refused), and two suite drivers that make the pair visible where someone would otherwise unpair them, `test_refuses_a_gallons_move_on_mulberry` and `test_refuses_a_gallons_move_on_dwarf_everbearing`.

**After the write, no standing gate ties the two.** `container_path_gate` checks each figure's shape on its own, `display_readiness` reads only the crop figure, and nothing compares them. The only thing carrying the tie is the mulberry `open_findings` entry `mulberry_min_pot_gallons_unanchored_pla464`, which names both paths and says both. A future session that inherits this pin should not assume a gate is holding it. PLA-533's promote, when it re-derives the figure, must move both or add the guard it needs; the risk it is handed is exactly that one gets re-derived and the other does not. No other leaf in mulberry carries a gallon figure traceable to the retired row (item 4 of the 2026-09-16 pinning report: the watering soak and the yield prose are unrelated gallons; the surviving Morus seedling row has null gallons).

## D2 and D6

fig and pomegranate fall to their crop `min_pot_gallons` of 15 in both consumers once the rows are gone (the rows' 20 equalled `recommended_pot_gallons`). Each crop gets a finding recording that the 15 carries no anchor of its own, routed to PLA-533. fig's `recommended_rootstock` is nulled; mulberry's names only the surviving row, so astro's recommended-lift matches an entry again.

## Armor

- `tools/promote_pla464_rootstock_array.py`: guards documented in its header (population measured twice; each row pinned by crop, index and exact name; fold-in absent before and pre-plus-sentence after; every source in `source_catalog`; container_path_gate with presence ON plus display_readiness and numeric_sanity on the five; set-before-value blast radius; the two verification_status lists append-only behind a byte-identical prefix; --out refuses the canonical path; the write requires --expect-sha).
- `tools/staging/pla464_rootstock_array/spec.json`: generated from the data (row anchors and the page hash read, never retyped).
- `tools/test_promote_pla464_rootstock_array.py`: **80 passed** (79 at the prepared read; the variety-level gallons driver added on Trevor's confirmation 2026-09-16), replay-pinned to `d7b33682` through `promote_fixture.pre_state` (COMMIT_FOR pins it to `4ade2d4`).
- `tools/mutate_pla464_rootstock_array_suite.py`: **58 injected / 58 caught / 0 survived / 0 broken**; anchor preflight 58/58; positive control green; sentinel reddened; pytest rc 5 graded BROKEN.
- Four guards were REMOVED from the draft rather than shipped unreachable: a post-state net check (implied by entry count plus survivor byte identity), a fold-in count==1 check (implied by equality with pre plus sentence), a verify_post gallons assertion (the generic outside-keys loop refuses first), and a change-count refusal (every per-key check implies it). One driver was rewritten when it failed for the convention's own reason: moving fig's only retire row swapped a crop for a crop and an earlier check answered.

## Gauntlet on the scratch post-state `a98b6cfd`

`whole_crop_gate` PASS on fig, pomegranate, mulberry, pawpaw, cherry-sour. `container_path_gate --presence` 0 violations, 121/128, presence ARMED. `register_completeness` PASS. `release_verify` (mulberry vs ref apple, base canonical, expect-changed the other four): section A only the declared crops changed, catalog unchanged, sections B through H clean, verdict clean. `gate_all` **121/121 PASS** on the post-state and again on the landed canonical.

**Full `tools/` tree on the landed canonical `a98b6cfd` (run after LATEST.txt was bumped, 63 minutes): 2 failed / 5,520 passed / 1 skipped.** The two are the same pre-existing failures as every run this arc, neither touched by this promote: `test_bare_host_scan::test_self_pathed_population_at_this_canonical` (its pinned population is stale) and `test_cited_claim_scan::test_MUTATION_the_anchoring_only_walk_reproduces_the_false_pass` (eight uncached allium URLs, reported UNDETERMINED not absent). The +80 passed are this promote's suite. An earlier attempt at the tree was interrupted at collection because `test_doc_roster_claim_gate` asserts LATEST.txt matches the canonical at import; the tree must run AFTER the trio is bumped.

## What was NOT verified

- The three fold-in sentences were composed from the retired rows' prose, which cites T1 anchors verified 2026-06-30; the anchors were not re-opened for this promote. The sentences restate the rows, they do not add claims.
- Consumer behaviour on an empty array: plant-app's picker is guarded on length; plant-astro's `RootstockCard` is not, and an astro session is landing that guard with the submodule bump held (Trevor, 2026-09-16). Not re-run here.
- PLA-457's held promote applies with `--expect-sha` against `72371c02` and already refuses on `d7b33682`; it will refuse on `a98b6cfd` too. Its re-pin is owed regardless of which lands first.

## Task 8 owes, in one commit, on approval

`--expect-sha a98b6cfd...`; the state trio (CURRENT_STATE amended surgically, STATE_HISTORY appended, LATEST.txt bumped); `promote_fixture.COMMIT_FOR` pin of `a98b6cfd` in a FOLLOW-UP commit, never an amend; a re-measure of `test_problem_id_collision_gate`'s `PINNED_SHA` (it pins live canonical; no ids move, expect 36/24/12 to hold); `export_staleness_gate` will report E1 and E3 until the app rebuilds and the astro bump lands.
