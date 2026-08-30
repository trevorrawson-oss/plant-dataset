#!/usr/bin/env python3
"""PLA-8 BATCH 13 -- THE SPRING FRUITING SET: four peppers + eggplant. Base ee0f54a3.

54 problems gain `id`, `type` and `control_ladder`; **264 rungs** across `cayenne-pepper` (54),
`habanero` (54), `banana-pepper` (52), `bell-pepper` (52) and `eggplant` (52). Roster laddered
53 -> 58. Ordered per Trevor's ruling 2026-08-30: spring fruiting next, the Companion & Pollinator
override DECLINED, the 2026-08-26 demand ruling stands.

**NO CATALOG MUTATION.** No mint, no widening; `control_methods` and `source_catalog` must come out
byte-for-byte identical.

--------------------------------------------------------------------------------------------------
THE TWIN STRUCTURE: TWO PROSE FAMILIES PLUS A FIVE-CROP HORNWORM TEXT
--------------------------------------------------------------------------------------------------
Measured on the base, the batch's advice prose (the four prevention/organic_treatment fields)
partitions into byte-identical groups: {cayenne, habanero} share 9 problems, {banana, bell} share
8 (plus their ECB pair under two names), and the hornworm advice text is IDENTICAL ON ALL FIVE
CROPS. Per the batch-2 corn precedent, identical prose ships ONE rung text set, and
`check_alignment` pins the correspondence in BOTH directions: identical advice + same id must
carry byte-identical ladders, and byte-identical ladders must sit on identical advice. The near
miss that proves the second direction is real: eggplant's flea-beetle prose differs from
cayenne's by ONE WORD ("outgrow" vs "can outgrow"), so eggplant keeps its own texts.

--------------------------------------------------------------------------------------------------
THE TAXON RULINGS: TWO IDS WHOSE OBVIOUS STRING NAMES THE WRONG ORGANISM
--------------------------------------------------------------------------------------------------
**`bacterial-spot`, NOT `bacterial-leaf-spot`.** All four peppers' "Bacterial leaf spot" is the
Xanthomonas disease jalapeno already carries as `bacterial-spot` (its own cause prose:
"Xanthomonas bacteria that are seed- and debris-borne"). The name-derived id exists on the roster
and is WRONG: cilantro's `bacterial-leaf-spot` is Pseudomonas syringae pv. coriandricola, a
different genus. The family id is reused; the wrong string is refused.

**`southern-bacterial-wilt`, NOT `bacterial-wilt`.** Eggplant's cause prose names Ralstonia
solanacearum, a soilborne bacterium spread in water and on tools. The roster's `bacterial-wilt`
(cucumbers, squash) is Erwinia tracheiphila, carried in cucumber beetles' guts. Different
organism, different vector, different controls; a reuse would assert the beetle-vectored disease
on a crop whose prose describes the soilborne one.

Family reuses verified by organism before pinning: jalapeno's `aphids`/`flea-beetles`/
`pepper-maggot`/`pepper-weevil`/`hornworms`/`mosaic-viruses`/`phytophthora-blight`/`anthracnose`/
`bacterial-spot`; the corns' `european-corn-borer` (bell's single-organism problem AND banana's
combined "European corn borer and corn earworm", the lead-organism convention that shipped
`carrot-rust-fly`); the tomatoes' `blossom-end-rot`; strawberry's `verticillium-wilt` (whose own
prose names eggplant as a host); the roster's `cutworms` and `spider-mites`.

--------------------------------------------------------------------------------------------------
THE READ'S RULINGS
--------------------------------------------------------------------------------------------------
**PRE-PLANT CULTIVATION IS NOT `off_season_tillage`.** The cutworm prose says "lightly cultivate
the soil BEFORE planting to expose overwintering larvae"; the method means a FINISHED bed worked
once AFTER harvest. Cayenne's authoring agent used the key and flagged it; habanero's refused the
identical advice as a gap. The habanero agent was right: the rung was dropped, the advice recorded
as unplaced, and the key is refused on cutworms here. The hornworm ladders DO carry it, because
that prose says "till the soil in fall to destroy overwintering pupae", which is the method's own
worked example.

**WEEVIL WEED HOSTS BELONG TO `weed_host_control`, NOT `garden_sanitation`.** All four peppers'
weevil prose names weedy nightshades and volunteer peppers as carryover hosts. banana/bell placed
that under weed_host_control (the catalog's own distinction: sanitation removes the CROP's debris,
weed_host_control removes OTHER plants hosting the problem); cayenne/habanero had folded it into
their sanitation notes, following the pre-r7 jalapeno exemplar. Aligned to the catalog: all four
weevil ladders carry the weed_host_control rung and the sanitation notes stay on crop scope. The
flea-beetle weeds stay IN sanitation on all five, deliberately: that prose describes overwintering
SHELTER in general litter, not host-relatives.

**TRAP CROPPING IS DIVERT-ONLY ON ALL THREE CARRIERS.** cayenne, habanero and eggplant flea-beetle
prose names a nasturtium trap planting as a lure and stops there, so those rungs route the removal
through the method's cautions and are FORBIDDEN the "this crop's guidance" attribution of a removal
step (the trap-cropping round's contract). banana/bell prose names no trap planting and their
ladders are refused the key.

**NO UNNAMED MATERIAL BECOMES A RUNG.** "A labeled spray/insecticide/fungicide" with no active
ingredient appears on pepper-maggot, pepper-weevil, and eggplant's phomopsis; none became a rung.
Copper lands only where the prose names copper: bacterial-spot on all four peppers, anthracnose on
cayenne/habanero ONLY (banana/bell's anthracnose prose says "a labeled fungicide", unnamed, and
their ladders end without a material). The mosaic, phytophthora, verticillium, southern-blight,
southern-bacterial-wilt, weevil, maggot, cutworm, hornworm and blossom-end-rot ladders carry no
soft_chemical or conventional rung at all, each on its own prose.

**NO TIMING OR ESCAPE KEY IS EARNED.** The flea-beetle "delay planting until soil and air are
warm so plants grow away fast" is transplant-vigor advice: `planting_time_avoidance` (a published
pest window) and `disease_escape_sowing` (a fungal foliar escape) are both refused batch-wide,
along with `pyrethroid` (house) and `bt` on Colorado potato beetle (the prose names the
tenebrionis strain; the catalog's `bt` key means kurstaki and carries caterpillar cautions).

REFUSALS: base SHA mismatch; any crop already laddered; an id off the convention table; either
taxon-refused id anywhere in the batch; a reused family id that no longer resolves on the roster,
or a new id already taken; the alignment correspondence broken in either direction; trap_cropping
outside the three divert carriers, or a divert rung attributing removal to the crop, or missing
its cautions pointer; a weevil ladder without weed_host_control, or weevil sanitation notes
re-absorbing the nightshade weeds; off_season_tillage on cutworms or absent from hornworms; a
material rung on a no-material ladder; copper on banana/bell anthracnose; a forbidden method
anywhere; a note byte-identical to a shipped rung or sharing a 10+ word sentence with one;
unknown method; tier decrease; applies_to incoherence; identical registers; duplicate method in a
ladder; empty ladder; counts off; ANY change to control_methods, source_catalog, or a bystander
crop.

Guard suite:      tools/test_promote_pla8_batch13.py
Mutation harness: tools/mutate_pla8_batch13_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_batch13.py [--apply] [--dry-run]
"""
import argparse, copy, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
STAGING = os.path.join(REPO, "tools", "staging", "pla8_batch13_peppers_eggplant")
BASE_SHA = "ee0f54a35a4dd1eee0da6daa5992c636cc422f25796e46d4649fd3c9fcc07277"

