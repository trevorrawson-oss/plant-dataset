# Final Blind Re-Audit (#2) -- breaking the REMEDIATED armor before the bots

**Date:** 2026-06-28
**Auditor:** Claude Code session, fresh/blind context. The orchestrator mapped the armor from the
code, ran the C1-C16 regression itself, then dispatched **ten** clean-context, blind adversarial
sub-agents (2 per high-stakes surface: the dispatch guard, the coverage floors, the numeric/cross-
consistency truth layer, the roster/register layer; plus 2 "you are the bot" scale agents). Each was
given ONE surface and the instruction "the gates claim to catch everything here -- prove that false;
report only holes you reproduced past the live gate." None saw the others' work, the remediation
writeup, or the prior audit. The orchestrator then **independently re-verified** the highest-stakes
findings by direct injection with a DIFFERENT crop/defect than the agent used (apple, orange-navel,
zinnia, green-beans-bush, broccoli), and ran each "still-open" claim against `release_verify` too.
**Dataset SHA at audit:** `6dfd9798b9bfab364361ccb06ec8c8e29a105a3c45a6865a116d57ed787797b4`
(matches `LATEST.txt`, session `soil_texture_beginner_backfill_A36_cleared_18of18_CONTENT`).
**Discipline:** READ-ONLY on `crops_data_final.json`. Every injection in an isolated scratch copy;
the gates take an explicit path arg, so every PASS shown reflects the MODIFIED scratch file.
Canonical `shasum -a 256` confirmed byte-identical at start and end (§6). Baseline confirmed
**18/18 GATE: PASS** + `register_completeness_gate` PASS before starting.

---

## 1. Bottom line

The claim under test -- *"the gate armor, now HARDENED by the 2026-06-27 remediation (A30 dispatch
guard, A31/A32 coverage floors, A33/A34 truth-layer, tightened A25 + A35 laundering + A36 CP-required),
now catches every defect class that matters; the 18 are sound and the system is GO to scale 18 -> ~105
via a bot pipeline"* -- is **FALSE for the scale phase.**

The remediation's **mechanical 11 are genuinely closed and fire at the correct gate** (regression in
§3): C1 (A30), C2 (A3 chill-mirror), C3 (A31), C4 (A32), C5 (A9), C8-whitespace (A29 `.strip()`), C9
(§3 well-ordered), C10-egregious (A33), C11-long-string (A25), C12 (A23), C16-string (A36). That is
real progress and I confirmed each by injection + correct-gate VIOLATION.

But the audit reproduced **24 distinct holes that still ship `GATE: PASS`** (and `RELEASE-VERIFY:
clean`), and they fall into three structural patterns -- two of which are the SAME pattern the prior
audit named, re-opened one level down by the new armor itself:

> **1. The new floors/guards still dispatch on author-controlled fields they never validate.** A30
> hardened the ONE key `calendar_basis`, but the suite still trusts `zone_independent`, the
> `gating_factors` token set, per-cell `suitability`, and `archetype` -- flip any one and a
> load-bearing gate silently no-ops while the crop renders. The coverage floors check *that keys
> exist*, never *that enough productive structure exists below them*.
>
> **2. The new truth-layer gates are narrow-by-design and one-keystroke-evadable.** A33 bounds a
> fixed ~12-field list with wide margins; A34 parses exactly one pH rule and one harvest-token rule.
> The C11 ruling's premise that "non-string novelty is A33/A34's domain" is FALSE: a novel numeric
> field is bounded by nothing.
>
> **3. The roster/register tightening has structural bypasses.** Bare list-string elements escape
> A25 AND the dash/temp scans AND `release_verify`; the `_seasoned` suffix self-certifies any novel
> consumer field; backend-key families and `applicable:false` launder past the register gates. Two
> of these are LIVE in the shipping canonical (§4).

