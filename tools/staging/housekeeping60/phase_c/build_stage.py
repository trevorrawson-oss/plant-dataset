#!/usr/bin/env python3
"""build_stage -- writes ops.json, EVIDENCE.tsv and DECISIONS.tsv for promote_housekeeping60_phase_c (Phase C, part 1).

Every `new` prose string below is Trevor's, verbatim, from "PHASE C STRINGS, PART 1" (claude.ai, 2026-10-04). Every
quote is a sentence from the Phase C packets (docs/kickoffs/61-phase-c-quote-packets/), i.e. the hashed bytes of a page
cited on the crop. `old` values are read from the base canonical (b331e5f2) so the promote refuses a drifted base.
Re-run from the repo root: python3 tools/staging/housekeeping60/phase_c/build_stage.py
"""
import csv, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "tools"))
from cited_promote_common import EVIDENCE_COLS, resolve  # noqa: E402

TODAY = "2026-10-04"
ABSENT = "<absent>"
CATALOG = "<catalog>"

U = {  # url per (crop, source id) where the new anchor is minted here
    "ncsu_chives": "https://plants.ces.ncsu.edu/plants/allium-schoenoprasum/",
    "umn_chives": "https://extension.umn.edu/vegetables/growing-chives",
    "wisc_chives": "https://hort.extension.wisc.edu/articles/chives-allium-schoenoprasum/",
    "illinois_chives": "https://extension.illinois.edu/herbs/chives",
    "tamu_eht044": "https://aggie-horticulture.tamu.edu/wp-content/uploads/sites/10/2013/09/EHT-044.pdf",
    "wsu": "https://s3.wp.wsu.edu/uploads/sites/2073/2014/09/Home-Vegetable-Gardening-in-Washington.pdf",
    "isu_corn": "https://yardandgarden.extension.iastate.edu/how-to/growing-sweet-corn-home-garden",
    "umn_corn": "https://extension.umn.edu/vegetables/growing-sweet-corn",
    "scc_fava": "https://ucanr.edu/site/uc-master-gardeners-santa-clara-county/fava-beans",
    "ncsu_fava": "https://plants.ces.ncsu.edu/plants/vicia-faba/",
    "umn_beans": "https://extension.umn.edu/vegetables/growing-beans",
    "clemson_wm": "https://hgic.clemson.edu/factsheet/watermelon/",
    "clemson_insects": "https://hgic.clemson.edu/factsheet/cucumber-squash-melon-other-cucurbit-insect-pests/",
    "uga_wm": "https://fieldreport.caes.uga.edu/publications/C1035/",
    "usu_ti": "https://extension.usu.edu/yardandgarden/research/tomatillos-in-the-garden",
    "sdsu_ti": "https://extension.sdstate.edu/tomatillo-how-grow-it",
    "ncsu_ti": "https://plants.ces.ncsu.edu/plants/physalis-philadelphica/",
    "umn_ti": "https://extension.umn.edu/vegetables/growing-tomatillos-and-ground-cherries",
    "alameda_ti": "https://ucanr.edu/site/uc-master-gardener-program-alameda-county/article/guide-growing-tomatillos",
    "usu_lav": "https://extension.usu.edu/yardandgarden/research/english-lavender-in-the-garden",
    "ncsu_lav": "https://plants.ces.ncsu.edu/plants/lavandula-angustifolia/",
    "umn_basil": "https://extension.umn.edu/vegetables/growing-basil",
}


def a(url):
    return {"url": url, "verified": TODAY}


def load():
    with open(os.path.join(REPO, "crops_data_final.json"), encoding="utf-8") as f:
        return json.load(f)


DATA = load()
IDX = {c["slug"]: c for c in DATA["crops"]}


def old(crop, path):
    root = DATA["source_catalog"] if crop == CATALOG else IDX[crop]
    try:
        conc = resolve(root, path)
    except Exception:
        return ABSENT
    node = root
    for s in conc[:-1]:
        node = node[s]
    k = conc[-1]
    if isinstance(node, dict) and k not in node:
        return ABSENT
    return node[k]


OPS, EV, DEC = [], [], []


def op(crop, path, kind, new, cited_at, reason):
    OPS.append({"crop": crop, "path": path, "kind": kind, "old": old(crop, path), "new": new,
                "cited_at": cited_at, "reason": reason})


def ev(crop, path, field, value, sid, url, quote):
    EV.append({"crop": crop, "entry_id": path, "field": field, "value": value, "source_id": sid, "url": url,
               "sha256": None, "quote": quote})


def dec(crop, path, decision, reason):
    DEC.append({"crop": crop, "path": path, "decision": decision, "reason": reason})


def anchors_add(crop, block, add, reason, keep=(), drop=(), sources=True):
    """Add (and drop) anchors on a block; sources (where the block has / gets them) follow the same ids."""
    cur = old(crop, f"{block}.anchoring_urls")
    cur = {} if cur == ABSENT else dict(cur)
    for sid in drop:
        del cur[sid]
    for sid, url in add.items():
        if sid in cur:
            assert cur[sid]["url"] == url, (crop, block, sid)
        else:
            cur[sid] = a(url)
    op(crop, f"{block}.anchoring_urls", "anchors", cur, None, reason)
    if sources:
        s = old(crop, f"{block}.sources")
        s = [] if s == ABSENT else [x for x in s if x not in drop]
        s += [sid for sid in add if sid not in s]
        op(crop, f"{block}.sources", "sources", s, None, reason)
    for sid in keep:
        dec(crop, f"{block}.anchoring_urls.{sid}", "kept", keep[sid])


UNHASHED = "NOT hashed, so it cannot be shown to support nothing; the block keeps unedited leaves (decision 37)"

# ============================================================ CHIVES (ruling 7)
C, B = "chives", "varieties.recommended[0]"
P = f"{B}.note"
op(C, P, "prose", "The standard Allium schoenoprasum. It grows in clumps of fine, hollow, grass-like leaves about 1 to "
   "1.5 feet tall. Its edible flowers are round, pink to pale purple globes that bloom in late spring to early summer. "
   "The leaves have a mild onion flavor, and the plant is hardy.", B,
   "ruling 7: the species-type note follows NCSU's height; cut tidy / 8 to 14 / pom-pom / extremely / workhorse")
ev(C, P, "species", "the standard Allium schoenoprasum", "umn_ext", U["umn_chives"],
   "the chive plant, allium schoenoprasum , is a member of the onion family (alliaceae).")
ev(C, P, "clumps", "grows in clumps", "uwi_hort", U["wisc_chives"],
   "this species is a hardy herbaceous perennial that grows in dense clumps of slender bulbs")
ev(C, P, "leaves", "fine, hollow, grass-like leaves", "ncsu_ext", U["ncsu_chives"],
   "leaf description: hollow, fragrant, upright grass-like leaves forming clumps")
ev(C, P, "leaves", "fine (leaf texture)", "uiuc_ext", U["illinois_chives"],
   "they grow in clumps from underground bulbs and produce round, hollow leaves that are much finer than onion.")
ev(C, P, "leaves", "hollow, grass-like leaves", "umn_ext", U["umn_chives"],
   "its grass-like hollow leaves have a mild onion flavor and are common in salads and dips.")
ev(C, P, "height", "about 1 to 1.5 feet tall", "ncsu_ext", U["ncsu_chives"],
   "height: 1 ft. 0 in. - 1 ft. 6 in.")
ev(C, P, "flowers", "edible flowers", "umn_ext", U["umn_chives"],
   "these are edible, and you can use them in salads and flower arrangements.")
ev(C, P, "flowers", "round, pink to pale purple globes", "uwi_hort", U["wisc_chives"],
   "the pink to pale purple round globes are composed of many small, tightly packed, star-shaped florets")
ev(C, P, "bloom", "bloom in late spring to early summer", "umn_ext", U["umn_chives"],
   "the small puffs of flowers begin to bloom in late may or june.")
