#!/usr/bin/env python3
"""PLA-8 BATCH 12 -- FALL FINISHERS, the last batch of the fall block. Base 1e4d0c06.

22 problems gain `id`, `type` and `control_ladder`; **105 rungs** across `broad-beans-fava` (33),
`brussels-sprouts` (49) and `parsley` (23). Roster laddered 50 -> 53.

**NO CATALOG MUTATION.** No mint, no widening, nothing. `control_methods` must come out of this
promote byte-for-byte identical, and `verify_post` asserts that over the whole dict rather than
per-key -- the strictest blast radius of the arc so far, and the right one for a batch whose only
job is to place existing keys.

--------------------------------------------------------------------------------------------------
THE BASE IS BATCH 11'S OUTPUT, NOT LIVE CANONICAL
--------------------------------------------------------------------------------------------------
parsley REUSES `parsleyworm`, the id batch 11 mints for dill. If this batch were built on
`be444e25` that reuse would be a second, independent MINT of the same problem on a sibling crop,
which is how a family splits its join keys at birth. Batch 11 is verified but uncommitted, so its
output is reachable only by replay: `promote_fixture.CHAIN` carries 1e4d0c06 -> 96cbc68c via
`promote_pla8_batch11.py`, hash-verified at every level. **Batch 12 must promote AFTER batch 11.**

--------------------------------------------------------------------------------------------------
THE TAXON RULINGS: TWO IDS THAT LOOK LIKE REUSES AND ARE NOT
--------------------------------------------------------------------------------------------------
Two of fava's problems carry names whose obvious id is already on the roster, and both would have
asserted the WRONG ORGANISM. A problem id is a permanent join key, so these are pinned as REFUSALS
in both directions -- the right string required, the wrong one named and rejected.

**`pea-and-bean-weevil`, NOT `pea-weevil`.** The shipped `pea-weevil` (sugar-snap-peas, snow-peas)
is *Bruchus pisorum*, whose own cause text says "host range is peas alone" -- a bruchid whose larvae
develop inside the seed. Fava's is *Sitona lineatus*: leaf-margin notching by adults, larvae on the
root nodules. Different insect, different damage, different control. `bean-weevil` is refused too,
because that name is the dried bean weevil (*Acanthoscelides obtectus*), which a later bean crop
may need.

**`broad-bean-rust`, NOT `bean-rust`.** The shipped `bean-rust` (green-beans-bush, pole-beans,
dry-bean) is *Uromyces appendiculatus* on *Phaseolus*. Fava's is *U. viciae-fabae* on *Vicia*:
different species, different host, no cross-infection. The roster already mints per-pathogen rust
ids (`asparagus-rust`, `fig-rust`, `common-rust`, `white-rust`, `cedar-apple-rust`).

**`root-rots-damping-off` IS reused**, over the also-plausible `bean-root-rots`. Fava is *Vicia*,
in the same tribe as *Pisum* and not a *Phaseolus* bean, and its treatment prose is a near-verbatim
twin of snow-peas' ("no rescue for rotted seed or collapsed seedlings; replant... into warmer,
better-drained conditions once the soil has dried"). The authoring agent and the orchestrator
reached this independently and disagreed; the prose twin settled it.

**`black-bean-aphid` is minted rather than folded into generic `aphids`**, because the record is
wholly *Aphis fabae* and its control (pinch the growing tip once the lower pods have set) applies
to nothing else. The roster already carries five species-scoped aphid ids.

--------------------------------------------------------------------------------------------------
THE READ'S RULINGS
--------------------------------------------------------------------------------------------------
**NO FUNGICIDE ON THREE LADDERS, AND THE PROSE IS WHY.** fava's chocolate spot and broad bean rust
both say outright that no fungicides are available to home gardeners; parsley's septoria says there
is "no reliable spray cure once it is established". All three ladders end cultural. broad-bean-rust
is the pointed one: shipped `bean-rust` on dry-bean CARRIES sulfur, so this is a deliberate
divergence from a sibling id, driven by this crop's own prose.

**A SECOND MECHANISM WAS STRIPPED OUT OF A TIMING RUNG.** fava's bean seed fly is a ONE-RUNG
ladder (`planting_time_avoidance`), and the authored note also carried "let coarse residue or manure
break down before sowing, since the flies are drawn to decaying organic matter". That is a
different mechanism (remove the attractant) wearing a timing rung's clothes. Removed and recorded
as unplaced; guarded here so it cannot come back.

**THE TIP PINCH IS `garden_sanitation`, NOT `handpick`.** fava's aphid control removes the infested
shoot and carries it off, which is that method's stated best_use ("pulling the first affected leaves
or fruit during the season"). `handpick` means catching free-living insects.

**PARSLEY'S RELOCATION STAYS UNPLACED, DELIBERATELY.** "Relocate the larvae to a sacrificial plant"
is conservation: the caterpillars end alive, on a host grown partly for the butterflies. It is one
of the six documented exclusions in the trap-cropping round, and `trap_cropping` (which ends in
DESTROYING the trap) reverses it. No note in this batch may mention it.

**BRUSSELS SPROUTS TAKES ITS TRAP CROP, BECAUSE THE PARALLEL ROUND LANDED FIRST.** Its harlequin
bug prose names the classic action WITH the destroy timing ("deploy an early trap crop of cleome or
mustard to divert overwintering adults, then destroy it before the main crop is set out"), so it
earns the rung the moment `trap_cropping` exists. It now does: the mint and its backfill landed at
`86c5396a` and `96cbc68c`. The rung was authored to the contract the round's own session wrote
(`staging/.../BRUSSELS_TRAP_CROPPING_CONTRACT.md`): group DESTROY_STATED, so it restates the removal
and may carry the "this crop's guidance" attribution that DIVERT_ONLY rungs are denied; it names
cleome or mustard and nothing else; it points at the method's `cautions` for the deadline rather
than restating it; and it sits at index 1, the end of the cultural run, matching all ten rungs that
round shipped. **Landing that round first kept its backfill at 10 rather than 11 and shipped this
crop correct the first time.**

Every OTHER problem in the batch still refuses the key, and parsley's parsleyworm is the one where a
rung would actively reverse the advice: relocating larvae to a spare plant is CONSERVATION, they end
alive, and this method's meaning ends in destroying the trap with the pest on it.

REFUSALS: base SHA mismatch; any crop already laddered; an id off the convention table; either
taxon-refused id; parsley's `parsleyworm` diverging from dill's; a fungicide on the three
no-fungicide ladders; `handpick` on the aphid; the residue clause back in the seed-fly note;
`trap_cropping` on any problem but brussels-sprouts/harlequin-bug, or missing from that one, or off
index 1; `pyrethroid` anywhere; "trap crop"/"sacrificial"/"relocate"/"diatomaceous" in a note other
than that one rung; a base PREDATING the trap_cropping mint; `planting_time_avoidance` outside fava's two insect problems; the bt rung losing its hedge or
its non-selectivity warning; an unknown method; a tier decrease; applies_to incoherence; identical
registers; an empty ladder; counts off; a rung note byte-identical to a shipped one, or sharing a
sentence of 10+ words with one; ANY change to control_methods, source_catalog, or a bystander crop.

Guard suite:      tools/test_promote_pla8_batch12.py
Mutation harness: tools/mutate_pla8_batch12_suite.py (PLA-215)

Usage: python3 tools/promote_pla8_batch12.py [--apply] [--dry-run]
"""
import argparse, copy, hashlib, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
CANONICAL = os.path.join(REPO, "crops_data_final.json")
STAGING = os.path.join(REPO, "tools", "staging", "pla8_batch12_fall_finishers")
BASE_SHA = "1e4d0c06ad28ed28642f64a3ae15b537bb7d14367b73280489ebde3befd311ae"

