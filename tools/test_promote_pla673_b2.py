"""Suite for promote_pla673_b2 (PLA-673 part B2: eggplant, the four squash soil_prep pairs, parsnip's three hilling
leaves; two document-level ids; A62 armed on soil_prep).

DEVIATION, recorded: the promote was derived (tools/staging/pla673_b2/derive_promote.py) before this suite existed.
Stand-ins: POST_SHA was computed by build_stage.py's INDEPENDENT minimal apply (no promote code) before the promote
ran, and mutate_promote_pla673_b2.py switches every guard off in turn. The pre-state is REPLAYED from its pinned commit
(promote_fixture: 3ccc25f1 -> fbe11bc), never read live.

One test runs the whole promote (gates included) on the real stage; every other test injects ONE defect and asserts its
refusal message, so a test cannot pass on an earlier, unrelated refusal.
"""
import copy, json, os, sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402
import promote_pla673_b2 as P  # noqa: E402
from cited_promote_common import Refused  # noqa: E402

BASE_SHA = "3ccc25f194cf0b3808877546b160572ab7ac6a12dbc7dae891f37d43f21a717a"
POST_SHA = "aaf004a23eb52005962c399d9f2f779b98b6226dacba0f454dff4442c1324812"  # usu_ext removed (was aeeb5789)
EGG = "diseases[id=phytophthora-blight]"
EGG_S, EGG_B = f"{EGG}.prevention_seasoned", f"{EGG}.prevention_beginner"
PGS = "growth_stages[id=established]"


@pytest.fixture(scope="module")
def pre():
    return json.loads(promote_fixture.pre_state(P.BASE_SHA))


@pytest.fixture(scope="module")
def stage():
    return P.load_stage(P.STAGE)


def _c(stage):
    return tuple(copy.deepcopy(x) for x in stage)


def _check(pre, ops, ev, dec, post=None):
    P.check_pre(pre, ops)
    post = P.apply_to(pre, ops) if post is None else post
    return P.check_post(pre, post, ops, ev, dec, P.EVIDENCE)


def _refuses(match, pre, ops, ev, dec, post=None):
    with pytest.raises(Refused, match=match):
        _check(pre, ops, ev, dec, post)


def _op(ops, crop, path):
    hits = [o for o in ops if o["crop"] == crop and o["path"] == path]
    assert len(hits) == 1, (crop, path)
    return hits[0]


def _retext(ops, ev, crop, path, old, new):
    o = _op(ops, crop, path)
    assert old in o["new"]
    o["new"] = o["new"].replace(old, new)
    for r in ev:
        if r["crop"] == crop and r["entry_id"] == path and old in r["value"]:
            r["value"] = r["value"].replace(old, new)


# ---------------------------------------------------------------- the real stage
def test_base_is_pinned():
    assert P.BASE_SHA == BASE_SHA


def test_real_stage_promotes_and_pins_its_populations(pre, stage):
    ops, ev, dec = stage
    post, n = P.run(pre, ops, ev, dec, P.EVIDENCE)
    assert (n["ops"], n["evidence_rows"], n["decisions"], n["gated_crops"]) == (34, 109, 6, 6)
    assert (n["register_pairs"], n["hill_inspected"]) == (16, 225)
    assert {o["crop"] for o in ops} == {"eggplant", "pumpkin", "butternut-squash", "acorn-squash", "spaghetti-squash",
                                        "parsnip", "<catalog>"}
    assert P.sha256_bytes(P.serialize(post)) == POST_SHA


def test_check_post_alone_passes(pre, stage):
    assert _check(pre, *_c(stage))["register_pairs"] == 16


# ---------------------------------------------------------------- loading / pre
def test_wrong_base(tmp_path, pre):
    p = tmp_path / "c.json"
    p.write_bytes(P.serialize(pre) + b" ")
    with pytest.raises(Refused, match="pinned to"):
        P.load_canonical(str(p))


def _stage_dir(tmp_path, ops):
    (tmp_path / "ops.json").write_text(json.dumps(ops), encoding="utf-8")
    return str(tmp_path)


def test_empty_stage(tmp_path):
    with pytest.raises(Refused, match="names no op"):
        P.load_stage(_stage_dir(tmp_path, []))


