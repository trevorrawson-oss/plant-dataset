#!/usr/bin/env python3
"""PLA-8 BATCH 14 -- okra, tomatillo, and the three melons. Base 4c5a79d3 (the mancozeb mint).

48 problems gain `id`, `type` and `control_ladder`; **232 rungs** across `okra` (34), `tomatillo`
(36), `cantaloupe` (57), `honeydew-melon` (50) and `watermelon` (55). Roster laddered 58 -> 63.

**NO CATALOG MUTATION HERE** -- the round's mint (`mancozeb`, 60 -> 61) is its own promote,
sequenced FIRST so the key existed in the authoring brief. This promote's base premise is that the
mint has landed: a base without `mancozeb` predates it, and the two conventional rungs below would
fail as unknown methods.

--------------------------------------------------------------------------------------------------
THE CONVENTIONAL SCOPING: EXACTLY TWO LADDERS, AND ON THOSE TWO BOTH MATERIALS ARE REQUIRED
--------------------------------------------------------------------------------------------------
cantaloupe's Alternaria leaf blight and watermelon's Anthracnose each say "treat at the first
spots with a labeled fungicide such as chlorothalonil or mancozeb". Those two ladders carry BOTH
rungs (dropping one would silently un-name a material the crop names), and no other problem in the
batch carries either -- every other spray mention is "a labeled fungicide", unnamed, which earns
no material rung. Copper appears once: tomatillo's early blight names "copper sprays preventively
if pressure is high", so that ladder alone carries `copper_fungicide`.

--------------------------------------------------------------------------------------------------
THE BACTERIAL-WILT REUSE IS THE MIRROR OF EGGPLANT'S REFUSAL, AND THE PREMISE IS PINNED
--------------------------------------------------------------------------------------------------
Batch 13 REFUSED `bacterial-wilt` for eggplant because that roster string is Erwinia tracheiphila
and eggplant's disease is Ralstonia. The melons REUSE it because theirs IS the Erwinia: both
cause-prose records name "Erwinia tracheiphila" carried by cucumber beetles.
`check_bacterial_wilt_premise` asserts that in canonical, so the reuse never silently outlives
its evidence. (watermelon carries no bacterial-wilt problem at all, which its own prose explains:
it rides the wilt out better than cucumber or muskmelon.)

--------------------------------------------------------------------------------------------------
THE MELON TWIN STRUCTURE, AND THE CROP-NEUTRALITY RULE THE ALIGNMENT ADDED
--------------------------------------------------------------------------------------------------
Six problems carry byte-identical advice prose on all three melons (aphids, spider mites, squash
bug, powdery mildew, downy mildew, gummy stem blight) and ship ONE text set each, pinned both
directions as in batch 13. The subtlety this batch adds: the melons' SYMPTOM prose is crop-named
where their advice prose is shared, so a donor set may carry only claims backed on every member
and NO single crop's name -- `check_melon_neutrality` refuses a propagated rung that says
cantaloupe, honeydew or watermelon. (Each read-checked claim in the shipped sets is backed by all
three records: the one-generation-South squash bug line, powdery mildew's fruit-size/sugar/
sunscald costs, downy mildew's 10-to-14-day leaf kill, gummy stem blight's Didymella.) The
per-crop problems (cucumber beetles, fusarium, squash vine borer, the two wilts) differ in prose
and keep their own ladders.

--------------------------------------------------------------------------------------------------
THE READ'S OTHER RULINGS
--------------------------------------------------------------------------------------------------
**okra's stink bugs earn the trap rung WITH attribution.** "A cowpea trap planting concentrates
them for removal" states the removal purpose -- the turnip precedent -- so the rung says "this
crop's guidance" AND points at the method's cautions for the timing the prose omits. It is the
batch's only trap carrier.

**`stink-bugs`, not `stink-bugs-leaf-footed-bugs`.** The combined name takes the lead organism's
id, the convention that shipped `cabbageworms`, `carrot-rust-fly` and `european-corn-borer`.

**off_season_tillage is earned twice and bounded.** tomatillo's hornworm prose states fall
tillage of pupae (the method's own example); the melons' vine-borer prose states late-winter
tillage of the old bed against overwintering pupae, which is still off-season work of a finished
bed. Pre-plant cultivation (tomatillo's cutworms) stays refused, the batch-13 ruling: its agent
refused the key unprompted and the advice is recorded as unplaced.

REFUSALS: base SHA mismatch; a base without mancozeb; any crop already laddered; an id off the
convention table; a reused id that no longer resolves or a new id already taken; the
bacterial-wilt premise gone; the alignment correspondence broken either way; a crop-named
propagated melon rung; a conventional rung outside the two earning ladders, or either material
missing from them; copper outside tomatillo's early blight; trap_cropping outside okra's stink
bugs, or that rung losing its attribution or cautions pointer; off_season_tillage outside its two
earners; a material on a no-material ladder; a forbidden method; a shipped-rung echo; unknown
method; tier decrease; applies_to incoherence; identical registers; duplicate method; empty
ladder; counts off; ANY change to control_methods, source_catalog, or a bystander crop.

Guard suite:      tools/test_promote_pla8_batch14.py
Mutation harness: tools/mutate_pla8_batch14_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_batch14.py [--apply] [--dry-run]
"""
import argparse, copy, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
STAGING = os.path.join(REPO, "tools", "staging", "pla8_batch14_okra_tomatillo_melons")
BASE_SHA = "4c5a79d34a435117adee9723242d1846a04045eda739226e6b3419892644c739"

