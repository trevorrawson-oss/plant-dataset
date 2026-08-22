#!/usr/bin/env python3
"""Perennial year-pill coherence (PLA-6 Round 1). Fires only for `perennial: true` crops.

WHY THIS EXISTS -- the shape of the perennial year model, measured on canonical fe26f783.

There is NO year-keyed prose field in this dataset. `growth_stages_year_one` and
`growth_stages_annual` are present on 25 perennials and EMPTY on all 25 (15 x `[]`, 10 x
`null`); nothing reads them in either consumer repo. `year_one_notes_*` (26 crops),
`establishment_note` (26), `harvest_stop_rule` (2) and `yield_expectations.first_year_note_*`
(37) are authored, carried through the export projection, and rendered by NO component in
plant-app -- `first_year_note_*` reaches only the plant-astro website.

What the grower actually sees is three year-pills, and plant-app composes their captions out of
prose authored for other purposes (`src/app/(tabs)/learn/[slug].tsx`, establishmentCopy):

    Establishing   -> tips_by_stage.establishment[0].text_{level}
    First harvests -> tips_by_stage.establishment[0].text_{level}     <-- the SAME string
    Full harvest   -> firstSentence(harvest_ready_{level})

That composition is a deliberate app decision, not drift ("Establishing and first harvests share
the establishment tip" is in its own comment). It has two consequences this gate owns.

1. THE FULL-HARVEST CAPTION IS A TRUNCATION. `harvest_ready_*` is a paragraph; the pill shows
   its first sentence and nothing else. A field that is excellent as a paragraph can open with a
   bare topic sentence, and then a mature bed's entire guidance reads "Squeeze the bud." on
   certified artichoke. Every existing check reads the WHOLE field and passes -- the
   optional-field-gates-go-vacuous class in a new spot.

2. TWO PILLS SHARE ONE STRING, so that string is load-bearing twice over and must carry both
   registers. A39's register-coverage floor runs on the register-map fields;
   `tips_by_stage.establishment[0].text_*` is not one of them.

Family three is PLA-6 Round 1 step 3's literal ask: intra-crop duplication between two stage
entries. The gold-standard template-copy check compares ACROSS crops, so a crop repeating itself
is invisible to it. Measured 0 roster-wide, which makes it a REFUSAL-SPEC guard -- per CLAUDE.md
a guard that refuses an input and stays green is a pass, not a vacuity, and the mutation harness
(tools/mutate_perennial_year_gate.py) is its only non-vacuity evidence.

NOT GATED HERE, deliberately: `establishment_years` ships in three incompatible shapes (27 int,
4 `[lo, hi]`, 2 null, 5 absent). That is a live SCHEMA question Trevor raised on 2026-08-22
("is a fixed three-year model right for every perennial?") and it awaits a ruling. Gating an
unruled shape would force the answer, which is exactly the failure the A25 tightening taught.

Run standalone:  python3 tools/perennial_year_gate.py [crops_data_final.json]
"""
import difflib
import itertools
import json
import re
import sys

# Ported from plant-app's firstSentence() -- `/^.*?[.!?](?=\s|$)/`. The lookahead is what keeps
# "0.25 inch" from truncating to "0.", so it is reproduced rather than approximated.
_FIRST_SENTENCE = re.compile(r"^.*?[.!?](?=\s|$)", re.S)

# MEASURED, not guessed. First-sentence word counts over all 242 harvest_ready register strings
# roster-wide: min 3, p05 7, p10 11, median 24. At `< 8`, scoped to the crops that actually
# render pills, this yields 4 findings on 3 crops. The same threshold applied roster-wide pulls
# in 15, mostly legitimate topic sentences on annuals with no pill to truncate into ("Beets give
# you two harvests."). The scope is what keeps it at 4 -- narrow the CHECK, not the threshold.
CAPTION_MIN_WORDS = 8

# Cross-stage near-duplication. 0.90 sits well clear of the live maximum: the most similar
# same-field cross-stage pair on the whole perennial roster is echinacea's vegetative/budding
# log_prompt_beginner at 0.833, and only 3 of 5,484 comparisons exceed 0.80.
DUP_RATIO = 0.90

# Below this, similarity is noise -- "Any buds yet?" vs "Any pods yet?" scores 0.92 on length
# alone. Short strings still flag on EXACT equality, which is where the real log_prompt
# duplicates live (PLA-326 owns whether those short UI strings should be register-bearing).
DUP_MIN_CHARS = 40

# The register-bearing stage fields. Cross-stage comparison is same-field only: what_to_look_for
# and user_action may legitimately converge inside one stage, and comparing across field names
# floods without finding a copy defect.
STAGE_FIELDS = (
    "what_to_look_for_beginner", "what_to_look_for_seasoned",
    "user_action_beginner", "user_action_seasoned",
    "log_prompt_beginner", "log_prompt_seasoned",
    "timing_beginner", "timing_seasoned",
)

REGISTERS = ("beginner", "seasoned")


def first_sentence(text):
    """plant-app's firstSentence(): the lead sentence, or the whole string if unterminated."""
    m = _FIRST_SENTENCE.match(text or "")
    return m.group(0) if m else (text or "")


