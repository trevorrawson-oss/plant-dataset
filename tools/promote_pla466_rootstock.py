#!/usr/bin/env python3
"""promote_pla466_rootstock -- PLA-466 rootstock attribution repair. Base 1721208e.

WHAT MOVES. Six crops plus one catalog entry. Nothing else.

 1. CATALOG. source_catalog.ucd_fruitnut.citable_for is widened to cover FNRIC's per-crop scion
    and rootstock selection pages, and to EXCLUDE per-region timing. The exclusion is the
    load-bearing half: it stops a widened id being used to hang timing cells on a rootstock page,
    which is the PLA-579 defect.

 2. PLUM ROSTER. St. Julien A is DROPPED (absent from the only cited T1 page across four Wayback
    captures 2025-05-24..2026-01-13 and Trevor's live 2026-09-21 save). Citation is ADMITTED at
    dwarf [8,12] from that page's own sentence. Marianna 2624 keeps semi_dwarf [10,15] (verbatim
    on the page) but its container_suitable and container_size_gallons go NULL: the page makes no
    container claim about any rootstock (container 0, gallon 0, pot 0 on all five reads).

 3. PLUM MYROBALAN ROW. Renamed to "Myrobalan 29C (P. cerasifera)" -- the page describes only the
    clonal selection, and seedling Myrobalan is on neither live source. clemson_hgic is DROPPED
    from the row: hgic.clemson.edu/factsheet/plum/ does not mention Myrobalan at all (Myrobalan 0,
    29C 0, sucker 0, wet 0, heavy 0), so the credit implied support it does not give. All three
    prose fields are replaced with text whose every claim maps to the page's own Myrobalan
    sentence.

 4. PLUM REPOINT. The three surviving rootstock rows move from the dead ucanr_ext URL to
    ucd_fruitnut at https://fruitsandnuts.ucdavis.edu/rootstock-selection, verified 2026-09-21.
    The old URL is dead for the public (residential read 403 while a control page on the same
    /site/ subtree returns 200). The verified date MOVES with the url -- carrying the old date
    onto a new url would fabricate the attribution (mandarin precedent, PLA-465).

 5. PLUM VARIETIES. The ucanr_ext credit is DROPPED, not repointed. The page carries 1 of the 7
    recommended varieties (Santa Rosa); the two "Burbank" hits are Luther Burbank the breeder.
    The cell keeps mu_ext and clemson_hgic, which have NOT been read against the seven names.

 6. LAUNCH FLAGS. plum, apple, pear-european and pear-asian take launch_ready_core=false and
    launch_ready_seasoned=false with a blocks_launch open finding. verification_status.status is
    UNTOUCHED: the values may be right, what failed is the attribution, and status is the page
    gate. These are the dataset's FIRST live blocking findings (all 12 existing ones are
    status:resolved).

 7. LEMON + LIME. The tristeza claim is corrected: both crops said susceptibility is "in some
    scion combinations"; HS402 says lemons are susceptible "regardless of rootstock" and CH092
    says the same flatly of Key limes. size_class goes NULL (not standard -- standard would be an
    unread value) on the semi_dwarf entries, and their container flags go null. lime's sour orange
    row gains uf_ifas_edis/CH092, recorded as a sourcing change.
    rootstock_selection_basis is NOT touched on either crop: held for Plan E's Rule N.

WHY EACH GUARD EXISTS.
 1. PINNED PRE-STATE, BY IDENTITY. Every row this promote touches is located by its exact current
    name and its exact current field values. A drift in any of them refuses rather than writing
    over an unexpected state.
 2. EVERY REPLACED STRING IS MATCHED EXACTLY ONCE. The four prose replacements are exact-substring
    edits whose target must occur exactly once in the field. A target found 0 or 2+ times refuses.
 3. SET COMPARISON BEFORE VALUE COMPARISON. assert set(pre) == set(post) at crop level and at row
    level BEFORE any value is compared -- iterating pre alone makes anything ADDED in post
    invisible, which was all four PLA-162 defects.
 4. BLAST RADIUS IS PINNED. Exactly 7 crops change (6 crops + the catalog is not a crop, so 6),
    and within each only the declared keys. The leaf count is pinned.
 5. THE CONTAINER NULL IS A FIRST. container_suitable has never been null on a rootstock row
    (45 false / 15 true / 0 null across all 60). The guard asserts the post-state has exactly 2,
    and rootstock_container_shape_gate enforces true|false|null from here on.
 6. LAUNCH FLAGS MOVE TOGETHER WITH A BLOCKING FINDING. A crop may not take launch_ready false
    without gaining a blocks_launch finding in the same pass, and status must NOT move.

Usage:
    promote_pla466_rootstock.py --check
    promote_pla466_rootstock.py --out /path/scratch.json
    promote_pla466_rootstock.py --expect-sha <sha>      # writes canonical, on approval
"""
import argparse
import copy
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CANON = os.path.join(REPO, "crops_data_final.json")

BASE_SHA = "1721208ee0cbe4249ecf32ca3bd47a786f8a689cadcb7bb300d8d8ada4d82054"
SESSION = "pla466_rootstock_2026_09_21"
VERIFIED = "2026-09-21"
ROSTER = 128

# The live save every plum claim is checked against. Hash computed in-session from the file
# Trevor saved from Safari on a residential connection, 2026-09-21.
NODE4506_SHA = "e68e8f91d7af6ecfbedf01a012cb80dcbd64b21c63981f741fe3c1a003e1707a"
NODE4506_BYTES = 35321
CLEMSON_PLUM_SHA = "4d7200773e2215ff468b659d253211273044a094e75eb2be8671ba480874dfaf"
CHILL_CANDIDATE_SHA = "41021901b9a55f0b378118b144ef5e57e5d1e51a427aa2bddc1eb51c47addbfa"

