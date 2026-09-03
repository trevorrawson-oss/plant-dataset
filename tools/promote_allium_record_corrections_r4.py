#!/usr/bin/env python3
"""ALLIUM RECORD CORRECTIONS, ROUND 4 -- onion thrips on five crops. Base 9d2031ff (after r3).

The record on garlic, onion, shallot, leek and spring-onion said: "Keep plants vigorous and watered,
hose off light infestations, and rotate away from alliums." Twelve documents were fetched and read
this session (UC IPM home-and-landscape and agriculture pages, USU x2, UMass, Wisconsin, PNW x3,
Cornell x3, UMD x2). A search summary counted for nothing.

* "ROTATE AWAY FROM ALLIUMS" is supported for thrips in NONE of them. UC IPM's only "rotation" is
  insecticide mode-of-action; Clemson's four-year rotation sits in its DISEASE paragraph; the
  keyword sweep of the UC IPM agriculture page found no sentence containing rotate, volunteer,
  debris, cull, residue, nitrogen, mulch or resistant. The claim comes out of every record and the
  two SHIPPED `crop_rotation` rungs (garlic, spring-onion) are REPLACED, at the same cultural tier
  and the same ladder position, by `garden_sanitation`, which is what the documents actually say.
* What IS supported goes in, each claim on at least two documents:
  - volunteers and debris: USU "Remove or destroy volunteer onion plants and debris. Onion plant
    matter left on the soil surface can harbor thrips during the winter"; UMass "Practice good field
    sanitation at the end of the season ... Eliminate volunteers."; Wisconsin "Remove plant debris
    from gardens"; PNW leek/shallot "Sanitation is very important. Volunteers should be rogued out."
  - neighbors: UC IPM ag "Avoid planting onions near grain or alfalfa fields ... thrips ... migrate to
    onion fields when the grain senesces, or when the alfalfa is cut."; UMass "Avoid planting onions
    near alfalfa, wheat or clover"; USU "Avoid planting onions adjacent to grain and alfalfa fields."
  - nitrogen: UC IPM home "avoid excessive applications of nitrogen fertilizer, which may promote
    higher populations of thrips"; USU "Moderate, consistent availability of nitrogen has been
    associated with ... reduced onion thrips densities"; UMD "Excess nitrogen promotes rapid, tender
    growth which is often more attractive to thrips".
  - vigor is TOLERANCE, not fewer thrips: UC IPM home "keep plants vigorous and increase their
    tolerance to thrips damage. Keep plants well irrigated"; UMass "Healthy vigorous plants can
    tolerate moderate populations." The record's "keep plants vigorous" survives, reframed.
  - the hose: USU onions-in-the-garden "apply a stiff spray of water to wash thrips from plants";
    UMD "knock them off with a strong jet of plain water from a garden hose"; UC IPM ag and PNW carry
    the hedge ("Overhead irrigation and rainfall suppress thrips numbers, but pesticide applications
    are often still necessary"). Kept, as a light-infestation measure.
  - straw mulch: USU "Straw or other mulch placed on the plant bed has been shown to reduce thrips
    populations."; UMass "Use straw mulch to deter thrips." The catalog's `straw_mulch` is scoped
    fungal_foliar/disease_general, so NO rung is authored for it here; the record carries the claim
    and the widening is catalog r11.
  - natural enemies: UC IPM home "green lacewings, minute pirate bugs ... help to control
    plant-feeding thrips. To conserve ... avoid persistent pesticides".
  - weedy edges (leek): PNW leek/shallot "Cultivating nearby weedy areas early in the year reduces
    the potential of a thrips problem when the weeds begin to dry out."
* HUNT BEFORE DOWNGRADING, again: the vigor and hose claims were declared unsupported off UC IPM's
  AGRICULTURE page and are supported on its HOME-AND-LANDSCAPE page (vigor) and on USU's and UMD's
  home-garden pages (hose). Same institutions, different documents.
* Anchors move off pages that do not discuss thrips management: UMN growing-garlic contains no
  "thrips" at all; UMN growing-onions and growing-leeks carry no thrips management; Clemson's is a
  one-clause mention. Each record now cites four documents that do: USU's onion thrips fact sheet
  (or the PNW leek-and-shallot page for leek and shallot), UMass, UC IPM home-and-landscape, UMD.
* chives' thrips entry is NOT touched: it never carried the rotation claim and its vigor framing is
  already tolerance ("Keeping plants unstressed and watered blunts outbreaks" is the one hedge to
  revisit at batch-24 authoring, not here).

SCOPE: 10 prose fields (management_* on 5 crops), 2 shipped rungs REPLACED in place (method + both
notes; 6 leaves), 5 source sets. No rung added or removed (3243 -> 3243), no id, no name, no type,
no severity, no catalog.
"""
import argparse, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "9d2031ff5ba3abd7a61fe6f0d02715b67d3d0f880cb9d89c0f1729e52df48e8b"
VERIFIED = "2026-09-03"