ev(C, P, "bloom", "bloom in late spring to early summer", "uwi_hort", U["wisc_chives"],
   "chives bloom in mid spring to early summer.")
ev(C, P, "flavor", "mild onion flavor", "uwi_hort", U["wisc_chives"],
   "today the leaves are typically used as a culinary herb with a mild onion flavor.")
ev(C, P, "hardy", "the plant is hardy", "umn_ext", U["umn_chives"],
   "a clump-forming habit and cold hardiness make this plant an appealing garden perennial.")
ev(C, P, "hardy", "the plant is hardy", "uwi_hort", U["wisc_chives"], "this plant, hardy to zone 4a")
dec(C, P, "height divergence", "the note follows NCSU's 1 ft 0 in - 1 ft 6 in (ruling 7). Illinois, now anchored on "
    "this entry for the leaf texture, says \"they are a hardy, drought-tolerant perennial growing to about 10-12 inches "
    "tall.\" (cacc0c83). Recorded, not followed (review 3).")
dec(C, P, "NCSU divergences", "NCSU (933eb2c4, the height page) also states \"leaf length: 3-6 inches\" and \"bloom "
    "april-may\". The note's 1 to 1.5 ft is NCSU's whole-plant height (ruling 7) and its late-spring-to-early-summer bloom "
    "follows UMN / Wisc. Recorded, not followed (Trevor, final round).")
dec(C, P, "bloom timing", "UMN (late May or June) and Wisc (mid spring to early summer) support 'late spring to early "
    "summer'; Illinois, cited on chives, says mid-summer: \"in mid-summer, they produce round, pink flowers similar in "
    "appearance to clover.\" (cacc0c83). Recorded, not followed (Trevor, Part 1).")
anchors_add(C, B, {"ncsu_ext": U["ncsu_chives"], "umn_ext": U["umn_chives"], "uwi_hort": U["wisc_chives"],
                   "uiuc_ext": U["illinois_chives"]},
            "the note's citations, in place on the variety entry (53 of 623 certified entries carry sources)")

# ============================================================ SWEET CORN (ruling 8, R5)
C = "sweet-corn"
for path, new in (("thinning.when", "after the plants are up"), ("thinning.to_spacing", "1 foot")):
    op(C, path, "prose", new, "thinning", "R5 / ruling 8: TAMU EHT-044's thinning sentence")
    ev(C, path, "thin", new, "tamu_agrilife", U["tamu_eht044"], "after the plants are up, thin them to 1 foot apart.")
op(C, "thin_to_inches", "value", [12, 12], "thinning", "R5: thin_to_inches [12,12] (TAMU EHT-044, 1 foot)")
ev(C, "thin_to_inches", "thin_to_inches", "[12,12]", "tamu_agrilife", U["tamu_eht044"],
   "after the plants are up, thin them to 1 foot apart.")
dec(C, "thin_to_inches", "ruled", "R5: [12,12], EHT-044's 1 foot. 8-12 in is ISU/UMN SEED spacing, not a thin-to "
    "figure; WSU (cited) advises sowing corn at final spacing to avoid thinning (carried into the tips).")
op(C, "thinning.method", "value", None, None, "R5: no hashed page states a thinning method")
dec(C, "thinning.method", "null", "R5: no hashed cited page states a method ('snip at the soil line' is on none, nor on "
    "EHT-044). Schema allows null: whole_crop_gate + register_completeness PASS on a scratch canonical with it null; no "
    "consumer reads thinning.method (decision 34).")
P = "thinning.tip_seasoned"
op(C, P, "prose", "In-row seed spacing is 8 to 12 inches. Sowing large seed like corn at the recommended spacing avoids "
   "thinning the stand later. If you sow at 3 to 4 inches instead, thin to 1 foot once the plants are up. Closer stands "
   "produce small, poorly filled ears.", "thinning", "R5: Trevor's tip; ISU/UMN seed spacing, WSU, EHT-044")
P2 = "thinning.tip_beginner"
op(C, P2, "prose", "Plant corn seeds 8 to 12 inches apart in the row. Big seeds like corn can go in at their final "
   "spacing, so you won't need to thin them later. If you planted them closer, about 3 to 4 inches apart, thin them to 1 "
   "foot apart once the plants are up. Corn left too close together makes small ears that don't fill out well.",
   "thinning", "R5: Trevor's tip; ISU/UMN seed spacing, WSU, EHT-044")
for p in (P, P2):
    ev(C, p, "seed spacing", "8 to 12 inches in the row", "iastate_ext", U["isu_corn"],
       "space seeds 8 to 12 inches apart in rows")
    ev(C, p, "seed spacing", "8 to 12 inches in the row", "umn_ext", U["umn_corn"],
       "plant seeds one inch deep, and eight to 12 inches apart, with rows 30 to 36 inches apart.")
    ev(C, p, "no thinning at final spacing", "large seed sown at the recommended spacing avoids thinning", "wsu_ext",
       U["wsu"], "plant large seeds such as beans, corn, and squash at the recommended row spacing to avoid having to "
       "thin the stand later.")
    ev(C, p, "close sowing", "3 to 4 inches", "tamu_agrilife", U["tamu_eht044"],
       "plant the corn seeds about 1 inch deep and 3 to 4 inches apart in the row.")
    ev(C, p, "thin", "thin to 1 foot once the plants are up", "tamu_agrilife", U["tamu_eht044"],
       "after the plants are up, thin them to 1 foot apart.")
    ev(C, p, "crowding", "closer stands produce small, poorly filled ears", "tamu_agrilife", U["tamu_eht044"],
       "if you plant them closer, your corn will have small, poorly-filled ears")
anchors_add(C, "thinning", {"tamu_agrilife": U["tamu_eht044"], "wsu_ext": U["wsu"], "iastate_ext": U["isu_corn"],
                            "umn_ext": U["umn_corn"]}, "R5: thinning.sources cover EHT-044, WSU, ISU and UMN")
B = "growth_stages[1]"
P = f"{B}.user_action_seasoned"
op(C, P, "prose", "Keep the block weed-free with frequent, shallow cultivation. Hoe only deep enough to cut weeds below "
   "the surface, since corn roots run close to the top of the soil. Water as needed to keep plants from wilting. If you "
   "sowed closer than the final spacing, thin to 1 foot apart now.", B, "ruling 8: Trevor's string")
P2 = f"{B}.user_action_beginner"
op(C, P2, "prose", "Keep weeds down by hoeing often and lightly. Only hoe deep enough to cut the weeds off just under the "
   "soil, because corn roots grow close to the surface. Water often enough that the plants don't wilt. If you planted "
   "the seeds closer together, thin the plants to 1 foot apart now.", B, "ruling 8: Trevor's string")
for p in (P, P2):
    ev(C, p, "cultivation", "frequent, shallow cultivation keeps weeds down", "umn_ext", U["umn_corn"],
       "frequent, shallow cultivation with a hoe or other tool will kill weeds before they become a problem.")
    ev(C, p, "hoe depth", "hoe only deep enough to cut weeds below the surface", "umn_ext", U["umn_corn"],
       "hoe just deeply enough to cut the weeds off below the surface of the soil.")
    ev(C, p, "roots", "corn roots run close to the top of the soil", "tamu_agrilife", U["tamu_eht044"],
       "deep hoeing will cut the corn roots, which are close to the top of the soil.")
    ev(C, p, "water", "water as needed to keep plants from wilting", "tamu_agrilife", U["tamu_eht044"],
       "water sweet corn as needed to keep it from wilting.")
    ev(C, p, "thin", "thin to 1 foot apart", "tamu_agrilife", U["tamu_eht044"],
       "after the plants are up, thin them to 1 foot apart.")
anchors_add(C, B, {"tamu_agrilife": U["tamu_eht044"], "umn_ext": U["umn_corn"]},
            "the stage's citations, in place (113 of 728 certified growth_stages entries carry sources)")