NEW_PLUM_URL = "https://fruitsandnuts.ucdavis.edu/rootstock-selection"
EXPECTED_PLUM_TITLE = "Plum Rootstock & Scion Selection"
# Carried on every repointed plum anchor. Two jobs: record WHY this path is fragile, and give
# PLA-568's instrument a literal to detect reuse of the generic path by another crop's page.
ANCHOR_NOTE = (
    "This is the page's own declared canonical, read from its <link rel=\"canonical\"> on "
    "2026-09-21. FRAGILE BY DESIGN: /rootstock-selection is a site-wide GENERIC path that FNRIC "
    "currently serves the plum page from. If FNRIC ever publishes a second crop's rootstock page "
    "the path is contested and this anchor would silently point at the wrong crop. Expected page "
    "title at this URL: \"" + EXPECTED_PLUM_TITLE + "\". A url_health instrument (PLA-568) should "
    "assert that title and flag a mismatch rather than trusting a 200. The stable alternative is "
    "the node reference /node/4506, not used here because the ucd_fruitnut precedent is "
    "word-paths and a node id breaks on a site migration."
)
ANCHOR = {"url": NEW_PLUM_URL, "verified": VERIFIED, "note": ANCHOR_NOTE}
DEAD_PLUM_URL = "https://ucanr.edu/site/fruit-nut-research-information-center/plum-rootstock-scion-selection"

# ---------------------------------------------------------------- catalog

UCD_CITABLE_FOR_OLD = (
    "The UC Davis Fruit & Nut Research & Information Center, the canonical California authority "
    "on tree-fruit chilling requirements and chill-accumulation models (its chill calculators are "
    "referenced by UC Master Gardener county pages). California chill-hour and deciduous-fruit "
    "phenology coverage."
)
UCD_CITABLE_FOR_NEW = (
    "The UC Davis Fruit & Nut Research & Information Center (FNRIC), the canonical California "
    "authority on tree-fruit chilling requirements and chill-accumulation models (its chill "
    "calculators are referenced by UC Master Gardener county pages), and its per-crop scion and "
    "rootstock selection pages. Citable for California chill-hour and deciduous-fruit phenology "
    "coverage, and for rootstock identity, graft compatibility, soil and pest traits, and any "
    "tree-size claim the page itself states for the scion it names. NOT citable for per-region "
    "planting, bloom or harvest timing."
)

# ---------------------------------------------------------------- plum rows

PLUM_PRE_NAMES = [
    "Myrobalan (P. cerasifera seedling / 29C)",
    "Marianna 2624",
    "St. Julien A (P. insititia)",
    "Guardian / Nemaguard (peach seedling, Southeast)",
]
PLUM_POST_NAMES = [
    "Myrobalan 29C (P. cerasifera)",
    "Marianna 2624",
    "Citation (P. salicina x P. persica)",
    "Guardian / Nemaguard (peach seedling, Southeast)",
]
MYROBALAN_NEW_NAME = "Myrobalan 29C (P. cerasifera)"
DROP_ROW = "St. Julien A (P. insititia)"

MYROBALAN_PROSE = {
    "traits_seasoned": (
        "A common plum rootstock, compatible with most cultivars, producing a hardy, vigorous, "
        "long-lived, full-size tree. It tolerates a wide range of soil types and climates but is "
        "prone to suckering. A reasonable choice where a full-size tree is wanted."
    ),
    "traits_beginner": (
        "A common full-size plum rootstock: tough, vigorous and long-lived, and it copes with a "
        "wide range of soils. It works with most plum varieties. Its one quirk is a tendency to "
        "send up suckers from the roots."
    ),
    "what_to_ask_nursery": (
        "Ask for your variety on Myrobalan 29C if you want a vigorous, full-size tree that adapts "
        "to a wide range of soils."
    ),
}

CITATION_ROW = {
    "name": "Citation (P. salicina x P. persica)",
    "size_class": "dwarf",
    "mature_height_ft": [8, 12],
    "spread_ft": None,
    "container_suitable": None,
    "container_size_gallons": None,
    "bearing_age_years": None,
    "what_to_ask_nursery": (
        "Ask for your variety on Citation if you want a smaller plum tree, around 8 to 12 feet "
        "tall."
    ),
    "traits_seasoned": (
        "A peach-plum hybrid rootstock that keeps a plum tree to about 8 to 12 feet. It tolerates "
        "wet soils and resists root-knot nematode, but it is susceptible to crown gall and "
        "bacterial canker."
    ),
    "traits_beginner": (
        "Keeps a plum tree small, about 8 to 12 feet tall. It copes with wet soil and resists "
        "root-knot nematodes (microscopic worms that attack roots), but it is prone to crown gall "
        "and bacterial canker, two bacterial diseases worth watching for."
    ),
    "sources": ["ucd_fruitnut"],
    "anchoring_urls": {"ucd_fruitnut": dict(ANCHOR)},
}

# ---------------------------------------------------------------- prose edits

# (crop, field-path-description, exact target, replacement). Each target must occur EXACTLY ONCE.
LEMON_NOTE_OLD = "Its one serious caveat is susceptibility to tristeza virus in some scion combinations."
LEMON_NOTE_NEW = (
    "Tristeza virus is a lemon problem rather than a rootstock one: lemon trees are susceptible "
    "to severe tristeza strains whatever the rootstock, and also to milder strains when grown on "
    "macrophylla or rough lemon. Buying certified disease-free trees reduces the chance of "
    "bringing one home infected."
)
SOUR_ORANGE_TRAITS_OLD = (
    "Main weakness is susceptibility to severe tristeza virus strains in some scion combinations."
)
LEMON_TRAITS_NEW = (
    "On lemon, susceptibility to severe tristeza strains does not depend on the rootstock, so it "
    "is not a reason to choose against this one."
)
LIME_NOTE_OLD = ", though it is susceptible to tristeza in some combinations."
LIME_NOTE_NEW = (
    ". Tristeza virus is a lime concern rather than a rootstock one: Key limes are susceptible to "
    "tristeza whatever the rootstock, and Tahiti limes may be susceptible to severe strains "
    "whatever the rootstock."
)
LIME_TRAITS_NEW = (
    "On lime, tristeza susceptibility does not depend on the rootstock: Key limes are susceptible "
    "regardless of rootstock, and Tahiti limes may be susceptible to severe strains regardless of "
    "it. It is not a reason to choose against this one."
)

SOUR_ORANGE = "sour orange (Citrus aurantium)"

# size_class -> null + container_suitable -> null, by (crop, row name).
NULL_SIZE_ROWS = [
    ("lemon", "trifoliate orange (Citrus trifoliata)"),
    ("lemon", "Carrizo / Swingle citrumelo (trifoliate hybrids)"),
    ("lime", "Swingle citrumelo (trifoliate hybrid)"),
]