THRIPS = "Onion thrips"
CROPS = ("garlic", "onion", "shallot", "leek", "spring-onion")
TARGETS = tuple((c, THRIPS) for c in CROPS)
SHIPPED = (("garlic", THRIPS), ("spring-onion", THRIPS))

USU_THRIPS = "https://extension.usu.edu/pests/research/onion-thrips"
UMASS_THRIPS = "https://www.umass.edu/agriculture-food-environment/vegetable/fact-sheets/onion-thrips"
UC_HOME = "https://ipm.ucanr.edu/home-and-landscape/thrips/"
UMD_HOME = "https://extension.umd.edu/resource/thrips-home-gardens"
PNW_LEEK = "https://pnwhandbooks.org/insect/vegetable/vegetable-pests/hosts-pests/leek-shallot-thrips"

_OLD_S = ("Keep plants vigorous and watered, hose off light infestations, and rotate away from "
          "alliums; treat persistent outbreaks per local extension guidance.")
_OLD_S_LEEK = ("Keep plants vigorous and evenly watered, hose off light infestations, and rotate away "
               "from alliums; treat persistent outbreaks per local extension guidance.")
_TAIL_B = " For heavy infestations, ask your local extension office what to use."

PROSE = {
 ("garlic", THRIPS, "management_seasoned"): (
  _OLD_S,
  "Clear volunteer garlic and onions and the crop debris after harvest, since thrips overwinter in "
  "allium material left on the surface, and keep the planting away from small grains, alfalfa or "
  "clover, which shed thrips into alliums when they dry down or are cut. Feed nitrogen adequately "
  "but not heavily, since excess promotes thrips, and keep plants well watered: vigor buys tolerance "
  "of the feeding rather than fewer thrips. A stiff spray of water into the leaf folds knocks a light "
  "infestation back, straw mulch on the bed has been shown to reduce populations, and minute pirate "
  "bugs and lacewings do real work where broad-spectrum sprays are avoided. Treat persistent "
  "outbreaks per local extension guidance."),
 ("garlic", THRIPS, "management_beginner"): (
  "Keep the plants healthy and watered, spray them off with water if thrips are light, and do not "
  "plant garlic where onions or garlic grew last year." + _TAIL_B,
  "After harvest, pull any garlic or onion plants left in the bed and clear the old tops and "
  "trimmings, because thrips spend the winter in that material, and keep garlic away from a grain, "
  "alfalfa or clover patch, which sends thrips into it when it dries or is cut. Go easy on nitrogen, "
  "which makes thrips worse, and keep the plants well watered so they can shrug off the feeding. "
  "Wash light infestations off with a stiff spray from the hose aimed into the leaf folds, and a "
  "straw mulch on the bed helps hold numbers down." + _TAIL_B),
 ("onion", THRIPS, "management_seasoned"): (
  _OLD_S,
  "Clear volunteer onions and crop debris at the end of the season, since thrips overwinter in onion "
  "material left on the surface, and keep the bed away from small grains, alfalfa or clover, which "
  "shed thrips into onions when they dry down or are cut. Hold nitrogen to adequate rather than "
  "heavy, since excess promotes thrips, and keep plants well watered: vigor buys tolerance of the "
  "feeding rather than fewer thrips. A hard spray of water into the leaf folds knocks a light "
  "infestation back, straw mulch on the bed has been shown to reduce populations, and minute pirate "
  "bugs and lacewings help where broad-spectrum sprays are avoided. Treat persistent outbreaks per "
  "local extension guidance."),
 ("onion", THRIPS, "management_beginner"): (
  "Keep the plants healthy and watered, spray them off with water if thrips are light, and do not "
  "plant onions in the same spot every year." + _TAIL_B,
  "At the end of the season pull any onions left in the bed and clear the debris, because that is "
  "where thrips spend the winter, and do not put onions right beside a grain, alfalfa or clover "
  "patch, which sends thrips into them when it dries or is cut. Go easy on nitrogen, which makes "
  "thrips worse, and keep the plants well watered so they can shrug off the feeding. Wash light "
  "infestations off with a hard spray from the hose aimed down into the leaf folds, and a straw "
  "mulch on the bed helps hold numbers down." + _TAIL_B),
 ("shallot", THRIPS, "management_seasoned"): (
  _OLD_S,
  "Rogue out volunteer alliums and clear crop debris at season's end, since thrips overwinter in "
  "allium material left on the surface, and site shallots away from small grains, alfalfa or "
  "clover, which shed thrips into alliums when they dry down or are cut. Keep nitrogen adequate "
  "rather than heavy, since excess promotes thrips, and water well: vigor buys tolerance of the "
  "feeding, not fewer thrips. A hard spray of water into the leaf folds knocks a light infestation "
  "back, straw mulch on the bed deters thrips, and minute pirate bugs and lacewings help where "
  "broad-spectrum sprays are avoided. Treat persistent outbreaks per local extension guidance."),
 ("shallot", THRIPS, "management_beginner"): (
  "Keep the plants healthy and watered, spray them off with water if thrips are light, and do not "
  "plant shallots in the same spot every year." + _TAIL_B,
  "Pull any onion-family plants left in the bed at the end of the season and clear the debris, "
  "because that is where thrips spend the winter, and keep shallots away from a grain, alfalfa or "
  "clover patch, which sends thrips into them when it dries or is cut. Go easy on nitrogen, which "
  "makes thrips worse, and keep the plants well watered so they can shrug off the feeding. Wash "
  "light infestations off with a hard spray from the hose aimed into the leaf folds, and a straw "
  "mulch on the bed helps hold numbers down." + _TAIL_B),
 ("leek", THRIPS, "management_seasoned"): (
  _OLD_S_LEEK,
  "Sanitation carries the most weight: rogue out volunteer alliums and clear crop debris at "
  "season's end, since thrips overwinter in allium material left on the surface, and cultivate "
  "weedy edges early in the year, before they dry down and push thrips onto the crop. Site leeks "
  "away from small grains, alfalfa or clover, which shed thrips when they dry or are cut, hold "
  "nitrogen to adequate rather than heavy, and keep plants evenly watered: vigor buys tolerance of "
  "the feeding, not fewer thrips. A hard spray of water into the leaf folds and the neck knocks a "
  "light infestation back, straw mulch on the bed deters thrips, and minute pirate bugs and "
  "lacewings help where broad-spectrum sprays are avoided. Treat persistent outbreaks per local "
  "extension guidance."),
 ("leek", THRIPS, "management_beginner"): (
  "Keep the plants healthy and well watered, spray them off with water if thrips are light, and do "
  "not plant leeks where you grew onions or leeks last year." + _TAIL_B,
  "At the end of the season pull any onion-family plants left in the bed and clear the debris, "
  "because that is where thrips spend the winter, and keep leeks away from a grain, alfalfa or "
  "clover patch, which sends thrips into them when it dries or is cut. Go easy on nitrogen, which "
  "makes thrips worse, and keep the plants well watered so they can shrug off the feeding. Wash "
  "light infestations off with a hard spray from the hose aimed down into the leaf folds, and a "
  "straw mulch on the bed helps hold numbers down." + _TAIL_B),
 ("spring-onion", THRIPS, "management_seasoned"): (
  _OLD_S,
  "Clear volunteer onions and the leftovers of each sowing as it finishes, since thrips overwinter "
  "in onion material left on the surface, and keep scallions away from small grains, alfalfa or "
  "clover, which shed thrips when they dry down or are cut. Hold nitrogen to adequate rather than "
  "heavy, since excess promotes thrips, and keep plants well watered: vigor buys tolerance of the "
  "feeding rather than fewer thrips, and on a crop sold with its leaves the scarring itself is the "
  "loss. A hard spray of water into the leaf folds knocks a light infestation back, straw mulch on "
  "the bed has been shown to reduce populations, and minute pirate bugs and lacewings help where "
  "broad-spectrum sprays are avoided. Treat persistent outbreaks per local extension guidance."),
 ("spring-onion", THRIPS, "management_beginner"): (
  "Keep the plants healthy and watered, spray them off with water if thrips are light, and do not "
  "plant alliums in the same spot every year." + _TAIL_B,
  "Pull the leftovers of a finished sowing and any volunteer onions rather than letting them stand, "
  "because that is where thrips spend the winter, and keep scallions away from a grain, alfalfa or "
  "clover patch, which sends thrips into them when it dries or is cut. Go easy on nitrogen, which "
  "makes thrips worse, and keep the plants well watered so they can shrug off the feeding. Wash "
  "light infestations off with a hard spray from the hose aimed into the leaf folds, and a straw "
  "mulch on the bed helps hold numbers down." + _TAIL_B),
}
# (crop, name, index, old method) -> (new method, note_beginner, note_seasoned). The rung is
# REPLACED in place: same position, same cultural tier, the method the documents support.
RUNG_REPLACE = {
 ("garlic", THRIPS, 0, "crop_rotation"): (
  "garden_sanitation",
  "Once the garlic is harvested, clear the old tops, trimmings and any volunteer garlic or onions "
  "out of the bed and from around it, and get the material out of the garden rather than leaving it "
  "in a heap. Thrips spend the winter in onion-family debris left on the ground and in volunteer "
  "plants, and next year's population starts from what you leave behind.",
  "Sanitation is the standing cultural control for onion thrips: they overwinter in allium debris "
  "left on the soil surface and in volunteer plants, so clearing tops, trimmings and volunteers "
  "after harvest removes the local carryover. The spring influx that matters most comes from that "
  "debris and from grain or alfalfa drying down nearby, which is why bed choice against those "
  "neighbors sits alongside the cleanup."),
 ("spring-onion", THRIPS, 0, "crop_rotation"): (
  "garden_sanitation",
  "When a sowing is finished, pull the leftovers and any onion volunteers instead of letting them "
  "stand, and clear the trimmings away from the bed. Thrips spend the winter in onion material left "
  "on the ground, so a bed cleared in fall gives them nothing to start from in spring.",
  "Onion thrips overwinter in allium material left on the soil surface and in volunteer plants, so "
  "clearing each finished sowing, its trimmings and any volunteers is the cultural control with the "
  "most support behind it. With scallions the whole plant is sold, so keeping the carryover "
  "population small matters more here than on a bulb crop."),
}
SOURCES = {
 ("garlic", THRIPS): (["umn_ext", "usu_ext"], ["usu_ext", "umass_ext", "uc_ipm", "umd_ext"],
                      {"usu_ext": USU_THRIPS, "umass_ext": UMASS_THRIPS, "uc_ipm": UC_HOME,
                       "umd_ext": UMD_HOME}),
 ("onion", THRIPS): (["umn_ext"], ["usu_ext", "umass_ext", "uc_ipm", "umd_ext"],
                     {"usu_ext": USU_THRIPS, "umass_ext": UMASS_THRIPS, "uc_ipm": UC_HOME,
                      "umd_ext": UMD_HOME}),
 ("shallot", THRIPS): (["umn_ext"], ["osu_ext", "umass_ext", "uc_ipm", "umd_ext"],
                       {"osu_ext": PNW_LEEK, "umass_ext": UMASS_THRIPS, "uc_ipm": UC_HOME,
                        "umd_ext": UMD_HOME}),
 ("leek", THRIPS): (["usu_ext", "umn_ext"], ["osu_ext", "umass_ext", "uc_ipm", "umd_ext"],
                    {"osu_ext": PNW_LEEK, "umass_ext": UMASS_THRIPS, "uc_ipm": UC_HOME,
                     "umd_ext": UMD_HOME}),
 ("spring-onion", THRIPS): (["clemson_hgic"], ["usu_ext", "umass_ext", "uc_ipm", "umd_ext"],
                            {"usu_ext": USU_THRIPS, "umass_ext": UMASS_THRIPS, "uc_ipm": UC_HOME,
                             "umd_ext": UMD_HOME}),
}
EXPECTED_PROSE = 10
EXPECTED_RUNG_LEAVES = 6
EXPECTED_SOURCE_SETS = 5
EXPECTED_RUNGS = 3243