CROPS = ("cayenne-pepper", "habanero", "banana-pepper", "bell-pepper", "eggplant")
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
MATERIAL_TIERS = ("soft_chemical", "conventional")
EXPECTED_PROBLEMS = {"cayenne-pepper": 11, "habanero": 11, "banana-pepper": 11,
                     "bell-pepper": 11, "eggplant": 10}
EXPECTED_RUNGS = {"cayenne-pepper": 54, "habanero": 54, "banana-pepper": 52,
                  "bell-pepper": 52, "eggplant": 52}

# All five crops use the CLASSIC schema; the alignment correspondence is keyed on these four
# advice-bearing fields, because they are what a rung restates.
ADVICE_FIELDS = ("prevention_beginner", "prevention_seasoned",
                 "organic_treatment_beginner", "organic_treatment_seasoned")

ID_CONVENTION = {
    "Aphids": "aphids",
    "Anthracnose": "anthracnose",
    "Anthracnose (ripe fruit rot)": "anthracnose",
    "Bacterial leaf spot": "bacterial-spot",
    "Bacterial wilt": "southern-bacterial-wilt",
    "Blossom-end rot": "blossom-end-rot",
    "Colorado potato beetle": "colorado-potato-beetle",
    "Cutworms": "cutworms",
    "Eggplant lace bug": "eggplant-lace-bug",
    "European corn borer": "european-corn-borer",
    "European corn borer and corn earworm": "european-corn-borer",
    "Flea beetles": "flea-beetles",
    "Hornworms": "hornworms",
    "Mosaic and other viruses": "mosaic-viruses",
    "Pepper maggot": "pepper-maggot",
    "Pepper weevil": "pepper-weevil",
    "Phomopsis blight": "phomopsis-blight",
    "Phytophthora blight": "phytophthora-blight",
    "Southern blight": "southern-blight",
    "Spider mites": "spider-mites",
    "Tobacco and tomato hornworms": "hornworms",
    "Tomato and tobacco hornworms": "hornworms",
    "Verticillium wilt": "verticillium-wilt",
}

