# PLA-8 -- the chemical-cohort close-out round (prepped 2026-08-26, NOT started)

Closes the LAST of the pilot-era (2026-07-22/23) chemical entries. After this the catalog's
safety-bearing surface is fully re-read and the catalog audit can be declared closed.

Instrument already built and validated: `uaidb.py` in this scratchpad parses UC IPM's two-level
hazard grid from RAW HTML. Chlorothalonil (uaiKey=115) is the POSITIVE CONTROL -- it must return
water=H natural_enemies=L bees=medium acute=H chronic=prop65+epa, matching the 2026-08-26 rendered
screenshot, before any other reading is trusted.

Source `ucipm_uaidb` is already minted, so this round adds anchors rather than a source.

| method | uaiKey(s) | note |
| -- | -- | -- |
| copper_fungicide | 123 copper ammonium complex / 124 copper hydroxide / 125 copper octanoate / 126 copper oxychloride sulfate | A CLASS, like pyrethroid. Expect ratings to differ across the four; the caution may have to name which. |
| sulfur | 70 | Single ingredient. Its 90F limit already lives in the entry. |
| neem_oil | 38 neem oil / 91 azadirachtin | Two pages: the whole oil vs the active fraction. Decide which the entry actually describes. |
| spinosad | 64 | Single. Bee toxicity already stated; check the band. |
| insecticidal_soap | 50 potassium salts of fatty acids | 90 (ammoniated salt) is a different material, do not conflate. |
| horticultural_oil | 142 | Single. |
| iron_phosphate_slug_bait | 24 iron phosphate | 8 (ferric sodium EDTA) is the OTHER slug bait chemistry and is more toxic to pets -- check which our entry means. |

## What to check on each, from this round's findings
1. THE BEE BAND, directionally. `bee-precaution-rating-high` grants NO time window;
   `-medium` grants sunset to midnight; `-low` needs no precaution. An entry advising "spray at
   dusk" while sitting in the high band is the exact defect this round fixed on two entries.
2. THE CHRONIC COLUMN. Prop 65 / US EPA listing, or NKR. Two of three conventionals carried a
   listing nobody had written down.
3. Acute band, water quality, natural enemies -- state the mild rating as well as the alarming one.
4. Whether the entry is a CLASS key whose members disagree (copper certainly, neem probably).

## Guard shapes that already exist and should be reused
- `band_violation` -- directional, strict vs middle band.
- `split_violation` -- side-sliced, with `named()` word-boundary matching. REQUIRED for copper:
  "copper hydroxide" contains "copper", so naive containment goes vacuous exactly as it did for
  permethrin inside cypermethrin.
- The six-axis `DISCLOSURE_AXES` table, with the axis list frozen as a LITERAL in the test.
- POST-doctoring drivers: every verify_post guard needs one, because check() refuses upstream.

## Known trap, cost 2 harness runs this round
Eight of twelve first-run survivors were verify_post guards with no driver. Write the
`VerifyPostIsDriven` class FIRST next time, not after the harness reports.
