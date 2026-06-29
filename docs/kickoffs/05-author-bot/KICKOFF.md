# Author-bot kickoff — author ONE new gold-standard crop

Paste the block below into a claude.ai session **with web search on** (the bot must find real
sources), filling in `{{TARGET}}` (the new crop) and `{{TEMPLATE}}` (the nearest certified crop to
model on). See `DIRECTIONS.md` for choosing the pair and running the pilot.

---

```
TASK: author the crop {{TARGET}} at GOLD-STANDARD quality, modeled STRUCTURALLY on the certified
template {{TEMPLATE}}, following the GS-arc methodology, and hand back a patch for the Claude Code
lane to apply + gate. You have web search -- use it; this job cannot be done from memory.

WHAT YOU ARE DOING (and the division of labor): you produce a DRAFT crop record. The deterministic
gates (A2-A36) catch STRUCTURE; a biology-fidelity judge + a human daily review catch SUBSTANCE.
Your draft WILL be reviewed and corrected -- aim correct-first, not flawless. But the two failure
modes below make a draft worthless, and the audits proved they are exactly what bots do. Avoid them.

THE TWO FAILURE MODES THAT KILL A DRAFT:
1. COPY-TEMPLATE-DON'T-REFIT. {{TEMPLATE}} gives you STRUCTURE ONLY -- which fields exist, their
   shape, the archetype, the region/zone layout, the dual-register pattern. It does NOT give you
   CONTENT. EVERY biological value must be RE-DERIVED for {{TARGET}} from real sources: pH, spacing,
   days_to_maturity, chill hours, sunlight hours, germination temp; the pests, diseases, companions,
   rotation family; the per-region planting/harvest calendars; the variety list. A {{TARGET}} that
   ships {{TEMPLATE}}'s pH, pests, or calendar is a FAILED draft. The single most common bot mistake
   is keeping the donor's biology -- do not.
2. FABRICATED OR VAGUE SOURCING. Every claim-bearing value cites a REAL Tier-1 source (US
   university extension / .edu) for {{TARGET}}, with a real working URL, in the
   source_catalog + anchoring_urls shape {{TEMPLATE}} uses. No invented source IDs, no "TODO"/
   placeholder URLs, no citing a source that does not actually cover the claim. If you cannot find
   a real source for a value, FLAG IT in a notes list -- do NOT fabricate one. The entire pipeline's
   trust rests on this; a fabricated citation is the worst possible output.

READ THESE IN THE REPO (do not reinvent the conventions):
- {{TEMPLATE}}'s full record in crops_data_final.json -- the structure + register pattern to mirror.
- CURRENT_STATE.md "Live locked decisions / guardrails" -- the archetype/dispatch rules + every
  locked modeling decision (do not relitigate them).
- register_bearing_field_inventory_v1_0.md -- which fields are dual-register prose vs categorical.
- source_truth_sampling_qa_v1_0.md -- the sourcing discipline this is held to.
- handoff_patch_format_v1_0.md -- the EXACT output format (CC applies it via tools/apply_patch.py).

THE GATE CONTRACT your draft must satisfy (or CC bounces it back -- you can self-check against these):
- Dispatch fields correct for {{TARGET}}: calendar_basis (one of the 7 bases), archetype (must map
  to that basis), zone_independent (true ONLY if non_seasonal_indoor), gating_factors (chill_hours
  for a chill-gated tree, heat_accumulation if heat-gated, photoperiod if day-length-gated).
- Coverage: the full 10-region roster (ca_desert/ca_interior/ca_north_coast/ca_south_coast/
  fl_peninsula/hawaii_tropical/low_desert_az/northern_tier/se_gulf/warm_arid), each region with real
  resolved_by_zone cells keyed by USDA zone (3-11), each non-tree cell carrying a NON-EMPTY calendar.
- Numbers within physical bounds AND right for the species. Soil TEXTURE is categorical chips
  (string arrays: preferred/problematic/tolerated_texture_seasoned); the soil PROSE is
  preferred_description_{seasoned,beginner}.
- Dual-register: every established consumer prose field carries BOTH _seasoned AND _beginner
  (description, care/watering/fertilizer, harvest, storage, region_notes, tips, ...).
- Consumer copy: American English; NO em dashes (use commas/colons/semicolons/periods); temperatures
  render as °F; "plant" lowercase except sentence-start.

OUTPUT: a single handoff patch (per handoff_patch_format_v1_0.md) that builds {{TARGET}}'s full
record, with base_sha = the current canonical SHA. Plus a short notes list of anything you could NOT
source and any judgment calls you made. Hand both to the Claude Code (~/plant-dataset) lane: it
applies the patch, runs the gates (A2-A36) + release_verify, and queues {{TARGET}} for the daily
biology-fidelity review. Expect a correction loop -- that is the workflow, not a failure.
```
