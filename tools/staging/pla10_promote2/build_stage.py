#!/usr/bin/env python3
"""build_stage -- PLA-10 promote 2 session 2 helper (2026-10-02): writes crops/<slug>.json and EVIDENCE.tsv for
promote_pla10_promote2 from the literals below. The promote imports nothing from here; this file exists so the
stage is reproducible and every decision row, entry and quote is reviewable in one place.

Every quote is a substring of norm_text() of the HASHED bytes in tools/.evidence_cache (PDFs through the pinned
pypdf); --check on the promote re-reads them. Plan: docs/kickoffs/58-pla10-promote2-plan.md (rulings TAKEN).

Usage: python3 tools/staging/pla10_promote2/build_stage.py   (then promote_pla10_promote2.py --check)
"""
import csv, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, TOOLS)
import pla10_promote_common as C  # noqa: E402
import promote_pla10_promote2 as P  # noqa: E402

V = "2026-10-02"
D = "2026-10-02"  # correction date
SEE = "-- see PLA-10 promote 1, d021116.]"

# ---------------------------------------------------------------- pages (url as the crop cites it, hashed sha)
PAGE = {
    "ncsu": ("ncsu_ext_handbook_tree_fruit", "https://content.ces.ncsu.edu/extension-gardener-handbook/15-tree-fruit-and-nuts",
             "0e16d13e3df8fe822acab5ae904bdcc1de5346cf7ba7d96db5bb15e3dc164408"),
    "psu": ("psu_ext", "https://extension.psu.edu/heat-stress-and-tomatoes",
            "292915ad7ceb"),
    "isu_tom": ("iastate_ext", "https://yardandgarden.extension.iastate.edu/how-to/growing-tomatoes-home-garden",
                "9e86cd2ecc9b"),
    "unl": ("unl_ext", "https://extensionpublications.unl.edu/assets/html/g1650/build/g1650.htm",
            "b222f9ef109b34ef2a985afbd49e6b760fccdb5e770bf60e6ec7e4045e18ede9"),
    "clem": ("clemson_hgic", "https://hgic.clemson.edu/factsheet/cucumber/", "9d1eaeb1131d"),
    "umn_sq": ("umn_ext", "https://extension.umn.edu/vegetables/pumpkins-and-winter-squash", "fbdd655463e4"),
    "umn_tr": ("umn_ext_trellises_cages",
               "https://extension.umn.edu/garden-and-home/yard-and-garden/gardening-in-minnesota/trellises-and-cages",
               "8ee29202ffee"),
    "usu_cant": ("usu_ext", "https://extension.usu.edu/yardandgarden/research/cantaloupe-in-the-garden", "3699b2981c95"),
    "vce": ("vce_426_331", "https://www.pubs.ext.vt.edu/426/426-331/426-331.html", "52fda56c97ec"),
    "ucipm": ("uc_ipm", "https://ipm.ucanr.edu/home-and-landscape/cultural-tips-for-growing-strawberry",
              "9fb5c11e54b200f115322117253c7228d1a62919ba8bf0a4afc23813e76f2db9"),
    "mg_pdf": ("ucanr_mg_monterey_santacruz", "https://ucanr.edu/sites/default/files/2018-03/281247.pdf",
               "e7677756f59493cc052063e86a68cb0a7bf662a7a7b93e3fda899c5affe20470"),
}

Q = {
    "psu_stake": "recommended spacings for tomatoes are 18 to 24 inches between plants in a row and a minimum of 5-6 feet between rows for staked culture",
    "isu_stake": "indeterminate cultivars that are staked can be planted 1.5-2 feet apart within rows.",
    "isu_cage": "if grown in wire cages, space plants 2-3 feet apart.",
    "unl_cage": "caged tomatoes are best spaced 24 to 36 inches apart in rows 4 feet apart.",
    "clem_trellis": "if cucumbers are trellised, plant four to five seeds per foot in rows spaced 3 feet apart. when plants are 4 to 5 inches high, thin so they are 9 to 12 inches apart.",
    "umn_sq": "plant pumpkin and winter squash seeds three-fourths of an inch deep, 24 to 36 inches apart.",
    "vce_musk": "Muskmelon 24-36 in 60-90 in",
    "bed": "space plants about 12 inches apart in each row with rows about 12 inches apart in two-row beds",
}