def _register_note(source, base, level):
    """plant-app's registerNote() fallback chain: exact level, then seasoned, then beginner."""
    for key in (f"{base}_{level}", f"{base}_seasoned", f"{base}_beginner"):
        v = (source or {}).get(key)
        if isinstance(v, str) and v:
            return v
    return ""


def renders_pills(crop):
    """True when plant-app actually shows this crop's three year-pills.

    The app gates the whole pill row on a well-formed `years_to_first_harvest`, and its
    establishmentState() FAILS OPEN to 'full' on anything malformed. 12 of the 38 perennials
    carry no usable range (the 5 woody-ornamental herbs, the 3 culinary herbs, both flowers, and
    the avocado/olive shells) and show no pills at all, so a short caption there is never
    rendered and is not a finding. Scoping to the rendered set is what keeps this gate at 4
    findings: the same threshold over all 38 perennials yields 7, and roster-wide 15.
    """
    if crop.get("perennial") is not True:
        return False
    y = crop.get("years_to_first_harvest")
    return (isinstance(y, list) and len(y) >= 2
            and all(isinstance(n, (int, float)) and not isinstance(n, bool) for n in y[:2]))


def pill_caption_violations(crop):
    """PILL-CAPTION: the Full-harvest pill's caption must stand alone.

    Absence is NOT reported here -- A39 owns register presence, and double-counting the two
    uncertified shells would inflate this gate's findings with someone else's defect.
    """
    if not renders_pills(crop):
        return []
    out = []
    for level in REGISTERS:
        # SUPPRESSED once the pill has its own field. PLA-6 Round 2 gave the Full-harvest pill
        # `full_harvest_notes_{level}`, which plant-app prefers and never shears; the
        # harvest_ready first sentence is now only the FALLBACK. Measuring a string that is no
        # longer rendered would report a defect nobody can see. Checked per register, because a
        # crop can be half-migrated mid-wave.
        if crop.get(f"full_harvest_notes_{level}"):
            continue
        raw = _register_note(crop, "harvest_ready", level)
        if not raw:
            continue
        lead = first_sentence(raw)
        words = len(lead.split())
        if words < CAPTION_MIN_WORDS:
            out.append(
                f"{crop.get('slug')}: {level}: Full-harvest pill caption is {words} words -- "
                f"plant-app renders only this sentence for a mature bed: {lead!r}")
    return out


def estab_caption_violations(crop):
    """ESTAB-CAPTION: the establishment tip is the caption for TWO pills, in both registers."""
    if not renders_pills(crop):
        return []
    tips = (crop.get("tips_by_stage") or {}).get("establishment") or []
    if not tips or not isinstance(tips[0], dict):
        return [f"{crop.get('slug')}: tips_by_stage.establishment is absent or empty -- "
                f"the Establishing and First-harvests pills would render no caption"]
    tip = tips[0]
    missing = [f"text_{lvl}" for lvl in REGISTERS if not tip.get(f"text_{lvl}")]
    if missing:
        return [f"{crop.get('slug')}: tips_by_stage.establishment[0] missing "
                f"{', '.join(missing)} -- this string captions two of the three year-pills"]
    return []


def _norm(s):
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def year_dup_violations(crop):
    """YEAR-DUP: two different stages of the SAME crop carrying the same text in the same field.

    The cross-crop template-copy check cannot see this. Same-field only, and short strings flag
    only on exact equality -- see DUP_MIN_CHARS.
    """
    if crop.get("perennial") is not True:
        return []
    stages = crop.get("growth_stages") or []
    out = []
    for field in STAGE_FIELDS:
        for i, j in itertools.combinations(range(len(stages)), 2):
            a, b = _norm(stages[i].get(field)), _norm(stages[j].get(field))
            if not a or not b:
                continue
            if a == b:
                exact = True
            elif min(len(a), len(b)) < DUP_MIN_CHARS:
                continue
            elif difflib.SequenceMatcher(None, a, b).ratio() >= DUP_RATIO:
                exact = False
            else:
                continue
            out.append(
                f"{crop.get('slug')}: {field}: stages {stages[i].get('id')!r} and "
                f"{stages[j].get('id')!r} carry {'identical' if exact else 'near-identical'} "
                f"text -- a year-2 reader learns nothing new: {a[:90]!r}")
    return out


def violations(crop):
    """Every family, for the whole-crop gate."""
    return (pill_caption_violations(crop)
            + estab_caption_violations(crop)
            + year_dup_violations(crop))


def main(argv):
    path = argv[1] if len(argv) > 1 else "crops_data_final.json"
    data = json.load(open(path, encoding="utf-8"))
    per = [c for c in data["crops"] if c.get("perennial") is True]
    pills = [c for c in per if renders_pills(c)]
    print(f"perennial crops: {len(per)}   rendering year-pills: {len(pills)}   "
          f"pills suppressed (no usable years_to_first_harvest): {len(per) - len(pills)}")
    total = 0
    for name, fn in (("PILL-CAPTION", pill_caption_violations),
                     ("ESTAB-CAPTION", estab_caption_violations),
                     ("YEAR-DUP", year_dup_violations)):
        found = [v for c in per for v in fn(c)]
        total += len(found)
        print(f"\n{name}: {len(found)}")
        for v in found:
            print(f"  {v}")
    print(f"\nTOTAL: {total}")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
