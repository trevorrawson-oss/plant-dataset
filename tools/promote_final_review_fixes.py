#!/usr/bin/env python3
"""FINAL-REVIEW FIX WAVE for the asparagus harvest-duration branch (2026-07-28).

WHAT THIS FIXES. The whole-branch review found the DATA sound and the PERMANENT RECORD
over-claiming. In this repo the written record is load-bearing, so an over-claim is a
blocking defect. Three canonical repairs, all asparagus, all record-or-citation:

  1a  verification_status.open_findings[39].finding -- TWO factual errors, plus the
      over-claim the review names in its Part 2:
        * "NINE cells were source-checked and left inheriting the crop default" -- the
          entry's OWN list names TEN (mid_atlantic z7/z8, northern_tier z3/z4/z5/z6/z7,
          pnw z8, se_gulf z8, warm_arid z8). 12 candidates minus the 2 that received
          overrides = 10, which is what the register and LATEST.txt already say.
        * "place the mature-bed season between 6 and 10 weeks (... MU G6405 5-8 ...)" --
          the sentence contradicts its own citation list, since 5 is below the stated
          floor of 6. Restated: the documents SPAN roughly five to ten weeks, and [6, 10]
          is the range carried for the mature bed (UC MG publishes that span verbatim).
        * "Three layers ... now agree" -- false, and the same over-claim the review
          orders corrected in LATEST.txt / CURRENT_STATE.md / STATE_HISTORY.md /
          register row 27. Fixing it in three documents while leaving it standing in the
          canonical would leave the strongest copy of the false claim in place, so the
          clause is corrected here too. Same named field, minimal clause-level edit.
      Nothing else in the entry is touched.

  1b  harvest_ready_sources / harvest_ready_anchoring_urls -- the list rested on msu_ext,
      which returns an 85-character JavaScript shell with ZERO asparagus content at all
      three URL spellings, and omitted the documents the REWRITTEN registers actually
      rest on. The rewritten harvest_ready_beginner/_seasoned make exactly two load-bearing
      claims: (i) harvest length scales with BED AGE, mature ceiling at year five and
      beyond, and (ii) the season closes on SPEAR CALIPER at about pencil diameter, a
      quarter to a half inch. ADMISSION CRITERION APPLIED HERE: an id is listed iff it is
      (i) verified by raw fetch to publish a claim the rewritten prose makes and (ii)
      already present in source_catalog. No catalog additions, no invented ids.

        kept    umn_ext        bed-age ramp ("In the first year of harvest, only pick
                               asparagus for two weeks"; harvest begins year three)
                mu_ext         caliper (3/8 in.) + MU G6405's two-step bed-age ramp
                clemson_hgic   caliper ("Stop harvesting when the diameter of the spears
                               has been reduced to pencil-size") + third/fourth-year ramp
        added   uc_mg          bed-age keyed mature span ("in their fourth season, they
                               may be harvested for 6 to 10 weeks per year")
                rutgers_njaes  the full bed-age ladder (3rd / 4th / 5th-and-subsequent)
                umd_ext        bed-age keyed ("in their fourth season, harvest for 8 to 10")
                illinois_ext   bed-age keyed ("During the fourth year and thereafter")
                nmsu_ext       caliper 1/4 in. + "From year four on, harvest a maximum of
                               10 weeks/year"
                usu_ext        caliper ("majority of spears smaller than a pencil") + ramp
                uada_ext       caliper ("When the diameter of the spears is less than the
                               size of a pencil, cease harvesting.")
                ucanr_marin_mg          caliper 1/2 in.
                ucanr_santa_clara_mg    caliper ("thinner than a pencil")
        dropped msu_ext        FETCH RETURNS NO CONTENT (853-959 raw bytes -> an 85-char
                               JS shell, 0 asparagus mentions, three URL spellings).
                ucanr_pub7234  publishes a FLAT "8- to 10-week period" with no bed-age
                               keying and no caliper rule. The rewritten registers no
                               longer state a bare week count, so it carries no claim the
                               prose makes. In source_catalog, cited elsewhere, not here.

      harvest_ready_anchoring_urls is rebuilt to match one-for-one: every listed source is
      anchored at the asparagus DOCUMENT (never a portal root), and no anchor survives for
      a source no longer listed. All twelve URLs were re-fetched raw on 2026-07-28.

  1c  failure_diagnostics[0].next_season_tip_seasoned -- "cut no longer than six to eight
      weeks on bearing beds" is PRESCRIPTIVE and caps the season below the mature ramp's
      [6, 10] ceiling. That one clause is rewritten to defer to bed age and the stop rule.
      The rest of the string is untouched.

WHAT DELIBERATELY DOES NOT LAND. Eight further crop-level consumer strings still carry the
superseded six-to-eight-week figure (description_beginner, description_seasoned,
watering.schedule_by_stage[1].note_seasoned, growth_stages[1].user_action_beginner/_seasoned,
tips_by_stage.spear_emergence[0].text_beginner/_seasoned, notifications[1].body_seasoned).
They are DESCRIPTIVE and sit inside [6, 10], so they are superseded rather than contradictory:
stale, not wrong. They are registered as owed work, not rewritten here, and this script asserts
all eight are byte-identical before AND after -- they are the control group. (The review named
six of them; description_beginner/_seasoned are two the review's list missed. Same class.)

Usage: python3 tools/promote_final_review_fixes.py [--write]
Dry-run by default. Aborts on ANY drift from the expected pre-state. Prove the abort by
re-running after --write: the SHA guard must refuse the second pass.
"""
import hashlib
import json
import sys