_ROTATE = re.compile(r"\brotat", re.I)
_SAME_SPOT = re.compile(r"do not plant (?:onions|shallots|leeks|garlic|alliums)[^.]*"
                        r"(?:same (?:spot|place)|last year|grew last|the year before)", re.I)
RETIRED = tuple(
 [(t, lambda s: bool(_ROTATE.search(s)), "the rotation claim") for t in TARGETS] +
 [(t, lambda s: bool(_SAME_SPOT.search(s)), "the same-spot rotation instruction") for t in TARGETS] +
 [(t, lambda s: bool(re.search(r"reflective|silver(?:ed|y)?\s+(?:mulch|plastic|film)", s, re.I)),
   "reflective mulch") for t in TARGETS] +
 [(t, lambda s: bool(re.search(r"\bthe guidance\b|guidance (?:names|asks|points)", s, re.I)),
   "the false-attribution device") for t in TARGETS]
)
REQUIRED = tuple(
 [(t, ("management_seasoned",), re.compile(r"\bvolunteer"), "volunteer and debris sanitation")
  for t in TARGETS] +
 [(t, ("management_seasoned", "management_beginner"), re.compile(r"\b(?:grains?|alfalfa|clover)\b"),
   "the grain, alfalfa or clover neighbor") for t in TARGETS] +
 [(t, ("management_seasoned", "management_beginner"), re.compile(r"\bnitrogen\b"),
   "nitrogen restraint") for t in TARGETS] +
 [(t, ("management_seasoned",), re.compile(r"\btolerance\b"), "vigor as TOLERANCE") for t in TARGETS] +
 [(t, ("management_beginner",), re.compile(r"shrug off the feeding"), "vigor as tolerance (beginner)")
  for t in TARGETS] +
 [(t, ("management_seasoned", "management_beginner"), re.compile(r"straw mulch"), "straw mulch")
  for t in TARGETS] +
 [(t, ("management_beginner",), re.compile(r"spend the winter"), "where thrips overwinter (beginner)")
  for t in TARGETS]
)
SURVIVE = {t: ("Thrips tabaci",) for t in TARGETS}

