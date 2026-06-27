# Incognito Red-Team Audit -- breaking the gates before betting 105 crops on them

**Date:** 2026-06-27
**Auditor:** Claude Code session, fresh context. Six clean-context, blind adversarial sub-agents, each
given ONE attack surface and the instruction "the gates claim to catch everything on your surface --
prove that false; report only holes you reproduced past the live gate." None saw the others' work or
the prior audit docs. The orchestrator (me) independently re-verified the eight highest-stakes findings
by direct injection rather than trusting the sub-agents -- with different crops and different defects
than the agents used, and corrected one agent's framing where its repro was incidentally caught by a
second gate (the peach A3/A4 isolation, §2 C2).
**Dataset SHA at audit:** `512e5a8d2cc6d5dba7c690244372ec6bbf24d1461aabc662d479e1454ac81331`
(matches `LATEST.txt`, session `pass3_register_prose_a29_corrections_batch_complete`).
**Discipline:** READ-ONLY on `crops_data_final.json`. Every defect injection in an isolated scratch
copy; the gates take an explicit path arg, so every PASS shown reflects the MODIFIED scratch file.
Canonical `shasum -a 256` confirmed byte-identical at start and end (§6). Method: build my own map of
the armor (every `*_violations()` function vs. what `whole_crop_gate.py` imports), then inject the
defect class and show `GATE: PASS` / `RELEASE-VERIFY: clean`.

---

## 1. Bottom line

The claim under test -- *"the gate armor catches every defect class that matters; the system is GO to
scale 18 -> ~105 via a bot pipeline"* (CURRENT_STATE.md: "Audit armor CLOSED -> GO to scale") -- is
**FALSE for the scale phase.** The B1/B2 wiring lessons held (every `*_violations` function is now
imported and called -- no unwired gate, no berries-only scope gap of the old kind), but the audit
reproduced **16 distinct holes that ship `GATE: PASS` + `RELEASE-VERIFY: clean`**, eight of them HIGH
scale-risk. The defects fall into one structural pattern:

> **Every gate verifies token-presence, enum-membership, and shape. The gates dispatch on, and trust,
> author-controlled fields they never validate -- so one keystroke (a typo'd `calendar_basis`, a dropped
> `gating_factors` token, a whitespace value, a capital letter, an omitted pause) silently disables a
> load-bearing gate or a whole gate family, with the suite still printing `GATE: PASS`.**

Precise verdict:

- **The 18 certified anchors are not implicated.** Every injection was a defect I introduced into a
  scratch copy; the canonical 18 still pass cleanly. This audit is about whether the ARMOR is strong
  enough to bet 105 BOT-authored crops on -- not about the current 18.
- **The dispatch layer is hollow (HIGH).** `calendar_basis` is never checked against a known enum
  anywhere in the suite. A typo, a case slip, or a novel value silently no-ops A3/A4/A5/A24/A28 (and
  the archetype gates). A live shell crop, `heirloom-tomato`, already ships `calendar_basis:
  "generic_placeholder"` -- its calendar is validated by nothing today.
- **The "is this fruit honest" logic is optional (HIGH).** The perennial no-fruit chill split and heat
  floor key on `gating_factors` CONTENT with no rule requiring the keying token -- while the
  structurally identical `berries_woody` gate DOES require it. A new fruit tree authored to the
  explicit-`gating_factors` convention (the convention lemon/orange set) drops one token and ships an
  over-promising fruit calendar.
- **The truth layer is entirely un-gated (HIGH, by design -- the scale claim over-trusts the gates).**
  No gate fetches a URL, checks a source exists, bounds a number, or compares a value to biology. A
  fabricated-but-catalogued T1 source, and an entire fabricated/biologically-impossible NEW crop, each
  ship clean on the first attempt. 100% of source-content and biology fidelity is defended only by the
  per-batch human sample -- which is a sample, and does not scale to 105 crops x ~17 sources each.