LIME_CH092 = {"url": "https://ask.ifas.ufl.edu/publication/CH092", "verified": VERIFIED}

# ---------------------------------------------------------------- launch flips

# crop -> (sole_sourced_cells, co_sourced_cells)
CHILL_CROPS = {"apple": (4, 9), "pear-european": (1, 17), "pear-asian": (1, 18)}
LAUNCH_FLIP_CROPS = ["plum"] + sorted(CHILL_CROPS)

DEAD_CHILL_URL = "https://fruitsandnuts.ucdavis.edu/general-information/chilling-requirement"

# ---------------------------------------------------------------- pins

EXPECTED_CHANGED_CROPS = ["apple", "lemon", "lime", "pear-asian", "pear-european",
                          "persimmon", "plum"]
# plum Marianna + plum Citation, PLUS the three NULL_SIZE_ROWS, whose container flags are nulled
# in the same pass. Pinned at 5 after the guard refused a wrong pin of 2 on the first run.
EXPECTED_NULL_CONTAINER_ROWS = 5
EXPECTED_NULL_SIZE_ROWS = 3        # lemon x2 + lime x1
# plum 6 + (apple, pear-european, pear-asian) x 2 + lemon 2 + lime 2 + persimmon 1. Pinned
# after the guard refused wrong pins of 13 and 16 in turn.
EXPECTED_NEW_FINDINGS = 17
EXPECTED_BLOCKERS_AFTER = 4


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def serialize(data):
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def by_slug(data):
    return {c["slug"]: c for c in data["crops"]}


def load_canonical(path=None):
    p = path or CANON
    with open(p, "rb") as f:
        raw = f.read()
    return json.loads(raw.decode("utf-8")), sha256_bytes(raw)


def row_of(crop, name):
    for e in crop.get("rootstock_options") or []:
        if e.get("name") == name:
            return e
    return None


def replace_once(text, old, new, where):
    if text is None:
        raise SystemExit(f"REFUSED: {where}: field is null")
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"REFUSED: {where}: target found {n} times, expected exactly 1")
    return text.replace(old, new)


def finding(fid, severity, status, blocks, summary, basis, **extra):
    e = {
        "id": fid,
        "severity": severity,
        "status": status,
        "blocks_launch": blocks,
        "filed_in_session": SESSION,
        "summary": summary,
        "basis": basis,
    }
    e.update(extra)
    return e


# ------------------------------------------------------------------ pre-state

def check_pre_state(data):
    S = by_slug(data)
    if len(data["crops"]) != ROSTER:
        raise SystemExit(f"REFUSED: roster {len(data['crops'])}, pinned {ROSTER}")

    cat = data.get("source_catalog", {}).get("ucd_fruitnut")
    if cat is None:
        raise SystemExit("REFUSED: source_catalog.ucd_fruitnut absent")
    if cat.get("citable_for") != UCD_CITABLE_FOR_OLD:
        raise SystemExit("REFUSED: ucd_fruitnut.citable_for is not the pinned pre-state text")
    if cat.get("tier") != "T1":
        raise SystemExit(f"REFUSED: ucd_fruitnut tier {cat.get('tier')!r}, expected T1")

    plum = S["plum"]
    names = [e["name"] for e in plum["rootstock_options"]]
    if names != PLUM_PRE_NAMES:
        raise SystemExit(f"REFUSED: plum rootstock names drifted: {names}")

    myro = row_of(plum, PLUM_PRE_NAMES[0])
    if sorted(myro["sources"]) != ["clemson_hgic", "ucanr_ext"]:
        raise SystemExit(f"REFUSED: plum Myrobalan sources {myro['sources']}")
    if myro["anchoring_urls"].get("ucanr_ext", {}).get("url") != DEAD_PLUM_URL:
        raise SystemExit("REFUSED: plum Myrobalan is not on the dead ucanr_ext URL")

    mari = row_of(plum, "Marianna 2624")
    if mari["container_suitable"] is not True or mari["container_size_gallons"] != 25:
        raise SystemExit("REFUSED: plum Marianna container pre-state is not true/25")
    if mari["size_class"] != "semi_dwarf" or mari["mature_height_ft"] != [10, 15]:
        raise SystemExit("REFUSED: plum Marianna size pre-state drifted")

    if row_of(plum, DROP_ROW) is None:
        raise SystemExit("REFUSED: plum St. Julien A row is already absent")
    if row_of(plum, CITATION_ROW["name"]) is not None:
        raise SystemExit("REFUSED: plum already carries a Citation row")

    v = plum.get("varieties") or {}
    if "ucanr_ext" not in (v.get("sources") or []):
        raise SystemExit("REFUSED: plum.varieties does not carry the ucanr_ext credit")
    if (v.get("anchoring_urls") or {}).get("ucanr_ext", {}).get("url") != DEAD_PLUM_URL:
        raise SystemExit("REFUSED: plum.varieties ucanr_ext is not the dead URL")

    # every crop taking a launch flip must currently be true/true with status verified_gs_arc
    for slug in LAUNCH_FLIP_CROPS:
        vs = S[slug]["verification_status"]
        if vs.get("launch_ready_core") is not True or vs.get("launch_ready_seasoned") is not True:
            raise SystemExit(f"REFUSED: {slug} launch_ready is not true/true pre-state")
        if vs.get("status") != "verified_gs_arc":
            raise SystemExit(f"REFUSED: {slug} status {vs.get('status')!r}, expected verified_gs_arc")
        live = [f for f in (vs.get("open_findings") or [])
                if isinstance(f, dict) and f.get("blocks_launch") and f.get("status") != "resolved"]
        if live:
            raise SystemExit(f"REFUSED: {slug} already carries a live blocking finding")

    # the chill crops must still be on the dead chill URL, with the pinned sole/co counts
    for slug, (sole, co) in CHILL_CROPS.items():
        s_n, c_n = _chill_counts(S[slug])
        if (s_n, c_n) != (sole, co):
            raise SystemExit(f"REFUSED: {slug} chill cells {s_n}/{c_n}, pinned {sole}/{co}")

    # prose targets, exactly once each
    lem = S["lemon"]
    if lem["recommended_rootstock_note"].count(LEMON_NOTE_OLD) != 1:
        raise SystemExit("REFUSED: lemon note target not found exactly once")
    if not row_of(lem, SOUR_ORANGE)["traits_seasoned"].rstrip().endswith(SOUR_ORANGE_TRAITS_OLD):
        raise SystemExit("REFUSED: lemon sour orange traits target is not the last sentence")
    lim = S["lime"]
    if lim["recommended_rootstock_note"].count(LIME_NOTE_OLD) != 1:
        raise SystemExit("REFUSED: lime note target not found exactly once")
    if not row_of(lim, SOUR_ORANGE)["traits_seasoned"].rstrip().endswith(SOUR_ORANGE_TRAITS_OLD):
        raise SystemExit("REFUSED: lime sour orange traits target is not the last sentence")
    if "uf_ifas_edis" in (row_of(lim, SOUR_ORANGE)["sources"] or []):
        raise SystemExit("REFUSED: lime sour orange already carries uf_ifas_edis")

    for slug, name in NULL_SIZE_ROWS:
        r = row_of(S[slug], name)
        if r is None:
            raise SystemExit(f"REFUSED: {slug} row {name!r} absent")
        if r["size_class"] != "semi_dwarf":
            raise SystemExit(f"REFUSED: {slug}/{name} size_class {r['size_class']!r}, expected semi_dwarf")
        if r["container_suitable"] is not True:
            raise SystemExit(f"REFUSED: {slug}/{name} container_suitable is not true")

    # the container null is a FIRST: no rootstock row may be null pre-state
    nulls = [(c["slug"], e["name"]) for c in data["crops"]
             for e in (c.get("rootstock_options") or []) if e.get("container_suitable") is None]
    if nulls:
        raise SystemExit(f"REFUSED: container_suitable is already null on {nulls}")