# ============================================================ FAVA (ruling 9)
C, B = "broad-beans-fava", "start_method"
P = f"{B}.notes_seasoned"
op(C, P, "prose", "Direct-sow the large, flattened seed, and thin seedlings to stand 8 to 10 inches apart. Santa Clara "
   "County's UC Master Gardeners grow fava as a cool-season crop, sowing in February or from August to September, "
   "possibly into October. Fall-planted beans typically begin producing in early spring. University of Minnesota "
   "Extension advises growing fava as you would peas, planting early in the spring. Fava needs cool weather, with highs "
   "only into the low 80s °F.", B,
   "ruling 9: rows 18 to 30 cut; seed-spacing clause cut (4 to 6 vs 3 to 5 stays with PLA-625)")
ev(C, P, "direct-sow; sowing months", "direct-sow; Aug-Sep, possibly Oct, or Feb (Santa Clara)",
   "ucanr_santa_clara_mg", U["scc_fava"], "direct seed 3 to 5 inches apart in february or in august to september, "
   "possibly into october depending on your microclimate.")
ev(C, P, "large seed", "the large seed", "ncsu_ext_toolbox_vicia_faba", U["ncsu_fava"],
   "major (broad beans) has large seeds, and is grown as a vegetable for human consumption.")
ev(C, P, "flattened seed", "large, flattened seed", "ncsu_ext_toolbox_vicia_faba", U["ncsu_fava"],
   "the seeds are .5 to 1 inch in diameter and are oval and compressed.")
ev(C, P, "thin", "thin to stand 8 to 10 inches apart", "ucanr_santa_clara_mg", U["scc_fava"],
   "thin to 8 to 10 inches apart.")
ev(C, P, "cool-season crop", "Santa Clara County's UC Master Gardeners grow fava as a cool-season crop", "ucanr_santa_clara_mg", U["scc_fava"],
   "grow well as a cool season crop in santa clara county.")
ev(C, P, "fall planting", "fall-planted beans begin producing in early spring", "ucanr_santa_clara_mg", U["scc_fava"],
   "fall-planted beans typically begin producing in early spring.")
ev(C, P, "as peas", "UMN: grow fava as you would peas, planting early in the spring", "umn_ext", U["umn_beans"],
   "grow as you would peas, planting early in the spring.")
ev(C, P, "cool weather", "highs only into the low 80s °F", "umn_ext", U["umn_beans"],
   "cool temperatures with highs only into the low eighties.")
anchors_add(C, B, {"ucanr_santa_clara_mg": U["scc_fava"], "ncsu_ext_toolbox_vicia_faba": U["ncsu_fava"],
                   "umn_ext": U["umn_beans"]},
            "the note's citations, in place (18 of 121 certified start_method blocks carry sources)")

# ============================================================ WATERMELON (ruling 10 + scope ruling)
C = "watermelon"
CL, CI, UG, WS = "clemson_hgic", "clemson_hgic_cucurbit_insects", "uga_ext", "wsu_ext"
ROOM = ("watermelons need a lot of room.",)
N_VINE = "too much nitrogen fertilizer can encourage excess vine growth and reduce fruit growth."
B = "yield_expectations"
P = f"{B}.per_plant_seasoned"
op(C, P, "prose", "Washington State's planning table gives 6 to 12 melons from 3 plants in a 10-foot row. Watermelons "
   "need a lot of room. Keep irrigation consistent through fruit set and development. Side-dress a second time after "
   "bloom, while fruit is developing, but avoid excess nitrogen, which encourages vine growth and reduces fruit growth.",
   B, "ruling 10: 24 sq ft clause dropped; per-plant yield replaced by WSU's row table")
ev(C, P, "yield", "6 to 12 melons from 3 plants per 10-ft row", WS, U["wsu"], "watermelon 3 6-12 melons")
ev(C, P, "room", "watermelons need a lot of room", CL, U["clemson_wm"], ROOM[0])
ev(C, P, "irrigation", "consistent irrigation through fruit set and development", CL, U["clemson_wm"],
   "it is extremely important to maintain consistent irrigation cycles during fruit set and development.")
ev(C, P, "side-dress", "side-dress a second time after bloom while fruit develops", CL, U["clemson_wm"],
   "sidedress a second time after bloom when fruit is developing on the vine.")
ev(C, P, "nitrogen", "excess nitrogen encourages vine growth, reduces fruit growth", CL, U["clemson_wm"], N_VINE)
dec(C, P, "24 sq ft dropped", "ruling 10: Clemson states \"a rule of thumb is to allow 24 square feet per plant.\" "
    "(77feea89); the clause and its 'for full-size types' qualifier are dropped from every leaf.")
P = f"{B}.factors_seasoned[2]"
op(C, P, "prose", "Space: watermelons need a lot of room. Planting too close, like overfeeding with nitrogen, leads to "
   "excessive vine growth and few fruit.", B, "ruling 10: 8 to 12 ft and 24 sq ft cut")
ev(C, P, "room", "watermelons need a lot of room", CL, U["clemson_wm"], ROOM[0])
ev(C, P, "crowding", "too close or too much nitrogen -> excessive vine, few fruit", CL, U["clemson_wm"],
   "excessive vine growth and few fruit are usually the result of an over-application of nitrogen fertilizer or by "
   "planting too close.")
P = f"{B}.first_year_note_seasoned"
op(C, P, "prose", "Plan for three things. Watermelons need a lot of room. Fruit set depends on insects such as honeybees "
   "and bumblebees to carry pollen, so consider a honeybee colony nearby. And ripeness takes judgment: check that the "
   "fruit has reached its expected size, the tendril closest to the fruit has turned brown, the rind has gone from "
   "glossy to dull, and the underside shows a large white to cream spot.", B, "scope ruling: 8 to 12 ft cut")
ev(C, P, "room", "watermelons need a lot of room", CL, U["clemson_wm"], ROOM[0])
ev(C, P, "pollination", "insects such as honeybees and bumblebees carry pollen", CL, U["clemson_wm"],
   "insects, such as honeybees, native bumblebees, and others, are necessary for proper pollination.")
ev(C, P, "honeybee colony", "consider a honeybee colony", CL, U["clemson_wm"],
   "to promote proper pollination, consider establishing a honeybee colony on site.")
ev(C, P, "ripeness", "expected size, brown tendril, dull rind, large white to cream spot", CL, U["clemson_wm"],
   "the fruit looks to be expected size, the tendril closest to the fruit turns brown, the skin color loses its gloss "
   "and becomes dull in color, and the bottom of the fruit has a large white to cream color oval spot.")
anchors_add(C, B, {"uga_ext": U["uga_wm"], WS: U["wsu"], CL: U["clemson_wm"]},
            "the three re-authored leaves cite WSU and Clemson",
            keep={"uga_ext": "hashed; no edited leaf uses it; the block's unedited leaves (peak_production_*, "
                             "first_year_note_beginner, factors_seasoned[0,1]) were not re-read this pass "
                             "(decision 37)",
                  "usu_ext": UNHASHED})