# id -> (the id a name-derived pass would reach for, why it is the wrong organism)
TAXON_REFUSED = {
    "bacterial-spot": ("bacterial-leaf-spot",
                       "cilantro's bacterial-leaf-spot is Pseudomonas syringae pv. coriandricola; "
                       "the peppers' disease is Xanthomonas, which jalapeno carries as "
                       "bacterial-spot"),
    "southern-bacterial-wilt": ("bacterial-wilt",
                                "the cucumbers' bacterial-wilt is Erwinia tracheiphila, carried by "
                                "cucumber beetles; eggplant's is Ralstonia solanacearum, soilborne, "
                                "spread in water and on tools"),
}

# Family/roster ids this batch REUSES: each must already resolve on a certified crop in the base.
REUSED_IDS = ("aphids", "flea-beetles", "pepper-maggot", "pepper-weevil", "hornworms",
              "mosaic-viruses", "phytophthora-blight", "anthracnose", "bacterial-spot",
              "european-corn-borer", "blossom-end-rot", "verticillium-wilt", "cutworms",
              "spider-mites")
# New to the roster; each must NOT resolve in the base.
NEW_IDS = ("colorado-potato-beetle", "eggplant-lace-bug", "phomopsis-blight",
           "southern-blight", "southern-bacterial-wilt")

# The three flea-beetle ladders whose prose names a trap planting, all DIVERT-ONLY: the prose is
# a lure with no removal step, so the rung must route removal through the method's cautions and
# must NOT attribute a removal to the crop.
TRAP_OK = (("cayenne-pepper", "flea-beetles"), ("habanero", "flea-beetles"),
           ("eggplant", "flea-beetles"))
ATTRIBUTION = "this crop's guidance"
CAUTIONS_POINTER = "cautions"

# Ladders whose prose states no cure / no home material / names no material: no soft_chemical or
# conventional rung. Copper is EARNED on bacterial-spot (all four peppers) and on cayenne/habanero
# anthracnose, whose prose names it; banana/bell anthracnose prose says only "a labeled
# fungicide", unnamed, so their ladders are in this list.
NO_MATERIAL = tuple(
    [(s, "mosaic-viruses") for s in CROPS[:4]] +
    [(s, "phytophthora-blight") for s in CROPS] +
    [(s, "pepper-weevil") for s in CROPS[:4]] +
    [(s, "pepper-maggot") for s in CROPS[:4]] +
    [(s, "hornworms") for s in CROPS] +
    [("cayenne-pepper", "cutworms"), ("habanero", "cutworms"),
     ("cayenne-pepper", "blossom-end-rot"), ("habanero", "blossom-end-rot"),
     ("banana-pepper", "anthracnose"), ("bell-pepper", "anthracnose"),
     ("banana-pepper", "southern-blight"), ("bell-pepper", "southern-blight"),
     ("eggplant", "verticillium-wilt"), ("eggplant", "southern-bacterial-wilt")]
)