And the un-gateable truth layer (the prior audit's C6/C7/C14/C15) is **unchanged**: a fabricated T1
source chain and an entire wrong-species crop (`carrot`-relabeled-"Dragon Fruit", `basil`-relabeled-
"rutabaga") each ship clean on the first try, ~0% of the species-misfit caught. That is the dominant
bot failure mode and it has no deterministic defense.

**Verdict: NO-GO to scale 18 -> ~105 on the current armor.** Precise reason in §5.

---

## 2. Reproduced holes

Each verified by injecting into a scratch copy and confirming the live gate did NOT fail it.
**[RV]** = orchestrator independently re-verified with a different crop/defect than the sub-agent.
**[LIVE]** = present in the shipping canonical right now, not only in a scratch copy.

### 2A. Dispatch + coverage floors (the NEW A30/A31/A32 surface -- attack-hardest)

| # | Hole | Injection (slug) -> result | Where it lives | Scale |
|---|---|---|---|---|
| **D1** | **`zone_independent:true` is a master kill-switch for the whole region/calendar layer.** `_is_indoor()` trusts the flag, so A31 exempts the crop from the 10-region roster; an empty `regions` then no-ops A32/A2/A5/A24/A28. A6 (indoor-cycle requirement) keys on `calendar_basis`, NOT on `zone_independent`, so no indoor cycle is demanded either. `zone_independent` is validated against `calendar_basis` NOWHERE. **[RV]** (basil + carrot; control `regions={}` without the flag correctly FAILS A31). Converged by all 4 dispatch/floor agents. | `crop["zone_independent"]=True; crop["regions"]={}` (basis stays `frost_anchored`) -> **GATE: PASS** (A31:0, A32:0, A2 regions:0) | `coverage_floor_gate.py:28` (`_is_indoor`); wired `whole_crop_gate.py:86-95` | **HIGH** |
| **D2** | **Hollow regions: full 10-region roster, every `resolved_by_zone={}`.** A31 checks region KEYS only; A32 + A3 loop over cells that don't exist; A2 checks `plantings`, never cell presence. The crop ships zero month-strip calendars on every archetype. **[RV]** (basil N1b). Converged by 3 agents (apple/peach/carrot/zinnia). | `for r in regions.values(): r["resolved_by_zone"]={}` -> **GATE: PASS** (A31:0, A32:0, A2 regions:10) | `coverage_floor_gate.py:43-44,66-74`; `whole_crop_gate.py:159-185` | **HIGH** |
| **D3** | **No calendar-presence floor for the 3 non-tree perennial archetypes.** A32 is `frost_anchored`-only; A11/A14/A16 skip empty calendars as "admission state"; A10/A13/A15 don't require tokens. strawberry / blueberry / lavender can ship every cell `calendar:[]` clean. Converged by 3 agents. | every cell `calendar=[]` on strawberry/blueberry/lavender -> **GATE: PASS** | `coverage_floor_gate.py:63`; `berry_calendar.py:104`, `berry_woody_calendar.py:85`, `woody_ornamental_calendar.py:105` | **MED-HIGH** |
| **D4** | **`suitability:null` skips a tree cell entirely.** The `if s is None: continue` admission shortcut sits ABOVE every suitability/no-fruit/heat invariant; A4 only checks calendar<->date coherence. A fully-populated, calendar-bearing cell in an unsuitable zone with `suitability=null` certifies -- a 12-month fruit calendar renders where the tree dies. **[RV]** (apple `ca_south_coast.10` <- fruiting calendar, suitability=None; agents used peach + orange-navel). | copy a fruiting cell into a cold zone, set `suitability=None` -> **GATE: PASS** (A3:0, A4:0) | `perennial_gate.py:104-106` | **HIGH** |
| **D5** | **`heat_accumulation` token-drop disables the citrus heat floor (missing mirror of the C2 chill guard).** A3's heat floor ("insufficient can't be fruits_reliably") only runs when `"heat_accumulation" in gating_factors`. The chill token IS guarded (`perennial_gate.py:76`, the C2 fix) but the heat token has no mirror. **[RV]** (orange-navel; control WITH the token correctly FAILS). | drop `heat_accumulation` from orange-navel `gating_factors`, set a `fruits_reliably` cell `heat_summer_basis="insufficient"` -> **GATE: PASS** (control: 1 VIOLATION) | `perennial_gate.py:68,136` (no mirror of `:76`) | **MED** |
| **D6** | **Degenerate identical-token calendar.** A32 only checks the calendar is truthy; A5 requires length-12 + enum but NOT that plant/harvest tokens appear; A24 only polices pause tokens. `["growing"]*12` (zero planting guidance) certifies on non-succession annuals. | every cell `calendar=["growing"]*12` (strip heat_pause) on cherry-tomato/basil/zinnia -> **GATE: PASS** | `coverage_floor_gate.py:72`; `annual_calendar.py` A5 (no token-content requirement) | **MED** |
| **D7** | **Zone roster is never validated.** A31 validates region keys; no zone-key roster exists anywhere. A region's `resolved_by_zone` can be a single FICTITIOUS zone (`{"banana_zone": <cell>}`) or one real zone, and it certifies. | replace each region's `resolved_by_zone` with one invented zone key -> **GATE: PASS** | `coverage_floor_gate.py:31-54` (region keys only) | **MED** |
| **D8** | **`archetype` is read by NO cert gate.** A basis/archetype mismatch (`archetype="deciduous_fruit_tree"` on a `frost_anchored` carrot) ships; gates dispatch solely on `calendar_basis`. | `crop["archetype"]="deciduous_fruit_tree"` -> **GATE: PASS** | absence of any check (read only by builders) | **MED/LOW** |

### 2B. Truth layer (A33 numeric, A34 cross-consistency, E/F sources)

| # | Hole | Injection -> result | Where it lives | Scale |
|---|---|---|---|---|
| **D9** | **The entire source-citation chain is fabricable** (prior C6, still open by design). E checks only catalogue-membership + `tier=="T1"`; F checks only truthy `url` + truthy `verified` (no fetch). A fabricated `{tier:"T1"}` catalog entry, cited + anchored with a fake URL + `verified:true`, ships. Sub-variants reproduced: a `{tier:"T1"}`-only entry; `verified:"false"` (string) / `url:"TODO"` (truthy placeholders); an anchor URL pointing at the WRONG claim; source IDs in `source_set`/`source_id` keys bypass E's collection entirely. **NOT caught by `release_verify` either** (confirmed). **[RV]** (basil). | add fake T1 catalog entry, cite+anchor on `soil` with `verified:true` -> **GATE: PASS** + **RELEASE-VERIFY: clean** | `whole_crop_gate.py:730-744` (E), `:751-761` (F) | **HIGH** |
| **D10** | **In-bounds-but-wrong-for-species numbers.** A33 bounds are wide by design; values copied from another crop pass. **[RV]** (basil: DTM `[7,9]`, spacing `[70,72]`, sunlight `[1,2]`). | tomato `days_to_maturity=[7,9]`, `spacing_inches=[70,72]` -> **GATE: PASS** | `numeric_sanity_gate.py:60-72` (wide bounds) | **MED-HIGH** |
| **D11** | **Novel / uncovered NUMERIC fields are bounded by nothing.** A25 polices strings only; A33 bounds a fixed ~12-key list. A novel numeric (`max_yield_tons_per_acre=999999`, `plant_height_inches=-50`) AND uncovered existing numerics (`days_to_maturity_mid` -- a rendered Hero stat, unbounded even against its own parent range; `weeks_indoors`, `chill_hours_range`, `hardiness_zone_*`, `growth_stages[].day_range_from_sow`) all ship. **Directly falsifies the C11 ruling's claim that "non-string novelty is A33/A34's domain."** **[RV]** (basil). | `crop["max_yield_tons_per_acre"]=999999; crop["plant_height_inches"]=-50` -> **GATE: PASS** | `register_completeness_gate.py:195-197` (str-only) + `numeric_sanity_gate.py:57-78` (fixed list) | **HIGH** |
| **D12** | **A34 pH-prose parse is evadable.** RULE 1's regex requires a decimal on BOTH endpoints and takes only the first match. Integer prose ("pH 6 to 7"), single-value prose ("around pH 9.4"), a decoy decimal range first, or pH guidance in any field other than `ph.note_{seasoned,beginner}` all evade it -- the Hero pH stat can contradict the prose silently. **[RV]** (basil: struct `[3.0,3.4]` vs integer prose "pH 6 to 7"; control with decimal prose correctly FAILS). | `ph.preferred_range=[3.0,3.4]`, prose "pH 6 to 7" -> **GATE: PASS** | `cross_consistency_gate.py:35,39-46` | **MED-HIGH** |
| **D13** | **A34 harvest-requires-plant is satisfied by mere token presence.** RULE 2 checks only that SOME plant-class token exists in the 12-strip -- not order, not month-sanity. A harvest-before-plant strip (`["harvest"]*11+["plant"]`) or a plant token in an impossible month certifies. **[RV]** (basil). | cell `calendar=["harvest"]*11+["plant"]` -> **GATE: PASS** | `cross_consistency_gate.py:74` | **MED** |
| **D14** | **No prose-vs-structured cross-check beyond pH.** A prose note can claim "ready in 9 to 11 days" while `days_to_maturity=[55,70]`; every numeric except pH has a prose twin that can contradict it freely. | append "ready in 9 to 11 days" to a note vs DTM `[55,70]` -> **GATE: PASS** | `cross_consistency_gate.py:49-78` (pH + harvest only) | **MED** |
| **D15** | **A whole WRONG-SPECIES crop ships clean** (prior C7, still open by design). A `carrot`-relabeled-"Dragon Fruit" (cactus) and a `basil`-relabeled-"rutabaga" each certify with the donor's companions, pests, rotation family, varieties, pH/spacing, and ~184 consumer prose strings naming the donor crop -- plus wrong-climate calendars (growing through a Minnesota January, desert summer harvest with no heat_pause). The two scale agents measured **~0% of the species-misfit caught**; only the two A34 self-consistency rules fire. | deep-copy + relabel slug/name/botanical_name, keep all physiology -> **GATE: PASS** | no external-biology layer; `cross_consistency_gate.py:21-27` documents these as STILL OPEN | **HIGH** |

### 2C. Roster / register / dual-register (tightened A25 + A35 + A36 + A29)

| # | Hole | Injection -> result | Where it lives | Scale |
|---|---|---|---|---|
| **D16** | **Bare list-of-strings escapes A25 AND the dash/temp scans AND `release_verify`.** Every walk tests dict VALUES (`for k,v in o.items(): isinstance(v,str)`); a string that is a LIST ELEMENT has no key and is never tested. A novel list field laundering a forbidden em-dash + "degrees F" + unverified prose ships -- and `release_verify` §D misses it too (confirmed). **[RV]** (zinnia). | `crop["care_bullets"]=["Water at 70 degrees F -- pinch tips..."]` -> **GATE: PASS** + **RELEASE-VERIFY: clean** | `register_completeness_gate.py:197,201-203`; `whole_crop_gate.py:707,713-715` | **HIGH** |
| **D17** | **The `_seasoned`/`_beginner` suffix self-certifies a novel consumer field.** A25 rules ANY suffixed key by suffix alone; gate B counts a lone `_seasoned` as legit SP; A36 only requires dual for its hardcoded 74-name set. A novel `miracle_claim_seasoned` renders to growers and certifies. **[RV]** (green-beans-bush). | `crop["miracle_claim_seasoned"]="This bean cures all disease..."` -> **GATE: PASS** | `register_completeness_gate.py:144`; `whole_crop_gate.py:671-687` | **HIGH** |
| **D18** | **Backend-named keys beyond A35's 3-key set launder prose + forbidden chars.** `note_internal`, `source_note`, `resolution_note`, `source_quote`, `classification`, `disposition`, ... are `is_backend` (dash/temp-exempt) AND A25-excluded but NOT in A35's `{summary,claim,note}`. Rename `note`->`note_internal` and the em-dash/"degrees F" canon is bypassed for ~50 keys (A35 closed exactly 3). | `crop["source_note"]="...70 degrees F... -- our best results."` -> **GATE: PASS** | `register_completeness_gate.py:30,153-177`; `field_classification.py:25-47,76-86` | **HIGH** |
| **D19** | **Open-ended exempt key families mint NEW exempt keys.** `_is_ruled` exempts any `zone_\d+_<anything>`, any `*_basis`, and any path containing an excluded substring (`sources_summary`/`verification_status`/...). A bot invents `zone_9_pitch`, `marketing_basis`, or a top-level `sources_summary` carrying prose + forbidden chars. | `crop["zone_9_pitch"]="...hold 70 degrees F..."` -> **GATE: PASS** | `register_completeness_gate.py:147,148,100-105`; `field_classification.py:53-73` | **MED-HIGH** |
| **D20** | **EXCLUDED user-facing keys smuggle unverified prose.** `title`/`subtitle`/`notes`/`season` are roster-excluded yet rendered. Clean prose (no forbidden char) ships unreviewed. **[RV]** (basil N4clean; the em-dash variant IS caught by C/D since these aren't backend -- so the payload is the unverified prose, not the dash). | `crop["subtitle"]="Clinically proven to cure every disease..."` -> **GATE: PASS** | `register_completeness_gate.py:35-93` | **MED** |
| **D21** | **A36's `isinstance(v,str)` guard exempts a CP field expressed as a list/dict -- LIVE on 11/18 crops.** A CP-ruled `<base>_seasoned` whose value is a LIST silently skips the dual-register requirement. This is exactly the state of the soil-texture trio -- the very field the remediation cites as the A36 GATE-UNLOCK -- on 11 of 18 crops (`preferred_texture_seasoned=['loam','silt loam',...]`, no `_beginner`). **The CURRENT_STATE claim "A36 cleared -> soil texture both dual-complete on all 18" is enforced on only the 7 string-valued crops.** **[RV][LIVE]** (broccoli scratch: convert to list + drop beginner -> PASS; control with string `_seasoned` -> FAILS). | broccoli `preferred_texture_seasoned=["loam","sandy loam"]` + drop `_beginner` -> **GATE: PASS** | `cp_required_gate.py:59,61` | **MED** |
| **D22** | **Present-but-fake `_beginner` passes.** A36 checks key presence; A29 rejects null/empty/whitespace; B accepts any non-None. A `_beginner` that is a verbatim copy of the seasoned, `"N/A"`, or `"x"` certifies -- the dual register is a facade. | `ph.note_beginner` = copy of `ph.note_seasoned` -> **GATE: PASS** | `cp_required_gate.py:61`; `whole_crop_gate.py:676-677`; `register_fill_gate.py:62` | **MED** |
| **D23** | **`applicable:false` self-declared N/A skips authoring (prior C8 false-N/A half, still open).** A bare boolean on any ancestor dict blankets its register subtree as N/A -- A29 skips, A36 skips, B counts ruled-empty. Nothing validates the N/A is honest. **[RV]** (basil: `container_notes.applicable=false` + null self_watering_notes_{seasoned,beginner}; control without the flag correctly FAILS A29). | add `applicable:false` to a block + null its `_seasoned`/`_beginner` children -> **GATE: PASS** | `register_fill_gate.py:52-53` | **MED** |

### 2D. LIVE finding (shipping canonical)

| # | Hole | Evidence | Where it lives | Scale |
|---|---|---|---|---|
| **D24** | **A consumer `_seasoned` field whose base is not in the hardcoded CP set ships seasoned-only -- LIVE.** `lettuce-leaf.regions.ca_north_coast.microclimate_note_seasoned` ("UC Marin Master Gardeners note that lettuce...") has NO `_beginner` sibling, and `microclimate_note` is not in `CP_BASE_NAMES`. Beginners get no copy; the `_seasoned` suffix self-certifies through A25 (this is D17 made live). **[LIVE]** | read of canonical: `beginner_sibling=False`; A36 + B report 0 | `cp_required_gate.py:28-46` (hardcoded set); `register_completeness_gate.py:144` | **MED** |

---

## 3. Regression on the prior 16 (C1-C16) -- each re-injected against the CURRENT armor

| Prior | Status now | Evidence |
|---|---|---|
| **C1** calendar_basis enum | **CLOSED** (A30) | `basil` basis `"frost_anchored "` -> `VIOLATION: calendar_basis ... not a known base` |
| **C2** tree chill split optional | **CLOSED** (A3 chill mirror) -- but **side-door D5**: the heat-token mirror is missing, and **D4** (suitability:null) is an adjacent door on the same gate | `peach gating_factors=["cold_hardiness"]` -> `VIOLATION: must keep 'chill_hours'` |
| **C3** no region floor | **CLOSED for `regions={}`** (A31) -- but **side-doors D1/D2/D7**: `zone_independent`, hollow `resolved_by_zone`, fictitious zones | `carrot regions={}` -> `VIOLATION: missing canonical region(s) (has 0/10)` |
| **C4** calendar absent on cells | **CLOSED for stripped cells** (A32) -- but **side-doors D2/D3/D6**: empty cells dict, non-frost archetypes, degenerate calendar | `cherry-tomato` 20 cells `calendar=[]` -> 20 `calendar-presence` VIOLATIONs |
| **C5** photoperiod token | **CLOSED** (A9 machinery guard) | `onion` drop `photoperiod` -> `VIOLATION: gating_factors must contain 'photoperiod'` |
| **C6** fabricable sources | **OPEN by design** (D9) -- un-gateable; `release_verify` also clean | fabricated T1 -> GATE: PASS |
| **C7** fabricated/wrong-species crop | **OPEN by design** (D15) -- A33/A34 catch only egregious/self-contradiction; wrong-species ~0% caught | dragon-fruit / rutabaga -> GATE: PASS |
| **C8** whitespace + false-N/A | **half CLOSED** (A29 `.strip()`); **false-N/A half OPEN** (D23) | whitespace -> `VIOLATION: unauthored`; `applicable:false` -> PASS |
| **C9** inverted pH range | **CLOSED** (§3 well-ordered) | `[9,4]` -> `VIOLATION: §3 ph range nesting` (+ A34) |
| **C10** presence-only numerics | **CLOSED for egregious/negatives** (A33) -- but **D10/D11**: in-bounds-wrong + uncovered numerics open | `spacing=0`, DTM `[-5,-10]` -> A33 + A20 VIOLATIONs |
| **C11** bolting-class evasions | **(a) long/short string CLOSED** (A25 any-unruled-string); **(b) non-string NOT covered** (D11); **(c) laundering only 3 of ~50 keys** (D18) + list/suffix/family bypasses (D16/D17/D19) | `mystery_advice:"Water it lots"` -> `VIOLATION: unruled prose field` |
| **C12** raw-display regex | **CLOSED** (A23 case-insensitive) | `sunlight="Full_sun"` -> `VIOLATION: raw-display` |
| **C13** core_months tolerance | **SURFACED, not built** (Trevor's call); D13 is the adjacent harvest-token door | -- |
| **C14** omission (no pause shown) | **OPEN by design** -- no "this crop NEEDS a pause" model (subset of D15) | growing-through-desert-summer ships |
| **C15** companion enum-only | **OPEN by design** -- semantic | label upgrade ships |
| **C16** dual-voice by omission | **CLOSED for string CP fields** (A36) -- but **side-doors D17/D21/D22/D24**: out-of-set consumer fields, list-valued CP fields (LIVE), fake beginner | drop `description_beginner` -> `VIOLATION: cp-required` |

**Net:** the 11 mechanically-closeable holes are closed and fire at the right gate. But 5 of those
closures opened named ADJACENT side-doors (C2->D4/D5, C3->D1/D2/D7, C4->D2/D3/D6, C8->D23, C11->D16-19,
C16->D17/D21/D22/D24), and the 4 by-design-open holes (C6/C7/C14/C15) are unchanged.

---

## 4. The two LIVE findings (in the shipping `6dfd9798` canonical, not just scratch)

1. **D21 -- the "A36 cleared, soil texture dual-complete on all 18" claim is overstated.**
   `*_texture_seasoned` is a token LIST with no `_beginner` on 11 crops (cherry-tomato, beefsteak-
   tomato, carrot, basil, zucchini-courgette, peach, apple, lemon, lettuce-leaf, strawberry, zinnia)
   and dual PROSE on 7 (green-beans-bush, broccoli, blueberry, onion, microgreens-mix, lavender,
   orange-navel). A36's `isinstance(v,str)` guard silently exempts the 11 list-valued crops, so the
   gate enforces the CP ruling on 7/18, not 18/18. (Whether the 11 list-valued crops SHOULD be dual
   prose is a content/ruling question for Trevor; the GATE-level claim is what is inaccurate.)
2. **D24 -- `lettuce-leaf.regions.ca_north_coast.microclimate_note_seasoned` ships seasoned-only.**
   A sourced consumer region note with no beginner sibling; `microclimate_note` is outside the
   hardcoded CP set, so beginners get no copy and the suffix self-certifies through A25.

Neither breaks cert (both ship green) -- which is the point: they show the new register armor's
coverage claim is broader than what the code enforces.

---

## 5. The armor that HELD (so we know what is genuinely solid)

The remediation's mechanical work is real and these negative controls confirm it:

- **A30** catches a typo/case-slip/synonym/novel `calendar_basis` (the C1 closure).
- **A3** catches a `perennial_chill_gated` crop that drops `chill_hours` (C2); **A15** the same for
  `berries_woody`; **A9** an onion that drops `photoperiod` or nulls a filled cell's day-length type.
- **A31** catches `regions={}`, a partial roster, and an unknown/typo region key; **A32** catches a
  present-but-empty `calendar:[]` on a frost_anchored cell that EXISTS.
- **A33** catches the egregious C7 numbers (DTM `[3,5]`, annual spacing `[120,144]`, sunlight `[0,1]`);
  **§3** catches the inverted pH range (C9); **A34** catches a DECIMAL pH-prose contradiction and a
  harvest token with ZERO plant tokens.
- **A25** halts on any unruled scalar prose string (C11a) and a dict-nested unruled string; **A23**
  catches `Full_sun` (C12); **A29** catches whitespace/null register fields (C8 whitespace); **A36**
  catches a dropped `_beginner` on a string CP field (C16); **C/D** catch an em-dash in a normal
  string field; **A6** demands an indoor_cycle for a `non_seasonal_indoor` masquerade (the substance
  check `zone_independent` lacks); **E** catches an uncatalogued/T2 source; **F** catches a removed
  anchoring dict / empty url / boolean `verified:false`.

So the per-validator LOGIC is sound when correctly dispatched and when the value is the shape it
expects. The holes are, again, in dispatch on unvalidated fields, in coverage floors that stop at the
key level, in the deterministic truth layer's narrow scope, and in walks that test only dict values.

---

## 6. GO / NO-GO on scaling to ~105

**NO-GO on the current armor.** The 18 are sound and the mechanical remediation is genuine, but the
GO bet is "can the armor survive 105 BOT-authored crops," and three independent failure modes still
propagate silently at bot volume:

1. **The new floors/guards dispatch on unvalidated author-controlled fields and stop at the key level
   (D1-D8).** One flag (`zone_independent`), one dropped token (`heat_accumulation`), one nulled enum
   (`suitability`), or one level of emptiness below the region key (hollow `resolved_by_zone`,
   fictitious zones, non-frost empty calendars) disables a load-bearing gate while the suite prints
   PASS. This is the prior audit's exact pattern, re-opened by the very gates added to close it.
2. **The deterministic truth layer is narrow-by-design and one-keystroke-evadable (D9-D14, D16-D20).**
   A novel numeric is bounded by nothing (the C11 ruling's premise is false); the pH cross-check dies
   on an integer or a different field; list elements and the `_seasoned` suffix and ~50 backend-key
   names launder prose + forbidden chars past A25 AND the dash/temp scan AND `release_verify`.
3. **The un-gateable truth layer (D9, D15) is unchanged and is the dominant bot failure mode.** A
   fabricated source chain and a copy-template-don't-refit wrong-species crop each ship clean on the
   first try; the deterministic suite catches ~0% of species-misfit, and the only defense -- the
   advisory LLM biology-judge + the human source-truth sample -- does not scale to 105 x ~17 sources.

What is genuinely ready to keep leaning on: the wiring discipline (every `*_violations` is imported +
called), the per-archetype validator logic (sound when correctly dispatched), the mechanical C1-C5/C8w/
C9/C10/C12/C16-string closures, and the source-truth sample (necessary, load-bearing -- NOT a backstop
the gates make optional).

Highest-leverage closes before a re-audit (remediation is a SEPARATE memory-ON session -- this session
only finds + proves): cross-validate `zone_independent`/`suitability`/`gating_factors` tokens/`archetype`
against the real archetype (mirror the A30/A3 pattern to the other dispatch fields); make the coverage
floors require a non-empty `resolved_by_zone` + a real zone roster + extend calendar-presence to the
non-frost archetypes; walk list ELEMENTS and non-string values in A25 + the dash/temp scans; widen A35
to the full backend-key set and A36 to non-string CP values; require `verified is True` (boolean) at F;
and treat the species-truth layer as load-bearing QA that gates the bot pipeline, not an advisory.

---

## 7. READ-ONLY confirmation

`crops_data_final.json` SHA-256 at the START of this audit and at the END:
`6dfd9798b9bfab364361ccb06ec8c8e29a105a3c45a6865a116d57ed787797b4` -- **unchanged.** Every defect
injection was confined to scratch copies in the session scratchpad (`scratch_*.json`, plus per-agent
`agents/<surface>/` dirs); the canonical was never opened for write, `git status` shows it clean, and
the 18/18 baseline re-confirmed identical at the end. The gates were proven to read the modified
scratch file each time (explicit path arg; none hardcodes the canonical).
