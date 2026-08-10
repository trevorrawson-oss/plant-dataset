# PLA-156 lead, read out: does B577's one Corn row cover field-corn, popcorn, flint-corn?

2026-08-10. Base canonical `72284f02` (untouched -- this is a decision-ready read-out, not a promote).
Companion to the ledger correction in `docs/2026-07-06-url-liveness-ledger.json` and PLA-156's owed #4.

## The document, actually read

`B577PlantingChart.pdf` ("Home Garden Planting Chart", Bulletin 577, reviewed March 2022) is a
31-row vegetable table. It has exactly ONE corn row:

```
Corn   80-100   Mar. 15-June 1 (spring)   June 1-July 20 (fall)
```

Footnote: dates are approximate for MIDDLE Georgia; South Georgia may plant ~2 weeks earlier in
spring and somewhat later in fall; North Georgia ~2 weeks later in spring.

In a home-garden vegetable guide the unqualified Corn row is sweet corn. 38 canonical nodes cite
`uga_b577`; the corn-family live-layer nodes split as below.

## Adjudication, one row per decision

| # | Claim (sole source `uga_b577`) | What the chart says | Verdict |
|---|---|---|---|
| 1 | sweet-corn se_gulf: all 11 nodes. z8 `plant_out` Mar 15 - Jul 20; z9/z10 Mar 1 - Aug 5; succession blocks; harvest "75 to 85 days" prose; DTM [60,90] | Spring Mar 15-Jun 1 + fall Jun 1-Jul 20 = a continuous Mar 15-Jul 20 sowing span; South-Georgia note moves z9/z10 starts to ~Mar 1 and stretches the tail (~Aug 5); chart DTM 80-100 overlaps the claimed band | **SUPPORTED.** The chart carries the windows to the day, including the z9/z10 2-week advance via its own footnote. No action. |
| 2 | field/pop/flint `direct_sow` anchors + 9 zone `plant_out` cells: "Mar 15 - Apr 30", warm-soil-after-last-frost | Corn spring window OPENS Mar 15. Sowing timing for Zea mays is species-level (soil temperature), not variety-level | **START SUPPORTED; the Apr 30 cutoff is OURS, not the chart's** (chart runs to Jun 1). The narrowing is a full-season derivation, defensible as a subset of the sourced window, but it is not a published datum. Decision: accept-as-subset (recommended) or annotate the cutoff's basis. |
| 3 | field-corn `harvest_start`/`harvest_end` prose "110 to 120 days" + zone harvest "Jul 5 - Aug 30" | Chart says 80-100, and that row is sweet corn | **NOT SUPPORTED by the sole cited source.** The DTM figure appears nowhere in B577. |
| 4 | popcorn harvest prose "100 to 110 days" + cure "to 13 to 14 percent moisture" + zone harvest "Jun 25 - Aug 20" | Same single 80-100 row; no popcorn row, no moisture datum | **NOT SUPPORTED.** DTM and the popping-moisture figure are both un-carried by B577. |
| 5 | flint-corn harvest prose "90 to 110 days" + zone harvest "Jul 5 - Aug 30" | Same | **NOT SUPPORTED.** |

Rows 3-5 are `right-document-wrong-claim` in citation form: the sow-date anchor legitimately
points at B577, and the citation then rides along onto harvest cells whose quantitative content
(grain-corn DTM, cure moisture) B577 does not publish. The values themselves are plausible
variety-class figures; the defect is attribution, not (on current evidence) the data.

## Decisions for Trevor (canonical untouched pending ruling)

1. **Rows 3-5 (the real defect, 6 planting nodes + 9 zone harvest strings across 3 crops):**
   source a grain-corn/popcorn DTM document (T1) and add it as the harvest-cell anchor, or
   re-scope `uga_b577` on those crops to the sow-window claims only. Either way the harvest
   prose needs a source that actually publishes the numbers.
2. **Row 2 (minor):** rule whether a subset plant-out window needs its narrowing basis noted.
3. No action on sweet corn.

Not repeated here but related: the USCRN validation already marks field/pop/flint `direct_sow`
`offset_band: misaligned` (stored Mar 15 vs soil-60°F median Feb 28) while sweet-corn reads
`aligned` -- consistent with these three crops' timing being copied rather than independently
anchored.