CROPS = ("okra", "tomatillo", "cantaloupe", "honeydew-melon", "watermelon")
MELONS = ("cantaloupe", "honeydew-melon", "watermelon")
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
MATERIAL_TIERS = ("soft_chemical", "conventional")
EXPECTED_PROBLEMS = {"okra": 8, "tomatillo": 9, "cantaloupe": 11, "honeydew-melon": 10,
                     "watermelon": 10}
EXPECTED_RUNGS = {"okra": 34, "tomatillo": 36, "cantaloupe": 57, "honeydew-melon": 50,
                  "watermelon": 55}

ADVICE_FIELDS = ("prevention_beginner", "prevention_seasoned",
                 "organic_treatment_beginner", "organic_treatment_seasoned")

ID_CONVENTION = {
    "Alternaria leaf blight": "alternaria-leaf-blight",
    "Anthracnose": "anthracnose",
    "Aphids": "aphids",
    "Bacterial wilt": "bacterial-wilt",
    "Corn earworm": "corn-earworm",
    "Cucumber beetles": "cucumber-beetles",
    "Cutworms": "cutworms",
    "Downy mildew": "downy-mildew",
    "Early blight": "early-blight",
    "Flea beetles": "flea-beetles",
    "Fusarium wilt": "fusarium-wilt",
    "Gummy stem blight": "gummy-stem-blight",
    "Mosaic and other viruses": "mosaic-viruses",
    "Powdery mildew": "powdery-mildew",
    "Root and stem rots": "root-and-stem-rots",
    "Root-knot nematode": "root-knot-nematode",
    "Southern blight": "southern-blight",
    "Spider mites": "spider-mites",
    "Squash bug": "squash-bug",
    "Squash vine borer": "squash-vine-borer",
    "Stink bugs and leaf-footed bugs": "stink-bugs",
    "Three-lined potato beetle": "three-lined-potato-beetle",
    "Tomato hornworm": "tomato-hornworm",
}

REUSED_IDS = ("aphids", "corn-earworm", "flea-beetles", "fusarium-wilt", "southern-blight",
              "powdery-mildew", "root-knot-nematode", "tomato-hornworm", "cutworms",
              "early-blight", "mosaic-viruses", "cucumber-beetles", "spider-mites",
              "squash-bug", "squash-vine-borer", "bacterial-wilt", "anthracnose",
              "downy-mildew")
NEW_IDS = ("stink-bugs", "three-lined-potato-beetle", "root-and-stem-rots",
           "gummy-stem-blight", "alternaria-leaf-blight")

# The two ladders whose prose names BOTH conventional fungicides; each must carry both rungs,
# and no other ladder in the batch may carry either.
CONVENTIONAL_ON = (("cantaloupe", "alternaria-leaf-blight"), ("watermelon", "anthracnose"))
CONVENTIONALS = ("chlorothalonil", "mancozeb")
# The one ladder whose prose names copper.
COPPER_ON = (("tomatillo", "early-blight"),)

# okra's stink bugs: the trap rung with the removal purpose STATED, so attribution is REQUIRED,
# and the timing routed through the cautions because the prose stops short of a deadline.
TRAP_OK = (("okra", "stink-bugs"),)
ATTRIBUTION = "this crop's guidance"
CAUTIONS_POINTER = "cautions"

TILLAGE_OK_PIDS = ("tomato-hornworm", "squash-vine-borer")

FORBIDDEN_METHODS = {
    "pyrethroid": "no problem in this batch earns a conventional insecticide",
    "planting_time_avoidance": "the vigor advice on okra and tomatillo flea beetles is not a "
                               "published pest window; ruled unplaceable in batch 13 and again "
                               "here by both agents",
    "disease_escape_sowing": "no problem in this batch states a sow-early fungal escape; "
                             "watermelon's late-plantings-hit-hard observation is not a "
                             "recommendation",
}

