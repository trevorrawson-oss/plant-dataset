#!/usr/bin/env python3
"""build_stage -- writes the PLA-666 row-figures stage (ops.json, EVIDENCE.tsv, DECISIONS.tsv) from the canonical at
afbd4113. Every `old` is READ from the canonical, never typed, so a drifted base refuses at --check. The prose strings
are Trevor's (claude.ai, 2026-10-05), verbatim. Every quote is a norm_text substring of the hashed bytes it names
(the promote's guard E re-checks each one).

Rulings: PLA-666 Phase A rulings 1-7 and the strings ruling (Trevor via claude.ai, 2026-10-05); Linear document
"PLA-666 row figures: DECISIONS".
Usage: python3 tools/staging/pla666_row_figures/build_stage.py
"""
import copy, csv, hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "tools"))
from cited_promote_common import EVIDENCE_COLS, resolve  # noqa: E402

BASE_SHA = "afbd4113e94b8fc41776178c31e8e3743ec7eef1c11ed0f57e6cf6dfdd7dcd3e"
VERIFIED = "2026-10-04"   # the date the cited bytes were hashed (MANIFEST)
ENTRY = "planting_layout[id=row-none]"

UMN = ("umn_ext", "https://extension.umn.edu/fruit/growing-raspberries-home-garden",
       "2e413287db204c6b283af3e5e7bb257302e30301a36db468f5ffb883ffae181a")
UADA = ("uada_ext_fsa6107", "https://www.uaex.uada.edu/publications/PDF/FSA-6107.pdf",
        "c8bb32a415427da002f8df1d0e35d280f34b5bcac8186d31a13fca791a13fea5")
PSU = ("psu_ext", "https://extension.psu.edu/raspberry-production",
       "ae4edab591f1f39c5068abc3b53ae1868feecfb0198a7fb9fbc9b8970eb8d791")
UGA = ("uga_ext", "https://fieldreport.caes.uga.edu/publications/C766/",
       "74b91280ff415c4242d8a1f1c1a1335fce5855fdac795a26b3aee38ee1f5ecc9")
PBI = ("ksu_pawpaw_pbi004", "https://www.kysu.edu/brand-identity-approved-images/pawpaw/OrganicPawpawPBI-004.pdf",
       "c1eefcc3be48fff127514a35dd1ddcacecc4988406d3e6f20b742375d1c3734f")

Q = {  # norm_text form, machine-checked as substrings of the hashed bytes
    "umn_spring": "april, may- plant bare-root transplants as soon as the soil can be worked",
    "uada_spring": "planting should occur in the spring as soon as the soil can be properly prepared.",
    "umn_bareroot": "raspberry plants can be purchased as dormant bare-root plants or as potted plants.",
    "umn_inrow": "plant them 18 to 24 inches apart in moist soil.",
    "uada_rows": "spacing for red raspberries can be from 5 to 10 feet between rows, depending on how the row "
                 "middles will be managed, i.e., cultivation, mowing or mulching.",
    "uada_middles": "wider row spacing will be required for cultivated row middles than for row middles which are "
                    "mowed or mulched.",
    "umn_yellow": "yellow raspberries are red raspberries that don't make red pigment.",
    "umn_black": "set black and purple raspberries 4 feet apart because these types do not produce root suckers, "
                 "they will create what is commonly called a hill.",
    "umn_drained": "any well-drained soil is good for growing raspberries.",
    "umn_site": "grow raspberries in a part of the garden that has good air circulation, good drainage and full "
                "sunlight.",
    "umn_raised": "if planting on heavier soils, create raised rows or raised bed gardens before planting, to "
                  "increase water drainage.",
    "uga_trailing": "while only the trailing raspberry dormanred has proven itself for all of georgia.",
    "uga_section": "growing trailing blackberries and the dormanred raspberry trailing blackberries and the dormanred "
                   "raspberry are known as brambles, and their culture is similar.",
    "uga_inrow": "plant trailing brambles with 10 feet between plants.",
    "uga_rows": "if more than one row is to be planted, space the rows 12 feet apart.",
    "uada_dormanred_red": "this variety differs from other red raspberries in that it has weak vine-like growth and "
                          "requires trellising similar to trailing blackberries.",
    "uada_suckers": "red raspberries generally have erect- growing canes and propagate from sucker plants growing from "
                    "the roots of the parent plant.",
    "uada_cultivation": "if clean cultivation is used, the area between rows will need to be cultivated to a depth of 1 "
                        "to 2 inches every two weeks from early spring until the end of harvest.",
    "umn_virusfree": "summer or fall before planting order or buy plants from an established nursery that sells plants "
                     "that have been certified virus-free.",
    "umn_early_spring": "early spring is the best time to plant raspberries.",
    "umn_potted": "may, june- plant potted transplants after the threat of frost has passed",
    "umn_step2": "step 2: plant the raspberry plants plant them 18 to 24 inches apart in moist soil.",
    "umn_suckers": "red and yellow raspberry plants send up shoots or suckers in places you would least expect.",
    "umn_water": "water thoroughly after planting.",
    "umn_mulch": "apply woodchip or straw mulch to help keep moisture in and weeds out.",
    "umn_support": "support all types of raspberries require support to prevent the canes from wind damage, bending "
                   "over, cracking, and getting out of control.",
    "uada_black_no_trellis": "black raspberries do not require a trellis system.",
    "uada_dormanred_trellis": "'dormanred,' the recommended summer bearing variety, must be trellised due to its "
                              "trailing growth habit.",
    "psu_verticillium": "also, raspberry plantings should not follow verticillium -susceptible crops, such as peppers, "
                        "eggplant, tomatoes, potatoes, or strawberries.",
    "psu_rotation": "soil that has been used to grow these crops should be cropped for five to eight years with a non- "
                    "verticillium -susceptible crop.",
    "pbi_rows": "we p resently recommend that trees be planted at a spacing of 8 feet with in rows and 12 to 18 feet "
                "between rows.",
}