- **The always-on backstops are defeated at their boundaries (MED-HIGH).** Whitespace defeats the
  register-fill gate; an inverted pair defeats the §3 consistency gate with all fields present; a
  capital letter defeats the raw-display gate; a sub-25-char string or a backend-named key defeats the
  bolting-class catcher.

**Verdict: NO-GO to scale 18 -> ~105 on the current armor.** Reason in one line: the armor is
structural-only and dispatches on unvalidated author-controlled fields, so at bot volume the common
failure modes (near-miss enum strings, omissions, whitespace/casing noise, copy-nearest-template) each
slip a load-bearing gate -- and the only defense for the un-gateable truth layer is a human sample that
does not scale. (Remediation is a separate, memory-ON session per the kickoff; this session only finds
and proves. "Where it lives" file:line is given per finding as a map, not a fix.)

---

## 2. Reproduced holes

Each verified by injecting the defect into a scratch copy and confirming the live gate did NOT fail it.
"Self-verified" marks the eight I reproduced independently (different crop/defect than the sub-agent).

| # | Hole | Class | Scale risk | Where it lives |
|---|---|---|---|---|
| **C1** | **`calendar_basis` has no enum guard.** A typo (`"frost_anchored "`), case slip (`"Frost_anchored"`), synonym (`"annual"`), or novel value silently no-ops EVERY calendar gate (A5/A24/A28 for annuals; A3/A4/A22 for trees; A10-A16 for the other archetypes). A length-3 calendar with an `EXPLODE` token, or a `cold_pause` on a plant month, then PASSES. Live: `heirloom-tomato` ships `"generic_placeholder"`. **Self-verified** (basil pause-on-plant: A24 fires under correct basis, vanishes under the trailing-space typo). | Scope / unvalidated dispatch key | **HIGH** | `annual_calendar.py:147,275,323`; `perennial_gate.py:63`; `tree_calendar.py:105`; no enum check anywhere |
| **C2** | **Perennial chill/heat direction-split is silently optional.** A3's no-fruit chill split + heat floor key on `gating_factors` CONTENT. peach/apple ship `gating_factors:null` and fall through to the chill default, so they're covered -- but a tree carrying an EXPLICIT `gating_factors` that omits `"chill_hours"` flips `chill_gated=False` and skips the split. `berries_woody_gate.py:59` REQUIRES the token; the tree gate has no equivalent assertion. **Self-verified** (peach `ca_south_coast.10`, chill-limited [50,350], given a coherent fruiting calendar: A3 over-promise fires under default `gating_factors`, full `GATE: PASS` under `["cold_hardiness"]`). | Scope / B2-class sibling gap | **HIGH** | `perennial_gate.py:67-69` vs. the missing mirror of `berries_woody_gate.py:59` |
| **C3** | **No region/zone roster floor.** A non-indoor crop ships with `regions:{}` (zero coverage) or a single region/zone and PASSES -- "10 regions / 9 zones" is enforced nowhere. **Self-verified** (cherry-tomato `regions={}` -> `GATE: PASS`). | Coverage floor missing | **HIGH** | `whole_crop_gate.py:99` (iterates whatever exists); no `len>=N` |
| **C4** | **The month-strip calendar can be entirely ABSENT on filled cells.** Delete `calendar[]` on every filled cell (keep plantings + region_notes) and the crop certifies. A5/A24/A28 + release_verify C all `continue` on an absent calendar; A2 checks plantings, never the calendar. **Self-verified** (cherry-tomato, 20 cells stripped -> `GATE: PASS`). | Presence floor missing | **HIGH** | `annual_calendar.py:153,281,329`; `release_verify.py:123`; `whole_crop_gate.py:99-127` |
| **C5** | **`gating_factors` omission disables A9; null cell-type evades coverage.** Drop `"photoperiod"` from an onion's `gating_factors` and an invalid `day_length_type:"banana"` ships; or null a single filled cell's `recommended_day_length_type` to evade A9 coverage + window-fit while still rendering a calendar. | Scope / self-declared jurisdiction | **MED-HIGH** | `photoperiod_gate.py:67` (factor gate), `:94-96` (null skip) |
| **C6** | **The entire source-citation chain is fabricable.** Gate E only checks a cited ID is in `source_catalog` with `tier=="T1"`; F only checks `url` non-empty + `verified` truthy (no fetch); A28 only checks presence. ADD a fabricated `{tier:"T1"}` entry to the catalog, cite + anchor it with a fake URL and `verified:true`, and it PASSES. release_verify flags DROPPED catalog entries but PRINTS added ones without concern. A wholly fabricated heat_pause backing chain ships clean. **Self-verified** (fabricated `orch_fabricated_2099` T1 source on carrot.soil -> `uncatalogued:0; non-T1:0` -> `GATE: PASS`). | Un-gateable truth layer | **HIGH** | `whole_crop_gate.py:642-664` (E), `:680-681` (F); `annual_calendar.py:309-356` (A28); `release_verify.py:93-96` (add/drop asymmetry) |
| **C7** | **A fabricated, biologically impossible, copy-pasted NEW crop ships clean on the first try.** A "rutabaga" that is basil verbatim (mint-family rotation, basil pests/companions), `days_to_maturity:[3,5]`, `spacing_inches:[120,144]`, `sunlight_hours:[0,1]`, `ph:[3.0,3.4]` with prose that says 6.0-7.5, harvest charted 3 months BEFORE planting, `growing` through Minnesota January, 10 months of `cold_pause` in Phoenix, carrot's `heat_pause` object (wrong-crop physiology + sources) pasted in -> `GATE: PASS` + `RELEASE-VERIFY: clean`, zero iterations. | Un-gateable truth layer | **HIGH** | every always-on gate is structural; none reads biology/number truth |
| **C8** | **Whitespace + false-N/A defeat the always-on register-fill backstop (A29).** A29 emptiness test is `o is None or o == ""`, so `description_seasoned:"   "` or `"."` renders blank but PASSES; gate B then counts the whitespace pair as `populated CP` and SKIPS its null-sibling check. A self-declared `{"applicable":false}` slapped on an applicable field skips authoring it (control: same block without the flag -> A29 fires). **Self-verified path** (orch + agent both). | Backstop bypass | **HIGH** | `register_fill_gate.py:60,52`; `whole_crop_gate.py:593,597` |
| **C9** | **§3 pH nesting accepts an INVERTED `preferred_range` with `tolerated_range` present.** The check is `tolerated[0] <= preferred[0] and preferred[1] <= tolerated[1]` and never guards `preferred[0] <= preferred[1]`. `preferred:[9,4]`, `tolerated:[5.8,7.5]` -> `ph preferred [9, 4] within tolerated [5.8, 7.5]: PASS`. The Hero pH stat renders "9.0 to 4.0." **Self-verified.** | Consistency-gate logic bug | **MED-HIGH** | `whole_crop_gate.py:71-75` |
| **C10** | **A20 display-readiness is presence-only.** `spacing_inches:0`, `days_to_maturity:[-5,-10]`, negative/zero scalars are "present" and render onto the Hero/planner cards. `days_to_maturity` is unbounded by the entire cert suite. | Presence-only, no sanity bound | **MED** | `display_readiness_gate.py:21-31,53`; no range check |
| **C11** | **The bolting-class catcher (A25) is evaded three ways.** A novel unruled prose field ships if it is (a) < 25 chars (`"mystery_advice":"Water it lots"`), (b) non-string (number/list), or (c) under a generic backend-named key (`note`/`summary`/`claim`). `claim` double-launders: it also evades the C/D dash scan, so a forbidden `--` reaches a grower. Control: the same key with a long value -> A25 halts. | Backstop blind spot | **HIGH** | `register_completeness_gate.py:90` (len<25), `:87-88` (str-only), `:29-70` (EXCLUDED_KEYS) |
| **C12** | **A23 raw-display regex dodged by a capital or a space.** `^[a-z0-9]+(_[a-z0-9]+)+$` misses `"Full_sun"` / `"Slow_release_granular"` / `"full sun_partial"` -- all render verbatim with underscores to growers. Control: lowercase `"full_sun"` -> A23 fires. **Self-verified.** | Regex anchor edge | **MED** | `raw_display_gate.py:31` |
| **C13** | **A24 pause-placement rides the `core_months` day-precision tolerance.** `harvest:"Aug 15 - Oct"` makes Aug non-core, so a `cold_pause`/undeclared `heat_pause` on Aug -- a month the page advertises as harvest -- PASSES. Control: day-less `"Aug - Oct"` -> A24 fires. | Boundary tolerance abuse | **MED** | `annual_calendar.py:188-217` (`core_months`), `:295-305` |
| **C14** | **Omission is free: A28/A24/A5 only fire when the `heat_pause` TOKEN is shown.** Render a lethal desert summer as `growing`, delete the heat_pause object, and nothing fires -- the page tells a Phoenix grower carrots are "growing" through 110F+. No gate models "this crop NEEDS a pause here." | Omission class | **HIGH** | `annual_calendar.py:329` (token-presence guard) |
| **C15** | **A27 companion evidence checks enum membership, never justification.** Upgrade a pairing `traditional/medium -> research_backed/high` (its own `reason` prose still says "well established" / contradicts) and it PASSES; only an out-of-enum label fires. The grower-facing `provenance.label` is now untrustworthy. | Enum-only, no substance | **MED** | `companion_shape_gate.py:121-152` |
| **C16** | **Dual-voice downgraded to single-register by omission.** Delete the `_beginner` sibling and gate B counts the field `SP seasoned-only` (no violation) -- a field that should be dual-register ships with beginners getting no copy. "Presence IS the visibility declaration" means a bot declares any field single-register by simply not writing the sibling. | Dual-voice blind spot | **MED-HIGH** | `whole_crop_gate.py:606-607` |

