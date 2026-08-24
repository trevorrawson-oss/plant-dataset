#!/usr/bin/env python3
"""PLA-8: the Bt safety absolute in CROP prose. Content + the source read.

THE DEFECT. Nine crops' `organic_treatment_beginner` say Bt is "safe and targets only caterpillars":
  kale, spinach, arugula, bok-choy, cauliflower, cabbage, kohlrabi, brussels-sprouts, collards

Two things are wrong with that sentence, and the second is the one that matters.

1. "which is SAFE" is an unhedged safety absolute, the PLA-253 class. NPIC (fetched and READ
   2026-08-24) never uses the word "safe" without qualification: it says Bt is "low in toxicity to
   people and other mammals when eaten", "practically nontoxic and doesn't cause disease in birds,
   fish, and shrimp", and that EPA "concluded that the Bt strains tenebrionis, israelensis, and
   kurstaki are low in toxicity to bees". It also records that "some pesticide products with Bt in
   them have caused eye and skin irritation".

2. "targets ONLY caterpillars" is literally true and CONSUMER-MISLEADING, which is worse than a
   plain overstatement. It reads as "harmless to everything else you care about", when the actual
   non-target risk IS other caterpillars. NPIC: "a few studies also found that non-target moths
   were harmed." A gardener told Bt targets only caterpillars has been given a reason to spray
   freely, which is the opposite of the intended behaviour.

THE CATALOG ALREADY HAD THIS RIGHT -- FOR THE THIRD TIME THIS ARC. `control_methods.bt` carries:
  cautions: "Bt kurstaki kills the caterpillars of moths and butterflies as a group, including
             desirable species such as swallowtails and monarchs; spray only plants with a pest
             problem, never butterfly host plants"
  how_it_works_beginner: "...it does not tell good caterpillars from bad, so spray only the plants
             that have a pest problem."
PLA-253 removed and hedged the absolute in the METHOD and the remediation never reached the crops.
Same shape as the iron-phosphate slug bait: check the catalog before assuming the whole record is
wrong -- see [[source-catalog-is-the-admission-authority]].

AND THE DATASET ALREADY KNOWS THE NUANCE ON THREE OTHER CROPS, which is what makes these nine
inconsistent rather than merely unhedged:
  dill    "Bt is effective if control is truly needed, but is rarely warranted on a host plant
           grown partly for the butterflies."
  viola   "...leaving native fritillary larvae where butterflies are wanted."
  parsley "Bacillus thuringiensis (Bt) controls them if needed, but on parsley they rarely warrant it."

READ, NOT COUNTED. A scan for Bt + safe/only/harmless returned 17 hits. NINE are this class. The
other EIGHT are FALSE POSITIVES on four corn crops, where "only" is about EFFICACY TIMING and is
correctly stated: "An organic Bt spray only works while they are still out on the leaves" and
"a Bt product reaches them only while they are still feeding in the open whorl". Untouched.

DELIBERATELY NOT FIXED HERE, recorded:
  * The `organic_treatment_seasoned` on cauliflower, cabbage, kohlrabi and brussels-sprouts says Bt
    and spinosad "target caterpillars and spare beneficials". That is a DIFFERENT claim -- true of
    non-Lepidopteran beneficials and incomplete about Lepidopteran ones. It is not the safety
    absolute this sweep was opened for, and folding it in would repeat the scope creep this arc has
    twice had to resist deliberately.
"""

