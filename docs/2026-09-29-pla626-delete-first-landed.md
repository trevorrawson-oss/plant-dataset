# PLA-626 apricot/plum rootstock delete-first landed (2026-09-29)

**`d8906b43` -> `00dda31c`. ONE promote, two crops.** Trevor's rulings of 2026-09-29, from the chat review at
`_handoff/pla626_delete_first_review.md` (gitignored). Spec: `tools/staging/pla626_delete_first/spec.json`.
It follows the PLA-533 subtractive pattern: it removes wrong text and adds no claim, number or citation.

## Re-verification narrowed the ticket

PLA-626 was filed from PLA-566 Finding 3, which judged apricot's rootstock prose against FNRIC's apricot page. That
page is **silent** on the claims, and silence is not contradiction. UC IPM's **Apricot Pest Management Guidelines**
(T1, read live 2026-09-29 via WebFetch, no raw bytes saved) state them directly:

- Bacterial Canker: "Rootstocks of plum parentage (e.g. Myrobalan, Marianna 2624) are highly susceptible to bacterial
  canker." / "Lovell peach rootstocks are more tolerant than Nemaguard or apricot rootstocks."
- Nematodes: "Plum rootstocks Myrobalan 29C and Marianna 2624 are resistant to root-knot nematode, but susceptible to
  ring and root lesion nematode."
- Armillaria Root Rot: "Marianna 2624 is more resistant to Armillaria mellea than other apricot rootstocks, but is not
  immune."

So apricot's Myrobalan-canker, Lovell-canker and Marianna nematode/oak-root text is an **attribution** defect: the
rows cite `ucanr_ext` and `usu_ext`, which carry no rootstock content. It is not wrong text. It **stays**, and
re-anchoring it to these UC IPM pages is final-pass work on PLA-566. Deleting it as the ticket first proposed would
have taken true guidance off the site and contradicted apricot's own bacterial-canker entry and its
`resistant_rootstock` rung.

## What moved

- **apricot `recommended_rootstock`: "Myrobalan 29C" -> `null`.** FNRIC confines Myrobalan on apricot to very heavy or
  wet soils (the graft union breaks in wind), and UC IPM calls it highly susceptible to canker. Nothing is promoted
  into the field; a new pick belongs to PLA-566.
- **apricot `rootstock_options[2]` (Marianna 2624) `traits_seasoned`:** the wrong-crop "prune brownline" cut (a prune
  disorder). Now reads "...with resistance to root-knot nematode and oak root fungus."
- **plum `recommended_rootstock_note`:** "while Marianna and St. Julien are size-limiting choices for smaller trees and
  containers." -> "while Marianna is a size-limiting choice for smaller trees." St. Julien's row was dropped and its
  attribution retracted by PLA-466, and Marianna's container flag is null (not assessed). **The Myrobalan
  heavier/wetter-soils clause stays by ruling** (FNRIC supports it).
- **plum `container_notes` `notes_beginner` + `notes_seasoned`:** "St. Julien or Marianna" -> "Marianna". These are
  dangling references to the retracted row, outside PLA-608's scan.
- **Kept by ruling:** the apricot text above, plum soil "or Myrobalan", and plum Guardian's "Lovell, Halford" (Clemson
  says it verbatim, re-read live 2026-09-29).
- No finding, flag, id or region moves. Certified 121, launch-ready 114. plum stays not launch-ready (PLA-466 /
  PLA-579); apricot stays launch-ready.

## Guards and proof

The promote pins the base SHA and the change set. Each target must be found exactly once. Nothing may be added.
The retraction is pinned to apricot's `recommended_rootstock` = "Myrobalan 29C", and the Marianna row is pinned at
index 2. It compares the crop set before any value and checks blast radius by reversal. It also has a **purpose
guard**: no St. Julien may remain in plum's consumer text and no "brownline" in apricot's (verification_status is
exempt as history). The purpose guard catches a spec that forgot an edit, which the reversal check cannot see.

- **Suite `tools/test_promote_pla626_delete_first.py`: 33 passed.** RED was only a collection error before the
  promote existed, so the harness is the non-vacuity evidence. The kept-by-ruling text is asserted byte-identical,
  and both purpose guards are asserted to find their text in the pre-state (reachability).
- **Harness `tools/mutate_pla626_delete_first_suite.py`: 17 injected, 17 caught**; positive control green, sentinel
  caught. A separate run confirmed each mutation reddens its own driver, not just some test.
- The promote's output is byte-identical to the independently staged scratch (`_handoff/pla626_stage_delete_first.py`)
  reviewed in chat.

## Gauntlet on `00dda31c`

- `whole_crop_gate` apricot + plum PASS.
- `gate_all` PASS 121/121 certified, launch-ready 114/121.
- control_ladder 0/0; variety_resistance 0; variety_ladder_delta 0; register_completeness PASS; container_path 0.
- `release_verify --slug apricot --expect-changed plum --ref apple`: clean, only the two declared crops changed (also
  clean with `--slug plum`).
- Collision gate: whole output byte-identical (36 / 12 / 24) with a live control (33 / 9 / 24); pin advanced.
- **Full `tools/` tree: VERDICT PASS**, 182 collectable + 73 script-style entry points, 6,257 passed, the 2 known waived
  failures (PLA-544, PLA-161), 1 skipped.

## Consumers

- **plant-app:** the re-export PLA-628 now carries this too. `guides.json` bundles `container_notes` whole, and
  `TreeRootstockCard` reads `recommended_rootstock` and its note (null-safe; lime already ships null).
- **plant-astro:** `RootstockCard.astro` reads the same fields (`?? ''`). It picks this up through a submodule bump,
  the astro session's call.

## Handed on

- PLA-566: re-anchor the kept apricot text to the three UC IPM pages; decide a new `recommended_rootstock`
  (Nemaguard is the candidate); add the missing Myrobalan graft-union wind caution.
- PLA-608: plum's St. Julien hits are retired by content; the gate and its waivers are unchanged.
