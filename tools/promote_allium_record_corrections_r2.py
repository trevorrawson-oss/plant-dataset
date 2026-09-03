#!/usr/bin/env python3
"""ALLIUM RECORD CORRECTIONS, ROUND 2 -- the two leek entries whose netting advice would FAIL.
Base 80519a28.

Both entries were UK-sourced (RHS) and both told a US reader to net DURING flight windows that are
not the US windows, which is the one instruction on this pest that has to be right. Every quotation
below was fetched and read this session; a search summary counted for nothing.

1. LEEK / LEEK MOTH -- the months in the record are RHS's LARVAL FEEDING months ("larvae feeding on
   the plants in May to June and August to October") relabelled as flight periods, and RHS publishes
   no adult-flight months at all. The US picture, from Cornell's Leek Moth Identification and
   Management Guide (doc_764) and confirmed by UVM's 2022 fact sheet and UNH: "There are 2 to 3
   generations per year in New York" / "There are three generations of this pest" (UNH); "three
   flight periods ... The first flight (the overwintering generation) begins in mid-late April,
   ending in mid-May. The second flight period ... begins in mid-June, ending in early to mid-July.
   The third flight period begins in late July, ending in mid- to late August"; "Injury first appears
   in June, and following generations increase damage throughout the field through September". The
   cover instruction inverts: "It is important to have the row cover in place over the crop BEFORE
   the moths emerge from their overwintering sites in spring ... Moths may emerge extremely early
   during warm spells in March"; emergence is anchored to temperature, "when temperatures reach
   10 C (50 F)". RHS itself says "The mesh should be kept in place for the entire growing season",
   which the record also misread. The record said nothing about scope: "As of 2013, they have been
   found in Northern New York and Northern New England" (UVM), with UNH reporting four New Hampshire
   counties in 2025. Also corrected: on leek's FLAT leaves the symptom is holes chewed through the
   folded inner leaves ("As they move toward the center of the plant, they leave a series of holes in
   the inner leaves"); the see-through "windowpane" is Cornell's HOLLOW-leaf symptom for "onions,
   chives and shallots". Bt: "Laboratory studies indicated that all but DiPel significantly reduced
   leek moth larval populations", so the record no longer implies Bt is the organic answer.
   Sources move RHS -> Cornell + UNH. UVM's fact sheet was read and agrees on every figure; it was
   not minted as a catalog id because nothing carried here rests on it alone.

2. LEEK / ALLIUM LEAF MINER -- the window "March to April and September to November" and "the
   autumn generation is usually the most damaging" are RHS's sentences ("Peak adult activity is
   March to April and September to November"), and the record's US citation, UMD's growing-leeks
   page, contains zero flight dates: its only leafminer content is a link to a page that now 404s.
   Chives and shallot already carry the US window from UMD's leafminer page ("Adults emerge in late
   winter (March) into spring (throughout April, perhaps into May) ... emerge in the autumn
   (September / October)"), confirmed by Cornell IPM ("between late March and late April", "early
   September") and UMass. The fall-is-worse claim SURVIVES, now sourced and explained: "Fall leeks are
   often the most damaged crop because they are the only allium crop remaining in fields during the
   fall flight" (UMass). The cover instruction inverts, with DIRECT leek evidence: "Covering plants in
   February, prior to the emergence of adults" (UMD); "before the flight period starts (spring:
   March/April and fall: September/October) until 8 weeks after the tentative start of the flight"
   (Cornell); "Waiting to cover leeks two weeks after the start of ALM's fall flight has been shown to
   result in higher densities of ALM larvae and pupae in the plants" (UMass). The trap precondition
   is sourced too: "Row covers should not be used in fields which were infested with the previous
   generation of ALM" (UMass). The mechanism is corrected: pupae overwinter "in plant tissue or
   surrounding soil" (UMD), not simply "in the soil". Sources move RHS + UMD/growing-leeks ->
   UMD/allium-onion-leafminer + Cornell + UMass. The entry's NAME, "Allium leaf miner", is NOT
   touched: the spelling is adjudicated (PLA-448 s2) but the rename waits for the post-PLA-8 naming
   pass, and prose may spell the insect the way every US source does.

CROSS-CROP CONSISTENCY: chives and shallot agree with each other on the leafminer window and
disagreed with leek. After this promote leek carries the same "September into October" phrase they
do, and the guard asserts it against the SIBLINGS' live text rather than against a constant.

SCOPE: 12 prose fields and 2 source sets on 2 problems of ONE crop. No severity, no rung, no id, no
name, no type, no catalog, no other crop. Both problems are unladdered and carry no id; batch 24
will pin `leek-moth` and `allium-leafminer` on them, and the batch-24 spelling pin anchors on
"Phytomyza gymnostoma" surviving in leek's prose, which a guard here asserts.
"""
import argparse, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
BASE_SHA = "80519a28548586aedd9754a664f1618b722fb55976d8eb6c3314891ddc5c328f"
VERIFIED = "2026-09-03"

