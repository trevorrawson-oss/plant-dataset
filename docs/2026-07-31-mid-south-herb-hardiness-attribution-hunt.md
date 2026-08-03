# Mid-South herb hardiness attributions: five UAEX lookups

**Date:** 2026-07-31. **Pre-state canonical:** `c6f50a1417a82786356fef764e524641143d41f973dc8f7097eb18454cb3fe5a` (commit `761a128`).
**Kickoff:** `docs/kickoffs/49-herb-hardiness-attribution-hunt.md`.

## The question

Five herb crops (thyme, rosemary, oregano, sage, lavender) credit the University of Arkansas with
**10 attributed sentences across 7 `mid_south` cells** while citing `uada_ext`, a bare domain root,
as their sole source. Does UAEX publish the datum each sentence credits it with?

The worklist was **re-measured** at the pre-state rather than taken from the kickoff table. It
matches exactly: thyme 1, rosemary 2, oregano 1, sage 2, lavender 4.

## What the prose actually is

`mid_south` is the `mid_atlantic` prose with the region words swapped ("Piedmont" to "Ozark
uplands", "Coastal Plain" to "lowland South") and the institution find-and-replaced ("NC State" to
"the University of Arkansas"). The two versions are otherwise identical sentence by sentence.

The citations make the origin unambiguous. Every `mid_atlantic` herb cell anchors to the **real NC
State Plant Toolbox page for the exact species**:

| crop | `mid_atlantic` anchoring URL |
|---|---|
| thyme | `plants.ces.ncsu.edu/plants/thymus-vulgaris/` |
| rosemary | `plants.ces.ncsu.edu/plants/salvia-rosmarinus/` |
| oregano | `plants.ces.ncsu.edu/plants/origanum-vulgare/` |
| sage | `plants.ces.ncsu.edu/plants/salvia-officinalis/` |
| lavender | `plants.ces.ncsu.edu/plants/lavandula-angustifolia/` |

Every `mid_south` herb cell anchors to `https://www.uaex.uada.edu` -- the bare host. There is no
document behind any of the ten claims.

## The NC State pages, read from raw bytes

Fetched with `urllib` + the repo's `extract()`, not through a WebFetch summary:

| crop | NC State `USDA Plant Hardiness Zone` field | our prose claim | verdict |
|---|---|---|---|
| thyme | `5a, 5b ... 9a, 9b` | "zones 5a to 9b" | **exact** |
| oregano | `4a, 4b ... 8a, 8b` | "hardy to about zone 4" | floor exact |
| sage | `4a, 4b ... 8a, 8b` | "zones 4 to 8" | **exact** |
| lavender | `5a, 5b ... 9a, 9b` | "zones 5a to 9b" | **exact** |
| rosemary | `8a, 8b, 9a, 9b, 10a, 10b` | "zone 7 to 8" | **does not match** (see §Rosemary) |

Lavender's disease sentence is likewise verbatim NC State. The Toolbox page reads: *"it is
susceptible to leaf spot and root rot. Root rot is caused by overwatering."* Our cell says "root rot
from overwatering and leaf spot as this species' main threats". That is the same sentence.

Four of the five numbers are NC State's to the character. This is template inheritance, not
independent Arkansas sourcing.

## What UAEX actually publishes

### Documents read (raw bytes, 2026-07-31)

1. `yard-garden/in-the-garden/herbs.aspx` -- "Growing herbs in Arkansas". **No `zone` token.**
2. `.../reference-desk/herbs/thyme.aspx` -- Q&A column. **No `zone` token.**
3. `.../reference-desk/herbs/rosemary.aspx` -- Q&A column. **No `zone` token.**
4. `.../reference-desk/herbs/oregano.aspx` -- Q&A column. **No `zone` token.**
5. `.../reference-desk/herbs/basil.aspx` -- control. **No `zone` token.**
6. `.../in-the-garden/edible-landscaping-herbs.aspx` -- **no `zone`/`hardy to`/`hardiness` token.**
7. `.../reference-desk/plant-selection/perennials.aspx` -- **no `zone`/`hardiness` token.**
8. Pulaski County "Drought Tolerant Plants Suitable for Arkansas Landscapes" (PDF) -- a bare plant
   list with no zones of any kind.
9. **Plant of the Week archive** (`plant-week/archive.aspx`), all **1,197** entry links parsed.
10. The individual Plant of the Week pages named below.
11. `.../reference-desk/herbs/*` sidebar, which **enumerates the entire herb reference desk**:
    Basil, Chives, Oregano, Parsley, Rosemary, Thyme, Wild Garlic/Onion. **No sage. No lavender.**

The `sage.aspx` and `lavender.aspx` reference-desk URLs return HTTP 404. The sidebar enumeration
above is the stronger evidence and is what this finding rests on -- a 404 alone would only be a
guessed URL.

### The Plant of the Week archive is the decisive document

Searching all 1,197 archive links for `salvia|origanum|thymus|lavandul|officinalis|vulgare|rosmarin`
plus the five common names returns **nine** entries. Their Latin names, read off each page:

| archive entry | Latin name on the page | is it our crop? | zone published |
|---|---|---|---|
| Lavender, English | *Lavandula angustifolia* | **YES** | **"hardy from zones 5 to 8"** |
| Spanish Lavender | *Lavandula stoechas* | no | "around 10 degrees Fahrenheit, making them a zone 8 plant" |
| Thyme, Creeping | *Thymus praecox* | no (crop is *T. vulgaris*) | none |
| Hopflower Oregano | *Origanum* x 'Amethyst Falls' | no (crop is *O. vulgare*) | none |
| Willow, Rosemary | ***Salix elaeagnos*** | no -- **a willow** | "zones 4 through 7" |
| Autumn Sage | *Salvia greggii* | no | none |
| Sage, Russian | *Perovskia atriplicifolia* | no | none |
| Pineapple Sage | *Salvia elegans* | no | "zones 8-10" |
| Rose Marvel Sage | *Salvia nemorosa* | no | "zones 4-9" |