# Methods refused batch-wide, each on a specific ruling.
FORBIDDEN_METHODS = {
    "pyrethroid": "this arc uses pyrethrin where a pyrethroid-class material is earned; here neither is",
    "planting_time_avoidance": ("the flea-beetle delay-planting advice is transplant VIGOR, not a "
                                "published pest window; ruled unplaceable, not a timing rung"),
    "disease_escape_sowing": ("no problem in this batch states a sow-early fungal escape; the "
                              "warm-soil advice is vigor, the exact stretch the mint forbids"),
    "bt": None,  # scoped below: legal on caterpillars, refused on colorado-potato-beetle
}
# bt is legal on the hornworm and ECB ladders (kurstaki caterpillar prose) and REFUSED on
# colorado-potato-beetle: the prose names the tenebrionis strain, a different organism-target,
# and the catalog's bt key means the kurstaki caterpillar spray with caterpillar cautions.
BT_OK_PIDS = ("hornworms", "european-corn-borer")

# off_season_tillage: earned by hornworms (fall tillage of pupae, the method's own example),
# refused on cutworms (the prose's cultivation is PRE-PLANT, a different action).
TILLAGE_REQUIRED = tuple((s, "hornworms") for s in CROPS)
TILLAGE_REFUSED_PIDS = ("cutworms",)

# All four pepper weevil ladders carry the weed rung, and their sanitation notes stay on crop
# scope (the nightshade weeds live in weed_host_control now).
WEEVIL_CROPS = CROPS[:4]

TIER_RANK = {t: i for i, t in enumerate(TIERS)}
BRITISH = ("colour", "flavour", "fertilise", "organise", "sulphur", "centre", "metre",
           "mould", "grey", "labour", "practise", "favour")


def hygiene(s):
    if re.search(r"[—–]", s):
        return "em or en dash"
    if "--" in s:
        return "double hyphen"
    if re.search(r"\b(?:always|never|completely|harmless|guaranteed|totally|eliminates?)\b", s, re.I):
        return "absolute claim"
    if re.search(r"\s°F", s):
        return "spaced degF"
    for w in BRITISH:
        if re.search(rf"\b{w}\b", s, re.I):
            return f"British spelling {w!r}"
    if re.search(r"(?<![.!?]\s)(?<!^)\bPlant\b(?! Pro)", s):
        return "capital Plant mid-sentence"
    if re.search(r"\b(?:is|are)\s+safe\b", s, re.I):
        return "bare safety claim"
    return None


def staged():
    return {s: json.load(open(os.path.join(STAGING, f"out_{s}.json"))) for s in CROPS}


def problems(obj):
    return [(fam, p) for fam in ("pests", "diseases") for p in (obj.get(fam) or [])
            if isinstance(p, dict)]


def rung_count(batch):
    return sum(len(p.get("control_ladder") or []) for s in CROPS for _, p in problems(batch[s]))


def ladder_of(obj, pid):
    for _, p in problems(obj):
        if p.get("id") == pid:
            return [r["method"] for r in p.get("control_ladder") or []], p
    return None, None


def roster_ids(data):
    return {p["id"] for c in data["crops"] for _, p in problems(c) if p.get("id")}


def advice_key(p):
    return json.dumps([p.get(f) for f in ADVICE_FIELDS], ensure_ascii=False)


def ladder_key(p):
    return json.dumps([(r["method"], r["note_beginner"], r["note_seasoned"])
                       for r in p.get("control_ladder") or []], ensure_ascii=False)