BRITISH = (r"\bbin\b", r"colour", r"fortnight", r"whilst", r"\bautumn\b", r"mould", r"practise",
           r"favour", r"sulphur")
ABSOLUTES = ("always", "never", "completely", "totally", "harmless", "guaranteed", "eliminate",
             "eliminates")


def serialize(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def by_slug(data):
    return {c["slug"]: c for c in data["crops"]}


def problems(crop):
    return [p for f in ("pests", "diseases") for p in crop.get(f) or []]


def find_problem(data, slug, name):
    c = by_slug(data).get(slug)
    if c is None:
        raise SystemExit("REFUSED: crop %s is not on the roster" % slug)
    hits = [p for p in problems(c) if p.get("name") == name]
    if len(hits) != 1:
        raise SystemExit("REFUSED: %s has %d problems named %r, expected exactly 1"
                         % (slug, len(hits), name))
    return hits[0]


def rung_count(data):
    return sum(len(p.get("control_ladder") or []) for c in data["crops"] for p in problems(c))


def snapshot(data):
    snap = {}

    def walk(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, path + (str(k),))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, path + ("[%d]" % i,))
        else:
            snap[path] = node
    walk(data, ())
    return snap


def strings_of(p):
    out = [(k, v) for k, v in p.items() if isinstance(v, str)]
    for r in p.get("control_ladder") or []:
        for k in ("note_beginner", "note_seasoned"):
            if isinstance(r.get(k), str):
                out.append(("%s/%s" % (r.get("method"), k), r[k]))
    return out