CROP = "leek"
TARGETS = ((CROP, "Leek moth"), (CROP, "Allium leaf miner"))
# The two crops whose leafminer window leek must now agree with. Read LIVE, never a constant.
SIBLINGS = (("chives", "Allium leafminer"), ("shallot", "Allium leafminer"))
SIBLING_PHRASE = "September into October"

PROSE = {
 (CROP, "Leek moth", "identification_seasoned"): (
  "Pale, papery window-pane patches where caterpillars have eaten the inner leaf tissue, then "
  "tunnels bored down into the shaft; two generations feed roughly May to June and August to "
  "October.",
  "On leek's flat leaves the larvae feed on the young leaves and inside the folded ones at the heart "
  "of the plant, chewing through the folds so the inner leaves open with a line of holes, and "
  "sometimes mining down toward the base; the see-through window-pane patch with the outer skin left "
  "intact is the hollow-leaf symptom seen on onions and chives. Split a damaged leaf to find the "
  "slender, creamy yellow larva or the frass it leaves behind, which stays visible after it has left "
  "to pupate in a loose, net-like cocoon on the foliage. Injury first shows in June and builds "
  "through September as two to three generations follow one another."),
 (CROP, "Leek moth", "identification_beginner"): (
  "Whitish, see-through papery patches on the leaves where small caterpillars have eaten the inside, "
  "and later tunnels down into the stem. There are two waves, in late spring and again in late "
  "summer.",
  "Small caterpillars chew inside the folded young leaves at the heart of the plant, so as the leaves "
  "open you see a row of holes and pale chewed patches, sometimes with a tunnel running down toward "
  "the base. Pull a damaged leaf apart and look for a slim creamy yellow caterpillar or the dark "
  "crumbs it leaves behind, and check the newest leaves too. Damage starts in June and keeps building "
  "into September, with two or three rounds of caterpillars in a season, and you may find their "
  "little net-like cocoons on the leaves."),
 (CROP, "Leek moth", "cause_seasoned"): (
  "Larvae of the leek moth (Acrolepiopsis assectella), a small brown moth; young caterpillars mine "
  "the foliage and older ones bore into the stems, then pupate in net-like silk cocoons spun on the "
  "leaves.",
  "Larvae of the leek moth (Acrolepiopsis assectella), a European moth about 3/8 inch long, speckled "
  "brown with a white spot halfway down each forewing. Adults overwinter in sheltered plant debris "
  "and emerge once spring temperatures reach about 50°F, sometimes during a warm spell in March, and "
  "lay eggs singly on the leaves; larvae mine and bore through the foliage for two to three weeks, "
  "then pupate in a net-like cocoon on the plant. New York records two to three generations a year, "
  "with flights around mid-April to mid-May, mid-June to mid-July and late July to late August. In "
  "the US it is so far confined to northern New York and northern New England, and leeks take the "
  "heaviest damage of the alliums."),
 (CROP, "Leek moth", "cause_beginner"): (
  "The caterpillars of a small brown moth. The young ones eat the inside of the leaves and the older "
  "ones tunnel into the stem, then spin little net-like cocoons on the plant.",
  "The caterpillars of a small speckled brown moth that arrived from Europe. The moths spend the "
  "winter tucked into old plant debris and come out once spring warms to around 50°F, which can be "
  "as early as March, and there are two or three rounds of caterpillars between then and the end of "
  "summer. So far it is found only in northern New York and northern New England, and leeks get the "
  "worst of it."),
 (CROP, "Leek moth", "management_seasoned"): (
  "Cover the crop with insect-proof mesh through the flight periods, rotate alliums, and find and "
  "crush the white net-like cocoons on the foliage.",
  "Exclusion is the main tool on a garden scale, and timing is what makes it work: have insect "
  "netting or row cover on before the overwintered moths emerge, in very early spring or on the day "
  "of planting if that comes later, sealed at the edges and left in place rather than lifted between "
  "flights. A pheromone trap set by mid-April shows when each flight peaks. Rotate off last year's "
  "allium ground, delay planting past the first emergence where the season allows, remove larvae and "
  "cocoons from the plants, and clear allium debris at the end of the season, since the adults "
  "overwinter in it. Where a spray is warranted, spinosad applied 7 to 10 days after a peak flight is "
  "the organic material with trial support; Bt did not significantly reduce larvae in laboratory "
  "tests."),
 (CROP, "Leek moth", "management_beginner"): (
  "Cover the plants with fine insect netting during late spring and late summer when the moths are "
  "active, move leeks to a new spot each year, and squash any little net-like cocoons you find on the "
  "leaves.",
  "Cover the bed with fine insect netting or row cover before the moths come out in early spring, or "
  "on the same day you plant if that is later, tuck the edges in, and leave it on for the season "
  "instead of taking it off between flights. Put it over a bed that did not grow onions or leeks last "
  "year, because the moths winter in that old debris and can end up under the cover with the crop. "
  "Grow leeks in a different spot each year, pick off caterpillars and their little net-like cocoons "
  "when you see them, and clear out old onion-family leaves and stems at the end of the season, since "
  "that is where the moths spend the winter."),
 (CROP, "Allium leaf miner", "identification_seasoned"): (
  "Neat rows of white dots punched in the leaves by the egg-laying flies, then white legless maggots "
  "and small brown pupae tunneling in leaves and shafts; the autumn generation is usually the most "
  "damaging.",
  "Neat rows of small white dots toward the leaf tips, punched by the egg-laying flies, then straight "
  "mines running down the leaf toward the base; leaves twist and go wavy as the white, headless "
  "maggots, up to about 1/3 inch, feed their way into the sheath and base, where the brown pupae "
  "lodge. The punctures and mines open the plant to bacterial and fungal rots. Fall leeks take the "
  "worst of it, since by then they are often the only allium left standing for the second flight."),
 (CROP, "Allium leaf miner", "identification_beginner"): (
  "Lines of small white dots on the leaves, then white maggots and little brown pupae tunneling "
  "inside the leaves and stem. The fall wave does the most damage.",
  "A neat line of small white dots near the tip of a leaf is the first sign, left by the flies as "
  "they lay. Then thin tunnels run down the leaf, the leaves can go wavy and twisted, and small white "
  "maggots and little brown pupae turn up down in the base of the plant. Fall leeks get hit hardest, "
  "because by then they are often the only onion-family crop still in the ground."),
 (CROP, "Allium leaf miner", "cause_seasoned"): (
  "The allium leaf miner (Phytomyza gymnostoma), an increasingly widespread fly with two generations "
  "a year, active roughly March to April and again September to November; secondary rots often "
  "follow the tunneling.",
  "The allium leafminer (Phytomyza gymnostoma), a small gray-black fly with a yellow-orange patch on "
  "its head, first found in Pennsylvania in 2015 and now across the mid-Atlantic and Northeast. It "
  "has two generations a year: adults emerge from late March through April, sometimes into May, then "
  "the pupae rest through summer and a second flight runs from about September into October. Pupae "
  "overwinter in the plant tissue or the soil around it, and the mines and egg punctures open the way "
  "for bacterial and fungal rots."),
 (CROP, "Allium leaf miner", "cause_beginner"): (
  "A fly called the allium leaf miner. It is active in spring and again in fall, and its maggots "
  "tunnel inside, often letting rot set in afterward.",
  "A small fly called the allium leafminer, a newcomer from Europe that turned up in Pennsylvania in "
  "2015 and has spread across the mid-Atlantic and Northeast. The flies are out from late March into "
  "April or May, and again from about September into October, and their maggots tunnel inside the "
  "plant and let rot in behind them. Between flights the pupae wait in old plant tissue or in the "
  "soil right around it."),
 (CROP, "Allium leaf miner", "management_seasoned"): (
  "Cover the crop with insect-proof mesh during the two flight periods (about March to April and "
  "September to November) and rotate alliums, since the flies emerge from pupae in the soil.",
  "Exclusion works, and the timing decides it: put insect netting or row cover on before each flight "
  "begins, by late March for the spring flight and by early September for the fall one, bury the "
  "edges, and keep it on for the whole egg-laying period, roughly eight weeks. Covering fall leeks "
  "two weeks after the flight has started has been shown to leave more larvae and pupae in the "
  "plants, not fewer. Do not cover ground that held infested alliums last season, or the emerging "
  "flies are trapped under it with the crop; rotate instead, and site new plantings as far as you can "
  "from last year's alliums. Transplanting after mid-May and harvesting by early September can dodge "
  "both flights, and destroying infested debris after harvest removes overwintering pupae. Spinosad "
  "is the organic material with trial support, applied twice in the two to four weeks after the "
  "flies first appear."),
 (CROP, "Allium leaf miner", "management_beginner"): (
  "Cover the plants with fine insect netting in spring and again in fall when the flies are active, "
  "and move leeks to a new spot each year.",
  "Cover the bed with fine insect netting or row cover before the flies show up, by late March for "
  "the spring flight and by early September for the fall one, bury the edges so nothing crawls under, "
  "and leave it on for about eight weeks. Putting it on late does not help: leeks covered two weeks "
  "into the fall flight ended up with more maggots, not fewer. Do not cover a bed that grew leeks or "
  "onions last year, or you trap the flies coming up out of the ground under the cover with the crop. "
  "Move leeks to a fresh spot each year, as far from last year's onion-family beds as you can, and "
  "clear out the old plants after harvest, because the pupae wait there for the next flight."),
}
SOURCES = {
 (CROP, "Leek moth"): (
   ["rhs"], ["cornell_ext", "unh_ext"],
   {"cornell_ext": "https://rvpadmin.cce.cornell.edu/uploads/doc_764.pdf",
    "unh_ext": "https://extension.unh.edu/blog/2025/07/leek-moth-nh"}),
 (CROP, "Allium leaf miner"): (
   ["rhs", "umd_ext"], ["umd_ext", "cornell_ext", "umass_ext"],
   {"umd_ext": "https://extension.umd.edu/resource/allium-onion-leafminer",
    "cornell_ext": "https://cals.cornell.edu/integrated-pest-management/outreach-education/"
                   "fact-sheets/allium-leafminer",
    "umass_ext": "https://www.umass.edu/agriculture-food-environment/vegetable/fact-sheets/"
                 "allium-leafminer"}),
}
EXPECTED_PROSE = 12
EXPECTED_SOURCE_SETS = 2
RETIRED_SOURCE = "rhs"