for p, new in (("soil_prep_seasoned",
                "Choose a well-drained site with 8 to 10 hours of sun a day. Incorporate organic matter such as compost "
                "into the native soil before planting. Go light on nitrogen, since too much encourages excess vine "
                "growth and reduces fruit growth. Plant in small hills spaced 8 feet apart on all sides. Black plastic "
                "mulch warms the soil faster in spring, conserves moisture, and gives watermelons an early start. It also "
                "helps control weeds and reduces fruit rot."),
               ("soil_prep_beginner",
                "Pick a spot that drains well and gets 8 to 10 hours of sun. Mix compost into your soil before planting. "
                "Don't overdo nitrogen-rich fertilizer, or you'll get lots of vine and less fruit. Plant seeds in small "
                "hills 8 feet apart in every direction. Black plastic laid over the soil warms it faster in spring and "
                "gives the plants an early start. The plastic also holds in moisture, keeps weeds down, and cuts down on "
                "rotten fruit.")):
    op(C, p, "prose", new, None, "scope ruling: 8 to 12 ft, 24 sq ft and unsourced mound claims cut")
    dec(C, p, "record-only", "soil_prep has no citation sibling on any crop (0 of 121); the sources live in these "
        "EVIDENCE rows until PLA-674 rules soil_prep_sources / soil_prep_anchoring_urls (Trevor, 2026-10-04)")
    ev(C, p, "site", "well-drained, 8 to 10 hours of sun", UG, U["uga_wm"],
       "watermelons need a well-drained soil that receives 8 to 10 hr of sunlight per day.")
    ev(C, p, "compost", "incorporate compost into the native soil", UG, U["uga_wm"],
       "adding organic matter in the form of topsoil, compost or a bagged amendment and incorporating into the native "
       "soil can help improve soil quality.")
    ev(C, p, "nitrogen", "too much nitrogen: excess vine, less fruit", CL, U["clemson_wm"], N_VINE)
    ev(C, p, "hills", "small hills 8 feet apart on all sides", UG, U["uga_wm"],
       "plant watermelon from seed in small hills with a spacing of 8 ft on all sides.")
    ev(C, p, "black plastic", "warms the soil faster in spring, conserves moisture", CL, U["clemson_wm"],
       "the black plastic will warm the soil faster in the spring and will also conserve moisture throughout the season.")
    ev(C, p, "black plastic", "an early start", CL, U["clemson_wm"],
       "black plastic in the field gives watermelons an early start to growth.")
    ev(C, p, "black plastic", "weed control, less fruit rot", CL, U["clemson_wm"],
       "other advantages of this type of mulch are weed control and a reduction of fruit rot.")
B = "growth_stages[2]"
P = f"{B}.user_action_seasoned"
op(C, P, "prose", "The first side-dressing goes on before the vines start to run; give a second after bloom while fruit "
   "develops. Mulch with dried "
   "grass clippings, straw, or wood chips to conserve water and hold down weeds. Give the runners plenty of room. Scout "
   "leaf undersides for aphids, which usually arrive once vines form runners. In hot, dry weather, watch the upper leaf "
   "surfaces for spider mite damage, pale yellow to reddish-brown spots.", B, "scope ruling: 8 to 12 ft cut")
ev(C, P, "side-dress", "before the vines start to run", CL, U["clemson_wm"],
   "melons should be side-dressed before the vines start to \"run.\"")
ev(C, P, "side-dress", "again after bloom while fruit develops", CL, U["clemson_wm"],
   "sidedress a second time after bloom when fruit is developing on the vine.")
ev(C, P, "mulch", "dried grass clippings, straw or wood chips; conserve water, hold down weeds", UG, U["uga_wm"],
   "mulch the plants with weed-free grass clippings (already dried, not green), straw or wood chips to prevent weeds "
   "from growing and to conserve water.")
ev(C, P, "room", "give the runners plenty of room", CL, U["clemson_wm"], ROOM[0])
ev(C, P, "aphids", "aphids on leaf undersides", CI, U["clemson_insects"],
   "they are found chiefly on the underside of the leaves, where they suck the sap from the plants")
ev(C, P, "aphids", "aphids usually arrive once vines form runners", CI, U["clemson_insects"],
   "usually, cucurbits are not attacked by aphids until the vines form runners.")
ev(C, P, "spider mites", "spider mites in hot, dry weather", CI, U["clemson_insects"],
   "can be a serious problem on cucurbits, especially on watermelons and cantaloupes, during hot, dry weather.")
ev(C, P, "spider mites", "upper leaf surfaces, pale yellow to reddish-brown spots", CI, U["clemson_insects"],
   "this damage appears as pale yellow and reddish-brown spots ranging in size from small specks to large whitish, "
   "stippled areas on the upper sides of leaves.")
anchors_add(C, B, {CL: U["clemson_wm"], UG: U["uga_wm"], CI: U["clemson_insects"]},
            "the stage's citations, in place; the insect page needs its own id (decision 36)")
B = "tips_by_stage.vining[0]"
P = f"{B}.text_seasoned"
op(C, P, "prose", "Hold back on extra nitrogen. Too much encourages excess vine growth and reduces fruit, and so does "
   "planting too close.", B, "scope ruling: 8 to 12 ft cut")
ev(C, P, "nitrogen", "too much nitrogen: excess vine growth, reduced fruit", CL, U["clemson_wm"], N_VINE)
ev(C, P, "crowding", "planting too close does the same", CL, U["clemson_wm"],
   "excessive vine growth and few fruit are usually the result of an over-application of nitrogen fertilizer or by "
   "planting too close.")
anchors_add(C, B, {CL: U["clemson_wm"]}, "the tip's citation, in place (834 of 1147 certified tips carry sources)")
op(CATALOG, CI, "catalog", {
    "id": CI, "name": "Clemson HGIC 2207 -- Cucumber, Squash, Melon & Other Cucurbit Insect Pests",
    "title": "Cucumber, Squash, Melon & Other Cucurbit Insect Pests", "publisher": "Clemson University",
    "url": U["clemson_insects"], "source_class": "university_extension", "trust_tier": "high",
    "accessed": "2026-10", "tier": "T1",
    "citable_for": "Clemson HGIC 2207 factsheet: cucurbit insect pests (melon aphids, two-spotted spider mites) and "
                   "where and when they appear on watermelon vines."}, None,
   "decision 36: a document-scoped id for the insect page (the portal id clemson_hgic anchors the watermelon factsheet "
   "on the same block); title read off the hashed page's <title> (535e3615)")

# ============================================================ TOMATILLO (PLA-652, ruling 11, R2-R4, R6)
C = "tomatillo"
B = "det_indet"
SEAS = ("Tomatillos are indeterminate: they keep flowering and fruiting until frost, which allows multiple harvests "
        "through the season. Unlike tomatoes, which have both determinate and indeterminate varieties, all tomatillo "
        "varieties are indeterminate. Plants grow 3 to 4 feet tall and wide with a bushy, sprawling habit, and stems "
        "root where they touch the ground. Stake, cage, or trellis each plant to keep fruit off the ground and improve "
        "air circulation. Tomatillos weigh less than tomato plants, so they are easier to support. Habit varies by "
        "variety: Rendidora grows upright, while Gigante, Tamayo, Toma Verde, and Gulliver Hybrid sprawl more.")
BEG = ("Tomatillos keep growing, flowering, and making fruit until frost, so you can pick them many times over the "
       "season. Every tomatillo variety grows this way. Tomatoes are different: some tomato varieties grow this way and "
       "others don't. The plants get big, about 3 to 4 feet tall and just as wide. Give each one a cage, stake, or "
       "trellis to keep the fruit off the ground and let air move through the leaves. Tomatillo plants are lighter than "
       "tomato plants, so they are easier to hold up.")
op(C, f"{B}.detail_seasoned", "prose", SEAS, B, "PLA-652 / R4: re-authored from the tomatillo pages")
op(C, f"{B}.detail_beginner", "prose", BEG, B, "PLA-652 / R4: re-authored from the tomatillo pages")
for p in (f"{B}.detail_seasoned", f"{B}.detail_beginner"):
    ev(C, p, "indeterminate", "flowers and fruits until frost", "usu_ext", U["usu_ti"],
       "tomatillos are an indeterminate plant, meaning they will continue to flower and fruit until frost.")
    ev(C, p, "multiple harvests", "fruit through the season, multiple harvests", "sdsu_ext", U["sdsu_ti"],
       "tomatillos are indeterminate plants, meaning that they will produce fruit continuously throughout the season, "
       "which allows for multiple harvests.")
    ev(C, p, "all varieties", "all tomatillo varieties are indeterminate", "usu_ext", U["usu_ti"],
       "tomatillos are not self-fertile like tomatoes, and all varieties are indeterminate.")
    ev(C, p, "tomatoes differ", "tomatoes have both determinate and indeterminate varieties", "usu_ext", U["usu_ti"],
       "in contrast, tomatoes have varieties that are both indeterminate and determinate.")
    ev(C, p, "size", "3 to 4 feet tall and wide", "usu_ext", U["usu_ti"], "tomatillos grow 3-4 feet tall and wide")
    ev(C, p, "size", "3 to 4 feet tall and wide", "ncsu_ext", U["ncsu_ti"],
       "these easy to grow indeterminate plants grow to 3 to 4 feet in height and width and they produce fruits until "
       "the first frost.")
    ev(C, p, "support", "stake or cage to keep fruit off the ground and improve air circulation", "usu_ext", U["usu_ti"],
       "trellis tomatillos have an indeterminate, sprawling growth habit and benefit from staking or caging plants to "
       "keep fruit off the ground and improve air circulation through the plant.")
    ev(C, p, "support", "trellis, cage, or support each plant", "sdsu_ext", U["sdsu_ti"],
       "plan to trellis, cage, or otherwise support each plant.")
    ev(C, p, "lighter", "weigh less than tomato plants, easier to support", "usu_ext", U["usu_ti"],
       "tomatillos weigh less than tomato plants, and therefore, can be supported much easier.")
