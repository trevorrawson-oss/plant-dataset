#!/usr/bin/env python3
"""Generate the Layer-1 `ladder_delta` content for the PLA-8 Round 2 pilot (apple + strawberry).

LAYER 1 IS DERIVED, NOT HAND-AUTHORED PER VARIETY. What is authored here is FOUR dual-register
sentence patterns, one per delta class; the generator fills them from data already in the canonical
(`varieties[].resistance` + the parent `control_ladder`). Nothing is invented per variety, so no
delta can drift from its parent and every delta inherits the T1 sourcing of the grade behind it.

THE FOUR CLASSES (see docs/2026-08-22-pla8-round1-...md sec 5b, corrected 2026-08-22):

  R0-SATISFIED  non-susceptible + rung 0 is `resistant_varieties` -> the reader already completed
                that rung by choosing this variety. Restate it as done. Wording tracks the GRADE:
                immune / resistant / tolerant are three different promises and get three different
                sentences.
  R0-INVERTED   `susceptible` + rung 0 is `resistant_varieties` -> rung 0 tells a reader who already
                owns the plant to go choose a different one. Reframe it as load-bearing: the rungs
                below are now carrying what genetics would have carried.
  DROP          immune / resistant -> remove the soft_chemical + conventional rungs.
  SOFTEN        tolerant -> keep the escalation rung, move it from schedule to response.

SOURCING: every delta is `basis: "resistance"`, meaning it is recomputable from the grade and
inherits that grade's anchors. The DROP class additionally rests on UMN Extension's own instruction
("Do not use fungicides: On apple and crabapple varieties that are resistant or immune to apple
scab."), verified live 2026-08-22 -- a T1 source stating the mechanism, not merely the grade.

COPY RULES APPLIED: no em dashes in consumer copy; American English; `°F` for temperatures; "plant"
lowercase; everyday words in the beginner register; no NEW unglossed jargon (disease names are used
exactly as the parent rung already uses them); no absolute-outcome claims.

Run: python3 tools/build_variety_ladder_delta_content.py [--emit PATH]
"""
import argparse
import json
import sys

CANON = "crops_data_final.json"
ESCALATION = {"soft_chemical", "conventional"}
R0_METHOD = "resistant_varieties"

# Natural-language disease names, used exactly as the parent rungs already say them.
DISEASE = {
    "apple-scab": "apple scab",
    "fire-blight": "fire blight",
    "cedar-apple-rust": "cedar-apple rust",
    "powdery-mildew": "powdery mildew",
    "anthracnose": "anthracnose",
    "red-stele": "red stele",
    "verticillium-wilt": "verticillium wilt",
}

# What neglecting the remaining rungs ACTUALLY costs, per disease. A single generic clause was the
# first draft and it was WRONG on five of the seven: red stele and verticillium kill whole plants
# (they are root and vascular diseases, nothing to do with fruit quality), and fire blight kills
# wood. Never let one consequence sentence stand in for seven different diseases.
CONSEQUENCE = {
    "apple-scab": "shows up as scabbed fruit and early leaf drop",
    "fire-blight": "costs you shoots, and can set a young tree back badly",
    "cedar-apple-rust": "shows up as spotted, early-dropping leaves",
    "powdery-mildew": "shows up as distorted shoots and russeted fruit",
    "anthracnose": "shows up as rotting fruit right at picking time",
    "red-stele": "costs you whole plants, since there is no cure once the roots go",
    "verticillium-wilt": "costs you whole plants, since there is no cure once one wilts",
}

# Purdue BP-132-W's own caution, carried rather than compressed away. A source's hedge dropped in
# summary is a defect with no term to scan for, so it is pinned here at the point of generation.
HEDGE = ("Resistance is not immunity: Purdue's rating table cautions that even highly resistant "
         "varieties can succumb under extreme conditions or stress.")

# ---------------------------------------------------------------- the four authored patterns

