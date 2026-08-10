# DECISION SPEC -- source_catalog titles (surfaced by PLA-155, 2026-08-10)

For Trevor to rule in the claude.ai lane. Written decision-ready per convention: one row per
decision, each with its own evidence. Nothing here is done yet except the two precedent entries
noted in D1.

## The problem, measured

`source_catalog` (206 entries) has **no title field populated anywhere**. `name` is typically
"Virginia Cooperative Extension Publication 426-331" -- an id restated, not a title. Three costs
landed this week, all documented:

1. **The ornamental-lead scan missed the one confirmed case.** With no titles, the
   vegetable-guide filter had to match on URL text; `vce_426_331`'s URL carries no subject
   word, so the scan that produced the 377-node lead list missed the document PLA-155 was
   about (issue body, "the scan producing it is itself undercounting").
2. **Wrong-pub-number defects are invisible at authoring time.** strawberry credited
   matted-row guidance to "426-331" when the content is in 426-840; edamame cited
   `vce_426_331` for claims whose anchors already pointed at SPES-455. An author seeing
   "Home Garden VEGETABLE Planting Guide" next to a strawberry matted-row claim would have
   caught both instantly. (Both fixed in `503c29f`; classification doc has the detail.)
3. **Genre/subject checks have nothing to work with.** The "ornamental crop citing a
   vegetable-scoped document" filter -- the sweet-pea mechanism, mechanical to detect in
   principle -- cannot be built without knowing what each document IS.

## Decisions

| # | decision | options | evidence / cost | recommendation |
| -- | -- | -- | -- | -- |
| D1 | Where does the title live? | (a) new optional `title` field; (b) convention: `name` = "Pub ID (Title)"; (c) no change | The two ids minted by PLA-155 (`vce_426_840`, `vce_spes_455`) already follow (b) -- e.g. "Virginia Cooperative Extension Publication 426-840 (Small Fruit in the Home Garden)". (a) is cleaner for tooling but is a schema addition consumers never read; (b) needs zero schema change and is already precedent. | **(b)** -- ratify the precedent; a tool can parse the parenthetical when needed |
| D2 | Backfill scope | (a) all 206; (b) only DOCUMENT-scoped ids (pathed URLs -- institution roots like `ncsu_ext` have no title to state); (c) none, new entries only | Institution-root ids are the bare-anchor convention and would get fabricated titles under (a) -- the fill-the-shape trap. Document-scoped ids are the ones the three costs above bite on. Rough count owed at build time; many are already cached so most titles come from the cache, not new fetches. | **(b)** |
| D3 | Gated or convention-only? | (a) hard A-gate: every NEW document-scoped id carries a title; (b) convention documented, ungated (the `verification_log_ref` pattern); (c) roster-wide hard gate | (c) blocks every promote on a backfill treadmill -- the exact thing the register-field rule exists to avoid mid-rollout. (a) only bites at mint time, when the author has the document open anyway. | **(a)** after the D2 backfill completes, (b) until then |
| D4 | Subject/genre tagging (`subject_scope`: vegetables / small-fruit / ornamental / pest / ...) | (a) yes, with D2; (b) separate later decision; (c) no | This is what makes the ornamental-filter class MECHANICAL. But it is a new vocabulary needing its own enum discipline, and a wrong tag is worse than no tag. Bigger than a title backfill. | **(b)** -- file separately once titles exist; titles alone already carry most of the signal for a human reader |
| D5 | Who and when | (a) fold into PLA-138 (instrument arc); (b) its own issue; (c) opportunistic (title added whenever an id is touched) | (c) is how the two precedent entries happened and costs nothing, but never converges. The backfill is a bounded mechanical pass over cached docs -- not instrument REPAIR, so PLA-138 is a scope stretch. | **(b)** own issue, small, after PLA-138's scanner fixes land (the scanners are the main consumer) |

## Explicitly NOT proposed

- No consumer-facing change of any kind (the catalog renders nowhere).
- No renaming of existing ids.
- No title on institution-root ids (D2) -- a bare anchor honestly labeled beats a decorated one.