# Ladders whose prose earns no soft_chemical or conventional rung.
NO_MATERIAL = (
    ("okra", "fusarium-wilt"), ("okra", "southern-blight"), ("okra", "root-knot-nematode"),
    ("okra", "flea-beetles"),
    ("tomatillo", "mosaic-viruses"), ("tomatillo", "root-and-stem-rots"),
    ("cantaloupe", "cucumber-beetles"), ("honeydew-melon", "cucumber-beetles"),
    ("watermelon", "cucumber-beetles"),
    ("cantaloupe", "squash-vine-borer"), ("honeydew-melon", "squash-vine-borer"),
    ("watermelon", "squash-vine-borer"),
    ("cantaloupe", "bacterial-wilt"), ("honeydew-melon", "bacterial-wilt"),
    ("cantaloupe", "fusarium-wilt"), ("honeydew-melon", "fusarium-wilt"),
    ("watermelon", "fusarium-wilt"),
    ("cantaloupe", "downy-mildew"), ("honeydew-melon", "downy-mildew"),
    ("watermelon", "downy-mildew"),
    ("cantaloupe", "gummy-stem-blight"), ("honeydew-melon", "gummy-stem-blight"),
    ("watermelon", "gummy-stem-blight"),
)

# The six problems whose advice prose is byte-identical on all three melons and whose shipped
# text sets are therefore ONE set each, crop-neutral by rule.
MELON_SHARED_PIDS = ("aphids", "spider-mites", "squash-bug", "powdery-mildew", "downy-mildew",
                     "gummy-stem-blight")
MELON_NAMES = ("cantaloupe", "honeydew", "watermelon")

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
    """Identical advice + same id <-> identical ladder, both directions, pairwise (batch 13)."""
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


def check_melon_neutrality(batch):
    """A propagated melon set may not name a single crop: the advice prose is shared but the
    symptom prose is crop-named, so a crop-specific claim in a shared rung is one member's
    source speaking for the other two."""
    for slug in MELONS:
        for _, p in problems(batch[slug]):
            if p.get("id") not in MELON_SHARED_PIDS:
                continue
            for r in p.get("control_ladder") or []:
                blob = (r["note_beginner"] + " " + r["note_seasoned"]).lower()
                for w in MELON_NAMES:
                    if w in blob:
                        return (f"{slug}/{p['id']}/{r['method']}: a shared melon rung names "
                                f"{w!r}; the six propagated sets must stay crop-neutral")
    return None