SEASONED = ("Plant dormant bare-root canes in spring, as soon as the soil can be worked. Space red and yellow "
            "raspberries about 18 to 24 inches apart. Rows of red and yellow raspberries can be 5 to 10 feet apart, "
            "depending on how the row middles are managed: cultivated middles need wider rows than mowed or mulched "
            "ones. UGA Extension spaces Dormanred, a trailing red, like a trailing blackberry: plants 10 feet apart in "
            "rows 12 feet apart. Set black and purple raspberries 4 feet apart. Plant in well-drained soil. On heavier "
            "soils, make raised rows or raised beds before planting to improve drainage.")
BEGINNER = ("Plant bare-root raspberry plants in spring, as soon as the soil can be worked. Space red and yellow "
            "raspberries about 18 to 24 inches apart, in rows 5 to 10 feet apart. Leave more room between rows if you "
            "plan to cultivate there, meaning lightly loosen the soil, than if you'll mow or mulch. Georgia Extension "
            "spaces Dormanred, a trailing red raspberry, the way it spaces trailing blackberries: plants 10 feet "
            "apart, in rows 12 feet apart. Set black and purple raspberries 4 feet apart. Choose a spot where the soil drains well. If "
            "your soil is heavy, build raised rows or beds before planting so water drains away.")

# Ruling E strings (Trevor via claude.ai, 2026-10-05), verbatim
SM_SEASONED = ("Start from dormant bare-root plants or potted plants from an established nursery that sells certified "
               "virus-free stock. Plant bare-root plants in early spring, as soon as the soil can be worked, and potted "
               "plants after the threat of frost has passed. Space plants along the row. Red and yellow raspberries "
               "send up suckers from their roots; black and purple raspberries do not.")
SM_BEGINNER = ("Buy raspberries as dormant bare-root plants or as potted plants, from a nursery that sells certified "
               "virus-free plants. Plant bare-root plants in early spring, as soon as the soil can be worked. Wait to "
               "plant potted ones until the danger of frost has passed.")
GS_SEASONED = ("Space plants along the row, water thoroughly after planting, and apply woodchip or straw mulch to hold "
               "in moisture and keep weeds out. Use certified virus-free stock. Penn State advises against following "
               "verticillium-susceptible crops such as peppers, eggplant, tomatoes, potatoes, or strawberries, and "
               "recommends five to eight years of non-susceptible crops first. On support, sources differ: Minnesota "
               "Extension says all types need it, while Arkansas Extension says black raspberries need no trellis and "
               "that Dormanred must be trellised.")
GS_BEGINNER = ("Plant along your row, water well right after planting, and spread woodchip or straw mulch to keep "
               "moisture in and weeds out. Buy certified virus-free plants. Minnesota Extension recommends a trellis or "
               "other support for all raspberries, to protect the canes from wind damage, bending over, and cracking.")
GS_LOOK_SEASONED = ("Dormant bare-root plants or potted nursery plants going into a well-drained row. Bare-root plants "
                    "are planted in early spring, as soon as the soil can be worked; potted plants are planted after "
                    "the threat of frost has passed.")
GS0 = "growth_stages[id=planting]"