def check_alignment(by, batch):
    """Identical advice prose + same shipped id <-> identical ladder, both directions, pairwise
    over every batch problem. One direction catches a needless fork on shared prose (the batch-2
    propagation contract); the other catches a ladder copied across prose that differs (the
    cucumber defect), including the one-word eggplant flea-beetle near-twin."""
    rows = []
    for slug in CROPS:
        canon = problems(by[slug])
        for idx, (_, p) in enumerate(problems(batch[slug])):
            rows.append((slug, p.get("id"), advice_key(canon[idx][1]), ladder_key(p)))
    for i, (s1, id1, a1, l1) in enumerate(rows):
        for s2, id2, a2, l2 in rows[i + 1:]:
            if id1 == id2 and a1 == a2 and l1 != l2:
                return (f"{s1}/{id1} and {s2}/{id2} carry byte-identical advice prose but "
                        f"different ladders; identical prose ships one text set")
            if l1 == l2 and a1 != a2:
                return (f"{s1}/{id1} and {s2}/{id2} share a byte-identical ladder but their "
                        f"advice prose differs, so one crop is being given the other's source")
    return None


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text or "") if len(s.strip()) > 25]


def shipped_notes(data):
    whole, sent = {}, {}
    for c in data["crops"]:
        for _, p in problems(c):
            for r in p.get("control_ladder") or []:
                for k in ("note_beginner", "note_seasoned"):
                    v = r.get(k)
                    if not v:
                        continue
                    whole.setdefault(v, f"{c.get('slug')}/{p.get('id')}/{r['method']}")
                    for s in sentences(v):
                        sent.setdefault(s, f"{c.get('slug')}/{p.get('id')}/{r['method']}")
    return whole, sent


def check_no_shipped_echo(batch, data):
    """jalapeno is the certified sibling the authoring agents read as an exemplar, which is
    exactly how a find-and-replaced ladder arrives looking authored. Two real echoes were caught
    and rewritten at the read; this keeps them out."""
    whole, sent = shipped_notes(data)
    for slug in CROPS:
        for _, p in problems(batch[slug]):
            for r in p.get("control_ladder") or []:
                where = f"{slug}/{p.get('id')}/{r['method']}"
                for k in ("note_beginner", "note_seasoned"):
                    n = r.get(k) or ""
                    if n in whole:
                        return f"{where}: {k} is byte-identical to the shipped {whole[n]}"
                    for s in sentences(n):
                        if s in sent and len(s.split()) >= 10:
                            return (f"{where}: {k} shares a {len(s.split())}-word sentence with "
                                    f"the shipped {sent[s]}: {s!r}")
    return None