def hygiene(s):
    bad = []
    if "—" in s or "–" in s:
        bad.append("em/en dash")
    for w in ABSOLUTES:
        if re.search(r"\b%s\b" % w, s, re.I):
            bad.append("absolute:%s" % w)
    for pat in BRITISH:
        if re.search(pat, s, re.I):
            bad.append("british:%s" % pat)
    if re.search(r"\b(?:rung|ladder|tier)s?\b", s, re.I):
        bad.append("ladder vocabulary")
    if re.search(r"\d\s+°F", s):
        bad.append("spaced degF")
    if re.search(r"\bthe guidance\b|'s own sourcing|guidance (?:names|asks|points)", s, re.I):
        bad.append("false-attribution device")
    return bad


# ------------------------------------------------------------------ guards
def check_pins(data):
    sizes = (len(PROSE), len(RUNG_REPLACE), len(SOURCES))
    want = (EXPECTED_PROSE, len(SHIPPED), EXPECTED_SOURCE_SETS)
    if sizes != want:
        raise SystemExit("REFUSED: edit tables hold %d/%d/%d, expected %d/%d/%d" % (sizes + want))
    for key in [k[:2] for k in PROSE] + [k[:2] for k in RUNG_REPLACE] + list(SOURCES):
        if key not in TARGETS:
            raise SystemExit("REFUSED: %s/%s is not a declared target" % key)
    for (slug, name, field), (before, after) in sorted(PROSE.items()):
        p = find_problem(data, slug, name)
        if p.get(field) != before:
            raise SystemExit("REFUSED: %s/%s/%s does not match its pinned text; the record moved"
                             % (slug, name, field))
        if after == before:
            raise SystemExit("REFUSED: %s/%s/%s replacement is identical" % (slug, name, field))
        bad = hygiene(after)
        if bad:
            raise SystemExit("REFUSED: %s/%s/%s replacement: %s" % (slug, name, field, ", ".join(bad)))
    # SHAPE FIRST: a shipped target with no ladder must refuse here, before the rung pins below
    # look for a rung on it and refuse for the narrower reason.
    for slug, name in TARGETS:
        p = find_problem(data, slug, name)
        if (slug, name) in SHIPPED:
            if not p.get("control_ladder") or not p.get("id"):
                raise SystemExit("REFUSED: %s/%s is declared shipped but carries no ladder or id"
                                 % (slug, name))
        elif p.get("control_ladder") is not None or p.get("id") is not None:
            raise SystemExit("REFUSED: %s/%s already carries a ladder or id; this promote must land "
                             "BEFORE batch 24" % (slug, name))
    cm = data["control_methods"]
    for (slug, name, idx, old), (new, nb, ns) in sorted(RUNG_REPLACE.items()):
        if (slug, name) not in SHIPPED:
            raise SystemExit("REFUSED: %s/%s is not a shipped target; it has no rung to replace"
                             % (slug, name))
        lad = find_problem(data, slug, name).get("control_ladder") or []
        if idx >= len(lad) or lad[idx].get("method") != old:
            raise SystemExit("REFUSED: %s/%s rung %d is %r, expected %r"
                             % (slug, name, idx, lad[idx].get("method") if idx < len(lad) else None,
                                old))
        if sum(1 for r in lad if r.get("method") == old) != 1:
            raise SystemExit("REFUSED: %s/%s carries %r more than once; the replacement is ambiguous"
                             % (slug, name, old))
        if new not in cm:
            raise SystemExit("REFUSED: %s/%s replacement method %r is not in control_methods"
                             % (slug, name, new))
        if any(r.get("method") == new for r in lad):
            raise SystemExit("REFUSED: %s/%s already carries %r; the replacement would duplicate it"
                             % (slug, name, new))
        if cm[new].get("tier") != cm[old].get("tier"):
            raise SystemExit("REFUSED: %s/%s replacing %r (%s) with %r (%s) changes the tier at that "
                             "position" % (slug, name, old, cm[old].get("tier"), new, cm[new].get("tier")))
        applies = cm[new].get("applies_to") or []
        if "any" not in applies:
            raise SystemExit("REFUSED: %s/%s replacement %r does not carry applies_to any"
                             % (slug, name, new))
        for label, note in (("note_beginner", nb), ("note_seasoned", ns)):
            if not note or not note.strip():
                raise SystemExit("REFUSED: %s/%s/%s %s is empty" % (slug, name, new, label))
            bad = hygiene(note)
            if bad:
                raise SystemExit("REFUSED: %s/%s/%s %s: %s" % (slug, name, new, label, ", ".join(bad)))
        if nb.strip() == ns.strip():
            raise SystemExit("REFUSED: %s/%s/%s registers are identical" % (slug, name, new))
    for (slug, name), (before, after, anchors) in sorted(SOURCES.items()):
        p = find_problem(data, slug, name)
        if p.get("sources") != before:
            raise SystemExit("REFUSED: %s/%s sources are %r, pinned %r"
                             % (slug, name, p.get("sources"), before))
        if sorted(set(after)) != sorted(after) or not after:
            raise SystemExit("REFUSED: %s/%s new source list is empty or has duplicates" % (slug, name))
        for sid in after:
            if sid not in data["source_catalog"]:
                raise SystemExit("REFUSED: %s/%s cites %r, which is not in source_catalog"
                                 % (slug, name, sid))
            if sid not in anchors:
                raise SystemExit("REFUSED: %s/%s cites %r without a document anchor" % (slug, name, sid))
        for sid in anchors:
            if sid not in after:
                raise SystemExit("REFUSED: %s/%s anchors %r which is not in its new source list"
                                 % (slug, name, sid))
    for slug, name in TARGETS:
        if not any(k[:2] == (slug, name) for k in PROSE) or (slug, name) not in SOURCES:
            raise SystemExit("REFUSED: %s/%s is declared but not fully edited" % (slug, name))