CROPS = ("broad-beans-fava", "brussels-sprouts", "parsley")
TIERS = ("cultural", "physical", "biological", "soft_chemical", "conventional")
MATERIAL_TIERS = ("soft_chemical", "conventional")
EXPECTED_PROBLEMS = {"broad-beans-fava": 7, "brussels-sprouts": 9, "parsley": 6}
EXPECTED_RUNGS = {"broad-beans-fava": 33, "brussels-sprouts": 49, "parsley": 23}

# All three crops use the CLASSIC schema. Kept as an explicit expectation rather than an assumption:
# batch 11 was the first mixed-schema batch and a crop silently arriving in the newer shape would
# make prose_signature all-None for it and the twins check vacuous.
PROSE_FIELDS = ("name", "severity", "sources",
                "symptoms_beginner", "symptoms_seasoned", "cause_beginner", "cause_seasoned",
                "organic_treatment_beginner", "organic_treatment_seasoned",
                "prevention_beginner", "prevention_seasoned",
                "identification_beginner", "identification_seasoned",
                "management_beginner", "management_seasoned")
ADVICE_FIELDS = ("organic_treatment_beginner", "organic_treatment_seasoned",
                 "prevention_beginner", "prevention_seasoned",
                 "management_beginner", "management_seasoned")