def check_bacterial_wilt_premise(by):
    """The reuse premise: the melons' bacterial wilt is the cucumbers' Erwinia, stated by their
    own cause prose. If that prose ever stops naming Erwinia, the reuse has outlived its
    evidence and must be re-argued, not assumed."""
    for slug in ("cantaloupe", "honeydew-melon"):
        for _, p in problems(by[slug]):
            if p.get("name") == "Bacterial wilt":
                blob = " ".join(str(p.get(f) or "") for f in
                                ("cause_beginner", "cause_seasoned")).lower()
                if "erwinia" not in blob:
                    return (f"{slug}'s bacterial wilt cause prose no longer names Erwinia, so "
                            f"reusing the cucumbers' id would assert an organism the record no "
                            f"longer claims")
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

    staged_ids = {p["id"] for slug in CROPS for _, p in problems(batch[slug])}
    base_ids = roster_ids(data)
    for pid in REUSED_IDS:
        if pid in staged_ids and pid not in base_ids:
            return (f"{pid!r} is declared a REUSE but resolves nowhere on the roster, so this "
                    f"would be a mint wearing a reuse's name")
    for pid in NEW_IDS:
        if pid in base_ids:
            return f"{pid!r} is already on the roster; it is listed as new to this base"

    # CONVENTIONAL scoping: both materials on both earning ladders, neither anywhere else.
    for slug, pid in CONVENTIONAL_ON:
        ms, _p = ladder_of(batch[slug], pid)
        if ms is None:
            return f"{slug} has no {pid} problem"
        for m in CONVENTIONALS:
            if m not in ms:
                return (f"{slug}/{pid} lost its {m} rung; the prose names both materials, and "
                        f"shipping one silently un-names the other")
    for slug in CROPS:
        for _, p in problems(batch[slug]):
            pid = p.get("id")
            lad = [r["method"] for r in p.get("control_ladder") or []]
            for m in CONVENTIONALS:
                if m in lad and (slug, pid) not in CONVENTIONAL_ON:
                    return (f"{slug}/{pid} carries {m!r}, but only the two ladders whose prose "
                            f"names both materials earn a conventional rung")
            if "copper_fungicide" in lad and (slug, pid) not in COPPER_ON:
                return (f"{slug}/{pid} carries copper, which only tomatillo's early blight "
                        f"prose names in this batch")
            if "trap_cropping" in lad and (slug, pid) not in TRAP_OK:
                return (f"{slug}/{pid} carries trap_cropping, which only okra's stink bugs earn "
                        f"in this batch")
            if "off_season_tillage" in lad and pid not in TILLAGE_OK_PIDS:
                return (f"{slug}/{pid} carries off_season_tillage, earned only by the hornworm "
                        f"fall tillage and the vine borer's late-winter bed work; pre-plant "
                        f"cultivation stays refused")
            for m, why in FORBIDDEN_METHODS.items():
                if m in lad:
                    return f"{slug}/{pid} carries {m!r}: {why}"

    # The trap rung: attribution REQUIRED (removal purpose stated) plus the cautions pointer.
    for slug, pid in TRAP_OK:
        ms, p = ladder_of(batch[slug], pid)
        if ms is None or "trap_cropping" not in ms:
            return f"{slug}/{pid} lost its trap_cropping rung; its prose names the cowpea trap"
        for r in p["control_ladder"]:
            if r["method"] != "trap_cropping":
                continue
            blob = (r["note_beginner"] + " " + r["note_seasoned"]).lower()
            if ATTRIBUTION not in blob:
                return (f"{slug}/{pid}: the trap rung does not attribute the removal purpose, "
                        f"which the prose STATES ('concentrates them for removal'); the "
                        f"strongest thing it could say goes unsaid")
            if CAUTIONS_POINTER not in blob:
                return (f"{slug}/{pid}: the trap rung never points at the method's cautions, "
                        f"which carry the removal deadline the prose omits")

    for slug, pid in NO_MATERIAL:
        ms, _p = ladder_of(batch[slug], pid)
        if ms is None:
            return f"{slug} has no {pid} problem"
        cm = data["control_methods"]
        for m in ms:
            if m in cm and cm[m]["tier"] in MATERIAL_TIERS:
                return (f"{slug}/{pid} carries {m!r} ({cm[m]['tier']}), but its prose names no "
                        f"such material or states there is no cure")
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
    if "mancozeb" not in cm:
        return ("mancozeb is NOT in this base, so it predates the mint; watermelon and "
                "cantaloupe carry mancozeb rungs that would fail as unknown methods. Re-pin "
                "BASE_SHA onto the mint's output or later")
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
    for problem in (check_bacterial_wilt_premise(by), check_read_fixes(batch, by, data),
                    check_alignment(by, batch), check_melon_neutrality(batch),
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

    for slug in CROPS:
        for _, p in problems(by[slug]):
            pid = p.get("id")
            lad = [r["method"] for r in p.get("control_ladder") or []]
            if not lad:
                return f"post: {slug}/{pid}: no ladder after promote"
            for m in CONVENTIONALS:
                if m in lad and (slug, pid) not in CONVENTIONAL_ON:
                    return f"post: {slug}/{pid} shipped {m!r} outside the two earning ladders"
            if "copper_fungicide" in lad and (slug, pid) not in COPPER_ON:
                return f"post: {slug}/{pid} shipped copper unearned"
            if "trap_cropping" in lad and (slug, pid) not in TRAP_OK:
                return f"post: {slug}/{pid} shipped trap_cropping unearned"
            if "off_season_tillage" in lad and pid not in TILLAGE_OK_PIDS:
                return f"post: {slug}/{pid} shipped tillage outside its two earners"
            for m in FORBIDDEN_METHODS:
                if m in lad:
                    return f"post: {slug}/{pid} shipped forbidden {m!r}"
    for slug, pid in CONVENTIONAL_ON:
        ms, _p = ladder_of(by[slug], pid)
        if ms is None:
            return f"post: {slug} lost its {pid} problem"
        for m in CONVENTIONALS:
            if m not in ms:
                return f"post: {slug}/{pid} shipped without its {m!r} rung"
    for slug, pid in NO_MATERIAL:
        ms, _p = ladder_of(by[slug], pid)
        if ms is None:
            return f"post: {slug} lost its {pid} problem"
        for m in ms:
            if m in cm and cm[m]["tier"] in MATERIAL_TIERS:
                return f"post: {slug}/{pid} shipped {m!r}, which its prose rules out"
    shipped = {p["id"] for slug in CROPS for _, p in problems(by[slug])}
    for pid in NEW_IDS:
        if pid not in shipped:
            return f"post: new id {pid!r} did not ship"

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

    print("PLA-8 BATCH 14 -- okra, tomatillo, and the three melons")
    print(f"  crops        : {', '.join(CROPS)}")
    print(f"  problems     : {sum(EXPECTED_PROBLEMS.values())}   rungs: {rungs}")
    print(f"  ids          : {minted} minted on these crops ({len(NEW_IDS)} new to the roster)")
    print(f"  catalog      : UNTOUCHED here; the round's mancozeb mint is its own promote")
    print(f"  conventionals: chlorothalonil + mancozeb on exactly {CONVENTIONAL_ON}, both "
          f"required, nowhere else")
    print(f"  reuse premise: melon bacterial-wilt IS the cucumbers' Erwinia, asserted in canonical")
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
