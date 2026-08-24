#!/usr/bin/env python3
"""PLA-8 catalog round 4: mint `exclusion_fencing`. Base 76c70488.

WHY, AND HOW IT WAS FOUND. A batch-2 authoring agent hit a wall on sweet-corn/raccoons: the crop's
highest-severity problem, whose control is a two-wire electric fence, had NO expressible rung. It
correctly refused to pad and emitted `"control_ladder": []` rather than reach for a near-miss key.

MEASURED, not assumed: only SEVEN methods are legal on a `vertebrate` problem -- `bird_netting`,
`bird_scare_deterrents`, `prompt_harvest`, and the four `any` culturals. Both catalog occurrences of
the word "fence" are METAPHORICAL (`floating_row_cover`: "a physical fence: the moths, flies, and
beetles cannot reach the plants"; `bird_netting`: "a physical fence that keeps birds from reaching
the fruit"). Nothing in the catalog means a fence you build around a bed.

That empty ladder ALSO exposed a gate hole: `control_ladder_gate` skipped `None` (correctly, since
unladdered is legal through the rollout) but `[]` is not `None`, so it fell through and reported
nothing. Fixed separately in `a256211`; an empty ladder is now a violation. Both halves came from
one refusal by one agent, which is why "trust the bots' self-flags" is in the playbook.

TWO T1 SOURCES THAT DISAGREE ON THE SECOND WIRE, and the prose says so rather than picking silently:
  iastate_ext  "A two-wire fence with one wire 4 to 6 inches above the ground and the other at 12
                inches should keep the raccoons out" + "the electric fence should be installed
                about 2 weeks before the sweet corn reaches the milk stage"
  umn_ext      "an electric fence with two strands about four inches apart, starting five inches
                above the ground, may keep them away"  (so roughly 5 and 9 inches)
UMN also hedges the whole approach -- "It is difficult to fence out raccoons" and "may keep them
away" -- and that hedge is KEPT. A method that promised exclusion would be the safety-absolute class
in a new costume.

NOT MINTED THIS ROUND, recorded and owed:
  `adjust_planting_date` -- the highest-FREQUENCY gap on corn, unplaceable in FOUR of eight entries
    (earworm "plant early so the crop silks before peak moth flights", cutworms "delay sowing until
    the soil is warm", flea beetles "plant after the soil warms", rust "plant early so the crop
    matures before rust builds late"). It will recur across the rollout and deserves its own read of
    the sources rather than being tacked onto a fencing promote.
  `oil_on_silks`         -- corn earworm's traditional tactic; `horticultural_oil` is a different
    action (dosed into one silk channel vs sprayed over foliage) and was correctly not stretched.
  `preplant_weed_control`-- cutworms and flea beetles both name weedy ground as the source;
    `garden_sanitation` is debris and infected-leaf removal, not pre-plant weed clearing.
  `avoid_wounding`       -- common smut enters through wounds made during cultivation.
  `container_culture`    -- still owed from r2/r3, still three negative source reads.
"""

NEW_METHODS = {
    "exclusion_fencing": {
        "name": "Exclusion fencing",
        "tier": "physical",
        "applies_to": ["vertebrate"],
        "how_it_works_beginner": (
            "Some animals cannot be sprayed for or scared off for long, so the answer is a barrier "
            "they will not cross. For raccoons in sweet corn that means a low electric fence of two "
            "wires run around the patch, close to the ground where the animal pushes through rather "
            "than up high where it would climb. Put it up and switch it on before the ears are "
            "ready, not after the first raid: once they have found the patch they come back night "
            "after night. Fencing out a determined climber is hard, so treat this as your best "
            "chance rather than a certainty."
        ),
        "how_it_works_seasoned": (
            "A ground-level electrified barrier interrupts the approach rather than the animal, "
            "which is why wire height matters more than fence height: raccoons push under and "
            "through at ground level. Iowa State puts the two wires at 4 to 6 inches and 12 inches "
            "above the ground and has the fence energized about two weeks before the crop reaches "
            "the milk stage; Minnesota describes two strands about four inches apart starting five "
            "inches up, and notes it is difficult to fence raccoons out at all. Timing is the part "
            "growers get wrong: a fence raised after the first raid is trying to break an "
            "established nightly habit rather than prevent one."
        ),
        "best_use": (
            "Mammals that raid a ripening crop and cannot be sprayed or scared off, above all "
            "raccoons in sweet corn, with the fence energized before the crop is ready. Distinct "
            "from bird netting, which drapes mesh over the plants themselves against birds; this is "
            "a barrier around the bed, set at the height the animal travels."
        ),
        "find_it_beginner": (
            "Sold as a garden or pet fence energizer with polywire or poly-tape and step-in posts; "
            "a low-joule solar unit is enough for a small patch."
        ),
        "pros": [
            "Acts on the one control that works when spraying and scaring do not",
            "Reusable season after season, and it moves with the planting",
        ],
        "cons": [
            "Raccoons are hard to fence out at all, so treat a good result as the aim rather than the expectation",
            "Needs to be energized before the crop ripens, and vegetation growing into the wires "
            "shorts it out",
        ],
        "cautions": [
            "An electric fence is a real shock hazard to children and pets; use a fence energizer "
            "sold for the purpose, follow its instructions, and check local rules before installing "
            "one"
        ],
        "sources": ["iastate_ext", "umn_ext"],
        "anchoring_urls": {
            "iastate_ext": {
                "url": "https://yardandgarden.extension.iastate.edu/faq/how-can-i-keep-raccoons-out-my-sweet-corn",
                "verified": "2026-08-24"},
            "umn_ext": {"url": "https://extension.umn.edu/vegetables/growing-sweet-corn",
                        "verified": "2026-08-24"},
        },
    },
}

DISAMBIGUATION = {"exclusion_fencing": "bird netting"}

# The method must keep its sources' hedge. A fence that "keeps raccoons out" would be the
# safety-absolute class wearing a different hat.
REQUIRED_HEDGE = r"difficult to fence|rather than a certainty|rather than the expectation"

SOURCE_READS = [
    {"id": "iastate_ext", "for": "exclusion_fencing", "read": "2026-08-24",
     "url": "https://yardandgarden.extension.iastate.edu/faq/how-can-i-keep-raccoons-out-my-sweet-corn",
     "quote": "A two-wire fence with one wire 4 to 6 inches above the ground and the other at 12 "
              "inches should keep the raccoons out"},
    {"id": "umn_ext", "for": "exclusion_fencing", "read": "2026-08-24",
     "url": "https://extension.umn.edu/vegetables/growing-sweet-corn",
     "quote": "It is difficult to fence out raccoons, but an electric fence with two strands about "
              "four inches apart, starting five inches above the ground, may keep them away."},
]

NOT_MINTED = {
    "adjust_planting_date": "highest-frequency gap on corn (4 of 8 entries); deserves its own "
                            "source read, and it will recur across the rollout",
    "oil_on_silks": "corn earworm's traditional tactic; horticultural_oil is a different action "
                    "and was correctly not stretched",
    "preplant_weed_control": "cutworms and flea beetles both name weedy ground; garden_sanitation "
                             "is debris and infected-leaf removal, not pre-plant weed clearing",
    "avoid_wounding": "common smut enters through cultivation wounds",
    "container_culture": "still owed from r2/r3; three negative source reads",
}
