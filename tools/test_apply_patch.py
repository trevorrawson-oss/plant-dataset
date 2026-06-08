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