PATH = "crops_data_final.json"
EXPECT_SHA = "f37b228bf97ca87c15d6c358dece243d3b852c69f2349c164242a5a330c80b62"

FINDING_IDX = 39
EXPECT_FINDINGS_LEN = 40
# sha256 of the exact finding string this pass edits; a whole-string guard without
# pasting 2,507 characters into the script (a transcription risk of its own).
EXPECT_FINDING_SHA = "b39748e2a092e1fd66cf974c0fc93eb8e7816f96311748b72f0bc6575d37a8fc"

# --- 1a. three clause-level substitutions inside open_findings[39].finding ---------------
# Each `old` must occur EXACTLY ONCE. Anything else means the entry drifted.
FINDING_EDITS = [
    (
        "Three layers of asparagus made different claims about the same mature bed and "
        "now agree.",
        "Three layers of asparagus made different claims about the same mature bed. The two "
        "harvest_ready_* registers, the structured harvest_ramp_weeks ramp and the new "
        "per-cell harvest_duration_weeks layer are now reconciled and gate-enforced; EIGHT "
        "further crop-level consumer strings still carry the superseded six-to-eight-week "
        "figure and are owed a follow-on prose pass (description_beginner, "
        "description_seasoned, watering.schedule_by_stage[1].note_seasoned, "
        "growth_stages[1].user_action_beginner/_seasoned, "
        "tips_by_stage.spear_emergence[0].text_beginner/_seasoned, "
        "notifications[1].body_seasoned). Those eight are descriptive and sit inside [6, 10], "
        "so they are stale rather than wrong, and no gate reads them: RAMP-PROSE reads only "
        "harvest_ready_*.",
    ),
    (
        "Eight independently fetched T1 documents place the mature-bed season between 6 and "
        "10 weeks (UMN 6-8, Rutgers 6, USU 6-8, MU G6405 5-8, UMD 8-10, Illinois 8-10, UC ANR "
        "7234 8-10, NMSU max 10) and UC Master Gardener statewide publishes the span verbatim "
        "('they may be harvested for 6 to 10 weeks per year');",
        "Eight independently fetched T1 documents span roughly five to ten weeks on the mature "
        "bed (UMN 6-8, Rutgers 6, USU 6-8, MU G6405 5-8, UMD 8-10, Illinois 8-10, UC ANR 7234 "
        "8-10, NMSU max 10), and [6, 10] is the range carried for the mature bed because UC "
        "Master Gardener statewide publishes that span verbatim ('they may be harvested for 6 "
        "to 10 weeks per year');",
    ),
    (
        "NINE cells were source-checked and deliberately left inheriting the crop default",
        "TEN cells were source-checked and deliberately left inheriting the crop default",
    ),
]

# --- 1b. the source list the rewritten registers actually rest on ------------------------
EXPECT_SOURCES = ["umn_ext", "msu_ext", "mu_ext", "clemson_hgic"]
EXPECT_ANCHORS = {
    "umn_ext": {"url": "https://extension.umn.edu/vegetables/growing-asparagus",
                "verified": "2026-07-24"},
    "msu_ext": {"url": "https://www.canr.msu.edu/resources/asparagus_in_the_home_garden",
                "verified": "2026-07-24"},
    "mu_ext": {"url": "https://extension.missouri.edu/publications/g6405",
               "verified": "2026-07-24"},
    "clemson_hgic": {"url": "https://hgic.clemson.edu/factsheet/asparagus/",
                     "verified": "2026-07-24"},
}

