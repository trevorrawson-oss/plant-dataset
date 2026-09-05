# PLA-8 BATCH 26 (TREES AND SHRUBS) -- AUTHORING BRIEF

You author the `control_ladder` for ONE crop. You write ONE JSON file. You do not touch canonical,
you do not touch any other crop, and you do not edit any tool except the validator, if it is wrong.

Canonical: `ce98b0a6f83cc04b380a6c3be3009709a7c6c3626b2611c88fafec1164997144`. READ-ONLY.

## What a ladder is

A `control_ladder` is an ordered list of rungs, **least invasive first**. The tier order is the
one `control_ladder_gate.TIER_RANK` enforces, and it is NOT the order you would guess:

    cultural (0) -> physical (1) -> biological (2) -> soft_chemical (3) -> conventional (4)

**`biological` ranks BEFORE `soft_chemical`.** A ladder that puts `insecticidal_soap` above
`beneficial_predators` is out of order and will be refused. Each rung is:

```json
{"method": "<slug from control_methods>",
 "note_beginner": "<consumer prose>",
 "note_seasoned": "<consumer prose>"}
```

`method` MUST be one of the 64 slugs in `control_methods.json`. The rung order must be
non-decreasing in tier. A rung's method must be reachable for the problem's `type` via the method's
`applies_to`. Read the method's own `how_it_works_*`, `best_use`, `pros` and `cons` before using
it: **gate-legal is not method-correct.** Batch 25's agents refused three gate-legal rungs on the
method's own text (a spotted leaf picked off is garden sanitation, not `prune_out_infection`), and
they were right each time.

**A short ladder is a legitimate ladder.** 54 shipped ladders have exactly one rung
(sweet-corn's raccoons is `exclusion_fencing` alone; peach's peach-leaf-curl is `copper_fungicide`
alone). If the sources support two cultural steps and nothing else, write two cultural rungs. Do
NOT pad a ladder to look thorough, and do NOT reach for a chemical rung because the tier exists.
These are perennials, and several of their problems have NO effective home spray (borers already
inside wood, black heart, popcorn disease, root and crown rot, pear decline): the ladder says so
inside the rung that IS available, and stops.

## The rule that matters most: THE RECORD GOVERNS

You are handed a **record report** (`record_<crop>.md`) produced by an independent reviewer who
fetched and read every anchoring document. That report, not your own knowledge, is the warrant for
every sentence you write.

* If the report says a claim **HOLDS**, you may write it.
* If the report says a claim is **WRONG** or has **NO ANCHOR**, you may not write it, even if the
  crop's current record prose says it. The current prose is what this batch is correcting.
* If the report gives you a fact the record lacks (a timing, an overwintering site, a threshold, a
  cultivar or rootstock name), you may use it -- it came from a read document.
* **If your brief tells you to write something the report does not support, REFUSE and say so in
  your output.** A refusal is a finding, not a failure.
* **Where the report quotes a document, and the claim matters, GO TO THE DOCUMENT.** Batch 25's
  one wrong rung was authored from a curated summary that omitted the sentence that mattered.
  The report's `ANCHORS` lines carry the URLs; read the page behind any rung you are unsure of.

Do not invent a figure. Do not invent a product rating. Do not invent a bee-safety claim. Every
temperature figure you write must appear in the record report or the method's catalog text.

## PLA-457: the sulfur/oil interval is HELD. Do not state one.

`control_methods.horticultural_oil` says to keep sulfur and oil two weeks apart; its own anchor
(UC IPM PN 7405) says 30 days; two other UC IPM Pest Notes say two weeks and three weeks. A
roster-wide ruling is pending and this batch does not pre-empt it. **No rung note and no
correction may state a sulfur/oil spacing interval, whichever figure it gives.** A promote guard
refuses any sentence that names sulfur, names oil and gives a duration. If a document you are
authoring from recommends both materials on the same problem (pear scab and pear psylla are the
likely cases), you may write both rungs, you may say the two are never mixed or applied close
together, and you must NOT give the number. Put the document and the figure it states in
`notes_to_orchestrator` under a `PLA-457` heading so the ruling can find it.

## Region and audience discipline

The audience is US home gardeners with one to a few trees. Several anchors for this batch are
COMMERCIAL documents (WSU tree fruit, UC IPM `agriculture/` pages): their biology is usable, their
per-acre rates, degree-day programs and postharvest thresholds are not. A rung that hands a home
grower a commercial monitoring program is a FIT defect. If the only home-scale signal a document
gives is "check the fruit" or "look under the leaves in spring", write that.