def _chill_counts(crop):
    """(sole-sourced, co-sourced) anchoring cells citing the dead chill URL."""
    sole = co = 0

    def walk(o):
        nonlocal sole, co
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "anchoring_urls" and isinstance(v, dict):
                    hit = [kk for kk, e in v.items()
                           if isinstance(e, dict) and DEAD_CHILL_URL == (e.get("url") or "")]
                    if hit:
                        if len(v) == 1:
                            sole += 1
                        else:
                            co += 1
                elif v is not None:
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                if v is not None:
                    walk(v)

    walk(crop)
    return sole, co


# ------------------------------------------------------------------ apply

def apply(data):
    S = by_slug(data)
    data["source_catalog"]["ucd_fruitnut"]["citable_for"] = UCD_CITABLE_FOR_NEW

    plum = S["plum"]
    rows = plum["rootstock_options"]

    myro = row_of(plum, PLUM_PRE_NAMES[0])
    myro["name"] = MYROBALAN_NEW_NAME
    for k, v in MYROBALAN_PROSE.items():
        myro[k] = v
    myro["sources"] = ["ucd_fruitnut"]
    myro["anchoring_urls"] = {"ucd_fruitnut": dict(ANCHOR)}

    mari = row_of(plum, "Marianna 2624")
    mari["container_suitable"] = None
    mari["container_size_gallons"] = None
    mari["sources"] = ["ucd_fruitnut"]
    mari["anchoring_urls"] = {"ucd_fruitnut": dict(ANCHOR)}

    idx = next(i for i, e in enumerate(rows) if e["name"] == DROP_ROW)
    rows[idx] = copy.deepcopy(CITATION_ROW)

    v = plum["varieties"]
    v["sources"] = [s for s in v["sources"] if s != "ucanr_ext"]
    v["anchoring_urls"] = {k: val for k, val in v["anchoring_urls"].items() if k != "ucanr_ext"}

    # lemon
    lem = S["lemon"]
    lem["recommended_rootstock_note"] = replace_once(
        lem["recommended_rootstock_note"], LEMON_NOTE_OLD, LEMON_NOTE_NEW, "lemon note")
    so = row_of(lem, SOUR_ORANGE)
    so["traits_seasoned"] = replace_once(
        so["traits_seasoned"], SOUR_ORANGE_TRAITS_OLD, LEMON_TRAITS_NEW, "lemon sour orange traits")

    # lime
    lim = S["lime"]
    lim["recommended_rootstock_note"] = replace_once(
        lim["recommended_rootstock_note"], LIME_NOTE_OLD, LIME_NOTE_NEW, "lime note")
    lso = row_of(lim, SOUR_ORANGE)
    lso["traits_seasoned"] = replace_once(
        lso["traits_seasoned"], SOUR_ORANGE_TRAITS_OLD, LIME_TRAITS_NEW, "lime sour orange traits")
    lso["sources"] = sorted(set(lso["sources"]) | {"uf_ifas_edis"})
    lso["anchoring_urls"]["uf_ifas_edis"] = dict(LIME_CH092)

    for slug, name in NULL_SIZE_ROWS:
        r = row_of(S[slug], name)
        r["size_class"] = None
        r["container_suitable"] = None

    for slug in LAUNCH_FLIP_CROPS:
        vs = S[slug]["verification_status"]
        vs["launch_ready_core"] = False
        vs["launch_ready_seasoned"] = False

    for f in build_findings():
        S[f["crop"]]["verification_status"]["open_findings"].append(f["entry"])

    for slug, entry in build_field_additions().items():
        S[slug]["verification_status"].setdefault("field_additions", []).append(entry)

    return data