NEW_SOURCES = [
    "umn_ext", "mu_ext", "clemson_hgic",           # incumbents that re-verify
    "uc_mg", "rutgers_njaes", "umd_ext", "illinois_ext",   # bed-age ramp carriers
    "nmsu_ext", "usu_ext", "uada_ext",             # caliper stop (+ ramp) carriers
    "ucanr_marin_mg", "ucanr_santa_clara_mg",      # caliper stop, UC MG chapters
]
NEW_ANCHORS = {
    "umn_ext": "https://extension.umn.edu/vegetables/growing-asparagus",
    "mu_ext": "https://extension.missouri.edu/publications/g6405",
    "clemson_hgic": "https://hgic.clemson.edu/factsheet/asparagus/",
    "uc_mg": "https://ucanr.edu/statewide-program/uc-master-gardener-program/asparagus",
    "rutgers_njaes": "https://njaes.rutgers.edu/fs1301/",
    "umd_ext": "https://extension.umd.edu/resource/growing-asparagus-home-garden",
    "illinois_ext": "https://extension.illinois.edu/gardening/asparagus",
    "nmsu_ext": "https://pubs.nmsu.edu/_h/H227/index.html",
    "usu_ext": "https://extension.usu.edu/yardandgarden/research/asparagus-in-the-garden",
    "uada_ext": "https://www.uaex.uada.edu/publications/PDF/FSA-6002.pdf",
    "ucanr_marin_mg": "https://ucanr.edu/site/uc-marin-master-gardeners/document/asparagus",
    "ucanr_santa_clara_mg":
        "https://ucanr.edu/site/uc-master-gardeners-santa-clara-county/asparagus",
}
VERIFIED_ON = "2026-07-28"

# --- 1c. the one prescriptive clause that now contradicts the [6, 10] mature ramp ---------
EXPECT_TIP = ("Delay harvest on young beds, cut no longer than six to eight weeks on bearing "
              "beds, and stop at pencil-diameter thinning to protect the crown.")
NEW_TIP = ("Delay harvest on young beds, let bed age set how long a bearing bed is cut, and "
           "stop at pencil-diameter thinning to protect the crown.")

# --- the control group: descriptive six-to-eight-week strings that must NOT move ----------
CONTROL_STRINGS = {
    "description_beginner": ("description_beginner",),
    "description_seasoned": ("description_seasoned",),
    "watering.schedule_by_stage[1].note_seasoned":
        ("watering", "schedule_by_stage", 1, "note_seasoned"),
    "growth_stages[1].user_action_beginner": ("growth_stages", 1, "user_action_beginner"),
    "growth_stages[1].user_action_seasoned": ("growth_stages", 1, "user_action_seasoned"),
    "tips_by_stage.spear_emergence[0].text_beginner":
        ("tips_by_stage", "spear_emergence", 0, "text_beginner"),
    "tips_by_stage.spear_emergence[0].text_seasoned":
        ("tips_by_stage", "spear_emergence", 0, "text_seasoned"),
    "notifications[1].body_seasoned": ("notifications", 1, "body_seasoned"),
}
CONTROL_SHA16 = {
    "description_beginner": "3310bc7a1dc92b1a",
    "description_seasoned": "e880c268b2ecfe08",
    "watering.schedule_by_stage[1].note_seasoned": "de9e7acd71964162",
    "growth_stages[1].user_action_beginner": "3efb0fac23e6783e",
    "growth_stages[1].user_action_seasoned": "bd58dc9473ebb7cf",
    "tips_by_stage.spear_emergence[0].text_beginner": "c987f65ceeabe084",
    "tips_by_stage.spear_emergence[0].text_seasoned": "7e8b73eb98b0104f",
    "notifications[1].body_seasoned": "db0f73c26537f59d",
}

# The ONLY leaf-path prefixes this pass may move. Anything else is a defect.
ALLOWED_PREFIXES = (
    "verification_status.open_findings[39].finding",
    "harvest_ready_sources",
    "harvest_ready_anchoring_urls",
    "failure_diagnostics[0].next_season_tip_seasoned",
)


def fail(msg):
    sys.exit(f"ABORT: {msg}")


def dig(obj, path):
    for k in path:
        obj = obj[k]
    return obj


