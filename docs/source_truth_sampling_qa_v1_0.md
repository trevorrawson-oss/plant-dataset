# Source-Truth Sampling QA, v1.0 (the standing per-batch correctness process)

**Status:** LOCKED process for the scale phase (~105 remaining crops).
**Created:** 2026-06-24 (Phase C of the post-roster GS-arc audit).
**Companion tool:** `tools/source_truth_sample.py` (+ `test_source_truth_sample.py`).
**Worked example:** `plant-astro/docs/gs-arc-source-truth-qa-2026-06-24.md`.

---

## 1. The problem this solves (and why it is NOT a gate)

The gates check **coherence** (the calendar matches the authored windows; fields cohere) and now
**display-readiness** (the cards' fields are present). Neither checks **source-truth**: do the
authored regional planting/harvest **dates** match real-world regional reality?

Source-truth is **irreducibly per-cell** and **un-gateable**. A gate can only compare the dataset to
itself; it cannot know that "lettuce, Central Valley, fall" really runs Sep-Oct. The only check is to
compare a sample of cells against live Tier-1 (university extension) planting calendars. So this is a
**sampled release-QA step, never a gate.** It is the deliberate human/agent-in-the-loop bottleneck the
audit identified: bots author and gates catch structure, but correctness must be spot-checked.

> **Do not try to turn this into a gate.** The audit already proved that the obvious gate ideas
> false-positive the subtlest crops (photoperiod onion, continuous-succession lettuce) to catch ~1 real
> nit. See the parent audit §5 "REJECTED". Sample it; don't gate it.

---

## 2. The loop (per batch of newly-built crops)

```
  extract  ->  fan out  ->  verify-before-fix  ->  route the fix  ->  re-run
  (tool)       (agents)     (the deriver oracle)    (authoring lane)   (gates)
```

### Step 1 -- EXTRACT the sample (deterministic)
Run `tools/source_truth_sample.py` to dump each candidate cell's **EFFECTIVE plant window**
(`plant_out` string UNION `calendar[]` plant tokens) + harvest string + heat/cold pauses, grouped by
region. Example:

```
python3 tools/source_truth_sample.py --regions ca_desert low_desert_az --crops carrot lettuce-leaf
```

**The effective-window union is load-bearing.** Region-primary cells store sow windows in the
`calendar[]` plant tokens, not in `plant_out` (often null). A verifier that reads only `plant_out`
will hallucinate "a harvest with no planting behind it" -- the exact false positive that was retracted
in the parent audit. The tool unions both for you; keep it that way.

### Step 2 -- FAN OUT region-scoped verification agents
One agent per extension-service territory (so each becomes fluent in one source's planting calendar):

| Cluster | Regions | Canonical T1 source |
|---|---|---|
| California | ca_interior, ca_north_coast, ca_south_coast | UC ANR / UCCE Master Gardener planting calendars (Sacramento EHN 11, Marin) |
| Desert SW | ca_desert, low_desert_az, warm_arid | **UArizona AZ1005** (low-desert), UC Desert Valleys, NMSU |
| SE / Gulf / FL / HI | se_gulf, fl_peninsula, hawaii_tropical | **UF-IFAS SP103/VH021**, UGA C963, Clemson, UH-CTAHR |
| Northern tier | northern_tier (z3-z7) | **UMN Extension**, USU, UNH, Cornell |

Each agent: WebFetch the region's planting calendar, verify the effective plant + harvest windows,
return a per-cell verdict (**MATCH** / **MINOR** ~1 month / **WRONG** wrong-season-or-unreachable) with
the exact T1 source URL and a corrected window for anything non-MATCH. **T1 only** (no seed companies,
no almanacs). Give every agent the semantics below so they don't false-positive.

### Step 3 -- VERIFY every finding before acting (the false-positive firewall)
The QA itself can be wrong (the parent audit produced a broccoli false positive). Before treating any
agent finding as real, the releaser re-checks it against the full data representation:
- **Effective plant window**, not one field (`plant_out` UNION calendar tokens).
- **`heat_pause` / `cold_pause` mean "too {hot,cold} to SOW", NOT "no harvest".** A month can be a
  pause AND a harvest month (split spring+fall crops). Never flag harvesting-during-a-pause.
- **Use `derive_annual_calendar` (annual_calendar.py) as an oracle.** Apply the proposed corrected
  window and check what calendar it derives: if the stored calendar becomes re-derivable, the fix is a
  clean coherence repair with no cascade; if plant tokens move, it cascades to `successions_realized`
  and harvest extent (authoring-grade).

### Step 4 -- ROUTE the fix to the right lane
- **Clean coherence repair** (no plant-token change, e.g. a harvest string that over-claims a window
  the calendar already excludes): a structural nit; Claude Code can apply it directly.
- **Window-shape change** (plant tokens move -> calendar + `successions_realized` + harvest cascade):
  authoring; hand the exact sourced corrected window to the claude.ai authoring lane (it owns the
  method-resolution: `*_month_resolution` / frost resolution) so the cascade is recomputed coherently.
- **Modeling/product call** (e.g. a tropical year-round cell shown as a narrow representative window):
  not a defect; flag for a product decision, do not "fix".
- Batch the routed corrections into the next combined dataset release (one SHA, one submodule bump);
  do not fragment the dataset with one-cell releases unless a fix is urgent and self-contained.

### Step 5 -- RE-RUN gates after the corrections land, and record
`whole_crop_gate` on every touched crop + `release_verify` + the no-regression net, then the normal
release ceremony. Append the sample's findings doc to the release record.

---

## 3. Sampling strategy at scale (risk-ordered, rotating)

You cannot check every cell every batch. Per batch:
- **Cover ~25-30% of the batch's annual cells**, weighted to the **highest-risk classes** (where
  Layer-2 errors cluster): warm/desert **winter-inverted** calendars (zones 8-11), **succession
  splits** (spring+fall), the **tightest cold-zone** seasons (z3-z4 reachability), and **photoperiod**
  onion windows (short vs intermediate vs long day).
- **Spread across crops** within each region cluster (don't deep-dive one crop and skip the rest).
- **Rotate** the specific cells sampled across batches so coverage compounds over time.
- Trees/berries/indoor crops use other models -- sample their harvest windows separately, lighter
  (the parent audit found tree/berry harvest 3/3 MATCH; lower risk than annual regional windows).

---

## 4. What scales well vs the bottleneck

- **Scales:** the deterministic extract, the gate-able structural/display classes (Phases A+B armor),
  and -- proven across two audits -- the authoring of accurate regional dates (the hard part is
  correct by sample).
- **Bottleneck:** this per-batch source sample + a render eyeball. Parallel region agents carry most
  of it, but it is bounded, non-negotiable, and not a gate, because the calendars are the crux of the
  product ("a grower opens THEIR cell and it's right").