CLASSIC_SCHEMA_CROPS = CROPS

ID_CONVENTION = {
    "Alternaria leaf spot": "alternaria-leaf-spot",
    "Aphids": "aphids",
    "Black bean aphid": "black-bean-aphid",
    "Black rot": "black-rot",
    "Bean seed fly": "bean-seed-fly",
    "Broad bean rust": "broad-bean-rust",
    "Cabbage aphids": "cabbage-aphids",
    "Cabbage root maggot": "cabbage-root-maggot",
    "Cabbageworms and cabbage loopers": "cabbageworms",
    "Carrot rust fly and carrot weevil": "carrot-rust-fly",
    "Chocolate spot": "chocolate-spot",
    "Clubroot": "clubroot",
    "Crown and root rot": "crown-and-root-rot",
    "Damping-off and seedling rot": "damping-off",
    "Downy mildew": "downy-mildew",
    "Flea beetles": "flea-beetles",
    "Harlequin bug": "harlequin-bug",
    "Parsleyworm (black swallowtail caterpillar)": "parsleyworm",
    "Pea and bean weevil": "pea-and-bean-weevil",
    "Root rots and seed decay": "root-rots-damping-off",
    "Septoria leaf spot": "septoria-leaf-spot",
}
# New to the base. `parsleyworm` is NOT here: batch 11 mints it for dill, which is why this batch
# sits on batch 11's output. If it ever appears in this tuple, the base is wrong.
NEW_IDS = ("black-bean-aphid", "bean-seed-fly", "broad-bean-rust", "chocolate-spot",
           "crown-and-root-rot", "pea-and-bean-weevil")

# id -> (the id a name-derived pass would reach for, why it is the wrong organism)
TAXON_REFUSED = {
    "pea-and-bean-weevil": ("pea-weevil",
                            "Bruchus pisorum, host range peas alone, larvae inside the seed; "
                            "fava's is Sitona lineatus, notching adults and root-nodule larvae"),
    "broad-bean-rust": ("bean-rust",
                        "Uromyces appendiculatus on Phaseolus; fava's is U. viciae-fabae on Vicia"),
}
# The cross-batch join. parsley must carry the SAME string dill received in batch 11.
PARSLEYWORM = "parsleyworm"
PARSLEYWORM_SIBLING = "dill"

# Ladders whose prose states no home fungicide exists, or none that cures. No material rung.
NO_MATERIAL = (("broad-beans-fava", "chocolate-spot"),
               ("broad-beans-fava", "broad-bean-rust"),
               ("broad-beans-fava", "downy-mildew"),
               ("brussels-sprouts", "black-rot"),
               ("parsley", "septoria-leaf-spot"))
