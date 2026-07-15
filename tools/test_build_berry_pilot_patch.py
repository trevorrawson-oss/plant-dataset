#!/usr/bin/env python3
"""Unit test for build_berry_pilot_patch -- op emission against the LIVE canonical + the real
staged inputs (/private/tmp/strawberry_varieties.json, /private/tmp/hero_backfill.json), plus
synthetic-fixture edge cases (source_set skip vs emit, em-dash rejection, clobber refusal).

Run from repo root: python3 tools/test_build_berry_pilot_patch.py
"""
import copy
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_berry_pilot_patch import (
    CANON, STRAWBERRY_VARIETIES, HERO_BACKFILL,
    build_patch, build_strawberry_ops, build_hero_ops,
)

fails = []


def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)


def check_raises(name, fn):
    try:
        fn()
        check(name, False)
    except AssertionError:
        check(name, True)


# ---------------------------------------------------------------------------
# 1. Real-batch test: against the live canonical + the actual staged inputs.
# ---------------------------------------------------------------------------
raw = open(CANON, "rb").read()
sha = hashlib.sha256(raw).hexdigest()
data = json.loads(raw)
staged = json.load(open(STRAWBERRY_VARIETIES, encoding="utf-8"))
hero_rows = json.load(open(HERO_BACKFILL, encoding="utf-8"))

patch, source_set_op = build_patch(data, staged, hero_rows, sha)

check("base_sha matches the live canonical", patch["base_sha"] == sha)

expected_op_count = 2 + 1 + (1 if source_set_op == "emitted" else 0) + 33
check(f"op count == {expected_op_count} (strawberry ops + 33 hero adds)",
      len(patch["patches"]) == expected_op_count)

hero_ops = [o for o in patch["patches"] if o["json_path"].endswith(".hero_description")]
check("exactly 33 hero_description ops", len(hero_ops) == 33)
check("every hero_description value is dash-free",
      all("—" not in o["value"] for o in hero_ops))

archetype_op = next(o for o in patch["patches"] if o["json_path"].endswith(".variety_archetype"))
check("variety_archetype add == 'berry'", archetype_op["op"] == "add" and archetype_op["value"] == "berry")
group_op = next(o for o in patch["patches"] if o["json_path"].endswith(".berry_group"))
check("berry_group add == 'strawberry'", group_op["op"] == "add" and group_op["value"] == "strawberry")

rec_op = next(o for o in patch["patches"] if o["json_path"].endswith(".varieties.recommended"))
check("varieties.recommended replace carries 9 varieties", rec_op["op"] == "replace" and len(rec_op["value"]) == 9)
sb = next(c for c in data["crops"] if c["slug"] == "strawberry")
check("varieties.recommended from-guard is verbatim the live legacy list",
      rec_op["from"] == sb["varieties"]["recommended"])

refs = [v["id"] for v in rec_op["value"] if v["is_reference"]]
check("exactly one flagship (albion)", refs == ["albion"])

ss_ops = [o for o in patch["patches"] if o["json_path"].endswith("source_set")]
check("source_set op presence matches source_set_op flag",
      (len(ss_ops) == 1) == (source_set_op == "emitted"))
if source_set_op == "skipped":
    cited = sorted({i for v in rec_op["value"] for i in v["sources"]})
    check("source_set genuinely introduces no new id (skip is correct)",
          set(cited) <= set(sb["verification_status"]["source_set"]))

# every hero op targets a variety that currently has no hero_description (or empty) in canonical.
for row in hero_rows:
    c = next(cc for cc in data["crops"] if cc["slug"] == row["slug"])
    v = next(x for x in c["varieties"]["recommended"] if x.get("id") == row["id"])
    check(f"{row['slug']}/{row['id']}: hero_description absent pre-patch",
          v.get("hero_description") in (None, ""))

# ---------------------------------------------------------------------------
# 2. Synthetic fixtures: source_set emit vs skip, em-dash rejection, clobber refusal,
#    flagship-count enforcement, duplicate-id rejection.
# ---------------------------------------------------------------------------
LEGACY_REC = [{"name": "Old One", "type": "june_bearing", "days_or_season": "early",
               "use": "fresh", "recommended_note": "legacy"}]


def synth_crop(source_set=("cornell_ext", "umn_ext")):
    return {
        "slug": "strawberry",
        "varieties": {"recommended": copy.deepcopy(LEGACY_REC), "note_beginner": "x", "note_seasoned": "y"},
        "verification_status": {"source_set": list(source_set)},
    }


def synth_variety(vid="honeoye", is_ref=False, sources=("umn_ext",), **overrides):
    v = {
        "id": vid, "name": vid.title(), "maturity_class": "early", "confidence_tier": "T1",
        "hero_description": "A fine berry.", "note_beginner": "beginner note.",
        "note_seasoned": "seasoned note.", "sources": list(sources),
        "anchoring_urls": {s: {"url": f"https://example.edu/{s}", "verified": "2026-07-15"} for s in sources},
        "bearing_habit": "june_bearing", "use": "fresh", "is_reference": is_ref,
    }
    v.update(overrides)
    return v


