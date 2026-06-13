#!/usr/bin/env python3
"""Tests for the hardened apply_patch -- the variants claude.ai actually emitted.
Run from repo root: python3 tools/test_apply_patch.py

History-reconstruction (the way apply_patch is validated): rebuild a prior base
from git and confirm the tool reproduces the patch's declared end-SHA / chains
forward. The `./` in `git show <sha>:./crops_data_final.json` is REQUIRED here.
"""
import json, os, sys, subprocess, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import apply_patch as ap

BUNDLE = os.path.expanduser(
    "~/Documents/plant-project/06-sessions/handoffs-bundles/m16-beefsteak-releases")


def git_base(commit):
    out = subprocess.run(["git", "show", f"{commit}:./crops_data_final.json"],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def canon_sha(data):
    return hashlib.sha256(
        json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def load_patch(rel):
    return json.load(open(os.path.join(BUNDLE, rel)))


# ============ UNIT: the envelope / op / field / path / sha pieces ============

# 1. envelope flattens _meta/corrections + reads start_sha + crop slug
wrapper = {"_meta": {"start_sha": "abc", "crop": "beefsteak-tomato"},
           "corrections": [{"id": "x", "changes": [
               {"op": "set_value", "path": "crops[beefsteak-tomato].regions.se_gulf",
                "before": "prose desc", "after": {"region_id": "se_gulf"}}]}]}
base_sha, edits, slug = ap.normalize_envelope(wrapper)
assert base_sha == "abc", base_sha
assert slug == "beefsteak-tomato", slug
assert len(edits) == 1 and edits[0]["op"] == "set_value", edits

# 1b. edit-list alias `ops` (carrot Step 5.5 drift) resolves like patches/edits/patch
_b, _e, _s = ap.normalize_envelope({"base_sha": "q", "ops": [
    {"op": "replace", "json_path": "$.x", "from": 1, "value": 2}]})
assert _b == "q" and len(_e) == 1 and _e[0]["op"] == "replace", ("ops alias", _e)

# 1c. `add` at list index == len APPENDS a new entry (carrot Step 5.5: new
# track:"succession" plantings entries onto a plantings[] that has only [0]).
_d = {"crops": [{"slug": "carrot", "regions": {"northern_tier": {"plantings": [{"track": "beginner"}]}}}]}
ap.apply_patch(_d, {"base_sha": "z", "ops": [
    {"op": "add", "json_path": "$.crops[?(@.slug=='carrot')].regions.northern_tier.plantings[1]",
     "value": {"track": "succession", "label": "spring"}},
    {"op": "add", "json_path": "$.crops[?(@.slug=='carrot')].regions.northern_tier.plantings[2]",
     "value": {"track": "succession", "label": "fall"}}]})
_pl = _d["crops"][0]["regions"]["northern_tier"]["plantings"]
assert len(_pl) == 3 and _pl[1]["label"] == "spring" and _pl[2]["label"] == "fall", ("append", _pl)

# 1d. JSON-Pointer crop-relative paths (peach Steps 1-3 drift): `/a` and `/a/b` resolve
# like dot-paths. claude.ai emitted RFC-6901 pointers (`path:"/sunlight"`,
# `"/soil/drainage_requirement"`); the applier must split on `/`, not treat it as one key.
_jp = {"crops": [{"slug": "peach", "sunlight": None, "soil": {"drainage_requirement": None},
                  "rootstock_options": [{"name": None}]}]}
ap.apply_patch(_jp, {"base_sha": "z", "crop": "peach", "ops": [
    {"op": "replace", "path": "/sunlight", "from": None, "value": "full sun"},
    {"op": "replace", "path": "/soil/drainage_requirement", "from": None, "value": "excellent"},
    {"op": "replace", "path": "/rootstock_options/0/name", "from": None, "value": "Lovell"}]})
_pk = _jp["crops"][0]
assert _pk["sunlight"] == "full sun", ("json-pointer top", _pk)
assert _pk["soil"]["drainage_requirement"] == "excellent", ("json-pointer nested", _pk)
assert _pk["rootstock_options"][0]["name"] == "Lovell", ("json-pointer array index", _pk)

# 1e. from-guard tolerates EMPTY-EQUIVALENT mismatch. The wipe types lists as [], dicts as {},
# scalars as null; claude.ai's drift `from:null` must not block filling an empty [] / {} slot
# (base_sha is the real drift gate). A populated cur vs from:null STILL halts.
_e = {"crops": [{"slug": "x", "sunlight_hours": [], "soil": {}}]}
ap.apply_patch(_e, {"base_sha": "z", "crop": "x", "ops": [
    {"op": "replace", "path": "/sunlight_hours", "from": None, "value": [8, 12]},
    {"op": "replace", "path": "/soil", "from": None, "value": {"texture": "loam"}}]})
assert _e["crops"][0]["sunlight_hours"] == [8, 12] and _e["crops"][0]["soil"] == {"texture": "loam"}, _e
# 1e-ii. NO-OP overwrite: a KEPT field (e.g. difficulty) survives the wipe populated; claude.ai
# re-authors it to the SAME value with from:null. cur==value -> no drift -> apply (no halt).
_k = {"crops": [{"slug": "x", "difficulty": "medium"}]}
ap.apply_patch(_k, {"base_sha": "z", "crop": "x", "ops": [
    {"op": "replace", "path": "/difficulty", "from": None, "value": "medium"}]})
assert _k["crops"][0]["difficulty"] == "medium", _k
# but a populated cur -> a DIFFERENT value with a wrong from:null STILL halts (real drift):
_d2 = {"crops": [{"slug": "x", "v": "already here"}]}
try:
    ap.apply_patch(_d2, {"base_sha": "z", "crop": "x", "ops": [
        {"op": "replace", "path": "/v", "from": None, "value": "new"}]})
    raise AssertionError("populated cur vs from:null should still FROM-GUARD halt")
except SystemExit:
    pass

# 1f. numeric JSON-Pointer token against a DICT resolves as a STRING KEY, not a list
# index (peach Step 4: `regions[r].resolved_by_zone` is keyed by zone-string "3".."11",
# so `/resolved_by_zone/3/suitability` must hit dict key "3", not list index [3]). The
# `/0/name` list case (test 1d) must still index a list -- the resolver branches on the
# actual node type (RFC-6901), so both coexist.
_rz_nt = {"resolved_by_zone": {"3": {"suitability": None}, "4": {"calendar": []}}}
_rz = {"crops": [{"slug": "peach", "regions": {"northern_tier": _rz_nt}}]}
ap.apply_patch(_rz, {"base_sha": "z", "crop": "peach", "ops": [
    {"op": "replace", "path": "/regions/northern_tier/resolved_by_zone/3/suitability",
     "from": None, "value": "unsuitable"},
    {"op": "replace", "path": "/regions/northern_tier/resolved_by_zone/4/calendar",
     "from": [], "value": ["dormant"]}]})
_nt = _rz["crops"][0]["regions"]["northern_tier"]["resolved_by_zone"]
assert _nt["3"]["suitability"] == "unsuitable", ("numeric dict-key traversal", _nt)
assert _nt["4"]["calendar"] == ["dormant"], ("numeric dict-key traversal 2", _nt)

# 1f-ii. a numeric dict key as the LEAF token (set/from-guard on the cell slot itself).
_lf = {"crops": [{"slug": "peach", "regions": {"se_gulf": {"resolved_by_zone": {"8": None}}}}]}
ap.apply_patch(_lf, {"base_sha": "z", "crop": "peach", "ops": [
    {"op": "replace", "path": "/regions/se_gulf/resolved_by_zone/8",
     "from": None, "value": {"suitability": "fruits_reliably"}}]})
assert _lf["crops"][0]["regions"]["se_gulf"]["resolved_by_zone"]["8"] == {"suitability": "fruits_reliably"}, ("numeric dict-key leaf", _lf)

# 2. set_value alias + `after` value + advisory `before` (no from-guard, sets anyway)
data = {"crops": [{"slug": "x", "regions": {"r": {"old": True}}}]}
ap.apply_patch(data, {"base_sha": "z", "patches": [
    {"op": "set_value", "json_path": "$.crops[?(@.slug=='x')].regions.r",
     "before": "a human description of the old shell", "after": {"new": 1}}]})
assert data["crops"][0]["regions"]["r"] == {"new": 1}, data

# 3. bracket-slug path crops[x] resolves like a slug filter (numeric index untouched)
data = {"crops": [{"slug": "x", "v": 1}, {"slug": "y", "v": 2}]}
ap.apply_patch(data, {"base_sha": "z", "patches": [
    {"op": "replace", "path": "crops[y].v", "value": 9}]})
assert data["crops"][1]["v"] == 9 and data["crops"][0]["v"] == 1, data

# 4. crop-relative $-rooted path is prefixed with the crop filter from the envelope
data = {"crops": [{"slug": "beefsteak-tomato", "pests": [{"cause_seasoned": "old"}]}]}
ap.apply_patch(data, {"_meta": {"crop": "beefsteak-tomato"}, "base_sha": "z", "patches": [
    {"op": "replace", "json_path": "$.pests[0].cause_seasoned", "value": "new"}]})
assert data["crops"][0]["pests"][0]["cause_seasoned"] == "new", data

# 5. bare crop-relative path + explicit slug arg
data = {"crops": [{"slug": "carrot", "regions": {"warm_arid": {"region_label": "old"}}}]}
ap.apply_patch(data, {"base_sha": "z", "patches": [
    {"op": "replace", "path": "regions.warm_arid.region_label", "value": "Warm Arid"}]},
    slug="carrot")
assert data["crops"][0]["regions"]["warm_arid"]["region_label"] == "Warm Arid", data

# 6. proposed-SHA dual-encoding verifier
txt = json.dumps({"t": "95°F"}, separators=(",", ":"), ensure_ascii=False)
canon = hashlib.sha256(txt.encode()).hexdigest()
asc = hashlib.sha256(json.dumps({"t": "95°F"}, separators=(",", ":"),
                                ensure_ascii=True).encode()).hexdigest()
assert "CANONICAL" in ap.verify_proposed_sha(txt, canon)
assert "ASCII-ESCAPED" in ap.verify_proposed_sha(txt, asc)
assert "NEITHER" in ap.verify_proposed_sha(txt, "0" * 64)

# 7. add still refuses to clobber a present non-null value (safety preserved)
data = {"crops": [{"slug": "x", "v": "present"}]}
try:
    ap.apply_patch(data, {"base_sha": "z", "patches": [
        {"op": "add", "json_path": "$.crops[?(@.slug=='x')].v", "value": "boom"}]})
    raise AssertionError("add onto present non-null should have exited")
except SystemExit:
    pass

# 7b. add onto an EMPTY-EQUIVALENT cur ([] / {} / "") PROCEEDS. The wipe types unpopulated
# list/dict/string scalars as [] / {} / "" (not null), and claude.ai emits op:add for them
# (basil Steps 1-3: days_to_maturity:[], sunlight_hours:[], spacing_inches:[], pests:[],
# diseases:[]). This mirrors the replace path's _is_empty tolerance (test 1e); the
# present-non-null safety guard (test 7) is unchanged.
_ae = {"crops": [{"slug": "x", "dtm": [], "soil": {}, "note": "", "n": None}]}
ap.apply_patch(_ae, {"base_sha": "z", "patches": [
    {"op": "add", "json_path": "$.crops[?(@.slug=='x')].dtm", "value": [60, 90]},
    {"op": "add", "json_path": "$.crops[?(@.slug=='x')].soil", "value": {"texture": "loam"}},
    {"op": "add", "json_path": "$.crops[?(@.slug=='x')].note", "value": "Genovese"},
    {"op": "add", "json_path": "$.crops[?(@.slug=='x')].n", "value": 5}]})
_x = _ae["crops"][0]
assert _x["dtm"] == [60, 90] and _x["soil"] == {"texture": "loam"} \
    and _x["note"] == "Genovese" and _x["n"] == 5, ("add onto empty-equiv", _x)

print("  unit: envelope/op/field/path/sha all PASS")

# ============ HISTORY: real archived patches reconstructed from git ============

# A. HARD -- beefsteak Step-4 _meta/corrections wrapper reproduces its _meta.end_sha.
patch4 = load_patch("step4_warm_regions/m16_beefsteak_step4_patch.json")
base4 = git_base("cf6da2c")                       # content 006cd0af == _meta.start_sha
assert canon_sha(base4) == patch4["_meta"]["start_sha"], "git base != Step-4 start_sha"
ap.apply_patch(base4, patch4)
got4 = canon_sha(base4)
assert got4 == patch4["_meta"]["end_sha"], f"Step-4 apply: got {got4}, want {patch4['_meta']['end_sha']}"
assert got4 == "a87932cd063f20f06863b3fd04b919909a6cfb7be220d78299d4ebb7962b413d", got4
# NOTE: intentionally NOT fc702ca's committed 3a482908 -- that commit hand-converted one
# warm_arid heat_pause.basis_seasoned "95 degrees F" -> "95degF" (an edit absent from the
# patch). The applier faithfully reproduces the patch; it does not author conversions.
print("  history A: Step-4 corrections wrapper -> a87932cd (== _meta.end_sha) PASS")

# B. CHAIN -- canonical-format step5 (full $.crops[...] paths) applies onto its git base.
patch5 = load_patch("step5_5_nt_cold_pause/m16_beefsteak_step5_patch.json")
base5 = git_base("fc702ca")                       # Step-4 committed; content 3a482908
assert canon_sha(base5) == patch5["base_sha"], f"step5 base mismatch: {canon_sha(base5)} != {patch5['base_sha']}"
n5 = ap.apply_patch(base5, patch5)
got5 = canon_sha(base5)
committed5 = canon_sha(git_base("423ee36"))        # Step 5.5 committed; content 8fdb3ee6
tag5 = "matches committed Step-5.5" if got5 == committed5 else "DIVERGES from committed (release-time hand-edit?)"
print(f"  history B: step5 applied {n5} canonical edits -> {got5[:8]} ({tag5})")

# C. CHAIN -- crop-relative steps678 ($.pests[0]... paths) applies with an explicit slug.
patch678 = load_patch("steps6_7_8_dualvoice/m16_beefsteak_steps678_patch.json")
base678 = git_base("423ee36")                      # Step 5.5 committed; content 8fdb3ee6
assert canon_sha(base678) == patch678["base_sha"], f"steps678 base mismatch: {canon_sha(base678)}"
n678 = ap.apply_patch(base678, patch678, slug="beefsteak-tomato")  # paths are crop-relative
got678 = canon_sha(base678)
committed678 = canon_sha(git_base("559cbe5"))      # Steps 6/7/8 committed; content e8b46da5
tag678 = "matches committed Steps-6/7/8" if got678 == committed678 else "DIVERGES from committed (release-time hand-edit?)"
print(f"  history C: steps678 applied {n678} crop-relative edits -> {got678[:8]} ({tag678})")

print("PASS apply_patch hardening")
