#!/usr/bin/env python3
"""PLA-8: widen the catalog `best_use` fields that are narrower than their own shipped usage.

WHY. `ladder_batch.py prepare` puts `best_use` in front of every authoring agent as "what the
method MEANS", and `MethodSheet.tsx` renders it to users under "When to reach for it". It was
written around each method's motivating crop and never widened as the method spread, so it now
understates what the method is for on both surfaces at once.

MEASURED during batch 3 (the three cucumbers): 11 of 49 shipped methods carry a `best_use` narrower
than their real use. In that ONE batch it produced four false gaps -- an agent refusing a legal,
precedented rung -- plus one genuinely missing rung, where cucumber's agent read
`resistant_varieties`' "for diseases that recur in your beds" as disease-only and declined to place
a varietal non-preference trait that eight shipped rungs across six crops already carry. With ~34
batches left, that is a recurring tax on every authoring pass.

THIS IS CONSUMER COPY. `best_use` renders in the app, so these follow the copy rules: no em or en
dashes, American English, no absolutes, everyday words. They must also stay CONCRETE -- a bland
catch-all would be worse guidance than a narrow example, for the agent and the reader both. The
shape used throughout is: name the ACTION generally, then give the classic cases as EXAMPLES rather
than as the boundary.

NO NEW CLAIMS. Each widened string describes usage that already shipped, restating what the existing
rungs assert. The one genuinely new fact is the corn borer's overwintering site, and it comes from
sweet-corn's own sourced prose ("the borer overwinters in old stalks; shred and turn under
cornstalks after harvest").

ONE OF THE ELEVEN IS CORRECT AS WRITTEN AND IS DELIBERATELY NOT TOUCHED -- see EXCLUDED.

Used by: tools/promote_pla8_bestuse.py
"""

# ---------------------------------------------------------------------------------------------
# EXCLUDED. The detector flagged this on a keyword match; reading it says leave it alone.
# ---------------------------------------------------------------------------------------------
EXCLUDED = {
    "bottom_watering":
        "CORRECT AS WRITTEN. Its best_use already names BOTH shipped problems (damping-off and "
        "fungus gnats) and correctly confines the method to indoor trays and seedlings. That "
        "confinement is not narrowness to be fixed, it is the whole point of the field: "
        "`bottom_watering` MEANS water from below in seed trays, and twelve authored rungs in "
        "batch 1 used it to mean water at the base outdoors, which is a different action. Widening "
        "this one would re-open the worst defect the rollout has produced.",
}

