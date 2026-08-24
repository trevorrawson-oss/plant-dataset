#!/usr/bin/env python3
"""PLA-8: the iron-phosphate slug-bait safety absolute, in the CROP prose. Content + rationale.

THE DEFECT. Eight `organic_treatment_*` fields across five crops assert that iron-phosphate slug
bait IS SAFE, without qualification:

    basil        beginner   "Iron phosphate slug pellets are safe to use around food plants."
    lettuce-leaf beginner   "... approved for organic gardens and safe around pets and wildlife"
    lettuce-leaf seasoned   "... approved for organic use and safe around pets and wildlife"
    swiss-chard  beginner   "... an iron-phosphate slug bait, which is safe around pets and wildlife"
    arugula      beginner   "... an iron-phosphate slug bait, which is pet-safe"
    arugula      seasoned   "... iron-phosphate baits (pet-safe) ..."
    bok-choy     beginner   "... an iron-phosphate slug bait, which is pet-safe"
    bok-choy     seasoned   "... iron-phosphate baits (pet-safe) ..."

This is the PLA-253 class: an unhedged safety absolute in consumer copy. `arugula` and `bok-choy`
are BYTE-IDENTICAL, which is the template-inheritance pattern -- one authoring template carried the
claim to a sibling crop.

WHAT THE SOURCE ACTUALLY SAYS. UC IPM Pest Note 7427 (fetched and read 2026-08-24) says iron
phosphate baits "have the advantage of being SAFER for use around children, domestic animals, birds,
fish, and other wildlife", and separately that "Metaldehyde baits are particularly poisonous to dogs
and cats". The page NEVER calls iron phosphate simply "safe". The claim is COMPARATIVE against
metaldehyde, and the comparison is the whole content of it. The page also notes baits are "toxic to
ALL snails and slugs, including the predatory decollate snail and native species", so a bait is a
pesticide with real non-target effects, not a benign product.

THE CATALOG ALREADY HAD THIS RIGHT. `control_methods.iron_phosphate_slug_bait` says "safer for use
around children, pets, birds, fish, and other wildlife than metaldehyde" and carries a `cautions`
entry, "Even a lower-risk bait is still a pesticide". The crop prose overstated what the catalog and
the source both state carefully. The fix aligns the crop prose to them; it does not soften a
sourced claim, it restores the qualifier the source carries.

WHY ALL EIGHT AND NOT THE TWO THAT SURFACED. Two fields (basil, swiss-chard) surfaced while reading
the PLA-8 batch-1 ladders. A scan of all 23 iron-phosphate mentions in crop prose found six more of
the identical class on three crops OUTSIDE that batch. Correcting a claim in one field and leaving
it live in the others is a documented failure mode in this repo. The remaining 15 mentions (sage,
marigold, nasturtium, calendula, sweet-alyssum, viola, sweet-pea, and the two already-careful fields
noted below) make NO safety claim and are deliberately untouched.

DELIBERATELY NOT FIXED HERE, recorded instead:
  * basil `organic_treatment_seasoned` says the pellets are "low-risk to NON-TARGET ORGANISMS".
    Against pn7427's "toxic to all snails and slugs, including ... native species" that is
    imprecise, since native snails are non-target. It is a different claim from the safety
    absolute this promote addresses, so it is left alone rather than swept in.
  * The `find_it_beginner` and `cautions` fields on the catalog method are already correct.
"""

