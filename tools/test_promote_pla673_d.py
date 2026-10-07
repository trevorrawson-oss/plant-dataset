"""Suite for promote_pla673_d (PLA-673 part D: the pepper Phytophthora blight entry on both peppers, watermelon's row
entry + mirror re-sourced to UF VH021, watermelon's thinning leaves).

DEVIATION, recorded: the promote was derived (tools/staging/pla673_d/derive_promote.py) before this suite existed.
Stand-ins: POST_SHA was computed by build_stage.py's INDEPENDENT minimal apply (no promote code) before the promote ran,
and mutate_promote_pla673_d.py switches every guard off in turn. The pre-state is REPLAYED from its pinned commit
(promote_fixture: aaf004a2 -> 6bce088), never read live.

One test runs the whole promote (gates included) on the real stage; every other test injects ONE defect and asserts its
refusal message, so a test cannot pass on an earlier, unrelated refusal.
"""
import copy, json, os, sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promote_fixture  # noqa: E402
import promote_pla673_d as P  # noqa: E402
from cited_promote_common import Refused  # noqa: E402

BASE_SHA = "aaf004a23eb52005962c399d9f2f779b98b6226dacba0f454dff4442c1324812"
POST_SHA = "5420479d85bb8b65be62fa459fd97b8ce12dfdf9d3951e455be52aadc7a98063"
PB = "diseases[id=phytophthora-blight]"
SYM_S, SYM_B = f"{PB}.symptoms_seasoned", f"{PB}.symptoms_beginner"
TIP_S, TIP_B = "thinning.tip_seasoned", "thinning.tip_beginner"
ROW = "planting_layout[id=row-none]"


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


def _both_peppers(ops, ev, path, old, new):
    for c in ("bell-pepper", "banana-pepper"):
        _retext(ops, ev, c, path, old, new)


# ---------------------------------------------------------------- the real stage
def test_base_is_pinned():
    assert P.BASE_SHA == BASE_SHA


def test_real_stage_promotes_and_pins_its_populations(pre, stage):
    ops, ev, dec = stage
    post, n = P.run(pre, ops, ev, dec, P.EVIDENCE)
    assert (n["ops"], n["evidence_rows"], n["decisions"], n["gated_crops"]) == (50, 176, 12, 3)
    assert (n["register_pairs"], n["hill_inspected"], n["identical"], n["mirrors"]) == (38, 224, 1, 1)
    assert {o["crop"] for o in ops} == {"bell-pepper", "banana-pepper", "watermelon"}
    assert P.sha256_bytes(P.serialize(post)) == POST_SHA


def test_real_stage_values_and_sources(pre, stage):
    post = P.apply_to(pre, stage[0])
    w = P.by_slug(post)["watermelon"]
    row = next(e for e in w["planting_layout"] if e["id"] == "row-none")
    assert (row["in_row_inches"], row["row_spacing_inches"], row["sources"]) == ([24, 48], [60, 60], ["uf_ifas"])
    assert w["spacing_inches"] == [24, 48] and w["row_spacing_inches"] == [96, 96]   # the hill entry's row mirror stays
    assert w["thinning"]["method"] == "thin to two plants per hill"
    assert w["thinning"]["to_spacing"] == "2 plants per hill"
    for c in ("bell-pepper", "banana-pepper"):
        d = next(x for x in P.by_slug(post)[c]["diseases"] if x["id"] == "phytophthora-blight")
        assert d["sources"] == ["ncsu_ext_phytophthora_blight_peppers", "umn_ext"]


def test_check_post_alone_passes(pre, stage):
    assert _check(pre, *_c(stage))["register_pairs"] == 38


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
    ops = copy.deepcopy(stage[0][:1]); ops[0]["kind"] = "orthography"
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
    _op(ops, "watermelon", f"{ROW}.in_row_inches")["old"] = [60, 70]
    with pytest.raises(Refused, match="base value is not the op's `old`"):
        P.check_pre(pre, ops)


def test_not_a_crop(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "watermelon", TIP_S)["crop"] = "ghost-crop"
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
    post = P.apply_to(pre, stage[0]); P.by_slug(post)["watermelon"]["name"] = "Watermelons"
    _refuses("changed outside the staged ops", pre, *_c(stage), post=post)


def test_catalog_stray(pre, stage):
    post = P.apply_to(pre, stage[0]); post["source_catalog"]["uf_ifas"]["tier"] = "T2"
    _refuses("source_catalog changed outside", pre, *_c(stage), post=post)


# ---------------------------------------------------------------- guard V / P
def test_post_value_not_new(pre, stage):
    ops, ev, dec = _c(stage)
    post = P.apply_to(pre, ops)   # the post differs from `new` on a STAGED path (so guard B cannot fire)
    row = next(e for e in P.by_slug(post)["watermelon"]["planting_layout"] if e["id"] == "row-none")
    row["row_spacing_inches"] = [60, 72]
    _refuses("post value is not the op's `new`", pre, ops, ev, dec, post=post)