# `handpick` means catching free-living insects on a scouting walk. Only these qualify here.
HANDPICK_OK = ("cabbageworms", "harlequin-bug", "parsleyworm")
# The three problems whose prose actually RECOMMENDS shifting the sowing, rather than merely
# describing when the pest is active. A risk description is not a recommendation (batch 10's
# ruling, which dropped this key from four cabbage-root-maggot ladders); nothing else may carry it.
#   fava/black-bean-aphid  "sow early so the crop is well grown and podding before the spring
#                           aphid flights peak"
#   fava/bean-seed-fly     "waiting for the ground to warm before sowing where the fly is a known
#                           problem is the practical control"
#   parsley/carrot-rust-fly "delay sowing past the first fly generation where it is severe" /
#                           "time sowings around the fly's generations"
TIMING_OK = (("broad-beans-fava", "black-bean-aphid"), ("broad-beans-fava", "bean-seed-fly"),
             ("parsley", "carrot-rust-fly"))
# The stripped second mechanism. Removing the attractant is not a timing lever.
SEED_FLY_BANNED = ("manure", "residue", "compost")
# The bt rung on a butterfly host: both registers must hedge AND state the non-selectivity.
BT_HEDGES = ("rarely", "seldom")
BT_NONSELECTIVE = "caterpillars as a group"
# A shared sentence this long is an echo of one specific shipped crop, not house phrasing. Measured
# 2026-08-28: the only sentences this batch shares with the base are "Go easy on nitrogen
# fertilizer." (5 words, 9x in base) and "Water the soil rather than the leaves." (7 words, 6x).
ECHO_MIN_WORDS = 10
NOTE_BANNED = ("trap crop", "sacrificial", "relocate", "diatomaceous")
# The one rung entitled to trap-crop vocabulary. The ban exists to keep parsley's CONSERVATION
# relocation from being written up as a control; applying it to a legitimate trap_cropping note
# would be a scope error, so exempt that rung by (slug, problem, method) rather than by word.
NOTE_BAN_EXEMPT = (("brussels-sprouts", "harlequin-bug", "trap_cropping"),)
# The single problem whose prose earns a trap_cropping rung, and where it belongs: index 1, the end
# of the cultural run, matching the ten rungs the parallel round shipped.
TRAP_OK = ("brussels-sprouts", "harlequin-bug")
TRAP_INDEX = 1


def staged():
    return {s: json.load(open(os.path.join(STAGING, f"out_{s}.json"))) for s in CROPS}


def staged_digests():
    return {s: hashlib.sha256(open(os.path.join(STAGING, f"out_{s}.json"), "rb").read()).hexdigest()
            for s in CROPS}


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


def prose_signature(crop):
    return [tuple(json.dumps(p.get(f), sort_keys=True) for f in PROSE_FIELDS)
            for _, p in problems(crop)]


def ladder_signature(obj):
    """Keyed by problem id, not position (batch 10's fix)."""
    return json.dumps({p["id"]: [(r["method"], r["note_beginner"], r["note_seasoned"])
                                 for r in p["control_ladder"]]
                       for _, p in problems(obj)}, sort_keys=True)


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text or "") if len(s.strip()) > 25]


def shipped_notes(data):
    """Every rung note already in the base, and every sentence in them.

    Reads with .get(): 53 rungs across broccoli, celery, artichoke, asparagus and microgreens-mix
    carry no `note_seasoned` at all, and nothing gates the field. Indexing would crash here on data
    that is merely old, not malformed.
    """
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


def check_schema_coverage(by):
    """PROSE_FIELDS must reach each crop's ADVICE-bearing prose, not merely its shared fields."""
    for slug in CROPS:
        seen = set()
        for _, p in problems(by[slug]):
            seen |= set(p.keys())
        own_advice = seen & set(ADVICE_FIELDS)
        if not own_advice:
            return f"{slug}: no advice-bearing prose field found; the record shape is unexpected"
        if not (own_advice & set(PROSE_FIELDS)):
            return (f"{slug}: PROSE_FIELDS reaches none of its advice-bearing fields "
                    f"({sorted(own_advice)}), so the twins check would compare only names and causes")
        if slug in CLASSIC_SCHEMA_CROPS and "organic_treatment_seasoned" not in seen:
            return (f"{slug} was expected to use the classic symptoms_/organic_treatment_/"
                    f"prevention_ schema and does not; re-check PROSE_FIELDS before trusting twins")
    return None


