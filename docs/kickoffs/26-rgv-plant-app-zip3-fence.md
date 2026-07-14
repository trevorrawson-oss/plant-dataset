# Kickoff: RGV plant-app 785xx ZIP3 fence (roadmap item 2, paired with item 3)

**For:** a fresh plant-app session.
**From:** the plant-dataset session that shipped the real Rio Grande Valley region.
**Status:** committed, NOT YET pushed (Trevor confirms push before you sync); no plant-astro bump
this session.

## Sync/rebuild off this canonical

```
crops_data_final.json  sha256 = d0832254e3a1e9a520bcc3629fd91f347dea28206a6e2e063072e946b0465fa8
dataset commit = 4e2e9e7   (bump/sync assets off this, once pushed)
```

## The headline: a real `rgv` region now exists, dataset side is done

The dataset shipped a real, authored Rio Grande Valley / subtropical South Texas region,
`rgv` (`zone_span` `["9","10"]`), across all 108 certified region-carrying crops. This retires
the se_gulf z10 interim from the 2026-07-12 zone-span reconciliation (kickoff #24), which had
RGV's 95 TX z10 ZIPs riding borrowed Gulf-coast dates. That interim is gone. The remaining gap
is entirely app-side: nothing in the app yet points RGV ZIPs at `rgv` instead of `se_gulf`.

## What you need to do

### 1. `REGION_STATES`: map `rgv` to TX

Add `rgv` to the region-to-state map, mapped to Texas, the same shape as the existing region
entries (`se_gulf`, `low_desert_az`, etc).

### 2. `ZIP3_REGION_HINT`: fence 785xx ONLY to `rgv`

Add a ZIP3 hint that sends `785xx` to `rgv`. **Fence 785xx only, not all TX z10.**

Of the roughly 96 TX z10 ZIPs, only 56 are in 785xx (the actual Rio Grande Valley: McAllen,
Edinburg, Mission, Pharr, Weslaco, Harlingen, Brownsville, San Benito). The other roughly 40 are
784/783 (Corpus Christi and the Coastal Bend) and 775 (the Galveston barrier islands). Those are
frost-prone coastal climates, genuinely different from the RGV's frost-free subtropical
character, and they must stay on `se_gulf`. Fencing all of TX z10 to `rgv` would misassign
Corpus Christi and Galveston to a region built for a warmer, frost-free climate; that is a
regression, not an improvement.

785xx also carries about 12 z9 ZIPs (the inland Valley, away from the immediate river/coast
moderation). Since `rgv`'s `zone_span` is `["9","10"]`, both zones resolve once the ZIP3 fence
is in place; you do not need a separate z9 carve-out.

### 3. Verify the regions.json sync path picks up `rgv`

After your build/sync step regenerates `assets/data/regions.json` from the dataset, confirm the
new `rgv` region actually appears (region id, label, zone_span, and the per-zone calendar rows).
`resolveFromZip` reads `zone_span` at runtime, so once `rgv` is in the synced data and the ZIP3
fence is wired up, no further app code should be needed for the region to resolve. plant-astro
consumes the region the same way (reads spans at runtime, unions across crops); it will pick up
`rgv` automatically the next time its submodule is bumped to this dataset commit, which is a
separate step owned by the plant-astro session, not this one.

## Honesty flags, do not "correct"

- The 785xx-only fence is deliberate, not a simplification. Corpus Christi (783/784) and
  Galveston's barrier islands (775) are genuinely frost-prone despite sharing a USDA zone label
  with the RGV; they belong on `se_gulf`, not `rgv`.
- If you find other TX ZIP3s that plausibly belong in the RGV footprint (Starr, Hidalgo, Cameron,
  Willacy county ZIP3s beyond 785), treat that as a scope question for Trevor rather than
  expanding the fence unilaterally; 785xx is the documented, TAMU AgriLife-aligned Rio Grande
  Valley footprint used when the region was authored.

## Definition of done

RGV ZIPs (785xx, both z9 and z10) resolve to `rgv` in the app, not the retired `se_gulf`
interim; Corpus Christi/Coastal Bend (783/784) and Galveston (775) still resolve to `se_gulf`;
`REGION_STATES` and `ZIP3_REGION_HINT` both updated; the regions.json sync path verified end to
end for a sample RGV ZIP (e.g. a McAllen 785xx ZIP resolves to `rgv`, not `se_gulf` or a bare
zone label).
