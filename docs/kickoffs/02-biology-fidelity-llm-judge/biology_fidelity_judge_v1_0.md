# Biology-Fidelity Judge — rubric, review process, and calibration (v1.0)

**Date:** 2026-06-28
**Lane:** claude.ai (authoring/judgment lane). This is a QA design + calibration deliverable, not a code build. No deterministic gate is proposed here; the deterministic gates (A2–A36) stay the hard cert bar.
**Calibration ground truth:** `certified-18.json` @ SHA `512e5a8d` (the 18 `verified_gs_arc` anchors + shared `source_catalog` + `region_chill_delivered`).
**Addresses:** the un-gateable truth layer from the 2026-06-27 incognito red-team — C6 (fabricable source chain), C7 (biologically-impossible copy-template crop), C14 (no gate models "this crop NEEDS a pause here"), plus the three checks the remediation explicitly routed to this lane (calendar-vs-climate, rotation-family vs botanical-family, wrong-crop pause physiology).

---

## 0. What this is and what it is not

The deterministic gates prove a crop is **well-shaped, self-consistent, and exemplar-matched.** The red-team proved that is not the same as **correct**: a fabricating or copy-nearest-template bot can ship a crop that passes every structural gate while being biologically false. The Claude Code lane has since built the deterministic *self-contradiction* layer — A33 `numeric_sanity` (numbers within physical bounds) and A34 `cross_consistency` (pH prose vs structured range; harvest-requires-plant). Those catch a crop contradicting **itself**.

What no structural gate can reach is a crop that is internally consistent but **wrong about the world**: a plausible-looking pH that is wrong for *this species*, a citation chain that is well-formed but fabricated, a heat-pause whose prose describes a different crop, a calendar that grows a frost-tender crop through a hard freeze. Catching those needs botanical knowledge applied to the specific crop. That is this judge.

**This judge is a QA AID, not a gate.** It is non-deterministic, it can be wrong, and it emits *findings for human triage*, never auto-edits. Its place in the pipeline is advisory-by-default (see §5). The hard cert bar remains the deterministic suite plus the load-bearing per-batch source-truth sample.

**Scope boundary that must not be crossed (decision B3):** heat and cold tolerance are **per-crop × region × zone physiology, backed per-cell.** This judge evaluates whether a given cell is plausible *for that crop in that region/zone*; it must never collapse tolerance into a shared region-heat or region-cold envelope. "Broccoli tolerates this cool month; a frost-tender crop does not" is a per-crop judgment, exactly the thing automation rejected and the judge is for.

---

## 1. The rubric — eight dimensions an expert asks of one crop's record

Each dimension below names: the question, where the signal lives in the schema, the failure mode it targets, and — critically — the **calibration carve-outs** (the legitimate shapes in the 18 that the judge must NOT flag). The carve-outs are not footnotes; they are the difference between a usable judge and one that cries wolf on correct crops.

The judge evaluates one crop at a time, with the crop's `slug`/`name` as the identity anchor (the judge knows what a carrot *is*), the full crop record, and the shared `source_catalog` + `region_chill_delivered` table as context.

### D1 — Family coherence: do pests, diseases, companions, and rotation match the crop's real botanical family?