def check_retired_claims(data):
    left = []
    for (slug, name), still_present, label in RETIRED:
        p = find_problem(data, slug, name)
        for where, v in strings_of(p):
            if still_present(v):
                left.append("%s/%s/%s still carries %s" % (slug, name, where, label))
    if left:
        raise SystemExit("REFUSED: %r" % left)
    return len(RETIRED)


def check_no_rotation_rung(data):
    """No thrips ladder may carry crop_rotation afterward, and the two shipped ladders must carry
    garden_sanitation at the replaced position with their length unchanged."""
    for slug, name in TARGETS:
        for r in find_problem(data, slug, name).get("control_ladder") or []:
            if r.get("method") == "crop_rotation":
                raise SystemExit("REFUSED: %s/%s still carries a crop_rotation rung" % (slug, name))
    n = 0
    for (slug, name, idx, _old), (new, _nb, _ns) in RUNG_REPLACE.items():
        lad = find_problem(data, slug, name)["control_ladder"]
        if lad[idx].get("method") != new:
            raise SystemExit("REFUSED: %s/%s rung %d is %r, expected %r after replacement"
                             % (slug, name, idx, lad[idx].get("method"), new))
        n += 1
    return n


def check_required_claims(data):
    missing = []
    for (slug, name), fields, pat, label in REQUIRED:
        p = find_problem(data, slug, name)
        for f in fields:
            if not pat.search(p.get(f) or ""):
                missing.append("%s/%s/%s lacks %s" % (slug, name, f, label))
    if missing:
        raise SystemExit("REFUSED: %r" % missing)
    return sum(len(f) for _t, f, _p, _l in REQUIRED)