P = f"{B}.detail_seasoned"
ev(C, P, "habit", "bushy habit", "sdsu_ext", U["sdsu_ti"],
   "tomatillos have a bushy habit and should be transplanted with 3 feet between plants.")
ev(C, P, "habit", "bushy habit", "umn_ext", U["umn_ti"],
   "tomatillos need more space, as much as three feet, because of their bushy habit.")
ev(C, P, "rooting stems", "stems root where they touch the ground; sprawling", "ncsu_ext", U["ncsu_ti"],
   "the stems easily root when they come into contact with the ground so its sprawling habit needs support like a "
   "tomato cage or trellis in the landscape or vegetable garden.")
ev(C, P, "varieties", "Rendidora upright; Gigante, Tamayo, Toma Verde, Gulliver Hybrid sprawl more", "usu_ext",
   U["usu_ti"], "green varieties include: rendidora, (upright growth; high yields), gigante, tamayo, toma verde, and "
   "gulliver hybrid have more sprawling growth habits.")
op(C, f"{B}.anchoring_urls", "anchors",
   {"usu_ext": a(U["usu_ti"]), "sdsu_ext": a(U["sdsu_ti"]), "ncsu_ext": a(U["ncsu_ti"]), "umn_ext": a(U["umn_ti"])},
   None, "R4: det_indet anchors = USU, SDSU, NCSU, UMN (the pages the strings use); the three cherry-tomato anchors "
   "(clemson blog, cornell tomato guide, umd tomatoes) drop")
dec(C, f"{B}.anchoring_urls", "no sources key", "decision 38: no certified crop's det_indet carries `sources`; R4's "
    "'anchoring_urls / sources' is met by the anchors")
dec(C, f"{B}.type", "unchanged", "R4: type stays 'indeterminate' (USU: \"all varieties are indeterminate.\")")
op(C, "days_to_maturity_anchoring_urls", "anchors", {"sdsu_ext": a(U["sdsu_ti"])}, None,
   "R3: re-anchor days_to_maturity [65,100] to SDSU; the four tomato anchors drop")
ev(C, "days_to_maturity_anchoring_urls", "days_to_maturity", "[65,100] from transplant", "sdsu_ext", U["sdsu_ti"],
   "tomatillos will be ready to harvest 65 to 100 days after transplanting.")
op(C, "days_to_maturity_mid", "value", None, None, "R2: TAMU's 90-day basis is unclear -> null")
dec(C, "days_to_maturity_mid", "null", "R2: TAMU 21aeb3a5 \"mature fruit are produced in about 90 days.\" follows "
    "\"plant in full sunlight after all danger of frost.\" ('plant' does not say transplant or seed: unclear). No hashed "
    "page cited on tomatillo states a single typical figure; [65,100] is SDSU's range. Consumers handle null (plant-app "
    "effectiveDtm typeof guard; plant-astro z.number().nullish(); 30 certified crops already null) (decision 33).")
op(C, "days_to_maturity_mid_anchoring_urls", "delete", None, None,
   "R2: the mid is null; no null-mid crop carries a mid-anchoring key (decision 39)")
B = "failure_diagnostics[5]"
P = f"{B}.next_season_tip_beginner"
op(C, P, "prose", "Tomatillos need at least 6 hours of direct sun a day, and South Dakota State Extension recommends 8. "
   "If your spot gets less than that, choose a sunnier spot next season.", B,
   "ruling 11: 'cherry tomatillo' and other unsourced claims cut")
ev(C, P, "sun", "at least 6 hours of direct sun", "ncsu_ext", U["ncsu_ti"],
   "light: full sun (6 or more hours of direct sunlight a day)")
ev(C, P, "sun", "South Dakota State Extension recommends 8", "sdsu_ext", U["sdsu_ti"],
   "tomatillos need 8 hours of sun per day.")
# ---- Part 2 (Trevor, 2026-10-04): R9 re-authors what_happened_*; the seasoned tip; R8 drops all four tomato anchors
TI_6 = ("tomatillos need at least six hours of sunlight per day.", "light: full sun (6 or more hours of direct sunlight a day)")
TI_8 = "tomatillos need 8 hours of sun per day."
TI_N = "too much nitrogen fertilization will lead to plants that are bushy, leafy, and slow to bear fruit."
TI_WET = "wet leaves are more disease-prone."
TI_HUMID = "rainy periods or humid, windless days can encourage foliar diseases."
TI_DIS = "early blight , anthracnose, late blight, and tobacco mosaic virus can affect tomatillos."
TI_FULL = "they prefer full sun and well-drained soils."
TI_AM = "sprinkle irrigate in the morning to allow the foliage dry out before night- fall."
P = f"{B}.what_happened_beginner"
op(C, P, "prose", "Tomatillos need full sun, at least 6 hours of direct sunlight a day, and South Dakota State Extension "
   "recommends 8. If your plants got less than that, the spot was too shady for them. If your plants were very leafy and slow to make fruit, "
   "also check your fertilizer: too much nitrogen makes tomatillos bushy, leafy, and slow to bear fruit. Wet leaves get "
   "diseases more easily, so if you water with a sprinkler, do it in the morning so the leaves dry before night.", B,
   "R9: live-data finding; the leafy / slow-to-fruit cause is nitrogen on UMN and USU, not shade")
P2 = f"{B}.what_happened_seasoned"
op(C, P2, "prose", "Tomatillos need full sun: NC State calls for 6 or more hours of direct sunlight a day, UC Master "
   "Gardeners (Alameda) at least six hours of sunlight, and South Dakota State 8. A bushy, leafy plant that is slow to bear may also point to excess "
   "nitrogen, which produces exactly that growth. Foliar disease is a separate risk: wet leaves are more disease-prone, "
   "rainy periods or humid, windless days can encourage foliar diseases, and early blight, anthracnose, late blight, and "
   "tobacco mosaic virus can all affect tomatillos.", B, "R9: as the beginner register")
P3 = f"{B}.next_season_tip_seasoned"
op(C, P3, "prose", "Tomatillos need full sun. NC State calls for 6 or more hours of direct sunlight a day and UC Master "
   "Gardeners (Alameda) at least six hours of sunlight; South Dakota State recommends 8. If the bed fell short, move the planting to a sunnier site "
   "next season.", B, "Part 2: 'cherry tomatillo' and every unsourced claim cut (ruling 11)")
for p in (P, P2, P3):
    ev(C, p, "full sun", "tomatillos need full sun", "usu_ext", U["usu_ti"], TI_FULL)
    ev(C, p, "sun", "6 or more hours of direct sunlight (NC State)", "ncsu_ext", U["ncsu_ti"], TI_6[1])
    ev(C, p, "sun", "8 hours (South Dakota State)", "sdsu_ext", U["sdsu_ti"], TI_8)
for p in (P2, P3):
    ev(C, p, "sun", "at least six hours of sunlight (UC Master Gardeners, Alameda)", "ucanr_ext", U["alameda_ti"], TI_6[0])