CATALOG_PBI = {
    "id": "ksu_pawpaw_pbi004",
    "name": "Kentucky State University PBI-004, Organic Production of Pawpaw (Kirk W. Pomper, Sheri B. Crabtree, "
            "Jeremy D. Lowe)",
    "title": "Organic Production of Pawpaw",
    "publisher": "Kentucky State University Cooperative Extension Program",
    "url": PBI[1],
    "source_class": "university_extension",
    "trust_tier": "high",
    "accessed": "2026-10",
    "tier": "T1",
    "citable_for": "KSU Pawpaw Research Program publication PBI-004 (July 2010): organic pawpaw orchard "
                   "establishment, including the recommended tree spacing of 8 feet within rows and 12 to 18 feet "
                   "between rows (orchard scope). A document-scoped child of ksu_pawpaw.",
}


def by_slug(data):
    return {c["slug"]: c for c in data["crops"]}


def value(crop, path):
    node = crop
    for s in resolve(crop, path):
        node = node[s]
    return node


def op(crop, slug, path, kind, new, cited_at, reason, old=None):
    return {"crop": slug, "path": path, "kind": kind, "old": value(crop, path) if old is None else old, "new": new,
            "cited_at": cited_at, "reason": reason}


def ev(slug, entry, field, val, src, quote_key):
    sid, url, sha = src
    return {"crop": slug, "entry_id": entry, "field": field, "value": val, "source_id": sid, "url": url,
            "sha256": sha, "quote": Q[quote_key]}