def full_sha(prefix):
    if len(prefix) == 64:
        return prefix
    import glob
    hits = [os.path.basename(p).split(".")[0] for p in glob.glob(os.path.join(TOOLS, ".evidence_cache", prefix + "*"))]
    assert len(set(hits)) == 1, (prefix, hits)
    return hits[0]


def anchor(*keys):
    return {PAGE[k][0]: {"url": PAGE[k][1], "verified": V} for k in keys}


def entry(eid, sup, in_row, rows, keys, **extra):
    arr = eid.split("-")[0]
    e = {"id": eid, "arrangement": arr, "support": sup, "default": False, "in_row_inches": in_row}
    e.update(extra)
    e["row_spacing_inches"] = rows
    e["row_spacing_reason"] = None if rows is not None else "not_authored"
    e["sources"] = [PAGE[k][0] for k in keys]
    e["anchoring_urls"] = anchor(*keys)
    return e


EV = []


def ev(crop, eid, field, value, key, quote):
    sid, url, sha = PAGE[key]
    EV.append({"crop": crop, "entry_id": eid, "field": field, "value": C.compact(value), "source_id": sid,
               "url": url, "sha256": full_sha(sha), "quote": quote})


STAGE = {}


def stage(slug, decision, **kw):
    s = STAGE.setdefault(slug, {"slug": slug, "decision": decision})
    if s["decision"] != decision:
        s["decision"] = s["decision"] + " || " + decision
    s.update(kw)


def agrees(slug, note):
    """Every scanner hit on the BASE crop, adjudicated 'agrees' with the same reviewed note (each hit read in
    session 2; the note says what the string states)."""
    base = {c["slug"]: c for c in P.load_canonical()["crops"]}[slug]
    return [{"path": p, "verdict": "agrees", "note": note[p]} for p in C.spacing_strings(base)]


# ================================================================ 1.1 apple's rootstock overrides (R1, owed item 1)
OWED = (("M9", [48, 96], "M.9** 4 – 8 3 – 5 6 – 11"), ("M26", None, None),
        ("MM106", [144, 192], "MM.106 12 – 16 8 – 11 17 – 22"), ("MM111", [168, 216], "MM.111 14 – 18 9 – 12 20 – 25"),
        ("seedling", [216, 300], "Seedling* 18 – 25 12 – 16 25 – 35"))
rows = []
for name, val, quote in OWED:
    r = {"name": name, "spacing_inches": val}
    if val is not None:
        r["add_source"] = {"id": PAGE["ncsu"][0], "url": PAGE["ncsu"][1], "verified": V}
        ev("apple", f"rootstock_options[name={name}]", "spacing_inches", val, "ncsu", quote)
    rows.append(r)
stage("apple",
      "R1 (ruled 2026-09-30) + owed item 1: per-rootstock between-tree spacing from NC State Extension Gardener "
      "Handbook ch. 15, Table 15-4 (nonspur, feet), already cited by apple as ncsu_ext_handbook_tree_fruit, hashed "
      "0e16d13e. Each override is the table row's Nonspur Cultivars column (the first of three scion-habit columns under 'Distance Between Trees (feet)'; the spur and very-vigorous columns are not used) converted to inches, quoted as the full row "
      "string as promote 1 quoted M.26: M9 4-8 ft [48,96], MM106 12-16 ft [144,192], MM111 14-18 ft [168,216], "
      "seedling 18-25 ft [216,300]. M26 is null: it is the recommended row and the crop basis [96,144], cited on "
      "planting_layout row-none since promote 1. NCSU is appended to each non-null row's sources beside umd_ext "
      "(which states no spacing), with its document url, never the host.",
      rootstock_spacing=rows)