# Claims that must be GONE afterward, checked on the WHOLE problem, not just the edited field.
RETIRED = (
 ((CROP, "Leek moth"), lambda t: bool(re.search(r"May to June|August to October", t or "")),
  "the UK larval-feeding months relabelled as flight periods"),
 ((CROP, "Leek moth"), lambda t: bool(re.search(r"\btwo (?:generations|waves)\b", t or "", re.I)),
  "a two-generation count (the US has two to three)"),
 ((CROP, "Leek moth"),
  lambda t: bool(re.search(r"through the flight periods|during late spring and late summer|"
                           r"when the moths are active", t or "", re.I)),
  "netting DURING the flights"),
 ((CROP, "Allium leaf miner"),
  lambda t: bool(re.search(r"March to April|September to November", t or "")),
  "the RHS flight window"),
 ((CROP, "Allium leaf miner"),
  lambda t: bool(re.search(r"during the (?:two )?flight periods|when the flies are active",
                           t or "", re.I)),
  "netting DURING the flights"),
 ((CROP, "Allium leaf miner"),
  lambda t: bool(re.search(r"pupae in the soil\b", t or "", re.I)),
  "the soil-only overwintering mechanism"),
)
# Claims that must be PRESENT afterward, each in the register(s) named, and each ABSENT in the
# pre-state so the check is a measurement rather than a restatement. The suite asserts both.
REQUIRED = (
 ((CROP, "Leek moth"), ("management_seasoned", "management_beginner"),
  re.compile(r"\bbefore\b"), "cover BEFORE the moths emerge"),
 ((CROP, "Leek moth"), ("identification_seasoned", "identification_beginner", "cause_seasoned",
                        "cause_beginner"),
  re.compile(r"\btwo (?:to|or) three (?:generations|rounds)\b"), "the two-to-three generation count"),
 ((CROP, "Leek moth"), ("cause_seasoned", "cause_beginner"),
  re.compile(r"northern New York"), "the US geographic scope"),
 ((CROP, "Leek moth"), ("cause_seasoned", "cause_beginner"),
  re.compile(r"50°F"), "the 50°F emergence anchor"),
 ((CROP, "Allium leaf miner"), ("management_seasoned", "management_beginner"),
  re.compile(r"\bbefore\b"), "cover BEFORE the flight"),
 ((CROP, "Allium leaf miner"), ("management_seasoned", "management_beginner"),
  re.compile(r"\btwo weeks\b"), "the UMass late-cover evidence"),
 ((CROP, "Allium leaf miner"), ("cause_seasoned", "cause_beginner"),
  re.compile(r"late March"), "the US spring window"),
)
# Organism names the batch-24 id pins anchor on. They must SURVIVE the rewrite.
TAXA = {(CROP, "Leek moth"): "Acrolepiopsis assectella",
        (CROP, "Allium leaf miner"): "Phytomyza gymnostoma"}

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
    # The device the source-truth pass found invented at authoring time: a sentence claiming what
    # "the guidance" says. Roughly 15 of 27 were false. Do not write it again.
    if re.search(r"\bthe guidance\b|'s own sourcing|guidance (?:names|asks|points)", s, re.I):
        bad.append("false-attribution device")
    return bad


