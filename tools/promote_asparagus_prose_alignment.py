#!/usr/bin/env python3
"""Align asparagus's remaining crop-level prose with the [6,10] mature ramp.

THE DEFECT. The 2026-07-28 reconciliation widened `harvest_ramp_weeks` bed year 5 from
[8,10] to [6,10] and rewrote `harvest_ready_*`, but RAMP-PROSE only read `harvest_ready_*`,
so NINE other crop-level strings went on asserting a superseded six-to-eight-week figure
while the gate reported clean. Seven of the nine are rendered by plant-app -- the guide
body, both Growing Journey stage-card lines, the watering note and a tip callout -- so a
grower could read "Year 5. 6 to 10 weeks." in the phase ribbon and "six to eight weeks"
in the body copy on one screen.

RAMP-PROSE has since been widened to read EVERY crop-level consumer string (measured: a
no-op on every crop without a ramp, which today is all of them but one). It reports 8 of
the 9 on the pre-fix canonical. This promote drives it to 0.

THE NINTH, and it is the one worth the pass. `year_one_notes_seasoned` CONTRADICTS ITSELF
inside a single string: "Cut nothing the first year AND NOTHING THE SECOND ... Expect a
FIRST LIGHT CUT IN YEAR 2 or 3." That is the [0,0] collapse in prose form -- the same
false-precision error corrected in `harvest_ramp_weeks` year 2 on 2026-07-27, still
sitting in consumer copy where no gate had ever looked. The ramp says year 2 is [0,2], an
optional light cut, and `years_to_first_harvest` is [2,3]. The repaired string states the
disagreement honestly instead of asserting both of its sides at once. It also said the
season lengthens to "six weeks ... around year 5", understating the [6,10] the ramp now
carries; the range regex cannot parse that phrasing, so it is repaired by hand and the
parser gap is recorded rather than papered over.

GUARD. Pre-state is pinned by sha256 of each expected string rather than a transcribed
copy, so a typo in this file cannot silently widen what it overwrites.

Usage: python3 tools/promote_asparagus_prose_alignment.py [--write]
Dry-run by default. Aborts on ANY drift. Prove the abort by re-running after --write.
"""
import hashlib
import json
import sys

PATH = "crops_data_final.json"
EXPECT_SHA = "27f14303c3c77e7ca34313bf137173bc3a83e76ff2626578916ddd40336c2a79"

# (path, sha256 of the expected pre-state string, replacement)
EDITS = [
    (
        ("description_beginner",),
        "3310bc7a1dc92b1a",
        "Asparagus is a long-lived perennial vegetable: you plant it once and a good bed "
        "keeps feeding you for 15 to 20 years. You grow it from one-year-old crowns set in "
        "a deep trench, then wait two to three years for the first real harvest while the "
        "roots get strong. Each spring the bed sends up the tender green spears you eat; a "
        "young bed gives only a short pick and a mature one can run six to ten weeks, and "
        "you stop when the new spears come up thin and let the rest grow into tall, ferny "
        "foliage that feeds the roots for next year. For a new bed, plant an all-male "
        "hybrid like Millennium, a very cold-hardy, high-yielding variety that most "
        "northern nurseries now carry. Jersey Knight is another good all-male pick, with "
        "better tolerance to rust and root rot. Mary Washington is the classic seed-grown "
        "heirloom, lower-yielding but easy to find, and Purple Passion has sweet purple "
        "spears that are nice raw in a salad. Asparagus likes full sun and deep, "
        "well-drained soil, and it needs a real winter rest, so it is a temperate crop "
        "rather than a tropical one.",
    ),
    (
        ("description_seasoned",),
        "e880c268b2ecfe08",
        "Asparagus (Asparagus officinalis) is a long-lived herbaceous perennial grown for "
        "the tender spring spears it pushes from a deep, cold-hardy crown. Established "
        "once from one-year-old crowns in a deep trench, a well-sited bed yields for 15 to "
        "20 years and sometimes far longer. The rhythm is fixed: spears emerge as the soil "
        "warms and are cut for a spring window that lengthens with bed age, reaching six "
        "to ten weeks on a mature crown, after which every remaining spear grows into a "
        "tall fern canopy that recharges the crown for the next season. It is a temperate "
        "crop by physiology, not a tropical one; UC IPM notes asparagus requires two "
        "distinct periods, a growing period and a resting period, so it needs a real "
        "winter dormancy to persist. Variety choice sets the ceiling. All-male hybrids "
        "outyield the open-pollinated types and skip the weedy volunteer seedlings: "
        "Millennium, a cold-hardy University of Guelph hybrid, is the modern high-yield "
        "northern standard but runs more susceptible to rust, while the Rutgers Jersey "
        "hybrids, represented here by Jersey Knight, carry the class's vigor-based field "
        "tolerance to rust and to Fusarium crown and root rot. Among the open-pollinated "
        "types, Mary Washington is the century-old heirloom standard, hardy but "
        "lighter-yielding with mixed male and female plants, and Purple Passion is a "
        "sweeter, purple-speared strain that yields less and catches foliage disease more "
        "easily. Give asparagus full sun and deep, well-drained ground, and choose the "
        "site with care, since the crowns will hold it for two decades.",
    ),
    (
        ("watering", "schedule_by_stage", 1, "note_seasoned"),
        "de9e7acd71964162",
        "The crown is spending reserves to push spears, so keep even, deep moisture through "
        "the whole cutting season, however long the bed's age lets it run; water at the "
        "soil line with drip or a soaker so the emerging spears and soon-to-grow ferns "
        "stay dry against rust.",
    ),
    (
        ("growth_stages", 1, "user_action_beginner"),
        "3efb0fac23e6783e",
        "Pick spears every day or two right through the spring harvest, then stop once the "
        "new spears come up thin and let the plants grow. If frost is coming, cut the "
        "standing spears first or cover the bed.",
    ),
    (
        ("growth_stages", 1, "user_action_seasoned"),
        "bd58dc9473ebb7cf",
        "Snap or cut spears at the soil line every one to three days through the harvest "
        "window the bed's age supports, then stop once the spears thin toward pencil width "
        "and let the rest grow into ferns. If frost threatens emerged spears, harvest them "
        "first or cover the bed.",
    ),
    (
        ("tips_by_stage", "spear_emergence", 0, "text_beginner"),
        "c987f65ceeabe084",
        "Once a bed is established, cut spears when they are about 6 to 8 inches tall with "
        "closed, tight tips, every day or two. A mature bed can keep going six to ten "
        "weeks, but let the spears call it: stop when the new ones turn thin, about "
        "pencil-width or skinnier. That thinning is the plant telling you it is low on "
        "energy, so let the rest grow into ferns.",
    ),
    (
        ("tips_by_stage", "spear_emergence", 0, "text_seasoned"),
        "7e8b73eb98b0104f",
        "On an established bed, cut spears at about 6 to 8 inches with tight tips, every "
        "one to three days, through a spring window that reaches six to ten weeks once the "
        "crown is mature. The signal to stop is the spears themselves: when the majority "
        "thin down to about pencil width, a quarter to a half inch depending on which "
        "extension you follow, and come up spindly, quit cutting. Harvesting past that "
        "point drains the crown, so let the rest grow to fern once the diameter drops off.",
    ),
    (
        ("notifications", 1, "body_seasoned"),
        "db0f73c26537f59d",
        "You are near the end of the cutting season for a bed this age. Once the spears "
        "thin to about pencil width, stop cutting and let the rest grow to fern, or you "
        "will drain the crown and cost next spring's yield.",
    ),
    (
        ("year_one_notes_seasoned",),
        "2daa6134e3e7082a",
        "Set one-year-old crowns while they are still dormant, as early as the soil can be "
        "worked; the planting year is about root establishment, not spears. Cut nothing at "
        "all the first year: the fern is the crown's only way to build the reserves that "
        "carry every later harvest. Let the fern stand all season and until it browns after "
        "a hard frost, then cut it down. The second spring, take a light two-week pick only "
        "if the bed came through the first season strong, since the extension literature "
        "splits on whether to cut in year 2 at all. From there the season lengthens with "
        "bed age, reaching six to ten weeks once the crown matures around year 5.",
    ),
]