# (crop slug, problem name, field, exact old text, exact new text)
# `old` is matched EXACTLY and in full. A miss is a REFUSAL, never a silent skip.
EDITS = [
    (
        "basil", "Slugs and snails", "organic_treatment_beginner",
        "Set out beer traps at ground level. Iron phosphate slug pellets are safe to use around "
        "food plants.",
        "Set out beer traps at ground level. Iron phosphate slug pellets are approved for organic "
        "gardens and carry less risk around pets and wildlife than the older metaldehyde baits, "
        "though they are still a pesticide, so scatter them on the soil and follow the label.",
    ),
    (
        "lettuce-leaf", "Slugs & snails", "organic_treatment_beginner",
        "Set beer traps with the rim level with the soil so the slugs fall in and cannot climb out, "
        "and refresh them every couple of days. Sprinkle diatomaceous earth in a ring around "
        "vulnerable plants, but remember it stops working once it gets wet and needs reapplying "
        "after rain or watering. Hand-pick them after dark with a flashlight, when they are out "
        "feeding. An iron-phosphate bait (sold as Sluggo and similar) is approved for organic "
        "gardens and safe around pets and wildlife; it stops the slugs feeding so they die within a "
        "few days. Scatter it in the evening after watering, when slugs are most active, for the "
        "best results.",
        "Set beer traps with the rim level with the soil so the slugs fall in and cannot climb out, "
        "and refresh them every couple of days. Sprinkle diatomaceous earth in a ring around "
        "vulnerable plants, but remember it stops working once it gets wet and needs reapplying "
        "after rain or watering. Hand-pick them after dark with a flashlight, when they are out "
        "feeding. An iron-phosphate bait (sold as Sluggo and similar) is approved for organic "
        "gardens and carries less risk around pets and wildlife than the older metaldehyde baits, "
        "though it is still a pesticide; it stops the slugs feeding so they die within a few days. "
        "Scatter it in the evening after watering, when slugs are most active, for the best results.",
    ),
    (
        "lettuce-leaf", "Slugs & snails", "organic_treatment_seasoned",
        "Set beer traps with the rim at soil level so they fall in and cannot climb back out, and "
        "refresh them every couple of days. Ring vulnerable plants with diatomaceous earth, "
        "remembering it stops working once wet and needs reapplying after rain or irrigation. "
        "Hand-pick after dark with a flashlight, when they are out feeding. Iron phosphate bait "
        "(sold as Sluggo and similar) is approved for organic use and safe around pets and "
        "wildlife; it disrupts their gut so they stop feeding and die within a few days. Scatter it "
        "in the evening after watering, when slugs are most active, for the best effect.",
        "Set beer traps with the rim at soil level so they fall in and cannot climb back out, and "
        "refresh them every couple of days. Ring vulnerable plants with diatomaceous earth, "
        "remembering it stops working once wet and needs reapplying after rain or irrigation. "
        "Hand-pick after dark with a flashlight, when they are out feeding. Iron phosphate bait "
        "(sold as Sluggo and similar) is approved for organic use and is safer around children, "
        "pets, birds, fish, and other wildlife than metaldehyde, though it remains a pesticide; it "
        "disrupts their gut so they stop feeding and die within a few days. Scatter it in the "
        "evening after watering, when slugs are most active, for the best effect.",
    ),
    (
        "swiss-chard", "Slugs and snails", "organic_treatment_beginner",
        "Pick them off after dark by flashlight, set out shallow dishes of beer to trap them, or "
        "scatter an iron-phosphate slug bait, which is safe around pets and wildlife. Remove hiding "
        "spots like boards and dense debris near the plants.",
        "Pick them off after dark by flashlight, set out shallow dishes of beer to trap them, or "
        "scatter an iron-phosphate slug bait, which carries less risk around pets and wildlife than "
        "the older metaldehyde baits. It is still a pesticide, so put it on the soil and follow the "
        "label. Remove hiding spots like boards and dense debris near the plants.",
    ),
    (
        "arugula", "Slugs and snails", "organic_treatment_beginner",
        "Hand-pick at night or after rain, set out shallow traps, and use an iron-phosphate slug "
        "bait, which is pet-safe. Reduce damp hiding places and water in the morning so the surface "
        "dries by night.",
        "Hand-pick at night or after rain, set out shallow traps, and use an iron-phosphate slug "
        "bait, which carries less risk around pets than the older metaldehyde baits. Reduce damp "
        "hiding places and water in the morning so the surface dries by night.",
    ),
    (
        "arugula", "Slugs and snails", "organic_treatment_seasoned",
        "Hand-pick after dark or rain, use shallow traps and iron-phosphate baits (pet-safe), and "
        "remove daytime shelter; morning watering lets the surface dry before they feed.",
        "Hand-pick after dark or rain, use shallow traps and iron-phosphate baits (safer around "
        "pets than metaldehyde, though still a pesticide), and remove daytime shelter; morning "
        "watering lets the surface dry before they feed.",
    ),
    (
        "bok-choy", "Slugs and snails", "organic_treatment_beginner",
        "Hand-pick at night or after rain, set out shallow traps, and use an iron-phosphate slug "
        "bait, which is pet-safe. Reduce damp hiding places and water in the morning so the surface "
        "dries by night.",
        "Hand-pick at night or after rain, set out shallow traps, and use an iron-phosphate slug "
        "bait, which carries less risk around pets than the older metaldehyde baits. Reduce damp "
        "hiding places and water in the morning so the surface dries by night.",
    ),
    (
        "bok-choy", "Slugs and snails", "organic_treatment_seasoned",
        "Hand-pick after dark or rain, use shallow traps and iron-phosphate baits (pet-safe), and "
        "remove daytime shelter; morning watering lets the surface dry before they feed.",
        "Hand-pick after dark or rain, use shallow traps and iron-phosphate baits (safer around "
        "pets than metaldehyde, though still a pesticide), and remove daytime shelter; morning "
        "watering lets the surface dry before they feed.",
    ),
    # sage was MISSED by the iron-phosphate scan and caught by the roster-wide post-state guard:
    # its BEGINNER field says "pet-safe bait" without naming the product, while its SEASONED field
    # on the same problem names iron-phosphate bait. Same product, same claim, ninth field.
    (
        "sage", "Slugs and snails", "organic_treatment_beginner",
        "Pick them off after dark, clear away damp hiding spots, and use slug traps or pet-safe "
        "bait near young plants.",
        "Pick them off after dark, clear away damp hiding spots, and use slug traps or an "
        "iron-phosphate bait, which carries less risk around pets than the older metaldehyde "
        "baits, near young plants.",
    ),
]