def build_field_additions():
    return {
        "plum": {
            "field": "rootstock_options",
            "date": VERIFIED,
            "sources": ["ucd_fruitnut"],
            "note": (
                "PLA-466. Myrobalan row renamed to the clonal selection and its three prose fields "
                "re-authored so every claim maps to the page's own sentence, read from Trevor's live "
                f"2026-09-21 save (node4506.html, {NODE4506_BYTES} bytes, sha256 {NODE4506_SHA}): "
                "compatible with most cultivars -> 'is compatible with most cultivars'; hardy, "
                "vigorous, long-lived, full-size -> 'produces a hardy, vigorous, long lived, standard "
                "size tree'; tolerates a wide range of soil types and climates -> 'tolerates a wide "
                "range of soil types and climatic conditions'; prone to suckering -> 'but is prone to "
                "suckering'. Citation admitted from the same page: peach-plum hybrid, dwarf 8 to 12 ft, "
                "tolerant of wet soils, resistant to root-knot nematode, susceptible to crown gall and "
                "bacterial canker, all in one sentence. Citation's two beginner glosses (nematodes as "
                "microscopic worms that attack roots; crown gall and bacterial canker as bacterial "
                "diseases) are general biology under the bio-accuracy carve-out, not page claims. "
                "clemson_hgic dropped from the Myrobalan row: its plum factsheet does not mention "
                f"Myrobalan at all (sha256 {CLEMSON_PLUM_SHA})."
            ),
        },
        "lime": {
            "field": "rootstock_options",
            "date": VERIFIED,
            "sources": ["uf_ifas_edis"],
            "note": (
                "PLA-466 SOURCING CHANGE. uf_ifas_edis (FC47/CH092, Key Lime Growing in the Florida "
                "Home Landscape) added to the sour orange row so the corrected tristeza sentence can "
                "carry its Key lime half. CH092 states flatly that Key limes are susceptible "
                "regardless of rootstock; CH093 hedges for Tahiti ('may be susceptible') and attributes "
                "the milder-strain half to a personal communication, which is deliberately NOT used. "
                "Each document is kept to its own lime."
            ),
        },
    }