def sha16(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def leaves(obj, pat="", out=None):
    """Flatten to {dotted.path[i]: scalar} so the footprint can be diffed exactly."""
    if out is None:
        out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            leaves(v, f"{pat}.{k}" if pat else k, out)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            leaves(v, f"{pat}[{i}]", out)
    else:
        out[pat] = obj
    return out


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
    asps = [c for c in data["crops"] if c.get("slug") == "asparagus"]
    if len(asps) != 1:
        fail(f"expected exactly 1 asparagus crop, found {len(asps)}")
    asp = asps[0]
    before = leaves(asp)

    catalog = data["source_catalog"]

    # --- pre-state: assert every value this pass is about to overwrite --------------------
    findings = asp["verification_status"]["open_findings"]
    if len(findings) != EXPECT_FINDINGS_LEN:
        fail(f"open_findings length {len(findings)} != {EXPECT_FINDINGS_LEN}")
    finding = findings[FINDING_IDX]["finding"]
    got = hashlib.sha256(finding.encode("utf-8")).hexdigest()
    if got != EXPECT_FINDING_SHA:
        fail(f"open_findings[{FINDING_IDX}].finding drifted\n  have sha {got}\n"
             f"  want sha {EXPECT_FINDING_SHA}")
    for old, _new in FINDING_EDITS:
        n = finding.count(old)
        if n != 1:
            fail(f"finding clause occurs {n} times, expected exactly 1: {old[:70]!r}")
    print(f"pre-state OK: open_findings[{FINDING_IDX}].finding "
          f"({len(finding)} chars, {len(FINDING_EDITS)} clauses matched once each)")

    if asp.get("harvest_ready_sources") != EXPECT_SOURCES:
        fail(f"drift on harvest_ready_sources\n  have: {asp.get('harvest_ready_sources')!r}\n"
             f"  want: {EXPECT_SOURCES!r}")
    if asp.get("harvest_ready_anchoring_urls") != EXPECT_ANCHORS:
        fail("drift on harvest_ready_anchoring_urls\n"
             f"  have: {asp.get('harvest_ready_anchoring_urls')!r}\n  want: {EXPECT_ANCHORS!r}")
    print(f"pre-state OK: harvest_ready_sources {EXPECT_SOURCES} + {len(EXPECT_ANCHORS)} anchors")

    tip = asp["failure_diagnostics"][0].get("next_season_tip_seasoned")
    if tip != EXPECT_TIP:
        fail(f"drift on failure_diagnostics[0].next_season_tip_seasoned\n"
             f"  have: {tip!r}\n  want: {EXPECT_TIP!r}")
    print("pre-state OK: failure_diagnostics[0].next_season_tip_seasoned")

    # --- pre-state invariants this pass must NOT disturb -----------------------------------
    ramp = {e["bed_year"]: e["weeks"] for e in asp["harvest_ramp_weeks"]}
    if ramp.get(5) != [6, 10]:
        fail(f"harvest_ramp_weeks bed year 5 is {ramp.get(5)!r}, expected [6, 10]; the "
             f"1c rewrite is only correct against the widened mature ramp")
    for label, path in CONTROL_STRINGS.items():
        s = dig(asp, path)
        if sha16(s) != CONTROL_SHA16[label]:
            fail(f"control string {label} drifted before this pass ran (sha {sha16(s)})")
        if "six to eight" not in s and "six-to-eight" not in s:
            fail(f"control string {label} no longer carries the superseded figure; the "
                 f"owed-work registration in the record would be wrong")
    print(f"control OK: {len(CONTROL_STRINGS)} descriptive strings verified pre-apply "
          f"(all still carry the superseded six-to-eight-week figure)")

    # --- 1b admission checks, BEFORE applying ---------------------------------------------
    if set(NEW_SOURCES) != set(NEW_ANCHORS):
        fail("NEW_SOURCES and NEW_ANCHORS disagree; every listed source needs an anchor and "
             "no anchor may survive for a source no longer listed")
    if len(NEW_SOURCES) != len(set(NEW_SOURCES)):
        fail("NEW_SOURCES contains a duplicate id")
    for s in NEW_SOURCES:
        if s not in catalog:
            fail(f"{s} is not in source_catalog; this pass adds nothing to the catalog")
        if catalog[s].get("tier") != "T1":
            fail(f"{s} is tier {catalog[s].get('tier')!r}, not T1")
    if not NEW_SOURCES:
        fail("BLOCKED: dropping msu_ext would leave harvest_ready_sources empty")
    for s, u in NEW_ANCHORS.items():
        if not u.startswith("https://"):
            fail(f"anchor for {s} is not an https URL: {u!r}")
    print(f"admission OK: {len(NEW_SOURCES)} source ids, all in source_catalog, all T1, "
          f"all https-anchored")

    # --- apply -----------------------------------------------------------------------------
    new_finding = finding
    for old, new in FINDING_EDITS:
        new_finding = new_finding.replace(old, new, 1)
    if new_finding == finding:
        fail("finding was not modified")
    findings[FINDING_IDX]["finding"] = new_finding

    asp["harvest_ready_sources"] = list(NEW_SOURCES)
    asp["harvest_ready_anchoring_urls"] = {
        s: {"url": NEW_ANCHORS[s], "verified": VERIFIED_ON} for s in NEW_SOURCES
    }
    asp["failure_diagnostics"][0]["next_season_tip_seasoned"] = NEW_TIP
    print(f"applied: finding {len(finding)} -> {len(new_finding)} chars, "
          f"harvest_ready_sources {len(EXPECT_SOURCES)} -> {len(NEW_SOURCES)} ids, "
          f"1 failure-diagnostic clause")

    # --- post: the control group must be exactly where it started --------------------------
    for label, path in CONTROL_STRINGS.items():
        if sha16(dig(asp, path)) != CONTROL_SHA16[label]:
            fail(f"control string {label} was MODIFIED by this pass")
    print(f"control OK: {len(CONTROL_STRINGS)} descriptive strings untouched post-apply")

    # --- post: no em dash anywhere this pass wrote, and no stale claims ---------------------
    written = [new_finding, NEW_TIP]
    for s in written:
        if "\u2014" in s:
            fail(f"em dash in copy this pass wrote: {s[:60]!r}")
    if "NINE cells" in new_finding:
        fail("the NINE-cell count survived the edit")
    if "now agree." in new_finding:
        fail("the 'now agree' over-claim survived the edit")
    if "six to eight weeks on bearing beds" in NEW_TIP:
        fail("the prescriptive six-to-eight-week cap survived the 1c rewrite")

    # --- post: the semantic footprint is exactly the four named fields ----------------------
    after = leaves(asp)
    moved = sorted(
        set(k for k in set(before) | set(after) if before.get(k, object()) != after.get(k, object()))
    )
    stray = [k for k in moved if not k.startswith(ALLOWED_PREFIXES)]
    if stray:
        fail("footprint escaped the four named fields:\n  " + "\n  ".join(stray))
    print(f"footprint OK: {len(moved)} leaf path(s) moved, all inside the four named fields")
    for k in moved:
        print(f"    {k}")

    # --- post: every invariant this arc shipped must return zero, BEFORE writing ------------
    sys.path.insert(0, "tools")
    from harvest_duration_gate import (
        duration_violations, ramp_violations, ramp_prose_violations, stop_rule_violations,
    )
    from zone_order_gate import zone_order_violations
    for name, fn in (("ramp_violations", ramp_violations),
                     ("ramp_prose_violations", ramp_prose_violations),
                     ("stop_rule_violations", stop_rule_violations),
                     ("duration_violations", duration_violations),
                     ("zone_order_violations", zone_order_violations)):
        residue = fn(asp)
        if residue:
            fail(f"{name} fires after repair:\n  " + "\n  ".join(residue))
        print(f"invariant OK: {name} returns 0 on the repaired crop")

    # --- post: sources/anchors stay a one-for-one pair (whole_crop_gate F, in miniature) -----
    if set(asp["harvest_ready_sources"]) != set(asp["harvest_ready_anchoring_urls"]):
        fail("harvest_ready_sources and harvest_ready_anchoring_urls are not one-for-one")
    for s, rec in asp["harvest_ready_anchoring_urls"].items():
        if not rec.get("url", "").startswith("https://") or not rec.get("verified"):
            fail(f"malformed anchoring entry for {s}: {rec!r}")
    print("invariant OK: harvest_ready_* sources and anchors are one-for-one and well-formed")

    out = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    if out.endswith("\n"):
        fail("trailing newline would be written")

    if not write:
        print("\nDRY RUN -- re-run with --write to apply")
        print(f"  open_findings[{FINDING_IDX}].finding   3 clause corrections "
              f"(NINE->TEN, 6-10 span, 'now agree')")
        print(f"  harvest_ready_sources          {EXPECT_SOURCES} ->")
        print(f"                                 {NEW_SOURCES}")
        print(f"  harvest_ready_anchoring_urls   REBUILT one-for-one ({len(NEW_SOURCES)} "
              f"entries, verified {VERIFIED_ON})")
        print("  failure_diagnostics[0].next_season_tip_seasoned  clause REWRITTEN")
        return

    with open(PATH, "w", encoding="utf-8", newline="") as f:
        f.write(out)
    new = hashlib.sha256(open(PATH, "rb").read()).hexdigest()
    print(f"\nWRITTEN. canonical {sha[:8]} -> {new[:8]}")
    print(f"  full new SHA: {new}")


if __name__ == "__main__":
    main()
