# Window-token flip: same-rule candidates NOT flipped (for a ruling pass)

**Date:** 2026-07-10. Companion to the window-vs-token release (canonical `928c9d7c`).
Spec: `docs/superpowers/specs/2026-07-10-window-token-plant-indoors-flip-design.md`.

The release flipped EXACTLY the plant-app handoff's curated cells (item A: 7 plant flips; item B: 44
indoors flips). The same action-over-passive rule has more candidates across the roster. They were
DELIBERATELY left un-flipped -- a blind uniform sweep drags in artifacts and no-seed crops, and
several need a per-crop authoring call. Surfaced here for a ruling, not silently applied.

## Heat-side `indoors` candidates not flipped (23)

Boundary/adjacent months of a real indoor window sitting on a still-`heat_pause` month:
- tomato se_gulf z8/z9 **June** (beefsteak/heirloom; sp.start_indoors 'May 20-Jun 8' etc.) -- the
  fall seed-start's June tail. Entangled with item A's July plant flip on the same cells.
- tomato/broccoli/kohlrabi **low_desert_az z9, ca_south_coast z9/z10, ca_interior z8/z9, se_gulf z9,
  northern_tier z5** -- Jun/Jul/Aug boundary months #17's core rule and the handoff both skipped.
- fl_peninsula **beefsteak/heirloom z10/z11 July** (primary start_indoors 'Aug 1-21' bleeds no; the
  July flag is the pre-Aug boundary) -- #17 flipped Aug/Sep here, not July.

## Cold-side `indoors` candidates not flipped (50)

- **lemongrass (11 cells)** -- a no-seed division grass; its winter `start_indoors` overlaps a
  January `cold_pause` across 11 regions. Almost certainly should NOT flip (no real home indoor
  seed-start). Likely a data-model question (why does lemongrass carry a start_indoors at all).
- tomato / cucurbit / broccoli / kohlrabi / sweet-alyssum / habanero **northern_tier + ca_south_coast
  + ca_north_coast + warm_arid** Jan-Apr boundary cold months -- same class as item B's cold flips,
  just the months the handoff didn't enumerate (mostly the window's far-boundary month, e.g. the
  `Apr` tail of a 'Mar-Apr' window).

## Plant-flip (set-out shown on a `heat_pause` month) candidates not flipped (23)

- tomato/cucurbit/jalapeno/lettuce **warm_arid z8 (Jul/Aug), low_desert_az z9 (Aug)** -- a real
  `plant_out`/sp.plant_out set-out window overlapping a summer heat month; the item-A plant-flip
  rule would apply. Not in the handoff (item A was se_gulf tomato only).
- **Hawaii + potato + flowers** (borage/calendula/chamomile hawaii_tropical z11 Oct; potato
  fl_peninsula z11 Oct; sweet-alyssum/viola northern_tier z6 Aug) -- need a per-crop look; some may
  be legitimate set-outs during a declared pause, some may be a heat_pause that should not be there.

## Recommendation

Run a single ruling pass over these three groups on a STABLE roster: (1) fix or remove the
lemongrass start_indoors first (data-model), (2) decide the boundary-month policy (flip every
overlapped pause month, or keep #17's conservative core-ish curation), (3) extend item A's plant
flip to warm_arid/low_desert if the set-outs are real. The gates already ALLOW all of these
(A5 tolerates the flips; A5b backs them by overlap) -- this is an authoring-scope decision, not a
gate gap. Cold-side flips currently have no A5b-analog backing gate (see the release note); adding
one is the natural companion to that ruling.