# ================================================================ 1.2 the 24 finding corrections (C1-C4)
CORR = {
    "slicing-cucumber": ("slicing-cucumber_pilot_finding_004_modeled_judgment_values",
                         "spacing_inches is 24 in since PLA-10 promote 1 (12-24 in was a span across trellised and ground spacing); rows, 48 in, are now in row_spacing_inches"),
    "habanero": ("habanero_pilot_finding_006",
                 "spacing_inches is 12-24 in since PLA-10 promote 1 (18-24 in was the earlier genus-level figure); rows, 30-36 in, are now in row_spacing_inches"),
    "pickling-cucumber": ("pickling-cucumber_pilot_finding_005",
                          "spacing_inches is 6-12 in since PLA-10 promote 1 (8-18 in was a modeled span across sources and bush types); rows, 48 in, are now in row_spacing_inches"),
    "butternut-squash": ("butternut_pilot_spacing_capped_72in",
                         "spacing_inches is 24-36 in since PLA-10 promote 1 (24-72 in was a blend of the in-row low and the between-row high); rows, 60-72 in, are now in row_spacing_inches, not carried only in prose"),
    "acorn-squash": ("acorn_pilot_spacing_prose",
                     "spacing_inches is 24-36 in since PLA-10 promote 1 (24-48 in spanned in-row spacing to a 4 ft row, a blend); rows, 60-72 in, are now in row_spacing_inches, not carried only in prose"),
    "spaghetti-squash": ("spaghetti_pilot_spacing_prose",
                         "spacing_inches is 24-36 in since PLA-10 promote 1, on UMN's winter-squash page; 24-48 in was not a span to a row figure, it was VCE 426-331 Table 5's winter-squash in-row 2-4 ft; rows, 60-72 in, are now in row_spacing_inches, not carried only in prose"),
    "broad-beans-fava": ("broad_beans_fava_pilot_finding_001",
                         "spacing_inches is 8-10 in, the thin-to figure, since PLA-10 promote 1 (4-8 in was a modeled span); no row figure is authored, row_spacing_reason not_authored"),
    "arugula": ("arugula_pilot_spacing_babyleaf",
                "spacing_inches is 3-6 in since PLA-10 promote 1 (1-3 in was the broadcast baby-leaf figure); rows, 18-36 in, are now in row_spacing_inches"),
    "sweet-potato": ("sweet_potato_pilot_finding_004",
                     "spacing_inches is 12-14 in since PLA-10 promote 1 (12-18 in spanned several sources' in-row figures); rows, 36 in, are now in row_spacing_inches"),
    "cilantro-coriander": ("cilantro_pilot_dtm_spacing_germ_modeled",
                           "spacing_inches is 2 in since PLA-10 promote 1 (2-4 in was the baby-leaf and cut-leaf span); rows, 15 in, are now in row_spacing_inches"),
    "chives": ("chives_pilot_dtm_spacing_germ_modeled",
               "spacing_inches is 6-12 in since PLA-10 promote 1 (8-12 in was a modeled value inside the sourced span); no row figure is authored, row_spacing_reason not_authored"),
    "mint": ("mint_pilot_finding_005",
             "spacing_inches is 12 in since PLA-10 promote 1 (12-24 in spanned the sourced range); no row figure is authored, row_spacing_reason not_authored"),
    "dill": ("dill_pilot_dtm_spacing_germ_modeled",
             "spacing_inches is 9 in since PLA-10 promote 1; the summary's 8-12 in and the basis's 8 to 12 inch spacing were a span across USU and harvest-to-table, and both are now 9 in; rows, 12 in, are now in row_spacing_inches"),
    "rosemary": ("rosemary_pilot_finding_004",
                 "spacing_inches is 24 in since PLA-10 promote 1 (24-36 in was 2 ft plus a modeled allowance for large upright plants); no row figure is authored, row_spacing_reason not_authored"),
    "watermelon": ("watermelon_pilot_spacing_capped_72in",
                   "spacing_inches is 60-72 in, the between-plants figure from the row entry, since PLA-10 promote 1 (36-72 in, which the basis gives as 3-6 ft in-row plant-to-hill spacing, was a blend capped at 72 in); the hill default, 96 in hills, and its 96 in rows are now in planting_layout and row_spacing_inches, not carried only in prose"),
    "cantaloupe": ("cantaloupe_pilot_spacing_in_row",
                   "the 24-36 in figure stands, but the between-row spacing is no longer carried only in prose: row_spacing_inches is 60-90 in since PLA-10 promote 1, and the hills are a non-default planting_layout entry"),
    "pumpkin": ("pumpkin_pilot_spacing_capped_72in",
                "spacing_inches is 48 in, the between-plants figure from the row entry, since PLA-10 promote 1 (36-72 in, which the basis gives as 3-6 ft in-row plant-to-hill spacing, was a blend capped at 72 in); the hill default, 96 in hills, and its 96 in rows are now in planting_layout and row_spacing_inches, not carried only in prose"),
    "mandarin-clementine": ("mandarin-clementine_pilot_finding_004",
                            "spacing_inches is 180 in, the UF/IFAS HS132 minimum, since PLA-10 promote 1 (120-216 in was modeled from small-tree size, not a spacing table); no row figure is authored, row_spacing_reason not_authored"),
    "honeydew-melon": ("honeydew_pilot_spacing_capped_48in",
                       "spacing_inches is 18-24 in since PLA-10 promote 1 (36-48 in was a gate-capped figure that no cited page states between plants); rows, 72-96 in, are now in row_spacing_inches and the 48 in hills are a planting_layout entry, not carried only in prose"),
    "shallot": ("shallot_spacing_upper_8in_modeled",
                "spacing_inches is 3-6 in since PLA-10 promote 1 (6-8 in carried a modeled 8 in upper end); rows, 12-18 in, are now in row_spacing_inches"),
    "cosmos": ("cosmos_pilot_finding_003",
               "spacing_inches is 12-24 in since PLA-10 promote 1 (12-18 in was modeled toward the low end of NCSU's width); no row figure is authored, row_spacing_reason not_authored"),
    "sweet-alyssum": ("sweet-alyssum_pilot_finding_008",
                      "spacing_inches is 8-10 in since PLA-10 promote 1 (4-8 in was a modeled carpet planting); no row figure is authored, row_spacing_reason not_authored"),
    "bee-balm": ("bee-balm_pilot_numerics_modeled",
                 "spacing_inches is 24-30 in since PLA-10 promote 1 (18-24 in was modeled inside the sourced span); no row figure is authored, row_spacing_reason not_authored"),
    "sweet-pea": ("sweet-pea_pilot_finding_004",
                  "spacing_inches is 5-6 in, the thin-to figure, since PLA-10 promote 1 (3-6 in was a representative value); no row figure is authored, row_spacing_reason not_authored"),
}
for slug, (fid, what) in CORR.items():
    stage(slug, "C1-C4 (ruled 2026-10-02): the open finding still states a spacing figure promote 1 moved "
                "(finding_corrections.tsv); one dated correction appended to its summary, the original byte-for-byte."
                + (" C3: mechanism-only, the figure is true." if slug == "cantaloupe" else "")
                + (" C2: names the basis figure too; basis untouched." if slug == "dill" else ""),
          finding_corrections=[{"id": fid, "append": f" [CORRECTION {D}: {what} {SEE}"}])