for p in (P, P2):
    ev(C, p, "nitrogen", "too much nitrogen: bushy, leafy, slow to bear fruit", "umn_ext", U["umn_ti"], TI_N)
    ev(C, p, "over-fertilizing", "over-fertilizing: excess leaf growth, delayed fruit set (supports, not states, N)", "usu_ext", U["usu_ti"],
       "avoid over-fertilizing tomatillos, which causes excess leaf growth and delays fruit set and maturity.")
    ev(C, p, "wet leaves", "wet leaves are more disease-prone", "umn_ext", U["umn_ti"], TI_WET)
ev(C, P, "morning water", "if watering with a sprinkler, do it in the morning so leaves dry before night", "usu_ext", U["usu_ti"], TI_AM)
ev(C, P2, "humid", "rainy periods or humid, windless days can encourage foliar diseases", "umn_ext", U["umn_ti"], TI_HUMID)
ev(C, P2, "diseases", "early blight, anthracnose, late blight, tobacco mosaic virus", "umn_ext", U["umn_ti"], TI_DIS)
ev(C, P2, "diseases", "early blight, anthracnose, late blight, tobacco mosaic virus", "sdsu_ext", U["sdsu_ti"],
   "early blight, anthracnose, late blight, and tobacco mosaic virus can affect tomatillos.")
anchors_add(C, B, {"ucanr_ext": U["alameda_ti"], "ncsu_ext": U["ncsu_ti"], "sdsu_ext": U["sdsu_ti"],
                   "umn_ext": U["umn_ti"], "usu_ext": U["usu_ti"]},
            "R8: the entry is authored entirely from tomatillo pages; all four tomato anchors drop",
            drop=("umn_ext", "umd_ext", "iastate_ext", "cornell_ext"))
dec(C, f"{B}.anchoring_urls", "R8", "all four tomato anchors dropped (ISU, Cornell hashed and unused; UMN growing-"
    "tomatoes and UMD unhashed, tomato pages carried over from cherry-tomato: the PLA-652 defect itself). umn_ext now "
    "names UMN's tomatillo page.")
for p in ("weather_triggers[0].body_beginner", "weather_triggers[0].body_seasoned",
          "failure_diagnostics[1].what_happened_beginner", "failure_diagnostics[1].what_happened_seasoned"):
    op(C, p, "orthography", old(C, p).replace("Tomatilloes", "Tomatillos"), None,
       "spelling only: 'Tomatilloes' -> 'Tomatillos' (Trevor, 2026-10-04)")
    dec(C, p, "orthography-only", "spelling fixed ('Tomatilloes' -> 'Tomatillos'); the leaf's claims were NOT reviewed "
        "and this edit is not verification. Routed to PLA-625 for claim review.")
P = "verification_status.verification_log_ref"
o = old(C, P)
op(C, P, "append", o + " [CORRECTION 2026-10-04: det_indet and days_to_maturity anchors were carried over from "
   "cherry-tomato, not re-derived for tomatillo. Re-anchored to tomatillo pages in housekeeping 60 Phase C "
   "(PLA-652). The four tomato anchors on failure_diagnostics[5] were dropped in the same pass.]", None, "R6: append-only cert-log correction, original untouched")

# ============================================================ LAVENDER (finding (a))
C, B = "lavender", "diseases[1]"
L_SPACE = "space lavender plants 18-24 inches apart into light, well aerated, gravelly soil."
L_AIR = "providing good air circulation helps prevent leaf spot."
L_SUN_DRY = "this plant requires perfectly drained soil, preferably on the dry side, and full sun."
L_WATER = "do not overwater or let water stand around the plants."
for leaf, new, extra in (
        ("control_ladder[0].note_beginner",
         "Plant lavender 18 to 24 inches apart in full sun, in soil that drains well and stays on the dry side. Good "
         "airflow around the plants helps prevent leaf spot.", ()),
        ("control_ladder[0].note_seasoned",
         "Space plants 18 to 24 inches apart in full sun, on perfectly drained soil that stays on the dry side. NC State "
         "reports no significant problems for English lavender, though it is susceptible to leaf spot and root rot. Good "
         "air circulation helps prevent leaf spot, and root rot is caused by overwatering.", ("rot",)),
        ("prevention_seasoned",
         "Space plants 18 to 24 inches apart in full sun, with good air circulation to help prevent leaf spot.", ()),
        ("prevention_beginner",
         "Leave 18 to 24 inches between plants, give them full sun, and keep air moving around them to help prevent "
         "leaf spot.", ())):
    p = f"{B}.{leaf}"
    op(C, p, "prose", new, B, "finding (a): prose moves to the field's 18 to 24 inches (USU)")
    ev(C, p, "spacing", "18 to 24 inches apart", "usu_ext_english_lavender", U["usu_lav"], L_SPACE)
    ev(C, p, "site", "full sun, well-drained soil on the dry side", "ncsu_ext_lavandula_angustifolia", U["ncsu_lav"],
       L_SUN_DRY)
    ev(C, p, "airflow", "air circulation helps prevent leaf spot", "ncsu_ext_lavandula_angustifolia", U["ncsu_lav"], L_AIR)
    if "rot" in extra:
        ev(C, p, "problems", "no significant problems; susceptible to leaf spot and root rot",
           "ncsu_ext_lavandula_angustifolia", U["ncsu_lav"], "no significant problems. however, it is susceptible to leaf "
           "spot and root rot.")
        ev(C, p, "root rot", "caused by overwatering", "ncsu_ext_lavandula_angustifolia", U["ncsu_lav"],
           "root rot is caused by overwatering.")
    if "water" in extra:
        ev(C, p, "water", "do not overwater or let water stand", "usu_ext_english_lavender", U["usu_lav"], L_WATER)
anchors_add(C, B, {"usu_ext_english_lavender": U["usu_lav"]}, "the 18 to 24 inch figure is USU's",
            keep={"ncsu_ext": "NC State newcropsorganics, " + UNHASHED, "rhs": "RHS Hidcote, " + UNHASHED})
dec(C, "diseases[1].control_ladder[0]", "placement accepted", "the pre-existing rung airflow_spacing on diseases[1] "
    "(leaf spot) implies spacing, sun and soil prevent leaf spot, which no hashed lavender page states; NCSU ties only "
    "air circulation to leaf spot. The four edited leaves state only hashed claims and make only NCSU's link (Trevor, "
    "final round). The rung's structure is routed to PLA-625.")
PNW = ("NC State lists English lavender as hardy in zones 5a through 9b. It does not like wet feet and will die out in "
       "heavy clay, and overwatering causes root rot. Prune every year after flowering. Space plants 18 to 24 inches "
       "apart; good air circulation helps prevent leaf spot.")
for z in ("8", "9"):
    B = f"regions.pnw.resolved_by_zone.{z}"
    p = f"{B}.frost_risk_note_seasoned"
    op(C, p, "prose", PNW, B, "finding (a): 2 to 3 feet and the unhashed (OSU) attribution go")
    ev(C, p, "hardiness", "zones 5a through 9b", "ncsu_ext_lavandula_angustifolia", U["ncsu_lav"],
       "usda plant hardiness zone: 5a, 5b, 6a, 6b, 7a, 7b, 8a, 8b, 9a, 9b")
    ev(C, p, "wet feet", "does not like wet feet, will die out in heavy clay", "ncsu_ext_lavandula_angustifolia",
       U["ncsu_lav"], "english lavender does not like wet feet and will die out in heavy clays.")
    ev(C, p, "root rot", "overwatering causes root rot", "ncsu_ext_lavandula_angustifolia", U["ncsu_lav"],
       "root rot is caused by overwatering.")
    ev(C, p, "pruning", "prune every year after flowering", "usu_ext_english_lavender", U["usu_lav"],
       "lavender should be pruned every year after flowering.")
    ev(C, p, "spacing", "18 to 24 inches apart", "usu_ext_english_lavender", U["usu_lav"], L_SPACE)
    ev(C, p, "airflow", "air circulation helps prevent leaf spot", "ncsu_ext_lavandula_angustifolia", U["ncsu_lav"], L_AIR)
    keep = {sid: UNHASHED for sid in (old(C, f"{B}.sources") or []) if sid != "usu_ext_english_lavender"}
    anchors_add(C, B, {"usu_ext_english_lavender": U["usu_lav"], "ncsu_ext_lavandula_angustifolia": U["ncsu_lav"]},
                "Trevor, Part 1: add USU and NCSU to the entry's sources", keep=keep)

