#!/usr/bin/env python3
"""PLA-8 batch 5 -- the four fixes the READ found, applied to the staged files.

Kept as a script rather than hand-edits so the fixes are reproducible, reviewable, and can be
re-asserted by the promote (batch 4's `check_read_fixes` pattern). Every anchor is asserted before
it is changed: if the staged shape is not what the read saw, this aborts rather than guessing.

FIX 1 -- pole-beans / mexican-bean-beetle: `off_season_tillage` -> `garden_sanitation`.
  THE BATCH-1 DEFECT CLASS. The seasoned clause is BYTE-IDENTICAL on both bean siblings ("Work crop
  debris into the soil promptly after harvest to remove overwintering shelter"), and the two
  authoring passes filed it under different keys. `off_season_tillage` MEANS destroying
  soil-pupating stages -- "disrupts the pupal cells of soil-pupating Lepidoptera such as the
  hornworms". Mexican bean beetle overwinters as ADULTS near woodland edges, which both crops' own
  `cause` field states. Same-sounding action, wrong mechanism.
  ONLY THE KEY MOVES. The note as authored already describes shelter removal rather than pupal
  destruction, so it is correct under the new key and no prose is invented here.
  The pole-beans pass flagged this itself and used the key anyway -- third batch running where a
  self-flagged loose fit was a real mismatch.

FIX 2 + 3 -- green-beans-bush ordering, to match the sibling AND the source's own order.
  The cross-sibling check flagged Anthracnose and Bean root rots: same method SET, different order,
  and the prevention prose the differing rungs are built from is byte-identical across the two
  crops. Its rule is that a divergence is a defect "when the prose they share is the prose the
  differing rung would be built from", which is exactly this.
  Both are same-tier (cultural) moves, so no tier ordering changes and no claim is added or removed.
  Direction chosen by the SOURCE, not by the sibling: anthracnose prevention reads seed -> clear old
  plants -> rotation -> water at base, and root rots reads soil warmth -> raised beds.

FIX 4 -- green-beans-bush / bean-root-rots: drop the root-injury clause from sound_sowing_practice.
  `sound_sowing_practice`'s best_use ENUMERATES its scope: "seed quality, depth, soil warmth and
  restrained watering". Handling damage at planting is outside that list. The crop's prose does say
  "Avoid damaging the roots when planting", so this is a real sourced control with no catalog home;
  the honest move is to leave it unplaced and record the gap, not to stretch the key. The pole-beans
  pass refused it for the same reason, so this also settles a sibling divergence.
"""
import json, os, sys

B = os.path.dirname(os.path.abspath(__file__))


def load(slug):
    return json.load(open(os.path.join(B, f"out_{slug}.json")))


def save(slug, d):
    json.dump(d, open(os.path.join(B, f"out_{slug}.json"), "w"), ensure_ascii=False, indent=2)


def problems(d):
    return list(d.get("pests") or []) + list(d.get("diseases") or [])


def by_id(d, pid):
    for p in problems(d):
        if p["id"] == pid:
            return p
    raise AssertionError(f"problem {pid!r} not in staged file")


def methods(p):
    return [r["method"] for r in p["control_ladder"]]


def reorder(p, want):
    """Reorder a ladder to `want`. Refuses unless it is a pure permutation of what is there."""
    have = methods(p)
    assert sorted(have) == sorted(want), f"not a permutation: {have} vs {want}"
    assert have != want, f"already in the target order: {have}"
    index = {r["method"]: r for r in p["control_ladder"]}
    p["control_ladder"] = [index[m] for m in want]


def main():
    changed = []

    # ---- FIX 1 -------------------------------------------------------------------------------
    pole = load("pole-beans")
    mbb = by_id(pole, "mexican-bean-beetle")
    rung = next(r for r in mbb["control_ladder"] if r["method"] == "off_season_tillage")
    before = list(methods(mbb))
    assert "garden_sanitation" not in before, "pole-beans already carries garden_sanitation on MBB"
    assert "shelter" in (rung["note_beginner"] + rung["note_seasoned"]).lower(), (
        "the authored note is not about shelter removal, so swapping the key alone would leave the "
        "note describing a mechanism the new key does not carry")
    rung["method"] = "garden_sanitation"
    changed.append(f"pole-beans/mexican-bean-beetle: off_season_tillage -> garden_sanitation "
                   f"({before} -> {methods(mbb)})")
    save("pole-beans", pole)

    # ---- FIX 2, 3, 4 -------------------------------------------------------------------------
    gbb = load("green-beans-bush")

    anth = by_id(gbb, "anthracnose")
    reorder(anth, ["certified_clean_stock", "crop_rotation", "garden_sanitation",
                   "water_at_the_base", "copper_fungicide"])
    changed.append(f"green-beans-bush/anthracnose: reordered -> {methods(anth)}")

    rr = by_id(gbb, "bean-root-rots")
    reorder(rr, ["sound_sowing_practice", "improve_drainage", "crop_rotation", "garden_sanitation"])
    changed.append(f"green-beans-bush/bean-root-rots: reordered -> {methods(rr)}")

    ssp = next(r for r in rr["control_ladder"] if r["method"] == "sound_sowing_practice")
    b_old = " Take care not to damage the roots as you plant."
    s_old = ("; root injury at planting is named alongside cold, wet soil as what sets these fungi "
             "up, so handle the row accordingly.")
    assert ssp["note_beginner"].endswith(b_old), "beginner root-injury clause not found as authored"
    assert ssp["note_seasoned"].endswith(s_old), "seasoned root-injury clause not found as authored"
    ssp["note_beginner"] = ssp["note_beginner"][: -len(b_old)]
    ssp["note_seasoned"] = ssp["note_seasoned"][: -len(s_old)] + (
        " in the cold, wet conditions these fungi exploit.")
    changed.append("green-beans-bush/bean-root-rots: root-injury clause removed from "
                   "sound_sowing_practice (outside the key's enumerated scope; recorded as a gap)")
    save("green-beans-bush", gbb)

    print(f"applied {len(changed)} read fixes:")
    for c in changed:
        print(f"  - {c}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