# (crop slug, problem name, field, exact old text, exact new text)
EDITS = [
    (
        "kale", "Cabbageworms and cabbage loopers", "organic_treatment_beginner",
        "Spray a product called Bt, which is safe and targets only caterpillars, or pick the "
        "caterpillars and eggs off by hand from under the leaves. Spray again after rain, since it "
        "washes off.",
        "Spray a product called Bt, which is low in toxicity to people, pets and bees and acts on "
        "caterpillars rather than on insects in general. It cannot tell a pest caterpillar from a "
        "butterfly one, so treat only the plants that have a problem. Or pick the caterpillars and "
        "eggs off by hand from under the leaves. Spray again after rain, since it washes off.",
    ),
    (
        "collards", "Cabbageworms and cabbage loopers", "organic_treatment_beginner",
        "Spray a product called Bt, which is safe and targets only caterpillars, or pick the "
        "caterpillars and eggs off by hand from under the leaves. Spray again after rain, since it "
        "washes off.",
        "Spray a product called Bt, which is low in toxicity to people, pets and bees and acts on "
        "caterpillars rather than on insects in general. It cannot tell a pest caterpillar from a "
        "butterfly one, so treat only the plants that have a problem. Or pick the caterpillars and "
        "eggs off by hand from under the leaves. Spray again after rain, since it washes off.",
    ),
    (
        "spinach", "Caterpillars (loopers and armyworms)", "organic_treatment_beginner",
        "Spray Bt, which is safe and targets only caterpillars, or pick them off by hand. Spray "
        "again after rain since it washes off.",
        "Spray Bt, which is low in toxicity to people, pets and bees and acts on caterpillars "
        "rather than on insects in general. It cannot tell a pest caterpillar from a butterfly one, "
        "so treat only the plants that have a problem. Or pick them off by hand. Spray again after "
        "rain since it washes off.",
    ),
    (
        "arugula", "Cabbage caterpillars", "organic_treatment_beginner",
        "Spray Bt, which is safe and targets only caterpillars, or pick them and their eggs off by "
        "hand from the undersides of leaves. Spray again after rain, since it washes off.",
        "Spray Bt, which is low in toxicity to people, pets and bees and acts on caterpillars "
        "rather than on insects in general. It cannot tell a pest caterpillar from a butterfly one, "
        "so treat only the plants that have a problem. Or pick them and their eggs off by hand from "
        "the undersides of leaves. Spray again after rain, since it washes off.",
    ),
    (
        "bok-choy", "Cabbage caterpillars", "organic_treatment_beginner",
        "Spray Bt, which is safe and targets only caterpillars, or pick them and their eggs off by "
        "hand from the undersides of leaves. Spray again after rain, since it washes off.",
        "Spray Bt, which is low in toxicity to people, pets and bees and acts on caterpillars "
        "rather than on insects in general. It cannot tell a pest caterpillar from a butterfly one, "
        "so treat only the plants that have a problem. Or pick them and their eggs off by hand from "
        "the undersides of leaves. Spray again after rain, since it washes off.",
    ),
    (
        "cauliflower", "Cabbageworms, loopers, and diamondback moths", "organic_treatment_beginner",
        "Spray Bt, which is safe and targets only caterpillars, or spinosad, and pick caterpillars "
        "and eggs off by hand from under the leaves. Spray again after rain, since it washes off.",
        "Spray Bt, which is low in toxicity to people, pets and bees and acts on caterpillars "
        "rather than on insects in general, or spinosad. Bt cannot tell a pest caterpillar from a "
        "butterfly one, so treat only the plants that have a problem. Pick caterpillars and eggs "
        "off by hand from under the leaves. Spray again after rain, since it washes off.",
    ),
    (
        "cabbage", "Cabbageworms, loopers, and diamondback moths", "organic_treatment_beginner",
        "Spray Bt, which is safe and targets only caterpillars, or spinosad, and pick caterpillars "
        "and eggs off by hand from under the leaves. Spray again after rain, since it washes off.",
        "Spray Bt, which is low in toxicity to people, pets and bees and acts on caterpillars "
        "rather than on insects in general, or spinosad. Bt cannot tell a pest caterpillar from a "
        "butterfly one, so treat only the plants that have a problem. Pick caterpillars and eggs "
        "off by hand from under the leaves. Spray again after rain, since it washes off.",
    ),
    (
        "brussels-sprouts", "Cabbageworms and cabbage loopers", "organic_treatment_beginner",
        "Spray Bt, which is safe and targets only caterpillars, or spinosad, and pick caterpillars "
        "and eggs off by hand from under the leaves. Spray again after rain, since it washes off.",
        "Spray Bt, which is low in toxicity to people, pets and bees and acts on caterpillars "
        "rather than on insects in general, or spinosad. Bt cannot tell a pest caterpillar from a "
        "butterfly one, so treat only the plants that have a problem. Pick caterpillars and eggs "
        "off by hand from under the leaves. Spray again after rain, since it washes off.",
    ),
    (
        "kohlrabi", "Cabbageworms, loopers, and diamondback moths", "organic_treatment_beginner",
        "Spray Bt, which is safe and targets only caterpillars, or spinosad, and pick caterpillars "
        "and eggs off by hand from under the leaves. Spray again after rain.",
        "Spray Bt, which is low in toxicity to people, pets and bees and acts on caterpillars "
        "rather than on insects in general, or spinosad. Bt cannot tell a pest caterpillar from a "
        "butterfly one, so treat only the plants that have a problem. Pick caterpillars and eggs "
        "off by hand from under the leaves. Spray again after rain.",
    ),
]

# The banned constructions, checked roster-wide over Bt prose only (see SCOPE).
BANNED = (
    r"\bwhich\s+is\s+safe\b",
    r"\btargets?\s+only\s+caterpillars\b",
    r"\bBt\b[^.]{0,40}\bis\s+safe\b",
)

# The banned scan is roster-wide but SCOPED to prose that talks about Bt. A promote's post-state
# guard must assert only what the promote establishes; an unscoped "which is safe" scan would catch
# unrelated classes and pressure a silent widening.
SCOPE = r"\bB\.?t\.?\b|bacillus thuringiensis|thuricide"

# Absence of the absolute proves nothing on its own -- deleting the sentence would satisfy it.
# Every rewritten field must ALSO carry the qualified toxicity claim AND the non-target caveat.
REQUIRED_QUALIFIER = r"low in toxicity"
REQUIRED_NONTARGET = r"butterfly"

# Correctly-stated efficacy uses of "only" on four corn crops. NOT the class; must stay untouched.
CORN_EFFICACY_ONLY = ("sweet-corn", "field-corn", "popcorn", "flint-corn")

# Crops that already carry the butterfly nuance and are the model these nine were out of step with.
ALREADY_CORRECT = ("dill", "viola", "parsley")

SOURCE_READ = {
    "id": "npic_orst",
    "url": "https://npic.orst.edu/factsheets/btgen.html",
    "read": "2026-08-24",
    "quotes": [
        "Bt is low in toxicity to people and other mammals when eaten",
        "practically nontoxic and doesn't cause disease in birds, fish, and shrimp",
        "the Bt strains tenebrionis, israelensis, and kurstaki are low in toxicity to bees",
        "a few studies also found that non-target moths were harmed",
        "some pesticide products with Bt in them have caused eye and skin irritation",
    ],
    "never_says": "safe (unqualified)",
}

# Recorded, deliberately NOT fixed here.
NOT_FIXED = {
    "cauliflower/cabbage/kohlrabi/brussels-sprouts organic_treatment_seasoned":
        "says Bt and spinosad 'target caterpillars and spare beneficials'. A DIFFERENT claim: true "
        "of non-Lepidopteran beneficials, incomplete about Lepidopteran ones. Not the safety "
        "absolute this sweep was opened for.",
}