# ============================================================ BASIL (finding (a))
C = "basil"
B = "failure_diagnostics[2]"
P = f"{B}.next_season_tip_seasoned"
op(C, P, "prose", "Plant a variety resistant to basil downy mildew. UMN Extension names downy mildew the most common basil "
   "problem in Minnesota and recommends choosing a resistant variety.", B, "finding (a): 12-18 in and unsourced claims cut")
ev(C, P, "resistant variety", "choose a variety resistant to basil downy mildew", "umn_ext", U["umn_basil"],
   "due to the emergence of basil downy mildew , it is important to choose a variety resistant to this disease .")
ev(C, P, "most common", "downy mildew is the most common basil problem in Minnesota", "umn_ext", U["umn_basil"],
   "the most common basil issue in minnesota is basil downy mildew .")
anchors_add(C, B, {"umn_ext": U["umn_basil"]}, "Trevor, Part 1: add UMN to the entry's sources",
            keep={sid: UNHASHED for sid in ("umd_ext", "umass_ext", "cornell_ext")})
B = "tips_by_stage.seedling[0]"
P = f"{B}.text_seasoned"
op(C, P, "prose", "Thin or transplant seedlings to stand 6 to 12 inches apart once they have two to three pairs of true "
   "leaves.", B, "finding (a): UMN's 6-12 and its timing")
ev(C, P, "thin", "6 to 12 inches apart at two to three pairs of true leaves", "umn_ext", U["umn_basil"],
   "thin and transplant seedlings to stand 6-12 inches apart once they have developed two to three pairs of true "
   "leaves.")

P = f"{B}.text_beginner"
op(C, P, "prose", "Wait until your basil seedlings have two or three pairs of true leaves, not counting the two broad "
   "seed leaves. Then thin them so the plants stand 6 to 12 inches apart.", B,
   "Part 2: timing now matches the seasoned register (UMN)")
ev(C, P, "thin", "6 to 12 inches apart at two or three pairs of true leaves", "umn_ext", U["umn_basil"],
   "thin and transplant seedlings to stand 6-12 inches apart once they have developed two to three pairs of true "
   "leaves.")
ev(C, P, "seed leaves", "the two broad seed leaves are named apart from the true leaves", "umn_ext", U["umn_basil"],
   "the basil seedling is recognizable by its two broad seed leaves")
anchors_add(C, B, {"umn_ext": U["umn_basil"]}, "Part 2: both texts are UMN's; the unhashed USU anchor drops (nothing in "
            "the tip uses it)", drop=("usu_ext",))

# ============================================================ OREGANO (finding (a) + rgv misattribution, Part 2)
C = "oregano"
UF = "https://blogs.ifas.ufl.edu/pascoco/2024/04/02/spice-up-your-life-a-beginners-guide-to-growing-oregano/"
TAMU = "https://agrilifeextension.tamu.edu/wp-content/uploads/2025/06/growingherbsintexas_4-1.pdf"
NCSU = "https://plants.ces.ncsu.edu/plants/origanum-vulgare/"
UF_SPACE = ("adequate air circulation : space your plants 10-12 inches apart, this will help with air circulation and "
            "prevent extra humidity that attracts pests and diseases.")
UF_PM = "to prevent powdery mildew, provide good air circulation around plants and avoid overhead watering."
UF_ROT = ("oregano is generally resistant to diseases, but it can occasionally suffer from fungal infections like powdery "
          "mildew or root rot, especially in humid conditions.")
TAMU_ROW = "plant in rich soil. space 8-10 in. start in protected location and move to full sun."
TAMU_DIV = "divide plants every 3 or 4 years in the early spring."
B = "diseases[2]"
P = f"{B}.control_ladder[0].note_seasoned"
op(C, P, "prose", "UF/IFAS recommends spacing plants 10 to 12 inches apart to improve air circulation and prevent the "
   "extra humidity that attracts pests and diseases. To prevent powdery mildew, UF/IFAS pairs good air circulation with "
   "avoiding overhead watering. Oregano generally resists disease but can occasionally get powdery mildew or root rot, "
   "especially in humid conditions.", B, "finding (a): 'up to 18 inches' and unsourced claims cut")
ev(C, P, "spacing", "10 to 12 inches for air circulation and less humidity", "uf_ifas", UF, UF_SPACE)
ev(C, P, "powdery mildew", "air circulation plus avoiding overhead watering", "uf_ifas", UF, UF_PM)
ev(C, P, "disease", "generally resists disease; powdery mildew or root rot in humid conditions", "uf_ifas", UF, UF_ROT)
dec(C, f"{B}.anchoring_urls.ucanr_ext", "kept", "UC IPM pn7406, " + UNHASHED + " (no anchor op on this block)")
G = ("Oregano is a hardy perennial. Texas A&M AgriLife's herb guide recommends full sun after a protected start and "
     "spacing of 8 to 10 inches; UF/IFAS gives 10 to 12 inches for air circulation. Texas A&M advises dividing perennial "
     "herbs every 3 or 4 years in early spring. Humid conditions can bring on root rot, so plant in well-drained soil "
     "with good air circulation. UF/IFAS recommends raised beds in humid central Florida to control moisture.")
S = ("grown_as=perennial: oregano is a woody, branching perennial (NCSU). Bloom (May to July) is reused from this crop's "
     "own se_gulf zone 9/10 rows, frost/phenology-modeled rather than read from a Valley-specific chart. Texas A&M "
     "AgriLife's statewide herb guide recommends full sun and 8 to 10 inch spacing for oregano, and dividing perennial "
     "herbs every 3 or 4 years in early spring. plant_out follows the general cool-season, avoid-peak-heat convention. "
     "Flagged blocks_launch:false: no oregano-specific RGV chart exists.")
for z in ("9", "10"):
    B = f"regions.rgv.resolved_by_zone.{z}"
    P = f"{B}.grown_as_note_seasoned"
    op(C, P, "prose", G, B, "Part 2: TAMU's oregano row (8 to 10) restored; 10-12 attributed to UF")
    ev(C, P, "perennial", "a hardy perennial", "uf_ifas", UF, "oregano is a hardy perennial")
    ev(C, P, "TAMU", "full sun after a protected start; 8 to 10 inches", "tamu_agrilife", TAMU, TAMU_ROW)
    ev(C, P, "UF spacing", "10 to 12 inches for air circulation", "uf_ifas", UF, UF_SPACE)
    ev(C, P, "division", "divide perennial herbs every 3 or 4 years in early spring", "tamu_agrilife", TAMU, TAMU_DIV)
    ev(C, P, "root rot", "humid conditions can bring on root rot", "uf_ifas", UF, UF_ROT)
    ev(C, P, "drainage", "well-drained soil", "uf_ifas", UF, "oregano prefers slightly dry, well-draining soil")
    ev(C, P, "airflow", "good air circulation against humidity", "uf_ifas", UF, UF_SPACE)
    ev(C, P, "raised beds", "raised beds in central Florida to control moisture", "uf_ifas", UF,
       "in central florida, it is beneficial to grow oregano in raised beds to better control moisture retention and "
       "soil texture.")
    ev(C, P, "humid central Florida", "central Florida is humid", "uf_ifas", UF,
       "these varieties are better suited to withstand central florida's high temperatures and humidity.")
