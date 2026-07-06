# `pet_safe` pilot -- resolved verdicts + evidence (for Trevor's ratify-gate)

**Date:** 2026-07-06. **Status:** authored on scratch, all gates GREEN, **awaiting Trevor ratification before promote.**
**Sources per crop:** ASPCA Toxic/Non-Toxic Plants list (now catalogued T1, pet-toxicity scope) + NCSU Plant Toolbox (`.edu`), both fetched live via WebFetch 2026-07-06 and self-verified in the main loop.

## The headline: 3 of 6 provisional expectations SHIFTED on verification

This is the point of a verify-don't-lift pilot. The existing prose conflates pet toxicity with human edibility/allergy; checking the real pet authorities changed three calls:

| Crop | Provisional (spec) | **Verified** | Why it shifted |
|---|---|---|---|
| rosemary | safe | **safe** | (held) ASPCA: non-toxic to cats/dogs/horses |
| chives | toxic | **toxic** | (held) ASPCA + NCSU: toxic to cats/dogs/horses |
| cherry-tomato | caution | **caution** | (held) part-conditional: ripe fruit safe, foliage toxic |
| sweet-pea | toxic | **caution** | ASPCA (genus *L. latifolius*) = non-toxic to cats/dogs, toxic to **horses only**; NCSU (*L. odoratus*) = **seeds** poisonous, lathyrism, "low" severity. Not a blanket toxic -- a seed/pod, horse-weighted caution. |
| chamomile | toxic | **caution** | Species mismatch: ASPCA's toxic entry is *Anthemis nobilis* (Roman); our crop is German *Matricaria chamomilla*, which NCSU rates "low severity" (contact dermatitis / oral swelling), no pet-species tag. |
| borage | safe/caution | **toxic** | Both ASPCA AND NCSU tag it problem-for-cats/dogs/horses; NCSU names the pyrrolizidine alkaloids (liver/lung, potentially carcinogenic). The human PA caution and the pet toxicity point the same way. |

Result: a genuinely diverse spread -- **safe 1, toxic 2, caution 3** -- and every "can't lift the prose" trap fired.

## Per-crop detail (exactly what was authored)

### rosemary -> `safe`
- **note:** "A culinary herb the ASPCA lists as non-toxic to cats, dogs, and horses."
- **sources:** aspca -> https://www.aspca.org/pet-care/animal-poison-control/toxic-and-non-toxic-plants/rosemary
- ASPCA: Rosmarinus officinalis, Non-Toxic to Dogs / Cats / Horses. This closes the rosemary R3 gap (its `.edu` set never carried the toxicity fact; ASPCA is the affirmative source).

### chives -> `toxic` (cats, dogs, horses)
- **note:** "An allium: toxic to cats, dogs, and horses, and it can damage their red blood cells."
- **sources:** aspca (.../chives) + ncsu_ext (plants.ces.ncsu.edu/plants/allium-schoenoprasum/)
- ASPCA: Allium schoenoprasum, toxic dogs/cats/horses, N-propyl disulfide, hemolytic anemia. NCSU: problem for cats/dogs/horses. Serious systemic principle -> `toxic`.

### sweet-pea -> `caution` (horses) -- **JUDGMENT CALL, please confirm**
- **toxic_parts:** "seeds and pods"
- **note:** "The seeds and pods are poisonous and can cause lathyrism; the ASPCA lists sweet pea as toxic to horses, so keep seedpods away from pets."
- **sources:** ncsu_ext (lathyrus-odoratus/, our exact species) + aspca (.../sweet-pea, genus L. latifolius)
- **The call:** ASPCA rates dogs/cats NON-toxic, horses toxic; NCSU says seeds poisonous (lathyrism), "low" severity, no species tag. I read this as a **part-specific, horse-weighted caution**, not a blanket `toxic`. Alternative: `toxic` with affects=["horses"]. Also note the species nuance (ASPCA entry is the congener L. latifolius; NCSU covers our L. odoratus directly).