def r0_satisfied(variety, disease, grade, hedge=True):
    """Rung 0 is already done, because of the variety the reader chose.

    Wording tracks the source's own word for the grade and goes no further. The first draft said
    an immune variety "cannot catch it at all", which is stronger than anything the sources say;
    UMN's word is "immune" and Purdue cautions in the same breath that resistance is not immunity.
    """
    if grade == "immune":
        return (
            f"Already done. You chose {variety}, which is immune to {disease}, so this step is "
            f"settled from the start.",
            f"Satisfied at purchase: {variety} is rated immune to {disease} (UMN Extension's own "
            f"wording), so the protectant program the lower rungs support is not warranted here.",
        )
    if grade == "resistant":
        return (
            f"Already done. You chose {variety}, which shrugs off {disease} in most years, so this "
            f"step is settled from the start. It is not a guarantee in a punishing season, so keep "
            f"an eye out rather than assuming.",
            f"Satisfied at purchase: {variety} is rated resistant to {disease}. Scout in a season "
            f"that favors the disease rather than spraying on a calendar."
            + (f" {HEDGE}" if hedge else ""),
        )
    return (  # tolerant
        f"Mostly done. You chose {variety}, which gets {disease} more lightly than most, so this "
        f"step is largely settled, though a bad year can still bring some on.",
        f"Partly satisfied: {variety} is rated moderately resistant to {disease}, which lowers the "
        f"pressure without removing it. Watch a season that favors the disease."
        + (f" {HEDGE}" if hedge else ""),
    )


def r0_inverted(variety, disease, consequence):
    """Rung 0 asks for a choice the reader has already made the other way."""
    return (
        f"This step is about choosing a resistant variety, and {variety} is not one: it catches "
        f"{disease} readily. That choice is behind you now, so the steps below are what keep this "
        f"planting healthy, and letting them slide {consequence}.",
        f"Not satisfied on this cultivar: {variety} rates susceptible to {disease}, so the cultural "
        f"and protectant rungs below carry the full load here instead of backing up genetic "
        f"resistance.",
    )


def drop(variety, disease, method_name, grade):
    """An escalation rung that this variety does not need."""
    if grade == "immune":
        why_b = (f"You can skip {method_name} on this one. {variety} is immune to {disease}, so "
                 f"there is nothing for a protective spray to guard against.")
    else:
        why_b = (f"You can skip {method_name} as a routine on this one. {variety} resists "
                 f"{disease}, so a protective spray has little left to do.")
    return (
        why_b,
        f"Not indicated on a {grade} cultivar: UMN Extension states plainly that fungicide is not "
        f"to be used on varieties that are resistant or immune to the disease, so this rung drops "
        f"out rather than being held in reserve.",
    )


# Where the sources genuinely disagree about a grade, the conservative reading is carried AND the
# disagreement is stated in the prose rather than hidden behind the grade (ruled by Trevor
# 2026-08-22). Keyed by (variety id, problem id); the text is appended to that pair's rung-0 note.
# A reader who is told only the safer of two ratings has been given a fact; a reader told that the
# raters differ has been given the actual state of the evidence.
GRADE_DISAGREEMENT = {
    ("honeycrisp", "apple-scab"): (
        " The raters differ here: University of Minnesota Extension calls Honeycrisp resistant to "
        "scab, Purdue rates it only moderately so, and we have taken the more cautious of the two.",
        " The two ratings differ: UMN Extension lists Honeycrisp under \"Resistant to apple scab\" "
        "while Purdue BP-132-W rates it MR, moderately resistant. The conservative MR reading is "
        "the one carried here, and Honeycrisp does not appear in the Cornell variety database at "
        "all, so there is no third table to break the tie.",
    ),
}


# A rung whose text is written CONDITIONALLY on susceptibility ("If you grow a susceptible
# variety...") is addressing a question the variety page has already answered. Measured across both
# pilot crops: 34 occurrences, but only 4 distinct rung+register combinations, and 3 of those are the
# rung-0 note that R0-INVERTED already replaces. This is the ONE genuine leftover -- apple scab's
# sulfur rung, which survives on susceptible varieties (nothing is dropped for them) and reaches 13
# apple varieties. Authored for that rung specifically rather than regex-rewritten, and keyed so the
# rollout can add more only where a rung really is written this way.
CONDITIONAL_SPENT = {
    ("apple-scab", "sulfur"): lambda variety: (
        f"This is your spray rung, and on {variety} it earns its place. Sulfur has to go on in "
        f"spring before infection starts, on a protective schedule. Once the spots are everywhere "
        f"it is too late for that year. Do not spray it in heat above 90°F, since it burns leaves."
    ),
}