# ------------------------------------------------------------------ guards
def check_pins(data):
    if len(PROSE) != EXPECTED_PROSE or len(SOURCES) != EXPECTED_SOURCE_SETS:
        raise SystemExit("REFUSED: edit tables hold %d/%d, expected %d/%d"
                         % (len(PROSE), len(SOURCES), EXPECTED_PROSE, EXPECTED_SOURCE_SETS))
    for key in list(PROSE) + [k + ("",) for k in SOURCES]:
        if (key[0], key[1]) not in TARGETS:
            raise SystemExit("REFUSED: %s/%s is not a declared target" % (key[0], key[1]))
    for (slug, name, field), (before, after) in sorted(PROSE.items()):
        p = find_problem(data, slug, name)
        if p.get(field) != before:
            raise SystemExit("REFUSED: %s/%s/%s does not match its pinned text; the record moved"
                             % (slug, name, field))
        if after == before:
            raise SystemExit("REFUSED: %s/%s/%s replacement is identical" % (slug, name, field))
        bad = hygiene(after)
        if bad:
            raise SystemExit("REFUSED: %s/%s/%s replacement: %s" % (slug, name, field,
                                                                    ", ".join(bad)))
    for (slug, name), (before, after, anchors) in sorted(SOURCES.items()):
        p = find_problem(data, slug, name)
        if p.get("sources") != before:
            raise SystemExit("REFUSED: %s/%s sources are %r, pinned %r"
                             % (slug, name, p.get("sources"), before))
        if sorted(set(after)) != sorted(after) or not after:
            raise SystemExit("REFUSED: %s/%s new source list is empty or has duplicates"
                             % (slug, name))
        for sid in after:
            if sid not in data["source_catalog"]:
                raise SystemExit("REFUSED: %s/%s cites %r, which is not in source_catalog"
                                 % (slug, name, sid))
        for sid in anchors:
            if sid not in after:
                raise SystemExit("REFUSED: %s/%s anchors %r which is not in its new source list"
                                 % (slug, name, sid))
        # Every id in the new list must carry a PATHED anchor: a bare catalog root is the
        # citation-cleanup defect class (node bare while catalog pathed).
        for sid in after:
            if sid not in anchors:
                raise SystemExit("REFUSED: %s/%s cites %r without a document anchor"
                                 % (slug, name, sid))
    # Every problem this promote edits must carry BOTH a prose edit and a source set: a target with
    # one and not the other is a half-finished correction.
    for slug, name in TARGETS:
        if not any(k[:2] == (slug, name) for k in PROSE) or (slug, name) not in SOURCES:
            raise SystemExit("REFUSED: %s/%s is declared but not fully edited" % (slug, name))