def nine_varieties(sources_per=(("umn_ext",),) * 9):
    # index 4 carries the hardcoded flagship id "albion" (build_strawberry_ops asserts on it,
    # mirroring every prior pilot's per-crop flagship-id assert: onion/super-star, leek/lancelot,
    # apple/golden-delicious).
    ids = ["v" + str(i) for i in range(9)]
    ids[4] = "albion"
    return [synth_variety(vid=ids[i], is_ref=(i == 4), sources=sources_per[i]) for i in range(9)]


# 2a. source_set SKIPPED when every cited id is already in the crop's source_set.
data_skip = {"crops": [synth_crop(source_set=("umn_ext", "cornell_ext"))]}
ops_skip, mode_skip = build_strawberry_ops(data_skip, nine_varieties())
check("synthetic: source_set SKIPPED when no new id introduced", mode_skip == "skipped")
check("synthetic: 3 ops when skipped (archetype+group+recommended)", len(ops_skip) == 3)

# 2b. source_set EMITTED when a variety cites a genuinely new id.
data_emit = {"crops": [synth_crop(source_set=("umn_ext",))]}
varieties_new_src = nine_varieties()
varieties_new_src[0]["sources"] = ["brand_new_ext"]
varieties_new_src[0]["anchoring_urls"] = {"brand_new_ext": {"url": "https://x.edu", "verified": "2026-07-15"}}
ops_emit, mode_emit = build_strawberry_ops(data_emit, varieties_new_src)
check("synthetic: source_set EMITTED when a new id is introduced", mode_emit == "emitted")
check("synthetic: 4 ops when emitted", len(ops_emit) == 4)
ss_op = next(o for o in ops_emit if o["json_path"].endswith("source_set"))
check("synthetic: emitted source_set value is the union, sorted",
      ss_op["value"] == sorted({"umn_ext", "brand_new_ext"}))
check("synthetic: emitted source_set from is the original list",
      ss_op["from"] == ["umn_ext"])

# 2c. exactly-one-flagship enforcement: 0 or 2+ flagships both raise.
no_flagship = nine_varieties()
for v in no_flagship:
    v["is_reference"] = False
check_raises("synthetic: 0 flagships raises",
             lambda: build_strawberry_ops({"crops": [synth_crop()]}, no_flagship))

two_flagship = nine_varieties()
two_flagship[0]["is_reference"] = True
two_flagship[4]["is_reference"] = True
check_raises("synthetic: 2 flagships raises",
             lambda: build_strawberry_ops({"crops": [synth_crop()]}, two_flagship))

# 2d. duplicate variety id raises.
dupe = nine_varieties()
dupe[1]["id"] = dupe[0]["id"]
check_raises("synthetic: duplicate variety id raises",
             lambda: build_strawberry_ops({"crops": [synth_crop()]}, dupe))

# 2e. wrong count (not 9) raises.
check_raises("synthetic: 8 varieties (not 9) raises",
             lambda: build_strawberry_ops({"crops": [synth_crop()]}, nine_varieties()[:8]))

# 2f. em dash in an authored variety string raises.
em_dash_variety = nine_varieties()
em_dash_variety[0]["hero_description"] = "A berry — with an em dash."
check_raises("synthetic: em dash in hero_description raises",
             lambda: build_strawberry_ops({"crops": [synth_crop()]}, em_dash_variety))

# 2g. missing required common-core/berry field raises.
missing_field = nine_varieties()
del missing_field[0]["bearing_habit"]
check_raises("synthetic: missing bearing_habit raises",
             lambda: build_strawberry_ops({"crops": [synth_crop()]}, missing_field))

# 2h. hero backfill: em dash in a staged hero line raises.
hero_ok = [{"slug": "strawberry", "id": "v0", "hero_description": "clean line."}]
hero_bad = [{"slug": "strawberry", "id": "v0", "hero_description": "a line — with a dash."}]


def crop_with_variety(hero_val=None):
    return {"crops": [{"slug": "strawberry",
                        "varieties": {"recommended": [{"id": "v0", "name": "V0",
                                                        "hero_description": hero_val}]}}]}


check("synthetic: clean hero backfill produces one add op",
      len(build_hero_ops(crop_with_variety(None), hero_ok)) == 1)
check_raises("synthetic: em dash in staged hero line raises",
             lambda: build_hero_ops(crop_with_variety(None), hero_bad))

# 2i. hero backfill refuses to clobber an already-present hero_description.
check_raises("synthetic: hero backfill refuses to clobber a present hero_description",
             lambda: build_hero_ops(crop_with_variety("already here"), hero_ok))

# 2j. hero backfill: unknown variety id raises (no silent skip).
hero_unknown = [{"slug": "strawberry", "id": "nonexistent", "hero_description": "clean."}]
check_raises("synthetic: hero backfill unknown variety id raises",
             lambda: build_hero_ops(crop_with_variety(None), hero_unknown))

# 2k. hero backfill: duplicate (slug,id) row raises.
hero_dupe = hero_ok + hero_ok
check_raises("synthetic: duplicate hero row raises",
             lambda: build_hero_ops(crop_with_variety(None), hero_dupe))

if fails:
    print(f"\n{len(fails)} test(s) FAILED: {fails}")
    sys.exit(1)
print("\nall build_berry_pilot_patch tests passed")