def check_not_twins(by, batch):
    problem = check_schema_coverage(by)
    if problem:
        return problem
    for i in range(len(CROPS)):
        for j in range(i + 1, len(CROPS)):
            a, b = CROPS[i], CROPS[j]
            if prose_signature(by[a]) == prose_signature(by[b]):
                return f"{a} and {b} are byte-identical in canonical, a TRUE TWIN"
    dg = staged_digests()
    for i in range(len(CROPS)):
        for j in range(i + 1, len(CROPS)):
            a, b = CROPS[i], CROPS[j]
            if dg[a] == dg[b]:
                return f"the staged files for {a} and {b} are byte-identical, so one was copied"
    # Compare each rung's notes against notes from OTHER rungs only. A rung whose own two registers
    # are identical is validate_batch's business, and it says so in clearer words; catching it here
    # first would mask that guard behind this one.
    seen = {}
    for slug in CROPS:
        for _, p in problems(batch[slug]):
            for r in p.get("control_ladder") or []:
                where = f"{slug}/{p.get('id')}/{r['method']}"
                mine = [r.get(k) or "" for k in ("note_beginner", "note_seasoned")]
                for n in mine:
                    if n in seen:
                        return f"{where}: note is byte-identical to {seen[n]}, within this batch"
                for n in mine:
                    seen[n] = where
    return None