def build_findings():
    F = []

    F.append({"crop": "plum", "entry": finding(
        "plum_st_julien_a_absent_from_cited_page", "high", "resolved", False,
        "St. Julien A (P. insititia) is ABSENT from the only T1 page it was cited to, and the row "
        "has been dropped. Measured on five independent reads of that page: four Wayback captures "
        "(2025-05-24, 2025-06-13, 2025-11-11, 2026-01-13) and Trevor's live residential save of the "
        "UC Davis mirror on 2026-09-21. Term counts identical on all five: Julien 0, insititia 0. "
        "The page enumerates exactly five rootstocks (Myrobalan 29C, Mariana 2624, Nemaguard, "
        "Lovell, Citation) and St. Julien is not among them. The NC-140 plum trials are NOT cited as "
        "a reason: they were not read in this arc, and PLA-463 already caught that claim being "
        "misapplied once.",
        f"Live save node4506.html, {NODE4506_BYTES} bytes, sha256 {NODE4506_SHA}, read 2026-09-21. "
        "Wayback captures read as original bytes via the id_ modifier.")})

    F.append({"crop": "plum", "entry": finding(
        "plum_marianna_container_claim_unsourced", "medium", "resolved", False,
        "Marianna 2624 kept semi_dwarf [10,15], which the page carries verbatim ('produces a "
        "semi-dwarf tree (10 to 15 ft)'), but its container_suitable:true and "
        "container_size_gallons:25 are NULLED. The page makes no container claim about any "
        "rootstock: container 0, gallon 0, pot 0 on all five reads. null rather than false because "
        "false would assert an unsourced negative; null records that it was not assessed.",
        f"Live save sha256 {NODE4506_SHA}. Same measurement across four Wayback captures.")})

    F.append({"crop": "plum", "entry": finding(
        "plum_myrobalan_claims_absent_from_both_sources", "medium", "resolved", False,
        "Three claims were removed from the Myrobalan row because they are ABSENT from both live "
        "sources. (a) 'the most tolerant of heavy, wet soils': the UC Davis page says only that "
        "Myrobalan 'tolerates a wide range of soil types and climatic conditions' and assigns wet "
        "and heavy soils to Mariana 2624 in the next paragraph; Clemson has wet 0, heavy 0. (b) "
        "'compatible with both European and Japanese plums': the page says 'compatible with most "
        "cultivars' and never splits the two; Clemson's European/Japanese sentences are about "
        "cross-pollination. (c) 'the clonal 29C selection suckers less': the page says only 'prone "
        "to suckering' and Clemson has sucker 0, 29C 0. A third field, what_to_ask_nursery, also "
        "carried (a) and was replaced in the same pass. The row was renamed to the clonal selection "
        "because seedling Myrobalan is described on neither source.",
        f"UC Davis live save sha256 {NODE4506_SHA}; Clemson HGIC 1358 read live 2026-09-21, sha256 "
        f"{CLEMSON_PLUM_SHA}, on which Myrobalan 0, 29C 0, sucker 0, wet 0, heavy 0.")})

    F.append({"crop": "plum", "entry": finding(
        "plum_myrobalan_numbers_unsourced", "low", "deferred", False,
        "Myrobalan's mature_height_ft [15,25], spread_ft [15,20] and bearing_age_years [3,5] are "
        "unsourced on both live pages and were NOT nulled in this pass. The UC Davis page says "
        "'standard size tree' with no figure, giving numbers only for Mariana (10 to 15 ft) and "
        "Citation (8 to 12 ft); Clemson does not mention Myrobalan. size_class:standard stays, as it "
        "is the page's own word. Same finding class as PLA-566 Finding 2 on apricot's row heights.",
        "Routed to Plan E's D-B nulling pass, which owes a consumer check before any null lands.",
        deferred_to="PLA-463 Plan E D-B")})

    F.append({"crop": "plum", "entry": finding(
        "plum_varieties_ucanr_credit_dropped", "medium", "resolved", False,
        "The ucanr_ext credit was DROPPED from plum.varieties rather than repointed. The page "
        "carries 1 of the 7 recommended varieties: Santa Rosa (5 hits). Methley 0, Green Gage 0, "
        "Reine Claude 0, Stanley 0, Italian Prune 0, Fellenberg 0. The two 'Burbank' hits are Luther "
        "Burbank the breeder ('Luther Burbank, a legendary plant breeder, introduced ...'), not the "
        "'Burbank' cultivar; the context was read rather than the term count trusted. The page's "
        "scion section is a California COMMERCIAL list; the dataset's is a home-garden list. "
        "IMPORTANT: the surviving sources mu_ext and clemson_hgic have NOT been read against the "
        "seven names. The cell keeps two UNCHECKED sources, not two verified ones.",
        f"Live save sha256 {NODE4506_SHA}, read 2026-09-21.")})

    F.append({"crop": "plum", "entry": finding(
        "plum_region_cells_cite_a_rootstock_page", "high", "open", True,
        "BLOCKS LAUNCH. 48 of plum's region cells anchor to a rootstock-and-scion selection page "
        "that carries no timing content: bloom 0, plant out 0, planting date 0, frost 0, chill 0, "
        "zone 0. Its 6 harvest hits are all California commercial cultivar timing (Friar early July, "
        "Angeleno late August through September). So Rio Grande Valley and Arizona low-desert harvest "
        "cells cite California commercial cultivar months, and bloom and plant_out cells cite a "
        "document with zero bloom and zero planting text. These fail the asparagus-R4 rule "
        "independently of the URL being dead. 39 of the cells have NO other source. The VALUES are "
        "not shown to be wrong; their attribution fails. Values are NOT nulled: the T1 re-source "
        "comes first, per the mandarin precedent that no claim-bearing cell is left uncited.",
        f"Page read in full, live save sha256 {NODE4506_SHA} plus four Wayback captures. Cell counts "
        "measured against canonical 1721208e: 52 refs total (48 regions, 3 rootstock_options, 1 "
        "varieties), 39 sole-sourced, 13 co-sourced, out of 220 anchoring refs on the crop.",
        deferred_to="PLA-579")})

    for slug, (sole, co) in sorted(CHILL_CROPS.items()):
        F.append({"crop": slug, "entry": finding(
            f"{slug.replace('-', '_')}_chill_anchor_dead_sole_sourced", "high", "open", True,
            f"BLOCKS LAUNCH. {sole} region cell(s) on this crop are SOLE-sourced to "
            f"{DEAD_CHILL_URL}, which is DEAD for the public. Confirmed from a residential Safari "
            "save on 2026-09-21: Cloudflare passed and the site itself answers 'Page not found. The "
            "requested page could not be found.' The content is UNRECOVERABLE: Wayback CDX returns "
            "zero captures for that URL, and that zero was retried after an Internet Archive outage "
            "and confirmed against an identically shaped query that did return captures. A proposed "
            "successor, /about-chilling-hours-units-and-portions, was READ AND REJECTED for R4: it "
            "is a methodology page about the three chill models, with zone 0, county 0, plant out 0, "
            "planting 0, month 0, and it explicitly declines per-crop numbers ('varies depending on "
            "variety and species ... contact local nurseries or farm advisors'). Values are NOT "
            "nulled; the T1 re-source comes first.",
            f"Chill.html saved 2026-09-21, 25,630 bytes, sha256 "
            "8ff22b44bc9a586adeff4c2a606d2bfaaf39a775affabf9924bad59f21911a3d. Candidate read from "
            f"Wayback capture 2025-10-10T20:57:39Z, 31,253 bytes, sha256 {CHILL_CANDIDATE_SHA}.",
            deferred_to="PLA-579")})
        F.append({"crop": slug, "entry": finding(
            f"{slug.replace('-', '_')}_chill_anchor_dead_co_sourced", "medium", "open", False,
            f"{co} further region cells on this crop cite the same dead chill URL but are "
            "CO-SOURCED, so each retains at least one other credit. These do not block launch. The "
            "dead credit may be dropped only after confirming, PER CELL, that the surviving source "
            "actually carries the claim; none of those surviving sources has been read yet.",
            "Same evidence as the sole-sourced finding on this crop.",
            deferred_to="PLA-579")})

    F.append({"crop": "lemon", "entry": finding(
        "lemon_tristeza_is_rootstock_independent", "medium", "resolved", False,
        "CONTRADICTED, not merely unsupported, and corrected. The crop said tristeza susceptibility "
        "is 'in some scion combinations'. HS1153/HS402 states: 'Lemons are susceptible to severe "
        "tristeza virus strains regardless of rootstock, and less severe strains when propagated on "
        "Citrus macrophylla (macrophylla) and rough lemon ( C. jambhiri ) rootstocks.' Both the "
        "crop-level note and the sour orange row's traits_seasoned were corrected. SCOPE: only the "
        "tristeza claim is corrected. The note's other claims are NOT verified by this pass. HS402 "
        "ties its certified-tree advice to Florida's budwood program and the new copy generalizes to "
        "certified trees.",
        "HS1153/HS402 read live 2026-09-21 from raw bytes, 158,367 bytes, sha256 "
        "50436e71fe8fb2bcaee7949f83f9fb192cdc3c0cbe875f7b6b74808f5f9459fb.")})

    F.append({"crop": "lemon", "entry": finding(
        "lemon_semi_dwarf_labels_unsourced_nulled", "medium", "resolved", False,
        "size_class NULLED (not set to standard) on trifoliate orange and Carrizo / Swingle "
        "citrumelo, and their container_suitable flags nulled. No cited page supports a size claim: "
        "dwarf 0 and semi-dwarf 0 in all four cited UF/IFAS documents, and the non-dwarf size "
        "vocabulary was checked too (every 'smaller' hit is nursery pots, psyllid nymphs or "
        "zinc-deficient leaves). HS132 does not mention trifoliate, Swingle, Carrizo or sour orange "
        "at all. standard would have been an unread value. RECORDED REASON for the null: the only "
        "T1 that rates these rootstocks, SP248/HS1260, uses a Sm/I/Lg scale the dataset has not "
        "mapped, and it rates Swingle citrumelo I (intermediate), not small. That is UNDETERMINED, "
        "not contradicted. rootstock_selection_basis is deliberately NOT touched: held until Plan E "
        "applies Rule N, because the pre-Rule-N mechanical test would read the remaining {standard} "
        "and return soil_and_pest on a question that is undetermined.",
        "HS402 sha256 50436e71fe8fb2bcaee7949f83f9fb192cdc3c0cbe875f7b6b74808f5f9459fb; HS132 sha256 "
        "5b22371df47e8a27e3b138079b6e8e41e246caeefb31af114febd07c975d183a; HS1260 sha256 "
        "9503b58425e7c94b15f500c88654714f24b9b39ba58cffaf887f4ecf0c2dec27. All read live 2026-09-21.",
        deferred_to="PLA-567")})

    F.append({"crop": "lime", "entry": finding(
        "lime_tristeza_is_rootstock_independent", "medium", "resolved", False,
        "Same defect as lemon's, on the same rootstock, corrected from lime's own anchors. CH092 "
        "states flatly: 'Key limes are susceptible to tristeza virus regardless of rootstock.' CH093 "
        "hedges for Tahiti: 'Tahiti limes may be susceptible to severe tristeza virus strains, "
        "regardless of rootstock.' Each document is kept to its own lime, the hedge is preserved, "
        "and CH093's personal-communication half is deliberately excluded. HS402's flat lemon "
        "phrasing was NOT borrowed. SCOPE: only the tristeza claim is corrected; the note's other "
        "claims (rough lemon, Volkamer, Swingle, the Key lime propagation line) are not verified by "
        "this pass.",
        "CH093 read live 2026-09-21, 160,411 bytes, sha256 "
        "5bbca72512ff1e408787cdd7ae007c369532882659b8cdd008fdf2ce1782c14f. CH092 read live "
        "2026-09-21, 151,716 bytes, sha256 "
        "27c7bc139ab30f6fe73bd68145ffb47e8cc241bf017c9f90b4774f8cba068206.")})

    F.append({"crop": "lime", "entry": finding(
        "lime_semi_dwarf_label_unsourced_nulled", "medium", "resolved", False,
        "size_class NULLED (not standard) on Swingle citrumelo, and its container_suitable nulled. "
        "Neither CH093 nor CH092 makes any size claim: dwarf 0 in both, and neither names Flying "
        "Dragon. CH093's one 'tree size' hit is about PRUNING to keep height at 6 to 8 ft. Same "
        "recorded reason as lemon's: the only T1 rating uses an unmapped Sm/I/Lg scale. Whether a "
        "dwarfing rootstock is available for lime at all is UNDETERMINED and weaker than lemon's: no "
        "T1 document read connects any dwarfing rootstock to lime. rootstock_selection_basis NOT "
        "touched, held for Rule N.",
        "CH093 sha256 5bbca72512ff1e408787cdd7ae007c369532882659b8cdd008fdf2ce1782c14f; CH092 sha256 "
        "27c7bc139ab30f6fe73bd68145ffb47e8cc241bf017c9f90b4774f8cba068206; HS1260 sha256 "
        "9503b58425e7c94b15f500c88654714f24b9b39ba58cffaf887f4ecf0c2dec27.",
        deferred_to="PLA-567")})

    F.append({"crop": "persimmon", "entry": finding(
        "persimmon_rooststock_slug_is_uc_davis_own", "low", "resolved", False,
        "DO NOT 'FIX' THIS URL. persimmon anchors "
        "https://fruitsandnuts.ucdavis.edu/persimmon-scion-rooststock-selection under "
        "ucd_fruitnut, and the three-s spelling 'rooststock' is UC DAVIS'S OWN SLUG, not a "
        "transcription error on our side. Confirmed from a residential Safari save on "
        "2026-09-21: the page's <link rel=\"canonical\"> carries that exact path AND its "
        "<title> reads 'Persimmon Scion & Rooststock Selection | Fruit & Nut Research & "
        "Information Center'. The typo is in the publisher's slug and in their own page title. "
        "Correcting it to 'rootstock' would produce a 404. Recorded because the spelling looks "
        "exactly like an error a later pass would tidy up. SEPARATELY OWED: this anchor is now "
        "IN SCOPE under the widened ucd_fruitnut citable_for, but scope legality is not R4 "
        "compliance. Nobody has read that page against persimmon's actual rootstock claims; that "
        "read is filed as its own ticket.",
        "persimmon.html saved from Safari 2026-09-21, residential connection, 31,727 bytes, "
        "sha256 bcad546ea09e9354de1fd05b7be39a3aa97295d4451983a0b188152b5e06b8d1. A real page: "
        "no Cloudflare challenge, no 404.")})

    return F