def main():
    raw = open(os.path.join(REPO, "crops_data_final.json"), "rb").read()
    if hashlib.sha256(raw).hexdigest() != BASE_SHA:
        sys.exit("canonical is not afbd4113")
    idx = by_slug(json.loads(raw))
    ras, paw = idx["raspberry"], idx["pawpaw"]

    ras_anchors = copy.deepcopy(value(ras, f"{ENTRY}.anchoring_urls"))
    ras_anchors[UADA[0]] = {"url": UADA[1], "verified": VERIFIED}
    paw_anchors = copy.deepcopy(value(paw, f"{ENTRY}.anchoring_urls"))
    paw_anchors[PBI[0]] = {"url": PBI[1], "verified": VERIFIED}

    ops = [
        op(ras, "raspberry", "planting_method_notes_seasoned", "prose", SEASONED, None,
           "Trevor's string (2026-10-05): rows 6-8 ft (on no page) -> UADA 5-10 ft; black/purple 4 ft (UMN); depth, "
           "handle, trellis, late winter, 'larger', 'slightly' cut (rulings 1-3)"),
        op(ras, "raspberry", "planting_method_notes_beginner", "prose", BEGINNER, None,
           "Trevor's string (2026-10-05): the registers agree (ruling 4)"),
        op(ras, "raspberry", f"{ENTRY}.row_spacing_inches", "value", [60, 120], ENTRY,
           "ruling 1 (PLA-666 measurement): UADA FSA-6107 home-garden red raspberry, 5 to 10 feet between rows"),
        op(ras, "raspberry", f"{ENTRY}.row_spacing_reason", "value", None, ENTRY,
           "null iff the entry carries a row figure (spec §1.6 item 5)"),
        op(ras, "raspberry", f"{ENTRY}.sources", "sources", value(ras, f"{ENTRY}.sources") + [UADA[0]], None,
           "the row figure's page joins the entry (two-page reading, ruled)"),
        op(ras, "raspberry", f"{ENTRY}.anchoring_urls", "anchors", ras_anchors, None,
           "UADA FSA-6107 anchors the row figure; umn_ext keeps the in-row"),
        op(ras, "raspberry", "row_spacing_inches", "value", [60, 120], ENTRY,
           "the crop-root mirror of the default entry's row figure (spec §1.6 item 7)"),
        op(ras, "raspberry", "row_spacing_reason", "value", None, ENTRY,
           "the crop-root reason is null iff row_spacing_inches is non-null (spec §1.6 item 7)"),
        op(paw, "pawpaw", f"{ENTRY}.row_spacing_inches", "value", [144, 216], ENTRY,
           "ruling 5: KSU PBI-004, 12 to 18 feet between rows (orchard scope, admitted: no home-garden figure)"),
        op(paw, "pawpaw", f"{ENTRY}.row_spacing_reason", "value", None, ENTRY,
           "null iff the entry carries a row figure (spec §1.6 item 5)"),
        op(paw, "pawpaw", f"{ENTRY}.sources", "sources", value(paw, f"{ENTRY}.sources") + [PBI[0]], None,
           "PBI-004 joins the entry under its own id; the planting guide (ksu_pawpaw) keeps the in-row"),
        op(paw, "pawpaw", f"{ENTRY}.anchoring_urls", "anchors", paw_anchors, None,
           "both KSU pages on the entry (Trevor, 2026-10-05)"),
        op(paw, "pawpaw", "row_spacing_inches", "value", [144, 216], ENTRY,
           "the crop-root mirror of the default entry's row figure (spec §1.6 item 7)"),
        op(paw, "pawpaw", "row_spacing_reason", "value", None, ENTRY,
           "the crop-root reason is null iff row_spacing_inches is non-null (spec §1.6 item 7)"),
        {"crop": "<catalog>", "path": PBI[0], "kind": "catalog", "old": "<absent>", "new": CATALOG_PBI,
         "cited_at": None, "reason": "a document-scoped child of ksu_pawpaw: anchoring_urls is keyed by source id, "
                                     "so the entry cannot carry two KSU pages under one id"},
    ]
    # ruling E (appended, so the earlier op indices stay put)
    gs0_anchors = copy.deepcopy(value(ras, f"{GS0}.anchoring_urls"))
    gs0_anchors[UADA[0]] = {"url": UADA[1], "verified": VERIFIED}
    ops += [
        op(ras, "raspberry", "start_method.notes_seasoned", "prose", SM_SEASONED, "start_method",
           "ruling E string: depth, handle, 'not from seed', 'common, economical', own-root/no rootstock, support "
           "timing and 'late winter' cut"),
        op(ras, "raspberry", "start_method.notes_beginner", "prose", SM_BEGINNER, "start_method",
           "ruling E string: depth, handle, 'rather than growing from seed', support timing and 'late winter' cut"),
        op(ras, "raspberry", "start_method.anchoring_urls", "anchors",
           {UMN[0]: {"url": UMN[1], "verified": VERIFIED}, UADA[0]: {"url": UADA[1], "verified": VERIFIED}}, None,
           "start_method gains a citation block (the broad-beans-fava precedent, Housekeeping 60 Phase C)", old="<absent>"),
        op(ras, "raspberry", "start_method.sources", "sources", [UMN[0], UADA[0]], None,
           "start_method gains a citation block (the broad-beans-fava precedent)", old="<absent>"),
        op(ras, "raspberry", f"{GS0}.user_action_seasoned", "prose", GS_SEASONED, GS0,
           "ruling E string: depth, handle, bramble history, support timing cut; PSU rotation and the support "
           "conflict stated with attribution"),
        op(ras, "raspberry", f"{GS0}.user_action_beginner", "prose", GS_BEGINNER, GS0,
           "ruling E string: depth, handle, support timing cut"),
        op(ras, "raspberry", f"{GS0}.what_to_look_for_seasoned", "prose", GS_LOOK_SEASONED, GS0,
           "ruling E string: 'late winter' and 'support in place' cut"),
        op(ras, "raspberry", f"{GS0}.anchoring_urls", "anchors", gs0_anchors, None,
           "UADA joins growth_stages[0] (the support sentence uses it)"),
        op(ras, "raspberry", f"{GS0}.sources", "sources", value(ras, f"{GS0}.sources") + [UADA[0]], None,
           "UADA joins growth_stages[0]"),
    ]

    # ruling 1 (2026-10-05): "Dormanred", the sources' spelling, in every display string. Left alone: the variety
    # name (a lookup key: plant-app slugifies it to dorman-red), rgv.plantings_provenance and open_findings (records).
    ORTHO_PATHS = ["varieties.note_seasoned", "varieties.note_beginner", "chill_hours_note_seasoned"]
    for reg in ("se_gulf", "fl_peninsula", "rgv", "utah_dixie"):
        for z, cell in sorted((ras["regions"][reg].get("resolved_by_zone") or {}).items(), key=lambda kv: int(kv[0])):
            for k in ("type_note_seasoned", "type_note_beginner"):
                if "Dorman Red" in (cell.get(k) or ""):
                    ORTHO_PATHS.append(f"regions.{reg}.resolved_by_zone.{z}.{k}")
        for k in ("region_notes_seasoned", "region_notes_beginner"):
            if "Dorman Red" in (ras["regions"][reg].get(k) or ""):
                ORTHO_PATHS.append(f"regions.{reg}.{k}")
    for path in ORTHO_PATHS:
        old = value(ras, path)
        assert "Dorman Red" in old, path
        ops.append(op(ras, "raspberry", path, "orthography", old.replace("Dorman Red", "Dormanred"), None,
                      "ruling 1: 'Dorman Red' -> 'Dormanred' (the sources' spelling), spelling only"))

    S, B = "planting_method_notes_seasoned", "planting_method_notes_beginner"
    rows = []
    for entry, reg in ((S, "seasoned"), (B, "beginner")):
        timing = ("Plant dormant bare-root canes in spring, as soon as the soil can be worked" if reg == "seasoned"
                  else "Plant bare-root raspberry plants in spring, as soon as the soil can be worked")
        rows += [
            ev("raspberry", entry, "timing", timing, UMN, "umn_spring"),
            ev("raspberry", entry, "timing", timing, UADA, "uada_spring"),
            ev("raspberry", entry, "bare-root", timing, UMN, "umn_bareroot"),
            ev("raspberry", entry, "in-row", "red and yellow about 18 to 24 inches apart", UMN, "umn_inrow"),
            ev("raspberry", entry, "yellow", "red and yellow", UMN, "umn_yellow"),
            ev("raspberry", entry, "rows", "rows 5 to 10 feet apart", UADA, "uada_rows"),
            ev("raspberry", entry, "row middles",
               "cultivated middles need wider rows than mowed or mulched ones" if reg == "seasoned" else
               "Leave more room between rows if you plan to cultivate there ... than if you'll mow or mulch", UADA,
               "uada_middles"),
            ev("raspberry", entry, "Dormanred: trailing red",
               "Dormanred, a trailing red" if reg == "seasoned" else "Dormanred, a trailing red raspberry", UGA,
               "uga_trailing"),
            ev("raspberry", entry, "Dormanred: trailing red",
               "Dormanred, a trailing red" if reg == "seasoned" else "Dormanred, a trailing red raspberry", UADA,
               "uada_dormanred_red"),
            ev("raspberry", entry, "Dormanred: spaced like a trailing blackberry",
               "like a trailing blackberry" if reg == "seasoned" else "the way it spaces trailing blackberries", UGA,
               "uga_section"),
            ev("raspberry", entry, "Dormanred: in-row", "plants 10 feet apart", UGA, "uga_inrow"),
            ev("raspberry", entry, "Dormanred: rows", "rows 12 feet apart", UGA, "uga_rows"),
            ev("raspberry", entry, "black and purple", "Set black and purple raspberries 4 feet apart", UMN,
               "umn_black"),
            ev("raspberry", entry, "drainage",
               "Plant in well-drained soil" if reg == "seasoned" else "Choose a spot where the soil drains well",
               UMN, "umn_drained" if reg == "seasoned" else "umn_site"),
            ev("raspberry", entry, "raised rows",
               "On heavier soils, make raised rows or raised beds before planting to improve drainage"
               if reg == "seasoned" else
               "If your soil is heavy, build raised rows or beds before planting so water drains away",
               UMN, "umn_raised"),
        ]
        if reg == "beginner":
            rows.append(ev("raspberry", entry, "cultivate gloss", "meaning lightly loosen the soil", UADA,
                           "uada_cultivation"))
    SMS, SMB = "start_method.notes_seasoned", "start_method.notes_beginner"
    GSS, GSB, GSL = f"{GS0}.user_action_seasoned", f"{GS0}.user_action_beginner", f"{GS0}.what_to_look_for_seasoned"
    R = "raspberry"
    for entry in (SMS, SMB):
        rows += [
            ev(R, entry, "bare-root or potted", "dormant bare-root plants or potted plants", UMN, "umn_bareroot"),
            ev(R, entry, "certified virus-free nursery", "a nursery that sells certified virus-free stock/plants", UMN,
               "umn_virusfree"),
            ev(R, entry, "bare-root timing", "bare-root plants in early spring, as soon as the soil can be worked", UMN,
               "umn_spring"),
            ev(R, entry, "bare-root timing", "early spring", UMN, "umn_early_spring"),
            ev(R, entry, "bare-root timing", "in spring, as soon as the soil can be worked", UADA, "uada_spring"),
            ev(R, entry, "potted timing", "potted plants after the threat (danger) of frost has passed", UMN,
               "umn_potted"),
        ]
    rows += [
        ev(R, SMS, "along the row", "Space plants along the row", UMN, "umn_step2"),
        ev(R, SMS, "suckering", "Red and yellow raspberries send up suckers from their roots", UMN, "umn_suckers"),
        ev(R, SMS, "suckering", "red raspberries ... suckers from their roots", UADA, "uada_suckers"),
        ev(R, SMS, "no root suckers: black and purple", "black and purple raspberries do not", UMN, "umn_black"),
    ]
    for entry in (GSS, GSB):
        rows += [
            ev(R, entry, "along the row", "Space plants / plant along the row", UMN, "umn_step2"),
            ev(R, entry, "water", "water thoroughly / well right after planting", UMN, "umn_water"),
            ev(R, entry, "mulch", "woodchip or straw mulch, moisture in, weeds out", UMN, "umn_mulch"),
            ev(R, entry, "certified virus-free", "certified virus-free stock/plants", UMN, "umn_virusfree"),
            ev(R, entry, "support: Minnesota", "Minnesota Extension: all types need support", UMN, "umn_support"),
        ]
    rows += [
        ev(R, GSS, "rotation: Penn State", "advises against following verticillium-susceptible crops such as peppers, "
           "eggplant, tomatoes, potatoes, or strawberries", PSU, "psu_verticillium"),
        ev(R, GSS, "rotation: Penn State", "five to eight years of non-susceptible crops first", PSU, "psu_rotation"),
        ev(R, GSS, "support: Arkansas", "black raspberries need no trellis", UADA, "uada_black_no_trellis"),
        ev(R, GSS, "support: Arkansas", "Dormanred must be trellised", UADA, "uada_dormanred_trellis"),
        ev(R, GSL, "bare-root or potted", "Dormant bare-root plants or potted nursery plants", UMN, "umn_bareroot"),
        ev(R, GSL, "well-drained", "a well-drained row", UMN, "umn_drained"),
        ev(R, GSL, "bare-root timing", "early spring, as soon as the soil can be worked", UMN, "umn_spring"),
        ev(R, GSL, "bare-root timing", "early spring", UMN, "umn_early_spring"),
        ev(R, GSL, "potted timing", "after the threat of frost has passed", UMN, "umn_potted"),
    ]
    for path in (f"{ENTRY}.row_spacing_inches", "row_spacing_inches"):
        rows += [ev("raspberry", path, "rows", "[60,120]", UADA, "uada_rows"),
                 ev("raspberry", path, "scope: yellow", "[60,120] covers red and yellow", UMN, "umn_yellow"),
                 ev("pawpaw", path, "rows", "[144,216]", PBI, "pbi_rows")]

    D = []

    def dec(slug, path, decision, reason):
        D.append({"crop": slug, "path": path, "decision": decision, "reason": reason})

    sib = ("planting_method_notes has no citation sibling on any crop (0 of the 4 crops carrying it); the sources "
           "live in these EVIDENCE rows, the watermelon soil_prep precedent (Housekeeping 60 Phase C, PLA-674)")
    dec("raspberry", S, "record-only", sib)
    dec("raspberry", B, "record-only", sib)
    dec("raspberry", S, "cut", "Rulings 1 and 3: the depth clause (UMN crown 1 or 2 in ABOVE the ground, UGA 1/2 in "
        "below, UADA 2-3 in deeper than nursery depth; routed to PLA-625), the handle-cane cut and the "
        "trellis-before-growth clause (on no hashed page), and 'late winter' are cut; 'larger'/'bigger' and "
        "'slightly' are on no page and cut (strings ruling).")
    dec("raspberry", S, "timing", "'In spring' rests on UMN's April-May checklist entry (a Minnesota calendar); the "
        "portable part is 'as soon as the soil can be worked'. UADA agrees: \"planting should occur in the spring as "
        "soon as the soil can be properly prepared.\"")
    dec("raspberry", S, "black and purple", "Ruling 2: UMN's \"4 feet apart\" covers black AND purple. UADA's "
        "black-only \"within-row plant spacing should be 2 to 3 feet for red raspberries and 4 to 5 feet for black "
        "raspberries.\" is recorded, not followed.")
    dec("raspberry", S, "in-row divergence", "The leaf keeps the field's 18 to 24 in (UMN \"plant them 18 to 24 "
        "inches apart\"). UMN also says \"space red or yellow raspberry plants every 2 to 3 feet\" and UADA \"2 to 3 "
        "feet for red raspberries\": recorded, not this promote's call.")
    dec("raspberry", S, "hill not used", "UMN's black/purple 'hill' (a cane clump) is deliberately not used: a third "
        "sense of 'hill' that would collide with PLA-673's glossary; recorded on PLA-673 for its sense-guard "
        "exclusion list.")
    dec("raspberry", f"{ENTRY}.row_spacing_inches", "UADA general range", "Ruling A (2026-10-05; replaces 'home-garden "
        "scope wins', withdrawn: UGA C766 is ALSO a home-garden publication). UADA FSA-6107 gives the general "
        "home-garden range for red raspberries, tied to how the row middles are managed: [60,120]. UGA's 12 ft is a "
        "single point for the types it covers in Georgia (erect primocane reds: \"set the plants 2 feet apart in rows "
        "12 feet apart.\"; trailing Dormanred: \"if more than one row is to be planted, space the rows 12 feet "
        "apart.\"), [144,144], not used. PSU (commercial) \"rows are typically spaced 8 to 12 feet apart in field "
        "production, and 7 feet to 8 feet apart in tunnel production.\" [96,144], not used.")
    dec("raspberry", S, "Dormanred named", "Rulings C and 2 (2026-10-05): both planting-notes leaves attribute "
        "Dormanred's spacing to UGA, which spaces it like a trailing blackberry (its section \"growing trailing "
        "blackberries and the dormanred raspberry\": 10 ft between plants, rows 12 ft). Not stated as an exception "
        "to the general figures, because UADA lists Dormanred among its red raspberries and does not exempt it from "
        "its 5 to 10 ft range (review round 2). UGA's timing \"plant trailing brambles between december and "
        "march.\" is NOT stated in the leaves: it is left to the se_gulf region cell.")
    dec("raspberry", f"{ENTRY}.row_spacing_inches", "yellow in scope", "UADA states the figure for red raspberries; "
        "yellow takes it via UMN: \"yellow raspberries are red raspberries that don't make red pigment.\"")
    dec("raspberry", f"{ENTRY}.row_spacing_inches", "red/yellow-scoped", "Ruling D: the figure is red/yellow-scoped, "
        "but the field carries no type limit, so consumers apply it to black and purple too. Black needs 8 to 10 ft "
        "(UADA: \"black raspberry row spacing should be wider (8-10 feet between rows) due to their sprawling growth "
        "habit.\"). Noted on PLA-12: the type-scoped figure becomes an override when variety/type slots exist.")
    dec("raspberry", f"{ENTRY}.row_spacing_inches", "bytes re-verified", "UADA FSA-6107 re-fetched 2026-10-04 under "
        "both user agents: byte-identical to its 2026-10-01 MANIFEST row (c8bb32a4).")
    dec("raspberry", f"{ENTRY}.anchoring_urls.umn_ext", "kept", "umn_ext anchors the unchanged in-row [18,24] (and "
        "the yellow scope row).")
    for slug in ("raspberry", "pawpaw"):
        dec(slug, f"{ENTRY}.row_spacing_reason", "null by rule", "An entry's reason is null iff its row figure is "
            "non-null (spec §1.6 item 5).")
        dec(slug, "row_spacing_reason", "null by rule", "The crop-root reason is null iff row_spacing_inches is "
            "non-null (spec §1.6 item 7).")
    dec("pawpaw", f"{ENTRY}.row_spacing_inches", "orchard scope admitted", "Methodology rule, RULED for TREES (Trevor, "
        "2026-10-05; proposed earlier the same day without the scope): rows between trees follow canopy and light rather "
        "than equipment, so an orchard T1 tree-row figure is admissible when no home-garden page gives one; for canes "
        "and row crops home-garden scope still wins (the raspberry ruling stands). No hashed cited page gives a "
        "home-garden pawpaw row figure. KSU PBI-004 is an organic ORCHARD production guide. Also orchard-scoped and not used: ACES "
        "\"for commercial planting, place trees 6 to 10 feet apart within a row, with rows 15 to 20 feet apart.\" "
        "and MU AF1021 \"space tree rows 15 to 20 feet apart, with trees spaced 6 to 10 feet apart in the planting "
        "row.\" [180,240].")
    dec("pawpaw", f"{ENTRY}.row_spacing_inches", "same institution, agreeing in-row", "Ruling 5 as corrected: KSU "
        "PBI-004 is preferred because the in-row 96 is anchored to KSU's planting-guide page (\"when planting trees, "
        "allow 8 feet (2.5m) between them.\") and PBI-004 agrees on the in-row: \"8 feet with in rows\".")
    dec("pawpaw", f"{ENTRY}.row_spacing_inches", "Cornell in-row only", "Cornell Small Farms gives in-row only "
        "(\"should be spaced from eight to 15 feet apart\"); that sentence is in the article body (bytes of 64f2a976 on "
        "the element tags: body div 170,452, the sentence 174,913, comments div 198,037). The page's spam is a reader "
        "comment (PLA-679).")
    dec("pawpaw", f"{ENTRY}.anchoring_urls.ksu_pawpaw", "kept", "ksu_pawpaw (the planting-guide page) keeps the "
        "in-row [96,96] anchor.")
    dec("pawpaw", f"{ENTRY}.row_spacing_inches", "pdf extraction", "The PBI-004 quote keeps pypdf's extraction "
        "artifacts ('p resently', 'with in') so it is a substring of the pinned extractor's text.")
    dec("<catalog>", PBI[0], "minted", "A document-scoped child of ksu_pawpaw (the clemson_hgic_cucurbit_insects "
        "pattern): title and authors from PBI-004's own heading \"kentucky state university cooperative extension "
        "program organic production of pawpaw kirk w. pomper, ph.d., sheri b. crabtree, m.sc., and jeremy d. lowe\".")
    dec("elderberry", f"{ENTRY}.row_spacing_inches", "not_authored after hunt", "Ruling 6: no hashed cited page states "
        "an elderberry row figure. PSU gives in-row only (\"ensure spacing is 5 to 7 feet between plants\"); NCSU "
        "none; MU AF1017's cited url is a landing page (the guide PDF is uncited; lead on PLA-625); MSU returns an "
        "Incapsula block under the browser, plain and Safari user agents (PLA-678). The hunt ends at the block; "
        "row_spacing_reason stays not_authored. No canonical change.")

    dec("raspberry", "start_method", "citation block added", "start_method had no sources / anchoring_urls; its "
        "re-authored leaves cite umn_ext and uada_ext_fsa6107 there, the broad-beans-fava start_method precedent "
        "(Housekeeping 60 Phase C); key order anchoring_urls then sources, as fava's.")
    dec("raspberry", "start_method.notes_seasoned", "cut", "Ruling E: depth and handle (rulings 1 and 3), 'not from "
        "seed', 'the common, economical choice', 'own-root / no rootstock or grafting' (on no hashed page), every "
        "support-timing claim and 'late winter' cut.")
    dec("raspberry", "start_method.notes_beginner", "cut", "Ruling E: depth, handle, 'rather than growing from seed', "
        "support timing and 'late winter' cut.")
    dec("raspberry", f"{GS0}.user_action_seasoned", "cut", "Ruling E: depth, handle, 'bramble history' (on no hashed "
        "page; UMN's 'destroying wild or abandoned brambles near the garden' is about neighbors) and every "
        "support-timing claim ('put the trellis or support up now') cut; the support conflict is stated with "
        "attribution instead (UMN all types vs UADA black no trellis / Dormanred must be trellised; PLA-534).")
    dec("raspberry", f"{GS0}.user_action_seasoned", "PSU commercial scope admitted", "Penn State's raspberry-production "
        "page is a commercial guide; its verticillium rotation is admitted because no hashed home-garden page cited on "
        "raspberry states one (the proposed methodology rule, PLA-666 DECISIONS, 2026-10-05), and the leaf attributes "
        "it by name.")
    dec("raspberry", f"{GS0}.user_action_beginner", "cut", "Ruling E: depth, handle and support timing ('set up a "
        "stake or trellis') cut; UMN's support sentence stated with attribution.")
    dec("raspberry", f"{GS0}.what_to_look_for_seasoned", "cut", "Ruling E: 'late winter to early spring', 'in most "
        "regions', 'prepared' and 'with support in place' cut.")
    dec("raspberry", "start_method.notes_seasoned", "timing", "'Early spring' (UMN: \"early spring is the best time "
        "to plant raspberries.\"); the planting notes say 'spring' (UADA: \"planting should occur in the spring\"). "
        "Both rest on 'as soon as the soil can be worked'; Dormanred's December-to-March timing is the se_gulf cell's.")

    for path in ORTHO_PATHS:
        dec("raspberry", path, "orthography-only", "Ruling 1 (2026-10-05): 'Dorman Red' -> 'Dormanred', the spelling "
            "of UGA C766, UADA FSA-6107 and the TAMU page. Spelling only: this leaf's claims were NOT reviewed.")
    dec("raspberry", "varieties.recommended[12].name", "left: lookup key", "Ruling 1's key exception: the variety "
        "has no id, so consumers slugify its name (dorman-red); renaming it would break stored plantings' variety "
        "lookups. 'Dorman Red' stays here, and in regions.rgv.plantings_provenance and "
        "verification_status.open_findings[2]/[3] (records, not display text).")

    with open(os.path.join(HERE, "ops.json"), "w", encoding="utf-8") as f:
        json.dump(ops, f, ensure_ascii=False, indent=1)
        f.write("\n")
    for name, cols, data in (("EVIDENCE.tsv", EVIDENCE_COLS, rows),
                             ("DECISIONS.tsv", ("crop", "path", "decision", "reason"), D)):
        with open(os.path.join(HERE, name), "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols, delimiter="\t", lineterminator="\n")
            w.writeheader()
            w.writerows(data)
    print(f"wrote {len(ops)} ops, {len(rows)} evidence rows, {len(D)} decisions")


if __name__ == "__main__":
    main()
