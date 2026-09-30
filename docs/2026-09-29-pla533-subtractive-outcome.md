# PLA-533 subtractive pass landed (2026-09-29)

**`edcd9bf9` -> `cd0f9f17`. ONE promote, five crops:** orange-navel, grapefruit, mandarin-clementine,
lemon, lime. Trevor ruled on it in three batches on 2026-09-29, from the chat review at
`_handoff/pla533_subtractive_review.md` (gitignored). Spec: `tools/staging/pla533_subtractive/spec.json`.

**This pass only deletes and repairs grammar.** Nothing adds a claim, a number or a citation, and the
promote refuses any after-text that carries a digit, a URL or a citation token. Every other word an
after-text adds is recorded per edit in the spec (`added_words`). **None of this resolves a PLA-533
blocking finding.** All seven findings and every launch flag are byte-identical before and after.
Certified stays 121 and launch-ready stays 114. Only a clause-checked re-author closes a finding.

## What moved

**31 string edits (12 whole-sentence deletes, 19 rewrites):**

- **Sulfur acidification (15 strings):**
  - Deleted the six `failure_diagnostics` "durable fix" sentences: orange-navel [4], grapefruit [5],
    mandarin-clementine [3], both registers each.
  - Cut the sulfur clause from `soil.preferred_description_seasoned` and both `ph.note_*` on each of the
    three crops.
- **Navel juice freezing (orange-navel `storage`):** cut the juice clauses and deleted the beginner
  "Squeeze the juice..." sentence. "Whole navels do not freeze well" and "segments in syrup" stay: they are
  unsupported but not contradicted, so they wait for the re-author.
- **Pot suitability (orange-navel `container_notes`):**
  - The seasoned note opens "A navel on Flying Dragon (a naturally dwarfing trifoliate rootstock) is well
    suited to a large pot."
  - The beginner sentence is replaced with Trevor's text: "A dwarf orange on Flying Dragon rootstock does
    well in a big pot."
- **Yield (orange-navel):** the "one hundred to two hundred or more pounds" figure is gone from both
  registers. "Dwarf container trees yield far less..." stays, by ruling.
- **Leaked kickoff note (orange-navel `container_notes.notes_seasoned`):** "Do not lift peach's container
  guidance here; unlike peach, citrus genuinely thrives in pots." deleted.
- **Dangling references (orange-navel):** "See the container watering note for detail." and "See the
  container fertilizer note for detail." deleted. They pointed at notes that do not render.
- **lemon `rootstock_options[0].traits_seasoned`:** ", so it is not a reason to choose against this one" cut.
- **grapefruit Flying Dragon `traits_beginner`:** the wrong-crop clause "...the key to growing oranges in cold
  climates..." cut.
- **lime:**
  - Deleted the note sentence "Where it is, sour orange is a broad default with good fruit quality and
    foot-rot resistance."
  - Deleted row 1's "Trade-offs are somewhat lower fruit quality and greater susceptibility to some diseases
    than sour orange."
  - Cut the note's framing clause "Tristeza virus is a lime concern rather than a rootstock one:". The
    sentence now reads "Key limes are susceptible to tristeza whatever the rootstock, and Tahiti limes may be
    susceptible to severe strains whatever the rootstock." The Tahiti half is CH093's own sentence; the
    Key-lime half is CH092's and was not read here.

**Structure:**

- **Flying Dragon `container_size_gallons` 25 -> null on orange-navel and grapefruit (shape B).**
  `container_suitable` stays `true`, unsourced, recorded on PLA-612. The full PLA-466 shape (flag AND gallons)
  was measured to cascade: Flying Dragon is the only container-suitable rootstock on both crops, so nulling the
  flag trips A58 rules 2 then 1 and ends in retracting the pot verdict.
- **lime: the sour orange rootstock row is REMOVED and `recommended_rootstock` is RETRACTED to null** (the
  PLA-466 shape; rough lemon is not promoted into it). No lime source recommends sour orange. UF/IFAS CH093
  (raw bytes `6fc9a10b...`, MANIFEST `5fc5357`) says tristeza "may cause tree decline and death of 'Tahiti' lime
  trees on susceptible rootstocks (e.g., sour orange, alemeow)". The row's `field_additions` record and
  `open_findings[5]` still name it: they are append-only history.

## Guards and proof

The promote pins the base SHA. Every edit's before-text must occur exactly once. No number or citation may be
added. It pins lime's row 0, lime's `recommended_rootstock` and Flying Dragon's pre-state. It compares the crop
SET before any value. Blast radius is checked **by reversal**: the declared changes are undone on a copy of the
post, and the result must equal the pre crop exactly. So a resolved finding, a flipped flag, a moved container
flag or any stray key refuses. Every other crop and top-level key must be byte-equal.

- **Suite `tools/test_promote_pla533_subtractive.py`: 28 passed**, RED first.
  - A post-state "held sentence" guard was measured UNREACHABLE: its driver was graded caught by the reversal
    guard, which fires first, and the spec check forbids declaring the edit. It was removed rather than shipped
    as coverage (the PLA-580 precedent).
  - The held guard was then retired when Trevor approved that sentence's deletion.
- **Harness `tools/mutate_pla533_subtractive_suite.py`: 15 injected, 15 caught**; positive control green;
  sentinel caught.
- **Independent cross-check:** the promote's output was byte-identical to a separately staged scratch copy
  (`_handoff/pla533_stage_subtractive_v2.py`) before the third-batch rulings.

## Gauntlet on `cd0f9f17`

- `whole_crop_gate` PASS on all five crops.
- `gate_all` PASS 121/121 certified, launch-ready 114/121; container-citation floor 4 (unchanged).
- `container_path_gate` 0; `register_completeness_gate` PASS. A null `recommended_rootstock` is gate-legal
  (no gate reads that key).
- **`release_verify --ref apple`** (a reference outside the change set, so lemon is not both edited and the
  reference):
  - no new violations on any of the five;
  - calendars coherent, no dashes;
  - the 16 section-E concerns per crop (evergreen region keys apple lacks) are IDENTICAL base-vs-base.
- Collision gate re-measured byte-identical (36 / 12 / 24) with a live positive control (33 / 9 / 24); pin
  advanced.

## Consumers

**plant-app needs a re-export after the push.** `src/data/guides.json` bundles `container_notes` whole
(`scripts/export-projection.mjs`), so the leaked-note deletion and the other container prose edits stay in the
app bundle until it is rebuilt. The export has been frozen at `d7b33682` until plant-app `378c7b9f` ships
(E1, waived [PLA-465]).

plant-astro picks this up only through a submodule bump, which is the astro session's call. Unlike the blockers
landing, this pass DOES change what users see: the text edits, "pot OK" instead of "pot OK, 25+ gal" on Flying
Dragon, and lime's rootstock card losing its sour orange row.