def check_read_fixes(batch, by, data):
    for slug in CROPS:
        canon = problems(by[slug])
        for idx, (_, p) in enumerate(problems(batch[slug])):
            name = (canon[idx][1].get("name") if idx < len(canon) else None) or ""
            want = ID_CONVENTION.get(name)
            if want is None:
                return f"{slug}: problem {name!r} is not in the id-convention table"
            if p.get("id") != want:
                return (f"{slug}: problem {name!r} has id {p.get('id')!r}, but the convention "
                        f"ships {want!r}; ids are join keys and are never re-derived from the "
                        f"name")

    # THE TAXON REFUSALS, both directions.
    staged_ids = {p["id"] for slug in CROPS for _, p in problems(batch[slug])}
    for right, (wrong, why) in TAXON_REFUSED.items():
        if right not in staged_ids:
            return f"the taxon ruling requires id {right!r}, which no problem in this batch carries"
        if wrong in staged_ids:
            return (f"a problem carries {wrong!r}, which is the WRONG ORGANISM: {why}")

    # Reused family ids must resolve on the roster; new ids must not.
    base_ids = roster_ids(data)
    for pid in REUSED_IDS:
        if pid in staged_ids and pid not in base_ids:
            return (f"{pid!r} is declared a REUSE but resolves nowhere on the roster, so this "
                    f"would be a mint wearing a reuse's name")
    for pid in NEW_IDS:
        if pid in base_ids:
            return f"{pid!r} is already on the roster; it is listed as new to this base"

    # TRAP: divert-only on exactly the three carriers.
    for slug in CROPS:
        for _, p in problems(batch[slug]):
            pid = p.get("id")
            lad = [r["method"] for r in p.get("control_ladder") or []]
            if "trap_cropping" in lad and (slug, pid) not in TRAP_OK:
                return (f"{slug}/{pid} carries trap_cropping, which only the three flea-beetle "
                        f"ladders whose prose names a trap planting earn")
    for slug, pid in TRAP_OK:
        ms, p = ladder_of(batch[slug], pid)
        if ms is None or "trap_cropping" not in ms:
            return (f"{slug}/{pid} lost its trap_cropping rung; its prose names a nasturtium "
                    f"trap planting")
        for r in p["control_ladder"]:
            if r["method"] != "trap_cropping":
                continue
            blob = (r["note_beginner"] + " " + r["note_seasoned"]).lower()
            if ATTRIBUTION in blob:
                return (f"{slug}/{pid}: the trap rung uses {ATTRIBUTION!r}, crediting the crop "
                        f"with a removal step its prose stops short of; the prose is a lure only")
            if CAUTIONS_POINTER not in blob:
                return (f"{slug}/{pid}: the trap rung never points at the method's cautions, "
                        f"which carry the removal deadline the prose omits")

    # NO MATERIAL where the prose earns none.
    cm = data["control_methods"]
    for slug, pid in NO_MATERIAL:
        ms, _p = ladder_of(batch[slug], pid)
        if ms is None:
            return f"{slug} has no {pid} problem"
        for m in ms:
            if m in cm and cm[m]["tier"] in MATERIAL_TIERS:
                return (f"{slug}/{pid} carries {m!r} ({cm[m]['tier']}), but its prose names no "
                        f"such material or states there is no cure")

    # Forbidden methods, plus the scoped bt ruling.
    for slug in CROPS:
        for _, p in problems(batch[slug]):
            pid = p.get("id")
            lad = [r["method"] for r in p.get("control_ladder") or []]
            for m, why in FORBIDDEN_METHODS.items():
                if m == "bt":
                    continue
                if m in lad:
                    return f"{slug}/{pid} carries {m!r}: {why}"
            if "bt" in lad and pid not in BT_OK_PIDS:
                return (f"{slug}/{pid} carries bt, but the catalog's bt key means the kurstaki "
                        f"caterpillar spray; the CPB prose names the tenebrionis strain, a "
                        f"different target, and no other problem here earns it")
            if "off_season_tillage" in lad and pid in TILLAGE_REFUSED_PIDS:
                return (f"{slug}/{pid} carries off_season_tillage, but the cutworm prose's "
                        f"cultivation is PRE-PLANT; the method means a finished bed worked after "
                        f"harvest, and the advice is recorded as unplaced")
    for slug, pid in TILLAGE_REQUIRED:
        ms, _p = ladder_of(batch[slug], pid)
        if ms is None or "off_season_tillage" not in ms:
            return (f"{slug}/{pid} lost its off_season_tillage rung; the hornworm prose states "
                    f"fall tillage of pupae, the method's own worked example")

    # WEEVIL: the weed rung is carried and sanitation stays on crop scope.
    for slug in WEEVIL_CROPS:
        ms, p = ladder_of(batch[slug], "pepper-weevil")
        if ms is None:
            return f"{slug} has no pepper-weevil problem"
        if "weed_host_control" not in ms:
            return (f"{slug}/pepper-weevil has no weed_host_control rung; its prose names weedy "
                    f"nightshades and volunteers as carryover hosts, which is that method's "
                    f"action, not sanitation's")
        for r in p["control_ladder"]:
            if r["method"] == "garden_sanitation":
                blob = (r["note_beginner"] + " " + r["note_seasoned"]).lower()
                if "nightshade" in blob:
                    return (f"{slug}/pepper-weevil: the sanitation note re-absorbed the "
                            f"nightshade weeds, which moved to weed_host_control at the read")
    return None


