# How to run the author-bot — and the one-crop pilot

The author bot is the hard part of the pipeline: it produces a B+ draft, and its quality lives or
dies on **refitting the biology to the species** and **citing real sources**. The deterministic
gates + the daily biology review are what turn a B+ draft into a shippable crop. Do NOT expect
author-once-ship; expect author -> gate -> review -> correct -> re-gate.

## Pick the pair: {{TARGET}} (new crop) and {{TEMPLATE}} (nearest certified crop)

The template should share the **archetype + family shape** so the structure maps cleanly, while the
biology differs enough that refitting is real (which is the thing we're testing). Good pilot pairs:

| {{TARGET}} | {{TEMPLATE}} | why it's a clean template, and what must be refit |
|---|---|---|
| **parsnip** | carrot | Apiaceae cool-season root; refit: longer maturity, cold-sweetening, biennial habit, parsnip-specific pests (vs carrot's) |
| kale | broccoli | Brassica cool-season; refit: leafy not heading, more cold-hardy, no head-formation calendar |
| bell pepper | beefsteak-tomato | Solanaceae warm-season fruiting; refit: pepper pH/spacing/DTM, different heat behavior |
| rosemary | lavender | woody_ornamental Mediterranean subshrub; refit: culinary use, hardiness, different bloom |
| raspberry | blueberry | berries_woody (the dataset already names blueberry the template for the cane berries); refit: cane lifecycle, neutral pH (not acidic), different chill |

**Recommended pilot: parsnip ← carrot.** It's the most common archetype (frost_anchored annual), the
template is clean, and the refit is unmistakable (a parsnip that ships carrot's 60-75 day maturity or
carrot's pH would be the C7 failure made visible) -- so the pilot actually tests the discipline.

## Run it (the pilot loop)

1. **Author** (claude.ai, web on): fill `{{TARGET}}`/`{{TEMPLATE}}` into `KICKOFF.md`, paste, let it
   research + draft. Output = a handoff patch + a notes list of unsourced/judgment items.
2. **Apply + gate** (Claude Code, `~/plant-dataset`): CC applies the patch (`apply_patch.py`),
   runs `whole_crop_gate` (A2-A36) + `release_verify`. Structural problems bounce back to step 1.
3. **Daily review** (the biology layer): run `tools/daily_review_handoff.py {{TARGET}}`, take the
   package + `biology_fidelity_judge_v1_0.md` into claude.ai (the daily-review ritual,
   `docs/kickoffs/04-daily-review/`), and you eyeball it. Findings -> corrections.
4. **Correct + re-gate** until the crop is clean and you're satisfied. THEN it counts.

## What the pilot tells us (watch these)

- **Authoring quality:** how close is the draft? how much did it actually refit vs copy?
- **Sourcing honesty:** are the citations real and on-point? (Spot-check a few URLs -- this is the
  load-bearing check.) How many values did it have to flag as unsourceable?
- **Your review cost:** how long did one crop take you? That sets the sustainable daily batch size.
- **What the gates caught vs what only you/the judge caught:** confirms the silent-vs-substance split.

If the pilot is clean with reasonable review effort, we scale to ~5-10/day. If the draft is mostly
copied biology or thin sourcing, the kickoff discipline gets tightened before scaling -- far cheaper
to learn that on one crop than on a batch.