def check_retired_claims(data):
    """Gone from the WHOLE problem, not just the field that carried the claim."""
    left = []
    for (slug, name), still_present, label in RETIRED:
        p = find_problem(data, slug, name)
        for k, v in p.items():
            if isinstance(v, str) and still_present(v):
                left.append("%s/%s/%s still carries %s" % (slug, name, k, label))
    if left:
        raise SystemExit("REFUSED: %r" % left)
    return len(RETIRED)


def check_required_claims(data):
    """Each claim in EVERY register it is declared for. A correction that lands the new advice in
    the seasoned register and leaves the beginner one vague has fixed it for the reader least
    likely to need it."""
    missing = []
    for (slug, name), fields, pat, label in REQUIRED:
        p = find_problem(data, slug, name)
        for f in fields:
            if not pat.search(p.get(f) or ""):
                missing.append("%s/%s/%s lacks %s" % (slug, name, f, label))
    if missing:
        raise SystemExit("REFUSED: %r" % missing)
    return sum(len(f) for _t, f, _p, _l in REQUIRED)


def check_taxa_survive(data):
    """Batch 24's spelling-variant pin reuses `allium-leafminer` on leek BECAUSE leek's prose names
    Phytomyza gymnostoma. A rewrite that dropped the binomial would silently invalidate that
    adjudication."""
    for (slug, name), taxon in sorted(TAXA.items()):
        p = find_problem(data, slug, name)
        blob = " ".join(v for v in p.values() if isinstance(v, str))
        if taxon not in blob:
            raise SystemExit("REFUSED: %s/%s no longer names %s" % (slug, name, taxon))
    return len(TAXA)