def check_no_shipped_echo(batch, data):
    """brussels-sprouts is the SIXTH brassica and parsley the third umbellifer authored this week.

    The failure this catches is a sibling's ladder copied and find-and-replaced, which reads as
    authored work and is how a template carries a claim onto a crop that never made it.
    """
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
                        if s in sent and len(s.split()) >= ECHO_MIN_WORDS:
                            return (f"{where}: {k} shares a {len(s.split())}-word sentence with the "
                                    f"shipped {sent[s]}, which is an echo, not house phrasing: {s!r}")
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
                return (f"{slug}: problem {name!r} has id {p.get('id')!r}, but the convention ships "
                        f"{want!r}; ids are join keys and are never re-derived from the name")

    # THE TAXON REFUSALS, in both directions: the right string present, the wrong one absent.
    staged_ids = {p["id"] for slug in CROPS for _, p in problems(batch[slug])}
    for right, (wrong, why) in TAXON_REFUSED.items():
        if right not in staged_ids:
            return f"the taxon ruling requires id {right!r}, which no problem in this batch carries"
        if wrong in staged_ids:
            return (f"a problem carries {wrong!r}, which is the WRONG ORGANISM: {why}. The roster's "
                    f"{wrong!r} belongs to other crops and reusing it here asserts their pathogen")

    # THE CROSS-BATCH JOIN. parsley reuses the string batch 11 minted for dill.
    sibling = None
    for c in data["crops"]:
        if c.get("slug") == PARSLEYWORM_SIBLING:
            sibling = {p["id"] for _, p in problems(c) if p.get("id")}
    if sibling is None:
        return f"no crop {PARSLEYWORM_SIBLING!r} in the base"
    if PARSLEYWORM not in sibling:
        return (f"{PARSLEYWORM_SIBLING} does not carry {PARSLEYWORM!r} in this base, so batch 12 is "
                f"sitting on the wrong canonical: it must follow batch 11, which mints that id")
    ms, _ = ladder_of(batch["parsley"], PARSLEYWORM)
    if ms is None:
        return (f"parsley does not carry {PARSLEYWORM!r}; a second, divergent id for the same "
                f"problem is exactly the split this batch's base exists to prevent")

    # NO MATERIAL where the prose says none is available or none cures.
    cm = data["control_methods"]
    for slug, pid in NO_MATERIAL:
        ms, _ = ladder_of(batch[slug], pid)
        if ms is None:
            return f"{slug} has no {pid} problem"
        for m in ms:
            if m in cm and cm[m]["tier"] in MATERIAL_TIERS:
                return (f"{slug}/{pid} carries {m!r} ({cm[m]['tier']}), but its prose states no home "
                        f"fungicide is available or that none cures once established")

    # The tip pinch is sanitation, not handpicking.
    ms, _ = ladder_of(batch["broad-beans-fava"], "black-bean-aphid")
    if "garden_sanitation" not in ms:
        return ("broad-beans-fava/black-bean-aphid has no garden_sanitation rung; the tip pinch is "
                "this crop's primary control and that is where it lives")

    # The stripped second mechanism must not return to the timing rung.
    ms, p = ladder_of(batch["broad-beans-fava"], "bean-seed-fly")
    if ms is None:
        return "broad-beans-fava has no bean-seed-fly problem"
    blob = " ".join((r.get("note_beginner") or "") + " " + (r.get("note_seasoned") or "")
                    for r in p["control_ladder"]).lower()
    for word in SEED_FLY_BANNED:
        if word in blob:
            return (f"broad-beans-fava/bean-seed-fly: a note mentions {word!r}. Letting residue break "
                    f"down before sowing removes the ATTRACTANT; this rung is a timing lever, and "
                    f"folding a second mechanism into its note smuggles an unplaceable control")

    # The bt rung on a butterfly host.
    ms, p = ladder_of(batch["parsley"], PARSLEYWORM)
    if "bt" in ms:
        for r in p["control_ladder"]:
            if r["method"] != "bt":
                continue
            for k in ("note_beginner", "note_seasoned"):
                low = (r.get(k) or "").lower()
                if not any(h in low for h in BT_HEDGES):
                    return (f"parsley/{PARSLEYWORM}: the bt {k} lost its hedge. This crop's own prose "
                            f"de-recommends bt, and an unhedged rung reads as the step after "
                            f"hand-picking")
                if BT_NONSELECTIVE not in low:
                    return (f"parsley/{PARSLEYWORM}: the bt {k} no longer states that the material "
                            f"acts on caterpillars as a group; parsley is a swallowtail host and "
                            f"that is the safety-bearing half of the rung")

    # Batch-wide standing refusals.
    for slug in CROPS:
        for _, p in problems(batch[slug]):
            pid = p.get("id")
            lad = [r["method"] for r in p.get("control_ladder") or []]
            if "planting_time_avoidance" in lad and (slug, pid) not in TIMING_OK:
                return (f"{slug}/{pid} carries planting_time_avoidance, but only {TIMING_OK} have "
                        f"prose recommending the shift; a risk description is not a recommendation")
            if "handpick" in lad and pid not in HANDPICK_OK:
                return (f"{slug}/{pid} carries handpick, whose meaning is catching free-living "
                        f"insects; removing affected tissue is garden_sanitation")
            if "pyrethroid" in lad:
                return f"{slug}/{pid} carries the synthetic pyrethroid; this batch uses pyrethrin"
            # SCOPED, not banned. Exactly ONE problem in this batch earns a trap_cropping rung:
            # brussels-sprouts/harlequin-bug, whose prose names cleome or mustard AND carries the
            # destroy step ("destroy it before the main crop is set out"). Everything else is a
            # refusal, and parsley's parsleyworm is the one that would actively reverse the advice:
            # relocating larvae to a spare plant is CONSERVATION, they end alive, and this method's
            # meaning ends in destroying the trap with the pest on it.
            if "trap_cropping" in lad and (slug, pid) != TRAP_OK:
                return (f"{slug}/{pid} carries trap_cropping, which only {TRAP_OK} earns in this "
                        f"batch; parsley's relocation is conservation and reversing it is harmful")
            for r in p.get("control_ladder") or []:
                low = ((r.get("note_beginner") or "") + " " + (r.get("note_seasoned") or "")).lower()
                if (slug, pid, r.get("method")) in NOTE_BAN_EXEMPT:
                    continue
                for word in NOTE_BANNED:
                    if word in low:
                        return (f"{slug}/{pid}: a note mentions {word!r}. parsley's relocation is "
                                f"CONSERVATION (the larvae end alive) and is a documented exclusion "
                                f"from the trap-cropping round; it stays unplaced")
    return None