def validate_batch(batch, cm):
    from control_ladder_gate import TYPE_TARGETS
    for crop in CROPS:
        n_prob = 0
        for _, p in problems(batch[crop]):
            n_prob += 1
            if not p.get("id") or not p.get("type"):
                return f"{crop}: a problem is missing id or type"
            lad = p.get("control_ladder")
            if lad is None:
                return f"{crop}/{p.get('id')}: no control_ladder"
            if not lad:
                return f"{crop}/{p.get('id')}: control_ladder is EMPTY"
            tiers, seen = [], set()
            for i, r in enumerate(lad):
                m = r.get("method")
                if m not in cm:
                    return f"{crop}/{p.get('id')}#{i}: method {m!r} not in catalog"
                if m in seen:
                    return f"{crop}/{p.get('id')}#{i}: method {m!r} appears twice in one ladder"
                seen.add(m)
                targets = TYPE_TARGETS.get(p.get("type")) or set()
                if "any" not in cm[m]["applies_to"] and not (set(cm[m]["applies_to"]) & targets):
                    return (f"{crop}/{p.get('id')}#{i}: {m!r} applies_to "
                            f"{sorted(cm[m]['applies_to'])} cannot reach type {p.get('type')!r}")
                for k in ("note_beginner", "note_seasoned"):
                    if not str(r.get(k) or "").strip():
                        return f"{crop}/{p.get('id')}#{i}: {k} missing or empty"
                if r["note_beginner"] == r["note_seasoned"]:
                    return f"{crop}/{p.get('id')}#{i}: registers are identical"
                for k in ("note_beginner", "note_seasoned"):
                    bad = hygiene(r[k])
                    if bad:
                        return f"{crop}/{p.get('id')}#{i}: {k} fails copy hygiene ({bad})"
                tiers.append(TIER_RANK[cm[m]["tier"]])
            if tiers != sorted(tiers):
                return f"{crop}/{p.get('id')}: tiers decrease {tiers}"
        if n_prob != EXPECTED_PROBLEMS[crop]:
            return f"{crop}: {n_prob} problems, expected {EXPECTED_PROBLEMS[crop]}"
    return None


def check(data):
    cm = data["control_methods"]
    by = {c.get("slug"): c for c in data["crops"]}
    for slug in CROPS:
        if slug not in by:
            return f"no crop {slug!r} in canonical"
        for _, p in problems(by[slug]):
            if "control_ladder" in p:
                return f"{slug} is already laddered; re-laddering changes shipped ids"

    batch = staged()
    for slug in CROPS:
        a, b = len(problems(batch[slug])), len(problems(by[slug]))
        if a != b:
            return f"{slug}: staged {a} problems, canonical {b}"
    for problem in (check_read_fixes(batch, by, data), check_alignment(by, batch),
                    check_no_shipped_echo(batch, data)):
        if problem:
            return problem
    problem = validate_batch(batch, cm)
    if problem:
        return problem
    for slug in CROPS:
        n = sum(len(p.get("control_ladder") or []) for _, p in problems(batch[slug]))
        if n != EXPECTED_RUNGS[slug]:
            return f"{slug}: {n} rungs, expected {EXPECTED_RUNGS[slug]}"
    if rung_count(batch) != sum(EXPECTED_RUNGS.values()):
        return f"rung count {rung_count(batch)}, expected {sum(EXPECTED_RUNGS.values())}"
    return None