def check_sources_retired(data):
    """RHS must be gone from both problems, in `sources` AND `anchoring_urls`."""
    stale = []
    for slug, name in TARGETS:
        p = find_problem(data, slug, name)
        if RETIRED_SOURCE in (p.get("sources") or []) or RETIRED_SOURCE in (p.get("anchoring_urls") or {}):
            stale.append("%s/%s" % (slug, name))
    if stale:
        raise SystemExit("REFUSED: still cites %r: %r" % (RETIRED_SOURCE, stale))


def check_sibling_window_agreement(data):
    """Leek must now say what chives and shallot ALREADY say about the fall flight, read from their
    LIVE text. The pre-state fails this (leek says November); a sibling that stops carrying the
    phrase makes the check refuse rather than pass, so it cannot go vacuous."""
    for slug, name in SIBLINGS:
        p = find_problem(data, slug, name)
        blob = " ".join(v for v in p.values() if isinstance(v, str))
        if SIBLING_PHRASE not in blob:
            raise SystemExit("REFUSED: sibling %s/%s no longer says %r; the agreement check has "
                             "nothing to agree with" % (slug, name, SIBLING_PHRASE))
    leek = find_problem(data, CROP, "Allium leaf miner")
    hits = [k for k, v in leek.items() if isinstance(v, str) and SIBLING_PHRASE in v]
    if not hits:
        raise SystemExit("REFUSED: leek/Allium leaf miner does not carry the siblings' %r window"
                         % SIBLING_PHRASE)
    return len(hits)


def apply_to(data):
    check_pins(data)
    for (slug, name, field), (_b, after) in PROSE.items():
        find_problem(data, slug, name)[field] = after
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
    want_owners = {(s, n) for s, n in TARGETS}

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
    n_prose = sum(1 for k in changed if k[-1] in {f for _s, _n, f in PROSE})
    if n_prose != EXPECTED_PROSE:
        raise SystemExit("REFUSED: %d prose leaves changed, expected %d" % (n_prose, EXPECTED_PROSE))
    for (slug, name, field), (_b, after) in PROSE.items():
        if find_problem(data, slug, name).get(field) != after:
            raise SystemExit("REFUSED: %s/%s/%s did not receive its replacement"
                             % (slug, name, field))
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
    # Severity is NOT in scope and must not move.
    for slug, name in TARGETS:
        k = [k for k in changed if owner(k) == (slug, name) and k[-1] == "severity"]
        if k:
            raise SystemExit("REFUSED: %s/%s severity changed; not in scope" % (slug, name))
    touched = {owner(k) for k in changed}
    if touched - want_owners:
        raise SystemExit("REFUSED: leaves changed outside the declared targets: %r"
                         % sorted(touched - want_owners))
    return len(changed)


def check_catalog_untouched(before_cm, before_sc, data):
    if serialize(data["control_methods"]) != before_cm:
        raise SystemExit("REFUSED: control_methods changed; this promote mints nothing")
    if serialize(data["source_catalog"]) != before_sc:
        raise SystemExit("REFUSED: source_catalog changed; every id cited here already exists")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("canonical", nargs="?", default=CANONICAL)
    # `--canonical` is the form promote_fixture's CHAIN replay uses; both spellings are accepted.
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
    required = check_required_claims(data)
    taxa = check_taxa_survive(data)
    check_sources_retired(data)
    agree = check_sibling_window_agreement(data)

    blob = serialize(data)
    print("leaves changed      : %d (%d prose, %d source sets)" % (n, EXPECTED_PROSE,
                                                                     EXPECTED_SOURCE_SETS))
    print("retired claims gone : %d/%d" % (retired, len(RETIRED)))
    print("required claims in  : %d registers" % required)
    print("taxa survive        : %d/%d" % (taxa, len(TAXA)))
    print("sibling window      : leek agrees with chives + shallot in %d fields" % agree)
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