There is **no** *Thymus vulgaris*, **no** *Origanum vulgare*, **no** *Salvia officinalis* and **no**
*Salvia rosmarinus* / *Rosmarinus officinalis* anywhere in the archive.

"Willow rosemary" is the trap this table exists to catch: it is a **willow**, *Salix elaeagnos*, and
it is the only UAEX page in the corpus that publishes a zone range next to the word "rosemary".

## Per-crop ruling

The kickoff's §6 warning held: the answer is **not the same for all five**.

**thyme -- credit FALSE.** UAEX publishes no hardiness zone for *Thymus vulgaris*. Its only thyme
material is a Q&A column about creeping thyme as a groundcover (no zone) and a Plant of the Week on
*Thymus praecox* (no zone). "zones 5a to 9b" is NC State's.

**rosemary -- credit FALSE.** UAEX publishes no zone for rosemary. Its reference-desk page says
rosemary is "quite winter hardy in most parts of Arkansas" and repeats a *nursery tag's* "hardy to
10 degrees F" -- a temperature quoted from a plant label, not a published UAEX zone. Note that
UAEX's own framing is **less** marginal than our cell's, not more.

**oregano -- credit FALSE.** UAEX publishes no zone for *Origanum vulgare*. Its oregano page carries
no oregano-specific hardiness statement at all (the paragraph it shares with the thyme page just
lists oregano among "very easy to grow" herbs). The only *Origanum* in the archive is an ornamental
hybrid with no zone.

**sage -- credit FALSE.** UAEX publishes no zone for *Salvia officinalis*. The archive holds four
ornamental salvias; the two that do publish zones give 8-10 (*S. elegans*) and 4-9 (*S. nemorosa*),
neither of which is our "zones 4 to 8".

**lavender -- credit FALSE, and this is the bigger find.** UAEX **does** publish a hardiness range
for our exact species. Its English Lavender Plant of the Week (Gerald Klingaman, 2007-07-20) states:

> "Lavender is hardy from **zones 5 to 8**."

We credit UAEX with "**zones 5a to 9b**". That is NC State's number, and UAEX's real number is
different at the warm end. The same page does support the humidity framing -- *"Wet soils,
especially during wintertime, cause root rot and are responsible for most plant losses. High summer
humidity is not to its liking"* -- but it **never mentions leaf spot**, and "plant profile" is
Toolbox vocabulary, not UAEX's.

## The fix

Purely subtractive: **remove the false credit, keep the horticultural fact.** The `cherry-sweet`
precedent (2026-07-30) and the target shape already present in these same cells -- `thyme`
`mid_south` z7 `grown_as_note_seasoned` reads "Thyme is hardy to about zone 4 to 5" with no
institution, and `mid_atlantic` z8 reads "zone 8 is comfortably inside thyme's zone 5-plus hardy
range" with no institution.

No number changes. No suitability changes. No citation changes. Ten parenthetical or clausal
attributions are deleted and nothing else.

**The retained facts are corroborated by the crops' own records**, so removing the credit strands
nothing:

- `thyme.hardiness_zone_min/max` = 4/9; `thyme_pilot_finding_002` cites "NCSU 5a-9b; PSU/UF/UMD z5-9".
- `rosemary` = 7/10; `rosemary_pilot_finding_004` records 7 as the *hardy-cultivar-inclusive* floor
  ("Hill Hardy z7, Arp z6"), explicitly noting the species is z8 per NCSU.
- `oregano` = 4/9; `oregano_pilot_finding_002` cites "multiple extension/horticulture sources z4-9".
- `sage` = 4/8; `sage_pilot_finding_004` cites "NCSU (4a-8b) + Clemson (4-8)".
- `lavender` = 5/9.

**Why the credit is not simply repointed to NC State:** the `mid_south` cells do not carry
`ncsu_ext` as a source. Writing a reason that names a source the arm does not carry is the exact
failure the hunt-1 guard (`promote_apple_mid_atlantic_bloom_reason.py`) exists to refuse.

## Surfaced, NOT fixed here (each its own ruling)

**1. Lavender's UAEX range is 5 to 8, ours is 5a to 9b.** We keep 5a-9b because it is NC State's and
matches `lavender.hardiness_zone_max` = 9. But if `mid_south` lavender is ever repointed to UAEX's
real Plant of the Week URL (which would fix the bare host and is the one genuine repoint this hunt
found), the z8 cell must change with it: it currently reads "zone 8 sits comfortably inside English
lavender's zone 5 to 9b hardy range", and under UAEX's number zone 8 is **the ceiling**, not
comfortably inside. Filed as `lavender_mid_south_uaex_zone_range_divergence`.

**2. Rosemary's `mid_atlantic` credit has the same shape.** `mid_atlantic` z7 attributes "zone 7 to
8" to NC State, but NC State's Toolbox gives *Salvia rosmarinus* as 8a-10b. The **number** is sound
-- it is our own hardy-cultivar-inclusive floor per `rosemary_pilot_finding_004` -- but NC State
does not publish it, so the credit overstates. Out of scope here (this hunt is `mid_south`), filed
as `rosemary_mid_atlantic_ncsu_zone_attribution`.

## Scope note

Absence here is **document-scoped**, per the standing rule. The claim is: *across the eleven UAEX
sources enumerated above, including the complete 1,197-entry Plant of the Week archive, UAEX
publishes a USDA hardiness zone range for exactly one of these five species -- English lavender --
and that range is 5 to 8.* It is not a claim about every document UAEX has ever published.