# ================================================================ 2. support entries
TOMATO_AGREES = {
    "failure_diagnostics[2].next_season_tip_beginner": "a mulch depth and watering cadence, not a spacing; states no plant or row distance",
    "failure_diagnostics[2].next_season_tip_seasoned": "watering depth and a mulch depth, not a spacing; states no plant or row distance",
    "companions.good_seasoned[2].why_seasoned": "states the cage footprint as 24-36 inch spacing, which is the new row-cage default's in-row [24,36]",
    "companions.note_seasoned": "states 24-36 inch spacing with 6-foot cages, which is the new row-cage default's in-row [24,36]",
}
CAGE_DECISION = ("S1 TAKEN on its S3 condition: UNL G1650's cage row figure IS citable. Fetched 2026-10-02 into "
                 "tools/.evidence_cache (b222f9ef, browser and plain user agents byte-identical; the cited url now "
                 "redirects to extensionpubs.unl.edu, recorded as a second manifest row on the same bytes): "
                 "'caged tomatoes are best spaced 24 to 36 inches apart in rows 4 feet apart.' So row-cage is the "
                 "DEFAULT. row-cage: in-row [24,36] (ISU 'if grown in wire cages, space plants 2-3 feet apart.'; "
                 "UNL, the same sentence as its rows), rows [48,48] from UNL only (S3: ISU's 'rows should be "
                 "spaced 4-5 feet apart' follows its sprawl sentence and is NOT applied to cages). ")
STAKE_PSU = ("row-stake: in-row [18,24] and rows [60,72] from PSU heat-stress 'a minimum of 5-6 feet between rows "
             "for staked culture' (a range minimum, authored as the range per the promote-1 cherry/grape/roma "
             "precedent; S6, PSU over UNL's 3 ft staked rows); ISU's 'indeterminate cultivars that are staked can be planted 1.5-2 feet "
             "apart within rows.' corroborates the in-row. ")