def validate_batch(batch, cm):
    from control_ladder_gate import TYPE_TARGETS
    order = {t: i for i, t in enumerate(TIERS)}
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
                tiers.append(order[cm[m]["tier"]])
            if tiers != sorted(tiers):
                return f"{crop}/{p.get('id')}: tiers decrease {tiers}"
        if n_prob != EXPECTED_PROBLEMS[crop]:
            return f"{crop}: {n_prob} problems, expected {EXPECTED_PROBLEMS[crop]}"
    return None


def check_base_premises(data):
    """This batch mints and widens NOTHING, so the catalog premise is the base's own shape."""
    cm = data.get("control_methods")
    if not isinstance(cm, dict) or not cm:
        return "control_methods is missing or empty"
    # INVERTED 2026-08-28, when the parallel round landed (be444e25 -> 86c5396a -> 96cbc68c).
    # Before that this refused a base CONTAINING trap_cropping, because the batch carried no rung
    # for it and shipping brussels-sprouts without one would have been silently wrong. Now the key
    # exists and brussels-sprouts carries the rung its prose earns, so the premise is the reverse:
    # a base WITHOUT the key means this promote is pointed at a canonical predating the mint, and
    # the rung would fail the ladder gate as an unknown method.
    if "trap_cropping" not in cm:
        return ("trap_cropping is NOT in this base, so it predates the mint. brussels-sprouts now "
                "carries a trap_cropping rung and it would fail as an unknown method; re-pin "
                "BASE_SHA onto the trap_cropping backfill's output or later")
    ids = {p["id"] for c in data["crops"] for _, p in problems(c) if p.get("id")}
    for pid in NEW_IDS:
        if pid in ids:
            return f"{pid!r} is already on the roster; it is listed as new to this base"
    return None