def check_survivors(data):
    for (slug, name), phrases in sorted(SURVIVE.items()):
        blob = " ".join(v for _w, v in strings_of(find_problem(data, slug, name)))
        for ph in phrases:
            if ph not in blob:
                raise SystemExit("REFUSED: %s/%s no longer says %r" % (slug, name, ph))
    return sum(len(v) for v in SURVIVE.values())


def check_chives_untouched(pre, data):
    """chives' thrips entry is out of scope and must be byte-identical."""
    post = snapshot(data)
    moved = [k for k in set(pre) | set(post)
             if len(k) > 3 and k[0] == "crops" and pre.get(k) != post.get(k)
             and data["crops"][int(k[1][1:-1])]["slug"] == "chives"]
    if moved:
        raise SystemExit("REFUSED: chives changed: %r" % sorted(moved)[:5])


def apply_to(data):
    check_pins(data)
    for (slug, name, field), (_b, after) in PROSE.items():
        find_problem(data, slug, name)[field] = after
    for (slug, name, idx, _old), (new, nb, ns) in RUNG_REPLACE.items():
        r = find_problem(data, slug, name)["control_ladder"][idx]
        r["method"], r["note_beginner"], r["note_seasoned"] = new, nb, ns
    for (slug, name), (_b, after, anchors) in SOURCES.items():
        p = find_problem(data, slug, name)
        p["sources"] = list(after)
        au = {k: v for k, v in (p.get("anchoring_urls") or {}).items() if k in after}
        for sid, url in anchors.items():
            au[sid] = {"url": url, "verified": VERIFIED}
        p["anchoring_urls"] = {k: au[k] for k in after if k in au}
    return data