- **Signal:** `pests[].name`, `diseases[].name`, `companions.*`, `rotation.family`, `rotation.avoid_after_*`. Identity from `slug`/`name`.
- **Failure targeted:** C7's signature — "a rutabaga that is basil verbatim," carrying mint-family rotation and basil's pests/companions. The copy-nearest-template-and-forget-to-refit mode.
- **What the judge does:** From the crop's identity, derive its true family and its expected pest/disease/relative profile, then check the record against it. Rutabaga is *Brassicaceae*; a rutabaga citing `rotation.family: "Mint family (Lamiaceae)"`, listing basil downy mildew, and warning against planting after basil is a hard flag.
- **Calibration carve-outs (load-bearing — these are correct in the 18):**
  - **Top-level `family` and `botanical_name` are null on 17 of 18 crops** (only carrot populates them). The judge must work from crop *identity*, never from the structured `family` field, and must NOT flag a null `family`/`botanical_name` as a defect. A rubric that keys on those fields false-positives 17/18.
  - **`rotation.family` is free-text, not a Latin enum**, and is null on 4 crops (lemon, blueberry, orange-navel, lavender). Phrasings like `"Nightshade family (Solanaceae)"`, `"Brassica family (Brassicaceae), the cole crops"` are correct. Null is legitimate (skip the structured-family check for those; still check pests/companions against identity).
  - **`rotation.family` uses the grower-relevant grouping, which is sometimes the genus or common family, not the current APG clade.** Onion ships `rotation.family: "Allium"` — botanically Amaryllidaceae, but "Allium" is the correct rotation grouping for a grower (it captures the crop's actual relatives). The judge evaluates "does this grouping correctly capture the crop's relatives for rotation purposes," not "does this string equal the textbook clade name." Flag only a grouping that names the **wrong** relatives (rutabaga→Lamiaceae), never a colloquial-but-correct one (onion→Allium).
  - **`microgreens-mix` is a multi-species blend:** `rotation.family: "mixed (multiple families in a blend)"`, mixed pests/companions. The judge recognizes blends and does not demand single-family coherence.

### D2 — Calendar-vs-climate: is every calendar cell physically possible for that region+zone, given THIS crop's real cold/heat tolerance?

- **Signal:** per cell, `regions[r].resolved_by_zone[z].calendar` (12-month token array), `region_chill_delivered[r][z]`, the region's `zone_span`, cell `min_winter_temp_f` (present on ~40 cells), `suitability`, and the crop's own `heat_threshold_temp_f` / chill fields. Token vocabulary in the 18: `harvest, growing, plant, cold_pause, dormant, bloom, heat_pause, season_over, indoors, prune, care, wait, renovation, late`.
- **Failure targeted:** C7's "growing through Minnesota January" and "10 months of cold_pause in Phoenix"; C14's "a Phoenix grower told carrots are growing through 110°F+." A calendar that is structurally valid but climatically impossible for the crop.
- **What the judge does:** For each cell, ask whether the token in each month is plausible for that crop at that region/zone's climate. A `growing` or `plant` token in a month the region/zone runs hard-frost, on a frost-tender crop, is a flag. A frost-tender crop showing `growing` through deep desert summer with no `heat_pause`, when the crop's own `heat_threshold_temp_f` says otherwise, is the C14 flag.
- **Calibration carve-outs (correct in the 18):**
  - **Cold-hardy crops legitimately grow in cool/shoulder months.** Broccoli zone 3 ships `[cold_pause ×3, plant, growing, harvest, plant, growing, harvest, cold_pause ×3]` — winter is correctly `cold_pause`, the workable season is `growing`/`harvest`. This is right. The judge must hold the crop's *actual* tolerance, not a blanket "no winter growth" rule.
  - **`suitability: "unsuitable"` + empty `calendar: []` is the correct encoding for "this crop can't grow here,"** not missing coverage. Lemon in `northern_tier` is `unsuitable` with `calendar: []`. The judge must NOT flag an empty calendar on an unsuitable cell as a defect — that is the dataset correctly saying "don't grow lemons in zone 3."
  - **`heat_pause` / `cold_pause` are the correct tokens for a real climatic exclusion**, and they carry an object with `months` + `basis_*` prose + sources. Their presence is correct, not suspicious. The judge reads the *basis prose* under D5, not the token's existence.
  - `min_winter_temp_f` is null on most cells; absence is not a defect. The judge uses `region_chill_delivered` and the region/zone identity as the climate anchor when the explicit field is absent.

### D3 — Numeric species-fitness: are the numbers right for THIS species, not merely within physical bounds?

- **Signal:** `days_to_maturity`, `days_to_maturity_mid`, `spacing_inches`, `ph.preferred_range`/`tolerated_range`, `chill_hours` (perennials), `sunlight_hours`, `germination_temp_f`, `heat_threshold_temp_f.temp_f`.
- **Failure targeted:** C7's `days_to_maturity:[3,5]`, `spacing_inches:[120,144]`, `sunlight_hours:[0,1]`, `ph:[3.0,3.4]` — each inside A33's *physical* bounds (or nearly) but absurd *for the species*. A33 catches "pH 47"; only the judge catches "pH 3.2 for a crop that wants 6.5."
- **What the judge does:** For each numeric, ask whether the value is in the right neighborhood for the named species — a carrot at 70-80 days, a blueberry at pH 4.5-5.5, a peach needing several hundred chill hours. Flag a value that is physically possible but wrong for THIS crop. This is the layer above A33: A33 is species-agnostic bounds; D3 is species-specific plausibility.
- **Calibration carve-outs (correct in the 18):**
  - **Empty `[]` / null is the legitimate N/A for a crop type that has no single value.** `microgreens-mix` ships `ph: []` and an empty `days_to_maturity` — a blend has no single pH or maturity. The judge treats `[]`/null as N/A, never as a violation (mirrors the gates' perennial-N/A handling). DTM `[]` on a perennial tree is likewise legitimate.
  - **Perennial chill values vary widely and legitimately by cultivar class.** A low-chill peach and a high-chill apple are both correct; the judge checks "plausible for this species/class," not against a single number.
  - Wide ranges are normal (germination temperature spans, spacing ranges). The judge flags *implausible center*, not *width*.

### D4 — Source-content fidelity (C6): do the cited sources actually support the claim, and is the citation chain real?

- **Signal:** every `sources` array + sibling `anchoring_urls` (`{url, verified}`), cross-referenced to `source_catalog` (133 entries; 124 T1, 9 T2), plus `verification_status.source_set`.
- **Failure targeted:** C6 — a fabricated `{tier:"T1"}` catalog entry, cited and anchored with a fake URL and `verified:true`, ships clean because gate E only checks "catalogued + T1" and gate F only checks "url non-empty + verified truthy," with zero fetches. Also a real-but-irrelevant URL that does not support the claim it backs.
- **What the judge does — two parts, different reach:**
  1. **Plausibility of the chain (in-context, the judge can do this now):** does the cited source *institution* plausibly publish on this claim? A carrot soil-pH claim citing Clemson HGIC is plausible; a carrot claim citing a fabricated-looking ID, or a citrus source on a blueberry chill claim, is a flag. The judge reads `source_catalog[id].citable_for` and asks whether the institution's stated coverage fits the claim.
  2. **Content fidelity (out-of-band, NOT this judge's live reach):** whether the URL's actual page text supports the specific number/claim requires fetching the page. That is the **source-URL liveness + content sweep** the remediation scoped as a periodic out-of-band job (≈1785 fetches/batch, flaky, bot-blocked — not a per-cert blocker). The judge flags *suspicious* chains for that sweep to prioritize; it does not itself certify content fidelity.
- **Calibration carve-outs (correct in the 18):**
  - **Every cited source in all 18 is catalogued** (verified: 0 uncatalogued across the set). The judge must not invent a fabrication where the chain is clean.
  - **High citation counts are normal** (cherry-tomato cites 42 distinct sources, lettuce 40, carrot 17). Density is a sign of thoroughness, not padding.
  - **T2 sources exist and may be referenced** (9 in the catalog); a T2 citation is not by itself a defect — the methodology allows T2 as reference. The judge flags a T2 *cited as T1-grade evidence for a biological claim*, not the mere presence of a T2 id.

### D5 — Pause-physiology attribution: does each heat_pause / cold_pause describe THIS crop's physiology?

- **Signal:** `resolved_by_zone[z].heat_pause` / `cold_pause` objects: `months`, `classification`, `basis_seasoned`/`basis_beginner`, `sources`, `anchoring_urls`.
- **Failure targeted:** C7's "carrot's heat_pause object pasted onto a different crop" — the wrong-crop physiology paste. The basis prose names carrot's 75°F root-quality ceiling while sitting on a tomato.
- **What the judge does:** Read each pause object's `basis_*` prose and check that the physiology it describes, and the crop it names, match the crop the object lives on. A pause whose prose says "sustained soil above the 75°F air-temperature root-quality ceiling degrades roots" belongs on carrot; finding that text on zucchini is a flag. Also check the pause's `sources` plausibly cover *this* crop.
- **Calibration carve-out:** the 18's pause objects correctly name their own crop's physiology (carrot's names carrot root quality; the broccoli/lettuce cold/heat pauses name cool-season bolting/cold limits). Correct attribution is the norm; the judge flags the mismatch, not the presence.

### D6 — Internal contradiction the gates miss (semantic):

- **Signal:** whole record — prose vs structured fields, cell-to-cell coherence within a crop.
- **Failure targeted:** the residue C7 leaves after A33/A34 run — e.g., prose describing one stage's behavior under a different stage's label, a companion note that contradicts the `bad_*` list, a `harvest_urgency` that contradicts the storage prose. A34 catches pH-prose-vs-range and harvest-requires-plant; D6 is the open-ended "anything else self-contradictory a structural rule did not encode."
- **Calibration carve-out:** the 18 are hand-authored and internally coherent; this dimension should be near-silent on them. Any D6 hit on a certified crop is a prime tuning signal (see §3).

### D7 — Dual-register / coverage honesty (the C16-adjacent semantic check):

- **Signal:** `*_seasoned` / `*_beginner` sibling pairs across the register-bearing fields; the cell-level `suitability` + calendar coverage.
- **Failure targeted:** C16 — a bot downgrades a field to single-register by simply not writing the `_beginner` sibling, and "presence IS the visibility declaration" means the gate counts it seasoned-only with no violation. The structural gate cannot tell "legitimately seasoned-only" from "should have been dual-register but the bot skipped it." The judge can ask the semantic question: *should* this field carry beginner copy?
- **What the judge does:** For a field a beginner would need (anything safety-, timing-, or action-bearing), flag a missing `_beginner` sibling as a *candidate* coverage gap for human ruling — explicitly NOT as a gate violation (the locked decision stands). This feeds the CP/SP ruling-inventory question the remediation surfaced (C16), it does not pre-empt it.
- **Calibration carve-out:** many fields are legitimately seasoned-only in the 18. The judge proposes candidates for ruling; it does not assert a violation. Tune the "a beginner would need this" threshold against the 18 so the candidate list is short and credible.

### D8 — Whole-crop plausibility gut-check (C7 catch-all):

- **Signal:** the entire record, read as one organism.
- **Failure targeted:** the fabricated-crop case where the *gestalt* is wrong even if no single field trips D1-D7 — the judge's holistic "would an extension horticulturist recognize this as a real, correctly-described crop?"
- **Calibration carve-out:** the 18 read as real crops; a flag here on a certified crop means the rubric or the judge's prior is miscalibrated.

---

## 2. The review process — how the rubric is applied

**One crop per pass.** Batching crops invites cross-contamination of judgment and dilutes attention; the failure mode (copy-template) is per-crop, so the review is per-crop.

**Inputs to each pass:** the single crop record; the shared `source_catalog` and `region_chill_delivered`; the rubric above. No other crops in context (so the judge cannot be primed to treat a copied crop as "consistent with its neighbor").

**The judge emits structured findings, never edits.** Output shape, one row per finding:

```json
{
  "crop": "<slug>",
  "dimension": "D1|D2|D3|D4|D5|D6|D7|D8",
  "field_path": "regions.low_desert_az.resolved_by_zone.9.heat_pause.basis_seasoned",
  "observation": "Pause basis prose describes carrot root-quality ceiling; crop is zucchini.",
  "why_it_is_wrong": "75F root-quality ceiling is carrot physiology; zucchini is heat-driving, not heat-excluded, in this window.",
  "confidence": "high|medium|low",
  "suggested_correction": "Re-author the heat_pause basis for zucchini, or remove if no real exclusion exists.",
  "routes_to": "human_triage | source_url_sweep | cp_sp_ruling_inventory"
}
```

- **`confidence`** is mandatory and load-bearing: it lets triage sort. A high-confidence family mismatch (rutabaga→Lamiaceae) is actioned first; a low-confidence "this pH feels slightly low" is reviewed but not urgent.
- **`routes_to`** sends each finding to the right destination: most go to **human triage / corrections log**; D4 content-fidelity suspicions go to the **out-of-band source-URL sweep** to prioritize which URLs to actually fetch; D7 dual-register candidates go to the **CP/SP ruling inventory** thread (C16), not to a gate.
- **Pattern escalation:** when the same finding class recurs across crops in a deterministic-gateable shape, it is escalated to the Claude Code lane as a candidate new gate (the way C9/C10-class self-contradictions became A33/A34). The judge is also a *gate-discovery* instrument, not only a per-crop reviewer.

**A clean pass emits zero findings** (or only low-confidence candidates with explicit rationale). Silence on a correct crop is the design target, not a failure to find something.

---

## 3. Calibration against the 18 — the false-positive discipline

The judge must be tuned so it does **not** flag the 18 certified, biologically-correct anchors before it is trusted on bot output. I ran a structural FP probe of the checkable dimensions (D1 family-consistency, D2/D3 numeric, D4 catalogued-source) across all 18. The probe surfaced **two false-positive traps a naive rubric would fall into** — both are now encoded as carve-outs above. This is the calibration payoff: the traps were found on correct crops, in advance, not discovered later as noise on bot batches.

**Trap 1 — colloquial-but-correct rotation family (onion).** Strict Latin-clade matching flags onion's `rotation.family: "Allium"` because the textbook clade is Amaryllidaceae. Onion is correct: "Allium" is the right rotation grouping for a grower. **Carve-out (D1):** evaluate whether the grouping names the crop's *actual relatives*, not whether it equals the APG clade string. Expected FP without the carve-out: 1/18 on this dimension alone, and the pattern (genus/common grouping vs clade) would recur across the bot set.

**Trap 2 — legitimate N/A numerics on a blend (microgreens-mix).** Treating `ph: []` / empty `days_to_maturity` as "missing/invalid" flags a correct crop: a multi-species blend has no single pH or maturity. **Carve-out (D3):** `[]`/null is N/A, never a violation. Expected FP without the carve-out: 1/18, plus every legitimate perennial-N/A cell.

**The structural FP probe result with carve-outs applied: 0/18 false positives** across D1 (family), D2/D3 (numeric bounds + N/A handling), and D4 (catalogued source). The two traps are the *reason* the carve-outs exist; with them in the rubric, the certified set comes back clean.

**The semantic dimensions (D2 climate, D5 pause-physiology, D6 contradiction, D7 dual-register, D8 gestalt) cannot be probed structurally — they ARE the judge.** Their calibration is a live run: execute the full rubric (all 8 dimensions) against each of the 18 with the actual judge, and **the target is zero high/medium-confidence findings on the 18.** Any such finding is triaged as either (a) a genuine latent issue in a "certified" crop — valuable, route to corrections — or (b) a rubric miscalibration — tighten the carve-out and re-run. Report the per-dimension finding count on the 18 as the published FP rate. **Surface that calibration run's output before pointing the judge at any bot batch** (per the kickoff's "surface the design before running it at volume").

**Recommended FP acceptance bar before the judge is trusted on bot output:** zero high-confidence and zero medium-confidence findings on the 18 after carve-out tuning; low-confidence findings allowed but each must have a written rationale that a human agrees is "worth a glance, not a defect." If a semantic dimension cannot get under that bar without going silent, it ships **advisory-only** (its findings inform but never block) until it can.

---

## 4. The specific checks the remediation routed here — disposition

The remediation (Part B/C) named three checks that "bottomed out at biology/prose" and could not be clean 0-FP deterministic gates. Their disposition in this rubric:

| Routed check | Rubric home | Why it lands here, not in a gate |
|---|---|---|
| calendar-vs-climate (`growing` in a hard-frost month) | **D2** | Needs per-crop cold/hardiness judgment; broccoli grows in cool months, a tender crop must not. Cannot be a shared envelope (B3). |
| rotation-family vs botanical family | **D1** | `family`/`botanical_name` null on 17/18; `rotation.family` free-text + null on 4. Nothing clean to gate; needs botanical knowledge. |
| wrong-crop heat_pause physiology | **D5** | Requires reading basis prose against the crop's identity. Pure semantics. |
| C6 fabricated source chain | **D4** (plausibility half) + out-of-band sweep (content half) | Institution-fit is in-context judgment; URL-content fidelity needs fetching, which is the periodic sweep, not the judge. |
| C7 biologically-impossible crop | **D1+D2+D3+D5+D6+D8** together | The whole rubric *is* the C7 backstop; A33/A34 took the self-contradiction half, the judge takes the wrong-about-the-world half. |
| C16 dual-voice-by-omission | **D7** (as ruling *candidates*, not violations) | The locked "presence IS the declaration" decision stands; the judge proposes the CP/SP ruling inventory, it does not gate. |

---

## 5. How it gates a bot batch — recommendation

**Advisory by default, with one promotion path to blocking.** The judge's findings route to human triage and the corrections log; they do **not** auto-block a batch. Reasoning: the judge is non-deterministic and can hallucinate; making a stochastic reviewer a hard gate would inject false negatives/positives into the cert bar the project has spent the gate work making deterministic. Accuracy-over-velocity here means *catching* errors reliably, not *auto-rejecting* on a probabilistic signal.

**The promotion path:** when a finding *class* proves itself — recurs across batches, is consistently a true defect, and has a deterministic shape — it graduates to the Claude Code lane as a new gate (the A33/A34 precedent). Over time the deterministic bar absorbs everything the judge finds that *can* be made deterministic; the judge keeps only the irreducibly-semantic residue.

**Layering (the full truth-layer stack), in priority order:**
1. **Deterministic self-contradiction gates (A33/A34, built) — hard cert bar.** Cheapest, surest, already done.
2. **This biology-fidelity judge — advisory, per-crop, every bot crop.** Catches wrong-about-the-world that determinism cannot see. Calibrated to 0 FP on the 18 first.
3. **Per-batch source-truth sample — made LOAD-BEARING (mandatory, sized), the remediation's process change.** The judge's D4 plausibility flags *prioritize which rows to sample*, raising the sample's hit rate. The sample stays the human ground truth; the judge makes it sharper, not redundant.
4. **Out-of-band source-URL liveness + content sweep — periodic, for C6.** The judge's D4 suspicions feed the fetch priority queue.

**Sample sizing with the judge in place:** the judge does not let the sample shrink — D4 is plausibility, not content-fidelity, so the human sample remains the only true source-content check. Recommend the sample stay sized to the batch's risk (a fixed floor plus every crop the judge flagged at medium+ confidence on D4/D5), so judge-flagged crops are *always* in the sampled set. The sample size question itself is a Trevor decision; the judge's role is to make sure the rows most likely to be wrong are never the unsampled ones.

---

## 6. Open decisions for Trevor

These are the calls the kickoff's "surface the design before running it at volume" implies, stated explicitly:

1. **Cert-bar placement.** Confirm the judge is **advisory** (recommended) vs blocking. Recommended: advisory, with the A33/A34-style promotion path for proven deterministic patterns.
2. **FP acceptance bar.** Confirm "zero high/medium-confidence findings on the 18 after carve-out tuning" as the trust gate before the judge runs on bot output (recommended), and whether a dimension that cannot clear it ships advisory-only or is held.
3. **Sample interaction.** Confirm the per-batch source-truth sample stays load-bearing and is *augmented* (every medium+ D4/D5-flagged crop is force-included), not replaced, by the judge. Sample floor size is yours to set.
4. **CP/SP ruling inventory (C16).** D7 only produces *candidates*. The actual "which fields MUST be dual-register" ruling inventory is still the separate authoring-lane pass the remediation surfaced — confirm whether that runs before or alongside the bot pipeline.
5. **Live calibration run.** Approve running the full 8-dimension rubric against the 18 as the next step (the structural probe is done and clean; the semantic dimensions need the live pass), with its per-dimension finding count surfaced before any bot batch.

The recommended path throughout is the one that scales the *accuracy* bar long-term: deterministic where it can be, calibrated-advisory where it cannot, with the judge continuously feeding new deterministic gates as patterns harden.