# ------------------------------------------------------------------ post-state

def check_post_state(pre, post):
    P, Q = by_slug(pre), by_slug(post)
    # SET before VALUE (PLA-162)
    if set(P) != set(Q):
        raise SystemExit(f"REFUSED: crop set changed: {sorted(set(P) ^ set(Q))}")
    if set(pre) != set(post):
        raise SystemExit("REFUSED: top-level key set changed")

    changed = sorted(s for s in P if P[s] != Q[s])
    if changed != EXPECTED_CHANGED_CROPS:
        raise SystemExit(f"REFUSED: changed crops {changed}, pinned {EXPECTED_CHANGED_CROPS}")

    if post["source_catalog"]["ucd_fruitnut"]["citable_for"] != UCD_CITABLE_FOR_NEW:
        raise SystemExit("REFUSED: citable_for did not take the new text")
    # NOTE: there is deliberately NO separate "exclusion sentence present" guard here. The
    # byte-equality check above already covers it, and the mutation harness proved the extra
    # guard was unreachable as coverage (disabling it left the suite green). Removed rather than
    # shipped as decoration, per the four guards removed on the same grounds in PLA-465. The
    # sentence itself is asserted on the POST state by the suite's happy-path test.
    other = {k: v for k, v in post["source_catalog"].items() if k != "ucd_fruitnut"}
    if other != {k: v for k, v in pre["source_catalog"].items() if k != "ucd_fruitnut"}:
        raise SystemExit("REFUSED: a source_catalog entry other than ucd_fruitnut changed")

    plum = Q["plum"]
    names = [e["name"] for e in plum["rootstock_options"]]
    if names != PLUM_POST_NAMES:
        raise SystemExit(f"REFUSED: post plum rootstock names {names}")
    if row_of(plum, DROP_ROW) is not None:
        raise SystemExit("REFUSED: St. Julien A survived the drop")

    for nm in (MYROBALAN_NEW_NAME, "Marianna 2624", CITATION_ROW["name"]):
        r = row_of(plum, nm)
        if r["sources"] != ["ucd_fruitnut"]:
            raise SystemExit(f"REFUSED: {nm} sources {r['sources']}")
        au = r["anchoring_urls"]
        if set(au) != {"ucd_fruitnut"}:
            raise SystemExit(f"REFUSED: {nm} anchoring keys {sorted(au)}")
        if au["ucd_fruitnut"]["url"] != NEW_PLUM_URL:
            raise SystemExit(f"REFUSED: {nm} url did not repoint")
        if au["ucd_fruitnut"]["verified"] != VERIFIED:
            raise SystemExit(f"REFUSED: {nm} verified date did not move with the url")
        note = au["ucd_fruitnut"].get("note") or ""
        if EXPECTED_PLUM_TITLE not in note:
            raise SystemExit(f"REFUSED: {nm} anchor note omits the expected page title")
        if "GENERIC" not in note:
            raise SystemExit(f"REFUSED: {nm} anchor note omits the generic-path fragility")

    cit = row_of(plum, CITATION_ROW["name"])
    if cit != CITATION_ROW:
        raise SystemExit("REFUSED: the Citation row is not byte-equal to its spec")

    if "ucanr_ext" in plum["varieties"]["sources"]:
        raise SystemExit("REFUSED: plum.varieties still credits ucanr_ext")
    if "ucanr_ext" in plum["varieties"]["anchoring_urls"]:
        raise SystemExit("REFUSED: plum.varieties still anchors ucanr_ext")
    if sorted(plum["varieties"]["sources"]) != ["clemson_hgic", "mu_ext"]:
        raise SystemExit("REFUSED: plum.varieties survivors are not mu_ext + clemson_hgic")

    # the dead plum URL must be gone from every rootstock and varieties cell, but the 48 region
    # cells KEEP it (values are not nulled, the credit is not dropped until the T1 re-source)
    still = _count_url(plum, DEAD_PLUM_URL)
    if still != 48:
        raise SystemExit(f"REFUSED: dead plum URL appears {still} times, expected exactly 48 (regions)")

    nulls = [(c["slug"], e["name"]) for c in post["crops"]
             for e in (c.get("rootstock_options") or []) if e.get("container_suitable") is None]
    if len(nulls) != EXPECTED_NULL_CONTAINER_ROWS:
        raise SystemExit(f"REFUSED: {len(nulls)} null container rows, pinned {EXPECTED_NULL_CONTAINER_ROWS}: {nulls}")

    sizenulls = [(c["slug"], e["name"]) for c in post["crops"]
                 for e in (c.get("rootstock_options") or []) if e.get("size_class") is None]
    if len(sizenulls) != EXPECTED_NULL_SIZE_ROWS:
        raise SystemExit(f"REFUSED: {len(sizenulls)} null size_class rows, pinned {EXPECTED_NULL_SIZE_ROWS}")

    for slug in ("lemon", "lime"):
        if Q[slug]["rootstock_selection_basis"] != P[slug]["rootstock_selection_basis"]:
            raise SystemExit(f"REFUSED: {slug} rootstock_selection_basis moved; it is held for Rule N")
        cn = Q[slug]["container_notes"]
        if cn["container_path"] != "direct" or cn["container_ok"] is not True:
            raise SystemExit(f"REFUSED: {slug} container_path/container_ok moved")

    lso = row_of(Q["lime"], SOUR_ORANGE)
    if "uf_ifas_edis" not in lso["sources"]:
        raise SystemExit("REFUSED: lime sour orange did not gain uf_ifas_edis")
    if lso["anchoring_urls"]["uf_ifas_edis"] != LIME_CH092:
        raise SystemExit("REFUSED: lime CH092 anchor is not the pinned value")

    new_f = 0
    for slug in set(EXPECTED_CHANGED_CROPS):
        a = {f["id"] for f in P[slug]["verification_status"]["open_findings"] if isinstance(f, dict)}
        b = {f["id"] for f in Q[slug]["verification_status"]["open_findings"] if isinstance(f, dict)}
        if not a <= b:
            raise SystemExit(f"REFUSED: {slug} lost an existing finding id")
        new_f += len(b - a)
    if new_f != EXPECTED_NEW_FINDINGS:
        raise SystemExit(f"REFUSED: {new_f} new findings, pinned {EXPECTED_NEW_FINDINGS}")

    blockers = 0
    for c in post["crops"]:
        vs = c["verification_status"]
        live = [f for f in (vs.get("open_findings") or [])
                if isinstance(f, dict) and f.get("blocks_launch") and f.get("status") != "resolved"]
        if live:
            blockers += 1
            if vs.get("launch_ready_core") is not False or vs.get("launch_ready_seasoned") is not False:
                raise SystemExit(f"REFUSED: {c['slug']} has a live blocker but launch_ready is not false")
        if vs.get("status") != P[c["slug"]]["verification_status"].get("status"):
            raise SystemExit(f"REFUSED: {c['slug']} verification_status.status moved; it must not")
    if blockers != EXPECTED_BLOCKERS_AFTER:
        raise SystemExit(f"REFUSED: {blockers} crops carry a live blocker, pinned {EXPECTED_BLOCKERS_AFTER}")

    for slug in LAUNCH_FLIP_CROPS:
        vs = Q[slug]["verification_status"]
        if vs["launch_ready_core"] is not False or vs["launch_ready_seasoned"] is not False:
            raise SystemExit(f"REFUSED: {slug} launch_ready did not flip")


