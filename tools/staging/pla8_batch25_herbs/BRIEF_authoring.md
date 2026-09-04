# PLA-8 BATCH 25 (HERBS) -- AUTHORING BRIEF

You author the `control_ladder` for ONE crop. You write ONE JSON file. You do not touch canonical,
you do not touch any other crop, and you do not edit any tool.

Canonical: `9a141091fce3378e3f9fc8e4e67c7200b7d654c883d86bc6961d3723f092afd2
(rebased from a9c84847fe2e0ad595db8cf9cc7d7e82ac65803e3284e16071be6d536bf9dad7, which differs only by the additive uc_ipm_pn7493
source_catalog entry; zero crop records changed)`.

## What a ladder is

A `control_ladder` is an ordered list of rungs, **least invasive first**. The tier order is the
one `control_ladder_gate.TIER_RANK` enforces, and it is NOT the order you would guess:

    cultural (0) -> physical (1) -> biological (2) -> soft_chemical (3) -> conventional (4)

**`biological` ranks BEFORE `soft_chemical`.** A ladder that puts `insecticidal_soap` above
`beneficial_predators` is out of order and will be refused. This brief originally stated the wrong
order; it was caught by importing the gate's table instead of retyping it. Each rung is:

```json
{"method": "<slug from control_methods>",
 "note_beginner": "<consumer prose>",
 "note_seasoned": "<consumer prose>"}
```

`method` MUST be one of the 64 slugs in `control_methods.json`. The rung order must be
non-decreasing in tier. A rung's method must be reachable for the problem's `type` via the method's
`applies_to`, unless your brief explicitly tells you the widening is filed.

**A short ladder is a legitimate ladder.** bee-balm's rust ships three rungs, all cultural. If the
sources support three cultural steps and nothing else, write three cultural rungs. Do NOT pad a
ladder to look thorough, and do NOT reach for a chemical rung because the tier exists.

## The rule that matters most: THE RECORD GOVERNS

You are handed a **record report** (`record_<crop>.md`) produced by an independent reviewer who
fetched and read every anchoring document. That report, not your own knowledge, is the warrant for
every sentence you write.

* If the report says a claim **HOLDS**, you may write it.
* If the report says a claim is **WRONG** or has **NO ANCHOR**, you may not write it, even if the
  crop's current record prose says it. The current prose is what this batch is correcting.
* If the report gives you a fact the record lacks (a timing, an overwintering site, a threshold),
  you may use it -- it came from a read document.
* **If your brief tells you to write something the report does not support, REFUSE and say so in
  your output.** Two batch-24 agents did exactly this and both were right. A refusal is a finding,
  not a failure.

Do not invent a figure. Do not invent a product rating. Do not invent a bee-safety claim. Every
temperature figure you write must appear in the record report.

## Region discipline