for slug, row_none_note, rows_before in (
        ("cherry-tomato", "row-none [24,36]/[60,72] is PSU's unstaked-indeterminate figure (S2) and stays, id pinned.", [60, 72]),
        ("grape-tomato", "row-none [24,36]/[60,72] is PSU's unstaked-indeterminate figure and stays, id pinned.", [60, 72]),
        ("heirloom-tomato", "row-none [24,36]/[48,60] (Missouri G6461, which names no support: flagged in plan 58 "
                            "§2, not reopened) stays, id pinned.", [48, 60])):
    stage(slug, CAGE_DECISION + STAKE_PSU + row_none_note +
          f" Mirrors: spacing_inches [24,36] unchanged; row_spacing_inches {C.compact(rows_before)} -> [48,48]. "
          "Every scanner restatement adjudicated. No height override (plan 58 §2.4).",
          planting_layout_add=[entry("row-stake", "stake", [18, 24], [60, 72], ("psu", "isu_tom")),
                               entry("row-cage", "cage", [24, 36], [48, 48], ("isu_tom", "unl"))],
          default="row-cage", restatements=agrees(slug, TOMATO_AGREES))
    ev(slug, "row-stake", "in_row_inches", [18, 24], "psu", Q["psu_stake"])
    ev(slug, "row-stake", "in_row_inches", [18, 24], "isu_tom", Q["isu_stake"])
    ev(slug, "row-stake", "row_spacing_inches", [60, 72], "psu", Q["psu_stake"])
    ev(slug, "row-cage", "in_row_inches", [24, 36], "isu_tom", Q["isu_cage"])
    ev(slug, "row-cage", "in_row_inches", [24, 36], "unl", Q["unl_cage"])
    ev(slug, "row-cage", "row_spacing_inches", [48, 48], "unl", Q["unl_cage"])

stage("beefsteak-tomato", CAGE_DECISION +
      "row-stake: in-row [18,24] from ISU 'indeterminate cultivars that are staked can be planted 1.5-2 feet apart "
      "within rows.'; rows [60,72] from PSU heat-stress (psu_ext, hashed 292915ad) 'recommended spacings for "
      "tomatoes are 18 to 24 inches between plants in a row and a minimum of 5-6 feet between rows for staked "
      "culture' (S6), which also states the in-row. Scope: tomatoes, staked culture; page not previously cited by "
      "this crop (beefsteak cites other PSU pages, not heat-stress); the entry's sources list is the citation "
      "(Trevor, 2026-10-02: leaving it null would make beefsteak the only one of the four row-stake entries with "
      "no row figure for the same page-stated reason). The entry is non-default, so no mirror moves on it. "
      "ISU's 4-5 ft sentence follows its sprawl sentence and is not used. row-none [36,48]/[48,60] (ISU sprawl) stays, id pinned. "
      "Mirrors: spacing_inches [36,48] -> [24,36] (the hero moves, X4); row_spacing_inches [48,60] -> [48,48]. "
      "The two scanner restatements already said '24-36 inch spacing' (one 'cage footprint', one 'large plant "
      "footprint ... 6-foot cages'), which contradicted the old "
      "[36,48] and now agree. No height override.",
      planting_layout_add=[entry("row-stake", "stake", [18, 24], [60, 72], ("psu", "isu_tom")),
                           entry("row-cage", "cage", [24, 36], [48, 48], ("isu_tom", "unl"))],
      default="row-cage", restatements=agrees("beefsteak-tomato", TOMATO_AGREES))
ev("beefsteak-tomato", "row-stake", "in_row_inches", [18, 24], "psu", Q["psu_stake"])
ev("beefsteak-tomato", "row-stake", "in_row_inches", [18, 24], "isu_tom", Q["isu_stake"])
ev("beefsteak-tomato", "row-stake", "row_spacing_inches", [60, 72], "psu", Q["psu_stake"])
ev("beefsteak-tomato", "row-cage", "in_row_inches", [24, 36], "isu_tom", Q["isu_cage"])
ev("beefsteak-tomato", "row-cage", "in_row_inches", [24, 36], "unl", Q["unl_cage"])
ev("beefsteak-tomato", "row-cage", "row_spacing_inches", [48, 48], "unl", Q["unl_cage"])