def test_op_keys_must_be_exact(tmp_path, stage):
    ops = copy.deepcopy(stage[0][:1]); ops[0]["x"] = 1
    with pytest.raises(Refused, match="keys must be exactly"):
        P.load_stage(_stage_dir(tmp_path, ops))


def test_unknown_kind(tmp_path, stage):
    ops = copy.deepcopy(stage[0][:1]); ops[0]["kind"] = "value"
    with pytest.raises(Refused, match="unknown kind"):
        P.load_stage(_stage_dir(tmp_path, ops))


def test_empty_reason(tmp_path, stage):
    ops = copy.deepcopy(stage[0][:1]); ops[0]["reason"] = ""
    with pytest.raises(Refused, match="empty reason"):
        P.load_stage(_stage_dir(tmp_path, ops))


def test_op_staged_twice(tmp_path, stage):
    with pytest.raises(Refused, match="staged twice"):
        P.load_stage(_stage_dir(tmp_path, copy.deepcopy(stage[0][:1]) * 2))


def test_drifted_base(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "eggplant", EGG_S)["old"] = "something else"
    with pytest.raises(Refused, match="base value is not the op's `old`"):
        P.check_pre(pre, ops)


def test_not_a_crop(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "eggplant", EGG_S)["crop"] = "ghost-crop"
    with pytest.raises(Refused, match="is not a crop"):
        P.check_pre(pre, ops)


# ---------------------------------------------------------------- guard B
def test_roster_change(pre, stage):
    post = P.apply_to(pre, stage[0]); post["crops"] = post["crops"][:-1]
    _refuses("roster changed", pre, *_c(stage), post=post)


def test_top_level_key_change(pre, stage):
    post = P.apply_to(pre, stage[0]); post["extra"] = 1
    _refuses("top-level keys changed", pre, *_c(stage), post=post)


def test_top_level_value_change(pre, stage):
    post = P.apply_to(pre, stage[0]); post["glossary"]["hill"]["term"] = "Hill"
    _refuses("top-level 'glossary' changed", pre, *_c(stage), post=post)


def test_stray_crop_change(pre, stage):
    post = P.apply_to(pre, stage[0]); P.by_slug(post)["parsnip"]["name"] = "Parsnips"
    _refuses("changed outside the staged ops", pre, *_c(stage), post=post)


def test_catalog_stray(pre, stage):
    post = P.apply_to(pre, stage[0]); post["source_catalog"]["umn_ext"]["tier"] = "T2"
    _refuses("source_catalog changed outside", pre, *_c(stage), post=post)


# ---------------------------------------------------------------- guard V / P
def test_post_value_not_new(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops)   # the post-state differs from `new` on a STAGED path (so guard B cannot fire)
    o = _op(ops, "pumpkin", "soil_prep_beginner")
    P.by_slug(post)["pumpkin"]["soil_prep_beginner"] = o["new"] + " Extra."
    _refuses("post value is not the op's `new`", pre, ops, ev, dec, post=post)


def test_noop(pre, stage):
    ops, ev, dec = _c(stage)
    o = _op(ops, "eggplant", EGG_S)
    o["new"] = o["old"]
    _refuses("a no-op", pre, ops, ev, dec)


def test_em_dash(pre, stage):
    ops, ev, dec = _c(stage)
    _retext(ops, ev, "eggplant", EGG_S, "key strategy", "key — strategy")
    _refuses("em or en dash", pre, ops, ev, dec)


def test_bare_degree(pre, stage):
    ops, ev, dec = _c(stage)
    _retext(ops, ev, "eggplant", EGG_S, "key strategy", "key strategy above 70 degrees")
    _refuses("without °F", pre, ops, ev, dec)