# ---------------------------------------------------------------------------------------------
# WIDENINGS. `old` is asserted byte-for-byte against canonical before any write; a mismatch is a
# REFUSAL, never a silent overwrite.
# ---------------------------------------------------------------------------------------------
WIDENINGS = {
    "garden_sanitation": {
        "why": "103 rungs / 19 crops / 7 types, of which 31 are INSECT, but the field is framed "
               "entirely around disease.",
        "old": "End-of-season cleanup and in-season removal of the first infected leaves; the "
               "backbone step for black rot and other diseases with no chemical cure.",
        "new": "End-of-season cleanup, plus pulling the first affected leaves or fruit during the "
               "season. It is the backbone step for anything that spends the winter in the debris "
               "you leave behind, from black rot and other diseases with no chemical cure to "
               "beetles, borers and slugs sheltering in what is still standing.",
    },
    "resistant_varieties": {
        "why": "65 rungs / 17 crops, 15 of them INSECT. The disease-only framing is what made "
               "cucumber's agent refuse a rung its own prose earned.",
        "old": "Chosen at seed-buying time for diseases that recur in your beds, such as clubroot, "
               "downy mildew, and black rot; the natural handoff to variety-level resistance data.",
        "new": "Chosen at seed-buying time, and worth checking first for any problem that returns "
               "year after year. Most often disease resistance, such as clubroot, downy mildew and "
               "black rot, but it also covers varieties a pest is less drawn to, like a tight corn "
               "husk against earworm. The natural handoff to variety-level resistance data.",
    },
    "crop_rotation": {
        "why": "44 rungs / 15 crops, 16 INSECT, and many of the fungal ones are FOLIAR diseases "
               "carried in residue rather than soilborne.",
        "old": "A season-to-season foundation for soilborne diseases and root pests, especially "
               "clubroot, black rot, and cabbage maggot in the same bed.",
        "new": "A season-to-season foundation wherever a problem survives in the bed between crops, "
               "whether it waits in the soil or in last year's debris. Clubroot, black rot and "
               "cabbage maggot are the classic cases, and the same move works on cucumber beetles "
               "and on the leaf diseases that carry over in old vines.",
    },
    "floating_row_cover": {
        "why": "31 rungs / 14 crops, and SEVEN are bacterial: excluding a vector to prevent a "
               "disease you cannot treat. The field never mentions that use at all.",
        "old": "Preventive exclusion from transplanting until the pest's egg-laying period passes, "
               "for cabbageworms, flea beetles, and cabbage maggot; remove for pollination if the "
               "crop needs it.",
        "new": "Preventive exclusion from transplanting until the pest's egg-laying period passes, "
               "for cabbageworms, flea beetles and cabbage maggot. It is also the main defense "
               "against a disease with no cure once it arrives, such as bacterial wilt, where "
               "keeping the carrier insect off young plants is the lever that works. Remove for "
               "pollination if the crop needs it.",
    },
    "handpick": {
        "why": "27 rungs / 16 crops including mollusks; the field says chewing pests only.",
        "old": "Low to moderate numbers of visible chewing pests such as cabbageworms and cutworms "
               "in a small garden, on a regular scouting routine.",
        "new": "Low to moderate numbers of anything big enough to spot and slow enough to catch, on "
               "a regular scouting routine: cabbageworms, cutworms, beetles, squash bugs, slugs and "
               "snails. Best in a small garden where you walk the rows anyway.",
    },
    "airflow_spacing": {
        "why": "29 rungs / 15 crops, reaching gray mold, powdery mildew and seedling damping-off, "
               "not only the two leaf blights named.",
        "old": "Preventive layout for foliar diseases such as downy mildew and the celery leaf-spot "
               "blights, set at planting by spacing and site choice.",
        "new": "Preventive layout for the diseases that need damp, still air, set at planting by "
               "spacing and site choice. Downy mildew and the celery leaf-spot blights are typical, "
               "and the same room helps against gray mold, powdery mildew and damping-off in a "
               "crowded tray.",
    },
    "bt": {
        "why": "13 rungs / 8 crops across seven caterpillar problems, not two. The added last "
               "sentence carries the non-target caveat the corrected register and cautions already "
               "make, onto the surface a reader consults when DECIDING to use it.",
        "old": "The go-to biological control for cabbageworms and loopers, sprayed on young "
               "caterpillars and reapplied after rain or new growth.",
        "new": "The go-to biological control for caterpillars, from cabbageworms and loopers to "
               "hornworms, corn earworm and stalk borers. Spray on young caterpillars and reapply "
               "after rain or new growth. It acts on caterpillars as a group, so keep it off "
               "plants you are growing for butterflies.",
    },
    "balance_nitrogen": {
        "why": "9 rungs / 9 crops, all aphids, but the crops include tomato, strawberry, pepper and "
               "the cucumbers. The PROBLEM scope was right; the CROP restriction was not.",
        "old": "A preventive feeding habit for aphids and other soft-bodied sap-suckers on leafy "
               "and cole crops.",
        "new": "A preventive feeding habit anywhere aphids and other soft-bodied sap-suckers turn "
               "up most years. Heavy nitrogen pushes out the soft new growth they multiply on, "
               "whatever the crop.",
    },
    "off_season_tillage": {
        "why": "A FACTUAL CORRECTION, not only a widening. Flagged in batch 2 one round after the "
               "method was minted: glossed around the hornworms that motivated it, so it names a "
               "life stage European corn borer does not have. The borer overwinters INSIDE THE "
               "STALK, per sweet-corn's own sourced prose. The action was right the whole time.",
        "old": "A finished bed that carried a soil-pupating caterpillar such as tomato or tobacco "
               "hornworm, worked once after harvest. Distinct from garden sanitation, which clears "
               "plant debris off the surface rather than disturbing the soil the pupae are sitting "
               "in.",
        "new": "A finished bed that carried a pest which stays put over the winter, worked once "
               "after harvest. That may be pupae in the soil, as with tomato hornworm, or "
               "caterpillars inside old stalks, as with European corn borer, where shredding and "
               "turning the stalks under is what reaches them. Distinct from garden sanitation, "
               "which clears the surface rather than breaking up what sits in it.",
    },
    "even_watering": {
        "why": "8 rungs / 6 crops and HALF are spider mites, but the field is written entirely "
               "around calcium disorders. The 1 to 2 inch figure is kept, scoped to the case it "
               "was published for.",
        "old": "Preventing calcium-movement disorders such as celery blackheart, by watering on a "
               "steady schedule of about 1 to 2 inches per week and never letting shallow-rooted "
               "crops dry out.",
        "new": "Steady soil moisture instead of a swing between soaked and bone dry. It prevents "
               "the calcium-movement disorders such as celery blackheart and blossom-end rot, at "
               "roughly 1 to 2 inches per week on shallow-rooted crops, and it holds spider mites "
               "down too, since they build up fastest on plants that have been left dry and "
               "stressed.",
    },
}


def apply_widenings(cm):
    """Apply to a loaded control_methods dict, in place. Returns the count.

    Raises on ANY mismatch: a method that is missing, whose current text is not the expected `old`,
    or that is in EXCLUDED. The alternative is silently overwriting prose someone else changed.
    """
    applied = 0
    for key, w in WIDENINGS.items():
        if key in EXCLUDED:
            raise AssertionError(f"{key} is in EXCLUDED and must not be widened")
        if key not in cm:
            raise AssertionError(f"no catalog method {key!r}")
        cur = cm[key].get("best_use")
        if cur != w["old"]:
            raise AssertionError(
                f"{key}: best_use is not the expected text; it changed under this pass.\n"
                f"  expected: {w['old'][:90]!r}\n  found   : {str(cur)[:90]!r}")
        cm[key]["best_use"] = w["new"]
        applied += 1
    if applied != len(WIDENINGS):
        raise AssertionError(f"applied {applied} of {len(WIDENINGS)}")
    return applied


if __name__ == "__main__":
    import json, os, sys
    REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    d = json.load(open(os.path.join(REPO, "crops_data_final.json")))
    n = apply_widenings(d["control_methods"])
    print(f"widened     : {n} methods")
    print(f"excluded    : {len(EXCLUDED)} ({', '.join(EXCLUDED)})")
    for k, w in WIDENINGS.items():
        print(f"\n{k}\n  WHY: {w['why']}\n  NEW: {w['new']}")