def test_noop(pre, stage):
    ops, ev, dec = _c(stage)
    o = _op(ops, "watermelon", "thinning.method")
    o["new"] = o["old"]
    _refuses("a no-op", pre, ops, ev, dec)


def test_em_dash(pre, stage):
    ops, ev, dec = _c(stage)
    _both_peppers(ops, ev, SYM_S, "turn dark brown", "turn dark brown — fast")
    _refuses("em or en dash", pre, ops, ev, dec)


def test_bare_degree(pre, stage):
    ops, ev, dec = _c(stage)
    _both_peppers(ops, ev, SYM_S, "75 to 90°F", "75 to 90 degrees")
    _refuses("without °F", pre, ops, ev, dec)


def test_null_prose(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "watermelon", "thinning.method")["new"] = None
    _refuses("non-empty string", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard D
def test_decision_on_a_crop_not_in_the_roster(pre, stage):
    ops, ev, dec = _c(stage)
    dec.append({"crop": "ghost-crop", "path": "x", "decision": "y", "reason": "z"})
    _refuses("which is not a crop", pre, ops, ev, dec)


def test_prose_without_cited_at(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "watermelon", TIP_S)["cited_at"] = None
    _refuses("no cited_at and no record-only", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard E
def test_duplicate_row(pre, stage):
    ops, ev, dec = _c(stage)
    ev.append(dict(ev[0]))
    _refuses("duplicate row", pre, ops, ev, dec)


def test_row_on_an_unstaged_path(pre, stage):
    ops, ev, dec = _c(stage)
    ev.append(dict(ev[0], entry_id="thinning.when"))
    _refuses("not a staged prose / value op", pre, ops, ev, dec)


def test_quote_not_in_bytes(pre, stage):
    ops, ev, dec = _c(stage)
    ev[0]["quote"] = "no such sentence anywhere on this page at all."
    _refuses("not in the cached bytes", pre, ops, ev, dec)


def test_url_not_cited_on_crop(pre, stage):
    ops, ev, dec = _c(stage)
    r = next(r for r in ev if r["crop"] == "bell-pepper" and r["source_id"] == "ncsu_ext_phytophthora_blight_peppers")
    ev.append(dict(r, crop="watermelon", entry_id=TIP_S, field="x"))
    _refuses("url is not cited anywhere on watermelon", pre, ops, ev, dec)


def test_block_anchor_missing(pre, stage):
    ops, ev, dec = _c(stage)
    a = _op(ops, "watermelon", "thinning.anchoring_urls")["new"]
    a["uga_ext"] = dict(a["uga_ext"], url="https://fieldreport.caes.uga.edu/publications/C1036/")
    _refuses("anchoring_urls does not carry uga_ext at the row's url|url is not cited", pre, ops, ev, dec)


def test_block_sources_missing(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "watermelon", "thinning.sources")["new"].remove("uga_ext")
    _refuses("sources does not name uga_ext", pre, ops, ev, dec)


def test_prose_without_evidence(pre, stage):
    ops, ev, dec = _c(stage)
    ev = [r for r in ev if not (r["crop"] == "banana-pepper" and r["entry_id"] == SYM_B)]
    _refuses(f"banana-pepper {SYM_B.replace('[', '.').replace(']', '.')}: no EVIDENCE row", pre, ops, ev, dec)


def test_value_without_evidence(pre, stage):
    """Value ops are evidenced too: the mirror op loses its rows."""
    ops, ev, dec = _c(stage)
    ev = [r for r in ev if not (r["crop"] == "watermelon" and r["entry_id"] == "spacing_inches")]
    _refuses("watermelon spacing_inches: no EVIDENCE row", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard A
def _add_unused_anchor(ops):
    """clemson_hgic back on the pepper entry with no evidence row using it (the pre-part-D shape)."""
    _op(ops, "bell-pepper", f"{PB}.sources")["new"].append("clemson_hgic")
    _op(ops, "bell-pepper", f"{PB}.anchoring_urls")["new"]["clemson_hgic"] = {
        "url": "https://hgic.clemson.edu/factsheet/pepper/", "verified": "2026-10-06"}
    _op(ops, "banana-pepper", f"{PB}.sources")["new"].append("clemson_hgic")
    _op(ops, "banana-pepper", f"{PB}.anchoring_urls")["new"]["clemson_hgic"] = {
        "url": "https://hgic.clemson.edu/factsheet/pepper/", "verified": "2026-10-06"}


def test_unused_unkept_anchor(pre, stage):
    ops, ev, dec = _c(stage)
    _add_unused_anchor(ops)
    _refuses("anchor clemson_hgic supports no evidenced leaf", pre, ops, ev, dec)


def test_a_kept_decision_exempts_an_unused_anchor(pre, stage):
    """Positive control for the test above: with `kept` rows the same anchors pass all of check_post."""
    ops, ev, dec = _c(stage)
    _add_unused_anchor(ops)
    for c in ("bell-pepper", "banana-pepper"):
        dec.append({"crop": c, "path": f"{PB}.anchoring_urls.clemson_hgic", "decision": "kept", "reason": "test"})
    assert _check(pre, ops, ev, dec)["identical"] == 1


def test_sources_and_anchors_diverge(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "watermelon", f"{ROW}.sources")["new"].append("rhs")
    _refuses("sources and anchoring_urls name different ids", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard C
def _catalog_op(new):
    return {"crop": "<catalog>", "path": "ghost_mint", "kind": "catalog", "old": "<absent>", "new": new,
            "cited_at": None, "reason": "t"}


def test_catalog_id_must_match(pre, stage):
    ops, ev, dec = _c(stage)
    ops.append(_catalog_op({"id": "other_id", "url": "https://example.edu/x"}))
    _refuses("its id is 'other_id'", pre, ops, ev, dec)


def test_catalog_mint_must_be_evidenced(pre, stage):
    ops, ev, dec = _c(stage)
    ops.append(_catalog_op({"id": "ghost_mint", "url": "https://example.edu/x"}))
    _refuses("ghost_mint: no EVIDENCE row cites it", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard R
def test_seasoned_without_its_beginner(pre, stage):
    ops, ev, dec = _c(stage)
    ops = [o for o in ops if not (o["crop"] == "watermelon" and o["path"] == TIP_B)]
    ev = [r for r in ev if not (r["crop"] == "watermelon" and r["entry_id"] == TIP_B)]
    _refuses("without its beginner sibling", pre, ops, ev, dec)


def test_byte_identical_registers(pre, stage):
    ops, ev, dec = _c(stage)
    s, b = _op(ops, "watermelon", TIP_S), _op(ops, "watermelon", TIP_B)
    b["new"] = s["new"]
    for r in ev:
        if r["crop"] == "watermelon" and r["entry_id"] == TIP_B:
            r["value"] = next(x["value"] for x in ev if x["entry_id"] == TIP_S
                              and x["field"].split()[1] == r["field"].split()[1])
    _refuses("byte-identical", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard I
def test_peppers_must_stay_identical(pre, stage):
    ops, ev, dec = _c(stage)
    _retext(ops, ev, "banana-pepper", SYM_B, "In wet weather,", "In wet spells,")
    _refuses("not identical across", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard X
def test_mirror_must_follow_the_row_entry(pre, stage):
    ops, ev, dec = _c(stage)
    _op(ops, "watermelon", "spacing_inches")["new"] = [24, 36]
    for r in ev:
        if r["crop"] == "watermelon" and r["entry_id"] == "spacing_inches":
            r["value"] = "[24, 36]"
    _refuses("is not the mirror", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard M
def test_match_unclassified(pre, stage):
    ops, ev, dec = _c(stage)
    _retext(ops, ev, "watermelon", TIP_S, "Sow four to five seeds per hill.",
            "Sow four to five seeds per hill, then hill soil up.")
    _refuses("glossary match on the post roster", pre, ops, ev, dec)


def test_match_population_pinned(pre, stage, monkeypatch):
    ops, ev, dec = _c(stage)
    monkeypatch.setattr(P, "HILL_POPULATION", 223)
    _refuses("inspected 224 consumer leaves, not 223", pre, ops, ev, dec)


# ---------------------------------------------------------------- guard G
class _R:
    def __init__(self, rc, out):
        self.returncode, self.stdout, self.stderr = rc, out, ""


def test_gate_failure(pre, stage, monkeypatch):
    monkeypatch.setattr(P.subprocess, "run", lambda *a, **k: _R(1, "GATE: 1 VIOLATION(S)"))
    with pytest.raises(Refused, match="whole_crop_gate .* rc=1"):
        P.gate_post(P.apply_to(pre, stage[0]), {"watermelon"})


def test_gate_count_is_the_gates_own_verdict(pre, stage, monkeypatch):
    monkeypatch.setattr(P.subprocess, "run", lambda *a, **k: _R(0, "no verdict printed"))
    with pytest.raises(Refused, match="PASS verdicts"):
        P.gate_post(P.apply_to(pre, stage[0]), {"watermelon"})


def test_gate_all_failure(pre, stage, monkeypatch):
    def fake(cmd, **k):
        return _R(0, "\nGATE: PASS") if "whole_crop_gate.py" in cmd[1] else _R(1, "gate_all: 1 FAILED")
    monkeypatch.setattr(P.subprocess, "run", fake)
    with pytest.raises(Refused, match="gate_all rc=1"):
        P.gate_post(P.apply_to(pre, stage[0]), {"watermelon"})


def test_gate_all_population(pre, stage, monkeypatch):
    def fake(cmd, **k):
        return _R(0, "\nGATE: PASS") if "whole_crop_gate.py" in cmd[1] else _R(0, "all fine")
    monkeypatch.setattr(P.subprocess, "run", fake)
    with pytest.raises(Refused, match="did not report its population"):
        P.gate_post(P.apply_to(pre, stage[0]), {"watermelon"})