def _count_url(obj, url):
    n = 0

    def walk(o):
        nonlocal n
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "anchoring_urls" and isinstance(v, dict):
                    n += sum(1 for e in v.values() if isinstance(e, dict) and e.get("url") == url)
                elif v is not None:
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                if v is not None:
                    walk(v)

    walk(obj)
    return n


def run(data):
    check_pre_state(data)
    pre = copy.deepcopy(data)
    post = apply(data)
    check_post_state(pre, post)
    return post


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--expect-sha")
    ap.add_argument("--in", dest="inp")
    a = ap.parse_args()

    data, sha = load_canonical(a.inp)
    if a.inp is None and sha != BASE_SHA:
        raise SystemExit(f"REFUSED: canonical is {sha[:8]}, base is {BASE_SHA[:8]}")

    post = run(data)
    out = serialize(post)
    print(f"pre  {sha}")
    print(f"post {sha256_bytes(out)}")

    if a.check:
        print("CHECK OK -- nothing written")
        return
    if a.out:
        with open(a.out, "wb") as f:
            f.write(out)
        print("wrote", a.out, "(COMPACT)")
        return
    if a.expect_sha:
        if a.expect_sha != BASE_SHA:
            raise SystemExit(f"REFUSED: --expect-sha {a.expect_sha[:8]} is not the base")
        with open(CANON, "wb") as f:
            f.write(out)
        print("wrote", CANON, "(COMPACT)")
        return
    print("no action: pass --check, --out or --expect-sha")


if __name__ == "__main__":
    main()