stage("roma-tomato",
      "row-cage only, NON-default (S1 covers the four indeterminate tomatoes; roma is determinate and row-none "
      "stays its default). S7: no stake entry (the hashed staked figures are scoped to indeterminate cultivars; "
      "roma's own text says 'a sturdy cage instead of a tall stake'). row-cage in-row [24,36] (ISU's cage sentence, "
      "which carries no habit word; UNL's, which carries none either), rows [48,48] (UNL, S3). The PLA-532 UMN "
      "trellises page names roma for cages but gives no figure. Recorded, not reopened: roma's row-none ISU "
      "[18,24]/[48,48] vs PSU's determinate-without-stakes 24 in / 4-5 ft. No mirror moves.",
      planting_layout_add=[entry("row-cage", "cage", [24, 36], [48, 48], ("isu_tom", "unl"))])
ev("roma-tomato", "row-cage", "in_row_inches", [24, 36], "isu_tom", Q["isu_cage"])
ev("roma-tomato", "row-cage", "in_row_inches", [24, 36], "unl", Q["unl_cage"])
ev("roma-tomato", "row-cage", "row_spacing_inches", [48, 48], "unl", Q["unl_cage"])

CUKE = ("row-trellis from Clemson HGIC cucumber (clemson_hgic, cited, hashed 9d1eaeb1): 'if cucumbers are "
        "trellised, plant four to five seeds per foot in rows spaced 3 feet apart. when plants are 4 to 5 inches "
        "high, thin so they are 9 to 12 inches apart.' The thin-to sentence closes the paragraph directly after "
        "the trellised sentence (a seeding rate that needs a thin-to figure); the non-trellised case already states "
        "its own final 8-10 in spacing, and the later non-trellised repeat is an image caption. So it is the trellised case: in-row [9,12], rows [36,36]. ")
for slug in ("slicing-cucumber", "pickling-cucumber", "cucumber"):
    stage(slug, CUKE + "NON-default: every cited page presents the trellis as optional, so row-none stays the "
                       "default, id pinned. No mirror moves. No height override (Clemson's 6 ft and UMN's 3-4 ft "
                       "are trellis heights, §2.4).",
          planting_layout_add=[entry("row-trellis", "trellis", [9, 12], [36, 36], ("clem",))])
    ev(slug, "row-trellis", "in_row_inches", [9, 12], "clem", Q["clem_trellis"])
    ev(slug, "row-trellis", "row_spacing_inches", [36, 36], "clem", Q["clem_trellis"])

stage("english-cucumber", CUKE + "DEFAULT (S5): the crop's own text says to 'train the plants up a string or "
      "trellis to keep the long fruit straight', and Clemson names 'hybrid, burpless or european-type cucumbers'. "
      "row-none [12,18]/[48,72] (VCE 426-331) stays, id pinned, non-default. Mirrors: spacing_inches [12,18] -> "
      "[9,12] (the hero moves, X4); row_spacing_inches [48,72] -> [36,36]. The three scanner restatements are fruit "
      "lengths and agree. The greenhouse cordon figures (ACES, UF CV268) are commercial and doc-cache only: not "
      "used.",
      planting_layout_add=[entry("row-trellis", "trellis", [9, 12], [36, 36], ("clem",))], default="row-trellis",
      restatements=agrees("english-cucumber", {
          "harvest_ready_seasoned": "fruit lengths at harvest (12 to 14 in, 11 in, 5 to 8 in), not a spacing",
          "varieties.recommended[1].recommended_note": "a fruit length (7 to 8 inch fruit), not a spacing",
          "varieties.recommended[3].recommended_note": "a fruit length (5 to 7 inch fruit), not a spacing"}))
ev("english-cucumber", "row-trellis", "in_row_inches", [9, 12], "clem", Q["clem_trellis"])
ev("english-cucumber", "row-trellis", "row_spacing_inches", [36, 36], "clem", Q["clem_trellis"])

stage("acorn-squash",
      "row-trellis, NON-default, acorn by name (M2 note): its own UMN page, 'you can train small-fruited squash like "
      "delicata or acorn to a trellis to save space.' In-row [24,36] is the ground figure on the same page ('24 to "
      "36 inches apart'), by UMN's trellis rule 'plant the vines at the foot of the trellis at the same spacing "
      "between the seeds or transplants as if they were going to grow on the ground' (umn_ext_trellises_cages, "
      "PLA-532). Rows null, not_authored: UMN gives no trellised row figure. Flag for review: the page ties the 24 "
      "end to bush types, so the trellised (vining) form reads toward 36. No mirror moves; no height override.",
      planting_layout_add=[entry("row-trellis", "trellis", [24, 36], None, ("umn_sq", "umn_tr"))])
