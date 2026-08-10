#!/usr/bin/env python3
"""Tests for the hardened apply_patch -- the variants claude.ai actually emitted.

CONVERTED TO REAL TESTS (PLA-162). The previous version of this file defined ZERO test
functions: ~30 module-level assertions ran only as a side effect of pytest's collection
import, contributed nothing to any pass count, could not be selected individually, and its
out-of-repo fixture path turned into a collection ERROR (not a failure) the day that
directory moved. This is the tool that WRITES CANONICAL -- its guards run as first-class,
selectable, countable tests now, and the three archived patches it replays are VENDORED
under tools/fixtures/apply_patch/ so the suite cannot rot with a home directory.

History-reconstruction (the way apply_patch is validated): rebuild a prior base from git and
confirm the tool reproduces the patch's declared end-SHA / chains forward onto the next
committed state. The `./` in `git show <sha>:./crops_data_final.json` is REQUIRED here.

    python3 -m pytest tools/test_apply_patch.py -q
"""
import hashlib
import json
import os
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import apply_patch as ap  # noqa: E402

FIXTURES = os.path.join(HERE, 'fixtures', 'apply_patch')


def git_base(commit):
    out = subprocess.run(["git", "show", f"{commit}:./crops_data_final.json"],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def canon_sha(data):
    return hashlib.sha256(
        json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def load_patch(name):
    with open(os.path.join(FIXTURES, name)) as fh:
        return json.load(fh)


# ============ UNIT: the envelope / op / field / path / sha pieces ============

def test_envelope_flattens_meta_corrections_and_reads_slug():
    wrapper = {"_meta": {"start_sha": "abc", "crop": "beefsteak-tomato"},
               "corrections": [{"id": "x", "changes": [
                   {"op": "set_value", "path": "crops[beefsteak-tomato].regions.se_gulf",
                    "before": "prose desc", "after": {"region_id": "se_gulf"}}]}]}
    base_sha, edits, slug = ap.normalize_envelope(wrapper)
    assert base_sha == "abc", base_sha
    assert slug == "beefsteak-tomato", slug
    assert len(edits) == 1 and edits[0]["op"] == "set_value", edits


def test_ops_alias_resolves_like_patches():
    """Edit-list alias `ops` (carrot Step 5.5 drift) resolves like patches/edits/patch."""
    b, e, _s = ap.normalize_envelope({"base_sha": "q", "ops": [
        {"op": "replace", "json_path": "$.x", "from": 1, "value": 2}]})
    assert b == "q" and len(e) == 1 and e[0]["op"] == "replace", ("ops alias", e)


def test_add_at_list_index_equal_to_len_appends():
    """carrot Step 5.5: new track:"succession" plantings entries onto a plantings[] of [0]."""
    d = {"crops": [{"slug": "carrot",
                    "regions": {"northern_tier": {"plantings": [{"track": "beginner"}]}}}]}
    ap.apply_patch(d, {"base_sha": "z", "ops": [
        {"op": "add",
         "json_path": "$.crops[?(@.slug=='carrot')].regions.northern_tier.plantings[1]",
         "value": {"track": "succession", "label": "spring"}},
        {"op": "add",
         "json_path": "$.crops[?(@.slug=='carrot')].regions.northern_tier.plantings[2]",
         "value": {"track": "succession", "label": "fall"}}]})
    pl = d["crops"][0]["regions"]["northern_tier"]["plantings"]
    assert len(pl) == 3 and pl[1]["label"] == "spring" and pl[2]["label"] == "fall", pl


def test_json_pointer_crop_relative_paths_resolve():
    """peach Steps 1-3 drift: RFC-6901 pointers must split on '/', not read as one key."""
    d = {"crops": [{"slug": "peach", "sunlight": None, "soil": {"drainage_requirement": None},
                    "rootstock_options": [{"name": None}]}]}
    ap.apply_patch(d, {"base_sha": "z", "crop": "peach", "ops": [
        {"op": "replace", "path": "/sunlight", "from": None, "value": "full sun"},
        {"op": "replace", "path": "/soil/drainage_requirement", "from": None,
         "value": "excellent"},
        {"op": "replace", "path": "/rootstock_options/0/name", "from": None,
         "value": "Lovell"}]})
    pk = d["crops"][0]
    assert pk["sunlight"] == "full sun", ("json-pointer top", pk)
    assert pk["soil"]["drainage_requirement"] == "excellent", ("json-pointer nested", pk)
    assert pk["rootstock_options"][0]["name"] == "Lovell", ("json-pointer array index", pk)


def test_from_guard_tolerates_empty_equivalent_mismatch():
    """The wipe types lists as [], dicts as {}, scalars as null; drift `from:null` must not
    block filling an empty slot (base_sha is the real drift gate)."""
    e = {"crops": [{"slug": "x", "sunlight_hours": [], "soil": {}}]}
    ap.apply_patch(e, {"base_sha": "z", "crop": "x", "ops": [
        {"op": "replace", "path": "/sunlight_hours", "from": None, "value": [8, 12]},
        {"op": "replace", "path": "/soil", "from": None, "value": {"texture": "loam"}}]})
    assert e["crops"][0]["sunlight_hours"] == [8, 12]
    assert e["crops"][0]["soil"] == {"texture": "loam"}


def test_noop_overwrite_of_a_kept_field_applies_without_halt():
    """claude.ai re-authors a KEPT field to the SAME value with from:null -- no drift."""
    k = {"crops": [{"slug": "x", "difficulty": "medium"}]}
    ap.apply_patch(k, {"base_sha": "z", "crop": "x", "ops": [
        {"op": "replace", "path": "/difficulty", "from": None, "value": "medium"}]})
    assert k["crops"][0]["difficulty"] == "medium", k


def test_populated_cur_vs_from_null_still_halts():
    """Real drift: a populated current value changed to something ELSE must FROM-GUARD halt."""
    d = {"crops": [{"slug": "x", "v": "already here"}]}
    with pytest.raises(SystemExit):
        ap.apply_patch(d, {"base_sha": "z", "crop": "x", "ops": [
            {"op": "replace", "path": "/v", "from": None, "value": "new"}]})


def test_numeric_pointer_token_against_a_dict_is_a_string_key():
    """peach Step 4: resolved_by_zone is keyed "3".."11" -- /resolved_by_zone/3 must hit dict
    key "3", not list index [3]; the /0/name list case must still index a list."""
    rz_nt = {"resolved_by_zone": {"3": {"suitability": None}, "4": {"calendar": []}}}
    rz = {"crops": [{"slug": "peach", "regions": {"northern_tier": rz_nt}}]}
    ap.apply_patch(rz, {"base_sha": "z", "crop": "peach", "ops": [
        {"op": "replace", "path": "/regions/northern_tier/resolved_by_zone/3/suitability",
         "from": None, "value": "unsuitable"},
        {"op": "replace", "path": "/regions/northern_tier/resolved_by_zone/4/calendar",
         "from": [], "value": ["dormant"]}]})
    nt = rz["crops"][0]["regions"]["northern_tier"]["resolved_by_zone"]
    assert nt["3"]["suitability"] == "unsuitable", ("numeric dict-key traversal", nt)
    assert nt["4"]["calendar"] == ["dormant"], ("numeric dict-key traversal 2", nt)


def test_numeric_dict_key_as_the_leaf_token():
    lf = {"crops": [{"slug": "peach",
                     "regions": {"se_gulf": {"resolved_by_zone": {"8": None}}}}]}
    ap.apply_patch(lf, {"base_sha": "z", "crop": "peach", "ops": [
        {"op": "replace", "path": "/regions/se_gulf/resolved_by_zone/8",
         "from": None, "value": {"suitability": "fruits_reliably"}}]})
    cell = lf["crops"][0]["regions"]["se_gulf"]["resolved_by_zone"]["8"]
    assert cell == {"suitability": "fruits_reliably"}, ("numeric dict-key leaf", lf)


def test_set_value_alias_with_advisory_before():
    """`before` is advisory (no from-guard); `after` is the value."""
    data = {"crops": [{"slug": "x", "regions": {"r": {"old": True}}}]}
    ap.apply_patch(data, {"base_sha": "z", "patches": [
        {"op": "set_value", "json_path": "$.crops[?(@.slug=='x')].regions.r",
         "before": "a human description of the old shell", "after": {"new": 1}}]})
    assert data["crops"][0]["regions"]["r"] == {"new": 1}, data


def test_bracket_slug_path_resolves_like_a_slug_filter():
    data = {"crops": [{"slug": "x", "v": 1}, {"slug": "y", "v": 2}]}
    ap.apply_patch(data, {"base_sha": "z", "patches": [
        {"op": "replace", "path": "crops[y].v", "value": 9}]})
    assert data["crops"][1]["v"] == 9 and data["crops"][0]["v"] == 1, data


def test_crop_relative_dollar_path_gets_the_envelope_crop_prefix():
    data = {"crops": [{"slug": "beefsteak-tomato", "pests": [{"cause_seasoned": "old"}]}]}
    ap.apply_patch(data, {"_meta": {"crop": "beefsteak-tomato"}, "base_sha": "z", "patches": [
        {"op": "replace", "json_path": "$.pests[0].cause_seasoned", "value": "new"}]})
    assert data["crops"][0]["pests"][0]["cause_seasoned"] == "new", data


def test_bare_crop_relative_path_with_explicit_slug_arg():
    data = {"crops": [{"slug": "carrot", "regions": {"warm_arid": {"region_label": "old"}}}]}
    ap.apply_patch(data, {"base_sha": "z", "patches": [
        {"op": "replace", "path": "regions.warm_arid.region_label", "value": "Warm Arid"}]},
        slug="carrot")
    assert data["crops"][0]["regions"]["warm_arid"]["region_label"] == "Warm Arid", data


def test_proposed_sha_dual_encoding_verifier():
    txt = json.dumps({"t": "95°F"}, separators=(",", ":"), ensure_ascii=False)
    canon = hashlib.sha256(txt.encode()).hexdigest()
    asc = hashlib.sha256(json.dumps({"t": "95°F"}, separators=(",", ":"),
                                    ensure_ascii=True).encode()).hexdigest()
    assert "CANONICAL" in ap.verify_proposed_sha(txt, canon)
    assert "ASCII-ESCAPED" in ap.verify_proposed_sha(txt, asc)
    assert "NEITHER" in ap.verify_proposed_sha(txt, "0" * 64)


def test_add_refuses_to_clobber_a_present_non_null_value():
    data = {"crops": [{"slug": "x", "v": "present"}]}
    with pytest.raises(SystemExit):
        ap.apply_patch(data, {"base_sha": "z", "patches": [
            {"op": "add", "json_path": "$.crops[?(@.slug=='x')].v", "value": "boom"}]})


def test_add_onto_empty_equivalent_proceeds():
    """basil Steps 1-3: the wipe types unpopulated list/dict/string slots as []/{}/"" (not
    null) and claude.ai emits op:add for them. Mirrors the replace path's tolerance; the
    present-non-null safety guard is unchanged."""
    ae = {"crops": [{"slug": "x", "dtm": [], "soil": {}, "note": "", "n": None}]}
    ap.apply_patch(ae, {"base_sha": "z", "patches": [
        {"op": "add", "json_path": "$.crops[?(@.slug=='x')].dtm", "value": [60, 90]},
        {"op": "add", "json_path": "$.crops[?(@.slug=='x')].soil",
         "value": {"texture": "loam"}},
        {"op": "add", "json_path": "$.crops[?(@.slug=='x')].note", "value": "Genovese"},
        {"op": "add", "json_path": "$.crops[?(@.slug=='x')].n", "value": 5}]})
    x = ae["crops"][0]
    assert x["dtm"] == [60, 90] and x["soil"] == {"texture": "loam"}
    assert x["note"] == "Genovese" and x["n"] == 5, ("add onto empty-equiv", x)


def test_add_onto_recursively_empty_block_proceeds_but_a_real_leaf_halts():
    """The schema-2.9 migration scaffolded universal blocks as null-KEYED dicts (NOT {}), so
    _is_empty must recurse (microgreens-mix Steps 1-3, whole-block adds). A block carrying
    ANY real leaf still halts -- the clobber guard is intact."""
    re_ = {"crops": [{"slug": "x",
                      "watering": {"method_seasoned": None, "amount_beginner": None,
                                   "drainage": {"holes": None, "gravel": None},
                                   "sources": [], "anchoring_urls": {}},
                      "occupied": {"method_seasoned": None, "self_watering_ok": False}}]}
    ap.apply_patch(re_, {"base_sha": "z", "patches": [
        {"op": "add", "json_path": "$.crops[?(@.slug=='x')].watering",
         "value": {"method_seasoned": "bottom-water", "amount_beginner": "keep moist"}}]})
    assert re_["crops"][0]["watering"] == {"method_seasoned": "bottom-water",
                                           "amount_beginner": "keep moist"}
    with pytest.raises(SystemExit):
        ap.apply_patch(re_, {"base_sha": "z", "patches": [
            {"op": "add", "json_path": "$.crops[?(@.slug=='x')].occupied",
             "value": {"x": 1}}]})


# ============ HISTORY: real archived patches reconstructed from git ============

def test_history_A_step4_corrections_wrapper_reproduces_its_declared_end_sha():
    """HARD -- beefsteak Step-4 _meta/corrections wrapper reproduces _meta.end_sha.

    Intentionally NOT fc702ca's committed 3a482908: that commit hand-converted one warm_arid
    heat_pause.basis_seasoned "95 degrees F" -> "95degF" (an edit absent from the patch). The
    applier faithfully reproduces the patch; it does not author conversions."""
    patch4 = load_patch("m16_beefsteak_step4_patch.json")
    base4 = git_base("cf6da2c")                   # content 006cd0af == _meta.start_sha
    assert canon_sha(base4) == patch4["_meta"]["start_sha"], "git base != Step-4 start_sha"
    ap.apply_patch(base4, patch4)
    got4 = canon_sha(base4)
    assert got4 == patch4["_meta"]["end_sha"], \
        f"Step-4 apply: got {got4}, want {patch4['_meta']['end_sha']}"
    assert got4 == "a87932cd063f20f06863b3fd04b919909a6cfb7be220d78299d4ebb7962b413d", got4


def test_history_B_step5_chain_matches_the_committed_state():
    """CHAIN -- canonical-format step5 (full $.crops[...] paths) applies onto its git base
    and reproduces the COMMITTED Step-5.5 state byte-for-byte. The previous version of this
    file only PRINTED whether these matched; asserting it is the whole point."""
    patch5 = load_patch("m16_beefsteak_step5_patch.json")
    base5 = git_base("fc702ca")                   # Step-4 committed; content 3a482908
    assert canon_sha(base5) == patch5["base_sha"], \
        f"step5 base mismatch: {canon_sha(base5)} != {patch5['base_sha']}"
    n5 = ap.apply_patch(base5, patch5)
    assert n5 == 22, f"step5 should apply 22 canonical edits, applied {n5}"
    committed5 = canon_sha(git_base("423ee36"))   # Step 5.5 committed; content 8fdb3ee6
    assert canon_sha(base5) == committed5, \
        'step5 apply DIVERGES from the committed Step-5.5 state'


def test_history_C_steps678_chain_matches_the_committed_state():
    """CHAIN -- crop-relative steps678 ($.pests[0]... paths) applies with an explicit slug
    and reproduces the COMMITTED Steps-6/7/8 state byte-for-byte."""
    patch678 = load_patch("m16_beefsteak_steps678_patch.json")
    base678 = git_base("423ee36")                 # Step 5.5 committed; content 8fdb3ee6
    assert canon_sha(base678) == patch678["base_sha"], \
        f"steps678 base mismatch: {canon_sha(base678)}"
    n678 = ap.apply_patch(base678, patch678, slug="beefsteak-tomato")
    assert n678 == 42, f"steps678 should apply 42 crop-relative edits, applied {n678}"
    committed678 = canon_sha(git_base("559cbe5"))  # Steps 6/7/8 committed; content e8b46da5
    assert canon_sha(base678) == committed678, \
        'steps678 apply DIVERGES from the committed Steps-6/7/8 state'


def test_vendored_fixtures_are_the_archived_bundle_bytes():
    """The three patches were vendored 2026-08-10 from
    ~/Documents/plant-project/06-sessions/handoffs-bundles/m16-beefsteak-releases. Pin their
    hashes so a corrupted or regenerated fixture cannot silently change what the history
    tests replay."""
    expected = {
        'm16_beefsteak_step4_patch.json':
            '8ad0a9237c7e9bab188b99c767c3cd49d0735f8f9afb5ee2bbfe6c24c57cecb5',
        'm16_beefsteak_step5_patch.json':
            '1a0a3e0137807693c3c9b1e6cd7c41de5ee25bb91beae94e0df59776ffc45f92',
        'm16_beefsteak_steps678_patch.json':
            'b558af9bc72ddbe357d0be9d549eccc4750cf05a7f0c4fe6200f2ee31abb1278',
    }
    for name, want in expected.items():
        with open(os.path.join(FIXTURES, name), 'rb') as fh:
            got = hashlib.sha256(fh.read()).hexdigest()
        assert got == want, f'{name} does not match the archived bundle ({got})'


if __name__ == '__main__':
    raise SystemExit(pytest.main([__file__, '-q']))