## Consumer copy rules (these are hard)

* **No em dashes.** Use commas, colons, semicolons, periods.
* American English. Temperatures render as `°F` (give the °F figure; a °C figure may follow in
  parentheses only if the source is metric and the report carries it).
* "plant" is lowercase except at sentence start or in "Plant Pro".
* **Everyday words** in `note_beginner`: "spray it off with water", "the fungus lives through the
  winter in fallen leaves". `note_seasoned` may carry the technical term once it has been earned.
* `note_beginner` and `note_seasoned` are a DUAL REGISTER, not a long version and a short version.
  Beginner: what to do and why, in plain words. Seasoned: the mechanism, the timing, the tradeoff,
  the thing a practiced gardener would want that a beginner would not act on.
* **The two registers must not be the same sentence with words swapped.**
* **Never name the machinery.** No "rung", "ladder", "tier", "applies_to", "control_method" in any
  consumer string. A guard refuses them.
* **A note describes the world, not the set of steps.** "This is the only step that works" goes
  false the moment a rung is added. Say what the method does.

## Do not copy precedent prose

`shipped_precedents.json` is for SHAPE ONLY: how long a rung note runs, how the registers differ.
**Copying a shipped sentence fails the batch.** A promote guard compares every note you write
against the whole shipped corpus using rare n-grams and a similarity ratio taken in both orders,
and it has caught multi-donor recombination before. Write your own sentences from your own record
report. Apple's ladders (codling moth, fire blight, scab) are the obvious precedent for the pears;
their METHOD sequences are fair to learn from, their prose is not yours to reuse.

**Template twins.** pear-asian and pear-european share byte-identical entries (Pear scab, Pear
psylla, Pear decline). Two agents author them independently, one per crop, and a guard refuses a
byte-identical rung note across the two crops. Write from YOUR record report; if your reviewer
found something the other pear's did not, your ladder may legitimately differ, and the
orchestrator will pin that divergence with your evidence. Say in `notes_to_orchestrator` why any
ladder on a shared problem is shaped the way it is.

## Ids and types are PINNED. Use them verbatim.

`pinned_ids.json` gives the `id`, `type` and `severity` for every problem on your crop. **Never
re-derive an id from the problem name.** A problem `id` is a join key: `varieties[].resistance`
and `varieties[].ladder_delta` point at it, and renaming one silently orphans every grade hanging
off it. The ids were decided against the whole roster and run through the PLA-449 collision guard
before you were dispatched. If you think a pinned id or type is wrong, SAY SO in your output; do
not change it.

Four of the six crops carried only the coarse `pest`/`disease` type; the pin table upgrades every
entry to a fine type (`insect`, `fungal`, `bacterial`, `vertebrate`, ...) and that fine type is what
decides which methods reach the problem. Check `applies_to` against the PINNED type.

## Method gaps already known for this batch (file them, do not force them)

* There is no method for **trunk protection from mower and string-trimmer wounds**, for **hand
  pollination as crop insurance**, for **trunk baffles or live-trapping** of mammals, or for
  **relocating a caterpillar** rather than killing it. If your record supports one of these, list it
  under `unreachable_claims`; do NOT bend another method to carry it.
* `balance_nitrogen` does not reach `bacterial`. Fire blight's "do not push growth with nitrogen"
  is a real cultural control with no method; file it as unreachable, or carry it inside the
  `prune_out_infection` or `resistant_varieties` note only where the document ties it to that step.
* `resistant_rootstock` reaches `disease_general` and `fungal_soilborne`: legal on root and crown
  rot and on pear decline (typed `bacterial`), which is where the documents put rootstock choice.
* `borer_stem_surgery` is the only method reaching a larva already inside wood. `prompt_harvest`,
  `bird_netting`, `bird_scare_deterrents` and `exclusion_fencing` are the only four methods that
  reach `vertebrate`.
* `even_watering` reaches `physiological` / `mite` / `bacterial` only; steady moisture against a
  fungal problem is the known two-class gap. File it.

Report every claim your record supports that no method can carry, under `unreachable_claims`.

## Problems the sources say NOT to control