def soften(variety, disease, method_name):
    """Keep the escalation rung, but move it from schedule to response."""
    return (
        f"Keep {method_name} in reserve rather than on the calendar. {variety} takes {disease} "
        f"lightly, so use it only if a season actually turns bad, not as a routine.",
        f"Reserve rather than schedule: on a moderately resistant cultivar, apply in response to a "
        f"genuine infection period instead of on the standard protectant interval.",
    )


# ---------------------------------------------------------------- generation

def build(data, crops=("apple", "strawberry")):
    catalog = data["control_methods"]
    by_slug = {c["slug"]: c for c in data["crops"]}
    out, stats = {}, {"R0-SATISFIED": 0, "R0-INVERTED": 0, "DROP": 0, "SOFTEN": 0, "CONDITIONAL-SPENT": 0, "GRADE-DISAGREEMENT": 0}
    for slug in crops:
        crop = by_slug[slug]
        ladders = {p["id"]: p for f in ("pests", "diseases") for p in crop.get(f) or []
                   if isinstance(p, dict) and "control_ladder" in p}
        per_variety = {}
        for v in crop["varieties"]["recommended"]:
            grades = v.get("resistance") or {}
            if not grades:
                continue
            name = v["name"]
            delta = {}
            for pid, grade in grades.items():
                parent = ladders[pid]["control_ladder"]
                disease = DISEASE[pid]
                rungs = []
                # -- the rung-0 classes ---------------------------------------------------
                if parent[0]["method"] == R0_METHOD:
                    # A specific source-disagreement note SUPERSEDES the generic hedge: saying
                    # "resistance is not immunity" and "these two raters differ" in the same
                    # paragraph is the same caution twice, and the second is the precise version.
                    add = GRADE_DISAGREEMENT.get((v["id"], pid))
                    if grade == "susceptible":
                        nb, ns = r0_inverted(name, disease, CONSEQUENCE[pid]); stats["R0-INVERTED"] += 1
                    else:
                        nb, ns = r0_satisfied(name, disease, grade, hedge=not add)
                        stats["R0-SATISFIED"] += 1
                    if add:
                        nb, ns = nb + add[0], ns + add[1]
                        stats["GRADE-DISAGREEMENT"] += 1
                    rungs.append({"method": R0_METHOD, "op": "replace",
                                  "note_beginner": nb, "note_seasoned": ns})
                # -- the escalation classes -----------------------------------------------
                for r in parent[1:]:
                    if catalog[r["method"]]["tier"] not in ESCALATION:
                        continue
                    mname = catalog[r["method"]]["name"].lower()
                    if grade in ("immune", "resistant"):
                        wb, ws = drop(name, disease, mname, grade); stats["DROP"] += 1
                        rungs.append({"method": r["method"], "op": "drop",
                                      "why_beginner": wb, "why_seasoned": ws})
                    elif grade == "tolerant":
                        nb, ns = soften(name, disease, mname); stats["SOFTEN"] += 1
                        rungs.append({"method": r["method"], "op": "replace",
                                      "note_beginner": nb, "note_seasoned": ns})
                    elif grade == "susceptible":
                        fn = CONDITIONAL_SPENT.get((pid, r["method"]))
                        if fn:
                            stats["CONDITIONAL-SPENT"] += 1
                            rungs.append({"method": r["method"], "op": "replace",
                                          "note_beginner": fn(name)})
                if rungs:
                    delta[pid] = {"basis": "resistance", "rungs": rungs}
            if delta:
                per_variety[v["id"]] = delta
        out[slug] = per_variety
    return out, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit")
    a = ap.parse_args()
    data = json.load(open(CANON))
    content, stats = build(data)
    n_var = sum(len(v) for v in content.values())
    n_prob = sum(len(d) for v in content.values() for d in v.values())
    n_rung = sum(len(e["rungs"]) for v in content.values() for d in v.values() for e in d.values())
    print(f"varieties with a ladder_delta : {n_var}")
    print(f"problem entries               : {n_prob}")
    print(f"rung operations               : {n_rung}")
    for k, v in stats.items():
        print(f"   {k:14s} {v}")
    if a.emit:
        with open(a.emit, "w") as fh:
            json.dump(content, fh, ensure_ascii=False, indent=1)
        print(f"\nwrote {a.emit}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
