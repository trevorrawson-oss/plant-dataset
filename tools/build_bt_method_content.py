#!/usr/bin/env python3
"""PLA-8: close the Bt safety absolute in the CATALOG method. The last of the class.

THE DEFECT, AND WHY IT IS THE LAST ONE. `9116050` swept "Spray Bt, which is safe and targets only
caterpillars" from nine crops' prose. It deliberately did NOT touch `control_methods.bt`, because
that was a different file, a different claim, and folding it in would have been the scope creep this
arc resisted all session. This promote closes it.

`bt.how_it_works_beginner` carries both halves of the class, and it CONTRADICTS ITSELF:

    "It ONLY AFFECTS CATERPILLARS, so the risk to bees is low, and people and pets cannot activate
     the proteins at all, which is why a treated vegetable IS SAFE TO EAT. Two things to watch. The
     spray itself can irritate eyes and skin ... And IT DOES NOT TELL GOOD CATERPILLARS FROM BAD, so
     spray only the plants that have a pest problem."

Sentence three says it affects only caterpillars; sentence six says it cannot tell a pest caterpillar
from a butterfly one. Both are trying to say the true thing -- Bt is selective to Lepidoptera AS A
GROUP -- but the first phrasing is the one that misleads, because the non-target risk IS other
caterpillars. NPIC: "a few studies also found that non-target moths were harmed."

WHAT NPIC ACTUALLY SAYS (fetched and READ 2026-08-24, the same read that backed `9116050`):
  "Bt is low in toxicity to people and other mammals when eaten"
  "Bt is very low in toxicity to people and other mammals when inhaled"
  "practically nontoxic and doesn't cause disease in birds, fish, and shrimp"
  "the Bt strains tenebrionis, israelensis, and kurstaki are low in toxicity to bees"
  "some pesticide products with Bt in them have caused eye and skin irritation"
It NEVER uses "safe" without qualification.

READ, NOT COUNTED. A scan of all 50 catalog methods for safety constructions returned 15 hits.
**THIRTEEN ARE CORRECT AS WRITTEN and are deliberately untouched:**
  * "non-toxic" on `stem_collars`, `yellow_sticky_traps`, `red_sphere_trap`, `slug_traps_barriers`,
    `swd_monitoring_traps`, `codling_moth_pheromone_trap` -- these methods are cardboard, glue and
    pheromone. There is no toxicant, so the word is literally accurate.
  * "completely selective" on `handpick` and `stem_collars` -- accurate for a physical method where
    you choose each target by hand.
  * "must completely cover the planting" on `swd_exclusion_netting` -- an INSTRUCTION, not a safety
    claim.
  * **"practically nontoxic to people, pets, bees, and wildlife" in `bt.how_it_works_seasoned` and
    `bt.pros` -- this is NPIC'S OWN TERM OF ART and is already qualified. Rewriting it would make
    the record LESS faithful to the source, not more.**
Only the two constructions in `bt.how_it_works_beginner` are the class.

THE `cautions` ENTRY IS ALREADY RIGHT and is untouched: "Bt kurstaki kills the caterpillars of moths
and butterflies as a group, including desirable species such as swallowtails and monarchs; spray only
plants with a pest problem, never butterfly host plants."
"""

METHOD = "bt"
FIELD = "how_it_works_beginner"

OLD = (
    "Bt is a natural soil bacterium. When a caterpillar eats leaves sprayed with it, the Bt "
    "proteins wreck its gut, and it stops feeding and dies. It only affects caterpillars, so the "
    "risk to bees is low, and people and pets cannot activate the proteins at all, which is why a "
    "treated vegetable is safe to eat. Two things to watch. The spray itself can irritate eyes and "
    "skin, so wear gloves and keep it away from your face. And it does not tell good caterpillars "
    "from bad, so spray only the plants that have a pest problem."
)

NEW = (
    "Bt is a natural soil bacterium. When a caterpillar eats leaves sprayed with it, the Bt "
    "proteins wreck its gut, and it stops feeding and dies. It acts on caterpillars rather than on "
    "insects in general, so the risk to bees is low, and it is low in toxicity to people and pets, "
    "who cannot activate the proteins the way a caterpillar's gut does. Two things to watch. The "
    "spray itself can irritate eyes and skin, so wear gloves and keep it away from your face. And "
    "it cannot tell a pest caterpillar from a butterfly one, so spray only the plants that have a "
    "pest problem, never a plant you are growing for butterflies."
)

# What must be GONE from the rewritten field.
BANNED = (
    r"\bonly\s+affects?\b",
    r"\bis\s+safe\s+to\s+eat\b",
    r"\b(?:is|are)\s+safe\b",
)

# Absence proves nothing on its own -- deleting the sentence would satisfy it. Each of these must be
# PRESENT, and together they are the specification.
REQUIRED = {
    "qualified toxicity": r"low in toxicity",
    "acts-on not only-affects": r"acts on caterpillars rather than",
    "the non-target caveat": r"cannot tell a pest caterpillar from a butterfly one",
    "the actionable consequence": r"never a plant you are growing for butterflies",
    "the irritation warning": r"irritate eyes and skin",
    "the mechanism that makes it low-toxicity": r"cannot activate the proteins",
}

# Deliberately NOT touched, and the suite asserts they survive byte-for-byte.
UNTOUCHED_BT_FIELDS = ("how_it_works_seasoned", "best_use", "pros", "cons", "cautions",
                       "sources", "anchoring_urls", "applies_to", "tier", "name")

# The 13 correct-as-written hits from the roster-wide scan. Guarded so a later sweep cannot
# "finish the job" by flattening accurate language.
CORRECT_AS_WRITTEN = {
    "stem_collars": "non-toxic / completely selective -- a cardboard collar",
    "yellow_sticky_traps": "non-toxic -- glue on a card",
    "red_sphere_trap": "non-toxic and pesticide-free -- a sticky sphere",
    "slug_traps_barriers": "non-toxic -- traps and barriers",
    "swd_monitoring_traps": "non-toxic -- a monitoring trap",
    "codling_moth_pheromone_trap": "non-toxic -- a pheromone lure",
    "handpick": "completely selective -- you choose each target by hand",
    "swd_exclusion_netting": "must completely cover -- an instruction, not a safety claim",
}

SOURCE_READ = {
    "id": "npic_orst",
    "url": "https://npic.orst.edu/factsheets/btgen.html",
    "read": "2026-08-24",
    "quotes": [
        "Bt is low in toxicity to people and other mammals when eaten",
        "the Bt strains tenebrionis, israelensis, and kurstaki are low in toxicity to bees",
        "a few studies also found that non-target moths were harmed",
        "some pesticide products with Bt in them have caused eye and skin irritation",
    ],
    "never_says": "safe (unqualified)",
}