# The banned constructions, as they appear in THESE fields.
BANNED = (
    r"\bpet-safe\b",
    r"\bis\s+safe\s+(?:around|to\s+use)\b",
    r"\bare\s+safe\s+(?:around|to\s+use)\b",
    r"\band\s+safe\s+around\b",
    r"\bwhich\s+is\s+safe\b",
)

# The banned scan runs roster-wide, but only over prose IN THIS PROMOTE'S CLASS -- a string that
# talks about a slug or snail bait. Scoping it this way is deliberate: a promote's post-state guard
# must assert only what the promote actually establishes. An unscoped scan for "which is safe" also
# catches the Bt class below, which this promote does NOT fix, so an unscoped guard would either
# block a correct promote or pressure a silent widening into someone else's arc.
SCOPE = r"iron.?phosphate|pet-safe|slug\s+bait|slug\s+pellets|snail\s+bait|slug\s+traps\s+or"

# OUT OF SCOPE, MEASURED AND RECORDED, NOT FIXED HERE.
#
# A separate unhedged safety absolute rides on Bt in NINE crops' `organic_treatment_beginner`:
#   kale, spinach, arugula, bok-choy, cauliflower, cabbage, kohlrabi, brussels-sprouts, collards
#   "Spray Bt, which is safe and targets only caterpillars, ..."
# PLA-253 removed and hedged this absolute in the CATALOG method `bt`, whose beginner prose now
# carries the eye/skin irritation caution and "it does not tell good caterpillars from bad, so
# spray only the plants that have a pest problem". That remediation never reached the crop prose,
# so nine crops still publish the absolute the arc was opened to remove. It is a different product
# and a different claim from the slug bait, and folding it in would silently reopen a closed arc.
# Note the substantive half too: "targets only caterpillars" is literally true and consumer-
# misleading, because the non-target risk IS other caterpillars, i.e. butterfly larvae.
BT_ABSOLUTE_CROPS = ("kale", "spinach", "arugula", "bok-choy", "cauliflower",
                     "cabbage", "kohlrabi", "brussels-sprouts", "collards")
#
# ALSO deliberately untouched, because reading them shows they are NOT the class:
#   cayenne-pepper, habanero  "though not completely safe where the fly is around" -- a NEGATED
#                             construction, i.e. already a hedge, and correct as written.
#   persimmon (x2), pawpaw    "a harmless nuisance" / "harmless level" / "leaf nibbling is
#                             harmless" -- describes a DAMAGE LEVEL, not a product's safety.

# A fix is not proved by the absence of a word. Every rewritten field must ALSO carry the
# comparative that replaced it -- this is the positive control (PLA-215 bar item 3).
REQUIRED_COMPARATIVE = r"\b(?:less\s+risk\s+around|safer\s+around)\b"

SOURCE_READ = {
    "id": "ucanr_ext",
    "url": "https://ipm.ucanr.edu/PMG/PESTNOTES/pn7427.html",
    "read": "2026-08-24",
    "quote": "have the advantage of being safer for use around children, domestic animals, "
             "birds, fish, and other wildlife",
}