def verify_post(pre, data):
    post = snapshot(data)
    added, dropped = set(post) - set(pre), set(pre) - set(post)
    want_owners = set(TARGETS)

    def owner(k):
        if len(k) < 4 or k[0] != "crops" or k[2] not in ("pests", "diseases"):
            return None
        try:
            crop = data["crops"][int(k[1][1:-1])]
            return crop["slug"], crop[k[2]][int(k[3][1:-1])].get("name")
        except (ValueError, IndexError, KeyError):
            return None

    for k in added | dropped:
        if "anchoring_urls" not in k and "sources" not in k:
            raise SystemExit("REFUSED: a key was added or dropped outside sources/anchoring_urls: "
                             "%r" % (k,))
        if owner(k) not in want_owners:
            raise SystemExit("REFUSED: a key was added or dropped outside the declared targets: "
                             "%r" % (k,))
    changed = sorted(k for k in set(pre) & set(post) if pre[k] != post[k])
    # NOTHING on a TARGET may change except what this promote pins: the two management fields,
    # the three leaves of the replaced rung, and the source set. A target's cause text moving is
    # invisible to the owner check and to the counts, so each changed leaf is matched to a pin.
    rung_idx = {(slug, name): idx for (slug, name, idx, _o) in RUNG_REPLACE}
    for k in changed:
        o = owner(k)
        if o not in want_owners:
            continue
        if "sources" in k or "anchoring_urls" in k:
            continue
        if "control_ladder" in k:
            if int(k[5][1:-1]) != rung_idx.get(o, -1) or k[-1] not in ("method", "note_beginner",
                                                                       "note_seasoned"):
                raise SystemExit("REFUSED: %s/%s rung %s/%s is not the replaced rung of this promote"
                                 % (o[0], o[1], k[5], k[-1]))
            continue
        if k[-1] not in ("management_seasoned", "management_beginner"):
            raise SystemExit("REFUSED: %s/%s/%s is not a pinned field of this promote"
                             % (o[0], o[1], k[-1]))
    n_prose = sum(1 for k in changed if "control_ladder" not in k
                  and k[-1] in ("management_seasoned", "management_beginner"))
    if n_prose != EXPECTED_PROSE:
        raise SystemExit("REFUSED: %d prose leaves changed, expected %d" % (n_prose, EXPECTED_PROSE))
    n_rung = sum(1 for k in changed if "control_ladder" in k)
    if n_rung != EXPECTED_RUNG_LEAVES:
        raise SystemExit("REFUSED: %d rung leaves changed, expected %d" % (n_rung, EXPECTED_RUNG_LEAVES))
    for (slug, name, field), (_b, after) in PROSE.items():
        if find_problem(data, slug, name).get(field) != after:
            raise SystemExit("REFUSED: %s/%s/%s did not receive its replacement" % (slug, name, field))
    for (slug, name, idx, _old), (new, nb, ns) in RUNG_REPLACE.items():
        r = find_problem(data, slug, name)["control_ladder"][idx]
        if (r.get("method"), r.get("note_beginner"), r.get("note_seasoned")) != (new, nb, ns):
            raise SystemExit("REFUSED: %s/%s rung %d did not receive its replacement" % (slug, name, idx))
    for (slug, name), (_b, after, anchors) in SOURCES.items():
        p = find_problem(data, slug, name)
        if p.get("sources") != list(after):
            raise SystemExit("REFUSED: %s/%s sources are %r, expected %r"
                             % (slug, name, p.get("sources"), list(after)))
        if list(p.get("anchoring_urls") or {}) != list(after):
            raise SystemExit("REFUSED: %s/%s anchoring_urls keys %r do not match its sources %r"
                             % (slug, name, list(p.get("anchoring_urls") or {}), list(after)))
        for sid, url in anchors.items():
            if (p["anchoring_urls"].get(sid) or {}).get("url") != url:
                raise SystemExit("REFUSED: %s/%s anchor %s is %r, expected %r"
                                 % (slug, name, sid, p["anchoring_urls"].get(sid), url))
    touched = {owner(k) for k in changed}
    if touched - want_owners:
        raise SystemExit("REFUSED: leaves changed outside the declared targets: %r"
                         % sorted(touched - want_owners))
    if rung_count(data) != EXPECTED_RUNGS:
        raise SystemExit("REFUSED: %d rungs after, expected %d; this promote replaces in place"
                         % (rung_count(data), EXPECTED_RUNGS))
    return len(changed)


def check_catalog_untouched(before_cm, before_sc, data):
    if serialize(data["control_methods"]) != before_cm:
        raise SystemExit("REFUSED: control_methods changed; this promote mints nothing")
    if serialize(data["source_catalog"]) != before_sc:
        raise SystemExit("REFUSED: source_catalog changed; every id cited here already exists")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("canonical", nargs="?", default=CANONICAL)
    ap.add_argument("--canonical", dest="canonical_flag", default=None)
    ap.add_argument("--expect-sha", default=None)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    a.canonical = a.canonical_flag or a.canonical

    raw = open(a.canonical, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    expect = a.expect_sha or BASE_SHA
    if sha != expect:
        raise SystemExit("REFUSED: base SHA %s != expected %s" % (sha[:16], expect[:16]))

    data = json.loads(raw.decode("utf-8"))
    pre = snapshot(data)
    before_cm = serialize(data["control_methods"])
    before_sc = serialize(data["source_catalog"])

    apply_to(data)
    n = verify_post(pre, data)
    check_catalog_untouched(before_cm, before_sc, data)
    retired = check_retired_claims(data)
    swapped = check_no_rotation_rung(data)
    required = check_required_claims(data)
    survivors = check_survivors(data)
    check_chives_untouched(pre, data)

    blob = serialize(data)
    print("leaves changed      : %d (%d prose, %d rung leaves, %d source sets)"
          % (n, EXPECTED_PROSE, EXPECTED_RUNG_LEAVES, EXPECTED_SOURCE_SETS))
    print("retired claims gone : %d/%d" % (retired, len(RETIRED)))
    print("rungs replaced      : %d crop_rotation -> garden_sanitation; rungs %d -> %d"
          % (swapped, EXPECTED_RUNGS, rung_count(data)))
    print("required claims in  : %d registers" % required)
    print("taxa survive        : %d" % survivors)
    print("base  SHA           : %s" % sha)
    print("post  SHA           : %s" % hashlib.sha256(blob).hexdigest())
    if a.apply:
        with open(a.canonical, "wb") as fh:
            fh.write(blob)
        print("APPLIED -> %s" % a.canonical)
    else:
        print("dry run; pass --apply to write")


if __name__ == "__main__":
    main()