Three entries in this batch carry sources that say no control is warranted or none is available
(pawpaw's zebra swallowtail: "do not cause enough damage to warrant treatment", UMD; pawpaw's
peduncle borer: "does not require control of this insect", KSU, and no product is registered;
persimmon's psyllid: usually no treatment warranted). The catalog has no tolerate-and-monitor method,
and an empty ladder is a defect by this repo's convention. **The roster's own precedent is the
parsleyworm** (black swallowtail on parsley and dill): ONE `handpick` rung whose note leads with
tolerance ("many gardeners simply leave them alone") and describes hand removal as the whole control
where a grower wants it. Follow that shape: at most ONE rung, on the least-invasive method a document
leaves open, with the sources' do-not-treat framing carrying the note. Do NOT add a `bt` or spray
rung the sources never mention. If no document leaves ANY method open, REFUSE the ladder in
`refusals` and say so; the orchestrator decides, and that decision is flagged for Trevor.

## Two rulings on documents

* **A retired publication does not anchor.** UF/IFAS ENY-835 is 410 Gone and ENY-803 survives only
  on a third-party mirror; a URL the reader cannot open is not an anchor. Cite the live document
  that carries the claim (HS1389, UGA C784, Clemson) or file the claim as unanchored.
* **A proxy read is still a read of the live URL.** Where a page 403s first-party and was read
  through the `r.jina.ai` proxy or a Wayback capture, anchor the LIVE URL with today's date and say
  in `notes_to_orchestrator` which reads were proxied. A claim resting ONLY on an archival capture
  of a page that no longer exists is unanchored.

## Output

This batch does TWO things at once: it CORRECTS the record and it LADDERS it. Where the record pass
found a claim WRONG or unanchored, authoring a ladder on top of it would ladder a falsehood.

Write ONE file: `tools/staging/pla8_batch26_trees/out_<crop>.json`.

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

### `sources` and `anchoring_urls` -- every entry ships anchored, to the page that carries the claim

Every entry on these crops already lists sources, but the record pass found anchors pointing at
the wrong document (a stink bug entry anchored to a fire-blight factsheet), at a toolbox title row,
or at a page that never names the organism. Write `sources` and `anchoring_urls` from your record
report's ANCHORS lines: only keys the report verified, each with the URL the report read. Drop a key
the report found does not carry the claim (persimmon's anthracnose drops `clemson_hgic` per its own
cert log). Every key must be in the catalog and every anchored key must also be in `sources`.

### `field_corrections` -- declare every prose field you change, and change no others

The promote applies **only** the pinned fields (`id`, `type`, `severity`, `control_ladder`,
`sources`, `anchoring_urls`) plus exactly the fields you declare in `field_corrections`, and it
REFUSES if any other leaf moved. If you want to change a prose field, declare it. If you do not
declare it, do not touch it. Each correction needs `why` (what was wrong with the current text) and
`anchor` (the catalog key plus the verbatim source sentence that supports the replacement). A
correction with no anchor is not a correction, it is a rewrite. **A correction must make the field
MORE true, not merely different.** Batch 25 shipped one that added a driver its own cited document
contradicts two sentences later.

### Rows whose `from` says RENAME, SPLIT or KEEP-FROM-DUPLICATE

Check the `from` field on each row in `pinned_ids.json`:

* **`KEEP`** -- the entry already exists. Write the ladder, plus `field_corrections` for whatever
  your record report found wrong, plus corrected `sources`/`anchoring_urls`.
* **`RENAME from 'X'`** -- same as KEEP, but the display name changes to the target name. Make sure
  the prose still reads correctly under the new name.
* **`SPLIT n/m from 'X'`** -- this entry is one limb of a bundle being broken up. **You must author
  the FULL prose set for each limb** (`symptoms_beginner`, `symptoms_seasoned`, `cause_beginner`,
  `cause_seasoned`, `organic_treatment_beginner`, `organic_treatment_seasoned`,
  `prevention_beginner`, `prevention_seasoned`) as `field_corrections`, because the bundle's shared
  prose describes several organisms and is wrong for any single one of them. Write each limb from
  its own anchors.
* **The pears' retired duplicates.** pear-asian's pests[] "Pear scab" and pear-european's pests[]
  "Pear scab" and "Fabraea leaf spot" are retired: they were second copies of the diseases[]
  entries, authored separately. They are NOT in your pin table and you do not author them. Your
  record report graded BOTH copies; where the retired copy's sentence was the better-anchored one,
  carry it into the surviving entry as a `field_correction` with the same anchor.

### Then validate

Run `python3 tools/staging/pla8_batch26_trees/validate_out.py <crop>` and fix what it reports. If
the validator is itself wrong, fix it on disk and say that you did: tooling handed to a fan-out gets
exercised harder than its author exercised it, and the last two batches' validators were each wrong
at least once.