### chamomile -> `caution` (cats, dogs, horses) -- **JUDGMENT CALL, please confirm**
- **note:** "German chamomile is a mild irritant that can cause contact dermatitis or oral swelling; the related Roman chamomile is listed by the ASPCA as toxic to cats, dogs, and horses."
- **sources:** ncsu_ext (matricaria-chamomilla/, our German species) + aspca (.../chamomile, Roman)
- **The call:** ASPCA's toxic listing is *Anthemis nobilis* (Roman chamomile), a different species from our German *Matricaria chamomilla*. NCSU (German) rates it low-severity contact dermatitis / oral swelling, no pet-species tag. So a same-species `toxic` is NOT established; I authored `caution` with a note that honestly distinguishes German (mild) from Roman (ASPCA toxic). Alternative: `toxic` on the genus-level read.

### cherry-tomato -> `caution` (cats, dogs, horses)
- **toxic_parts:** "leaves, stems, and unripe fruit"
- **note:** "Ripe tomatoes are fine, but the leaves, stems, and unripe fruit are toxic to cats, dogs, and horses."
- **sources:** aspca (.../tomato-plant) + ncsu_ext (solanum-lycopersicum/)
- ASPCA: toxic (solanine), "ripe fruit is non-toxic." NCSU: #poisonous + problem for cats/dogs/horses, poisonous parts = leaves/stems only. The exemplary part-conditional `caution` -- the fruit you grow it for is safe; keep pets off the foliage.

### borage -> `toxic` (cats, dogs, horses) -- **JUDGMENT CALL, please confirm**
- **note:** "Contains pyrrolizidine alkaloids and is listed as a problem for cats, dogs, and horses, so keep pets from grazing on it."
- **sources:** aspca (.../borage) + ncsu_ext (borago-officinalis/)
- **The call:** Both ASPCA and NCSU tag it problem-for-cats/dogs/horses. ASPCA's acute signs are mild (vomiting/diarrhea/dermatitis from tannins/mucilage), but NCSU names the pyrrolizidine alkaloids (liver/lung, potentially carcinogenic) -- an organ-damaging principle -> I authored `toxic`. Alternative: `caution` if you weight the mild acute signs over the PA principle.

## The enum-mapping rule this pilot establishes (for the 108-crop rollout -- please ratify)

ASPCA is a binary (toxic / non-toxic); our enum has three values. The pilot forces a mapping rule. Proposed:
- **`safe`** = ASPCA non-toxic to all three species (affirmative source).
- **`toxic`** = a serious / systemic toxic principle (hemolysis, solanine, organ-damaging PAs, neuro/cardiac) with a same-or-close-species pet tag. (chives, borage)
- **`caution`** = part-conditional (edible part safe, only foliage/seeds toxic: tomato, sweet-pea), OR low-severity irritant (mild GI / contact dermatitis: the ratified "mild" bucket), OR species-uncertain / not-established (chamomile German-vs-Roman).

This is the precedent the rollout applies 108 times, so it is worth an explicit yes/adjust.

## New gate ruling added this session (register_completeness) -- **please sign off**

Adding `pet_safe` introduced two novel user-facing string keys. `register_completeness_gate` correctly HALTED on them (the STOP-AND-ASK design). Encoding your ratified "single concise note, USER-FACING-CATEGORICAL" decision, I added two `ruled_categorical` rules:
- `pet_safe.note` -> USER-FACING-CATEGORICAL (single-form icon tooltip; also exempts it from the C11c laundering check, since `note` is a laundering key).
- `pet_safe.toxic_parts` -> USER-FACING-CATEGORICAL (which parts are toxic).

TDD: added a RED test (`pet_safe.note`/`toxic_parts` flagged) -> added the rules -> GREEN; live canonical still passes register_completeness (0 regression). This ruling should also be recorded in `register_bearing_field_inventory_v1_0.md` at promote.

## Gate state (scratch, all GREEN)
- `pet_safe_gate --slugs <the 6>`: safe=1 toxic=2 caution=3, unset=0, exit 0.
- `whole_crop_gate` on all 6: exit 0 each (pet_safe survives the full cert suite).
- `register_completeness_gate` dataset-wide on scratch: exit 0.
- SHA-guard preview: exactly the 6 slugs + `source_catalog.aspca` changed; all other top-level keys byte-identical; certified count 114 -> 114 (amend-not-recert).