The audience is US home gardeners. `rhs` (Royal Horticultural Society) is catalog-admitted T1 and is
good for **organism identity, symptoms and biology**, but its climate guidance and especially its
**product-availability and pesticide-law statements are UK-scoped**. Never carry a sentence like
"no fungicides are available for use on culinary herbs" into US consumer copy: that is UK product
law, not a fact about the reader's options. If a US source makes an availability statement
(for example NC State's "There is a lack of OMRI-approved products"), that one is usable, scoped as
the document scopes it.

## Consumer copy rules (these are hard)

* **No em dashes.** Use commas, colons, semicolons, periods.
* American English. Temperatures render as `°F` (give the °F figure; a °C figure may follow in
  parentheses only if the source is metric and the report carries it).
* "plant" is lowercase except at sentence start or in "Plant Pro".
* **Everyday words.** Write "spray it off with water", not "dislodge via hydro-agitation". Write
  "the fungus lives through the winter in the roots", not "overwinters in the rhizome mass" --
  in `note_beginner`. `note_seasoned` may carry the technical term once it has been earned.
* `note_beginner` and `note_seasoned` are a DUAL REGISTER, not a long version and a short version.
  Beginner: what to do and why, in plain words. Seasoned: the mechanism, the timing, the tradeoff,
  the thing a practiced gardener would want that a beginner would not act on.
* **The two registers must not be the same sentence with words swapped.** A promote guard measures
  this and a similarity above threshold fails the batch.

## Do not copy precedent prose

You are given `shipped_precedents.json` for SHAPE ONLY: to see what a rung note looks like, how long
it runs, how the registers differ. **Copying a shipped sentence fails the batch.** A promote guard
compares every note you write against the whole shipped corpus using rare n-grams and a similarity
ratio taken in both orders, and it has caught multi-donor recombination before. Write your own
sentences from your own record report.

**Schema warning.** This batch is uniform FULL schema (`symptoms_*`, `cause_*`,
`organic_treatment_*`, `prevention_*`). Some laddered crops that look like natural precedent are
NOT: bee-balm, the obvious rust precedent, is a **NOTE-schema** crop carrying only
`note_beginner`/`note_seasoned`. Comparing your crop's prose against a NOTE-schema crop compares
absent fields to absent fields and reports identity. Use FULL-schema crops for any prose comparison.

## Template twins

Several entries in this batch are near-verbatim across crops (lavender / rosemary / sage
spittlebugs; the root-rot family; aphids and spider mites almost everywhere). **A template twin is
where a fabricated claim propagates.** If your crop's entry reads like a sibling's, that is a reason
to go back to your record report and write from the document, not a reason to reuse the sibling's
sentences. A promote guard refuses byte-identical rung notes across crops.

## Ids are PINNED. Use them verbatim.

`pinned_ids.json` gives the `id` and `type` for every problem on your crop. **Never re-derive an id
from the problem name.** A problem `id` is a join key: `varieties[].resistance` and
`varieties[].ladder_delta` point at it, and renaming one silently orphans every grade hanging off
it. The ids were decided against the whole roster and run through the PLA-449 collision guard
before you were dispatched. If you think a pinned id is wrong, SAY SO in your output; do not change
it.

## Method gaps already known for this batch (filed, not forced)

* **CORRECTED 2026-09-04 (lemongrass authoring agent was right, this brief was wrong).**
  An earlier version of this line said `prune_out_infection` "does NOT reach `fungal_foliar`" and
  told you to route rust and leaf-spot sanitation through `garden_sanitation` instead. That is wrong
  at the level the gate actually checks. `prune_out_infection.applies_to` is
  `{bacterial, disease_general}`, and `TYPE_TARGETS['fungal']` is
  `{fungal_foliar, fungal_soilborne, disease_general}`, so the intersection is `disease_general` and
  the method IS LEGAL on a `fungal` problem. The original claim was true of the applies_to VALUE
  `fungal_foliar` and false of the problem TYPE `fungal`, which is the only thing the gate tests.
  **`prune_out_infection` is available on every fungal problem in this batch**, and on rust and leaf
  spot it is arguably the more apt method, since the action being described is literally pruning out
  infected growth. `garden_sanitation` remains legal and is the better fit where the action is
  clearing debris rather than cutting out infection.
* There is **no method** for hot-water treatment of infected rhizomes or cuttings (RHS publishes
  44°C / 111°F for 10 minutes for mint rust). If your record report supports it, note it in your
  output as an unreachable claim; do NOT bend another method to carry it.
* `even_watering` reaches `physiological` / `mite` / `bacterial` only. If your record supports steady
  moisture against a fungal problem, that is the known two-class gap; file it, do not force it.

Report every claim your record supports that no method can carry, under `unreachable_claims`.

## Output

This batch does TWO things at once, because for most entries they are the same work: it CORRECTS the
record and it LADDERS it. The record pass found 16 wrong or unanchored claims and 22 entries with no
anchor at all, so authoring a ladder without fixing the record underneath it would ladder a
falsehood.

Write ONE file: `tools/staging/pla8_batch25_herbs/out_<crop>.json`.

```json
{"crop": "<slug>",
 "pests": [
   {"name": "<the TARGET name from pinned_ids.json>",
    "id": "<pinned>", "type": "<pinned>", "severity": "<pinned>",
    "control_ladder": [ {"method": "...", "note_beginner": "...", "note_seasoned": "..."} ],
    "sources": ["<catalog_key>", "..."],
    "anchoring_urls": {"<catalog_key>": {"url": "...", "verified": "2026-09-04"}},
    "field_corrections": {
      "cause_seasoned": {"new": "<replacement prose>",
                         "why": "<what was wrong>",
                         "anchor": "<catalog_key> + the verbatim sentence that carries it>"}
    }}
 ],
 "diseases": [ ... same shape ... ],
 "unreachable_claims": ["..."],
 "refusals": ["..."],
 "notes_to_orchestrator": ["..."]}
```

### `field_corrections` -- declare every prose field you change, and change no others

The promote applies **only** the pinned fields (`id`, `type`, `severity`, `control_ladder`,
`sources`, `anchoring_urls`) plus exactly the fields you declare in `field_corrections`, and it
REFUSES if any other leaf moved. This is deliberate: batch 24 found that an owner-and-count check
passes while a target's *unpinned* field changes unseen, so every changed leaf now has to match a
declaration. If you want to change a prose field, declare it. If you do not declare it, do not
touch it.

Each correction needs `why` (what was wrong with the current text) and `anchor` (the catalog key
plus the verbatim source sentence that supports the replacement). A correction with no anchor is
not a correction, it is a rewrite.

### Rows whose `from` says RENAME or SPLIT need the FULL field set

Check the `from` field on each row in `pinned_ids.json`:

* **`KEEP`** -- the entry already exists. Write the ladder, plus `field_corrections` for whatever
  your record report found wrong, plus `sources`/`anchoring_urls` if the entry had none.
* **`RENAME from 'X'`** -- the entry exists under a different name. Same as KEEP, but the display
  name changes to the target name. Make sure the prose still reads correctly under the new name:
  oregano's "Botrytis and humid-weather foliar disease" becomes "Powdery mildew", so any prose that
  described Botrytis is now wrong and must be corrected, not carried.
* **`SPLIT n/m from 'X'`** -- this entry is one limb of a bundle being broken up. The other limbs
  become their own entries. **You must author the FULL prose set for each limb**
  (`symptoms_beginner`, `symptoms_seasoned`, `cause_beginner`, `cause_seasoned`,
  `organic_treatment_beginner`, `organic_treatment_seasoned`, `prevention_beginner`,
  `prevention_seasoned`) as `field_corrections`, because the bundle's shared prose describes several
  organisms and is wrong for any single one of them. Do not divide the old sentences between the
  limbs; write each limb from its own anchors.

### Retired entries

Two entries are retired and are NOT in your pin table: lemongrass's "Generally pest-resistant
(aromatic-oil deterrence)" and thyme's "Foliar fungal problems in humid weather". Do not author them.
If your crop has one, your `notes_to_orchestrator` should say what sourced content from it (if any)
deserves to survive elsewhere in the crop record, and where.

### Then validate

Run `python3 tools/staging/pla8_batch25_herbs/validate_out.py <crop>` and fix what it reports. If the
validator is itself wrong, fix it on disk and say that you did: tooling handed to a fan-out gets
exercised harder than its author exercised it, and batch 24's validator was wrong twice. This one
already had a wrong tier order, caught by importing `control_ladder_gate`'s table instead of
retyping it.