def check(data):
    cm = data["control_methods"]
    by = {c.get("slug"): c for c in data["crops"]}

    problem = check_base_premises(data)
    if problem:
        return problem
    for slug in CROPS:
        if slug not in by:
            return f"no crop {slug!r} in canonical"
        for _, p in problems(by[slug]):
            if "control_ladder" in p:
                return f"{slug} is already laddered; re-laddering changes shipped ids"

    batch = staged()
    for problem in (check_not_twins(by, batch), check_read_fixes(batch, by, data),
                    check_no_shipped_echo(batch, data)):
        if problem:
            return problem
    for slug in CROPS:
        a, b = len(problems(batch[slug])), len(problems(by[slug]))
        if a != b:
            return f"{slug}: staged {a} problems, canonical {b}"
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
            "methods": {k: dump(v) for k, v in data["control_methods"].items()},
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
    post = snapshot(data)

    # SUBSTANTIVE INVARIANTS FIRST.
    for slug in CROPS:
        for _, p in problems(by[slug]):
            pid = p.get("id")
            lad = [r["method"] for r in p.get("control_ladder") or []]
            if not lad:
                return f"post: {slug}/{pid}: no ladder after promote"
            if "trap_cropping" in lad and (slug, pid) != TRAP_OK:
                return (f"post: {slug}/{pid} shipped trap_cropping, which only {TRAP_OK} earns; "
                        f"on parsley's parsleyworm it would reverse a conservation instruction")
            if "pyrethroid" in lad:
                return f"post: {slug}/{pid} shipped the synthetic pyrethroid"
            if "handpick" in lad and pid not in HANDPICK_OK:
                return f"post: {slug}/{pid} shipped handpick on a tissue-removal target"
            if "planting_time_avoidance" in lad and (slug, pid) not in TIMING_OK:
                return f"post: {slug}/{pid} shipped an unearned timing rung"
            for r in p["control_ladder"]:
                if (slug, pid, r.get("method")) in NOTE_BAN_EXEMPT:
                    continue
                low = ((r.get("note_beginner") or "") + " " + (r.get("note_seasoned") or "")).lower()
                for word in NOTE_BANNED:
                    if word in low:
                        return f"post: {slug}/{pid}: a note mentions {word!r}"
    cm = data["control_methods"]
    for slug, pid in NO_MATERIAL:
        ms, _ = ladder_of(by[slug], pid)
        if ms is None:
            return f"post: {slug} lost its {pid} problem"
        for m in ms:
            if m in cm and cm[m]["tier"] in MATERIAL_TIERS:
                return f"post: {slug}/{pid} shipped {m!r}, which its prose rules out"
    for right, (wrong, _why) in TAXON_REFUSED.items():
        shipped = {p["id"] for slug in CROPS for _, p in problems(by[slug])}
        if right not in shipped:
            return f"post: the taxon-ruled id {right!r} is not on the roster"
        if wrong in {p["id"] for _, p in problems(by["broad-beans-fava"])}:
            return f"post: broad-beans-fava shipped {wrong!r}, the wrong organism"
    ms, _ = ladder_of(by["parsley"], PARSLEYWORM)
    if ms is None:
        return f"post: parsley did not ship {PARSLEYWORM!r}, dill's id"
    ms, _ = ladder_of(by[TRAP_OK[0]], TRAP_OK[1])
    if ms is None or "trap_cropping" not in ms:
        return (f"post: {TRAP_OK[0]}/{TRAP_OK[1]} lost its trap_cropping rung; its prose names "
                f"cleome or mustard AND the destroy step, so the rung is what the round landed for")
    if ms.index("trap_cropping") != TRAP_INDEX:
        return (f"post: {TRAP_OK[0]}/{TRAP_OK[1]} carries trap_cropping at index "
                f"{ms.index('trap_cropping')}, not {TRAP_INDEX}; it belongs at the END of the "
                f"cultural run, matching the ten rungs the parallel round shipped")

    # Blast radius, set-equality before value comparison (PLA-162).
    if set(post["crops"]) != set(pre["crops"]):
        return "post: the crop set changed"
    if set(post["methods"]) != set(pre["methods"]):
        return "post: control_methods gained or lost a key; this promote mints and widens NOTHING"
    for slug, before in pre["crops"].items():
        if slug in CROPS:
            continue
        if post["crops"][slug] != before:
            return f"post: crop {slug!r} changed, and this promote touches only {CROPS}"
    # STRICTER THAN ITS SIBLINGS: no method may change AT ALL, so this compares the whole dict
    # rather than skipping a widened key.
    for key, before in pre["methods"].items():
        if post["methods"][key] != before:
            return f"post: method {key!r} changed, and this promote mutates no catalog entry"
    if post["sources"] != pre["sources"]:
        return "post: source_catalog changed, and this promote touches no source"

    for i in range(len(CROPS)):
        for j in range(i + 1, len(CROPS)):
            if ladder_signature(by[CROPS[i]]) == ladder_signature(by[CROPS[j]]):
                return f"post: {CROPS[i]} and {CROPS[j]} carry identical ladder CONTENT"
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

    print("PLA-8 BATCH 12 -- FALL FINISHERS (fall block, batch 5 of 5)")
    print(f"  crops        : {', '.join(CROPS)}")
    print(f"  problems     : {sum(EXPECTED_PROBLEMS.values())}   rungs: {rungs}")
    print(f"  ids          : {minted} minted, {reused} reused ({len(NEW_IDS)} new to the roster)")
    print(f"  catalog      : UNTOUCHED -- no mint, no widening, no method edited")
    print(f"  taxon rulings: pea-and-bean-weevil NOT pea-weevil (Sitona vs Bruchus);")
    print(f"                 broad-bean-rust NOT bean-rust (U. viciae-fabae vs U. appendiculatus)")
    print(f"  cross-batch  : parsley reuses dill's {PARSLEYWORM!r} from batch 11")
    print(f"  blast radius : 3 crops; methods 0; sources 0; bystanders 0")
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