for B in ("regions.rgv.plantings[0]", "regions.rgv.resolved_by_zone.9", "regions.rgv.resolved_by_zone.10"):
    P = f"{B}.synthesis_note_seasoned"
    op(C, P, "prose", S, B, "Part 2: TAMU's oregano row (8 to 10) restored; woodiness credited to NCSU")
    ev(C, P, "woody", "a woody, branching perennial", "ncsu_ext", NCSU,
       "oregano is a woody, branching, herbaceous perennial with a bushy habit in the mint family native to europe and "
       "asia.")
    ev(C, P, "TAMU", "full sun and 8 to 10 inch spacing for oregano", "tamu_agrilife", TAMU, TAMU_ROW)
    ev(C, P, "division", "divide perennial herbs every 3 or 4 years in early spring", "tamu_agrilife", TAMU, TAMU_DIV)
dec(C, "spacing_inches", "unchanged; TAMU/UF difference recorded", "the field stays [10,12] (UF: \"space your plants "
    "10-12 inches apart\"); TAMU's oregano row says \"space 8-10 in.\" and now appears attributed beside it in the rgv "
    "notes. Noted on PLA-625 with the jalapeno / brussels field questions (Trevor, Part 2).")


# ============================================================ PART 3 (Trevor, 2026-10-04): beginner siblings
C = "watermelon"
P = "yield_expectations.per_plant_beginner"
op(C, P, "prose", "Washington State's planning table expects about 6 to 12 melons from 3 plants in a 10-foot row. "
   "Watermelons need a lot of room. Water steadily while the fruit sets and grows. Feed them a second time after they "
   "bloom, while the fruit is growing, but don't overdo nitrogen: too much gives you more vine and less fruit.",
   "yield_expectations", "Part 3: per-plant count, full-size, icebox and fruit-thinning claims cut")
ev(C, P, "yield", "6 to 12 melons from 3 plants per 10-ft row", WS, U["wsu"], "watermelon 3 6-12 melons")
ev(C, P, "room", "watermelons need a lot of room", CL, U["clemson_wm"], ROOM[0])
ev(C, P, "water", "water steadily while the fruit sets and grows", CL, U["clemson_wm"],
   "it is extremely important to maintain consistent irrigation cycles during fruit set and development.")
ev(C, P, "feed", "a second feeding after bloom while fruit grows", CL, U["clemson_wm"],
   "sidedress a second time after bloom when fruit is developing on the vine.")
ev(C, P, "nitrogen", "too much nitrogen: more vine, less fruit", CL, U["clemson_wm"], N_VINE)
P = "growth_stages[2].user_action_beginner"
op(C, P, "prose", "Plants get their first feeding before the vines start to run and a second one after they bloom, "
   "while fruit is growing. Spread mulch, such as dried grass clippings, straw, or wood chips, to save water and keep weeds down. Give "
   "the vines plenty of room to spread. Check under the leaves for aphids, which usually show up once the vines start "
   "running. In hot, dry weather, also watch for spider mites: these tiny mites leave pale yellow to reddish-brown "
   "specks on the tops of the leaves.", "growth_stages[2]", "Part 3: timing and pest surfaces follow Clemson")
ev(C, P, "feed", "before the vines start to run", CL, U["clemson_wm"],
   "melons should be side-dressed before the vines start to \"run.\"")
ev(C, P, "feed", "again after bloom while fruit grows", CL, U["clemson_wm"],
   "sidedress a second time after bloom when fruit is developing on the vine.")
ev(C, P, "mulch", "dried grass clippings, straw or wood chips; save water, keep weeds down", UG, U["uga_wm"],
   "mulch the plants with weed-free grass clippings (already dried, not green), straw or wood chips to prevent weeds "
   "from growing and to conserve water.")
ev(C, P, "room", "plenty of room to spread", CL, U["clemson_wm"], ROOM[0])
ev(C, P, "aphids", "aphids under the leaves", CI, U["clemson_insects"],
   "they are found chiefly on the underside of the leaves, where they suck the sap from the plants")
ev(C, P, "aphids", "aphids show up once the vines start running", CI, U["clemson_insects"],
   "usually, cucurbits are not attacked by aphids until the vines form runners.")
ev(C, P, "spider mites", "spider mites in hot, dry weather", CI, U["clemson_insects"],
   "can be a serious problem on cucurbits, especially on watermelons and cantaloupes, during hot, dry weather.")
ev(C, P, "spider mites", "tiny mites", CI, U["clemson_insects"],
   "these tiny mites feed on the contents of individual cells of the leaves.")
ev(C, P, "spider mites", "pale yellow to reddish-brown specks on the tops of the leaves", CI, U["clemson_insects"],
   "this damage appears as pale yellow and reddish-brown spots ranging in size from small specks to large whitish, "
   "stippled areas on the upper sides of leaves.")
C = "broad-beans-fava"
P = "start_method.notes_beginner"
op(C, P, "prose", "Plant the big, flat fava seeds right where they will grow, then thin the seedlings to about 8 to 10 "
   "inches apart. Favas are a cool-season crop and like highs no warmer than the low 80s °F. In Santa Clara County, "
   "California, UC Master Gardeners sow them in February or from August to September, sometimes into October, and "
   "fall-planted beans usually start producing in early spring. University of Minnesota Extension says to plant them "
   "early in spring, the way you would peas.", "start_method",
   "Part 3: 4 to 6 (PLA-625), depth, slow sprouting, three weeks, no indoor start and late-winter planting cut")
ev(C, P, "direct-sow", "plant where they will grow", "ucanr_santa_clara_mg", U["scc_fava"],
   "direct seed 3 to 5 inches apart in february or in august to september, possibly into october depending on your "
   "microclimate.")
ev(C, P, "big seed", "big seeds", "ncsu_ext_toolbox_vicia_faba", U["ncsu_fava"],
   "major (broad beans) has large seeds, and is grown as a vegetable for human consumption.")
ev(C, P, "flat seed", "flat seeds", "ncsu_ext_toolbox_vicia_faba", U["ncsu_fava"],
   "the seeds are .5 to 1 inch in diameter and are oval and compressed.")
ev(C, P, "thin", "thin to about 8 to 10 inches apart", "ucanr_santa_clara_mg", U["scc_fava"],
   "thin to 8 to 10 inches apart.")
ev(C, P, "cool-season", "a cool-season crop", "ncsu_ext_toolbox_vicia_faba", U["ncsu_fava"],
   "this cool season crop can be grown in most climates")
ev(C, P, "heat", "highs no warmer than the low 80s °F", "umn_ext", U["umn_beans"],
   "cool temperatures with highs only into the low eighties.")
ev(C, P, "Santa Clara dates", "February or August to September, sometimes into October", "ucanr_santa_clara_mg",
   U["scc_fava"], "direct seed 3 to 5 inches apart in february or in august to september, possibly into october")
ev(C, P, "fall planting", "fall-planted beans start producing in early spring", "ucanr_santa_clara_mg", U["scc_fava"],
   "fall-planted beans typically begin producing in early spring.")
ev(C, P, "as peas", "UMN: plant early in spring, the way you would peas", "umn_ext", U["umn_beans"],
   "grow as you would peas, planting early in the spring.")


# ------------------------------------------------------------ write
def main():
    man = {}
    with open(os.path.join(REPO, "tools", ".evidence_cache", "MANIFEST.tsv"), encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            man.setdefault(r["url"], r["sha256"])
    for r in EV:
        r["sha256"] = man[r["url"]]
    with open(os.path.join(HERE, "ops.json"), "w", encoding="utf-8") as f:
        json.dump(OPS, f, ensure_ascii=False, indent=1)
        f.write("\n")
    with open(os.path.join(HERE, "EVIDENCE.tsv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=EVIDENCE_COLS, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(EV)
    with open(os.path.join(HERE, "DECISIONS.tsv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=("crop", "path", "decision", "reason"), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(DEC)
    print(f"{len(OPS)} ops, {len(EV)} evidence rows, {len(DEC)} decisions")


if __name__ == "__main__":
    main()