def serialize(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def snapshot(data):
    dump = lambda o: json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return {"crops": {c.get("slug"): dump(c) for c in data["crops"]},
            "methods": dump(data["control_methods"]),
            "sources": dump(data["source_catalog"])}


def apply_to(data):
    batch = staged()
    by = {c.get("slug"): c for c in data["crops"]}
    minted = reused = 0
    for slug in CROPS:
        crop = by[slug]
        for fam in ("pests", "diseases"):
            adds = [p for p in (batch[slug].get(fam) or []) if isinstance(p, dict)]
            for i, add in enumerate(adds):
                tgt = crop[fam][i]
                if isinstance(tgt.get("id"), str) and tgt["id"]:
                    reused += 1
                else:
                    tgt["id"] = add["id"]
                    minted += 1
                tgt["type"] = add["type"]
                tgt["control_ladder"] = copy.deepcopy(add["control_ladder"])
    return minted, reused, rung_count(batch)


def verify_post(pre, data):
    by = {c.get("slug"): c for c in data["crops"]}
    cm = data["control_methods"]
    post = snapshot(data)

    # SUBSTANTIVE INVARIANTS FIRST.
    for slug in CROPS:
        for _, p in problems(by[slug]):
            pid = p.get("id")
            lad = [r["method"] for r in p.get("control_ladder") or []]
            if not lad:
                return f"post: {slug}/{pid}: no ladder after promote"
            if "trap_cropping" in lad and (slug, pid) not in TRAP_OK:
                return f"post: {slug}/{pid} shipped trap_cropping unearned"
            if "bt" in lad and pid not in BT_OK_PIDS:
                return f"post: {slug}/{pid} shipped bt outside the caterpillar ladders"
            if "off_season_tillage" in lad and pid in TILLAGE_REFUSED_PIDS:
                return f"post: {slug}/{pid} shipped the pre-plant cultivation as tillage"
            for m in ("pyrethroid", "planting_time_avoidance", "disease_escape_sowing"):
                if m in lad:
                    return f"post: {slug}/{pid} shipped forbidden {m!r}"
    for slug, pid in NO_MATERIAL:
        ms, _p = ladder_of(by[slug], pid)
        if ms is None:
            return f"post: {slug} lost its {pid} problem"
        for m in ms:
            if m in cm and cm[m]["tier"] in MATERIAL_TIERS:
                return f"post: {slug}/{pid} shipped {m!r}, which its prose rules out"
    shipped = {p["id"] for slug in CROPS for _, p in problems(by[slug])}
    for right, (wrong, _why) in TAXON_REFUSED.items():
        if right not in shipped:
            return f"post: the taxon-ruled id {right!r} did not ship"
        if wrong in shipped:
            return f"post: {wrong!r} shipped, the wrong organism"
    for slug in WEEVIL_CROPS:
        ms, _p = ladder_of(by[slug], "pepper-weevil")
        if ms is None or "weed_host_control" not in ms:
            return f"post: {slug}/pepper-weevil lost its weed_host_control rung"

    # Blast radius, set-equality before value comparison (PLA-162).
    if set(post["crops"]) != set(pre["crops"]):
        return "post: the crop set changed"
    for slug, before in pre["crops"].items():
        if slug in CROPS:
            continue
        if post["crops"][slug] != before:
            return f"post: crop {slug!r} changed, and this promote touches only {CROPS}"
    if post["methods"] != pre["methods"]:
        return "post: control_methods changed, and this promote mints and widens NOTHING"
    if post["sources"] != pre["sources"]:
        return "post: source_catalog changed, and this promote touches no source"
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("canonical", nargs="?", default=CANONICAL)
    ap.add_argument("--expect-sha", default=BASE_SHA)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    # CHAIN-REPLAY CONTRACT (see promote_fixture._from_chain).
    ap.add_argument("--canonical", dest="canonical_flag", default=None)
    a = ap.parse_args()
    a.canonical = a.canonical_flag or a.canonical

    raw = open(a.canonical, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != a.expect_sha:
        print(f"ABORT: base SHA mismatch\n  expected {a.expect_sha}\n  found    {sha}", file=sys.stderr)
        return 1
    data = json.loads(raw.decode("utf-8"))
    problem = check(data)
    if problem:
        print("ABORT: " + problem, file=sys.stderr)
        return 1

    pre = snapshot(data)
    minted, reused, rungs = apply_to(data)
    problem = verify_post(pre, data)
    if problem:
        print("ABORT (post): " + problem, file=sys.stderr)
        return 1

    print("PLA-8 BATCH 13 -- THE SPRING FRUITING SET: four peppers + eggplant")
    print(f"  crops        : {', '.join(CROPS)}")
    print(f"  problems     : {sum(EXPECTED_PROBLEMS.values())}   rungs: {rungs}")
    print(f"  ids          : {minted} minted on these crops ({len(NEW_IDS)} new to the roster, "
          f"{len(REUSED_IDS)} reusing family/roster strings)")
    print(f"  catalog      : UNTOUCHED -- no mint, no widening, no method edited")
    print(f"  taxon rulings: bacterial-spot NOT bacterial-leaf-spot (Xanthomonas vs Pseudomonas);")
    print(f"                 southern-bacterial-wilt NOT bacterial-wilt (Ralstonia vs Erwinia)")
    print(f"  alignment    : identical advice prose ships one text set, both directions pinned")
    print(f"  blast radius : 5 crops; methods 0; sources 0; bystanders 0")
    out = serialize(data)
    new_sha = hashlib.sha256(out).hexdigest()
    if a.dry_run or not a.apply:
        print(f"DRY RUN -- would write {len(out)} bytes, sha {new_sha}")
        return 0
    open(a.canonical, "wb").write(out)
    print(f"wrote {len(out)} bytes\nnew canonical SHA: {new_sha}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