def test_null_prose(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "eggplant", EGG_S)["new"] = None
    _refuses("non-empty string", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard D
def test_decision_on_a_crop_not_in_the_roster(pre, stage):
    ops, ev, dec = _c(stage)
    dec.append({"crop": "ghost-crop", "path": "x", "decision": "y", "reason": "z"})
    _refuses("which is not a crop", pre, ops, ev, dec)


def test_prose_without_cited_at(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "eggplant", EGG_S)["cited_at"] = None
    _refuses("no cited_at and no record-only", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard E
def test_duplicate_row(pre, stage):
    ops, ev, dec = _c(stage)
    ev.append(dict(ev[0]))
    _refuses("duplicate row", pre, ops, ev, dec)


def test_row_on_an_unstaged_path(pre, stage):
    ops, ev, dec = _c(stage)
    ev.append(dict(ev[0], entry_id=f"{EGG}.symptoms_seasoned"))
    _refuses("not a staged prose", pre, ops, ev, dec)


def test_quote_not_in_bytes(pre, stage):
    ops, ev, dec = _c(stage)
    ev[0]["quote"] = "no such sentence anywhere on this page at all."
    _refuses("not in the cached bytes", pre, ops, ev, dec)


def test_url_not_cited_on_crop(pre, stage):
    ops, ev, dec = _c(stage)
    r = next(r for r in ev if r["crop"] == "eggplant")
    ev.append(dict(r, crop="parsnip", entry_id=f"{PGS}.user_action_seasoned", field="x"))
    _refuses("url is not cited anywhere on parsnip", pre, ops, ev, dec)


def test_block_anchor_missing(pre, stage):
    ops, ev, dec = _c(stage)
    a = _op(ops, "parsnip", f"{PGS}.anchoring_urls")["new"]
    a["rhs"] = dict(a["rhs"], url="https://www.rhs.org.uk/somewhere-else")
    _refuses("anchoring_urls does not carry rhs at the row's url|url is not cited", pre, ops, ev, dec)


def test_block_sources_missing(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "parsnip", f"{PGS}.sources")["new"].remove("rhs")
    _refuses("sources does not name rhs", pre, ops, ev, dec)


def test_prose_without_evidence(pre, stage):
    ops, ev, dec = _c(stage)
    ev = [r for r in ev if not (r["crop"] == "acorn-squash" and r["entry_id"] == "soil_prep_beginner")]
    _refuses("acorn-squash soil_prep_beginner: no EVIDENCE row", pre, ops, ev, dec)


def test_soil_prep_block_carries_the_row(pre, stage):
    """The crop-root soil_prep pair is the leaf's block: a row whose id the pair does not anchor refuses."""
    ops, ev, dec = _c(stage)
    _op(ops, "pumpkin", "soil_prep_anchoring_urls")["new"].pop("umn_ext")
    _op(ops, "pumpkin", "soil_prep_sources")["new"].remove("umn_ext")
    _refuses("<soil_prep>.anchoring_urls does not carry umn_ext|url is not cited", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard A
def _add_unused_anchor(ops):
    """An anchor + source on parsnip's canker entry that no evidence row uses (the pre-B2 usu_ext shape)."""
    _op(ops, "parsnip", "diseases[id=itersonilia-canker].sources")["new"].append("usu_ext")
    _op(ops, "parsnip", "diseases[id=itersonilia-canker].anchoring_urls")["new"]["usu_ext"] = {
        "url": "https://extension.usu.edu/planthealth/ipm/notes_ag/veg-list-root-crops", "verified": "2026-10-06"}


def test_unused_unkept_anchor(pre, stage):
    ops, ev, dec = _c(stage)
    _add_unused_anchor(ops)
    _refuses("anchor usu_ext supports no evidenced leaf", pre, ops, ev, dec)


def test_a_kept_decision_exempts_an_unused_anchor(pre, stage):
    """Positive control for the test above: the same anchor passes guard A with a `kept` row (it then passes all of
    check_post, so the refusal above is guard A's own)."""
    ops, ev, dec = _c(stage)
    _add_unused_anchor(ops)
    dec.append({"crop": "parsnip", "path": "diseases[id=itersonilia-canker].anchoring_urls.usu_ext",
                "decision": "kept", "reason": "test"})
    assert _check(pre, ops, ev, dec)["register_pairs"] == 16


def test_real_stage_cites_no_usu_on_parsnip(pre, stage):
    post = P.apply_to(pre, stage[0])
    p = P.by_slug(post)["parsnip"]
    d = next(x for x in p["diseases"] if x["id"] == "itersonilia-canker")
    assert d["sources"] == ["umass_ext_itersonilia_canker", "clemson_hgic"]
    assert list(d["anchoring_urls"]) == ["umass_ext_itersonilia_canker", "clemson_hgic"]


def test_sources_and_anchors_diverge(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "pumpkin", "soil_prep_sources")["new"].append("rhs")
    _refuses("sources and anchoring_urls name different ids", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard C
def test_catalog_id_must_match(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "<catalog>", "umass_ext_itersonilia_canker")["new"]["id"] = "umass_canker"
    _refuses("its id is 'umass_canker'", pre, ops, ev, dec)


def test_catalog_mint_must_be_evidenced(pre, stage):
    ops, ev, dec = _c(stage)
    ops.append({"crop": "<catalog>", "path": "ghost_mint", "kind": "catalog", "old": "<absent>",
                "new": {"id": "ghost_mint", "url": "https://example.edu/x"}, "cited_at": None, "reason": "t"})
    _refuses("ghost_mint: no EVIDENCE row cites it", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard R
def test_seasoned_without_its_beginner(pre, stage):
    ops, ev, dec = _c(stage)
    ops = [o for o in ops if not (o["crop"] == "eggplant" and o["path"] == EGG_B)]
    ev = [r for r in ev if not (r["crop"] == "eggplant" and r["entry_id"] == EGG_B)]
    _refuses("without its beginner sibling", pre, ops, ev, dec)


def test_byte_identical_registers(pre, stage):
    ops, ev, dec = _c(stage)
    s, b = _op(ops, "parsnip", f"{PGS}.user_action_seasoned"), _op(ops, "parsnip", f"{PGS}.user_action_beginner")
    b["new"] = s["new"]
    for r in ev:
        if r["crop"] == "parsnip" and r["entry_id"] == b["path"]:
            r["value"] = next(x["value"] for x in ev if x["entry_id"] == s["path"] and x["field"].split()[1] == r["field"].split()[1])
    _refuses("byte-identical", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard S
def test_soil_prep_restating_spacing(pre, stage):
    ops, ev, dec = _c(stage)
    _retext(ops, ev, "acorn-squash", "soil_prep_seasoned", "Form raised beds,",
            "Space plants 24 to 36 inches apart and form raised beds,")
    _refuses("restates a spacing", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard M
def test_match_unclassified(pre, stage):
    ops, ev, dec = _c(stage)
    _retext(ops, ev, "parsnip", f"{PGS}.user_action_seasoned", "Hill soil over", "Sow in hills, then hill soil over")
    _refuses("glossary match on the post roster", pre, ops, ev, dec)


def test_match_population_pinned(pre, stage, monkeypatch):
    ops, ev, dec = _c(stage)
    monkeypatch.setattr(P, "HILL_POPULATION", 224)
    _refuses("inspected 225 consumer leaves, not 224", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard G
class _R:
    def __init__(self, rc, out):
        self.returncode, self.stdout, self.stderr = rc, out, ""


def test_gate_failure(pre, stage, monkeypatch):
    monkeypatch.setattr(P.subprocess, "run", lambda *a, **k: _R(1, "GATE: 1 VIOLATION(S)"))
    with pytest.raises(Refused, match="whole_crop_gate .* rc=1"):
        P.gate_post(P.apply_to(pre, stage[0]), {"parsnip"})


def test_gate_count_is_the_gates_own_verdict(pre, stage, monkeypatch):
    monkeypatch.setattr(P.subprocess, "run", lambda *a, **k: _R(0, "no verdict printed"))
    with pytest.raises(Refused, match="PASS verdicts"):
        P.gate_post(P.apply_to(pre, stage[0]), {"parsnip"})


def test_gate_all_failure(pre, stage, monkeypatch):
    calls = []

    def fake(cmd, **k):
        calls.append(cmd)
        return _R(0, "\nGATE: PASS") if "whole_crop_gate.py" in cmd[1] else _R(1, "gate_all: 1 FAILED")
    monkeypatch.setattr(P.subprocess, "run", fake)
    with pytest.raises(Refused, match="gate_all rc=1"):
        P.gate_post(P.apply_to(pre, stage[0]), {"parsnip"})


def test_gate_all_population(pre, stage, monkeypatch):
    def fake(cmd, **k):
        return _R(0, "\nGATE: PASS") if "whole_crop_gate.py" in cmd[1] else _R(0, "all fine")
    monkeypatch.setattr(P.subprocess, "run", fake)
    with pytest.raises(Refused, match="did not report its population"):
        P.gate_post(P.apply_to(pre, stage[0]), {"parsnip"})