ev("acorn-squash", "row-trellis", "in_row_inches", [24, 36], "umn_sq", Q["umn_sq"])

stage("cantaloupe",
      "row-trellis, NON-default, by ruling (M1): USU 'cantaloupe plants can be trained to a fence or trellis or "
      "grown in a large pot. after the fruits begin to enlarge they will need some support' is the citation. "
      "In-row [24,36] is the crop's ground figure (VCE 426-331 'Muskmelon 24-36 in 60-90 in', the row-none "
      "entry's own quote) by UMN's same-spacing rule (umn_ext_trellises_cages). Rows null, not_authored. The "
      "cultivar condition, stated here because cultivar is not an entry axis: UMN says 'varieties with fruit "
      "weighing up to three pounds ... work best', and ISU's listed cultivars are mostly 4-9 lb (only 'sarah's "
      "choice' 3 lb, 'sugar cube' 2 lb), so the trellis suits small-fruited cultivars, and the fruit needs slings (UMN: melons 'slip' from the vine when ripe, 'make hammocks or slings to support the developing fruit'; USU: 'after the fruits begin to enlarge they will need some support'). Flag: UMD "
      "melons (doc-cache only) says a trellis 'allows closer spacing', against UMN; no figure. No mirror moves.",
      planting_layout_add=[entry("row-trellis", "trellis", [24, 36], None, ("vce", "usu_cant", "umn_tr"))])
ev("cantaloupe", "row-trellis", "in_row_inches", [24, 36], "vce", Q["vce_musk"])

stage("strawberry",
      "row-none-bed, NON-default (B1, B2). TWO hashed pages, both cited by strawberry, both carrying the sentence: "
      "(1) UC IPM 'Cultural Tips for Growing Strawberry', HTML (uc_ipm, 9fb5c11e, fetched 2026-10-02, both user "
      "agents byte-identical); (2) 281247.pdf, the UC Master Gardeners of Monterey & Santa Cruz class handout "
      "(ucanr_mg_monterey_santacruz, e7677756, fetched 2026-10-02, read through pinned pypdf). There is NO UC IPM "
      "PDF: plan 58's B2 note calls 281247.pdf 'the UC IPM PDF', but it is the MG handout. Quote: 'space plants about 12 inches apart in each row with rows about "
      "12 inches apart in two-row beds'; beds '18 inches wide if you are planting two rows'. rows_per_bed 2, in-row "
      "[12,12], row_spacing_inches [12,12] = the IN-BED row gap (spec §1.1 as appended 2026-10-02). The same sentence continues 'and stagger the plants in the two rows to give them maximum growing room': the "
      "planting is offset, and staggering is not an entry axis. UC IPM's single-row figure ('in single-row beds, space "
      "plants about 10 inches apart') is not authored. ucanr_mg_monterey_santacruz reproduces UC IPM's text: a second "
      "copy, not independent corroboration. No home page "
      "gives a between-bed figure. Scope: statewide California home garden, stated here because the entry has no "
      "region axis. row-none [18,24]/[36,48] (UMN matted row) stays the default, id pinned. No mirror moves.",
      planting_layout_add=[entry("row-none-bed", "none", [12, 12], [12, 12], ("ucipm", "mg_pdf"), rows_per_bed=2)])
for k in ("ucipm", "mg_pdf"):
    ev("strawberry", "row-none-bed", "in_row_inches", [12, 12], k, Q["bed"])
    ev("strawberry", "row-none-bed", "row_spacing_inches", [12, 12], k, Q["bed"])


def main():
    out = os.path.join(HERE, "crops")
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        if f.endswith(".json"):
            os.remove(os.path.join(out, f))
    for slug, s in sorted(STAGE.items()):
        with open(os.path.join(out, slug + ".json"), "w", encoding="utf-8") as f:
            json.dump(s, f, ensure_ascii=False, indent=2)
            f.write("\n")
    with open(os.path.join(HERE, "EVIDENCE.tsv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=C.EVIDENCE_COLS, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(EV)
    print(f"staged {len(STAGE)} crops, {len(EV)} evidence rows")


if __name__ == "__main__":
    main()