---

## 3. The un-gateable truth layer -- how big is the gap the human sample is the only defense for

The kickoff asked this directly. The answer is: **total.** Quantified on carrot (a representative
annual): 17 distinct cited sources across 122 claim-bearing leaves / 225 anchoring entries. The gates
check, per entry: catalogued + T1 + url-nonempty + verified-truthy. **URL fetches: 0. Content-fidelity
checks: 0. Numeric sanity bounds: 0. Biology-vs-identity checks: 0.** Rewriting all 225 anchoring URLs
on carrot to `https://fake.invalid/...` with `verified:true` -> `gaps: 0` -> `GATE: PASS`.

This is not a gate bug -- the tools' own docstrings are honest ("proves a cell is well-SHAPED +
self-consistent + exemplar-matched, NOT correct"; "biology is Step 5"). The defect is in the SCALE
CLAIM, which conflates `GATE: PASS` with "shippable." The documented defense -- the per-batch
source-truth sample (protocol #6) plus the verbatim/copyright scan -- is the ONLY thing between a
fabricating bot and a live fabrication. At 18 hand-authored crops a careful human wrote every value; at
105 bot crops x ~17 sources, a fabricated-but-well-formed citation (or a copy-nearest-template crop that
forgot to refit biology -- the single most likely bot failure mode, C7) that lands outside the sampled
rows ships certified. The sample is a SAMPLE; the gap it covers is 100% of substance.

---

## 4. The armor that HELD (so we know what is genuinely solid, not just untested)

The B1/B2 lessons are learned and the gate LOGIC is well built -- the holes are in dispatch and
boundaries, not in the validators themselves. Confirmed by negative controls:

- **Wiring (the B1 lesson) is clean.** Every `*_violations()` function in `tools/` is imported and
  called by `whole_crop_gate.py` (A2-A29). No unwired gate; no defined-but-uncalled drift.
- **A24** catches a pause on a CORE (day-less) plant/harvest month: `cold_pause on core harvest month Aug`.
- **A28** guards a SHOWN heat_pause: `calendar shows heat_pause but the cell carries no heat_pause object`.
- **A5** catches an invalid token + a heat_pause-months/calendar disagreement: `invalid calendar token(s) ['frolicking']`.
- **A3** catches an invalid suitability and the over-promise WHEN chill-gated: `survives_no_fruit chill-limited (50 < 400) MUST have an empty calendar`.
- **A4** catches a basis MIS-LABEL to a valid sibling (deciduous tagged `perennial_evergreen`) -- the deriver mismatch fires. (Only a NOVEL/typo basis, C1, escapes A4 too, by no-oping it entirely.)
- **A9 window-fit** catches a blatant season contradiction: `short_day but plant_out window [5] includes spring/summer months`.
- **A22** catches a string variety chill (the B2 closure): `chill_hours_required must be numeric ... got '400-500 hours'`.
- **A27** enforces evidence enum membership: `provenance.label 'strong' not in [...]`.
- **A2** blocks a sparse fill (1-2 regions with nulls): `region unfilled (plantings stub/missing): se_gulf`.
- **A29** catches a TRUE empty string and a plain-null register field; **A25** halts on a LONG novel unruled field; **A23** catches a lowercase snake_case token; **§3** catches a non-nested preferred range; **release_verify H** catches a reversed `[hi,lo]` chill band; **release_verify A** catches a DROPPED catalog entry.

So the picture is precise: the per-archetype validators are sound, but they are guarded by
string-equality dispatch on author-controlled fields that are themselves never validated, and they are
tuned with tolerances (core-months, presence-only, enum-only, `== ""`) that a bot exercises far more
often than 18 careful humans ever did.

---

## 5. GO / NO-GO on scaling to ~105

**NO-GO on the current armor.** The 18 are sound and the gate logic is good, but three independent
failure modes would silently propagate across 105 bot-authored crops, and the only defense for the
biggest one does not scale:

1. **Unvalidated dispatch + missing floors (C1-C5).** One author-controlled string (`calendar_basis`,
   `gating_factors`) or one omission (no calendar, no regions) disables a load-bearing gate or family
   while the suite prints PASS. A bot emits near-miss strings and omissions at volume.
2. **Backstop boundaries (C8-C16).** The always-on gates that exist precisely to catch bot sloppiness
   (register-fill, §3, raw-display, bolting-class, dual-voice) are each defeated by a one-character
   variant (whitespace, capital, swapped endpoints, short string, dropped sibling) -- exactly the noise
   a generator produces.
3. **The un-gateable truth layer (C6, C7).** 100% of source-content and biology fidelity rides on a
   human sample that, at 105 x ~17 sources, will not cover what a fabricating-or-template-copying bot
   produces.

What is genuinely ready to keep leaning on: the wiring discipline (B1 closed), the per-archetype
validator logic (sound when correctly dispatched), and the per-batch source-truth sample (necessary,
working -- but it must be treated as load-bearing QA, not a backstop the gates make optional).

Remediation -- the enum guard on `calendar_basis`, the `gating_factors` assertion mirroring
`berries_woody`, the region/calendar floors, `.strip()` emptiness, the `preferred[0]<=preferred[1]`
check, the case-insensitive raw-display regex, and the structural question of how to defend the truth
layer at scale -- is a SEPARATE, memory-ON session (so it does not re-propose a gate already tried and
rejected). This session only found and proved.

---

## 6. READ-ONLY confirmation

`crops_data_final.json` SHA-256 at the START of this audit and at the END:
`512e5a8d2cc6d5dba7c690244372ec6bbf24d1461aabc662d479e1454ac81331` -- **unchanged.** Every defect
injection was confined to scratch copies (`a1_`-`a6_` per sub-agent, `orch_` for my own re-verification)
in the session scratchpad; the canonical was never opened for write, and `git status` is clean. The
gates were proven to read the modified scratch file each time (explicit path arg; none hardcodes the
canonical).