# untouched reference values, asserted before and after
REFS = {
    ("year_one_notes_beginner",): "0e6c9a",   # prefix only; full check is "unchanged"
}


def fail(msg):
    sys.exit(f"ABORT: {msg}")


def get(node, path):
    for k in path:
        node = node[k]
    return node


def put(node, path, value):
    for k in path[:-1]:
        node = node[k]
    node[path[-1]] = value


def main():
    write = "--write" in sys.argv
    raw = open(PATH, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != EXPECT_SHA:
        fail(f"canonical SHA {sha[:16]} != expected {EXPECT_SHA[:16]}")
    print(f"canonical SHA OK: {sha[:16]}")

    data = json.loads(raw.decode("utf-8"))
    if len(data["crops"]) != 128:
        fail(f"crop count {len(data['crops'])} != 128")
    asp = [c for c in data["crops"] if c.get("slug") == "asparagus"]
    if len(asp) != 1:
        fail(f"expected exactly 1 asparagus crop, found {len(asp)}")
    asp = asp[0]

    # pre-state, pinned by hash so a typo here cannot widen what we overwrite
    for path, want_sha, _ in EDITS:
        cur = get(asp, path)
        if not isinstance(cur, str):
            fail(f"{list(path)} is not a string")
        got = hashlib.sha256(cur.encode()).hexdigest()[:16]
        if got != want_sha:
            fail(f"drift on {list(path)}\n  sha {got} != expected {want_sha}\n  have: {cur[:120]!r}")
    print(f"pre-state OK: all {len(EDITS)} strings match their expected hash")

    before_refs = {p: get(asp, p) for p in REFS}

    for path, _, new in EDITS:
        if "—" in new:
            fail(f"em dash in replacement for {list(path)}")
        put(asp, path, new)

    for p, v in before_refs.items():
        if get(asp, p) != v:
            fail(f"reference value {list(p)} changed")
    print(f"reference OK: {len(REFS)} untouched value(s) verified")

    sys.path.insert(0, "tools")
    from harvest_duration_gate import (duration_violations, ramp_violations,
                                       ramp_prose_violations, stop_rule_violations)
    from zone_order_gate import zone_order_violations
    for name, fn in (("ramp", ramp_violations), ("ramp_prose", ramp_prose_violations),
                     ("stop_rule", stop_rule_violations), ("duration", duration_violations),
                     ("zone_order", zone_order_violations)):
        v = fn(asp)
        if v:
            fail(f"{name} still fires after repair:\n  " + "\n  ".join(v))
    print("invariant OK: all five gate checks return 0 on the repaired crop")

    out = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    if out.endswith("\n"):
        fail("trailing newline would be written")

    if not write:
        print("\nDRY RUN -- re-run with --write to apply")
        for path, _, _ in EDITS:
            print(f"  {'.'.join(str(k) for k in path)}")
        return

    with open(PATH, "w", encoding="utf-8", newline="") as f:
        f.write(out)
    new_sha = hashlib.sha256(open(PATH, "rb").read()).hexdigest()
    print(f"\nWRITTEN. canonical {sha[:8]} -> {new_sha[:8]}")


if __name__ == "__main__":
    main()
